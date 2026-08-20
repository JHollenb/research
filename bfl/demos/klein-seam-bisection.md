---
title: "Klein Seam Bisection: Base Future Capture and Distilled Recipient Repair"
type: experiment-report
status: exploratory
followup_rank: 1
model: FLUX.2 Klein 4B Base and distilled checkpoints
tags:
  - bfl
  - causal-intervention
  - distillation
  - capability-repair
---

# Klein Seam Bisection: Base Future Capture and Distilled Recipient Repair

> [!summary]
> A Base checkpoint was used only as a sealed future donor while a fresh distilled recipient searched 32 route × timestep × stream seams for a small rank-8 repair. The selected seam was `joint.2 → step 0 → text`; it reproduced one of four held-out count cells, so the run demonstrates a clean split-load protocol and a localized mismatch, not general capability restoration.

## Research question

FLUX.2 Klein Base and distilled checkpoints can produce different object counts from the same prompt family. The experiment asks whether the behavioral gap can be localized to one early carrier seam and repaired inside the distilled recipient without loading the Base model during repair, copying donor logits, or looking up the held-out answer.

The important distinction is between a capability gap and a donor replay. A valid repair must fit a compact intervention from sealed Base activations, install it into the distilled recipient, and let the recipient's own scheduler and image decoder produce the final output. A correct result on one prompt is not enough; held-out cells, zero-dose, sign, wrong-site, and energy-matched controls must be retained.

## Specimen and split

The organism is FLUX.2 Klein 4B at the fixed scalar inference configuration recorded in the local receipts. The Base capture stage rendered three red squares and five blue circles for discovery, plus four red squares and six blue circles for held-out evaluation, at seeds `31337` and `31339`. The distilled repair stage consumed only the sealed Base boundary artifacts and its own native checkpoint.

The route search covered `joint.2`, `joint.3`, `joint.4`, and `single.0`; denoising steps `0–3`; and text versus image streams. That gives 32 candidate seams. The intervention was rank 8 and coordinate-local. The evaluator counted connected components of the requested color, while exact checkpoint replay and suffix RGB equality checked that the repair did not alter unrelated execution mechanics.

## How the experiment works

The Base stage runs once and records boundary tensors at every candidate route, step, and stream. Each tensor is sealed with its prompt, seed, shape, route, timestep, and checkpoint identity. The repair stage loads the distilled checkpoint once, reads the immutable Base tensors, fits a small Act at each candidate seam on the discovery cells, and chooses the site, timestep, and stream hierarchically rather than searching all combinations after looking at held-out outputs.

For each held-out branch, the recipient begins from the same distilled source checkpoint. The selected Act is applied at the chosen boundary, then the native suffix continues normally. Zero-dose, sign-flipped, wrong-site, and norm-matched sham branches test whether a count improvement is specific to the learned payload rather than generic image movement. The parent checkpoint is replayed after every branch so exact rollback is independently observable.

## Results

The bisection selected `joint.2 → step 0 → text`. The discovery scores favored `joint.2` at `0.500`, step 0 at `0.606`, and the text stream at `0.738` versus `0.475` for the image stream. These are selection scores, not universal route importance estimates.

| held-out prompt and seed | expected count | repaired count | exact |
|---|---:|---:|---|
| four red squares, `31337` | 4 | 4 | yes |
| four red squares, `31339` | 4 | 3 | no |
| six blue circles, `31337` | 6 | 5 | no |
| six blue circles, `31339` | 6 | 4 | no |

The selected repair therefore achieved `1/4` exact held-out cells. It reproduced the sealed discovery evaluator on three of four discovery cells. The repair process used one distilled model load, native scheduler and VAE execution, and exact scalar site replacement. The suffix checkpoint replay has RGB MAD `0.0` against the unreplayed suffix, proving that the intervention machinery itself is deterministic under the declared contract.

The failed blue-circle generalization is scientifically informative. Some sham and sign branches also satisfy the component-count evaluator on individual seeds, so a count-only gate is insufficient to claim a semantic repair. The result points to an object-family-dependent mismatch or an underpowered evaluator rather than an absent route.

![Held-out repaired red-square output](../artifacts/klein-seam-bisection/red_squares_4__seed-31337.png)

![Held-out repaired blue-circle output](../artifacts/klein-seam-bisection/blue_circles_6__seed-31337.png)

## Interpretation

The observation is that a compact, recipient-local intervention can be selected from a sealed Base future and executed by the distilled recipient at a reproducible early seam. The trend is that the Base-to-distilled difference is not uniformly distributed: the discovery panel identifies a strong early text-stream candidate. The held-out result does not support a general Base-to-distilled capability compiler because the same Act fails on the fresh blue-circle family.

The most useful working inference is that distillation removed or weakened a family-conditioned carrier path whose repair requires more than one rank-8 coordinate-local Act. A multi-coordinate, geometry-aware evaluator is the next discriminating experiment. The current evidence does not distinguish a true family-specific carrier mismatch from a count-evaluator loophole.

## Claim boundary

Established: Base capture and distilled repair can be separated into independently auditable stages; a 32-cell seam search can select a reproducible early candidate; and the selected Act changes the distilled output through the native recipient execution.

Not established: universal Base-to-distilled recovery, donor-free training, semantic ownership of `joint.2`, generalization beyond the declared red-square/blue-circle panel, or a claim that the failure is caused by distillation rather than prompt-family and evaluator limitations.

## Local proof bundle

- [Bundle README](../artifacts/klein-seam-bisection/README.md)
- [Base capture report](../artifacts/klein-seam-bisection/base-capture-report.json)
- [Distilled repair report](../artifacts/klein-seam-bisection/distilled-repair-report.json)
- [Base capture receipt](../artifacts/klein-seam-bisection/base-capture-receipt.json)
- [Distilled repair receipt](../artifacts/klein-seam-bisection/distilled-repair-receipt.json)
- [Artifact verifier](../artifacts/klein-seam-bisection/verify.py)
