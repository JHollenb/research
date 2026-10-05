# Round 1 review — "Rounding Placement" (Hollenbeck)

**Reviewer persona:** training/inference numerics (FP8/BF16 stacks, FlashAttention kernels, KV-cache quant).
**Verdict:** borderline reject at a top main track as-is; clear accept at a workshop. **Score 5/10.**
**Disclosure:** READ-ONLY review. I re-derived the load-bearing numbers from the cited raw JSONs in-session (results below). The scheduler was unreachable from this host (LAN blocked: `No route to host` to `<scheduler-host>:9025`), so I could not inspect the running training-continuation job directly.

---

## Summary of what I verified (independent re-derivation from raw evidence)

The number discipline here is unusually good. Every headline I checked reproduced from the cited file, with one metric caveat (below).

- **Table 6 (B(x) training, `median_param_rel`)** — exact match. 160m@143k: BF16 2.0376→**203.8%**, BF16+B(x) 0.1182→**11.8%**, FP8 33.07→**3307%** (abstract's "past 300,000%"), MXFP8 6.71→**671%**, MXFP8+B 0.761→**76.1%**. 410m@143k: 0.4266→**42.7%**, B(x) 0.0303→**3.0%**, FP8 198.1→**19,809×=1.98M%**, MXFP8+B 0.410→**41.0%**. All 20 cells verify (`ea-pythia160m.json`, `ea-pythia410m.json`).
- **Table 5 (GFPA, worst-layer `dq_fro.max`)** — exact. Pythia-160m plain **131.7%**, mean@0 **15.1%**, mean@8M **37.1%**, GFPA **13.5%** (bit-identical @0 and @8M confirmed: 0.13472 == 0.13472). nobase→**131.8%**, noconserve (Qwen2.5-1.5B)→**23.9%**. All six models verify (`gfpa-*.json`).
- **Rotation swamping** — 35/64 pairs (BF16), 28 (FP16); random-walk pred 0.0361; exact-swamped-pairs remove 103%/101%/97% (`rerotate_exact_slow`), complementary 41%/20%/27% (`rerotate_exact_fast`), γ6 88%/76%. γ²-mass-in-slow 77%/75%, γ6-in-slow 74%/70%. All verify (`rotation-swamping.json`, `review-fixes.json`).
- **§7.1 kernel 142.2%** — `runs[5].layers[11].errors.flash.dq_fro = 1.42236` → real FA2 kernel, final 160m checkpoint. Verifies.
- **Figures** — all 5 referenced PNGs exist on disk.

**The one number that does not reproduce on the paper's main metric.** The headline "a 16-bit log-polar format is **five times worse** than BF16" (abstract L19; §2.3 L81; §8.2 L259: "12.8% vs BF16's 2.6%") is computed on **`global_rel`** (spf16g_B 0.1280, bf16_B 0.0261 → 4.9×). On **`median_param_rel`**, the metric used for Table 6 and everywhere else, the same two arms are **5.2% vs 2.4% = 2.2×**, not 5×. The paper silently switches to the norm-weighted statistic — which is dominated by exactly the high-norm gain-outlier channels the narrative is about — for its most-quoted negative result. The direction is real; the "5×" is metric-selected. This must be disclosed and ideally stated on the consistent metric.

---

## 1. Is the thesis novel/correct/supported, or retrospective unification?

**Partly a genuine mechanism, partly repackaging.** The real contribution is the swamping lens: *a stored value = large invariant + small content; the model depends only on content; linear-coordinate rounding spends the mantissa on the invariant.* That single idea correctly unifies (a) the softmax key-mean, (b) the late-training key-mean in the gradient, and (c) the RoPE low-frequency pairs, and the fix "remove the invariant in high precision first" genuinely is one operation across them. That part is sound, correct, and the paper's best idea. It is also *exactly* SageAttention key-smoothing (mean subtraction), which the paper credits honestly (§9 L277).

**Where the unification is forced.** "Coordinate frame, not bit width" bundles three mechanically different things under "one recipe B(x)": (1) invariant removal (relative-precision misallocation — the real unifying case), (2) integer phase, (3) conservation-law projection. (2) and (3) are bolted on. Most tellingly, the **FP32 2^24 cliff is a dynamic-/integer-range phenomenon, not a frame phenomenon** — the paper itself concedes it is "the one place the integer representation is strictly necessary and more value bits do not substitute" (§4 L147; L34). A 24-bit integer range running out at 2^24 **is** a bit-count limit (of the integer field); filing it under "frame beats bits" is a category slip. So the thesis is three claims wearing one coat: swamping (strong, correct), integer range (real but it *is* a bits story), conservation projection (second-order, by the author's own §7.2). The "frame beats bits" slogan is supported cleanly only by the magnitude-independence of swamping (§2.3 first point) — the other two legs are weaker than the framing implies.

**Novelty:** none of the four fixes is new (author states this, L40). The novelty is the lens + the cross-setting measurement that the same operation repairs an inference drift and a training gradient. That is a real but modest synthesis contribution, not a new method.

## 2. Prior art missed / under-credited (IDs verified where noted)

Cited and correct: RoFormer 2104.09864, StreamingLLM 2309.17453, KVQuant 2401.18079, KIVI 2402.02750, QuaRot 2404.00456, SpinQuant 2405.16406, SageAttention 2410.02367, Wang "When Precision Meets Position" 2411.13476, nGPT 2410.01131, LNS-Madam 2106.13914, H2O/Quest/InfLLM. Ref [12] **2609.34272 does appear to exist** (title + mechanism — broken row-sum symmetry, leak ∝ mean key, FP32-recompute fix — match a live arXiv entry; still verify canonical).

**Missing, and a numerics committee will notice:**
- **SmoothQuant (2211.10438, verified)** and **AWQ (2306.00978, verified)** — per-channel scaling / outlier migration by dividing out an activation-side gain. This is *precisely* the §5.2 Qwen3 "divide out the per-channel γ" fix. Not citing SmoothQuant for a per-channel-gain-removal paper is the biggest gap.
- **DeepSeek-V3 technical report (2412.19437, verified)** — fine-grained (1×128 / 128×128) FP8 scaling + periodic FP32-register accumulation at real pretraining scale. This is the state of the art the "frame beats bits / spend precision by granularity" thesis must engage, and it directly bears on §8's accumulation/localization story. Its absence is the paper's most serious scholarship hole for this audience.
- **FlashAttention / FA2 / FA3 (2205.14135; 2307.08691; FA3 NeurIPS 2024)** — replayed but never cited by name.
- **μP / Tensor Programs V (2203.03466, verify)** and **Unit Scaling (2303.11257, verify)** — choosing scales/coordinates so low precision works; the conceptual neighbors of the thesis.
- **"To FP8 and Back Again" (2405.18710, verify)** — FP8 training stability; directly relevant to §8.
- Minor: **FP8-LM (2310.18313, verify)**; **SageBwd** — paper cites it under 2505.11594, but a separate "SageBwd: A Trainable Low-bit Attention" (2603.02170) surfaced; the [14] ID likely conflates SageAttention2/3 and SageBwd — **verify and split**. FP8-Formats (Micikevicius) is 2209.05433 (verify); MX spec/"Microscaling Data Formats" 2310.10537 (verify).

## 3. Experimental rigor

- **Scale ≤1.7B, single seed** (L15). For a top venue making a *training* claim this is disqualifying on its own; the mechanisms plausibly scale but are shown only on old small models (Pythia 160/410m, Qwen ≤1.7B). No current architecture (Llama-3, Qwen3-4B+, any MoE).
- **FP64 as exact-integer stand-in** (§8 L235, L287) is defensible and well-argued (elementwise idealized for every arm, so it isolates matmul-operand format). Acceptable.
- **One-step gradient error ≠ training outcome.** This is the central weakness and the author flags it (L15, L285). Real BF16 training uses FP32 master weights + optimizer state that absorb per-step error; the cited [12] failure took 25B tokens to manifest. A 204% *single-step* `median_param_rel` is not 204% loss degradation. Gradient parity is necessary, not sufficient.
- **The FP8 baseline is a strawman.** "Standard per-tensor E4M3/E5M2" reaching 330k–1.98M% (Table 6; abstract L19; L83) is not how anyone trains in FP8. The fair baseline — fine-grained/block FP8 with FP32 accumulation (DeepSeek-V3) — is approximated only by **MXFP8**, and there **B(x) reaches 41–76%, still worse than plain BF16's 42.7%** on 410m. So on the honest baseline the FP8 story is *unimpressive*, and the "frame not the eight-vs-sixteen bits" claim (L83) is argued against a baseline no FP8 stack uses. This is the single point a numerics lab will press hardest.
- **Perplexity on WikiText-2 only; batch-1 Python-decoder speed** (L288). Speed numbers "bound the operation, not end-to-end throughput" — correctly hedged, but then not usable as a systems result.
- Good practice: content-addressed receipts, paired block bootstraps with honest "descriptive, dependent" caveats, causal exact-pair ablations (not just correlation).

## 4. What a lab acts on tomorrow vs dismisses

**Act on now (low risk, mechanism-backed):**
1. Subtract per-head key mean before any low-bit K cache / low-precision QK. Free, exact, already half-known via SageAttention; the paper's value is showing it is also the *dominant* late-training gradient fix.
2. Pre-RoPE key quant + per-channel affine removal (bias for Qwen2.5, γ for Qwen3) for 4-bit KV — i.e. KVQuant+SmoothQuant, here validated on two families with a clean γ-ratio→KL predictor (ρ=0.83).
3. Don't one-position re-rotate KV in BF16 in streaming; keep pristine pre-RoPE keys (StreamingLLM) or block-shift ≥16. Confirmed CI-includes-zero from Δ≥16.
4. Integer/FP64 RoPE phase *if* you actually serve >16M-token absolute positions (niche but real).

**Dismiss / not yet:**
- "B(x) fixes FP8 training" — no loss curve, strawman baseline, MXFP8+B(x) still worse than BF16.
- Log-domain/integer accumulator for determinism — author's own measurement is **95× slower**, no hardware. (Batch-invariance is better addressed by Triton deterministic reductions / the recent batch-invariant-kernels line, not a new number system.)
- GFPA "as a packaged kernel" — no kernel, no throughput, proxy metric only.
- SPF/log-polar as a format — author already cut this; correct call.

## 5. Over/under-claims (line numbers)

- **L19 / L81 / L259** "five times worse" / "12.8% vs 2.6%" — metric-switched to `global_rel`; 2.2× on the paper's main metric. Overclaim.
- **L19 / L83 / Table 6** FP8 "past 300,000%" / "1,980,000%" — true vs per-tensor FP8, but that is a strawman baseline; the framing oversells.
- **L23 / title** "coordinate frame, not bit width" — overclaims relative to §4's own concession (L147) that the 2^24 cliff *is* an integer-range (bit) limit.
- **L227 Table 5** "GFPA matches or beats the best per-model special case" — on Qwen2.5-1.5B, GFPA 1.02% > mean-centering 0.95%. "Matches" at best; slight overstatement.
- **L38 / §6** "immutable keys tie full-precision quality" — genuinely a *tie* (8.057 vs 8.055), honestly presented; good example of not overclaiming.
- **L15, L285-291** limitations are unusually candid (no training run, proxy, scale, strawman omission of Hadamard, layer-dependent ratio). Credit.
- Under-claim: the magnitude-independence of swamping (§2.3) is the cleanest, most novel, most defensible result and is buried; it deserves to be the lead, not the log-polar 5×.

## 6. Clarity

- Abstract is dense but lands the four failures + one recipe. Structure (mechanism → 2 inference → 2 training → serving → related) is sound.
- **Jargon:** **B(x)** defined (§2.2 L65). **GFPA** defined (§7.3 L218). **SPF** is used (L73, L269, §8.3, Appendix) but **never expanded in this paper** — it is a cross-project term (log-polar / "spectral" format); a reader without the companion will not know what SPF is. Define on first use or remove. "Swamping" is defined and cited [11] — good. "Twiddle," "GProj," "page/per-page frame" could use one-line glosses.
- Figures: all 5 paths resolve. But two central objects have **no figure**: the schematic of the shared mechanism (§2) and any loss curve. README acknowledges both as "still needed." For a paper whose whole pitch is one mechanism, the missing §2 schematic is a real gap.
- Appendix B (SAR) is correctly demoted but still risks diluting focus for a transformers venue.

## 7. Score and the 5 highest-leverage changes

**Score: 5/10.** Main track (MLSys/ICLR/NeurIPS): **reject (borderline)** — faithful numbers and a genuine lens, but synthesis-level novelty, ≤1.7B single-seed, a proxy for the training claim, a strawman FP8 baseline, and missing core prior art (SmoothQuant/AWQ/DeepSeek-V3). Workshop (ICLR/NeurIPS efficient-ML, MLSys-adjacent): **accept** — the swamping mechanism + cross-setting demonstration is a good workshop contribution.

**Ranked changes that most raise the score:**
1. **Land the running training continuation (and a fair-baseline FP8 A/B).** Convert one-step parity into a loss curve: BF16+B(x) vs plain BF16 vs FP32 ref, and crucially **vs fine-grained/block FP8 (DeepSeek-V3-style)**, not per-tensor FP8. This is the difference between "diagnostic" and "method."
2. **Fix the FP8 baseline framing throughout.** Lead with MXFP8/block-FP8+B(x); drop or heavily caveat the per-tensor "millions of %."
3. **Cite and engage SmoothQuant, AWQ, DeepSeek-V3 FP8, FlashAttention, μP/Unit Scaling.** Position §5.2 explicitly as SmoothQuant-in-the-KV-cache.
4. **Report the log-polar result on the consistent (`median_param_rel`) metric**, or justify `global_rel` and apply it everywhere; retire the unqualified "5×."
5. **Scale to one current model (Qwen3-4B / Llama-3-8B), even single forward+backward**, and separate the thesis into its two honest halves (swamping=frame; 2^24=integer range), dropping the overreach of the one-coat framing. Add the §2 mechanism schematic.

## 8. On the running training continuation (Pythia-160m BF16 vs BF16+B(x) vs FP32 ref, held loss)

I could not reach the scheduler to inspect it. What the outcome would mean:

**Would rescue the training claim** (promote it from diagnostic to method): a **reproducible, seed-robust held-out loss gap** where BF16+B(x) tracks the FP32 reference and plain BF16 diverges, the gap **grows with steps**, holds across **≥2–3 seeds**, and persists against a **realistic BF16 recipe** (FP32 master weights, standard scaling — not a crippled per-tensor arm). Even a small but clean, growing, multi-seed gap on a late-checkpoint continuation is enough to say "the one-step gradient error matters for convergence."

**Would NOT rescue it:** (a) **indistinguishable curves** — the author's own stated kill condition; then B(x) is cosmetic for training and the whole training half must be reframed as diagnostic. (b) A gap only at **a single seed / within bootstrap noise**. (c) A gap on **training loss but not held-out**. (d) A gap that exists **only because the plain-BF16 arm is a strawman** (no FP32 master weights, per-tensor only) — a numerics reviewer will reconstruct the baseline and discount it. (e) A **positive-but-tiny** result at 160m that still leaves the ≤1.7B / single-family / old-architecture limitation fully intact — it narrows, not closes, the gap, and says nothing about FP8 (the actual frontier pain point, which needs experiment #2 in the README, the fine-grained-FP8 A/B). Also note a few-hundred-step continuation from an already-late checkpoint may be **too short to accumulate divergence** (the [12] failure took 25B tokens); a null there is weak evidence, not vindication of plain BF16.
