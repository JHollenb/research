"""E7 search/initialization experiment on Beast via mrun (CPU jobs). Adapted from e6_generality/submit.py.

    ~/domains/common/bin/common exec python e7_search_init/submit.py --plan smoke [--dry-run]
    ~/domains/common/bin/common exec python e7_search_init/submit.py --plan A
    ~/domains/common/bin/common exec python e7_search_init/submit.py --plan B
    ~/domains/common/bin/common exec python e7_search_init/submit.py --plan C
    ~/domains/common/bin/common exec python e7_search_init/submit.py --plan Cpc0
    ~/domains/common/bin/common exec python e7_search_init/submit.py --plan D
    ~/domains/common/bin/common exec python e7_search_init/submit.py --plan E
    ~/domains/common/bin/common exec python e7_search_init/submit.py --plan Emulti
    ~/domains/common/bin/common exec python e7_search_init/submit.py --collect

CPU jobs, pinned to Beast, priority 75, 4 threads. Each runs `seeds/beast_job.sh e7_search_init.arms <args>`.
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
JOBS = ROOT / "results" / "e7_search_init" / "jobs.json"
EXPERIMENT = "unpaired-rosetta-e7-search-init"
SHIP = ["pyproject.toml", "uv.lock", "common", "seeds", "e5_scaffold_axis", "e6_generality", "e7_search_init"]
PRIMARY = ["DenselyCaptionedImages", "DOCCIDataset"]
GEN = "qwen3-8b-gen_69445574b3021b8a2733e87d8603d769"
EMB = "qwen3-embedding-8b"


def manifest_sha256() -> str:
    files = sorted([HERE / "PREREG.md", HERE / "arms.py", HERE / "submit.py", HERE / "__init__.py"])
    out = {f.name: hashlib.sha256(f.read_bytes()).hexdigest() for f in files if f.exists()}
    return json.dumps(out, sort_keys=True)


def A(sha, c):
    return dict(args=["e7_search_init.arms", "--arm", "a", "--corpus", c, "--candidate", "none",
                      "--workers", "4", "--manifest-sha256", sha], ram_mb=9000, timeout_s=5400)


def plan(name: str, sha: str) -> list[dict]:
    if name == "smoke":
        jobs = []
        for arm in ("a", "b", "c", "d", "e"):
            jobs.append(dict(args=["e7_search_init.arms", "--arm", arm, "--corpus", "DenselyCaptionedImages",
                                   "--smoke", "--workers", "4", "--manifest-sha256", sha],
                             ram_mb=13000, timeout_s=2400))
        return jobs
    if name == "A":
        return [A(sha, c) for c in PRIMARY]
    if name == "B":
        return [dict(args=["e7_search_init.arms", "--arm", "b", "--targets", *PRIMARY,
                           "--workers", "4", "--manifest-sha256", sha], ram_mb=10000, timeout_s=5400)]
    if name == "C":  # few true pairs, candidate none, all k, one job per corpus
        return [dict(args=["e7_search_init.arms", "--arm", "c", "--corpus", c, "--candidates", "none",
                           "--ks", "1", "5", "10", "50", "100", "--workers", "4", "--manifest-sha256", sha],
                     ram_mb=8000, timeout_s=5400) for c in PRIMARY]
    if name == "Cpc0":  # few true pairs + axis removal (secondary)
        return [dict(args=["e7_search_init.arms", "--arm", "c", "--corpus", c, "--candidates", "pc0",
                           "--ks", "1", "5", "10", "50", "100", "--workers", "4", "--manifest-sha256", sha],
                     ram_mb=8000, timeout_s=5400) for c in PRIMARY]
    if name == "D":  # cumulative drop-k, pairs-free
        return [dict(args=["e7_search_init.arms", "--arm", "d", "--corpus", c, "--ks", "2", "3", "4", "5",
                           "--workers", "4", "--manifest-sha256", sha], ram_mb=8000, timeout_s=5400)
                for c in PRIMARY]
    if name == "E":  # per-iterate trace, baseline aligner, all 3 encoders, one job per corpus, seed 0
        return [dict(args=["e7_search_init.arms", "--arm", "e", "--corpus", c, "--encoders", GEN, EMB, "mpnet",
                           "--candidate", "none", "--workers", "4", "--manifest-sha256", sha],
                     ram_mb=9000, timeout_s=5400) for c in ("StanfordParagraphCaptioning", *PRIMARY)]
    if name == "Emulti":  # gen baseline seeds 1,2 for the seed-selection analysis, DCI+DOCCI
        jobs = []
        for c in PRIMARY:
            for seed in (1, 2):
                jobs.append(dict(args=["e7_search_init.arms", "--arm", "e", "--corpus", c, "--encoders", GEN,
                                       "--candidate", "none", "--seed", str(seed), "--workers", "4",
                                       "--manifest-sha256", sha], ram_mb=8000, timeout_s=5400))
        return jobs
    raise SystemExit(f"unknown plan {name}")


def stage() -> Path:
    staging = Path(tempfile.mkdtemp(prefix="e7-stage-"))
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
        print(json.dumps([j["args"] for j in jobs], indent=2))
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
        note = ("e7 search-init: " + " ".join(args))[:500]
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
        log_dir = ROOT / "results" / "e7_search_init" / "logs"
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
            out = ROOT / "results" / "e7_search_init" / name
            out.write_text(json.dumps(receipt, indent=2) + "\n")
            record["receipt"] = str(out.relative_to(ROOT))
        record["collected"] = True
        print(record["job_id"], state, record.get("receipt", "NO RECEIPT"))
    JOBS.write_text(json.dumps(records, indent=2) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", choices=["smoke", "A", "B", "C", "Cpc0", "D", "E", "Emulti"])
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
