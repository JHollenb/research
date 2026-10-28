# When a Rotation Exists but the Search Misses It

**Alignability, searchability, and pairs-free seed selection in unpaired cross-modal alignment**

*A note for the authors of "Shared Geometry as a Rosetta Stone" (Schnaus, Dagès, Cremers, Wang, Isola; arXiv 2610.09411 v2)*

Jacob Hollenbeck, independent researcher

Date: 2026-10-26

Status: draft 2 (readability and tone pass), merged from `response.md` (draft 3.2) and `followup.md` (draft 2.1). Not sent to anyone.

---

## Abstract

Schnaus et al. show that separately trained encoders can be aligned by a single rotation with no paired data. Our measurements support that result. This note gives you a way to tell, for a pair that scores poorly, whether the shared geometry is missing or the unpaired search failed. It also lists changes to your evaluation that follow from the answer.

We use two terms. A pair is alignable if a rotation fitted on the true pairs aligns it. It is searchable if your unpaired aligner finds that rotation on its own. We found pairs that are alignable and not searchable, and the search fails for two different reasons.

The first reason is a nuisance direction: a high-variance direction in one space that the other space cannot predict. We found one in Qwen3-8B generative embeddings of long captions. It misleads every run in the same way: on the long-caption corpora DCI and DOCCI your aligner scores near chance (FOSCTTM 0.479 and 0.474), while a rotation fitted on true pairs reaches 0.014 and 0.010. The second reason is seed variance. On single-cell pairs no direction misleads the search, and different seeds land in different places.

Each reason has a fix you could adopt. For seed variance, a score computed without true pairs (S1, the mean cosine of the aligner's own matched pairs) selects good seeds. This answers the limitation that "without supervision one cannot select the best-performing seed". On CITE-seq it selects a seed at FOSCTTM 0.089, against your reported average of 0.225 and a true-pair rotation at 0.073. For a nuisance direction, a better starting point recovers the alignment: starting your refinement from a map fitted on another corpus gives 0.078 on DCI and 0.051 on DOCCI. We also describe a diagnostic that tells the two failures apart. It is not a validated rule. Finally, CKA predicts how hard the search will be. It does not tell you whether a rotation exists.

---

## 1. What this note offers

This note shows what you could change in your evaluation and why each change helps. Your paper states two open problems. One is a fully unsupervised alignment prediction score. The other is seed selection: "we report average rather than best performance, since without supervision one cannot select the best-performing seed." Our results bear on both.

We start from your result and ask one question. When your unpaired score is poor, does a rotation exist anyway? We answer it with an oracle, a rotation fitted on true pairs (Section 3). For the pairs we tested, the answer is yes. The search is then the bottleneck, and we ask why it fails.

The search fails in two ways (Section 4). In long-caption text, one nuisance direction misleads every run. In single-cell data, runs differ by seed. The two need different fixes. We call a score or a test pairs-free when it is computed without any true pairs.

Seed variance has a pairs-free fix (Section 5). A selection score picks good seeds. It is a few lines around your aligner call. It does not help when every seed is misled by the same direction.

A nuisance direction needs a better starting point (Section 6). A map fitted on another corpus works, and so does a small number of true pairs.

CKA is the predictor in your main text (Section 7). We show what it does and does not tell you.

Section 8 turns these results into six concrete steps. Section 9 lists the limits of our evidence. Every number has a receipt in Appendix A. Our claim is narrow. Your result holds. Where it looks weaker, the search falls short and the geometry does not, and there are inexpensive ways to see that and to fix it.

## 2. Setup and terms

This section lists what we took from your work, what we changed, and the terms we use.

**Your code and data.** Every experiment uses your released embeddings and your library pinned at commit `fdfad84`. Splits, preprocessing, the Wasserstein-Procrustes aligner, the QAP initialization and FOSCTTM are yours. The one thing we change per experiment is stated in the text. Your aligner, as we read it, returns the last of its R=100 refinement iterates with no selection step. Each experiment began by matching your published numbers. Appendix A gives the reproduction checks.

**FOSCTTM.** This is the average fraction of candidates that outrank the true partner. 0 is perfect and 0.5 is chance. Holdout scores for vision-language pairs use the last 2,000 items. We write "gen" for Qwen3-8B generative pooling of long captions. SPC is Stanford Paragraph Captions, DCI is DenselyCaptionedImages, and PC is a principal component.

**Three instruments.**
- *Oracle.* Fit a Procrustes map on the true pairs of the training half, then score FOSCTTM on a disjoint held-out half. We also fit an unconstrained linear map on the same pairs. If the two agree, the map that exists is a rotation.
- *S1.* The mean cosine of the aligner's own Hungarian-matched pairs (its pseudo-pairs), computed on its training rows. It measures how well one rotation makes the two clouds coincide as sets. We also tracked S2, the linear CKA of the matched pairs. S2 did worse than S1 and we do not use it below.
- *Axis probe.* For each of the top PCs of one space, fit a ridge regression from the other space and report held-out R². A dominant PC with R² near zero is a candidate nuisance direction. We call such a PC a *non-visual axis* when the other space is the image.

**Restarts and seeds.** A restart is a new run of your aligner with a different seed. Seed counts are stated with each result and collected in Appendix C. The starting-point arms use three seeds. The negative controls (cumulative axis search, iterate selection) use one. In the vision-language tables, gen uses three seeds on each corpus. The control encoders, Qwen3-Embedding-8B and MPNet, are seed 0 unless a spread is shown. Single-cell selection results use twelve seeds.

**Labels.** *Measured* means a result with a JSON receipt. *Inferred* means a mechanism read from measurements and not tested directly. *Post hoc* means found after a frozen prediction. Predictions for the CITE-seq, PBMC, SNARE-seq and starting-point experiments were frozen before any scored run. The refinement of the diagnostic in Section 4.3 is post hoc. The rule we registered mis-flagged SNARE-seq, and we report that.

## 3. A rotation exists where the search fails

This section shows that for the pairs where your unpaired score is poor, a rotation still exists. That tells you the search is the bottleneck, and it supports your premise.

A poor unpaired score has two readings. If no rotation aligns the pair even with true pairs, the geometry is not shared. If a rotation exists and the unpaired search misses it, the geometry is shared and the search failed. The oracle separates the two. For gen, it says the second.

| holdout FOSCTTM | SPC | DCI | DOCCI |
|---|---:|---:|---:|
| gen, unpaired aligner, nothing removed | 0.415 ± 0.055 | 0.479 ± 0.066 | 0.474 ± 0.044 |
| gen, unpaired aligner, top PC removed | 0.038 ± 0.006 | 0.391 ± 0.069 | 0.478 ± 0.012 |
| gen, true-pair rotation, nothing removed | 0.009 | 0.014 | 0.010 |
| gen, true-pair rotation, top PC removed | 0.007 | 0.010 | 0.007 |
| gen, true-pair unconstrained linear map, top PC removed | 0.010 | 0.018 | 0.010 |
| Qwen3-Embedding, true-pair rotation | 0.002 | 0.003 | 0.001 |

The table supports three readings (measured).

A single rotation aligns gen on all three corpora, with or without the top PC. The geometry is there. The oracle values for gen (0.007 to 0.014) are close to those of the best control encoder (0.001 to 0.003).

The unconstrained linear map does no better than the rotation (0.010 to 0.018). The orthogonality constraint is not the obstacle, and a rotation is the right class of map for this pair.

The top PC does not break the geometry. It corrupts the pseudo-pairs that the unpaired solver builds from. Removing it is a search aid. It is enough on SPC and not enough on DCI or DOCCI.

Two more checks fit this reading. First, we ran eight restarts (seeds 0 to 7) of your aligner on gen with the top PC removed, and selected one per corpus by S1. This leaves gen near chance (DCI 0.396, DOCCI 0.502). The best of the eight, picked by truth, is still far from the oracle (0.280 and 0.341). Second, removing each of the next four PCs on its own also leaves gen near chance (DCI PC1 to PC4: 0.492, 0.511, 0.437, 0.455; DOCCI: 0.443, 0.552, 0.408, 0.570). PCs 1 to 3 are visual directions (held-out image R² 0.47 to 0.61), so removing them discards shared signal.

The oracle gives the same message on single-cell data. On CITE-seq, a rotation fitted on true pairs reaches 0.073 on held-out cells, and the unconstrained linear map reaches 0.074. You report 0.225. On SNARE-seq the oracle is 0.143 against your 0.209. On PBMC it is 0.074 against your 0.089, and there the search already works. The SNARE-seq oracle is a weaker bound than the other two, because it uses 10 and 19 dimensions and about 523 training cells.

For your paper, this means a low FOSCTTM tells you the search worked, and a high one does not tell you why. An oracle reported next to the unpaired score separates "no shared geometry" from "shared geometry that the search missed". The two need opposite responses.

## 4. Why the search fails: two kinds

This section shows that the search fails for two different reasons. The reason matters because each one needs a different fix, and a diagnostic can tell them apart.

### 4.1 A nuisance direction (long-caption text)

For gen on the three long-caption corpora, one dominant PC holds 14% to 22% of the variance, and the image embedding does not predict it. Short COCO captions show no such direction. The table gives the axis probe on the first 4,096 rows of your stored gen embeddings.

| Qwen3-8B gen | SPC | DCI | DOCCI | COCO-val (short captions) |
|---|---:|---:|---:|---:|
| top PC, share of variance | 13.8% | 19.4% | 22.2% | 12.3% |
| held-out R² of top PC from the image | 0.16 | 0.052 | 0.052 | 0.899 |
| linear CKA, gen vs image | 0.433 | 0.253 | 0.213 | 0.670 |
| linear CKA after projecting out the top PC | 0.583 | 0.462 | 0.449 | 0.513 |
| mutual 10-NN with the image | 0.216 | 0.132 | 0.115 | 0.368 |

On the three long-caption corpora, projecting out the top PC raises linear CKA. On COCO it lowers it, as it would for a good encoder whose top direction is shared. The control encoders behave like the COCO case. On SPC, Qwen3-Embedding and MPNet have top-PC image R² of 0.89 and 0.88. On DCI and DOCCI they have 0.77 to 0.87. Their top direction is the image's own, and removing it hurts them. On SPC it takes Qwen3-Embedding from 0.019 to 0.364 and MPNet from 0.026 to 0.325 (seed 0). So removal is not a blanket rule.

Our reading of the mechanism is inferred from this sign pattern. Your aligner locks onto each space's dominant axis. For the control encoders that axis is the image's own. For gen it is non-visual, so the image's top axis is matched to the wrong direction and the alignment collapses. The pseudo-pairs that the solver bootstraps from are then wrong, and every seed inherits the error. This is why more restarts do not help.

The axis is not a numeric artifact. The Qwen3-8B gen file is stored in fp32 (the loader docstring says bf16). Centering leaves about 20 of 24 mantissa bits in the residual. The bf16 files are far from rounding loss. Their per-coordinate |mean|/σ is 6 to 13.

### 4.2 Seed variance (single-cell pairs)

CITE-seq has the highest CKA of your fourteen scientific pairs (0.96) and a seed standard deviation of 0.13. In your words, "CITE-seq has a high CKA of 0.96, but its FOSCTTM varies strongly over the seeds, with a standard deviation of 0.13." Strong geometry with an unstable search is what we would expect from seed variance.

We checked for a nuisance direction and found none. Each of CITE-seq's top five PCs is predictable from the other modality (held-out R² 0.82 to 0.95 in both directions). Removing the top component before fitting makes things worse (seed mean 0.337 against a matched baseline of 0.200, over six seeds). The top components are shared signal. Over twelve seeds, FOSCTTM has mean 0.184 and ranges from 0.089 to 0.439. Some seeds find the rotation and others miss it.

### 4.3 A diagnostic to tell them apart

The first two steps use true pairs, which a small held-out paired set can supply. The third step is pairs-free. It is a diagnostic to confirm, not a validated rule.

1. Run the oracle. If it is poor, the geometry is not shared, and the rest does not apply.
2. Run the axis probe. A dominant PC with near-zero held-out R² in the other space suggests a nuisance direction.
3. Run your aligner at several seeds and record S1. A wide S1 spread that tracks true quality suggests seed variance. A narrow S1 with poor truth suggests that every seed landed on the same wrong rotation.

On long captions, S1 separates the removal of the top PC from keeping it by 0.043 on SPC, where removal works. On DCI and DOCCI the margin is only 0.001 to 0.006 (DCI: 0.485 against 0.491; DOCCI: 0.436 against 0.437). S1 can flag the problem there but cannot cure it.

The axis probe needed a post-hoc correction. We registered it as the minimum held-out R² over each space's top five PCs. That rule flagged SNARE-seq as a nuisance case, because its fourth and fifth PCs hold 4.6% and 3.0% of the variance and are not predictable from the other modality (minimum R² of −0.17). The registered removal control disagreed with the flag. Removing the top PC hurts (seed mean 0.259 against a matched 0.198), and S1 stops tracking truth (Spearman 0.83 falls to 0.09). That pattern means the top component is shared signal.

The refinement is to read only high-variance PCs. The nuisance direction in long captions is dominant (13.8% of the variance, R² 0.16). The single-cell top components are high-variance and predictable: R² 0.62 to 0.92 for PCs 1 to 3 of SNARE-seq, and 0.82 to 0.95 on CITE-seq. On PBMC the minimum over the top five is 0.61. The refinement is post hoc and rests on three single-cell pairs and three long-caption corpora. Back the diagnostic with a removal control.

## 5. A fix for seed variance: pairs-free seed selection

This section shows that S1 picks good seeds when the failure is seed variance. It answers the limitation in your paper.

Your limitation reads: "we report average rather than best performance, since without supervision one cannot select the best-performing seed." For the seed-variance type, S1 removes that limitation.

**The rule.** Run your aligner at R seeds. For each run, compute S1 on its own training rows. Report the run with the highest S1, together with S1. No true pairs are used.

**Results (measured, twelve seeds each).** On CITE-seq, which you list among your "partially aligned" pairs, S1 picks the best seed by truth. Your reported value is 0.225. Our twelve-seed mean is 0.184, with a worst seed of 0.439 and a best seed, by truth, of 0.089. The S1-selected seed is 0.089, just above the true-pair rotation (0.073). Across seeds, S1 and −FOSCTTM agree at Spearman 0.84 (0.82 pooled over iterates).

| pair | oracle | reported | 12-seed mean ± sd | S1-selected (best by truth) | Spearman(S1, −FOSCTTM) |
|---|---:|---:|---:|---:|---:|
| CITE-seq | 0.073 | 0.225 | 0.184 ± 0.095 | 0.089 (0.089) | 0.84 |
| SNARE-seq | 0.143 | 0.209 | 0.233 ± 0.137 | 0.149 (0.144) | 0.82 |
| PBMC | 0.074 | 0.089 | 0.0895 ± 0.004 | 0.096 (0.082) | 0.32 |

On SNARE-seq the selected run is within 0.005 of the best seed and next to the oracle. On PBMC the seeds barely spread, so there is nothing to pick, and the selected run (0.096) sits a little above the mean. We registered PBMC as the case where selection should not apply, and it did not apply. We claim no win there. Selection helps on the two pairs with real seed spread, and the third is already solved.

**Where selection acts and where it does not.**
- Across seeds, it is the lever.
- Across the 100 refinement iterates within a seed, it adds nothing (CITE-seq seed mean 0.18369 at the best-S1 iterate against 0.18372 at the last). The refinement is stable once it converges, and S1 never beat the last iterate in any of our runs.
- Under a shared nuisance direction, it does not help. On long captions, the S1-selected seed gives DCI 0.396 against a seed mean of 0.366, and DOCCI 0.502 against 0.466. Every seed is pulled toward the same axis, so no good seed exists to select.

**S1 as a selector over removal settings.** S1 can also choose which PC to remove. We fit your aligner once per setting (nothing removed, or one of PCs 0 to 4 removed) and kept the setting with the highest S1. On SPC, at seed 0, this picks PC0 for gen and nothing removed for Qwen3-Embedding and MPNet. At seeds 1 and 2 we re-ran the two highest-S1 settings for each encoder, and the same choice won in 9 of 9 encoder-seed cases. Every choice is also the best true-pair FOSCTTM among the settings compared. The S1 margin over the runner-up is thin for MPNet at seed 0 (0.005).

Across all six settings, the rank correlation of S1 with −FOSCTTM is 0.94 (Qwen3-Embedding), 0.94 (MPNet) and 0.77 (gen). A first version of this detector took pseudo-pairs from one fit and tested each PC inside that fit. It failed because it was circular: the image side "predicts" the non-visual PC at R² 0.855 on pseudo-pairs, against 0.16 on true pairs. Selection across separate fits avoids this.

For your paper, this means you can replace the seed average with a selected run plus the score that selected it. Where seeds do not spread, the two coincide. Where they do, the selected run is much closer to the oracle. We would still report the seed mean and range too. The result is measured on three pairs and one aligner configuration, so we would call S1 a promising selector and not a general one.

## 6. A fix for a nuisance direction: a better starting point

This section shows how to recover long-caption pairs where removing one axis was not enough. It matters because it works on the pairs where seed selection does not.

The oracle shows that a rotation exists, so the starting point of the search is the place to intervene. We pre-registered one success bar: bring gen below FOSCTTM 0.10 on both DCI and DOCCI, the level the control encoders reach. Your aligner without changes gives about 0.48 on both.

| gen, long captions, FOSCTTM | DCI | DOCCI | image-caption pairs used | seeds |
|---|---:|---:|---|---:|
| baseline, one axis removed | 0.391 | 0.478 | none | 3 |
| SPC-fit map as the start, then your refinement | **0.078 ± 0.008** | **0.051 ± 0.007** | SPC only | 3 |
| the same map applied directly, no refinement | 0.107 ± 0.013 | 0.100 ± 0.010 | SPC only | 3 |
| 100 true pairs, your few-pair protocol | 0.085 ± 0.002 | 0.100 ± 0.008 | 100 on target | 3 |
| 50 true pairs | 0.109 ± 0.009 | 0.152 ± 0.015 | 50 on target | 3 |
| text pivot through Qwen3-Embedding | 0.170 ± 0.055 | 0.172 ± 0.026 | none | 3 |
| the pivot's own unpaired Qwen3-Embedding-to-image step | 0.139 ± 0.051 | 0.136 ± 0.028 | none | 3 |
| true-pair rotation (ceiling) | 0.010 | 0.007 | all | |

**A map fitted on SPC works (measured).** We fit the map on SPC with the top PC removed and used it as the start for your refinement on DCI and DOCCI. It cleared the bar on both corpora with margin. Applied directly, the map is borderline (0.107, 0.100), and the refinement makes it robust. If the axis is kept, the transferred map stays at chance (0.489, 0.486). This extends your SPC-to-COCO validation. A map fitted on SPC with its axis removed also transfers to held-out COCO-val (holdout FOSCTTM 0.409 raw, 0.022 with the axis removed, on 5,000 images the map never saw).

**About one hundred true pairs work (measured).** On DCI, FOSCTTM falls with pair count: 0.462, 0.368, 0.282, 0.109 and 0.085 at 1, 5, 10, 50 and 100 pairs. On DOCCI it falls as 0.450, 0.260, 0.213, 0.152 and 0.100. One hundred pairs clear the bar on DCI. They sit at the bar on DOCCI, where two of three seeds are below it. Fifty clear it on neither. The count is larger than the handful your method needs on well-behaved pairs, which shows how far the non-visual axis sets the search back. DOCCI may want somewhat more than 100 for margin. The DOCCI values at 1, 5 and 10 pairs are single-seed.

**A text pivot gets closer without image-caption pairs, and does not reach the bar (measured).** A second text encoder on the same captions gives a free within-text correspondence. We fit a rotation from gen to Qwen3-Embedding (text-to-text FOSCTTM 0.0002) and composed it with your unpaired Qwen3-Embedding-to-image map. The result is about three times better than the 0.48 baseline. It is limited by its own unpaired image step, which your method does at about 0.14 here with large seed variation. Refining from the pivot start makes it worse (0.182 and 0.199). Whether a second same-modality encoder fits your definition of "unpaired" is for you to judge. We flag the assumption and do not settle it.

**What does not help (measured, single-seed for the first two).** Removing the top two to five PCs cumulatively and selecting by S1 leaves gen near chance (DCI 0.464 at the S1-selected setting, DOCCI 0.354; the range across settings is 0.369 to 0.470 and 0.354 to 0.532). Selecting the best refinement iterate by S1 gains nothing (0.0000 in every run). Selecting the best seed by S1 does not beat the seed mean (Section 5). Each of these needs a search that does not converge to the wrong place to begin with.

For your paper, this means that if a long-caption generative encoder is in scope, an SPC-fit start plus your refinement is a practical default. It assumes a second corpus with the same encoder pair exists, and it uses SPC image-caption pairs only through the fitted map. If you can allow a small labelled set, 100 pairs do almost as well.

## 7. What CKA predicts

This section shows what linear CKA tells you about a pair and what it does not. It matters because your main-text predictor is CKA.

Your main-text predictor is linear CKA. It explains most of the variance in FOSCTTM (R² 0.73 in your Section 4.3), and it rates gen low. On SPC, gen's linear CKA is 0.433 against 0.657 for Qwen3-Embedding and 0.633 for MPNet. On DCI and DOCCI it is 0.253 and 0.213. That prediction is right: your unpaired aligner does fail on gen there.

CKA predicts the difficulty of the search. It does not predict whether a rotation exists. The oracle in Section 3 finds one for gen on all three corpora, so low CKA is evidence that unpaired search will struggle and not that the geometry is missing. CITE-seq shows the other side (Section 4.2). Its CKA is the highest you report, and its seeds still vary widely. So a low CKA does not rule out a rotation, and a high CKA does not guarantee that the search finds one.

On the first open problem, we offer S1 as a pairs-free ingredient and nothing more. It is not an alignment prediction score. Read across seeds, it flags seed variance (Section 5). Read across removal settings, it picks the nuisance PC on SPC without any pairs (Section 5). The axis probe in Section 4.3 is clearer, but it uses true pairs.

**A note on your Appendix D.** That analysis uses the clipped CKA of Wang et al. On SPC it gives 0.608, 0.659 and 0.636 for gen, Qwen3-Embedding and MPNet, which puts gen level with the others (+0.014 over mean pooling). It turns negative on the two densest corpora (−0.144 on DOCCI, −0.067 on DCI). Linear CKA separates gen (0.433) from the others (0.63 to 0.66) on SPC. Our inferred reading is that clipping bounds the large coordinates of the dominant axis, so the clipped comparison understates the SPC deficit. This is a comment on your Appendix D, not on your main predictor.

**A lemma behind the sign pattern.** The lemma explains the pattern in Section 4.1. If X = R + S is zero-mean and S is independent of the image, then CKA(X, Y) = CKA(R, Y) · ‖Σ_R‖_F / ‖Σ_R + Σ_S‖_F. Removing an image-independent component raises CKA, and removing a component the image shares lowers it. The independence assumption is inferred, not shown. For gen on SPC the implied nuisance ratio is ρ ≈ 0.9, from 0.583/0.433 = 1.35. The proof is in `response.md`.

## 8. Recommendations

This section turns the results above into six changes you could make. The last one stands apart from the main thread.

1. **Report a true-pair oracle next to each unpaired FOSCTTM.** Use a closed-form Procrustes fit on held-out true pairs, and a linear fit beside it. It separates a geometry problem from a search problem. A pair at chance with a good oracle is worth more effort. A pair at chance with a poor oracle is not.
2. **Where seeds spread, report the S1-selected run.** Wrap your aligner: run R seeds, compute S1 on each run's training rows, and report the maximum with its score. Show the seed mean and range too. This is measured on three single-cell pairs, and selection is not needed on PBMC.
3. **Run the diagnostic.** Check whether a high-variance PC of one space is unpredictable from the other, and read the S1 spread across seeds. Back it with a removal control, since the registered rule mis-flagged SNARE-seq.
4. **For a nuisance direction, start the search better.** An SPC-fit map plus your refinement, or about 100 true pairs, recovered DCI and DOCCI. Do not rely on axis removal alone off SPC. Do not rely on iterate or seed selection under a shared nuisance direction.
5. **In your Appendix D, report linear CKA next to clipped CKA,** and state that CKA predicts the search and not the existence of a rotation.
6. **Report per-pair fidelity next to FOSCTTM for text-to-image use.** This comes from our first note and is outside the main thread here. On COCO with DINOv2-B and MPNet, your zero-pair map retrieves almost perfectly (FOSCTTM 0.0073, seed 0). Its median cosine to the true partner is 0.53. Two oracle maps fitted on 20,000 true pairs retrieve identically (FOSCTTM 0.0027 and 0.0026) and differ by 0.21 in median cosine (0.572 and 0.781). The zero-pair map is only 0.07 ± 0.03 below the best rotation, and the rotation constraint costs three times that. Relaxing the rotation is the lever for per-item fidelity. We have not tested a relaxed map. The measurements are in `response.md`.

## 9. Limitations

This section lists where our evidence is thin, so you can judge how far to trust each result.

- **Three single-cell pairs, one aligner configuration.** The single-cell pairs have 1,000 to 2,400 cells and use your defaults. S1 should be confirmed on more pairs before it is called a general selector. Human-versus-mouse RNA and histology-versus-expression need external pipelines and were not run.
- **The diagnostic is not a validated rule.** The registered form mis-flagged SNARE-seq. The high-variance refinement is post hoc.
- **The vision-language selection and removal results lean on gen.** The axis probe covers four corpora and three encoders. The detector searches only the top five PCs. It would miss a nuisance axis outside them, or one on the vision side. Control-encoder cells are seed 0.
- **The starting-point arms use three seeds, and several negatives use one.** The cumulative axis search and iterate selection come from one seed, as marked. The pivot assumes a second same-modality encoder is admissible.
- **Our SNARE-seq reproduction is 0.178 against your 0.209.** FOSCTTM, LTA (0.945 against your 0.942) and CKA match on PBMC, and CKA matches on all three pairs. We have not explained the SNARE-seq gap.
- **Our implementation, your commit.** Differences from your numbers would come from our reimplementation of the pipeline, though the reproduction checks match closely.
- **The fidelity numbers use one dataset.** The span-ceiling and fidelity results in `response.md` rest on COCO with one encoder pair. The FLUX consumer zones used there are a reference scale for a different space.

---

## Appendix A. Receipts

Every scored number comes from a JSON receipt produced with your library at `fdfad84`, under `experiments/results/` in the `unpaired-rosetta` directory. Experiment identifiers appear only here.

| id | measures | receipt | numbers backed |
|---|---|---|---|
| E5 | axis probe and removal on SPC; removal-setting detector | `results/e5_scaffold_axis/e5_axis_probe-20261009T191307.json`; `e5_gates-*.json`; `e5_scaffold_axis-raw-drop1-*-seed{1,2}-*.json` | SPC probe; removal 0.415 to 0.038; detector 9 of 9 |
| E6 | axis probe and unpaired fits on DCI, DOCCI, COCO-val | `results/e6_generality/e6_axis_probe-*.json` | Section 4.1 table; DCI and DOCCI unpaired rows |
| E6b | true-pair oracle and eight restarts | `results/e6_generality/e6b_oracle-*.json` | Section 3 table; 0.396 and 0.502 selected, 0.280 and 0.341 best of eight |
| E7 | starting points | `results/e7_search_init/e7_arm{A,B,C,D,E}-*.json`; `experiments/e7_search_init/FINDINGS.md` | Section 6 table |
| E8 | CITE-seq | `results/e8_single_cell/e8_merged_summary.json`; `experiments/e8_single_cell/FINDINGS.md` | Section 5 CITE-seq table |
| E9 | PBMC and SNARE-seq | `results/e9_single_cell_more/e9_merged_summary.json`; `experiments/e9_single_cell_more/FINDINGS.md` | Section 5 pair table; type-test correction |
| E1 | fidelity gap | `results/e1_fidelity_gap/e1_fidelity_gap-20261009T200203.json`; `e1_fidelity_gap-seed{1,2}-*.json` | recommendation 6 |

**Reproduction checks.** For CITE-seq, over your five seeds, we get a mean FOSCTTM of 0.221 and a standard deviation of 0.132, against your 0.225 and 0.13. CKA on the 1,000 cells is 0.961, against your 0.96. Our first attempt gave 0.305. It drew fresh randomness where your code reuses the random state already advanced by the train split. The check caught this, the corrected run is the one reported here, and the stale receipts are quarantined. For PBMC our five-seed value is 0.088 (yours 0.089). For SNARE-seq our five-seed value is 0.178 against your 0.209, and we do not know why. CKA matches on all three pairs.

**Hosts.** Fits ran on a laptop and on a Linux GPU host. Small fits agree to 1e-6. Full-scale fits differ like seeds (Qwen3-gen at seed 0, raw 0.407 against 0.419). Each comparison is made within one host.

**Reproduction table, single-cell pairs.**

| pair | CKA (paper) | oracle orthogonal / linear | their result / our 5-seed canary | 12 seeds mean ± sd (min to max) | S1-selected (best) | Spearman |
|---|---|---|---|---|---|---:|
| CITE-seq | 0.961 (0.96) | 0.0727 / 0.0741 | 0.225 / 0.221 | 0.184 ± 0.095 (0.089 to 0.439) | 0.0893 (0.089) | 0.839 |
| SNARE-seq | 0.855 (0.86) | 0.143 / 0.144 | 0.209 / 0.178 | 0.233 ± 0.137 (0.144 to 0.652) | 0.149 (0.144) | 0.818 |
| PBMC | 0.898 (0.90) | 0.074 / 0.078 | 0.089 / 0.088 | 0.0895 ± 0.0043 | 0.096 (0.082) | 0.32 |

**Single-cell removal controls (top PC removed).** CITE-seq (six seeds): mean 0.337, S1-selected 0.360, against matched baselines 0.200 and 0.098. SNARE-seq (six seeds): 0.259 against a matched 0.198, and S1 agreement 0.83 to 0.09. CITE-seq top-5 PC cross-modal R²: 0.82 to 0.95. SNARE-seq registered rule minimum top-5 R²: −0.17, PCs 4 and 5 at 4.6% and 3.0% of variance. PBMC minimum top-5 R²: 0.61. Their reported values (CITE-seq 0.225, sd 0.13, CKA 0.96; PBMC 0.089; SNARE-seq 0.209; scientific CKA R² 0.69) come from arXiv 2610.09411 v2.

**Removal settings on SPC (seed 0).** Gen S1 and FOSCTTM: none removed 0.473 and 0.419; PC0 removed 0.517 and 0.033; PC1 0.464 and 0.460; PC2 0.470 and 0.377; PC3 0.469 and 0.293; PC4 0.469 and 0.459. For Qwen3-Embedding and MPNet, "none removed" has the highest S1 (0.516 and 0.524) and the best FOSCTTM (0.021 and 0.030). S1 margins over the runner-up, seeds 0 / 1 / 2: gen 0.044 / 0.030 / 0.041; Qwen3-Embedding 0.017 / 0.023 / 0.013; MPNet 0.005 / 0.023 / 0.021. The S2 variant (linear CKA of matched pairs) disagrees with S1 for MPNet at seed 0 (it picks PC3 removed, FOSCTTM 0.043 against 0.030) and has rank correlation with −FOSCTTM of 0.83, 0.89 and 0.26 (Qwen3-Embedding, MPNet, gen).

**Other starting-point detail.** Text pivot control and compose: Section 6 table. Refine-from-pivot: 0.182 ± 0.052 and 0.199 ± 0.027. Transfer, axis kept: 0.489 and 0.486 (one seed). Few-pair rows at k = 10, 5, 1: DCI 0.282 ± 0.051, 0.368 ± 0.039, 0.462 ± 0.028 (three seeds); DOCCI 0.213, 0.260, 0.450 (one seed).

## Appendix B. Preregistration and integrity

The CITE-seq hypotheses (a rotation exists, the reproduction matches, pairs-free selection beats the mean, the removal control) were frozen before any scored run in `experiments/e8_single_cell/`. The PBMC and SNARE-seq hypotheses and the registered type rule were frozen in `experiments/e9_single_cell_more/PREREG.md`. The starting-point hypotheses and the 0.10 bar were frozen in `experiments/e7_search_init/PREREG.md`. The high-variance refinement of the type test was found after the registered rule mis-flagged SNARE-seq and is labelled post hoc. Predictions for the SPC removal experiment and the removal-setting detector are in their script headers. Two of those predictions, that a pseudo-pair detector finds gen's axis and never hurts, were false.

We read each claim from the direction and size of its measured effect against seed noise. A frozen bar decides only its own prediction. We adopted this after self-set round bars decided claims in both directions on identical evidence.

## Appendix C. Seed counts

| result | seeds |
|---|---|
| SPC removal, gen (raw and top PC removed) | 3 |
| SPC, Qwen3-Embedding and MPNet: nothing removed | 3 |
| SPC, Qwen3-Embedding and MPNet: top PC removed | 1 (seed 0) |
| DCI and DOCCI unpaired fits, gen | 3 |
| DCI and DOCCI, control encoders | 1 (seed 0) |
| Eight-restart search test | 8 |
| Detector on SPC | 3 (top two settings re-run at seeds 1 and 2) |
| Starting-point headline arms | 3 |
| Cumulative axis search; iterate selection | 1 |
| S1 seed selection on long captions | 3 (raw) and 8 (axis removed) |
| Single-cell selection | 12 |
| Single-cell removal controls | 6 |

## Appendix D. What this note leaves out

The first note also reports four results that are not part of this thread. A symbol-level check of your premise between SmolLM2 and a diffusion text conditioner recovers an 18-symbol correspondence with zero pairs (18 of 18). A span ceiling for pair-based baselines holds on COCO but is loose. Choosing pairs as vision-side medoids helps the baselines and not your method. Two ideas failed: token-centering the thinking preamble lowers CKA, and a late layer helps by only 0.007 to 0.015 CKA. Details and receipts are in `response.md`.

## References

1. Schnaus, Dagès, Cremers, Wang, Isola. Shared Geometry as a Rosetta Stone: Cross-Modal Alignment Without Paired Data. arXiv 2610.09411 v2, 2026. Code commit `fdfad84`.
2. Schnaus, Araslanov, Cremers. It's a (Blind) Match! Towards Vision-Language Correspondence Without Parallel Data. CVPR 2025. arXiv 2503.24129.
3. Kornblith, Norouzi, Lee, Hinton. Similarity of Neural Network Representations Revisited. ICML 2019.
4. Mémoli. Gromov-Wasserstein Distances and the Metric Approach to Object Matching. Foundations of Computational Mathematics 11(4), 2011.
5. Alvarez-Melis, Jaakkola. Gromov-Wasserstein Alignment of Word Embedding Spaces. EMNLP 2018. arXiv 1809.00013.
6. Conneau, Lample, Ranzato, Denoyer, Jégou. Word Translation Without Parallel Data. ICLR 2018. arXiv 1710.04087.
7. Jha, Zhang, Shmatikov, Morris. Harnessing the Universal Geometry of Embeddings. arXiv 2505.12540, 2025.
