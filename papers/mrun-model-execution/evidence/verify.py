"""Verify this paper's portable evidence with the Python standard library.

Checks integrity and recorded result arithmetic. Does not load models, rerun
hardware measurements, or certify that a historical promotion is current.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import statistics
from pathlib import Path
import xml.etree.ElementTree as ET


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def close(a: float, b: float) -> None:
    if not math.isclose(a, b, rel_tol=1e-10, abs_tol=1e-8):
        raise AssertionError(f"Recorded arithmetic mismatch: {a} versus {b}")


def read(path: Path) -> dict:
    return json.loads(path.read_text())


def verify_cpu(record: dict) -> None:
    independent = record["independent_seconds"]
    compiled = record["compiled_seconds"]
    assert len(independent) == len(compiled) == 30
    close(statistics.median(independent), record["independent_median_seconds"])
    close(statistics.median(compiled), record["compiled_median_seconds"])
    ratios = [a/b for a, b in zip(independent, compiled)]
    close(statistics.median(independent)/statistics.median(compiled), record["speedup"])
    close(statistics.median(ratios), record["paired_speedup_median"])
    close(min(ratios), record["paired_speedup_min"])
    assert record["qualified"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", type=Path, help="Also compare the current local source snapshot")
    args = parser.parse_args()
    evidence = Path(__file__).resolve().parent
    paper_root = evidence.parent
    sums = read(evidence / "checksums.json")
    checked = 0
    for relative, expected in sums["files"].items():
        path = paper_root / relative
        assert path.resolve().is_relative_to(paper_root), relative
        assert path.is_file() and not path.is_symlink(), relative
        assert digest(path) == expected, f"Checksum mismatch: {relative}"
        checked += 1
    snapshot = read(evidence / "review-snapshot.json")
    for lane, record in snapshot["tests"].items():
        suites = list(ET.parse(evidence / f"{lane}.xml").getroot().iter("testsuite"))
        for key in ("tests", "failures", "errors", "skipped"):
            assert sum(int(s.get(key, 0)) for s in suites) == record[key], (lane, key)
        assert record["passed"] == record["tests"] - sum(
            record[k] for k in ("failures", "errors", "skipped")
        )
    prior = evidence / "prior"
    branch = read(prior / "sciencegraph-qwen25-0.5b-v3-cpu-30x-v2.json")["benchmark"]
    verify_cpu(branch)
    assert branch["exact_winners"]
    assert branch["max_abs_score_delta"] <= branch["atol"]
    automatic = read(prior / "automatic-campaign-qwen25-0.5b-v3-cpu-30x-v1.json")
    verify_cpu(automatic)
    assert automatic["exact_rows"] and automatic["exact_summary"]
    cuda = read(prior / "cuda-graph-primary-4dc54fcd1048.json")
    graph = cuda["cuda_graph_benchmark"]
    eager = graph["matched_eager_control"]["samples_ms"]
    replay = graph["cuda_graph"]["samples_ms"]
    assert len(eager) == len(replay) == 30
    close(statistics.median(eager), graph["matched_eager_control"]["median_ms"])
    close(statistics.median(replay), graph["cuda_graph"]["median_ms"])
    paired = [a/b for a, b in zip(eager, replay)]
    close(statistics.median(paired), graph["matched_eager_to_cuda_graph"]["median_ratio"])
    assert sum(a > b for a, b in zip(eager, replay)) == graph["matched_eager_to_cuda_graph"]["wins"]
    assert graph["output_parity"]["exact"] and graph["output_parity"]["max_abs_error"] == 0
    assert math.ceil(graph["capture_setup_ms"]/graph["per_replay_savings_ms"]) == graph["break_even_replays"]
    campaign = cuda["campaign_benchmark"]
    ratios = [a/b for a, b in zip(campaign["independent"]["samples_ms"], campaign["compiled"]["samples_ms"])]
    close(statistics.median(ratios), campaign["independent_to_compiled"]["median_ratio"])
    fusion = read(prior / "profile-fusion-qwen25-0.5b-cuda-v1.json")
    assert not fusion["qualified"] and not any(cell["qualified"] for cell in fusion["cells"])
    service = read(prior / "resident-batch-service-qwen25-0.5b-cuda-v1.json")
    assert service["cancellation_passed"] and service["refill_passed"]
    assert service["service_telemetry"]["captured_rows"] == 1892
    assert service["service_telemetry"]["captured_dispatches"] == 151
    source_count = 0
    if args.workspace:
        records = snapshot["source"]["files"] + read(evidence / "test-source-records.json")["files"]
        for row in records:
            path = args.workspace / row["path"]
            assert path.is_file() and digest(path) == row["sha256"], f"Current source differs: {row['path']}"
            source_count += 1
    print(json.dumps({"status": "verified", "bundle_files": checked,
                      "source_files_compared": source_count,
                      "recorded_test_failures_preserved": 3,
                      "historical_hardware_rerun": False}, indent=2))


if __name__ == "__main__":
    main()
