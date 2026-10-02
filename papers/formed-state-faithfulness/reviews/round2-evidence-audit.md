# Round-2 evidence audit — formed-state-faithfulness/paper.md

Auditor pass 2026-10-02. Read-only on `paper.md`. Every number in the abstract, tables, figure
captions and body traced to `saturn/experiments/2026-10-02-cot-formed-state-faithfulness/`
(`FINDINGS-draft.md`, `FINDINGS-addendum-2-draft.md`, `PAPER-SECTION.md`, `results/*/report.json`,
`results/analysis-summary.json`, `results/analysis-addendum-summary.json`, `FROZEN*.json`) and the
custody audit `research/papers/custody-audit-2026-10-02.md` (CoT + CoT addendum-2 sections). Figures
opened and checked against the numbers. Raw report fields spot-recomputed where load-bearing.

Verdict: **numbers are overwhelmingly custody-clean and trace to FINAL full post-bugfix runs.** One
real sourcing defect (3B text-visible), a few provenance/wording flags, several round-1 custody
issues now confirmed FIXED. No number in the paper is drawn from the cancelled job (job-366e400ba3aa)
or from a smoke/killed run.

## Claim | line | source | status

| Claim | Paper line | Source | Status |
|---|---|---|---|
| State-only 1.00 @0.5B bf16/fp32, 1.5B bf16/fp32/NF4; 0.955 @7B; n=32/32/21/29/21/32/22 | Table 1, L108-116 | analysis-summary.json teacher monitor_blind_change_rate; 7B job-bc10cd445816 dissoc 0.9545 n22 | MATCH |
| State-only 1.00 @3B (base) bf16, n=32 | Table 1, L115 | addendum qwen3 `swap_changed`=1.0 n32 (job-52b8771fc5ef) | MATCH (cross-worker; see F2) |
| **Text-visible 1.00 @3B (base)** | Table 1, L115; also "1.00 everywhere" L120; App C L248 | **none — 3B control report has NO text_visible field; dissoc panel never ran 3B** | **UNSOURCED (MF1)** |
| Text-visible 1.00 all other rows | Table 1 | analysis-summary text_visible_change_rate (0.5B/1.5B all; 7B job dissoc 1.0) | MATCH |
| Text-only cell 0.47/0.56/0.00/0.10 (0.5B bf16/fp32; 1.5B all; 7B) | L100 | text_wrong_state_orig_rate 0.469/0.5625/0.0/0.0952 | MATCH |
| Pre-registered E2 bar ≥0.30 met; falsifier (CI incl 0) not fired | L104 | FROZEN.json E2_monitor_blind | MATCH (prereg named 1.5B+7B; 0.5B/3B are extra — minor framing) |
| Re-verbalization 21/32, 20/21, 29/29, 21/21, 14/21 (0.66/0.95/1.00/1.00/0.67) | L124, Fig3 | custody-audit CoT §ISSUES-1 (measured from dissoc rows) | MATCH |
| Donor swap 0.59[.41,.75]n32 / 0.81[.62,.95]n21 / 1.00[1,1]n29 / 0.82[.64,.96]n22 | L132 | swap_cf_authored 0.594/0.810/1.0/0.818 + CIs | MATCH |
| Probe swap-recall 0.19/0.19/0.00 vs 0.70 bar | L140, Fig4 | addendum swap_decode_mistake_recall 0.1875/0.1905/0.0 | MATCH |
| Loose flag 0.84/0.81/0.97; base-decode 0.44/0.28/0.095 vs chance 0.05/0.05/0.062 | L142 | swap_flag_recall; base_decode_acc; chance_decode | MATCH |
| Table 2 R1 0.188/0.762/0.531; R2 0.000/0.000/0.031; R3 1.0/0.571/1.0; R4 0.156/0.450; tracks-orig 0.000/0.000; R4s 1.0/0.952 | Table 2 L172-174 | addendum qwen05/qwen15/qwen3 fields | MATCH |
| R4 0.450 misses R1−0.15=0.612; 1.5B partial | L176 | addendum controlAprime_verdict | MATCH |
| Non-monotone 0.188/0.762/0.531 | L180 | R1 control runs | MATCH |
| tracks-original never reproduced (0.5B,1.5B only) | Abstract L20, L34, L176, L184 | resample_tracks_old 0.0 (0.5B,1.5B); 3B no resample arm | MATCH (correctly scoped; custody flagged the over-scoped PAPER-SECTION wording — paper fixed it) |
| Free: no-op 8/9 @1.5B, 5/9 @7B; ablate-correct 7/9 @1.5B; swap 100%+reverb 100% | L190, Fig F1 | analysis-summary free | MATCH |
| Both free arms discounted (0.90 threshold) | L190, App F | FROZEN free_noop_min=0.9; 1.5B=0.889<0.9 | MATCH — custody CoT ISSUE-2 now FIXED (both discounted) |
| App F table (1.5B/7B free rates; 7B ablate over 8) | App F L274-277 | analysis-summary free (ablate_answer_changed n8 @7B) | MATCH |
| App G 0.188=0.188; 0.762 vs 0.828; NF4 0.292 vs 0.762 | L285 | repair_rate fp32/bf16/nf4 | MATCH |
| Canaries: remount |Δ|max 0.0; copied 1.00 (7B 6/6 over 7); early/late 0.00/1.00; mask-id 1.0 | L68, App B L240 | report remount_delta_max=0.0; copied n=7/flip n=6 @7B; mask_identity_ok=1.0 (verified 3B ctrl) | MATCH — custody ISSUE-4 (7B copied n) FIXED |
| Fig2 VM trace: L20 necessity 0.274; band L20-22; visible 3.38 / hidden 3.76; zero-page −3.04; no-op 0.0 | L76, L80, Fig2, App A | vm-trace-visualizer job-e034c77db8d6 (0.2738/3.3827/3.76/−3.0433) | MATCH (source is a DIFFERENT experiment dir, disclosed App A; outside custody audit — F4) |
| App E battery 8.02/0.94, 9.23/0.88, 14.18/0.53, 11.59/1.64, −1.09/+5.82, +2.40 | L90, L266 | ird-fruit-battery README (2026-08-21) | MATCH (prior battery; outside custody audit scope — F4) |
| 7B bf16 control pending; no claim rests on it | L56, L180, L259, App A | live job-050706578e6c (queued); cancelled job-366e400ba3aa NOT cited | MATCH (paper clean; see F3) |
| Fig G1 7B marked NF4 (not on bf16 line) | App G, Fig G1 | figG1 shows 7B on green NF4 axis + annotation | FIXED (custody CoT ISSUE-6) |

## Issues

**MF1 (must-fix). 3B text-visible = 1.00 is unsourced.** The only 3B run is the control
`job-52b8771fc5ef`; its report aggregate has no text-visible metric (keys: base_correct,
copied_step_mean_changed, mask_identity_ok, operandcut_*, remount_delta_max, repair_mean,
repair_zero, swap_changed). The dissociation panel never ran 3B. 3B state-only (1.00 = swap_changed)
is real; **3B text-visible (1.00) has no measurement**. Fix Table 1 L115 (mark n/a or "—"), and
soften "1.00 everywhere" (L120) and App C L248 "text-visible 1.00" which currently imply the 3B cell
was measured.

**F2 (flag). 3B state-only is from a different worker/metric.** 3B uses control-worker `swap_changed`
(job-52b8771fc5ef, worker 3b4db8d2, pre-resample) rather than the main panel's
`monitor_blind_change_rate`. Equivalent by definition and disclosed (App D worker rev), but add a
one-line note that the 3B dissociation point comes from the control run, not the main 2×2 panel.

**F3 (flag; source file, not paper). `FINDINGS-addendum-2-draft.md:36` still cites the CANCELLED
`job-366e400ba3aa`** as the pending 7B. The paper correctly uses live `job-050706578e6c` everywhere
(0 hits on the cancelled id). Fix the draft so a later promotion can't reintroduce the stale id.

**F4 (flag). Fig2 and App E numbers are from experiments OUTSIDE this audit's source set / custody
audit** (`2026-10-02-vm-trace-visualizer`, `2026-08-21-ird-fruit-battery`). Both verified against
their own source files and match; both are disclosed in App A/E as separate. No defect, but note they
are not custody-audited.

**F5 (minor). Fig F1 title** ("removal is silently repaired & unspoken") retains the pre-correction
framing that Section 7/8 explicitly retract (recompute-from-prompt). Caption is correct; retitle the
figure to avoid reading as a contradiction of the retraction.

**F6 (minor). "Note on n" (L118)** labels the 1.5B-NF4 repair denominator "(Section 7)". That repair
rate (0.292, n=24) is the Appendix-G precision-control value from the dissociation-panel job
`job-4a5981fa28fc`; Section 7's 1.5B row is bf16, n=21. n=24 is correct; the section label is off.

## Round-1 custody issues confirmed addressed in this draft
- Re-verbalization caveat added (Section 4.3, Fig3) — custody CoT ISSUE-1 FIXED.
- Both free arms discounted at 0.90 — custody CoT ISSUE-2 FIXED.
- 7B copied canary n footnoted (6/6 over 7) — custody CoT ISSUE-4 FIXED.
- Fig G1 7B styled as NF4, off the bf16 line — custody CoT ISSUE-6 FIXED.
- VRAM figures declared asserted (App D L261); the body carries no VRAM numbers.
- Probe prereg metric (0.19/0.19/0.00) vs post-hoc loose flag kept strictly separate — custody
  addendum-2 deviation handled.
- tracks_old scoped to 0.5B/1.5B (not "every scale") — custody addendum-2 overclaim fixed.
