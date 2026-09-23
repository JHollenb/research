---
title: "Results: prompt-held-out replication of the certified semantic route"
type: results
status: complete (certified-axis scope)
date: 2026-09-22
parent: PREREGISTRATION.md
---

# Results — prompt-held-out replication of the certified FLUX.2 Klein 4B semantic route

Executed under the frozen preregistration (`PREREGISTRATION.md`) and its Amendments 1–4. Amendment 3 reduced execution to the six discovery-certified axes for compute reasons; **all six have now completed** on held-out prompts. Two new subject/scene rewordings per axis, seeds 4242 / 9001 / 20260922, on the pinned model revision and recipe, with route, thresholds, mediation step, and dose curve byte-identical to the certified panel.

- Held-out configuration SHA-256: `846d1e1ee205f2406dbcb87f2336dfb260e6e0c2c69137224a52b2c0042b2a3d` (byte-exact file retained in the private tree; contrasts and thresholds are enumerated in the preregistration).
- Frozen (discovery) configuration SHA-256: `9701c9ed08bb668cc73a4c1b20b3dfda736f50ae3eba87a3a1bc2cec55265135`.

## Aggregate verdict — the certified route SURVIVES prompt hold-out

The preregistered aggregate rule (the certified route survives prompt hold-out iff ≥ 4 of 6 certified axes replicate on held-out prompts) is **met**, and the route-level readout is stronger still:

- **Route-level (the environment-robust, central mechanistic readout): 6 of 6** certified axes route-replicate — every certified axis passes the six causal-route gates on ≥ 3 of its 6 held-out (variant×seed) cells.
- **Literal strict rule (all 8 per-cell gates, per the preregistration): 4 of 6** certified axes replicate (identity, orientation, beside→behind, lighting). This clears the ≥ 4/6 bar.

The transport route carries the same twenty semantic transformations expressed on new subjects and scenes. Strict pixel reconstruction is the weaker, more seed/prompt/environment-sensitive property (2 of 6 certified axes — fur, weather — route-replicate but miss the strict tier), exactly the route-vs-pixel distinction the paper draws.

## Certified axes: discovery tier vs held-out outcome

`route/6` = held-out cells (2 variants × 3 seeds) passing the six causal-route gates; `strict/6` = cells also passing the two strict pixel gates (full-dose sufficiency, dose endpoints). Discovery tier is from the published panel (seeds 4242/9001, different environment — see caveat). `variant tiers` = each reworded variant's tier across its three seeds (`partial` = route gates pass on some but not all three seeds).

| certified axis | held-out contrast (variant a / b subjects) | disc. tier | route/6 | strict/6 | route-replicate | strict-replicate | variant tiers (pa, pb) |
|---|---|---|--:|--:|:--:|:--:|---|
| `fur_short_long` | brown dog on porch / gray rabbit on lawn | strict | 5/6 | 1/6 | **yes** | no | partial, route-certified |
| `identity_cat_fox` | tabby→beagle / squirrel→rabbit | strict | 5/6 | 3/6 | **yes** | **yes** | partial, route-certified |
| `orientation_left_right` | owl on branch / retriever on beach | strict | 5/6 | 3/6 | **yes** | **yes** | route-certified, partial |
| `relation_beside_behind_ball` | puppy+bucket / kitten+box | strict | 5/6 | 5/6 | **yes** | **yes** | partial, **strict** |
| `lighting_dawn_sunset` | lighthouse / park bench | strict | 6/6 | 4/6 | **yes** | **yes** | **strict**, route-certified |
| `weather_clear_snowstorm` | red fox in pine forest / horse in valley | strict | 3/6 | 1/6 | **yes** | no | partial, route-certified |

All six route-replicate; four strict-replicate. Two variants reach the full strict tier across all three held-out seeds (beside→behind pb, lighting pa) — a strict certificate on a brand-new prompt.

## Supporting context: the completed groups (14 original axes, 28 held-out contrasts)

The completed groups also cover eight route-certified/open axes (retained for context, not as a scoped claim). Across all 14 completed original axes, **13 route-replicate** (≥ 3/6 route-pass cells); only `pose_sitting_lying` (a discovery-*open* axis) does not (1/6). The consolidated ledger over the 28 contrasts: 2 across-seed strict, 14 route-certified (route gates pass on the weakest of three seeds), 12 partial (route gates pass on some but not all three seeds).

## Independent auditor

The standalone auditor (standard library + NumPy + Pillow only; no import from the experiment pipeline), pointed at this configuration and results tree, re-derived every gate from the raw branch rows and recomputed image-side scalars from the retained images. On the 28 completed contrasts:

- **Zero** tier mismatches, **zero** ledger mismatches, **zero** pixel/metric mismatches (max image-scalar discrepancy 1.5×10⁻⁵, float32 reduction noise), **zero** hash mismatches (per-group config hashes reconcile).
- Its overall verdict prints `mismatches_found`, driven only by two verified non-substantive items: the 12 out-of-scope axes flagged as "no retained report" (expected under the reduced scope), and 28 `mediation` entries flagging an `all_rescue_fractions` **list-ordering** difference — the worker and auditor emit the same nine rescue values (3 edges × 3 seeds) in a different order. The multiset and the minimum are identical, so the mediation gate decision (min ≥ 0.50) and every tier are unchanged. A canonical sort of that diagnostic array would remove the flag; it is not a scientific inconsistency.

## Environment caveat (Amendment 2)

The uv packaging environment that formerly supplied the torch/CUDA base for this worker family is no longer present on the GPU host, and the certified panel's exact torch build is not recorded in the retained artifacts. This run used the host's current base environment (torch 2.13.0+cu130, CUDA) with the identical diffusion pins (diffusers 0.39.0, transformers 5.14.1, accelerate 1.14.0). Any environment-induced difference is expected to fall on the strict pixel tier, not the causal-route gates — which is why the 6/6 route-level replication is the environment-robust result, while strict-tier numbers carry this caveat. The matched-environment discovery baseline (Amendment 2) was cancelled under the Amendment-3 scope reduction and remains a clean-comparison follow-up.

## Job identifiers

Held-out groups (seeds 4242/9001/20260922), all succeeded: g0 `job-3965f6d2c20b` (size, fur), g1 `job-3f3b24ab8459` (eyes, marking), g2 `job-6f32cbefcaef` (identity, geometry), g3 `job-2baf28fddb02` (sitting→lying, action), g4 `job-b63a7543a301` (orientation, ears), g5 `job-fee7b2bb0d62` (beside→behind, on→under), g8 `job-a41550277906` (lighting, weather). Cancelled under scope reduction: held-out groups 6/7/9 and the five matched-environment baseline groups. (g4/g5/g8 were resubmitted once with a right-sized RAM reservation — Amendment 4 — replacing earlier IDs.)

## Deviations from the preregistration

- Amendment 1: per-cell operationalization of the cross-seed reproducibility gate.
- Amendment 2: execution-environment / host-drift fix (torch base), diffusion pins unchanged.
- Amendment 3: scope reduced to the six certified axes for compute; decision rule unchanged; route-certified held-out replication and the matched-environment baseline left open.
- Amendment 4: RAM reservation right-sized (execution-only); job IDs replaced; config hash unchanged.

## Artifacts

- Consolidated ledger (28 completed contrasts): `artifacts/circuit-panel-ledger.json`, `artifacts/circuit-panel-ledger.md`
- Independent auditor verdict: `artifacts/independent-recheck.json`
- Per-cell decision record (all six certified axes + context): `artifacts/prompt-heldout-decision.json`
- Representative montages: `artifacts/*.png` (a passing certified axis and a failing open axis)
