# Black Forest Labs Experiments

I am studying Black Forest Labs image generators as systems that can be measured, interrupted, replayed, and controlled. My central question is not only whether a prompt produces a convincing image. I want to know what information the model carries, where that information is consumed, whether I can change it without changing the model weights, and how reliably the change reaches the final image.

I move from broad behavior to causal routes, then from routes to practical interfaces. I use native target images, exact replay, route ablations, wrong-source and wrong-site controls, norm-matched shams, dose sweeps, held-out prompts, and collateral measurements. A successful image is useful evidence, but I treat it as a working result until the native consumer and the controls support the interpretation.

## Strongest experiments

The strongest experiments below are ordered the same way as the top of [the experiment index](index.md). Together they describe the main arc of my current work.

### 1. Semantic Circuit Objects

In [Semantic Circuit Objects](demos/semantic-circuit-object-interface.md), I take a causal semantic route and compile it into a typed object symbol. I localize lexical rows, join them to spatial probes, record route, timing, payload, dose, and evidence fields, and use the resulting symbol to edit, isolate, delete, compose, and numerically steer objects. The blue-mug result works at both tested seeds, while durable manifest readback passes 11/11 checks. This is still exploratory, but it is the clearest statement of the interface I am trying to build.

### 2. Objects Become Debugger I/O

In [Objects Become Debugger I/O](demos/objects-debugger-io-structs-stress-isolation.md), I map a fox and ball to lexical and spatial addresses, test those addresses through property edits, movement, layering, dose, wrong-address writes, and isolation, and preserve the result as a fingerprinted manifest. Fox recolor progress reaches 0.92/0.94 across the two seeds; isolation progress is above 0.91 for the fox and 0.99 for the ball. The failures show where size, pose, relations, and image-side deletion still depend on context, turning a promising route effect into a durable object-facing control record.

### 3. Counterfactual Diffusion Futures

In [Counterfactual Diffusion Futures](demos/counterfactual-diffusion-futures.md), I pause a generation, fork its trajectory, apply a controlled route intervention, and resume the unchanged image process. Early branches reach 0.904–0.971 target progress, while later cut points fall to 0.095–0.358; exact replay, hostile donors, and shams show when the effect is real and when it fades. This opens controlled image editing and counterfactual exploration without requiring me to regenerate every branch from scratch.

### 4. Exact Phase-Resident Serving

In [Exact Phase-Resident Serving](demos/exact-phase-resident-serving.md), I separate reusable generation phases, suffix replay, and reference-edit caching while preserving exact pixels. Eight 512² generations run 10.66× faster per image and 6.25× faster end-to-end with exact parity, while the reference-edit cache reaches a median 4,696× cache-hit improvement. This is the systems layer that lets the scientific work scale.

### 5. Route Cartographer with Consumer-Closed Promotion

In [Route Cartographer with Consumer-Closed Promotion](demos/route-cartographer-consumer-closure.md), I map 685 native states and 85 branches, predict which addresses may matter, and promote an intervention only when the actual image consumer improves. One update was promoted, three were rejected, and exact rollback succeeded 5/5; full text-state transfers close routes that single-token operations cannot. This gives me a safe way to distinguish an internally interesting signal from a route that can actually control the output image.

### 6. Twenty-Axis Native Semantic Route Circuit

In [Twenty-Axis Native Semantic Route Circuit](demos/twenty-axis-semantic-route-circuit.md), I test one typed route against twenty independent visual factors. Six rows pass the strict 9/9 gate, eleven pass the relaxed 7/9 gate, and three remain candidates; ablations and empty controls keep the interpretation bounded to route-level control rather than single-token semantic ownership. This broadens the object work beyond one scene and helps identify which kinds of visual information are worth compiling into future symbols.

## How the program fits together

I start with behavioral measurement so I know which user-visible behaviors are reliable and which fail under counting, typography, lexical, or substitution tests. Model-family forensics and decoder-boundary work tell me which artifacts and output stages I am actually comparing. Context and denoising-time experiments show that positional structure and timing can affect the image even when a prompt looks empty or unchanged.

I then map causal routes. Distributed K/V interventions, semantic route panels, route cartography, and typed topology edits test whether a visual effect is local or distributed, whether it survives into the image, and whether composition is linear or nonlinear. These experiments give me the route and consumer vocabulary needed to create an object symbol instead of guessing at a token or hidden unit.

Once a route is understood, I use saved trajectories as controlled parents. Counterfactual futures, wall-picture edits, living-room movement, and scene certificates test whether a branch can change one requested aspect while preserving the rest. The results are useful precisely because they expose the limits: early edits are stronger, spatial movement is not automatically metric, and scene changes can carry collateral.

The interface experiments test how conditioning reaches the image consumer. Cross-family conditioners, structured frontends, textless rendering, and FLUX.1 controls show that tensor compatibility is easy to establish but semantic interchange is much harder. Complete native state often transfers where compact slices fail, which supports the distributed, consumer-dependent picture behind the object symbols.

Finally, repair, selection, serving, and approximation experiments turn the findings into practical infrastructure. Recipient-native patches, seam bisection, nonlinear interaction compilers, native-state selectors, exact replay, paged execution, and closed-loop students test whether I can repair, accelerate, or safely abstain without losing the native consumer as the authority.

## What I believe the experiments show

My current working inference is that FLUX.2 conditioning behaves like a distributed, time-dependent state interface. Some lexical rows are compact enough to act like object addresses. Their values can carry property changes, but the meaning of a write depends on the base context, route, timing, decoder priors, dose, and downstream consumer. Relations, pose, size, and composition are more contextual than simple color or noun identity.

This is why I use the word “object” carefully. I am not claiming that the model contains a conventional object database. I am creating a typed, measured record that tells me where a model-state write is allowed, what payload it represents, what image region it should affect, and which controls establish that interpretation. The record becomes useful when the native image consumer confirms it.

The evidence remains exploratory. I keep failed transfers, noisy metrics, instrument bugs, collateral, and held-out failures in the record. The goal is to find interfaces that survive stronger tests, not to turn a clean visualization into a broader claim than the experiment earned.

## Reading the reports

Start with [the experiment index](index.md) for the executive summary of every demo. Open the strongest reports first, then follow the route, editing, compatibility, and systems sections outward. Each [standalone demo](demos/) links to its own proof bundle, receipts, representative images, and verifier, so the reader can move from the high-level story to the evidence without needing the original notebook context.
