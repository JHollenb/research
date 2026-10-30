#!/usr/bin/env python3
"""Benchmark Stage 3 PAN and QEMU on the same uninterrupted x86 program.

This is intentionally separate from the Stage 3 oracle validator. The validator
single-steps selected trace instructions with trampolines; this harness emits one
contiguous instruction stream and gives QEMU only one final capture trampoline.
"""
from __future__ import annotations

import argparse
import json
import math
import random
import shutil
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

import torch

from pan_x86_stages.stage0_x86_pan import DEFAULT_ARTIFACT_ROOT, DEFAULT_DATE, FLAGS, hex_u, write_json
from pan_x86_stages.stage3_complex_scalar_pan import (
    CODE_BASE,
    CPUID_FEATURES,
    FactorizedStage3PAN,
    MASK64,
    MEM_BASE,
    MEM_SIZE,
    NeuralStage3Predictor,
    OPS,
    REGS,
    make_step,
    memory_digest,
    random_flags,
    random_memory,
    random_regs,
)
from pan_x86_stages.validate_stage0_qemu import FLOPPY_IMAGE_BYTES, MAX_FLOPPY_STAGE_SECTORS, generate_boot_sector
from pan_x86_stages.validate_stage1_qemu import Code, ORIGIN, emit_enter_long_mode, emit_exit_hang64, emit_mov_reg_imm64, emit_puts64
from pan_x86_stages.validate_stage1_qemu import emit_memcheck64
from pan_x86_stages.validate_stage2_qemu import (
    HARNESS_STACK_ADDR,
    emit_copy_label_to_addr,
    emit_jmp_r11,
    emit_memset64,
    emit_mov_r11_imm64,
    emit_mov_rsp_imm64,
    emit_pushfq_from_word,
)
from pan_x86_stages.validate_stage3_emulator import (
    RESULT_ADDRS,
    TRAMPOLINE_BYTES,
    emit_compare_flags,
    emit_compare_memory_result,
    emit_compare_result64,
    emit_trampoline_blob,
    flags_word,
)


DEFAULT_RUN_DIR = (
    DEFAULT_ARTIFACT_ROOT
    / DEFAULT_DATE
    / "pan-x86-isa"
    / "stage3_complex_scalar"
    / "stage3-complex-scalar-base-alu-v21-neural"
)
DEFAULT_OUT_DIR = (
    DEFAULT_ARTIFACT_ROOT
    / DEFAULT_DATE
    / "pan-x86-isa"
    / "pan_vs_qemu_stage3_uninterrupted"
)
DEFAULT_PROGRAM = "stage3_uninterrupted_program.json"
DEFAULT_IMAGE = "stage3_uninterrupted_qemu.img"
CODE_BYTES_LIMIT = 0x100000
SERIAL_NAME = "qemu_uninterrupted_serial.log"
CONTINUOUS_UNSAFE_OP_PREFIXES = (
    "ADC_",
    "SBB_",
    "RCL_",
    "RCR_",
    "BSF_",
    "BSR_",
    "DIV_",
    "IDIV_",
    "MUL_",
    "IMUL_",
)


def u64(value: int) -> int:
    return int(value) & MASK64


def ensure_stage3_memory_constants() -> None:
    if MEM_BASE != 0x160000 or MEM_SIZE != 256:
        raise AssertionError("unexpected Stage 3 memory layout")


def flags_dict(flags: Sequence[int]) -> Dict[str, int]:
    return {name: int(flags[i]) for i, name in enumerate(FLAGS)}


def state_record(regs: Sequence[int], flags: Sequence[int], rip: int, memory: Sequence[int]) -> Dict[str, Any]:
    return {
        "rip": hex_u(rip, 64),
        "gpr": {reg: hex_u(regs[i], 64) for i, reg in enumerate(REGS)},
        "rflags": flags_dict(flags),
        "exception": None,
        "memory_digest": memory_digest(memory),
    }


def continuous_safe_op(op_name: str) -> bool:
    return not op_name.startswith(CONTINUOUS_UNSAFE_OP_PREFIXES)


def make_uninterrupted_trace(
    instructions: int,
    seed: int,
    split: str,
    code_bytes_limit: int,
    continuous_safe_only: bool,
) -> Dict[str, Any]:
    ensure_stage3_memory_constants()
    rng = random.Random(seed)
    regs = random_regs(rng, split)
    flags = random_flags(rng)
    flag_defined = [True for _ in FLAGS]
    memory = random_memory(rng, split)
    initial_regs = list(regs)
    initial_flags = list(flags)
    initial_memory = list(memory)
    rip = CODE_BASE
    steps: List[Dict[str, Any]] = []
    asm: List[str] = []
    bytes_parts: List[str] = []

    for index in range(instructions):
        accepted: Optional[Tuple[Dict[str, Any], List[int], List[int], List[int], int, str]] = None
        for _ in range(2000):
            candidate = make_step(index, split, list(regs), list(flags), list(memory), rip, rng, flag_defined)
            step = candidate[0]
            if step["pan_stage3"].get("exception") is not None:
                continue
            op_name = OPS[int(step["pan_stage3"]["op_index"])].name
            if continuous_safe_only and not continuous_safe_op(op_name):
                continue
            accepted = candidate
            break
        if accepted is None:
            raise RuntimeError(f"could not generate non-exception instruction at index {index}")
        step, regs, flags, memory, _unused_next_rip, asm_text = accepted
        fallthrough = int(step["pan_stage3"]["fallthrough_rip"])
        if fallthrough + TRAMPOLINE_BYTES - CODE_BASE > code_bytes_limit:
            raise ValueError(
                f"program exceeds code byte limit at instruction {index}: "
                f"{fallthrough + TRAMPOLINE_BYTES - CODE_BASE} > {code_bytes_limit}"
            )
        steps.append(step)
        asm.append(asm_text)
        bytes_parts.append(step["decode"]["bytes_hex"])
        flag_defined = [bool(x) for x in step["pan_stage3"]["after_flag_defined"]]
        rip = fallthrough

    program_bytes = "".join(bytes_parts)
    return {
        "schema_version": "pan-x86-uninterrupted-benchmark-v1",
        "trace_id": f"uninterrupted-{seed}-{instructions}",
        "stage": "stage3_complex_scalar",
        "source": {
            "generator": "benchmark_stage3_uninterrupted.py",
            "seed": seed,
            "oracle": ["internal_semantics"],
        },
        "mode": {
            "long_mode": True,
            "operand_bits": 64,
            "address_bits": 64,
            "ring": 0,
            "cpuid_features": list(CPUID_FEATURES),
        },
        "program": {
            "bytes_hex": program_bytes,
            "byte_len": len(bytes.fromhex(program_bytes)),
            "start_rip": CODE_BASE,
            "final_rip": rip,
            "asm": asm,
            "length": instructions,
            "template_id": "uninterrupted_contiguous_stage3",
            "continuous_safe_only": continuous_safe_only,
            "excluded_op_prefixes": list(CONTINUOUS_UNSAFE_OP_PREFIXES) if continuous_safe_only else [],
        },
        "initial": state_record(initial_regs, initial_flags, CODE_BASE, initial_memory),
        "initial_stage3": {
            "regs": initial_regs,
            "flags": initial_flags,
            "memory": initial_memory,
        },
        "steps": steps,
        "final": state_record(regs, flags, rip, memory),
        "final_stage3": {
            "regs": regs,
            "flags": flags,
            "memory": memory,
            "flag_mask": steps[-1]["pan_stage3"]["flag_mask"],
        },
    }


def load_program(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def run_pan(program: Dict[str, Any], run_dir: Path) -> Dict[str, Any]:
    ckpt = torch.load(run_dir / "stage3_pan.pt", map_location="cpu")
    model = FactorizedStage3PAN()
    model.load_state_dict(ckpt["model_state"])
    predictor = NeuralStage3Predictor(model)

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

    started = time.perf_counter()
    for step in program["steps"]:
        p = step["pan_stage3"]
        pred_regs, pred_flags, pred_memory, aux = predictor.predict_next(regs, flags, memory, step)
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

    expected_final = program["final_stage3"]
    final_regs_ok = regs == [int(x) for x in expected_final["regs"]]
    final_memory_ok = memory_digest(memory or []) == program["final"]["memory_digest"]
    final_flags_ok = all(
        int(m) == 0 or int(flags[i]) == int(expected_final["flags"][i])
        for i, m in enumerate(expected_final["flag_mask"])
    )
    steps = len(program["steps"])
    return {
        "engine": "pan_stage3",
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
        "failure_count": steps - exact_steps,
        "failure_examples": failures,
    }


def emit_fail_path(code: Code, reason: str) -> None:
    code.label(f"fail_{reason}")
    emit_mov_reg_imm64(code, "rsi", 0)
    code.fixups.append(("abs64", code.offset - 8, f"fail_msg_{reason}"))
    code.call32("puts64")
    code.jmp32("final_fail")


def generate_qemu_second_stage(program: Dict[str, Any], code_bytes_limit: int) -> bytes:
    program_bytes = bytes.fromhex(program["program"]["bytes_hex"])
    final_rip = int(program["program"]["final_rip"])
    if final_rip + TRAMPOLINE_BYTES - CODE_BASE > code_bytes_limit:
        raise ValueError("program plus final trampoline exceeds code byte limit")
    code = Code(ORIGIN)
    code_size = final_rip + TRAMPOLINE_BYTES - CODE_BASE
    initial = program["initial_stage3"]
    final = program["final_stage3"]

    emit_enter_long_mode(code)
    emit_memset64(code, CODE_BASE, 0x90, code_size)
    emit_copy_label_to_addr(code, "program_bytes", CODE_BASE, len(program_bytes))
    emit_copy_label_to_addr(code, "final_trampoline", final_rip, TRAMPOLINE_BYTES)
    emit_copy_label_to_addr(code, "initial_memory", MEM_BASE, MEM_SIZE)

    for reg_name, value in zip(("rax", "rbx", "rcx", "rdx"), initial["regs"]):
        emit_mov_reg_imm64(code, reg_name, int(value))
    emit_mov_rsp_imm64(code, HARNESS_STACK_ADDR)
    emit_pushfq_from_word(code, flags_word(initial["flags"]))
    emit_mov_r11_imm64(code, CODE_BASE)
    emit_jmp_r11(code)

    code.label("after_program")
    for reg_name, value in zip(("RAX", "RBX", "RCX", "RDX"), final["regs"]):
        emit_compare_result64(code, RESULT_ADDRS[reg_name], int(value), f"fail_{reg_name}")
    emit_compare_result64(code, RESULT_ADDRS["RIP"], final_rip, "fail_RIP")
    emit_compare_flags(code, final["flags"], final["flag_mask"], "fail_FLAGS")
    emit_compare_memory_result(code, MEM_BASE, "final_memory", "fail_MEMORY")
    emit_mov_reg_imm64(code, "rsi", 0)
    code.fixups.append(("abs64", code.offset - 8, "success_msg"))
    code.call32("puts64")
    emit_exit_hang64(code, "success_hang64")

    for reason in ("RAX", "RBX", "RCX", "RDX", "RIP", "FLAGS", "MEMORY"):
        emit_fail_path(code, reason)

    code.label("final_fail")
    emit_mov_reg_imm64(code, "rsi", 0)
    code.fixups.append(("abs64", code.offset - 8, "failure_result_msg"))
    code.call32("puts64")
    emit_exit_hang64(code, "failure_hang64")

    emit_puts64(code)
    emit_memcheck64(code)
    code.label("success_msg")
    code.emit_bytes(f"RESULT {len(program['steps'])} {len(program['steps'])} 0\n".encode("ascii") + b"\x00")
    code.label("failure_result_msg")
    code.emit_bytes(f"RESULT {len(program['steps'])} 0 1\n".encode("ascii") + b"\x00")
    for reason in ("RAX", "RBX", "RCX", "RDX", "RIP", "FLAGS", "MEMORY"):
        code.label(f"fail_msg_{reason}")
        code.emit_bytes(f"FAIL {reason}\n".encode("ascii") + b"\x00")

    code.label("program_bytes")
    code.emit_bytes(program_bytes)
    code.label("final_trampoline")
    emit_trampoline_blob(code, "final_trampoline_blob", "after_program", final_rip)
    code.label("initial_memory")
    code.emit_bytes(bytes(int(x) & 0xFF for x in initial["memory"]))
    code.label("final_memory")
    code.emit_bytes(bytes(int(x) & 0xFF for x in final["memory"]))
    return code.resolve()


def build_qemu_image(program: Dict[str, Any], image_path: Path, code_bytes_limit: int) -> Dict[str, Any]:
    second_stage = generate_qemu_second_stage(program, code_bytes_limit)
    sectors = math.ceil(len(second_stage) / 512)
    if sectors > MAX_FLOPPY_STAGE_SECTORS:
        raise ValueError(f"generated second stage needs {sectors} sectors; limit is {MAX_FLOPPY_STAGE_SECTORS}")
    boot = generate_boot_sector(sectors, load_addr=ORIGIN)
    padded_stage = second_stage + b"\x00" * (sectors * 512 - len(second_stage))
    image = boot + padded_stage
    if len(image) > FLOPPY_IMAGE_BYTES:
        raise ValueError(f"boot image exceeds 1.44MB floppy size: {len(image)} bytes")
    image = image + b"\x00" * (FLOPPY_IMAGE_BYTES - len(image))
    image_path.parent.mkdir(parents=True, exist_ok=True)
    image_path.write_bytes(image)
    return {
        "image_path": str(image_path),
        "image_bytes": len(image),
        "used_image_bytes": 512 + len(padded_stage),
        "floppy_image_bytes": FLOPPY_IMAGE_BYTES,
        "second_stage_bytes": len(second_stage),
        "second_stage_sectors": sectors,
        "program_byte_len": int(program["program"]["byte_len"]),
        "code_bytes": int(program["program"]["final_rip"]) + TRAMPOLINE_BYTES - CODE_BASE,
        "trampoline_bytes": TRAMPOLINE_BYTES,
    }


def parse_serial(serial: str, steps: int) -> Dict[str, Any]:
    failures = []
    checked = 0
    exact = 0
    failure_count = 0
    for line in serial.splitlines():
        parts = line.strip().split()
        if not parts:
            continue
        if parts[0] == "RESULT" and len(parts) == 4:
            checked = int(parts[1])
            exact = int(parts[2])
            failure_count = int(parts[3])
        elif parts[0] == "FAIL":
            failures.append(line.strip())
    return {
        "checked_steps": checked,
        "exact_steps": exact,
        "exact": round(exact / max(1, checked), 6),
        "failure_count": failure_count,
        "failure_examples": failures[:10],
        "ok": checked == steps and exact == steps and failure_count == 0,
    }


def qemu_command(binary: str, image_path: Path, serial_path: Path, cpu: str) -> List[str]:
    return [
        binary,
        "-display",
        "none",
        "-monitor",
        "none",
        "-serial",
        f"file:{serial_path}",
        "-boot",
        "a",
        "-no-reboot",
        "-no-shutdown",
        "-cpu",
        cpu,
        "-device",
        "isa-debug-exit,iobase=0xf4,iosize=0x01",
        "-drive",
        f"file={image_path},format=raw,if=floppy",
    ]


def cmd_generate(args: argparse.Namespace) -> int:
    args.out_dir.mkdir(parents=True, exist_ok=True)
    program = make_uninterrupted_trace(
        args.instructions,
        args.seed,
        args.split,
        args.code_bytes_limit,
        args.safe_op_subset,
    )
    path = args.out_dir / args.program_name
    write_json(path, program)
    summary = {
        "program_path": str(path),
        "trace_id": program["trace_id"],
        "instructions": len(program["steps"]),
        "program_byte_len": program["program"]["byte_len"],
        "start_rip": hex_u(program["program"]["start_rip"], 64),
        "final_rip": hex_u(program["program"]["final_rip"], 64),
        "memory_digest": program["final"]["memory_digest"],
    }
    write_json(args.out_dir / "program_summary.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


def cmd_run_pan(args: argparse.Namespace) -> int:
    args.out_dir.mkdir(parents=True, exist_ok=True)
    program = load_program(args.program)
    report = run_pan(program, args.run_dir)
    write_json(args.out_dir / "pan_uninterrupted_report.json", report)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["exact"] == 1.0 and report["final_exact"] else 1


def cmd_build_qemu(args: argparse.Namespace) -> int:
    args.out_dir.mkdir(parents=True, exist_ok=True)
    program = load_program(args.program)
    image_path = args.out_dir / args.image_name
    serial_path = args.out_dir / SERIAL_NAME
    serial_path.write_text("", encoding="utf-8")
    image_info = build_qemu_image(program, image_path, args.code_bytes_limit)
    qemu_binary = shutil.which(args.qemu_binary) or args.qemu_binary
    command = qemu_command(qemu_binary, image_path, serial_path, args.qemu_cpu)
    report = {
        "program": str(args.program),
        "image": image_info,
        "serial_path": str(serial_path),
        "qemu_command": command,
        "qemu_command_shell": " ".join(command),
    }
    write_json(args.out_dir / "qemu_uninterrupted_image.json", report)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


def cmd_parse_qemu(args: argparse.Namespace) -> int:
    program = load_program(args.program)
    serial = args.serial.read_text(encoding="utf-8", errors="replace")
    report = parse_serial(serial, len(program["steps"]))
    out = args.out or (args.serial.parent / "qemu_uninterrupted_report.json")
    write_json(out, report)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["ok"] else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    gen = sub.add_parser("generate")
    gen.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    gen.add_argument("--program-name", default=DEFAULT_PROGRAM)
    gen.add_argument("--instructions", type=int, default=8192)
    gen.add_argument("--seed", type=int, default=2026061701)
    gen.add_argument("--split", default="heldout_boundary")
    gen.add_argument("--code-bytes-limit", type=int, default=CODE_BYTES_LIMIT)
    gen.add_argument(
        "--safe-op-subset",
        action="store_true",
        help="Use the older coarse safe subset in addition to the flag-definedness guard.",
    )
    gen.set_defaults(func=cmd_generate)

    pan = sub.add_parser("run-pan")
    pan.add_argument("--program", type=Path, default=DEFAULT_OUT_DIR / DEFAULT_PROGRAM)
    pan.add_argument("--run-dir", type=Path, default=DEFAULT_RUN_DIR)
    pan.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    pan.set_defaults(func=cmd_run_pan)

    qemu = sub.add_parser("build-qemu")
    qemu.add_argument("--program", type=Path, default=DEFAULT_OUT_DIR / DEFAULT_PROGRAM)
    qemu.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    qemu.add_argument("--image-name", default=DEFAULT_IMAGE)
    qemu.add_argument("--qemu-binary", default="qemu-system-x86_64")
    qemu.add_argument("--qemu-cpu", default="max")
    qemu.add_argument("--code-bytes-limit", type=int, default=CODE_BYTES_LIMIT)
    qemu.set_defaults(func=cmd_build_qemu)

    parse = sub.add_parser("parse-qemu")
    parse.add_argument("--program", type=Path, default=DEFAULT_OUT_DIR / DEFAULT_PROGRAM)
    parse.add_argument("--serial", type=Path, default=DEFAULT_OUT_DIR / SERIAL_NAME)
    parse.add_argument("--out", type=Path, default=None)
    parse.set_defaults(func=cmd_parse_qemu)
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
