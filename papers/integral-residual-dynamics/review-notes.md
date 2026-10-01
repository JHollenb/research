---
title: "Review notes: Integral Residual Dynamics"
type: review-notes
date: 2026-09-30
reviewer: Claude (Opus 5.5), at the author's request
scope: paper.md as committed on 2026-09-30; external-impact assessment, not a correctness audit
---

# Review notes: Integral Residual Dynamics

These notes assess whether the draft, as written, would draw attention from frontier-lab research teams, and what to change so it would. They are a reading of `paper.md` plus a short web search for overlapping work. Nothing was re-run. The overlap judgments rest on the abstracts of the cited papers, not full reads.

## Verdict

Unlikely to draw frontier-lab attention as a standalone paper. One result inside it, C7, could if it is extracted and scaled.

## Why not, as written

1. **The headline claim overlaps known and recent work.** "Single-site patching returns a null while whole-path patching removes and installs the behavior" is long-standing practice knowledge. ROME's causal tracing restores 10-layer windows; the Hydra effect and self-repair papers explain the compensation; and 2026 papers state the observation directly:
   - *Single-Position Intervention Fails: Distributed Output Templates Drive In-Context Learning* (arXiv 2605.04061) reports 0% transfer at every single (layer, position) pair and window effects exceeding the sum of single-layer effects.
   - *Single-Layer Activation Edits Easily Corrupt Factual Recall but Rarely Repair It* (TrustNLP 2026).

   A reviewer will read `R = 𝓘(r(t))` as notation for that observation rather than as a new object.
2. **Thin evidence.** Every grid cell has n ≤ 4, readouts are single-token, and several grid rows report "single-layer below bar" with no number.
3. **Unverifiable by outsiders.** Many load-bearing numbers cite private job IDs with no bundled receipt. As a theory companion, the paper mostly cites its own sibling papers.

## What is distinctive

1. **C7, chain-of-thought externalization.** A scratchpad key/value swap flips the committed answer in four families up to a 30B MoE (log-prob shifts 8.02 / 9.23 / 14.18 / 11.59). Chain-of-thought faithfulness and monitorability is an active safety priority at the frontier labs, and a key/value swap is a cleaner causal test than truncation or inserted mistakes (Lanham et al., 2023). This is the result with real pull, and the draft gives it one bullet.
2. **The certificate is about a cut (§7).** In the same transformer, the four-quadrant cross exists at the key/value cut and vanishes at the residual cut (single-site necessity 1.0–1.5% → 172–236%). This is a useful methods warning.
3. **Isolated vs in-forward key/value swap (§3, rule 2).** The two disagree completely on the same model (0.99 vs 0.00). Practitioners would want this gotcha.
4. **Scale floor (§6).** 70M is concentrated (79–81% of necessity in one layer) and the distributed signature appears by roughly 400M. Interesting but secondary.

## Recommendations

1. **Extract C7 into its own short paper** (but see the addendum: the current C7 design measures copying of a stated answer and needs an intermediate-step swap first). Use more tasks and at least 20 items per cell, and add one larger open model (Qwen3-32B class). Run Lanham-style truncation and mistake-insertion baselines on the same items, and ship a public offline verifier. This is the highest-leverage path to lab attention in this paper.
2. **Fold the cut result and the isolated-swap rule into the measurement paper** (`../pointwise-instruments-miss-distributed-circuits/`). That paper is the strongest of the set: public verifiers, blind grading, and a SAELens arm. Either retire IRD as a standalone theory paper or keep it as that paper's appendix.
3. **Before any external release,** bundle or drop every number that cites only a private job ID, and replace "below bar" grid entries with values.
4. **Engage the 2026 overlap directly** in Related Work (the two papers above), stating what the four-quadrant certificate adds beyond "window beats single site."

## Sources

- [Single-Position Intervention Fails: Distributed Output Templates Drive In-Context Learning](https://arxiv.org/html/2605.04061)
- [Single-Layer Activation Edits Easily Corrupt Factual Recall but Rarely Repair It](https://aclanthology.org/2026.trustnlp-main.38/)
- [Towards Best Practices of Activation Patching](https://arxiv.org/pdf/2309.16042)
- [Layer-Patching Analysis (overview)](https://www.emergentmind.com/topics/layer-patching-analysis)

## Addendum (same day): lineage dig

Written after reading the work behind the paper: `saturn/experiments/2026-08-21-ird-fruit-battery/README.md`, `2026-08-21-ird-verification-battery/`, and the Aug 21–26 ledger and audit posts.

**Correction to "What is distinctive", item 1 (C7).** The C7 evidence is weaker than stated above.
- **One prompt pair per family.** The base prompt is "In the code, x is set to three, and y is set to x plus one. Since x is three, y is three plus one, that is four. The value of y is", and the target swaps in six/seven.
- **The swapped position is the answer token the scratchpad already wrote** ("that is four"), which the final clause then repeats.
- **So the S1 ≫ S2p result shows the model copies its stated answer** rather than recomputing from the input carrier. That matters, but it is close to an expected copy or induction effect. It is not yet evidence about whether intermediate reasoning steps are causally used.

The extraction recommendation therefore needs a harder design:
- Swap an *intermediate* step whose value differs from the final answer (for example, the "three plus one" operand restatement).
- Use multi-step problems where the answer is never written verbatim before the readout.
- Use at least 20 items per family.

Without that, C7 should not be the headline.

**Lineage that raises confidence in the method, not the claim:**
- **Falsifiers fired and stayed in the record:** F-V1 at 70M, F-V2b, F-V3 at 1.7B, and the struck V4 hallucination predictor and F-F.
- **The 8B identity cell closed only after a floor confound and a bf16 last-place artifact were found**, then fixed with a preregistered fp32 dual-backend rerun.
- **The "0.2218 / 0.0013" folklore was caught by the program's own audit.**

This matches the program's evidence discipline, and it is the paper's real credibility asset.

**Excluded at the author's direction.** An earlier draft of this addendum cited results from the 2026-09-30 blind-certification run (`saturn/experiments/2026-09-30-blind-final-boss-certification/`): wrong-depth ratios and a Qwen2.5-0.5B single-layer-sufficiency replay. The author flagged that run's tooling as unreliable, so those findings are withdrawn from these notes and should not be used without independent re-measurement.

## Shared session notes

See [`../capabilities-as-transactions/assessment-notes.md`](../capabilities-as-transactions/assessment-notes.md) for the full session record: first-pass and revised verdicts, the symbol-table and image-editing dig, the author's correction about the final-boss circuit, and a second session's line of thought.
