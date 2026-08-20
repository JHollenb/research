#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).parent

def load(name):
    p = ROOT / name
    assert p.is_file(), f"missing {name}"
    return json.loads(p.read_text())

base = load("base-capture-report.json")
repair = load("distilled-repair-report.json")
assert base.get("status") == "complete"
assert repair.get("status") == "raw_exploratory"
assert (ROOT / "base-capture-receipt.json").is_file()
assert (ROOT / "distilled-repair-receipt.json").is_file()
ledger = (ROOT / "source-ledger.md").read_text()
for needle in ("joint.2 → step 0 → text", "1/4", "blue circles", "32 candidate seams"):
    assert needle in ledger, needle
for name in ("red_squares_4__seed-31337.png", "red_squares_4__seed-31339.png", "blue_circles_6__seed-31337.png", "blue_circles_6__seed-31339.png"):
    assert (ROOT / name).stat().st_size > 1000, name
print("PASS klein-seam-bisection")

