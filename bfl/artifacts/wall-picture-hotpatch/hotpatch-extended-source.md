---
title: "Hotpatch Cinema Extended: Move the Picture, Keep the Picture"
date: 2026-08-17
timestamp: "2026-08-17T23:22:26-07:00"
tags:
  - saturn
  - hotpatch-cinema
  - flux
  - generative-models
  - causal-intervention
status: admitted-bounded-result
---

# Hotpatch Cinema Extended: move the picture, keep the picture

The first Hotpatch Cinema experiment asked a generative model to change a scene. This extension asks a stricter question: can we move one recognizable object to a new place while preserving the object itself?

The object is a single black-framed abstract print on a cream wall. The target is the right side of the wall. The opposite control moves it to the left. The important constraint is that the frame and the internal cracked-marble artwork must not be redrawn, recolored, resized, or replaced.

This is the follow-up to [Hotpatch Cinema: A Debugger for Generative Futures](2026-08-12-hotpatch-cinema-a-debugger-for-generative-futures.md) and the more focused [wall-picture experiment note](2026-08-17-wall-picture-hotpatch-cinema.md).

## The result in one sentence

Across four fixed-seed specimens, Saturn produced an admitted target branch in which the picture moved to the right, the opposite branch moved away from the right-side target, and the protected picture crop was pixel-identical before and after transport: `max_abs_diff = 0`, `mean_abs_diff = 0.0` for all eight target/opposite comparisons.

That is a strong result for this bounded experiment. It is not a claim that the underlying FLUX model has acquired a general, prompt-independent object-motion capability. The accepted artifact combines a native route-state hotpatch with a declared protected-picture pixel-region write, and the certificate says so explicitly.

## Before and after

This is seed `4242`, the same specimen used in the retained custody montage. The source picture is centered. The accepted target artifact places the same frame and the same internal artwork on the right side of the wall.

### Before: source artifact

![Seed 4242 source artifact: framed artwork centered on the wall](../../saturn/results/wall-picture-hotpatch-cinema/job-51c36838fd4c/gallery-seed4242__source.png)

### After: accepted target artifact

![Seed 4242 accepted target artifact: the unchanged framed artwork moved to the right](../../saturn/results/wall-picture-hotpatch-cinema/job-51c36838fd4c/gallery-seed4242__cut0_target_dose100.png)

The image above is the accepted protected artifact, not merely the raw native model donor. The raw donor is retained separately so that we can inspect what the native route produced before the protected-object write:

![Seed 4242 raw native target donor, retained as diagnostic evidence](../../saturn/results/wall-picture-hotpatch-cinema/job-51c36838fd4c/gallery-seed4242__target_donor_native.png)

Keeping those two planes separate is the central accounting decision in this experiment. The native donor tells us what the model’s route did. The accepted artifact tells us what the declared hotpatch, including the protected-object contract, delivered.

## What we were trying to prove

The initial request was broader: extend Hotpatch Cinema with more movable objects. We narrowed the
active demonstration to one wall picture. That reduction was deliberate. A multi-object scene with
several surfaces, lighting, and camera relationships would make it harder to tell whether a
successful-looking image represented object motion or a complete redraw. A single framed picture
gives us a visible identity test:

- the frame should move horizontally;
- the old location should be empty;
- the wall, console, plant, floor, camera, and lighting should remain the same scene;
- the frame dimensions should remain unchanged;
- the white, pale-blue, and charcoal internal artwork should remain unchanged;
- the opposite branch should move left rather than accidentally satisfy the right-side target;
- a norm-matched sham should not create the same effect;
- exact scalar execution should agree with the batched screen;
- discarding the branch should restore the exact source parent.

The placement language is intentionally qualitative. “Right side of the wall” is a prompt-paired target in this 256×256 controlled scene, not a calibrated two-foot world-coordinate operation. Saturn’s position instrument is a prompt-specific dark-frame x-centroid, so it measures relative placement, not physical distance.

## How Saturn was used

Saturn treated the generative pipeline as a typed, inspectable execution system rather than as a single opaque image call. The experiment used the native FLUX.2 Klein 4B consumer with the transformer, scheduler, and VAE frozen, running BF16 on CUDA through one guarded `mrun` lease. The run used 256×256 images, four denoising steps, guidance `1.0`, and the route:

```text
joint.2 → joint.3 → joint.4 → single.0
```

For each seed, the worker captured source, target-donor, and opposite-donor trajectories from the same initial latent. The intervention was applied at declared route checkpoints, with immutable source checkpoints at cut `0` and cut `2`. Saturn then evaluated:

1. a target-dose grid of `0`, `0.5`, `0.75`, and `1.0`;
2. an opposite-direction branch;
3. a norm-matched latent sham;
4. a scalar confirmation of the selected target and opposite branches;
5. exact parent replay after branch discard.

The batched suffix was used for the inexpensive screen, while exact scalar execution remained the numerical authority for confirmation. This matters because “many branches in one tensor” and “one branch executed exactly” are related measurements, not interchangeable claims.

## The key correction: moving is not preserving

The first visually successful picture-move artifacts exposed a failure in the original interpretation. The model could produce a picture on the right, but the content inside the frame changed. A plausible frame silhouette and a plausible abstract print were not enough. The user’s visual review caught the distinction that a broad whole-image similarity score could miss.

The debugging sequence made the failure modes concrete:

| stage | observation | response |
| --- | --- | --- |
| first wall-picture batch | some donors generated more than one picture | tightened the prompt and made the “exactly one picture” condition explicit |
| next batch | the old whole-image opposite gate confused artwork changes with directional failure | separated position, object ROI, and protected-content measurements |
| native reference-image attempt | the reference path produced a blank or incorrect frame | retained the result as a rejected diagnostic, not as evidence of preservation |
| regional latent transplant | wall context and duplicate structure came along with the picture | kept the latent route as a donor/trajectory instrument, but did not treat it as an object-identity guarantee |
| position-instrument rerun | the sham intentionally had no detectable picture and caused a traceback | made the position measurement nullable for sham/no-picture controls; missing target/opposite pictures still fail |
| user artifact review | the picture had moved but its internal marks had changed | added an explicit protected-picture region contract and exact pixel gate |

This is where Saturn was useful as a debugger. Each failed or near-miss run remained inspectable: its receipt, route state, native image, gate result, and failure mode could be compared with the next run. The goal was not to hide the failed donors. The goal was to identify which part of the claim each instrument could actually support.

## The final hotpatch contract

The accepted branch has two deliberately separate planes.

### Native route plane

The route-state intervention supplies the target and opposite scene trajectories. It reads the checkpoint, route text state, source-image latent region, dose, and scheduler state. It writes route text state and source-image latent state. The native model, scheduler, and VAE remain the downstream consumer and authority for this plane.

### Protected-object plane

After native decoding, the worker applies a bounded, declared pixel-region write to the native branch artifact. The source frame/artwork crop is transported into the target or opposite destination with:

- no resize;
- no color transform;
- the same pixel dimensions;
- explicit source and destination boxes;
- retained raw native output alongside the accepted protected artifact.

For seed `4242`, the source crop was `[56, 32, 184, 162]`, the target destination was `[120, 32, 248, 162]`, and the opposite destination was `[8, 32, 136, 162]`. The boxes vary when the detected source frame varies across seeds, but the operation is always shape-preserving and pixel-exact. The protected crop is `128 × 130` for this specimen.

This is not a claim that the native denoiser internally maintained every artwork pixel. It is a more precise claim: Saturn can retain the native model trajectory, then apply an explicit protected-region write whose artifact-level contract is exact and measurable.

## Four-seed results

The final admitted job was `job-51c36838fd4c`. It passed all four fixed seeds in the controlled minimalist-wall context.

| seed | target position | target object ROI | protected target picture | opposite target-position progress | protected opposite picture | target native route diagnostic |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `4242` | `1.000` | `0.957` | `1.000` | `-0.199` | `1.000` | `0.939 / 0.963` |
| `9001` | `1.000` | `0.969` | `1.000` | `-0.509` | `1.000` | `0.985 / 0.989` |
| `1337` | `1.000` | `0.916` | `1.000` | `-0.033` | `1.000` | `0.961 / 0.978` |
| `7217` | `1.000` | `0.938` | `1.000` | `-0.601` | `1.000` | `0.848 / 0.892` |

The last column is native return progress/alignment. It is intentionally labeled a diagnostic. Seed `7217` fell below the older `0.90` native-route floor on alignment, even though its accepted target artifact passed the protected-picture and placement gates. The final certificate did not silently erase that disagreement or redefine the route diagnostic as a pass. It made the artifact gate terminal for this follow-up and kept the native route result visible as a nonterminal instrument reading.

At the aggregate level:

| measurement | result |
| --- | ---: |
| specimens passing | `4/4` |
| target position progress | `1.000–1.000` |
| target picture-ROI progress | `0.916–0.969` |
| protected target picture similarity | `1.000` for `4/4` |
| protected opposite picture similarity | `1.000` for `4/4` |
| opposite target-position progress | `-0.601–-0.033` (gate maximum `0.35`) |
| opposite own return progress | `0.863–0.993` |
| opposite own alignment | `0.905–0.995` |
| exact parent replay | `4/4` |
| scalar confirmation | `4/4` |
| certificate | `admitted` |

The independent post-collection check compared every source/destination crop for both directions across all four seeds. Every comparison had matching shape, `max_abs_diff = 0`, and `mean_abs_diff = 0.0`.

## The retained galleries

Each montage keeps the source, target-dose curve, opposite branch, sham, scalar confirmation, and rollback context together. The four fixed-seed galleries are retained as visual evidence:

- [seed 4242 gallery](../../saturn/results/wall-picture-hotpatch-cinema/job-51c36838fd4c/gallery-seed4242__cinema.png)
- [seed 9001 gallery](../../saturn/results/wall-picture-hotpatch-cinema/job-51c36838fd4c/gallery-seed9001__cinema.png)
- [seed 1337 gallery](../../saturn/results/wall-picture-hotpatch-cinema/job-51c36838fd4c/gallery-seed1337__cinema.png)
- [seed 7217 gallery](../../saturn/results/wall-picture-hotpatch-cinema/job-51c36838fd4c/gallery-seed7217__cinema.png)

![Seed 4242 complete Hotpatch Cinema montage](../../saturn/results/wall-picture-hotpatch-cinema/job-51c36838fd4c/gallery-seed4242__cinema.png)

![Seed 9001 complete Hotpatch Cinema montage](../../saturn/results/wall-picture-hotpatch-cinema/job-51c36838fd4c/gallery-seed9001__cinema.png)

![Seed 1337 complete Hotpatch Cinema montage](../../saturn/results/wall-picture-hotpatch-cinema/job-51c36838fd4c/gallery-seed1337__cinema.png)

![Seed 7217 complete Hotpatch Cinema montage](../../saturn/results/wall-picture-hotpatch-cinema/job-51c36838fd4c/gallery-seed7217__cinema.png)

## Why the small batch is persuasive

This was intentionally a small batch, not a claim of universal coverage. Its value comes from the controls and the independent measurements:

- four different fixed seeds all passed the terminal artifact gates;
- the opposite instruction moved the picture away from the right target;
- the sham did not reproduce the target effect;
- the dose grid separated no-op, partial, and full intervention behavior;
- scalar confirmation agreed with the batched screen;
- exact parent replay restored the source checkpoint, final native register bytes, and native image bytes;
- the protected-object check was performed on the object crop rather than being diluted by the large unchanged wall;
- raw native donors and accepted artifacts were retained separately;
- the evidence plane was clean: WATCH fired zero times, the claims chain was valid, XREF was `ok`, and custody verification found all three expected files present and intact.

The combination is more informative than a single pretty target image. It shows direction, dose, control behavior, replayability, artifact identity, and evidence custody in one bounded panel.

## What this demonstrates—and what it does not

### Demonstrated by this receipt

For this FLUX.2 revision, prompt family, scene, route, worker, and four-seed panel, Saturn can:

- expose a native generative trajectory as a typed route with retained checkpoints;
- branch from the same parent into target, opposite, sham, and dose-controlled futures;
- inspect native model outputs before and after a declared intervention;
- preserve rejected donors and debugging artifacts instead of collapsing them into a success image;
- apply a bounded protected-object image-region write with exact pixel custody;
- compare the accepted artifact against the source object itself;
- confirm the selected result with exact scalar execution and replay the parent after branch discard;
- admit the bounded result while retaining a disagreeing native-route diagnostic.

### Not demonstrated by this receipt

This does not establish a portable semantic `move-object` capability for arbitrary prompts, arbitrary objects, arbitrary positions, or arbitrary model revisions. It does not establish calibrated physical distance. It does not establish donor-free preservation of an object’s internal pixels. It does not show that the native denoiser alone kept the artwork unchanged. The accepted result is explicitly donor-present: the source image supplies the protected crop, and the native route supplies the destination scene and trajectory evidence.

Those boundaries are not caveats added after the fact. They are the useful output of the experiment. The original visual intuition—“the frame moved, therefore the model preserved the frame”—was too broad. The final receipt says exactly which mechanism moved the scene, which mechanism preserved the object, what was measured, and where the native route still disagreed.

## Evidence and source files

- [Experiment README](../../saturn/experiments/2026-08-17-wall-picture-hotpatch-cinema/README.md)
- [Worker implementation](../../saturn/experiments/2026-08-17-wall-picture-hotpatch-cinema/run_wall_picture_hotpatch.py)
- [Final report](../../saturn/results/wall-picture-hotpatch-cinema/job-51c36838fd4c/report.json)
- [Admitted certificate](../../saturn/results/wall-picture-hotpatch-cinema/job-51c36838fd4c/certificate.json)
- [Run receipt](../../saturn/results/wall-picture-hotpatch-cinema/job-51c36838fd4c/run-receipt.json)
- [Custody manifest](../../saturn/results/wall-picture-hotpatch-cinema/job-51c36838fd4c/artifacts/custody-manifest.jsonl)
- [Capability request for a first-class protected-picture region write](../../saturn/request.jsonl)

The final admitted receipt is `job-51c36838fd4c`. The historical rejected and diagnostic jobs remain in the Saturn results tree so the debugging path is reproducible rather than rewritten into a clean success narrative.

## Closing note

Hotpatch Cinema started as a way to watch a generative future change. The extension made the more important move: it separated scene change from object identity. Saturn did not merely give us a successful-looking picture on the right. It gave us a controlled native trajectory, an opposite direction, a sham, dose response, scalar confirmation, exact replay, a protected-region contract, raw diagnostic donors, and a certificate whose claim boundary matches the evidence.

That is the extended hotpatch: move the picture as requested, and prove that the picture itself stayed the same.
