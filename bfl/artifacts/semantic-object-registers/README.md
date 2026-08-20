# Semantic circuit object Part III proof bundle

This is the compact proof bundle for [Semantic Circuit Object Part III: Semantic Object Registers Across FLUX](../../demos/semantic-circuit-object-part-III.md). It joins the original FLUX.2 object interface to the 2026-08-19 multi-model, value-algebra, cross-conditioner, and struct-write follow-ups.

The bundle is intentionally compact: large per-branch `report.json` files remain immutable under `saturn/results/`, while this directory holds the run receipts and human-facing proof panes used by the report. Every copied CUDA arm passed its declared mrun success, strict-preflight, single-lease, and exact no-op/determinism checks in the source receipt. The visual panes are the corrected analyzer outputs; panes are primary when ROI scalars are diluted by background or donor-pose mismatch.

## Receipts

- `run-receipt.job-17788d5a1b0d.json`: undistilled FLUX.2-klein-base-4B, 50-step real CFG, seeds 7217/31337.
- `run-receipt.job-638d05dcbff2.json`: FLUX.2-klein-9B, 4-step sequential offload, seed 7217.
- `run-receipt.job-3e1bc534e0eb.json`: FLUX.2-klein-9B, 512² debug replay, seed 7217.
- `run-receipt.job-a676189574d1.json` and `run-receipt.job-27fef20e82a0.json`: FLUX.1-schnell base battery and locality probes.
- `run-receipt.job-e920a0e84b37.json` and `run-receipt.job-ee619dfec24f.json`: FLUX.1 route certification and rows-plus-pooled interaction.
- `run-receipt.job-3980f89faa61.json`, `run-receipt.job-65d315d873dc.json`, and `run-receipt.job-86cb59fb03a0.json`: FLUX.1 window algebra, pair mining, and context-rotation debug.
- `run-receipt.job-e1ba0cbed889.json`: cross-conditioner wrong-object diagnosis on klein-4B.
- `run-receipt.job-0a318a2d8c9d.json` and `tecm-closure-analysis.md`: prompt-disjoint closure negative.
- `run-receipt.job-f0edaded5d06.json`: klein-4B struct-write debugger I/O and durable manifest round trip.

## Proof panes

- FLUX.2 replication: `zoom-fox-base4b-seed31337.png`, `zoom-mug-port-base4b.png`, `zoom-fox-klein9b-seed7217.png`, `zoom-mug-port-klein9b.png`, `zoom-fox-9b-512-seed7217.png`, `zoom-mug-port-9b-512.png`, `proof-sheet-foxball-9b-512-seed7217.png`, and `proof-sheet-catmug-9b-512.png`.
- FLUX.1 address grain and route: `locality-strip-flux1.png`, `rows-pooled-interaction-strip.png`.
- Wrong-object register diagnosis: `xcond-diagnosis-strip.png`.
- Value-level algebra: `window-algebra-strip.png`, `zoom-mug-window-port.png`, `pure-color-port-strip.png`, `pure-color-debug-strip.png`, `species-prior-strip.png`, and `zoom-mug-pure-color.png`.
- Struct write-back: `struct-write-strip-seed7217.png`, `struct-write-strip-seed31337.png`, and `zoom-ball-remove-vs-translate.png`.

The source reports and the reproducible analyzer are in `saturn/experiments/2026-08-19-object-multimodel/`. The bundle does not replace those immutable source artifacts; it makes the cross-model proof legible from the standalone BFL demo.

Run `python verify.py` from this directory, or `python ../artifacts/semantic-object-registers/verify.py` from `research/bfl/demos/`.
