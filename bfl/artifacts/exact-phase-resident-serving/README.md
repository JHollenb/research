# Exact phase-resident serving: cross-model evidence bundle

This bundle contains the compact evidence for the [Exact Phase-Resident Serving, Replay, and Edit Caching Across FLUX](../../demos/exact-phase-resident-serving.md) demo. It joins the original Klein-4B receipts to the 2026-08-19 phase-parity and reference-edit cross-model campaigns.

## Original receipts

- `phase-parity-receipt.json`: original Klein-4B 512² phase-resident panel, 8/8 pixel/PNG exact, 10.66× denoise-loop and 6.25× end-to-end speedups.
- `cheap-deep-replay-receipt.json`: exact suffix replay at six saved cuts, including the late-cut 7.993× result.
- `edit-cache-receipt.json`: original four-edit reference cache, 4/4 exact, 4,696.49× median lookup speedup, and four invalidations.
- `cache-receipt.json` and `edit-cache-run-receipt.json`: cache custody and execution receipts.

## Cross-model receipts and analyses

- `phase-parity-crossmodel-analysis.md`: certified resident and sequential cells, fast fp8 substrates, and the non-bitwise fp8-resident hybrid.
- `run-receipt.phase.job-4bc506e9fe64.json`: resident-lane first run; images were exact, but post-render cleanup failed and the receipt is retained as null/harness evidence.
- `run-receipt.phase.job-6a7f7b0603dd.json`: corrected sequential-lane specimen; clean receipt for the 9B and FLUX.1 exact cells.
- `run-receipt.phase.job-271e7732c430.json`: fast-v1 follow-up; fp8-sequential evidence retained, resident hybrid attempt incomplete.
- `run-receipt.phase.job-4da6fc7c4238.json`: fast-v2 follow-up; exact fp8-sequential cells and separate non-bitwise hybrid throughput cell.
- `edit-reuse-crossmodel-analysis.md`: plain-Klein cache replication and the 9B-KV ABI boundary.
- `run-receipt.edit.job-d6832f02cdf2.json`: v2 edit-reuse panel; plain-Klein cells completed, KV class-mismatch evidence retained.
- `run-receipt.edit.job-df22ad4e5c17.json`: corrected KV-v3 cell; cache mechanics pass, replay remains non-exact.
- `run-receipt.edit.job-981b01d2de66.json` and `run-receipt.edit.job-86f2ae8e1d0a.json`: earlier null-evidence runs preserved for the latent-channel and decode-signature corrections.

The full immutable reports remain under `saturn/results/phase-parity-crossmodel/` and `saturn/results/edit-reuse-crossmodel/`. This local bundle keeps the receipts and analysis notes small enough for the standalone research demo while preserving the distinction between clean results, partial evidence, and declared ABI boundaries.

Run `python verify.py` from this directory, or `python ../artifacts/exact-phase-resident-serving/verify.py` from `research/bfl/demos/`.
