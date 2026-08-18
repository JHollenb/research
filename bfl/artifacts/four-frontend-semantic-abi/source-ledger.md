# Five BFL experiments in Saturn: the carrier is real, the frontend is not yet replaceable

*2026-08-14 · FLUX.2 Klein 4B · Saturn exploratory ledger*

The recent Saturn/BFL posts changed the question.

The interesting object is not merely a hidden activation inside FLUX.2. It is a
model runtime: a typed execution graph with address and payload planes,
semantic state, family-local lowering, checkpointed futures, causal Acts,
native scheduler/VAE execution, and exact rollback. The right next step was
therefore not one more isolated activation patch. It was a five-part attempt to
turn the strongest observations into interfaces that could be searched,
compiled, substituted, and falsified.

This post records what I ran, what the measurements say, and what I explicitly
did not do. Every result below is marked as exploratory. None should be read as
a terminal claim about the architecture of FLUX.2 or about Black Forest Labs'
training code.

## The experimental contract

I used Saturn for the execution and analysis rather than wrapping the model in
a conventional training loop.

Each real-model job was admitted through `mrun` with one CUDA lease and one
resident Klein process. Local branches were checkpoint restores or scalar
suffix replays inside that process. The native scheduler and VAE remained in
the loop. The important controls were zero-dose/no-op, sign reversal, wrong
site or time, energy/norm-matched shams, and exact checkpoint replay.

The reason for this discipline is simple: a tensor can look similar without
being useful to the downstream consumer, and an intervention can change an
image without carrying the intended semantic variable. Saturn lets us keep
producer, typed write, carrier, consumer, scheduler, and VAE in one causal
ledger.

The fresh jobs were:

| Experiment | Saturn artifact | Main question | Outcome |
| --- | --- | --- | --- |
| Klein Seam Bisection | `rosetta-klein-seam-bisection-bfl-next` | Can Base behavior be repaired in a minimal distilled seam? | A real seam was localized, but the repair generalized exactly on only 1/4 held-out cases. |
| Four-Frontend Semantic ABI | `rosetta-cross-family-four-axis-bfl-next` plus the structured probe | Do Qwen, SmolLM, Mamba, and structured state reach one consumer through one contract? | The typed consumer boundary is real; donor-free, common-contract frontend closure is not established. |
| Nonlinear Interaction Compiler | `rosetta-semantic-mixer-bfl-next` and `rosetta-interaction-residual-panel-bfl-next` | Does a learned interaction composer beat additive composition? | No. Native interaction is strong; the learned composer was worse than additive on held-out pairs. |
| Temporal Carrier Compiler | `rosetta-temporal-carrier-compiler-bfl-next` | What is the smallest phase-specific carrier Act? | Authority increased sharply with time; a late joint.2 image seam transferred substantial held-out effect. |
| Textless Klein Renderer | `rosetta-structured-frontend-bfl-next` | Can structured state drive frozen Klein without language at inference? | Yes as a pilot, with heterogeneous generalization: one exact held-out composition, one strong partial rescue, and two failures. |

The jobs used one resident model each. The seam experiment necessarily had two
physical jobs—one Base capture and one distilled repair—so that the Base
artifact was immutable and the repair process loaded only the distilled
recipient. The ABI and textless results are complementary one-load specimens,
not a claim that four frontends were already proven in one monolithic job.

## 1. Klein Seam Bisection

### Why

The earlier Base-versus-distilled work showed a useful behavioral gap, but its
execution was not yet the cleanest possible split-load experiment. The new
question was narrower:

> If Base and distilled Klein disagree, can a fresh Base trajectory be sealed,
> loaded into MinIO as boundary artifacts, and then used by a one-load
> distilled process to learn the smallest route × timestep × stream repair?

This is a stronger test than copying a whole hidden state. It asks whether a
small typed Act can repair a downstream capability while preserving the
recipient's own execution.

### How

The Base capture job loaded `FLUX.2-klein-4B` Base once and captured all four
routes—`joint.2`, `joint.3`, `joint.4`, and `single.0`—at four denoising
timesteps, for both text and image streams. It used fresh sealed prompts for
three red squares and five blue circles during discovery, and four red squares
and six blue circles as held-out prompts, with two seeds each.

Each boundary tensor was written as a content-addressed Saturn artifact. The
repair job then loaded only the distilled model once, fetched those immutable
artifacts, fit a rank-8 coordinate-local Act, and searched 32 candidate seams.
The hierarchical selection order was site, then timestep, then stream. The
repair job also ran native-distilled, zero-dose, sign-flip, energy-matched
sham, and wrong-site branches.

### What happened

The selected seam was:

```text
joint.2 → step 0 → text
```

The discovery site scores were 0.500 for `joint.2`, 0.469 for `joint.3`, and
about 0.466 for both `joint.4` and `single.0`. The timestep score favored step
0 at 0.606; the text stream scored 0.738 versus 0.475 for image.

The selected Act reproduced the sealed discovery evaluator exactly on three of
four cells. On the held-out repair cells it produced:

| Prompt | Expected count | Repaired count | Exact |
| --- | ---: | ---: | ---: |
| four red squares, seed 31337 | 4 | 4 | yes |
| four red squares, seed 31339 | 4 | 3 | no |
| six blue circles, seed 31337 | 6 | 5 | no |
| six blue circles, seed 31339 | 6 | 4 | no |

The job itself was technically clean: one distilled model load, native
scheduler and VAE, exact scalar site replacement, and exact checkpoint replay
with RGB MAD 0.0 against the unreplayed suffix.

### Interpretation

This is evidence for a localized, early carrier seam in this particular
Base-to-distilled mismatch. It is not evidence that the seam is a universal
semantic ABI. The repair did not generalize to the fresh count prompts. Some
controls also produced a correct count on individual seeds, which means the
connected-component evaluator and the intervention must be expanded before a
terminal causal claim.

The important result is therefore a boundary result:

> Saturn can split Base capture from distilled repair, preserve the Base
> future immutably, and search a typed seam in the recipient. The first
> discovered seam is not yet a donor-free general repair.

Artifact: `saturn/results/rosetta-klein-seam-bisection-bfl-next/`.

## 2. Four-Frontend Semantic ABI

### Why

The cross-family observations already suggested that Qwen, SmolLM, and Mamba
can reach a common Klein consumer even when their conditioner tensors have
almost no semantic alignment. The dangerous overinterpretation would be to
call that a universal frontend ABI immediately.

The fresh test asked whether independent family-local lowering could preserve a
held-out semantic change without pretending that hidden tensors were shared
machine code.

### How

The fresh cross-family job loaded the Qwen, SmolLM, and Mamba conditioners and
one frozen Klein consumer in a single resident process. It used one fresh
held-out semantic pair—exactly two blue foxes, with a scene change—and measured
72 route × timestep × stream coordinates. Source token IDs were not assumed
to be shared. The job retained dense tensors, typed shapes, image/token axes,
channel axes, route/site, and timestep as separate coordinates.

The job also tested full-site donor, compact semantic-token and channel
intersections, packed-return intersections, shams, wrong-step controls, and
exact rollback.

### What happened

The operational contract was unusually strong:

- 72/72 planned coordinates observed exactly;
- one resident Klein load;
- one outer `mrun` submission;
- exact scalar causal replays;
- compact dense replay parity;
- exact checkpoint no-ops and rollback.

The values were not interchangeable. The small semantic-token/channel
intersections rescued almost nothing. A full-site donor was also weak in this
fresh specimen: normalized rescue was about 0.010 for Mamba and 0.122 for
SmolLM. The late selected-site/all-step package was much stronger—about 0.821
for Mamba and 0.935 for SmolLM—while still being a native Qwen donor package,
not a donor-free compiler.

That distinction matters. The consumer boundary accepts the packages, but the
carrier values remain family-specific. The experiment supports a typed
transport boundary and a distributed downstream carrier. It does not show
that SmolLM or Mamba can independently generate the same semantic package on
unseen concepts without a donor or a trained family-local compiler.

Artifact: `saturn/results/rosetta-cross-family-four-axis-bfl-next/`.

## 3. Nonlinear Interaction Compiler

### Why

For two semantic changes A and B, additive composition uses:

```text
ΔA + ΔB
```

The native pair contains an interaction residual:

```text
I_AB = ΔAB − ΔA − ΔB
```

The existing native-donor result showed that `I_AB` can matter. The bolder
claim was that a tiny learned nonlinear composer could infer it from held-out
training pairs and beat additive composition.

### How

The fresh learned mixer used two discovery pairs—lighting × identity and
weather × fur—and two pair-disjoint held-out pairs—lighting × fur and
orientation × relation—across two seeds. It exposed 32 learned coefficients,
including normalized-product and signed-product-root features, to Saturn's
proposal evaluator. Each proposal was promoted or rejected through checkpoint
feedback; rejected proposals were rolled back exactly.

The mixer made 32 proposals, promoted 9, rejected 23, and recorded exact
rollback for every rejected proposal. The held-out comparison was against
additive delta sum and the native AB reference.

### The negative result

On held-out pairs:

| Method | Mean progress to native AB | Mean return progress | Mean return alignment |
| --- | ---: | ---: | ---: |
| additive delta sum | 0.735 | 0.860 | 0.881 |
| learned nonlinear mixer | 0.716 | 0.840 | 0.864 |
| native AB reference | 1.000 | 1.000 | 1.000 |

The learned nonlinear mixer lost to the simpler additive baseline. This is
exactly the kind of result the proposal mechanism is supposed to expose: a
model-shaped hypothesis that looked plausible on discovery was not promoted to
a stronger held-out claim.

### The native interaction panel

I also ran a fresh native interaction residual panel on the lighting × color
pair with two seeds. The algebraic reconstruction was exact: dose-1 native
interaction matched the native AB image with MAD 0.0 and the native AB return
with RMS 0.0.

The downstream dose curve was clear:

| Branch | Mean progress to AB | Mean return progress |
| --- | ---: | ---: |
| additive linear | 0.596 | 0.754 |
| interaction dose 0.25 | 0.679 | 0.806 |
| interaction dose 0.50 | 0.764 | 0.854 |
| interaction dose 0.75 | 0.840 | 0.921 |
| interaction dose 1.00 | 0.894 | 0.931 |
| interaction dose 1.25 | 0.842 | 0.925 |
| norm-matched sham | 0.236 | 0.499 |
| sign flip | 0.373 | 0.598 |
| wrong site | 0.576 | 0.745 |
| wrong time | 0.679 | 0.831 |
| interaction only, no linear terms | -0.030 | 0.090 |

The interaction is real and dose-sensitive, but it is not sufficient by
itself. The late `single.0` boundary carried much more of the interaction-only
effect than `joint.2`, `joint.3`, or `joint.4`.

The combined conclusion is stronger than either result alone:

> Native nonlinear composition is a useful causal target. The first learned
> composer did not recover it on held-out pairs.

Artifacts: `saturn/results/rosetta-semantic-mixer-bfl-next/` and
`saturn/results/rosetta-interaction-residual-panel-bfl-next/`.

## 4. Temporal Carrier Compiler

### Why

The route might be the right address but the wrong abstraction if a semantic
carrier is distributed across denoising time. The experiment therefore searched
route × phase rather than treating `joint.2`, `joint.3`, `joint.4`, and
`single.0` as interchangeable sites.

### How

The temporal compiler used the image stream across all four routes and four
denoising steps: 16 candidate coordinates. It selected on two discovery pairs
and evaluated two pair-disjoint held-out pairs. The Act copied a native target
image-stream boundary into a source branch, then measured progress, return
alignment, continuation RMS, collateral, and dose efficiency.

I intentionally kept this run image-stream-only. Text sequence lengths differed
between some prompts, and direct cross-prompt text replacement would have been
a shape error disguised as a scientific result. The runtime rejected that
initial attempt; the repaired run made the stream contract explicit instead.

### What happened

The selected coordinate was:

```text
joint.2 → step 3 → image
```

The mean early-authority curve across discovery cells was:

| Step | Authority |
| ---: | ---: |
| 0 | 0.035 |
| 1 | 0.228 |
| 2 | 0.508 |
| 3 | 0.722 |

On four held-out cells, the selected Act achieved mean progress 0.545 toward
the native target, mean return progress 0.717, and mean return alignment
0.978. The controls were much weaker: zero-dose progress 0.000, wrong-time
0.001, energy-matched sham -0.008, and sign-flip 0.047.

The selected dose efficiency was 0.000662 under the experiment's
progress/alignment/collateral score. Exact scalar suffix replay again had RGB
MAD 0.0 against the full native suffix.

This is a convergent temporal trend, not a claim that one tiny Act is the
complete semantic frontend. Authority rises toward the late denoising phase,
but the intervention still transfers only part of the target behavior.

Artifact: `saturn/results/rosetta-temporal-carrier-compiler-bfl-next/`.

## 5. Textless Klein Renderer

### Why

The most ambitious version of the ABI removes natural language entirely. A
SceneGraph, CAD description, image-derived state, or robot state should be able
to compile into the same frozen Klein consumer package.

### How

The structured probe used four representations:

- SceneGraph;
- CAD;
- image-derived JSON;
- robot/JSON.

The compiler first built an atomic codebook from Qwen teacher prompts. At
structured inference, it accepted only typed fields such as object, color,
scene, count, relation, negation, and composition, and emitted a family-local
Klein `PromptEmbeds` tensor. It did not convert held-out structured states back
into text. The same native scheduler, denoiser, and VAE rendered the result.

The held-out states deliberately mixed unseen counts, colors, relations,
negation, and composition.

### What happened

The discovery cells were exact by construction: the atomic codebook matched the
teacher prompts. The held-out results were heterogeneous:

| Frontend | Held-out behavior | Progress to native Qwen |
| --- | --- | ---: |
| SceneGraph | two red foxes, desert, left-of relation | -0.299 |
| CAD | two blue cats, forest, right-of relation | 0.024 |
| image-derived JSON | space, no-circle negation | 0.733 |
| robot/JSON | fox-and-circle composition | 1.000 |

The mean held-out progress was 0.364. Mean native-embedding cosine was 0.984,
which is a useful warning: embedding closeness did not guarantee downstream
image equivalence. The zero-dose control averaged essentially 0.000 progress;
the norm-matched sham averaged 0.0003; the wrong structured state averaged
-0.120.

The result is a genuine textless rendering trend. One structured composition
was exact and another transferred most of the native effect. It is not yet a
general structured semantic renderer because the SceneGraph and CAD cases did
not generalize.

Artifact: `saturn/results/rosetta-structured-frontend-bfl-next/`.

## What changed after reading the recent BFL posts

I refreshed against the current `bfl-saturn-founder-ledger`,
`we-treated-klein-like-an-executable-machine`,
`the-route-carried-pairs-the-snake-needed-a-better-donor`,
`flux-capability-cherry-pick`, and the three-day Saturn summary. The posts did
not change the ambition. They changed the claim boundary.

The strongest prior work still supports these statements:

1. Klein can be treated as an executable, checkpointable machine.
2. A typed consumer boundary can accept family-local packages whose source
   tensors are not semantically aligned.
3. Semantic changes are carried by distributed route/time state, not one
   arbitrary tensor slice.
4. Native pair interactions are downstream-relevant and nonlinear.
5. Saturn makes branch, rewind, conflict, and exact replay practical research
   operations.

The new results do not justify saying that Klein already has a replaceable
semantic frontend. They justify saying that the frontend hypothesis has an
executable test surface. The structured pilot and the cross-family map now sit
on either side of that surface: one shows that non-language state can work for
some compositions, and the other shows that distinct conditioner families can
reach the same consumer boundary without tensor identity.

## What I did not do

This is the most important section.

I did not close donor-free SmolLM/Mamba generalization. The fresh cross-family
run used a small held-out semantic panel and native donor packages for its
strongest rescue branches. It did not train independent Qwen, SmolLM, and Mamba
frontends to a common held-out contract.

I did not learn a nonlinear composer that beats additive composition. The new
held-out result goes the other way. The native interaction residual is a strong
oracle target, not a learned compiler result.

I did not prove a universal seam between Base and distilled Klein. The seam run
was split-load and exact, but the selected Act reached only one of four held-out
cases exactly, and several controls were not yet perfectly discriminative.

I did not run all four frontends on the identical semantic examples in one
physical job. The Qwen/SmolLM/Mamba map and the structured frontend are two
one-load experiments joined at the report level. That is useful evidence of a
shared consumer contract, but it is not the explosive four-frontend closure
described in the proposal.

I did not build real CAD, robot, or image encoders. The structured inputs were
typed JSON-like states. “Image-derived” means a structured state derived from
an image, not raw pixels entering a learned vision frontend.

I did not update Klein's weights. The denoiser and native consumer stayed
frozen. The learned mixer was a tiny proposal object; the structured compiler
was an additive teacher-built codebook, not a trained universal semantic
frontend.

I did not establish a universal BFL internal architecture from these outputs.
All claims are about measured behavior at the tested boundary, prompts, seeds,
revision, scheduler, and VAE.

I did not run terminal certification. These are exploratory trends with strong
execution receipts, not preregistered multi-seed release gates.

## Bottom line

No one of the three proposed architecture closures passed cleanly:

- donor-free Smol/Mamba unseen-semantics frontend: not closed;
- learned nonlinear `I_AB` composer beating additive: failed on held-out pairs;
- general structured SceneGraph frontend: promising but not closed.

But the experiments did produce a sharper result than “we tried some patches.”

The frozen Klein consumer behaves like a real typed runtime boundary. Its
semantic carrier has temporal authority. Its pair composition contains a
measurable nonlinear residual. Structured non-language state can drive it in
some unseen cases. And Saturn can make each of those statements causal,
branchable, replayable, and falsifiable.

The next decisive experiment is now obvious: one resident Klein job with the
same sealed semantic contract presented independently by Qwen, SmolLM, Mamba,
and a structured SceneGraph compiler, with no donor tensors at inference,
multiple seeds, exact controls, and a learned frontend trained only on
disjoint semantics. Until that run passes, “replaceable semantic frontend” is a
well-supported hypothesis—not an experimental fact.
