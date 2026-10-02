#!/usr/bin/env python3
"""Figure 8 for the rounding-placement paper: the B(x) training continuation,
MEAN OVER THREE DATA ORDERS (seeds 1234, 2, 3), in ONE process.

Panel 1: held val loss vs step, core arms, mean over 3 orders (shaded = min-max).
Panel 2: gap to the fp32 reference vs step, mean over 3 orders (shaded = min-max);
         this is the primary metric. The matched-precision bf16-vs-B(x) gap is the
         distance between the red and blue bands.
Panel 3: one-step gradient error along the trajectory (seed-1234 probe schedule,
         the only order probed at 0/100/300/600/999; the 0 and 999 endpoints
         replicate across all three orders).

Sources: ../../../saturn/experiments/2026-10-02-bx-training-continuation/results/
         {full6-s1234.json (job-fec87d0ed93a), core4-s2.json, core4-s3.json}
Run once:  python3 figures/make_fig8.py
"""
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RES = "../../../saturn/experiments/2026-10-02-bx-training-continuation/results"
ORDERS = {"1234": "full6-s1234.json", "2": "core4-s2.json", "3": "core4-s3.json"}
data = {k: json.load(open(f"{RES}/{v}")) for k, v in ORDERS.items()}

CORE = {
    "ref":       ("fp32 reference (A)",   "#333333", "o", "-"),
    "bf16":      ("plain bf16 (B)",       "#c0504d", "s", "-"),
    "bf16_Bx":   ("bf16 + B(x) (C)",      "#1f5a96", "D", "-"),
    "bf16_mean": ("bf16 + key-mean only (D)", "#2e8b57", "^", "--"),
}
TS = [0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]


def held(order, arm):
    return {p["t"]: p["val_loss"] for p in data[order]["arms"][arm]["held"]}


def mean_band(per_order):
    """per_order: list of dicts {t: value}. Return ts, mean, lo, hi over common ts."""
    ts, mu, lo, hi = [], [], [], []
    for t in TS:
        vals = [d[t] for d in per_order if t in d]
        if len(vals) == len(per_order):
            ts.append(t)
            mu.append(sum(vals) / len(vals))
            lo.append(min(vals))
            hi.append(max(vals))
    return ts, mu, lo, hi


fig, axes = plt.subplots(1, 3, figsize=(16, 4.6))

# -------- Panel 1: held loss, mean over 3 orders, min-max band
ax = axes[0]
for k, (lab, col, mk, ls) in CORE.items():
    per = [held(o, k) for o in ORDERS]
    ts, mu, lo, hi = mean_band(per)
    ax.plot(ts, mu, ls, color=col, marker=mk, ms=4, label=lab)
    ax.fill_between(ts, lo, hi, color=col, alpha=0.15, lw=0)
ax.set_xlabel("continuation step")
ax.set_ylabel("held val loss (fp32, nats/token)")
ax.set_title("Held-out loss, Pythia-160m step143000\ncontinued on WikiText-2 (lr=2e-5), 3 data orders")
ax.legend(fontsize=8)
ax.grid(alpha=0.3)

# -------- Panel 2: gap to fp32 reference, mean over 3 orders, min-max band
ax = axes[1]
for k, (lab, col, mk, ls) in CORE.items():
    if k == "ref":
        continue
    per = []
    for o in ORDERS:
        ref = held(o, "ref")
        arm = held(o, k)
        per.append({t: arm[t] - ref[t] for t in arm if t in ref})
    ts, mu, lo, hi = mean_band(per)
    ax.plot(ts, mu, ls, color=col, marker=mk, ms=4, label=lab)
    ax.fill_between(ts, lo, hi, color=col, alpha=0.15, lw=0)
ax.axhline(0, color="#333333", lw=1)
ax.set_xlabel("continuation step")
ax.set_ylabel("held loss - fp32 reference (nats/token)")
ax.set_title("Gap to the fp32 reference (primary metric)\nmean of 3 orders; shaded = min-max")
ax.legend(fontsize=8)
ax.grid(alpha=0.3)

# -------- Panel 3: one-step gradient error along trajectory (seed-1234 probe schedule)
ax = axes[2]
for k, (lab, col, mk, ls) in CORE.items():
    if k == "ref":
        continue
    pr = data["1234"]["arms"][k].get("probe", [])
    ts = [p["t"] for p in pr]
    ys = [p["global_rel"] * 100 for p in pr]
    ax.plot(ts, ys, ls, color=col, marker=mk, ms=4, label=lab)
ax.set_xlabel("continuation step")
ax.set_ylabel("one-step grad error vs fp32 ref (%)")
ax.set_yscale("log")
ax.set_title("One-step gradient error along the trajectory\n(seed 1234; 0 and 999 replicate across orders)")
ax.legend(fontsize=8)
ax.grid(alpha=0.3, which="both")

fig.suptitle("B(x) training continuation: gradient repair becomes a held-out loss benefit (3 data orders)",
             fontsize=12, fontweight="bold")
fig.tight_layout(rect=[0, 0, 1, 0.95])
fig.savefig("figures/bx-training-3order.png", dpi=150)
plt.close(fig)
print("wrote figures/bx-training-3order.png")
