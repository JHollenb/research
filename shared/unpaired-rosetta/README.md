# Unpaired Rosetta: Schnaus, Dagès, Cremers, Wang and Isola (2026)

**"Shared Geometry as a Rosetta Stone: Cross-Modal Alignment Without Paired Data."** Dominik Schnaus, Thomas
Dagès, Daniel Cremers, Xi Wang and Phillip Isola. TU Munich, MCML, Ulm University, ETH Zurich and MIT. Cremers,
Wang and Isola advised equally.

| | |
|---|---|
| Paper | [arXiv 2610.09411](https://arxiv.org/abs/2610.09411) ([PDF](https://arxiv.org/pdf/2610.09411)) |
| Project page | <https://dominik-schnaus.github.io/unpaired-rosetta/> |
| Code | <https://github.com/dominik-schnaus/unpaired-rosetta> (MIT). We read commit `fdfad84` (2026-10-08). |
| Embeddings | <https://huggingface.co/datasets/schnaus/unpaired-rosetta-embeddings> |
| Notebook | `unpaired_rosetta.ipynb` in the repo (also on Colab) |

This folder holds our reading of the paper and what we can offer the authors:

| file | content |
|---|---|
| `README.md` | this page: what they did and how, with links |
| [`shared.md`](shared.md) | how our work relates to theirs, what we can do for them, what they can do for us |
| [`response.md`](response.md) | **the response paper (draft 2)**: a hidden scaffold axis in Qwen3 generative pooling and an unpaired fix (SPC FOSCTTM 0.415 → 0.038), the retrieval-vs-fidelity gap and rotation ceiling, a span ceiling for pair baselines, and the ideas that failed |
| [`experiments/`](experiments/README.md) | the code for every claim, built on their library at the pinned commit |
| [`figures/`](figures/) | report figures, regenerated from receipts by `experiments/figures/make_figures.py` |

## The question

Multimodal models such as CLIP learn image–text alignment from very large paired datasets. The Platonic
Representation Hypothesis (Huh, Cheung, Wang and Isola, 2024) suggests that models trained separately on
different modalities converge toward a shared geometry. If so, is paired data necessary at all? The paper
answers that, for **coarse** alignment, it is not.

## The method: Wasserstein Procrustes with a geometric initialization

Given two unpaired embedding sets X (for example DINOv2 images) and Y (for example MPNet captions), both centered
by their own mean and normalized to unit length, they solve

```
max over W in St(d_X, d_Y) and over couplings T:   Tr(X W Yᵀ Tᵀ)
```

Here W is a single semi-orthogonal map, so it can only rotate or reflect, and T is a correspondence between
samples. This is non-convex, so the initialization does the hard work (Algorithm 2 in
`unpaired_rosetta/geometric_initialization.py`):

1. **Coarse matching.** For each of S = 30 restarts, draw b = 10,000 rows from each space and run k-means with
   C = 30 on each. Then match the two sets of 30 centers by the permutation that maximizes their linear CKA.
   That permutation search is a Koopmans–Beckmann quadratic assignment problem:
   `argmax_P Tr(K_A P K_B Pᵀ)` over the centered kernels. They solve it with MPOpt (Hutschenreiter et al., 2021,
   via `pylibmgm`).
2. **Average.** The coarse correspondence is `M = 1/(SC) Σ_s A_sᵀ P_s B_s`, the mean over restarts of the
   center cross-covariances.
3. **Readout.** Match `X M` to Y one-to-one with the Hungarian algorithm in random blocks of b, then fit W by
   orthogonal Procrustes, `W = polar(Xᵀ T Y)`.
4. **Refinement.** Run R = 100 alternations of batched Hungarian matching of `X W` to Y followed by
   Procrustes.
5. **Known pairs.** If p pairs are available, they are added to every Procrustes step with weight k/p, so they
   carry the same total weight as the k pseudo-pairs. In the QAP they enter as a linear term.

**Language embeddings** (`modalities/image_captions/encoders.py`, `generative.py`):
- **MPNet and Qwen3-Embedding:** sentence-embedding models with their own pooling.
- **Qwen3 "mean":** the mean of last-layer states over the chat-formatted text.
- **Qwen3 "gen":** generative token pooling (Wang et al., 2026). The caption is wrapped as "Imagine what it would
  look like to see: {caption}" with thinking mode on. The model decodes greedily for up to 128 tokens, and the
  embedding is the mean of the last-layer states that produce the generated tokens.

Images are the mean over all last-layer tokens of DINOv2, DINOv3, iBOT or Franca.

**Metric.** FOSCTTM is the fraction of samples closer than the true match: 0 is perfect and 0.5 is chance. It
is computed on 40,504 MS COCO val2014 pairs that the aligner never saw. The two training sets are the two
disjoint halves of COCO train2014.

## Results (as stated on the project page and in the repo README)

- **Unpaired alignment works.** It works across 7 vision models × 3 language models on COCO, SPC, DCI and DOCCI,
  and across datasets. The alignment is coarse: quality depends on the model pair and the caption style. Qwen3
  generative pooling stays close to chance on long, detailed captions (SPC, DCI, DOCCI).
- **Geometry predicts alignability.** Across 84 vision model × language model × dataset combinations, CKA
  explains alignment quality with R² = 0.73 and Spearman ρ = −0.90. Across 14 further modality pairs from seven
  fields, R² = 0.69 and ρ = −0.82.
- **Few pairs.** With ≤ 20 known pairs, their FOSCTTM is 14–28× lower than the best of seven pair-based methods
  (linear, orthogonal, ASIF, LocalCKA, SUE, STRUCTURE, SOTAlign). Six of those need 100–500 pairs to catch up,
  and SUE never does.
- **Other domains.** Competitive with mini-vec2vec on Natural Questions (text↔text), lower FOSCTTM than SCOT+ on
  PBMC single-cell data, and lower than Platonic Brain on NSD fMRI.
- **Text-to-image without pairs.** A DiT-DH-S RAE diffusion model, trained on ImageNet images only and
  conditioned on the mean DINOv2-B latent, generates from MPNet or Contriever captions mapped into DINOv2 space.
  The scenes are reasonable but often miss fine details.

## What their pipeline already does well

Read the code before claiming to improve it:
- Both spaces are centered and unit-normalized before every step.
- The QAP solver is strong: MPOpt with fixed seeds, with an ablation against other solvers in their Fig. 7.
- Every baseline is checked against its official code.
- Runs are bit-reproducible.

A suggestion of the form "center your embeddings" or "use a better QAP solver" would be wrong. We checked both
before writing `response.md`.
