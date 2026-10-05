# Research

Papers, demonstrations, and evidence bundles from a program that treats a trained model as software: capture its state at a declared boundary, fork it, change one thing, replay it exactly, and let the model's own output judge the change. Every number in the papers traces to a frozen result file, and the headline numbers are bound to those files in a hash-chained [evidence registry](papers/evidence-registry/README.md) that re-checks offline.

## Start here

Three results carry the program. Each is measured on public checkpoints with a stock forward pass, and each has a preregistered or blind component.

**1. A formed key/value band can be moved between models and it carries the answer.**
[Time-Formed Circuits](papers/time-formed-circuits/README.md). An early residual patch seeds a fact, the model forms it over depth, and the formed state commits to a late key/value band. Blocking that band removes 73–92% of the seed's effect; transplanting the same band into a separate model that never saw the seed restores 71–99% and authors the correct answer, while a wrong-content band authors the wrong one. The transplant reproduces in eight decoder families at 1B to 7B, four of them with the band fixed blind before any mediation job. Where a blind locator missed, a causal window sweep found the band (GPT-2 XL block 0.16 → 0.89). Attribution-graph methods cannot reach this band: a matched transcoder interchange moves the identity answer 0.31 of the way against 0.94 for a native key/value cut. This is the paper to read first.

**2. Single-site tests miss distributed stores, measured against standard tooling.**
[Single-Site Tests Miss Distributed Stores](papers/pointwise-instruments-miss-distributed-circuits/README.md). In FLUX.2 Klein 4B no single denoising step or component is necessary or sufficient, while all of them together are both (22% survives any single ablation; 0.13% survives the joint one; insertion carries 91%). In three language-model families single-layer key/value replacement removes at most 18% while the second half of layers removes 81–104%. A preregistered head-to-head with SAELens and Gemma Scope, and a blind-graded comparison of four standard readouts, ship with offline verifiers that re-derive every headline value.

**3. Instruments and baselines audited against public ground truth.**
[One Grokked Circuit Is Not a Certificate](papers/instrument-audit-interpbench/README.md) scores three in-house instruments and the standard baselines against all 86 InterpBench circuits, with the benchmark's own generators and a hash-frozen scorer. Activation patching, EAP-IG and EAP reproduce the published ordering (0.990 / 0.976 / 0.892); two of the lab's own instruments sit at chance in the form a single known circuit had certified, and one constraint change rescues each. [Score Multi-Turn Interventions Against the Pass-Indexed Native](papers/pass-indexed-baseline/README.md) measures a baseline error most multi-turn intervention studies make: scoring against the single-turn parent instead of the model's own continuation flips 11 of 12 conclusions on Qwen2.5-1.5B and mis-sizes the effect by 2.7 nats under a chat template.

Two further manuscripts build on these. [Dynamic Circuits Loop Through a Stable Time Scaffold](papers/time-circuit-scaffold/README.md) states the architecture hypothesis the first paper suggests, with its falsifiers and which ones fired. [mdb and saturn-pub](papers/mdb-saturn-pub/README.md) describes the two public packages that run every experiment above as a receipted, forkable, replayable transaction across transformer, state-space and diffusion models.

The full list, including earlier drafts and what superseded them, is in [papers/README.md](papers/README.md).

## Why this work holds up

- **The model judges.** Interventions are scored by the unchanged native readout, not by a probe or a proxy metric.
- **Exact replay.** Checkpoints are frozen, decoding is greedy, and each intervention is a fixed cache edit, so a repeat run reproduces the logits bit for bit; canaries (no-op self-install, fact-span invariance, determinism) run in every job.
- **Preregistration and blind tests.** Predictions and scorers are hash-frozen before data; failed predictions are reported with the falsifier that fired.
- **Stock execution.** Headline claims run on unmodified Hugging Face eager forward passes and were validated against TransformerLens where a comparison exists.
- **Receipts.** Every result folder carries the worker, the frozen design, the collected reports, and the verifier; the registry binds headline numbers to receipt bytes.

## Diffusion program

The [Black Forest Labs line](bfl/README.md) applies the same discipline to FLUX: capture typed boundaries from conditioner through denoiser, scheduler, and VAE; fork matched futures; change a route, phase, carrier, or state; ask the native image consumer what changed. Its strongest pieces are exact phase-resident serving, consumer-closed route promotion, cross-family conditioner compilation, and the [certified distributed semantic route](bfl/docs/certified-semantic-circuits/README.md) in FLUX.2 Klein 4B. The [tracer cards](bfl/docs/tracer/README.md) document the checkpoint-scoped instrumentation and the [artifacts](bfl/artifacts/) hold receipts, proof sheets, and verification scripts.

## Limits, stated once

One laboratory, one harness, mostly single seed, models at and below 7B. Outside replication is the open item for every paper; each reproducibility appendix lists the checkpoints, panels, frozen bands, and verifier an outside group needs.

# About me

My name is Jacob Hollenbeck. I have a B.S. in Electrical and Computer Engineering from Boise State and an M.S. in Machine Learning from Georgia Tech OMSCS. I have been a full-stack software engineer for 10+ years. This repository is a sample of my research into decomposing models and treating them as software.
