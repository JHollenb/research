---
title: Black Forest Labs Model Wiki
type: wiki
status: active
updated: 2026-08-18
claim_status: adversarially-reviewed-synthesis
source_policy: latest verified BFL artifact and adjudication wins; historical boundaries retained
tags: [wiki, black-forest-labs, flux, flux1, flux2, diffusion, rectified-flow, image-generation, model-analysis, vae, decoder, static-analysis, shard-comparison, saturn, rosetta, mamba, cross-family, circuit-search]
related:
  - "[[blog/2026-08-03-135833-the-models-had-metabolisms-not-just-scores|The Models Had Metabolisms, Not Just Scores]]"
  - "[[generative-model-wiki|Generative Model Wiki]]"
  - "[[tools/generative-model-debugger|Generative Model Debugger]]"
  - "[[indexes/black-forest-labs-survey|Black Forest Labs Research Survey]]"
  - "[[indexes/generative-model-analysis|Generative Model Analysis Index]]"
  - "[[blog/2026-08-02-seven-flux-artifacts-under-the-microscope|Seven FLUX Artifacts Under the Microscope]]"
  - "[[blog/2026-08-03-153511-the-vae-was-a-stable-boundary|The VAE Was a Stable Boundary, Not the Scaling Axis]]"
  - "[[blog/2026-08-03-160047-how-the-black-forest-models-work-from-conditioner-to-pixels|From Conditioner to Pixels]]"
  - "[[blog/2026-08-01-040000-inside-the-flux-arbitration-harness|FLUX Arbitration Harness arc]]"
  - "[[blog/2026-08-01-213500-the-answer-fiber-became-a-consumer-quorum|Qwen E1-lite consumer quorum comparison]]"
  - "[[blog/2026-08-02-e1-followup-transport-frontier|Qwen E1 follow-up transport frontier comparison]]"
  - "[[experiments/bfl-flux2-lineage-sweep|BFL FLUX.2 Lineage Sweep]]"
  - "[[experiments/bfl-frontier-program-2026-07-31|BFL Frontier Program]]"
  - "[[bfl-overview|BFL Overview]]"
  - "[[blog/2026-08-01-black-forest-labs-model-analysis-capabilities-report|Shareable BFL Capabilities Report]]"
  - "[[blog/2026-08-02-black-forest-labs-measured-model-reference|Measured BFL Model Reference]]"
  - "[[blog/2026-08-04-104147-the-scene-state-became-a-trainable-interface|The Scene State Became a Trainable Interface]]"
  - "[[blog/2026-08-04-112441-where-we-are-with-the-disassembled-image-model|Where We Are With the Disassembled Image Model]]"
  - "[[blog/2026-08-04-150000-one-character-five-worlds-flux|One Character, Five Worlds: Debugging Character Pinning in FLUX]]"
  - "[[blog/2026-08-04-182551-from-the-plane-to-a-debuggable-model|From the Plane to a Debuggable Model]]"
  - "[[blog/2026-08-04-220500-the-boundary-became-a-debugger|The Boundary Became a Debugger]]"
  - "[[blog/2026-08-06-titan-frames-acts-physical-binaries|Titan: Frames, Acts, and Physical Binaries]]"
  - "[[blog/2026-08-06-project-titan-frames-acts|Project TITAN: Making a Generative Model a Program of Frames and Acts]]"
  - "[[blog/2026-08-06-the-model-became-a-program-saturn-stack|The Model Became a Program: SATURN, TITAN, MARS, mstack, and manalysis]]"
  - "[[blog/2026-08-06-what-the-mars-saturn-benchmark-got-wrong|Erratum: What the MARS × SATURN Benchmark Got Wrong]]"
  - "[[blog/2026-08-05-120615-the-model-as-software-the-evidence-graph|The Model as Software: The Evidence Graph]]"
  - "[[blog/2026-08-05-black-forest-labs-experiment-report|BFL Model-by-Model Experiment Report]]"
  - "[[blog/2026-08-06-the-saturn-project|SATURN project]]"
  - "[[blog/2026-08-07-125447-saturn-mamba-rosetta|SATURN's Mamba Rosetta]]"
  - "[[blog/2026-08-06-can-we-find-causal-circuits-in-diffusion-models|Causal Circuits in Diffusion Models]]"
  - "[[blog/2026-08-06-the-image-token-map-found-the-spatial-circuit|Image-Token Spatial Circuit]]"
  - "[[blog/2026-08-06-tracer-seven-bfl-models|Tracer Across the Black Forest]]"
  - "[[experiments/bfl-tracer-2026-08-06/README|BFL Tracer and SATURN Model Ledger]]"
  - "[[blog/2026-08-06-saturn-native-debugger-first-circuit|SATURN Native Debugger]]"
  - "[[blog/2026-08-06-titan-native-scheduler-bounded-acceptance|TITAN Native Scheduler]]"
  - "[[../experiments/2026-08-02-bfl-three-claims/FINAL_ADJUDICATION|BFL Three-Claim Adversarial Adjudication]]"
  - "[[blog/2026-07-31-212627-what-we-know-about-the-black-forest-models-a-data-driven-report|Data-Driven BFL Report]]"
  - "[[experiments/flux-causal-programs-cross-calibration|FLUX Causal Programs Cross-Calibration]]"
  - "[[experiments/flux-fnet-mamba-mechanism-atlas|FLUX, FNet, and Mamba Mechanism Atlas]]"
  - "[[experiments/post-flux-toy-research|Post-FLUX Toy Research]]"
  - "[[experiments/diffract-diffusion-circuit-tracing|DifFRACT diffusion reference]]"
  - "[[flux-generation-by-design-proposal|FLUX Generation by Design]]"
---

# Black Forest Labs Model Wiki

This is the model-specific knowledge base for the Black Forest Labs FLUX family. It records what
we know about the exact pinned subjects in our custody, how the family changes across FLUX.1 and
FLUX.2, what the conditioner and denoiser actually do in the measured assays, and where the
mechanism claims stop.

The short answer is: **we have unusually strong custody, anatomy, runtime, lineage, and
assay-relative physiology.** The strongest terminal causal result is still the distributed
single-stream K/V intervention route in FLUX.2 Klein 4B with temporal accumulation and five valid
matched controls. The newest real-FLUX trend is stronger multi-step mediation evidence: across
four lighthouse/tram cases, all-step text-route transfer was donor-like in `4/4`, and a `joint.2`
ablation rescued by a `joint.3` donor state recovered `97.4%` of the lost image margin. That is
an exploratory route result, not a replacement for the H5–H9 terminal boundary. The original
bilateral H9 specificity verdict is superseded because the reverse wrong-world donor map was
contaminated; its direction-safe worker repair is now collected as raw evidence, while the frozen
familywise adjudication remains open. We do not have a compact universal quorum,
endogenous-necessity proof, cross-model circuit, complete prompt-to-pixel explanation, or
validated semantic quality-improvement recipe.

The neighboring [CUDA ScienceGraph lattice closure](blog/2026-08-01-cuda-sciencegraph-lattice-closure)
is intentionally not counted as BFL evidence: it is a Qwen2.5 language-model position-lattice
certificate and runtime replay. It is linked here only to prevent the two causal programs from
being conflated; the BFL result remains the separate FLUX.2 H5–H9 assay-relative route.
The newer Qwen E1-lite and clean-target follow-up results are likewise comparisons, not BFL
evidence: Qwen supports a local original-consumer quorum, but its broad follow-up quorum fails;
the FLUX program supports a distributed intervention route and block-13 carrier without a compact
universal quorum. The two claims remain separate until a cross-modal test exists.

## Start here

- [[bfl-overview|BFL Overview]] — model-by-model summary of what we measured and what each result means.
- [[blog/2026-08-03-135833-the-models-had-metabolisms-not-just-scores|The Models Had Metabolisms, Not Just Scores]] — anatomy-and-physiology survey of the seven measured BFL artifacts, including the latest 9B route qualification and independent H9R audit.
- [[indexes/black-forest-labs-survey|Black Forest Labs Research Survey]] — run-oriented synthesis of the measured findings, novel BFL-relevant measurements, and informative failed runs.
- [[blog/2026-08-02-seven-flux-artifacts-under-the-microscope|Seven FLUX Artifacts Under the Microscope]] — standalone, publication-ready analysis of every measured BFL artifact, its methods, results, and evidence ceiling.
- [[blog/2026-08-03-153511-the-vae-was-a-stable-boundary|The VAE Was a Stable Boundary, Not the Scaling Axis]] — exact-static and paired-decoder synthesis: ordinary VAE budget conservation, the FLUX.1→FLUX.2 latent ABI change, and the Small Decoder output-interface tradeoff.
- [[blog/2026-08-03-160047-how-the-black-forest-models-work-from-conditioner-to-pixels|From Conditioner to Pixels]] — the full conditioner → denoiser → latent → VAE/pixel chain and how the recorder, decoder, shard comparison, and generational work fit together.
- [[blog/2026-08-04-104147-the-scene-state-became-a-trainable-interface|The Scene State Became a Trainable Interface]] — a frozen FLUX.1 host, runtime-owned typed scene state, held-out teacher alignment, and the completed image-level battery showing trajectory movement without typed semantic control.
- [[blog/2026-08-04-112441-where-we-are-with-the-disassembled-image-model|Where We Are With the Disassembled Image Model]] — current component-wise state of the work: executable model boundaries, recorder/decoder IO debugging, the one trained bridge, the semantic-battery corrections, and the next repair sequence.
- [[blog/2026-08-04-150000-one-character-five-worlds-flux|One Character, Five Worlds: Debugging Character Pinning in FLUX]] — the first reference-conditioned character-retention gallery, trajectory localization, partial activation transport, and reversible live BF16 weight edit on FLUX.2 Klein 4B.
- [[blog/2026-08-04-182551-from-the-plane-to-a-debuggable-model|From the Plane to a Debuggable Model]] — full cross-arc synthesis and the latest recipient-aware reference-swap, no-op, wrong-donor, and consumer-trace results.
- [[blog/2026-08-04-220500-the-boundary-became-a-debugger|The Boundary Became a Debugger]] — independent FLUX VAE execution, exact latent-boundary matching, decoder hypergraph seams, CPU/CUDA divergence, and the NCCL hardware admission result.
- [[blog/2026-08-06-project-titan-frames-acts|Project TITAN: Making a Generative Model a Program of Frames and Acts]] — the SATURN-adjacent Frame/Act runtime, exact native scheduler/VAE seam replacement on the pinned FLUX.2 path, framework-free ABI proof, and the open boundary to a standalone generator.
- [[blog/2026-08-06-the-model-became-a-program-saturn-stack|The Model Became a Program: SATURN, TITAN, MARS, mstack, and manalysis]] — the cross-tool synthesis of the FLUX runtime, binary replacement boundary, debugger, mapper, hypergraph, batching, caching, and student work.
- [[blog/2026-08-07-125447-saturn-mamba-rosetta|SATURN's Mamba Rosetta: Same FLUX.2 Suffix, Different Image]] — an external Mamba-1.4B conditioner crossed the native Qwen-facing `PromptEmbeds` ABI while the FLUX.2 suffix stayed fixed; the resulting semantic mismatch is retained as circuit-search evidence.
- [[blog/2026-08-05-120615-the-model-as-software-the-evidence-graph|The Model as Software: Removing Confounds, Tracing Resolution, and Building a Shared Evidence Graph]] — same-device donor propagation, native-1024 versus latent-resize tracing, and the shared recorder-to-pixels evidence graph.
- [[tools/generative-model-debugger|Generative Model Debugger]] — the reusable debugger reference for typed component IO, replay, consumer propagation, execution hypergraphs, spatial seams, and distributed boundaries.
- [[../experiments/2026-08-02-bfl-three-claims/FINAL_ADJUDICATION|BFL Three-Claim Adversarial Adjudication]] — investigator packets, adversarial attacks, owner repairs, and publication-safe language for the three strongest claims.
- [[blog/2026-07-31-212627-what-we-know-about-the-black-forest-models-a-data-driven-report|What We Know About the Black Forest Models]] — broad measured report.
- [[experiments/bfl-flux2-lineage-sweep|BFL FLUX.2 Lineage Sweep]] — canonical owner for the six-generator cohort plus Small Decoder boundary and evidence cards.
- [[experiments/bfl-frontier-program-2026-07-31|BFL Frontier Program]] — lineage, distillation, KV, typography, statics, and causal tracks.
- [[experiments/flux-causal-programs-cross-calibration|FLUX Causal Programs Cross-Calibration]] — proposed shared-controls contract between behavior-first and weight-statics programs; no experiment artifact was changed.
- [[experiments/flux-fnet-mamba-mechanism-atlas|FLUX, FNet, and Mamba Mechanism Atlas]] — historical FLUX.1 static/cross-architecture baseline; its old FLUX.2 access block is superseded by the lineage sweep.
- [[experiments/post-flux-toy-research|Post-FLUX Toy Research]] — measured toy mechanisms that inform future designs, explicitly not BFL model evidence.
- [[experiments/diffract-diffusion-circuit-tracing|DifFRACT diffusion circuit tracing reference]] — external FLUX.1[schnell] method/case-study reference, not a local result.
- [[experiments/model-understanding-discriminating-experiments|Model Understanding Discriminating Experiments]] — E11 is the proposed FLUX block-13 carrier-closure test; it has no result yet.
- [[blog/2026-07-31-145130-the-conditioners-were-stock-checkpoints|Conditioner provenance]] — exact public parent checkpoints for the FLUX.2 conditioners.
- [[blog/2026-08-01-001500-opening-the-black-forest-what-six-parallel-tracks-taught-us-about-flux|Six-track synthesis]] — latest integrated account of the frontier program.
- [[blog/2026-08-01-black-forest-labs-model-analysis-capabilities-report|Shareable BFL Capabilities Report]] — external-facing summary of the measured capabilities, findings, live demonstration path, and open boundaries.
- [[blog/2026-08-02-black-forest-labs-measured-model-reference|Measured BFL Model Reference]] — non-narrative card for every measured BFL artifact, including the latest Schnell admission result.
- [[blog/2026-08-01-h9-native-specificity-replication|H9 adversarial correction and repair]] — current owner verdict, surviving five-control result, and the collected raw H9R repair with terminal adjudication boundary.
- [[blog/2026-08-01-213500-the-answer-fiber-became-a-consumer-quorum|Qwen E1-lite consumer quorum]] — neighboring language-model result; linked for boundary comparison, not counted as BFL evidence.
- [[blog/2026-08-02-e1-followup-transport-frontier|Qwen E1 follow-up transport frontier]] — shows that the original Qwen consumer quorum does not automatically become a later-query quorum; not counted as BFL evidence.
- [[blog/2026-08-01-040000-inside-the-flux-arbitration-harness|FLUX Arbitration Harness arc]] — complete H1–H9 route-resolution report.
- [[indexes/generative-model-analysis|Generative Model Analysis Index]] — cross-modal synthesis and claim boundary.
- [[../gen-anal/image-atlas-nucleus-freeze.ifleUZ/BFL_FLUX2_REPORT|BFL_FLUX2_REPORT.md]] — source report for architecture, runtime, behavior, and historical claim boundaries.
- [[generative-model-wiki|Generative Model Wiki]] — modality-wide context and neighboring model families.

## How to read the claims

```mermaid
flowchart LR
  A["Pinned BFL artifact"] --> B["Static anatomy / provenance"]
  B --> C["Certified trajectory / behavior"]
  C --> D["Readability / physiology"]
  D --> E["Native causal route"]
  E --> F["Generalization / portability"]
```

| Evidence class | Current BFL example | Boundary |
|---|---|---|
| **Custody** | Immutable revisions, manifests, tensor inventories, MLflow references, Beast model bytes. | Does not establish behavior or meaning. |
| **Anatomy** | Component parameter counts, block programs, Qwen/Mistral conditioner identities, KV/base/distilled inventory comparisons. | Describes what can exist, not what is used. |
| **Runtime / instrument** | Exact stock trajectories, cache extraction/application, Dev component decoupling, decoder swap, phase-CUDA parity. | Certifies execution and delivery, not semantic causality. |
| **Behavior** | Matched 512px panels, count cliff, typography substrate, Dev diagnostic panel. | Recipe-, seed-, prompt-, precision-, and resolution-specific. |
| **Readability** | Pooled concept contrasts, CKA, conditioner cartography, stream/time readouts. | Information can be readable without being load-bearing. |
| **Causal physiology** | H5–H9 K/V intervention route in the fixed Klein 4B/Qwen3 binding assay; five H9 controls remain valid; H9R raw repair has completed. | The terminal six-contrast bilateral adjudication, endogenous necessity, universal quorum, and cross-model portability remain open. |
| **Open / proposed** | Distillation-transfer generalization, typography causal ladder, Dev/9B portability, quality edits. | Do not cite as measured results. |

## The pinned cohort

This is the cohort actually covered by the BFL sweep. It is not a catalog of every BFL product or
release. FLUX.1 Dev/Pro/Fill/Canny, Kontext, Krea, and other BFL variants are outside this wiki's
measured cohort unless a linked owner adds them.

| Subject | Exact revision | Package / role | Conditioner | Current evidence status |
|---|---|---:|---|---|
| **FLUX.1 Schnell** | `741f7c3ce8b383c54771c7003378a50191e9efe9` | 16.860B baseline generator | CLIP + T5 | Common behavior, recorder, readouts, legacy intervention; FLUX.1 witness for lineage. |
| **FLUX.2 Klein 4B** | `e7b7dc27f91deacad38e78976d1f2b499d76a294` | 7.982B step-distilled generator | Qwen3-4B | Common behavior, exact trajectories, stream/time readouts, H5–H9 causal route assay. |
| **FLUX.2 Klein base 4B** | `a3b4f484…` | 7.982B undistilled 50-step matched pair | Qwen3-4B family | Acquired and trajectory-certified; activation-forensics synthesis is not promoted pending local final-artifact reconciliation. |
| **FLUX.2 Klein 9B** | `92196c8e11f7b6cf2b7493e037d8c5345c559216` | 17.353B generator | Qwen3-8B | Common behavior, recorder/readouts, exact stock trajectory. |
| **FLUX.2 Klein 9B-KV** | `a6dfb36eca3a3906eb2fd460795adfb844e5fcce` | 17.353B cache-specialized sibling | Qwen3-8B | Same tensor shapes/inventory as 9B, different denoiser weights; reference-KV trajectory and cache probe. |
| **FLUX.2 Dev** | `26afe3a78bb242c0a8bb181dcc8937bb16e5c66c` | 56.319B flagship generator | Mistral-Small-3.2-24B | Exact component-decoupled BF16 execution, later full-suite runtime/behavior/recorder legs; semantic mechanism open. |
| **FLUX.2 Small Decoder** | `a3efc24f613ef42d9428af62fdbd6f5fd8856c4a` | 62.373M decoder component | none | Static anatomy and paired latent decode only; not a generator or denoiser mechanism result. |

The model bytes remain on Beast under `/mnt/big/llm-models`; the lineage mirror is
`s3://experiments/model-analysis/bfl-flux2-lineage-v1/results/`. The sweep mirror contains
2,883 manifest-tracked objects and 17.442 GB with no missing objects or size mismatches in the
verified listing.

## Architecture and lineage

All pinned generators are attention-based rectified-flow / diffusion-transformer systems. The
held cohort contains no Mamba/state-space, sparse-MoE, scene-register, or persistent symbolic
scene substrate. That conclusion is about the loaded configurations and tensors, not a claim
about all future BFL models.

| Subject | Denoiser | Conditioner | VAE | Transformer program |
|---|---:|---:|---:|---|
| FLUX.1 Schnell | 11.891B | 4.885B CLIP+T5 | 83.8M | 19 joint + 38 single, width 3,072 |
| Klein 4B | 3.876B | 4.022B Qwen3 | 84.0M | 5 joint + 20 single, width 3,072 |
| Klein 9B / 9B-KV | 9.079B | 8.191B Qwen3 | 84.0M | 8 joint + 24 single, width 4,096 |
| FLUX.2 Dev | 32.223B | 24.011B Mistral3 | 84.0M | 8 joint + 48 merged/single, width 6,144 |
| Small Decoder | — | — | narrowed decoder | encoder 128/256/512/512; decoder 96/192/384/384 |

### FLUX.1 Schnell → FLUX.2 Klein

Klein 4B is not a simple smaller Schnell. Both denoisers have width 3,072, but the program
changes from 57 transformer blocks to 25, replaces CLIP+T5 with Qwen3, changes the conditioning
interface, and uses a four-step distillation regime. The denoiser falls from 11.891B to 3.876B
parameters while the conditioner remains roughly 4B. This transition changes topology, conditioner,
and training regime together.

The exploratory architectural cliff is also clear: Schnell carries attention K bias in fused QKV,
while FLUX.2 drops that bias and retains QK-norm gains. The bias→QK-norm comparison is useful
statics, not a causal explanation of the models.

### FLUX.2 Klein 4B → 9B

The 9B model scales both the denoiser and conditioner: width rises from 3,072 to 4,096, heads
from 24 to 32, joint blocks from 5 to 8, and post-joint blocks from 20 to 24. The common panel
does not improve monotonically with size; parameter count is not a mechanism or quality proxy.

### Klein 9B → Klein 9B-KV

This is the cleanest natural adaptation control:

- 883 tensors, 17,353,362,980 parameters, and complete tensor metadata are shape/inventory matched.
- The exact denoiser denominator is 233 tensors and 9,078,581,248 BF16 elements; 8,725,252,912
  elements differ (96.10811065795288%).
- The denoiser shards differ, while all text-encoder and VAE shard pairs are byte-identical.
- The standard path recomputes reference-image information; KV extracts reference K/V once and reuses it.
- In one 512px/four-step reference probe, standard processed 2,048 tokens on all calls; KV processed 2,048 once, then 1,024 target tokens on three cache-apply calls.
- The measured probe was about 1.073× faster for KV, with a maximum observed cache of 512 MiB.

This is cross-step reference-K/V reuse. It is not recurrence, a scene register, Mamba state, or
sparse dirty-tile rendering.

### Klein base 4B → distilled Klein 4B

The public matched pair has identical tensor inventory: 818 tensors and 7,982,059,044
parameters. The recorded configuration difference is the distilled flag/recipe; the change is
in the weights and denoising trajectory, not a topology rewrite.

The pair passed adapter and trajectory certification, including 658/658 exact registered trajectory
observations and bit-exact CUDA-BF16 CFG recombination. These are comparison points along one run,
not saved model checkpoints.

A later synthesis reports P1–P4 activation-forensics outcomes, but the current local owner status
still marks the capture phase in flight and the cited final adjudication artifact is absent from this
workspace. Those claims are therefore retained as historical synthesis, not promoted as current
evidence. Until the artifact is reconciled, the supported interpretation stops at an identical
topology, distinct weights, and an exactly certified 50-step true-CFG versus four-step distilled
trajectory. Semantic preservation, loss, and reorganization remain open.

### FLUX.2 Dev and Small Decoder

Dev is a systems-scale version of the same broad program: a 32.223B denoiser, 24.011B
conditioner, width 6,144, and explicit component lifetimes. mrun executed the exact BF16 path by
persisting prompt embeddings, releasing the conditioner, then loading the denoiser through
CPU/disk dispatch. The conditioner and denoiser were never co-resident; swap telemetry confirms
that paging carried the run.

The Small Decoder narrows only the latent-to-pixel decoder boundary. It leaves the denoiser,
conditioning, and global image mixing untouched.

The decoder-specific synthesis is [[blog/2026-08-03-153511-the-vae-was-a-stable-boundary|The VAE Was a Stable Boundary, Not the Scaling Axis]]. The exact per-tensor VAE shard comparison is tracked in
[[../experiments/2026-08-03-141631-generative-functional-rosetta-static-decode/results/vae-shard-comparison|the VAE shard report]]; it keeps package identity, pipeline connection, and byte identity as separate evidence levels.

The exact static result covered seven pinned subjects and all 21 pairwise comparisons:

- The ordinary FLUX.2 quartet (Klein base 4B, distilled 4B, 9B, and 9B-KV) is byte-identical
  across all six pairs: 251/251 VAE tensor payloads match in each pair.
- FLUX.1 Schnell has 244 VAE tensors rather than 251; none of its 244 common payloads match
  ordinary FLUX.2, so the FLUX.1→FLUX.2 comparison is a changed codec inventory/interface, not
  a byte-preserved VAE.
- Dev preserves the ordinary FLUX.2 251-name, 251-shape inventory and parameter count, but 250
  learned/state tensors change storage from BF16 to F32 and their raw payload bytes differ. The
  current pass does not test BF16→F32 numeric cast equivalence.
- Small Decoder has 62,373,348 parameters, 250 BF16→F32 transitions, 137 shape changes, and
  different payload bytes for all 251 common tensors. Its retained encoder is a topology/latent-
  interface fact, not a claim that encoder weights were copied.

This is static artifact evidence only. It establishes identity and representation boundaries; it
does not by itself establish a behavioral, semantic, or training-history consequence.

## Conditioner provenance

The conditioner side is the clearest provenance result in the family. A byte-screen over three
sampled 256-row embedding chunks plus eigenbasis lineups identified:

| BFL component | Public parent | Evidence |
|---|---|---|
| Dev text encoder | `mistralai/Mistral-Small-3.2-24B-Instruct-2506` | sampled embedding bytes match; eigenbasis ≈ `0.9999997` |
| Klein 9B text encoder | `Qwen/Qwen3-8B` | sampled embedding bytes match; eigenbasis ≈ `0.9999992` |
| Klein 4B text encoder | `Qwen/Qwen3-4B` | sampled embedding bytes match; eigenbasis ≈ `0.9999999` |

The evidence boundary matters:

- The byte result is a three-chunk identification screen, not a full-tensor hash.
- The input embedding was compared; the entire conditioner body is not yet byte-certified.
- The instrument identifies substrate/parent, not the denoiser's teacher or training data.
- The public parent names the checkpoint family; the sampled bytes identify the exact candidate in this lineup.

This provenance result also explains why the FLUX denoisers remain the black forest: they have no
vocabulary embedding and no public parent against which the same instrument can directly line up.

## Denoiser lineage and adaptation

### FLUX.2 versus FLUX.1

A validated principal-angle lineup used known related pairs first:

| Validation / question arm | Measured alignment |
|---|---:|
| Klein 9B ↔ 9B-KV known finetune pair | T1 17-object panel: `0.9977`, minimum `0.9914`; separate 249-object k=64 minimum `0.930871` at near-degenerate `norm_out.linear` |
| Klein base 4B ↔ distilled 4B known pair | `0.9991` minimum `0.9964` |
| Klein 4B ↔ FLUX.1 Schnell, 1,425 depth×depth cells | median `0.0205` vs analytic null `0.0208`; max `0.0224` |

The 25 frozen depth-matched cells supply the `0.0205` median; the complete 1,425-cell matrix supplies
the `0.0224` maximum. Zero of 50 matched primary QKV objects shared the first streamed chunk hash;
that is not a full-tensor byte test. The original reader used Hub `main`, so current exact-revision
matching is retrospective rather than self-contained historical custody.

The frozen verdict is **NO DETECTABLE INHERITANCE**: FLUX.2 Klein is not measurably closer to
Schnell than the matched random null in this validated residual-facing lineup. The honest boundary
is that a warm start whose subspaces fully rotated away would look the same as a fresh start.

The within-family adaptation result is stronger: finetuning and step distillation are near-zero
rotation events on residual-facing subspaces even though the weights changed. This supports a
useful derivative-fingerprinting method; it does not prove training-history identity or semantic
inheritance.

### What KV training changed

The complete 9B↔9B-KV delta map finds a distributed change rather than a surgical rewrite:

- exactly 8,725,252,912 / 9,078,581,248 denoiser elements changed (`96.1081%`);
- median tensor relative Frobenius delta is `0.041628`;
- Q/K deltas dominate, while V and attention-output deltas are smaller;
- nine-coordinate activation CKA medians are `0.9382467` linear and `0.9447244` RBF;
- a receipt-bound ten-object true-FP64 check upholds primary k=64 Q/K/V/output geometry, while
  global `proj_out` is unstable at an effectively degenerate k=256 cutoff;
- the measured anatomy is consistent with re-aligned query-key matching for cached reference K/V.

That last sentence is a working interpretation of the delta pattern, not Q/K→cache causality or a
private training-history result.

## Behavior at the common operating point

The common panel uses 14 prompts, two seeds, 512×512 renders, and four denoising steps. These are
deployment-recipe diagnostics, not a universal quality leaderboard.

| Model | Mean CLIP | Count exactness | OCR exact / char accuracy |
|---|---:|---:|---:|
| FLUX.1 Schnell | `0.351` | `0.500` | `0 / 0.083` |
| Klein 4B | `0.351` | `0.833` | `0 / 0.000` |
| Klein 9B | `0.354` | `0.500` | `0.250 / 0.307` |
| Klein 9B-KV | `0.353` | `0.667` | `0 / 0.209` |
| Dev diagnostic tier | `0.360` | `0.833` | `0.250 / 0.472` |

The narrow practical reading is: Klein 4B was the best quality/latency/host-memory balance in
the tested recipe; KV's advantage is reference execution; Dev's result is diagnostic and
component-decoupled; OCR is an auxiliary measure, not ground truth.

### Counting

Klein 4B has a sharp count cliff in the matched diagnostic panel:

| Requested count | Exact rate |
|---:|---:|
| 2 | `1.000` |
| 3 | `0.875` |
| 4 | `0.875` |
| 5 | `0.4375` |
| 6 | `0.1875` |
| 7 | `0.0625` |

The early causal interpretation—“joint.4 call 2 is the counting circuit”—did not survive
adjudication. The site is behaviorally live, but not a necessary bottleneck.

### Typography

The frozen 256-pair behavior substrate decomposed text rendering into distinct failure modes:

| Family | Pair admission | What it says |
|---|---:|---|
| Spelling, plain / specific | `0.9375` / `0.906` | Spelling transitions are comparatively robust. |
| Presence, plain / specific | `0.500` / `0.500` | Lexically gated: `open` ≈ `0.94–1.00`, `exit` ≈ `0.00–0.0625`. |
| Substitution, specific | `0.469` | `open↔closed` can work; `push↔pull` is near-dead at `0.125`. |
| Substitution, plain | `0.094` | Both arms are near failure. |

This turns “text rendering is bad” into three different problems: spelling transitions, word-
presence gating, and semantic substitution. The panel is a behavior result; the causal typography
ladder remains gated on sealed-report custody and behavior admission.

## The current causal result: H5–H9

The strongest BFL mechanism work is the FLUX.2 Klein 4B/Qwen3 binding assay. It should be read as
a sequence, because each stage narrows a different alternative.

| Stage | Question | Result |
|---|---|---|
| **H5** | Is there a native denoiser route that moves binding? | Yes; distributed single-stream K/V sites are causally live, with block 13 a contributor. |
| **H6** | Does route dose matter? | Yes; full20 shows a nonlinear route-dose transition; S4/S8 move margins but are not endpoint-sufficient. |
| **H7** | Does the route replicate on held-out workload? | The distributed route replicates; compact quorum does not. Native-versus-wrong-world specificity was inconclusive at that power. |
| **H8** | Is the effect only a late scheduler call? | No; all-step grafting beats every single-step arm. The route accumulates across time. |
| **H9** | Does native source identity beat matched controls? | Five controls remain valid and positive; the original reverse wrong-world arm has 45/96 donor-color collisions. H9R now has direction-safe raw repair evidence, but the bilateral six-control family is not terminally closed. |

H9 used 96 paired instances and 1,152 renders. All image hashes and row metadata reverified. The
five valid controls retain positive conservative six-family lower bounds, with minimum `+2.345`.
The contaminated reverse wrong-world statistic remains a trend only. Full20 endpoint recovery was
83/96 forward and 88/96 reverse, while S4 remained a continuous-margin intervention.

The defensible current statement is:

> FLUX.2 Klein 4B supports an assay-relative, distributed single-stream K/V intervention route whose
> binding-related behavioral quotient accumulates across denoising time. Broad full20 coverage
> makes endpoint transfer reliable, and native S4 beats five admissible controls. The direction-safe
> reverse wrong-world worker rerun is now raw-repair-ready; bilateral six-control specificity remains
> pending until the frozen familywise adjudicator passes.

This is not the initially expected compact `{8,11}` quorum. It is not a universal list of magic
blocks, not a cross-model circuit, and not proof that all image concepts use the same route.

### Upstream conditioner result

Conditioner cartography compares the stock Qwen3-4B conditioner against the Schnell CLIP+T5
conditioners. All three separate color from object internally, so “Qwen3 simply encodes color
better” is not supported. The measured divergence is reconstruction:

- Qwen3 absorbs color-token information and later reconstructs it at output positions; final color/noncolor norm ratio `0.936`, effective rank `10.1`.
- T5 remains around `0.10–0.16` after absorption; CLIP recovers only to about `0.269` with effective rank around `2.2`.
- FLUX.1 Schnell fails the color-binding admission at `0.375`; Klein 4B passes the corresponding assay at `1.000`.

The interpretation is that the conditioner supplies a position-rich representation that the
denoiser can distribute. It is not a proof that Qwen3 alone causes the image result; the denoiser,
recipe, and model family also change.

## Runtime and engineering results

### mrun phase-CUDA engine

The BFL program forced a temporal residency split for Diffusers: encode phase, denoise phase,
release/reload boundaries, and explicit measured reservations. The resulting path achieved:

- bitwise parity `8/8` against the offload baseline;
- `0.607 s/image` versus `6.469 s/image`;
- `10.66×` per-image and `6.25×` end-to-end speedup;
- typography replay around `1.2 s/pair`.

This is a runtime result. It does not imply better images or a different model mechanism.

### Dev paging

The 112.805 GB BF16 package ran without co-resident 24.011B conditioner and 32.223B denoiser:
prompt embeddings were persisted, the conditioner was released, and the denoiser loaded through
CPU/disk dispatch. Swap telemetry confirms that the execution was genuinely paged. This expands
the analysis envelope; it is not a production throughput claim.

### Small Decoder

The decoder path removes 43.678% of decoder parameters, measured `1.517×` faster repeated decode,
and achieved cosine `0.999784` / PSNR `44.64 dB` on one persisted latent. Pixel exactness did not
hold, and one latent cannot establish distribution-wide perceptual equivalence.

## What failed, was corrected, or remains bounded

- **No detectable FLUX.1 denoiser inheritance** is a validated negative within the held witness panel, not proof that no warm start ever occurred.
- **The counting circuit claim was refused.** The original strict replication passed only `5/16`; the paraphrase canary passed `0/16`; wrong-site rescue reached `0.609`; effects were seed-gated and location/lexicalization-sensitive.
- **The compact quorum hypothesis failed.** H5–H9 support a distributed route, not a small sufficient set like `{8,11}`.
- **The original H9 bilateral specificity gate was superseded.** The reverse wrong-world map has
  `45/96` donor-color collisions. Direction-specific maps and regression tests are fixed; the
  low-priority repair worker has completed as raw evidence, but it is not terminal bilateral evidence
  until the frozen familywise adjudicator passes.
- **Weight statics did not cleanly predict semantic-port ranking.** A later input-rank survivor was multiplicity-eaten and is prospective-only; it is not a promoted image-side law.
- **Legacy pooled readouts and direction removal were not causal evidence.** Readability can be real while a direction is redundant, downstream, mistimed, or non-specific.
- **Denoiser provenance remains open.** The conditioner has sampled byte identity; the denoiser has no public parent embedding and no unique training-history explanation.
- **Quality-improvement prescriptions remain open.** We have runtime levers and diagnostic hypotheses, not a validated edit, retraining rule, pruning rule, or distillation recipe that improves semantic quality without regressions.
- **Human-facing evaluation is incomplete.** CLIP, OCR, counting, and manual panels do not establish broad preference, safety, bias, memorization, copyright behavior, or adversarial robustness.

### Residual-merge debugging (2026-08-04)

The new checkpointed debugger was applied to `decoder.up_blocks.1.resnets.0` in FLUX.2 Klein 4B.
The block was observed as an identity shortcut plus a normalized/convolved main branch and an
explicit residual merge. Control suffixes from `norm1`, `conv1`, `norm2`, and `conv2` reproduced the
recorded block output and final decoded tensor exactly. A F32-only residual-add island was also
exact, while a one-pixel shifted shortcut donor produced a much larger terminal change (L2 207.13,
cosine 0.92090). The result is a debugging trend about this route, not a semantic ownership claim;
see [[../experiments/2026-08-04-231120-flux-residual-merge-debug/ANALYSIS|the full residual-merge analysis]].

### Shortcut-donor matrix: matched specimens and consumer propagation (2026-08-04)

The residual merge is now being treated as a software port rather than only a tensor location.
The primary FLUX.2 Klein 4B path (seed `84101`) was held fixed while alternate matched VAE
specimens (seeds `84102` and `84103`) supplied shortcut donors at
`decoder.up_blocks.1.resnets.0`. The main `conv2` branch did not change across donor branches.

The completed mrun retry is `job-f06d61327575` (parent `job-15d80e720d57`). It ran the calibrated
rank-0 CUDA denoiser / rank-1 CPU VAE split for 425.59 s, with 30.49 GB peak RSS and 8.55 GB peak
VRAM. The first 26 GB declaration was killed by memory pressure; the retry grew to a 39.4 GB
reservation, and the measured result now calibrates future panels to 32 GB RAM without changing
the measured 14 GB VRAM route.

The donor matrix produced a clear scale ordering in the decoded tensor:

| Donor family | Terminal cosine vs identity | Dominant-region mask flip |
|---|---:|---:|
| one-pixel spatial shifts | 0.911–0.921 | 3.46–4.46% |
| alternate seed shortcut | 0.705–0.739 | 11.49–13.04% |
| zero/main-branch donor | 0.377–0.403 | 77.98–78.57% |
| F32 precision island | 1.000 | 0% |

The consumer trace shows the VAE route, not just the terminal image: alternate-seed donor changes
were amplified about `6×` at `decoder.up_blocks.1.after_resnet0`, `14–15×` at `up_blocks.2`, and
`13×` at `up_blocks.3`, then attenuated to about `0.04×` of the source delta by `decoder.tail`
while remaining nonzero at the output. This supports a working description of a donor port feeding
an expansion/amplification chain followed by renderer-scale attenuation.

This is not yet an identity circuit claim. The alternate seeds change the whole upstream denoiser
trajectory, the replay only isolates the VAE response to their shortcut tensors, and the CPU VAE
replacement is not byte-identical to the CUDA reference after the VAE boundary. The full evidence
and independent color/mask/edge/flipbook measurements are in
[[../experiments/2026-08-04-234635-flux-shortcut-donor-matrix/ANALYSIS|the shortcut-donor matrix
analysis]] and [[../tools/generative-model-debugger|the generative-model debugger wiki]].

The next BFL question is whether the same donor behavior survives a small spatial panel, reference
swaps, multiple seeds, and neighboring residual blocks. That is a trend study, not a certification
gate.

## Complete experiment and work ledger (2026-07-19–2026-08-06)

This is the current consolidation ledger for the Black Forest Labs program. It includes model
science, failed or corrected instruments, runtime work, debugger work, and the SATURN/TITAN
continuation. A row is not automatically a terminal claim: the status column preserves whether the
evidence is an observation, trend, diagnostic, bounded claim, or open design. The full retry,
cancellation, custody, and scheduler history remains immutable in the
[[../experiments/2026-08-01-233923-bfl-generational-model-observatory/RUNS|BFL Observatory run ledger]].

### Model, lineage, behavior, and causal program

| Experiment / owner | Measurements retained | Current interpretation and boundary |
|---|---|---|
| [[../experiments/2026-07-24-generative-image-model-atlas/CURRENT_SYNTHESIS|FLUX.2 model atlas]] and [[experiments/bfl-flux2-lineage-sweep|lineage sweep]] | Seven pinned artifacts: six generators plus Small Decoder; exact revisions, manifests, tensor inventories, 2,883 mirrored objects / 17.442 GB in the lineage mirror, and 21 pairwise static comparisons. | The custody/anatomy baseline for every later claim. Model bytes, parameter counts, and module topology are not behavior or semantic evidence. |
| [[../experiments/2026-08-01-233923-bfl-generational-model-observatory/RUNS|Generational observatory]] | The corrected snapshot records 682 source artifacts, 166 typed attempts, and 167 MLflow pointer rows. It retains successful, failed, cancelled, unsupported, and custody-incomplete runs rather than treating them as absence. | Canonical run history. Retries and copied synthesis bundles are attached to owner runs, not counted as new discoveries. |
| [[../experiments/2026-07-31-dit-weight-subspace-lineage|Schnell → Klein lineage]] | 1,425 matched cells; median residual-facing alignment `0.0205` versus analytic null `0.0208`; complete matrix maximum `0.0224`; `0/50` matched QKV first-chunk hashes shared. | Bounded no-detectable-inheritance result for this witness/instrument, not proof of fresh initialization or private training history. |
| [[../experiments/2026-08-01-flux1-schnell-arbitration/PLAN|Schnell arbitration]] | At 512/768/1024 px, clean/corrupt rates were `0.750/0.625`, `0.625/0.750`, and `0.375/0.6875`; the 1024 px eight-step retry was unchanged. All missed the `0.9375` admission floor. | G0 instrumentation passed, G1 workload admission failed. This is an assay/conditioner/recipe boundary, not a universal Schnell incapability claim. |
| [[../experiments/2026-07-31-klein-base-distillation-forensics/STATUS|Base ↔ distilled Klein 4B]] | Identical `818`-tensor, `7,982,059,044`-parameter inventory; adapter `22/22`; true-CFG trajectory `31/31`; checkpoints `658/658`; sigma matching maps distilled calls `{0,1,3}` near base calls `{0,10,34}`. | Exact matched substrate and trajectory evidence. Final activation-forensics artifact is still unreconciled, so P1–P4 remain synthesis-reported rather than promoted. |
| [[../experiments/2026-07-31-typography-behavior-substrate/STATUS|Counting and typography]] | Counting replication: strict wording `5/16`, paraphrase `0/16`; typography discovery `125/256`, confirmation `113/192`, final `spell-plain` certificate `39/48`. Spelling admitted `0.9375/0.906`; `open↔closed` `0.8125`; `push↔pull` `0.125`. | Structured lexical and operation-specific behavior. The old single counting site was demoted; no typography causal ladder has been admitted. |
| [[../experiments/2026-08-02-bfl-three-claims/FINAL_ADJUDICATION|Three-claim adversarial adjudication]] | Rechecked Schnell→Klein lineage, 9B→9B-KV adaptation, and Klein H9. The 9B/KV pair has 883 tensors and `96.1081%` of denoiser BF16 elements changed; the H9 route recovered `83/96` forward and `88/96` reverse endpoints. | Keeps the strongest claims bounded. The contaminated H9 reverse wrong-world map contains `45/96` donor-color collisions; its five valid controls survive, but bilateral specificity is still open. |
| [[../experiments/2026-07-31-211500-flux-arbitration-harness|H5–H9 Klein 4B route]] | Twenty single-stream sites over four denoising calls; all-step grafting beats single-step arms; no compact site quorum is sufficient; native S4 margins were `+6.740` forward and `+8.830` reverse. | Current terminal causal result: an assay-relative distributed K/V route with temporal accumulation. It is not endogenous necessity, a universal quorum, cross-model portability, or a quality-edit recipe. |
| [[../experiments/2026-07-29-202802-flux2-fp32-control-feasibility|Reference behavior / semantic-port program]] | Count, paraphrase, corner, top-left, grid, dual-stream, full-trajectory, semantic-port, and causal canary arms are retained with their per-job reports and custody receipts. | A family of bounded reference behaviors and proposed semantic-port tests. The reports are not collapsed into a single “circuit” verdict. |

### Runtime, boundaries, editing, and consumer propagation

| Experiment / owner | Measurements retained | Current interpretation and boundary |
|---|---|---|
| [[../experiments/2026-07-27-flux2-dev-full-failure-diagnosis/REPORT|Dev diagnosis and component-decoupled execution]] | The stock frontend had `32/32` typed load failures; the repaired component-decoupled probe passed its lifecycle checks and produced a one-step image in about `336.41 s`, with about `12.7 GB` swap at forward completion. | The guarded one-step BF16 runtime is admitted. The richer unguarded Dev behavior/recorder suite remains diagnostic. |
| [[../experiments/2026-08-03-141631-generative-functional-rosetta-static-decode/results/vae-shard-comparison|VAE shard comparison]], [[blog/2026-08-04-220500-the-boundary-became-a-debugger|VAE boundary]] and [[../experiments/2026-08-03-153000-flux2-dev-vae-boundary-probe/ANALYSIS|Dev VAE probe]] | FLUX.2 ordinary VAE payloads are matched across the cohort; the Small Decoder removes `43.678%` of decoder parameters, is about `1.517×` faster, and reaches pixel cosine `.999784` / PSNR `44.64 dB` but fails exact parity on `192/192` paired rows. | The latent→decoded tensor→pixel boundaries are distinct instruments. Decoder substitution is an efficiency/fidelity tradeoff, not generator equivalence. |
| [[blog/2026-08-04-000320-how-we-built-a-logically-divided-image-generative-model|Logical decomposition and boundary interchange]] | Scheduler interchange passed across tested generations; raw conditioner and VAE swaps failed typed latent/context contracts; transformers share a role but not a plug-compatible ABI; the renderer is the cleanest shared boundary. | Executable compatibility and failure localization are measured. Semantic modularity and quality transfer are not established. |
| [[blog/2026-08-04-104147-the-scene-state-became-a-trainable-interface|Scene-state bridge]] | A typed carrier/codec/host bridge moved measured trajectories, but adversarial review found relation, color, target-window, and scorer confounds in the image battery. | Runtime state movement is real; typed semantic control and an independent scene computer remain open. |
| [[blog/2026-08-04-150000-one-character-five-worlds-flux|Character pinning]], [[blog/2026-08-04-203000-resume-at-k-for-a-diffusion-model-the-character-pinning-clock|resume-at-k]], and [[blog/2026-08-04-221500-the-ruler-was-scoring-the-background-character-pinning-remeasured|metric remeasurement]] | Sustained regional injection preserved more subject signal than whole-latent swapping in the tested panel; cheap-deep resume was about `7.99×` faster; reference-token attention was measurable but weaker than regional injection. | Small-panel editing trends with subject/scene metric confounds. No general identity or product recipe is certified. |
| [[../experiments/2026-08-04-231120-flux-residual-merge-debug/ANALYSIS|Residual-merge debugger]] | Control suffix replay through `norm1`, `conv1`, `norm2`, and `conv2` was exact; a one-pixel shortcut shift produced terminal L2 `207.13` and cosine `.92090`. | A typed VAE boundary can be replayed and perturbed. The residual block is not thereby an identity organ. |
| [[../experiments/2026-08-05-001500-flux-evidence-graph-donor-map/results/SAME_DEVICE_ANALYSIS|Same-device donor map and evidence graph]] | `283` intervention arms across seven residual blocks, including a complete `8×8` coarse spatial field. Alternate-seed donor effects were amplified about `6×` at `up_blocks.1`, `14–15×` at `up_blocks.2`, and `13×` at `up_blocks.3`, then attenuated to about `0.04×` by the decoder tail. | Convergent propagation trend with placement confound removed. Local norm expansion is not semantic amplification or necessity. |
| [[../experiments/2026-08-05-001500-flux-evidence-graph-donor-map/results/RESOLUTION_ANALYSIS|Native-1024 and latent-resize comparison]] | Native 1024 paired traces changed `0.8813/0.9143` of pixels in two seeds; late-cell source-to-prediction L2 was retained at only `0.0334×/0.0369×`. Bilinear latent resize versus native 1024 had mean absolute pixel difference `51.4251`; the operator itself took `0.255 s`. | A resolution/consumer boundary and debugging seam. Native 1024 is not an interpolated 512 trajectory. |
| [[../experiments/2026-08-05-flux-blind-circuit-probe/FLUX_BLIND_FINDINGS|Blind structural circuit probe]] | On the immutable donor map, all `283/283` nonzero source perturbations changed the output; the opaque pass found seven source groups, 24 observed stages, and a repeated late corridor ending at `unit.23`. | A repeatable output-connected envelope, not a unique semantic circuit; there were no silent arms to establish necessity. |
| [[../experiments/2026-08-05-context-extension-runtime-poc/results/ANALYSIS|Context extension and cross-session context]] | Manual-loop parity and context-tail error were `0.0`; valid/wrong-donor latent movement was `.80426925/.77342147`; cross-session bundle hash and tail exactness passed with no consumer reference prompts. | A bounded external-context transport mechanism. It is not a general semantic memory system. |
| [[../experiments/2026-08-05-flux-context-position-sweep/results/ANALYSIS|Context position/layout sweep]] and [[../experiments/2026-08-05-flux-mask-without-face/results/ANALYSIS|mask-without-face]] | Position arms moved the latent by `.7830–.8211`; recipient-native mask-only controls were silent at the operator level; donor/full-body arms moved `.7770–.8086`; no-person band reached `1.0449` movement. | Layout, donor, and mask controls are now separated. Repeat-run CUDA movement in the native-mask arms is not evidence of a mask effect. |

### Real-FLUX serving, replay, and SATURN/TITAN continuation

| Experiment / owner | Measurements retained | Current interpretation and boundary |
|---|---|---|
| [[../experiments/20260805-165513-klein4b-serving-sweep/results/ANALYSIS|Klein 4B serving sweep]] and [[../experiments/20260805-190748-klein4b-all-real-comparison/results/ANALYSIS|all-real comparison]] | At 32 branches, exact shared-prefix replay was `21.861 s` versus `33.428 s` independent (`1.529×`), reducing physical denoiser calls `256→163`. Stacked exact reached `1.549×` with `163` calls; fused B4 used `43` calls and reached `1.396×` but was batch-dependent. | Exact scalar replay is the current serving promotion candidate for branch panels. Fused batching is a throughput trend, not exact parity. |
| [[../experiments/20260805-174531-klein4b-exact-batched-vae/results/ANALYSIS|Exact denoise + batched VAE]] and [[../experiments/20260805-171746-klein4b-cosine-sweep/results/ANALYSIS|cosine sweep]] | B4 VAE decode was `1.542×` versus native, with raw cosine `.999998995–.999999021`, max mean RGB delta `.069`, and max changed fraction `6.93%`; it was not hash-identical. The measured phase/batch/compile/FP16 stack reached `9.964×` request and `5.416×` cold speedup with mean/min cosine `.993475/.980190` and `0/8` exact rows. | Exact denoiser authority and pixel parity remain separate from throughput. Compile warm median was `1.105×` but `0/3` exact; FP16 minimum cosine was `.9796`, so neither is promoted to the exact lane. |
| [[../experiments/20260805-branch-replay-runtime-fix/results/ANALYSIS|Checkpoint replay runtime fix]] and [[../experiments/20260805-branch-batched-debugger-real-benchmark/results/ANALYSIS|branch-batched debugger benchmark]] | Exact replay fixed scheduler `begin_index`, giving exact latent/control pixels and `1.512×` speedup; the fused four-row benchmark reduced calls `4→1` but was `0.903×` scalar speed and changed `33.55–52.47%` of channel values. | The explicit checkpoint ABI exposes the difference between scalar-authority replay and batch-dependent exploration. |
| [[../experiments/2026-08-05-191412-toy-circuit-rosetta/artifacts/diffusion-new-prompts-seeds/2026-08-06/REPORT|Tracer new prompts/seeds]] | Four lighthouse/tram × seed cases used 31 interventions each; donor-like branches were `22/31`, `18/31`, `24/31`, and `22/31`. `single.10` recurred as an image-stream candidate; cross-seed top-eight rank correlation was `.929`/`.533` by prompt family. | Repeated candidate route family, not a universal address or circuit. The fixed-token-position bug was corrected by deriving positions from each receipt. |
| [[../experiments/2026-08-05-191412-toy-circuit-rosetta/artifacts/diffusion-edge-mediation/2026-08-06/REPORT|Checkpointed edge mediation]] and [[../experiments/2026-08-05-191412-toy-circuit-rosetta/artifacts/diffusion-sequential-mediation/2026-08-06/REPORT|sequential mediation]] | Single-checkpoint `joint.2→joint.3` rescue fraction `.942`; sequential all-step text sufficiency was donor-like `4/4` with donor progress `.900`; all-step `joint.2` ablation→`joint.3` rescue had blue MAD `1.58` batched / `1.82` exact and rescue fraction `.974`; all no-op controls were image MAD `0.00`, return cosine `1.0000`. | Strong exploratory conditional-rescue and accumulation evidence for a `joint.2→joint.3` candidate. Exact edge specificity, redundancy outside the tested sites, and replication remain open. |
| [[../mstack/results/diffusion_image_token_address_klein4b.md|Image-token map]] and [[blog/2026-08-06-the-image-token-map-found-the-spatial-circuit|spatial-circuit report]] | Corrected native grid is `16×16` / 256 image tokens. Red→blue, fox→cat, and scene contrasts had mean field norms `61.98`, `79.37`, and `131.45`; top-20 support Jaccards were `.026`, `.053`, `.053`. The initial offline flow was `9.453015`, but its topology could not represent redundancy. | A distributed spatial carrier with an upper-left causal core and redundant envelope is the working inference; the graph is a search instrument, not a physical flow or causal proof. |
| [[blog/2026-08-06-tracer-found-an-action-circuit-not-the-color-relay|Action tracer]] | On paired seeds, `image.single.10` scored `.989/.985`; `image.single.0` `.966/.936`. `single.10` image distance to writing donor was `6.57/5.25` versus reading `60.02/34.03`; `single.19` was a latent false positive. | A task-distinct action/hand-object candidate family. Mediation, coalition, and region-specific scoring are still required. |
| [[blog/2026-08-06-saturn-native-debugger-first-circuit|SATURN native debugger]] | Native Klein 4B trace: 112 module events / trajectory, 28 boundaries × 4 steps, and 4 runtime events with 4 reads / 8 writes. Replay was exact at `joint.4` and image-stream output. Rescue fractions were `97.72%`, `97.03%`, and `93.12%` for successive candidate links. | Proves a replayable native boundary and a distributed time-expanded route under one paired prompt/seed. It does not yet align a student and teacher internal graph. |
| [[blog/2026-08-07-125447-saturn-mamba-rosetta|SATURN Mamba Rosetta]] | External `state-spaces/mamba-1.4b-hf` source produced `[B,512,2048]` CPU/FP32 states, which the same 14,966,272-parameter adapter translated to `[B,512,7680]` FLUX.2 `PromptEmbeds`. Native and Mamba rows shared substrate fingerprint `e11165d1…b31f6`; Mamba red/blue MAD was `26.9863` versus native `70.9545`, and mean direction cosine was `.0284`. | A controlled external-conditioner substitution crossed the typed interface and preserved the suffix runtime, but not semantic equivalence. The Mamba arm is a circuit-search specimen, not evidence that native BFL FLUX.2 uses Mamba. |
| [[blog/2026-08-06-titan-native-scheduler-bounded-acceptance|TITAN native scheduler]] | Four of four scheduler calls used the CUDA body; local formula parity was exact; final latent cosine `.9958787`; decoded image cosine `.9988290`; native scheduler time `.212 ms`; peak RSS/VRAM `17.9 GB/8.3 GB`. The later production trajectory used native routing for `504/504` scheduler calls. | Clears the interim `.997` returned-image bar for exploratory mixed execution. A non-contiguous `[1,256,128]` layout mismatch keeps exact frame certification open; this is not a speed or semantic promotion. |
| [[../saturn/experiments/2026-08-06-saturn-full-trajectory-student/report|SATURN full-trajectory student]] and [[../mrun/docs/evidence/2026-08-06-saturn-roadmap-execution|SATURN roadmap]] | Real FLUX latent student image cosine by cut averaged `.8496`, `.8665`, `.8832`, `.9132` (minimum `.7438`, `.7633`, `.7860`, `.8316`); overall mean/min `.8781/.7438`. A separate economics run measured `22.18–32.66×` end-to-end speedups with student cosine about `.921–.930`. | A teacher-trajectory student and serving experiment, not a replacement for the full transformer. Quality denominators and broader held-out acceptance remain open. |
| [[../saturn/results/real-edit-reuse.json|SATURN real edit reuse]] | Four image-conditioned edits reused one 256-token reference; native versus replay was exact `4/4`, mean cosine `1.0`, and cache-hit speedup median `4,696×` (`0.1741 s` miss vs `0.000037 s` hit). | Strong typed checkpoint/cache mechanics for the pinned model. It does not establish semantic identity quality or general edit superiority. |
| [[../saturn/experiments/2026-08-17-ship-the-hotfix/RESULTS.md|Ship the Hotfix preregistered ship-gate]] (2026-08-18) | A donor-free gated counting hotfix on distilled Klein 4B: sealed apple panel exact `23.3%→51.1%` (+27.8 pts, dual evaluators); resolution non-inferior at 256² and `+33 pts` at 1024²; family transfer `37%→72%`; zero-dose/uninstall/parity byte-exact; 6/6 donor-free fresh-process cells. Collateral gate **failed**: the binary detector fired on `58/120` open prompts (p95 RGB-MAD `41.5` vs `≤6.0`). Saturn post-mortem (`job-3e94680b28d5`): score-vs-style correlation `.928` vs score-vs-object-multiplicity `.029`; same-subject style swap flips fire/abstain; count and watercolor score bands overlap by construction — a style-label confound in the 23-state detector training set. | The repair class generalizes (paraphrase, resolution, family) and serves donor-free, but the hotfix does **not** ship: no 1-D threshold can pass collateral given the confound. Fix requirement: style-balanced negatives + two-feature abstain boundary validated on open prompts. See [[blog/2026-08-18-ship-the-hotfix-result|the result post]]. |

### External-conditioner Rosetta: Mamba versus native Qwen (2026-08-07)

The new [[blog/2026-08-07-125447-saturn-mamba-rosetta|SATURN Mamba Rosetta]]
run belongs in this wiki as a controlled FLUX.2 boundary experiment, with an
important scope distinction: **Mamba is an external conditioner used by the
experiment, not a component discovered inside native Black Forest Labs FLUX.2**.
The pinned native model remains Qwen-conditioned.

SATURN held the FLUX.2 Klein 4B transformer, scheduler, VAE, latent seed,
resolution, four-step recipe, and checkpoint/replay ABI fixed. Native Qwen
conditioning supplied the reference `PromptEmbeds`; `state-spaces/mamba-1.4b-hf`
was loaded on CPU/FP32 and verified at width `2048` and sequence length `512`.
The same 14,966,272-parameter, 700-step masked adapter translated Mamba states
to the `[512,7680]` FLUX.2 contract. Both arms exposed the same substrate
fingerprint, while Mamba's semantic behavior diverged.

| Measurement | Native Qwen | Mamba adapter | Reading |
|---|---:|---:|---|
| Red/blue RGB MAD | `70.9545` | `26.9863` | The foreign route carried less of the tested color contrast. |
| Held-out embedding cosine | — | red `.1948`, blue `.1952` | The target tensor was reached, but held-out alignment was weak. |
| Mean discriminating-direction cosine | — | `.0284` | Tested color/subject/scene directions were much less preserved than broad statistics. |
| Bounded max flow | `.9312` | `.5112` | The route remained measurable but weaker under the Mamba payload. |

The first held-out image made the boundary concrete: the native baseline followed
the lighthouse/storm prompt, while the Mamba image was clear but depicted a
different planter/sidewalk-like composition. Its flattened RGB cosine was
`.8103743`; that is a pixel statistic, not semantic agreement. The full artifact
pair and prompt are embedded in the linked blog, and the source result tree is
`../saturn/results/rosetta-cross-family-manalysis-mamba/`.

The Mamba lexical artifact is labeled with source positions and adapter output
slots. It is never relabeled as literal Qwen token identity. The spatial-support
artifact uses a `16×16` image-token grid grouped into `4×4` blocks; the top-five
subject and scene supports shared one block. These are search coordinates and
support observations, not standalone causal circuits.

The run lineage also retains three informative failures: missing Mamba asset on
the first preflight, a memory-guard kill during the first lexical reverse trace,
and an autograd-boundary failure in the first spatial run. The asset was acquired,
the lexical reservation was grown, and the spatial worker restored gradients
around adapter fitting. Each corrected result has its own receipt and MinIO/
MLflow publication; failed attempts are excluded from scientific claims.

This matters for the open BFL question because the foreign arm is a controlled
semantic perturbation over a fixed image program. Native-Qwen lexical traces can
nominate the reference route; Mamba traces show where translated source positions
and adapter slots weaken or reroute it; spatial support, checkpoint replay,
return-register/RGB dual scoring, tracer, MRI, and intervention panels can then
test whether a candidate survives at the intended consumer. The result supports a
circuit-search workflow and a useful semantic-mismatch specimen, not a universal
cross-family interchange theorem.

### Work deliberately retained as adjacent, proposed, or non-BFL evidence

| Work | Status and reason it is not promoted as BFL model evidence |
|---|---|
| [[experiments/post-flux-toy-research|Post-FLUX toy research]] | Completed synthetic organisms: attention `97.14%` versus about `60%` for the tested axial-state toy, sparse role anchors `98.18%`, and oracle dirty-region rendering `30.57×–1638.40×`. These calibrate instruments and generate hypotheses only. |
| [[experiments/diffract-diffusion-circuit-tracing|DifFRACT reference]] | External FLUX.1[schnell] method/case-study reference. Its transcoders and intervention controls are not local FLUX.2 measurements. |
| [[experiments/flux-causal-programs-cross-calibration|Cross-calibration contract]], [[experiments/model-understanding-discriminating-experiments|E11]], and [[flux-generation-by-design-proposal|FLUX Generation by Design]] | Proposed or queued contracts. They specify future controls, not additional executed results. |
| Qwen ScienceGraph/E1 and other language-model runs | Linked elsewhere only for boundary comparison. They are not BFL evidence and do not transfer a Qwen circuit claim into FLUX. |
| Native hierarchical/routed synthetic organism in the SATURN matrix | Measured native organism only: learned compact one-step route `4.951×` with PSNR `+0.004 dB`, cached edit wave `22.390×`; no decoded-RGB cosine was available. It is a runtime organism, not the BFL model. |

### What the ledger changes

The combined evidence supports three separate conclusions:

1. **Model conclusion:** seven pinned public BFL artifacts have measured custody, anatomy,
   trajectories, behavior surfaces, and release-specific adaptation trends.
2. **Mechanism conclusion:** Klein 4B has a terminal assay-relative distributed K/V route and a
   newer exploratory multi-step mediation trend; the spatial and action tracer work expands the
   candidate universe without closing necessity, specificity, or portability.
3. **Engineering conclusion:** exact checkpoint replay, typed context/cache reuse, native
   component replay, and phase-aware serving are real and measurable; batch-dependent numerical
   shortcuts, compiler/precision variants, student models, and decoder substitutions remain
   separately labeled.

No failed gate in this ledger is treated as proof that a mechanism is absent. The raw gate result,
trend interpretation, instrument limitation, and terminal-claim status remain separate.

## Experiment and source coverage audit (2026-08-06)

The vault-wide audit searched `obsidian/**/*.md` for BFL/FLUX source notes, experiment owners,
contracts, and proposals. The table below is the consolidation map. It keeps direct measurements,
working trends, external references, and future designs separate so that “captured in the wiki” does
not silently become “established as a terminal claim.”

| Source note | Role / status | What is now captured here |
|---|---|---|
| [[experiments/bfl-flux2-lineage-sweep|BFL FLUX.2 Lineage Sweep]] | Primary owner; measured with adjudication boundaries | The six-generator cohort plus Small Decoder boundary, custody, architecture, conditioner provenance, lineage, KV adaptation, Dev paging, recorder/readouts, behavior, H5–H9 route, and decoder evidence. |
| [[experiments/bfl-frontier-program-2026-07-31|BFL Frontier Program]] | Six-track program; mixed measured, queued, and gated work | T1 lineage, T2 counting, T3 base/distilled forensics, T4 KV delta, T5 weights-to-ports, and T6 typography are represented in the lineage/behavior/open-program sections with their current gates. |
| [[experiments/flux-causal-programs-cross-calibration|FLUX Causal Programs Cross-Calibration]] | Proposed contract over measured artifacts | Behavior-first counting/typography and weight-statics nomination remain independent programs. The shared-controls panel is proposed; it authored no run and changed no artifact. |
| [[experiments/flux-fnet-mamba-mechanism-atlas|FLUX, FNet, and Mamba Mechanism Atlas]] | Historical FLUX.1/cross-architecture atlas; measured-bounded | FLUX.1 Schnell static anatomy and the original FLUX.2 authorization boundary are retained as historical evidence. Later access and live FLUX.2 results are owned by the lineage sweep; the old 403 is not current status. |
| [[experiments/post-flux-toy-research|Post-FLUX Toy Research]] | Completed synthetic mechanism study; adjacent, not BFL evidence | Attention beat the tested axial state toy (`97.14%` versus about `60%`), recurrent trajectory state failed its quality test, sparse role anchors reached `98.18%`, and oracle dirty-region rendering reduced pixel work by `30.57×–1638.40×`. These motivate design hypotheses only. |
| [[experiments/diffract-diffusion-circuit-tracing|DifFRACT diffusion circuit tracing reference]] | External FLUX.1[schnell] method reference | Timestep-conditioned transcoders, stream-aware attribution, conservation, reconstruction, and intervention controls are recorded as a comparison instrument. External case studies are not merged into FLUX.2 evidence. |
| [[experiments/model-understanding-discriminating-experiments|Model Understanding Discriminating Experiments — E11]] | Proposed next FLUX test; no result | The block-13 carrier-closure design is listed as open: native deletion/rescue, external K/V graft, wrong-world/wrong-role controls, continuous margin, exact witness, and collateral guards. |
| [[flux-generation-by-design-proposal|FLUX Generation by Design]] | Forecast and design proposal; not a BFL observation | The measured grammar—outsource, rebuild/rotate, preserve interfaces while adapting—and the proposed `flux-i1/i2`, `flux-10x`, and `flux-100x` gates are future-facing. FG-G0’s forecast registry is frozen; later design gates remain proposed/drafted. |
| [[../experiments/2026-08-05-001500-flux-evidence-graph-donor-map/README|Evidence graph and same-device donor map]] | Completed exploratory debugger owner | The 283-arm same-device VAE donor matrix, native-1024 versus latent-resize trace, consumer amplification, and opaque blind-circuit pass are consolidated in the ledger above. |
| [[../experiments/2026-08-05-context-extension-runtime-poc/README|Context extension runtime PoC]] plus [[../experiments/2026-08-05-flux-context-position-sweep/README|position sweep]] and [[../experiments/2026-08-05-flux-mask-without-face/README|mask ablation]] | Completed bounded runtime/context work | Exact context transport, cross-session bundle custody, position/layout movement, and native-mask null controls are measured; no general semantic memory or identity claim is promoted. |
| [[../experiments/20260805-165513-klein4b-serving-sweep/README|Klein serving sweep]], [[../experiments/20260805-173337-klein4b-stacked-serving/README|stacked serving]], [[../experiments/20260805-174531-klein4b-exact-batched-vae/README|exact denoise + batched VAE]], and [[../experiments/20260805-190748-klein4b-all-real-comparison/README|all-real comparison]] | Completed real-FLUX runtime comparison | Exact replay, fused branch batching, VAE batching, cosine, compile, FP16, and full-stack speed/parity measurements are included with their separate numerical contracts. |
| [[../experiments/20260805-branch-replay-runtime-fix/README|Branch replay runtime fix]], [[../experiments/20260805-branch-batched-debugger-proof/README|branch-batched proof]], and [[../experiments/20260805-branch-batched-debugger-real-benchmark/README|real branch benchmark]] | Completed runtime repair and benchmark work | Scheduler resume identity, exact scalar replay, branch batching, physical-call reduction, drift, and memory measurements are retained; fused replay is not treated as scalar-equivalent. |
| [[../experiments/20260805-215201-titan/README|TITAN]] and [[../saturn/experiments/2026-08-06-saturn-full-trajectory-student/report|SATURN roadmap]] | Active runtime/student continuation | Named Frame/Act execution, native scheduler acceptance, real-FLUX student trajectories, cached edits, and SATURN circuit/debugger work are measured in the 2026-08-06 section; semantic and exact-frame gates remain open where stated. |

Two search hits are deliberately not promoted as additional BFL experiments: the general
[[experiments/generator-relative-operation-atlas|Generator-Relative Operation Atlas]] only links
FLUX as cross-architecture context, and `scale-panel-reaudit.md` matched `bfloat16` text rather
than Black Forest Labs. The general E11–E14 plan is likewise not a second result source; only its
explicit FLUX E11 section belongs in this ledger.

## Recent component, boundary, and editing work (2026-08-03–2026-08-06)

The 2026-08-03–08-04 notes extend the BFL program from model-family comparison into typed runtime
boundaries and controlled editing. They are captured here as trends, not as proof of independent
semantic modules:

| Work | Observation / trend | Boundary |
|---|---|---|
| [[blog/2026-08-04-000320-how-we-built-a-logically-divided-image-generative-model|Logical model decomposition]] and [[blog/2026-08-04-000001-a-flux1-host-with-flux2-organs|FLUX.1 host with FLUX.2 organs]] | The scheduler is directly interchangeable across generations; raw conditioner and VAE swaps fail at typed latent/context contracts; the transformers share a role but not a plug-compatible interface; the renderer is the cleanest shared boundary. | Executable compatibility and boundary diagnosis are not semantic modularity or a quality comparison. |
| [[blog/2026-08-04-104147-the-scene-state-became-a-trainable-interface|Scene State became a trainable interface]] and [[blog/2026-08-04-112441-where-we-are-with-the-disassembled-image-model|current disassembled-image status]] | A typed carrier, codec, and host bridge can be trained and can move measured trajectories; adversarial review found relation, color, target-window, and scorer confounds in the first image battery. | No typed semantic control, independent scene computer, or causal field ownership is established. |
| [[blog/2026-08-04-150000-one-character-five-worlds-flux|Character pinning in FLUX]], [[blog/2026-08-04-203000-resume-at-k-for-a-diffusion-model-the-character-pinning-clock|resume-at-k clock]], and [[blog/2026-08-04-221500-the-ruler-was-scoring-the-background-character-pinning-remeasured|metric remeasurement]] | On Klein 4B, sustained regional injection preserves subject identity while retaining more scene context than whole-latent swapping; the whole-image identity gap was largely a background/layout metric artifact; cheap-deep resume measured about `7.99×` speedup; reference-token attention is real but dominated by regional injection in the tested panel. | These are two-scene/small-panel editing trends, not a general identity, quality, or product recipe. |
| [[blog/2026-08-04-182551-from-the-plane-to-a-debuggable-model|From the Plane to a Debuggable Model]], [[blog/2026-08-04-220500-the-boundary-became-a-debugger|Boundary Became a Debugger]], and [[tools/generative-model-debugger|Generative Model Debugger]] | Recipient-aware reference swaps, no-op and wrong-donor controls, component IO, residual-merge replay, and consumer traces expose where VAE/decoder deltas propagate and amplify. | The debugger establishes local execution and propagation facts, not a native identity circuit, semantic ownership, or CPU/CUDA equivalence. |
| [[blog/2026-08-06-can-we-find-causal-circuits-in-diffusion-models|Tracer and sequential mediation]], [[blog/2026-08-06-the-image-token-map-found-the-spatial-circuit|image-token map]], and [[blog/2026-08-06-tracer-found-an-action-circuit-not-the-color-relay|action tracer]] | New-prompt/seed intervention screens, checkpointed edge mediation, a corrected `16×16` spatial map, and a task-distinct action route now expose repeated candidate families. All-step text transfer is donor-like `4/4`; `joint.2→joint.3` rescue is `.974`; `single.10` action scores are `.989/.985` across paired seeds. | These are exploratory real-FLUX observations and working inferences. They need coalition, mediation, necessity, and held-out replication before circuit language becomes terminal. |
| [[blog/2026-08-06-saturn-native-debugger-first-circuit|SATURN native debugger]] and [[blog/2026-08-06-the-saturn-project|SATURN program runtime]] | Native `joint.4` execution is replayable exactly; the time-expanded route is visible through typed frames, runtime traces, checkpoint branches, and decoded RGB. Real-FLUX serving stacks reach up to `9.964×` request speedup, while the exact lane remains separate. | The model can be instrumented as a program-shaped runtime. This does not show that BFL trained a typed software pipeline or that a student replaces the dense transformer. |
| [[blog/2026-08-06-titan-native-scheduler-bounded-acceptance|TITAN native scheduler]] | Four native scheduler calls were formula-exact; decoded-image cosine `.9988290` cleared the interim `.997` exploratory bar; the production trajectory used native routing `504/504` times. | Layout preservation and exact frame parity remain open; the result is a bounded engineering acceptance, not a semantic or performance claim. |
| [[blog/2026-08-06-titan-frames-acts-physical-binaries|Titan: Frames, Acts, and Physical Binaries]] | The pinned FLUX.2 Klein 4B path now emits named Frame/Act transitions. A Beast run used native scheduler, VAE-normalization, and VAE-unpatchify acts with an exact final image against scalar Python authority; a separate C-ABI package proves those pure acts and frame metadata can load without Python/Torch. | This is a runtime and packaging result over the pinned public artifact. It does not establish that BFL’s model is semantically decomposed, that the dense transformer is native, or that Titan is a standalone generator. |

## Open BFL program

1. Complete the frozen H9 six-contrast cluster adjudication; only then generalize across new
   workloads, lexicalizations, spatial selectors, resolutions, seeds,
   Klein 9B, 9B-KV, base 4B, and Dev.
2. Complete the base↔distilled forensics as a cross-trajectory account of which readouts relocate, survive, or disappear under 50→4-step distillation.
3. Run the typography causal ladder only after the Wilson-gated behavior substrate and sealed custody report admit it.
4. Extend the conditioner result beyond sampled embeddings to full-shard identity and direct downstream mediation into denoiser ports.
5. Resolve the KV delta interpretation with matched reference tasks, cache ablations, and broader speed/quality sweeps.
6. Re-run the weight-statistics→ports question with a better-conditioned, prospective predictor and independent model/workload holdout.
7. Build a complete prompt → conditioner reconstruction → denoiser K/Q/V route → latent → VAE/pixel evidence chain without promoting any link beyond its own gates.
8. Run the proposed E11 block-13 carrier-closure panel with native deletion/rescue and external-graft controls; keep native necessity, external restoration, and endpoint sufficiency separate.
9. Continue typed component interchange and character-pinning panels with exact boundary receipts, subject/scene-separated scorers, multiple seeds, and neighboring-component controls.
10. Score the frozen FLUX Generation by Design forecast registry on future releases; keep `flux-10x`/`flux-100x` design gates separate from claims about BFL releases.
11. Replicate the `joint.2→joint.3` sequential mediation route on held-out prompts/seeds and test whether the spatial image-token envelope contains a reproducible causal core.
12. Run action-specific coalition and mediation tests for `image.single.0` and `image.single.10`, with hand/object-region scoring separated from café/background preservation.
13. Align SATURN student targets to native denoiser actions, return registers, and selected image-token fields before comparing student and teacher mechanisms.
14. Preserve the exact scalar serving lane while separately measuring batch-dependent suffixes, VAE batching, compiler, precision, and native Frame/Act layout contracts.

## Navigation by question

| Question | Start here |
|---|---|
| What are the exact BFL subjects and artifacts? | [[experiments/bfl-flux2-lineage-sweep]], [[../gen-anal/image-atlas-nucleus-freeze.ifleUZ/BFL_FLUX2_REPORT|BFL_FLUX2_REPORT]] |
| Which public checkpoints do the conditioners come from? | [[blog/2026-07-31-145130-the-conditioners-were-stock-checkpoints]] |
| Did FLUX.2 inherit FLUX.1? | [[blog/2026-08-01-001500-opening-the-black-forest-what-six-parallel-tracks-taught-us-about-flux#T1|T1 lineage]], [[blog/2026-07-31-212627-what-we-know-about-the-black-forest-models-a-data-driven-report#Result 2 — no detectable residual-facing inheritance from the Schnell witness (measured, bounded)|bounded lineage result]] |
| What did KV finetuning change? | [[blog/2026-07-31-212627-what-we-know-about-the-black-forest-models-a-data-driven-report#Result 3 — What the KV finetune changed (measured)|KV delta map]] |
| What did step distillation change? | [[blog/2026-08-01-001500-opening-the-black-forest-what-six-parallel-tracks-taught-us-about-flux#T3 — What does step-distillation do to representations?|distillation forensics]] |
| What is the strongest causal result? | [[blog/2026-08-01-h9-native-specificity-replication]], [[blog/2026-08-01-h8-temporal-route-localization]], [[blog/2026-08-01-h7-heldout-quotient-replication]] |
| Why does FLUX.2 bind colors better than Schnell in the measured assay? | [[blog/2026-08-01-conditioner-cartography-reconstruction-bottleneck]] |
| What are the counting and typography failure modes? | [[blog/2026-07-31-212627-what-we-know-about-the-black-forest-models-a-data-driven-report#Result 5 — The counting circuit demoted itself, correctly (adjudicated)|counting]], [[blog/2026-07-31-212627-what-we-know-about-the-black-forest-models-a-data-driven-report#Result 6 — The typography behavior atlas (measured tonight; sealed-report verification agent-pending)|typography]] |
| What transfers across FLUX.1/FLUX.2 component boundaries? | [[blog/2026-08-04-000320-how-we-built-a-logically-divided-image-generative-model]], [[blog/2026-08-04-000001-a-flux1-host-with-flux2-organs]] |
| Can reference identity be retained without copying the whole scene? | [[blog/2026-08-04-221500-the-ruler-was-scoring-the-background-character-pinning-remeasured]], [[blog/2026-08-04-203000-resume-at-k-for-a-diffusion-model-the-character-pinning-clock]] |
| Which nearby sources are not BFL evidence? | [[experiments/post-flux-toy-research]], [[experiments/diffract-diffusion-circuit-tracing]], [[flux-generation-by-design-proposal]] |
| How do the large models run? | [[experiments/bfl-flux2-lineage-sweep]], [[../mrun/README|mrun]], [[../mrun/docs/WORKPLAN|mrun workplan]] |
| What is still proposed or queued? | [[experiments/bfl-frontier-program-2026-07-31]], [[flux-generation-by-design-proposal]] |

## Source anchors and precedence

- [[../gen-anal/image-atlas-nucleus-freeze.ifleUZ/BFL_FLUX2_REPORT|BFL_FLUX2_REPORT.md]]
- [[../experiments/2026-07-24-generative-image-model-atlas/BFL_FLUX2_REPORT|Current BFL FLUX.2 source report and custody audit]]
- [[../gen-anal/image-atlas-nucleus-freeze.ifleUZ/BFL_FLUX2_SWEEP|BFL_FLUX2_SWEEP.md]]
- [[../gen-anal/image-atlas-nucleus-freeze.ifleUZ/MECHANISM_AUDIT|Generative Image Mechanism Audit]]
- [[../gen-anal/image-atlas-nucleus-freeze.ifleUZ/FLUX2_KLEIN_CAUSAL_PROTOCOL|Klein causal protocol]]
- [[blog/2026-07-31-212627-what-we-know-about-the-black-forest-models-a-data-driven-report|Data-Driven BFL Report]]
- [[blog/2026-08-01-001500-opening-the-black-forest-what-six-parallel-tracks-taught-us-about-flux|Six-track synthesis]]
- [[blog/2026-08-01-040000-inside-the-flux-arbitration-harness|FLUX arbitration harness]]
- [[blog/2026-08-01-black-forest-labs-model-analysis-capabilities-report|Shareable BFL capabilities report]]
- [[blog/2026-08-01-h9-native-specificity-replication|H9 adversarial correction and repair]]
- [[blog/2026-07-31-145130-the-conditioners-were-stock-checkpoints|Conditioner provenance]]
- [[experiments/bfl-flux2-lineage-sweep|BFL lineage owner]]
- [[experiments/bfl-frontier-program-2026-07-31|BFL frontier owner]]
- [[experiments/flux-causal-programs-cross-calibration|FLUX causal cross-calibration contract]]
- [[experiments/flux-fnet-mamba-mechanism-atlas|Historical FLUX/FNet/Mamba atlas]]
- [[experiments/post-flux-toy-research|Post-FLUX toy mechanism study]]
- [[experiments/diffract-diffusion-circuit-tracing|External DifFRACT reference]]
- [[experiments/model-understanding-discriminating-experiments|E11 FLUX carrier-chain proposal]]
- [[flux-generation-by-design-proposal|FLUX generation-by-design proposal]]

When summaries disagree, use the latest verified artifact/adjudication, then the current owner
note, then historical blog prose. Preserve superseded negative results: the old “no causal result
yet” language describes the pre-H9 state; H9 adds a bounded fixed-assay route and five-control
result without closing bilateral specificity or turning it into a universal mechanism.
