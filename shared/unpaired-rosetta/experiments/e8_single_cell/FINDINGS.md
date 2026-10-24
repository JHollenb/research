# FINDINGS — E8: CITE-seq, the "partially aligned" tier of Schnaus et al.

Written 2026-10-24 by the coordinator from NOTES.md and `../results/e8_single_cell/e8_merged_summary.json` (spot-checked). Status: COMPLETE. All numbers MEASURED on Beast via mrun unless marked.

## Short version

Schnaus et al. report CITE-seq (RNA vs surface protein in the same cells) as "partially aligned": FOSCTTM 0.225, with a seed standard deviation of 0.13, even though its CKA (0.96) is the highest of their fourteen scientific pairs. We reproduced their setting exactly and found three things.

1. A rotation exists. Fit on true pairs, one orthogonal map reaches FOSCTTM 0.073 on held-out cells (a general linear map does no better, 0.074). The geometry is shared; the unpaired search is what misses it.
2. Their own aligner sometimes finds it, and a pairs-free score can tell when. Over 12 seeds the seed mean is 0.184 and the seed range 0.089-0.439. The pairs-free self-score S1 (mean cosine of the aligner's own Hungarian-matched pairs) picks the best seed by truth, 0.089, with no pairs. S1 and true FOSCTTM agree across seeds (Spearman 0.84). This turns their "we report average rather than best performance, since without supervision one cannot select the best-performing seed" into a seed they can select.
3. Unlike long-caption text, CITE-seq has no dominant nuisance axis. Every top-5 principal component of each modality is predictable from the other (held-out R² 0.82-0.95), and removing the top component hurts (seed mean 0.337 vs 0.200 matched baseline). The two failures have different causes: a misleading axis in long-caption generative embeddings, pure seed variance in CITE-seq.

## Results

| quantity | value | receipt |
|---|---|---|
| reproduction canary, 5 paper seeds | FOSCTTM mean 0.221, sd 0.132 (paper 0.225, 0.13); CKA 0.9614 (paper 0.96) | NOTES.md, fixed-run receipts |
| true-pair oracle, orthogonal / linear | 0.0727 / 0.0741 | `e8_merged_summary.json` oracle |
| 12-seed baseline: mean, sd, min, max | 0.184, 0.095, 0.089, 0.439 | baseline_selection |
| S1-selected seed | 0.0893 (= best seed by truth) | baseline_selection |
| Spearman(S1, -FOSCTTM): across seeds / pooled iterates | 0.839 / 0.823 | baseline_selection |
| iterate selection within a seed | no gain (0.18369 vs 0.18372 mean) | baseline_selection |
| top-1 PC removed (6 seeds): mean, S1-selected | 0.337, 0.360 (matched baseline 0.200, 0.098) | removal |

## Caveats

- One dataset (1,000 cells), one aligner configuration (their defaults).
- The S1 selection is over 12 seeds; picking the best-by-truth seed is a strong result, but it should be confirmed on more pairs before calling S1 a general selector. On the long-caption corpora (E7) S1 seed selection did NOT beat the mean, so S1 works when the seed spread reflects search luck, not when every seed is misled by the same axis.
- A first pass used a fresh random state where their `run_alignment` passes the one already advanced by the train split; the reproduction canary caught it (mean 0.305 vs 0.225). Pre-fix receipts are quarantined in `../results/e8_single_cell/stale_prefix_randomness/`.
- Human vs mouse scRNA and histology vs expression were deferred (external downloads/pipelines).

## Next

Run the same oracle + S1 selection on their other scientific pairs that their loaders already support (PBMC, SNARE-seq) to test whether S1 selection generalizes, then fold E7 and E8 into a short follow-up note for the authors.
