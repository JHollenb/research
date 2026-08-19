---
title: "Exact Phase-Resident Serving, Replay, and Edit Caching for FLUX.2 Klein"
type: experiment-report
status: bounded-terminal-engineering-result
rank_in_bfl_survey: 2
model: "FLUX.2 Klein 4B"
model_id: "black-forest-labs/FLUX.2-klein-4B"
revision: "e7b7dc27f91deacad38e78976d1f2b499d76a294"
checkpoint_role: "distilled native generator"
tags: [bfl, flux, serving, exact-parity, replay, caching, inference-efficiency]
---

# Exact Phase-Resident Serving, Replay, and Edit Caching for FLUX.2 Klein

> [!summary]
> Separating prompt encoding from denoising removes repeated weight transfers while preserving the native computation. On eight 512×512 FLUX.2 Klein 4B image cells, the phase-resident path is pixel- and PNG-exact against per-call CPU offload, with 10.66× per-image generation speedup and 6.25× end-to-end speedup. The same exact-state discipline enables suffix replay: use a saved entering cut and run only the remaining steps, saving seven of eight denoiser forwards at a late cut with zero relative error. A reference-edit cache reuses one 256-token image reference across four edits with exact output parity and a median cache-hit speedup of 4,696×.

## Research question

Can a FLUX.2 Klein serving schedule reduce residency and repeated computation without changing any output pixels, random-number behavior, or downstream semantics?

The experiment separates three related but independently testable mechanisms:

1. **Phase residency:** keep the prompt encoder resident only while prompt embeddings are produced, then keep the denoiser and VAE resident while multiple images use the cached embeddings.
2. **Deep replay:** retain an exact intermediate denoising state, validate/capture the prefix
   separately, and resume only the unchanged suffix.
3. **Reference-edit caching:** retain the exact reference-conditioned state needed by repeated image edits, then replay only the edit-specific suffix.

The central acceptance criterion is exact parity, not a perceptual tolerance. A candidate image
passes only when its pixel bytes and encoded PNG bytes match the reference image.

## Specimen and baseline

The primary specimen is `black-forest-labs/FLUX.2-klein-4B` at revision
`e7b7dc27f91deacad38e78976d1f2b499d76a294`, run through `Flux2KleinPipeline` in BF16. The
parity panel uses 512×512, four denoising steps, guidance 1.0, and the fixed prompts/seeds below.
The replay panel is the same model family and pipeline, but uses an eight-step trajectory for its
saved-cut assay.

The main parity panel uses FLUX.2 Klein 4B at 512×512, four denoising steps, guidance 1.0, two
seeds (`101`, `202`), and four prompts:

- a shop sign that says “OPEN” in bold red letters;
- a chrome teapot on a wooden table, studio lighting;
- a foggy mountain village at dawn, watercolor;
- exactly three yellow tennis balls on blue fabric.

The reference strategy uses model CPU offload. It transfers model components as needed for each image. The candidate strategy has explicit phases:

```text
encode phase:
    encoder resident → encode each prompt once → move embeddings to CPU/durable cache

denoise phase:
    encoder released → denoiser + VAE resident → generate all images from cached embeddings
```

No weights, scheduler equations, latent initialization, or VAE decode operations are changed.
Only the residency schedule changes.

## Exact parity test

The 10.66× figure is the candidate denoise-loop timing after the phase has been prepared; it does
not charge the one-time model load, prompt encoding, or encoder-to-denoiser transfer to the
per-image generation column. The reported 6.25× end-to-end figure is the benchmark's setup-plus-
generation comparison for this same panel. Neither number includes a separate circuit-tracer or
MRI capture pass: the phase runtime records its timing and parity receipts, but the expensive
instrumentation is not part of this serving benchmark.

The candidate receipt exposes the setup rather than hiding it: `load_wall_s = 0.370`,
`encode_phase_wall_s = 1.247`, and `swap_to_denoise_wall_s = 2.173`, alongside
`gen_wall_total_s = 4.855`. The headline per-image value uses the final field; the end-to-end
value uses the benchmark's request-level denominator.

For every prompt/seed pair, the reference and candidate receive the same prompt, seed, resolution, step count, guidance, and model revision. The receipt records both pixel and PNG SHA-256 hashes.

| Quantity | Reference | Phase-resident |
|---|---:|---:|
| Cells | 8 | 8 |
| Pixel/PNG parity | — | 8/8 exact |
| Aggregate generation time | 51.752 s | 4.855 s |
| Per-image speedup | — | 10.66× |
| End-to-end speedup | — | 6.25× |
| Peak VRAM in panel | 8,321.8 MB | 8,583.3 MB |

The small candidate VRAM increase is a phase-level residency choice, not extra model precision or an approximation. Every candidate pixel hash equals its reference hash. This is stronger than a
CLIP or perceptual-similarity result because it rules out even one-pixel changes in the declared
panel.

The [machine-readable parity receipt](../artifacts/exact-phase-resident-serving/phase-parity-receipt.json) contains the eight reference/candidate hash pairs.

## Exact deep replay

Let a generation contain `N = 8` denoising forwards and let `k` be a saved cut. A conventional
resume from a saved cut would still need to execute the suffix. The cheap-deep procedure uses the
cached entering-`k` latent and replays only the remaining `N-k` steps; a separate full-prefix
capture/validation path establishes that saved state. This is useful when a branch needs an exact
future after a known prefix rather than a new independent render.

The test uses cut positions `k ∈ {1, 2, 3, 4, 6, 7}`. Every cut has `cheap_exact_rel = 0.0` and `edit_exact_rel = 0.0`. At `k = 7`, the branch runs one cached suffix forward instead of eight and measures 7.993× speedup. This is an amortized suffix-replay number: the cost of creating and retaining the entering-`k` checkpoint is outside the replay timing. The same exactness holds for the tested edited suffixes.

| Cut `k` | Forwards used | Forwards saved | Speedup | Exact relative error |
|---:|---:|---:|---:|---:|
| 1 | 7 | 1 | 1.143× | 0.0 |
| 2 | 6 | 2 | 1.334× | 0.0 |
| 3 | 5 | 3 | 1.600× | 0.0 |
| 4 | 4 | 4 | 2.000× | 0.0 |
| 7 | 1 | 7 | 7.993× | 0.0 |

The key condition is state identity. A saved cut must retain the latent tensor, scheduler cursor,
full timestep/sigma schedule, latent IDs, prompt-conditioned state, and resolution. Retaining only an image or only an integer step index is not sufficient to guarantee the same suffix.

## Reference-edit cache

The edit-cache panel uses one real 256-token image reference and four image-conditioned edit
prompts. For each edit, the native path creates the reference-conditioned state from scratch. The cache path reuses the same state and runs the edit-specific continuation.

| Quantity | Result |
|---|---:|
| Reference reuses | 4 |
| Cache hits | 4 |
| Native-versus-replay exact cells | 4/4 |
| Mean cosine | 1.0 |
| Median native edit time | 0.3452 s |
| Median replay time | 0.1746 s |
| Median cache-hit speedup | 4,696.49× |
| Dependency invalidations | 4 |

The large hit-speedup number measures the reference-capture lookup itself, not the full image
render. It is therefore also an amortized cache-hit number, not an end-to-end image-generation
speedup. The full edit continuation still consumes time. The meaningful claims are exact replay,
correct dependency invalidation, and removal of repeated reference preparation.

## Why the three mechanisms belong together

Phase residency lowers the cost of repeated images by moving model weights at phase boundaries rather than per operation. Deep replay lowers the cost of repeated futures by retaining a precise intermediate state. Reference caching lowers the cost of repeated image-conditioned setup by retaining a precise reference state. All three depend on the same engineering invariant: state identity, scheduler position, dtype, and random-number contract must be explicit enough to compare two runs byte-for-byte.

This turns one expensive render into a reusable panel primitive:

```text
one encode → one resident denoise phase → many exact scalar images
one saved cut → many exact future branches
one reference state → many exact edits
```

## Claim boundary

**Terminal engineering result:** the exact scalar phase-resident panel is pixel/PNG exact for the
declared FLUX.2 Klein 4B configuration, and its measured speedup is directly actionable for that
configuration.

The reusable part is the explicit execution contract—conditioner preparation, typed state identity,
resident denoising, scheduler custody, and native-consumer parity. The measured result itself is
bound to `black-forest-labs/FLUX.2-klein-4B@e7b7dc27f91deacad38e78976d1f2b499d76a294`, BF16,
512×512, four steps, and the declared pipeline. A different FLUX topology or reference-conditioned
pipeline must earn its own ABI inspection, cache identity, and parity panel.

**Bounded replay result:** the tested cut positions and reference-edit rows replay exactly.

**Not established:** exact parity for batch sizes greater than one, compile modes, FP16 variants,
or other model families. Those faster lanes have separate numerical contracts and must be measured independently. The result also does not claim a quality improvement; the model and outputs are the same, only the execution schedule is more efficient.

## Local proof bundle

The complete compact evidence is in [the local artifact bundle](../artifacts/exact-phase-resident-serving/):

- [phase parity receipt](../artifacts/exact-phase-resident-serving/phase-parity-receipt.json)
- [cheap-deep replay receipt](../artifacts/exact-phase-resident-serving/cheap-deep-replay-receipt.json)
- [edit-cache receipt](../artifacts/exact-phase-resident-serving/edit-cache-receipt.json)
- [cache run receipt](../artifacts/exact-phase-resident-serving/edit-cache-run-receipt.json)
- [receipt verifier](../artifacts/exact-phase-resident-serving/verify.py)

Run `python ../artifacts/exact-phase-resident-serving/verify.py` from this directory to verify the 8/8 parity, zero replay error, saved-forward counts, exact edit rows, and cache statistics.
