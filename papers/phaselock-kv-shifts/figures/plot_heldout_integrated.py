"""Plot paired post-fill NLL by window lifetime for the integrated Qwen assay."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("analysis", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    data = json.loads(args.analysis.read_text())
    pairs = {tuple(row["arms"]): row for row in data["comparisons"]}

    fig, axes = plt.subplots(2, 1, figsize=(8.3, 6.5), sharex=True,
                             constrained_layout=True)
    series = (
        (axes[0], ("reference", "rerotate_bf16"), "BF16 arithmetic + BF16 storage", "#b33428"),
        (axes[1], ("reference", "rerotate_fp32_bf16"), "FP32 rerotation, BF16 storage", "#e28e22"),
        (axes[1], ("reference", "ring_integer"), "Integer-phase ring", "#2257a6"),
        (axes[1], ("reference", "ring_float64"), "Float64-phase ring", "#188267"),
    )
    for axis, pair, label, color in series:
        if pair not in pairs:
            continue
        values = np.asarray(pairs[pair]["block_mean_nll_deltas"])
        axis.plot(np.arange(1, len(values) + 1), values, marker="o", markersize=3,
                  linewidth=1.65, label=label, color=color)
    for axis in axes:
        axis.axhline(0, color="#606060", linewidth=0.9, linestyle="--")
        axis.grid(axis="y", color="#dddddd", linewidth=0.6)
        axis.legend(frameon=False, fontsize=8.5, loc="best")
        axis.set_ylabel("Excess next-token NLL")
    axes[0].set_title("Destructive rerotation versus pristine reference")
    axes[1].set_title("FP32 rerotation and immutable rings versus pristine reference")
    axes[1].set_ylim(-0.045, 0.09)
    axes[1].set_xlabel("Completed 1,024-shift block after window fill")
    axes[1].set_xticks(np.arange(1, 19, 2))
    fig.suptitle("Held-out WikiText-2 test stream · Qwen2.5-1.5B · S4/W1024",
                 fontsize=11, fontweight="bold")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.out, dpi=180)
    plt.close(fig)
    print(args.out)


if __name__ == "__main__":
    main()
