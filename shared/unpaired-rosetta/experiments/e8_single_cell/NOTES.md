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

## SMOKE RESULTS (MEASURED, job-9779e67cfc0a, Beast, 2 seeds = universe[0:2])

Receipt: results/e8_single_cell/e8_citeseq_remove0-20261023T231003.json
- smoke: logged_vs_stock=0.0, synthetic_oracle_foscttm=0.0, synthetic_true_rot_s1=0.99997 (reproduction exact)
- canary: CKA all-1000 = 0.9614 (paper 0.96; within 0.04 -> P2 CKA PASS)
- seed 734796314 (paper seed 0): FOSCTTM_last = 0.2270 (paper mean 0.225!) ; seed 576165995: 0.4165. sd(2)=0.134 (~0.13)
- ORACLE (Q1, DECISIVE): orth_holdout FOSCTTM = 0.07273, lin_holdout = 0.07412. Both << 0.225 and < 0.10 -> P1 PASS:
  a single ROTATION aligns the true pairs on a disjoint holdout. orth ~ lin => it IS a rotation (not scale/shear).
  => CITE-seq failure is a SEARCH failure, not missing shared geometry.
- AXIS (Q3, DECISIVE, seed-independent): top-5 PC held-out cross-modal R2 = rna-from-adt [.95,.94,.90,.94,.85],
  adt-from-rna [.95,.94,.82,.93,.88]. Every top PC of each modality is highly predictable from the OTHER => NO
  dominant nuisance axis that one side carries and the other cannot. depth-proxy |corr| with topPC: rna 0.18, adt 0.41.
  => H3 (nuisance axis) looks FALSE for CITE-seq; removal predicted to be ~null (pre-registered control).
- COST: ~10-16 min/seed single-threaded; QAP model build is O(C^4)=810k-iter pure-Python loop per restart x S=30
  (NEW-B bottleneck). => parallelize restarts with --workers 8 and shard seeds; cross-seed merge done locally.

## Jobs

- smoke: job-9779e67cfc0a SUCCEEDED (see SMOKE RESULTS above) = baseline seeds universe[0:2].
- baseline shards (12 seeds total incl smoke's [0:2]), SUBMITTED, queued: job-30a3af365527 [2:5], job-c04428e9cbfd
  [5:8], job-0d378844e6a8 [8:10], job-8435ccb584eb [10:12]. workers=8, cpu_threads=8, timeout 1800.
- removal shards (k=1, seeds [0:6]), SUBMITTED, queued: job-77dcac75d1bb [0:3], job-7673283a887d [3:6].
- Collect: `common exec python e8_single_cell/submit.py --collect` -> results/e8_single_cell/e8_citeseq_remove{0,1}_sLO_HI-*.json
- Merge/analyze (local, floats only): `python -m e8_single_cell.analyze` -> e8_merged_summary.json + prints selection stats.

## How to continue (if interrupted)

1. `export MRUN_URL=http://127.0.0.1:19025` (reopen tunnel if needed: see HARD RULE 2). Run submitters with
   `~/domains/common/bin/common exec python ...` and Bash `dangerouslyDisableSandbox: true`.
2. Poll job-9779e67cfc0a; when terminal, `--collect`, read the receipt's `smoke`, `canary`, `oracle`.
3. If canary mean FOSCTTM ~0.225 and CKA ~0.96 (P2) and oracle sensible: submit `baseline` and `removal`.
4. Collect, then verdict vs PREREG P1-P4; write FINDINGS.md.

## REPRODUCTION BUG FOUND + FIXED (canary did its job)

First baseline sweep (pre-fix) gave paper-5-seed mean 0.305 (not 0.225): their `run_alignment` passes the SAME
`Randomness` object into `aligner.fit` AFTER it was advanced by the train `disjoint_split`'s permutation(1000); I was
passing a fresh `Randomness(seed)`, so the aligner's kmeans/solver/batch draws differed. FIXED in run.py: fit now gets
the advanced `rnd` object. Oracle (Q1) and axis (Q3) are UNAFFECTED (they never use the aligner randomness). The Q2
per-seed FOSCTTM distribution + S1 selection are being RE-RUN. Stale pre-fix receipts moved to
results/e8_single_cell/stale_prefix_randomness/. Also fixed killed_ram: workers 8->4, ram 6000->12000 (clamped 10240).

NOTE (pre-fix, for reference only, DO NOT cite): even with the wrong randomness, S1 selection already worked -- 9-seed
mean 0.247, S1-selected-seed 0.089 (== best-by-truth), Spearman(S1,-FOSCTTM)=0.767; removal (top-1) HURT (0.346 vs
matched baseline 0.305), confirming no nuisance axis. The fixed run should land near 0.225 mean and is the citable one.

## Jobs (FIXED run)

- baseline [0:12], 4 shards: job-06a9c7d97274 [0:3], job-84b8d9b76ae3 [3:6], job-76beff7dcbb4 [6:9],
  job-1f437f00652f [9:12]. workers=4, ram 12000 (clamped 10240), timeout 1800.
- removal k=1 [0:6], 2 shards: job-d99a81cffc18 [0:3], job-50fa2d621902 [3:6].
- Collect: `common exec python e8_single_cell/submit.py --collect`. Analyze LOCALLY with the experiment venv:
  `./.venv/bin/python -m e8_single_cell.analyze` (NOT `common exec` -- the shared env lacks unpaired_rosetta).

## FINAL VERDICT vs PREREG (MEASURED, fixed run; receipts results/e8_single_cell/e8_citeseq_remove{0,1}_s*-2026102*.json)

- P1 (rotation exists, orth holdout < 0.10): PASS -- orth 0.0727, lin 0.0741 (orth~=lin => true rotation, not
  scale/shear). vs their 0.225. => shared geometry is real; failure is a SEARCH failure.
- P2 (canary): PASS. Paper-5 seeds mean 0.2214 (vs 0.225), sample sd 0.1315 (vs 0.13), CKA all-1000 0.9614 (vs 0.96).
  (The pre-fix run gave 0.305 and caught the randomness bug.)
- P3 (S1-selected seed < mean AND Spearman > 0.3): PASS, strongly. 12 seeds: mean 0.1837, sd 0.0952; pairs-free
  S1-selected seed = 0.0893 (== best-by-truth; near the 0.073 oracle); Spearman(S1_last,-FOSCTTM) across seeds = 0.839,
  pooled over iterates 0.823. Iterate-within-seed selection adds ~nothing (refinement is stable) -- seed selection is
  the lever.
- P4 (axis + removal): axis MEASURED -> NO nuisance axis (top-PC cross-modal R2 0.82-0.95 both ways). Removal CONTROL
  (6 seeds): top-1 axis removal HURTS (mean 0.337 vs matched baseline 0.200; S1-sel 0.360 vs 0.098) and flattens the
  S1-FOSCTTM relation (Spearman 0.086) => the top axes are shared SIGNAL, not nuisance. H3 FALSE for CITE-seq.
- Kill condition (oracle >= 0.20): NOT triggered.

Headline (citable): CITE-seq is a clean in-biology case of "a rotation EXISTS (oracle 0.073) but the unpaired search
misses it" -- alignability != searchability. The failure is seed/search variance, NOT a nuisance axis (opposite of the
text/gen case). The pairs-free S1 score both diagnoses it (Spearman 0.84) and fixes it over seeds (0.089 selected vs
0.184 mean, near the 0.073 ceiling) -- answering their open problem (L992-994) and limitation (L777) on this pair.

## Deferred (documented)

- human vs mouse scRNA (0.338): needs CZ CELLxGENE Census (~1.3 GB + cellxgene/tiledbsoma env), not on their HF repo.
- histology vs expression (0.369): needs 13.9 GB HEST + H-Optimus-0 GPU tile embedding (external pipeline) -> out.
