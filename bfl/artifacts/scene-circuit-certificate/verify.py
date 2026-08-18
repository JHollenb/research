#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).parent
report = json.loads((ROOT / "report.json").read_text())
certificate = json.loads((ROOT / "certificate.json").read_text())
assert certificate.get("status") == "certified"
assert report.get("status") == "raw"
gates = {g["id"]: g for g in certificate["gates"]}
assert gates["reproducibility"]["passed"] is True
assert gates["sufficiency"]["passed"] is True
assert gates["necessity"]["passed"] is True
assert (ROOT / "certificate.md").is_file()
assert (ROOT / "run-receipt.json").is_file()
assert abs(gates["sufficiency"]["observed"]["minimum_scene_progress"] - 0.9132605915813907) < 1e-12
assert abs(gates["necessity"]["observed"]["maximum_route_ablation_scene_progress"] - 0.022478059397213257) < 1e-12
assert abs(gates["specificity_wrong_axis"]["observed"]["maximum_wrong_color_scene_progress"] + 0.4303132839954793) < 1e-12
assert abs(gates["specificity_sham"]["observed"]["maximum_sham_scene_progress"] - 0.10859346469260778) < 1e-12
assert abs(gates["mediation"]["observed"]["minimum_rescue_fraction"] - 0.7704782254031485) < 1e-12
assert abs(gates["consumer_continuation"]["observed"]["minimum_scene_return_progress"] - 0.9823917150497437) < 1e-12
assert abs(gates["consumer_continuation"]["observed"]["minimum_scene_return_alignment"] - 0.9708396196365356) < 1e-12
for name in ("seed-4242__source.png", "seed-4242__montage.png", "seed-4242__scene_dose_100.png", "seed-4242__wrong_color_full.png", "seed-4242__route_ablation.png", "seed-4242__sham_full.png", "seed-9001__montage.png"):
    assert (ROOT / name).stat().st_size > 1000, name
print("PASS scene-circuit-certificate")
