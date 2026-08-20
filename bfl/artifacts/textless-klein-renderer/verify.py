#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).parent
report = json.loads((ROOT / "report.json").read_text())
assert report.get("status") == "raw_exploratory"
assert (ROOT / "run-receipt.json").is_file()
ledger = (ROOT / "source-ledger.md").read_text()
for needle in ("-0.299", "0.024", "0.733", "1.000", "0.364", "0.984", "zero-dose"):
    assert needle in ledger, needle
for name in ("scene_graph_holdout.png", "robot_json_holdout.png"):
    assert (ROOT / name).stat().st_size > 1000, name
print("PASS textless-klein-renderer")

