# Black Forest Labs Experiments

Black Forest Labs image generators are studied as systems that can be measured, interrupted, replayed, and controlled. The central question is not only whether a prompt produces a convincing image. It is also which information is carried by the model, where that information is consumed, whether it can be changed without changing the model weights, and how reliably the change reaches the final image.

The main narrative is led by six reports: exact phase-resident serving, consumer-closed route
promotion, a multi-model tracer campaign, recipient-native repair, typed interaction controls, and
real hotpatch/counterfactual futures. Native target images, exact replay, route ablations, hostile
donors, shams, dose sweeps, held-out prompts, and collateral measurements keep the claims bounded
to what the image consumer actually confirms. The other demo reports remain in this repository as
supporting evidence rather than being displaced by that front-of-house sequence.

## Models, checkpoints, and portability

Most of the phase-resident and causal demos use a single, explicitly pinned specimen: distilled
`black-forest-labs/FLUX.2-klein-4B` at revision
`e7b7dc27f91deacad38e78976d1f2b499d76a294`. Unless a demo says otherwise, that is the model,
checkpoint, and native denoiser behind the route, object, hotpatch, and serving results. The
recipient-patch demo is the deliberate exception: it compares the full-capacity
`black-forest-labs/FLUX.2-klein-base-4B` at `a3b4f4849157f664bdbc776fd7453c2783562f4d`
(50 steps, guidance 4) with the distilled recipient above (four steps, guidance 1).

The older circuit and instrumentation work is broader. The forward-free seven-model tracer
campaign covered the following checkpoint cohort; the FLUX.1 cross-compiled conditioner follow-up
then exercised the Schnell member dynamically alongside the Klein comparison:

| checkpoint | revision | native transformer shape | evidence scope |
| --- | --- | --- | --- |
| `black-forest-labs/FLUX.1-schnell` | `741f7c3ce8b383c54771c7003378a50191e9efe9` | 19 joint + 38 single blocks | static tracer; bounded capture/resume follow-up |
| `black-forest-labs/FLUX.2-klein-base-4B` | `a3b4f4849157f664bdbc776fd7453c2783562f4d` | 5 joint + 20 single | tracer; matched base/distilled diagnosis |
| `black-forest-labs/FLUX.2-klein-4B` | `e7b7dc27f91deacad38e78976d1f2b499d76a294` | 5 joint + 20 single | primary demos; tracer; causal-route panels |
| `black-forest-labs/FLUX.2-klein-9B` | `92196c8e11f7b6cf2b7493e037d8c5345c559216` | 8 joint + 24 single | tracer; bounded stock trajectory and readouts |
| `black-forest-labs/FLUX.2-klein-9b-kv` | `a6dfb36eca3a3906eb2fd460795adfb844e5fcce` | 8 joint + 24 single | tracer; native KV trajectory and cache path |
| `black-forest-labs/FLUX.2-dev` | `26afe3a78bb242c0a8bb181dcc8937bb16e5c66c` | 8 joint + 48 merged/single | tracer; component-decoupled runtime/instrumentation |
| `black-forest-labs/FLUX.2-small-decoder` | `a3efc24f613ef42d9428af62fdbd6f5fd8856c4a` | decoder-only boundary | tracer boundary and paired decoder diagnostics |

The portable result is therefore the instrument contract and route vocabulary, not a universal
semantic circuit. The tracer study was intentionally forward-free: it established that tensor
anatomy, shape budgets, substrate fingerprints, and coarse role fractions could be enumerated
across the cohort. The later FLUX.1 work showed that checkpoint capture, exact scalar resume,
typed debugger addresses, and consumer-facing causal-route instrumentation can be cross-compiled
to another family. Those are convergent portability trends; they do not establish that a payload,
readout, or causal meaning learned on Klein 4B transfers unchanged to Schnell, 9B, 9B-KV, Dev, or
newer variants.

## What the `joint.*` mapping means

`joint.i` is a native transformer address: the ordinal `i` of the `i`th joint/double-stream block
in that checkpoint's own denoiser. `single.i` is the ordinal `i` of a later single-stream block
after the streams have merged. These names are structural coordinates, not globally shared layer
IDs, tensor weights, or semantic labels.

For example, `joint.2 → joint.3 → joint.4 → single.0` is the route vocabulary used by several
Klein 4B demos. A mapping that reappears in another family means that the instrumentation can
address the corresponding native stage sequence using the same typed schema. It does not mean
that `joint.2` is at the same relative depth, contains the same basis vectors, carries the same
token role, or has the same causal effect: Schnell has 19 joint blocks, Klein 4B has 5, and Klein
9B/9B-KV and Dev have 8. Cross-family work must re-enumerate the local topology and revalidate the
consumer effect.

In short: the address ABI is portable; the state payload and semantic interpretation are
checkpoint-local. This is why the circuit reports can share a `joint.*` route map while keeping
model revisions, readouts, interventions, and terminal claims separate. See the [seven-model
tracer report](../../obsidian/blog/2026-08-06-tracer-seven-bfl-models.md) and the
[FLUX.1 cross-compiled instrumentation report](../../obsidian/blog/2026-08-09-saturn-flux1-cross-compiled-conditioner.md)
for the broader evidence and its boundaries.

## Tracer documentation

The [BFL research documentation](docs/README.md) contains the checkpoint-scoped tracer atlas behind
multi-model demo. It keeps separate cards for Schnell, Klein Base 4B, Klein 4B, Klein 9B, Klein
9B-KV, Dev, and the Small Decoder, including each revision, topology, instrument scope, live
assay, and claim boundary. The cards make the portability claim auditable: a shared role grammar
and address schema, with fresh local validation for any payload or consumer-facing circuit.

## Main narrative

These six reports lead the BFL story in the order most useful for evaluation: first the exact
systems result, then the consumer-closed method, then evidence of breadth across the FLUX.2 line,
followed by compact causal demonstrations and their honest boundaries.

### 1. Exact Phase-Resident Serving

[Exact Phase-Resident Serving](demos/exact-phase-resident-serving.md) is the strongest systems
result: byte-exact pixel and PNG parity, explicit phase-residency contracts, and speedups whose
denominators distinguish prepared-phase replay from setup-plus-generation. The measured Klein 4B
result is exact and legible; the execution contract is reusable, while another checkpoint needs
its own ABI, cache, and parity validation.

### 2. Route Cartographer with Consumer-Closed Promotion

[Route Cartographer with Consumer-Closed Promotion](demos/route-cartographer-consumer-closure.md)
is the central methodological contribution. A candidate is promoted only when the native image
consumer improves; otherwise it is rejected and the prior state is restored exactly. This closes
the loop between an internal route change and a useful image capability without treating a hidden
state movement as success.

### 3. Multi-Model Structural Tracer Campaign

[Multi-Model Structural Tracer](demos/multi-model-structural-tracer.md) provides the breadth result:
the FLUX.2 line exhibits a stable coarse role grammar and a useful search order, while concrete
addresses, payloads, and causal meanings remain topology-local. The recurring `joint.*` vocabulary
is therefore a portable instrumentation schema, not a universal circuit map.

### 4. Recipient-Native Capability Patch

[Recipient-Native Capability Patch](demos/recipient-native-capability-patch.md) is a compact
existence proof of a donor-free, process-surviving local repair: 55,297 FP16 values are installed
in the declared recipient and the patch uninstalls exactly. The held-out collateral failure stays
in the report, making the result a bounded repair rather than a universal fix.

### 5. Typed Snake Topology and Interaction Residuals

[Typed Snake Topology Repair and Interaction Residual](demos/typed-snake-topology-interaction.md)
shows route necessity and non-additive composition under proper ablation, wrong-axis, dose,
held-out, wrong-time/site/sign, and sham controls. The interaction is a pinned Klein 4B result and
does not by itself establish a portable compositor across checkpoint topologies.

### 6. Real Hotpatch Cinema and Counterfactual Futures

[Real FLUX Hotpatch Cinema](demos/real-hotpatch-cinema.md) and [Counterfactual Diffusion
Futures](demos/counterfactual-diffusion-futures.md) form the timing-sensitive supporting panel:
early cuts have authority, later cuts are weaker, and hostile donors steer toward their own
factor. Exact rollback keeps the parent recoverable, while the timing and donor-specificity claims
remain bound to the declared Klein 4B trajectory.

## Additional demo reports

These existing reports remain available as supporting evidence alongside the six-report main
narrative. They retain their local proof bundles, receipts, representative images, and verifier
links.

### 1. Exact Phase-Resident Serving

In [Exact Phase-Resident Serving](demos/exact-phase-resident-serving.md), reusable generation phases, suffix replay, and reference-edit caching are separated while exact pixels are preserved. Eight 512² generations run 10.66× faster per image and 6.25× faster end-to-end with exact parity, while the reference-edit cache reaches a median 4,696× cache-hit improvement. This is the systems layer through which the more expensive causal and editing work can scale.

### 2. Semantic Circuit Objects

In [Semantic Circuit Objects](demos/semantic-circuit-object-interface.md), a causal semantic route is compiled into a typed object symbol. Lexical rows are localized, joined to spatial probes, and recorded with route, timing, payload, dose, and evidence fields. The symbol is used to edit, isolate, delete, compose, and numerically steer objects. The blue-mug result works at both tested seeds, while durable manifest readback passes 11/11 checks.

### 3. Objects Become Debugger I/O

In [Objects Become Debugger I/O](demos/objects-debugger-io-structs-stress-isolation.md), a fox and ball are mapped to lexical and spatial addresses. Those addresses are tested through property edits, movement, layering, dose, wrong-address writes, and isolation, and the result is preserved as a fingerprinted manifest. Fox recolor progress reaches 0.92/0.94 across the two seeds; isolation progress is above 0.91 for the fox and 0.99 for the ball.

### 4. Real FLUX Hotpatch Cinema

In [Real FLUX Hotpatch Cinema](demos/real-hotpatch-cinema.md), the native trajectory intervention is replicated across four specimens and two semantic axes. Early edits reach 0.904–0.971 target progress, hostile donors move toward their own factor at 0.926–0.953, and later-cut edits fall to 0.095–0.358, with exact scalar confirmation and parent replay. Timing and donor identity are shown to be part of the editing capability boundary.

### 5. Counterfactual Diffusion Futures

In [Counterfactual Diffusion Futures](demos/counterfactual-diffusion-futures.md), a generation is paused, its trajectory is forked, a controlled route intervention is applied, and the unchanged image process is resumed. Early branches reach 0.904–0.971 target progress, while later cut points fall to 0.095–0.358; exact replay, hostile donors, and shams show when the effect is real and when it fades. Controlled image editing and counterfactual exploration are thereby enabled without regenerating every branch from scratch.

### 6. Twenty-Axis Native Semantic Route Circuit

In [Twenty-Axis Native Semantic Route Circuit](demos/twenty-axis-semantic-route-circuit.md), one typed route is tested against twenty independent visual factors. Six rows pass the strict 9/9 gate, eleven pass the relaxed 7/9 gate, and three remain candidates. The panel broadens the object work beyond one scene while keeping the interpretation at route-level control rather than single-token semantic ownership.

### 7. Recipient-Native Capability Patch

In [Recipient-Native Capability Patch](demos/recipient-native-capability-patch.md), a tiny rank-8 recipient-local patch repairs a counting regression in a distilled FLUX.2 model. The output changes from three apples to five using 55,297 FP16 parameters, survives a fresh process without the donor path, and uninstalls exactly. Held-out collateral keeps the result bounded, but the experiment directly demonstrates surgical repair of a release-specific capability.

### 8. Route Cartographer with Consumer-Closed Promotion

In [Route Cartographer with Consumer-Closed Promotion](demos/route-cartographer-consumer-closure.md), 685 native states and 85 branches are mapped, candidate addresses are predicted, and an intervention is promoted only when the actual image consumer improves. One update was promoted, three were rejected, and exact rollback succeeded 5/5. This distinguishes an internally interesting activation change from a route that can actually control the output image.

## Supporting report detail

[Typed Snake Topology Repair and Interaction Residual](demos/typed-snake-topology-interaction.md) provides a compact secondary example. A typed route changes a closed green coil into an open S-shaped snake with 0.9008 progress, while ablation, wrong-axis, dose, and held-out controls reject generic image movement. A paired lighting×color panel shows a real nonlinear interaction, although the first learned mixer does not beat a held-out linear baseline.

## What the primary path shows

The current working inference is that FLUX conditioning behaves like a distributed, time-dependent state interface. Some lexical rows are compact enough to act like object addresses, but the meaning of a write depends on the base context, route, timing, decoder priors, dose, and downstream consumer. Relations, pose, size, and composition are more contextual than simple color or noun identity.

The word “object” is used carefully. A conventional object database is not being claimed. Instead, a typed, measured record specifies where a model-state write is allowed, what payload it represents, what image region it should affect, and which controls establish that interpretation. The record becomes useful when it is confirmed by the native image consumer.

Failed transfers, noisy metrics, collateral, and held-out failures remain part of the evidence. The
remaining supporting and exploratory reports are preserved in this repository on `main`, so the
front-of-house sequence stays focused without discarding the research record.

## Reading the reports

The [experiment index](index.md) provides the executive summary of the primary path. Each [standalone demo](demos/) links to its local proof bundle, receipts, representative images, and verifier, allowing the reader to move from the high-level story to the evidence without needing the original notebook context.
