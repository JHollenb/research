# Time-Formed Circuits: Formation, Commitment, and Causal Use

Jacob Hollenbeck. Submission manuscript. Target: arXiv + an interpretability venue; audience = frontier-lab interpretability researchers.

## Abstract

Single-site activation patching and attribution graphs often disagree about where a circuit lives. We argue that some circuits are organized over ordered execution: a source seeds internal state, the model forms it over an interval, commits it to a store with independent causal authority, and a later consumer reads it. Source, formed store, and read localize differently, so a single-site tool can find the source or the read and miss the formed store. In a decoder transformer, a clean identity residual written into a neutral recipient at an early layer makes the recipient's later layers form a late key/value record; blocking that recipient-formed band removes most of the seed's effect on the answer, and transplanting it into a separate unseeded recipient restores it. The block-and-rescue dissociation holds in Qwen2.5-1.5B, Gemma-2-2B, and SmolLM2-1.7B (block removes 0.73-0.92 of the per-row seed gain; transplant recovers 0.71-0.99) and on held-out identities. On Gemma-2-2B an attribution-graph feature basis moves the identity answer at most 0.08 under feature interchange while a native key/value cut flips 83% of answers. A diffusion transformer gives a strictly path-distributed instance that no language-model cell matches, and a weighted additive system can also pass it.

## Status

- **paper.md**: ~8,300 words, ~55 KB, 11 main sections plus Appendices A-C. Submission draft (not committed by this author; the coordinator commits).
- Built on the `space-and-time-circuits/time-emphasis-paper.md` spine, with the cross-family E20 replication, the Mamba clock-dose correction, and a restored full circuit-tracer section integrated.
- Numbers trace to opened source files (see evidence map). No internal tool names, job IDs, or experiment numbers appear in the body; experiment numbers and job IDs appear only in Appendix A.
- Figures: six. Fig 1, Fig 2, Fig 3, Fig 6 are copied from existing receipts; Fig 4 (FLUX) and Fig 5 (circuit-tracer) are small charts generated from the measured numbers in the findings records.

## Evidence map (claim -> source path)

Paths are repo-relative to `~/domains/`.

| Claim in paper (section) | Measured value | Source record |
|---|---|---|
| Block/rescue dissociation across 3 families + held-out (3.4, Fig 1) | block 0.73-0.92; rescue 0.71-0.99; wrong-identity near 0 | `saturn/experiments/2026-10-02-e20-cross-family/FINDINGS.md`; `results/analysis.json` |
| Gemma block 0.768 / rescue 0.985 (n=42) (3.4) | 0.768 [0.752,0.809] / 0.985 [0.980,0.995] | same FINDINGS, Table |
| SmolLM2 block 0.740 / rescue 0.910 (n=34) (3.4) | 0.740 [0.663,0.812] / 0.910 [0.884,0.917] | same FINDINGS |
| Qwen held-out block 0.728 / rescue 0.713 (n=79); rescue cand 81% / full 39% (3.4) | 0.728 / 0.713; 0.81 / 0.39 | same FINDINGS |
| Original Qwen mediation: block 0.924 / rescue 0.871 (n=42); seed gains 1.577-5.555 nats (3.3) | 0.924 [0.765,1.030] / 0.871 [0.850,0.894] | `saturn/experiments/2026-09-30-full-layer-sweeps/FINDINGS-E20-mediation.md`; spine Table 1 |
| Wrong-identity authors own 37/42; earlier-band 0.066 (3.3) | 37/42; 0.066 | same + `2026-10-02-e20-cross-family/results/analysis.json` |
| In-forward L0 0.985 vs isolated 0.009 (2.2) | 0.985 / 0.009 | `.../full-layer-sweeps/FINDINGS-E17-isolated-kv-writes.md` |
| Formation windows: Qwen L24 0.57, L27 0.37; SmolLM2 L23 0.07; Pythia-410M L22 0.01 (3.1) | as stated | `.../full-layer-sweeps/FINDINGS-E16-residual-writes.md` |
| Window necessity table; best w3 Qwen 0.23, Gemma 0.18; Qwen0.5B L20-21 0.99 (3.2, Table 1, Fig 2) | as stated | `.../full-layer-sweeps/FINDINGS-E19-window-necessity.md` |
| Isolated late write 0.81 at Qwen L23 and Gemma L22 (3.2) | 0.81 / 0.81 | `.../full-layer-sweeps/` (E15/E17); E6 FINDINGS line 53 |
| Read: best single-layer necessity 0.074; L23 restore 1.22; one-hot join 1.02, 88% (4) | as stated | `saturn/experiments/2026-09-30-e13-time-circuit-read-join/FINDINGS.md` |
| Exact-row join = oracle at commit; repetition 1.00 vs semantic 0.00 (4) | as stated | `saturn/experiments/2026-09-30-e18-bucket-join-time-reads/FINDINGS.md` |
| Exact-join rescue within 0.03 of clean in cut induction circuit (4) | 0.03 | `saturn/experiments/2026-09-25-ar-exact-join-admission/FINDINGS.md` |
| circuit-tracer: ~30% error-node influence; largest subject layer L0 (11/12, 8/8); commit band 0.10-0.21 (5) | as stated | `saturn/experiments/2026-09-30-circuit-tracer-head-to-head/FINDINGS.md` lines 44-53 |
| Matched feature interchange moves identity <=0.08, color 0.31-0.42 (5, Fig 5) | 0.08 / 0.42 | same FINDINGS lines 147-148 (Amendment) |
| Native K/V second-half flip 0.83 (identity) / 0.84 (color) on 42/25-row sweep (5, Fig 5) | 0.83 / 0.84 | same FINDINGS lines 142-143 (`job-ed4ce1ac5974`) |
| FLUX four-condition bounds 0.5620 / 0.20743 / 0.91309 / 0.01101 (6.1, Table 3, Fig 4) | as stated | `saturn/experiments/2026-09-30-flux2-joint01-time-accumulation/FINDINGS.md` line 22 |
| FLUX 5-seed necessity; sham also nulls; deletion removes target after dp fix (6.1, 6.2) | interchange->source 5/5; deletion->null 5/5 & 4/5; sham->null 5/5 | `.../2026-09-30-e7-flux-color-multiseed/`; `.../2026-09-30-flux2-residual-deletion/FINDINGS.md` |
| Klein-9B single-step <=0.48 vs all-step 0.90-0.95; 8/9 identity, 7/9 lighting (6.2) | as stated | `saturn/experiments/2026-10-01-e8-klein9b-nine-gate/FINDINGS.md` lines 61,68 |
| SDXL single step <=0.215 vs all 0.985; one step meets removal (6.2) | as stated | `saturn/experiments/2026-10-01-e9-sdxl-four-quadrant/` |
| Mamba writer depths L20/L39/L44 = 0.69-0.83 of depth (7) | as stated | `saturn/experiments/2026-09-30-mamba-full-layer-sweeps/FINDINGS.md` |
| Mamba write>clock lever 6/6; clock release doesn't collapse; neighbor clock > writer in 2.8B id (7.1, Fig 6) | write 0.02-1.37 vs clock 0.01-0.40; 0.36 vs 0.04 | `saturn/experiments/2026-10-02-mamba-writer-clock-dose/FINDINGS.md`; `PAPER-SECTION.md` |
| Pythia-70M induction: triple (relay+2 writers) necessary & sufficient; relay 0.58-0.72 (7.2) | as stated | `saturn/experiments/2026-09-30-e4-pythia-recovered-loss/` |
| E10: swap authors donor 19/32, 30/30; removal wrong 26/32, 3/30 (repairs 6/32, 25/30) (8) | as stated | `saturn/experiments/2026-10-01-e10-completed-answer-rerun/FINDINGS.md` |
| E10 two-step: consumed-step unmount 8/8, early 0/8 (8) | as stated | `saturn/experiments/2026-10-01-e10-cot-intermediate-steps/FINDINGS.md` |
| Computed-object cell: operands <=L7, sum L18-L21, necessity 0.35 (8) | as stated | `.../full-layer-sweeps/FINDINGS-E11-computed-object.md` |
| Falcon-H1 hybrid attention-dominated, no SSM writer (7) | as stated | `saturn/experiments/2026-10-01-e14-hybrid-attn-ssm/` |

## Figures

| File | Source | Note |
|---|---|---|
| `figures/fig1-e20-dissociation.png` | copied from `saturn/experiments/2026-10-02-e20-cross-family/results/e20_dissociation_bars.png` | hero: cross-family dissociation bars |
| `figures/fig2-window-necessity.png` | copied from `space-and-time-circuits/figures/fig4-window-necessity.png` | E19 window necessity |
| `figures/fig3-layer-profiles.png` | copied from `space-and-time-circuits/figures/fig3-layer-profiles.png` | per-layer formation/commit profiles |
| `figures/fig4-flux-quadrants.png` | generated from the four measured bounds in the FLUX findings | FLUX four-condition signature |
| `figures/fig5-circuit-tracer.png` | generated from the E6 findings numbers | feature interchange vs native K/V cut |
| `figures/fig6-mamba-clock-dose.png` | copied from `saturn/experiments/2026-10-02-mamba-writer-clock-dose/results/writer-levers.png` | write vs clock lever at the Mamba writer |

## Open gaps (owed before camera-ready)

- Sub-layer-grain sweep of a distributed cell (heads, key vs value, positions in the band) to test whether distributed necessity survives below the layer grain.
- A second model or behavior for the circuit-tracer head-to-head, to turn the instrument-coverage result into a trend.
- External-lab / external-harness replication; all results here are one lab under stock eager attention.
- Fig 1 caption uses the cross-family bars; a redrawn two-panel version pairing the schematic with the bars would read cleaner in print.
