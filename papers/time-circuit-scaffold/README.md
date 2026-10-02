# The Commit Layer Does Not Move

Paper 2 of the circuits pair, by Jacob Hollenbeck. The architecture paper.
Companion: Paper 1, [Time-Formed Circuits in Transformers](../time-formed-circuits/paper.md).

- Manuscript: [paper.md](paper.md)
- Figures: [figures/](figures/)
- Reviews and response: [reviews/](reviews/)

## Status

Submission manuscript, 2026-10-02, round-2 revision. Round-1 reviews in `reviews/round1-*`
(response `reviews/round1-response.md`); round-2 reviews in `reviews/round2-*`
(`round2-interp-reviewer.md` 6/10, `round2-evidence-audit.md`, `round2-priorart-clarity.md`);
response in `reviews/round2-response.md`.

Main text about 8,000 words across 13 sections; abstract 219 words; four appendices
(reviewer-control Figures A and B in Appendix D). Twelve figures. All numbers measured on
stock Hugging Face eager execution in float32 unless a line says otherwise; effective n is
stated per claim.

All six experiments have landed:

- Confirm-color (§5): **landed.** A preregistered retest on fresh colors — all three locators
  frozen in advance — holds the color commit input-invariant in both families (Qwen 48 items / 27
  colors: S1 2.84 / S2 1.44 / S3 1.76; Gemma 106 items / 54 colors: S1 3.44 / S2 0.90 / S3 0.97; no
  color cell fires on any locator).
  The Phase-2 Qwen-color firing does not reproduce. Deviations: Qwen covers only 27 colors, short of
  the frozen ≥40 (single-token filter dropped 14, 36 items failed read-back); the Gemma run used a
  post-freeze subject-chunking change, numerics-neutral ~2e-5 nats (custody PASS); freeze is
  file-mtime only. The Gemma identity canary's argmax S1 still fires (4.06) with commit SD 0.00 — the
  anticipated plateau artifact. Source: `.../site-variance-decomposition/FINDINGS-confirm.md`,
  `results/confirm_fal3_analysis.json` (job-8b550b584da4 Qwen, job-b7d05acf8192 Gemma).
- P2-B sliding causality (§3, Figure B): **landed.** The Gemma-2 commit tracks depth, not
  attention type. At our 17-token prompts the sliding-window mask equals the full causal mask, so
  swapping a layer's attention type is an exact no-op (0.0 logit change) while a real window-4
  mask shifts logits by 19.6; the per-layer commit profile is byte-identical under the swap
  (positive L16/18/20/22, non-positive global L17/L21). The alternation is confounded with layer
  parity, not caused by attention type; long-context causality is untested (Gemma-3 unavailable).
  Source: `.../2026-10-02-p2-reviewer-experiments/results/B_analysis.json` (job-0b7652b2112d,
  Gemma-2-2B, 42 identity items, fp32 eager).
- P2-A null (§5, Figure A): **landed.** The read-site split is learned. In random-init and
  weight-shuffled nets the coordinate main effect falls to 1.2–1.4% and the op:fact ratio from
  19.0 to ~1 (v_proj permute keeps 11.9). The reviewer's "coord is trivial" hypothesis failed.
  Caveat: nulls are incompetent (top-1 0/96), so the control shows learned, not scaffold-vs-any-
  competent-net. Source: `.../2026-10-02-p2-reviewer-experiments/FINDINGS-AC-coordinator.md`.
- P2-C function vectors (§4, Figure C): **landed.** An additive Todd-style operation vector at
  L24 gives no top-1 flip (0/14), relation target +2.19 nats, and erases the identity route
  without building the relational one — the operation weighting is NOT_FV. Same source.
- Relational-operation addendum (§5, Table 1): **landed.** Capital-of on 20 countries × 2
  templates (40 facts) separates operation from fact prospectively — within-op per-item cosine 0.74–0.99,
  identity~capital 0.204/0.218, identity~color 0.842/0.911 (read-back ops share a reader);
  FAL-2b (cosine) not triggered, FAL-2a (sum-of-squares) fired for Gemma (0.58 ≥ 0.42),
  reported as frozen. Source: `.../site-variance-decomposition/FINDINGS-addendum-draft.md`
  (jobs job-9693441af910 Qwen, job-756b971f9486 Gemma).

## Honesty corrections made in round 1

- The write-window falsifier (frozen as `sd_argmax_write > 4`, the SD of the per-item argmax
  write layer) **fired in two of six cells**: Qwen color 5.45 and Gemma identity 4.01. The
  earlier "4.17" is a different, post-hoc quantity (the commit-locator SD on the same 22 Qwen
  color items), not the frozen statistic. The frozen argmax locator lands on a noisy early
  write-gain plateau (median argmax layer 0 for Qwen color, 13 for Gemma identity); under a
  post-hoc commit locator the band is input-invariant in five of six cells (Gemma identity SD
  0.00/42 facts; Qwen color the exception at 4.17). The paper states this in abstract, §1, §3,
  §5, §13, and the Fig 5 caption, labels the commit locator as post hoc, and says which locator
  each SD uses. A confirmatory retest freezing all three locators has since run and cleared FAL-3
  on fresh colors (no color cell fires in either family; the argmax locator still trips on the
  Gemma identity plateau, 4.06 with commit SD 0.00, as preregistered), so the invariance no longer
  rests on a post-hoc locator.
- The read-site split (42.2 / 29.0 / 1.1) is a **retrospective re-analysis** of pre-freeze
  data; only the per-fact commit location is prospective and preregistered. The two are now
  kept separate.
- The 42.2% coordinate main effect is not asserted as the scaffold's learned share on faith;
  the text leads with the operation-to-fact-like interaction ratio (~11×), and the untrained
  null (Figure A) has now run and confirms the whole split is learned (coordinate structure
  collapses to ~1% in random/shuffled nets), bounded by the nulls' incompetence (top-1 0/96).

## Abstract

In a trained model the layer where a factual answer commits does not move with the input. Across 42 fresh facts the commit layer (located by the close of the write window, a post-hoc commit locator) lands at Gemma-2-2B layer 22 (SD 0.00) and Qwen2.5-1.5B layer 23 (SD 1.16), and a preregistered retest on fresh colors (48 Qwen, 106 Gemma) holds the color commit input-invariant under all three frozen locators. We call the fixed schedule the time scaffold, and the per-input computation on it a space circuit: the operation re-weights a recurring reader, the fact selects which stored row is read. Byte-identical stored state acquires query-dependent authority (median 3.130 nats, 16/16). A frozen reader profile predicts held relation contexts in all eight; permuting the value-projection rows collapses it. In a re-analysis the operation's weighting carries eleven times the fact-like variance and 84.0% of store necessity; this split is learned, collapsing to ~1% in random or shuffled nets — themselves incompetent (top-1 0/96), bounding the claim to learned, not scaffold-versus-any-competent-net. Of three preregistered falsifiers two held and the third, a write-window locator, fired in two of six earlier cells; the color retest clears all three locators, while the argmax still trips on the identity plateau (Gemma 4.06, commit SD 0.00), as preregistered; the cross-family common graph remains a null. The same organization holds in a state-space and a diffusion model, where attribution tools find the space circuit, not the scaffold.

## Evidence map (claim → source path)

Paths are relative to `~/domains`. "Companion" means the claim is carried by Paper 1 and
cited here, not re-derived.

| § | Claim | Effective n / model | Source |
|---|---|---|---|
| 3 | Gemma-2-2B commit lands at late layers L16–22 (carry 0.58); coincides with sliding-window layers but tracks depth not attention type — type flip is an exact no-op (0.0) at 17-token prompts, commit profile byte-identical; long-context untested (Gemma-3 unavailable) | 8–42 items/cell, single seed; Gemma-2-2B | `saturn/experiments/2026-09-30-full-layer-sweeps/FINDINGS-E17-isolated-kv-writes.md`, `FINDINGS-E19-window-necessity.md` (companion); `saturn/experiments/2026-10-02-p2-reviewer-experiments/results/B_analysis.json` (job-0b7652b2112d) |
| 3 | Commit at ~0.69–0.83 depth across sizes (Mamba 130M L20 / 370M L39 / 2.8B L44) | single seed; Mamba-130M/370M/2.8B | `saturn/experiments/2026-09-30-mamba-full-layer-sweeps/FINDINGS.md` (companion) |
| 3 | Commit is a depth-fixed write port; retention is a correlate | 6 cells × 3 prompts; Mamba | `saturn/experiments/2026-10-02-mamba-writer-clock-dose/FINDINGS.md` (companion) |
| 3 | Formation window closes near commit (Qwen0.5B L21→L22 sharp; Pythia 0.95@L17→0.48@L18→0.01@L22 gradual) | single seed; 4 models | `saturn/experiments/2026-09-30-full-layer-sweeps/FINDINGS-E16-residual-writes.md` (companion) |
| 3,5 | Commit layer input-invariant per fresh fact (Gemma L22 SD 0.00; Qwen L23 SD 1.16) — commit locator (post hoc; preregistered argmax locator fired, see §5); confirmatory fresh-color retest holds under all three locators | 42 identity facts/model | `saturn/experiments/2026-10-02-site-variance-decomposition/FINDINGS.md` |
| 5 | Confirmatory FAL-3 retest (all three locators frozen): fresh colors input-invariant both families (Qwen S1 2.84/S2 1.44/S3 1.76 @48; Gemma S1 3.44/S2 0.90/S3 0.97 @106; none fire). Qwen 27 colors = deviation; Gemma chunking custody PASS; canary argmax 4.06 fires (commit 0.00) | 48 Qwen + 106 Gemma colors | `saturn/experiments/2026-10-02-site-variance-decomposition/FINDINGS-confirm.md`, `results/confirm_fal3_analysis.json` (job-8b550b584da4, job-b7d05acf8192) |
| 4 | Same bytes, different query → query-selective harm 3.130 / 0.583 / 3.021 nats, 16/16 | 16 contrasts/op, 128 pairing checks; Qwen2.5-1.5B | `saturn/experiments/2026-10-01-qwen-scaffold-context-poc/FINDINGS.md` |
| 4 | Operation re-weights a recurring reader (within-op cosine 0.92–0.999; across-op 0.336) | Qwen2.5-1.5B, Gemma-2-2B | `saturn/experiments/2026-10-02-site-variance-decomposition/FINDINGS.md` |
| 4 | Fact moves which row is read (selected-row cosine 0.61–0.70 vs reader 0.95–0.96) | Qwen2.5-1.5B | `saturn/experiments/2026-10-02-site-variance-decomposition/FINDINGS.md` |
| 5 | Read-site variance (RETROSPECTIVE re-analysis): coord×op 29.0% vs fact-like 2.7% (coord×fact 1.1% + coord×binding 1.6%); coord main 42.2% (null ran; learned — see Fig A / row below) | 1,152 cells; Qwen2.5-1.5B | `saturn/experiments/2026-10-02-site-variance-decomposition/results/F2_F3_qwen_predictive_readmap.json` |
| 5 | Store necessity: op 84.0%, fact 3.2%, op×fact 2.0%, residual 10.4% (64 cells) | Qwen2.5-1.5B | `saturn/experiments/2026-10-02-site-variance-decomposition/results/F2_scaffold_poc_store_necessity.json` |
| 5 | Read-site split is LEARNED: coord→1.2–1.4%, op:fact 19.0→~1 in random/shuffled nets; v_proj permute keeps 11.9; nulls incompetent (top-1 0/96) | random-init + shuffled Qwen2.5-1.5B | `saturn/experiments/2026-10-02-p2-reviewer-experiments/FINDINGS-AC-coordinator.md` (job-48af2d6fc73c) |
| 4 | Operation weighting is NOT_FV: additive op vector at L24 gives 0/14 flips, +2.19 nats, erases identity route without building relational one | Qwen2.5-1.5B | `saturn/experiments/2026-10-02-p2-reviewer-experiments/FINDINGS-AC-coordinator.md` (job-5d7cf4e4b3d8) |
| 5 | Three preregistered falsifiers: two held; write-window falsifier fired as frozen (argmax locator) in 2/6 cells — Qwen color 5.45, Gemma identity 4.01; commit-locator SDs 0.00–4.17; confirmatory fresh-color retest cleared FAL-3 under all three locators | Qwen2.5-1.5B, Gemma-2-2B | `.../2026-10-02-site-variance-decomposition/PREREG.md`, `FROZEN.json`, `phase2_sitemap_analysis.json`, `FINDINGS-addendum-draft.md`, `FINDINGS-confirm.md` |
| 6 | Frozen 24-coord profile predicts held relation (raw-RMSE 8/8; cosine 7/8 all-row, 8/8 competent; .954 vs .566) | 8 contexts; Qwen2.5-1.5B | `saturn/experiments/2026-10-01-scaffold-confirmation/qwen-predictive/FINDINGS.md` |
| 6 | Full v_proj row permutation collapses the profile (.955→.049 relation) | 4 contexts; Qwen2.5-1.5B | `saturn/experiments/2026-10-01-scaffold-confirmation/FINDINGS.md` |
| 7 | Mamba shared state, two operations; H-only transfer 12/12; 27-coord profile capital 8/8 | 12 rows; Mamba-130M | `saturn/experiments/2026-10-02-mamba-operation-clock-debugger/FINDINGS.md` |
| 7 | Diffusion static bus / per-prompt program; 21/21 byte-exact; wrong-source/sign 57–97 MAE; early vs late install | 7 specimens, 5 families | `obsidian/blog/2026-09-30-165158-the-scene-generator-survey...md` (21/21, 57–97 MAE line 153), `research/demos/scene-editing.md` |
| 8 | France→Germany two-update feedback (1 of 3 held competent + dev) | 1/3 held; Qwen2.5-1.5B | `saturn/experiments/2026-10-01-scaffold-confirmation/qwen-feedback/FINDINGS.md` |
| 8 | Frozen-reference payload changes B 7/8, preserves A 8/8 | 2 values × 2 orders; Qwen2.5-1.5B | `saturn/experiments/2026-10-01-qwen-frozen-reference-payload/FINDINGS.md` |
| 8 | Source→store mediation (block 0.924, rescue 0.871, 42 rows) | companion; Qwen2.5-1.5B | `saturn/experiments/2026-09-30-full-layer-sweeps/FINDINGS-E20-mediation.md` (Paper 1) |
| 10 | Scene compiler: captured program reproduces native pixels 21/21; wrong-source/sign 57–97 (0–255 scale) vs 0.0 | 7 specimens, 5 families; 3 control prompts | `research/demos/scene-generator.md`, `.../reports/cross-model-replication.json`; blog `2026-09-30-165158` (controls, line 153) |
| 10 | Program not steering vector: XOR 148/150 vs 0/150; hostile XNOR inverts 148/150 | 150 spans; Qwen2.5/Qwen3 | `obsidian/2026-08-17-151407-all-experiments-composite-survey.md` (lines 265–267) |
| 10 | Frozen-site install: right 1.011 vs wrong-site −0.133 vs shuffled −0.607; K/V 0.602 vs −0.153 | 14 held facts (6/14 competent); Qwen2.5-1.5B | `saturn/experiments/2026-10-01-scaffold-dynamic-circuits/ar/results/panel-02e83e9ae183/report.json` |
| 10 | Archive page read: selected 4/4, absent/wrong 0/4 | 2,048-page archive; Qwen | `saturn/experiments/2026-09-24-spectral-virtual-context/FINDINGS.md` |
| 10 | Bit-exact fork/replay + page-out (4/4+4/4 over 32 tok; Mamba 64/64; 0/96 checkpoint reads) | single seed; Qwen/Mamba | blog `2026-09-06-015603`, `saturn/experiments/2026-09-30-source-frame-stack` |
| 9 | Connected forecast ties additive exactly (MAE .015099 vs .014593), wins 1/3 | 3 held; Qwen2.5-1.5B | `saturn/experiments/2026-10-01-connected-architecture/qwen/FINDINGS.md` |
| 9 | Role-matcher ≈ depth null (6.9125 vs 6.9511, gap 0.0386) | opened outcomes | `saturn/experiments/2026-10-01-scaffold-dynamic-circuits/ssm/results/e4-e1-e2-e3-alignment.json`, `ssm/E4_ALIGNMENT.md` |
| 9 | Cross-family core = 2+2+1 rows (RMSE .0928 vs .8526); color reader misses 8/8 | 2 FLUX + 2 Mamba + 1 Qwen | `saturn/experiments/2026-10-01-scaffold-confirmation/FINDINGS.md`, `cross-family/FINDINGS.md` |
| 11 | Attribution graph sees L0, misses commit band (≤0.08 interchange vs 0.83 K/V cut) | companion; 12+8 items, Gemma-2-2B | `saturn/experiments/2026-09-30-circuit-tracer-head-to-head/FINDINGS.md` (Paper 1) |

## Figure sources

| Figure | Content | Source |
|---|---|---|
| fig1_scaffold_schematic.png | Scaffold + space-circuit schematic | authored for this paper |
| fig2_band_location.png | Commit-layer stability per fact | decisive test panel F1 |
| fig3_same_patch_query.png | Same-patch / different-query harm | authored from scaffold-context FINDINGS |
| fig4_reader_cosine.png | Reader cosine within-op vs across-op | decisive test panel F3 |
| fig5_variance_decomposition.png | 3 panels: read-site (F2A), store necessity (F2B), write-formation falsifier (F2C): frozen argmax (S1) and commit (S2) per cell for Phase-2 and the confirmatory retest, threshold at 4 | decisive test panels F2A–F2C |
| fig6_confirmation_results.png | Frozen profile vs competitors + permutation | scaffold-confirmation |
| fig7_honest_null.png | Connected forecast tie + role-matcher null | authored from honest-null numbers |
| fig8_scene_compiler_proof.png | Captured program reproduces native render byte-exact | scene-generator proof sheet |
| fig9_qkv_controls_proof.png | Wrong-program / wrong-sign / shuffled-row controls diverge | scene-generator control sheet |
| figA_null_variance_split.png | Read-site split collapses in random/shuffled nets (learned); in Appendix D | reviewer experiment A (job-48af2d6fc73c) |
| figB_commit_by_layer_typeswap.png | Gemma-2 commit tracks depth not attention type; type flip is a no-op; in Appendix D | reviewer experiment B (job-0b7652b2112d) |
| figC_fv_reproduction.png | Additive operation function vector fails to reproduce the weighting | reviewer experiment C (job-5d7cf4e4b3d8) |

## What is deliberately excluded

The cross-family common role graph is reported as a null (Section 9), not a headline.
Internal tooling names, experiment codes, and job identifiers are confined to Appendix A.
The retired causal-mask-defective feedback instrument is named once in Limitations with
the results it does not touch. The scaffold claim is bounded to the measured models:
two transformers, one state-space model, one diffusion family, single seed. The
constructive systems of Section 10 show the site is fixed and shared across inputs, not
that it is learned (that rests on the Section 6 weight permutation).
