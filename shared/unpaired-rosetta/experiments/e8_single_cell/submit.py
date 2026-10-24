"""E8 single-cell (CITE-seq) sweep on Beast via mrun (CPU jobs). Adapted from e6_generality/submit.py.

    ~/domains/common/bin/common exec python e8_single_cell/submit.py --plan smoke [--dry-run]
    ~/domains/common/bin/common exec python e8_single_cell/submit.py --plan baseline
    ~/domains/common/bin/common exec python e8_single_cell/submit.py --plan removal
    ~/domains/common/bin/common exec python e8_single_cell/submit.py --collect

Each job runs `seeds/beast_job.sh e8_single_cell.run <args>` in the venv on /mnt/usb-storage (torch + their library
at fdfad84 + pylibmgm), prints its receipt into the job log, and `--collect` decodes it into results/e8_single_cell/.
CITE-seq data was prebuilt from the checksummed SCOT+ CSVs and rsynced to Beast storage. CPU jobs, pinned to Beast,
priority 75, threads <= 4.
"""

from __future__ import annotations

import argparse
import base64
import gzip
import hashlib
import json
import shutil
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
JOBS = ROOT / "results" / "e8_single_cell" / "jobs.json"
EXPERIMENT = "unpaired-rosetta-e8-single-cell"
SHIP = ["pyproject.toml", "uv.lock", "common", "seeds", "e8_single_cell"]


def manifest_sha256() -> str:
    files = sorted([HERE / "PREREG.md", HERE / "run.py", HERE / "aligner_logged.py", HERE / "submit.py"])
    out = {f.name: hashlib.sha256(f.read_bytes()).hexdigest() for f in files if f.exists()}
    return json.dumps(out, sort_keys=True)


def plan(name: str, sha: str) -> list[dict]:
    if name == "smoke":  # 2 real seeds, full config: validates env + canary + oracle, measures per-seed Beast time
        return [dict(args=["e8_single_cell.run", "--seeds", "2", "--workers", "1", "--manifest-sha256", sha],
                     ram_mb=4000, timeout_s=1800)]
    if name == "baseline":  # 20 seeds, no removal: canary, oracle, selection, axis probe
        return [dict(args=["e8_single_cell.run", "--seeds", "20", "--workers", "1", "--manifest-sha256", sha],
                     ram_mb=6000, timeout_s=1800)]
    if name == "removal":  # 20 seeds, top-1 and top-2 pairs-free axis removal
        return [dict(args=["e8_single_cell.run", "--seeds", "20", "--remove-topk", str(k), "--workers", "1",
                           "--manifest-sha256", sha], ram_mb=6000, timeout_s=1800) for k in (1, 2)]
    raise SystemExit(f"unknown plan {name}")


def stage() -> Path:
    staging = Path(tempfile.mkdtemp(prefix="e8-stage-"))
    for item in SHIP:
        src = ROOT / item
        if src.is_dir():
            shutil.copytree(src, staging / item, ignore=shutil.ignore_patterns("__pycache__", "payload"))
        else:
            shutil.copy2(src, staging / item)
    return staging


def submit(name: str, dry_run: bool, priority: int) -> None:
    sha = manifest_sha256()
    jobs = plan(name, sha)
    if dry_run:
        print(json.dumps(jobs, indent=2))
        return
    from mrun.client.submit import launch

    staging = stage()
    records = json.loads(JOBS.read_text()) if JOBS.exists() else []
    for job in jobs:
        cmd = ["bash", "seeds/beast_job.sh", *job["args"]]
        args = job["args"]
        if "--manifest-sha256" in args:
            i = args.index("--manifest-sha256")
            args = args[:i] + args[i + 2:]
        note = ("e8 single-cell: " + " ".join(args))[:500]
        job_id = launch(cmd, experiment=EXPERIMENT, payload=str(staging), gpu=False, pin="beast",
                        ram_mb=job["ram_mb"], vram_mb=0, cpu_threads=4, priority=priority, detach=True,
                        timeout_s=job["timeout_s"], note=note)
        records.append({"job_id": str(job_id), "plan": name, "args": job["args"]})
        print("submitted", job_id, " ".join(job["args"]), flush=True)
    JOBS.parent.mkdir(parents=True, exist_ok=True)
    JOBS.write_text(json.dumps(records, indent=2) + "\n")


def collect() -> None:
    from mrun.client.api import Api

    api = Api()
    records = json.loads(JOBS.read_text())
    for record in records:
        if record.get("collected"):
            continue
        job = api.json("GET", f"/api/jobs/{record['job_id']}", timeout_s=60)
        state = job.get("state")
        record["state"] = state
        if state not in ("succeeded", "failed", "cancelled", "killed"):
            continue
        _, body, _ = api.request("GET", f"/api/jobs/{record['job_id']}/logs?offset=0&wait_s=1", timeout_s=180)
        logs = body.decode("utf-8", "replace")
        log_dir = ROOT / "results" / "e8_single_cell" / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        (log_dir / f"{record['job_id']}.txt").write_text(logs)
        name = blob = None
        for line in logs.splitlines():
            if line.startswith("UNPAIRED_ROSETTA_RECEIPT_NAME="):
                name = line.split("=", 1)[1].strip()
            elif line.startswith("UNPAIRED_ROSETTA_RECEIPT_GZIP_B64="):
                blob = line.split("=", 1)[1].strip()
        if name and blob:
            receipt = json.loads(gzip.decompress(base64.b64decode(blob)))
            receipt["fleet"] = {"job_id": record["job_id"], "host": job.get("assigned_host")}
            out = ROOT / "results" / "e8_single_cell" / name
            out.write_text(json.dumps(receipt, indent=2) + "\n")
            record["receipt"] = str(out.relative_to(ROOT))
        record["collected"] = True
        print(record["job_id"], state, record.get("receipt", "NO RECEIPT"))
    JOBS.write_text(json.dumps(records, indent=2) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", choices=["smoke", "baseline", "removal"])
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--priority", type=int, default=75)
    parser.add_argument("--collect", action="store_true")
    args = parser.parse_args()
    if args.collect:
        collect()
    elif args.plan:
        submit(args.plan, args.dry_run, args.priority)
    else:
        parser.error("--plan or --collect")


if __name__ == "__main__":
    main()
