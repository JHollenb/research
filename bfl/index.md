# Black Forest Labs Experiment Index

I use this index to explain what I am trying to learn or build with each Black Forest Labs experiment, what changed in the model's output or execution, and what practical capability the result opens—or rules out. The linked reports and local artifact bundles contain the detailed methods, receipts, images, controls, and verifiers.

## Strongest experiments at a glance

| experiment | why it matters |
| --- | --- |
| [Semantic Circuit Objects](#semantic-circuit-objects-creating-symbols-and-using-them-directly-in-flux2) | My strongest synthesis: I turn a causal semantic route into a typed object symbol that I can read, edit, isolate, and write back into the model. The blue-mug value-level write works at both tested seeds, and durable manifest readback passes 11/11 checks. |
| [Objects Become Debugger I/O](#objects-become-debugger-io-deep-property-mapping-stress-and-isolation) | I map image regions to lexical addresses, prove selective edits, package the address as durable state, and stress-test dose, wrong-address writes, composition, and isolation. Fox recolor reaches 0.92/0.94 progress across two seeds, making this my clearest bridge from model internals to a usable control surface. |
| [Counterfactual Diffusion Futures](#counterfactual-diffusion-futures) | I fork a generation early, steer it toward a different scene or subject, and resume the unchanged image process. Early branches reach 0.904–0.971 target progress, opening controlled image editing while preserving exact parents and controls. |
| [Exact Phase-Resident Serving](#exact-phase-resident-serving-replay-and-edit-caching) | I separate prompt encoding, denoising, suffix replay, and reference edits while preserving exact pixels. The measured speedups are 10.66× per image, 6.25× end-to-end, and 4,696× at the median cache hit, making expensive causal experiments practical. |
| [Route Cartographer with Consumer-Closed Promotion](#route-cartographer-with-consumer-closed-promotion) | I promote route interventions only when the native image consumer improves, and I roll rejected futures back exactly. Across 685 native states and 85 branches, one update was promoted, three were rejected, and rollback succeeded 5/5. |
| [Twenty-Axis Native Semantic Route Circuit](#twenty-axis-native-semantic-route-circuit) | I test whether one causal route carries many independent visual factors. Six rows pass 9/9, eleven pass 7/9, and three remain candidates, giving me a broad route-level capability map without overclaiming single-token ownership. |

## Object interfaces and semantic circuits

### [Semantic Circuit Objects: Creating Symbols and Using Them Directly in FLUX.2](demos/semantic-circuit-object-interface.md)

I use this synthesis to explain how a consumer-visible semantic circuit becomes a typed object symbol. I localize lexical rows with controlled donor/base contrasts, join them to image-space probes, record route, timing, payload, dose, and evidence fields, and use the symbol to edit, isolate, delete, compose, or numerically steer an object. The blue-mug write works at both tested seeds, while durable manifest readback passes 11/11 checks. This opens a model-facing object interface for controllable editing and debugging, but remains exploratory rather than a universal prompt-independent API.

### [Objects Become Debugger I/O: Deep Property Mapping, Stress, and Isolation](demos/objects-debugger-io-structs-stress-isolation.md)

I use this three-stage experiment to test whether a rendered object can become a durable debugger value rather than a visual region selected after the fact. I map a fox and ball to lexical addresses, prove those addresses through recolor, material, shape, movement, layering, dose, wrong-address, and isolation tests, and store the result as a fingerprinted manifest. Fox recolor reaches 0.92/0.94 progress across two seeds, and white-context isolation reaches above 0.91 for the fox and 0.99 for the ball. This opens a concrete path toward object-level image tools with explicit addresses, controls, and failure modes.

### [Twenty-Axis Native Semantic Route Circuit](demos/twenty-axis-semantic-route-circuit.md)

I use this panel to test one typed native route against twenty visual contrasts such as identity, count, lighting, and scene changes. Six rows pass the strict 9/9 gate and eleven pass a looser 7/9 carrier-level gate; the expected output is movement toward the native target image, while route ablation and sham controls distinguish a real consumer effect from a hidden-state correlation. This opens a broad route map for choosing where to intervene, but does not establish that any single address owns a named concept.

### [Distributed K/V Causal Route](demos/distributed-kv-causal-route.md)

I probe twenty native key/value sites to learn whether a color-binding effect lives in one location or across a distributed route. The effect reproduces across sites, grows nonlinearly with dose, accumulates across denoising steps, and reaches native endpoint margins of +6.740 forward and +8.830 reverse, with 83/96 and 88/96 endpoint recoveries. This opens distributed route control and better intervention design, while donor-color collisions leave bilateral specificity and cross-scene portability unresolved.

### [Route Cartographer with Consumer-Closed Promotion](demos/route-cartographer-consumer-closure.md)

I use the cartographer to record native states, branches, route candidates, and endpoint outcomes, then promote an intervention only when the real image consumer improves. One update is promoted, three are rejected, and exact rollback succeeds 5/5; whole text-state transfers close the tested edges while single-token QKV routes do not. The practical use case is a safe model-debugging loop that can discover promising routes without mistaking an internal activation change for a useful image capability.

### [Scene Circuit Certificate](demos/scene-circuit-certificate.md)

I use this two-seed certificate to test whether a declared route can change scene context while controls show causal necessity, donor specificity, dose response, and consumer visibility. Minimum scene progress is 0.9133, route-ablation progress is 0.0225, and wrong-color progress is -0.4303; the image-side collateral panel shows that subjects are not perfectly preserved. This opens bounded scene editing and route certification, but not clean scene-only disentanglement.

### [Diffusion-Time Causal Clock and Image-Stream Roles](demos/diffusion-time-causal-clock.md)

I change when an intervention enters the denoising schedule to learn when image decisions become difficult to change. At relative dose 0.15, step 1 produces 0.359 final effect and 2.399× amplification, while step 7 produces 0.078 and 0.523×; character pinning, regional edits, and image-token tracing separate identity, scene, and carrier timing. This opens schedule-aware editing, checkpoint selection, and more efficient intervention search; it does not imply every semantic factor has the same temporal authority.

### [Empty-Context Positional Scaffold](demos/empty-context-positional-scaffold.md)

I remove only a small set of active-adjacent conditioning rows from an otherwise empty context and compare the result with prompt swaps and matched-position controls. Changing roughly 3.5% of the occupied rows produces large RGB changes across two seeds, showing that apparently empty context can carry a positional or tonal scaffold that affects the image. This opens better context design and warns me against treating unused conditioner space as harmless padding.

### [Temporal Carrier Compiler](demos/temporal-carrier-compiler.md)

I search across routes and denoising steps to find a carrier that can transfer an image edit to a new trajectory. The search selects a late image-stream seam and transfers part of two held-out edits with wrong-time, sign, and sham separation. This opens reusable temporal interventions, while the partial transfer shows that a carrier location alone is not yet a complete semantic editor.

## Editing, repair, and composition

### [Counterfactual Diffusion Futures](demos/counterfactual-diffusion-futures.md)

I pause a four-step generation, fork the trajectory, write a donor route state, and resume the unchanged image process. Early edits reach 0.904–0.971 progress toward the intended scene or subject, hostile donors move toward their own targets, shams stay near the source, and halfway edits are much weaker; exact replay restores every parent. This opens controlled image editing, counterfactual previews, and branching creative workflows, with the boundary that the result is a bounded donor-assisted editor rather than a universal prompt-free editor.

### [Recipient-Native Capability Patch](demos/recipient-native-capability-patch.md)

I install a tiny rank-8 recipient-local patch in a distilled FLUX.2 model to repair a counting regression. The output changes from three apples to five using 55,297 FP16 parameters, survives a fresh process without the donor path, and uninstalls exactly; held-out prompts reveal collateral changes. This opens targeted model repair and capability-specific patching, but the current patch is not general enough to ship as a universal fix.

### [Typed Snake Topology Repair and Interaction Residual](demos/typed-snake-topology-interaction.md)

I use a typed route intervention to change a closed green coil into an open S-shaped snake, reaching 0.9008 progress while ablation, wrong-axis, dose, and held-out controls reject generic image movement. A paired lighting×color panel shows a real nonlinear interaction that addition alone misses, while the first learned mixer fails to beat a held-out linear baseline. This opens structured shape editing and native interaction measurement, not a general algebra for combining arbitrary edits.

### [Nonlinear Interaction Compiler](demos/nonlinear-interaction-compiler.md)

I first establish that two edits interact in the native consumer, then train a small mixer to predict the interaction residual on held-out pairs. The learned mixer reaches 0.716 mean progress versus 0.735 for simple addition, so the image still contains a real nonlinear term but the first compiler does not generalize enough. This opens a path toward learned multi-edit composition with a clear native-consumer promotion gate.

### [Wall-Picture Hotpatch](demos/wall-picture-hotpatch.md)

I use four prompt-paired trajectories to move a framed picture to the requested side of a wall while a protected-object write preserves the frame and artwork crop. Position and opposite-direction controls pass, so the expected output is a localized scene change with the protected object retained. This opens practical spatial hotpatching for layout edits, while remaining limited to this prompt family and consumer rather than proving donor-free spatial understanding.

### [Living-Room Hotpatch](demos/living-room-hotpatch.md)

I move a couch right in four living-room trajectories, move it left with an opposite donor, keep a norm-matched sham separate, and verify exact parent replay. Native target progress reaches 0.943–0.975 and couch-region progress 0.766–0.871, strongest at an early cut. This opens localized object movement while showing that natural-language distance such as “two feet” is not yet calibrated to physical measurement.

### [Native-State Route Selector v6](demos/native-state-route-selector-v6.md)

I use an earlier native state to choose native continuation, one of two fixed repair routes, or abstention. Calibration finds a support radius with zero false-positive repairs, and every unsupported held-out case abstains while native cases match exactly. This opens fail-closed automation that refuses uncertain interventions instead of producing a confident-looking bad image; it is not yet a general semantic router.

### [Klein Seam Bisection](demos/klein-seam-bisection.md)

I search route, timestep, and stream seams to locate where a distilled recipient diverges from a base model, then try a small rank-8 repair. The search repeatedly selects `joint.2 → step 0 → text` and preserves exact split-load custody, but only one of four held-out count cells transfers. This opens a practical debugging method for finding model seams, while showing that local repair does not automatically generalize.

### [Textless Klein Renderer](demos/textless-klein-renderer.md)

I compile SceneGraph, CAD, image-derived JSON, and robot-state JSON directly into a native Klein conditioner without converting held-out inputs back into text. The transport contract works, but held-out progress ranges from -0.299 to 1.000 with mean 0.364. This opens direct structured-input rendering for design and robotics workflows, while establishing that tensor compatibility is not the same as reliable compositional semantics.

## Serving, compatibility, and model characterization

### [Exact Phase-Resident Serving, Replay, and Edit Caching](demos/exact-phase-resident-serving.md)

I separate prompt encoding from denoising so weights are not repeatedly transferred. Eight 512² generations remain pixel- and PNG-exact while running 10.66× faster per image and 6.25× faster end-to-end; exact suffix replay and reference-edit caching extend the result to zero-error branching and a median 4,696× cache-hit speedup. This opens an efficient substrate for large intervention sweeps, interactive editing, and reproducible counterfactual research.

### [Closed-Loop Students and Reference Mappers](demos/closed-loop-students-mappers.md)

I train a 3.77-million-parameter student to predict dense FLUX.2 transitions, maintain a reference register, apply uncertainty-gated corrections, and let the native consumer finish. It reaches scheduler parity cosine 0.999998, free-run image cosine 0.878 mean and 0.744 minimum, and 22.2–32.7× speed in the bounded lane. This opens fast approximate simulation and cost-effective search, but poor worst cases prevent treating it as a replacement model.

### [Cross-Family Conditioner Substitution and Repair](demos/cross-family-conditioner-repair.md)

I map foreign language-model conditioners into the native FLUX.2 `[512, 7680]` contract while the image suffix stays fixed. A complete native tensor restores the native image exactly, while learned adapters improve seen prompts but only partially preserve held-out semantics. This opens multimodel frontends and compatibility repair, with the important boundary that matching tensor shape or hidden-state similarity does not guarantee semantic interchangeability.

### [Four-Frontend Semantic ABI](demos/four-frontend-semantic-abi.md)

I test Qwen, SmolLM, and Mamba conditioners against one frozen Klein consumer across route, timestep, and stream coordinates. Typed capture, exact replay, and complete native donor transport work, but compact token/channel intersections fail and carrier values remain family-specific. This opens a disciplined design for frontend/consumer interfaces while ruling out the assumption that a small shared semantic tensor ABI already exists.

### [VAE and Decoder Output Boundary](demos/vae-decoder-output-boundary.md)

I change the decoder while holding the upstream trajectory fixed. A smaller decoder removes 43.678% of parameters, runs 1.517× faster, and reaches pixel cosine 0.999784 without exact parity across 192 outputs; a third-party VAE reaches 0.999729. This opens decoder optimization and output-boundary substitution, while showing that visual similarity is not the same as exact compatibility.

### [FLUX.2 Dev Paged Execution](demos/flux2-dev-paged-execution.md)

I execute a 112.805 GB BF16 FLUX.2 Dev artifact by paging the conditioner and denoiser so they are never co-resident. All 11 lifecycle gates pass for a one-step 512² forward and VAE decode in about 336 seconds. This opens research access to models that exceed local memory, while keeping the richer four-step diagnostic separate from any terminal quality claim.

### [Model-Family Forensics](demos/model-family-forensics.md)

I compare seven pinned BFL artifacts byte-for-byte and by trajectory behavior, covering 2,883 objects totaling 17.442 GB. The study identifies conditioner provenance, a structured 96.1081% Klein 9B→9B-KV rewrite, exact base/distilled trajectory compatibility, a bounded FLUX.1→FLUX.2 lineage result, and byte-identical VAE statics. This opens release auditing, model-lineage analysis, and safer artifact selection without claiming semantic inheritance.

### [9B and 9B-KV Head-Sensitivity Stability](demos/9b-kv-head-sensitivity.md)

I repeat four physical head ablations across a natural FLUX.2 Klein 9B/9B-KV pair whose denoisers differ by 96.1081%. The same sensitivity ordering survives the rewrite; D0H29 produces MAD 13.54 and 11.61 while S22H25 is nearly silent. This opens robust architectural debugging and helps me separate causal sensitivity from raw weight identity, without assigning semantic ownership to a single head.

### [FLUX.1 Conditioner Causal Controls](demos/flux1-conditioner-causal-controls.md)

I test a SmolLM adapter against a frozen FLUX.1 dual conditioner with native, adapted, zero, wrong-source, and native-wrong controls on held-out pairs. The adapter changes the consumer in a source-specific way, but held-out behavior remains far from native equivalence while the corrected native no-op is exact. This opens a clean compatibility benchmark and prevents false confidence from wiring success alone.

### [Behavior Taxonomy](demos/behavior-taxonomy.md)

I decompose image-model behavior into counting, typography, lexical presence, and semantic substitution instead of assigning one broad “understanding” score. Counting accuracy falls from 1.000 at two objects to 0.0625 at seven; spelling remains strong, lexical presence depends on the word, and substitutions are asymmetric. This opens better product and research diagnostics by showing which user-visible behaviors are reliable and which need targeted improvement.
