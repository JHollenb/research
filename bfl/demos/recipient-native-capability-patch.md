---
title: "Recipient-Native Capability Patch for a Distilled FLUX.2 Klein Model"
type: experiment-report
status: bounded-developmental-result
rank_in_bfl_survey: 1
model: "FLUX.2 Klein 4B"
model_id: "black-forest-labs/FLUX.2-klein-4B"
revision: "e7b7dc27f91deacad38e78976d1f2b499d76a294"
comparison_model_id: "black-forest-labs/FLUX.2-klein-base-4B"
comparison_revision: "a3b4f4849157f664bdbc776fd7453c2783562f4d"
checkpoint_role: "distilled recipient; matched against full-capacity base"
tags: [bfl, flux, distilled-models, capability-repair, causal-intervention, image-counting]
---

# Recipient-Native Capability Patch for a Distilled FLUX.2 Klein Model

> [!summary]
> A matched full-capacity/distilled comparison exposed a counting regression in the four-step FLUX.2 Klein model. A frozen recipient-local rank-8 patch, applied at one route and one early denoising step with dose 2, changed the rendered result from three red apples to five. The package is 55,297 FP16 parameters and 104,044 bytes, contains no donor payload or prompt table, and served correctly in a fresh process with the donor path unavailable. The result is a real, tightly controlled repair trend, not a shippable general-purpose hotfix: the later held-out gate found transfer across paraphrases, resolutions, and object families, but excessive collateral on ordinary prompts.

## Research question

Can a capability present in a full-capacity diffusion model but weakened by step distillation be
repaired after distillation, without retraining the recipient and without shipping the full model
that supplied the diagnostic signal?

The target capability is deliberately narrow and measurable: render exactly five separate red
apples in one horizontal row. The test is useful because object counting is visible in pixels,
independently scorable, and sensitive to both under-counting and accidental visual changes.

The experiment has four distinct questions:

1. Is there a reproducible base-versus-distilled gap under the same prompt, seed, resolution,
   scheduler, and VAE?
2. Is the gap localized to a route/time neighborhood where a recipient-local write can affect the
   native downstream image computation?
3. Does a small packaged write improve the target while wrong-time, zero-dose, uninstall, and
   wrong-source controls remain inactive or distinct?
4. Does the package actually serve without the model used to construct its payload?

## Specimens and task

The full-capacity comparison specimen is `black-forest-labs/FLUX.2-klein-base-4B` at revision
`a3b4f4849157f664bdbc776fd7453c2783562f4d` (50 steps, guidance 4). The frozen recipient and
patch target is `black-forest-labs/FLUX.2-klein-4B` at revision
`e7b7dc27f91deacad38e78976d1f2b499d76a294` (four steps, guidance 1). The patch package is bound
to the latter recipient revision; the base checkpoint supplies the diagnostic comparison, not a
runtime donor payload.

The matched specimens are:

| Property | Full-capacity specimen | Distilled specimen |
|---|---|---|
| Model family | FLUX.2 Klein 4B | FLUX.2 Klein 4B, step-distilled |
| Denoising schedule | 50 steps | 4 steps |
| Guidance | CFG 4 | guidance 1 |
| Resolution | 512 × 512 | 512 × 512 |
| VAE and scheduler | native, unchanged | native, unchanged |
| Weights during repair | reference only | frozen recipient |

The canonical prompt is:

> A clean flat illustration on a pure white background showing exactly five separate red apples arranged in a single horizontal row with equal spacing. No other objects, fruit, marks, or text.

The gap screen contains eight paired red-apple prompt/seed cells. A connected-component evaluator counts red objects in RGB pixels. An independent geometry evaluator also reports expected count, observed count, and absolute error. The two evaluators are kept separate because an earlier wording screen showed that a geometry scorer can be falsely satisfied by a prompt-specific visual pattern.

## Method

### 1. Establish the behavioral gap

Both models receive the same prompt, latent seed, resolution, scheduler, and VAE. The full-capacity model is the reference for the missing behavior; the distilled model is the recipient to be
repaired. The diagnostic records final images and compares intermediate route state at four named locations: `joint.2`, `joint.3`, `joint.4`, and `single.0`.

Across eight red-apple cells, the full-capacity model is exact under the independent evaluator in
all cells. The distilled model is exact in 4/8 cells under that evaluator and 5/8 under the second
evaluator. The corresponding exact-rate means are:

| Evaluator | Full-capacity | Distilled | Gap |
|---|---:|---:|---:|
| Independent connected components | 1.000 | 0.500 | 0.500 |
| Geometry evaluator | 1.000 | 0.625 | 0.375 |

The internal route-state comparison also separates the trajectories: the route cosine falls from
approximately 0.923 at the earliest compared location to 0.818 by the later location. This is a
localization clue, not a claim that one block is the unique source of counting.

### 2. Compile a recipient-local write

The patch is a low-rank write with this numerical contract:

```text
operation: flux.route.low_rank_write v1
site:      joint.2
stream:    text
step:      0
rank:      8
reads:     route_state, compiled_delta, dose
writes:    route_state_out
payload:   55,297 FP16 parameters
```

The full-capacity specimen supplies a state difference during compilation and diagnosis. The
serving package itself contains no donor logits, no donor activation tensor, no prompt lookup
table, and no runtime labels. At serving time, the recipient reads its own route state and the
package applies a scaled local write.

### 3. Search dose through the real image consumer

The intervention is not accepted on an internal similarity score. Each candidate is run through
the recipient's unchanged denoising continuation, scheduler, VAE, and final image evaluators.
The dose search is non-monotonic:

| Dose | Observed red-apple count |
|---:|---:|
| 0.25 | 3 |
| 0.50 | 3 |
| 1.00 | 3 |
| 2.00 | 5 |
| 4.00 | 3 |

The useful interval is therefore a consumer-calibrated window, not “more patch is better.” Dose 2
is promoted; dose 4 is rejected and the prior state is restored exactly.

## Results

The selected target cell changes from the distilled native count of 3 to 5. The full control panel
is:

| Branch | Result |
|---|---|
| Full-capacity reference | 5 apples |
| Distilled native | 3 apples |
| Distilled + selected patch | 5 apples |
| Distilled + patch at wrong route time | 3 apples |
| Distilled + zero-dose patch | 3 apples |
| Distilled + uninstall/zero-dose output | byte-exact native output |
| Separate preservation prompt | native and patched branches both count 5 |
| Fresh process, donor path unavailable | 5 apples |

The target branch is exact under both image evaluators. The selected package hash is
`f4c49f07a4a19ec689528274822c3585686f00f8b33bff9ca1ca2b91c62d4e83`. The package is 104,044 bytes and has 55,297 trainable values, so the repair is small relative to the frozen image model.

![Native distilled target: three apples](../artifacts/recipient-native-capability-patch/target-native.png)

![Patched target: five apples](../artifacts/recipient-native-capability-patch/target-act.png)

![Wrong-time control](../artifacts/recipient-native-capability-patch/target-wrong-time.png)

![Fresh donor-free output](../artifacts/recipient-native-capability-patch/fresh-donor-free.png)

## Independent serving boundary

The fresh-process test is important. It starts a new recipient-only process, intentionally points
the donor path at an unavailable location, and then renders the target. The process returns
successfully, records that the donor path is unavailable, and still obtains an exact count of five.
This rules out a serving implementation that silently reloads or consults the full-capacity model.

It does not prove that the package is portable to other recipient revisions. The package binds to
the tested FLUX.2 Klein 4B revision and to the declared route, stream, step, and numerical ABI.

## Later generalization and safety gate

The later sealed gate expands the test beyond the discovery cell:

- six paraphrases and three held-out seeds;
- 256, 512, and 1024 pixel resolutions;
- three untrained object families;
- dual-evaluator agreement;
- six of six fresh donor-free serving cells.

Exact-count performance improves from 37% to 72% on the expanded panel, and the 1024-pixel panel gains 33 percentage points. That is meaningful transfer evidence. It is not sufficient for release, because the collateral gate fails: the binary detector fires on 58/120 ordinary prompts, about 48%, with p95 RGB-MAD 41.5 against a threshold of 6.0. A post-mortem finds that the detector tracks rendering style more strongly than object multiplicity: score-versus-style correlation is 0.928, while score-versus-object-multiplicity correlation is 0.029. The training negatives therefore do not support a one-dimensional abstention threshold.

The correct interpretation is: the patch repairs the declared capability and transfers beyond
the original specimen, but the current patch-plus-detector pair is unsafe as a general hotfix.
Style-balanced negatives and a two-feature abstention rule are required before a shipping claim.

## Working inference and claim boundary

**Observation:** a matched distillation gap exists, a small route/time/dose-specific write changes
the recipient's final object count, and the result survives a donor-free fresh process.

**Convergent trend:** the useful write is causal and consumer-closed rather than merely correlated
with an internal activation; wrong time and zero dose remove the effect, and dose 4 is worse than dose 2.

**Working inference:** some distillation regressions can be compensated by recipient-local writes
when the write is calibrated against the recipient's native image consumer.

**Terminal status:** bounded developmental repair trend. The package is not a general counting
module, not a universal capability compiler, and not approved for deployment because the collateral gate fails.

This is nevertheless a clean existence proof for a very small recipient-local repair: 55,297 FP16
values, no donor payload at serving time, successful fresh-process execution with the donor path
unavailable, and exact uninstall/zero-dose behavior. Its portability boundary is explicit. The
package is compiled for the declared distilled recipient revision, route, stream, step, and
numerical ABI; the matched base checkpoint diagnoses the gap but does not make the package a
cross-checkpoint artifact. The held-out collateral failure is part of the result and is why this
remains supporting evidence rather than a deployment claim.

Open axes are paraphrase robustness beyond the tested panel, broader count ranges, unrelated
compositions, more recipient revisions, and a transferable abstention boundary.

## Local proof bundle

All evidence needed to audit this report is in
[the local artifact bundle](../artifacts/recipient-native-capability-patch/):

- [gap report](../artifacts/recipient-native-capability-patch/gap-report.json)
- [patch report](../artifacts/recipient-native-capability-patch/patch-report.json)
- [FP16 patch package](../artifacts/recipient-native-capability-patch/act-package.npz)
- [dose-search image](../artifacts/recipient-native-capability-patch/dose-2-grid.png)
- [later generalization gate](../artifacts/recipient-native-capability-patch/generalization-gate-results.md)
- [receipt verifier](../artifacts/recipient-native-capability-patch/verify.py)

Run `python ../artifacts/recipient-native-capability-patch/verify.py` from this directory to check the package hash and the reported evaluator/control facts.
