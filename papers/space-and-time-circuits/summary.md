---
title: "Space and Time Circuits — research summary and current evidence"
date: 2026-10-01
type: research-summary
status: source-reviewed
paper: paper.md
---

# Space and Time Circuits — research summary

[Space and Time Circuits: Causal Control Across Model Trajectories](paper.md) consolidates the final-boss, IRD, distributed-store measurement, and certified FLUX route work. This summary reflects draft 3 and the recovered overnight experiment records through October 1, 2026. The [README](README.md) records current status; the [outline](outline.md) preserves the earlier plan. Historical certificates and later corrections should be read separately.

**Definition check: the paper does establish its operational time-circuit definition in FLUX.** A blanket statement that the research does not meet its own definition would be wrong. The [reviewer's clarification](critiques/clarification-2026-10-01_110945_PDT.md) explicitly concedes this. The decoder-LM formed-store results and E10 scratchpad-step results have different quadrant profiles; their limitations do not revoke the diffusion certificate. The additive [definition and rerun audit](../../../saturn/experiments/2026-09-30-space-and-time-circuits/TIME-DEFINITION-VERIFICATION-2026-10-01.md) checks the saved FLUX reports and identifies stale statements separately from corrected measurements.

## The papers it brings together

| Writeup | Contribution to the combined paper |
|---|---|
| [Integral Residual Dynamics](../integral-residual-dynamics/paper.md) | The trajectory-functional object `R = 𝓘(r(t))`, the four-quadrant certificate, C1–C8, the transport-cut comparison, and depth/time kernels. Its original 8/8 grid is historical; later exhaustive sweeps change its interpretation. |
| [Capabilities as Support-Aware Transactions: The Final Boss Is a Role, Not a Layer](../capabilities-as-transactions/paper.md) | Separates source, address, payload, formation, carriage, recipient transition, native consumer, and continuation. The final boss names the consumer role where state acquires behavioral authority. |
| [Single-Site Tests Miss Distributed Stores](../pointwise-instruments-miss-distributed-circuits/paper.md) | Primary single-site/whole-path measurements, public-tool comparisons, and the blind-graded instrument trial. Its [execution-model appendix](../pointwise-instruments-miss-distributed-circuits/appendix-execution-model.md) explains the replay method. |
| [The Circuit That Survived Its Coordinates](../../bfl/docs/certified-semantic-circuits/paper.md) | The production FLUX.2 semantic-route measurements, held-out tests, controls, and evidence bundle. |

The new manuscript is intended to supersede the separate IRD and transaction drafts for external release. The [assessment notes](../capabilities-as-transactions/assessment-notes.md) explain the consolidation. Read the [October 1 review](critiques/review-2026-10-01_094028_PDT.md) alongside its later [clarification](critiques/clarification-2026-10-01_110945_PDT.md) and [experiment-recovery audit](critiques/experiment-recovery-2026-10-01.md): the manuscript has since repaired several statements criticized in the initial snapshot.

## The question and the instrument

Localization, formation, storage, writing, and consumption can occur at different sites and times. A pointwise null therefore need not imply that the model lacks a causal mechanism.

The paper separates three claims: an operational discovery with strict path-distributed diffusion instances; architectural generalization of the broader time-formed family; and implemented applications through scene compilation and the Saturn VM. The introduction maps each claim to its evidence. Section 3 explains replay, typed execution and model virtual memory; section 10 specifies the compiler and reports the VM's native continuation, durable-state and residency results.

A **time-formed circuit** has controlling state that depends causally on ordered execution. Local seeds, commits, latches and readouts can belong to that family. Its **strict path-distributed subtype** fixes a model, behavior, accumulation axis, state cut, intervention, and unchanged native consumer, and requires all four quadrants:

| Intervention | Every individual site | Whole path |
|---|---|---|
| Necessity: remove or replace state | Behavior survives | Behavior is removed |
| Sufficiency: install target state | Little target transfer | Target behavior is installed |

The universal quantifier matters: a weak average singleton effect does not suffice if one individual site is decisive. The signature is cut- and granularity-specific. **Nonlinearity and non-additivity are not conditions of the definition:** even a linear additive route can pass. Competing mechanism explanations do not revoke an operational pass; dose, window, ordering and control panels provide separate anatomy. Architectural generalization concerns the broader time-formed family, while each specimen's strict-subtype status is reported separately.

Saturn captures native execution, forks matched alternatives, changes typed state, and executes the original downstream model to tokens or pixels. Its exact restore/replay checks protect against confusing runtime error with a causal effect. The model's output supplies the behavioral evidence. See the [Saturn architecture and use protocol](../../../saturn/docs/SATURN-BIBLE.md), [evidence-plane guide](../../../saturn/docs/EVIDENCE-PLANE.md), and [capability map](../../../obsidian/blog/2026-08-14-what-saturn-can-actually-do.md).

Replay recomputes a future from captured state; a fork owns its future writes, and rewind restores a retained cut. Model virtual memory separates logical state, physical residency and causal ancestry. Eviction/reload preserves state; a causal swap or mean ablation changes it. A compiled scene source is produced before target rendering, while live queries and native denoising still execute. These distinctions make the compiler and VM claims concrete without treating state reuse as cached answers.

## What the current evidence says

### FLUX: the cleanest time-circuit case

The [committed time-signature bundle](evidence/time-signature/README.md) contains the current single-step/all-step report, five-seed color necessity report, pinned hashes and an offline verifier. Section 5.2 now places all four criteria beside their measured bounds. The [coherence correction note](critiques/coherence-corrections-2026-10-01.md) records why the definition, E17 leak/count wording and figure labels changed.

In FLUX.2 Klein 4B, the historical `joint.2 → joint.3 → joint.4 → single.0` text route carries twenty tested semantic contrasts: six strict nine-gate certificates, eleven additional carrier-level results, and three candidates. Single-step target transplantation leaves pixel MAD 48.4 to the target; all-step transplantation reduces it to 0.47. In the five-seed color necessity panel, removing one step leaves the target, while all-step interchange reverts to the source and all-step deletion produces the null image.

Independent re-analysis of the later joint-region report confirms **15/15 tested setup/site-set combinations meet all four declared criteria**: three setups crossed with five site sets, not fifteen independent model replications. Progress was recomputed from the saved image distances. The largest singleton write is 0.562, below the 0.90 full-transfer bar; the smallest whole-path write is 0.91309. Every singleton source replacement leaves progress above 0.15, while every whole-path replacement leaves it at or below 0.01101. The five-seed color report separately confirms the necessity half, rather than five complete four-quadrant replications. See the [pinned audit JSON](../../../saturn/experiments/2026-09-30-space-and-time-circuits/time-definition-verification-2026-10-01.json).

Later alternative-path controls show that the carrier is a redundant joint-region text-conditioning pathway. The historical route is a certified representative, not a unique or minimal route. Whole-path deletion is non-specific: a norm-matched sham also nulls the image, and deleting the input conditioning is equivalent to removing the prompt. Interchange and the singleton/joint gap carry the more specific information.

Klein 9B identity also shows the four-quadrant pattern on two seeds and two route windows, although the stricter nine-gate panel is 8/9. Lighting is mixed. SDXL is mixed in the opposite direction to the language models: target writing requires a temporal path, but removing an early step can be individually decisive.

Supporting writeups: [twenty-axis panel](../../bfl/demos/certified-semantic-route.md), [distributed K/V route](../../bfl/demos/certified-semantic-route.md), [causal clock](../../bfl/demos/forking-a-generation.md), and [SDXL decoder study](../../demos/sdxl-decoder.md). The newest [off-route](../../../saturn/experiments/2026-09-30-flux2-offroute-span-sweep/FINDINGS.md), [five-seed](../../../saturn/experiments/2026-09-30-e7-flux-color-multiseed/FINDINGS.md), [9B](../../../saturn/experiments/2026-10-01-e8-klein9b-nine-gate/FINDINGS.md), and [SDXL four-quadrant](../../../saturn/experiments/2026-10-01-e9-sdxl-four-quadrant/FINDINGS.md) records remain under Saturn.

One stale reading is especially consequential: E1b/E2b treated deletion's `dp ≈ 0` as target survival. The later [E1c correction](../../../saturn/experiments/2026-09-30-flux2-residual-deletion/FINDINGS.md) shows that this is the null image, so whole-path deletion does remove the target. Preserve the older measurements, but use the corrected interpretation.

### Language models: written during a formation window, committed late

Full sweeps changed the older IRD grid. No fully swept language-model cell currently passes all four quadrants. Selected transformer cells have low single-layer necessity, but a substantial single-layer write.

For identity, the recorded best isolated K/V writes are 0.808 at Qwen2.5-1.5B L23 and 0.809 at Gemma-2-2B L22, versus whole-trace writes approximately 1.0. Their best single-layer necessity fractions are only 0.079 and 0.078. These figures were checked directly in the corresponding report JSONs during this summary's preparation.

Window cuts further distinguish the cells: Qwen2.5-0.5B identity is a redundant pair; some other cells have a short band; the necessity-clean cases require a broader late band. The cleanest identity panels have best three-layer effects of only 0.18–0.23, with six to eight layers carrying much more. That is a real necessity/write asymmetry, but it fails the definition's single-site-sufficiency quadrant.

A residual write can install the information before the commit band. Native computation then forms stored state, and the answer reads it at the commit layer. In addition, operands are writable early at their own positions while the computed sum becomes writable late at the query position. Mamba's concentrated writer preserves state through unusually high retention over the suffix.

Consequently, the final boss survives as a model-local role or band. A universal boss layer or an all-family four-quadrant certificate is not established. The sampled Mamba certificates were retracted; Qwen3-30B's in-forward certificate does not survive the isolated cache-swap protocol. Training in the inspected Pythia identity case sharpens a late writer, reversing the earlier sampled interpretation that it progressively distributes the effect.

Sources: [residual-write findings](../../../saturn/experiments/2026-09-30-full-layer-sweeps/FINDINGS-E16-residual-writes.md), [isolated-write findings](../../../saturn/experiments/2026-09-30-full-layer-sweeps/FINDINGS-E17-isolated-kv-writes.md), [window necessity](../../../saturn/experiments/2026-09-30-full-layer-sweeps/FINDINGS-E19-window-necessity.md), [computed objects](../../../saturn/experiments/2026-09-30-full-layer-sweeps/FINDINGS-E11-computed-object.md), [Mamba sweeps](../../../saturn/experiments/2026-09-30-mamba-full-layer-sweeps/FINDINGS.md), and [writer clock](../../../saturn/experiments/2026-09-30-mamba-writer-clock/FINDINGS.md).

**E20 connects the source seed to the formed store.** In the completed Qwen2.5-1.5B identity mediation panel (42 admitted rows), blocking the endogenous L22–27 subject K/V removes a median 0.924 of an L12 seed's answer-logprob effect. Installing K/V formed by the seeded recipient into an otherwise unseeded recipient recovers 0.871; a wrong-identity band authors the wrong identity on 37/42 rows. This strengthens the source → formation → store → consumer account in this cell. These are per-row logprob-effect ratios, not unique total causal mediation. It does not change the 0.81 singleton write or establish a new strict certificate. The [E20 findings and raw record](../../../saturn/experiments/2026-09-30-full-layer-sweeps/FINDINGS-E20-mediation.md) retain context effects, signed outcomes and limitations.

### Falcon hybrid: attention dominates the formed-state read

The overnight E14 full sweep completed on Falcon-H1-0.5B-Base. Every singleton was tested at its attention and SSM cuts, with identity attention windows through width six. Identity admits 22/22 items across two contexts; color admits 9/20, all from one context.

| Identity intervention | Attention K/V | SSM state | Both |
|---|---:|---:|---:|
| Whole-cut candidate changes | 17/22 | 2/22 | 21/22 |
| Median original-answer Δlogprob | −1.774 | −0.038 | −2.644 |
| Whole-cut normalized write | 0.987 | 0.345 | 1.000 |

The strongest attention singleton identity write is 0.224, with CI [0.191, 0.254], versus about 0.81 in Qwen2.5-1.5B and Gemma-2 identity. The best six-layer necessity window carries 0.715 of attention's whole-cut effect; widths above six remain unresolved. The strongest SSM singleton writes are only 0.066 for identity and 0.055 for color. Weak, sign-varying SSM removal effects make normalized necessity shares unstable.

This supports a broader attention profile and partial complementary SSM authority at the **post-subject formed-state cut**. It does not establish the predicted Mamba-like SSM writer, SSM dispensability during prefix formation, or a new strict certificate. The identity attention write crosses the 0.2 bar and color singleton necessity crosses 0.25. Falcon formation, commit, read and clock roles were not measured. These results narrow the late-writer generalization without changing the FLUX certificate.

The [bundled report and verifier](evidence/hybrid-attn-ssm/README.md) check report/log equality, source hashes and complete layer/window coverage without executing a model. The aggregate-only report cannot support independent re-bootstrap. See the [canonical findings](../../../saturn/experiments/2026-10-01-e14-hybrid-attn-ssm/FINDINGS.md) for signed effects and execution history.

## Larger experiments incorporated in the story

| Experiment | Connection and boundary |
|---|---|
| [Scene-source compilation](../../demos/scene-generator.md) and its [full paper](../../demos/docs/scene-generator-paper.md) | Complete prompt-derived source installation reproduces 21/21 native images across seven specimens and five diffusion families. Exact native replay establishes execution equivalence; it does not establish independent semantic editing or prompt fidelity. |
| [Durable causal-context VM](../../../saturn/experiments/2026-09-29-causal-context-vm-integration/FINDINGS.md) and [Mamba state VM](../../../saturn/experiments/2026-09-30-mvm-mamba-cot/FINDINGS.md) | Shared exact-history context, private computed continuation, bounded residency, abort/restore and fresh-process resumption; independently implemented recurrent-state sweeps agree with the paper's measurements. These are bounded execution results, with numerical contracts reported per backend. |
| [Scene editing](../../demos/scene-editing.md) and [real hotpatch futures](../../bfl/demos/forking-a-generation.md) | Timing changes which properties a write can control. Register and program state can jointly reproduce an endpoint that neither alone reproduces. |
| [Character registers](../../demos/jen-character-register.md), [sprite registers](../../demos/jen-sprite-register.md), and [trait diagnostics](../../demos/anime-sprite-register.md) | Saved native reference operands can be replayed and reused. Fine identity, spatial ownership, and actor binding retain visible failures. |
| [Relations and transport](../../demos/flux-relations-and-transport.md) | Object movement depends on spatial support and early timing; donor-assisted contextual results must be separated from donor-free binding. |
| [Recipient-native counting patch](../../bfl/demos/small-targeted-repairs.md) | A small early patch improves exact count on held-out cases, but its collateral gate fails. |
| [Blind instrument trial](../pointwise-instruments-miss-distributed-circuits/evidence/instrument-trial/README.md) and [circuit-tracer comparison](../../../saturn/experiments/2026-09-30-circuit-tracer-head-to-head/FINDINGS.md) | Quantify particular readout and representation failures, rather than establish universal blindness of circuit methods. |

The manuscript is a consolidation of this circuit/formation thread, rather than a complete portfolio survey. [SourceWrite](../../demos/sourcewrite-consumer-feedback.md), [Qwen causal programs](../../demos/qwen-causal-programs.md), [Black Mamba memory and writer repair](../../demos/black-mamba-memory-and-writer-repair.md), and [reversible structural growth](../../demos/reversible-structural-growth.md) remain fuller standalone reports in the [Saturn highlights collection](../../demos/saturn-highlights.md).

## CoT: what was tested and what changed

The original IRD C7 scratchpad swaps changed answers across four model families, but the manipulated scratchpad already stated the answer. That establishes causal copying. A later [model-virtual-memory pilot](../../../saturn/experiments/2026-09-30-mvm-mamba-cot/FINDINGS.md) motivated a design in which the answer requires a further operation on an intermediate that is never restated.

[E10](../../../saturn/experiments/2026-10-01-e10-cot-intermediate-steps/READOUT-QUALIFICATION-2026-10-01.md) holds visible base text fixed, mean-ablates or counterfactually replaces a step's K/V rows, and observes a 14-token greedy number-parser readout. It compares those state interventions with text mistake insertion and truncation, and restores original pages as a control.

| Recorded result | Qwen2.5-0.5B | Qwen2.5-1.5B |
|---|---:|---:|
| Non-copied single-intermediate items | 32 | 30 |
| Intermediate unmount changes bounded parser readout | 32/32 | 30/30 |
| Intermediate swap produces the correct counterfactual answer | 15/32 | 30/30 |
| Two-step chain: early value unmount changes answer | 0/8 | 0/8 |
| Two-step chain: later value unmount changes answer | 8/8 | 8/8 |
| Two-step chain: later value swap produces counterfactual answer | 8/8 | 8/8 |
| Two-step chain: whole-scratchpad unmount changes answer | 8/8 | 8/8 |
| Maximum recorded remount sequence-logprob delta | 0.0 | 0.0 |

The single-intermediate result supports causal use of non-restated arithmetic state on admitted, scaffolded synthetic items. In 8/32 and 24/30 removal strings, the parser reads an operand from an unfinished compound RHS such as `= 42 - 5`, so the historical rates do not demonstrate wrong completed final answers on every item. The probability metric includes the baseline worked expression through its selected number. Directed counterfactual authorship survives this qualification. The result does not establish an automated monitor of freely generated long reasoning or hidden motives.

The [subsequent completed-answer mrun reproduction](../../../saturn/experiments/2026-10-01-e10-completed-answer-rerun/FINDINGS.md) collects all 48 original rows per checkpoint while retaining the 32/30 historical primary intervention denominator. Removal ends wrong on 26/32 and 3/30, repairs correctly on 6/32 and 25/30, and leaves two Qwen1.5 rows unresolved at the budget. Completed donor answers occur on 19/32 and 30/30. All eight later-step multiplications complete correctly on both models despite leading-number flag patterns of 0/8 and 3/8. The stored intermediate is causally active; it is not universally necessary for the model to reach a correct longer answer. Generated early-swap branches author donor answers on 8/8, while removal diagnostics retain a first-result stopping-stage confound. Historical outcomes, numerical regimes, and admission remain unchanged.

**The chain does not meet the strict path-distributed subtype at scratchpad-step grain.** Its later step is individually necessary and its counterfactual state is individually sufficient to direct the answer. Pooling the inert early step with the decisive later step gives 50% average single-step flips, but the strict definition concerns every singleton. Whole-path removal does not exceed the strongest singleton on the binary answer-change endpoint.

The code prefills the entire scratchpad before intervening. It therefore tests the final answer's use of already formed state; it does not test whether the early step was required to generate the later one. Calling the early value "re-derived" after intervention is not directly supported, because the later state was already present.

The audit also finds a prose/design discrepancy: multi-step items have `require_on_policy=[]`, so step-generation checks do not control admission. The saved later-step on-policy flags are 0/8 and 3/8; those flags use a leading-number parser and the checking rollouts were not saved, so they cannot alone distinguish arithmetic failure from formatting. All primary single-intermediate items pass their recorded step check. See the additive [E10 verification note](../../../saturn/experiments/2026-10-01-e10-cot-intermediate-steps/VERIFICATION-2026-10-01.md), [audit JSON](../../../saturn/experiments/2026-10-01-e10-cot-intermediate-steps/verification-2026-10-01.json), and [recomputable verifier](../../../saturn/experiments/2026-10-01-e10-cot-intermediate-steps/verify_record.py).

## Connections to Anthropic's questions

Anthropic's [Biology open questions](https://transformer-circuits.pub/2025/attribution-graphs/biology.html#open-questions) ask about CoT faithfulness, internal versus external reasoning, cross-model recurrence, scale, training, and hidden goals. Their [methods paper](https://transformer-circuits.pub/2025/attribution-graphs/methods.html) discusses missing attention explanations and unexplained reconstruction state. The following is a mapping of the local results to those questions, not a claim that the whole question has been solved.

| Question | Local contribution | Remaining boundary |
|---|---|---|
| Does a written intermediate cause the answer? | E10's exact formed-cache intervention produces directed arithmetic effects with base text fixed. | Selected synthetic successes, supplied scaffolds, two small Qwen checkpoints; no automated faithfulness classifier. |
| Where does information become output-controlling? | Formation, commit, stored-state necessity, and read sweeps separate distinct causal roles. | The recorded cuts do not reconstruct all intermediate computation. |
| Does a sparse replacement basis expose every causal dependence? | E6's identity interventions barely move the answer while native-state cuts have large effects. | One transcoder basis, with reconstruction-error terms held clean; color is partly visible. |
| Why does attention select a source row? | [Exact joins and spectral buckets](../../../saturn/experiments/2026-09-30-e18-bucket-join-time-reads/FINDINGS.md) can substitute selected reads and identify repetition rows. | Query-derived addressing fails on the semantic identity/coreference panels. |
| How do mechanisms recur across models and training? | Full sweeps distinguish late bands, redundant pairs, and concentrated writers; Pythia training sharpens a writer. | Bounded model/behavior panels; no universal scale law. |

Anthropic's [QK follow-up](https://www.transformer-circuits.pub/2025/attention-qk/index.html) already explains attention patterns through feature interactions. The original attribution graphs represent cross-position information flow; their initial omission was why attention selected those positions. The local paper should retain that distinction.

Arithmetic CoT has direct [causal predecessors](https://arxiv.org/abs/2412.01113). E10's distinctive contribution is the typed, reversible formed-K/V cut with visible text fixed. Motivated-reasoning detection, hidden-goal discovery, general hallucination prediction, and prospective CoT monitoring are not established by these results. The program's earlier hallucination predictor was struck.

## Where the linked writeups live

- **Already present and Git-tracked under `research/`:** all four constituent papers and the core BFL reports.
- **Present under `research/`, but currently untracked:** the entire `research/demos/` collection, including scene compilation/editing, character registers, SourceWrite, Qwen causal programs, Black Mamba, and structural growth. "In the directory" and "committed into the research repository" are different statuses here.
- **Not copied into `research/`:** the standalone E10, E6, E18, E16/E17/E19, Mamba sweep/clock, and newest diffusion experiment findings. Their current canonical records are under `saturn/experiments/`; this summary links to them explicitly. The paper contains summaries, and older AR bundles exist in [research evidence](evidence/ar-certificates/README.md), but that does not make the newer records part of the research bundle.
- **Also outside `research/`:** the Saturn Bible/evidence documentation and the dated Obsidian capability map and retrospective, [From the Final Boss to Executable Models](../../../obsidian/blog/2026-09-08-211251-from-the-final-boss-to-executable-models.md).

The [consolidated experiment directory](../../../saturn/experiments/2026-09-30-space-and-time-circuits/SUMMARY.md) links back to this summary. Verification re-analyzed existing reports and code without running models or rewriting historical results. The initial review left the manuscript untouched; the subsequent authorized draft-3 revision incorporates E14, corrects E10's setup/timing account, and narrows the headline and late-writer claims after preserving the as-is paper directory at `369ab87`.
