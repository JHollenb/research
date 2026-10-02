# Round 2 — Evidence audit of time-formed-circuits/paper.md

Auditor: round-2 evidence pass (read-only on paper.md). Date: 2026-10-02.
Scope: every number in abstract, §1, all tables (1-4 + §9 delta), all figure captions
(Fig 1-8) and §3-§6. Each traced to its FINDINGS/report JSON under
`~/domains/saturn/experiments/`. Numbers independently recomputed from raw JSON where
load-bearing. Prior audits (`research/papers/custody-audit-2026-10-02.md`,
`reviews/round1-evidence-audit.md`) cross-checked; blind-final-boss / grail outputs NOT used.
Classes: MATCH / ROUNDING (benign) / MISMATCH / IMPRECISE (number real, operator/scope label off).

Key sources opened: e20-cross-family `results/analysis.json` + FINDINGS; p1-reviewer-experiments
`results/{A_analysis,B_clustered_stats,C_analysis}.json` + FINDINGS; full-layer-sweeps
FINDINGS-{E16,E17,E19,E20-mediation,E11}; e13/e18/ar-exact-join; circuit-tracer FINDINGS
(+Amendment); flux2-joint01 `results/full-report.json`, e7 `results/full-report.json`+FINDINGS,
e8, e9; mamba-writer-clock-dose `results/summary.json`+FINDINGS; mamba-full-layer-sweeps.

## Verification table (claim | paper line | source | status)

| claim (section) | paper | source | status |
|---|---|---|---|
| block 73-92% / rescue 71-99% (abstract, Fig2 L36, §3.4 L131) | L18,36,131 | e20 analysis.json block 0.728-0.924 / rescue 0.713-0.985 | MATCH |
| wrong-content authors wrong answer (abstract) | L18 | e20 analysis.json wrong-donor cand 0.75-1.00 | MATCH |
| identity matched interchange ≤0.31 vs native 0.94 (abstract, §5, Fig6) | L18,179,183 | C_analysis features_plus_error id all-pos 0.3139; E6 native 0.94 | MATCH |
| in-forward L0 0.985 vs isolated 0.009 (§2.2; §9 tbl L267; L273) | L62,267,273 | FINDINGS-E17 "In-forward L0 0.985 (identity); Isolated L0 0.009" | MATCH |
| formation window: Qwen L24 0.57, L27 0.37; SmolLM2 L23 0.07; Pythia-410M L22 0.01 (§3.1) | L76 | FINDINGS-E16 lines 48,51,52 | MATCH |
| Table 1 all 7 cells (single/w3/w80) (§3.2) | L86-92 | FINDINGS-E19 results table | MATCH (all 7) |
| best-3-adj 0.23 (Qwen) / 0.18 (Gemma) (§3.2, §7.2 L248) | L96,248 | E19 Qwen id w3 0.23, Gemma id w3 0.18 | MATCH |
| isolated write 0.81 at Qwen L23 / Gemma L22 (§3.2) | L102 | E17 (Qwen L23 0.81), E6 (Gemma L22 0.81) | MATCH |
| seed enters L12, mediator L22-27 (§3.3) | L108 | analysis.json qwen_pub seed_layer 12, mediator [22..27] | MATCH |
| block 0.924 [0.765,1.030]; rescue 0.871 [0.850,0.894] item-boot (§3.3) | L112 | B_clustered item_bootstrap qwen_pub | MATCH |
| seed gain 1.577-5.555 nats, median 3.515 (§3.3) | L112 | FINDINGS-E20-mediation L78; analysis seed_median 3.5148 | MATCH |
| clustered block [0.732,1.075] / rescue [0.835,0.894] (§3.3) | L114 | B_clustered identity_clustered qwen_pub | MATCH |
| block hi can exceed 1 (§3.3) | L114 | B_clustered qwen_pub clustered block hi 1.0745 | MATCH |
| wrong-id authors own 37/42, retains -0.067; earlier band 0.066 (§3.3) | L116 | E20-mediation (37/42, -0.067); analysis outside_removed 0.0664 | MATCH |
| Table 2 clustered CIs — all 4 cells, block/rescue/wrong (§3.4) | L124-127 | B_clustered identity_clustered_bootstrap (all 4) | MATCH (exact) |
| Table 2 earlier-band 0.066/0.219/-0.008/0.020 (§3.4) | L124-127 | analysis.json outside_band_removed_median | MATCH |
| Table 2 n 14/42, 27/79, 14/42, 13/34 (§3.4) | L124-127 | B_clustered n_ids/n_rows | MATCH |
| held-out: 27 ids from 29 pool, disjoint (§3.4) | L129 | analysis n_adm 79/n_items 87; custody 27 admitted of 29 | MATCH |
| Gemma seed L7 mediator L16-23; SmolLM2 seed L12 mediator L19-22 (§3.4) | L129 | E20 FINDINGS frozen-design table | MATCH |
| all block/rescue clustered lower bounds >0 (§3.4) | L131 | B_clustered (min lo = smollm2 block 0.653) | MATCH |
| **wrong-id interval includes zero in "three of four" cells (§3.4)** | **L131** | **B_clustered: ALL 4 clustered wrong intervals include 0 (Table 2 confirms)** | **MISMATCH (should be four)** |
| wrong-donor top-1 0.75-1.00, target ≤0.06 (§3.4) | L131 | analysis top1 (0.7468-1.0; target max 0.0588) | MATCH (round) |
| Gemma block 0.768 = 0.76 necessity (§3.4) | L131 | E19 Gemma L16-23 0.76 | MATCH |
| held-out rescue cand 81% / full-vocab 39%; seed gain 6.05 vs 3.5 (§3.4) | L133 | analysis qwen_ho (0.8101/0.3924; 6.0485/3.5148) | MATCH |
| earlier band removes 0.219 held-out (§3.4) | L133 | analysis qwen_ho outside_removed 0.2188 | MATCH |
| split/reinstall ≤1e-4 or exact; verifier 6/6 gates (§3.4; AppB 8.6e-5) | L135 | E20 FINDINGS "≤8.6e-5 ... exactly 0 ... 6/6 gates" | MATCH |
| P1-A late 0.871, seed-layer -0.010, early -0.028, linear 0.023 (R2 -0.13), freeze 0.675, drop 0.197, frozen-seed 0.994, late-early 0.90 (§3.5, Fig4) | L145,149 | A_analysis.json arms + deltas (0.8713/-0.0101/-0.0279/0.0227/-0.1262/0.6747/0.1967/0.9944/0.8992) | MATCH |
| best read necessity 0.074; L23 restore 1.22; one-hot 1.02, 88% (§4) | L157 | FINDINGS-E13 L38 (0.074/1.22), L52 (1.02/0.88) | MATCH |
| standardized bucket = oracle at commit (§4) | L159 | FINDINGS-E18 L63,92 bucket_subjref==oracle | MATCH |
| exact-join rescue within 0.03 of clean, forced-choice (§4) | L159 | ar-exact-join (gap ≤0.005 forced-choice; caveats) | MATCH (conservative) |
| predecessor query: repetition 1.00, semantic/color 0.00 (§4) | L161 | E12 induction 1.00; E18 query-bucket 0.00 (id/color) | MATCH (two records) |
| ~30% error nodes; ≤0.18-0.28/layer; L0 largest 11/12, 8/8; commit band 0.10-0.21 (§5) | L167 | circuit-tracer FINDINGS attribution tbl | MATCH |
| feat-only subj-all-layers: id ≤0.08, color 0.31-0.42; all-pos id ≤0.08, color 0.32-0.34 (§5) | L169 | E6 Amendment (color subj-all 0.42/0.31; all-pos 0.32/0.34) | MATCH |
| graph-top features move id -0.03 to -0.14, color up to -0.19 (§5) | L169 | E6 Amendment (id -0.03..-0.14; color -0.19) | MATCH (round-1 fix landed) |
| native 2nd-half flip 0.83/0.84, whole 0.93/1.00, single 0.08/0.15 (§5, Fig5) | L171,175 | E6 ref tbl (job-ed4ce1ac5974) | MATCH |
| feature-only repro: id 0.044 vs 0.049; color 0.313 vs 0.344 (§5) | L177 | C_analysis features_only vs library_features_only | MATCH |
| matched f+e id median "0.31 over subject+all-later positions", flip 3/12, error-only -0.15 (§5) | L179 | C_analysis: subj_and_later=0.294; all-pos=0.314; flip 0.25; error-only -0.149 | IMPRECISE (0.31 is all-pos; subj+later=0.29) |
| matched f+e color 0.36→0.99, flip 8/8 (§5, Fig6) | L179,183 | C_analysis color all-pos feat-only 0.359 / f+e 0.990 / flip 1.0 | MATCH |
| Fig5 caption "all-layer all-position ... color 0.42" | L175 | E6: all-pos color = 0.32-0.34; 0.42 is subj-all-layers (frozen) | IMPRECISE (label vs value) |
| FLUX bounds 0.5620/0.20743/0.91309/0.01101 (§6.1, T3, Fig7) | L198-200,206 | flux2-joint01 full-report.json (0.562/0.20743/0.91309/0.01101) | MATCH |
| 15 cells = 3 setups x 5 site sets, 3 baselines (§6.1) | L195 | E1b design (3x5) | MATCH |
| 5-seed: interchange→source 5/5 both; deletion→null 5/5 & 4/5; sham 5/5 (§6.1) | L208 | e7 full-report/FINDINGS B1-B3 (route 5/5/5, resid 5/5/4) | MATCH |
| Klein-9B single ≤0.48 vs 0.90-0.95; 8/9 id, 7/9 light; one-step source on one seed (§6.2) | L214 | E8 FINDINGS verdict | MATCH |
| SDXL single ≤0.215 vs 0.985; one step meets removal (§6.2) | L214 | E9 FINDINGS four-quadrant tbl | MATCH |
| FLUX whole-path 0.913 vs single 0.562 vs 0.90 line (§6.3) | L220 | flux2-joint01 (same bounds) | MATCH |
| Table 4 Qwen/Gemma write port 0.81 @ L23/L22 (§7) | L228 | E17/E6 | MATCH |
| Table 4 Mamba writer 0.69-0.83 depth, L20/L39/L44 (§7) | L230 | mamba-full-layer-sweeps (0.833/0.813/0.688) | MATCH |
| Fig8/§7.1 write 0.02-1.37 vs clock 0.01-0.40 vs joint 0.02-1.87; write>clock 6/6; clock-release positive 2/6; neighbor L40 0.36 vs writer L44 0.04 (§7.1, Fig8) | L240,244 | mamba summary.json + FINDINGS (2/6 corrected) | MATCH (3/6→2/6 fix landed) |

## Round-1 / custody required-fixes: CONFIRMED LANDED

- App A E11 model Qwen→**SmolLM2-1.7B (24L)** (L327). FIXED.
- §5 graph-top identity range now **-0.03 to -0.14** (color -0.19) (L169). FIXED.
- Eager-attention overclaim split: store/mediation/read eager, §8 arithmetic **stock SDPA** (L289, L347). FIXED.
- §4 exact-join **forced-choice** qualifier added (L159). FIXED.
- §7.2 "per layer" reworded to "no three adjacent layers above 0.23" (L248). FIXED.
- §5 color 0.31-0.42 (subj-pos) vs 0.32-0.34 (all-pos) body attribution corrected (L169). FIXED.
- §8 two-step "about 0.04 and 0.02 nats" (L254). FIXED.
- Mamba clock-release **"two of the six cells"** (L240). FIXED (custody discrepancy #1 resolved).

## Provenance / contamination checks

- All E20 cells from FINAL succeeded full jobs (fab52bcf3cce / a66b102614e3 / c128e07da015 / e1f652e80f43); killed_vram `66931f253d0c` and killed_ram `0efc7bef9d07`/`64761294e4b3` carry NO report.json and contribute nothing. Smokes are smoke=True n=3, excluded.
- P1 jobs: A `802a7371546f` (only non-smoke full), C `5b8f55665345` (only non-smoke), B = no-GPU reanalysis of the correct pre-existing reports. Custody-audit P1 section = PASS; B clustered CIs reproduced exactly, A LOO genuine, C reimpl≡library.
- No smoke/killed/cancelled number reached the body. No wrong denominators found (each arm normalized by its own per-row seed gain `g_i`, documented in App B).

## Carryover (not a §3-6 number, still open)

- Reference **[Geiger 2023] arXiv:2301.04709** (§9) still unverified independently (round-1 fix #4). Not a numeric claim.
- App A L301 / README hedge "P1 custody audit in progress, numbers may be revised" is now stale: the P1 custody section is complete (PASS). Optional: firm up the hedge.
