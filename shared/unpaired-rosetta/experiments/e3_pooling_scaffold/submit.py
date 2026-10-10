"""E3 step 2/3: submit the worker to the fleet with mrun, or collect a finished job.

    ~/domains/common/bin/common exec python e3_pooling_scaffold/submit.py --dry-run
    ~/domains/common/bin/common exec python e3_pooling_scaffold/submit.py
    ~/domains/common/bin/common exec python e3_pooling_scaffold/submit.py --collect job-XXXX

TODO(mrun-pub): this uses the private fleet client (``mrun.client.submit.launch``). Port to the public
``mrun-pub`` package so outside readers can rerun E3 on their own GPU; until then ``worker.py`` also runs
directly: ``python worker.py --data payload --device cuda`` in an env with torch + transformers.
"""

from __future__ import annotations

import argparse
import base64
import gzip
import hashlib
import json
import shutil
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULTS = HERE.parents[0] / "results" / "e3_pooling_scaffold"
MARKER = "UNPAIRED_ROSETTA_E3_REPORT_GZIP_B64="
EXPERIMENT = "unpaired-rosetta-e3-pooling-scaffold"
SHIPPED = ("worker.py", "their_geometry.py", "PREREG.md")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def collect(job_id: str) -> None:
    from mrun.client.api import Api

    api = Api()
    job = api.json("GET", f"/api/jobs/{job_id}", timeout_s=60)
    _, body, _ = api.request("GET", f"/api/jobs/{job_id}/logs?offset=0&wait_s=1", timeout_s=180)
    logs = body.decode("utf-8", "replace")
    out = RESULTS / job_id
    out.mkdir(parents=True, exist_ok=True)
    (out / "log.txt").write_text(logs)
    report = None
    for line in reversed(logs.splitlines()):
        if line.startswith(MARKER):
            report = json.loads(gzip.decompress(base64.b64decode(line[len(MARKER):].strip())))
            break
    receipt = {"job_id": job_id, "state": job.get("state"), "result": job.get("result"),
               "log_sha256": hashlib.sha256(logs.encode()).hexdigest(), "report_present": report is not None,
               "submission": json.loads((out / "submission.json").read_text()) if (out / "submission.json").exists()
               else None}
    (out / "run-receipt.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    if report is not None:
        (out / "report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"state": job.get("state"), "report": report is not None, "out": str(out)}, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="Qwen/Qwen3-1.7B")
    parser.add_argument("--items", type=int, default=2048)
    parser.add_argument("--corpora", nargs="*", default=["coco_train2014", "StanfordParagraphCaptioning"])
    parser.add_argument("--save-dir", default="/mnt/usb-storage/unpaired-rosetta-e3")  # never / on Beast
    parser.add_argument("--vram-mb", type=float, default=9000)  # ~1.5x expected peak for 1.7B bf16, batch 64
    parser.add_argument("--ram-mb", type=float, default=8000)  # must be declared too, else the server uses its probe default
    parser.add_argument("--priority", type=int, default=0)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--collect")
    args = parser.parse_args()
    if args.collect:
        collect(args.collect)
        return

    if not (HERE / "payload" / "manifest.json").exists():
        raise SystemExit("run `uv run python -m e3_pooling_scaffold.prepare` first")
    staging = Path(tempfile.mkdtemp(prefix="e3-stage-"))
    for name in SHIPPED:
        shutil.copy2(HERE / name, staging / name)
    shutil.copytree(HERE / "payload", staging / "payload")
    stamp = time.strftime("%Y%m%dT%H%M%S")
    cmd = ["uv", "run", "--project", "{env}", "python", "worker.py", "--data", "payload", "--model", args.model,
           "--items", str(args.items), "--corpora", *args.corpora, "--save-dir", f"{args.save_dir}/{stamp}"]
    submission = {
        "experiment": EXPERIMENT, "cmd": cmd, "model": args.model, "vram_mb": args.vram_mb, "ram_mb": args.ram_mb,
        "sha256": {name: sha(HERE / name) for name in SHIPPED},
        "payload_manifest": json.loads((HERE / "payload" / "manifest.json").read_text()),
        "note": (f"E3 pooling scaffold: {args.model} bf16, {len(args.corpora)} corpora x {args.items} items x "
                 "2 thinking modes, 128 greedy tokens, batch 64, + mean-pooling forwards; one model load; smoke gate "
                 "first; stop when both corpora report"),
    }
    if args.dry_run:
        print(json.dumps(submission, indent=2))
        return
    from mrun.client.submit import launch

    job_id = launch(cmd, experiment=EXPERIMENT, payload=str(staging), gpu=True, vram_mb=args.vram_mb, ram_mb=args.ram_mb,
                    priority=args.priority, note=submission["note"], detach=True, env_alias="mrun",
                    timeout_s=3 * 3600)
    out = RESULTS / str(job_id)
    out.mkdir(parents=True, exist_ok=True)
    (out / "submission.json").write_text(json.dumps(submission, indent=2, sort_keys=True) + "\n")
    print("submitted", job_id)


if __name__ == "__main__":
    main()
