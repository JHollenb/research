# Round-1 response — "Where You Round Beats How Many Bits" (was "Rounding Placement")

Author response to the three round-1 reviews (`round1-numerics-reviewer.md` 5/10; `round1-evidence-audit.md`; `round1-priorart-clarity.md`). All changes are in `paper.md` / `README.md`; two figures added under `figures/`. No new experiments were run (the training continuation is left as a marked placeholder). Every arXiv ID added was verified live via web search this session.

Legend: ✅ done · ◑ partial / as far as possible without experiments · ⛔ not done (reason).

## A. Metric & number corrections (evidence audit items 1–9; numerics reviewer #4)

| # | Reviewer point | Change | Status |
|---|---|---|---|
| 1 | §7.2 "29.6%→0.67% (44×)" mixes worst-layer and median | Now "29.6%→0.97% (30×)", consistently worst-layer (`flash`/`flash_center` `dq_fro.max`). Fixed in §7.2 body, Appendix A, README ledger. | ✅ |
| 2 | §6 bit-hack "17×" not reproduced | Changed to "12.8× lower maximum-absolute rotation error (0.00090 vs 0.01151 at 128k)" with the `bithacks-speed.json` source inlined. | ✅ |
| 3 | §8.3 "~95×" miscited/high | Now "~93× (1.0 vs 92.6 TFLOP/s)", source corrected to the two-domain-note speed table. | ✅ |
| 4 | Q4 bias "+1.8%" → +1.7% | Fixed in §5.1 table and README. | ✅ |
| 5 | Key-mean ratio (~800×/2,400×) not in committed JSON | Kept but explicitly flagged in-text as "not in the committed JSON, so we down-weight it and lead with the gradient error"; also in Limitations. | ✅ |
| 6 | "within 0.4%" uses an untabulated arm | Now stated as 0.6% (calibrated K) and 0.4% (calibrated K+V, `ringpre_q4c_v4b`), both tabulated in §5.2 text; abstract says "within 0.6–1.7%". | ✅ |
| 7 | Document the gradient-error metric switch | One sentence added in §2.3 naming the three statistics (worst-layer `dq_fro.max`; median per-parameter; norm-weighted global) and which is primary; §8.1 and §8.2 now say which metric they report. | ✅ |
| 8 | §8.1 "0.6–0.9%" low end is 0.52% | Now "0.5–0.9%". | ✅ |
| 9 | §5.2 gain "3–42×" low end 2.44× | Now "2.4–42×". | ✅ |

## B. The log-polar "5×" headline (numerics #4; evidence item 55; priorart)

| Point | Change | Status |
|---|---|---|
| "16-bit log-polar 5× worse" is metric-selected (`global_rel`); 2.1× on the paper's main metric | Retired the 5× headline. Abstract no longer cites it. §2.3 and §8.2 now report **5.2% vs 2.4% = 2.1× (median per-parameter, primary)** and note **4.9× on the norm-weighted metric** that the outlier channels dominate, explicitly. Promoted swamping's magnitude-independence to the lead "frame beats bits" evidence. | ✅ |

## C. FP8 baseline is a strawman (numerics #2, #5; priorart)

| Point | Change | Status |
|---|---|---|
| Don't lead with per-tensor E4M3/E5M2 "300,000%/millions %"; frame around block-scaled FP8 + FP32 accumulation (DeepSeek-V3); state honestly MXFP8+B(x) (41–76%) is only ≈ plain BF16 | §8.2 retitled and rewritten: table reordered so **block-scaled MXFP8 is the fair FP8 baseline** and naive per-tensor is a labeled bottom row "shown only for contrast". New text states plainly: block-FP8+B(x) recovers to ≈ plain-BF16 error (41.0% vs 42.7% on 410m), far from BF16+B(x) (3.0%); **"we do not claim B(x) fixes FP8 training."** Abstract drops the "past 300,000%" line. New Fig 6 bar chart makes this visual. DeepSeek-V3 [18] cited in §2.3, §8.2, §9. | ✅ |

## D. Thesis precision — split "frame" from "range" (numerics #1, #5; priorart #1,4)

| Point | Change | Status |
|---|---|---|
| "Frame beats bits" bundles invariant-removal (real unifier), integer phase, conservation projection; the 2^24 cliff is an integer-*range* limit, not a frame one — category slip | Thesis paragraph rewritten to name the **three mechanically distinct legs**: invariant removal (the unifier, repairs 3/4), integer phase (a *range* fix, §4), conservation projection (second-order, §7.2). §2.3 keeps the 2^24 result explicitly separate ("a range, not a mantissa, story… the one leg that is honestly a bit-count story — of the integer field"). Swamping's magnitude-independence promoted to the lead. | ✅ |
| Pick an accurate title | Adopted reviewer option A: **"Where You Round Beats How Many Bits: One Mechanism Behind Four Low-Precision Transformer Failures"**; subtitle "Remove the invariant first…". | ✅ |

## E. Prior art (numerics #2, #3; priorart #2, #7)

| Missing / under-credited | Change | Status |
|---|---|---|
| SmoothQuant (2211.10438), AWQ (2306.00978) — per-channel gain migration = §5.2 | Added [19], [20]; §5.2 now states it is "exactly SmoothQuant's migration and AWQ's salient-channel scaling, applied to the pre-RoPE KV cache"; §1 and README echo it. | ✅ |
| DeepSeek-V3 FP8 (2412.19437) — the real FP8 baseline | Added [18]; drives the §8.2 reframe (C above) and cited in §9. | ✅ |
| FlashAttention / FA2 / FA3 (2205.14135 / 2307.08691 / 2407.08608) — replayed, never cited | Added [21–23], named in §9. | ✅ |
| "Is Flash Attention Stable?" (2405.02803) — forward numeric deviation | Added [24]; §8.1 credits its order-of-magnitude forward-deviation finding as consistent with our forward-dominance result. | ✅ |
| FP8-LM (2310.18313); Unit Scaling (2303.11257); μP / Tensor Programs V (2203.03466) | Added [25–27], engaged in §9 (unit scaling / μP = "pick the coordinates at init", the same idea at a different site). | ✅ |
| Contrast Wang 2411.13476's first-token mechanism | §9 now contrasts explicitly: "Wang blames which token (first-token/AnchorAttention); we locate which channels (ω<2^-9) and which range (2^24)." | ✅ |
| Sharpen delta vs [12]; drop the "mirror/verify" hedge; credit its forward-FMA finding | [12] confirmed real (Chen et al.) → hedge withdrawn in §10, refs, README. §7.2/§8.1/§9 now credit that [12] itself traces the blowup to a term ∝ mean key (and notes a forward-pass FMA cause), and state our narrow delta: same object, removed at its forward source (SageAttention smoothing) rather than via backward GProj. | ✅ |
| Split SageAttention3 vs SageBwd refs | Verified: SageBwd is introduced *in* SageAttention3 (2505.11594); no separate 2603.02170. [14] relabeled "SageAttention3 … introduces SageBwd". | ✅ |
| FP8-Formats ID (Micikevicius) | Verified 2209.05433; [17] now carries the link (hedge removed). | ✅ |

## F. Clarity (priorart #3,5; numerics #6)

| Point | Change | Status |
|---|---|---|
| Abstract ≤200 words, sentence 1 = thesis | Rewritten; **198 words**; sentence 1 is "Where you round… matters more than how many bits." | ✅ |
| Define "gauge" once | Added one sentence at the top of §2.1 (gauge = a direction of exact invariance; fixing it = choosing a representative). | ✅ |
| Re-gloss GFPA at first substantive use (§7.3) | Done: "GFPA (gauge-fixed phase attention) … fixing the gauge of the stored keys in one operator." | ✅ |
| Define or drop SPF | No bare "SPF" appears in the body (grep-confirmed); the format is called "log-polar" and defined once in §2.2. | ✅ |
| Inline load-bearing "companion §x" numbers | The headline serving numbers (8.057 vs 8.055, 98,972 evictions / zero rewrites, 7.44 vs 22.46 ms = 3.0×, 12.8× error, 8.6%) are all stated inline; companion pointers remain only as provenance. | ✅ |
| Promote §2.3 key sentence | §2.3 now opens with a bold one-liner ("Across these failures, choosing the frame changes the error by 1–3 orders of magnitude; changing the mantissa width does not."). | ✅ |
| Cut §8.3 determinism | Condensed from two paragraphs to one short paragraph; added "deterministic reductions are also achievable with batch-invariant float kernels; the integer route is one option." | ✅ |
| Shrink / drop Appendix B SAR | Cut to 3 sentences. | ✅ |

## G. Figures (numerics #6; priorart #4,6)

| Point | Change | Status |
|---|---|---|
| §2 mechanism schematic | **New Figure 1** (`figures/mechanism-schematic.png`): invariant+content block, rounding band lands on the invariant, remove-first drops content into the band. | ✅ |
| §8.2 B(x) vs FP8/MXFP8 bar chart | **New Figure 6** (`figures/bx-vs-fp8-bars.png`): BF16 / BF16+B(x) / MXFP8 / MXFP8+B(x), Pythia-160m & 410m, median_param_rel, log scale, from the verified JSON. | ✅ |
| Both built by one matplotlib process | `figures/make_figures.py` (single run). | ✅ |

## H. Training-continuation placeholder + limitations (must-do #8)

| Point | Change | Status |
|---|---|---|
| Marked placeholder in §8 | New **§8.4** with `<!-- TODO training-continuation -->` describing the arms (realistic BF16 w/ FP32 master weights vs +B(x) vs FP32 reference, held-out loss, ≥2–3 seeds) and the kill condition. | ✅ |
| State one-step gradient error ≠ training outcome until it lands | Added in §8.4 and strengthened in Limitations (the [12] failure took ~25B tokens; a short continuation may be too short to diverge, so a null is weak). | ✅ |

## Points acknowledged but not fully closable without experiments

- **Scale ≤1.7B, single seed (numerics #3).** Still the central limitation; owed experiment 3 (one forward+backward on Qwen3-4B / Llama-3-8B) is the cheapest fix and is listed in README. ◑
- **No loss curve / "method vs diagnostic" (numerics #1,#8).** Owed experiment 1 is running; §8.4 placeholder reserves the slot, and Limitations reads the training half as diagnostic until it lands. ◑
- **GFPA "as a packaged kernel" / throughput (numerics #4).** No kernel or throughput is claimed; GFPA is presented as a gradient-accuracy result with a proxy metric, said so. ◑
- **Novelty is synthesis-level (numerics #1).** We agree and now say so plainly: the contribution is the unifying mechanism + cross-setting demonstration + the better-placed fix vs [12] + the two-family correction rule, not a new method. ◑
