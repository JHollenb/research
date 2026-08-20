from pathlib import Path


ROOT = Path(__file__).parent


def main() -> None:
    report = (ROOT / "report.json").read_text()
    evidence = "\n".join((ROOT / name).read_text() for name in ("2026-08-13-the-empty-context-was-holding-the-picture-up.md", "2026-08-13-the-write-was-a-tone-bank-and-the-scaffold-was-an-echo.md"))
    assert "41.9" in report or "41.9" in evidence
    assert "53.2" in report or "53.2" in evidence
    assert "42.7" in evidence and "55.5" in evidence
    assert "16.4" in evidence and "22.1" in evidence
    assert "68.6" in evidence and "76.5" in evidence
    assert "80" in evidence and "89" in evidence
    assert (ROOT / "2026-08-13-the-write-was-a-tone-bank-and-the-scaffold-was-an-echo.md").read_text().lower().find("tone bank") >= 0
    assert (ROOT / "run-receipt.json").exists()
    print("empty-context-positional-scaffold: PASS")


if __name__ == "__main__":
    main()
