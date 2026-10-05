#!/usr/bin/env python3
"""Regenerate the two figures for the pass-indexed-baseline methods note.

Light single-process matplotlib; no models loaded. Every plotted value is read
from a frozen analysis.json (paths relative to ~/domains/). Run:

    python3 make_figures.py

(a) fig1-per-pass-drift.png  - per-pass native-answer drift across arms.
(b) fig2-install-vs-baseline.png - R2 install effect scored against the fixed
    parent vs the pass-indexed native, with the +/-1-nat threshold lines.
"""
import glob
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
DOMAINS = None
for _p in HERE.parents:
    if (_p / "saturn").is_dir():
        DOMAINS = _p
        break
if DOMAINS is None:
    raise SystemExit("could not locate ~/domains (no parent with a saturn/ dir)")

BASE = "saturn/experiments/2026-10-02-pass-indexed-baseline/results"
INST = "saturn/experiments/2026-10-05-pass-indexed-instruct-7b/results"

OI = {
    "black": "#000000", "orange": "#E69F00", "skyblue": "#56B4E9",
    "green": "#009E73", "yellow": "#F0E442", "blue": "#0072B2",
    "vermillion": "#D55E00", "purple": "#CC79A7", "grey": "#9A9A9A",
}


def set_style():
    plt.rcParams.update({
        "figure.dpi": 300, "savefig.dpi": 300,
        "figure.facecolor": "white", "axes.facecolor": "white",
        "savefig.facecolor": "white", "savefig.bbox": "tight",
        "font.family": "DejaVu Sans", "font.size": 8,
        "axes.titlesize": 8, "axes.labelsize": 8,
        "xtick.labelsize": 7, "ytick.labelsize": 7, "legend.fontsize": 7,
        "legend.frameon": False,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "grid.color": "#E2E2E2", "grid.linewidth": 0.5,
        "axes.axisbelow": True, "lines.linewidth": 1.0, "errorbar.capsize": 2.0,
        "pdf.fonttype": 42, "ps.fonttype": 42,
    })


def load_one(pattern):
    hits = glob.glob(str(DOMAINS / pattern))
    if not hits:
        raise SystemExit("no analysis.json for: " + pattern)
    return json.load(open(sorted(hits)[0]))


def fig1_per_pass_drift(out):
    arms = [
        ("Qwen2.5-1.5B\n(base)", BASE + "/*/analysis.json", OI["blue"]),
        ("Qwen2.5-1.5B-Instruct\n(raw)", INST + "/q15i_raw_full*/analysis.json", OI["vermillion"]),
        ("Qwen2.5-7B-Instruct\n(raw)", INST + "/q7i_raw_full_bf16*/analysis.json", OI["orange"]),
        ("Qwen2.5-1.5B-Instruct\n(chat template)", INST + "/q15i_chat_full*/analysis.json", OI["green"]),
    ]
    passes = ["1", "2", "3"]
    fig, ax = plt.subplots(figsize=(6.5, 3.3))
    narm = len(arms)
    w = 0.8 / narm
    for j, (lab, pat, col) in enumerate(arms):
        dd = load_one(pat)["R0_drift"]["median_abs_drift_by_pass"]
        xs = [i + (j - (narm - 1) / 2) * w for i in range(len(passes))]
        ys = [dd[p] for p in passes]
        ax.bar(xs, ys, width=w, color=col, label=lab, edgecolor="white", linewidth=0.4)
    ax.axhline(0.0, color=OI["black"], lw=0.7)
    ax.set_xticks(range(len(passes)))
    ax.set_xticklabels(["pass %s" % p for p in passes])
    ax.set_xlabel("turn index after install (pass 0 = install turn, drift 0 by construction)")
    ax.set_ylabel("median |Δ| native-answer log-prob\nvs fixed parent (nats)")
    ax.legend(ncol=2, loc="upper center", bbox_to_anchor=(0.5, 1.20),
              columnspacing=1.2, handlelength=1.2)
    fig.savefig(out)
    plt.close(fig)
    return out


def fig2_install_vs_baseline(out):
    r2 = load_one(BASE + "/*/analysis.json")["R2_pass_indexed_install"]
    ppm = r2["per_pass_median"]
    rows = r2["flip_rows"]
    passes = ["1", "2", "3"]
    series = [
        ("eff_fixed", "effect_vs_fixed", "vs fixed parent", OI["vermillion"]),
        ("eff_reb", "effect_vs_rebaselined", "vs pass-indexed native", OI["blue"]),
    ]
    fig, ax = plt.subplots(figsize=(6.5, 3.4))
    w = 0.34
    rng = np.random.default_rng(0)
    for j, (mkey, rkey, lab, col) in enumerate(series):
        xs = [i + (j - 0.5) * w for i in range(len(passes))]
        ys = [ppm[p][mkey] for p in passes]
        ax.bar(xs, ys, width=w, color=col, alpha=0.55, label=lab + " (median)",
               edgecolor="white", linewidth=0.4, zorder=2)
        # individual scene points
        for i, p in enumerate(passes):
            pts = [r[rkey] for r in rows if str(r["pass"]) == p]
            jx = xs[i] + rng.uniform(-w * 0.32, w * 0.32, size=len(pts))
            ax.scatter(jx, pts, s=14, color=col, edgecolors="white", linewidths=0.4,
                       zorder=4)
    ax.axhline(0.0, color=OI["black"], lw=0.8)
    for sgn in (1, -1):
        ax.axhline(sgn, color=OI["grey"], lw=0.9, ls="--")
    ax.text(len(passes) - 0.5, 1.02, "+1 nat install threshold", color=OI["grey"],
            fontsize=6, ha="right", va="bottom")
    ax.text(len(passes) - 0.5, -1.02, "−1 nat", color=OI["grey"],
            fontsize=6, ha="right", va="top")
    ax.set_xticks(range(len(passes)))
    ax.set_xticklabels(["pass %s" % p for p in passes])
    ax.set_xlabel("install read at later turn  (Qwen2.5-1.5B base, points = scenes)")
    ax.set_ylabel("install effect on native answer\nlog-prob (nats)")
    ax.legend(loc="upper right", handlelength=1.4)
    fig.savefig(out)
    plt.close(fig)
    return out


def main():
    set_style()
    print("wrote", fig1_per_pass_drift(HERE / "fig1-per-pass-drift.png"))
    print("wrote", fig2_install_vs_baseline(HERE / "fig2-install-vs-baseline.png"))


if __name__ == "__main__":
    main()
