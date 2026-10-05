"""Capture a read-only mrun review; run through common exec from the workspace.

No model weights are loaded and no scheduler writes are performed. The supplied
estimator dimensions are a controlled fixture, not a measured model acquisition.
An existing output is refused so historical observations remain immutable.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch
import xml.etree.ElementTree as ET


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(
        ["rtk", "proxy", "git", "-C", str(repo), *args], text=True
    ).strip()


def suite_summary(path: Path) -> dict:
    if not path.exists():
        return {"available": False}
    suites = list(ET.parse(path).getroot().iter("testsuite"))
    counts = {
        key: sum(int(s.get(key, 0)) for s in suites)
        for key in ("tests", "failures", "errors", "skipped")
    }
    counts["passed"] = counts["tests"] - sum(
        counts[key] for key in ("failures", "errors", "skipped")
    )
    counts["seconds"] = sum(float(s.get("time", 0)) for s in suites)
    counts["unique_cases"] = len({
        (case.get("classname"), case.get("name"))
        for case in ET.parse(path).getroot().iter("testcase")
    })
    counts["nonpassing"] = [
        {"class": case.get("classname"), "name": case.get("name"),
         "outcome": child.tag, "message": child.get("message", "")}
        for case in ET.parse(path).getroot().iter("testcase")
        for child in case
        if child.tag in {"failure", "error", "skipped"}
    ]
    return counts


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", type=Path, default=Path(__file__).resolve().parents[4])
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--live", action="store_true")
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit("Refusing to replace an existing review observation")
    repo = args.workspace / "mrun"
    files = sorted((repo / "src/mrun").rglob("*.py"))
    docs = [repo / "docs" / name for name in (
        "API.md", "WORKPLAN.md", "ARCHITECTURE.md", "ENGINE-SELECTION.md",
        "SURFACE.md", "NATIVE-INFERENCE.md", "SCIENTIFIC-BENCHMARKS.md",
        "DIFFUSERS-PHASE-CUDA.md", "QWEN3-MOE-CUDA.md", "DENSE-QSTORE-CUDA.md",
        "OLMOE-CUDA.md", "APPLE-RUNTIME.md",
    )]
    records = [
        {"path": str(path.relative_to(args.workspace)), "bytes": path.stat().st_size,
         "sha256": sha256(path)} for path in files + docs
    ]
    source_digest = hashlib.sha256(json.dumps(
        records[:len(files)], sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    from mrun.estimate import estimate_activation_mb, _find_config_json
    from mrun.protocol import kill_ceiling_mb, PROBE_DEFAULT_RAM_MB
    from mrun.policy import HostCaps, plan_run
    import torch
    from mrun.engine.moe_stream import MoEStreamEngine
    stream = object.__new__(MoEStreamEngine)
    stream.dtype = torch.float32
    capability_diagnostic = {"advertised_mlp_acts": stream.capabilities().mlp_acts}
    try:
        stream.forward_acts(None)
    except NotImplementedError as exc:
        capability_diagnostic["actual_forward_acts"] = {
            "exception": type(exc).__name__, "message": str(exc)
        }

    dimensions = {"hidden": 896, "layers": 24, "heads": 14,
                  "kv_heads": 2, "head_dim": 64, "vocab": 151936}
    diagnostic = {
        "configuration_found_by_estimator": _find_config_json("qwen2.5-0.5b") is not None,
        "supplied_dimensions": dimensions,
        "instrument": "unittest.mock.patch of _model_dims; no model execution",
    }
    with patch("mrun.estimate._model_dims", return_value=dimensions):
        forward = estimate_activation_mb("qwen2.5-0.5b", seq_lens=[512], batch=16)
        recorder = estimate_activation_mb(
            "qwen2.5-0.5b", seq_lens=[512], batch=16, task="recorder"
        )
        base = estimate_activation_mb("qwen2.5-0.5b", seq_lens=[64], batch=64)
        logits = estimate_activation_mb(
            "qwen2.5-0.5b", seq_lens=[64], batch=64, count_logits=True
        )
    diagnostic.update({
        "forward_mb": forward, "recorder_mb": recorder,
        "recorder_forward_ratio": recorder / forward,
        "added_logits_mb": logits - base,
        "expected_logits_mb": 64 * 64 * 151936 * 4 / 1e6,
        "recorder_assertion_with_explicit_dims": recorder > forward * 5,
        "logits_assertion_with_explicit_dims": abs(logits-base-2489.319424) < 0.1,
    })
    hosts = (
        HostCaps("synthetic-cpu", ram_mb=64000, cpus=16),
        HostCaps("synthetic-cuda", ram_mb=64000, vram_mb=16384, has_cuda=True, cpus=16),
    )
    planning = []
    for host in hosts:
        for model in ("qwen2.5-0.5b", "qwen3-30b-a3b"):
            planning.append({"synthetic_host": host.name, "model": model,
                             "plan": plan_run(model, host=host, seq_lens=[8]).as_dict()})
    observation = {
        "schema": "mrun-model-execution-review-v1",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "source": {"head": git(repo, "rev-parse", "HEAD"),
                   "branch": git(repo, "branch", "--show-current"),
                   "dirty_status": git(repo, "status", "--short"),
                   "source_records_digest": source_digest,
                   "source_python_count": len(files), "files": records},
        "environment": {"python": sys.version, "platform": platform.platform(),
                        "machine": platform.machine(),
                        "packages": {name: importlib.metadata.version(name)
                                     for name in ("mrun", "torch", "transformers", "pytest", "psutil")}},
        "tests": {name: suite_summary(args.output.parent / f"{name}.xml")
                  for name in ("review-tests", "runtime-tests", "compiler-tests", "coadmission-isolated")},
        "estimator_diagnostic": diagnostic,
        "capability_diagnostic": capability_diagnostic,
        "planning_observations": planning,
        "containment_formula": {"probe_default_ram_mb": PROBE_DEFAULT_RAM_MB,
                                "ram_kill_ceiling_for_4096_mb": kill_ceiling_mb(4096)},
        "live": {"requested": args.live},
    }
    if args.live:
        from common_harness.mrun_api import MRunServerClient
        client = MRunServerClient(timeout_s=5)
        observation["live"].update({"health": client.health(), "version": client.version()})
        inventory = client.hosts()
        if isinstance(inventory, dict):
            inventory = inventory.get("hosts", [])
        observation["live"]["hosts"] = [
            {"name": h.get("name"), "os": h.get("os"),
             "ram_total_mb": h.get("ram_total_mb"), "vram_total_mb": h.get("vram_total_mb"),
             "cuda": bool((h.get("caps") or {}).get("cuda")),
             "mps": bool((h.get("caps") or {}).get("mps")),
             "telemetry_timestamp": (h.get("telemetry") or {}).get("ts"),
             "artifact_inventory_rows": len(h.get("models") or [])}
            for h in inventory
        ]
    args.output.write_text(json.dumps(observation, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"output": str(args.output), "source_python_count": len(files),
                      "tests": {k: {a:b for a,b in v.items() if a != "nonpassing"}
                                for k,v in observation["tests"].items()},
                      "estimator_diagnostic": diagnostic, "live": observation["live"]}, indent=2))


if __name__ == "__main__":
    main()
