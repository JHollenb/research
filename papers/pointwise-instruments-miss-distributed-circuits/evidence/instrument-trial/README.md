# Blind-Graded Comparison: Standard Readouts vs. the Model's Own Output

Receipts and an offline verifier for §5 of [Single-Site Tests Miss Distributed Stores](../../paper.md). Each case pairs a standard interpretability readout with a check of what the unchanged downstream model actually produces from the same internal state, on the same model, prompts and seeds.

## Quickstart

```bash
pip install .
instrument-trial-verify
```

The verifier (standard-library Python, no GPU) checks every receipt against `bundle/manifest.json`, re-derives each case's verdict from the raw receipt values with the frozen decision rules, and compares the results with `verdicts/expected.json`. Exit code 0 means everything reproduces.

## Cases

| Case | Standard readout and verdict | Output check | Blind grade (standard arm) |
|---|---|---|---|
| 1. Identity route (FLUX.2) | single-component, single-step patching over 4 sites × 4 steps: "no necessary component" (≥ 22% of the transition survives every cell) | ablating the same 4 components at every step removes the transition (0.13% remains); inserting them carries it (91%), held-out seeds | misreport |
| 2. Foreign-encoder subject rows (FLUX.2) | nearest-class-mean probe, 16/16 on held-out native states: "no decodable content" (top-1 tiger, margin 0.035 vs floor 0.352) | transplanting the 2 subject rows into a native fox run renders a wolf on both seeds; noise sham flat | misreport |
| 3. Cross-model direction transfer (Qwen) | transferred difference-of-means direction, bit-identical to the original pipeline: 95.4% negative cosines, "representations differ" | native cosines 0% negative in every model; the split falls to 0.0 under mean-centering; a low-split control model reads 0.0 | misreport |
| 4. Reconstruction cosine (FLUX.2) | cosine 0.993–0.997 on held-out prompts: "state recovered" | a content-free mean template scores the same; rendered, the reconstruction differs from native by pixel MAD 70–97 and shows the wrong animal | misreport |
| 5. Step-wise mediation (control) | "mediation holds at the measured step" | holds in 17/18 step × axis cells | inconclusive |
| 6. Zeroed logits (reserve) | "a zeroed answer logit is a maximal knockout" | all 76 zeros are at the final layer, where RMSNorm(0) followed by a bias-free unembedding is zero by arithmetic | misreport |

The preregistered criterion (the standard arm misreports in at least 3 of cases 1–4) was met at 4 of 4. The grader was a fresh model instance with no project context, given only the rubric and anonymized readings; its raw output is `bundle/grading/grader-raw.json`. In the grading files the two arms appear under their original internal labels; `standard` and `output_check` in `verdicts/` are the same two arms.

## Limits

- The standard arms are the author's implementations of each recipe, not third-party libraries. TransformerLens does not load FLUX; nnsight and pyvene can hook a diffusion denoiser as a generic module but were not used. No sparse-autoencoder method is included here (see the paper's SAE experiment).
- Cases were selected because the author expected the standard readout to fail there, and the ground truth comes from the output-check arm. This shows the failure modes exist; it does not estimate how often they occur.
- Two grading disclosures are kept as they happened: the grader declined to decide case 5, where the author expected a match, and one arm-order assignment was transposed relative to the preregistered rule (blinding unaffected).

[TRAPS.md](TRAPS.md) lists seven measurement traps that produced confident wrong answers during this work.

Host-specific paths and hostnames in the receipts were replaced with placeholders after the runs; see `REDACTIONS.md`.
