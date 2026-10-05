#!/usr/bin/env python3
"""Regenerate the two figures for the InterpBench instrument-audit paper.

Light single-process matplotlib; no models loaded. Both figures read AUROC values
directly from the frozen per-model result file. Run:

    python3 make_figures.py

Data: saturn/experiments/2026-10-05-interpbench-method-audit/results/full.json
  (86 records; 2 have ok=False with no node_auroc -> 84 usable models).
"""
import json
import math
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

DATA = DOMAINS / "saturn/experiments/2026-10-05-interpbench-method-audit/results/full.json"

OI = {
    "black": "#000000", "orange": "#E69F00", "skyblue": "#56B4E9",
    "green": "#009E73", "yellow": "#F0E442", "blue": "#0072B2",
    "vermillion": "#D55E00", "purple": "#CC79A7", "grey": "#9A9A9A",
}

# methods to plot (the 11 keys named in the paper; random_single is excluded)
METHODS = ["act_patch", "eap", "eap_ig", "gradxact", "gradxact_mag",
           "writesite", "writesite_raw", "subspace", "subspace_rand",
           "subspace_rank1", "random"]
BASELINES = {"act_patch", "eap_ig", "eap"}
CONTROLS = {"subspace_rand", "subspace_rank1"}
PRETTY = {
    "act_patch": "act_patch", "eap": "EAP", "eap_ig": "EAP-IG",
    "gradxact": "grad×act\n(centred std)", "gradxact_mag": "grad×act\n(magnitude)",
    "writesite": "write-site\n(baseline-rel)", "writesite_raw": "write-site\n(raw)",
    "subspace": "subspace", "subspace_rand": "subspace\nrand ctrl",
    "subspace_rank1": "subspace\nrank-1 ctrl", "random": "random",
}


def set_style():
    plt.rcParams.update({
        "figure.dpi": 300, "savefig.dpi": 300,
        "figure.facecolor": "white", "axes.facecolor": "white",
        "savefig.facecolor": "white", "savefig.bbox": "tight",
        "font.family": "DejaVu Sans", "font.size": 8,
        "axes.titlesize": 8, "axes.labelsize": 8,
        "xtick.labelsize": 6.5, "ytick.labelsize": 7, "legend.fontsize": 7,
        "legend.frameon": False,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "grid.color": "#E2E2E2", "grid.linewidth": 0.5,
        "axes.axisbelow": True, "lines.linewidth": 1.0,
        "pdf.fonttype": 42, "ps.fonttype": 42,
    })


def load_records():
    recs = []
    for x in json.load(open(DATA)):
        na = x.get("node_auroc")
        if isinstance(na, dict) and x.get("ok", True):
            recs.append(x)
    return recs


def vals(recs, m):
    out = []
    for x in recs:
        v = x["node_auroc"].get(m)
        if v is not None and not (isinstance(v, float) and math.isnan(v)):
            out.append(v)
    return out


def fig1_strip(recs, out):
    means = {m: np.mean(vals(recs, m)) for m in METHODS}
    order = sorted(METHODS, key=lambda m: -means[m])
    rand = sorted(vals(recs, "random"))
    null_lo, null_hi = rand[0], rand[-1]  # 0.486 .. 0.517 across the 84 models

    rng = np.random.default_rng(0)
    fig, ax = plt.subplots(figsize=(6.5, 3.6))
    ax.axhspan(null_lo, null_hi, color=OI["green"], alpha=0.14, lw=0,
               label="random-null band\n[%.3f, %.3f]" % (null_lo, null_hi))
    ax.axhline(0.5, color=OI["grey"], lw=0.7, ls=":")
    for i, m in enumerate(order):
        y = vals(recs, m)
        x = i + rng.uniform(-0.18, 0.18, size=len(y))
        if m in CONTROLS:
            col, mk = OI["purple"], "D"
        elif m in BASELINES:
            col, mk = OI["blue"], "o"
        else:
            col, mk = OI["grey"], "o"
        ax.scatter(x, y, s=9, color=col, alpha=0.45, marker=mk,
                   linewidths=0, zorder=2)
        # mean marker
        ax.plot([i - 0.30, i + 0.30], [means[m], means[m]], color=OI["vermillion"],
                lw=2.0, zorder=4, solid_capstyle="butt")
        ax.text(i, 1.015, "%.2f" % means[m], ha="center", va="bottom",
                fontsize=6, color=OI["vermillion"])
    ax.set_xticks(range(len(order)))
    labels = ax.set_xticklabels([PRETTY[m] for m in order])
    for lab, m in zip(labels, order):
        if m in BASELINES:
            lab.set_fontweight("bold")
    ax.set_ylabel("node AUROC (per model, n=%d)" % len(recs))
    ax.set_ylim(0.15, 1.06)
    ax.set_xlim(-0.6, len(order) - 0.4)
    # proxy legend handles
    from matplotlib.lines import Line2D
    handles = [
        Line2D([0], [0], color=OI["vermillion"], lw=2.0, label="method mean"),
        Line2D([0], [0], marker="o", color="none", markerfacecolor=OI["blue"],
               markersize=5, label="high-recall baseline", linestyle="none"),
        Line2D([0], [0], marker="D", color="none", markerfacecolor=OI["purple"],
               markersize=5, label="subspace control", linestyle="none"),
    ]
    ax.legend(handles=handles, loc="lower left", ncol=1, handlelength=1.4)
    fig.savefig(out)
    plt.close(fig)
    return out


def fig2_scatter(recs, out):
    fig, ax = plt.subplots(figsize=(3.6, 3.6))
    ax.plot([0, 1], [0, 1], color=OI["black"], lw=0.9, ls="--", label="y = x")
    groups = [(True, "categorical", OI["blue"], "o", 16),
              (False, "regression", OI["orange"], "s", 22)]
    for cat, lab, col, mk, sz in groups:
        xs = [x["node_auroc"]["act_patch"] for x in recs if bool(x.get("categorical")) == cat]
        ys = [x["node_auroc"]["gradxact"] for x in recs if bool(x.get("categorical")) == cat]
        n = sum(1 for x in recs if bool(x.get("categorical")) == cat)
        ax.scatter(xs, ys, s=sz, facecolors=(col if cat else "none"),
                   edgecolors=col, linewidths=0.8, alpha=0.8,
                   label="%s (n=%d)" % (lab, n), zorder=3)
    # optional magnitude-form overlay
    xm = [x["node_auroc"]["act_patch"] for x in recs]
    ym = [x["node_auroc"]["gradxact_mag"] for x in recs]
    ax.scatter(xm, ym, s=10, color=OI["green"], alpha=0.35, marker="^",
               linewidths=0, label="grad×act magnitude", zorder=2)
    ax.set_xlabel("activation patching  node AUROC")
    ax.set_ylabel("gradient×activation  node AUROC")
    ax.set_xlim(0.3, 1.02)
    ax.set_ylim(0.3, 1.02)
    ax.set_aspect("equal", adjustable="box")
    ax.legend(loc="lower right", handlelength=1.2)
    fig.savefig(out)
    plt.close(fig)
    return out


def main():
    set_style()
    recs = load_records()
    print("usable records:", len(recs))
    print("wrote", fig1_strip(recs, HERE / "fig1-method-auroc-strip.png"))
    print("wrote", fig2_scatter(recs, HERE / "fig2-actpatch-vs-gradxact.png"))


if __name__ == "__main__":
    main()
