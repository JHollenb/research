# FINDINGS — E7: can a better start recover Qwen3-gen on DCI and DOCCI?

Written 2026-10-24 by the coordinator from NOTES.md and the receipts in `../results/e7_search_init/` (spot-checked). Status: COMPLETE. All numbers MEASURED on Beast via mrun; holdout FOSCTTM for Qwen3-8B generative pooling (gen) vs DINOv2; bar = 0.10; their unpaired search gives about 0.48 on both corpora; the true-pair oracle gives 0.014 (DCI) and 0.010 (DOCCI).

| start | uses image-caption pairs? | DCI | DOCCI | seeds |
|---|---|---|---|---|
| SPC-fit rotation (top PC removed) as the start, then their refinement | yes, but only on SPC | 0.078 ± 0.008 | 0.051 ± 0.007 | 3 |
| same, applied directly without refinement | SPC only | 0.107 ± 0.013 | 0.100 ± 0.010 | 3 |
| 100 true pairs on the target (their Sec 4.4 protocol) | 100 on target | 0.085 ± 0.002 | 0.100 ± 0.008 | 3 |
| 50 true pairs | 50 on target | about 0.11 | about 0.15 | see NOTES |
| text pivot: gen to Qwen3-Embedding on the same captions, composed with the unpaired Qwen3-Embedding to image map | no | 0.170 ± 0.055 | 0.172 ± 0.026 | 3 |
| the pivot's own unpaired Qwen3-Embedding to image step | no | 0.139 ± 0.051 | 0.136 ± 0.028 | 3 |
| removing more top PCs (2-5), pairs-free | no | chance | chance | 1 |
| pairs-free selection (S1) of iterate or seed | no | no gain | no gain | 1-3 |

## Reading

- **Two recipes recover gen.** Starting their refinement from a rotation fitted on another corpus (SPC) brings both corpora below 0.10, near the oracle. About 100 on-target pairs also works (DCI robustly; DOCCI borderline, 2 of 3 seeds below 0.10).
- **No pairs-free recipe reaches the bar.** The text pivot uses no image-caption pairs and cuts the error about 3× (0.48 to 0.17), but it is limited by its own unpaired Qwen3-Embedding to image step, which their method does at about 0.14 on these corpora with large seed variation. Refining from the pivot makes it worse.
- **Pairs-free selection does not help on this failure type.** S1 picks the last iterate in every run and does not beat the seed mean. S1 tracks true quality only where alignment already works. This is the "misleading direction" type; compare CITE-seq and SNARE-seq (E8, E9), where selection does help.

## Caveats

- Only the pivot uses zero image-caption pairs. Whether a second encoder of the same modality fits their definition of "unpaired" is for the authors to judge.
- The more-PCs and selection cells are seed 0 or few seeds; the headline arms have 3 seeds.
- Four early full-size seed jobs timed out under Beast contention and were replaced by leaner resubmissions (NOTES, deviations).
