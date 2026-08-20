---
title: "Distributed K/V Causal Route in a Native FLUX.2 Consumer"
type: experiment-report
status: replicated-native-consumer-trend
rank_in_bfl_survey: 6
model: "FLUX.2 Klein 4B with native Qwen3 conditioning"
tags: [bfl, flux, causal-intervention, kv-route, color-binding, denoising]
---

# Distributed K/V Causal Route in a Native FLUX.2 Consumer

> [!summary]
> A 20-site intervention panel shows that color-binding information can be carried by a distributed K/V route in a native FLUX.2 Klein 4B generation. The route reproduces across all 20 tested sites, responds nonlinearly to dose, accumulates across denoising steps, and gives native S4 margins of +6.740 forward and +8.830 reverse with 83/96 and 88/96 endpoint recoveries. The adversarial reverse map contains 45/96 donor-color collisions, so bilateral specificity and portability remain open rather than established.

## Research question

The experiment asks whether a semantic variable can be traced to a distributed collection of attention key/value sites that remains causally active in the native image-generation loop. The target variable is color binding: the relation between a color token and the object or region that should receive that color. The test is deliberately stronger than correlating hidden activations with color. It intervenes on saved K/V values, resumes the unchanged native denoising suffix, and scores the rendered endpoint against paired color-swapped worlds.

The central alternatives are a distributed route, a small magic subset of blocks, or a nonspecific perturbation effect. A distributed route predicts that all tested sites should carry some causal signal, that an intervention over all sites should be stronger than a compact subset, and that the effect should grow when the same donor difference is installed over more denoising steps. A nonspecific perturbation predicts endpoint movement without consistent recovery of the intended color world.

## Specimen and assay

The specimen is FLUX.2 Klein 4B at 256×256 resolution with four denoising steps and native Qwen3 text conditioning. The assay contains 96 paired color-binding instances and 1,152 rendered endpoints. Each instance has a forward and reverse color world, matched prompt structure, a source trajectory, a donor trajectory, and control branches. Raw hashes and metadata were reverified after collection.

For each route site, the intervention forms a donor difference in the site's K/V state and adds a signed dose of that difference to the source state. The native model then consumes the modified state through its ordinary denoising, image-token, and decode path. The all-site arm applies the intervention at the full set of 20 tested route sites. The compact arm uses only sites `{8,11}`. Single-site arms isolate each member of the 20-site set. Forward and reverse directions are evaluated separately so that donor-color collisions can be identified instead of silently counted as specificity.

## What was measured

The primary endpoint is a native S4 margin: the score of the intended color-binding world minus the score of its matched alternative at the final image. A positive margin means that the endpoint favors the intended world. Recovery is the number of paired instances whose endpoint selects the intended world under the declared threshold. The route-dose analysis varies intervention dose and site coverage. The time accumulation analysis compares interventions installed at individual denoising steps with an all-step graft.

The conditioning audit separately compares how much color-token information is present in the Qwen3, T5, and CLIP conditioning streams. This is an instrument and bottleneck analysis, not a claim that the conditioner alone implements the route. Qwen3 has a final color/noncolor norm ratio of 0.936, while the corresponding T5 ratios are 0.10–0.16 and CLIP is 0.269 at effective rank approximately 2.2.

## Results

The 20-site panel is positive in both directions under the native S4 score. Forward recovery is 83/96 and reverse recovery is 88/96. The corresponding native margins are +6.740 forward and +8.830 reverse. Five matched controls are positive, providing a control set against which to interpret the main route result.

The route is distributed rather than a compact two-site circuit. The full 20-site intervention reproduces the effect across all tested sites, while the compact `{8,11}` quorum does not reproduce the same endpoint behavior. The result falsifies the narrower “magic block” explanation for this assay, but it does not prove that every untested site in every model family participates in the same way.

The dose curve has a nonlinear transition: small route doses remain near baseline, then endpoint recovery rises over a finite dose range rather than increasing smoothly from the first perturbation. The all-step graft is stronger than every single-step arm, showing that route authority accumulates over denoising time. This is consistent with a temporal coalition whose partial contributions are individually insufficient or weak but jointly decisive.

The adversarial adjudication changes the interpretation of the reverse score. In the reverse direction, 45/96 donor-color collisions contaminate the wrong-world map. The reverse recovery and margin therefore establish a strong assay result but do not establish bilateral semantic specificity. The correct conclusion is that the route is causally live for the declared native color-binding panel, with an unresolved ambiguity in reverse-world construction.

[Native K/V route audit](../artifacts/distributed-kv-causal-route/h9-raw-audit.v1.json)

## Mechanistic interpretation

The simplest working inference is that color-binding information is represented in a distributed set of K/V carriers whose downstream authority is jointly expressed by the denoising trajectory. The route does not behave like a single address or a two-block switch. Its nonlinear dose response suggests thresholded competition, recurrent amplification, or a score margin that only becomes visible after multiple route contributions are combined.

The conditioner audit supports a plausible upstream bottleneck: Qwen3 preserves a much larger color-token contrast than T5 or CLIP in the measured representation. That observation does not identify the exact causal transformation from text to K/V state. It does explain why a native Qwen3-conditioned assay is the appropriate consumer for this experiment and why a replacement conditioner would be a separate portability question.

## Controls and limitations

The compact `{8,11}` arm controls the hypothesis that the route is secretly a small block pair. Single-site arms control the possibility that the full effect is an artifact of one dominant site. Single-step arms control the possibility that all-step success is merely a measurement timing artifact. Forward/reverse adjudication controls the possibility that score asymmetry is caused by donor-color collisions.

The panel is model-, resolution-, step-count-, conditioner-, prompt-, and assay-specific. It does not establish portability to FLUX.1, to Klein 9B, to a different text encoder, or to unseen semantic axes. It also does not establish bilateral specificity because of the 45/96 reverse collision count. The raw audit records are retained so that a cleaner reverse-world construction can be added without rewriting this result.

## Claim status

**Observation:** K/V interventions at the 20 tested sites change native FLUX.2 endpoints in a color-binding assay.

**Convergent trend:** the effect is distributed, nonlinear in dose, stronger when accumulated over all denoising steps, and positive under native S4 margins in both declared directions.

**Working inference:** the assay exposes a distributed temporal K/V coalition rather than a compact magic-block circuit.

**Terminal status:** native-consumer causal trend for the declared Klein 4B assay. Bilateral specificity, model-family portability, and a universal route topology are not terminal claims.

## Local proof bundle

The local bundle contains the raw H9 audit, the adversarial adjudication, and the source evidence used to reconstruct the assay:

- [H9 raw audit](../artifacts/distributed-kv-causal-route/h9-raw-audit.v1.json)
- [adversarial H9 audit](../artifacts/distributed-kv-causal-route/adversarial-h9-raw-audit.v1.json)
- [bundle verifier](../artifacts/distributed-kv-causal-route/verify.py)

Run `python ../artifacts/distributed-kv-causal-route/verify.py` from this directory to verify the native margins, recovery counts, collision caveat, and conditioner-audit evidence.
