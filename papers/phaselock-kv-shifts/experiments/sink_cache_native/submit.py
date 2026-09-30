"""Stage an immutable paired SinkCache payload and submit it through mrun."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

from mrun.client.submit import submit


HERE = Path(__file__).resolve().parent
WORKSPACE = HERE.parents[4]
UPSTREAM = WORKSPACE / "sink_cache"
BASELINE_REVISION = "ea681c770c26d245c37d49c6760eeaa07f4fc1ce"
MODEL = Path(
    "/mnt/big/llm-models/hf/hub/models--Qwen--Qwen2.5-1.5B-Instruct/snapshots/"
    "989aa7980e4cf806f80c7fef2b1adb7bc71aa306"
)
DATASET_TRAIN = Path(
    "/home/beast/.cache/huggingface/hub/datasets--wikitext/snapshots/"
    "b08601e04326c79dfdd32d625aee71d232d685c3/"
    "wikitext-2-raw-v1/train-00000-of-00001.parquet"
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True)
    parser.add_argument("--tokens", type=int, default=2600)
    parser.add_argument("--window", type=int, default=1024)
    parser.add_argument("--split", choices=("train", "test"), default="train")
    parser.add_argument("--position-mode", choices=("bounded_local_slot", "absolute_global"),
                        default="bounded_local_slot")
    parser.add_argument("--priority", type=int, default=90)
    args = parser.parse_args()
    capacity = args.window + 4
    reservation_vram_mb = 4000 if args.window <= 256 else 5120
    # The first W1024 global run reached 3821 MB RSS and was killed by its
    # 3584 MB cgroup ceiling before prefill. Allow for the full-run peak.
    reservation_ram_mb = 3072 if args.window <= 256 else 5120
    dataset = Path(str(DATASET_TRAIN).replace("train-00000", f"{args.split}-00000"))

    stage = Path(tempfile.mkdtemp(prefix=f"sink-cache-{args.name}-"))
    shutil.copy2(HERE / "compare.py", stage / "compare.py")
    source = "custom_generate/generate.py"
    baseline = subprocess.run(
        ["git", "-C", str(UPSTREAM), "show", f"{BASELINE_REVISION}:{source}"],
        check=True, capture_output=True,
    ).stdout
    (stage / "baseline_generate.py").write_bytes(baseline)
    shutil.copy2(UPSTREAM / source, stage / "patched_generate.py")
    if baseline == (stage / "patched_generate.py").read_bytes():
        raise RuntimeError("baseline and patched source are identical")
    hashes = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in stage.iterdir()}
    output = Path(f"/mnt/big/sweep-logs/phaselock-sinkcache-native-{args.name}.json")
    command = [
        "/usr/bin/env", "UV_CACHE_DIR=/mnt/big/llm-models/.uv-cache",
        "HF_HUB_OFFLINE=1", "TRANSFORMERS_OFFLINE=1", "TOKENIZERS_PARALLELISM=false",
        "PYTHONUNBUFFERED=1", "uv", "run", "--offline", "--project", "{env}",
        "--with", "transformers==4.52.1", "python", "-u", "compare.py",
        "--baseline", "baseline_generate.py", "--patched", "patched_generate.py",
        "--model", str(MODEL), "--dataset", str(dataset),
        "--tokens", str(args.tokens), "--window", str(args.window), "--sinks", "4",
        "--position-mode", args.position_mode,
        "--report-every", str(args.window),
        "--out", str(output),
    ]
    note = (
        f"Native paired SinkCache {args.name}: Qwen2.5-1.5B bf16, WikiText-2 {args.split}, "
        f"{args.tokens} tokens, sequential arms, W={args.window}, S=4, "
        f"capacity={capacity}, positions={args.position_mode}. "
        f"VRAM {reservation_vram_mb}MB (observed W1024 max 4742MB); "
        f"RAM {reservation_ram_mb}MB (global prefill reached 3821MB; "
        "previous 3584MB ceiling killed job). Stop at JSON. "
        "Compare upstream vs corrected cache phases."
    )
    print(json.dumps({"stage": str(stage), "hashes": hashes, "command": command, "note": note}), flush=True)
    job_id = submit(
        experiment=f"phaselock-sinkcache-native-{args.name}",
        cmd=command,
        config={"research_stage": "developmental-discovery", "task_family": "decode",
                "tokens": args.tokens, "window": args.window, "sinks": 4,
                "context_len": capacity, "dataset_split": args.split,
                "position_mode": args.position_mode,
                "native_cache_sources": hashes},
        payload=stage, model="qwen2.5-1.5b-instruct", task="decode", backend="hf",
        dtype="bfloat16", device="cuda", host="beast", priority=args.priority,
        reservation={"ram_mb": reservation_ram_mb, "vram_mb": reservation_vram_mb, "cpu_threads": 4},
        note=note, timeout_s=10800 if args.tokens > 5000 else 1800,
        preflight=True, retry_on_kill=False,
    )
    print(json.dumps({"job_id": job_id, "output": str(output), "stage": str(stage)}), flush=True)


if __name__ == "__main__":
    main()
