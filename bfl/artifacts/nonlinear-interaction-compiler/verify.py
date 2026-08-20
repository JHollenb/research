#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).parent
mixer = json.loads((ROOT / "mixer-report.json").read_text())
interaction = json.loads((ROOT / "interaction-report.json").read_text())
assert mixer.get("status") == "raw_exploratory"
assert interaction.get("status") == "raw_exploratory"
for name in ("mixer-receipt.json", "interaction-receipt.json"):
    assert (ROOT / name).is_file(), name
ledger = (ROOT / "source-ledger.md").read_text()
for needle in ("0.735", "0.716", "0.894", "0.596", "32 proposals", "interaction only, no linear terms"):
    assert needle in ledger, needle
for name in ("pair-lighting__color_bfl_next__seed-52013__montage.png", "pair-lighting__color_bfl_next__seed-52013__linear.png", "pair-lighting__color_bfl_next__seed-52013__interaction_dose_1p00.png", "pair-lighting__color_bfl_next__seed-52013__native_ab.png"):
    assert (ROOT / name).stat().st_size > 1000, name
print("PASS nonlinear-interaction-compiler")
