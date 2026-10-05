# Figures — Dynamic Circuits Loop Through a Stable Time Scaffold

Figures used by the findings-first manuscript (`../paper.md`), with the data file behind each one.
Paths are relative to this directory unless noted; `~/domains`-relative paths point at the primary
record. Figures reused from the earlier `../../scaffolds-and-dynamic-circuits/figures/` drafts are
marked **[reused]**.

## In the paper

| In paper | File | Shows | Data / source |
|---|---|---|---|
| Figure 1 (§1.1) | `fig3_same_patch_query.png` | Query-dependent authority of a byte-identical K/V patch (3.130 / 0.583 / 3.021 nats, 16/16 each) | `~/domains/saturn/experiments/2026-10-01-qwen-scaffold-context-poc/` (report.json) |
| Figure 2 (§1.2) | `fig6_confirmation_results.png` **[reused]** | Frozen 24-coordinate relation reader beats three sealed competitors 8/8 (0.954 vs 0.566); v_proj permutation collapse (0.955→0.049) | `../../scaffolds-and-dynamic-circuits/figures/confirmation-results-data.json`; source `~/domains/saturn/experiments/2026-10-01-scaffold-confirmation/qwen-predictive/FINDINGS.md` |
| Figure 3 (§1.4) | `locator_R_curves.png` | Fit-free locator R_ℓ by layer for 4 known + 2 blind models, with true / locator / depth bands | `~/domains/saturn/experiments/2026-10-02-attention-band-locator/results/` (phaseA + phaseB scorecards) |
| Figure 4 (§1.6) | `fig7_honest_null.png` | Cross-family common-graph null: connected forecast ties addition (MAE 0.015099); role-matcher gap 0.0386 | `~/domains/saturn/experiments/2026-10-01-connected-architecture/qwen/FINDINGS.md`; schematic `../../scaffolds-and-dynamic-circuits/figures/common-role-graph.{svg,pdf}` **[reused]** |

## Data for findings without a dedicated figure

| Finding | Data / source |
|---|---|
| §1.3 fine-tune directional asymmetry (base→coder 0.92; coder→base 0.34; math→base 0.05) | `~/domains/saturn/experiments/2026-10-02-qwen-variant-circuits/FINDINGS.md`; plot data `figures/fig_transplant_matrix.png`, `fig_locator_overlay.png`, `fig_cka_perlayer.png` in that experiment dir |
| §1.4 locator vs tracing (within-2 = 0.5; IoU 0.565 vs 0.402 vs 0.260) | `~/domains/saturn/experiments/2026-10-02-locator-vs-tracing/results/analysis.json` |
| §1.4 causal-band relocation (GPT-2 XL 0.888 vs 0.160; Phi-2 0.485 vs 0.033) | `~/domains/saturn/experiments/2026-10-05-e20-causal-band-phi2-gpt2xl/results/causal_band_curves.png`, `results/analysis.json`; companion Table 2 / Figure 7 |
| §1.5 cross-operation band (0.852 / 0.950 / 1.000; joint rescue 0.925) | `~/domains/saturn/experiments/2026-10-02-break-it-r2/results/breakit-r2-qwen15base-6c46852af315/report.json` |
| §1.6 null nets + function vector (coord 0.012–0.014 vs 0.381; FV 0/14, +2.19 nats) | `~/domains/saturn/experiments/2026-10-02-p2-reviewer-experiments/results/A_analysis.json` |
| §2.1 band-only KV (0.000); routing transfer (gates carry content) | `.../2026-10-02-band-kv-memory/results/`; `.../2026-10-02-routing-transfer/results/routing-transfer-3dfc8e072461/report.json` |
| §3 dispatch gate / orthogonal correction / cache decomposition | §3 records in `../paper.md` Appendix C |

## Reusable figures available from the scaffolds-and-dynamic-circuits drafts

These apply to the companion / appendix material and are available with their data if an appendix
figure is wanted; they are not in the findings-first body:

- `reader-profiles.{svg}` + `reader-profiles-data.json` — per-item reader cosines (within- vs across-operation).
- `retained-and-formed-state-effects.{svg,pdf}` — history×row decomposition (two-update feedback).
- `native-learning-timeline.*`, `native-role-learning-timeline.*`, `native-surface-deltas.*`, `native-learning-state-transfer.*` — continuation-training and developmental trajectory, with their large data JSONs.

## Not in the findings-first body (demoted from the seven-properties rebuild)

`fig1_scaffold_schematic.png`, `fig2_band_location.png`, `fig4_reader_cosine.png`,
`fig5_variance_decomposition.png` (superseded), `fig8_scene_compiler_proof.png` (superseded by
`fig_scene_compiler_flux2.png`), `fig9_qkv_controls_proof.png`, `fig_scene_compiler_flux2.png`,
`fig_k_address_v_payload.png`, `fig_eye_color_timing.png`, `fig_eye_geometry_timing.png`,
`fig_chair_transport.png`, `figA_null_variance_split.png`, `figB_commit_by_layer_typeswap.png`,
`figC_fv_reproduction.png`. These carry the diffusion scene-generator and location-index material now
held by the companion paper and the scaffolds drafts; they remain in this directory for that use.
