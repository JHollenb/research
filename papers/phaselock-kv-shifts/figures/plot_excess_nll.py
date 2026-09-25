"""Render the binned excess-NLL figure from the included PhaseLock-only data."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "evidence" / "nll-bins.json"
OUTPUT = ROOT / "figures" / "excess-nll.png"


def main() -> None:
    data = json.loads(DATA.read_text())
    arms = data["arms"]
    reference = arms["pristine_float"]
    x = [(i + 0.5) * data["bin_size"] / 1000 for i in range(len(reference))]

    fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(10.8, 3.7), sharex=True)
    styles = [
        ("phaselock", "PhaseLock", "#007f7f"),
        ("quantize_once_q8", "Q8 quantized once", "#2980b9"),
        ("requantize_each_shift_q8", "Q8 requantized per shift", "#d35400"),
    ]
    for key, label, color in styles:
        excess = [value - base for value, base in zip(arms[key], reference)]
        ax_left.plot(x, excess, marker="o", markersize=2.8, linewidth=1.8,
                     color=color, label=label)

    bf16_excess = [value - base for value, base in zip(arms["rerotate_bf16"], reference)]
    ax_right.plot(x, bf16_excess, marker="o", markersize=3.2, linewidth=1.9,
                  color="#9b2c5a", label="BF16 rerotated per shift")

    for ax in (ax_left, ax_right):
        ax.axhline(0, color="#777777", linewidth=0.8)
        ax.axvline((data["sinks"] + data["window"]) / 1000,
                   color="#777777", linestyle="--", linewidth=0.9)
        ax.set_xlim(0, data["n_tokens"] / 1000)
        ax.set_xlabel("Stream position (thousand tokens)")
        ax.grid(axis="y", color="#e5e5e5", linewidth=0.6)
        ax.spines[["top", "right"]].set_visible(False)
        ax.legend(loc="upper right", frameon=False, fontsize=8)

    ax_left.set_title("Pristine and Q8 key paths")
    ax_left.set_ylabel("Excess next-token NLL (nats)")
    ax_left.set_ylim(-0.06, 0.63)
    ax_right.set_title("Repeated BF16 rerotation")
    ax_right.set_ylim(-0.25, 5.0)
    fig.suptitle("Error after sliding-cache evictions begin", fontsize=12)
    fig.tight_layout()
    fig.savefig(OUTPUT, dpi=220, bbox_inches="tight")
    plt.close(fig)
    print(OUTPUT)


if __name__ == "__main__":
    main()
