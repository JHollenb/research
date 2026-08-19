#!/usr/bin/env python3
"""Verify the copied four-specimen Real Hotpatch Cinema evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).parent
REPORT = ROOT / "replication-report.json"


def main() -> int:
    report = json.loads(REPORT.read_text())
    assert report["status"] == "PASS"
    assert report["aggregate"]["passing_specimens"] == 4
    assert report["aggregate"]["total_specimens"] == 4
    assert report["aggregate"]["gates"]["all_rollbacks_exact"] is True
    assert report["aggregate"]["gates"]["both_axes_represented"] is True
    assert report["execution"]["logical_batched_suffixes"] == 40
    assert report["execution"]["exact_scalar_suffixes"] == 20
    assert report["execution"]["model_loads"] == 1

    early = []
    late = []
    hostile_own = []
    hostile_target = []
    for specimen in report["specimens"]:
        assert specimen["passed"] is True
        assert all(specimen["gates"].values())
        summary = specimen["summary"]
        early.append(summary["cut0_dose_progress"][-1])
        late.append(summary["cut2_correct_full_progress"])
        hostile_own.append(summary["cut0_hostile_own_progress"])
        hostile_target.append(summary["cut0_hostile_target_progress"])

    assert min(early) >= 0.904
    assert max(early) <= 0.971
    assert min(late) >= 0.095
    assert max(late) <= 0.359
    assert min(hostile_own) >= 0.925
    assert max(hostile_own) <= 0.954
    assert max(hostile_target) < -0.40
    print("PASS: four specimens, native-consumer controls, timing separation, and exact rollback verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
