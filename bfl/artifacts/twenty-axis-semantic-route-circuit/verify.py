from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).parent


def main() -> None:
    ledger = json.loads((ROOT / "circuit-panel-ledger.json").read_text())
    assert ledger["axis_count"] == 20
    assert ledger["route"] == ["joint.2", "joint.3", "joint.4", "single.0"]
    assert ledger["counts"] == {
        "carrier_candidate": 3,
        "carrier_certified": 11,
        "certified": 6,
        "unknown": 0,
    }
    rows = {row["axis_id"]: row for row in ledger["rows"]}
    assert len(rows) == 20
    for axis in ("lighting_dawn_sunset", "identity_cat_fox", "weather_clear_snowstorm"):
        assert rows[axis]["level"] == "certified"
        assert rows[axis]["gate_summary"]["passed"] == 9
        assert rows[axis]["gate_summary"]["failed"] == []
    assert rows["lighting_dawn_sunset"]["aggregate"]["min_target_progress"] >= 0.915
    assert rows["lighting_dawn_sunset"]["aggregate"]["max_route_ablation_progress"] <= 0.017

    promptless = json.loads((ROOT / "promptless-control-report.json").read_text())
    assert promptless["model"] == "black-forest-labs/FLUX.2-klein-4B"
    assert promptless["execution"]["device"] == "cuda"
    assert promptless["execution"]["elapsed_s"] < 70.0
    assert len(promptless["site_order"]) == 25

    print("twenty-axis-semantic-route-circuit: PASS")


if __name__ == "__main__":
    main()
