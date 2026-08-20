---
title: "From Conditioner to Pixels: How the Black Forest Models Are Put Together"
subtitle: "A systems-level account of what FLUX is, where its state moves, and what the decoder work changed"
author: codex
type: research-synthesis
subtype: bfl-system-architecture
date: 2026-08-03
status: active-working-synthesis
claim_status: observations-trends-and-working-inferences
epistemic_status: pinned-artifact-runtime-and-paired-boundary-evidence
tags: [blog, black-forest-labs, flux, flux1, flux2, architecture, denoiser, conditioner, vae, decoder, latent, static-analysis, model-analysis, manalysis, mrun, trend-first]
source_docs:
  - ../../experiments/2026-08-03-141631-generative-functional-rosetta-static-decode/results/vae-comparison.md
  - ../../experiments/2026-08-03-141631-generative-functional-rosetta-static-decode/results/vae-shard-comparison.md
  - ../../experiments/2026-08-01-233923-bfl-generational-model-observatory/reports/DECODER_TRENDS.md
  - ../../experiments/2026-08-01-233923-bfl-generational-model-observatory/reports/STATIC_TRENDS.md
  - ../../experiments/2026-08-01-233923-bfl-generational-model-observatory/reports/PHYSIOLOGY_TRENDS.md
  - ../../experiments/2026-07-24-generative-image-model-atlas/BFL_FLUX2_REPORT.md
related:
  - "[[../black-forest-labs-model-wiki|Black Forest Labs Model Wiki]]"
  - "[[2026-08-03-153511-the-vae-was-a-stable-boundary|The VAE Was a Stable Boundary, Not the Scaling Axis]]"
  - "[[2026-08-03-135833-the-models-had-metabolisms-not-just-scores|The Models Had Metabolisms, Not Just Scores]]"
  - "[[2026-08-02-seven-flux-artifacts-under-the-microscope|Seven FLUX Artifacts Under the Microscope]]"
  - "[[2026-08-02-black-forest-labs-measured-model-reference|Measured BFL Model Reference]]"
  - "[[2026-07-28-143331-inside-the-black-forest-flux-models|Inside the Black Forest FLUX Models]]"
  - "[[2026-08-02-213500-black-forest-model-observatory-what-we-built-and-learned|BFL Generational Observatory]]"
  - "[[../indexes/black-forest-labs-survey|Black Forest Labs Research Survey]]"
  - "[[../experiments/2026-08-03-141631-generative-functional-rosetta-static-decode/results/vae-shard-comparison|Exact per-tensor VAE shard comparison]]"
---

# From Conditioner to Pixels: How the Black Forest Models Are Put Together

After measuring six Black Forest Labs generators and one auxiliary decoder, we can give a more
useful answer to the question “what is a FLUX model?” It is not one undifferentiated neural
network, and it is not adequately described by a parameter count or a final image score. In the
pinned cohort, it is a typed computational chain whose parts have different jobs, different
scaling behavior, different state, and different evidence boundaries.

Our current working picture is:

```text
prompt / reference inputs
          │
          ▼
conditioner ──► context carried into the image program
          │
          ▼
flow denoiser ◄── repeated scheduler / latent updates
          │
          ▼
latent boundary
          │
          ▼
VAE decoder ──► pixels ──► evaluator, recorder, or downstream consumer
```

That diagram is simple, but it gives us a powerful way to keep unlike questions separate. The
conditioner supplies context. The denoiser performs the main iterative transformation. The
scheduler moves the latent state through the denoising trajectory. The VAE converts the final
latent into pixels. The evaluator sees only the rendered result, unless we deliberately record the
intermediate state.

The diagram is an evidence-backed model of the public artifacts we hold, not a claim about BFL’s
private training process or a complete semantic explanation of the latent.

## What we were trying to understand

The initial temptation with generative image models is to ask which model scores highest or which
release is “better.” That is useful for product evaluation, but it is a poor microscope. A score
does not tell us whether a change came from the conditioner, the denoising program, the scheduler,
the latent interface, the decoder, the runtime, or the evaluator.

We wanted to understand the model as a working system:

- What physical components are actually present in each pinned artifact?
- Which interfaces connect them?
- Which parts scale across FLUX.1, Klein, 9B, 9B-KV, and Dev?
- Which release differences are weight changes, topology changes, recipe changes, or runtime
  changes?
- Where can we capture state without confusing a readout with a causal mechanism?
- What happens when we hold the latent fixed and replace only the output consumer?

This is why the VAE and Small Decoder work matters. It gives us an unusually clean intervention at
the end of the chain. The denoiser can produce one latent, and two different consumers can render
it. That lets us study the output boundary without pretending that pixel differences explain how
the denoiser formed its state.

The work is summarized in the component-specific post
[The VAE Was a Stable Boundary, Not the Scaling Axis](2026-08-03-153511-the-vae-was-a-stable-boundary.md),
while this post places that result inside the full FLUX system.

## The five parts of the chain

### 1. The conditioner establishes context

The conditioner turns the prompt, reference information, or other external inputs into a state
that the image program can consume. It is not merely an embedding lookup in the systems we
measured. Its width, token structure, parent checkpoint, and connection to the denoiser are part
of the model’s physical interface.

The measured cohort shows three distinct conditioner regimes:

- FLUX.1 Schnell uses a CLIP plus T5 arrangement.
- Klein 4B and 9B use Qwen3-derived conditioner substrates at their respective scales.
- Dev uses a Mistral-Small-derived conditioner substrate.

Sampled embedding screens and eigenbasis comparisons strongly associate those components with the
public parent checkpoints. That is useful provenance evidence, but it is not a claim that the
denoisers inherit the parent model’s knowledge or that a sampled embedding screen reconstructs the
entire conditioner.

The conditioner is also one of the reasons parameter counts are easy to misread. Klein 4B has a
roughly 3.9B denoiser and a roughly 4.0B conditioner. Dev has a roughly 32.2B denoiser and a
roughly 24.0B conditioner. The context-producing phase is a large part of the system, and in Dev
it has a distinct runtime lifetime from the denoiser.

### 2. The flow denoiser is the main iterative organism

The denoiser receives the current latent state, the conditioned context, timestep information, and
in some variants reference state. It predicts the update used by the scheduler. That operation is
repeated over the model’s native denoising recipe.

In the pinned cohort, the denoisers are attention-based rectified-flow transformer programs. Their
physical scale and block allocation change substantially:

| Artifact | Denoiser scale | Broad program | Conditioner |
|---|---:|---|---|
| FLUX.1 Schnell | 11.891B | 19 joint + 38 merged blocks, width 3,072 | CLIP + T5 |
| Klein 4B | 3.876B | 5 joint + 20 merged blocks, width 3,072 | Qwen3-4B |
| Klein 9B | 9.079B | 8 joint + 24 merged blocks, width 4,096 | Qwen3-8B |
| FLUX.2 Dev | 32.223B | 8 joint + 48 merged blocks, width 6,144 | Mistral-Small-derived |

This is why the VAE result is so clarifying: an ordinary FLUX.2 VAE is about 84M parameters,
while the denoiser and conditioner range from billions to tens of billions. The VAE is not where
the family’s primary scaling budget lives.

That does not make the VAE unimportant. It means that the denoiser is the more plausible location
for most changes in conditioning behavior, trajectory shape, reference interaction, and learned
image-generation organization—provided we keep that as a working inference rather than a private
training-history claim.

### 3. The scheduler and latent state form a trajectory

The denoiser is not called once in the native FLUX recipes. The scheduler turns each prediction
into the next latent state. A four-step distilled Klein model and a 50-step base model can have the
same broad architecture while moving through very different trajectories.

The matched Klein base/distilled comparison makes this visible. The pair has the same tensor
inventory and the same ordinary VAE, but different weights and different native recipes. The
distilled system is not simply a smaller copy of the base system; its four-step path is a different
computational program over the same general body.

The 9B-to-9B-KV comparison adds another kind of state. The KV variant preserves the model’s static
architecture and VAE while adapting the denoiser and changing the reference execution path. The
reference K/V state can be extracted once and reused across later calls. That is not a VAE change,
and it is not just a parameter-count change. It is a weight-plus-interface phenotype.

This is one reason we record trajectories rather than only final images. A final image collapses a
sequence of states into one artifact. The recorder lets us ask where a difference first appears,
how it accumulates, and whether it is carried into the latent boundary.

### 4. The VAE is the latent-to-pixel boundary

The VAE consumes the final latent and renders pixels. It is a codec boundary: the denoiser works in
latent space, while downstream users usually judge the result in image space.

The exact static work established several distinct facts.

First, the ordinary FLUX.2 quartet—Klein base 4B, distilled 4B, 9B, and 9B-KV—uses the exact same
VAE tensor payloads. All six pairwise comparisons matched 251/251 tensor hashes. This is stronger
than matching a class name, parameter count, or tensor inventory. It means the behavior differences
among those four artifacts do not need to be explained by four different ordinary VAEs.

Second, FLUX.1 and FLUX.2 cross a real latent ABI boundary. FLUX.1 uses an `AutoencoderKL` with
16 raw latent channels and a 64-channel packed denoiser interface. FLUX.2 uses
`AutoencoderKLFlux2` with 32 raw channels and a 128-channel packed interface. The exact shard pass
also found 244 VAE tensors in FLUX.1 versus 251 in ordinary FLUX.2, with no equal payload hashes
among the common names.

Third, Dev preserves the ordinary FLUX.2 VAE’s 251 tensor names, shapes, and parameter count, but
250 learned/state tensors are serialized BF16→F32 and their raw payload bytes differ. The current
pass does not yet establish whether those F32 values are exactly the BF16 values cast to F32. The
correct statement is therefore “same structural envelope, not byte-identical,” not “Dev retrained
the VAE.”

The exact comparison covered seven pinned subjects and all 21 pairwise comparisons through
`mrun`, without constructing a full generator. The [complete report](../experiments/2026-08-03-141631-generative-functional-rosetta-static-decode/results/vae-shard-comparison.md)
contains the tensor-level evidence.

### 5. The decoder turns latent differences into pixel differences

The Small Decoder gives us a controlled consumer comparison. It retains the FLUX.2 latent contract
and the encoder channel topology but narrows the decoder path from `[128, 256, 512, 512]` to
`[96, 192, 384, 384]`.

The exact shard comparison adds an important correction to the phrase “retains the encoder.” It
retains the encoder topology and interface, not the original encoder weights. Relative to ordinary
FLUX.2, the Small Decoder has 250 BF16→F32 transitions, 137 shape changes, and different payload
hashes for all 251 common tensors.

The paired C6 decode experiment held the latent fixed across 96 disjoint inputs and produced 192
ordinary/small rows. The Small Decoder was roughly 1.508× faster, used about 25% less peak VRAM,
and preserved coarse structure with median coarse cosine near 0.999773. Exact pixel parity failed
for every row, and the amount of difference varied by input.

That result is not a failed model. It is an observation about a tradeoff. The latent contains
enough information for both consumers to preserve much of the same large-scale geometry, but the
decoder capacity and weights affect local detail, edges, colors, and texture. The output organ is
part of the observable model phenotype even when it is not where the denoiser formed the prompt’s
conditioning or image-level state.

## What changed across the Black Forest releases

The release sequence is not one clean scale ladder. Different transitions alter different parts of
the chain.

### FLUX.1 Schnell → FLUX.2 Klein

This is a broad system transition. The denoiser becomes much smaller and shallower, the conditioner
changes from CLIP+T5 to Qwen3, the latent interface changes, the block allocation changes, and the
native recipe moves to a four-step distilled regime. We should not attribute the resulting behavior
to one architectural knob.

### Klein base 4B → distilled Klein 4B

This is a useful matched endpoint contrast. The VAE and tensor inventory are the same, while the
weights and denoising recipe differ. It isolates trajectory and denoiser adaptation more cleanly
than a comparison that also changes the codec.

### Klein 4B → Klein 9B

This scales both the denoiser and conditioner, increases width and block depth, and changes the
joint/merged program. It is a system expansion, not a VAE expansion. The common behavior panel did
not improve monotonically with parameter count, which is another reason not to use size as a proxy
for mechanism or quality.

### Klein 9B → Klein 9B-KV

This preserves the VAE and static model geometry while changing most denoiser elements and adding a
reference K/V reuse path. The important object of comparison is the pair `(weights, interface)`,
not either one alone.

### FLUX.2 Dev

Dev scales both denoiser and conditioner into a system that needs explicit component lifetimes and
paging. Our admitted run demonstrated exact BF16 component-decoupled execution, not a complete
semantic behavior result. The VAE remains a small, separable terminal component even though the
full package is large enough that runtime ownership becomes a first-class experimental variable.

## How we learned this

The result came from layering instruments, not from assigning an architecture in advance.

### Custody and static anatomy

We pinned exact model revisions and recorded manifests, configurations, component boundaries,
tensor names, shapes, dtypes, parameter counts, and storage. The per-tensor VAE pass then read the
manifest-selected safetensors headers and hashed each tensor payload independently. This separates
package identity, tensor identity, storage precision, and latent interface.

### Runtime reconstruction

We rebuilt the stock execution path around `manalysis` and used `mrun` for model-bearing runs. The
runtime layer follows prompt state, denoiser calls, scheduler transitions, latent state, VAE state,
and pixels. For Dev, it also makes component lifetimes and paging visible.

### Recording and decoding

The recorder is an observation instrument. It captures selected runtime states and their addresses,
routes, or time positions so that we can compare trajectories and consumers. The decoder is another
observation instrument. It takes a compatible latent at a declared boundary and renders it so that
We can inspect the corresponding image-space effect.

Neither tool is an architecture theory. Neither should be used as a single scalar gate that deletes
near misses or heterogeneous rows. They make the model’s internal and output-facing state visible;
post-processing can then ask whether a trend is structural, physiological, causal, or merely an
instrument artifact.

### Controlled comparisons

We used matched releases, exact shared latents, paired decodes, repeated seeds, component swaps,
reference-K/V variants, and static tensor comparisons. The Small Decoder experiment is especially
clean because the same latent enters both output consumers. The exact shard comparison is clean in a
different way because it never constructs a generator and therefore cannot accidentally turn a
hashing question into a runtime behavior question.

### Trend-first interpretation

We kept the evidence categories separate:

- an **observation** is what a file, run, or image directly measured;
- a **trend** is a directional pattern across inputs, releases, or tools;
- a **convergent trend** survives multiple independent comparisons;
- a **working inference** is our current explanation with alternatives retained;
- a **terminal claim** is a bounded conclusion that earned its end-stage controls.

The Small Decoder’s failed pixel-parity gate therefore remains evidence of a systematic, input-
dependent tradeoff. It is not evidence that the decoder is useless. Likewise, Dev’s raw BF16/F32
payload difference is an exact serialization observation, not yet evidence of a learned numerical
change.

## Where the recorder and decoder fit in the larger program

The chain gives us a natural experimental coordinate system.

1. Record the conditioner output and denoiser trajectory under a fixed prompt, seed, and recipe.
2. Locate where two releases or interventions first diverge.
3. Persist the latent at the exact VAE boundary, including packing, dtype, scaling, and
   denormalization metadata.
4. Decode the same latent with one or more compatible consumers.
5. Compare the resulting images using several independent measurements: coarse structure, frequency,
   edges, color statistics, perceptual similarity, and downstream task behavior.
6. Relate the output trend back to the recorded internal trajectory without treating correlation as
   causation.

This allows us to ask increasingly precise questions:

- Did a release change the conditioner, the denoiser, or only the recipe?
- Did an intervention alter the latent, or did it merely alter a downstream render?
- Does a denoiser difference survive the same decoder?
- Does a decoder difference matter only for local detail, or does it change a downstream semantic
  measurement?
- Is a Dev artifact’s VAE change a storage policy or a value change?

The tools are valuable because they let us postpone those interpretations until after the data is
visible.

## What this explains—and what it does not

The current evidence supports a strong systems-level picture:

- FLUX is a family of dense, attention-based rectified-flow image systems in the inspected cohort.
- The conditioner, denoiser, scheduler/latent trajectory, and VAE decoder are separable measurement
  surfaces.
- Most cross-release scaling and adaptation occurs in the denoiser, conditioner, recipe, or
  reference interface rather than in the ordinary FLUX.2 VAE.
- The VAE is a stable architectural boundary, but not one universally byte-identical set of weights
  across every release.
- The output consumer changes the observable image even when the latent is held fixed.
- The complete model phenotype includes the consumer and execution interface, not only the denoiser
  checkpoint.

It does not yet explain:

- what a latent coordinate means semantically;
- how BFL trained or distilled the private models;
- whether Dev’s F32 VAE is numerically just a cast of ordinary FLUX.2;
- which internal denoiser route causes a particular concept or image feature;
- whether Small Decoder differences are perceptually important across a broad distribution;
- whether these findings generalize to unmeasured BFL releases.

Those are not reasons to collapse the architecture back into a vague “black box.” They are the next
questions, now expressed at the right boundaries.

## The next experiments

The immediate static control is a normalized Dev comparison: decode common ordinary-FLUX.2 BF16
payloads to F32 and compare the numeric arrays with Dev’s F32 tensors. That separates a serialization
policy change from a value change.

The immediate runtime program is a prompt-to-pixel mediation panel. We should hold prompts, seeds,
and recipes fixed; record conditioner state, denoiser trajectory, scheduler transitions, and final
latents; then decode those latents through compatible consumers and retain the full image-space
distribution instead of only a pass/fail score.

The longer-term goal is a release physiology passport: exact anatomy, trajectory shape, interface
sensitivity, output-consumer behavior, intervention response, execution cost, and instrument health
for each pinned model. That would let us compare generations without pretending that release order
alone reveals a genealogy.

## Conclusion

The Black Forest models now look less like isolated checkpoints and more like a family of coupled
computational systems. Their evolution moves several things at once: context production, denoiser
width and depth, denoising schedule, latent ABI, reference state, component lifetime, and output
decoding.

The VAE work gave us the cleanest boundary in that system. Four ordinary FLUX.2 releases share the
same VAE bytes. FLUX.1 crosses a latent and codec boundary. Dev preserves the structural envelope
but changes storage representation. Small Decoder proves that a cheaper output organ can preserve
coarse geometry while changing local pixels.

That is the level at which we can start to truly understand these models: not by asking whether a
single score went up, and not by imposing a favorite architecture on incomplete evidence, but by
following state from conditioner to denoiser to latent to decoder and measuring what each boundary
does.

## Follow-up: making the boundaries executable

The next experiment turns this static picture into an observation surface across all six pinned
FLUX.2 subjects: [FLUX.2 logical decomposition v1](../../experiments/2026-08-03-180000-flux2-logical-decomposition-v1/results/ANALYSIS.md).
It records the native conditioner, initial latent, every declared joint/single denoiser port,
scheduler transition, VAE boundary, rendered artifact, and the KV reference path where applicable.
The result is deliberately a decomposition of observed boundaries, not a claim that the model's
semantics have been cleanly separated.
