---
title: "Native-State Route Selector v6: Calibrated Abstention on an Unsupported Family"
type: experiment-report
status: exploratory-safety-result
followup_rank: 8
model: FLUX.2 Klein 4B
tags:
  - bfl
  - route-selection
  - uncertainty
  - fail-closed
---

# Native-State Route Selector v6: Calibrated Abstention on an Unsupported Family

> [!summary]
> A four-action selector used an earlier native state summary to choose `native`, two fixed repair routes, or abstention. Calibration selected a support radius with zero false positives, then the selector abstained on all unsupported green-circle held-outs and matched native continuation exactly. This is a useful distribution-shift safety result, not evidence of route utility or a semantic meta-router.

## Research question

If a fixed FLUX.2 recipient has several known route repairs, can an earlier native state decide when to apply one and when to leave the trajectory untouched? The primary risk is collateral: a route that helps one family can harm native successes in another. The experiment therefore prioritizes calibrated abstention over action diversity.

The test asks whether a selector can identify an in-support state where a non-native route has measured utility, while failing closed on a genuinely new held-out family. It never receives held-out outcomes at dispatch.

## Specimen and split

The selector uses a 32-dimensional pooled summary of earlier native `joint.1` text state. Development uses red families and two seeds; calibration uses disjoint red families and two seeds; final held-out uses green circles, green squares, and negative green triangles with two seeds. The four actions are `native`, `joint3_gain2`, `joint4_gain2`, and `abstain`, where abstain means native continuation.

The support radius is chosen from calibration-only route utility and collateral. A serving state outside the standardized support is not allowed to dispatch a repair. The native consumer, route payloads, evaluator, checkpoint, and held-out split are frozen before serving.

## How the experiment works

Development labels are formed from sealed route outcomes. The selector fits a small action policy over native-state features. Calibration estimates the largest support radius that produces zero false-positive repairs on its own disjoint panel. During held-out serving, the selector sees only the earlier native feature, chooses an action or abstains, and then the native suffix renders the final image.

The run includes fixed-route controls, native replay, zero-state, inverted-state, wrong-time, exact rewind, exact one-step suffix replay, and two independent image evaluators. Any evaluator disagreement is retained rather than silently choosing the favorable instrument.

## Results

The run contains 106 logical rows across 22 immutable parent cuts. Rewind, suffix replay, and forest closure checks are exact. The independent RGB evaluator and image atlas agree on 105/106 rows; the one disagreement is a calibration red-circle branch where downsampling merges components.

Calibration selected support multiplier `3.0` and radius `8.115`. At smaller multipliers the policy abstained on all eight calibration parents. At `3.0` it dispatched native on four and abstained on four, with zero calibration false positives.

On the green held-out panel, the selector abstained on both six-circle rows and selected native on both five-square rows and both negative three-triangle rows. It therefore matched constant native continuation exactly: positive mean count error `1.500` for both policies, positive exactness `0/4`, and all negative rows exact. Fixed `joint3` reached positive mean error `0.500`; fixed `joint4` reached `2.500` and visibly merged components.

![Held-out green-circle native branch](../artifacts/native-state-route-selector-v6/heldout__green_circles_six__seed-7001__native.png)

![Held-out green-square native branch](../artifacts/native-state-route-selector-v6/heldout__green_squares_five__seed-7001__native.png)

![Held-out negative triangle native branch](../artifacts/native-state-route-selector-v6/heldout__green_triangles_three_negative__seed-7001__native.png)

## Interpretation

The observation is that native-state features expose a distribution-shift signal that can support a fail-closed gate. The selector did not enter a regime where a non-native route had a calibrated advantage, so abstention was the correct result rather than a miss.

The working inference is `native state → support/distribution signal`, not `native state → per-parent repair utility`. The next experiment needs a calibration set with genuine in-support route advantages and a held-out family where a selector can beat constant native and fixed-route baselines without collateral.

## Claim boundary

Established: support-aware calibration, held-out outcome hiding, exact replay, independent evaluator agreement, and safe abstention on an unsupported family.

Not established: semantic route keys, route utility prediction, a useful meta-capability, or generalization beyond this split and action set.

## Local proof bundle

- [Bundle README](../artifacts/native-state-route-selector-v6/README.md)
- [Raw report](../artifacts/native-state-route-selector-v6/report.json)
- [Analysis](../artifacts/native-state-route-selector-v6/ANALYSIS.md)
- [Execution receipt](../artifacts/native-state-route-selector-v6/run-receipt.json)
- [Portable selector package](../artifacts/native-state-route-selector-v6/selector-package.npz)
- [Artifact verifier](../artifacts/native-state-route-selector-v6/verify.py)

