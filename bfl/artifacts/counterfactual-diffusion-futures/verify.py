from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).parent


def main() -> None:
    report = json.loads((ROOT / "replication-report.json").read_text())
    assert report["aggregate"]["passing_specimens"] == 4
    assert report["aggregate"]["total_specimens"] == 4
    assert report["aggregate"]["passing_fraction"] == 1.0
    assert report["aggregate"]["gates"]["all_rollbacks_exact"] is True
    assert report["execution"]["logical_batched_suffixes"] == 40
    assert report["execution"]["physical_batched_suffix_calls"] == 8
    assert report["execution"]["exact_scalar_suffixes"] == 20

    rows = {row["id"]: row for row in report["specimens"]}
    assert set(rows) == {
        "scene-seed9001",
        "scene-seed1337",
        "subject-seed4242",
        "subject-seed9001",
    }
    for row in rows.values():
        assert row["passed"] is True
        assert all(row["rollback"].values())
        summary = row["summary"]
        assert summary["cut0_dose_progress"][-1] >= 0.904
        assert summary["cut2_correct_full_progress"] <= 0.359
        assert summary["cut0_hostile_own_progress"] >= 0.925
        assert summary["cut0_hostile_target_progress"] <= -0.404

    print("counterfactual-diffusion-futures: PASS")


if __name__ == "__main__":
    main()
