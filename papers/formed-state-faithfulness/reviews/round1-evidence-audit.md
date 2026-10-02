# Round-1 evidence audit — Formed-State Faithfulness

Auditor pass 2026-10-02. Read-only except this file. Sources: `EXP = saturn/experiments/2026-10-02-cot-formed-state-faithfulness`
(FINDINGS-draft.md, PREREG.md, FROZEN.json, results/analysis-summary.json, raw results/*/report.json),
`research/papers/custody-audit-2026-10-02.md`, `saturn/experiments/2026-08-21-ird-fruit-battery/README.md`,
E10 rerun, qwen-alias-binding-feedback, mvm-mamba-cot. Common-subset + re-verbalization contrasts recomputed from raw rows.

## Verdict
**CUSTODY CLEAN.** ~67 numeric claims checked (>45 target): all MATCH or ROUNDING. Zero MISMATCH, UNSOURCED,
WRONG-CONDITION, or SUPERSEDED-as-positive in the **paper body**. Every point estimate traces to the final
post-bugfix full runs; all six custody-audit corrections are incorporated in paper.md. One real new finding:
the **README abstract** uses a discounted free-running number (11%) as a headline without its caveat (the paper
abstract does not). Rest are minor transparency notes.

## Recomputed from raw report.json rows (independent)
| Contrast | Paper | Recomputed | Class |
|---|---|---|---|
| per-arm repair n/rate (6 arms) | 32/.188, 32/.188, 21/.762, 29/.828, 24/.292, 22/.727 | identical | MATCH |
| bf16 common 0.5B→1.5B, n=21 | 0.095 → 0.762 | 2/21=0.0952 → 16/21=0.7619 | MATCH |
| nf4 common 1.5B→7B, n=17 | 0.353 → 0.824 | 6/17=0.3529 → 14/17=0.8235 | MATCH |
| all-six common, n=11 | 0.091/0.818/0.273/0.818 | 1/11/9/11/3/11/9/11 = 0.0909/0.8182/0.2727/0.8182 | MATCH |
| re-verbalize among changed (5 arms) | 21/32,20/21,29/29,21/21,14/21 | 21/32,20/21,29/29,21/21,14/21 | MATCH |

## Classification by section (representative; all verified items)
| Claim | Source | Class |
|---|---|---|
| Abs/§4.2 state-only 1.00 @0.5B/1.5B (bf16,fp32,NF4); 0.955 @7B [.864,1] | analysis monitor_blind_change_rate | MATCH |
| Abs/§4.3 re-verbalize 0.66–1.00 | raw rows (0.656→1.00) | MATCH (ROUNDING) |
| Abs/§5 repair 0.19→0.76 bf16; 0.29→0.73 NF4 | repair_rate | MATCH |
| §2.5/App copied canary 1.00 n=8; 7B 6/6 (n=7 adm) | copied_unmount_changed | MATCH |
| §2.5 early 0.00 / late 1.00 n=8 | multi_early/late | MATCH |
| §2.4 remount Δmax=0.0 all runs incl NF4 | remount_delta_max | MATCH |
| §3 plain −0.54 / chain +2.40 (1.7B) | IRD F1-R (measured) | MATCH |
| §3 ×4 fam 8.02/0.94, 9.23/0.88, 14.18/0.53, 11.59/1.64; 30B −1.09/+5.82 | IRD F3-R (MEASURED, receipts) | MATCH |
| Tbl1 monitor-blind + text-visible 1.00; 7B 0.955 | analysis | MATCH |
| Tbl2 repair + removal-wrong (6 arms) | analysis | MATCH |
| §4.5 donor 0.594/0.810/1.00/0.818 + CIs | swap_cf_authored | MATCH |
| §5.4/5.5 fp32 null d=0.066; NF4 d=0.47; 0.47<0.57 | analysis | MATCH |
| Tbl3 free 1.5B .222/.778/.111/1.0/8-9; 7B .5/.444/.222/1.0/5-9 | analysis free.* | MATCH |
| Fig2 (redrawn) bf16 line .19/.76, NF4 dashed .29/.73, fp32 diamonds, 7B=NF4 labeled | viewed PNG vs analysis | MATCH (fixes custody#6) |
| Fig3/Fig4 captions | analysis | MATCH |
| App A E10 19/32, 30/30, 26/32, 3/30 | E10-rerun FINDINGS | MATCH |
| App A alias-binding 3/3 eligible, block 2/3 | alias-binding FINDINGS | MATCH |
| App A MVM copied-necessity 0.84 | mvm-mamba-cot FINDINGS | MATCH |
| 7B base_native_correct 0.955 (1/22 wrong) | base_native_correct | MATCH |
| VRAM 15.2/15.9/14.6 GB | no artifact — labeled "asserted" App D | ASSERTED (correctly labeled) |

## Citation spot-check (WebSearch, 3 of 9)
- 2507.11473 Korbak et al. "Chain of Thought Monitorability…" — VERIFIED (title/ID/authors).
- 2503.11926 Baker et al. "Monitoring Reasoning Models for Misbehavior…" — VERIFIED (authors Baker/Huizinga/Gao/Dou/Guan/Madry/Zaremba/Pachocki/Farhi match).
- 2404.15758 Pfau/Merrill/Bowman "Let's Think Dot by Dot…" — VERIFIED (title/ID/authors; §8 filler-token characterization accurate).
README's "9 arXiv IDs web-verified" is credible on this sample.

## Superseded / discounted-number discipline
- **MVM −0.015** (non-copied step "robust") — NOT used; paper labels it "superseded as a restatement artifact." CLEAN.
- **E10 path-distributed / strict time-circuit** — explicitly disclaimed twice (§8, §9): "does not make the distributed-circuit claim." CLEAN.
- **15/32** — not present anywhere in paper.md. CLEAN.
- **Old 14-token parser 32/32 / 30/30** — superseded by conservative readout; paper uses 26/32, 3/30 instead. CLEAN.
- **Discounted free numbers as headline** — paper abstract is clean; BUT README abstract uses 11% (see Fix 1).

## Minor transparency notes (source-faithful, not errors)
- 1.5B NF4 denominators differ by metric: monitor-blind n=21, text-visible n=23, repair n=24 (Tbl1 vs Tbl2). Faithful to source but unexplained in text.
- 7B free `ablate_answer_changed` tuple n=8 in analysis-summary vs Table 3 header n=9 (source inconsistency carried through; rate 0.500 unaffected).
- FROZEN.json mutated post-freeze (sha 3b3c22→03d207→89fd78); additive, disclosed App D; PREREG.md is the real registration. Acceptable.

## TOP-10 FIXES (priority order)
1. **README.md abstract (line 28):** the "regenerated text announces the removal only 11% of the time" is the 1.5B *free* arm, which the final paper discounts (no-op 8/9=0.889 < 0.90). Add "exploratory/discounted" qualifier or drop from the abstract — it is a discounted number in a headline slot (paper.md abstract correctly omits it).
2. **Table 1 / Table 2 n mismatch for 1.5B NF4 (21 vs 24):** add a one-line note that the dissociation denominator (valid 2×2 cells) is smaller than the repair denominator, so readers don't read it as an inconsistency.
3. **Table 3 7B n:** reconcile header n=9 with the analysis `ablate_answer_changed` n=8 (footnote the one unscored item).
4. **§3 provenance:** the ×4-family token-visible numbers are from the private August IRD battery (different task, code-trace) and Qwen3-30B — measured with receipts, and Appendix A lists the path; consider stating inline in §3 that these are a supporting prior battery, not this experiment's runs, so §3 isn't misread as part of the pre-registered panel.
5. **§4.1 text-only cell:** `text_wrong_state_orig_change_rate` (0.47 @0.5B bf16, 0.56 @0.5B fp32, 0 at 1.5B+) is defined but never reported; either report it or drop the cell from §4.1 to avoid an unused definition.
6. **Fig2 caption vs file:** caption says "float32 diamonds overlap the bfloat16 line" — the 1.5B fp32 diamond is at 0.83, visibly above the 0.76 bf16 point in the PNG; soften "overlap" to "sit on/near" for 1.5B.
7. **Appendix C E3 row:** mark the swap-falsifier-refuted result as from the discounted panel (it currently reads as a clean refutation; body §6.2 hedges it, the table should too).
8. **VRAM figures:** already labeled asserted in App D — also add the "asserted" tag at first mention in §2.2 (currently only the appendix carries the caveat).
9. **README status line:** says "custody audit in progress" / "custody-audit corrections applied" in different places; the audit is complete — make the status consistent.
10. **Fig1 supersession:** README notes primary `fig1_repair_vs_scale.png` is superseded by the redrawn fig2; confirm the stale `fig1` is not referenced elsewhere (it is not in paper.md; housekeeping only).
