# Round 2 review — prior-art positioning + clarity (frontier-lab reader lens)

Scope: read round1-priorart-clarity.md + round1-response.md first, then the full paper.md (381 lines, 10,525 words measured), README, round1-interp-reviewer.md, and all 8 figures. Read-only on paper.md. New citation IDs below are WebSearch-verified. Numbers labeled "measured" are from `wc`/`rg`/`awk` on the manuscript this session; page estimates are asserted (no venue template compiled).

## 0. Headline

Round 1's prior-art asks landed almost completely and well — this is now a strongly positioned paper against the exact literature a frontier reviewer polices. The remaining prior-art debt is three canonical ancestors the paper's own framing invites (causal mediation, induction heads, entity binding). Clarity is in good shape on the two axes people usually fail (hedging, lab jargon) — both measured clean — but has one real, quantified debt: sentence density. The document is over the 12–14pp target and needs ~1.5–2.5k words + 2–3 figures demoted.

## 1. Round-1 follow-through (verified in the current manuscript)

Every item in the task's required-comparison list is now cited and positioned. Measured verdicts:

| Required comparison | Cited? | Positioning quality |
|---|---|---|
| ROME / causal tracing (Meng 2022) | Yes (§9, refs) | Adequate. "restoration semantics" link stated; delta = isolated cut + transplant. |
| Geva 2023 (enrich→propagate→extract) | Yes | **Strong.** Per-stage delta table (§9) maps formation/commit/read onto it. |
| Hase 2023 (localization ≠ editing) | Yes | **Strong.** Paper offers formation/commit as a *mechanistic reason* for Hase's result — a genuine framing contribution, not just a cite. |
| Marks 2024 (sparse feature circuits / error nodes) | Yes (§5, §9) | **Strong.** P1-C matched feature+error interchange directly answers the error-node objection rather than conceding it. |
| Attribution graphs / circuit-tracer (Ameisen 2025) | Yes (+Hanna 2025 library, Lieberum 2024 Gemma Scope, Lindsey 2025 Biology) | **Strong.** §5 runs their actual published pipeline and operator. |
| Deferred commitment (Agarwal, 2609.17537) | Yes | **Strong.** In delta table; "commit" mapped to generation-controlling commitment. |
| Zhang & Nanda 2024 (patching best practice) | Yes (as "Zhang & Nanda 2023", 2309.16042) | Good. Isolated cut framed as patch-placement hygiene; 0.985-vs-0.009 is the payoff. |
| Heimersheim & Nanda 2024 (patching guide) | Yes (2404.15255) | Good. Paired with above. |

Also landed from round 1: Chughtai 2402.07321 (additive motif, tied to the four-condition caveat — the "most damaging" round-1 omission, now resolved), Sharma 2404.03646 (Mamba), Wang 2211.00593 (IOI analogue), Dunefsky 2406.11944, Basu 2310.13730 + Localizing-Knowledge-in-DiT 2505.18832, Conmy 2304.14997. Fig 5 caption now matches the grouped-by-behavior figure (verified against the PNG). Fig 3 is now referenced (Table 1 + §3.2) — the round-1 orphan is gone. No fabricated IDs found.

## 2. Remaining prior-art gaps (round-2, new — ranked)

**(a) Vig et al. 2020, "Causal Mediation Analysis for Interpreting Neural NLP," NeurIPS 2020, arXiv:2004.12265 — HIGH, credibility-level.** The paper's spine is causal mediation: the tag is `causal-mediation`, §3 is titled "Formation and **mediation**," the late band is repeatedly "the **mediator**," and block/rescue are necessity/sufficiency arms that map onto natural direct/indirect effects. Vig 2020 is the paper that introduced causal mediation analysis to transformer interpretability; omitting it while centering mediation reads as unawareness to this audience. Fix: one sentence in §9 crediting Vig 2020 (and, if desired, Pearl's natural direct/indirect effects) as the mediation-analysis ancestor, with the delta = native-state interfaces + the independent transplant rather than neuron/head-level mediation.

**(b) Olsson et al. 2022, "In-context Learning and Induction Heads," arXiv:2209.11895 — MEDIUM-HIGH.** "induction circuit" is a load-bearing, locally-decisive control (§7.2 Pythia-70M, §4 Qwen2.5-0.5B exact-join rescue) used without citing the canonical induction-heads paper. Wang 2022 (IOI) is cited as the "distributed-but-locatable" analogue, but IOI is not induction; Olsson is the exact lineage for the induction control itself. Fix: cite Olsson at first use of "induction circuit" (§4 or §7.2); keep Wang as the distributed-attention analogue.

**(c) Feng & Steinhardt 2023, "How do Language Models Bind Entities in Context?," ICLR 2024, arXiv:2310.17191 — MEDIUM, positioning opportunity.** The central experiment binds single-token animal identities to a subject position and shows the bound state is a transplantable formed store. "Binding IDs" are the closest cousin to "a formed identity store you can block and transplant," and a reviewer who works on entity tracking will ask. The matched-interchange finding (identity lives in attention-formed K/V, not features/error nodes) is also a natural dialogue with binding-ID representations. Fix: a clause in §3 or §9 distinguishing the formed-store account (a causal state you can cut/transplant across stages) from the binding-ID account (a representational scheme for which attribute binds to which entity).

**Lower priority / optional.** (i) The transplant *is* an interchange intervention / resample ablation; Geiger 2023 is cited for causal abstraction, but naming the transplant as an "interchange intervention" at first use would connect the method to that lineage in one word. (ii) Mamba-2 "state sink" (2606.00930) was suggested in round 1 and not added; optional, since Sharma 2404.03646 covers the Mamba-editing baseline the §7.1 claim needs.

## 3. Clarity

**Hedging: non-issue (measured).** Whole-paper hedge counts: "may" 1, "might" 1, "could" 3, "suggest" 1, "appears" 1; zero of "we believe / arguably / somewhat / potentially / likely / perhaps." The three "could" uses are precise scope statements, not fog. The paper errs confident-and-exact. No action.

**Lab jargon in body: contained (measured).** No "Saturn", "mrun", "job-…", "E20/E6/E11", or "P1-A/B/C" appears before Appendix A; experiment IDs and job IDs live only in Appendix A, paths only in Appendix A/C and refs. The round-1 ask is satisfied. Residual process-jargon in the body is small: §3.4 line 135 ("an **artifact-only verifier** passed six **custody and arithmetic gates**", "FP32 replay checks") reads as internal QA, not result — move that sentence to Appendix B/C. "preregistered threshold" (§3.5) is fine to keep.

**Sentence density: the real clarity debt (measured).** 60 sentences exceed 45 words; the worst genuine single sentences run 68–98 words and chain 2–4 distinct claims with semicolons and "…and… so… and…". Clear offenders to split (one claim per sentence):
- §3.5 line 145 (mid-freeze): "Zeroing the attention and MLP updates … lowers the transplant from 0.871 to 0.675 … so construction over those layers contributes to the store; the drop narrowly undershoots the preregistered threshold of 0.20 …" — three claims; split after "…contributes to the store."
- §5 line 177 (83 words): the "repeat the interchange swapping features and error nodes … adding the per-cell error difference where the tool adds feature decoder deltas; writing the clean values back changes the answer by zero, and our feature-only arm reproduces the library's interchange …" — split into method / validation.
- §8 line 252 (98 words), §9 line 271 (self-repair, 87 words), §11 line 293 (92 words), §3.4 line 133 (held-out, 68 words). These are comprehension taxes, not errors; splitting the top ~10 would materially improve a cold read and costs no content.

**One-claim-per-paragraph.** Mostly honored at paragraph grain (§3.3, §3.4 separate controls into their own paragraphs well). The violations are within-sentence, per above.

**Figure captions — self-contained but two mismatches to fix (verified against the PNGs):**
- **Fig 2 caption vs figure.** (i) Caption says "across **three** decoder families," but the figure has **four** column groups (Qwen2.5-1.5B appears twice: "published, same ids" and "held-out ids"). Reword to "three decoder families, with Qwen shown on both its development and held-out identity sets." (ii) Caption describes "a matched-width **earlier band** removes little," but no earlier-band bar is plotted (bars are seed gain, block, rescue, wrong-identity). Drop that clause from the caption or add the bar. (iii) Caption says "item-bootstrap intervals," but the paper's headline CIs are now identity-clustered (Table 2); state which the error bars are, and prefer the clustered ones for consistency with the text.
- Fig 1, 3, 4, 5, 7 captions are self-contained and match their panels. Fig 5/Fig 7 in-figure titles editorialize ("the formed store is invisible to the feature basis"; "strict path-distributed signature") — acceptable, but if a venue dislikes conclusions-in-titles, neutralize to the quantity shown.

**Abstract: good, no change needed.** 199 words (measured, ≤250). Memorable hook ("Activation patching and attribution graphs disagree about where a circuit lives. We show why:") and memorable closer ("Construction history is part of a circuit's causal anatomy."). Leads with block-and-rescue + the 0.31-vs-0.94 tool miss, per the round-1 ask. It is dense (long sentences) but within budget.

## 4. Concrete cuts to reach ~12–14 pages

Estimate (asserted): 10,525 words + 8 figures + 4 tables ≈ 15–17 double-column pages; ~11–12pp is text alone and 8 figures + 4 tables add ~3–5pp. To land 12–14pp, trim ~1.5–2.5k words-equivalent and demote 2–3 figures. Priority order:

1. **§8 Computed intermediate state (328 words, no figure) → one paragraph in §7 + Appendix A.** Tangential to the block-and-rescue thesis and the result is explicitly weak ("necessity … frequently repaired at 1.5B"; "does not pass the strict signature"). Keep a 2–3 sentence summary (non-restated intermediate is causally active under a directed swap; necessity is consumer/horizon-dependent) and push the 19/32, 26/32, 8/8-vs-0/8 detail to Appendix A. Saves ~230 words.
2. **§6.2 boundary cases (Klein-9B + SDXL) → a boundary table in Appendix.** The FLUX headline (§6.1 Klein-4B four-condition pass) and §6.3 "what it adds" carry the contribution; the Klein-9B 8/9 and SDXL one-step-necessity enumeration are generality detail. Saves ~200–300 words.
3. **§7.1 Mamba dose enumeration → Appendix; keep the one-sentence conclusion.** The write-vs-clock refutation is a good honest correction but secondary; the dose-factor 0.5/2 × six-cell × neighbor-layer-40-vs-44 detail is appendix-grade. Keep "the writer's causal property is its write; the near-stopped clock holds the store rather than authoring the answer." Saves ~150 words.
4. **§3.4 custody/replay sentence (line 135) → Appendix B/C.** Process, not result. Saves ~70 words from the body.

**Figures: 8 → 5 in the main body.**
- **Merge or cut Fig 5 into Fig 6.** Both are Gemma feature-basis-vs-native-cut bars; Fig 6 (feature-only / matched feature+error / error-only vs native) *supersedes* Fig 5 (feature-only vs native), and the abstract now leads with the matched-interchange number (0.31 vs 0.94) that only Fig 6 shows. Keep Fig 6 as the §5 punchline; fold Fig 5's identity-0.08/color-0.42 into it or cut it.
- **Demote Fig 3 (window necessity) to Appendix.** Referenced, but Table 1 already carries the numbers; the heatmap is confirmatory.
- **Demote Fig 8 (Mamba clock-dose) to Appendix** with the §7.1 compression.
- Main-body set: Fig 1 (schematic), Fig 2 (dissociation hero), Fig 4 (formation-vs-propagation — now answers the biggest conceptual attack), Fig 6 (tool miss, matched operator), Fig 7 (FLUX). This matches round-1's "carry it" set, updated for the round-2 experiments.

## 5. Top fixes (ranked)

1. **Cite Vig 2020 (2004.12265) for causal mediation** — credibility-level given the mediation-centered framing. Add Olsson 2022 (2209.11895) at "induction circuit" and Feng & Steinhardt 2023 (2310.17191) for the entity-binding neighbor.
2. **Fix the Fig 2 caption** — "three families" vs four groups; remove the unplotted earlier-band clause; state the error bars are identity-clustered.
3. **Cut to 12–14pp**: §8 → §7 + appendix; §6.2 and §7.1 detail → appendix; merge Fig 5 into Fig 6; demote Fig 3, Fig 8.
4. **Split the ~10 worst 68–98-word sentences** (§3.5, §5, §8, §9, §11) into one-claim sentences; move the §3.4 "artifact-only verifier / custody gates" sentence to the appendix.
5. **One clause naming the transplant as an interchange intervention** (Geiger lineage) — cheap, pre-empts a methods reviewer.

No blocking prior-art or clarity defect found; these are positioning and polish. Hedging and body jargon are measured-clean and should not be touched.
