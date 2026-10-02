# Round 1 — Evidence audit: rounding-placement/paper.md

Reviewer: Claude (Opus 4.8), 2026-10-02. Method: opened every cited JSON and re-derived each
numeric claim (no model runs). Metric used by the paper for gradient error is **`dq_fro.max`**
(worst-layer Frobenius relative error) in §7 and GFPA, **`median_param_rel`** in Table 6, and
**`global_rel`** in the §8.2 log-polar line — this switching is correctly sourced but undocumented.

Verdict: **~50 claims checked, the large majority MATCH exactly.** The GFPA panel (24 cells +
ablations), Table 6 (20 cells), Table 2/3, all Q4 tables, rotation-swamping, the FP32 cliff on three
models, SAR, and the ring probe all reproduce to the stated digits. A small number of secondary
numbers have metric/source problems; none touches the five headline results except item 1 (a
sub-claim of §7.2).

## Claim → source → value → class

| Claim (paper) | Line/§ | Source key | Found | Class |
|---|---|---|---|---|
| 35/64 pairs ω<2^-9; FP16 28 | §3.2 | rotation-swamping `pairs_below_half_ulp_*` | 35 / 28 | MATCH |
| key err 0.0020/0.031/0.10/0.43 @1/64/256/1024 | §3.2 | rotation-swamping traj | .00201/.0307/.1019/.4333 | MATCH |
| random-walk 0.036; FP16 0.054; FP32 2e-5 @1024 | §3.2 | same | .0361/.0539/1.97e-5 | MATCH |
| BF16 twiddle rel 1.17, norm 1.61 | §3.2 | same | 1.169 / 1.609 | MATCH |
| ~10% slow-pair / ~98% fast-pair @256 | §3.2 | achieved_rotation_frac | 10.3% / 98.2% | MATCH |
| Re-rotate +1.4/+27/+49% (8.170/22.090/20.692) | Tab2 | review-fixes f6/f7 | 8.170/22.090/20.692 | MATCH |
| Excess NLL +.0142/+.241/+.400 + CIs | Tab2 | review-fixes | identical | MATCH |
| swamped-pair fix 103/101/97% | §3.3 | review-fixes derive | 102.8/100.5/97.2 | MATCH |
| unswamped 41/20/27%; γ6 88/76% | §3.3-4 | review-fixes | 41.2/19.8/26.5; 87.8/76.2 | MATCH |
| swamped carry 77/75% γ²; 55%; top6 74/70% | §3.4 | gamma_slow_overlap | .773/.752/.547/.744/.696 | MATCH |
| block Δ≥16 CI incl 0 both models | §3.4 | review-fixes d16/128/512 | all CIs span 0 | MATCH |
| Δ=512 raises pristine ~0.05 NLL | §3.4 | review-fixes ref_ppl | ln(8.453/8.055)=.048 | MATCH |
| BF16 twiddle 254/406/2501 | §3.4 | paper53 (406,2501); 254=companion | 405.8/2500.8 | MATCH (254 unchecked, companion) |
| FP32 cliff Tab3 (22.6/85.0/1467.6/6304.9) + int/fp64 flat; ref 9.472 | Tab3 | free-wins-offset | 22.649/85.02/1467.6/6304.9; pristine 9.4716 | MATCH |
| Qwen3-0.6B 20.4→28.8→21,782; 1.7B 15.7→20.3→798,643 | §4 | paper63 | 20.43/28.81/21782; 15.77/20.30/798643 | MATCH |
| Qwen2.5 bias 316, resid 1.08, 74% | §5.1 | calibration_stats[0] | 316/1.080/.740 | MATCH |
| Q4 6135→268.4→**8.194 (+1.8%)**→8.104 | Tab4 | free-wins-quality arms | 6135.3/268.4/8.194/8.104 | ROUNDING (8.194/8.055=**+1.73%→+1.7%**, not +1.8) |
| Qwen3-0.6B gain 96.5/med 2.28; 45% SNR<1; 8 ch=82% | §5.2 | bithacks diag l0 | 96.5/2.281/.450/.820 | MATCH |
| gain range "3–42×" | §5.2 | gamma_max_over_median | [2.44, 42.16] | ROUNDING (low end 2.44, not 3) |
| Qwen3 Q4 411.9/126.7→17.465(+0.6); 115.1/53.3→13.943(+0.5) | §5.2 | paper61 | identical | MATCH |
| "within 0.4%" / "0.4–0.6%" | abs,§5.2 | paper61 q4c vs q4c_v4b | q4c=+0.6/+0.5; 0.4 only from untabulated q4c_v4b (+0.36) | WRONG-CONDITION (minor) |
| γ max/med ρ=+0.83 p=4e-8; calib −0.33 p=.09 | §5.2 | companion paper.md:683 | identical | MATCH (companion) |
| Immutable 8.057 vs 8.055; FP64 8.054; +0.0003[−.0006,+.0009] | §6 | free-wins-quality | 8.0572/8.0551/8.0545; +.00027 CI match | MATCH |
| ring beats FP32 by −0.0140[−.0191,−.0086] | §6 | free-wins-quality pair | −.01395 CI match | MATCH |
| fused pre-RoPE 3.0× (7.44 vs 22.46 ms) @32k | §6 | free-wins-speed | 22.46 / 7.43 → 3.02× | MATCH |
| page-frame Q4 8.6% faster vs best BF16 @32k | §6 | bithacks-speed whole_model | 6.79 vs 7.43 = 8.6% | MATCH |
| bit-hack 1.30× over table; **17× lower err** @128k | §6 | bithacks-speed one_layer 128k | 208.9/160.5=1.30×; err 0.01151/0.00090=**12.8×** | 1.30× MATCH; 17× = MISMATCH/VERIFY (companion §6.8, diff metric) |
| dQ 1.0/4.0/50.5/142.2% (160m); 111.2 (410m); dK 218% | §7.1 | ladder flash dq_fro.max/dk_fro.max | .0099/.0401/.5055/1.4224; 1.1116; 2.181 | MATCH |
| centering 142.2→20.8 (160m); 111.2→9.5 (410m) | §7.2 | ladder flash_center dq_fro.max | .2075 / .0953 | MATCH |
| **Qwen2.5-1.5B 29.6%→0.67% (44×)** | §7.2 | final-qwen25-1.5b-t512 | flash fro.max=.2957(29.6); flash_center **fro.max=.0097(0.97%, 30.5×)**; med.median=.0068 | MISMATCH (before=worst-layer, after=median; consistent = 0.97%/30.5×) |
| score-grad cast alone ≤2.7% | §7.2 | ladder cast_only dq_fro.max | 160m max 2.67% (qwen25 8.3%, exception) | MATCH (pythia) |
| key mean ~800× / ~2,400× | §7.2 | "replay notes" | not in committed JSON (stats arm lacks it); blog says 476× | UNSOURCED-in-JSON (paper hedges; low) |
| GFPA Tab5 (all 24 cells: 131.7/92.9/12.2/27.9/2.9/1.9 … GFPA 13.5/7.5/1.44/1.02/0.96/1.08); bit-ident 0=8M | Tab5 | gfpa-* dq_fro.max | every cell matches; gfpa@0==gfpa@8M | MATCH |
| no base→131.8; no conserve (Qwen2.5)→23.9 | §7.3 | gfpa nobase/noconserve | 131.83 / 23.88 | MATCH |
| backward-only 0.6–0.9% | §8.1 | ea2-loc @bwd global_rel | .55/.92 (qwen25 **0.52**) | ROUNDING (low end 0.52, not 0.6) |
| Table 6 (20 cells: BF16 2.0/31.8/203.8/42.7; +B 1.1/1.4/11.8/3.0; FP8 56.1/65262/330746/1980961; MXFP8…; +B…) | Tab6 | ea-pythia160m/410m median_param_rel | every cell matches | MATCH |
| row sums ~5e-4 → ~3e-17 | §8.2 | ea dS_rowsum before/after | 3.8e-4→2.5e-17 (step-dep up to 1.2e-2) | MATCH (approx) |
| log-polar 12.8% vs BF16 2.6% (Qwen3); 0.7% Pythia16k | §8.2 | ea2-loc spf16g_B/bf16_B **global_rel** | 12.8 / 2.61 / 0.68 | MATCH (note: global_rel, not Tab6's metric) |
| 8-bit log-prod bit-identical 12/12; fp32/bf16 never | §8.3 | two-domain note Test 3 | yes 12/12 vs no | MATCH |
| log accumulator ~95× slower than BF16 TC | §8.3 | cited "two-domain note speed" | number NOT there; blog note: 1 vs **92.6** TFLOP/s = 92.6× | UNSOURCED-in-cited-file + ROUNDING (92.6×, not 95×) |
| SAR 29× (174.7→5.95 ms), −39 dB; FP32 peak −29 dB | AppB | sar-4080-v2 | 174.70/5.946/29.4×/−39.3; LEO peak −29.3 | MATCH (uses corrected v2; v1 flagged INVALID, not cited) |
| θ=n·f n=1e13: FP32 noise, FP64 8e-4, ring exact | AppB | FINDINGS ring table | 3.14 / 7.7e-4 / 0 | MATCH |
| All 5 figure paths + ea2/ea3 sources exist | §Figs | filesystem | all present | MATCH |

## Top-10 fixes (by severity)

1. **§7.2 "Qwen2.5-1.5B 29.6% → 0.67% (44×)" is a metric mismatch.** 29.6% is worst-layer
   (`flash dq_fro.max`); 0.67% is the *median* layer (`flash_center dq_med.median`=0.677%). The
   consistent worst-layer centered value is **0.97%** (`flash_center dq_fro.max`), i.e. **30.5×**,
   not 44×. Fix to "29.6% → 0.97% (30×)" (or state the metric). Also in README ledger.
2. **§6 "17× lower rotation error" (bit-hack) not reproduced.** bithacks-speed.json gives
   table/bithack `max_abs_err` = 0.01151/0.00090 = **12.8×**. The 1.30× speed is correct. Verify the
   17× against companion §6.8's rotation-error definition or change to ~13×.
3. **§8.3 "~95× slower" is miscited and slightly high.** The number lives in the blog note
   (1 vs **92.6** TFLOP/s = 92.6×), not the cited "two-domain note speed table" (which only says
   "SPF kernels measured slower" / "SPF-64 add 60–100×"). Fix source and round to ~93×.
4. **§5.1/README Q4 bias "+1.8%" should be +1.7%** (8.194/8.055 = +1.73%). Two places.
5. **Key-mean ratio (~800×/~2,400×) is not in committed JSON.** The `stats` arm of ladder-pythia
   has no key-mean/spread ratio; it rests on uncommitted "replay notes" and the blog still says
   476×. Paper hedges honestly, but either commit the measuring script output or keep it out of the
   body. (Low, already down-weighted.)
6. **"within 0.4%" (abstract/§5.2) uses an untabulated arm.** Tabulated calibrated Q4 is +0.6%/+0.5%
   (`ringpre_q4c`); 0.4% only via `ringpre_q4c_v4b` (+0.36%). Either tabulate v4b or say "within
   ~0.6%".
7. **Document the gradient-error metric switch.** §7/GFPA = `dq_fro.max`, Table 6 = `median_param_rel`,
   §8.2 log-polar = `global_rel`. All sourced correctly, but a reader cannot tell; add one sentence.
8. **§8.1 "0.6–0.9%" low end is 0.52%** (qwen25 `@bwd`). Say "0.5–0.9%".
9. **§5.2 gain range "3–42×" low end is 2.44×** (`gamma_max_over_median`). Say "~2.4–42×".
10. **Reference [12] arXiv 2609.34272** is future-dated and mirror-sourced; it appears only as the
    author's own citation in ladder-pythia meta (no independent identity in workspace). Paper already
    flags it — keep the flag, verify before submission. (SageAttention 2410.02367, SageBwd 2505.11594,
    LNS-Madam 2106.13914, nGPT 2410.01131 are standard IDs; ref [17] FP8 Formats still needs an ID.)

Nothing fabricated: every headline (swamping fix, 2^24 cliff, Q4 affine, Table 6 B(x), GFPA panel,
SAR) checks out to the stated digits against raw run output.
