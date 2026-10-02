---
title: "Evidence inventory for Paper 2 (time-circuit-scaffold): every experiment bearing on the thesis"
type: review
date: 2026-10-02
scope: "~/domains/saturn/experiments (2026-08..2026-10-02), ~/domains/obsidian/blog (last ~3 weeks), research/papers/{time-circuit-scaffold,time-formed-circuits,space-and-time-circuits,scaffolds-and-dynamic-circuits}, submission-review-2026-10-02.md"
method: "Read-only. Paper 2 paper.md + README evidence map read directly; 3 parallel read-only inventory agents over the experiment tree + blog + sibling papers; highest-value items (7B scale, E20 cross-family job IDs, retractions, alias-binding, scaffold-graph, product-store, CoT) re-verified by direct read of FINDINGS files."
note: "Excludes blind-final-boss-certification and grail tool outputs per instruction. No paper edits, no model runs."
---

# Evidence inventory — the scaffold / space-circuit thesis

**Thesis under test (author's words):** the *architecture is the time circuit*, which works as a scaffolding — a FIXED schedule of causal stages built over ordered execution (seed → formation → commit → store → consumer) whose **location does not move with the input** — and **space circuits** (which reader/row/coordinate is used) form **dynamically per input/operation** on top of it.

**Citation status key:** `P2` = cited in Paper 2 (time-circuit-scaffold); `P1` = owned by companion Paper 1 (time-formed-circuits) and cited there, not in P2 by design; `NEITHER` = in no current submission; `ALLUDED` = mentioned in P2 prose but not cited as evidence. **Support key:** SCAFFOLD (fixed location/commit/weights) / SPACE (per-input read/row/reweight) / BOTH / NEITHER (infra or off-thesis). All language-model and Mamba cells are **single-seed** unless noted (prototype-first policy); FLUX panels use 2–5 seeds (declared exception). "custody PASS" = independent verifier + hash-chain receipts.

---

## A. What Paper 2 currently cites (the anchor)

Paper 2's own evidence map (paper.md §Appendix A + README) already spans well beyond its stated scope: Qwen2.5-0.5B/1.5B, Gemma-2-2B, Pythia-410M/160m, Mamba-130M/370M/2.8B, FLUX.2 Klein 4B, SDXL, Qwen2.5-Coder-1.5B, and Qwen3-30B (XOR). Its **core preregistered test** (commit-invariance + variance split) is Qwen2.5-1.5B + Gemma-2-2B. Yet §1 line 39 and §12 say the scope is *"two transformer checkpoints of at most 2B parameters, four operations, short prompts, and a single checkpoint per model."* That sentence is the mismatch this inventory addresses: the thesis evidence is materially broader than the preregistered-test scope.

---

## B. Full experiment inventory

### B.1 Core preregistered / confirmation (CITED in P2)

| Dir / path | Model(s) + family | Measured | Numbers | Supports | Evidence status | P2? |
|---|---|---|---|---|---|---|
| `saturn/experiments/2026-10-02-site-variance-decomposition` | Qwen2.5-1.5B, Gemma-2-2B (transformer) | Decisive test: commit-location invariance + read-site variance split + 3 falsifiers + fresh-color retest | read-map coord 42.2% / coord×op 29.0% / coord×fact 1.1%; store necessity op 84.0% / fact 3.2%; per-fact commit SD Gemma 0.00, Qwen 1.16 (42 facts); within-op reader cosine 0.92–0.999 vs across-op 0.336 | BOTH | MEASURED, custody PASS. jobs job-9a3d0b5139ec (Qwen), job-06001771bc33 (Gemma); confirm job-8b550b584da4, job-b7d05acf8192. **FAL-3 fired as frozen in 2/6 cells** (Qwen color 5.45, Gemma identity 4.01); fresh-color retest clears all 3 locators | P2 |
| `.../2026-10-02-p2-reviewer-experiments` | Qwen2.5-1.5B + random-init/shuffled nulls (transformer) | A: variance-split null; C: function-vector equivalence | A: coord 42.2%→1.2–1.4% in nulls, op:fact 19.0→~1 (v_proj permute keeps 11.9), nulls top-1 0/96; C: additive op vector 0/14 flips, +2.19 nats, erases identity route | SCAFFOLD(learned) + SPACE(NOT_FV) | MEASURED, custody PASS. job-48af2d6fc73c (A), job-5d7cf4e4b3d8 (C). Caveat: A-P4 relation-reader margin also +0.350 in **random-init (failed prediction)**; FROZEN.json edited after jobs (freeze-timing) | P2 |
| `.../2026-10-01-scaffold-confirmation/qwen-predictive` + `/FINDINGS` | Qwen2.5-1.5B (transformer) | Frozen 24-coord reader profile vs 3 competitors; full v_proj row permutation | relation mapped cosine .954 vs .566 blind, RMSE .029 vs .149, 8/8 raw-RMSE; v_proj permute .955→.049 (relation); **color predicted ordering misses 8/8** | SCAFFOLD(weights) | MEASURED prospective; single seed | P2 |
| `.../2026-10-01-qwen-scaffold-context-poc` | Qwen2.5-1.5B (transformer) | Fixed L22–27 store serves identity/color/position; byte-identical patch, query-selective authority | query-selective harm median 3.130 / 0.583 / 3.021 nats, all 16/16; donor redirect color 16/16, position 12/16; 128 pairing checks pass | BOTH (lead SPACE result) | MEASURED; jobs …/08678fbc9188 +3 scenes. Identity readout-limited (11/16 readable) | P2 |
| `.../2026-10-01-qwen-frozen-reference-payload` | Qwen2.5-1.5B (transformer) | Frozen reference consumes separately-changed B payload | direct B 7/8, A preserved 8/8, refB follows fresh B 3/4; CPU 112/112 identical | BOTH | MEASURED prospective; 2 correlated contexts. Pointer-vs-copy unresolved | P2 (§8) |

### B.2 Scaffold location / formation / commit (companion-owned or cited)

| Dir / path | Model(s) + family | Measured | Numbers | Supports | Evidence status | P2? |
|---|---|---|---|---|---|---|
| `.../2026-09-30-full-layer-sweeps` (E16/E17/E19/E20/E11) | Qwen2.5-0.5B/1.5B, Pythia-410M, SmolLM2-1.7B, Gemma-2-2B (transformer); Mamba (SSM) | Write-once residual, isolated late commit band, window necessity, source→store mediation | commit L19–23 (~0.7–0.9 depth); E20 block 0.924 / rescue 0.871 (42 Qwen); E19 best-window always contains commit; Qwen1.5B early in-forward leak L0 0.985→iso 0.009 | SCAFFOLD + BOTH(E20) | MEASURED single seed; E20 job-e1f652e80f43. E11/E17 overshoot = commit redundancy, not leak | P2 cites E16/17/19/20 as companion |
| `.../2026-09-30-mamba-full-layer-sweeps` (E3b) | Mamba-130M/370M/2.8B (SSM) | Full native state-cut sweep: one concentrated late writer per cell | 130M L20 81%, 370M L39 67%, 2.8B L44 67% (0.69–0.83 depth); canary PASS | SCAFFOLD | MEASURED single seed. **RETRACTS E5** (sampling artifact) | P2 (§3 companion) |
| `.../2026-10-02-mamba-writer-clock-dose` | Mamba-130M/370M/2.8B (SSM) | Is writer "the layer that stops its clock"? matched clock/write/dt dose | write is larger lever 6/6; A-clock never hits −0.30 collapse (P1 false 6/6); clock-specificity false 5/6 | SCAFFOLD (commit = depth-fixed write port) | MEASURED, custody-corrected. jobs job-baf14cd06dd2/cbb0e8a57f45/e55fc32a16ed. **Refutes P1 "stops its clock" mechanism** | P2 (§3 companion) |
| `.../2026-09-30-mamba-writer-clock` | Mamba-130M/370M/2.8B (SSM) | Writer is a retention outlier (correlational) | writer cumdt 0.03–0.07, surv-rank 1–3/N, z +1.46..+4.29 | SCAFFOLD (correlational) | MEASURED, 1 prompt/cell. Write-magnitude-outlier REFUTED | NEITHER (superseded by dose) |
| `.../2026-10-02-scale-9b-scaffold` | **Qwen2.5-7B (transformer, PAGED fp32)**; Gemma-2-9B **unavailable** (gated 403) | Scale thesis to 7B: commit-band depth (P2), per-fact SD (P3), E20 (P4) | commit band median **L21 rel_depth 0.778 PASS[0.7,0.9]**, 100% commit L19–27; per-fact S2 SD 2.30 (strict-FAIL vs ≤1.5 but ≪ SD>4 falsifier; mode L21=68%); canary reproduces resident 1.5B L23 | SCAFFOLD (band depth-invariant at 7B) | MEASURED single seed. job-32fa0281137c (7B), job-0163b84499f1 (canary). **P4 (E20) PENDING; P1 N/A** (Qwen uniform attention) | **NEITHER** |
| `.../2026-10-02-p1-reviewer-experiments` | Qwen2.5-1.5B, Gemma-2-2B (transformer) | A: formation-vs-propagation; C: fair E6 error-node interchange | A: Qwen late 0.871 vs early −0.028, freeze-mid drop 0.197; **P-A4 freeze-noop falsifier FIRED both models**; C identity feat+error 0.13–0.31 vs native cut 0.94, color 0.99 | SCAFFOLD (formation, not propagation) | MEASURED, custody PASS. A job-802a7371546f/d37efcecae3e, C job-5b8f55665345 | P1 |

### B.3 Space-circuit: per-input read / row / reweighting

| Dir / path | Model(s) + family | Measured | Numbers | Supports | Evidence status | P2? |
|---|---|---|---|---|---|---|
| `.../2026-10-01-qwen-head-edge-topology` | Qwen2.5-1.5B (transformer) | GQA reader skeleton (fixed coords) + operation-specific weighting | recurring routes L23/KV0/V, L22/KV1/V; within-binding cosine .947/.927/.961; cross-op id↔relation 0.336 | BOTH (strong) | MEASURED; one scene/2 bindings; group-resolution causal | NEITHER (numbers partly surface in P2 §4) |
| `.../2026-10-01-qwen-alias-binding-feedback` | Qwen2.5-1.5B (transformer) | Source store + local reference selection + generated-state feedback | source rescue 98.90% / block 99.83%; held signs 3/3 eligible; generated-state rescue flips later answer 3/3 (bird→fox +12.7 / −7.3 nats); C selector preserves A/B | BOTH | MEASURED, custody. jobs job-535ba4f9b9e5 (held), job-2f40cd33f44e (controls). Reference not isolated from copied value; 2/4 cells incompetent | **NEITHER** |
| `.../2026-10-01-qwen-formation-replay` | Qwen2.5-1.5B (transformer) | Formation during inference; dynamic readers; executable memory (scene/code/copy/alias) | L11 seed read 8/8; late-anchor rescue identity/code/copy 2/2; late block→donor 8/8; shared coords L23/KV0/V, L22/KV1/V | BOTH | MEASURED; one scene/order; alias anchor-only limit | NEITHER |
| `.../2026-10-01-qwen-routing-mediation` | Qwen2.5-1.5B (transformer) | Selector changes attention routing; how much one L22 row carries | route-only carries 50%/14%/80% of selector effect; K/V direction retained ~91–98% | SPACE | MEASURED; 3 pre-opened contexts. **Fixes Transformers 5.14.1 causal-mask defect** in retired feedback instrument | NEITHER |
| `.../2026-10-01-qwen-route-write-future-attribution` | Qwen2.5-1.5B (transformer) | Route (L22) → new L23 K/V writer → later L23 read | total route effect +0.0215 dev; L23 transfer small & **counteracting**; L23–27 band reproduces future exactly; no answer flip | BOTH | MEASURED prospective; distributed, not single mediator | NEITHER |
| `.../2026-10-01-qwen-source-bridge-read-law` | Qwen2.5-1.5B (transformer) | Source-conditioned bridge formation + consequential L22 attention read | ψ negative 4/4; L22 V effect +2.4..+3.7 nats; FP64 recon 3.55e-15; no answer flip | BOTH | MEASURED prospective; 4 bindings/1 op. Landed 23:14–23:27, **after the paper** (review flag) | NEITHER |
| `.../2026-10-02-common-causal-graph` | Qwen2.5-1.5B (tr), Mamba-130M (SSM), SDXL (diffusion) | Conditional read→writer→formed-state→later consumer; retained vs formed paths | Qwen forecast bit-exact (fp64 3.9e-7), additive rival L2 1.5–4.6; new-band-only +0.022 vs whole +0.414 (color sign reversal); Mamba 2/4 held | BOTH | MEASURED; jobs job-6d6c63065c30 etc. Retained-history path can OPPOSE formed memory | NEITHER |
| `.../2026-10-01-scaffold-graph-identification` | Qwen2.5-1.5B (tr) + Mamba-130M (SSM) | Which state carries the effect: retained history vs new row | history b0 +1.28..+1.58 (4/4) vs new-row r0/r1 negative; τ +0.96..+1.42; **all 16 greedy answers stay base country (no flip)** | BOTH (graded) | MEASURED, independently reviewed. job-7610b9a5797d (held). New-row contribution counteracts; no unique graph | **NEITHER** |

### B.4 Formed state feeds later computation (reasoning / arithmetic — new operation class)

| Dir / path | Model(s) + family | Measured | Numbers | Supports | Evidence status | P2? |
|---|---|---|---|---|---|---|
| `.../2026-10-02-cot-formed-state-faithfulness` | **Qwen2.5 0.5B/1.5B/3B/7B** (transformer; bf16/fp32/nf4) | CoT step causal role splits token-visible vs hidden formed-K/V; repair vs scale | E2 hidden-state swap changes answer 1.00 (0.5–3B), 0.955 (7B); silent repair 0.188(0.5B)→0.762(1.5B); NF4 halves repair | SPACE (E2 dissociation holds) | MEASURED single seed. jobs job-87c47cb47c2b/e3c984961358/52b8771fc5ef; 7B job-050706578e6c **timed out (n=12 partial)**. **E1 "hidden channel" DEMOTED by addendum-2** (recompute-from-prompt; tracks_old=0 all scales). **Paper 4 parked 4/10; recommended fold into P2** | ALLUDED (§8 "in preparation") |
| `.../2026-10-02-qwen-role-aware-generated-chain` | Qwen2.5-0.5B-Instruct (transformer, CPU fp32) | Generated sum-state changes later freely-generated multiply+subtract (4 fresh contexts) | donor sum-state swap changes product+subtraction **4/4 fresh**; 20/20 arms complete; exact reinstall 4/4 | BOTH (fixed formation→consumption order) | MEASURED. jobs job-963d0b3b9e85/4f877c21b611. Native arithmetic correct only 2/4; no unique address | NEITHER |
| `.../2026-10-02-qwen-generated-product-store` | Qwen2.5-0.5B-Instruct (transformer) | Generated product-store mediation | dev product 44→41, block→8, rescue→41; held ctx1 30→26; held ctx2 EOS (evidence-incomplete) | SPACE (partial) | MEASURED. jobs job-a9b6e59f4ed4/ea94dcb135ec. No text-independent product pointer | NEITHER |
| `.../2026-10-02-qwen-product-store-continuation` | Qwen2.5-0.5B-Instruct (transformer, CPU) | Product-store continuation to EOS | 14/14 first-closure match parent; row2 EOS bare number | SPACE (partial) | MEASURED exploratory (`fresh_context:false`). Row2 instrument-incomplete | NEITHER |
| `.../2026-10-01-e10-completed-answer-rerun` | Qwen2.5-0.5B/1.5B (transformer) | Repaired-parser E10 CoT: completed-answer + timing | removal ends wrong 26/32 (0.5B) / **3/30 (1.5B, repairs 25/30)**; swap authorship 19/32, 30/30; late later-row removal wrong 8/8 | BOTH | MEASURED single greedy. job-527c598e9bc0/d637c4110a59. Corrects historical 15/32 → 19/32 | P1 (E10) |
| `.../2026-10-01-e10-cot-intermediate-steps` | Qwen2.5-0.5B/1.5B (transformer) | Are non-copied CoT steps causally used | single-step unmount flip 1.00; multi early-step 0/8 inert, consumed step 8/8 (Δ 7.3–7.6) | BOTH | MEASURED. **Prereg H2 REFUTED** (step IS single-site necessary); superseded by completed-answer-rerun | P1 (E10) |
| `.../2026-10-02-qwen-b-store-{layer-support,middle-split}` | Qwen2.5-1.5B (transformer) | Which layer band carries frozen B-value payload | direct-B 7/8–8/8, A preserved 8/8, expected-C 6/8–7/8 | SPACE (weak) | MEASURED exploratory; coarse split **does not isolate** repair from collateral | NEITHER |

### B.5 State-space (SSM) and hybrid

| Dir / path | Model(s) + family | Measured | Numbers | Supports | Evidence status | P2? |
|---|---|---|---|---|---|---|
| `.../2026-10-02-mamba-operation-clock-debugger` | Mamba-130M (SSM) | Shared country-history state serves identity+capital; prospective 27-coord profile | H-only successor transfer **12/12**; capital mapped cosine .9941 vs .9880 (8/8), delayed identity .9586 vs .9102 (4/4); clock dose near-cancellation | BOTH | MEASURED prospective. jobs job-9e4c98b7af35/777090f89576/bfd9c10291d6. Recent-identity 4 rows begin " also" | P2 (§7) |
| `.../2026-09-30-mamba-state-cut-certificate` (E5) | Mamba-130M/370M/2.8B (SSM) | (Original) Mamba certifies 4-quadrant at state cut | claimed single-site ≤2.4%, W2_all 1.00 | NEITHER (was BOTH) | **RETRACTED same day** (2-layer sampling artifact; no Mamba cell certifies) | NEITHER |
| `.../2026-09-30-mvm-mamba-cot` | Mamba-130M (SSM), Qwen2.5-0.5B (tr) | MVM state pages + CoT; copied vs computed step | VM sweep bit-exact vs E3b; copy-item necessity 0.84; two-hop non-copied unmount −0.015 (no flip) | SPACE (infra+probe) | MEASURED. bf16 run superseded (0.47 gap)→fp32. Tiny panel | NEITHER |
| `.../2026-10-01-e14-hybrid-attn-ssm` | **Falcon-H1-0.5B** (hybrid attn+SSM) | Attention vs SSM formed-state necessity/write | identity attn K/V −1.774 (17/22 flips, write 0.987); SSM −0.038 (2/22); color attn −2.289 | SCAFFOLD (partial; attn store) | MEASURED single seed. job-5efb5697631c. **Predicted concentrated SSM writer NOT found**; no strict certificate | P1 |
| `.../2026-09-30-black-mamba-quotient-theorem` | Black Mamba (trained SSM organism) | Exact phase-safe quotient impossibility + balanced truncation | exact min quotient = 32 (lemma); balanced trunc 98–99% @ r16; coord-select exact 0.65 | NEITHER (model-reduction) | **Laptop CPU replay, NO mrun job / no custody** (author: "does not yet count as evidence") | NEITHER |

### B.6 Diffusion (prompt-agnostic bus + per-prompt program)

| Dir / path | Model(s) + family | Measured | Numbers | Supports | Evidence status | P2? |
|---|---|---|---|---|---|---|
| `research/demos/scene-generator.md` + `.../cross-model-replication.json` | **5 families / 7 specimens**: WAI-SDXL, Illustrious-SDXL, FLUX.1-schnell, FLUX.2-Klein, Chroma1-HD, Krea2 (diffusion) | Prompt compiled to source K/V program installed into native run reproduces image byte-exact | **21/21 exact RGB (MAE 0.0)**; controls: wrong-sign 94.3, K-permute 78.4, wrong-source 79.9, base 59.4 | BOTH | MEASURED; job-5b20cdbb0f15; artifact-only cross-family join | P2 (§7/§10) |
| `research/demos/scene-editing.md` | FLUX.2 Klein 4B (diffusion), 4 matched cases | Write timing decides edit kind (early composition vs late appearance) | early eye P 0.577 (blue) vs late 0.069 (violet); 12 native refs + 24 outputs exact; 2-parent closure: both = exact | BOTH | MEASURED; job-eb10b3c02dc5 (56 images). Target-assisted; not RGB-exact (MAE 1.8–2.7) | P2 (§7/§10) |
| `.../2026-09-30-flux2-{joint01-time-accumulation,residual-deletion,offroute-span-sweep}` (E1/E1b/E1c) | FLUX.2 Klein 4B (diffusion) | Four-quadrant time signature; whole-path necessity under deletion; carrier redundancy | single-step write ≤0.56 vs all-step ≥0.91; route 6/6 certified; joint region redundant | SCAFFOLD | MEASURED 2–3 seeds; byte-exact canaries. **E1b "necessity counterfactual-only" and E2b FLUX "target survives" CORRECTED by E1c** | P1 |
| `.../2026-09-30-e7-flux-color-multiseed` (E7) | FLUX.2 Klein 4B (diffusion) | Multi-seed necessity (no single step necessary) | B1/B2/B3 5/5 | SCAFFOLD | MEASURED 5 seeds. Deletion non-specific; not a full write sweep | P1 |
| `.../2026-10-01-e8-klein9b-nine-gate` | **FLUX.2 Klein 9B** (diffusion) | Four-quadrant + nine-gate, identity+lighting | identity 8/9 gates, no single write ≥0.90 (max 0.48), all-step 0.90–0.95; lighting 7/9 | SCAFFOLD | MEASURED 2 seeds. jobs job-8dfc9cd970bf etc. No strict nine-gate certificate | P1 |
| `.../2026-10-01-e9-sdxl-four-quadrant` | SDXL (diffusion) | Four-quadrant on up1 route | single-step necessity steps 0/1 → source (space-like); all-step write 0.985 | SPACE(necessity)/SCAFFOLD(sufficiency) | MEASURED single seed. **Prereg primary "TIME" prediction REFUTED** | P1 |
| `.../2026-08-26-flux-cross-prompt-structural-grammar` (+ `flux-rosetta-*` cluster) | FLUX.2 Klein 4B/9B (diffusion), 7 families | Shared physical skeleton (bus) + per-prompt/seed weighted handoffs | shared-text spine 0.9106 vs prompt-specific 0.9597; hostile control 0.389; "route is a field, not a lookup table" | BOTH | MEASURED discovery, 1 seed/ckpt. Necessity/minimality unresolved | NEITHER (blog cited) |

### B.7 Space-circuit poles, read-join, induction (companion-owned)

| Dir / path | Model(s) + family | Measured | Numbers | Supports | Evidence status | P2? |
|---|---|---|---|---|---|---|
| `.../2026-09-30-e4-pythia-recovered-loss` (E4) | Pythia-70M step1000 (transformer) | Head-level writer/relay induction circuit | minimal 3-head set R_keep 0.92–1.05; writer N_ko 0.74–0.81 | SPACE (head coalition pole) | MEASURED, bootstrap CIs. job-19e98d8ac631/b69d8fc7654a | P1 |
| `.../2026-09-30-e12-bucket-exact-address` (E12) | Qwen2.5-0.5B, Qwen3-0.6B (transformer) | Model-derived address replaces selection step | bucket contains answer 1.00; bucket+exact = oracle (gap 0.000) | SPACE | MEASURED single seed | P1 |
| `.../2026-09-30-e13-time-circuit-read-join` (E13) | Qwen2.5-1.5B, SmolLM2-1.7B (transformer) | Read is localized at one late layer, join-replaceable | read best-single 0.07–0.22; single-layer restore 0.82–1.22; forced donor row authors donor 1.00 | SCAFFOLD+SPACE | MEASURED single seed. Raw-cosine bucket degenerate → fixed in E18 | P1 |
| `.../2026-09-30-e18-bucket-join-time-reads` (E18) | Qwen2.5-1.5B, SmolLM2-1.7B, Gemma-2-2B (transformer) | Standardized bucket; query-formable address vs semantic selection | repetition 1.00 vs **semantic/coref 0.00**; Gemma join works on sliding commit L22 | SCAFFOLD(commit=read) | MEASURED single seed. **NULL headline**: formable address finds subject 0% for identity/color/coref | P1 (semantic-address limitation) |
| `.../2026-09-30-isolated-swap-reruns` (E3) | SmolLM2-1.7B, Qwen3-8B (transformer); Qwen3-30B-A3B (MoE) | Full isolated-swap sweeps + public cert bundle | SmolLM2 color PASS, identity FAILS (L19 write 0.991); Qwen3-8B sufficiency textbook, necessity degenerate; 30B single-site −0.025/−0.029, W2_all 1.0376 | SCAFFOLD/mixed | MEASURED single seed. **RETRACTS SmolLM2-identity "time circuit" label**; 30B sampled only 2 layers | P1 (as scale caveat) |
| `.../2026-09-30-ablation-method-sensitivity` (E2b) | SmolLM2-1.7B, Qwen2.5-0.5B (tr); FLUX (diff) | LM sink robust to ablation method | all methods keep single-site <0.25, whole-path removes top-1 | SCAFFOLD | MEASURED single seed. **FLUX "counterfactual-only" RETRACTED by E1c** | P1 |
| `.../2026-09-30-circuit-tracer-head-to-head` (E6) | Gemma-2-2B + Gemma Scope (transformer) | Attribution graph vs native store cut | feature interchange moves identity ≤0.08, **0/20 flips**; biggest influence at L0; native K/V cut flips 0.83 | SCAFFOLD (tools blind) | MEASURED single seed. job-03225ce474d1/ed4ce1ac5974 | P2 (§11 companion) |
| `.../2026-10-02-native-role-learning-timeline` | Qwen2.5-1.5B (tr) + Mamba (SSM) | Does continuation-training change formed-state authority | Qwen writer +0.445 vs matched-depth ~0; **Mamba wrong-label control also +0.448** | SCAFFOLD (partial) | MEASURED. job-58b8ed5f2066. **Cannot date pretraining onset** (no authenticated checkpoint trajectory) | NEITHER |

### B.8 Cross-family / connected / externalization (nulls + infra)

| Dir / path | Model(s) + family | Measured | Numbers | Supports | Evidence status | P2? |
|---|---|---|---|---|---|---|
| `.../2026-10-01-connected-architecture` | Mamba-130M (SSM), Qwen2.5-1.5B (tr), Pythia, SDXL (diff) | Connected source→formed-state→read→continuation across families | Mamba monkey→donkey +4.59; Qwen connected +0.0215; **Qwen forecast ties additive, wins 1/3** | BOTH / **NULL** | MEASURED. Cross-family graph NOT distinguishable from addition | P2 (§9 null, qwen lane) |
| `.../2026-10-01-scaffold-dynamic-circuits` (ar + ssm + diffusion-text) | FLUX.2 Klein 4B, Qwen2.5-0.5B/1.5B, Mamba-130M/370M, Pythia-70M | Frozen-site install (program not vector); role-matcher alignment | frozen-site install right 1.011 vs wrong-site −0.133 vs shuffled −0.607; role-matcher 6.9125 vs depth null 6.9511 (**gap 0.0386 = null**); E1b above/below relation **FAILED −0.045** | BOTH / NULL | MEASURED exploratory. jobs job-02e83e9ae183 etc | P2 (§10 install; §9 matcher null) |
| `.../2026-10-01-scaffold-confirmation/cross-family` | FLUX + Mamba + Qwen (core = 2+2+1 rows) | Prospective cross-family formed-state→consumer edge | RMSE .0928 vs .8526 permute; color reader misses 8/8 | partial / NULL | MEASURED; effective n = 2+2+1 | P2 (§9) |
| `.../2026-09-24-spectral-virtual-context` | Qwen2.5-0.5B-Instruct (transformer) | Typed addressed page read from 2,048-page archive | routed 1-page 4/4; wrong-page 0/4; resident-only 0/4 | SPACE | MEASURED single seed. Merging independently-compiled pages answers only 1/4 | P2 (§10) |
| `.../2026-09-30-source-frame-stack` | Qwen2.5-0.5B (transformer) | Source scopes join to StateCuts without changing continuation | 24/24 exact (max diff 0); wrong-source flips 6/6; wrong-role abstains 9/9 | SCAFFOLD/SPACE | MEASURED. job-b1df140ac26a | P2 (§10) |
| `.../2026-09-30-qwen3-reverse-source-mechanism` | Qwen3-0.6B-Base (transformer) | Query-conditioned source selection + reader coalition | native 16/16; delete 8 heads → 7/16; delete all source → 0/16; clean rescue 16/16 | SPACE | MEASURED. job-a3d26738cd74. Reachability ≠ causality | NEITHER |
| `.../2026-10-02-vm-trace-visualizer` | Mamba-130M, Qwen2.5-1.5B, FLUX (all 3) | VM trace tool: commit-band + hidden-vs-visible overlays | Mamba L20 −2.94 (reproduces E3b); Qwen multiply item **removal NOT repaired (honest negative Δ−3.04)** | BOTH (tooling) | MEASURED (Qwen/Mamba fresh). Draft; visualization deliverable | NEITHER |
| `.../{open-bench, open-bench-families, bench-paging-discovery, qwen-virtual-memory-audit, causal-context-vm-integration}` | Qwen/Mamba/FLUX/SDXL | Runtime/VM/paging mechanics | exact-exec, eviction, fresh-process bit-exact; no speedup | NEITHER (infra) | MEASURED runtime. vm-audit uses a **toy random 2-layer model** | NEITHER |
| `.../2026-10-02-bx-training-continuation` | Pythia-160m (transformer) | B(x) boundary operator in bf16/fp8 training | B(x) lowers bf16 held loss 0.044 nats; grad err 148%→66% | NEITHER (numerics) | MEASURED. **Custody audit pending**. Off-thesis (SPF/Paper 3) | NEITHER |

---

## 1. Model-coverage table for the thesis (families × sizes)

| Family | Sizes with a thesis-bearing result | Scaffold half | Space half | Notes |
|---|---|---|---|---|
| **Transformer (decoder)** | Pythia-70M, Pythia-410M, Qwen2.5-0.5B, **Qwen2.5-1.5B** (primary), **Qwen2.5-7B**, Qwen2.5-Coder-1.5B, Qwen3-0.6B, Qwen3-8B, **Gemma-2-2B**, **SmolLM2-1.7B** | ✅ commit band fixed L19–23 / ~0.7–0.9 depth across all sizes incl. 7B | ✅ query-selective authority, reader reweighting, read-join | Gemma-2-9B **unavailable** (gated 403); 7B is paged |
| **State-space (Mamba)** | 130M, 370M, 2.8B | ✅ one late writer 0.69–0.83 depth; write=lever | ✅ shared state serves 2 ops, 27-coord profile 8/8 | single-seed; E5 certificate retracted |
| **Hybrid (attn+SSM)** | Falcon-H1-0.5B | ✅ late attention store | partial | predicted SSM writer not found |
| **Diffusion** | FLUX.2 Klein 4B, **FLUX.2 Klein 9B**, FLUX.1-schnell, SDXL, Chroma1-HD, Krea2 | ✅ fixed bus; four-quadrant time signature | ✅ per-prompt program; 21/21 byte-exact | 2–5 seeds (declared exception) |
| **MoE** | Qwen3-30B-A3B | ❌ **negative only** (in-forward cert fails isolated cut) | — | the only >7B test; no positive result |

**Breadth of the thesis evidence (measured):** 5 transformer sizes 70M→7B across 4 model families, a 3-size SSM family, a hybrid, and 6 diffusion specimens in 5 families. **Core preregistered test:** Qwen2.5-1.5B + Gemma-2-2B only.

---

## 2. Strong supporting results NOT currently in Paper 2 (ranked)

1. **`scale-9b-scaffold` — Qwen2.5-7B (paged).** Commit band depth-invariant at 7B (median L21, rel_depth 0.778, 100% in L19–27; SD 2.30 ≪ SD>4 falsifier). **Directly refutes the "≤2B" scope.** job-32fa0281137c. (P4/E20 at 7B still pending; P1 N/A on uniform attention.)
2. **`e20-cross-family` — Gemma-2-2B + SmolLM2-1.7B + held-out Qwen.** E20 block/rescue reproduces in two non-Qwen families (block 0.73–0.92, rescue 0.71–0.99) with wrong-identity control ≈0. **Answers "one model, one lab, not held out."** jobs job-fab52bcf3cce / job-a66b102614e3 / job-c128e07da015. (Paper 1 Appendix A has it; Paper 2 cites only the Qwen E20.)
3. **`cot-formed-state-faithfulness` — Qwen2.5 0.5B/1.5B/3B/7B.** E2 hidden-state channel dissociable from the visible token (answer change 1.00–0.955 across scale) — a new operation (reasoning) and a scale axis. **Paper 4 is parked (4/10) and the author's own note recommends folding it into Paper 2.** Caveat: E1 "silent repair = hidden channel" is demoted by its own addendum-2 — fold only E2.
4. **`qwen-alias-binding-feedback`** — source store + generated-state feedback flips the later native answer 3/3 (±8–13 nats); reference selects C while preserving A/B. Strong space-circuit evidence.
5. **`qwen-head-edge-topology`** — the GQA reader skeleton (fixed coords L23/KV0/V, L22/KV1/V) reused across facts with operation-specific weighting; sharpens §4 at head/edge grain.
6. **`common-causal-graph` / `scaffold-graph-identification`** — retained-history vs newly-formed-row signed paths (history +1.28..+1.58 nats, 4/4), showing the scaffold hosts interacting paths; honest limit: graded, no answer flip.
7. **`e8-klein9b-nine-gate` (FLUX.2 Klein 9B)** and **`e14-hybrid-attn-ssm` (Falcon-H1)** — extend the fixed-schedule reading to a 9B diffusion model and to a hybrid attention+SSM architecture (the latter is the cleanest "the architecture carries the scaffold" case).
8. **`role-aware-generated-chain` / `generated-product-store` (Qwen2.5-0.5B, arithmetic)** — a model-generated intermediate store controls the next freely-generated operation (4/4 fresh), extending §8 "formed state feeds later computation" to a new operation class.

---

## 3. The correct scope sentence + suggested subtitle

**Problem with the current sentence** (§1 line 39 / §12): "two transformer checkpoints of at most 2B parameters, four operations" describes only the preregistered variance/commit test, not the thesis evidence, which already spans 7B, an SSM family, a hybrid, and five diffusion families inside the same paper.

**Suggested replacement scope sentence:**
> "The preregistered commit-invariance and read-site variance tests are measured on two transformer checkpoints (Qwen2.5-1.5B and Gemma-2-2B); the scaffold/space-circuit division is corroborated more broadly — across four transformer families from 70M to 7B (Pythia, Qwen2.5-0.5B/1.5B/7B, Gemma-2-2B, SmolLM2-1.7B), a state-space family (Mamba-130M/370M/2.8B), a hybrid attention-SSM model (Falcon-H1), and five diffusion families (FLUX.2 Klein 4B/9B, SDXL, Chroma, Krea2) — all single-seed. The cross-family *common graph* remains an explicit null (§9), and there is no positive result above 7B: the Qwen3-30B-A3B certificate does not survive an isolated cut."

**Suggested title/subtitle** (the current title ends "...in Small Transformers," which understates the breadth). Keep the memorable main title; add a breadth-naming subtitle and drop "in Small Transformers":
- Title: *The Commit Layer Does Not Move: An Input-Invariant Time Scaffold Hosts Per-Input Space Circuits*
- Subtitle (options): (a) *"The architecture is the time circuit: a fixed commit-and-store schedule, measured across transformers, a state-space model, a hybrid, and diffusion, carries per-input space circuits"*; (b) *"A fixed, learned schedule built over execution — seed, formation, commit, store, consumer — across four transformer sizes, Mamba, Falcon-H1, and five diffusion families."*

---

## 4. Retracted / contradicting results that MUST stay disclosed

These are already disclosed in the current drafts; none is used as positive P2 evidence. They must remain visible:

1. **E5 Mamba four-quadrant certificate — RETRACTED** (two-layer-sampling artifact; full sweep shows one concentrated writer; no Mamba cell certifies). `mamba-full-layer-sweeps`, `space-and-time-circuits/E5`.
2. **Qwen3-30B-A3B (MoE) — NEGATIVE/no positive result**: the in-forward certificate does not survive the isolated cut; sampled only 2 layers. The only >7B test. `isolated-swap-reruns`, `space-and-time-circuits` E3b-T; Paper 1 §10.
3. **SmolLM2-1.7B identity "time circuit" label — RETRACTED** (concentrated L19 writer under full sweep). Note: this is distinct from the *valid* SmolLM2 E20 cross-family result.
4. **FLUX "necessity is counterfactual-only / deletion leaves target" — RETRACTED/CORRECTED by E1c** (dp≈0 was the null image). `flux2-residual-deletion`, `ablation-method-sensitivity`.
5. **Cross-family common role graph — NULL** (connected forecast ties plain addition exactly, MAE .015099 vs .014593, wins 1/3; role-matcher ≈ depth null, gap 0.0386). P2 §9. The thesis does not need it.
6. **Preregistered falsifiers that fired:** P2's write-window FAL-3 fired as frozen in 2/6 cells (argmax-of-plateau artifact; cleared by the fresh-color retest, which carries its own deviations — Qwen 27 colors < frozen 40, Gemma post-freeze chunking, freeze by file-mtime only); Paper 1's freeze-noop falsifier (P-A4) fired in both models.
7. **Mamba "writer stops its clock" mechanism — REFUTED** (clock-dose P1 false 6/6, P2 false 5/6); reread as a depth-fixed write port.
8. **CoT E1 "silent repair = hidden channel" — DEMOTED/CONTRADICTED** by its own addendum-2 (recompute-from-prompt; tracks_old=0 at every scale). Fold only the E2 dissociation.
9. **Function-vector equivalence (P2 Fig C) — NULL (NOT_FV)**, and A-P4 relation-reader prediction **failed for random-init** (+0.350). Both disclosed.
10. **Prereg primary predictions refuted:** E9 SDXL "TIME circuit" (necessity is space-like); E10 H2 (step is single-site necessary); E14 Falcon-H1 concentrated SSM writer (not found).
11. **Causal-mask defect (retired feedback instrument):** Transformers 5.14.1 skipped mask creation for a custom attention function, so a multi-token query could attend to future tokens while passing the instrument's own replay checks. The old selector/feedback packets in `scaffolds-and-dynamic-circuits` are disqualified; neither submission relies on them, and `qwen-routing-mediation` re-ran the affected measurement on stock eager. Keep the one-paragraph disclosure.
12. **Custody gaps to flag, not cite as clean:** Black Mamba quotient (laptop CPU, no mrun receipt); `native-role-learning-timeline` cannot date pretraining onset; P2 FROZEN.json edited after its jobs (freeze-timing); `bx-training-continuation` custody audit pending.
