---
title: "The Answer Follows the Cache (working name: Formed-State Faithfulness)"
author: Jacob Hollenbeck
type: research-paper-readme
status: Parked 2026-10-02 after round 2 (4/10, fold recommended); content will likely fold into Paper 2
date: 2026-10-02
---

> **Parked 2026-10-02 after round 2 (4/10, fold recommended).** Kept as an accurate record; its
> content will likely fold into the companion paper (Paper 2). Only evidence-accuracy fixes were
> applied after round 2 (see `reviews/round2-response.md`).

# The Answer Follows the Cache: A Reasoning Step's Formed State Can Override Its Written Token

Working name: *Formed-State Faithfulness*. Paper: [`paper.md`](paper.md). Audience:
chain-of-thought monitoring and interpretability work.

## Abstract

Chain-of-thought monitoring assumes that reading what a model writes reveals what it used. We
separate a reasoning step's role into the written token a monitor reads and the key/value cache it
forms (Qwen2.5, 0.5B-3B), under a bit-exact restore control. Main pre-registered result: when the
two channels disagree, the answer follows the cache. Overwriting only the step's stored state with a
wrong value's, leaving the written token correct, changes the answer on 100% of items at
0.5B/1.5B/3B. The disagreement is injected, so it shows the hidden channel can override the token,
not that models hide reasoning. A step-reading monitor has zero recall on it by construction, though
the model usually re-verbalizes the injected value, so a full-transcript monitor recovers most. We
also correct our earlier reading: when a removed step's answer survives, it is recomputed from
still-visible operands — two pre-registered controls show the original answer is never reproduced
once operands are cut or resampled (0.5B, 1.5B), making this a dispensability caveat for
removal-based attribution, not a hidden channel. A single-layer linear probe did not reach its
pre-registered detection bar. Natural-task reasoning is the open gap. Scope: synthetic arithmetic,
greedy, one seed; a workshop-scale note.

## Status

- **Round-2 revision — major reframe.** Controls landed and the central round-1 critique is
  conceded: the "silent repair rises with scale" result (old E1) is **recompute-from-prompt**, not a
  hidden channel. The paper is retitled and rebuilt around the one solid pre-registered result (the
  injected token-vs-state dissociation) plus two honest negatives (E1 = dispensability; the state
  probe did not clear its bar). Framed as a workshop-scale note.
- **Primary evidence:** `saturn/experiments/2026-10-02-cot-formed-state-faithfulness/`
  (FINDINGS-draft.md, FINDINGS-addendum-2-draft.md, PREREG + PREREG-addendum-2, results, figures);
  VM trace `saturn/experiments/2026-10-02-vm-trace-visualizer/`.
- **Round-2 changes:** (1) E1 demoted — two pre-registered controls (operand-mask A, operand-resample
  A') show post-ablation repair collapses when operands are cut (0.188→0.000 at 0.5B, 0.531→0.031 at
  3B; tracks-original 0.000 at 0.5B and 1.5B) → recompute-from-prompt, not concealment. Scale-growth
  claim retracted (rate non-monotone 0.188/0.762/0.531; 3B is a BASE model). (2) E2 (state-only swap)
  promoted to the central result (100% at 0.5B/1.5B/3B; invisible to a step-reading monitor by
  construction; injected, not natural). (3) Probe (control B) reported as a NEGATIVE: pre-registered
  swap-decode recall 0.19/0.19/0.00 < 0.70 bar; the looser 0.84/0.81/0.97 flag is exploratory only
  (no false-positive rate, ridge λ tuned on the same items). "Monitor the cache" is NOT headlined.
  (4) Title → "The Answer Follows the Cache". (5) Figures: Fig 4 = probe-negative, Fig 5 = control A;
  old repair-vs-scale demoted to Appendix G; VM trace kept as Fig 2. (6) Full-transcript
  re-verbalization caveat kept (0.66-1.00). (7) 7B bf16 (Instruct, paged) pending `job-050706578e6c`.
- **Open:** TODO D natural-task reasoning (the main gap); 7B clean point; layer-swept probe with a
  held-out false-positive rate; multi-seed.
- Custody audit of addendum-2 is in progress; small wording fixes may follow.
- All runs on one RTX 4080, greedy, one seed, stock attention with native causal masks. CIs are 95%
  item-level bootstrap (10,000 resamples).

## Figures

| Figure | File | Source |
|---|---|---|
| 1 Two-lane schematic (§2.4) | `figures/fig1_two_lane_schematic.png` | schematic: visible token lane vs formed-cache lane + the three interventions |
| 2 VM trace, one real item (§2.4) | `figures/fig2_vm_trace.png` | measured render from `saturn/experiments/2026-10-02-vm-trace-visualizer/renders/qwen-trace.png` (`job-e034c77db8d6`): hidden-page attention, necessity peak L20 (0.274), hidden/visible dependence strip |
| 3 Token-vs-state + recovery (§4.3) | `figures/fig3_token_vs_state.png` | state-only/text-visible bars + full-transcript recovery series (0.66-1.00) |
| 4 Probe is a NEGATIVE (§5) | `figures/fig4_probe_monitor.png` | rebuilt this round from addendum-2: state-swap 1.0, text recall 0, PREREG probe swap-recall 0.19/0.19/0.00 vs 0.70 bar, loose post-hoc flag shown hatched/exploratory. Replaces the earlier over-positive figB |
| 5 Control: repair-from-prompt (§7) | `figures/fig5_control_repair_from_prompt.png` | copied from addendum-2 `figures/figA_control_repair_from_prompt.png`: R1/R2/R3 + resample R4/R4s vs size |
| F1 Free-running (Appendix F) | `figures/figF1_free_running.png` | discounted panel |
| G1 Repair-rate precision controls (Appendix G, supplementary) | `figures/figG1_repair_vs_scale.png` | the uncontrolled repair rate (R1) = recompute-from-prompt; retained only for the fp32/NF4 precision controls |

## Evidence map (claim → source path)

Paths under `~/domains/`. The primary experiment directory is abbreviated
`EXP = saturn/experiments/2026-10-02-cot-formed-state-faithfulness`.

| # | Claim in paper | Numbers | Source path |
|---|---|---|---|
| C1 | Exact-restore no-op reproduces the base answer bit-for-bit (instrument foundation) | max abs seq-logprob Δ = 0.0, all items, all runs incl 4-bit | `EXP/results/analysis-summary.json` (`remount_delta_max`); `EXP/FINDINGS-draft.md` (canaries table); `EXP/PREREG.md` (F1c) |
| C2 | Copied point-read canary flips the answer | 1.00 (n=8/run; n=6-7 at 7B) | `EXP/results/analysis-summary.json` (`copied_unmount_changed`) |
| C3 | Early-vs-late canary: early inert, late decisive | early 0.00, late 1.00 (n=8) | `EXP/results/analysis-summary.json` (`multi_early_changed`, `multi_late_changed`) |
| C4 | Token-visible channel: written-token swap dominates input swap, ×4 families; plain-incapable → chain-capable | SmolLM2-1.7B 8.02 vs 0.94; Qwen2.5-0.5B 9.23 vs 0.88; Qwen3-8B 14.18 vs 0.53; Qwen3-30B-A3B 11.59 vs 1.64; plain -0.54→+2.40, pc 1.00→9.60 | `saturn/experiments/2026-08-21-ird-fruit-battery/README.md` (Addenda F1-R, F2-R, F3-R; F-E) |
| C5 | Hidden channel load-bearing: state-only edit changes answer, written value correct (written-step-blind) | 1.00 @0.5B/1.5B (bf16, fp32, NF4); 0.955 @7B NF4 [0.864,1.000], n per table | `EXP/results/analysis-summary.json` (`monitor_blind_change_rate`); `EXP/FINDINGS-draft.md` (Exp 2) |
| C5b | Text-only cell (written value wrong, state restored correct): token pull falls with scale | 0.469 @0.5B bf16, 0.5625 @0.5B fp32, 0.00 @1.5B (all prec), 0.095 @7B | `EXP/results/analysis-summary.json` (`text_wrong_state_orig_rate`) |
| C6 | Text-visible edit changes answer (co-varies channels; baseline) | 1.00 on every row where measured; **not measured at 3B (n/a)** — dissociation panel never ran 3B | `EXP/results/analysis-summary.json` (`text_visible_change_rate`) |
| C7 | Directed state authorship (sufficiency): donor state → donor answer, rises with scale | 0.594 @0.5B → 0.810 @1.5B bf16 / 1.000 @1.5B fp32 / 0.818 @7B NF4 | `EXP/results/analysis-summary.json` (`swap_cf_authored`) |
| C8 | **RETRACTED reading** — repair rate R1 (now = recompute-from-prompt, not a hidden channel; scale-growth retracted, rate non-monotone across the full curve); kept only in Appendix G | 0.188 (0.5B) / 0.762 (1.5B) / 0.531 (3B base); see CA1/CA2 | `EXP/results/analysis-summary.json` (`repair_rate`); `EXP/FINDINGS-addendum-2-draft.md` |
| C9 | Repair rate R1 on the 4-bit axis (supplementary precision characterization) | 0.292 (1.5B) → 0.727 (7B NF4) | `EXP/results/analysis-summary.json` (`repair_rate`) |
| C10 | fp32-vs-bf16 is a null (not a float-point artifact) | 0.5B 0.188 = 0.188; 1.5B 0.762 vs 0.828 (d=0.066, overlapping CIs) | `EXP/results/analysis-summary.json` (`repair_rate`); `EXP/FINDINGS-draft.md` (Exp 1, DTYPE part A) |
| C11 | NF4 4-bit halves repair at fixed size (measured confound) | 1.5B NF4 0.292 vs bf16 0.762 (d=0.47); gap 0.47 < bf16 scale gap 0.57 | `EXP/results/analysis-summary.json`; `EXP/FINDINGS-draft.md` (Exp 1, DTYPE part B) |
| C12 | Removal-wrong rate falls with scale (complement of repair) | 0.812 (0.5B) → 0.238 (1.5B bf16); 0.625 (1.5B NF4) → 0.273 (7B NF4) | `EXP/results/analysis-summary.json` (`removal_wrong_rate`) |
| C13 | Free-running: self-generated state is causally read (swap changes answer) | 1.000 @1.5B and @7B | `EXP/results/analysis-summary.json` (`free.*.swap_answer_changed`) |
| C14 | Free-running: removed-step answer usually still correct (now read as recompute-from-prompt, per CA1/CA2) | @1.5B ablate still-correct 0.778, text-reveals 0.111, answer-changed 0.222 | `EXP/results/analysis-summary.json` (`free.qwen15/bf16`) |
| C15 | Free-running boundary: coherent injected value is re-verbalized | swap text-reveals 1.000 both sizes | `EXP/results/analysis-summary.json` (`free.*.swap_text_reveals`) |
| C16 | Free-running BOTH sizes discounted by frozen no-op canary (threshold 0.90) | free no-op 8/9=0.889 @1.5B, 5/9=0.556 @7B | `EXP/results/analysis-summary.json` (`noop_matches_base`); `EXP/PREREG.md` + `EXP/FROZEN.json` (F3c, `free_noop_matches_base_min`=0.9) |
| C17 | Monitor recall: a STEP-reading monitor has ~0% recall on the state-only edit (by construction); a FULL-TRANSCRIPT monitor recovers most because the model re-verbalizes the injected value | re-verbalize among written-step-blind-changed items: 21/32 (0.5B), 20/21 (1.5B bf16), 29/29 (1.5B fp32), 21/21 (1.5B nf4), 14/21 (7B) | measured from raw `report.json` rows (`steps.s1v.dissoc.text_orig_state_wrong.text` vs `mistake_value`); matches custody audit |
| C17b | Scale rise and NF4 deflation survive on common (paired) item subsets | 0.5B→1.5B bf16 common n=21: 0.095→0.762; 1.5B→7B nf4 common n=17: 0.353→0.824; all-six common n=11: 0.091/0.818(bf16)/0.273(nf4)/0.818(7B) | computed from raw `report.json` rows (`steps.s1v.unmount.repaired` by item name) |
| C18 | Deviations: 3B uncached; 7B bf16 exceeds card → NF4; shim inert on non-4-bit paths | — | `EXP/FROZEN.json` (`deviations`, `smoke_bugfixes`); `EXP/FINDINGS-draft.md` (Deviations) |
| C19 | Confounded precedent de-confounded here (prior E10; later step individually decisive, not a strict time circuit) | swap authorship 19/32, 30/30; removal-wrong 26/32, 3/30 | `research/papers/time-formed-circuits/paper.md` (E10 row); `saturn/experiments/2026-10-01-e10-completed-answer-rerun/FINDINGS.md`; `.../2026-10-01-e10-cot-intermediate-steps/VERIFICATION-2026-10-01.md` |
| C20 | Hidden state in self-generated, non-arithmetic content (corroboration) | move self-generated value state, visible reply fixed → later answer changes 3/3 eligible, block 2/3 | `saturn/experiments/2026-10-01-qwen-alias-binding-feedback/FINDINGS.md` |
| C21 | Copied-value necessity (context; non-copied earlier reading superseded) | copied-value necessity 0.84 flips | `saturn/experiments/2026-09-30-mvm-mamba-cot/FINDINGS.md` |
| C22 | VM trace, one real item (Fig 2): hidden page read, necessity peak L20, state-swap flip, NO repair on this item | Qwen2.5-1.5B bf16, 6×7−5 answer 37; L20 necessity 0.2738, band 20-22; hidden/visible dep 3.76/3.38 at answer digit; donor state-swap flips (text fixed); zeroing −3.0433; no-op 0.0 | `saturn/experiments/2026-10-02-vm-trace-visualizer/` (FINDINGS-draft.md; traces/qwen-trace.json `side_series` argmax L20, `removal_answer_delta`, `canaries.noop_canary_max_abs`); `job-e034c77db8d6` |
| CE2b | E2 dissociation holds at 3B base: state-only swap changes answer 100% | swap_changed 1.000 @3B (adds to 0.5B/1.5B all-prec 1.00, 7B NF4 0.955) | `EXP/FINDINGS-addendum-2-draft.md`; `job-52b8771fc5ef` |
| CA1 | **Control A (operand mask):** post-ablation repair collapses when operands are cut (recompute-from-prompt) | R1/R2/R3: 0.188/0.000/1.000 (0.5B); 0.762/0.000/0.571 (1.5B, mask destructive); 0.531/0.031/1.000 (3B) | `EXP/FINDINGS-addendum-2-draft.md`; `EXP/figures/figA_control_repair_from_prompt.png`; jobs `job-87c47cb47c2b` (0.5B), `job-e3c984961358` (1.5B), `job-52b8771fc5ef` (3B) |
| CA2 | **Control A' (operand resample, non-destructive):** original answer never reproduced → no hidden channel | tracks-new/tracks-original/sanity: 0.156/0.000/1.000 (0.5B); 0.450/0.000/0.952 (1.5B; R4 misses R1−0.15 bar = PARTIAL). tracks-original 0.000 at 0.5B & 1.5B (no 3B resample arm) | `EXP/FINDINGS-addendum-2-draft.md`; resample smoke `job-2a7348247f9e` |
| CB1 | **Control B (probe) — NEGATIVE:** single-layer linear probe did NOT reach the prereg swap-decode bar | prereg swap-decode recall 0.19/0.19/0.00 (0.5B/1.5B/3B) < 0.70. Loose post-hoc flag 0.844/0.810/0.969 = EXPLORATORY (no FPR; ridge λ tuned on same items; LOO decode). base-decode 0.438/0.095/0.281 vs chance 0.048/0.062/0.048 | `EXP/FINDINGS-addendum-2-draft.md`; `EXP/figures/figB_probe_monitor.png` |
| CT1 | 7B bf16 (Instruct, paged) control point PENDING | — | `job-050706578e6c` (draft earlier cited cancelled `job-366e400ba3aa`) |
| CP1 | Addendum-2 prereg provenance | frozen_utc as recorded; file rewritten 02:57 (additive resample arm; no earlier copy exists); 3B row ran worker 3b4db8d2 (not FROZEN header 50ebb297); 3B "base" from dir name, config confirms 3B arch | `EXP/PREREG-addendum-2.md`, `EXP/FROZEN-addendum-2.json` |

## Job identifiers (custody)

Full runs: teacher — 0.5B bf16 `job-8acc379d0951`, 0.5B fp32 `job-bd0bf96a7a27`,
1.5B bf16 `job-d0ad89ab793c`, 1.5B fp32 `job-4861f1f15284`, 1.5B NF4 `job-4a5981fa28fc`,
7B NF4 `job-bc10cd445816`; free — 1.5B bf16 `job-602f0c494da4`, 7B NF4 `job-f904b4749690` (discounted).
Full binding records in `EXP/results/job-bindings/`.

## Citations (arXiv IDs verified via web search 2026-10-02)

Round-0: Lanham et al. 2023 (2307.13702); Turpin et al. 2023 (2305.04388, NeurIPS 2023);
Chen et al. 2025 (2505.05410); Korbak et al. 2025 (2507.11473);
Pfau, Merrill, Bowman 2024 (2404.15758); Baker et al. 2025 (2503.11926);
Paul, West, Bosselut, Faltings 2024 (2402.13950); Bentham, Stringham, Marasović 2024 (2402.14897);
Miller, Chughtai, Saunders 2024 (2407.08734).
Round-1 additions: McGrath et al. 2023 Hydra Effect (2307.15771); Rushing & Nanda 2024 (2402.15390,
ICML 2024); Bugaud 2026 (TrustNLP 2026, pp. 515-527, no arXiv — as cited in Paper 1); Yu 2024
(2411.15862); Yang et al. 2024 (2402.16837, ACL 2024); Biran et al. 2024 (2406.12775, EMNLP 2024);
Radhakrishnan et al. 2023 (2307.11768).

## Known open items (round-2)

- Control A (repair-from-prompt): **DONE** — recompute-from-prompt confirmed (CA1/CA2); E1 demoted.
- Control B (probe monitor): **DONE, negative** — single-layer probe below the prereg bar (CB1).
- Control C (clean high-scale point): 7B bf16 Instruct via paged execution PENDING (`job-050706578e6c`).
- Control D (natural word problems): the main open gap; the dissociation and dispensability results
  are synthetic-arithmetic only.
- Probe follow-up: layer sweep + held-out false-positive rate (the single-layer, same-item-tuned
  probe is a lower bound).
- Secondary: zero/resample-ablation comparison for mean-ablation OOD; multi-seed.
