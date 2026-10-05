---
title: "Theory assessment: is there enough for a strong, attention-getting paper?"
type: theory-assessment
date: 2026-10-02
reviewer: "Opus 5.5 (claude-opus-5-5), senior-interp-researcher frame, at the author's request"
scope: "Paper 2 (time-circuit-scaffold) + reviews/, Paper 1 (time-formed-circuits), the 2026-10-02 experiment round, earlier 10-01 evidence, the living-theory post and the original outline"
method: "Read-only. No models run and no heavy computation. I read every primary listed in the brief and re-checked the load-bearing numbers in result JSONs (rp1_scorecard.json, residual-program-v2 scorecard_qwen15it.json, FOT_analysis.json, run_sae_comparison.py templates). Labels: MEASURED = read in a primary FINDINGS file or result JSON; COMP = computed here from primary numbers; INFERRED = my reasoning; PRIOR = my recollection of the literature (verify citations before use)."
---

# Theory assessment: dynamic circuits on a stable time scaffold

## 0. Three findings from re-reading the primaries that change the picture

These came out of the primaries, not the summaries. Where the two disagree, the primary wins.

1. **The hop-depth law does not replicate, and it never had more than one organism per hop count. Neither does the stale-pointer→competitor signature.**
   - In the base run, the P8 ladder `l* = 22 > 20 > 16` is built from one organism per hop count, all from lexical set 0. The code is `analyze_rp1.py`, which builds the ladder from organisms whose IDs start `P-hop`.
   - The other competent one-hop base organisms have `l*` of 20, 22, 16, 20 and 20. That range already overlaps the single two-hop value of 16 (MEASURED, `saturn/experiments/2026-10-02-residual-program/results/rp1_scorecard.json`).
   - The residual-program v2 instruct arm has landed. Qwen2.5-1.5B-Instruct ran with 46 competent organisms (MEASURED, `saturn/experiments/2026-10-02-residual-program-v2/FINDINGS_qwen15it.md`, verified against `results/scorecard_qwen15it.json`):
     - **`l*` by hop count is 22 / 22 / 23** (n = 7 / 18 / 10), so it does not decrease.
     - A late clean K+V install at the anchor lands on the **competitor in 0.0** of 28 cases and recovers **clean in 0.89**.
     - Above `l*`, failures go to the donor in 23 of 34 and to the competitor in only 2 of 34.
   - The living-theory post still lists both claims under MEASURED. The Gemma arm of v2 is still pending (only smokes exist).
   - The v2 file has no coordinator custody note yet. I treat it as an agent-written primary and checked it against its JSON.
2. **The core transformer evidence comes from one templated in-context copying task.** E20 uses `"A photorealistic {subject} {pose} in {scene}. The animal in this picture is a"` (MEASURED, `saturn/experiments/2026-10-02-e20-cross-family/run_sae_comparison.py:115`).
   - The answer is the subject token itself, which sits in the context. Color is also read back from context.
   - The IIA test covers identity and color only. Position admitted 0 rows and the held-out `size` operation admitted 4 (MEASURED, `2026-10-02-fixed-lowering-iia/FINDINGS.md`).
   - The pillar is therefore "how an in-context entity attribute is read back", not factual recall in general. This is the largest scope gap.
3. **The full routing freeze is close to a tautology, and that is the premise of attribution graphs, not a discovery.** The raw-readout successor says so itself: "conditional affinity is expected once that freeze is implemented correctly. It does not independently establish a learned scaffold" (MEASURED, `2026-10-02-routing-readout-correction/FINDINGS.md`).
   - Freezing attention patterns and normalisation denominators to linearise the model is exactly how attribution graphs are built (PRIOR: Ameisen et al. 2025).
   - The empirical content that remains is the apportionment. In base, attention-only freezes leave 0.067 / 0.017 / 0.200 of the interaction and gate-only freezes leave 0.019 / 0.000 / 0.005. In instruct, attention-only removes a median 0.958 and gate-only a median 0.99, each at ≥80% in 13/14 cells.

Smaller custody notes:
- The custody review flagged the SDXL "20.82 vs 2.15" late-call lesion as unsourced. It is sourced: `research/demos/docs/scene-generator-paper.md` §5.2 gives "MAE 2.1535, compared with 20.8215 for the early lesion".
- The FLUX.2 control MAEs and the "pre-band freeze 0.675" sentence have already been corrected in the current `paper.md`.

---

## 1. Verdict

**Not yet.** There is not enough for a strong, attention-getting paper on a *theory of model computation architecture*.

There **is** enough, with about 3–5 hours of cheap, targeted runs, for a solid and well-defended empirical paper on a narrower claim. That claim:
- A transformer keeps the fact it is about to say in a fixed, findable late K/V band at the subject position.
- The content is formed before the band, committed there, and read by the answer position's attention.
- The band can be located blind from one forward pass.
- It is conserved under heavy continued pretraining, with an asymmetric code.
- MLP-transcoder attribution graphs largely miss it.

Why the umbrella theory is not yet a paper:
- **It is not falsifiable at the top level.** "A fixed machine runs a per-input program that reads and writes carried state" describes every residual-stream transformer, every diffusion sampler and every recurrent model by construction. The frontier review made the same point, and nothing since answers it, because no tested *competent* network fails to have a scaffold.
- **The falsifiable sub-claims that held** are:
  - the E20 dissociation;
  - IIA at its ceiling;
  - the blind locator;
  - query selectivity;
  - pointer/value separation;
  - fine-tune conservation.

  Each is either a causal refinement of a known stage picture (Geva et al. 2023's attribute extraction by upper-layer attention to the subject) or narrow in task scope.
- **The two most theory-distinctive AR claims both failed to replicate** in the first larger, different-checkpoint run. These are the hop-depth deadline and stale-pointer→competitor (§0.1).
- **The "three families" breadth is vocabulary-level.** The cross-family common graph is a measured null: the connected forecast ties additive (MAE 0.015099), and the role-matcher gap is 0.0386 (MEASURED, Paper 2 §10). Diffusion timing is the generic coarse-to-fine schedule. The SDXL lock-in L1/L2 predictions are falsified under the frozen readout (MEASURED, `2026-10-02-sdxl-relation-lockin/FINDINGS.md`, coordinator note). Mamba is a separate story about which layer writes.

**Scores**

| Version | Top interp venue (ICLR/NeurIPS main track, mech-interp) | Would a frontier-lab interp team circulate it? |
|---|---|---|
| Paper 2 as currently written | **4/10** (a clear workshop accept; main-track reject on "true by construction + sprawling + small n") | **3/10** (rigorous but diffuse; the headline reads as vocabulary) |
| The consolidated paper of §5, with to-dos 1–4 landing positive | **6.5/10** | **6/10** (circulated as "a cheap way to find where facts are read, and it survives fine-tuning") |
| The same paper with the to-dos landing negative (e.g. parametric recall does not show the band) | 5/10 | 4/10 |

Why my scores are lower than the earlier frontier review's 6/10:
- that review took the numbers at face value and did not open the primaries;
- it predates the instruct non-replication;
- it did not weigh the single-task scope or the prior-art overlap with Geva's extraction stage.

**Confidence: medium, about 0.7.**
- High confidence in the evidence reading: I re-checked the numbers that carry weight.
- Medium confidence in the novelty calls: they rest on my recollection of the literature, and some 2025–26 work may be missing.
- Low confidence about how the venue will react to the scene-compiler and VM material. I have discounted it, and a systems-minded reviewer may value it more.

What the program does unusually well, and should keep:
- hashed preregistration;
- exact-replay canaries;
- the isolated-cut hygiene (0.985 in-forward vs 0.009 isolated at L0);
- disclosing failed predictions;
- the asymmetric-skepticism rule.

This is above the median for the field and will earn reviewer trust. The problem is what is being claimed, not how carefully it was measured.

---

## 2. The pillars

These are the minimum load-bearing claims that make a *scoped* theory solid. They are ordered by strength. P1, P2 and P5 carry a paper. P3 adds texture. P4 is a theorem plus a measured apportionment. P6 is diffusion-only and should be demoted.

### P1. Formation, commit and read are separable, and the formed late band independently authors the answer

**Claim.** In the tested entity-attribute readout:
- the answer-controlling content is present in the subject's residual stream before a late band;
- each band layer's K/V projections commit it into the subject-position K/V store;
- the answer position's attention reads it at the subject position;
- the formed band, transplanted into an unseeded recipient, authors the answer, and a wrong-identity band authors the wrong answer.

**Discriminating evidence (all MEASURED).**
- **Block and rescue, in six decoder families and at 7B:**

  | Cell | Block | Rescue | n |
  |---|---|---|---|
  | Qwen2.5-1.5B (development) | 0.924 | 0.871 | 42 |
  | Qwen2.5-1.5B (held-out identities) | 0.728 | 0.713 | 79 |
  | Gemma-2-2B | 0.768 | 0.985 | 42 |
  | SmolLM2-1.7B | 0.740 | 0.910 | 34 |
  | Qwen2.5-7B | 0.595 | 0.770 | 40 |
  | Pythia-1.4B (matched earlier band L13–17) | 0.97 | 1.46 | 83 |
  | Phi-2 | 0.515 | 0.892 | — |
  | OLMo-2-1B | 0.972 | 0.903 | — |

  Sources: `2026-10-02-e20-cross-family/FINDINGS.md`; `2026-10-02-scale-9b-scaffold/PAPER-SECTION.md` via the Paper 2 table; `2026-10-02-blind-scaffold-prediction/FINDINGS.md`; `2026-10-02-attention-band-locator/FINDINGS.md`.
- **Wrong-identity controls:** target top-1 is 0.00–0.06 and wrong-donor top-1 is 0.75–1.00 (e20 cross-family).
- **Rules out "read-off-source / no formation":**
  - the seed layer's own K/V restores −0.010 (Qwen) and 0.080 (Gemma);
  - the matched earlier band restores −0.028;
  - an L12 residual seed run through the native layers rescues 16/16;
  - an early fact-span K/V patch gives 0/15.

  Sources: Paper 1 §3.5; `2026-10-01-qwen-scaffold-context-poc/FINDINGS.md`.
- **Rules out "the band computes the content":** freezing the band's attention+MLP leaves rescue at 0.904 / 1.023, and the prereg's P2a failed in both families, so F2 fired (MEASURED, `2026-10-02-formation-over-time/results/FOT_analysis.json`).
- **The read site:** cutting answer→subject attention takes rescue from 0.871 to 0.010 (Qwen) and from 0.985 to 0.015 (Gemma). Cutting answer→other positions does not (same JSON, `test3_position`).
- **Rules out an attribution-graph-visible store:** a matched transcoder feature+error interchange moves identity 0.31, against 0.94 for a native K/V cut (Paper 1 §5, Gemma, n=12).

**Strength: strong** (measured in six families, at 7B, with hashed freezes and exact canaries), for this task.

**What it does not rule out (INFERRED).**
- **Geva et al.'s three-stage picture.** In that picture, subject enrichment happens at the subject position and upper-layer attention from the last token extracts the attribute. P1 is that picture with a stronger causal design: an independent unseeded-recipient rescue, plus the "band freeze does not matter" result. That refinement is real and publishable. It is not a new architecture.
- **"Distributed commit"** is generous in Qwen, where one layer, L23, carries 0.732 of the full-band rescue. OLMo-2 is near single-layer: L13 carries 0.894 of 0.903.
- **The "not a linear image of the seed" ridge test** fits 14 identities with leave-one-identity-out. With so few classes in a high-dimensional target, a linear map would struggle anyway, so it is weak support (INFERRED).

**Biggest hole.** Task scope. E20 reads back an in-context animal token, and the RP3 locus for such a lexical value is the L0 attention write at fraction 1.00 (MEASURED, `FINDINGS_rp3.md`). A reviewer will call this a copy/induction readout.

**Cheapest closer.** Run the identical nine-arm E20 panel and the locator on *parametric* recall, where the answer is not in context. Use Known-1000/CounterFact-style prompts, e.g. "The Eiffel Tower is located in the city of" → Paris, with filler subject substitution, in Qwen2.5-1.5B and Gemma-2-2B. That is 4 runs, about 40 minutes.
- A positive result moves P1 from "in-context readback" to "factual recall", which is where the ROME/MEMIT/Geva audience lives.
- A negative result is also informative: it would scope the scaffold to in-context retrieval and say so.

### P2. The read site is fixed, not per-input, and predictable without fitting

**Claim.** One frozen band lowering captures what per-example re-fitting can. Its location can be predicted blind from a single clean forward pass, where a depth-fraction rule fails.

**Discriminating evidence (MEASURED).**
- **IIA:** fixed/ceiling is 0.87 [0.74, 1.00] in Qwen and 1.00 in Gemma, pooled over identity and color. The wrong-role floor is 0.00 everywhere. Absolute IIA is 0.57 / 0.76 (Qwen identity/color) and 0.31 / 0.63 (Gemma), all below the 0.75 target (`2026-10-02-fixed-lowering-iia/FINDINGS.md`).
- **The depth-fraction rule failed blind on Pythia-1.4B.** At the predicted band, block was −0.28 and rescue 0.14 (`2026-10-02-blind-scaffold-prediction/FINDINGS.md`).
- **The attention locator, Phase A:** mean IoU 0.615 against 0.490 for the depth rule. On Pythia the peak is L16, the commit, with IoU 0.571 against 0.000. Gemma is biased about 3 layers early, scoring 0.364 against 0.444.
- **The locator, Phase B (blind):**
  - Phi-2 passes 6/6. Its peak L23 is the commit. Locator-band block is 0.515 against 0.065 for the depth band.
  - OLMo-2 passes 5/6, failing only S5 (distributed).

  Source: `2026-10-02-attention-band-locator/FINDINGS.md`.
- **Variants:** the locator curve is bimodal (L21–23 and L27) in all six Qwen2.5-1.5B variants (`2026-10-02-qwen-variant-circuits/FINDINGS.md`).

**Rules out:**
- a universal relative-depth law, the strong reading of Lad et al.;
- "the band must be re-found per example" — but only within the six-band ceiling (next point).

**Strength: adequate.** Moving to strong needs one hole closed.

**Holes (INFERRED from the primaries).**
1. **The IIA "ceiling" is a re-fit over six overlapping candidate bands** chosen by log P(counterfactual). It is not a genuinely per-input lowering: no per-row single layers, no head subsets, no learned alignment. Fixed/ceiling ≈ 1 therefore shows that the band choice is stable. It does not show that a per-input circuit cannot do better.
2. **Blind n = 2, with wide bands.** Locator-vs-true IoU is 0.125 (Phi-2) and 0.25 (OLMo-2) against single-layer true bands. On OLMo-2 the locator and depth bands nearly coincide, so only Phi-2 discriminates the two rules.
3. **The statistic, `Σ_h α(final→subject)·‖v·W_O‖`, is essentially Geva's attention-to-subject extraction locus** made fit-free. It is useful, but a reviewer will name the lineage.

**Cheapest closer.** Widen the IIA ceiling to every single layer and every contiguous band of width 2–8, plus per-KV-head subsets. That is 2 runs, about 20 minutes. If fixed/ceiling stays at or above 0.85, the "fixed not per-input" claim is earned against a real rival. Then extend the blind locator to 4–6 more models; see to-do 2.

### P3. Reads are query-selective, V carries the payload, and pointers live apart from values

**Claim.**
- The same stored bytes gain authority only when their attribute is queried.
- The value travels in V. A same-position K swap on a decided read does nothing.
- An alias position carries "which slot". The value is fetched from the anchor's committed slot at read time.

**Evidence (MEASURED).**
- **Byte-identical patch, only the question changes:** 3.130 / 0.583 / 3.021 nats, each 16/16, with 128 digest checks (`2026-10-01-qwen-scaffold-context-poc/FINDINGS.md`).
- **Symbol table T4:** 2.66 vs 0.044 nat, selective in 36/36.
- **Symbol table T2:** V-only moves 1.03 nat with an attention shift of 0.0018. K-only moves 0.087 nat and is inert (`2026-10-02-qwen-address-symbol-table/FINDINGS.md`).
- **Pointer/value split, replicated:**
  - base: alias-seed clean rate 0.0;
  - instruct: alias-clean 0.0 with donor 0.96, K-only clean 0.0, V-only 0.89 (n=28).

  Sources: `residual-program/FINDINGS_rp1.md`; `residual-program-v2/FINDINGS_qwen15it.md`.
- **Bag-of-facts:** jointly formed pages match the native top-1 in 6/6, against 1/6 for independently formed pages (Paper 2 §9.2; `2026-09-25-book-index-two-source-coherence/FINDINGS.md`).

**Rules out:**
- query-independent steering vectors;
- bag-of-facts memory (Mount = Prefill);
- "the alias residual holds the value".

**Strength: adequate on replication, weak on novelty.**
- Query selectivity is what any attention-based retrieval predicts. The validity audit already labels it "VALID-but-expected".
- Pointer/address/payload separation for bindings has direct prior art: Feng & Steinhardt 2023 (binding IDs) and Prakash et al. 2025 (the "lookback" mechanism, which uses address/pointer/payload language) (PRIOR).

**Biggest hole.** K-as-address is never directly exercised in AR. T2a is inert on decided reads, and the clean pre-RoPE joint swap was never run. The SDXL K×V superadditivity (+0.341) is one factorial on one contrast, and the SDXL joint permutation (0.859) is still awaiting its fp64 check.

**Cheapest closer.** A pre-RoPE K re-rotation joint swap on *undecided* reads in Qwen, where α on the target is roughly 0.3–0.7. It is one run. Without it, say "V is payload" and drop "K is address" for AR.

### P4. Non-additive effects pass through routing (conditional linearity), with attention and MLP gating coupled

**Claim.**
- With attention probabilities, gates and norm scales frozen, the model-internal path is affine, so raw-logit interactions vanish.
- Freezing either attention alone or the gates alone removes most of a measured two-edit interaction.

**Evidence (MEASURED).**
- **Raw all-frozen interactions:** −9.54e−6, −7.63e−6 and 2.48e−5, against live values of 0.89–1.94. Dose R² > 0.99999999996 (`routing-readout-correction/FINDINGS.md`).
- **Instruct (14 cells):** attention-only removes a median 0.958, gate-only 0.99, each at ≥80% in 13/14 cells. The payload main effect keeps 0.42 of its size under the full freeze (`residual-program-v2/FINDINGS_qwen15it.md`).

**Rules out:** "fixed nonlinear conjunction units on payloads" (FixC), at the raw boundary.

**Strength.** As a theorem, strong, but true by construction. As an empirical finding, weak to adequate:
- it is one alias organism family;
- the partial freezes are coupled, and the successor itself says they are "not additive percentages";
- prior art: this linearisation is how attribution graphs are built, and the missing QK routing is the known gap (PRIOR: Ameisen et al. 2025; Kamath et al. 2025).

**Biggest hole.** It does not say *where* the relation is routed.

**Cheapest closer.** Nested routing freezes by layer band (L0–11, L12–21, L22–27) on the RP2 cells. That is 1 run, about 10 minutes. It converts the tautology into a depth map of where the interaction is routed, which is the empirical content the theory actually needs.

### P5. The read band is conserved under heavy fine-tuning, with asymmetric codes

**Claim.**
- Instruct tuning is a ~1% uniform nudge.
- Domain continued pretraining rewrites most weights without sparing the band.
- Yet the read location is conserved, and the band is where the variants converge most.
- Domain models can read the base model's band code, but write one the base cannot read.

**Evidence (MEASURED, `2026-10-02-qwen-variant-circuits/FINDINGS.md`).**
- **Weight change:** instruct relative ‖ΔW‖ 0.012 with cos ≈ 1.0. Coder relative 0.862, cos 0.47–0.72. Math relative 1.507, cos 0.20–0.42. The change is depth-flat.
- **Locator:** bimodal in all six variants, and 5/6 peak at L27.
- **CKA vs base (math):** 0.718 in the band against 0.409 at L18.

**Transplant results** (rescue; COMP = rescue divided by the recipient's own self-transplant):

| Pair | Rescue | Recipient self | COMP ratio |
|---|---|---|---|
| base→coder | 0.92 | coder→coder 0.76 | ≈1.2 |
| coder→base | 0.34 | base→base 0.63 | ≈0.54 |
| base→math | 0.43 | math→math 0.86 | ≈0.50 |
| math→base | 0.05 | base→base 0.63 | ≈0.08 |

The asymmetry survives normalisation. Specificity (wrong→correct) is about 0.00 everywhere.

**Rules out:** "domain fine-tuning relocates the read" and "a different code means a different scaffold".

**Strength: adequate, and the most novel item in the program** (INFERRED). Prakash et al. 2024 showed that entity-tracking circuits are preserved and enhanced under fine-tuning, and base↔chat transfer of SAEs and crosscoders is known (PRIOR). A *directional* readability asymmetry, measured by causal K/V transplant after continued pretraining that leaves cosine at 0.2, is a crisp new observation.

**Holes.**
- **Late-layer CKA convergence may be generic,** because models that predict similar next tokens converge near the output, and the band L22–27 includes the final layer. No control separates "scaffold conserved" from "output convergence".
- One task; n = 38 rows; the instruct wrong-donor index was miscomputed (disclosed); the dynamic-circuit half is still pending.
- Same initialisation in every case, so conservation may be basin inertia.

**Cheapest closer.**
1. Run the pending dynamic half.
2. Add the E20 block/rescue at each variant's own band (frozen, not run).
3. Add a CKA control computed against an unrelated model, e.g. SmolLM2-1.7B. CKA works across widths, so this tests whether the in-band convergence exceeds what generic output convergence gives.
4. Add one more lineage pair that changes behaviour sharply: DeepSeek-R1-Distill-Qwen-1.5B against its Qwen2.5-Math-1.5B parent.

That is about 5–6 runs, about 1 hour.

### P6 (demote). Carried state locks progressively along the execution axis

**Claim.** Later sources can only change what the carried state has not yet locked.

**Evidence (MEASURED).**
- **SDXL lock-in:** relations and background lock by k0 = 2 of 24. At k0 = 8 they reach 0.06–0.08. Early:late install authority is 16.56–16.88 (`sdxl-relation-lockin/FINDINGS.md`; `sdxl-address-symbol-table/FINDINGS.md`).
- **SDXL SP4:** register gain 0.929 (n = 2 relation cases).
- **FLUX closure:** program-only 0.712, register-only 0.403, both together exact.
- **Mamba:** staged 3/3 against 0 for endpoint sums. The commit lever is the write, not retention: release hurts 0/6 and dt acts via the write 6/6 (`mamba-clock-retest/FINDINGS.md`).
- **AR, multi-turn baseline:** it moves +2.54 nats, with answer content contributing +2.25 and format priming decaying to −1.18 by pass 3 (`pass-indexed-baseline/FINDINGS.md`).

**Strength: weak as discriminating evidence.**
- Diffusion coarse-to-fine is the textbook expectation; the math document derives it from posterior-mean denoising.
- Under the frozen readout the lock-in L1/L2 predictions failed, and the v2 readout is pilot-informed.
- The AR depth-deadline version (hop-depth) failed to replicate (§0.1).
- The pass-indexed baseline is correct methodology. Scoring against a fixed parent is the wrong counterfactual, the standard patching-baseline warning (PRIOR: Zhang & Nanda 2023). It is not a scaffold discovery.

**Biggest hole.** In AR there is no positive, replicated "time" result beyond P1's formed-before-read.

**Cheapest closer.** Wait for the Gemma arm of RP-v2. If it also fails to show a hop-depth ordering, retire the claim. If it shows one, it is a base-vs-instruct difference worth a paragraph, not a law.

---

## 3. What is genuinely new against prior work

| Prior line | What it already established (PRIOR) | What this program adds (MEASURED unless noted) | Delta |
|---|---|---|---|
| Causal abstraction / IIA (Geiger et al. 2021, 2023; DAS, Wu et al. 2023) | Formal scaffold-as-abstraction; learned alignments; IIA as the metric | The definition is used as is. New: one fixed band reaching its re-fit ceiling across two operations and two families | Small: the ceiling is narrow (P2 hole 1) |
| Path patching / mediation (Wang et al. 2022; Goldowsky-Dill et al. 2023; Meng et al. 2022 causal tracing) | Edge-level mediation and localisation of factual recall | Block **and** independent unseeded-recipient rescue, plus wrong-content authorship, plus isolated vs in-forward cuts (0.985 vs 0.009) | Moderate: a cleaner causal design, and the isolated-cut point is a useful methods contribution |
| Geva et al. 2023, "Dissecting recall" | Subject enrichment at the subject position; upper-layer attention from the last position extracts the attribute | Content is present at band entry, the band's own computation is not needed (0.904 / 1.023), the band's K/V commits it, and the read is at the subject position only (0.010) | Moderate: a causal refinement of the extraction stage. The fit-free locator is Geva's attention-knockout locus made predictive |
| Lad et al. 2024, stages of inference | Universal stages at relative depths across families | A frozen relative-depth rule fails blind (Pythia); a model-read locator succeeds (Phi-2) | Small–moderate: a falsified depth law plus a working alternative |
| Function vectors (Todd et al. 2024; Hendel et al. 2023) | Operations as compact vectors | Per-item reader cosine within vs across operations (0.73–0.99 vs 0.20); the FV-reproduction negative is weak (unit coefficient, all heads) | Small |
| Binding IDs / lookback (Feng & Steinhardt 2023; Prakash et al. 2025) | Bindings via binding-ID vectors; address/pointer/payload lookback | Alias carries pointer, not value; K-only never transfers; replicated at n = 28 on instruct | Small: confirms prior mechanisms with causal K/V/residual cuts |
| ROME/MEMIT limits (Meng et al. 2022, 2023; Hase et al. 2023; MQuAKE, Zhong et al. 2023; RippleEdits, Cohen et al. 2024) | Localisation ≠ editability; edits fail to propagate to multi-hop | The inference "edit values at the store, bindings before the hop depth" now lacks AR support (§0.1) | None at present |
| Merullo et al. 2024, component reuse | Small sets of components reused across tasks | One L22–27 interface hosts color 16/16, position 12/16, identity 11/11 | Small |
| Chain-of-thought / depth limits (Biran et al. 2024, "Hopping too late"; Merrill & Sabharwal 2023) | Multi-hop fails when the bridge resolves too late; CoT adds serial depth | The hop-depth law was the candidate here; it failed to replicate | None; even if it had held, Biran et al. is the obvious predecessor |
| Attribution graphs (Ameisen et al. 2025; Lindsey et al. 2025; Kamath et al. 2025) | Linearise by freezing attention and norms; QK routing is the acknowledged gap | Quantifies the gap on one store: 0.31 (features+errors) vs 0.94 (native cut); the graph puts the most subject influence at layer 0 (11/12 identity items) | Moderate and timely, but it needs an attention-inclusive comparator to be fair |
| Model diffing / fine-tuning effects (Prakash et al. 2024; Jain et al. 2023; Kissane et al. 2024; Lindsey et al. 2024 crosscoders) | Mechanisms are preserved or enhanced under fine-tuning; features transfer base↔chat | Read location conserved despite cos 0.2–0.4 weights; **directional readability asymmetry** under K/V transplant | **The most novel item** |
| Diffusion editing (Hertz et al. 2022; Meng et al. 2021 SDEdit; Balaji et al. 2022 eDiff-I) | Timestep-dependent edits; early steps set layout | Closure partition (program vs register); relations lock by step 2 of 24 | Small |

**The three findings most likely to make people pay attention, in order.**

1. **"Find the store with one forward pass, then prove it causally."** Combine the blind locator, the E20 block-and-rescue in six families plus 7B, and IIA at its ceiling.
   - It is a practical tool, falsifiable, and already passed one discriminating blind test (Phi-2: locator block 0.515 against 0.065 for the depth band).
   - It becomes a circulating result if it holds for parametric recall and on 8–10 blind models.
2. **Fine-tuned models read the base model's store but write one the base cannot read,** while the read location stays put through near-total reweighting.
   - It is surprising, simple to state, and matters to anyone transferring probes, SAEs or edits across a model lineage.
   - It needs normalisation (done above as COMP), a generic-convergence control, and one more lineage.
3. **Attribution graphs miss the attention-formed store** (0.31 vs 0.94).
   - It is timely, but expect pushback: the result is "by construction" for MLP-only transcoders.
   - It lands only paired with the locator, i.e. "here is where to look instead".

**Not attention-getters on the current evidence.**
- *Stale-pointer / hop-depth deadlines:* they failed to replicate, and Biran et al. 2024 is prior.
- *Routing makes relations:* the full freeze is a theorem and is the attribution-graph premise.
- *Per-pass re-baselining flips conclusions:* this is baseline hygiene. Keep it as a methods box.
- *The scene compiler / model-as-software:* the paper itself calls exact parity "architectural custody", and caching prompt-static cross-attention K/V is a known optimisation. It is valuable tooling, and it is the reason the experiments are trustworthy, but it is not a science headline.

---

## 4. Weaknesses a hostile reviewer will hit

| # | Weakness | Severity | Fix |
|---|---|---|---|
| 1 | **The umbrella thesis is unfalsifiable** ("every stateful model fits"). No competent network has been shown *without* a scaffold. | **Fatal if the theory is the headline**; fine if the paper leads with falsifiable claims | Reframe around the named falsifiers (IIA ceiling, blind locator, block/rescue, transplant asymmetry). State what would refute each. Move the theory to the discussion |
| 2 | **One templated in-context copy task carries the AR spine** (§0.2). Identity and color are both read back from context. | **High**, cheap to fix | To-do 1: parametric recall, plus one relational task with competent rows |
| 3 | **Claims that fail on the first replication are still in the living theory and blog** (hop-depth, stale-pointer). | High (credibility) | Retract or scope both today. This costs nothing |
| 4 | **Prior-art overlap with Geva's extraction stage** is not stated head-on; the locator is Geva's locus made fit-free. | Medium–high | Say it in the introduction. Claim the delta: causal independence, blind prediction, conservation under fine-tuning |
| 5 | **The IIA ceiling is narrow** (six overlapping bands), and absolute IIA is moderate (0.31–0.76). | Medium | To-do 4 widens the ceiling. Report absolute IIA prominently |
| 6 | **Small n.** Blind locator n = 2. Transplant n = 38. Pass-indexed n = 4 scenes. RP2 base 3 cells. SDXL relation n = 2–4. Hop ladder one organism per hop. | Medium; mostly cheap | Expand where a claim is headlined; demote elsewhere |
| 7 | **Single seed.** | Low for LMs: the models are deterministic and the replication unit is the context or identity. Medium for SDXL | State it as a limit. Increase identities, not seeds |
| 8 | **Base models only** for most claims. | Medium; partly fixed by the variants and v2-instruct, which is exactly where two claims broke | Run headline claims on at least one instruct model |
| 9 | **≤7B.** The 7B E20 is weaker (block 0.595); the 7B locator is deferred (meta-device bug); the 30B MoE result is negative. | Acceptable as a stated limit at a venue; a lab will ask for 7–9B on the locator | Fix the paging bug, then run the locator plus E20 at 7B (to-do 8) |
| 10 | **Post-hoc or pilot-informed readouts:** the SDXL SP1 rescore and v2 readout; locator rule C chosen among three on Phase A; the formation-over-time refinement after P2a failed. | Medium; already disclosed | Keep the disclosures. Do not headline these items |
| 11 | **The cross-family common graph is a null,** so "diffusion + AR + SSM" is shared vocabulary, not a shared mechanism. | Medium for the current framing; none for a transformer-scoped paper | Scope to transformers. Put diffusion and Mamba in a short "the vocabulary transfers" section or a separate paper |
| 12 | **Competence gating shrinks scope** (OLMo-1B 0/108; position 0 admitted; size 4). | Low–medium | Report denominators. The gating is principled |
| 13 | **Vocabulary inflation** (scaffold, lowering, dynamic circuit, StateCut, register, program, plane). | Medium for reception | Use about five terms and define them once |
| 14 | **One toolchain, with a past silent causal-mask defect.** | Low–medium | Release code. Rerun the headline E20 cell with TransformerLens or nnsight as an independent harness (one run) |
| 15 | **Late-layer CKA convergence may be generic** (P5). | Medium for the variants claim | The control in to-do 3 |

---

## 5. The paper to write

**Recommendation.** Write a **new consolidated, transformer-only paper**. It absorbs Paper 1's E20 and transcoder results plus Paper 2's IIA, locator and variants. The pointer/value result goes in as a short section.

The alternatives:
- **Revising Paper 2** inherits its seven-properties × three-families frame, which the evidence does not carry.
- **A short headline paper plus a long one** is also viable: a 4-page "blind locator + block/rescue + fine-tune asymmetry" and a long technical report holding the theory, diffusion, Mamba and the VM.

If Paper 1 has already gone out, keep it as the formation/commit paper. Make this the "fixed, findable, conserved" paper and cite Paper 1 for the E20 design. Either way, retire the current Paper 2 framing.

**Title.** *A Fixed, Findable Read Band: Transformers Commit In-Context Facts to Late Subject Keys and Values, Predictably and Across Fine-Tuning*

Shorter alternative: *One Forward Pass Finds the Store.*

**Abstract (≈150 words; numbers MEASURED; bracketed text depends on to-dos).**

> Where does a transformer keep the fact it is about to say? For entity-attribute readout we find the controlling content is formed in the subject's residual stream before a late band of layers, committed into that band's subject-position keys and values, and read there by the answer position's attention. Blocking the formed band removes 0.52–0.97 of an early seed's effect, and transplanting it into an unseeded recipient restores 0.71–0.99 (1.46 in Pythia), across six decoder families and at 7B; a wrong-identity band authors the wrong answer. One fixed band reaches the interchange accuracy of per-example re-fitting (0.87 and 1.00 of ceiling). A fit-free statistic from one clean forward pass predicts the band blind in [two → N] unseen families where a relative-depth rule fails. The band survives continued pretraining that rewrites most weights, and fine-tuned models read the base model's band code while writing one the base cannot read. A matched MLP-transcoder interchange moves the identity answer only 0.31 of the way, against 0.94 for a native cut. [The same holds for parametric recall.]

**Section skeleton.**
1. **Introduction.** The localisation disagreement between patching and attribution. The claim: a fixed, findable read band. The delta from Geva and Lad stated up front.
2. **Setup.** The isolated K/V cut (in-forward 0.985 vs isolated 0.009); the nine-arm block/rescue panel; admission rules; the five-role vocabulary (source, formation, commit, read, consumer) defined once.
3. **Formation, commit and read separate** (P1). E20 across families and at 7B. The band-internal test, with the falsified P2a disclosed as the refinement. The read at the subject position.
4. **The band is fixed** (P2a). IIA with the widened ceiling; absolute IIA reported plainly.
5. **The band is findable** (P2b). The locator: Phase A, then blind Phase B on N models. The depth-rule failure.
6. **The band survives fine-tuning** (P5). Weight deltas; locator; CKA with its generic-convergence control; transplant asymmetry, normalised; [dynamic half].
7. **What the band holds and how it is addressed** (P3, short). Query selectivity; V as payload; pointer vs value (base plus instruct).
8. **Attribution graphs miss it.** The transcoder interchange, with the matched-operator and coverage caveats.
9. **Limits and what did not hold.** The hop-depth law and stale-pointer did not replicate on instruct. The cross-family graph is null. MoE-30B is negative. Competence gating.
10. **Discussion.** The scaffold/program view as an interpretation; conditional linearity (P4) as the reason interactions are routing; implications for editing and probing.
- **Appendix:** pass-indexed baselines (methods box); diffusion and Mamba analogues; reproducibility and custody.

**Figure list (existing files first).**
1. A new schematic with source, formation, commit, read and consumer on depth × position. Adapt `research/papers/time-formed-circuits/figures/fig1-schematic.png`.
2. Block/rescue across six families plus 7B: extend `time-formed-circuits/figures/fig2-dissociation.png` or `saturn/experiments/2026-10-02-e20-cross-family/results/e20_dissociation_bars.png` with the Pythia, Phi-2, OLMo-2 and 7B cells.
3. Band-internal results: `saturn/experiments/2026-10-02-formation-over-time/figures/fig_fot_test2.png` (band freeze) and `fig_fot_test3.png` (read position).
4. IIA fixed vs ceiling vs floors: `saturn/experiments/2026-10-02-fixed-lowering-iia/analysis/iia_summary.png`.
5. The locator R_ℓ with true, locator and depth bands: `research/papers/time-circuit-scaffold/figures/locator_R_curves.png`, plus `saturn/experiments/2026-10-02-blind-scaffold-prediction/figures/pythia_localization.png`.
6. Fine-tune panel (2×2):
   - `saturn/experiments/2026-10-02-qwen-variant-circuits/figures/fig_weight_delta_heatmap.png`
   - `fig_locator_overlay.png`
   - `fig_cka_perlayer.png`
   - `fig_transplant_matrix.png` — redraw it normalised by recipient self-transplant
7. Query selectivity: `research/papers/time-circuit-scaffold/figures/fig3_same_patch_query.png` or `saturn/experiments/2026-10-02-qwen-address-symbol-table/figures/fig5_T4_selectivity.png`.
8. Pointer vs value: `saturn/experiments/2026-10-02-residual-program/figures/rp1_install_categories.png`, with the instruct replication. Also `saturn/experiments/2026-10-02-residual-program-v2/figures/rp1_anchor_seed_depth_qwen15it.png`, which shows the non-decreasing `l*` honestly.
9. Attribution coverage: `research/papers/time-formed-circuits/figures/fig4-error-interchange.png`.

**What to cut from the main paper.**
- The seven-property × three-family frame and the coverage matrix.
- The scene compiler: the 21/21 parity, the FLUX proof sheets, the cache speed-up. Move them to a tooling paper.
- The FLUX four-quadrant certificate.
- The XNOR inversion. It is sourced to an Obsidian survey, not a primary.
- The archive/page VM.
- The Mamba lane, except one sentence.
- Diffusion timing and lock-in.
- The cross-family common-graph null: reduce it to one sentence.
- Section 13 and Appendix D (location-index proxies, variance ratios, sliding window, FV).
- The hop-depth law and stale-pointer as positive claims.
- "Routing makes relations" as a finding. Keep it as a one-paragraph theorem with attribution-graph lineage.
- Pass-indexed baseline: appendix only.

---

## 6. Ranked to-do list (cheapest moves that raise the score most)

Costs assume about 10 minutes per mrun run at ≤2B.

| Rank | Item | Cost | Why it moves the score |
|---|---|---|---|
| 1 | **Parametric-recall E20 + locator + IIA** (Known-1000/CounterFact-style prompts, filler-subject substitution), Qwen2.5-1.5B and Gemma-2-2B, prereg-frozen | ~4–6 runs, ~1 h incl. panel build | Closes the largest scope hole (§0.2). Either outcome sharpens the paper |
| 2 | **Blind locator on 4–6 more models**: Qwen2.5-0.5B/3B, Llama-3.2-1B (pipe-download as for Phi-2), Gemma-2-2B-it, SmolLM2-360M, Pythia-410M/2.8B. Freeze before each run; also score a narrow (±1 layer) band against the true single-layer commit | ~12 runs, ~2 h | Takes "predictive" from n = 2 to n ≈ 8. This is attention-getter #1 |
| 3 | **Finish and harden the variants**: the pending dynamic half; E20 at each variant's own band; transplant normalised by recipient self; a CKA control against an unrelated model; one extra lineage (R1-Distill-Qwen-1.5B vs Qwen2.5-Math-1.5B) | ~6 runs, ~1 h | Turns attention-getter #2 from interesting into defensible |
| 4 | **Widen the IIA ceiling** (every single layer, every contiguous band of width 2–8, per-KV-head subsets) and add a competent relational operation (a two-object relation panel with natively competent rows) | ~3 runs, ~30 min | Answers "fixed vs per-input" against a real rival |
| 5 | **Writing, now:** retract the hop-depth law and stale-pointer→competitor in the living theory and Paper 2 (cite v2-instruct); add the Geva/Lad/Prakash/Biran/attribution-graph lineage; reframe the thesis as named falsifiers | 0 runs, ~2–3 h | Removes the two easiest attacks on credibility |
| 6 | **Attention-inclusive comparator** for the attribution claim: e.g. circuit-tracer with QK attribution enabled or attention-output SAEs, or a matched-magnitude native cut restricted to the MLP path | ~1–2 h build + 2 runs | Makes attention-getter #3 fair. If the build is too costly, soften the claim to "MLP-transcoder" |
| 7 | **Nested layer-band routing freezes** on the RP2/RP-v2 cells | 1–2 runs, ~20 min | Turns P4 from a tautology into a depth map of where relations are routed |
| 8 | **7B locator** (fix the meta-device/hook incompatibility in paging), then locator + E20 at Qwen2.5-7B | engineering + 2 runs | The lab audience will ask for it |
| 9 | **Independent-harness replication** of one headline E20 cell in TransformerLens or nnsight | 1 run + ~1 h port | Neutralises the single-toolchain objection |
| 10 | **Pre-RoPE joint K/V swap on undecided reads** (Qwen); SDXL joint permutation in fp64 only if diffusion stays | 1–2 runs | Earns or retires "K is address" |

The top five cost about 5 hours of runs plus a writing pass. Of these, items 1–3 move the score the most.

---

## 7. Appendix: a "full understanding" picture

This is my best integrated account under the theory. Each statement carries its status.

**Transformer, single forward pass (entity-attribute readout).**
1. **[Solid]** The subject token's identity enters the subject position at layer 0 through the token's own attention write. For a lexical value this write alone fully rescues (1.00, RP3).
2. **[Solid]** Context-computed attributes accumulate in the subject residual stream over pre-band depth. The content is fully present by band entry: a cumulative seed rescues about 1.0 from L0 to L20, and freezing the band changes nothing.
3. **[Partly solid]** Pre-band MLPs refine the subject representation early (L0–3) and again just before the band (L19–21: 0.32 and 0.21 single-write rescue, RP3, n = 6).
4. **[Solid]** In a late band (Qwen L22–27, Gemma L16–23, Pythia ~L16, Phi-2 ~L23, OLMo-2 L13), each layer's K/V projections make the subject content available. Most of the commit can sit in one layer: Qwen L23 0.732, OLMo-2 L13 0.894.
5. **[Solid]** The answer position's query attends to the subject position in that band and reads V. The read is query-selective, and an MLP-only feature basis cannot see it.
6. **[Partly solid]** The query's "which entity" comes from earlier reads into the answer and alias positions: pointers. Values are fetched from the anchor's slot at read time. Relation content at the consumer position stays redirectable through about L16 and locks by about L20 (RP4, base, model-limited).
7. **[Theorem]** Interactions between edits arise only through routing (attention, gates, norms). Attention-only and gate-only freezes are coupled, and each removes most of it.

**Across checkpoints.**
- **[Solid, one lineage]** The read band's location survives domain continued pretraining.
- **[Solid, one lineage]** The *readable* code is conserved in the base→derivative direction, while the *written* code drifts.
- **[Speculative]** This is basin inertia from a shared initialisation, not a universal attractor.

**Across passes.**
- **[Solid, n = 4]** Later turns read the model's own answers. The answer-content increment is +2.25 nats and is persistent; format priming decays.

**Across architectures.**
- **[Vocabulary-level]** Diffusion: the prompt K/V are static and the latent supplies the queries; early steps lock layout and relations, late steps fine detail.
- **[Vocabulary-level]** Mamba: the commit is a write at a late layer, and retention is a correlate.
- **[Measured null]** A shared cross-family role graph.

**The deepest open questions.**
1. **The address algorithm.** How does the answer position compute which subject row to read for *semantic* queries? A predecessor-based query address works on surface repetition (1.00) and fails on semantic panels (0.00) (Paper 1 §4). This is the real "dynamic circuit" question, and it is unopened.
2. **Is there one read band or many?** Does parametric recall, arithmetic, code or a multi-hop bridge use the same late band, and why is the locator bimodal (L21–23 and L27) in every Qwen variant?
3. **Where does non-lexical content form?** Pending (`2026-10-02-nonlexical-store`, results present but no FINDINGS yet; not interpreted here).
4. **Base vs instruct indirection.** Why does the base model's pointer failure go to the competitor while the instruct model's goes to the donor? Is the "deadline" a property of weak indirection rather than of depth? The Gemma v2 arm is pending.
5. **Acquisition and scale.** When during pretraining does the band appear (no authenticated checkpoint trajectory yet)? Does it survive above 7B and in MoE, where the one 30B test was negative?
