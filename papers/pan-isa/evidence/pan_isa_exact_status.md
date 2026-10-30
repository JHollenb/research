# PAN ISA Exact Status

Status date: 2026-06-17

This is the single current status document for the `pan-isa-exact` proof of concept in
`pan-x86-isa-experiment-automation`. It merges the generated stage rollup, the full-ISA
ledger report, the Stage 3 uninterrupted PAN/QEMU comparison, and the newer cumulative
Stage 5 model artifact.

## Executive Status

PAN ISA exactness is a working proof of concept, not a complete x86 implementation.

What is working:

- Stage 0 through Stage 4 each have passing validation evidence on their scoped subsets.
- Stage 3 validation was tightened so stream-level undefined flag consumption now fails.
- The old Stage 3 v21 artifact fails that new validation as intended.
- The fixed Stage 3 v22 artifact passes the new validation.
- PAN and QEMU ran the same uninterrupted 8192-instruction Stage 3 program and matched the
  expected final state exactly.
- A cumulative Stage 5 model composes the current Stage 0-4 state surfaces and passes its
  own component-touch and exactness gate.
- A live PAN user-mode runtime can load simple static x86-64 ELFs, expose state through a
  GDB remote stub, and accept debugger-driven register and memory edits.

What is not done:

- Full x86 ISA closure is not done.
- The Intel SDM and AMD APM PDFs are still missing from the source-freeze report.
- The XED JSON encode/decode helper from the full-ISA plan is not implemented yet.
- The shared multi-profile QEMU/Bochs oracle backend layer is not implemented yet.
- The profile-neutral full-ISA trainer and promotion-scale batch runner are not implemented
  yet.
- Only one `user64` XED row is marked `fully_validated_user64` in the current full-ISA
  report.
- Most XED rows are still out of scope or unimplemented for the current proof of concept.

## Source Documents

Use this document for status. It replaces the older generated markdown status docs.
Supporting machine-readable and reference sources are:

- `reports/generated/full_isa_user64_report.json`: machine-readable `user64` full-ISA ledger report.
- `reports/generated/gate_evidence.json`: current Stage 0-4 gate-evidence rollup.
- `reports/generated/freshness_report.json`: freshness check for Stage 0-4 generated artifacts.
- `knowledge/reference/docs/pan-isa-exact.md`: narrative reference for the Stage 3 validation
  fix and PAN/QEMU uninterrupted benchmark.
- `data/artifacts/2026-06-17/pan-x86-isa/full_stage_model/full_stage_summary.json`: current
  cumulative Stage 5 model summary.

## Current Stage Coverage

### Stage 0 ALU

Status: passed for scoped subset.

- Implemented forms: 25.
- Validation step exactness: 1.0.
- Long split step exactness: 1.0.
- Oracle evidence: QEMU checked 768 cases at exact 1.0.
- Covers low-byte ALU behavior and selected flags.
- Does not cover memory, branches, SIMD/x87, exceptions, prefixes, or mode variation.

### Stage 1 Memory

Status: passed for scoped subset.

- Implemented forms: 16.
- Validation step exactness: 1.0.
- Long split step exactness: 1.0.
- Register, memory-event, effective-address, and final exactness are all 1.0.
- Oracle evidence: QEMU checked 768 cases at exact 1.0.
- Covers flat mapped integer load/store/XCHG addressing.
- Does not cover vector/floating memory forms, exceptions, branches, SIMD/x87, prefixes, or
  mode variation.

### Stage 2 Control Flow

Status: passed for scoped subset.

- Implemented forms: 18.
- Validation step exactness: 1.0.
- Long split step exactness: 1.0.
- Branch target, call/ret, flag, and final exactness are all 1.0.
- Oracle evidence: QEMU and Bochs each checked 768 cases at exact 1.0.
- Covers a bounded flat stack image, RIP/RSP movement, branch behavior, and call/return.
- Does not cover full register families, CMOVcc/SETcc, segmentation, interrupts, privilege,
  or exception semantics.

### Stage 3 Complex Scalar

Status: current fixed artifact passes the new stream-safety validation.

Important note: the older generated Stage 0-4 rollup pointed at the historical v21 snapshot
artifact. After the validation fix, v21 is compatibility evidence only because it contains
stream-level undefined-flag reads. The current passing Stage 3 artifact is v22.

Historical v21 artifact:

- Artifact: `data/artifacts/2026-06-16/pan-x86-isa/stage3_complex_scalar/stage3-complex-scalar-base-alu-v21-neural`.
- Old per-step exactness: validation 1.0, long 1.0.
- New continuous flag-safety validation: fails.
- Failure reason: later instructions such as `RCL`/`RCR` can consume `CF` after a previous
  instruction left it undefined.

Current v22 artifact:

- Artifact: `data/artifacts/2026-06-16/pan-x86-isa/stage3_complex_scalar/stage3-complex-scalar-continuous-flag-safe-v22-neural`.
- Schema valid: true.
- Stage 3 gate passed: true.
- Validation step exactness: 1.0.
- Long split step exactness: 1.0.
- Validation continuous undefined flag reads: 0.
- Long continuous undefined flag reads: 0.
- Negative controls degrade: scrambled opcode exactness 0.0; flipped carry input degrades.

Scope:

- Covers 125 current complex-scalar forms in the base-ALU subset.
- Tracks `RAX`, `RBX`, `RCX`, `RDX`.
- Tracks `CF`, `ZF`, `SF`, `OF` plus flag definedness.
- Tracks a flat 256-byte memory image for selected memory-source and memory-destination
  forms.
- Covers selected bit scan, bit test, rotate, shift, multiply/divide, POPCNT/LZCNT/TZCNT,
  BMI1, and BMI2 forms.
- Does not cover the full GPR file, full flag set, full addressing modes, paging,
  segmentation, privilege, interrupts, all exceptions, or vector state.

### Stage 4 SIMD/XMM

Status: passed for scoped subset.

- Implemented forms in manifest: 268.
- Validation step exactness: 1.0.
- Long split step exactness: 1.0.
- XMM, memory, exception, and worst-family exactness are all 1.0.
- Oracle evidence includes Bochs aligned-exception priority checks and QEMU non-exception
  priority checks at exact 1.0 for their accepted scopes.
- Covers XMM0-XMM15 for selected SSE/SSE2 integer, transfer, scalar floating, packed
  floating, compare, memory, and aligned exception forms.
- Does not cover AVX/VEX/EVEX, YMM, ZMM, x87 stack, MMX, masks, MXCSR exception status
  behavior, subnormal/overflow/underflow/signaling-NaN behavior, or full FP payload policy.

### Stage 5 Cumulative Model

Status: passes the current cumulative proof-of-concept gate.

Artifact:

- `data/artifacts/2026-06-17/pan-x86-isa/full_stage_model/full_stage_summary.json`.

Validation:

- `full_stage_model_gate_passed`: true.
- `all_stage_slices_present`: true.
- `all_required_components_touched`: true.
- `full_x86_goal_complete`: false.
- Overall step exactness: 1.0.
- Stage exactness: Stage 0 1.0, Stage 1 1.0, Stage 2 1.0, Stage 3 1.0, Stage 4 1.0.
- Stage 3 continuous undefined flag reads: 0.

Components touched in the cumulative trace:

- GPR state.
- RFLAGS and flag definedness.
- RIP.
- RSP.
- Branch behavior.
- Call/return behavior.
- Data memory.
- Stack memory.
- Stage 3 scalar memory.
- Stage 4 SIMD memory.
- XMM state.

Negative controls degrade:

- Wrong stack action exactness: 0.388889.
- Wrong Stage 3 opcode exactness: 0.666667.
- Wrong XMM source exactness: 0.833333.

Limitations:

- Stage 5 is a composition of the current Stage 0-4 semantic cartridges.
- It is not full x86.
- It is not yet wired into the generated Stage 0-4 status rollup.
- The live GDB runtime exists as a separate proof-of-concept path; Stage 5 itself remains a
  cumulative trace/model gate rather than a full process target.

## PAN/QEMU Uninterrupted Program Comparison

Status: completed for the Stage 3 proof of concept.

Artifacts:

- Program: `data/artifacts/2026-06-16/pan-x86-isa/pan_vs_qemu_stage3_uninterrupted_flag_fixed/stage3_uninterrupted_program.json`.
- PAN report: `data/artifacts/2026-06-16/pan-x86-isa/pan_vs_qemu_stage3_uninterrupted_flag_fixed/pan/pan_uninterrupted_report.json`.
- QEMU report: `data/artifacts/2026-06-16/pan-x86-isa/pan_vs_qemu_stage3_uninterrupted_flag_fixed/qemu/qemu_uninterrupted_report.json`.

Measured result:

- Same uninterrupted 8192-instruction program for both engines.
- PAN exact steps: 8192/8192.
- PAN final state: exact.
- PAN measured engine time: 0.599302 seconds.
- PAN speed: 13,669.23 steps/second.
- QEMU exact steps: 8192/8192.
- QEMU final state: exact.
- QEMU measured engine time: 0.165826 seconds.
- QEMU speed: 49,401.23 steps/second.
- QEMU was about 3.61x faster on measured engine time.
- PAN used substantially more RAM in the wrapper benchmark.

Interpretation:

- The current PAN implementation is exact for this program and scope.
- It is slower than QEMU because this version is Python/orchestration-heavy, uses structured
  semantic cartridges, and is optimized for inspectable validation rather than execution speed.
- This is V1 proof-of-concept evidence, not a claim that PAN is faster than QEMU.

## Live PAN Runtime And GDB Findings

Status: working proof-of-concept for simple static x86-64 ELF programs.

Implementation surface:

- `pan_x86_isa/memory.py`: sparse mapped virtual memory with permissions, dirty
  page digests, and memory fault classification.
- `pan_x86_isa/process.py`: ELF64 loader and Linux-style initial stack setup for
  `argc`, `argv`, `envp`, and `auxv`.
- `pan_x86_isa/runtime.py`: fail-closed user-mode execution loop for the first
  implemented instruction subset, Linux syscall subset, and typed architectural state.
- `pan_x86_isa/gdbstub.py`: GDB remote protocol for register reads/writes, memory
  reads/writes, breakpoints, stepping, continuations, and scoped PAN monitor commands.
- `python3 -m pan_x86_automation run-program`: public command for running an ELF under PAN or
  serving a one-session GDB remote target.

Observed program behavior:

- A generated static ELF at `/private/tmp/pan_math_funcs` ran two math functions,
  `add7` and `sub5`, and exited with code `42`.
- Direct `qemu-x86_64` comparison is currently blocked because `qemu-x86_64` is not
  installed; `qemu-system-x86_64` is installed but does not directly execute a Linux user
  ELF without a guest harness.
- GDB attached to PAN, disassembled the program, set breakpoints, single-stepped, read
  registers, and inspected stack memory.

Debugger mutation findings:

- At `add7`, changing `$rdi` from `40` to `100` through GDB changed the final program exit
  from `42` to `102`, proving that PAN consumed the debugger-mutated register state.
- Editing the saved return address on the stack from `0x40000a` to `0x400013` changed
  control flow and made the program exit with `40`, proving that PAN consumed debugger-
  mutated stack memory during `ret`.
- GDB memory inspection showed the expected frame layout: local data below `RBP`, saved
  old `RBP` at `[RBP]`, and saved return address at `[RBP+8]`.

Overflow findings:

- A controlled overflow ELF at `/private/tmp/pan_overflow_hijack` wrote past a stack local
  and overwrote `[RBP+8]` with `0x400011`, a mapped `win` block. PAN followed the corrupted
  saved return address and exited with code `77`.
- A bad-return overflow ELF at `/private/tmp/pan_overflow_badret` overwrote `[RBP+8]` with
  `0x41414141`. PAN set `RIP` to `0x41414141` and produced a SIGSEGV-style stop:
  `kind=fault`, `signal=11`, `detail=unmapped`.
- The GDB stub now returns a remote error packet for unmapped debugger memory reads/writes,
  so a faulted target remains debuggable instead of crashing the remote server.

PAN-only capability demonstrated:

- After the bad-return overflow stopped at unmapped `RIP=0x41414141`, GDB initially could
  not read memory at that address.
- The PAN monitor command `monitor pan-map 0x41414000 0x2000 rwx` materialized an executable
  page in the PAN model.
- The PAN monitor command `monitor pan-write 0x41414141 bf7b000000b83c0000000f05` injected
  `mov edi,123; mov eax,60; syscall` at the formerly unmapped crash address.
- Continuing with `signal 0` executed the injected code and exited with code `123`.
- This is intentionally PAN-only model surgery: a normal user process cannot make an
  already faulting unmapped instruction address become executable from outside the process
  without OS/debugger-mediated mapping semantics.

Current GDB limitations:

- This is a single-thread static-ELF subset, not full Linux or `gdbserver` parity.
- Dynamic linking is not handled: ET_DYN/PIE and PT_INTERP ELFs are rejected explicitly by
  the loader.
- Threading is not complete: thread-related syscalls such as `clone`, `clone3`, and `futex`
  stop with `unsupported_runtime_feature`.
- Signals are not complete: signal-related syscalls such as `rt_sigaction` and
  `rt_sigreturn` stop with `unsupported_runtime_feature`.
- Only the proof subset of Linux syscalls is implemented: `read`, `write`, `mmap`,
  `mprotect`, `munmap`, `brk`, `getpid`, `arch_prctl`, `exit`, and `exit_group`.
- All other Linux syscall numbers now fail closed with `unsupported_runtime_feature` and
  `RAX=-ENOSYS`; known families such as filesystem, descriptor, process, threading,
  signal, identity, resource-limit, and randomness syscalls get named diagnostics.
- The current local GDB rejects the custom target XML and falls back to its default x86-64
  register layout; core register, segment, memory, breakpoint, step, and continue behavior
  works, but full XML/FPU/vector register presentation still needs completion.
- The runtime intentionally fails closed on unsupported instructions and unimplemented
  system behavior.

## Full-ISA Ledger Status

Current `user64` full-ISA report:

- Report: `reports/generated/full_isa_user64_report.json`.
- `ok`: false.
- Gate failure: `source_hashes`.
- XED rows: 8,863.
- Classified rows: 8,863.
- Unclassified rows: 0.
- Executable `user64` rows: 1,088.
- Classified out-of-scope rows: 7,775.
- Operand-subset learned/validated rows: 370.
- Fully validated `user64` rows: 1.
- Unimplemented executable `user64` rows: 718.

Current full-ISA source freeze:

- XED is frozen by hash.
- Intel SDM PDF: missing.
- AMD APM PDF: missing.
- Source freeze `ok`: false.

Current `user64` status counts:

- `fully_validated_user64`: 1.
- `operand_subset_learned_validated`: 370.
- `unimplemented`: 718.
- `classified_out_of_scope`: 7,775.

Largest remaining executable `user64` gaps:

- SSE: 159.
- BINARY: 127.
- LOGICAL: 86.
- DATAXFER: 58.
- COND_BR: 43.
- SHIFT: 36.
- BMI1: 34.
- CMOV: 32.
- SETCC: 32.
- ROTATE: 22.
- BMI2: 20.
- PUSH: 16.
- POP: 13.
- BITBYTE: 10.
- MISC: 9.
- RET: 6.
- UNCOND_BR: 6.
- CALL: 5.
- LZCNT: 4.

Largest global unimplemented XED categories:

- AVX512: 1,573.
- CONVERT: 758.
- DATAXFER: 576.
- VFMA: 528.
- APX: 505.
- AVX: 471.
- BINARY: 333.
- LOGICAL: 331.
- FP16: 296.
- AVX2: 257.

## Components Present Today

The current proof-of-concept has these components represented somewhere in Stage 0-5:

- Registers: partial GPR state in Stage 0-3; XMM0-XMM15 in Stage 4; cumulative state in
  Stage 5.
- Flags: `CF`, `ZF`, `SF`, `OF` plus Stage 3 definedness tracking.
- RIP: Stage 2 and Stage 5.
- RSP: Stage 2 and Stage 5.
- Stack memory: Stage 2 and Stage 5.
- Data memory: Stage 1, Stage 3, Stage 4, and Stage 5.
- Branches: Stage 2 and Stage 5.
- Calls and returns: Stage 2 and Stage 5.
- SIMD/XMM: Stage 4 and Stage 5.
- Exceptions: selected Stage 3 and Stage 4 exception/advisory behavior.
- Oracles: QEMU and Bochs evidence exists for current stage scopes.

Missing or incomplete components:

- Full GPR file across all stages.
- Full RFLAGS and all undefined/advisory flag policies.
- Segments, descriptors, paging, control registers, MSRs, and privilege transitions.
- Real-mode, protected-mode, compatibility-mode, and ring0/ring3 profile matrix.
- Interrupts and full exception priority semantics.
- x87, MMX, YMM, ZMM, AVX, AVX2, AVX512, APX, VEX, EVEX, masks, and vendor overlays.
- Full operand-policy generation across all XED rows.
- Full trace splits across smoke, train, validation, long, exception, and negative controls
  for every row/profile tuple.
- Promotion-scale batch execution and resumable failure handling.

## Validation Commands

Current smoke checks:

```bash
rtk python3 tests/test_pan_x86_auto.py
rtk python3 -m py_compile pan_x86_stages.stage5_full_model_pan
rtk python3 -m pan_x86_stages.stage5_full_model_pan validate --trace /Users/jakeholl/domains/data/artifacts/2026-06-17/pan-x86-isa/full_stage_model/full_stage_trace.json
```

Regenerate the Stage 5 smoke artifact:

```bash
rtk python3 -m pan_x86_stages.stage5_full_model_pan run-smoke --out-dir /Users/jakeholl/domains/data/artifacts/2026-06-17/pan-x86-isa/full_stage_model
```

Inspect the current full-ISA report:

```bash
rtk python3 -m json.tool reports/generated/full_isa_user64_report.json
```

Run the live GDB proof-of-concept:

```bash
rtk python3 -m pan_x86_automation run-program --program /private/tmp/pan_math_funcs --gdb :12345
gdb /private/tmp/pan_math_funcs
```

## Next Work

The highest-value next work is:

1. Wire Stage 5 into generated status reporting so this document is no longer manually
   reconciling Stage 0-4 reports with Stage 5 artifacts.
2. Commit or intentionally discard the current untracked Stage 5 implementation, depending
   on whether it should become part of the proof-of-concept baseline.
3. Update the Stage 3 artifact snapshot/report path to the v22 continuous-flag-safe artifact.
4. Add the XED JSON helper and connect it to trace generation.
5. Promote the current stage-specific QEMU/Bochs code into shared oracle backends.
6. Expand operand policies and trace generation from scoped stage subsets toward the XED
   row/profile promotion key.
7. Add the profile-neutral trainer and batch runner from the full-ISA plan.
8. Freeze externally supplied Intel SDM and AMD APM PDFs or explicitly keep the PDF issue as
   an excluded blocker in final reports.

## Bottom Line

The proof of concept can execute and validate scoped x86 behavior with inspectable state. It
has registers, flags, memory, stack, control flow, XMM state, selected exceptions, and QEMU/
Bochs evidence across current stage scopes.

It does not yet implement full x86. The remaining work is mainly coverage scale, source
freeze closure, XED-backed encoding, shared oracle infrastructure, profile coverage, and
promotion automation.
