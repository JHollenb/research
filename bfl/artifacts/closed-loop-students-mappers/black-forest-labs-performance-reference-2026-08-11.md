---
title: "Black Forest Labs / FLUX Performance and Runtime Reference"
date: 2026-08-11
status: working-reference
claim_status: bounded-observations-with-explicit-baselines
scope: FLUX, SATURN, mrun, and related BFL model experiments
---

# Black Forest Labs / FLUX Performance and Runtime Reference

This is the performance and systems reference for the BFL/FLUX work. It is intentionally explicit about hardware, model, scope, baseline, parity, and whether a number is a complete image-generation result or only a latent/student-path measurement.

The most important rule is: **never combine these numbers into one speedup.** They measure different boundaries.

- Phase-resident serving changes execution around the unchanged FLUX model.
- Batched suffix and queue paths measure throughput and may be batch-dependent numerically.
- Learned students change the model and can be much faster, but they are not automatically exact replacements.
- mrun token-throughput numbers are useful evidence for aggregate serving, but they are not diffusion image-generation numbers.

## Hardware and primary model

Unless a row says otherwise, the real FLUX runs were executed on `beast`:

- Linux CUDA worker;
- AMD Ryzen 9 7950X;
- NVIDIA RTX 4080, 16 GB VRAM;
- approximately 64 GB system RAM;
- model weights under `/mnt/big/llm-models`;
- mrun-managed CUDA lease and telemetry.

The primary specimen is:

```text
black-forest-labs/FLUX.2-klein-4B
revision e7b7dc27f91deacad38e78976d1f2b499d76a294
pipeline Flux2KleinPipeline
dtype bfloat16
```

The main serving panels use 512×512 images, four denoising steps, guidance 1.0, and fixed prompts/seeds. The student validation panel uses 256×256 images and four steps unless noted.

## Performance summary

The table covers the BFL/FLUX/SATURN performance runs that are useful for explaining the project. “Baseline” always means the authority for that row, not necessarily the same authority as another row.

| Run | Hardware and workload | Baseline | Measured path | Result | Parity / quality boundary |
|---|---|---|---|---|---|
| Phase/program sequential | Beast RTX 4080; FLUX.2 Klein 4B; 512²; 4 steps; 8 images | `model_cpu_offload`; 52.651 s generation reference | Phase-resident scalar denoise | 4.872 s generation; 8.396 s end-to-end; 10.81× generation, 6.27× end-to-end | 8/8 pixel exact |
| Phase serving-max, B1 | Beast RTX 4080; same model; 512²; 4 steps; 8 images | Same-run `model_cpu_offload`; 57.273 s total | Phase-resident scalar B1 | 4.404 s generation; 8.636 s end-to-end; 13.00× generation, 6.63× end-to-end | 8/8 exact |
| Phase serving-max, B2 | Same | Same | Denoise batch 2; 4 physical calls | 4.600 s generation; 8.846 s end-to-end; 12.45× / 6.47× | 0/8 exact; max mean RGB error 3.89 |
| Phase serving-max, B4 | Same | Same | Denoise batch 4; 2 physical calls | 4.831 s generation; 10.746 s end-to-end; 11.85× / 5.33× | 0/8 exact; max mean RGB error 7.88 |
| Corrected factorial, phase/cache | Beast RTX 4080; 512²; 4 steps; eight fixed baseline images | CPU-offload BF16 authority | Phase residency and device cache | 5.59–5.60× request speedup | 8/8 exact; cache reduced transfers but did not materially change this small image’s latency |
| Corrected factorial, complete stack B2 | Same | Same | Phase + cache + batch 2 + FP16 + compile | 9.90× warm request speedup; 5.36× cold | Mean/min cosine 0.993475 / 0.980190; 0/8 exact |
| Checkpoint suffix reuse | Beast RTX 4080; FLUX.2 Klein 4B; four 512² images; 4-step path | Four scalar complete generations: 2.192 s | One shared checkpoint plus exact scalar suffixes | 1.450 s; approximately 1.51× over complete scalar calls | Control branch pixel exact; this is debugger reuse, not a new model |
| Checkpoint suffix fused | Same | Same | One checkpoint plus fused suffix | 1.580 s; approximately 1.39× over complete scalar calls | Batch-dependent; not the scalar authority |
| Terminal-specialist student | Beast CUDA lease; FLUX.2 Klein 4B teacher; 24 prompts, 12 train / 12 eval; 72 sequences; 144 eval transitions; 256²; 4 steps | Dense full-trajectory student/control | Batched student reference-rollout path | 3,552.9 student rollout images/s mean; 10.13 ms median | Not end-to-end image generation; VAE quality measured separately; standard free rollout cosine 0.873372 mean / 0.692964 min vs dense 0.878103 / 0.743759 |
| Large routed student microbenchmark | Beast CUDA; batch 6; latent denoiser suffix only | Native teacher suffix, 133.506 ms | Eager student 0.251 ms; compiled fixed-route student 0.149 ms | 23,950 / 40,334 latent-path images/s; compiled path ~897× lower latency | Omits VAE bridge and full service costs; not a production end-to-end speed claim |
| FLUX student plus real VAE | Beast CUDA; FLUX.2 Klein 4B; batches 1/2/4/8 | Native dense image path: 2.711 / 3.946 / 3.743 / 3.553 images/s | Student plus real Klein VAE: 88.529 / 87.520 / 82.946 / 80.257 images/s | 32.658× / 22.177× / 22.158× / 22.592× | Student/native cosine 0.920539 / 0.921034 / 0.928804 / 0.930156; bounded benchmark, not universal quality equivalence |
| Rollout-transition student | Beast CUDA; sequence-disjoint real FLUX states; batch 12; four-step latent path | Native teacher is the quality authority, not a matched end-to-end timing arm | 2.232 ms per 12-sequence four-step batch | 5,375 latent-path images/s; 21,501 transitions/s | Teacher-forced cosine 0.977279 / 0.828315; free-running 0.850788 / 0.778415; excludes VAE |
| MST-1 stateful student | Beast CUDA; 24 sequences; four-step latent path | Dense/control transition student | 4.844 ms per 24-sequence batch | 4,955 images/s; 19,818 transitions/s | Free standard cosine 0.852977 / 0.748230; exploratory, not promoted |
| MST-2 residual/state student | Beast CUDA; 24 sequences; four-step latent path | MST-1/control quality arm | 3.095 ms per 24-sequence batch | 7,754 images/s; 31,016 transitions/s | Free standard/reference cosine 0.842961 / 0.881249; typed step-kernel result, not an image-generator replacement |
| Native queue reference | Beast RTX 4080; native FLUX path; queue waves B1/B2/B4/B8 | Native dense/authority path | Queue-managed waves | 3.909 / 3.930 / 3.718 / 3.687 images/s | B1 exact; batched rows are cosine-close but not pixel-exact; queue/throughput evidence |
| mrun causal-family batch | Beast CUDA; SmolLM2 causal search; 93 families × 2,048 held-out examples | Scalar oracle, 735.05 s | Row-batched mrun, 388.85 s; batch 256; 744 physical forwards/arm | 1.89× end-to-end | 1,024/1,024 embedded scalar parity; not FLUX image generation |

The most important correction is that **3,552.9 images/s is not a perfect-match number**. It is a learned student’s batched latent/reference-rollout throughput. The exact-match numbers belong to the phase-resident scalar serving lane and to specific native act replacements, not to the student.

## Phase-resident FLUX: what we changed and how it scaled

### The hardware constraint

FLUX.2 Klein-4B in BF16 is too large to keep fully resident on a 16 GB RTX 4080. The approximate component sizes are:

- Qwen3-4B text encoder: about 8 GB;
- 3.876B-parameter denoiser: about 7.8 GB;
- VAE: about 84 MB;
- full resident BF16 pipeline: approximately 15.9 GB before working memory.

The ordinary `model_cpu_offload` path repeatedly moves the text encoder and denoiser across the CPU/GPU boundary. The phase experiment measured roughly 56 seconds per image pair in the earlier atlas workload, with about 12% GPU utilization; the cost was weight movement and coordination rather than arithmetic.

### The phase split

`mrun.diffusion.PhasePipeline` wraps an already-loaded CPU-resident Diffusers pipeline.

```text
encode phase:
  text encoder on CUDA
  denoiser + VAE on CPU
  encode each prompt once
  cache PromptEmbeds with exact dtype

denoise phase:
  text encoder detached/off card
  denoiser + VAE resident on CUDA
  generate repeatedly from cached embeddings
```

The full component transfer happens twice per job instead of twice per image. Prompt encoding remains serial because padding/batching changes the conditioning values. The cached embeddings preserve their original dtype; no silent BF16→FP32 round trip is allowed.

The serving path was measured on the Beast RTX 4080 with `black-forest-labs/FLUX.2-klein-4B`, BF16, 512×512, four steps, guidance 1.0, four prompts, and two seeds per prompt. The eight-image native `model_cpu_offload` run is the authority.

### Exact scalar lane

The first program/phase receipt measured:

| Path | Images | Physical calls | Generation | End-to-end | Output |
|---|---:|---:|---:|---:|---|
| `model_cpu_offload` | 8 | 8 | 52.651 s reference | reference | Authority |
| Phase/program sequential | 8 | 8 | 4.872 s | 8.396 s | 8/8 pixel exact |

The follow-on serving-max receipt used a 57.273-second same-run baseline and measured the scalar phase arm at 4.404 seconds generation and 8.636 seconds end-to-end. It reported 13.00× generation and 6.63× end-to-end speedup with 8/8 exact outputs.

The two receipts have different same-run setup and baseline timing, so the safe headline is **roughly 10.8–13× generation speedup and 6.3–6.6× end-to-end speedup on the exact scalar lane**, not one universal number.

### Batch scaling

The serving-max run kept the model resident through a denoise wave and reduced physical calls:

| Phase arm | Logical images | Physical calls | Generation | End-to-end | Generation speedup | Exact output |
|---|---:|---:|---:|---:|---:|---|
| B1 | 8 | 8 | 4.404 s | 8.636 s | 13.00× | 8/8 |
| B2 | 8 | 4 | 4.600 s | 8.846 s | 12.45× | 0/8; max mean RGB error 3.89 |
| B4 | 8 | 2 | 4.831 s | 10.746 s | 11.85× | 0/8; max mean RGB error 7.88 |

This is the important systems lesson: reducing physical calls did not improve per-image latency on this single RTX 4080 workload. The exact scalar lane is the numerical authority. B2/B4 are throughput observations with a separate batch-dependent contract.

### Other phase toggles

The corrected factorial tested phase residency, device-feed caching, batch size, FP16, and `torch.compile` against the same eight BF16 baseline images.

- Phase residency: 5.59× request speedup, 8/8 exact.
- Device cache: 5.60× request speedup, 8/8 exact. It reduced four device feeds to one and 30 MiB of transfer to 7.5 MiB, but did not materially change latency at this image size.
- Batch 2: 5.44×, mean/min cosine 0.999465 / 0.998270, 0/8 exact.
- FP16: 5.80×, mean/min cosine 0.993515 / 0.979631, 0/8 exact. It did not reduce peak VRAM enough to justify the numerical drift.
- `torch.compile`: 9.39× warm / 5.44× cold in the factorial, but it was not pixel-exact and is not promoted for the exact lane.
- Complete stack, B2: 9.90× warm / 5.36× cold, mean/min cosine 0.993475 / 0.980190, 0/8 exact.

The phase result is therefore primarily a **residency and scheduling optimization**, not a learned-model optimization.

Sources: [phase-CUDA design and API](/Users/jakeholl/domains/mrun/docs/DIFFUSERS-PHASE-CUDA.md), [serving-max evidence](/Users/jakeholl/domains/mrun/docs/evidence/2026-08-05-flux-serving-max-summary.json), [phase/program report](/Users/jakeholl/domains/obsidian/blog/2026-08-05-the-model-stayed-the-same-flux-got-10x-faster.md), and [corrected factorial report](/Users/jakeholl/domains/obsidian/blog/2026-08-05-the-model-stayed-the-same-flux-got-10x-faster.md).

## The 3,552.9 images/s student experiment

### Setup

This was not a full native FLUX serving benchmark. It was a learned closed-loop student experiment on a real FLUX.2 Klein-4B teacher.

- Hardware: Beast CUDA lease, RTX 4080-class worker.
- Teacher: real FLUX.2 Klein-4B.
- Resolution: 256×256.
- Schedule: four denoising steps.
- Prompts: 24 total; 12 training and 12 prompt-disjoint evaluation prompts.
- Image seeds: 81101, 81202, 81303.
- Student seeds: 202601, 202602, 202603.
- Sequences: 72 reference/edit sequences; 36 train and 36 evaluation.
- Evaluation transitions: 144.
- mrun execution: one guarded CUDA lease, one model load, no per-branch mrun submissions; peak VRAM about 8,908 MB and peak RSS about 27,982 MB.

### Student architecture and operation

The student was a `HybridReferenceRegisterStudent` with:

- a dense latent transition backbone;
- a typed reference register;
- a learned uncertainty head for sparse correction regions;
- banked correction state;
- a terminal specialist at the final transition.

Its closed-loop path was:

```text
typed latent state + conditioning + reference register
  → student action/state prediction
  → real scheduler transition
  → next student state
  → repeat for four steps
  → VAE decode
  → RGB
```

The student was fed its own predicted state on subsequent steps. It was not given the teacher’s next latent during free rollout. That makes it a real closed-loop transition experiment rather than teacher-forced tensor emission.

### What the 3,552.9 number means

The measured figure was:

```text
3,552.9 student rollout images/s mean
10.13 ms median rollout
```

It measured the batched student/reference-rollout path. It did **not** include a complete native FLUX call, and VAE/image quality was evaluated separately. “Images” here means student rollout rows, not necessarily fully decoded production images with all conditioning, VAE, service, and queue costs charged.

### Did it match the baseline 100% of the time?

No.

The student was near parity on average in the standard free-rollout panel, but it was not pixel-exact and its worst cases drifted:

| Quality metric | Student | Dense/control baseline |
|---|---:|---:|
| Standard free-rollout mean cosine | 0.873372 | 0.878103 |
| Standard free-rollout minimum cosine | 0.692964 | 0.743759 |
| Reference/edit free-rollout mean cosine | 0.960046 | 0.902797 older terminal baseline |
| Reference/edit free-rollout minimum cosine | 0.795940 | 0.831866 older terminal baseline |
| Reference teacher-forced mean cosine | 0.986923 | — |
| Student/reference aggregate cosine | 0.980590 | — |

The correct story is more interesting than “3,552 images/s at 100% parity”:

> A learned, scheduler-closed student reached 3,552.9 latent/reference rollouts per second in a bounded batch benchmark and achieved strong average alignment, while exposing a meaningful long-tail failure gap that Saturn can localize.

That is absolutely worth a blog post. The blog should make the distinction between throughput and exact replacement the central point. A good title would be **“3,552 Images per Second: What the Student Matched—and What It Didn’t.”**

Sources: [closed-loop student report](/Users/jakeholl/domains/obsidian/blog/2026-08-08-saturn-from-rosetta-to-a-closed-loop-student.md), [current Saturn student/performance reference](/Users/jakeholl/domains/saturn/README.md), and [scaled validation summary](/Users/jakeholl/domains/saturn/results/scaled-validation-job-4268d927765a2-summary.json).

## Student performance ladder

These are useful, but they must remain separate from phase-resident serving because they change the learned computation.

### Full student plus VAE

The registered 2,475,777-parameter student plus the real Klein VAE measured approximately 80–89 images/s in a bounded benchmark versus approximately 2.7–3.9 native images/s. The reported speedup range was 22.2×–32.7×.

The benchmark’s per-batch rows were:

| Batch | Native images/s | Student + VAE images/s | Speedup | Student/native cosine |
|---:|---:|---:|---:|---:|
| 1 | 2.711 | 88.529 | 32.658× | 0.920539 |
| 2 | 3.946 | 87.520 | 22.177× | 0.921034 |
| 4 | 3.743 | 82.946 | 22.158× | 0.928804 |
| 8 | 3.553 | 80.257 | 22.592× | 0.930156 |

Important caveat: the economics panel reused one captured input across some wider batch rows rather than exercising fully independent latent requests. The result is a bounded systems trend and must be rerun with independent prompts/latents before making a general production claim.

### Transition students

The rollout-transition student reached 5,375 latent-path images/s at batch 12, excluding VAE. Its free-running held-out mean/minimum cosine was 0.850788 / 0.778415. Teacher-forced quality was 0.977279 / 0.828315.

MST-1 reached 4,955 images/s at batch 24 and MST-2 reached 7,754 images/s at batch 24. These are typed transition-kernel measurements, not complete image-generation throughput. MST-2 is useful because it exposes an explicit action/state ABI, but its free quality remains below the dense/control authority.

## Aggregate serving and the Qwen mrun harness

### Existing aggregate mrun evidence

The Qwen-oriented mrun harness demonstrates a different but highly relevant serving property: aggregate throughput can rise dramatically as compatible requests share resident model work.

The relevant Qwen/OLMoE reference points include:

- Qwen2.5-0.5B: 57.80 tok/s at B1 to 29,793.59 aggregate tok/s at B1024, 515.49× aggregate scaling.
- OLMoE: 36.71 tok/s at B1 to 4,748.42 at B128 and 8,100.66 at B512, 220.66× aggregate scaling at B512.
- Fused OLMoE queue: 8,936.43 tok/s at B1024, 245.46× versus its paired B1, with approximately 10,180 MiB scheduler peak VRAM.

These are aggregate batch/service numbers, not single-request latency. They are also token-model results, not diffusion image-generation results.

The mrun causal-family batch experiment is a separate relevant systems result:

- 93 candidate families × 2,048 held-out examples = 190,464 rows per arm;
- row batch 256;
- 744 physical forwards per position arm;
- scalar oracle 735.05 s;
- row-batched 388.85 s;
- 1.89× end-to-end improvement;
- peak VRAM effectively flat at 2,586 versus 2,590 MB;
- 1,024/1,024 embedded scalar decisions matched;
- canonical scientific payloads were byte-identical after runtime fields were removed.

Source: [candidate-universe compiler results](/Users/jakeholl/domains/experiments/2026-07-30-104908-candidate-universe-compiler/RESULTS.md), [mrun throughput reference](/Users/jakeholl/domains/obsidian/blog/2026-07-19-from-fast-mamba-to-a-100x-model-runtime.md), and [mrun API throughput notes](/Users/jakeholl/domains/mrun/docs/API.md).

### Can we run the same idea for diffusion?

Yes, but the Qwen harness should be reused at the **admission, compatibility, queue, and telemetry layer**, not copied literally as a token engine.

Diffusion has no autoregressive token decode loop. The primary metrics should be:

```text
images/s = completed image rows / service wall time
denoiser transitions/s = images × denoising steps / denoise wall time
conditioning tokens/s = encoded conditioner tokens / encode wall time
queue p50/p95 and execution p50/p95
physical pipeline calls and physical denoiser calls
peak VRAM/RSS
RGB cosine, RGB MAD, changed-pixel fraction, and exact-output count
```

The proposed diffusion aggregate experiment is:

| Item | Proposed contract |
|---|---|
| Model | FLUX.2 Klein 4B, pinned revision above |
| Host | Beast RTX 4080, one mrun CUDA lease |
| Dtype | BF16 |
| Resolution | 512×512 |
| Schedule | Four steps, guidance 1.0 |
| Request set | 32–128 independent prompt/seed requests, with a repeated-prompt control |
| Batch waves | B1, B2, B4, B8, and the largest safe admitted batch |
| Baseline | Native `model_cpu_offload`, scalar requests |
| Exact candidate | Phase-resident scalar execution |
| Throughput candidates | Phase-resident denoise batches and compatible suffix waves |
| Primary outputs | images/s, denoiser transitions/s, queue latency, physical calls, VRAM |
| Fidelity outputs | per-image RGB hashes, cosine/MAD, exact count, semantic prompt checks |
| Required split | independent prompts/latents versus repeated prompt/conditioner reuse |

The existing `mrun.diffusion.PhasePipeline`, `generate_batch()`, `capture_checkpoint()`, `resume_checkpoint_batch()`, and `ContinuousBatchScheduler` already expose most of the needed shape. `ResidentCapturedBatchFamily/Service` is a reusable queue wrapper, but its current promoted template/executor is for Qwen selected-row CUDA work; it cannot be used unchanged for FLUX because the bindings, static shapes, scheduler state, and image outputs differ. The diffusion implementation should reuse the same admission/service contract with a PhasePipeline-compatible executor.

The first run should be a small informative matrix, not a production-scale sweep. It should establish whether batching helps after the model is phase-resident, whether the VAE becomes the bottleneck, and how much aggregate throughput is purchased by a small numerical drift. Only after that should we add queue delay, request refill, cancellation, and larger waves.

Status: the scalar and small-batch phase measurements already exist; the Qwen-style continuous request/aggregate diffusion service has not yet been run as a separate promoted experiment.

## Other relevant BFL experiments

### Model profiles and observatory

- [Black Forest Labs model wiki](/Users/jakeholl/domains/obsidian/black-forest-labs-model-wiki.md)
- [BFL overview](/Users/jakeholl/domains/obsidian/bfl-overview.md)
- [BFL tracer card index](/Users/jakeholl/domains/obsidian/experiments/bfl-tracer-2026-08-06/README.md)
- [FLUX.1 Schnell card](/Users/jakeholl/domains/obsidian/experiments/bfl-tracer-2026-08-06/flux1-schnell.md)
- [FLUX.2 Klein base 4B card](/Users/jakeholl/domains/obsidian/experiments/bfl-tracer-2026-08-06/flux2-klein-base-4b.md)
- [FLUX.2 Klein 4B card](/Users/jakeholl/domains/obsidian/experiments/bfl-tracer-2026-08-06/flux2-klein-4b.md)
- [FLUX.2 Klein 9B card](/Users/jakeholl/domains/obsidian/experiments/bfl-tracer-2026-08-06/flux2-klein-9b.md)
- [FLUX.2 Klein 9B-KV card](/Users/jakeholl/domains/obsidian/experiments/bfl-tracer-2026-08-06/flux2-klein-9b-kv.md)
- [FLUX.2 Dev card](/Users/jakeholl/domains/obsidian/experiments/bfl-tracer-2026-08-06/flux2-dev.md)
- [FLUX.2 Small Decoder card](/Users/jakeholl/domains/obsidian/experiments/bfl-tracer-2026-08-06/flux2-small-decoder.md)

### Circuits and conditioners

- [Certified semantic circuits in FLUX.2](/Users/jakeholl/domains/obsidian/whitepapers/certified-semantic-circuits-flux2.md)
- [The first Saturn circuit certificate](/Users/jakeholl/domains/obsidian/blog/2026-08-10-saturn-causal-circuit-certificate.md)
- [Distributed semantic carrier](/Users/jakeholl/domains/obsidian/blog/2026-08-10-saturn-the-semantic-function-was-a-distributed-carrier.md)
- [Mamba Rosetta](/Users/jakeholl/domains/obsidian/blog/2026-08-07-125447-saturn-mamba-rosetta.md)
- [Cross-family closed-loop student](/Users/jakeholl/domains/obsidian/blog/2026-08-08-saturn-from-rosetta-to-a-closed-loop-student.md)

### Debugger, training, and model-as-software

- [Running Saturn as a checkpointed debugger](/Users/jakeholl/domains/obsidian/blog/2026-08-07-running-saturn-as-a-checkpointed-debugger.md)
- [Saturn circuits, tools, and I/O](/Users/jakeholl/domains/obsidian/blog/2026-08-11-saturn-circuits-tools-and-io.md)
- [Saturn learned to train like a software system](/Users/jakeholl/domains/obsidian/blog/2026-08-11-150313-saturn-learned-to-train-like-a-software-system.md)
- [The scene state became a trainable interface](/Users/jakeholl/domains/obsidian/blog/2026-08-04-104147-the-scene-state-became-a-trainable-interface.md)
- [Project TITAN: frames and acts](/Users/jakeholl/domains/obsidian/blog/2026-08-06-project-titan-frames-acts.md)
- [The model became a program](/Users/jakeholl/domains/obsidian/blog/2026-08-06-the-model-became-a-program-saturn-stack.md)

### Snake and failure diagnosis

- [Semantic circuit from prompt to geometry](/Users/jakeholl/domains/obsidian/blog/2026-08-10-saturn-semantic-circuit-from-prompt-to-geometry.md)
- [Snake geometry research artifact](/Users/jakeholl/domains/saturn/results/rosetta-snake-geometry-research-20260810.md)
- [The circuit outlives Saturn](/Users/jakeholl/domains/obsidian/blog/2026-08-11-the-circuit-outlives-saturn.md)

## Safe language for external conversations

Use:

- “phase-resident execution on an RTX 4080 reduced a fixed FLUX.2 serving workload by roughly an order of magnitude in the exact scalar lane”;
- “the batched lane reduced physical calls but had a separate numerical contract”;
- “a learned student reached 3,552.9 latent/reference rollouts per second with strong average alignment, but it was not pixel-exact”;
- “mrun has demonstrated large aggregate request scaling on token models, and the next diffusion experiment will measure images/s and denoiser transitions/s under the same queue principles.”

Avoid:

- “3,552 images/s with 100% baseline parity”;
- “95% of the I/O was exactly the same”;
- “we fixed the snake problem”;
- “FLUX 3 uses Mamba”;
- “mrun’s 515× token scaling means 515× faster single-request inference”;
- any student-plus-VAE number without naming the independent-latent and VAE scope.
