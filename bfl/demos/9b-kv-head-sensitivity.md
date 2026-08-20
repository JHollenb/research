---
title: "9B and 9B-KV Head-Sensitivity Stability"
type: experiment-report
status: physical-sensitivity-replication-trend
rank_in_bfl_survey: 15
model: "FLUX.2 Klein 9B and Klein 9B-KV"
tags: [bfl, flux, head-ablation, qkv, physical-circuit, stability, sensitivity]
---

# 9B and 9B-KV Head-Sensitivity Stability

> [!summary]
> A four-head ablation panel compares FLUX.2 Klein 9B with Klein 9B-KV, a natural finetune pair with identical tensor inventory but 96.1081% denoiser BF16 values rewritten. The physical sensitivity ordering is stable across the pair: D0H29 > D0H27 > S5H26 ≫ S22H25. D0H29 produces mean image MAD 13.54 in 9B and 11.61 in 9B-KV, while S22H25 is near silent at 1.03 and 0.78. The result shows that weight identity and intervention sensitivity can dissociate; it does not assign semantic ownership to any head.

## Research question

If two model variants have substantially different weights but preserve an internal circuit-like sensitivity pattern, what exactly is stable? This experiment asks whether one-head physical ablation produces the same relative ordering across Klein 9B and Klein 9B-KV. The target is a measurable response pattern, not a human semantic label.

The comparison is useful because an identical tensor inventory can create a false sense of identity, while a raw weight-delta fraction can create a false sense of complete rewrite. A head-sensitivity panel probes a third property: how the native consumer responds when a runtime-addressed component is removed or altered.

## Specimen and intervention

The two specimens are FLUX.2 Klein 9B and FLUX.2 Klein 9B-KV. They share the same tensor inventory, while 96.1081% of denoiser BF16 values differ. The panel ablates four heads one at a time: D0H29, D0H27, S5H26, and S22H25. Each ablation is evaluated on one prompt pair and two seeds in the native image consumer.

The response metric is mean image MAD from the unablated native output. Larger MAD means greater physical sensitivity to that head under the declared prompt and seeds. The ordering is compared across model variants rather than interpreted from absolute MAD alone.

## Results

The head ordering is stable in both variants:

| Head | Klein 9B mean MAD | Klein 9B-KV mean MAD | Interpretation |
|---|---:|---:|---|
| D0H29 | 13.54 | 11.61 | strongest tested sensitivity |
| D0H27 | lower than D0H29 | lower than D0H29 | second in the tested ordering |
| S5H26 | below D0H27 | below D0H27 | weaker but visible |
| S22H25 | 1.03 | 0.78 | near-silent in this panel |

The large rewrite fraction does not erase the relative physical pattern. D0H29 remains the strongest tested ablation and S22H25 remains near silent. The absolute MAD shifts downward in the KV variant for the strongest and near-silent heads, so the stable object is the ordering or sensitivity topology, not exact numeric identity.

[Head ablation source evidence](../artifacts/9b-kv-head-sensitivity/2026-08-06-flux-head-ablation-physical-circuit-signal.md)

## Mechanistic interpretation

The working inference is that runtime-address sensitivity can be more stable than raw weight identity. Finetuning can rewrite many values while preserving a route or interface that makes particular heads more influential to the native consumer. This is compatible with a functional reparameterization, a preserved address contract, or a shared downstream bottleneck.

The result does not identify what D0H29 “means.” An ablation effect can arise from a head's participation in routing, normalization, information transport, or downstream numerical conditioning. A semantically specific head-ownership claim would require concept-specific interventions, multiple prompts, multiple seeds, and consumer-closed rescue or replacement tests.

## Controls and limitations

Using the same four head addresses in both variants controls the comparison's physical coordinate system. The matched prompt pair and two seeds reduce dependence on one image realization. Reporting near-silent S22H25 alongside D0H29 prevents selection of only dramatic examples. The rewrite fraction establishes that sensitivity stability is not trivial weight identity.

The panel has four heads, one prompt pair, and two seeds. The ordering is therefore a trend, not a universal ranking over all heads or prompts. The output metric is physical image MAD, not semantic fidelity. This report explicitly does not claim semantic head ownership, causal necessity for a named concept, or invariance under another finetune.

## Claim status

**Observation:** the same relative head-sensitivity ordering appears in Klein 9B and Klein 9B-KV despite a large denoiser rewrite.

**Convergent trend:** strong D0H29, intermediate D0H27/S5H26, and near-silent S22H25 responses replicate across the pair.

**Working inference:** a runtime-addressed physical sensitivity pattern can remain stable while weights change substantially.

**Terminal status:** bounded physical-sensitivity trend. It is not a semantic circuit map or a general head ranking.

## Local proof bundle

The bundle contains the ablation narrative, both variant records, the model-family context, and the verifier:

- [head-ablation report](../artifacts/9b-kv-head-sensitivity/2026-08-06-flux-head-ablation-physical-circuit-signal.md)
- [Klein 9B record](../artifacts/9b-kv-head-sensitivity/flux2-klein-9b.md)
- [Klein 9B-KV record](../artifacts/9b-kv-head-sensitivity/flux2-klein-9b-kv.md)
- [bundle verifier](../artifacts/9b-kv-head-sensitivity/verify.py)

Run `python ../artifacts/9b-kv-head-sensitivity/verify.py` from this directory to verify the rewrite fraction, stable ordering, and absolute sensitivity values.
