---
title: "When a Rotation Exists but the Search Misses It: Alignability, Searchability, and Pairs-Free Selection in Unpaired Alignment"
subtitle: "A follow-up to Schnaus, Dagès, Cremers, Wang and Isola, 'Shared Geometry as a Rosetta Stone' (arXiv 2610.09411), and to our first note"
status: "DRAFT 2 (2026-10-24): all experiments measured and complete. CITE-seq (E8), the search-initialization study (E7, three seeds on the headline arms), and two more single-cell pairs (E9, PBMC and SNARE-seq) are done; the one refinement of the type test is labelled post-hoc."
date: 2026-10-24
authors: Jacob Hollenbeck
code: experiments/ (their library pinned at fdfad84; every scored number has a JSON receipt under experiments/results/)
---

# When a Rotation Exists but the Search Misses It

**Alignability, searchability, and pairs-free selection in unpaired alignment.**
*A follow-up to Schnaus, Dagès, Cremers, Wang and Isola, "Shared Geometry as a Rosetta Stone" (arXiv 2610.09411),
and to our first note, "Reading Is Not Authoring."*

> **How to read this note.** *Measured* results cite a receipt (a JSON file) under `experiments/results/`. *Inferred*
> marks a mechanism read from measurements but not tested directly. *Post-hoc* marks a result found after a frozen
> test. Experiment identifiers (E7, E8, ...) appear only in the receipts appendix; the text uses plain names. All
> experiments are measured and complete. One refinement of the type test, in Section 6, was found after our registered
> rule mis-flagged a pair; we label it post-hoc wherever it appears and treat the type test as a diagnostic to confirm,
> not a validated rule.

## Abstract

Schnaus et al. show that separately trained encoders often share enough geometry to be aligned by a single rotation,
with no paired data, and that a pair's alignment quality tracks its shared geometry as measured by linear CKA. They
leave two problems open in the paper, in their own words. "Developing fully unsupervised alignment prediction scores
remains an open problem," and, on seed variance, "we report average rather than best performance, since without
supervision one cannot select the best-performing seed." Our first note, working on their vision and language data,
found one case where their unpaired search fails even though a rotation exists: a dominant non-visual axis in their
generative token pooling of long captions. This note separates the two ideas that case runs together. We call a pair
*alignable* when a single rotation fitted on the true pairs aligns it, and *searchable* when their unpaired search
finds such a rotation on its own. A pair can be alignable without being searchable.

We report three results. First, the two search failures we have measured have different causes. In long-caption text
the search is misled by a shared non-visual axis. In the single-cell pairs that Schnaus et al. list among their
"partially aligned" data, the search is not misled by any dominant axis; it simply varies from seed to seed. We propose
a pairs-free test meant to tell the two apart, and we are honest about its limits: the exact rule we registered
mis-flagged one pair, and the refinement that fixes it is post-hoc and still needs confirming. Second, for the
seed-variance type a pairs-free score selects good runs, measured on three single-cell pairs. On CITE-seq, scoring each
run by the mean cosine of its own matched pairs picks the single best seed by truth out of twelve (FOSCTTM 0.089
against a seed mean of 0.184 and a true-pair rotation ceiling of 0.073), with no pairs. On SNARE-seq it selects a
near-best run (0.149 against a seed mean of 0.233, next to the 0.143 oracle). On PBMC, which the search already solves,
the seeds barely spread and there is nothing to select; we report that plainly. The same score does not help when every
seed is misled by the same axis, which is the long-caption case. Third, on the long-caption corpora where removing one
axis was not enough, a better search initialization recovers the alignment: transferring a map fitted on another corpus
(FOSCTTM 0.078 and 0.051 over three seeds), or supplying about one hundred true pairs (0.085 and 0.100), brings the
generative pooling near the well-aligned text encoders, while a pairs-free axis search, iterate selection and seed
selection do not. The one fix that uses no image-caption pairs, a pivot through a second text encoder, cuts the error
about threefold but does not reach 0.10. We close with a short list of things an author of an unpaired alignment method
can do: report a true-pair oracle, run the type test as a diagnostic, and select runs by the pairs-free score when the
failure is seed variance.

---

## 1. Introduction

Schnaus et al. align two separately trained representation spaces without any matched examples. They center and
unit-normalize both spaces, match cluster centers by their internal similarities (a step equivalent to maximizing
linear CKA), read a set of pseudo-pairs out of the matched centers, and then alternate Hungarian matching with
orthogonal Procrustes to refine a single rotation. They evaluate retrieval with FOSCTTM, the average fraction of
candidates that outrank the true partner, where 0 is perfect and 0.5 is chance. Their main finding is that the
alignment quality of a pair tracks its shared geometry: linear CKA explains most of the variance in FOSCTTM, both
across vision-language encoders and across fourteen scientific pairs.

They are explicit about two limits. They cannot decide from unpaired data alone whether two spaces are similar enough
to align, because the usual metrics need matched samples, and they call a fully unsupervised prediction score an open
problem. And because they cannot select the best run without supervision, they report the average over seeds rather
than the best. Our first note added a third observation on their vision-language data: their generative token pooling
of long captions aligns near chance even though its geometry is shared, because one dominant axis of the text
embeddings is non-visual and misleads the unpaired search.

This note makes four contributions, built on their released embeddings and their library at commit `fdfad84`.

1. A clean separation of two properties that the generative-pooling case runs together: whether a rotation exists
   (alignability, measured by a true-pair oracle) and whether their unpaired search finds one (searchability).
2. Evidence that search failures come in at least two types, with a pairs-free diagnostic meant to tell them apart. The
   long-caption case is a misleading axis; the single-cell pairs are seed variance. We also report where the first form
   of the diagnostic failed and label the fix post-hoc.
3. A pairs-free score that selects good runs when the failure is seed variance, measured on three single-cell pairs
   (CITE-seq, SNARE-seq and PBMC), together with the boundary where it does not help.
4. A measured recovery of the long-caption case through a better search initialization, where one-axis removal and a
   pairs-free axis search had failed.

## 2. Alignability and searchability

We separate two questions that FOSCTTM alone does not.

**Alignability.** A pair is alignable if a single rotation, fitted on the true pairs, aligns it. We measure this with
an oracle: give a Procrustes fit the true correspondence on one unpaired half of the data, then score FOSCTTM on a
disjoint held-out half. If the oracle reaches good retrieval, a rotation exists and the shared geometry is real. We
also fit an unconstrained linear map on the same pairs; when the orthogonal and linear oracles agree, the map that
exists is a true rotation, not a scaling or a shear.

**Searchability.** A pair is searchable if their unpaired aligner, given no pairs, finds a rotation close to the
oracle's. This is what their reported FOSCTTM measures.

The two can diverge. Their own CKA predictor speaks to searchability, not to alignability: a low CKA says the unpaired
search will struggle, not that no rotation exists. Our first note showed this for generative pooling on long captions,
where the oracle aligns the space (held-out FOSCTTM 0.009 to 0.014 across three corpora) while the unpaired search
stays near chance off one corpus. The sections below show the same gap in a second domain and use the oracle as a
routine instrument: run it first, and the number it returns tells you whether to invest in a better search or to stop.

## 3. Two types of search failure

When the unpaired search fails on a pair the oracle says is alignable, the cause is not always the same. We have
measured two.

**Type one, a misleading axis.** This is the long-caption case from our first note. The text embeddings have one
dominant axis that the image does not predict. Their search locks the image's own dominant axis onto this non-visual
axis, and the alignment collapses. The signature is a dominant principal component of one space with near-zero
held-out predictability from the other space. On the three long-caption corpora the top generative-pooling component
holds 14 to 22 percent of the variance with held-out image predictability (R-squared) of 0.05 to 0.16, against 0.77 to
0.90 for the text encoders that align well. Removing that one component raises linear CKA, which is the opposite of
what removing a shared component does.

**Type two, seed variance.** Here no axis is misleading; different seeds of the same search land in different places,
some good and some near chance. The centerpiece of this note is a measured example.

### 3.1 CITE-seq: a rotation exists, but the search varies (measured)

Schnaus et al. list CITE-seq among their "partially aligned" scientific pairs. CITE-seq measures the same cells two
ways, as RNA expression and as surface-protein counts. They report its FOSCTTM at 0.225 with a seed standard deviation
of 0.13, even though its CKA of 0.96 is the highest of their fourteen scientific pairs. In their words, "CITE-seq has a
high CKA of 0.96, but its FOSCTTM varies strongly over the seeds, with a standard deviation of 0.13." That pattern,
strong shared geometry with a search that misses, is exactly what alignability without searchability looks like.

We reproduced their setting exactly, using their single-cell loader, their default aligner (the four hyperparameters
C=30, S=30, b=10000, R=100), their disjoint unpaired split, and their FOSCTTM. The reproduction canary matches: over
their five seeds the mean FOSCTTM is 0.221 and the sample standard deviation 0.132, against their 0.225 and 0.13, and
CKA on all 1,000 cells is 0.961 against their 0.96. A first attempt missed their numbers (mean 0.305) because it drew
fresh randomness where their code reuses the random state already advanced by the split; the canary caught it, and the
corrected run is the one cited here. The stale receipts are quarantined.

**A rotation exists.** Given the true pairs on one unpaired half, a single orthogonal map reaches FOSCTTM 0.073 on the
held-out half. An unconstrained linear map does no better (0.074), so the map that exists is a rotation. Both are far
below their reported 0.225. CITE-seq is alignable. The failure is in the search.

**The failure is seed variance, not an axis.** Every one of the top five principal components of each modality is
predictable from the other modality (held-out R-squared 0.82 to 0.95 in both directions). There is no dominant
component that one side carries and the other cannot. This is the opposite of the long-caption case, and it rules out
the type-one mechanism here. To confirm, we removed the top variance component of each modality before fitting: it
hurt rather than helped (seed mean 0.337 against a matched baseline of 0.200), because on this pair the top components
are shared signal, not a misleading axis.

### 3.2 A pairs-free test that tells the types apart

The two types can be separated without any pairs, using two measurements already available before fitting.

First, the axis probe. For each top principal component of one space, measure how well the other space predicts it,
using only the within-space pairing of a second encoding where available, or the raw features of the paired modality.
A dominant component with near-zero cross-space predictability is the type-one signature. On the long-caption corpora
the top generative-pooling component has held-out predictability near 0.05 to 0.16; on CITE-seq every top component is
predictable at 0.82 or above. The probe uses no image-caption or cross-modality correspondence beyond what is free.

Second, the seed spread of the pairs-free self-score. Run the search at several seeds and, for each, record the mean
cosine of its own matched pairs. Call this score S1. S1 uses no true pairs. If S1 spreads across seeds and tracks true
quality, the failure is seed variance and selection will help (Section 4). If S1 is uniformly high across seeds while
true FOSCTTM stays poor, the search is confidently landing on the wrong rotation every time, which is the type-one
signature. On the long-caption corpora the S1 margin between removing the misleading axis and leaving it in was only
0.001 to 0.006, far thinner than its 0.043 margin on the one corpus where removal worked, so S1 could flag but not fix
the problem there. On CITE-seq S1 spreads widely and tracks truth (Section 4).

The test, then, is to run the oracle to check whether a rotation exists; if it does, run the axis probe and read the
seed spread of S1. A dominant non-predictable axis means type one; a wide, truth-tracking S1 spread with no such axis
means type two.

A caution on the axis probe, measured in Section 6. We registered it as a minimum held-out predictability over each
space's top five principal components, a low minimum meaning a misleading axis. That exact rule mis-flagged one
single-cell pair (SNARE-seq), because it fired on a low-variance idiosyncratic direction rather than a dominant one,
and the registered removal control showed the top component there was shared signal, not a nuisance. The refinement
that fixes this, reading only high-variance components, is post-hoc. We describe it where it is measured, in Section 6,
and we treat the whole probe as a diagnostic to confirm rather than a validated rule.

## 4. Pairs-free selection when the failure is seed variance

Their stated limitation is that without supervision they cannot select the best seed, so they report the average. For
the seed-variance type, a pairs-free score removes that limitation.

**The score.** S1 is the mean cosine of the aligner's own Hungarian-matched pairs, computed on its training rows with
no true correspondence. It measures how well one rotation makes the two point clouds coincide as sets. We also track
S2, the linear CKA of the matched pairs. Their refinement loop returns the last of R=100 iterates with no selection
step (read from their `wasserstein_procrustes.py` at commit `fdfad84`, as recorded in our contribution-map note), so
there are three places selection could act: across iterates within a run, across restarts, and across seeds.

**CITE-seq result (measured).** Over twelve seeds the last-iterate FOSCTTM has mean 0.184 and ranges from 0.089 to
0.439. Selecting the seed with the highest S1 picks the single best seed by truth, 0.089, with no pairs. That selected
value sits just above the true-pair rotation ceiling of 0.073 and well below the 0.184 seed mean and the 0.225 Schnaus
et al. report. Across seeds S1 and true FOSCTTM agree, with a Spearman correlation of 0.84 (0.82 pooled over
iterates). This turns their sentence, "without supervision one cannot select the best-performing seed," into a seed
that can be selected on this pair.

| CITE-seq, their default aligner | FOSCTTM |
|---|---:|
| their reported value | 0.225 |
| seed mean over 12 seeds (our reproduction) | 0.184 |
| worst of 12 seeds | 0.439 |
| best of 12 seeds (by truth) | 0.089 |
| **pairs-free S1 selection over 12 seeds** | **0.089** |
| true-pair orthogonal oracle (ceiling) | 0.073 |

Receipt: `results/e8_single_cell/e8_merged_summary.json`.

**Where selection acts, and where it does not.** Selection across seeds is the lever. Selection across iterates within
a single seed adds nothing (seed-mean 0.18369 at the best-S1 iterate against 0.18372 at the last), because the
refinement is stable once it converges. And selection does not rescue the type-one failure. On the long-caption
corpora, S1 seed selection does not beat the seed mean for generative pooling, because there the spread does not
reflect search luck; every seed is pulled toward the same non-visual axis, so there is no good seed to select. This is
the boundary the type test predicts: select by S1 when the failure is seed variance, not when it is a shared
misleading axis.

## 5. Better search initialization for the long-caption case

Our first note left the long-caption case as a diagnosis without a general fix. Removing one axis restored the
alignment on one corpus (FOSCTTM 0.415 to 0.038) but not on the two others (0.479 to 0.391, and 0.474 to 0.478), even
though the oracle showed a rotation exists on all three (0.007 to 0.014). The deficit is a search failure, so the
right place to intervene is the search's starting point. We pre-registered a set of initialization changes with a
single success bar: bring generative pooling below FOSCTTM 0.10 on both of the two corpora where axis removal had
failed, the level the well-aligned text encoders reach. The headline arms below are measured over three seeds; the
negative-control arms are single-seed, noted where they appear.

**A map transferred from another corpus works.** Fitting the map on the first corpus with the one axis removed and
using it as the start for their refinement on the other two reaches FOSCTTM 0.078 plus or minus 0.008 and 0.051 plus or
minus 0.007 over three seeds, near the oracle. Applying the transferred map directly, with no refinement, is borderline
(0.107 plus or minus 0.013 and 0.100 plus or minus 0.010), so the refinement step is what makes it robust. The refined
arm clears the 0.10 bar on both corpora, against about 0.49 for the untransferred baseline and the 0.391 to 0.478 that
one-axis removal alone left. This is the first note's forward-transfer result, measured on two more corpora: the removal
rescues the fitting, and the fitting can be done once and carried over.

**About one hundred true pairs work.** Weaving true pairs into the initialization and every refinement step, in their
few-pair protocol, recovers generative pooling as the pair count rises. On the first corpus the FOSCTTM falls 0.462,
0.368, 0.282, 0.109, 0.085 at 1, 5, 10, 50, 100 pairs; on the second, 0.450, 0.260, 0.213, 0.152, 0.100. One hundred
pairs clear the bar on the first corpus robustly (0.085 plus or minus 0.002 over three seeds) and sit at it on the
second (0.100 plus or minus 0.008, two of three seeds below it); fifty clear it on neither. The smallest recovering
count here is about one hundred, larger than the handful their method needs on well-behaved pairs, which is itself a
measure of how far the non-visual axis sets the search back; the second corpus looks to want somewhat more than one
hundred for margin.

**A text pivot gets closer without image-caption pairs, but not to the bar.** A second text encoder on the same captions
gives a free within-text correspondence: the same caption, encoded twice. Fitting a rotation from generative pooling to
that second text encoder (text-to-text FOSCTTM 0.0002, so the rotation is near-exact) and composing it with the unpaired
image-to-text map that their method already finds reaches FOSCTTM 0.170 plus or minus 0.055 and 0.172 plus or minus
0.026 over three seeds. This is about a threefold improvement over the 0.48 baseline and uses no image-caption pairs,
but it does not clear 0.10. It is bounded by its own unpaired image-to-text step, which their method does at 0.139 plus
or minus 0.051 and 0.136 plus or minus 0.028 on these corpora with large seed variation; the pivot does not add the
failure, it inherits the generic unpaired-fit ceiling. Refining from the pivot start makes it worse. Whether a second
same-modality encoder fits inside their unpaired setting is a scoping question for the authors; we flag the assumption
rather than settle it.

**A pairs-free axis search and selection do not work.** Removing the top two, three, four or five components
cumulatively and selecting by S1 leaves generative pooling near chance (0.35 to 0.53 at seed 0), confirming the first
note's finding that no small set of axis removals is enough off the one corpus. Selecting the best of the 100 refinement
iterates by S1 also does nothing, because the search has already settled near chance before the last iterate. Selecting
across seeds by S1 does not help either: on the two corpora the best-S1 seed gives 0.396 (against a seed mean of 0.366
and a best-by-truth of 0.280) and 0.502 (against 0.466 and 0.341), so S1 neither beats the mean nor nears 0.10. This is
the same boundary Section 4 draws: selection cannot fix a search that converges confidently to the wrong place, because
there is no good seed to select.

| long-caption generative pooling, FOSCTTM | corpus A | corpus B |
|---|---:|---:|
| baseline, one axis removed (from the first note) | 0.391 | 0.478 |
| transfer a map from another corpus, applied directly | 0.107 | 0.100 |
| transfer a map, then refine on the target | **0.078** | **0.051** |
| about 100 true pairs | 0.085 | 0.100 |
| text pivot, no image-caption pairs | 0.170 | 0.172 |
| image-to-text control (the pivot's ceiling) | 0.139 | 0.136 |
| cumulative axis search, pairs-free selection (seed 0) | 0.464 | 0.354 |
| true-pair rotation oracle (ceiling) | 0.010 | 0.007 |

Receipts: `results/e7_search_init/e7_arm{A,B,C,D,E}-*.json`. Corpus A and B are the two long-caption corpora where
one-axis removal did not clear the bar in the first note. The headline arms (transfer-then-refine, about 100 pairs, the
text pivot and its control) are three-seed means; the axis-search row is a single-seed negative control.

## 6. Generality across their scientific pairs

CITE-seq is one dataset. The claim that a pairs-free score selects good runs for the seed-variance type needs more than
one pair. Schnaus et al.'s own loaders support two more that run on modest compute, PBMC and SNARE-seq, and we ran the
same instruments on all three: the true-pair oracle, which checks whether a rotation exists; the axis probe, which
checks for a misleading axis; and the pairs-free seed selection, which checks whether S1 picks a good seed.

| scientific pair | oracle FOSCTTM | their reported | 12-seed mean | S1 selection (best by truth) | failure type |
|---|---:|---:|---:|---:|---|
| CITE-seq (RNA vs surface protein) | 0.073 | 0.225 | 0.184 | 0.089 (0.089) | seed variance |
| SNARE-seq (RNA vs ATAC) | 0.143 | 0.209 | 0.233 | 0.149 (0.144) | seed variance |
| PBMC (RNA vs ATAC) | 0.074 | 0.089 | 0.0895 | 0.096 (0.082) | seed variance, already solved |

Receipt: `results/e9_single_cell_more/e9_merged_summary.json`.

A rotation exists on all three. The oracle sits well below each reported FOSCTTM on CITE-seq (0.073 against 0.225) and
SNARE-seq (0.143 against 0.209), and level with it on PBMC (0.074 against 0.089), where the search already succeeds.
SNARE-seq's oracle is looser than the other two, on ten and nineteen dimensions and about 523 training cells, so its
ceiling is a weaker bound.

Pairs-free selection helps where the seeds spread and has nothing to do where they do not. On SNARE-seq the seeds range
widely (12-seed mean 0.233, standard deviation 0.137) and the S1-selected seed is 0.149, within 0.005 of the best seed
by truth (0.144) and next to the 0.143 oracle, with S1 and truth agreeing at Spearman 0.82. On PBMC the search is
already near the oracle and the seeds barely move (mean 0.0895, standard deviation 0.004); there is no good seed to pick,
and the S1-selected seed (0.096) sits a touch above the mean rather than below it. We registered PBMC as the case where
selection should not apply, and it did not; this is a confirmation that S1's lever is seed spread, not a win we can claim
on PBMC. So selection helps on two of the three single-cell pairs, the two with real spread, and the third is already
solved.

A correction on the type test. We registered the probe as a minimum held-out predictability over each modality's top
five principal components, with a low minimum meaning a misleading axis. That exact rule flagged SNARE-seq as the
misleading-axis type, because its fourth and fifth principal components (about 3 to 5 percent of the variance each) are
not predictable from the other modality. The registered removal control contradicts the flag: removing the top variance
component hurts rather than helps (seed mean 0.259 against a matched baseline of 0.198), and it destroys the agreement
between S1 and truth (Spearman falls from 0.83 to 0.09), which is what you see when the top component is shared signal,
not a nuisance. So SNARE-seq has no removable misleading axis; it is the seed-variance type, like CITE-seq and PBMC. The
lesson is that the rule should read high-variance components, not any of the top five. In the long-caption case the
misleading direction is a dominant one (about 14 percent of the variance with held-out predictability near 0.16),
whereas the single-cell top components are predictable at 0.82 to 0.97. We mark this refinement post-hoc: it was found
after the registered rule mis-fired, and it needs confirming on more pairs before the type test can be called validated.
For now it is a promising diagnostic, not a settled one.

Among their partially aligned scientific pairs, then, the ones whose failure is seed variance can be improved by
pairs-free selection, and the three single-cell pairs their loaders support are all of this type. We state the general
claim with the post-hoc caveat on the type test and the three pairs it rests on.

## 7. Practical recommendations for unpaired alignment

For an author building or reporting an unpaired alignment method, the measurements above suggest a short routine.

First, report a true-pair oracle alongside each unpaired FOSCTTM. It is a closed-form Procrustes fit on held-out true
pairs and costs almost nothing. It separates a pair with no shared geometry from a pair whose geometry is shared but
whose search fails, and those two call for opposite responses. A pair at chance with an oracle also at chance is a
geometry problem; a pair at chance with a good oracle is a search problem worth more effort.

Second, when the oracle says a rotation exists but the search misses it, run the type test. Check whether one
high-variance component of either space is unpredictable from the other (a misleading axis), and read the seed spread of
the pairs-free self-score. These decide whether selection or re-initialization is the right lever. Read high-variance
components, not any of the top few: our first rule, a minimum over the top five, mis-flagged SNARE-seq on a low-variance
direction, so treat the type test as a diagnostic to confirm and back it with a removal control.

Third, for the seed-variance type, select runs by the pairs-free self-score instead of averaging over seeds. On CITE-seq
this recovered the best seed by truth and turned a reported 0.225 into a selected 0.089; on SNARE-seq it turned 0.209
into a selected 0.149, next to the oracle. Reporting the selected run, with the score that selected it, is more honest
than an average that mixes good and failed runs, and it needs no labels.

Fourth, for the misleading-axis type, do not rely on axis removal or iterate selection alone off the corpus where they
happen to work. A better initialization is the lever that cleared the bar in our measurements: a map transferred from
another corpus, or a modest number of true pairs. A free within-modality pivot through a second encoder gets close and
deserves a look as a no-image-pair option.

Fifth, treat a low CKA as a prediction about the search, not about the geometry. It correctly says the unpaired search
will struggle, and it correctly flags where to put effort, but it does not say a rotation is absent. The oracle says
that.

## 8. Limitations

The single-cell results are three pairs of 1,000 to 2,400 cells and one aligner configuration, their defaults. The
seed-selection result now covers all three: it helps on the two with seed spread (CITE-seq and SNARE-seq) and has
nothing to select on the already-solved third (PBMC). Three pairs is still a small base, and S1 should be confirmed on
more before it is called a general selector. The type test is a diagnostic, not a validated rule: our registered form
mis-flagged SNARE-seq, and the high-variance refinement that fixes it is post-hoc and needs confirming. Everything here
runs on our reimplementation of their pipeline at commit `fdfad84`; any difference from their numbers would come from
that, though the single-cell canaries and the vision-language reproductions in the first note match them closely. The
search-initialization headline arms in Section 5 are measured over three seeds; the negative-control arms (cumulative
axis search, iterate selection) are single-seed. Two biological pairs that Schnaus et al. report, human against mouse
single-cell RNA and histology against expression, need external downloads and pipelines and are deferred. The text-pivot
arm assumes a second same-modality encoder is admissible in their unpaired setting, which is a scoping question we flag
rather than resolve.

## 9. Related work

This note builds directly on Schnaus et al., who establish that shared geometry predicts unpaired alignment, provide
the aligner and the FOSCTTM protocol we use, and state the two open problems this note addresses. Their earlier work
(It's a (Blind) Match!, CVPR 2025) casts unpaired vision-language correspondence as a quadratic assignment and notes
that mutual k-NN, CKA and Gromov-Wasserstein matching are special cases of it; the oracle and the pairs-free score here
sit on top of that same matching machinery. The idea of translating representations across spaces with no pairs,
through a shared latent and a non-orthogonal decoder, appears in vec2vec (Jha et al., 2025). Unpaired alignment by
matching internal similarities has a long history in the Wasserstein-Procrustes and Gromov-Wasserstein literature,
including Gromov-Wasserstein alignment of word embeddings (Alvarez-Melis and Jaakkola, 2018) and adversarial
map-then-refine translation (MUSE; Conneau et al., 2018). Our contribution against this background is not another
matcher. It is a separation of alignability from searchability, a diagnostic for the failure type, and a pairs-free
selection that improves the seed-variance type, measured across three single-cell pairs.

---

## Appendix A. Receipts

Every scored number above comes from a committed JSON receipt under `experiments/results/`, produced with their
library at commit `fdfad84`. The table lists the experiment identifier, the receipt, and the numbers it backs.

| id | what it measures | receipt(s) | key numbers |
|---|---|---|---|
| E8 | CITE-seq: oracle, 12-seed baseline, pairs-free selection, axis probe, axis removal | `results/e8_single_cell/e8_merged_summary.json`; shards `e8_citeseq_remove{0,1}_s*-2026102*.json`; `experiments/e8_single_cell/{FINDINGS,NOTES}.md` | canary CKA 0.961, 5-seed mean 0.221 / sd 0.132; oracle orth 0.0727, lin 0.0741; 12 seeds mean 0.184, sd 0.095, min 0.089, max 0.439; S1-selected seed 0.0893; Spearman(S1,-FOSCTTM) 0.839 (across seeds), 0.823 (pooled iterates); iterate-within-seed 0.18369 vs 0.18372; top-5 PC cross-modal held-out R-squared 0.82-0.95 both ways; top-1 axis removal (6 seeds) mean 0.337 vs matched baseline 0.200, S1-selected 0.360 vs 0.098 |
| E7 | long-caption search initialization: pivot, transfer, few pairs, axis search, iterate and seed selection | `results/e7_search_init/e7_arm{A,B,C,D,E}-*.json`; `experiments/e7_search_init/{FINDINGS,NOTES}.md` | text-pivot (3 seeds): text-to-text 0.0002, compose (no image-caption pairs) 0.170±0.055 / 0.172±0.026, image-to-text control (ceiling) 0.139±0.051 / 0.136±0.028, refine-from-pivot hurts 0.182 / 0.199; transfer direct 0.107±0.013 / 0.100±0.010, transfer+refine 0.078±0.008 / 0.051±0.007, transfer axis-kept 0.489 / 0.486; few pairs (corpus A) 0.462 / 0.368 / 0.282 / 0.109 / 0.085, (corpus B) 0.450 / 0.260 / 0.213 / 0.152 / 0.100 at k=1/5/10/50/100; cumulative axis search (seed 0) S1-selected 0.464 (A) / 0.354 (B); S1 seed selection 0.396 vs mean 0.366 (A) / 0.502 vs mean 0.466 (B); oracle 0.010 / 0.007 (E6b) |
| E9 | PBMC and SNARE-seq: oracle, axis probe, 12-seed selection, SNARE-seq removal control | `results/e9_single_cell_more/e9_merged_summary.json`; shards `e9_{pbmc,snareseq}_remove{0,1}_s*.json`; `experiments/e9_single_cell_more/{FINDINGS,NOTES}.md` | SNARE-seq: CKA 0.855 (paper 0.86), 5-seed canary 0.178 (0.209), oracle orth 0.143 / lin 0.144, 12 seeds mean 0.233 sd 0.137 min 0.144 max 0.652, S1-selected 0.149 (best 0.144), Spearman 0.818, top-1 removal control 0.259 vs matched 0.198 with Spearman 0.83->0.09, registered rule min top-5 R-squared -0.17 (mis-flag), high-variance PC1-3 R-squared 0.62-0.92; PBMC: CKA 0.898 (0.90), 5-seed canary 0.088 (0.089) LTA 0.945 (0.942), oracle orth 0.074 / lin 0.078, 12 seeds mean 0.0895 sd 0.004, S1-selected 0.096 (best 0.082), Spearman 0.32, min top-5 R-squared 0.61 (variance-type) |

Background numbers from the first note (`response.md`, draft 3.2), cited here and not re-measured: long-caption
one-axis removal 0.415 to 0.038 (first corpus), 0.479 to 0.391 and 0.474 to 0.478 (the two corpora recovered here by a
better initialization); true-pair oracle for generative pooling 0.009 / 0.014 / 0.010 (none removed) and 0.007 / 0.010
/ 0.007 (axis removed) across the three long-caption corpora; forward transfer 0.409 to 0.022 to held-out short-caption
images; eight pairs-free restarts off the first corpus reaching only 0.280 / 0.341. Their reported values (CITE-seq
0.225, standard deviation 0.13, CKA 0.96; PBMC 0.089 plus or minus 0.003, CKA 0.90; SNARE-seq 0.209 plus or minus 0.034,
CKA 0.86; scientific CKA R-squared 0.69) are from arXiv 2610.09411 v2 (CITE-seq lines 6012-6016, 779 and 790; PBMC and
SNARE-seq from their Tables 4, 9 and 12), and the two open-problem quotations from lines 994 and 777.

## Appendix B. Status and integrity

**Their code, unchanged.** The split, preprocessing, aligner, initialization and FOSCTTM come from their library at
commit `fdfad84`. The only thing we change per arm is the initialization, the number of true pairs, or the post-hoc
selection.

**Preregistration.** The CITE-seq hypotheses (a rotation exists; the canary matches; pairs-free seed selection beats
the mean; the axis-removal control) were frozen before any scored run in `experiments/e8_single_cell/`. The PBMC and
SNARE-seq hypotheses, including the type rule and the removal control, were frozen in
`experiments/e9_single_cell_more/PREREG.md` before any scored run; the high-variance refinement of the type test was
found after the registered rule mis-flagged SNARE-seq and is labelled post-hoc in Section 6. The search-initialization
hypotheses and the single success bar (below 0.10 on both corpora) were frozen in
`experiments/e7_search_init/PREREG.md` before any scored run. Post-hoc results, where present, are labelled.

**Seeds.** CITE-seq is measured over twelve seeds for the selection result and six for the axis-removal control. PBMC
and SNARE-seq are each measured over twelve seeds for selection, and SNARE-seq over six for its removal control. The
search-initialization headline arms (transfer-then-refine, about 100 pairs, the text pivot and its control) are measured
over three seeds; the negative-control arms (cumulative axis search, iterate selection) are single-seed.

**Nothing sent.** This note has not been sent, posted, or emailed to anyone. No one was contacted. The intended path,
when the work is complete, is a short note to the authors with the CITE-seq and search-initialization code and the JSON
receipts it cites.
