---
title: "Forking a FLUX.2 generation mid-flight"
type: experiment-report
date: 2026-08-19
models:
  - id: black-forest-labs/FLUX.2-klein-4B
    revision: e7b7dc27f91deacad38e78976d1f2b499d76a294
status: "replicated editing trend on one pinned FLUX.2 checkpoint; not a portable editor"
merged_from:
  - counterfactual-diffusion-futures.md
  - real-hotpatch-cinema.md
  - wall-picture-hotpatch.md
  - diffusion-time-causal-clock.md
  - temporal-carrier-compiler.md
tags: [bfl, flux, diffusion, trajectory-editing, counterfactuals, rollback, causal-timing]
---

# Forking a FLUX.2 generation mid-flight

## What we found

A running FLUX.2 generation can be paused at a denoising step, forked into several branches,
edited, and resumed through the unchanged denoiser, scheduler, and decoder. Injecting a
content-specific edit early moves the final image toward the intended scene or subject with
progress **0.904–0.971** across two semantic axes and two seeds each; a hostile donor instead
drags the branch toward *its own* content (0.926–0.953), and an equal-size random edit does not.
The same edit applied halfway through denoising is much weaker (0.095–0.358). After every branch,
exact scalar replay restores the parent image and final latent **bit-for-bit**. This is a
replicated causal-editing trend on one pinned checkpoint, not a portable learned editor.

![Forking one FLUX.2 generation (scene axis, seed 9001). The first three cells are the endpoints: source, correct donor (desert fox), hostile donor (blue fox). An early full-dose edit lands the desert scene; the hostile edit turns the fox blue; the sham collapses to noise; the same edit at the halfway cut barely moves the image.](../artifacts/counterfactual-diffusion-futures/scene-seed9001.png)

## Why it matters / what is new

It is already known that early diffusion steps fix layout and content while late steps refine
detail: SDEdit (Meng et al. 2021) relies on this, and Prompt-to-Prompt (Hertz et al. 2022)
applies prompt edits across the schedule. Our early-vs-late timing numbers agree with that picture
and are **not** claimed as new. What is new is the engineering and controls around it: (a) exact
*fork and rollback* of a real generation, with bitwise parent recovery, so rejected branches and
the source future coexist; (b) a **hostile-donor** control showing the edit carries the donor's
specific content; (c) a spatial edit that moves one framed picture across a wall while a separate
protected-pixel write holds the artwork identical; and (d) dose and timing curves measured
end-to-end through the real decoder, not on hidden states. It is activation patching (Meng et al.
2022; Wang et al. 2022) carried to final pixels, plus a Git-style checkpoint of the generation.

## Setup

All experiments use `black-forest-labs/FLUX.2-klein-4B`, revision
`e7b7dc27f91deacad38e78976d1f2b499d76a294`, a distilled generator, at 256×256, guidance 1.0.
FLUX.2 is a dual-stream-then-single-stream diffusion transformer: `joint.i` is the *i*th
dual-stream block (text and image tokens attend separately), `single.i` the *i*th merged
single-stream block.

**The route we edit** (fork and wall experiments) is the text-stream output of `joint.2`,
`joint.3`, `joint.4` and the text rows of `single.0`, at every denoising step after the cut.
**Donor** and **source** are two real generations from the same initial latent; the **edit
vector** is donor-minus-source on that route, scaled by a **dose** and added into the source at a
saved checkpoint (the **cut**). We then run the real suffix and judge the final image. The timing
and route-search experiments instead intervene on the *image* stream and the whole latent.

**Progress P** is a normalized image-distance score: `P = 1 − d(branch, target) / d(source,
target)`, with `d` the mean absolute pixel distance. `P = 0` means source-like, `P = 1`
target-like, negative means moved away from the target.

| knob | fork panel | wall-picture | causal clock | route×time search |
|---|---|---|---|---|
| steps | 4 | 4 | 8 | 4 |
| cut(s) | 0, 2 | 0, 2 | resume k=1…7 | step 0–3 |
| doses | 0, 0.5, 1.0 | 0, 0.5, 0.75, 1.0 | relative 0.15 | 0…1.0 |
| seeds | 9001, 1337, 4242 | 4242, 9001, 1337, 7217 | per-scene | 52013, 52019 |
| stream edited | text route | text route + protected pixels | image / whole latent | image stream |

The fork panel was run once but written up twice internally; the two replication reports are
byte-identical (md5 `d46abb8f…`), so it appears once below.

## Results

### Fork, edit, resume — and selectively

Early full-dose edits land the donor; hostile edits land the hostile donor; late edits mostly wash
out. The replication passes 4/4.

| specimen | early correct | hostile: target / own | sham target | late correct |
|---|---:|---:|---:|---:|
| scene, seed 9001 | 0.916 | −0.531 / 0.953 | 0.031 | 0.165 |
| scene, seed 1337 | 0.907 | −0.508 / 0.950 | 0.029 | 0.095 |
| subject, seed 4242 | 0.971 | −0.404 / 0.926 | −0.315 | 0.099 |
| subject, seed 9001 | 0.904 | −2.810 / 0.953 | −2.176 | 0.358 |

The hostile donor (a blue fox that keeps the source pose and scene) is the decisive control: the
branch moves *away* from the declared target but strongly toward the hostile donor's own blue
target, so this is selective content transfer, not generic disruption. Dose is nonlinear and
axis-dependent: a single-specimen screen rose roughly −0.001, −0.015, 0.060, 0.485, 0.942 as dose
increased. The run used one model load, 40 logical batched suffixes in 8 physical calls, and 20
exact scalar confirmations, in 47.45 s (peak 8,232.6 MB VRAM, 18,854.9 MB RSS). Every branch
starts from an immutable checkpoint, and exact replay restores the source image and final latent
bytes.

### A spatial edit with a protected object

The route can move *where* an object is; keeping its internal marks identical needs a separate
protected write. Across four seeds the edit moves a framed abstract print to the requested side of
the wall and preserves the exact decoded frame/artwork crop.

| instrument | across four seeds |
|---|---:|
| target position progress | 1.000–1.000 |
| target picture-ROI progress | 0.916–0.969 |
| protected frame/artwork similarity | 1.000 (4/4) |
| opposite-donor position progress | −0.601 to −0.033 |
| protected similarity, opposite branch | 1.000 (4/4) |
| exact parent replay / scalar confirmation | 4/4 / 4/4 |

![Wall-picture branches (seed 4242): source, target donor (picture right), opposite donor (picture left), then dose sweeps at cut 0 and cut 2. The route moves the print and changes the scene; a protected-pixel write keeps the marbled artwork bit-identical; the opposite donor moves it the other way.](../artifacts/wall-picture-hotpatch/gallery-seed4242__cinema.png)

The route edit alone does **not** preserve the artwork — that is why the explicit protected-crop
write is part of the accepted claim. Return-to-target readings (progress 0.848–0.985, alignment
0.892–0.989) are kept only as diagnostics: one of four seeds under-reached the older 0.90 return
threshold while its exact crop and placement still passed. Earlier designs failed instructively: whole-image gates mistook artwork changes for
directional failure, a reference-image attempt produced a blank frame, and a latent transplant
dragged in wall context.

### The denoising clock: when an edit lands

The same relative edit has step-dependent influence. At resume step k=1 the final relative effect
is 0.35981 (amplification 2.3986, pixel MAD 12.9322); at k=7 it is 0.0784 (amplification 0.5226,
pixel MAD 1.1853), crossing amplification = 1 near k=4. A "cheap-deep" shortcut computes the
resume state in one forward pass instead of replaying the prefix and is bit-exact at every k (edit
relative error 0.0), giving a 7.993× speedup at k=7 — so dense timing sweeps are affordable
without changing what is measured.

![Cheap-deep is exact: the reference generation (left), its one-forward-pass reconstruction at k=3 (middle, pixel-identical), and an edit injected at k=3 and run through the real suffix (right).](../artifacts/diffusion-time-causal-clock/diffusion_cheap_deep_montage.jpg)

Pinning a character's identity shows the same clock. Injecting a reference latent into a different
scene raises latent similarity from 0.295 at k=1 to 0.9785 at k=4 and 0.9992 at k=7. A whole-image
DINOv2-small CLS cosine over four scenes gives −0.0209, 0.1793, 0.6966,
0.9914, 0.9991 at k=1,2,3,4,6, with pinned-vs-baseline persistence 0.7913 vs −0.008 — a strong
*whole-image* identity trend, not a face-crop guarantee. Regional replacement trades identity for
scene: a 0.7 box at steps 2–7 reaches reference 0.5249 / scene 0.4107, while a 0.5 box at steps
2–4 reaches reference 0.2011 / scene 0.7283.

![Character pinning across resume step: by replace@k4 the output face matches the reference portrait; blends at k=2–3 keep more of the hiking scene.](../artifacts/diffusion-time-causal-clock/character_pin_montage.jpg)

Image-stream sites play different operational roles (a carrier here = a hidden state that moves
content downstream): `joint.4:image` an upstream carrier (unit-dose progress ≈0.445),
`single.0:image` the most reproducible scene carrier, `single.10:image` a semantic amplifier
(≈0.589), `single.19:image` a late readout (absolute replacement reaches 1.000 but has little
influence left to reshape the scene).

### Route × time search

Searching four image-stream routes × four steps (16 candidates) selected `joint.2`, step 3, image
stream. Influence rose over the trajectory — 0.035, 0.228, 0.508, 0.722 at steps 0–3 — and the
selected edit vector transferred part of two pair-disjoint held-out edits (mean target progress
0.545, return progress 0.717, return alignment 0.978) with controls near zero: zero-dose 0.000,
wrong-time 0.001, sham −0.008, sign-flip 0.047, and exact no-op replay at RGB MAD 0.0. The edit
transfers only *part* of the target behavior, so this stays exploratory.

![One pair-disjoint held-out result (lighting × relation, seed 52013), judged on the final decoded image.](../artifacts/temporal-carrier-compiler/lighting__relation__seed-52013.png)

## Is this more than swapping the prompt?

A full-dose edit of this route from step 0 may be close to simply swapping the prompt at that step
— both change the text-stream state the suffix reads. The controls above rule out several nulls
(generic perturbation, energy-matched noise, wrong timing, sign flip) but do not yet separate an
early full-dose edit from prompt replacement. A direct control comparing the two is being run.

<!-- PROMPT-SWAP-CONTROL -->

What is *not* reducible to prompt-swapping is the surrounding structure: bitwise parent recovery,
the hostile-donor specificity, the early-to-late influence drop, and moving an object while a
protected write holds its pixels fixed.

## Controls

- **Hostile donor** — rules out generic disruption; the branch follows the donor's content.
- **Norm-matched sham** — rules out perturbation *energy* as the cause (not manifold membership).
- **Late cut / wrong-time** — rules out a time-invariant edit; influence depends on step.
- **Zero-dose** — recovers the source exactly; rules out harness leakage.
- **Sign-flip** — direction matters; rules out magnitude-only effects.
- **Opposite donor (wall)** — rules out "any edit moves it right"; it moves the other way.
- **Exact scalar replay** — RGB MAD 0.0 for no-op, bit-exact parent; rules out numeric drift.
- **Protected-crop pixel test (wall)** — rules out whole-image similarity standing in for fidelity.
- **Cheap-deep parity** — rules out the fast timing sweep changing the measured object.
- **Baseline / pairwise identity** — rules out background similarity passing as identity.

## Limits and open questions

- The edit vector is built from a paired native donor trajectory; portability to unseen prompts, objects, revisions, resolutions, and donor-free serving is open. No optimizer learns a reusable edit package.
- Early-vs-late timing is a trend for this model, route, and schedule — consistent with SDEdit, not a universal timing law. Zero late effect does not prove a site is irrelevant; it may be outside the remaining causal window.
- Dose is nonlinear and semantic-/axis-dependent; a scalar dose is not a linear strength control.
- The norm-matched sham controls energy, not manifold membership; its destructive images are not evidence that all same-norm edits are unsafe.
- Wall-picture: the route edit alone does not preserve the object (needs a protected write); one of four seeds under-reached the older 0.90 return threshold; placement is a prompt-level target, not a calibrated world coordinate; no donor-free spatial capability.
- Causal clock: whole-latent replacement imports the reference portrait's composition, and whole-image DINOv2 conflates identity with background, so these are whole-image trends, not face-crop recognition; regional editing trades identity for scene; the panel is small (one model, one resolution, few steps, small seed set); image-stream role labels are operational, not claims that a site owns a human semantic, and may not transfer across families.
- Route×time search is raw/exploratory: the selected edit transfers only part of the target behavior, and it avoids cross-prompt text replacement (text lengths differ) by testing a shape-safe image-stream boundary.
- Open: is a step-0 full-dose route edit distinguishable from a prompt swap? (control pending, above.)

## Reproduce and inspect

Each bundle under `../artifacts/` holds the report JSON, run record, figures, and a `verify.py`
that re-checks the reported gates from this directory.

- Fork panel: [`counterfactual-diffusion-futures/`](../artifacts/counterfactual-diffusion-futures/) and the byte-identical [`real-hotpatch-cinema/`](../artifacts/real-hotpatch-cinema/) (the latter also keeps the single-specimen precursor report).
- Spatial edit: [`wall-picture-hotpatch/`](../artifacts/wall-picture-hotpatch/) (report, admitted certificate, galleries).
- Causal clock: [`diffusion-time-causal-clock/`](../artifacts/diffusion-time-causal-clock/) (resume-at-k, cheap-deep, character-pin, face-id, regional, image-token role map).
- Route×time search: [`temporal-carrier-compiler/`](../artifacts/temporal-carrier-compiler/) (report, run record, four held-out images).

Additional internal run logs are available on request.
