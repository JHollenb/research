#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).parent
result = json.loads((ROOT / "result.json").read_text())
assert result["causal_control_contract"]["native_noop_is_separate_pipeline_call"] is True
assert result["causal_control_contract"]["wrong_source_has_native_wrong_prompt_reference"] is True
assert result["causal_control_contract"]["zero_is_distinct_from_noop"] is True
assert len(result["causal_controls"]["examples"]) == 4
assert result["causal_controls"]["seeds"] == [4242, 9001]
assert result["image_metrics"]["held_out_mean_abs_delta"] > 0
assert result["embedding_metrics"]["held_out"]["token_cosine"] < result["embedding_metrics"]["train"]["token_cosine"]
assert (ROOT / "artifact-manifest.json").is_file()
assert (ROOT / "run-receipt.json").is_file()
ledger = (ROOT / "source-ledger.md").read_text()
for needle in ("65.80", "95.27", "114.71", "65.57", "max MAD 0", "8 × 4 = 32", "control pipeline calls"):
    assert needle in ledger, needle
for name in ("contact-sheet.png", "00_held-out-lighthouse-from-corgi_native.png", "00_held-out-lighthouse-from-corgi_adapted.png", "00_held-out-lighthouse-from-corgi_zero.png", "00_held-out-lighthouse-from-corgi_wrong_source.png"):
    assert (ROOT / name).stat().st_size > 1000, name
print("PASS flux1-conditioner-causal-controls")
