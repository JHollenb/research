# Round 1 evidence audit — time-circuit-scaffold/paper.md

Scope: every numeric claim in abstract, intro, §3–§12 lead sentences, tables, figure
captions, conclusion. 55+ checked against README map + source FINDINGS/result JSONs
(read-only; no model runs). Verdict: **numerically sound**. The large majority MATCH to
the digit. One MISMATCH (Pythia formation window), one overstated prereg headline, and a
few framing/selective-reporting items. Figure-caption numbers (fig2–fig7) were verified
against the decisive-test JSONs; PNG pixels were not inspected.

Source legend: SVD = saturn/experiments/2026-10-02-site-variance-decomposition;
POC = 2026-10-01-qwen-scaffold-context-poc; CONF = 2026-10-01-scaffold-confirmation;
E16/17/19/20 = 2026-09-30-full-layer-sweeps; MSW = 2026-09-30-mamba-full-layer-sweeps;
DOSE = 2026-10-02-mamba-writer-clock-dose; MCLK = 2026-10-02-mamba-operation-clock-debugger;
CONN = 2026-10-01-connected-architecture; P1 = ../time-formed-circuits/paper.md;
ARCH = ../scaffolds-and-dynamic-circuits/architectural-paper.md.

| Claim | Paper | Source | Value | Class |
|---|---|---|---|---|
| coord 42.2% / coord×op 29.0% / fact 1.1% / tmpl 0.6% / order 0.2% (1,152 cells) | L19,91,171 | SVD results/F2_F3_qwen_predictive_readmap.json | .42156/.28956/.01059/.00576/.00223; 48×24 | MATCH |
| coord×binding 1.6% (read-site) | — | same JSON | .01630 (>fact) **omitted from §5/abstract** | MATCH-but-incomplete |
| store op 84.0% / fact 3.2% / tmpl .06% / binding .3% (64) | L19,93,95 | SVD F2_scaffold_poc_store_necessity.json | .83952/.03169/.00064/.00338; [4,4,2,2] | MATCH |
| "~26× the fact" | L91 | 29.0/1.1 | 26.4 | MATCH |
| Gemma id L22 SD0.00 n42; Qwen id L23 SD1.16 n42 | L19,65,97 | SVD phase2_sitemap_analysis.json | 22/0.0/42; 23/1.165/42 | MATCH |
| Gemma color L20 SD1.11 n25 | L97 | same | 20/1.114/25 | MATCH |
| Qwen color L23 SD4.17 n22; 20/22 @L18–23 | L99 | same | 23/4.172/22; range[7,23] | MATCH(value); see Fix 1 |
| across-op commit shift Qwen 0 / Gemma 2 | L67,69,97 | same | 0.0 / 2.0 | MATCH |
| within-op reader 0.947/0.927/0.961 | L79 | SVD F3_head_edge_cosines.json | .9474/.9273/.9607 | MATCH |
| across-op id~relation 0.336 | L81,83,173 | same | .33621 | MATCH |
| denoised within-op 0.92–0.999 | L79,81,173 | SVD FINDINGS (phase2) | Qwen .995/.96/.92 Gemma .999/.976/.987 | MATCH |
| id route −1.18 (L23KV0V); relation −0.30 (L22KV1V) | L83 | SVD FINDINGS | as stated | MATCH(findings) |
| attn mass .63/.61/.70 vs reader .95/.93/.96 | L85 | SVD FINDINGS | as stated | MATCH(findings) |
| Gemma sliding L16–22 0.58; each ≤0.08; global −.03..−.08; cut raises 0.18 | L55 | E19-window FINDINGS(E19b), E17 | 0.58; .02/.00/.04/.08; −.18 | MATCH |
| Mamba 130M L20 d.83 81% / 370M L39 d.81 67% / 2.8B L44 d.69 67% | L57 | MSW FINDINGS | 81.3%/66.6%/66.5%; 20/24,39/48,44/64 | MATCH |
| write is larger lever 6/6; retention correlate | L59,121 | DOSE FINDINGS/summary.json | 6/6; P1 false 6/6 | MATCH |
| window: Qwen0.5B .70@L21/.04@L22; Mamba130M .70@L19/.00@L20 | L61 | E16 FINDINGS | L21 0.70/L22 0.04; L19 0.70/L20 0.00 | MATCH |
| window: "Pythia .48@L17 then .01@L18" | L61 | E16 FINDINGS | **0.48 at L18; 0.01 at L22; writer L17=0.95** | **MISMATCH** |
| Qwen1.5B best single .08 / 3-adj .23 / band L22–27 .96 | L63 | E19 FINDINGS | .08/.23/.96 | MATCH |
| layer main-effect 66–98%; shift 0/1/2 | L69 | SVD FINDINGS C2 | as stated | MATCH |
| same-patch harm 3.130/0.583/3.021 nats, ranges, 16/16 | L73,75,173 | POC FINDINGS | identical | MATCH |
| redirect color 16/16, position 12/16, id anchor 10/10 | L77 | POC FINDINGS | identical | MATCH |
| "32 same-parent query pairs" | L73 | POC (64 rows,16/16/op,128 checks) | not stated verbatim | VERIFY(minor) |
| relation .954 vs .566, RMSE .029 vs .149, 8/8; shape 7/8 all,8/8 comp | L109,111 | CONF qwen-predictive FINDINGS | identical | MATCH |
| color 5/8; identity comp 0/4; size unavailable | L113 | same | 5/8; 0/4 | MATCH |
| permute 256: rel .955→.049, color .838→.110, id .931→.569; mild intact | L109,115 | CONF FINDINGS | identical | MATCH |
| Mamba capital 8/8 .9941/.9880; id 4/4 .9586/.9102; transfer 12/12; 27-coord | L119 | MCLK FINDINGS/FROZEN | identical ("both arms 8/8" NOT used) | MATCH |
| diffusion 21/21 byte-exact; 7 specimens; 5 families | L123 | blog 2026-09-30-165158 (21/21,5 fam); scene-generator-paper (7 specimens) | confirmed | MATCH |
| wrong-source/sign diverge "57 to 97 MAE" | L123 | not in cited blog (scene-gen shows ~59) | not located | VERIFY |
| late=violet/early=blue; 12 refs across 56 images; 4 cases | L125 | research/demos/scene-editing.md | late dist .0689; 4×3=12, 4×14=56 | MATCH(derived) |
| France→Germany 1/3 held; zero→"is"; reinstate | L129 | CONF qwen-feedback FINDINGS | identical | MATCH |
| frozen-ref B 7/8, A 8/8; refB 3/4, refA 4/4 | L131 | 2026-10-01-qwen-frozen-reference-payload FINDINGS | identical | MATCH |
| mediation block 0.924, rescue 0.871, 42 rows, wrong-id 37/42 | L133 | E20 FINDINGS; P1 L106–116 | .924/.871/42; 37/42 | MATCH |
| connected MAE .015099 vs .014593 / .014588; additive .015099; 1/3 | L139,141 | CONN qwen FINDINGS + analysis.json recompute | .015099; op-blind .014593, query .014588 (recomputed) | MATCH |
| role matcher 6.9125 vs 6.9511, gap .0386 | L139,143 | ARCH:433 ("opened outcomes") | identical | MATCH(sibling) |
| cross-family RMSE .0928 vs .8526; 2+2+1 rows; color 8/8 miss | L145 | CONF FINDINGS + cross-family | identical | MATCH |
| attribution 0.10–0.21 in band; flip 83%; ~30% error nodes; 12+8 items | L31,155 | P1 §5 | .10–.21; .83; ~30%; 12/8 | MATCH(companion) |
| arXiv IDs | §10 | P1/ARCH/space-and-time ref lists | 13/14 attested; 2310.17191 only in bridge-paper.md | VERIFY(minor) |

Audit checks: (a) fig captions' numbers all trace to JSONs above (not pixel-verified).
(b) **Prereg timing: genuine for Phase 2.** FROZEN.json mtime 00:14:51 and PREREG 00:14:36
predate Phase-2 job receipts (smoke 00:16:16, Qwen 00:18:12, Gemma 00:20:42). BUT the
headline read-site split (42.2/29.0/1.1) is a **Phase-1 retrospective reanalysis** of
pre-freeze site maps (F*.json mtime 00:05:42); only the per-fact band location is
post-freeze. (c) "both Mamba arms 8/8" confirmed NOT used. (d) all five "stock eager"
results confirmed to load attn_implementation="eager" (incl. qwen-feedback worker.py:727,
tagged "stock-HF-eager-native-causal"); feedback runs eager under a TokenMachine stepping
harness. (e) above. (f) no number conflicts between Paper 1 and Paper 2 (0.924/0.871/42,
attribution, mediation all identical).

## Top 10 fixes (by severity)

1. **"Three preregistered falsifiers, none triggered" is overstated** (abstract L19, §1 L33,
   §5 L99, §12 L171). FROZEN.json defines FAL-3 = `sd_argmax_write > 4` and P3 = `<=2`;
   Qwen color's write-commit SD is **4.17** (range [7,23]) — literally crossed. "None
   triggered" relies on a post-hoc switch to the robust necessity-argmin SD (≤2.06) and
   exclusion of two weak-signal facts, neither preregistered. Reword to "one falsifier
   crossed on one underpowered cell; robust statistic and median clear it."
2. **§3 L61 Pythia formation-window numbers misassigned** (MISMATCH). Paper: "0.48 at L17
   then 0.01 at L18." E16: residual write is 0.95 *through* L17; 0.48 is at **L18**, 0.01
   at **L22**; writer L17. Pythia decays gradually, so "fails immediately after" is false
   for Pythia. Fix layers or drop Pythia as the hard-edge exemplar (Qwen0.5B/Mamba hold).
3. **Variance decomposition is retrospective, not prospective** (abstract/§5). The 42.2/29.0/
   1.1 split is Phase-1 reanalysis of pre-freeze data; Phase-2's own read split is confounded
   (coord×fact .865 > coord×op .135, disclosed §5 L101). Add one clause so the abstract does
   not imply the split itself was preregistered.
4. **coord×binding 1.6% omitted** from the read-site enumeration (§5 L91, abstract) though it
   exceeds coord×fact 1.1%; "1.1% to the fact"/"26×" selectively reports the smaller term.
   Report binding or state it is folded into the query/operation grain.
5. **Diffusion "57 to 97 MAE" (§7 L123) unlocated** in the cited blog (gives 21/21, 5
   families). Cite scene-generator-paper.md for the wrong-source divergence range and the
   "seven specimens" count.
6. **"32 same-parent query pairs" (§4 L73)** not stated verbatim in POC (64 rows, 16/16 per
   op, 128 pairing checks). Show the derivation or restate as 16/op.
7. **Ref 2310.17191** (Feng & Steinhardt) is absent from the companion/architectural
   reference lists (present only in bridge-paper.md). Confirm intended.
8. **2026-dated arXiv IDs** (2609.17537, 2606.15796) are workspace-consistent but externally
   unverifiable; flag for a reviewer, as future IDs can read as fabricated.
9. **§5 L99 "largest SD for a well-powered cell is 1.16"** silently reclassifies Qwen color
   (n=22) as not well-powered. State the power threshold used.
10. **Figures not re-rendered.** Caption numbers match the JSONs, but confirm the plotted
    bars/points in fig2/fig4/fig5 equal those values before submission (PNGs not pixel-read
    in this audit).
