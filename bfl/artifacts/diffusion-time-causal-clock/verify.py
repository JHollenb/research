import json
from pathlib import Path


ROOT = Path(__file__).parent


def main() -> None:
    resume = json.loads((ROOT / "diffusion_resume_klein4b.json").read_text())
    resume_text = (ROOT / "diffusion_resume_klein4b.json").read_text()
    assert "Klein" in resume_text
    assert "0.35981" in resume_text and "2.3986" in resume_text
    assert "0.0784" in resume_text and "0.5226" in resume_text
    cheap = (ROOT / "diffusion_cheap_deep_klein4b.json").read_text()
    assert "7.993" in cheap and "0.0" in cheap
    faceid = (ROOT / "character_pin_faceid_klein4b.json").read_text()
    assert "0.7913" in faceid and "-0.008" in faceid
    regional = (ROOT / "diffusion_regional_sustained_klein4b.json").read_text()
    assert "0.5249" in regional and "0.4107" in regional
    role_map = (ROOT / "image-stream-control-buttons.md").read_text()
    for label in ("joint.4:image", "single.0:image", "single.10:image", "single.19:image"):
        assert label in role_map
    for name in ("diffusion_cheap_deep_montage.jpg", "character_pin_montage.jpg", "character_pin_faceid_montage.jpg", "diffusion_regional_sustained_montage.jpg"):
        assert (ROOT / name).exists()
    assert resume is not None
    print("diffusion-time-causal-clock: PASS")


if __name__ == "__main__":
    main()
