# Round-3 evidence / consistency audit — time-circuit-scaffold

Date: 2026-10-02. Scope: everything changed between round-2 baseline `30c8267` and HEAD
(`bf7257f`) in `papers/time-circuit-scaffold/{paper.md,README.md}` plus `figures/make_fig5.py`.
Method: every added/edited number traced to its result artifact and independently cross-checked
against `custody-audit-2026-10-02.md`. Read-only on `paper.md`. MEASURED = recomputed/confirmed
against the JSON or custody recompute; ASSERTED = stated in text without a backing artifact value.

Diff size: paper +47/−29, README +77/−48. Round-2 commits audited:
`30c8267` (relational addendum) → `96f0e5d` (null) → `be07fe0` (sliding causality) → `bf7257f`
(confirm-color).

## Numbers traced to source — all MATCH unless flagged

### Confirm-color (§5, abstract, Fig 5, README, evidence appendix)
Source: `.../site-variance-decomposition/FINDINGS-confirm.md`, `results/confirm_fal3_analysis.json`
(job-8b550b584da4 Qwen, job-b7d05acf8192 Gemma); custody "Confirm-color run" = PASS.
- Qwen colorC n=48: S1 2.84 / S2 1.44 / S3 1.76 — MATCH JSON (2.835 / 1.4428 / 1.7647). MEASURED.
- Gemma colorC n=106: S1 3.44 / S2 0.90 / S3 0.97 — MATCH (3.4368 / 0.9009 / 0.9740). MEASURED.
- Gemma identity canary S1 4.06 (write-signal n=41) / commit SD 0.00 — MATCH (4.0560 / 0.0);
  all-admitted 4.01 (n=42) — MATCH. MEASURED.
- Colors: Qwen 27 unique (frozen ≥40; single-token filter dropped 14, 36 items failed read-back),
  Gemma 54. MATCH FINDINGS + custody. MEASURED.
- Chunking "numerics-neutral ~2e-5 nats, custody PASS; freeze mtime-only" — MATCH custody. MEASURED.

### Appendix D reviewer controls A/B/C
Source: `.../p2-reviewer-experiments/FINDINGS-AC-coordinator.md`, `results/{A,B,C}_analysis.json`;
custody "P2 reviewer A/C" = PASS, B recomputed here from `B_analysis.json`.
- A (Fig A, §5): op:fact 19.0 trained → 0.62 shuffled / 1.10 random; vproj 11.9; coord main
  1.2–1.4%; exceeds nulls 17×/7.8×; relation 0.997 vs 0.485 (random +0.350 = failed pred);
  top-1 0/96. ALL MATCH A_analysis (.381/.304/.0159/19.05; .0137/.0178→0.62; .0116/.0390→1.10;
  11.85; 17.07×/7.79×; .997/.485/+0.350). MEASURED.
- B (Fig B, §3): type flip 0.0 both directions; window-4 flip 19.6; commit profile byte-identical,
  positive L16/18/20/22, non-positive L17/L21; 17 tokens < 4096; 42 identity items. ALL MATCH
  B_analysis (0.0/0.0, 19.624, B_P2 0.0, baseline==typeswap pooled). MEASURED.
- C (Fig C, §4): 0/14 flips; relation +2.19 nats, color +0.16; L23.KV0 −0.808→+0.007. MATCH
  C recompute (+2.185 / +0.159). MEASURED.

### Agarwal reconciliation (§5 new ¶, §11)
Source: addendum custody (capital commit L22 SD 0.00 n=40 both; frozen-argmax 5.39 Qwen / 2.14
Gemma). See FLAG-2 below — the "same layer (22) in both models" claim is wrong for Qwen.

### §10 (edited wording/scale/refs)
- XNOR 148/150, XOR 148/150 vs 0/150: MATCH `obsidian/2026-08-17-151407` lines 265–267. MEASURED.
- wrong-site 1.011 vs −0.133 / −0.607 / K/V 0.602 vs −0.153: panel report rows carry
  normalized_effect 1.011/1.0 (right) and the negatives; median ≈1.011. MEASURED (unchanged in R2).
- 57–97 MAE vs 0.0: MATCH blog `2026-09-30-165158` line 153 ("57–97 MAE") + cross-model JSON
  (rgb_mae 0.0 ×21). Both cited blog files EXIST. MEASURED. "(0–255 RGB scale)" = ASSERTED label
  (source says "MAE"; rgb_mae on 8-bit implies 0–255 — reasonable).
- Relational addendum: "20 countries × 2 templates = 40 facts" now consistent (was "40 countries").
  Table 1 cosines 0.204/0.218, 0.842/0.911; SS Gemma 0.58/0.42 fired, Qwen 0.27/0.73. MATCH custody.

### Fig 5 regeneration (`make_fig5.py`)
Reads F2A from `F2_F3_qwen_predictive_readmap.json`, F2B from `F2_scaffold_poc_store_necessity.json`,
F2C confirm S1/S2/S3 + Phase-2 S2 from JSONs (`confirm_fal3_analysis.json`, `phase2_sitemap_analysis.json`).
F2A/F2B values (42.2/29.0/1.1/1.6; 84.0/3.2/2.0/10.4) custody-verified. **Phase-2 S1 (argmax SD)
is HARDCODED** (6 literals: Qwen id 3.81/color 5.45/shape 1.86, Gemma id 4.01/color 3.05/shape 2.45).
Values MATCH `FINDINGS-addendum-draft.md` recompute table, and `phase2_sitemap_analysis.json` holds
no argmax-SD field, so no committed JSON exists to read them from. The script's docstring discloses
this. Reproducibility nit, not a wrong number (see FLAG-3).

### Stale-text / verbatim / locator checks
- README abstract == paper abstract: IDENTICAL (normalized whitespace). PASS.
- All round-1 `<!-- TODO -->` placeholders removed from both files. PASS.
- `paper.md:200` "same-assay checkpoint trajectory … not yet run" = legitimate open-question future
  work, not a stale landed-experiment placeholder. ACCEPTABLE.
- `README.md:115` still reads "coord main 42.2% (null pending)" — STALE (see FLAG-1).

## FLAGS

**FLAG-1 (MUST-FIX, README:115).** Evidence-map row 5 still says "coord main 42.2% (null pending)".
The null ran (Fig A; adjacent new row says "Read-site split is LEARNED"). Internally contradictory
and stale. Replace "(null pending)" with "(null ran; learned — see Fig A / row below)".

**FLAG-2 (MUST-FIX, paper.md:114).** "capital-of committing at the same layer as identity (layer 22,
SD 0.00 in both models)". Capital is L22 (SD 0.00) in both — correct — but Qwen identity commits at
median **L23** (SD 1.16), not L22 (confirmed §5:97, confirm JSON, custody). So in Qwen capital and
identity are NOT the same layer, and identity is not at 22. In Qwen capital (L22) actually commits
one layer *before* identity (L23), which trends toward Agarwal's asymmetry rather than against it.
Reword, e.g. "capital-of commits at layer 22 (SD 0.00) in both models — identical to identity's
layer in Gemma (L22) and within one layer in Qwen (identity L23)".

**FLAG-3 (SHOULD-FIX, make_fig5.py F2C).** Six Phase-2 S1 argmax SDs are hardcoded (correct vs
FINDINGS-addendum-draft.md, but will not regenerate if upstream changes; four of six are not in any
committed JSON). Either emit `phase2_argmax_sd` into a JSON and read it, or keep the literal and
tighten the comment to cite the exact source table.

**FLAG-4 (SHOULD-FIX, abstract).** Round-2 removed "located by the close of the write window" from
the abstract, so the headline "layer 22 … standard deviation zero / layer 23 (SD 1.16)" no longer
names its locator. Every other instance (Fig 2, §3, §5, §11, README map) labels it the post-hoc
commit locator; round-2's own theme was "locator-label every SD". Re-attach the locator caveat.

**NOTE-5 (minor).** §10 "A parallel result in preparation extends this to a reasoning step" — the CoT
formed-state experiment exists and is custody-audited, but is cited only as "in preparation". Cite the
experiment/companion or soften; as written it is an uncited forward claim.

**NOTE-6 (minor).** Table 2 (paper:134) "SD 0.00–1.16/fact" omits the commit-locator label used
elsewhere.

## Verdict
Every round-2 number recomputes against its source. Two must-fixes are consistency errors (one stale
README cell, one inaccurate Qwen "same-layer" claim); two should-fixes are locator/figure-provenance
hygiene. No fabricated or wrong-run numbers found.
