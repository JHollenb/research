"""Render the bounded Qwen confirmation figure from retained analysis JSON."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
CONTEXT_SOURCE = ROOT / (
    "saturn/experiments/2026-10-01-scaffold-confirmation/qwen-predictive/"
    "results/qwen-predictive-held-20ede7e6e0c0/context-analysis.json"
)
DISORDER_SOURCE = ROOT / (
    "saturn/experiments/2026-10-01-scaffold-confirmation/qwen-predictive/"
    "results/qwen-predictive-followup-organization_1.0-c6a7ade0e793/"
    "followup-analysis.json"
)

OPERATIONS = ("identity", "color", "relation")
DOSES = (0.0, 0.05, 0.2, 1.0)
COLORS = {
    "identity": "#2C5F8A",
    "color": "#B35C2E",
    "relation": "#4D7A52",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_selected_data() -> dict:
    context = json.loads(CONTEXT_SOURCE.read_text())
    disorder = json.loads(DISORDER_SOURCE.read_text())

    panel_a_rows = [
        row
        for row in context["context_profile_summaries"]
        if row["operation"] in OPERATIONS
        and row["view"] == "native_competent_readout_applicable"
        and float(row["weight_dose"]) == 0.0
    ]
    panel_a_lookup = {row["operation"]: row for row in panel_a_rows}
    assert set(panel_a_lookup) == set(OPERATIONS)

    panel_a = {}
    for operation in OPERATIONS:
        row = panel_a_lookup[operation]
        panel_a[operation] = {
            "context_n": int(row["context_n"]),
            "binding_rows_included": int(row["binding_rows_included"]),
            "mapped_raw_rmse": float(row["mapped"]["raw_rmse_no_fit"]),
            "operation_blind_raw_rmse": float(
                row["operation_blind"]["raw_rmse_no_fit"]
            ),
        }

    panel_b_rows = [
        row
        for row in disorder["organization"]["same_four_context_summaries"]
        if row["operation"] in OPERATIONS and row["view"] == "all_rows"
    ]
    panel_b_lookup = {
        (row["operation"], float(row["weight_dose"])): row
        for row in panel_b_rows
    }
    assert set(panel_b_lookup) == {
        (operation, dose) for operation in OPERATIONS for dose in DOSES
    }

    panel_b = {}
    for operation in OPERATIONS:
        values = []
        for dose in DOSES:
            row = panel_b_lookup[(operation, dose)]
            assert int(row["context_n"]) == 4
            values.append(
                {
                    "dose": dose,
                    "context_n": int(row["context_n"]),
                    "binding_rows_included": int(row["binding_rows_included"]),
                    "mapped_signed_cosine": float(
                        row["mapped_signed_cosine_median"]
                    ),
                }
            )
        panel_b[operation] = values

    return {
        "schema": "scaffold-confirmation-figure-data-v1",
        "sources": [
            {
                "path": str(CONTEXT_SOURCE.relative_to(ROOT)),
                "sha256": digest(CONTEXT_SOURCE),
                "selected_record": (
                    "context_profile_summaries, dose=0, "
                    "view=native_competent_readout_applicable"
                ),
            },
            {
                "path": str(DISORDER_SOURCE.relative_to(ROOT)),
                "sha256": digest(DISORDER_SOURCE),
                "selected_record": (
                    "organization.same_four_context_summaries, view=all_rows"
                ),
            },
        ],
        "panel_a": {
            "metric": "raw_rmse_no_fit",
            "aggregation": (
                "Median across context-level mean profiles among contexts with "
                "registered native competence/readout applicability; no CI."
            ),
            "scope": (
                "Frozen held-context profile. Identity n=4 contexts; color and "
                "relation n=8 context combinations. The eight combinations are "
                "2 lexical sets x 2 templates x 2 orders, not eight independent "
                "lexical worlds."
            ),
            "operations": panel_a,
        },
        "panel_b": {
            "metric": "mapped_signed_cosine_median",
            "aggregation": (
                "Median across the same four context-level mean profiles at each "
                "dose, all-row dose-matched summary; no CI."
            ),
            "scope": (
                "Separately sealed post-held exploratory permutation of output "
                "rows in L22/L23 v_proj. The 100% arm permutes all 256 output "
                "rows. It is not a chronological training assay or a whole-model "
                "weight permutation, and native competence falls at strong dose."
            ),
            "operations": panel_b,
        },
    }


def render(data: dict) -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 9,
            "axes.titlesize": 11,
            "axes.labelsize": 9.5,
            "legend.fontsize": 8.5,
            "xtick.labelsize": 9,
            "ytick.labelsize": 9,
            "svg.fonttype": "none",
        }
    )
    fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(11.6, 5.25))
    fig.subplots_adjust(left=0.075, right=0.985, top=0.775, bottom=0.255, wspace=0.28)

    # Panel A: competent context-level prediction error.
    x = np.arange(len(OPERATIONS))
    width = 0.34
    mapped = [data["panel_a"]["operations"][op]["mapped_raw_rmse"] for op in OPERATIONS]
    blind = [
        data["panel_a"]["operations"][op]["operation_blind_raw_rmse"]
        for op in OPERATIONS
    ]
    bars_mapped = ax_a.bar(
        x - width / 2,
        mapped,
        width,
        color="#396A93",
        edgecolor="white",
        linewidth=0.6,
        label="Mapped profile",
    )
    bars_blind = ax_a.bar(
        x + width / 2,
        blind,
        width,
        color="#B9BDC3",
        edgecolor="#72767C",
        linewidth=0.55,
        label="Operation-blind",
    )
    for bars in (bars_mapped, bars_blind):
        for bar in bars:
            ax_a.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.005,
                f"{bar.get_height():.3f}",
                ha="center",
                va="bottom",
                fontsize=8,
            )
    for index, operation in enumerate(OPERATIONS):
        n = data["panel_a"]["operations"][operation]["context_n"]
        ax_a.text(index, -0.025, f"n={n} contexts", ha="center", va="top", fontsize=8)
    ax_a.set_xticks(x, [op.capitalize() for op in OPERATIONS])
    ax_a.set_ylim(0, 0.245)
    ax_a.set_ylabel("Raw RMSE (lower is better)")
    ax_a.text(
        0,
        1.17,
        "A   Frozen profile prediction",
        transform=ax_a.transAxes,
        fontsize=11,
        fontweight="bold",
    )
    ax_a.text(
        0,
        1.075,
        "Competent context summaries · median across context means",
        transform=ax_a.transAxes,
        fontsize=8.5,
        color="#4A4A4A",
    )
    ax_a.legend(frameon=False, loc="upper right")

    # Panel B: all-row, same-four-context disorder trajectory.
    dose_x = np.arange(len(DOSES))
    for operation in OPERATIONS:
        values = [
            row["mapped_signed_cosine"]
            for row in data["panel_b"]["operations"][operation]
        ]
        ax_b.plot(
            dose_x,
            values,
            marker="o",
            markersize=5.2,
            linewidth=2.0,
            color=COLORS[operation],
            label=operation.capitalize(),
        )
        ax_b.text(
            dose_x[-1] + 0.06,
            values[-1],
            f"{values[-1]:.3f}",
            va="center",
            fontsize=8,
            color=COLORS[operation],
        )
    ax_b.axvspan(2.5, 3.5, color="#D9A441", alpha=0.10, zorder=0)
    ax_b.text(
        3,
        0.76,
        "strong disorder\ncompetence falls",
        ha="center",
        va="center",
        fontsize=8,
        color="#684D16",
    )
    ax_b.set_xlim(-0.15, 3.45)
    ax_b.set_ylim(0, 1.02)
    ax_b.set_xticks(dose_x, ["0%", "5%", "20%", "100%"])
    ax_b.set_xlabel("L22/L23 value-projection output rows permuted")
    ax_b.set_ylabel("Mapped signed cosine (higher is closer)")
    ax_b.text(
        0,
        1.17,
        "B   Final-weight correspondence",
        transform=ax_b.transAxes,
        fontsize=11,
        fontweight="bold",
    )
    ax_b.text(
        0,
        1.075,
        "Post-held exploratory · same 4 opened contexts · all rows",
        transform=ax_b.transAxes,
        fontsize=8.5,
        color="#4A4A4A",
    )
    ax_b.legend(frameon=False, loc="lower left")

    for ax in (ax_a, ax_b):
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="y", color="#D7D9DC", linewidth=0.65, alpha=0.7)
        ax.set_axisbelow(True)

    fig.suptitle(
        "Prospective relation prediction and sensitivity to strong projection disorder",
        fontsize=14,
        fontweight="bold",
        y=0.955,
    )
    fig.text(
        0.075,
        0.105,
        "A: context combinations are lexical set × template × order; they are not independent lexical worlds. "
        "B: medians over n=4 contexts at each dose; no confidence intervals. The post-held disorder assay "
        "tests final L22/L23 value-projection correspondence, not training chronology or whole-model weights.",
        ha="left",
        va="bottom",
        fontsize=8.1,
        color="#404040",
        wrap=True,
    )
    fig.savefig(OUT / "confirmation-results.svg")
    fig.savefig(OUT / "confirmation-results.png", dpi=220)
    plt.close(fig)


if __name__ == "__main__":
    selected = load_selected_data()
    (OUT / "confirmation-results-data.json").write_text(
        json.dumps(selected, indent=2) + "\n"
    )
    render(selected)
    print("Rendered confirmation-results.svg/png from two retained analysis files.")
