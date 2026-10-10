"""Seed sweeps on the fleet: E1 and E5 at more seeds, E2 draw spread, and the Prop. D1 check.

    ~/domains/common/bin/common exec python seeds/submit.py --plan smoke          # one tiny job: env + data check
    ~/domains/common/bin/common exec python seeds/submit.py --plan full [--dry-run]
    ~/domains/common/bin/common exec python seeds/submit.py --collect             # pull receipts of finished jobs

Each job runs ``seeds/beast_job.sh <module> <args>`` with the venv provisioned on /mnt/usb-storage (Beast's
torch + their library at fdfad84 + pylibmgm) and prints the receipt into the job log; ``--collect`` decodes it into ``results/<exp>/``.
Jobs are pinned to Beast: these are CPU jobs, and an unpinned CPU job could land on the laptop agent.

TODO(mrun-pub): uses the private fleet client (``mrun.client.submit.launch``); port to ``mrun-pub``. Without a
fleet, the same commands run locally: ``uv run python -m <module> <args>``.
"""

from __future__ import annotations

import argparse
import base64
import gzip
import json
import shutil
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
JOBS = ROOT / "results" / "seeds" / "jobs.json"
EXPERIMENT = "unpaired-rosetta-seeds"
SHIP = ["pyproject.toml", "uv.lock", "common", "seeds", "e1_fidelity_gap", "e2_span_bound", "e5_scaffold_axis"]
LANGUAGES = ["qwen3-8b-gen_69445574b3021b8a2733e87d8603d769", "qwen3-embedding-8b", "mpnet"]
SEEDS = [0, 1, 2]  # 3 seeds total (user 2026-10-09: "3 seeds are plenty")
OUT_DIR = {"e5_gates": "e5_scaffold_axis", "e1_fidelity_gap": "e1_fidelity_gap", "e1_d1_check": "e1_fidelity_gap", "e5_scaffold_axis": "e5_scaffold_axis",
           "e2_draws": "e2_span_bound"}


def plan(name: str) -> list[dict]:
    if name == "smoke":
        return [dict(args=["e5_scaffold_axis.run", "--smoke", "--languages", "mpnet", "--workers", "4"],
                     ram_mb=6000, timeout_s=3600)]
    if name == "gates":  # E5c discovery-selected gate detector: one fit per (language, candidate), seed 0
        return [dict(args=["e5_scaffold_axis.gates", "--workers", "4", "--language", language, "--candidate", candidate],
                     ram_mb=8000, timeout_s=3 * 3600)
                for language in LANGUAGES for candidate in ["none", "pc0", "pc1", "pc2", "pc3", "pc4"]]
    if name == "gates-seeds":  # the new headline (G1); seeds 1-2 for each model's top-2 S1 settings at seed 0 only
        top2 = {LANGUAGES[0]: ["none", "pc0"], "qwen3-embedding-8b": ["none", "pc4"], "mpnet": ["none", "pc3"]}
        return [dict(args=["e5_scaffold_axis.gates", "--workers", "4", "--language", language, "--candidate", candidate,
                           "--seed", str(seed)], ram_mb=8000, timeout_s=3 * 3600)
                for language, candidates in top2.items() for candidate in candidates for seed in SEEDS[1:]]
    if name == "core":
        # Seeds only where a headline could move (user rule 2026-10-09: no multi-seed runs for things that fail or
        # cannot contribute). Seed 0 already exists from the laptop; Beast parity was measured on the smoke.
        jobs = [dict(args=["e1_fidelity_gap.run", "--workers", "4", "--seed", str(seed), "--pairs"],
                     ram_mb=10000, timeout_s=3 * 3600) for seed in SEEDS[1:]]  # zero-pair map + both oracles
        jobs += [dict(args=["e5_scaffold_axis.run", "--workers", "4", "--seed", str(seed), "--languages", LANGUAGES[0],
                            "--arms", "raw", "drop1"], ram_mb=8000, timeout_s=3 * 3600) for seed in SEEDS[1:]]
        return jobs
    jobs = []
    for seed in SEEDS:  # E1: their method at p = 0, 10, 100 plus both oracles; COCO, ~3 fits per job
        jobs.append(dict(args=["e1_fidelity_gap.run", "--workers", "4", "--seed", str(seed)],
                         ram_mb=10000, timeout_s=5 * 3600))
    for language in LANGUAGES:  # E5: raw, drop1, detector per language; SPC
        for seed in SEEDS:
            jobs.append(dict(args=["e5_scaffold_axis.run", "--workers", "4", "--seed", str(seed),
                                   "--languages", language], ram_mb=8000, timeout_s=4 * 3600))
    jobs.append(dict(args=["e2_span_bound.draws"], ram_mb=10000, timeout_s=3 * 3600))
    for seed in SEEDS:
        jobs.append(dict(args=["e1_fidelity_gap.d1_check", "--seed", str(seed)], ram_mb=10000, timeout_s=2 * 3600))
    return jobs


def stage() -> Path:
    staging = Path(tempfile.mkdtemp(prefix="seeds-stage-"))
    for item in SHIP:
        src = ROOT / item
        if src.is_dir():
            shutil.copytree(src, staging / item, ignore=shutil.ignore_patterns("__pycache__", "payload"))
        else:
            shutil.copy2(src, staging / item)
    return staging


def submit(name: str, dry_run: bool, priority: int) -> None:
    jobs = plan(name)
    if dry_run:
        print(json.dumps(jobs, indent=2))
        return
    from mrun.client.submit import launch

    staging = stage()
    records = json.loads(JOBS.read_text()) if JOBS.exists() else []
    for job in jobs:
        cmd = ["bash", "seeds/beast_job.sh", *job["args"]]
        job_id = launch(cmd, experiment=EXPERIMENT, payload=str(staging), gpu=False, pin="beast",
                        ram_mb=job["ram_mb"], vram_mb=0, cpu_threads=4, priority=priority, detach=True,
                        timeout_s=job["timeout_s"], note="unpaired-rosetta seed sweep: " + " ".join(job["args"]))
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
        log_dir = ROOT / "results" / "seeds" / "logs"
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
            prefix = next(k for k in sorted(OUT_DIR, key=len, reverse=True) if name.startswith(k))
            out = ROOT / "results" / OUT_DIR[prefix] / name
            out.write_text(json.dumps(receipt, indent=2) + "\n")
            record["receipt"] = str(out.relative_to(ROOT))
        record["collected"] = True
        print(record["job_id"], state, record.get("receipt", "NO RECEIPT"))
    JOBS.write_text(json.dumps(records, indent=2) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", choices=["smoke", "core", "gates", "gates-seeds", "full"])
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--priority", type=int, default=100)
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
