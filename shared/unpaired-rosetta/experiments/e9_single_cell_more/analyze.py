"""Merge E9 shard receipts per pair (per-seed float records only), compute the authoritative cross-seed selection
stats, the LTA canary (PBMC), the type-test verdict, and a cross-pair table that folds in E8's CITE-seq receipts
(cited, not rerun). No real data is touched -- this reads the small JSON numbers the Beast jobs already produced.

    python -m e9_single_cell_more.analyze
"""

from __future__ import annotations

import json
from pathlib import Path

import torch

from e9_single_cell_more.run import spearman, type_verdict

OUT = Path(__file__).resolve().parents[1] / "results" / "e9_single_cell_more"
E8 = Path(__file__).resolve().parents[1] / "results" / "e8_single_cell" / "e8_merged_summary.json"
PAPER_SEEDS = 5  # the first 5 of the universe are derive_seeds(42,5), the paper's seeds


def load_arm(dataset_tag: str, remove_topk: int):
    by_seed, meta = {}, {}
    for path in sorted(OUT.glob(f"e9_{dataset_tag}_remove{remove_topk}_*.json")):
        r = json.load(open(path))
        for s in r["results"]["per_seed"]:
            by_seed[s["seed"]] = s
        meta = {"canary": r["results"]["canary"], "oracle": r["results"]["oracle"],
                "axis": r["results"].get("axis"), "type_verdict": r["results"].get("type_verdict"),
                "aligner": r["config"]["aligner"], "smoke": r["config"]["smoke"], "paper": r["config"].get("paper"),
                "config": {k: r["config"].get(k) for k in ("dataset", "d_x", "d_y", "model_x", "model_y")}}
    per_seed = [by_seed[k] for k in sorted(by_seed)]
    return per_seed, meta


def selection_stats(per_seed):
    seeds = [s["seed"] for s in per_seed]
    fos_last = [s["foscttm_last"] for s in per_seed]
    s1_last = [s["s1_last"] for s in per_seed]
    fos_argmaxS1_iter = [s["foscttm_argmaxS1_iter"] for s in per_seed]
    pooled_s1, pooled_fos = [], []
    for s in per_seed:
        pooled_s1 += [i["s1"] for i in s["iters"]]
        pooled_fos += [i["foscttm"] for i in s["iters"]]
    ft = torch.tensor(fos_last)
    sel = int(torch.tensor(s1_last).argmax())
    best = int(ft.argmin())
    return {
        "n_seeds": len(per_seed),
        "mean_foscttm_last": round(float(ft.mean()), 5),
        "std_foscttm_last": round(float(ft.std()), 5),
        "min_foscttm_last": round(float(ft.min()), 5),
        "max_foscttm_last": round(float(ft.max()), 5),
        "S1_selected_seed": seeds[sel],
        "S1_selected_seed_foscttm": round(fos_last[sel], 5),
        "S1_selected_seed_and_iter_foscttm": round(fos_argmaxS1_iter[sel], 5),
        "best_seed_oracle_foscttm": round(fos_last[best], 5),
        "mean_foscttm_argmaxS1_iter": round(float(torch.tensor(fos_argmaxS1_iter).mean()), 5),
        "spearman_S1last_vs_negfoscttm_across_seeds": round(spearman(s1_last, [-f for f in fos_last]), 4),
        "spearman_S1_vs_negfoscttm_pooled_iters": round(spearman(pooled_s1, [-f for f in pooled_fos]), 4),
    }


def paper_seed_canary(per_seed):
    """Mean/sd over the first PAPER_SEEDS seeds (the paper's own seeds) for the reproduction canary."""
    first = per_seed[:PAPER_SEEDS]
    fos = torch.tensor([s["foscttm_last"] for s in first])
    out = {"n": len(first), "mean_foscttm": round(float(fos.mean()), 5), "sd_foscttm": round(float(fos.std()), 5)}
    ltas = [s["lta_last"] for s in first if "lta_last" in s]
    if ltas:
        lt = torch.tensor(ltas)
        out["mean_lta"] = round(float(lt.mean()), 5)
        out["sd_lta"] = round(float(lt.std()), 5)
    return out


def analyze_pair(dataset_tag):
    base, meta = load_arm(dataset_tag, 0)
    if not base:
        return None
    out = {"meta": meta, "paper_seed_canary": paper_seed_canary(base),
           "selection": selection_stats(base), "per_seed": base}
    if meta["axis"]:
        out["type_verdict"] = type_verdict(meta["axis"])
    rem, _ = load_arm(dataset_tag, 1)
    if rem:
        rseeds = {s["seed"] for s in rem}
        matched = [s for s in base if s["seed"] in rseeds]
        out["removal"] = {"remove1_selection": selection_stats(rem),
                          "baseline_matched_selection": selection_stats(matched) if matched else None}
    return out


def cite_from_e8():
    if not E8.exists():
        return None
    d = json.load(open(E8))
    b = d["baseline_selection"]
    return {"dataset": "CITE-seq", "cka": d["canary"]["cka_all1000"], "oracle_orth": d["oracle"]["orth_holdout"],
            "oracle_lin": d["oracle"]["lin_holdout"], "n_seeds": b["n_seeds"],
            "mean": b["mean_foscttm_last"], "sd": b["std_foscttm_last"], "min": b["min_foscttm_last"],
            "max": b["max_foscttm_last"], "S1_sel": b["S1_selected_seed_foscttm"],
            "best_by_truth": b["best_seed_oracle_foscttm"],
            "spearman_across": b["spearman_S1last_vs_negfoscttm_across_seeds"],
            "paper_foscttm": 0.225, "paper_sd": 0.13, "axis": d["axis"],
            "type": type_verdict({"x": {"min_r2_top": min(d["axis"]["rna"]["heldout_r2_from_other_top5"])},
                                  "y": {"min_r2_top": min(d["axis"]["adt"]["heldout_r2_from_other_top5"])}})}


def main():
    summary = {}
    for tag in ("pbmc", "snareseq"):
        res = analyze_pair(tag)
        if res:
            summary[tag] = res
            print(f"\n===== {res['meta']['config']['dataset']} =====")
            print("paper:", res["meta"]["paper"])
            print("canary(paper seeds):", res["paper_seed_canary"], "| cka:", res["meta"]["canary"],
                  "| oracle:", res["meta"]["oracle"])
            print("type_verdict:", res.get("type_verdict"))
            print("selection:")
            for k, v in res["selection"].items():
                print(f"   {k} = {v}")
            if "axis" in res["meta"] and res["meta"]["axis"]:
                print("axis:", json.dumps(res["meta"]["axis"]))

    cite = cite_from_e8()
    if cite:
        summary["cite_e8"] = cite
        print("\n===== CITE-seq (E8, cited) =====")
        print(json.dumps({k: v for k, v in cite.items() if k != "axis"}, indent=1))

    out = OUT / "e9_merged_summary.json"
    out.write_text(json.dumps(summary, indent=2) + "\n")
    print("\nwrote", out)


if __name__ == "__main__":
    main()
