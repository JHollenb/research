from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).parent


def load(name: str) -> dict:
    return json.loads((ROOT / name).read_text())


def main() -> None:
    smol = load("smol-conditioner-receipt.json")
    assert smol["model"]["conditioning"] == "smol_adapter"
    assert smol["matrix_contract"]["student_denoiser"] is False
    parity = smol["legs"]["adapter_parity"]
    assert parity["status"] == "completed"
    assert parity["held_out_mean_rgb_cosine"] > 0.82
    exact_validation = smol["legs"]["causal_checkpoint_panel"]["exact_validation"]
    assert len(exact_validation) == 4
    assert all(row["execution"]["execution_mode"] == "exact_scalar_suffix" for row in exact_validation)
    assert smol["legs"]["baseline"]["red_blue_image_mad"] == 11.422810554504395

    tecm = load("tecm-v4-report.json")
    assert tecm["mapper_fit"]["contract"]["parameter_count"] == 21074176
    assert tecm["mapper_fit"]["steps"] == 900
    assert tecm["scheduler_closure_fit"]["steps"] == 120
    assert tecm["checkpoint_control"]["same_process_native_duplicate_exact"] is True
    assert tecm["checkpoint_control"]["scheduler_parity"]["max_abs"] == 0

    heldout = load("function-recovery-heldout-report.json")
    assert heldout["execution"]["checkpoint_captures"] == 12
    assert heldout["execution"]["noop_suffix_replays"] == 12
    assert heldout["execution"]["logical_local_evaluations"] == 92
    assert heldout["execution"]["model_loads"] == 1
    smol_fit = heldout["conditioner_fit"]["smol"]["fit"]
    mamba_fit = heldout["conditioner_fit"]["mamba"]["fit"]
    assert smol_fit["parameter_count"] == 14966272
    assert mamba_fit["parameter_count"] == 14966272

    analysis = (ROOT / "function-recovery-heldout-analysis.md").read_text()
    assert "71.5%" in analysis
    assert "71.2%" in analysis
    assert "zero RGB MAD" in analysis

    print("cross-family-conditioner-repair: PASS")


if __name__ == "__main__":
    main()
