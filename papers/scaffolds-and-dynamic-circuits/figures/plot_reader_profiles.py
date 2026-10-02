"""Render the paper's reader profile figure from the retained native-cut CSV."""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[4]
SOURCE = ROOT / "saturn/experiments/2026-10-01-qwen-head-edge-topology/analysis/single_cuts.csv"
OUT = Path(__file__).resolve().parent
rows = list(csv.DictReader(SOURCE.open()))
coordinates = [(layer, head, component) for layer in range(22, 28)
               for head in range(2) for component in ("key", "value")]
operations = ("identity", "color", "relation")
colors = ("#245b8f", "#ad542a", "#567943")
profiles = {}
fig, axes = plt.subplots(3, 1, figsize=(12, 8), sharex=True, layout="constrained")
for ax, operation, color in zip(axes, operations, colors):
    by_binding = []
    for binding in (0, 1):
        matches = [r for r in rows if r["operation"] == operation
                   and int(r["logical_index"]) == binding
                   and r["components"] in ("key", "value")]
        lookup = {(int(r["layer"]), int(r["kv_head"]), r["components"]):
                  float(r["delta_target_logprob"]) for r in matches}
        assert len(lookup) == 24, (operation, binding, len(lookup))
        by_binding.append(np.array([lookup[c] for c in coordinates]))
    mean = np.mean(by_binding, axis=0)
    profiles[operation] = {f"L{l}/KV{h}/{c}": float(v)
                           for (l, h, c), v in zip(coordinates, mean)}
    ax.axhline(0, color="#333333", lw=.7)
    ax.bar(np.arange(24), mean, color=color, alpha=.78, label="Mean of two queried bindings")
    ax.plot(np.arange(24), by_binding[0], ".", color="#181818", ms=4, label="Binding 0")
    ax.plot(np.arange(24), by_binding[1], "x", color="#181818", ms=4, label="Binding 1")
    for index in (5, 3):
        # L23/KV0/V and L22/KV1/V, respectively.
        ax.axvspan(index - .43, index + .43, color="#e0b54c", alpha=.22, zorder=0)
    for split in (3.5, 7.5, 11.5, 15.5, 19.5):
        ax.axvline(split, color="#b8b8b8", lw=.6)
    ax.set_title(operation.capitalize(), loc="left", fontsize=12)
    ax.set_ylabel("Change in target\nlog probability (nats)")
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", alpha=.15)
axes[0].legend(loc="lower left", fontsize=8, ncol=3)
axes[-1].set_xticks(np.arange(24), [f"L{l}\nKV{h} {'K' if c == 'key' else 'V'}"
                                   for l, h, c in coordinates], fontsize=8)
axes[-1].set_xlabel("Stored K/V coordinate; single-coordinate donor replacement")
fig.suptitle("Shared reader coordinates with operation-specific causal weights", fontsize=15)
fig.savefig(OUT / "reader-profiles.svg")
fig.savefig(OUT / "reader-profiles.png", dpi=160)
plt.close(fig)
(OUT / "reader-profiles-data.json").write_text(json.dumps({
    "source": str(SOURCE.relative_to(ROOT)),
    "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    "scope": "One Qwen2.5-1.5B checkpoint, one scene/order; three operations, two bindings.",
    "metric": "delta_target_logprob",
    "aggregation": "Arithmetic mean of two paired binding profiles; points show both, no sampling-error bars.",
    "profiles": profiles,
}, indent=2) + "\n")
print("Rendered 3 operations × 24 coordinates × 2 bindings from retained measurements.")
