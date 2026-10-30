"""Render the historical selector timing figure without running a model.

Run with --report PATH to derive the plot data from the original six-model
report, or with no arguments to render the checked-in data snapshot.
"""

import argparse
import hashlib
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, FuncFormatter


HERE = Path(__file__).resolve().parent
DATA = HERE / "selector-performance-data.json"
NAMES = [
    ("native", "Native CPU process"),
    ("pan_isa", "Original PAN selector"),
    ("nn", "NN selector"),
    ("fieldlm", "FieldLM selector"),
    ("spf_transformer", "SPF memory selector"),
    ("mamba", "Mamba selector"),
    ("hydra", "Hydra selector"),
]


def extract(report_path):
    raw = report_path.read_bytes()
    report = json.loads(raw)
    rows = []
    for key, label in NAMES:
        entry = report["timings"][key]["counter-1024"]
        metric = "wall_s" if key == "native" else "program_stop_s"
        timing = entry[metric]
        rows.append({
            "key": key,
            "label": label,
            "source_metric": metric,
            "median_ms": 1000 * timing["median"],
            "min_ms": 1000 * timing["min"],
            "max_ms": 1000 * timing["max"],
            "n": timing["n"],
            "correct": entry["correct"],
            "total": entry["total"],
        })
    result = {
        "source": "isa/outputs/ssm-native-report/report.json",
        "source_sha256": hashlib.sha256(raw).hexdigest(),
        "case": "counter-1024",
        "host": report["host"],
        "backend": report["backend"],
        "jobs": report["jobs"],
        "seeds": report["seeds"],
        "scope": report["scope"],
        "rows": rows,
    }
    DATA.write_text(json.dumps(result, indent=2) + "\n")
    return result


def render(data):
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11})
    fig, ax = plt.subplots(figsize=(10.5, 6.2))
    fig.subplots_adjust(left=0.25, right=0.94, top=0.79, bottom=0.34)
    for y, row in enumerate(data["rows"]):
        color = "#147D78" if row["key"] == "native" else "#35669A"
        ax.hlines(y, row["min_ms"], row["max_ms"], color=color, linewidth=2)
        ax.plot(row["median_ms"], y, "o", color=color, markersize=7)
        ax.annotate(
            f'{row["median_ms"]:.3f} ms',
            (row["max_ms"], y), xytext=(9, 0),
            textcoords="offset points", va="center", fontsize=10, color=color,
        )
    ax.set_xscale("log")
    ax.set_xlim(0.08, 1600)
    ax.set_ylim(len(data["rows"]) - 0.5, -0.5)
    ax.set_yticks(range(len(data["rows"])), [r["label"] for r in data["rows"]])
    ax.xaxis.set_major_locator(FixedLocator([0.1, 1, 10, 100, 1000]))
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:g}"))
    ax.set_xlabel("Counter completion wall time in milliseconds · logarithmic scale", labelpad=12)
    ax.grid(axis="x", which="major", color="#DFE5EC", linewidth=0.8)
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(axis="both", length=0, pad=8)
    fig.text(0.03, 0.95, "Finishing the same 1,024-instruction counter", fontsize=18, weight="bold")
    fig.text(0.03, 0.895, "Beast CPU · one model thread · six-model selector study", fontsize=12, color="#455568")
    fig.text(
        0.03, 0.06,
        "Points show medians; lines show observed minimum to maximum. Models completed 9/9 counter trials each; native 60/60.\n"
        "Model timing includes warm ELF setup and execution to stop. Native timing includes process launch, execution and wait.\n"
        "Model cold start and diagnostic serialization are excluded. Correct counter output does not establish full hardware-state parity.",
        fontsize=9, color="#455568", linespacing=1.6,
    )
    for extension in ("svg", "png"):
        fig.savefig(HERE / f"selector-performance.{extension}", dpi=180, facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    render(extract(args.report) if args.report else json.loads(DATA.read_text()))
