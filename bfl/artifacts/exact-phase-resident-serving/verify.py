from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).parent


def load(name: str) -> dict:
    return json.loads((ROOT / name).read_text())


def check_mrun_receipt(name: str, *, state: str, returncode: int, status: str) -> dict:
    receipt = load(name)
    assert receipt["mrun_state"] == state, name
    result = receipt["mrun_result"]
    assert result["returncode"] == returncode, name
    assert result["status"] == status, name
    return receipt


def main() -> None:
    phase = load("phase-parity-receipt.json")
    assert phase["model_id"] == "flux2-klein-4b"
    assert phase["parity_pass"] is True
    assert len(phase["parity"]) == 8
    assert all(row["pixel_equal"] and row["png_equal"] for row in phase["parity"])
    assert phase["speedup_per_image"] == 10.66
    assert phase["speedup_end_to_end"] == 6.25

    cheap = load("cheap-deep-replay-receipt.json")
    assert cheap["loop_parity_rel"] == 0.0
    assert len(cheap["per_k"]) == 6
    assert all(row["cheap_exact_rel"] == 0.0 for row in cheap["per_k"])
    assert all(row["edit_exact_rel"] == 0.0 for row in cheap["per_k"])
    assert max(row["speedup"] for row in cheap["per_k"]) >= 7.99

    cache = load("edit-cache-receipt.json")
    summary = cache["summary"]
    assert summary["reference_reused_count"] == 4
    assert summary["native_vs_replay_exact_count"] == 4
    assert summary["native_vs_replay_mean_cosine"] == 1.0
    assert summary["cache_hit_speedup_median"] > 4000.0
    assert cache["cache_stats"]["hits"] == 4
    assert cache["cache_stats"]["invalidations"] == 4

    # Cross-model phase campaign: the failed receipts are retained because their
    # image evidence was either recovered or superseded by the corrected run.
    check_mrun_receipt(
        "run-receipt.phase.job-4bc506e9fe64.json",
        state="failed",
        returncode=3,
        status="failed",
    )
    check_mrun_receipt(
        "run-receipt.phase.job-6a7f7b0603dd.json",
        state="succeeded",
        returncode=0,
        status="ok",
    )
    check_mrun_receipt(
        "run-receipt.phase.job-271e7732c430.json",
        state="failed",
        returncode=3,
        status="failed",
    )
    check_mrun_receipt(
        "run-receipt.phase.job-4da6fc7c4238.json",
        state="succeeded",
        returncode=0,
        status="ok",
    )

    # Cross-model edit-reuse campaign: plain-Klein cells are represented by the
    # successful corrected receipt; the other statuses are intentional findings.
    check_mrun_receipt(
        "run-receipt.edit.job-d6832f02cdf2.json",
        state="failed",
        returncode=3,
        status="failed",
    )
    check_mrun_receipt(
        "run-receipt.edit.job-df22ad4e5c17.json",
        state="succeeded",
        returncode=0,
        status="ok",
    )
    check_mrun_receipt(
        "run-receipt.edit.job-981b01d2de66.json",
        state="failed",
        returncode=1,
        status="failed",
    )
    check_mrun_receipt(
        "run-receipt.edit.job-86f2ae8e1d0a.json",
        state="failed",
        returncode=1,
        status="failed",
    )

    for name in (
        "phase-parity-crossmodel-analysis.md",
        "edit-reuse-crossmodel-analysis.md",
    ):
        assert (ROOT / name).exists(), name

    print("exact-phase-resident-serving: PASS")


if __name__ == "__main__":
    main()
