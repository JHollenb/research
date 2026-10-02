# Rounding Placement: Coordinate Choice, Not Bit Width, Sets Low-Precision Error in Transformers

[Full paper](paper.md) · Jacob Hollenbeck · draft 2026-10-02

The author's third paper. It merges two measured programs — a streaming-inference study of rotary KV caches (the "PhaseLock / rotation-swamping" line) and a training-numerics study of attention gradients (the "gauge leak / boundary-operator B(x) / exact-accumulation" line) — into one claim.

## The thesis (tested, not assumed)

The task proposed the framing *"low-precision error is dominated by where rounding is placed relative to the model's coordinates/gauge; choose coordinates before rounding and restore the exact law at the boundary."* We tested that against the evidence and it holds, with one sharpening that the data forced:

> **The dominant error in low-precision transformer inference and training is set by the coordinate frame in which values are rounded relative to the model's exact symmetries, not by the number of mantissa bits.** Every large failure measured — RoPE re-rotation drift, the FP32 position cliff, 4-bit key collapse, and the late-training BF16 attention-gradient blowup — is one symmetry (a rotation, a per-channel scaling, or an additive shift) rounded in the wrong frame. The fix is one recipe: remove the invariant in high precision before rounding, keep positional phase as an exact integer, and restore the conservation law at the boundary.

Why the sharpening. The original phrasing emphasizes *choosing coordinates* and *restoring the law*, which is correct, but the single most persuasive and most falsifiable fact in the merged evidence is the **negative** one: *more bits in the wrong frame do not help, and can hurt.* Three measured instances (16-bit log-polar worse than BF16 on Qwen3; FP32 position bits useless past 2^24; swamping independent of key magnitude) make "frame beats bit width" the load-bearing claim a frontier numerics team can act on and check. The "remove invariant / integer phase / restore law" recipe is then the *how*. The paper leads with the sharpened thesis and keeps the original recipe as §2.2.

## The five headline results

1. **Rotation swamping.** One-position BF16 re-rotation freezes the 35 of 64 rotary pairs with ω < 2^-9; cost +1.4%/+27%/+49% perplexity (Qwen2.5-1.5B / Qwen3-0.6B / 1.7B); keeping only those 35 pairs exact removes 97–103%. `evidence/rotation-swamping.json`, `evidence/review-fixes.json`.
2. **FP32 position cliff.** FP32 rotary angles collapse at exactly 2^24 on three models; integer phase and FP64 stay flat past 2^32. `evidence/bithacks-qwen3.json`, `evidence/free-wins-offset.json`.
3. **Affine correction before 4-bit keys.** Removing the Qwen2.5 key bias takes Q4 keys 6,135 → 8.194 ppl (+1.8%); per-channel gain calibration brings Qwen3 Q4 within 0.4–0.6%. `evidence/free-wins-quality.json`, `evidence/bithacks-qwen3.json`.
4. **Training blowup fixed by the same recipe.** Late BF16 attention dQ error reproduces (142% worst-layer, Pythia-160m final); key-mean removal + softmax-gradient zero-sum restoration (B(x)) takes a full BF16 step's gradient error 204% → 11.8% (160m), 43% → 3.0% (410m); standard FP8 explodes past 300,000%. `ladder-pythia.json`, `ea-pythia160m.json`, `ea-pythia410m.json`.
5. **Frame beats bit width.** GFPA (one config) ties the best per-model fix on six models and is bit-identical at offset 0 and 8M (132% → 13.5% on Pythia-160m); a 16-bit log-polar format is 5× worse than BF16 on Qwen3 (12.8% vs 2.6%); immutable keys tie full precision at inference (8.057 vs 8.055) with zero surviving-key rewrites. `gfpa-*.json`, `ea2-loc-qwen3.json`, `free-wins-quality.json`.

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
| Q4 after-RoPE 411.9/115.1 → calibrated 17.465/13.943 (Qwen3-0.6B/1.7B) | `../phaselock-kv-shifts/evidence/bithacks-qwen3.json` | measured |
| γ max/median predicts plain-Q4 KL (ρ=+0.83, p=4e-8); calibration erases it | `../phaselock-kv-shifts/paper.md` §6.9; `evidence/bithacks-qwen3.json` | measured |
| Immutable ring ties pristine 8.057 vs 8.055; FP64 ring 8.054 | `../phaselock-kv-shifts/evidence/free-wins-quality.json` | measured |
| Zero surviving-key rewrites over 100k tokens; bit-exact restart at 32,768 | `../phaselock-kv-shifts/paper.md` §6.4 | measured |
| Fused pre-RoPE 3.0× faster than FP32 re-rotation at 32k window | `../phaselock-kv-shifts/evidence/free-wins-speed.json` | measured |
| Integer bit-hack trig 1.30× over table at 128k, 17× lower error vs FP64 | `../phaselock-kv-shifts/evidence/bithacks-speed.json` | measured |
| Page-frame Q4 decodes 8.6% faster than best BF16 fused kernel at 32k | `../phaselock-kv-shifts/evidence/bithacks-speed.json` | measured |
| Late-training BF16 dQ 142% (160m), 111% (410m); growth 1→4→50→142% | `saturn/experiments/2026-09-30-phaselock-gauge-leak/results/ladder-pythia.json` | measured |
| Centering 142%→20.8% (160m kernel); 29.6%→0.67% (Qwen2.5-1.5B kernel, 44×) | `.../gauge-leak/results/ladder-pythia.json`, `final-qwen25-1.5b-t512.json` | measured |
| GFPA 131.7%→13.5% (160m), 27.9%→1.02% (Qwen2.5-1.5B); bit-identical 0 vs 8M | `.../gauge-leak/results/gfpa-small.json`, `gfpa-qwen25-1.5b.json`, `gfpa-qwen3-*.json` | measured |
| GFPA needs base (nobase→131.8%) and conservation (noconserve Qwen2.5-1.5B→23.9%) | `.../gauge-leak/results/gfpa-small.json`, `gfpa-qwen25-1.5b.json` | measured |
| B(x): BF16 204%→11.8% (160m-143k), 43%→3.0% (410m-143k) | `saturn/experiments/2026-09-30-spf-native-boundary/results/ea-pythia160m.json`, `ea-pythia410m.json` | measured |
| FP8 standard → 331k% (160m) / 1.98M% (410m); MXFP8+B 76%/41% | `.../spf-native-boundary/results/ea-pythia160m.json`, `ea-pythia410m.json` | measured |
| Error is forward not backward (backward-only 0.6–0.9% BF16) | `.../spf-native-boundary/results/ea2-loc-*.json` | measured |
| 16-bit log-polar 12.8% vs BF16 2.6% (Qwen3-0.6B, full step) | `.../spf-native-boundary/results/ea2-loc-qwen3.json` | measured |
| Integer accumulation bit-identical across reduction splits (12/12 layers) | `obsidian/spf/2026-09-30-spf-native-transformer-two-domain-machine.md` Test 3 | measured |
| Log-domain accumulator ~95× slower than BF16 tensor cores | same note, speed table | measured |
| Toy witness: common key 65536 turns exact-0 gradient coord into −24; factoring restores 0 | `.../phaselock-kv-shifts/experiments/training_factorization/` (`mechanics.json`) | measured |
| SAR factored precision 29× faster than FP64 at matched quality (−39 dB) | `saturn/experiments/2026-09-30-spf-factored-precision/FINDINGS.md`, `results/sar-4080-v2.json` | measured |
| Count×rate ring load-bearing: θ=n·f exact at n=1e13 (FP64 off 8e-4) | `.../spf-factored-precision/probes/ring_probe.py` output in FINDINGS | measured |
| B(x)/GFPA symmetries = integer lines in log coordinates | §2.2, derivation `../phaselock-kv-shifts/notes/phase-integer-training-factorization.tex` | derived |

### Claims dropped or downgraded (and why)

- **"Key mean is 476× the spread" (from a blog post) → downgraded.** The blog number (476×) is not in the raw output; the measured per-layer replay notes give ≈835× (Pythia-160m worst layer) and ≈2,400× (Qwen2.5-1.5B layer 0). The paper states the ratio approximately and layer-dependent, and leads with the robustly raw-verified worst-layer gradient error (142%) instead. The ratio is not used as a headline number.
- **"Gauge-centred attention 29.6% → 0.67% (Qwen2.5-1.5B)" clarified, not dropped.** That number is real but is the **FlashAttention-2 kernel** replay with key centering (job-5ff65227df2e), not GFPA. The paper reports it as such and reports the separate manual-recompute GFPA numbers (27.9% → 1.02%) distinctly, so the two harnesses are not conflated.
- **SPF as a *speed* win in training → cut from the main claim.** Measured: a log-domain accumulator is ~95× slower than BF16 tensor cores; the lazy factored carriers do not close the gap on dense trained weights (median header R² 1–8%). The paper restricts the log-polar format's role to storage + exact components and keeps B(x) format-agnostic (demonstrated on plain BF16). SPF is defined once and used sparingly.
- **SAR / factored precision → moved to a brief Appendix B, not a main result.** It is outside transformers and is a factorization win, not a number-format win (an FP64 base ties the integer ring when the count is small). Included only to show the mechanism is general.
- **Any "PhaseLock integer phase improves the model over float" claim → not made.** Integer phase ties FP64 on quality; its only exclusive advantage is removing the 2^24 cliff at FP32 throughput (a representation result).
- **"7% vs 98.5% top-1 after 1024 shifts" (older PhaseLock headline) → not used.** Superseded by the magnitude-independent swamping mechanism and the per-pair model-level numbers, which are better controlled.

## Owed experiments (to raise acceptance odds)

The three cheapest, highest-value runs (each ~10 min on one RTX 4080). All are training continuations or single-model generalizations, because the paper's weakest point is that no training run yet shows a loss benefit.

1. **Late-checkpoint Pythia training continuation, BF16+B(x) vs plain BF16 (loss curve).** Resume Pythia-160m from a late checkpoint (≈100k–143k) for a few hundred steps, one arm plain BF16 attention, one arm with key-mean removal + GProj. Report the training loss difference. This converts the paper's one-step gradient-parity claim into an actual convergence claim — the single biggest gap. Kill condition: if the loss curves are indistinguishable, the gradient-error result does not matter for training and the training half should be reframed as diagnostic only.
2. **FP8 pretraining A/B with per-channel key correction + B(x).** The SageBwd open problem is that 8-bit attention converges slower in pretraining. A short Pythia continuation in FP8 ± (key-mean removal, per-channel gain calibration, GProj) measuring loss would directly address a known frontier-lab pain point and connect the paper to SageAttention3. Kill condition: if B(x) does not narrow the FP8-vs-BF16 loss gap, the training claim is overstated.
3. **Generalize the fix above 1.7B / to a current family.** One single forward+backward on a larger or more current model (e.g. a Llama-3 8B or Qwen3-4B) through the GFPA / B(x) harness, reporting worst-layer dQ error plain vs fixed. This attacks the "≤1.7B, two families" limitation head-on and is the cheapest credibility buy for a frontier-lab audience. Kill condition: if the key-mean/gain mechanism is absent on a current model, the inference and training stories narrow to older architectures.

Secondary (cheap, lower novelty): interpolated-bin SAR arm to close the −39 dB gap (Appendix B); a real-engine (llama.cpp) block-shift confirmation of §3.4; vocab-head gauge quotient to close the last batch-invariance leak.

## Figures

Reused existing files (referenced by relative path; no new figures generated):

- `../phaselock-kv-shifts/figures/rotation-swamping.png` — swamping by rotary frequency (§3).
- `../phaselock-kv-shifts/figures/fp32-phase-threshold.png` — the 2^24 cliff (§4).
- `../phaselock-kv-shifts/figures/decode-speed-vs-window.png` — decode speed vs window (§6).
- `../../../saturn/experiments/2026-09-30-spf-native-boundary/results/figures/forward-vs-backward.png` — error is forward not backward (§8).
- `../../../saturn/experiments/2026-09-30-spf-native-boundary/results/figures/ablation-ladder.png` — native stack ablation (§8).

Figures still needed (not yet generated; would be made from the cited evidence files):

- A single schematic of the shared mechanism (invariant + content; rounding lands on the invariant) for §2 — the paper's central idea has no figure yet.
- Exact-pair / block-shift bar chart for §3.3–§3.4 (data in `review-fixes.json`; `../phaselock-kv-shifts/figures/swamping-fixes.png` is close and could be reused).
- GFPA offset-robustness panel (0 vs 8M, six models) for §7.3 (data in `gfpa-*.json`).
- B(x) vs FP8/MXFP8 bar chart across checkpoints for §8.2 (data in `ea-pythia*.json`).
- Any figure for a loss-curve result once owed experiment 1 is run.

## Provenance and scope

Every number in the paper has an evidence path listed above; the author verified the load-bearing numbers against the raw run JSONs in-session (GFPA, B(x), rotation-swamping, review-fixes, Q4 keys, 2^24 cliff, immutable tie, forward-vs-backward, log-polar-vs-BF16). The training-side FINDINGS notes were written by a fork and were uncommitted; their headline numbers (142% dQ, GFPA table, B(x) table) were re-derived here from `results/*.json` and matched. Reference [12] (arXiv 2609.34272) was reached via a mirror and should be checked against the canonical source; the SageAttention, FP8-formats and stochastic-rounding identifiers need a final bibliographic pass before submission (flagged in paper §10 and reference [17]).

This paper does not edit any file outside this directory. The companion inference paper is `../phaselock-kv-shifts/`; the training experiments are in `saturn/experiments/2026-09-30-phaselock-gauge-leak/` and `2026-09-30-spf-native-boundary/`.
