---
title: "Space and Time Circuits: Causal Control Across Model Trajectories"
type: research-documentation
status: draft-3
updated: 2026-10-01
---

# Space and Time Circuits: Causal Control Across Model Trajectories

[The paper](paper.md) (draft 3; the original outline is preserved in [`outline.md`](outline.md)) consolidates four documents into one argument:

- the certified FLUX.2 route ([`../../bfl/docs/certified-semantic-circuits/`](../../bfl/docs/certified-semantic-circuits/README.md));
- the measurement paper ([`../pointwise-instruments-miss-distributed-circuits/`](../pointwise-instruments-miss-distributed-circuits/README.md));
- the IRD theory draft ([`../integral-residual-dynamics/`](../integral-residual-dynamics/README.md));
- the final-boss / transaction draft ([`../capabilities-as-transactions/`](../capabilities-as-transactions/README.md)).

The argument has four parts:

1. **Compatible locality and time axes.** A space circuit has locally decisive support. A time-formed circuit depends on ordered execution. A local source, commit, latch or readout can participate in a time-formed computation.
2. **Architecture-level variations.** Diffusion accumulation updates a carrier across denoising steps; autoregressive formation/commit transforms source state through depth into a later read store; SSM retention/latch forms recurrent state and can hold it locally for a later consumer. These are definitions, not universal claims about every model in an architecture family.
3. **A strict path-distributed subtype.** The four-quadrant certificate identifies a subtype with no individually necessary or sufficient site at the declared cut, while the whole path is both. FLUX exhibits that signature across denoising steps. The original formation/commit panels and standalone Mamba cells are time-formed but do not pass all four quadrants; Falcon adds a post-subject hybrid formed-state profile without establishing its formation or retention clock.
4. **Static/dynamic structure and editing.** In the tested diffusion system, per-prompt dynamic circuits load onto static infrastructure, and the image-editing and scene-compilation results follow from that timing structure.

## Status

Draft 3 (updated 2026-10-01): full prose for every section whose results are settled. Open items are marked inline:

- **TODO [E#]** marks an experiment to run (Appendix A);
- **TODO [R#]** marks a collation or correction step (Appendix B);
- **TODO [W]** marks writing only.

The 2026-10-01 status update reconciles the completed experiments through E19 with the summaries and limitations, including the recovered E14 Falcon hybrid run. Earlier sampled verdicts and historical nulls remain labeled as such. E10 establishes causal use of non-restated intermediate arithmetic state; E12/E18 establish bucket-and-join replacement in the tested settings, while query-derived semantic selection remains open.

E14 shows attention-dominated formed-state dependence, partial SSM writing and no strong concentrated SSM writer or new strict certificate. The [pinned report and verifier](evidence/hybrid-attn-ssm/README.md) are bundled here. This narrows the recurring late-writer claim while preserving the FLUX result. E10's corrected account distinguishes use of an already cached consumed step from regeneration of that step after intervention.

The as-is paper directory was committed at `369ab87` before this recovery revision. The [recovery audit](critiques/experiment-recovery-2026-10-01.md) records the inclusion gaps and source checks.

Results produced on 2026-09-30 by the blind-certification and grail tooling are excluded at the author's direction.

Assessment and census notes behind this outline: [`../capabilities-as-transactions/assessment-notes.md`](../capabilities-as-transactions/assessment-notes.md).
