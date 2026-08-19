# Research

This is where I keep my public-facing research notes, standalone demos, and evidence-backed experiment reports. I organize the work so that a reader can move from the question I am asking, to the experiment I ran, to the artifacts that show what happened.

# Black Forest Labs

I study Black Forest Labs image generators as controllable systems rather than as opaque image makers. I want to understand what information the models use, where that information enters the generation process, which interventions reach the final image, and which explanations fail when I add native-consumer controls, wrong-source tests, shams, dose sweeps, held-out prompts, exact replay, and collateral measurements.

I work outward from broad behavior to model structure and then to practical control. I begin with counting, typography, context, model lineage, and decoder boundaries. I then trace distributed semantic routes and denoising-time authority. From there I test trajectory branching, object-level edits, capability repair, foreign and structured conditioners, exact serving, and learned approximations. The reports preserve both successful effects and failed or incomplete transfers because the boundary of an intervention is part of what I am trying to learn.

## Strongest experiments

I currently organize the strongest line of work in this order:

1. [Semantic Circuit Objects](bfl/demos/semantic-circuit-object-interface.md) — I compile a causal semantic route into a typed object symbol and use it to read, edit, isolate, and write object state back into the model. The blue-mug value write works at both tested seeds, while the durable manifest readback passes 11/11 checks.
2. [Objects Become Debugger I/O](bfl/demos/objects-debugger-io-structs-stress-isolation.md) — I map image objects to lexical addresses, test those addresses with controlled edits, and preserve them as durable model-facing records. Fox recolor progress reaches 0.92/0.94 across the two seeds, with isolation progress above 0.91 for the fox and 0.99 for the ball.
3. [Counterfactual Diffusion Futures](bfl/demos/counterfactual-diffusion-futures.md) — I fork an in-progress generation, change its future, and compare the result with exact parent, sham, hostile-donor, and rollback controls. Early edits reach 0.904–0.971 target progress, while later edits are much weaker.
4. [Exact Phase-Resident Serving](bfl/demos/exact-phase-resident-serving.md) — I separate reusable phases of generation while preserving exact pixels, making the more expensive causal work practical. The measured speedups are 10.66× per image and 6.25× end-to-end, with a median 4,696× cache-hit improvement.
5. [Route Cartographer with Consumer-Closed Promotion](bfl/demos/route-cartographer-consumer-closure.md) — I promote route interventions only when the native image consumer improves and retain exact rollback for rejected futures. From 685 captured native states and 85 branches, one update was promoted, three were rejected, and rollback succeeded 5/5.
6. [Twenty-Axis Native Semantic Route Circuit](bfl/demos/twenty-axis-semantic-route-circuit.md) — I test whether one causal route carries many visual factors and measure where route-level control is reliable or still only a candidate. Six rows pass the strict 9/9 gate, eleven pass the looser 7/9 gate, and three remain candidates.

## How to navigate this research

Start with the [Black Forest Labs README](bfl/README.md) for the overall story, then use the [experiment index](bfl/index.md) for the executive summary of every demo. Each [standalone report](bfl/demos/) links to its own local proof bundle, receipts, representative images, and verifier. The detailed reports distinguish observations, trends, working inferences, and bounded claims so that a compelling image is never mistaken for a general capability without the controls to support it.
