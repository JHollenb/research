# E4 design: consumer-closed validation of an unpaired map (planned)

## Question

Their text-to-image demo conditions a generator directly on mapped embeddings, and FOSCTTM cannot say whether
a map is good enough to drive a generator. We can test the read/author split (response.md, Claim D) on a
consumer with causal ground truth: the frozen FLUX.2 Klein 4B denoiser. For it we have exact replay, the
native-donation ceiling, and norm-matched shams.

## Plan

1. **Bank.** Grow the 18-animal bank into a 200-symbol bank: single-token nouns in both tokenizers, crossed
   with 4 distinct prefixes (template collapse makes more prefixes redundant). Encode the subject-row
   displacements on both sides: SmolLM2-1.7B with the TECM recipe, and the Klein-Qwen conditioner. This is
   one mrun job, reusing `saturn/workers/run_saturn_symbol_table_bridge.py` with a bank override.
2. **Unpaired map.** Fit their `WassersteinProcrustes` with zero pairs on the two displacement sets. Report:
   - FOSCTTM on held-out prefixes;
   - per-symbol α = cos(W x_s, y_s);
   - the E0 class-QAP correspondence.
   This step is offline.
3. **Consumer.** For about 24 symbols spread over the α range, write the mapped displacement at the fox subject
   rows (norm-matched) and render through the unchanged suffix: 256², 4 steps, seeds 7217/31337. Score
   progress P toward the native target render. Controls: native direction (positive), shuffled-map sham,
   zero-dose no-op (must be exactly 0).
4. **Prediction (frozen before step 3).**
   - P rises with α (Spearman ρ(P, α) > 0, bootstrap 95% interval excluding 0). The Wall-A zones (α ≥ 0.895
     rendered, α ≤ 0.50 failed) are checked as a replication of FLUX's own scale, not used as a bar.
   - Once α is known, retrieval rank adds little: report the partial correlation of P with rank given α,
     and the gain in R² over α alone, each with a bootstrap interval. P is used as a continuous score, with no
     render cutoff.
   - Falsified if rank predicts P better than α does, meaning the bootstrap interval of R²(rank) − R²(α) lies
     above 0.
   - *Revised 2026-10-09, before anything was built.* The first draft used a P > 0.3 render cut and a ΔAUC < 0.05
     bar. Neither number was grounded, so both were removed.

## Why this helps them

It gives a generation-grounded acceptance test for any unpaired map, where they currently have only CLIPScore,
VQAScore, TIFA and CycleReward on RAE samples. It also gives the α threshold a consumer must clear, which tells
them how many anchors (Claim E) a deployment needs.

## Status

Not built. It needs the private Saturn worker and mrun. TODO: a public path through `saturn-pub` and
`mrun-pub` once the FLUX adapter ships there.
