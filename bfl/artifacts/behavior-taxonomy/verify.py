from pathlib import Path


ROOT = Path(__file__).parent


def main() -> None:
    count = "\n".join((ROOT / name).read_text() for name in ("count-confirmation-release-v3.json", "count-runtime-certificate-v3.json", "discovery-behavior-evaluation.json"))
    typography = "\n".join((ROOT / name).read_text() for name in ("flux2-typography-behavior-certificate-v1.json", "confirmation-report-job-5bc3ca2850ed.json", "discovery-report-job-d32bf4b13094.json", "STATUS.md", "2026-07-31-212627-what-we-know-about-the-black-forest-models-a-data-driven-report.md"))
    for value in ("0.875", "0.4375", "0.1875", "0.0625"):
        assert value in count
    assert "1.0" in count or "1.000" in count
    for value in ("0.9375", "0.906", "39/48", "0.8125", "0.125", "5/16", "0/16", "0.609"):
        assert value in typography or value in count
    assert (ROOT / "2026-07-31-212627-what-we-know-about-the-black-forest-models-a-data-driven-report.md").exists()
    print("behavior-taxonomy: PASS")


if __name__ == "__main__":
    main()
