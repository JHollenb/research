"""E6 generality sweep on Beast via mrun (CPU jobs). Adapted from seeds/submit.py.

    ~/domains/common/bin/common exec python e6_generality/submit.py --plan smoke [--dry-run]
    ~/domains/common/bin/common exec python e6_generality/submit.py --plan probe
    ~/domains/common/bin/common exec python e6_generality/submit.py --plan sweep0
    ~/domains/common/bin/common exec python e6_generality/submit.py --plan sweeds
    ~/domains/common/bin/common exec python e6_generality/submit.py --plan coco      # needs the 14 GB gen file
    ~/domains/common/bin/common exec python e6_generality/submit.py --collect

Each job runs `seeds/beast_job.sh <module> <args>` in the venv on /mnt/usb-storage (torch + their library at
fdfad84 + pylibmgm), prints its receipt into the job log, and `--collect` decodes it into results/e6_generality/.
CPU jobs, pinned to Beast. Priority 75.
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
JOBS = ROOT / "results" / "e6_generality" / "jobs.json"
EXPERIMENT = "unpaired-rosetta-e6-generality"
SHIP = ["pyproject.toml", "uv.lock", "common", "seeds", "e5_scaffold_axis", "e6_generality"]
GEN = "qwen3-8b-gen_69445574b3021b8a2733e87d8603d769"
ENCODERS = [GEN, "qwen3-embedding-8b", "mpnet"]
PRIMARY = ["DenselyCaptionedImages", "DOCCIDataset"]
CORPORA3 = ["StanfordParagraphCaptioning", "DenselyCaptionedImages", "DOCCIDataset"]


def manifest_sha256() -> str:
    files = sorted([HERE / "PREREG.md", HERE / "PREREG_E6b.md", HERE / "axis_probe.py", HERE / "sweep.py",
                    HERE / "transfer.py", HERE / "submit.py", HERE / "e6b_oracle.py", HERE / "e6b_transfer.py",
                    HERE / "e6b_ladder.py", HERE / "e6b_restarts.py"])
    out = {}
    for f in files:
        if f.exists():
            out[f.name] = hashlib.sha256(f.read_bytes()).hexdigest()
    return json.dumps(out, sort_keys=True)


def plan(name: str, sha: str) -> list[dict]:
    if name == "smoke":
        return [dict(args=["e6_generality.sweep", "--smoke", "--corpus", c, "--language", GEN,
                           "--candidates", "none", "pc0", "--manifest-sha256", sha], ram_mb=8000, timeout_s=3600)
                for c in PRIMARY]
    if name == "probe":
        return [dict(args=["e6_generality.axis_probe", "--corpus", c, "--manifest-sha256", sha],
                     ram_mb=6000, timeout_s=1800) for c in PRIMARY]
    if name == "sweep0":  # seed-0 full 6-candidate sweep, every encoder, both primary corpora
        return [dict(args=["e6_generality.sweep", "--corpus", c, "--language", e, "--workers", "4",
                           "--manifest-sha256", sha], ram_mb=9000, timeout_s=3 * 3600)
                for c in PRIMARY for e in ENCODERS]
    if name == "sweeds":  # gen none+pc0 at seeds 1,2 (the paper-relevant fix claim), both primary corpora
        return [dict(args=["e6_generality.sweep", "--corpus", c, "--language", GEN, "--candidates", "none", "pc0",
                           "--seed", str(seed), "--workers", "4", "--manifest-sha256", sha],
                     ram_mb=9000, timeout_s=3 * 3600) for c in PRIMARY for seed in (1, 2)]
    if name == "p3fast":  # fast none+pc0 at seed 0 for all 6 cells + DOCCI gen seeds 1,2 (low-contention)
        jobs = [dict(args=["e6_generality.sweep", "--corpus", c, "--language", e, "--candidates", "none", "pc0",
                           "--workers", "4", "--manifest-sha256", sha], ram_mb=9000, timeout_s=2 * 3600)
                for c in PRIMARY for e in ENCODERS]
        jobs += [dict(args=["e6_generality.sweep", "--corpus", "DOCCIDataset", "--language", GEN,
                            "--candidates", "none", "pc0", "--seed", str(seed), "--workers", "4",
                            "--manifest-sha256", sha], ram_mb=9000, timeout_s=2 * 3600) for seed in (1, 2)]
        return jobs
    if name == "rerun":  # after the bf16 unit-norm gate fix: the controls (both corpora) + all DOCCI gen
        jobs = [dict(args=["e6_generality.sweep", "--corpus", c, "--language", e, "--workers", "4",
                           "--manifest-sha256", sha], ram_mb=9000, timeout_s=3 * 3600)
                for c in PRIMARY for e in ("qwen3-embedding-8b", "mpnet")]
        jobs += [dict(args=["e6_generality.sweep", "--corpus", "DOCCIDataset", "--language", GEN, "--workers", "4",
                            "--manifest-sha256", sha], ram_mb=9000, timeout_s=3 * 3600)]
        jobs += [dict(args=["e6_generality.sweep", "--corpus", "DOCCIDataset", "--language", GEN,
                            "--candidates", "none", "pc0", "--seed", str(seed), "--workers", "4",
                            "--manifest-sha256", sha], ram_mb=9000, timeout_s=3 * 3600) for seed in (1, 2)]
        return jobs
    if name == "docci_gen":  # re-run only DOCCI gen (seed-0 full sweep + seeds 1,2 none+pc0) after a gate fix
        jobs = [dict(args=["e6_generality.sweep", "--corpus", "DOCCIDataset", "--language", GEN, "--workers", "4",
                           "--manifest-sha256", sha], ram_mb=9000, timeout_s=3 * 3600)]
        jobs += [dict(args=["e6_generality.sweep", "--corpus", "DOCCIDataset", "--language", GEN,
                            "--candidates", "none", "pc0", "--seed", str(seed), "--workers", "4",
                            "--manifest-sha256", sha], ram_mb=9000, timeout_s=3 * 3600) for seed in (1, 2)]
        return jobs
    if name == "coco_probe":  # secondary short-caption control: within-COCO axis probe (needs the gen file)
        return [dict(args=["e6_generality.axis_probe", "--corpus", "coco_val2014", "--manifest-sha256", sha],
                     ram_mb=44000, timeout_s=3600)]
    if name == "coco":  # within-COCO sweep (only if the probe shows the axis is present); may be slow
        return [dict(args=["e6_generality.sweep", "--corpus", "coco_val2014", "--language", e, "--holdout", "2000",
                           "--workers", "4", "--manifest-sha256", sha], ram_mb=20000, timeout_s=5 * 3600)
                for e in ENCODERS]
    if name == "transfer":  # secondary: map fit on SPC gen, eval on COCO-val gen, raw vs PC0-removed
        return [dict(args=["e6_generality.transfer", "--eval-corpus", "coco_val2014", "--workers", "2",
                           "--manifest-sha256", sha], ram_mb=44000, timeout_s=4 * 3600)]
    # ---- E6b (fix-diagnosis addendum) ----
    if name == "oracle":  # DECISIVE: true-pair oracle ceilings (orth + lin), all cells, one job
        return [dict(args=["e6_generality.e6b_oracle", "--manifest-sha256", sha], ram_mb=9000, timeout_s=1800)]
    if name == "transfer2":  # secondary P6, chunked COCO reduce
        return [dict(args=["e6_generality.e6b_transfer", "--eval-corpus", "coco_val2014", "--workers", "4",
                           "--manifest-sha256", sha], ram_mb=24000, timeout_s=3 * 3600)]
    if name == "ladder":  # part 3 (geometry branch): drop-k ladder k=2,3,4, one job per corpus
        return [dict(args=["e6_generality.e6b_ladder", "--corpus", c, "--ks", "2", "3", "4", "--workers", "4",
                           "--manifest-sha256", sha], ram_mb=9000, timeout_s=2 * 3600) for c in CORPORA3]
    if name == "genpcs":  # finish the promised pc1-pc4 individual-PC ladder for gen on DCI+DOCCI (sweep.py, fixed)
        jobs = []
        for c in PRIMARY:
            for cands in (["pc1", "pc2"], ["pc3", "pc4"]):
                jobs.append(dict(args=["e6_generality.sweep", "--corpus", c, "--language", GEN, "--candidates",
                                       *cands, "--workers", "4", "--manifest-sha256", sha],
                                 ram_mb=9000, timeout_s=2 * 3600))
        return jobs
    if name == "restarts":  # part 2 (search branch): gen-pc0 restarts seeds 3-7, split per corpus into 3+2
        jobs = []
        for c in ("DenselyCaptionedImages", "DOCCIDataset"):
            for seeds in (["3", "4", "5"], ["6", "7"]):
                jobs.append(dict(args=["e6_generality.e6b_restarts", "--corpus", c, "--seeds", *seeds,
                                       "--workers", "4", "--manifest-sha256", sha], ram_mb=9000, timeout_s=2 * 3600))
        return jobs
    raise SystemExit(f"unknown plan {name}")


def stage() -> Path:
    staging = Path(tempfile.mkdtemp(prefix="e6-stage-"))
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
        # note has a 500-char server cap; drop the long --manifest-sha256 value (it is recorded in the receipt)
        args = job["args"]
        if "--manifest-sha256" in args:
            i = args.index("--manifest-sha256")
            args = args[:i] + args[i + 2:]
        note = ("e6 generality: " + " ".join(args))[:500]
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
        log_dir = ROOT / "results" / "e6_generality" / "logs"
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
            out = ROOT / "results" / "e6_generality" / name
            out.write_text(json.dumps(receipt, indent=2) + "\n")
            record["receipt"] = str(out.relative_to(ROOT))
        record["collected"] = True
        print(record["job_id"], state, record.get("receipt", "NO RECEIPT"))
    JOBS.write_text(json.dumps(records, indent=2) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", choices=["smoke", "probe", "sweep0", "sweeds", "p3fast", "rerun", "docci_gen", "coco_probe", "coco", "transfer", "oracle", "transfer2", "ladder", "restarts", "genpcs"])
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
