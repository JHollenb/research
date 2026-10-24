# PREREG - E9: do E8's CITE-seq results generalize to the other single-cell pairs their loaders support?

Frozen before any Beast job ran the aligner on PBMC or SNARE-seq. Extends E8 (CITE-seq). Scores the registered text
literally; any threshold/scorer change after seeing data is labelled POST HOC.

## Question

E8 found, for Schnaus et al.'s (arXiv 2610.09411 v2) worst "partially aligned" pair CITE-seq (scRNA vs ADT, CKA 0.96,
FOSCTTM 0.225 +/- 0.13): (a) a rotation EXISTS (true-pair orth-Procrustes holdout 0.073); (b) the failure is a SEARCH
failure (seed mean 0.184, range 0.089-0.439); (c) the pairs-free self-score S1 selects the best seed by truth (0.089),
Spearman(S1,-FOSCTTM) 0.84; (d) NO nuisance axis (every top-5 PC cross-modal predictable, R2 0.82-0.95), so it is a
"variance type", unlike long-caption text/gen which is a "nuisance type". Does this generalize to the other single-cell
pairs their own `modalities/single_cell/prepare.py` loaders support with no external pipeline?

Loadable pairs (their `prepare.py` @ fdfad84, checksummed SCOT/SCOT+ downloads, no external pipeline):
- PBMC: scRNA (pca50) vs scATAC (topics50), 2407 cells. Paper (Table 9 / Table 12): FOSCTTM 0.089 +/- 0.003 (vs SCOT+
  0.121 +/- 0.027), LTA 0.942, CKA 0.90. Run via `domain_specific.py` (same `run_alignment` as the others).
- SNARE-seq: scRNA (pca10) vs scATAC (lsi19), 1047 cells, 4 cell lines. Paper (Table 4 / Table 12): FOSCTTM 0.209 +/-
  0.034 (reported as 0.21 +/- 0.03), CKA 0.86. Run via `other_domains.py` (same driver as CITE-seq).
The other pairs in Table 12 need external pipelines/downloads and are OUT (documented below): human<->mouse scRNA (CZ
CELLxGENE Census), histology<->expression (HEST + GPU tiles), and the non-single-cell pairs (galaxy, MLIP, MS/MS,
tissue-CT/MRI, MEG, fMRI, Cell Painting) which are other modalities, not single-cell loaders.

## Setup (reproduced exactly from their code @ fdfad84)

- Data: built locally from the checksummed SCOT (SNARE) / SCOT+ (PBMC) raw files, sha256 verified against their
  `prepare.py` CHECKSUMS (all MATCH, laptop receipts in NOTES.md), tensors identical to `prepare_pbmc` /
  `prepare_snare_seq`, rsynced to Beast storage (sha256 re-verified Beast==laptop). No model, no fitting in prep.
- Preprocessing: their `embeddings.load_rows` (each cell unit-normalized), then the aligner center+normalizes.
- Aligner: their `WassersteinProcrustes` defaults C=30, S=30, b=10000, R=100 (`build_aligner("ours")`; confirmed no
  per-dataset override in methods.py).
- Protocol (identical for all three pairs; confirmed in alignment.py `run_alignment` + `evaluate`): training is a
  `disjoint_split(n, Randomness(seed))` into 50/50 UNPAIRED cells; the SAME randomness object (already advanced by the
  split) is passed into `aligner.fit` (the E8 reproduction bug, reproduced here); evaluation uses a FRESH
  `Randomness(seed)` over ALL paired cells (holdout=0). Seeds from `derive_seeds(42, N)`.
- The logged aligner is a verbatim copy of their `_fit` plus a weight trajectory; a frozen synthetic smoke asserts its
  final weight equals the stock aligner's to < 1e-5 for BOTH geometries (square 50x50 and rectangular 10->19), so
  reproduction is exact. (Smoke PASSED locally on synthetic data: logged_vs_stock 0.0, oracle 0.0, true-rot S1 ~1.)

## Hypotheses (per pair)

- H1 (rotation exists): oracle orth-Procrustes holdout FOSCTTM far below the paper's unpaired mean (predict <= 0.10 for
  both; both pairs have CKA >= 0.86, higher than CITE-seq's reproduced oracle setting).
- H2 (search failure + selection): per-seed last-iterate FOSCTTM varies as the paper reports; S1 is positively
  associated with alignment quality (Spearman(S1,-FOSCTTM) > 0 across seeds); S1-selected seed <= mean-over-seeds.
  NOTE: PBMC's paper sd is 0.003 (near-zero spread). A selection method cannot beat the mean when there is nothing to
  select; so for a pair with observed sd < 0.02 the selection test is declared N/A (not a failure) and the finding is
  "already near-solved, no spread for S1 to exploit".
- H3 (type test / nuisance axis): for each pair, is there a top PC of one modality with high variance share but low
  held-out cross-modal R2 (nuisance type) or not (variance type)? Prediction: both PBMC and SNARE-seq are VARIANCE type
  (no nuisance axis; min top-5 cross-modal R2 >= 0.30 both ways), like CITE-seq and unlike long-caption text/gen.
  Cross-pair claim: S1-selection usefulness tracks seed spread, and no high-CKA biology pair shows a nuisance axis.

## Primary outcomes and PASS/FAIL (per pair)

- P1 (oracle / Q1): oracle orth holdout FOSCTTM. PASS "a rotation exists" if < 0.10; AMBIGUOUS 0.10-0.20; FAIL if >=
  0.20. Linear-map oracle reported alongside; lin << orth would mean a non-orthogonal residual.
- P2 (reproduction canary): mean last-iterate FOSCTTM over the 5 paper seeds within 0.04 of the paper mean AND CKA on
  all cells within 0.04 of the paper CKA. For PBMC additionally LTA within 0.04 of 0.942. If the canary fails, the
  reproduction is wrong and nothing else is reported as a finding for that pair.
- P3 (selection / Q2): if observed sd(FOSCTTM over 12 seeds) >= 0.02: PASS if S1-selected-seed FOSCTTM <=
  mean-over-seeds AND Spearman(S1_last,-FOSCTTM_last) across seeds > 0.3. If sd < 0.02: report N/A (no spread), PASS the
  weaker check that S1-selected-seed FOSCTTM <= mean + 0.01 (selection does not hurt).
- P4 (type test / Q3): report the top-5 PC held-out cross-modal R2 table both ways + depth correlation. Classify each
  pair variance-type (min top-5 R2 >= 0.30 both ways) or nuisance-type (any < 0.30). A removal arm is run ONLY if a
  pair is classified nuisance-type (then: removal PASS if top-1-axis removal lowers S1-selected or mean FOSCTTM by >=
  0.02). Cross-pair: tabulate (sd, type, S1-selection gain) for CITE-seq (E8, cited), PBMC, SNARE-seq and state whether
  type + spread predict S1-selection usefulness.

## Kill condition

Per pair: if the oracle orth holdout FOSCTTM is itself >= 0.20 (no rotation aligns even the true pairs on a holdout),
the "search failure" framing is dead for that pair; report that and stop (no removal, no extra seeds). Likewise if the
reproduction canary (P2) fails, stop and debug the reproduction before claiming anything for that pair.

## Nulls / controls / canaries

- Canary P2 (match the paper mean, CKA, and PBMC LTA on the 5 paper seeds).
- Synthetic smoke (in-process, pre-real, aborts on failure), for BOTH the square and rectangular geometry: a known
  (semi-)orthogonal map is recovered by the oracle (FOSCTTM < 0.05), its S1 > 0.9, logged aligner == stock (< 1e-5).
- Linear-map oracle (ridge) next to the orth oracle.
- Oracle uses a DISJOINT holdout (fit 50%, eval the other 50%), so it cannot memorize.
- min-FOSCTTM iterate / best-seed-by-truth reported only as labelled references (they use truth), never as the
  pairs-free selection result. S1 selection never looks at FOSCTTM.
- PBMC LTA per seed reproduces their `evaluate()` randomness sequence exactly (subset -> retrieval shuffle -> LTA
  shuffle); the LTA job re-derives the same foscttm to confirm the sequence (`foscttm_last_with_lta_check`).

## Smoke checks (frozen)

Synthetic (both geometries) as above (PASSED locally). Then on Beast a 2-seed real job per pair (`--seed-hi 2`) runs
the full config first; the canary and oracle are printed before the 12-seed sweep is submitted.

## Pre-registration looks (local runs that touched real models / real data)

None that ran the aligner. The only local real-data touch is building the PBMC/SNARE .pt tensors from the checksummed
SCOT/SCOT+ raw files (download + transpose/convert + label indices, no model, no analysis, no alignment) per HARD RULE
6, in an isolated venv with `-I`. All sha256 verified (MATCH). The synthetic smoke ran on synthetic data only. No
aligner was run on PBMC or SNARE-seq locally. All scored alignment runs on Beast via mrun, priority 75.

## Deferred / out of scope (documented)

- human <-> mouse scRNA (0.34): needs the CZ CELLxGENE Census (`cross_species.py`, ~1.3 GB + cellxgene/tiledbsoma).
- histology <-> expression (0.37): needs HEST-Benchmark + H-Optimus-0 GPU tile embedding (external pipeline).
- All non-single-cell Table 12 pairs: other modalities, not single-cell loaders.
