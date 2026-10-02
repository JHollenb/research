# Round 2 — Interpretability reviewer (hostile but fair)

Paper: *The Commit Layer Does Not Move* (Hollenbeck, 2026-10-02, round-1 revision).
Read in full; round-1 reviews + response read first; figs 1–9, A–C opened (fig5, figA,
figB, fig2, fig3 pixel-inspected).

## Did round 1 land?

Mostly yes, and the honesty work is genuine.
- **Variance-split null (Exp A, §5 L93–95, figA):** landed. Trained op:fact 19.0, coord-main
  collapses to ~1.3% in random/shuffle nets; vproj-permute keeps 11.9. Kills the "coord-main
  is trivial" hypothesis. **But the null is incompetent (top-1 0/96), conceded in-text** — so
  "learned" is earned, "scaffold rather than what any competent net learns" is not.
- **Sliding-window causality (Exp B, §3 L59, figB):** honestly *conceded*, not resolved. At
  17 tokens sliding==causal, so the type-flip is an exact no-op (0.0); the architecture claim
  is correctly downgraded from "layer typing predicts commit" to "depth." Good science, but
  the original attention-type reading is withdrawn, not vindicated.
- **Function vectors (Exp C, §4 L83, figC):** NOT_FV, but a bounded negative (all-heads,
  coef=1, extracted incl. held, L24 top-of-grid). The XNOR inversion (§10 L172) carries more
  weight than the FV test itself.
- **FAL-3 firing:** now disclosed plainly (abstract L19; §5 L103) — a real improvement.
- **Relational op (Table 1, L107):** landed; identity~capital 0.20 vs identity~color 0.84
  closes the "all read-back" confound. But FAL-2a (sum-of-squares) fired for Gemma, again
  cleared by the "robust" cosine statistic.

## Fresh attacks

1. **Is "scaffold" > "late layers commit" (Geva/Meng/Lad/Stoehr/tuned-lens)?** Marginally.
   The real delta over Lad 2024 is *per-fact causal* location + the learned-split null +
   cross-arch — legitimate but incremental, and the crispest number (SD 0.00) is
   locator-dependent (below). **Stoehr et al. 2024 (paragraph-memorization localization) is
   uncited** and is a direct depth-localization predecessor; add it to §11 (L184).
2. **Post-hoc locator (the core live hole):** the title and headline SD 0.00 rest on a
   *post-hoc* commit locator; the preregistered argmax locator fired the falsifier. The fix
   (confirm-color, all three locators frozen) is **half-done** — Qwen passed (S1 2.84/S2
   1.44/S3 1.76 <4, median L23); Gemma still running. Until both halves land, the title
   overclaims. The concern holds up.
3. **Right null?** No — a competent different-task/different-seed trained net is the right
   null; the paper concedes this. Surface the bound in the abstract, not only §5.
4. **Constructive §10 = evidence or decoration?** Mostly decoration for the *learned*-scaffold
   thesis (host-supplied addresses, donor payloads, 6/14 competent; paper admits it shows
   "fixed+shared, not learned"). Only the XNOR-inversion + wrong-site controls load-bear.

A quiet pattern a hostile reader will flag: falsifiers keep firing and being cleared by a
post-hoc "robust" statistic (FAL-3 argmax→commit; FAL-2a SoS→cosine). Honest, but reads as
moving goalposts until confirm-color pre-commits the primary statistic.

## Clarity / length
~8,000 words, 13 sections, 12 figures — defensible, but §5 is overloaded: three locators
(argmax/commit/necessity-argmin) + two provenances + two falsifier reconciliations in one
section. A frontier reader loses the thread. Restructure §5 around one primary statistic.

## Score & tier
**Score: 6/10** (up from 5 — honesty and the null earn it). Main conference (ICLR/NeurIPS):
**reject as-is**, borderline-accept once confirm-color lands *both* halves and the Fig 5
defect is fixed. MI workshop (BlackboxNLP): **clear accept**. Would my team cite it? Yes —
the per-fact commit metric, the learned-split null, and the honest-null methodology; not the
title at face value yet.

## Top-5 must-fix

1. **Title + headline invariance rest on a post-hoc locator; confirm-color is half-landed**
   (L1/L11, abstract L19, §3 L65, §5 L103). *Fix:* gate the "does not move / SD 0.00" claim
   on confirm-color landing the **Gemma** half with all three locators frozen; until then
   soften the title (e.g. "...Barely Moves") or label the SD 0.00 explicitly commit-locator-
   contingent in the abstract. This is the paper's single biggest exposure.

2. **Fig 5 F2C (PNG) contradicts the corrected §5 text** (caption L97 + figure). The panel
   still labels the 4.0 line "FAL-3 threshold," plots the *commit*-locator SD (qwen color
   4.17) crossing it, and annotates "2 weak-signal facts: median=L23" — the exact
   "none-really-triggered" framing the text has retracted. The *frozen* FAL-3 statistic
   (argmax SD 5.45/4.01, fired 2/6) is nowhere plotted. *Fix:* regenerate F2C to plot the
   frozen argmax statistic with its threshold, or drop the "FAL-3 threshold" label and the
   weak-signal annotation; the figure currently undersells the fired falsifier.

3. **Scope the null to "learned," not "scaffold vs any competent net"** (§5 L93–95, abstract
   L19, §13 L206). *Fix:* add one competent control (different-seed or different-task trained
   net of identical shape) or state the open gap in the abstract — the incompetence bound
   (top-1 0/96) currently lives only mid-§5.

4. **Pre-commit one primary statistic per falsifier** (§5 L103, L107). *Fix:* in confirm-color,
   name the commit-locator and cosine statistics as *primary* in the prereg (not merely
   "freeze all three"); report one primary result per falsifier so the "robust statistic
   clears it" pattern is not post-hoc. Report FAL-2a Gemma firing in the abstract's falsifier
   tally, not only §5.

5. **Compress §10 and add Stoehr 2024** (§10 L166–180; §11 L184). *Fix:* cut §10 to the
   XNOR-inversion (L172) + wrong-site/wrong-sign controls (L174) — the only parts that
   load-bear on "fixed, program-not-vector"; fold the VM/fork-replay paragraph (L176) into
   one sentence, since the paper concedes it does not speak to *learned*. Cite Stoehr et al.
   2024 as a depth-localization predecessor and claim the per-fact-causal delta.
