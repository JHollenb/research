import json
from pathlib import Path


ROOT = Path(__file__).parent


def main() -> None:
    report = json.loads((ROOT / "report.json").read_text())
    assert "klein" in report["model"].lower()
    assert report["route"] == ["joint.2", "joint.3", "joint.4", "single.0"]
    assert report["pair_count"] == 3
    assert report["claim_boundary"]
    interaction = (ROOT / "interaction-residual-analysis.md").read_text()
    for value in ("0.9014", "0.3963", "0.5685"):
        assert value in interaction
    assert "-0.4010" in interaction or "−0.4010" in interaction
    for name in ("repair_route.png", "repair_half.png", "route_ablation.png", "wrong_axis_coiled_rope.png", "sham_norm_matched.png"):
        assert (ROOT / name).exists()
    print("typed-snake-topology-interaction: PASS")


if __name__ == "__main__":
    main()
