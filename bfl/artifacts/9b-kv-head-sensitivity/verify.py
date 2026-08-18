from pathlib import Path


ROOT = Path(__file__).parent


def main() -> None:
    ablation = (ROOT / "2026-08-06-flux-head-ablation-physical-circuit-signal.md").read_text()
    nine = (ROOT / "flux2-klein-9b.md").read_text()
    kv = (ROOT / "flux2-klein-9b-kv.md").read_text()
    wiki = (ROOT / "black-forest-labs-model-wiki.md").read_text()
    for value in ("D0H29", "D0H27", "S5H26", "S22H25", "13.54", "11.61", "1.03", "0.78", "96.1081"):
        assert value in ablation or value in nine or value in kv or value in wiki
    assert (ROOT / "black-forest-labs-model-wiki.md").exists()
    print("9b-kv-head-sensitivity: PASS")


if __name__ == "__main__":
    main()
