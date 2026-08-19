---
title: "Semantic Object Registers: Family Replication, Window Locality, and a Wrong-Object Diagnosis"
type: experiment-report
status: convergent-portability-trend
priority: supporting-generalization-check
model_scope: "FLUX.2 Klein family (base-4B undistilled, 4B distilled, 9B) primary; FLUX.1 Schnell cross-family extension"
model_ids:
  - "black-forest-labs/FLUX.2-klein-4B"
  - "black-forest-labs/FLUX.2-klein-base-4B"
  - "black-forest-labs/FLUX.2-klein-9B"
  - "black-forest-labs/FLUX.1-schnell"
revisions:
  flux2_klein_4b: "e7b7dc27f91deacad38e78976d1f2b499d76a294"
  flux2_klein_base_4b: "a3b4f4849157f664bdbc776fd7453c2783562f4d"
  flux2_klein_9b: "92196c8e11f7b6cf2b7493e037d8c5345c559216"
  flux1_schnell: "741f7c3ce8b383c54771c7003378a50191e9efe9"
checkpoint_role: "klein-4B distilled anchor + cross-conditioner substrate; base-4B and klein-9B replication arms; schnell cross-family extension"
backend: "CUDA on Beast (16 GB), bf16, single mrun lease per arm, no retries"
consumer: "native FLUX.2/FLUX.1 denoiser, scheduler, VAE, and RGB image output"
tags: [bfl, flux, flux2, flux1, object-registers, semantic-object, semantic-circuit, cross-family, conditioner, portability, causal-route]
---

# Semantic Object Registers: Family Replication, Window Locality, and a Wrong-Object Diagnosis

> [!summary]
> The object-register interface found on distilled `FLUX.2-klein-4B` (two-row subject patch → white fox, cross-scene displacement port → blue mug, inert norm-matched shams, no-op ×2 scale) replicates on the undistilled `klein-base-4B` at its native 50-step real-CFG operating point and on `klein-9B` under sequential offload. On `FLUX.1-schnell`'s bidirectional T5 conditioner the same battery degrades from row-sharp to NP-window-local addressing: single-row edits are sham-level, but a ±3 noun-phrase window patch renders a clean white fox. A separate diagnosis maps the cross-conditioner's signature wolf-not-fox failure onto the same register structure: the wrong object is row-portable both ways, and a linear carrier-space readout cannot see what the native consumer plainly decodes. A third result is a measured negative — prompt-disjoint TECM scheduler closure does not transfer; its held-out corgi lands at the same error as a closure run that saw the prompt.

## Research question

The 2026-08-18 [object-register results](semantic-circuit-object-interface.md) (token-row addressing, row-local edit battery, base-anchored displacement algebra, value-level debugging) were all bound to one checkpoint: distilled `FLUX.2-klein-4B` at 256², 4 steps, guidance 1. Are those properties of that one checkpoint, or of the FLUX text-to-image program family?

The campaign runs the same preregistered battery — noop/determinism gates, zero-rows role-backfill probes, route-band certification, donor row addressing with norm-matched shams, in-scene displacement algebra, wrong-address payload transfer, and a cross-scene displacement port — against three further checkpoints spanning two axes: distillation (undistilled base-4B vs. distilled 4B/9B) and conditioner family (Qwen-family text encoders vs. FLUX.1's T5 + pooled-CLIP). A fourth and fifth arm ask narrower follow-on questions: does scheduler closure for the Smol→Qwen cross-conditioner generalize to held-out prompts, and where does the cross-conditioner's known wrong-object failure actually live in the register structure.

## Cohort and execution contract

| arm | model | checkpoint | topology | steps / guidance | memory strategy | seeds | job |
|---|---|---|---|---|---|---|---|
| A | FLUX.2-klein-base-4B (undistilled) | `a3b4f484…` | 5 joint + 20 single | 50 / 4.0 (real CFG) | `enable_model_cpu_offload` | 7217, 31337 | `job-17788d5a1b0d` |
| B | FLUX.2-klein-9B (distilled) | `92196c8e…` | 8 joint + 24 single | 4 / 1.0 | `enable_sequential_cpu_offload` | 7217 | `job-638d05dcbff2` |
| C | FLUX.1-schnell (cross-family) | `741f7c3c…` | 19 joint + 38 single | 4 / 0.0 | sequential offload + fp8-e4m3 layerwise | 7217, 31337 | `job-a676189574d1`, `job-27fef20e82a0` |
| D | TECM v4 closure (klein-4B recipient) | `e7b7dc27…` | — | — | in-process | n/a | `job-0a318a2d8c9d` |
| E | Cross-conditioner wrong-object diagnosis (klein-4B) | `e7b7dc27…` | — | 4 / — | model offload | 7217, 31337 | `job-e1ba0cbed889` |

Every arm ran single-lease on Beast via mrun with strict preflight and no retries. Arm A's identity gates are the strongest in the campaign: `noop`-with-armed-hooks RGB MAD `0.0`, determinism rerun MAD `0.0`, through a **100-transformer-call CFG native render** (50 steps × cond/uncond). The phase trajectory replay path refuses CFG, so Arm A's branches run as native `__call__` renders with forward hooks rather than checkpoint suffix replay — every branch under an exact scalar contract, with cond/uncond split by deterministic call order and verified by a pointer-disjointness check. Arms B, C, and E use checkpoint capture/suffix-replay instead, and all report exact `0.0` noop/determinism gates under their own contract (sequential-offload seq for B, cut-0 trajectory checkpoints for C, native-call branches for E).

Receipt-level resource facts (from the copied run receipts): Arm A `elapsed_s = 410.31`, `peak_rss_mb = 24624.9`, `peak_vram_mb = 8334.0`; Arm B `elapsed_s = 161.46`, `peak_rss_mb = 20261.0`, `peak_vram_mb = 2708.0` (the 16 GB Qwen3-8B encoder is freed in-worker after the encode phase — a 50 GB reservation attempt was permanently unschedulable against Beast's floating 12–30 GB baseline, diagnosed via `mrun why` and fixed by resizing to 42 GB); Arm C `elapsed_s = 323.0` / `350.62` across the two jobs, `peak_vram_mb` under 700 MB (fp8 layerwise + sequential offload keeps VRAM low at the cost of RSS near 36 GB); Arm E `elapsed_s = 349.07`, `peak_rss_mb = 22316.8`, `peak_vram_mb = 8314.0`, with `mapper_steps = 900` for the in-job TECM v3 warm start.

## FLUX.2 family: the registers replicate

| property | klein-4B distilled (anchor, 08-18) | base-4B undistilled, 50-step real CFG | klein-9B, 8+24 blocks, Qwen3-8B cond |
|---|---|---|---|
| exact noop / determinism gates | 0.0 (checkpoint replay) | 0.0 / 0.0 (native 100-call CFG) | 0.0 / 0.0 (seq offload) |
| subject row-patch → white fox | yes (0.92–0.94) | yes, both seeds (0.888 @7217) | yes (0.743, sham 0.043) |
| attr row-patch (ball → green) | yes | yes (0.784/0.836) | yes (0.713, fox-ROI 0.074) |
| norm-matched sham rows | inert | inert (≤0.13) | inert (≤0.05) |
| zero subject rows | generic-animal backfill | generic tan animal, both seeds | whitened/genericized fox |
| cross-scene port d = row(blue) − row(red) → mug | blue mug | **blue mug** (pane; ROI scalar diluted) | **blue mug** (0.471 vs sham 0.076) |
| scale ×2 color row | no-op | no-op (0.75/0.94 MAD) | no-op (0.55) |
| displacement at fox's own color row | fox stays red (species prior) | fox stays red, both seeds | fox stays red |

Three checkpoints, three operating points (4-step distilled / 50-step CFG undistilled / 4-step distilled at 4096 width with a different conditioner), one register grammar. The sham controls are what make this a claim rather than a coincidence: on klein-9B the subject-row donor patch beats its norm-matched sham by more than 15×.

On base-4B, the 31337-seed fox row-patch scores `0.071` "progress" by the ROI scalar, but the pane (`zoom-fox-base4b-seed31337.png`) shows a clean white fox — a pose mismatch against the donor render understates the scalar, not a failed edit. The base-4B cross-scene mug port similarly averages to "gray" over an ROI box that includes dark background (`zoom-mug-port-base4b.png`), while the pane is unambiguously blue. Panes are primary evidence in this campaign; ROI scalars are a secondary, sometimes-misleading instrument.

**Route concentration is an operating-point property, not a family constant.** On distilled klein-4B the certified route (`joint.2 → joint.3 → joint.4 → single.0`) is load-bearing. On base-4B at 50 steps, a full-512-row donor patch at *any* preregistered band — `joint.0-1` alone, `single.0` alone — reaches 0.92–0.98 progress toward the donor render (the chosen route stayed the default band only because the preregistered 0.8-of-best rule kept it there). On klein-9B, every joint band reaches roughly 0.99 progress while `single.0` alone still reaches 0.70; the default `joint.4-7 + single.0` band was kept. More steps and more blocks buy route redundancy; the row addresses themselves stay sharp across all three checkpoints.

Proof: `zoom-fox-base4b-seed31337.png`, `zoom-mug-port-base4b.png`, `zoom-fox-klein9b-seed7217.png`, `zoom-mug-port-klein9b.png` in the [local bundle](../artifacts/semantic-object-registers/), reproducible with zoom crops from `saturn/results/object-multimodel-flux2/job-17788d5a1b0d/` (base-4B) and `saturn/results/object-multimodel-flux2/job-638d05dcbff2/` (klein-9B) via `analyze_multimodel.py`.

## FLUX.1-schnell: same registers, different addressing grain

FLUX.1-schnell runs a T5 + pooled-CLIP dual conditioner rather than the Qwen-family causal decoder that backs every FLUX.2 arm above. Single-row edits collapse to sham level, but a locality-probe ladder over donor-patch granularity is clean:

| donor patch granularity (white-fox → foxball, route: all-joint + s0) | image progress (7217 / 31337) | pane |
|---|---|---|
| single subject row ("fox") | −0.05 / 0.03 (≈ sham) | fox stays red |
| NP window ±3 (7 rows) | 0.56 / 0.63 | **clean white fox, ball untouched** |
| all active rows (~20) | 0.66 / 0.61 | white fox |
| padding rows only (492 rows) | 0.10 / 0.03 | fox stays red |
| full 512 rows (ceiling) | 0.71 / 0.78 | white animal, composition shifts |
| pooled-CLIP swap only | −0.09 / 0.04 | fox stays red |

Row-sharp semantics also fail downstream: the single-row displacement port into `catmug` reaches 0.27 against a 0.15 sham (the mug stays red in the pane), scale ×2 on the color row is **not** a no-op (MAD 4.9, vs. base-4B's 0.75), and zeroing the single row does not delete the object.

**Working inference (architectural):** the Qwen-family conditioners used across the FLUX.2 arms are causal decoders — token rows carry locally-addressable object content and padding rows are load-bearing. T5 is a bidirectional encoder; its attention mask makes padding inert and smears lexical content across the NP window instead. Object addressing therefore crosses the family at *window* granularity, while single-row addressing and row-value algebra look specific to the FLUX.2/Qwen-conditioner combination. The full-carrier route ceiling is also lower on FLUX.1 (0.71 vs. 0.98 on base-4B): part of the change is carried outside the joint text stream — the 38 single blocks and the pooled path are candidates, and this remains unattributed.

Proof: `locality-strip-flux1.png` in the [local bundle](../artifacts/semantic-object-registers/), from `saturn/results/object-multimodel-flux1/job-27fef20e82a0/`. The base battery (`job-a676189574d1`) supplies the row/sham/scale/zero controls; the locality probes (`job-27fef20e82a0`) supply the granularity ladder.

## Cross-conditioner: which object did the foreign conditioner actually write

The cross-conditioner's signature failure is a clean scene with the wrong object: ask the Smol TECM v3 compiler for a red fox in snow, get a gray wolf in a grass field. `job-e1ba0cbed889` (in-job TECM v3 warm start, 900 steps, deterministic; foreign-render determinism gates 0.0) maps that wrong object onto the same subject/attribute/route register structure used across this campaign, on two seeds.

- **E3 transplant:** writing *only* the foreign carrier's two subject rows into the native Qwen carrier puts a wolf into the native snow scene — fox-ROI moves 0.48–0.59 toward the foreign render on both seeds. The foreign conditioner writes canid-not-fox content into exactly the subject register the object structs name.
- **E2a repair:** writing the native fox rows into the foreign carrier turns the wolf back into a red fox — standing in the still-foreign grass scene. The whole-image progress scalar reported `0.063` here (the scene stays foreign); the pane is unambiguous. Repairing all ~20 active rows restores fox **and** snow together (0.82/0.89 vs. a norm-matched sham of 0.003–0.007).
- **Factorization:** subject identity lives in the subject rows; the scene (snow ↔ grass) lives in the remaining active rows; the compiled carrier's padding rows are apparently healthy, since active-row repair alone suffices.
- **E2b caveat:** route-level row repair *inside* the fully-foreign run is weak (0.05) — with every other row at every site still foreign, two repaired route rows get swamped. Carrier-level repair, not route-level repair, is the effective handle.

**Instrument finding:** a linear dictionary readout — template-residual cosine of the foreign subject rows against eight native animals — scores every candidate at or below the unrelated-pair floor (fox 0.126, wolf 0.104, dog 0.003, floor 0.186), while the native consumer decodes those same rows as a wolf every time. Foreign register content has to be identified causally, by transplant into a native context, not by carrier-space cosine. Failure means wrong lens, measured live.

Proof: `xcond-diagnosis-strip.png` in the [local bundle](../artifacts/semantic-object-registers/), from `saturn/results/object-xcond-diagnosis/job-e1ba0cbed889/`.

## TECM prompt-disjoint scheduler closure: a measured negative

The TECM v4 scheduler closure previously repaired wolf→fox for prompts the closure training saw. The decisive follow-up (`job-0a318a2d8c9d`) holds all four eval prompts (fox, blue_fox, cat, corgi) out of *both* the carrier warm start and the closure fit, training closure only on a disjoint 12-prompt train panel for 240 steps.

Closure loss on the train prompts fell 81% (0.4196 → 0.0802). Held-out RGB-MAD improvements were: fox −0.64 (worse), blue_fox −0.32 (worse), cat +0.89, corgi +8.63. The tell is the corgi row: the prompt-disjoint closed MAD is `87.6044`, essentially identical to the `87.63` reached by a closure run that had actually seen the corgi prompt during training. The held-out gain is generic scaffold pressure, present whether or not closure ever saw a fox.

**Working inference:** v4 scheduler closure is per-prompt repair capacity, not a general Smol→Qwen semantic compiler. The wolf/dog-instead-of-fox failure is a generalization limit of the 21M-parameter compiler under this loss, not a closure-data-coverage problem. Caveat, not established as absent: 240 steps over 12 prompts is fewer per-prompt updates than the original v4 closure's 120 steps over 8 prompts, so a power sweep could still move this result — but the corgi-invariance across both closure policies argues against it.

Evidence: `saturn/results/rosetta-cross-family-manalysis/tecm-scheduler-closure/job-0a318a2d8c9d/analysis.md`.

## Process notes (measured, for the record)

Three submissions failed on pure sizing before this campaign's jobs succeeded: a server-sized ~5 GB cgroup killed the 12B schnell pipeline load in 18 s; a generalized-history sizing proposal put 18.4 GB of VRAM on a 16 GB card (caught by strict preflight); and a klein-9B 50 GB reservation was permanently unschedulable against Beast's floating 12–30 GB baseline until the Qwen3-8B encoder was freed in-worker post-encode and the reservation resized to 42 GB. T5 broke the auto-extractor (`KeyError: 'fox'` — the noun-phrase heuristic is tuned to the Qwen chat layout); the schnell worker now records `row_source` and falls back to an exact-word locator. A pre-run adversarial review caught two science bugs before launch: ROI probes originally ran at the hypothesized route before route certification chose the real one (reordered), and the 9B encode path built autograd graphs under sequential offload (`no_grad` added).

## Claim boundary

**Observation:** the two-row subject patch, cross-scene displacement port, norm-matched-sham inertness, and ×2-scale no-op measured on distilled FLUX.2-klein-4B on 2026-08-18 all reproduce on undistilled klein-base-4B at its native 50-step real-CFG operating point and on klein-9B under sequential offload, on the tested seeds and scenes.

**Convergent trend:** row-sharp object addressing crosses the FLUX.2 family regardless of distillation state, step count, or conditioner width; it degrades to noun-phrase-window granularity on FLUX.1-schnell's bidirectional T5 conditioner rather than disappearing outright; and a known cross-conditioner wrong-object failure factorizes cleanly along the same subject/scene register axes, row-portable in both directions.

**Working inference:** register sharpness tracks conditioner causality (causal-decoder rows vs. bidirectional-encoder windows) rather than model scale or distillation; route redundancy is an operating-point property (more steps, more blocks → any band suffices) layered on top of addresses that stay sharp regardless; and a linear carrier-space readout is the wrong instrument for identifying foreign register content — only a causal transplant test resolves it.

**Terminal status:** convergent portability trend across four checkpoints and two conditioner families, paired with one clean measured negative (TECM v4 closure does not generalize prompt-disjointly). This is not a universal object-algebra certificate, not proof that FLUX.1 and FLUX.2 share a semantic basis, and not evidence that scheduler closure is a general cross-conditioner compiler.

**Not established:** universal single-row addressing on non-Qwen-family conditioners; attribution of FLUX.1's lower full-carrier route ceiling (0.71 vs. 0.98) between its 38 single blocks and the pooled path; klein-9B evidence beyond one seed; results at resolutions other than 256²; and any claim that prompt-disjoint scheduler closure would succeed with a larger closure-step budget — the corgi-invariance argues against it but does not rule it out.

## Local proof bundle and reproduction

The complete compact evidence is in [the local artifact bundle](../artifacts/semantic-object-registers/):

- [Arm A run receipt](../artifacts/semantic-object-registers/run-receipt.job-17788d5a1b0d.json) (`FLUX.2-klein-base-4B`, undistilled, 50-step real CFG)
- [Arm B run receipt](../artifacts/semantic-object-registers/run-receipt.job-638d05dcbff2.json) (`FLUX.2-klein-9B`, sequential offload)
- [Arm C base-battery run receipt](../artifacts/semantic-object-registers/run-receipt.job-a676189574d1.json) and [locality-probe run receipt](../artifacts/semantic-object-registers/run-receipt.job-27fef20e82a0.json) (`FLUX.1-schnell`)
- [Arm E run receipt](../artifacts/semantic-object-registers/run-receipt.job-e1ba0cbed889.json) (cross-conditioner wrong-object diagnosis)
- Proof panes: `zoom-fox-base4b-seed31337.png`, `zoom-mug-port-base4b.png`, `zoom-fox-klein9b-seed7217.png`, `zoom-mug-port-klein9b.png`, `locality-strip-flux1.png`, `xcond-diagnosis-strip.png`
- [Bundle verifier](../artifacts/semantic-object-registers/verify.py)

The full per-branch reports are not copied into the bundle (2.6–5.1 MB each); they remain at [`saturn/results/object-multimodel-flux2/job-17788d5a1b0d/`](../../../saturn/results/object-multimodel-flux2/job-17788d5a1b0d/), [`saturn/results/object-multimodel-flux2/job-638d05dcbff2/`](../../../saturn/results/object-multimodel-flux2/job-638d05dcbff2/), [`saturn/results/object-multimodel-flux1/job-a676189574d1/`](../../../saturn/results/object-multimodel-flux1/job-a676189574d1/), [`saturn/results/object-multimodel-flux1/job-27fef20e82a0/`](../../../saturn/results/object-multimodel-flux1/job-27fef20e82a0/), [`saturn/results/object-xcond-diagnosis/job-e1ba0cbed889/`](../../../saturn/results/object-xcond-diagnosis/job-e1ba0cbed889/), and [`saturn/results/rosetta-cross-family-manalysis/tecm-scheduler-closure/job-0a318a2d8c9d/`](../../../saturn/results/rosetta-cross-family-manalysis/tecm-scheduler-closure/job-0a318a2d8c9d/).

Authoritative accounts: the [preregistration](../../../saturn/experiments/2026-08-19-object-multimodel/PREREGISTRATION.md) and [findings](../../../saturn/experiments/2026-08-19-object-multimodel/FINDINGS.md), plus the [blog synthesis](../../../obsidian/blog/2026-08-19-133500-the-registers-travel-object-semantics-across-flux-models.md).

Reproduction path: workers `run_saturn_object_multimodel_flux2.py`, `run_saturn_object_flux1_schnell.py`, and `run_saturn_object_xcond_diagnosis.py`, submitted respectively by `submit_object_multimodel_flux2.py`, `submit_object_flux1_schnell.py`, and `submit_object_xcond_diagnosis.py` (all in `saturn/workers/`); proof sheets and zoom crops regenerate from each job's `report.json` via `saturn/experiments/2026-08-19-object-multimodel/analyze_multimodel.py`.

Run `python ../artifacts/semantic-object-registers/verify.py` from this directory to check the five job receipts and confirm the referenced proof images are present.
