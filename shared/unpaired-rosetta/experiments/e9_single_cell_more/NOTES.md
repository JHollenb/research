# E9 single-cell MORE (PBMC + SNARE-seq) - NOTES (live state)

Plain version: E8 showed that CITE-seq (the paper's worst "partially aligned" pair) fails because the unpaired SEARCH
misses a rotation that exists, not because the geometry is unalignable; a pairs-free self-score (S1) picks the good
seeds; and there is no nuisance axis (it is a "variance type", unlike long-caption text). E9 asks whether this
generalizes to the other single-cell pairs their own loaders support: PBMC (scRNA vs scATAC, 2407 cells) and SNARE-seq
(scRNA vs scATAC, 1047 cells). Same code, same protocol, parametrized per pair. The interesting contrast: PBMC is
near-solved (paper 0.089 +/- 0.003, almost no seed spread) so S1 has nothing to select; SNARE-seq has modest spread
(0.209 +/- 0.034). The "type test": does each pair have a top PC the other modality cannot predict (nuisance type) or
not (variance type), and does type+spread predict whether S1 selection helps?

Status as of writing: code built; synthetic smoke PASSED locally for BOTH geometries (square 50x50 PBMC and rectangular
10->19 SNARE); PBMC+SNARE data built from checksummed SCOT/SCOT+ files and rsynced to Beast (sha256 verified
Beast==laptop); PREREG frozen; 2-seed smoke job submitted for each pair (QUEUED behind a busy Beast). No real-data
findings yet.

## Loadable pairs (MEASURED from their code)

Their `modalities/single_cell/prepare.py` @ fdfad84 supports exactly three paired single-cell pairs with checksummed
downloads and no external pipeline: CITE-seq (E8, done), PBMC, SNARE-seq. human<->mouse scRNA needs CZ CELLxGENE
Census (`cross_species.py`); histology<->expression needs HEST+GPU. All other Table 12 pairs are non-single-cell.

Paper numbers (MEASURED from schnaus_v2.txt):
- PBMC: Table 9 "ours" FOSCTTM 0.089 +/- 0.003 (SCOT+ 0.121 +/- 0.027), LTA 0.942 +/- 0.019; Table 12 CKA 0.90.
- SNARE-seq: Table 4 (refinement "ours") FOSCTTM 0.209 +/- 0.034 (= Table 12 0.21 +/- 0.03); CKA 0.86.
- CITE-seq (E8 reproduced): 0.225 +/- 0.13, CKA 0.96.

## Provenance (MEASURED)

- Their repo @ fdfad84 (confirmed `git log -1`).
- Raw files downloaded on laptop (isolated venv, `python -I`), sha256 verified against prepare.py CHECKSUMS -> ALL
  MATCH: PBMC/{rna_50pca_50topics.pkl, atac_50pca_50topics.pkl, adata.h5ad}, SNARE/{SNAREseq_rna_feat.npy,
  SNAREseq_atac_feat.npy, SNAREseq_rna_types.txt}. Prep script:
  /private/tmp/claude-501/-Users-jakeholl-domains/f7d2d6aa-a67f-4693-9e4e-270539ab32fe/scratchpad/e9_prep/prep_data.py
- Built tensors (exactly prepare_pbmc / prepare_snare_seq), sha256 (first16) verified Beast==laptop:
  PBMC/rna/pca50.pt fce8a3b33e9dd597 (2407,50); PBMC/atac/topics50.pt e2b28d4368265b9f (2407,50);
  PBMC/labels.pt 640361bee4787309 (2407, 7 classes);
  SNARE-seq/rna/pca10.pt 53ac06032b20a414 (1047,10); SNARE-seq/atac/lsi19.pt 00a57c381d64ca67 (1047,19);
  SNARE-seq/labels.pt 018c6a4161d45ab2 (1047, 4 cell lines).
  At beast:/mnt/usb-storage/unpaired-rosetta/storage/embeddings/{PBMC,SNARE-seq}/. Laptop raw+staging deleted.

## Exact reproduction (from their code)

- Protocol IDENTICAL for all three pairs (confirmed alignment.py run_alignment + evaluate): disjoint_split(n,
  Randomness(seed)) -> 50/50 unpaired; the SAME advanced randomness into fit (E8 bug, reproduced); evaluate uses fresh
  Randomness(seed) over ALL paired cells (holdout=0). SNARE/CITE via other_domains.py; PBMC via domain_specific.py but
  the same run_alignment. Aligner defaults C=30 S=30 b=10000 R=100 (no per-dataset override, confirmed methods.py).
- run.py is E8's run.py parametrized by `--pair {PBMC,SNARE-seq}` (dims/models per pair); handles rectangular maps
  (SNARE 10->19) via polar on a non-square cross-covariance (their St(d_X,d_Y)). PBMC additionally logs per-seed LTA
  reproducing their evaluate() randomness sequence exactly (`foscttm_last_with_lta_check` must equal `foscttm_last`).

## SMOKE (synthetic, local, MEASURED) - PASSED

synthetic_smoke for (d_x,d_y) in {(50,50),(10,19),(25,25)}: logged_vs_stock=0.0 (exact), synthetic_oracle_foscttm=0.0,
synthetic_true_rot_s1~0.99995 (reproduction exact; rectangular map handled).

## What each job computes (run.py) - same three measurements as E8

- canary: linear CKA on all cells (+ PBMC per-seed LTA, aggregated over the 5 paper seeds in analyze).
- oracle (Q1): true-pair orth Procrustes (+ ridge-linear) FOSCTTM on a disjoint 50/50 holdout.
- per seed: full trajectory; per iterate S1 (pairs-free Hungarian pseudo-pair cosine), S2, true FOSCTTM.
- selection (Q2): mean/sd/min/max last-iterate FOSCTTM over seeds; S1-selected seed+iter (pairs-free); best-by-truth
  (labelled); Spearman(S1,-FOSCTTM) across seeds and pooled over iterates.
- axis + type test (Q3): top-5 PC var share, held-out cross-modal R2 both ways, depth-proxy corr; verdict
  variance-type (min top-5 R2 >= 0.30 both ways) vs nuisance-type. Removal arm only if nuisance-type appears.

## SMOKE RESULTS (real seeds [0:2], full config, MEASURED) - both SUCCEEDED

Workers change speed only, not the result (logged==stock, and the aligner states workers are result-invariant), so the
smoke receipts ARE valid baseline data for seeds [0:2]; the baseline sweep therefore runs seeds [2:12] only and merges.

PBMC (job-87be96821f51, receipt e9_pbmc_remove0_s0_2-20261024T010900.json):
- smoke exact (logged_vs_stock 0.0). canary CKA_all 0.8975 (paper 0.90) -> within 0.04.
- 2-seed FOSCTTM 0.0840, 0.0915 (mean ~0.088; paper 0.089). LTA 0.9489, 0.9618 (mean ~0.955; paper 0.942) -> canary
  PASS. fos_check == fos_last (randomness sequence reproduced exactly).
- ORACLE orth 0.07368, lin 0.07826 -> both < 0.10 => P1 PASS, a rotation exists (<< paper 0.089).
- TYPE: variance (min top-5 cross-modal R2 = 0.6148). NO nuisance axis. No removal arm (per PREREG).
- SLOW: ~8-10 min/seed even at workers=8 (QAP on 50-dim, 1203 cells/side). Baseline sharded by 2 at workers=8.

SNARE-seq (job-d96393f4df64, receipt e9_snareseq_remove0_s0_2-20261024T012010.json):
- smoke exact. canary CKA_all 0.8554 (paper 0.86) -> within 0.04. fos_check == fos_last.
- 2-seed FOSCTTM 0.2235, 0.1489 (noisy with 2; 5-paper-seed mean is the real canary; paper 0.209).
- ORACLE orth 0.14277, lin 0.14399 -> AMBIGUOUS (0.10-0.20), NOT < 0.10. A rotation exists (<< paper 0.209) but the
  ceiling is LOOSER than CITE/PBMC (0.073/0.074). Kill condition (oracle >= 0.20) NOT triggered.
- TYPE (registered P4 rule, min top-5 R2 < 0.30): NUISANCE (min R2 = -0.171). BUT the low-R2 PCs are rna PC4/PC5 and
  atac PC4/PC5, which have LOW variance share (~0.03-0.06), while the HIGH-variance PCs (PC1-3, >0.10 share) are all
  cross-predictable (R2 0.62-0.92). So by the registered rule SNARE is nuisance-type and the removal arm is triggered;
  the POST-HOC variance-aware read is "no DOMINANT nuisance axis, only low-variance idiosyncratic directions" -> the
  by-variance removal (top-1/top-2 = the predictable axes) is expected to NOT help (like CITE). Both views reported.
- FAST (1047 cells); baseline sharded by 3 at workers=4.

## Jobs (all priority 75)

- smoke: job-87be96821f51 (PBMC [0:2]) SUCCEEDED; job-d96393f4df64 (SNARE [0:2]) SUCCEEDED.
- PBMC baseline [2:12], workers=8, ram14000: job-3e63da8ce250 [2:4], job-713d3d56cf20 [4:6], job-66580058d182 [6:8],
  job-42c8021d0129 [8:10], job-??? [10:12] (see jobs.json). (5 shards.)
- SNARE baseline [2:12], workers=4: job-733fcbda3f08 [2:5], job-40ad12e38ffe [5:8], job-d384b7e602a8 [8:11],
  job-51d39f86676b [11:12].
- SNARE removal (registered, k=1) [0:6]: job-66171c32f3e4 [0:3], job-292693ce43a5 [3:6].
- Records + exact job ids in results/e9_single_cell_more/jobs.json.

## RESULTS (MEASURED; receipts in results/e9_single_cell_more/)

PBMC (12 seeds COMPLETE):
- P2 canary PASS on all three: 5-paper-seed FOSCTTM mean 0.0884 (paper 0.089), LTA mean 0.9452 (paper 0.942), CKA
  0.8975 (paper 0.90). (fos_check==fos_last on every seed.)
- P1 oracle orth 0.07368, lin 0.07826 -> both < 0.10 => a rotation EXISTS (<< paper 0.089). PASS.
- Type: variance (min top-5 cross-modal R2 0.6148 both ways). No nuisance axis -> no removal arm (per PREREG).
- P3 selection: 12-seed mean 0.08952, sd 0.00434 (near-zero spread, matches paper 0.003). S1-selected seed 0.09564
  (slightly ABOVE mean). sd < 0.02 => PREREG P3 declares N/A "no spread"; weaker check S1-sel <= mean+0.01 (0.0956 <=
  0.0995) PASS. Spearman 0.322. VERDICT: PBMC is near-solved; there is nothing for S1 to select, exactly as predicted
  for a near-zero-spread pair. (Not a failure of S1; a confirmation that S1's lever is seed spread.)

SNARE-seq (12 seeds COMPLETE; seeds 8,9,10 were resubmitted as singletons after the [8:11] 3-seed shard hit the 30-min
cap -- SNARE QAP solver time varies a lot by seed; one seed ran to 0.65 FOSCTTM):
- P2 canary: 5-paper-seed FOSCTTM mean 0.17785 (paper 0.209; |diff| 0.031 < 0.04) PASS; CKA 0.8554 (paper 0.86) PASS.
  (No paper LTA for SNARE; our LTA mean 0.849 descriptive.)
- P1 oracle orth 0.14277, lin 0.14399 -> AMBIGUOUS (0.10-0.20): a rotation EXISTS (<< paper 0.209) but the ceiling is
  LOOSER than CITE/PBMC (0.073/0.074) -- 10-dim RNA / 19-dim ATAC, ~523 training cells. Kill condition (>=0.20) NOT
  triggered.
- Type: registered P4 rule (min top-5 R2 < 0.30) -> NUISANCE (min R2 -0.171 at rna PC4). BUT low-R2 PCs are PC4/PC5
  (var share ~0.03-0.06); the dominant PC1-3 (>0.80 of variance) are all cross-predictable (R2 0.62-0.92 both ways).
- Removal CONTROL (registered, top-1 variance axis, 6 seeds): removal HURTS -- remove1 mean 0.25894 vs matched
  baseline 0.19833 (+0.061); S1-sel 0.26283 vs 0.14888; Spearman collapses 0.829 -> 0.086. The top axis is shared
  SIGNAL, not nuisance => removal FAILS the PREREG "helps by >=0.02" test. So despite the blunt R2 flag, SNARE has NO
  removable nuisance axis (POST-HOC variance-aware read: no DOMINANT nuisance axis).
- P3 selection (12 seeds): mean 0.23262, sd 0.13696, min 0.14374, max 0.65155. S1-selected seed 0.14888 (near
  best-by-truth 0.14374, near the 0.143 oracle); Spearman(S1,-FOSCTTM) across seeds 0.818, pooled over iterates 0.806.
  S1 selection WORKS STRONGLY (0.149 selected vs 0.233 mean, ~ the oracle ceiling). => PASS. SNARE, like CITE, is a
  search-variance pair where the pairs-free S1 picks the good seed.

## FINAL CROSS-PAIR TABLE (MEASURED; CITE-seq from E8 cited, not rerun)

| pair | CKA (paper) | oracle orth / lin | canary FOSCTTM (paper) | 12-seed mean +/- sd | S1-sel (best-by-truth) | Spearman(S1,-FOS) | type (min top-5 R2) | removal top-1 |
|---|---|---|---|---|---|---|---|---|
| CITE-seq (E8) | 0.961 (0.96) | 0.0727 / 0.0741 | 0.221 (0.225) | 0.184 +/- 0.095 | 0.0893 (0.0893) | 0.839 | variance (0.82) | hurts (0.337 vs 0.200) |
| PBMC | 0.898 (0.90) | 0.0737 / 0.0783 | 0.0884 (0.089); LTA 0.945 (0.942) | 0.0895 +/- 0.0043 | 0.0956 (0.0824) | 0.322 | variance (0.61) | n/a (no nuisance axis) |
| SNARE-seq | 0.855 (0.86) | 0.1428 / 0.1440 | 0.1776 (0.209) | 0.2326 +/- 0.1370 | 0.1489 (0.1437) | 0.818 | nuisance by rule (-0.17); variance by control | hurts (0.259 vs 0.198) |

Receipts: results/e9_single_cell_more/e9_merged_summary.json; per-pair shard JSONs e9_{pbmc,snareseq}_remove{0,1}_s*.json.

## VERDICT vs PREREG (per pair)

- PBMC: P1 PASS (oracle 0.074 < 0.10, rotation exists). P2 PASS (FOSCTTM 0.0884 vs 0.089, LTA 0.945 vs 0.942, CKA 0.898
  vs 0.90). P4 variance-type (min R2 0.61), no removal. P3 N/A then weak-check PASS (near-zero spread; S1 nothing to
  select; near-solved). Kill condition not triggered.
- SNARE-seq: P1 AMBIGUOUS (oracle 0.143 in 0.10-0.20; rotation exists but looser; << paper 0.209). P2 PASS (FOSCTTM
  0.1776 vs 0.209 within 0.04; CKA 0.855 vs 0.86). P4 registered rule -> nuisance-type, but removal CONTROL FAILS the
  >=0.02 help test (removal HURTS +0.061, Spearman collapses) => no removable nuisance axis; variance-type by control.
  P3 PASS (S1-sel 0.149 vs mean 0.233, Spearman 0.818). Kill condition not triggered.
- CROSS-PAIR: E8's CITE-seq result GENERALIZES. All three single-cell pairs: a rotation exists (oracle 0.07-0.14 <<
  unpaired mean), no DOMINANT/removable nuisance axis (removal hurts where tested), and S1-selection usefulness tracks
  SEED SPREAD -- large gain at high spread (CITE sd 0.095, SNARE sd 0.137; S1 ~ oracle ceiling), nothing to do at
  near-zero spread (PBMC sd 0.004, already solved). Opposite of the E7 long-caption text/gen case (dominant nuisance
  axis, S1 selection did not beat the mean). Status: COMPLETE.

CROSS-PAIR TYPE TEST (MEASURED; CITE from E8 cited):
- CITE-seq: variance-type, sd 0.095, S1 works (Spearman 0.84, S1-sel 0.089 vs mean 0.184), removal hurts.
- PBMC: variance-type, sd 0.004 (near-solved 0.089), S1 N/A (no spread), no nuisance axis.
- SNARE-seq: variance-type by the variance-aware / removal-control reading (blunt R2 rule mis-flags it nuisance), sd
  ~0.16, S1 works (Spearman 0.87, S1-sel 0.149 vs mean 0.245), removal hurts.
- SYNTHESIS: all three single-cell pairs are variance-type (no DOMINANT, removable nuisance axis; top-variance axes are
  shared signal). S1-selection usefulness tracks SEED SPREAD, not a nuisance axis: big gain at high spread (CITE,
  SNARE), nothing to do at near-zero spread (PBMC). This is the opposite of the long-caption text/gen case (E7), where
  a dominant nuisance axis made every seed wrong and S1 selection did NOT beat the mean. The E8 CITE result generalizes.
- CAVEAT: the registered P4 min-R2 rule over-flags SNARE (low-variance idiosyncratic axes); the variance-share-aware
  verdict + the removal control are the correct read and are the registered CONTROL. Labelled POST HOC where it
  refines the registered rule.

## How to continue (if interrupted)

1. `export MRUN_URL=http://127.0.0.1:19025` (reopen tunnel if needed: HARD RULE 2). Submitters via
   `~/domains/common/bin/common exec python ...`, Bash `dangerouslyDisableSandbox: true`.
2. Poll smoke jobs; when terminal, `common exec python e9_single_cell_more/submit.py --collect`. Read receipt `smoke`,
   `canary`, `oracle`, and the printed per-seed timing from logs/<job>.txt to size baseline shards.
3. If canary matches paper (P2) and oracle sensible: submit baseline per pair:
   `submit.py --plan baseline --pair PBMC` and `--pair SNARE-seq` (shards in submit.py SHARDS).
4. Only run `--plan removal --pair <p>` if that pair's type_verdict == "nuisance".
5. Collect, analyze LOCALLY with the experiment venv (NOT common exec; shared env lacks unpaired_rosetta):
   `PYTHONPATH=. .venv/bin/python -m e9_single_cell_more.analyze` -> e9_merged_summary.json (+ cross-pair table with
   CITE-seq from E8 cited).
6. Verdict vs PREREG P1-P4 per pair + cross-pair type test; write FINDINGS.md (coordinator) / update NOTES.md.

## Shard sizing note

PBMC has 2407 cells (slower Hungarian assignments per iterate + per refinement) so sharded by 2 seeds (6 shards);
SNARE-seq 1047 cells sharded by 3 (4 shards). Confirm per-seed wall time from the smoke log before the full sweep; if a
shard would exceed ~20 min, shrink it.
