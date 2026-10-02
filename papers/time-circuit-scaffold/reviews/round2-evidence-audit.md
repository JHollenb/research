# Round 2 evidence audit — time-circuit-scaffold/paper.md

Scope: trace every number (abstract, tables, captions, body, Appendix A) to source under
`~/domains/saturn/experiments/` and `research/papers/custody-audit-2026-10-02.md`. Round-2
emphasis per task: stale framings (`4.17 fired`, `none triggered`, `rock-stable`,
sliding-window causal claims), smoke/killed-job leakage, SD-without-locator,
prereg-vs-post-hoc confusion, claims stronger than source, figures-vs-text. Read-only on
paper. Did NOT cite blind-final-boss-certification or grail outputs.

Verdict: **numerically sound — every headline number recomputes to the digit against its
JSON.** One material staleness (the confirmatory run has LANDED but the paper says it is
"in progress"), one Appendix-A completeness gap (Figures A/B/C sources absent), and a
handful of minor wording/label items. Stale framings the task warned about are NOT present
in the paper text (they live only in the source FINDINGS files).

Source legend: SVD = 2026-10-02-site-variance-decomposition; P2 = 2026-10-02-p2-reviewer-experiments;
E20X = 2026-10-02-e20-cross-family; VMT = 2026-10-02-vm-trace-visualizer; CA = custody-audit-2026-10-02.md;
R1 = reviews/round1-evidence-audit.md (already matched there).

## Trace table (claim | paper line | source | status)

| Claim | Line | Source | Status |
|---|---|---|---|
| Gemma id L22 SD 0.00 n42; Qwen id L23 SD 1.16 n42 | 19,65,101,206 | SVD phase2_sitemap_analysis.json | MATCH (22/0.0/42; 23/1.165/42) |
| Gemma color L20 SD 1.11 n25; Qwen color commit-SD 4.17 n22 | 97,101,103 | SVD phase2_sitemap_analysis.json | MATCH (20/1.114/25; 23/4.172/22, range[7,23]) |
| Qwen shape 0.75; Gemma shape 1.88 (5-of-6 list) | 103 | SVD phase2_sitemap (0.745, 1.881) | MATCH |
| across-op commit shift Qwen 0 / Gemma 2 | 67,69,101 | SVD phase2_sitemap (0.0 / 2.0 id~color) | MATCH |
| whole-band necessary 100% all cells | 101 | SVD phase2_sitemap frac_whole_iso=1.0 | MATCH |
| read-site 42.2/29.0/1.1/1.6 (1,152 cells) | 93,97 | SVD F2_F3_qwen_predictive_readmap.json | MATCH (R1; = A_analysis ab_subset) |
| "eleven to one" = coord×op 29.0 / fact-like 2.7 | 19,93,206 | 29.0/(1.1+1.6)=10.7 | MATCH (R1 fix #4 applied) |
| store necessity 84.0/3.2/2.0/10.4 (64 cells) | 97,99 | SVD F2_scaffold_poc_store_necessity.json | MATCH |
| within-op reader 0.947/0.927/0.961; across-op id~rel 0.336 | 79,81,83 | SVD F3_head_edge_cosines.json | MATCH (R1) |
| denoised within-op 0.92–0.999 | 79,81 | SVD FINDINGS / phase3 | MATCH |
| id route −1.18 (L23KV0V); rel −0.30 (L22KV1V) | 83 | SVD FINDINGS | MATCH |
| attn mass .63/.61/.70 vs reader .95/.93/.96 | 87 | SVD FINDINGS | MATCH (R1) |
| **FAL-3 fired as frozen in 2/6: Qwen color 5.45, Gemma id 4.01** | 97,103,206,259 | SVD FINDINGS-addendum-draft + confirm_fal3_analysis.json | MATCH — correct post-fix framing; **4.17 is labeled commit-locator, not "fired"** |
| median argmax L 0 (Qwen color) / 13 (Gemma id) | 103 | SVD confirm_fal3 S1_median | MATCH (1.0/13.0) |
| Fig A: ratio 19.0; coord→1.2–1.4%; vproj 11.9; top-1 0/96 | 93,95 | P2 A_analysis.json | MATCH (19.05; 1.16/1.37%; 11.85; 0/96) |
| Fig A: coord×op exceeds nulls 17× and 7.8×; ratio>5; 0.997 vs 0.485; random +0.350 | 93 | P2 A_analysis.json | MATCH (17.07/7.79; 0.997/0.485; +0.350) |
| jackknife interval 16.3–30.6 (prereg promised bootstrap) | 93 | P2 A_analysis ratio_jackknife | MATCH; deviation correctly disclosed |
| Fig B: no-op 0.0 both dirs; window-4 shifts 19.6; profile byte-identical; L16/18/20/22 + / L17/L21 − | 59,61 | P2 B_analysis.json (job-0b7652b2112d) | MATCH (0.0/0.0; 19.624; 0.0; pooled signs) |
| Fig C: 0/14 flips; rel +2.19, color +0.16; L23KV0 −0.808→+0.007; L24 top of grid | 83,85 | P2 C_analysis.json | MATCH |
| Table 1 within-op per-item 0.749/0.735/0.988 (Q), 0.895/0.865/0.807 (G) | 111 | SVD phase3_relational_analysis.json | MATCH |
| Table 1 id~capital 0.204/0.218; id~color 0.842/0.911 | 112,113 | SVD phase3_relational | MATCH |
| Table 1 capital SD 0.00/5.39 (Q), 0.00/2.14 (G) | 114 | SVD phase3 (commit) + FINDINGS-addendum (argmax) | MATCH |
| SS stat Gemma 0.58/0.42 fired; Qwen 0.27/0.73 | 107 | SVD phase3 (0.581/0.419; 0.274/0.726) | MATCH |
| App C denoised 0.995/0.96/1.00 (Q), 0.999/0.976/0.995 (G) | 259 | SVD phase3 within_op_across_template_denoised | MATCH |
| §8 mediation block 0.924 / rescue 0.871 / 42 rows (companion) | 150 | E20X FINDINGS.md (Qwen published cell) | MATCH |
| diffusion 21/21; wrong-source/sign 57–97 MAE; 7 specimens/5 fam | 144,170 | scene-generator demos/blog | CARRY R1 VERIFY (57–97 not located in cited blog; outside named set) |
| fork/replay 4/4+4/4 over 32 tok; 64/64; 0/96 | 176, AppxA 241 | blog 2026-09-06-015603; 2026-09-30-source-frame-stack | NOT re-verified (outside named set); VMT does NOT back these |
| confirmatory run "in progress / underway / pending" | 19,37,65,103,206,259 | SVD confirm_fal3_analysis.json + FINDINGS-confirm.md (promoted) | **STALE — see must-fix #1** |
| Appendix A rows for Figures A/B/C + confirm run | 220–241 | P2 + SVD confirm | **MISSING — see must-fix #2** |
| §5 "40 fresh countries across two templates" | 107 | SVD phase3 (20 countries × 2 templates = 40 facts) | MISLABEL (should be 20 countries) |
| Appendix A "32 same-parent query pairs" vs §4 "16/op … 128 checks" | 73 vs 223 | POC FINDINGS (job-08678fbc9188) | INCONSISTENT count (carry R1) |
| §11 "SD 0.00 across 42 Gemma facts" (no locator label) | 184 | SVD phase2_sitemap | MATCH value; SD quoted w/o post-hoc-locator label |

## Notes / non-issues
- **Stale phrases absent from paper:** `none triggered`, `rock-stable`, `strong-signal
  counterpoint`, `4.17 fired` do NOT appear in paper.md (they persist in SVD FINDINGS.md /
  FINDINGS-addendum-draft / FINDINGS-confirm — source files, not the paper). The paper's
  §3/Fig B sliding-window handling is the corrected depth-not-attention-type reading. Good.
- **Smoke/killed leakage:** none into the paper. Appendix A labels smokes job-378aa78e7b17 /
  job-ba1c1a4a6a04 as smokes; E20X killed jobs (66931f253d0c, 0efc7bef9d07) have no report
  and feed no number. FINDINGS-addendum's "6.4 GB / 37 s" (smoke vs full 7.4 GB / 41 s per
  CA) is NOT in the paper.
- **vm-trace-visualizer:** none of its numbers (−2.9423, P=0.887, RGB MAE 2.74, 3.76 nats)
  appear in paper.md — nothing to reconcile. If a VMT figure is ever added, its own snippet
  is internally inconsistent (Mamba writer band "L19-21" para vs "L21-23" caption) and runs
  bf16, not the paper's fp32 — fix before citing.
- **Dual ratio:** "eleven to one" (29.0/2.7 on 2-lex) and Fig A "19.0" (coord×op/coord×fact
  on 4-lex) are different quantities; both sourced, but a reader may conflate them. Optional
  one-clause clarification.
- Prereg timing for SVD Phase-2, the reader-profile confirmation, and the addendum is genuine
  (R1/CA); the frozen-manifest rewrite and jackknife-vs-bootstrap are disclosed in §5.
- Figure PNG pixels were not inspected (as in R1); caption numbers all trace to the JSONs
  above. Recommend a pre-submission pixel check of figs 2/4/5/A/B/C bars.
