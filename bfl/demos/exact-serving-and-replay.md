---
title: "Bitwise-Exact State Cuts and Replay Across FLUX"
type: experiment-report
date: 2026-08-19
models:
  - id: "black-forest-labs/FLUX.2-klein-4B"
    revision: "e7b7dc27f91deacad38e78976d1f2b499d76a294"
  - id: "black-forest-labs/FLUX.2-klein-base-4B"
    revision: "a3b4f4849157f664bdbc776fd7453c2783562f4d"
  - id: "black-forest-labs/FLUX.2-klein-9B"
    revision: "92196c8e11f7b6cf2b7493e037d8c5345c559216"
  - id: "black-forest-labs/FLUX.2-klein-9b-kv"
    revision: "a6dfb36eca3a3906eb2fd460795adfb844e5fcce"
  - id: "black-forest-labs/FLUX.1-schnell"
    revision: "741f7c3ce8b383c54771c7003378a50191e9efe9"
  - id: "black-forest-labs/FLUX.2-dev"
    revision: "26afe3a78bb242c0a8bb181dcc8937bb16e5c66c"
  - id: "black-forest-labs/FLUX.2-small-decoder"
    revision: "a3efc24f613ef42d9428af62fdbd6f5fd8856c4a"
status: "bitwise-exact across five checkpoints; two labeled exceptions"
merged_from:
  - exact-phase-resident-serving.md
  - flux2-dev-paged-execution.md
  - vae-decoder-output-boundary.md
  - closed-loop-students-mappers.md
tags: [bfl, flux, flux1, flux2, serving, exact-replay, state-cuts, caching, paging, vae-decoder, distillation, inference-efficiency]
---

# Bitwise-exact state cuts and replay across FLUX

## What we found

We can stop a FLUX image generation at any denoising step, save the full state, and resume it later with no error at all. Across five pinned FLUX checkpoints, 64 of 64 phase-parity images (eight cell runs of eight images; one cell was measured in two sessions) came out byte-identical to the pipeline's own output, and replaying only the unchanged suffix from a saved cut had relative error exactly 0.0 at every tested step (k ∈ {1, 2, 3, 4, 6, 7}). Exactness is the headline because it is what makes every causal experiment in this collection trustworthy: a resumed or edited image is provably the model's own output, not a look-alike. The same discipline lets us encode each prompt once and keep the denoiser resident, worth 10.66–12.73× per image against the pipeline's own CPU-offload schedule on a 16 GB RTX 4080, where the encoder and denoiser cannot both stay in memory. Two results sit just outside the exact set, and we label them as such: the 9B-KV reference cache and an fp8-resident hybrid.

![Native FLUX.2 decoder output.](../artifacts/vae-decoder-output-boundary/native.png)
![Small Decoder output, 43.678% fewer parameters.](../artifacts/vae-decoder-output-boundary/alternate.png)

*Figure 1. Two decoder outputs that are indistinguishable to the eye. Left: the native FLUX.2 decoder. Right: a Small Decoder with 43.678% fewer parameters, at pixel cosine 0.999784 and PSNR 44.64 dB — yet exact parity fails on all 192/192 tested outputs. This is exactly why we certify "same" by comparing bytes, not by looking.*

## Why this matters

Activation patching and causal tracing (Meng et al. 2022; Wang et al. 2022; Zhang & Nanda 2023 on patching's fragility) only mean something if the patched run is otherwise the model's exact computation. Trajectory-reuse edit methods — Prompt-to-Prompt (Hertz et al. 2022), SDEdit (Meng et al. 2021) — resume part of a diffusion trajectory but judge the result by appearance. We take the Git-style idea (save a state, branch, resume) and hold it to a stricter bar: the resumed or edited image must be byte-identical to what the unmodified pipeline would have produced. That is what lets the rest of this collection attribute an image change to the model, not to an approximation.

## Setup

| checkpoint | revision | role here |
| --- | --- | --- |
| FLUX.2 Klein 4B | `e7b7dc27…` | phase parity, replay, edit cache |
| FLUX.2 Klein base 4B | `a3b4f484…` | phase parity, edit cache |
| FLUX.2 Klein 9B | `92196c8e…` | phase parity, edit cache |
| FLUX.2 Klein 9B-KV | `a6dfb36e…` | labeled cache boundary |
| FLUX.1 Schnell | `741f7c3c…` | phase parity (CLIP+T5 conditioner) |
| FLUX.2 Dev | `26afe3a7…` | paged one-step feasibility |
| FLUX.2 Small Decoder | `a3efc24f…` | decoder compatibility boundary |

Unless noted, the judge is the real FLUX denoiser, scheduler, VAE, and decoded PNG — no surrogate. The phase-parity panel uses four prompts, two seeds (`101`, `202`), 512×512, four denoising steps, and fresh CPU random generators per image. The reference-edit panel uses one reference image from the cell's own model, four real edits, seed `92001`, 256×256, four steps, with a state cut saved at step 2. The suffix-replay panel uses an eight-forward trajectory with cuts at k ∈ {1, 2, 3, 4, 6, 7}.

A valid **state cut** holds everything needed to resume exactly: the latent tensor, the scheduler cursor and full timestep schedule, latent IDs, the prompt-conditioned hidden state and its dtype, the random-number contract, the reference identity, and the resolution. An image, or a bare step index, is not an exact future. Acceptance is byte identity: pixel bytes and encoded PNG bytes must match the pipeline's own offload reference.

## Exact: encode once, keep the denoiser resident

The stock pipeline streams weights per image because the card cannot hold both encoder and denoiser. Encoding every prompt once, caching the exact conditioner state, releasing the encoder, and keeping the denoiser resident removes those per-image transfers while changing no weight, equation, latent initialization, or decode operator. Every image came out byte-identical.

| cell | memory lane | parity | per-image speedup vs the pipeline's own offload schedule |
| --- | --- | ---: | ---: |
| Klein 4B | resident BF16 | 8/8 exact | 12.73× |
| Klein base 4B | resident BF16 | 8/8 exact | 12.38× |
| Klein 9B | BF16 sequential | 8/8 exact | 1.18× |
| FLUX.1 Schnell | fp8-e4m3 sequential | 8/8 exact | 1.43× |
| Klein 9B-KV | fp8-e4m3 sequential | 8/8 exact | 2.49× |

Across the full panel, 64/64 images were bitwise identical (the table shows representative cells). The original Klein-4B run reported 10.66× per image and 6.25× end-to-end against its offload baseline; the expanded same-day panel reported 12.73× and 7.02× against the same kind of baseline. Resident lanes get the large (~12×) gain by dropping per-image weight transfers; sequential lanes still stream the oversized denoiser, so their 1.06–1.43× gain is only from removing encoder streaming. The speedup is a bonus — the byte identity is the result.

**Labeled exception (non-bitwise).** An fp8-resident 9B hybrid keeps an fp8 denoiser resident while streaming the Qwen3-8B encoder, reaching 1.51 s/image at 512² (9,961 MB peak) and 6.40× per image over the same offload baseline. But resident and streamed fp8 accumulate differently, so it is 0/8 exact with median ΔRGB 4.6. It is a throughput mode, not a parity mode.

## Exact: resume from a saved cut

Replaying only the unchanged suffix from a saved cut reproduces the trajectory exactly — every cut has relative error 0.0, and the late one-forward cut replaces eight forwards.

| cut k | forwards used | forwards saved | speedup | exact relative error |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 7 | 1 | 1.143× | 0.0 |
| 2 | 6 | 2 | 1.334× | 0.0 |
| 3 | 5 | 3 | 1.600× | 0.0 |
| 4 | 4 | 4 | 2.000× | 0.0 |
| 7 | 1 | 7 | 7.993× | 0.0 |

These are amortized replay numbers: checkpoint creation and retention sit outside the suffix timing.

## Exact edit reuse, and where it stops

Repeated edits that share one reference image can replay from the step-2 cut instead of recomputing the reference each time. On plain Klein 4B, base 4B, and 9B the replay is byte-identical to native (4/4 exact per cell), and all four reference changes correctly invalidate the cache. The honest edit-time saving is the full native-versus-replay median below. The cache hit itself is roughly 50 µs against a roughly 2.8 s miss, so the "thousands-×" lookup ratios some tables report are this cache-hit latency, not a render speedup.

| cell | memory lane | native↔replay exact | full native / replay median |
| --- | --- | ---: | ---: |
| Klein 4B | resident | 4/4 | 0.350 s / 0.175 s |
| Klein base 4B | resident | 4/4 | 0.350 s / 0.175 s |
| Klein 9B | BF16 sequential | 4/4 | 5.43 s / 2.71 s |
| Klein 9B-KV | BF16 sequential | 0/4 | 5.11 s / 2.70 s |

**Labeled exception (9B-KV replay).** The 9B-KV cache mechanics pass — hits return the identical checkpoint, hashes match, all four reference changes invalidate — but replay is not byte-exact (cosine ≥ 0.994, mean ΔRGB about 5–13). The reason is specific, not a generic cache failure. The native KV loop orders tokens `[reference, target]`, gives reference tokens extract-mode causal self-attention, and reuses cached K/V, whereas the generic capture path orders `[target, reference]` through the standard forward with a different decode signature. The KV pipeline needs its own trajectory format before exact replay can be claimed. Shared weights do not imply a shared execution contract.

## Running an oversized checkpoint by paging

The 112.805 GB BF16 FLUX.2 Dev artifact runs a guarded one-step 512² forward and VAE decode by paging its 24.011B-parameter Mistral conditioner and 32.223B-parameter denoiser with explicit lifetimes, so they are never co-resident. All 11/11 lifecycle gates pass in about 336.41 s with about 12.7 GB of swap observed at completion — direct evidence that paging actually occurred rather than accidental co-residency. This is a feasibility and memory result, not a speed or quality one. A richer, unguarded four-step worker diagnostic reaches CLIP 0.360, count 0.833, and OCR character 0.472, but it stays exploratory and does not upgrade the one-step claim.

## The decoder is a compatibility surface, not an exact one

Figure 1 makes the point numerically. The Small Decoder removes 43.678% of decoder parameters, runs about 1.517× faster, and reaches pixel cosine 0.999784 and PSNR 44.64 dB — yet exact parity fails on all 192/192 tested outputs. A third-party MageFlow VAE reaches latent cosine 0.945507 and, swapped into the full path, image cosine 0.999729. Residual-merge replay through `norm1`, `conv1`, `norm2`, and `conv2` is exact until a one-pixel shortcut shift moves the terminal L2 by 207.13 — a tiny indexing error, a large endpoint change. A 283-arm blind probe (seven residual blocks × an 8×8 field of source perturbations) reaches the output in every arm, so there are no silent arms, but reaching the output is not owning a concept. The decoder can be swapped within a perceptual tolerance; it cannot be swapped where exact reproducibility is required.

## The approximate end: a distilled closed-loop student

Give up exactness and you can go much faster. A 3,768,459-parameter student — a dense state transition, a patchwise reference register (a saved slice of hidden state it can read and write), an uncertainty-gated correction bank, and a predictor for the next native step — continues a FLUX.2 Klein 4B trajectory from its own predictions. Scheduler parity is cosine 0.9999981638. Over a full 800-step, 6,400-image trajectory, free-rollout image cosine is 0.878103 mean with 0.743759 minimum, and it improves across cuts (mean 0.849561 → 0.913191; minimum 0.743759 → 0.831640) rather than drifting away. In a bounded 24-prompt lane the reference-register student runs 22.2–32.7× faster than native generation (≈80–89 versus 2.7–3.9 images/s) at free-rollout image cosine 0.960046 mean but 0.796 minimum; teacher-forced is ≈0.987. The worst cases stay poor — the uncertainty-mode raw rollout has minimum 0.066238 — so this is a fast approximate simulator, not a drop-in replacement.

## Controls

- Byte and PNG identity against the model's own offload output rules out a near-miss passing as exact.
- Checkpoint-hash return plus dependency invalidation on every reference change rules out a stale cache hit.
- Explicit non-co-residency plus swap telemetry rules out accidental co-residency masquerading as paging.
- The 192/192 exact-parity failure count rules out high cosine or PSNR being read as identity.
- Teacher-forced versus free rollout rules out compounding error hidden by supplied ground truth; prompt-disjoint evaluation rules out memorizing the training prompts; reporting minima rules out hiding failure behind a mean.

## Limits and open questions

- Exact parity is established only for batch size 1, 512² (and 256² edits), four steps, BF16 and fp8-sequential storage, on the one 16 GB RTX 4080 host. Larger batches, compile modes, FP16 variants, 1024² panels, and other hosts are untested.
- 9B-KV reference-conditioned replay is not byte-exact until a KV-specific trajectory format exists; only its cache mechanics are verified.
- The fp8-resident hybrid is non-bitwise by construction (median ΔRGB 4.6); it is a throughput mode only.
- Dev paging is a one-step 512² feasibility proof on one host; its four-step diagnostic is unguarded. No throughput, multi-request, or quality claim follows.
- The Small Decoder and MageFlow swaps are bounded-panel compatibility, not arbitrary interchangeability, training-time gradient equivalence, or semantic ownership; the blind-probe magnitudes (alternate-seed deltas ~6× at `up_blocks.1`, 14–15× at `up_blocks.2`, 13× at `up_blocks.3`, ~0.04× in the decoder tail) reflect output connectivity, normalization scales, and local geometry, not semantic necessity.
- The student's worst-case tail is poor; some wide-batch throughput rows reuse one captured input, so they show repeated-input speed, not independent-prompt throughput; latent/VAE closure is incomplete, and portability to other families and resolutions is untested.
- None of these results claims a quality improvement; the goal is identical native output under a cheaper schedule.
- **Recoverable failures retained.** The first sequential phase job rendered every image bit-exact, then crashed in cleanup (`PhasePipeline.close()` called `module.to("cpu")` on accelerate-owned meta tensors); the PNGs were rehashed and a corrected run reran cleanly. The first fp8-resident probe resolved `_execution_device` to the encoder's meta device; excluding resident components from the device walk fixed it. Both are harness bugs, not parity failures, and their null run records are kept.

## Reproduce and inspect

- Phase-parity, suffix-replay, and edit-cache receipts, cross-model analyses, null and corrected run records, and the verifier: [`../artifacts/exact-phase-resident-serving/`](../artifacts/exact-phase-resident-serving/README.md) (run `verify.py` from `research/bfl/demos/`).
- Dev paged-execution configuration, lifecycle evidence, and verifier: [`../artifacts/flux2-dev-paged-execution/`](../artifacts/flux2-dev-paged-execution/README.md).
- VAE/decoder report, residual substitution I/O, blind probe, and verifier: [`../artifacts/vae-decoder-output-boundary/`](../artifacts/vae-decoder-output-boundary/README.md).
- Closed-loop mapper and full-trajectory records, performance reference, and verifier: [`../artifacts/closed-loop-students-mappers/`](../artifacts/closed-loop-students-mappers/README.md).

Additional internal run logs are available on request.
