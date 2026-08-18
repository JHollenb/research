# Black Forest Labs Experiments

This directory contains standalone reports on experiments with Black Forest Labs image generators. Together they form one investigation rather than a collection of unrelated demos: first we measure the model's behavioral limits and artifact boundaries, then trace where information travels, then intervene on those routes, and finally test whether the discovered interfaces support editing, repair, substitution, or efficient execution.

## New highest-value experiment

### Objects Become Debugger I/O

The object experiment is currently the strongest because it closes the loop from a rendered object to a durable, inspectable control interface. The first stage discovers lexical and spatial addresses, the second proves that those addresses support selective edits and exposes contextual limits for size, movement, and layering, and the third turns the result into a fingerprinted manifest before testing conditioner depth, route redundancy, dose tolerance, out-of-distribution attributes, composition, wrong-address payload portability, and isolation. The most important findings are that property payloads remain row-local and route-redundant, the address selects the target while the payload selects the transform, and text-route object rows can re-bind an object in a void context while image-side complement writes remove it. The evidence is still bounded to one scene family and two seeds, but it is the collection's clearest demonstration of a useful model-facing object interface and its failure modes.

## How the experiments fit together

The foundation is measurement. Behavior taxonomy reports separate counting, typography, lexical presence, and semantic substitution, while model-family forensics and decoder-boundary studies establish which artifacts are actually being compared. The empty-context scaffold and image-stream timing experiments add an important constraint: both positional structure and denoising phase affect the final image, so a successful intervention must respect shape, route, and time rather than treating the model as a static latent space.

The next layer is causal route mapping. Distributed K/V interventions, the twenty-axis semantic circuit, the route cartographer, and the typed snake experiment use native targets, route ablations, wrong-axis donors, dose changes, shams, and held-out cases to show that useful information is often distributed across several sites and is consumed nonlinearly. These experiments support each other by moving from one narrow binding effect, to many semantic factors, to a broader route map, while repeatedly testing whether internal movement survives into the rendered image.

Once route behavior is established, the reports test operations on saved trajectories. Counterfactual diffusion futures, wall-picture hotpatching, living-room couch movement, and scene certificates show that an early trajectory can be forked and steered toward a requested scene or object change. The timing and collateral results keep the claim bounded: early edits can be powerful, late edits are weaker, and scene movement does not automatically preserve identity or every unrelated object.

The interface experiments ask whether the same downstream image process can accept new sources of conditioning. Cross-family conditioner repair, the four-frontend semantic ABI, FLUX.1 causal controls, and the textless Klein renderer show that shape-compatible inputs can reach the consumer, while held-out semantic interchange remains difficult. Complete native-state donors often work where compact token or channel slices fail, which ties the interface results back to the distributed-carrier findings.

The repair and control experiments turn those observations into practical tests. The recipient-native capability patch shows that a small local operation can restore a bounded capability in a distilled model; Klein seam bisection probes where that mismatch enters; the nonlinear interaction compiler tests whether native composition can be learned; and the native-state selector tests whether an earlier state can decide when to intervene. Their partial or negative results are useful because they identify the missing pieces: generalization, uncertainty calibration, collateral control, and consumer-closed training.

The object-address experiment now provides the clearest bridge across these layers. It uses the causal route and checkpoint controls established by the earlier panels, turns the resulting addresses into a durable manifest, and then uses the edit battery, dose sweep, wrong-address control, and isolation test to distinguish a real object-facing interface from a visually convenient but unstable mask. Its results support the broader route findings while adding a concrete unit of state—an object with lexical, route, spatial, and evidence fields—that later editing and composition experiments can compile against.

The systems experiments make the scientific loop affordable and reproducible. Exact phase-resident serving, suffix replay, reference caching, closed-loop students, and guarded FLUX.2 Dev paging reduce the cost of branching and preserve exactness where it matters. This lets the causal experiments retain alternative futures, replay controls, and failure cases instead of relying on a single winning image.

## Strongest experiments

### Objects Become Debugger I/O

This is the strongest integrated experiment because it demonstrates discovery, a live write path, durable typed state, and stress-tested boundaries in one chain. It shows selective property edits, route redundancy, useful dose through roughly 4×, visually clean novel attributes and compositions, target/payload separation under a wrong-address control, and text-route isolation of individual objects. Its importance is not that every address is solved; it is that the experiment defines a plausible object interface and measures exactly where that interface stops working.

### Exact phase-resident serving and replay

This is one of the strongest engineering results because it combines a large speed improvement with exact output parity rather than trading fidelity for throughput. It shows that prompt encoding, denoising, suffix replay, and reference caching can be separated into auditable phases, making the much more expensive causal experiments practical and reproducible.

### Counterfactual diffusion futures and hotpatch cinema

These experiments are strong because they use same-parent branches, hostile donors, dose controls, shams, multiple cut points, and exact rollback. Early trajectory edits move toward the intended scene or subject while late edits weaken, showing that image generation can be studied as a time-dependent program whose future can be compared under controlled interventions.

### Twenty-axis route circuit and distributed K/V route

Together these are important because they broaden the evidence beyond one successful feature. The twenty-axis panel finds several independently testable visual factors, while the distributed K/V panel shows that a narrow binding behavior can depend on a multi-site route. Their ablations and held-out controls support the conclusion that useful information is distributed and consumer-dependent rather than stored in one obvious token or unit.

### Recipient-native capability patch

The capability patch is strong because the intervention is tiny, recipient-local, donor-independent at serving time, and tested with zero-dose, wrong-time, fresh-process, and uninstall controls. It shows that a distilled model can have a bounded capability gap that is repairable without changing the whole model, while the later collateral and generalization failures define why this is a research result rather than a deployable universal hotfix.

### Route cartographer with consumer-closed promotion

This experiment is important because it turns route discovery into a measured decision process. Candidate updates are promoted only when the native image consumer improves and are rejected with exact rollback otherwise. The result shows that whole-edge or coalition-level transfers can work where single-token interventions are weak, and that internal alignment alone is not enough to justify a route claim.

### Cross-family conditioner repair and structured frontends

These experiments establish a valuable boundary: a frozen image suffix can accept foreign or structured conditioning in the correct tensor contract, but high hidden-state similarity does not guarantee held-out semantic equivalence. The combination of exact native-donor rescue, compact-mask failures, held-out controls, and partial structured transfer shows both what is portable and where a learned consumer-facing compiler is still missing.

### Typed snake repair and native interaction residual

The snake experiment is strong because it tests a discrete topology change with route ablation, wrong-axis, dose, and held-out controls. Its paired interaction panel shows that native composition contains a nonlinear term that simple addition misses, while the failed learned mixer prevents overclaiming a universal composition rule. This connects causal route evidence to the harder problem of composing multiple edits.

## Reading the reports

Each report is standalone and links only to its own local proof bundle. The reports distinguish observations, directional trends, convergent evidence, working interpretations, and bounded claims. A failed gate is retained as evidence about the instrument, specimen, or claim boundary; it is not silently converted into a claim that the underlying mechanism does not exist.

Start with the [experiment index](index.md), then open any [standalone demo report](demos/). Each artifact directory contains the raw result files, representative images or receipts, a short README, and a verifier that checks the evidence bundle locally.
