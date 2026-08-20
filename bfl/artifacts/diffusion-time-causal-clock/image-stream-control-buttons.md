---
title: "Saturn's Image-Stream Control Panel: What Each Circuit Button Does"
subtitle: "Turning the FLUX.2 image route into a set of typed, checkpointed controls"
author: codex
type: blog
subtype: saturn-rosetta-image-stream-control-buttons
date: 2026-08-11
updated: 2026-08-11
status: measured-research-report
claim_status: bounded-image-stream-control-route
epistemic_status: native-flux2-qwen-mrun-checkpoint-replay
tags:
  - blog
  - saturn
  - rosetta
  - rosetta-stone
  - circuits
  - image-circuit
  - image-stream
  - semantic-circuit
  - control-panel
  - causal-intervention
  - checkpoint-replay
  - exact-replay
  - lexical-mapper
  - reverse-engineering
  - model-as-software
  - flux2
  - qwen
  - native-qwen
  - mrun
  - cuda
  - todo
source_docs:
  - ../../saturn/workers/run_saturn_image_control_panel.py
  - ../../saturn/workers/submit_saturn_image_control_panel.py
  - ../../saturn/src/saturn/image_control_analysis.py
  - ../../saturn/configs/rosetta-image-control-panel.json
  - ../../saturn/results/image-circuits/control-panel/job-bcbb4f9dd97b/report.json
  - ../../saturn/results/image-circuits/control-panel/job-bcbb4f9dd97b/run-receipt.json
  - ../../saturn/results/image-circuits/control-panel/job-bcbb4f9dd97b/image-control-report.md
  - ../../saturn/results/image-circuits/control-panel/job-bcbb4f9dd97b/analysis/image-control-analysis.json
  - ../../saturn/results/image-circuits/control-panel/job-bcbb4f9dd97b/analysis/image-control-analysis.md
  - ../../saturn/results/image-circuits/control-panel/job-bcbb4f9dd97b/00-appearance-montage.png
  - ../../saturn/results/image-circuits/control-panel/job-bcbb4f9dd97b/01-scene-montage.png
  - ../../saturn/results/image-circuits/control-panel/job-bcbb4f9dd97b/02-character-montage.png
  - ../../saturn/results/image-circuits/lexical/job-9ce1bd903e1b/report.json
  - ../../saturn/results/image-circuits/scene/job-1dc1d31ddc21/report.json
  - ../../saturn/results/image-circuits/character/job-6a5c4b85cd82/report.json
related:
  - "[[./2026-08-10-saturn-semantic-circuit-from-prompt-to-geometry|The Semantic Circuit: How Saturn Turned FLUX.2 Meaning into a Controllable Program]]"
  - "[[./2026-08-10-saturn-the-semantic-function-was-a-distributed-carrier|SATURN Found a Semantic Function — and It Was a Distributed Carrier]]"
  - "[[./2026-08-10-saturn-scene-circuit-token-route|The Scene Circuit: From Prompt Tokens to a Controllable Image Background]]"
  - "[[../circuits-wiki|Circuits Wiki]]"
---

# Saturn's Image-Stream Control Panel: What Each Circuit Button Does

> [!summary] The result
> We turned the strongest candidate image route into an operational control
> panel. `joint.4:image` injects an image carrier, `single.0:image` bridges it
> into the merged stream, `single.10:image` transports and amplifies it, and
> `single.19:image` closes the image readout. Null, dose, timestep, and
> checkpoint controls let us distinguish a semantic carrier from a terminal
> image write. The result is a typed, time-dependent route through the real
> FLUX.2 program—not a claim that one address is a universal semantic neuron.

The earlier Saturn experiments found a semantic circuit by comparing source and
target prompts, following their hidden-state differences, and intervening at
candidate boundaries. That work answered an important question:

> Where does a semantic contrast travel through the image stream?

This experiment asks the next, more practical question:

> What does each boundary do when we press it?

The answer matters for the Rosetta program. A circuit becomes software-like
when it has an interface, a state type, a consumer, and a measurable effect.
The control panel is our first direct interface to the discovered image route.

## The model as a program

At the resolution of these experiments, the native FLUX.2 pipeline looks like
a typed program:

```text
prompt
  → native Qwen conditioner
  → joint text/image transformer blocks
  → single merged-stream transformer blocks
  → image return register
  → real scheduler / denoiser continuation
  → native VAE
  → RGB image
```

The precise address names are Saturn's typed execution boundaries. They are not
human-readable source functions recovered from the model weights. The useful
thing is that Saturn can capture a state at one of those boundaries, restore
the exact checkpoint, replace one typed field, and run the untouched suffix.

That gives us a software-style call boundary:

```text
capture(source checkpoint)
  → replace one image-stream value
  → resume the real suffix
  → measure return-register and RGB effects
```

The denoiser, scheduler, VAE, seed, weights, and numerical execution remain
the real native components. We are not asking a learned surrogate to render
the result.

## The route we are controlling

The current working route is:

```text
joint.4:image
  → single.0:image
  → single.10:image
  → return-register / scheduler / VAE
```

The route is distributed. `joint.4` is not “the scene neuron,” and
`single.10` is not “the color neuron.” The same image-state pathway can carry
different contrasts depending on what changed in the prompt. We tested three
axes with the same source image concept:

| axis | source | target |
|---|---|---|
| appearance/color | red fox in snow | blue fox in snow |
| scene/background | red fox in snow | red fox on a beach |
| character identity | red fox in snow | red cat in snow |

The source and target were each generated through native Qwen FLUX.2 with the
same seed, resolution, number of steps, and model revision. The target run was
used as a donor trajectory. Every intervention branch started from the source
checkpoint and continued through the real native suffix.

## What a button means mathematically

Let `h^S_s(t)` be the source image-stream state at typed site `s` and denoising
step `t`. Let `h^T_s(t)` be the corresponding state from the target prompt.
For a donor dose `d`, the control panel constructs:

```text
h^B_s(t) = h^S_s(t) + d · (h^T_s(t) − h^S_s(t))
```

The branch state is then inserted only at the selected site and selected
timesteps. The rest of the model runs normally.

The main image-level score is:

```text
P = (MAD(source, branch) − MAD(target, branch)) / MAD(source, target)
```

`P > 0` means that the branch moved toward the target image. `P = 1` means the
branch reached the target image in this metric. The panel also records hidden
return-register direction and progress, because a hidden-state change can be
real while being poorly expressed by RGB—or can be a late readout effect that
should not be mistaken for semantic transport.

Nulling is separate from dose interpolation. It replaces the selected
normalized image state with zeros:

```text
h^B_s(t) = 0
```

That is an ABI/necessity probe. A broken image after nulling tells us that the
state is needed for a valid execution, but it does not by itself tell us which
meaning the state carries.

## The buttons

### `joint.4:image` — image-carrier injection

This is the earliest of the four controls in the working route. Pressing it
replaces the image half of the paired joint-stream state before the first
single-stream handoff.

Across the three semantic axes, a full target-state replacement at all four
steps produced mean target progress of `0.445`. Its mean late-step gain was
`1.069`: interventions at early steps could be source-ward, while the same
carrier became strongly targetward by the last step.

The practical interpretation is an **image-carrier injection boundary**. It
places a donor contrast into the image-side state, but downstream computation
still has to interpret and transport that contrast. A single early write is
not sufficient to guarantee a clean target image.

### `single.0:image` — cross-stream bridge

`single.0:image` is the first image boundary after the joint streams have been
merged. It receives the carrier from the paired route and exposes it to the
single-stream computation.

Its mean dose-1 target progress was also `0.445`, with a mean late-step gain of
`0.900`. This is consistent with a **cross-stream bridge**: the state is no
longer being introduced into the paired representation, but is being
integrated into the stream that later image blocks consume.

This boundary is particularly useful for the Rosetta map because it gives us a
typed handoff between two architectural regimes. In software terms, it looks
less like a semantic storage cell and more like an adapter between two data
structures.

### `single.10:image` — semantic transport and amplification

`single.10:image` is later in the merged stream and was the strongest
non-terminal control. Its mean dose-1 target progress was `0.589`, the highest
of the three non-terminal sites.

Pressing this button moved the image toward all three targets: blue fox,
beach background, and cat identity. That does not mean `single.10` contains
three independent semantic functions. It means the target contrast has become
available to a later image-state consumer, where the normal suffix can express
it more effectively in RGB.

Our working label is **semantic transport amplifier**. It is a behavioral label
for the observed state transition, not a recovered name from the weights.

### `single.19:image` — terminal image readout

`single.19:image` behaves differently. Replacing its complete image state with
the target state at dose `1.0` produced target RGB exactly for appearance,
scene, and character identity. Its mean dose-1 progress was `1.000`.

This is an important control, but it is not evidence that `single.19` is where
the semantic concept originates. It is the terminal image-state readout. If we
write the target's complete state directly at the last relevant boundary, the
remaining computation has little opportunity to do anything other than decode
that target state.

This also resolves an apparent disagreement with the earlier lexical screen.
The lexical screen injected a normalized donor **delta** and found that the
late boundary was comparatively source-preserving. The new panel injects an
absolute **target state**, and therefore demonstrates that the same boundary
can directly control the final image. One experiment identifies transport; the
other identifies terminal writeout.

### `null` — remove the image state

Nulling each candidate site produced structured noise or visibly broken images.
That is valuable because it shows the image-stream value is part of the valid
execution contract. It is not enough to call the site semantic, however.

Many useful intermediate states are necessary for a clean image without being
the place where a particular concept is represented. Null is therefore a
necessity and ABI button, not a semantic naming button.

### `dose` — turn the intervention up or down

The dose button tests whether the effect behaves like a stable linear control.
It did not.

At `joint.4`, `single.0`, and `single.10`, doses `0.25` and `0.5` were often
negative or weakly targetward. Dose `1.0` crossed into a clear targetward
effect, and dose `1.5` generally pushed farther or overshot.

This suggests that the model's valid semantic trajectory is not a straight
line through arbitrary hidden-state space. A half-strength interpolation is
not necessarily a half-strength meaning. It can land off-manifold and make
the image worse before the full donor state becomes useful.

### `timestep` — find when the button has leverage

The timestep button applies a full donor replacement at only one denoising
step. It exposes the temporal part of the circuit.

For appearance and scene, `joint.4` and `single.0` were generally source-ward
at steps `0–2` and became targetward at step `3`. `single.10` became useful
around steps `2–3`. Character identity had earlier leverage at `single.0` and
`single.10`, especially at steps `1–2`.

The semantic circuit is therefore not just a set of addresses. It is a
space-time route:

```text
boundary × denoising step → downstream state → image
```

This explains why a static graph can find a plausible neighborhood while a
single intervention at the wrong timestep fails to produce the expected
image.

### checkpoint no-op — prove the button is real

The no-op control restores a Saturn checkpoint and runs the suffix without any
state replacement. All three axes reproduced the source image with RGB MAD
`0.0`.

That control is easy to overlook, but it is what makes the other buttons
credible. Without exact replay, a difference could come from a changed random
number stream, scheduler state, latent mutation, or dtype drift. With the
no-op, the experiment has a measured baseline for “press nothing.”

## What the images show

The [appearance montage](../../saturn/results/image-circuits/control-panel/job-bcbb4f9dd97b/00-appearance-montage.png)
shows the red-to-blue contrast. The [scene montage](../../saturn/results/image-circuits/control-panel/job-bcbb4f9dd97b/01-scene-montage.png)
shows snow-to-beach transport. The [character montage](../../saturn/results/image-circuits/control-panel/job-bcbb4f9dd97b/02-character-montage.png)
shows the fox-to-cat contrast. The [full control report](../../saturn/results/image-circuits/control-panel/job-bcbb4f9dd97b/image-control-report.md)
contains every branch, checkpoint handle, image metric, return-register metric,
and intervention event.

The visual pattern is consistent with the typed route:

- null branches lose clean image structure;
- full donor injections at the non-terminal route move toward the intended
  semantic target, though they are not guaranteed to preserve every unrelated
  detail;
- later boundaries express the contrast more cleanly than early boundaries;
- the terminal boundary can reproduce the target exactly because it is a
  direct image-state readout.

The [machine-readable role analysis](../../saturn/results/image-circuits/control-panel/job-bcbb4f9dd97b/analysis/image-control-analysis.json)
and [human-readable analysis](../../saturn/results/image-circuits/control-panel/job-bcbb4f9dd97b/analysis/image-control-analysis.md)
join these images with the earlier lexical activation traces.

## What we can claim

The strongest current interpretation is:

```text
JointCarrier
  → CrossStreamBridge
  → LateSemanticTransport
  → ImageReadoutClosure
```

The route is supported by several independent observations:

1. the same non-terminal boundaries move three distinct semantic axes;
2. targetward movement grows through the route rather than appearing only at
   one isolated address;
3. dose and timestep controls show structured, reproducible response curves;
4. null controls damage the image ABI;
5. exact checkpoint no-ops reproduce the source exactly;
6. the earlier lexical screen and the new absolute-state panel agree on the
   non-terminal route while explaining the special behavior of the terminal
   boundary.

This is a convergent reverse-engineering result. It is not yet a minimal
semantic-circuit certificate. We have used one seed, three prompt contrasts,
four denoising steps, and a fixed FLUX.2/Qwen configuration. We still need
multi-seed route ablations, spatial support measurements, collateral-effect
tests, and downstream continuation gates before claiming that the route is
minimal or universal.

## Reproducing the control panel

The panel is implemented in
[`run_saturn_image_control_panel.py`](../../saturn/workers/run_saturn_image_control_panel.py)
and configured by
[`rosetta-image-control-panel.json`](../../saturn/configs/rosetta-image-control-panel.json).
Run the dry check and launch one resident CUDA lease:

```bash
cd /Users/jakeholl/domains/saturn
uv run python workers/submit_saturn_image_control_panel.py \
  --config configs/rosetta-image-control-panel.json --dry-run

uv run python workers/submit_saturn_image_control_panel.py \
  --config configs/rosetta-image-control-panel.json

uv run python workers/submit_saturn_image_control_panel.py \
  --config configs/rosetta-image-control-panel.json \
  --collect JOB_ID --results-dir results/image-circuits/control-panel
```

Then analyze the receipt without loading the model again:

```bash
uv run saturn-image-control-analyze \
  results/image-circuits/control-panel/JOB_ID/report.json \
  --lexical results/image-circuits/lexical/JOB_ID/report.json \
  --lexical results/image-circuits/scene/JOB_ID/report.json \
  --lexical results/image-circuits/character/JOB_ID/report.json \
  --output-dir results/image-circuits/control-panel/JOB_ID/analysis
```

The Saturn implementation and usage notes are also documented in the
[image-stream control-panel section of the Saturn README](../../saturn/README.md#turn-image-stream-boundaries-into-control-buttons).

## The Rosetta interpretation

Before this work, an address such as `joint.4` was easy to treat as a label.
Now we can ask a better question: what typed state transition does this
boundary perform, under which semantic contrast, at which time, and with which
consumer?

That is the beginning of turning the model into software. We have not decoded
every instruction, but we have identified a callable family of operations:

```text
inject carrier → bridge streams → amplify semantic transport → close image ABI
```

The next step is to remove more of the donor crutch. We should learn whether a
carrier can be reconstructed from a smaller typed field, whether the route can
be ablated while preserving unrelated content, and whether the same labeled
operations survive across seeds, subjects, and model families. If they do, the
buttons stop being experiment-specific interventions and become reusable
software primitives in the Saturn Rosetta runtime.
