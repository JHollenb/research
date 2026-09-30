"""Build compact, hash-bound evidence extracts for the paper's §6.8–§6.10 from the
Saturn bit-hacks experiment (saturn/experiments/2026-09-30-phaselock-bithacks)."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np

EXP = Path(__file__).resolve().parents[3] / "saturn/experiments/2026-09-30-phaselock-bithacks"
RES = EXP / "results"
OUT = Path(__file__).parent / "evidence"
S, W = 4, 1024


def load(name):
    p = RES / f"{name}.json"
    return json.loads(p.read_text()), hashlib.sha256(p.read_bytes()).hexdigest()


def src(x, h):
    return {"sha256": h, "status": x["status"], "gpu": x.get("gpu"), "torch": x.get("torch"),
            "model": x.get("model"), "source_sha256": x.get("source_sha256")}


def block_boot(d, block=512, reps=4000, seed=0):
    nb = len(d) // block
    means = d[:nb * block].reshape(nb, block).mean(1)
    boots = np.random.default_rng(seed).choice(means, size=(reps, nb)).mean(1)
    return {"mean": float(d.mean()), "ci95": [float(np.quantile(boots, .025)), float(np.quantile(boots, .975))],
            "blocks": nb}


def speed():
    out = {"schema": "phaselock-bithacks-speed-v1", "sources": {}, "whole_model_ms_per_token": {},
           "one_layer_us_per_call": {}, "pristine_vs_ring": {}}
    x, h = load("speed-v3")
    out["sources"]["speed-v3"] = src(x, h)
    for r in x["runs"]:
        out["whole_model_ms_per_token"].setdefault(r["arm"], {})[r["window"]] = r["ms_per_token_median"]
    merged = []
    for name in ("attnbench-v2", "attnbench-128k"):
        x, h = load(name)
        out["sources"][name] = src(x, h)
        if name == "attnbench-128k":
            merged = [r for r in merged if r["window"] != 131072]
        merged += x["runs"]
    for r in merged:
        out["one_layer_us_per_call"].setdefault(r["kernel"], {})[r["window"]] = {
            "us": r["us_per_call_graphed"], "max_abs_err_vs_fp64_same_format": r["max_abs_err_vs_fp64_same_format"]}
    for name in sorted(p.stem for p in RES.glob("speedx-*.json")):
        x, h = load(name)
        if x["status"] != "complete":
            continue
        out["sources"][name] = {**src(x, h), "max_layers": x["args"].get("max_layers")}
        rows = {}
        for r in x["runs"]:
            rows.setdefault(r["arm"], {})[r["window"]] = r["ms_per_token_median"]
        out["pristine_vs_ring"][name] = rows
    return out


def quality():
    out = {"schema": "phaselock-bithacks-quality-v1", "sources": {}, "models": {}}
    for m in ("qwen25-1.5b", "qwen25-0.5b", "qwen3-0.6b"):
        x, h = load(f"quality-{m}")
        out["sources"][f"quality-{m}"] = src(x, h)
        R = {r["arm"]: r for r in x["runs"]}
        ref = np.array(R["pristine"]["nll"])[S + W:]
        arms = {a: {"ppl_steady": r["ppl_steady"], **block_boot(np.array(r["nll"])[S + W:] - ref)}
                for a, r in R.items()}
        pairs = []
        for a, b in [("pf_bf16", "pre_bf16"), ("pf_fp16", "pf_bf16"), ("pf_q4_f16", "pf_q4"),
                     ("pf_q4_f16_i8q", "pf_q4_f16"), ("pf_q4pc_f16", "pre_q4c"), ("pf_q4lut_f16", "pf_q4_f16"),
                     ("pf_vq8_f16", "pf_q4_f16"), ("pf_spf44_f16", "pf_q4_f16"), ("pf_spf35_f16", "pf_spf44_f16"),
                     ("pre_q4c", "pre_q4")]:
            if a in R and b in R:
                d = np.array(R[a]["nll"])[S + W:] - np.array(R[b]["nll"])[S + W:]
                pairs.append({"a": a, "b": b, **block_boot(d)})
        out["models"][m] = {"arms": arms, "pairs": pairs, "steady_tokens": int(len(ref))}
    return out


def qwen3():
    out = {"schema": "phaselock-bithacks-qwen3-v1", "sources": {}, "paper53": {}, "paper61": {}, "paper63": {},
           "diag": {}}
    for size in ("0.6b", "1.7b"):
        x, h = load(f"paper53-qwen3-{size}")
        out["sources"][f"paper53-qwen3-{size}"] = {"sha256": h, "status": x["status"], "input_sha256": x.get("input_sha256")}
        out["paper53"][size] = {"runs": [{k: r[k] for k in ("arm", "steady_ppl", "steady_nll", "n_shifts")}
                                         for r in x["quality_runs"]],
                                "pairs": x["quality_pairs"], "attention_probe_times": x["attention_probe"]["times"]}
        x, h = load(f"paper61-qwen3-{size}")
        out["sources"][f"paper61-qwen3-{size}"] = src(x, h)
        out["paper61"][size] = [{"arm": r["arm"], "ppl_steady": r["ppl_steady"],
                                 "tokens_per_s_contended": r["steady_tokens_per_s"]} for r in x["runs"]]
        x, h = load(f"paper63-qwen3-{size}")
        out["sources"][f"paper63-qwen3-{size}"] = src(x, h)
        out["paper63"][size] = [{"mode": r["mode"], "phase": r.get("phase"), "offset": r.get("offset"),
                                 "ppl_steady": r["ppl_steady"]} for r in x["runs"]]
    for m in ("qwen25-0.5b", "qwen25-1.5b", "qwen3-0.6b", "qwen3-1.7b"):
        x, h = load(f"diag-{m}")
        out["sources"][f"diag-{m}"] = src(x, h)
        out["diag"][m] = {
            "ablation_kl_mean": {a: v["mean"] for a, v in x["ablation_kl"].items()},
            "layers": [{"layer": L["layer"], "score_err_energy": L["A"]["score_err_energy"],
                        "pf_exact_rerep_frac_low64_pairs": L["A"]["pf_exact_rerep_frac_low64_pairs"],
                        "B": {k: v for k, v in L["B"].items()}} for L in x["layers"]]}
    return out


def main():
    OUT.mkdir(exist_ok=True)
    for name, fn in (("bithacks-speed", speed), ("bithacks-quality", quality), ("bithacks-qwen3", qwen3)):
        (OUT / f"{name}.json").write_text(json.dumps(fn(), indent=1) + "\n")
        print("wrote", OUT / f"{name}.json")


if __name__ == "__main__":
    main()
