---
title: "Model-Family Forensics: Conditioner, Denoiser, Lineage, and VAE Boundaries"
type: experiment-report
status: custody-backed-structural-trend
rank_in_bfl_survey: 11
model: "Pinned FLUX.1 and FLUX.2 Black Forest Labs artifacts"
tags: [bfl, flux, model-forensics, lineage, conditioner, vae, distillation, custody]
---

# Model-Family Forensics: Conditioner, Denoiser, Lineage, and VAE Boundaries

> [!summary]
> Seven pinned Black Forest Labs artifacts were mirrored into exact custody: 2,883 objects totaling 17.442 GB. The evidence separates stock conditioner provenance, a large but structured FLUX.2 Klein 9B→9B-KV rewrite, exact base/distilled trajectory compatibility, bounded FLUX.1→FLUX.2 lineage, and byte-identical FLUX.2 VAE statics. The strongest results are structural and trajectory claims; they do not by themselves establish semantic inheritance or explain why a model behaves as it does.

## Research question

Model-family labels are often treated as informal lineage statements. This experiment asks which parts of the relationship between pinned FLUX artifacts can be established mechanically: are the conditioners stock checkpoints, how much of a paired denoiser changed, do base and distilled variants share an exact trajectory contract, does FLUX.2 retain measurable FLUX.1 structure, and which VAE tensors are actually shared?

The evidence is organized as a custody-backed forensic panel rather than a single similarity score. Tensor inventories, byte identity, parameter counts, activation CKA, principal angles, scheduler trajectories, and cache behavior answer different questions. A positive result on one instrument is not used to infer semantic equivalence on another.

## Custody and specimen set

Seven pinned artifacts were mirrored with exact hashes and metadata. The collection contains 2,883 mirrored objects totaling 17.442 GB. The denoisers include the FLUX.2 Klein 9B and 9B-KV pair, a base/distilled pair, and a FLUX.1→FLUX.2 lineage witness. The conditioner panel includes Dev Mistral-Small-3.2-24B, Klein 9B, and Klein 4B. The VAE panel compares a FLUX.2 quartet against the Schnell codec.

Exact custody is important because forensic claims are only as reproducible as the bytes being compared. Every comparison in this report is bound to the pinned artifact identities retained in the local bundle. The bundle contains narrative records and model-wiki excerpts that define the comparison scope and the measured instruments.

## Conditioner provenance

The Dev conditioner matches the eigenbasis of Mistral-Small-3.2-24B at approximately 0.9999997. The Klein 9B conditioner matches Qwen3-8B at approximately 0.9999992. Klein 4B uses Qwen3-4B. These measurements support stock-checkpoint provenance for the tested conditioner representations. They do not show that the surrounding image model is a stock assembly, nor do they determine how the conditioner is transformed downstream.

## Klein 9B and 9B-KV rewrite

The 9B and 9B-KV pair has an identical 883-tensor inventory and 17,353,362,980 parameters. Despite the inventory identity, 96.10811065795288% of denoiser BF16 values changed. Q/K deltas dominate the V/output deltas, and activation CKA is 0.9382467 under a linear kernel and 0.9447244 under an RBF kernel. The broad alignment indicates a substantial re-alignment rather than a small local patch.

The pair also supports a practical cache observation: a reference K/V can be cached once at approximately 512 MiB, with a measured speed factor around 1.073× in the declared probe. This is a serving-side consequence of the paired artifact structure, not evidence that the two models are semantically interchangeable.

## Base, distilled, and lineage comparisons

The base/distilled pair has an identical 818-tensor inventory and 7,982,059,044 parameters. Adapter gates are present at 22/22 tested locations. Trajectory comparisons are exact at 31/31 and 658/658 checkpoints when the distilled sigma map `{0,1,3}` is aligned to base steps `{0,10,34}`. This establishes an exact tested trajectory compatibility relation under the declared mapping.

The FLUX.1→FLUX.2 lineage witness contains 1,425 matched cells. The median principal-angle residual-facing alignment is 0.0205 against an analytic null of 0.0208. This witness does not detect a distinctive inherited subspace, but the result must not be translated into “fresh initialization”: failure to detect inheritance in one witness is not affirmative evidence of no lineage.

## VAE static identity

The FLUX.2 quartet is byte-identical across six pairwise comparisons, with 251/251 tensors matching. Schnell's 244-tensor codec matches none of those quartet tensors. This cleanly separates a shared FLUX.2 decoder/codec boundary from the Schnell artifact in the tested files. It does not establish that image outputs are identical after arbitrary surrounding model changes or preprocessing differences.

[Model-family forensic inventory](../artifacts/model-family-forensics/black-forest-labs-model-wiki.md)

## What the evidence establishes

The strongest terminal-grade portions are static: custody, tensor inventories, byte identity, parameter counts, and exact trajectory checkpoints. The 9B→9B-KV analysis supports a structured weight rewrite with preserved activation geometry but extensive value changes. The conditioner results support stock-checkpoint provenance. The lineage witness is informative but bounded by its chosen representation and null model.

The evidence does not establish semantic inheritance, a complete genealogy, or a causal explanation for model behavior. CKA and principal angles are geometric instruments. They can show alignment or lack of alignment under a probe, but they cannot by themselves identify a human-interpretable feature or prove that a downstream consumer uses the aligned subspace.

## Claim status

**Observation:** the pinned artifact family contains exact static identities, large structured rewrites, exact mapped trajectories, and bounded geometric lineage signals.

**Convergent trend:** custody, inventories, activation geometry, checkpoint replay, and VAE byte comparisons agree on a layered family structure rather than a single “same model/different model” label.

**Working inference:** Black Forest Labs variants reuse some stable component and trajectory contracts while substantially rewriting denoiser weights and possibly re-aligning internal representations.

**Terminal status:** structural and trajectory forensics under explicit custody. Semantic lineage and unresolved P1–P4 distillation questions remain open.

## Local proof bundle

The bundle contains the pinned model-family wiki, forensic narrative records, and a compact evidence image:

- [model-family evidence](../artifacts/model-family-forensics/black-forest-labs-model-wiki.md)
- [seven-artifact forensic report](../artifacts/model-family-forensics/2026-08-02-seven-flux-artifacts-under-the-microscope.md)
- [conditioner provenance record](../artifacts/model-family-forensics/2026-07-31-145130-the-conditioners-were-stock-checkpoints.md)
- [bundle verifier](../artifacts/model-family-forensics/verify.py)

Run `python ../artifacts/model-family-forensics/verify.py` from this directory to verify custody size, conditioner provenance, denoiser rewrite, lineage witness, and VAE identity values.
