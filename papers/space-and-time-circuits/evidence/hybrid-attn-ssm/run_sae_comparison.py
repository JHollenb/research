#!/usr/bin/env python
"""SAE feature ablation vs. per-layer / whole-path interventions.

Standalone, public reproduction script for the preregistered experiment
"SAE feature ablation vs. per-layer and whole-path interventions".

It compares, on a fixed panel of small language models, whether a standard
sparse-autoencoder workflow (SAELens public pretrained SAEs) identifies
components whose ablation removes a prompt-controlled behavior, against
per-layer key/value swaps, layer-range key/value swaps, and single-layer
residual-stream swaps.

Only plain PyTorch + Hugging Face Transformers + SAELens are used. SAELens is
used *only* to load pretrained SAE weights; the SAE encode/decode is applied by
hand to residual activations captured from the HF model (as SAELens itself
documents for non-TransformerLens models).

Interventions:
  KV-1        replace the subject-token key/value entries at a single layer with
              the filler prompt's, for every layer.
  KV-range    same, across the first half / second half / all layers.
  Resid-1     replace the subject-token residual stream (input to block L) with
              the filler's, for every layer.
  SAE-k       at a layer, zero the top-k latents (ranked by attribution) at the
              subject position, keep the SAE reconstruction error; k in {1,5,20}.
  SAE-swap    replace the full SAE latent vector at the subject position with the
              filler's, keep the clean error term; every layer.
  SAE-global  rank all (layer, position, latent) triples by attribution, zero the
              top N simultaneously (errors kept); N in {10,50,200}.
  Steering    on the filler prompt, add the decoder directions of the clean
              prompt's top-20 attributed latents at their clean activations at a
              layer; compare with writing the clean KV into the filler prompt at
              one layer and all layers.

Every arm has an exact no-op control and, for the SAE arms, a random-feature
control. Metrics: fraction of the whole-path (KV-all) effect, top-1 flip rate,
and 95% bootstrap intervals over items.

Key/value replacement is implemented by capturing the filler prompt's
post-rotary key/value at the subject position (via a DynamicCache subclass whose
update() records them), then patching those entries into the clean prompt's
cache before the attention read at the target layers. Attention math
(softcapping, sliding window, GQA) is left entirely to the model. A no-op
control (patch installed, nothing changed) must reproduce the clean logits
exactly in fp32.
"""
from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import os
import platform
import subprocess
import sys
import time
from typing import Any, Callable

# Keep model I/O deterministic and offline-friendly; can be overridden by the
# environment before launch.
os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

import numpy as np
import torch


# --------------------------------------------------------------------------- #
# Model registry
# --------------------------------------------------------------------------- #
# `sae` is None for models that only run the KV/residual arms.
MODELS: dict[str, dict[str, Any]] = {
    "gpt2": {
        "hf_id": "openai-community/gpt2",
        "layers_path": ("transformer", "h"),
        "final_norm": ("transformer", "ln_f"),
        "sae": {
            "release": "gpt2-small-res-jb",
            "sae_id": "blocks.{L}.hook_resid_pre",
            "hook": "pre",  # residual *input* to block L
        },
    },
    "gemma2": {
        "hf_id": "unsloth/gemma-2-2b",
        "layers_path": ("model", "layers"),
        "final_norm": ("model", "norm"),
        "sae": {
            "release": "gemma-scope-2b-pt-res-canonical",
            "sae_id": "layer_{L}/width_16k/canonical",
            "hook": "post",  # residual *output* of block L
        },
    },
    "smollm2": {"hf_id": "HuggingFaceTB/SmolLM2-1.7B", "layers_path": ("model", "layers"),
                "final_norm": ("model", "norm"), "sae": None},
    "qwen05": {"hf_id": "Qwen/Qwen2.5-0.5B", "layers_path": ("model", "layers"),
               "final_norm": ("model", "norm"), "sae": None},
    "qwen15": {"hf_id": "Qwen/Qwen2.5-1.5B", "layers_path": ("model", "layers"),
               "final_norm": ("model", "norm"), "sae": None},
}


# --------------------------------------------------------------------------- #
# Deterministic prompt / subject generation
# --------------------------------------------------------------------------- #
IDENTITY_SUBJECTS = [
    "fox", "cat", "dog", "wolf", "bear", "lion", "tiger",
    "deer", "horse", "rabbit", "mouse", "owl", "pig", "sheep",
]
IDENTITY_CONTEXTS = [
    ("sitting", "a forest"),
    ("standing", "a snowy field"),
    ("resting", "a grassy meadow"),
]
IDENTITY_TEMPLATE = ("A photorealistic {subject} {pose} in {scene}. "
                     "The animal in this picture is a")
IDENTITY_FILLER = "creature"

COLOR_SUBJECTS = [
    "red", "blue", "green", "black", "white",
    "brown", "pink", "orange", "purple", "yellow",
]
COLOR_CONTEXTS = [
    ("car", "a table"),
    ("ball", "a shelf"),
    ("cup", "a desk"),
]
COLOR_TEMPLATE = ("A {color} {object} on a {surface}. "
                  "The color of the {object} is")
COLOR_FILLER = "plain"


def build_items(smoke: bool) -> dict[str, dict]:
    """Return the two behaviors, each with its candidate list, contexts and items.

    An 'item' is (behavior, context_index, subject). Prompts are materialized
    later once a tokenizer is known.
    """
    behaviors: dict[str, dict] = {}

    id_subjects = IDENTITY_SUBJECTS[:3] if smoke else IDENTITY_SUBJECTS
    id_contexts = IDENTITY_CONTEXTS[:1] if smoke else IDENTITY_CONTEXTS
    behaviors["identity"] = {
        "template": IDENTITY_TEMPLATE,
        "filler_word": IDENTITY_FILLER,
        "subjects": id_subjects,
        "candidates": id_subjects,     # candidate set == full subject list
        "contexts": [{"pose": p, "scene": s} for (p, s) in id_contexts],
        "slot": "subject",
    }

    c_subjects = COLOR_SUBJECTS[:3] if smoke else COLOR_SUBJECTS
    c_contexts = COLOR_CONTEXTS[:1] if smoke else COLOR_CONTEXTS
    behaviors["color"] = {
        "template": COLOR_TEMPLATE,
        "filler_word": COLOR_FILLER,
        "subjects": c_subjects,
        "candidates": c_subjects,
        "contexts": [{"object": o, "surface": s} for (o, s) in c_contexts],
        "slot": "color",
    }
    return behaviors


def render_prompt(behavior: dict, context: dict, subject: str) -> str:
    fmt = dict(context)
    fmt[behavior["slot"]] = subject
    return behavior["template"].format(**fmt)


# --------------------------------------------------------------------------- #
# Model utilities
# --------------------------------------------------------------------------- #
def get_layers(model, cfg) -> list:
    obj = model
    for attr in cfg["layers_path"]:
        obj = getattr(obj, attr)
    return list(obj)


def load_model_and_tokenizer(model_key: str, model_path: str, device: str, dtype):
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tok = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(
        model_path, dtype=dtype, attn_implementation="eager"
    )
    model.to(device)
    model.eval()
    model.requires_grad_(False)  # we only ever need gradients w.r.t. SAE latents
    return model, tok


# --------------------------------------------------------------------------- #
# Cache subclass that captures / patches subject-position key/value entries.
# --------------------------------------------------------------------------- #
def make_patch_cache_class():
    from transformers.cache_utils import DynamicCache

    class PatchCache(DynamicCache):
        # set via attributes after construction
        _capture: dict | None = None      # layer_idx -> (k_subj, v_subj)
        _patch: dict | None = None        # layer_idx -> (subj_pos, k_col, v_col)

        def update(self, key_states, value_states, layer_idx, *args, **kwargs):
            keys, values = super().update(key_states, value_states, layer_idx, *args, **kwargs)
            cap = getattr(self, "_capture", None)
            if cap is not None:
                cap[layer_idx] = (keys.detach().clone(), values.detach().clone())
            patch = getattr(self, "_patch", None)
            if patch is not None and layer_idx in patch:
                subj_pos, k_col, v_col = patch[layer_idx]
                keys = keys.clone()
                values = values.clone()
                keys[:, :, subj_pos, :] = k_col.to(keys.dtype)
                values[:, :, subj_pos, :] = v_col.to(values.dtype)
            return keys, values

    return PatchCache


# --------------------------------------------------------------------------- #
# Forward helpers
# --------------------------------------------------------------------------- #
class HookHandles:
    def __init__(self):
        self.handles = []

    def add(self, h):
        self.handles.append(h)

    def remove(self):
        for h in self.handles:
            h.remove()
        self.handles = []


def logits_from(model, input_ids, cache=None):
    kw = {}
    if cache is not None:
        kw = {"use_cache": True, "past_key_values": cache}
    out = model(input_ids=input_ids, **kw)
    return out.logits


def pre_hook_replace(subj_positions, new_value):
    """forward_pre_hook: replace hidden_states[:, pos, :] with new_value.

    new_value broadcasts over the batch (shape [1 or B, d] or [1 or B, len(pos), d]).
    subj_positions: int or 1-D index tensor.
    """
    def hook(module, args, kwargs):
        hs = args[0] if args else kwargs["hidden_states"]
        hs = hs.clone()
        hs[:, subj_positions, :] = new_value.to(hs.dtype)
        if args:
            return (hs,) + args[1:], kwargs
        kwargs = dict(kwargs)
        kwargs["hidden_states"] = hs
        return args, kwargs
    return hook


def post_hook_replace(subj_positions, new_value):
    """forward_hook: replace output[:, pos, :] (output is a bare tensor)."""
    def hook(module, args, output):
        if isinstance(output, tuple):
            hs = output[0].clone()
            hs[:, subj_positions, :] = new_value.to(hs.dtype)
            return (hs,) + output[1:]
        hs = output.clone()
        hs[:, subj_positions, :] = new_value.to(hs.dtype)
        return hs
    return hook


def pre_hook_capture(store, key):
    def hook(module, args, kwargs):
        hs = args[0] if args else kwargs["hidden_states"]
        store[key] = hs.detach()
        return None
    return hook


def post_hook_capture(store, key):
    def hook(module, args, output):
        hs = output[0] if isinstance(output, tuple) else output
        store[key] = hs.detach()
        return None
    return hook


def pre_hook_inject(subj_positions, new_value_tensor):
    """Like pre_hook_replace but keeps new_value_tensor in the autograd graph."""
    def hook(module, args, kwargs):
        hs = args[0] if args else kwargs["hidden_states"]
        hs = hs.clone()
        hs = hs.index_copy(1, subj_positions, new_value_tensor.to(hs.dtype))
        if args:
            return (hs,) + args[1:], kwargs
        kwargs = dict(kwargs)
        kwargs["hidden_states"] = hs
        return args, kwargs
    return hook


def post_hook_inject(subj_positions, new_value_tensor):
    def hook(module, args, output):
        hs = output[0] if isinstance(output, tuple) else output
        hs = hs.index_copy(1, subj_positions, new_value_tensor.to(hs.dtype))
        if isinstance(output, tuple):
            return (hs,) + output[1:]
        return hs
    return hook


# --------------------------------------------------------------------------- #
# Scoring
# --------------------------------------------------------------------------- #
def answer_logprobs(logits_last, answer_ids):
    """logits_last: [B, V]; answer_ids: [B]  -> per-row logprob of answer."""
    lp = torch.log_softmax(logits_last.float(), dim=-1)
    return lp[torch.arange(lp.shape[0]), answer_ids]


def top1_candidate(logits_last, candidate_ids):
    """Return, per row, the candidate id with the max logit."""
    cand = logits_last[:, candidate_ids]  # [B, C]
    idx = cand.argmax(dim=-1)
    return torch.tensor([candidate_ids[i] for i in idx.tolist()], device=logits_last.device)


# --------------------------------------------------------------------------- #
# Bootstrap
# --------------------------------------------------------------------------- #
def bootstrap_median_ci(values, n_boot=10000, seed=0):
    v = np.asarray(values, dtype=float)
    v = v[np.isfinite(v)]
    if len(v) == 0:
        return {"median": None, "lo": None, "hi": None, "n": 0}
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(v), size=(n_boot, len(v)))
    meds = np.median(v[idx], axis=1)
    return {"median": float(np.median(v)),
            "lo": float(np.percentile(meds, 2.5)),
            "hi": float(np.percentile(meds, 97.5)),
            "n": int(len(v))}


def bootstrap_rate_ci(flags, n_boot=10000, seed=0):
    v = np.asarray(flags, dtype=float)
    if len(v) == 0:
        return {"rate": None, "lo": None, "hi": None, "n": 0}
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(v), size=(n_boot, len(v)))
    rates = v[idx].mean(axis=1)
    return {"rate": float(v.mean()),
            "lo": float(np.percentile(rates, 2.5)),
            "hi": float(np.percentile(rates, 97.5)),
            "n": int(len(v))}


# --------------------------------------------------------------------------- #
# Per-context runner
# --------------------------------------------------------------------------- #
class ContextRunner:
    """Runs every arm for one (behavior, context): a batch of subjects sharing
    one prompt template, so all rows have identical length and subject index
    (no padding, so the no-op controls are exact in fp32)."""

    def __init__(self, model, tok, cfg, device, dtype, behavior, context,
                 candidate_ids, sae_provider, layers, log):
        self.model = model
        self.tok = tok
        self.cfg = cfg
        self.device = device
        self.dtype = dtype
        self.behavior = behavior
        self.context = context
        self.candidate_ids = candidate_ids
        self.sae_provider = sae_provider  # callable(L) -> sae or None
        self.layers = layers
        self.n_layers = len(layers)
        self.log = log
        self.PatchCache = make_patch_cache_class()

    # ---- setup: tokenize clean batch + filler, find subject position -------- #
    def prepare(self):
        beh = self.behavior
        subjects = beh["subjects"]
        prompts = [render_prompt(beh, self.context, s) for s in subjects]
        filler_prompt = render_prompt(beh, self.context, beh["filler_word"])

        enc = [self.tok.encode(p, add_special_tokens=True) for p in prompts]
        enc_filler = self.tok.encode(filler_prompt, add_special_tokens=True)

        # Determine subject position from the diff of clean vs filler.
        lengths = {len(e) for e in enc} | {len(enc_filler)}
        admit_mask = []
        subj_pos = None
        base_len = len(enc_filler)
        clean_ids = []
        answer_ids = []
        for s, e in zip(subjects, enc):
            ans_id = self.tok.encode(" " + s, add_special_tokens=False)
            ok = (len(e) == base_len) and (len(ans_id) == 1)
            diff_positions = [i for i in range(min(len(e), base_len)) if e[i] != enc_filler[i]]
            if len(e) == base_len and len(diff_positions) == 1:
                if subj_pos is None:
                    subj_pos = diff_positions[0]
                ok = ok and (diff_positions[0] == subj_pos)
            else:
                ok = False
            admit_mask.append(ok)
            clean_ids.append(e)
            answer_ids.append(ans_id[0] if len(ans_id) == 1 else -1)

        if subj_pos is None:
            # nothing usable in this context
            self.usable = False
            return
        self.usable = True
        # rows where tokenization is consistent
        self.tok_ok = admit_mask
        # Build the clean batch from only tok-ok rows (others cannot be scored).
        keep = [i for i, ok in enumerate(admit_mask) if ok]
        self.keep = keep
        self.subjects = [subjects[i] for i in keep]
        self.subj_pos = subj_pos
        self.answer_ids = torch.tensor([answer_ids[i] for i in keep], device=self.device)
        self.clean_input = torch.tensor([clean_ids[i] for i in keep], device=self.device)
        self.filler_input = torch.tensor([enc_filler], device=self.device)
        self.seq_len = self.clean_input.shape[1]
        self.filler_prompt = filler_prompt
        self.prompts = [prompts[i] for i in keep]

    # ---- capture clean + filler activations --------------------------------- #
    @torch.no_grad()
    def _capture_one(self, input_ids):
        """Plain (no-cache) forward with residual hooks + a capturing-cache
        forward. Returns (logits_last, resid_store, kv_store, logits_cache_last)."""
        layers = self.layers
        store = {}
        hh = HookHandles()
        for L, layer in enumerate(layers):
            hh.add(layer.register_forward_pre_hook(pre_hook_capture(store, ("pre", L)), with_kwargs=True))
            hh.add(layer.register_forward_hook(post_hook_capture(store, ("post", L))))
        logits = logits_from(self.model, input_ids)          # canonical (no cache)
        hh.remove()
        cache = self.PatchCache()
        cache._capture = {}
        logits_c = logits_from(self.model, input_ids, cache=cache)  # capturing cache
        return logits[:, -1, :].detach(), store, cache._capture, logits_c[:, -1, :].detach()

    @torch.no_grad()
    def capture(self):
        cl_last, clean_store, clean_kv, cl_cache = self._capture_one(self.clean_input)
        fl_last, filler_store, filler_kv, fl_cache = self._capture_one(self.filler_input)
        self.clean_resid = clean_store
        self.filler_resid = filler_store
        self.clean_kv = clean_kv
        self.filler_kv = filler_kv
        self.clean_logits_last = cl_last
        self.filler_logits_last = fl_last
        # cache-path parity gate (expect ~0 in fp32)
        self.cache_parity = float((cl_cache - cl_last).abs().max().item())

        self.clean_lp = answer_logprobs(self.clean_logits_last, self.answer_ids)
        self.filler_lp = answer_logprobs(self.filler_logits_last, self.answer_ids)
        self.clean_top1 = top1_candidate(self.clean_logits_last, self.candidate_ids)

    # ---- admission ---------------------------------------------------------- #
    def admission(self):
        # top-1 among candidates == answer, and filler lp <= clean lp - 1.0
        admitted = []
        for i in range(len(self.subjects)):
            top1 = int(self.clean_top1[i].item()) == int(self.answer_ids[i].item())
            drop = (self.clean_lp[i].item() - self.filler_lp[i].item()) >= 1.0
            admitted.append(bool(top1 and drop))
        self.admitted = admitted
        return admitted

    # ---- delta logprob given a modified last-position logits ---------------- #
    def _delta(self, logits_last):
        lp = answer_logprobs(logits_last, self.answer_ids)
        dlp = (lp - self.clean_lp).detach().cpu().numpy()
        top1 = top1_candidate(logits_last, self.candidate_ids)
        flip = (top1 != self.clean_top1).detach().cpu().numpy().astype(float)
        return dlp, flip

    def _delta_vs(self, logits_last, base_lp, base_top1):
        """Delta vs an explicit baseline (used for the isolated KV arms, whose
        baseline is the prefix/suffix-split clean forward)."""
        lp = answer_logprobs(logits_last, self.answer_ids)
        dlp = (lp - base_lp).detach().cpu().numpy()
        top1 = top1_candidate(logits_last, self.candidate_ids)
        flip = (top1 != base_top1).detach().cpu().numpy().astype(float)
        return dlp, flip

    # ---- KV arms ------------------------------------------------------------ #
    @torch.no_grad()
    def kv_swap(self, layer_indices):
        """Replace subject KV with the filler's at the given layers."""
        cache = self.PatchCache()
        patch = {}
        for L in layer_indices:
            fk, fv = self.filler_kv[L]  # [1,H,S,D]
            patch[L] = (self.subj_pos, fk[:, :, self.subj_pos, :], fv[:, :, self.subj_pos, :])
        cache._patch = patch
        logits = logits_from(self.model, self.clean_input, cache=cache)
        return self._delta(logits[:, -1, :])

    @torch.no_grad()
    def kv_noop(self):
        """Patch installed, subject KV replaced with the *clean* subject KV."""
        cache = self.PatchCache()
        patch = {}
        for L in range(self.n_layers):
            ck, cv = self.clean_kv[L]
            patch[L] = (self.subj_pos, ck[:, :, self.subj_pos, :], cv[:, :, self.subj_pos, :])
        cache._patch = patch
        logits = logits_from(self.model, self.clean_input, cache=cache)
        return logits[:, -1, :].detach()

    # ---- KV isolated arms (prefix/suffix split; subject stream intact) ------ #
    @torch.no_grad()
    def _kv_isolated_logits(self, layer_indices):
        """Run the prefix (through the subject token) cleanly into a cache, then
        (optionally) overwrite the subject KV at `layer_indices` with the filler's,
        then run only the suffix and return the last-position logits. With
        layer_indices=None nothing is overwritten (the split no-op baseline)."""
        subj, S = self.subj_pos, self.seq_len
        B = self.clean_input.shape[0]
        prefix_ids = self.clean_input[:, : subj + 1]
        suffix_ids = self.clean_input[:, subj + 1:]
        cache = self.PatchCache()  # plain: _patch is None
        self.model(input_ids=prefix_ids, use_cache=True, past_key_values=cache)
        if layer_indices is not None:
            for L in layer_indices:
                fk, fv = self.filler_kv[L]
                lk = cache.layers[L].keys
                lv = cache.layers[L].values
                lk[:, :, subj, :] = fk[:, :, subj, :].to(lk.dtype)
                lv[:, :, subj, :] = fv[:, :, subj, :].to(lv.dtype)
        if suffix_ids.shape[1] == 0:
            # subject is the last token: no suffix, read prefix's last position
            out = self.model(input_ids=self.clean_input[:, : subj + 1], use_cache=False)
            return out.logits[:, -1, :].detach()
        cache_position = torch.arange(subj + 1, S, device=self.device)
        position_ids = cache_position.unsqueeze(0).expand(B, -1)
        out = self.model(input_ids=suffix_ids, use_cache=True, past_key_values=cache,
                         cache_position=cache_position, position_ids=position_ids)
        return out.logits[:, -1, :].detach()

    @torch.no_grad()
    def kv_isolated_baseline(self):
        """Split no-op baseline: prefix/suffix split with no overwrite."""
        self._split_logits = self._kv_isolated_logits(None)
        self._split_lp = answer_logprobs(self._split_logits, self.answer_ids)
        self._split_top1 = top1_candidate(self._split_logits, self.candidate_ids)
        self.split_noop_max = float((self._split_logits - self.clean_logits_last).abs().max().item())
        return self.split_noop_max

    @torch.no_grad()
    def kv_swap_isolated(self, layer_indices):
        logits = self._kv_isolated_logits(list(layer_indices))
        return self._delta_vs(logits, self._split_lp, self._split_top1)

    # ---- residual arms ------------------------------------------------------ #
    @torch.no_grad()
    def resid_swap(self, L):
        """Replace subject residual (input to block L) with filler's."""
        filler_col = self.filler_resid[("pre", L)][:, self.subj_pos, :]  # [1,d]
        hh = HookHandles()
        hh.add(self.layers[L].register_forward_pre_hook(
            pre_hook_replace(self.subj_pos, filler_col), with_kwargs=True))
        logits = logits_from(self.model, self.clean_input)
        hh.remove()
        return self._delta(logits[:, -1, :])

    @torch.no_grad()
    def resid_noop(self, L):
        clean_col = self.clean_resid[("pre", L)][:, self.subj_pos, :]
        hh = HookHandles()
        hh.add(self.layers[L].register_forward_pre_hook(
            pre_hook_replace(self.subj_pos, clean_col), with_kwargs=True))
        logits = logits_from(self.model, self.clean_input)
        hh.remove()
        return logits[:, -1, :].detach()

    # ---- SAE helpers -------------------------------------------------------- #
    def _sae_hook_key(self):
        return self.cfg["sae"]["hook"]  # "pre" or "post"

    def _install_resid_patch(self, L, positions, new_value_tensor, grad=False):
        """Return a HookHandles patching the residual at the SAE hook point of L."""
        hh = HookHandles()
        is_post = self._sae_hook_key() == "post"
        if grad:
            hook = post_hook_inject(positions, new_value_tensor) if is_post else pre_hook_inject(positions, new_value_tensor)
        else:
            hook = post_hook_replace(positions, new_value_tensor) if is_post else pre_hook_replace(positions, new_value_tensor)
        if is_post:
            hh.add(self.layers[L].register_forward_hook(hook))
        else:
            hh.add(self.layers[L].register_forward_pre_hook(hook, with_kwargs=True))
        return hh

    def _resid_at(self, store, L):
        key = ("post", L) if self._sae_hook_key() == "post" else ("pre", L)
        return store[key]

    def attribution(self, sae, L):
        """Return attribution [B,S,d_sae] = f * d(sum answer logprob)/d f, at layer L.

        The residual at the SAE hook point (all positions) is expressed as
        decode(f)+error with f a differentiable leaf; the reconstruction is
        numerically identical to the clean residual, so the forward is clean and
        the gradient is exact first-order attribution. Rows are processed in
        chunks so the backward graph (which retains activations for layers >= L)
        stays within VRAM regardless of the batch size."""
        pos = torch.arange(self.seq_len, device=self.device)
        resid_full = self._resid_at(self.clean_resid, L).to(torch.float32)  # [B,S,d]
        B = self.clean_input.shape[0]
        attrs, fs, errs = [], [], []
        chunk = getattr(self, "attr_chunk", 6)
        for c0 in range(0, B, chunk):
            c1 = min(B, c0 + chunk)
            ids = self.clean_input[c0:c1]
            resid = resid_full[c0:c1]
            f = sae.encode(resid).detach().float().requires_grad_(True)
            recon = sae.decode(f)
            err = (resid - sae.decode(sae.encode(resid))).detach()
            new_val = recon + err  # grad flows through f
            hh = self._install_resid_patch(L, pos, new_val.to(self.dtype), grad=True)
            logits = logits_from(self.model, ids)
            hh.remove()
            lp = answer_logprobs(logits[:, -1, :], self.answer_ids[c0:c1])
            grad = torch.autograd.grad(lp.sum(), f)[0]
            attrs.append((f.detach() * grad.detach()))
            fs.append(f.detach())
            errs.append(err.detach())
        return torch.cat(attrs, 0), torch.cat(fs, 0), torch.cat(errs, 0)

    @torch.no_grad()
    def sae_ablate_single(self, sae, L, f_clean, ranking, k, positions=None):
        """Zero the top-k latents (by ranking) at the subject position and score.

        Implemented as removing the clean feature contributions from the residual
        (decode is affine, so this equals zeroing the latents and keeping the
        reconstruction error)."""
        subj = self.subj_pos
        resid = self._resid_at(self.clean_resid, L).to(torch.float32)
        f_subj = f_clean[:, subj, :]                       # [B,d_sae]
        rank_subj = ranking[:, subj, :]                    # [B,d_sae]
        B, dsae = f_subj.shape
        # per-row top-k indices among latents with positive activation
        contribs = torch.zeros(B, resid.shape[-1], device=self.device, dtype=torch.float32)
        Wdec = sae.W_dec.to(torch.float32)                 # [d_sae, d]
        for b in range(B):
            active = (f_subj[b] > 0)
            scores = rank_subj[b].clone()
            scores[~active] = float("-inf")
            kk = min(k, int(active.sum().item()))
            if kk <= 0:
                continue
            top = torch.topk(scores, kk).indices
            contribs[b] = (f_subj[b, top].unsqueeze(-1) * Wdec[top]).sum(0)
        new_subj = (resid[:, subj, :] - contribs)          # [B,d]
        hh = self._install_resid_patch(L, subj, new_subj.to(self.dtype))
        logits = logits_from(self.model, self.clean_input)
        hh.remove()
        return self._delta(logits[:, -1, :])

    @torch.no_grad()
    def sae_topk_sel(self, f_clean, ranking, k):
        """Per-item list of the top-k active latent ids at the subject position
        (the exact selection sae_ablate_single uses); for the TL cross-check."""
        subj = self.subj_pos
        f_subj = f_clean[:, subj, :]
        rank_subj = ranking[:, subj, :]
        B = f_subj.shape[0]
        sel = []
        for b in range(B):
            active = (f_subj[b] > 0)
            scores = rank_subj[b].clone()
            scores[~active] = float("-inf")
            kk = min(k, int(active.sum().item()))
            sel.append(torch.topk(scores, kk).indices.tolist() if kk > 0 else [])
        return sel

    @torch.no_grad()
    def sae_ablate_random(self, sae, L, f_clean, k, seed):
        subj = self.subj_pos
        resid = self._resid_at(self.clean_resid, L).to(torch.float32)
        f_subj = f_clean[:, subj, :]
        B = f_subj.shape[0]
        g = torch.Generator(device="cpu").manual_seed(seed + L)
        contribs = torch.zeros(B, resid.shape[-1], device=self.device, dtype=torch.float32)
        Wdec = sae.W_dec.to(torch.float32)
        for b in range(B):
            active = torch.nonzero(f_subj[b] > 0).flatten()
            if active.numel() == 0:
                continue
            kk = min(k, active.numel())
            perm = torch.randperm(active.numel(), generator=g)[:kk]
            sel = active[perm]
            contribs[b] = (f_subj[b, sel].unsqueeze(-1) * Wdec[sel]).sum(0)
        new_subj = resid[:, subj, :] - contribs
        hh = self._install_resid_patch(L, subj, new_subj.to(self.dtype))
        logits = logits_from(self.model, self.clean_input)
        hh.remove()
        return self._delta(logits[:, -1, :])

    @torch.no_grad()
    def sae_swap(self, sae, L):
        """Replace the full subject latent vector with the filler's, keep clean err."""
        subj = self.subj_pos
        clean_resid = self._resid_at(self.clean_resid, L).to(torch.float32)
        filler_resid = self._resid_at(self.filler_resid, L).to(torch.float32)  # [1,S,d]
        f_filler = sae.encode(filler_resid)[:, subj, :]     # [1,d_sae]
        recon_filler = sae.decode(f_filler)                 # [1,d]
        cs = clean_resid[:, subj, :]                        # [B,d]
        err_clean = cs - sae.decode(sae.encode(cs.unsqueeze(1)))[:, 0, :]  # [B,d]
        new_subj = recon_filler + err_clean                 # broadcast [B,d]
        hh = self._install_resid_patch(L, subj, new_subj.to(self.dtype))
        logits = logits_from(self.model, self.clean_input)
        hh.remove()
        return self._delta(logits[:, -1, :])

    @torch.no_grad()
    def sae_noop(self, sae, L):
        """Exact no-op: remove *zero* feature contributions at the subject
        position (this is SAE-k with k=0, i.e. keep all features + error). The
        residual is replaced with itself, so logits must match clean exactly."""
        subj = self.subj_pos
        resid = self._resid_at(self.clean_resid, L).to(torch.float32)
        new_subj = resid[:, subj, :]  # identity
        hh = self._install_resid_patch(L, subj, new_subj.to(self.dtype))
        logits = logits_from(self.model, self.clean_input)
        hh.remove()
        return logits[:, -1, :].detach()

    @torch.no_grad()
    def sae_recon_error(self, sae, L):
        """Diagnostic: max abs deviation of decode(encode(resid))+error from resid
        at the subject position (SAE reconstruction faithfulness; not gated)."""
        subj = self.subj_pos
        resid = self._resid_at(self.clean_resid, L).to(torch.float32)[:, subj, :]
        rec = sae.decode(sae.encode(resid.unsqueeze(1)))[:, 0, :]
        err = resid - rec
        approx = rec + err
        return float((approx - resid).abs().max().item())

    # ---- SAE global (propagating ablation; one item at a time) -------------- #
    def _prop_hook(self, posmap, sae_cpu):
        """Hook that ablates selected features at selected positions from the
        CURRENT residual (so upstream ablations propagate). `posmap` maps
        position -> list of latent ids. Encoding is done on CPU so no full SAE
        needs to sit on the GPU; only the affected positions are encoded."""
        positions = sorted(posmap.keys())
        is_post = self._sae_hook_key() == "post"
        Wdec = sae_cpu.W_dec  # [d_sae, d] (cpu, fp32)

        def apply(hs):
            hs = hs.clone()
            rows = hs[0, positions, :].to("cpu", torch.float32)      # [n_pos, d]
            f = sae_cpu.encode(rows)                                 # [n_pos, d_sae]
            for i, pos in enumerate(positions):
                lats = torch.tensor(posmap[pos], dtype=torch.long)
                delta = (f[i, lats].unsqueeze(-1) * Wdec[lats]).sum(0)  # [d]
                hs[0, pos, :] = hs[0, pos, :] - delta.to(hs.device, hs.dtype)
            return hs

        if is_post:
            def hook(module, args, output):
                hs = output[0] if isinstance(output, tuple) else output
                hs2 = apply(hs)
                return (hs2,) + output[1:] if isinstance(output, tuple) else hs2
        else:
            def hook(module, args, kwargs):
                hs = args[0] if args else kwargs["hidden_states"]
                hs2 = apply(hs)
                if args:
                    return (hs2,) + args[1:], kwargs
                kwargs = dict(kwargs); kwargs["hidden_states"] = hs2
                return args, kwargs
        return hook

    @torch.no_grad()
    def sae_global_prop_item(self, saes_cpu, selected_b, b):
        by_layer = {}
        for (L, pos, lat) in selected_b:
            by_layer.setdefault(L, {}).setdefault(pos, []).append(lat)
        ids = self.clean_input[b:b + 1]
        hh = HookHandles()
        is_post = self._sae_hook_key() == "post"
        for L, posmap in by_layer.items():
            hook = self._prop_hook(posmap, saes_cpu[L])
            if is_post:
                hh.add(self.layers[L].register_forward_hook(hook))
            else:
                hh.add(self.layers[L].register_forward_pre_hook(hook, with_kwargs=True))
        logits = logits_from(self.model, ids)
        hh.remove()
        return logits[:, -1, :].detach()  # [1, V]

    @torch.no_grad()
    def sae_global_context(self, saes_cpu, selected_all):
        """Run the propagating global ablation for every item; return dlp/flip
        arrays aligned to the context's rows."""
        dlps, flips = [], []
        for b in range(len(self.subjects)):
            ll = self.sae_global_prop_item(saes_cpu, selected_all[b], b)
            lp = answer_logprobs(ll, self.answer_ids[b:b + 1])
            dlps.append(float((lp - self.clean_lp[b:b + 1]).item()))
            top1 = top1_candidate(ll, self.candidate_ids)
            flips.append(float((top1 != self.clean_top1[b:b + 1]).item()))
        return dlps, flips

    def global_position_diag(self, selected_all):
        """Distribution of selected (layer,pos,latent) over position class and
        layer, aggregated over items (diagnostic)."""
        subj, last = self.subj_pos, self.seq_len - 1
        pos_counts = {"subject": 0, "answer_last": 0, "other": 0}
        layer_counts = {}
        total = 0
        for sel in selected_all:
            for (L, pos, lat) in sel:
                total += 1
                cls = "subject" if pos == subj else ("answer_last" if pos == last else "other")
                pos_counts[cls] += 1
                layer_counts[L] = layer_counts.get(L, 0) + 1
        return {"total_selected": total, "by_position_class": pos_counts,
                "by_layer": layer_counts, "n_items": len(selected_all)}

    # ---- steering / KV sufficiency (on the filler prompt) ------------------- #
    @torch.no_grad()
    def steer_filler(self, sae, L, attr_L, f_clean_L):
        """On the filler prompt, add the decoder directions of the clean prompt's
        top-20 attributed latents at their clean activations, at the subject
        position of layer L. One steered row per subject."""
        subj = self.subj_pos
        B = len(self.subjects)
        Wdec = sae.W_dec.to(torch.float32)
        attr_subj = attr_L[:, subj, :]
        f_subj = f_clean_L[:, subj, :]
        steer = torch.zeros(B, Wdec.shape[1], device=self.device, dtype=torch.float32)
        for b in range(B):
            top = torch.topk(attr_subj[b], min(20, attr_subj.shape[1])).indices
            steer[b] = (f_subj[b, top].unsqueeze(-1) * Wdec[top]).sum(0)
        filler_batch = self.filler_input.repeat(B, 1)
        filler_resid = self._resid_at(self.filler_resid, L).to(torch.float32)[:, subj, :]  # [1,d]
        new_subj = filler_resid + steer  # [B,d]
        hh = self._install_resid_patch(L, subj, new_subj.to(self.dtype))
        logits = logits_from(self.model, filler_batch)
        hh.remove()
        lp = answer_logprobs(logits[:, -1, :], self.answer_ids)
        gain = (lp - self.filler_lp).detach().cpu().numpy()
        return gain

    @torch.no_grad()
    def kv_write_into_filler(self, layer_indices):
        """Write each subject's clean KV into the filler prompt at the given
        layers; score the gain in that subject's answer logprob."""
        B = len(self.subjects)
        filler_batch = self.filler_input.repeat(B, 1)
        cache = self.PatchCache()
        patch = {}
        for L in layer_indices:
            ck, cv = self.clean_kv[L]  # [B,H,S,D]
            patch[L] = (self.subj_pos, ck[:, :, self.subj_pos, :], cv[:, :, self.subj_pos, :])
        cache._patch = patch
        logits = logits_from(self.model, filler_batch, cache=cache)
        lp = answer_logprobs(logits[:, -1, :], self.answer_ids)
        gain = (lp - self.filler_lp).detach().cpu().numpy()
        return gain


# --------------------------------------------------------------------------- #
# SAE loading
# --------------------------------------------------------------------------- #
def load_sae(release, sae_id, device):
    from sae_lens import SAE
    out = SAE.from_pretrained(release, sae_id, device="cpu")
    sae = out[0] if isinstance(out, tuple) else out
    sae = sae.to(device)
    sae = sae.to(torch.float32)
    sae.eval()
    for p in sae.parameters():
        p.requires_grad_(False)
    return sae


# --------------------------------------------------------------------------- #
# Per-behavior orchestration
# --------------------------------------------------------------------------- #
def run_behavior(model, tok, cfg, device, dtype, behavior, candidate_ids,
                 sae_cfg, layers, log, seed=0):
    K_LIST = [1, 5, 20]
    N_LIST = [10, 50, 200]

    runners = []
    for ci, ctx in enumerate(behavior["contexts"]):
        cr = ContextRunner(model, tok, cfg, device, dtype, behavior, ctx,
                           candidate_ids, None, layers, log)
        cr.prepare()
        if not getattr(cr, "usable", False):
            log(f"  context {ci}: not usable (tokenization), skipped")
            continue
        cr.capture()
        cr.admission()
        cr.context_idx = ci
        runners.append(cr)
        log(f"  context {ci}: kept {len(cr.subjects)} rows, admitted "
            f"{sum(cr.admitted)}, subj_pos {cr.subj_pos}, seq_len {cr.seq_len}, "
            f"cache_parity {cr.cache_parity:.2e}")

    # ----- item table -----
    items = []
    whole_path_dlp = []
    for cr in runners:
        for i, s in enumerate(cr.subjects):
            items.append({
                "context_idx": cr.context_idx, "subject": s,
                "prompt": cr.prompts[i], "filler_prompt": cr.filler_prompt,
                "subj_pos": cr.subj_pos,
                "admitted": bool(cr.admitted[i]),
                "clean_lp": float(cr.clean_lp[i].item()),
                "filler_lp": float(cr.filler_lp[i].item()),
            })

    arms: dict[str, Any] = {}
    gates: dict[str, Any] = {"cache_parity": [cr.cache_parity for cr in runners]}
    n_layers = len(layers)

    def extend(dst_key, sub, dlp, flip):
        d = arms.setdefault(dst_key, {}).setdefault(sub, {"dlp": [], "flip": []})
        d["dlp"].extend([float(x) for x in dlp])
        d["flip"].extend([float(x) for x in flip])

    # ----- whole-path (KV all) first, per runner, in item order -----
    for cr in runners:
        dlp, flip = cr.kv_swap(list(range(n_layers)))
        whole_path_dlp.extend([float(x) for x in dlp])
        extend("kv_range", "all", dlp, flip)

    # ----- KV-1 (every layer) -----
    for L in range(n_layers):
        for cr in runners:
            dlp, flip = cr.kv_swap([L])
            extend("kv1", f"L{L}", dlp, flip)

    # ----- KV-range first/second half -----
    half = n_layers // 2
    first = list(range(0, half))
    second = list(range(half, n_layers))
    for name, idxs in [("first", first), ("second", second)]:
        for cr in runners:
            dlp, flip = cr.kv_swap(idxs)
            extend("kv_range", name, dlp, flip)

    # ----- KV ISOLATED variants (subject stream intact; prefix/suffix split) -----
    whole_path_iso_dlp = []
    split_noop_max = 0.0
    for cr in runners:
        split_noop_max = max(split_noop_max, cr.kv_isolated_baseline())
    gates["kv_isolated_split_noop_max"] = split_noop_max
    for cr in runners:
        dlp, flip = cr.kv_swap_isolated(list(range(n_layers)))
        whole_path_iso_dlp.extend([float(x) for x in dlp])
        extend("kv_range_iso", "all", dlp, flip)
    for L in range(n_layers):
        for cr in runners:
            dlp, flip = cr.kv_swap_isolated([L])
            extend("kv1_iso", f"L{L}", dlp, flip)
    for name, idxs in [("first", first), ("second", second)]:
        for cr in runners:
            dlp, flip = cr.kv_swap_isolated(idxs)
            extend("kv_range_iso", name, dlp, flip)

    # ----- Resid-1 (every layer) -----
    for L in range(n_layers):
        for cr in runners:
            dlp, flip = cr.resid_swap(L)
            extend("resid1", f"L{L}", dlp, flip)

    # ----- no-op gates -----
    kv_noop_max = 0.0
    resid_noop_max = {}
    for cr in runners:
        kv_noop_max = max(kv_noop_max,
                          float((cr.kv_noop() - cr.clean_logits_last).abs().max().item()))
    gate_layers = sorted(set([0, n_layers // 2, n_layers - 1]))
    for L in gate_layers:
        m = 0.0
        for cr in runners:
            m = max(m, float((cr.resid_noop(L) - cr.clean_logits_last).abs().max().item()))
        resid_noop_max[f"L{L}"] = m
    gates["kv_noop_max"] = kv_noop_max
    gates["resid_noop_max"] = resid_noop_max

    # ----- SAE arms -----
    if sae_cfg is not None:
        sae_layers = list(range(n_layers))
        per_layer_global = {}  # {ci: {L: (f_clean_cpu, None)}}  (f_clean for random-active)
        attr_cpu = {}          # {ci: {L: attr_cpu}}
        saes_cpu = {}          # {L: SAE resident on CPU, for propagating global}
        sae_sel20 = {}         # {ci: {L: [per-item top-20 latent ids]}}  for the TL cross-check
        for cr in runners:
            per_layer_global[cr.context_idx] = {}
            attr_cpu[cr.context_idx] = {}
            sae_sel20[cr.context_idx] = {}
        sae_noop_max = {}
        sae_recon_err = {}
        for L in sae_layers:
            sae = load_sae(sae_cfg["release"], sae_cfg["sae_id"].format(L=L), device)
            for cr in runners:
                attr, f_clean, err = cr.attribution(sae, L)
                ranking = attr  # rank by attribution (activation * grad)
                # SAE-k for each k
                for k in K_LIST:
                    dlp, flip = cr.sae_ablate_single(sae, L, f_clean, ranking, k)
                    d = arms.setdefault("sae_k_by_k", {}).setdefault(f"k{k}", {}).setdefault(f"L{L}", {"dlp": [], "flip": []})
                    d["dlp"].extend([float(x) for x in dlp]); d["flip"].extend([float(x) for x in flip])
                    dlp_r, flip_r = cr.sae_ablate_random(sae, L, f_clean, k, seed=seed + 1000 * k)
                    dr = arms.setdefault("sae_k_random_by_k", {}).setdefault(f"k{k}", {}).setdefault(f"L{L}", {"dlp": [], "flip": []})
                    dr["dlp"].extend([float(x) for x in dlp_r]); dr["flip"].extend([float(x) for x in flip_r])
                # SAE-swap
                dlp, flip = cr.sae_swap(sae, L)
                extend("sae_swap", f"L{L}", dlp, flip)
                # SAE no-op (exact) + recon diagnostic
                nm = float((cr.sae_noop(sae, L) - cr.clean_logits_last).abs().max().item())
                sae_noop_max[f"L{L}"] = max(sae_noop_max.get(f"L{L}", 0.0), nm)
                sae_recon_err[f"L{L}"] = max(sae_recon_err.get(f"L{L}", 0.0), cr.sae_recon_error(sae, L))
                # steering (per item gains)
                gains = cr.steer_filler(sae, L, attr, f_clean)
                sd = arms.setdefault("steering", {}).setdefault(f"L{L}", {"gain": []})
                sd["gain"].extend([float(x) for x in gains])
                # store for global (f_clean for random-active; W_dec comes from saes_cpu)
                per_layer_global[cr.context_idx][L] = (f_clean.detach().to("cpu"), None)
                attr_cpu[cr.context_idx][L] = attr.detach().to("cpu")
                sae_sel20[cr.context_idx][L] = cr.sae_topk_sel(f_clean, attr, 20)
            # keep the SAE resident on CPU for the propagating global ablation
            saes_cpu[L] = sae.to("cpu")
            if device.startswith("cuda"):
                torch.cuda.empty_cache()
        gates["sae_noop_max"] = sae_noop_max
        gates["sae_recon_err"] = sae_recon_err

        # ----- KV sufficiency into filler (single layer + all) -----
        for L in range(n_layers):
            for cr in runners:
                gains = cr.kv_write_into_filler([L])
                sd = arms.setdefault("kv_suff_single", {}).setdefault(f"L{L}", {"gain": []})
                sd["gain"].extend([float(x) for x in gains])
        for cr in runners:
            gains = cr.kv_write_into_filler(list(range(n_layers)))
            sd = arms.setdefault("kv_suff_all", {"gain": []})
            sd["gain"].extend([float(x) for x in gains])

        # ----- SAE-global: three position-scopes, each propagating with random ctrl -----
        # all      : rank all (layer, position, latent)  [preregistered; rule 3]
        # subject  : restrict to the SUBJECT position (fair SAE analog of whole-path KV)
        # nonfinal : exclude the final (answer-readout) position
        def build_selected(cr, attr_layers, N, pos_ok):
            B = len(cr.subjects)
            selected = [[] for _ in range(B)]
            cap = max(N_LIST)
            for b in range(B):
                cand = []
                for L, a in attr_layers.items():
                    ab = a[b]  # [S, dsae]
                    dsae = ab.shape[1]
                    flat = ab.reshape(-1)
                    kk = min(cap * 4, flat.numel())
                    vals, idx = torch.topk(flat, kk)
                    for v, ii in zip(vals.tolist(), idx.tolist()):
                        pos, lat = divmod(ii, dsae)
                        if pos_ok(pos):
                            cand.append((v, L, pos, lat))
                cand.sort(key=lambda t: t[0], reverse=True)
                selected[b] = [(L, pos, lat) for (_, L, pos, lat) in cand[:N]]
            return selected

        def rand_selected(cr, plg, N, pos_ok, seed_off):
            g = np.random.default_rng(seed + seed_off)
            rand_sel = [[] for _ in range(len(cr.subjects))]
            for b in range(len(cr.subjects)):
                triples = [(L, r[0], r[1]) for L, (fc, _) in plg.items()
                           for r in torch.nonzero(fc[b] > 0).tolist() if pos_ok(r[0])]
                if triples:
                    pick = g.choice(len(triples), size=min(N, len(triples)), replace=False)
                    rand_sel[b] = [triples[p] for p in pick]
            return rand_sel

        diags = {"all": {}, "subject": {}, "nonfinal": {}}

        def merge_diag(dst, gd):
            for key in ("total_selected", "n_items"):
                dst[key] = dst.get(key, 0) + gd[key]
            for k2, v2 in gd["by_position_class"].items():
                dst.setdefault("by_position_class", {})
                dst["by_position_class"][k2] = dst["by_position_class"].get(k2, 0) + v2
            for k2, v2 in gd["by_layer"].items():
                dst.setdefault("by_layer", {})
                dst["by_layer"][str(k2)] = dst["by_layer"].get(str(k2), 0) + v2

        for cr in runners:
            plg = per_layer_global[cr.context_idx]
            attrs = attr_cpu[cr.context_idx]
            last = cr.seq_len - 1
            subj = cr.subj_pos
            scopes = {
                "all": (lambda p: True, 0),
                "subject": (lambda p, s=subj: p == s, 100000),
                "nonfinal": (lambda p, lst=last: p != lst, 200000),
            }
            for scope, (pos_ok, soff) in scopes.items():
                arm = "sae_global" if scope == "all" else f"sae_global_{scope}"
                armr = "sae_global_random" if scope == "all" else f"sae_global_{scope}_random"
                for N in N_LIST:
                    sel = build_selected(cr, attrs, N, pos_ok)
                    dlp, flip = cr.sae_global_context(saes_cpu, sel)
                    extend(arm, f"N{N}", dlp, flip)
                    if N == max(N_LIST):
                        merge_diag(diags[scope], cr.global_position_diag(sel))
                    rsel = rand_selected(cr, plg, N, pos_ok, soff + N)
                    dlp_r, flip_r = cr.sae_global_context(saes_cpu, rsel)
                    extend(armr, f"N{N}", dlp_r, flip_r)
        gates["sae_global_diag_N200"] = diags["all"]
        gates["sae_global_subject_diag_N200"] = diags["subject"]
        gates["sae_global_nonfinal_diag_N200"] = diags["nonfinal"]

    # context data for the TransformerLens cross-check (token ids/positions kept
    # in item order so TL Δlp aligns with the HF arm arrays)
    context_data = []
    for cr in runners:
        context_data.append({
            "context_idx": cr.context_idx,
            "clean_ids": cr.clean_input.tolist(),
            "filler_ids": cr.filler_input.tolist(),
            "subj_pos": cr.subj_pos, "seq_len": cr.seq_len,
            "answer_ids": [int(x) for x in cr.answer_ids.tolist()],
            "admitted": [bool(a) for a in cr.admitted],
            "subjects": list(cr.subjects),
            "clean_lp_hf": [float(x) for x in cr.clean_lp.tolist()],
            "clean_top1_hf": [int(x) for x in cr.clean_top1.tolist()],
        })
    out = {
        "candidates": [int(c) for c in candidate_ids],
        "items": items,
        "whole_path_dlp": whole_path_dlp,
        "whole_path_iso_dlp": whole_path_iso_dlp,
        "arms": arms,
        "gates": gates,
        "context_data": context_data,
    }
    if sae_cfg is not None:
        out["sae_selected_k20"] = {str(ci): {str(L): sel for L, sel in d.items()}
                                   for ci, d in sae_sel20.items()}
    return out


# --------------------------------------------------------------------------- #
# Aggregation
# --------------------------------------------------------------------------- #
def _fractions(dlp, wp, admitted, eps=1e-6):
    out = []
    for d, w, a in zip(dlp, wp, admitted):
        if not a:
            continue
        if abs(w) < eps:
            continue
        out.append(d / w)
    return out


def _flips(flip, admitted):
    return [f for f, a in zip(flip, admitted) if a]


def _norm_gain(gain, clean_lp, filler_lp, admitted, eps=1e-6):
    out = []
    for g, c, f, a in zip(gain, clean_lp, filler_lp, admitted):
        gap = c - f
        if not a or abs(gap) < eps:
            continue
        out.append(g / gap)
    return out


def aggregate_behavior(raw, n_layers, has_sae):
    items = raw["items"]
    admitted = [it["admitted"] for it in items]
    clean_lp = [it["clean_lp"] for it in items]
    filler_lp = [it["filler_lp"] for it in items]
    wp = raw["whole_path_dlp"]
    wp_iso = raw.get("whole_path_iso_dlp", wp)
    arms = raw["arms"]
    n_adm = int(sum(admitted))

    summ: dict[str, Any] = {"n_items": len(items), "n_admitted": n_adm,
                            "usable_for_rules": n_adm >= 12}

    def per_layer_stats(arm_dict, wpv=None):
        wpv = wp if wpv is None else wpv
        res = {}
        for Lkey, d in arm_dict.items():
            fr = _fractions(d["dlp"], wpv, admitted)
            fl = _flips(d["flip"], admitted)
            res[Lkey] = {"fraction": bootstrap_median_ci(fr),
                         "flip": bootstrap_rate_ci(fl),
                         "median_dlp": float(np.median([x for x, a in zip(d["dlp"], admitted) if a])) if n_adm else None}
        return res

    def best_layer(stats):
        best, bestval = None, -1e18
        for Lkey, s in stats.items():
            m = s["fraction"]["median"]
            if m is not None and m > bestval:
                bestval, best = m, Lkey
        return best, (stats[best] if best else None)

    # KV-1
    kv1 = per_layer_stats(arms["kv1"])
    kv1_best, kv1_beststat = best_layer(kv1)
    summ["kv1"] = {"per_layer": kv1, "best_layer": kv1_best, "best": kv1_beststat}

    # KV-range
    def kv_range_stats(key, wpv):
        kvr = {}
        for name in ("first", "second", "all"):
            if name in arms.get(key, {}):
                d = arms[key][name]
                fr = _fractions(d["dlp"], wpv, admitted)
                fl = _flips(d["flip"], admitted)
                kvr[name] = {"fraction": bootstrap_median_ci(fr), "flip": bootstrap_rate_ci(fl),
                             "median_dlp": float(np.median([x for x, a in zip(d["dlp"], admitted) if a])) if n_adm else None}
        return kvr
    summ["kv_range"] = kv_range_stats("kv_range", wp)

    # KV isolated (primary): fractions normalized by the isolated whole-path
    if "kv1_iso" in arms:
        kv1i = per_layer_stats(arms["kv1_iso"], wpv=wp_iso)
        kv1i_best, kv1i_beststat = best_layer(kv1i)
        summ["kv1_iso"] = {"per_layer": kv1i, "best_layer": kv1i_best, "best": kv1i_beststat}
        summ["kv_range_iso"] = kv_range_stats("kv_range_iso", wp_iso)

    # Resid-1
    r1 = per_layer_stats(arms["resid1"])
    r1_best, r1_beststat = best_layer(r1)
    early = [f"L{L}" for L in range(n_layers // 2)]
    early_hit = None
    for Lkey in early:
        if Lkey in r1 and r1[Lkey]["fraction"]["median"] is not None and r1[Lkey]["fraction"]["median"] >= 0.5:
            early_hit = Lkey
            break
    summ["resid1"] = {"per_layer": r1, "best_layer": r1_best, "best": r1_beststat,
                      "first_early_layer_ge_0.5": early_hit}

    if has_sae:
        sae_k = {}
        sae_k_best = {}
        for kkey, ld in arms.get("sae_k_by_k", {}).items():
            st = per_layer_stats(ld)
            b, bs = best_layer(st)
            sae_k[kkey] = st
            sae_k_best[kkey] = {"best_layer": b, "best": bs}
        summ["sae_k"] = {"per_layer": sae_k, "best": sae_k_best}

        sae_k_rand = {}
        for kkey, ld in arms.get("sae_k_random_by_k", {}).items():
            st = per_layer_stats(ld)
            b, bs = best_layer(st)
            sae_k_rand[kkey] = {"best_layer": b, "best": bs}
        summ["sae_k_random"] = sae_k_rand

        sw = per_layer_stats(arms.get("sae_swap", {}))
        sw_b, sw_bs = best_layer(sw)
        summ["sae_swap"] = {"per_layer": sw, "best_layer": sw_b, "best": sw_bs}

        def global_stats(arm_key):
            out = {}
            for Nkey, d in arms.get(arm_key, {}).items():
                fr = _fractions(d["dlp"], wp, admitted)
                fl = _flips(d["flip"], admitted)
                out[Nkey] = {"fraction": bootstrap_median_ci(fr), "flip": bootstrap_rate_ci(fl)}
            return out
        for arm_key in ("sae_global", "sae_global_random",
                        "sae_global_subject", "sae_global_subject_random",
                        "sae_global_nonfinal", "sae_global_nonfinal_random"):
            if arm_key in arms:
                summ[arm_key] = global_stats(arm_key)

        # steering / kv sufficiency (normalized gain)
        st_stats = {}
        for Lkey, d in arms.get("steering", {}).items():
            ng = _norm_gain(d["gain"], clean_lp, filler_lp, admitted)
            st_stats[Lkey] = bootstrap_median_ci(ng)
        st_best = max(st_stats.items(), key=lambda kv: (kv[1]["median"] if kv[1]["median"] is not None else -1e18), default=(None, None))
        summ["steering"] = {"per_layer": st_stats, "best_layer": st_best[0], "best": st_best[1]}

        kvs = {}
        for Lkey, d in arms.get("kv_suff_single", {}).items():
            ng = _norm_gain(d["gain"], clean_lp, filler_lp, admitted)
            kvs[Lkey] = bootstrap_median_ci(ng)
        kvs_best = max(kvs.items(), key=lambda kv: (kv[1]["median"] if kv[1]["median"] is not None else -1e18), default=(None, None))
        summ["kv_suff_single"] = {"per_layer": kvs, "best_layer": kvs_best[0], "best": kvs_best[1]}
        if "kv_suff_all" in arms:
            ng = _norm_gain(arms["kv_suff_all"]["gain"], clean_lp, filler_lp, admitted)
            summ["kv_suff_all"] = bootstrap_median_ci(ng)

    # ---- decision rules ----
    rules = {}
    if n_adm >= 12:
        # Rule 1 — in-forward variant
        bm = kv1_beststat["fraction"]["median"] if kv1_beststat else None
        rules["rule1_single_layer_kv_null_inforward"] = {
            "best_layer": kv1_best, "best_median_fraction": bm,
            "holds": (bm is not None and bm < 0.25)}
        # Rule 1 — isolated variant (PRIMARY)
        if "kv1_iso" in summ:
            bmi = summ["kv1_iso"]["best"]["fraction"]["median"] if summ["kv1_iso"]["best"] else None
            rules["rule1_single_layer_kv_null_isolated_PRIMARY"] = {
                "best_layer": summ["kv1_iso"]["best_layer"], "best_median_fraction": bmi,
                "holds": (bmi is not None and bmi < 0.25)}
        # Rule 2
        if has_sae and "sae_k" in summ and "k20" in summ["sae_k"]["per_layer"]:
            k20 = summ["sae_k"]["per_layer"]["k20"]
            best_frac = max((s["fraction"]["median"] for s in k20.values() if s["fraction"]["median"] is not None), default=None)
            best_flip = max((s["flip"]["rate"] for s in k20.values() if s["flip"]["rate"] is not None), default=None)
            rules["rule2_sae_single_layer_necessary"] = {
                "best_k20_median_fraction": best_frac, "best_k20_flip_rate": best_flip,
                "holds": ((best_frac is not None and best_frac >= 0.5) or (best_flip is not None and best_flip >= 0.5))}
        # Rule 3
        if has_sae and "sae_global" in summ and "N200" in summ["sae_global"]:
            m = summ["sae_global"]["N200"]["fraction"]["median"]
            rules["rule3_sae_global_faithful"] = {"N200_median_fraction": m,
                                                   "holds": (m is not None and m >= 0.5)}
        # Rule 4
        rb = r1_beststat["fraction"]["median"] if r1_beststat else None
        rules["rule4_residual_bus"] = {
            "best_layer": r1_best, "best_median_fraction": rb,
            "first_early_layer_ge_0.5": summ["resid1"]["first_early_layer_ge_0.5"],
            "predicted_holds": (summ["resid1"]["first_early_layer_ge_0.5"] is not None),
            "contradicts_paper": (summ["resid1"]["first_early_layer_ge_0.5"] is None)}
    else:
        rules["note"] = "fewer than 12 admitted items; decision rules not applied"
    summ["rules"] = rules
    return summ


# --------------------------------------------------------------------------- #
# Provenance / environment
# --------------------------------------------------------------------------- #
def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def scrub(obj):
    import re
    pat = re.compile(r"(/home/[^\s\"']*|/mnt/[^\s\"']*|/Users/[^\s\"']*|/root/[^\s\"']*)")
    if isinstance(obj, str):
        return pat.sub("<host-path>", obj)
    if isinstance(obj, dict):
        return {k: scrub(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [scrub(v) for v in obj]
    return obj


def resolve_provenance(hf_id, model_path):
    import glob
    prov = {"hf_id": hf_id, "requested_path": model_path}
    snap = None
    try:
        if os.path.isdir(model_path) and os.path.exists(os.path.join(model_path, "config.json")):
            snap = model_path
        else:
            from huggingface_hub import snapshot_download
            snap = snapshot_download(hf_id)
    except Exception as e:
        prov["resolve_error"] = str(e)[:200]
    if snap:
        real = os.path.realpath(snap)
        commit = os.path.basename(real)
        prov["commit"] = commit if len(commit) >= 12 else None
        st = {}
        for sf in sorted(glob.glob(os.path.join(snap, "*.safetensors"))):
            st[os.path.basename(sf)] = {"sha256": sha256_file(sf), "bytes": os.path.getsize(sf)}
        prov["safetensors"] = st
    return prov


def environment_snapshot():
    import importlib.metadata as md
    pkgs = {}
    for dist in md.distributions():
        try:
            pkgs[dist.metadata["Name"]] = dist.version
        except Exception:
            pass
    env = {
        "python": sys.version,
        "platform": platform.platform(),
        "torch": torch.__version__,
        "cuda_available": torch.cuda.is_available(),
        "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        "packages_selected": {k: pkgs.get(k) for k in
                              ["torch", "transformers", "sae-lens", "sae_lens",
                               "transformer-lens", "transformer_lens", "numpy",
                               "accelerate", "safetensors", "huggingface-hub",
                               "tokenizers"]},
        "packages_all": pkgs,
    }
    try:
        env["nvidia_smi"] = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,memory.total,driver_version",
             "--format=csv,noheader"], capture_output=True, text=True, timeout=20).stdout.strip()
    except Exception:
        env["nvidia_smi"] = None
    return env


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True, choices=list(MODELS.keys()))
    ap.add_argument("--model-path", default=None, help="override local snapshot path")
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--tl", action="store_true", help="run the TransformerLens cross-check")
    ap.add_argument("--out-tag", default="", help="suffix appended to output filenames, e.g. _v2")
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    torch.manual_seed(args.seed)
    np.random.seed(args.seed)
    if args.device.startswith("cuda"):
        torch.backends.cuda.matmul.allow_tf32 = False
        torch.backends.cudnn.allow_tf32 = False

    os.makedirs(args.out_dir, exist_ok=True)
    logs = []

    def log(msg):
        line = f"[{time.strftime('%H:%M:%S')}] {msg}"
        print(line, flush=True)
        logs.append(line)

    cfg = MODELS[args.model]
    model_path = args.model_path or cfg["hf_id"]
    dtype = torch.float32
    t0 = time.time()
    log(f"loading {args.model} from {model_path} (fp32, eager)")
    model, tok = load_model_and_tokenizer(args.model, model_path, args.device, dtype)
    layers = get_layers(model, cfg)
    n_layers = len(layers)
    log(f"loaded: {n_layers} layers, hidden {model.config.hidden_size}")

    behaviors = build_items(args.smoke)
    has_sae = cfg["sae"] is not None
    out = {"model": args.model, "smoke": args.smoke, "n_layers": n_layers,
           "provenance": resolve_provenance(cfg["hf_id"], model_path),
           "behaviors": {}, "summary": {}}

    for bname, beh in behaviors.items():
        log(f"behavior {bname}")
        candidate_ids = [tok.encode(" " + s, add_special_tokens=False)[0] for s in beh["candidates"]]
        raw = run_behavior(model, tok, cfg, args.device, dtype, beh, candidate_ids,
                           cfg["sae"], layers, log, seed=args.seed)
        out["behaviors"][bname] = raw
        summ = aggregate_behavior(raw, n_layers, has_sae)
        out["summary"][bname] = summ
        log(f"  admitted {summ['n_admitted']}/{summ['n_items']}; gates "
            f"kv_noop={raw['gates'].get('kv_noop_max')}, "
            f"resid_noop={raw['gates'].get('resid_noop_max')}, "
            f"sae_noop={raw['gates'].get('sae_noop_max')}")

    # ---- TransformerLens cross-check (secondary) ----
    # Capture HF-side timing while the HF model is still resident, THEN delete the HF
    # model + free the GPU so the HF and TL fp32 copies never coexist on the 16 GB card.
    if args.tl and args.model in TL_NAMES:
        log("TransformerLens cross-check")
        try:
            import gc
            hf_timing = {}
            first_cd = None
            for b in out["behaviors"].values():
                if b.get("context_data"):
                    first_cd = b["context_data"][0]; break
            if first_cd is not None:
                PatchCacheCls = make_patch_cache_class()
                cids = torch.tensor(first_cd["clean_ids"], device=args.device)
                nrep = min(n_layers, 12)
                hf_full, hf_cached = time_hf(model, PatchCacheCls, cids, first_cd["subj_pos"], nrep, args.device)
                hf_timing = {"n_reps": nrep, "n_items_ctx": cids.shape[0],
                             "hf_full_recompute_s": hf_full, "hf_cached_prefix_s": hf_cached,
                             "hf_full_per_item_per_interv_ms": 1000 * hf_full / (nrep * cids.shape[0]),
                             "hf_cached_per_item_per_interv_ms": 1000 * hf_cached / (nrep * cids.shape[0])}
                del cids
            model.to("cpu")
            del model
            gc.collect()
            if args.device.startswith("cuda"):
                torch.cuda.empty_cache()
            out["tl"] = run_tl_comparison(args.model, cfg, model_path, tok, args.device, dtype,
                                          out["behaviors"], cfg["sae"], n_layers, log, hf_timing)
            for bn, bd in out["tl"]["behaviors"].items():
                log(f"  TL[{bn}] clean_gate={bd['clean_logit_gate']:.2e} "
                    f"agreement={ {k: round(v['max_abs_dlp_diff'],5) for k,v in bd['arm_agreement'].items()} }")
        except Exception as e:
            import traceback; traceback.print_exc()
            out["tl"] = {"error": str(e)[:400]}
            log(f"  TL comparison FAILED: {str(e)[:200]}")

    out["elapsed_s"] = time.time() - t0
    env = environment_snapshot()

    tag = f"{args.model}{'_smoke' if args.smoke else ''}{args.out_tag}"
    raw_path = os.path.join(args.out_dir, f"raw_{tag}.json")
    summ_path = os.path.join(args.out_dir, f"summary_{tag}.json")
    adm_path = os.path.join(args.out_dir, f"admission_{tag}.json")
    env_path = os.path.join(args.out_dir, f"environment_{tag}.json")
    log_path = os.path.join(args.out_dir, f"log_{tag}.txt")

    admission_table = {b: {"n_items": s["n_items"], "n_admitted": s["n_admitted"],
                           "usable_for_rules": s["usable_for_rules"],
                           "items": [{"context_idx": it["context_idx"], "subject": it["subject"],
                                      "admitted": it["admitted"], "clean_lp": it["clean_lp"],
                                      "filler_lp": it["filler_lp"]} for it in out["behaviors"][b]["items"]]}
                       for b, s in out["summary"].items()}

    # trim in-process-only bulk from the raw before writing
    for b in out["behaviors"]:
        out["behaviors"][b].pop("context_data", None)
        out["behaviors"][b].pop("sae_selected_k20", None)
    with open(raw_path, "w") as f:
        json.dump(scrub(out), f, indent=1)
    with open(summ_path, "w") as f:
        json.dump(scrub({"model": args.model, "smoke": args.smoke, "n_layers": n_layers,
                         "provenance": out["provenance"], "summary": out["summary"],
                         "tl": out.get("tl"),
                         "gates": {b: out["behaviors"][b]["gates"] for b in out["behaviors"]},
                         "elapsed_s": out["elapsed_s"]}), f, indent=1)
    with open(adm_path, "w") as f:
        json.dump(scrub(admission_table), f, indent=1)
    with open(env_path, "w") as f:
        json.dump(scrub(env), f, indent=1)
    with open(log_path, "w") as f:
        f.write("\n".join(scrub(logs)))
    log(f"wrote {raw_path}, {summ_path}, {adm_path}, {env_path}")


# --------------------------------------------------------------------------- #
# TransformerLens cross-check (secondary, descriptive)
# --------------------------------------------------------------------------- #
TL_NAMES = {"gpt2": "gpt2", "qwen15": "Qwen/Qwen2.5-1.5B", "gemma2": "google/gemma-2-2b"}
TL_SEQUENTIAL = {"gemma2", "qwen15"}  # HF + TL fp32 don't both fit; build TL then free HF


def _inject_tl_config(model_key, hf_model, hf_home):
    """TL resolves the model config from its HF repo name (which may be gated, e.g.
    google/gemma-2-2b, or absent from HF_HOME when the HF weights were loaded from an
    explicit local snapshot, e.g. Qwen2.5-1.5B). Inject the identical config+tokenizer
    that the HF model actually used, under the TL cache name, so TL loads it offline."""
    import shutil
    name = TL_NAMES[model_key]
    if "/" not in name:  # gpt2: ungated and cached under its own name
        return
    src = getattr(hf_model, "name_or_path", None) or getattr(hf_model.config, "_name_or_path", None)
    if src and not os.path.isdir(src):
        try:
            from huggingface_hub import snapshot_download
            src = snapshot_download(src)
        except Exception:
            src = None
    if not src or not os.path.isdir(src):
        return
    org, repo = name.split("/", 1)
    fake = os.path.join(hf_home, "hub", f"models--{org}--{repo}")
    snapdir = os.path.join(fake, "snapshots", "mirror0")
    if os.path.exists(os.path.join(snapdir, "config.json")):
        return
    os.makedirs(snapdir, exist_ok=True)
    os.makedirs(os.path.join(fake, "refs"), exist_ok=True)
    with open(os.path.join(fake, "refs", "main"), "w") as f:
        f.write("mirror0")
    for fn in ["config.json", "tokenizer.json", "tokenizer_config.json", "special_tokens_map.json",
               "generation_config.json", "tokenizer.model", "vocab.json", "merges.txt"]:
        s = os.path.join(src, fn)
        if os.path.exists(s):
            shutil.copy(s, os.path.join(snapdir, fn))


def load_tl_model(model_key, hf_model, tok, build_device, dtype):
    from sae_lens import HookedSAETransformer
    name = TL_NAMES[model_key]
    _inject_tl_config(model_key, hf_model,
                      os.environ.get("HF_HOME", os.path.expanduser("~/.cache/huggingface")))
    tl = HookedSAETransformer.from_pretrained(
        name, hf_model=hf_model, tokenizer=tok, device=build_device, dtype=dtype,
        fold_ln=False, center_writing_weights=False, center_unembed=False,
        fold_value_biases=False,
    )
    tl.eval()
    return tl


class TLRunner:
    """Computes TransformerLens Δlp for the arms, aligned to one context's items."""

    def __init__(self, tl, cfg, cd, candidate_ids, device):
        self.tl = tl
        self.cfg = cfg
        self.cd = cd
        self.candidate_ids = candidate_ids
        self.device = device
        self.subj = cd["subj_pos"]
        self.S = cd["seq_len"]
        self.clean_ids = torch.tensor(cd["clean_ids"], device=device)
        self.filler_ids = torch.tensor(cd["filler_ids"], device=device)
        self.answer_ids = torch.tensor(cd["answer_ids"], device=device)
        self.is_post = cfg["sae"]["hook"] == "post" if cfg["sae"] else False

    @torch.no_grad()
    def capture(self):
        tl = self.tl
        logits, cache = tl.run_with_cache(self.clean_ids)
        self.clean_last = logits[:, -1, :].float()
        self.clean_lp = answer_logprobs(self.clean_last, self.answer_ids)
        self.clean_top1 = top1_candidate(self.clean_last, self.candidate_ids)
        self.clean_cache = cache
        flogits, fcache = tl.run_with_cache(self.filler_ids)
        self.filler_cache = fcache

    def _dl(self, last):
        lp = answer_logprobs(last.float(), self.answer_ids)
        dlp = (lp - self.clean_lp).detach().cpu().numpy()
        top1 = top1_candidate(last, self.candidate_ids)
        flip = (top1 != self.clean_top1).detach().cpu().numpy().astype(float)
        return dlp, flip

    @torch.no_grad()
    def resid1(self, L):
        name = f"blocks.{L}.hook_resid_pre"
        fill = self.filler_cache[name][:, self.subj, :]

        def hook(act, hook):
            act[:, self.subj, :] = fill.to(act.dtype)
            return act
        last = self.tl.run_with_hooks(self.clean_ids, fwd_hooks=[(name, hook)])[:, -1, :]
        return self._dl(last)

    @torch.no_grad()
    def kv_inforward(self, L):
        kn, vn = f"blocks.{L}.attn.hook_k", f"blocks.{L}.attn.hook_v"
        fk = self.filler_cache[kn][:, self.subj, :, :]
        fv = self.filler_cache[vn][:, self.subj, :, :]

        def hk(act, hook):
            act[:, self.subj, :, :] = fk.to(act.dtype)
            return act

        def hv(act, hook):
            act[:, self.subj, :, :] = fv.to(act.dtype)
            return act
        last = self.tl.run_with_hooks(self.clean_ids, fwd_hooks=[(kn, hk), (vn, hv)])[:, -1, :]
        return self._dl(last)

    @torch.no_grad()
    def _kv_iso_last(self, layer_indices):
        from transformer_lens.cache.key_value_cache import TransformerLensKeyValueCache
        subj, S = self.subj, self.S
        B = self.clean_ids.shape[0]
        prefix = self.clean_ids[:, : subj + 1]
        suffix = self.clean_ids[:, subj + 1:]
        cache = TransformerLensKeyValueCache.init_cache(self.tl.cfg, self.device, B)
        self.tl(prefix, past_kv_cache=cache)
        if layer_indices is not None:
            fpref = self.filler_ids[:, : subj + 1]
            fcache = TransformerLensKeyValueCache.init_cache(self.tl.cfg, self.device, 1)
            self.tl(fpref, past_kv_cache=fcache)
            for L in layer_indices:
                cache[L].past_keys[:, subj, :, :] = fcache[L].past_keys[:, subj, :, :]
                cache[L].past_values[:, subj, :, :] = fcache[L].past_values[:, subj, :, :]
        if suffix.shape[1] == 0:
            return self.tl(prefix)[:, -1, :]
        return self.tl(suffix, past_kv_cache=cache)[:, -1, :]

    @torch.no_grad()
    def kv_iso_baseline(self):
        self._split_last = self._kv_iso_last(None)
        self._split_lp = answer_logprobs(self._split_last.float(), self.answer_ids)
        self._split_top1 = top1_candidate(self._split_last, self.candidate_ids)
        return float((self._split_last - self.clean_last).abs().max().item())

    @torch.no_grad()
    def kv_isolated(self, layer_indices):
        last = self._kv_iso_last(list(layer_indices))
        lp = answer_logprobs(last.float(), self.answer_ids)
        dlp = (lp - self._split_lp).detach().cpu().numpy()
        top1 = top1_candidate(last, self.candidate_ids)
        flip = (top1 != self._split_top1).detach().cpu().numpy().astype(float)
        return dlp, flip

    @torch.no_grad()
    def sae_k(self, sae, L, sel):
        """Ablate the given latent ids (per item) at the subject position via the
        attached SAE, keeping the error term (so clean is identity)."""
        sae.use_error_term = True
        hookname = sae.cfg.metadata.hook_name + ".hook_sae_acts_post"
        subj = self.subj

        def zero(acts, hook):
            for b in range(acts.shape[0]):
                if sel[b]:
                    acts[b, subj, sel[b]] = 0.0
            return acts
        last = self.tl.run_with_hooks_with_saes(
            self.clean_ids, saes=[sae], fwd_hooks=[(hookname, zero)])[:, -1, :]
        self.tl.reset_saes()
        return self._dl(last)


def _sync(device):
    if device.startswith("cuda"):
        torch.cuda.synchronize()


def _fork_hf_cache(PatchCacheCls, cache):
    """Clone a filled HF cache so each suffix run starts from the same prefix state."""
    new = PatchCacheCls()
    for entry in cache.layers:
        new.update(entry.keys.clone(), entry.values.clone(), len(new.layers))
    return new


@torch.no_grad()
def time_hf(model, PatchCacheCls, clean_ids, subj, n_reps, device):
    prefix = clean_ids[:, : subj + 1]
    suffix = clean_ids[:, subj + 1:]
    # warmup
    model(input_ids=clean_ids)
    c = PatchCacheCls(); model(input_ids=prefix, use_cache=True, past_key_values=c)
    _sync(device)
    t0 = time.perf_counter()
    for _ in range(n_reps):
        model(input_ids=clean_ids)
    _sync(device); full = time.perf_counter() - t0
    base = PatchCacheCls(); model(input_ids=prefix, use_cache=True, past_key_values=base)
    _sync(device)
    t0 = time.perf_counter()
    for _ in range(n_reps):
        fk = _fork_hf_cache(PatchCacheCls, base)
        model(input_ids=suffix, use_cache=True, past_key_values=fk)
    _sync(device); cached = time.perf_counter() - t0
    return full, cached


@torch.no_grad()
def time_tl(tl, clean_ids, subj, n_reps, device):
    from transformer_lens.cache.key_value_cache import TransformerLensKeyValueCache
    B = clean_ids.shape[0]
    prefix = clean_ids[:, : subj + 1]
    suffix = clean_ids[:, subj + 1:]
    tl(clean_ids)  # warmup
    _sync(device)
    t0 = time.perf_counter()
    for _ in range(n_reps):
        tl(clean_ids)
    _sync(device); full = time.perf_counter() - t0
    _sync(device)
    t0 = time.perf_counter()
    for _ in range(n_reps):
        c = TransformerLensKeyValueCache.init_cache(tl.cfg, device, B)
        tl(prefix, past_kv_cache=c)
        tl(suffix, past_kv_cache=c)
    _sync(device); cached = time.perf_counter() - t0
    return full, cached


def run_tl_comparison(model_key, cfg, model_path, tok, device, dtype, behaviors_raw,
                      sae_cfg, n_layers, log, hf_timing=None):
    """The HF model has already been deleted off the GPU by the caller (so HF and TL
    fp32 copies never coexist on the card). TL is built from a fresh CPU copy of the
    weights and only then moved to the GPU; the HF Δlp arrays come from behaviors_raw."""
    import gc
    import transformer_lens
    try:
        import importlib.metadata as _md
        tl_version = _md.version("transformer_lens")
    except Exception:
        tl_version = getattr(transformer_lens, "__version__", "unknown")
    result = {"tl_version": tl_version, "tl_name": TL_NAMES[model_key],
              "processing": "no_processing (fold_ln=F, center_writing_weights=F, center_unembed=F, fold_value_biases=F)",
              "behaviors": {}, "timing": dict(hf_timing or {})}

    first_cd = None
    for b, raw in behaviors_raw.items():
        if raw.get("context_data"):
            first_cd = raw["context_data"][0]; break

    # ---- build TL: fresh CPU weights -> TL on CPU -> del HF -> TL to GPU ----
    log("  building TransformerLens model (CPU build, then move to GPU)")
    from transformers import AutoModelForCausalLM
    hf_cpu = AutoModelForCausalLM.from_pretrained(
        model_path, dtype=dtype, attn_implementation="eager").eval()
    tl = load_tl_model(model_key, hf_cpu, tok, "cpu", dtype)
    del hf_cpu
    gc.collect()
    if device.startswith("cuda"):
        torch.cuda.empty_cache()
    tl.to(device)
    gc.collect()
    if device.startswith("cuda"):
        torch.cuda.empty_cache()

    if first_cd is not None:
        cids = torch.tensor(first_cd["clean_ids"], device=device)
        subj = first_cd["subj_pos"]
        nrep = result["timing"].get("n_reps") or min(n_layers, 12)
        result["timing"]["n_reps"] = nrep
        result["timing"]["n_items_ctx"] = cids.shape[0]
        tl_full, tl_cached = time_tl(tl, cids, subj, nrep, device)
        result["timing"]["tl_full_recompute_s"] = tl_full
        result["timing"]["tl_cached_prefix_s"] = tl_cached
        result["timing"]["tl_full_per_item_per_interv_ms"] = 1000 * tl_full / (nrep * cids.shape[0])
        result["timing"]["tl_cached_per_item_per_interv_ms"] = 1000 * tl_cached / (nrep * cids.shape[0])

    sae_layers = list(range(n_layers)) if sae_cfg else []

    for bname, raw in behaviors_raw.items():
        cds = raw["context_data"]
        if not cds:
            continue
        admitted = [it["admitted"] for it in raw["items"]]
        cand = raw["candidates"]
        # accumulate TL dlp per arm/layer aligned to item order
        tl_arms = {}
        clean_gate = 0.0
        iso_split_gate = 0.0
        runners = []
        for cd in cds:
            r = TLRunner(tl, cfg, cd, cand, device)
            r.capture()
            # clean-logit agreement vs HF clean lp
            hf_lp = torch.tensor(cd["clean_lp_hf"], device=device)
            clean_gate = max(clean_gate, float((r.clean_lp - hf_lp).abs().max().item()))
            iso_split_gate = max(iso_split_gate, r.kv_iso_baseline())
            runners.append(r)

        def acc(arm, Lkey, dlp, flip):
            d = tl_arms.setdefault(arm, {}).setdefault(Lkey, {"dlp": [], "flip": []})
            d["dlp"].extend([float(x) for x in dlp]); d["flip"].extend([float(x) for x in flip])

        for L in range(n_layers):
            for r in runners:
                acc("resid1", f"L{L}", *r.resid1(L))
            for r in runners:
                acc("kv1", f"L{L}", *r.kv_inforward(L))
            for r in runners:
                acc("kv1_iso", f"L{L}", *r.kv_isolated([L]))

        # SAE-k (k=20) reusing HF-selected latents
        if sae_cfg:
            sel_all = raw.get("sae_selected_k20", {})
            for L in sae_layers:
                sae = load_sae(sae_cfg["release"], sae_cfg["sae_id"].format(L=L), device)
                for r in runners:
                    sel = sel_all.get(str(r.cd["context_idx"]), {}).get(str(L))
                    if sel is None:
                        continue
                    acc("sae_k20", f"L{L}", *r.sae_k(sae, L, sel))
                del sae
                if device.startswith("cuda"):
                    torch.cuda.empty_cache()

        # ---- agreement vs HF ----
        hf_arms = raw["arms"]
        agree = {}

        def compare(tl_key, hf_key, sub=None):
            worst = 0.0; nseen = 0
            tld = tl_arms.get(tl_key, {})
            for Lkey, d in tld.items():
                hd = (hf_arms.get(hf_key, {}) if sub is None
                      else hf_arms.get(hf_key, {}).get(sub, {})).get(Lkey)
                if hd is None:
                    continue
                for a, bb in zip(d["dlp"], hd["dlp"]):
                    worst = max(worst, abs(a - bb)); nseen += 1
            return {"max_abs_dlp_diff": worst, "n": nseen}
        agree["resid1"] = compare("resid1", "resid1")
        agree["kv1_inforward"] = compare("kv1", "kv1")
        agree["kv1_isolated"] = compare("kv1_iso", "kv1_iso")
        if sae_cfg:
            agree["sae_k20"] = compare("sae_k20", "sae_k_by_k", sub="k20")

        # ---- verdict agreement: rule1 (isolated) + rule2 (sae20) on TL dlp ----
        wp_iso = raw["whole_path_iso_dlp"]
        wp = raw["whole_path_dlp"]

        def best_frac(tl_key, wpv):
            best = None
            for Lkey, d in tl_arms.get(tl_key, {}).items():
                fr = _fractions(d["dlp"], wpv, admitted)
                m = float(np.median(fr)) if fr else None
                if m is not None and (best is None or m > best):
                    best = m
            return best
        n_adm = int(sum(admitted))
        verdict = {}
        if n_adm >= 12:
            tl_r1 = best_frac("kv1_iso", wp_iso)
            hf_r1 = raw_rule(raw, "rule1_iso")
            verdict["rule1_isolated"] = {"tl_best_fraction": tl_r1,
                                         "tl_holds": (tl_r1 is not None and tl_r1 < 0.25),
                                         "hf_holds": hf_r1, "agree": ((tl_r1 is not None and tl_r1 < 0.25) == hf_r1) if hf_r1 is not None else None}
            if sae_cfg:
                tl_r2 = best_frac("sae_k20", wp)
                hf_r2 = raw_rule(raw, "rule2")
                verdict["rule2_sae20"] = {"tl_best_fraction": tl_r2,
                                          "tl_holds": (tl_r2 is not None and tl_r2 >= 0.5),
                                          "hf_holds": hf_r2, "agree": ((tl_r2 is not None and tl_r2 >= 0.5) == hf_r2) if hf_r2 is not None else None}
        result["behaviors"][bname] = {"clean_logit_gate": clean_gate,
                                      "isolated_split_gate": iso_split_gate,
                                      "arm_agreement": agree, "verdict_agreement": verdict,
                                      "n_admitted": n_adm}
    return result


def raw_rule(raw, which):
    """Recompute the HF verdict (holds bool) from the raw arms for TL comparison."""
    items = raw["items"]; admitted = [it["admitted"] for it in items]
    if int(sum(admitted)) < 12:
        return None
    wp = raw["whole_path_dlp"]; wp_iso = raw["whole_path_iso_dlp"]; arms = raw["arms"]
    if which == "rule1_iso":
        best = None
        for Lkey, d in arms.get("kv1_iso", {}).items():
            fr = _fractions(d["dlp"], wp_iso, admitted)
            m = float(np.median(fr)) if fr else None
            if m is not None and (best is None or m > best):
                best = m
        return (best is not None and best < 0.25)
    if which == "rule2":
        best = None
        for Lkey, d in arms.get("sae_k_by_k", {}).get("k20", {}).items():
            fr = _fractions(d["dlp"], wp, admitted)
            m = float(np.median(fr)) if fr else None
            if m is not None and (best is None or m > best):
                best = m
        return (best is not None and best >= 0.5)
    return None


if __name__ == "__main__":
    main()
