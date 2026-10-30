# PAN-ISA SPF v2 Comparison

## Program

- Trace: `uninterrupted-2026061701-8192`
- Instructions: `8192`
- Program bytes: `52373`
- RIP range: `0x0000000000500000` -> `0x000000000050cc95`

## Engines

| Engine | Exact | Final | Elapsed s | CPU s | Steps/s | QEMU faster by | Storage bytes | Max RSS bytes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| pan_stage3_v1 | 1.0 | True | 0.648707 | 0.652808 | 12628.19 | 3.912 | 129869 | 420593664 |
| pan_stage3_spf_v2 | 1.0 | True | 0.369115 | 0.368695 | 22193.6 | 2.226 | 140384 | 427950080 |
| qemu_x86_64 | 1.0 | True | 0.165826 | None | 49401.23 | 1.0 | 1477781 | 37830656 |

## SPF v2 Implementation

- SPF source: `/Users/jakeholl/domains/spectral-phase-format-research/src`
- Selector table: `[125, 16]`
- SPF scalar words: `2000`
- SPFTensor v2 block: `spf.tensor.v2.TensorBlock`
- SPFTensor v3 block: `spf.tensor.v3.SPFBlockV3`
- SPF block matrix router: `spf.tensor.core.LowRankOperator diagonal block matrix`
- Compile time: `0.371772` s
- Parity: `{'v2_words_exact': True, 'v3_words_exact': True, 'decoded_selector_table_exact': True, 'blockmatrix_routed_table_exact': True}`

## Notes

- PAN v1 and SPF v2 elapsed times measure Python execution loops, not model/SPF compile time.
- QEMU report is the existing run for the same uninterrupted program and includes child RSS telemetry.
- PAN RSS is measured in the Python/Torch process; QEMU RSS is measured for the emulator child process.
- PAN storage includes the Stage 3 checkpoint; SPF v2 storage also includes its materialized selector table; QEMU storage includes the image/report directory.
