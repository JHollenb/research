# Black Forest Labs Experiments

Black Forest Labs image generators are studied as systems that can be measured, interrupted, replayed, and controlled. The central question is not only whether a prompt produces a convincing image. It is also which information is carried by the model, where that information is consumed, whether it can be changed without changing the model weights, and how reliably the change reaches the final image.

The primary demo path is intentionally short. It moves from exact serving, through causal routes and object-facing interfaces, into counterfactual editing and recipient-local repair. Native target images, exact replay, route ablations, hostile donors, shams, dose sweeps, held-out prompts, and collateral measurements keep the claims bounded to what the image consumer actually confirms.

## Strongest experiments

These eight experiments form the primary product and research narrative. They are ordered to show the most direct progression from measurable systems leverage to causal control and model repair.

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

## Supporting experiment

[Typed Snake Topology Repair and Interaction Residual](demos/typed-snake-topology-interaction.md) provides a compact secondary example. A typed route changes a closed green coil into an open S-shaped snake with 0.9008 progress, while ablation, wrong-axis, dose, and held-out controls reject generic image movement. A paired lighting×color panel shows a real nonlinear interaction, although the first learned mixer does not beat a held-out linear baseline.

## What the primary path shows

The current working inference is that FLUX conditioning behaves like a distributed, time-dependent state interface. Some lexical rows are compact enough to act like object addresses, but the meaning of a write depends on the base context, route, timing, decoder priors, dose, and downstream consumer. Relations, pose, size, and composition are more contextual than simple color or noun identity.

The word “object” is used carefully. A conventional object database is not being claimed. Instead, a typed, measured record specifies where a model-state write is allowed, what payload it represents, what image region it should affect, and which controls establish that interpretation. The record becomes useful when it is confirmed by the native image consumer.

Failed transfers, noisy metrics, collateral, and held-out failures remain part of the evidence. The remaining supporting and exploratory reports are preserved on the `additional-experiments` branch so that the primary path stays focused without discarding the research record.

## Reading the reports

The [experiment index](index.md) provides the executive summary of the primary path. Each [standalone demo](demos/) links to its local proof bundle, receipts, representative images, and verifier, allowing the reader to move from the high-level story to the evidence without needing the original notebook context.
