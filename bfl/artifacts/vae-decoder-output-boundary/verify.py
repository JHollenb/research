from pathlib import Path


ROOT = Path(__file__).parent


def main() -> None:
    report = (ROOT / "report.json").read_text()
    residual = (ROOT / "component-substitution-io.json").read_text()
    blind = (ROOT / "flux-blind-probe.json").read_text()
    index = "\n".join((ROOT / name).read_text() for name in ("generative-model-run-survey.md", "decoder-boundary-index.md"))
    narrative = "\n".join((ROOT / name).read_text() for name in ("2026-08-04-220500-the-boundary-became-a-debugger.md", "2026-08-10-a-third-party-vae-crossed-the-flux2-boundary.md", "FLUX_BLIND_FINDINGS.md"))
    for value in ("43.678", "1.517", "44.64", "0.945507", "0.999729", "207.13", "283", "0.04"):
        assert value in report or value in residual or value in blind or value in narrative or value in index
    assert "0.999784" in report or "0.9997839" in index or "0.9997839" in narrative
    assert "192" in report
    assert (ROOT / "native.png").exists() and (ROOT / "alternate.png").exists()
    print("vae-decoder-output-boundary: PASS")


if __name__ == "__main__":
    main()
