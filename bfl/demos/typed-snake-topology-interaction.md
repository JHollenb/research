---
title: "Typed Snake Topology Repair and Native Interaction Residuals"
type: experiment-report
status: native-consumer-trend-with-causal-controls
rank_in_bfl_survey: 7
model: "FLUX.2 Klein 4B"
tags: [bfl, flux, topology, typed-route, interaction, residual]
---

# Typed Snake Topology Repair and Native Interaction Residuals

> [!summary]
> A typed donor relay changes a closed green coil into an open S-shaped snake through a four-site native route, reaching 0.9008 progress with mean absolute deviation 4.53 and zero topology holes. Route ablation, wrong-axis, half-dose, and held-out-seed controls separate the effect from a generic image perturbation. A paired interaction panel then shows that native lighting×color composition reaches 0.901 at full dose while naive additive composition reaches 0.396. The learned mixer fails to beat a linear held-out baseline, so the result is a native interaction residual and causal route repair, not a learned universal compositor.

## Research question

This report contains two linked but separately scored experiments. The first asks whether a typed route can repair a topological property of an object: turn a closed coil into an open S-shaped snake while preserving the intended green appearance. The second asks whether a native model stores a non-additive interaction between two semantic controls, using lighting and color as the pair. Both tests require the final native consumer to render the endpoint; hidden-state similarity alone is not accepted as proof.

The first experiment distinguishes a typed route from a generic donor injection. If the route is meaningful, a full-dose route should approach the open target, a half dose should be weaker, a wrong-axis route should fail to add the required green component, and route ablation should preserve the closed-coil failure. The second experiment distinguishes a native interaction residual from naive vector addition by comparing the native paired endpoint with an additive reconstruction, dose curves, wrong-time and wrong-site interventions, sign flips, and a norm-matched sham.

## Specimen and native execution

Both panels use FLUX.2 Klein 4B at 256×256 resolution and four denoising steps. The topology route is `joint.2 → joint.3 → joint.4 → single.0`. The source is a closed green coil, and the target is an open S-shaped snake. The interaction panel contains three semantic pairs and two seeds per pair, with 102 total branches evaluated in one resident model.

The typed route applies a donor-derived state difference only at the declared sites and preserves the remainder of the source state. A branch is then completed by the unchanged native denoising and decoding path. The interaction panel uses a pairwise native endpoint as the reference and tests whether that endpoint can be predicted by composing the two single-factor effects. All branch comparisons use the same prompt family, resolution, seed controls, and image-space progress definition.

## Topology-repair assay

Topology progress is the normalized movement from the closed-coil source toward the open-S target. Mean absolute deviation is reported against the target image, and a topology-hole counter checks whether the rendered shape remains closed. Full-dose route progress is 0.9008 with target MAD 4.53, an open shape, and zero topology holes. The half-dose route reaches 0.1884 progress with MAD 35.04. Route ablation reaches −1.0 progress, retains the closed coil, and contains a hole. The wrong-axis route reaches only 0.2716 and does not recover the green component.

The route generalizes directionally to held-out seeds, with progress 0.8344 and 0.8943. A critical caveat is retained: the original S-curve donor used in an early gallery was itself coiled, so that gallery was not a valid topology target. The corrected target-native panel is the evidence used for the result above.

![Full-dose typed topology repair](../artifacts/typed-snake-topology-interaction/repair_route.png)

![Half-dose topology repair](../artifacts/typed-snake-topology-interaction/repair_half.png)

![Route ablation](../artifacts/typed-snake-topology-interaction/route_ablation.png)

## Interaction-residual assay

For each semantic pair, let `E_A`, `E_B`, and `E_AB` be native endpoints for factor A, factor B, and the paired condition. The naive additive estimate is formed in the measured endpoint representation from the two single-factor changes. The native interaction residual is the difference between the paired native endpoint and that additive estimate. The endpoint progress values are evaluated by the same consumer and normalized to the native pair target.

At dose 1.0, the native pair reaches 0.901 progress, matching the native AB endpoint by construction, while naive additive composition reaches 0.396. The dose curve for the native residual is 0.568, 0.697, 0.821, 0.901, and 0.8175 at doses 0.25, 0.5, 0.75, 1.0, and 1.25. This rising-then-falling curve is evidence of a finite useful intervention range rather than a monotonic “more is better” rule.

The wrong-time intervention reaches 0.657, wrong-site reaches 0.433, sign flip reaches 0.266, and a norm-matched sham reaches −0.401. These controls indicate that endpoint progress depends on when and where the interaction residual is installed and on its sign. The learned mixer did not beat the linear held-out baseline, so the panel does not claim that a small learned module has recovered the model's full composition rule.

[Native versus additive interaction panel](../artifacts/typed-snake-topology-interaction/interaction-residual-analysis.md)

## What the controls establish

The topology ablation controls route necessity for this repair, the half dose controls dose dependence, the wrong-axis control tests typed address selectivity, and held-out seeds test whether the effect is confined to one noise realization. The invalid early S-curve donor is retained as an instrument-quality caveat rather than silently discarded.

The interaction controls show that the native paired endpoint is not well explained by adding two isolated semantic effects. Wrong-time and wrong-site degradation provide spatial-temporal localization, sign reversal suppresses the intended effect, and the sham moves away from the target. The learned-mixer miss establishes a boundary: the measured residual is useful as an intervention and diagnostic, but it has not been distilled into a validated standalone compositor.

## Claim status

**Observation:** a four-site typed relay can causally repair the declared snake topology, and native semantic pairs contain a large non-additive endpoint residual.

**Convergent trend:** full-dose route repair, dose weakening, route ablation, wrong-axis failure, held-out seed recovery, native-vs-additive separation, and temporal/site/sign controls all point in the same direction.

**Working inference:** typed route state can carry a topology-specific correction, while semantic composition is computed by a native interaction mechanism that is not captured by simple addition.

**Terminal status:** native-consumer causal trend for the declared Klein 4B panels. It is not evidence for a universal topology editor, a learned interaction module, or a general factorization law.

## Local proof bundle

The bundle contains raw topology reports, native branch images, and the interaction analysis:

- [topology report](../artifacts/typed-snake-topology-interaction/report.json)
- [topology route image](../artifacts/typed-snake-topology-interaction/repair_route.png)
- [interaction residual analysis](../artifacts/typed-snake-topology-interaction/interaction-residual-analysis.md)
- [bundle verifier](../artifacts/typed-snake-topology-interaction/verify.py)

Run `python ../artifacts/typed-snake-topology-interaction/verify.py` from this directory to check the route, dose, ablation, held-out, and native-interaction values.
