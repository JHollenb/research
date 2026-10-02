---
title: "Frontier-venue review: Dynamic Circuits Loop Through a Stable Time Scaffold"
type: peer-review
venue-frame: ICLR/NeurIPS interpretability track
reviewer-role: senior interpretability researcher (frontier lab)
paper: ../paper.md (commit 4214b0c)
context: architecture-brief-2026-10-02.md, architecture-math-2026-10-02.md
date: 2026-10-02
---

# Review

## Summary (of what the paper claims)

The paper proposes that the computation controlling a model's output is a *dynamic circuit* (per-input source coalition, address, payload, dose, timing) looping through a *stable time scaffold* (a reusable organization of causal roles: contextual source, live reader/transition, writer, carried state, native consumer) laid out along ordered execution. The time axis is denoising steps (diffusion), depth+position (AR transformer), or recurrent transitions (SSM). It formalizes the scaffold as a causal abstraction (Geiger et al.): one *fixed* lowering + alignment with high interchange-intervention accuracy (IIA) across a context×operation range, while the active edge set varies per input. It reports seven properties (reusable interfaces host different computations; context/operation selects participation; state formed over ordered execution; written state changes later reads; frozen profile predicts held behavior; organization lives in trained weights; architecture is executable as a scene generator and a model virtual machine), claiming each is replicated across a diffusion model, an AR transformer, and a state-space model. It is unusually explicit about limits: the cross-family common graph is a null; diffusion exact-reproduction is architectural custody, not discovery; most LM/SSM results are single-seed; and a block of location-index/variance-ratio checks are disclosed as non-discriminating proxies.

**Assessment in one line.** A genuinely ambitious synthesis with several real new measurements and exemplary failure-disclosure, held back from clear acceptance by (a) a top-line thesis whose falsifiable core is never measured with the one statistic its own framework names, (b) a "seven properties × three families" scaffold that two properties do not actually satisfy, and (c) heavy single-seed / small-correlated-denominator evidence plus dependence on an unseen companion for the central causal result.

## Score: 6 / 10

Marginally above threshold for a venue that rewards rigor and honest negative results; below the bar for a confident accept. The paper's candor is a real asset and most individual claims are carefully hedged; what keeps it at 6 rather than 7–8 is that the *unifying* claim — the thing that makes this a paper rather than five vignettes — is the least directly tested part.

## Confidence: Medium-high (0.7)

I read the full paper (361 lines) and both context documents closely. I did **not** independently verify the underlying FINDINGS files, rerun any experiment, or read the companion paper that carries the core E20 mediation result. All numeric claims below are **asserted by the paper** and taken at face value; I flag where a claim's *logic* (not its number) is the problem. Word counts are **measured** (see below).

---

## Focus-area findings

### 1. Novelty vs prior work — delta stated, partly real

The delta is **stated clearly** (§1 line 34; §11), which already puts it ahead of most submissions. The honest mapping to Geva (staged recall), Lad (stages of inference), Todd/Hendel (function vectors), Feng & Steinhardt (binding), Merullo (reuse), and Geiger (causal abstraction) is a strength, not a liability.

Whether the delta is **real**:
- The *formalism* is borrowed wholesale from Geiger et al. (the scaffold is literally a causal abstraction with high IIA; §2 line 50). The paper does not over-claim this, but the contribution must therefore live entirely in (i) the *content* of the role decomposition and (ii) its cross-family recurrence — not in the method.
- The genuinely new *measurements* are: the same-parent/byte-identical-patch query-selectivity assay (∂A/∂q ≠ 0; §4 line 96), the signed per-item reader cosine as a per-coordinate statement (§4 line 102), time-indexed diffusion authority (first-call lesion 20.82 vs late 2.15; §5 line 128), and the executable MVM with hostile XNOR inversion (§9.2 line 196). These are incremental-but-real contributions on top of the named priors.
- The *core conceptual move* — "fixed infrastructure + variable program + carried state" — is close to the union of Geva + Todd + Feng + Merullo. The paper's "unification" is real as positioning but thin as mechanism: a skeptic can read it as repackaging four known results under one metaphor plus a cross-family demonstration. The cross-family recurrence is the most defensible novel empirical claim, but each family individually leans on prior cross-architecture work (Sharma for Mamba/ROME, Basu for diffusion mediation), so the novelty reduces to "we did all three and called it one architecture."

**Verdict:** delta clearly stated; partially real. It is a synthesis-plus-a-few-new-assays, not a new mechanism. This is publishable novelty at an interp venue *if* the unification is earned empirically (see #2), which is where it is weakest.

### 2. Falsifiability — the central weakness

The top-line thesis (abstract line 20; §1 line 32) is stated so generally that it is **true by construction of almost any stateful sequential model**: "an operation reads the present carried state, acts through ... writer and consumer roles, changes that state, and thereby influences the next operation." The functional form (§2 line 56: `a_t=A(...)`, `w_t=W(...)`, `z_{t+1}=T(z_t,w_t)`, `y_t=C(...)`) is a generic recurrence satisfied trivially by any residual stream / KV cache / hidden state. A reviewer *will* ask: what network is *not* a dynamic circuit looping through a scaffold?

The paper knows this and tries to rescue falsifiability with "the force is the word *fixed*" (§2 line 50–52): one lowering/alignment with high IIA across a broad context×operation range, roles separately testable. **This is the right move — but the paper never reports the number that operationalizes it.** The math companion itself states "the right statistic is band-level IIA under a fixed lowering" (architecture-math §9.1/§10) and it is never a headline. Instead we get a patchwork of per-operation block/rescue numbers and by-construction exact reproductions.

Which results are **risky** vs **by construction**:
- *By construction (not risky):* diffusion 21/21 exact reproduction (the paper says so repeatedly); transformer fork/replay bit-exactness (complete-state theorem, math §2); Mamba export/resume exactness; "early-layer absence" (predicted by the thesis, §2 line 60; math §3.1); joint row-permutation invariance (an exact algebraic identity, math §4); the superadditivity *sign* of the K×V interaction (also an identity).
- *Risky and held:* same-patch different-query selectivity 16/16 (a steering-vector model predicts 0 — genuinely discriminating); block-and-rescue of a *narrow late band*, which the paper correctly argues is **not** architectural (§12 line 228); one fixed interface hosting 3 operations; per-item reader cosine within>across operations; Mamba staged 3/3 vs endpoint-sum 0; ancestry 6/6 vs 1/6; hostile XNOR inversion 148/150.
- *Risky and missed (disclosed — credit):* cross-family common graph (null, ties additive, §10); position reader 12/16; color reader ordering 5/8; hybrid SSM writer not found; MoE-30B negative; random-init reader margin +0.350.

**Verdict:** the thesis is *technically* falsifiable through the fixed-lowering/separability clauses and several sub-predictions genuinely risked failure, but the top-line framing invites "true by construction." The discriminating-tests table (architecture-math §9.2) is the real falsifiability argument and it is buried in a supplementary doc. It should be the spine of the paper.

### 3. Is "predictive" earned? — partly, and over-generalized

- Earned, prospective, held: the **24-coordinate relational reader** (transformer) beats three frozen competitors 8/8 on held relation contexts (§7 line 160); the **Mamba 27-coordinate** capital reader 8/8 and delayed-identity 4/4 (§7 line 164). Both frozen before held contexts opened; the formation-over-time and clock-retest are prereg-frozen with canaries and job IDs (strong).
- **Disclosed misses within the same predictive test:** color retains shape but misses reader *ordering* (5/8); identity is readout-limited; size unavailable (§7 line 160). So "predictive" holds for *one operation per family*, not across the board.
- Two caveats degrade the strength of the held numbers: (i) the paper itself calls the eight relation contexts **"eight correlated contexts"** (§7 line 160) — 8/8 on correlated contexts is closer to ~1–2 effective independent tests; (ii) several freezes are "evidenced by file modification time only" (Appendix C line 348; §13), which is not a preregistration a frontier reviewer will accept (mtime is forgeable and self-set). The prereg-with-canaries runs (formation-over-time, clock-retest) are the credible ones; the mtime freezes are not.
- The abstract (line 20) says "it predicts held behavior from a frozen role profile" without the "one operation per family, others missed" qualifier. **This over-generalizes a result the body correctly scopes.**

**Verdict:** "predictive" is earned specifically for the relational reader (transformer) and the Mamba capital/identity readers, with honest misses. It is not earned as the general property the abstract and §7 title imply.

### 4. Overclaims (sentence-level, with line numbers)

1. **§1 line 40 / abstract line 20 — "seven properties, each replicated across the three families."** Not literally true. **Property 5** (predicts held behavior) has no standalone within-family *diffusion* prospective test — diffusion appears only inside the cross-family core, which is "suggestive" (§7 line 166). **Property 6** (lives in trained weights) is essentially transformer-only (v_proj permutation, Pythia); the SSM continuation result has a confound (wrong-label control also moved +0.448, §8 line 176) and there is no diffusion weight-dependence result. So P5 and P6 are not replicated across all three families. This is a **structural overclaim** in the organizing sentence of the paper.
2. **§8 (whole section) — Property 6 is the weakest and is presented as a peer of the other six.** Its cleanest reader-specific test *partially failed* (random-init net also shows the margin, +0.350, §8 line 174 — disclosed, credit) and its nulls are "behaviorally dead" so cannot separate a scaffold from any competent net (§8 line 174; math §9.1). The paper half-concedes this ("bounded by the incompetence of the nulls"). It should be **downgraded** from "a property replicated across families" to "suggestive, incompletely controlled; the discriminating control (a competent non-scaffold net) is not run."
3. **§5 line 122 — the 7B block = 0.595 explanation.** "The block is lower at 7B only because the commit is redundantly spread across several late layers and a fixed six-layer mediator cannot capture a commit that leaks to the last layer." This is a post-hoc auxiliary hypothesis rescuing a weaker number (block 0.595, rescue 0.770 vs 0.92/0.87 at 1.5B). It is plausible and partially supported (commit-SD 2.30, 100% in L19–27), but it is asserted as the explanation rather than independently tested, and the stronger of the two numbers (rescue) is the one foregrounded. Flag the asymmetry.
4. **§9.2 line 196 — "An additive steering vector would not invert with the program."** Fine for the specific full-K/V XNOR program, but stated as a clean dichotomy; an input-reading additive mechanism could also invert. Minor; soften.
5. **Abstract line 20 — "independently authors the answer ... (transplant rescue 0.71 to 0.99 ...)."** "Authors" is strong for a 0.71–0.77 rescue with 0.595 block at 7B. The 0.99 upper bound is a round-up of Gemma's 0.985. Minor.
6. **Address/payload consistency.** §4 line 110 honestly flags that the joint row-permutation is "near-invariant but not exact" (0.859; MAE 7–11) against an identity that predicts *exact* invariance, and says it should be rerun in fp64 before 0.859 is cited as anything but near-invariant. But Figure 1 and §9 then cite the 7–11 MAE as clean support for "the key, not the row, is the address" without the fp64 caveat. **Inconsistent emphasis** between the careful §4 statement and the confident figure captions.
7. **"Three families" / "a state-space model."** The SSM leg is essentially one family (Mamba 130M–2.8B); the one hybrid test (Falcon-H1) found the SSM side does *not* carry the store — the attention side does (§3 line 88). The title's singular "a state-space model" is honest; several body sentences generalize to "state-space models" as a class on one-family evidence. Keep the singular framing throughout.

### 5. Clarity, structure, length

**Measured:** total 13,873 words; abstract **525 words** (one unbroken paragraph); main text through §14 = 11,565 words; appendices 2,308; §13 alone 979.

- **The abstract is ~2.5× a venue abstract and is a single dense paragraph.** This is the first thing an area chair reads and it is exhausting — it tries to state every result with numbers. Cut to ~200 words: thesis, the three families, the 2–3 genuinely discriminating results, and the headline honest limit (cross-family null + custody/parity caveat).
- **Section 13 + Appendix D (~979 + ~600 words) defend against tests the paper says don't matter.** Admirable honesty, wrong location. Move §13 almost entirely into Appendix D (merge), leaving a 3-sentence pointer in main text: "A set of location-index and variance-ratio checks test a proxy, not the role graph; they are reported with their limits in Appendix D and none is used as spine evidence."
- **The custody/parity caveat for diffusion exactness is repeated ~5 times** (abstract, §1 line 36, §9.1 line 186, §9.2, §12 line 228, plus math §2). Consolidate to one authoritative statement in §9.1 and cross-reference.
- **The attention-identity derivation (§4 lines 108–112)** duplicates math §4. Keep the result and the SDXL factorial in main text; move the derivation to an appendix.
- **Promote the discriminating-tests table (architecture-math §9.2) into the main text** as the falsifiability spine (see #2). It is currently the paper's best argument and lives only in a companion doc.
- Net: ~13.9k → ~9k is achievable without losing substance. Everything above the "levels of claim" table (§2) and the seven-property spine is worth keeping; the proxy-defense and repeated caveats are what bloat it.

Structure is otherwise logical and the levels-of-claim table (§2 lines 64–74) and Appendix A evidence table are genuinely useful — keep both.

### 6. Single most important additional experiment (≤7B)

**Measure interchange-intervention accuracy (IIA) of the fixed role lowering directly, on a held grid of contexts × operations, against a per-context re-fit ceiling and a random-lowering null.** Qwen2.5-1.5B or Gemma-2-2B — well within budget.

Rationale: the thesis's falsifiable heart is "there exists *one fixed* lowering with high IIA across a broad context×operation range" (§2 line 50). The paper's own math says band-level IIA under a fixed lowering is "the right statistic" yet never reports it. Everything shipped is either a per-operation partial test or a by-construction exact reproduction. The experiment:
1. Freeze one lowering + alignment (the L22–27 K/V band + subject-position read) on discovery contexts.
2. Evaluate IIA on *held* contexts crossed with *held* operations (color, position, identity, relation), reporting a single accuracy.
3. Compare against (a) a lowering **re-fit per context** (the ceiling: if this is much higher, the scaffold is really per-input and the thesis weakens) and (b) a random/permuted lowering (the floor).

If the fixed lowering reaches near-ceiling IIA on held operations, the "fixed scaffold" claim is *earned quantitatively* and the "true by construction" objection dissolves. If per-context re-fitting wins decisively, the paper's own thesis is falsified in the direction it should want to know about. This single number does more for the paper than any additional vignette.

*Runner-up (the paper names it as the key missing control, §12 line 230):* a **behaviorally competent non-scaffold network** for the learned claim (Property 6). It is more important scientifically but ill-defined and expensive to construct ≤7B; the IIA test is cheaper, directly addresses the review's central concern, and is unambiguous.

---

## Major issues (ranked)

- **M1. The unifying claim is never measured with the statistic its framework demands (falsifiability).** No headline IIA for a fixed lowering; the top-line thesis reads as true-by-construction. Fix: run the IIA experiment above and lead with it; promote architecture-math §9.2's discriminating-tests table into the main text. (abstract line 20; §1 line 32; §2 lines 50–52, 56; §7)
- **M2. "Seven properties, each replicated across three families" is not literally true.** P5 (predicts held behavior) has no standalone within-family diffusion prospective test; P6 (lives in weights) is transformer-centric with a confounded SSM result and no diffusion result. Fix: either add the missing cells or rephrase to "seven properties, each demonstrated in at least two families, with the family coverage stated per property." (§1 line 40; §7 lines 156–166; §8 lines 168–176)
- **M3. Property 6 ("lives in trained weights") is overstated.** Disclosed failed prediction (random-init margin +0.350), nulls behaviorally dead, discriminating control (competent non-scaffold net) not run; continuation result confounded by a wrong-label control that also moved. Fix: downgrade to a hedged sub-claim; move it out of the seven-property spine or explicitly mark it "incompletely controlled." (§8 lines 168–176; §13 line 255)
- **M4. "Predictive" is over-generalized from one operation per family, and several freezes rest on file-mtime.** Fix: scope the predictive claim in the abstract to the relational reader (transformer) and capital/identity readers (Mamba); state that color/position/identity-readout/size missed; drop mtime freezes from the evidence of prospectiveness or label them explicitly as non-preregistered. (abstract line 20; §7 line 160; Appendix C line 348)
- **M5. The central causal result (E20 block/rescue) is offloaded to an unseen companion.** §5 line 120/122 re-reports block 0.924 / rescue 0.871 but attributes the quantitative mediation to the companion. A reviewer cannot verify the foundation. Fix: include a self-contained statement of the E20 design and at least the primary cell's numbers and controls in this paper, or submit the companion together. (§1 line 24; §5 lines 120–122)
- **M6. Length and abstract bloat.** 13,873 words measured; 525-word single-paragraph abstract; §13 defends non-discriminating proxies in the main text. Fix: abstract → ~200 words; §13 → Appendix D with a 3-sentence pointer; consolidate the repeated diffusion-custody caveat; move the attention-identity derivation to an appendix. Target ~9k.

## Minor issues

- **m1.** 7B block=0.595 is rescued by a post-hoc "redundant spread" hypothesis asserted rather than tested; the stronger rescue number is foregrounded. State the asymmetry plainly. (§5 line 122)
- **m2.** Address/payload emphasis is inconsistent: §4 flags the 0.859 joint-permutation as merely "near-invariant" pending an fp64 rerun, but Figure 1 / §9 cite the MAE 7–11 as clean support. Harmonize the caption caveats with §4. (§4 line 110; Figure 1 line 38; §9.1 line 186)
- **m3.** "An additive steering vector would not invert with the program" is a clean dichotomy that an input-reading additive mechanism could violate; soften to the specific full-K/V program. (§9.2 line 196)
- **m4.** The one >7B test (Qwen3-30B MoE) is a negative; honest, but ensure no body sentence implies scale-robustness. The scaffold is unproven above 7B and the single scale test failed the isolated cut. (§10 line 208; Appendix line 328)
- **m5.** The function-vector refutation is explicitly a "weak, unit-coefficient, all-head negative" (§13 line 255; Appendix D4), yet the delta-from-function-vectors claim in §1/§11 leans on the reader being non-additive. The strong evidence for non-additivity is the same-patch selectivity and hostile XNOR, not the FV null; make that the cited basis and stop implying the FV null refutes function vectors. (§1 line 34; §11 line 218; §13 line 255)
- **m6.** "Independently authors" overstates a 0.71–0.77 rescue; "0.99" rounds up 0.985. (abstract line 20)
- **m7.** SSM generalization rests on one family (Mamba) plus a hybrid where the SSM side failed; keep the honest singular "a state-space model" everywhere, including any body sentence that says "state-space models." (§3 line 88; §12 line 226)
- **m8.** The competence-conditioned 8/8 vs all-row 7/8 (§7 line 160) means the competence gate flipped one context; confirm the gate was frozen before evaluation and state it, or the conditioning looks like post-hoc selection. (§7 line 160)

## Concrete fixes (minimal set to move toward accept)

1. Run and lead with the fixed-lowering IIA experiment (held contexts × held operations, vs per-context re-fit ceiling and random-lowering floor). This is the single highest-leverage change.
2. Rewrite the abstract to ~200 words; scope "predictive" to the relational/capital readers; name the cross-family null and custody/parity caveat as the two headline limits.
3. Fix the "seven × three" claim: a per-property family-coverage line, and move P6 out of the spine (or mark it incompletely controlled).
4. Pull the discriminating-tests table (architecture-math §9.2) into the main text as the falsifiability spine; move §13's proxy defense to Appendix D.
5. Make this paper self-contained on E20 (include the design, primary numbers, and controls), or submit with the companion.
6. Harmonize the address/payload caveat across §4 and the figure captions; rerun the 0.859 joint permutation in fp64 at one site as promised before citing it.

## What the paper does well (should be preserved)

- Exemplary disclosure: retractions, a failed prediction kept in the text (+0.350), the cross-family null, and the explicit "custody not discovery" and "replay parity not task success" caveats. This is above the median for the venue and should not be diluted when trimming.
- The genuinely new assays (same-patch query selectivity, signed per-item reader cosine, time-indexed diffusion authority, hostile XNOR inversion) are clean and discriminating.
- The levels-of-claim table (§2) and Appendix A evidence table are models of how to make a sprawling program auditable.
