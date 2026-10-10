"""E3 worker (CUDA host, via mrun): pooling-scaffold and commit-layer test for Qwen3 caption embeddings.

Claims under test (response.md, Claims A and B, predictions frozen in PREREG.md before the job):
  A  Their generative pooling (thinking on, 128 greedy tokens, mean of last-layer states that produce the tokens)
     averages mostly over a caption-independent <think> preamble. That scaffold dilutes CKA with the image space.
     Removing it (thinking off, post-</think> positions only, or position-wise centering) raises clipped CKA.
  B  The last layer is not the best layer: the formed content is committed at ~0.7-0.9 depth, and later layers
     add next-token readout directions that act as scaffold. A layer sweep peaks before the final layer.

One model load. Phase 1 is a smoke gate on 64 items (determinism, capture counts, finite values, CKA(x, x) = 1)
that aborts the job on failure; phase 2 runs the full config in the same process. The report goes to stdout as one
gzip+base64 line after MARKER; embeddings are written under --out on the host.

Replicates their pooling code (modalities/image_captions/{generative,encoders}.py at fdfad84) with HF transformers
instead of vLLM: the captured state at generation step k is the final-norm hidden state of the position whose
logits produce token k (prefill last position for k = 0), up to and including the step that emits EOS.
"""

from __future__ import annotations

import argparse
import base64
import gzip
import json
import time
from pathlib import Path

import torch
from torch.nn.functional import normalize

from their_geometry import clipped_cka  # their unpaired_rosetta/geometry.py, vendored verbatim (MIT)

MARKER = "UNPAIRED_ROSETTA_E3_REPORT_GZIP_B64="
GENERATION_PROMPT = "Imagine what it would look like to see: {}"  # their generative.py
SLICE = 1024  # their token_pooling.py SLICE_SIZE


def log(*parts) -> None:
    print(time.strftime("%H:%M:%S"), *parts, flush=True)


def layer_indices(num_layers: int, fractions: list[float]) -> list[int]:
    """hidden_states index for each depth fraction; index num_layers is the final (normed) output."""
    return sorted({max(1, min(num_layers, round(f * num_layers))) for f in fractions})


class Pooler:
    """Generation + capture + online pooled sums for every (layer, position set)."""

    def __init__(self, model, tokenizer, layers: list[int], max_new_tokens: int) -> None:
        self.model, self.tokenizer, self.layers, self.max_new = model, tokenizer, layers, max_new_tokens
        self.store_layers = sorted(layers)[-2:]  # per-state copies for the leave-one-out arm (Amendment 2)
        self.think_end = tokenizer.convert_tokens_to_ids("</think>")
        configured = model.generation_config.eos_token_id
        configured = configured if isinstance(configured, list) else [configured]
        self.eos = {t for t in [*configured, tokenizer.eos_token_id, tokenizer.convert_tokens_to_ids("<|im_end|>")]
                    if t is not None}
        d = model.config.hidden_size
        # position-wise scaffold sums over the corpus, per layer: S[l][k] = sum_i h_{i,k}, C[k] = count
        self.position_sum = {l: torch.zeros(max_new_tokens, d, dtype=torch.float64) for l in layers}
        self.position_count = torch.zeros(max_new_tokens, dtype=torch.float64)
        # token-wise scaffold: corpus mean state per produced token id, per layer (rows allocated on first sight)
        self.token_row: dict[int, int] = {}
        self.token_sum = {l: torch.zeros(4096, d, dtype=torch.float32) for l in layers}
        self.token_count = torch.zeros(4096, dtype=torch.float64)

    @torch.inference_mode()
    def generate(self, captions: list[str], thinking: bool):
        chats = [
            self.tokenizer.apply_chat_template(
                [{"role": "user", "content": GENERATION_PROMPT.format(c)}],
                tokenize=False, add_generation_prompt=True, enable_thinking=thinking,
            )
            for c in captions
        ]
        inputs = self.tokenizer(chats, return_tensors="pt", padding=True).to(self.model.device)
        out = self.model.generate(
            **inputs, max_new_tokens=self.max_new, do_sample=False, temperature=None, top_p=None, top_k=None,
            output_hidden_states=True, return_dict_in_generate=True, pad_token_id=self.tokenizer.pad_token_id,
        )
        generated = out.sequences[:, inputs["input_ids"].shape[1]:].cpu()
        steps = len(out.hidden_states)
        b = len(captions)
        # alive[i, k]: step k is captured for item i (no EOS among tokens < k)
        alive = torch.ones(b, steps, dtype=torch.bool)
        for k in range(1, steps):
            emitted = torch.tensor([int(t) in self.eos for t in generated[:, k - 1]])
            alive[:, k] = alive[:, k - 1] & ~emitted
        # after_think[i, k]: token k is generated after </think> was emitted
        after_think = torch.zeros(b, steps, dtype=torch.bool)
        seen = torch.zeros(b, dtype=torch.bool)
        for k in range(steps):
            after_think[:, k] = seen
            seen = seen | (generated[:, k] == self.think_end)
        per_layer = {}
        for l in self.layers:
            states = [out.hidden_states[0][l][:, -1]] + [out.hidden_states[k][l][:, 0] for k in range(1, steps)]
            per_layer[l] = torch.stack(states, dim=1).float().cpu()  # [b, steps, d]
        return generated, alive, after_think, per_layer

    def pool(self, captions: list[str], thinking: bool, track_positions: bool):
        generated, alive, after_think, per_layer = self.generate(captions, thinking)
        result = {"lengths": alive.sum(1), "post_think_counts": (alive & after_think).sum(1),
                  "tokens": generated, "sum_all": {}, "sum_post": {},
                  "states": {l: per_layer[l].half() for l in self.store_layers}}
        for l, h in per_layer.items():
            mask_all = alive.unsqueeze(-1).float()
            mask_post = (alive & after_think).unsqueeze(-1).float()
            result["sum_all"][l] = (h * mask_all).sum(1).double()
            result["sum_post"][l] = (h * mask_post).sum(1).double()
            if track_positions:
                self.position_sum[l][: h.shape[1]] += (h * mask_all).sum(0).double()
        if track_positions:
            self.position_count[: alive.shape[1]] += alive.sum(0).double()
            rows = self.rows_for(generated[:, : alive.shape[1]])
            flat_rows, flat_alive = rows.flatten(), alive.flatten()
            for l, h in per_layer.items():
                self.token_sum[l].index_add_(0, flat_rows[flat_alive], h.flatten(0, 1)[flat_alive])
            self.token_count.index_add_(0, flat_rows[flat_alive], torch.ones(int(flat_alive.sum()), dtype=torch.float64))
        return result

    def rows_for(self, tokens: torch.Tensor) -> torch.Tensor:
        """Table rows for token ids, growing the tables when new ids appear."""
        for t in torch.unique(tokens).tolist():
            if t not in self.token_row:
                self.token_row[t] = len(self.token_row)
        needed = len(self.token_row)
        if needed > self.token_count.shape[0]:
            grow = max(needed, 2 * self.token_count.shape[0]) - self.token_count.shape[0]
            self.token_count = torch.cat([self.token_count, torch.zeros(grow, dtype=torch.float64)])
            for l in self.token_sum:
                self.token_sum[l] = torch.cat([self.token_sum[l], torch.zeros(grow, self.token_sum[l].shape[1])])
        return torch.tensor([[self.token_row[t] for t in row] for row in tokens.tolist()], dtype=torch.long)

    def token_centered_loo(self, states: torch.Tensor, tokens: torch.Tensor, lengths: torch.Tensor, layer: int,
                           min_count: int = 20):
        """Amendment 2: subtract the corpus mean of the produced token computed WITHOUT the item's own states,
        and only for tokens seen >= min_count times elsewhere (frequent = template-like). Returns the pooled
        embeddings and the share of captured positions that were centered."""
        total_sum = self.token_sum[layer].double()
        total_count = self.token_count
        out = torch.empty(states.shape[0], states.shape[2], dtype=torch.float64)
        centered_positions, all_positions = 0, 0
        for i in range(states.shape[0]):
            t_i = int(lengths[i])
            h = states[i, :t_i].double()
            rows = torch.tensor([self.token_row[t] for t in tokens[i, :t_i].tolist()], dtype=torch.long)
            uniq, inverse, own_counts = torch.unique(rows, return_inverse=True, return_counts=True)
            own_sum = torch.zeros(len(uniq), h.shape[1], dtype=torch.float64).index_add_(0, inverse, h)
            others = total_count[uniq] - own_counts.double()
            keep = others >= min_count
            mu = (total_sum[uniq] - own_sum) / others.clamp(min=1)[:, None]
            mu[~keep] = 0
            out[i] = (h.sum(0) - (mu * own_counts.double()[:, None]).sum(0)) / max(t_i, 1)
            centered_positions += int(own_counts[keep].sum())
            all_positions += t_i
        return out, centered_positions / max(all_positions, 1)

    def token_centered(self, total: torch.Tensor, tokens: torch.Tensor, lengths: torch.Tensor, layer: int):
        """(sum_k h_ik - sum_k mu[token_ik]) / T_i over each item's captured steps."""
        mu = (self.token_sum[layer].double() / self.token_count.clamp(min=1)[:, None])
        out = torch.empty_like(total)
        for i in range(total.shape[0]):
            ids = [self.token_row[t] for t in tokens[i, : int(lengths[i])].tolist()]
            out[i] = (total[i] - mu[ids].sum(0)) / max(int(lengths[i]), 1)
        return out


@torch.inference_mode()
def mean_pooling(model, tokenizer, captions: list[str], layers: list[int]) -> dict:
    """Their MeanPooling (encoders.py) plus two variants: caption tokens only, and without the first token."""
    chats = [tokenizer.apply_chat_template([{"role": "user", "content": c}], tokenize=False,
                                           add_generation_prompt=False, enable_thinking=True) for c in captions]
    inputs = tokenizer(chats, return_tensors="pt", padding=True).to(model.device)
    mask = inputs["attention_mask"]
    positions = (mask.long().cumsum(-1) - 1).masked_fill(mask == 0, 1)
    out = model(input_ids=inputs["input_ids"], attention_mask=mask, position_ids=positions,
                output_hidden_states=True, use_cache=False, logits_to_keep=1)
    # caption span: tokens of the caption itself inside each chat (left padding; same template for every item)
    caption_mask = torch.zeros_like(mask)
    for i, c in enumerate(captions):
        ids = tokenizer(c, add_special_tokens=False)["input_ids"]
        row = inputs["input_ids"][i].tolist()
        for start in range(len(row) - len(ids), -1, -1):
            if row[start:start + len(ids)] == ids:
                caption_mask[i, start:start + len(ids)] = 1
                break
    first_real = mask.float().argmax(dim=1)
    no_first = mask.clone()
    no_first[torch.arange(len(captions)), first_real] = 0
    pooled = {}
    for l in layers:
        h = out.hidden_states[l].float()
        for name, m in (("mean_all", mask), ("mean_caption", caption_mask), ("mean_no_first", no_first)):
            w = m.unsqueeze(-1).float()
            pooled[(name, l)] = ((h * w).sum(1) / w.sum(1).clamp(min=1)).cpu()
    return pooled, int((caption_mask.sum(1) == 0).sum())


def slice_cka(vision: torch.Tensor, language: torch.Tensor) -> dict:
    """Their protocol: clipped CKA per slice of 1024 items (their reduce_texts unit-normalizes first)."""
    language = normalize(language.float(), dim=-1)
    size = min(SLICE, vision.shape[0])  # fewer than 1024 items only in local wiring tests
    values = [clipped_cka(vision[s:s + size].float(), language[s:s + size])
              for s in range(0, vision.shape[0] - size + 1, size)]
    return {"mean": sum(values) / len(values), "slices": values}


def scaffold_share(tokens: torch.Tensor, lengths: torch.Tensor) -> list[float]:
    """Per generated position k: share of items whose token equals the corpus-modal token at k."""
    shares = []
    for k in range(tokens.shape[1]):
        live = lengths > k
        if live.sum() < 8:
            break
        column = tokens[live, k]
        shares.append(float((column == column.mode().values).float().mean()))
    return shares


def run_corpus(name, captions, refs, model, tokenizer, layers, args, smoke=False) -> dict:
    n = len(captions)
    report = {"num_items": n}
    for thinking in args.thinking:
        pooler = Pooler(model, tokenizer, layers, args.max_new_tokens)
        sums_all = {l: [] for l in layers}
        sums_post = {l: [] for l in layers}
        lengths, post_counts, tokens = [], [], []
        stored = {l: [] for l in pooler.store_layers}
        for start in range(0, n, args.batch):
            batch = captions[start:start + args.batch]
            r = pooler.pool(batch, thinking, track_positions=True)
            for l in pooler.store_layers:
                padded = torch.zeros(len(batch), args.max_new_tokens, r["states"][l].shape[2], dtype=torch.float16)
                padded[:, : r["states"][l].shape[1]] = r["states"][l]
                stored[l].append(padded)
            for l in layers:
                sums_all[l].append(r["sum_all"][l])
                sums_post[l].append(r["sum_post"][l])
            lengths.append(r["lengths"])
            post_counts.append(r["post_think_counts"])
            pad = torch.full((len(batch), args.max_new_tokens), -1, dtype=torch.long)
            pad[:, : r["tokens"].shape[1]] = r["tokens"]
            tokens.append(pad)
            if start % (args.batch * 8) == 0:
                log(name, "thinking" if thinking else "no-thinking", start + len(batch), "/", n)
        lengths, post_counts, tokens = torch.cat(lengths), torch.cat(post_counts), torch.cat(tokens)
        mode = "think" if thinking else "nothink"
        mu_prefix = {}
        counts = pooler.position_count.clamp(min=1)
        for l in layers:
            mu = pooler.position_sum[l] / counts[:, None]
            mu_prefix[l] = torch.cat([torch.zeros(1, mu.shape[1], dtype=mu.dtype), mu.cumsum(0)])
        for l in layers:
            total = torch.cat(sums_all[l])
            post = torch.cat(sums_post[l])
            gen_all = total / lengths.clamp(min=1)[:, None]
            centered = (total - mu_prefix[l][lengths]) / lengths.clamp(min=1)[:, None]
            has_post = post_counts > 0
            gen_post = torch.where(has_post[:, None], post / post_counts.clamp(min=1)[:, None], gen_all)
            tokcentered = pooler.token_centered(total, tokens, lengths, l)
            variants = [("gen_all", gen_all), ("gen_poscentered", centered),
                        ("gen_tokcentered", tokcentered), ("gen_post_think", gen_post)]
            if l in pooler.store_layers:
                loo, share = pooler.token_centered_loo(torch.cat(stored[l]), tokens, lengths, l)
                variants.append(("gen_tokcentered_loo20", loo))
                report[f"{mode}/loo20_centered_position_share/L{l}"] = share
            for variant, emb in variants:
                report[f"{mode}/{variant}/L{l}"] = slice_cka(refs["vision"], emb) if not smoke else {
                    "finite": bool(torch.isfinite(emb).all())}
            if not smoke and l == max(layers) and args.save_dir:
                torch.save({"gen_all": gen_all.half(), "gen_poscentered": centered.half(),
                            "gen_tokcentered": tokcentered.half(),
                            "gen_post_think": gen_post.half(), "lengths": lengths, "post_counts": post_counts},
                           Path(args.save_dir) / f"{name}-{mode}-L{l}.pt")
        report[f"{mode}/diagnostics"] = {
            "mean_generated_positions": float(lengths.float().mean()),
            "share_reaching_post_think": float((post_counts > 0).float().mean()),
            "mean_post_think_positions": float(post_counts.float().mean()),
            "scaffold_token_share_by_position": scaffold_share(tokens, lengths)[:128],
            "examples": [tokenizer.decode([t for t in tokens[i].tolist() if t >= 0]) for i in range(min(6, n))],
        }
    pooled, no_span = {}, 0
    for start in range(0, n, args.batch):
        p, missing = mean_pooling(model, tokenizer, captions[start:start + args.batch], layers)
        no_span += missing
        for key, value in p.items():
            pooled.setdefault(key, []).append(value)
    for (variant, l), parts in pooled.items():
        emb = torch.cat(parts)
        report[f"mean/{variant}/L{l}"] = slice_cka(refs["vision"], emb) if not smoke else {
            "finite": bool(torch.isfinite(emb).all())}
    report["mean/caption_span_not_found"] = no_span
    if not smoke:
        report["reference/mpnet_stored"] = slice_cka(refs["vision"], refs["mpnet"])
    return report


def smoke_gate(model, tokenizer, layers, args, captions) -> dict:
    pooler = Pooler(model, tokenizer, layers, args.max_new_tokens)
    a = pooler.pool(captions[:8], True, False)
    b = pooler.pool(captions[:8], True, False)
    checks = {
        "deterministic_tokens": bool(torch.equal(a["tokens"], b["tokens"])),
        "deterministic_states": all(torch.equal(a["sum_all"][l], b["sum_all"][l]) for l in layers),
        "captured_positions_le_budget": bool((a["lengths"] <= args.max_new_tokens).all()),
        "captured_positions_ge_1": bool((a["lengths"] >= 1).all()),
        "finite": all(bool(torch.isfinite(a["sum_all"][l]).all()) for l in layers),
    }
    x = torch.randn(64, 32, dtype=torch.float64)
    checks["cka_self_is_one"] = abs(clipped_cka(x, x) - 1.0) < 1e-9
    checks["example_think"] = tokenizer.decode(a["tokens"][0])[:300]
    return checks


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="Qwen/Qwen3-1.7B")
    parser.add_argument("--corpora", nargs="*", default=["coco_train2014", "StanfordParagraphCaptioning"])
    parser.add_argument("--items", type=int, default=2048)
    parser.add_argument("--batch", type=int, default=64)
    parser.add_argument("--long-batch", type=int, default=16,
                        help="batch for long-caption corpora (SPC): memory only; the 64-batch run hit 12.3 GB")
    parser.add_argument("--max-new-tokens", type=int, default=128)
    parser.add_argument("--thinking", type=lambda s: s == "on", nargs="*", default=[True, False])
    parser.add_argument("--depths", type=float, nargs="*", default=[0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
    parser.add_argument("--save-dir", default="")
    parser.add_argument("--data", type=Path, default=Path("payload"))
    parser.add_argument("--device", default="cuda")
    args = parser.parse_args()
    from transformers import AutoModelForCausalLM, AutoTokenizer

    started = time.time()
    tokenizer = AutoTokenizer.from_pretrained(args.model, padding_side="left")
    model = AutoModelForCausalLM.from_pretrained(args.model, dtype=torch.bfloat16).to(args.device).eval()
    layers = layer_indices(model.config.num_hidden_layers, args.depths)
    if args.save_dir:
        Path(args.save_dir).mkdir(parents=True, exist_ok=True)
    report = {"config": {**vars(args), "data": str(args.data), "layers": layers,
                         "num_hidden_layers": model.config.num_hidden_layers,
                         "torch": torch.__version__,
                         "device": torch.cuda.get_device_name(0) if args.device == "cuda" else args.device}}
    default_batch = args.batch
    first = json.loads((args.data / f"{args.corpora[0]}.json").read_text())
    report["smoke"] = smoke_gate(model, tokenizer, layers, args, first)
    log("smoke", report["smoke"])
    gate = [k for k, v in report["smoke"].items() if isinstance(v, bool) and not v]
    if gate:
        report["aborted"] = f"smoke gate failed: {gate}"
    else:
        for corpus in args.corpora:
            captions = json.loads((args.data / f"{corpus}.json").read_text())[: args.items]
            args.batch = args.long_batch if corpus == "StanfordParagraphCaptioning" else default_batch
            report.setdefault("batch_by_corpus", {})[corpus] = args.batch
            refs = torch.load(args.data / f"{corpus}.pt")
            refs = {k: v[: len(captions)] for k, v in refs.items()}
            report[corpus] = run_corpus(corpus, captions, refs, model, tokenizer, layers, args)
            torch.cuda.empty_cache() if args.device == "cuda" else None
            log("done", corpus)
    report["wall_s"] = time.time() - started
    report["peak_vram_mb"] = torch.cuda.max_memory_allocated() / 2**20 if args.device == "cuda" else None
    print(MARKER + base64.b64encode(gzip.compress(json.dumps(report).encode())).decode(), flush=True)
    if "aborted" in report:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
