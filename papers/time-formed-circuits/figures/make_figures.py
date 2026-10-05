#!/usr/bin/env python3
"""Regenerate the data-driven figures for the Time-Formed Circuits paper.

Light, single-process matplotlib only; no models are loaded. Every plotted value
is read from a frozen data file under ~/domains/ (resolved by walking up to the
directory that contains `saturn/`). Run:

    python3 make_figures.py

Figures written next to this script. Fig 1 (hand-drawn schematic) is not produced
here. See figures/README.md for the per-figure data provenance.
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# ---------------------------------------------------------------- paths
HERE = Path(__file__).resolve().parent
DOMAINS = None
for _p in HERE.parents:
    if (_p / "saturn").is_dir():
        DOMAINS = _p
        break
if DOMAINS is None:
    raise SystemExit("could not locate ~/domains (no parent with a saturn/ dir)")


def d(rel):
    """Open a JSON data file given a path relative to ~/domains/."""
    return json.load(open(DOMAINS / rel))


# ---------------------------------------------------------------- style
# Okabe-Ito colour-blind-safe palette.
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
        "font.family": "DejaVu Sans",  # DejaVu digits are tabular (fixed-width)
        "font.size": 8, "axes.titlesize": 8, "axes.labelsize": 8,
        "xtick.labelsize": 7, "ytick.labelsize": 7, "legend.fontsize": 7,
        "legend.frameon": False,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "grid.color": "#E2E2E2", "grid.linewidth": 0.5,
        "axes.axisbelow": True, "lines.linewidth": 1.0, "errorbar.capsize": 2.0,
        "pdf.fonttype": 42, "ps.fonttype": 42,
    })


def asym_err(med, lo, hi):
    """Return a (2,1) yerr column clipped to non-negative distances."""
    return np.array([[max(0.0, med - lo)], [max(0.0, hi - med)]])


# ---------------------------------------------------------------- Fig 2
def fig2_dissociation(out):
    stats = d("saturn/experiments/2026-10-02-p1-reviewer-experiments/results/B_clustered_stats.json")
    pts = d("saturn/experiments/2026-10-02-e20-cross-family/results/analysis.json")
    pt_by = {c["family"]: c for c in pts["cells"]}

    order = ["qwen_pub", "qwen_ho", "gemma", "smollm2"]
    names = {
        "qwen_pub": "Qwen2.5-1.5B\n(published)",
        "qwen_ho": "Qwen2.5-1.5B\n(held-out)",
        "gemma": "Gemma-2-2B", "smollm2": "SmolLM2-1.7B",
    }
    # arm key in analysis.json, arm key in clustered stats, label, colour
    arms = [
        ("__seed__", None, "seed", OI["grey"]),
        ("block_removed", "block", "block removed", OI["vermillion"]),
        ("rescue_recovered", "rescue", "rescue recovered", OI["blue"]),
        ("wrong_identity_retained", "wrong", "wrong-identity retained", OI["orange"]),
    ]

    fig, ax = plt.subplots(figsize=(6.5, 3.3))
    nfam, narm = len(order), len(arms)
    w = 0.8 / narm
    for j, (pkey, ckey, lab, col) in enumerate(arms):
        xs, ys, los, his = [], [], [], []
        for i, fam in enumerate(order):
            x = i + (j - (narm - 1) / 2) * w
            if pkey == "__seed__":
                y, lo, hi = 1.0, None, None
            else:
                y = pt_by[fam][pkey]["median"]
                cell = next(c for c in stats["cells"] if c["key"] == fam)
                ci = cell["identity_clustered_bootstrap"][ckey]
                lo, hi = ci["lo"], ci["hi"]
            xs.append(x); ys.append(y); los.append(lo); his.append(hi)
        bars = ax.bar(xs, ys, width=w, color=col, label=lab,
                      edgecolor="white", linewidth=0.4,
                      hatch=("//" if pkey == "__seed__" else None))
        if pkey != "__seed__":
            for x, y, lo, hi in zip(xs, ys, los, his):
                ax.errorbar(x, y, yerr=asym_err(y, lo, hi), fmt="none",
                            ecolor=OI["black"], elinewidth=0.7, capsize=2.0)
    ax.axhline(1.0, color=OI["grey"], lw=0.7, ls=":")
    ax.axhline(0.0, color=OI["black"], lw=0.7)
    ax.set_xticks(range(nfam))
    ax.set_xticklabels([names[f] for f in order])
    ax.set_ylabel("fraction of per-row seed effect")
    ax.set_ylim(-0.52, 1.25)
    ax.legend(ncol=2, loc="upper center", bbox_to_anchor=(0.5, 1.14),
              columnspacing=1.2, handlelength=1.2)
    fig.savefig(out)
    plt.close(fig)
    return out


# ---------------------------------------------------------------- Fig 3
def fig3_formation(out):
    A = d("saturn/experiments/2026-10-02-p1-reviewer-experiments/results/A_analysis.json")
    cell_by = {c["model"]: c for c in A["cells"]}
    models = [("qwen15", "Qwen2.5-1.5B"), ("gemma2", "Gemma-2-2B")]
    arms = [
        ("residual_seed", "seed (residual)", OI["grey"]),
        ("rescue_late_band", "late band", OI["blue"]),
        ("rescue_seed_layer", "seed layer", OI["vermillion"]),
        ("rescue_early_band", "earlier band", OI["orange"]),
        ("rescue_linear_pred_late", "linear seed→band prediction", OI["green"]),
    ]
    fig, ax = plt.subplots(figsize=(6.5, 3.3))
    nmod, narm = len(models), len(arms)
    w = 0.82 / narm
    for j, (akey, lab, col) in enumerate(arms):
        xs, ys, errs = [], [], []
        for i, (mkey, _) in enumerate(models):
            x = i + (j - (narm - 1) / 2) * w
            f = cell_by[mkey]["arms"][akey]["fraction_of_seed_effect"]
            xs.append(x); ys.append(f["median"])
            errs.append(asym_err(f["median"], f["lo"], f["hi"]))
        ax.bar(xs, ys, width=w, color=col, label=lab, edgecolor="white",
               linewidth=0.4, hatch=("//" if akey == "residual_seed" else None))
        for x, y, e in zip(xs, ys, errs):
            ax.errorbar(x, y, yerr=e, fmt="none", ecolor=OI["black"],
                        elinewidth=0.7, capsize=2.0)
    ax.axhline(1.0, color=OI["grey"], lw=0.7, ls=":")
    ax.axhline(0.0, color=OI["black"], lw=0.7)
    ax.set_xticks(range(nmod))
    ax.set_xticklabels([m[1] for m in models])
    ax.set_ylabel("fraction of per-row seed effect")
    ax.set_ylim(-0.15, 1.15)
    ax.legend(ncol=3, loc="upper center", bbox_to_anchor=(0.5, 1.16),
              columnspacing=1.0, handlelength=1.2)
    fig.savefig(out)
    plt.close(fig)
    return out


# ---------------------------------------------------------------- Fig 4
def fig4_error_interchange(out):
    C = d("saturn/experiments/2026-10-02-p1-reviewer-experiments/results/C_analysis.json")
    native = d("saturn/experiments/2026-09-30-full-layer-sweeps/results/gemma2-ed4ce1ac5974/report.json")
    metric = "all_positions_all_layers"  # the "fraction moved" used in the paper
    arms = [
        ("features_only", "feature-only", OI["skyblue"]),
        ("features_plus_error", "matched\nfeature+error", OI["blue"]),
        ("error_only", "error-only", OI["orange"]),
    ]
    panels = [("identity", "Identity"), ("color", "Color")]
    fig, axes = plt.subplots(1, 2, figsize=(6.5, 3.2), sharey=True)
    for ax, (beh, title) in zip(axes, panels):
        bd = C["behaviors"][beh]
        xs = np.arange(len(arms))
        ys = [bd["arms"][a[0]][metric]["median"] for a in arms]
        ax.bar(xs, ys, width=0.62, color=[a[2] for a in arms],
               edgecolor="white", linewidth=0.4)
        # native key/value cut reference (from the 42-identity / 25-color sweep)
        kv = native["summary"][beh]["kv_range"]
        whole = kv["all"]["fraction"]["median"]
        sh = kv["second"]["fraction"]
        ax.axhline(whole, color=OI["black"], lw=1.1, ls="-",
                   label="native cut, whole path" if beh == "identity" else None)
        ax.axhspan(sh["lo"], sh["hi"], color=OI["grey"], alpha=0.18, lw=0)
        ax.axhline(sh["median"], color=OI["black"], lw=1.1, ls="--",
                   label="native cut, second half" if beh == "identity" else None)
        ax.axhline(0.0, color=OI["black"], lw=0.7)
        ax.set_xticks(xs)
        ax.set_xticklabels([a[1] for a in arms])
        ax.set_xlabel("%s (n=%d)" % (title, bd["n"]))
        ax.set_ylim(-0.25, 1.1)
    axes[0].set_ylabel("fraction of answer moved to filler")
    axes[0].legend(loc="upper left", bbox_to_anchor=(0.02, 0.80), handlelength=1.6)
    fig.savefig(out)
    plt.close(fig)
    return out


# ---------------------------------------------------------------- Fig 5
def fig5_flux_quadrants(out):
    rep = d("saturn/experiments/2026-09-30-flux2-joint01-time-accumulation/results/full-report.json")
    # derive the four bounds across all scenes / site-sets
    src_single, src_all, wr_single, wr_all = [], [], [], []
    for sd in rep["results"].values():
        for sv in sd.get("site_sets", {}).values():
            src = sv.get("necessity", {}).get("source", {})
            for step, v in src.items():
                (src_all if step == "all" else src_single).append(v["scene_progress"])
            suf = sv.get("sufficiency", {})
            for step, v in suf.items():
                (wr_all if step == "all" else wr_single).append(v["scene_progress"])
    suff_single = max(wr_single)   # best single-call transfer
    suff_all = min(wr_all)         # worst-case whole-path transfer
    nec_single = min(src_single)   # best single-call removal (min remaining)
    nec_all = max(src_all)         # worst-case whole-path removal (max remaining)

    ms = d("saturn/experiments/2026-09-30-e7-flux-color-multiseed/results/full-summary.json")
    seeds = ["color_s1337", "color_s2024", "color_s4242", "color_s7217_canary", "color_s9001"]
    seed_lab = ["1337", "2024", "4242", "7217", "9001"]
    variants = [("resid_route", "route", OI["blue"], "o", True),
                ("canary_e1b_route", "route (E1b canary)", OI["vermillion"], "s", False)]

    fig = plt.figure(figsize=(6.5, 2.9))
    gs = fig.add_gridspec(1, 3, width_ratios=[1, 1, 1.25], wspace=0.42)
    ax0, ax1, ax2 = (fig.add_subplot(gs[i]) for i in range(3))

    # sufficiency
    ax0.bar([0, 1], [suff_single, suff_all], width=0.6,
            color=[OI["skyblue"], OI["blue"]], edgecolor="white", linewidth=0.4)
    ax0.axhline(0.90, color=OI["green"], lw=1.1, ls="--")
    ax0.text(1.48, 0.90, "transfer\nP≥0.90", color=OI["green"], va="center",
             ha="right", fontsize=6)
    ax0.set_xticks([0, 1]); ax0.set_xticklabels(["single\ncall", "all\ncalls"])
    ax0.set_ylim(0, 1.02); ax0.set_ylabel("image progress  P")
    ax0.set_xlabel("sufficiency (write)")
    for x, y in zip([0, 1], [suff_single, suff_all]):
        ax0.text(x, y + 0.02, "%.3f" % y, ha="center", va="bottom", fontsize=6)

    # necessity
    ax1.bar([0, 1], [nec_single, nec_all], width=0.6,
            color=[OI["orange"], OI["vermillion"]], edgecolor="white", linewidth=0.4)
    ax1.axhline(0.15, color=OI["green"], lw=1.1, ls="--")
    ax1.text(1.48, 0.17, "removal\nP≤0.15", color=OI["green"], va="bottom",
             ha="right", fontsize=6)
    ax1.set_xticks([0, 1]); ax1.set_xticklabels(["single\ncall", "all\ncalls"])
    ax1.set_ylim(0, 1.02)
    ax1.set_xlabel("necessity (source replace)\nremaining progress")
    for x, y in zip([0, 1], [nec_single, nec_all]):
        ax1.text(x, y + 0.02, "%.3f" % y, ha="center", va="bottom", fontsize=6)

    # five-seed colour necessity strip
    for vkey, vlab, col, mk, filled in variants:
        xs = np.arange(len(seeds))
        ys = [ms["setups"][s]["arms"][vkey]["source"]["all_dp"] for s in seeds]
        ax2.scatter(xs, ys, marker=mk, s=26, label=vlab,
                    facecolors=(col if filled else "none"), edgecolors=col, linewidths=1.0)
    ax2.axhline(-1.0, color=OI["green"], lw=1.0, ls=":")
    ax2.text(len(seeds) - 0.5, -0.97, "source", color=OI["green"], fontsize=6,
             ha="right", va="bottom")
    ax2.axhline(0.0, color=OI["black"], lw=0.7)
    ax2.set_xticks(range(len(seeds))); ax2.set_xticklabels(seed_lab, rotation=0)
    ax2.set_xlabel("seed  (all-call source interchange)")
    ax2.set_ylabel("dp  (−1 source … +1 target)")
    ax2.set_ylim(-1.08, 0.15)
    ax2.legend(loc="upper center", bbox_to_anchor=(0.5, 1.18), ncol=1, handlelength=1.2)
    fig.savefig(out)
    plt.close(fig)
    return out


# ---------------------------------------------------------------- Fig 6
def fig6_blind_band_families(out):
    A = d("saturn/experiments/2026-10-05-e20-nonqwen-families/results/analysis.json")
    cells = {c["family"]: c for c in A["new_cells"]}
    order = ["olmo2", "pythia14b", "phi2", "gpt2xl"]
    names = {"olmo2": "OLMo-2-1B", "pythia14b": "Pythia-1.4B",
             "phi2": "Phi-2", "gpt2xl": "GPT-2 XL"}
    arms = [
        ("__seed__", "seed", OI["grey"]),
        ("block_removed", "block removed", OI["vermillion"]),
        ("rescue_recovered", "rescue recovered", OI["blue"]),
        ("wrong_identity_retained", "wrong-identity retained", OI["orange"]),
    ]
    fig, ax = plt.subplots(figsize=(6.5, 3.3))
    nfam, narm = len(order), len(arms)
    w = 0.8 / narm
    for j, (key, lab, col) in enumerate(arms):
        xs, ys, errs = [], [], []
        for i, fam in enumerate(order):
            x = i + (j - (narm - 1) / 2) * w
            if key == "__seed__":
                xs.append(x); ys.append(1.0); errs.append(None)
            else:
                v = cells[fam][key]
                xs.append(x); ys.append(v["median"])
                errs.append(asym_err(v["median"], v["lo"], v["hi"]))
        ax.bar(xs, ys, width=w, color=col, label=lab, edgecolor="white",
               linewidth=0.4, hatch=("//" if key == "__seed__" else None))
        for x, y, e in zip(xs, ys, errs):
            if e is not None:
                ax.errorbar(x, y, yerr=e, fmt="none", ecolor=OI["black"],
                            elinewidth=0.7, capsize=2.0)
    ax.axhline(1.0, color=OI["grey"], lw=0.7, ls=":")
    ax.axhline(0.0, color=OI["black"], lw=0.7)
    ax.set_xticks(range(nfam))
    ax.set_xticklabels([names[f] for f in order])
    ax.set_ylabel("fraction of per-row seed effect")
    ax.set_ylim(-0.4, 1.85)
    ax.legend(ncol=2, loc="upper center", bbox_to_anchor=(0.5, 1.15),
              columnspacing=1.2, handlelength=1.2)
    fig.savefig(out)
    plt.close(fig)
    return out


# ---------------------------------------------------------------- Fig S1
def _window_profile(report, beh):
    """Return {width: [(center_layer, median_fraction), ...]} incl. width 1."""
    s = report["summary"][beh]
    prof = {}
    single = []
    for lk, v in s["single"].items():
        L = int(lk[1:])
        single.append((L, v["fraction"]["median"]))
    prof[1] = sorted(single)
    for wk, wv in s["windows"].items():
        width = int(wk[1:])
        pts = []
        for name, v in wv["per_window"].items():
            a, b = name[1:].split("-")
            center = (int(a) + int(b)) / 2.0
            pts.append((center, v["window"]["fraction"]["median"]))
        prof[width] = sorted(pts)
    return prof


def figS1_window_necessity(out):
    cells = [
        ("saturn/experiments/2026-09-30-full-layer-sweeps/results/e19-qwen15-57ad67c21bd1/report.json",
         "identity", "Qwen2.5-1.5B (identity)"),
        ("saturn/experiments/2026-09-30-full-layer-sweeps/results/e19-gemma2-2f9593a800cd/report.json",
         "identity", "Gemma-2-2B (identity)"),
    ]
    widths = [1, 2, 3, 4, 6, 8]
    cmap = {1: OI["grey"], 2: OI["skyblue"], 3: OI["green"], 4: OI["orange"],
            6: OI["blue"], 8: OI["vermillion"]}
    fig, axes = plt.subplots(1, 2, figsize=(6.5, 3.1), sharey=True)
    for ax, (path, beh, title) in zip(axes, cells):
        rep = d(path)
        prof = _window_profile(rep, beh)
        for wdt in widths:
            if wdt not in prof:
                continue
            xs = [p[0] for p in prof[wdt]]
            ys = [p[1] for p in prof[wdt]]
            ax.plot(xs, ys, marker="o", ms=2.2, lw=0.9, color=cmap[wdt],
                    label=("single" if wdt == 1 else "width %d" % wdt))
        ax.axhline(1.0, color=OI["grey"], lw=0.7, ls=":")
        ax.axhline(0.0, color=OI["black"], lw=0.7)
        ax.set_xlabel("window centre (layer index)")
        ax.set_title(title, fontsize=7)
    axes[0].set_ylabel("median signed fraction of whole-path effect")
    axes[1].legend(ncol=1, loc="upper left", handlelength=1.4)
    fig.savefig(out)
    plt.close(fig)
    return out


# ---------------------------------------------------------------- Fig S2
def figS2_mamba_clock_retest(out):
    s = d("saturn/experiments/2026-10-02-mamba-clock-retest/results/summary.json")
    cells = s["scored"]
    labels = ["%s\n%s" % (c["model"], c["object"]) for c in cells]
    rel = [c["writer"]["ret_release"] for c in cells]
    wrt = [c["writer"]["write_matched"] for c in cells]
    null_abs = [c["random_null"]["mean_abs"] for c in cells]
    sub = s["frozen_thresholds"]["substantial_nats"]

    fig, ax = plt.subplots(figsize=(6.5, 3.2))
    x = np.arange(len(cells))
    w = 0.38
    ax.bar(x - w / 2, rel, width=w, color=OI["blue"], label="retention release lever",
           edgecolor="white", linewidth=0.4)
    ax.bar(x + w / 2, wrt, width=w, color=OI["orange"], label="matched write lever",
           edgecolor="white", linewidth=0.4)
    # per-cell random-null noise floor band (+/- mean_abs) drawn at 0
    for xi, na in zip(x, null_abs):
        ax.add_patch(plt.Rectangle((xi - 0.45, -na), 0.9, 2 * na,
                                   color=OI["grey"], alpha=0.25, lw=0, zorder=0))
    ax.axhline(0.0, color=OI["black"], lw=0.7)
    for sgn in (1, -1):
        ax.axhline(sgn * sub, color=OI["green"], lw=0.8, ls="--")
    ax.text(len(cells) - 0.5, sub, "substantial ±0.3 nats", color=OI["green"],
            fontsize=6, ha="right", va="bottom")
    ax.set_xticks(x); ax.set_xticklabels(labels)
    ax.set_ylabel("Δ log-prob at writer (nats)")
    ax.set_xlabel("Mamba model × object  (grey band = random-null |Δ| floor)")
    ax.legend(loc="upper left", handlelength=1.2)
    fig.savefig(out)
    plt.close(fig)
    return out


def main():
    set_style()
    jobs = [
        ("fig2-dissociation.png", fig2_dissociation),
        ("fig3-formation.png", fig3_formation),
        ("fig4-error-interchange.png", fig4_error_interchange),
        ("fig5-flux-quadrants.png", fig5_flux_quadrants),
        ("fig6-blind-band-families.png", fig6_blind_band_families),
        ("figS1-window-necessity.png", figS1_window_necessity),
        ("figS2-mamba-clock-retest.png", figS2_mamba_clock_retest),
    ]
    for name, fn in jobs:
        out = fn(HERE / name)
        print("wrote", out)


if __name__ == "__main__":
    main()
