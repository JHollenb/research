---
title: "What We Know About the Black Forest Models: A Data-Driven Report"
type: report
date: 2026-07-31 21:26
status: measured-except-where-labelled
tags: [report, flux, flux2, black-forest-labs, lineage, provenance, distillation, causal-circuits, typography, kv-cache, mrun, phase-cuda]
related:
  - "[[2026-07-28-143331-inside-the-black-forest-flux-models|Inside the Black Forest FLUX Models]]"
  - "[[2026-07-31-145130-the-conditioners-were-stock-checkpoints|The Conditioners Were Stock Checkpoints]]"
  - "[[../experiments/bfl-flux2-lineage-sweep|BFL FLUX.2 Lineage Sweep]]"
  - "[[../experiments/bfl-frontier-program-2026-07-31|BFL Frontier Program 2026-07-31]]"
  - "[[2026-07-28-173304-four-doors-beyond-the-image-model-atlas|Four Doors Beyond the Image Model Atlas]]"
---

# What We Know About the Black Forest Models: A Data-Driven Report

> **Adversarial update, 2026-08-02.** This historical report predates the three-claim owner audit.
> The Schnell result is a bounded residual-facing non-match, not proof of a fresh substrate; its
> original revision custody is retrospective and `0/50` refers only to first streamed chunks. The
> exact 9B↔9B-KV denoiser denominator is 233 tensors, not the 883-object package inventory, and its
> Q/K-heavy delta map is descriptive rather than cache causality. Use
> [[2026-08-02-black-forest-labs-measured-model-reference|the measured model reference]] and the
> current owner adjudication for publication claims.

Consolidation of everything this lab has measured about Black Forest Labs' FLUX family
across three days (2026-07-28 → 2026-07-31), ending with the six-track frontier program
adjudicated tonight. Every number here traces to a sealed artifact, a frozen plan, or a
job log; claims are labelled **measured** / **asserted** / **agent-reported** per house
rules. Prior art in this vault: the anatomy survey
([[2026-07-28-143331-inside-the-black-forest-flux-models|Inside the Black Forest]]), the
conditioner-provenance post
([[2026-07-31-145130-the-conditioners-were-stock-checkpoints|The Conditioners Were Stock
Checkpoints]]), the lineage-sweep owner note
([[../experiments/bfl-flux2-lineage-sweep|bfl-flux2-lineage-sweep]]), and the program
owner note ([[../experiments/bfl-frontier-program-2026-07-31|bfl-frontier-program]]).

## What

Six FLUX.2 subjects: **Dev** (d=4096 denoiser + Mistral-Small-24B conditioner),
**Klein-9B** and **Klein-9B-KV** (d=6144 + Qwen3-8B), **Klein-4B** (d=3072 + Qwen3-4B),
**Klein-base-4B** (the undistilled base of Klein-4B, acquired tonight), and
**FLUX.1-Schnell** (d=3072, the held FLUX.1 witness). Questions, in dependency order:

1. **Provenance** — what exactly did BFL ship, and where did each part come from?
2. **Adaptation anatomy** — what do BFL's own derivation steps (KV finetune, step
   distillation) do to the weights?
3. **Mechanism** — do behavior-certified circuits exist (counting, typography), and do
   they survive adversarial causal gates?
4. **Statics→dynamics** — do weight statistics predict where mechanism lives?

## Why

The 07-28 survey established anatomy but disclaimed provenance six times and closed with
every intervention null. The instruments that closed those gaps on the LLM side —
eigenbasis lineups ([[../experiments/bfl-flux2-lineage-sweep|lineage sweep]] §method),
weight-subspace statics, behavior-gated causal programs — had never crossed a modality
boundary. FLUX.2 is the test: open weights, a public distillation pair at matched scale,
an undisclosed substrate question BFL themselves never answered, and two documented
behavioral weaknesses (counting, text rendering) to aim causal programs at.

## How

House method throughout: frozen preregistration before outcome-bearing computation;
lineups against candidate panels, never thresholds; analytic + measured nulls; physics
controls (energy parity, pixel-exact restoration) on every causal arm; Holm correction;
sealed content-hashed plans executed by fail-closed workers; independent custody agents
adjudicating sealed reports digit-for-digit; refusal gates that close claims when any
frozen criterion fails. All compute through the mrun fleet with measured reservations.

---

## Result 1 — The conditioners are stock checkpoints, byte-verified (measured)

Full detail in [[2026-07-31-145130-the-conditioners-were-stock-checkpoints|the
conditioners post]]. Embedding eigenbasis lineups + byte-screen (3×256-row sampled
chunks):

| FLUX.2 component | Identified checkpoint | Eigenbasis (k=64) | Bytes |
|---|---|---|---|
| Dev text_encoder | mistralai/Mistral-Small-3.2-24B-Instruct-2506 | 0.9999999997 | identical |
| Klein-9B text_encoder | Qwen/Qwen3-8B | ~0.999 (family ties) | identical |
| Klein-4B text_encoder | Qwen/Qwen3-4B | 0.9999 (margin to sibs 0.86–0.89) | identical |
| Nemo control | — | 0.012544 = analytic null exactly | — |

Lesson that generalizes: the subspace names the *family*; only bytes name the
*checkpoint*.

## Result 2 — no detectable residual-facing inheritance from the Schnell witness (measured, bounded)

The undisclosed question. Instrument: principal-angle lineups between top-k singular
subspaces of matched DiT weight matrices, residual-facing sides only, validated on
ground-truth pairs *before* the question arm (gates frozen first):

| Validation gate | Criterion | Measured |
|---|---|---|
| klein-9B ↔ 9B-KV (finetune pair) | ≥0.0781 ∧ ≥2× controls | **0.9977** (min 0.9914) |
| klein-base-4B ↔ klein-4B (distill pair) | ≥0.1042 ∧ ≥2× controls | **0.9991** (min 0.9964) |
| Cross-layer controls | below pair means | max 0.3170 |
| Random nulls | [0.7,1.4]×k/d | 0.0151–0.0208 (on analytic values) |

Question arm — Klein-4B and klein-base-4B vs FLUX.1-Schnell at matched width 3072,
stacked-QKV right subspace k=64, 25 depth-matched positions: **median 0.0205 vs analytic
null 0.0208**; full 25×57 depth×depth matrix mean 0.0208, **max 0.0224 over all 1,425
cells — zero cells above 2× null**; k=256 and stored MLP objects likewise at null. The
`0/50` byte screen compares only each object's first streamed chunk. Frozen instrument verdict:
**NO-DETECTABLE-RESIDUAL-FACING-INHERITANCE FROM THIS WITNESS**. Schnell is the only FLUX.1 witness;
the historical reads used mutable Hub `main` and are only retrospectively revision-reconciled; and
a warm start rotated fully away by training would read identically.

Two instrument surprises worth their own lines:
- **The measured finetune and step-distillation interfaces are near-zero-rotation on DiT residual
  subspaces** (`0.9977 / 0.9991`). This supports derivative fingerprinting for these declared pairs;
  it is not a universal law or a complete byte-identity statement.
- **Within-model cross-layer same-role alignment runs 2–15× null** (0.024–0.317): DiTs
  carry shared global residual directions. Control *bands*, not k/d nulls, are mandatory.

Workspace: `experiments/2026-07-31-dit-weight-subspace-lineage/` (212 cached top-256
bases reusable).

## Result 3 — What the KV finetune changed (measured)

9B ↔ 9B-KV has a matched 883-tensor package topology at pinned revisions. Exact denoiser deltas use
233 tensor pairs; dual-sourced custody has 7/7 shard SHAs matching HF LFS oids:

- **Perimeter:** text encoder and VAE **byte-identical** — the finetune touched only the
  denoiser.
- **Frozen prediction "K,V dominate" REFUTED:** ordering is **Q≈K most, V≈attn-out
  least** (merged fused slices q 0.0544 / k 0.0535 vs v 0.0359 / out 0.0358; rescale
  ruled out at norm-ratio 1.0005). Reading (asserted): KV training re-aligned query–key
  *matching* geometry. Interpreting that as the causal adaptation for cached reference K/V is a
  hypothesis; the weights alone do not establish it or the private training objective.
- Q/K deltas depth-uniform; V/out/mlp-down decay with depth; largest single movers are
  conditioning globals (context_embedder 0.0874, img modulation 0.0837). ~96% of
  denoiser elements bit-changed; median rel ‖Δ‖_F 0.042 — a small uniform nudge, not
  surgery. Consistent with frozen CKA 0.939.

Workspace: `experiments/2026-07-31-kv-weight-delta-map/`.

## Result 4 — The distillation pair is now a certified instrument (measured)

`FLUX.2-klein-base-4B` (undistilled, Apache-2.0) acquired @`a3b4f484…`
(15,980,152,959 bytes, sealed receipts, MLflow READY). Static comparison: the
distilled/base pair is **tensor-inventory identical** — 818 tensors, 7,982,059,044
params; the *only* config deltas are `is_distilled` and the recipe. Distillation shipped
as pure weight change at this scale. Certification: adapter cert **22/22 gates PASS**;
true-CFG trajectory cert **31/31 PASS, 658/658 checkpoints exact**, per-step CFG
recombination `torch.equal(uncond + 4.0·(cond−uncond))` bit-exact on CUDA bf16. Capture
plan frozen (predictions P1–P4: readability relocation, site-class preservation, CKA
minimum, no count in the unconditional branch) — the "what does step-distillation do to
representations" experiment is loaded and gated, not yet run.

Workspace: `experiments/2026-07-31-klein-base-distillation-forensics/`.

## Result 5 — The counting circuit demoted itself, correctly (adjudicated)

Follow-on to the counting program in
[[2026-07-28-143331-inside-the-black-forest-flux-models|the survey]]. Two independent
16-pair sealed causal panels at the `joint.4` call-2 owned-cell site:

| Panel | Strict pairs | Key numbers |
|---|---|---|
| v3 strict replication (original wording) | **5/16**, Wilson lower 0.142 | addition & deletion **bimodal**: exactly 1.0 on 11 seeds, exactly 0.0 on 5; physics 16/16 perfect; population effect survives full Holm (p_adj 0.0039) |
| Paraphrase causal canary | **0/16** | sufficiency transfers 14/16 @ exactly 1.0; necessity 1/16; wrong-site control rescues at 0.609 |

Frozen policy-bound verdict: **NOT_VERIFIED** — the claim gate did not open, the repair
leg stays human-gated. The measured object, stated without widening: **seed-gated
redundant routing** — the owned-cell route is one of several sufficient paths, engaged
all-or-nothing per seed, not a necessary bottleneck. Two panels, one conclusion. The
harness refused the cleaner story a weaker harness would have shipped; this is the
gray-region discipline of
[[2026-07-31-193000-the-gray-region-had-to-survive-the-compiler|the compiler post]]
doing its job.

## Result 6 — The typography behavior atlas (measured tonight; sealed-report verification agent-pending)

BFL's other documented weakness, now quantified. Frozen 256-pair panel (fingerprint
`18fc7cba…`), 16 seeds × 2 instantiations per family, TrOCR-scored, Wilson-gated:

| Family | Pair admission | Wilson 95% lower | Per-instantiation split |
|---|---|---|---|
| spell-plain | **0.9375** | **0.799** | cash→wash 1.0, stop→shop 0.875 |
| spell-spec | 0.906 | 0.758 | cash→wash 1.0, stop→shop 0.8125 |
| presence-plain | 0.50 | 0.336 | **open 0.94 / exit 0.0625** |
| presence-spec | 0.50 | 0.336 | **open 1.0 / exit 0.0** |
| substitution-spec | 0.469 | 0.309 | open↔closed 0.8125, push↔pull 0.125 |
| substitution-plain | 0.094 | 0.032 | both near dead |

Three measured facts: **spelling transitions are robust** (the certified substrate for
the causal ladder); **substitution is broken**, with push↔pull nearly dead in both
lexicalizations; **presence is lexically gated** — the *word being rendered* flips
success from ~1.0 to ~0.0 at fixed seed and difficulty. Downstream legs
(selection → confirmation → port ranking → causal ladder) stay closed until the sealed
discovery report clears custody. Workspace:
`experiments/2026-07-31-typography-behavior-substrate/`.

## Result 7 — One clean null (measured, preregistered)

Static weight statistics (16 frozen predictors from `matrix-diagnostics.json`) do **not**
retrodict the measured semantic-port max-T ranking. In-sample retrodiction, labelled as
such; caveat recorded that the target ranking is nearly flat. The weights→ports bridge
that held on the LLM side has no image-side confirmation yet.
Workspace: `experiments/2026-07-31-weights-predict-ports-retrodiction/`.

## Infrastructure the program forced into existence

- **`mrun.diffusion` phase-cuda engine** (branch `feat/diffusers-phase-cuda`, unpushed):
  the measured `model_cpu_offload` tax (56s/pair, 100% single-core, GPU 12%) replaced by
  a temporal resident split — encode-phase / denoise-phase. **Bitwise parity 8/8**
  against offload; **10.66× per-image, 6.25× end-to-end**; typography panel replays at
  1.2s/pair (~47× its own baseline). Evidence sealed in
  `docs/evidence/diffusers-phase-cuda-klein4b-smoke.json`.
- Beast pathology diagnosed and cleared: a 2-day-stalled `hf download` (socket
  CLOSE-WAIT) held 17.2GB of swapped anon in **zram** — kernel-resident, invisible to
  per-process RSS. Diagnosis chain preserved in memory; margins now honest.

## Practical implications and open research directions

This section translates the measured results into model-development, evaluation, and systems
implications. It separates observed capabilities from plausible follow-on uses; it does not make
claims about private training choices, internal tooling, or product plans. The distinction is
important because the public residual-facing screen cannot reveal private ancestry, and a useful
method is not the same thing as proof of a particular lineage or mechanism.

- **The method is the transferable result.** Frozen plans, physics controls, refusal gates, and
  custody separation caught two wrong claims *inside this program* (the universal counting circuit
  and an early RAM misattribution) before either shipped. The individual model facts are bounded to
  the measured cohort and revision custody.
- **The new evidence is diagnostic rather than merely descriptive.** The experiments expose
  seed-gated redundancy in counting, lexical gating in typography, and the geometric shape of a
  measured KV adaptation. Those distinctions carry information that an aggregate benchmark score
  cannot carry.
- **The measurements support reproducible engineering workflows.** The results below describe
  concrete ways to use the instruments for comparison, diagnosis, and prioritization while keeping
  the remaining uncertainty visible.

### What the measurements enable

1. **Derivative screening.** The measured near-zero-rotation pairs (`0.9977 / 0.9991`) show that
   some finetune/distill relations retain a strong residual-facing fingerprint. The calibrated
   lineup can triage candidate relations with analytic nulls and known-related anchors. It is not
   universal IP proof: fully rotated ancestry and unmeasured interfaces remain observationally open.
2. **Targeted text-rendering diagnosis.** The atlas decomposes the failure: spelling is robust
   (0.94), substitution is weak (push↔pull 0.125), and presence is gated by the *word* (open ~1.0 /
   exit ~0.0). Lexical gating points conditioner-side; substitution failure points at the joint
   stream. That turns a broad quality complaint into separable hypotheses instead of a generic
   prescription to add more text data.
3. **Distillation auditing.** The certified base/distilled pair plus frozen capture plan measures
   what step-distillation costs representationally—where readability relocates and which site
   classes survive. The same measurements can be used to compare or regularize later distillation
   runs.
4. **A geometric changelog for adaptations.** The KV delta template identifies where an adaptation
   moved the weights (here: larger Q/K than V/output relative deltas) before downstream evaluation.
   Causal cache purpose and semantic payload ownership remain separate questions and require their
   own interventions.
5. **Seed-resolved evaluation.** Per-seed bimodality (exactly 1.0 / exactly 0.0) shows how
   mean-based evaluations can mask all-or-nothing routing. Reporting the seed distribution exposes
   structural variance rather than treating it as measurement noise.
6. **Adversarially reproducible capability claims.** Behavior certificates with Wilson admission,
   sealed causal panels, and refusal gates provide a concrete evaluation harness for claims that
   need to survive independent replication.
7. **Convergence data for optimization hypotheses.** Independent model families crossing the same
   bias→QK-norm transition in the same generation provide evidence about the optimization
   landscape. The observation is a hypothesis generator, not a forecast that the transition is
   universal or irreversible.

## Big picture

This was the microscope door of
[[2026-07-28-173304-four-doors-beyond-the-image-model-atlas|Four Doors]] crossing its
first modality boundary. Every load-bearing instrument transferred from LLMs to DiTs
and passed validation *inside the run* — lineups, statics, behavior-gated causal
programs, sealed-plan discipline. Two lab-level regularities got first cross-substrate
confirmation: **substrate preservation under adaptation** and **redundancy instead of
bottlenecks**. One bridge (weights→mechanism) did not transfer and is now an open,
honestly-bounded question. The certified distillation pair and the admitted typography
substrate are the loaded next experiments, and the follow-on proposal
([[../experiments/bfl-flux2-lineage-sweep|lineage sweep]] →
flux-generation-by-design) inherits all of it at the new 10× execution speed.

## Addendum (21:45) — parallel-program findings folded in

A same-day sweep of the vault found a parallel statics program
([[2026-07-31-205147-the-gate-survived-review-the-bias-did-not-and-flux-repeated-the-cliff|the
cliff post]]) and the finalized
[[../flux-generation-by-design-proposal|generation-by-design proposal]] (frozen after
this report's timestamp). Additions and qualifications, labelled per their sources:

**New facts this report missed:**
- **The bias→QK-norm cliff (measured, exploratory statics):** FLUX.1-schnell carries an
  attention K bias (fused qkv) + QK-norm; all three FLUX.2 checkpoints drop attention
  bias and keep QK-norm gains — the *same generational transition as Qwen2.5→Qwen3*.
  Two labs, two modalities, one architectural move. Implication: any admission
  machinery surviving into FLUX.2 cannot live in the bias channel.
- **FLUX.1 K-port signature map (measured, NOT depth-matched — source's own caveat):**
  image-stream "bias-anchored, content-light" heads front-load hard (double block 0:
  all 24 heads; then 1–5); single-stream signature heads concentrate blocks 13–37.
  FLUX.2 `norm_k` gain variance concentrates in early double blocks and at
  single-stream stack edges.
- **Scale re-allocation across generations (measured, from the proposal):**
  conditioner:denoiser ratio roughly doubled, 0.41× (FLUX.1) → 0.75–1.04× (FLUX.2);
  double-stream block fraction fell 33%→14%.

**Qualifications to results above:**
- **Result 7's null is qualified:** input-side effective rank produced perfect orderings
  twice (MLP_IN and FUSED_IN ρ=−1.00, p=0.042 each; "lower input erank ⇒ stronger
  port") — a multiplicity-eaten survivor, to be watched prospectively only, but "no
  image-side confirmation" was too flat.
- **Result 3 instrument update:** the later 249-object k=64 panel reports median `0.997713` and
  minimum `0.930871`; it is distinct from T1's 17-object `0.9914` minimum. Adversarial review found
  FP32 right-facing products under the old “FP64 Grams” label. A receipt-bound ten-object true-FP64
  check preserves primary k=64 Q/K/V/output geometry to `1.86e-9`, while rank-degenerate global
  `proj_out` is unstable at k=256. This is a stratified method check, not a full 249-object rerun.
- **Result 5 addition:** counting is also **location-gated** — on the Dev canary both
  top-left pairs passed strictly, neither bottom-right pair did. Seed-gated AND
  place-gated.

**Standing bets now on the record:** the forecast registry
(`experiments/2026-07-31-flux-forecast-registry/`, sha `e6a7125b…`) freezes **nine
scored predictions about BFL's next minor and major releases** — lineups ≥0.99 to
FLUX.2, Q/K+globals delta signature, deficits moving <10 points within-generation,
conditioners staying byte-stock, rebuild-at-null on the next major, and the cliff
staying crossed. When BFL ships next, this lab scores itself in public.

**Convergence note:** the cliff post sketches a FLUX causal harness (text-stream K/V
graft + release enumeration over three statically nominated banks) that is independent
of, and convergent with, the T2/T6 machinery here — the two programs should be
cross-calibrated before either runs its next causal leg.

## Artifact index

| Track | Workspace / key artifacts |
|---|---|
| T1 lineage | `experiments/2026-07-31-dit-weight-subspace-lineage/` — PLAN.md, validation.json, question_arm.json, full depth matrices, 212-base cache |
| T2 counting | `experiments/2026-07-29-202802-flux2-fp32-control-feasibility/` — v3 plan seal `374808a5…`, policy-v2 `9c45bed2…`, analysis `ce314ea7…`, canary report `c2d219ce…` |
| T3 distillation | `experiments/2026-07-31-klein-base-distillation-forensics/` — certs `job-3f6cd6775661`/`job-3746b8968ef3`, frozen PLAN.md |
| T4 KV delta | `experiments/2026-07-31-kv-weight-delta-map/` — kv-delta-map.json, rollups, pinned LFS SHAs |
| T5 retrodiction | `experiments/2026-07-31-weights-predict-ports-retrodiction/` |
| T6 typography | `experiments/2026-07-31-typography-behavior-substrate/` — panel `18fc7cba…`, parity `job-5a13d598c7fb`, discovery `job-d32bf4b13094` |
| Engine | mrun `feat/diffusers-phase-cuda` @ `10167b1`/`ed7cc44`/`1b6cc98`; smoke `job-eac6b216a07c` |
