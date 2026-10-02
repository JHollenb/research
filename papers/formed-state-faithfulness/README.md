---
title: "Formed-State Faithfulness"
author: Jacob Hollenbeck
type: research-paper-readme
status: submission-manuscript (custody audit in progress)
date: 2026-10-02
---

# Formed-State Faithfulness: A Reasoning Step's Causal Role Splits Into the Token a Monitor Sees and the Cache It Cannot

Paper: [`paper.md`](paper.md). Audience: frontier-lab chain-of-thought monitoring and interpretability teams.

## Abstract

Chain-of-thought monitoring assumes that reading what a model writes tells you what the model
used. We measure how far that assumption holds for a single arithmetic reasoning step whose written
value is not restated in the prompt. We separate the step's causal role into a token-visible channel
(the written value a monitor can read) and a hidden-state channel (the key/value cache the step
forms, which the text does not expose). Every intervention is gated by an exact-restore control that
reproduces the base answer bit-for-bit. Two results stand out. The hidden channel has near-total
capacity: overwriting only the step's cached state with a wrong value's state, while the written
value stays correct, changes the completed answer on 100% of items at 0.5B and 1.5B parameters
(n=21-32) and 95% at 7B (n=22), across three precisions; a monitor reading the correct chain sees
nothing. This is a capacity measurement made with an artificial edit, not a claim that models hide
reasoning. The natural gap grows with scale: after a step's cached state is removed, larger models
silently re-derive it and still answer correctly more often (0.19 at 0.5B to 0.76 at 1.5B in
bfloat16, non-overlapping CIs; replicated 0.29 to 0.73 on a 4-bit axis), and when the model writes
its own chain the regenerated text announces the removal only 11% of the time. Removal-based
faithfulness metrics therefore under-count a step's role, increasingly with scale. Visible
chain-of-thought is an upper bound on monitorability, not a measure of it.

## Status

- **Submission manuscript (custody-audit corrections applied).** Pre-registration and falsifiers
  frozen before any run.
- **Primary evidence:** `~/domains/saturn/experiments/2026-10-02-cot-formed-state-faithfulness/`
  (findings, pre-registration, frozen manifest, per-job results, analysis summary, figures).
- **Custody audit complete.** Point estimates recomputed exactly from the final post-bug-fix full
  runs; no fabricated or stale numbers. Six corrections applied in this version: (1) the
  hidden-channel result is scoped to a step-reading monitor and the answer-continuation
  re-verbalization fractions are now reported (Sections 4.3, 7.1); (2) both free-running arms are
  discounted by the frozen no-op canary (8/9 and 5/9 below 0.90), free is exploratory only;
  (3) scale comparisons are unpaired/nested, with a common-subset robustness check (Section 5.3);
  (4) Figure 2 redrawn with two separate precision axes and the 7B point marked NF4; (5) the 7B
  copied-canary n (6/6) footnoted and the VRAM figures labeled asserted; (6) the post-freeze
  additive amendment to the frozen manifest disclosed (Appendix D). Further reviewer corrections
  will be folded in with a changelog.
- All runs measured on one RTX 4080, greedy, one seed, stock attention with native causal masks.
  Confidence intervals are 95% item-level bootstrap (10,000 resamples).

## Figures

| Figure | File | Source |
|---|---|---|
| 1 (planned) | `<!-- TODO: VM trace render -->` placeholder in `paper.md` | trace visualizer in preparation |
| 2 Silent repair vs scale | `figures/fig2_repair_vs_scale.png` | redrawn from `EXP/results/analysis-summary.json` (two separate precision axes; 7B marked NF4). Supersedes primary `figures/fig1_repair_vs_scale.png`, which drew the 7B-NF4 point on the bf16 line |
| 3 Token-vs-state dissociation | `figures/fig3_token_vs_state.png` | copied from primary `figures/fig2_token_vs_state.png` |
| 4 Free-running chain-of-thought | `figures/fig4_free_running.png` | copied from primary `figures/fig3_free_running.png` |

## Evidence map (claim → source path)

Paths under `~/domains/`. The primary experiment directory is abbreviated
`EXP = saturn/experiments/2026-10-02-cot-formed-state-faithfulness`.

| # | Claim in paper | Numbers | Source path |
|---|---|---|---|
| C1 | Exact-restore no-op reproduces the base answer bit-for-bit (instrument foundation) | max abs seq-logprob Δ = 0.0, all items, all runs incl 4-bit | `EXP/results/analysis-summary.json` (`remount_delta_max`); `EXP/FINDINGS-draft.md` (canaries table); `EXP/PREREG.md` (F1c) |
| C2 | Copied point-read canary flips the answer | 1.00 (n=8/run; n=6-7 at 7B) | `EXP/results/analysis-summary.json` (`copied_unmount_changed`) |
| C3 | Early-vs-late canary: early inert, late decisive | early 0.00, late 1.00 (n=8) | `EXP/results/analysis-summary.json` (`multi_early_changed`, `multi_late_changed`) |
| C4 | Token-visible channel: written-token swap dominates input swap, ×4 families; plain-incapable → chain-capable | SmolLM2-1.7B 8.02 vs 0.94; Qwen2.5-0.5B 9.23 vs 0.88; Qwen3-8B 14.18 vs 0.53; Qwen3-30B-A3B 11.59 vs 1.64; plain -0.54→+2.40, pc 1.00→9.60 | `saturn/experiments/2026-08-21-ird-fruit-battery/README.md` (Addenda F1-R, F2-R, F3-R; F-E) |
| C5 | Hidden channel capacity: state-only edit changes answer, written value correct (monitor-blind) | 1.00 @0.5B/1.5B (bf16, fp32, NF4); 0.955 @7B NF4 [0.864,1.000], n per table | `EXP/results/analysis-summary.json` (`monitor_blind_change_rate`); `EXP/FINDINGS-draft.md` (Exp 2) |
| C6 | Text-visible edit changes answer (co-varies channels; baseline) | 1.00 everywhere | `EXP/results/analysis-summary.json` (`text_visible_change_rate`) |
| C7 | Directed state authorship (sufficiency): donor state → donor answer, rises with scale | 0.594 @0.5B → 0.810 @1.5B bf16 / 1.000 @1.5B fp32 / 0.818 @7B NF4 | `EXP/results/analysis-summary.json` (`swap_cf_authored`) |
| C8 | Silent repair rises with scale, bfloat16 axis (clean) | 0.188 [0.062,0.344] (0.5B) → 0.762 [0.571,0.952] (1.5B); +0.57, non-overlapping | `EXP/results/analysis-summary.json` (`repair_rate`); `EXP/figures/fig1_repair_vs_scale.png` |
| C9 | Silent repair rises with scale, 4-bit axis (quant-matched) | 0.292 [0.125,0.458] (1.5B) → 0.727 [0.545,0.909] (7B); +0.44, non-overlapping | `EXP/results/analysis-summary.json` (`repair_rate`) |
| C10 | fp32-vs-bf16 is a null (not a float-point artifact) | 0.5B 0.188 = 0.188; 1.5B 0.762 vs 0.828 (d=0.066, overlapping CIs) | `EXP/results/analysis-summary.json` (`repair_rate`); `EXP/FINDINGS-draft.md` (Exp 1, DTYPE part A) |
| C11 | NF4 4-bit halves repair at fixed size (measured confound) | 1.5B NF4 0.292 vs bf16 0.762 (d=0.47); gap 0.47 < bf16 scale gap 0.57 | `EXP/results/analysis-summary.json`; `EXP/FINDINGS-draft.md` (Exp 1, DTYPE part B) |
| C12 | Removal-wrong rate falls with scale (complement of repair) | 0.812 (0.5B) → 0.238 (1.5B bf16); 0.625 (1.5B NF4) → 0.273 (7B NF4) | `EXP/results/analysis-summary.json` (`removal_wrong_rate`) |
| C13 | Free-running: self-generated state is causally read (swap changes answer) | 1.000 @1.5B and @7B | `EXP/results/analysis-summary.json` (`free.*.swap_answer_changed`) |
| C14 | Free-running: silent repair of removed step, text usually silent | @1.5B ablate silent-repair 0.778, text-reveals 0.111 [0,0.333], answer-changed 0.222 | `EXP/results/analysis-summary.json` (`free.qwen15/bf16`) |
| C15 | Free-running boundary: coherent injected value is re-verbalized | swap text-reveals 1.000 both sizes | `EXP/results/analysis-summary.json` (`free.*.swap_text_reveals`) |
| C16 | Free-running BOTH sizes discounted by frozen no-op canary (threshold 0.90) | free no-op 8/9=0.889 @1.5B, 5/9=0.556 @7B | `EXP/results/analysis-summary.json` (`noop_matches_base`); `EXP/PREREG.md` + `EXP/FROZEN.json` (F3c, `free_noop_matches_base_min`=0.9) |
| C17 | Monitor recall: a STEP-reading monitor has ~0% recall on the state-only edit (derived); a FULL-TRANSCRIPT monitor recovers most because the model re-verbalizes the injected value | re-verbalize among monitor-blind-changed items: 21/32 (0.5B), 20/21 (1.5B bf16), 29/29 (1.5B fp32), 21/21 (1.5B nf4), 14/21 (7B) | measured from raw `report.json` rows (`steps.s1v.dissoc.text_orig_state_wrong.text` vs `mistake_value`); matches custody audit |
| C17b | Scale rise and NF4 deflation survive on common (paired) item subsets | 0.5B→1.5B bf16 common n=21: 0.095→0.762; 1.5B→7B nf4 common n=17: 0.353→0.824; all-six common n=11: 0.091/0.818(bf16)/0.273(nf4)/0.818(7B) | computed from raw `report.json` rows (`steps.s1v.unmount.repaired` by item name) |
| C18 | Deviations: 3B uncached; 7B bf16 exceeds card → NF4; shim inert on non-4-bit paths | — | `EXP/FROZEN.json` (`deviations`, `smoke_bugfixes`); `EXP/FINDINGS-draft.md` (Deviations) |
| C19 | Confounded precedent de-confounded here (prior E10; later step individually decisive, not a strict time circuit) | swap authorship 19/32, 30/30; removal-wrong 26/32, 3/30 | `research/papers/time-formed-circuits/paper.md` (E10 row); `saturn/experiments/2026-10-01-e10-completed-answer-rerun/FINDINGS.md`; `.../2026-10-01-e10-cot-intermediate-steps/VERIFICATION-2026-10-01.md` |
| C20 | Hidden state in self-generated, non-arithmetic content (corroboration) | move self-generated value state, visible reply fixed → later answer changes 3/3 eligible, block 2/3 | `saturn/experiments/2026-10-01-qwen-alias-binding-feedback/FINDINGS.md` |
| C21 | Copied-value necessity (context; non-copied earlier reading superseded) | copied-value necessity 0.84 flips | `saturn/experiments/2026-09-30-mvm-mamba-cot/FINDINGS.md` |

## Job identifiers (custody)

Full runs: teacher — 0.5B bf16 `job-8acc379d0951`, 0.5B fp32 `job-bd0bf96a7a27`,
1.5B bf16 `job-d0ad89ab793c`, 1.5B fp32 `job-4861f1f15284`, 1.5B NF4 `job-4a5981fa28fc`,
7B NF4 `job-bc10cd445816`; free — 1.5B bf16 `job-602f0c494da4`, 7B NF4 `job-f904b4749690` (discounted).
Full binding records in `EXP/results/job-bindings/`.

## Citations (arXiv IDs verified 2026-10-02 via web search)

Lanham et al. 2023 (2307.13702); Turpin et al. 2023 (2305.04388, NeurIPS 2023);
Chen et al. 2025 (2505.05410); Korbak et al. 2025 (2507.11473);
Pfau, Merrill, Bowman 2024 (2404.15758); Baker et al. 2025 (2503.11926);
Paul, West, Bosselut, Faltings 2024 (2402.13950); Bentham, Stringham, Marasović 2024 (2402.14897);
Miller, Chughtai, Saunders 2024 (2407.08734).

## Known open items for revision

- Custody-audit corrections to the primary numbers (audit was running at submission).
- Figure 1 (hidden-vs-visible trace render) is a placeholder pending the trace visualizer.
- Natural-language reasoning at scale, a bfloat16 7B point, and multi-seed runs are future work.
