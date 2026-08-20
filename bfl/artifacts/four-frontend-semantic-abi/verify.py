#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).parent
report = json.loads((ROOT / "report.json").read_text())
assert report.get("status") == "exploratory"
for name in ("run-receipt.json", "analysis.md"):
    assert (ROOT / name).is_file(), name
ledger = (ROOT / "source-ledger.md").read_text()
for needle in ("72/72", "0.821", "0.935", "semantic-token", "intersections rescued almost nothing", "one resident Klein load"):
    assert needle in ledger, needle
for name in ("baseline_qwen_a.png", "baseline_smol_a.png", "baseline_mamba_a.png", "smol_positive_full_site_donor.png", "mamba_positive_full_site_donor.png", "smol_selected_site_all_steps.png", "mamba_selected_site_all_steps.png", "compact_proof_smol_norm_matched_axis_sham.png"):
    assert (ROOT / name).stat().st_size > 1000, name
print("PASS four-frontend-semantic-abi")
