# Time-Formed Circuits: Formation, Commitment, and Causal Use

Jacob Hollenbeck. Submission manuscript. Target: arXiv + an interpretability venue; audience = frontier-lab interpretability researchers.

## Abstract

Activation patching and attribution graphs disagree about where a circuit lives. We show why: some circuits are built over ordered execution, meaning depth, denoising, or recurrence rather than token position. A source seeds internal state, the model forms it over an interval, commits it to a store with independent causal authority, and a later consumer reads it, and these three localize to different places. Our central result is a block-and-rescue dissociation: in Qwen2.5-1.5B, Gemma-2-2B, and SmolLM2-1.7B, blocking the late recipient-formed key/value band removes 73-92% of an early seed's effect, while transplanting that same band into a separate unseeded recipient restores 71-99% and authors the correct answer; a wrong-content control authors the wrong answer, and the effect reproduces on held-out identities. The tools built to find circuits miss this store: on Gemma-2-2B a published attribution-graph feature basis moves the answer at most 0.08 under full feature interchange while a native key/value cut flips 83%. A FLUX.2 diffusion transformer gives a strictly path-distributed instance no language-model cell matches, though a weighted additive mechanism also passes, so that signature names a support profile, not a mechanism.

## Status

- **paper.md**: Round-1 revision. ~9,600 words, ~64 KB, 11 main sections plus Appendices A-C. Submission draft (not committed by this author; the coordinator commits). Abstract 192 words.
- Built on the `space-and-time-circuits/time-emphasis-paper.md` spine, with the cross-family E20 replication, the Mamba clock-dose correction, and a full attribution-graph (circuit-tracer) section integrated.
- Round-1 reviews in `reviews/`; point-by-point response in `reviews/round1-response.md`. Two evidence mismatches (eager/SDPA wording; E11 model) fixed; prior-art set expanded; strict signature de-risked; §5 title softened; a source-to-consumer schematic added as Fig 1; four RUNNING experiments marked with `<!-- TODO ... -->` placeholders.
- Numbers trace to opened source files (see evidence map). No internal tool names, job IDs, or experiment numbers appear in the body; experiment numbers and job IDs appear only in Appendix A.
- Figures: six. Fig 2 (E20 bars), Fig 3 (window necessity), Fig 6 (Mamba) are copied from receipts; Fig 1 (schematic), Fig 4 (circuit-tracer), Fig 5 (FLUX) are generated from measured numbers / as a diagram.

## Evidence map (claim -> source path)

Paths are repo-relative to `~/domains/`.

| Claim in paper (section) | Measured value | Source record |
|---|---|---|
| Block/rescue dissociation across 3 families + held-out (3.4, Fig 2) | block 0.73-0.92; rescue 0.71-0.99; wrong-identity near 0 | `saturn/experiments/2026-10-02-e20-cross-family/FINDINGS.md`; `results/analysis.json` |
| Gemma block 0.768 / rescue 0.985 (n=42) (3.4) | 0.768 [0.752,0.809] / 0.985 [0.980,0.995] | same FINDINGS, Table |
| SmolLM2 block 0.740 / rescue 0.910 (n=34) (3.4) | 0.740 [0.663,0.812] / 0.910 [0.884,0.917] | same FINDINGS |
| Qwen held-out block 0.728 / rescue 0.713 (n=79); rescue cand 81% / full 39% (3.4) | 0.728 / 0.713; 0.81 / 0.39 | same FINDINGS |
| Original Qwen mediation: block 0.924 / rescue 0.871 (n=42); seed gains 1.577-5.555 nats (3.3) | 0.924 [0.765,1.030] / 0.871 [0.850,0.894] | `saturn/experiments/2026-09-30-full-layer-sweeps/FINDINGS-E20-mediation.md`; spine Table 1 |
| Wrong-identity authors own 37/42; earlier-band 0.066 (3.3) | 37/42; 0.066 | same + `2026-10-02-e20-cross-family/results/analysis.json` |
| In-forward L0 0.985 vs isolated 0.009 (2.2) | 0.985 / 0.009 | `.../full-layer-sweeps/FINDINGS-E17-isolated-kv-writes.md` |
| Formation windows: Qwen L24 0.57, L27 0.37; SmolLM2 L23 0.07; Pythia-410M L22 0.01 (3.1) | as stated | `.../full-layer-sweeps/FINDINGS-E16-residual-writes.md` |
| Window necessity table; best w3 Qwen 0.23, Gemma 0.18; Qwen0.5B L20-21 0.99 (3.2, Table 1, Fig 3) | as stated | `.../full-layer-sweeps/FINDINGS-E19-window-necessity.md` |
| Identity-clustered sensitivity bootstrap, original Qwen panel: block [0.732,1.075], rescue [0.835,0.894] (3.3) | as stated | `.../full-layer-sweeps/FINDINGS-E20-mediation.md`; spine Table 1 caption |
| Isolated late write 0.81 at Qwen L23 and Gemma L22 (3.2) | 0.81 / 0.81 | `.../full-layer-sweeps/` (E15/E17); E6 FINDINGS line 53 |
| Read: best single-layer necessity 0.074; L23 restore 1.22; one-hot join 1.02, 88% (4) | as stated | `saturn/experiments/2026-09-30-e13-time-circuit-read-join/FINDINGS.md` |
| Exact-row join = oracle at commit; repetition 1.00 vs semantic 0.00 (4) | as stated | `saturn/experiments/2026-09-30-e18-bucket-join-time-reads/FINDINGS.md` |
| Exact-join rescue within 0.03 of clean in cut induction circuit (4) | 0.03 | `saturn/experiments/2026-09-25-ar-exact-join-admission/FINDINGS.md` |
| circuit-tracer: ~30% error-node influence; largest subject layer L0 (11/12, 8/8); commit band 0.10-0.21 (5) | as stated | `saturn/experiments/2026-09-30-circuit-tracer-head-to-head/FINDINGS.md` lines 44-53 |
| Matched feature interchange: subject-all-layer identity <=0.08, color 0.31-0.42; every-position color 0.32-0.34 (5, Fig 4) | 0.08 / 0.42 / 0.32-0.34 | same FINDINGS lines 118-148 (Amendment) |
| Graph-top features move identity -0.03 to -0.14, color to -0.19 (5) | as stated | same FINDINGS lines 124,136 |
| Native K/V second-half flip 0.83 (identity) / 0.84 (color) on 42/25-row sweep (5, Fig 4) | 0.83 / 0.84 | same FINDINGS lines 142-143 (`job-ed4ce1ac5974`) |
| FLUX four-condition bounds 0.5620 / 0.20743 / 0.91309 / 0.01101 (6.1, Table 3, Fig 5) | as stated | `saturn/experiments/2026-09-30-flux2-joint01-time-accumulation/FINDINGS.md` line 22 |
| FLUX 5-seed necessity; sham also nulls; deletion removes target after dp fix (6.1, 6.2) | interchange->source 5/5; deletion->null 5/5 & 4/5; sham->null 5/5 | `.../2026-09-30-e7-flux-color-multiseed/`; `.../2026-09-30-flux2-residual-deletion/FINDINGS.md` |
| Klein-9B single-step <=0.48 vs all-step 0.90-0.95; 8/9 identity, 7/9 lighting (6.2) | as stated | `saturn/experiments/2026-10-01-e8-klein9b-nine-gate/FINDINGS.md` lines 61,68 |
| SDXL single step <=0.215 vs all 0.985; one step meets removal (6.2) | as stated | `saturn/experiments/2026-10-01-e9-sdxl-four-quadrant/` |
| Mamba writer depths L20/L39/L44 = 0.69-0.83 of depth (7) | as stated | `saturn/experiments/2026-09-30-mamba-full-layer-sweeps/FINDINGS.md` |
| Mamba write>clock lever 6/6; clock release doesn't collapse; neighbor clock > writer in 2.8B id (7.1, Fig 6) | write 0.02-1.37 vs clock 0.01-0.40; 0.36 vs 0.04 | `saturn/experiments/2026-10-02-mamba-writer-clock-dose/FINDINGS.md`; `PAPER-SECTION.md` |
| Pythia-70M induction: triple (relay+2 writers) necessary & sufficient; relay 0.58-0.72 (7.2) | as stated | `saturn/experiments/2026-09-30-e4-pythia-recovered-loss/` |
| E10: swap authors donor 19/32, 30/30; removal wrong 26/32, 3/30 (repairs 6/32, 25/30) (8) | as stated | `saturn/experiments/2026-10-01-e10-completed-answer-rerun/FINDINGS.md` |
| E10 two-step: consumed-step unmount 8/8, early 0/8 (8) | as stated | `saturn/experiments/2026-10-01-e10-cot-intermediate-steps/FINDINGS.md` |
| Computed-object cell (SmolLM2-1.7B, 24 layers): operands <=L7, sum L18-L21, necessity 0.35 at L17 (8) | as stated | `.../full-layer-sweeps/FINDINGS-E11-computed-object.md` |
| Falcon-H1 hybrid attention-dominated, no SSM writer (7) | as stated | `saturn/experiments/2026-10-01-e14-hybrid-attn-ssm/` |

## Figures

| File | Source | Note |
|---|---|---|
| `figures/fig1-schematic.png` | generated diagram | source -> formation -> commit -> store -> consumer, with block and transplant |
| `figures/fig2-e20-dissociation.png` | copied from `saturn/experiments/2026-10-02-e20-cross-family/results/e20_dissociation_bars.png` | hero: cross-family dissociation bars |
| `figures/fig3-window-necessity.png` | copied from `space-and-time-circuits/figures/fig4-window-necessity.png` | E19 window necessity |
| `figures/fig4-circuit-tracer.png` | generated from the E6 findings numbers | feature interchange vs native K/V cut (grouped by behavior) |
| `figures/fig5-flux-quadrants.png` | generated from the four measured bounds in the FLUX findings | FLUX four-condition signature |
| `figures/fig6-mamba-clock-dose.png` | copied from `saturn/experiments/2026-10-02-mamba-writer-clock-dose/results/writer-levers.png` | write vs clock lever at the Mamba writer |

(The orphaned per-layer-profiles figure from the first draft was cut; the schematic was added in its place.)

## Open gaps (RUNNING or owed before camera-ready)

RUNNING (placeholder `<!-- TODO ... -->` in the body):
- **P1-A formation vs propagation** (§3.5): seed-layer vs late-band transplant into the fresh recipient; the late band must beat a linear image of the seed for "formation" to be construction rather than carriage.
- **P1-B identity-clustered bootstrap** (§3.3/§3.4): the original Qwen panel now carries an identity-clustered interval; the cross-family clustered re-estimate is pending.
- **P1-C error-node swap** (§5): a fully matched interchange that swaps transcoder error nodes as well as features, to decide "content sits in the error" vs "attribution graphs cannot see it."
- **9B scale** (§3/§10): a 7-9B block-and-rescue replication; the strict signature and mediation are currently at or below 4B, and Qwen3-30B's in-forward certificate did not survive the isolated cut.

Owed:
- Sub-layer-grain sweep of a distributed cell (heads, key vs value, positions in the band).
- A second model or behavior for the circuit-tracer head-to-head, to make the instrument-coverage result a trend.
- External-lab / external-harness replication; all results here are one lab, stock eager attention (stock SDPA for the §8 arithmetic cells).
