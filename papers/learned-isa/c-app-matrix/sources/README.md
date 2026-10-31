# Compiled C versus frozen ISA architectures

This benchmark compiles four freestanding C micro-apps once on Linux x86-64 and
executes the identical ELF bytes natively, through six learned selector adapters,
and through three frozen R3 direct-effect models. A supplied PAN runtime control
separates shared instruction coverage from learned selection. No model is fitted
or repaired from these apps.

The workloads are Hello World, a straight-line checksum, insertion sort of 32
integers, and parsing/aggregating 80 CSV records. “Large” means the largest app in
this small suite. See [the workload manifest](programs/manifest.json) and
[independent references](programs/reference.py). Inline assembly supplies only
Linux write/exit; the application computations are C. There is no libc or dynamic
loader dependency.

## Run and collect

From the domains workspace:

```sh
rtk proxy common/bin/common exec python isa/benchmarks/c_apps/run_matrix.py launch \
  --run-dir isa/runs/c-app-matrix-<unique-name>
rtk proxy common/bin/common exec python isa/scripts/campaign_collect.py \
  isa/runs/c-app-matrix-<unique-name>
rtk proxy python3 isa/benchmarks/c_apps/summarize.py \
  isa/runs/c-app-matrix-<unique-name>/result/matrix.json \
  --output-dir isa/outputs/c-app-matrix-<unique-name>
```

The launcher uses mrun strict preflight, hashes the source/checkpoints, requests
CPU execution, and runs one architecture/app child at a time. Each whole cell
has a ten-second limit including imports, loading, first request and three warm
requests. Each request starts a fresh architectural process and has a 200,000
instruction limit. The worker stops starting science cells after 420 seconds;
the entire lease has a 600-second limit. Native helpers and traced descendants
are killed together on a deadline. All completed evidence is retained.

The October 30 full run is `job-007fe5d65603`, collected in
`runs/c-app-matrix-20261030-full/`. It completed in 60.3 seconds. The published
reading bundle is `../research/papers/learned-isa/c-app-matrix/` relative to the
ISA repository root.

## What is measured

- C file bytes, ELF bytes, `.text` bytes, static disassembly and dynamic native
  ptrace instruction/mnemonic counts describe the real compiled program. They
  are separate from the complete x86 instruction set or the learned profile.
- Native timing is fork/exec through wait4 termination. Parent pipe capture and
  file writes are excluded. There are 15 independently checked native trials.
- Model warm timing includes ELF loading, fresh runtime/memory setup, the
  adapter, model calls, supplied consumer/OS boundary, and small stop diagnostics.
  It excludes model loading and uses the three requests following the first.
- Instrumented first response starts at script entry after standard-library
  imports. It includes Torch/imports, artifact parsing/loading, integrity
  snapshots, collection and the first request. It is not pure inference latency.
- CPU seconds are process CPU time, including the memory sampler. RSS is sampled
  every 2 ms and includes Python, Torch, shared runtime and the model. Native RSS
  is the kernel's wait4 child high-water report. Neither is model tensor storage.
- Parameter counts, complete tensor-state bytes, structural records, packed
  planes and serialized artifact bytes remain separate. Selector artifacts use
  JSON; direct-effect weights use Torch serialization. These are not compression
  ratios against native code or hardware.

Only exact stdout plus terminal exit is a successful app result. Failed attempts
remain visible, with elapsed time to failure kept out of successful timing
comparisons. No intermediate hardware-state parity, energy, FLOPs, throughput
scaling or full ISA emulation is established by this suite.

## Supplied and learned components

The six selectors share a supplied binary decoder/typed architectural consumer
with 33 runtime family labels. They select operations; supplied code computes
their effects. The control uses that consumer without a learned selector.

The newer R3 models receive actual instruction bytes and their own eight
registers/four flags. They predict effects, length, stores and a syscall bit. They
have no general memory-load value input or branch-target head. ELF mapping and
the historical write/exit OS boundary are supplied. On a predicted syscall the
boundary preserves pre-instruction arguments/flags and advances RIP by two;
model stores are committed first. Output bytes for write are read by that OS
boundary. No candidate ALU, instruction parser or oracle after-state repairs the
model. The [adapter](newer_adapter.py) checks exact source/checkpoint identities.

The newer structural FieldLM/SPF microcode serving archive was unavailable in a
bounded lookup of its original successful job. It is **unmeasured**, rather than
a failed architecture; [retrieval provenance](newer/recovered-structural-job-d3ecda62fb95/retrieval-provenance.json)
records the distinction.

Two pilot runs are retained separately: the first exposed an incorrect diagnostic
CPU-state attribute in this harness; the second verified the corrected control
and FieldLM paths. Neither contributes samples to the full-run matrix.
