---
title: "H9 After Adversarial Review: Five Controls Held, One Needs Repair"
date: 2026-08-01
updated: 2026-08-02
status: corrected
claim_status: distributed-route-supported-bilateral-specificity-partially-resolved
tags: [flux, mechanistic-analysis, native-circuit, specificity, replication, measured]
source_docs:
  - ../../experiments/2026-07-31-211500-flux-arbitration-harness/H9_SPECIFICITY_REPLICATION_DESIGN.md
  - ../../experiments/2026-07-31-211500-flux-arbitration-harness/outputs/h9-specificity-replication/h9-specificity-replication.v1.json
  - ../../experiments/2026-07-31-211500-flux-arbitration-harness/outputs/h9-specificity-replication/H9_VISUAL_AUDIT.md
  - ../../experiments/2026-07-31-211500-flux-arbitration-harness/CIRCUIT_CLOSURE_LEDGER.md
  - ../../experiments/2026-08-02-bfl-three-claims/FINAL_ADJUDICATION.md
  - ../../experiments/2026-08-02-bfl-three-claims/h9-causal-route/ADVERSARIAL_REVIEW.md
  - ../../experiments/2026-08-02-bfl-three-claims/h9-causal-route/OWNER_REPAIR_STATUS.md
  - ../../experiments/2026-07-31-211500-flux-arbitration-harness/H9_REVERSE_WRONG_WORLD_REPAIR_DESIGN.md
related:
  - "[[../indexes/generative-model-analysis|Generative Model Analysis Index]]"
  - "[[../generative-model-wiki|Generative Model Wiki]]"
  - "[[../model-analysis-wiki|Model Analysis Wiki]]"
  - "[[../black-forest-labs-model-wiki|Black Forest Labs Model Wiki]]"
  - "[[2026-08-01-040000-inside-the-flux-arbitration-harness|Inside the FLUX Arbitration Harness]]"
  - "[[2026-08-01-001500-opening-the-black-forest-what-six-parallel-tracks-taught-us-about-flux|Opening the Black Forest]]"
  - "[[2026-08-01-h8-temporal-route-localization|The Route Accumulates Across Time]]"
  - "[[2026-08-01-h7-heldout-quotient-replication|The Route Replicated; Native Specificity Did Not]]"
  - "[[2026-08-01-h6-native-quotient-dose|The Native Quotient Has a Dose Curve]]"
---

# H9 After Adversarial Review: Five Controls Held, One Needs Repair

H9 remains a strong causal-intervention result, but its original automatic verdict is no longer the
owner verdict. An independent review found that the reverse wrong-world arm reused a donor map
validated only for the forward payload. Forty-five of 96 reverse donors collide with one of the
destination colors, including 20 that already carry the reverse target color.

The correction is specific and consequential: the distributed route, image custody, scorer,
five controls, and temporal result survive; the bilateral six-control specificity gate does not.

## Current verdict

`PARTIALLY_RESOLVED — DISTRIBUTED ROUTE SUPPORTED; REVERSE WRONG-WORLD CONTROL PENDING REPAIR`

The original report's `NATIVE_SPECIFICITY_SUPPORTED_FOR_ASSAY` value is preserved as the runner's
historical automatic output. It is superseded as a terminal scientific conclusion because one of
its six controls was not what the design claimed.

## What H9 measured

- Model: FLUX.2 Klein 4B at revision
  `e7b7dc27f91deacad38e78976d1f2b499d76a294`.
- Conditioner: the Qwen3 conditioner packaged with that pinned Klein 4B artifact; no independent
  upstream conditioner digest was recorded.
- Workload: 48 prompt pairs × two base seeds = 96 paired instances.
- Protocol: 12 arms, 1,152 renders, 512×512, four denoising calls.
- Native route: S4 `{7,11,13,14}`, joint K/V, all four calls.
- Positive benchmark: full20 joint K/V transfer.

Every one of the 1,152 stored PNG hashes, dimensions, modes, and row records was independently
reverified. The four harness suites originally passed `18/18`; after the donor-map source repair and
new regression fixture, the expanded suite passes `21/21`.

## The six measured contrasts

| Direction | Control | Mean difference | Original 95% interval | Control status |
|---|---|---:|---:|---|
| Forward | wrong-token | +5.292 | [+3.332, +7.419] | valid |
| Forward | wrong-world | +6.910 | [+4.523, +9.404] | valid; 0/96 donor-color collisions |
| Forward | scrambled | +6.285 | [+4.135, +8.644] | valid |
| Reverse | wrong-token | +7.311 | [+4.762, +10.080] | valid |
| Reverse | wrong-world | +6.171 | [+3.270, +9.090] | **invalid as collision-safe** |
| Reverse | scrambled | +8.450 | [+5.640, +11.365] | valid |

The original bootstrap treated 96 rows as independent even though each prompt pair contributed two
seeds. Reanalysis averaged within 48 prompt-pair clusters and applied a one-sided six-contrast
Bonferroni bound. All six nominal calculations remained positive, but arithmetic cannot repair a
contaminated control.

The five valid contrasts retain positive conservative six-family lower bounds:

| Valid contrast | Familywise lower bound |
|---|---:|
| Forward native − wrong-token | +2.345 |
| Forward native − wrong-world | +3.431 |
| Forward native − scrambled | +2.949 |
| Reverse native − wrong-token | +3.510 |
| Reverse native − scrambled | +4.269 |

A stricter all-palette hue sensitivity also remains positive for these five controls; its smallest
valid familywise lower bound is `+2.317`. This sensitivity shares the same hue representation and is
not an independent semantic scorer.

## The reverse wrong-world defect

The harness generated one map with `world="clean"`. That rule checks the source pair's `color_a`
against both destination colors, which is correct for the forward clean-A store. H9 reused the same
map for the reverse corrupt-A store, where the carried source color is `distractor`.

| Reverse-map audit | Count |
|---|---:|
| Entries / unique sources / self-maps | 96 / 96 / 0 |
| Source distractor collides with either destination color | 45/96 |
| Source distractor equals the reverse target | 20/96 |
| Source distractor equals the alternate clean color | 25/96 |
| Safe reverse donors | 51/96 |

The reverse statistic is retained as a contaminated trend, not discarded. Post-hoc filtering to the
51 safe rows remains positive, but it was not preregistered and is not a repair.

## What still holds

The route-level native S4 margin remains `+6.740 [4.414, 9.254]` forward and
`+8.830 [5.988, 11.804]` reverse. Full20 produces much larger continuous effects and reaches the
strict endpoint in `83/96` forward and `88/96` reverse instances. S4 reaches `0/96` endpoints in
both directions: it is a continuous route intervention, not an endpoint-sufficient compact circuit.

H8 is unaffected. Its full20 all-step intervention exceeds every corresponding single-step arm,
and late-minus-early effects are negative. The defensible temporal conclusion is distributed
accumulation across denoising calls.

Visual review also remains useful but bounded. The images are coherent, and malformed output does
not explain the effects. Visual coherence cannot validate the semantic construction of a donor
control, which is why the reverse defect matters despite good-looking images.

## Repair status

The shared harness now builds separate clean-world and corrupt-world donor permutations and
certifies both source colors against both destination colors. The H9 wrapper can no longer replace
the reverse map with the forward map.

The frozen H9R run repeats the original 48-pair/two-seed workload with three arms: clean baseline,
reverse native S4, and corrected reverse wrong-world. Baseline/native images and metrics must match
H9 exactly before the corrected arm can join the five valid original contrasts. The terminal rule
is one 48-cluster, 10,000-resample, six-contrast Bonferroni adjudication.

mrun `job-9bd1dd958932` is payload-sealed at low priority behind existing GPU work. A queued job is
not evidence.

## Current claim boundary

The evidence supports an assay-relative distributed native K/V intervention route with temporal
accumulation and five valid specificity controls. It does not yet support the original bilateral
six-control closure. It also does not establish endogenous necessity, a compact quorum, universal
semantic ownership, cross-model portability, or Black Forest Labs' private training mechanism.

The neighboring Qwen result remains a boundary comparison only:
[[2026-08-01-213500-the-answer-fiber-became-a-consumer-quorum|The Answer Fiber Became a
Consumer Quorum]] does not show that Qwen and FLUX share a semantic plane or quorum.

## Filed in the model-analysis corpus

This result is cross-indexed so the bounded claim can be read in its model, modality, and arc
contexts:

- [[../indexes/generative-model-analysis|Generative Model Analysis Index]] — synthesis and claim boundary.
- [[../generative-model-wiki|Generative Model Wiki]] — modality-wide front door.
- [[../model-analysis-wiki|Model Analysis Wiki]] — broader analysis map.
- [[../black-forest-labs-model-wiki|Black Forest Labs Model Wiki]] — FLUX-family custody and mechanism context.
- [[2026-08-01-040000-inside-the-flux-arbitration-harness|Inside the FLUX Arbitration Harness]] — complete H1–H9 arc report.
- [[2026-08-01-001500-opening-the-black-forest-what-six-parallel-tracks-taught-us-about-flux|Opening the Black Forest]] — six-track Black Forest Labs program arc.

## Artifacts

- [H9 design](../../experiments/2026-07-31-211500-flux-arbitration-harness/H9_SPECIFICITY_REPLICATION_DESIGN.md)
- [H9 report](../../experiments/2026-07-31-211500-flux-arbitration-harness/outputs/h9-specificity-replication/h9-specificity-replication.v1.json)
- [H9 visual audit](../../experiments/2026-07-31-211500-flux-arbitration-harness/outputs/h9-specificity-replication/H9_VISUAL_AUDIT.md)
- [H9 attempt log](../../experiments/2026-07-31-211500-flux-arbitration-harness/outputs/h9-specificity-replication/H9_ATTEMPT_LOG.md)
- [Circuit closure ledger](../../experiments/2026-07-31-211500-flux-arbitration-harness/CIRCUIT_CLOSURE_LEDGER.md)
- [Three-claim final adjudication](../../experiments/2026-08-02-bfl-three-claims/FINAL_ADJUDICATION.md)
- [C3 adversarial review](../../experiments/2026-08-02-bfl-three-claims/h9-causal-route/ADVERSARIAL_REVIEW.md)
- [C3 owner repair status](../../experiments/2026-08-02-bfl-three-claims/h9-causal-route/OWNER_REPAIR_STATUS.md)
- [H9R frozen repair design](../../experiments/2026-07-31-211500-flux-arbitration-harness/H9_REVERSE_WRONG_WORLD_REPAIR_DESIGN.md)
