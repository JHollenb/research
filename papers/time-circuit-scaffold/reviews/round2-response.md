# Round-2 response

Point-by-point response to the three round-2 reviews (`round2-interp-reviewer.md` 6/10,
`round2-evidence-audit.md`, `round2-priorart-clarity.md`). Write scope: `paper.md`, `README.md`,
`figures/`, this file. No other file edited; no commit.

## Highest-priority: confirm-color landed; abstract and framing rewritten

The preregistered confirmatory retest has landed and is now folded into every pending mention.
On fresh colors (disjoint from Phase-2), with all three locators and the pass rule frozen in
advance, no cell fires in either family: Qwen 48 items / 27 colors — S1 2.84, S2 1.44, S3 1.76;
Gemma 106 items / 54 colors — S1 3.44, S2 0.90, S3 0.97. The Phase-2 Qwen-color firing does not
reproduce. The invariance therefore no longer rests on a post-hoc locator, and the abstract,
title framing, §1, §3, §5, §13, Fig 5 caption, Appendix A, and Appendix C now say so, while
keeping the Phase-2 frozen firing (2/6 cells) disclosed.

Honesty items carried verbatim: Qwen covers only 27 colors (short of the frozen ≥40 — single-token
filter dropped 14, 36 items failed read-back) = a deviation; the Gemma run used a post-freeze
subject-chunking change, numerics-neutral to ~2e-5 nats (custody PASS); the Gemma identity canary's
argmax S1 still fires (4.06) with commit SD 0.00 (the anticipated plateau artifact); freeze is
file-mtime only. Source `FINDINGS-confirm.md`, `results/confirm_fal3_analysis.json`
(job-8b550b584da4 Qwen, job-b7d05acf8192 Gemma).

## Interpretability reviewer (6/10)

| Must-fix | Action |
|---|---|
| 1. Title + headline invariance rest on a post-hoc locator; confirm-color half-landed | **Done.** Both halves landed (Qwen + Gemma, all three locators frozen, none fire). Title kept; abstract/§1/§3/§5/§13 now gate the "does not move" claim on the retest, not the commit locator alone. |
| 2. Fig 5 F2C contradicts the corrected §5 text | **Done.** F2C regenerated from results: per cell it plots the frozen argmax S1 and the commit S2 for Phase-2 **and** the confirm run, threshold line at 4, fired bars flagged. The "FAL-3 threshold" mislabel against the 4.17 commit SD and the "2 weak-signal facts" annotation are gone; the frozen argmax (fired 2/6) is now the plotted statistic. |
| 3. Scope the null to "learned," not "scaffold vs any competent net" | **Done.** The incompetence bound (top-1 0/96) now appears in the abstract, not only §5; abstract and §13 state the control shows learned, not scaffold-versus-any-competent-net. (A competent different-seed/different-task control is named as the open gap in §12/§5.) |
| 4. Pre-commit one primary statistic per falsifier; report FAL-2a Gemma firing in the abstract tally | **Partly.** The confirm retest froze the pass rule as S2 ≤ 4 **and** S3 ≤ 4 (commit + necessity primary), reported in §5 and Appendix C; FAL-2a Gemma firing stays disclosed in §5 (the ≤220-word abstract keeps the falsifier tally to one clause). |
| 5. Compress §10 and add Stoehr 2024 | **Done.** §10 trimmed to the diffusion wrong-source control, the XNOR inversion (148/150), and the frozen-site wrong-site control; the archive-page read and the fork/replay result moved to Appendix D. Stoehr et al. 2024 cited in §6. |

## Evidence audit

| Item | Action |
|---|---|
| Confirmatory run "in progress" is STALE (it landed) | **Done.** All six "in progress/underway/pending" mentions rewritten to the landed result. |
| Appendix A missing rows for Figures A/B/C + confirm | **Done.** Added rows for the read-site null (job-48af2d6fc73c), attention-type swap (job-0b7652b2112d), function-vector test (job-5d7cf4e4b3d8), and the confirm retest (job-8b550b584da4 / job-b7d05acf8192), with smoke IDs. |
| "40 fresh countries across two templates" | **Done.** → "20 countries across two templates (40 facts)" in §5; README matched. |
| Appendix A "32 same-parent query pairs" vs §4 "16/op … 128 checks" | **Done.** Appendix A row now reads "16 contrasts per operation; 128 directional pairing checks." |
| §11 "SD 0.00 across 42 Gemma facts" without locator | **Done.** Labelled "under the commit locator" (and notes the retest holds under all three). |
| "eleven" vs 19.0 are different ratios | **Done.** One-clause clarification added in §5 (19.0 = coord×op / coord×fact on the 4-lexical-set design; eleven-to-one pools the binding term). |
| "57–97 MAE" not located in cited source | **Located.** It is blog `2026-09-30-165158` line 153 ("Wrong-source and wrong-sign controls diverged by 57–97 MAE"), on the 0–255 RGB scale (scene-editing.md defines the scale). §7, §10, and Appendix A now cite it with the unit; the non-existent `2026-09-02-071815` control-blog reference is removed. |

## Prior-art / clarity / companion split

| Item | Action |
|---|---|
| Agarwal 2026 under-positioned; same-layer-vs-relation-before-entity tension | **Done.** Agarwal gets its own delta sentence in §11 (per-fact causal invariance vs cross-type ordering) and an explicit reconciliation after Table 1 in §5 (different quantities, different positions). |
| Add Merullo 2024 (circuit reuse) to §4 | **Done.** Cited in §4 (reader reuse) with the delta (signed per-coordinate split vs qualitative reuse) and in §11 ¶3. |
| Add Stoehr 2024 to §6 | **Done.** |
| Companion duplication: attention-type-swap control | **Resolved for this paper.** The type-swap control is owned here (§3 + Figure B, job-0b7652b2112d). Paper 1's one-line pointer is left to the coordinator. |
| Companion duplication: Mamba clock-dose job IDs | **Done.** §3/§7 cite the companion for clock-dose; the Appendix A clock-dose row reads "(see companion)" with no job IDs. |
| Cut to 12–14 pp | **Done (partial).** §10 compressed; reviewer-control Figures A and B moved to Appendix D; §3 companion summary cut to two sentences; §13 cut ~40% and ends on the interpretation consequence; abstract ends on the attribution result, not a caveat; §7 hedges trimmed; reviewer-control captions shortened. |
| Delete line-103 TODO comment | **Done.** No `<!-- -->` comments remain in `paper.md`. |

## Still open (named in the paper)

- A behaviorally competent null (different-seed or different-task trained net of identical
  shape) is not yet run; the paper bounds the learned-split claim accordingly.
- Long-context attention-type causality is untested (Gemma-3 unavailable); §3 says so.
- The parked chain-of-thought result (state-only K/V swap controls the answer while the step
  token is unchanged) is folded as one in-preparation sentence in §10.
