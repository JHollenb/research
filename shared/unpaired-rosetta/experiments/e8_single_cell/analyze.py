"""Merge E8 shard receipts (per-seed float records only) and compute the authoritative cross-seed selection stats,
correlations, and the baseline-vs-removal comparison. No real data is touched -- this reads the small JSON numbers the
Beast jobs already produced.

    python -m e8_single_cell.analyze
"""

from __future__ import annotations

import json
from pathlib import Path

import torch

from e8_single_cell.run import spearman

OUT = Path(__file__).resolve().parents[1] / "results" / "e8_single_cell"


def load_arm(remove_topk: int):
    """Merge all shard receipts for a given removal level, deduped by seed; return (per_seed, meta)."""
    by_seed, meta = {}, {}
    for path in sorted(OUT.glob(f"e8_citeseq_remove{remove_topk}_*.json")) + (
        sorted(OUT.glob("e8_citeseq_remove0-*.json")) if remove_topk == 0 else []
    ):
        r = json.load(open(path))
        for s in r["results"]["per_seed"]:
            by_seed[s["seed"]] = s  # later files win; identical config so harmless
        meta = {"canary": r["results"]["canary"], "oracle": r["results"]["oracle"],
                "axis": r["results"].get("axis"), "aligner": r["config"]["aligner"], "smoke": r["config"]["smoke"]}
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
        "best_seed_oracle_foscttm": round(fos_last[best], 5),  # labelled: uses truth
        "mean_foscttm_argmaxS1_iter": round(float(torch.tensor(fos_argmaxS1_iter).mean()), 5),
        "spearman_S1last_vs_negfoscttm_across_seeds": round(spearman(s1_last, [-f for f in fos_last]), 4),
        "spearman_S1_vs_negfoscttm_pooled_iters": round(spearman(pooled_s1, [-f for f in pooled_fos]), 4),
    }


def main():
    base, meta = load_arm(0)
    print("== canary ==", meta["canary"])
    print("== oracle ==", meta["oracle"])
    print("== axis ==", json.dumps(meta["axis"], indent=1) if meta["axis"] else None)
    bsel = selection_stats(base)
    print("== baseline selection ==")
    for k, v in bsel.items():
        print(f"   {k} = {v}")
    print("== per-seed (baseline) ==")
    for s in base:
        print(f"   seed {s['seed']}: fos_last={s['foscttm_last']:.4f} s1_last={s['s1_last']:.4f} "
              f"fos@argmaxS1={s['foscttm_argmaxS1_iter']:.4f} best_iter_fos={s['foscttm_best_iter_oracle']:.4f}")

    removal = {}
    rem, _ = load_arm(1)
    if rem:
        rsel = selection_stats(rem)
        rseeds = {s["seed"] for s in rem}
        matched_base = [s for s in base if s["seed"] in rseeds]
        mb = selection_stats(matched_base) if matched_base else None
        removal = {"remove1_selection": rsel, "baseline_matched_selection": mb}
        print("== removal (top-1 axis) selection ==")
        for k, v in rsel.items():
            print(f"   {k} = {v}")
        if mb:
            print(f"   [matched baseline mean={mb['mean_foscttm_last']} S1sel={mb['S1_selected_seed_foscttm']}]")

    summary = {"canary": meta["canary"], "oracle": meta["oracle"], "axis": meta["axis"],
               "aligner": meta["aligner"], "smoke": meta["smoke"],
               "baseline_selection": bsel, "baseline_per_seed": base, "removal": removal}
    out = OUT / "e8_merged_summary.json"
    out.write_text(json.dumps(summary, indent=2) + "\n")
    print("wrote", out)


if __name__ == "__main__":
    main()
