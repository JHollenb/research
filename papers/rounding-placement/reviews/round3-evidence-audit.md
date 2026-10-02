# Round 3 — evidence audit (final round)

Auditor pass over `paper.md`: every headline number traced to its raw source (result JSONs,
evidence extracts, the two-domain note, factored-precision FINDINGS, and the custody audit
`research/papers/custody-audit-2026-10-02.md`). Numbers were re-derived from `results/*.json`
in-session via Python, not read from the FINDINGS prose. Read-only on the paper.

**Verdict: PASS.** All load-bearing numbers reproduce from raw files, to the stated rounding.
One provenance must-fix (§8.3 speed citation points to a table that does not exist; the number
is real but lives in a different file, and the ratio is slightly understated). A handful of
last-digit rounding nits. No smoke/killed-job number reaches a headline; no undisclosed
prereg-vs-post-hoc confusion (the two real deviations — the failed §7.4 prediction and the
step64000 preregistration ordering — are disclosed in the paper).

Status key: **PASS** (matches raw to stated rounding) · **NIT** (last-digit / wording) ·
**FIX** (source/number needs correction).

## §8.4 / round-2 training continuation (primary focus) — all re-derived from raw JSON

| Claim | Line | Source (verified) | Status |
|---|---|---|---|
| Held loss ref 3.183 / bf16 3.206 (+0.0232±0.0030) / B(x) 3.162 (−0.0205±0.0076) / mean 3.156 (−0.0266±0.0038) | 293 | `results/{full6-s1234,core4-s2,core4-s3}.json` held[-1]; recomputed exact | PASS |
| Matched-precision gap 0.044 (B(x)) / 0.050 (mean); per-order −0.039/−0.042/−0.051; ~7× cross-order half-range (0.0061) | 293 | same; gaps −0.0387/−0.0416/−0.0509, mean −0.0438; 0.0438/0.0061=7.2× | PASS |
| Gap trajectory: +0.036@100, peak +0.057@300 (max order +0.073), narrows +0.044@1000 (range .039–.051) | 295,297 | same, bf16−B(x) per step; @300 mean .0571 max .0731; @1000 .0438 range .0387–.0509 | PASS |
| Trajectory grad err bf16 148%→66% (desc .41→.84); s2/s3 end 78%/80%; B(x) 29%→8.6% (.95→.998) | 305 | `full6-s1234.json` probe global_rel/descent_eff; s2/s3 0.780/0.802 | PASS |
| Dose step64000 (n=3): bf16 +.0001/+.0041/+.0021 (mean +.0021); B(x) +.0010/+.0017/+.0007; vs +0.0232@143k (per-order +.0215/+.0271/+.0211) | 307 | `full-mid-s0,mid-s2,mid-s3.json`; recomputed exact | PASS |
| FP8: MXFP8 3.58→4.78 (desc −0.67); +B(x) min 3.26@step200 → 3.45 (+0.27 vs ref); BF16+B(x)≈3.16 | 309 | `full6-s1234.json` mxfp8/mxfp8_Bx held; true min=3.2583@t200 (FINDINGS "3.27@t100" was pre-correction) | PASS |
| Throughput ref 16.9k / bf16 15.3k / B(x) 14.0k (~8%) / mean 15.0k | 311 | `full6-s1234.json` 16883.8/15281.6/14031.4/15047.7; (FINDINGS 17.0k/15.1k corrected) | PASS |
| Custom fwd reproduces HF loss to 4e-6; 2.05M tokens | 291,309 | 1000×8×256=2,048,000 | PASS |

## §7.4 current-model Qwen3-1.7B — re-derived from raw JSON

| Claim | Line | Source (verified) | Status |
|---|---|---|---|
| Key-mean ratio worst-head 63×, median-head 2.2×, ~98% slow-pair energy | 241 | `round2/results/gauge-qwen3-1.7b.json` summary geometry: 63.44 / 2.184 / 0.9864 | PASS |
| Worst-layer dQ bf16 1.9% (FA2 2.0%) → key-mean 1.2% → B(x) 1.1% (~1.6×); dK 1.3%→1.0% | 241 | emu/flash/emu_center/emu_center_proj dq_fro.max 1.85/1.99/1.19/1.11; dK 1.26/1.03 | PASS |
| Preregistered several-fold cut did NOT occur; seq256/1.7B vs PREREG seq512/4B; 4B killed_vram ~15.4GB | 241,328 | custody "B(x) round 2"; kills 15372/15416 MB | PASS (disclosed) |

## §7.1–§7.3 gauge-leak gradients — re-derived from raw JSON

| Claim | Line | Source (verified) | Status |
|---|---|---|---|
| dQ growth 1.0/4.0/50.5/142.2% (160m); 111.2% (410m); dK 218% | 216 | `ladder-pythia.json` flash dq_fro.max; dk 218.1% | PASS |
| Centering 142.2→20.8% (160m), 111.2→9.5% (410m) | 220 | flash_center 20.75/9.53 | PASS |
| Qwen2.5-1.5B centering 29.6%→0.97% (30×) | 220 | `final-qwen25-1.5b-t512.json` flash 29.57 / flash_center 0.97 | PASS |
| Table 5 GFPA (all 6 models × 4 rows); nobase 131.8%; noconserve 23.9% | 232-237 | `gfpa-small/-qwen25-1.5b/-qwen3-*.json` dq_fro.max; 5 beat best, 1 tie | PASS |
| Qwen2.5-1.5B plain BF16 "27.9%" (Table 5, §7.3, §8.4 list, README, two-domain note) | 232 | raw = 27.847% → rounds to **27.8%** | NIT |
| Qwen2.5-0.5B mean-centering offset-8M "20.3%" | 234 | raw = 20.246% → rounds to **20.2%** | NIT |

## §8.1–§8.2 full-step / FP8 / log-polar — re-derived from raw JSON

| Claim | Line | Source (verified) | Status |
|---|---|---|---|
| Table 6 BF16 2.0/31.8/203.8/42.7; +B(x) 1.1/1.4/11.8/3.0; MXFP8 36.3/21200/67139/18106; +B(x) 16.6/20.7/76.1/41.0; per-tensor 56.1/65262/330746/1980961 | 263-269 | `ea-pythia160m/410m.json` median_param_rel; all exact | PASS |
| Backward-only 0.5–0.9% (global); forward reproduces whole error | 251 | `ea2-loc-*.json` bf16_B@bwd 0.52/0.55/0.57/0.92% | PASS |
| 16-bit log-polar 5.2% vs 2.4% median (2.1×); 12.8% vs 2.6% global (4.9×) | 273 | `ea2-loc-qwen3.json` spf16g_B 5.16/12.80 vs bf16_B 2.42/2.61 | PASS |
| Row sums ~5×10⁻⁴ → ~3×10⁻¹⁷ | 271 | `ea-pythia160m.json` dS_rowsum before 4.36e-4 / after 2.79e-17 | PASS |

## §3–§6 inference — re-derived from raw JSON

| Claim | Line | Source (verified) | Status |
|---|---|---|---|
| 35/64 pairs ω<2⁻⁹; FP16 28 | 103 | `rotation-swamping.json` 35/28 | PASS |
| Key err .0020/.031/.10/.43 @1/64/256/1024; rand-walk .036; FP16 .054; FP32 2e-5 | 105 | `rotation-swamping.json` fp32_twiddle_bf16_store traj | PASS |
| BF16 twiddle rel .1.17, norm 1.61 @1024 | 107 | bf16_twiddle_bf16_store 1.1693/1.6092 | PASS |
| Table 2 re-rotate 8.170/22.090/20.692 vs 8.055/17.363/13.868; +1.4/+27/+49%; excess+CIs | 121-123 | `review-fixes.json` f6/f7 | PASS |
| Exact swamped remove 103/101/97%; complement 41/20/27%; γ-mass 77/75%; 55% pairs; top6 74/70%; γ6-exact 88/76%; gain 2.4–42× | 125,129 | `review-fixes.json` shares + gamma_slow_overlap | PASS |
| Block Δ≥16 CI includes 0; Δ512 pristine +~0.05 | 131 | `review-fixes.json` d16/d512 | PASS |
| Table 3 cliff 22.6/85.0/1467.6/6304.9; ref 9.472; int/FP64 flat | 141-147 | `free-wins-offset.json` | PASS |
| Qwen3 cliff 20.4→28.8→21782; 15.7→20.3→798643 | 149 | `bithacks-qwen3.json` paper63 | PASS |
| Table 4 Q4 6135/268.4/8.194(+1.7%)/8.104(+0.6%) | 171-176 | `free-wins-quality.json` ring_q4post/ringpre_q4/q4b/q4c | PASS |
| Qwen3 Q4 411.9/115.1, 126.7/53.3, 17.465(+0.6%)/13.943(+0.5%); K+V +0.36%/−0.19% | 188-190 | `bithacks-qwen3.json` paper61 | PASS |
| γ layer0 96.5/2.28; 45% SNR<1; 8/1024 carry 82% | 182 | `bithacks-qwen3.json` diag qwen3-0.6b layer0 | PASS |
| Immutable 8.057 vs 8.055; FP64 ring 8.054; beats re-rotate by −0.0140 | 200 | `free-wins-quality.json` ring_int32/ring_fp64/rerotate | PASS (point); CIs not in file |
| Qwen2.5 bias 316 / residual σ 1.08 / 74% / step ~45 | 165 | not in cited files; traces to **companion paper.md L467** (its own calibration) | NIT (uncited here) |
| Fused 3.0× (7.44 vs 22.46 ms@32k); bit-hack 1.30×@128k; 12.8× lower max-abs (0.00090 vs 0.01151) | 204 | `free-wins-speed.json` 22.461; `bithacks-speed.json` trig32 160.5µs/.000902 vs table 208.9µs/.011507 | PASS |

## §8.3 / Appendix B

| Claim | Line | Source | Status |
|---|---|---|---|
| Integer accum bit-identical 12/12 layers; fp32/bf16 never | 285 | two-domain note Test 3 "yes (12/12)" | PASS |
| Log accumulator ~93× slower (1.0 vs 92.6 TFLOP/s) "[two-domain note, speed table]" | 285 | **number NOT in two-domain note (no speed table).** Real value in `spf-native-boundary/results/speed-v1.json` part_a[2] (job-141c554fb988): bf16_tc 92.62, lns8_exact_int 0.9715 → ratio **95.3×**, not 93× | **FIX** |
| SAR factored 29× (174.7→5.95 ms), −39 dB; FP32 destroys sat image | 394 | factored-precision FINDINGS v2 (job-10c2e0f5ac5b) 174.7/5.95/29.4×/−39.3 dB | PASS |
| Ring θ=n·f @n=1e13: FP64 off 8×10⁻⁴, ring exact | 394 | FINDINGS phase-law table n0=1e13: fp64 7.7e-4, ring 0 | PASS |

## Custody / prereg / smoke hygiene
- Custody audit (`custody-audit-2026-10-02.md`, "B(x) training continuation" + "B(x) round 2")
  independently PASS; I re-derived its headline table from raw and it matches. Its own nits
  (canonical job `job-fec87d0ed93a`, throughput last-digits, FP8-min metric) are all applied in the paper.
- Canonical seed-1234 job is the committed `full6-s1234.json` (job-fec87d0ed93a), not the
  bit-identical `job-05070b1d9ab9` — correctly used.
- No smoke/killed/lrsweep number reaches a headline (`fp8smoke`, `smoke1`, `full-s0/s1`,
  `lrsweep`, `mid-*` early runs are excluded from the headline tables). The Qwen3-4B VRAM kill is
  reported as a hardware-scope limit, not a null — correct.
