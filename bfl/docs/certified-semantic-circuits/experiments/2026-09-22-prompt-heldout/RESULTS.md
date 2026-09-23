---
title: "Results: prompt-held-out replication of the certified semantic route (interim, certified-axis scope)"
type: results
status: interim
date: 2026-09-22
parent: PREREGISTRATION.md
---

# Results — prompt-held-out replication of the certified FLUX.2 Klein 4B semantic route

**Status: interim.** Executed under the frozen preregistration (`PREREGISTRATION.md`) and its Amendments 1–3. Amendment 3 reduced execution to the job groups covering the six discovery-certified axes for compute reasons. Of those, **two certified axes have completed** (fur length, identity cat→fox) and **four are pending** on the shared GPU at low priority (orientation, beside→behind relation, lighting, weather); the four pending groups were queued and not yet admitted. The completion path is in section 6.

- Held-out configuration SHA-256: `846d1e1ee205f2406dbcb87f2336dfb260e6e0c2c69137224a52b2c0042b2a3d` (byte-exact file retained in the private tree; contrasts and thresholds are enumerated in the preregistration).
- Frozen (discovery) configuration SHA-256: `9701c9ed08bb668cc73a4c1b20b3dfda736f50ae3eba87a3a1bc2cec55265135`.
- Seeds: 4242, 9001, 20260922. Route, thresholds, mediation step, dose curve, model, revision, resolution, steps, guidance: byte-identical to the frozen config.

## Aggregate verdict

**Incomplete — cannot yet be concluded.** The preregistered aggregate rule (the certified route survives prompt hold-out iff ≥ 4 of 6 certified axes replicate on held-out prompts) requires all six certified axes; only **two** have run. On the evidence available:

- **Both completed certified axes route-replicate on held-out prompts.** Fur and identity each pass the six causal-route gates on **5 of 6** held-out (variant×seed) cells. This is the environment-robust readout (Amendment 2).
- **Strict pixel tier: weak, as anticipated.** Identity strict-replicates (all 8 per-cell gates on **3/6** cells); fur does not (**1/6**). No completed variant reaches the strict tier across all three seeds (0/16 across-seed certified) — consistent with the paper's finding that strict pixel reconstruction is seed-sensitive, compounded here by the environment change (Amendment 2).

The route-level signal is strong and consistent; the strict-pixel signal is weak. A final ≥4/6 verdict is deferred until orientation, beside→behind, lighting, and weather run.

## Certified axes: discovery tier vs held-out outcome

`route/6` = held-out cells (2 variants × 3 seeds) passing the six causal-route gates; `strict/6` = cells also passing the two strict pixel gates. Discovery tier is from the published panel (seeds 4242/9001, different environment — see caveat).

| certified axis | discovery contrast | disc. tier | route/6 | strict/6 | route-replicate | strict(literal)-replicate | status |
|---|---|---|--:|--:|:--:|:--:|---|
| `fur_short_long` | short → long fur | strict | 5/6 | 1/6 | **yes** | no | complete |
| `identity_cat_fox` | black cat → red fox | strict | 5/6 | 3/6 | **yes** | **yes** | complete |
| `orientation_left_right` | facing left → right | strict | — | — | — | — | pending (queued, low priority) |
| `relation_beside_behind_ball` | beside → behind ball | strict | — | — | — | — | pending (queued, low priority) |
| `lighting_dawn_sunset` | dawn → sunset | strict | — | — | — | — | pending (queued, low priority) |
| `weather_clear_snowstorm` | clear → snowstorm | strict | — | — | — | — | pending (queued, low priority) |

## Supporting context: the completed groups (8 original axes, 16 held-out contrasts)

The already-completed groups incidentally include several route-certified and open axes (retained for context, not as a scoped claim). Across all 8 completed original axes, **7 route-replicate** (≥3/6 route-pass cells); only `pose_sitting_lying` (a discovery-*open* axis) does not (1/6). Route-pass counts: eyes 6/6, marking 6/6, action 6/6, fur 5/6, identity 5/6, size 5/6, geometry 4/6, pose_sitting_lying 1/6. Across-seed variant tiers: 9 of 16 variants reach route-level (route-certified) across all three seeds; 7 are route-certified-candidate; 0 reach strict. The transport route demonstrably carries new subject/scene prompts; strict pixel reconstruction does not survive the prompt (and environment) change.

## Independent auditor (completed panel)

The standalone auditor (standard library + NumPy + Pillow only; no import from the experiment pipeline), pointed at this configuration and results tree, re-derived every gate from the raw branch rows and recomputed image-side scalars from the retained images. On the 16 completed contrasts:

- **Zero** tier mismatches, **zero** ledger mismatches, **zero** pixel/metric mismatches (max image-scalar discrepancy 1.5×10⁻⁵, float32 reduction noise), **zero** hash mismatches (per-group config hashes reconcile).
- Its overall verdict prints `mismatches_found`, driven by two non-substantive items, both verified: (a) the 24 axes not yet run are flagged as "no retained report" (expected under the reduced/partial scope); (b) 16 `mediation` entries flag an `all_rescue_fractions` **list-ordering** difference — the worker and auditor emit the same nine rescue values (3 edges × 3 seeds) in a different order. The multiset and the minimum are identical, so the mediation gate decision (min ≥ 0.50) and every tier are unchanged. This is a cosmetic array-ordering artifact, not a scientific inconsistency (a canonical sort of that diagnostic array would remove it).

## Environment caveat (Amendment 2)

The uv packaging environment that formerly supplied the torch/CUDA base for this worker family is no longer present on the GPU host, and the certified panel's exact torch build is not recorded in the retained artifacts. This run used the host's current base environment (torch 2.13.0+cu130, CUDA) with the identical diffusion pins (diffusers 0.39.0, transformers 5.14.1, accelerate 1.14.0). Any environment-induced difference is expected to fall on the strict pixel tier, not the causal-route gates; the route-level readout is therefore the environment-robust comparison. The matched-environment discovery baseline (Amendment 2) was cancelled under the Amendment-3 scope reduction and is deferred.

## Completing the remaining four certified axes

Three queued groups cover them (all at low priority — they run when the GPU is idle, or on demand):

- group 4 `job-a462fa7715df` — orientation (+ ears)
- group 5 `job-301446e88c0b` — beside→behind (+ on/under)
- group 8 `job-60ffbd20debc` — lighting + weather

To run them promptly, raise their priority or re-launch via the private on-demand script (kept outside this public directory). Then collect each group and re-run the ledger + auditor + decision analysis (commands recorded with the script); the aggregate ≥4/6 verdict follows directly.

## Job identifiers

Completed (retained): group 0 `job-3965f6d2c20b` (size, fur), group 1 `job-3f3b24ab8459` (eyes, marking), group 2 `job-6f32cbefcaef` (identity, geometry), group 3 `job-2baf28fddb02` (pose_sitting_lying, action). Pending: groups 4/5/8 above. Cancelled under scope reduction: held-out groups 6/7/9 and the five matched-environment baseline groups.

## Deviations from the preregistration

- Amendment 1: per-cell operationalization of the reproducibility gate.
- Amendment 2: execution-environment / host-drift fix (torch base), diffusion pins unchanged.
- Amendment 3: scope reduced to the six certified axes for compute; decision rule unchanged; route-certified held-out replication and the matched-environment baseline left open.

## Artifacts

- Consolidated ledger (16 completed contrasts): `artifacts/circuit-panel-ledger.json`, `artifacts/circuit-panel-ledger.md`
- Independent auditor verdict: `artifacts/independent-recheck.json`
- Per-cell decision record: `artifacts/prompt-heldout-decision.json`
- Representative montages: `artifacts/*.png`
