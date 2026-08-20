from pathlib import Path


ROOT = Path(__file__).parent


def main() -> None:
    wiki = (ROOT / "black-forest-labs-model-wiki.md").read_text()
    seven = (ROOT / "2026-08-02-seven-flux-artifacts-under-the-microscope.md").read_text()
    conditioner = (ROOT / "2026-07-31-145130-the-conditioners-were-stock-checkpoints.md").read_text()
    for value in ("2,883", "17.442", "96.1081", "17,353,362,980", "0.9382467", "0.9447244", "1,425", "0.0205", "0.0208", "251/251"):
        assert value in wiki or value in seven
    assert "0.9999997" in conditioner and "0.9999992" in conditioner
    assert wiki and seven and conditioner
    print("model-family-forensics: PASS")


if __name__ == "__main__":
    main()
