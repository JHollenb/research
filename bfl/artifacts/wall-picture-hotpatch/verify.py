#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).parent
report = json.loads((ROOT / "report.json").read_text())
certificate = json.loads((ROOT / "certificate.json").read_text())
assert certificate.get("status") == "admitted"
assert report.get("status") in {"PASS", "EXPLORATORY", "complete", "admitted"}
assert (ROOT / "run-receipt.json").is_file()
ledger = (ROOT / "wall-picture-source.md").read_text() + (ROOT / "hotpatch-extended-source.md").read_text()
for needle in ("1.000–1.000", "0.916–0.969", "1.000` for `4/4", "4/4", "protected-picture pixel-region write"):
    assert needle in ledger, needle
for name in ("gallery-seed4242__source.png", "gallery-seed4242__cinema.png", "gallery-seed4242__cut0_target_dose100.png", "gallery-seed4242__opposite_donor.png", "gallery-seed4242__cut2_sham_dose100.png"):
    assert (ROOT / name).stat().st_size > 1000, name
print("PASS wall-picture-hotpatch")
