# Where You Round Beats How Many Bits: One Mechanism Behind Four Low-Precision Transformer Failures

[Full paper](paper.md) · Jacob Hollenbeck · draft 2026-10-02 (round-1 reviews addressed)

The author's third paper. It merges two measured programs — a streaming-inference study of rotary KV caches (the "PhaseLock / rotation-swamping" line) and a training-numerics study of attention gradients (the "gauge leak / boundary-operator B(x) / exact-accumulation" line) — into one claim.

## The thesis (tested, and split after round 1)

The task proposed *"low-precision error is dominated by where rounding is placed relative to the model's coordinates/gauge; choose coordinates before rounding and restore the exact law at the boundary."* It holds, but round-1 review (correctly) pushed us to split one coat into three mechanically distinct legs:

> **Where you round, relative to a transformer's exact symmetries, matters more than how many mantissa bits you round to.** The single *unifying* mechanism is swamping: each symmetry hides a large invariant inside a stored value, the model depends only on the content, and rounding in native coordinates spends the mantissa on the invariant. The one fix that unifies is **remove the invariant in high precision before rounding** (it repairs three of the four failures and is one operation across them). Two companion operations complete the recipe where needed: **carry positional phase as an exact integer** (a distinct *range* fix, §4), and **restore the conservation law after rounding** (a second-order finishing step, §7.2).

What changed from the pre-review draft. The old framing filed the FP32 2^24 cliff under "frame beats bit width." A reviewer flagged that a 24-bit integer field running out at 2^24 *is* a bit-count limit (of the integer field, not the mantissa). The paper now keeps that leg explicitly separate as a *range* result, promotes the magnitude-independence of swamping (the cleanest "frame, not bits" fact) to the lead, and reports the log-polar "more bits can be worse" result on the consistent primary metric (2.1×, not the metric-selected 5×). Title changed to match (per the reviewers' suggested option A).

## The five headline results

1. **Rotation swamping.** One-position BF16 re-rotation freezes the 35 of 64 rotary pairs with ω < 2^-9; cost +1.4%/+27%/+49% perplexity (Qwen2.5-1.5B / Qwen3-0.6B / 1.7B); keeping only those 35 pairs exact removes 97–103%. `evidence/rotation-swamping.json`, `evidence/review-fixes.json`.
2. **FP32 position cliff.** FP32 rotary angles collapse at exactly 2^24 on three models; integer phase and FP64 stay flat past 2^32. `evidence/bithacks-qwen3.json`, `evidence/free-wins-offset.json`.
3. **Affine correction before 4-bit keys (SmoothQuant in the KV cache).** Removing the Qwen2.5 key bias takes Q4 keys 6,135 → 8.194 ppl (+1.7%); per-channel gain calibration brings Qwen3 Q4 within 0.6% (K) / 0.4% (K+V). `evidence/free-wins-quality.json`, `evidence/bithacks-qwen3.json`.
4. **Training blowup fixed by the same recipe.** Late BF16 attention dQ error reproduces (142% worst-layer, Pythia-160m final); Chen et al. [12] already trace it to a term ∝ mean key, and we show removing that key mean in the forward QK (SageAttention smoothing) is the dominant lever — B(x) takes a full BF16 step's gradient error 204% → 11.8% (160m), 43% → 3.0% (410m). On the *realistic* FP8 baseline (block-scaled MXFP8+FP32 accum), B(x) only recovers to ≈ plain-BF16 error (41–76%), not BF16+B(x). `ladder-pythia.json`, `ea-pythia160m.json`, `ea-pythia410m.json`.
5. **Where you round beats how many bits.** The cleanest instance: swamping is magnitude-independent. Supporting: a 16-bit log-polar format is 2.1× worse than BF16 on Qwen3 (5.2% vs 2.4% median per-parameter; 4.9× on the norm-weighted metric), and GFPA (one config) beats the best per-model fix on 5/6 models, ties on the 6th, and is bit-identical at offset 0 and 8M (132% → 13.5% on Pythia-160m); immutable keys tie full precision at inference (8.057 vs 8.055). `gfpa-*.json`, `ea2-loc-qwen3.json`, `free-wins-quality.json`.

## Claims ledger

Status: **measured** = author verified the number against the raw run output in this session; **derived** = arithmetic from measured values; **modeled** = from op counts / spec sheets.

| Claim | Evidence path | Status |
|---|---|---|
| 35/64 rotary pairs swamped (ω<2^-9); FP16 28 | `../phaselock-kv-shifts/evidence/rotation-swamping.json` | measured |
| Re-rotation key error 0.0020/0.031/0.10/0.43 at 1/64/256/1024 shifts; FP32 exact | `../phaselock-kv-shifts/evidence/rotation-swamping.json` | measured |
| BF16 twiddle → rel error 1.17, norm ratio 1.61 at 1024 shifts | `../phaselock-kv-shifts/evidence/rotation-swamping.json` | measured |
| Re-rotation +1.4%/+27%/+49% ppl (Qwen2.5-1.5B / Qwen3-0.6B / 1.7B) | `../phaselock-kv-shifts/evidence/review-fixes.json` | measured |
| Re-rotation % expressed as ratios | from `review-fixes.json` ppl / ref_ppl | derived |
| Exact swamped pairs remove 103%/101%/97% of loss | `../phaselock-kv-shifts/evidence/review-fixes.json` | measured |
| Swamped pairs carry 77%/75% squared QK-norm gain; 55% of pairs | `../phaselock-kv-shifts/evidence/review-fixes.json` (`gamma_slow_overlap`) | measured |
| Block shift ≥16 removes cost (CI includes 0, both models) | `../phaselock-kv-shifts/evidence/review-fixes.json` | measured |
| BF16 twiddle → 254/406/2501 ppl (Qwen2.5-1.5B/Qwen3-0.6B/1.7B) | `../phaselock-kv-shifts/paper.md` §5.3/§6.9; `evidence/bithacks-qwen3.json` | measured |
| FP32 cliff at 2^24 (9.5→22.6, →6305 at 5e9); int32/FP64 flat (Qwen2.5-1.5B) | `../phaselock-kv-shifts/paper.md` §6.3; `evidence/free-wins-offset.json` | measured |
| 2^24 cliff replicates Qwen3-0.6B (20.4→28.8) and 1.7B (15.7→20.3) | `../phaselock-kv-shifts/evidence/bithacks-qwen3.json` | measured |
| Q4 keys 6135 (post-RoPE) → 268 (pre-RoPE) → 8.194 (bias removed) Qwen2.5-1.5B | `../phaselock-kv-shifts/evidence/free-wins-quality.json` | measured |
| Q4 after-RoPE 411.9/115.1 → calibrated 17.465/13.943 (+0.6%/+0.5%); K+V calibrated +0.36%/−0.19% | `../phaselock-kv-shifts/evidence/bithacks-qwen3.json`, `free-wins-quality.json` | measured |
| γ max/median predicts plain-Q4 KL (ρ=+0.83, p=4e-8); calibration erases it; gain range 2.4–42× | `../phaselock-kv-shifts/paper.md` §6.9; `evidence/bithacks-qwen3.json` | measured |
| Immutable ring ties pristine 8.057 vs 8.055; FP64 ring 8.054 | `../phaselock-kv-shifts/evidence/free-wins-quality.json` | measured |
| Zero surviving-key rewrites over 100k tokens; bit-exact restart at 32,768 | `../phaselock-kv-shifts/paper.md` §6.4 | measured |
| Fused pre-RoPE 3.0× faster than FP32 re-rotation at 32k window | `../phaselock-kv-shifts/evidence/free-wins-speed.json` | measured |
| Integer bit-hack trig 1.30× over table at 128k; 12.8× lower max-abs error (0.00090 vs 0.01151) | `../phaselock-kv-shifts/evidence/bithacks-speed.json` | measured |
| Page-frame Q4 decodes 8.6% faster than best BF16 fused kernel at 32k | `../phaselock-kv-shifts/evidence/bithacks-speed.json` | measured |
| Late-training BF16 dQ 142% (160m), 111% (410m); growth 1→4→50→142% | `saturn/experiments/2026-09-30-phaselock-gauge-leak/results/ladder-pythia.json` | measured |
| Centering (worst-layer) 142%→20.8% (160m kernel); 29.6%→0.97% (Qwen2.5-1.5B kernel, 30×) | `.../gauge-leak/results/ladder-pythia.json`, `final-qwen25-1.5b-t512.json` (`dq_fro.max`) | measured |
| GFPA 131.7%→13.5% (160m), 27.9%→1.02% (Qwen2.5-1.5B); bit-identical 0 vs 8M | `.../gauge-leak/results/gfpa-small.json`, `gfpa-qwen25-1.5b.json`, `gfpa-qwen3-*.json` | measured |
| GFPA needs base (nobase→131.8%) and conservation (noconserve Qwen2.5-1.5B→23.9%) | `.../gauge-leak/results/gfpa-small.json`, `gfpa-qwen25-1.5b.json` | measured |
| B(x): BF16 204%→11.8% (160m-143k), 43%→3.0% (410m-143k) | `saturn/experiments/2026-09-30-spf-native-boundary/results/ea-pythia160m.json`, `ea-pythia410m.json` | measured |
| MXFP8 (block) 18k–67k% → +B(x) 41–76% (≈ plain BF16, ≫ BF16+B); per-tensor FP8 331k%/1.98M% | `.../spf-native-boundary/results/ea-pythia160m.json`, `ea-pythia410m.json` | measured |
| Error is forward not backward (backward-only 0.5–0.9%, global_rel) | `.../spf-native-boundary/results/ea2-loc-*.json` | measured |
| 16-bit log-polar vs BF16 (Qwen3-0.6B): 5.2% vs 2.4% median (2.1×); 12.8% vs 2.6% global (4.9×) | `.../spf-native-boundary/results/ea2-loc-qwen3.json` | measured |
| Integer accumulation bit-identical across reduction splits (12/12 layers) | `obsidian/spf/2026-09-30-spf-native-transformer-two-domain-machine.md` Test 3 | measured |
| Log-domain accumulator ~93× slower than BF16 tensor cores (1.0 vs 92.6 TFLOP/s) | same note, speed table | measured |
| Toy witness: common key 65536 turns exact-0 gradient coord into −24; factoring restores 0 | `.../phaselock-kv-shifts/experiments/training_factorization/` (`mechanics.json`) | measured |
| SAR factored precision 29× faster than FP64 at matched quality (−39 dB) | `saturn/experiments/2026-09-30-spf-factored-precision/FINDINGS.md`, `results/sar-4080-v2.json` | measured |
| Count×rate ring load-bearing: θ=n·f exact at n=1e13 (FP64 off 8e-4) | `.../spf-factored-precision/probes/ring_probe.py` output in FINDINGS | measured |
| B(x)/GFPA symmetries = integer lines in log coordinates | §2.2, derivation `../phaselock-kv-shifts/notes/phase-integer-training-factorization.tex` | derived |

### Claims dropped, downgraded, or corrected

Round-1 corrections (metric/wording errors caught by the evidence audit; all verified against raw JSON this session):

- **"16-bit log-polar 5× worse than BF16" → corrected to 2.1× on the primary metric.** The 5× (4.9×) used `global_rel`, which is dominated by the very outlier channels the story is about; on `median_param_rel` (the Table 6 metric) it is 5.2% vs 2.4% = 2.1×. The paper now reports both and names the three error statistics once (§2.3). This also demoted the claim from an abstract/§2.3 headline to a supporting point; the *promoted* lead is swamping's magnitude-independence.
- **"Centering 29.6% → 0.67% (44×)" → corrected to 29.6% → 0.97% (30×).** The old line mixed worst-layer "before" (`dq_fro.max`) with median "after" (`dq_med.median`). Now consistently worst-layer.
- **Bit-hack rotation error "17×" → 12.8×** (max-abs, 0.00090 vs 0.01151 at 128k; the 17× was a different-metric companion number). Q4-bias "+1.8%" → **+1.7%**. Backward-only "0.6–0.9%" → **0.5–0.9%**. γ gain range "3–42×" → **2.4–42×**. "~95× slower" → **~93×** (1.0 vs 92.6 TFLOP/s). "within 0.4%" → tabulated as **0.6% (K) / 0.4% (K+V)**.
- **[12] "reached via a mirror, verify" hedge → withdrawn.** arXiv 2609.34272 is confirmed real (Chen et al., "Broken Symmetry in BF16 Attention"); all cited arXiv IDs were verified live during revision. The honest *delta* vs [12] is now stated crisply: same mean-key object, removed at its forward source rather than via the backward GProj; [12]'s own forward-pass softmax-FMA finding is credited in §8.1.
- **FP8 strawman → reframed.** The abstract/§8.2 no longer lead with per-tensor FP8's "millions of %". The fair baseline is block-scaled MXFP8 + FP32 accumulation (DeepSeek-V3); on it, B(x) only recovers to ≈ plain-BF16 error (41–76%), stated plainly. "B(x) fixes FP8 training" is explicitly *not* claimed.

Standing from round 0:

- **"Key mean is 476× the spread" (blog) → downgraded.** Not in committed JSON; replay notes give ≈835× (Pythia-160m) / ≈2,400× (Qwen2.5-1.5B L0). The paper leads with the raw-verified worst-layer gradient error (142%), not the ratio.
- **Log-polar/"SPF" as a training *speed* win → cut.** A log-domain accumulator is ~93× slower than BF16 tensor cores; its role is restricted to storage + exact components, and B(x) is format-agnostic (demonstrated on plain BF16). The term is defined once ("log-polar") and used sparingly; no bare "SPF" appears in the body.
- **SAR / factored precision → brief Appendix B (≤3 sentences), not a main result.** Factorization win, not a number-format win.
- **"Integer phase improves the model over float" → not claimed.** It ties FP64 on quality; its only exclusive advantage is removing the 2^24 cliff at FP32 throughput.
- **"7% vs 98.5% top-1 after 1024 shifts" (older headline) → not used.** Superseded by the magnitude-independent mechanism and per-pair model-level numbers.

## Owed experiments (to raise acceptance odds)

The three cheapest, highest-value runs (each ~10 min on one RTX 4080). All are training continuations or single-model generalizations, because the paper's weakest point is that no training run yet shows a loss benefit.

1. **Late-checkpoint Pythia training continuation, BF16+B(x) vs plain BF16 (loss curve) — RUNNING as of this draft (placeholder `<!-- TODO training-continuation -->` in §8.4).** Resume Pythia-160m from a late checkpoint (≈100k–143k), arms: realistic BF16 with FP32 master weights; same + B(x) (key-mean removal + GProj); FP32-attention reference. Report held-out loss vs steps, ≥2–3 seeds. This converts the paper's one-step gradient-parity claim into a convergence claim — the single biggest gap, and the one the numerics reviewer said separates "diagnostic" from "method." Kill condition: indistinguishable curves → reframe the training half as diagnostic (a few-hundred-step continuation from an already-late checkpoint may be too short to accumulate divergence, so a null is weak evidence, not vindication of plain BF16).
2. **FP8 pretraining A/B with per-channel key correction + B(x).** The SageBwd open problem is that 8-bit attention converges slower in pretraining. A short Pythia continuation in FP8 ± (key-mean removal, per-channel gain calibration, GProj) measuring loss would directly address a known frontier-lab pain point and connect the paper to SageAttention3. Kill condition: if B(x) does not narrow the FP8-vs-BF16 loss gap, the training claim is overstated.
3. **Generalize the fix above 1.7B / to a current family.** One single forward+backward on a larger or more current model (e.g. a Llama-3 8B or Qwen3-4B) through the GFPA / B(x) harness, reporting worst-layer dQ error plain vs fixed. This attacks the "≤1.7B, two families" limitation head-on and is the cheapest credibility buy for a frontier-lab audience. Kill condition: if the key-mean/gain mechanism is absent on a current model, the inference and training stories narrow to older architectures.

Secondary (cheap, lower novelty): interpolated-bin SAR arm to close the −39 dB gap (Appendix B); a real-engine (llama.cpp) block-shift confirmation of §3.4; vocab-head gauge quotient to close the last batch-invariance leak.

## Figures

Seven figures, numbered in order. Two were generated this round (tiny matplotlib, one process, `figures/make_figures.py`); five are reused existing files referenced by relative path.

- **Figure 1** (new) — `figures/mechanism-schematic.png`: the shared mechanism (value = invariant + content; rounding lands on the invariant; remove-first fixes it), §2.
- **Figure 2** — `../phaselock-kv-shifts/figures/rotation-swamping.png`: swamping by rotary frequency, §3.
- **Figure 3** — `../phaselock-kv-shifts/figures/fp32-phase-threshold.png`: the 2^24 cliff, §4.
- **Figure 4** — `../phaselock-kv-shifts/figures/decode-speed-vs-window.png`: decode speed vs window, §6.
- **Figure 5** — `.../spf-native-boundary/results/figures/forward-vs-backward.png`: error is forward not backward, §8.1.
- **Figure 6** (new) — `figures/bx-vs-fp8-bars.png`: B(x) vs BF16/MXFP8/MXFP8+B(x), primary metric, log scale, §8.2.
- **Figure 7** — `.../spf-native-boundary/results/figures/ablation-ladder.png`: native-stack ablation, §8.2.

Still useful but not yet made: a GFPA offset-robustness panel (0 vs 8M, six models) for §7.3 (`gfpa-*.json`); an exact-pair/block-shift bar chart for §3.3–§3.4 (`../phaselock-kv-shifts/figures/swamping-fixes.png` is close); and the loss-curve figure once owed experiment 1 lands.

## Provenance and scope

Every number in the paper has an evidence path listed above; the author verified the load-bearing numbers against the raw run JSONs in-session (GFPA, B(x), rotation-swamping, review-fixes, Q4 keys, 2^24 cliff, immutable tie, forward-vs-backward, log-polar-vs-BF16, both on `median_param_rel` and `global_rel`). The three round-1 reviewers independently re-derived ~50 numbers and the large majority matched exactly; the handful of metric/rounding corrections they flagged are applied (see "Claims corrected" above). The training-side FINDINGS notes were written by a fork and were uncommitted; their headline numbers (142% dQ, GFPA table, B(x) table) were re-derived here from `results/*.json` and matched. All cited arXiv identifiers — including [12] (2609.34272, Chen et al.), [17] (FP8-Formats, 2209.05433), and the added SmoothQuant/AWQ/DeepSeek-V3/FlashAttention/Unit-Scaling/μP references — were verified live via web search during revision.

This paper does not edit any file outside this directory. The companion inference paper is `../phaselock-kv-shifts/`; the training experiments are in `saturn/experiments/2026-09-30-phaselock-gauge-leak/` and `2026-09-30-spf-native-boundary/`.
