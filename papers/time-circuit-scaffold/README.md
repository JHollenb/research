# Dynamic Circuits Loop Through a Stable Time Scaffold

Paper 2 of the circuits pair, by Jacob Hollenbeck. The architecture paper.
Companion: Paper 1, [Time-Formed Circuits in Transformers](../time-formed-circuits/paper.md).

- Manuscript: [paper.md](paper.md)
- Figures: [figures/](figures/)
- Reviews, briefs, and rebuild notes: [reviews/](reviews/)

## Status

Submission manuscript, 2026-10-05 (findings-first rebuild). The manuscript now leads with the
measured findings (§1), states the hypothesis and a C1–C8 falsifier scoreboard (§2), adds related
measured results from the same runtime framed as static-infrastructure-versus-dynamic-routing (§3),
states the prior-art delta (§4), and gives an outside-replication list (§5). The full within-family
evidence for the seven architecture properties, the diffusion scene-generator controls, and the
disclosed retractions are carried by the companion paper and the superseded
`../scaffolds-and-dynamic-circuits/` drafts. Formal backbone:
`reviews/architecture-math-2026-10-02.md`; architecture brief:
`reviews/architecture-brief-2026-10-02.md`; rebuild log: `reviews/rebuild-notes.md`.

Thesis (the named hypothesis): **dynamic circuits loop through a stable time scaffold.** The
scaffold is a reusable organization of causal roles (source, reader/transition, writer, carried
state, consumer), identified by intervening on recurring roles rather than by a layer index. The
headline sentence is a framing no deterministic stateful network can violate; the falsifiable core
is a **store/router factorization**, scored in the paper. The surviving statement is: a late commit
band exists per model for this task family, its location is architecture-dependent, and it must be
found causally rather than by attention salience.

All numbers measured through the unchanged native consumer on stock Hugging Face eager
execution (float32 for language/SSM; native pipeline precision for diffusion, RGB equality by
decoded-array and hash). Effective n stated per claim; most LM/SSM results single-seed,
diffusion panels 2–5 seeds. Experiment identifiers and job IDs are confined to Appendix C.

## Abstract

A trained language model, read for factual recall, factors into a small store that later computation
reads by address and an input-dependent routing program computed from carried state. We report that
factorization findings-first. (1) A byte-identical stored key/value state takes different causal
authority when only the question changes: patching the queried fact adds a median 3.130 nats of harm
for color (16 of 16) and 0.583 nats for position (16 of 16). (2) A 24-coordinate reader profile
frozen before evaluation predicts held relation effects in all eight contexts, beating three sealed
competitors (cosine 0.954 vs 0.566), and permuting the two trained value projections collapses it
(relation 0.955 to 0.049). (3) Fine-tuning conserves where the store is read while rewriting how it
is routed, and the band code transfers base-to-derivative (0.92) but not derivative-to-base (coder
0.34, math 0.05). (4) A fit-free locator predicts the commit band blind in two new families (Phi-2 6
of 6, OLMo-2 5 of 6) but reads salience, not causality: on deeper models the necessary band must be
found by causal search (GPT-2 XL block 0.888 at the causal band vs 0.160 at the blind band). (5) One
band frozen before data ties a strong per-input rival across three operation classes (0.85 to 1.00).
(6) The cross-family common role graph is a null, and a function-vector account of the reader fails.
Of eight commitments, six hold for this task family, one fired this week (blind findability in deep
nets), and two more are narrowed by firings this week (band-only key/value retrieves at 0.000;
borrowed routing smuggles a donor's answer through MLP gates). Evidence is one laboratory, one
harness, mostly single seed, at and below 7B. (Full abstract in paper.md.)

## Evidence map (property → claim → source)

Paths relative to `~/domains`. "Companion" means the claim is carried by Paper 1 and cited here.

| Property | Claim | Effective n / model | Source |
|---|---|---|---|
| 1 | FLUX same-organization profile 0.913 vs 0.734 across; late image seam strongest 8/9 | 7 families; FLUX.2 Klein 4B | `saturn/experiments/2026-08-26-flux-rosetta-format-ontology-recurrence/FINDINGS.md` |
| 1 | Eye color/geometry share 5–7 of top 8 heads; source rows share 10–15/64 | 4 cases; FLUX.2 Klein 4B | `research/demos/scene-editing.md` |
| 1 | One fixed L22–27 interface: color 16/16, position 12/16, identity 11/11 | 16/op; Qwen2.5-1.5B | `saturn/experiments/2026-10-01-qwen-scaffold-context-poc/FINDINGS.md` |
| 1 | Store role at rel depth 0.69–0.83 (Mamba), late band at 7B; hybrid lowers to attention | Mamba 130M–2.8B; Qwen2.5-7B; Falcon-H1-0.5B | `.../2026-09-30-mamba-full-layer-sweeps/FINDINGS.md`; `.../2026-10-02-scale-9b-scaffold/PAPER-SECTION.md`; `.../2026-10-01-e14-hybrid-attn-ssm/FINDINGS.md` |
| 1 | One recurrent state serves identity and capital | 12; Mamba-130M | `saturn/experiments/2026-10-02-mamba-operation-clock-debugger/FINDINGS.md` |
| 2 | Same bytes, different query → query-selective harm 3.130/0.583/3.021 nats, 16/16 | 16/op, 128 checks; Qwen2.5-1.5B | `saturn/experiments/2026-10-01-qwen-scaffold-context-poc/FINDINGS.md` |
| 2 | Reader re-weighted not rebuilt: per-item within-op 0.74–0.99 vs across-op 0.204/0.218 | 40 facts; Qwen2.5-1.5B, Gemma-2-2B | `.../2026-10-02-site-variance-decomposition/FINDINGS-addendum-draft.md` |
| 2 | Shared value routes L23/KV0/V, L22/KV1/V; within-binding 0.95; cross-op 0.336 | Qwen2.5-1.5B | `saturn/experiments/2026-10-01-qwen-head-edge-topology/FINDINGS.md` |
| 2 | Address (K) vs payload (V): K×V interaction α_s(1−α_s)(E−1)/D·Δv; SDXL 0.72/0.66/0.72/1.0, Δ 0.3413; joint-perm invariance OPEN (0.859) | SDXL factorial | `research/demos/docs/scene-generator-paper.md` §5.2; math doc §4 |
| 2 | Static bus, dynamic query: K/V byte-identical, candidate-vs-base Q cosine 0.9999→0.8399 as carried states diverge | SDXL | `research/demos/docs/scene-generator-paper.md`; `.../scene-generator/sources/qkv-findings.md` |
| 3 | E20 source→formed store block 0.924 / rescue 0.871; replicates Gemma/SmolLM2/held-out Qwen and 7B (rescue 0.770, block 0.595, wrong −0.026) | 42/34/79/40 | `.../2026-09-30-full-layer-sweeps/FINDINGS-E20-mediation.md`; `.../2026-10-02-e20-cross-family/FINDINGS.md`; `.../2026-10-02-scale-9b-scaffold/PAPER-SECTION.md` |
| 3 | Recipient formation (L12 seed) rescue 16/16, block 14/14; early-band patch donor 0/15; Python/copy generality | Qwen2.5-1.5B | `.../2026-10-01-qwen-scaffold-context-poc/FINDINGS.md:62`; `.../2026-10-01-qwen-formation-replay/FINDINGS.md` |
| 3 | Formation over time (prereg; decisive P2a/P3b falsified, thesis refined): best single layer 0.732/0.804; freeze band attn+MLP 0.904/1.023 (F2 fired); cut consumer→subject 0.871→0.010, 0.985→0.015 | 42/model; Qwen, Gemma | `saturn/experiments/2026-10-02-formation-over-time/results/FOT_analysis.json` |
| 3 | Install timing decides edit; call-0 lesion MAE 20.82 vs call-14 2.15; temporal closure 0.712/0.403/exact | FLUX.2 Klein 4B | `research/demos/scene-editing.md`; `.../artifacts/closure/temporal-closure-summary.json` |
| 3 | Mamba transition composition 3/3 vs endpoint-sum 0; L0→L18–20 donkey/Vienna +4.59/+7.65, restore removes 90–92% | Mamba-130M | `.../2026-09-03-mamba-transition-conjunction-rosetta/FINDINGS.md`; `.../2026-10-01-connected-architecture/mamba/FINDINGS.md` |
| 3 | Mamba commit = write, not clock (retest γ=15–142): release hurts 0/6, dt via write 6/6, writer-specific 1/6 | Mamba 130M/370M/2.8B | `saturn/experiments/2026-10-02-mamba-clock-retest/FINDINGS.md` |
| 4 | Two-update France→Germany (1/3 held + dev); route→write→future key-only exact, L23–27 closure 3 held | Qwen2.5-1.5B | `.../2026-10-01-scaffold-confirmation/qwen-feedback/FINDINGS.md`; `.../2026-10-01-qwen-route-write-future-attribution/FINDINGS.md` |
| 4 | History×row: history +1.28–1.58, row opposing, total +0.96–1.43; retained-history fit 0.0995 | 4 held; Qwen2.5-1.5B | `saturn/experiments/2026-10-01-scaffold-graph-identification/FINDINGS.md` |
| 4 | Mamba S2 closure exact; fresh CPU dog→cat +2.74 (conv-dominant); SDXL stale-writer diverges later | Mamba-130M; SDXL | `.../connected-architecture/mamba/POST_HELD_FINDINGS.md`; `.../scaffold-graph-identification/mamba-cpu/FINDINGS.md`; `.../connected-architecture/diffusion/FINDINGS.md` |
| 5 | Frozen 24-coord relation profile 8/8 (0.954 vs 0.566); Mamba 27-coord capital 8/8, identity 4/4 | 8; Qwen2.5-1.5B / Mamba-130M | `.../scaffold-confirmation/qwen-predictive/FINDINGS.md`; `.../mamba-operation-clock-debugger/FINDINGS.md` |
| 5 | Cross-family formed-state→consumer core RMSE 0.0928 vs 0.8526 (n=2+2+1); color reader misses 8/8 | FLUX+Mamba+Qwen | `saturn/experiments/2026-10-01-scaffold-confirmation/cross-family/FINDINGS.md` |
| 5 | Fit-free locator predicts commit band blind: Phase A mean IoU 0.615 vs depth 0.490 (Pythia peak L16 = commit, 0.571 vs 0.000; Gemma miss); Phase B Phi-2 6/6 (block 0.515 vs depth 0.065), OLMo-2 5/6 (S5 single-layer fail) | 4 Phase-A cells + 2 blind (Phi-2 / OLMo-2-1B); Qwen-7B deferred | `saturn/experiments/2026-10-02-attention-band-locator/FINDINGS.md`; `results/phaseA_scorecard.json`; `results/phaseB_scorecard_{phi2,olmo2}.json` |
| 6 | v_proj row permutation collapses profile (0.955→0.049); null nets collapse, top-1 0/96 (incompetent) | Qwen2.5-1.5B | `.../scaffold-confirmation/qwen-predictive/FINDINGS.md`; `.../2026-10-02-p2-reviewer-experiments/results/A_analysis.json` |
| 6 | Pythia developmental trajectory; continuation training writer +0.445 vs matched-depth ~0 (Mamba wrong-label +0.448) | Pythia; Qwen/Mamba | `.../scaffold-dynamic-circuits/development/FINDINGS.md`; `.../2026-10-02-native-role-learning-timeline/FINDINGS.md` |
| 7 | Scene compiler 21/21 byte-exact, 7 specimens (3 SDXL-family) / 5 families; FLUX.2 wrong-source 54.5–94.3, wrong-sign 60.0–89.3, perm 4.6–22.8 (SDXL wrong-sign 94.29) | 7 specimens, 5 families | `research/demos/docs/scene-generator-paper.md`; `.../reports/cross-model-replication.json`; `.../reports/flux2-klein.json` |
| 7 | XNOR inverts 148/150; frozen-site install 1.011 vs −0.133; page-out 0/96; archive 4/4 vs 0/4; ancestry 6/6 vs 1/6 | Qwen/Mamba | `obsidian/2026-08-17-151407-...md`; `.../scaffold-dynamic-circuits/ar/results/panel-02e83e9ae183/report.json`; `.../source-frame-stack/FINDINGS.md`; `.../spectral-virtual-context/FINDINGS.md`; `.../2026-09-25-book-index-two-source-coherence/FINDINGS.md` |
| 10 | Cross-family common graph NULL: connected forecast ties additive (0.015099); role-matcher gap 0.0386 | 3 held; Qwen route | `saturn/experiments/2026-10-01-connected-architecture/qwen/FINDINGS.md`; `.../scaffold-dynamic-circuits/ssm/E4_ALIGNMENT.md` |
| 11 | Attribution graph sees L0, misses commit band (≤0.08 vs 0.83 K/V cut) | companion; Gemma-2-2B | `saturn/experiments/2026-09-30-circuit-tracer-head-to-head/FINDINGS.md` |

## Figure sources

| Figure | Content | Source |
|---|---|---|
| fig_scene_compiler_flux2.png | Teaser (§1) + property 7: compiled = native, wrong source / wrong sign / permute | scene-generator cross-model proof sheet |
| fig1_scaffold_schematic.png | Role-graph schematic (§2) | authored |
| fig3_same_patch_query.png | Property 2: same-patch / different-query harm | scaffold-context FINDINGS |
| fig4_reader_cosine.png | Property 2: per-item reader cosine within-op vs across-op | decisive-test panel F3 |
| fig_k_address_v_payload.png | Property 2: K address, V payload (SDXL factorial) | scene-generator binding sheet |
| fig_eye_color_timing.png / fig_eye_geometry_timing.png | Property 3: install timing on the time axis | scene-editing reproduction |
| fig_chair_transport.png | Property 3: spatiotemporal conjunction | transport experiment |
| fig6_confirmation_results.png | Property 5/6: frozen profile + v_proj permutation | scaffold-confirmation |
| locator_R_curves.png | Property 5 (§7.1): fit-free locator R_ℓ curves, locator vs true vs depth band, Phase A + blind Phase B | attention-band-locator figures |
| fig9_qkv_controls_proof.png | Property 7: wrong-source / wrong-sign / shuffled controls | scene-generator control sheet |
| fig7_honest_null.png | §10: connected-forecast tie + role-matcher null | authored |
| fig2_band_location.png | Appendix D1: commit-location (weak symptom) | decisive-test panel F1 |
| figA_null_variance_split.png | Appendix D2: read-site split learned, nulls incompetent | reviewer experiment A |
| figB_commit_by_layer_typeswap.png | Appendix D3: sliding-window type-swap no-op | reviewer experiment B |
| figC_fv_reproduction.png | Appendix D4: additive FV weak negative | reviewer experiment C |

Removed from the body: `fig5_variance_decomposition.png` (its variance-ratio panel is superseded by the
per-item reader cosine and the clean 2.65/0.72 ratio; see `reviews/rebuild-notes.md`). `fig8_scene_compiler_proof.png`
is superseded as a teaser by `fig_scene_compiler_flux2.png`.

## What is deliberately excluded or demoted

- The cross-family common role graph is a null (§10), not a headline.
- The commit-layer index, the lexical-set variance ratio, the FAL locators, the confirm-color retest,
  the incompetent null nets, the sliding-window type swap, the function vector, and the pre-band freeze
  are location-index / proxy checks: they go to §13 and Appendix D with their limits, not the spine.
- The diffusion 21/21 result is architectural custody (the prompt enters only through the compiled
  source), not a discovery; the discoveries are the K/V factorization, time-indexed authority, and closure.
- Scene results are replay parity, reproducing native mistakes; compiled programs are donor-derived and
  installed at host addresses; no donor-free compiler, no instance binding, no shared tensor binary.
- Internal tooling names, experiment codes, and job identifiers are confined to Appendix A.
- The retired causal-mask-defective feedback instrument is named once in Limitations.
