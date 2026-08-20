from pathlib import Path


ROOT = Path(__file__).parent


def main() -> None:
    config = (ROOT / "flux2-dev-concept-capture.json").read_text()
    wiki = (ROOT / "black-forest-labs-model-wiki.md").read_text()
    runtime = (ROOT / "2026-08-03-160047-how-the-black-forest-models-work-from-conditioner-to-pixels.md").read_text()
    failure = (ROOT / "REPORT.md").read_text()
    index = (ROOT / "dev-runtime-index.md").read_text()
    for value in ("112.805", "24.011", "32.223", "11/11", "336.41", "12.7"):
        assert value in config or value in wiki or value in runtime or value in index
    for value in ("0.360", "0.833", "0.472"):
        assert value in failure or value in runtime or value in wiki
    assert "diagnostic" in failure.lower() or "failure" in failure.lower()
    print("flux2-dev-paged-execution: PASS")


if __name__ == "__main__":
    main()
