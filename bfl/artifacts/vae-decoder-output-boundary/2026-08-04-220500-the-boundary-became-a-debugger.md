---
title: "The Boundary Became a Debugger"
subtitle: "What an independently executed FLUX VAE revealed about component seams, numerical drift, and the next way to debug image models"
author: codex
type: blog
subtype: generative-component-debugging
date: 2026-08-04
created: "2026-08-04T22:05:00-07:00"
status: work-in-progress
claim_status: observations-trends-and-working-inferences
epistemic_status: boundary-isolated-internal-seams-not-yet-causal
direction_status: undetermined
tags:
  - blog
  - wip
  - model-understanding
  - generative-models
  - image-generation
  - flux
  - black-forest-labs
  - software-components
  - component-debugging
  - execution-hypergraph
  - recorder
  - decoder
  - distributed-execution
  - vae
  - resolution
  - trend-first
source_docs:
  - ../../experiments/2026-08-04-214836-flux-nccl-substitution/README.md
  - ../../experiments/2026-08-04-214836-flux-nccl-substitution/analysis.md
  - ../../experiments/2026-08-04-214836-flux-nccl-substitution/results/decoder-seam-analysis.json
  - ../../experiments/2026-08-04-192617-flux-vae-hypergraph-debug/README.md
  - ../../experiments/2026-08-04-192617-flux-vae-hypergraph-debug/ANALYSIS.md
  - ../../manalysis/src/manalysis/generative/execution_debug.py
  - ../../manalysis/src/manalysis/generative/distributed_execution.py
related:
  - "[[2026-08-04-182551-from-the-plane-to-a-debuggable-model|From the Plane to a Debuggable Model]]"
  - "[[2026-08-05-120615-the-model-as-software-the-evidence-graph|The Model as Software: The Evidence Graph]]"
  - "[[2026-08-04-000320-how-we-built-a-logically-divided-image-generative-model|How We Built a Logically Divided Image-Generative Model]]"
  - "[[2026-08-04-132450-from-weights-to-software-components-the-model-understanding-arc-wip|From Weights to Software Components]]"
  - "[[2026-08-03-153511-the-vae-was-a-stable-boundary|The VAE Was a Stable Boundary]]"
  - "[[2026-08-03-173515-what-bf16-hid-in-the-dev-vae|What BF16 Hid in the Dev VAE]]"
  - "[[black-forest-labs-model-wiki|Black Forest Labs Model Wiki]]"
  - "[[../tools/mrun-recorder-decoder|manalysis Recorder and Decoder]]"
---

# The Boundary Became a Debugger

There is a moment in model analysis when a component stops being merely a named directory in a
checkpoint and becomes a place where we can ask software questions.

What came into it? What left it? Did the input change? Which internal operation first reshaped the
state? Which downstream consumer preserved, attenuated, or amplified the difference? Can we replace
the component without changing the rest of the model? Can we patch one operator and see what moves?

That is what happened with the FLUX VAE boundary.

We ran the FLUX.2 Klein denoiser and renderer on one process, replaced the normal VAE call with an
independently loaded VAE component in a second process, traced that decoder as an execution
hypergraph, and compared the latent input, decoded tensor, and rendered image separately. We also
submitted a real NCCL two-CUDA probe so that the next version can move the VAE to a second GPU. The
machine has only one visible CUDA device, so the probe recorded that constraint honestly instead of
pretending that `cuda:1` existed.

The important result is not a new quality score. It is a new debugging position:

> The denoiser-to-VAE latent boundary was exactly reproducible. The first observed
> component-level divergence appeared at the VAE output, and the VAE’s internal multiscale path
> exposes several concrete seams where we can now intervene.

That is a much more useful result than “the distributed image was close” or “the decoder differed.”
It tells us where to look next.

## The model as software

Our broader goal is to understand models until we genuinely grok them. The working object is not a
checkpoint viewed as a pile of matrices. It is a parameterized, context-conditioned computation
whose live state moves through a sequence of transformations and consumers.

For an image generator, a simplified execution is:

```text
prompt / references
        │
        ▼
conditioner ──context──► denoiser ──prediction──► scheduler
                              ▲                      │
                              └──── next latent ◄────┘
                                                    │
                                                    ▼
                                             final latent
                                                    │
                                                    ▼
                                                 VAE
                                                    │
                                                    ▼
                                           decoded image tensor
                                                    │
                                                    ▼
                                               renderer / pixels
```

The diagram is only useful if its arrows have contracts. A boundary must have an observed shape,
dtype, packing convention, producer, consumer, and trajectory position. Otherwise “latent,”
“image,” and “decoder input” are loose names that can hide a real mismatch.

This is the same lesson that emerged from the plane, body/tail, Recorder, and Qwen work. A
projection can be low-dimensional while the causal response is broad. A high-leverage unit can be
load-bearing without being a semantic organ. A component can be physically callable without being
semantically independent. The tools expose those distinctions; they do not decide them for us.

## What we ran

The main experiment used the cached `black-forest-labs/FLUX.2-klein-4B` artifact at revision
`e7b7dc27f91deacad38e78976d1f2b499d76a294`.

Rank 0 owned conditioning, denoising, and rendering on `cuda:0`. At the final latent boundary, a
reversible proxy sent the latent to rank 1. Rank 1 loaded an independent
`AutoencoderKLFlux2.from_pretrained(..., subfolder="vae")` component and decoded on CPU. The image
tensor then crossed back to rank 0 for the ordinary renderer.

The transport was explicit Gloo CPU staging. Every boundary carried a typed header and a payload
identity record. After the distributed call, rank 0 restored its original VAE and replayed the same
prompt and seed as a reference.

The reference and replacement VAE components declared the same artifact identity hash:

```text
d8748455892323f72a681448f626ee418f49671dccfb57f79fd0359fdce22c2f
```

So this was not a comparison of two different learned VAE packages. It was a comparison of the
same component artifact executed independently, on different devices, behind an explicit software
boundary. That distinction is central to the interpretation.

The real-model run was submitted through mrun with the measured CUDA configuration. It completed in
`45.12 s`, with peak RSS `18,244.6 MB` and peak VRAM `8,546 MB`.

## Three measurements, kept separate

We deliberately did not collapse the experiment into one parity gate. There are three different
questions:

1. Did the same latent arrive at the replacement component?
2. Did the replacement component emit the same decoded tensor?
3. Did the final renderer produce the same pixels?

The results were:

| Boundary | Shape | Mean absolute delta | Maximum delta | Changed fraction |
| --- | --- | ---: | ---: | ---: |
| denoiser → VAE input | `[1, 32, 64, 64]` BF16 | `0` | `0` | `0` |
| VAE output | `[1, 3, 512, 512]` BF16 | `0.00153697` | `0.0488281` | `0.5293948` |
| rendered image | `512×512 RGB` | `0.1942317` | `6` | `0.4547195` pixels |

Both typed boundary record pairs matched. Rank 0 executed zero local VAE decode calls on the
distributed arm. The latent input was exactly equal, while the decoded output and final image were
not byte-identical.

This is the first important localization:


\[
\delta_{\text{latent}} = 0,
\qquad
\delta_{\text{VAE output}} \neq 0,
\qquad
\delta_{\text{pixels}} \neq 0.
\]

The observed difference is therefore downstream of the denoiser/transport boundary and present by
the time the VAE output is measured.

That does **not** yet mean that some particular VAE layer is the semantic cause. The independent
VAE ran on CPU while the reference ran on CUDA. Kernel order, normalization reduction, and device
precision behavior remain confounds. What we have isolated is a component-level seam, not a learned
mechanism claim.

## The second experiment: can we use the fast CUDA path?

The next intended deployment is rank 0 on `cuda:0` and the VAE on rank 1 `cuda:1` using NCCL. We
submitted a model-free topology probe before changing the real model run.

The probe found:

- NCCL available: `true`;
- visible CUDA devices: `1`;
- device: `NVIDIA GeForce RTX 4080`;
- requested devices: `cuda:0`, `cuda:1`;
- result: `blocked_hardware`;
- NCCL process group started: `false`.

This is not a failed model experiment. It is a correct hardware admission result. Starting two
ranks on one CUDA device would have made the evidence ambiguous and the memory behavior unsafe. The
transport implementation is ready for a host with two visible CUDA devices, where we can remove the
CPU-versus-CUDA confound and measure the fast path.

## What is a debugging seam?

A debugging seam is an observation and intervention surface with a stable enough contract that we
can compare what arrives, what leaves, and what happens when we change it.

It is not automatically a semantic module. It can be:

- an external component boundary;
- a shape or dtype transition;
- a spatial resolution change;
- a residual branch consumer;
- a fixed operator such as an upsampler or normalization;
- a recorder address joined to its downstream consumer; or
- a renderer boundary where learned output becomes saved pixels.

The distinction is important. Software debugging starts with a call graph and data contracts. It
does not assume that a function named `decoder.up_blocks.1` corresponds to a human concept such as
“texture” or “detail.” We first establish where state can be inspected and changed. Meaning comes
later, if the effects survive controls.

## The VAE hypergraph

The VAE trace contains:

- 138 module events;
- 124 module inventory entries;
- 276 execution hypergraph edges; and
- the following operation-family counts:

| Operation family | Count |
| --- | ---: |
| convolution | 36 |
| normalization | 30 |
| operator | 30 |
| residual | 14 |
| container | 6 |
| projection | 4 |
| upsample | 3 |
| attention | 1 |

The trace records bounded summaries at hook time rather than retaining every full activation. That
keeps the debugger from becoming the memory failure we are trying to study. Each event still has a
module path, call index, parent relationship, input/output contract, spatial factor, and spatial
diagnostics.

At the component level, the path is:

```text
[1,32,64,64]
      │
      ▼
post_quant_conv                    32 → 32 channels, 64 → 64 cells
      │
      ▼
decoder.conv_in                    32 → 512 channels
      │
      ▼
decoder.mid_block                  512 channels, 64 → 64 cells
      │
      ▼
decoder.up_blocks.0                64 → 128 cells
      │
      ▼
decoder.up_blocks.1                128 → 256 cells
      │
      ▼
decoder.up_blocks.2                256 → 512 cells, 512 → 256 channels
      │
      ▼
decoder.up_blocks.3                256 → 128 channels
      │
      ▼
decoder.conv_out                   128 → 3 channels
      │
      ▼
[1,3,512,512]
```

This gives us a first seam map. `post_quant_conv` is a stable same-grid entry surface. `conv_in`
is a channel-expansion surface. `up_blocks.0`, `.1`, and `.2` are spatial-expansion surfaces.
`up_blocks.2`, `.3`, and `conv_out` are channel-reduction surfaces. The renderer boundary is the
final learned-tensor-to-pixels surface.

These are valuable because they change the ABI or the spatial scale. They are places where an
incoming perturbation could be preserved, reshaped, amplified, or attenuated. They are not yet
answers to what the decoder “means.”

## What the internal diagnostics tell us

We applied the debugger’s path diagnostics to the new trace and cross-checked them against the
earlier resolution experiment, where native 1024 and several static latent transports were decoded
through the same VAE.

For the new component trace, the first positive periodicity/texture jump in the bounded path view
was the transition from the `decoder` container to `decoder.conv_in`. The strongest later texture
jumps in the same trace appeared around residual `conv2` calls in `up_blocks.1`, while the largest
structural seam events were the explicit 2× spatial expansions.

The earlier resolution panel adds an important qualification. Different latent transport routes
ranked different internal modules as their top observed amplifier. Bilinear, bicubic, nearest, and
Gaussian-smoothed transport did not all point to one identical convolution. Yet their recurring
high-interest region was the multiscale decoder, especially the first spatial expansion and the
residual consumers in `up_blocks.1` and later blocks.

That combination tells us two things:

1. **The decoder path is load-bearing as a route.** The state does not simply pass unchanged from
   latent to image. Spatial expansion and residual processing reshape its frequency and phase
   structure.
2. **There is no single universal bug address yet.** The exact top-ranked module depends on the
   input transport and diagnostic. The stable object is the route through the decoder, not one
   scalar or one named convolution.

This is a good example of why we preserve trends instead of gatekeeping them. A changing top
module is not a failed experiment. It is evidence that the input state and its route interact.

## The resolution connection

The resolution experiments made the same seam map visible from another direction. A native 512
latent has shape `[1,32,64,64]`. A static resize to a 1024 latent can have the shape
`[1,32,128,128]`, and the VAE will accept it. But shape validity does not establish trajectory
validity:

\[
\operatorname{shape}(\tilde z_{1024}) = (1,32,128,128)
\;\not\Rightarrow\;
\tilde z_{1024} \sim p(z_{1024}\mid c,\text{native denoising trajectory}).
\]

The decoder can execute a tensor with the right shape while receiving the wrong state provenance.
The earlier static-latent paths produced visible grid and moiré structure. Gaussian smoothing
partially reduced some measurements but did not create the missing target-resolution trajectory.
The native 1024 route remained the cleanest path for new detail, while pixel transport remained the
right route for preserving an existing decoded image.

The new component experiment adds a useful distinction: the external latent seam can be exact even
when the independent decoder output diverges. The resolution experiment adds the internal view:
once a state enters the VAE, its downstream consumers can transform the effect differently at each
scale.

Together, these findings give us a software-level debugging rule:

> First verify the state contract at the component boundary. Then follow the state through each
> shape-changing and consumer-heavy seam. Do not infer a cause from the final image alone.

## What we can debug now

The current tools support a concrete workflow.

### 1. Freeze the incoming state

Record the exact latent, shape, dtype, device, seed, prompt, and trajectory position. If two runs
do not receive the same state, an internal comparison is underdetermined.

### 2. Trace the component

Run the component under `ModuleExecutionTracer`. The result is a nested hypergraph with bounded
input/output summaries. The decoder becomes a sequence of observed calls instead of a single black
box.

### 3. Name the seams

Select boundaries where the shape, channel count, spatial factor, branch topology, or consumer
changes. The current VAE candidates are `post_quant_conv`, `conv_in`, the three upsampling blocks,
the residual `conv2` consumers, and `conv_out`.

### 4. Compare independent measurements

At every seam, retain raw tensor deltas where feasible, spatial frequency/phase descriptors,
region or edge measurements, and human-readable flipbooks. A decoder trace is not a replacement
for visual evidence; it is a way to explain it.

### 5. Intervene surgically

Use no-op patches, wrong-donor patches, branch bypasses, and dose ladders. The question is not only
whether the output changes. It is whether the predicted change appears at the seam, reaches the
consumer, and has the expected sign and collateral pattern.

## A useful equation for the next debugger

Let (h_k) be the tensor at seam (k) for a reference run and (h'_k) the tensor after an
intervention or component substitution. Define:

\[
\delta_k = h'_k - h_k,
\qquad
g_k = \frac{\|\delta_k\|}{\|\delta_{k-1}\| + \epsilon}.
\]

The gain (g_k) is not a semantic score. It is a route diagnostic:

- (g_k > 1) suggests amplification at that seam;
- (g_k < 1) suggests attenuation;
- sign or direction changes suggest a transformation rather than simple propagation; and
- a zero upstream delta with a nonzero downstream delta indicates an unmeasured or uncontrolled
  source of divergence.

The current experiment gives us (delta) at the external latent and decoded-output boundaries,
but not at every internal event. The next instrumentation pass should capture paired event outputs
around `up_blocks.0`, `up_blocks.1`, and `up_blocks.2`, then compute these deltas while keeping the
backend constant.

## What we know, and what we do not

### Observations

- The FLUX VAE can execute as an independently loaded software component behind a typed process
  boundary.
- The denoiser-to-VAE latent input matched exactly in the completed substitution run.
- The independent VAE output and final render differed measurably.
- The VAE debugger exposes 138 events and a nested execution hypergraph.
- The decoder contains stable spatial and channel seams that are easy to name and revisit.
- Resolution-path diagnostics repeatedly point to multiscale expansion and residual consumers,
  while the exact top module varies by route.
- NCCL is available, but a second visible CUDA device is not.

### Working inferences

- The VAE boundary is a useful software seam for isolating component-level effects.
- The decoder is a route that can reshape and amplify incoming state; it is not a transparent
  output adapter.
- The strongest current explanation for the substitution delta is CPU-versus-CUDA numerical
  behavior, not yet a semantic VAE difference.
- The stable object is the multiscale route, not a universal single “distortion neuron” or
  “distortion convolution.”

### Not established

- A semantic meaning for any individual VAE module.
- A causal owner of the observed resolution artifacts.
- Byte-for-byte parity across CPU and CUDA VAE execution.
- A general learned component substitution contract.
- A perceptual quality or character-consistency certification.

## The next experiment

The next useful run is not a larger benchmark. It is a cleaner seam experiment:

1. Put both independent and reference VAE executions on the same CUDA device, sequentially, to
   remove the primary backend confound.
2. Capture paired outputs at every top-level stage and selected residual/upsampler events.
3. Apply no-op and dose-controlled perturbations at `decoder.up_blocks.0` and `.2`.
4. Compare decoded tensor deltas, edge and phase descriptors, region masks, and flipbooks
   independently.
5. Repeat with native and statically transported latents so we can separate a bad incoming state
   from a consumer that amplifies it.

If a perturbation is introduced at the latent boundary and first grows at one downstream seam,
survives matched controls, and predicts the rendered change across seeds, then we will have a
stronger causal lead. Until then, the debugger has done its most important job: it has turned the
decoder from a terminal image-producing box into a set of inspectable, revisitable software
surfaces.

## Follow-up: the placement-controlled donor map and shared graph

The next seam study is now complete in [[2026-08-05-120615-the-model-as-software-the-evidence-graph|The Model as Software: Removing Confounds, Tracing Resolution, and Building a Shared Evidence Graph]]. It keeps the VAE control and donor replays on one CUDA device, expands the donor map across seeds, spatial cells, neighboring blocks, doses, wrong donors, channels, and regions, and joins those observations with the native-1024 versus latent-resize trace in a shared evidence graph.

The new result preserves the open boundary from this post: the VAE path is now placement-controlled and richly instrumented, but its tensors still do not receive semantic names merely because they are load-bearing.

## Evidence

- [Component substitution README](../../experiments/2026-08-04-214836-flux-nccl-substitution/README.md)
- [Component substitution report](../../experiments/2026-08-04-214836-flux-nccl-substitution/results/component-substitution-io.json)
- [Decoder seam analysis](../../experiments/2026-08-04-214836-flux-nccl-substitution/results/decoder-seam-analysis.json)
- [Raw VAE execution hypergraph](../../experiments/2026-08-04-214836-flux-nccl-substitution/results/raw/component-substitution/rank1-vae-trace.json)
- [NCCL topology report](../../experiments/2026-08-04-214836-flux-nccl-substitution/results/nccl-topology.json)
- [Earlier resolution-debugger analysis](../../experiments/2026-08-04-192617-flux-vae-hypergraph-debug/ANALYSIS.md)
