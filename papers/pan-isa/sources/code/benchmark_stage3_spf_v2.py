#!/usr/bin/env python3
"""Benchmark a Stage 3 SPF-backed PAN variant against PAN v1 and QEMU.

PAN v1 calls the learned selector network once per instruction. This v2 keeps
the same Stage 3 semantics, but compiles the learned selector relation into SPF
artifacts:

* SPF scalar words store selector values and one-hot flag vectors.
* SPFTensor v2 and v3 blocks store the op x flag selector table.
* ``LowRankOperator`` instances act as per-op SPF block matrices for runtime
  selector routing.

The uninterrupted program is still executed sequentially because each x86 step
mutates registers, flags, and memory. The SPF path removes per-step PyTorch
forward calls while preserving the same learned selector surface.
"""
from __future__ import annotations

import argparse
import importlib
import json
import resource
import sys
import time
import types
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

import numpy as np
import torch

from pan_x86_stages.benchmark_stage3_uninterrupted import load_program, run_pan
from pan_x86_stages.stage0_x86_pan import DEFAULT_ARTIFACT_ROOT, hex_u, write_json
from pan_x86_stages.stage3_complex_scalar_pan import (
    FLAGS,
    OPS,
    FactorizedStage3PAN,
    memory_digest,
    transition_with_selector,
)

try:
    import psutil
except Exception:  # pragma: no cover - optional telemetry
    psutil = None


SPF_SRC = Path("/Users/jakeholl/domains/spectral-phase-format-research/src")
DEFAULT_PROGRAM_DIR = (
    DEFAULT_ARTIFACT_ROOT
    / "2026-06-16"
    / "pan-x86-isa"
    / "pan_vs_qemu_stage3_uninterrupted_flag_fixed"
)
DEFAULT_PROGRAM = DEFAULT_PROGRAM_DIR / "stage3_uninterrupted_program.json"
DEFAULT_PAN_V1_REPORT = DEFAULT_PROGRAM_DIR / "pan" / "pan_uninterrupted_report.json"
DEFAULT_QEMU_REPORT = DEFAULT_PROGRAM_DIR / "qemu" / "qemu_uninterrupted_report.json"
DEFAULT_RUN_DIR = (
    DEFAULT_ARTIFACT_ROOT
    / "2026-06-16"
    / "pan-x86-isa"
    / "stage3_complex_scalar"
    / "stage3-complex-scalar-continuous-flag-safe-v22-neural"
)
DEFAULT_OUT_DIR = (
    DEFAULT_ARTIFACT_ROOT
    / "2026-06-17"
    / "pan-x86-isa"
    / "pan_vs_qemu_stage3_spf_v2"
)
DEFAULT_REPORT_MD = Path("reports/pan_isa_spf_v2_comparison.md")
DEFAULT_REPORT_JSON = Path("reports/pan_isa_spf_v2_comparison.json")


@dataclass(frozen=True)
class SPFTensorModules:
    core: Any
    v2: Any
    v3: Any


def import_spf_tensor_modules(spf_src: Path = SPF_SRC) -> SPFTensorModules:
    """Import only the SPF tensor modules needed on Python 3.10.

    The local SPF package top-level imports optional runtime modules that require
    Python 3.11's ``enum.StrEnum``. The tensor implementation used here does not
    require those modules, so we install package shims and import the concrete
    tensor implementation files directly.
    """

    spf_pkg_root = spf_src / "spf"
    if not spf_pkg_root.exists():
        raise FileNotFoundError(f"SPF package source not found: {spf_pkg_root}")

    spf_pkg = sys.modules.get("spf")
    if spf_pkg is None or not hasattr(spf_pkg, "__path__"):
        spf_pkg = types.ModuleType("spf")
        spf_pkg.__path__ = [str(spf_pkg_root)]
        sys.modules["spf"] = spf_pkg

    tensor_pkg = sys.modules.get("spf.tensor")
    if tensor_pkg is None or not hasattr(tensor_pkg, "__path__"):
        tensor_pkg = types.ModuleType("spf.tensor")
        tensor_pkg.__path__ = [str(spf_pkg_root / "tensor")]
        sys.modules["spf.tensor"] = tensor_pkg

    core = importlib.import_module("spf.tensor.core")
    v2 = importlib.import_module("spf.tensor.v2")
    v3 = importlib.import_module("spf.tensor.v3")
    importlib.import_module("spf.tensor.reducers")
    importlib.import_module("spf.tensor.base_models")
    importlib.import_module("spf.tensor.residual_codecs")
    return SPFTensorModules(core=core, v2=v2, v3=v3)


def load_stage3_model(run_dir: Path) -> FactorizedStage3PAN:
    ckpt = torch.load(run_dir / "stage3_pan.pt", map_location="cpu")
    model = FactorizedStage3PAN()
    model.load_state_dict(ckpt["model_state"])
    return model.eval()


def flag_index(flags: Sequence[int]) -> int:
    idx = 0
    for bit, value in enumerate(flags):
        idx |= (int(value) & 1) << bit
    return idx


def one_hot_word(core: Any, index: int, width: int) -> np.ndarray:
    out = np.full(width, core.SPF32_WORD_ZERO, dtype=np.uint32)
    out[int(index)] = core.encode_words(np.asarray([1.0], dtype=np.complex128))[0]
    return out


@dataclass
class SPFSelectorBlockMatrix:
    """SPF-backed learned selector router for Stage 3.

    ``selector_table`` is indexed by ``[op_index, flag_bits]`` and stores the
    selector chosen by the learned Stage 3 model. The runtime path routes through
    one ``LowRankOperator`` per op, treating each op row as a 16x16 diagonal SPF
    block matrix over one-hot flag vectors.
    """

    spf: SPFTensorModules
    selector_table: np.ndarray
    selector_words: np.ndarray
    tensor_block_v2: Any
    tensor_block_v3: Any
    op_operators: Tuple[Any, ...]
    flag_inputs: Tuple[np.ndarray, ...]
    routed_selector_table: np.ndarray
    compile_elapsed_s: float
    parity: Mapping[str, bool]

    @classmethod
    def from_model(cls, model: torch.nn.Module, spf: SPFTensorModules) -> "SPFSelectorBlockMatrix":
        started = time.perf_counter()
        with torch.no_grad():
            op_indices: List[int] = []
            flag_rows: List[List[int]] = []
            for op_index in range(len(OPS)):
                for bits in range(1 << len(FLAGS)):
                    op_indices.append(op_index)
                    flag_rows.append([(bits >> bit) & 1 for bit in range(len(FLAGS))])
            op_tensor = torch.tensor(op_indices, dtype=torch.long)
            flag_tensor = torch.tensor(flag_rows, dtype=torch.float32)
            logits = model(op_tensor, flag_tensor)
            selector_table = logits.argmax(-1).cpu().numpy().astype(np.int64)
        selector_table = selector_table.reshape(len(OPS), 1 << len(FLAGS))

        core = spf.core
        selector_values = selector_table.astype(np.float64) + 1.0
        selector_words = core.encode_words(selector_values.astype(np.complex128))
        header = spf.v2.TensorBlockHeaderV2(dims=selector_words.shape)
        tensor_block_v2 = spf.v2.TensorBlock(
            header=header,
            dL=core.unpack_L(selector_words).reshape(-1),
            dT=core.unpack_theta(selector_words).astype(np.int16).reshape(-1),
        )
        v2_L, v2_T = tensor_block_v2.reconstruct()
        v2_words = core.pack_words(v2_L, v2_T)
        tensor_block_v3 = spf.v3.tensorblock_to_v3(tensor_block_v2)
        v3_words = tensor_block_v3.to_words()

        decoded_table = np.rint(core.decode_words(v3_words).real).astype(np.int64) - 1
        one = core.encode_words(np.asarray([1.0], dtype=np.complex128))[0]
        zero = core.SPF32_WORD_ZERO
        flag_inputs = tuple(one_hot_word(core, bits, 1 << len(FLAGS)) for bits in range(1 << len(FLAGS)))
        op_operators = []
        for row in selector_words:
            u = np.full((row.shape[0], row.shape[0]), zero, dtype=np.uint32)
            v = np.full((row.shape[0], row.shape[0]), zero, dtype=np.uint32)
            for idx, word in enumerate(row):
                u[idx, idx] = np.uint32(word)
                v[idx, idx] = np.uint32(one)
            lambdas = np.full(row.shape[0], one, dtype=np.uint32)
            op_operators.append(core.LowRankOperator(u, v, lambdas))

        routed_selector_table = np.zeros_like(selector_table)
        for op_index, operator in enumerate(op_operators):
            for bits, flag_input in enumerate(flag_inputs):
                routed = operator.apply_words(flag_input)
                decoded = core.decode_words(np.asarray([routed[bits]], dtype=np.uint32)).real[0]
                routed_selector_table[op_index, bits] = int(round(float(decoded))) - 1

        parity = {
            "v2_words_exact": bool(np.array_equal(v2_words, selector_words)),
            "v3_words_exact": bool(np.array_equal(v3_words, selector_words)),
            "decoded_selector_table_exact": bool(np.array_equal(decoded_table, selector_table)),
            "blockmatrix_routed_table_exact": bool(np.array_equal(routed_selector_table, selector_table)),
        }
        return cls(
            spf=spf,
            selector_table=selector_table,
            selector_words=selector_words,
            tensor_block_v2=tensor_block_v2,
            tensor_block_v3=tensor_block_v3,
            op_operators=tuple(op_operators),
            flag_inputs=flag_inputs,
            routed_selector_table=routed_selector_table,
            compile_elapsed_s=time.perf_counter() - started,
            parity=parity,
        )

    def route_selector(self, op_index: int, flags: Sequence[int], runtime_router: str = "compiled") -> int:
        bits = flag_index(flags)
        if runtime_router == "compiled":
            return int(self.routed_selector_table[int(op_index), bits])
        if runtime_router != "blockmatrix":
            raise ValueError(f"unsupported SPF runtime router: {runtime_router}")
        routed = self.op_operators[int(op_index)].apply_words(self.flag_inputs[bits])
        decoded = self.spf.core.decode_words(np.asarray([routed[bits]], dtype=np.uint32)).real[0]
        return int(round(float(decoded))) - 1

    def manifest(self, runtime_router: str) -> Dict[str, Any]:
        return {
            "spf_source": str(SPF_SRC),
            "selector_table_shape": list(self.selector_table.shape),
            "selector_table_words": int(self.selector_words.size),
            "selector_table_bytes": int(self.selector_words.nbytes),
            "flag_state_count": int(1 << len(FLAGS)),
            "op_operator_count": int(len(self.op_operators)),
            "op_operator_kind": "spf.tensor.core.LowRankOperator diagonal block matrix",
            "runtime_router": runtime_router,
            "runtime_router_note": "compiled uses the SPF block-matrix materialized table; blockmatrix applies LowRankOperator per instruction",
            "spftensor_v2": {
                "type": "spf.tensor.v2.TensorBlock",
                "dims": list(self.tensor_block_v2.header.dims),
                "metadata": self.tensor_block_v2.header.to_metadata(),
            },
            "spftensor_v3": {
                "type": "spf.tensor.v3.SPFBlockV3",
                "dims": list(self.tensor_block_v3.dims),
                "storage_bits": int(self.tensor_block_v3.storage_bits()),
                "base_model": int(self.tensor_block_v3.base.profile_id),
                "residual_codec": int(self.tensor_block_v3.residual.codec_id),
            },
            "compile_elapsed_s": round(self.compile_elapsed_s, 6),
            "parity": dict(self.parity),
        }


def process_rss_bytes() -> Optional[int]:
    if psutil is None:
        return None
    return int(psutil.Process().memory_info().rss)


def run_pan_v1_measured(program: Dict[str, Any], run_dir: Path) -> Dict[str, Any]:
    rss_before = process_rss_bytes()
    cpu_before = time.process_time()
    ru_before = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    report = run_pan(program, run_dir)
    report["cpu_time_s"] = round(time.process_time() - cpu_before, 6)
    report["rss_before_bytes"] = rss_before
    report["rss_after_bytes"] = process_rss_bytes()
    report["ru_maxrss_before"] = int(ru_before)
    report["ru_maxrss_after"] = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    return report


def run_pan_spf_v2(
    program: Dict[str, Any],
    run_dir: Path,
    spf_src: Path = SPF_SRC,
    runtime_router: str = "compiled",
) -> Dict[str, Any]:
    spf = import_spf_tensor_modules(spf_src)
    model = load_stage3_model(run_dir)
    router = SPFSelectorBlockMatrix.from_model(model, spf)

    regs = [int(x) for x in program["initial_stage3"]["regs"]]
    flags = [int(x) for x in program["initial_stage3"]["flags"]]
    memory: Optional[List[int]] = [int(x) & 0xFF for x in program["initial_stage3"]["memory"]]
    exact_steps = 0
    selector_exact = 0
    flag_compared = 0
    flag_exact = 0
    memory_checked = 0
    memory_exact = 0
    failures: List[Dict[str, Any]] = []

    rss_before = process_rss_bytes()
    cpu_before = time.process_time()
    ru_before = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    started = time.perf_counter()
    for step in program["steps"]:
        p = step["pan_stage3"]
        selector = router.route_selector(int(p["op_index"]), flags, runtime_router)
        try:
            pred_regs, pred_flags, pred_memory, aux = transition_with_selector(regs, flags, memory, step, selector)
        except Exception as exc:
            pred_regs, pred_flags, pred_memory = list(regs), list(flags), memory
            aux = {"selector": selector, "flag_mask": [0, 0, 0, 0], "error": f"{type(exc).__name__}: {exc}"}
        exp_regs = [int(x) for x in p["after_regs"]]
        exp_flags = [int(x) for x in p["after_flags"]]
        exp_memory = [int(x) & 0xFF for x in p["after_memory"]] if "after_memory" in p else memory
        mask = [int(x) for x in p["flag_mask"]]
        regs_ok = pred_regs == exp_regs
        flags_ok = all(int(m) == 0 or int(pred_flags[i]) == int(exp_flags[i]) for i, m in enumerate(mask))
        memory_ok = pred_memory == exp_memory
        selector_ok = int(aux["selector"]) == int(p["selector"])
        exception_ok = aux.get("exception") is None
        step_ok = regs_ok and flags_ok and memory_ok and selector_ok and exception_ok
        exact_steps += int(step_ok)
        selector_exact += int(selector_ok)
        if any(mask):
            flag_compared += 1
            flag_exact += int(flags_ok)
        if "after_memory" in p:
            memory_checked += 1
            memory_exact += int(memory_ok)
        if not step_ok and len(failures) < 10:
            failures.append(
                {
                    "index": int(step["index"]),
                    "op": OPS[int(p["op_index"])].name,
                    "selector": int(aux["selector"]),
                    "expected_selector": int(p["selector"]),
                    "regs_ok": regs_ok,
                    "flags_ok": flags_ok,
                    "memory_ok": memory_ok,
                    "exception_ok": exception_ok,
                }
            )
        regs, flags, memory = pred_regs, pred_flags, pred_memory
    elapsed = time.perf_counter() - started
    cpu_elapsed = time.process_time() - cpu_before
    ru_after = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    rss_after = process_rss_bytes()

    expected_final = program["final_stage3"]
    final_regs_ok = regs == [int(x) for x in expected_final["regs"]]
    final_memory_ok = memory_digest(memory or []) == program["final"]["memory_digest"]
    final_flags_ok = all(
        int(m) == 0 or int(flags[i]) == int(expected_final["flags"][i])
        for i, m in enumerate(expected_final["flag_mask"])
    )
    steps = len(program["steps"])
    return {
        "engine": "pan_stage3_spf_v2",
        "program": program["trace_id"],
        "checked_steps": steps,
        "exact_steps": exact_steps,
        "exact": round(exact_steps / max(1, steps), 6),
        "selector_exact": round(selector_exact / max(1, steps), 6),
        "flag_exact": round(flag_exact / max(1, flag_compared), 6) if flag_compared else 1.0,
        "memory_exact": round(memory_exact / max(1, memory_checked), 6) if memory_checked else 1.0,
        "memory_checked_steps": memory_checked,
        "final_exact": bool(final_regs_ok and final_flags_ok and final_memory_ok),
        "final_regs_ok": final_regs_ok,
        "final_flags_ok": final_flags_ok,
        "final_memory_ok": final_memory_ok,
        "elapsed_s": round(elapsed, 6),
        "steps_per_s": round(steps / elapsed, 2) if elapsed > 0 else None,
        "cpu_time_s": round(cpu_elapsed, 6),
        "rss_before_bytes": rss_before,
        "rss_after_bytes": rss_after,
        "ru_maxrss_before": int(ru_before),
        "ru_maxrss_after": int(ru_after),
        "failure_count": steps - exact_steps,
        "failure_examples": failures,
        "spf": router.manifest(runtime_router),
    }


def path_size(path: Path) -> int:
    if not path.exists():
        return 0
    if path.is_file():
        return path.stat().st_size
    return sum(p.stat().st_size for p in path.rglob("*") if p.is_file())


def load_json_if_exists(path: Path) -> Optional[Dict[str, Any]]:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def engine_row(
    name: str,
    report: Optional[Mapping[str, Any]],
    artifact: Path,
    extra_storage_bytes: int = 0,
) -> Dict[str, Any]:
    storage_bytes = path_size(artifact) + int(extra_storage_bytes)
    if report is None:
        return {
            "engine": name,
            "available": False,
            "artifact_path": str(artifact),
            "artifact_kind": "directory" if artifact.is_dir() else "file",
            "artifact_bytes": storage_bytes,
            "artifact_storage_bytes": storage_bytes,
        }
    steps = report.get("checked_steps") or report.get("result", {}).get("observed_steps")
    ok = report.get("ok")
    final_exact = report.get("final_exact")
    exact = report.get("exact")
    return {
        "engine": name,
        "available": True,
        "ok": bool(ok) if ok is not None else bool(final_exact and exact == 1.0),
        "exact": exact if exact is not None else (1.0 if ok else None),
        "final_exact": final_exact if final_exact is not None else bool(ok),
        "steps": int(steps) if steps is not None else None,
        "elapsed_s": report.get("elapsed_s"),
        "steps_per_s": report.get("steps_per_s"),
        "cpu_time_s": report.get("cpu_time_s"),
        "max_rss_bytes": report.get("max_child_rss_bytes") or report.get("rss_after_bytes"),
        "artifact_path": str(artifact),
        "artifact_kind": "directory" if artifact.is_dir() else "file",
        "artifact_bytes": storage_bytes,
        "artifact_storage_bytes": storage_bytes,
    }


def comparison_summary(
    program: Dict[str, Any],
    pan_v1: Mapping[str, Any],
    pan_spf: Mapping[str, Any],
    qemu: Optional[Mapping[str, Any]],
    out_dir: Path,
    pan_v1_artifact: Path,
    qemu_artifact: Path,
    run_dir: Path,
) -> Dict[str, Any]:
    model_bytes = path_size(run_dir / "stage3_pan.pt")
    spf_selector_bytes = int(pan_spf.get("spf", {}).get("selector_table_bytes", 0))
    rows = [
        engine_row("pan_stage3_v1", pan_v1, pan_v1_artifact, model_bytes),
        engine_row("pan_stage3_spf_v2", pan_spf, out_dir / "pan_spf_v2_report.json", model_bytes + spf_selector_bytes),
        engine_row("qemu_x86_64", qemu, qemu_artifact),
    ]
    for row in rows:
        if row["engine"] == "qemu_x86_64" and row.get("steps") is None and row.get("available"):
            row["steps"] = len(program["steps"])
    qemu_speed = next((r.get("steps_per_s") for r in rows if r["engine"] == "qemu_x86_64"), None)
    for row in rows:
        speed = row.get("steps_per_s")
        if speed and qemu_speed:
            row["qemu_speed_ratio"] = round(float(speed) / float(qemu_speed), 6)
            row["qemu_faster_by"] = round(float(qemu_speed) / float(speed), 3)
    fastest = max((r for r in rows if r.get("steps_per_s")), key=lambda r: float(r["steps_per_s"]))
    return {
        "program": {
            "trace_id": program["trace_id"],
            "instructions": len(program["steps"]),
            "program_byte_len": int(program["program"]["byte_len"]),
            "start_rip": hex_u(program["program"]["start_rip"], 64),
            "final_rip": hex_u(program["program"]["final_rip"], 64),
        },
        "comparison": rows,
        "fastest_engine": fastest["engine"],
        "notes": [
            "PAN v1 and SPF v2 elapsed times measure Python execution loops, not model/SPF compile time.",
            "QEMU report is the existing run for the same uninterrupted program and includes child RSS telemetry.",
            "PAN RSS is measured in the Python/Torch process; QEMU RSS is measured for the emulator child process.",
            "PAN storage includes the Stage 3 checkpoint; SPF v2 storage also includes its materialized selector table; QEMU storage includes the image/report directory.",
        ],
        "spf_v2": pan_spf.get("spf", {}),
    }


def render_markdown(summary: Mapping[str, Any]) -> str:
    program = summary["program"]
    rows = summary["comparison"]
    lines = [
        "# PAN-ISA SPF v2 Comparison",
        "",
        "## Program",
        "",
        f"- Trace: `{program['trace_id']}`",
        f"- Instructions: `{program['instructions']}`",
        f"- Program bytes: `{program['program_byte_len']}`",
        f"- RIP range: `{program['start_rip']}` -> `{program['final_rip']}`",
        "",
        "## Engines",
        "",
        "| Engine | Exact | Final | Elapsed s | CPU s | Steps/s | QEMU faster by | Storage bytes | Max RSS bytes |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in rows:
        lines.append(
            "| {engine} | {exact} | {final} | {elapsed} | {cpu} | {speed} | {qemu_by} | {bytes} | {rss} |".format(
                engine=row["engine"],
                exact=row.get("exact"),
                final=row.get("final_exact"),
                elapsed=row.get("elapsed_s"),
                cpu=row.get("cpu_time_s"),
                speed=row.get("steps_per_s"),
                qemu_by=row.get("qemu_faster_by", ""),
                bytes=row.get("artifact_bytes"),
                rss=row.get("max_rss_bytes", ""),
            )
        )
    spf = summary["spf_v2"]
    lines.extend(
        [
            "",
            "## SPF v2 Implementation",
            "",
            f"- SPF source: `{spf.get('spf_source')}`",
            f"- Selector table: `{spf.get('selector_table_shape')}`",
            f"- SPF scalar words: `{spf.get('selector_table_words')}`",
            f"- SPFTensor v2 block: `{spf.get('spftensor_v2', {}).get('type')}`",
            f"- SPFTensor v3 block: `{spf.get('spftensor_v3', {}).get('type')}`",
            f"- SPF block matrix router: `{spf.get('op_operator_kind')}`",
            f"- Compile time: `{spf.get('compile_elapsed_s')}` s",
            f"- Parity: `{spf.get('parity')}`",
            "",
            "## Notes",
            "",
        ]
    )
    lines.extend(f"- {note}" for note in summary.get("notes", []))
    lines.append("")
    return "\n".join(lines)


def cmd_run_spf(args: argparse.Namespace) -> int:
    args.out_dir.mkdir(parents=True, exist_ok=True)
    program = load_program(args.program)
    report = run_pan_spf_v2(program, args.run_dir, args.spf_src, args.runtime_router)
    write_json(args.out_dir / "pan_spf_v2_report.json", report)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["exact"] == 1.0 and report["final_exact"] and all(report["spf"]["parity"].values()) else 1


def cmd_compare_three(args: argparse.Namespace) -> int:
    args.out_dir.mkdir(parents=True, exist_ok=True)
    program = load_program(args.program)

    if args.rerun_pan_v1:
        pan_v1 = run_pan_v1_measured(program, args.run_dir)
        write_json(args.out_dir / "pan_v1_report.json", pan_v1)
        pan_v1_artifact = args.out_dir / "pan_v1_report.json"
    else:
        pan_v1 = load_json_if_exists(args.pan_v1_report)
        if pan_v1 is None:
            pan_v1 = run_pan_v1_measured(program, args.run_dir)
            write_json(args.out_dir / "pan_v1_report.json", pan_v1)
            pan_v1_artifact = args.out_dir / "pan_v1_report.json"
        else:
            pan_v1_artifact = args.pan_v1_report

    pan_spf = run_pan_spf_v2(program, args.run_dir, args.spf_src, args.runtime_router)
    write_json(args.out_dir / "pan_spf_v2_report.json", pan_spf)

    qemu = load_json_if_exists(args.qemu_report)
    summary = comparison_summary(
        program,
        pan_v1,
        pan_spf,
        qemu,
        args.out_dir,
        pan_v1_artifact,
        args.qemu_report.parent,
        args.run_dir,
    )
    write_json(args.out_dir / "comparison_summary.json", summary)
    if args.report_json:
        args.report_json.parent.mkdir(parents=True, exist_ok=True)
        write_json(args.report_json, summary)
    if args.report_md:
        args.report_md.parent.mkdir(parents=True, exist_ok=True)
        args.report_md.write_text(render_markdown(summary), encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    ok = pan_spf["exact"] == 1.0 and pan_spf["final_exact"] and all(pan_spf["spf"]["parity"].values())
    ok = ok and bool(pan_v1.get("final_exact")) and pan_v1.get("exact") == 1.0
    if qemu is not None:
        ok = ok and bool(qemu.get("ok"))
    return 0 if ok else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    run = sub.add_parser("run-spf")
    run.add_argument("--program", type=Path, default=DEFAULT_PROGRAM)
    run.add_argument("--run-dir", type=Path, default=DEFAULT_RUN_DIR)
    run.add_argument("--spf-src", type=Path, default=SPF_SRC)
    run.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    run.add_argument("--runtime-router", choices=("compiled", "blockmatrix"), default="compiled")
    run.set_defaults(func=cmd_run_spf)

    cmp = sub.add_parser("compare-three")
    cmp.add_argument("--program", type=Path, default=DEFAULT_PROGRAM)
    cmp.add_argument("--run-dir", type=Path, default=DEFAULT_RUN_DIR)
    cmp.add_argument("--spf-src", type=Path, default=SPF_SRC)
    cmp.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    cmp.add_argument("--pan-v1-report", type=Path, default=DEFAULT_PAN_V1_REPORT)
    cmp.add_argument("--qemu-report", type=Path, default=DEFAULT_QEMU_REPORT)
    cmp.add_argument("--rerun-pan-v1", action="store_true")
    cmp.add_argument("--runtime-router", choices=("compiled", "blockmatrix"), default="compiled")
    cmp.add_argument("--report-md", type=Path, default=DEFAULT_REPORT_MD)
    cmp.add_argument("--report-json", type=Path, default=DEFAULT_REPORT_JSON)
    cmp.set_defaults(func=cmd_compare_three)
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
