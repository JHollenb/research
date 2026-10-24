# PREREG - E8: the CITE-seq "partially aligned" tier (scRNA vs ADT)

Frozen before any job touched real single-cell data. Contribution-map item #3 (plus #4 oracle, NEW-A/#2 selection).
Scores the registered text literally; any threshold/scorer change after seeing data is labelled POST HOC.

## Question

On Schnaus et al.'s (arXiv 2610.09411 v2) weakest "partially aligned" scientific pair -- CITE-seq (scRNA vs ADT),
which has the highest CKA of all 14 pairs (0.96) yet FOSCTTM 0.225 +/- 0.13, their largest seed variance:

1. Does a rotation exist? (true-pair orthogonal Procrustes oracle FOSCTTM on a disjoint holdout)
2. Is the failure a search failure? Does per-seed FOSCTTM vary as they report (sd ~ 0.13), and can the pairs-free
   score S1 (mean cosine of Hungarian-matched pseudo-pairs) select the good seeds / iterates vs their mean-over-seeds
   and last-iterate?
3. Is there a dominant technical nuisance axis (sequencing depth / library size) that one modality's top PCs carry
   and the other cannot predict (held-out cross-modal R2 of each top PC)? Does removing it (pairs-free) help?

## Setup (reproduced exactly from their code @ fdfad84)

- Data: `modalities/single_cell/prepare.py` CITE-seq, 1000 cells, 25 genes (rna) vs 25 surface proteins (adt).
  Built locally from the two checksummed SCOT+ CSVs (sha256 verified against their CHECKSUMS), transposed to
  [1000,25] float32, same as `prepare_cite_seq`. rsynced to Beast storage. No model, no fitting in prep.
- Preprocessing: their `embeddings.load_rows` (each cell unit-normalized), then the aligner center+normalizes.
- Aligner: their `WassersteinProcrustes` defaults C=30, S=30, b=10000, R=100 (`methods.build_aligner("ours")`).
- Split (their `experiments/other_domains.py` Pair for CITE-seq, `separate_corpora=False`, holdout=0): training is a
  `disjoint_split` into 500/500 UNPAIRED cells; evaluation is all 1000 PAIRED cells (their comment: "evaluation uses
  all paired items, including the training items"). Seeds from their `derive_seeds(42, N)`.
- The logged aligner is a verbatim copy of their `_fit` plus a weight trajectory; a smoke check asserts its final
  weight equals the stock aligner's to < 1e-5 (identical randomness), so reproduction is exact.

## Hypotheses

- H1 (rotation exists): oracle orth-Procrustes holdout FOSCTTM is far below their 0.225 (predict <= 0.10), i.e. a
  single rotation aligns the true pairs well, so the geometry is shared and the failure is in the search.
- H2 (search failure + selection): per-seed last-iterate FOSCTTM has sd near 0.13; S1 is positively associated with
  alignment quality (Spearman(S1, -FOSCTTM) > 0 across seeds and pooled over iterates); S1-selected seed and
  S1-selected iterate beat the mean-over-seeds / last-iterate.
- H3 (nuisance axis): at least one top PC of one modality has high variance share but near-zero held-out cross-modal
  R2 from the other modality, and correlates with the depth proxy; removing the top axis (pairs-free) lowers FOSCTTM
  (mean and/or S1-selected).

## Primary outcomes and PASS/FAIL

- P1 (oracle / Q1): oracle orth holdout FOSCTTM. PASS "a rotation exists" if < 0.10; AMBIGUOUS 0.10-0.20; FAIL
  (no good rotation, geometry not alignable) if >= 0.20 (at/above their achieved mean).
- P2 (reproduction canary): mean last-iterate FOSCTTM over the 5 paper seeds within 0.06 of 0.225 AND sd > 0.05
  (their sd 0.13) AND CKA on all 1000 paired cells within 0.04 of 0.96. If the canary fails, the reproduction is
  wrong and nothing else is reported as a finding.
- P3 (selection / Q2): S1-selected-seed last-iterate FOSCTTM < mean-over-seeds FOSCTTM, AND
  Spearman(S1_last, -FOSCTTM_last) across seeds > 0.3. Secondary: S1-selected iterate < last-iterate on average.
- P4 (axis / Q3): report the top-PC held-out cross-modal R2 table + depth correlation (descriptive). Removal PASS if
  top-1-axis removal lowers the S1-selected (or mean) FOSCTTM by >= 0.02 vs no removal; else removal has no effect.

## Kill condition

If the oracle orth holdout FOSCTTM is itself >= 0.20 (no rotation aligns even the true pairs on a holdout), the
"search failure" framing is dead for CITE-seq: the pair is genuinely only coarsely alignable and the nuisance-axis /
selection story does not apply. Report that as the result and stop (do not chase removal or extra seeds). Likewise if
the reproduction canary (P2) fails, stop and debug the reproduction before claiming anything.

## Nulls / controls / canaries

- Canary P2 above (match their mean, sd, CKA on the paper's 5 seeds).
- Synthetic smoke (in-process, pre-real, aborts on failure): known 25-dim rotation recovered by the oracle
  (FOSCTTM < 0.05), S1 of the true rotation > 0.9, logged aligner == stock aligner (< 1e-5).
- Linear-map oracle (ridge) reported next to the orth oracle: if lin << orth, the residual misalignment is a
  non-orthogonal (scaling/shear) effect, not a missing rotation.
- Oracle uses a DISJOINT holdout (fit 500 true pairs, eval the other 500), so it cannot trivially memorize.
- min-FOSCTTM iterate / best-seed-by-truth are reported only as labelled references (they use true pairs), never as
  the pairs-free selection result.
- S1 selection never looks at FOSCTTM; it is computed from pseudo-pairs on the training sets only.

## Smoke checks (frozen)

Synthetic rotation recovery + S1 + logged==stock, as above. Then on Beast a 2-seed real job (`--seeds 2`) runs the
full config first; the canary and oracle are printed before the 20-seed job is submitted.

## Pre-registration looks (local runs that touched real models / real data)

None. The only local real-data touch is building the CITE-seq .pt tensors from the two checksummed CSVs (download +
transpose, no model, no analysis) per HARD RULE 6 (download/prepare on the laptop). The synthetic smoke was run
locally on synthetic data only. No aligner was run on CITE-seq locally. All scored alignment runs on Beast via mrun.

## Deferred (documented, not run)

- human vs mouse scRNA (0.338): needs the CZ CELLxGENE Census (`cross_species.py`, ~1.3 GB download + the
  `cellxgene`/tiledbsoma env); not on their HF embeddings repo. Not cheap -> deferred.
- histology vs expression (0.369): needs 13.9 GB HEST-Benchmark + H-Optimus-0 tile embedding (external GPU pipeline).
  Fails the "no external pipeline" test -> out of scope.
