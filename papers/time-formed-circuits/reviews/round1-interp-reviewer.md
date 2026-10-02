# Round 1 — Interpretability reviewer (hostile but fair)

**Paper:** Time-Formed Circuits (Hollenbeck, 2026-10-02). **Verdict:** workshop accept; main-venue reject. **Score 5/10.** Numbers spot-checked against `saturn/experiments/.../analysis.json`, FLUX and E6 findings — all match the manuscript; this is an honest, well-instrumented paper. The problem is conceptual novelty and two load-bearing comparisons.

## Thesis (as I read it)
Some circuits are built over execution order: a *source* seeds state, the model *forms* it over an interval, *commits* it to a store with independent authority, and a *consumer* reads it — and because source/store/read localize to different places, single-site patching and attribution graphs disagree about "where the circuit is." Memorable? The framing is clean but close to prior art; the one thing I will actually remember is the isolated-vs-in-forward gap (L56: 0.985 → 0.009), which is concrete and useful.

## Novelty
This is enrich→propagate→extract (Geva 2023) plus deferred commitment (Agarwal 2026) with better operators, not a new phenomenon. The late-band "formed store" ≈ Geva's extraction-ready subject enrichment; "commit" ≈ Agarwal's late generation-controlling commitment. Real deltas: (1) the **isolated cut** (finish prefix, overwrite only cached K/V, run only later positions) — genuinely under-practiced and the 0.985/0.009 result is a real cautionary contribution; (2) **full window sweeps** overturning sampled 2-layer certificates; (3) **transplant into a fresh recipient** across 3 families + held-out; (4) **exact-row read join**. These are solid methodological refinements. But "time-formed circuit" as a *new category* will not clear a main-venue bar — it repackages known structure. Section 9 cites the right predecessors; it does not cite Zhang & Nanda (2023) or Heimersheim & Nanda patching guides, which is where the isolated-cut insight actually lives (noising/denoising, resample ablation, patch placement), nor Marks 2024 on error nodes (central to §5).

## Methodological attacks
1. **Is "formation" just forward computation renamed? (biggest)** The seed is a *clean, ground-truth* residual injected at L12; the recipient then runs normally. Block = necessity patch on late K/V; transplant = sufficiency (resample) patch of that band into a neutral host. Nothing here distinguishes **formation** (the late layers construct content not present at the seed) from **propagation** (the seeded residual rides the stream and is projected into late K/V). The wrong-identity and earlier-band controls establish content-specificity and late-ness, not construction. §3.5 half-concedes this ("recipient-native … not donor-free"), which undercuts the "formation" label. Until a seed-layer-vs-late-band head-to-head shows the late band beats a linear image of the seed, the central concept is soft.
2. **Isolated vs in-forward:** genuinely convincing and the paper's best idea. Keep it; frame it as correct-patching hygiene.
3. **Statistics:** n=42 = 14 identities × 3 contexts (L102). Item-bootstrap over 42 correlated rows treats 3 copies of an identity as independent → anti-conservative CIs (note block CI upper bound 1.03, read restore 1.22, L106/L139 overshoot = noise). Cluster at the identity level; report effective n. Single execution seed throughout.
4. **Four-quadrant certificate (§2.3/§6):** the authors show a weighted mean passes it and *no* LM cell passes it, so by their own account it names a support profile, not a mechanism — then what does it buy? The FLUX headline rests on all-four = 0.913 vs a 0.90 line while a single call already reaches 0.562; the signature largely reflects threshold choice. Honest, but thin as a "contribution."
5. **E6 fairness (indictment of circuit-tracer):** partly circular. The interchange holds error terms at clean values (L151, Appendix B), and the paper's own diagnosis is that identity *lives in* the transcoder error (L159, findings L147). So "features can't move it" is close to tautological — it restates the known transcoder-reconstruction limitation (error nodes are first-class in Marks 2024 / Ameisen 2025; ~30% influence through them, L149). A fair matched operator would also swap error nodes. One transcoder set, one model, 12+8 items. Fair *demonstration*; the §5 title "Standard single-site tools miss the formed store" overclaims.
6. **Scale:** ≤2.8B, and Qwen3-30B's in-forward certificate did **not** survive the isolated cut (L250) — reported honestly, but it actively weakens the generality claim and deserves prominence, not a limitations footnote.

## Over/underclaims (lines)
- **Overclaim** L145 §5 title; L28/L133 "form"/"formed store" (vs propagation); L90 "genuinely distributed" is true only at the layer grain (conceded L252).
- **Underclaim / good hygiene** L18 and L194 (additive passes the signature); L250 (30B failure); L108/L123 controls.
- **Honest** all headline numbers reproduce from records.

## Clarity / figures (opened all six)
Fig 1 legible, honest (0.92/0.77/0.74 block; −0.26 Gemma wrong-id shown). Fig 2 heatmaps clear. **Fig 3 is never cited in the body** — orphaned; wire it or cut it. Fig 4 clean but shows how narrow the FLUX pass is. Fig 5 is honest but its caption (L156–157, "Left bars… Right bars…") does **not** match the figure, which is grouped by identity/color. Fig 6 is a good honest refutation (write ≫ clock, 6/6). "space circuit" (L60) and "time-formed" are under-motivated neologisms.

## Would my team read/cite? Yes — the isolated-cut result and the error-node demonstration. Not as a new category.

## Six changes that most raise the score (ranked)
1. Add a **formation-vs-propagation** discriminator (seed-layer vs late-band sufficiency; beat a linear seed image).
2. **Honest statistics:** identity-clustered bootstrap, ≥25 distinct identities, ≥2 seeds.
3. **Fair E6:** also intervene on error nodes / engage Marks 2024; soften §5 title.
4. **Delta table vs Geva & Agarwal**, quantified per claim; cite Zhang & Nanda / Heimersheim & Nanda for the isolated cut.
5. **Demote or de-risk the strict signature** (add a mechanism-discriminating test, or make it a short observation; more FLUX seeds/thresholds).
6. Land the **7–9B replication**, foreground the 30B failure; wire/cut Fig 3; fix Fig 5 caption.

## Three experiments that would most change my mind (~10 min, ≤9B)
- **A. Formation test:** on Qwen2.5-1.5B, transplant L12 seed-layer K/V vs L22–27 late-band into the fresh recipient. Late ≫ seed, and late not reconstructable by linear map of seed ⇒ formation is real.
- **B. Clustered re-estimate:** rerun E20 with ≥25 identities, bootstrap at identity level, 2 seeds. Does block/rescue survive honest CIs?
- **C. Fully-matched E6:** redo interchange swapping features **and** error nodes to filler on Gemma-2-2B. If that moves identity ≈ native, the claim is "transcoder error," not "tools miss the store."
