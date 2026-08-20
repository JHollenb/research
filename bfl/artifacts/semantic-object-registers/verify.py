from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).parent


def load(name: str) -> dict:
    return json.loads((ROOT / name).read_text())


def assert_success(name: str, *, model: str | None = None) -> dict:
    receipt = load(name)
    assert receipt.get("mrun_ok", True) is True, name
    assert receipt["mrun_state"] == "succeeded", name
    result = receipt["mrun_result"]
    assert result["returncode"] == 0, name
    assert result["status"] == "ok", name
    assert result.get("failure") is None, name
    if model is not None:
        assert receipt["model_id"] == model, name
    return receipt


def payload_seeds(receipt: dict) -> list[int] | None:
    for key in ("object_multimodel", "object_flux1"):
        block = receipt.get("payload", {}).get(key)
        if block is not None and "seeds" in block:
            return block["seeds"]
    return receipt.get("payload", {}).get("seeds")


def main() -> None:
    base = assert_success(
        "run-receipt.job-17788d5a1b0d.json",
        model="flux2-klein-base-4b",
    )
    assert base["steps"] == 50
    assert base["guidance"] == 4.0
    assert payload_seeds(base) == [7217, 31337]

    for name in (
        "run-receipt.job-638d05dcbff2.json",
        "run-receipt.job-3e1bc534e0eb.json",
    ):
        receipt = assert_success(name, model="flux2-klein-9b")
        assert receipt["steps"] == 4
        assert receipt["offload"] == "sequential"
        assert payload_seeds(receipt) == [7217]

    for name in (
        "run-receipt.job-a676189574d1.json",
        "run-receipt.job-27fef20e82a0.json",
        "run-receipt.job-e920a0e84b37.json",
        "run-receipt.job-ee619dfec24f.json",
        "run-receipt.job-3980f89faa61.json",
        "run-receipt.job-65d315d873dc.json",
        "run-receipt.job-86cb59fb03a0.json",
    ):
        receipt = assert_success(name, model="flux1-schnell")
        assert receipt["steps"] == 4
        assert receipt["offload"] == "sequential"
        assert payload_seeds(receipt) == [7217, 31337]

    xcond = assert_success(
        "run-receipt.job-e1ba0cbed889.json",
        model="black-forest-labs/FLUX.2-klein-4B",
    )
    assert xcond["payload"]["seeds"] == [7217, 31337]

    closure = assert_success("run-receipt.job-0a318a2d8c9d.json")
    assert closure["mrun_job_id"] == "job-0a318a2d8c9d"

    struct = assert_success(
        "run-receipt.job-f0edaded5d06.json",
        model="black-forest-labs/FLUX.2-klein-4B",
    )
    assert struct["instrument"].startswith("struct-write debugger IO")

    for image in (
        "zoom-fox-base4b-seed31337.png",
        "proof-sheet-foxball-9b-512-seed7217.png",
        "locality-strip-flux1.png",
        "rows-pooled-interaction-strip.png",
        "xcond-diagnosis-strip.png",
        "window-algebra-strip.png",
        "pure-color-port-strip.png",
        "pure-color-debug-strip.png",
        "species-prior-strip.png",
        "zoom-mug-pure-color.png",
        "struct-write-strip-seed7217.png",
        "struct-write-strip-seed31337.png",
        "zoom-ball-remove-vs-translate.png",
    ):
        assert (ROOT / image).exists(), image

    assert (ROOT / "tecm-closure-analysis.md").exists()
    print("semantic-object-registers: PASS")


if __name__ == "__main__":
    main()
