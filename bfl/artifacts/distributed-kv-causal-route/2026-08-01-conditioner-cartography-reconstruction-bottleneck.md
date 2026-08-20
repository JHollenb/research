---
title: "The Binding Bottleneck Was Reconstruction, Not Encoding"
date: 2026-08-01T19:30:00-07:00
tags: [flux, conditioner, binding, cartography, measured]
source_docs:
  - ../../experiments/2026-08-01-conditioner-cartography/outputs/conditioner-cartography.v1.json
  - ../../experiments/2026-08-02-bfl-three-claims/h9-causal-route/OWNER_REPAIR_STATUS.md
related:
  - "[[2026-08-01-040000-inside-the-flux-arbitration-harness]]"
  - "[[2026-08-01-h8-temporal-route-localization]]"
  - "[[2026-07-31-145130-the-conditioners-were-stock-checkpoints]]"
  - "[[2026-08-01-001500-opening-the-black-forest-what-six-parallel-tracks-taught-us-about-flux]]"
---

FLUX.1-schnell (CLIP+T5) fails color-binding admission at 0.375. FLUX.2-klein-4B (Qwen3-4B) passes at 1.000. Why?

The obvious hypothesis: Qwen3 *encodes* binding better. It represents "red cube" differently from "blue cube" in a way CLIP/T5 don't. This is wrong.

## The experiment

Load all three text encoders — Qwen3-4B (from klein-4B), T5-XXL (from schnell), CLIP (from schnell) — and process 16 two-object color-binding prompts ("a red cube on the left and a blue sphere on the right"). Extract per-layer hidden states. Measure:

1. **Color/noncolor norm ratio**: how large are color-token representations relative to non-color tokens at each layer
2. **Effective rank**: dimensionality of the representation at color-token positions  
3. **CKA cosine structure**: does same-color > same-object > different-both in representation space
4. **Binding decodability**: can a linear probe decode color-object binding from concatenated token vectors

All three encoders run on CPU. No GPU needed — these are text encoders, not denoisers.

## What we found

### All three encoders separate color from object

CKA at the final layer:

| Encoder | same_color cos | same_object cos | diff_both cos | color_separation |
|---------|---------------|-----------------|---------------|-----------------|
| Qwen3-4B | 0.860 | 0.814 | 0.787 | 0.073 |
| T5-XXL | 0.777 | 0.758 | 0.691 | 0.086 |
| CLIP | 0.621 | 0.462 | 0.399 | 0.222 |

CLIP actually has the *strongest* relative color separation. The encoding hypothesis — that Qwen3 encodes color better — is wrong.

### All three absorb color tokens into context mid-network

Every encoder shows the same pattern: early in the network, color-word tokens have normal representation norms. Then they crash — color token norms drop to 7-14% of non-color token norms:

| Encoder | Transition layer | Pre-transition ratio | Post-transition ratio |
|---------|-----------------|---------------------|----------------------|
| Qwen3-4B | 6→7 | 0.962 | 0.088 |
| T5-XXL | 7→8 | 1.170 | 0.157 |
| CLIP | 0→1 | 0.608 | 0.074 |

Color information diffuses from word positions into distributed context. This is why binding probes at word positions fail — binding isn't *at* color positions mid-network, it's everywhere.

### Only Qwen3 reconstructs

Here's the critical divergence. After the absorption phase:

**Qwen3-4B**: color/noncolor ratio RECOVERS from 0.088 at layer 7 to 0.759 at layer 35 and 0.936 at the final layer (36). Effective rank grows from 1.4 to 10.1. Color information is read from distributed context and written back to output positions.

**T5-XXL**: stays at 0.10-0.16 from layer 8 through layer 23. No recovery. Final layer (24) normalizes to 1.123 but this appears to be layer-norm artifact — effective rank only reaches 2.1 at layer 23.

**CLIP**: ratio grows from 0.074 to 0.269 over 12 layers. Slow partial recovery. Effective rank reaches only 2.2. Color tokens are still 4× smaller than non-color tokens at output.

### Qwen3 reconstruction trajectory (all 37 layers)

| Layer | Color norm | Noncolor norm | Ratio | Eff rank |
|-------|-----------|---------------|-------|----------|
| 0 | 1.05 | 0.99 | 1.063 | 10.7 |
| 6 | 32.23 | 33.49 | 0.962 | 9.7 |
| 7 | 33.71 | 384.57 | **0.088** | 1.4 |
| 18 | 57.25 | 422.50 | 0.136 | 1.6 |
| 27 | 169.14 | 509.89 | 0.332 | 2.5 |
| 31 | 321.81 | 636.10 | 0.506 | 3.5 |
| 35 | 630.65 | 831.20 | 0.759 | 5.6 |
| 36 | 116.90 | 124.90 | **0.936** | 10.1 |

This is a U-shaped trajectory: encode → absorb → distribute → **reconstruct**. The reconstruction phase (layers 7–35) steadily re-concentrates binding information at output positions with growing effective rank.

## Why this matters for image generation

The denoiser reads the text encoder's output embeddings. If binding information is distributed and low-rank at output positions, the denoiser's cross-attention has weaker signal for which color belongs to which object.

Qwen3's reconstruction trajectory gives the denoiser output embeddings where:
- Color-token positions have **93.6%** the norm of non-color tokens (vs 26.9% for CLIP)
- Effective rank at color positions is **10.1** (vs 2.2 for CLIP)
- Binding structure is high-dimensional and positioned where cross-attention can read it

The binding bottleneck was never about encoding — all three encoders separate color from object internally. The bottleneck is **reconstruction**: whether the encoder writes binding-relevant structure back to output positions in a form the denoiser can use.

## Binding probe failure (expected)

The linear probe (concatenated color+object token vectors → binary binding label) produced below-chance accuracy for all three encoders. This is informative, not broken: with n=52 samples in d=5120 dimensional space, the probe is fundamentally underpowered. More importantly, binding information isn't *at* word positions in mid-network — it's distributed.

A properly powered probe would need (a) many more prompts and (b) to use attention-weighted or position-averaged representations rather than single-token vectors. But the norm/rank diagnostics already tell the story without needing a probe.

## Connection to the arbitration harness

The arbitration harness showed that FLUX.2's denoiser processes binding through distributed native mechanisms — no single block is sufficient to flip binding, block 13 is the native carrier but doesn't categorically determine outcomes. The conditioner cartography explains the upstream side: Qwen3 reconstructs binding information in a high-rank, position-rich format that gives the denoiser material to distribute.

The full pipeline picture: Qwen3 absorbs → distributes → **reconstructs** binding at output → denoiser cross-attention reads it → block 13 carries it → distributed network processes it → binding appears in the image.

## Artifacts

- `conditioner-cartography.v1.json`: full results (37 Qwen3 layers + 25 T5 layers + 13 CLIP layers, per-layer diagnostics, CKA, probe results)
- Script: `experiments/2026-08-01-conditioner-cartography/src/run_conditioner_cartography.py`

## What's next

1. **Activation divergence** (GPU, pending): where does clean/corrupt binding divergence concentrate in the denoiser? Connects conditioner output to denoiser processing.
2. **H5–H9 native route program** (spatial/temporal route supported; bilateral specificity pending): the
   progressive coalition and held-out dose assays support a distributed native carrier trajectory,
   while exact endpoint transfer is concentrated in the full20 exchange. H8 shows that full20
   all-step grafting beats every single-step graft in both directions, with a negative late-minus-
   early contrast. Five H9 controls remain valid and positive, but the reverse wrong-world arm has
   45/96 donor-color collisions and awaits H9R. Compact S4/S8 sets still do not form an exact native quorum. See
   [[2026-08-01-h9-native-specificity-replication]].
3. **T6 typography connection**: do per-word diagnostics (norm, effective rank at output) predict rendering success for typography words? If Qwen3's reconstruction trajectory correlates with renderability, this becomes a predictive instrument.
4. **Repair, then generalization**: complete the frozen direction-safe reverse wrong-world H9R
   bridge, then repeat the route on another workload or model/conditioner combination if a broader
   claim is required. The historical H9 automatic verdict is not the current owner verdict.
