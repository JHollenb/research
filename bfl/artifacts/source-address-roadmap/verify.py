#!/usr/bin/env python3
"""Verify the copied SourceAddress roadmap and self-debugging evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).parent


def main() -> int:
    matrix = json.loads((ROOT / "source-address-roadmap-matrix.json").read_text())
    assert matrix["status"] == "bounded-development-matrix-complete"
    assert matrix["terminal_claim"] is False
    pythia = matrix["pythia_step512"]
    assert pythia["native_consumer_accuracy"] == 3 / 128
    assert pythia["fixed_consumer_accuracy"] == 12 / 128
    assert pythia["learned_consumer_accuracy"] == 59 / 128
    assert pythia["oracle_consumer_accuracy"] == 78 / 128
    assert matrix["fresh_alphabet"]["payload_bottleneck"] is True
    assert matrix["fresh_alphabet"]["source_zero_native_exact"] is True
    assert matrix["report_custody_verified"] is True

    qwen = {row["family"]: row for row in matrix["natural_language_cross_family"]}
    assert qwen["qwen2"]["fresh_template"]["native_cosine_accuracy"] == 1.0
    assert qwen["qwen3"]["fresh_template"]["native_cosine_accuracy"] == 1.0
    assert len(matrix["cross_family_direct_package_checks"]) == 2
    assert all(item["rejected"] for item in matrix["cross_family_direct_package_checks"])

    verification = json.loads((ROOT / "self-debugging-verification.json").read_text())
    assert verification["status"] == "passed"
    assert all(verification["checks"].values())
    trial = verification["sealed_trial"]
    assert trial["native_correct"] == 5
    assert trial["fixed_correct"] == 13
    assert trial["learned_correct"] == 92
    assert trial["oracle_correct"] == 105
    assert trial["wrong_source_correct"] == 1
    assert trial["random_address_correct"] == 11
    assert trial["source_zero_correct"] == 5
    assert trial["address_correct"] == 113
    print("PASS: SourceAddress matrix, family-local rejection, payload diagnosis, and sealed trial verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
