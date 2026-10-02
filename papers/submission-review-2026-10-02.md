---
title: "Submission review: Space/Time + Scaffolds papers"
type: review
date: 2026-10-02
scope: research/papers/space-and-time-circuits, research/papers/scaffolds-and-dynamic-circuits, obsidian 09-30/10-01 writeups, saturn/experiments 09-29..10-02, all Mamba/Black Mamba work
method: 2 Opus 4.8 deep reviews, 1 Opus 4.8 staleness audit, 1 Opus 4.8 Mamba investigation, 3 Sonnet inventories; read-only. Full agent reports in session scratchpad (review-space-time.md, review-architecture.md, staleness-audit.md, mamba-investigation.md, inventory-*.md).
---

# Submission review (2026-10-02)

Goal: two submissions that frontier interpretability teams read and remember.

## Verdict

Both papers have real, checkable results under too much wording. The numbers are mostly honest: spot-checks of E20, E6, FLUX four-quadrant, E19, E8, the 24-coordinate relation profile, C7/C8 and the Mamba H-only result all match their FINDINGS. The problems are **length, hedging, internal jargon, three papers' worth of scope in each draft, and a handful of stale/overclaimed lines in space-and-time `paper.md`.**

| | Paper 1: Time-formed circuits | Paper 2: Scaffolds and dynamic circuits |
|---|---|---|
| Vehicle | `time-emphasis-paper.md` spine + E6 restored as full section (~14 pp) | `bridge-paper.md` spine + method/figures from `architectural-paper.md` (~10 pp) |
| Memorable sentence | circuit-tracer + Gemma Scope moves the identity answer ≤0.08 under full feature interchange; a native K/V cut flips 83% — identity lives in the transcoder error terms | an identical K/V patch has query-dependent authority (16/16, 16/16; 3.13 / 0.58 nats), and a profile frozen before held evaluation beats three sealed competitors 8/8 |
| Flagship | E20: block 0.924 / independent rescue 0.871 (42 rows, Qwen2.5-1.5B) | same-patch/different-query + prospective 24-coord profile + v_proj permutation collapse |
| Drop/demote | "new class of circuit", "final boss", compiler/VM (§3.2–3.4, §10) to appendix or systems paper | cross-family "common role graph" claim → honest null section; C5/C7/C8, SDXL, Pythia, scene compiler, VM → appendix; `paper.md` (≈90% redundant) |
| Realistic target | arXiv + interp workshop now; main track after cut + 1 external-model replication | arXiv + workshop (BlackboxNLP / mech-interp workshops); main track needs public reproducible release |

Venue deadlines were not verified. Check ICLR 2027 / workshop CFPs before choosing.

## Split the two papers cleanly

Today E20 appears in three documents, and "static infrastructure and dynamic circuits" is both the space-time §8 heading and Paper 2's title.
- **Paper 1 owns:** what time-formed circuits are and how to certify them (E20, E16/17/19, E13/E18 read join, E6, FLUX four-quadrant, E10, architecture-variation table).
- **Paper 2 owns:** reuse. That means the scaffold framing, query-selective authority, the prospective profile, the weight-permutation result, France→Germany feedback and the connected paths. It cites Paper 1 for E20.
- Retitle space-time §8.

## Must-fix before any submission (Paper 1, `space-and-time-circuits/paper.md`)

| # | line | issue | fix |
|---|---|---|---|
| 1 | :47 abstract | "non-restated intermediate K/V causally controls subsequent answers". E10 rerun: removal ends wrong 26/32 (0.5B) but only **3/30** (1.5B, repairs 25/30) | lead with swap authorship 19/32, 30/30; say removal is often repaired at 1.5B |
| 2 | :938 | "15/32 and 30/30" is the old 14-token readout; completed rerun = **19/32** (paper already says 19/32 at :926 and App. A) | use 19/32 |
| 3 | :632, :702, :719, :728, :801 | Mamba writer "stops its clock" stated as mechanism. Only causal test (`2026-10-02-mamba-operation-clock-debugger`) gives small mixed-sign clock-dose effects (+.0322 / −.0664 / joint −.0343 nats) and says retention alone cannot nominate a writer. Paper B already absorbed this; A did not | "writer is a retention outlier (correlational, 1 prompt/1 seed); a matched clock-dose test on a different task shows small mixed-sign effects" |
| 4 | :1298 | "per-carrier attribution passes at 30B": no provenance found; neighbours the retracted 30B in-forward confound | verify or mark in-forward-only |
| 5 | :910 | Qwen3-30B CoT swap 11.59 from private August battery, unannotated | annotate or drop |
| 6 | E6 text | head-to-head n = 12 identity + 8 color; the 0.83/0.84 flips come from the separate 42/25-row sweep | state both denominators |

Paper 2 is current as of its 23:08 save. Open items:
- **C8 "Both Mamba arms reach 8/8 longitudinal competence from a 4/8 baseline":** no source line in the checked-in FINDINGS/LEARNING-SUMMARY (checked). Add the receipt line or cite the report JSON path.
- **`qwen-source-bridge-read-law`:** development findings landed at 23:14–23:27, after the paper. Held rows are unopened; re-check before freezing the paper.
- **Source records needing in-file annotations:** E5 FINDINGS still opens with the retracted Mamba certification; the E1b heading still says "interchange-only"; `ar-feedback/FINDINGS.md` lacks the causal-mask note.

## Reviewer attacks to pre-empt (both papers)

1. **Hedging fog.** Sentences stack 3–5 qualifiers ("bounded / host-orchestrated / post-held / not_assessed / mask-qualified / n_new=0"). Use one claim per paragraph and move evidence-ladder labels to a legend. Worst examples, with rewrites, are in the agent reports.
2. **Lab jargon in the body:** Saturn, mrun, TokenMachine, Future Forest, LayerCut, C5–C8/E#, job IDs, seal/denominator/registered. Move it to a reproducibility appendix and gloss what stays.
3. **Single unreleased stack plus the causal-mask defect.** The defect shows the harness can emit confident, verifier-passing, invalid results. Re-derive the headline numbers with stock HF eager, and release code and receipts.
4. **Novelty vs Meng 2022 / Geva 2023 / Hase 2023 / Agarwal 2026 (2609.17537, deferred commitment).** Lead with the delta: isolated vs in-forward cut, full sweeps overturning sampled certificates, E20 independent transplant rescue, exact-row read join.
5. **Certificate framing.** By the paper's own §2.2, a linear additive system passes four quadrants, and no LM cell passes. Present it as an operational signature with FLUX as the clean instance, not a "new class".
6. **n and replication.** LM cells ≤4 items, mostly 1 seed, one lab. For Paper 2 the cross-family core is 2+2+1 rows, feedback is 1/3 held contexts, and the connected forecast **ties plain addition exactly**. Report that null openly as its own figure.

## Results not yet in either paper (from obsidian + saturn inventories)

Strongest first:
- **qwen-frozen-reference-payload** (Paper 2): a frozen late B-value K/V changes native B in 7/8 held reference ops, with A preserved 8/8.
- **qwen-alias-binding-feedback** (Paper 2): 3/3 eligible held cells at 96.8–100% recovery; generated-state rescue flips the later answer 3/3. Two of four held cells are not competent.
- **scaffold-graph-identification** four-branch decomposition (Paper 2): retained history +1.28 to +1.58 nats against an opposing new row, in 4/4 contexts.
- **Semantic-program payload** 148/150 vs 0/150 native (145/148 incl. Qwen3-30B-A3B) and **source-address plane** 96/128 vs 59/128. These are strong "program" results that fit neither thesis cleanly; possibly a Paper 2 appendix.
- **Hidden-objective audit negatives:** internals AUROC .734 vs black-box .812; sandbag cue flips only at layers ≥15. Not in the thesis, but a credibility asset with labs as an honest limitation.
- **Mamba quotient theorem:** exact quotient impossible; balanced truncation keeps 98–99% at r16. It is in neither paper and runs on the laptop only, without mrun custody.

## Mamba / Black Mamba

- **Keep the split.** Stock-Mamba connected results belong in Paper 2, which already uses them well and carefully: H-only successor transfer 12/12, the 27-coord prospective profile (capital 8/8, delayed identity 4/4), and one shared state serving two operations. Paper 1 keeps Mamba as the SSM variation: one concentrated late writer at 0.69–0.83 depth (130M L20 81%, 370M L39 67%, 2.8B L44 67%), no certificate, sampled E5 retracted. Apply fix #3 above.
- **No standalone Black Mamba paper.** Too many owned-organism results fail or are unfinished: common-parent LOCO failed, the Krylov GO rule failed, the writer-affine arc is not established, shared-basis Stage-A was never executed, and the local-clock 24/24 is matched by a no-decay slot.
- The quotient theorem is the one clean separable result. It is a model-reduction result, not a circuits result.

## Possible third paper (stronger than expected)

**Rotation Swamping / PhaseLock + B(x) exact accumulation.** These are measured, cheap to reproduce, and directly relevant to lab training numerics:
- bf16 RoPE re-rotation: pass-key 0/24 vs 24/24; fp32 phase collapses at 2^24;
- B(x) cuts median gradient error vs fp64 from 204% to 11.8% on Pythia-160m;
- Qwen3 Q4 failure traced to a k_norm γ outlier.

Gaps: no training run shows a loss or throughput win; everything is ≤1.7B and single seed; prior art overlaps (GProj, SageAttention smoothing, pre-RoPE KV quant). The missing piece is a late-checkpoint Pythia continuation with B(x) vs bf16.

## Cheapest experiments with most acceptance impact (~10-min mrun each)

**Paper 1**
1. E20 on a non-Qwen family (Llama-3.2-3B or Gemma-2-2B). Answers "one model".
2. E6 on a second behavior or model, so the flagship becomes a trend.
3. Sub-layer sweep of Qwen1.5 identity in L22–27 (heads, K vs V, positions). Tests whether "distributed" survives below layer grain.
4. Clock-dose panel on the original writer-clock task (130M L20, 2.8B L44). Settles fix #3 on its own task.
5. Held-out E20 identities.

**Paper 2**
1. Scale France→Germany feedback from 1/3 to 6–8 clean held contexts.
2. Stock-HF-eager re-derivation of the query-selective and relation-profile headlines (mask-defect trust).
3. Double holdout: unseen checkpoint and task family, with frozen site and null predictions.
4. A cross-family test whose scaffold and additive predictions differ.

**Black Mamba:** run the quotient theorem q1–q4 under mrun with receipts.

## Figures

- **Paper 1, missing:** E20 dissociation bar chart (seed / block / rescue / wrong-band), FLUX four-quadrant 2×2 with the 5-seed strip, E6 side-by-side. Keep fig3, fig4, fig5; demote fig1 and fig6.
- **Paper 2, missing:** same-patch/different-query (its most memorable result has no figure), an honest generalization panel (additive tie, matcher ≈ depth null, 2+2+1 n), and a France→Germany ladder. The existing role schema and confirmation-results figures are fine; move reader-profiles to the appendix.
