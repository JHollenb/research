from pathlib import Path


ROOT = Path(__file__).parent


def main() -> None:
    audit = (ROOT / "h9-raw-audit.v1.json").read_text()
    adversarial = (ROOT / "adversarial-h9-raw-audit.v1.json").read_text()
    replication = (ROOT / "2026-08-01-h9-native-specificity-replication.md").read_text()
    assert '"schema"' in audit
    assert "83" in audit and "88" in audit
    assert "6.740" in replication and "8.830" in replication
    assert "45/96" in replication and "collision" in replication.lower()
    assert "96" in replication and "1152" in audit.replace(",", "")
    for name in (
        "2026-08-01-040000-inside-the-flux-arbitration-harness.md",
        "2026-08-01-h9-native-specificity-replication.md",
        "2026-08-01-conditioner-cartography-reconstruction-bottleneck.md",
    ):
        assert (ROOT / name).exists()
    print("distributed-kv-causal-route: PASS")


if __name__ == "__main__":
    main()
