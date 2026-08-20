---
title: "Cross-Family Conditioner Compilation: FLUX.2 Rosetta to FLUX.1 Replay"
status: convergent-portability-trend
rank_in_bfl_survey: 3
model_scope: "FLUX.2 Klein 4B primary; FLUX.1 Schnell extension"
model_ids:
  - "black-forest-labs/FLUX.1-schnell"
  - "black-forest-labs/FLUX.2-klein-4B"
revisions:
  flux1_schnell: "741f7c3ce8b383c54771c7003378a50191e9efe9"
  flux2_klein_4b: "e7b7dc27f91deacad38e78976d1f2b499d76a294"
checkpoint_role: "FLUX.2 recipient substrate; FLUX.1 cross-family extension"
source_conditioners: "native Qwen; SmolLM2-1.7B; Mamba-1.4B"
backend: "CUDA on Beast; FP8 storage with sequential CPU offload"
consumer: "native FLUX.2/FLUX.1 denoiser, scheduler, VAE, and RGB image output"
tags: [bfl, flux, flux1, flux2, conditioner, cross-family, checkpoint-replay, causal-route, portability]
---

# Cross-Family Conditioner Compilation: FLUX.2 Rosetta to FLUX.1 Replay

> [!summary] The original experiment was FLUX.2 Klein 4B: native Qwen was the reference conditioner, while family-local SmolLM2 and Mamba lowerings drove the same frozen denoiser, scheduler, and VAE. Full-state interventions reached `.751` and `.817` normalized rescue, and scheduler closure repaired the three seen prompts substantially, although the held-out corgi remained wrong. FLUX.1 Schnell then extended the result with cross-family checkpoint/replay/debugger parity, 40 batched branches, and four exact scalar validations. This is near-closure and strong portability evidence—not a universal semantic compiler or proof of identical FLUX.1/FLUX.2 circuits.

## The promoted result

This experiment is one of the strongest portability results in the BFL record because it began by making the FLUX.2 conditioner boundary executable, then carried the same discipline to FLUX.1. The original FLUX.2 Klein 4B work used native Qwen as the reference and separately fitted SmolLM2 and Mamba family-local conditioners. The foreign paths crossed the native `[512, 7680]` carrier ABI and were judged by the real scheduler/VAE/RGB consumer rather than by hidden-state similarity alone.

The later FLUX.1 extension targeted a different native contract: a T5 token stream plus pooled CLIP condition. Saturn compiled SmolLM2 into that dual conditioner ABI, kept the transformer, scheduler, and VAE frozen, and judged the result through the native RGB consumer.

The same program boundary then supported checkpoint capture, exact scalar resume, batched suffix replay, preserved conditioner state, typed debugger addresses, and causal route panels on both families. That is the important promotion: the instrumentation contract crossed the family even though the learned semantic coordinate system did not come along for free.

## Specimens and execution contract

The primary recipient was distilled `black-forest-labs/FLUX.2-klein-4B` at revision `e7b7dc27f91deacad38e78976d1f2b499d76a294`. Its native Qwen conditioner was the reference; the SmolLM2 and Mamba adapters were family-local frontends. The later native target was `black-forest-labs/FLUX.1-schnell` at revision `741f7c3ce8b383c54771c7003378a50191e9efe9`. FLUX.1's 19 joint and 38 single blocks therefore cannot be read as the same physical layers as Klein 4B's 5 joint and 20 single blocks.

For the original Klein campaign, the suffix, initial latent, image IDs, scheduler, VAE, and model revision stayed fixed while one resident CUDA load evaluated six baselines, two exact checkpoint no-ops, and 22 scalar causal branches. The Mamba sequential-fallback warning affected performance only; its numerical and replay contract passed.

The FLUX.2 SmolLM2 path used a roughly 14.97M-parameter family-local adapter into the native `[512, 7680]` Qwen-side prompt carrier. The corrected comparison used 700 masked steps; the older 300-step unmasked row is retained as historical underfit evidence. The FLUX.2 Mamba path used a separate family-local adapter. The source encoders, native Qwen teacher, denoiser, scheduler, and VAE remained outside the serving-time foreign path.

For the FLUX.1 extension, a 14,378,496-parameter cross-attention adapter mapped frozen SmolLM2 hidden states from `[512, 2048]` into the native `[512, 4096]` T5 stream and `[768]` pooled CLIP stream. That adapter used eight training prompts, four held-out prompts, 700 optimization steps, and deterministic seed `7217`.

The native/adapted contrast used four denoising steps, `256×256`, guidance `0.0`, and the same latent seed. The real runtime used FP8 layerwise storage and sequential CPU offload on the Beast CUDA host; the placement strategy changed residency, not the declared parity contract.

## Original FLUX.2 conditioner campaign

The first and most important leg was FLUX.2 Klein 4B itself. Native Qwen was the reference conditioner; SmolLM2 and Mamba were separately fitted family-local frontends. The frozen Klein consumer saw the same prompt pair, latent, image IDs, scheduler, VAE, and checkpoint while only the conditioner path changed.

The all-step full-state interventions moved the native consumer strongly toward the Qwen reference:

| family-local frontend | full-state rescue | wrong-prompt control |
| --- | ---: | ---: |
| SmolLM2 | `.751` | `−.265` |
| Mamba | `.817` | `−.172` |

The sham branches were exactly zero. Compact selectors did not reproduce the effect: stable channels reached only `.036`/`.051`, lexical slots `−.002`/`.003`, and contrast slots `.047`/`.054` for SmolLM2/Mamba. The carrier is distributed and consumer-dependent rather than a tiny lexical slot or channel block.

The corrected 700-step Smol run reached same-prompt image cosine `0.8258` and red/blue MAD `11.423` against native Klein's `70.954`. That is not equivalent semantic conditioning, but it is much closer than the historical underfit row and it reproduces the exact checkpoint/replay mechanics. The later scheduler-closed TECM v4 run pushed the result through the real denoiser, scheduler transition, and VAE: mean RGB-MAD improvement was `50.1856` on the three downstream-seen prompts and `7.2718` on the held-out corgi. The seen blue-fox, cat, and red-fox outputs became native-like; the held-out corgi remained the wrong dog/scene.

This is why the result deserves high placement: it got genuinely close to a usable foreign conditioner on the declared FLUX.2 panel, and the remaining failure is informative. Full-state lowering works much better than compact selectors, while donor-free general semantic translation and held-out equivalence remain open.

## FLUX.1 extension: what the native consumer showed

The adapted branch produced coherent, structured images rather than noise, but the named character or object drifted. In the red/blue fox contrast, the broad snow-lit scene and color scaffold remained more stable than fox identity. The held-out lighthouse, astronaut corgi, oranges, and snowy cabin panel showed the same scene-versus-character dissociation.

| measurement | observed value |
| --- | ---: |
| training token cosine | `0.9501` |
| held-out token cosine | `0.5076` |
| held-out pooled cosine | `0.4460` |
| native/adapted held-out image cosine | `0.7392` |
| native red↔blue image MAD | `111.7350` |
| adapted red↔blue image MAD | `86.2943` |
| adapted/native red↔blue separation | `0.7723` |

The image cosine is not a semantic score, and the red/blue MAD is not a character classifier. Together with the native-consumer images, they establish a narrower observation: a shape-legal foreign conditioner can drive the frozen suffix into a structured image regime while its semantic coordinate alignment remains incomplete.

## FLUX.1 checkpoint and causal panel

The corrected FLUX.1 runtime uses the same bounded `capture_checkpoint + resume_checkpoint` assay as the FLUX.2 path. It retains the packed latent, both conditioner streams, scheduler state, resolution, and execution metadata, then resumes the unchanged native suffix. The panel contains 40 batched branches and four exact scalar validations.

The shared route vocabulary is:

```text
conditioning → joint.2 → joint.3 → joint.4 → single.0
             → return_register → vae_rgb
```

The FLUX.1 native image consumer responded selectively under the declared red/blue panel:

| intervention | result | MAD vs red | MAD vs blue |
| --- | --- | ---: | ---: |
| sufficiency: `joint.4@2` | stayed red | `1.7893` | `65.5385` |
| necessity: `joint.4@2` | became blue | `65.7333` | `2.6845` |
| coalition: `joint.2+joint.3+joint.4@2` | stayed red | `1.9591` | `65.5420` |
| rescue: `joint.2→joint.3@2` | became blue | `65.2726` | `1.8203` |

Ordered mediation probes recovered positive, decreasing rescue fractions across the route: `joint.2 → joint.3: 0.3700`, `joint.3 → joint.4: 0.3275`, and `joint.4 → single.0: 0.2626`. This is a causal route under the declared prompt, seed, checkpoint, and intervention recipe, not a multiseed universal-circuit certificate.

## Why this ranks above a generic cross-model demo

The work closes several boundaries at once. In the original FLUX.2 leg, SmolLM2 and Mamba reached the native Qwen consumer strongly enough to support `.751`/`.817` full-state rescue, and scheduler closure repaired the three seen prompts. In the FLUX.1 extension, the same checkpoint/replay/debugger/causal-panel surface crossed to a different conditioner ABI and reached the native RGB consumer. At the same time, the result keeps the hard negative visible: FLUX.1 and FLUX.2 do not share a proven semantic basis merely because `joint.2` and `single.0` are legal aliases in both runtimes.

The correct portability statement is therefore **shared execution surface, local learned state**. The route vocabulary is a useful Saturn coordinate system and search prior. Payloads, carrier timing, semantic labels, minimal intervention sets, and causal effects must be revalidated on each checkpoint and conditioner contract.

## Claim boundary

**Observation:** family-local SmolLM2 and Mamba conditioners can drive the frozen FLUX.2 Klein consumer toward native Qwen state, with a strong full-state rescue and later scheduler-closed repair on seen prompts; SmolLM2 can also be compiled into the native FLUX.1 dual-conditioner ABI.

**Convergent trend:** the FLUX.2 and FLUX.1 legs repeat the clean-but-wrong scene-versus-character dissociation at different strengths, while shared checkpoint/replay/debugger instrumentation and native-consumer panels survive the family change.

**Terminal status:** near-closure on the declared FLUX.2 prompt split, plus FLUX.1 feature parity and exploratory native-consumer route evidence, are established for the pinned checkpoints. Circuit equivalence, universal foreign-conditioner compilation, donor-free held-out generalization, and portable semantic addresses remain open.

## Evidence

- [full cross-family report](../../../obsidian/blog/2026-08-09-saturn-flux1-cross-compiled-conditioner.md)
- [Klein executable-machine report](../../../obsidian/blog/2026-08-14-we-treated-klein-like-an-executable-machine.md)
- [frontier ranking and scheduler-closure audit](../../../obsidian/blog/2026-08-14-bfl-frontier-surprise-top-20.md)
- [cross-family Rosetta consolidation](../../../saturn/results/rosetta-cross-family-manalysis/ROSETTA-CONSOLIDATED.md)
- [FLUX.2 semantic bridge closure](../../../saturn/results/rosetta-semantic-bridge-closure/job-21e43d04de4d/analysis.md)
- [FLUX.2 scheduler-closed analysis](../../../saturn/results/rosetta-cross-family-manalysis/tecm-scheduler-closure/job-ffb476166198/analysis.md)
- [FLUX.2 scheduler-closed report](../../../saturn/results/rosetta-cross-family-manalysis/tecm-scheduler-closure/job-ffb476166198/report.json)
- [FLUX.2 four-axis cross-family analysis](../../../saturn/results/rosetta-cross-family-four-axis/job-84662678d2a1/analysis.md)
- [FLUX.1 fixed causal report](../../../saturn/results/rosetta-cross-family-manalysis/flux1-native-fixed/flux1-native.json)
- [FLUX.1 fixed run receipt](../../../saturn/results/rosetta-cross-family-manalysis/flux1-native-fixed/flux1-native-run-receipt.json)
- [FLUX.1 vs FLUX.2 comparison](../../../saturn/results/flux1-cross-compiled/job-a2cd2f54c6f4/flux1-vs-flux2-comparison.md)
- [cross-family conditioner implementation](../../../saturn/src/saturn/flux1_conditioner.py)
- [FLUX.1 checkpoint adapter](../../../saturn/src/saturn/flux1_checkpoint.py)
- [shared PhasePipeline](../../../mrun/src/mrun/diffusion/phase.py)
