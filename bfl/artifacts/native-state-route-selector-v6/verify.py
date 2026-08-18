#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).parent
report = json.loads((ROOT / "report.json").read_text())
assert report.get("status") == "complete"
assert report["panel"]["row_count"] == 106
assert report["panel"]["fresh_green_family_holdout"] if "fresh_green_family_holdout" in report["panel"] else True
assert report["compiler"]["calibration_phase_present"] is True
assert report["compiler"]["calibration_uses_heldout_outcomes"] is False
assert report["compiler"]["family_disjoint_calibration_and_holdout"] is True
assert (ROOT / "ANALYSIS.md").is_file()
assert (ROOT / "run-receipt.json").is_file()
assert (ROOT / "selector-package.npz").stat().st_size > 1000
ledger = (ROOT / "source-ledger.md").read_text()
for needle in ("support multiplier `3.0`", "radius `8.115`", "both six-circle", "positive exactness `0/4`", "fixed `joint3`"):
    assert needle in ledger, needle
for name in ("heldout__green_circles_six__seed-7001__native.png", "heldout__green_squares_five__seed-7001__native.png", "heldout__green_triangles_three_negative__seed-7001__native.png"):
    assert (ROOT / name).stat().st_size > 1000, name
print("PASS native-state-route-selector-v6")
