# The Commit Layer Does Not Move

Paper 2 of the circuits pair, by Jacob Hollenbeck. The architecture paper.
Companion: Paper 1, [Time-Formed Circuits in Transformers](../time-formed-circuits/paper.md).

- Manuscript: [paper.md](paper.md)
- Figures: [figures/](figures/)
- Reviews and response: [reviews/](reviews/)

## Status

Submission manuscript, 2026-10-02, round-1 revision after three reviews
(`reviews/round1-interp-reviewer.md` 5/10, `reviews/round1-evidence-audit.md`,
`reviews/round1-priorart-clarity.md`); point-by-point response in
`reviews/round1-response.md`.

Main text about 8,000 words across 13 sections; abstract 220 words; three appendices.
Nine figures. All numbers measured on stock Hugging Face eager execution in float32
unless a line says otherwise; effective n is stated per claim.

Four running experiments are marked by placeholders in the text, to be filled on landing:

- `<!-- TODO confirm-color -->` (§5): preregistered confirmatory re-run of the cells that
  fired the write-window falsifier, with fresh color facts and all three per-fact locators
  (argmax, commit, necessity-argmin) frozen in advance.
- `<!-- TODO P2-A null -->` (§5): untrained / weight-shuffled null for the read-site split,
  the control that would license reading the coordinate main effect as the scaffold's share.
- `<!-- TODO P2-B sliding causality -->` (§3): attention-type switch to break the
  sliding-vs-global parity confound in Gemma-2.
- `<!-- TODO P2-C function vectors -->` (§4): Todd-style operation-vector equivalence test.
- `<!-- TODO addendum: relational op -->` (§5): relational operation on fresh facts that
  separates operation from fact on the read side prospectively.

## Honesty corrections made in round 1

- The write-window falsifier (frozen as `sd_argmax_write > 4`, the SD of the per-item argmax
  write layer) **fired in two of six cells**: Qwen color 5.45 and Gemma identity 4.01. The
  earlier "4.17" is a different, post-hoc quantity (the commit-locator SD on the same 22 Qwen
  color items), not the frozen statistic. The frozen argmax locator lands on a noisy early
  write-gain plateau (median argmax layer 0 for Qwen color, 13 for Gemma identity); under a
  post-hoc commit locator the band is input-invariant in five of six cells (Gemma identity SD
  0.00/42 facts; Qwen color the exception at 4.17). The paper states this in abstract, §1, §3,
  §5, §13, and the Fig 5 caption, labels the commit locator as post hoc, and says which locator
  each SD uses; a confirmatory run freezing all three locators is in progress.
- The read-site split (42.2 / 29.0 / 1.1) is a **retrospective re-analysis** of pre-freeze
  data; only the per-fact commit location is prospective and preregistered. The two are now
  kept separate.
- The 42.2% coordinate main effect is **not** presented as the scaffold's learned share; the
  text leads with the operation-to-fact-like interaction ratio (~11×) and defers the
  main-effect reading to an untrained null.

## Abstract

In a trained model the layer where a factual answer commits does not move with the input:
across 42 fresh facts the commit layer, located by the close of the write window, lands at
Gemma-2-2B layer 22 with standard deviation zero and at Qwen2.5-1.5B layer 23 (SD 1.16). We
call the fixed schedule — seed, formation, commit, store, consumer — the time scaffold, and the
per-input computation on it a space circuit (a locally decisive, per-position operation): the
operation re-weights a recurring reader, the fact selects which stored row is read. In a
re-analysis of the site maps, the operation's weighting carries eleven times the fact-like
variance (coordinate-by-operation 29.0% versus coordinate-by-fact-and-binding 2.7%); store
necessity is 84.0% operation and 3.2% fact. Byte-identical stored state acquires query-dependent
authority (median 3.130 nats, 16/16). A reader profile frozen before evaluation predicts held
relation contexts in all eight; permuting the trained value-projection rows collapses it, so the
scaffold lives in the weights. The same organization holds in a state-space and a diffusion
model; attribution tools find the space circuit, not the scaffold. Two of three preregistered
falsifiers held; the third fired in two of six cells (its frozen locator tracks a noisy
plateau), so the commit-invariance uses a post-hoc locator pending a confirmatory run. The
cross-family
common-graph claim ties a plain additive baseline — a null.

## Evidence map (claim → source path)

Paths are relative to `~/domains`. "Companion" means the claim is carried by Paper 1 and
cited here, not re-derived.

| § | Claim | Effective n / model | Source |
|---|---|---|---|
| 3 | Gemma-2-2B commits on sliding-window layers (L16–22 carry 0.58); parity-confounded, causal test running | 8–42 items/cell, single seed; Gemma-2-2B | `saturn/experiments/2026-09-30-full-layer-sweeps/FINDINGS-E17-isolated-kv-writes.md`, `FINDINGS-E19-window-necessity.md` (companion) |
| 3 | Commit at ~0.69–0.83 depth across sizes (Mamba 130M L20 / 370M L39 / 2.8B L44) | single seed; Mamba-130M/370M/2.8B | `saturn/experiments/2026-09-30-mamba-full-layer-sweeps/FINDINGS.md` (companion) |
| 3 | Commit is a depth-fixed write port; retention is a correlate | 6 cells × 3 prompts; Mamba | `saturn/experiments/2026-10-02-mamba-writer-clock-dose/FINDINGS.md` (companion) |
| 3 | Formation window closes near commit (Qwen0.5B L21→L22 sharp; Pythia 0.95@L17→0.48@L18→0.01@L22 gradual) | single seed; 4 models | `saturn/experiments/2026-09-30-full-layer-sweeps/FINDINGS-E16-residual-writes.md` (companion) |
| 3,5 | Commit layer input-invariant per fresh fact (Gemma L22 SD 0.00; Qwen L23 SD 1.16) — commit locator (post hoc; preregistered argmax locator fired, see §5) | 42 identity facts/model | `saturn/experiments/2026-10-02-site-variance-decomposition/FINDINGS.md` |
| 4 | Same bytes, different query → query-selective harm 3.130 / 0.583 / 3.021 nats, 16/16 | 16 contrasts/op, 128 pairing checks; Qwen2.5-1.5B | `saturn/experiments/2026-10-01-qwen-scaffold-context-poc/FINDINGS.md` |
| 4 | Operation re-weights a recurring reader (within-op cosine 0.92–0.999; across-op 0.336) | Qwen2.5-1.5B, Gemma-2-2B | `saturn/experiments/2026-10-02-site-variance-decomposition/FINDINGS.md` |
| 4 | Fact moves which row is read (selected-row cosine 0.61–0.70 vs reader 0.95–0.96) | Qwen2.5-1.5B | `saturn/experiments/2026-10-02-site-variance-decomposition/FINDINGS.md` |
| 5 | Read-site variance (RETROSPECTIVE re-analysis): coord×op 29.0% vs fact-like 2.7% (coord×fact 1.1% + coord×binding 1.6%); coord main 42.2% (null pending) | 1,152 cells; Qwen2.5-1.5B | `saturn/experiments/2026-10-02-site-variance-decomposition/results/F2_F3_qwen_predictive_readmap.json` |
| 5 | Store necessity: op 84.0%, fact 3.2%, op×fact 2.0%, residual 10.4% (64 cells) | Qwen2.5-1.5B | `saturn/experiments/2026-10-02-site-variance-decomposition/results/F2_scaffold_poc_store_necessity.json` |
| 5 | Three preregistered falsifiers: two held; write-window falsifier fired as frozen (argmax locator) in 2/6 cells — Qwen color 5.45, Gemma identity 4.01; commit-locator SDs 0.00–4.17 | Qwen2.5-1.5B, Gemma-2-2B | `.../2026-10-02-site-variance-decomposition/PREREG.md`, `FROZEN.json`, `phase2_sitemap_analysis.json`, `FINDINGS-addendum-draft.md` (FAL-3 reconciliation) |
| 6 | Frozen 24-coord profile predicts held relation (raw-RMSE 8/8; cosine 7/8 all-row, 8/8 competent; .954 vs .566) | 8 contexts; Qwen2.5-1.5B | `saturn/experiments/2026-10-01-scaffold-confirmation/qwen-predictive/FINDINGS.md` |
| 6 | Full v_proj row permutation collapses the profile (.955→.049 relation) | 4 contexts; Qwen2.5-1.5B | `saturn/experiments/2026-10-01-scaffold-confirmation/FINDINGS.md` |
| 7 | Mamba shared state, two operations; H-only transfer 12/12; 27-coord profile capital 8/8 | 12 rows; Mamba-130M | `saturn/experiments/2026-10-02-mamba-operation-clock-debugger/FINDINGS.md` |
| 7 | Diffusion static bus / per-prompt program; 21/21 byte-exact; wrong-source/sign 57–97 MAE; early vs late install | 7 specimens, 5 families | `obsidian/blog/2026-09-30-165158-the-scene-generator-survey...md` (21/21, 57–97 MAE line 153), `research/demos/scene-editing.md` |
| 8 | France→Germany two-update feedback (1 of 3 held competent + dev) | 1/3 held; Qwen2.5-1.5B | `saturn/experiments/2026-10-01-scaffold-confirmation/qwen-feedback/FINDINGS.md` |
| 8 | Frozen-reference payload changes B 7/8, preserves A 8/8 | 2 values × 2 orders; Qwen2.5-1.5B | `saturn/experiments/2026-10-01-qwen-frozen-reference-payload/FINDINGS.md` |
| 8 | Source→store mediation (block 0.924, rescue 0.871, 42 rows) | companion; Qwen2.5-1.5B | `saturn/experiments/2026-09-30-full-layer-sweeps/FINDINGS-E20-mediation.md` (Paper 1) |
| 10 | Scene compiler: sealed program reproduces native pixels 21/21; wrong-source/sign 57–97 vs 0.0 | 7 specimens, 5 families; 3 control prompts | `research/demos/scene-generator.md`, `.../reports/cross-model-replication.json`; controls blog `2026-09-02-071815` |
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
| fig5_variance_decomposition.png | 3 panels: read-site (F2A), store necessity (F2B), per-fact write-commit SD under the commit locator (F2C; frozen argmax statistic reported in §5, not plotted) | decisive test panels F2A–F2C |
| fig6_confirmation_results.png | Frozen profile vs competitors + permutation | scaffold-confirmation |
| fig7_honest_null.png | Connected forecast tie + role-matcher null | authored from honest-null numbers |
| fig8_scene_compiler_proof.png | Sealed program reproduces native render byte-exact | scene-generator proof sheet |
| fig9_qkv_controls_proof.png | Wrong-program / wrong-sign / shuffled-row controls diverge | scene-generator control sheet |

## What is deliberately excluded

The cross-family common role graph is reported as a null (Section 9), not a headline.
Internal tooling names, experiment codes, and job identifiers are confined to Appendix A.
The retired causal-mask-defective feedback instrument is named once in Limitations with
the results it does not touch. The scaffold claim is bounded to the measured models:
two transformers, one state-space model, one diffusion family, single seed. The
constructive systems of Section 10 show the site is fixed and shared across inputs, not
that it is learned (that rests on the Section 6 weight permutation).
