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
3. **If it stays standalone,** lead with one result that only the transaction view predicts, and test it at n ≥ 20 on public models with a bundled verifier. (Superseded by the addendum below: the position-invariance result first proposed here is an attention identity, not a candidate.)
4. **Replace private-only receipts** with bundled extracts, or drop those rows from the dossier.

## Sources

- [Models Take Notes at Prefill: KV Cache Can Be Editable and Composable](https://arxiv.org/html/2606.17107v1)
- [Single-Position Intervention Fails: Distributed Output Templates Drive In-Context Learning](https://arxiv.org/html/2605.04061)
- [DecodeShare: Tracing the Shared Subspace of LLM Decode-Time Decisions](https://arxiv.org/pdf/2607.20469)

## Addendum (same day): lineage dig

Written after reading `saturn/experiments/2026-08-25-natural-task-state-kv-causal-chain/RESULTS.md`, `2026-08-23-mimas-blind-final-boss/`, and the Aug 23–Sep 24 final-boss and transaction posts.

**Correctness issue: joint K/V row-permutation invariance is an identity, not a finding.**
- For cached post-RoPE keys, with no mask or positional bias left to permute, attention is invariant under a joint permutation P of source rows: softmax(Q(PK)ᵀ)PV = softmax(QKᵀ)V.
- The program's own 2026-09-24 post (`obsidian/blog/2026-09-24-194732-break-the-model-at-the-memory-transaction.md`) states this.
- §4.2 presents the joint-permutation result as a measured property, and §6 calls it "a real result and also a leak." A reviewer will flag both.
- Restate it as an expected invariance that served as an instrument check. Keep only the K-only/V-only divergence as the measured part, which is itself expected (see above).

**§7 placeholder.** It still needs filling or removing before release. An earlier draft of this addendum filled it from the 2026-09-30 blind-certification run; the author flagged that run's tooling as unreliable, so those findings are withdrawn here.

**Prior art for the 7B chain.** The corrected chain (`job-a12ed4b56846`) finds that a PROGRAM prefix forms a task state at the post-layer-0 residual, and that the resulting K/V corridor makes a task-free prompt execute the algorithm on later data.
- That is close to in-context task vectors (Hendel et al., 2023) and function vectors (Todd et al., 2024).
- Neither is cited. Cite both and state what joint-K/V carriage adds.
- The record itself scopes the result to one checkpoint, one program, and four operands.

**Baselines already run.** The 2026-08-26 head-to-head (`2026-08-26-hyperion3-writer-baselines-head-to-head`) found a mean-tape baseline matching the donor-free writer (6/6 vs 5/6) and single-direction steering at 0/6. The surviving claim is that factorization buys address specificity, not computation. The paper's §5 cites the 5/6 writer without that baseline and should add it.

**Net effect on the verdict above.** Unchanged for this paper as a standalone. The dig raises the standing of the program behind it (consumer-closed certification, preregistration, custody, blind grading, retractions kept on the record) more than it raises this paper.

## Shared session notes

See [`assessment-notes.md`](assessment-notes.md) for the full session record.
