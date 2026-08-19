
# Research Portfolio

Public-facing research notes, standalone demos, and evidence-backed experiment reports are kept here. The material is organized so that the question being studied, the experiment used to study it, and the artifacts showing what happened can be followed in sequence.

## Black Forest Labs

The work treats FLUX as software, not as a sealed model. The generation pipeline is broken into components, those components are profiled, and their inputs and outputs are monitored and rewritten to see what actually changes in the image.

The point is to know what the system is doing well enough to intervene on purpose: change a route, a phase, a conditioner, or a cached state, then measure whether the native image consumer follows. Some of that is scientific — which information is used, where it enters, which edits survive, and which stories collapse under controls. Some of it is practical — whether generation can be made cheaper, faster, or more reusable without losing exact pixels. Some of it is just to try ideas that would be hard to test if the model stayed opaque.

Failed and incomplete transfers are kept in the record. The boundary of an intervention is part of the result.

### Strongest experiments

1. [Semantic Circuit Objects](bfl/demos/semantic-circuit-object-interface.md) — A causal semantic route is compiled into a typed object symbol that can be used to read, edit, isolate, and write object state back into the model. The blue-mug value write works at both tested seeds, while durable manifest readback passes 11/11 checks.
2. [Objects Become Debugger I/O](bfl/demos/objects-debugger-io-structs-stress-isolation.md) — Image objects are mapped to lexical addresses, those addresses are tested with controlled edits, and the results are preserved as durable model-facing records. Fox recolor progress reaches 0.92/0.94 across the two seeds, with isolation progress above 0.91 for the fox and 0.99 for the ball.
3. [Counterfactual Diffusion Futures](bfl/demos/counterfactual-diffusion-futures.md) — An in-progress generation is forked, its future is changed, and the result is compared with exact-parent, sham, hostile-donor, and rollback controls. Early edits reach 0.904–0.971 target progress, while later edits are much weaker.
4. [Real FLUX Hotpatch Cinema](bfl/demos/real-hotpatch-cinema.md) — The native trajectory intervention is replicated across four specimens and two semantic axes. Early edits reach 0.904–0.971 target progress, hostile donors move toward their own factor at 0.926–0.953, and later edits fall to 0.095–0.358, with exact scalar confirmation and parent replay.
5. [Exact Phase-Resident Serving](bfl/demos/exact-phase-resident-serving.md) — Reusable phases of generation are separated while exact pixels are preserved, making the more expensive causal work practical. The measured speedups are 10.66× per image and 6.25× end-to-end, with a median 4,696× cache-hit improvement.
6. [Route Cartographer with Consumer-Closed Promotion](bfl/demos/route-cartographer-consumer-closure.md) — Route interventions are promoted only when the native image consumer improves, and exact rollback is retained for rejected futures. From 685 captured native states and 85 branches, one update was promoted, three were rejected, and rollback succeeded 5/5.
7. [Twenty-Axis Native Semantic Route Circuit](bfl/demos/twenty-axis-semantic-route-circuit.md) — One causal route is tested against many visual factors, and the reliability of route-level control is measured. Six rows pass the strict 9/9 gate, eleven pass the looser 7/9 gate, and three remain candidates.

### How to navigate this research

The [Black Forest Labs README](bfl/README.md) provides the overall story, and the [experiment index](bfl/index.md) provides the executive summary of every demo. Each [standalone report](bfl/demos/) links to its own local proof bundle, receipts, representative images, and verifier. Observations, trends, working inferences, and bounded claims are distinguished in the detailed reports so that a compelling image is not mistaken for a general capability without supporting controls.

---

## About the Author

My name is Jacob Hollenbeck. I have a B.S. in Electrical and Computer Engineering from Boise State University and an M.S. in Machine Learning from Georgia Tech OMSCS. I have 10+ years of experience in software and cyber engineering. This portfolio contains a sample of my independent AI/ML research.
