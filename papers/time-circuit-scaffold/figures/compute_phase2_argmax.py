#!/usr/bin/env python3
"""Compute the six Phase-2 frozen-FAL-3 S1 statistics (SD across admitted facts of the
per-item argmax layer of the residual-write curve, ddof=0) from the per-item reports, and
write them to phase2_argmax_sd.json beside this script so make_fig5.py reads them instead of
hardcoding. Single process, no GPU. Frozen definition: FROZEN.json `sd_argmax_write`."""
import os, json
import numpy as np

RES = os.path.expanduser("~/domains/saturn/experiments/2026-10-02-site-variance-decomposition/results")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "phase2_argmax_sd.json")
JOBS = {"qwen15": "peritem-job-9a3d0b5139ec", "gemma2": "peritem-job-06001771bc33"}
OPS = ["identity", "color", "shape"]

out = {"schema": "phase2-argmax-sd-v1", "ddof": 0,
       "definition": "SD across admitted facts of argmax_layer(resid_write), per (model, op)",
       "source_reports": JOBS, "models": {}}
for model, job in JOBS.items():
    rep = json.load(open(os.path.join(RES, job, "report.json")))
    by_op = {op: [] for op in OPS}
    for it in rep["items"]:
        if not it.get("admitted"):
            continue
        op = it["operation"]
        if op not in by_op:
            continue
        rw = it["resid_write"]
        argmax_layer = max(rw.items(), key=lambda kv: kv[1])[0]
        by_op[op].append(int(argmax_layer))
    out["models"][model] = {
        op: {"n": len(v), "S1_argmax_write_sd": float(np.std(v, ddof=0)),
             "median_argmax_layer": float(np.median(v))}
        for op, v in by_op.items()
    }

json.dump(out, open(OUT, "w"), indent=2)
print("wrote", OUT)
for m, d in out["models"].items():
    for op, s in d.items():
        print(f"  {m:7s} {op:9s} n={s['n']:3d}  S1={s['S1_argmax_write_sd']:.2f}  med={s['median_argmax_layer']:.0f}")
