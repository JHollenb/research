---
title: "The Model as Software: Removing Confounds, Tracing Resolution, and Building a Shared Evidence Graph"
subtitle: "How a same-device donor map turned the FLUX decoder into a debuggable component and connected recorder addresses to downstream consumers and pixels"
author: codex
type: blog
subtype: model-as-software-debugging-arc
date: 2026-08-05
created: "2026-08-05T12:06:15-07:00"
status: work-in-progress
claim_status: observations-trends-and-working-inferences
epistemic_status: placement-controlled-propagation-and-route-divergence-measured-semantic-meaning-open
direction_status: undetermined
tags:
  - blog
  - wip
  - model-understanding
  - model-analysis
  - generative-models
  - image-generation
  - flux
  - black-forest-labs
  - model-as-software
  - software-components
  - recorder
  - decoder
  - component-debugging
  - execution-hypergraph
  - consumer-tracing
  - distributed-execution
  - resolution
  - donor-map
  - evidence-graph
  - trend-first
source_docs:
  - ../../experiments/2026-08-05-001500-flux-evidence-graph-donor-map/README.md
  - ../../experiments/2026-08-05-001500-flux-evidence-graph-donor-map/results/SAME_DEVICE_TRENDS.md
  - ../../experiments/2026-08-05-001500-flux-evidence-graph-donor-map/results/RESOLUTION_ANALYSIS.md
  - ../../experiments/2026-08-05-001500-flux-evidence-graph-donor-map/results/same-device-donor-map.json
  - ../../experiments/2026-08-05-001500-flux-evidence-graph-donor-map/results/resolution-1024.json
  - ../../experiments/2026-08-05-001500-flux-evidence-graph-donor-map/results/latent-resize.json
  - ../../experiments/2026-08-05-001500-flux-evidence-graph-donor-map/results/evidence-graph/shared-evidence-graph.json
  - ../../manalysis/src/manalysis/generative/execution_debug.py
  - ../../manalysis/src/manalysis/generative/component_debug.py
  - ../../manalysis/src/manalysis/generative/distributed_execution.py
  - ../../manalysis/src/manalysis/generative/distributed_debug.py
related:
  - "[[2026-08-04-182551-from-the-plane-to-a-debuggable-model|From the Plane to a Debuggable Model]]"
  - "[[2026-08-04-220500-the-boundary-became-a-debugger|The Boundary Became a Debugger]]"
  - "[[2026-08-04-000320-how-we-built-a-logically-divided-image-generative-model|How We Built a Logically Divided Image-Generative Model]]"
  - "[[2026-08-04-112441-where-we-are-with-the-disassembled-image-model|Where We Are With the Disassembled Image Model]]"
  - "[[2026-08-04-150000-one-character-five-worlds-flux|One Character, Five Worlds: Debugging Character Pinning in FLUX]]"
  - "[[2026-08-03-a-decoder-that-watches-compression|A Decoder That Watches Compression]]"
  - "[[../tools/generative-model-debugger|Generative Model Debugger]]"
  - "[[../tools/mrun-recorder-decoder|manalysis Recorder and Decoder]]"
  - "[[../black-forest-labs-model-wiki|Black Forest Labs Model Wiki]]"
  - "[[../experiments/bfl-flux2-lineage-sweep|BFL FLUX.2 Lineage Sweep]]"
  - "[[../indexes/generative-model-analysis|Generative Model Analysis Index]]"
---

# The Model as Software: Removing Confounds, Tracing Resolution, and Building a Shared Evidence Graph

There is a difference between saying that a model has components and being able to debug one.

The first statement is architectural. We can look at a checkpoint, identify a text encoder, a
denoiser, a scheduler, a VAE, and a renderer, and draw boxes around them. The second statement is
operational and scientific. It asks whether a component has an observable interface, whether its
input and output can be captured, whether a change can be replayed without changing the rest of the
system, and whether we can follow that change through the consumers that use it.

This experiment was about crossing that second threshold for FLUX.

We started from the recent arc that moved from the plane, to a logically divided image generator,
to a component debugger. The immediate question was no longer “can we draw a better architecture?”
It was:

> Can we treat the model as running software, make controlled edits at its interfaces, trace the
> resulting state through its consumers, and retain enough provenance that another run can be
> compared without guessing what changed?

The answer is now yes at the level of the instrumented execution. The semantic interpretation of
those interfaces remains open, which is exactly why the instrument matters.

## The software framing

Our working object is not a checkpoint viewed as a bag of tensors. It is a parameterized program
whose execution depends on the prompt, reference images, seed, scheduler state, device placement,
precision, and runtime policy.

For an image generator, the live computation is approximately:

```text
prompt + reference images
             │
             ▼
       conditioner
             │ context
             ▼
     denoiser trajectory ◄──── scheduler state transition
             │ prediction
             ▼
       final latent
             │
             ▼
        VAE decoder
             │ decoded tensor
             ▼
       renderer / pixels
```

That diagram becomes a software architecture only when its arrows have contracts. A useful
boundary record includes, where available:

- the component and implementation version;
- the producer and consumer;
- shape, dtype, device, layout, and packing convention;
- the trajectory position, call number, scheduler step, and seed;
- the actual input and output summaries or hashes;
- the intervention that changed the state;
- the downstream stages that saw the change; and
- the rendered or decoded artifact produced at the end.

This is why the recorder, decoder, and debugger are not interchangeable.

The recorder gives us a stable address in the live trajectory. In FLUX.2, an address can look like
`single.1/call=3/cell=5`. The decoder gives us a way to inspect a tensor at a boundary and carry it
through a fixed downstream component. The debugger joins those observations with module execution,
interventions, consumers, and outputs. The shared evidence graph then makes the whole path
queryable.

The software language is useful because it gives us concrete questions: what is the API, what is the
state, what is the call site, what is the test fixture, what is the regression, and what is the
first consumer that changes? It does not give us permission to assume that a physical software
boundary is already a semantic organ. A residual block can be a perfectly real callable component
without being “the identity module.”

## The experiment in one picture

The experiment used the cached `black-forest-labs/FLUX.2-klein-4B` artifact at revision
`e7b7dc27f91deacad38e78976d1f2b499d76a294`.

The main architecture under test was:

```text
                         ┌──────────────────────────────┐
prompt/reference ──────► │ conditioner + denoiser        │
                         │ trajectory / recorder address │
                         └──────────────┬───────────────┘
                                        │ final latent
                                        ▼
                         ┌──────────────────────────────┐
                         │ VAE boundary                  │
                         │                                │
                         │ residual block                 │
                         │   main branch ─┐              │
                         │   shortcut ────┴─► merge       │
                         │                  │             │
                         │       residuals / upsamplers  │
                         │                  │             │
                         │             decoder tail       │
                         └──────────────────┬─────────────┘
                                            │
                                            ▼
                                    decoded tensor / image
```

The debugging architecture sat beside it:

```text
static component contract + recorder address
                    │
                    ▼
             intervention / replay
                    │
                    ▼
        component IO and consumer trace
                    │
                    ▼
       execution hypergraph + path metrics
                    │
                    ▼
          latent / decoded / rendered output
                    │
                    ▼
             shared evidence graph
```

The model is still the model. The debugger is an observation and intervention layer around it. That
separation matters: it lets us change the instrument without pretending we changed the learned
architecture.

## Why we removed the placement confound

The earlier shortcut-donor experiment used a useful distributed placement, but its VAE replay mixed
CUDA and CPU execution. That left an ambiguity. If a donor branch changed the decoded image, how
much of the change came from the donor and how much came from device or precision behavior?

We therefore ran the new donor map with a hook-free standalone VAE resident on `cuda:0`. The source
specimens were captured from three matched trajectories. Every control replay and every donor replay
used the same BF16 VAE on the same CUDA device.

The final run, `job-a2aacc5c10d7`, measured:

- 283 intervention arms;
- 3 seeds: `84101`, `84102`, and `84103`;
- 7 selected residual blocks;
- peak RSS of 32.55 GB;
- peak VRAM of 8.55 GB; and
- `cuda:0` for every captured decode event and donor arm.

This does not prove that CPU and CUDA are equivalent. It answers a narrower and more useful
question: within the donor comparison, did the placement change? No. The control and intervention
are now paired on one device.

We also corrected the execution path to cache the unmodified VAE suffix once per `(seed, block)`.
That changed the experiment from repeatedly recomputing the same control for every arm into a
normal software test pattern: build the fixture once, replay the counterfactuals against it, and
retain the control as a named reference.

## The donor map

The central donor surface was the shortcut of:

```text
decoder.up_blocks.1.resnets.0
```

For a primary shortcut (x_p), donor shortcut (x_d), spatial mask (M), and dose
(alpha), the intervention was:

\[
x_{patch} = x_p + \alpha M \odot (x_d - x_p).
\]

For each downstream stage (k), we recorded a local propagation ratio:

\[
R_k = \frac{\lVert y^{patch}_k - y^{control}_k \rVert_2}
           {\lVert x_{patch} - x_p \rVert_2}.
\]

This is a diagnostic ratio, not a semantic score. It is affected by width, normalization,
upsampling, representation, and the chosen coordinate system.

The 283 arms were divided into six families:

| family | arms | purpose |
|:---|---:|:---|
| complete 8×8 spatial field | 192 | Every cell in a small spatial panel, across three seeds. |
| neighboring-block panel | 72 | Whether the effect is local to one residual block or repeated across scales. |
| dose ladder | 5 | Whether response changes continuously with intervention magnitude. |
| wrong-donor controls | 5 | Shifted, zero, main-branch, and alternate-seed controls. |
| channel-specific | 4 | Heterogeneity across channel quarters. |
| region-specific | 5 | Heterogeneity across coarse spatial regions. |

The VAE execution tracer added an independent static/live inventory of 138 events, 124 modules, and
276 hypergraph edges. The donor map then attached actual interventions to that execution surface.

## What the donor map showed

The cleanest trend is the dose response. For the central tile, terminal movement rose smoothly:

| dose | source ΔL2 | terminal ΔL2 |
|---:|---:|---:|
| 0.25 | 266.84 | 11.02 |
| 0.50 | 533.67 | 22.24 |
| 0.75 | 800.45 | 33.00 |
| 1.00 | 1,067.33 | 42.95 |
| 1.25 | 1,334.14 | 52.19 |

The decoder suffix is therefore responsive to the injected carrier in a continuous, dose-like way.
That is a useful software test result: the patched input is not being silently discarded. It still
does not tell us what the tile means.

The consumer path is more interesting than the terminal score. In the full matrix, the median
local ratio was approximately:

| consumer | median local ratio |
|:---|---:|
| `decoder.up_blocks.1.upsampler.0` | 6.31 |
| `decoder.up_blocks.2.upsampler.0` | 13.97 |
| `decoder.up_blocks.3.resnets.0` | 10.85 |
| `decoder.tail.norm` | 0.25 |
| `decoder.tail.conv_out` | 0.034 |

The perturbation expands in intermediate representation space and is then compressed at the
decoder tail. Calling this “amplification” without qualification would be misleading. The safer
description is that the internal representation changes scale as it passes through consumers.

The strongest spatial tile varied by seed: `coarse_tile_06_07` for seed 84101,
`coarse_tile_05_01` for seed 84102, and `coarse_tile_07_06` for seed 84103. That variation is
important. It gives us leads for a denser map, but not a stable semantic coordinate system.

The wrong-donor controls span a broad range. Shifted donors produced terminal ΔL2 values around
207–220; an alternate seed produced about 398; zero and main-branch donors produced about 495. The
VAE is sensitive to the donor choice, but the response is not one-dimensional. A single broad RGB
score would erase exactly the distinctions we need to investigate.

## Why we traced native 1024

The next question was resolution. If a 512 latent is enlarged to 1024 and decoded, do we get the
same thing as running the model natively at 1024?

We compared three routes:

```text
A. native 1024 trajectory → native 1024 latent → VAE → image
B. native 512 trajectory → image resize → 1024 image
C. native 512 trajectory → bilinear latent resize → VAE → 1024 image
```

The latent resize operator was explicit:

```text
torch.nn.functional.interpolate(
    latent,
    mode="bilinear",
    align_corners=False,
)
```

It transformed `[1, 32, 64, 64]` into `[1, 32, 128, 128]`. The shape was valid, but the route was
not equivalent to native generation. Relative to native 1024, the bilinear-latent image had a
mean absolute pixel difference of 51.43/255. The image-resized 512 reference differed by
50.10/255.

The recorder and consumer trace localized another part of the story. At
`single.1/call=3/cell=5`, the late-cell perturbation was preserved at the local block output but
was attenuated to roughly 3–4% of its source L2 at the prediction boundary. The VAE still turned
the resulting latent change into a broad image change.

The current working inference is therefore that the resolution artifact is not simply a VAE
problem and not simply a final image-resize problem. Native high resolution selects a different
trajectory state upstream of the decoder. The exact distortion mechanism remains an open seam for
the debugger.

## The shared evidence graph

Separate reports are useful while an experiment is being designed. They become limiting once we
need to follow one question across experiments. We therefore normalized the donor, native 1024,
and latent-resize reports into one graph.

The graph contains nodes for:

- runs and model artifacts;
- recorder addresses and intervention arms;
- trajectory positions and consumer boundaries;
- latent and decoded tensor boundaries;
- fixed operators such as latent interpolation;
- execution hypergraphs; and
- rendered outputs and flipbooks.

Its core path is:

```text
recorder address
      ↓
intervention arm
      ↓
consumer trajectory
      ↓
latent boundary
      ↓
decoded tensor
      ↓
rendered output
```

The completed graph has 4,645 nodes and 5,211 edges across the three runs. It includes a cross-route
link between the interpolated-latent output and the native 1024 reference.

This is the architecture that has actually formed so far: an evidence architecture. It is not a
claim that the VAE hypergraph is the model's semantic architecture. It is a way to preserve the
relationships needed to discover whether such an architecture exists.

## How to re-run the work

The workspace is:

`/Users/jakeholl/domains/experiments/2026-08-05-001500-flux-evidence-graph-donor-map`

The real-model commands use `mrun` internally. They request CUDA, use local/offline model custody,
run strict preflight, and use the measured donor reservation of 32 GB RAM and 11 GB VRAM. The
accelerator lanes should remain serial; the point is to preserve valid telemetry and provenance,
not to create competing runs on one GPU.

```bash
cd /Users/jakeholl/domains/experiments/2026-08-05-001500-flux-evidence-graph-donor-map

# Same-device VAE donor map: 3 seeds, 7 blocks, complete 8×8 panel, 283 arms.
python submit_same_device_donor_map.py
python submit_same_device_donor_map.py --collect JOB_ID

# Native 1024 trajectory and recorder/consumer/VAE trace.
python submit_resolution_trace.py --resolution 1024
python submit_resolution_trace.py --resolution 1024 --collect JOB_ID

# Fixed latent-resize comparator.
python submit_latent_resize_trace.py
python submit_latent_resize_trace.py --collect JOB_ID

# Compact donor trend readout.
python analyze_same_device_donor_map.py \
  results/same-device-donor-map.json \
  --output results/SAME_DEVICE_ANALYSIS.md

# Join all completed reports into the shared graph.
python build_shared_evidence_graph.py \
  --donor results/same-device-donor-map.json \
  --native results/resolution-1024.json \
  --latent-resize results/latent-resize.json \
  --output-dir results/evidence-graph
```

The raw JSON reports are intentionally kept alongside human-readable summaries. The graph builder
omits a missing source rather than converting it into negative evidence. A future run can add a
new report type without rewriting the older records.

## Why this arc matters

The earlier work established that we could physically separate FLUX into useful execution
boundaries. The character-pinning work showed that a late trajectory surface could move a rendered
image. The initial decoder work showed that a VAE residual shortcut could be replayed and followed
through downstream stages. The debugger work made those boundaries inspectable as software.

This experiment joined those pieces and changed the unit of progress.

Progress is no longer “we found a promising cell” or “the image score moved.” It is now:

1. the exact state was supplied at a typed boundary;
2. the control and intervention shared device, dtype, model, seed, and route where intended;
3. the change was measured at each downstream consumer;
4. the latent and decoded boundaries were retained separately;
5. independent output instruments remained visible; and
6. the entire path was recorded in a reusable evidence graph.

That is what treating the model as software buys us. It gives us fixtures, contracts, replay,
interventions, logs, diffs, and a place to ask where a failure begins. It also disciplines the
scientific interpretation: a component can be load-bearing without being semantically named, and a
rendered change can be real without proving the intended concept moved.

## What we know and what remains open

We now know that the instrumented FLUX execution can be decomposed into observable and replayable
boundaries. We know the VAE responds to placement-controlled donor changes, that those changes
have dose and consumer trajectories, and that native 1024 generation is not a latent-resized 512
route.

We do not yet know:

- whether any donor cell or region corresponds to character identity or a named visual attribute;
- whether the spatial pattern is stable under a denser, matched-energy panel;
- which exact denoiser operation causes the native-resolution divergence;
- whether a typed Scene State can become a causal, persistent visual object;
- whether the current logical components are semantic components; or
- whether the observed internal route generalizes across FLUX variants.

Those are not omissions in the current experiment. They are the next questions made possible by it.

The current perspective is therefore:

> A model is a trained substrate that implements context-conditioned state transitions. A run is a
> trajectory through that substrate. The useful components are the boundaries, transports, and
> consumers that can be observed and causally tested. Semantic names are conclusions to earn from
> replicated downstream behavior, not labels to place on the diagram in advance.

The model has become software in the practical sense: it can be inspected, replayed, patched,
traced, and compared. The deeper architecture is still being discovered.

## Artifacts

- [[../../experiments/2026-08-05-001500-flux-evidence-graph-donor-map/README|Experiment README]]
- [[../../experiments/2026-08-05-001500-flux-evidence-graph-donor-map/results/SAME_DEVICE_TRENDS.md|Same-device donor trends]]
- [[../../experiments/2026-08-05-001500-flux-evidence-graph-donor-map/results/RESOLUTION_ANALYSIS.md|Native-resolution analysis]]
- [[../../experiments/2026-08-05-001500-flux-evidence-graph-donor-map/results/same-device-donor-map.json|Same-device donor report]]
- [[../../experiments/2026-08-05-001500-flux-evidence-graph-donor-map/results/resolution-1024.json|Native 1024 report]]
- [[../../experiments/2026-08-05-001500-flux-evidence-graph-donor-map/results/latent-resize.json|Latent-resize report]]
- [[../../experiments/2026-08-05-001500-flux-evidence-graph-donor-map/results/evidence-graph/shared-evidence-graph.md|Shared evidence graph]]
- [[../../experiments/2026-08-05-001500-flux-evidence-graph-donor-map/results/evidence-graph/shared-evidence-graph.json|Shared evidence graph JSON]]

