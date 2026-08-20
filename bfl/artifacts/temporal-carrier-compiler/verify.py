#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).parent
report = json.loads((ROOT / "report.json").read_text())
assert report.get("status") == "raw_exploratory"
assert (ROOT / "run-receipt.json").is_file()
ledger = (ROOT / "source-ledger.md").read_text()
for needle in ("joint.2 → step 3 → image", "0.035", "0.722", "0.545", "0.717", "0.978", "wrong-time"):
    assert needle in ledger, needle
for name in ("lighting__relation__seed-52013.png", "lighting__relation__seed-52019.png", "orientation__relation__seed-52013.png", "orientation__relation__seed-52019.png"):
    assert (ROOT / name).stat().st_size > 1000, name
print("PASS temporal-carrier-compiler")

