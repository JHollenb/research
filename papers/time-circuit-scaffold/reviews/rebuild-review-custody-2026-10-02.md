# Adversarial custody audit — `time-circuit-scaffold/paper.md`

**Date:** 2026-10-02. **Target:** `research/papers/time-circuit-scaffold/paper.md` (commit 4214b0c).
**Method:** every number in the abstract, in each section's first paragraph, and in every figure
caption was traced to the cited primary (FINDINGS.md / results JSON / report.json under
`~/domains/saturn/experiments`, `~/domains/research/demos`, `~/domains/research/papers`); 50+
further body numbers sampled. No models were run; verification is by `rg`/`sed`/`python` reads of
primary records. Paper not edited. All source paths below are relative to `~/domains`.

**Headline:** The large majority of quantitative claims reproduce exactly against their primaries
(E20 mediation + cross-family, the Qwen context/reader PoC, the reader cosines, the diffusion
factorials and closure, the Mamba clock-retest, the 7B scale cell, the VM/scene-compiler counts).
**Three must-fix custody defects were found:** (1) the FLUX.2 scene-compiler control MAE ranges in
Figure 1 / §9.1 / Appendix A do not match the only FLUX.2 primary; (2) the §5 "pre-band freeze
0.675" sentence is sourced to a file that does not contain it and rests on a leg the paper's own
§13 and the formation-over-time prereg call *uninformative* (and whose prereg prediction failed);
(3) Appendix A row 316 names the wrong transformer model (Qwen2.5-Coder-1.5B) for a result whose
primaries are Qwen2.5-0.5B. All 14 referenced figure files exist.

---

## Verification table

Legend: OK = traces exactly (within rounding); MISMATCH = value/condition disagrees with primary;
UNSOURCED = not found in cited primary (or cited primary lacks it); STALE = drawn from a
draft/superseded leg when a promoted/corrected result exists.

| Claim | Paper line | Paper value | Primary value | Source path:line | Verdict |
|---|---|---|---|---|---|
| FLUX spine same-vs-diff organization | abs / §3 L82 | 0.913 vs 0.734; seam 8/9 | 0.9132 / 0.7344; 8/9 | saturn/experiments/2026-08-26-flux-rosetta-format-ontology-recurrence/FINDINGS.md:49-51,67 | OK |
| Eye color/geometry head & row reuse | §2 L48 / §3 L84 | 5–7 of top 8 heads; 10–15 of 64 rows | "five to seven of the same top eight heads … overlapped only 10–15 rows" | research/demos/artifacts/scene-editing/sources/2026-08-28-094822-the-final-image-had-two-parents.md:93 | OK (value); path imprecise — App A cites scene-editing.md, number is in a sources subfile |
| Qwen L22–27 interface serves 3 ops | §3 L86 | color 16/16, position 12/16, identity 11/11 | 16/16, 12/16, 11/11 | saturn/experiments/2026-10-01-qwen-scaffold-context-poc/FINDINGS.md:30-33 | OK |
| Mamba store depth across sizes | §3 L88 | L20/L39/L44, rel depth 0.69–0.83 | L20/L39/L44; "~0.69-0.83 fractional depth" | saturn/experiments/2026-09-30-mamba-full-layer-sweeps/FINDINGS.md:16-23 | OK |
| Falcon-H1 hybrid lowering | §3 L88 | attn −1.774 (17/22), 0.987; color −2.289; SSM −0.038 (2/22) | −1.774, 17/22, 0.987; −2.289; −0.038, 2/22 | saturn/experiments/2026-10-01-e14-hybrid-attn-ssm/FINDINGS.md:23-26 | OK |
| Byte-identical state, query-selective harm | abs / §4 L96 / Fig2 L98 | 3.130 / 0.583 / 3.021 nats; 16/16; 128 checks | 3.130 / 0.583 / 3.021; 16/16; 128 | saturn/experiments/2026-10-01-qwen-scaffold-context-poc/FINDINGS.md:52-54,42 | OK |
| Per-item reader cosine within/across op | abs / §4 L102 / Fig3 L104 | within 0.74–0.99 (Qwen .749/.735/.988; Gemma .895/.865/.807); id~cap .204/.218; id~col .842/.911 | identical (corrected coordinator note) | saturn/experiments/2026-10-02-site-variance-decomposition/FINDINGS-addendum-draft.md (coordinator note, top) | OK — but cited file is a **draft**; promoted FINDINGS.md defers to it; values are the custody-corrected ones |
| Head/edge value routes & cosines | §4 L106 | L23/KV0/V, L22/KV1/V; 0.947/0.927/0.961; cross-op 0.336; attn mass 0.61–0.70; reader 0.93–0.96 | 0.947/0.927/0.961; 0.336; 0.631/0.611/0.702; 0.93–0.96 | saturn/experiments/2026-10-01-qwen-head-edge-topology/FINDINGS.md:14-15,78-80,88,113 | OK |
| Key×value factorial + interaction | §4 L108 | 0.72139 / 0.66201 / 0.71808 / 1.00000; interaction 0.3413 | identical; ≈0.34130 | research/demos/docs/scene-generator-paper.md:221-224,232 | OK |
| Joint-permutation factorial | §4 L110 / Fig4 L114 | 0.859; k-only 0.436; v-only 0.627; wrong-k 0.358; wrong-v 0.413; compiled 1.000 | 0.8593; 0.4360; 0.6269; 0.3580; 0.4130 | research/demos/artifacts/scene-generator/artifacts/reports/binding.json (alpha_base_to_candidate) | OK |
| Live query drift | §4 L112 | K/V byte-identical; live Q cosine 0.9999→0.8399 | (per App A row 283) | research/demos/docs/scene-generator-paper.md | OK (not independently recomputed; stated in cited paper) |
| **FLUX.2 scene-compiler controls** | **Fig1 L38 / §9.1 L186 / App A 311** | **wrong-source 57–88; wrong-sign 64–97; row-perm 7–11; MAE 0.0** | **wrong-source 54.5/94.0/94.3; wrong-sign 60.0/79.5/89.3; perm 4.6/7.9/22.8** | research/demos/artifacts/scene-generator/artifacts/reports/flux2-klein.json (rows[0-2]) | **MISMATCH** |
| E20 source→store (published Qwen) | §5 L122 | block 0.924 / rescue 0.871 / wrong 37/42 | 0.924189 / 0.871323; wrong 37/42 | saturn/experiments/2026-10-02-scale-9b-scaffold/results/e20_analysis_with_7b.json; 2026-09-30-full-layer-sweeps/FINDINGS-E20-mediation.md:48,61 | OK |
| E20 cross-family (3 fam / 4 cells) | abs / §5 L122 | held-Qwen 0.728/0.713 n79; Gemma 0.768/0.985 n42; SmolLM2 0.740/0.910 n34; rescue 0.71–0.99 | identical | saturn/experiments/2026-10-02-e20-cross-family/FINDINGS.md (headline table) | OK |
| 7B scale cell | abs / §5 L122 / App A 287 | rescue 0.770 / block 0.595 / wrong −0.026 n40; commit L21, 100% L19–27 | 0.7703 / 0.5948 / −0.0261 n40; median L21 (0.78), 100% L19–27 | saturn/experiments/2026-10-02-scale-9b-scaffold/results/e20_analysis_with_7b.json; PAPER-SECTION.md:14-15,30,36-37 | OK |
| Recipient formation | §5 L124 | seed→state rescue 16/16; block 14/14; early-band 0/15; write port ~81%; no layer >~8% | 16/16; 14/14; 0/15; write 0.81 | saturn/experiments/2026-10-01-qwen-scaffold-context-poc/FINDINGS.md:62,38; 2026-09-30-full-layer-sweeps/FINDINGS-E20-mediation.md:143 | OK |
| Band-internal: single layer | §5 L126 | best single 0.732 (Qwen) / 0.804 (Gemma) | single_max 0.7325 / 0.8038 | saturn/experiments/2026-10-02-formation-over-time/results/FOT_analysis.json | OK |
| Band-internal: freeze band attn+MLP | §5 L126 | 0.904 (Qwen) / 1.023 (Gemma) | 0.9044 / 1.0226 | FOT_analysis.json (test2_bandfreeze last) | OK |
| Band-internal: cut consumer→subject | §5 L126 | 0.871→0.010 (Qwen), 0.985→0.015 (Gemma) | 0.8713→0.009766; 0.9849→0.014881 | FOT_analysis.json (test3) | OK |
| **"pre-band freeze 13–21 cuts Qwen 0.871→0.675"** | **§5 L126 / App A 290** | **0.675, attributed to FOT_analysis.json + PREREG.md** | **FOT_analysis.json has no such stat (its reads-earlier arm = 0.810, which FIRED falsifier F3b = cross-position construction UNSUPPORTED). 0.675 = OLD p1-reviewer `rescue_late_freeze_mid`** | saturn/experiments/2026-10-02-p1-reviewer-experiments/FINDINGS.md:69,94-100; FOT PREREG.md:22-24; FOT results/FOT_analysis.json (test3 P3b false) | **STALE + UNSOURCED** |
| Eye-color install timing | §5 L128 / Fig5 L130 | early 0.5772 (blue) / late 0.0689 (violet); final-call 0.0289, MAE 5.21; 56 imgs, 12 refs | 0.5772 / 0.0689; 0.0289 / 5.2129; 56 imgs, 12 refs exact | research/demos/scene-editing.md:167,196,15,23 | OK |
| First-call vs late-call source lesion | §5 L128 / §12 L228 | 20.82 vs 2.15 MAE | restore_single_10_early mad_vs_recipient = 20.827; **2.15 not located** | research/demos/artifacts/scene-editing/artifacts/historical/camera-distance/analysis/flux-rosetta-adult-anime-camera-distance-summary.json:255 | 20.82 OK; **2.15 UNSOURCED** (nearest late-call restore arms are 4.40/9.33) |
| Temporal closure | §5 L134 | program 0.712 / register 0.403 / both exact | target_pre_only rgb_eye 0.7124; target_register_only 0.4035; both 1.0 exact | research/demos/artifacts/scene-editing/artifacts/closure/temporal-closure-summary.json | OK |
| Conjunction dose response (App A) | App A 284 | −0.2203 / 0 / 0.5315 / 1 / 1.1382; roll −0.0089 | −0.2203 / 0.0 / 0.5315 / 1.0 / 1.1382; −0.008948 | research/demos/artifacts/scene-editing/artifacts/closure/interaction-residual-causal-summary.json | OK |
| Mamba source→writer joined | §5 L140 | donkey +4.59 / Vienna +7.65; restore removes 90.3% / 91.6% | +4.5906 / +7.6479; 90.3% / 91.6% | saturn/experiments/2026-10-01-connected-architecture/mamba/FINDINGS.md:51-52,17 | OK |
| FLUX four-quadrant subtype | §5 L142 / App A 297 | single-step ≤0.56, all-step ≥0.91; 15 cells; additive passes | max 0.28/0.56 vs ≥0.91; additive passes | saturn/experiments/2026-09-30-flux2-joint01-time-accumulation/FINDINGS.md:31-32 | OK (0.56/0.91/additive); "15 setup-by-site" count not located in FINDINGS |
| Two-update feedback | §6 L148 | France→Germany; block→function word; 1 of 3 held | Paris→France; Germany swap; zero→`is`; 1 clean of 3 | saturn/experiments/2026-10-01-scaffold-confirmation/qwen-feedback/FINDINGS.md:14-27 | OK |
| History×row decomposition | §6 L152 | history +1.279..+1.576; total +0.957..+1.425; fit 0.0995 vs 2.7024 vs 1.2574 | +1.279/+1.576; +0.957/+1.425; 0.0995 / 2.7024 / 1.2574 | saturn/experiments/2026-10-01-scaffold-graph-identification/FINDINGS.md:31-34,69 | OK |
| Mamba dog→cat conv split | §6 L154 | +2.74 selected; +2.79 conv-only; −0.04 recurrent-only | +2.7436; +2.7947; −0.0411 | saturn/experiments/2026-10-01-scaffold-graph-identification/mamba-cpu/FINDINGS.md:9,24-27 | OK |
| Frozen relational reader (held) | §7 L160 / Fig8 L162 | mapped 0.954 vs 0.566; RMSE 0.029 vs 0.149; 7/8 all-row, 8/8 competent; color 5/8 | 0.954/0.566; 0.029/0.149 (competent); 7/8, 8/8; color 5/8 | saturn/experiments/2026-10-01-scaffold-confirmation/qwen-predictive/FINDINGS.md:17-18,15-25,30 | OK |
| SSM frozen reader (held) | §7 L164 | capital 0.9941 vs 0.9880 (8/8); delayed-id 0.9586 vs 0.9102 (4/4); 12 rows | .9941/.9880 (8); .9586/.9102 (4); 12/12 | saturn/experiments/2026-10-02-mamba-operation-clock-debugger/FINDINGS.md:63-64,34-35 | OK |
| Cross-family core edge | §7 L166 | RMSE 0.0928 vs 0.8526; FLUX partial rescue | 0.0928 / 0.8526; FLUX coherent 0.1927 | saturn/experiments/2026-10-01-scaffold-confirmation/cross-family/FINDINGS.md:50-51,58 | OK |
| Weight-disorder collapse | §8 L172 / Fig8 L162 | rel 0.955→0.049; col 0.838→0.110; id 0.931→0.569 | 0.955→0.049; 0.838→0.110; 0.931→0.569 | saturn/experiments/2026-10-01-scaffold-confirmation/qwen-predictive/FINDINGS.md:36,38 | OK |
| Null nets dead; relation survives | §8 L174 / FigD2 L356 | top-1 0/96 both; trained +0.512, random +0.350 | random 0/96, shuffle 0/96; 0.5117 / 0.3499 | saturn/experiments/2026-10-02-p2-reviewer-experiments/results/A_analysis.json | OK |
| Continuation training | §8 L176 | writer +0.445 vs matched ~0; Mamba wrong-label +0.448 | +0.4451 / −0.0039; +0.4477 | saturn/experiments/2026-10-02-native-role-learning-timeline/FINDINGS.md:45-48 | OK |
| Scene compiler 21/21 | abs / §9.1 L186 | 21/21 exact; 7 specimens, 5 families; MAE 0.0 | exact_rows 21, specimen 7, family 5, all MAE 0.0 | research/demos/artifacts/scene-generator/artifacts/reports/cross-model-replication.json | OK (see note: "SDXL twice" = 3 SDXL-family specimens) |
| SDXL wrong-sign control | §9.1 L186 / Fig9 L188 | 94.29 | 94.2905 | research/demos/scene-generator.md:55 | OK |
| Cache speedup | §9.1 L190 / App A 312 | 33.895 → 28.407 s, RGB exact | median cached 28.407; baseline 33.90 via ratio 1.1932; all RGB exact | research/demos/artifacts/scene-generator/artifacts/reports/cache-benchmark.json | OK |
| VM frozen-site writes | §9.2 L194 | right 1.011 / wrong-site −0.133 / shuffle −0.607 (14 held) | residual_write correct 1.0112 / wrong_site −0.133 / shuffle −0.607 (identity held) | saturn/experiments/2026-10-01-scaffold-dynamic-circuits/ar/results/panel-02e83e9ae183/report.json | OK |
| Archive page read | §9.2 L194 | selected 4/4; absent/wrong 0/4; 2,048 pages | 4/4; 0/4; 2,048 | saturn/experiments/2026-09-24-spectral-virtual-context/FINDINGS.md:7,21-23 | OK |
| Externalize/resume + serving | §9.2 L194 / App A 316 | 32-tok bit-for-bit; Mamba 64/64; 0/96 checkpoint reads; **model Qwen2.5-Coder-1.5B** | 96/96 rows exact, Qwen2.5-**0.5B**; serving assay Qwen2.5-0.5B-Instruct | saturn/experiments/2026-09-30-source-frame-stack/FINDINGS.md:15,28; saturn/docs/CAUSAL-CONTEXT-VM.md:4,35 | **MISMATCH (wrong model in App A 316)**; "0/96 checkpoint reads" exact count not located |
| XNOR program-not-vector | §9.2 L196 | XOR 148/150 vs 0/150; XNOR inverts 148/150 | 148/150; 0/150; XNOR 148/150 | obsidian/2026-08-17-151407-all-experiments-composite-survey.md:57,265-266 | OK (primary is an obsidian survey, outside the 3 named primary roots) |
| Ancestry changes meaning | §9.2 L198 | joint 6/6 vs independent 1/6 | 6/6 vs 1/6 | saturn/experiments/2026-09-25-book-index-two-source-coherence/FINDINGS.md:31 | OK |
| Cross-family connected null | §10 L204 / Fig10 L206 | MAE 0.015099 vs 0.014593 vs 0.014588; ties additive; 1/3; matcher 6.9125 vs 6.9511, gap 0.0386 | 0.015099384; 1/3; additive identical; 6.9125/6.9511/0.0386 | saturn/experiments/2026-10-01-connected-architecture/qwen/DRAFT_INTEGRATION.md:155 + FINDINGS.md:46; research/papers/scaffolds-and-dynamic-circuits/architectural-paper.md:433 | OK — 0.015099 cited via a **draft** (FINDINGS.md corroborates 1/3 + additive-tie); 0.014593/0.014588 competitor values not located |
| Mamba clock-retest verdict | §10 L210 / App A 296 | γ 15–142; release hurts 0/6; dt via write 6/6, retention 0/6; writer-specific 1/6; survival 0.66–0.90 | γ 15–142; P1 0/6; P4 0/6; P3 1/6; verdict RETENTION_NOT_COMMIT_LEVER | saturn/experiments/2026-10-02-mamba-clock-retest/results/summary.json; FINDINGS.md | OK — survival "0.66–0.90" matches FINDINGS but raw writer_surv dips to 0.631 (130M counting) in summary.json |
| Commit-location invariance | §13 L249 / FigD1 L354 | Gemma L22 SD0.00; Qwen L23 SD1.16; capital L22 SD0.00 (post-hoc locator); 7B L21 SD2.30 | 0.00 / 1.16 / 0.00 (write-commit locator); 7B SD 2.30 | 2026-10-02-site-variance-decomposition/FINDINGS-addendum-draft.md; 2026-10-02-scale-9b-scaffold/PAPER-SECTION.md:37 | OK (paper correctly labels these the post-hoc locator) |
| FAL-3 fired 2 of 6 | §13 L251 | Qwen color 5.45, Gemma identity 4.01 | 5.45, 4.01 | 2026-10-02-site-variance-decomposition/FINDINGS-addendum-draft.md (top) | OK |
| Fresh-color retest | §13 L251 | Qwen 48 items/27 colors S1 2.84/S2 1.44/S3 1.76; Gemma 106/54 3.44/0.90/0.97; canary 4.06; 27<40 deviation | 48 items/27 colors; 106/54; frozen-short deviation | 2026-10-02-site-variance-decomposition/FINDINGS-confirm.md (header corrections) | OK (counts confirmed; S1/S2/S3 per-cell not independently recomputed) |
| Variance ratio | §13 L253 | op:fact 2.65 (Qwen) / 0.72 (Gemma); SS falsifier fired for Gemma | 2.65 / 0.72; FAL-2a fired Gemma | 2026-10-02-site-variance-decomposition/FINDINGS-addendum-draft.md (Phase 3 result) | OK |
| Sliding-window type swap | §13 L255 / FigD3 L358 | 0.0 vs 19.6 | 0.0; 19.624 | saturn/experiments/2026-10-02-p2-reviewer-experiments/results/B_analysis.json:18,62 | OK |
| Additive function-vector | §13 L255 / FigD4 L360 | 0/14 flips; +2.19 nats | 0/14; +2.19 | saturn/experiments/2026-10-02-p2-reviewer-experiments/FINDINGS-AC-coordinator.md:36 | OK |

---

## Must-fix items

### 1. FLUX.2 scene-compiler control MAEs are not supported by any primary (MISMATCH)
- **Where:** Figure 1 caption (L38, "MAE 7–11 against 57–97"), §9.1 (L186, "57 to 88 for a wrong
  source, 64 to 97 for a wrong sign, 7 to 11 for a row permutation"), Figure 9 caption (L188,
  "57–97"), Appendix A row 311 ("wrong-source 57–88, wrong-sign 64–97, perm 7–11").
- **Primary:** the only FLUX.2 scene-compiler record,
  `research/demos/artifacts/scene-generator/artifacts/reports/flux2-klein.json` (3 rows), gives
  **wrong-source 54.54 / 94.00 / 94.34** (range 54.5–94.3, not 57–88), **wrong-sign 59.98 / 79.53 /
  89.28** (60.0–89.3, not 64–97), **row-permutation 4.57 / 7.93 / 22.80** (4.6–22.8, not 7–11),
  compiled 0.0.
- The sources Appendix A cites for this row (`cross-model-replication.json`,
  `scene-generator-paper.md`) contain **no FLUX.2 controls at all** — `cross-model-replication.json`
  has only the 21 exact rows (all MAE 0.0). No single flux2-klein row reconciles the paper's
  triple.
- **Impact:** load-bearing. The row-permutation claim ("MAE 7–11", "near-invariant", key = address,
  row = basis coordinate) omits a prompt whose permutation MAE is **22.8**, and understates the
  low end (4.6). Fix the three ranges to the measured values (perm 4.6–22.8, wrong-source
  54.5–94.3, wrong-sign 60.0–89.3) or cite the actual FLUX.2 primary the figure was built from if a
  newer one exists (`fig_scene_compiler_flux2.png` was regenerated 08:56, later than the rest — if
  it used an unsaved run, commit that report).

### 2. §5 "pre-band freeze 13–21 cuts Qwen rescue 0.871→0.675" is mis-sourced, superseded, and internally contradicted (STALE + UNSOURCED)
- **Where:** §5 (L126, presented as positive evidence that "the content is built over the preceding
  depth, family-dependently"); Appendix A row 290 lists "pre-band freeze 0.675" with source
  `2026-10-02-formation-over-time/results/FOT_analysis.json` + `PREREG.md`.
- **Primary problem:** `FOT_analysis.json` contains **no pre-band-freeze statistic**. Its
  closest field (`rescue_form_block_subject_reads_earlier` = **0.810** for Qwen) *failed* its
  preregistered prediction P3b (≤ full−0.30) and *fired* falsifier F3b — i.e. the primary says the
  cross-position construction route is **UNSUPPORTED** for Qwen. The value 0.675 is only a single
  row's `prog_prefix_k5` there (median = 0.779).
- **Actual origin of 0.675:** the **old** p1-reviewer leg,
  `saturn/experiments/2026-10-02-p1-reviewer-experiments/FINDINGS.md:69` (`rescue_late_freeze_mid
  (freeze attn+MLP L13-21) = 0.675 [0.611,0.713]`). That leg's preregistered prediction P_A4 (drop
  ≥ 0.20) **FAILED in both models** (Qwen drop 0.197; Gemma `F_A4_freeze_noop` fired, 0.990 vs
  0.985 — see FINDINGS.md header note).
- **Internal contradiction:** the formation-over-time `PREREG.md:22-24` was written specifically
  because the validity audit found this pre-band freeze leg **UNINFORMATIVE** ("by construction it
  cannot see formation inside the band or across positions"), and the paper's **own §13 (L255)**
  says "The pre-band subject-position freeze could not see formation inside the band or across
  positions, so its near-null is uninformative and licenses no 'construction unsupported'
  conclusion." §5 uses that same leg as affirmative evidence.
- **Fix:** either drop the pre-band-freeze sentence from §5 (the band-internal tests in the same
  paragraph already carry the "formed over depth" claim), or re-state it as the superseded/
  uninformative leg it is, and correct Appendix A row 290's source to
  `2026-10-02-p1-reviewer-experiments/FINDINGS.md` with the failed-prereg caveat.

### 3. Appendix A row 316 names the wrong transformer model (MISMATCH)
- **Where:** Appendix A row 316 ("7 exact externalize/resume … **Qwen2.5-Coder-1.5B**, Mamba-130M").
- **Primary:** both cited records use Qwen2.5-**0.5B** —
  `source-frame-stack/FINDINGS.md:15` ("Qwen/Qwen2.5-0.5B", job-b1df140ac26a) and
  `saturn/docs/CAUSAL-CONTEXT-VM.md:4,35` ("Qwen2.5-0.5B" / "Qwen/Qwen2.5-0.5B-Instruct").
- **Fix:** change the model to Qwen2.5-0.5B (the §9.2 body text does not name a model, so only the
  appendix row is wrong).

---

## Secondary / disclose-and-correct items (not blocking, but custody-relevant)

- **`2.15` late-call lesion (§5 L128, §12 L228) UNSOURCED.** The paired "20.82 vs 2.15" first-vs-
  late source-lesion claim: 20.82 traces to `camera-distance … summary.json`
  (`restore_single_10_early/mad_vs_recipient = 20.827`), but **no 2.15** appears there; the nearest
  late-call restore arms are 4.40 and 9.33. Confirm the 2.15 primary or correct the value.
- **Draft-file citations.** The reader-cosine spine numbers (§4 L102, abstract, Fig 3) are cited to
  `FINDINGS-addendum-draft.md`; the connected-forecast MAE 0.015099 (§10) is cited to
  `qwen/DRAFT_INTEGRATION.md`. In both cases the *values* match and are custody-noted/corroborated
  by promoted files, but the appendix should point at the promoted record (or the drafts should be
  promoted). No promoted `FINDINGS-addendum.md` exists in site-variance-decomposition.
- **XNOR primary is an obsidian survey.** Appendix A row 313 sources the 148/150 vs 0/150 result to
  `obsidian/2026-08-17-151407-all-experiments-composite-survey.md` — outside the three primary
  roots the audit brief names; trace it to the underlying saturn experiment if one exists.
- **"0 of 96 checkpoint reads" (§8/§9.2) exact count not located.** `CAUSAL-CONTEXT-VM.md`
  documents the Qwen2.5-0.5B all-layer serving assay, but the exact "0/96" was not found as a
  string. (Distinct from the null-net "top-1 0/96", which is confirmed.)
- **"SDXL twice" (§9.1 L186).** The 7 specimens include **3** SDXL-family records (wai-sdxl-170917,
  wai-sdxl-170918, illustrious-sdxl), not two; family_count is 5. Minor wording.
- **Mamba writer survival "0.66–0.90" (§10 L210).** Matches the clock-retest FINDINGS, but the raw
  `summary.json` `writer_surv` dips to **0.631** (130M counting) — the FINDINGS' stated lower bound
  is slightly optimistic; the paper inherits it.
- **Eye-head/row overlap path (App A row 274).** Value (5–7/8, 10–15/64) is correct but lives in
  `artifacts/scene-editing/sources/2026-08-28-094822-….md:93`, not the cited `scene-editing.md`.
- **FLUX "15 setup-by-site combinations" (§5 L142)** and **head-edge figures generally**: the "15"
  count was not found in the flux2-joint01 FINDINGS; the ≤0.56 / ≥0.91 spine numbers it rests on
  are confirmed.

## Known-trap checklist (all cleared)
- E20 cross-family = 3 families / 4 cells — **confirmed** (`2026-10-02-e20-cross-family/FINDINGS.md`).
- Qwen formation 16/16 rescue, 14/14 block — **confirmed** at
  `2026-10-01-qwen-scaffold-context-poc/FINDINGS.md:62`.
- Mamba clock-retest primary `…/results/summary.json` — **confirmed** (verdict, 0/6, 1/6, 0/6).
- Formation-over-time primary `…/results/FOT_analysis.json` — **confirmed for its 4 real stats**;
  it is exactly where the paper's "pre-band freeze 0.675" is **not** found (must-fix #2).
- 7B numbers block 0.595 / rescue 0.770 / wrong −0.026 — **confirmed** from the 7B sweep.

## Figures
All 14 figure files referenced in `paper.md` exist under `figures/`. Caption data matches the
primaries **except** Figure 1 and Figure 9 (the FLUX.2 control MAEs — must-fix #1). Figure D1/D2/D3/
D4, Figure 2/3/4/5/8/10 captions match. (Unused figure files present but not referenced:
`fig1_scaffold_schematic.png`, `fig5_variance_decomposition.png`, `fig8_scene_compiler_proof.png`.)
