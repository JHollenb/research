import json
from pathlib import Path


ROOT = Path(__file__).parent


def require_files(names):
    for name in names:
        path = ROOT / name
        assert path.is_file() and path.stat().st_size > 1000, name


def main() -> None:
    stage1 = json.loads((ROOT / "stage-1-inverse-map.json").read_text())
    stage2 = json.loads((ROOT / "stage-2-edit-battery.json").read_text())
    manifest = json.loads((ROOT / "manifest-proof.json").read_text())
    deepmap = json.loads((ROOT / "stage-3-deepmap-summary.json").read_text())
    isolation = json.loads((ROOT / "stage-3-isolation-summary.json").read_text())

    assert stage1["route"] == ["joint.2", "joint.3", "joint.4", "single.0"]
    assert stage1["results"]["exact_noop_rgb_mad"] == 0.0
    assert stage1["results"]["fox_red_to_white_progress"] == [0.92, 0.94]
    assert stage2["results"]["ball_to_blue_cube"] == "pass on both seeds"
    assert stage2["results"]["occlusion_flip"] == [0.944, 0.951]
    assert manifest["readback_fingerprint_matches"] is True
    assert manifest["unit_tests_passed"] == "11/11"
    assert deepmap["conditioner_depth"]["layers_profiled"] == 36
    assert deepmap["conditioner_depth"]["final_layer_locality_ratio"]["ball_color_blue_to_green"] == 17.2
    assert isolation["native_route_isolation_progress"]["ball_seed_31337"] == 0.9968

    require_files([
        "stage-1-run-receipt.json",
        "stage-1-scene-proof-sheet.png",
        "stage-2-registry-run-receipt.json",
        "stage-2-source-address-registry.json",
        "stage-2-registry-proof-sheet.png",
        "stage-2-move-layering-proof-sheet.png",
        "stage-3-deepmap-run-receipt.json",
        "stage-3-deepmap-proof-seed7217.png",
        "stage-3-deepmap-proof-seed31337.png",
        "stage-3-dose-seed7217.png",
        "stage-3-wrong-address-seed7217.png",
        "stage-3-isolation-run-receipt.json",
        "stage-3-isolation-proof-seed7217.png",
        "stage-3-isolation-proof-seed31337.png",
        "stage-3-fox-isolation-seed7217.png",
        "stage-3-ball-isolation-seed7217.png",
    ])
    print("objects-debugger-io-structs-stress-isolation: PASS")


if __name__ == "__main__":
    main()
