# Black Forest Labs Experiment Index

This is the primary demo path for product and research discussion. It contains the eight individual experiments represented by the six recommended narrative groups, followed by the Typed Snake supporting experiment. Each entry states what was attempted, what changed in the image or execution, and what capability or boundary the result opens.

The remaining supporting and exploratory reports are preserved on the `additional-experiments` branch. They are not part of the first-look path, but their evidence remains available for follow-up review.

## Primary demo path

| experiment | why it matters |
| --- | --- |
| [Exact Phase-Resident Serving](#exact-phase-resident-serving-replay-and-edit-caching) | Separates reusable generation phases while preserving exact pixels, producing 10.66× per-image and 6.25× end-to-end speedups plus a median 4,696× cache-hit improvement. |
| [Semantic Circuit Objects](#semantic-circuit-objects-creating-symbols-and-using-them-directly-in-flux2) | Compiles a causal route into a typed object symbol that can be read, edited, isolated, composed, and written back; the blue-mug write works at both tested seeds and manifest readback passes 11/11. |
| [Objects Become Debugger I/O](#objects-become-debugger-io-deep-property-mapping-stress-and-isolation) | Converts image objects into durable debugger values. Fox recolor reaches 0.92/0.94 across two seeds, with isolation above 0.91 for the fox and 0.99 for the ball. |
| [Real FLUX Hotpatch Cinema](#real-flux-hotpatch-cinema) | Replicates native trajectory edits across four specimens and two semantic axes: early edits reach 0.904–0.971, hostile donors 0.926–0.953, and later edits 0.095–0.358. |
| [Counterfactual Diffusion Futures](#counterfactual-diffusion-futures) | Forks a paused generation, changes its future, and resumes the unchanged process with exact-parent, sham, hostile-donor, and rollback controls. |
| [Twenty-Axis Native Semantic Route Circuit](#twenty-axis-native-semantic-route-circuit) | Tests one typed route against twenty visual factors. Six rows pass 9/9, eleven pass 7/9, and three remain candidates, showing broad route-level scope without overclaiming ownership. |
| [Recipient-Native Capability Patch](#recipient-native-capability-patch) | Repairs a distilled counting regression with a 55,297-parameter recipient-local patch that survives a fresh process and uninstalls exactly, while held-out collateral remains visible. |
| [Route Cartographer with Consumer-Closed Promotion](#route-cartographer-with-consumer-closed-promotion) | Promotes only interventions that improve the native image consumer. One update was promoted, three rejected, and rollback succeeded 5/5 across 685 states and 85 branches. |

## Supporting experiment

### [Typed Snake Topology Repair and Interaction Residual](demos/typed-snake-topology-interaction.md)

A typed route changes a closed green coil into an open S-shaped snake, reaching 0.9008 progress while ablation, wrong-axis, dose, and held-out controls reject generic image movement. A paired lighting×color panel shows a real nonlinear interaction that addition alone misses, while the first learned mixer fails to beat a held-out linear baseline. Structured shape editing and native interaction measurement are opened, but not a general algebra for combining arbitrary edits.

## Primary reports

### [Exact Phase-Resident Serving, Replay, and Edit Caching](demos/exact-phase-resident-serving.md)

Prompt encoding is separated from denoising so that weights are not repeatedly transferred. Eight 512² generations remain pixel- and PNG-exact while running 10.66× faster per image and 6.25× faster end-to-end; exact suffix replay and reference-edit caching extend the result to zero-error branching and a median 4,696× cache-hit speedup. An efficient substrate for large intervention sweeps, interactive editing, and reproducible counterfactual research is opened.

### [Semantic Circuit Objects: Creating Symbols and Using Them Directly in FLUX.2](demos/semantic-circuit-object-interface.md)

A consumer-visible semantic circuit is compiled into a typed object symbol. Lexical rows are localized with controlled donor/base contrasts, joined to image-space probes, and recorded with route, timing, payload, dose, and evidence fields. The symbol is used to edit, isolate, delete, compose, or numerically steer an object. The blue-mug write works at both tested seeds, while durable manifest readback passes 11/11 checks. A model-facing object interface is opened, but it remains exploratory rather than a universal prompt-independent API.

### [Objects Become Debugger I/O: Deep Property Mapping, Stress, and Isolation](demos/objects-debugger-io-structs-stress-isolation.md)

A fox and ball are mapped to lexical addresses, those addresses are proven through recolor, material, shape, movement, layering, dose, wrong-address, and isolation tests, and the result is stored as a fingerprinted manifest. Fox recolor reaches 0.92/0.94 across two seeds, and white-context isolation reaches above 0.91 for the fox and 0.99 for the ball. A concrete path toward object-level image tools with explicit addresses, controls, and failure modes is opened.

### [Real FLUX Hotpatch Cinema](demos/real-hotpatch-cinema.md)

The replicated native panel contains four specimens, two semantic axes, two denoising cuts, dose controls, hostile donors, shams, scalar confirmation, and exact rollback. Early full-dose edits reach 0.904–0.971 target progress, hostile donors reach 0.926–0.953 toward their own factor, and the same intervention at the later cut falls to 0.095–0.358. Native-consumer trajectory debugging and counterfactual image futures are opened, while timing and donor identity remain explicit capability boundaries.

### [Counterfactual Diffusion Futures](demos/counterfactual-diffusion-futures.md)

A four-step generation is paused, its trajectory is forked, a donor route state is written, and the unchanged image process is resumed. Early edits reach 0.904–0.971 progress toward the intended scene or subject, hostile donors move toward their own targets, shams stay near the source, and halfway edits are much weaker; exact replay restores every parent. Controlled image editing and counterfactual previews are opened, with the boundary that this is a bounded donor-assisted editor rather than a universal prompt-free editor.

### [Twenty-Axis Native Semantic Route Circuit](demos/twenty-axis-semantic-route-circuit.md)

One typed native route is tested against twenty visual contrasts such as identity, count, lighting, and scene changes. Six rows pass the strict 9/9 gate and eleven pass a looser 7/9 carrier-level gate; route ablation and sham controls distinguish a real consumer effect from a hidden-state correlation. A broad route map for choosing where to intervene is opened, but ownership of a named concept by any single address is not established.

### [Recipient-Native Capability Patch](demos/recipient-native-capability-patch.md)

A tiny rank-8 recipient-local patch is installed in a distilled FLUX.2 model to repair a counting regression. The output changes from three apples to five using 55,297 FP16 parameters, survives a fresh process without the donor path, and uninstalls exactly; held-out prompts reveal collateral changes. Targeted model repair and capability-specific patching are opened, but the current patch is not general enough to ship as a universal fix.

### [Route Cartographer with Consumer-Closed Promotion](demos/route-cartographer-consumer-closure.md)

The cartographer records native states, branches, route candidates, and endpoint outcomes, after which an intervention is promoted only when the real image consumer improves. One update is promoted, three are rejected, and exact rollback succeeds 5/5; whole text-state transfers close the tested edges while single-token QKV routes do not. A safe model-debugging loop is thereby provided for discovering promising routes without mistaking an internal activation change for a useful image capability.
