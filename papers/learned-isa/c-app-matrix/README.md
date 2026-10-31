# Compiled C versus our ISA architectures

**Five frozen learned models run the compiled Hello World correctly: FieldLM and
SPF selectors, plus the newer NN, Mamba and Hydra direct-effect models. None
completes the three larger C apps in this run.** Native x86-64 completes all four.
The supplied runtime control also stops on those larger apps, exposing a shared
instruction-coverage limit before a broad architecture comparison is possible.

This October 30, 2026 experiment uses identical ELF bytes for every architecture.
The full mrun job, `job-007fe5d65603`, finished in **60.3 seconds** on the beast's
AMD Ryzen 9 7950X, using CPU execution and one Torch compute thread. It collected
60 native trials and 160 model/control trials: 40 cells, each with a first request
and three warm repeats. Every cell completed within its ten-second deadline;
frozen artifacts remained unchanged. No training was performed.
Each learned path uses one frozen seed-673 specimen; this is a bounded comparison,
not an architecture-wide ranking.

## The matrix

Times are milliseconds. Model times are medians of the **three successful warm
requests**; all displayed model successes also passed the first request, giving
4/4 successful trials. Native times are medians of 15/15 successful processes.
Failure cells intentionally have no completion time.

| Execution path | Tiny: Hello | Small: checksum | Medium: sort | Large: records |
|---|---:|---:|---:|---:|
| Native compiled C / x86-64 | **0.235** | **0.234** | **0.230** | **0.232** |
| Supplied PAN runtime control | **2.604** | Coverage stop | Coverage stop | Coverage stop |
| NN selector | Selection stop | Selection stop | Selection stop | Selection stop |
| Original PAN selector | Selection stop | Coverage stop | Coverage stop | Selection stop |
| FieldLM selector | **2.984** | Missing route | Missing route | Missing route |
| SPF selector / packed route planes | **3.945** | Missing route | Missing route | Missing route |
| Mamba selector | Selection stop | Selection stop | Selection stop | Coverage stop |
| Hydra selector | Selection stop | Coverage stop | Coverage stop | Coverage stop |
| Newer NN direct effects, R3 | **8.215** | Predicted store fault | Predicted store fault | Predicted store fault |
| Newer Mamba direct effects, R3 | **14.478** | Predicted syscall failure | Predicted store fault | Predicted store fault |
| Newer Hydra direct effects, R3 | **19.553** | Predicted syscall failure | Predicted store fault | Predicted store fault |
| Newer structural FieldLM/SPF microcode | Unmeasured | Unmeasured | Unmeasured | Unmeasured |

“Selection stop” includes low confidence or a selected operation disagreeing with
the typed adapter. “Coverage stop” means the supplied consumer rejects that
encoding. Structural missing routes surface as exceptions in the original APIs;
they are preserved as `execution_error` in the raw record. The newer structural
microcode serving archive could not be retrieved from its original successful
job; that row is an evidence-availability limit, not a measured failure.

## Real instruction size and app difficulty

These are deliberately small, freestanding C applications. “Large” is relative
to this suite: 80 records, not a large production application. Application
arithmetic, sorting and parsing are C; inline assembly only makes Linux write
and exit syscalls. GCC 13.3 compiles each app once with the same `-Os` flags,
without libc or a dynamic loader. Independent Python references check exact
stdout bytes and exit status.
Tiny preserves the earlier known Hello source. It is an execution/regression
case, not a held-out generalization test.

| App | Work | C file bytes¹ | ELF bytes | Machine code `.text` bytes | Executed native instructions² | Executed mnemonic labels |
|---|---|---:|---:|---:|---:|---:|
| Tiny | Write “Hello, world!” and exit | 521 | 8,968 | 29 | 8 | 3 |
| Small | 24 updates of four 64-bit values; checksum | 684 | 9,056 | 619 | 108 | 9 |
| Medium | Insertion-sort 32 integers; digest | 1,043 | 9,080 | 184 | 3,115 | 18 |
| Large | Parse 1,053 CSV bytes / 80 records; aggregate eight buckets | 3,200 | 10,216 | 269 | 12,313 | 25 |

¹ C file only; the shared syscall header is additional for the three larger apps.
² Ptrace single-step counts collected separately from timing. The collected
disassemblies and address/count traces retain the actual encodings. Mnemonic
labels, encoding forms, static instructions and dynamic instructions are
different counts. Straight-line checksum code is larger than the loop-based
apps even though it executes fewer instructions.

“Real ISA size” has two useful meanings here. The table measures the **actual x86
machine-code bytes and instruction use of each app**. The model profiles are
separate: the selector consumer exposes 33 runtime family labels, and the R3
direct-effect generator defines 28 encoding forms. Neither count describes the
complete x86-64 ISA, and families/forms are not interchangeable units. Native
hardware has no learned parameter file to compare with neural weights; its
implementation area and microcode storage were not measured.

## Learned state and storage

These counts describe the **exact specimens executed**, not historical averages.
Tensor-state bytes include buffers. Serialized selector JSON and direct-effect
Torch checkpoints have different format overhead; the artifact column excludes
shared code, Python/Torch and the direct-effect configuration JSON.

| Architecture | Track | Trainable parameters | Learned records | Tensor-state bytes | Serialized artifact bytes |
|---|---|---:|---:|---:|---:|
| Native x86-64 | Hardware execution | N/A | N/A | N/A | No learned artifact |
| Supplied PAN control | Supplied semantics | 0 | 0 | N/A | 0 learned bytes |
| NN | Selector | 56,929 | — | 227,716 | 1,807,203 |
| Original PAN | Selector | 225,329 | — | 917,700 | 7,274,893 |
| FieldLM | Structural selector | 0 | 760 | 0 | 42,016 |
| SPF | Structural selector | 0 | 760 | 0 | 42,156 |
| Mamba | Selector | 78,113 | — | 312,452 | 2,505,421 |
| Hydra | Selector | 78,713 | — | 314,852 | 2,526,571 |
| Newer NN | Direct effects | 322,283 | — | 1,289,132 | 1,314,005 |
| Newer Mamba | Direct effects | 291,851 | — | 1,167,404 | 1,191,012 |
| Newer Hydra | Direct effects | 292,151 | — | 1,168,604 | 1,191,859 |

Zero neural parameters or tensor bytes does **not** mean zero learned state:
FieldLM/SPF retain 760 records; SPF additionally packs its routes into 39,520
plane bytes. The selector artifacts also retain earlier staged heads/tables,
so their full parameter/record counts are broader than the runtime slice touched
by Hello. These are storage measurements, not compression ratios against a CPU
or a claim that the model replaces the entire ISA.

## Compute, memory and startup

Successful Hello measurements make the timing gap concrete. The ratio is against
the native process wall median; it compares the stated end-to-end scopes, not
hardware instruction latency.

| Successful path | Warm wall ms | Warm CPU ms | Wall / native | Warm sampled process peak MiB | Instrumented first response s |
|---|---:|---:|---:|---:|---:|
| Native C | 0.235 | 0.171 | 1.0× | 0.254³ | — |
| Supplied PAN control | 2.604 | 2.624 | 11.1× | 613.3 | 1.450 |
| FieldLM selector | 2.984 | 3.054 | 12.7× | 602.7 | 1.017 |
| SPF selector | 3.945 | 4.097 | 16.8× | 517.9 | 0.663 |
| Newer NN direct effects | 8.215 | 8.386 | 34.9× | 527.7 | 0.584 |
| Newer Mamba direct effects | 14.478 | 14.767 | 61.6× | 533.3 | 0.597 |
| Newer Hydra direct effects | 19.553 | 19.958 | 83.2× | 532.8 | 0.601 |

³ Native memory is the kernel's `wait4.ru_maxrss` child high-water report, not
sampled RSS; 0.254 MiB is the observed value, not hardware memory use. Model RSS
includes the interpreter, Torch and shared runtime, sampled every 2 ms. It is not
the size of the learned weights. Peak values above are maxima of warm samples.

Native wall time covers fork/exec through process termination, excluding parent
pipe capture/file writes. Model warm time covers fresh ELF/runtime setup,
execution and stop diagnostics with the model already loaded; adapter checks
and the memory sampler are included. First response includes imports, artifact
parsing/loading, integrity snapshots, garbage collection and the first request,
measured from instrumented script entry after standard-library imports.

Native process startup dominates these tiny runs; the nearly identical native
times do not show workload scaling. Three warm model samples give a useful
small-run observation, not a stable performance ranking. There is no successful
learned timing curve beyond Hello. CPU time and RSS were measured; energy,
hardware area and FLOPs were not.

## What the failures tell us

The supplied control rejects `ADD RAX,RDX` (`48 01 d0`) at the checksum's third
instruction. It rejects `PUSH RAX` (`50`) at the entry of the sort and record
apps. This is a limit of those encodings in the frozen consumer, not proof that
every ADD or PUSH is unsupported. The FieldLM/SPF tables lack corresponding
routes, while some neural selectors stop even earlier. A broader shared runtime
is needed before these apps can compare learned selection fairly.

The newer R3 models predict architectural effects directly. All three execute
the eight-instruction Hello ELF using their own predicted registers, exact
stdout and exit code in every trial. This extends the earlier hand-assembled
program evidence to a real C-compiled binary. Intermediate hardware-state parity
was not collected, so matching output does not certify every hidden state.

Their larger-app failures differ: emitted stores target unmapped addresses, or
predicted lengths/state lead to an unsupported syscall request on misaligned
bytes. The latter is a predicted-execution failure, not evidence that the app
requires an unavailable Linux service. These specimens have eight registers,
four flags, no general memory-load input and no arbitrary branch-target head;
ordinary compiler-generated code goes beyond that profile.

For selectors, the decoder and arithmetic remain supplied. For direct effects,
ELF mapping and the historical Linux write/exit boundary remain supplied. On a
predicted syscall that boundary preserves pre-instruction arguments/flags and
advances RIP by two; predicted stores commit first. It reads output memory for
write. There is no reference after-state, candidate ALU or oracle repair. Thus
Hello is a bounded endpoint success, not full ISA emulation.

## Evidence and reproduction

The [full measurements](measurements.md) include load CPU/wall time, per-cell
memory, first-response timing, successful warm ranges and elapsed-to-failure
diagnostics. The [raw matrix](evidence/matrix.json) preserves all 160 model and
60 native samples. [Provenance](evidence/provenance.json) hashes the reading
bundle and identifies the sealed mrun payload, checkpoints and compiler.

The [C programs and independent references](sources/programs/README.md),
[frozen adapter](sources/newer_adapter.py), [launcher/worker](sources/run_matrix.py)
and [native timer](sources/native_measure.c) make the measurement rules explicit.
The four original ELFs, disassemblies and ptrace counts are under
`evidence/programs/`. Full model weights and the shared execution environment are
not bundled. Original artifact identities and complete shipped-file hashes are
retained in `evidence/source-manifest.json`.

Mechanics and instruments passed the exact-source, frozen-state, reference and
collection checks. The observation is five learned Hello successes with larger
apps exposing coverage/state limits; complete x86-64 emulation remains
unestablished. See the [architecture paper](../paper.md) and
[early PAN-ISA companion](../../pan-isa/paper.md) for the mathematical and
historical context.
