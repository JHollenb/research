---
title: "Preregistration: prompt-held-out replication of the certified semantic route"
type: preregistration
status: frozen
date: 2026-09-22
parent: ../../paper.md
---

# Preregistration -- prompt-held-out replication of the certified FLUX.2 Klein 4B semantic route

**Frozen: 2026-09-22, before any generation job for this experiment was submitted.**
After the first run this document is not edited; corrections are appended as dated amendments in the log at the end, with reasons.

## 1. Motivation and hypothesis

The paper certifies a recurring four-block semantic transport route in a public text-to-image diffusion transformer across a panel of twenty prompt contrasts, and confirms it on two previously unopened random seeds. Section 9 states the remaining open follow-up verbatim: *"Prompt-held-out replication (new contrasts, not just new seeds) has not been run."* A route that only carries the exact twenty discovery prompts would be far weaker evidence than one that carries the same twenty semantic *transformations* expressed on new subjects and scenes.

**Hypothesis under test.** The certified transport route generalises to new prompt contrasts: applying each axis's semantic delta to a different subject and/or scene reproduces the same causal-gate outcomes, on held-out prompts, that the discovery prompts produced.

This is a confirmatory test with the decision rule, thresholds, contrasts, seeds, and route fixed in advance. A negative result (the route does not survive new prompts) is a valid and reportable outcome.

## 2. Fixed design

Everything below is held identical to the frozen discovery configuration except the three fields listed in section 2.4.

### 2.1 Model and generation recipe (unchanged from the certified panel)

- Model: `black-forest-labs/FLUX.2-klein-4B`, revision `e7b7dc27f91deacad38e78976d1f2b499d76a294`.
- Precision bfloat16; resolution 256x256; 4 denoising steps; guidance 1.0.
- Every intervention is a checkpoint-replay branch with the exact no-op guarantee (an untouched replay reproduces the original generation to zero pixel difference); all branches share the frozen suffix.

### 2.2 Route sites (unchanged)

Interventions patch the text-stream output of `joint.2`, `joint.3`, `joint.4` and the text-prefix rows of `single.0`, at all four denoising steps. Edge-mediation is tested at denoising step 2 (identical to the certified panel). Dose curve: [0.0, 0.25, 0.5, 0.75, 1.0].

### 2.3 Frozen gate thresholds (copied verbatim from the frozen config)

The nine promotion gates and their numeric thresholds are byte-identical to the certified panel. The frozen discovery configuration has SHA-256:

    9701c9ed08bb668cc73a4c1b20b3dfda736f50ae3eba87a3a1bc2cec55265135

Its threshold block, reproduced here and used unchanged:

| threshold | value |
|---|---|
| `sufficiency_min_scene_progress` | `0.9` |
| `necessity_max_scene_progress` | `0.15` |
| `specificity_max_wrong_scene_progress` | `0.35` |
| `specificity_max_sham_scene_progress` | `0.35` |
| `specificity_min_wrong_color_margin` | `0.1` |
| `dose_start_max_scene_progress` | `0.15` |
| `dose_endpoint_min_scene_progress` | `0.9` |
| `dose_image_monotonic_tolerance` | `0.1` |
| `dose_return_monotonic_tolerance` | `0.05` |
| `mediation_min_rescue_fraction` | `0.5` |
| `consumer_min_scene_return_progress` | `0.75` |
| `consumer_min_scene_return_alignment` | `0.8` |

Tiers (paper's definitions, stated plainly):
- **strict / certified** = all nine gates pass (including the two strict pixel gates: full-dose sufficiency >= 0.90 and the dose endpoints).
- **carrier / route-level** = the seven causal-route gates pass (reproducibility, necessity, wrong-axis specificity, energy/sham specificity, edge mediation, consumer continuation, exact-replay), with only the two strict pixel gates open.
- **open** = at least one causal-route gate is open.

### 2.4 The only changed fields

Created by copying the frozen config and changing **only**:

1. **prompts** -- two new prompt contrasts per original axis (section 3), each differing from the discovery prompt in subject and/or scene wording while holding the semantic delta fixed;
2. **seeds** -- `[4242, 9001, 20260922]` (the two discovery seeds 4242/9001, so the seed is held constant against discovery, plus one held-out seed 20260922 not previously used as a seed in the config or results trees);
3. **experiment name** -- a new unique run identifier, echoed in every job receipt.

Route, thresholds, mediation step, dose curve, model, revision, resolution, steps, and guidance are byte-identical to the frozen config (verified by field-wise comparison). The full contrast set and thresholds are enumerated verbatim in sections 3 and 2.3 below; the byte-exact configuration file (SHA-256 recorded below) is retained in the private experiment tree rather than this public directory, because it embeds host-specific paths.

New (prompt-held-out) configuration SHA-256, recorded before submission:

    846d1e1ee205f2406dbcb87f2336dfb260e6e0c2c69137224a52b2c0042b2a3d

Execution: the certification worker runs the panel in bounded groups on one resident model lease per group (the group size follows the frozen grouping rule; at three seeds this is four axes per group, ten groups). Each group is one scheduled GPU job. Grouping and per-branch counts are a scheduling detail and change no gate.

## 3. The held-out prompt contrasts (verbatim)

Forty contrasts: two new subject/scene rewordings for each of the twenty original axes. For each, the specificity distractor (`wrong_axis`) changes a *different* attribute than the one under test, mirroring the construction of the discovery distractor. `id` suffix `__pa`/`__pb` denotes the two rewordings.

### size_small_large  --  small -> large  (discovery tier: **carrier**)

- **`size_small_large__pa`**
  - source: "a photorealistic small brown dog sitting on a grassy lawn at noon, bright light"
  - target: "a photorealistic large brown dog sitting on a grassy lawn at noon, bright light"
  - wrong_axis: "a photorealistic small white dog sitting on a grassy lawn at noon, bright light"
- **`size_small_large__pb`**
  - source: "a photorealistic small gray elephant standing in a savanna at midday, warm light"
  - target: "a photorealistic large gray elephant standing in a savanna at midday, warm light"
  - wrong_axis: "a photorealistic small brown elephant standing in a savanna at midday, warm light"

### fur_short_long  --  short fur -> long fur  (discovery tier: **strict**)

- **`fur_short_long__pa`**
  - source: "a photorealistic short-haired brown dog sitting on a wooden porch at noon, warm light"
  - target: "a photorealistic long-haired brown dog sitting on a wooden porch at noon, warm light"
  - wrong_axis: "a photorealistic short-haired white dog sitting on a wooden porch at noon, warm light"
- **`fur_short_long__pb`**
  - source: "a photorealistic short-haired gray rabbit on a green lawn at midday, bright light"
  - target: "a photorealistic long-haired gray rabbit on a green lawn at midday, bright light"
  - wrong_axis: "a photorealistic short-haired brown rabbit on a green lawn at midday, bright light"

### eyes_green_blue  --  green eyes -> blue eyes  (discovery tier: **carrier**)

- **`eyes_green_blue__pa`**
  - source: "a photorealistic golden retriever with green eyes sitting on a lawn at noon, bright light"
  - target: "a photorealistic golden retriever with blue eyes sitting on a lawn at noon, bright light"
  - wrong_axis: "a photorealistic golden retriever with green eyes standing alert on a lawn at noon, bright light"
- **`eyes_green_blue__pb`**
  - source: "a photorealistic gray husky with green eyes lying on a wooden floor, soft light"
  - target: "a photorealistic gray husky with blue eyes lying on a wooden floor, soft light"
  - wrong_axis: "a photorealistic gray husky with green eyes standing alert on a wooden floor, soft light"

### marking_solid_tuxedo  --  solid -> tuxedo markings  (discovery tier: **carrier**)

- **`marking_solid_tuxedo__pa`**
  - source: "a photorealistic solid brown dog sitting on a grassy lawn at noon, bright light"
  - target: "a photorealistic black-and-white spotted dog sitting on a grassy lawn at noon, bright light"
  - wrong_axis: "a watercolor illustration of a solid brown dog sitting on a grassy lawn at noon, bright light"
- **`marking_solid_tuxedo__pb`**
  - source: "a photorealistic solid gray horse standing in a meadow at midday, warm light"
  - target: "a photorealistic black-and-white pinto horse standing in a meadow at midday, warm light"
  - wrong_axis: "a watercolor illustration of a solid gray horse standing in a meadow at midday, warm light"

### identity_cat_fox  --  black cat -> red fox  (discovery tier: **strict**)

- **`identity_cat_fox__pa`**
  - source: "a photorealistic orange tabby cat sitting on a windowsill in a sunlit room"
  - target: "a photorealistic small beagle dog sitting on a windowsill in a sunlit room"
  - wrong_axis: "a photorealistic black cat sitting on a windowsill in a sunlit room"
- **`identity_cat_fox__pb`**
  - source: "a photorealistic brown squirrel perched on a tree stump in a forest clearing"
  - target: "a photorealistic gray rabbit perched on a tree stump in a forest clearing"
  - wrong_axis: "a photorealistic white squirrel perched on a tree stump in a forest clearing"

### geometry_snake_straight_coil  --  straight -> coiled snake  (discovery tier: **carrier**)

- **`geometry_snake_straight_coil__pa`**
  - source: "a photorealistic yellow snake stretched in a straight line across a sandy desert at noon, harsh light"
  - target: "a photorealistic yellow snake tightly coiled on a sandy desert at noon, harsh light"
  - wrong_axis: "a photorealistic tan leather belt stretched in a straight line across a sandy desert at noon, harsh light"
- **`geometry_snake_straight_coil__pb`**
  - source: "a photorealistic green garden hose stretched in a straight line across a lawn at midday, bright light"
  - target: "a photorealistic green garden hose tightly coiled on a lawn at midday, bright light"
  - wrong_axis: "a photorealistic gray metal chain stretched in a straight line across a lawn at midday, bright light"

### pose_sitting_lying  --  sitting -> lying  (discovery tier: **open**)

- **`pose_sitting_lying__pa`**
  - source: "a photorealistic brown dog sitting on a grassy lawn at noon, bright light"
  - target: "a photorealistic brown dog lying on its side on a grassy lawn at noon, bright light"
  - wrong_axis: "a photorealistic brown dog sitting beside a blue bucket on a grassy lawn at noon, bright light"
- **`pose_sitting_lying__pb`**
  - source: "a photorealistic gray cat sitting on a wooden floor in a sunlit room"
  - target: "a photorealistic gray cat lying on its side on a wooden floor in a sunlit room"
  - wrong_axis: "a photorealistic gray cat sitting beside a yellow ball on a wooden floor in a sunlit room"

### action_sitting_jumping  --  sitting -> leaping  (discovery tier: **carrier**)

- **`action_sitting_jumping__pa`**
  - source: "a photorealistic brown dog sitting on a grassy lawn at noon, bright light"
  - target: "a photorealistic brown dog leaping across a grassy lawn at noon, bright light"
  - wrong_axis: "a photorealistic brown dog standing alert on a grassy lawn at noon, bright light"
- **`action_sitting_jumping__pb`**
  - source: "a photorealistic red squirrel sitting on a forest floor at midday, dappled light"
  - target: "a photorealistic red squirrel leaping across a forest floor at midday, dappled light"
  - wrong_axis: "a photorealistic red squirrel standing alert on a forest floor at midday, dappled light"

### orientation_left_right  --  facing left -> facing right  (discovery tier: **strict**)

- **`orientation_left_right__pa`**
  - source: "a photorealistic brown owl perched on a branch facing left in a forest at dusk, dim light"
  - target: "a photorealistic brown owl perched on a branch facing right in a forest at dusk, dim light"
  - wrong_axis: "a photorealistic white owl perched on a branch facing left in a forest at dusk, dim light"
- **`orientation_left_right__pb`**
  - source: "a photorealistic golden retriever facing left while sitting on a beach at noon, bright sunlight"
  - target: "a photorealistic golden retriever facing right while sitting on a beach at noon, bright sunlight"
  - wrong_axis: "a photorealistic black dog facing left while sitting on a beach at noon, bright sunlight"

### ears_upright_folded  --  upright -> folded ears (eye-openness proxy)  (discovery tier: **carrier**)

- **`ears_upright_folded__pa`**
  - source: "a photorealistic brown dog with upright ears sitting on a lawn at noon, bright light"
  - target: "a photorealistic brown dog with folded-back ears sitting on a lawn at noon, bright light"
  - wrong_axis: "a photorealistic brown dog with upright ears sitting on a snowy hill at dusk, cool light"
- **`ears_upright_folded__pb`**
  - source: "a photorealistic gray rabbit with upright ears on a wooden table, soft light"
  - target: "a photorealistic gray rabbit with folded-back ears on a wooden table, soft light"
  - wrong_axis: "a photorealistic gray rabbit with upright ears on a grassy field at noon, bright light"

### relation_beside_behind_ball  --  beside ball -> behind ball  (discovery tier: **strict**)

- **`relation_beside_behind_ball__pa`**
  - source: "a photorealistic brown puppy sitting beside a blue bucket on a green lawn at noon, bright light"
  - target: "a photorealistic brown puppy sitting behind a blue bucket on a green lawn at noon, bright light"
  - wrong_axis: "a photorealistic white puppy sitting beside a blue bucket on a green lawn at noon, bright light"
- **`relation_beside_behind_ball__pb`**
  - source: "a photorealistic gray kitten sitting beside a yellow box on a wooden floor, soft indoor light"
  - target: "a photorealistic gray kitten sitting behind a yellow box on a wooden floor, soft indoor light"
  - wrong_axis: "a photorealistic orange kitten sitting beside a yellow box on a wooden floor, soft indoor light"

### relation_on_under_furniture  --  on chair -> under table  (discovery tier: **open**)

- **`relation_on_under_furniture__pa`**
  - source: "a photorealistic brown dog sitting on a wooden bench in a quiet room, soft window light"
  - target: "a photorealistic brown dog sitting under a wooden desk in a quiet room, soft window light"
  - wrong_axis: "a photorealistic white dog sitting on a wooden bench in a quiet room, soft window light"
- **`relation_on_under_furniture__pb`**
  - source: "a photorealistic orange cat sitting on a red sofa in a living room, warm light"
  - target: "a photorealistic orange cat sitting under a glass coffee table in a living room, warm light"
  - wrong_axis: "a photorealistic gray cat sitting on a red sofa in a living room, warm light"

### count_one_two_birds  --  one bird -> two birds  (discovery tier: **open**)

- **`count_one_two_birds__pa`**
  - source: "one photorealistic brown squirrel sitting on a tree branch in a forest at dawn"
  - target: "two photorealistic brown squirrels sitting side by side on a tree branch in a forest at dawn"
  - wrong_axis: "one photorealistic gray squirrel sitting on a tree branch in a forest at dawn"
- **`count_one_two_birds__pb`**
  - source: "one photorealistic white duck floating on a calm pond at noon"
  - target: "two photorealistic white ducks floating side by side on a calm pond at noon"
  - wrong_axis: "one photorealistic brown duck floating on a calm pond at noon"

### scene_snow_beach  --  snow -> beach  (discovery tier: **carrier**)

- **`scene_snow_beach__pa`**
  - source: "a photorealistic golden retriever sitting in fresh snow at dawn, soft blue light"
  - target: "a photorealistic golden retriever sitting on a sunny sandy beach at noon, bright blue sky"
  - wrong_axis: "a photorealistic black dog sitting in fresh snow at dawn, soft blue light"
- **`scene_snow_beach__pb`**
  - source: "a photorealistic brown rabbit sitting in fresh snow at dawn, soft blue light"
  - target: "a photorealistic brown rabbit sitting on a sunny sandy beach at noon, bright blue sky"
  - wrong_axis: "a photorealistic white rabbit sitting in fresh snow at dawn, soft blue light"

### scene_snow_forest  --  snow -> autumn forest  (discovery tier: **carrier**)

- **`scene_snow_forest__pa`**
  - source: "a photorealistic golden retriever sitting in fresh snow at dawn, soft blue light"
  - target: "a photorealistic golden retriever sitting in a green autumn forest at noon, golden sunlight"
  - wrong_axis: "a photorealistic golden retriever sitting in fresh snow during a heavy snowstorm, gray light"
- **`scene_snow_forest__pb`**
  - source: "a photorealistic brown rabbit sitting in fresh snow at dawn, soft blue light"
  - target: "a photorealistic brown rabbit sitting in a green autumn forest at noon, golden sunlight"
  - wrong_axis: "a photorealistic brown rabbit sitting in fresh snow during a heavy snowstorm, gray light"

### scene_snow_greenhouse  --  snow -> greenhouse  (discovery tier: **carrier**)

- **`scene_snow_greenhouse__pa`**
  - source: "a photorealistic golden retriever sitting in fresh snow at dawn, soft blue light"
  - target: "a photorealistic golden retriever sitting inside a glass greenhouse among tropical plants, warm daylight"
  - wrong_axis: "a photorealistic black dog sitting in fresh snow at dawn, soft blue light"
- **`scene_snow_greenhouse__pb`**
  - source: "a photorealistic gray cat sitting in fresh snow at dawn, soft blue light"
  - target: "a photorealistic gray cat sitting inside a glass greenhouse among tropical plants, warm daylight"
  - wrong_axis: "a photorealistic orange cat sitting in fresh snow at dawn, soft blue light"

### lighting_dawn_sunset  --  dawn -> sunset  (discovery tier: **strict**)

- **`lighting_dawn_sunset__pa`**
  - source: "a photorealistic red brick lighthouse on a rocky coast at dawn, soft blue light"
  - target: "a photorealistic red brick lighthouse on a rocky coast at sunset, warm orange light"
  - wrong_axis: "a photorealistic red brick lighthouse on a rocky coast at midnight, silver moonlight"
- **`lighting_dawn_sunset__pb`**
  - source: "a photorealistic wooden park bench under an oak tree at dawn, soft blue light"
  - target: "a photorealistic wooden park bench under an oak tree at sunset, warm orange light"
  - wrong_axis: "a photorealistic wooden park bench under an oak tree at midnight, silver moonlight"

### weather_clear_snowstorm  --  clear sky -> snowstorm  (discovery tier: **strict**)

- **`weather_clear_snowstorm__pa`**
  - source: "a photorealistic red fox standing in a pine forest under a clear sky at dawn, soft blue light"
  - target: "a photorealistic red fox standing in a pine forest during a heavy snowstorm at dawn, diffuse gray light"
  - wrong_axis: "a photorealistic gray fox standing in a pine forest under a clear sky at dawn, soft blue light"
- **`weather_clear_snowstorm__pb`**
  - source: "a photorealistic brown horse in a mountain valley under a clear sky at dawn, soft blue light"
  - target: "a photorealistic brown horse in a mountain valley during a heavy snowstorm at dawn, diffuse gray light"
  - wrong_axis: "a photorealistic white horse in a mountain valley under a clear sky at dawn, soft blue light"

### style_photo_oil  --  photo -> oil painting  (discovery tier: **carrier**)

- **`style_photo_oil__pa`**
  - source: "a photorealistic brown horse standing in a meadow at noon, bright light"
  - target: "an oil painting of a brown horse standing in a meadow at noon, bright light"
  - wrong_axis: "a photorealistic white horse standing in a meadow at noon, bright light"
- **`style_photo_oil__pb`**
  - source: "a photorealistic red rose in a glass vase on a table, soft light"
  - target: "an oil painting of a red rose in a glass vase on a table, soft light"
  - wrong_axis: "a photorealistic yellow rose in a glass vase on a table, soft light"

### material_robot_metal_wood  --  metal robot -> wooden robot  (discovery tier: **carrier**)

- **`material_robot_metal_wood__pa`**
  - source: "a photorealistic silver metal robot standing in a city plaza at noon, bright light"
  - target: "a photorealistic carved wooden robot standing in a city plaza at noon, bright light"
  - wrong_axis: "a photorealistic silver metal robot standing in a forest clearing at dusk, dim light"
- **`material_robot_metal_wood__pb`**
  - source: "a photorealistic polished metal teapot on a kitchen counter, warm light"
  - target: "a photorealistic carved wooden teapot on a kitchen counter, warm light"
  - wrong_axis: "a photorealistic polished metal teapot on a mossy rock outdoors, cool light"

## 4. Decision rule (fixed before running)

A **cell** is one (prompt-variant, seed) pair. Each original axis has 2 variants x 3 seeds = **6 cells**. Each cell is scored by the nine frozen gates on that single (variant, seed) run, yielding a per-cell tier (strict / carrier / open) exactly as above.

**Per-axis replication (literal primary rule, as specified in the task).** An original axis *replicates on held-out prompts* if it passes **the same gate set it cleared on the discovery panel** on **>= half (>= 3 of 6) of its cells**:
- a discovery-**strict** axis replicates iff >= 3/6 cells reach strict (all nine gates);
- a discovery-**carrier** axis replicates iff >= 3/6 cells reach carrier-or-better (the seven route gates);
- a discovery-**open** axis is reported for completeness (its discovery gate set already had a route gate open); it is not part of the aggregate verdict.

**Aggregate verdict (as specified).** The paper's claim that *the certified route survives prompt hold-out* holds iff **>= 4 of the 6 discovery-certified axes replicate** under the rule above (i.e. reach strict on >= 3/6 of their held-out cells).

**Secondary, pre-declared route-level analysis (reported for all axes).** Because the paper's own held-out-*seed* confirmation found the strict pixel tier to be seed-sensitive while the transport route was robust, we also pre-declare a route-level readout that isolates the central mechanistic claim from strict pixel reconstruction: a cell *route-replicates* iff it reaches carrier-or-better (the seven route gates); an axis route-replicates iff >= 3/6 of its cells route-replicate. We report, for the six certified axes and for all twenty, how many route-replicate. This secondary readout is declared here in advance and reported alongside the primary verdict; it does not replace it.

**Comparison table.** Results will report, per original axis: discovery tier (from the published panel, seeds 4242/9001) vs held-out outcome (per-cell tiers across the 6 cells, the aggregated per-axis tier from the worker, replicate yes/no under both the literal and route-level rules).

## 5. Analysis and verification plan

- The panel is scored by the same production certification worker used for the certified panel (one model lease per group, real model, checkpoint replay, native conditioner, no training).
- Results are then re-derived by the standalone independent auditor (standard library + numpy + Pillow only; no import from the experiment pipeline), pointed at this configuration and this results tree. It re-implements all nine gate equations, the promotion rule, and the ledger from scratch against the retained raw branch rows and recomputes image-side scalars from the retained lossless images. A 'consistent' auditor verdict means every tier and gate re-derives from raw artifacts under the frozen thresholds and every recomputable declared hash matches.
- Reported artifacts: the consolidated per-axis ledger (JSON + Markdown), the independent-auditor verdict JSON, the exact scheduled-job identifiers, and a small set of representative montages (one passing and one failing axis).

## 6. What this test cannot establish

- It does not widen the seed distribution beyond the three seeds used here, nor claim population statistics.
- The per-branch replay-exactness gate remains metadata-attested (checkpoint tensors are not retained in the results tree), exactly as in the paper; the auditor verifies everything derivable from retained artifacts but cannot re-execute a replay.
- A negative result bounds generalisation of the *strict pixel* certificate to new prompts; the route-level readout is the test of the transport mechanism itself.

## 7. Amendment log

### Amendment 1 -- 2026-09-22 (per-cell operationalization of the reproducibility gate)

Reason: gate 1 (reproducibility) is defined in the frozen scoring code as "at least two independent seeds present" -- a cross-seed property of an axis, not of a single (variant, seed) cell; evaluated on one cell it is degenerate (always fails), which section 4 did not account for when it wrote "scored by the nine frozen gates". Clarification (no threshold, contrast, seed, route, or hypothesis change):

- Each **cell** is scored by the **other eight** frozen gates on its single run.
- **Reproducibility** is satisfied at the **axis-variant** level: each of the two prompt variants is run on the three seeds (>= 2), so reproducibility holds for the variant.
- A cell **strict-passes** when all eight per-cell gates pass (the two strict pixel gates -- full-dose sufficiency and dose-response -- plus the six causal-route gates: necessity, wrong-axis specificity, sham specificity, edge mediation, consumer continuation, exact-replay).
- A cell **route-passes** when the six causal-route gates pass.
- The per-axis rule (replicate iff the relevant pass-type holds on >= 3 of 6 cells) and the aggregate verdict (>= 4 of 6 certified axes replicate) are unchanged.

This was identified from the frozen scoring code before any result was analyzed. It sharpens how gate 1 maps onto a cell; it does not weaken or move any numeric threshold. The complementary axis-variant tier (each variant across its three seeds, with reproducibility in force) is also reported.

### Amendment 2 -- 2026-09-22 (execution environment; host-drift fix)

Reason: the first submission of all ten groups failed deterministically at process start (return code 2, ~1.4 s) with a "project directory does not exist" error for the packaging environment that formerly supplied the torch/CUDA base on the GPU host for this worker family. That environment is no longer present on the host (verified by direct inspection); it is absent from the retained artifacts and cannot be faithfully restored.

Fix: the diffusion-stack version pins are **unchanged** (diffusers 0.39.0, transformers 5.14.1, accelerate 1.14.0 -- identical to the certified panel's reproducibility anchors). Only the mechanism that supplies the torch base was changed, from the missing project to the host's current base environment (torch 2.13.0+cu130, CUDA available), with those same pins overlaid. The launcher command was edited accordingly. This is an infrastructure fix; it changes no route site, threshold, contrast, or seed.

Reproducibility caveat (reported as a limitation in RESULTS.md): the certified panel's exact torch build is not recorded in the retained artifacts, so this run's torch may differ from the panel's. Any environment-induced difference is expected to fall on the strict pixel-reconstruction tier -- which the paper already documents as seed-sensitive -- not on the causal-route gates. Because of this, the route-level readout (Amendment-1 route-pass) is the environment-robust comparison; strict-tier comparisons against the published (different-environment) discovery panel are interpreted with this caveat.

### Amendment 3 -- 2026-09-22 (scope reduced to the six certified axes)

Reason: compute reduction. Execution is limited to the job groups covering the six discovery-certified axes -- identity (cat->fox), fur length, lighting (dawn->sunset), orientation (left->right), the beside->behind relation, and weather (clear->snowstorm) -- plus the groups that had already completed. The remaining held-out groups (the carrier and open axes not already run) and the matched-environment discovery baseline are cancelled and not executed.

The decision rule is **unchanged**: the paper's claim that the certified route survives prompt hold-out holds iff **>= 4 of the 6 certified axes replicate on held-out prompts** (per the rule in section 4). Held-out replication of the carrier / route-certified axes is **left open** (not evaluated under this reduced scope). Data from the groups that had already completed -- which incidentally include several carrier and open axes -- are retained and reported for context, not as a scoped claim. The matched-environment discovery baseline (Amendment-2 control) is deferred; the primary comparison reverts to the published discovery tiers with the Amendment-2 environment caveat.

### Amendment 4 -- 2026-09-22 (execution-only)

RAM reservation right-sized (30000 -> 26000 MB) to clear scheduler admission for the three pending certified-axis groups, which were resubmitted with new job identifiers at moderate priority; the request payload, configuration hash, gates, contrasts, and seeds are unchanged.

(Any further change after the first submitted job is recorded here with a date and reason; the sections above are not edited.)
