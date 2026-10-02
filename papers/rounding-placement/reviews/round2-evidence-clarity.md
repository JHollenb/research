# Round 2 — combined evidence + clarity audit: rounding-placement/paper.md

Reviewer: Claude (Opus 4.8), 2026-10-02. Method: re-derived each corrected/new number from
the raw JSON (`cat`/`python3 -c`), opened all five new/§8.4 PNGs, spot-checked 4 citations live.
No model runs. Verdict: **evidence solid — all headline numbers reproduce to stated digits; one
figure-caption FAIL and a few attribution/rounding nits remain.**

## A. Round-1 top-10 fixes (did each land + match source JSON?)

| # | Round-1 fix | In paper? | Source re-derived | Status |
|---|---|---|---|---|
| 1 | 29.6%→0.67%(44×) → 29.6%→0.97%(30×), worst-layer | §7.2 L220, README L49, AppA L360 | final-qwen25-1.5b-t512: flash dq_fro.max .2957, flash_center .0097 → 30.5× | PASS |
| 2 | bit-hack 17× → 12.8× (0.00090 vs 0.01151 @128k) | §6 L204 | bithacks-speed: table .011507 / trig32_magic .000902 = 12.76× | PASS |
| 3 | ~95× → ~93× (1.0 vs 92.6 TFLOP/s) | §8.3 L279, README L63 | sourced to two-domain note (not JSON) — text landed; JSON uncheckable | PASS (text) |
| 4 | Q4 bias +1.8% → +1.7% | §5.1 L175, README L19 | free-wins-quality: 8.1941/8.0551 = +1.73% | PASS |
| 5 | key-mean ratio not in JSON → hedge | §7.2 L220, §10 L320 | hedge present ("~800×/~2,400× … not in committed JSON") | PASS |
| 6 | "within 0.4%" untabulated → tabulate | §5.2 L192 (0.6%K/0.4%K+V), abs "0.6–1.7%" | q4c +0.6/+0.5; q4c_v4b +0.36/−0.19 | PASS |
| 7 | document 3-metric switch | §2.3 L83 names all three, primary=median-param | — | PASS |
| 8 | "0.6–0.9%" low end .52% → "0.5–0.9%" | §8.1 L245 | ea2-loc bf16_B@bwd global_rel: qwen25 .0052, pythia .0057/.0092 | PASS |
| 9 | gain "3–42×" → "2.4–42×" | §5.2 L182 | bithacks-qwen3 gamma_max/median: Qwen3-0.6B top=42.3 (L0 96.5/2.28) | PASS* |
| 10 | ref [12] mirror hedge → withdrawn | §10 L322, refs L400, README | WebSearch: 2609.34272 REAL (Chen et al., 28 Sep 2026, 28pp) | PASS |

\*L9: paper's stated Qwen3-0.6B range top (42.3) matches; a broad scan of all gamma/median keys
shows some ratios <2.4 (q-norm/other layers), so "2.4" is the specific key-norm-channel low end
the round-1 audit cited — acceptable but selective.

## B. New-since-round-1 numbers (§8.4, FP8 reframe, abstract)

| Claim | Line | Source re-derived from JSON | Status |
|---|---|---|---|
| Held loss ref 3.183 / bf16 3.206 / B(x) 3.162 / mean 3.156 | §8.4 L287 | full6-s1234+core4-s2/s3: 3.1827/3.2059/3.1622/3.1561 | PASS |
| Δvs-fp32 +0.023±.003 / −0.021±.008 / −0.027±.004 | L287 | recompute +0.0232±.0030 / −0.0205±.0076 / −0.0266±.0038 | PASS |
| matched-prec gap 0.044 (mean 0.050); per-order −.039/−.042/−.051 | L287 | B(x)−bf16 −0.0438; mean −0.0499; −.0387/−.0416/−.0509 | PASS |
| traj grad err bf16 148→66% (0.41→0.84); B(x) 29→8.6% (0.95→.998) | L293 | probe global_rel 1.4825→.6563, .2883→.0863; desc_eff match | PASS |
| mid step64000: all 4 arms within 0.001 nats; bf16 err ~30%, B(x) ~20× | L295 | ref 2.9562/bf16 .9563/B(x) .9572/mean .9561 (range .0011); mid bf16 t0 global .2923, median 21%→1.1%=19× | PASS (range 0.0011; "~30%"=29% global) |
| FP8: MXFP8 3.58→4.78; +B(x) →3.27 then 3.45 (+0.27 vs ref) | §8.4 L297 | 3.5806→4.7806; +B(x) min 3.2583@t200 (3.2724@t100) → 3.4501 (+0.2674) | PASS (min is 3.26, not 3.27) |
| Table 6 / Fig 6: BF16 204→11.8% (160m), 43→3.0% (410m) | §8.2 L260, Fig6 | ea-pythia160m r2 bf16 2.0376/bf16_B .1182; 410m .4266/.0303 | PASS |
| MXFP8-block 67,139/18,106%; +B(x) 76.1/41.0%; naive 330,746/1,980,961% | §8.2 L261-263, Fig6 | mxfp8 671.39/181.06; mxfp8_B .7613/.4098; fp8 3307.46/19809.6 | PASS |
| Throughput bf16 15.3k / B(x) 14.0k (~8%) / mean 15.1k / fp32 17.0k | README L61 | 15282/14031(8.2%)/15048/16884 | PASS* (mean=15.0k, fp32=16.9k) |

Custody audit (custody-audit-2026-10-02.md "B(x) training continuation" section, which DOES exist,
appended): verdict **PASS**, headline numbers reproduce exactly; 5 minor nits (provenance pointer,
mid-metric label, throughput last-digit, single-order main figure, context numbers out-of-scope).
Consistent with my recompute.

## C. Clarity / internal consistency

| Check | Status |
|---|---|
| Abstract ≤200 words, thesis first | PASS — 195 words; sentence 1 = thesis |
| gauge/swamping/B(x)/GFPA/log-polar defined before use | PASS (gauge §2.1 L46; GFPA re-glossed §7.3 L226; no bare "SPF" in body) |
| 8 figures exist, referenced in order 1→8 | PASS (all files present; L67/109/151/206/247/269/273/289) |
| Fig 1,6, dose-response, 6-arm captions match PNG content | PASS (opened all) |
| **Fig 8 caption "Three data orders averaged"** | **FAIL** — bx-training-main.png is md5-identical to single-order bx-training-s0.png (data-seed 1234); shows one order, not a 3-order mean/spread |
| Prior-art landed: SmoothQuant/AWQ/DeepSeek-V3/FA/FA-stable/FP8-LM/UnitScaling/μP; Wang contrast | PASS (§5.2, §9; refs [17-27]) |
| Citation IDs correct (spot-check) | PASS — 2211.10438, 2306.00978, 2209.05433, 2609.34272 all verified live |
| Primary metric used consistently | PARTIAL — 3 metrics declared in §2.3; headline 204→11.8% (median-param) vs §7/GFPA 142%/13.5% (worst-layer dq_fro) differ, but labeled |
| 204%/11.8%, 0.044 nats, 35/64, 8.057/8.055, ±% consistent across abstract/§/README | PASS |

Note: round-1 response claimed "no separate 2603.02170" for SageBwd — WebSearch shows 2603.02170
("SageBwd: A Trainable Low-bit Attention") DOES exist. Paper doesn't cite it, so harmless, but the
response's parenthetical is wrong.

## D. Ranked remaining fixes

1. **(FAIL) Fig 8 caption.** `bx-training-main.png` = single data order (seed 1234), byte-identical
   to `bx-training-s0.png`; caption L291 says "Three data orders averaged." Either regenerate the
   figure as the 3-order mean±spread or change the caption to "one data order (seed 1234); the
   3-order means are in §8.4 text." (Custody nit #4.)
2. **(MED) Abstract/§1 attribute the 2-op number to 1 op.** Abstract L19 and §1 L36 say "subtracting
   the per-head key mean takes … 204% to 11.8%", but §8.2 L265 (and README) say 11.8% is *two* ops
   (key-mean + GProj); Table 6 has no mean-only one-step column. Either add a mean-only one-step
   number, or reword to "B(x) (key-mean removal + row-sum projection)".
3. **(LOW-MED) Abstract mislabels the 1.7%.** "a per-channel gain correction brings 4-bit keys within
   0.6–1.7%" — 1.7% is the Qwen2.5 *additive-bias* fix (§5.1), not a gain correction; only 0.6% is
   the Qwen3 gain correction. Say "affine (bias/gain) correction".
4. **(LOW) FP8 min loss.** §8.4 L297 "falls to 3.27" — true min is 3.26 (t=200); 3.27 is t=100.
5. **(LOW) README throughput last-digits.** mean-only 15048→"15.0k" not 15.1k; fp32 16884→"16.9k"
   not 17.0k (L61). (Custody nit #3.)
6. **(LOW) §8.4 "within 0.001 nats of each other"** — true spread is 0.0011 (B(x) 2.9572 vs mean
   2.9561); "within 0.001 of ref" is exact. Trivial.

Nothing fabricated. Every headline (swamping, 2^24 cliff, Q4 affine, Table 6 B(x), FP8 reframe,
GFPA panel, §8.4 loss benefit) reproduces to the stated digits from the committed JSON.
