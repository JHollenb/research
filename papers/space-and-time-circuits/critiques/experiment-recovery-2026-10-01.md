# Overnight experiment recovery for Space and Time Circuits

Review and recovery on October 1, 2026. **E10's measured headline results are already included; E14 finished overnight and was missing from the manuscript and experiment registry.** Its full report has now been downloaded, checked, and summarized in [the new Falcon hybrid findings](../../../../saturn/experiments/2026-10-01-e14-hybrid-attn-ssm/FINDINGS.md). No model jobs were launched and this review did not edit the paper.

The reviewed manuscript is [A New Class of Circuits: Space and Time](../paper.md). The file changed during this audit. The detailed review used its 11:45:28 PDT copy; a final targeted recheck used the copy with mtime 2026-10-01 11:51:26 PDT and SHA-256 `ceae27fae48fc2d10f8cd3b77eef4ef82ca97dca4436bf82ebd765055be0462a`. The E14 placeholder and the remaining E10, linear-exclusion and Figure 2 issues were still present. Several contradictions noted in the earlier [review](review-2026-10-01_094028_PDT.md) and [clarification](clarification-2026-10-01_110945_PDT.md) were already corrected. The findings below distinguish those repairs from work still owed.

## Inclusion audit

| Experiment | Current outcome | Included in the paper |
|---|---|---|
| E10 non-copied intermediate state | Removal changes 32/32 and 30/30 answers; counterfactual swap authors 15/32 and 30/30 arithmetic targets; recorded remount sequence-logprob delta 0.0 | Yes, section 6.7 and Appendix A. Remaining setup and timing wording needs correction. |
| E14 hybrid attention and SSM | Full Falcon-H1-0.5B sweep succeeded as `job-5efb5697631c`, completing at 01:40:58 PDT | No. Section 6.4 still has an optional TODO, and Appendix A has no result or record path. |
| E8 Klein 9B | Identity has the reported two-seed four-quadrant profile, with 8/9 stricter route gates; lighting is mixed | Yes, section 5.6 and Appendix A. The reproduction registry still calls it optional. |
| E9 SDXL | Whole-path writing is strong, but an early singleton removal is decisive; mixed quadrant profile | Yes, section 5.7 and Appendix A. The reproduction registry still calls it optional. |
| E15 through E19 and Mamba full sweeps | Concentrated or redundant writes, late necessity bands, and retractions of sampled certificates | Yes, chiefly sections 6.1, 6.1b and 6.4. The current copy repairs several earlier summaries. |

The inclusion judgment checks the working manuscript, experiment records, and registry. It is not an independent numerical re-analysis of every older experiment. E10 and E14 were checked directly in this pass. Newer raw experiment records remain under `saturn/experiments/`; prose inclusion does not bundle them into the public research repository.

## Recovered E14 results

The full run used Falcon-H1-0.5B-Base, 36 layers with parallel attention and SSM paths, CUDA FP32, two contexts per behavior, and seed 0. It took approximately 28 minutes. Identity retained 22 admitted items; color admitted 9 of 20, all from one context. The initial full attempt was killed by its VRAM ceiling, then the separately submitted full run succeeded. The failed log and receipt are preserved alongside the successful report.

| Cut removed after the subject prefix | Identity candidate changes | Color candidate changes |
|---|---:|---:|
| All attention K/V layers | 17/22 | 8/9 |
| All SSM state layers | 2/22 | 0/9 |
| Both cuts at all layers | 21/22 | 8/9 |

Attention-all writing into the filler prompt recovers normalized answer-logprob gains of **0.987 identity / 0.956 color**. SSM-all writing recovers **0.345 / 0.172**, and both-all writing is **1.000 / 1.000**. These are normalized logprob effects, not accuracy percentages.

The strongest attention singleton necessity shares are **0.149 at L30** for identity and **0.295 at L23** for color. The strongest attention singleton writes are **0.224 / 0.175**, both at L23. Identity's best six-layer necessity window, L29–34, carries **0.715**, versus **0.193** for its complement; no tested width up to six reaches a median of 0.8. The bootstrap interval for that six-layer share is [0.597, 1.036], so its exact breadth remains uncertain.

The main result is **attention-dominated post-subject dependence with partial SSM writing**. It does not establish the predicted strong, concentrated Mamba-like SSM writer. The SSM's small whole-cut necessity denominator also makes normalized singleton shares unstable; the raw effects and partial writing matter more than the maximum positive ratio. The absence of a large removal effect at this cut does not exclude an SSM role during prefix formation or on other tasks.

Neither attention behavior earns a new strict certificate under the manuscript's scalar bars: identity's best singleton write is 0.224 against 0.2, while color's best singleton necessity is 0.295 against 0.25. Those are near or mixed outcomes worth retaining, rather than evidence that temporal dependence is absent. No residual-write sweep was run for Falcon.

The new [verifier](../../../../saturn/experiments/2026-10-01-e14-hybrid-attn-ssm/verify_record.py) confirms the report's pinned hash, equality to its embedded log payload, collection-log hash, scheduler result, exact submitted source hashes, singleton coverage and window coverage. The [audit JSON](../../../../saturn/experiments/2026-10-01-e14-hybrid-attn-ssm/verification-2026-10-01.json) records these checks. The report retains aggregate medians and intervals, so the verifier cannot independently regenerate the bootstrap calculations from item rows. Standard Saturn evidence sweeping reported an inapplicable empty target because this custom record has neither a top-level gated receipt nor a JSONL stream; it supplies no additional scientific verdict.

## Remaining paper corrections

**Include E14 and qualify the recurring-writer claim.** Replace the section 6.4 placeholder and Appendix A row, and add the record to the reproduction registry. Section 6.5's statement that no attention model in the tested size range avoids a writer should be scoped to its original panel: Falcon's strongest formed-attention write is only 0.224, much weaker than the roughly 0.54–0.99 writers in several earlier cells. The experiment's more interesting outcome is that the two paths inside one architecture have unequal post-formation authority. It does not cleanly reproduce separate transformer-like and Mamba-like commits.

Suggested section 6.4 insertion:

> The hybrid Falcon-H1-0.5B-Base exposes attention K/V and SSM state in every one of its 36 layers. The completed E14 sweep finds attention-dominated dependence on the admitted synthetic identity/color panel. Attention-only whole-cut replacement changes 17/22 and 8/9 candidate answers; SSM-only replacement changes 2/22 and 0/9; replacing both changes 21/22 and 8/9. Whole attention writes recover 0.987/0.956 normalized answer-logprob gain, versus 0.345/0.172 for SSM and 1.000 for both. Identity attention has low singleton necessity (maximum 0.149) and a broad late profile, but the best tested six-layer window carries only 0.715 and its strongest singleton write is 0.224. Color has singleton necessity 0.295 on nine admitted items. These mixed results establish no new strict four-quadrant certificate and do not support a concentrated Mamba-like SSM writer. They instead show unequal authority of two formed-state cuts inside the same hybrid architecture.

**Correct E10 admission and timing.** The [existing E10 verification](../../../../saturn/experiments/2026-10-01-e10-cot-intermediate-steps/VERIFICATION-2026-10-01.md), rerun during this audit, finds both reports record-consistent. The primary single-intermediate items pass their recorded step-generation checks. Multi-step items have `require_on_policy=[]`; they were admitted on the final answer with a supplied scratchpad, rather than under the claimed all-step admission check. Their later-step diagnostic flags are 0/8 and 3/8, with ambiguous leading-number parsing and no retained checking rollout. State that distinction instead of saying all 48/46 admitted items generated every intermediate correctly.

The intervention happens **after the entire supplied scratchpad is prefilled**. The early value's removal does not cause the model to regenerate the later value. It leaves the already formed later K/V available. Replace the explanation that the value is re-derived after removal with post-formation consumption of the later state. Also replace the itemwise “|Δ| ≤ 0.04” bound with a mean absolute delta of approximately 0.037 nats for 0.5B; one row reaches 0.0964. The updated Reading paragraph correctly avoids declaring a step-axis time circuit. Link the verification note beside the original historical findings.

**Repair the discrimination argument in section 2.2.** A distributed linear readout can have weak singleton effects and strong whole-path effects. For example, `y = (x1 + … + x8)/8`, with a zero source and all-one target, gives singleton effects of 0.125 and joint effects of 1.0. With a class threshold at 0.5 it reproduces all four qualitative outcomes, and it also meets the manuscript's small-single-effect scalar bars. This is a counterexample to the claimed exclusion of distributed linear representations, not a model of FLUX. Describe the four quadrants as a cut-specific operational signature. The paper's dose, ordering, window and consumer measurements then carry the mechanistic interpretation.

**Reconcile remaining headlines, figures and instrument claims.** Figure 2 still says the whole path is 1.00 on both axes in every cell, while the surrounding table includes degenerate Qwen3 necessity and other non-unit effects. State which plotted cells and normalizations it describes. “Single-site tools cannot see the class by construction” is stronger than the measured limitation: the same manuscript reports whole-feature effects and shows full singleton sweeps discovering writers. Lead with what the tested operator, support and representation miss. E14 also reinforces the need to distinguish candidate-set flips, normalized logprob gain, semantic image classification and pixel reconstruction.

## Assessment of the current draft

The strongest contribution is the comparative causal anatomy: a temporal singleton/joint gap in diffusion, distributed necessity with concentrated or redundant writes in selected decoder stores, Mamba retention-associated writers, and concrete limitations of a tested feature basis. The new hybrid result strengthens that comparative story by showing different authority at two cuts inside one model. Its mixed result is useful evidence.

The manuscript needs integration and consistent claim scope more urgently than another broad run. In the latest checked copy, the stale “never write-swept” sentence is gone, the transformer K/V reading acknowledges no full certificate, the Qwen0.5 identity cell is described as a redundant pair, and the conclusion separates completed LM results from diffusion certification. Those repairs should be preserved. The remaining E14 omission, E10 setup/timing wording and false linear-exclusion assertion are concrete publication issues.
