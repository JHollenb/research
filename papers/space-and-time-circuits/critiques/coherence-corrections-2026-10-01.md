# Definition and receipt coherence corrections

This pass repairs the connection between the paper's definitions, experimental criteria and current measurements. It adds no model runs and changes no frozen thresholds or historical results. The pre-update paper directory is preserved by research commit `369ab87`.

## Changes and their justification

| Change | Reason | Evidence |
|---|---|---|
| Define a space circuit by meeting a declared singleton criterion, rather than by any measurable effect | The old wording made a partial singleton effect count as both localized control and a time-circuit singleton null. Decision criteria and numerical effects must have distinct meanings. | Existing FLUX bars P ≥ 0.90 / P ≤ 0.15 and LM bars 0.25 / 0.2; no bars changed |
| Quantify over every singleton at one cut, grain, observable and panel aggregation | A mean over decisive and inert sites cannot establish the singleton claims. Changing from formed K/V to a residual write changes the intervention being certified. | Full E1b step sweep; E17 formed-cache writes; the current section 2.3 separation of source formation from formed-state control |
| Put the four FLUX criteria beside their measured bounds in section 5.2 | Readers can assess the complete result directly, without relying on an assurance that the definition was met or inferring it from separate sections. | [Bundled joint-region report](../evidence/time-signature/joint-region-report.json), `job-67631847af7f`: 15/15 setup/site-set combinations, with singleton and joint coverage |
| Bundle current FLUX reports and a stdlib verifier | The committed argument now includes the saved measurements underlying this certificate, rather than requiring access to another repository to check its arithmetic. | [Bundle and hashes](../evidence/time-signature/README.md); byte-identical copies of the collected E1b and E7 reports |
| Keep the five-seed color result identified as necessity evidence | E7 did not run a sufficiency sweep. It corroborates the necessity half rather than supplying five complete four-quadrant replications. | [Color necessity report](../evidence/time-signature/color-necessity-report.json), `job-8d4a3845a671` |
| Correct E17's count and numerical contracts | The original five-job/ten-cell wording preceded Gemma. Six report directories now contain twelve identity/color cells. Isolated-write and split-replay no-ops are different measurements. | [E17 findings](../../../../saturn/experiments/2026-09-30-full-layer-sweeps/FINDINGS-E17-isolated-kv-writes.md) and all six reports: maximum isolated-write no-op 4.1246414e-5 nats; maximum split no-op 9.8228455e-5 |
| Replace the claim that only Qwen has an early write leak | The same E17 findings explicitly record Gemma L2 at 0.15–0.17 in-forward versus ≤ 0.006 isolated. Both models retain strong late isolated writers. | E17's Qwen and Gemma paragraphs; Qwen L23 0.808077 and Gemma L22 0.809070 |
| Describe the all-layer gain as 1.000 to recorded precision | A rounded normalized gain is not an exact equality or an independent bitwise replay measurement. | E17 normalized all-layer summaries and separately reported no-op values |

## Verification

The [offline verifier](../evidence/time-signature/verify.py) recomputes progress from retained MAD values and checks report identity, specimen, complete singleton coverage and zero image no-ops. All 15 combinations meet the four declared FLUX criteria. It separately recomputes source/target/null nearest classes for the historical and residual color-route arms; no recorded class disagrees.

The original FLUX deletion misreading remains a labeled historical correction in section 5.5: `dp ≈ 0` can denote a null image. The current result is read against the source, target and null references. Norm-matched shams also produce null images, so deletion is reported separately from the more specific source interchange.

The method supports an operational path-distributed certificate and retains its partial effects. The paper's formation, dose and ordering measurements characterize the execution mechanism separately. Its additive account can therefore be assessed on the same definitions as an interacting account; a nonlinearity requirement has not been added to the certificate.

The concurrent E14 recovery, architecture definitions and E10 admission/timing edits are preserved. Historical review snapshots describe earlier copies and remain historical rather than being rewritten into reviews of the corrected manuscript.
