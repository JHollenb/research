# Round 3 (final) review — "Where You Round Beats How Many Bits" (Hollenbeck)

**Reviewer:** training/inference numerics (bf16/fp8 kernels, FA, KV-cache quant).
**Score: 7/10** (round 2: 6.5). **Tier:** clear accept workshop; borderline (reject-leaning) main track.
**Disclosure:** READ-ONLY on paper. I re-derived the §8.4 headline and the §7.4 current-model numbers from the raw JSON this session (not just file→paper).

## 1. Are the round-2 attacks answered? Yes, all five.

| Round-2 top change | Status |
|---|---|
| #1 current-model fwd+bwd | **Done** (§7.4, Qwen3-1.7B) — and came back *negative*, handled honestly |
| #2 disclose non-monotonic gap | **Done** (§8.4 trajectory ¶, L295; Fig 8) |
| #3 training-loss active ingredient = key-mean | **Done** (abstract L19, §1 L36, §8.4 L293) |
| #4 lift custody hedge on arithmetic | **Done** (custody PASS both arithmetic+provenance) |
| #5 step64000 dose at n=3 | **Done** (§8.4 L307) |
Plus the evidence-clarity FAIL (single-order Fig 8 mislabeled) is fixed. This is a thorough, good-faith revision.

## 2. Does the training result survive the new disclosures? Yes — as a bounded claim.

I reconfirmed, from `full6-s1234/core4-s2/core4-s3.json`: ref 3.1827, bf16 3.2059, bf16+B(x) 3.1622, mean-only 3.1561; per-order bf16−B(x) gaps 0.0387/0.0416/0.0509, mean **0.0438**, half-range 0.0061 (**7.2×**), sign-consistent. MXFP8 diverges (4.78) and B(x) rescues to 3.45. Grad err (global_rel) bf16 1.48→0.656, B(x) 0.288→0.086. Qwen3-1.7B worst-head key-mean ratio **63.4×** (matches). All measured, all reproduce.

Three disclosures, weighed:
- **Transient gap** (peak +0.057 @ step300 → +0.044 @ step1000): *weakens* the "accumulating divergence" reading but the paper reframes correctly as faster recovery from a bad-gradient checkpoint, and flags the endpoint overstates steady state. Survives, downgraded in ambition.
- **Dose null at step64000**: this is a *strength*, not a wound — the correct causal control (B(x) cuts grad error ~20× there yet moves loss by nothing, because AdamW already absorbs a 30% error). It is the cleanest evidence in the paper that the benefit is caused by bad rounding.
- **Mild Qwen3-1.7B / failed prereg**: the real blow. The one current-model test of the *training-gradient* blowup shows the precondition present (63×) but error mild (1.9%→1.1%). Consistent with §5.2 (Qwen3's invariant is the QK-norm gain, not an additive key mean), but it means the training-side failure this paper fixes is **bounded to the large-additive-key-mean regime (≤410M Pythia)** and is *evidenced-against* on a 2026 architecture. The numerical result stands; its frontier relevance does not.

## 3. Is the story coherent? Mostly.

"Swamping = invariant + content, round in native coords, mantissa spent on invariant" genuinely unifies three of four failures (rotation §3, affine §5, key-mean §7–8) as *one operation* (invariant removal). The 2^24 cliff (§4) is honestly carved out as a distinct **range** (integer-bit) story — the paper says so plainly (L23, L34, L89). So the *body* is coherent and self-aware; the **title's "One Mechanism Behind Four Failures" / "one recipe fixes all four" over-asserts** relative to the body's own "three mechanically distinct steps." Secondary tension: for Qwen3 the inference-damaging invariant (gain) and the absent training failure are *different* invariants, so "the identical operator repairs inference drift and a training gradient" is demonstrated strongly only on the key-mean object, and that object's *loss* benefit only on Pythia-160m. The unification is real but thinner than the framing.

## 4. Would a lab engineer act on it? Partly — and the honest parts are the useful ones.

§11 is genuinely actionable. The immediately-usable, less-prior-art items: the **2^24 FP32-angle cliff + integer phase** (concrete, verified on 3 models), the **block-shift ≥16 rule** for context-shifting engines, and the **per-family invariant map** (Qwen2.5 additive bias vs Qwen3 QK-norm γ). The key-mean/affine levers largely re-confirm SageAttention/SmoothQuant/KVQuant/GProj (paper is honest about this in §9). The decision-relevant takeaway for a frontier trainer: *check whether your keys develop a large additive mean; if so, remove it pre-cast; current QK-norm models may not* — which is exactly what the paper now shows, and which a lab can test in an afternoon.

## 5. Top-5 must-fix (line refs)

1. **Abstract (L17–19) buries the most decision-relevant fact.** It leads with the 0.044 loss benefit and caveats only "not yet at scale," but never says the one current-model (Qwen3-1.7B) test of the training-gradient blowup came back mild / failed its prereg. A frontier reviewer reads the abstract to answer "does this happen in my models." Surface the current-model negative in the abstract, not only §7.4/§10.
2. **Title + banner overclaim (L9, L11).** "One Mechanism Behind Four … Failures" / "one recipe fixes all four" contradicts the body's own "three mechanically distinct steps" (L23) and the §4 range carve-out. Soften to "one mechanism behind three, plus a range fix," or add a one-clause caveat in the banner.
3. **Loss-mover attribution (abstract L19; §8.4 L293).** The headline 0.044 is the two-op B(x); but mean-only (0.050) ties/beats it and row-sum restoration is *inert* on the loss. "The per-head key mean, with its row sum restored" credits an op that does not move the loss. State at the headline that the loss mover is key-mean removal alone (SageAttention smoothing).
4. **Tie "no longer diagnostic-only at 160M" (L306, L327) to the §7.4 negative in the same breath.** As written, a skimmer takes the loss benefit as evidence the failure matters broadly. Append "…and only in the large-additive-key-mean regime; the one current QK-norm model tested shows no blowup."
5. **Flag thin evidence floors adjacent to the comparative headlines.** The "more format bits can be worse" log-polar leg (§2.3 L87, §8.2 L273, README headline 5) rests on **n = 2×48 tokens** — down-weight from a headline to a single thin probe. The loss benefit is **n=3 data orders with no stochastic-training noise floor** (deterministic seeds); say so where the 7× spread claim appears (L295).

## 6. Submit-readiness verdict

**Workshop (efficient-ML / MLSys-adjacent): submit now** — honest, reproducible, self-auditing; no experiment gated. **Main track: not yet.** The experiment the round-2 reviewer said would flip the verdict was run and answered *against* frontier relevance; the binding constraint is unchanged (≤1.7B, training blowup only ≤410M Pythia, synthesis-level novelty). The science is submit-ready as a *bounded* claim; land must-fixes #1–#4 (all writing) before any main-track submission. The only tier-moving work left is the owed ≥4B current-model run (needs >16 GB VRAM) — flagged, not fabricated. I raise the score to 7 on the strength of the resolution and the rigor of reporting a failed prediction, not on expanded impact.
