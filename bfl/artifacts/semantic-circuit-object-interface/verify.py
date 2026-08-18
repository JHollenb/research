import json
from pathlib import Path


ROOT = Path(__file__).parent


def require_files(names):
    for name in names:
        path = ROOT / name
        assert path.is_file() and path.stat().st_size > 100, name


def main() -> None:
    ledger = json.loads((ROOT / "synthesis-ledger.json").read_text())
    inverse = json.loads((ROOT / "inverse-object-map.json").read_text())
    manifest = json.loads((ROOT / "object-manifest-proof.json").read_text())
    isolation = json.loads((ROOT / "isolation-summary.json").read_text())

    assert ledger["route"] == ["joint.2", "joint.3", "joint.4", "single.0"]
    assert ledger["seeds"] == [7217, 31337]
    assert ledger["symbol_creation"]["exact_noop_rgb_mad"] == 0.0
    assert inverse["results"]["fox_red_to_white_progress"] == [0.92, 0.94]
    assert inverse["results"]["ball_blue_to_green_progress"] == [0.77, 0.65]
    assert manifest["readback_fingerprint_matches"] is True
    assert manifest["unit_tests_passed"] == "11/11"
    assert isolation["native_route_isolation_progress"]["ball_seed_31337"] == 0.9968
    assert ledger["value_level_debugger"]["mug_roi_mad"] == [59.8, 65.0]

    require_files([
        "README.md",
        "circuit-panel-ledger.json",
        "circuit-panel-proof-sheet.png",
        "route-certificate.json",
        "inverse-object-proof.png",
        "object-registry-proof.png",
        "object-manifest-proof.json",
        "wrong-address-proof.png",
        "dose-proof.png",
        "isolation-proof.png",
        "heldout-algebra-report.json",
        "heldout-catmug-proof.png",
        "heldout-parrotbike-proof.png",
        "displacement-strip.png",
        "cross-scene-port-proof.png",
        "pose-isolation-proof.png",
        "role-backfill-proof.png",
        "value-debugger-report.json",
        "value-write-proof.png",
        "register-semantics-proof.png",
        "subject-prior-proof.png",
        "value-debugger-proof-sheet.png",
    ])
    print("semantic-circuit-object-interface: PASS")


if __name__ == "__main__":
    main()
