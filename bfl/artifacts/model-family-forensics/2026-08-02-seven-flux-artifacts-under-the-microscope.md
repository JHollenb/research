---
title: "Seven FLUX Artifacts Under the Microscope"
subtitle: "A data-driven analysis of every Black Forest Labs model and component in our measured cohort"
date: 2026-08-02
updated: 2026-08-02
type: report
status: publication-ready
audience: public-technical
claim_status: adversarially-reviewed-and-bounded
tags: [black-forest-labs, flux, flux1, flux2, model-analysis, mechanistic-interpretability, diffusion, rectified-flow]
related:
  - "[[../black-forest-labs-model-wiki|Black Forest Labs Model Wiki]]"
  - "[[2026-08-03-160047-how-the-black-forest-models-work-from-conditioner-to-pixels|From Conditioner to Pixels]]"
  - "[[../generative-model-wiki|Generative Model Wiki]]"
  - "[[../indexes/generative-model-analysis|Generative Model Analysis Index]]"
  - "[[2026-08-01-h9-native-specificity-replication|H9 Adversarial Correction and Repair]]"
  - "[[../experiments/bfl-flux2-lineage-sweep|BFL FLUX.2 Lineage Sweep]]"
source_docs:
  - ../../experiments/2026-07-24-generative-image-model-atlas/BFL_FLUX2_REPORT.md
  - ../../experiments/2026-07-31-klein-base-distillation-forensics/STATUS.md
  - ../../experiments/2026-07-31-211500-flux-arbitration-harness/CIRCUIT_CLOSURE_LEDGER.md
  - ../../experiments/2026-08-01-flux1-schnell-arbitration/PLAN.md
  - ../../experiments/2026-08-01-233923-bfl-generational-model-observatory/STATUS.md
  - ../../experiments/2026-08-02-bfl-three-claims/FINAL_ADJUDICATION.md
---

# Seven FLUX Artifacts Under the Microscope

*A data-driven analysis of every Black Forest Labs model and component in our measured cohort*

We analyzed six Black Forest Labs image generators and one decoder component across five layers of
evidence: exact artifact custody, architecture, executable trajectories, controlled behavior, and
causal intervention. The result is not a product ranking. It is an evidence map of what each model
is, what changed between related releases, what behavior appeared under fixed tests, and which
mechanistic claims survived controls.

Several findings are unusually sharp. FLUX.2 Klein base 4B and distilled Klein 4B have exactly the
same tensor inventory but radically different denoising recipes. Klein 9B and 9B-KV share a complete
architecture while roughly 96% of denoiser elements differ. FLUX.2 Dev can be executed in exact BF16
on constrained hardware by separating conditioner and denoiser lifetimes. The Small Decoder cuts
the tested decoder path by 43.678% of its parameters. And in one preregistered Klein 4B binding assay,
a distributed native K/V intervention route clears five admissible source/statistics controls and
accumulates across denoising time; a sixth reverse wrong-world control is under frozen repair.

The boundaries are just as important. The behavior panel is small and recipe-specific. Readable
features are not automatically causal. The Dev behavior suite remains diagnostic rather than
custody-admitted. The Klein 4B route is established for one fixed assay, while its original bilateral
six-control specificity verdict is superseded by a donor-map defect. Those distinctions are part of
the result.

The chain-level architecture synthesis is [[2026-08-03-160047-how-the-black-forest-models-work-from-conditioner-to-pixels|From Conditioner to Pixels]]. It connects this cohort survey to the exact VAE shard identity and paired decoder-boundary work without collapsing the separate evidence classes.

## The measured cohort

The cohort contains every BFL artifact for which we currently hold a pinned, analyzed record. It is
not a catalog of every model Black Forest Labs has released.

| Artifact | Role | Packaged parameters | Core program | Highest supported evidence |
|---|---|---:|---|---|
| **FLUX.1 Schnell** | FLUX.1 generator and lineage witness | 16,860,369,379 | 19 joint + 38 merged blocks, width 3,072 | Anatomy, exact runtime, bounded behavior, failed causal-workload admission |
| **FLUX.2 Klein base 4B** | Undistilled matched reference | 7,982,059,044 | 5 joint + 20 merged blocks, width 3,072 | Anatomy and exact 50-step true-CFG trajectory |
| **FLUX.2 Klein 4B** | Four-step distilled generator | 7,982,059,044 | 5 joint + 20 merged blocks, width 3,072 | Exact trajectory, behavior, and fixed-assay intervention route; bilateral specificity repair pending |
| **FLUX.2 Klein 9B** | Larger compact generator | 17,353,362,980 | 8 joint + 24 merged blocks, width 4,096 | Exact trajectory/reference path and bounded behavior |
| **FLUX.2 Klein 9B-KV** | Reference-KV adaptation of 9B | 17,353,362,980 | Same 8 + 24 program as 9B | Exact cache path, complete weight delta, bounded behavior |
| **FLUX.2 Dev** | Flagship-scale generator | 56,318,688,804 | 8 joint + 48 merged blocks, width 6,144 | Admitted one-step BF16 runtime; richer suite diagnostic only |
| **FLUX.2 Small Decoder** | Auxiliary latent-to-pixel decoder | 62,373,348 | VAE component, no denoiser or conditioner | One sealed-latent paired component replay |

Packaged parameter counts include the denoiser, conditioner, and VAE where present. They should not
be read as denoiser-only model sizes. Schnell, for example, contains an 11.891B-parameter denoiser
inside a 16.860B-parameter package.

## How the measurements were made

Every promoted number in this report belongs to a specific evidence class.

| Evidence class | Measurement method | What it establishes | What it does not establish |
|---|---|---|---|
| **Custody** | Pin repository revision; record manifests, configuration, tensor names, shapes, dtypes, byte counts, and receipts | The exact artifact under test | Behavior, quality, or meaning |
| **Anatomy** | Parse complete `safetensors` headers and model configuration; count components and reconstruct block geometry | The model's physical and architectural substrate | Which features the model uses at runtime |
| **Execution** | Reconstruct the stock Diffusers path in `manalysis`; execute through `mrun`; compare prompt state, latent, denoiser calls, scheduler transitions, VAE state, and pixels | The intended model path ran and instrumentation was non-perturbing | Semantic causality |
| **Behavior** | Run seeded prompt panels under declared native recipes; score alignment, counting, color order, and text rendering | Performance on that exact panel and recipe | A general quality ranking |
| **Lineage / adaptation** | Compare bytes, complete weight deltas, principal-angle subspaces, CKA geometry, and known-related positive controls | Detectable continuity or adaptation in the measured representation | Private training history or ancestry by itself |
| **Causal physiology** | Use clean/corrupt baselines, no-op delivery, route dose, time, restoration, held-out data, and matched wrong-source controls | A load-bearing route in the declared assay | A universal or symbolic circuit |

[[../tools/mrun|mrun]] supplied guarded remote execution, resource reservations, model placement,
paging, and memory telemetry. [[../../manalysis/README|manalysis]] supplied model adapters,
trajectory certificates, activation capture, readouts, and interventions. A worker completing
without error was not sufficient: custody, exactness, and the applicable scientific gates had to
pass independently.

### The common behavior panel

Four generators were compared on the same 14 prompts and two seeds: 28 images per model at
512 × 512 and four denoising steps, using each pipeline's declared conditioning recipe. Mean CLIP
is text-image alignment, count exactness is automated object-count correctness, color order tests
eligible red/blue spatial prompts, and OCR reports exact-string and character accuracy. Runtime and
memory include the model-specific offload strategy.

| Model | Seconds / image | Peak RSS | Allocated VRAM | Mean CLIP | Count exact | Color order | OCR exact / char |
|---|---:|---:|---:|---:|---:|---:|---:|
| FLUX.1 Schnell | 8.7 | 33,947 MiB | 623 MiB | 0.351 | 0.500 | — | 0 / 0.083 |
| FLUX.2 Klein 4B | 6.1 | 19,382 MiB | 7,936 MiB | 0.351 | 0.833 | — | 0 / 0.000 |
| FLUX.2 Klein 9B | 8.3 | 34,109 MiB | 1,492 MiB | 0.354 | 0.500 | 1.000 | 0.250 / 0.307 |
| FLUX.2 Klein 9B-KV | 8.4 | 34,906 MiB | 1,492 MiB | 0.353 | 0.667 | — | 0 / 0.209 |
| FLUX.2 Dev¹ | — | — | — | 0.360 | 0.833 | 1.000 | 0.250 / 0.472 |

¹ The Dev row came from a richer unguarded diagnostic worker. It is included to disclose the data we
have, but it is not promoted to the same evidentiary tier as the four guarded panel rows. Dashes mean
that a metric was not part of the eligible scored subset, not that the model received a zero.

The table immediately rules out an easy story. In this panel, parameter count did not predict every
metric: Klein 4B beat Klein 9B on counting, while the 9B model did better on OCR. The CLIP means were
nearly flat. These are useful regressions to investigate, not a global judgment of image quality.

## FLUX.1 Schnell: a well-measured baseline that failed the new causal admission gate

**Pinned artifact.** `black-forest-labs/FLUX.1-schnell` at revision
`741f7c3ce8b383c54771c7003378a50191e9efe9`.

**How it was measured.** Complete tensor inventory and configuration established the anatomy. A
guarded common-panel run measured behavior and resource use. Exact G0 checks compared the stock and
instrumented pipelines at 512 and 1,024 pixels. Finally, a clean/corrupt two-object color-binding
gate tested whether the workload was strong enough to support the same causal arbitration used on
Klein 4B.

| Measured anatomy | Value |
|---|---:|
| Tensors / parameter bytes | 1,815 / 33,720,738,758 |
| Denoiser | 11,891,178,560 parameters |
| Conditioners | CLIP 123,060,480 + T5 4,762,310,656 parameters |
| VAE | 83,819,683 parameters; 16 latent channels |
| Transformer | 19 joint + 38 merged blocks; width 3,072; 24 heads × 128 |
| Conditioning interface | CLIP pooled state plus T5 sequence state; fused QKV with bias |

The common panel measured 0.351 mean CLIP, 0.500 count exactness, and 0 / 0.083 OCR exact/character
accuracy. Sequential offload kept allocated VRAM to 623 MiB, but peak process memory reached
33,947 MiB. At 1,024 pixels, sequential offload was the only tested strategy that fit the 16GB GPU
envelope; it took roughly two to three minutes per image in the four- to eight-step admission runs.
In that extension, layerwise float8 storage with BF16 compute occupied roughly 12GB before the
approximately 3GB activation load. Direct placement and model-level offload ran out of memory;
sequential offload reduced peak allocated VRAM to roughly 676MB and completed.

Instrumentation itself was not the failure. Stock/instrumented parity passed 11/11 gates at 512 and
11/11 at 1,024. The behavior prerequisite failed:

| Resolution / steps | Clean score | Corrupt score | Required floor | Admission |
|---|---:|---:|---:|---|
| 512 / 4 | 0.7500 | 0.6250 | 0.9375 each | Fail |
| 768 / 4 | 0.6250 | 0.7500 | 0.9375 each | Fail |
| 1,024 / 4 | 0.3750 | 0.6875 | 0.9375 each | Fail |
| 1,024 / 8 | 0.3750 | 0.6875 | 0.9375 each | Fail |

Increasing resolution and steps did not rescue the workload. A causal intervention cannot answer a
binding question if the unedited model does not reliably perform the behavior, so the planned
Schnell mechanism comparison was correctly stopped.

Schnell was also the only FLUX.1 witness in the denoiser-lineage test. The 25 frozen depth-matched
cells had median residual-facing alignment 0.0205 against an analytic null of 0.0208. A separate
complete 25×57 scan retained all 1,425 cells and had maximum 0.0224; zero cells exceeded twice the
null. Zero of 50 matched primary QKV objects had equal SHA-256 values for the first streamed chunk.
That last check is not a full-tensor byte comparison. The original range reader also requested Hub
`main`; current pointers retrospectively match the expected revisions, but historical custody was
not self-contained. The result is **no detectable residual-facing inheritance from this witness**,
not proof of fresh initialization, no rotated warm start, or no untested FLUX.1 source.

> **Supported:** exact anatomy, exact instrumented execution, bounded behavior, and a failed
> workload-admission result. **Not supported:** a Schnell color-binding circuit or a family-wide
> claim about FLUX.1 quality.

## FLUX.2 Klein base 4B: the exact undistilled reference

**Pinned artifact.** `black-forest-labs/FLUX.2-klein-base-4B` at revision
`a3b4f4849157f664bdbc776fd7453c2783562f4d`.

**How it was measured.** The base model was acquired through a guarded revision-pinned flow, compared
tensor-for-tensor with distilled Klein 4B, and run through a purpose-built true classifier-free
guidance trajectory certificate. The certificate separately recorded conditional and unconditional
denoiser calls and verified the BF16 recombination passed to every scheduler step.

| Measured anatomy / recipe | Base 4B | Distilled 4B reference |
|---|---:|---:|
| Tensors | 818 | 818 |
| Packaged parameters | 7,982,059,044 | 7,982,059,044 |
| Parameter bytes | 15,964,118,094 | 15,964,118,094 |
| Denoiser / Qwen3 / VAE | 3.876B / 4.022B / 84.046M | Identical component counts |
| Transformer geometry | 5 joint + 20 merged, width 3,072 | Identical |
| Native recipe | 50 steps, guidance 4.0, true CFG | 4 steps, guidance 1.0, one call per step |

The static pair is unusually clean: architecture, tensor names, shapes, dtypes, component counts,
and relevant configuration are matched. Weight values differ, as expected. The public distinction is
therefore a weight-and-trajectory change rather than a topology change.

The real-checkpoint adapter passed 22/22 gates. The true-CFG trajectory passed 31/31 gates across
100 denoiser calls, 50 scheduler steps, and four prompt-encoding snapshots. All 658 registered
trajectory comparisons were exact, including bit-exact BF16 recombination of the unconditional and
conditional predictions. Those 658 records are observation points—not 658 saved weight
checkpoints.

We do not include a base-model common behavior score or an H5–H9 causal claim because those tests
have not been completed at the required tier. A later activation-forensics synthesis reported
distillation results, but the current local owner record still marks its capture phase in flight and
lacks the cited final adjudication artifact. This publication therefore stops at the reconciled
custody, anatomy, and exact trajectory evidence.

> **Supported:** a topology-matched, exactly executed before/after reference for four-step
> distillation. **Not supported:** a final claim about which semantic capabilities distillation
> preserved, lost, or reorganized.

## FLUX.2 Klein 4B: the deepest behavior and causal record

**Pinned artifact.** `black-forest-labs/FLUX.2-klein-4B` at revision
`e7b7dc27f91deacad38e78976d1f2b499d76a294`.

**How it was measured.** Klein 4B passed exact stock/reference/no-op trajectory checks, the common
behavior panel, targeted count and typography panels, stream- and time-specific activation capture,
and a five-stage H5–H9 causal arbitration sequence. The final causal test used fresh prompts,
source-identity controls, bootstrap intervals, technical gates, and full visual review.

| Measured anatomy | Value |
|---|---:|
| Tensors / packaged parameters | 818 / 7,982,059,044 |
| Denoiser / Qwen3 / VAE | 3,875,544,576 / 4,022,468,096 / 84,046,372 |
| Transformer | 5 joint + 20 merged blocks; width 3,072; 24 heads × 128 |
| Attention | QK normalization; no Q/K/V bias |
| Native recipe | Four steps; guidance 1.0; no guidance embedding |
| Conditioner screen | Three sampled embedding chunks match Qwen3-4B; eigenbasis ≈ 0.9999999 |

### Behavior: strong small counts, a sharp count cliff, and a typography substrate

The common panel measured 0.351 mean CLIP, 0.833 count exactness, and zero OCR exact/character
accuracy. The corresponding Qwen3 color-binding workload admitted at 1.000, which is why a causal
test was valid here when the same workload was not valid on Schnell. A more focused count panel
showed where the aggregate score broke:

| Requested object count | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---:|---:|---:|---:|---:|---:|
| Exact generation rate | 1.0000 | 0.8750 | 0.8750 | 0.4375 | 0.1875 | 0.0625 |

The degradation is a cliff, not a smooth size effect. A candidate count site also failed as a unique
circuit: strict prompts passed 5/16 while paraphrases passed 0/16, and necessity did not survive the
full controls. Count behavior was seed-, wording-, and location-sensitive and compatible with
redundant routing.

A separate frozen 256-pair typography assay measured spelling success of 0.9375 for plain prompts
and 0.906 for prompts requesting a specific typographic attribute. Presence remained 0.500 in both
conditions. Specific substitutions succeeded at 0.469 overall, with large variation by contrast:
open↔closed reached 0.8125 while push↔pull reached 0.125. That establishes a manipulable behavior
substrate, not a causal typography circuit.

### Causal physiology: a distributed native K/V route

The H5–H9 sequence asked whether Qwen3's binding information reaches the generated image through a
specific native route. Early compact-circuit interpretations failed. The surviving result is
distributed:

- H5 identified multiple single-stream K/V contributors, including a block-13 carrier.
- H6 found a nonlinear dose curve: S4 and S8 moved the continuous margin, while broad full20
  coverage was needed for reliable endpoint restoration.
- H7 replicated the route on held-out data but left native-versus-wrong-world specificity open.
- H8 showed temporal accumulation. In the registered binding-margin units, full-route effects were
  +179.565 [157.329, 201.441] forward and +182.422 [160.293, 204.882] reverse; all-step grafting
  exceeded every single-step arm.
- H9 was the powered source-specificity test.

H9 held the model, prompt family, scorer, route, and rendering recipe fixed. It used 48 fresh prompt
pairs × two seeds = 96 paired instances, 12 arms, and 1,152 renders. All image hashes and row
metadata reverified. A prompt-pair cluster bootstrap and six-family Bonferroni calculation remained
positive, but adversarial review found that one control was malformed.

| Native S4 minus control | Forward mean | Reverse mean | Adjudication |
|---|---:|---:|---|
| Wrong-token | +5.292 | +7.311 | valid in both directions |
| Wrong-world | +6.910 | +6.171 | forward valid; reverse invalid as collision-safe |
| Scrambled | +6.285 | +8.450 | valid in both directions |

The reverse wrong-world map reused a forward-only permutation. Its corrupt-world donor color
collides with a destination color in 45/96 instances, including 20 direct target-color collisions.
The `+6.171` reverse statistic is retained as a contaminated trend, not terminal evidence. The five
valid controls have conservative six-family lower bounds above zero; the smallest is +2.345.

The route-level native S4 margin remains +6.740 [4.414, 9.254] forward and +8.830
[5.988, 11.804] reverse. Full20 produced much larger continuous margins—+202.154 and +201.537—and
recovered the target endpoint in 83/96 forward and 88/96 reverse instances. Manual review covered
all images, but visual coherence cannot certify donor semantics.

The runtime stack was also replaceable under a separate parity test. A local phase-CUDA branch was
bitwise exact on 8/8 checks and measured 0.607 seconds per image versus 6.469 seconds for the
reference path: 10.66× at the per-image stage and 6.25× end to end on the tested hardware and
recipe. This is a benchmark-specific engine result, not a universal speed claim.

> **Supported:** a distributed single-stream K/V intervention route whose effect accumulates over
> denoising time and beats five admissible controls in the fixed assay. **Pending:** a direction-safe
> rerun of the reverse wrong-world control before bilateral six-control specificity is restored.
> **Not supported:** endogenous necessity, a compact universal quorum, cross-model portability, a
> symbolic scene representation, or a general quality-edit recipe.

## FLUX.2 Klein 9B: a larger model with a certified reference path

**Pinned artifact.** `black-forest-labs/FLUX.2-klein-9B` at revision
`92196c8e11f7b6cf2b7493e037d8c5345c559216`.

**How it was measured.** Complete static inventory was followed by adapter, stock-trajectory, no-op,
and reference-image pathway certification. The model then ran through the common behavior panel,
legacy feature readouts, and a learned-versus-random style intervention.

| Measured anatomy / certification | Value |
|---|---:|
| Tensors / parameter bytes | 883 / 34,706,725,966 |
| Denoiser / Qwen3 / VAE | 9,078,581,248 / 8,190,735,360 / 84,046,372 |
| Transformer | 8 joint + 24 merged blocks; width 4,096; 32 heads × 128 |
| Conditioner screen | Three sampled embedding chunks match Qwen3-8B; eigenbasis ≈ 0.9999992 |
| Certificates | Adapter 22/22; trajectory 29/29 and 38/38; reference path 40/40 |

The common panel measured 0.354 mean CLIP, 0.500 count exactness, 1.000 red/blue centroid order,
and 0.250 / 0.307 OCR exact/character accuracy. Generation took 8.3 seconds per image with
34,109 MiB peak RSS and 1,492 MiB allocated VRAM under sequential offload.

The reference-image path was operationally real. Each tested call processed 1,024 reference and
1,024 target tokens; zeroing reference delivery changed 455,010 uint8 output-channel values with
mean absolute difference 1.143. This proves that the path reaches the pixels. It does not assign
semantic ownership—style, identity, layout, or another concept—to those states.

Older pooled probes found readable typography and watercolor-versus-photo information. The causal
style intervention did not validate those readouts as load-bearing: learned removal changed the
CLIP margin by -0.003, versus -0.001 for random and -0.008 at the wrong time. There was no
learned-over-random specificity pattern.

> **Supported:** exact stock and reference execution, a real reference-to-output path, and bounded
> behavior. **Not supported:** a causal style circuit or a monotonic “larger is better” conclusion.

## FLUX.2 Klein 9B-KV: a distributed adaptation for reference-state reuse

**Pinned artifact.** `black-forest-labs/FLUX.2-klein-9B-KV` at revision
`a6dfb36eca3a3906eb2fd460795adfb844e5fcce`.

**How it was measured.** The entire tensor inventory was matched against standard Klein 9B, every
denoiser delta was summarized, representation geometry was compared with CKA, and the cache path was
certified by tracing token counts, extraction/application events, memory, and output parity. The
model also ran through the common behavior panel.

The static relation is exact at the skeleton level: both artifacts contain 883 tensors,
17,353,362,980 parameters, the same shapes, and the same 8 + 24, width-4,096 program. They are not
the same weights. The conditioner and VAE are byte-identical; the adaptation is in the denoiser.
Across the exact 233-tensor denoiser denominator, 8,725,252,912 of 9,078,581,248 BF16 elements
changed (96.10811065795288%), with median tensor relative norm 0.041628.

| Denoiser delta family | Median relative change |
|---|---:|
| Query projection | 0.0544 |
| Key projection | 0.0535 |
| Value projection | 0.0359 |
| Output projection | 0.0358 |

Despite the broad elementwise change, matched activation geometry remained high over nine declared
depth×time coordinates, panel size 80 and two seeds: median linear CKA 0.9382467 and RBF CKA
0.9447244. The 249-object weight-angle panel used FP32 right-facing Gram products with FP64
accumulation/eigh. A receipt-bound ten-object true-FP64 check changed the primary k=64 Q/K/V/output
objects by at most 1.86e-9; a rank-degenerate global `proj_out` basis was unstable at k=256 and is
not used as a stable headline. The larger Q/K deltas are consistent with realignment of query-key
matching for consuming cached reference K/V, but they do not prove causality or reveal the private
training objective.

The runtime trace makes the operational change concrete. Standard 9B processed 2,048 tokens on all
four reference-conditioned calls. The KV variant processed 2,048 tokens once, extracted reference
K/V, and then processed 1,024 target tokens on each of the next three calls. The maximum observed
cache was 512 MiB. The measured speedup was approximately 1.073× in this 512-pixel, four-step probe.
Trajectory certification passed 29/29 gates and cache/reference certification passed 40/40.

The common panel measured 0.353 mean CLIP, 0.667 count exactness, and 0 / 0.209 OCR
exact/character accuracy. Runtime was 8.4 seconds per image, with 34,906 MiB peak RSS and 1,492 MiB
allocated VRAM under sequential offload.

> **Supported:** a geometry-preserving but weight-wide adaptation that extracts reference K/V once
> and reuses it across denoising calls. **Not supported:** a new static architecture, a semantic
> memory register, or a causal claim about what the cached state represents.

## FLUX.2 Dev: exact flagship-scale execution with a diagnostic behavior ceiling

**Pinned artifact.** `black-forest-labs/FLUX.2-dev` at revision
`26afe3a78bb242c0a8bb181dcc8937bb16e5c66c`.

**How it was measured.** Static analysis inventoried the full package. A guarded one-step run then
persisted conditioner output, released the 24B conditioner, loaded the 32B denoiser through CPU/disk
dispatch, executed one BF16 denoising step, and decoded the result. A separate richer worker ran the
behavior and recorder suite, but its receipt was unguarded and lacked an executed-payload digest;
those results remain diagnostic.

| Measured anatomy | Value |
|---|---:|
| Tensors / packaged parameters | 1,167 / 56,318,688,804 |
| Parameter bytes | 112,805,470,356 |
| Denoiser / conditioner / VAE | 32,223,281,152 / 24,011,361,280 / 84,046,372 |
| Transformer | 8 joint + 48 merged blocks; width 6,144; 48 heads × 128 |
| Context interface | Width 15,360; Mistral3-derived conditioner |
| Conditioner screen | Three sampled embedding chunks match Mistral Small 3.2 24B; eigenbasis ≈ 0.9999997 |

The admitted component-decoupled run passed 11/11 gates. It persisted a `[1, 512, 15360]` prompt
state from 585 conditioner tensors, released the conditioner, and completed a 512 × 512 one-step
forward plus VAE decode in 336.41 seconds. Peak RSS was 16,803.3 MiB and peak VRAM was 10,264 MB,
with no quantization. Swap telemetry and a 12.702GB swap footprint confirmed that paging—not hidden
co-residency—made the run possible.

The richer diagnostic worker passed 14 worker gates in 571.35 seconds at 17.365GB RSS and 11.628GB
VRAM. Its 28-image behavior values were 0.360 mean CLIP, 0.833 count exactness, 1.000 red/blue
centroid order, and 0.250 / 0.472 OCR exact/character accuracy. Because the execution receipt was
unguarded, those values are useful for experiment design but not for a guarded model ranking or a
semantic mechanism claim.

> **Supported:** exact, non-quantized BF16 execution of the pinned 56.319B package through explicit
> component lifetimes. **Not supported:** an admitted multistep behavior benchmark or a Dev semantic
> circuit.

## FLUX.2 Small Decoder: a faster component, not a smaller generator

**Pinned artifact.** `black-forest-labs/FLUX.2-small-decoder` at revision
`a3efc24f613ef42d9428af62fdbd6f5fd8856c4a`.

**How it was measured.** Static analysis established that the artifact contains only a VAE component.
One persisted latent was then decoded by the full and small decoders under the same conditions. The
test compared parameter count, repeated decode time, output cosine, PSNR, and pixel equality.

| Measured component result | Value |
|---|---:|
| Tensors / packaged parameters | 251 / 62,373,348 |
| Parameter bytes | 249,493,396 |
| Full encoder channels | 128 / 256 / 512 / 512 |
| Small decoder channels | 96 / 192 / 384 / 384 |
| Decoder-path parameters | 49,620,259 → 27,947,235 |
| Parameter reduction | 43.678% |
| Repeated-decode speedup | 1.5166× |
| Peak decode VRAM | 817.4 MB → 614.2 MB |
| Output cosine | 0.9997839 |
| MAE / RMSE | 0.003187 / 0.005860 |
| PSNR | 44.6426 dB |
| Pixel exact | No |

The experiment supports a concrete component tradeoff: substantially fewer decoder parameters,
lower peak decode memory, and a 1.517× speedup with close numerical output on the tested latent.
About 49% of uint8 output-channel values nevertheless differed, so high cosine and PSNR should not
be mistaken for pixel identity. The replay does not test prompt encoding, denoising, scheduler
behavior, or end-to-end generation, because the artifact contains none of those parts. One latent
is also insufficient for a distributional or human-preference equivalence claim.

> **Supported:** a one-latent component-level efficiency result. **Not supported:** a smaller FLUX
> generator, pixel equivalence, or unchanged perceptual quality across a data distribution.

## What the cross-model data says

### 1. FLUX.2 is not a detectable Schnell continuation in the tested witness

The lineage instrument first had to recognize known related pairs. It did: Klein base 4B ↔ distilled
4B measured 0.9991 residual-facing alignment with minimum 0.9964, and the narrower 17-object T1
Klein 9B ↔ 9B-KV validation panel measured 0.9977 with minimum 0.9914. A separate 249-object panel
has k=64 minimum 0.930871 at near-degenerate `norm_out.linear`; the two minima are not interchangeable.
Against the positive controls, Klein 4B ↔ Schnell fell to the random null. The bounded conclusion is
no detectable inheritance from the one tested FLUX.1 witness.

This is descriptive model evidence, not a claim about BFL's private training history. Release order
does not establish ancestry, and a fully rotated warm start can evade a subspace lineage screen.

### 2. The conditioner identities are much clearer than the denoiser lineage

| BFL subject | Candidate public conditioner | Sampled evidence |
|---|---|---:|
| Klein 4B | `Qwen/Qwen3-4B` | Three embedding chunks match; eigenbasis ≈ 0.9999999 |
| Klein 9B / 9B-KV | `Qwen/Qwen3-8B` | Three embedding chunks match; eigenbasis ≈ 0.9999992 |
| FLUX.2 Dev | `mistralai/Mistral-Small-3.2-24B-Instruct-2506` | Three embedding chunks match; eigenbasis ≈ 0.9999997 |

These are strong sampled identification screens, not full-tensor hashes of each conditioner body.
They identify the conditioner substrate; they do not identify the denoiser's teacher, dataset, or
training recipe.

### 3. Adaptation is visible at several scales

- **Distillation:** base and distilled Klein 4B retain an identical topology while replacing a
  50-step true-CFG recipe with a four-step single-call recipe.
- **KV specialization:** 9B-KV preserves architecture and high representational geometry while
  changing roughly 96% of denoiser elements and reducing repeated reference-token work.
- **Scale:** moving from Klein 4B to 9B changes denoiser and conditioner width and depth, but the
  small behavior panel does not improve monotonically.
- **Decoding:** the Small Decoder changes only the latent-to-pixel component, leaving conditioning
  and denoising outside the claim.

### 4. The strongest semantic result is local, distributed, and temporal

Klein 4B currently has the strongest BFL causal evidence, but it no longer clears an uncontested
bilateral six-control ladder. The surviving result is a distributed single-stream K/V intervention
route whose contribution grows with site coverage, accumulates across denoising calls, and beats
five valid controls. The corrected reverse wrong-world leg is frozen and queued. That is narrower
than a universal circuit—and more defensible.

## Conclusions

| Question | Evidence-backed answer |
|---|---|
| What did we measure? | Six pinned BFL generators and one pinned decoder component, each at an exact revision. |
| Is FLUX.2 simply FLUX.1 Schnell continued? | Not detectably in the tested residual-facing witness; broader ancestry remains open. |
| What does four-step distillation change? | The matched 4B pair keeps topology fixed and changes weights plus the denoising recipe; semantic reorganization is not yet artifact-reconciled. |
| What does 9B-KV change? | It makes a broad, geometry-preserving denoiser adaptation and reuses extracted reference K/V across steps. |
| Does model size predict the measured behavior? | No. The fixed panel is mixed and nearly flat in CLIP alignment. |
| Do we have causal FLUX evidence? | Yes: one fixed Klein 4B assay has a distributed native K/V intervention route with temporal accumulation and five valid controls. Bilateral six-control specificity awaits the corrected reverse wrong-world rerun. |
| Can the largest model be analyzed on constrained hardware? | Yes. Dev completed an exact one-step BF16 run through explicit conditioner/denoiser lifetime separation and paging. |
| Is the Small Decoder equivalent to the full decoder? | It was close and faster on one latent, but not pixel-exact or distributionally validated. |

The useful outcome is not that the Black Forest is fully mapped. It is that the family can be
measured with a repeatable standard: exact bytes before behavior, exact execution before
interpretation, and matched causal controls before mechanism claims. The seven artifacts already
show that this discipline can separate architecture, adaptation, runtime, behavior, readability,
and causality instead of collapsing them into one model-quality narrative.

## Scope and reproducibility

This report is current through **August 2, 2026**. FLUX.1 Dev, Pro, Fill, Canny, Kontext, Krea,
FLUX.2 base 9B, quantized variants, and other BFL releases were not part of the verified local panel
and are not silently represented here. A newer generational-observatory project has a reviewed
design scaffold but no model-bearing outcome runs, so it contributes no additional findings to this
edition.

The detailed custody ledger, artifact locations, run identifiers, and evidence precedence live in
the [[../black-forest-labs-model-wiki|Black Forest Labs Model Wiki]] and
[[../experiments/bfl-flux2-lineage-sweep|BFL FLUX.2 Lineage Sweep]]. The strongest causal result is
reported separately in [[2026-08-01-h9-native-specificity-replication|H9 After Adversarial Review]].
These records are supporting provenance; the analysis and boundaries needed to interpret every
model are contained in this report.
