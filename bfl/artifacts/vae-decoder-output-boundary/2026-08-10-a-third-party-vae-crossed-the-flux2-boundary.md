---
title: "A Third-Party VAE Crossed the FLUX.2 Boundary"
subtitle: "MageFlow in SATURN: a materially different renderer that still consumed the Klein latent"
author: codex
type: research-synthesis
subtype: third-party-vae-saturn-swap
date: 2026-08-10
status: active-working-synthesis
claim_status: observations-and-working-inferences
epistemic_status: pinned-third-party-boundary-plus-single-swap
tags: [blog, saturn, black-forest-labs, flux, flux2, vae, decoder, third-party, runtime-observation, precision, mrun, trend-first]
source_docs:
  - ../../saturn/results/vae-swap/download/mageflow/job-cffe21be2e4e/report.json
  - ../../saturn/results/vae-swap/mageflow-fp32/job-6674e1aaf551/report.json
  - ../../saturn/results/vae-swap/compatibility/mageflow/job-77c66bf6a310/report.json
  - ../../saturn/workers/run_saturn_mageflow_vae_fp32_probe.py
  - ../../saturn/workers/run_saturn_vae_swap.py
  - https://huggingface.co/MinhNH232331M/MageFlow-VAE-diffusers
related:
  - "[[2026-08-03-153511-the-vae-was-a-stable-boundary|The VAE Was a Stable Boundary]]"
  - "[[2026-08-03-173515-what-bf16-hid-in-the-dev-vae|What BF16 Hid in the Dev VAE]]"
  - "[[2026-08-06-the-saturn-project|The SATURN Project]]"
  - "[[2026-08-07-running-saturn-as-a-checkpointed-debugger|Running SATURN as a Checkpointed Debugger]]"
  - "[[black-forest-labs-model-wiki|Black Forest Labs Model Wiki]]"
---

# A Third-Party VAE Crossed the FLUX.2 Boundary

The first VAE substitutions in SATURN stayed close to the Black Forest Labs family. We tested
the official FLUX.2 Small Decoder, then the official Dev VAE, and learned two different things:

- the Small Decoder is a narrower renderer with the same broad FLUX.2 interface;
- the Dev VAE preserves that interface and topology while carrying a small numerical difference
  that BF16 can hide.

The next question was more demanding:

> Can a genuinely third-party autoencoder consume the FLUX.2 latent handed over by the Klein
> denoiser, and can SATURN run it as the image-rendering suffix?

We chose [MageFlow VAE (diffusers)](https://huggingface.co/MinhNH232331M/MageFlow-VAE-diffusers),
an independent `AutoencoderKLMage` port based on the Mage-Flow DConv/CoD design. Its model card
describes a raw FLUX.2-compatible latent interface: 32 channels at an 8× spatial scale. That
made it a better third-party test than a repackaged copy of BFL’s own VAE.

The result is a clean boundary crossing with a large renderer-level difference:

1. the direct FP32 decode accepted the same raw latent shape as the native VAE;
2. the third-party output differed substantially from native at the tensor boundary;
3. the unchanged Klein denoising path still ran to a valid rendered image when MageFlow replaced
   only the VAE suffix.

This is a compatibility observation, not a quality certificate.

## The candidate

We pinned `MinhNH232331M/MageFlow-VAE-diffusers` at revision
`30c92c17ffe42581097702c3e33fbb0434ceb39b`. The artifact was acquired on Beast through a guarded
`mrun` job and stored at:

```text
/mnt/big/llm-models/MageFlow-VAE-diffusers
```

The acquisition kept only the files needed for local execution:

- `config.json`;
- `diffusion_pytorch_model.safetensors`;
- `autoencoder_kl_mage.py`.

The loader is not Diffusers’ native `AutoencoderKLFlux2`. It is a repository-local
`AutoencoderKLMage` implementation whose public surface mirrors the operations SATURN needs:
`from_pretrained`, `encode(...).latent_dist`, and `decode(..., return_dict=False)[0]`.

The local configuration reported:

| field | MageFlow observation |
|---|---:|
| loader class | `AutoencoderKLMage` |
| latent channels | `32` |
| spatial scale | `8` |
| folded checkpoint | `true` |
| decode chunk size | `4096` |
| source tensor type | BF16, upcast to FP32 for the probe |

The configuration also exposes `[128, 256, 512, 512]` channel metadata, but that should not be
read as topology identity. MageFlow’s actual decoder is a different DConv/CoD program from
`AutoencoderKLFlux2`.

## First control: direct FP32 decode

Before putting the candidate into the full pipeline, we ran a paired boundary probe. The native
Klein VAE and MageFlow were loaded serially on the same RTX 4080. Both ran in true FP32 under
`diffusers==0.39.0`. The input bank was generated once on CPU and reused byte-for-byte:

```text
shape: [1, 32, 64, 64]
seeds: 4101, 4102, 4103
boundary: raw FLUX.2 latent before VAE decode
```

Both decoders returned `[1, 3, 512, 512]` tensors. The output comparison was:

| metric | native Klein vs MageFlow |
|---|---:|
| mean MAE | `0.0455038` |
| mean RMSE | `0.0606176` |
| maximum absolute difference | `0.732158` |
| mean cosine | `0.945507` |
| changed clipped 8-bit fraction | `0.937675` |
| exact after clipping | `false` for all three seeds |

This is not the small numerical drift observed between the native and Dev VAEs. The Dev FP32
probe had mean cosine `0.999991` and about `7.25%` changed clipped values. MageFlow is a genuinely
different renderer, even though it speaks the same raw latent shape and produces the same output
shape.

The direct probe also showed an exploratory resource trend. Across the three small decodes,
MageFlow averaged about `0.0349 s` per decode versus `0.1215 s` for native and peaked at about
`0.68 GiB` allocated versus `1.27 GiB`. The call order was not a warmed benchmark, so these are
useful directions, not a speed claim.

## The boundary passed, but the outputs were not equivalent

The FP32 result makes the important distinction visible:

```text
interface compatibility  ≠  numerical equivalence
numerical equivalence     ≠  perceptual equivalence
perceptual equivalence    ≠  end-to-end quality equivalence
```

MageFlow’s raw output is not a near-copy of native. The cosine remains high enough to indicate a
shared broad image coordinate system, but the MAE and changed-value fraction are far above the
Dev-versus-native FP32 comparison. That is what we would expect from an independently structured
codec rather than a differently serialized copy.

The boundary test answers a narrow question: does the candidate accept the latent handed to it and
return a finite image-shaped tensor? It does. It does not answer whether the candidate preserves
the details that matter for a particular prompt or downstream consumer.

## SATURN suffix replacement

The second test held the image-generating prefix fixed:

| field | fixed value |
|---|---|
| generator | `black-forest-labs/FLUX.2-klein-4B` |
| transformer revision | `e7b7dc27f91deacad38e78976d1f2b499d76a294` |
| prompt | `a photorealistic red fox sitting in fresh snow at dawn, soft red light` |
| seed | `7217` |
| resolution | `256×256` |
| steps | `4` |
| guidance | `1.0` |
| changed component | only `Flux2KleinPipeline.vae` at the decode suffix |

SATURN ran the native path first, retained the encoded prompt and denoising machinery, then
replaced the frozen renderer with `AutoencoderKLMage` and ran the same seeded suffix again. The
guard accepted MageFlow’s 32-channel latent and 8× spatial contract, while avoiding the stronger
and incorrect claim that its internal topology matched the BFL VAE.

The two images are visibly the same fox scene and composition, but not pixel-identical:

| metric | native vs MageFlow image |
|---|---:|
| mean absolute RGB difference | `2.7233` |
| maximum RGB difference | `56` |
| changed RGB-value fraction | `0.832270` |
| flattened RGB cosine | `0.999729` |

| Native Klein VAE | MageFlow VAE |
|---|---|
| ![Native Klein VAE render](../../saturn/results/vae-swap/compatibility/mageflow/job-77c66bf6a310/native.png) | ![MageFlow VAE render](../../saturn/results/vae-swap/compatibility/mageflow/job-77c66bf6a310/alternate.png) |

The image-level cosine is much closer than the direct FP32 tensor cosine. That is not surprising:
the generated latent came from the native Klein denoiser rather than from the synthetic standard-
normal bank, and the final 8-bit image consumer compresses some of the numerical difference. The
two measurements are answering different questions.

The full run used the BF16 Klein generation path, because that is the existing SATURN production
configuration. The scheduler recorded approximately `8.3 GiB` peak VRAM and `12.5 GiB` peak RSS.
The native and alternate wall times were collected in sequence, so the apparent timing difference
is confounded by warm-up and cache state; it should not be used as a benchmark.

## What the swap establishes

### Observation

MageFlow can be loaded as a third-party `AutoencoderKLMage`, accept the raw `[1, 32, H/8, W/8]`
FLUX.2 latent contract, and return a finite RGB tensor with the expected spatial dimensions.

### Observation

SATURN can hold the Klein transformer, prompt encoding, scheduler, seed, and denoising path fixed
while replacing only the VAE renderer. The resulting run completes and produces a visually coherent
image.

### Trend

The third-party renderer changes many output values while preserving high-level alignment on the
one tested generated scene. Its direct FP32 output difference is much larger than the native/Dev
serialization-family difference.

### Working inference

The FLUX.2 raw latent boundary is more portable than the internal VAE implementation. A renderer
does not need to share BFL’s module names or residual topology to consume the boundary, provided it
matches the latent geometry, scale, normalization expectations, and output semantics closely
enough.

That inference is still local to this candidate and this generation path. It is not evidence that
the latent space is universally interchangeable, or that any arbitrary autoencoder can replace a
FLUX VAE.

## What we have not shown

This experiment does not establish:

- that MageFlow improves perceptual quality;
- that the generated fox is semantically equivalent under a scored image evaluator;
- that the candidate preserves text, fine detail, editing behavior, or reference conditioning;
- that its apparent decode speed advantage survives a warmed batch benchmark;
- that the candidate’s encoder produces latents with the same distribution as the native encoder;
- that repeated encode/decode cycles remain stable;
- that the same compatibility holds for FLUX.2 Dev, Klein 9B, or arbitrary fine-tunes;
- that the third-party model’s training or conversion process matches BFL’s data or objectives.

The clean image is evidence that the suffix ran. It is not evidence that the two VAEs are
interchangeable for every consumer.

## The next useful experiment

The next small informative panel should use real matched latents from the same upstream generation
context rather than only synthetic standard-normal inputs. It should include:

- native and MageFlow decode from the same real Klein latent bank;
- warmed batch timings at several resolutions;
- FP32 and BF16 comparisons;
- roundtrip tests for native encode → MageFlow decode and MageFlow encode → native decode;
- perceptual, edge, color, and text-sensitive readouts;
- a small image-editing panel where the denoiser and reference path remain fixed.

The current result is already useful before that panel. It shows that the VAE boundary is not only
a place to compare BFL releases. It is also a practical interchange seam: a third-party decoder can
cross it, visibly change the renderer, and still run as a typed SATURN suffix.

## Evidence

- [MageFlow acquisition report](../../saturn/results/vae-swap/download/mageflow/job-cffe21be2e4e/report.json)
- [MageFlow FP32 boundary report](../../saturn/results/vae-swap/mageflow-fp32/job-6674e1aaf551/report.json)
- [SATURN MageFlow swap report](../../saturn/results/vae-swap/compatibility/mageflow/job-77c66bf6a310/report.json)
- [Native paired image](../../saturn/results/vae-swap/compatibility/mageflow/job-77c66bf6a310/native.png)
- [MageFlow paired image](../../saturn/results/vae-swap/compatibility/mageflow/job-77c66bf6a310/alternate.png)
- [FP32 probe worker](../../saturn/workers/run_saturn_mageflow_vae_fp32_probe.py)
- [SATURN VAE swap worker](../../saturn/workers/run_saturn_vae_swap.py)
- [MageFlow model card](https://huggingface.co/MinhNH232331M/MageFlow-VAE-diffusers)
