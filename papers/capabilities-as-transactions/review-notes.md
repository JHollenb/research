---
title: "Review notes: Capabilities as Support-Aware Transactions"
type: review-notes
date: 2026-09-30
reviewer: Claude (Opus 5.5), at the author's request
scope: paper.md as committed on 2026-09-30; external-impact assessment, not a correctness audit
---

# Review notes: Capabilities as Support-Aware Transactions

These notes assess whether the draft, as written, would draw attention from frontier-lab research teams, and what to change so it would. They are a reading of `paper.md` plus a short web search for overlapping work. Nothing was re-run. The overlap judgments rest on the abstracts of the cited papers, not full reads.

## Verdict

Unlikely to draw frontier-lab attention as written, and the weaker of the two companion drafts (the other is `../integral-residual-dynamics/`).

## Why not, as written

1. **Vocabulary carries more than the findings do.** "Transaction," "terminal consumer role," "custody," and "authority" are nonstandard terms. Without a result that only the new framing predicts, a reader will see renaming.
2. **The dossier table argues against the paper.** Most rows are trend, retracted, refuted, or not established. That is honest, and it reads as a lab notebook rather than a claim.
3. **§7 contains an unfilled placeholder** ("Blind certification on FLUX.2 Klein 4B (in progress) … to be completed by the lead session"). The draft cannot be shared until it is filled or removed.
4. **The blind trial did not certify.** The language-model pass issued 0 certificates, and only 1 of 3 diffusion edges survived the wrong-depth control.
5. **The positive mechanistic findings are mostly expected or adjacent to recent work.**
   - **Joint key/value 4/4 vs key-only and value-only 0/4.** Expected from attention's structure: keys without values carry no content, and values without matching keys are not read. *Models Take Notes at Prefill: KV Cache Can Be Editable and Composable* (arXiv 2606.17107) covers nearby ground.
   - **The Pythia-70M whole-model induction account needs layer-2 heads.** Those are the previous-token heads of the standard induction mechanism (Olsson et al., 2022), so finding them is a confirmation, not a discovery.
6. **Thin, partly private evidence.** Every cell is n = 4, and most receipts are private job IDs.

## What is distinctive

- **The method discipline.** The exact no-op gate, consumer-judged verdicts, the evidence ladder, and the "honest leaks" section show strong research judgment. This raises the author's credibility more than it raises the paper's reach.
- **Formation separates from protocol (§4.3).** The protocol-only arm is 0 of 4: the output format is not the task. This is a clean, reusable control.
- **Partial position invariance of the carrier.** Joint-row-shift still installs (4/4), and a row-permuted residual passes (4/4). The "paired records modulo joint permutation" reading is interesting if replicated at larger n.

## Recommendations

1. **Shelve as a standalone paper.** Reuse the transaction grammar as a discussion section in the measurement paper (`../pointwise-instruments-miss-distributed-circuits/`) or the certified-circuit paper.
2. **Fill or delete the §7 placeholder** before anyone outside sees the draft.
3. **If it stays standalone,** lead with one result that only the transaction view predicts, and test it at n ≥ 20 on public models with a bundled verifier. The best candidate is the position-invariance result (joint permutation preserves behavior; split K/V permutation breaks it at the first token).
4. **Replace private-only receipts** with bundled extracts, or drop those rows from the dossier.

## Sources

- [Models Take Notes at Prefill: KV Cache Can Be Editable and Composable](https://arxiv.org/html/2606.17107v1)
- [Single-Position Intervention Fails: Distributed Output Templates Drive In-Context Learning](https://arxiv.org/html/2605.04061)
- [DecodeShare: Tracing the Shared Subspace of LLM Decode-Time Decisions](https://arxiv.org/pdf/2607.20469)
