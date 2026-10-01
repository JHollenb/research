#!/usr/bin/env python3
"""Build figures for "Space and Time Circuits" from collected reports.

Every number is read from a report.json under saturn/experiments (paths below), except the
timeline (fig1), whose events are dated lab notes and records listed in EVENTS, and the
schematic (fig6), which draws the static/dynamic split of §8 with numbers quoted from §8.

Run from anywhere:  python research/papers/space-and-time-circuits/figures/make_figures.py
Needs numpy + matplotlib only (no model code).
"""
from __future__ import annotations

import glob
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch  # noqa: E402

HERE = Path(__file__).resolve().parent
DOMAINS = HERE.parents[3]
EXP = DOMAINS / "saturn" / "experiments"
FLS = EXP / "2026-09-30-full-layer-sweeps" / "results"
MAMBA = EXP / "2026-09-30-mamba-full-layer-sweeps" / "results"
E4 = EXP / "2026-09-30-e4-pythia-recovered-loss" / "results"
E7 = EXP / "2026-09-30-e7-flux-color-multiseed" / "results" / "full-report.json"
E14 = HERE.parent / "evidence" / "hybrid-attn-ssm" / "report.json"

# Okabe-Ito palette (colorblind-safe)
C = {"space": "#0072B2", "flux": "#D55E00", "clean": "#009E73", "band": "#E69F00",
     "pair": "#CC79A7", "mamba": "#56B4E9", "grey": "#999999", "ink": "#222222"}

plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.titlesize": 10, "figure.dpi": 150, "savefig.bbox": "tight"})


def load(p):
    return json.loads(Path(p).read_text())


def one(pattern):
    hits = sorted(glob.glob(str(pattern)))
    if len(hits) != 1:
        raise SystemExit(f"expected one match for {pattern}, got {hits}")
    return hits[0]


def med(x):
    return x["fraction"]["median"]


# --------------------------------------------------------------------------- #
# E19 windows
# --------------------------------------------------------------------------- #
E19_CELLS = [  # (label, result dir glob, behavior, n_layers-agnostic colour class)
    ("Qwen2.5-1.5B identity", "e19-qwen15-57ad67c21bd1", "identity", "clean"),
    ("Gemma-2-2B identity", "e19-gemma2-2f9593a800cd", "identity", "clean"),
    ("Gemma-2-2B color", "e19-gemma2-2f9593a800cd", "color", "clean"),
    ("Qwen2.5-1.5B color", "e19-qwen15-57ad67c21bd1", "color", "clean"),
    ("SmolLM2-1.7B color", "e19-canary-6d0625ad15ee", "color", "clean"),
    ("SmolLM2-1.7B identity", "e19-canary-6d0625ad15ee", "identity", "band"),
    ("Pythia-410M s16000 identity", "e19-pythia16000-9daa3992106d", "identity", "band"),
    ("Pythia-410M s4000 identity", "e19-pythia4000-e7f7ee98ac35", "identity", "band"),
    ("Qwen2.5-0.5B identity", "e19-qwen05-40bf74c38463", "identity", "pair"),
]


def e19_curve(rdir, beh):
    s = load(FLS / rdir / "report.json")["summary"][beh]
    ks = [1]
    ys = [max(med(v) for v in s["single"].values())]
    for w in (2, 3, 4, 6, 8):
        key = f"w{w}"
        if key in s["windows"]:
            ks.append(w)
            ys.append(med(s["windows"][key]["best"]["window"]))
    return ks, ys


# --------------------------------------------------------------------------- #
# Figure 1: necessity carried by the best cut of size k
# --------------------------------------------------------------------------- #
def fig1():
    fig, ax = plt.subplots(figsize=(6.6, 3.9))
    # space control: Pythia-70M induction heads (E4/E4b, band scope, mean ablation, N_ko)
    full = load(E4 / "e4-19e98d8ac631" / "report.json")
    e4b = load(E4 / "e4-b69d8fc7654a" / "report.json")
    single = max(v["N_ko_band_cand"] for k, v in full["per_head"].items() if k.endswith("|mean"))
    pair = e4b["sets"]["pairA|band|mean"]["N_ko_cand"]
    triple = e4b["sets"]["triple|band|mean"]["N_ko_cand"]
    five = full["sets"]["five|band|mean"]["N_ko_cand"]
    ax.plot([1, 2, 3, 5], [single, pair, triple, five], "-o", color=C["space"], lw=2.2,
            label="Pythia-70M induction heads (space circuit; E4)")
    # FLUX.2 Klein 4B: denoising steps (E7, route, source interchange; 5 seeds)
    rep = load(E7)
    one_step, all_step = [], []
    for setup, x in rep["results"].items():
        a = x["arms"]["canary_e1b_route"]["source"]
        dp_all = a["all"]["dp"]
        denom = 1.0 - dp_all
        one_step.append(max((1.0 - a[f"s{t}"]["dp"]) / denom for t in range(4)))
        all_step.append(1.0)
    ax.plot([1, 4], [float(np.median(one_step)), 1.0], "-s", color=C["flux"], lw=2.2,
            label="FLUX.2 Klein 4B route, denoising steps (E7, 5 seeds)")
    # language-model K/V traces (E19)
    seen = set()
    for label, rdir, beh, cls in E19_CELLS:
        ks, ys = e19_curve(rdir, beh)
        lab = {"clean": "LM K/V trace, necessity-clean cells (E19)",
               "band": "LM K/V trace, short-band cells", "pair": "Qwen2.5-0.5B (redundant pair)"}[cls]
        ax.plot(ks, ys, "-", marker=".", color=C[cls], lw=1.4 if cls == "clean" else 1.1,
                alpha=0.95 if cls == "clean" else 0.75, label=None if lab in seen else lab)
        seen.add(lab)
    ax.axhline(0.8, color=C["grey"], ls=":", lw=1)
    ax.text(8.25, 0.8, "0.8", va="center", fontsize=8, color=C["grey"])
    ax.set_xscale("log", base=2)
    ax.set_xticks([1, 2, 3, 4, 5, 6, 8])
    ax.set_xticklabels(["1", "2", "3", "4", "5", "6", "8"])
    ax.set_xlabel("size of the best contiguous cut (heads, steps, or layers)")
    ax.set_ylabel("fraction of whole-path necessity")
    ax.set_ylim(-0.1, 1.6)
    ax.set_title("Necessity by intervention size at each declared cut")
    ax.legend(frameon=False, fontsize=7.5, loc="upper left")
    fig.savefig(HERE / "fig5-cut-size.png")
    plt.close(fig)
    return {"pythia": [single, pair, triple, five], "flux_one_step_median": float(np.median(one_step))}


# --------------------------------------------------------------------------- #
# Figure 2: per-layer necessity and write profiles
# --------------------------------------------------------------------------- #
TRANS = [("SmolLM2-1.7B identity", "canary-70c9aa8890ca"),
         ("Qwen2.5-1.5B identity", "qwen15-11f9ce05b1fd"),
         ("Gemma-2-2B identity", "gemma2-ed4ce1ac5974")]
MAMB = [("Mamba-130M identity", "sweep130-c909150c9b9f"),
        ("Mamba-370M identity", "sweep370-b04f471035d8"),
        ("Mamba-2.8B identity", "sweep28b-3114654c6ec1")]


def per_layer(d):
    keys = sorted(d, key=lambda k: int(k[1:]))
    return np.array([int(k[1:]) for k in keys]), keys


def fig2():
    fig, axes = plt.subplots(2, 3, figsize=(9.6, 5.6), sharey="row")
    for ax, (label, rdir) in zip(axes[0], TRANS):
        s = load(FLS / rdir / "report.json")["summary"]["identity"]
        xs, keys = per_layer(s["kv1_iso"]["per_layer"])
        n = len(xs)
        nec = [med(s["kv1_iso"]["per_layer"][k]) for k in keys]
        res = [s["resid_suff_single"]["per_layer"][k]["median"] for k in keys]
        kvw = [s["kv_iso_suff_single"]["per_layer"][k]["median"] for k in keys]
        ax.plot(xs / n, res, color=C["grey"], lw=1.6, label="residual write (E16)")
        ax.plot(xs / n, kvw, color=C["band"], lw=1.6, label="isolated K/V write (E17)")
        ax.bar(xs / n, nec, width=0.8 / n, color=C["clean"], label="isolated K/V necessity")
        ax.set_title(label)
    for ax, (label, rdir) in zip(axes[1], MAMB):
        cell = load(MAMBA / rdir / "report.json")["cells"]["identity"]
        # necessity_per_layer is raw Δlogprob; share = Δ / whole-path Δ (as in max_single_necessity)
        nec = np.array(cell["necessity_per_layer"]) / cell["necessity_all_delta"]
        n = len(nec)
        xs = np.arange(n)
        ax.plot(xs / n, cell["resid_write_per_layer"], color=C["grey"], lw=1.6, label="residual write")
        ax.plot(xs / n, cell["write_per_layer"], color=C["band"], lw=1.6, label="state write")
        ax.bar(xs / n, nec, width=0.8 / n, color=C["mamba"], label="state necessity")
        ax.set_title(label)
    for ax in axes.flat:
        ax.axhline(0, color=C["ink"], lw=0.5)
        ax.set_xlim(-0.02, 1.0)
    for ax in axes[0]:
        ax.set_ylim(-0.25, 1.6)
    for ax in axes[1]:
        ax.set_ylim(-0.25, 1.15)
    for ax in axes[1]:
        ax.set_xlabel("relative depth (layer / layers)")
    axes[0][0].set_ylabel("fraction (transformers)")
    axes[1][0].set_ylabel("fraction (Mamba)")
    axes[0][0].legend(frameon=False, fontsize=7, loc="upper left")
    axes[1][0].legend(frameon=False, fontsize=7, loc="upper left")
    fig.suptitle("Written once through the residual, committed late: per-layer necessity and write",
                 fontsize=10.5)
    fig.tight_layout()
    fig.savefig(HERE / "fig3-layer-profiles.png")
    plt.close(fig)


# --------------------------------------------------------------------------- #
# Figure 3: E19 window maps + Gemma sliding/global sets (E19b)
# --------------------------------------------------------------------------- #
def window_map(ax, rdir, beh, title):
    s = load(FLS / rdir / "report.json")["summary"][beh]
    n = len(s["single"])
    widths = [1, 2, 3, 4, 6, 8]
    M = np.full((len(widths), n), np.nan)
    for i, w in enumerate(widths):
        if w == 1:
            for k, v in s["single"].items():
                M[i, int(k[1:])] = med(v)
        else:
            for k, v in s["windows"][f"w{w}"]["per_window"].items():
                M[i, int(k[1:].split("-")[0])] = med(v["window"])
    im = ax.imshow(M, aspect="auto", cmap="viridis", vmin=0, vmax=1, origin="lower",
                   interpolation="nearest")
    ax.set_yticks(range(len(widths)))
    ax.set_yticklabels([str(w) for w in widths])
    ax.set_xlabel("window start layer")
    ax.set_ylabel("window width")
    ax.set_title(title)
    return im


def fig3():
    fig = plt.figure(figsize=(11.0, 3.4))
    gs = fig.add_gridspec(1, 5, width_ratios=[1.15, 1.15, 0.05, 0.22, 1.0], wspace=0.3)
    ax0 = fig.add_subplot(gs[0])
    ax1 = fig.add_subplot(gs[1])
    cax = fig.add_subplot(gs[2])
    ax2 = fig.add_subplot(gs[4])
    window_map(ax0, "e19-qwen15-57ad67c21bd1", "identity", "Qwen2.5-1.5B identity")
    im = window_map(ax1, "e19-gemma2-2f9593a800cd", "identity", "Gemma-2-2B identity")
    cb = fig.colorbar(im, cax=cax)
    cb.set_label("fraction of whole-path necessity")
    sets = load(one(FLS / "e19b-gemma2-*" / "report.json"))["summary"]
    order = [("slide16_22", "sliding\n16,18,20,22"), ("global17_23", "global\n17,19,21,23"),
             ("win16_23", "window\n16–23")]
    x = np.arange(len(order))
    for j, (beh, col) in enumerate([("identity", C["clean"]), ("color", C["band"])]):
        vals = [sets[beh]["sets"][k]["cut"]["fraction"]["median"] for k, _ in order]
        lo = [sets[beh]["sets"][k]["cut"]["fraction"]["lo"] for k, _ in order]
        hi = [sets[beh]["sets"][k]["cut"]["fraction"]["hi"] for k, _ in order]
        err = [np.subtract(vals, lo), np.subtract(hi, vals)]
        ax2.bar(x + (j - 0.5) * 0.36, vals, width=0.36, color=col, yerr=err, capsize=2, label=beh)
    ax2.axhline(0, color=C["ink"], lw=0.5)
    ax2.set_xticks(x)
    ax2.set_xticklabels([lab for _, lab in order], fontsize=7.5)
    ax2.set_title("Gemma-2-2B layer sets (E19b)")
    ax2.legend(frameon=False, fontsize=7.5)
    fig.savefig(HERE / "fig4-window-necessity.png")
    plt.close(fig)


# --------------------------------------------------------------------------- #
# Figure 4: single-site necessity vs single-site write (quadrant view)
# --------------------------------------------------------------------------- #
QCELLS = [("SmolLM2 id", "canary-70c9aa8890ca", "identity"),
          ("SmolLM2 color", "canary-70c9aa8890ca", "color"),
          ("Qwen2.5-0.5B id", "qwen05-bfcd72596050", "identity"),
          ("Qwen2.5-0.5B color", "qwen05-bfcd72596050", "color"),
          ("Qwen2.5-1.5B id", "qwen15-11f9ce05b1fd", "identity"),
          ("Qwen2.5-1.5B color", "qwen15-11f9ce05b1fd", "color"),
          ("Pythia s4000 id", "pythia4000-8ce7a03b7f57", "identity"),
          ("Pythia s16000 id", "pythia16000-177cfa16ed4a", "identity"),
          ("Gemma-2 id", "gemma2-ed4ce1ac5974", "identity"),
          ("Gemma-2 color", "gemma2-ed4ce1ac5974", "color")]


def fig4():
    fig, ax = plt.subplots(figsize=(6.8, 5.0))
    ax.add_patch(plt.Rectangle((0, 0), 0.25, 0.2, color=C["clean"], alpha=0.10, lw=0))
    ax.text(0.01, 0.025, "low singleton effects\nwhole-path checks also required", fontsize=7,
            color=C["clean"], va="bottom")
    ax.axvline(0.25, color=C["grey"], ls=":", lw=0.8)
    ax.axhline(0.2, color=C["grey"], ls=":", lw=0.8)
    ax.add_patch(plt.Rectangle((0.5, 0.5), 0.55, 0.55, color=C["space"], alpha=0.08, lw=0))
    ax.text(0.52, 1.04, "large singleton effects", fontsize=7, color=C["space"], va="top")
    pts = []
    for label, rdir, beh in QCELLS:
        p = FLS / rdir / "report.json"
        if not p.exists():
            continue
        s = load(p)["summary"].get(beh)
        if not s or "kv1_iso" not in s or "kv_iso_suff_single" not in s:
            continue
        x = s["kv1_iso"]["best"]["fraction"]["median"]
        y = s["kv_iso_suff_single"]["best"]["median"]
        pts.append((label, x, y))
        ax.scatter(x, y, color=C["band"], s=28, zorder=3)
        off = {"Qwen2.5-1.5B id": (4, 5), "Gemma-2 id": (4, -9), "Qwen2.5-0.5B id": (4, 4),
               "Qwen2.5-1.5B color": (-6, -11), "Qwen2.5-0.5B color": (4, -9)}.get(label, (4, 2))
        ax.annotate(label, (x, y), xytext=off, textcoords="offset points", fontsize=6.5)
    for label, rdir in MAMB:
        cell = load(MAMBA / rdir / "report.json")["cells"]["identity"]
        x = cell["max_single_necessity"]["share"]
        y = cell["max_single_write"]["s_norm"]
        pts.append((label, x, y))
        ax.scatter(x, y, color=C["mamba"], marker="D", s=26, zorder=3)
        ax.annotate(label.replace(" identity", ""), (x, y), xytext=(4, -8),
                    textcoords="offset points", fontsize=6.5)
    for beh, offset in [("identity", (-65, 21)), ("color", (12, -17))]:
        s = load(E14)["summary"][beh]
        x = max(v["fraction"]["median"] for v in s["necessity"]["attn"].values())
        y = max(v["median"] for v in s["write"]["attn"].values())
        label = "Falcon attention " + ("id" if beh == "identity" else "color")
        pts.append((label, x, y))
        ax.scatter(x, y, color=C["flux"], marker="^", s=45, zorder=4)
        ax.annotate(label, (x, y), xytext=offset, textcoords="offset points", fontsize=7,
                    arrowprops={"arrowstyle": "-", "color": C["flux"], "lw": 0.6})
    ax.set_xlim(-0.05, 1.08)
    ax.set_ylim(-0.05, 1.08)
    ax.set_xlabel("best singleton necessity share of its own whole-cut effect")
    ax.set_ylabel("best singleton normalized write (isolated K/V or state)")
    ax.set_title("Singleton necessity and write profiles differ across specimens\n"
                 "Selected full sweeps; Falcon adds weaker attention write ports")
    ax.scatter([], [], color=C["band"], s=28, label="transformer cells (E3b/E17)")
    ax.scatter([], [], color=C["mamba"], marker="D", s=26, label="Mamba cells (E16)")
    ax.scatter([], [], color=C["flux"], marker="^", s=45, label="Falcon attention (E14)")
    ax.legend(frameon=False, fontsize=7, loc="lower right")
    fig.savefig(HERE / "fig2-quadrants.png")
    plt.close(fig)
    return pts


# --------------------------------------------------------------------------- #
# Figure 5: timeline
# --------------------------------------------------------------------------- #
EVENTS = [  # (date, lane, label, source)
    ("2026-08-05", 0, "FLUX.2 Klein 4B run as a program", "obsidian/blog/2026-08-05-164341-real-flux2-klein4b-multistream-lowering.md"),
    ("2026-08-11", 0, "FLUX semantic route certified;\nsingle-step patching misses it", "research/bfl/docs/certified-semantic-circuits/paper.md"),
    ("2026-08-11", 1, "AR source circuit closed (Qwen)", "obsidian/blog/2026-08-11-the-autoregressive-source-circuit-closed.md"),
    ("2026-08-14", 1, "Pythia induction forms (space circuit)", "obsidian/blog/2026-08-14-we-watched-a-capability-being-born.md"),
    ("2026-08-20", 2, "blind-graded instrument trial", "obsidian/blog/2026-08-20-214500-the-instruments-took-the-stand.md"),
    ("2026-08-21", 1, "\"final boss\" conjecture; IRD sink grid", "obsidian/blog/2026-08-21-114500-the-final-boss-circuit.md"),
    ("2026-08-25", 1, "final boss = a role, not a layer", "obsidian/blog/2026-08-25-221529-the-final-boss-was-a-role-not-a-layer.md"),
    ("2026-08-26", 3, "crossed-pairing leak retracted", "obsidian/blog/2026-08-26-105431-the-leak-was-in-the-oracle-not-the-address.md"),
    ("2026-08-26", 0, "skeleton holds while coordinates move", "obsidian/blog/2026-08-26-151627-the-hypergraph-had-a-skeleton.md"),
    ("2026-08-31", 3, "rank-16 clock retracted", "obsidian/blog/2026-08-31-143646-rank-16-was-a-basin-not-a-clock.md"),
    ("2026-09-01", 0, "SDXL native scene compiler", "obsidian/blog/2026-09-01-231018-we-found-the-native-scene-compiler.md"),
    ("2026-09-04", 2, "Saturn VM", "obsidian/blog/2026-09-04-151836-from-final-boss-to-saturn-vm.md"),
    ("2026-09-22", 2, "pointwise paper: single-site\ntests miss distributed stores", "research/papers/pointwise-instruments-miss-distributed-circuits/paper.md"),
    ("2026-09-25", 1, "exact join replaces attention's read", "saturn/experiments/2026-09-25-ar-exact-join-admission/FINDINGS.md"),
    ("2026-09-30", 3, "Mamba certificates and 30B\nin-forward certificate retracted", "saturn/experiments/2026-09-30-full-layer-sweeps/PLAN.md"),
    ("2026-09-30", 1, "one residual seed, late commit (E16/E17)", "saturn/experiments/2026-09-30-full-layer-sweeps/FINDINGS-E17-isolated-kv-writes.md"),
    ("2026-09-30", 2, "circuit-tracer misses the store (E6)", "saturn/experiments/2026-09-30-circuit-tracer-head-to-head/FINDINGS.md"),
    ("2026-10-01", 1, "the path is a late band (E19)", "saturn/experiments/2026-09-30-full-layer-sweeps/FINDINGS-E19-window-necessity.md"),
]
LANES = ["diffusion", "language models", "instruments", "retractions"]
LANE_C = [C["flux"], C["clean"], C["space"], C["pair"]]


def fig5():
    import datetime as dt
    for _, _, _, src in EVENTS:
        if not (DOMAINS / src).exists():
            raise SystemExit(f"timeline source missing: {src}")
    d0 = dt.date(2026, 8, 3)
    fig, ax = plt.subplots(figsize=(11.5, 5.0))
    counts: dict = {}
    for date, lane, label, _ in EVENTS:  # noqa: B007
        d = (dt.date.fromisoformat(date) - d0).days
        k = counts.get((lane, date), 0)
        counts[(lane, date)] = k + 1
        idx = len([e for e in EVENTS[:EVENTS.index((date, lane, label, _))] if e[1] == lane])
        y = lane + [0.36, -0.36, 0.18, -0.18][idx % 4]
        ax.scatter(d, lane, color=LANE_C[lane], s=30, zorder=3)
        ax.plot([d, d], [lane, y], color=LANE_C[lane], lw=0.6)
        ax.text(d + 0.3, y, label, fontsize=6.4, va="center", color=C["ink"])
    for i in range(len(LANES)):
        ax.axhline(i, color=LANE_C[i], lw=0.8, alpha=0.4)
    ax.set_yticks(range(len(LANES)))
    ax.set_yticklabels(LANES)
    ticks = [dt.date(2026, 8, 5), dt.date(2026, 8, 15), dt.date(2026, 8, 25), dt.date(2026, 9, 5),
             dt.date(2026, 9, 15), dt.date(2026, 9, 25), dt.date(2026, 10, 1)]
    ax.set_xticks([(t - d0).days for t in ticks])
    ax.set_xticklabels([t.strftime("%b %d") for t in ticks])
    ax.set_xlim(0, (dt.date(2026, 10, 9) - d0).days)
    ax.set_ylim(-0.7, len(LANES) - 0.3)
    ax.spines["left"].set_visible(False)
    ax.set_title("How circuit formation and control were mapped, Aug 5 – Oct 1, 2026")
    fig.savefig(HERE / "fig1-timeline.png")
    plt.close(fig)


# --------------------------------------------------------------------------- #
# Figure 6: static skeleton with dynamic overlays (§8 schematic)
# --------------------------------------------------------------------------- #
def fig6():
    blocks = ["joint.0", "joint.1", "joint.2", "joint.3", "joint.4", "single.0", "single.1…", "VAE"]
    route = {"joint.2", "joint.3", "joint.4", "single.0"}
    steps = ["t0", "t1", "t2", "t3"]
    fig, ax = plt.subplots(figsize=(9.4, 4.2))
    for j, st in enumerate(steps):
        for i, b in enumerate(blocks):
            if b == "VAE" and j < 3:
                continue
            on = b in route
            ax.add_patch(FancyBboxPatch((i - 0.38, j - 0.3), 0.76, 0.6,
                                        boxstyle="round,pad=0.02,rounding_size=0.08",
                                        fc="#d9d9d9" if on else "#f2f2f2",
                                        ec=C["ink"] if on else C["grey"], lw=1.1 if on else 0.6))
            ax.text(i, j, b, ha="center", va="center", fontsize=6.6,
                    color=C["ink"] if on else C["grey"])
        ax.text(-0.75, j, st, ha="right", va="center", fontsize=8)
    # static route across steps
    for j in range(len(steps) - 1):
        ax.add_patch(FancyArrowPatch((5, j + 0.3), (5, j + 0.7), arrowstyle="-|>",
                                     mutation_scale=8, color=C["ink"], lw=0.9))
    ax.text(7.55, 0.6, "static skeleton (grey):\nroute order, writer roles,\nstate boundaries, consumer,\n"
            "prompt-time K/V", fontsize=7, va="center")
    # dynamic overlays (numbers quoted from §8)
    ax.add_patch(FancyBboxPatch((2.55, -0.42), 0.9, 3.84, boxstyle="round,pad=0.02",
                                fc="none", ec=C["clean"], lw=1.6, ls="--"))
    ax.text(2.2, 3.62, "spectral address at joint.3,\nall four steps (6/6)", fontsize=6.5,
            color=C["clean"], ha="center")
    ax.add_patch(FancyBboxPatch((4.55, 1.62), 0.9, 0.76, boxstyle="round,pad=0.02",
                                fc="none", ec=C["flux"], lw=1.8))
    ax.text(6.5, 2.0, "register @ t2 only: 0.403", fontsize=6.5, color=C["flux"], va="center")
    ax.add_patch(FancyBboxPatch((4.55, 2.62), 0.9, 0.76, boxstyle="round,pad=0.02",
                                fc="none", ec=C["pair"], lw=1.8))
    ax.text(5.0, 3.62, "program @ t3 only: 0.712; both: 1.000, pixel-exact", fontsize=6.5,
            color=C["pair"], ha="center")
    ax.annotate("eye color 0.887, eye geometry 0.931,\nobject registers 13.7× / 9.6×:\n"
                "payloads loaded onto the same route", xy=(3.0, 0.0), xytext=(-0.6, -1.25),
                fontsize=6.5, color=C["space"], arrowprops=dict(arrowstyle="->", color=C["space"]))
    ax.set_xlim(-1.2, 9.6)
    ax.set_ylim(-1.6, 3.9)
    ax.axis("off")
    ax.set_title("Static infrastructure, dynamic circuits (FLUX.2 Klein 4B, §8): "
                 "denoising steps × blocks", fontsize=10)
    fig.savefig(HERE / "fig6-skeleton-overlays.png")
    plt.close(fig)


if __name__ == "__main__":
    f1 = fig1()
    fig2()
    fig3()
    pts = fig4()
    fig5()
    fig6()
    print(json.dumps({"fig1": f1, "fig4_points": [(a, round(b, 3), round(c, 3)) for a, b, c in pts]},
                     indent=1))
