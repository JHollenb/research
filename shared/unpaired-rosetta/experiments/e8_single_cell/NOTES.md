# E8 single-cell (CITE-seq) - NOTES (live state)

Plain version: testing whether Schnaus et al.'s worst "partially aligned" pair, CITE-seq (scRNA vs ADT, CKA 0.96 but
FOSCTTM 0.225 +/- 0.13), fails because no rotation exists (geometry not alignable) or because their unpaired search
misses a rotation that does exist. If it is a search failure, can the pairs-free score S1 pick the good seeds/iterates
(their stated open problem: they report mean over seeds because "without supervision one cannot select the best").

Status as of writing: code built, synthetic smoke PASSED locally, CITE-seq data built + verified on Beast, PREREG
frozen, 2-seed smoke job submitted to Beast (queued behind E7). No real-data findings yet.

## Provenance (MEASURED)

- Their repo cloned at pinned commit fdfad84 to
  /private/tmp/claude-501/-Users-jakeholl-domains/f7d2d6aa-a67f-4693-9e4e-270539ab32fe/scratchpad/dl/schnaus-repo
- CITE-seq raw CSVs downloaded from the SCOT+ book repo (commit 87aedd0), sha256 verified against their
  `modalities/single_cell/prepare.py` CHECKSUMS:
  rna  e1ab54359f9cbdd47ac74bcf3c3f61d22da3eedcd932501ee30bab73e352855e  (MATCH)
  adt  4c827685c66f52c483c0f4b65fb72f7dee18e90a36d486827a5bd325e794a0d3  (MATCH)
- Built [1000,25] float32 tensors (transpose of the [25,1000] CSVs, exactly `prepare_cite_seq`):
  rna raw25.pt sha256 2eb805bc...  adt raw25.pt sha256 7a6f56a3...
  rsynced to beast:/mnt/usb-storage/unpaired-rosetta/storage/embeddings/CITE-seq/{rna,adt}/raw25.pt (hashes match).

## Exact reproduction of their CITE-seq setting (from their code)

- Preprocess: `unpaired_rosetta.embeddings.load_rows` unit-normalizes each cell's 25-dim vector; the aligner then
  center+normalizes (`WassersteinProcrustes._fit`).
- Aligner: their defaults C=30, S=30, b=10000, R=100 (`methods.build_aligner("ours")`).
- Split (their `experiments/other_domains.py` CITE-seq Pair: separate_corpora=False, holdout=0): training =
  `disjoint_split(1000, rnd)` -> 500/500 UNPAIRED cells; eval = all 1000 PAIRED cells, `Randomness(seed)`.
- Seeds: `derive_seeds(42, N)`.
- `aligner_logged.LoggedWassersteinProcrustes` is a verbatim copy of `_fit` + a weight trajectory; the synthetic
  smoke asserts its final weight == the stock aligner's to <1e-5 (so reproduction is exact).

## What each job computes (run.py)

- canary: linear CKA on all 1000 paired cells (expect ~0.96).
- oracle (Q1): true-pair orthogonal Procrustes (+ ridge-linear) FOSCTTM, fit on 500 true pairs, eval on the disjoint
  other 500. "Does a rotation exist?"
- per seed: full trajectory (R+1 weights); per iterate log S1 (mean cosine of full-training Hungarian pseudo-pairs),
  S2 (CKA of pseudo-pairs), and true FOSCTTM. S1 uses NO true pairs.
- selection (Q2): mean/std/min/max of last-iterate FOSCTTM over seeds; S1-selected seed and S1-selected
  seed+iterate FOSCTTM (pairs-free); best-seed-by-truth and min-FOSCTTM-iterate as LABELLED references; Spearman(S1,
  -FOSCTTM) across seeds and pooled over iterates.
- axis (Q3): top-5 PC variance share of each modality, held-out cross-modal R2 predicting each top PC from the OTHER
  modality's raw features (ridge 2-fold), |corr| of top PC with a depth proxy (sum of raw features per cell).
- removal (Q3): plan "removal" re-runs the 20-seed sweep with the top-1 and top-2 variance axes of each modality
  projected out (pairs-free) before normalization; compare FOSCTTM (mean and S1-selected) vs baseline.

## Jobs

- smoke: job-9779e67cfc0a (--seeds 2), submitted, queued (Beast CPU committed by E7). Validates env/canary/oracle +
  measures per-seed Beast time before the 20-seed jobs.
- NEXT after smoke OK: `common exec python e8_single_cell/submit.py --plan baseline` (20 seeds), then `--plan removal`.
- Collect: `common exec python e8_single_cell/submit.py --collect` -> results/e8_single_cell/e8_citeseq_remove{0,1,2}-*.json

## How to continue (if interrupted)

1. `export MRUN_URL=http://127.0.0.1:19025` (reopen tunnel if needed: see HARD RULE 2). Run submitters with
   `~/domains/common/bin/common exec python ...` and Bash `dangerouslyDisableSandbox: true`.
2. Poll job-9779e67cfc0a; when terminal, `--collect`, read the receipt's `smoke`, `canary`, `oracle`.
3. If canary mean FOSCTTM ~0.225 and CKA ~0.96 (P2) and oracle sensible: submit `baseline` and `removal`.
4. Collect, then verdict vs PREREG P1-P4; write FINDINGS.md.

## Deferred (documented)

- human vs mouse scRNA (0.338): needs CZ CELLxGENE Census (~1.3 GB + cellxgene/tiledbsoma env), not on their HF repo.
- histology vs expression (0.369): needs 13.9 GB HEST + H-Optimus-0 GPU tile embedding (external pipeline) -> out.
