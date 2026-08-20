---
title: FLUX.2 Klein 9B-KV — Tracer Model Profile
type: public-model-profile
status: wip
updated: 2026-08-06
model_id: flux2-klein-9b-kv
claim_status: exploratory-anatomy-and-internal-physiology
tags:
  - wip
  - black-forest-labs
  - flux2
  - klein
  - kv
  - tracer
  - manalysis
  - diffusion
  - circuit-discovery
related:
  - "[[bfl/artifacts/9b-kv-head-sensitivity/README|Tracer Profiles for Seven Black Forest Labs Components]]"
  - "[[flux2-klein-9b|FLUX.2 Klein 9B profile]]"
---

# FLUX.2 Klein 9B-KV — Tracer Model Profile

## Bottom line

Klein 9B-KV has the same measured coarse transformer geometry and Base Decoder role budget as
Klein 9B, but a fresh live profile shows a different internal sensitivity ordering. `D0H29` still
leads, yet `S22H25` appears second, near the end of the single stream, where the ordinary 9B run
instead ranked `S5H26`. This is a useful warning against treating static architecture parity as
circuit parity. The result is a candidate difference for targeted prompt-conditioned testing, not
a semantic characterization of the KV variant.

## Anatomy

| anatomy measurement | observed value |
|---|---:|
| transformer parameters | 9.079B BF16 parameters, 226 tensors |
| joint / single blocks | 8 / 24 |
| heads / head width / inner width | 32 / 128 / 4,096 |
| context width / image channels | 12,288 / 128 |
| physical Tracer components | 1,056 |
| static header scan / Tracer scan | 1.553 s / 24.526 s |
| static mrun job | 27.75 s, 1.524 GB peak RSS (`job-2eb98ce9e507`) |
| live Manalysis job | 36.94 s, 26.021 GB peak RSS (`job-7b99a717a9a0`) |

The static role partition is identical at the reported precision to the 9B entry: `66.53%`
operation/MLP (6.040B parameters), `7.39%` each selector/address, payload, carrier, and address
families (671.1M each), `3.34%` clock modulation, and `0.56%` content. The static map is therefore
a good shared search grammar but insufficient evidence for shared dynamic circuits.

## What was actually measured

The profile ran the real Diffusers transformer with deterministic one-token text/image internal
transport. It reconstructed Q/K attention before rotary position encoding (**pre-RoPE**), recorded
gradient × activation under a synthetic output-energy objective, zeroed two components, and ran a
reversible Winder adapter check. “Grad×activation” means local response of that precise objective;
it does not say that a head represents a word or image region.

## Physiology results

| measurement | observed value |
|---|---:|
| reconstructed layers / heads | 32 / 1,024 |
| pre-RoPE entropy, min / median / max | 0.000014 / 0.317474 / 0.692891 |
| mean reconstructed attention entropy | 0.304680 |
| output-energy MSE | 0.499392 |
| grad×activation Gini | 0.274456 |
| top-ten sensitivity share | 3.934% |

| rank | component | mean absolute grad×activation |
|---:|---|---:|
| 1 | `D0H29` | 0.000933 |
| 2 | `S22H25` | 0.000893 |
| 3 | `D0H27` | 0.000846 |
| 4 | `D0H25` | 0.000797 |
| 5 | `D0H7` | 0.000777 |
| 6 | `S8H25` | 0.000774 |

Compared with the non-KV 9B internal probe, the raw sensitivity scale is lower and the second
ranked site moves from mid single-stream `S5H26` to late `S22H25`. There are several plausible
explanations—variant-specific weights, KV behavior, or objective/probe interaction—so this is a
comparison worth testing, not a mechanism conclusion.

## Lesions, hypergraph, and Winder

| component zeroed | clean-output change |
|---|---:|
| `D0MLP` | 0.155476 |
| `D0H0` | 0.015150 |

The first joint MLP is again about ten times stronger than the first head under the tested lesion.
The suspected hypergraph retains `D0MLP`, `D0H0`, and supported combinations such as
`D0H0`–`D0H25`; it explicitly does not claim minimality, necessity, sufficiency, or semantics.

Winder attached a rank-1 adapter with 8,192 trainable parameters. The synthetic loss was
`0.0001056798` before/after the guarded step and after exact unwind. This is a clean mechanical
reversibility result, not an image edit and not evidence against future learnable adapters.

## What we know and what to do next

This report establishes real model anatomy, attention reconstruction, sensitivity, and two internal
causal lesions. It does not establish prompt-conditioned behavior or any visual difference from the
non-KV sibling. The right next experiment is a matched prompt/seed comparison of `D0H29`,
`D0H27`, `S8H25`, and the KV-specific candidate `S22H25`, using return-register and RGB effects to
determine whether the late single-stream sensitivity is actually consumed by the generator.

## Evidence

- [weight-only Tracer receipt](../../../experiments/20260806-192537-bfl-full-suite-tracer-mapper/results/flux2-klein-9b-kv.v3.json)
- [live Manalysis receipt](../../../experiments/20260806-192537-bfl-full-suite-tracer-mapper/results/flux2-klein-9b-kv.microprofile.v1.json)
- [SATURN map](../../../experiments/20260806-192537-bfl-full-suite-tracer-mapper/results/saturn/flux2-klein-9b-kv/model-function-map.json)
