---
title: "Reading Is Not Authoring: A Hidden Non-Visual Axis, an Unpaired Fix, and the Rotation Ceiling in Unpaired Cross-Modal Alignment"
subtitle: "A response to Schnaus, Dagès, Cremers, Wang and Isola, 'Shared Geometry as a Rosetta Stone' (arXiv 2610.09411)"
status: "DRAFT 3.2 (2026-10-23): readability pass, no content changes. E0, E1, E2, E3, E5 measured. E6 (generality) measured: the non-visual axis and the unpaired detector reproduce on SPC, DCI and DOCCI and are absent on short COCO captions, and the one-axis removal fix is SPC-specific. E6b (oracle): given true pairs, a single rotation aligns gen on all three corpora, so the failure off SPC is a failure of the unpaired search, not of the geometry. E4 designed, not built."
date: 2026-10-22
authors: TBD
code: experiments/ (their library pinned at fdfad84; every scored number has a JSON receipt in experiments/results/)
---

# Reading Is Not Authoring

**A hidden non-visual axis, an unpaired fix, and the rotation ceiling in unpaired cross-modal alignment.**
*A response to Schnaus, Dagès, Cremers, Wang and Isola, "Shared Geometry as a Rosetta Stone" (arXiv 2610.09411).*

> **How to read this report.**
> *Measured* results cite a receipt (a JSON file) under `experiments/results/`. *Inferred* marks a mechanism read
> from measurements but not tested directly. *Post-hoc* marks a result found after a frozen test.
>
> We judge a claim by the direction and size of the measured effect against its noise (slice-to-slice agreement,
> seed spread). Predictions were frozen before their runs, and we report the outcome of each frozen bar. A bar
> decides only its own prediction. Only a proved inequality, a measured noise floor or a consumer zone measured on
> FLUX (labelled as such) may decide a claim (§9).
>
> One placeholder remains: E4, the consumer benchmark (§7), which is designed but not built.

## Abstract

Schnaus et al. show that separately trained vision and language encoders share enough geometry to be aligned by a
single rotation, with no paired data. We first check this premise on a new kind of pair. With no pairs, their solver
recovers an 18-symbol correspondence between SmolLM2 and the text conditioner of a diffusion model exactly. (The
solver is a quadratic assignment problem, QAP: it finds the permutation that best matches two similarity matrices.)
We then report three results that their evaluation does not show.

1. **A non-visual axis in generative embeddings, and an unpaired fix.** In their stored Qwen3-8B generative
   embeddings of long captions ("gen"), one axis carries 13.8% of the variance, and the image embedding barely
   predicts it (R² 0.16, against 0.88–0.89 for MPNet and Qwen3-Embedding). Linear CKA, the predictor in their main
   text, shows gen's deficit, and the deficit sits on this axis. The clipped CKA of their Appendix D does not show
   it on Stanford Paragraph Captions (SPC). Under their aligner, removing that one axis takes SPC holdout FOSCTTM
   from **0.415 ± 0.055 to 0.038 ± 0.006** over three seeds. Removing the top axis of MPNet or Qwen3-Embedding
   instead wrecks them, so this is not a blanket rule.

   A detector that uses no pairs picks the right setting for all three encoders. At seed 0 it chooses among six
   settings (nothing removed, or one of the top five axes removed). At seeds 1 and 2 it keeps the same choice over
   the seed-0 runner-up (9 of 9 encoder × seed comparisons). It removes Qwen3-gen's axis and leaves the other two
   encoders alone. Every choice is the best of the settings compared on true-pair FOSCTTM. The MPNet margin at
   seed 0 is thin (0.005 in S1, the detector's score).

   Generality (E6, §3.6). The axis reproduces on their two other long-caption corpora (DenselyCaptionedImages and
   DOCCI; top-PC variance 19–22%, image R² 0.05) and is absent on short COCO captions (image R² 0.90). It is
   therefore a long-caption effect, and the unpaired detector still selects it. Removing it rescues the alignment
   only on SPC. An SPC-fit map with the axis removed transfers to held-out COCO-val (0.409 → 0.022). On DCI and DOCCI
   the same projection leaves gen near chance (~0.39–0.48), not at the control encoders' ~0.10.

   An oracle that is given the true pairs shows why (E6b). A single rotation aligns Qwen3-gen to the image on all
   three corpora, with or without the axis (holdout FOSCTTM 0.007–0.014, against 0.001–0.003 for Qwen3-Embedding).
   The encoder they find weakest is therefore not geometrically misaligned. What fails is the unpaired search, which
   the non-visual axis misleads. Removing the axis is a search aid: it suffices on SPC and not on DCI or DOCCI, and
   eight pairs-free restarts do not close the gap.
2. **Retrieval is not fidelity, and the rotation is the ceiling.** We call the cosine between a mapped item and its
   true partner its fidelity (α). On COCO their zero-pair map retrieves almost perfectly (FOSCTTM 0.0073), yet its
   median cosine to the true partner is 0.53. Two oracle maps fitted on 20,000 true pairs retrieve identically
   (FOSCTTM 0.0027 vs 0.0026) but differ by 0.21 in median fidelity (0.57 vs 0.78). The fidelity gap is not an
   estimation error: their zero-pair map is only 0.07 ± 0.03 below the best rotation. The orthogonality constraint
   costs three times that.
3. **A span ceiling for pair baselines.** Their linear and ASIF baselines provably score keys through a
   p-dimensional projection, where p is the number of known pairs. Mean fidelity is therefore at most
   sqrt(top-p eigen-energy). The bound holds on their data but is loose. With 5 pairs their method already
   retrieves better than both baselines do with 200.

Two of our ideas failed, and we report them in §6. Token-centering the thinking preamble lowers CKA. Reading a late
layer instead of the last one helps by only 0.007–0.015 CKA, and not at all for thinking-mode pooling.

![Figure 1](figures/fig1-scaffold-axis-fix.png)

*Figure 1. **A.** SPC holdout FOSCTTM under their aligner. Bars are the mean over seeds; dots are individual seeds
(the control arms with the top PC removed are seed 0 only). **B.** For each encoder, the unpaired score S1 of
each of the six removal settings against its true-pair FOSCTTM, at seed 0. The ringed setting is the one S1 chooses.
Receipts: `results/e5_scaffold_axis/e5_gates-*.json`.*

---

## 1. Summary

### 1.1 What we offer them

| finding | measured result | what they could change |
|---|---|---|
| A non-visual dominant axis in Qwen3 generative pooling of long captions (§3, §3.6) | on SPC removing it: FOSCTTM 0.415 → 0.038 (3 seeds); the axis itself reproduces on DCI and DOCCI (variance 19–22%, image R² 0.05) and is absent on short COCO captions (R² 0.90); removing it leaves DCI/DOCCI near chance (~0.39–0.48), yet a true-pair rotation aligns gen on all three corpora (0.007–0.014), so the failure is the unpaired search | run the pairs-free detector before fitting, as a diagnostic (it flags the deficit on all three long-caption corpora); read gen's near-chance score as a search failure, not an incompatible geometry |
| Clipped CKA misses that axis on SPC (§3.5) | clipped CKA 0.61–0.66 for all three encoders; linear CKA 0.43 for gen vs 0.63–0.66, and 0.58 once the axis is projected out | in App. D, report linear CKA (the main-text predictor) next to clipped CKA |
| FOSCTTM does not measure fidelity (§4) | equal FOSCTTM (0.0027 / 0.0026), median α 0.57 vs 0.78 | report per-pair α next to FOSCTTM, especially for text-to-image use |
| The rotation, not the estimate, limits fidelity (§4.3) | estimation gap 0.07 ± 0.03; rotation constraint 0.21 | for generation, relax the rotation (for example a non-orthogonal correction on a few anchors); untested |
| Span ceiling of pair baselines (§5) | bound holds, loose; their method with 5 pairs retrieves better than the baselines with 200 | a proof of why their few-pair baselines need many pairs |

### 1.2 Every claim and its status

The letters in the first column are our working labels for claims, used in later sections. "A\*" is the
non-visual-axis claim. The E-numbers name our experiments.

| # | claim | test | status |
|---|---|---|---|
| — | Their premise holds for a language model vs a diffusion conditioner, at the symbol level | E0 | **confirmed**: 18/18 at zero pairs |
| A\* | *(post-hoc)* One non-visual axis dominates Qwen3-gen embeddings; an unpaired detector finds it; removing it fixes the alignment | axis probe, E5, removal settings | **mixed (E6)**: the axis and the detector reproduce on SPC, DCI and DOCCI and are absent on short COCO captions; the *removal fix* is SPC-specific (0.415 → 0.038 on SPC; only ~0.5 → ~0.4–0.47 on DCI/DOCCI); a true-pair oracle aligns gen on all three (0.007–0.014), so off SPC the unpaired search fails, not the geometry (E6b) |
| D | Near-zero FOSCTTM is compatible with low per-pair fidelity | E1, E1b | **supported**: equal-FOSCTTM oracles differ by 0.21 in α; the D1 formula is right in direction, off 3–30× in magnitude |
| C | Span-confined pair baselines: mean fidelity ≤ sqrt(top-p eigen-energy) | proof, E2 | **proved; holds on data**, but loose |
| E | Choosing pairs (vision-side medoids) helps | E2 | **baselines only**; no gain for their method |
| A | The thinking preamble dilutes CKA; token-centering removes it | E3 | **refuted**: centering lowers CKA in every thinking-on cell |
| B | A late, non-final layer aligns better | E3 | **supported, small**: +0.007–0.015 in 5 of 6 no-thinking cells; not for thinking mode |
| F | A consumer-grounded benchmark with causal ground truth | E4 | designed, not built |

### 1.3 Related work

Aligning separately trained representations without paired data has a long history. In word translation,
Gromov–Wasserstein matching aligns spaces by their internal pairwise similarities rather than absolute positions
(Mémoli 2011; Alvarez-Melis and Jaakkola 2018). MUSE learns an adversarial map, refines it with Procrustes, and
retrieves with CSLS (Conneau et al. 2018). It was an early separation of the *retrieval* criterion from the map
itself, which is the distinction §4 makes quantitative.

More recent work translates text embeddings across spaces with no pairs (vec2vec; Jha et al. 2025), using a shared
latent and a non-orthogonal decoder. This is the relaxed map class that §4.3 points to when per-item fidelity, not
retrieval, is the goal. Oozeer et al. (2025) map activation spaces between language models to transfer
interventions. Schnaus et al.'s own earlier QAP matcher (Blind Match, CVPR 2025) casts unpaired vision–language
correspondence as a quadratic assignment and notes that mutual k-NN, CKA and Gromov–Wasserstein are special cases
of it.

Against this background our contribution is a diagnosis, not another matcher. We show when their pipeline fails
(Qwen3 generative pooling on long captions) and why (a dominant non-visual axis, §3). We add a pairs-free detector
that flags the failure, and the two evaluation results in §4 and §5.

---

## 2. Their premise on our data (measured, E0)

Their premise holds for a language model against a diffusion-model conditioner, at the level of individual symbols.
The margin is thin, and the problem is small.

**Setting.**
- **Spaces.** Subject-row displacements (a subject row minus the template mean) of 18 animals × 4 distinct prompt
  prefixes. One space is SmolLM2-1.7B. The other is the Qwen3-4B text conditioner of FLUX.2 Klein 4B
  (7,680 dims). Source: our receipt `job-0706b0497903`.
- **Templates.** Six templates collapse to four, because causal models give bit-identical subject rows for templates
  that share the text before the subject.
- **Problem.** With zero pairs, maximize `Tr(K_A P K_B Pᵀ)` over permutations P, where K_A and K_B are the
  centered-cosine kernels of the class means. P matches each symbol in one space to a symbol in the other. This is
  their CKA-matching objective.

Receipt: `experiments/results/e0_symbol_qap/e0_symbol_qap-20261009T180533.json`.

| quantity | value |
|---|---|
| off-diagonal kernel correlation across spaces | 0.890 |
| zero-pair correspondence, 2-opt with 2,000 restarts | **18/18**; 169 of 2,000 restarts find it, and it is the best objective found (23.5915) |
| zero-pair correspondence, MPOpt (their solver and costs) | **18/18** |
| each prefix alone (4 independent problems) | 18/18 on every prefix |
| Gaussian-geometry null (10 draws) | 0–2 / 18 |
| margin to the next local optimum / to the best single swap | 0.236 / 0.053 |
| seeded with k = 1, 2, 3, 5 anchors (accuracy on the rest, scipy FAQ) | 0.22, 0.29, 0.52, 0.72 (chance 0.06–0.08) |
| fully unpaired rows (animal and prefix unknown) | 41.7% (chance 5.6%); source rows cluster by prefix (ARI 0.019), native rows by animal (0.331) |

- **Checked causally.** The recovered correspondence is the one our anchored bridge uses. That bridge authors
  held-out symbols through the image generator at native parity (progress 0.523–0.810 vs native 0.520–0.817).
- **Caveat.** The margin is thin, and 18 symbols is a small problem.

---

## 3. A hidden non-visual axis, and an unpaired fix

### 3.1 The axis (measured offline, post-hoc)

Their generative pooling of long captions has one dominant axis that the image embedding does not predict.

The preamble test in §6.1 did not explain why their generative pooling aligns near chance on long captions, even
though its clipped CKA (0.607) is close to MPNet's (0.633). We therefore examined their stored SPC embeddings
directly: 4,096 rows of DINOv2-B and of each language model. PC means principal component. Throughout, the
**non-visual axis** is a dominant principal axis of the text embeddings that the paired image embedding barely
predicts (held-out R² near 0). Script `experiments/e5_scaffold_axis/axis_probe.py`; receipt
`results/e5_scaffold_axis/e5_axis_probe-20261009T191307.json`.

| SPC, first 4,096 rows | Qwen3-8B gen | Qwen3-Embedding-8B | MPNet |
|---|---:|---:|---:|
| clipped CKA (their appendix metric) | 0.608 | 0.659 | 0.636 |
| **linear CKA** | **0.433** | 0.657 | 0.633 |
| top language PC: share of variance | **13.8%** | 5.4% | 6.7% |
| held-out R² of top language PC from the image embedding | **0.16** | 0.89 | 0.88 |
| \|corr\| of top language PC with top image PC | **0.006** | 0.889 | 0.901 |
| corr of top language PC with paragraph length (n = 2,048) [†] | 0.229 | −0.034 | 0.071 |
| **linear CKA after projecting out the top language PC** | **0.583 (↑)** | 0.498 (↓) | 0.466 (↓) |
| mutual 10-NN with the image embedding (n = 1,024) | **0.216** | 0.349 | 0.330 |

[†] Every number in this table is in the committed receipt `e5_axis_probe-20261009T191307.json`, except the
paragraph-length correlation. That value is `null` in the receipt (the caption payload was absent when it ran), so
we computed it in a separate pass. Treat that row as not receipt-backed here. It is a minor supporting detail and
decides no claim.

The opposite signs in the CKA-after-projection row are what this lemma predicts:

**Lemma A1 (nuisance-axis dilution of CKA, exact in population).** Let X = R + S be zero-mean, with S (a component
independent of the image, such as the non-visual axis) independent of (R, Y). Then

```
CKA(X, Y) = CKA(R, Y) · ||Σ_R||_F / ||Σ_R + Σ_S||_F  ≤  CKA(R, Y) / sqrt(1 + ρ²),   ρ = ||Σ_S||_F / ||Σ_R||_F,
```

with equality if and only if Σ_R Σ_S = 0.

*Proof.* Independence gives Cov(X, Y) = Cov(R, Y) and Cov(X) = Σ_R + Σ_S. Then
||Σ_R + Σ_S||_F² = ||Σ_R||² + ||Σ_S||² + 2 tr(Σ_R Σ_S), and tr(Σ_R Σ_S) ≥ 0 for positive semidefinite matrices. ∎

So removing a pure image-independent axis raises CKA, and removing an axis the image shares lowers it. Qwen3-gen's
top axis behaves like the first case: removing it raises linear CKA by 35%. The other two encoders' top axes are the
image's own top axis, so they behave like the second. The implied nuisance ratio for gen is ρ ≈ 0.9, from
0.583 / 0.433 = 1.35 ≈ sqrt(1 + ρ²).

### 3.2 Removing it fixes their aligner (measured, E5)

On SPC, projecting out the one axis moves gen from near chance to good retrieval. The same step ruins the
other two encoders.

**Protocol.** We use their `WassersteinProcrustes` with default settings. Training uses SPC minus the last 2,000
items, as their two disjoint unpaired halves. FOSCTTM is computed on those 2,000. The axis is the top principal
component of the unpaired language training rows, projected out of every language row. Runs were on our GPU host
(Beast), seeds 0–2. Receipts: `results/e5_scaffold_axis/e5_gates-*.json`,
`e5_scaffold_axis-raw-drop1-*-seed{1,2}-*.json`.

| SPC holdout FOSCTTM | Qwen3-8B gen | Qwen3-Embedding-8B | MPNet |
|---|---:|---:|---:|
| their pipeline (nothing removed) | 0.415 ± 0.055 (0.419 / 0.358 / 0.467) | 0.019 (0.021 / 0.013 / 0.023) | 0.026 (0.030 / 0.034 / 0.014) |
| top language PC projected out | **0.038 ± 0.006** (0.033 / 0.044 / 0.037) | 0.364 (seed 0) | 0.325 (seed 0) |

For Qwen3-gen the change is −0.377, about 7 seed SDs of the raw arm. FOSCTTM goes from near chance to about 4% of
keys outranking the partner.

This is not a blanket rule. The same projection takes the two good encoders from about 0.02–0.03 to 0.33–0.36. That
change is far beyond any seed noise we observed, so we did not re-seed it.

*Mechanism (inferred from the sign pattern and §3.1).* Their aligner locks onto each space's dominant axis. For MPNet
and Qwen3-Embedding that axis is the image's own top axis (|corr| 0.89–0.90), so it carries the alignment. For
Qwen3-gen it is non-visual (|corr| 0.006). The image's top axis is then matched to the non-visual axis, and the
alignment collapses.

### 3.3 Finding the axis without pairs (measured)

A detector that scores separate fits finds the axis with no pairs. A detector that removes an axis inside one fit does not.

**A first detector failed.** It took Hungarian pseudo-pairs from the raw fit. It then dropped any of the top-10
language PCs that the mapped image side could not predict (ridge R² < 0.3). For Qwen3-gen it dropped PC 8, not PC 0,
and FOSCTTM worsened from 0.407 to 0.484 (laptop, seed 0). For the two controls it correctly dropped nothing.

The cause (inferred) is that the test is circular. On its pseudo-pairs the image side "predicts" the non-visual PC
with R² 0.855, against 0.16 on true pairs. The pseudo-pairs come from a fit that had already rotated the image's top
axis onto the non-visual axis, so the test certifies whatever the broken fit matched.

**A detector that works.** Instead of removing an axis inside a single fit, we give each candidate removal its own
fresh fit and choose between the fits with a pairs-free score. We call this **selection over fits**. A *removal
setting* (called a "gate" in our scripts) projects one language PC out of the language rows before fitting, or
removes nothing. The steps are:
1. Fit once per setting: nothing removed, or one of language PCs 0–4 removed, with the PCs estimated on unpaired
   rows.
2. Score each fit on its own training rows, with no true pair:
   - **S1** is the mean cosine of Hungarian-matched pairs. It measures how well one rotation makes the two clouds
     coincide as sets.
   - **S2** is linear CKA over the matched pairs.
3. Keep the setting with the highest S1.

Script `experiments/e5_scaffold_axis/gates.py`. Predictions G1–G3 were frozen in its header before any score
existed. Seed 0 results:

| removal setting | Qwen3-8B gen S1 | FOSCTTM | Qwen3-Emb-8B S1 | FOSCTTM | MPNet S1 | FOSCTTM |
|---|---:|---:|---:|---:|---:|---:|
| none removed | 0.473 | 0.419 | **0.516** | **0.021** | **0.524** | **0.030** |
| PC0 removed | **0.517** | **0.033** | 0.439 | 0.364 | 0.483 | 0.325 |
| PC1 removed | 0.464 | 0.460 | 0.469 | 0.337 | 0.489 | 0.297 |
| PC2 removed | 0.470 | 0.377 | 0.476 | 0.168 | 0.500 | 0.118 |
| PC3 removed | 0.469 | 0.293 | 0.476 | 0.100 | 0.519 | 0.043 |
| PC4 removed | 0.469 | 0.459 | 0.498 | 0.032 | 0.492 | 0.096 |

Seeds 1–2, re-running each encoder's two highest-S1 settings:

| encoder | S1 choice | S1 margin over runner-up (seeds 0 / 1 / 2) | FOSCTTM, chosen vs runner-up |
|---|---|---|---|
| Qwen3-8B gen | PC0 removed | 0.044 / 0.030 / 0.041 | 0.033–0.044 vs 0.358–0.467 |
| Qwen3-Embedding-8B | none removed | 0.017 / 0.023 / 0.013 | 0.013–0.023 vs 0.032–0.050 |
| MPNet | none removed | 0.005 / 0.023 / 0.021 | 0.014–0.034 vs 0.030–0.063 |

G1, the prediction that could have falsified the detector, holds. S1 removes PC0 for Qwen3-gen and nothing for the
controls, in 9 of 9 encoder × seed cases. G2 holds. Every S1 choice is also the best true-pair FOSCTTM among the
settings compared: all six at seed 0, the top two at seeds 1–2. G3 is mixed. S2 agrees except for MPNet at seed 0,
where it picks PC3 removed (FOSCTTM 0.043 vs 0.030).

S1 also ranks all six settings well. The rank correlation of S1 with −FOSCTTM is 0.94, 0.94 and 0.77
(Qwen3-Embedding, MPNet, Qwen3-gen). For S2 it is 0.83, 0.89 and 0.26.

Two earlier frozen predictions came from the E5 script. P5a, that dropping the top PC lowers FOSCTTM for gen and
raises it for the others, holds. P5b and P5c, that the pseudo-pair detector finds gen's axis and never hurts, are
false (see the first detector above).

### 3.4 Not a precision artifact (measured)

The axis is a property of the representation, not of numeric storage.

The Qwen3-8B-gen file is stored in fp32, although their loader docstring says bf16. Its rows share a large common
direction: ‖mean of unit rows‖ ≈ 0.93, against 0.38–0.66 for the other files. Centering removes it in fp32 and
leaves about 20 of 24 mantissa bits in the residual. The bf16 files are far from swamping. Their per-coordinate
|mean| / σ is 6–13, against the 835–2,371 at which, in our own work, rounding swamped a centered residual.

### 3.5 What it means for their predictors

Clipped CKA misses the SPC deficit, but their main predictor does not. Their main-text alignability predictor is
already linear CKA (R² 0.73 against FOSCTTM, Sec. 4.3), and it rates gen low. Their App. D analysis uses the clipped
CKA of Wang et al. On SPC it gives 0.61–0.66 for all three encoders and puts gen level with mean pooling (+0.014). It
does turn negative on the two densest corpora (−0.144 DOCCI, −0.067 DCI). Linear CKA separates gen (0.433) from the
others (0.63–0.66) on SPC, and projecting out the one axis raises it to 0.583. Inferred: clipping bounds the dominant
axis's large coordinates, so App. D's clipped-CKA comparison understates gen's SPC deficit. This is a note on App. D,
not on their predictor.

CKA predicts the difficulty of the search, not the existence of a rotation. Gen's low linear CKA (0.21–0.43 on the
long-caption corpora) correctly predicts that their unpaired aligner fails there. Yet the true-pair oracle (§3.6)
finds a single rotation that aligns it (0.007–0.014). Low CKA is evidence that unpaired search will struggle, not that
the shared geometry is missing.

Local geometry agrees. Mutual 10-NN is 0.216 for gen against 0.33–0.35. This suggests the axis reorganizes
neighborhoods, which Hungarian matching depends on.

### 3.6 Generality across corpora: the axis reproduces, the single-axis fix does not (measured, E6)

The axis and the detector reproduce on three long-caption corpora. Removing the one axis rescues the alignment only
on SPC.

§3.1–§3.3 used one corpus (SPC). Schnaus et al. validate SPC-trained maps on COCO-val. They report Qwen3 generative
pooling near chance on two further long-caption corpora, DenselyCaptionedImages (DCI) and DOCCI. We ran the same
probe and the same unpaired detector on their stored DCI, DOCCI and COCO-val embeddings. We used their load path and
their aligner at commit `fdfad84`, and changed only the corpus. Receipts are under `results/e6_generality/`; the
pre-registration is `experiments/e6_generality/PREREG.md`.

**The axis is present, and it is a long-caption effect (axis probe, first 4,096 rows).**

| Qwen3-8B gen | SPC | DCI | DOCCI | COCO-val |
|---|---:|---:|---:|---:|
| top language PC: share of variance | 13.8% | 19.4% | 22.2% | 12.3% |
| held-out R² of top PC from the image | 0.16 | **0.052** | **0.052** | **0.899** |
| linear CKA (gen vs image) | 0.433 | 0.253 | 0.213 | 0.670 |
| linear CKA after projecting out the top PC | 0.583 ↑ | 0.462 ↑ | 0.449 ↑ | 0.513 ↓ |
| mutual 10-NN with the image | 0.216 | 0.132 | 0.115 | 0.368 |

On DCI and DOCCI the top gen axis is non-visual (image R² 0.05) and dominant (19–22% of variance). Projecting it out
raises linear CKA, which is the Lemma A1 behavior seen on SPC, more pronounced. The control encoders keep the
opposite sign on both corpora: their top PC has R² 0.77–0.87, and projecting it out lowers CKA.

On COCO-val the axis is absent. COCO-val has short captions, and it is the one setting where Schnaus et al. do not
report the gen failure. Gen's top PC is image-predictable (R² 0.899), and gen's linear CKA (0.670) matches the
control encoders. Projecting the top PC out *lowers* CKA (0.670 → 0.513, as for a good encoder), and mutual 10-NN is
0.368, not 0.12. The non-visual axis is therefore a property of generative pooling on long, detailed captions, not of
generative pooling as such. Receipts: `e6_axis_probe-{DenselyCaptionedImages,DOCCIDataset,coco_val2014}-*.json`.

**Removing that one axis does not rescue the alignment off SPC.** The table gives holdout FOSCTTM under their
aligner, on the last 2,000 rows:

| holdout FOSCTTM | SPC | DCI | DOCCI |
|---|---|---|---|
| gen, none removed | 0.415 ± 0.055 | 0.479 ± 0.066 (0.542 / 0.484 / 0.411) | 0.474 ± 0.044 (0.515 / 0.428 / 0.480) |
| gen, top PC removed | **0.038 ± 0.006** | **0.391 ± 0.069 (0.413 / 0.314 / 0.447)** | **0.478 ± 0.012 (0.465 / 0.482 / 0.488)** |
| Qwen3-Embedding, none removed / removed | 0.019 / 0.364 | 0.093 / 0.322 | 0.096 / 0.485 |
| MPNet, none removed / removed | 0.026 / 0.325 | 0.400 / 0.325 | 0.121 / 0.473 |

On SPC the removal is a rescue: 0.415 → 0.038, near-perfect retrieval. On DCI and DOCCI it does not rescue gen. On
DCI it lowers FOSCTTM only from 0.479 to 0.391 (three seeds), and on DOCCI it does essentially nothing, 0.474 →
0.478. Either way gen stays near chance (0.39–0.48), nowhere near the 0.09–0.12 the best control encoder reaches on
the same corpus.

**Why the fix fails off SPC: the geometry is alignable, the unpaired search is not (oracle, E6b).** Two explanations
are possible. The off-SPC failure could be a geometry problem, with no single rotation able to align gen to the
image. Or it could be a search problem, where a rotation exists but their unpaired solver does not find it. An oracle
separates them. We give the solver the *true* pairs, fit the best map it can on the same training rows, and measure
the same holdout FOSCTTM. With the true pairs a single orthogonal map aligns Qwen3-gen near-perfectly on all three
corpora, with or without the axis removed:

| oracle holdout FOSCTTM (true pairs) | SPC | DCI | DOCCI |
|---|---|---|---|
| gen, none removed, orthogonal map | 0.009 | 0.014 | 0.010 |
| gen, top PC removed, orthogonal map | 0.007 | 0.010 | 0.007 |
| gen, top PC removed, unconstrained linear map | 0.010 | 0.018 | 0.010 |
| Qwen3-Embedding, none removed, orthogonal map | 0.002 | 0.003 | 0.001 |

Receipt `e6b_oracle-*.json`. A single rotation *can* align gen to the image on DCI and DOCCI. The oracle with PC0
removed reaches 0.007–0.010, essentially the control-encoder ceiling (0.001–0.003) and far below the 0.391/0.478 that
their unpaired solver reaches. The geometry is rotation-alignable, and what fails off SPC is the unpaired *search*.

Two further facts sharpen this. First, even gen *without* the axis removed is rotation-alignable with true pairs
(0.009–0.014). The non-visual axis therefore does not break the geometry, even on SPC. It corrupts the pseudo-pairing
that the unpaired solver bootstraps from, so removing it is a *search aid*, not a geometry repair. Second, an
unconstrained linear map does no better than the rotation (0.010–0.018), so the orthogonality constraint is not the
obstacle either. The shared linear structure is there, and the unpaired solver does not reach it.

**More unpaired restarts do not recover it.** We re-ran their aligner on gen with the top PC removed over eight
restarts (seeds 0–7) and selected one per corpus by the pairs-free S1 alone. This leaves gen near chance (DCI 0.396,
DOCCI 0.502). Even the best of the eight restarts (0.280 / 0.341) is nowhere near the 0.007–0.010 that the oracle
shows is reachable. The bottleneck is the unpaired correspondence bootstrap, not the number of restarts.

**No other single axis helps.** Removing each of the next language PCs individually leaves gen near chance
(DCI PC1–PC4 0.492 / 0.511 / 0.437 / 0.455; DOCCI 0.443 / 0.552 / 0.408 / 0.570). The axis probe predicts this. PCs
1–3 are visual directions (held-out image R² 0.47–0.61), so removing them discards shared signal rather than a
nuisance axis.

**SPC→COCO transfer (their headline validation).** We fit a map on SPC gen and evaluated it on held-out COCO-val gen,
the setting Schnaus et al. validate in. It reaches holdout FOSCTTM 0.409 raw and 0.022 with the SPC top PC removed
from both sides (5000 COCO-val rows the map never saw). The SPC-fit map, axis removed, therefore transfers to COCO.
This is the same diagnosis read forward: the removal rescues the *fitting*, and here the fitting is done on SPC.

Seed counts: Qwen3-gen runs at three seeds on DCI and DOCCI, plus five more restarts each for the search test. The
control encoders run at seed 0. The oracle ceilings, the PC1–PC4 ladder and the SPC→COCO transfer are measured.

**The unpaired detector still identifies the right axis.** Its S1 (mean cosine of Hungarian-matched pairs, no true
pairs) still prefers removing the top PC for gen and keeping it for the well-aligned control encoders. On DOCCI it
chooses correctly in 3 of 3 (PC0 for gen, nothing removed for Qwen3-Embedding and MPNet). On DCI it chooses PC0 for
gen, nothing for Qwen3-Embedding, and PC0 for MPNet. MPNet is itself poorly aligned on DCI (0.400) and is also helped
by the removal (0.325), so the detector is self-consistent (it picks the setting that helps) rather than wrong.

The S1 margins on the new corpora are thin. On gen, S1(PC0) beats S1(none) by only 0.001–0.006 (DCI: none removed
0.485, PC0 removed 0.491; DOCCI: 0.436 and 0.437), against a clear 0.043 on SPC. This is consistent with the removal
being only weakly useful there. The detector transfers as a flag, but what it selects is not a cure off SPC.

**What this means for the response.** The *diagnostic* is a dominant non-visual axis in Qwen3 generative pooling of
long captions, read by linear-minus-clipped CKA and by the held-out image-predictability of the top PC, and found
without pairs. It is now measured on three corpora and shown absent on short captions. That part generalises and is
strengthened. The *fix* ("project out the top PC and the alignment is restored") is specific to SPC, and we scope it
to SPC below.

The oracle explains why. Off SPC, the geometry with PC0 removed is still a single rotation away from the image
(true-pair FOSCTTM 0.007–0.010). The deficit their aligner leaves is therefore a failure of the unpaired search, not
of the geometry, and removing the one axis is a search aid that is enough on SPC but not off it. We still recommend
the detector to the authors, because it flags the deficit before fitting. We do not claim a one-line repair.

---

## 4. Retrieval is not fidelity: the rotation ceiling

### 4.1 Why retrieval can be near-perfect while fidelity is low

Retrieval is a margin property that improves with dimension. Fidelity does not. We state this as a proposition.

**Proposition D1.** Let the keys ŷ_j and the mapped query q_i be unit vectors, with α_i = ⟨q_i, ŷ_i⟩ and
q_i = α_i ŷ_i + β_i u_i, where β_i = sqrt(1 − α_i²) and u_i ⟂ ŷ_i.
- **Exact condition.** Distractor j outranks the partner exactly when β_i ⟨u_i, ŷ_j⟩ > α_i (1 − c_ij), where
  c_ij = ⟨ŷ_i, ŷ_j⟩.
- **Approximation.** If u_i is uniform on a sphere of effective dimension d_eff orthogonal to ŷ_i, then

```
P(j outranks i) ≈ Φ̄( (α_i/β_i) · sqrt((d_eff − 1)(1 − c_ij)/(1 + c_ij)) ),
```

  which goes to 0 for any fixed α_i > 0 as d_eff grows. For example, with d_eff = 100 and c = 0.1, α = 0.3 gives
  P ≈ 0.003.

A generator conditioned on q_i receives only α_i of the true signal. Our FLUX.2 consumer measured three zones of
direction fidelity. At ≥ 0.895 it rendered the target in 8 of 8 cells. At ≤ 0.50 it failed. At 0.71–0.78 the result
depended on target and seed. Those zones belong to FLUX and serve here only as a reference scale.

### 4.2 Measured (E1, COCO val2014, DINOv2-B ↔ MPNet, their protocol)

Receipts: `results/e1_fidelity_gap/e1_fidelity_gap-20261009T200203.json` (seed 0, laptop) and
`e1_fidelity_gap-seed{1,2}-*.json` (Beast). The oracles are closed-form fits on 20,000 true pairs.

| map | FOSCTTM | median α | α 5th–95th pct | α ≥ 0.895 | α ≤ 0.50 |
|---|---:|---:|---|---:|---:|
| **their method, zero pairs** (seeds 0 / 1 / 2) | **0.0073** / 0.0259 / 0.0149 | **0.527** / 0.474 / 0.495 | 0.260–0.757 (seed 0) | **0.0%** (seed 0) | **43.3%** (seed 0) |
| their method, 10 known pairs (seed 0) | 0.0125 | 0.473 | 0.205–0.725 | 0.0% | 56.3% |
| their method, 100 known pairs (seed 0) | 0.0056 | 0.507 | 0.267–0.731 | 0.0% | 48.3% |
| best rotation (orthogonal oracle) | 0.0027 | 0.572 | 0.344–0.766 | 0.0% | 30.1% |
| best linear map (least-squares oracle) | **0.0026** | **0.781** | 0.547–0.901 | 6.5% | 2.8% |

Across seeds 0–2 the oracle rows agree within 0.001 (FOSCTTM 0.0026–0.0027; median α 0.571–0.572 and 0.781).

![Figure 2](figures/fig2-fidelity-gap.png)

*Figure 2. Per-pair fidelity on 40,504 COCO validation pairs (seed 0). Shaded bands are the FLUX consumer's zones,
measured on a different consumer and space, shown for scale only.*

**Claim D: supported.** Retrieval is near-perfect: only 0.73% of keys outrank the true partner (seed 0). Fidelity is
well below that. The median cosine to the partner is 0.53, and α² ≈ 0.28, so about 72% of a mapped vector's energy
is not along its partner. The two oracles retrieve identically (0.0027 vs 0.0026) but differ by 0.21 in median
fidelity (0.572 vs 0.781). FOSCTTM cannot tell them apart.

### 4.3 Where the fidelity goes (measured)

The rotation constraint costs three times as much fidelity as the unpaired estimate.

| gap (median α) | from → to | size |
|---|---|---:|
| unpaired estimation | their zero-pair map → best rotation | **0.073 ± 0.026** (0.045 / 0.097 / 0.077 over seeds 0–2) |
| the rotation constraint | best rotation → best linear map | **0.210** |
| linearity and the rest | best linear map → 1 | 0.219 |

Their estimate is close to the best rotation. With zero pairs it is within 0.07 ± 0.03 of a rotation fitted on
20,000 true pairs. The ceiling is the rotation itself: no single rotation puts any validation pair in FLUX's ≥ 0.895
zone, and relaxing orthogonality is worth three times the remaining estimation gap.

Few pairs cannot fix this. While the map stays a rotation, pairs can only close the ~0.07 estimation gap. With 10 or
100 pairs, fidelity was 0.473 and 0.507 (seed 0 each).

*Consequence (inferred).* For a consumer that needs per-item fidelity, the lever is the map class, not better
unpaired estimation. Candidates are a non-orthogonal correction fitted on a few anchors, or per-concept anchors as in
our symbol work (one anchor per symbol lifted bridge fidelity to 0.93–0.99).

### 4.4 Checking Proposition D1 (measured, E1b)

Receipt `results/e1_fidelity_gap/e1_d1_check-20261009T211416.json`. Oracle maps were fitted on p true pairs, and
FOSCTTM was predicted from each map's median α and the residual's effective dimension (participation ratio) on
2,000 validation queries.

| map, p | median α | d_eff | predicted FOSCTTM | measured FOSCTTM |
|---|---:|---:|---:|---:|
| rotation, 20 | 0.109 | 85 | 0.189 | 0.138 |
| linear, 20 | 0.286 | 11 | 0.185 | 0.108 |
| rotation, 200 | 0.399 | 146 | 0.0047 | 0.0122 |
| rotation, 2,000 | 0.533 | 180 | 0.0002 | 0.0037 |
| rotation, 20,000 | 0.572 | 183 | 0.0001 | 0.0027 |
| linear, 20,000 | 0.781 | 69 | ≈ 0 | 0.0026 |

The formula's magnitude is wrong where retrieval is good. Below FOSCTTM ≈ 0.02 it underpredicts by 3–30×. The
probable cause (inferred) is that it treats the residual as isotropic and ignores near-duplicate keys, which dominate
the tail of the ranking. We use D1 only qualitatively.

Its direction is right. Retrieval depends on α/β and d_eff together. The linear map has much higher fidelity, but its
residual lies in fewer directions (d_eff 69 vs 183), so it retrieves no better than the rotation.

---

## 5. Pair baselines: a span ceiling, and which pairs to label

Their pair-based baselines have a provable fidelity ceiling. Choosing the pairs helps those baselines but not their method.

**Notation.** ŷ is a centered, unit-normalized key. X̂_p and Ŷ_p are the p known pairs, V_p = rowspan(Ŷ_p), and P
is the projector onto V_p. λ_1 ≥ λ_2 ≥ … are the eigenvalues of Σ̂ = E[ŷŷᵀ], so Σλ = 1.

**Lemma C1 (span confinement, exact).** Their `linear` baseline is W = X̂_p⁺ Ŷ_p. Then x̂W = (x̂ X̂_p⁺) Ŷ_p ∈ V_p, so
sim(x, y) = ⟨x̂W, Pŷ⟩: keys are ranked using only their p-dimensional projection Pŷ. ASIF compares keys through
ŷŶ_pᵀ, which is also a function of Pŷ.

**Lemma C2 (fidelity ceiling).** For any map whose image lies in V_p,

```
E_i α_i ≤ E_i ||P ŷ_i|| ≤ sqrt(E_i ||P ŷ_i||²) = sqrt(tr(P Σ̂)) ≤ sqrt(Σ_{k≤p} λ_k).
```

*Proof.* Cauchy–Schwarz gives α_i ≤ ||Pŷ_i||; then Jensen; then Ky Fan's maximum principle. ∎

**Remarks.**
1. Their `orthogonal` baseline is informed by the data only on V_p. On the complement it is an arbitrary isometry
   from the SVD's completion, so the ceiling applies to it only heuristically.
2. Their own method with pairs is not span-confined, because the unpaired Procrustes term informs every direction.

**Measured (E2, COCO val, MPNet, one draw per p, random pairs as in their protocol).** Receipt
`results/e2_span_bound/e2_span_bound-20261009T222209.json`; the full ladder (p = 1 … 1,000, random and medoid) is in
the receipt.

| p | captured energy | Ky Fan max | ceiling sqrt(energy) | linear α | linear FOSCTTM | orthogonal α | orthogonal FOSCTTM | theirs α | theirs FOSCTTM |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.016 | 0.080 | 0.127 | 0.038 | 0.422 | 0.007 | 0.462 | | |
| 5 | 0.085 | 0.266 | 0.291 | 0.144 | 0.228 | 0.035 | 0.333 | **0.498** | **0.0090** |
| 20 | 0.328 | 0.548 | 0.572 | 0.328 | 0.109 | 0.153 | 0.139 | **0.494** | **0.0075** |
| 50 | 0.572 | 0.768 | 0.756 | 0.444 | 0.048 | 0.262 | 0.052 | | |
| 200 | 0.889 | 0.962 | 0.943 | 0.515 | 0.016 | 0.405 | 0.013 | | |
| 1,000 | 1.000 | 1.000 | 1.000 | 0.426 | 0.018 | 0.506 | 0.005 | | |

The bound holds in all 20 rows, as it must, but it is loose. At p = 20 the linear baseline reaches 0.328 against a
ceiling of 0.572. Their own method exceeds the ceiling at p = 5 (0.498 vs 0.291) but not at p = 20 (0.494 vs 0.572).
The more useful comparison is retrieval: with 5 pairs their method retrieves better than both baselines do at p = 200
(0.009 vs 0.013–0.016).

Least squares overfits near p ≈ d. Linear α falls from 0.515 (p = 200) to 0.426 (p = 1,000; span rank 766 of 768).
This is the interpolation regime of the pseudo-inverse.

Choosing pairs (Claim E) helps only the baselines. Vision-side k-means medoids capture more energy than random pairs
at every p ≤ 200 (0.085 → 0.128 at p = 5) and lower linear FOSCTTM at all of those p (0.228 → 0.161 at p = 5). For
their method, medoids gave 0.025 vs 0.009 at p = 5 and 0.0067 vs 0.0075 at p = 20. Pair selection is therefore not a
contribution to their method, and we did not spend seeds on it.

---

## 6. What did not work

### 6.1 Claim A: the thinking preamble does not dilute CKA (refuted, E3)

Token-centering lowers CKA, so the preamble is not an image-independent nuisance.

**What we tested.** Their generative pooling wraps each caption as "Imagine what it would look like to see:
{caption}" in Qwen3's chat template with thinking on. It decodes 128 greedy tokens and averages the final-layer
states that produce them. We predicted that the shared `<think>` preamble is an image-independent nuisance in
Lemma A1's sense, and that centering it away would raise CKA.

**Setup.**
- **Model and data.** Qwen3-1.7B in bf16 (the model of their Fig. 21 ladder), on the first 2,048 items of COCO
  train2014 (caption 0) and SPC, in their row order.
- **Row-order check.** Our MPNet embeddings match their stored rows: SPC cosine 1.000; COCO caption 0 retrieves
  its own row 95.7% of the time.
- **Metric.** Their clipped CKA against their stored DINOv2-B rows, per 1,024-item slice.
- **Replication.** Our pooling scores 0.591 on SPC against 0.607 for their stored 8B file.
- **Receipts and preregistration.** `results/e3_pooling_scaffold/job-9426423166f5/` and `job-5fd45e7c7f0d/`;
  `experiments/e3_pooling_scaffold/PREREG.md`.

| arm (final layer, clipped CKA) | COCO | SPC |
|---|---:|---:|
| their generative pooling (thinking on) | **0.623** | **0.591** |
| + token-centered | 0.602 | 0.573 |
| + leave-own-out frequent-token centering (post-hoc arm) | 0.609 | 0.581 |
| + position-centered (control) | 0.616 | 0.583 |
| thinking off | 0.587 | 0.548 |
| thinking off + token-centered | 0.591 | 0.571 |
| thinking off + leave-own-out centering | 0.595 | 0.575 |
| their mean pooling (all chat tokens) | 0.505 | 0.583 |
| mean pooling, caption tokens only | 0.506 | 0.596 |
| their stored MPNet (reference) | 0.687 | 0.633 |

| prediction | frozen bar | measured effect (COCO / SPC, paired per slice) | reading |
|---|---|---|---|
| A1: the first 12 generated tokens are shared by ≥ 90% of captions | true | 96–100% for each of the first 16 | preamble present |
| A2: token-centering beats theirs | false (0/4 cells) | −0.021 / −0.019 | opposite sign |
| A2′ *(post-hoc)*: leave-own-out centering beats theirs | false (0/4) | −0.015 / −0.010 | opposite sign |
| A3: best nuisance-removed arm gains ≥ 0.02 on SPC | false | −0.004 | no gain under any margin |
| A4: caption-token mean pooling ≥ all-token | true | +0.002 / +0.013 | SPC supported; COCO a tie |

The claim is refuted on the sign, not on a margin. Both slices agree in every cell, and every thinking-on centering
arm moves CKA the wrong way.

The reason is that the preamble is shared but not independent of content. With thinking on, the model restates the
caption inside its reasoning ("…what it would look like to see a close-up of bins of food that include broccoli and
bread"), so centering removes signal. Lemma A1's sign does appear with thinking off: centering helps in every cell
(+0.004 to +0.027), because there the removed tokens are not a restatement. Thinking off still ends below thinking
on.

### 6.2 Claim B: a late layer helps only a little (supported, small, E3)

The table gives clipped CKA by depth.

| clipped CKA by depth (layer / 28) | 0.50 | 0.61 | 0.71 | 0.79 | 0.89 | 1.00 |
|---|---:|---:|---:|---:|---:|---:|
| COCO, their mean pooling | 0.328 | 0.341 | 0.332 | 0.468 | **0.516** | 0.505 |
| SPC, their mean pooling | 0.298 | 0.294 | 0.299 | 0.533 | **0.590** | 0.583 |
| COCO, caption-token mean pooling | 0.330 | 0.347 | 0.339 | 0.473 | **0.519** | 0.506 |
| SPC, caption-token mean pooling | 0.325 | 0.312 | 0.304 | 0.537 | 0.594 | **0.596** |
| COCO, generation, thinking off | 0.419 | 0.365 | 0.374 | 0.594 | **0.602** | 0.587 |
| SPC, generation, thinking off | 0.328 | 0.260 | 0.277 | 0.545 | **0.557** | 0.548 |
| COCO, generation, thinking on (theirs) | 0.412 | 0.358 | 0.367 | 0.589 | 0.621 | **0.623** |
| SPC, generation, thinking on (theirs) | 0.300 | 0.238 | 0.255 | 0.519 | 0.564 | **0.591** |

The direction is supported. Depth 0.89 beats the final layer in 5 of 6 no-thinking cells, by +0.007 to +0.015, with
both slices agreeing. That includes their own mean pooling on both corpora. The frozen bars B1 and B2 failed on the
sixth cell, where 1.0 beats 0.89 by 0.002.

With thinking on, the final layer is best (−0.002 / −0.027). For their best generative embedding, choosing a layer
gives nothing.

The size is small, and the effect on FOSCTTM is untested. CKA jumps between depth 0.71 and 0.79 in every arm (+0.13
to +0.27) and then plateaus, consistent with content formed late.

---

## 7. A consumer-grounded benchmark (designed, not built)

The design is in `experiments/e4_consumer_closure/DESIGN.md`. It has four steps:
1. Build a 200-symbol displacement bank (SmolLM2 ↔ Klein-Qwen).
2. Fit their unpaired aligner and record per-symbol α.
3. Render about 24 symbols spread over α through the frozen FLUX.2 Klein 4B, with a native ceiling, a shuffled sham
   and an exact no-op.
4. Predict that render progress rises with α. Report how much variance retrieval rank adds once α is known, with
   a bootstrap interval.

The result would be an acceptance test for unpaired maps with causal ground truth. **[PENDING E4: not built.]**

---

## 8. Recommendations

| change | evidence | expected effect | status |
|---|---|---|---|
| Run the pairs-free detector before fitting, as a diagnostic | §3.3, §3.6 | flags the non-visual axis in Qwen3 generative pooling of long captions, with no pairs, on SPC, DCI and DOCCI; absent on short COCO captions | detector measured on SPC (9/9) and DCI/DOCCI (E6) |
| Treat the one-axis removal as an SPC-specific repair, not a general fix | §3.6 | restores alignment on SPC (0.415 → 0.038; the SPC-fit map transfers to COCO-val, 0.409 → 0.022) but leaves gen near chance on DCI (0.479 → 0.391) and DOCCI (0.474 → 0.478, no change) | measured, E6 and E6b (gen 3 seeds each, plus 8 restarts) |
| Do not read Qwen3-gen's near-chance score as an incompatible geometry | §3.6 (E6b) | a single rotation fitted on true pairs aligns it on SPC, DCI and DOCCI (0.007–0.014); a better-initialized unpaired search is the open lever | oracle measured; better initialization untested |
| In App. D, report linear CKA next to clipped CKA | §3.5, §3.6 | shows the SPC deficit that clipped CKA misses, and that it sits on one axis | measured on SPC, DCI, DOCCI, COCO |
| Report per-pair α next to FOSCTTM | §4.2 | separates maps that retrieval ranks as equal | measured (E1) |
| For text-to-image use, relax the rotation (for example a non-orthogonal correction on a few anchors) | §4.3 | higher per-item fidelity than any rotation | ceiling measured; correction untested |
| Read mean pooling at depth ≈ 0.9 | §6.2 | +0.007–0.015 clipped CKA | measured on CKA only |
| ~~Choose pairs as vision-side medoids~~ | §5 | helps only baselines | not a contribution |
| ~~Token-center the thinking preamble~~ | §6.1 | lowers CKA | refuted |

---

## 9. Methods and integrity

**Their code, unchanged.** Splits, preprocessing, the aligner and FOSCTTM come from their library at commit
`fdfad84`, so any difference from their numbers comes from the arm we change.

**What we checked and do not claim.** Their pipeline already centers and unit-normalizes both spaces. Their QAP
solver (MPOpt) reaches the optimum on our problem. Their runs are bit-reproducible. Two suggestions we first
considered, "center the embeddings" and "use a better solver", were dropped before any run.

**Preregistration.** E3's predictions and both amendments are in `e3_pooling_scaffold/PREREG.md`. The predictions
for E5 and for the removal-setting detector are in their script headers. Post-hoc arms are labelled.

**How claims are judged (adopted 2026-10-09, before any E2, removal-setting or seed result).** We read a claim from
its effect against its noise, and a frozen bar decides only its own prediction. We adopted this because self-set
round-number bars had decided claims in both directions. A "median α < 0.5" bar would have marked Claim D false at
0.527 but true at 0.473, on the same evidence. An "every cell" rule refuted Claim B on a 0.002 tie. A ≥ rule passed
A4 on a +0.0006 margin. We retired those bars, plus a rank-correlation bar that was confounded by p. We still report
every frozen outcome.

**Seeds.** We used three seeds (0–2) only for arms whose verdict noise could flip: the axis fix, the detector's two
closest settings, and their zero-pair map in E1. Effects far beyond noise, failed arms, and baselines their method
already beats were run once.

**Hosts.** Fits ran on a laptop (macOS, torch 2.14) and on a Linux GPU host (torch 2.13). They agree to 1e-6 on small
fits, but full-scale fits differ like seeds: Qwen3-gen at seed 0 gives raw 0.407 vs 0.419, and with the axis removed
0.036 vs 0.033. Every comparison above is made within one host.

## 10. Limits

- **The fix is SPC-specific (measured, E6).** The non-visual axis reproduces on DCI and DOCCI (and is absent on short
  COCO captions), and the unpaired detector still selects it (§3.6). But projecting the axis out rescues the
  alignment only on SPC. On DCI and DOCCI it leaves gen near chance (~0.39–0.48), not at the ~0.10 the control
  encoders reach. On those corpora the single-axis removal is not enough to make the unpaired solver converge, though
  a single rotation given the true pairs aligns gen as well as the control encoders (§3.6). Qwen3-gen is at three
  seeds on each corpus plus five further restarts for the search test, and the control encoders are at seed 0. The
  oracle ceilings, the PC1–PC4 ladder and the SPC→COCO transfer are measured.
- **Scope of the detector.** It searches the top five language PCs and was tested on three encoders. It would miss a
  non-visual axis outside the top five, or one on the vision side.
- **Model size in E3.** E3 used Qwen3-1.7B, not their 8B. The replication matches within 0.016 clipped CKA, but the
  token-level negative might not transfer to 8B.
- **Lemma A1 assumes independence.** The thinking preamble violates it, which is why A2 failed. The axis behaves as
  the lemma predicts, but we inferred the independence and did not show it.
- **Consumer zones.** The 0.895 and 0.50 zones come from FLUX.2 Klein 4B direction fidelity on few cells and a
  different space. They are a reference scale, not a claim about their RAE.
- **Small E0.** E0 uses 18 symbols with a thin margin (0.053 to the best single swap).

## 11. Reproduce

See `experiments/README.md`. Laptop runs use `uv run python -m <module>`. Fleet runs use
`experiments/seeds/submit.py --plan {core,gates,gates-seeds}`, then `--collect`. Figures come from
`experiments/figures/make_figures.py`, which reads only the receipts.

## References

1. Schnaus, Dagès, Cremers, Wang, Isola. Shared Geometry as a Rosetta Stone: Cross-Modal Alignment Without Paired
   Data. arXiv 2610.09411, 2026. (We read v2, 8 Oct 2026, and code commit `fdfad84`.)
2. Huh, Cheung, Wang, Isola. The Platonic Representation Hypothesis. ICML 2024.
3. Kornblith, Norouzi, Lee, Hinton. Similarity of Neural Network Representations Revisited. ICML 2019.
4. Hutschenreiter et al. Fusion Moves for Graph Matching. ICCV 2021 (MPOpt).
5. Ky Fan. On a theorem of Weyl concerning eigenvalues of linear transformations. PNAS 1949.
6. Schnaus, Araslanov, Cremers. It's a (Blind) Match! Towards Vision-Language Correspondence Without Parallel
   Data. CVPR 2025, pp. 24983–24992. arXiv 2503.24129. (Their unpaired QAP matcher; its supplement notes that
   mutual k-NN, CKA and the Gromov–Wasserstein distance are special cases of the same quadratic assignment.)
7. Mémoli. Gromov–Wasserstein Distances and the Metric Approach to Object Matching. Foundations of Computational
   Mathematics 11(4):417–487, 2011. (Isometry-invariant matching of metric measure spaces.)
8. Alvarez-Melis, Jaakkola. Gromov–Wasserstein Alignment of Word Embedding Spaces. EMNLP 2018, pp. 1881–1890.
   arXiv 1809.00013. (Unpaired cross-lingual alignment by matching intra-space similarities.)
9. Conneau, Lample, Ranzato, Denoyer, Jégou. Word Translation Without Parallel Data. ICLR 2018. arXiv 1710.04087.
   (MUSE: adversarial map, Procrustes refinement, and CSLS retrieval; a precedent for separating retrieval from
   the map's fidelity.)
10. Jha, Zhang, Shmatikov, Morris. Harnessing the Universal Geometry of Embeddings. arXiv 2505.12540, 2025.
    (vec2vec: translating text embeddings between spaces with no paired data, via a shared latent and a
    non-orthogonal decoder; the kind of relaxed map class §4.3 points to for fidelity.)
11. Oozeer, Nathawani, Prakash, Lan, Harrasse, Abdullah. Activation Space Interventions Can Be Transferred Between
    Large Language Models. arXiv 2503.04429, 2025. (Learned maps between model activation spaces transfer
    steering interventions.)
12. Our records: the FLUX encoder swap and symbol table (`obsidian/arcs/cross-conditioner-to-time-circuits.md`); the
    LM commit band (`research/papers/space-and-time-circuits/`); the learned per-axis gate ladder that the
    detector in §3.3 adapts (`research/shared/.../spectral-native` notes); rotation swamping
    (`research/papers/rounding-placement/`).

---

## Send checklist (not sent)

A record of how this would reach the authors; nothing here has been sent, posted, or emailed.

- **To whom.** Dominik Schnaus (first author, TU Munich / MCML), with Thomas Dagès, Daniel Cremers, Xi Wang and Phillip Isola.
- **What.** This response, plus the `experiments/e6_generality/` and `experiments/e5_scaffold_axis/` code and the JSON receipts it cites. It covers the non-visual axis and the pairs-free detector (measured on SPC, DCI and DOCCI, and shown absent on short COCO captions), the SPC-specific removal fix, the retrieval-vs-fidelity gap and rotation ceiling (§4), and the span ceiling (§5). Everything is built on their stored embeddings and their library at commit `fdfad84`.
- **Where.** A short note or email to the authors, or an issue on `github.com/dominik-schnaus/unpaired-rosetta` referencing their HF embeddings. The diagnostic (run the detector before fitting) is the part most directly useful to a revision.
- **When.** Before their next revision. The current arXiv version is v2 (8 October 2026); no v3 exists as of 2026-10-22 (we checked the arXiv version history). We did not re-diff the Appendix D clipped-CKA material that §3.5 addresses between v1 and v2, so it should be re-checked against whatever version they revise from.
- **Status.** Not sent. This agent did not contact anyone.
