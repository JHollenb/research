---
title: "Integral Residual Dynamics: Models Consume Trajectory Functionals, Not Sites"
type: research-documentation
status: draft
updated: 2026-09-30
---

# Integral Residual Dynamics

[The paper](paper.md) is the theory-and-certificate companion to the distributed-store measurements. It defines the object — a functional `R = 𝓘(r(t))` of the residual trajectory across depth or denoising time, not the residual at any one site `r(t*)` — the four-quadrant certificate that decides when a mechanism is path-constituted, and the eight operational certificates C1–C8. It reports the cross-family sink grid (8 of 8 measured cells), the scale floor, the transport-cut result, and the consumption kernel with its 2026-09-22 correction.

## Decision: theory-and-certificate companion, not a duplicate

The measurement paper already in this repository, [Single-Site Tests Miss Distributed Stores](../pointwise-instruments-miss-distributed-circuits/README.md), **is** the primary IRD measurement paper: its four-quadrant test, its language-model and diffusion tables, its sparse-autoencoder comparison, its blind-graded readout comparison, and its offline verifiers are built on the IRD receipts (`job-6650205b45eb`, `job-72f0e98679d5`, `job-6299f2391d5c`, `job-8a96572572cd`, `job-69e2f6a6b492`), and its `evidence/four-quadrant-tests/verify.py` re-derives the sink and kernel headline numbers this paper cites.

This paper is therefore staged as **option (a)**: the theory and certificate companion. It states the object formally (`x = s + r`, `R = 𝓘(r(t))`), gives the C1–C8 certificate definitions, and reports the claims that are IRD's own — the four-quadrant certificate; the sink grid (8/8 across four families ≤ 8B plus a 30B MoE identity extension); the scale floor (a capable 70M six-layer model concentrates 79–81% of whole-path necessity in one layer; distributed by ~400M); the transport-cut result (a state-space model does not certify at a residual-stream cut, but two transformers lose their own certificates at that same cut); and the consumption kernel with its 2026-09-22 correction (pixel reproduction of the target render, not identity change). It cross-references [1] and [2] and does not re-run or re-table their numbers.

On the "0.2218 / 0.0013" folklore: the receipt-backed statement is single-step ablation leaves **≥ 0.222** of the transition and all-step ablation leaves **0.0013** ([1] §4.1, §4.6; bundled `job-6650205b45eb`). The specific "0.2218 / 0.0013" *pair* as originally cited in the incoming notes was flagged as absent from the record by the campaign's own Addendum K and replaced with the step-accumulated mediation panel (private `job-7d53e47755f7`). Only receipt-backed numbers are used; §1 of the paper flags the folklore as an example of the failure mode the paper is about.

## Files

- [`paper.md`](paper.md): the paper.
- [`figures/`](figures/README.md): the figures this theory paper relies on live in the companion papers, already decoded from their bundled receipts; `figures/README.md` maps each to its receipt.

## Evidence

This theory paper does not re-bundle receipts. Every measured number is either (i) bundled in a companion paper in this repository, cited by path, or (ii) in the private experiment store, cited by job ID and marked as such.

**Re-derivable from a companion bundle (authoritative):**

- Sink certificate, 1.7B identity necessity + diffusion write schedule (kernel): `evidence/four-quadrant-tests/report-lm-necessity-and-write-schedule-job-6650205b45eb.json` in [1]; `python3 verify.py` re-derives the L12/L18/all-layer necessity values and the kernel ordering.
- Grid replication (color + second family) and P1 path dependence: `evidence/four-quadrant-tests/report-lm-grid-job-72f0e98679d5.json` in [1].
- fp32 dual-backend recheck (8B identity): `evidence/four-quadrant-tests/report-fp32-recheck-job-6299f2391d5c.json` in [1].
- Cross-model slot write at ceiling parity: `evidence/four-quadrant-tests/report-final-tests-rerun-job-69e2f6a6b492.json` in [1].
- Token-time point-read: `evidence/four-quadrant-tests/report-token-time-kernel-job-8a96572572cd.json` in [1].
- FLUX four-quadrant precedent, time accumulation, coordinate freedom, portable verifier: the `data/` and `verifier/` trees of [2].

**Evidence to bundle (candidate receipts; currently in the private experiment store, cited by job ID):**

- P4 cross-slot interchange (W1 hidden vs W2 full-KV trace): `job-0a07cb92d360` (numbers from the completed leg's log receipt; VRAM-kill disclosure in the paper).
- Scale floor (V1 formation over training checkpoints, Pythia 70M / 410M): V1 battery jobs.
- Transport-cut / Mamba result: `job-13a15543fbb1`, `job-8e2d02c4a51e`, `job-0622676c3473`, `job-f11cab813f66`.
- 30B MoE identity + issued-qualified arithmetic: `job-38c1c37dd591`, `job-7cc5b24954f0`, `job-ef8408d9c3d2`.
- Computed-object certificate (" eight"): `job-3b014f386fb8`.
- Kernel universality (V2) and edit transfer (C8/V3) batteries.

Any bundling of the private receipts must follow the redaction convention used in [1]'s `evidence/*/REDACTIONS.json` (replace host-specific paths and machine nicknames with placeholders, leave scalars unchanged, and record before/after SHA-256 hashes), and ship a stdlib `verify.py` that re-derives the headline verdicts. Until that redaction pass is run, the receipts are cited by job ID only.

## References

- [1] [Single-Site Tests Miss Distributed Stores](../pointwise-instruments-miss-distributed-circuits/paper.md).
- [2] [The Circuit That Survived Its Coordinates](../../bfl/docs/certified-semantic-circuits/paper.md).
