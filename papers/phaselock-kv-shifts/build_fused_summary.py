"""Rebuild the PhaseLock-only fused prototype evidence extract."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np

PAPER = Path(__file__).resolve().parent
EXPERIMENT = PAPER.parents[2] / "saturn/experiments/2026-09-24-phaselock-integrated-ring"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    raw = EXPERIMENT / "results-fused-w1024-pilot-v4.json"
    probe = EXPERIMENT / "results-probe-w1024-physical-v4.json"
    receipt = EXPERIMENT / "results/job-5a4426fff103/receipt.json"
    x = json.loads(raw.read_text())
    p = json.loads(probe.read_text())
    r = json.loads(receipt.read_text())
    allowed = {"ring_integer", "ring_float64", "rerotate_bf16",
               "unfused_fp32", "fused_logical", "fused"}
    quality = {v["arm"]: v for v in x["quality_runs"] if v["arm"] in allowed}
    fp = quality["unfused_fp32"]
    fu = quality["fused"]
    split = x["sinks"] + x["window"]
    paired = {
        "fused_minus_unfused_fp32_mean_nll_steady": float(np.mean(
            (np.asarray(fu["nll"]) - np.asarray(fp["nll"]))[split:])),
        "fused_vs_unfused_fp32_top1_agreement_steady": float(np.mean(
            np.asarray(fu["top1"])[split:] == np.asarray(fp["top1"])[split:])),
    }
    out = {
        "schema": "phaselock-paper-fused-prototype-summary-v1",
        "job_id": r["job_id"],
        "model": x["model"], "model_revision": x["model_revision"],
        "input_sha256": x["input_sha256"],
        "tokens": x["tokens"], "sinks": x["sinks"], "window": x["window"],
        "post_fill_shifts": fu["n_shifts"],
        "quality": {name: {"steady_ppl": row["steady_ppl"],
                           "steady_nll": row["steady_nll"],
                           "top1_sha256": row["top1_sha256"]}
                    for name, row in quality.items()},
        "paired": paired,
        "decoder_speed_runs": [
            {"arm": row["arm"], "steady_tokens_per_s": row["steady_tokens_per_s"]}
            for row in x["speed_runs"] if row["arm"] in allowed
        ],
        "attention_probe_ms_per_call": {
            name: row["cuda_event_ms_per_call"]
            for name, row in p["attention_probe"]["times"].items()
        },
        "same_input_trace_max_abs_fused_vs_fp32": max(
            row["max_abs_fused_vs_fp32"] for row in x["same_input_trace"]),
        "raw_result_sha256": sha(raw),
        "attention_probe_result_sha256": sha(probe),
        "saturn_receipt_sha256": sha(receipt),
        "mrun_payload_sha256": r["payload_archive_sha256"],
        "limitations": [
            "Python decoder prototype, not a native production engine",
            "571 post-fill shifts and one WikiText train prefix",
            "FP32 unfused control materializes conversion buffers",
            "BF16 attention arms and FP32 attention arms have different numerical contracts",
        ],
    }
    dest = PAPER / "evidence/fused-prototype-summary.json"
    dest.write_text(json.dumps(out, indent=2) + "\n")
    print(dest)


if __name__ == "__main__":
    main()
