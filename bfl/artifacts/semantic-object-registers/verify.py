from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).parent


def load(name: str) -> dict:
    return json.loads((ROOT / name).read_text())


def check_job(name: str, model_id: str, steps: int, offload: str, seeds: list[int]) -> dict:
    receipt = load(name)
    assert receipt["mrun_ok"] is True
    assert receipt["mrun_state"] == "succeeded"
    assert receipt["mrun_result"]["returncode"] == 0
    assert receipt["mrun_result"]["status"] == "ok"
    assert receipt["mrun_result"]["failure"] is None
    assert receipt["model_id"] == model_id
    assert receipt["steps"] == steps
    assert receipt["offload"] == offload
    assert receipt["device"] == "cuda"
    assert receipt["preflight"] == "strict"
    assert receipt["scheduling_contract"]["max_mrun_submissions"] == 1
    assert receipt["scheduling_contract"]["model_loads"] == 1
    assert receipt["scheduling_contract"]["mrun_retry_policy"] == "none_for_finite_lease"
    payload_seeds = None
    for key in ("object_multimodel", "object_flux1"):
        block = receipt["payload"].get(key)
        if block is not None:
            payload_seeds = block["seeds"]
            break
    if payload_seeds is None:
        payload_seeds = receipt["payload"]["seeds"]
    assert payload_seeds == seeds
    return receipt


def main() -> None:
    # Arm A: FLUX.2-klein-base-4B, undistilled, native 50-step real-CFG operating point.
    arm_a = check_job(
        "run-receipt.job-17788d5a1b0d.json",
        model_id="flux2-klein-base-4b",
        steps=50,
        offload="model",
        seeds=[7217, 31337],
    )
    assert arm_a["guidance"] == 4.0
    assert arm_a["payload"]["object_multimodel"]["default_route"] == [
        "joint.2", "joint.3", "joint.4", "single.0",
    ]

    # Arm B: FLUX.2-klein-9B, sequential offload, Qwen3-8B conditioner freed post-encode.
    arm_b = check_job(
        "run-receipt.job-638d05dcbff2.json",
        model_id="flux2-klein-9b",
        steps=4,
        offload="sequential",
        seeds=[7217],
    )
    assert arm_b["guidance"] == 1.0
    assert arm_b["payload"]["object_multimodel"]["default_route"] == [
        "joint.4", "joint.5", "joint.6", "joint.7", "single.0",
    ]

    # Arm C: FLUX.1-schnell base battery and locality-probe follow-up.
    for name in ("run-receipt.job-a676189574d1.json", "run-receipt.job-27fef20e82a0.json"):
        arm_c = check_job(
            name,
            model_id="flux1-schnell",
            steps=4,
            offload="sequential",
            seeds=[7217, 31337],
        )
        assert arm_c["guidance"] == 0.0
        assert arm_c["dtype"] == "bfloat16 (fp8_e4m3 layerwise storage)"

    # Arm E: cross-conditioner wrong-object diagnosis.
    arm_e = load("run-receipt.job-e1ba0cbed889.json")
    assert arm_e["mrun_ok"] is True
    assert arm_e["mrun_state"] == "succeeded"
    assert arm_e["mrun_result"]["returncode"] == 0
    assert arm_e["model_id"] == "black-forest-labs/FLUX.2-klein-4B"
    assert arm_e["payload"]["mapper_steps"] == 900
    assert arm_e["payload"]["seeds"] == [7217, 31337]

    for image in (
        "zoom-fox-base4b-seed31337.png",
        "zoom-mug-port-base4b.png",
        "zoom-fox-klein9b-seed7217.png",
        "zoom-mug-port-klein9b.png",
        "locality-strip-flux1.png",
        "xcond-diagnosis-strip.png",
    ):
        assert (ROOT / image).exists(), image

    print("semantic-object-registers: PASS")


if __name__ == "__main__":
    main()
