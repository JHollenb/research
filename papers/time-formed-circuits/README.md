# Time-Formed Circuits: Formation, Commitment, and Causal Use

Jacob Hollenbeck. Submission manuscript. Target: arXiv + an interpretability venue; audience = frontier-lab interpretability researchers.

## Abstract

Activation patching and attribution graphs disagree about where a circuit lives. We show why: some circuits are built over ordered execution — depth, denoising, or recurrence, not token position. A source seeds state, the model forms it over an interval, commits it to a store with independent authority, and a later consumer reads it, and these three localize to different places. Our central result is a block-and-rescue dissociation: in Qwen2.5-1.5B, Gemma-2-2B, and SmolLM2-1.7B, blocking the late recipient-formed key/value band removes 73-92% of an early seed's effect, while transplanting that same band into a separate unseeded recipient restores 71-99% and authors the correct answer; a wrong-content control authors the wrong answer, and the effect reproduces on held-out identities. The tools built to find circuits cannot reach the identity store: on Gemma-2-2B even a matched interchange of transcoder features and their error nodes moves the identity answer at most 0.31 of the way, against 0.94 for a native cut, because the store is attention-formed and that basis replaces only the MLP sublayers. A FLUX.2 diffusion transformer gives a strictly path-distributed instance no language-model cell matches, though a weighted additive mechanism also passes it. Construction history is part of a circuit's causal anatomy.

## Status

- **paper.md**: Round-4 revision. ~11,900 words, 11 main sections plus Appendices A-D. Submission draft (not committed by this author; the coordinator commits). Abstract 200 words.
- Built on the `space-and-time-circuits/time-emphasis-paper.md` spine, with the cross-family E20 replication, the Mamba write-vs-retention retest, a full attribution-graph (circuit-tracer) section, the 7B scale test, the blind location test, and the round-2 reviewer experiments integrated.
- Round-1 and round-2 reviews with point-by-point responses (`reviews/round1-response.md`, `reviews/round2-response.md`).
- **Round-3:** scoped §5 to an MLP-transcoder feature-and-error basis with the out-of-basis mechanism stated first and the magnitude-asymmetry and n=12 cautions added; added Vig 2020, Olsson 2022, Feng & Steinhardt 2023, a Meng/Hase delta row, and named the transplant as resample/interchange patching; demoted the window-necessity and Mamba figures to Appendix D, merged the two Gemma feature figures into one, and split the worst long sentences. Custody audit of the P1 experiments **PASSED (FROZEN, byte-identical predictions across versions)**.
- **Round-4 (consistency pass with the companion):** replaced the pre-band-freeze formation leg with the preregistered formation-over-time result (best single layer 0.732/0.804, band attn+MLP freeze 0.904/1.023, consumer-to-subject cut 0.871→0.010 / 0.985→0.015; P1a/P1b/P2c/P3a pass, P2a/P3b/P1c fail), concluding committed-at-the-band, formed-before-it, with the pre-band locus not localized; the positive formed-over-depth evidence is the L11/L12 residual seed (16/16 rescue, 14/14 block, early fact-span 0/15). Replaced the inert k∈{0.5,2} Mamba clock-dose with the aligned retention retest (γ=15–142; release-hurts 0/6, dt-via-write 6/6, writer-specific 1/6, retention-beats-write 4/6 near-tie; verdict RETENTION_NOT_COMMIT_LEVER). Added the 7B block-and-rescue (rescue 0.770, block 0.595, wrong −0.026, commit ~L21) and the blind depth-fraction location test (rule falsified on Pythia-1.4B, dissociation relocated to L13–17 with commit ~L16, OLMo-1B unavailable). Re-scoped the companion pointer to a fixed role lowering rather than a fixed commit-layer index; Fig S2 now carries the retest figure. No `TODO 9B scale` remains; Gemma-2-9B stays unavailable.
- Numbers trace to opened source files (see evidence map). No internal tool names, job IDs, or experiment numbers appear in the body; experiment numbers and job IDs appear only in Appendix A.
- Figures: five in the main body plus two supplementary in Appendix D. Fig 1 (schematic), Fig 2 (dissociation, regenerated with identity-clustered CIs), Fig 3 (formation), Fig 4 (error interchange), Fig 5 (FLUX); Fig S1 (window necessity), Fig S2 (Mamba) in Appendix D.

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
| Window necessity table; best w3 Qwen 0.23, Gemma 0.18; Qwen0.5B L20-21 0.99 (3.2, Table 1, Fig S1) | as stated | `.../full-layer-sweeps/FINDINGS-E19-window-necessity.md` |
| P1-B identity-clustered CIs (Table 2), effective n 14/27/14/13 ids: Qwen block [0.732,1.075]/[0.639,0.860], Gemma [0.740,0.838], SmolLM2 [0.653,0.832]; all rescue/block lower bounds >0 (3.3, 3.4) | as stated | `saturn/experiments/2026-10-02-p1-reviewer-experiments/FINDINGS.md` (part B); `results/B_clustered_stats.json` |
| P1-A formation vs propagation (Qwen + Gemma): Qwen late 0.871, early -0.028, seed-layer -0.010, linear-pred 0.023 (R2 -0.13); Gemma late 0.985, early -0.028, seed-layer 0.080, linear-pred 0.100 (R2 -0.06); pre-band freeze (Qwen 0.675/drop 0.197; Gemma 0.990/drop -0.005, falsifier fired) uninformative, not used (3.5, Fig 3) | as stated | `saturn/experiments/2026-10-02-p1-reviewer-experiments/FINDINGS.md` (part A); `results/A_analysis.json`; `job-802a7371546f`, `job-d37efcecae3e` |
| Formation-over-time (band-internal locus, Qwen+Gemma): best single layer 0.732/0.804; band attn+MLP freeze 0.904/1.023; consumer→subject cut 0.871→0.010, 0.985→0.015; P1a/P1b/P2c/P3a-i/P3a-ii pass, P2a fail (F2), P3b fail (F3b), P1c fail (3.5) | as stated | `saturn/experiments/2026-10-02-formation-over-time/results/FOT_analysis.json`; `job-eaf503028c04`, `job-9acb76a12273` |
| L11/L12 residual seed (positive formed-over-depth): 16/16 rescue, 14/14 block, early fact-span 0/15 (3.5) | as stated | `saturn/experiments/2026-10-01-qwen-scaffold-context-poc/FINDINGS.md` (lines 38, 62) |
| 7B block-and-rescue: rescue 0.770, block 0.595, wrong -0.026 (n=40); commit median L21, all 40 facts L19-27 (3.4, 10) | as stated | `saturn/experiments/2026-10-02-scale-9b-scaffold/PAPER-SECTION.md`; `results/e20_analysis_with_7b.json`; `job-32fa0281137c`, `job-6cbbb78fb7e3` |
| Blind location test: depth-fraction rule falsified on Pythia-1.4B (predicted band block -0.278, rescue 0.136); dissociation relocates L13-17, commit ~L16 (earlier band block 0.97, rescue 1.46); OLMo-1B unavailable (0/108) (10) | as stated | `saturn/experiments/2026-10-02-blind-scaffold-prediction/FINDINGS.md`; `job-2eb34b2106a9` |
| Isolated late write 0.81 at Qwen L23 and Gemma L22 (3.2) | 0.81 / 0.81 | `.../full-layer-sweeps/` (E15/E17); E6 FINDINGS line 53 |
| Read: best single-layer necessity 0.074; L23 restore 1.22; one-hot join 1.02, 88% (4) | as stated | `saturn/experiments/2026-09-30-e13-time-circuit-read-join/FINDINGS.md` |
| Exact-row join = oracle at commit; repetition 1.00 vs semantic 0.00 (4) | as stated | `saturn/experiments/2026-09-30-e18-bucket-join-time-reads/FINDINGS.md` |
| Exact-join rescue within 0.03 of clean in cut induction circuit (4) | 0.03 | `saturn/experiments/2026-09-25-ar-exact-join-admission/FINDINGS.md` |
| circuit-tracer: ~30% error-node influence; largest subject layer L0 (11/12, 8/8); commit band 0.10-0.21 (5) | as stated | `saturn/experiments/2026-09-30-circuit-tracer-head-to-head/FINDINGS.md` lines 44-53 |
| Feature-only interchange: subject-all-layer identity <=0.08, color 0.31-0.42; every-position color 0.32-0.34 (5, Fig 4) | 0.08 / 0.42 / 0.32-0.34 | circuit-tracer FINDINGS lines 118-148 (Amendment) |
| Graph-top features move identity -0.03 to -0.14, color to -0.19 (5) | as stated | circuit-tracer FINDINGS lines 124,136 |
| Native K/V second-half flip 0.83 (identity) / 0.84 (color) on 42/25-row sweep (5, Fig 4) | 0.83 / 0.84 | circuit-tracer FINDINGS lines 142-143 (`job-ed4ce1ac5974`) |
| P1-C matched feature+error interchange: identity 0.31 (flip 3/12), error-only -0.15; color 0.99 (flip 8/8); feature-only repro 0.044/0.313 (5, Fig 4) | as stated | `saturn/experiments/2026-10-02-p1-reviewer-experiments/FINDINGS.md` (part C); `results/C_analysis.json`; `job-5b8f55665345` |
| FLUX four-condition bounds 0.5620 / 0.20743 / 0.91309 / 0.01101 (6.1, Table 3, Fig 5) | as stated | `saturn/experiments/2026-09-30-flux2-joint01-time-accumulation/FINDINGS.md` line 22 |
| FLUX 5-seed necessity; sham also nulls; deletion removes target after dp fix (6.1, 6.2) | interchange->source 5/5; deletion->null 5/5 & 4/5; sham->null 5/5 | `.../2026-09-30-e7-flux-color-multiseed/`; `.../2026-09-30-flux2-residual-deletion/FINDINGS.md` |
| Klein-9B single-step <=0.48 vs all-step 0.90-0.95; 8/9 identity, 7/9 lighting (6.2) | as stated | `saturn/experiments/2026-10-01-e8-klein9b-nine-gate/FINDINGS.md` lines 61,68 |
| SDXL single step <=0.215 vs all 0.985; one step meets removal (6.2) | as stated | `saturn/experiments/2026-10-01-e9-sdxl-four-quadrant/` |
| Mamba writer depths L20/L39/L44 = 0.69-0.83 of depth (7) | as stated | `saturn/experiments/2026-09-30-mamba-full-layer-sweeps/FINDINGS.md` |
| Mamba aligned retention retest (7.1, Fig S2): γ=15-142 to median survival; release-hurts 0/6, dt via write 6/6 via retention 0/6, writer-specific 1/6, retention-beats-write 4/6 (near-tie ≤0.07 nats); survival 0.63-0.90; verdict RETENTION_NOT_COMMIT_LEVER | as stated | `saturn/experiments/2026-10-02-mamba-clock-retest/FINDINGS.md`; `results/summary.json` |
| Pythia-70M induction: triple (relay+2 writers) necessary & sufficient; relay 0.58-0.72 (7.2) | as stated | `saturn/experiments/2026-09-30-e4-pythia-recovered-loss/` |
| E10: swap authors donor 19/32, 30/30; removal wrong 26/32, 3/30 (repairs 6/32, 25/30) (8) | as stated | `saturn/experiments/2026-10-01-e10-completed-answer-rerun/FINDINGS.md` |
| E10 two-step: consumed-step unmount 8/8, early 0/8 (8) | as stated | `saturn/experiments/2026-10-01-e10-cot-intermediate-steps/FINDINGS.md` |
| Computed-object cell (SmolLM2-1.7B, 24 layers): operands <=L7, sum L18-L21, necessity 0.35 at L17 (8) | as stated | `.../full-layer-sweeps/FINDINGS-E11-computed-object.md` |
| Falcon-H1 hybrid attention-dominated, no SSM writer (7) | as stated | `saturn/experiments/2026-10-01-e14-hybrid-attn-ssm/` |

## Figures

Main body:

| File | Source | Note |
|---|---|---|
| `figures/fig1-schematic.png` | generated diagram | source -> formation -> commit -> store -> consumer, with block and transplant |
| `figures/fig2-dissociation.png` | generated from the identity-clustered CIs in `.../2026-10-02-p1-reviewer-experiments/results/B_clustered_stats.json` | hero: cross-family dissociation bars (block/rescue/wrong-identity), identity-clustered 95% intervals |
| `figures/fig3-formation.png` | copied from `.../2026-10-02-p1-reviewer-experiments/figures/figA_formation.png` | P1-A formation vs propagation bars |
| `figures/fig4-error-interchange.png` | copied from `.../2026-10-02-p1-reviewer-experiments/figures/figC_error_interchange.png` | P1-C feature-only / matched feature+error / error-only vs native cut, identity vs color |
| `figures/fig5-flux-quadrants.png` | generated from the four measured bounds in the FLUX findings | FLUX four-condition signature |

Appendix D (supplementary):

| File | Source | Note |
|---|---|---|
| `figures/figS1-window-necessity.png` | copied from `space-and-time-circuits/figures/fig4-window-necessity.png` | E19 window necessity (detail behind Table 1) |
| `figures/figS2-mamba-clock-retest.png` | copied from `.../2026-10-02-mamba-clock-retest/results/clock-retest.png` | aligned retention retest (release vs write lever) at the Mamba writer |

(The orphaned per-layer-profiles figure from the first draft was cut; the schematic replaced it. The standalone feature-only Gemma figure was merged into Fig 4. figB clustered-bars is carried as Table 2, not a figure.)

## Open gaps

RESOLVED in rounds 2-3 (numbers in the body; custody audit of the P1 experiments **PASSED**, FROZEN with byte-identical predictions across versions, the identity-clustered intervals reproduced exactly, a genuine leave-one-identity-out fit, and the error-node reimplementation matching the library):
- **P1-A formation vs propagation (two models)** — in Qwen the late band 0.871 beats seed-layer (-0.010), early band (-0.028), and a linear image of the seed (0.023, held-out R2 -0.13); Gemma replicates the two fitting-free legs (late 0.985 vs seed-layer 0.080, early -0.028; linear-pred 0.100, held-out R2 -0.06). The pre-band subject-layer freeze (Qwen 0.675/drop 0.197; Gemma 0.990/drop -0.005, freeze-no-op falsifier fired) is uninformative and is not used as evidence. The fitting-free legs (not early/seed K/V, not a linear image of the seed) replicate across both models.
- **Formation-over-time (band-internal locus, two models)** — the preregistered test places the late band as the commit and read-out zone: best single layer 0.732/0.804 (P1a, P1b), freezing the band's own attn+MLP leaves rescue intact 0.904/1.023 (P2c), consumer→subject cut collapses rescue 0.871→0.010 / 0.985→0.015 (P3a); the decisive "band builds the store" P2a failed (F2 fired), P3b failed (F3b fired), P1c failed. Reading: committed at the band, formed before it; pre-band locus not localized. Positive formed-over-depth evidence is the L11/L12 residual seed (16/16 rescue, 14/14 block, early fact-span 0/15).
- **P1-B identity-clustered bootstrap** — Table 2 now reports identity-clustered CIs and effective n (14/27/14/13 identities); every block/rescue lower bound stays above zero; under clustering the wrong-identity CI includes 0 in all 4 cells, so candidate top-1 (not the signed fraction) is the content control.
- **P1-C error-node swap** — split by behavior: identity misses even under matched feature+error interchange (0.31, flips 3/12); color recovers (0.99, 8/8). §5 scoped to an MLP-transcoder basis and the formed identity store.
- **7B scale** (§3.4, §10) — the block-and-rescue reproduces at 7B (rescue 0.770, block 0.595, wrong -0.026, n=40; commit ~L21). Block is lower only because the commit spreads across several late layers a six-layer mediator cannot all capture. No positive mediation above 7B; Qwen3-30B's in-forward certificate did not survive the isolated cut.
- **Mamba retention retest** (§7.1) — the aligned retest (γ=15-142) refutes the clock-stop-as-commit reading: release-hurts 0/6, dt-via-write 6/6, writer-specific 1/6, retention-beats-write 4/6 near-tie; verdict RETENTION_NOT_COMMIT_LEVER. The earlier k∈{0.5,2} dose was inert by construction and is dropped.
- **Blind location test** (§10) — the depth-fraction band-location rule is falsified blind on Pythia-1.4B (predicted band carries almost nothing) while the dissociation relocates to L13-17 (commit ~L16); OLMo-1B unavailable. Location-fixedness is a weak symptom, developed in the companion.

Still open:
- **Gemma-2-9B** (sliding-plus-global specimen) is unavailable, so the attention-pattern scale test above 7B is still open.

Owed:
- Sub-layer-grain sweep of a distributed cell (heads, key vs value, positions in the band).
- A second model or behavior for the circuit-tracer head-to-head, to make the instrument-coverage result a trend.
- External-lab / external-harness replication; all results here are one lab, stock eager attention (stock SDPA for the §8 arithmetic cells).
