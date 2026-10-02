# Round 2 — Interpretability reviewer (hostile but fair)

**Paper:** Time-Formed Circuits (Hollenbeck, 2026-10-02, ~10,525 words).
**Verdict:** workshop accept; borderline main-track (one revision away).
**Score: 6/10** (up from round-1's 5). Numbers re-spot-checked against the P1 `FINDINGS.md`
and the E20/E6/FLUX records — they reproduce. This is an unusually honest, well-instrumented
revision that answered most round-1 attacks with real experiments. It is held below a confident
main-track accept by three things: the title-level "formation" claim is only partially supported by
the authors' own numbers, the §5 identity indictment is substantially an out-of-basis artifact of
MLP transcoders, and the generality ceiling (≤4B, single seed, one lab, formation on one model).

---

## Part 1 — Did the round-1 attacks get answered?

| Round-1 attack | Status | Assessment |
|---|---|---|
| Formation vs propagation (the biggest) | **Partially answered** | Real experiment added (P1-A, §3.5, Fig 4). Rules out *linear* propagation (ridge R²=−0.13; predicted-band rescue 0.023). But the direct construction test (mid-freeze) narrowly **fails its own prereg** (0.197 < 0.20) and shows 77% of the store survives freezing — see fresh attack F1. The concept is better supported than round 1 but the framing still overclaims. |
| Item bootstrap is anti-conservative; cluster at identity | **Answered** | P1-B, §3.3–3.4, Table 2, App B. Whole-identity resampling, effective n reported (14/27/14/13), all block/rescue lower bounds > 0. Clean fix. Honest side-effect disclosed (wrong-id signed-fraction CI now includes 0 in 3/4 cells → control switched to candidate top-1). |
| E6 holds error nodes clean → near-tautological | **Answered well** | P1-C, §5, Fig 6. Now swaps features **and** error nodes; splits by behavior (identity still misses 0.31; color recovers 0.99). Turns a weak point into a sharper result. But the *reason* identity misses needs foregrounding — see fresh attack F2. |
| §5 title overclaims | **Answered** | Retitled to the identity store. |
| Four-quadrant buys little | **Answered** | §6.3 demotes it explicitly; block-and-rescue is now named the central result; additive-passes caveat kept. |
| Scale/30B deserves prominence | **Answered** | §10 leads with scale; 30B isolated-cut failure foregrounded. 9B still a TODO. |
| Cite Zhang&Nanda / Heimersheim&Nanda / Marks | **Answered** | All added (§9, References). |
| Fig 3 orphaned | **Fixed** | Now cited in §3.2. |
| Fig 5 caption mismatch | **Fixed** | Caption now describes grouped-by-behavior bars (but a number mismatch remains — F5). |
| Delta vs Geva/Agarwal buried | **Answered** | Per-stage delta table in §9. |
| ≥2 seeds | **NOT answered** | Still single execution seed throughout (L108, L281). The round-1 ask was explicit. |

Net: 9 of 11 attacks substantively resolved, 1 partially, 1 unmet. The response document is accurate
and the experiments are real. This is a strong-faith revision.

---

## Part 2 — Fresh attacks

### F1 (most important). "Formation" overclaims given the authors' own 77/23 split and the prereg miss.
The mid-freeze (freeze attn+MLP of the intervening layers L13–21 at the subject) drops the
transplant from 0.871 to **0.675** — i.e. **77% of the transplantable store survives with the
intervening interval doing nothing**; the intervening-interval contribution is 0.197, which
**fails the preregistered 0.20 bar** (reported honestly as a near-miss). Two further problems:
- Leg 1 ("late band 0.87 ≫ early band −0.03, so not propagation") rests on a strawman null. The
  FINDINGS states "pure propagation predicts early ≈ late" — that is false. Residual-stream
  propagation does *not* imply the identity is in K/V form at early layers; the consumer reads
  **late** K/V, and whether content is K/V-readable depends on each layer's K/V projection. "Early
  K/V doesn't carry it, late K/V does" is consistent with *residual propagation + late K/V readout*,
  and is nearly circular with "the store is the late K/V." So leg 1 does not discriminate.
- Leg 2 (linear map) rules out only *linear* propagation. Attention-mediated combination of the
  propagated seed with shared context is nonlinear and would also fail a linear fit, yet many would
  still call it propagation/routing rather than construction of new content.
So the discriminator is really leg 2 + leg 3, and leg 3 gives ~23% and misses its prereg.
**The honest conclusion is "the K/V store is late, is not a linear image of the seed, and intervening
construction contributes ~23%" — not "formation rather than propagation."** This matters because
"Formed" is in the title and the abstract (L18) and conclusion (L295) assert formation outright.
Also: formation is demonstrated on **one model** (Qwen2.5-1.5B); Gemma P1-A is in flight.

### F2. The §5 identity miss is substantially an out-of-basis artifact of MLP transcoders, not a general attribution-graph failure.
§5 (esp. L179) already concedes the store "lives in the attention-formed key/value and residual
state that… the MLP-replacement basis cannot express." Circuit-tracer's transcoders replace **MLP
sublayers**; attention is not decomposed into swappable feature nodes. So an all-layer/all-position
feature+error interchange **cannot** reach an attention-formed store **by construction** — the swept
feature set never spans attention. The identity result ("features+error move 0.31 vs native 0.94") is
therefore close to definitional, and a frontier-interp reader will see it as such. The title "An
attribution-graph **basis** misses the formed identity store" generalizes past what was tested (a
*MLP-transcoder* feature+error basis). Compounding this: the native K/V cut and the feature op are
**not matched in intervention magnitude** — the native cut perturbs the entire attention pathway, the
feature op perturbs MLP features+error — so 0.31-vs-0.94 conflates basis-coverage with how much state
each operator touches. The honest, still-interesting claim is: *MLP-transcoder circuits are
structurally blind to an attention-formed store; this is a coverage limitation Marks 2024 /
Ameisen 2025 would acknowledge.* State the mechanism up front, scope the title, and either test an
attention-inclusive operator or bound the claim to MLP-transcoder circuits. (Note Fig 6 identity
features+error CI ≈ [0, 0.57] at n=12 — the 0.31 point is also underpowered.)

### F3. Novelty remains incremental; the real deltas are operators, not a phenomenon.
- vs **Meng 2022 (ROME)**: ROME's corrupt-restore tracing ≈ the source intervention; ROME edits the
  located MLP. The paper's delta is the formed-store **transplant** + the isolated cut. Fair, but the
  §9 delta table omits a Meng/Hase row — add it.
- vs **Geva 2023 / Agarwal 2026**: enrich→propagate→extract + deferred commitment. The genuine new
  piece is **transplant into a fresh unseeded recipient** (block+rescue dissociation). But this is
  methodologically **resample/interchange activation patching with a particular source/target
  choice** — the *operator* is standard; the contribution is the dissociation design and the
  interpretation. Do not imply the operator is new; cite the resample-ablation lineage at the
  transplant.
- vs **Marks 2024 (SFC) / Ameisen-Lindsey 2025**: §5 is a coverage stress-test of their basis, not a
  new method (see F2).
The one thing I will remember remains the **isolated-vs-in-forward gap (0.985 → 0.009, L62)** — a
genuinely useful, under-practiced hygiene result — plus the cross-family + held-out dissociation.

### F4. Provenance statement contradicts the experiment record.
The paper (App A, L301) and README say the P1 custody audit is "in progress, so those numbers may be
revised." The source `FINDINGS.md` header says **"Custody (2026-10-02): PASS … FROZEN,"** with
byte-identical predictions across three FROZEN.json versions. The central round-2 evidence is being
needlessly undermined by a stale caveat (or the FINDINGS overclaims). Reconcile; if the audit passed,
drop the "may be revised" hedge.

### F5. Numerical inconsistency in the color feature-only interchange.
Three different "feature-only color" numbers: Fig 5 caption **0.42** (L174, labeled "all
layers/positions"), Fig 6 **0.36**, P1-C text **0.313** (vs library 0.344, L177); §5 text says
subject-position-all-layer = 0.31–0.42 but every-position-all-layer = 0.32–0.34. Fig 5's 0.42 is a
subject-position value mislabeled as all-position. Identity is also 0.08 (Figs 5/6) vs 0.044 (P1-C).
Reconcile to one value per scope and label scopes explicitly.

### F6 (minor). Single seed; FLUX threshold-dependence.
All decoder results are single execution seed — a load-bearing dissociation deserves ≥2 seeds on at
least the Qwen original panel. The FLUX "strict path-distributed, no LM cell matches" verdict is
threshold-defined (0.913 vs 0.90 line; single call already 0.562) — already hedged in §6.3; a
threshold-sensitivity curve would close it.

---

## Part 3 — Clarity / length (~10.5k words)
Long but within interp-venue norms. Trimmable ~15–20% without loss: move §8 (computed intermediate
state) to an appendix — it is tangential to the formation/commit/consume thesis and already demoted.
The abstract (L18) packs mid-sentence hedges ("though a weighted additive mechanism also passes…");
tighten. Neologisms ("time-formed," "space circuit") are now defined but heavy; a one-line glossary
would help. Figures are honest and legible; Fig 5's title "the formed store is invisible to the
feature basis" is identity-true but color-false (feature-only moves color 0.42) — retitle to the
split-by-behavior result.

---

## Top-5 must-fix

1. **Correct the formation framing (F1).** §3.5 L145–151, abstract L18, §11 L295. Report the
   0.675/0.871 = 77% survival explicitly; state the construction contribution is ~23% and the
   freeze-drop (0.197) is below the 0.20 prereg; drop the "pure propagation predicts early ≈ late"
   null (it is wrong). Change "formation rather than propagation" → "the store is late, not a linear
   image of the seed, and intervening construction contributes a distinct ~23% component." Flag the
   single-model (Qwen-only) scope.
2. **Scope §5 and state the mechanism of the miss (F2).** §5 title L163 and body L165–185. Say up
   front that transcoders replace MLP sublayers so an attention-formed store is out-of-basis by
   construction; retitle/qualify "attribution-graph basis" → "MLP-transcoder feature+error basis";
   report the residual-state fraction each operator perturbs to defuse the magnitude asymmetry; add
   the n=12 identity CI. Either test an attention-inclusive operator or bound the claim.
3. **Reconcile the P1 custody statement with the record (F4).** App A L301 + README say "in progress";
   `FINDINGS.md` says PASS/FROZEN. Update the paper; if passed, remove "may be revised."
4. **Add ≥2 seeds on at least the Qwen original block/rescue panel (F6).** L108, Table 2, L281. Show
   the dissociation medians are seed-stable, or state the single-seed limitation adjacent to Table 2,
   not only in §10.
5. **Fix the color feature-only number inconsistency (F5).** Fig 5 caption L174 (0.42) vs Fig 6
   (0.36) vs P1-C L177 (0.313); identity 0.08 vs 0.044. One value per declared scope, scopes labeled.

## Nice-to-haves
- Add a Meng-2022 / Hase-2023 row to the §9 delta table; cite resample-ablation lineage at the
  transplant so the operator is not read as new.
- Move §8 to an appendix; tighten the abstract; add a glossary line for the neologisms.
- Retitle Fig 5 to match the split-by-behavior result.
- State plainly in Table 2's text that the wrong-identity signed-fraction control went
  non-significant under clustering (3/4 cells) and that top-1 is now the content control — so it
  doesn't read as post-hoc.
- Land the Gemma P1-A replication to make formation more than a single-cell claim.
- Report a FLUX threshold-sensitivity curve for §6.

## Would my team read/cite?
Yes — the isolated-cut hygiene result and the matched feature+error interchange coverage gap. The
cross-family + held-out dissociation is solid and reproducible. Not yet as a new category, and not
yet as settled evidence that formation (vs late K/V readout of a propagated seed) is the dominant
story. Fix 1 and 2 and this clears a main-track bar; as written it is a strong workshop paper.
