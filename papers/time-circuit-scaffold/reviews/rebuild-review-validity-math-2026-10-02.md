---
title: "Rebuild review — validity and mathematics"
type: reviewer-validity-math
date: 2026-10-02
paper: research/papers/time-circuit-scaffold/paper.md (commit 4214b0c)
companions_reviewed: reviews/architecture-math-2026-10-02.md; reviews/architecture-brief-2026-10-02.md
reviewer_scope: validity of evidence→claim alignment; independent math check; prereg-accuracy; cross-family role consistency
method: read primary FINDINGS / result JSON / worker + analysis code; derived every identity independently; did NOT run models; did NOT edit the paper
---

# Rebuild review: validity and mathematics

**Score: 6 / 10.**

The mathematics is clean — I re-derived every identity and found no algebra error. Numeric fidelity to the primary records is unusually high; of ~40 load-bearing numbers I spot-checked against FINDINGS/JSON/code, all but one provenance case matched. Most of the paper is admirably candid (Sections 10, 12, 13 disclose a lot). The score is held down by **one serious validity defect in the paper's titular property (Property 3, "state is formed over ordered execution")**: Section 5 presents a preregistered test whose *decisive* predictions FAILED as if it were a clean confirmation, and the one number that positively localizes formation (the "0.675" pre-band freeze) is imported from a different experiment where it was a below-threshold near-miss in one family and a fired falsifier in the other — and it directly contradicts the paper's own Section 13 and the companion paper. Plus a FLUX.2 control-number provenance mismatch and a few non-discrimination hedging gaps. These are fixable by honest reframing, not by new experiments; the thesis survives on an independent leg (the L12 seeding result). Details below.

Labels: **[measured]** = I traced it to a primary file; **[asserted]** = stated in paper, not independently re-measured here; **[derived]** = I reproduced the algebra.

---

## 0. Headline findings (most load-bearing first)

1. **MAJOR — Section 5, line 126.** The "preregistered band-internal test" paragraph is tagged "(prereg-frozen; Qwen and Gemma; single seed)" and framed as a confirmation of "formation over ordered execution, committed at the late band." In the actual prereg (`2026-10-02-formation-over-time/PREREG.md` + `results/FOT_analysis.json`):
   - The **decisive** prediction **P2a** (freezing the band's own attn+MLP drops rescue by ≥0.40 — "the band's own computation builds the transplantable store") **FAILED in both families** (Qwen value −0.033, Gemma −0.038). The companion falsifier **F2** ("freezing the band leaves the store intact ⇒ present at band entry / pure propagation, *vindicating the reviewer*") **FIRED in both**.
   - **P3b** (cross-position formation) **FAILED in both**; falsifier **F3b** ("built within the subject token's own residual, NOT across positions") **FIRED in both**.
   - **P1c** (graded monotone ramp) and **P2b** (monotone band-freeze) also failed.
   The paper reports the *directions* of these outcomes honestly (distributed commit; band not forming; consumer reads subject) but **does not disclose that the prereg's decisive predictions failed and its falsifiers fired.** A reader cannot tell that "prereg-frozen" here means "the prereg's main new predictions were falsified and the thesis was refined post hoc." The refinement (formation is pre-band, band is commit) is *theory-consistent* with the author's thesis and is legitimate — but it must be presented as a falsified-and-refined prereg, not a confirmed one.

2. **MAJOR — Section 5, line 126, the "0.675" sentence.** "the content is built over the preceding depth, family-dependently: freezing the pre-band layers 13 to 21 cuts the Qwen rescue from 0.871 to 0.675." This number is **not in the formation-over-time experiment at all** (its `report.json` has no pre-band-freeze arm; `FOT_analysis.json` has no 0.675). [measured] It is the companion experiment `2026-10-02-p1-reviewer-experiments/results/A_analysis.json`, field `rescue_late_freeze_mid` = 0.67465 (Qwen), where:
   - the preregistered prediction `P_A4_freeze_breaks` = **False** — the pre-band contribution was 0.197, **below the preregistered 0.20 threshold**, which the *companion paper* reports as "a near miss ... not demonstrably built by the intervening layers";
   - in **Gemma** the identical freeze is a no-op (`rescue_late_freeze_mid` = 0.98994, drop −0.005) and `F_A4_freeze_noop` = **True** — the freeze-no-op **falsifier fired**; the companion concludes "The construction leg is unsupported in both models" and "consistent with construction happening *inside* the late band layers themselves."
   So the one datum Paper 2 uses to positively localize formation to pre-band depth is a leg that (a) fell below its own prereg threshold in Qwen, (b) fired a null falsifier in Gemma, (c) is given the *opposite* interpretation by the companion paper, and (d) is tagged "prereg-frozen" under a prereg that does not contain it. "family-dependently" silently stands in for "the claim has zero support in Gemma (null falsifier fired)."

3. **MAJOR (internal contradiction) — Section 5 (line 126) vs Section 13 (line 255).** Section 13 says: "The pre-band subject-position freeze could not see formation inside the band or across positions, so its near-null is uninformative and licenses no 'construction unsupported' conclusion." Section 5 uses the *same* pre-band freeze as positive evidence that "content is built over the preceding depth." The paper cannot have it both ways: the same measurement is "uninformative" in the appendix and load-bearing in the body. (The FOT prereg exists *precisely because* the validity audit declared this leg uninformative; see `PREREG.md` lines 19-31.)

4. **MODERATE (provenance) — Figure 1 (line 38) and Section 9.1 (line 186).** The FLUX.2 control MAEs "wrong source 57 to 88, wrong sign 64 to 97, row permutation 7 to 11" do **not** match the report bundled as the FLUX.2 row of the 21/21 join (`flux2-klein.json`), which measures wrong-source 54.5/94.0/94.3, wrong-sign 60.0/79.5/89.3, **row-permutation 4.6/7.9/22.8**. [measured] The paper's quoted ranges are from an earlier, non-IR FLUX.2 panel (seeds 260902/260903, `sources/portability-findings.md` lines 80-82). The qualitative story holds, but the **row-permutation upper bound in the bundled report is 22.8, not 11** — materially weakening the "near-invariant" claim the paper draws from "7 to 11," and the cited numbers should either be re-sourced to the panel they came from or replaced with the bundled report's numbers.

5. **MINOR but worth fixing — math doc §8 and paper §10 omit prereg P2.** The mamba-clock-retest's preregistered *discriminator* P2 ("retention beats a matched write") was nominally **4/6 TRUE** (a near-tie, ≤0.07 nats), yet both the paper and the math doc state only P1 (0/6), P3 (1/6), P4 (0/6). The verdict (`RETENTION_NOT_COMMIT_LEVER`) is correct and fired on P1, but a prereg's own named discriminator going 4/6 the *other* way (within noise) should be reported, not dropped.

Everything else below is largely sound.

---

## 1. Evidence → claim alignment (per spine experiment)

Format: **(a) claim · (b) what the instrument computes · (c) discriminating?** Verdicts are against the thesis vs the *named* alternative. "✅ discriminating," "⚠️ non-discriminating / proxy," "➖ custody/parity (not a discovery — paper agrees)."

### Property 1 — reusable interfaces host different computations
- **Qwen one fixed L22–27 interface serves color/position/identity (16/16, 12/16, 11/11).** (b) [measured, `qwen-scaffold-context-poc`] isolated K/V-span swap at a *prospectively fixed* band; native greedy continuation / full-vocab top-1; no site reselected per op. (c) ✅ discriminates against "per-input sites / no reuse" (which predicts each op needs its own reselected site).
- **FLUX same-organization profile 0.913 vs 0.734; late seam 8/9.** (b) [asserted] causal-profile cosine across paraphrases. (c) ✅ reuse vs per-input.
- **SSM store relative depth 0.69–0.83 (L20/L39/L44); 7B store L19–27.** (b) [measured, consistent] write-gain / block localization. (c) ⚠️ **non-discriminating on its own** — this is the paper's own Level-3 "recurring physical sites," which the Section 2 table says "may reflect depth, scale, or a generic bottleneck." It appears in the main body (Section 3) with no inline cross-reference to the Section 13 "location is a weak symptom" caveat. A generic late bottleneck recurring at fixed relative depth predicts the same. **Flag: add the caveat inline so it is not read as discriminating.** (It is *not* the same statistic as the per-fact commit SD — that one is correctly confined to Section 13.)
- **Falcon-H1 hybrid: store lowers to attention side; SSM writer not found.** (b) [asserted] isolated cuts both sides. (c) ✅ disclosed failed prediction, correctly.

### Property 2 — context and operation select participation
- **Same byte-identical patch, different query → 3.130 / 0.583 / 3.021 nats, 16/16; 128 pairing checks.** (b) [measured] `analyze.py:302` `query_selective_harm = unselected − selected`, where both forks share the same parent StateCut and the same patch tensor digests (128 digest-pairing checks confirm byte-identity); only the native question changes; cross-query (not within-row two-donor) contrast. (c) ✅ **the cleanest discriminator in the paper** — a content-additive / steering-vector model predicts ∂authority/∂query = 0; measured 16/16 positive. Aligned and correctly in the spine.
- **Per-item reader cosine 0.74–0.99 within-op vs 0.20 across-op.** (b) [measured, agent-verified in code] the profile is a vector of **signed causal single-site K/V-cut effects on the answer log-prob** (`per_item_worker.py:126-153` `fine_iso_cut`; `phase3_analyze.py:40,52-61`) — NOT attention mass. Numbers match `phase3_relational_analysis.json` exactly. (c) ✅ aligned (causal profile, not a proxy). **Two honest caveats to surface:** (i) within-op numbers are per-item pairwise medians while across-op numbers are op-*mean* cosines — the headline 0.99→0.20 gap compares two different operationalizations; (ii) the paper already discloses identity~color does not separate (0.842/0.911). The "variance-ratio 11×" proxy is correctly superseded (Section 13, line 253) and the clean 20-country design underlies the cosine.
- **Head/edge map: within-binding 0.947/0.927/0.961, cross-op 0.336; attention mass only 0.61–0.70.** (b) [measured, agent-verified] `delta_target_logprob` cut profile (causal) vs `target_span_probability` (attention mass, used *only* as an explicit less-stable contrast). (c) ✅ aligned; the causal-vs-attention contrast is exactly the right control.
- **Address-vs-payload SDXL factorial; Δ_{K×V}=0.3413.** (b) [measured, `qkv-factorial.json`] "image-axis progress" α = ⟨I−I₀, I₁−I₀⟩/‖I₁−I₀‖² (`verify.py:80`) — a **1-D projection diagnostic, not semantic quality** (paper states this). (c) ✅ for the sign/pattern of the interaction (matches the exact attention identity); ⚠️ the *scalar* is not meaningful and the paper correctly says so.

### Property 3 — state formed over ordered execution (the time axis)
- **E20 source→formed store: block 0.924 / rescue 0.871 / wrong 37/42; cross-family 0.768·0.985 / 0.740·0.910 / 0.728·0.713; 7B 0.595·0.770 / wrong −0.026.** (b) [measured] isolated prefix→suffix K/V transplant, normalized by each row's own seed gain. (c) ✅ discriminates "read-off-source / no formation" (early K/V or linear seed-image does not rescue; a native-layer seed does, 16/16). **This is the real backbone of Property 3 and it is solid.** The isolated-vs-in-forward hygiene (0.985 vs 0.009 at L0) is verified in the companion (E17). The L12-seed→native-layers→rescue result is genuine "formed over depth" evidence independent of any freeze leg.
- **Formation-over-time band-internal test (Section 5, line 126).** See Headlines 1–3. (c) The seeding/transplant legs are ✅; the "where formation happens" narrative is **misrepresented** — the prereg's decisive predictions failed, and the positive pre-band localization leans on a misattributed, below-threshold, Gemma-falsified number that Section 13 itself calls uninformative.
- **Diffusion install-timing: early P=0.5772 (blue) vs late 0.0689 (violet); first-call lesion MAE 20.82 vs late-call 2.15.** (b) [measured] source install/lesion at different denoising calls; α + MAE. (c) ⚠️ **weakly discriminating.** The math doc §7 itself derives this from *standard* coarse-to-fine denoising ("at high σ only coarse structure is unresolved… at low σ coarse structure is fixed"). So the result is expected under plain diffusion dynamics and does not uniquely separate "role scaffold" from "diffusion is coarse-to-fine." It supports "there is ordered carried state" (near-definitional for diffusion). **Flag: label as illustration, not discrimination.**
- **Temporal closure: program 0.712, register 0.403, both exact.** (b) [measured, `temporal-closure-summary.json`] separate installation of current program vs carried register. (c) ✅ stronger than install-timing — shows program and history are *separately* manipulable and must agree (the "carried state must agree with current operation" claim).
- **Mamba transition composition 3/3 vs endpoint-sum 0; L0→writer donkey +4.59 / Vienna +7.65, restore removes 90.3%/91.6%.** (b) [measured] staged recurrent transitions vs additive endpoints; conv-dominant disclosed. (c) ✅ composition discriminates "endpoint-sum" (fails whenever ρ≠1). Honest caveat preserved: Vienna is continuation recovery, not top-1; conv-dominant at the tested cut.
- **FLUX four-quadrant certificate.** (c) ⚠️ the paper correctly says "a weighted-additive profile also passes all four quadrants" → **non-discriminating**, presented as a subtype, not proof. Correct demotion.

### Property 4 — newly written state changes later reads
- **Two-update France→Germany (1/3 held + dev); route→write→future key-only exact; history×row 4-cell.** (b) [measured, `scaffold-graph-identification`] 2×2 history×row with the France token held visible; retained-history SSE 0.0995 vs serial 2.7024 vs any-edit 1.2574 (confirmed in FINDINGS). (c) ✅ the pre-update-intervention design (needed to separate serial from fork) is correct; history-dominated consumer with an opposing row term. Honest about n=4, no significance claim. The "new row opposes" framing slightly overstates a −0.01…−0.15 effect, but it is disclosed with per-context numbers.

### Property 5 — scaffold predicts held behavior
- **Frozen 24-coord relation profile: mapped cos 0.954 vs 0.566, RMSE 0.029 vs 0.149, 8/8.** (b) [measured, `qwen-predictive`] profile + 3 competitors frozen before any held context opened. (c) ✅ genuinely prospective; disclosed misses (color 5/8, identity readout-limited, size unavailable). Good.
- **Mamba 27-coord: capital 8/8 (0.9941 vs 0.9880), delayed identity 4/4.** (c) ✅ prospective; note the capital margin (0.9941 vs 0.9880) is thin, as stated.
- **Cross-family core RMSE 0.0928 vs 0.8526.** (c) ⚠️ "suggestive edge on a small denominator," correctly not sold as a shared graph.

### Property 6 — lives in trained weights
- **v_proj permute collapse (0.955→0.049); null nets top-1 0/96; +0.350 random-init miss; Pythia trend; continuation +0.445 vs ~0 (but Mamba wrong-label +0.448).** (c) ✅ dependence result, honestly bounded ("incompetent nulls ⇒ learned-not-generic, not scaffold-vs-competent-net"; the +0.350 random-init win and the +0.448 wrong-label mover are both disclosed as failed/specificity-limited). Correct.

### Property 7 — model virtual machine
- **Scene compiler 21/21 RGB-exact; wrong-source/sign controls.** (b) [measured] decoded-array + SHA256 equality gate (`verify.py`), not a progress proxy. (c) ➖ exactness is **architectural custody/parity, not a discovery** (prompt reaches denoiser only through K/V+pooled) — the paper says this plainly. Load-bearing discoveries are the factorization / address≠payload / time-indexed authority (measured with α+MAE, which are soft diagnostics — disclosed). See Headline 4 for the FLUX.2 control-number provenance issue.
- **XNOR hostile inversion 148/150 vs 0/150; XOR 148/150; IR 768/768.** (b) [measured, obsidian composite survey]. (c) ✅ strong discriminator vs "additive steering vector" (a steering vector would not invert with the program).
- **Frozen-site install 1.011 vs wrong-site −0.133 vs shuffled −0.607; archive 4/4 vs 0/4; fork/replay bit-exact 0/96 reads; ancestry 6/6 vs 1/6.** (c) ✅ ancestry 6/6 vs 1/6 discriminates "bag-of-facts / Mount=Prefill." Fork/replay exactness is the complete-state theorem made executable (see §2f below).

**Misaligned proxy used in the main body:** the pre-band freeze "0.675" (Headlines 1–3). **Non-discriminating items in the main body that should carry an inline caveat:** SSM relative-depth recurrence (Property 1) and diffusion install-timing (Property 3). **Aligned test wrongly demoted:** none found — the Section 13 demotions (commit-SD, variance-ratio, sliding-window, function-vector, random nulls, A-only dose) are all genuinely non-discriminating (verified). The anomaly is the *opposite*: the pre-band freeze is demoted in Section 13 yet used positively in Section 5.

---

## 2. Mathematics — independent verification

I re-derived each result from scratch. **All are correct; no algebra error found.**

### (2a) Attention key/value/joint identities and the K×V interaction — ✅ [derived]
With base weights α_j, output o=Σα_j v_j, E=e^{q·Δk/√d}, D=1+α_s(E−1):
- Key change renormalizes: α_s→α_sE/D, α_{j≠s}→α_j/D, giving **Δo^K = α_s(E−1)(v_s−o)/D**. ✓
- **Δo^V = α_s Δv.** ✓
- **Δo^{KV} = (α_s/D)[(E−1)(v_s−o) + E Δv].** ✓
- Interaction: Δo^{KV}−Δo^K−Δo^V = α_sΔv(E/D−1) = α_sΔv(E−D)/D, and E−D=(E−1)(1−α_s), so **= α_s(1−α_s)(E−1)/D · Δv.** ✓ Matches the paper and math doc exactly. Non-zero iff both operands change and 0<α_s<1; positive along Δv iff E>1. ✓ The prose ("K re-weights, bounded by v_s−o, saturates as the weight→1; V adds linearly, gated by α_s") is correct: as E→∞, Δo^K→(v_s−o) and α_s'→1. ✓
- SDXL factorial interaction: 1.0−0.66201−0.71808+0.72139 = **0.3413**. ✓ [measured in `qkv-factorial.json`]

### (2b) Four-cell identities — ✅ [derived]
Standard 2×2: b_0=Y_{10}−Y_{00}, r_0=Y_{01}−Y_{00}, i=Y_{11}−Y_{10}−Y_{01}+Y_{00}, τ=Y_{11}−Y_{00}=b_0+r_0+i=b_0+r_1=r_0+b_1 (with r_1=Y_{11}−Y_{10}, b_1=Y_{11}−Y_{01}); and i=r_1−r_0. All check. ✓ Measured per-context (history +1.294/+1.279/+1.576, row −0.030/−0.035/−0.014, with a negative-to-~0 interaction so that τ=+0.957…+1.425) is internally consistent with the identity.

### (2c) Mamba unrolled recurrence and A-dose sensitivity — ✅ [derived]
h_T = (Π ρ_j)h_{t0} + Σ_i(Π_{j>i}ρ_j)w_i, with ρ_j=exp(Δ_jA) ⇒ R_{i:T}=exp(A Σ_{j>i}Δ_j); R=exp(AΣΔ), elapsed clock c=−logR=−AΣΔ>0 (A<0). ✓ Scaling c→kc gives R'=e^{−kc}, so the carried contribution scales by **e^{−(k−1)c}.** ✓ The dose panel is right: A_log+=log k ⇒ A→kA ⇒ ρ→exp(AkΔ), write unchanged (clock-only); Δ×k is joint; b×k is write-only. ✓ Bound: c∈[0.03,0.07], k∈{0.5,2} ⇒ factor ∈[e^{−0.07},e^{0.035}] ≈ [0.93,1.04], "≤7%." ✓ Discriminating dose k≈c_ctrl/c_writer∼15–150; retest used γ=15–142. ✓

### (2d) Joint row-permutation invariance — ✅ [derived], correctly flagged as empirically only near-invariant
Softmax attention over a *set* with no positional term in the keys is exactly invariant to a joint permutation of (k_j,v_j) pairs (reindexing the same summation). ✓ The caveat "no positional term in the keys" is stated. The measured 0.859 (not 1.000) is honestly flagged as an open check to run in fp64, with correct candidate causes (unpermuted padding/pooled rows; reduction-order non-associativity). Good — the theorem is right and the gap is disclosed, not hidden.

### (2e) Flat-plateau argmax SD ≈ 1.7 — ✅ [derived]
For i.i.d. noise on a perfectly flat 6-layer band, the argmax is Uniform{1..6}; Var=(6²−1)/12=35/12, SD=√2.9167=**1.708**. ✓ The non-discrimination argument is valid: both "flat plateau under the thesis" and "each context recruits its own layers" predict large SD, so the SD statistic cannot separate them. Measured trained SDs (1.16, 1.60) sit at/under the plateau value. Correctly used as a reason the commit-SD check is non-discriminating, "for scale, not a test."

### (2f) Complete-state theorem and VM exactness — ✅ [derived], with a caveat on where the weight lies
For deterministic X_{t+1}=F_θ(X_t,z_{t+1}), Y=G_θ(X_T,q): if two runs share a *complete (Markov)* X_t and all future inputs, induction gives identical futures. ✓ The theorem is **near-tautological** — its entire force is the empirical claim that the externalized StateCut *is* the complete state, which the bit-exact fork/replay/resume (Qwen 32-tok, Mamba 64-tok, 0/96 checkpoint reads) verifies. The paper uses it correctly: 21/21 diffusion and VM exactness are treated as custody/parity, not discovery. Corollary 2 (stale writer: matched immediate output, divergent carried state ⇒ divergent future) is trivially valid and matched by the SDXL control. The ε-sufficiency "architectural (diffusion) vs learned (AR band)" distinction is sound.

**Math verdict: everything checks. The identities, the recurrence, the sensitivity, the invariance theorem, the plateau SD, and the completeness theorem are all correct.** The only math-adjacent flag is presentational (2f is near-tautological; the evidentiary weight is the empirical completeness check — the paper already treats it that way).

---

## 3. Prereg accuracy (task 3)

### Mamba clock retest (`2026-10-02-mamba-clock-retest`) — ✅ accurately described
Paper §10 (line 210) and math doc §8 match the primary record: γ=15–142; write arm ‖ΔH‖-matched; release hurts **0/6**; identity release *raises* the margin; dt via write **6/6**, via retention **0/6**; writer-specific **1/6**; verdict `RETENTION_NOT_COMMIT_LEVER`. All [measured] against `FINDINGS.md` + `results/summary.json`. Canaries (no-op 0.0, store-equiv ≤6.6e-7, batch parity ≤3.7e-4, write match-ratio 1.000) are correct. **One omission (minor):** the prereg's named discriminator **P2** ("retention beats matched write") was 4/6 TRUE (a ≤0.07-nat near-tie); the verdict legitimately fired on P1, but P2 should be reported, not dropped, since a prereg's own discriminator going 4/6 the other way (within noise) is exactly the kind of thing readers should see.

### Formation over time (`2026-10-02-formation-over-time`) — ⚠️ inaccurately described (see Headlines 1–3)
What the prereg actually returned (`FOT_analysis.json`, both families):

| Prereg item | Prediction | Result | Paper's treatment |
|---|---|---|---|
| P1a full ≥0.70 | thesis | PASS | reported (implicitly) |
| P1b no single ≥0.90×full | thesis | PASS (max 0.732/0.804) | reported ✅ |
| P1c graded monotone ramp | thesis | **FAIL** (monotone false) | not disclosed |
| **P2a band builds store (≥0.40 drop)** | **decisive** | **FAIL** (−0.033 / −0.038) | reported as positive ("band's own computation is not what forms the content") without noting P2a failed |
| P2b band-freeze monotone | thesis | **FAIL** | not disclosed |
| **F2 band-freeze leaves intact** | **falsifier** | **FIRED** both | not disclosed as a fired falsifier |
| P3a consumer reads subject | thesis | PASS | reported ✅ |
| P3b cross-position formation | thesis | **FAIL** | not disclosed |
| **F3b built within subject token, not across positions** | **falsifier** | **FIRED** both | not disclosed |

The pre-band freeze ("0.675") is **not part of this prereg**; it is `p1-reviewer-experiments/A_analysis.json` (`P_A4_freeze_breaks`=False in Qwen; `F_A4_freeze_noop`=True in Gemma). The thesis is not refuted by any of this — "formed over ordered execution" is carried by the independent L12-seed leg (16/16; early K/V 0/15), and a refinement to "formation pre-band, band commits" is theory-consistent. But the paragraph must be rewritten to say so honestly.

---

## 4. Cross-family role mapping consistency (task 4)

Within the **paper itself**, the role lowering per family is **consistent** [measured, read across the paper + math doc]:
- **Diffusion:** source = compiled K/V + pooled S; reader = queries from evolving residual; writer = Φ (latent update); carried state = latent + scheduler history; consumer = VAE/RGB renderer R. Consistent in paper §9.1 and math §2/§7. (Minor within-doc symbol reuse in the math doc: C(p,n) the conditioner vs C_m the consumer role — the diffusion consumer is unambiguously R, so no cross-doc conflict.)
- **AR:** writer = depth up to band entry; commit = band projections; carried state = K/V cache; reader = consumer attention at subject position; consumer = native logits. Paper §5 and math §3.2 are word-for-word; **no doc calls the band the writer.** Consistent.
- **SSM:** commit lowers to the **writer W**; retention/transition T not load-bearing (per the retest); carried state = channel states + conv buffer; consumer = native logits. Paper §10 and math §8 agree.
- Functional form a_t=A/w_t=W/z_{t+1}=T/y_t=C and the Mamba channel eq h_t=ρ_t⊙h_{t−1}+w_t, s_t=⟨c_t,h_t⟩+Du_t are identical across paper, math doc, and brief.

**One contradiction, in a support doc:** the **architecture brief** (line 66) still says the Mamba retention "causal role is untested; tonight's dose did not test it," never assigns the SSM commit to the writer, and does not mention the retest. The paper and math doc treat the retest as the resolving experiment. The brief is sourced from pre-retest material (its header) and is simply stale on this one point. It does *not* call T/retention the commit lever, so this is tested-and-resolved (paper/math) vs untested (brief), not a genuine disagreement about mechanism. **Fix: update brief line 66** to match paper §10 (commit → W; retention a measured correlate, not load-bearing). The one subtlety that is *correctly* handled everywhere: "commit" lowers differently per family (AR: commit ≠ writer; SSM: commit = writer W), consistent with the declared partial/many-to-many lowering.

---

## 5. Fixes (in priority order)

1. **Rewrite the Section 5 band-internal paragraph (line 126) to report the prereg honestly.** State that P2a (the decisive band-construction prediction) failed in both families and the F2 falsifier fired; that P3b failed and F3b fired (formation is within the subject token's residual, not across positions); and that the paper therefore *refined* the thesis to "formation over pre-band depth, band = commit." Keep the tag as "preregistered, decisive predictions falsified, thesis refined," not "prereg-frozen" confirmation.
2. **Fix the "0.675" provenance and framing.** Attribute it to `p1-reviewer-experiments` (not the FOT prereg), state the Qwen contribution (0.197) was *below* its 0.20 prereg threshold, and that the Gemma freeze-no-op falsifier fired (zero pre-band support in Gemma). Remove "family-dependently" as a euphemism, or spell out that Gemma shows no pre-band construction. Acknowledge that the companion paper draws the opposite localization from this datum.
3. **Resolve the Section 5 / Section 13 contradiction** about whether the pre-band freeze is informative. Pick one: either it is uninformative (then drop it from Section 5) or it is weak-positive (then soften Section 13 and disclose the threshold/Gemma failure in both places). It cannot be both.
4. **Re-source or correct the FLUX.2 control MAEs** (Figure 1 caption line 38; Section 9.1 line 186). Either cite the earlier seeds-260902/260903 panel they came from, or use the bundled `flux2-klein.json` numbers (wrong-source ~54.5–94.3, wrong-sign ~60–89, row-perm ~4.6–22.8) — and note the row-permutation upper bound is 22.8, not 11, which weakens "near-invariant."
5. **Report mamba-retest P2 (4/6 near-tie)** in §10 and math §8.
6. **Add inline non-discrimination caveats** to the SSM relative-depth recurrence (Property 1) and the diffusion install-timing (Property 3), cross-referencing the Section 2 claim-levels table and the math doc §7 coarse-to-fine derivation respectively.
7. **(Reader cosine, optional)** note that the within-op (per-item) and across-op (op-mean) cosines use different operationalizations, so the 0.99→0.20 gap is not a single statistic end-to-end.
8. **Update brief line 66** to the resolved Mamba commit/retention status.

---

## 6. What I could not verify / did not re-run

- I did **not** run any model; all "[measured]" items are traced to existing FINDINGS / result JSON / worker code, which I read.
- The FLUX same-organization 0.913/0.734, the Pythia developmental trend, the Falcon-H1 hybrid numbers, the archive-page 4/4, and the external-page/fork bit-exactness are **[asserted]** here — I accepted the paper's numbers without opening every primary file (budgeted to the load-bearing and contested claims). A full-corpus number-by-number audit already exists in `reviews/evidence-inventory-2026-10-02.md` and `reviews/validity-audit-2026-10-02.md`; this review did not re-derive those and focused on (i) independent math, (ii) the two preregs, (iii) the Property-2/3/7 instruments, and (iv) role consistency.
- The 0.675 contradiction and the FLUX.2 provenance mismatch are the two findings I am most confident change how a careful reader should weight Sections 5 and 9.1.
