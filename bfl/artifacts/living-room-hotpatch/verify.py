#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).parent
report = json.loads((ROOT / "report.json").read_text())
certificate = json.loads((ROOT / "certificate.json").read_text())
assert certificate.get("status") == "admitted"
assert report.get("status") in {"PASS", "EXPLORATORY", "complete", "admitted"}
assert (ROOT / "run-receipt.json").is_file()
ledger = (ROOT / "source-ledger.md").read_text()
for needle in ("0.943–0.975", "0.943–0.980", "0.766–0.871", "4/4", "two feet", "-0.014–0.043"):
    assert needle in ledger, needle
for name in ("controlled-seed4242__source.png", "controlled-seed4242__cinema.png", "controlled-seed4242__cut0_target_dose100.png", "controlled-seed4242__opposite_donor.png", "controlled-seed4242__cut2_sham_dose100.png"):
    assert (ROOT / name).stat().st_size > 1000, name
print("PASS living-room-hotpatch")
