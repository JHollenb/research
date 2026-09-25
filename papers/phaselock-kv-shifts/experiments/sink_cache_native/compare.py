"""Paired native SinkCache comparison using one frozen HF model on beast.

The payload contains exact upstream baseline and patched ``generate.py`` files.
Both cache objects receive the same one-token teacher-forced WikiText stream in
the same process. No model layers or attention implementation are replaced.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import os
import time
from pathlib import Path

import pyarrow.parquet as pq
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_cache(path: Path, name: str, capacity: int, sinks: int, position_mode: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    cache = module.SinkCache(window_length=capacity, num_sink_tokens=sinks)
    trace = {
        "update_calls": 0, "trig_delivery_calls": 0, "shift_calls": 0, "evictions": 0,
        "rerotation_calls": 0, "input_trig_dtype": None, "coefficient_dtype": None,
        "coefficient_norm_min": None, "coefficient_norm_max": None,
        "key_dtype": None, "position_contract_valid": True, "last_position": None,
    }
    original_update = cache.update
    original_get = cache._get_rerotation_cos_sin

    def traced_update(key_states, value_states, layer_idx, cache_kwargs=None):
        trace["update_calls"] += 1
        if cache_kwargs and cache_kwargs.get("cos") is not None and cache_kwargs.get("sin") is not None:
            trace["trig_delivery_calls"] += 1
        old_length = cache.get_seq_length(layer_idx) if layer_idx < len(cache.key_cache) else 0
        shifting = old_length + key_states.shape[-2] >= capacity and old_length > 0
        if shifting:
            trace["shift_calls"] += 1
            if layer_idx == 0:
                trace["evictions"] += 1
                position = cache_kwargs.get("cache_position") if cache_kwargs else None
                actual = int(position.item()) if position is not None and position.numel() == 1 else None
                expected = (capacity - 1 if position_mode == "bounded_local_slot" else
                            capacity if trace["last_position"] is None else trace["last_position"] + 1)
                trace["position_contract_valid"] &= actual == expected
                trace["last_position"] = actual
        result = original_update(key_states, value_states, layer_idx, cache_kwargs)
        if layer_idx == 0:
            trace["key_dtype"] = str(cache.key_cache[0].dtype)
        return result

    def traced(*args):
        cos, sin = original_get(*args)
        trace["rerotation_calls"] += 1
        if trace["coefficient_dtype"] is None:
            norm = torch.sqrt(cos.float().square() + sin.float().square())
            trace["input_trig_dtype"] = str(args[1].dtype)
            trace["coefficient_dtype"] = str(cos.dtype)
            trace["coefficient_norm_min"] = float(norm.min().item())
            trace["coefficient_norm_max"] = float(norm.max().item())
        return cos, sin

    cache.update = traced_update
    cache._get_rerotation_cos_sin = traced
    return cache, trace


def stream_ids(tokenizer, dataset: Path, n_tokens: int) -> list[int]:
    text = "\n".join(
        value for value in pq.read_table(dataset, columns=["text"]).column("text").to_pylist()
        if value.strip()
    )
    prefix_chars = min(len(text), max(4096, n_tokens * 8))
    while True:
        ids = tokenizer(text[:prefix_chars], return_tensors="pt").input_ids[0].tolist()
        if len(ids) >= n_tokens or prefix_chars == len(text):
            if len(ids) < n_tokens:
                raise RuntimeError(f"dataset has only {len(ids)} tokens")
            return ids[:n_tokens]
        prefix_chars = min(len(text), prefix_chars * 2)


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, sort_keys=True, indent=2) + "\n")
    os.replace(temporary, path)


@torch.inference_mode()
def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--patched", type=Path, required=True)
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument("--tokens", type=int, default=2600)
    parser.add_argument("--window", type=int, default=1024)
    parser.add_argument("--sinks", type=int, default=4)
    parser.add_argument("--report-every", type=int, default=0)
    parser.add_argument("--position-mode", choices=("bounded_local_slot", "absolute_global"),
                        default="bounded_local_slot")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    capacity = args.sinks + args.window
    if args.tokens <= capacity + 1:
        raise ValueError("tokens must exceed the sink-plus-window cache capacity")
    report_every = args.report_every or args.window

    torch.manual_seed(0)
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    model = AutoModelForCausalLM.from_pretrained(
        args.model, torch_dtype=torch.bfloat16, attn_implementation="eager", local_files_only=True
    ).eval().to("cuda")
    tokenizer = AutoTokenizer.from_pretrained(args.model, local_files_only=True)
    ids = stream_ids(tokenizer, args.dataset, args.tokens)
    token_hash = hashlib.sha256(torch.tensor(ids, dtype=torch.int32).numpy().tobytes()).hexdigest()
    arms = {}
    for name, path in (("baseline", args.baseline), ("patched", args.patched)):
        arms[name] = load_cache(path, name + "_sink_cache", capacity, args.sinks, args.position_mode)

    result = {
        "status": "running", "model": str(args.model), "model_config_sha256": sha256(args.model / "config.json"),
        "dataset": str(args.dataset), "dataset_sha256": sha256(args.dataset),
        "token_ids_sha256": token_hash, "tokens_requested": args.tokens,
        "recent_window": args.window, "capacity": capacity, "sinks": args.sinks, "block": 1,
        "position_mode": args.position_mode,
        "position_rule": ("initial 0..capacity-1; after each eviction new token at capacity-1"
                          if args.position_mode == "bounded_local_slot" else
                          "initial 0..capacity-1; subsequent tokens use original absolute positions"),
        "dtype": "torch.bfloat16", "attention": "eager", "transformers": __import__("transformers").__version__,
        "torch": torch.__version__, "gpu": torch.cuda.get_device_name(0),
        "source_sha256": {name: sha256(path) for name, path in (("baseline", args.baseline), ("patched", args.patched))},
        "measurements": [],
    }
    write_json(args.out, result)
    print(json.dumps({"event": "start", "out": str(args.out), "meta": {k: v for k, v in result.items() if k != "measurements"}}), flush=True)

    nll_sums = {name: 0.0 for name in arms}
    steady_sums = {name: 0.0 for name in arms}
    block_sums = {name: 0.0 for name in arms}
    block_count = 0
    nll_counts = capacity
    steady_count = 0
    top1_equal = capacity
    t_start = time.monotonic()
    prefill_ids = torch.tensor([ids[:capacity]], dtype=torch.long, device="cuda")
    prefill_positions = torch.arange(capacity, dtype=torch.long, device="cuda")
    prefill_hashes = {}
    for name, (cache, trace) in arms.items():
        logits = model(
            input_ids=prefill_ids, position_ids=prefill_positions[None],
            past_key_values=cache, cache_position=prefill_positions, use_cache=True
        ).logits[0]
        prefill_hashes[name] = hashlib.sha256(logits.view(torch.uint16).cpu().numpy().tobytes()).hexdigest()
        targets = torch.tensor(ids[1:capacity + 1], dtype=torch.long, device="cuda")
        for start in range(0, capacity, 64):
            block = logits[start:start + 64].float()
            scores = torch.logsumexp(block, dim=-1) - block.gather(-1, targets[start:start + 64, None]).squeeze(-1)
            nll_sums[name] += float(scores.sum().item())
        if cache.get_seq_length() != capacity or trace["rerotation_calls"] != 0 or trace["evictions"] != 0:
            raise RuntimeError(f"{name}: initial prefill changed position or evicted")
        if trace["key_dtype"] != "torch.bfloat16":
            raise RuntimeError(f"{name}: native cache key dtype is {trace['key_dtype']}")
        del logits
    if prefill_hashes["baseline"] != prefill_hashes["patched"]:
        raise RuntimeError("baseline and patched native logits differ before rerotation")
    result["prefill_logit_sha256"] = prefill_hashes["baseline"]
    result["prefill_nll"] = nll_sums.copy()
    write_json(args.out, result)
    print(json.dumps({"event": "prefill", "capacity": capacity, "logit_sha256": prefill_hashes["baseline"]}), flush=True)

    local_position = torch.tensor([capacity - 1], dtype=torch.long, device="cuda")
    for t in range(capacity, args.tokens - 1):
        position = local_position if args.position_mode == "bounded_local_slot" else torch.tensor(
            [t], dtype=torch.long, device="cuda"
        )
        token = torch.tensor([[ids[t]]], dtype=torch.long, device="cuda")
        target = ids[t + 1]
        outputs = {}
        for name, (cache, _) in arms.items():
            logits = model(
                input_ids=token, position_ids=position[None],
                past_key_values=cache, cache_position=position, use_cache=True
            ).logits[0, -1].float()
            outputs[name] = logits
            nll = float((torch.logsumexp(logits, dim=0) - logits[target]).item())
            nll_sums[name] += nll
            steady_sums[name] += nll
            block_sums[name] += nll
        nll_counts += 1
        steady_count += 1
        block_count += 1
        delta = float((outputs["baseline"] - outputs["patched"]).abs().max().item())
        top1_equal += int(outputs["baseline"].argmax().item() == outputs["patched"].argmax().item())
        if block_count == report_every or t == args.tokens - 2:
            traces = {name: trace.copy() for name, (_, trace) in arms.items()}
            row = {
                "step": t + 1, "elapsed_s": round(time.monotonic() - t_start, 3),
                "ppl": {name: math.exp(nll_sums[name] / nll_counts) for name in arms},
                "steady_ppl": {name: math.exp(steady_sums[name] / steady_count) for name in arms}
                if steady_count else None,
                "block_ppl": {name: math.exp(block_sums[name] / block_count) for name in arms},
                "block_tokens": block_count,
                "top1_agreement": top1_equal / nll_counts,
                "pre_shift_logit_exact": True,
                "current_max_logit_delta": delta,
                "traces": traces,
            }
            result["measurements"].append(row)
            write_json(args.out, result)
            print(json.dumps({"event": "progress", **row}), flush=True)
            block_sums = {name: 0.0 for name in arms}
            block_count = 0

    expected_evictions = args.tokens - 1 - capacity
    for name, (cache, trace) in arms.items():
        expected_rerotations = (0 if args.position_mode == "absolute_global" and name == "patched"
                                else trace["shift_calls"])
        if trace["evictions"] != expected_evictions or trace["rerotation_calls"] != expected_rerotations:
            raise RuntimeError(f"{name}: wrong evictions/rerotations: {trace}")
        if trace["trig_delivery_calls"] != trace["update_calls"] or not trace["position_contract_valid"]:
            raise RuntimeError(f"{name}: native RoPE or position was not delivered: {trace}")
        if cache.get_seq_length() != capacity or trace["key_dtype"] != "torch.bfloat16":
            raise RuntimeError(f"{name}: final cache shape or dtype changed: {trace}")
    if arms["baseline"][1]["coefficient_dtype"] != "torch.bfloat16":
        raise RuntimeError("upstream baseline did not use BF16 rerotation coefficients")
    if args.position_mode == "bounded_local_slot":
        if arms["patched"][1]["coefficient_dtype"] != "torch.float32":
            raise RuntimeError("patched cache did not use FP32 rerotation coefficients")
    elif arms["patched"][1]["coefficient_dtype"] is not None:
        raise RuntimeError("patched absolute-position cache unexpectedly rerotated keys")
    result["status"] = "succeeded"
    result["final"] = result["measurements"][-1]
    write_json(args.out, result)
    print(json.dumps({"event": "final", **result["final"]}), flush=True)


if __name__ == "__main__":
    main()
