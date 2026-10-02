#!/usr/bin/env python3
"""Generate the two figures for the rounding-placement paper in ONE process.

Fig: mechanism-schematic.png  — the swamping mechanism (value = invariant + content;
     native-coordinate rounding spends the mantissa on the invariant; remove-first fixes it).
Fig: bx-vs-fp8-bars.png       — full-step gradient error, primary metric (median_param_rel),
     from the verified Table 6 numbers (ea-pythia160m.json / ea-pythia410m.json).

Run once:  python3 figures/make_figures.py
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
import numpy as np

# ---------------------------------------------------------------- Figure: schematic
fig, axes = plt.subplots(1, 2, figsize=(9.6, 4.0))
fig.suptitle("Where you round: rounding lands on the invariant unless you remove it first",
             fontsize=12, fontweight="bold")

INV = "#9ecae1"      # invariant (large)
CON = "#f16913"      # content (small, what the model uses)
MANT = "#31a354"     # the mantissa band actually resolved

def draw_value(ax, x, invariant, content, label):
    """Draw a stored value as a tall invariant block + a thin content block on top."""
    ax.add_patch(Rectangle((x, 0), 0.5, invariant, facecolor=INV, edgecolor="k", lw=0.8))
    ax.add_patch(Rectangle((x, invariant), 0.5, content, facecolor=CON, edgecolor="k", lw=0.8))
    ax.text(x + 0.25, -0.6, label, ha="center", va="top", fontsize=9)

# Left panel: round in native coordinates
ax = axes[0]
ax.set_title("Round in native coordinates", fontsize=10)
draw_value(ax, 0.3, 10.0, 0.6, "stored\nvalue")
# mantissa band (8 bits ≈ 1/256 of the magnitude) sits near the top of the big block
band_lo = 10.6 * (1 - 1/8)   # a readable stand-in for the resolved band
ax.add_patch(Rectangle((1.3, band_lo), 0.5, 10.6 - band_lo, facecolor="none",
                        edgecolor=MANT, lw=1.6, hatch="////"))
ax.add_patch(Rectangle((1.3, 0), 0.5, band_lo, facecolor=INV, edgecolor="k", lw=0.8, alpha=0.5))
ax.text(1.55, 10.9, "mantissa band\n(8–11 bits of the magnitude)", ha="center", va="bottom",
        fontsize=8, color=MANT)
ax.text(1.55, -0.6, "what the\nformat resolves", ha="center", va="top", fontsize=9)
ax.annotate("content falls\nbelow the band\n→ erased", xy=(0.8, 10.3), xytext=(2.1, 7.5),
            fontsize=8, color=CON,
            arrowprops=dict(arrowstyle="->", color=CON, lw=1.3))
ax.set_xlim(0, 3.1); ax.set_ylim(-1.8, 12.4); ax.axis("off")

# Right panel: remove the invariant first
ax = axes[1]
ax.set_title("Remove the invariant first, then round", fontsize=10)
draw_value(ax, 0.3, 10.0, 0.6, "stored\nvalue")
arrow = FancyArrowPatch((0.95, 5.0), (1.55, 5.0), arrowstyle="->", mutation_scale=14, lw=1.4)
ax.add_patch(arrow)
ax.text(1.25, 5.4, "subtract\ninvariant", ha="center", va="bottom", fontsize=8)
# content now sits at the bottom, fully inside the band
ax.add_patch(Rectangle((1.8, 0), 0.5, 0.6, facecolor=CON, edgecolor="k", lw=0.8))
ax.add_patch(Rectangle((1.8, 0), 0.5, 0.6, facecolor="none", edgecolor=MANT, lw=1.6, hatch="////"))
ax.text(2.05, 1.1, "content now\nfills the band\n→ preserved", ha="center", va="bottom",
        fontsize=8, color=CON)
ax.text(2.05, -0.6, "content\n(gauge fixed)", ha="center", va="top", fontsize=9)
ax.set_xlim(0, 3.1); ax.set_ylim(-1.8, 12.4); ax.axis("off")

fig.text(0.5, 0.015,
         "Invariant = key mean / projection bias / per-channel gain / absolute position. "
         "Content = key-to-key differences the model actually uses.",
         ha="center", fontsize=8, style="italic")
fig.tight_layout(rect=[0, 0.04, 1, 0.95])
fig.savefig("figures/mechanism-schematic.png", dpi=150)
plt.close(fig)

# ---------------------------------------------------------------- Figure: B(x) vs FP8 bars
# median_param_rel (%), verified from ea-pythia160m.json / ea-pythia410m.json (Table 6).
arms = ["BF16", "BF16+B(x)", "MXFP8\n(block)", "MXFP8+B(x)"]
p160 = [203.8, 11.8, 67138.6, 76.1]      # Pythia-160m, final checkpoint
p410 = [42.7, 3.0, 18105.8, 41.0]        # Pythia-410m, final checkpoint
colors = ["#6baed6", "#08519c", "#fdae6b", "#e6550d"]

fig, axes = plt.subplots(1, 2, figsize=(9.6, 4.2), sharey=True)
for ax, vals, title in zip(axes, [p160, p410],
                           ["Pythia-160m (final)", "Pythia-410m (final)"]):
    xs = np.arange(len(arms))
    ax.bar(xs, vals, color=colors, edgecolor="k", lw=0.6)
    ax.set_yscale("log")
    ax.set_title(title, fontsize=10)
    ax.set_xticks(xs); ax.set_xticklabels(arms, fontsize=8)
    ax.axhline(100, color="grey", ls=":", lw=0.8)  # 100% = gradient as large as itself
    for x, v in zip(xs, vals):
        lab = f"{v:,.0f}%" if v >= 100 else f"{v:.1f}%"
        ax.text(x, v * 1.25, lab, ha="center", va="bottom", fontsize=8)
    ax.set_ylim(1, 3e5)
axes[0].set_ylabel("median per-parameter gradient error (%), log scale", fontsize=9)
fig.suptitle("B(x) fixes the full BF16 step; on block-FP8 it only reaches plain-BF16 error",
             fontsize=12, fontweight="bold")
fig.text(0.5, 0.01,
         "Dotted line = 100% (error as large as the gradient). Primary metric: median_param_rel. "
         "Source: ea-pythia160m.json / ea-pythia410m.json.",
         ha="center", fontsize=8, style="italic")
fig.tight_layout(rect=[0, 0.05, 1, 0.94])
fig.savefig("figures/bx-vs-fp8-bars.png", dpi=150)
plt.close(fig)

print("wrote figures/mechanism-schematic.png and figures/bx-vs-fp8-bars.png")
