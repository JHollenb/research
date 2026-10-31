"""Summarize a collected C-app matrix without running or modifying experiments.

Usage: python summarize.py RESULT/matrix.json --output-dir ANALYSIS_DIRECTORY
Only summary.json and README.md in the analysis directory are written.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import statistics


APPS = ("tiny", "small", "medium", "large")
ENGINES = ("pan_reference", "nn", "pan_isa", "fieldlm", "spf_transformer",
           "mamba", "hydra", "effect_nn", "effect_mamba", "effect_hydra")
HOST_FIELDS = ("host", "platform", "cpu_model", "logical_cpu_count", "python_version", "compiler")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def finite(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value) and value >= 0


def median(values):
    values = [value for value in values if finite(value)]
    return statistics.median(values) if values else None


def usage_summary(samples):
    """Report medians and ranges; do not rename sampled RSS into peak allocation."""
    keys = ("wall_s", "cpu_s", "sampled_peak_rss_mb", "sampled_peak_delta_mb",
            "process_lifetime_peak_rss_mb", "cpu_core_equivalent_percent")
    result = {"sample_count": len(samples)}
    for key in keys:
        values = [sample.get("usage", {}).get(key) for sample in samples]
        values = [value for value in values if finite(value)]
        result[key] = {"n": len(values), "median": median(values),
                       "min": min(values) if values else None,
                       "max": max(values) if values else None}
    return result


def exact_sample(sample, app):
    stop = sample.get("stop", {})
    return (sample.get("status") == "success" and app is not None
            and sample.get("stdout_hex") == app.get("expected_stdout_hex")
            and stop.get("kind") == "exit"
            and stop.get("exit_code") == app.get("expected_exit_code"))


def sample_record(sample, app):
    # Copy the full recorded observation, adding an independent observable check.
    return {"observable_exact": exact_sample(sample, app), "recorded": sample}


def summarize_row(row, app, warm_count):
    samples = row.get("samples", [])
    first = [s for s in samples if s.get("repeat") == 0]
    warm = [s for s in samples if isinstance(s.get("repeat"), int) and s["repeat"] > 0]
    warm_ids = [s["repeat"] for s in warm]
    expected_ids = list(range(1, warm_count + 1))
    usable = (row.get("complete") is True and row.get("status") not in
              ("timeout", "instrument_error", "budget_not_run")
              and row.get("artifact_unchanged") is True)
    warm_exact = (usable and warm_count > 0 and sorted(warm_ids) == expected_ids
                  and all(exact_sample(s, app) for s in warm))
    statuses = Counter(s.get("status", "missing_status") for s in samples)
    if row.get("status"):
        status = row["status"]
    elif not samples:
        status = "missing_samples"
    elif not usable:
        status = "incomplete_or_unverified"
    elif len(statuses) == 1:
        status = next(iter(statuses))
    else:
        status = "mixed"
    if status == "success" and not all(exact_sample(s, app) for s in samples):
        status = "observable_mismatch"
    failures = [s for s in samples if not exact_sample(s, app)]
    display_status = status
    interpretation = None
    errors = [s.get("error", "") for s in failures]
    if row.get("engine") in ("fieldlm", "spf_transformer") and any(
            "field route missing" in error or "missing phase route" in error for error in errors):
        display_status = "missing route"
        interpretation = "Recorded execution_error is a missing learned route; not an instrument failure."
    elif str(row.get("engine", "")).startswith("effect_") and any(
            s.get("stop", {}).get("kind") == "unsupported_syscall" for s in failures):
        display_status = "predicted syscall failure"
        interpretation = ("The model-predicted syscall flag reached an unsupported call. The C fixtures use only write/exit; "
                          "this does not establish that another Linux service is needed.")
    first_sample = first[0] if len(first) == 1 else None
    return {
        "status": status, "display_status": display_status, "interpretation": interpretation,
        "recorded_row_status": row.get("status"),
        "complete": row.get("complete", False), "artifact_unchanged": row.get("artifact_unchanged"),
        "sample_status_counts": dict(sorted(statuses.items())), "sample_count": len(samples),
        "expected_sample_count": warm_count + 1,
        "warm_expected": warm_count, "warm_recorded": len(warm),
        "warm_observable_exact": sum(exact_sample(s, app) for s in warm),
        "successful_warm_timing_eligible": warm_exact,
        "successful_warm_usage": usage_summary(warm) if warm_exact else None,
        "first_observable_exact": exact_sample(first_sample, app) if first_sample else False,
        "first_response_from_script_entry_s": row.get("first_response_from_script_entry_s"),
        "first_sample": sample_record(first_sample, app) if first_sample else None,
        "failure_usage_diagnostics": usage_summary(failures) if failures else None,
        "failure_samples": [sample_record(s, app) for s in failures],
        "all_samples": [sample_record(s, app) for s in samples],
        "load_usage": row.get("load_usage"), "artifact_parse_s": row.get("artifact_parse_s"),
        "child_total_wall_s": row.get("child_total_wall_s"),
        "child_returncode": row.get("child_returncode"), "child_stderr": row.get("child_stderr"),
    }


def native_summary(app, expected_count):
    samples = app.get("native_samples", []) if app else []
    exact = [s for s in samples if (s.get("correct") is True
             and s.get("stdout_hex") == app.get("expected_stdout_hex")
             and s.get("exit_code") == app.get("expected_exit_code")
             and not s.get("signal") and not s.get("stderr_hex"))]
    eligible = len(samples) == expected_count and len(exact) == expected_count and expected_count > 0
    return {
        "status": "success" if eligible else "missing" if not samples else "incomplete_or_wrong",
        "expected_samples": expected_count, "recorded_samples": len(samples), "exact_samples": len(exact),
        "successful_wall_median_s": median(s.get("wall_s") for s in exact) if eligible else None,
        "successful_cpu_median_s": median(s.get("cpu_s") for s in exact) if eligible else None,
        "successful_rss_median_mib": median(s.get("peak_rss_mib") for s in exact) if eligible else None,
        "samples": samples,
    }


def summarize(data, input_path):
    config = data.get("config", {})
    warm_count, native_count = config.get("warm_repeats", 3), config.get("native_repeats", 15)
    apps_by_id = {app["id"]: app for app in data.get("apps", [])}
    apps = list(dict.fromkeys((*APPS, *apps_by_id)))
    rows = data.get("rows", [])
    engines = list(dict.fromkeys((*ENGINES, *config.get("engines", []), *(r.get("engine") for r in rows))))
    grouped = {}
    for index, row in enumerate(rows):
        grouped.setdefault((row.get("engine"), row.get("app")), []).append((index, row))
        if row.get("app") not in apps:
            apps.append(row.get("app"))
    cells = []
    for engine in engines:
        for app_id in apps:
            observations = grouped.get((engine, app_id), [])
            row_summaries = [summarize_row(row, apps_by_id.get(app_id), warm_count) for _, row in observations]
            status = ("duplicate_rows" if len(observations) > 1 else row_summaries[0]["status"] if observations
                      else "not_requested" if engine not in config.get("engines", engines) else "missing")
            cells.append({"engine": engine, "app": app_id, "status": status,
                          "raw_row_indices": [i for i, _ in observations], "observations": row_summaries})
    architectures = []
    for engine in engines:
        engine_rows = [r for r in rows if r.get("engine") == engine]
        variants = {}
        for row in engine_rows:
            metadata = row.get("metadata")
            if metadata:
                variants.setdefault(json.dumps(metadata, sort_keys=True), metadata)
        loads = [r["load_usage"] for r in engine_rows if isinstance(r.get("load_usage"), dict)]
        architectures.append({
            "engine": engine,
            "track": "direct-effect" if engine.startswith("effect_") else
                     "supplied consumer control" if engine == "pan_reference" else "selector",
            "artifact_format": "PyTorch checkpoint (.pt)" if engine.startswith("effect_") else
                               "none" if engine == "pan_reference" else "JSON export",
            "metadata_consistent": len(variants) == 1, "metadata_variants": list(variants.values()),
            "load_usage_across_cells": usage_summary([{"usage": u} for u in loads]),
            "artifact_parse_median_s": median(r.get("artifact_parse_s") for r in engine_rows),
        })
    app_summaries = []
    for app_id in apps:
        raw = apps_by_id.get(app_id)
        app_summaries.append({"id": app_id, "present": raw is not None,
            "source": raw.get("source") if raw else None,
            "source_sha256": raw.get("source_sha256") if raw else None,
            "source_bytes": raw.get("source_bytes") if raw else None,
            "elf_sha256": raw.get("elf_sha256") if raw else None,
            "elf_bytes": raw.get("elf_bytes") if raw else None,
            "section_bytes": raw.get("section_bytes", {}) if raw else {},
            "static_instruction_count": raw.get("static_instruction_count") if raw else None,
            "static_mnemonics": raw.get("static_mnemonics", []) if raw else [],
            "native_trace": raw.get("native_trace", {}) if raw else {},
            "compile_command": raw.get("compile_command") if raw else None,
            "compile_wall_s": raw.get("compile_wall_s") if raw else None,
            "expected_stdout_hex": raw.get("expected_stdout_hex") if raw else None,
            "expected_exit_code": raw.get("expected_exit_code") if raw else None,
            "native": native_summary(raw, native_count)})
    return {"schema": "isa-c-app-summary-v1", "generated_utc": datetime.now(timezone.utc).isoformat(),
            "source": {"path": str(input_path.resolve()), "sha256": sha(input_path),
                       "summarizer_sha256": sha(__file__), "raw_rows": len(rows)},
            "host": {k: data.get(k) for k in HOST_FIELDS}, "config": config,
            "apps": app_summaries, "architectures": architectures, "cells": cells,
            "methodology": {
                "successful_warm": "All requested warm repeats must be present, observable-exact, from a completed cell with unchanged artifact. No first request or failed sample enters the warm median.",
                "native": "All requested native repeats must match exact stdout and exit. Fork/exec through wait4 wall time, excluding parent pipe capture/file writes.",
                "requests": "Instrumented runner scope includes ELF/process initialization and execution, supplied ABI, and Usage sampler overhead; not pure model-forward time.",
                "cold": "Runner ENTERED timestamp (after standard-library imports) to first completed response, including Torch/runtime imports, artifact parsing/load, snapshot/export/GC, and first request. Excludes interpreter startup and earlier standard-library imports. Never called time to first token.",
                "load": "Median of per-cell instrumented load regions; selector JSON parse is separate, checkpoint deserialization is inside direct-effect load. Load regions may include lazy imports.",
                "memory": "Usage field names ending _mb are MiB. Request RSS is sampled whole-process RSS, includes Python/Torch, and is not weight bytes or an exact allocation peak. Native RSS is wait4 child maximum and may be unavailable for very short programs.",
                "dynamic_count": "Separate ptrace single-step run; not timed as native performance. Counts can treat REP iterations as multiple traps. Incomplete traces are not full-program instruction counts.",
                "artifact_bytes": "Selector artifact_bytes counts its JSON export; direct-effect artifact_bytes counts model.pt only, excluding companion config/result JSON. Formats and scopes differ; not total deployment size.",
                "failures": "Refusal, faults, wrong output, timeouts, missing cells, and instrument errors remain observations. Their time to stop is diagnostic, not successful execution performance or a speedup.",
            }}


def text(value):
    return "—" if value is None else str(value).replace("|", "\\|").replace("\n", " ")


def number(value, digits=3):
    return f"{value:.{digits}f}" if finite(value) else "—"


def ms(value):
    return number(value * 1000) if finite(value) else "—"


def measured(usage, key):
    return (usage or {}).get(key, {}).get("median")


def table(headers, rows):
    return "\n".join(["| " + " | ".join(headers) + " |",
                       "| " + " | ".join("---" for _ in headers) + " |",
                       *("| " + " | ".join(text(v) for v in row) + " |" for row in rows)]) + "\n"


def observation(cell):
    return cell["observations"][0] if len(cell["observations"]) == 1 else None


def outcome_label(cell):
    row = observation(cell)
    if row is None:
        return cell["status"]
    label = row["display_status"]
    if label != cell["status"]:
        label += f" [raw {cell['status']}]"
    counts = row["sample_status_counts"]
    detail = "" if len(counts) == 1 else "; " + ", ".join(f"{k} {v}" for k, v in counts.items())
    return f"{label} ({row['sample_count']}/{row['expected_sample_count']}{detail})"


def render(summary, output_dir):
    apps = summary["apps"]
    app_ids = [a["id"] for a in apps]
    engines = [a["engine"] for a in summary["architectures"]]
    cells = {(c["engine"], c["app"]): c for c in summary["cells"]}
    native = {a["id"]: a["native"] for a in apps}
    raw_link = os.path.relpath(summary["source"]["path"], output_dir).replace(os.sep, "/")
    lines = ["# Compiled C application matrix", "",
             f"Host: {text(summary['host'].get('cpu_model'))}; {text(summary['host'].get('host'))}; "
             f"{text(summary['host'].get('compiler'))}. CPU threads per model: {summary['config'].get('threads', 'unrecorded')}.", "",
             f"[Immutable collected matrix]({raw_link}) · [Machine-readable summary](summary.json). "
             f"Raw SHA-256: `{summary['source']['sha256']}`.", "",
             "The same compiled ELF is used for native execution and every architecture. Exact stdout and exit "
             "are rechecked from recorded samples. This is a bounded application-output result, not an intermediate-state proof. "
             "Selectors use supplied typed semantics; direct-effect paths predict effects and share the declared ELF/syscall boundary.", "",
             "## Outcomes", ""]
    rows = [["native", *(f"{native[a]['status']} ({native[a]['exact_samples']}/{native[a]['expected_samples']})" for a in app_ids)]]
    rows += [[e, *(outcome_label(cells[e, a]) for a in app_ids)] for e in engines]
    lines += [table(["Path", *app_ids], rows),
              "Model counts include the first request plus warm repeats. Missing, partial, timed-out, and instrument-error cells stay visible.", "",
              "## Successful warm wall time", "",
              "Milliseconds. Model medians require every requested warm repeat to succeed; first requests are excluded. "
              "Native uses all native repeats. A dash is no qualifying execution timing, never zero or a speedup. "
              "Native includes fork/exec-to-wait4 overhead; model requests include process-image initialization and sampled execution overhead. "
              "These are harness-path measurements, not matched instruction-only kernels.", ""]
    timing_rows = [["native", *(ms(native[a]["successful_wall_median_s"]) for a in app_ids)]]
    for e in engines:
        timing_rows.append([e, *(ms(measured((observation(cells[e, a]) or {}).get("successful_warm_usage"), "wall_s")) for a in app_ids)])
    lines += [table(["Path", *app_ids], timing_rows), "## Native reference measurements", "",
              table(["App", "Exact / recorded / expected", "Wall median ms", "CPU median ms", "Child max RSS median MiB"],
                    [[a, f"{native[a]['exact_samples']}/{native[a]['recorded_samples']}/{native[a]['expected_samples']}",
                      ms(native[a]["successful_wall_median_s"]), ms(native[a]["successful_cpu_median_s"]),
                      number(native[a]["successful_rss_median_mib"])] for a in app_ids]),
              "These short native processes include startup and termination. Similar medians across apps should not be read as an application-scaling curve.", "",
              "## Application size and instruction demand", "",
              table(["App", "C bytes", "ELF bytes", ".text bytes", "Static instructions", "Dynamic steps", "Executed RIPs", "Dynamic mnemonic kinds", "Trace"],
                    [[a["id"], a["source_bytes"], a["elf_bytes"], a["section_bytes"].get(".text"),
                      a["static_instruction_count"], a["native_trace"].get("dynamic_instructions"),
                      a["native_trace"].get("distinct_executed_rips"), len(a["native_trace"].get("dynamic_mnemonics", {})),
                      a["native_trace"].get("status", "missing") + ("; complete" if a["native_trace"].get("complete") else "; incomplete")]
                     for a in apps]),
              "C bytes count the app source, excluding the shared header. ELF bytes include sections and file overhead. "
              "Dynamic steps come from a separate ptrace single-step run; incomplete traces are partial observations. "
              "They are not model steps or performance timings.", ""]
    for app in apps:
        mix = app["native_trace"].get("dynamic_mnemonics", {})
        mix_text = ", ".join(f"`{k}` × {v}" for k, v in sorted(mix.items(), key=lambda item: (-item[1], item[0]))) or "unavailable"
        missing = app["native_trace"].get("undecoded_rips", [])
        lines += [f"- **{app['id']}** dynamic mix: {mix_text}. Undecoded RIPs: {len(missing)}."]
    lines += ["", "## Architecture payloads", "",
              "Exact counts from the recorded frozen specimen metadata. Unreported fields stay unavailable. "
              "Zero neural parameters in a record-based selector does not mean zero learned state. "
              "JSON export bytes and PyTorch checkpoint bytes have different serialization scopes; neither is whole-process RSS or full deployment size.", ""]
    metadata_rows, load_rows = [], []
    for architecture in summary["architectures"]:
        variants = architecture["metadata_variants"] or [{}]
        for index, metadata in enumerate(variants):
            name = architecture["engine"] + (f" variant {index + 1}" if len(variants) > 1 else "")
            metadata_rows.append([name, architecture["track"], metadata.get("parameter_count"),
                metadata.get("learned_record_count"), metadata.get("tensor_state_bytes"), metadata.get("packed_plane_bytes"),
                metadata.get("artifact_bytes"), architecture["artifact_format"]])
        load = architecture["load_usage_across_cells"]
        load_rows.append([architecture["engine"], load["sample_count"], ms(measured(load, "wall_s")),
                          ms(measured(load, "cpu_s")), ms(architecture["artifact_parse_median_s"]),
                          number(measured(load, "sampled_peak_rss_mb"))])
    lines += [table(["Architecture", "Track", "Parameters", "Learned records", "Tensor bytes", "Packed-plane bytes", "Artifact bytes", "Format"], metadata_rows),
              "## Load instrumentation", "",
              "Medians across fresh app cells, including loads before unsuccessful requests. Load scopes include lazy imports where applicable. "
              "Selector JSON parsing is outside its load region; direct-effect checkpoint deserialization is inside its load region. "
              "The artifact parse/setup field for control and direct-effect rows measures path setup without JSON loading.", "",
              table(["Architecture", "Load samples", "Load wall ms", "Load CPU ms", "Artifact parse/setup ms", "Load sampled RSS MiB"], load_rows),
              "## Successful first responses and request resources", "",
              "First response runs from the runner's ENTERED timestamp (after standard-library imports) to the first completed response, including Torch/runtime imports, artifact setup, load, snapshot/export, GC, and the first request. "
              "It excludes interpreter startup and earlier standard-library imports. First request CPU/wall cover the narrower runner region. "
              "RSS is sampled whole-process MiB; it includes Python/Torch. Warm columns require every requested warm repeat to succeed.", ""]
    success_rows, failure_rows = [], []
    for cell in summary["cells"]:
        row = observation(cell)
        if row is None:
            failure_rows.append([cell["engine"], cell["app"], cell["status"], "—", "—", "—", "—", "—", "no unique recorded row"])
            continue
        first = (row.get("first_sample") or {}).get("recorded", {})
        first_usage = first.get("usage", {})
        warm = row.get("successful_warm_usage")
        if row["first_observable_exact"]:
            success_rows.append([cell["engine"], cell["app"], ms(row["first_response_from_script_entry_s"]),
                ms(first_usage.get("wall_s")), ms(first_usage.get("cpu_s")), number(first_usage.get("sampled_peak_rss_mb")),
                ms(measured(warm, "cpu_s")), number(measured(warm, "sampled_peak_rss_mb")),
                number(measured(warm, "sampled_peak_delta_mb"))])
        if cell["status"] != "success" or row["failure_samples"]:
            failure = row.get("failure_usage_diagnostics")
            first_fail = not row["first_observable_exact"]
            examples = row["failure_samples"]
            example = examples[0]["recorded"] if examples else {}
            detail = (example.get("stop", {}).get("detail") or example.get("error") or row.get("child_stderr")
                      or json.dumps(example.get("stop", {}), sort_keys=True))
            if row.get("interpretation"):
                detail += "; " + row["interpretation"]
            failure_rows.append([cell["engine"], cell["app"], outcome_label(cell),
                ms(row["first_response_from_script_entry_s"]) if first_fail else "—",
                ms(measured(failure, "wall_s")), ms(measured(failure, "cpu_s")),
                number(measured(failure, "sampled_peak_rss_mb")), ms(row["child_total_wall_s"]), detail])
    lines += [table(["Architecture", "App", "First response ms", "First request wall ms", "First request CPU ms", "First sampled RSS MiB", "Warm CPU median ms", "Warm sampled RSS median MiB", "Warm sampled RSS delta median MiB"], success_rows),
              "## Failure and missing-data diagnostics", "",
              "Times below measure unsuccessful responses or time to stop. They are not execution speed measurements or speedups. "
              "Failure medians include only failed recorded samples; child wall time includes the whole cell process and may reflect a timeout. "
              "Full per-repeat stop reasons, stdout, last instructions, and usage remain in summary.json and the immutable source.", "",
              table(["Architecture", "App", "Outcome", "Failed first response ms", "Failure request wall median ms", "Failure CPU median ms", "Failure sampled RSS median MiB", "Whole cell wall ms", "First diagnostic"], failure_rows),
              "## Measurement scopes", ""]
    lines += [f"- **{key.replace('_', ' ')}:** {value}" for key, value in summary["methodology"].items()]
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("matrix", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    source, output = args.matrix.resolve(), args.output_dir.resolve()
    if output == source.parent:
        parser.error("choose a separate analysis directory; do not write into the collected raw directory")
    original_hash = sha(source)
    data = json.loads(source.read_text())
    result = summarize(data, source)
    output.mkdir(parents=True, exist_ok=True)
    products = {"summary.json": json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n",
                "README.md": render(result, output)}
    for name, content in products.items():
        target = output / name
        if target.resolve() == source:
            parser.error("output would overwrite the input matrix")
        temporary = target.with_name(target.name + ".writing")
        temporary.write_text(content)
        temporary.replace(target)
    if sha(source) != original_hash:
        raise RuntimeError("input changed during analysis; do not use the generated summary")
    print(json.dumps({"output_dir": str(output), "raw_sha256": original_hash,
                      "cells": len(result["cells"]), "input_unchanged": True}, sort_keys=True))


if __name__ == "__main__":
    main()
