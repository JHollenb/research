#!/usr/bin/env python3
"""E14 — per-layer sweep of a hybrid (parallel attention + Mamba2) LM at TWO cuts.

For Falcon-H1 every decoder layer runs `self_attn` (K/V cache) and `mamba` (conv +
recurrent SSM state) in parallel on the same input, summed with per-path multipliers.
This worker reads the SAME identity/color panel + admission as the transformer panel
(`run_sae_comparison.py`, vendored unchanged for its pure helpers) and runs, per
behavior, four-quadrant arms at BOTH cuts plus window necessity for the attention path.

Isolated swap (paper §2.3 rule 2): prefix = tokens through the subject; suffix = the
rest (identical across subjects). Donor stores are captured by prefilling the prefix.
Every arm re-prefills a fresh cache, patches the named cut, and REPLAYS THE SUFFIX
TOKEN-BY-TOKEN (the exact single-token decode path, validated in the Mamba sweep
worker; it advances both the attention cache and the SSM state). Exact no-op gates for
both cuts. Emits a gzip+b64 MARKER line for the submitter to collect from the job log.
"""
from __future__ import annotations

import base64
import gzip
import json
import os
import time
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
# reduce reserved-VRAM fragmentation from churning per-leg hybrid caches
os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")

import numpy as np
import torch

import run_sae_comparison as rsc  # vendored unchanged; pure helpers + panel builders

MARKER = "SATURN_E14_HYBRID_GZIP_B64="

WINDOW_WIDTHS = (2, 3, 4, 6)


# --------------------------------------------------------------------------- #
# Per-(behavior, context) runner over the two cuts
# --------------------------------------------------------------------------- #
class HybridCtx:
    def __init__(self, model, tok, device, dtype, behavior, context, candidate_ids,
                 layers, log, suffix_mode="chunk"):
        self.model = model
        self.tok = tok
        self.device = device
        self.dtype = dtype
        self.behavior = behavior
        self.context = context
        self.candidate_ids = candidate_ids
        self.layers = layers
        self.n_layers = len(layers)
        self.log = log
        self.suffix_mode = suffix_mode  # "chunk" (1 fwd/leg) or "token" (exact, slow)
        self.usable = False

    # ---- tokenize, find subject position (copied from rsc.ContextRunner.prepare) -- #
    def prepare(self):
        beh = self.behavior
        subjects = beh["subjects"]
        prompts = [rsc.render_prompt(beh, self.context, s) for s in subjects]
        filler_prompt = rsc.render_prompt(beh, self.context, beh["filler_word"])
        enc = [self.tok.encode(p, add_special_tokens=True) for p in prompts]
        enc_filler = self.tok.encode(filler_prompt, add_special_tokens=True)
        admit_mask, subj_pos, base_len = [], None, len(enc_filler)
        clean_ids, answer_ids = [], []
        for s, e in zip(subjects, enc):
            ans_id = self.tok.encode(" " + s, add_special_tokens=False)
            ok = (len(e) == base_len) and (len(ans_id) == 1)
            diff = [i for i in range(min(len(e), base_len)) if e[i] != enc_filler[i]]
            if len(e) == base_len and len(diff) == 1:
                if subj_pos is None:
                    subj_pos = diff[0]
                ok = ok and (diff[0] == subj_pos)
            else:
                ok = False
            admit_mask.append(ok)
            clean_ids.append(e)
            answer_ids.append(ans_id[0] if len(ans_id) == 1 else -1)
        if subj_pos is None:
            self.usable = False
            return
        self.usable = True
        keep = [i for i, ok in enumerate(admit_mask) if ok]
        self.subjects = [subjects[i] for i in keep]
        self.subj_pos = subj_pos
        self.answer_ids = torch.tensor([answer_ids[i] for i in keep], device=self.device)
        self.clean_input = torch.tensor([clean_ids[i] for i in keep], device=self.device)
        self.filler_input = torch.tensor([enc_filler], device=self.device)
        self.seq_len = self.clean_input.shape[1]
        self.filler_prompt = filler_prompt
        self.prompts = [prompts[i] for i in keep]
        self.suffix_toks = [int(x) for x in self.clean_input[0, subj_pos + 1:].tolist()]

    # ---- cache helpers ------------------------------------------------------ #
    def _new_cache(self):
        from transformers.cache_utils import DynamicCache
        return DynamicCache(config=self.model.config)

    @torch.no_grad()
    def _prefill(self, input_ids):
        """Prefill the prefix (through the subject) into a fresh cache; return cache."""
        cache = self._new_cache()
        self.model(input_ids=input_ids[:, : self.subj_pos + 1], use_cache=True,
                   past_key_values=cache)
        return cache

    def _extract_stores(self, cache):
        """Per-layer donor stores at the cut: attention K/V column at subj, and the
        full Mamba conv + recurrent state."""
        subj = self.subj_pos
        store = {"K": [], "V": [], "conv": [], "rec": []}
        for L in range(self.n_layers):
            lyr = cache.layers[L]
            store["K"].append(lyr.keys[:, :, subj, :].detach().clone())
            store["V"].append(lyr.values[:, :, subj, :].detach().clone())
            store["conv"].append(lyr.conv_states[0].detach().clone())
            store["rec"].append(lyr.recurrent_states[0].detach().clone())
        return store

    @torch.no_grad()
    def _replay_suffix(self, cache, B, mode=None):
        """Advance the cache over the (shared) suffix and return last logits [B, V].
        mode 'chunk' = one multi-token forward; 'token' = token-by-token decode
        (exact single-step path). Both read the patched prefix cache."""
        mode = mode or self.suffix_mode
        if not self.suffix_toks:
            out = self.model(input_ids=self.clean_input[:, : self.subj_pos + 1],
                             use_cache=False)
            return out.logits[:, -1, :].detach()
        if mode == "chunk":
            suffix = torch.tensor([self.suffix_toks], dtype=torch.long,
                                  device=self.device).repeat(B, 1)
            out = self.model(input_ids=suffix, use_cache=True, past_key_values=cache)
            return out.logits[:, -1, :].detach()
        last = None
        for t in self.suffix_toks:
            tok = torch.full((B, 1), t, dtype=torch.long, device=self.device)
            out = self.model(input_ids=tok, use_cache=True, past_key_values=cache)
            last = out.logits[:, -1, :].detach()
        return last

    # ---- patch functions ---------------------------------------------------- #
    def _patch_attn(self, cache, donor, layers, B):
        subj = self.subj_pos
        for L in layers:
            lyr = cache.layers[L]
            lyr.keys[:, :, subj, :] = donor["K"][L].to(lyr.keys.dtype)
            lyr.values[:, :, subj, :] = donor["V"][L].to(lyr.values.dtype)

    def _patch_ssm(self, cache, donor, layers, B):
        for L in layers:
            lyr = cache.layers[L]
            lyr.conv_states[0][...] = donor["conv"][L].to(lyr.conv_states[0].dtype)
            lyr.recurrent_states[0][...] = donor["rec"][L].to(lyr.recurrent_states[0].dtype)

    # ---- setup -------------------------------------------------------------- #
    @torch.no_grad()
    def capture(self):
        B = self.clean_input.shape[0]
        # canonical clean + filler (no cache) last logits
        self.clean_logits = self.model(input_ids=self.clean_input, use_cache=False).logits[:, -1, :].detach()
        self.filler_logits = self.model(input_ids=self.filler_input, use_cache=False).logits[:, -1, :].detach()
        self.clean_lp = rsc.answer_logprobs(self.clean_logits, self.answer_ids)
        self.filler_lp = rsc.answer_logprobs(self.filler_logits, self.answer_ids)
        self.clean_top1 = rsc.top1_candidate(self.clean_logits, self.candidate_ids)
        # donor stores
        self.clean_store = self._extract_stores(self._prefill(self.clean_input))     # B rows
        self.filler_store = self._extract_stores(self._prefill(self.filler_input))   # 1 row
        # split no-op baseline (prefix/suffix replay, no overwrite) and gate, in the
        # ACTIVE mode (this is the gate the arms rely on)
        base_cache = self._prefill(self.clean_input)
        self.split_logits = self._replay_suffix(base_cache, B)
        self.split_lp = rsc.answer_logprobs(self.split_logits, self.answer_ids)
        self.split_top1 = rsc.top1_candidate(self.split_logits, self.candidate_ids)
        self.split_noop_max = float((self.split_logits - self.clean_logits).abs().max().item())
        # reference: the token-by-token split no-op (exact single-step path)
        tok_logits = self._replay_suffix(self._prefill(self.clean_input), B, mode="token")
        self.split_noop_token_max = float((tok_logits - self.clean_logits).abs().max().item())

    def admission(self):
        adm = []
        for i in range(len(self.subjects)):
            top1 = int(self.clean_top1[i].item()) == int(self.answer_ids[i].item())
            drop = (self.clean_lp[i].item() - self.filler_lp[i].item()) >= 1.0
            adm.append(bool(top1 and drop))
        self.admitted = adm
        return adm

    # ---- necessity leg ------------------------------------------------------ #
    @torch.no_grad()
    def _necessity(self, cut, layers):
        """Overwrite the clean cache's cut at `layers` with the FILLER donor; replay.
        Returns (dlp vs split baseline, flip vs split top1)."""
        B = self.clean_input.shape[0]
        cache = self._prefill(self.clean_input)
        patch = self._patch_attn if cut == "attn" else self._patch_ssm
        patch(cache, self.filler_store, layers, B)
        logits = self._replay_suffix(cache, B)
        lp = rsc.answer_logprobs(logits, self.answer_ids)
        dlp = (lp - self.split_lp).detach().cpu().numpy()
        top1 = rsc.top1_candidate(logits, self.candidate_ids)
        flip = (top1 != self.split_top1).detach().cpu().numpy().astype(float)
        return dlp, flip

    # ---- write leg ---------------------------------------------------------- #
    @torch.no_grad()
    def _write(self, cut, layers, source="clean"):
        """Prefill FILLER prefix (B rows), overwrite cut at `layers` with the per-row
        CLEAN subject store (source='filler' => filler's own = no-op), replay suffix.
        Returns per-row gain vs filler_lp."""
        B = len(self.subjects)
        filler_batch = self.filler_input.repeat(B, 1)
        cache = self._new_cache()
        self.model(input_ids=filler_batch[:, : self.subj_pos + 1], use_cache=True,
                   past_key_values=cache)
        donor = self.clean_store if source == "clean" else self.filler_store
        patch = self._patch_attn if cut == "attn" else self._patch_ssm
        patch(cache, donor, layers, B)
        last = self._replay_suffix_on(cache, filler_batch, B)
        lp = rsc.answer_logprobs(last, self.answer_ids)
        return (lp - self.filler_lp).detach().cpu().numpy()

    @torch.no_grad()
    def _replay_suffix_on(self, cache, prefix_batch, B, mode=None):
        """Advance `cache` over the shared suffix for a write leg (prefix_batch is the
        filler batch); return last logits."""
        mode = mode or self.suffix_mode
        if not self.suffix_toks:
            return self.model(input_ids=prefix_batch[:, : self.subj_pos + 1],
                              use_cache=False).logits[:, -1, :].detach()
        if mode == "chunk":
            suffix = torch.tensor([self.suffix_toks], dtype=torch.long,
                                  device=self.device).repeat(B, 1)
            return self.model(input_ids=suffix, use_cache=True,
                              past_key_values=cache).logits[:, -1, :].detach()
        last = None
        for t in self.suffix_toks:
            tok = torch.full((B, 1), t, dtype=torch.long, device=self.device)
            last = self.model(input_ids=tok, use_cache=True,
                              past_key_values=cache).logits[:, -1, :].detach()
        return last


# --------------------------------------------------------------------------- #
# Aggregation over contexts for one behavior
# --------------------------------------------------------------------------- #
def run_behavior(model, tok, device, dtype, behavior, cand, layers, log,
                 do_windows=True, suffix_mode="chunk"):
    n = len(layers)
    runners = []
    for ci, ctx in enumerate(behavior["contexts"]):
        cr = HybridCtx(model, tok, device, dtype, behavior, ctx, cand, layers, log,
                       suffix_mode=suffix_mode)
        cr.prepare()
        if not cr.usable:
            log(f"  context {ci}: not usable, skipped")
            continue
        cr.capture()
        cr.admission()
        runners.append(cr)
        log(f"  ctx {ci}: kept {len(cr.subjects)} admitted {sum(cr.admitted)} "
            f"subj_pos {cr.subj_pos} seq {cr.seq_len} suffix {len(cr.suffix_toks)} "
            f"split_noop {cr.split_noop_max:.2e}")
    if not runners:
        return {"error": "no usable contexts"}

    admitted = [bool(a) for cr in runners for a in cr.admitted]
    clean_lp = [float(x) for cr in runners for x in cr.clean_lp.tolist()]
    filler_lp = [float(x) for cr in runners for x in cr.filler_lp.tolist()]

    def collect_nec(cut, layers_set):
        dlp, flip = [], []
        for cr in runners:
            d, f = cr._necessity(cut, layers_set)
            dlp.extend(float(x) for x in d)
            flip.extend(float(x) for x in f)
        return dlp, flip

    def collect_write(cut, layers_set, source="clean"):
        g = []
        for cr in runners:
            g.extend(float(x) for x in cr._write(cut, layers_set, source=source))
        return g

    first = list(range(0, n // 2))
    second = list(range(n // 2, n))
    allL = list(range(n))

    # ---- whole-path necessity (denominators) ----
    attn_all_dlp, attn_all_flip = collect_nec("attn", allL)
    ssm_all_dlp, ssm_all_flip = collect_nec("ssm", allL)
    both_all_dlp, both_all_flip = [], []
    for cr in runners:
        B = cr.clean_input.shape[0]
        cache = cr._prefill(cr.clean_input)
        cr._patch_attn(cache, cr.filler_store, allL, B)
        cr._patch_ssm(cache, cr.filler_store, allL, B)
        logits = cr._replay_suffix(cache, B)
        lp = rsc.answer_logprobs(logits, cr.answer_ids)
        d = (lp - cr.split_lp).detach().cpu().numpy()
        t1 = rsc.top1_candidate(logits, cr.candidate_ids)
        fl = (t1 != cr.split_top1).detach().cpu().numpy().astype(float)
        both_all_dlp.extend(float(x) for x in d)
        both_all_flip.extend(float(x) for x in fl)

    def med(vals):
        v = [x for x, a in zip(vals, admitted) if a]
        return float(np.median(v)) if v else None

    def flip_rate(vals):
        return rsc.bootstrap_rate_ci(rsc._flips(vals, admitted))

    def frac_stats(dlp, denom_dlp, flip):
        fr = rsc._fractions(dlp, denom_dlp, admitted)
        return {"fraction": rsc.bootstrap_median_ci(fr),
                "flip": rsc.bootstrap_rate_ci(rsc._flips(flip, admitted)),
                "median_dlp": med(dlp)}

    out = {
        "n_items": len(admitted), "n_admitted": int(sum(admitted)),
        "capability_drop_median": float(np.median(
            [c - f for c, f, a in zip(clean_lp, filler_lp, admitted) if a])) if any(admitted) else None,
        "clean_lp_median": float(np.median([c for c, a in zip(clean_lp, admitted) if a])) if any(admitted) else None,
        "split_noop_max": max(cr.split_noop_max for cr in runners),
        "split_noop_token_max": max(cr.split_noop_token_max for cr in runners),
        "suffix_mode": suffix_mode,
        "whole_path": {
            "attn_all": {"median_dlp": med(attn_all_dlp), "flip": flip_rate(attn_all_flip)},
            "ssm_all": {"median_dlp": med(ssm_all_dlp), "flip": flip_rate(ssm_all_flip)},
            "both_all": {"median_dlp": med(both_all_dlp), "flip": flip_rate(both_all_flip)},
        },
        "necessity": {"attn": {}, "ssm": {}, "attn_half": {}, "ssm_half": {}},
        "write": {"attn": {}, "ssm": {}},
    }

    # ---- single-layer necessity (attn normalized by attn_all; ssm by ssm_all) ----
    for L in range(n):
        d, f = collect_nec("attn", [L])
        out["necessity"]["attn"][f"L{L}"] = frac_stats(d, attn_all_dlp, f)
        d, f = collect_nec("ssm", [L])
        out["necessity"]["ssm"][f"L{L}"] = frac_stats(d, ssm_all_dlp, f)
        if torch.cuda.is_available() and L % 6 == 0:
            torch.cuda.empty_cache()
    for name, idxs in (("first", first), ("second", second)):
        d, f = collect_nec("attn", idxs)
        out["necessity"]["attn_half"][name] = frac_stats(d, attn_all_dlp, f)
        d, f = collect_nec("ssm", idxs)
        out["necessity"]["ssm_half"][name] = frac_stats(d, ssm_all_dlp, f)

    # ---- write sufficiency ----
    noop_attn = collect_write("attn", [0], source="filler")
    noop_ssm = collect_write("ssm", [0], source="filler")
    out["gates"] = {
        "attn_write_noop_max": float(np.max(np.abs(noop_attn))) if noop_attn else None,
        "ssm_write_noop_max": float(np.max(np.abs(noop_ssm))) if noop_ssm else None,
    }

    def ng_stats(gain):
        return rsc.bootstrap_median_ci(rsc._norm_gain(gain, clean_lp, filler_lp, admitted))

    for L in range(n):
        out["write"]["attn"][f"L{L}"] = ng_stats(collect_write("attn", [L]))
        out["write"]["ssm"][f"L{L}"] = ng_stats(collect_write("ssm", [L]))
    out["write"]["attn_all"] = ng_stats(collect_write("attn", allL))
    out["write"]["ssm_all"] = ng_stats(collect_write("ssm", allL))
    # both-all write
    both_gain = []
    for cr in runners:
        B = len(cr.subjects)
        filler_batch = cr.filler_input.repeat(B, 1)
        cache = cr._new_cache()
        cr.model(input_ids=filler_batch[:, : cr.subj_pos + 1], use_cache=True,
                 past_key_values=cache)
        cr._patch_attn(cache, cr.clean_store, allL, B)
        cr._patch_ssm(cache, cr.clean_store, allL, B)
        last = cr._replay_suffix_on(cache, filler_batch, B)
        lp = rsc.answer_logprobs(last, cr.answer_ids)
        both_gain.extend(float(x) for x in (lp - cr.filler_lp).detach().cpu().numpy())
    out["write"]["both_all"] = ng_stats(both_gain)

    # ---- window necessity (attention path, E19) ----
    if do_windows:
        out["windows_attn"] = {}
        for w in WINDOW_WIDTHS:
            if w >= n:
                continue
            per = {}
            for s0 in range(0, n - w + 1):
                win = list(range(s0, s0 + w))
                comp = [L for L in range(n) if L not in win]
                dw, fw = collect_nec("attn", win)
                dc, fc = collect_nec("attn", comp)
                per[f"L{s0}-{s0 + w - 1}"] = {
                    "window": frac_stats(dw, attn_all_dlp, fw),
                    "complement": frac_stats(dc, attn_all_dlp, fc)}
            best = max(per.items(),
                       key=lambda kv: (kv[1]["window"]["fraction"]["median"]
                                       if kv[1]["window"]["fraction"]["median"] is not None else -1e18))
            out["windows_attn"][f"w{w}"] = {"per_window": per, "best_window": best[0],
                                            "best": best[1]}
            log(f"  attn w={w}: best {best[0]} frac "
                f"{best[1]['window']['fraction']['median']:.3f} comp "
                f"{best[1]['complement']['fraction']['median']:.3f}")

    # ---- derived verdict helpers ----
    def best_layer(arm, key):
        items = [(L, arm[f"L{L}"]["fraction"]["median"]) for L in range(n)] if key == "frac" \
            else [(L, arm[f"L{L}"]["median"]) for L in range(n)]
        items = [(L, v) for L, v in items if v is not None]
        if not items:
            return None, None
        L, v = max(items, key=lambda t: t[1])
        return L, v

    aL, aV = best_layer(out["necessity"]["attn"], "frac")
    sL, sV = best_layer(out["necessity"]["ssm"], "frac")
    awL, awV = best_layer(out["write"]["attn"], "ng")
    swL, swV = best_layer(out["write"]["ssm"], "ng")
    out["summary_verdict"] = {
        "best_attn_necessity": {"layer": aL, "share": aV, "rel_depth": (aL / n) if aL is not None else None},
        "best_ssm_necessity": {"layer": sL, "share": sV, "rel_depth": (sL / n) if sL is not None else None},
        "best_attn_write": {"layer": awL, "s_norm": awV, "rel_depth": (awL / n) if awL is not None else None},
        "best_ssm_write": {"layer": swL, "s_norm": swV, "rel_depth": (swL / n) if swL is not None else None},
        "attn_ssm_write_same_layer": (awL == swL) if (awL is not None and swL is not None) else None,
    }
    return out


def resolve_model_path(payload):
    p = payload.get("model_path")
    if p and os.path.isdir(p) and os.path.exists(os.path.join(p, "config.json")):
        return p
    raise RuntimeError(f"model_path not found or missing config.json: {p}")


def main() -> int:
    t0 = time.time()
    req = json.loads(Path(os.environ.get("SATURN_DEBUG_REQUEST",
                                         "saturn_debug_request.json")).read_text())
    payload = req.get("payload") or {}
    smoke = bool(payload.get("smoke", False))
    do_windows = bool(payload.get("windows", True))
    window_behaviors = payload.get("window_behaviors")  # None => all
    suffix_mode = str(payload.get("suffix_mode", "chunk"))  # "chunk" fast / "token" exact
    max_contexts = payload.get("max_contexts")  # cap contexts/behavior to fit ~10 min
    device = "cuda"
    dtype = torch.float32
    torch.manual_seed(0)
    np.random.seed(0)
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False

    logs = []

    def log(msg):
        line = f"[{time.strftime('%H:%M:%S')}] {msg}"
        print(line, flush=True)
        logs.append(line)

    path = resolve_model_path(payload)
    from transformers import AutoModelForCausalLM, AutoTokenizer
    import transformers
    tok = AutoTokenizer.from_pretrained(path, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(
        path, dtype=dtype, attn_implementation="eager", local_files_only=True)
    model.to(device)
    model.eval()
    model.requires_grad_(False)
    layers = list(model.model.layers)
    n_layers = len(layers)
    log(f"loaded {type(model).__name__} n_layers={n_layers} hidden={model.config.hidden_size} "
        f"transformers={transformers.__version__} path={path} smoke={smoke}")

    # cache-attribute introspection (verify the data we expect before the arms)
    if device.startswith("cuda"):
        torch.cuda.reset_peak_memory_stats()
    from transformers.cache_utils import DynamicCache
    probe = DynamicCache(config=model.config)
    ids = tok("A photorealistic fox sitting in a forest. The animal", return_tensors="pt").input_ids.to(device)
    with torch.no_grad():
        model(input_ids=ids, use_cache=True, past_key_values=probe)
    l0 = probe.layers[0]
    introspect = {"layer0_class": type(l0).__name__,
                  "layer0_attrs": sorted([a for a in dir(l0) if not a.startswith("__")])[:70]}
    for key, fn in (
        ("keys_shape", lambda: list(l0.keys.shape)),
        ("values_shape", lambda: list(l0.values.shape)),
        ("conv_shape", lambda: list(l0.conv_states[0].shape)),
        ("rec_shape", lambda: list(l0.recurrent_states[0].shape)),
        ("has_previous_state_L0", lambda: bool(probe.has_previous_state(0))),
    ):
        try:
            introspect[key] = fn()
        except Exception as exc:  # never let introspection crash the worker
            introspect[key] = f"ERR {type(exc).__name__}: {exc}"
    log(f"cache introspect: class={introspect['layer0_class']} keys={introspect.get('keys_shape')} "
        f"values={introspect.get('values_shape')} conv={introspect.get('conv_shape')} "
        f"rec={introspect.get('rec_shape')} has_prev_L0={introspect.get('has_previous_state_L0')}")

    behaviors = rsc.build_items(smoke)
    out = {"schema": "saturn-e14-hybrid-v1", "model": "Falcon-H1-0.5B-Base",
           "model_path": path, "n_layers": n_layers, "smoke": smoke,
           "suffix_mode": suffix_mode, "max_contexts": max_contexts,
           "introspect": introspect, "summary": {}}
    for bname, beh in behaviors.items():
        t1 = time.time()
        if max_contexts:
            beh = dict(beh); beh["contexts"] = beh["contexts"][: int(max_contexts)]
        log(f"behavior {bname} ({len(beh['contexts'])} contexts)")
        cand = [tok.encode(" " + s, add_special_tokens=False)[0] for s in beh["candidates"]]
        dw = do_windows and (window_behaviors is None or bname in window_behaviors)
        out["summary"][bname] = run_behavior(model, tok, device, dtype, beh, cand,
                                             layers, log, do_windows=dw,
                                             suffix_mode=suffix_mode)
        log(f"  behavior {bname} done in {time.time() - t1:.1f}s")

    if device.startswith("cuda"):
        out["peak_vram_mb"] = round(torch.cuda.max_memory_allocated() / 1024**2, 1)
    try:
        import resource
        out["peak_rss_mb"] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0, 1)
    except Exception:
        pass
    out["elapsed_s"] = round(time.time() - t0, 2)
    out["env"] = {"torch": torch.__version__, "transformers": transformers.__version__,
                  "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None}
    print(MARKER + base64.b64encode(gzip.compress(json.dumps(out).encode())).decode(), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
