"""E3 step 4: tables and the mechanical verdict of every frozen prediction in PREREG.md.

    uv run python -m e3_pooling_scaffold.analyze results/e3_pooling_scaffold/job-XXXX/report.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

CORPORA = ("coco_train2014", "StanfordParagraphCaptioning")


def cka(c: dict, key: str) -> float | None:
    v = c.get(key)
    return None if v is None else v["mean"]


def slices(c: dict, key: str) -> list[float]:
    return c[key]["slices"]


def main(path: Path) -> None:
    r = json.loads(path.read_text())
    layers = r["config"]["layers"]
    last = max(layers)
    depth = {l: l / r["config"]["num_hidden_layers"] for l in layers}
    lines, verdicts = [], {}

    for corpus in CORPORA:
        c = r[corpus]
        lines.append(f"\n### {corpus}\n")
        lines.append("| arm | " + " | ".join(f"L{l} ({depth[l]:.2f})" for l in layers) + " |")
        lines.append("|---|" + "---:|" * len(layers))
        arms = sorted({k.rsplit("/", 1)[0] for k in c if k.count("/") == 2 and isinstance(c[k], dict)})
        for arm in arms:
            row = [cka(c, f"{arm}/L{l}") if f"{arm}/L{l}" in c else None for l in layers]
            lines.append(f"| `{arm}` | " + " | ".join("—" if v is None else f"{v:.3f}" for v in row) + " |")
        lines.append(f"| `reference/mpnet_stored` | {cka(c, 'reference/mpnet_stored'):.3f} (all layers n/a) |")
        for mode in ("think", "nothink"):
            d = c[f"{mode}/diagnostics"]
            lines.append(f"\n{mode}: mean captured positions {d['mean_generated_positions']:.1f}; reaching </think> "
                         f"{d['share_reaching_post_think']:.2%}; scaffold token share at positions 0-15: "
                         + ", ".join(f"{x:.2f}" for x in d["scaffold_token_share_by_position"][:16]))

    def share_ok(corpus):
        s = r[corpus]["think/diagnostics"]["scaffold_token_share_by_position"]
        return len(s) > 12 and min(s[:12]) >= 0.9
    verdicts["A1"] = all(share_ok(c) for c in CORPORA)

    wins = sum(a > b for corpus in CORPORA for a, b in zip(slices(r[corpus], f"think/gen_tokcentered/L{last}"),
                                                             slices(r[corpus], f"think/gen_all/L{last}")))
    verdicts["A2"] = wins >= 3
    spc = r["StanfordParagraphCaptioning"]
    base = cka(spc, f"think/gen_all/L{last}")
    reached = spc["think/diagnostics"]["share_reaching_post_think"] > 0
    candidates = [k for k in spc if k.count("/") == 2 and isinstance(spc[k], dict) and "mean" in spc[k] and (
        (k.startswith("nothink/gen") and "post_think" not in k) or k.startswith("think/gen_tokcentered")
        or (reached and k.startswith("think/gen_post_think")))]
    best_key = max(candidates, key=lambda k: cka(spc, k))
    verdicts["A3"] = cka(spc, best_key) - base >= 0.02
    verdicts["A4"] = all(cka(r[c], f"mean/mean_caption/L{last}") >= cka(r[c], f"mean/mean_all/L{last}") for c in CORPORA)

    def best_depth(corpus, arm):
        return depth[max(layers, key=lambda l: cka(r[corpus], f"{arm}/L{l}"))]
    bests = {(c, a): best_depth(c, a) for c in CORPORA for a in ("mean/mean_caption", "nothink/gen_all")}
    verdicts["B1"] = all(v < 1.0 for v in bests.values())
    verdicts["B2"] = all(0.6 <= v <= 0.9 for v in bests.values())

    print("\n".join(lines))
    print("\n### Verdicts (frozen PREREG predictions)\n")
    print(f"- A1 scaffold share >= 0.9 at first 12 positions, both corpora: {verdicts['A1']}")
    print(f"- A2 tokcentered > gen_all at final layer in >= 3/4 corpus-slice cells: {verdicts['A2']} ({wins}/4)")
    print(f"- A3 SPC best scaffold-removed arm gain >= 0.02: {verdicts['A3']} "
          f"(best {best_key} = {cka(spc, best_key):.3f} vs think/gen_all {base:.3f})")
    print(f"- A4 mean_caption >= mean_all at final layer, both corpora: {verdicts['A4']}")
    print(f"- B1 best depth < 1.0: {verdicts['B1']}  B2 best depth in [0.6, 0.9]: {verdicts['B2']}  {bests}")
    loo = [k for k in r[CORPORA[0]] if "gen_tokcentered_loo20" in k and k.startswith("think/")]
    if loo:
        wins2 = sum(a > b for corpus in CORPORA for a, b in zip(
            slices(r[corpus], f"think/gen_tokcentered_loo20/L{last}"), slices(r[corpus], f"think/gen_all/L{last}")))
        verdicts["A2_amended"] = wins2 >= 3
        print(f"- A2' (Amendment 2, post-hoc) loo20 > gen_all at final layer in >= 3/4 cells: {verdicts['A2_amended']} ({wins2}/4)")
    # Effect sizes (Amendment 3). A frozen bar decides only its own prediction; the claim is read from these paired
    # per-slice differences. A cell's sign counts only when both slices agree.
    def paired(corpus, a, b):
        d = [x - y for x, y in zip(slices(r[corpus], a), slices(r[corpus], b))]
        sign = "+" if all(v > 0 for v in d) else "-" if all(v < 0 for v in d) else "mixed"
        return {"slices": [round(v, 4) for v in d], "mean": round(sum(d) / len(d), 4), "sign": sign}
    comparisons = {
        "A2 think tokcentered - gen_all": ("think/gen_tokcentered", "think/gen_all"),
        "A2' think loo20 - gen_all": ("think/gen_tokcentered_loo20", "think/gen_all"),
        "nothink tokcentered - gen_all": ("nothink/gen_tokcentered", "nothink/gen_all"),
        "nothink loo20 - gen_all": ("nothink/gen_tokcentered_loo20", "nothink/gen_all"),
        "A4 mean_caption - mean_all": ("mean/mean_caption", "mean/mean_all"),
    }
    effects = {}
    for name, (a, b) in comparisons.items():
        for corpus in CORPORA:
            if f"{a}/L{last}" in r[corpus]:
                effects[f"{name}|{corpus}"] = paired(corpus, f"{a}/L{last}", f"{b}/L{last}")
    late = max(l for l in layers if l < last)
    for arm in ("mean/mean_all", "mean/mean_caption", "nothink/gen_all", "think/gen_all"):
        for corpus in CORPORA:
            effects[f"B L{late} - L{last} {arm}|{corpus}"] = paired(corpus, f"{arm}/L{late}", f"{arm}/L{last}")
    print("\n### Effects (paired per-slice differences, clipped CKA)\n")
    for k, v in effects.items():
        print(f"- {k}: mean {v['mean']:+.4f} slices {v['slices']} sign {v['sign']}")
    print(f"\nwall {r.get('wall_s', 0):.0f} s, peak VRAM {r.get('peak_vram_mb') or 0:.0f} MB")
    (path.parent / "verdicts.json").write_text(json.dumps({"verdicts": verdicts, "best_depths": {
        f"{c}|{a}": v for (c, a), v in bests.items()}, "A3_best": best_key, "effects": effects}, indent=2))


if __name__ == "__main__":
    main(Path(sys.argv[1]))
