# Multi-model object registers: evidence bundle

This bundle contains the compact execution receipts and proof panes for the 2026-08-19 campaign
that tested whether the object-register interface found on distilled `FLUX.2-klein-4B` (2026-08-18)
is a property of that one checkpoint or of the FLUX text-to-image program family.

All five jobs ran single-lease on Beast (16 GB CUDA, bf16) via mrun, strict preflight, no retries.
Every job's exact no-op and determinism gates read `0.0`, and evidence-plane sweeps are clean
(watch 0 fires, claims chains valid).

The full per-branch reports (`report.json`, 2.6–5.1 MB each) are not copied here; they are
reproducible from the proof sheets via the analyzer and referenced by their `saturn/results/`
paths in the [parent demo](../../demos/multi-model-object-registers.md#local-proof-bundle-and-reproduction).

## Files

- `run-receipt.job-17788d5a1b0d.json`: Arm A, `FLUX.2-klein-base-4B` (undistilled), native 50-step
  real-CFG (guidance 4.0) operating point, `enable_model_cpu_offload`, seeds 7217/31337.
- `run-receipt.job-638d05dcbff2.json`: Arm B, `FLUX.2-klein-9B`, 8 joint + 24 single blocks,
  Qwen3-8B conditioner, `enable_sequential_cpu_offload`, seed 7217.
- `run-receipt.job-a676189574d1.json`: Arm C base battery, `FLUX.1-schnell`, T5 + pooled-CLIP dual
  conditioner, fp8-e4m3 layerwise storage + sequential offload, seeds 7217/31337.
- `run-receipt.job-27fef20e82a0.json`: Arm C locality probes (same `FLUX.1-schnell` config) —
  the NP-window granularity ladder and downstream displacement/scale/zero controls.
- `run-receipt.job-e1ba0cbed889.json`: Arm E, cross-conditioner wrong-object diagnosis on
  `FLUX.2-klein-4B` with an in-job TECM v3 Smol→Qwen warm start (900 steps), seeds 7217/31337.
- `zoom-fox-base4b-seed31337.png`, `zoom-mug-port-base4b.png`: Arm A proof crops — the two-row
  subject patch turning the fox white, and the cross-scene displacement port turning the mug blue.
- `zoom-fox-klein9b-seed7217.png`, `zoom-mug-port-klein9b.png`: Arm B equivalents on klein-9B.
- `locality-strip-flux1.png`: Arm C granularity ladder (single row / NP window ±3 / active rows /
  padding-only / full-512 / pooled-CLIP-only) showing the FLUX.1 window-locality result.
- `xcond-diagnosis-strip.png`: Arm E transplant/repair strip — foreign subject rows write a wolf
  into the native scene, native subject rows write a fox back into the foreign scene.

Arm D (TECM v4 prompt-disjoint scheduler closure, `job-0a318a2d8c9d`) is a measured negative with
no proof-sheet renders selected for this bundle; its receipts and rendered acceptance table live at
`saturn/results/rosetta-cross-family-manalysis/tecm-scheduler-closure/job-0a318a2d8c9d/` (see the
parent demo for the linked `analysis.md`).

Run `python verify.py` from this directory. The check is receipt-level: it confirms each job
succeeded under its declared model/offload/seed contract and that the referenced proof images are
present. It does not re-derive the ROI or route-progress scalars, which live in the (uncopied)
`report.json` files.
