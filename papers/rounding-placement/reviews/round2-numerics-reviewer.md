# Round 2 review — "Where You Round Beats How Many Bits" (Hollenbeck)

**Reviewer:** training/inference numerics (FP8/BF16 stacks, FA kernels, KV-cache quant).
**Verdict:** borderline reject main track (improved, scale is the binding constraint); clear accept workshop.
**Score: 6.5/10** (was 5/10).
**Disclosure:** READ-ONLY. I re-derived every §8.4 headline from `results/*.json` and read `train_worker.py` + `exact_accum_worker.py`. Scheduler not contacted; I verified file→paper arithmetic, not job provenance.

## 1. Round-1 resolution

| Round-1 point | Status |
|---|---|
| Training = one-step proxy, no loss curve (numerics #1,#8) | **Resolved** — §8.4 lands a measured, reproducible, dose-controlled held-loss benefit |
| FP8 baseline strawman (#2,#5) | **Resolved** — MXFP8 fair baseline; says plainly B(x) only ≈ plain BF16 |
| log-polar "5×" metric-selected (#4) | **Resolved** — 2.1× primary / 4.9× norm-weighted, both stated |
| "frame beats bits" bundles range+projection (#1,#5) | **Resolved** — three legs split; 2^24 flagged as an integer-*range* (bit) story |
| Missing SmoothQuant/AWQ/DeepSeek-V3/FA/μP/Unit-Scaling | **Resolved** — all cited and engaged |
| Metric-switch undocumented + 9 number errors (audit) | **Resolved** — all 9 re-verified corrected |
| §2 mechanism schematic | **Resolved** — Fig 1 |
| Scale ≤1.7B, single family, pre-2025 models (#3) | **Unresolved** — binding limit; no current/frontier model |
| Single-seed (#3) | **Partial** — seeds deterministic (dropout 0); 3 data-order replicates instead (thin but honest) |
| GFPA as kernel / throughput | **Partial** — proxy metric only, honestly scoped |
| Synthesis-level novelty (#1) | **Unresolved/inherent** — acknowledged |

## 2. Is the training result convincing to a numerics team?

**Numbers reproduce exactly** (3 orders → ref 3.1827 / bf16 3.2059 / B(x) 3.1621 / mean-only 3.1561; per-order B(x)−bf16 gaps −0.039/−0.042/−0.051; grad err bf16 148%→66%, B(x) 29%→8.6%; MXFP8 divergence desc-eff −0.67; dose control step64000 all arms 2.9561–2.9572). The "custody-audit-pending" hedge covers job provenance, not the arithmetic, which is clean.

- **Baseline is genuinely standard** (resolves the #1 round-1 strawman worry). `train_worker.py:52` = elementwise bf16 cast; fp32 master weights + fp32 AdamW + fp32 accumulation; softmax/LN/GELU/residual fp32. One caveat: it rounds **all** matmuls incl. backward and LM-head to bf16 (vanilla autocast keeps those fp32) — slightly *more* aggressive than real autocast, but §8.1 shows backward rounding costs 0.5–0.9%, and B(x) runs the identical path, so it is not an unfair baseline. It is an emulation, **not** the FA2 kernel of §7.1.
- **Dose control is the strongest element** and is real: at step64000 plain-bf16 descent-efficiency is already 0.97, so AdamW absorbs it and all arms tie; the benefit appears only where the gradient direction is bad. B(x) implementation verified non-trivial (`exact_accum_worker.py:238` key-mean, `:269` GProj gated by `BX_GPROJ`, `:288` unembed-mean, `:75` real block-32 MXFP8). Caveat: dose control is **single data order** (n=1), and it confounds "small grad error" with "less-converged checkpoint" — but descent-efficiency directly measures the thing B(x) fixes, so it holds.
- **"Key-mean alone = full B(x)" is consistent with the thesis** (invariant removal is the unifier; GProj second-order) — mean-only (3.156) even edges full B(x) (3.162). But note the implication: for *training loss*, the entire benefit is the **SageAttention key-mean operation**; GProj/unembed-mean/integer-phase add nothing measurable. The paper says this, but the "B(x) 3-part recipe" branding oversells what moves the loss.
- **Gap size vs noise:** 0.044 nats, ~6–7× the between-order spread, consistent sign across 3 orders — real, but small and thin (n=3, no stochastic-training noise floor).
- **Undisclosed trajectory shape:** the gap is **largest at step ~300 (bf16−B(x) = +0.073) and narrows to +0.039 by step 1000** as bf16's descent-eff climbs 0.41→0.84. §8.4 reports only the (conservative, smallest-post-100) final gap. The benefit is *transient recovery after a bad checkpoint*, not accumulating divergence — this must be stated (the PREREG addendum already admits it; the paper body does not).

**Net:** convincing as a diagnostic→method conversion at 160M; **not** convincing that it matters at frontier scale or in FP8 (MXFP8+B(x) ends +0.27 above ref, far from BF16+B(x)). Horizon 2.05M vs 25B tokens makes it a proof-of-concept, honestly labeled.

## 3. Remaining overclaims (line numbers)

- **L36 / L287** "B(x) … lowers held-out loss by 0.044 nats" — true, but omit the trajectory: gap peaks early and narrows. Add one sentence (over/under-sold by omission).
- **L287** "6–15× the spread between data orders" — loose; the clean statement is ~5–7× the gap's own cross-order half-range. Tighten.
- **L19 abstract / L71 §2.2 "B(x) recipe"** — for the training-*loss* claim the active ingredient is solely key-mean (SageAttention); say so where the loss result is stated, not just in §9.
- **L299 / README** "training half … no longer diagnostic-only" — fair, but it is diagnostic+**one** 160M proof-of-concept; keep "at 160M" adjacent every time.
- **Minor:** L295 "within 0.001 nats" is 0.0011 and single-order.

## 4. Decision

- **Main track (MLSys/ICLR/NeurIPS): borderline reject**, closer than round 1. The training result removes the biggest objection; the binding constraint is now scale/novelty (≤1.7B, pre-2025 families, synthesis-level). **One current-model result flips this to borderline accept.**
- **Workshop (efficient-ML / MLSys-adjacent): clear accept.**

## 5. Five changes that most raise the score

1. **One current-model (Qwen3-4B / Llama-3-8B) single fwd+bwd** through the B(x)/GFPA harness: worst-layer dQ plain vs fixed. Cheapest attack on the only remaining blocker.
2. **Disclose the non-monotonic gap** in §8.4 (peaks ~step 300, narrows); reframe as transient post-checkpoint recovery, not divergence.
3. **State the training-loss active ingredient = key-mean** at the result, and that GProj/integer-phase do not move the loss here.
4. **Lift the custody hedge for the arithmetic** (file→paper verified); keep it only for job provenance.
5. **Add the step64000 control at the same 3 data orders** (currently n=1) to make the causal claim replicate-backed.

## 6. Essential ≤10-min experiments (strict)

**None is strictly required for a workshop submission** given the paper's honesty. For main track, exactly **one** is worth gating on: **the current-model single forward+backward (change #1)** — ~10 min on mrun, directly tests whether the key-mean/gain mechanism exists on a 2026 architecture (kill condition: if absent, both stories narrow to older models). Everything else (#2–#5) is reporting/writing or a cheap replicate, not new science.
