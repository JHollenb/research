from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).parent


def load(name: str) -> dict:
    return json.loads((ROOT / name).read_text())


def main() -> None:
    required = [
        "gap-report.json",
        "patch-report.json",
        "act-package.npz",
        "target-native.png",
        "target-act.png",
        "target-wrong-time.png",
        "target-zero-dose.png",
        "fresh-donor-free.png",
        "generalization-gate-results.md",
    ]
    for name in required:
        assert (ROOT / name).is_file(), name

    gap = load("gap-report.json")
    row = gap["paired_gap"]["by_condition"]["red_apples:5"]
    assert row["pairs"] == 8
    assert row["independent_base_exact_mean"] == 1.0
    assert row["independent_distilled_exact_mean"] == 0.5

    report = load("patch-report.json")
    package = report["act_package"]
    assert package["parameter_count"] == 55297
    assert package["package_bytes"] == 104044
    assert package["payload_dtype"] == "float16"
    assert package["rank"] == 8
    assert package["site"] == "joint.2"
    assert package["selected_gain"] == 2.0
    assert package["donor_payloads"] is False
    assert package["donor_logits"] is False
    assert package["prompt_lookup"] is False
    assert package["runtime_labels"] is False

    package_bytes = (ROOT / "act-package.npz").read_bytes()
    assert len(package_bytes) == package["package_bytes"]
    assert hashlib.sha256(package_bytes).hexdigest() == package["package_sha256"]

    assert report["target_records"]["act"]["evaluation"]["independent"]["exact"] == 1.0
    assert report["fresh_process"]["donor_disabled"] == "1"
    assert report["fresh_process"]["result"]["donor_path_unavailable"] is True
    assert report["fresh_process"]["result"]["evaluation"]["independent"]["exact"] == 1.0
    assert report["uninstall"]["pixel_bytes_exact"] is True
    assert report["consumer_closed_controller"]["accepted_gain"] == 2.0
    assert report["consumer_closed_controller"]["ledger_verified"] is True

    print("recipient-native-capability-patch: PASS")


if __name__ == "__main__":
    main()
