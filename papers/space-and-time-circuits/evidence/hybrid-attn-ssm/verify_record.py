#!/usr/bin/env python3
"""Verify collected E14 record identity and coverage without executing a model.

This compares the report with its embedded log payload, checks source/receipt
hashes, and derives a compact summary. The report contains aggregates, not raw
item rows; this cannot independently recompute its bootstrap statistics.
"""
from __future__ import annotations

import base64
import gzip
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
JOB = HERE
REPORT_SHA256 = "914ee169683a7f751e2b3e1517c6b280ef2d7e3380083d3b13bd692e335a6121"
MARKER = "SATURN_E14_HYBRID_GZIP_B64="


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify() -> dict:
    report = json.loads((JOB / "report.json").read_text())
    receipt = json.loads((JOB / "run-receipt.json").read_text())
    execution = json.loads((JOB / "execution-record.json").read_text())
    problems = []

    def check(ok: bool, message: str) -> None:
        if not ok:
            problems.append(message)

    check(sha(JOB / "report.json") == REPORT_SHA256, "Pinned report hash differs")
    log_bytes = (JOB / "job-log.txt").read_bytes()
    check(hashlib.sha256(log_bytes).hexdigest() == receipt["log_sha256"],
          "Log hash differs from collection receipt")
    embedded = [json.loads(gzip.decompress(base64.b64decode(line[len(MARKER):])))
                for line in log_bytes.decode().splitlines() if line.startswith(MARKER)]
    check(len(embedded) == 1 and embedded[0] == report,
          "Collected report differs from embedded log report")
    check(receipt["job_id"] == execution["job_id"] == "job-5efb5697631c",
          "Job identity differs")
    check(receipt["mrun_state"] == execution["state"] == "succeeded"
          and receipt["mrun_ok"] and receipt["report_present"], "Completion record differs")
    check(receipt["mrun_result"] == execution["result"], "Scheduler results differ")
    config = execution["config"]
    source_checks = {
        "worker_hybrid.py": config["worker_sha256"],
        "PLAN.md": config["design_sha256"],
        **config["additional_worker_sha256"],
    }
    for filename, expected in source_checks.items():
        check(sha(HERE / filename) == expected, f"Source hash differs: {filename}")
    check(not report["smoke"] and report["n_layers"] == 36, "Not the full 36-layer sweep")
    check(config["device"] == "cuda-fp32" and config["needs"]["cuda"],
          "Execution device contract differs")
    check(report["suffix_mode"] == config["payload"]["suffix_mode"] == "chunk",
          "Suffix mode differs")
    check(report["max_contexts"] == config["payload"]["max_contexts"] == 2,
          "Context count differs")
    expected_layers = {f"L{i}" for i in range(36)}
    summary = {}
    for behavior, stats in report["summary"].items():
        n = stats["n_admitted"]
        cuts = {}
        for cut in ("attn", "ssm"):
            necessity = stats["necessity"][cut]
            writes = stats["write"][cut]
            check(set(necessity) == expected_layers and set(writes) == expected_layers,
                  f"Incomplete singleton sweep: {behavior}/{cut}")
            for layer in expected_layers:
                check(necessity[layer]["flip"]["n"] == n and writes[layer]["n"] == n,
                      f"Admitted count differs: {behavior}/{cut}/{layer}")
            best_n = max(necessity, key=lambda layer: necessity[layer]["fraction"]["median"])
            best_w = max(writes, key=lambda layer: writes[layer]["median"])
            abs_n = max(necessity, key=lambda layer: abs(necessity[layer]["fraction"]["median"]))
            abs_w = max(writes, key=lambda layer: abs(writes[layer]["median"]))
            sv = stats["summary_verdict"]
            check(sv[f"best_{cut}_necessity"]["layer"] == int(best_n[1:])
                  and sv[f"best_{cut}_necessity"]["share"] == necessity[best_n]["fraction"]["median"],
                  f"Necessity helper differs: {behavior}/{cut}")
            check(sv[f"best_{cut}_write"]["layer"] == int(best_w[1:])
                  and sv[f"best_{cut}_write"]["s_norm"] == writes[best_w]["median"],
                  f"Write helper differs: {behavior}/{cut}")
            whole = stats["whole_path"][f"{cut}_all"]
            cuts[cut] = {
                "whole_necessity": whole,
                "whole_write": stats["write"][f"{cut}_all"],
                "best_positive_necessity": {"layer": best_n, **necessity[best_n]},
                "best_positive_write": {"layer": best_w, **writes[best_w]},
                "largest_absolute_necessity": {"layer": abs_n, **necessity[abs_n]},
                "largest_absolute_write": {"layer": abs_w, **writes[abs_w]},
                "maximum_singleton_flip_rate": max(v["flip"]["rate"] for v in necessity.values()),
            }
        windows = {}
        for width, data in stats.get("windows_attn", {}).items():
            w = int(width[1:])
            expected_windows = {f"L{i}-{i+w-1}" for i in range(36-w+1)}
            check(set(data["per_window"]) == expected_windows, f"Incomplete windows: {width}")
            best = max(data["per_window"],
                       key=lambda key: data["per_window"][key]["window"]["fraction"]["median"])
            check(best == data["best_window"] and data["best"] == data["per_window"][best],
                  f"Window helper differs: {width}")
            windows[width] = {"best_window": best, "best": data["best"]}
        summary[behavior] = {
            "n_items": stats["n_items"], "n_admitted": n,
            "capability_drop_median": stats["capability_drop_median"],
            "split_noop_max": stats["split_noop_max"],
            "split_noop_token_max": stats["split_noop_token_max"],
            "write_noops": stats["gates"], "cuts": cuts, "windows_attn": windows,
            "both_all_necessity": stats["whole_path"]["both_all"],
            "both_all_write": stats["write"]["both_all"],
        }
    check(set(summary) == {"identity", "color"}, "Behavior coverage differs")
    return {
        "schema": "e14-record-audit-v1", "job_id": execution["job_id"],
        "scope": "Existing collected aggregates, log payload, scheduler record and source hashes; no model execution.",
        "report_sha256": sha(JOB / "report.json"),
        "execution_record_sha256": sha(JOB / "execution-record.json"),
        "sources": source_checks,
        "mechanics_status": "record-consistent" if not problems else "record-inconsistent",
        "instrument_status": "aggregate-only-no-item-rows",
        "terminal_status": "No new four-quadrant certificate established by this audit.",
        "problems": problems, "summary": summary,
    }


if __name__ == "__main__":
    result = verify()
    print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))
    raise SystemExit(0 if not result["problems"] else 1)
