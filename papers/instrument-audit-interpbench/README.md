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
baselines, against the ground-truth circuits of all 86 InterpBench models (Gupta et al. 2024;
84 Tracr-compiled aggregated, two IOI reported separately), reporting per-model node-level and
edge-level ROC-AUC, with preregistered predictions and hash-frozen scorers.

The audit was **re-run with the benchmark's own data generators** (Tracr/iit) on all 86 models
— replacing the first pass's synthetic in-distribution sampler — and the **no-embedding** node
universe is the primary metric (the embedding is a trivial ground-truth positive on 83/84
models). Measured no-embedding means under the real generator (84 Tracr): activation patching
0.990, EAP-IG 0.976, EAP 0.892 (edge 0.868 / 0.894); both lab instruments at chance in their
mandated forms (grad×act 0.499, write-site 0.462, null 0.493), rescued by dropping their one
carried deployment constraint (grad×act no-norm 0.842; write-site no-baseline 0.708–0.809); the
subspace trace (0.665) indistinguishable from a matched-rank random subspace (0.644). The
headline: the method ranking is **robust to the data generator** — every per-method mean shifts
< 0.1 (max 0.083), ordering preserved (Spearman 0.98), so **P5/P6/P7 pass** and the frozen
all-nodes P1–P4 keep their status. All three single-circuit verdicts transfer *in direction*;
what fails is each instrument's carried deployment constraint. The first pass's "P3 falsified"
is corrected — it was an all-nodes embedding artifact; on the no-embedding universe the subspace
trace's single-circuit failure **replicates** (concept edge +0.021). The two IOI models (scored
with a validated LayerNorm forward) show even gold patching uninformative (0.50) under the
benchmark's non-contrastive corruption — a property of the IOI generator.

- [`paper.md`](paper.md): the note (~5–6 pages) — motivation (calibrate before you trust, and on
  how many circuits), the benchmark and ground-truth node set, precise definitions of every
  method and baseline, the preregistration with the one disclosed post-freeze null correction
  (which flipped P2), the full results (headline, edge-level, categorical/regression split,
  per-prediction verdicts, per-method deployment constraints), what transfers from one grokked
  circuit and what does not, threats to validity in full, and a recommendation for what a method
  audit should report.
- [`figures/README.md`](figures/README.md): the two figures the paper needs and their data file.

Every AUROC is MEASURED — recomputed from the frozen per-model result files in the experiment
folder `saturn/experiments/2026-10-05-interpbench-method-audit/`: first pass `results/full.json`
+ `results/edge_full.json` (synthetic, all-nodes), real-generator rerun `results/real_full.json`
(86 models, both universes, 15 methods) + `results/real_edge_full.json` + `results/rerun_analysis.json`.
Traceable through the reproducibility appendix and Changelog (two preregistrations, frozen
SHA-256 hashes, run records, the HuggingFace ground-truth commit). Interpretations are labelled
ASSERTED. The first pass's load-bearing caveat — an in-distribution synthetic sampler standing
in for the benchmark's compiled generator — is now **closed**: the rerun uses the real
generators on all 86 models and the method ranking is unchanged (P5/P6). The forward is
validated against an independent TransformerLens implementation (Tracr relmax 3.7e-5; IOI
LayerNorm forward 2.1e-6).
