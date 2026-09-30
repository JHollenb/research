"""Section 6 figures: fp32 phase threshold, rotation swamping, decode speed vs window."""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

EV = Path(__file__).resolve().parent.parent / "evidence"
FIG = Path(__file__).resolve().parent


def offsets():
    x = json.loads((EV / "free-wins-offset.json").read_text())
    fig, ax = plt.subplots(figsize=(7.4, 4.0), constrained_layout=True)
    for phase, color, label in (("fp32", "#b33428", "FP32 angle (Hugging Face rotary contract)"),
                                ("fp64", "#188267", "FP64 angle"), ("int32", "#2257a6", "PhaseLock int32 ring")):
        rows = sorted({r["offset"]: r for r in x["rows"] if r["phase"] == phase and r["offset"] > 0}.values(),
                      key=lambda r: r["offset"])
        ax.plot([r["offset"] for r in rows], [r["ppl_steady"] for r in rows], marker="o", ms=4,
                color=color, label=label, lw=1.6)
    ax.axvline(2 ** 24, color="#606060", ls="--", lw=0.9)
    ax.text(2 ** 24 * 1.08, 2000, "2$^{24}$: FP32 stops\nrepresenting every integer", fontsize=8, va="top")
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel("Absolute position offset of the 4,096-token stream")
    ax.set_ylabel("Steady-state perplexity")
    ax.set_title("Immutable ring with absolute positions · Qwen2.5-1.5B · S4/W1024", fontsize=10)
    ax.grid(color="#dddddd", lw=0.6); ax.legend(frameon=False, fontsize=8.5, loc="upper left")
    fig.savefig(FIG / "fp32-phase-threshold.png", dpi=180); plt.close(fig)


def swamping():
    x = json.loads((EV / "rotation-swamping.json").read_text())
    om = np.array(x["omega"])
    fig, ax = plt.subplots(figsize=(7.4, 3.8), constrained_layout=True)
    for name, color, label in (("fp32_twiddle_bf16_store", "#b33428", "BF16 storage"),
                               ("fp32_twiddle_fp16_store", "#e28e22", "FP16 storage"),
                               ("fp32_twiddle_fp32_store", "#2257a6", "FP32 storage")):
        ax.plot(om, x["arms"][name]["achieved_rotation_fraction_at_256"], marker=".", color=color,
                label=label, lw=1.3)
    for thr, lab in ((2 ** -9, "BF16 half-ulp"), (2 ** -11, "FP16 half-ulp")):
        ax.axvline(thr, color="#606060", ls="--", lw=0.8)
        ax.text(thr * 1.1, 0.55, lab, fontsize=8, rotation=90)
    ax.set_xscale("log"); ax.set_ylim(-0.1, 1.15)
    ax.set_xlabel("RoPE pair frequency ω (rad/token)")
    ax.set_ylabel("Achieved / intended rotation after 256 shifts")
    ax.set_title("Rotation swamping under one-position rerotation (FP32 twiddle)", fontsize=10)
    ax.grid(color="#dddddd", lw=0.6); ax.legend(frameon=False, fontsize=8.5)
    fig.savefig(FIG / "rotation-swamping.png", dpi=180); plt.close(fig)


def speed():
    x = json.loads((EV / "free-wins-speed.json").read_text())
    rows = [r for r in x["decode"] if r["source"] == "speed-v2"] or [r for r in x["decode"] if r["source"] == "speed-v1"]
    fig, ax = plt.subplots(figsize=(7.4, 4.0), constrained_layout=True)
    style = {"rerotate_graph": ("#b33428", "FP32 rerotation (graph)"),
             "ring_graph": ("#188267", "Ring, SDPA (graph)"),
             "ring_graph_gqa": ("#2257a6", "Ring, GQA split-K (graph)"),
             "fusedpre_bf16_tab_graph": ("#7a4fb5", "Pre-RoPE BF16, fused rotate (graph)"),
             "fusedpre_q4b_tab_graph": ("#e28e22", "Pre-RoPE Q4+bias, fused (graph)")}
    for arm, (color, label) in style.items():
        rr = sorted([r for r in rows if r["arm"] == arm], key=lambda r: r["window"])
        if rr:
            ax.plot([r["window"] for r in rr], [r["ms_per_token_median"] for r in rr], marker="o", ms=4,
                    color=color, label=label, lw=1.6)
    ax.set_xscale("log", base=2)
    ax.set_xlabel("Recent-window tokens W"); ax.set_ylabel("ms / decoded token (batch 1)")
    ax.set_title("Steady-state decode · Qwen2.5-1.5B BF16 · RTX 4080 (idle)", fontsize=10)
    ax.grid(color="#dddddd", lw=0.6); ax.legend(frameon=False, fontsize=8.5)
    fig.savefig(FIG / "decode-speed-vs-window.png", dpi=180); plt.close(fig)


if __name__ == "__main__":
    offsets(); swamping(); speed()
    print("ok")
