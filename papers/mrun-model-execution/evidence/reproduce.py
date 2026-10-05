"""Repeat the focused review in a NEW output directory using the common runtime.

The fleet tests start a temporary localhost service. No production scheduler job
is submitted, and pretrained-model tests remain disabled. Outcomes can depend on
local baseline memory pressure; historical logs are never overwritten.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", type=Path, default=Path(__file__).resolve().parents[4])
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=False)
    definitions = json.loads((Path(__file__).parent / "test-commands.json").read_text())
    results = []
    for lane, paths in definitions["suites"].items():
        command = ["rtk", "proxy", "env", "MRUN_RUN_MODEL_TESTS=0",
                   "HF_HUB_OFFLINE=1", "TRANSFORMERS_OFFLINE=1",
                   str(args.workspace / "common/bin/common"), "exec", "python", "-m", "pytest", "-q",
                   *paths, f"--junitxml={output / (lane + '.xml')}"]
        with (output / f"{lane}.log").open("w") as log:
            result = subprocess.run(command, cwd=args.workspace / "mrun", stdout=log, stderr=subprocess.STDOUT)
        results.append({"lane": lane, "returncode": result.returncode})
        print(f"{lane}: exit {result.returncode}; {output / (lane + '.log')}", flush=True)
    (output / "reproduction-results.json").write_text(json.dumps(results, indent=2) + "\n")


if __name__ == "__main__":
    main()
