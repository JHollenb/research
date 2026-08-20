---
title: "FLUX.2 Dev Paged Execution at 512²"
type: experiment-report
status: guarded-one-step-runtime-proof
rank_in_bfl_survey: 16
model: "FLUX.2 Dev"
tags: [bfl, flux, dev, paging, memory, lifecycle, runtime, 512px]
---

# FLUX.2 Dev Paged Execution at 512²

> [!summary]
> A 112.805 GB BF16 FLUX.2 Dev artifact can execute a guarded one-step 512² forward and VAE decode by paging a 24.011B-parameter Mistral conditioner and a 32.223B-parameter denoiser with explicit lifetimes; they are never co-resident. All 11/11 lifecycle gates pass in approximately 336.41 seconds, and about 12.7 GB of swap is observed at completion. A richer worker-side four-step diagnostic reaches CLIP 0.360, count 0.833, and OCR character 0.472, but that diagnostic is unguarded and is not promoted to the terminal runtime claim.

## Research question

Can the full FLUX.2 Dev artifact run on a constrained host when the conditioner and denoiser are explicitly paged rather than held in memory together? The experiment targets a concrete runtime contract: load the conditioner, produce conditioning state, release it, load the denoiser, perform one 512² forward, release it, decode through the VAE, and verify lifecycle and output gates.

This is an execution and memory-boundary experiment, not a semantic capability benchmark. The primary proof is that the guarded runtime completes with the declared resource behavior. A separate richer diagnostic is retained because it is useful for exploration, but its metrics do not upgrade the one-step terminal claim.

## Artifact and memory plan

The BF16 artifact is 112.805 GB. The conditioner is a 24.011B-parameter Mistral component, and the denoiser is a 32.223B-parameter component. The runtime declares explicit object lifetimes so the conditioner and denoiser are never co-resident. Paging and swap telemetry are recorded at lifecycle boundaries rather than inferred from a final process statistic.

The one-step path uses 512×512 generation followed by VAE decode. The gates cover artifact availability, model load, conditioner execution, conditioner release, denoiser load, denoiser execution, denoiser release, VAE decode, output validity, swap telemetry, and completion receipt. A run passes only when all 11 gates are satisfied.

## Results

The guarded one-step runtime passes 11/11 lifecycle gates. Completion time is approximately 336.41 seconds. About 12.7 GB of swap is recorded at completion, providing direct evidence that the execution used the declared paging strategy. The result proves that this large artifact can cross the one-step 512² runtime boundary under the captured host and configuration.

The richer four-step worker-side diagnostic reports CLIP 0.360, count 0.833, and OCR character 0.472. These measurements show that the worker can produce a nontrivial image and support exploratory diagnostics, but they are explicitly unguarded. They do not establish a certified four-step quality contract, exact text rendering, or broad prompt capability.

[Runtime configuration and lifecycle evidence](../artifacts/flux2-dev-paged-execution/flux2-dev-concept-capture.json)

## Why paging is the result

For this artifact, memory orchestration is part of the scientific object. A successful output without lifecycle telemetry would not distinguish true sequential paging from accidental co-residency, host swapping at an uncontrolled point, or a smaller surrogate artifact. The explicit release gates and swap evidence make the runtime mechanism inspectable.

The result also identifies the practical tradeoff. Sequential paging makes the execution possible but costs approximately 336.41 seconds for one guarded 512² step. This is a feasibility proof and a baseline for future overlap, quantization, or host-placement work, not a throughput result.

## Controls and limitations

The 11 lifecycle gates control each resource phase separately. Explicit non-co-residency controls peak memory interpretation. Swap telemetry controls the claim that paging actually occurred. The artifact configuration binds the model sizes and 512² shape. The old failure-diagnosis record is retained in the bundle as a failure-boundary artifact and is not used as evidence that the runtime passed.

The terminal result is one-step, 512², and host/configuration specific. The richer four-step diagnostic is diagnostic-only. No claim is made about production throughput, multi-request serving, exact image quality, or successful execution on a different host without repeating the lifecycle evidence.

## Claim status

**Observation:** the 112.805 GB BF16 artifact completes a guarded one-step 512² forward and decode with sequential paging and observed swap.

**Convergent trend:** artifact sizes, explicit lifetimes, 11/11 gates, completion time, and swap telemetry agree on a real paged execution path.

**Working inference:** memory-lifetime orchestration is sufficient to make this otherwise oversized one-step consumer executable under the captured constraints.

**Terminal status:** guarded one-step runtime proof. The four-step quality diagnostic remains exploratory and does not extend the terminal claim.

## Local proof bundle

The bundle contains the runtime configuration, the failure-boundary diagnosis, the model-family runtime narrative, and the verifier:

- [runtime configuration](../artifacts/flux2-dev-paged-execution/flux2-dev-concept-capture.json)
- [runtime and memory evidence](../artifacts/flux2-dev-paged-execution/black-forest-labs-model-wiki.md)
- [runtime index](../artifacts/flux2-dev-paged-execution/dev-runtime-index.md)
- [failure-boundary artifact](../artifacts/flux2-dev-paged-execution/REPORT.md)
- [bundle verifier](../artifacts/flux2-dev-paged-execution/verify.py)

Run `python ../artifacts/flux2-dev-paged-execution/verify.py` from this directory to verify the artifact size, component sizes, lifecycle gate count, elapsed time, swap evidence, and diagnostic-only labeling.
