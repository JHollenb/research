"""Figures for response.md, drawn only from the JSON receipts in ../results/.

    python experiments/figures/make_figures.py        # needs matplotlib; writes ../figures/*.png
"""

from __future__ import annotations

import glob
import json
import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
RESULTS = HERE.parent / "results"
OUT = HERE.parents[1] / "figures"
ENCODERS = [("qwen3-8b-gen", "Qwen3-8B gen"), ("qwen3-embedding-8b", "Qwen3-Embedding-8B"), ("mpnet", "MPNet")]
COLORS = {"qwen3-8b-gen": "#c2410c", "qwen3-embedding-8b": "#2563eb", "mpnet": "#059669"}


def gate_rows() -> dict:
    """{encoder: {candidate: {seed: row}}} from the gate-detector receipts."""
    table: dict = {}
    for path in glob.glob(str(RESULTS / "e5_scaffold_axis" / "e5_gates-*.json")):
        if "smoke" in path:
            continue
        match = re.search(r"-seed(\d+)-", path)
        row = json.loads(Path(path).read_text())["results"]["row"]
        encoder = row["language"].split("_")[0]
        table.setdefault(encoder, {}).setdefault(row["candidate"], {})[int(match.group(1)) if match else 0] = row
    return table


def figure_scaffold_fix(table: dict) -> None:
    fig, (left, right) = plt.subplots(1, 2, figsize=(11, 4.2), gridspec_kw={"width_ratios": [1.1, 1]})
    width = 0.26
    arms = [("none", "no gate (their pipeline)", "#9ca3af"), ("pc0", "gate off top PC", "#f59e0b"),
            ("pick", "gate detector's pick (no pairs)", "#111827")]
    for i, (encoder, label) in enumerate(ENCODERS):
        cands = table[encoder]
        for j, (arm, arm_label, color) in enumerate(arms):
            if arm == "pick":
                values = []
                for seed in sorted(cands["none"]):
                    pair = [c for c in cands if seed in cands[c]]  # all settings run at this seed
                    best = max(pair, key=lambda c: cands[c][seed]["S1_matched_cosine"])
                    values.append(cands[best][seed]["foscttm_eval_only"])
            else:
                values = [r["foscttm_eval_only"] for r in cands[arm].values()]
            x = i + (j - 1) * width
            left.bar(x, sum(values) / len(values), width, color=color, label=arm_label if i == 0 else None)
            left.scatter([x] * len(values), values, s=10, color="white", edgecolor="black", linewidth=0.6, zorder=3)
    left.set_xticks(range(len(ENCODERS)), [label for _, label in ENCODERS])
    left.set_ylabel("FOSCTTM on SPC holdout (lower is better)")
    left.set_title("A. One non-visual axis breaks Qwen3-gen; the detector fixes it\nand leaves good encoders alone",
                   fontsize=10, loc="left")
    left.legend(frameon=False, fontsize=8, loc="upper right")
    left.set_ylim(0, 0.52)
    left.spines[["top", "right"]].set_visible(False)

    for encoder, label in ENCODERS:
        rows = [cands[0] for cands in table[encoder].values() if 0 in cands]
        s1 = [r["S1_matched_cosine"] for r in rows]
        fo = [r["foscttm_eval_only"] for r in rows]
        right.scatter(s1, fo, color=COLORS[encoder], label=label, s=28)
        chosen = max(rows, key=lambda r: r["S1_matched_cosine"])
        right.scatter([chosen["S1_matched_cosine"]], [chosen["foscttm_eval_only"]], s=140, facecolor="none",
                      edgecolor=COLORS[encoder], linewidth=1.6)
    right.set_xlabel("S1: matched cosine of each fit on its own training rows (no pairs)")
    right.set_ylabel("FOSCTTM (true pairs, evaluation only)")
    right.set_title("B. The unpaired score ranks the six gate settings (seed 0);\nringed = chosen", fontsize=10,
                    loc="left")
    right.legend(frameon=False, fontsize=8)
    right.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(OUT / "fig1-scaffold-axis-fix.png", dpi=160)
    plt.close(fig)


def figure_fidelity_gap() -> None:
    receipt = sorted(glob.glob(str(RESULTS / "e1_fidelity_gap" / "e1_fidelity_gap-2*.json")))[-1]
    arms = {a["arm"]: a for a in json.loads(Path(receipt).read_text())["results"]["arms"]}
    show = [("ours-p0", "their method,\nzero pairs"), ("orth-oracle", "best rotation\n(20k true pairs)"),
            ("lin-oracle", "best linear map\n(20k true pairs)")]
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    ax.axhspan(0, 0.50, color="#fee2e2", zorder=0)
    ax.axhspan(0.895, 1.0, color="#dcfce7", zorder=0)
    ax.text(2.45, 0.25, "FLUX failed\n(≤ 0.50)", fontsize=8, color="#991b1b", ha="right", va="center")
    ax.text(2.45, 0.947, "FLUX rendered 8/8 (≥ 0.895)", fontsize=8, color="#166534", ha="right", va="center")
    for i, (arm, label) in enumerate(show):
        q = arms[arm]["alpha"]
        ax.vlines(i, q["q05"], q["q95"], color="#374151", linewidth=1.2)
        ax.add_patch(plt.Rectangle((i - 0.18, q["q25"]), 0.36, q["q75"] - q["q25"], facecolor="#93c5fd",
                                   edgecolor="#1e3a8a", zorder=3))
        ax.hlines(q["q50"], i - 0.18, i + 0.18, color="#1e3a8a", linewidth=2.2, zorder=4)
        ax.text(i + 0.22, q["q50"], f"median {q['q50']:.2f}\nFOSCTTM {arms[arm]['foscttm']:.4f}", fontsize=8,
                va="center")
    ax.set_xticks(range(len(show)), [label for _, label in show])
    ax.set_xlim(-0.5, 2.5)
    ax.set_ylim(0, 1)
    ax.set_ylabel("fidelity α (cosine to true partner)")
    ax.set_title("Near-identical retrieval, very different fidelity (COCO val, 40,504 pairs;\n"
                 "box = quartiles, whisker = 5th–95th percentile)", fontsize=10, loc="left")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(OUT / "fig2-fidelity-gap.png", dpi=160)
    plt.close(fig)


def main() -> None:
    OUT.mkdir(exist_ok=True)
    figure_scaffold_fix(gate_rows())
    figure_fidelity_gap()
    print("wrote", sorted(p.name for p in OUT.glob("*.png")))


if __name__ == "__main__":
    main()
