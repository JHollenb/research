---
title: Single-Site Tests Miss Distributed Stores
type: research-documentation
status: published
updated: 2026-09-22
---

# Single-Site Tests Miss Distributed Stores

[The paper](paper.md) shows measured cases where single-site activation patching reports "no necessary component" while the same components across all diffusion steps, or the same token's key/value entries across the second half of a language model, both remove and carry the behavior. It adds a preregistered comparison with a standard sparse-autoencoder workflow (SAELens, public GPT-2 and Gemma Scope SAEs; GPT-2 cross-checked in TransformerLens) and a blind-graded comparison in which four standard readouts gave the wrong verdict in 4 of 4 graded cases.

- [`paper.md`](paper.md): the paper.
- [`appendix-execution-model.md`](appendix-execution-model.md): how the exact capture-and-replay experiments are run, how that compares with TransformerLens, nnsight and pyvene, and measured costs.
- [`experiments/2026-09-22-sae-comparison/`](experiments/2026-09-22-sae-comparison/): preregistration, standalone script, requirements, and every result file for the SAE and language-model panel.
- [`figures/`](figures/): Figures 1–3, decoded from the bundled receipts.
- [`evidence/four-quadrant-tests/`](evidence/four-quadrant-tests/README.md): receipts and render panes for the four-quadrant tests; `python3 verify.py` re-checks 37 file hashes and re-derives the headline values.
- [`evidence/instrument-trial/`](evidence/instrument-trial/README.md): the blind-graded comparison; `pip install . && instrument-trial-verify` re-checks every receipt hash and re-derives every mechanical verdict.

Host-specific paths in the receipts were replaced with placeholders after the runs; original file hashes are listed in each bundle's `REDACTIONS.json`. The blind-graded comparison arms are the author's implementations of standard recipes; the SAE comparison uses public libraries and SAEs (see §4.4, §5 and §6 of the paper).
