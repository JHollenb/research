---
title: Certified Semantic Circuits in FLUX.2
type: research-documentation
status: published
updated: 2026-09-22
---

# Certified Semantic Circuits in FLUX.2

[The Circuit That Survived Its Coordinates](paper.md) reports causal evidence for a distributed semantic route in FLUX.2 Klein 4B, certified with nine frozen promotion gates across twenty prompt contrasts, and shows why single-step activation patching cannot see it.

- [`paper.md`](paper.md): the full paper.
- [`figures/`](figures/): Figures 1–3.
- [`verifier/`](verifier/): the single-file CPU verifier for the Pythia-70M port of the proof grammar (§10). Run `python verify_pythia_induction.py --suite all --developmental-control --device cpu --strict-reference --output certificate.json` after `pip install -r requirements.txt`; a passing run ends with `VERDICT: STRICT REFERENCE PASS`. Its SHA-256 matches Appendix B.
- [`corrections/`](corrections/): additive corrections to the underlying panel.

## Revision 2026-09-22

§8.2 previously said the fitted second-order response model "achieves real steering." On the same panel, simple fixed-dose envelopes beat it (full dose 0.493, late dose 0.426, fitted optimum 0.395 mean contrast progress). The abstract, contribution 5, §8.2 and the conclusion now report the baseline table and describe the fitted model as a compact description of the response, not a better controller.
