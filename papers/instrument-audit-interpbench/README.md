---
title: One Grokked Circuit Is Not a Certificate
type: research-documentation
status: draft
updated: 2026-10-05
---

# One Grokked Circuit Is Not a Certificate: Auditing Three Interpretability Instruments Against 84 Known Circuits

[The paper](paper.md) is a short method-audit note. This lab had calibrated three in-house
interpretability instruments — a gradient×activation attribution, a direct-logit write-site
scan, and an input-concept subspace causal trace — on a *single* known circuit each (a grokked
modular-addition transformer, and a known numeric circuit on Pythia-160M). The note asks
whether those single-circuit verdicts transfer: we score all three instruments, plus standard
baselines, against the ground-truth circuits of 84 of the 86 InterpBench models
(Gupta et al. 2024), reporting per-model node-level ROC-AUC and edge-level ROC-AUC, with four
preregistered predictions and a hash-frozen scorer.

Measured means across 84 models: activation patching 0.941, EAP-IG 0.924, EAP 0.883 (the
published ordering); gradient×activation 0.642 (centered-std) / 0.783 (magnitude); write-site
0.484 (baseline-relative) / 0.693 (raw); subspace trace 0.772 (random-subspace control 0.657,
rank-1 0.761); random null 0.498. Two of the three single-circuit verdicts transferred in
direction (the gradient attribution is disqualified for node localization; the write-site
scan's scope boundary holds, so its mandated form is below chance for circuit-node recovery);
the third was falsified — the subspace trace's single-circuit failure did not reproduce, though
its own control still denies it concept-specificity (it beats a matched-rank random subspace by
only ~0.11–0.17 AUROC), so it is a degraded activation patch, not a concept localizer.

- [`paper.md`](paper.md): the note (~5–6 pages) — motivation (calibrate before you trust, and on
  how many circuits), the benchmark and ground-truth node set, precise definitions of every
  method and baseline, the preregistration with the one disclosed post-freeze null correction
  (which flipped P2), the full results (headline, edge-level, categorical/regression split,
  per-prediction verdicts, per-method deployment constraints), what transfers from one grokked
  circuit and what does not, threats to validity in full, and a recommendation for what a method
  audit should report.
- [`figures/README.md`](figures/README.md): the two figures the paper needs and their data file.

Every AUROC is MEASURED — recomputed from the frozen per-model result files
(`results/full.json`, `results/edge_full.json`) in the experiment folder
`saturn/experiments/2026-10-05-interpbench-method-audit/` — and traceable through the
reproducibility appendix (preregistration, frozen SHA-256 hashes, run records, and the
HuggingFace ground-truth commit). Interpretations are labelled ASSERTED. One load-bearing
caveat: inputs are sampled in-distribution to match the benchmark's sampler rather than its
compiled generator; the gold baseline reaching 0.94 bounds the damage, but absolute AUROCs may
shift under the original generator.
