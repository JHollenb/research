---
title: FLUX.2 Klein 9B — Tracer Model Profile
type: public-model-profile
status: wip
updated: 2026-08-06
model_id: flux2-klein-9b
claim_status: exploratory-anatomy-and-internal-physiology
tags: [wip, black-forest-labs, flux2, klein, tracer, manalysis, diffusion, circuit-discovery]
related:
  - "[[README|Tracer Profiles for Seven Black Forest Labs Components]]"
  - "[[flux2-klein-9b-kv|FLUX.2 Klein 9B-KV profile]]"
---

# FLUX.2 Klein 9B — Tracer Model Profile

## Bottom line

Klein 9B expands the Klein topology to eight joint blocks, 24 single blocks, and 32 heads. A fresh
real-model run now provides the full bounded Manalysis suite rather than a static-only placeholder.
The strongest local-sensitivity sites on the internal probe are `D0H29`, `S5H26`, `D0H27`, and
`D0H7`; the first joint-block MLP is the strongest tested lesion. These observations nominate a
compact first experiment set, but they do not yet identify lexical or visual semantics.

## Anatomy

| anatomy measurement | observed value |
|---|---:|
| transformer parameters | 9.079B BF16 parameters, 226 tensors |
| joint / single blocks | 8 / 24 |
| heads / head width / inner width | 32 / 128 / 4,096 |
| context width / image channels | 12,288 / 128 |
| physical Tracer components | 1,056 |
| static header scan / Tracer scan | 0.679 s / 26.038 s |
| static mrun job | 28.30 s, 1.522 GB peak RSS (`job-f8b709f59b48`) |
| live Manalysis job | 35.90 s, 25.774 GB peak RSS (`job-de26b9cbef0a`) |

Tracer’s forward-free role census assigns `66.53%` of parameter mass (6.040B parameters) to
operation/MLP families, `7.39%` each to selector/address, payload, and carrier families (671.1M
each), `3.34%` to the time-conditioning clock, and `0.56%` to content paths. These numbers define
the candidate universe efficiently; they are not observations of a prompt-specific circuit.

## What the live assay means

The live run uses one deterministic text token and one image token. The reported MSE is the
prediction energy against zero for a synthetic internal flow probe. A **head** is one attention
routing subchannel; an **MLP** is the nonlinear operation path; **grad×activation** measures local
sensitivity of that synthetic output; and **ablation** zeros a component output and measures the
resulting difference from clean output.

The attention maps are reconstructed from Q/K before rotary positional encoding (*pre-RoPE*), so
they are useful routing summaries, not exact exposed Diffusers attention probabilities.

## Physiology results

| measurement | observed value |
|---|---:|
| reconstructed layers / heads | 32 / 1,024 |
| pre-RoPE entropy, min / median / max | `4.99e-10` / 0.320710 / 0.693106 |
| mean reconstructed attention entropy | 0.302477 |
| output-energy MSE | 0.498085 |
| grad×activation Gini | 0.304016 |
| top-ten sensitivity share | 4.128% |

| rank | component | mean absolute grad×activation |
|---:|---|---:|
| 1 | `D0H29` | 0.002186 |
| 2 | `S5H26` | 0.001915 |
| 3 | `D0H27` | 0.001740 |
| 4 | `D0H7` | 0.001593 |
| 5 | `D0H9` | 0.001411 |
| 6 | `S8H25` | 0.001404 |

Two things are worth retaining. First, `D0H29`, `D0H27`, and `D0H7` put several early joint heads
at the top of the ranking. Second, `S5H26` is a mid-depth single-stream head, so the probe does
not reduce to an early text/image interaction alone. A circuit search should test both routes and
their interaction, rather than choose one from this ranking alone.

## Tested causal sites and suspected hypergraph

| component zeroed | clean-output change |
|---|---:|
| `D0MLP` | 0.149558 |
| `D0H0` | 0.018289 |

The 1,056-node component manifest yields a deliberately small hypergraph: `D0MLP` and `D0H0` are
supported by both the lesion and backward measurements; a `D0H0`–`D0H25` pair is retained as a
follow-up candidate. This is a discovery shortlist, not an exhaustive ablation or a minimality
test. The scale gap is important: only two components were directly lesioned.

## Winder result

The rank-1 Winder adapter exposed 8,192 trainable boundary parameters. Its synthetic one-step loss
was `0.0001048957` before and after the guarded update, and after removal; exact unwind succeeded.
The result says that reversible activation editing is mechanically healthy and the line-search did
not accept a worse step. It does not say that Klein 9B cannot be edited, nor that an image concept
has been manipulated.

## Current interpretation and next experiment

This model is no longer “not run”: Tracer has a verified anatomy, backward sensitivity map,
reconstructed attention panel, causal internal lesions, and Winder receipt. It is still missing the
prompt-conditioned consumer evidence needed to label a circuit as lexical, spatial, or visual. The
highest-value next run is a three-seed prompt-pair experiment that compares early joint heads
`D0H27/D0H29`, the mid single head `S5H26`, and `D0MLP` against matched random heads, recording
both the scheduler return state and final image.

## Evidence

- [weight-only Tracer receipt](../../../experiments/20260806-192537-bfl-full-suite-tracer-mapper/results/flux2-klein-9b.v3.json)
- [live Manalysis receipt](../../../experiments/20260806-192537-bfl-full-suite-tracer-mapper/results/flux2-klein-9b.microprofile.v1.json)
- [SATURN map](../../../experiments/20260806-192537-bfl-full-suite-tracer-mapper/results/saturn/flux2-klein-9b/model-function-map.json)
