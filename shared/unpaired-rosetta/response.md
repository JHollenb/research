---
title: "Reading Is Not Authoring: A Scaffold Axis, Two Ceilings and a Fidelity Gap in Unpaired Cross-Modal Alignment"
subtitle: "A response to Schnaus, Dagès, Cremers, Wang and Isola, 'Shared Geometry as a Rosetta Stone' (arXiv 2610.09411)"
status: "DRAFT 1.2 (2026-10-09). Gate detector measured over 3 seeds. E0, E3, part of E1 and part of E5 measured; claims rescored on effect size (no arbitrary bars); E1 measured except E1b; E2, E5 rest running; E4 design only."
date: 2026-10-09
authors: TBD
code: experiments/ (their library pinned at fdfad84; receipts in experiments/results/)
---

# Reading Is Not Authoring: A Scaffold Axis, Two Ceilings and a Fidelity Gap in Unpaired Cross-Modal Alignment

> **Status (draft 1).**
> - **How results are labelled.** Measured results carry a receipt path. Predictions were frozen before their
>   runs; we report each verdict as frozen, including the ones that failed. Results found after a frozen test
>   are labelled *post-hoc*.
> - **How claims are judged.** A frozen bar decides only its own prediction. A claim is judged on the direction
>   and size of the measured effect against its noise: slice-to-slice agreement (E3), seed spread (E5),
>   draw spread (E2). The only thresholds allowed to decide a claim are a proved inequality, a noise floor, or a
>   consumer zone measured on FLUX (labelled as FLUX's). Where a bar we set ourselves disagrees with the
>   effect, both are shown.
> - **Placeholders.** E0, E1 (with the D1 check), E2, E3 and E5 (with the gate detector) are measured. One
>   **[PENDING]** remains: E4, the FLUX consumer benchmark, which is designed but not built.

## Abstract

Schnaus et al. show that separately trained vision and language encoders share enough geometry to be aligned by
a single rotation with no paired data. We confirm this on a new kind of pair: zero-pair QAP recovers an
18-symbol correspondence between SmolLM2 and the text conditioner of a diffusion model, exactly, with their own
solver (§2).

We then tested four ideas about what their evaluation cannot see. One failed, and one holds only weakly:
- **A caption-independent `<think>` preamble does not dilute CKA (refuted).** The preamble is real: 96–100% of
  captions share each of their first 16 generated tokens. But removing it at the token level lowers CKA at
  Qwen3-1.7B with thinking on, in every cell (−0.010 to −0.021; §3).
- **A late non-final layer aligns slightly better (supported, small).** Depth 0.89 beats the final layer by
  0.007–0.015 in 5 of 6 no-thinking cells, including their own mean pooling on both corpora. It does not hold for
  their thinking-mode generative pooling. The effect on FOSCTTM is untested (§4).

The audit of the first failure led to a measured finding in their own stored Qwen3-8B generative embeddings for
long captions:
- one principal axis holds 13.8% of the variance;
- the image embedding barely predicts it (held-out R² 0.16, vs 0.88–0.89 for the top axis of MPNet and
  Qwen3-Embedding);
- projecting it out raises linear CKA from 0.433 to 0.583, while the same operation lowers CKA for the two
  other encoders. This is the behavior our Lemma A1 predicts for a scaffold.

The clipped CKA used in their appendix hides this (0.61–0.66 for all three). Under their aligner, this embedding
aligns near chance on SPC (FOSCTTM 0.407 in our holdout run), which matches their report. Projecting the one
axis out of the language side before fitting brings FOSCTTM to **0.036** on the same holdout (single seed;
seed-spread runs queued). Our first unpaired detector for the axis failed (FOSCTTM 0.484), because it trusted
pseudo-pairs from the broken fit. The same projection wrecks MPNet and Qwen3-Embedding (0.043 → 0.361, 0.022 → 0.402), whose top axis is the
image's own, so it is not a blanket rule. A gate detector that uses no pairs (§3.5) gets this right in all three
encoders: it gates off gen's axis and leaves the other two alone, choosing the best-FOSCTTM setting in 9 of 9
model × seed cases. Across three seeds the fix is 0.415 ± 0.055 → 0.038 ± 0.006.

The other two claims are proved. Span-confined pair baselines have a fidelity ceiling of
sqrt(top-p eigen-energy). It holds on their data but is loose, and their method needs no pairs to beat these baselines (§5). Retrieval and generation fidelity separate in high dimension
(§6). Measured on COCO: their unpaired map retrieves almost perfectly (FOSCTTM 0.0073), yet its median per-pair
cosine to the true partner is 0.527, so about 72% of each mapped vector's energy is off its partner. No
validation pair reaches the band where our diffusion consumer rendered 8/8, and 43% fall in the band where it
failed. The gap is not an estimation failure. Their zero-pair map sits only 0.07 (0.04–0.10 over three seeds) below a rotation fitted on 20,000
true pairs, and that best rotation still reaches no pair in the 8/8 band. Dropping orthogonality (least squares
on the same pairs) adds 0.21 median fidelity at identical FOSCTTM, so retrieval cannot see the difference.

---

## 1. Outline: what we claimed, what happened

| # | claim | basis | test | verdict so far |
|---|---|---|---|---|
| — | Their premise holds on a new pair type (LM ↔ diffusion conditioner, symbol level) | measurement | E0 | **confirmed**: 18/18 at zero pairs |
| A | The thinking-mode preamble dilutes CKA; token-centering removes it | Lemma A1 + code reading | E3 (2 runs) | **refuted**: preamble present, but centering it lowers CKA in every thinking-on cell (−0.010 to −0.021) |
| A\* | *(post-hoc)* A single non-visual axis dominates Qwen3-gen embeddings, and clipped CKA hides it | Lemma A1 behavior, measured offline on their stored embeddings | axis probe + E5 | **measured**: dropping it 0.415 ± 0.055 → 0.038 ± 0.006 (3 seeds); the same drop wrecks MPNet/Qwen3-Embedding; the pseudo-pair detector failed, but the gate detector (§3.5) selects correctly for all three with no pairs |
| B | The final layer is past the commit layer; a late layer aligns better | our LM commit-band results | E3 depth sweep | **supported, small**: depth 0.89 > 1.0 by 0.007–0.015 in 5/6 no-thinking cells; not for thinking-mode gen |
| C | Span-confined pair baselines: mean fidelity ≤ sqrt(top-p eigen-energy) | proof | E2 | **proved and measured**: the bound holds in all rows but is loose; their method beats it at p = 5, not at p = 20 |
| D | FOSCTTM ≈ 0 is compatible with low per-pair fidelity α | proof (Prop. D1) | E1 | **supported**: ours-p0 FOSCTTM 0.0073 with median α 0.527; two oracles with equal FOSCTTM (0.0027/0.0026) differ by 0.21 in median α; D1's formula is qualitatively right, quantitatively off 3–30× at low FOSCTTM |
| E | Choosing pairs (vision-side medoids) raises the ceiling | Ky Fan + shared geometry | E2 | **baselines only**: more energy and lower linear FOSCTTM at every p ≤ 200; no gain for their method |
| F | A consumer-grounded benchmark | infrastructure | E4 | design only |

We checked these and do not claim them:
- Their pipeline centers and unit-normalizes both spaces before every step.
- Their QAP solver (MPOpt) reaches the optimum on our problem.
- Their runs are bit-reproducible.

Two suggestions we first considered, "center the embeddings" and "use a better QAP solver", are wrong for their
code and were dropped before any run.

---

## 2. Their premise on our data (measured, E0)

**Setting.**
- **Spaces.** Subject-row displacements (a subject row minus the template mean) of 18 animals × 4 distinct
  prompt prefixes, in SmolLM2-1.7B and in the Qwen3-4B text conditioner of FLUX.2 Klein 4B (7,680 dims). Source:
  our receipt `job-0706b0497903`.
- **Templates.** Six templates collapse to four, because causal models give bit-identical subject rows for
  templates that share the text before the subject.
- **Problem.** Centered-cosine kernels of the class means; maximize `Tr(K_A P K_B Pᵀ)` with zero pairs. This is
  their CKA-matching objective.

Receipt: `experiments/results/e0_symbol_qap/e0_symbol_qap-20261009T180533.json` (2,000 restarts).

| quantity | value |
|---|---|
| off-diagonal kernel correlation across spaces | 0.890 |
| zero-pair correspondence, 2-opt with 2,000 restarts | **18/18**; 169/2,000 restarts find the truth, and it is the best objective found (23.5915) |
| zero-pair correspondence, MPOpt (their solver and costs) | **18/18** |
| each prefix alone (4 independent problems) | 18/18 on every prefix |
| Gaussian-geometry null (10 draws) | 0–2/18 |
| margin to the next local optimum / best single swap | 0.236 / 0.053 |
| seeded with k = 1, 2, 3, 5 anchors (accuracy on the rest, scipy FAQ) | 0.22, 0.29, 0.52, 0.72 (chance 0.06–0.08) |
| fully unpaired rows (animal and prefix unknown) | 41.7% (chance 5.6%); source rows cluster by prefix (ARI 0.019), native by animal (0.331) |

**What it adds.**
- **A new pair type.** Their finding extends to a language model against a diffusion-model conditioner, at the
  granularity of individual symbols.
- **Causal check.** The recovered correspondence is the one our anchored bridge uses. That bridge authors
  held-out symbols through the image generator at native parity (0.523–0.810 vs 0.520–0.817). So the geometric
  correspondence is checked causally, not only by retrieval.
- **Caveats.** The margin is thin, and 18 symbols is small.

---

## 3. Claim A: does the thinking-mode preamble dilute CKA? (measured: no, as framed)

### 3.1 Setup and the lemma we tested

Their generative pooling (`modalities/image_captions/generative.py`) works as follows:
1. Wrap the caption as "Imagine what it would look like to see: {caption}" in Qwen3's chat template, with
   `enable_thinking=True`.
2. Decode greedily for at most 128 tokens.
3. Embed as the mean of the final-layer states that produce those tokens.

**Lemma A1 (scaffold dilution of CKA, exact in population).** Let X = R + S be zero-mean, with S independent of
(R, Y). Then

```
CKA(X, Y) = CKA(R, Y) · ||Σ_R||_F / ||Σ_R + Σ_S||_F  ≤  CKA(R, Y) / sqrt(1 + ρ²),   ρ = ||Σ_S||_F / ||Σ_R||_F.
```

Equality holds if and only if Σ_R Σ_S = 0.

*Proof.* Independence gives Cov(X, Y) = Cov(R, Y) and Cov(X) = Σ_R + Σ_S. Expanding,
||Σ_R + Σ_S||_F² = ||Σ_R||² + ||Σ_S||² + 2 tr(Σ_R Σ_S), and tr(Σ_R Σ_S) ≥ 0 for positive semidefinite
matrices. ∎

Two consequences:
- **Prediction for a pure scaffold.** Removing it raises CKA. Removing a direction that carries content shared
  with Y lowers it. This sign test is what §3.4 uses.
- **Effect on alignment.** In their refinement the scaffold adds variance to every Hungarian score and no margin,
  so the probability that a distractor outranks the true partner rises (Corollary A2).

### 3.2 What we ran (E3)

- **Model and data.** Qwen3-1.7B, bf16 (the model of their Fig. 21 ladder), on the first 2,048 items of COCO
  train2014 (caption 0) and of SPC, in their row order.
- **Row-order check.** Our MPNet embeddings of the shipped captions match their stored rows: SPC cos 1.000;
  COCO caption 0 retrieves its own row 95.7% of the time.
- **Metric.** Their clipped CKA against their stored DINOv2-B rows, averaged over 1,024-item slices (their
  token-pooling protocol).
- **Execution.** One model load. A smoke gate (determinism, finite values, CKA(x, x) = 1) ran first.
- **Receipts.** `results/e3_pooling_scaffold/job-9426423166f5/` and `job-5fd45e7c7f0d/` (the amendment). The
  amendment run reproduced every shared arm of the first run exactly. Earlier attempts were killed on VRAM before
  emitting any report (PREREG Amendment 1).

**Replication check.** Our 1.7B replication of their pooling scores clipped CKA 0.591 on SPC. Their stored 8B
file scores 0.607 on the same 2,048 rows.

### 3.3 Results (final layer, clipped CKA with DINOv2-B)

| arm | COCO | SPC |
|---|---:|---:|
| their generative pooling (`think/gen_all`) | **0.623** | **0.591** |
| think + token-centered (`gen_tokcentered`, A2 arm) | 0.602 | 0.573 |
| think + leave-own-out frequent-token centering (`gen_tokcentered_loo20`, A2′ arm) | 0.609 | 0.581 |
| think + position-centered (control) | 0.616 | 0.583 |
| no thinking (`nothink/gen_all`) | 0.587 | 0.548 |
| no thinking + token-centered | 0.591 | 0.571 |
| no thinking + leave-own-out centering | 0.595 | 0.575 |
| their mean pooling, all chat tokens | 0.505 | 0.583 |
| mean pooling, caption tokens only | 0.506 | 0.596 |
| their stored MPNet (reference) | 0.687 | 0.633 |

Scaffold token share: with thinking on, the token at each of the first 16 positions is the same for 96–100% of
captions on both corpora. `</think>` was never reached within 128 tokens (0% of items).

**Frozen bars and measured effects.** The effect column gives the paired difference per 1,024-item slice
(COCO / SPC, final layer). Both slices have the same sign in every cell. Receipt: `verdicts.json` → `effects`.

| prediction | frozen bar | measured effect | reading |
|---|---|---|---|
| A1: scaffold share ≥ 0.9 at the first 12 positions | true | 0.96–1.00 | preamble present |
| A2: token-centered beats theirs in ≥ 3/4 cells | false (0/4) | −0.021 / −0.019 | opposite sign |
| A2′: post-hoc corrected arm (leave-own-out, tokens with ≥ 20 occurrences, 92–93% of positions centered) | false (0/4) | −0.015 / −0.010 | opposite sign |
| A3: best scaffold-removed arm on SPC gains ≥ 0.02 | false | −0.004 (best 0.587 vs 0.591) | no gain under any margin |
| A4: caption-token mean pooling ≥ all-token | true | +0.002 / +0.013 | supported on SPC; COCO is a tie in size |

Claim A is refuted on the effect, not on a margin. Every thinking-on centering arm moves CKA the wrong way.

**Reading.**
- **What the preamble is.** It is real and shared. It is not an independent scaffold in Lemma A1's sense. With
  thinking on, the model restates the caption inside its reasoning ("…what it would look like to see a close-up
  of bins of food that include broccoli and bread"). So the token identities carry content, and centering them
  away removes signal.
- **When centering helps.** With thinking off, where the text is a free-form description, centering helps in
  every cell: token-centering +0.004 / +0.023, leave-own-out +0.008 / +0.027 (COCO / SPC). This is the
  Lemma A1 sign, in the one setting where the removed tokens are not a restatement of the caption.
- **No free gain from switching modes.** Thinking on beats thinking off at the final layer by 0.036–0.043.
  Removing the preamble by turning thinking off is not a free gain either.

### 3.4 Post-hoc finding: a single non-visual axis in their stored 8B generative embeddings (measured offline)

The audit question was: if the token-level scaffold is not the problem, why does their generative pooling align
near chance on long captions while its clipped CKA (0.607) is close to MPNet's (0.633)? We examined their stored
SPC embeddings directly: 4,096 rows of DINOv2-B and of each language model. Script:
`experiments/e5_scaffold_axis/axis_probe.py`. Receipt: `results/e5_scaffold_axis/e5_axis_probe-20261009T191307.json`.
The length correlation and mutual k-NN rows come from the first 2,048 and 1,024 rows.

| SPC, first 4,096 rows | Qwen3-8B gen | Qwen3-Embedding-8B | MPNet |
|---|---:|---:|---:|
| clipped CKA (their appendix metric) | 0.608 | 0.659 | 0.636 |
| **linear CKA** (their main predictor family) | **0.433** | 0.657 | 0.633 |
| top language PC: share of variance | **13.8%** | 5.4% | 6.7% |
| held-out R² of top language PC from the image embedding | **0.16** | 0.89 | 0.88 |
| \|corr\| of top language PC with top image PC | 0.006 | 0.889 | 0.901 |
| corr of top language PC with paragraph length (n = 2,048) | 0.229 | −0.034 | 0.071 |
| **linear CKA after projecting out the top language PC** | **0.583 (↑)** | 0.498 (↓) | 0.466 (↓) |
| mutual 10-NN with the image embedding (local geometry) | **0.216** | 0.349 | 0.330 |

Lemma A1 predicts exactly these opposite signs:
- removing a scaffold that is independent of content raises CKA;
- removing an axis that is shared with the image lowers it.

The top axis of Qwen3-gen behaves as a scaffold: it holds 13.8% of the variance, the image predicts it with
R² 0.16, and removing it raises linear CKA by 35%. The top axes of the other two encoders are the image's own top
axis. The implied scaffold ratio for gen is about ρ ≈ 0.9, from 0.583/0.433 = 1.35 ≈ sqrt(1 + ρ²).

Two consequences for their paper:
1. **The clipped CKA in their App. D hides the deficit.** It gives 0.61–0.66 for all three encoders, while linear
   CKA separates gen (0.433) from the others (0.63–0.66). The clipping bounds the dominant axis's large
   coordinates, so a predictor built on clipped features over-predicts alignability for generative pooling.
2. **Low local agreement points to the same thing.** Mutual k-NN (0.216 vs 0.33–0.35) suggests the axis
   reorganizes neighborhoods, which the Hungarian matching in their refinement depends on.

**Does removing the axis help their aligner? (E5, measured in part.)** Protocol: their aligner with default
settings, trained on SPC minus the last 2,000 items, FOSCTTM on those 2,000. Receipt: `results/e5_scaffold_axis/e5_scaffold_axis-20261009T205002.json` (seed 0; seeds 1–4 running on the fleet).

| SPC holdout FOSCTTM (seed 0) | Qwen3-8B gen | Qwen3-Embedding-8B | MPNet |
|---|---:|---:|---:|
| raw (their pipeline) | 0.407 | 0.022 | 0.043 |
| drop top language PC (training rows, no pairs) | **0.036** | 0.402 | 0.361 |
| unpaired detector (drops PCs that pseudo-pairs cannot predict) | 0.484 (dropped PC 8 only) | 0.022 (dropped none) | 0.043 (dropped none) |

Projecting one axis out of the language side takes Qwen3-gen from near chance to about 3.6% of keys outranking
the partner. The same operation wrecks the two controls (0.022 → 0.402, 0.043 → 0.361), which is the Lemma A1
sign pattern on their aligner's own metric. Mechanism (inferred from the sign pattern and §3.4): their aligner
locks onto the dominant axis of each space. For MPNet and Qwen3-Embedding that axis is the image's own top axis
(|corr| 0.89–0.90), so it is the main thing they align on. For Qwen3-gen it is non-visual (|corr| 0.006), so the
image's top axis gets matched to a scaffold and the alignment collapses. Dropping the top PC is therefore a fix
only for an encoder known to carry such an axis. As a blanket rule it destroys good alignments. The axis is estimated from unpaired language rows alone, but "drop the top PC" is chosen with
knowledge from the axis probe. The detector arm is the version that needs no such knowledge.

**The detector failed on gen (measured, single seed).** It kept the scaffold axis and dropped PC 8, and FOSCTTM
went from 0.407 to 0.484. On its pseudo-pairs, the mapped vision side predicts the top language PC with R² 0.855,
against 0.16 on true pairs. Probable mechanism (inferred): the pseudo-pairs come from the raw fit, and that fit
had already rotated the image side onto the scaffold axis, so the test is circular. It certifies whatever the
broken fit matched. An unpaired detector has to be independent of the fit it is correcting. The §3.4 CKA sign
test needs true pairs, so it is not available. One unpaired candidate: drop a PC only if doing so raises their own
cluster-level QAP objective (kernel alignment of the k-means centroids at the matched optimum), which uses no
prior fit. *(Superseded by the gate detector below.)*

**Seed spread for the fix (measured, Beast, seeds 0–2).** Qwen3-gen raw: 0.419 / 0.358 / 0.467 (mean 0.415, SD
0.055). Drop the top PC: 0.033 / 0.044 / 0.037 (mean 0.038, SD 0.006). The change of −0.377 is about 7 raw SDs, so
P5a's gen half passes the amended noise rule. The controls' collapses (+0.32, +0.38) are far beyond any plausible
seed noise and were not re-seeded.

### 3.5 An unpaired gate detector (measured)

**Origin.** Our spectral dimension ladder: one learned gate per axis drove every nuisance gate to exactly 0 (61/61
at 64 axes), and leftover gates were pruned by choosing the setting that scored best on discovery data. Those
gates were trained on a supervised loss. Here the only signal is the alignment, and gating inside the fit is
circular: that is the detector failure above. So we port the second mechanism, **discovery selection**:
- one fresh fit per gate setting (none, or gate off one of language PCs 0–4, estimated on unpaired rows);
- each fit scored on its own training rows with no true pair. **S1** is the mean cosine of Hungarian-matched pairs,
  i.e. how well one rotation makes the two clouds coincide as sets. **S2** is linear CKA over the matched pairs;
- the setting with the highest score is chosen.

Script: `experiments/e5_scaffold_axis/gates.py`. Predictions were frozen in its header before any score was seen.
Seed 0, Beast, SPC holdout:

| setting | Qwen3-8B gen S1 | FOSCTTM | Qwen3-Emb-8B S1 | FOSCTTM | MPNet S1 | FOSCTTM |
|---|---:|---:|---:|---:|---:|---:|
| no gate | 0.473 | 0.419 | **0.516** | **0.021** | **0.524** | **0.030** |
| gate off PC0 | **0.517** | **0.033** | 0.439 | 0.364 | 0.483 | 0.325 |
| gate off PC1 | 0.464 | 0.460 | 0.469 | 0.337 | 0.489 | 0.297 |
| gate off PC2 | 0.470 | 0.377 | 0.476 | 0.168 | 0.500 | 0.118 |
| gate off PC3 | 0.469 | 0.293 | 0.476 | 0.100 | 0.519 | 0.043 |
| gate off PC4 | 0.469 | 0.459 | 0.498 | 0.032 | 0.492 | 0.096 |

(FOSCTTM uses true pairs and is evaluation only.)

- **G1 (the falsifier): holds.** S1 chooses gate-off-PC0 for Qwen3-gen and no gate for both controls.
- **G2: holds.** In all three models the S1 choice is also the best-FOSCTTM setting.
- **G3: mixed.** S2 agrees for Qwen3-gen and Qwen3-Embedding but picks gate-off-PC3 for MPNet: S2 0.671 vs 0.665;
  FOSCTTM 0.043 vs 0.030, a small cost. S1 is the better selector.
- **S1 tracks alignment quality across settings.** Rank correlation with −FOSCTTM is 0.94 (Qwen3-Embedding),
  0.94 (MPNet) and 0.77 (Qwen3-gen). For S2 it is 0.83, 0.89 and 0.26.
- **Seeds (measured, seeds 0–2, each model's top two settings).** S1 picks correctly in **9 of 9** model × seed
  cases, and every pick is also the best-FOSCTTM setting of the pair.

  | model | S1 choice | S1 margin over runner-up (seeds 0 / 1 / 2) | FOSCTTM chosen vs runner-up |
  |---|---|---|---|
  | Qwen3-8B gen | gate off PC0 | 0.044 / 0.030 / 0.041 | 0.033–0.044 vs 0.358–0.467 |
  | Qwen3-Embedding-8B | no gate | 0.017 / 0.023 / 0.013 | 0.013–0.023 vs 0.032–0.050 |
  | MPNet | no gate | 0.005 / 0.023 / 0.021 | 0.014–0.034 vs 0.030–0.063 |

  MPNet's thin seed-0 margin did not recur.

**What this gives them.** A fully unpaired rule for deciding whether an embedding has a non-visual dominant axis,
and which one. It fixes their worst long-caption cell (near chance → 0.033) and leaves the encoders that were
already good unchanged. The cost is six fits instead of one.

- **Predictions frozen in the E5 script header before any E5 FOSCTTM was seen.**
  - P5a: dropping the top PC lowers FOSCTTM for gen and raises it for the others.
  - P5b: the unpaired detector drops the top PC for gen only.
  - P5c: the detector never hurts, and helps gen.
- **Scored (seed 0; the seed-spread rule is applied when seeds 1–4 land).**
  - P5a: **holds in direction**, with large changes: gen −0.371; the two controls +0.38 and +0.32.
  - P5b: **false.** The detector dropped PC 8, not PC 0, for gen; it correctly dropped nothing for the others.
  - P5c: **false for gen** (+0.077, worse). For the controls it dropped nothing, so FOSCTTM is unchanged.
- **Scoring amendment, disclosed.** It was written after seeing the two gen numbers above, and before any
  detector or control number. A change counts as a direction only if it exceeds twice the seed SD of that
  model's raw arm (seeds 0–2, queued). The detector's R² < 0.3 cut is a method setting; every PC's R² is kept
  so other cuts can be rescored. For gen the gap between the axis (R² 0.16 on true pairs) and the shared axes
  (0.88–0.89) means any cut between about 0.2 and 0.85 gives the same decision on true pairs. On pseudo-pairs
  this failed: see the detector result above.

---

## 4. Claim B: is the final layer past the commit layer? (measured: yes in direction, small)

Our language-model work places a late commit band at about 0.7–0.9 of depth. We predicted the best alignment
depth for caption-token mean pooling and no-thinking generative pooling would be below 1.0 (B1) and in 0.6–0.9
(B2).

| arm, clipped CKA by depth (L/28) | 0.50 | 0.61 | 0.71 | 0.79 | 0.89 | 1.00 |
|---|---:|---:|---:|---:|---:|---:|
| COCO, their mean pooling (all chat tokens) | 0.328 | 0.341 | 0.332 | 0.468 | **0.516** | 0.505 |
| SPC, their mean pooling (all chat tokens) | 0.298 | 0.294 | 0.299 | 0.533 | **0.590** | 0.583 |
| COCO, mean pooling (caption tokens) | 0.330 | 0.347 | 0.339 | 0.473 | **0.519** | 0.506 |
| COCO, no-think gen | 0.419 | 0.365 | 0.374 | 0.594 | **0.602** | 0.587 |
| SPC, mean pooling (caption tokens) | 0.325 | 0.312 | 0.304 | 0.537 | 0.594 | **0.596** |
| SPC, no-think gen | 0.328 | 0.260 | 0.277 | 0.545 | **0.557** | 0.548 |
| COCO, think gen (theirs) | 0.412 | 0.358 | 0.367 | 0.589 | 0.621 | **0.623** |
| SPC, think gen (theirs) | 0.300 | 0.238 | 0.255 | 0.519 | 0.564 | **0.591** |

**Frozen bars.** B1 (best depth < 1.0 in all four scored cells) and B2 (best depth in 0.6–0.9 in all four) are
false. Both fail on one cell, SPC caption-token pooling, where 1.0 beats 0.89 by 0.002 (0.596 vs 0.594).

**Measured effect (depth 0.89 minus 1.0, paired per slice).**
- **No thinking, 6 cells:** +0.011 / +0.007 for their mean pooling (COCO / SPC), +0.012 / −0.002 for
  caption-token pooling, +0.015 / +0.008 for no-thinking generation. Five of six are positive in both slices.
- **Thinking on (their headline generative arm):** −0.002 / −0.027. The final layer is best.

**Reading.**
- **Direction.** The claim holds in direction for mean pooling and no-thinking generation, including their own
  `MeanPooling`. A one-cell tie should not have decided it.
- **Size.** The effect is small, 0.007–0.015 clipped CKA, and whether it moves FOSCTTM is untested.
- **Shape.** CKA jumps between depth 0.71 and 0.79 in every arm (+0.13 to +0.27) and then plateaus, which is
  consistent with content being formed late. The depth grid has only 0.79 and 0.89 between 0.71 and 1.0, so the
  peak is not localized more finely than that.
- **Thinking mode.** The thinking-mode arm keeps improving to the last layer, so for their best generative
  embedding, choosing a layer gives nothing.

---

## 5. Claim C: a provable fidelity ceiling for span-confined pair baselines

Notation: ŷ is a centered, unit-normalized key; X̂_p and Ŷ_p are the p known pairs; V_p = rowspan(Ŷ_p); P is
the projector onto V_p; λ_1 ≥ λ_2 ≥ … are the eigenvalues of Σ̂ = E[ŷŷᵀ], so Σλ = 1.

**Lemma C1 (span confinement, exact).** Their `linear` baseline is W = X̂_p⁺ Ŷ_p. Then x̂W = (x̂ X̂_p⁺) Ŷ_p ∈ V_p,
so sim(x, y) = ⟨x̂W, Pŷ⟩. Keys are ranked using only their p-dimensional projection Pŷ. ASIF compares keys
through ŷŶ_pᵀ, which is also a function of Pŷ.

**Lemma C2 (fidelity ceiling).** For any map whose image lies in V_p,

```
E_i α_i ≤ E_i ||P ŷ_i|| ≤ sqrt(E_i ||P ŷ_i||²) = sqrt(tr(P Σ̂)) ≤ sqrt(Σ_{k≤p} λ_k).
```

*Proof.* Cauchy–Schwarz gives α_i ≤ ||Pŷ_i||; then Jensen; then Ky Fan's maximum principle. ∎

**Remarks.**
1. Their `orthogonal` baseline is informed by the data only on V_p. On the complement it is an arbitrary isometry
   set by the SVD's numerical completion. The ceiling holds in expectation under a random completion; this is a
   heuristic, not a bound.
2. Their own method with pairs is not span-confined, because the unpaired Procrustes term informs every
   direction. This is a structural reason it dominates at small p.
3. The same span argument explained an instrument failure in our own work: a dual-ridge bridge scored 0/54 on
   held-out symbols because its predictions are confined to span(Y_fit).

**Smoke check (3,000 training rows, not a result).** At p = 5, linear α 0.146 ≤ sqrt(0.086) = 0.29; at p = 20,
0.335 ≤ 0.575.

**Measured (E2, COCO val, MPNet, one draw per p).** Receipt: `results/e2_span_bound/e2_span_bound-20261009T222209.json`.

| p | energy E‖Pŷ‖² | Ky Fan max | sqrt(energy) | linear α | linear FOSCTTM | orthogonal α | orthogonal FOSCTTM | theirs α | theirs FOSCTTM |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.016 | 0.080 | 0.127 | 0.038 | 0.422 | 0.007 | 0.462 | | |
| 5 | 0.085 | 0.266 | 0.291 | 0.144 | 0.228 | 0.035 | 0.333 | **0.498** | **0.0090** |
| 20 | 0.328 | 0.548 | 0.572 | 0.328 | 0.109 | 0.153 | 0.139 | **0.494** | **0.0075** |
| 50 | 0.572 | 0.768 | 0.756 | 0.444 | 0.048 | 0.262 | 0.052 | | |
| 200 | 0.889 | 0.962 | 0.943 | 0.515 | 0.016 | 0.405 | 0.013 | | |
| 1000 | 1.000 | 1.000 | 1.000 | 0.426 | 0.018 | 0.506 | 0.005 | | |

Random pairs (their protocol). The full ladder (p = 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, random and medoid) is
in the receipt.

Predictions:
- **C-i: holds.** Linear α ≤ sqrt(energy) in all 20 rows, as the theorem requires.
- **C-ii (energy explains the baselines at fixed p).** With one draw per p, the within-p test reduces to sign
  agreement. Wherever medoid pairs capture more energy (every p ≤ 200), linear FOSCTTM is lower: 7 of 7. For
  orthogonal FOSCTTM it is 6 of 7; at p = 1, orthogonal is worse with medoids (0.479 vs 0.462). No noise band
  (draw-spread runs were pruned).
- **C-iii: holds at p = 5, not at p = 20.** Their method's α (0.498) exceeds the span ceiling at p = 5 (0.291)
  but not at p = 20 (0.494 vs 0.572).

Reading:
- **The ceiling is valid but loose.** At p = 20 the linear baseline reaches 0.328 against a ceiling of 0.572.
  What separates their method from the baselines is not the bound but the data. With 5 pairs it already matches
  what the baselines reach only at p ≈ 200–1000 (FOSCTTM 0.009 vs 0.013–0.016), with α 0.49–0.50 against
  0.14–0.33 for the baselines at p ≤ 20.
- **Least squares overfits near p ≈ d.** Linear α falls from 0.515 (p = 200) to 0.426 (p = 1000; span rank 766
  of 768) and FOSCTTM rises. This is the interpolation regime of the pseudo-inverse.

---

## 6. Claim D: retrieval quality does not certify consumer fidelity

**Proposition D1.** Let the keys ŷ_j and the mapped query q_i be unit vectors, with α_i = ⟨q_i, ŷ_i⟩ and
q_i = α_i ŷ_i + β_i u_i, where β_i = sqrt(1 − α_i²) and u_i ⟂ ŷ_i. Distractor j outranks the partner exactly when
β_i ⟨u_i, ŷ_j⟩ > α_i (1 − c_ij), with c_ij = ⟨ŷ_i, ŷ_j⟩. If u_i is uniform on a sphere of effective dimension
d_eff orthogonal to ŷ_i, then

```
P(j outranks i) ≈ Φ̄( (α_i/β_i) · sqrt((d_eff − 1)(1 − c_ij)/(1 + c_ij)) ),
```

and this goes to 0 for any fixed α_i > 0 as d_eff grows. For example, with d_eff = 100 and c = 0.1, α = 0.3 gives
P ≈ 0.003. Retrieval is a margin property that improves with dimension; fidelity is not.

**Why it matters for generation.** A generator conditioned on q_i receives α_i of the true signal. Our FLUX.2
consumer measured three zones of direction fidelity: ≥ 0.895 rendered the target in 8/8 cells; ≤ 0.50 failed;
0.71–0.78 depended on target and seed. These thresholds belong to that consumer and are not claimed for their
RAE.

### 6.1 Measured (E1, COCO val2014, DINOv2-B ↔ MPNet, their protocol)

Receipt: `results/e1_fidelity_gap/e1_fidelity_gap-20261009T200203.json`. Single seed per arm; the oracles are closed-form fits on 20,000 true pairs.

| arm | FOSCTTM | α median | α q05–q95 | α ≥ 0.895 | α ≤ 0.50 |
|---|---:|---:|---|---:|---:|
| **ours-p0** (their method, no pairs) | **0.0073** | **0.527** | 0.260–0.757 | **0.0%** | **43.3%** |
| ours-p0, seeds 1 / 2 (Beast) | 0.0259 / 0.0149 | 0.474 / 0.495 | | | |
| ours-p10 (10 known pairs) | 0.0125 | 0.473 | 0.205–0.725 | 0.0% | 56.3% |
| ours-p100 (100 known pairs) | 0.0056 | 0.507 | 0.267–0.731 | 0.0% | 48.3% |
| orthogonal oracle (20,000 true pairs) | 0.0027 (all seeds) | 0.572 (0.571–0.572 over seeds) | 0.344–0.766 | 0.0% | 30.1% |
| least-squares oracle (20,000 true pairs) | **0.0026** | **0.781** | 0.547–0.901 | 6.5% | 2.8% |

Distractor similarity for ours-p0: mean ≈ 0.000, 99th percentile 0.466.

**Claim D: supported.** The claim is that near-zero FOSCTTM does not certify per-pair fidelity. The
measurement:
- **Near-perfect retrieval.** Only 0.73% of keys outrank the true partner.
- **Fidelity well below that.** The median cosine to the partner is 0.527. That means α² ≈ 0.28: about 72% of a
  mapped vector's energy is not along its partner.
- **The FLUX zones.** These were measured on a different consumer and a different space, so they are a
  reference scale only. Not one of 40,504 validation pairs reaches ≥ 0.895, where FLUX rendered 8/8; 43% are
  ≤ 0.50, where it failed.
- **Ten known pairs.** They make both retrieval (FOSCTTM 0.0073 → 0.0125) and fidelity (median 0.527 → 0.473)
  slightly worse. Both are single-seed fits, and seed spread is unmeasured, so we draw no direction from it.

*Retired bars.* Before E1 we wrote two numeric bars: D-i, median α < 0.5 at FOSCTTM < 0.1, and D-ii,
orthogonal-oracle median α < 0.7. Nothing grounds 0.5 or 0.7: neither is a consumer zone, a bound or a noise
floor. D-i reads "false" at 0.527 for ours-p0 and "true" at 0.473 for ours-p10, while the claim's evidence is the
same in both. We still report the bars' outcomes, but they do not decide Claim D.

**The cleanest evidence for Claim D (measured).** The two oracles retrieve identically (FOSCTTM 0.0027 vs
0.0026), yet their median fidelity differs by 0.21 (0.572 vs 0.781). FOSCTTM cannot tell them apart. Fidelity
can.

**Headroom decomposition (measured; median α, mean in parentheses).**

| gap | from → to | size |
|---|---|---:|
| unpaired estimation | ours-p0 → best rotation (orth-oracle) | 0.073 ± 0.027 over seeds 0–2 (0.044, 0.097, 0.077) |
| the rotation constraint | best rotation → best linear map (lin-oracle) | 0.210 (0.195) |
| linearity and the rest | best linear map → 1 | 0.219 (0.239) |

Reading:
- **Their unpaired estimate is close to the best rotation.** With zero pairs it sits 0.07 ± 0.03 below a
  rotation fitted on 20,000 true pairs. Retrieval-wise it is within 0.005 FOSCTTM.
- **The fidelity ceiling is the rotation itself.** No single rotation reaches FLUX's ≥ 0.895 zone for any
  validation pair. The orthogonality constraint costs about as much as everything that remains after it.
- **What a few pairs buy.** 10 and 100 known pairs did not raise fidelity (0.473, 0.507 vs 0.527). Each is a
  single seed with unmeasured seed spread, so no direction is drawn. Under this decomposition little is expected
  anyway: pairs can only close the ~0.07 estimation gap while the map stays a rotation.
- **Consequence for generation (inferred).** If a consumer needs high per-item fidelity, the lever is the map
  class, not better unpaired estimation. Examples are a non-orthogonal correction fitted on a few anchors
  (Claim E), or per-concept anchors as in our symbol work.

**Proposition D1 checked (E1b, measured, `results/e1_fidelity_gap/e1_d1_check-20261009T211416.json`).** Oracle
maps fitted on p true pairs; prediction from each map's median α and the residual's effective dimension (participation
ratio), on 2,000 validation queries.

| map, p | median α | d_eff | predicted FOSCTTM | measured FOSCTTM |
|---|---:|---:|---:|---:|
| orth, 20 | 0.109 | 85 | 0.189 | 0.138 |
| lin, 20 | 0.286 | 11 | 0.185 | 0.108 |
| orth, 200 | 0.399 | 146 | 0.0047 | 0.0122 |
| orth, 2,000 | 0.533 | 180 | 0.0002 | 0.0037 |
| orth, 20,000 | 0.572 | 183 | 0.0001 | 0.0027 |
| lin, 20,000 | 0.781 | 69 | ≈ 0 | 0.0026 |

- **The magnitude is wrong where retrieval is good.** Below FOSCTTM ≈ 0.02 the proposition underpredicts by 3–30×.
  Probable cause (inferred): it treats the residual as isotropic and ignores near-duplicate keys, which dominate the
  tail of the ranking. We keep D1 as a qualitative argument only.
- **The qualitative content holds.** Retrieval depends on α/β and d_eff together, not on α alone. The least-squares
  map has much higher fidelity than the rotation (0.781 vs 0.572), but its residual is concentrated in fewer
  directions (d_eff 69 vs 183), so the two retrieve identically.

---

## 7. Claim E: choose the pairs

The Lemma C2 ceiling is reached when V_p aligns with Y's top-p eigenspace. In the few-pair setting the
experimenter chooses which items to annotate, and can do so from the unpaired images alone. Their premise (shared
geometry) implies that well-spread images have well-spread captions.

**Prediction (E2 + E2b).** Vision-side k-means medoid pairs capture more energy than random pairs for p ≤ 50, and
lower linear and orthogonal FOSCTTM. E2 has one draw per p, so a single draw could not separate this from luck.
E2b (`e2_span_bound/draws.py`, queued after E2) adds seeds 1–5 for both selections at p ≤ 100. At each p,
medoids count as better when the mean difference over seeds 0–5 exceeds twice its standard error. Otherwise the
result is "no detectable difference" at that p.

**Measured (E2, one draw per p; E2b draw spread pruned).**
- **Baselines: yes, in direction.** Medoid pairs capture more energy at every p ≤ 200 (for example, 0.085 → 0.128
  at p = 5 and 0.328 → 0.382 at p = 20), and lower linear FOSCTTM at every one of those p (0.228 → 0.161 at p = 5,
  0.109 → 0.067 at p = 20).
- **Their method: no.** Medoids gave 0.0252 vs 0.0090 at p = 5, and 0.0067 vs 0.0075 at p = 20. Single fits.
- **Consequence.** Pair selection helps the baselines that their method already beats with zero pairs. It is not
  a contribution to their method, and we dropped the draw-spread runs for that reason.

The analogue in our work: one anchored example per symbol lifted bridge fidelity to 0.93–0.99. With that, the
bridge authored held-out symbols through the image generator.

---

## 8. Claim F: a consumer-grounded benchmark (design)

The design is in `experiments/e4_consumer_closure/DESIGN.md`:
1. Build a 200-symbol displacement bank (SmolLM2 ↔ Klein-Qwen).
2. Fit their unpaired aligner and record per-symbol α.
3. Render about 24 symbols spread over α through the frozen FLUX.2 Klein 4B, with a native ceiling, a shuffled
   sham and an exact no-op.
4. Prediction: render progress rises with α. Once α is known, retrieval rank adds little: report the extra
   variance in progress that rank explains, with a bootstrap interval. "Nothing" is not a claim we can test.

**[PENDING E4: not built.]**

---

## 9. What they might see

| change | evidence | expected effect | status |
|---|---|---|---|
| Report linear CKA (or CKA after deflating the top axis) next to clipped CKA, especially for generative pooling | §3.4: clipped 0.61 vs linear 0.43 for gen | a predictor that no longer over-rates generative pooling | measured on SPC; other corpora untested |
| Remove the non-visual axis of generative pooling | Lemma A1 + §3.4 + E5 | Qwen3-gen 0.415 → 0.038 FOSCTTM (3 seeds); controls unchanged when the gate detector chooses | measured on the SPC holdout; gate detector correct in 9/9 model × seed cases; DCI/DOCCI and their COCO-val protocol untested |
| Report α next to FOSCTTM | Prop. D1 + §6.1 (oracles: equal FOSCTTM, α 0.57 vs 0.78) | separates maps that retrieval ranks as equal | measured (E1) |
| For generation, relax the rotation (e.g. a non-orthogonal correction on a few anchors) | §6.1 decomposition: rotation constraint costs 0.21 median α; unpaired estimation 0.07 ± 0.03 | higher per-item fidelity; better unpaired estimation alone cannot exceed the rotation ceiling | ceiling measured; few-anchor correction untested |
| ~~Medoid pair selection~~ | E2 | helps span-confined baselines only; their method is unchanged or worse at p = 5 | **not a contribution to their method** |
| A few anchors per concept for generation | Lemma C2 + our k=1 result | moves α into the band one rotation cannot reach | conjecture |
| ~~Token-centering the thinking preamble~~ | E3 | lowers CKA at 1.7B with thinking on (−0.010 to −0.021) | **refuted** |
| Read mean pooling at depth ≈ 0.9 instead of the last layer | E3 §4 | +0.007–0.015 clipped CKA for mean pooling and no-thinking generation; none for thinking-mode generation | measured on CKA; effect on FOSCTTM untested |

## 10. Limits

- **E3** used Qwen3-1.7B, not their 8B. Our replication matches their 8B clipped CKA within 0.016 on SPC, but the
  token-level negative may not transfer to 8B. Two slices of 1,024 items per corpus.
- **The axis finding (§3.4)** is post-hoc, on one corpus (SPC), at one sample size (4,096). DCI and DOCCI are
  untested.
- **Lemma A1** assumes independence. The thinking preamble violates it, which is exactly why A2 failed.
- **Consumer thresholds** come from FLUX.2 Klein 4B and are not transferred to their RAE. They were measured on
  few cells (8/8 renders at ≥ 0.895) and on a different space, so they are a reference scale only.
- **Noise.** E3 slices are two halves of 2,048 items under greedy decoding. They measure sampling
  consistency, not model variance. E1 and E5 are single-seed fits; seed spread for E5 is queued, and for E1 it is
  unmeasured.
- **E0** uses 18 symbols, with a thin margin (0.053 to the best single swap).
- **Precision is not the cause of the axis (measured).** Their Qwen3-8B-gen file is stored fp32 (their loader
  docstring says bf16). Its rows share a large common direction (‖mean of unit rows‖ ≈ 0.93, against 0.38–0.66 for
  the other files), and centering removes it in fp32 with about 20 of 24 mantissa bits left in the residual. In the
  bf16 files, per-coordinate |mean|/σ is 6–13, far from the regime where rounding swamps a centered residual. The
  §3.4 axis is a property of the representation, not of storage.
- **E5's protocol differs from theirs.** E5 validates on an SPC holdout; their paper validates SPC-trained maps on
  COCO val.

## 11. Reproduce

`experiments/README.md`. Receipts are in `experiments/results/`. The E3 receipts hold the worker sha and the run
receipt; the frozen predictions and both amendments are in `experiments/e3_pooling_scaffold/PREREG.md`.

## References

1. Schnaus, Dagès, Cremers, Wang, Isola. Shared Geometry as a Rosetta Stone: Cross-Modal Alignment Without Paired
   Data. arXiv 2610.09411, 2026.
2. Huh, Cheung, Wang, Isola. The Platonic Representation Hypothesis. ICML 2024.
3. Kornblith, Norouzi, Lee, Hinton. Similarity of Neural Network Representations Revisited. ICML 2019.
4. Hutschenreiter et al. Fusion Moves for Graph Matching. ICCV 2021 (MPOpt).
5. Ky Fan. On a theorem of Weyl concerning eigenvalues of linear transformations. PNAS 1949.
6. Our internal records: FLUX encoder swap and symbol table (`obsidian/arcs/cross-conditioner-to-time-circuits.md`);
   LM commit band (`research/papers/space-and-time-circuits/`).
