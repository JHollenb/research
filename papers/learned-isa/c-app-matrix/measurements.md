# Compiled C application matrix

Host: AMD Ryzen 9 7950X 16-Core Processor; pop-os; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0. CPU threads per model: 1.

[Immutable collected matrix](evidence/matrix.json) · [Machine-readable summary](summary.json). Raw SHA-256: `72e46d91a2423b87454eff7d548633800669c7fee72491f47511dd4277a5997a`.

The same compiled ELF is used for native execution and every architecture. Exact stdout and exit are rechecked from recorded samples. This is a bounded application-output result, not an intermediate-state proof. Selectors use supplied typed semantics; direct-effect paths predict effects and share the declared ELF/syscall boundary.

## Outcomes

| Path | tiny | small | medium | large |
| --- | --- | --- | --- | --- |
| native | success (15/15) | success (15/15) | success (15/15) | success (15/15) |
| pan_reference | success (4/4) | refused (4/4) | refused (4/4) | refused (4/4) |
| nn | refused (4/4) | refused (4/4) | refused (4/4) | refused (4/4) |
| pan_isa | refused (4/4) | refused (4/4) | refused (4/4) | refused (4/4) |
| fieldlm | success (4/4) | missing route [raw execution_error] (4/4) | missing route [raw execution_error] (4/4) | missing route [raw execution_error] (4/4) |
| spf_transformer | success (4/4) | missing route [raw execution_error] (4/4) | missing route [raw execution_error] (4/4) | missing route [raw execution_error] (4/4) |
| mamba | refused (4/4) | refused (4/4) | refused (4/4) | refused (4/4) |
| hydra | refused (4/4) | refused (4/4) | refused (4/4) | refused (4/4) |
| effect_nn | success (4/4) | execution_error (4/4) | execution_error (4/4) | execution_error (4/4) |
| effect_mamba | success (4/4) | predicted syscall failure [raw refused] (4/4) | execution_error (4/4) | execution_error (4/4) |
| effect_hydra | success (4/4) | predicted syscall failure [raw refused] (4/4) | execution_error (4/4) | execution_error (4/4) |

Model counts include the first request plus warm repeats. Missing, partial, timed-out, and instrument-error cells stay visible.

## Successful warm wall time

Milliseconds. Model medians require every requested warm repeat to succeed; first requests are excluded. Native uses all native repeats. A dash is no qualifying execution timing, never zero or a speedup. Native includes fork/exec-to-wait4 overhead; model requests include process-image initialization and sampled execution overhead. These are harness-path measurements, not matched instruction-only kernels.

| Path | tiny | small | medium | large |
| --- | --- | --- | --- | --- |
| native | 0.235 | 0.234 | 0.230 | 0.232 |
| pan_reference | 2.604 | — | — | — |
| nn | — | — | — | — |
| pan_isa | — | — | — | — |
| fieldlm | 2.984 | — | — | — |
| spf_transformer | 3.945 | — | — | — |
| mamba | — | — | — | — |
| hydra | — | — | — | — |
| effect_nn | 8.215 | — | — | — |
| effect_mamba | 14.478 | — | — | — |
| effect_hydra | 19.553 | — | — | — |

## Native reference measurements

| App | Exact / recorded / expected | Wall median ms | CPU median ms | Child max RSS median MiB |
| --- | --- | --- | --- | --- |
| tiny | 15/15/15 | 0.235 | 0.171 | 0.254 |
| small | 15/15/15 | 0.234 | 0.165 | 0.254 |
| medium | 15/15/15 | 0.230 | 0.167 | 0.254 |
| large | 15/15/15 | 0.232 | 0.167 | 0.254 |

These short native processes include startup and termination. Similar medians across apps should not be read as an application-scaling curve.

## Application size and instruction demand

| App | C bytes | ELF bytes | .text bytes | Static instructions | Dynamic steps | Executed RIPs | Dynamic mnemonic kinds | Trace |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| tiny | 521 | 8968 | 29 | 8 | 8 | 8 | 3 | exit; complete |
| small | 684 | 9056 | 619 | 108 | 108 | 108 | 9 | exit; complete |
| medium | 1043 | 9080 | 184 | 52 | 3115 | 52 | 18 | exit; complete |
| large | 3200 | 10216 | 269 | 72 | 12313 | 72 | 25 | exit; complete |

C bytes count the app source, excluding the shared header. ELF bytes include sections and file overhead. Dynamic steps come from a separate ptrace single-step run; incomplete traces are partial observations. They are not model steps or performance timings.

- **tiny** dynamic mix: `mov` × 5, `syscall` × 2, `xor` × 1. Undecoded RIPs: 0.
- **small** dynamic mix: `mov` × 75, `xor` × 11, `add` × 8, `imul` × 4, `lea` × 3, `sub` × 3, `syscall` × 2, `cmp` × 1, `setne` × 1. Undecoded RIPs: 0.
- **medium** dynamic mix: `mov` × 1107, `cmp` × 379, `jne` × 349, `dec` × 283, `jae` × 283, `sub` × 255, `test` × 254, `add` × 63, `inc` × 63, `xor` × 34, `imul` × 32, `lea` × 4, `jmp` × 2, `movabs` × 2, `syscall` × 2, `pop` × 1, `push` × 1, `setne` × 1. Undecoded RIPs: 0.
- **large** dynamic mix: `mov` × 4219, `cmp` × 1465, `lea` × 1384, `jmp` × 893, `je` × 571, `jle` × 563, `imul` × 507, `and` × 410, `inc` × 403, `jg` × 403, `movsbl` × 403, `xor` × 266, `incq` × 240, `add` × 168, `call` × 160, `ret` × 160, `test` × 81, `jne` × 8, `movabs` × 2, `syscall` × 2, `movq` × 1, `pop` × 1, `push` × 1, `setne` × 1, `sub` × 1. Undecoded RIPs: 0.

## Architecture payloads

Exact counts from the recorded frozen specimen metadata. Unreported fields stay unavailable. Zero neural parameters in a record-based selector does not mean zero learned state. JSON export bytes and PyTorch checkpoint bytes have different serialization scopes; neither is whole-process RSS or full deployment size.

| Architecture | Track | Parameters | Learned records | Tensor bytes | Packed-plane bytes | Artifact bytes | Format |
| --- | --- | --- | --- | --- | --- | --- | --- |
| pan_reference | supplied consumer control | 0 | — | — | — | 0 | none |
| nn | selector | 56929 | — | 227716 | — | 1807203 | JSON export |
| pan_isa | selector | 225329 | — | 917700 | — | 7274893 | JSON export |
| fieldlm | selector | 0 | 760 | 0 | — | 42016 | JSON export |
| spf_transformer | selector | 0 | 760 | 0 | 39520 | 42156 | JSON export |
| mamba | selector | 78113 | — | 312452 | — | 2505421 | JSON export |
| hydra | selector | 78713 | — | 314852 | — | 2526571 | JSON export |
| effect_nn | direct-effect | 322283 | — | 1289132 | — | 1314005 | PyTorch checkpoint (.pt) |
| effect_mamba | direct-effect | 291851 | — | 1167404 | — | 1191012 | PyTorch checkpoint (.pt) |
| effect_hydra | direct-effect | 292151 | — | 1168604 | — | 1191859 | PyTorch checkpoint (.pt) |

## Load instrumentation

Medians across fresh app cells, including loads before unsuccessful requests. Load scopes include lazy imports where applicable. Selector JSON parsing is outside its load region; direct-effect checkpoint deserialization is inside its load region. The artifact parse/setup field for control and direct-effect rows measures path setup without JSON loading.

| Architecture | Load samples | Load wall ms | Load CPU ms | Artifact parse/setup ms | Load sampled RSS MiB |
| --- | --- | --- | --- | --- | --- |
| pan_reference | 4 | 0.250 | 0.253 | 0.003 | 502.256 |
| nn | 4 | 437.996 | 440.159 | 9.268 | 602.434 |
| pan_isa | 4 | 498.680 | 500.787 | 37.735 | 620.322 |
| fieldlm | 4 | 407.707 | 409.647 | 0.158 | 591.791 |
| spf_transformer | 4 | 70.333 | 72.421 | 0.159 | 507.408 |
| mamba | 4 | 442.734 | 444.445 | 13.075 | 609.684 |
| hydra | 4 | 442.087 | 444.322 | 13.075 | 606.799 |
| effect_nn | 4 | 8.551 | 8.574 | 0.003 | 510.180 |
| effect_mamba | 4 | 8.732 | 8.745 | 0.003 | 513.143 |
| effect_hydra | 4 | 8.188 | 8.202 | 0.002 | 510.033 |

## Successful first responses and request resources

First response runs from the runner's ENTERED timestamp (after standard-library imports) to the first completed response, including Torch/runtime imports, artifact setup, load, snapshot/export, GC, and the first request. It excludes interpreter startup and earlier standard-library imports. First request CPU/wall cover the narrower runner region. RSS is sampled whole-process MiB; it includes Python/Torch. Warm columns require every requested warm repeat to succeed.

| Architecture | App | First response ms | First request wall ms | First request CPU ms | First sampled RSS MiB | Warm CPU median ms | Warm sampled RSS median MiB | Warm sampled RSS delta median MiB |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| pan_reference | tiny | 1449.570 | 871.821 | 880.531 | 613.262 | 2.624 | 613.262 | 0.004 |
| fieldlm | tiny | 1017.386 | 21.365 | 21.734 | 602.703 | 3.054 | 602.727 | 0.012 |
| spf_transformer | tiny | 662.575 | 21.414 | 21.688 | 517.863 | 4.097 | 517.879 | 0.008 |
| effect_nn | tiny | 583.724 | 10.244 | 10.464 | 527.699 | 8.386 | 527.711 | 0.008 |
| effect_mamba | tiny | 597.322 | 17.493 | 17.863 | 533.316 | 14.767 | 533.348 | 0.020 |
| effect_hydra | tiny | 601.238 | 22.188 | 22.606 | 532.805 | 19.958 | 532.820 | 0.008 |

## Failure and missing-data diagnostics

Times below measure unsuccessful responses or time to stop. They are not execution speed measurements or speedups. Failure medians include only failed recorded samples; child wall time includes the whole cell process and may reflect a timeout. Full per-repeat stop reasons, stdout, last instructions, and usage remain in summary.json and the immutable source.

| Architecture | App | Outcome | Failed first response ms | Failure request wall median ms | Failure CPU median ms | Failure sampled RSS median MiB | Whole cell wall ms | First diagnostic |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| pan_reference | small | refused (4/4) | 981.907 | 2.103 | 2.118 | 601.053 | 1444.309 | unsupported instruction |
| pan_reference | medium | refused (4/4) | 982.745 | 1.884 | 1.897 | 601.207 | 1432.498 | unsupported instruction |
| pan_reference | large | refused (4/4) | 993.062 | 1.967 | 1.982 | 601.436 | 1455.488 | unsupported instruction |
| nn | tiny | refused (4/4) | 1094.251 | 1.770 | 1.784 | 619.225 | 1748.889 | learned selector MOVDQU_M128_XMM; typed adapter MOV_IMM_REG |
| nn | small | refused (4/4) | 1141.706 | 1.424 | 1.437 | 619.785 | 1632.166 | selector confidence 0.341653 below common threshold |
| nn | medium | refused (4/4) | 1087.608 | 1.521 | 1.532 | 619.164 | 1578.846 | selector confidence 0.270849 below common threshold |
| nn | large | refused (4/4) | 1094.207 | 1.437 | 1.454 | 618.832 | 1585.996 | selector confidence 0.149251 below common threshold |
| pan_isa | tiny | refused (4/4) | 1231.593 | 1.347 | 1.361 | 634.609 | 1773.300 | selector confidence 0.400598 below common threshold |
| pan_isa | small | refused (4/4) | 1214.906 | 1.883 | 1.895 | 634.602 | 1881.255 | unsupported instruction |
| pan_isa | medium | refused (4/4) | 1224.207 | 1.508 | 1.485 | 634.922 | 1863.580 | unsupported instruction |
| pan_isa | large | refused (4/4) | 1263.777 | 1.376 | 1.391 | 634.969 | 1933.381 | selector confidence 0.398159 below common threshold |
| fieldlm | small | missing route [raw execution_error] (4/4) | 1028.555 | 1.694 | 1.709 | 601.773 | 1505.275 | field route missing: (5, 1, 0, 0, 0, 0, 0, 0, 0); Recorded execution_error is a missing learned route; not an instrument failure. |
| fieldlm | medium | missing route [raw execution_error] (4/4) | 1016.644 | 1.173 | 1.187 | 603.059 | 1527.004 | field route missing: (5, 80, 0, 0, 0, 0, 0, 0, 0); Recorded execution_error is a missing learned route; not an instrument failure. |
| fieldlm | large | missing route [raw execution_error] (4/4) | 1068.800 | 1.156 | 1.171 | 601.598 | 1684.714 | field route missing: (5, 80, 0, 0, 0, 0, 0, 0, 0); Recorded execution_error is a missing learned route; not an instrument failure. |
| spf_transformer | small | missing route [raw execution_error] (4/4) | 660.823 | 2.135 | 2.149 | 519.285 | 983.093 | missing phase route: (5, 1, 0, 0, 0, 0, 0, 0, 0); Recorded execution_error is a missing learned route; not an instrument failure. |
| spf_transformer | medium | missing route [raw execution_error] (4/4) | 657.830 | 1.317 | 1.331 | 519.336 | 972.088 | missing phase route: (5, 80, 0, 0, 0, 0, 0, 0, 0); Recorded execution_error is a missing learned route; not an instrument failure. |
| spf_transformer | large | missing route [raw execution_error] (4/4) | 665.044 | 1.354 | 1.368 | 519.203 | 1004.553 | missing phase route: (5, 80, 0, 0, 0, 0, 0, 0, 0); Recorded execution_error is a missing learned route; not an instrument failure. |
| mamba | tiny | refused (4/4) | 1096.184 | 1.868 | 1.881 | 629.996 | 1592.084 | learned selector JMP_REL8; typed adapter MOV_IMM_REG |
| mamba | small | refused (4/4) | 1102.838 | 1.892 | 1.906 | 629.918 | 1609.915 | learned selector LEA; typed adapter MOV_REG_RM |
| mamba | medium | refused (4/4) | 1091.987 | 1.885 | 1.893 | 629.332 | 1602.346 | selector confidence 0.468663 below common threshold |
| mamba | large | refused (4/4) | 1095.591 | 1.889 | 1.903 | 629.355 | 1636.699 | unsupported instruction |
| hydra | tiny | refused (4/4) | 1102.757 | 3.229 | 3.288 | 630.273 | 1613.521 | learned selector XOR_RM_REG; typed adapter MOV_IMM_REG |
| hydra | small | refused (4/4) | 1102.618 | 3.196 | 3.261 | 629.879 | 1779.515 | unsupported instruction |
| hydra | medium | refused (4/4) | 1096.408 | 1.995 | 2.008 | 629.732 | 1601.068 | unsupported instruction |
| hydra | large | refused (4/4) | 1105.361 | 1.961 | 1.975 | 630.117 | 1609.721 | unsupported instruction |
| effect_nn | small | execution_error (4/4) | 603.227 | 23.755 | 24.106 | 528.283 | 972.223 | write fault at 0x3bfffcbd0: unmapped |
| effect_nn | medium | execution_error (4/4) | 611.146 | 35.530 | 36.212 | 527.963 | 1051.904 | write fault at 0xc8: unmapped |
| effect_nn | large | execution_error (4/4) | 605.181 | 18.758 | 19.033 | 527.023 | 998.713 | write fault at 0x20000824: unmapped |
| effect_mamba | small | predicted syscall failure [raw refused] (4/4) | 621.766 | 39.612 | 40.406 | 533.658 | 1193.940 | {"kind": "unsupported_syscall", "rax": 362999}; The model-predicted syscall flag reached an unsupported call. The C fixtures use only write/exit; this does not establish that another Linux service is needed. |
| effect_mamba | medium | execution_error (4/4) | 634.868 | 59.037 | 60.231 | 532.113 | 1273.980 | write fault at 0x804: unmapped |
| effect_mamba | large | execution_error (4/4) | 679.394 | 97.646 | 99.497 | 533.449 | 1345.696 | write fault at 0x8000040: unmapped |
| effect_hydra | small | predicted syscall failure [raw refused] (4/4) | 637.502 | 55.890 | 56.962 | 533.484 | 1133.457 | {"kind": "unsupported_syscall", "rax": 158}; The model-predicted syscall flag reached an unsupported call. The C fixtures use only write/exit; this does not establish that another Linux service is needed. |
| effect_hydra | medium | execution_error (4/4) | 653.546 | 70.686 | 72.047 | 533.316 | 1168.424 | write fault at 0x8420448848982444: unmapped |
| effect_hydra | large | execution_error (4/4) | 633.822 | 53.027 | 54.085 | 533.561 | 1097.598 | write fault at 0x244c8968082c7c: unmapped |

## Measurement scopes

- **successful warm:** All requested warm repeats must be present, observable-exact, from a completed cell with unchanged artifact. No first request or failed sample enters the warm median.
- **native:** All requested native repeats must match exact stdout and exit. Fork/exec through wait4 wall time, excluding parent pipe capture/file writes.
- **requests:** Instrumented runner scope includes ELF/process initialization and execution, supplied ABI, and Usage sampler overhead; not pure model-forward time.
- **cold:** Runner ENTERED timestamp (after standard-library imports) to first completed response, including Torch/runtime imports, artifact parsing/load, snapshot/export/GC, and first request. Excludes interpreter startup and earlier standard-library imports. Never called time to first token.
- **load:** Median of per-cell instrumented load regions; selector JSON parse is separate, checkpoint deserialization is inside direct-effect load. Load regions may include lazy imports.
- **memory:** Usage field names ending _mb are MiB. Request RSS is sampled whole-process RSS, includes Python/Torch, and is not weight bytes or an exact allocation peak. Native RSS is wait4 child maximum and may be unavailable for very short programs.
- **dynamic count:** Separate ptrace single-step run; not timed as native performance. Counts can treat REP iterations as multiple traps. Incomplete traces are not full-program instruction counts.
- **artifact bytes:** Selector artifact_bytes counts its JSON export; direct-effect artifact_bytes counts model.pt only, excluding companion config/result JSON. Formats and scopes differ; not total deployment size.
- **failures:** Refusal, faults, wrong output, timeouts, missing cells, and instrument errors remain observations. Their time to stop is diagnostic, not successful execution performance or a speedup.
