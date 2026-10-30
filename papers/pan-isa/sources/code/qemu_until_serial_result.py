#!/usr/bin/env python3
"""Run QEMU until a serial RESULT line appears, then terminate it."""
from __future__ import annotations

import argparse
import json
import subprocess
import time
from pathlib import Path
from typing import Any, Dict, Optional, Sequence

try:
    import psutil
except Exception:  # pragma: no cover - optional at runtime
    psutil = None  # type: ignore[assignment]


def parse_result(serial: str) -> Dict[str, Any]:
    for line in serial.splitlines():
        parts = line.strip().split()
        if parts and parts[0] == "RESULT" and len(parts) == 4:
            checked = int(parts[1])
            exact = int(parts[2])
            failures = int(parts[3])
            return {
                "found": True,
                "line": line.strip(),
                "checked_steps": checked,
                "exact_steps": exact,
                "failure_count": failures,
                "exact": round(exact / max(1, checked), 6),
                "ok": checked == exact and failures == 0,
            }
    return {"found": False, "ok": False}


def read_serial(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def run_until_result(command: Sequence[str], serial_path: Path, timeout_s: float, poll_s: float) -> Dict[str, Any]:
    serial_path.parent.mkdir(parents=True, exist_ok=True)
    serial_path.write_text("", encoding="utf-8")
    started = time.perf_counter()
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    child = psutil.Process(proc.pid) if psutil is not None else None
    max_rss = 0
    max_cpu = 0.0
    result: Dict[str, Any] = {"found": False, "ok": False}
    timed_out = False
    stopped_after_result = False
    try:
        if child is not None:
            child.cpu_percent(None)
        while True:
            if child is not None:
                try:
                    mem = child.memory_info()
                    max_rss = max(max_rss, int(mem.rss))
                    max_cpu = max(max_cpu, float(child.cpu_percent(None)))
                except psutil.Error:
                    pass
            serial = read_serial(serial_path)
            result = parse_result(serial)
            if result["found"]:
                stopped_after_result = True
                proc.terminate()
                break
            if proc.poll() is not None:
                break
            if time.perf_counter() - started > timeout_s:
                timed_out = True
                proc.terminate()
                break
            time.sleep(poll_s)
        try:
            stdout, stderr = proc.communicate(timeout=2.0)
        except subprocess.TimeoutExpired:
            proc.kill()
            stdout, stderr = proc.communicate(timeout=2.0)
    finally:
        if proc.poll() is None:
            proc.kill()
    elapsed = time.perf_counter() - started
    serial = read_serial(serial_path)
    result = parse_result(serial)
    return {
        "cmd": list(command),
        "serial_path": str(serial_path),
        "elapsed_s": round(elapsed, 6),
        "steps_per_s": round(result.get("checked_steps", 0) / elapsed, 2) if elapsed > 0 and result.get("checked_steps") else None,
        "returncode": proc.returncode,
        "timed_out": timed_out,
        "stopped_after_result": stopped_after_result,
        "max_child_rss_bytes": max_rss,
        "max_child_cpu_percent": max_cpu,
        "serial": serial,
        "stdout_tail": stdout[-2000:],
        "stderr_tail": stderr[-2000:],
        "result": result,
        "ok": bool(result.get("ok")) and stopped_after_result and not timed_out,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--serial", type=Path, required=True)
    parser.add_argument("--timeout-s", type=float, default=60.0)
    parser.add_argument("--poll-s", type=float, default=0.01)
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    command = list(args.command)
    if command and command[0] == "--":
        command = command[1:]
    if not command:
        raise SystemExit("missing command after --")
    report = run_until_result(command, args.serial, args.timeout_s, args.poll_s)
    if args.out is not None:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
