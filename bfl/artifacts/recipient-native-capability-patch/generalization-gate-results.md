---
title: "Ship the Hotfix — Results"
type: experiment-results
status: complete
created: 2026-08-18
runs:
  compile-smoke: [job-a7d92f9d1963, job-78285314483c, job-5673d7a72fcf]
  compile: [job-f68d68511556 (failed: sham device bug), job-cd5ef02ca1f4 (stopped_detector_misfire), job-562eb7e8e771 (stopped_detector_misfire), job-7080f8e2ac0d (killed_ram), job-9b2064bdab99 (complete)]
  audit-matrix: [job-0444f1d01bfd]
  audit-collateral: [job-700d4c389b14]
package_sha256: abd690d78d40fc225303f37567fe59f13384abd4c66fd124eb85bbc0e0a989b9
claim_status: preregistered-ship-gate-failed-on-collateral-generalization-positive
---

# Ship the Hotfix — Results

**One-line verdict.** The preregistered ship-gate ran end-to-end on the shipped distilled Klein 4B: generalization **passed** (paraphrase, resolution, object family, and the count-5 class repair all replicate held-out; +27.8 exact-count points on the sealed apple panel with both evaluators agreeing), the donor-free fresh-process serving proof **passed**, and the collateral safety gate **failed** — the binary count-detector fires on 48% of ordinary non-count prompts and visibly rewrites them (p95 RGB-MAD 41.5 vs the ≤ 6.0 gate). **The hotfix does not ship.** The gate did exactly what it was designed to do: convert a plausible product claim into a measured boundary.

## Gate table

| Gate | Requirement | Measured | Verdict |
|---|---|---|---|
| G1 gap direction (dev) | Base > distilled, both evaluators | independent 0.70 > 0.267; atlas 0.70 > 0.267 | **PASS** |
| G2 held-out repair (apple-512, 90 cells) | gated − native ≥ 15 pts, atlas ≥ 0, disagreement ≤ 20% | +27.8 pts (23.3%→51.1%); atlas +22.2; disagreement 6.0% | **PASS** |
| G2 gating vs fixed | gated ≥ fixed on the 45-cell join | 0.0 pts (tie — binary gate ≡ fixed on count prompts, as designed) | **PASS** |
| G4 resolution | non-inferior at 256, direction at 1024 | 256: 33.3% = 33.3%; 1024: 33.3% → 66.7% | **PASS** |
| G5 controls | zero-dose + uninstall byte-exact; parity exact | all byte-exact; parity exact at 256/512/1024 | **PASS** |
| G6 fresh donor-free serving | 6 held-out cells, donor path nonexistent | 6/6 rc=0, regime fired as packaged, collateral cell abstained | **PASS** |
| G3 collateral safety (120 prompts) | median MAD ≤ 2.0 and p95 ≤ 6.0 | median 0.0; **p95 41.5**; fires on 58/120 (48%) | **FAIL** |

## The measured generalization map

Apple panel exact-rate by requested count (18 cells each, native → gated):

| N | native | gated | reading |
|---:|---|---|---|
| 3 | 14/18 | **18/18** | already-working counts are not harmed |
| 4 | 3/18 | 9/18 | +6 |
| 5 | 3/18 | 12/18 | +9 (the admitted specimen class) |
| 6 | 0/18 | 1/18 | essentially unchanged |
| 7 | 1/18 | 6/18 | +5 |

Family transfer (template-0/2, counts {3,5,7}, 18 cells each): blue circles 7→12, green bottles 6→12, red strawberries 7→15. The repair is not apple-specific.

Count-7 fresh-serve cell rendered **5** — the single default-regime act is a count-5-class attractor, not a count-preserving operator across N. The per-count bank intended to fix this could not be gated (below).

## What was falsified, with receipts

1. **Count-value detection from pooled route state.** The regime-selecting ridge detector (leave-one-out over 23 dev states) collapsed: every count sample predicts ~4.7–5.1 regardless of true count (3→5.08 … 7→4.68) while non-count states separate cleanly negative. Binary count-present/count-absent detection cross-validates at **1.0**; the count value itself is not linearly decodable from the mean-pooled `joint.2` text state at this sample size. Two `stopped_detector_misfire` runs (job-cd5ef02ca1f4, job-562eb7e8e771) are the immutable evidence; the per-count bank remains in the package but is unreachable by any honest gate.
2. **Collateral selectivity.** The binary detector's abstain boundary does not transfer to open prompts: 58/120 ordinary scenes fire (median MAD 31.3 on fired rows). The shuffled-signature control also fires 20/20 — in the selected k=4 PCA space a permuted projection rarely crosses the threshold, so that control is uninformative in binary mode (recorded as a control weakness, not a pass).
3. **Wrong-site specificity (control battery).** The repair survives a `joint.3` write (observed 5); only wrong-time (step 1) separates cleanly (3). Sign-flip moves the count to 6 rather than reverting — direction-sensitive but not sign-symmetric.

## Amendments (all before any held-out render, receipts above)

- **Detector redesign** (after the two misfire stops): raw 3072-dim ridge → standardized PCA(k∈{4,8,16}) + ridge(α∈{1,10,100}), LOO-selected; then, on the LOO collapse, mode amended to `binary_default_regime` firing the admitted count-5 act at its controller-selected gain. The canonical compile check was amended from "predicted regime == true count" to the behavioral "gated arm repairs the canonical cell" — justified by the measured adjacent-regime equivalence (a regime-4 act repaired count-5) and because the ship question is repair, not prediction.
- **Sham control device bug** (job-f68d68511556): CPU/CUDA tensor mix in `random_sham_patch`; fixed to compute the reference norm as a Python float.
- **RAM reservation** (job-7080f8e2ac0d, killed at tree RSS 48.9GB): fresh-child spawn after parent release needed `malloc_trim`; compile reservation raised to 44GB on measured peaks.
- **Matrix scope** (preregistration deviation, stated in README): ~230-cell decisive subset of the review's ~1080-cell matrix; full paraphrase×count coverage on apples, families and resolutions on declared subsets.

## G3 post-mortem via Saturn (job-3e94680b28d5, 2026-08-18)

Artifact-only analysis of the collateral panel found firing predicted by the prompt's *style word* (watercolor 58/60 fired, photorealistic 0/60; subject irrelevant). A Saturn debug job (one lease, distilled + package only, checkpoint capture + read-only state inspection + patched suffix replays) confirmed the mechanism at the state level:

- **The detector score tracks rendering register, not objects.** Style-word vs score correlation **0.928**; salient-object-multiplicity vs score correlation **0.029**. A watercolor scene with 1 salient component scores 3.87 (fires); a photorealistic scene with 12 components scores 0.50 (abstains).
- **The style swap is decisive.** The same subject ("a vintage bicycle") scores 1.96 as a photorealistic prompt (abstain), 4.37 as watercolor (fire), 3.84 as flat illustration (fire). The score follows the adjective.
- **No 1-D threshold can fix it.** True count prompts score 3.50–3.66 — inside the watercolor band (2.56–3.95), which also contains the threshold (2.5). Photorealistic (0.49–1.94) sits below. The bands overlap by construction because the training labels were style-confounded: all 15 count states came from flat-illustration prompts, the 8 noncount dev states were half photorealistic — under leave-one-out the best binary separator was the style axis. The LOO accuracy of 1.0 was measuring register separation, not count detection.
- **The damage is the act write, dose-scaled.** On fired watercolor prompts, native-vs-gated MAD grows monotonically with gain (8.7→18.4→45.7 and 12.7→21.4→33.6 at 0.5/1.0/2.0); zero-dose remains byte-exact. The packaged gain 2.0 sits at the steep end for foreign-register scenes.
- One dev noncount prompt scored 6.09 at the audit seed (training captures used other seeds), i.e., even the training distribution's abstain boundary is seed-sensitive.

**Root cause:** a training-label confound (style register correlated with count labels in 23 dev states) plus a 1-D abstain rule on a feature that is 93% style. **Fix requirement for any rerun:** style-balanced negatives (flat-illustration-register noncount prompts: "a clean flat illustration of a single red apple"), a second feature (e.g., diagram-register score *and* count-band score), or an abstain boundary validated on open prompts before the collateral gate. Instrument caveat: the multiplicity proxy is color-masked and misses grayscale/other-hue objects (two watercolor scenes scored 0 components) — correlation conclusions stand, absolute component counts do not.

The debug job receipts, census (33 prompts with pooled-state scores and PCA projections), style-swap rows, dose-response rows, and native renders are in `results/job-3e94680b28d5/report.json`.

## Ship configuration (for the record)

Package `abd690d7…` (554,702 bytes fp16): five rank-8 route Acts at `joint.2/text/step 0` (gains 1.0/2.0/2.0/2.0/2.0 for N=3..7, promoted by `DeterministicCheckpointController` with verified ledgers), binary PCA(4)+ridge detector (LOO 1.0), default regime 5. Donor runtime not required; prompt lookup absent; detector reads state only. Provenance control (random-orthogonal-basis act through the same dose controller) accepted gain 2.0 — its separation evidence is in the compile report's dose ledger.

## Claim boundary

A preregistered, dual-evaluator, collateral-gated audit of a donor-free recipient-native counting hotfix on one shipped distilled model. Positive: the repair class generalizes across paraphrase, resolution (up), and object family, is uninstallable byte-exactly, serves from a fresh process with the donor path nonexistent, and improves the sealed count panel by +27.8 points. Negative: it is not collateral-safe (over-fires on ordinary prompts), not count-value-selective, and not count-preserving across N. Not a shipped product; not a universal counting capability. The next missing component is named precisely by the failure: an abstain boundary that transfers to open prompts.
