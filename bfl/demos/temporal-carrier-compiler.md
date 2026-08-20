---
title: "Temporal Carrier Compiler: Route × Denoising-Time Authority"
type: experiment-report
status: exploratory
followup_rank: 4
model: FLUX.2 Klein 4B
tags:
  - bfl
  - temporal-control
  - carrier
  - causal-intervention
---

# Temporal Carrier Compiler: Route × Denoising-Time Authority

> [!summary]
> A 16-cell image-stream search over four routes and four denoising steps selected `joint.2 → step 3 → image`. The selected Act transferred part of two pair-disjoint held-out edits with strong wrong-time, sign, and sham separation. The result is a late-authority trend, not a complete semantic compiler.

## Research question

A route address alone may be too coarse for a generative trajectory whose semantic authority changes over time. This experiment searches route and denoising phase jointly and asks when a native image-stream carrier becomes capable of transferring an edit into the final image.

The design deliberately excludes direct cross-prompt text replacement because text sequence lengths can differ. It tests a shape-safe image-stream boundary and therefore isolates temporal authority from a text-shape confound.

## Specimen and split

The specimen is FLUX.2 Klein 4B under a fixed native schedule. Candidate coordinates are `joint.2`, `joint.3`, `joint.4`, and `single.0`, each at denoising steps `0–3`, for 16 image-stream candidates. Two discovery pairs select the coordinate; two pair-disjoint held-out pairs, lighting × relation and orientation × relation, evaluate it at seeds `52013` and `52019`.

The outcome is measured by progress toward a native target, return progress after continuing from the modified state, continuation alignment, collateral, and exact checkpoint replay. Zero-dose, sign-flip, wrong-time, and norm-matched sham branches are load-bearing controls.

## How the experiment works

For each candidate, the worker captures the source and native target image-stream boundary at the chosen step. It forms an Act from the boundary difference and injects that Act into the source trajectory. The remaining schedule and decoder run natively. The same parent checkpoint is then replayed with the Act removed, with the Act applied at the wrong step, with its sign flipped, and with a norm-matched random substitute.

The selection score combines target progress, return alignment, and collateral. The held-out panel is pair-disjoint from selection. The exact replay branch compares the scalar suffix to the corresponding native continuation and requires RGB MAD `0.0` when no intervention is applied.

## Results

The selected coordinate was `joint.2 → step 3 → image`. The early-authority curve increased toward the late step:

| denoising step | authority |
|---:|---:|
| 0 | `0.035` |
| 1 | `0.228` |
| 2 | `0.508` |
| 3 | `0.722` |

Across four held-out cells, the selected Act reached mean progress `0.545` toward the native target, mean return progress `0.717`, and mean return alignment `0.978`. Controls were near zero: zero-dose `0.000`, wrong-time `0.001`, norm-matched sham `-0.008`, and sign-flip `0.047`. Exact scalar suffix replay retained RGB MAD `0.0` against the unmodified native suffix.

![Lighting relation held-out result](../artifacts/temporal-carrier-compiler/lighting__relation__seed-52013.png)

![Orientation relation held-out result](../artifacts/temporal-carrier-compiler/orientation__relation__seed-52019.png)

## Interpretation

The observation is a convergent temporal trend: the tested image-stream carrier has much greater authority at the late candidate step than at early steps. The selected Act is specific enough to separate wrong-time and sign controls, but it transfers only part of the target behavior.

The working inference is that semantic edits are distributed across route and phase, with a late consumer-facing boundary that has higher leverage. A future compiler should learn phase-conditioned payloads and include explicit collateral and dose controls rather than treating a single route as a time-invariant slot.

## Claim boundary

Established: a 16-cell route × step search can select a late image-stream coordinate with held-out transfer and strong controls; timing is load-bearing; and no-op replay is exact.

Not established: a universal causal clock, donor-free semantic compilation, or a single route that carries all visual factors across prompts, seeds, models, or resolutions.

## Local proof bundle

- [Bundle README](../artifacts/temporal-carrier-compiler/README.md)
- [Raw report](../artifacts/temporal-carrier-compiler/report.json)
- [Execution receipt](../artifacts/temporal-carrier-compiler/run-receipt.json)
- [Artifact verifier](../artifacts/temporal-carrier-compiler/verify.py)

