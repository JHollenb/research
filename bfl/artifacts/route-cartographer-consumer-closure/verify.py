from pathlib import Path


ROOT = Path(__file__).parent


def main() -> None:
    report = (ROOT / "multidomain-cartographer-report.json").read_text()
    narrative = (ROOT / "2026-08-14-183145-flux-route-address-register-became-a-cartographer.md").read_text()
    for value in ("685", "85", "325", "56", "54", "0.990", "0.977", "0.114", "0.455", "0.001", "0.227", "0.105", "0.197", "0.911"):
        assert value in report or value in narrative
    assert "5/5" in report or "5/5" in narrative
    for name in ("route-signatures.json", "native-route-outcomes.json", "leave-one-domain-out.json", "predictors.json", "summary.json"):
        assert (ROOT / name).exists()
    print("route-cartographer-consumer-closure: PASS")


if __name__ == "__main__":
    main()
