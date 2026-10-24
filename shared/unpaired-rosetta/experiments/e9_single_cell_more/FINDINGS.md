# FINDINGS — E9: do the CITE-seq results hold on PBMC and SNARE-seq?

Written 2026-10-24 by the coordinator from NOTES.md and `../results/e9_single_cell_more/e9_merged_summary.json` (spot-checked). Status: COMPLETE. All numbers MEASURED on Beast via mrun unless marked.

## Short version

Schnaus et al.'s own loaders support exactly three single-cell pairs without external pipelines: CITE-seq (E8), PBMC and SNARE-seq. On all three, a rotation exists and no removable nuisance axis explains the failure. The pairs-free score S1 picks a near-best run when runs vary (CITE-seq, SNARE-seq) and has nothing to pick when they do not (PBMC, which is already near the oracle).

| pair | CKA (paper) | oracle orth / linear | their result (paper) / our 5-seed canary | 12 seeds: mean ± sd | S1-selected (best by truth) | Spearman(S1, -FOSCTTM) | removing top PC |
|---|---|---|---|---|---|---|---|
| CITE-seq (E8) | 0.961 (0.96) | 0.073 / 0.074 | 0.225 / 0.221 | 0.184 ± 0.095 | 0.089 (0.089) | 0.84 | hurts (0.337 vs 0.200) |
| SNARE-seq | 0.855 (0.86) | 0.143 / 0.144 | 0.209 / 0.178 | 0.233 ± 0.137 | 0.149 (0.144) | 0.82 | hurts (0.259 vs 0.198) |
| PBMC | 0.898 (0.90) | 0.074 / 0.078 | 0.089 / 0.088 | 0.0895 ± 0.0043 | 0.096 (0.082) | 0.32 | not run |

## Reading

- **A rotation exists on all three.** The oracle is below their reported result on CITE-seq (0.073 vs 0.225) and SNARE-seq (0.143 vs 0.209), and equal on PBMC (0.074 vs 0.089), where their search already succeeds.
- **S1 selection works when runs vary.** On SNARE-seq the selected run (0.149) is within 0.005 of the best run and well below the 12-seed mean (0.233). On PBMC the spread is 0.004, so selection has nothing to gain; the selected run (0.096) is slightly worse than the mean (0.0895). This was pre-registered as not applicable.
- **No removable nuisance axis.** The registered type rule (minimum held-out R² over each modality's top-5 PCs) flagged SNARE-seq as "nuisance" because its 4th and 5th PCs (4.6% and 3.0% of variance) are not predictable from the other modality. The registered removal control contradicts that: removing the top PC hurts and destroys the S1-truth agreement (Spearman 0.09), so the top axes are shared signal. POST HOC refinement: the useful test is whether a high-variance top PC is unpredictable (as in long-caption generative text, top PC 13.8% of variance with R² 0.16), not whether any of the top five is.

## Caveats

- SNARE-seq's oracle (0.143) is looser than the others, with small dimensions (10 and 19) and about 523 training cells.
- Our SNARE-seq canary (0.178) is below their 0.209; FOSCTTM, LTA and CKA match on PBMC and CKA matches on all three.
- One aligner configuration (their defaults). Human vs mouse scRNA and histology vs expression were not run (external pipelines).
- One 3-seed SNARE shard hit the 30-minute job cap and was re-run as single-seed shards; the final 12 seeds are complete.
