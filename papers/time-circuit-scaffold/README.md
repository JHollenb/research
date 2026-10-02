# The Time Circuit Is the Scaffold

Paper 2 of the circuits pair, by Jacob Hollenbeck. The architecture paper.
Companion: Paper 1, [Time-Formed Circuits in Transformers](../time-formed-circuits/).

- Manuscript: [paper.md](paper.md)
- Figures: [figures/](figures/)

## Status

Submission manuscript, 2026-10-02. Audience: frontier-lab interpretability researchers.
Reviewer critiques will arrive by message and drive revision.

Main text about 6,300 words across 12 sections; abstract 220 words; three appendices
(experiment table, methods, reproducibility). Seven figures. All numbers measured on
stock Hugging Face eager execution in float32 unless a line says otherwise; effective
n is stated per claim. A relational-operation addendum that closes the
operation-versus-fact read-map separation prospectively on fresh facts is preregistered
and running at submission time; its placeholder is in Section 5
(`<!-- TODO addendum: relational op -->`), and its numbers will be dropped in there.

## Abstract

A model builds the state controlling its answer over a forward pass: seeded, formed
through ordered execution, committed to a late store, read by a consumer. We show this
time circuit is a fixed scaffold. The location where the store forms and is read is set
by architecture and training; it does not move when the fact, the operation, or the
template changes. What changes per input is a space circuit on it: the operation
re-weights a recurring reader, the fact selects which stored row is read. We hold a
model fixed and decompose the variance of its causal site maps. In Qwen2.5-1.5B a
crossed read-site map attributes 42.2% of variance to which coordinate is read and
29.0% to the operation's weighting, but 1.1% to the fact (1,152 cells); store necessity
at the committed band is 84.0% operation and 3.2% fact (64 cells). Per fresh fact the
commit layer is input-invariant: Gemma-2-2B commits at layer 22 (SD 0.00, 42 facts),
Qwen2.5-1.5B at layer 23 (SD 1.16). A reader profile frozen before evaluation predicts
held relation contexts in all eight; permuting the trained value-projection rows
collapses it. The same organization appears in a state-space and a diffusion model;
standard attribution tools find the space circuit and miss the scaffold. The
cross-family common-graph claim ties a plain additive baseline — a null.

## Evidence map (claim → source path)

Paths are relative to `~/domains`. "Companion" means the claim is carried by Paper 1 and
cited here, not re-derived.

| § | Claim | Effective n / model | Source |
|---|---|---|---|
| 3 | Gemma-2-2B commits only on sliding-window layers (L16–22 carry 0.58; global layers write ≤0) | 8–42 items/cell, single seed; Gemma-2-2B | `saturn/experiments/2026-09-30-full-layer-sweeps/FINDINGS-E17-isolated-kv-writes.md`, `FINDINGS-E19-window-necessity.md` |
| 3 | Commit at ~0.69–0.83 depth across sizes (Mamba 130M L20 / 370M L39 / 2.8B L44) | single seed; Mamba-130M/370M/2.8B | `saturn/experiments/2026-09-30-mamba-full-layer-sweeps/FINDINGS.md` |
| 3 | Commit is a depth-fixed write port; retention is a correlate | 6 cells × 3 prompts; Mamba-130M/370M/2.8B | `saturn/experiments/2026-10-02-mamba-writer-clock-dose/FINDINGS.md` |
| 3 | Formation window closes at the commit layer (Qwen0.5B L21→L22, Mamba L19→L20) | single seed; 4 models | `saturn/experiments/2026-09-30-full-layer-sweeps/FINDINGS-E16-residual-writes.md` |
| 3 | Band necessity is distributed (Qwen1.5B best single 0.08, band L22–27 0.96) | single seed; Qwen2.5-1.5B | `saturn/experiments/2026-09-30-full-layer-sweeps/FINDINGS-E19-window-necessity.md` |
| 3,5 | Commit layer input-invariant per fresh fact (Gemma L22 SD 0.00; Qwen L23 SD 1.16) | 42 identity facts/model | `saturn/experiments/2026-10-02-site-variance-decomposition/FINDINGS.md` |
| 4 | Same bytes, different query → query-selective harm 3.130 / 0.583 / 3.021 nats, 16/16 | 32 same-parent pairs; Qwen2.5-1.5B | `saturn/experiments/2026-10-01-qwen-scaffold-context-poc/FINDINGS.md` |
| 4 | Operation re-weights a recurring reader (within-op cosine 0.92–0.999; across-op 0.336) | Qwen2.5-1.5B, Gemma-2-2B | `saturn/experiments/2026-10-02-site-variance-decomposition/FINDINGS.md` |
| 4 | Fact moves which row is read (selected-row cosine 0.61–0.70 vs reader 0.95–0.96) | Qwen2.5-1.5B | `saturn/experiments/2026-10-02-site-variance-decomposition/FINDINGS.md` |
| 5 | Read-site variance: coord 42.2%, coord×op 29.0%, coord×fact 1.1% (1,152 cells) | Qwen2.5-1.5B | `saturn/experiments/2026-10-02-site-variance-decomposition/FINDINGS.md`, `results/F2_F3_qwen_predictive_readmap.json` |
| 5 | Store necessity: op 84.0%, fact 3.2% (64 cells) | Qwen2.5-1.5B | `saturn/experiments/2026-10-02-site-variance-decomposition/results/F2_scaffold_poc_store_necessity.json` |
| 5 | Three preregistered falsifiers, none triggered | Qwen2.5-1.5B, Gemma-2-2B | `.../2026-10-02-site-variance-decomposition/PREREG.md`, `FROZEN.json` |
| 6 | Frozen 24-coord profile predicts held relation 8/8 (cosine .954 vs .566; RMSE .029 vs .149) | 8 contexts; Qwen2.5-1.5B | `saturn/experiments/2026-10-01-scaffold-confirmation/qwen-predictive/FINDINGS.md` |
| 6 | Full v_proj row permutation collapses the profile (.955→.049 relation) | 4 contexts; Qwen2.5-1.5B | `saturn/experiments/2026-10-01-scaffold-confirmation/FINDINGS.md` |
| 7 | Mamba shared state, two operations; H-only transfer 12/12; 27-coord profile capital 8/8 | 12 rows; Mamba-130M | `saturn/experiments/2026-10-02-mamba-operation-clock-debugger/FINDINGS.md` |
| 7 | Diffusion static bus / per-prompt program; 21/21 byte-exact; early vs late install | 7 specimens, 5 families; FLUX/SDXL | `obsidian/blog/2026-09-30-165158-the-scene-generator-survey-the-machine-is-prompt-agnostic-the-program-is-not.md`, `research/demos/scene-editing.md` |
| 8 | France→Germany two-update feedback (1 of 3 held competent + dev) | 1/3 held; Qwen2.5-1.5B | `saturn/experiments/2026-10-01-scaffold-confirmation/qwen-feedback/FINDINGS.md` |
| 8 | Frozen-reference payload changes B 7/8, preserves A 8/8 | 2 values × 2 orders; Qwen2.5-1.5B | `saturn/experiments/2026-10-01-qwen-frozen-reference-payload/FINDINGS.md` |
| 8 | Source→store mediation (block 0.924, rescue 0.871, 42 rows) | companion; Qwen2.5-1.5B | `saturn/experiments/2026-09-30-full-layer-sweeps/FINDINGS-E20-mediation.md` (Paper 1) |
| 9 | Connected forecast ties additive exactly (MAE .015099 vs .014593), wins 1/3 | 3 held; Qwen2.5-1.5B | `saturn/experiments/2026-10-01-connected-architecture/qwen/FINDINGS.md` |
| 9 | Role-matcher ≈ depth null (6.9125 vs 6.9511) | opened outcomes | `research/papers/scaffolds-and-dynamic-circuits/architectural-paper.md:433` |
| 9 | Cross-family core = 2+2+1 rows (RMSE .0928 vs .8526); color reader misses 8/8 | 2 FLUX + 2 Mamba + 1 Qwen | `saturn/experiments/2026-10-01-scaffold-confirmation/FINDINGS.md`, `cross-family/FINDINGS.md` |
| 10 | Attribution graph sees L0, misses commit band (≤0.08 interchange vs 0.83 K/V cut) | companion; 12+8 items, Gemma-2-2B | `saturn/experiments/2026-09-30-circuit-tracer-head-to-head/FINDINGS.md` (Paper 1) |

## Figure sources

| Figure | Content | Source |
|---|---|---|
| fig1_scaffold_schematic.png | Scaffold + space-circuit schematic | authored for this paper |
| fig2_band_location.png | Commit-layer stability per fact | decisive test F1 |
| fig3_same_patch_query.png | Same-patch / different-query harm | authored from scaffold-context FINDINGS |
| fig4_reader_cosine.png | Reader cosine within-op vs across-op | decisive test F3 |
| fig5_variance_decomposition.png | Variance bars (coord/op/fact/template) | decisive test F2 |
| fig6_confirmation_results.png | Frozen profile vs competitors + permutation | scaffold-confirmation |
| fig7_honest_null.png | Connected forecast tie + role-matcher null | authored from honest-null numbers |

## What is deliberately excluded

The cross-family common role graph is reported as a null (Section 9), not a headline.
Internal tooling names, experiment codes, and job identifiers are confined to Appendix A.
The retired causal-mask-defective feedback instrument is named once in Limitations with
the results it does not touch. The scaffold claim is bounded to the measured models:
two transformers, one state-space model, one diffusion family, single seed.
