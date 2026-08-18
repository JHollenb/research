---
title: "Blocks, Routes, and the Selector: Replaying a FLUX Capability Through Saturn"
subtitle: "What the image organism actually showed, where our first interpretation went wrong, and the native-state selector test"
author: codex
type: blog
subtype: saturn-experiment-report
date: 2026-08-15
updated: 2026-08-16
status: exploratory-evidence-report
claim_status: convergent-trend-with-open-meta-router
epistemic_status: recipient-native-image-closed-with-held-out-route-policy-followup
tags:
  - saturn
  - flux
  - future-forest
  - route-selection
  - capability-formation
related:
  - 2026-08-15-bfl-failure-replay-saturn.md
  - 2026-08-15-bfl-new-top-20-saturn-upgrades.md
source_docs:
  - ../../saturn/experiments/2026-08-14-flux-capability-patch-red-apples/RESULTS.md
  - ../../saturn/experiments/2026-08-15-flux-block-future-replay/config.json
  - ../../saturn/experiments/2026-08-15-flux-block-future-replay/README.md
  - ../../saturn/results/flux-block-future-replay/job-620af5702f8c/ANALYSIS.md
  - ../../saturn/experiments/2026-08-14-flux-capability-patch-red-apples/README.md
  - ../../saturn/experiments/2026-08-15-flux-native-state-route-selector/README.md
  - ../../saturn/results/flux-native-state-route-selector/job-287fcc52b40f/ANALYSIS.md
  - ../../saturn/experiments/2026-08-15-flux-native-state-route-selector-v2/README.md
  - ../../saturn/results/flux-native-state-route-selector-v2/job-e9398856f6ec/ANALYSIS.md
  - ../../saturn/experiments/2026-08-15-flux-native-state-route-selector-v3/README.md
  - ../../saturn/experiments/2026-08-15-flux-native-state-route-selector-v3/config.json
  - ../../saturn/experiments/2026-08-15-flux-native-state-route-selector-v3/submit.py
  - ../../saturn/results/flux-native-state-route-selector-v3/job-a7556c2507cc/ANALYSIS.md
  - ../../saturn/results/flux-native-state-route-selector-v3/job-a7556c2507cc/run-receipt.json
  - ../../saturn/experiments/2026-08-15-flux-native-state-route-selector-v4/README.md
  - ../../saturn/experiments/2026-08-15-flux-native-state-route-selector-v4/config.json
  - ../../saturn/experiments/2026-08-15-flux-native-state-route-selector-v4/submit.py
  - ../../saturn/experiments/2026-08-15-flux-native-state-route-selector-v4/native_state_selector_v4.py
  - ../../saturn/experiments/2026-08-15-flux-native-state-route-selector-v4/analyze_v4.py
  - ../../saturn/results/flux-native-state-route-selector-v4/job-ecd0bdafb10e/ANALYSIS.md
  - ../../saturn/results/flux-native-state-route-selector-v4/job-ecd0bdafb10e/report.json
  - ../../saturn/results/flux-native-state-route-selector-v4/job-ecd0bdafb10e/run-receipt.json
  - ../../saturn/results/flux-native-state-route-selector-v4/job-2ff0ab4a93b9/run-receipt.json
  - ../../saturn/experiments/2026-08-15-flux-native-state-route-selector-v5/README.md
  - ../../saturn/experiments/2026-08-15-flux-native-state-route-selector-v5/config.json
  - ../../saturn/experiments/2026-08-15-flux-native-state-route-selector-v5/submit.py
  - ../../saturn/experiments/2026-08-15-flux-native-state-route-selector-v5/native_state_selector_v5.py
  - ../../saturn/experiments/2026-08-15-flux-native-state-route-selector-v5/analyze_v5.py
  - ../../saturn/results/flux-native-state-route-selector-v5/job-20d8fd4402fc/ANALYSIS.md
  - ../../saturn/results/flux-native-state-route-selector-v5/job-20d8fd4402fc/report.json
  - ../../saturn/results/flux-native-state-route-selector-v5/job-20d8fd4402fc/run-receipt.json
  - ../../saturn/results/flux-native-state-route-selector-v5/job-20d8fd4402fc/selector-package.npz
  - ../../saturn/experiments/2026-08-16-flux-native-state-route-selector-v6/README.md
  - ../../saturn/results/flux-native-state-route-selector-v6/job-32de47a11821/ANALYSIS.md
  - ../../saturn/results/flux-native-state-route-selector-v6/job-32de47a11821/report.json
  - ../../saturn/results/flux-native-state-route-selector-v6/job-32de47a11821/run-receipt.json
---

# Blocks, routes, and the selector

We started with a useful suspicion: a model's coding capability may not live in one
isolated “coding block.” It may be carried by a distributed route through the model, while a
separate control-plane capability decides when and where to use that route. A diffusion model is
a good organism for testing this because the final RGB image is an observable native consumer. If
we cannot see the effect in the image after the model's own scheduler, denoiser, and VAE have run,
we have not established an image capability.

This report is about what the Saturn replay actually supports. It is intentionally written as a
research log, not as a victory lap. The useful result is not that we found a magical block. The
useful result is that Saturn let us separate a reusable recipient-native payload, the route that
carried it, the timing and dose that made it effective, and the orchestration question that still
needs its own test.

## The short version

The red-apple Act moved a positive counting family toward its requested image while preserving a
negative three-apple family. The effect survived fresh-process execution and same-parent replay.
The payload worked at more than one early `joint` site, was weaker at `joint.4`, and was least
useful at `single.0`. That is evidence for a distributed early route coalition, not a unique
semantic block.

The Saturn future-forest replay made the distinction concrete. We created twelve immutable
prompt/seed parent cuts, retained native, route, dose, timing, sign, random, and zero futures, and
selected `joint.3` at gain `2.0` from development image outcomes. That fixed policy reached the
held-out panel without seeing held-out outcomes: positive mean count error went from `0.500` for
native to `0.000` for the selected policy, while the negative family stayed at `0.000` error.
However, `joint.2` and `joint.4` controls also reached `0.000` held-out positive error. The
held-out result therefore supports route-policy usefulness and coalition membership, not unique
block identity.

The full arc matters more than any single number. The red-apples patch established a recipient-
native image repair organism. The route/dose replay established that the repair lives on a timed,
dosed route coalition. v1 then showed that a native-state hook could dispatch a route, but only as
a constant held-out choice. v2 made the development assay less underdetermined and found varied
route labels without downstream gain. v3 returned to the one visible v2 miss and compiled a
smaller repair gate that fixed it in the final RGB consumer. Each stage narrowed a different
failure mode; none should be read as a replacement for the others.

The exact Saturn mechanics also held: `108` logical futures, one resident recipient model, exact
native rewinds for `12/12` parents, exact one-step suffix replays, reopened Future Forest closure,
and `105/108` atlas/independent evaluator agreement. The three evaluator disagreements were small
red-component threshold splits in one negative red-apple seed, not route failures.

The remaining question is the one we had been calling a meta-capability too early: can the model's
earlier native state select the route, without a development utility being handed the answer? That
is the follow-up below. The selector is compiled from native state at `joint.1`; its held-out
dispatch is then tested through the same Future Forest protocol.

The clean v4 follow-up answered a narrower version of that question: the native state generalized
the route preference from red development families to blue held-out families, but it did not
generalize the per-parent repair utility. It selected `joint4_gain2` for every blue-circle seed,
including native successes and a case where `joint4` was harmful. The explicit abstain action never
fired. That is a useful negative result about calibration and a positive trend about family-level
state structure.

The v5 Saturn debug replay then rewound that failure, added the missing `joint3_gain2` candidate,
and put a support-aware gate in front of all non-native routes. Every blue serving state was outside
the frozen red development support, so the selector abstained `9/9` times and exactly matched
native continuation. This removed the v4 collateral but deliberately left route utility unresolved:
v5 demonstrates a useful fail-closed uncertainty signal, not an autonomous meta-router.

## The experimental arc at a glance

| Stage | What changed | Result | What it established |
|---|---|---|---|
| Recipient-native patch | A small Act repaired the named red-apple image property through the native FLUX suffix | Fresh donor-free and exact-uninstall trend; wording sensitivity remained | A payload can be useful to the recipient without copying a donor model |
| Route/dose Future Forest, `job-620af5702f8c` | Same Act across `joint.2`, `joint.3`, `joint.4`, `single.0`, gains, timing, sign, random, and zero controls | Development selected `joint3_gain2`; held-out positive error `0.500→0.000`, negative error stayed `0.000`; `joint2`/`joint4` also worked | A distributed, timed route coalition and a usable fixed policy—not a unique block |
| Native selector v1, `job-287fcc52b40f` | Earlier native `joint.1` state selected among five route actions | `joint4_gain2` on `6/6` held-out parents; zero-state chose native | Native-state dispatch mechanics and route correlation; not state-dependent orchestration |
| Balanced selector v2, `job-e9398856f6ec` | More families, class-balanced ridge, constant baseline, leave-family-out diagnostics | Fit `11/14` vs `10/14` constant native; route labels varied, but count outcomes matched native | Route diversity and useful control are different measurements |
| Repair-gated selector v3, `job-a7556c2507cc` | Binary `native`/`joint4_gain2` gate, targeted blue-circle development task, three seeds | One held-out native miss went `3/5→5/5`; selector `6/6` positive and `3/3` negative exact vs native `5/6` and `3/3` | First bounded native-state repair trend closed at the final RGB image |
| Clean split selector v4, `job-ecd0bdafb10e` | Red-family development, blue-family held-out, disjoint seeds, explicit abstain, fixed repair/native controls | Selector chose `joint4` on all blue-circle positives; RGB `4/6` positive exact and atlas `3/6`, below native `5/6` and fixed `joint3` `6/6`; no abstentions | Native state generalized a family preference, not a calibrated per-parent repair gate |
| Support-aware selector v5, `job-20d8fd4402fc` | Replayed v4 with `joint3` added, standardized native-state support gate, explicit abstention telemetry, and portable policy package | All `9/9` blue serving states were out of support; selector abstained and matched native (`5/6` positive, `3/3` negative); fixed `joint3` remained `6/6` | Support-aware fail-closed control is mechanically useful; route utility and meta-routing remain unproven |

The table is a chronology, not a pooled benchmark. The denominators, prompts, action sets, and
development policies differ. Raw reports remain the authority for each row.

## What we did, step by step

The experiment kept the causal chain explicit:

`earlier native state → route decision → typed Act write → native denoiser/scheduler/VAE → RGB image`.

For each prompt and seed, Saturn captured a step-zero checkpoint before branching. Every candidate
then resumed from that same parent. The candidate panel included:

- native continuation;
- the same recipient-native Act at `joint.2`, `joint.3`, `joint.4`, and `single.0`;
- gain `1`, `2`, and `3` at the leading site;
- wrong time, sign-flipped, random, and zero-dose controls.

The development panel contained canonical red apples, seven blue circles, and a negative
three-red-apple prompt. The held-out panel used a red-apple paraphrase, five blue circles, and a
negative three-blue-circle prompt. Selection happened from development rows only. The selected
route was promoted in Saturn, then the forest was rewound to the root before held-out replay.

This is why the test is more informative than looking at a before/after PNG. A good-looking image
can be a proxy, a prompt artifact, or an evaluator mistake. Here the final image is still the
consumer, but the image is attached to a parent checkpoint, a route address, an Act payload, an
intervention dose, a Future Forest node, and a held-out decision.

## The mistakes we made

### 1. We treated the first working address as the block

The initial successful patch was at `joint.2`. It was tempting to say “the capability is in
`joint.2`.” Localization immediately made that too strong: `joint.3` also worked, `joint.4` had a
weaker effect, and `single.0` behaved differently. A payload that transfers across adjacent
addresses is more consistent with a distributed route or coalition than with one privileged
neuron-sized block.

The correction is to target candidate routes, not just blocks: test multiple sites, preserve the
same parent, keep the payload fixed where possible, and report the route/time/dose surface.

### 2. We let an incomplete instrument look like a negative result

The first confirmation report had null structured Image Atlas fields because it predated the
atlas evaluator adapter fix. That was an instrumentation problem, not evidence that the rendered
effect was absent. The corrected localization and replay used both the independent RGB evaluator
and the structured atlas, and retained the disagreements rather than silently choosing the more
convenient score.

The correction is to treat evaluators as instruments: version them, inspect their schemas, compare
independent measurements, and diagnose threshold splits before making a scientific claim.

### 3. We confused image movement with coding capability

An image can change because of color, texture, layout, or collateral damage. A successful route
write alone does not prove that the model recovered a count operation. The replay therefore kept
negative prompts, no-op and zero-dose branches, wrong time, wrong site, sign flip, random payload,
and dose controls. These do not prove semantic ownership, but they narrow the live explanations.

The correction is to call the current result an image-space, consumer-closed trend. It is stronger
than a carrier correlation and weaker than a general semantic compiler.

### 4. We called an explicit development utility a meta-capability

The first policy experiment selected `joint.3` by inspecting downstream development image scores.
That is a valid controller experiment, but it is not yet a model-native meta-router. The utility
was supplied by the experimenter; the model did not have to infer a route from its own earlier
state.

The correction was to compile a small selector from earlier native `joint.1` state, freeze it,
and dispatch on held-out prompts before looking at their final images. The development image score
could compile the selector, but it was not available to serving-time dispatch or held-out
selection. The resulting controller was mechanically valid but collapsed to one held-out route,
which is why the meta-capability claim remains open.

### 5. We underused Saturn's ability to rewind and retain rejected futures

Without Future Forest custody, “we tried several routes” is only a list of outputs. It does not
show that the routes shared a parent or that the native trajectory was restored after exploration.
The replay retained rejected and hostile futures, recorded promotion and rewind, and checked the
native image again from the original parent.

The correction is procedural: every serious route claim should carry a parent fingerprint, a typed
transition, a downstream observation, a decision, and a same-parent rewind receipt. Rejected
futures are evidence about the mechanism, not clutter.

### 6. We initially treated dose and timing as implementation details

Gain `1` was underpowered, gain `2` was the useful region, and gain `3` lost negative-family
preservation. The wrong-time branch did not reproduce the effect. That tells us that the payload is
not just a timeless semantic label; the native consumer reads it in a particular temporal and
amplitude regime.

The correction is to make route, timestep, gain, sign, and carrier part of the Act contract and to
measure a response surface before trying to generalize.

### 7. We could have mistaken logical branching for repeated model training

The run had `108` logical branches, but it loaded one recipient model under one mrun lease and
reused one checkpoint per prompt/seed. This distinction matters. We were not doing classical blind
training; we were using Saturn as a microscope over counterfactual futures and as a reversible
controller over a frozen native consumer.

The correction is to state physical execution and logical branching separately, and to retain the
exact scheduler/VAE suffix rather than replacing it with a proxy renderer.

### 8. We omitted a dependency from the first mrun payload

The first submission failed before model loading because the new staging manifest copied
`confirm_block.py` but not its imported `patch_compile.py`. That failure says nothing about the
model or the route. It is an ordinary execution-contract bug, and it is still worth recording
because Saturn's evidence chain begins before inference.

The correction was to add the dependency and its hash to the staging/request manifest, preserve
the failed receipt as null execution evidence, and rerun under a new job identity. The corrected
job loaded the model once and completed the full panel.

### 9. We made a tiny selector look more learned than it was

The native-state selector compiled with six development parents, five possible actions, and a
label distribution of three `native`, two `joint4_gain2`, and one `joint3_gain2`. Its development
fit accuracy was `1.000`, but that is interpolation on an underdetermined panel. The honest
baseline is the majority/constant action, not the fit score.

The correction is to include constant-policy baselines in every selector assay, balance the
development families, and use leave-one-seed/family-out compilation before reading a route choice
as state-dependent. A selector that chooses the same action for every held-out parent has not
demonstrated orchestration even if the action itself is excellent. We reran this correction in v2
with fourteen development examples, inverse-label-frequency weighting, and leave-one-family-out
diagnostics. The fit became `11/14` versus `10/14` for the majority constant-native baseline, and
the held-out controller varied by family. That fixed the original interpolation problem, but the
selector's image outcome vector still matched constant native continuation, so route diversity
and useful orchestration remain separate measurements.

### 10. We adapted to a held-out miss without resetting the claim boundary

The v3 development panel was intentionally chosen after v2 exposed a blue-circle miss. That is
good debugging: Saturn let us rewind the story, target the live failure mode, and ask whether a
smaller repair gate could close it. It is not a blind confirmation. The blue-circle family is in
both development and held-out panels, and the seed values overlap even though the task/seed
combinations are distinct.

The correction is to name v3 accurately: an adaptive, outcome-blind-at-dispatch repair experiment.
The next confirmation must hide the target family, use seed-disjoint development and test sets,
and be frozen before inspecting new held-out images. We preserve v3 because an adaptive debugging
result is still valuable evidence about mechanism and instrument behavior.

### 11. We mistook family routing for per-instance repair

The clean v4 split did what v3 could not: development used red families and seeds `611`, `6172`,
and `2718`, while held-out serving used blue families and seeds `3141`, `1618`, and `4242`. The
split checks leakage, but the selector chose `joint4_gain2` for all three blue-circle positives.
That was a family preference, not a decision about whether each individual parent needed repair:
one blue-circle parent already succeeded natively, one remained a miss after `joint4`, and one was
made worse by it. Fixed `joint3` repaired all three on both instruments.

The correction is to make the utility disagreement per-parent and to calibrate uncertainty on a
separate calibration organism. A selector must earn the right to intervene on a particular native
state, not merely recognize the broad prompt family.

### 12. We added abstention as an action without evidence that the margin was calibrated

v4 included an explicit native-continuation `abstain` action with a predeclared `0.10` top-two
route-logit margin. It never fired: the blue-circle route margins were confidently above that
threshold even when the route was wrong. This is not evidence that abstention is useless; it is
evidence that an uncalibrated margin is not a safety gate.

The correction is to reserve a calibration split for abstention, report coverage versus repair
precision, and include an oracle/constant-abstain comparison. The threshold must be frozen before
the final held-out family, and the calibration objective must price collateral damage on native
successes.

### 13. We let an evaluator disagreement hide inside an aggregate

The v4 run had `104/108` atlas/RGB agreements. All four disagreements were on the same two blue
circle `joint4` images: the RGB connected-component evaluator counted `5` and `2`, while the atlas
counted `2` and `1`. The aggregate selector score therefore changes from positive exact `4/6` under
RGB to `3/6` under the atlas. The disagreement is itself a finding about instrument sensitivity,
not a rounding detail.

The correction is to publish both instruments, list every disagreement, and require convergence or
an adjudicated evaluator before any terminal claim. If the mechanism is important, the next image
organism should use a renderer/evaluator with instance identity and anti-aliasing robustness.

## Findings, with the claim boundary kept visible

**Observation.** The recipient-native Act changes the final FLUX image at step zero. The same
payload is effective at `joint.2` and `joint.3`, weaker at `joint.4`, and less useful at `single.0`.

**Trend.** Positive counting prompts improve while the negative three-count family is mostly
preserved. The route has a dose and timing window; wrong time, sign, random, and zero controls do
not behave like the selected Act.

**Convergent trend.** Independent image scoring, structured atlas scoring, multiple sites, two
seeds, fresh-process package loading, and exact replay all point to a real recipient-native,
distributed route effect. The alternate route controls prevent us from naming a unique block.

**Working inference.** The current FLUX organism contains an early joint-stream route coalition
that can carry a reusable payload into a native consumer. A second capability—route orchestration—
may read earlier native state and select among those carriers. The evidence supports testing that
architecture; it does not yet establish that the selector is learned, semantic, or universal.

**Terminal claim.** We have not earned a terminal claim about a general coding capability, a
unique semantic block, or a universal meta-capability. We have earned a bounded image-closed trend
and a precise next experiment.

## The native-state selector result

The follow-up was executed as [the native-state route-selector experiment](../../saturn/experiments/2026-08-15-flux-native-state-route-selector/README.md)
in mrun job `job-287fcc52b40f`. It used the same model revision, Act package, task splits, seeds,
native suffix, and Future Forest discipline. The selector source was `joint.1`, text stream, step
zero. Its feature was a 64-dimensional mean/std pooled native-state summary. The package was
promoted, rewound, and then dispatched on held-out prompts without exposing held-out outcomes.

The mechanical closure is strong: `84` logical branches, `12` parent cuts, one resident model,
`6/6` raw native-feature matches between selector and native captures, exact native rewind for
all parents, exact step-observer suffix replay, reopened Future Forest closure, and `82/84`
atlas/independent evaluator agreement. The two evaluator disagreements were threshold-level image
instrument splits, not selector hook failures.

The controller result is more modest:

| Held-out branch | Positive mean error | Positive exact | Negative mean error | Negative exact | Dispatch |
|---|---:|---:|---:|---:|---|
| native | `0.500` | `0.750` | `0.000` | `1.000` | — |
| selector dispatch | `0.000` | `1.000` | `0.000` | `1.000` | `joint4_gain2` on `6/6` |
| fixed `joint.4` | `0.000` | `1.000` | `0.000` | `1.000` | fixed |
| selector zero-state | `0.500` | `0.750` | `0.000` | `1.000` | `native` on `6/6` |
| selector inverted | `0.500` | `0.750` | `0.000` | `1.000` | mostly `joint3_gain2`/native |

This is a useful debugging result. The nonzero native feature changes the controller relative to
the zero-information input, so the selector hook is not dead code. But the selector collapses to a
constant held-out action, and the fixed `joint.4` control gets the same image result. The experiment
therefore establishes native-state-conditioned dispatch mechanics and a strong `joint.4` route
trend; it does not establish that the state carries a semantic route key or that a meta-capability
orchestrated the choice.

The v2 assay below enlarged and balanced the development organism and retained the same Future
Forest and final-image closure. The next improvement should add independent held-out families and
an action set whose route utilities are not already tied, so a selector can be rewarded for
choosing the right carrier rather than merely changing the label. This is the productive boundary
Saturn exposed: the payload is image-effective, while the orchestration signal is a candidate
mechanism with a visible native-state trend but no downstream gain yet.

## The balanced native-state selector rerun

We then ran [the v2 native-state route-selector experiment](../../saturn/experiments/2026-08-15-flux-native-state-route-selector-v2/README.md)
in mrun job `job-e9398856f6ec`. It kept the exact v1 held-out Future Forest panel and final RGB
consumer, but expanded development to seven tasks and fourteen parent/seed examples. The selector
used a 32-dimensional pooled feature from earlier native `joint.1` text state, a class-balanced
ridge fit, an explicit majority constant policy, and leave-one-family-out diagnostics. The serving
package still received only the earlier native state; development image outcomes were sealed
before held-out dispatch.

The Saturn mechanics remained closed: `124/124` logical branches, `20` immutable parent cuts,
one resident recipient model, exact native rewind and suffix replay, reopened Future Forest
closure, `6/6` held-out raw-feature matches, and `121/124` atlas/independent image agreement. The
three disagreements were threshold-level evaluator splits, not missing selector captures. The
worker completed in `652.94` seconds (`665.58` seconds in the mrun result), with peak RSS about
`20.4 GB` and peak VRAM about `8.3 GB`.

The compiler was no longer a six-parent interpolation: it fit `11/14` development labels versus
`10/14` for the majority constant `native` baseline. The label distribution was `10 native`, `2
joint4_gain2`, `1 joint3_gain2`, and `1 single0_gain2`. Leave-one-family-out accuracy was `0.000`
for negative red apples and positive blue circles, `0.500` for positive red apples, and `1.000`
for negative red squares and positive red squares. That pattern is a useful map of where the
controller is family-dependent.

On held-out parents the selector chose `single0_gain2` for both red-apple paraphrases and `native`
for both blue-circle parents and both negative parents. The final images make the behavior
concrete: the selected apple output has all five requested apples, while one selected blue-circle
output has only three of five and the other has all five. The negative outputs preserve three of
three. Overall selector dispatch was `0.500` positive mean count error / `0.750` positive exact
rate, with `0.000` negative error. Most importantly, its complete observed-count vector was
identical to constant native continuation; fixed `joint.2`, `joint.3`, and `joint.4` controls each
reached `0.000` positive error on this small held-out panel.

This is a stronger and more interesting result than the v1 constant dispatch, but its meaning is
precise: earlier native state did change the route choice in a family-structured way, and the
choice was made without held-out outcome access. The choice did not yet improve the native image
consumer over the constant-native policy, and the leave-family-out failures show that the routing
rule is not stable across families. We should treat v2 as a convergent trend toward a native-state
route signal, not as proof of a useful meta-capability. The next test should create held-out route
utility differences that the selector must resolve, then compare it against constant policies on
new families and seeds.

Representative RGB artifacts are [the selected apple](../../saturn/results/flux-native-state-route-selector-v2/job-e9398856f6ec/heldout__red_apples_paraphrase__seed-611__selector_dispatch.png),
[the missed blue-circle case](../../saturn/results/flux-native-state-route-selector-v2/job-e9398856f6ec/heldout__blue_circles_five__seed-611__selector_dispatch.png),
and [the exact blue-circle case](../../saturn/results/flux-native-state-route-selector-v2/job-e9398856f6ec/heldout__blue_circles_five__seed-6172__selector_dispatch.png).

## The repair-gated native-state selector rerun

The v2 result gave us a concrete debugging target instead of a vague claim: one held-out
five-blue-circle native branch missed two circles, while fixed `joint.3` and `joint.4` routes
repaired it. We therefore ran [the v3 repair-gated experiment](../../saturn/experiments/2026-08-15-flux-native-state-route-selector-v3/README.md)
in mrun job `job-a7556c2507cc`. It compiled a smaller binary choice—`native` versus
`joint4_gain2`—from earlier native `joint.1` state, added a targeted blue-circle development
task, used three seeds, and sealed the held-out outcomes before dispatch.

The execution contract held: `111/111` rows, `33` immutable parent cuts, `9/9` held-out native
feature matches, exact native rewind and suffix replay, reopened Future Forest closure, and
`110/111` atlas/independent evaluator agreement. The compiler fit `21/24` development labels
(`0.875`) versus `20/24` for the constant-native baseline (`0.833`). It chose `native` on eight
held-out parent/seed cases and `joint4_gain2` on one.

That one choice is the finding. On the held-out five-blue-circle case at seed `611`, native
continuation rendered three circles, while the native-state selector dispatched `joint4_gain2`
and rendered all five. Across the held-out panel, selector dispatch reached `6/6` positive and
`3/3` negative exact counts; native reached `5/6` positive and `3/3` negative. The selector's
repair image is byte-identical to the fixed `joint4` control for that branch, which is exactly
what we would expect from a route dispatch and not evidence of a new payload. Fixed `joint3` and
fixed `joint4` also reached `6/6` positive and `3/3` negative, so the selector has not shown
that it can outperform a route chosen in advance.

This moves the result forward in a precise way. We now have a bounded, consumer-closed trend that
an earlier native feature can gate a repair route on a known failure family. The targeted design
matters: v3 was motivated by the v2 miss, and the held-out panel is only nine parent/seed
decisions. The result is therefore not a terminal claim about a universal meta-capability or a
semantic route key. The next assay should keep the binary repair gate but hide the target family
from development, add genuinely new held-out families, and require the selector to beat both
constant-native and fixed-repair policies across fresh prompts and seeds.

Representative v3 RGB artifacts are [the native three-circle miss](../../saturn/results/flux-native-state-route-selector-v3/job-a7556c2507cc/heldout__blue_circles_five__seed-611__native.png),
[the selected five-circle repair](../../saturn/results/flux-native-state-route-selector-v3/job-a7556c2507cc/heldout__blue_circles_five__seed-611__selector_dispatch.png),
and [the third-seed selected output](../../saturn/results/flux-native-state-route-selector-v3/job-a7556c2507cc/heldout__blue_circles_five__seed-2718__selector_dispatch.png).

## The clean family- and seed-disjoint confirmation

The recommended next step was to stop reusing the known blue-circle family in development. We
implemented that as [v4](../../saturn/experiments/2026-08-15-flux-native-state-route-selector-v4/README.md)
and ran it as mrun job `job-ecd0bdafb10e`. Development contained only red apples and red squares
with seeds `611`, `6172`, and `2718`. Held-out serving contained blue circles and blue squares
with seeds `3141`, `1618`, and `4242`. The worker asserts both family and seed disjointness before
opening the held-out phase.

The action set was deliberately small and interpretable:

```text
native continuation
joint4_gain2 recipient-native repair
abstain → native continuation when route-logit margin < 0.10
```

The held-out panel also retained fixed `joint3`, fixed `joint4`, native, zero-state, inverted, and
wrong-time controls. The selector compiled from the 32-dimensional native `joint.1` summary,
with development image outcomes used only to form labels. The held-out selector package was
promoted in Saturn, rewound to the root, and then served from earlier native state.

### What Saturn proved mechanically

The corrected run completed `108/108` rows across `24` immutable parent cuts (`15` development,
`9` held out) in `636.99` seconds of worker time. The earlier native feature matched the paired
native capture on `9/9` held-out decisions. Native rewind and one-step suffix replay were exact;
Future Forest closure and reopened closure were exact; held-out outcomes were hidden at dispatch.
The atlas and independent RGB instruments agreed on `104/108` rows. These are strong instrument
and custody results, but they are not themselves evidence that the selector's utility was correct.

The development compiler fit `12/15` labels (`0.800`), exactly matching the constant-native
baseline. Its labels were `12 native`, `3 joint4_gain2`, and `0 abstain`. Leave-family-out
accuracy was `0.000` for negative red apples, `1.000` for negative red squares, `0.500` for
positive red apples, and `1.000` for positive red squares. The family holdouts already warned
that the selector was learning a family-correlated surface rather than a stable instance rule.

### What the consumer showed

The selector chose `joint4_gain2` on all three blue-circle positive parents and native on all
three blue-square positives and all three negative blue-circle parents. It abstained zero times.
The per-seed blue-circle panel is the key evidence:

| Held-out seed | Native | Selector / fixed `joint4` | Fixed `joint3` |
|---:|---:|---:|---:|
| `3141` | RGB `5/5`, atlas `5/5` | RGB `5/5`, atlas `2/5` | `5/5` on both |
| `1618` | `4/5` | `4/5` | `5/5` |
| `4242` | `5/5` | RGB `2/5`, atlas `1/5` | `5/5` on both |

Across the six positive held-out rows, the selector reached `4/6` exact under the independent RGB
evaluator and `3/6` under the atlas. Native reached `5/6` under both; fixed `joint3` reached
`6/6` under both. All three negative rows were exact for every principal branch. The selector's
dispatch image was byte-identical to fixed `joint4` on the two affected seeds, confirming route
closure but also confirming that the selector inherited the route's collateral behavior.

This is not the v3 result repeated. v3 found one targeted repair. v4 shows that when the target
family is hidden and seeds are disjoint, the native state can still separate the broad blue-circle
family from blue squares and negatives—but it cannot tell which blue-circle parent needs `joint4`,
and the fixed `0.10` abstention margin is overconfident. The working inference is now sharper:

```text
native state → family-correlated route preference
                ≠ calibrated per-parent repair utility
```

That is meaningful progress. It identifies the missing capability as uncertainty-aware consumer
prediction, not merely route classification. It also prevents us from promoting the v3 trend into
a universal meta-capability claim.

### Debugging the first v4 attempt

The first sealed v4 job, `job-2ff0ab4a93b9`, completed the `45/45` development rows and failed at
the first serving hook with `KeyError: route_action_ids`. The compiler had fitted the selector but
the worker had not copied the new route/abstention metadata into the in-memory manifest. No
held-out row ran. We preserved the [failed receipt](../../saturn/results/flux-native-state-route-selector-v4/job-2ff0ab4a93b9/run-receipt.json)
with its original worker hash and log hash, patched the compiler wrapper, and reran as a new job.
The [successful receipt](../../saturn/results/flux-native-state-route-selector-v4/job-ecd0bdafb10e/run-receipt.json)
and [artifact-only analysis](../../saturn/results/flux-native-state-route-selector-v4/job-ecd0bdafb10e/ANALYSIS.md)
make that rewind explicit. This is an execution-contract failure, not a model result.

The collected selector package contains the three route actions and weights; the fixed abstention
margin is currently recorded in the config and compiled report manifest rather than in the NPZ
payload itself. That is sufficient for this exact replay, but it is a portability gap. Before
moving this controller to another organism, the package writer should serialize the route-action
allowlist, abstention threshold, calibration version, and evaluator contract into the portable
package and verify a fresh-process package-only replay.

## Replication appendix

The experiment is reproducible as a Saturn/mrun transaction, not as a prompt-only image recipe.
The native FLUX model, scheduler, VAE, recipient Act, selector package, parent checkpoints,
Future Forest, evaluator outputs, hashes, and rewind receipts all belong to the evidence chain.

### Fixed specimen and control-plane contract

The v3 specimen is `black-forest-labs/FLUX.2-klein-4B` at revision
`e7b7dc27f91deacad38e78976d1f2b499d76a294`, CUDA/bfloat16, `512×512`, four denoising steps, and
guidance `1.0`. The recipient-native payload is the previously sealed Act at `joint.2/text`,
step `0`, gain `2.0`. The selector reads only a 32-dimensional mean/std pooled summary of native
`joint.1/text`, step `0`, and fits a ridge model with `λ=1.0` and inverse-label-frequency class
balancing. Its only actions are `native` and `joint4_gain2`.

The physical and logical planes are separate:

```text
mrun: one CUDA lease, model placement, RAM/VRAM admission, telemetry
Saturn: one resident recipient, immutable parent cuts, typed route writes
selector: native-state control plane, frozen before held-out dispatch
Future Forest: candidate futures, promotion, rejection, rewind, reopen
consumer: native denoiser → scheduler → VAE → RGB image and count evaluators
```

The panel contains eight development tasks × two candidate actions × three seeds (`48` branches)
and three held-out tasks × seven controls × three seeds (`63` branches), for `111` logical rows.
There are `24` development parent/seed specimens and `9` held-out parent/seed decisions. The
held-out result is not leaked into dispatch: expected count, task label, final image, and score are
absent from the serving input. The development utility is used only to form frozen training
labels for the selector.

### Source tree and exact run path

The v3 README is the operational entry point: [experiment README](../../saturn/experiments/2026-08-15-flux-native-state-route-selector-v3/README.md),
[config](../../saturn/experiments/2026-08-15-flux-native-state-route-selector-v3/config.json),
[submitter](../../saturn/experiments/2026-08-15-flux-native-state-route-selector-v3/submit.py),
and [worker](../../saturn/experiments/2026-08-15-flux-native-state-route-selector-v3/native_state_selector_v3.py).
The v3 worker deliberately imports the v2 compiler and v1 native-state runner; the submitter
stages those dependencies, the original route/dose worker, the frozen atlas evaluator, and the
sealed [Act package](../../saturn/experiments/2026-08-14-flux-capability-patch-red-apples/results/job-b2aab6012d61/act-package.npz).
A future researcher should reproduce from this source closure rather than copying only
`native_state_selector_v3.py`.

From `/Users/jakeholl/domains`, the intended sequence is:

```bash
# 1. inspect the request; expect 111 total branches and 9 held-out decisions
rtk common/bin/common exec python \
  saturn/experiments/2026-08-15-flux-native-state-route-selector-v3/submit.py \
  --dry-run

# 2. launch one guarded mrun worker; record the printed job id
rtk common/bin/common exec python \
  saturn/experiments/2026-08-15-flux-native-state-route-selector-v3/submit.py

# 3. after the job is terminal, collect report, images, selector package, and forest archive
rtk common/bin/common exec python \
  saturn/experiments/2026-08-15-flux-native-state-route-selector-v3/submit.py \
  --collect <job-id>

# 4. analyze the collected report without loading a model
rtk common/bin/common exec python \
  saturn/experiments/2026-08-15-flux-native-state-route-selector-v2/analyze_v2.py \
  --report saturn/results/flux-native-state-route-selector-v3/<job-id>/report.json \
  --output saturn/results/flux-native-state-route-selector-v3/<job-id>/ANALYSIS.md
```

Before interpretation, verify the config/report JSON, Python compilation, package and model
hashes, `heldout_outcomes_visible_at_dispatch=false`, exact rewind and suffix replay, Future
Forest closure and reopened closure, and `9/9` raw feature matches. The two image instruments
must be compared row by row. The v3 receipt reports `110/111` atlas/independent agreements; that
one disagreement remains part of the instrument record.

The collected reference run is [job `job-a7556c2507cc` report](../../saturn/results/flux-native-state-route-selector-v3/job-a7556c2507cc/report.json),
[run receipt](../../saturn/results/flux-native-state-route-selector-v3/job-a7556c2507cc/run-receipt.json),
[artifact-only analysis](../../saturn/results/flux-native-state-route-selector-v3/job-a7556c2507cc/ANALYSIS.md),
and [Future Forest archive](../../saturn/results/flux-native-state-route-selector-v3/job-a7556c2507cc/future-forest.tar.gz).

### Expected reference output

The reference v3 run completed with `111/111` rows, `33` immutable parent cuts, one resident
recipient, peak RSS about `20.5 GB`, peak VRAM about `8.35 GB`, worker time about `748` seconds,
and mrun time about `761` seconds. Its compiler fit `21/24` development labels (`0.875`) versus
`20/24` for constant native (`0.833`). Leave-family-out accuracy was `1.000` on negative red
apples, negative red squares, and positive red squares, and `0.667` on positive blue circles and
positive red apples.

The held-out route distribution was eight `native` decisions and one `joint4_gain2` decision.
Selector dispatch reached `6/6` positive and `3/3` negative exact counts; native reached `5/6`
positive and `3/3` negative. Fixed `joint3` and fixed `joint4` each also reached `6/6` positive
and `3/3` negative. The selector's one successful repair is the blue-circle seed-611 branch:
the native image has three circles and the selected image has five. The selected image is
byte-identical to the fixed `joint4` control, which is evidence of correct route dispatch, not a
new payload discovery.

### v4 clean-split replication

The v4 source closure is [its README](../../saturn/experiments/2026-08-15-flux-native-state-route-selector-v4/README.md),
[config](../../saturn/experiments/2026-08-15-flux-native-state-route-selector-v4/config.json),
[submitter](../../saturn/experiments/2026-08-15-flux-native-state-route-selector-v4/submit.py),
[worker](../../saturn/experiments/2026-08-15-flux-native-state-route-selector-v4/native_state_selector_v4.py),
and [artifact-only analyzer](../../saturn/experiments/2026-08-15-flux-native-state-route-selector-v4/analyze_v4.py).
The model revision, Act package, resolution, steps, guidance, source address, and ridge fit remain
the same as v3. The v4-specific contract is:

| Field | Development | Held out |
|---|---|---|
| Families | red apples, red squares | blue circles, blue squares |
| Seeds | `611`, `6172`, `2718` | `3141`, `1618`, `4242` |
| Tasks | `5` | `3` |
| Parent cuts | `15` | `9` |
| Branches | `45` (`native`, `joint4`, `abstain`) | `63` (`7` controls) |
| Selector | labels from image utility | earlier native `joint.1` state only |
| Abstention | fixed margin `0.10` | native continuation |

The worker asserts family and seed disjointness. The request must show `108` total branches,
`45` development branches, `63` held-out control branches, a single resident CUDA lease, and
selector actions `native`, `joint4_gain2`, `abstain`:

```bash
rtk common/bin/common exec python \
  saturn/experiments/2026-08-15-flux-native-state-route-selector-v4/submit.py \
  --dry-run

rtk common/bin/common exec python \
  saturn/experiments/2026-08-15-flux-native-state-route-selector-v4/submit.py

rtk common/bin/common exec python \
  saturn/experiments/2026-08-15-flux-native-state-route-selector-v4/submit.py \
  --collect <job-id>

rtk common/bin/common exec python \
  saturn/experiments/2026-08-15-flux-native-state-route-selector-v4/analyze_v4.py \
  --report saturn/results/flux-native-state-route-selector-v4/<job-id>/report.json \
  --output saturn/results/flux-native-state-route-selector-v4/<job-id>/ANALYSIS.md
```

The successful reference is [v4 report](../../saturn/results/flux-native-state-route-selector-v4/job-ecd0bdafb10e/report.json),
[run receipt](../../saturn/results/flux-native-state-route-selector-v4/job-ecd0bdafb10e/run-receipt.json),
[analysis](../../saturn/results/flux-native-state-route-selector-v4/job-ecd0bdafb10e/ANALYSIS.md),
[analysis JSON](../../saturn/results/flux-native-state-route-selector-v4/job-ecd0bdafb10e/ANALYSIS.json),
[selector package](../../saturn/results/flux-native-state-route-selector-v4/job-ecd0bdafb10e/selector-package.npz),
and [Future Forest directory](../../saturn/results/flux-native-state-route-selector-v4/job-ecd0bdafb10e/future-forest/).
The preserved failed debug attempt is [job `job-2ff0ab4a93b9`](../../saturn/results/flux-native-state-route-selector-v4/job-2ff0ab4a93b9/run-receipt.json).

Before interpreting a reproduction, verify both evaluators, not only the aggregate: `108` rows,
`24` parent cuts, `9/9` raw feature matches, exact rewind and suffix replay, Future Forest
closure/reopen, `heldout_outcomes_visible_at_dispatch=false`, and the complete evaluator
disagreement table. The v4 reference agrees on `104/108` rows; the four disagreements are the
blue-circle `joint4`/selector images at seeds `3141` and `4242`.

### The evaluator disagreement has two different causes

The disagreement table is not one homogeneous failure. I replayed the frozen v4 PNGs through the
image-atlas hue mask at `160`, `256`, `384`, and `512` pixels, without loading the model. The atlas
implementation nominally downsamples to `160×160`; the independent RGB evaluator measures
full-resolution connected components.

| Image | Atlas at 160 | Same hue mask at 256/384/512 | Diagnosis |
|---|---:|---:|---|
| blue circles, seed `3141`, native | `5` | `5/5/5` | stable |
| blue circles, seed `3141`, joint4 | `2` | `5/5/5` | evaluator-resolution sensitivity |
| blue circles, seed `4242`, native | `5` | `5/5/5` | stable |
| blue circles, seed `4242`, joint4 | `1` | `1/1/3` | real route-induced merging, with scale sensitivity |
| blue circles, seed `4242`, fixed joint3 | `5` | `5/5/5` | stable repair control |

The full-resolution RGB evaluator sees five components for seed `3141` joint4, so the atlas count
of two there is an instrument artifact caused by near-touching anti-aliased circles after
downsampling. Seed `4242` is different: joint4 actually merges geometry at full resolution (the
independent evaluator sees two components), and only the largest-scale hue mask separates three
components. This preserves the substantive conclusion that joint4 can be harmful, while narrowing
the atlas disagreement claim. Saturn's rule is to retain both measurements, diagnose the
instrument, and never choose the more favorable evaluator silently.

### v5: rewind the selector, add the missing route, and fail closed

The next step was not to declare v4 a failure and move on. We used Saturn to rewind the policy
design and replay the same panel with the specific missing controls. The source closure is [the
v5 README](../../saturn/experiments/2026-08-15-flux-native-state-route-selector-v5/README.md),
[config](../../saturn/experiments/2026-08-15-flux-native-state-route-selector-v5/config.json),
[submitter](../../saturn/experiments/2026-08-15-flux-native-state-route-selector-v5/submit.py),
[worker](../../saturn/experiments/2026-08-15-flux-native-state-route-selector-v5/native_state_selector_v5.py),
and [artifact-only analyzer](../../saturn/experiments/2026-08-15-flux-native-state-route-selector-v5/analyze_v5.py).
It retains the v4 red development / blue held-out family split and seeds, so this is a debug
replay, not an independent confirmation.

The repair had two parts:

1. Add `joint3_gain2` to the compiled action set. v4 could not select the route that won its
   fixed control panel.
2. Compile a support-aware gate from the earlier native `joint.1` state. The support radius was
   predeclared as the maximum leave-one-out nearest-neighbor distance in the standardized red
   development cloud, `2.013879`. A serving state abstained if its top-route margin was below
   `0.10` or its nearest red development state was farther away.

The worker then ran `123` same-parent branches (`60` development and `63` held-out controls) under
one resident CUDA model. Development fit rose to `0.867` versus constant-native `0.733`; the
development labels were `11` native, `1` joint3, `3` joint4, and no abstentions. Saturn verified
exact rewind, exact one-step suffix replay, hidden held-out dispatch, and Future Forest closure
and reopen (`149` nodes, `172` decisions/observations, `198` content objects, no orphan content).

The support gate exposed the real distribution shift rather than pretending it was route utility:

| Held-out family | Nearest standardized distance range | Support radius | v5 action |
|---|---:|---:|---|
| blue circles, five | `5.300–5.679` | `2.014` | abstain, all `3` seeds |
| blue squares, four | `2.202–2.772` | `2.014` | abstain, all `3` seeds |
| negative blue circles, three | `7.675–8.462` | `2.014` | abstain, all `3` seeds |

Because abstention means native continuation, v5's selector images were byte-identical to native
on all nine held-out parents. Selector/native positive exactness was `5/6` under both the full
RGB evaluator and the atlas; fixed `joint3` was `6/6` under both, and all negative controls were
exact. Compared with v4, the selector action distribution changed from `6` native + `3` joint4
to `9` abstentions/native-equivalent. That is the intended safety repair: it prevented unsupported
joint4 dispatch and made uncertainty visible. It did not prove that native state can choose
joint3, nor that abstention is calibrated—the gate covered the entire blue panel.

One implementation defect is recorded rather than silently repaired in history. The collected raw
report's nested selector schema says `saturn-native-state-route-selector-v2`, although its report
schema, selector version, route IDs, support policy, and portable package are v5. The raw report
and receipt remain immutable; the [v5 analysis](../../saturn/results/flux-native-state-route-selector-v5/job-20d8fd4402fc/ANALYSIS.md)
flags this metadata mismatch, and the source was corrected for later runs. It changes no recorded
route decision or image, but it is part of the reproducibility record.

## What this means

### The likely unit is a route coalition, not a block

The same recipient-native Act works at multiple early joint sites, with strength depending on
site, timestep, dose, and sign. The carrier route is distributed and reusable; the semantic
message is the payload written into that route. “Find the coding block” is therefore probably the
wrong first question. The more useful decomposition is:

```text
source / context → address policy → payload → carrier route → writer → dose/time
→ native consumer → continuation or image
```

Saturn lets us test each term independently. A route can be real while a payload is wrong. A
payload can be useful while its donor geometry is dissimilar. A selector can vary route labels
while failing to improve the consumer. These are different capabilities.

### The selector is a candidate control plane, not yet a semantic meta-capability

v1 established that the hook worked. v2 established that native state could change choices in a
family-structured way. v3 showed one native-state-conditioned repair on a known failure family.
Together they support the working inference that earlier native state contains a route-correlated
signal. They do not identify what the signal means. It could encode a semantic need, a prompt
family, a phase/seed condition, a local denoising trajectory, or a feature correlated with all of
those.

The fixed-route controls are important: `joint4` repaired the same branch without any selector.
The selector's added value is conditional choice—choosing native on the eight cases that already
worked and repair on the one visible miss—not payload creation. That is exactly the architecture
we wanted to probe. v4 supplied the blind-family/seed split and showed the missing term: the state
can prefer a route for a family while failing to predict which parent benefits. The selector lost
to native on the clean split, fixed `joint3` won, and the abstention margin never fired. The
control-plane hypothesis remains live, but its next version must predict utility and uncertainty,
not only route identity. v5 is the first explicit uncertainty repair: all nine blue states were
outside the development support and therefore fell back to native. That is evidence that the
earlier state carries a detectable distribution-shift signal. It is not evidence that the state
knows which supported route will improve a parent, because the gate never entered its in-support
route-selection regime on this replay.

### Consumer closure changes what counts as evidence

The final RGB result is not decoration. It is the native consumer's verdict after the denoiser,
scheduler, and VAE have processed the intervention. The exact rewind and reopen receipts show that
the result came from a controlled parent-linked future rather than a separately loaded image
generation. The independent atlas disagreement also shows why one evaluator is insufficient.

This pattern generalizes beyond images. For language, the consumer should be native logits,
generated tokens, continuation, and—where relevant—an external code test that never supplies the
answer. For memory, it should be native retrieval and continuation. For training, it should be
the future checkpoint's behavior and collateral, not only loss. The consumer defines the claim.

### Future Forest is more than bookkeeping

The forest turns route selection into an inspectable version history. Every branch shares a parent,
every Act has a typed address and dose, every rendered image is attached to a transition, and every
rejected route remains available for later diagnosis. This creates a valuable research dataset:

- native state before a failure;
- candidate route and dose;
- native-consumer outcome;
- collateral and negative-family behavior;
- exact rollback and continuation evidence;
- the eventual control decision.

That dataset can train a selector, calibrate abstention, identify when a payload or route is at
fault, and provide reversible training feedback. It is a much better substrate for orchestration
than a collection of winning PNGs.

## What we can do with this now

The immediate practical capability is a failure-specific native repair gate:

```text
native state at an early boundary
  → selector scores native continuation versus a tested repair route
  → abstain or dispatch a typed Act
  → native consumer closes the loop
  → Future Forest retains the alternative and rollback receipt
```

That can support:

1. **Canary repair.** Run native first, intervene only when a calibrated state signature predicts
   a known failure, and require negative/collateral preservation before promotion.
2. **Route-aware training.** Treat accepted and rejected futures as labeled transitions. Train the
   control plane on route utility while keeping the recipient payload and native consumer fixed;
   rewind every candidate controller update that harms the accepted closure.
3. **Failure localization.** Compare native, fixed-route, selector, zero-state, inverted, wrong-time,
   and oracle arms to decide whether the problem is address, payload, dose, timing, continuation,
   or evaluator—not merely “the model failed.”
4. **Capability packaging.** Package the payload and selector separately. The payload is a
   recipient-bound Act; the selector is a least-authority control policy with explicit reads,
   allowed routes, dose envelope, abstention, hashes, and rollback permissions.
5. **Model versioning.** Re-run the same route gate at a later checkpoint. If the fixed Act drifts
   but the native state still predicts the repair seam, Saturn can recompile the local route or
   reject the stale package instead of silently applying it.
6. **Coding-model experiments.** Move the same architecture to an autoregressive code organism:
   earlier native state selects a repair Act, the untouched model generates code, and a sandboxed
   test suite measures compilation, behavior, and continuation. The host must not write the code
   or choose the answer; it may only score the native consumer after the branch.

The last item is the bridge back to our original coding-capability hypothesis. This FLUX result
does not prove coding ability. It tests whether a capability can be factored into a native payload,
a distributed carrier route, and a separate context-conditioned control plane. That architectural
fact is worth testing in code models because code execution provides a strong native consumer,
while FLUX provides unusually visible final RGB closure.

## The next protocol after v5

v5 completed the support-gate debug pass. Its result says the next run should preserve the Saturn
mechanics while separating calibration from final held-out routing. The current support threshold
is useful as a fail-closed instrument, but it is not calibrated: it rejected the entire blue panel.
The next run should therefore add a third split and genuinely new held-out families:

1. Freeze the route candidates, evaluator, split, and analysis script before looking at outcomes.
2. Use seed-disjoint development, calibration, and held-out sets; do not call a same-seed,
   same-family panel cross-seed or blind family generalization.
3. Hide the previously targeted blue-circle family from final held-out development, then introduce
   at least two genuinely new held-out families with both positive and negative/collateral tasks.
4. Keep `native`, fixed `joint3`, fixed `joint4`, selector, zero-state, shuffled-state, inverted,
   wrong-time, and oracle-route controls. Add a constant-repair baseline and a constant-abstain
   baseline.
5. Calibrate the abstention threshold on a separate split. Report coverage, repair precision,
   false-positive cost, and collateral cost; freeze the threshold before final held-out dispatch.
6. Require the selector to beat both constant native and fixed repair on a predeclared utility
   score, not merely to vary its action labels or recognize a family.
7. Measure count, independent image structure, pixel-level change, route/action identity, and
   continuation. Preserve every evaluator disagreement and adjudicate anti-aliasing failures.
8. Repeat across enough seeds to estimate repair precision and false-positive cost. A useful gate
   must repair failures without applying collateral changes to native-success and negative rows.
9. Add a coding-organism pilot only after the image gate has an in-support calibration result.
   Use an autoregressive model whose native consumer is generated code plus an external sandboxed
   test suite; keep model-authored code, route choice, test execution, and host scoring separate.
10. Only after that, test a new FLUX revision and a broader autoregressive coding organism. Keep each
   consumer and claim denominator separate.

The success criterion is not “the selector chose different routes.” It is:

```text
native-state selector improves held-out native-consumer utility
> constant native and fixed repair baselines
while preserving negatives, abstaining on unknown cases, reporting both instruments,
and replaying exactly.
```

That is the experiment that could turn this promising route signal into a real meta-capability
claim.

## What the native-state test was meant to ask

The selector experiment uses the same model revision, Act package, prompts, seeds, route candidates,
and held-out Future Forest structure. The new difference is where the decision comes from.

At `joint.1`, before any candidate write, the worker captures a low-dimensional summary of the
native text state. A deterministic ridge selector is compiled from development specimens: its
labels come from development-only downstream image utility, while its serving input is only the
earlier native state. It can choose among `native`, `joint.2`, `joint.3`, `joint.4`, and `single.0`.

On held-out prompts, the selector sees no expected count, family label, final image, or held-out
score. It dispatches a typed route write during the same native denoising pass. Controls include a
fixed `joint.3` route, native continuation, zero-state selector input, and an inverted/hostile
dispatch. The selector package, logits, chosen action, parent frame, final image, and Future
Forest decision are all retained.

The v4 result sharpens the same separation. Native state can change the selected action without
seeing held-out outcomes, and the changes can be structured by a new held-out family. But the
selected route did not beat constant native continuation, fixed `joint3` was better, and the
abstention threshold was overconfident. The v5 replay then made the uncertainty plane explicit:
all nine serving states were outside the frozen development support, so the selector abstained
and matched native exactly. This separates “the state carries a route-correlated family and
distribution-shift signal” from “the model can predict per-parent native-consumer utility.”
That distinction is the bridge to coding models: the code organism must expose a strong native
consumer and a held-out test where route choices, uncertainty, and collateral behavior can all be
measured independently.

## v6: calibrating support before allowing a route

The next replay froze the selector protocol before opening a fresh green held-out family. It used
two red development seeds, two red calibration seeds, and two green held-out seeds, with seed and
family sets disjoint. The selector had four actions—`native`, `joint3_gain2`, `joint4_gain2`, and
`abstain`—and its support radius was chosen from calibration-only utility and collateral.

The run had `106` logical rows across `22` immutable parent cuts. Saturn loaded one FLUX.2 Klein
recipient, captured the earlier native state, compiled the package, promoted it in a Future Forest,
rewound to the root, and reopened the forest. Native rewind, suffix replay, and both forest closure
checks were exact. Held-out outcomes were hidden at dispatch. The independent RGB evaluator and the
image atlas agreed on `105/106` rows; the one disagreement was a calibration red-circle branch
where downsampling merged components.

The calibration policy chose support multiplier `3.0` and radius `8.115`. At smaller multipliers it
abstained on all eight calibration parents. At `3.0` it dispatched `native` on four and abstained on
four, with zero calibration false positives. On green held-out parents it abstained on both six-circle
rows and selected native on the two five-square rows and the two negative three-triangle rows. The
selector therefore matched constant native continuation exactly: positive mean count error was
`1.500` for both, positive exactness `0/4`, and all negative rows remained exact. Fixed `joint3` had
positive mean error `0.500`; fixed `joint4` had `2.500` and visible component merging.

This is a useful safety trend, not route improvement. v6 demonstrates that an earlier native state
can expose a distribution-shift/support signal and that Saturn can fail closed before an unsupported
route write. It does not demonstrate per-parent route utility, semantic block ownership, or a useful
meta-router. The policy never entered a calibration regime where a non-native route had a measured
advantage, so abstention was the correct instrument outcome.

Two debugging details matter for replication. First, the first image audit only counted blue
components; the corrected analyzer uses the target hue and keeps the legacy blue audit for
backward compatibility. Second, the atlas disagreement was not silently discarded: a full-resolution
audit showed that the atlas's `160×160` downsample merged red components that remained separate at
`512×512`. The raw report remains the authority, and the audit is a separate derived artifact.

The v6 artifacts are the [experiment README](../../saturn/experiments/2026-08-16-flux-native-state-route-selector-v6/README.md),
[analysis](../../saturn/results/flux-native-state-route-selector-v6/job-32de47a11821/ANALYSIS.md),
[raw report](../../saturn/results/flux-native-state-route-selector-v6/job-32de47a11821/report.json),
and [run receipt](../../saturn/results/flux-native-state-route-selector-v6/job-32de47a11821/run-receipt.json).

## Artifacts

- [Prior route/dose Future Forest README](../../saturn/experiments/2026-08-15-flux-block-future-replay/README.md)
- [Prior route/dose analysis](../../saturn/results/flux-block-future-replay/job-620af5702f8c/ANALYSIS.md)
- [Prior route/dose report](../../saturn/results/flux-block-future-replay/job-620af5702f8c/report.json)
- [Native-state selector analysis](../../saturn/results/flux-native-state-route-selector/job-287fcc52b40f/ANALYSIS.md)
- [Native-state selector report](../../saturn/results/flux-native-state-route-selector/job-287fcc52b40f/report.json)
- [Balanced native-state selector v2 analysis](../../saturn/results/flux-native-state-route-selector-v2/job-e9398856f6ec/ANALYSIS.md)
- [Balanced native-state selector v2 report](../../saturn/results/flux-native-state-route-selector-v2/job-e9398856f6ec/report.json)
- [Repair-gated native-state selector v3 analysis](../../saturn/results/flux-native-state-route-selector-v3/job-a7556c2507cc/ANALYSIS.md)
- [Repair-gated native-state selector v3 report](../../saturn/results/flux-native-state-route-selector-v3/job-a7556c2507cc/report.json)
- [Clean split native-state selector v4 README](../../saturn/experiments/2026-08-15-flux-native-state-route-selector-v4/README.md)
- [Clean split native-state selector v4 analysis](../../saturn/results/flux-native-state-route-selector-v4/job-ecd0bdafb10e/ANALYSIS.md)
- [Clean split native-state selector v4 report](../../saturn/results/flux-native-state-route-selector-v4/job-ecd0bdafb10e/report.json)
- [Clean split native-state selector v4 successful receipt](../../saturn/results/flux-native-state-route-selector-v4/job-ecd0bdafb10e/run-receipt.json)
- [Clean split native-state selector v4 failed debug receipt](../../saturn/results/flux-native-state-route-selector-v4/job-2ff0ab4a93b9/run-receipt.json)
- [Support-aware native-state selector v5 README](../../saturn/experiments/2026-08-15-flux-native-state-route-selector-v5/README.md)
- [Support-aware native-state selector v5 analysis](../../saturn/results/flux-native-state-route-selector-v5/job-20d8fd4402fc/ANALYSIS.md)
- [Support-aware native-state selector v5 report](../../saturn/results/flux-native-state-route-selector-v5/job-20d8fd4402fc/report.json)
- [Support-aware native-state selector v5 receipt](../../saturn/results/flux-native-state-route-selector-v5/job-20d8fd4402fc/run-receipt.json)
- [Support-aware native-state selector v5 analysis JSON](../../saturn/results/flux-native-state-route-selector-v5/job-20d8fd4402fc/ANALYSIS.json)
- [Support-aware native-state selector v5 package](../../saturn/results/flux-native-state-route-selector-v5/job-20d8fd4402fc/selector-package.npz)
- [Support-aware native-state selector v5 Future Forest](../../saturn/results/flux-native-state-route-selector-v5/job-20d8fd4402fc/future-forest/)
- [Recipient-native patch experiment](../../saturn/experiments/2026-08-14-flux-capability-patch-red-apples/README.md)
- [Failure-first Saturn replay guide](2026-08-15-bfl-failure-replay-saturn.md)
- [Saturn capability map](2026-08-14-what-saturn-can-actually-do.md)

This report preserves both the successful route trend and the selector's unresolved orchestration
boundary without rewriting either underlying artifact.
