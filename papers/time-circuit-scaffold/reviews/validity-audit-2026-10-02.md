# Measurement-validity audit — time-circuit-scaffold/paper.md (2026-10-02)

READ-ONLY. No model runs, no paper edits. Numbers below recomputed from the committed
result JSONs; code read under `saturn/experiments/2026-10-02-site-variance-decomposition/`
(`worker/per_item_worker.py`, `analysis/phase1_decompose.py`, `phase2_analyze.py`,
`phase3_analyze.py`, `confirm_analyze.py`) and `2026-10-02-p2-reviewer-experiments/`
(`analysis/analyze_A|B|C.py`, workers). This complements, not repeats, the custody audit:
custody asks "right run?"; this asks "right thing measured, and does it discriminate the
thesis from its stated alternative?"

**Thesis facets (author's framing):** (T-loc) commit/read *locations* are fixed by
architecture+training and do not move with input; (T-time) the scaffold is *built over
ordered execution* (seed→formation→commit→store→consumer); (T-space) per input the
operation re-weights a recurring reader and the fact re-points the row. "The store isn't
early" is expected under T-time and is **not** discriminating — correct.

Legend: VALID / WEAK / MEASURED-WRONG-THING / TRIVIALLY-EXPECTED / UNINFORMATIVE.

---

## 1. Per-fact commit invariance (§3, §5, Fig 2; P1/FAL-1)

(a) Tests T-loc: commit layer same across fresh facts.
(b) `phase2_analyze.write_commit` = **last layer L with resid-write gain(L) ≥ 0.5·max**
(S2); secondary `late_half_argmin` = argmin of single-layer necessity over the late half
(S3). Reported: Gemma identity SD 0.00, Qwen 1.16 (measured).
(c) Discriminates "location fixed" from "location rebuilt per fact" (grain-3 strawman). It
does **not** discriminate scaffold from ordinary localized factual recall (Geva/Meng/Lad
already predict recall commits mid-late regardless of fact). SD *exactly* 0.00 is partly a
quantization artifact: S2 is an integer index on a step-shaped curve whose step is
architecturally fixed, so SD→0 almost by construction once the curve shape is fact-stable.
(d) **VALID but under-powered / partly TRIVIALLY-EXPECTED.** Supports the narrow
"location-fixed" claim; weak as "scaffold vs standard recall."
(e) Paper: "commit layer input-invariant per fact." Licensed for T-loc; the broader
"scaffold" reading is carried by Paper 1 (T-time), not by this statistic — paper mostly
keeps that separation.
(f) **Cheap (~10 min): run write_commit/necessity-argmin SD across facts on random-init /
weight-shuffled Qwen (the Fig-A nulls already exist).** If SD is also ~0 there, invariance
is a locator+architecture property, not a learned scaffold. This null was run for the
read-site split but **never for commit location** — the single most valuable missing control.

**Frozen-metric swap (both FAL-1 and FAL-3):** FROZEN.json's band locator was
"argmax of the per-item necessity curve" (FAL-1) and "argmax of the resid-write curve"
(FAL-3). The committed code reports **neither** — it uses `late_half_argmin` and
`write_commit`. The paper discloses the write-window swap loudly; it is near-silent that the
necessity locator was *also* replaced (argmax→late-half-argmin). FAL-1's "held" verdict thus
also rests on a post-hoc locator. The confirm retest re-freezes both (S2/S3), which repairs
this prospectively.

## 2. FAL-3 write-window falsifier (frozen `sd_argmax_write > 4`)

(a) Tests T-time: the formation window closes at an input-invariant layer.
(b) Frozen statistic = SD across facts of **argmax of the residual-write gain curve**.
(c) **Was this ever a valid commit locator? No (asserted, with mechanism).** The write-gain
curve is a high early plateau that steps *down* at the commit (writing the subject early
authors the answer; re-writing after commit does nothing). Its argmax is therefore the
earliest effective layer (median argmax layer 0 for Qwen color, 13 for Gemma identity —
measured), i.e. it locates the plateau peak, not the commit, and on a near-flat curve is
noise-dominated. Firing (Qwen color 5.45, Gemma identity 4.01 — measured) is a locator
artifact, not evidence against T-time; equally its passing would prove nothing.
(d) **MEASURED-WRONG-THING** (the frozen statistic). The correct locator is the step-down
(S2) or necessity (S3).
(e) Paper states FAL-3 fired, labels the locator ill-chosen, reports plainly. Licensed and
honest.
(f) Done: confirm retest + S2/S3.

## 3. Confirm color retest (PREREG-confirm; S1/S2/S3)

(a) Re-test T-loc/T-time on fresh colors, all three locators frozen in advance.
(b) Measured: Qwen colorC S1 2.84 / S2 1.44 / S3 1.76 (n=48); Gemma colorC S1 3.44 / S2
0.90 / S3 0.97 (n=106); Gemma identity canary S1 **4.06 FIRED**, S2 0.00, S3 0.65.
(c) Genuinely confirmatory (frozen, reported either way). Two caveats: (i) the decision
rule keys on S2/S3 — the *stable-by-construction* step/necessity locators — while the one
input-varying locator (S1 argmax) still fires for Gemma identity; S1 is correctly argued to
be a bad locator, but "which locator counts" was decided after seeing that S1 fires. (ii)
The write-signal admission floor (1.5 nats) was set just above the two known phase-2
outliers (~1.3 nats); here it changed nothing (n_signal≈n_all), so moot, but it is a
threshold tuned to known bad cases.
(d) **VALID** (S3 is an independent-enough locator; both clear 4 on fresh facts).
(e) "Color commit input-invariant under all three locators." Licensed, with (c-i) noted.
(f) None needed.

## 4. Read-site variance split — retrospective (§5 left, Fig 5A; 42.2/29.0/1.1, "11×")

(a) Tests T-space: reader variance is op-driven, not fact-driven.
(b) `phase1_decompose.analyze_qwen_predictive`: balanced ANOVA on 24-coord signed profiles,
**fact factor = lexical set `lex`, 2 levels**. coord 42.2% / coord×op 29.0% / coord×lex
1.1% / coord×binding 1.6%. The code's own comment: "lexical set (FACT) has only 2 levels …
LOW-POWERED."
(c) **Does the 'fact' factor vary facts? Largely no.** Two lexical word-sets is 1 df; the
coord×lex main/interaction captures only the a-set-mean vs b-set-mean contrast and
noise-averages everything else, so it is structurally tiny regardless of whether facts move
the reader. coord×op has 3 levels (one a categorically distinct relational route). The "11×"
ratio is thus a design artifact of under-sampled facts, not a measured dominance of op over
fact.
(d) **MEASURED-WRONG-THING for the ratio headline** (fact under-sampled). The within-op vs
across-op *cosine* on the same data is the robust part.
(e) Paper leads the abstract with "eleven times the fact-like variance." Not licensed as a
robust ratio; see §6 below for what the clean design actually gives.
(f) Use the cosine + the Phase-3 clean ratio as headline (below). For a true variance split,
re-run with ≥2 measurements per fact so a split-half estimates the single-measurement noise
floor and separates true-fact variance from noise (~10 min).

## 5. Store-necessity split (§5 mid; 84.0/3.2)

(a) T-space on how much store is needed.
(b) `analyze_scaffold_poc`: ANOVA of |whole-band-swap effect| over op(3)×scene(4=fact)×
order×binding, **band fixed at L22–27** — tests necessity *magnitude* by fact, not location.
(c) Different ops have intrinsically different effect sizes (color read-back moves more
logprob than identity), so "op sets the magnitude" is close to expected; 4 correlated scenes
weakly sample fact.
(d) **WEAK / partly TRIVIALLY-EXPECTED.** Not wrong, but low discriminating power.
(e) "Store necessity set by operation." Over-read as thesis support; it is mostly an
effect-size statement.
(f) Report alongside the cosine evidence, not as independent confirmation.

## 6. Relational addendum — the clean op-vs-fact test (§5, Table 1; FAL-2a/2b)

This is the only design that both varies facts richly (20 countries) **and** has a
categorically distinct relational op, so it is the decisive read-side test.
(b) `phase3_analyze`: coord×op vs within-op-residual coord×fact. **Measured:**
Qwen coord×op 0.726 / coord×fact 0.274 → ratio **2.65**; Gemma 0.419 / 0.581 → ratio
**0.72 (fact > op → FAL-2a FIRED)**. Per-item within-op cosines Qwen 0.749/0.735/0.988,
Gemma 0.895/0.865/0.807; across-op identity~capital 0.204/0.218.
(c) When facts are properly sampled, op does **not** dominate fact 11×; it is 2.65× (Qwen)
and <1 (Gemma). So the variance-ratio claim does not survive the clean design. The **cosine**
claim does: within-op (0.73–0.99) ≫ across-op identity~capital (0.20) in both models, so
FAL-2b (within ≤ across) did **not** fire — genuine, robust support for "reader re-weighted
by op, not rebuilt by fact."
(d) Variance-ratio: **WEAK/refuted in clean design** (FAL-2a fired for Gemma). Cosine:
**VALID.**
(e) Paper calls FAL-2a firing "noise-sensitive" and leans on the "denoised" cosine. The
denoising (`within_op_across_template_cos_denoised`) **averages facts within a template
first, then cosines across templates** — it removes fact variance by construction, so it
cannot rebut a fact-variance falsifier without circularity. The honest, non-circular
statistic is the **per-item across-fact cosine** (0.73–0.99 vs 0.20), which already supports
the claim. Recommend: drop "11×/19×" from the headline; lead with per-item cosine + the
2.65×/0.72× clean ratio stated plainly (FAL-2a fired for Gemma).
(f) None needed; the honest numbers already exist in the JSON.

## 7. Reviewer-A null — "the split is learned" (§5, Fig A)

(a) Rule out: coord-main / op-weighting is a property of any structured net.
(b) `analyze_A`: same decomposition on trained / random-init / weight-shuffle / vproj-permute,
4 lexical sets. **Measured:** coord-main trained 0.381 vs random 0.012 / shuffle 0.014;
op:fact ratio trained **19.05** (jackknife 16.3–30.5) vs random 1.10 / shuffle 0.62;
vproj-permute 11.85. Held-out relation op-reader beats blind: trained Δ 0.512, **random-init
Δ 0.350 (also beats — a failed prediction, disclosed)**. Null top-1 **0/96**.
(c) Shows trained ≠ broken net. It does **not** show scaffold vs *competent non-scaffold*
net — random/shuffled nets are behaviorally dead (0/96), a strawman null. The relation
reader partially surviving in random-init weakens even the "learned" reading for that op.
Note the ratio (19) rests again on the 4-set `lex` fact factor (coord×lex 0.016), the same
under-sampling as §4 — so A inherits §4's weakness, not an independent confirmation.
(d) **VALID but WEAK / correctly bounded.** The paper states the incompetence bound
explicitly ("learned, not scaffold-vs-any-competent-net").
(e) "Split is learned." Licensed only to "not present in a random/broken net."
(f) A competent control (e.g. a different-seed or lightly-fine-tuned competent net, or a
non-recall competent task) is the missing discriminator; not ~10-min cheap.

## 8. Reviewer-B sliding-window type-swap (§3, Fig B)

(a) Tests whether attention *type* (sliding vs global) causes the commit location.
(b) `analyze_B`: at **seq_len 17**, full mask == sliding-4096 mask (measured maxabsdiff
0.0); flipping `is_sliding` on a layer = **0.0** logit change; a genuine window-4 mask moves
logits 19.62; commit profile byte-identical under the swap (0.0). Commit sits on even
(=sliding) layers (mean gain 0.407 vs 0.091 global).
(c) At this context the type flip is a **tautological no-op** — it toggles a flag whose mask
is already identical to the causal mask. So B cannot test the type-causality question at
all here; it only *removes* the earlier causal claim and exposes the type/parity/depth
confound.
(d) **VALID as confound-removal; UNINFORMATIVE as a positive test** (expected under both
thesis and null).
(e) "Commit tracks depth, not attention type." Slightly over-read — licensed version is
"attention-type is not causal at this context length; it covaries with depth and parity;
long-context untested." Paper's Fig-B caption/§3 largely say this.
(f) **Cheap (~10 min): impose a genuinely short window (e.g. 8/16) during the per-layer
commit sweep** and see whether the commit profile moves when the sliding mechanism is
actually live. More informative than the inert flip; the 19.62 calibration shows the hook
works.

## 9. Reviewer-C function vector (§4, Fig C)

(a) Tests whether op weighting = an additive Todd-style FV (deflation of T-space).
(b) `analyze_C`: rel−id o_proj vector injected at L24. **Measured:** 0/14 top-1 flips,
relation target +2.19 nats (color +0.16), reader not shifted toward relation, identity route
L23.KV0.value erased (−0.808→+0.007) without building the relational route.
(c) Discriminates "additive direction" from "re-pointed program" in the right direction.
But: the FV summed over all heads, coefficient fixed at 1, L24 = top of grid, extracted
including held contexts — a deliberately weak FV. The per-item relation logprob already
rises +1.7 to +2.5; a scale sweep could plausibly cross the flip threshold. And the held
contexts' greedy top is a function word (" a", ":\n"), so the flip metric is partly
ill-posed; C-P2 (reader shift) is the sound part.
(d) **WEAK negative** — shows "a unit all-head additive vector at L24 does not reproduce
it," not "no FV can."
(e) Verdict "NOT_FV" is overstated. Paper flags it as "a bounded negative" with the exact
caveats — so the conclusion as written in §4 is adequately hedged; the one-word JSON verdict
is not.
(f) **Cheap (~10 min): top-causal-head FV, coefficient scale-sweep, L_inj sweep** (grid
already computed; L24 peaks at +1.94). Paper says this follow-up has not run.

## 10. Query-selective authority / same-parent (§4, Fig 3)

(a) T-space: identical stored bytes get different authority under different queries.
(b) Same donor state+bytes, change only the question; median query-selective harm 3.130
(color) / 0.583 (position) / 3.021 (lookup) nats, 16/16 (measured, source POC).
(c) The byte-identical / same-parent construction is a real methodological strength (rules
out a different stored state). But the *result* — a patched color store harms the color
answer more when color is queried — is expected under any query-routed memory, which is
itself the space-circuit claim. So it confirms query-dependent read (grains 1–2) but is
**TRIVIALLY-EXPECTED** as stated; it does not bear on T-loc (the fixed part).
(d) **VALID-but-expected.** Clean demonstration of an unsurprising component.
(e) "Space circuit chosen per input." Licensed for the dynamic grains only.

## 11. Prospective relation profile + v_proj permutation (§6, Fig 6)

(a) T-loc/weights: a reader profile frozen pre-evaluation predicts held contexts; permuting
trained v_proj rows destroys it.
(b) Frozen 24-coord profile beats operation-blind/wrong-op/permutation competitors on held
relation contexts (mapped cosine 0.954 vs 0.566, RMSE 0.029 vs 0.149, 8/8 raw); full 256-row
v_proj permute collapses relation cosine 0.955→0.049.
(c) Prospective and competitor-controlled → genuine support for a learned, op-specific
reader. Bounds: 8 "contexts" = 2 lex×2 template×2 order (correlated replications, not 8
facts); the permutation also destroys competence (dependence result, not behavior-matched
null). Note tension to flag, not a contradiction: §6's *full* v_proj permute collapses the
profile *cosine*, while Reviewer-A's *L22/L23* v_proj permute *keeps* the variance *ratio*
(11.85) — different statistics (signed per-coord correspondence vs gross variance), so both
can hold, but the paper uses v_proj-permute in two opposite rhetorical roles.
(d) **VALID, low effective breadth — correctly bounded in text.**
(f) None cheap.

## 12. Constructive VM / XOR-XNOR / diffusion static bus (§7, §10)

(a) Engineering converse: the fixed site hosts an executable program (not a direction);
installing it drives new inputs.
(b) XOR 148/150 vs native 0/150; hostile XNOR inverts 148/150; diffusion program install
21/21 byte-exact, wrong-source/sign 57–97 MAE (0–255).
(c) XNOR inversion genuinely discriminates "program" from "additive direction" (adding −v
does not invert a function) — VALID for that sub-claim. But the diffusion "static bus is
prompt-agnostic" is near-definitional: cross-attention KV is constant across denoising steps
by construction, so 21/21 replay is a caching-consistency check; the wrong-source/sign
*controls* are the only discriminating part. These show the site is *fixed/addressable*, not
*learned* or *input-invariant-per-fact* — a different claim from the thesis core.
(d) **VALID (controls) / partly TRIVIALLY-EXPECTED (static-bus-by-architecture).** Paper §10
explicitly scopes it to "fixed and shared, not learned." Correct.

---

## Bottom line

- **Strongest, robust evidence:** per-item within-op vs across-op reader **cosine** (§6, §10,
  Phase-3 Table 1) and the same-parent query contrast — these survive the clean design.
- **Not robust as written:** the "11×/19×/26× op-over-fact variance" headline (§4-§5, A) —
  an artifact of a 2–4-level `lex` fact factor; the clean relational design gives 2.65×
  (Qwen) and <1 (Gemma, FAL-2a fired). Lead with the cosine instead.
- **Frozen FAL-3 statistic was never a valid commit locator** (argmax of a down-stepping
  plateau); firing is an artifact. Both FAL-1 and FAL-3 frozen locators were silently
  replaced by post-hoc robust ones; the confirm retest repairs this prospectively (VALID).
- **Input-invariant commit** is a VALID test of *location-fixedness* but under-powered as
  "scaffold vs ordinary recall," and SD 0.00 is partly a step-curve quantization artifact.
- **Single most valuable cheap follow-up (~10 min):** run the commit-location SD across facts
  on the existing random-init / shuffled Fig-A nulls. The read-site null was run; the
  commit-location null was not — and it is the one that would tell input-invariant commit
  apart from a locator+architecture artifact.
- Reviewer B is a tautological no-op at seq 17 (confound-removal, not a positive test);
  Reviewer C's "NOT_FV" is a weak/unit-coefficient negative. Both are hedged in the text,
  less so in the JSON verdict strings.
