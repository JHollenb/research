"""Bounded compiled-C matrix: native CPU, six selectors and three raw-effect models."""
from __future__ import annotations

import argparse
import base64
import gc
import hashlib
import importlib
import json
import os
import platform
import re
import shutil
import signal
import statistics
import subprocess
import sys
import tarfile
import time
from pathlib import Path

ENTERED = time.perf_counter()
HERE = Path(__file__).resolve().parent
SELECTORS = ("nn", "pan_isa", "fieldlm", "spf_transformer", "mamba", "hydra")
ENGINES = ("pan_reference", *SELECTORS, "effect_nn", "effect_mamba", "effect_hydra")
FLAGS = ["-Os", "-std=c11", "-nostdlib", "-static", "-no-pie", "-fno-pie",
         "-fno-stack-protector", "-fno-asynchronous-unwind-tables", "-fcf-protection=none",
         "-Wl,--build-id=none,-e,_start"]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".writing")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n")
    temporary.replace(path)


def verify_source():
    data = json.loads(Path("source-manifest.json").read_text())
    for name, digest in data.items():
        if sha(name) != digest:
            raise ValueError(f"source identity changed: {name}")


def host_metadata():
    cpuinfo = Path("/proc/cpuinfo")
    cpu = next((line.split(":", 1)[1].strip() for line in cpuinfo.read_text().splitlines()
                if line.startswith("model name")), None) if cpuinfo.exists() else None
    return {"host": platform.node(), "platform": platform.platform(), "cpu_model": cpu,
            "logical_cpu_count": os.cpu_count(), "python_version": platform.python_version(),
            "compiler": command(["cc", "--version"]).stdout.splitlines()[0]}


def command(args, timeout=15):
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               text=True, start_new_session=True)
    try:
        stdout, stderr = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        # Native measurement and ptrace helpers fork. A deadline must terminate
        # the entire process group, including their measured/traced child.
        os.killpg(process.pid, signal.SIGKILL)
        stdout, stderr = process.communicate()
        raise subprocess.TimeoutExpired(args, timeout, output=stdout, stderr=stderr)
    if process.returncode:
        raise subprocess.CalledProcessError(process.returncode, args, output=stdout, stderr=stderr)
    return subprocess.CompletedProcess(args, process.returncode, stdout, stderr)


def disassemble(path):
    text = command(["objdump", "-d", "--no-show-raw-insn", str(path)]).stdout
    decoded = {}
    for line in text.splitlines():
        found = re.match(r"^\s*([0-9a-f]+):\s+([a-z][a-z0-9.]*)\s*(.*)$", line)
        if found:
            address, mnemonic, operands = found.groups()
            if mnemonic in ("rep", "repz", "repnz", "lock"):
                mnemonic += " " + operands.split()[0]
            decoded[int(address, 16)] = {"mnemonic": mnemonic, "operands": operands}
    return text, decoded


def compile_and_reference(config):
    out = Path("result")
    programs = out / "programs"
    programs.mkdir()
    command(["cc", "-O2", "native_measure.c", "-o", str(out / "native_measure")])
    command(["cc", "-O2", "trace_opmix.c", "-o", str(out / "trace_opmix")])
    manifest = json.loads(Path("programs/manifest.json").read_text())
    independent = json.loads(command([sys.executable, "programs/reference.py"]).stdout)
    for spec in manifest["apps"]:
        reference = independent[spec["id"]]
        if (reference["stdout_hex"] != spec["expected_stdout_hex"]
                or reference["exit_code"] != spec["expected_exit_code"]
                or sha(Path("programs") / spec["source"]) != spec["source_sha256"]):
            raise ValueError(f"independent reference or source mismatch: {spec['id']}")
    apps = []
    for spec in manifest["apps"]:
        app_id = spec["id"]
        elf = programs / f"{app_id}.elf"
        compile_command = ["cc", *FLAGS, f"programs/{spec['source']}", "-o", str(elf)]
        started = time.perf_counter()
        built = command(compile_command, timeout=30)
        compile_s = time.perf_counter() - started
        listing, instructions = disassemble(elf)
        (programs / f"{app_id}.disassembly.txt").write_text(listing)
        section_text = command(["size", "-A", str(elf)]).stdout
        sections = {}
        for line in section_text.splitlines():
            fields = line.split()
            if len(fields) >= 3 and fields[0].startswith(".") and fields[1].isdigit():
                sections[fields[0]] = int(fields[1])
        native_rows = []
        for repeat in range(config["native_repeats"]):
            stdout_file, stderr_file = out / "native.stdout", out / "native.stderr"
            row = json.loads(command([str((out / "native_measure").resolve()), str(elf.resolve()),
                                      str(stdout_file), str(stderr_file)], timeout=5).stdout)
            row.update(stdout_hex=stdout_file.read_bytes().hex(), stderr_hex=stderr_file.read_bytes().hex())
            row["wall_scope"] = "fork/exec through wait4 termination; excludes parent pipe capture/file writes"
            row["correct"] = (row["stdout_hex"] == spec["expected_stdout_hex"]
                              and row["exit_code"] == spec["expected_exit_code"] and not row["stderr_hex"])
            row["peak_rss_mib"] = row["maxrss_kib"] / 1024 if row["maxrss_kib"] > 0 else None
            native_rows.append(row)
        if not all(row["correct"] for row in native_rows):
            write(out / f"{app_id}-native-invalid.json", native_rows)
            raise RuntimeError(f"native/reference mismatch for {app_id}")
        trace_path = programs / f"{app_id}.opmix.txt"
        trace_status = {"status": "not-collected"}
        try:
            command([str((out / "trace_opmix").resolve()), str(trace_path), "200000", str(elf.resolve())], timeout=12)
            lines = trace_path.read_text().splitlines()
            head = lines[0].split()
            counts, missing = {}, []
            for line in lines[1:]:
                rip, count, raw = line.split()
                inst = instructions.get(int(rip, 16))
                if inst is None:
                    missing.append(rip)
                    continue
                name = inst["mnemonic"]
                counts[name] = counts.get(name, 0) + int(count)
            trace_status = {"status": head[3], "exit_code": int(head[4]), "dynamic_instructions": int(head[1]),
                            "distinct_executed_rips": len(lines) - 1, "dynamic_mnemonics": counts,
                            "undecoded_rips": missing,
                            "complete": head[3] == "exit" and int(head[4]) == spec["expected_exit_code"]}
        except subprocess.TimeoutExpired:
            trace_status = {"status": "timeout", "complete": False}
        item = {**spec, "elf_path": str(elf), "elf_sha256": sha(elf), "elf_bytes": elf.stat().st_size,
                "section_bytes": sections, "compile_command": compile_command, "compile_wall_s": compile_s,
                "compiler_stderr": built.stderr, "static_instruction_count": len(instructions),
                "static_mnemonics": sorted({x["mnemonic"] for x in instructions.values()}),
                "native_trace": trace_status, "native_samples": native_rows}
        apps.append(item)
        write(out / "apps.json", apps)
        print("MATRIX_APP:" + json.dumps({"app": app_id, "elf_bytes": item["elf_bytes"],
              "native_trace": trace_status}, sort_keys=True), flush=True)
    return apps


def fetch(memory, rip):
    result = bytearray()
    for offset in range(15):
        try:
            result.extend(memory.read(rip + offset, 1, access="execute", record=False))
        except Exception:
            break
    if not result:
        raise RuntimeError(f"unmapped instruction fetch at {rip:#x}")
    return bytes(result)


def run_effect(model, path, max_steps, context):
    # Only ELF loading and the established Linux write/exit boundary are supplied.
    from pan_x86_isa.process import load_elf64
    image = load_elf64(path)
    regs = [0] * 8
    regs[4] = image.initial_rsp
    state = {"regs": regs, "flags": {k: 0 for k in ("CF", "ZF", "SF", "OF")}, "rip": image.entry}
    stdout = bytearray()
    last = None
    for step in range(max_steps):
        before = state
        context.update(attempted_steps=step + 1, last_instruction={"address": hex(before["rip"])},
                       stdout_hex=stdout.hex())
        window = fetch(image.memory, before["rip"])
        last = {"address": hex(before["rip"]), "fetch_hex": window.hex(), "attempt": step + 1}
        context["last_instruction"] = last
        nxt = model.step(window, before)
        if nxt["store"]:
            image.memory.write(nxt["store_addr"], int(nxt["store_value"]).to_bytes(8, "little"), record=False)
        if nxt["syscall"]:
            # Same syscall convention as direct_effect.v2.run_program: current
            # arguments survive the OS boundary; the SYSCALL instruction is2 bytes.
            state = {"regs": list(before["regs"]), "flags": dict(before["flags"]), "rip": before["rip"] + 2}
            rax, rdi, rsi, rdx = state["regs"][0], state["regs"][7], state["regs"][6], state["regs"][2]
            if rax == 60:
                return {"stdout_hex": stdout.hex(), "stop": {"kind": "exit", "exit_code": rdi & 255},
                        "attempted_steps": step + 1, "last_instruction": last}
            if rax == 1 and rdi == 1 and rdx < 4096:
                stdout.extend(image.memory.read(rsi, rdx, record=False))
                state["regs"][0], state["regs"][1] = rdx, state["rip"]
            else:
                return {"stdout_hex": stdout.hex(), "stop": {"kind": "unsupported_syscall", "rax": rax},
                        "attempted_steps": step + 1, "last_instruction": last}
        else:
            state = {k: nxt[k] for k in ("regs", "flags", "rip")}
    return {"stdout_hex": stdout.hex(), "stop": {"kind": "step_limit"},
            "attempted_steps": max_steps, "last_instruction": last}


def run_selector(model, path, max_steps, context):
    api = importlib.import_module("pan_isa_x86_runtime_spf.runtime")
    runtime = api.SPFPrimaryPanRuntime.from_elf(path, model=model, backend="ps", trace_proposals=False)
    try:
        reason = runtime.run(max_steps=max_steps)
    except Exception:
        context.update(runtime_steps=runtime.steps, last_instruction={"address": hex(runtime.state.gpr["RIP"])},
                       stdout_hex=bytes(runtime.stdout).hex())
        raise
    try:
        raw = fetch(runtime.memory, runtime.state.gpr["RIP"]).hex()
    except Exception:
        raw = None
    return {"stdout_hex": bytes(runtime.stdout).hex(), "stop": reason.to_json(),
            "runtime_steps": runtime.steps, "model_transition_count": runtime.model_transition_count,
            "last_instruction": {"address": hex(runtime.state.gpr["RIP"]), "fetch_hex": raw}}


def classify(outcome, app):
    stop = outcome["stop"]
    if stop["kind"] == "exit":
        if outcome["stdout_hex"] == app["expected_stdout_hex"] and stop.get("exit_code") == app["expected_exit_code"]:
            return "success"
        return "wrong_output"
    if "unsupported" in stop["kind"]:
        return "refused"
    if stop["kind"] in ("step_limit", "max_steps"):
        return "step_limit"
    return "execution_fault"


def cell(args):
    import torch
    from isa_lab.measurement import Usage
    from pan_isa.native import mount

    torch.set_num_threads(1)
    torch.set_num_interop_threads(1)
    mount()
    app = json.loads(Path("result/apps.json").read_text())[args.app_index]
    config = json.loads(Path("matrix-config.json").read_text())
    engine = args.engine
    parse_started = time.perf_counter()
    artifact_path = Path("artifacts") / f"{engine}.json"
    artifact = json.loads(artifact_path.read_text()) if engine in SELECTORS else None
    parse_s = time.perf_counter() - parse_started
    with Usage() as load:
        if engine.startswith("effect_"):
            from newer_adapter import FrozenDirectEffect
            selector = FrozenDirectEffect(engine.removeprefix("effect_"), Path("artifacts") / engine)
            runtime_model = selector
            metadata = dict(selector.metadata)
        elif engine in SELECTORS:
            from isa_lab.full_training import restore
            from pan_isa.runtime_adapter import SharedRuntimeModel
            selector = restore(artifact)
            runtime_model = SharedRuntimeModel(selector)
            payload = selector.export()
            metadata = {k: payload[k] for k in ("parameter_count", "learned_record_count", "packed_plane_bytes") if k in payload}
            metadata.update(artifact_bytes=artifact_path.stat().st_size, artifact_sha256=sha(artifact_path),
                            implementation=selector.implementation,
                            tensor_state_bytes=sum(t.numel() * t.element_size() for t in selector.state_dict().values()
                                                   if isinstance(t, torch.Tensor)))
        else:
            selector, runtime_model = None, None
            metadata = {"parameter_count": 0, "artifact_bytes": 0, "implementation": "supplied PAN consumer control"}
    before = (json.dumps(selector.export(), sort_keys=True) if engine in SELECTORS else
              {k: v.detach().clone() for k, v in selector.model.state_dict().items()} if engine.startswith("effect_") else None)
    runner = run_effect if engine.startswith("effect_") else run_selector
    samples = []
    first_response_s = None
    for repeat in range(config["warm_repeats"] + 1):
        gc.collect()
        context = {}
        try:
            with Usage(sample_seconds=0.002) as usage:
                result = runner(runtime_model, Path(app["elf_path"]), config["max_steps"], context)
            result["status"] = classify(result, app)
        except Exception as error:
            result = {"status": "execution_error", "error_type": type(error).__name__, "error": str(error),
                      "stop": {"kind": "python_exception"}, **context}
        result.update(repeat=repeat, usage=usage.result)
        samples.append(result)
        if first_response_s is None:
            first_response_s = time.perf_counter() - ENTERED
        write(args.output, {"engine": engine, "app": app["id"], "metadata": metadata,
              "load_usage": load.result, "artifact_parse_s": parse_s, "first_response_from_script_entry_s": first_response_s,
              "samples": samples, "complete": False})
    if engine in SELECTORS:
        unchanged = before == json.dumps(selector.export(), sort_keys=True)
    elif engine.startswith("effect_"):
        unchanged = all(torch.equal(before[k], v) for k, v in selector.model.state_dict().items())
    else:
        unchanged = True
    if not unchanged:
        raise RuntimeError("serving changed the frozen artifact")
    final = {"engine": engine, "app": app["id"], "metadata": metadata, "load_usage": load.result,
             "artifact_parse_s": parse_s, "first_response_from_script_entry_s": first_response_s,
             "samples": samples, "complete": True, "artifact_unchanged": unchanged}
    write(args.output, final)


def pack():
    with tarfile.open("result.tar.gz", "w:gz", compresslevel=3) as archive:
        for p in sorted(Path("result").rglob("*")):
            if p.is_file():
                archive.add(p, arcname=str(p.relative_to("result")), recursive=False)
    raw = Path("result.tar.gz").read_bytes()
    encoded = base64.b64encode(raw).decode()
    for index, offset in enumerate(range(0, len(encoded), 3000)):
        print(f"ISA_ARCHIVE_CHUNK:{index}:{encoded[offset:offset + 3000]}", flush=True)
    print("ISA_ARCHIVE_SHA256:" + hashlib.sha256(raw).hexdigest(), flush=True)


def worker():
    verify_source()
    Path("result").mkdir(exist_ok=False)
    config = json.loads(Path("matrix-config.json").read_text())
    started = time.monotonic()
    try:
        apps = compile_and_reference(config)
        host = host_metadata()
        for app in apps:
            trace = app["native_trace"]
            if trace.get("complete") and trace["dynamic_instructions"] > config["max_steps"]:
                raise RuntimeError(f"instruction budget below native count: {app['id']}")
        rows = []
        # Rotate app order for each architecture. Every timed cell uses a fresh
        # child; all repetitions reinitialize the entire architectural process.
        for engine_index, engine in enumerate(config["engines"]):
            for offset in range(len(apps)):
                index = (engine_index + offset) % len(apps)
                app = apps[index]
                output = Path("result/cells") / f"{engine}-{app['id']}.json"
                if time.monotonic() - started > config["worker_budget_s"]:
                    rows.append({"engine": engine, "app": app["id"], "status": "budget_not_run"})
                    continue
                child_started = time.perf_counter()
                try:
                    completed = subprocess.run([sys.executable, "run_matrix.py", "cell", "--engine", engine,
                         "--app-index", str(index), "--output", str(output)], capture_output=True, text=True,
                         timeout=config["cell_timeout_s"])
                    row = json.loads(output.read_text()) if output.exists() else {"engine": engine, "app": app["id"]}
                    row.update(child_returncode=completed.returncode, child_stderr=completed.stderr[-4000:],
                               child_total_wall_s=time.perf_counter() - child_started)
                    if completed.returncode or not row.get("complete"):
                        row["status"] = "instrument_error"
                except subprocess.TimeoutExpired:
                    row = json.loads(output.read_text()) if output.exists() else {"engine": engine, "app": app["id"]}
                    row.update(status="timeout", child_total_wall_s=time.perf_counter() - child_started)
                rows.append(row)
                write("result/matrix.json", {"config": config, "apps": apps, "rows": rows, **host})
                print("MATRIX_CELL:" + json.dumps({"engine": engine, "app": app["id"],
                      "status": row.get("status", row.get("samples", [{}])[-1].get("status")),
                      "child_wall_s": row.get("child_total_wall_s")}), flush=True)
        write("result/matrix.json", {"config": config, "apps": apps, "rows": rows, **host})
        verify_source()
    except Exception as error:
        write("result/worker-error.json", {"type": type(error).__name__, "error": str(error)})
        raise
    finally:
        pack()


def launch(args):
    repo = HERE.parents[1]
    sys.path.insert(0, str(repo))
    from isa_lab.dependencies import WORKSPACE, namespace
    namespace("saturn", WORKSPACE / "saturn/src/saturn")
    from saturn.job_support import guarded_mrun_launch, one_lease_sequential_models_scheduling_contract

    config = {"schema": "isa-c-app-matrix-v1", "engines": args.engines, "warm_repeats": args.repeats,
              "native_repeats": 15, "cell_timeout_s": 10, "max_steps": 200000, "worker_budget_s": 420,
              "threads": 1, "device": "cpu", "seed": 673, "training_updates": 0,
              "scope": "Matched C-compiled freestanding ELF execution; native outputs checked independently; failures retained."}
    args.run_dir.mkdir(parents=True, exist_ok=False)
    payload = args.run_dir / "source"
    shutil.copytree(repo / "outputs/ssm-native-seed673/source", payload,
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "source-manifest.json", "preflight.v1.json"))
    for name in ("run_matrix.py", "native_measure.c", "newer_adapter.py"):
        shutil.copy2(HERE / name, payload / name)
    # The frozen source already has its older ELF fixtures under programs/.
    shutil.copytree(HERE / "programs", payload / "programs", dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    shutil.copy2(repo / "native_asm/trace_opmix.c", payload / "trace_opmix.c")
    (payload / "artifacts").mkdir()
    for name in SELECTORS:
        if name in args.engines:
            shutil.copy2(repo / f"outputs/ssm-native-seed673/result/{name}-673/model.json", payload / f"artifacts/{name}.json")
    if any(name.startswith("effect_") for name in args.engines):
        notes = json.loads((HERE / "newer/notes.json").read_text())
        newer_source = repo / notes["source_root"]
        shutil.copytree(newer_source / "direct_effect", payload / "direct_effect",
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        if sha(newer_source / "isa_lab/ssm.py") != sha(payload / "isa_lab/ssm.py"):
            raise ValueError("cannot mix selector and direct-effect SSM source identities")
        for arch, item in notes["models"].items():
            name = f"effect_{arch}"
            if name in args.engines:
                target = payload / "artifacts" / name
                target.mkdir()
                original = repo / item["artifact_dir"]
                shutil.copy2(original / "model.pt", target / "model.pt")
                write(target / "result.json", {"config": json.loads((original / "result.json").read_text())["config"]})
    write(payload / "matrix-config.json", config)
    roots = sorted(p.name for p in payload.iterdir())
    write(payload / "preflight.v1.json", {"path_token_allowlist": ["{env}", "result", "result.tar.gz"], "hashed_roots": roots})
    write(payload / "source-manifest.json", {str(p.relative_to(payload)): sha(p) for p in sorted(payload.rglob("*")) if p.is_file()})
    needs = {"cpu": True}
    request = {"schema": "isa-c-app-matrix-request-v1", "task_family": "inference", "device": "cpu",
          "needs": needs, "config": config, "source_manifest_sha256": sha(payload / "source-manifest.json"),
          "scheduling_contract": one_lease_sequential_models_scheduling_contract(
              model_processes=len(args.engines) * 4, task_family="inference", max_local_work_items=200,
              checkpoint_policy="One frozen architecture per fresh child/cell, serial CPU1; no fitting/fallback; four apps share exact ELF bytes.")}
    cmd = ["/usr/bin/env", "OMP_NUM_THREADS=1", "MKL_NUM_THREADS=1", "OPENBLAS_NUM_THREADS=1", "CUDA_VISIBLE_DEVICES=-1",
           "uv", "run", "--no-sync", "--project", "{env}", "python", "run_matrix.py", "worker"]
    write(args.run_dir / "request.json", {"request": request, "command": cmd})
    job = guarded_mrun_launch(cmd, request=request, experiment="isa-c-app-matrix", task="inference", model=None,
            payload=payload, prefer_host="beast", needs=needs, gpu=False, env_alias="mrun", preflight=True,
            retry_on_kill=False, timeout_s=600,
            note=f"Compiled-C matrix:4 apps, {len(args.engines)} frozen paths, serial CPU1. Each whole cell <=10s/200k instructions; first+{args.repeats} warm requests. Native reference and ptrace separately. No fitting, fallback, or per-model compiler changes; stop science at420s, finalize by600s.")
    write(args.run_dir / "submission.json", {"job_id": job})
    print(json.dumps({"job_id": job, "run_dir": str(args.run_dir)}), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("launch", "worker", "cell"))
    parser.add_argument("--run-dir", type=Path)
    parser.add_argument("--engines", nargs="+", choices=ENGINES, default=list(ENGINES))
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--engine", choices=ENGINES)
    parser.add_argument("--app-index", type=int)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.mode == "launch":
        launch(args)
    elif args.mode == "worker":
        worker()
    else:
        cell(args)


if __name__ == "__main__":
    main()
