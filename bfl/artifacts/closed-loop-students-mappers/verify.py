import json
from pathlib import Path


ROOT = Path(__file__).parent


def main() -> None:
    mapper = json.loads((ROOT / "mapper-complete-v3.json").read_text())
    mapper_text = (ROOT / "mapper-complete-v3.json").read_text()
    assert "3768459" in mapper_text
    assert "0.9999981638" in mapper_text or "0.999998163845" in mapper_text
    assert "0.750672" in mapper_text and "0.066238" in mapper_text
    trajectory = (ROOT / "full-trajectory.json").read_text()
    assert "0.878103" in trajectory and "0.743758" in trajectory
    assert "0.913190" in trajectory and "0.831639" in trajectory
    performance = (ROOT / "black-forest-labs-performance-reference-2026-08-11.md").read_text()
    assert "22.18" in performance or "22.177" in performance
    assert "32.66" in performance or "32.658" in performance
    assert "0.960046" in performance
    assert mapper is not None
    assert (ROOT / "full-trajectory-run-receipt.json").exists()
    print("closed-loop-students-mappers: PASS")


if __name__ == "__main__":
    main()
