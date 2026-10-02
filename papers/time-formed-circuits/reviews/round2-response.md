# Round-2 response (point-by-point)

Author response to the three round-2 reviews (interp 6/10, evidence audit, prior-art/clarity). "Done" means the change is in `paper.md`/`README.md` now; "Decision" means a reasoned choice. References are to the revised manuscript.

## A. Interpretability reviewer (round2-interp-reviewer.md) — top-5 + fresh attacks

| # | Item | Action | Location |
|---|---|---|---|
| 1 / F1 | "Formation" overclaims given the 77/23 split and the 0.197 prereg miss; drop the "pure propagation predicts early ≈ late" null; scope the model claim | Done, and strengthened by the landed Gemma replication (job-d37efcecae3e). §3.5 reports both models: the two fitting-free legs (late ≫ seed/early K/V; late not a linear image of the seed) replicate in Qwen (late 0.871) and Gemma (late 0.985). The construction leg is unsupported in **both** models: Qwen misses the 0.20 bar at 0.197 (77% survives the freeze) and Gemma's freeze is a no-op (0.990 vs 0.985), firing the preregistered freeze-no-op falsifier. The scoped conclusion no longer says "construction," only "assembled into the late band and not read off the source." §11 matches; abstract and intro make no construction claim and needed no walk-back. | §3.5, §11, Fig 3 |
| 2 / F2 | §5 identity miss is an out-of-basis artifact of MLP transcoders; state the mechanism first, scope the title, report the magnitude asymmetry, add the n=12 CI | Done. Retitled "An MLP-transcoder feature basis cannot reach the formed identity store on Gemma-2-2B." A new second paragraph states up front that transcoders replace the MLP sublayers, attention is not decomposed, so an attention-formed store is out of basis by construction. Added a two-caution paragraph: the native cut and the feature operator are not magnitude-matched, and n=12 gives a wide interval read as "far below native," not a point. The scoped conclusion bounds the claim to MLP-transcoder circuits and names an attention-inclusive operator as the settling test. | §5 |
| 3 / F4 | Custody statement contradicts the record ("in progress" vs PASS/FROZEN) | Done. The P1 custody audit passed; App A states the audit passed with byte-identical frozen predictions, and the README "may be revised" hedge is removed. | App A, README |
| 4 / F6 | Add ≥2 seeds or state the single-seed limitation adjacent to Table 2 | Done (state). A paragraph after Table 2 explains the interventions are deterministic (frozen weights, greedy decoding, fixed cache edits reproduce logits exactly), the variance that matters is across items/identities (captured by the clustered intervals and the held-out set), and multiple pretraining seeds are unavailable for these public checkpoints, so pretraining-seed robustness is a stated limitation. | §3.4, §10 |
| 5 / F5 | Color feature-only number inconsistency (0.42 / 0.36 / 0.313); identity 0.08 vs 0.044 | Done. One value per declared scope: feature-only all-position color ≈ 0.36 and identity ≤ 0.08; the subject-position all-layer peak is 0.42 (identity 0.08); the library-reproduction value is 0.313 vs 0.344. The old standalone feature-only figure (which labeled 0.42 as all-position) was merged into Fig 4, removing the mislabel. | §5, Fig 4 |
| F3 | Novelty is in operators; add a Meng/Hase delta row; cite resample-ablation lineage at the transplant | Done. Added a Source-localization delta row (Meng restoration sites; Hase localization ≠ edit site) to the §9 table, and a sentence naming the transplant as an interchange intervention / resample patching with a chosen source and target. | §9 |

## B. Evidence audit (round2-evidence-audit.md)

| # | Item | Action | Location |
|---|---|---|---|
| MISMATCH | §3.4 "three of four" wrong-identity CIs include zero; the record shows all four | Done. Changed to "includes zero in all four cells." | §3.4 |
| IMPRECISE | Matched f+e identity "0.31" is all-position; subject+later is 0.29 | Done. Both are stated with their scopes: "0.31 over every position and layer, 0.29 over the subject and later positions." | §5 |
| IMPRECISE | Fig 5 caption labeled 0.42 as all-position | Done by removal: that figure was merged into Fig 4; the color scopes are now labeled in text. | §5 |
| Carryover | [Geiger 2023] 2301.04709 unverified | Decision/Done. WebSearch-confirmed in round 1 (Geiger, Ibeling, Zur et al.); reference carries authors. | References |

All other audited numbers were MATCH/ROUNDING and are unchanged; no smoke/killed/cancelled number reached the body.

## C. Prior-art and clarity (round2-priorart-clarity.md) — top-5

| # | Item | Action | Location |
|---|---|---|---|
| 1 | Cite Vig 2020 (causal mediation), Olsson 2022 (induction), Feng & Steinhardt 2023 (entity binding) | Done. Vig 2020 credited as the mediation-analysis ancestor in §9; Olsson 2022 cited at the induction control (§7.2); Feng & Steinhardt 2023 placed in §9 distinguishing the formed-store account from binding-ID representations. | §7.2, §9, References |
| 2 | Fix Fig 2 caption (three vs four groups; unplotted earlier-band clause; clustered error bars) | Done. Fig 2 was regenerated with identity-clustered 95% intervals; the caption says Qwen is shown on development and held-out sets, drops the earlier-band clause, and labels the bars identity-clustered. | Fig 2 |
| 3 | Cut to 12-14pp: §8 → summary + Appendix A; §6.2/§7.1 detail → appendix; merge Fig 5 into Fig 6; demote Fig 3 and Fig 8 | Done. §8 compressed to two paragraphs (two-step chain and the SmolLM2 sweep moved to Appendix A); §7.1 Mamba dose enumeration compressed with the detail in Appendix A and Fig S2; the feature-only Gemma figure merged into Fig 4; window-necessity and Mamba figures demoted to Appendix D (Figs S1, S2). Main body now has five figures. | §7.1, §8, App A, App D, figures |
| 4 | Split the worst 68-98-word sentences | Done. Split the §3.5 mid-freeze, §5 identity-conclusion, §8, and §9 self-repair sentences into one-claim sentences; §8 rewrite also removed the longest chain sentence. | §3.5, §5, §8, §9 |
| 5 | Name the transplant as an interchange intervention (Geiger lineage) | Done. See F3 above. | §9 |

Hedging and body jargon were measured clean by the reviewer and were not touched. Abstract is 200 words.

## D. Still open

- `TODO 9B scale`: a 7-9B block-and-rescue replication; the strict signature and mediation remain at or below 4B, and Qwen3-30B's in-forward certificate did not survive the isolated cut.
- An attention-inclusive operator for the §5 coverage claim; a FLUX threshold-sensitivity curve (nice-to-have).
