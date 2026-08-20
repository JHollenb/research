---
title: "Exact Phase-Resident Serving, Replay, and Edit Caching Across FLUX"
type: experiment-report
status: bounded-terminal-engineering-result-with-recorded-boundary
rank_in_bfl_survey: 2
model_scope: "FLUX.2 Klein 4B, Klein base-4B, Klein 9B, Klein 9B-KV, and FLUX.1 Schnell"
model_ids:
  - "black-forest-labs/FLUX.2-klein-4B"
  - "black-forest-labs/FLUX.2-klein-base-4B"
  - "black-forest-labs/FLUX.2-klein-9B"
  - "black-forest-labs/FLUX.2-klein-9b-kv"
  - "black-forest-labs/FLUX.1-schnell"
revisions:
  flux2_klein_4b: "e7b7dc27f91deacad38e78976d1f2b499d76a294"
  flux2_klein_base_4b: "a3b4f4849157f664bdbc776fd7453c2783562f4d"
  flux2_klein_9b: "92196c8e11f7b6cf2b7493e037d8c5345c559216"
  flux2_klein_9b_kv: "a6dfb36eca3a3906eb2fd460795adfb844e5fcce"
  flux1_schnell: "741f7c3ce8b383c54771c7003378a50191e9efe9"
checkpoint_role: "native FLUX generators used to test execution-contract portability and pipeline-local ABI boundaries"
backend: "CUDA on Beast RTX 4080, mrun single lease per specimen set, strict preflight, no retries"
consumer: "native FLUX denoiser, scheduler, VAE, reference-conditioning path, and decoded RGB/PNG output"
tags: [bfl, flux, flux1, flux2, serving, exact-parity, replay, caching, edit-reuse, cross-model, inference-efficiency, runtime-abi]
---

# Exact Phase-Resident Serving, Replay, and Edit Caching Across FLUX

> [!summary] Two execution boundaries crossed the FLUX family on 2026-08-19. The encode→denoise phase boundary produced bitwise-identical pixels and PNGs across the declared resident and sequential lanes, covering Klein 4B/base-4B/9B, FLUX.1 Schnell, and the fp8-sequential 9B-KV prompt-only cell. The reference-edit cache replicated its 4,696× lookup result on plain Klein 4B, base-4B, and 9B, but stopped at the 9B-KV pipeline because its native reference/KV attention and token ordering require a different trajectory ABI. A faster fp8-resident 9B hybrid is useful but non-bitwise, so it is a separate throughput contract. Exactness belongs to the full declared state and pipeline semantics, not to a vague “same model” label.

## Research question

Can Saturn reduce repeated FLUX serving work without changing the native computation, and do the resulting state contracts survive checkpoint, pipeline, conditioner, memory-lane, and storage-dtype changes?

The experiment separates three mechanisms:

1. **Phase residency:** encode each prompt once, detach and cache the conditioner state, release the encoder, and generate the panel from a resident denoiser/VAE phase when the card permits it.
2. **Deep replay:** retain an exact entering cut and execute only the unchanged denoising suffix.
3. **Reference-edit caching:** retain the exact reference-conditioned state needed by repeated image edits, replay each edit suffix, and invalidate the cache when the reference identity changes.

The acceptance criterion is exact native-consumer parity: pixel bytes and encoded PNG bytes must match the model’s own offload reference. A cache hit must also return the same checkpoint fingerprint and pass dependency invalidation. A speedup without those identity controls is telemetry, not an exact-serving result.

## Shared execution contract

The parity panel uses four prompts, two seeds (`101`, `202`), 512×512 output, four denoising steps, fresh CPU generators per image, and identical VAE memory controls within each cell. The reference arm uses the model’s ordinary offload schedule; the candidate changes only the encode/denoise residency boundary. The edit-reuse panel uses one reference image from the cell’s own model, four real edits, seed `92001`, 256×256 output, four steps, and a saved cut at step 2.

The phase split is:

```text
encode phase:
    encoder resident → encode each prompt once → exact-dtype state on CPU/cache

denoise phase:
    encoder detached → denoiser + VAE resident or externally streamed → native suffix
```

No weights, scheduler equations, latent initialization, VAE decode operation, or edit prompt is changed by the phase-resident candidate. The reusable state contract includes model revision, conditioner state and dtype, scheduler cursor, latent IDs, resolution, random-number handling, reference identity, and the pipeline-specific trajectory ABI.

## Boundary 1: phase parity crossed the tested FLUX family

The cross-model phase panel covered two pipeline classes, two conditioner ABIs, resident and sequential memory lanes, and BF16 plus fp8-e4m3 storage with BF16 compute. The source analysis records 64/64 candidate images bitwise identical to their offload-reference twins across the full exact panel; the table below shows the principal and fast-substrate cells.

| cell | lane | pixel/PNG parity | per-image speedup | end-to-end speedup | reading |
|---|---|---:|---:|---:|---|
| klein-4B, same-day control | resident BF16 | 8/8 exact | 12.73× | 7.02× | resident phase split works |
| klein-base-4B | resident BF16 | 8/8 exact | 12.38× | 7.19× | new checkpoint, same ABI |
| klein-9B | BF16 sequential | 8/8 exact | 1.18× | 1.06× | only encoder streaming is removed |
| FLUX.1 Schnell | fp8-e4m3 + sequential | 8/8 exact | 1.43× | 1.36× | T5 + pooled-CLIP conditioner boundary holds |
| klein-9B fp8-seq | fp8-e4m3 + BF16, streamed | 8/8 exact | 1.18× | 1.06× | parity stable; speed varies by session |
| klein-9B-KV fp8-seq | fp8-e4m3 + BF16, streamed | 8/8 exact | 2.49× | 2.24× | prompt-only KV cell now has parity |
| klein-9B fp8-resident hybrid | fp8 denoiser resident, Qwen encoder streamed | 0/8 exact; median ΔRGB 4.6 | 6.40× | 4.36× | useful throughput contract, not parity |

Every exact cell records `encode_calls=4` and `unplanned_swaps=0`. Resident lanes remove per-image weight transfers and therefore show roughly 12× denoise-loop speedups. Sequential lanes still stream the oversized denoiser, so their 1.06–1.43× gains are encoder-stream removal only. Parity, not speed, is the portable claim.

The original Klein-4B receipt reported 10.66× per-image and 6.25× end-to-end speedups under its original benchmark denominator. The same-day cross-model control reports 12.73× and 7.02× under the expanded panel. These are different timing contracts; both are exact, and neither includes a separate circuit-tracer or MRI capture pass.

The 9B hybrid is intentionally separate. Keeping an fp8 denoiser resident while streaming the Qwen3-8B encoder reaches 1.51 s/image at 512² with a 9,961 MB VRAM peak, but resident and streamed materialization differ at BF16 accumulation level. Its median ΔRGB is 4.6, so it is a declared throughput contract rather than an exact-parity lane.

The phase boundary is therefore portable as an execution contract, not as one fixed placement schedule. When the card cannot hold the denoiser, the surviving exact contract is typed phase separation, exact-dtype conditioner custody, encoder detach, scheduler/RNG identity, and native suffix parity under external sequential placement.

## The phase instrument’s failure was recoverable evidence

The first sequential phase job rendered every declared image bitwise-exact, then crashed in post-render cleanup because `PhasePipeline.close()` called `module.to("cpu")` on a module whose placement was owned by accelerate and whose parameters were meta tensors between materializations. The surviving PNGs were rehashed, and the corrected specimen reran the sequential cells cleanly. The crash is a harness failure, not a parity failure; the null receipt remains part of the evidence trail.

The first fp8-resident hybrid probe similarly exposed a runtime seam: `DiffusionPipeline._execution_device` walked through the first unhooked component and resolved to the encoder’s meta device even though the denoiser was correctly resident on CUDA. Excluding resident components from that device walk fixed the mechanics. The substrate is useful, but its non-bitwise numerical contract remains explicit.

## Boundary 2: reference-edit caching crossed plain Klein, then met local KV semantics

The original edit-cache panel reused one 256-token reference across four real edits, replaying from a step-2 checkpoint. It passed 4/4 exact cells on Klein 4B with a median cache-hit lookup speedup of 4,696×. The cross-model panel repeated the same instrument:

| cell | lane | native↔replay exact | cache hits | invalidations | median hit speedup | full native/replay median |
|---|---|---:|---:|---:|---:|---:|
| klein-4B control | resident | 4/4 | 4/4 | 4 | 4,711× | 0.350 s / 0.175 s |
| klein-base-4B | resident | 4/4 | 4/4 | 4 | 5,039× | 0.350 s / 0.175 s |
| klein-9B | BF16 sequential | 4/4 | 4/4 | 4 | 57,324× | 5.43 s / 2.71 s |
| klein-9B-KV | BF16 sequential | 0/4 | 4/4 | 4 | 56,040× | 5.11 s / 2.70 s |

The plain Klein cells cross both checkpoint and memory lane. The 57,324× number is still a keyed reference-capture lookup, not a full render; the miss is more expensive because the streamed reference-conditioned prefix takes about 2.8 seconds while the hit remains roughly 50 microseconds. The full-continuation native/replay medians are the honest view of edit-time savings.

The 9B-KV cell is the useful boundary. Cache mechanics pass: hits return the identical checkpoint, fingerprints match, all four reference changes invalidate, and the reference token count is recorded. Replay is not exact: cosine remains ≥0.994 but mean ΔRGB is about 5–13. The reason is not a generic cache failure. The native KV loop orders tokens `[reference, target]`, gives reference tokens extract-mode causal self-only attention, and reuses cached K/V; the generic Flux2 capture ABI orders `[target, reference]` through the standard forward and uses a different decode signature. The KV pipeline needs its own trajectory ABI before native equivalence can be claimed.

This is the second boundary: the cache contract is portable across the plain-Klein execution surface, while the reference/KV pipeline has local attention and trajectory semantics. Shared checkpoint mechanics do not imply portable consumer semantics.

## Exact suffix replay

The deep-replay panel uses an eight-forward trajectory and saved cuts `k ∈ {1, 2, 3, 4, 6, 7}`. Every cut has `cheap_exact_rel = 0.0` and `edit_exact_rel = 0.0`; at `k = 7`, one cached suffix forward replaces eight and measures 7.993× speedup. This is amortized replay timing: checkpoint creation and retention are outside the suffix timing.

| cut `k` | forwards used | forwards saved | speedup | exact relative error |
|---:|---:|---:|---:|---:|
| 1 | 7 | 1 | 1.143× | 0.0 |
| 2 | 6 | 2 | 1.334× | 0.0 |
| 3 | 5 | 3 | 1.600× | 0.0 |
| 4 | 4 | 4 | 2.000× | 0.0 |
| 7 | 1 | 7 | 7.993× | 0.0 |

A valid cut contains the latent tensor, scheduler cursor and full timestep schedule, latent IDs, prompt-conditioned state, dtype, random-number contract, and resolution. An image or an integer step index alone is not an exact future.

## Why the mechanisms belong together

Phase residency lowers the cost of repeated images by moving weights at a declared boundary. Deep replay lowers the cost of repeated futures by retaining a typed entering state. Reference caching lowers the cost of repeated image-conditioned setup by retaining a reference state with an explicit identity and invalidation key. All three are instances of the same Saturn discipline:

```text
typed state identity + native consumer + declared suffix
        → exact replay, measured speedup, retained evidence
```

The execution layer is therefore portable at the contract level, while the actual state schema, token order, cache mode, decode operator, and numerical lane remain pipeline-local. That is why the plain Klein cache transfers and the KV adaptation stops at a recorded boundary.

## Claim boundary

**Observation:** The phase parity panel is bitwise exact across the declared resident and sequential FLUX cells, including the prompt-only 9B-KV fp8-sequential cell. The plain-Klein reference-edit cache is exact across Klein 4B, base-4B, and 9B. The 9B-KV cache mechanics pass while native-equivalent replay fails. The fp8-resident 9B hybrid is faster but non-bitwise. Deep replay is exact at every tested cut.

**Convergent trend:** The encode→denoise phase boundary and typed reference-state cache are portable across checkpoint and memory-lane changes when the pipeline shares the same trajectory ABI. The boundary does not transfer automatically into a pipeline whose attention order, K/V custody, token layout, or decode operator differs.

**Working inference:** The portable unit is an explicit execution contract — model and pipeline identity, conditioner preparation, dtype, scheduler/RNG state, latent IDs, reference identity, and native consumer — rather than a generic cached tensor or placement recipe. Exactness is a property of the whole declared state.

**Terminal status:** bounded terminal engineering result for scalar 512² four-step serving and the tested replay/cache panels on the Beast RTX 4080. Phase parity is established for the exact lanes listed above; plain-Klein edit reuse is established across three checkpoints; the KV adaptation is a recorded ABI boundary, not a null result about caching mechanics.

**Not established:** exact parity for batch sizes greater than one, compile modes, FP16 variants, 1024² panels, FLUX.2-dev, arbitrary hosts, or reference-conditioned 9B-KV replay before a KV-specific trajectory ABI. The fp8-resident hybrid does not establish parity, and none of these measurements claims a quality improvement — the goal is identical native output under a more efficient schedule.

## Local proof bundle

The complete compact evidence is in the [local artifact bundle](../artifacts/exact-phase-resident-serving/README.md). It contains the original receipts, copied cross-model receipts, null-evidence receipts, and the two cross-model analysis notes.

- [Original phase parity receipt](../artifacts/exact-phase-resident-serving/phase-parity-receipt.json)
- [Original cheap-deep replay receipt](../artifacts/exact-phase-resident-serving/cheap-deep-replay-receipt.json)
- [Original edit-cache receipt](../artifacts/exact-phase-resident-serving/edit-cache-receipt.json)
- [Cross-model phase analysis](../artifacts/exact-phase-resident-serving/phase-parity-crossmodel-analysis.md)
- [Cross-model edit-reuse analysis](../artifacts/exact-phase-resident-serving/edit-reuse-crossmodel-analysis.md)
- [Updated receipt verifier](../artifacts/exact-phase-resident-serving/verify.py)
- [Phase-parity preregistration](../../../saturn/experiments/2026-08-19-phase-parity-crossmodel/README.md)
- [Edit-reuse preregistration](../../../saturn/experiments/2026-08-19-edit-reuse-crossmodel/README.md)

The immutable source reports remain under `saturn/results/phase-parity-crossmodel/` and `saturn/results/edit-reuse-crossmodel/`, including the failed/null receipts and their corrected successors. Run `python ../artifacts/exact-phase-resident-serving/verify.py` from `research/bfl/demos/` to verify the original receipts and the copied cross-model receipt statuses.
