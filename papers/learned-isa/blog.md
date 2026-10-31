---
title: "2026-10-30 17:28:44 Running compiled C on our learned ISA models"
subtitle: "Five models run Hello World and three larger apps reveal where instruction coverage and predicted execution break down"
author: "Jake Holl with Codex"
type: blog
category: research
subtype: compiled-c-isa-execution
date: 2026-10-30
created: "2026-10-30T17:28:44-07:00"
timestamp: "2026-10-30T17:28:44-07:00"
status: measured-exploration
claim_status: "Exact stdout and exit evaluated on four fixed freestanding C apps using one frozen seed-673 specimen per learned path. Five learned paths succeed on Hello only. Selector semantics and the Linux boundary are supplied. Intermediate hardware-state parity and full ISA emulation are not established."
tags: [blog, research, isa, x86, compiled-c, pan-isa, fieldlm, spf, neural-networks, mamba, hydra, direct-effect, emulation, performance, debugging]
source_docs:
  - c-app-matrix/README.md
  - c-app-matrix/measurements.md
  - paper.md
source_code:
  - c-app-matrix/sources/run_matrix.py
  - c-app-matrix/sources/newer_adapter.py
  - c-app-matrix/sources/programs/
artifacts:
  - c-app-matrix/evidence/matrix.json
  - c-app-matrix/evidence/programs/
  - c-app-matrix/evidence/provenance.json
jobs: [job-007fe5d65603]
---

# 2026-10-30 17:28:44 Running compiled C on our learned ISA models

We compiled four small C applications and handed the same executable bytes to our frozen ISA models. Five learned models ran Hello World correctly. Every tested model stopped before completing the checksum, sort or record parser.

The stops were informative. One runtime rejected the checksum's third instruction. Two models tried to make system calls after execution drifted into the middle of an instruction. Others predicted writes to addresses that did not exist. These failures identify different pieces of work: extending a supplied instruction consumer, improving learned selection, and giving a model the information and control outputs needed to execute ordinary code.

An instruction set architecture (ISA) defines how machine instructions change registers, memory and control flow. This experiment compares six older operation selectors with three models that predict those architectural effects. R3 identifies the retained round-three checkpoint cohort used here. We use one frozen specimen per path, all from seed 673. Other systems in the wider ISA project are outside this run. The [complete matrix](c-app-matrix/README.md) retains the sizes, timings and failure details.

## Four C apps and identical executable bytes

The first application prints `Hello, world!`. The second performs 24 arithmetic updates on four volatile 64-bit values and writes a checksum. The third sorts 32 integers and writes an order-sensitive digest. The fourth parses 80 built-in CSV records and aggregates their quantities and revenues into eight buckets.

“Large” means the largest app in this deliberately small suite. It reads 1,053 bytes of text. None of the programs needs a dynamic loader, libc, threads or external files. Inline assembly supplies only the Linux write and exit calls; the application calculations are C.

GCC 13.3 compiled each application once with the same size-optimization flags. Every execution path received that exact ELF file, the executable format used here on Linux. Independent Python calculations supplied the expected output, and native execution checked it before the model trials.

| App | Work | ELF file bytes | .text code bytes | Native instructions executed |
|---|---|---:|---:|---:|
| Tiny | Hello World | 8,968 | 29 | 8 |
| Small | Arithmetic checksum | 9,056 | 619 | 108 |
| Medium | Sort 32 integers | 9,080 | 184 | 3,115 |
| Large | Parse and aggregate 80 records | 10,216 | 269 | 12,313 |

Code size and execution length are already different quantities. The checksum has a long straight-line body. The sort and parser reuse shorter bodies through loops, so they execute many more instructions from less machine code.

Hello reuses our earlier known source, so we treat it as a regression case. We kept the compiler flags and programs fixed across models.

## What completed

We included native execution and a supplied PAN runtime control alongside the nine learned paths. The control executes without a learned selector, which lets us distinguish a runtime coverage problem from a learned selection problem.

Each model/app cell ran a first request and three warm repeats. A success required the exact output bytes and a normal exit with the expected code. Each request started with fresh architectural state. Native execution used 15 trials per app.

| Execution path | Hello World | Checksum | Sort | Record parser |
|---|---|---|---|---|
| Native x86-64 | Pass | Pass | Pass | Pass |
| Supplied PAN runtime control | Pass | Coverage stop | Coverage stop | Coverage stop |
| NN selector | Selection stop | Selection stop | Selection stop | Selection stop |
| Original PAN selector | Selection stop | Coverage stop | Coverage stop | Selection stop |
| FieldLM selector | Pass | Missing route | Missing route | Missing route |
| SPF selector | Pass | Missing route | Missing route | Missing route |
| Mamba selector | Selection stop | Selection stop | Selection stop | Coverage stop |
| Hydra selector | Selection stop | Coverage stop | Coverage stop | Coverage stop |
| R3 NN direct effects | Pass | Store fault | Store fault | Store fault |
| R3 Mamba direct effects | Pass | Predicted syscall failure | Store fault | Store fault |
| R3 Hydra direct effects | Pass | Predicted syscall failure | Store fault | Store fault |

Every displayed model pass succeeded in all four trials. All native trials passed. The full CPU run finished in 60.3 seconds, collecting 160 model/control trials and 60 native trials. No cell hit its ten-second deadline or instruction limit.

## The selectors reached the edge of their supplied instruction vocabulary

A selector chooses an operation, then supplied runtime code computes its effect. The learned component can recognize the instruction correctly and still be unable to execute it if the consumer has no implementation for that encoding.

The checksum makes this concrete. Its first three native instructions load two values from memory and add them:

```asm
mov rdx, [rip + displacement]
mov rax, [rip + displacement]
add rax, rdx                 ; encoding: 48 01 d0
```

The supplied runtime executes the two loads, then rejects that register-to-register ADD. The sort and parser encounter a different boundary immediately: their entry instruction is `PUSH RAX`, encoded as `50`, which this frozen consumer rejects.

These are specific encoding gaps. The runtime supports some ADD and stack operations, but that does not imply support for every width, register combination or encoding. FieldLM and SPF lack corresponding routes and surface a missing-route exception at the same locations.

The control matters here. It fails without any neural prediction involved. These cells therefore cannot tell us how well a learned selector would execute the whole algorithm through a broader consumer. Most of the sort and parser never runs.

The neural selectors introduce another failure mode. A selector may choose the wrong operation or decline because its confidence is too low. On Hello, for example, the NN selected a SIMD move where the adapter expected an immediate register move. Mamba selected a jump, and Hydra selected XOR, at locations requiring immediate moves. The typed adapter stopped those mismatches before committing their proposed effects.

## The direct-effect models need a richer execution interface

The R3 models take a more ambitious route. They receive up to 15 instruction bytes, eight register values and four flag bits, then predict the next registers, flags, instruction length, a possible store and a syscall indicator. Supplied code maps the ELF and handles the declared Linux boundary, but there is no supplied arithmetic routine correcting their predictions.

This interface has two limits that ordinary compiled C exposes quickly.

**General loads need memory contents.** Consider the same load instruction with the same registers and flags, but with a different value stored at its target address. The correct result changes. These models receive no general memory-read value, so both situations look identical to the model. Increasing the number of parameters cannot recover an input that the interface never supplies.

The checksum starts with memory loads, and the larger apps depend heavily on memory and stack values. The observed direct-effect failures include predicted writes to unmapped addresses. For example, the NN checksum attempt stopped on a write to `0x3bfffcbd0`. That is the recorded fault; an earlier incorrect load, register value or instruction length may have led to it. We did not trace the first incorrect intermediate state in this run.

**Branches need control over the next instruction address.** The ordinary direct-effect path advances the instruction pointer by the predicted length:

$$
\mathrm{RIP}_{t+1}=\mathrm{RIP}_t+\widehat{\ell}_t,\qquad 1\leq\widehat{\ell}_t\leq15.
$$

There is no arbitrary branch-target output. A loop that jumps backward therefore needs an additional mechanism. Calls and returns also need control flow and memory interactions beyond this interface.

The small Mamba and Hydra attempts show how errors can propagate even before a complete loop is involved. Both eventually fetched bytes at `0x40103b`, inside the displacement of a native instruction. They then predicted a syscall request that the boundary could not serve. The C app uses only write and exit; it did not suddenly require another operating-system service. The predicted execution had drifted.

Attempting 23 or 58 model steps does not mean that many instructions were correct. Once a register, length or store is wrong, later inputs can describe an execution that the native program never takes.

## Why Hello succeeds and what it costs

Hello's eight native instructions mostly move constants into registers, clear a register, and invoke write and exit. It does not require general variable loads, a sorting loop or a call stack. Its message bytes are read by the supplied operating-system boundary when the model requests a write.

All three direct-effect models completed those eight predicted steps with the exact 14 output bytes and exit code zero. This is useful execution evidence for a real C-compiled binary. It establishes the program's observed result, while leaving intermediate hardware-state parity for a separate measurement.

The size and timing differences are substantial even on this tiny case. Warm times below are medians of the three repeats after the first request:

| Successful learned path | Neural parameters | Other learned state | Serialized artifact bytes | Warm Hello wall ms |
|---|---:|---|---:|---:|
| FieldLM selector | 0 | 760 route records | 42,016 | 2.984 |
| SPF selector | 0 | 760 records; 39,520 packed plane bytes | 42,156 | 3.945 |
| R3 NN direct effects | 322,283 | — | 1,314,005 | 8.215 |
| R3 Mamba direct effects | 291,851 | — | 1,191,012 | 14.478 |
| R3 Hydra direct effects | 292,151 | — | 1,191,859 | 19.553 |

The 39,520 packed plane bytes describe SPF's serving representation of the routes; they should not be added to the JSON file size as a second serialized artifact. The selector JSON files and direct-effect Torch checkpoints also have different format overhead. Shared runtime code and dependencies are additional, so these are learned-artifact sizes rather than complete deployment sizes.

Native Hello took a median 0.235 ms, while the supplied runtime control took 2.604 ms. Native timing includes process creation and termination. Warm model timing includes fresh ELF/runtime setup, execution, adapter work and memory sampling, with the model already loaded. These are end-to-end path measurements with different startup costs.

The successful model processes used roughly 518–603 MiB of sampled resident memory, including Python, Torch and the shared runtime. Hello's compiled machine code was 29 bytes. Those quantities answer different questions: program representation, learned storage and total process cost. The [detailed measurements](c-app-matrix/measurements.md) keep them separate and include CPU time, loading and first-response latency. Failed attempts contribute elapsed-to-failure diagnostics, never successful execution speedups.

## The next experiment should target the first missing capability

For the selector track, the immediate work is to extend the common decoder, schema and consumer for the encodings ordinary C emits, starting with the observed ADD and PUSH gaps. Every selector should then face the same expanded contract. That would let us distinguish correct selection from consumer coverage on a larger part of each program.

For the direct-effect track, the interface needs a declared memory-read mechanism and a way to predict the next instruction address to support general loads, loops, calls and returns. The current faults also call for native-state traces that identify the first wrong prediction and explain how it leads to the final bad store or syscall.

We should retain these original binaries and results while testing those extensions. Hello gives us a working regression case. The other three apps give us concrete memory, instruction and control-flow demands, with independently checked native outputs. Progress becomes visible when an executor handles the next required operation correctly and the unchanged program continues further.

The experiment, source and evidence are linked in the [benchmark matrix](c-app-matrix/README.md), [raw trials](c-app-matrix/evidence/matrix.json), [C workloads and references](c-app-matrix/sources/programs/README.md), [execution harness](c-app-matrix/sources/run_matrix.py) and [direct-effect adapter](c-app-matrix/sources/newer_adapter.py). The [architecture paper](paper.md) and [early PAN-ISA account](../pan-isa/paper.md) explain the surrounding designs and their mathematical contracts.

The newer structural FieldLM/SPF microcode executor is separate from the tested selector rows. Its original serving archive was unavailable during a bounded retrieval attempt; the benchmark retains that [retrieval record](c-app-matrix/evidence/structural-artifact-retrieval/retrieval-provenance.json) as an unmeasured path.
