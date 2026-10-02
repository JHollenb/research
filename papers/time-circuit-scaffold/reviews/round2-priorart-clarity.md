# Round 2 review — prior-art positioning, clarity, companion split

Reviewer lens: novelty/prior-art + frontier-reader clarity + the companion split. Read-only on `paper.md`; this file is the output. Scope: verify round-1 fixes, catch what the revision introduced.

## 0. Round-1 status (verified fixed)
- Prior-art adds landed: Lad 2024, Chughtai 2024 (§9), Sharma 2024, Basu 2023, Nanda 2023, Belrose 2023, Gurnee 2024 all present in §9/§11 with deltas.
- Thesis now verbatim at end of §1 and close of §13; "space circuit" glossed on first use; "scaffold" disambiguated from prompt/CoT scaffolds.
- §5 confound moved below results; relational addendum landed (Table 1). §8 compressed to one paragraph.
- Companion now links back by path (companion §11, line 294) — cross-ref is symmetric.
- Body prose is **clean** of Saturn/mrun/job-ID/FAL-/FROZEN/PREREG jargon; those survive only in figure panel labels (F1, F2A–C) and the reproducibility appendix (correct place). Abstract is 219 words (≤250).

## 1. Prior-art verification (WebSearch; no fabrication found)
Every arXiv ID I checked resolves to the claimed paper. The three IDs round-1 could not verify are **real**:
- Agarwal 2026 = arXiv:2609.17537, "Relation Before Entity: Deferred Commitment in LM Factual Recall" (ICML 2026 MI workshop). Confirmed.
- Kamath 2025 = transformer-circuits.pub "Tracing Attention Computation Through Feature Interactions" (no arXiv; thread). Confirmed.
- Mazur 2026 = arXiv:2606.15796, DifFRACT. Confirmed.
- Spot-checked Chughtai 2402.07321 and Lad 2406.19384 — both correct.

No citation changes required for accuracy. Do confirm Görgün 2512.08486, Cheng&Zhang 2605.04061, Bugaud (TrustNLP 2026) before camera-ready — these live in the companion ref list but are inherited; I did not re-verify all three this round.

## 2. Prior-art GAPS (new / unaddressed)

**(a) Agarwal 2026 is the nearest competitor and is under-positioned — highest priority.**
Agarwal reports a *temporal asymmetry*: relation information becomes generation-controlling **before** entity information (four decoder models, eight prompt families). The scaffold paper currently buries Agarwal in a one-liner lumped with Hase (§11 ¶2: "recall defers commitment"). Two problems:
  1. This is the single closest contemporaneous work on *when/where commitment happens by depth* — it deserves its own delta sentence, not a shared clause. Your delta is clean (per-fact causal **input-invariance**, SD 0.00; Agarwal shows a cross-*type* asymmetry, not per-fact invariance) but you must state it.
  2. **Apparent tension to resolve.** Your relational addendum finds capital-of commits at **layer 22, SD 0.00 — the same layer as identity** in both models (line 107). Agarwal finds relation commits *before* entity. A reader who knows Agarwal will read these as contradictory. They are reconcilable (Agarwal measures relation-type vs entity-token availability at the entity position; you measure the commit of the operation's controlling state at the final token), but you must say so explicitly, or the headline same-layer result looks like it refutes a cited paper you don't engage. One sentence in §5 (after Table 1) or §11.

**(b) Merullo, Eickhoff, Pavlick 2024, "Circuit Component Reuse Across Tasks"** (arXiv:2310.08744, ICLR 2024). Uncited. Directly relevant to your §4 central claim that a **recurring reader is reused across inputs and merely re-weighted by operation** — Merullo argues a small set of task-general components is reused across tasks. Your "reader is a fixed object that operations tune" is a sharper, causal, per-coordinate version of their reuse claim. Cite in §4 or §11 ¶3 (alongside Todd/Hendel) and claim the delta (signed per-coordinate variance split, not qualitative reuse).

**(c) Stoehr et al. 2024, "Localizing Paragraph Memorization"** (arXiv:2403.19851). Uncited. Relevant to §6 ("the scaffold lives in the weights" / value-projection row-permutation) — Stoehr localizes memorized content to specific low-layer weights/heads via gradient spatial pattern. A light cite strengthens §6's "disordering trained weights destroys the reader." Lower priority than (a)/(b).

**(d) Olsson 2022 (induction) / Wang 2022 (IOI)** are cited in the companion but not here. §4's row-selection-over-fixed-reader is an attention-read story; one cross-ref ("the companion's induction/IOI controls are the locally-decisive contrast") would help, but duplication risk argues for leaving ownership with the companion. Optional.

## 3. Companion split — two NEW duplications the revision introduced

The round-1 split (P1 owns sweeps/formation/clock-dose/attribution-head-to-head; P2 owns per-fact invariance/variance/same-parent/frozen-profile/null) is otherwise clean. But the revisions re-created two overlaps:

- **Attention-type-swap control now lives in BOTH papers.** Scaffold §3 + Figure B (lines 59–61) present the "17-token sliding mask == causal mask, type flip is a 0.0-logit no-op, commit profile byte-identical, logits shift 19.6 under a real window-4 mask" result as the paper's own reviewer experiment (job-0b7652b2112d). The companion §7 Table 4 row (line 229) states the identical finding in prose ("flipping a layer's attention type is an exact no-op … per-layer commit profile is byte-identical under the swap"). Pick one owner. Recommend **scaffold owns it** (it ran the dedicated experiment and makes the architectural "fixed by depth, not attention type" claim); companion Table 4 should cite the scaffold for the causal control and keep only the parity observation.

- **Mamba clock-dose: same three job IDs in both appendices** (scaffold Appendix A line 230: job-baf14cd06dd2 / cbb0e8a57f45 / e55fc32a16ed; companion Appendix A line 319: identical). The companion §7.1 is the clock-dose's full home and owns it correctly. The scaffold restates the result twice (§3 line 63 "the matched dose panel finds the write is the larger lever in all six cells"; §7 lines 141–142) and lists the primary job IDs as if primary. **Fix:** scaffold §3/§7 should cite the companion for clock-dose (as it already does for mediation/attribution-blindness), and the scaffold Appendix A clock-dose row should read "(see companion)" without re-listing the three jobs.

- Minor: the 21/21 byte-exact diffusion scene-compiler result appears in scaffold §7 (line 144) and again in §10 (line 170) — internal, not cross-paper. Consolidate to §10 and have §7 cite forward.

## 4. Clarity

- **Abstract ends on two caveats** (falsifier + null), which blunts an otherwise strong open. The honesty is right but misplaced for memorability: compress the falsifier sentence to one clause and drop the null to a single trailing sentence, so the reader leaves on the result, not the hedge. Target the round-1 suggested shape (lead with SD 0.00, same-parent 3.130 nats, attribution-blindness; one honest-limit line).
- **Visible authoring artifact:** `<!-- TODO confirm-color -->` at line 103 must be removed before submission (it renders in Markdown viewers). Grep found exactly one.
- **§13 conclusion re-states most abstract numbers** (SD 0.00/1.16, 3.130 nats, 0.336, 84.0%, falsifier, null) plus the thesis a third time (line 212 vs line 27). Cut §13 ~40%: keep the thesis restatement and the interpretation consequence (attribution tools see the space circuit, miss the scaffold); drop the number recital.
- **Hedging density** (~52 hedge tokens) is mostly load-bearing honesty, but stacks in §7 ("consistent with," "at smaller scale and lower power," "single-seed," "we say consistent with not the same" — four hedges in two sentences, lines 132). Keep one, cut the rest.
- **Figure captions double as results paragraphs.** Captions for the three reviewer-control figures (A, B, C) run 90–130 words each and repeat the body. Trim each to ~50 words; the body already carries the numbers.

## 5. Concrete cuts to 12–14 pages (currently ~10,200 words + 11 figures + 2 tables + 3 appendices → ~18–20 pp)

Ranked by pages saved vs. cost to the thesis:
1. **§10 "Constructive evidence" (~1,100 words + Fig 8)** is the biggest discretionary cut. It draws on separate programs (VM fork/replay, archive pages, scene compiler) and the §10 limits paragraph already concedes "efficiency figures come from separate experiments." Compress to one tight subsection keeping only the result that bears on the thesis — *the per-input program is installable at the fixed site, and matched wrong-site/wrong-program controls fail* (scene-compiler 21/21 + wrong-source/sign; XOR/XNOR inversion). Move fork/replay + archive-page paragraphs (lines 174–176) to an appendix. Saves ~1.5–2 pp.
2. **Move Figures A and B to an appendix** (reviewer controls). Keep Figure C in body — it carries the function-vector delta, which is a substantive novelty claim. Saves ~1 pp.
3. **§3 companion-summary paragraph (lines 62–63)** restates the companion's formation-window + clock-dose + distributed-band at length. Cut to 2–3 sentences citing the companion; keep only the per-fact SD result that is genuinely this paper's. Saves ~0.5 pp.
4. **§13 ~40% cut** (above). Saves ~0.5 pp.
5. **§9 null**: three paragraphs + Fig 7. Tighten prose ~30% (the Chughtai framing and the two decisive-null numbers are the keepers; the "two transfers also miss" paragraph, lines 162, can fold to one sentence). Saves ~0.3 pp.
6. **§7 diffusion timing-of-write paragraph (line 146)** overlaps §10's install-timing result; consolidate.

Net: ~4 pp of cuts reaches the target without touching the decisive test (§5), the same-parent result (§4), or the frozen-profile prediction (§6).

## 6. Five ranked actions
1. **Position against Agarwal 2026** — own delta sentence + resolve the same-layer-vs-relation-before-entity tension (the one gap that can look like an unaddressed contradiction).
2. **Add Merullo 2024** (circuit reuse) to §4/§11; it is the direct predecessor to "recurring reader reused across inputs."
3. **Resolve the two new companion duplications** — assign the attention-type-swap control (recommend scaffold) and stop re-listing the clock-dose job IDs in the scaffold.
4. **Cut to length** — §10 compress + Figs A/B to appendix + §3/§13 trim (~4 pp).
5. **Housekeeping** — delete the line-103 TODO comment; de-hedge the abstract ending and §7; trim reviewer-control captions.
