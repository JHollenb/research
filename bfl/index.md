# Black Forest Labs Experiment Index

This index explains what is being learned or built with each Black Forest Labs experiment, what changed in the model's output or execution, and what practical capability is opened—or ruled out—by the result. Detailed methods, receipts, images, controls, and verifiers are contained in the linked reports and local artifact bundles.

## Strongest experiments at a glance

| experiment | why it matters |
| --- | --- |
| [Semantic Circuit Objects](#semantic-circuit-objects-creating-symbols-and-using-them-directly-in-flux2) | Strongest synthesis: a causal semantic route is turned into a typed object symbol that can be read, edited, isolated, and written back into the model. The blue-mug value-level write works at both tested seeds, and durable manifest readback passes 11/11 checks. |
| [Objects Become Debugger I/O](#objects-become-debugger-io-deep-property-mapping-stress-and-isolation) | Image regions are mapped to lexical addresses, selective edits are demonstrated, the address is packaged as durable state, and dose, wrong-address writes, composition, and isolation are stress-tested. Fox recolor reaches 0.92/0.94 progress across two seeds, making this the clearest bridge from model internals to a usable control surface. |
| [Counterfactual Diffusion Futures](#counterfactual-diffusion-futures) | A generation is forked early, steered toward a different scene or subject, and resumed through the unchanged image process. Early branches reach 0.904–0.971 target progress, opening controlled image editing while preserving exact parents and controls. |
| [Real FLUX Hotpatch Cinema](#real-flux-hotpatch-cinema) | The native hotpatch is replicated over two semantic axes and four seeds. Early edits reach 0.904–0.971, hostile donors move toward their own factor at 0.926–0.953, and late edits fall to 0.095–0.358, establishing a strong timing- and donor-specific counterfactual trend. |
| [Exact Phase-Resident Serving](#exact-phase-resident-serving-replay-and-edit-caching) | Prompt encoding, denoising, suffix replay, and reference edits are separated while exact pixels are preserved. The measured speedups are 10.66× per image, 6.25× end-to-end, and 4,696× at the median cache hit, making expensive causal experiments practical. |
| [Route Cartographer with Consumer-Closed Promotion](#route-cartographer-with-consumer-closed-promotion) | Route interventions are promoted only when the native image consumer improves, and rejected futures are rolled back exactly. Across 685 native states and 85 branches, one update was promoted, three were rejected, and rollback succeeded 5/5. |
| [Twenty-Axis Native Semantic Route Circuit](#twenty-axis-native-semantic-route-circuit) | One causal route is tested against many independent visual factors. Six rows pass 9/9, eleven pass 7/9, and three remain candidates, providing a broad route-level capability map without overclaiming single-token ownership. |

## Object interfaces and semantic circuits

### [Semantic Circuit Objects: Creating Symbols and Using Them Directly in FLUX.2](demos/semantic-circuit-object-interface.md)

A consumer-visible semantic circuit is compiled into a typed object symbol in this synthesis. Lexical rows are localized with controlled donor/base contrasts, joined to image-space probes, and recorded with route, timing, payload, dose, and evidence fields. The symbol is used to edit, isolate, delete, compose, or numerically steer an object. The blue-mug write works at both tested seeds, while durable manifest readback passes 11/11 checks. A model-facing object interface for controllable editing and debugging is opened, but it remains exploratory rather than a universal prompt-independent API.

### [Objects Become Debugger I/O: Deep Property Mapping, Stress, and Isolation](demos/objects-debugger-io-structs-stress-isolation.md)

A three-stage experiment is used to test whether a rendered object can become a durable debugger value rather than a visual region selected after the fact. A fox and ball are mapped to lexical addresses, those addresses are proven through recolor, material, shape, movement, layering, dose, wrong-address, and isolation tests, and the result is stored as a fingerprinted manifest. Fox recolor reaches 0.92/0.94 progress across two seeds, and white-context isolation reaches above 0.91 for the fox and 0.99 for the ball. A concrete path toward object-level image tools with explicit addresses, controls, and failure modes is opened.

### [Twenty-Axis Native Semantic Route Circuit](demos/twenty-axis-semantic-route-circuit.md)

This panel tests one typed native route against twenty visual contrasts such as identity, count, lighting, and scene changes. Six rows pass the strict 9/9 gate and eleven pass a looser 7/9 carrier-level gate; movement toward the native target image is expected, while route ablation and sham controls distinguish a real consumer effect from a hidden-state correlation. A broad route map for choosing where to intervene is opened, but ownership of a named concept by any single address is not established.

### [Distributed K/V Causal Route](demos/distributed-kv-causal-route.md)

Twenty native key/value sites are probed to determine whether a color-binding effect lives in one location or across a distributed route. The effect reproduces across sites, grows nonlinearly with dose, accumulates across denoising steps, and reaches native endpoint margins of +6.740 forward and +8.830 reverse, with 83/96 and 88/96 endpoint recoveries. Distributed route control and better intervention design are opened, while donor-color collisions leave bilateral specificity and cross-scene portability unresolved.

### [Route Cartographer with Consumer-Closed Promotion](demos/route-cartographer-consumer-closure.md)

The cartographer records native states, branches, route candidates, and endpoint outcomes, after which an intervention is promoted only when the real image consumer improves. One update is promoted, three are rejected, and exact rollback succeeds 5/5; whole text-state transfers close the tested edges while single-token QKV routes do not. A safe model-debugging loop is thereby provided for discovering promising routes without mistaking an internal activation change for a useful image capability.

### [Scene Circuit Certificate](demos/scene-circuit-certificate.md)

This two-seed certificate tests whether a declared route can change scene context while causal necessity, donor specificity, dose response, and consumer visibility are measured by controls. Minimum scene progress is 0.9133, route-ablation progress is 0.0225, and wrong-color progress is -0.4303; the image-side collateral panel shows that subjects are not perfectly preserved. Bounded scene editing and route certification are opened, but clean scene-only disentanglement is not established.

### [Diffusion-Time Causal Clock and Image-Stream Roles](demos/diffusion-time-causal-clock.md)

The entry point of an intervention is changed within the denoising schedule to determine when image decisions become difficult to change. At relative dose 0.15, step 1 produces 0.359 final effect and 2.399× amplification, while step 7 produces 0.078 and 0.523×; character pinning, regional edits, and image-token tracing separate identity, scene, and carrier timing. Schedule-aware editing, checkpoint selection, and more efficient intervention search are opened; equal temporal authority across all semantic factors is not implied.

### [Empty-Context Positional Scaffold](demos/empty-context-positional-scaffold.md)

Only a small set of active-adjacent conditioning rows is removed from an otherwise empty context, and the result is compared with prompt swaps and matched-position controls. Changing roughly 3.5% of the occupied rows produces large RGB changes across two seeds, showing that apparently empty context can carry a positional or tonal scaffold that affects the image. Better context design is enabled, and unused conditioner space is shown not to be harmless padding by default.

### [Temporal Carrier Compiler](demos/temporal-carrier-compiler.md)

Routes and denoising steps are searched for a carrier that can transfer an image edit to a new trajectory. A late image-stream seam is selected, and part of two held-out edits is transferred with wrong-time, sign, and sham separation. Reusable temporal interventions are opened, while the partial transfer shows that a carrier location alone is not yet a complete semantic editor.

## Editing, repair, and composition

### [Counterfactual Diffusion Futures](demos/counterfactual-diffusion-futures.md)

A four-step generation is paused, its trajectory is forked, a donor route state is written, and the unchanged image process is resumed. Early edits reach 0.904–0.971 progress toward the intended scene or subject, hostile donors move toward their own targets, shams stay near the source, and halfway edits are much weaker; exact replay restores every parent. Controlled image editing, counterfactual previews, and branching creative workflows are opened, with the boundary that the result is a bounded donor-assisted editor rather than a universal prompt-free editor.

### [Real FLUX Hotpatch Cinema](demos/real-hotpatch-cinema.md)

The larger replicated native panel behind the counterfactual synthesis contains four specimens, two semantic axes, two denoising cuts, dose controls, hostile donors, shams, scalar confirmation, and exact rollback. Early full-dose edits reach 0.904–0.971 target progress, hostile donors reach 0.926–0.953 toward their own factor, and the same intervention at the later cut falls to 0.095–0.358. Native-consumer trajectory debugging and counterfactual image futures are opened, while timing and donor identity are shown to be part of the capability boundary.

### [Recipient-Native Capability Patch](demos/recipient-native-capability-patch.md)

A tiny rank-8 recipient-local patch is installed in a distilled FLUX.2 model to repair a counting regression. The output changes from three apples to five using 55,297 FP16 parameters, survives a fresh process without the donor path, and uninstalls exactly; held-out prompts reveal collateral changes. Targeted model repair and capability-specific patching are opened, but the current patch is not general enough to ship as a universal fix.

### [Typed Snake Topology Repair and Interaction Residual](demos/typed-snake-topology-interaction.md)

A typed route intervention changes a closed green coil into an open S-shaped snake, reaching 0.9008 progress while ablation, wrong-axis, dose, and held-out controls reject generic image movement. A paired lighting×color panel shows a real nonlinear interaction that addition alone misses, while the first learned mixer fails to beat a held-out linear baseline. Structured shape editing and native interaction measurement are opened, not a general algebra for combining arbitrary edits.

### [Nonlinear Interaction Compiler](demos/nonlinear-interaction-compiler.md)

An interaction between two edits is first established in the native consumer, after which a small mixer is trained to predict the interaction residual on held-out pairs. The learned mixer reaches 0.716 mean progress versus 0.735 for simple addition, so the image still contains a real nonlinear term but the first compiler does not generalize enough. A path toward learned multi-edit composition is opened with a clear native-consumer promotion gate.

### [Wall-Picture Hotpatch](demos/wall-picture-hotpatch.md)

Four prompt-paired trajectories are used to move a framed picture to the requested side of a wall while a protected-object write preserves the frame and artwork crop. Position and opposite-direction controls pass, so the expected output is a localized scene change with the protected object retained. Practical spatial hotpatching for layout edits is opened, while the result remains limited to this prompt family and consumer rather than proving donor-free spatial understanding.

### [Native-State Route Selector v6](demos/native-state-route-selector-v6.md)

An earlier native state is used to choose native continuation, one of two fixed repair routes, or abstention. Calibration finds a support radius with zero false-positive repairs, and every unsupported held-out case abstains while native cases match exactly. Fail-closed automation is opened, allowing uncertain interventions to be refused instead of producing a confident-looking bad image; a general semantic router is not yet established.

### [Klein Seam Bisection](demos/klein-seam-bisection.md)

Route, timestep, and stream seams are searched to locate where a distilled recipient diverges from a base model, after which a small rank-8 repair is attempted. The search repeatedly selects `joint.2 → step 0 → text` and preserves exact split-load custody, but only one of four held-out count cells transfers. A practical debugging method for finding model seams is opened, while local repair is shown not to generalize automatically.

### [Textless Klein Renderer](demos/textless-klein-renderer.md)

SceneGraph, CAD, image-derived JSON, and robot-state JSON are compiled directly into a native Klein conditioner without converting held-out inputs back into text. The transport contract works, but held-out progress ranges from -0.299 to 1.000 with mean 0.364. Direct structured-input rendering for design and robotics workflows is opened, while tensor compatibility is shown not to be the same as reliable compositional semantics.

## Source addressing and control planes

### [SourceAddress: Learning Where to Read Before Writing](demos/source-address-control-plane.md)

Source selection is separated from payload writing and native-consumer execution. On the latest Pythia panel, learned addressing plus SourceWrite reaches 59/128 outputs versus 3/128 native, 12/128 fixed-address, and 78/128 oracle; self-debugging relowering reaches 92/128 learned and 105/128 oracle on a fresh alphabet, with source-zero/native behavior exact. Qwen2.5 and Qwen3 reproduce the address role in family-local coordinates with 128/128 native fresh retrieval, while direct tensor-package reuse fails closed. A disciplined control-plane vocabulary for model interventions is opened, with payload compatibility and long continuation still open.

## Serving, compatibility, and model characterization

### [Exact Phase-Resident Serving, Replay, and Edit Caching](demos/exact-phase-resident-serving.md)

Prompt encoding is separated from denoising so that weights are not repeatedly transferred. Eight 512² generations remain pixel- and PNG-exact while running 10.66× faster per image and 6.25× faster end-to-end; exact suffix replay and reference-edit caching extend the result to zero-error branching and a median 4,696× cache-hit speedup. An efficient substrate for large intervention sweeps, interactive editing, and reproducible counterfactual research is opened.

### [Closed-Loop Students and Reference Mappers](demos/closed-loop-students-mappers.md)

A 3.77-million-parameter student is trained to predict dense FLUX.2 transitions, maintain a reference register, apply uncertainty-gated corrections, and let the native consumer finish. Scheduler parity cosine reaches 0.999998, free-run image cosine reaches 0.878 mean and 0.744 minimum, and speed reaches 22.2–32.7× in the bounded lane. Fast approximate simulation and cost-effective search are opened, but poor worst cases prevent treatment as a replacement model.

### [Cross-Family Conditioner Substitution and Repair](demos/cross-family-conditioner-repair.md)

Foreign language-model conditioners are mapped into the native FLUX.2 `[512, 7680]` contract while the image suffix remains fixed. A complete native tensor restores the native image exactly, while learned adapters improve seen prompts but only partially preserve held-out semantics. Multimodel frontends and compatibility repair are opened, with the important boundary that matching tensor shape or hidden-state similarity does not guarantee semantic interchangeability.

### [Four-Frontend Semantic ABI](demos/four-frontend-semantic-abi.md)

Qwen, SmolLM, and Mamba conditioners are tested against one frozen Klein consumer across route, timestep, and stream coordinates. Typed capture, exact replay, and complete native donor transport work, but compact token/channel intersections fail and carrier values remain family-specific. A disciplined design for frontend/consumer interfaces is opened, while the assumption that a small shared semantic tensor ABI already exists is ruled out.

### [VAE and Decoder Output Boundary](demos/vae-decoder-output-boundary.md)

The decoder is changed while the upstream trajectory is held fixed. A smaller decoder removes 43.678% of parameters, runs 1.517× faster, and reaches pixel cosine 0.999784 without exact parity across 192 outputs; a third-party VAE reaches 0.999729. Decoder optimization and output-boundary substitution are opened, while visual similarity is shown not to be the same as exact compatibility.

### [FLUX.2 Dev Paged Execution](demos/flux2-dev-paged-execution.md)

A 112.805 GB BF16 FLUX.2 Dev artifact is executed by paging the conditioner and denoiser so they are never co-resident. All 11 lifecycle gates pass for a one-step 512² forward and VAE decode in about 336 seconds. Research access to models that exceed local memory is opened, while the richer four-step diagnostic remains separate from any terminal quality claim.

### [Model-Family Forensics](demos/model-family-forensics.md)

Seven pinned BFL artifacts are compared byte-for-byte and by trajectory behavior, covering 2,883 objects totaling 17.442 GB. Conditioner provenance, a structured 96.1081% Klein 9B→9B-KV rewrite, exact base/distilled trajectory compatibility, a bounded FLUX.1→FLUX.2 lineage result, and byte-identical VAE statics are identified. Release auditing, model-lineage analysis, and safer artifact selection are opened without claiming semantic inheritance.

### [9B and 9B-KV Head-Sensitivity Stability](demos/9b-kv-head-sensitivity.md)

Four physical head ablations are repeated across a natural FLUX.2 Klein 9B/9B-KV pair whose denoisers differ by 96.1081%. The same sensitivity ordering survives the rewrite; D0H29 produces MAD 13.54 and 11.61 while S22H25 is nearly silent. Robust architectural debugging is opened, and causal sensitivity can be separated from raw weight identity without assigning semantic ownership to a single head.

### [FLUX.1 Conditioner Causal Controls](demos/flux1-conditioner-causal-controls.md)

A SmolLM adapter is tested against a frozen FLUX.1 dual conditioner with native, adapted, zero, wrong-source, and native-wrong controls on held-out pairs. The consumer changes in a source-specific way, but held-out behavior remains far from native equivalence while the corrected native no-op is exact. A clean compatibility benchmark is opened, and false confidence from wiring success alone is prevented.

### [Behavior Taxonomy](demos/behavior-taxonomy.md)

Image-model behavior is decomposed into counting, typography, lexical presence, and semantic substitution instead of being assigned one broad “understanding” score. Counting accuracy falls from 1.000 at two objects to 0.0625 at seven; spelling remains strong, lexical presence depends on the word, and substitutions are asymmetric. Better product and research diagnostics are opened by showing which user-visible behaviors are reliable and which need targeted improvement.
