"""Parse E7 receipts under results/e7_search_init/ into the NOTES tables. Reads receipts only; no compute."""

from __future__ import annotations

import glob
import json
from pathlib import Path

RES = Path(__file__).resolve().parents[1] / "results" / "e7_search_init"


def load_receipts() -> list[dict]:
    out = []
    for p in sorted(glob.glob(str(RES / "*.json"))):
        if Path(p).name == "jobs.json":
            continue
        try:
            out.append((Path(p).name, json.loads(Path(p).read_text())))
        except Exception as e:  # noqa
            print("skip", p, e)
    return out


def corr(xs, ys):
    import statistics as st
    if len(xs) < 3:
        return float("nan")
    mx, my = st.mean(xs), st.mean(ys)
    num = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
    dx = sum((a - mx) ** 2 for a in xs) ** 0.5
    dy = sum((b - my) ** 2 for b in ys) ** 0.5
    return num / (dx * dy) if dx and dy else float("nan")


def main() -> None:
    receipts = load_receipts()
    print(f"# {len(receipts)} receipts\n")
    print("## A/B/C/D rows (arm, corpus, cand/k, FOSCTTM)")
    for fname, rec in receipts:
        rows = rec.get("results", {}).get("rows", [])
        for r in rows:
            if r.get("arm", "").startswith("E_"):
                continue
            key = r.get("candidate", "")
            if "k_pairs" in r:
                key = f"k={r['k_pairs']}"
            if "k_removed" in r:
                key = f"drop{r['k_removed']}"
            f = r.get("foscttm_eval_only")
            extra = ""
            if "S1_matched_cosine" in r:
                extra = f"  S1={r['S1_matched_cosine']:.4f}"
            print(f"  {r.get('arm'):28s} {r.get('corpus','?'):28s} {str(key):8s} "
                  f"FOSCTTM={f:.4f}{extra}  [{fname}]")
    print("\n## E trace-selection (per run: last vs best-by-S1 vs best-overall; S1-vs-FOSCTTM corr)")
    for fname, rec in receipts:
        for r in rec.get("results", {}).get("rows", []):
            if not r.get("arm", "").startswith("E_"):
                continue
            tr = r.get("trace", [])
            s1 = [e["S1_matched_cosine"] for e in tr]
            fo = [e["foscttm"] for e in tr]
            c = corr(s1, [-x for x in fo])  # S1 vs -FOSCTTM
            gain_vs_last = r["foscttm_last"] - r["foscttm_at_bestS1"]
            print(f"  {r.get('corpus','?'):26s} {r.get('language','?'):10s} seed{r.get('seed')} "
                  f"last={r['foscttm_last']:.4f} bestS1={r['foscttm_at_bestS1']:.4f} "
                  f"(iter {r['bestS1_iter']}) best={r['foscttm_best']:.4f} "
                  f"S1sel_gain_vs_last={gain_vs_last:+.4f}  corr(S1,-FOSCTTM)={c:.3f}  [{fname}]")


def aggregate():
    """Mean +/- sd over seeds per (arm, corpus, cand/k). Ignores smoke receipts."""
    import statistics as st
    acc = {}
    for fname, rec in load_receipts():
        if "smoke" in fname:
            continue
        for r in rec.get("results", {}).get("rows", []):
            arm = r.get("arm", "")
            if arm.startswith("E_"):
                continue
            key = r.get("candidate", "")
            if "k_pairs" in r:
                key = f"k={r['k_pairs']}"
            if "k_removed" in r:
                key = f"drop{r['k_removed']}"
            f = r.get("foscttm_eval_only")
            if f is None:
                continue
            acc.setdefault((arm, r.get("corpus", "?"), str(key)), []).append(f)
    print("\n## Seed-aggregated FOSCTTM (mean +/- sd, n)")
    for k in sorted(acc):
        vs = acc[k]
        sd = st.pstdev(vs) if len(vs) > 1 else 0.0
        mark = "  <0.10" if st.mean(vs) < 0.10 else ""
        print(f"  {k[0]:28s} {k[1]:28s} {k[2]:8s} {st.mean(vs):.4f} +/- {sd:.4f}  n={len(vs)}  {sorted(round(v,4) for v in vs)}{mark}")


if __name__ == "__main__":
    main()
    aggregate()
