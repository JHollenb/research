---
title: "Two Channels of a Reasoning Step (working name: Formed-State Faithfulness)"
author: Jacob Hollenbeck
type: research-paper-readme
status: submission-manuscript (round-1 revision; custody audit complete; Controls A-D running)
date: 2026-10-02
---

# Two Channels of a Reasoning Step: The Token a Monitor Reads and the Cache It Does Not

Working name: *Formed-State Faithfulness*. Paper: [`paper.md`](paper.md). Audience: frontier-lab
chain-of-thought monitoring and interpretability teams.

## Abstract

Chain-of-thought monitoring assumes that reading what a model writes reveals what it used. We test
this on a single arithmetic step whose value the prompt never restates (Qwen2.5, 0.5B-7B), editing
the key/value cache the step forms, under an exact-restore control that reproduces the base answer
bit-for-bit. Our cleanest result is natural and scale-dependent: after a step's cached state is
removed, the model still answers correctly far more often at larger scale, the removal unannounced
in the text. On common items the still-correct rate rises from 0.095 (0.5B) to 0.762 (1.5B), so
removal-based attribution under-measures the effect of removing a step. Whether this is internal
re-derivation or recomputation from operands still in the prompt is a control we are running. A
precision control rules out a floating-point artifact; 4-bit quantization roughly halves the rate.
Separately, a maximal edit shows the hidden-state channel is load-bearing: overwriting only the
cached state, written value held correct, flips the answer on 95-100% of items. A step-reading
monitor is blind to this, but the model usually re-verbalizes the injected value (0.66-1.00), so a
full-transcript monitor recovers most. Reading written reasoning steps bounds monitorability rather
than measuring it. Scope: synthetic arithmetic, greedy, one seed.

## Status

- **Round-1 revision.** Pre-registration and falsifiers frozen before any run. Custody audit
  complete (point estimates recomputed exactly from the final post-bug-fix full runs; no fabricated
  or stale numbers). Workshop-ready; main-venue pending the running controls below.
- **Primary evidence:** `~/domains/saturn/experiments/2026-10-02-cot-formed-state-faithfulness/`
  (findings, pre-registration, frozen manifest, per-job results, analysis summary, figures).
- **Round-1 reviewer corrections applied:** (1) central reframe — the silent-repair result is
  stated as measured compensation under removal, with the recompute-from-prompt confound flagged
  plainly and the mechanism left open pending Control A; overclaims ("silently re-derive / under-counts
  a step's role / grows with capability") softened in Sections 5, 7, 10. (2) Re-led abstract/intro
  with the natural silent-repair scale result (common-subset 0.095→0.762); demoted "near-total
  capacity"; promoted the full-transcript recovery (Section 4.3). (3) Title changed to the
  two-channel framing (robust to how Control A falls). (4) "monitor-blind" → "written-step-blind"
  throughout; step-reading vs full-transcript monitor separated (zero recall stated as by
  construction). (5) Fig 1 schematic built (no placeholder); Fig 3 given a re-verbalization/recovery
  series; Fig 4 moved to Appendix F. (6) §3 compressed to a paragraph + Appendix E; §6 compressed;
  §4.4-4.6 merged; scope caveat ≤2 substantive statements; "formed state" defined in §2. (7) Prior
  art added: self-repair/Hydra (McGrath 2023; Rushing & Nanda 2024; Bugaud 2026), implicit/latent
  reasoning (Yu 2024; Yang 2024; Biran 2024), Radhakrishnan 2023; Paper-1 overlap sharpened to a
  new-contribution list. (8) Evidence-audit fixes 1-10 applied (see below).
- **Measured VM-trace figure added (Figure 2).** A real render of one item (Qwen2.5-1.5B,
  `job-e034c77db8d6`) now sits next to the schematic: it shows the hidden page being read (necessity
  peak L20 0.274, band 20-22), the hidden/visible dependence per token (3.76/3.38 at the answer
  digit), the state-only donor swap flipping the answer with text fixed, and — reported honestly —
  zeroing the page breaking the answer (−3.04, NO silent repair on this harder multiply item, vs the
  0.76 panel aggregate: per-item variation). All figures renumbered to reading order (schematic 1,
  VM trace 2, token-vs-state 3, repair-vs-scale 4, free-running F1); files renamed to match.
- **Controls running** (placeholders in paper): A repair-from-prompt (decisive mechanism test),
  B probe-based state monitor, C bfloat16-7B via paged execution + Qwen2.5-3B, D natural word problems.
- All runs measured on one RTX 4080, greedy, one seed, stock attention with native causal masks.
  Confidence intervals are 95% item-level bootstrap (10,000 resamples).

## Evidence-audit fixes applied (round-1)

1. README abstract no longer headlines the discounted 11% free-running number (dropped).
2. Table 1 vs Table 2 n mismatch for 1.5B NF4 (21/23/24) explained in a table note.
3. Table F1 (free) 7B n footnoted (header 9 vs 8 scored for ablate).
4. §3 provenance stated inline (prior battery, different task/models) + Appendix E.
5. Text-only 2×2 cell now reported (§4.1: 0.47/0.56 at 0.5B, 0.00 at 1.5B, 0.10 at 7B).
6. Fig 2 caption "overlap" softened to "sit on/near" (1.5B fp32 diamond at 0.83).
7. Appendix C E3 row tagged discounted.
8. VRAM figures labeled asserted at first mention (§2.2) and Appendix D.
9. Status consistent (audit complete).
10. Superseded primary `fig1_repair_vs_scale.png` not referenced in paper (confirmed).

## Figures

| Figure | File | Source |
|---|---|---|
| 1 Two-lane schematic (§2.4) | `figures/fig1_two_lane_schematic.png` | static schematic: visible token lane vs formed-cache lane + the three interventions |
| 2 VM trace, one real item (§2.4) | `figures/fig2_vm_trace.png` | measured render copied from `saturn/experiments/2026-10-02-vm-trace-visualizer/renders/qwen-trace.png` (`job-e034c77db8d6`); layer×token attention onto the hidden page, necessity peak L20 (0.274), band 20-22, hidden/visible dependence strip; honest note: this item shows NO repair (−3.04 on zeroing) vs the 0.76 panel rate |
| 3 Token-vs-state + recovery (§4.3) | `figures/fig3_token_vs_state.png` | from analysis-summary + raw re-verbalization rows: state-only/text-visible bars + full-transcript recovery series (0.66-1.00) |
| 4 Silent repair vs scale (§5.5) | `figures/fig4_repair_vs_scale.png` | drawn from `EXP/results/analysis-summary.json` (two separate precision axes; 7B marked NF4). Supersedes primary `fig1_repair_vs_scale.png`, which drew the 7B-NF4 point on the bf16 line |
| F1 Free-running (Appendix F) | `figures/figF1_free_running.png` | copied from primary `fig3_free_running.png`; demoted to appendix (discounted panel) |

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
| C17 | Monitor recall: a STEP-reading monitor has ~0% recall on the state-only edit (by construction); a FULL-TRANSCRIPT monitor recovers most because the model re-verbalizes the injected value | re-verbalize among written-step-blind-changed items: 21/32 (0.5B), 20/21 (1.5B bf16), 29/29 (1.5B fp32), 21/21 (1.5B nf4), 14/21 (7B) | measured from raw `report.json` rows (`steps.s1v.dissoc.text_orig_state_wrong.text` vs `mistake_value`); matches custody audit |
| C17b | Scale rise and NF4 deflation survive on common (paired) item subsets | 0.5B→1.5B bf16 common n=21: 0.095→0.762; 1.5B→7B nf4 common n=17: 0.353→0.824; all-six common n=11: 0.091/0.818(bf16)/0.273(nf4)/0.818(7B) | computed from raw `report.json` rows (`steps.s1v.unmount.repaired` by item name) |
| C18 | Deviations: 3B uncached; 7B bf16 exceeds card → NF4; shim inert on non-4-bit paths | — | `EXP/FROZEN.json` (`deviations`, `smoke_bugfixes`); `EXP/FINDINGS-draft.md` (Deviations) |
| C19 | Confounded precedent de-confounded here (prior E10; later step individually decisive, not a strict time circuit) | swap authorship 19/32, 30/30; removal-wrong 26/32, 3/30 | `research/papers/time-formed-circuits/paper.md` (E10 row); `saturn/experiments/2026-10-01-e10-completed-answer-rerun/FINDINGS.md`; `.../2026-10-01-e10-cot-intermediate-steps/VERIFICATION-2026-10-01.md` |
| C20 | Hidden state in self-generated, non-arithmetic content (corroboration) | move self-generated value state, visible reply fixed → later answer changes 3/3 eligible, block 2/3 | `saturn/experiments/2026-10-01-qwen-alias-binding-feedback/FINDINGS.md` |
| C21 | Copied-value necessity (context; non-copied earlier reading superseded) | copied-value necessity 0.84 flips | `saturn/experiments/2026-09-30-mvm-mamba-cot/FINDINGS.md` |
| C22 | VM trace, one real item (Fig 2): hidden page read, necessity peak L20, state-swap flip, NO repair on this item | Qwen2.5-1.5B bf16, 6×7−5 answer 37; L20 necessity 0.2738, band 20-22; hidden/visible dep 3.76/3.38 at answer digit; donor state-swap flips (text fixed); zeroing −3.0433; no-op 0.0 | `saturn/experiments/2026-10-02-vm-trace-visualizer/` (FINDINGS-draft.md; traces/qwen-trace.json `side_series` argmax L20, `removal_answer_delta`, `canaries.noop_canary_max_abs`); `job-e034c77db8d6` |

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

## Known open items (running controls / future work)

- Control A (decisive): repair-from-prompt — ablate step + cut operand access; resolves whether the
  scale result is hidden re-derivation (monitorability loss) or benign recompute-from-prompt.
- Control B: probe-based state monitor (does a linear probe read the "hidden" channel?).
- Control C: bfloat16 7B via paged/offload + Qwen2.5-3B, so each axis has >2 points off the
  4-bit-deflated axis.
- Control D: natural word problems (operands not trivially present as clean prompt tokens).
- Secondary: zero/resample-ablation comparison to harden Section 5 against mean-ablation OOD; multi-seed.
