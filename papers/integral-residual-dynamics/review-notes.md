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

1. **Extract C7 into its own short paper.** Use more tasks and at least 20 items per cell, and add one larger open model (Qwen3-32B class). Run Lanham-style truncation and mistake-insertion baselines on the same items, and ship a public offline verifier. This is the highest-leverage path to lab attention in this paper.
2. **Fold the cut result and the isolated-swap rule into the measurement paper** (`../pointwise-instruments-miss-distributed-circuits/`). That paper is the strongest of the set: public verifiers, blind grading, and a SAELens arm. Either retire IRD as a standalone theory paper or keep it as that paper's appendix.
3. **Before any external release,** bundle or drop every number that cites only a private job ID, and replace "below bar" grid entries with values.
4. **Engage the 2026 overlap directly** in Related Work (the two papers above), stating what the four-quadrant certificate adds beyond "window beats single site."

## Sources

- [Single-Position Intervention Fails: Distributed Output Templates Drive In-Context Learning](https://arxiv.org/html/2605.04061)
- [Single-Layer Activation Edits Easily Corrupt Factual Recall but Rarely Repair It](https://aclanthology.org/2026.trustnlp-main.38/)
- [Towards Best Practices of Activation Patching](https://arxiv.org/pdf/2309.16042)
- [Layer-Patching Analysis (overview)](https://www.emergentmind.com/topics/layer-patching-analysis)
