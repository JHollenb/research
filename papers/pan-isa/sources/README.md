# Sources and provenance

These small snapshots make the study readable without a sibling `pan-isa` checkout. They were captured on **2026-10-30** from the workspace's `pan-isa/` repository. Every copied file and excerpt is byte-for-byte preserved; no paths, timestamps, historical gates, or results inside it have been rewritten. Absolute paths inside historical reports document the original run and are not links required by this study.

[manifest.json](manifest.json) records each workspace-relative original path, original whole-file SHA-256, snapshot SHA-256, byte length, whether it is a complete file or contiguous excerpt, and the original inclusive line range for excerpts. Snapshot hashes can be checked using only this research repository; originals are not required. The `.py.txt` files are deliberately excerpts, not runnable modules. The complete `.py` files are reference snapshots, not a packaged or self-contained executable environment.

## Measurement evidence

- [June 17 exact-status reconciliation](../evidence/pan_isa_exact_status.md): dated stage scopes, v21/v22 distinction, cumulative Stage 5, process/debugger capabilities, original PAN/QEMU result, full-ISA ledger. This is a project status synthesis, not the original per-step trace.
- [SPF comparison JSON](../evidence/pan_isa_spf_v2_comparison.json) and [its generated Markdown report](../evidence/pan_isa_spf_v2_comparison.md): machine-readable timing, RSS, storage scopes, selector-table representation, parity, and compile time. The underlying program, original checkpoints, PAN engine reports, and QEMU child report are not present in the inspected artifact snapshot and are not bundled here.
- [Stage 0 width-8 validation report](../evidence/stage0_w8_validation_report.json): primary result record with split sizes, exactness, byte-overlap checks, Unicorn agreement, controls, and retained operator diagnostics.
- [Stage 0 training summary](../evidence/stage0_w8_train_summary.json): factorized model identity and training trajectory.
- [Full-ISA ledger report](../evidence/full_isa_user64_report.json): machine-readable classification, named promotion, source-freeze outcome, and the retained one-row discrepancy between executable total and coverage-status sum.
- [Historical Stage 3 v21 training summary](../evidence/stage3_v21_train_summary.json): neural factorized-selector identity and selector scores. This does not override the later continuous-flag failure recorded in the status synthesis. The v22 raw artifact and Stage 5 raw summary were not available in the inspected local snapshot.

The full-ISA ledger retains an accounting inconsistency: `operand_subset_learned_validated=370`, `fully_validated_user64=1`, and `unimplemented=718` sum to 1,089 statuses, while the executable total is 1,088. Its summary does not establish which bucket should change. No invented reconciliation is applied. The source-freeze result also lacks the Intel SDM and AMD APM PDFs, despite frozen XED data. These limit the historical ledger's accounting and terminal certification, without erasing the scoped execution results.

## Architecture and implementation

- [Stage 0 scope](code/stage0_scope.py.txt), [networks](code/stage0_networks.py.txt), [effect commit](code/stage0_effect_commit.py.txt), and [structured control constructor](code/stage0_controls.py.txt).
- [Stage 1](code/stage1_network.py.txt), [Stage 2](code/stage2_network.py.txt), [Stage 3 selector and semantic handoff](code/stage3_selector.py.txt), and [Stage 4](code/stage4_network.py.txt).
- [Uninterrupted benchmark harness](code/benchmark_stage3_uninterrupted.py): PAN state feedback and per-step comparisons; QEMU guest generation and final-state assertions.
- [QEMU timing helper](code/qemu_until_serial_result.py): process-launch-to-observed-result timing, polling, child telemetry, and termination.
- [SPF benchmark implementation](code/benchmark_stage3_spf_v2.py): enumeration, materialization, block-matrix routing, and measurement scopes.
- [Neural runtime](code/neural_runtime.py): 33 labels, engineered input features, MLP, exported inference, and supplied-adapter comparison.
- [Runtime commit](code/runtime.py), [proposal schema and validator](code/transitions.py), and [SPF backend](code/spf_backend.py).
- [June 19 PAN-ISA whitepaper](WHITEPAPER-PAN-ISA.md) and [PAN Fabric whitepaper](WHITEPAPER-PAN-FABRIC.md): design intent and division of responsibility. Aspirational language in these sources is not treated as measurement.

Source code reflects the checkout at capture time, while historical reports retain their own dates. Architecture-derived parameter counts in the study describe explicitly named default configurations; they are not measurements of an unavailable checkpoint. The source bundle totals about 222 kB, excluding this index and manifest. No weights, large traces, external manuals, or benchmark images are copied.
