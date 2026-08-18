from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).parent


def load(name: str) -> dict:
    return json.loads((ROOT / name).read_text())


def main() -> None:
    phase = load("phase-parity-receipt.json")
    assert phase["model_id"] == "flux2-klein-4b"
    assert phase["parity_pass"] is True
    assert len(phase["parity"]) == 8
    assert all(row["pixel_equal"] and row["png_equal"] for row in phase["parity"])
    assert phase["speedup_per_image"] == 10.66
    assert phase["speedup_end_to_end"] == 6.25

    cheap = load("cheap-deep-replay-receipt.json")
    assert cheap["loop_parity_rel"] == 0.0
    assert len(cheap["per_k"]) == 6
    assert all(row["cheap_exact_rel"] == 0.0 for row in cheap["per_k"])
    assert all(row["edit_exact_rel"] == 0.0 for row in cheap["per_k"])
    assert max(row["speedup"] for row in cheap["per_k"]) >= 7.99

    cache = load("edit-cache-receipt.json")
    summary = cache["summary"]
    assert summary["reference_reused_count"] == 4
    assert summary["native_vs_replay_exact_count"] == 4
    assert summary["native_vs_replay_mean_cosine"] == 1.0
    assert summary["cache_hit_speedup_median"] > 4000.0
    assert cache["cache_stats"]["hits"] == 4
    assert cache["cache_stats"]["invalidations"] == 4

    print("exact-phase-resident-serving: PASS")


if __name__ == "__main__":
    main()
