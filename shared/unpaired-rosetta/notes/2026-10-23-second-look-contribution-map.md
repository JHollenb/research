---
title: "Second look: contribution opportunities for Schnaus et al., Shared Geometry as a Rosetta Stone"
date: 2026-10-23
status: research note (read-only analysis; nothing run on real data, no jobs submitted, not sent to anyone)
paper: arXiv 2610.09411 v2 (8 Oct 2026)
paper_text: /private/tmp/claude-501/-Users-jakeholl-domains/f7d2d6aa-a67f-4693-9e4e-270539ab32fe/scratchpad/dl/papers/schnaus/schnaus_v2.txt
code: github.com/dominik-schnaus/unpaired-rosetta @ fdfad84 (MIT)
our_prior_work: research/shared/unpaired-rosetta/response.md (draft 3.2), shared.md, experiments/ (E0-E6b)
scope_note: E7 (better initializations for gen on DCI/DOCCI) is already running separately; items below do not duplicate it.
---

# Second look: how to make a genuinely bigger contribution to "Shared Geometry as a Rosetta Stone"

All line numbers (L####) refer to the paper text file named in the front matter. Code references are `path:line @ fdfad84`.

## Part 1 - Map of their paper

**Method in one line.** Center and unit-normalize both spaces; QAP-match k-means cluster centers on centered kernels (equivalent to maximizing linear CKA, equivalent to a low-rank Gromov-Wasserstein plan), solved with MPOpt; a conditional-gradient read-out turns the averaged plan into pseudo-pairs via blocked Jonker-Volgenant; alternating Hungarian matching and orthogonal Procrustes refine a single semi-orthogonal map W. Four hyperparameters (C=30, b=10000, S=30, R=100). Paired examples, when present, enter both stages as a linear term. (Algorithms 1-2, L171-349; complexity L1676-1699.)

| # | Main claim | Evidence | Where weakest / untested |
|---|---|---|---|
| 1 | Unpaired coarse cross-modal alignment is possible | COCO FOSCTTM 0.154 average, beats mini-vec2vec on 17 of 21 vision-language pairs (L385); holds cross-dataset, COCO images vs SPC captions, 0.236 (L681) | Coarse only: paired CLIP is 0.0006 vs their 0.154 (L386). Generative token pooling fails on every long-caption corpus (L677, L3546, L4621). iBOT ViT-B/16 is consistently weak (L2463). |
| 2 | Shared geometry predicts alignability; CKA is the score | CKA R2=0.73, rho=-0.90 on vision-language (Fig 3c); R2=0.69, rho=-0.82 across 14 scientific pairs (L790); CKA is the best of four metrics (mutual k-NN 0.40, TSI 0.37, QSI 0.18; L2475) | The predictor needs pairs: all four metrics are computed on 10,000 paired validation samples (L2271-2273). CKA predicts search success, not rotation existence (our E6b). CITE-seq is a counterexample: CKA 0.96, the highest of all 14, yet FOSCTTM 0.22 +/- 0.13 (L6015; Tab 12 L6384). |
| 3 | Generalizes across domains | Competitive with or better than SCOT+ (PBMC 0.089 vs 0.121) and Platonic Brain (fMRI 0.033 vs 0.035) (L779); 14-pair scientific sweep (Fig 4b) | Reports average, not best, "since without supervision one cannot select the best-performing seed" (L777). The "partially aligned" tier (CITE-seq; human vs mouse scRNA 0.338; histology vs expression 0.369) is unexplained (L6012-6016). |
| 4 | Few pairs give a large advantage | 14x-28x lower FOSCTTM than the best baseline at <=20 pairs; 5.4x at 50, 3.2x at 100 (L806); zero-pair beats baselines-with-500 downstream (L892) | Strongest claim, least to add. Our span ceiling (Part 2 #10) explains why baselines lag but does not dispute it. |
| 5 | Alignment enables text-to-image generation without pairs | RAE diffusion on DINOv2 embeddings; TIFA 0.552 (0 pairs, MPNet) beats linear-with-100-pairs 0.507 (Tab 6, L5120) | "reasonable quality... albeit with often missing fine details" (L914). Fidelity is only qualitative plus CLIP/TIFA. The rotation is the fidelity ceiling (our Part 2 #5). Gap to GT and Scale-RAE is large (L5207). |

**What they themselves flag as open (verbatim).**

- L992-994: "Currently, we cannot reliably determine from unpaired data alone whether two spaces are sufficiently similar to be aligned, as usual alignment metrics need matching samples. Developing fully unsupervised alignment prediction scores remains an open problem."
- L777-778: "we report average rather than best performance, since without supervision one cannot select the best-performing seed."
- L999-1006: "much of web-available text does not describe visual scenes and may thus share less semantic structure with vision representations. This limits the applicability of our current approach to noisier multimodal data..."
- L6042-6044 (future work): "Such an alignment would allow architectures that place a generative model in each space and translate between them without a GAN... we leave this direction to future work."
- L2466-2467: "we don't observe a strong trend that bigger models can be aligned better, even though our study is not big enough to conclude on this point."
- L995-998: the mechanism for why alignment is coarse rather than fine is described but not resolved.

**What our prior note already owns (do not re-litigate).** The non-visual-axis diagnosis plus the pairs-free detector (claim A*), retrieval-is-not-fidelity plus the rotation ceiling (claim D), the span ceiling for pair baselines (claim C), the layer/pooling negatives (E3), and a single true-pair oracle on Qwen3-gen (E6b). See response.md draft 3.2.

## Part 2 - Ranked contribution opportunities

Big vs small is called out per item. "Decisive experiment" assumes Beast CPU plus one 16 GB GPU, using their released embeddings and their own loaders. I did not run anything, so job times are not measured; all items are small by their own complexity analysis (no n x m matrix is ever formed, L1697).

### 1. A fully unsupervised alignability predictor (their stated open problem). BIG.
What it adds: converts their descriptive predictor (CKA, which needs an oracle pairing, L2271-2273) into an operational score that needs no pairs. The aligner already produces pseudo-pairs; score them with S1 (mean cosine of Hungarian-matched pseudo-pairs) and S2 (linear CKA on pseudo-pairs). Why they care: it is verbatim the problem they pose (L992-994), and the code confirms there is no predictor module today, only a scatter-plus-fit (`experiments/shared_geometry.py`, `experiments/other_domains.py` @ fdfad84).
Decisive experiment: re-run their aligner across the released benchmark (21 vision-language pairs x 4 corpora, plus the 14 scientific pairs), record S1/S2 per fit alongside FOSCTTM, and compare the S1-vs-FOSCTTM R2/rho to CKA's 0.73/0.69.
Chance it works: high within a domain (we measured Spearman(S1, -FOSCTTM) 0.77-0.94 across removal settings, response section 3.3); medium across the whole zoo, because S1 is over-optimistic exactly when the search locks onto a nuisance axis (the gen case, where our S1 margin was 0.001-0.006, response section 3.6). That boundary is itself reportable.
Risk it is already done: low. All four of their metrics need pairs; they propose no unpaired score.

### 2. Unsupervised seed selection (their stated limitation, L777). BIG-ish; pairs with #1 and NEW-A.
What it adds: lets them report selected-best instead of average, honestly improving essentially every FOSCTTM in the paper and removing a limitation they state twice (L373, L777).
Decisive experiment: in the same sweep as #1, run 5 seeds per pair and check whether argmax-S1 selects a near-best seed.
Chance it works: high. Risk it is already done: none.

### 3. The CITE-seq / "partially aligned" tier: the gen mechanism in biology. BIG, novel.
What it adds: CITE-seq (scRNA vs ADT protein) has CKA 0.96, the highest of all 14 pairs, yet FOSCTTM 0.22 +/- 0.13 with the largest seed variance (Tab 12 L6384 and L6367; text L6015). That is the exact gen signature: global geometry shared, unpaired search fails. Hypothesis: a dominant technical nuisance axis (sequencing depth / library size in scRNA, a textbook covariate; an analogous depth axis in ADT) uncorrelated across modalities, so the search rotates one space's depth axis onto the other's. Why they care: it explains their weakest tier and offers a concrete, domain-relevant fix, generalizing our SPC axis result into a second field.
Decisive experiment: using their own loaders (`modalities/single_cell/prepare.py` and `modalities/single_cell/cross_species.py` @ fdfad84 wire CITE-seq, SNARE-seq, PBMC, and human vs mouse scRNA with checksummed downloads, no stubs), run our axis probe (top-PC cross-modal held-out R2), the true-pair oracle (does a rotation exist?), and axis removal. Single-cell sets are thousands of cells, so this is CPU-minutes.
Chance it works: moderate-good (depth is a known scRNA axis). Risk it is already done: none.

### 4. Alignability vs searchability: the theory frame for Finding 1. MEDIUM, high-confidence.
What it adds: our E6b already shows gen off-SPC has a rotation the unpaired search misses. Generalize by running the true-pair oracle across every benchmark pair, especially the partially-aligned and borderline at-chance tiers (L6012-6020). Reframe Finding 1 as: CKA predicts whether the unpaired search succeeds, not whether a rotation exists. This tells them and E7 where to invest (better init/search) versus where to stop (no shared geometry). The oracle is closed-form Procrustes on true pairs, computed free inside the #1 sweep.
Chance it works: high that it yields a clean three-way taxonomy (no rotation / rotation exists but search misses / both). Risk it is already done: our section 3.6 covers the gen case only; this is the extension. Do not re-run E7's init experiments; this is the measurement and theory wrapper around them.

### 5. A fidelity metric plus a relaxed-map fix for their text-to-image demo. MEDIUM.
What it adds: our section 4 shows FOSCTTM is not fidelity and that the rotation itself is the ceiling (the constraint costs 0.21 median-alpha versus a 0.07 estimation gap). The code confirms the mechanism: the "ours" map is inverted as `aligner.weight.T` (an orthogonal map) and the RAE decoder never sees text, so image fidelity is bounded by the map (`modalities/text_to_image/sample.py:98`, `experiments/text_to_image.py:84` @ fdfad84). Build the untested lever from response section 4.3: unpaired rotation plus a low-rank non-orthogonal correction on <=100 anchors, measured against their rotation-plus-100-pairs with their own TIFA/VQAScore harness (`experiments/text_to_image_scores.py`).
Chance it works: medium-good. Risk: the decoder may only care about direction within a zone (our FLUX zones) - report honestly.

### 6. A cheaper, mechanism-grounded predictor. MEDIUM-SMALL.
What it adds: their Appendix E shows the first ~10 PCs and cosines 0.0-0.6 carry the alignment (L6614, L6773). A top-10-PC CKA may predict FOSCTTM as well as full CKA, and a CKA-plus-S1 (geometry plus search) combination may beat either alone, feeding #1 directly. Cheap, computed in the same sweep.

### 7. Scaling and more encoders. MEDIUM.
What it adds: they flag no clear size trend (L2466). Add a few larger and more diverse encoder pairs to test whether PRH's scale claim predicts unpaired alignability (not just paired convergence). Medium cost (new embeddings), medium novelty; most valuable only once #1 gives it a cheap readout. (See NEW-B for the aligner-side scaling lever, which is sharper.)

### 8. Release a diagnostic tool / PR. SMALL but strategic.
What it adds: package axis-probe + S1 predictor + per-pair alpha fidelity report against their repo's API (MIT license confirmed). Low research risk, high adoption, makes co-authorship or citation natural. Their metric and evaluation suite (`unpaired_rosetta/geometry.py`, `unpaired_rosetta/evaluation.py` @ fdfad84) and the drop-in notebook (`unpaired_rosetta.ipynb`) are clean integration points.

### 9. FOSCTTM robustness. SMALL.
What it adds: our D1 check (response section 4.4) found near-duplicate keys dominate the ranking tail, and they note mutual k-NN is density- and size-sensitive (L6024). A short study of FOSCTTM's dependence on near-duplicates and sample size, plus a deduplicated variant. (Implementation: `retrieval_metrics` with mid-ranks in `unpaired_rosetta/evaluation.py:96` @ fdfad84.)

### 10. Few-pair curve theory. SMALL.
What it adds: our span ceiling (Lemma C) plus CKA gives a predicted FOSCTTM(p) curve to overlay on their Fig 5. Mostly closes out section 5; low marginal value.

### NEW-A. Best-iterate / best-restart selection inside their own aligner. BIG; merges with #1, #2, #4.
What the code revealed: the refinement loop runs a fixed R=100 iterations and returns the last iterate, with no convergence test or best-iterate selection (`WassersteinProcrustes.refinement_step`, `unpaired_rosetta/wasserstein_procrustes.py:148-165` @ fdfad84; defaults C=30/S=30/b=10000/R=100 at `:53-69`). Combined with L777, the pairs-free score S1 can do triple duty: select the best iterate along the R=100 trajectory, the best restart, and the best seed, all with no pairs. This turns #1's predictor from a diagnostic into an in-loop improvement to their own reported numbers.
Decisive experiment: log S1 per iterate and per restart inside the Run-1 sweep; check whether S1-selection beats last-iterate and seed-average on true FOSCTTM. Trivial compute.

### NEW-B. A better aligner: scalable QAP and soft refinement. MEDIUM.
What the code revealed: the QAP initialization builds an O(C^4) dense graphical model in Python loops, which caps C (`unpaired_rosetta/qap.py:95-104` @ fdfad84), yet their own ablation says larger C generally helps (L2208). And refinement uses hard Hungarian assignment; Sinkhorn exists only as an ablation, not on the main path (`unpaired_rosetta/ablation/sinkhorn.py` @ fdfad84). Two concrete levers: (a) a sparse or scalable QAP enabling larger C; (b) entropic / soft refinement on the main path. These are exactly the "make the search reach the rotation the oracle shows exists" moves that #4 motivates and that E7 is circling. Higher risk than #1-#3.

### NEW-C. Classifier-free guidance for the generation demo. SMALL, free add-on to #5.
What the code revealed: sampling runs with no classifier guidance (guidance scale 1.0), 250 Euler ODE steps from Gaussian noise (`modalities/text_to_image/sample.py`, `load_diffusion` at `:52`, conditioning at `:98` @ fdfad84). Turning on classifier-free guidance is a zero-pair fidelity lever they left on the table; test it alongside the relaxed-map correction in #5.

## Part 3 - Recommendation (revised, in run order)

1. Run 1, one benchmark sweep. Re-run their released aligner across the full benchmark, logging per fit: FOSCTTM, the pairs-free self-scores S1/S2 (per seed, per restart, per iterate), and the true-pair oracle FOSCTTM. This single sweep yields the unsupervised predictor (#1), unpaired selection over seeds and now iterates/restarts (#2 plus NEW-A), and the alignability-vs-searchability oracle taxonomy (#4). NEW-A makes the sweep improve their reported numbers, not just diagnose, and the block hits their stated open problem (L992-994) and stated limitation (L777) at once. This is the flagship: highest value, cheapest, lowest risk.

2. Run 2, the CITE-seq / partially-aligned probe (#3), confirmed runnable with their own single-cell loaders: axis probe + true-pair oracle + removal on the CKA-0.96 / FOSCTTM-0.22 pair, extended to human vs mouse scRNA and histology vs expression. This is the memorable second-domain evidence and a natural case study inside Run 1's taxonomy.

3. Then NEW-B (scalable QAP and soft refinement) if Runs 1-2 show the bottleneck is searchability rather than geometry, and #8 to package the predictor and probe as an MIT-compatible PR to their repo. #5 plus NEW-C is the optional GPU-heavier add-on if a generation-quality result is wanted.

Together these turn our current note (a diagnosis of one failure) into a general, positive contribution: an unpaired alignability score that answers their headline open problem and improves their own numbers in-loop, a principled separation of "a rotation exists" from "the search finds it," and a second-domain confirmation that the nuisance-axis mechanism is not specific to text.

Caveat: nothing above requires the external fMRI pipeline, which needs NSD access plus the authors' stage-3 outputs (`modalities/brain_scans/` @ fdfad84 is wired but consumes an external pipeline). Only COCO/SPC vision-language embeddings are present locally; everything else must be pulled from their release using their loaders.
