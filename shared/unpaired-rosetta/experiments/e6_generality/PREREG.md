# E6 (X01-schnaus-generality) pre-registration

Written 2026-10-22, before any fit or axis statistic touched DCI, DOCCI or COCO-val Qwen3-8B-gen data. Theme
C19-cross-model-alignment. Response under revision: `../../response.md` (draft 2).

## Question

The response (draft 2) finds, on one corpus (StanfordParagraphCaptioning, SPC), that Qwen3-8B generative-pooling
text embeddings carry a dominant non-visual principal axis; projecting it out takes SPC holdout FOSCTTM from
0.415 to 0.038 under Schnaus et al.'s unpaired aligner; the same projection wrecks MPNet and Qwen3-Embedding-8B;
and a pairs-free gate detector (S1 = mean cosine of Hungarian-matched pairs) picks the right setting in 9/9
encoder x seed cases. Its stated main vulnerability (response.md §10) is "one corpus": Schnaus validate
SPC-trained maps on COCO-val and also use DenselyCaptionedImages (DCI) and DOCCIDataset (DOCCI). This experiment
asks whether the axis, the fix and the detector reproduce on those other corpora, using Schnaus' own stored
Qwen3-8B-gen embeddings (no re-embedding).

## Data (all from their HF dataset `schnaus/unpaired-rosetta-embeddings`, their stored files, loaded by their
`unpaired_rosetta.embeddings.load_rows` at their pinned commit fdfad84)

- Corpora: DenselyCaptionedImages (DCI, 7805 rows), DOCCIDataset (DOCCI, 14847 rows) [primary, long detailed
  captions, the two non-SPC long-caption corpora Schnaus use]; coco_val2014 [secondary, short captions,
  contingent on a 14 GB download of its Qwen3-8B-gen file completing].
- Vision: `dinov2_vit-b14@224_mean`. Language encoders: `qwen3-8b-gen_69445574b3021b8a2733e87d8603d769` (gen),
  `qwen3-embedding-8b`, `mpnet`.
- Their `reduce_texts` reduces the stored (N, k, 4096) gen tensors to one unit (N, 4096) vector per item exactly
  as for SPC; the pipeline is their code, unchanged, with only the `--corpus` argument changed from SPC.

## Protocol (identical to E5, their `WassersteinProcrustes` with default hyperparameters)

- Train on the corpus minus the last `holdout=2000` rows, as their two disjoint unpaired halves; FOSCTTM on those
  2000 held-out rows. The dropped axis is the top principal component of the unpaired language training rows,
  projected out of every language row (train and eval). Fits are CPU, on Beast via mrun (never the laptop).
- Gate candidates per encoder: `none` (their pipeline) or `pc{k}` for k in 0..4 (gate off language PC k).
  Unpaired scores on the training rows (no true pair): S1 = mean cosine of Hungarian-matched pairs; S2 = linear
  CKA over the matched pairs. FOSCTTM uses true pairs and is evaluation only; it never enters the selection.
- Axis probe (offline, seconds): per corpus, on the first 4096 rows, clipped and linear CKA with DINOv2, top
  language PC variance share, held-out R^2 of the top-5 language PCs from the image embedding (ridge, 2-fold),
  |corr| of top language PC with top image PC, linear CKA after projecting out the top-k language PCs, mutual
  10-NN. This is `e5_scaffold_axis/axis_probe.py` parameterised by corpus.

## Primary metric

Holdout FOSCTTM (fraction of samples closer than the true match; 0 perfect, 0.5 chance), from their
`retrieval_metrics`. Secondary: top-PC variance share, held-out image-predictability R^2, linear/clipped CKA,
sign of linear-CKA change after dropping the top PC, and the unpaired S1/S2 scores.

## Hypotheses and PASS/FAIL thresholds (frozen before any DCI/DOCCI/COCO number was seen)

Primary (DCI and DOCCI; both long detailed captions, Schnaus report Qwen3-gen stays near chance on them):

- **P1 (axis exists).** For Qwen3-8B-gen the top language PC carries a large variance share (>= 8%, cf. SPC 13.8%)
  and low held-out image-predictability R^2 (<= 0.40, cf. SPC 0.16), while for MPNet and Qwen3-Embedding the top
  PC has a smaller variance share than gen's and high R^2 (>= 0.70, cf. SPC 0.88-0.89). PASS per corpus if the
  gen-vs-control separation holds in both variance share and R^2.
- **P2 (CKA sign, Lemma A1).** Projecting out gen's top PC raises linear CKA with DINOv2; projecting out the top
  PC of MPNet and Qwen3-Embedding lowers it. PASS per corpus if the sign is + for gen and - for both controls.
- **P3 (the fix).** Under their aligner, dropping the top language PC lowers gen holdout FOSCTTM by at least a 50%
  relative reduction and clearly below raw beyond seed noise, and raises FOSCTTM for both control encoders (makes
  them worse by a clear margin). PASS per corpus if gen improves by >= 50% relative and both controls worsen.
- **P4 (unpaired detector).** The S1 argmax selects pc0 for Qwen3-gen and `none` for both MPNet and
  Qwen3-Embedding, at seed 0 over the full 6-candidate sweep. PASS per corpus if S1 picks pc0 for gen and none
  for both controls. (Falsifier, as in E5 G1.)

Secondary (coco_val2014; short captions; contingent on the download):

- **P5 (short-caption scope).** On COCO, Qwen3-gen's top PC is less non-visual than on the long-caption corpora
  (higher R^2 and/or smaller variance share) and dropping it does not produce the large fix seen on long captions
  (no-op or harmful). This ties the axis to long/detailed captions. If the axis is as strong on COCO as on SPC,
  that is a finding (the axis is a generic gen property), reported as such, not a failure.
- **P6 (transfer protocol).** A map fit on SPC gen and evaluated on COCO-val gen (their validation setting), with
  and without the SPC-estimated top PC projected out of both sides. Report raw vs fixed FOSCTTM; no directional
  bar frozen because COCO captions are short (gen may already work), so this is descriptive.

## Kill condition (from the C19 dossier)

The axis/fix does not reproduce outside SPC -> narrow the response to a scoped (SPC-only) comment. Operationalised:
if on BOTH DCI and DOCCI the drop-top-PC fix fails to materially reduce gen FOSCTTM (relative reduction < 30% on
both, or drop1 not below raw beyond fit noise on both), the generality claim FAILS and response.md §3/§8 are
narrowed to an SPC-scoped comment with the negative reported honestly.

## Named nulls / controls

- Control encoders MPNet and Qwen3-Embedding-8B: the same drop-top-PC operation must harm them, not help (the
  fix is encoder-specific, not a blanket rule).
- No-op canary: gate candidate `none` reproduces the raw FOSCTTM within fit noise (same fit, no projection).
- Short-caption control: coco_val2014 (if downloaded), where Schnaus do not report the gen failure.
- Code/data parity: Schnaus' load path + aligner at commit fdfad84, unchanged; only `--corpus` changes. The
  smoke-gate confirms wiring before any scored fit.

## Smoke checks (frozen; run in-process first in each scored job; abort the job on failure)

1. reduce_texts(gen) for the corpus loads as (N, 4096), finite (no NaN/Inf), unit-norm within 1e-3, and n equals
   the vision n.
2. A tiny fit (num_clusters=10, num_restarts=3, batch_size=1500, num_iterations=5) on a 3000-row disjoint subset
   returns a finite FOSCTTM in [0, 0.5].
3. principal_axes(sy, 1) is unit-norm (|norm-1| < 1e-4) and projecting it out changes the training-row covariance
   trace (the projection is non-trivial).

A separate tiny smoke job (gates --smoke on DCI gen and DOCCI gen) runs first to catch the DCI row-count /
bf16-DOCCI path before the full sweep is submitted.

## Seeds

Single seed (0) per arm for the full 6-candidate sweep. Extra seeds (1, 2) only for the gen `none`+`pc0` arms on
DCI and DOCCI (the paper-relevant fix claim), to match the SPC 3-seed headline. No seeds spent on arms that fail
or that cannot contribute (owner rule 2026-10-09).

## Pre-registration looks (local runs that touched real data before this prereg)

- Listed the HF dataset's file names and byte sizes (`HfApi.list_repo_files`, `repo_info(files_metadata=True)`).
  Metadata only; no embedding values read.
- Loaded the DCI and DOCCI stored tensors on the laptop with `torch.load(mmap=True)` to read `.shape` and
  `.dtype` and row counts only (DCI gen (7805,3,4096) fp32; DOCCI gen (14847,3,4096) bf16; etc.). No fit, CKA,
  R^2, principal component, variance share, S1/S2 or FOSCTTM was computed locally; the predictions above are
  blind to every quantity any hypothesis is about.
- No real model was loaded on the laptop. All fits and all axis statistics run on Beast via mrun.

## Scoring

The frozen text above is scored literally. Any scorer or threshold changed after seeing data is labelled POST
HOC in FINDINGS.md. sha256 of this PREREG.md and of every shipped e6 file is recorded in each job's receipt
config (`manifest_sha256`).
