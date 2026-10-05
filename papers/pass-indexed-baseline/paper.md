---
title: "Score Multi-Turn Interventions Against the Pass-Indexed Native, Not a Fixed Parent"
type: research-paper
status: draft
date: 2026-10-05
updated: 2026-10-05
tags: [interpretability, activation-patching, kv-patching, steering-vectors, baselines, multi-turn, methods]
---

# Score Multi-Turn Interventions Against the Pass-Indexed Native, Not a Fixed Parent

**A methods note on baselines for interventions inside multi-turn contexts**

Jacob Hollenbeck

*2026-10-05*

> Every number in this note is measured and traceable to a frozen report in the two experiment
> folders named in the reproducibility appendix.

---

## Abstract

When you intervene on a transformer inside a multi-turn context — add a steering vector at the
third turn, patch a key/value entry that a later question reads — you have to compare the
intervened run against *some* clean run. A common, convenient choice is the single-turn parent: the
prompt with only the current question, no earlier turns. We show this is the wrong baseline and
measure how wrong. In a four-turn context on Qwen2.5-1.5B (base), the native answer
log-probability of a later turn moves by a median of 2.54 nats relative to the single-turn parent,
and every move is positive: the earlier turns, including the model's own earlier answers, make the
later answer more confident. The move is not a formatting artifact. A length-matched control with
irrelevant earlier turns attributes about half the median move (≈1.31 nats) to turn formatting and
the other half (≈2.25 nats, and all of the persistent, later-turn part) to carried content — chiefly
the model's own earlier answers. Scoring a late key/value install against the single-turn parent,
rather than against the pass-indexed native (the same earlier turns already run), flips the sign
and/or the 1-nat-threshold conclusion in 11 of 12 pass≥1 cells; a format-matched baseline removes
none of the 11 flips. The effect reproduces on instruction-tuned weights
(Qwen2.5-1.5B-Instruct: median drift 2.76 nats, 9 of 12 cells flip) and at 7B
(Qwen2.5-7B-Instruct, median drift 1.99 nats, baseline-difference 1.04 nats, 4 of 12 cells cross the sign/1-nat flip line) **when the multi-turn context is plain text, the regime the
base measurement used**. Under the idiomatic chat template the error vanishes only on saturated reads (1.5B-Instruct: median drift 0.002 nats, 0 of 12 cells flip), for a mechanistic reason the base experiment's own control predicts: a chat-template baseline is already turn-formatted, removing the formatting half, and an instruct model saturates on scene-determined reads, so the carried-content half adds nothing and both baselines agree. It returns in full on a harder, referential chat read on the same model (median drift 2.23 nats; the reported install effect changes by a median of 2.72 nats between baselines), where it surfaces as a materially mis-sized effect rather than a binary sign or threshold flip, and across chat cells its size tracks the unsaturation of the read (Spearman 0.91 over 60 per-pass cells). The error is therefore large exactly when the scored read is not already saturated and the earlier turns bear on it. The recipe to avoid it is one any careful evaluator would endorse: build the baseline by running the earlier turns natively, then continue. Our contribution is the measured size of the error, and the regimes in which it bites.

## 1. The problem

Causal-intervention methods localize and quantify a behavior by changing one thing in a forward
pass and reading the change in output against a clean baseline [1–4]. The baseline is load-bearing:
necessity and sufficiency, a sign, a "removes X% of the effect," a "crosses the 1-nat threshold" all
mean *relative to the clean run*. Best-practice guides are explicit that the baseline and the
corruption define the quantity, and that a poorly matched baseline produces confident wrong numbers
[1, 2].

Most single-pass experiments pick the baseline correctly by construction: the clean run is the
same context as the intervened run, minus the intervention. The hazard appears in **multi-turn**
settings, which are now ordinary — steering vectors added during a conversation [5, 6], key/value
patches whose effect is read by a *later* question, cached-prefix evaluations, rewind-and-continue
probes. Here the intervened read sits after several earlier turns, and it is tempting to score it
against the single-turn parent: the prompt with just the current question. That parent is missing
everything the earlier turns wrote into the context — including the model's own earlier answers,
which a later turn can attend to. In an autoregressive model the cached keys and values of those
earlier positions are part of the state the later read consumes. Dropping them changes the clean
distribution the intervention is measured against.

We call the correct baseline the **pass-indexed native**: the model's own greedy continuation with
the *same* earlier turns already executed natively, differing from the intervened run only by the
intervention. A **pass** is one answered turn (equivalently, in a free generation, one produced
token); pass p means p earlier turns are already in context. The fixed parent is pass 0. This note
measures `Drift(p) = native_logprob(pass p) − native_logprob(pass 0)` and shows what it does to
the conclusions of a key/value install.

The recipe to get it right is obvious and not novel; careful practitioners already rewind and
continue [2]. The point of the note is the measured magnitude: the error is large (nats, not
hundredths), it is content (not formatting), and it flips sign and threshold conclusions on the
reads an interpretability experiment actually scores — at base, instruct, and 7B.

## 2. Setup

**Panel.** A synthetic two-fact scene, "On the left is a {color} {animal}. On the right is a
{color} {animal}.", followed by a four-turn context. The turns are T0 identity-left (answer: the
left animal), T1 color-right, T2 color-left, and T3 recap-left (a referential turn that can be
answered from the scene or from the model's own T0 answer). Four scenes
(fox/cat, frog/dog, bird/sheep, wolf/pig). Each content word is a single leading-space token,
asserted per run. The scored answer token of each turn is a fixed gold token; the margin is against
a named competitor. Greedy, seed 0; the model is deterministic, so the replicate axis is
scenes × passes, not seeds.

**Baselines.** For turn t, the **fixed** context is the scene plus turn t's question only; the
**pass-indexed (re-baselined)** context is the scene plus the model's own greedy answers to turns
0..t−1 plus turn t's question. For t = 0 the two are identical by construction (a built-in
Drift ≈ 0 canary).

**Intervention (R2).** A key/value install in the standard isolated form [3]: run the context
normally, overwrite the left-animal fact-span keys and values at a late layer band with a donor
scene's (a different left animal at the same token positions and geometry), then run only the
later read and score the left-animal answer. The install is scored at each pass p = 0..3 against
both the fixed parent and the pass-indexed native. By construction,
`effect_vs_fixed(p) − effect_vs_rebaselined(p) = Drift(p)`, which we verify to ≤1e-6 as an
internal-consistency check.

**Models and regime.** The primary measurement is Qwen2.5-1.5B (base), FP32, eager attention,
late band L22–27. The replication (Section 6) adds Qwen2.5-1.5B-Instruct (FP32, chat template,
band L22–27) and Qwen2.5-7B-Instruct (layer-paged engine, band L19–27 — the commit band measured
for this model). Every intervention has an exact no-op control (install the recipient's own entries,
change nothing); every run asserts that the fact-span band keys/values are bit-identical across
passes (they must be, by causality — the scene is a common prefix of every turn's context).

## 3. The baseline moves (R0)

On Qwen2.5-1.5B (base), the later-turn native answer log-probability moves substantially once the
earlier turns are in context, and always in the same direction — more confident:

| pass p | turn | median Drift (nats, re-baselined − fixed) | native top-1 answer changed |
|---|---|---:|---:|
| 0 | identity-left | 0.000 | — |
| 1 | color-right | +3.125 | yes |
| 2 | color-left | +2.202 | mostly |
| 3 | recap-left | +2.063 | yes |

The median `|Drift|` over passes ≥ 1 is **2.54 nats**; every drift is positive. The native argmax
answer differs between the fixed and the re-baselined baseline in **11 of 12** pass≥1 cells, so even
a bare "is the top token the answer?" check is pass-sensitive. Scoring a later pass against the
single-turn parent therefore understates the model's native support for the answer by ~2–3 nats.
Causality is respected: the fact-span band keys/values are bit-identical across every pass
(max-abs 0.0) — the baseline moves through the *new* positions (the questions and the model's own
answers) and the reader's query, not through the scene's stored entries.

## 4. The move is content, not formatting

A natural objection: the later turns add question/answer *formatting* and absolute position, and
maybe that, not any carried fact, is what raises confidence. A length-matched control separates the
two. For each pass p ≥ 1 we compare three earlier-history arms, all scored on the identical cached
path so only the history *content* differs, with every answer padded to the same length and the
irrelevant questions token-length-matched so the final question sits at the same absolute position:
(a) irrelevant native question→answer turns (formatting and position only); (b) the real questions
with each answer replaced by equal-length placeholders (question content, answers absent); (c) the
real questions and the model's own native answers (= the re-baselined arm).

| component | ≈ | median increment (nats) |
|---|---|---:|
| format priming | drift(a) | +1.312 |
| question-content increment | drift(b) − drift(a) | −0.051 |
| answer-content increment | drift(c) − drift(b) | +2.247 |

Formatting accounts for about half the median move and is **front-loaded**: it is the largest single
component at pass 1 (+2.04) but decays and goes negative by pass 3 (−1.18). The positive,
persistent later-pass drift is carried almost entirely by **content**, and specifically by the
model's own earlier *answers* (the answer-content increment is +2.25 nats and positive at every
pass; the question text, with answers blanked, adds essentially nothing). So the drift is not a
positional/format artifact: a later read draws on what the model itself wrote earlier, which the
fixed parent omits.

## 5. The baseline choice flips install conclusions (R2)

Install the left-animal donor at the late band and score its effect on the identity read at each
pass, against both baselines:

| pass p | effect vs FIXED parent | effect vs PASS-INDEXED native | difference (= Drift) | conclusion flip |
|---|---:|---:|---:|---|
| 0 | −4.749 | −4.749 | 0.000 | — |
| 1 | **+1.237** | **−0.132** | 1.424 | sign and 1-nat both flip |
| 2 | −0.138 | −0.915 | 0.785 | 1-nat threshold flips |
| 3 | −0.290 | −0.990 | 0.690 | 1-nat threshold flips |

At pass 1 the fixed parent reports the install as **+1.24 nats — the wrong sign**, as if the install
*helps* the gold answer, while against the correct pass-indexed native it is −0.13 (a slight harm).
At passes 2–3 the fixed parent understates the harm by ~0.7–0.8 nat, dropping it below the 1-nat
threshold that sibling experiments use to call an effect "real." Counting a flip as a sign change or
a crossing of the 1-nat install-effect threshold, there are **11 flips across the 12 pass≥1 cells**;
the direction-of-authorship conclusion (does the top token become the donor animal?) is
baseline-independent, as expected — only the nat/sign conclusions move. The consistency identity
holds to ≤1e-6.

**A format-matched baseline does not fix it.** Re-scoring the same install against the
format-matched arm (a) instead of the fixed parent, the flips attributable to formatting vs to
carried content split as:

| baseline comparison | flips / 12 | attributable to |
|---|---:|---|
| fixed → pass-indexed (the error in full) | **11** | total drift |
| fixed → format-matched (a) | 7 | formatting |
| format-matched (a) → pass-indexed (c) | **11** | carried content |

Using a format-matched baseline removes **none** of the 11 flips: it is as wrong as the fixed parent
relative to the true per-pass native. Only the pass-indexed native — the model's own earlier answers
in context — removes them.

## 6. Replication on an instruct model and at 7B, in two regimes

We repeated R0 and R2 on Qwen2.5-1.5B-Instruct and Qwen2.5-7B-Instruct (the latter run with a
layer-paged engine; its full runs use BF16, labelled as such). We ran each model in two formats for
the multi-turn context: **raw text** — the base panel verbatim, a plain continuation of the scene
with the questions appended and the model's own answers left in place — and the **chat template** —
the scene as the system message and each turn a real user/assistant exchange with the scored stem
teacher-forced into the assistant turn. The fact-span band keys/values are bit-identical across
passes on every model and format (the scene is a common prefix; the causality canary), and the R2
consistency identity `effect_vs_fixed − effect_vs_pass_indexed = Drift` holds to ≤1e-6 throughout.

The result depends on the regime, and the dependence is informative.

| model | format | median \|Drift\| passes≥1 (R0) | fixed→pass-indexed flips / 12 (R2) |
|---|---|---:|---:|
| Qwen2.5-1.5B (base) | raw | +2.54 | 11 |
| Qwen2.5-1.5B-Instruct | raw | **2.76** | **9** |
| Qwen2.5-1.5B-Instruct | chat | 0.002 | 0 |
| Qwen2.5-7B-Instruct | raw | 1.99 | 4 (bdiff 1.04) |
| Qwen2.5-7B-Instruct | chat | 0.000 | 0 |
| Qwen2.5-0.5B-Instruct | chat, scene-pinned reads | 0.005 | 0 |
| Qwen2.5-1.5B-Instruct | chat, referential reads | **2.23** | 0 (bdiff **2.72**) |
| Qwen2.5-1.5B-Instruct | chat, distractor read | 0.077 | 0 (bdiff 0.39) |

In the **raw-text** regime the base phenomenon reproduces on instruct weights: the later-pass
baseline moves by nats (1.5B-Instruct median 2.76, all per-pass medians positive) and the install
conclusion flips in a majority of cells (9/12; pass-1 sign flip, passes 2–3 threshold flips, just as
in the base). A not-length-matched format-matched control leaves 4 of those flips in place, i.e.
some are carried-content-driven, consistent with the base's rigorous decomposition.

In the chat-template regime the effect attenuates to zero *when the scored read is saturated* — but
not otherwise, and the condition is what matters. On the fully-specified scenes the identity and
color reads are pinned by the always-present scene (system message), and an instruction-tuned model
reads them with near-certainty (fixed-parent gold logprob ≈ −0.000); its own earlier answer then adds
nothing, both baselines agree, and the drift is 0.002 nats on Qwen2.5-1.5B-Instruct (0/12 flips) and
1.4e-5 on Qwen2.5-7B-Instruct. Two mechanisms combine to produce this: a chat-template *fixed*
baseline is already a formatted turn, so the formatting half of the base drift is absent by
construction; and the scene-pinned read is saturated, so the carried-content half adds nothing.

The error returns, still under the chat template, as soon as the scored read is not saturated. On a
harder, referential read on Qwen2.5-1.5B-Instruct — teacher-forced turns of the form "repeat the
animal you named earlier" and "repeat your previous answer", whose answer the fixed parent cannot
supply because it contains no earlier answer (fixed-parent gold logprob −4.1 to −6.2 nats) — the
pass-indexed native and the fixed parent disagree by a median of 2.23 nats over passes ≥ 1, and the
reported effect of a late key/value install changes by a median of 2.72 nats depending on which
baseline is used (for example, at the second turn the install reads as −6.0 nats of harm against the
fixed parent but −1.4 nats against the pass-indexed native). Across all chat-template cells measured
here and in the sibling run, the size of the baseline error tracks the unsaturation of the read:
Spearman(|drift|, −fixed-parent logprob) = 0.91 over 60 per-pass cells. The fixed-parent error is
therefore real and large in the chat regime precisely when the scored read is not already saturated —
the "harder or referential read" of the base claim — and it is harmless only when it is small, on the
saturated reads where both baselines coincide.

Two qualifications follow from the measurements and refine the base claim. First, in this
instruction-tuned chat regime the error surfaces as a large materially-changed *number* — the same
install scored against the wrong baseline is reported several nats too large — rather than as a binary
sign or 1-nat-threshold *flip*: the referential-read cell gives 0 of 12 sign-or-1-nat flips because
the install effect is strongly negative against both baselines (the same pattern as the 7B plain-text
cell, where the baseline difference is ≈ 1 nat but the install is strong under both baselines). The
sign/threshold flips of the base measurement require the moderate regime in which the install effect
sits near a decision boundary; the chat template pushes instruct reads to the extremes (saturated, or
off-distribution) and so reproduces the large *baseline movement* without the binary *flip*. An
evaluator should therefore compare the two baselines on the reported effect size, not only on whether
a sign or threshold conclusion changes. Second, "a weaker model" is not by itself sufficient:
Qwen2.5-0.5B-Instruct still saturates the easy fully-specified reads (median |drift| 0.005 nats, no
read below −0.5 nat), and a four-animal distractor scene does not unsaturate the identity read either,
because first-mention bias pins the first same-side animal over its same-color neighbour by 7.7 nats.
Unsaturation also is not sufficient on its own: an unsaturated read the conversation does not bear on
("which is the second animal on the left", fixed-parent logprob −6.8 nats) does not drift
(≈ 0.08 nat), because the pass-indexed context adds no information the read uses. The error is large
exactly when the read is both unsaturated *and* informed by the earlier turns — which is the common
case for the referential reads a multi-turn interpretability experiment actually scores.

The three added chat cells are preregistered in `saturn/experiments/2026-10-05-pass-indexed-chat-unsaturated/` with four frozen predictions; the two that bear on the claim are that at least one chat arm drifts by a median of 1 nat or more (passed, 2.23) and that the size of the drift tracks the unsaturation of the read across chat cells (passed, Spearman 0.91). The prediction that the referential arm would also cross the sign or 1-nat flip line failed (0 of 12), which is why the chat-regime claim is stated as a mis-sized effect rather than a flipped conclusion. The lesson for an evaluator is therefore conditional but simple: you cannot tell in advance whether your read is in the saturated regime, so build the pass-indexed baseline anyway. It costs one extra native continuation and it is never wrong, whereas the fixed parent is wrong by nats whenever the read has room to move and the earlier turns bear on it.

## 7. Recommendation and recipe

Score any intervention inside a multi-turn context against the pass-indexed native: the model's own
continuation with the same earlier turns already executed, differing from the intervened run only by
the intervention. Concretely:

```
1. Build the pass-indexed context: run turns 0..t-1 natively (greedy), committing
   the model's OWN answers into the context (not teacher-forced references).
2. Clean baseline = continue that context into turn t with NO intervention; read out.
3. Intervened run = fork the same context, apply the intervention, read out the same position.
4. Report effect = intervened - clean, both pass-indexed. Never score against pass 0
   (the single-turn parent) unless t == 0.
5. Canary: with no intervention the fork must reproduce the clean run bit-for-bit, and
   any common-prefix (e.g. system/scene) keys/values must be identical across passes.
6. Sanity: effect_vs_fixed - effect_vs_pass_indexed should equal the native drift; if a
   sign or threshold conclusion changes between the two, trust the pass-indexed one.
```

This is not a new method; it is what careful mediation already prescribes [1, 2]. The contribution
is the measured error from skipping it: median ~2.5 nats of baseline movement, 11/12
install-conclusion flips, half of which survive a format-matched baseline, reproduced at instruct
and 7B.

The recipe is available as an mdb `BenchSession` example
(`saturn-pub/packages/mdb/examples/pass_indexed_baseline.py`) and reproduces the R0 drift on the
same four scenes: run on Beast through mrun in BF16 (mdb's Qwen lane refuses FP32), its per-pass
median drift is +3.33 / +2.08 / +2.22 nats at passes 1–3 (base FP32 +3.13 / +2.20 / +2.06), all
three medians positive, with the fact-span K/V bit-identity canary exact (max-abs 0.0) on every
scene (MEASURED, `job-30443c340ead`).

## 8. Limitations

Synthetic two-fact scenes with templated turns; greedy decoding; a single seed (the model is
deterministic, so seeds are not the replicate axis, but prompt and scene diversity is narrow).
One model family (Qwen2.5) at three sizes up to 7B, plus an instruction-tuned variant; no
cross-family or >7B check here. The 7B run uses a layer-paged execution engine and (for the full
run) BF16; it is validated against a bit-reproduced small-model canary but is a different numeric
regime than the FP32 primary, and we report its result as a direction/size replication, not a bit
match. The install is a late-band key/value swap at one fact span; we did not sweep bands,
intervention types (e.g. steering-vector addition was not run, only argued by analogy), or turn
counts beyond four. The instruct replication uses teacher-forced assistant stems to keep the scored
token fixed; free-form assistant answers would test a slightly different quantity. The flip count
depends on the 1-nat threshold borrowed from sibling experiments; we report the full per-pass effect
tables so a reader can apply another threshold.

## 9. Related work

**Patching baselines and best practice.** Zhang and Nanda [1] (towards best practices for activation
patching) and Heimersheim and Nanda [2] (how to use activation patching) both make the baseline and
the corruption central and warn that the choice determines the quantity measured; this note is a
quantified instance in the multi-turn case, where the "clean run" is ambiguous. Standard
causal-mediation and path-patching treatments [3, 4] assume a matched clean/corrupt pair, which in a
multi-turn context means matching the earlier turns.

**Cache reuse is not a fresh prefill.** Prompt-cache and block-sparse cache-reuse systems (Prompt
Cache [9], CacheBlend [10]) show that reusing cached keys/values across contexts changes the
computation versus a fresh prefill; our drift is the same fact viewed from the evaluation side — the
cached state of earlier turns is part of what a later read consumes, so a baseline that omits it is
not the same computation.

**Steering and intervention methods.** Activation addition (ActAdd [5]) and inference-time
intervention (ITI [6]) add vectors during a forward pass; when that forward pass is turn t of a
conversation, the clean comparison is the pass-indexed native, not the single-turn prompt, for the
same reason given here. Our R2 is a key/value install rather than a residual-stream addition, but
the baseline argument is identical.

**Conversational-context effects.** A growing line documents that multi-turn context changes model
behavior substantially versus single-turn prompting (position and history effects, degradation over
turns); our measurement is the methodological corollary for interventions — if the native behavior
moves across turns, so must the baseline an intervention is scored against.

## Appendix: reproducibility

The 1.5B-base measurement and the format-vs-content control are preregistered in
`saturn/experiments/2026-10-02-pass-indexed-baseline/` (`PREREG.md`, `PREREG-addendum.md`,
`FROZEN.json`; primary job `job-35d4adaeed36`, control job `job-5dbbbeee0dea`, both on frozen
Qwen2.5-1.5B weights, FP32 eager, greedy, seed 0). The instruct and 7B replication is preregistered
in `saturn/experiments/2026-10-05-pass-indexed-instruct-7b/` (`PREREG.md`, `FROZEN.json`; jobs
job-23194c4f1d09 (raw) and job-2e4198b3de14 (chat) for Qwen2.5-1.5B-Instruct and job-8243f04af7c7 (raw) and job-1d9876bd8f78 (chat) for Qwen2.5-7B-Instruct), and the three chat-template cells with unsaturated reads in `saturn/experiments/2026-10-05-pass-indexed-chat-unsaturated/` (`PREREG.md`, `FROZEN.json`; jobs job-7d1a89ea97a7 for Qwen2.5-0.5B-Instruct, job-6fe222d7fd5f for the referential reads and job-7cec3eb6012f for the distractor read on Qwen2.5-1.5B-Instruct, FP32 eager; the vendored 2026-10-05 instrument is reused byte-identically for the 0.5B cell and imported for the other two), with on-disk
weight custody sha256 asserted before load. Each experiment folder carries the worker, the analyzer,
the frozen predictions, every collected report, and the canary results (exact no-op self-install,
fact-span key/value invariance across passes, determinism, and the drift-consistency identity). All
model execution was on a single host via the lab's job scheduler; no numbers were produced on a
laptop. No decoded model-output strings are stored — token ids, log-probabilities, booleans and
sha256 only.

The headline numbers are also bound to their receipt files in a saturn-pub evidence claim registry
at `papers/evidence-registry/` (append-only, hash-chained, standard-library only). The Section 3 R0
drift (+3.125/+2.202/+2.063 nats, all positive) and the Section 5 R2 11/12 install-conclusion flips
are covered by `pib-r0-drift-r2-flips-base`
(`2026-10-02-pass-indexed-baseline/results/pass-indexed-35d4adaeed36/analysis.json`); the Section 6
two-regime replication table is covered by `pib-instruct15b-raw` (9/12 flips), `pib-instruct15b-chat`
(0/12), `pib-instruct7b-raw-bf16` (4/12) and `pib-instruct7b-chat-bf16` (0/12), one per cell, and the three chat-template cells with unsaturated reads by `pib-chat-unsat-05b`, `pib-chat-unsat-referential`, `pib-chat-unsat-distractor` and the cross-cell correlation by `pib-chat-unsat-p3-spearman`. Re-check
offline with `saturn-pub evidence claims verify --check --registry papers/evidence-registry/claims.jsonl`.

## Changelog

- **2026-10-05 (chat regime, unsaturated reads).** Added the three chat-template cells (0.5B-Instruct scene-pinned reads 0.005 nats; 1.5B-Instruct referential reads 2.23 nats with the install effect mis-sized by 2.72 nats between baselines, 0 of 12 binary flips; distractor read 0.077 nats) and the cross-cell correlation (Spearman 0.91 over 60 cells). Rewrote the Section 6 chat paragraphs and the abstract sentence so the chat-regime claim is a mis-sized effect that tracks read unsaturation. Registry claims `pib-chat-unsat-*` bind these cells.
- **2026-10-05 (instruct and 7B).** Added the instruct-weight and 7B replication in the plain-text and chat-template regimes (Section 6) and the evidence-registry paragraph in the appendix.
- **2026-10-02.** First draft: R0 drift, the format-versus-content control, the R2 install-conclusion flips, the recipe.

## References

[1] F. Zhang, N. Nanda. *Towards Best Practices of Activation Patching in Language Models.*
arXiv:2309.16042.
[2] S. Heimersheim, N. Nanda. *How to use and interpret activation patching.* arXiv:2404.15255.
[3] J. Vig et al. *Investigating Gender Bias in Language Models Using Causal Mediation Analysis.*
NeurIPS 2020.
[4] K. Meng, D. Bau, A. Andonian, Y. Belinkov. *Locating and Editing Factual Associations in GPT
(ROME).* NeurIPS 2022.
[5] A. Turner et al. *Activation Addition: Steering Language Models Without Optimization (ActAdd).*
arXiv:2308.10248.
[6] K. Li et al. *Inference-Time Intervention: Eliciting Truthful Answers from a Language Model
(ITI).* arXiv:2306.03341.
[7] N. Elhage et al. *A Mathematical Framework for Transformer Circuits.* Anthropic, 2021.
[8] nostalgebraist. *interpreting GPT: the logit lens.* 2020.
[9] I. Gim et al. *Prompt Cache: Modular Attention Reuse for Low-Latency Inference.* MLSys 2024.
[10] J. Yao et al. *CacheBlend: Fast Large Language Model Serving for RAG with Cached Knowledge
Fusion.* EuroSys 2025 (arXiv:2405.16444).
