# Round 1 — Evidence audit of time-formed-circuits/paper.md

Auditor: evidence-audit pass (read-only). Date: 2026-10-02.
Scope: every numeric claim in abstract, intro, all tables, figure captions, conclusion,
section lead sentences. Each opened against the README evidence-map source. No model runs.
Classes: MATCH / ROUNDING / MISMATCH / UNSOURCED / WRONG-CONDITION / SUPERSEDED.

Sources read in full or in part: E20-xfam FINDINGS + results/analysis.json; E20-mediation;
E16; E17; E19; E11; E13; E18; E12 (ar-exact-join); E6 circuit-tracer (+Amendment);
FLUX E1b (+results/full-report.json), E1c, E7, E8, E9; Mamba full-layer-sweeps;
mamba-writer-clock-dose (+summary.json); E4 (+E4b); E10 (completed-answer-rerun);
E10-cot; E14; isolated-swap-reruns; space-and-time-circuits/paper.md References.

## Verification table (claim | paper line | source path:locus | value found | class)

| # | Claim (section) | paper | source | found | class |
|--|--|--|--|--|--|
|1|block 0.73–0.92 (abstract/1/3.4)|L18,32,123|e20-cross-family/FINDINGS.md + analysis.json|0.728–0.924|ROUNDING-OK|
|2|rescue 0.71–0.99 (abstract/3.4)|L18,32|same|0.713–0.985|ROUNDING-OK|
|3|identity interchange ≤0.08 (abstract/5/Fig5)|L18,151,157|circuit-tracer/FINDINGS.md Amendment|0.08 (unfrozen max median)|MATCH|
|4|native K/V cut flips 83% (abstract/5)|L18,153|circuit-tracer FINDINGS ref tbl|identity 2nd-half flip 0.83|MATCH|
|5|in-forward L0 0.985 (2.2)|L56|E17-isolated-kv-writes.md|0.985|MATCH|
|6|isolated L0 0.009 (2.2)|L56|E17|0.009|MATCH|
|7|Qwen L24 0.57, L27 0.37 (3.1)|L70|E16-residual-writes.md|0.57 / 0.37|MATCH|
|8|SmolLM2 L23 0.07 (3.1)|L70|E16|0.07|MATCH|
|9|Pythia-410M L22 0.01 (3.1)|L70|E16 (s16000)|0.01|MATCH|
|10|Table 1 all 21 cells (3.2)|L78-88|E19-window-necessity.md|all match (single/w3/w80)|MATCH|
|11|best-3 adj 0.23 & 0.18 (3.2)|L90|E19|Qwen 0.23, Gemma 0.18|MATCH|
|12|isolated write 0.81 Qwen L23 & Gemma L22 (3.2)|L96|E17|0.81 / 0.81|MATCH|
|13|block 0.924 [0.765,1.030] (3.3)|L106|E20-mediation.md + analysis.json|0.924189 [0.7647,1.0305]|MATCH|
|14|rescue 0.871 [0.850,0.894] (3.3)|L106|same|0.871323 [0.8495,0.8939]|MATCH|
|15|seed gain 1.577–5.555, med 3.515 (3.3)|L106|E20-mediation|1.577–5.555, 3.5148|MATCH|
|16|wrong-id authors own 37/42, −0.067 (3.3)|L108|E20-mediation|37/42, −0.0667|MATCH|
|17|earlier band 0.066 (3.3)|L108|E20-mediation (retained 0.9336)|0.0664|MATCH|
|18|Table 2 Qwen held-out 0.728/0.713 (3.4)|L117|analysis.json qwen_ho|0.7279/0.7131|MATCH|
|19|Table 2 Gemma 0.768/0.985 (3.4)|L118|analysis.json gemma|0.7678/0.9849|MATCH|
|20|Table 2 SmolLM2 0.740/0.910 (3.4)|L119|analysis.json smollm2|0.740/0.910|MATCH|
|21|held-out cand 81% / full 39% (3.4)|L125|analysis.json top1|0.8101/0.3924|MATCH|
|22|held-out seed gain med 6.05 vs 3.5 (3.4)|L125|analysis.json|6.0485 / 3.5148|MATCH|
|23|Gemma 0.768 = 0.76 necessity (3.4)|L123|E19 Gemma L16-23|0.76|MATCH|
|24|wrong-donor 0.75–1.00; target ≤0.06 (3.4)|L123|analysis.json top1|0.747–1.0; max 0.059|ROUNDING-OK|
|25|earlier band held-out 0.219 (3.4)|L125|analysis.json|0.2188|MATCH|
|26|held-out = 29 single-token ids ×3 ctx, n=79 (3.4)|L121,125|FINDINGS/analysis.json|29 admitted; n_items 87, n_adm 79|MATCH|
|27|read necessity 0.074; L23 restore 1.22 (4)|L139|E13/FINDINGS.md|0.074 / 1.22|MATCH|
|28|one-hot 1.02, full top-1 88% (4)|L139|E13 Q2|1.02 / 0.88|MATCH|
|29|exact-join within 0.03 of clean (4)|L141|ar-exact-join/FINDINGS.md|gap ≤0.005 (forced-choice)|MATCH*|
|30|repetition 1.00 / semantic 0.00 (4)|L143|E18/FINDINGS.md|query-bucket 0.00 all synth; E12 induction 1.00|MATCH*|
|31|~30% error nodes (5)|L149|E6 FINDINGS|~30%|MATCH|
|32|≤0.18–0.28 per layer (5)|L149|E6 (largest single-layer share)|0.180 / 0.284|ROUNDING-OK|
|33|L0 largest in 11/12, 8/8 (5)|L149|E6|L0 11/12, 8/8|MATCH|
|34|commit band 0.10–0.21 (5)|L149|E6 (0.163[.099,.214]/0.144[.099,.187])|0.099–0.214|ROUNDING-OK|
|35|interchange identity ≤0.08, color 0.31–0.42 (5)|L151|E6 Amendment|0.08; 0.31(unfroz)–0.42(froz)|MATCH|
|36|graph-top identity −0.03 to −0.19 (5)|L151|E6 Amendment identity row|identity −0.03 to −0.14 (−0.19 is COLOR)|MISMATCH|
|37|native 2nd-half 0.83/0.84; whole 0.93/1.00; single 0.08/0.15 (5)|L153|E6 ref tbl|all match|MATCH|
|38|FLUX bounds 0.5620/0.20743/0.91309/0.01101 (6.1,T3)|L172-174|E1b full-report.json|0.562/0.20743/0.91309/0.01101|MATCH|
|39|15 cells, 3 baselines = 3 setups ×5 site sets (6.1)|L169|E1b|3×5=15|MATCH|
|40|5-seed: interchange→source 5/5; deletion 5/5 & 4/5; sham 5/5 (6.1)|L182|E7/FINDINGS.md B1-B3|5/5, 5/5, 4/5, sham 5/5|MATCH|
|41|Klein-9B single ≤0.48 vs 0.90–0.95; 8/9 id, 7/9 light (6.2)|L188|E8/FINDINGS.md|0.48; 0.90-0.95; 8/9, 7/9|MATCH|
|42|SDXL single ≤0.215 vs 0.985; one-step removal (6.2)|L188|E9/FINDINGS.md|0.215 / 0.985; steps 0-1 →source|MATCH|
|43|Mamba writer 0.69–0.83 depth L20/L39/L44 (7,T4)|L204|mamba-full-layer-sweeps|0.833/0.813/0.688|MATCH|
|44|clock 0.01–0.40, write 0.02–1.37, joint 0.02–1.87 (7.1)|L213|writer-clock-dose/FINDINGS.md|exact ranges match|MATCH|
|45|neighbor L40 0.36 vs writer L44 0.04 (7.1)|L214|writer-clock-dose|0.36 / 0.04|MATCH|
|46|margin positive in 3/6 cells; 0.87→0.83 (7.1)|L214|writer-clock-dose (3/6 in text)|3/6 confirmed; 0.87/0.83 not in summary.json (in report/text)|MATCH*|
|47|writer pair 0.74–0.81 recoverable loss (7.2)|L222|E4/FINDINGS.md N_ko|0.736–0.814|ROUNDING-OK|
|48|relay 0.58–0.72, writer 0.24–0.29 (7.2)|L222|E4 per-head (L2H1,L3H6)|0.576/0.724; 0.241/0.291|MATCH|
|49|≤0.18 necessity per layer in distributed stores (7.2)|L222|E19|0.18=Gemma best-3-adj; single-layer 0.08; Qwen 3-adj 0.23|IMPRECISE|
|50|swap authors donor 19/32, 30/30 (8)|L228|E10/FINDINGS.md|19/32, 30/30|MATCH|
|51|removal wrong 26/32, 3/30; repair 6/32, 25/30; unres 0/2 (8)|L228|E10|26/32,3/30;6/32,25/30;0,2|MATCH|
|52|primary panels 32 & 30; canary flips 1.00 (8)|L226|E10|32/32, 30/30 parser changed|MATCH|
|53|two-step 8/8 consumed, 0/8 early, Δ 0.037/0.015 (8)|L230|E10-cot/FINDINGS.md|8/8; 0/8; Δ 0.04/0.02|ROUNDING-OK|
|54|E11 operands ≤L7, sum L18-21, necessity 0.35 (8)|L232|E11-computed-object.md|L17 0.35; residual sum L18-21|MATCH|
|55|Appendix A E11 model = Qwen2.5-1.5B, n=45 (App A)|L291|E11-computed-object.md|"SmolLM2-1.7B, 24 layers", n=45|MISMATCH|
|56|E14 Falcon-H1 22 identity, 9 color (App A)|L288|E14/FINDINGS.md|22/22, 9/20|MATCH|
|57|Fig 4 plotted 0.562/0.913/0.207/0.011|L178-180|E1b (visual read)|bars 0.562/0.913/0.207/0.011|MATCH|
|58|Fig 5 plotted 0.08/0.94(.83), 0.42/0.81(.84)|L155-157|E6 (visual read)|bars match exactly|MATCH|

\* = matches source but carries a qualifier (see fixes D, G/H, #46).

## Task-specific checks

(a) Fig 4 & Fig 5 (writer-generated): every plotted value read visually and matched to the
FINDINGS source (#57, #58). Fig 4: 0.562 / 0.913 / 0.207 / 0.011 against the 0.90 and 0.15
lines. Fig 5: identity 0.08 vs 0.94 (flip 0.83); color 0.42 vs 0.81 (flip 0.84). One label
nuance: Fig 5 x-axis shows n=12 / n=8 (the feature-comparison panel), while the green
native bars (0.94/0.81) are from the 42-id/25-color sweep; the caption states this, so OK.

(b) References: 17 of 18 body references and all 6 model/tool cites have arXiv IDs / venues
that match the API-verified space-and-time-circuits/paper.md References list
(Agarwal 2609.17537, Cheng&Zhang 2605.04061, Görgün 2512.08486, Mazur 2606.15796,
Bugaud TrustNLP pp.515-527, Hanna BlackboxNLP pp.239-249, Geva 2304.14767, Hase 2301.04213,
Hendel 2310.15916, Lieberum 2408.05147, McGrath 2307.15771, Meng 2202.05262,
Miller 2407.08734, Rushing&Nanda 2402.15390, Todd 2310.15213; models 2408.00118 / 2312.00752
/ 2304.01373 / 2412.15115 / 2502.02737). ONE reference is NOT in the verified list and
must be independently checked: **[Geiger 2023] arXiv:2301.04709** (added in §9). Flag: verify.

(c) Stock eager attention outside the wrapper defect: CONFIRMED for the defect question — no
cited experiment uses the mask-defective wrapper. Backends found: E16/E17/E19/E13/E18/E11/
E20(xfam+med)/E4/E14 = eager; E12 = eager; E6 native cut = eager (feature side = nnsight/
transcoders). BUT **E10 and E10-cot (§8) ran stock SDPA** ("native-default attention
resolving to SDPA"), so the universal wording "All language-model interventions reported here
use stock eager attention" (App C; §10) is false for §8. SDPA is still stock/outside the
defect, so the safety-relevant "outside that defect" claim survives. See fix B.

(d) No retracted result used as positive evidence — CONFIRMED:
 - E5 Mamba (C_l,H_l) four-quadrant certificate: NOT used; Table 4 lists Mamba strict
   signature = "no"; §6.3 states no LM cell passes and the only clean instance is diffusion.
 - Qwen3-30B in-forward: appears only as a §10 limitation (certificate did not survive the
   isolated cut) — negative framing, correct.
 - E2b interchange-only necessity: reported in §6.2 as a corrected same-day misreading after
   the distance-metric fix (E1c), not as positive evidence.
 - "15/32": absent. §8 uses 19/32 (swap) and 26/32 (removal) from the repaired E10 rerun.

## Top 10 fixes by severity

1. **(B, med) §10 + Appendix C overclaim "ALL language-model interventions use stock eager
   attention."** E10 / E10-cot (§8, computed intermediate state) ran stock SDPA, not eager.
   Fix: restrict the sentence (e.g. "all store/mediation/read interventions use eager; the
   §8 arithmetic cells use stock SDPA — both are outside the wrapper defect").
2. **(A, med) Appendix A E11 row model is wrong.** Lists "Qwen2.5-1.5B"; the cited source
   FINDINGS-E11-computed-object.md is **SmolLM2-1.7B, 24 layers** (n=45; profile ends L23;
   necessity peak L17 0.35). Correct the model (and the §8 "computed-object cell" is SmolLM2).
3. **(C/#36, low-med) §5 identity "graph's own top features ... move the answer away by
   −0.03 to −0.19."** Identity range in the source is −0.03 to −0.14; −0.19 is the COLOR
   top-50 (unfrozen). Fix to −0.14, or make the sentence cover identity+color explicitly.
4. **(G, low) Verify reference [Geiger 2023] arXiv:2301.04709.** Only body reference absent
   from the API-verified space-and-time-circuits list; confirm ID/title before submission.
5. **(D, low) §4 exact-join "within 0.03 of clean."** True on forced-choice-over-alphabet
   (token join ≡ oracle), per E12; the source carries audit caveats (dose confound; the
   "exact beats soft" claim untested; not full-vocabulary). Add the forced-choice qualifier.
6. **(E/#49, low) §7.2 "at most 0.18 of necessity per layer in the distributed stores."**
   0.18 is Gemma's best 3-adjacent window; best single layer is 0.08 and Qwen's best-3 is
   0.23. Reword ("no three adjacent layers above 0.23") to avoid "per layer."
7. **(F, low) §5 color "0.31 to 0.42" tied to "every feature at every position and layer."**
   0.42 is subject-position-only / all-layers; the every-position all-layers value is
   0.32/0.34. Minor attribution slip; align wording with the E6 Amendment table.
8. **(H, low) §4 "coreference panel ... rate 0.00."** E18 explicitly reports query-bucket
   0.00 for synthetic identity/color; a distinct "coreference" panel at 0.00 is not clearly
   located in the E18 FINDINGS (may be in the natural runner). Confirm the source cell.
9. **(#46, low) §7.1 "0.87 to 0.83" surviving-state fraction (2.8B identity).** Not present
   in results/summary.json; stated in FINDINGS/report text. Add the exact per-run receipt
   locus so the number is traceable (the 3/6 positive-margin claim IS in summary/FINDINGS).
10. **(#53, low) §8 two-step "0.037 and 0.015 nats."** E10-cot table reports Δ 0.04 / 0.02;
    0.037/0.015 are the un-rounded values. Harmless, but cite the raw record so the extra
    precision is reproducible.

## Bottom line
Numerically the paper is in strong shape: of ~58 distinct checks, ~50 are exact MATCH,
~7 are benign rounding, and only **two are substantive MISMATCHes** (B: eager-attention
overclaim covering the SDPA §8 cells; A: E11 model mislabeled Qwen for SmolLM2). One
reference (Geiger 2023) needs independent verification. All four retraction guards hold; no
retracted result is used as positive evidence; both generated figures (4,5) are faithful to
source. Remaining items are low-severity wording/attribution tightenings.
