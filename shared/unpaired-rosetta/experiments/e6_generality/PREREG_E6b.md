# E6b (X01-schnaus-generality, fix-diagnosis addendum) pre-registration

Written 2026-10-22 22:25 PDT (2026-10-23T05:25Z), as an addendum to `PREREG.md`
(sha256 `ac2259bdd4b5c12c2c548a280683722cb8595422d7c030f9b879010c2a982f4c`, unchanged). Written before any oracle
FOSCTTM, any drop-k>=2 FOSCTTM, any gen-pc0 restart beyond seeds 0-2, or any SPC->COCO transfer number touched this
builder. Theme C19-cross-model-alignment. Response under revision: `../../response.md` (draft 3), section 3.6.

## Why this addendum

E6 (frozen, measured) established: Qwen3-8B generative pooling of long captions carries a dominant non-visual top
PC on SPC, DCI and DOCCI (variance share 13.8 / 19.4 / 22.2 %, held-out image R^2 0.16 / 0.052 / 0.052), absent on
short COCO captions (R^2 0.899); and under Schnaus et al.'s unpaired `WassersteinProcrustes`, projecting that one
axis out **rescues** SPC holdout FOSCTTM (0.415 -> 0.038, 3 seeds) but **not** DCI (0.479 -> 0.391, 3 seeds) or DOCCI
(0.474 -> 0.478, 3 seeds), while Qwen3-Embedding reaches 0.093 / 0.096 unpaired on the same corpora. Receipts in
`../results/e6_generality/`. The response reports this honestly as "the one-axis fix is SPC-specific".

The owner's rule is asymmetric skepticism on a negative: before the response says "the one-axis fix is SPC-specific",
find out WHY the fix fails off SPC. The fix could fail for two very different reasons:

- **Search-limited.** After removing the scaffold axis the geometry *is* alignable by a single rotation, but the
  unpaired `WassersteinProcrustes` (geometric k-means init + Sinkhorn/Hungarian refinement) lands in a bad local
  optimum off SPC. Then the obstacle is the *search*, not the geometry.
- **Geometry-limited.** Even with the true correspondence, one rotation cannot bring the pc0-removed gen cloud onto
  the image cloud on DCI/DOCCI. Then the obstacle is the *geometry* (the shared structure is not a rotation apart),
  and removing one axis is simply not enough.

A true-pair **oracle** separates these: it measures the best FOSCTTM a single rotation can reach *given the true
pairs*, i.e. the ceiling the unpaired search is trying to climb to.

## Question

Is the failure of the one-axis fix off SPC search-limited or geometry-limited, and what is the residual obstacle?

## Data and protocol

Same data and load path as E6: `schnaus/unpaired-rosetta-embeddings`, commit `fdfad84`, loaded by their
`unpaired_rosetta.embeddings.load_rows` / `reduce_texts`; vision `dinov2_vit-b14@224_mean` (768-d); language
`qwen3-8b-gen_...769` (gen, 4096-d) and `qwen3-embedding-8b` (4096-d). Corpora: StanfordParagraphCaptioning (SPC,
19561 rows), DenselyCaptionedImages (DCI, 7805), DOCCIDataset (DOCCI, 14847). Holdout = last 2000 rows (E6-identical).
All execution on Beast via mrun, CPU jobs, <=4 threads each (`OMP/MKL/torch` pinned), right-sized RAM.

## (1) DECISIVE: true-pair oracle ceilings (frozen)

For each cell below, train on the **true pairs** at indices `arange(0, n-2000)` (vision row i paired with language
row i), evaluate holdout FOSCTTM on the last 2000 rows with their `retrieval_metrics` (same shuffle seed 0). Two
oracle maps, both using only the training rows (never the holdout) to fit:

- **Oracle orthogonal Procrustes** (their aligner's map class, with the true correspondence instead of the learned
  one): `mean_x, mean_y` = training means; `Xc = center_and_normalize(train_x, mean_x)`,
  `Yc = center_and_normalize(train_y, mean_y)`; `W = polar(Xc^T Yc)` (their `unpaired_rosetta.linalg.polar`, the
  orthogonal-Procrustes optimum `argmax_{W in St} Tr(Xc W Yc^T)`). This is the exact ceiling for the rotation-only
  family their method searches over.
- **Oracle unconstrained linear** (ridge): `W = (Xc^T Xc + lambda I)^-1 (Xc^T Yc)`, `lambda = 1e-3` (negligible
  vs the eigenvalues of `Xc^T Xc`, whose trace = m; reported in the receipt). The best linear map X->Y under least
  squares; retrieval by `(Xc W) @ Yc^T`.

Cells: gen `none`, gen `pc0`, qwen3-embedding `none`, each on SPC, DCI, DOCCI (9 cells x 2 maps = 18 FOSCTTM).
`pc0` removal mirrors E6's `Deflated`: `basis = principal_axes(train_y, 1)`; project it out of both `train_y` and
`val_y` (raw rows) before centering. The oracle sees the true pairs and all `n-2000` training rows; it is an upper
bound (ceiling), by design stronger than each unpaired disjoint half.

### Canaries (frozen; if either fails, the oracle is broken and no branch is interpreted)

- **C1 (ceiling real, corpora alignable).** qwen3-embedding `none` oracle-orthogonal FOSCTTM <= 0.05 on all three
  corpora and <= its unpaired FOSCTTM (SPC ~0.019, DCI 0.093, DOCCI 0.096). An encoder the unpaired aligner already
  aligns must align at least as well with the true pairs.
- **C2 (SPC fix reproduced).** gen `pc0` oracle-orthogonal FOSCTTM <= 0.10 on SPC (matching the measured 0.038
  unpaired rescue), and gen `none` oracle on SPC clearly worse than gen `pc0` oracle (the scaffold axis blocks even
  the true-pair rotation).

### Branch criterion (frozen) — let O = gen-`pc0` oracle-orthogonal FOSCTTM

- **SEARCH-LIMITED** if O <= 0.15 on BOTH DCI and DOCCI (near the qwen3-embedding ceiling) AND clearly below the
  measured unpaired gen-pc0 (DCI 0.391, DOCCI 0.478). Conclusion: the pc0-removed geometry is rotation-alignable;
  the unpaired search fails off SPC. Then run **(2)**.
- **GEOMETRY-LIMITED** if O >= 0.30 on BOTH (near chance 0.5, far above the control ceiling). Conclusion: one
  rotation cannot align gen-pc0 even with the true pairs; one axis is not the whole obstacle. Then run **(3)**.
- **MIXED/PARTIAL** otherwise (0.15 < O < 0.30 on either, or the two corpora disagree): report the oracle numbers as
  the finding and run the follow-up(s) the pattern points to, each labelled, without forcing a single verdict.

In every branch, the oracle-**linear** ceiling is reported as the "is any linear map enough" control: if linear is
low where orthogonal is high, the residual obstacle is the orthogonality (isometry) constraint — the shared signal
is linear but not a rotation, which is exactly the rotation-ceiling theme of response.md section 4.

## (2) If SEARCH-LIMITED: can an unpaired procedure recover it?

Re-run their `WassersteinProcrustes` (default hyperparameters, as E6: clusters 30, restarts 30, batch 10000,
iterations 100) on gen with `pc0` removed, on DCI and DOCCI, at seeds 0-7 (8 independent restarts of the whole
pipeline; seeds 0-2 already measured in E6, seeds 3-7 new). Select ONE restart per corpus by the **pairs-free S1**
(mean cosine of Hungarian-matched pairs on the training rows) only — true-pair FOSCTTM never enters selection.
Report: the S1-selected restart's FOSCTTM, the best FOSCTTM over restarts (labelled "restart-oracle", not
pairs-free), and whether argmax-S1 lands near the oracle ceiling. PASS (search recoverable) if the S1-selected
restart's FOSCTTM is within 0.05 of the oracle-orthogonal ceiling on both corpora.

## (3) If GEOMETRY-LIMITED: what is the residual obstacle?

Drop-k FOSCTTM ladder under their aligner (default hyperparameters, seed 0): deflate the top k language PCs
(`basis = principal_axes(sy, k)`, first k columns, estimated on the unpaired training half, as E6's gate) for
k = 0,1,2,3,4, on gen, for SPC, DCI, DOCCI. k=0 is `none`, k=1 is `pc0` (both already measured at seed 0; re-run in
one job for a consistent ladder). Prediction (frozen): because the axis probe already shows gen PCs 1-3 are visual
(held-out image R^2 0.47-0.61 on DCI/DOCCI, vs 0.05 for PC0), dropping beyond k=1 removes shared signal and does
not lower FOSCTTM further (monotone non-improving past k=1, i.e. no k in 2..4 beats k=1 by > 0.03 on either corpus).
Report the ladder and read the residual obstacle against the oracle-linear ceiling from (1).

## (4) SECONDARY (unconditional): finish P6, SPC->COCO transfer

Their headline validation fits a map on one corpus and evaluates on held-out COCO-val. Fit `WassersteinProcrustes`
(defaults) on SPC gen (two disjoint unpaired halves of SPC minus the last 2000, E6-identical), evaluate holdout
FOSCTTM on a random 5000-row subset of COCO-val gen the map never saw. Two arms: `raw` (their pipeline) and `drop1`
(the top PC of the SPC *training* language rows projected out of every language row, train and eval). Descriptive,
no directional bar frozen (per E6 P6: COCO captions are short, gen may already work). The COCO gen file is 13.9 GB
float32 `[40504, 21, 4096]`; load the 5000 eval rows with a **chunked** `reduce_texts` (gather + normalize + nanmean
in row-blocks of <= 2000, concatenating only the reduced `[rows, 4096]` outputs) so peak RAM stays ~20 GB. Declare
RAM 24000 MB.

## Smoke checks (frozen; run in-process first in each scored job; abort on failure)

Oracle job: (a) synthetic recovery — X ~ N(0, I) `[4000, 768]`, R a random semi-orthogonal `[768, 4096]`,
Y = center_and_normalize(X) @ R; the oracle-orthogonal FOSCTTM on a 1000-row held-out split is < 0.02 (recovers a
known rotation); (b) `polar(Xc^T Yc)` is semi-orthogonal (`||W^T W - I_768|| < 1e-3`); (c) the ridge solve is finite;
(d) real rows load finite, unit-norm within 2e-2 (bf16 reduce tolerance, as E6), vision and language row counts
equal. Ladder / restart jobs reuse E6's frozen smoke_gate. Transfer job: the chunked `reduce_texts` of the first 64
COCO rows equals the library `reduce_texts` of those rows within 1e-4 (chunking is a no-op on the math).

## Seeds

The oracle is deterministic given the split (retrieval shuffle seed 0). Single seed. The drop-k ladder is seed 0
(matching the E6 seed-0 sweep it extends). The restart branch spans seeds 0-7 by design (the restarts ARE the
experiment). No extra seeds spent on arms that do not contribute.

## Pre-registration looks (local runs that touched real data before this addendum)

- Read tensor shapes/dtypes/row counts via `torch.load(mmap=True).shape` on Beast over ssh (metadata only): vision
  768-d bf16; gen/embedding 4096-d; SPC 19561, DCI 7805, DOCCI 14847, COCO 40504 rows; COCO gen `[40504, 21, 4096]`
  float32 13.9 GB. No fit, FOSCTTM, PC, CKA, R^2, variance share or S1/S2 computed anywhere before this addendum.
- Re-read the E6 receipts already on disk (the frozen E6 numbers quoted above). No new number computed.
- No real model or real-data analysis ran on the laptop; every E6b number runs on Beast via mrun.

## Scoring

The frozen text above is scored literally. The branch is chosen by the frozen criterion on the oracle result; any
scorer or threshold changed after seeing data is labelled POST HOC in NOTES.md. sha256 of `PREREG.md`,
`PREREG_E6b.md` and every shipped e6 python file is recorded in each job's receipt config (`manifest_sha256`).
