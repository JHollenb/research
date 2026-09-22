---
title: Single-Site Tests Miss Distributed Stores
type: research-documentation
status: published
updated: 2026-09-22
---

# Single-Site Tests Miss Distributed Stores

[The paper](paper.md) shows measured cases where single-site activation patching reports "no necessary component" while the same components across all diffusion steps, or the same token's key/value entries across the second half of a language model, both remove and carry the behavior. It also reports a preregistered, blind-graded comparison in which four standard readouts gave the wrong verdict in 4 of 4 graded cases.

- [`paper.md`](paper.md): the paper.
- [`figures/`](figures/): Figures 1–3, decoded from the bundled receipts.
- [`evidence/ird-certificate/`](evidence/ird-certificate/README.md): receipts and render panes for the four-quadrant tests; `python3 verify.py` re-checks 35 file hashes and re-derives the headline values.
- [`evidence/instrument-trial/`](evidence/instrument-trial/README.md): the blind-graded comparison; `pip install . && instrument-trial-verify` re-checks every receipt hash and re-derives every mechanical verdict.

The receipts are unmodified scheduler records, so they include the original host paths; they are hash-pinned and are not edited here. The comparison arms are the author's implementations of standard recipes, not third-party libraries, and no sparse-autoencoder method was tested (see §5 and §6 of the paper).
