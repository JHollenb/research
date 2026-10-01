# FLUX time-circuit signature

This bundle supports the four-quadrant result in [section 5.2 of the paper](../../paper.md#52-built-over-time). The reports are byte-identical copies of the collected Saturn records. No fields were redacted, no images were regenerated, and no historical result was changed.

| File | Job | Measurement | SHA-256 |
|---|---|---|---|
| `joint-region-report.json` | `job-67631847af7f` | Single-step and all-step writing and source replacement; three setups × five site sets | `799f173989898f8d9d5465a717038ec0cc094cf970388dcf9c109f7190f2f4d2` |
| `color-necessity-report.json` | `job-8d4a3845a671` | Five-seed single-step/all-step color necessity; source, target and null image distances | `2ad48f08f0aebc4422c159a3a887eb7a64ebf6b5a5cd31c14ff0da1c4e124e0a` |

Run `python3 verify.py` from this directory, or pass its path from anywhere. The verifier uses only the Python standard library. It checks the pinned reports, complete single-step coverage, zero image no-ops, and all four criteria for each setup/site-set combination. It recomputes target-image progress from the saved distances and nearest source/target/null class from the color report's distances.

The four-quadrant record has 15 combinations sharing three baseline setups. The color record tests the necessity half on five seeds; it contains no write sweep. The verifier checks saved measurements and arithmetic, not fresh native-model execution or semantic image judgments.

The FLUX intervention criteria are target-image progress ≥ 0.90 for sufficiency and ≤ 0.15 after source replacement for necessity. Every singleton is assessed with those same criteria. Partial effects remain visible in the returned ranges. The color panel additionally identifies the nearest reference image: single-step removal stays nearest target, all-step interchange reaches source, and all-step deletion reaches null. A norm-matched sham also reaches null, so the deletion effect alone is not semantic specificity.

Canonical experimental code, plans and additional controls remain in:

- [joint-region experiment](../../../../../saturn/experiments/2026-09-30-flux2-joint01-time-accumulation/PLAN.md);
- [residual deletion correction](../../../../../saturn/experiments/2026-09-30-flux2-residual-deletion/FINDINGS.md);
- [five-seed color experiment](../../../../../saturn/experiments/2026-09-30-e7-flux-color-multiseed/PLAN.md).

The joint-region report's original deletion interpretation was corrected by E1c: a projection near zero can be a null image, rather than target survival. This bundle uses source replacement for the four-quadrant calculation and the corrected nearest-reference observable for the deletion panel.
