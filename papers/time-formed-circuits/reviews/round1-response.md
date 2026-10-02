# Round-1 response (point-by-point)

Author response to the three round-1 reviews. "Done" means the change is in `paper.md`/`README.md` now; "RUNNING" means a placeholder marks a result in flight; "Decision" means a reasoned choice not to change. Line/section references are to the revised manuscript.

## A. Evidence audit (round1-evidence-audit.md) — 2 mismatches, 8 tightenings

| # | Item | Action | Location |
|---|---|---|---|
| B | "ALL language-model interventions use stock eager" false for §8 (SDPA) | Done. Split the claim: store/mediation/read/sweep = eager; §8 arithmetic = stock SDPA; both outside the wrapper defect | §10 (final para), App C |
| A | App A E11 model mislabeled Qwen2.5-1.5B; source is SmolLM2-1.7B (24 layers, n=45, peak L17 0.35) | Done. Corrected App A row and named SmolLM2-1.7B in §8 body; added "at L17" | §8, App A |
| C/#36 | §5 graph-top identity range should be −0.03 to −0.14 (−0.19 is color) | Done. "move the identity answer away by −0.03 to −0.14, and the color answer by up to −0.19" | §5 |
| G | Verify Geiger 2023 arXiv:2301.04709 | Done. WebSearch-confirmed: Geiger, Ibeling, Zur et al., "Causal Abstraction: A Theoretical Foundation for Mechanistic Interpretability," arXiv:2301.04709. Reference updated with authors | References |
| D/#29 | §4 "within 0.03 of clean" needs forced-choice qualifier | Done. "recovers the behavior on a forced choice over the candidate tokens to within 0.03 of clean," plus the record's caveats (forced-choice, not full-vocabulary; exact-beats-soft untested) | §4 |
| E/#49 | §7.2 "0.18 per layer" imprecise | Done. Reworded: "no single layer carries more than 0.08 of necessity and no three adjacent layers more than 0.23" | §7.2 |
| F/#35 | §5 color 0.31–0.42 tied to the wrong condition | Done. 0.31–0.42 attributed to the subject-position, all-layer swap; every-position, all-layer stated as about 0.32–0.34 | §5 |
| H/#30 | §4 coreference 0.00 not clearly sourced | Done. Dropped "coreference"; now "the semantic identity and color panels at rate 0.00," which the E18 record supports | §4 |
| #46 | §7.1 "0.87 to 0.83" not in summary.json | Done. Dropped the untraceable number; kept the sourced claim (surviving-state fraction falls; margin positive in 3/6) | §7.1 |
| #53 | §8 "0.037/0.015" are un-rounded | Done. Changed to "about 0.04 and 0.02 nats" to match the published table | §8 |

Retraction guards (auditor confirmed all hold) are unchanged: no retracted result (E5 Mamba certificate, 30B in-forward, interchange-only necessity) is used as positive evidence; §8 uses 19/32 and 26/32, not 15/32.

## B. Interpretability reviewer (round1-interp-reviewer.md)

| Item | Action | Location |
|---|---|---|
| Formation vs propagation (biggest attack) | RUNNING + Done-in-text. Stated as an explicit open question with the discriminating test (seed-layer vs late-band transplant; late band must beat a linear image of the seed). Until it lands, "formation" is labeled as the measured interval and endpoint, not a construction claim | §3.5, `<!-- TODO P1-A -->` |
| Statistics: item bootstrap over 42 correlated rows is anti-conservative; cluster at identity level | Done + RUNNING. Added the identity-clustered sensitivity interval for the original panel (block [0.732,1.075], rescue [0.835,0.894]) and stated why the item bootstrap overshoots one; cross-family clustered re-estimate marked pending | §3.3, `<!-- TODO P1-B -->` |
| E6 fairness: interchange holds error nodes clean, so "features can't move it" is near-tautological; a fair operator swaps error nodes | Done + RUNNING. Added an explicit fairness-limit paragraph tying it to Marks 2024, and the fully-matched error-node swap is marked in flight with the honest alternative conclusion pre-stated | §5, `<!-- TODO P1-C -->` |
| §5 title overclaims | Done. Retitled "An attribution-graph feature basis misses the formed store on Gemma-2-2B" | §5 heading |
| Four-quadrant buys little; threshold-dependent (0.913 vs 0.90; single call 0.562) | Done. Explicitly de-risked: presented as a support-profile observation, not a mechanism or the central result; threshold narrowness stated; the paper now says the block-and-rescue dissociation is the central result | §6.3, §11 |
| Scale/30B deserves prominence, not a footnote | Done. Scale is now the lead limitation; 30B isolated-cut failure is foregrounded | §10 |
| Isolated cut = patching hygiene; cite Zhang & Nanda / Heimersheim & Nanda | Done. Added both, framed as patch-placement hygiene with the 0.985-vs-0.009 consequence; added Conmy 2023 | §9 |
| Delta vs Geva/Agarwal is buried | Done. Added a quantified per-stage delta table | §9 |
| Fig 3 orphaned | Done. Cut the layer-profiles figure; replaced with the source-to-consumer schematic as Fig 1 | figures/, §1 |
| Fig 5 caption does not match the grouped-by-behavior figure | Done. Rewrote the caption to describe bars grouped by identity/color | §5 (now Fig 4) |
| "space circuit"/"time-formed" under-motivated | Done. "time" disambiguated in sentence 1 of §2; "space circuit" defined once in §2.3 | §2, §2.3 |
| "genuinely distributed" true only at layer grain | Done (already). Text says "distributed at the layer grain"; limitation restates the sub-layer caveat | §3.2, §10 |
| New category will not clear a main venue | Decision. We do not claim a new phenomenon; the contribution is the operator set and the dissociation. Abstract and §9 now foreground the delta, not a taxonomy | abstract, §9 |
| Three mind-changing experiments (A/B/C) | RUNNING. A = P1-A, B = P1-B, C = P1-C; all three are marked and their designs stated in the body |  |

## C. Prior-art + clarity (round1-priorart-clarity.md)

| Item | Action | Location |
|---|---|---|
| Chughtai, Cooney & Nanda 2024 (2402.07321) — additive motif; most damaging omission | Done. Cited and tied explicitly to the "`y=(x1+…+xn)/n` passes all four conditions" caveat | §2.3, §6.3, References |
| Sharma 2024 (2404.03646) — Mamba ROME; section cited zero Mamba interp | Done. Cited in the Mamba section | §7.1, References |
| Wang 2022 IOI (2211.00593) — canonical distributed-but-locatable circuit | Done. Cited as the analogue for the Pythia-70M control | §7.2, References |
| Marks 2024 Sparse Feature Circuits (2403.19647) — error nodes central to §5 | Done. Cited; error nodes framed as first-class carriers; WebSearch-verified ID | §5, References |
| Dunefsky 2024 transcoders (2406.11944) | Done. Cited at the interchange operator definition | §5, References |
| Lindsey 2025 Biology of an LLM | Done. Cited alongside the attribution-graph methods | §9, References |
| Basu 2023 (2310.13730) + Localizing Knowledge in DiT (2505.18832) | Done. Cited for the diffusion-distributed-vs-LM observation that anticipates our split | §6.3, References |
| "time-formed" collides with token-time | Done. Sentence 1 of §2 defines "time"/"temporal" as the ordered execution axis (depth/denoising/recurrence), not token position. Name kept, hard-disambiguated | §2 |
| Lead abstract/intro with block/rescue + 83%-vs-0.08 | Done. Adopted a merged ≤200-word abstract (192 words) leading with block/rescue, then the tool-miss | abstract, §1 contributions |
| Add the source→formation→commit→store→consumer schematic | Done. New Fig 1 | figures/fig1-schematic.png, §1 |
| Define "admitted rows" and "seed gain" inline | Done. Both defined at first substantive use | §3.3 |
| Define "filler state" | Done. Glossed at first use | §3.2 |
| Fig 2 third panel reads as a separate chart | Done. Caption labels the Gemma sliding/global set as a third inset panel | §3.2 (Fig 3) |
| Demote §8 | Done. Compressed from four paragraphs to three, with per-item detail pushed to Appendix A | §8 |
| Promote §5 | Decision (partial). §5 is sharpened and foregrounded in the abstract and §1 contributions, but kept after §3–4 because the formed store must be defined before showing tools miss it. Happy to reorder if the venue prefers |  |
| Footnote the Falcon-H1 hybrid | Done. Kept only as a terse boundary row in Table 4; no separate prose | §7 |
| Cross-reference companion Paper 2 and remove duplication | Done. §11 cross-references `../time-circuit-scaffold/paper.md`, assigns per-fact invariance / variance decomposition / query-selective authority to Paper 2, and removes the "input-invariant depth" claim this paper had strayed into | §11 |

## D. Not changed, with rationale

- **"authors" (verb)** is left unglossed; its meaning (the state causes the model to output that token) is clear in every use and a definition would add noise. Flag if a reviewer still trips on it.
- **Physical section reorder to promote §5** not done (see C above); foregrounding was done instead.
- **Falcon-H1** retained as a boundary row rather than cut, because it is the one hybrid specimen and marks where the anatomy is not yet established.
