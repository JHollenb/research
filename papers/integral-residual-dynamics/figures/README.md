# Figures

This is a theory-and-certificate companion. The figures it relies on are already decoded from bundled receipts in the companion papers; rather than duplicate the image bytes, this file maps each figure to its source and to the receipt behind it. Every figure is re-derivable from a bundle in this repository.

| figure (in a companion paper) | what it shows for this paper | receipt |
|---|---|---|
| [`fig1-single-step-patching.png`](../../pointwise-instruments-miss-distributed-circuits/figures/fig1-single-step-patching.png) | the four-quadrant sink shape in the diffusion model: single-component, single-step interventions read as "no effect" while the same components across all steps remove (0.13% remains) or carry (91.1%) the transition | bundled `job-6650205b45eb` (and `job-72f0e98679d5`) in [1] |
| [`fig2-write-schedule.png`](../../pointwise-instruments-miss-distributed-circuits/figures/fig2-write-schedule.png) | the consumption kernel on the diffusion time axis, front-loaded and non-exchangeable, with the 2026-09-22 correction (progress is pixel reproduction of the target render, not identity change) | bundled `job-6650205b45eb` in [1] |
| [`fig2-separation-curves.png`](../../../bfl/docs/certified-semantic-circuits/figures/fig2-separation-curves.png) | the monotone accumulation of internal separation across denoising steps (0.355 → 0.919 → 2.487 → 9.723 for identity), the direct evidence that the object is a trajectory integral | [2], §5 |

If the private IRD receipts listed under "Evidence to bundle" in [`../README.md`](../README.md) are later redacted and bundled here, their decoded panes (the P4 cross-slot interchange table and the 30B quadrant table) belong in this directory, decoded by a stdlib script alongside the bundle's `verify.py`, following the convention in [1].

- [1] [Single-Site Tests Miss Distributed Stores](../../pointwise-instruments-miss-distributed-circuits/paper.md).
- [2] [The Circuit That Survived Its Coordinates](../../../bfl/docs/certified-semantic-circuits/paper.md).
