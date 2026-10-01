"""Read-only, stdlib audit of selected paper receipts; no model or scheduler calls.

Run from any directory. Output is derived evidence, not a new experiment.
"""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[4]
PAPER = ROOT / "research/papers/space-and-time-circuits/paper.md"
SWEEPS = ROOT / "saturn/experiments/2026-09-30-full-layer-sweeps/results"

def read(path):
    return json.loads(path.read_text())

def fingerprint(path):
    return {"path": str(path.relative_to(ROOT)),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}

out = {"scope": "Selected receipt arithmetic and existing verifier checks; no fresh model reproduction",
       "paper": fingerprint(PAPER), "inputs": [], "writes": {}, "windows": {}, "cot": {}}
for model, job in [("qwen15", "qwen15-11f9ce05b1fd"),
                   ("gemma2", "gemma2-ed4ce1ac5974")]:
    path = SWEEPS / job / "report.json"
    out["inputs"].append(fingerprint(path))
    out["writes"][model] = {}
    for behavior, row in read(path)["summary"].items():
        single = row["kv_iso_suff_single"]
        out["writes"][model][behavior] = {
            "n": row["n_admitted"], "single_layer": single["best_layer"],
            "single": single["best"], "whole": row["kv_iso_suff_all"],
            "sum_of_layer_medians": sum(r["median"] for r in single["per_layer"].values()),
        }
for model, job in [("qwen15", "e19-qwen15-57ad67c21bd1"),
                   ("gemma2", "e19-gemma2-2f9593a800cd")]:
    path = SWEEPS / job / "report.json"
    out["inputs"].append(fingerprint(path))
    out["windows"][model] = {}
    for behavior, row in read(path)["summary"].items():
        out["windows"][model][behavior] = {
            "n": row["n_admitted"],
            "best_by_width": {k: {"location": v["best_window"], **v["best"]}
                              for k, v in row["windows"].items()}}
for name in ["full-5c53b6865f0f", "big15-f62de8e717a0"]:
    path = ROOT / "saturn/experiments/2026-10-01-e10-cot-intermediate-steps/results" / name / "report.json"
    out["inputs"].append(fingerprint(path))
    for model in read(path)["models"]:
        out["cot"][model["model_tag"]] = model["summary"]

# Counterexample to the assertion that the four-quadrant pattern excludes a
# diffuse linear representation. An order-invariant arithmetic mean has no
# temporal dynamics, yet passes the paper's quantitative single/whole bars.
n = 8
mean = lambda xs: sum(xs) / len(xs)
target, source = [1.0] * n, [0.0] * n
necessity = mean(target) - mean([0.0] + target[1:])
sufficiency = mean([1.0] + source[1:]) - mean(source)
out["linear_counterexample"] = {
    "consumer": "y = sum(x_i)/8; optional class decision y > 0.5",
    "single_necessity_share": necessity,
    "single_write": sufficiency,
    "whole_necessity_share": mean(target) - mean(source),
    "whole_write": mean(target) - mean(source),
    "passes_single_bars": necessity < 0.25 and sufficiency < 0.2,
    "temporal_order_relevant": False,
}

verifiers = [
    ROOT / "research/papers/space-and-time-circuits/evidence/ar-certificates/verify.py",
    ROOT / "research/bfl/artifacts/twenty-axis-semantic-route-circuit/verify.py",
]
out["verifiers"] = []
for path in verifiers:
    proc = subprocess.run([sys.executable, str(path)], capture_output=True, text=True)
    out["verifiers"].append({**fingerprint(path), "exit_code": proc.returncode,
                             "stdout": proc.stdout, "stderr": proc.stderr})
proc = subprocess.run([sys.executable,
    str(ROOT / "saturn/experiments/2026-09-30-space-and-time-circuits/run.py"),
    "canary", "all"], capture_output=True, text=True)
out["recorded_canaries"] = {
    "exit_code": proc.returncode,
    "pass_count": proc.stdout.count("[PASS]"),
    "unavailable_count": proc.stdout.count("[recorded check unavailable]"),
    "interpretation": "Checks already-collected values, not fresh model executions",
    "stderr": proc.stderr,
}
print(json.dumps(out, indent=2))
