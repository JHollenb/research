"""Build compact, hash-bound evidence extracts for the paper's Section 6 from the
Saturn free-wins experiment (saturn/experiments/2026-09-29-phaselock-free-wins)."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np

EXP = Path(__file__).resolve().parents[3] / "saturn/experiments/2026-09-29-phaselock-free-wins"
RES = EXP / "results"
OUT = Path(__file__).parent / "evidence"
S, W = 4, 1024


def load(name):
    p = RES / f"{name}.json"
    return json.loads(p.read_text()), hashlib.sha256(p.read_bytes()).hexdigest()


def block_boot(d, block=1024, reps=4000, seed=0):
    nb = len(d) // block
    means = d[:nb * block].reshape(nb, block).mean(1)
    boots = np.random.default_rng(seed).choice(means, size=(reps, nb)).mean(1)
    return {"mean": float(d.mean()), "ci95": [float(np.quantile(boots, .025)), float(np.quantile(boots, .975))],
            "blocks_positive": int((means > 0).sum()), "blocks": nb}


def quality():
    out = {"schema": "phaselock-free-wins-quality-v1", "sources": {}, "arms": {}, "pairs": []}
    runs = {}
    for name in ("quality-test20k-v1", "quality-test20k-q4-v1", "quality-test20k-v2"):
        x, h = load(name)
        out["sources"][name] = {"sha256": h, "status": x["status"], "input_sha256": x.get("input_sha256"),
                                "source_sha256": x["source_sha256"]}
        for r in x["runs"]:
            runs.setdefault(r["arm"], r)
        if "calibration_stats" in x:
            out["calibration_stats"] = x["calibration_stats"]
    ref = np.array(runs["pristine"]["nll"])[S + W:]
    rt = np.array(runs["pristine"]["top1"])[S + W:]
    for a, r in runs.items():
        n = np.array(r["nll"])[S + W:]
        out["arms"][a] = {"ppl_steady": r["ppl_steady"], "excess_nll_vs_pristine": float((n - ref).mean()),
                          "top1_agree_vs_pristine": float((np.array(r["top1"])[S + W:] == rt).mean()),
                          "spec": r.get("spec"), "dirty_rows_since_snapshot": r.get("dirty_rows_since_snapshot")}
    for a, b in [("ring_int32", "pristine"), ("ring_int32", "rerotate_fp32"), ("ring_int32", "old_ring_integer"),
                 ("ring_int32_eagerattn", "old_ring_integer"), ("ring_int32", "ring_fp64"),
                 ("ring_int32_gqa", "ring_int32"), ("fusedpre_bf16", "ringpre_int32"),
                 ("fusedpre_q4b", "ringpre_q4b"), ("fusedpre_bf16_tab", "fusedpre_bf16"),
                 ("fusedpre_q4b_tab", "fusedpre_q4b"), ("ringpre_q8b", "ring_q8post"),
                 ("ringpre_q4b", "ringpre_q4"), ("ringpre_q4c", "ringpre_q4b"),
                 ("ringpre_q4b_v4b", "ringpre_q4b_v4"), ("ringpre_q4c_v4b", "ringpre_q4b_v4b")]:
        if a in runs and b in runs:
            d = np.array(runs[a]["nll"])[S + W:] - np.array(runs[b]["nll"])[S + W:]
            out["pairs"].append({"a": a, "b": b, **block_boot(d)})
    return out


def offsets():
    out = {"schema": "phaselock-free-wins-offset-v1", "sources": {}, "rows": []}
    for name in ("offset-test4k-v1", "offset-fine-v1"):
        x, h = load(name)
        out["sources"][name] = {"sha256": h, "input_sha256": x["input_sha256"]}
        ref = np.array([r for r in x["runs"] if r["mode"] == "pristine"][0]["nll"])[S + W:]
        for r in x["runs"]:
            if r["mode"] != "ring":
                continue
            out["rows"].append({"source": name, "phase": r["phase"], "offset": r["offset"],
                                "ppl_steady": r["ppl_steady"],
                                "excess_nll_vs_pristine": float((np.array(r["nll"])[S + W:] - ref).mean())})
        out["pristine_ppl_" + name] = [r for r in x["runs"] if r["mode"] == "pristine"][0]["ppl_steady"]
    return out


def recall():
    out = {"schema": "phaselock-free-wins-recall-v1", "sources": {}, "per_script": [], "aggregate": {}}
    seen = set()
    for p in sorted(RES.glob("recall-*.json")):
        x = json.loads(p.read_text())
        if x.get("status") != "complete":
            continue
        out["sources"][p.stem] = {"sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
                                  "input_sha256": x["input_sha256"]}
        script = f"{x['args']['schedule']}-s{x['args']['script_seed']}"
        for r in x["runs"]:
            if (r["arm"], script) in seen:
                continue
            seen.add((r["arm"], script))
            ev = [q for q in r["probes"] if not q["in_window"]]
            ret = [q for q in r["probes"] if q["in_window"]]
            row = {"script": script, "arm": r["arm"], "source": p.stem,
                   "retained_correct": sum(q["open_correct"] for q in ret), "retained": len(ret),
                   "evicted_correct": sum(q["open_correct"] for q in ev), "evicted": len(ev),
                   "evicted_mean_target_logprob": float(np.mean([q["target_logprob"] for q in ev])),
                   "evicted_fact_page_layers": [q.get("fact_page_retrieved_layers") for q in ev]}
            out["per_script"].append(row)
            a = out["aggregate"].setdefault(r["arm"], {"scripts": 0, "retained": [0, 0], "evicted": [0, 0]})
            a["scripts"] += 1
            a["retained"][0] += row["retained_correct"]; a["retained"][1] += row["retained"]
            a["evicted"][0] += row["evicted_correct"]; a["evicted"][1] += row["evicted"]
    return out


def speed():
    out = {"schema": "phaselock-free-wins-speed-v1", "sources": {}, "decode": [], "kernels": []}
    for name, key in (("speed-v1", "decode"), ("speed-v2", "decode"), ("attnbench-v1", "kernels"),
                      ("attnbench-v2", "kernels")):
        p = RES / f"{name}.json"
        if not p.exists():
            continue
        x, h = load(name)
        out["sources"][name] = {"sha256": h, "status": x["status"], "gpu": x["gpu"]}
        for r in x["runs"]:
            out[key].append({"source": name, **{k: v for k, v in r.items() if k != "tokens_per_s_reps"}})
    return out


def main():
    for fname, fn in (("free-wins-quality.json", quality), ("free-wins-offset.json", offsets),
                      ("free-wins-recall.json", recall), ("free-wins-speed.json", speed)):
        (OUT / fname).write_text(json.dumps(fn(), indent=1) + "\n")
        print("wrote", OUT / fname)


if __name__ == "__main__":
    main()
