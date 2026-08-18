# Black Forest Labs Experiment Index

This index is a map of the standalone BFL experiment reports in this directory. Each entry says what the experiment tests, how the intervention is evaluated, and what the evidence currently supports. The reports and their local proof bundles contain the full methods, raw receipts, images, and verifiers.

## Original ranked experiments

### 1. [Recipient-native capability patch](demos/recipient-native-capability-patch.md)

This experiment compares a full-capacity and distilled FLUX.2 Klein model, then installs a tiny rank-8 recipient-local patch at an early route and dose to repair a counting regression. It changes a three-apple output to five using only 55,297 FP16 parameters, survives a fresh process without the donor path, and uninstalls exactly; later held-out tests show that the patch is not yet general because collateral changes ordinary prompts.

### 2. [Exact phase-resident serving, replay, and edit caching](demos/exact-phase-resident-serving.md)

The serving experiment separates prompt encoding from denoising so model weights are not repeatedly transferred. Eight 512² generations are pixel- and PNG-exact while running 10.66× faster per image and 6.25× faster end-to-end; exact suffix replay and a reference-edit cache extend the result to zero-error trajectory branching and a median 4,696× cache-hit speedup.

### 3. [Counterfactual diffusion futures](demos/counterfactual-diffusion-futures.md)

Here a four-step FLUX.2 trajectory is paused, forked, edited with a donor route state, and resumed through the unchanged image generator. Early edits reach 0.904–0.971 progress toward the intended scene or subject, hostile donors move toward their own targets, shams stay non-targeted, and halfway edits fall to 0.095–0.358; exact replay restores every parent, establishing a strong bounded editing trend rather than a universal editor.

### 4. [Twenty-axis native semantic route circuit](demos/twenty-axis-semantic-route-circuit.md)

This panel tests one typed route against twenty independent visual contrasts using native targets, route transfers, and route-write ablations. Six rows pass the strict 9/9 gate, eleven pass a looser carrier-level 7/9 gate, and three remain candidates; an empty-string control confirms structural route activity without proving that any one address owns a named concept.

### 5. [Cross-family conditioner substitution and repair](demos/cross-family-conditioner-repair.md)

Foreign language-model conditioners are mapped into the native FLUX.2 `[512, 7680]` contract while the image suffix stays fixed. Copying the complete native tensor restores the native image exactly, proving the suffix is healthy; learned adapters achieve high tensor alignment and improve seen prompts, but held-out semantic fidelity remains partial, so the result establishes compatibility and repair potential rather than universal interchangeability.

### 6. [Distributed K/V causal route](demos/distributed-kv-causal-route.md)

This 20-site intervention panel asks where color-binding information travels through a native Klein generation. The effect reproduces across all sites, changes nonlinearly with dose, accumulates across denoising steps, and reaches native S4 margins of +6.740 forward and +8.830 reverse with 83/96 and 88/96 endpoint recoveries; adversarial donor-color collisions mean bilateral specificity and portability remain open.

### 7. [Typed snake topology repair and interaction residual](demos/typed-snake-topology-interaction.md)

A typed donor relay changes a closed green coil into an open S-shaped snake through a four-site route, reaching 0.9008 progress while route ablation, wrong-axis, half-dose, and held-out controls separate the effect from generic image movement. The paired composition panel reaches 0.901 for a native lighting×color interaction versus 0.396 for addition, while the first learned mixer fails to beat a held-out linear baseline.

### 8. [Diffusion-time causal clock and image-stream roles](demos/diffusion-time-causal-clock.md)

This experiment varies the denoising step at which the same intervention enters the trajectory. At relative dose 0.15, step 1 produces 0.359 final effect and 2.399× amplification, while step 7 produces 0.078 and 0.523×, with a crossover near step 4; character pinning, regional edits, and image-token tracing further show that identity, scene, and carrier roles have different temporal authority.

### 9. [Closed-loop students and reference mappers](demos/closed-loop-students-mappers.md)

A 3.77-million-parameter student predicts dense FLUX.2 transitions, keeps a reference register, applies uncertainty-gated corrections, and lets the native consumer finish the trajectory. It reaches scheduler parity cosine 0.999998, full-trajectory free image cosine 0.878 mean and 0.744 minimum, and 22.2–32.7× speed in a bounded lane; poor worst cases remain, so it is an approximation trend rather than a replacement model.

### 10. [Empty-context positional scaffold](demos/empty-context-positional-scaffold.md)

The context experiment zeros only 18 active-adjacent rows in a `[1,512,7680]` maskless conditioner and compares the result with prompt swaps and matched-position controls. That 3.5%-occupancy intervention changes RGB MAD by 41.9 and 53.2 across two seeds, comparable to whole-prompt changes, supporting a positional scaffold or tone-bank mechanism rather than the assumption that unused rows are harmless padding.

### 11. [Model-family forensics](demos/model-family-forensics.md)

Seven pinned BFL artifacts are compared byte-for-byte and by trajectory behavior, covering 2,883 objects totaling 17.442 GB. The study identifies conditioner provenance, a structured 96.1081% Klein 9B→9B-KV rewrite, exact base/distilled trajectory compatibility, a bounded FLUX.1→FLUX.2 lineage result, and byte-identical VAE statics; these are release and structure findings, not semantic inheritance claims.

### 12. [Behavior taxonomy](demos/behavior-taxonomy.md)

Instead of assigning one “understanding” score, this experiment decomposes counting, typography, lexical presence, and semantic substitution. Count accuracy falls from 1.000 at two objects to 0.0625 at seven; spelling remains strong, lexical presence is word-dependent, and substitutions are asymmetric, while an early counting-circuit hypothesis collapses under strict wording and paraphrase controls.

### 13. [Route cartographer with consumer-closed promotion](demos/route-cartographer-consumer-closure.md)

The cartographer records 685 native states, 85 branches, and 325 observations across 56 nodes and 54 edges, then promotes address-driven updates only when the native endpoint improves. One update is promoted and three are rejected with exact 5/5 rollback; whole text-state transfers close every tested joint edge at weakest return alignment 0.911, while single-token QKV routes reach only 0.001–0.227, rejecting the idea that every local address is a standalone program.

### 14. [VAE and decoder output boundary](demos/vae-decoder-output-boundary.md)

The decoder study replaces or perturbs the output boundary while holding the upstream trajectory fixed. A Small Decoder removes 43.678% of parameters, runs 1.517× faster, and reaches pixel cosine 0.999784 but never exact parity across 192 outputs; a third-party VAE reaches 0.999729 cosine, while blind output-connected probes show reachability without proving semantic necessity.

### 15. [9B and 9B-KV head-sensitivity stability](demos/9b-kv-head-sensitivity.md)

Four physical head ablations are repeated in a natural FLUX.2 Klein 9B/9B-KV pair whose denoiser values differ by 96.1081%. The same sensitivity ordering survives the rewrite—D0H29 > D0H27 > S5H26 ≫ S22H25—with D0H29 producing MAD 13.54 and 11.61 while S22H25 is nearly silent; this separates causal sensitivity from weight identity without assigning semantic ownership to a head.

### 16. [FLUX.2 Dev paged execution](demos/flux2-dev-paged-execution.md)

This guarded runtime experiment executes a 112.805 GB BF16 FLUX.2 Dev artifact by paging a 24.011B-parameter conditioner and 32.223B-parameter denoiser with explicit lifetimes, never co-resident. All 11 lifecycle gates pass for a one-step 512² forward and VAE decode in about 336 seconds; a richer four-step diagnostic is retained separately and is not promoted as a terminal quality result.

## Follow-up experiments

### 17. [Klein seam bisection](demos/klein-seam-bisection.md)

Base activations are sealed first, then a fresh distilled recipient searches 32 route × timestep × stream seams for a rank-8 repair. It selects `joint.2 → step 0 → text`, demonstrating a reproducible localized mismatch and exact split-load custody, but only one of four held-out count cells transfers, so this is not general capability restoration.

### 18. [Four-frontend semantic ABI](demos/four-frontend-semantic-abi.md)

Qwen, SmolLM, and Mamba conditioners are tested against one frozen Klein consumer over 72 route × timestep × stream coordinates. Typed capture, exact replay, and complete native donor transport work, but compact token/channel intersections fail and the carrier values remain family-specific, supporting a distributed consumer boundary rather than a shared semantic tensor ABI.

### 19. [Nonlinear interaction compiler](demos/nonlinear-interaction-compiler.md)

The experiment first proves that a native pair interaction residual is causal and dose-sensitive, then trains a 32-parameter mixer to predict it on held-out edit pairs. The learned mixer reaches 0.716 mean progress versus 0.735 for simple addition, so native nonlinear composition remains a real target while this first learned compiler is rejected as a general solution.

### 20. [Temporal carrier compiler](demos/temporal-carrier-compiler.md)

A 16-cell search over four routes and four denoising steps selects `joint.2 → step 3 → image` as the strongest image-stream carrier. The selected Act transfers part of two pair-disjoint held-out edits with strong wrong-time, sign, and sham separation, establishing late temporal authority but not a complete semantic compiler.

### 21. [Textless Klein renderer](demos/textless-klein-renderer.md)

SceneGraph, CAD, image-derived JSON, and robot/JSON states are compiled directly into a native Klein conditioner without converting held-out states back into text. The transport contract works, but held-out progress ranges from -0.299 to 1.000 with mean 0.364, showing a promising textless rendering path whose compositional semantics are not yet general.

### 22. [Wall-picture hotpatch](demos/wall-picture-hotpatch.md)

A four-seed prompt-paired trajectory edit moves a framed picture to the requested side of a wall while an explicit protected-object write preserves the exact frame/artwork crop in all four specimens. Position and opposite-direction controls pass, but the result is scoped to this prompt family and consumer; it is not donor-free spatial understanding.

### 23. [Living-room hotpatch](demos/living-room-hotpatch.md)

Four living-room trajectories are patched so a couch moves right, while an opposite donor moves it left, a norm-matched sham stays separate, and parent replay remains exact. Native target progress is 0.943–0.975 and couch-region progress is 0.766–0.871, with the effect strongest at an early cut; “two feet” remains a prompt-level instruction rather than a calibrated distance.

### 24. [Native-state route selector v6](demos/native-state-route-selector-v6.md)

A four-action selector uses an earlier native state to choose native continuation, two fixed repair routes, or abstention. Calibration finds a support radius with zero false-positive repairs, and the selector abstains on every unsupported green-circle held-out while matching native exactly; this is valuable fail-closed uncertainty evidence, not route-utility prediction or a semantic meta-router.

### 25. [Scene circuit certificate](demos/scene-circuit-certificate.md)

The two-seed scene panel certifies a reproducible native route effect: minimum scene progress is 0.9133, route-ablation progress is 0.0225, wrong-color progress is -0.4303, and exact replay passes. A separate collateral analysis shows incomplete subject preservation, so the result certifies scene-route control but not scene-only disentanglement.

### 26. [FLUX.1 conditioner causal controls](demos/flux1-conditioner-causal-controls.md)

A SmolLM adapter is tested against the frozen FLUX.1 dual conditioner with separate native, adapted, zero, wrong-source, and native-wrong controls on held-out pairs. The adapted branch changes the consumer in a source-specific way, but held-out behavior remains far from native equivalence; the corrected native no-op is exact, making this a clean negative result for semantic interchangeability rather than a wiring failure.
