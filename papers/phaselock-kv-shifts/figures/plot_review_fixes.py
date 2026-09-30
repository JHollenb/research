"""Figure 6: block shifts remove the rerotation loss; the swamped pairs carry it.

Reads evidence/review-fixes.json and writes figures/swamping-fixes.png.
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).parent
d = json.loads((HERE.parent / "evidence/review-fixes.json").read_text())
INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
plt.rcParams.update({"font.size": 10, "axes.edgecolor": INK2, "axes.labelcolor": INK, "xtick.color": INK2,
                     "ytick.color": INK2, "axes.spines.top": False, "axes.spines.right": False})
fig, (a, b) = plt.subplots(1, 2, figsize=(11, 4.2), gridspec_kw={"width_ratios": [1, 1.25]}, facecolor=SURF)
for ax in (a, b):
    ax.set_facecolor(SURF)
    ax.grid(axis="y", color=GRID, lw=0.8)
    ax.set_axisbelow(True)

# (a) perplexity change from rerotating versus shift size, matched pristine reference
models = [("qwen25-1.5b", "Qwen2.5-1.5B", "#2a78d6", "o"), ("qwen3-1.7b", "Qwen3-1.7B", "#eb6834", "s")]
for key, name, col, mk in models:
    rows = d["f6"][key]
    x = np.array([r["shift"] for r in rows])
    y = np.array([100 * (r["ppl_ratio"] - 1) for r in rows])
    lo = np.array([100 * (np.exp(r["ci95"][0]) - 1) for r in rows])
    hi = np.array([100 * (np.exp(r["ci95"][1]) - 1) for r in rows])
    a.errorbar(x, y, yerr=[y - lo, hi - y], color=col, marker=mk, ms=8, lw=2, capsize=3,
               mec=SURF, mew=1.5, label=name)
    a.annotate(f"+{y[0]:.1f}%", (x[0], y[0]), xytext=(12, 10 if y[0] < 5 else 0), textcoords="offset points",
               color=INK, va="center")
a.axhline(0, color=INK2, lw=1)
a.set_xscale("log", base=2)
a.set_xticks([1, 16, 128, 512], ["1", "16", "128", "512"])
a.set_xlabel("Positions moved per eviction (Δ)")
a.set_ylabel("Perplexity change from rerotating (%)")
a.set_title("Block shifts remove the loss", loc="left", color=INK, fontweight="bold")
a.legend(frameon=False, loc="upper right")

# (b) share of the one-token rerotation loss removed by keeping chosen RoPE pairs exact
arms = [("rerotate_exact_slow", "35 swamped pairs exact", "#1baf7a"),
        ("rerotate_exact_gamma6", "6 highest-gain pairs exact", "#4a3aa7"),
        ("rerotate_exact_fast", "29 unswamped pairs exact", "#eda100")]
mods = [("qwen25-1.5b", "Qwen2.5-1.5B"), ("qwen3-0.6b", "Qwen3-0.6B"), ("qwen3-1.7b", "Qwen3-1.7B")]
w = 0.26
for i, (arm, label, col) in enumerate(arms):
    for j, (mk_, _) in enumerate(mods):
        r = {x["arm"]: x for x in d["f7"][mk_]}.get(arm)
        if r is None:
            continue
        v = 100 * r["share_of_rerotate_excess_removed"]
        xpos = j + (i - 1) * w
        b.bar(xpos, v, w - 0.03, color=col, label=label if j == 1 else None)
        b.text(xpos, v + 2, f"{v:.0f}%", ha="center", va="bottom", fontsize=9, color=INK)
b.set_xticks(range(3), [m[1] for m in mods])
b.set_ylim(0, 118)
b.set_ylabel("Share of rerotation loss removed (%)")
b.set_title("The swamped pairs carry the loss", loc="left", color=INK, fontweight="bold")
b.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=3, fontsize=9)
b.text(0, 3, "no QK-norm", ha="center", va="bottom", fontsize=8, color=INK2, rotation=90)
fig.tight_layout()
out = HERE / "swamping-fixes.png"
fig.savefig(out, dpi=160, facecolor=SURF)
print(out)
