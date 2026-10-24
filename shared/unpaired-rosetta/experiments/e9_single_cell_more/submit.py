"""E9 single-cell (PBMC, SNARE-seq) sweep on Beast via mrun (CPU jobs). Adapted from e8_single_cell/submit.py.

    ~/domains/common/bin/common exec python e9_single_cell_more/submit.py --plan smoke --pair PBMC [--dry-run]
    ~/domains/common/bin/common exec python e9_single_cell_more/submit.py --plan baseline --pair SNARE-seq
    ~/domains/common/bin/common exec python e9_single_cell_more/submit.py --collect

Each job runs `seeds/beast_job.sh e9_single_cell_more.run <args>` in the venv on /mnt/usb-storage (torch + their
library at fdfad84 + pylibmgm), prints its receipt into the job log, and `--collect` decodes it into
results/e9_single_cell_more/. PBMC/SNARE data was prebuilt from the checksummed SCOT/SCOT+ files and rsynced to Beast
storage. CPU jobs, pinned to Beast, priority 75, threads <= 4.
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
JOBS = ROOT / "results" / "e9_single_cell_more" / "jobs.json"
EXPERIMENT = "unpaired-rosetta-e9-single-cell-more"
SHIP = ["pyproject.toml", "uv.lock", "common", "seeds", "e9_single_cell_more"]

TOTAL = 12  # canonical seed universe derive_seeds(42, 12); shards slice it so jobs stay under the 30-min cap.
# Baseline shards cover seeds [2:12]; seeds [0:2] come from the smoke job (full config, workers-invariant result, so the
# smoke receipt IS valid baseline data for [0:2]). PBMC (2407 cells) is slow -> 2 seeds/shard at workers=8 (smoke-proven
# to fit the 30-min cap); SNARE-seq (1047 cells) is fast -> 3 seeds/shard at workers=4.
SHARDS = {"PBMC": [(2, 4), (4, 6), (6, 8), (8, 10), (10, 12)],
          # SNARE seeds 8,9,10 are SINGLE-seed shards: the original 3-seed [8:11] shard timed out at the 30-min cap
          # (SNARE QAP solver time varies a lot by seed; one seed reaches 0.65 FOSCTTM). This is the reproducible set
          # covering seeds [2:12]; [0:2] come from the smoke job (workers-invariant result).
          "SNARE-seq": [(2, 5), (5, 8), (8, 9), (9, 10), (10, 11), (11, 12)]}
RAM = {"PBMC": 14000, "SNARE-seq": 12000}
WORKERS = {"PBMC": 8, "SNARE-seq": 4}


def manifest_sha256() -> str:
    files = sorted([HERE / "PREREG.md", HERE / "run.py", HERE / "aligner_logged.py", HERE / "submit.py"])
    out = {f.name: hashlib.sha256(f.read_bytes()).hexdigest() for f in files if f.exists()}
    return json.dumps(out, sort_keys=True)


def _job(pair, sha, lo, hi, k=0):
    return dict(args=["e9_single_cell_more.run", "--pair", pair, "--total-seeds", str(TOTAL),
                      "--seed-lo", str(lo), "--seed-hi", str(hi), "--remove-topk", str(k),
                      "--workers", str(WORKERS[pair]), "--manifest-sha256", sha],
                ram_mb=RAM[pair], timeout_s=1800)


def plan(name: str, pair: str, sha: str) -> list[dict]:
    if name == "smoke":  # 2 real seeds (universe [0:2]), full config: validates env + canary + oracle + axis + timing
        return [dict(args=["e9_single_cell_more.run", "--pair", pair, "--total-seeds", str(TOTAL),
                           "--seed-lo", "0", "--seed-hi", "2", "--workers", "8", "--manifest-sha256", sha],
                     ram_mb=RAM[pair], timeout_s=1800)]
    if name == "baseline":
        return [_job(pair, sha, lo, hi) for lo, hi in SHARDS[pair]]
    if name == "removal":  # top-1 pairs-free (by-variance) axis removal, seeds [0:6]; run only for a nuisance-type pair
        return [_job(pair, sha, lo, hi, k=1) for lo, hi in [(0, 3), (3, 6)]]
    raise SystemExit(f"unknown plan {name}")


def stage() -> Path:
    staging = Path(tempfile.mkdtemp(prefix="e9-stage-"))
    for item in SHIP:
        src = ROOT / item
        if src.is_dir():
            shutil.copytree(src, staging / item, ignore=shutil.ignore_patterns("__pycache__", "payload"))
        else:
            shutil.copy2(src, staging / item)
    return staging


def submit(name: str, pair: str, dry_run: bool, priority: int) -> None:
    sha = manifest_sha256()
    jobs = plan(name, pair, sha)
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
        note = ("e9 single-cell: " + " ".join(args))[:500]
        job_id = launch(cmd, experiment=EXPERIMENT, payload=str(staging), gpu=False, pin="beast",
                        ram_mb=job["ram_mb"], vram_mb=0, cpu_threads=4, priority=priority, detach=True,
                        timeout_s=job["timeout_s"], note=note)
        records.append({"job_id": str(job_id), "plan": name, "pair": pair, "args": job["args"]})
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
        log_dir = ROOT / "results" / "e9_single_cell_more" / "logs"
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
            out = ROOT / "results" / "e9_single_cell_more" / name
            out.write_text(json.dumps(receipt, indent=2) + "\n")
            record["receipt"] = str(out.relative_to(ROOT))
        record["collected"] = True
        print(record["job_id"], state, record.get("receipt", "NO RECEIPT"))
    JOBS.write_text(json.dumps(records, indent=2) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", choices=["smoke", "baseline", "removal"])
    parser.add_argument("--pair", choices=["PBMC", "SNARE-seq"])
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--priority", type=int, default=75)
    parser.add_argument("--collect", action="store_true")
    args = parser.parse_args()
    if args.collect:
        collect()
    elif args.plan:
        if not args.pair:
            parser.error("--pair required with --plan")
        submit(args.plan, args.pair, args.dry_run, args.priority)
    else:
        parser.error("--plan or --collect")


if __name__ == "__main__":
    main()
