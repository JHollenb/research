---
title: "Space and Time Circuits — research summary and current evidence"
date: 2026-10-01
type: research-summary
status: source-reviewed
paper: paper.md
---

# Space and Time Circuits — research summary

[A New Class of Circuits: Space and Time](paper.md) consolidates the final-boss, IRD, distributed-store measurement, and certified FLUX route work. This summary reflects the working manuscript and experiment records through October 1, 2026. The manuscript contains newer results than its [README](README.md) and preserved [outline](outline.md). Historical certificates and later corrections should be read separately.

## The papers it brings together

| Writeup | Contribution to the combined paper |
|---|---|
| [Integral Residual Dynamics](../integral-residual-dynamics/paper.md) | The trajectory-functional object `R = 𝓘(r(t))`, the four-quadrant certificate, C1–C8, the transport-cut comparison, and depth/time kernels. Its original 8/8 grid is historical; later exhaustive sweeps change its interpretation. |
| [Capabilities as Support-Aware Transactions: The Final Boss Is a Role, Not a Layer](../capabilities-as-transactions/paper.md) | Separates source, address, payload, formation, carriage, recipient transition, native consumer, and continuation. The final boss names the consumer role where state acquires behavioral authority. |
| [Single-Site Tests Miss Distributed Stores](../pointwise-instruments-miss-distributed-circuits/paper.md) | Primary single-site/whole-path measurements, public-tool comparisons, and the blind-graded instrument trial. Its [execution-model appendix](../pointwise-instruments-miss-distributed-circuits/appendix-execution-model.md) explains the replay method. |
| [The Circuit That Survived Its Coordinates](../../bfl/docs/certified-semantic-circuits/paper.md) | The production FLUX.2 semantic-route measurements, held-out tests, controls, and evidence bundle. |

The new manuscript is intended to supersede the separate IRD and transaction drafts for external release. The [assessment notes](../capabilities-as-transactions/assessment-notes.md) explain the consolidation, while the [October 1 review](critiques/review-2026-10-01_094028_PDT.md) identifies remaining interpretation and prior-art issues.

## The question and the instrument

Localization, formation, storage, writing, and consumption can occur at different sites and times. A pointwise null therefore need not imply that the model lacks a causal mechanism.

The paper's operational time-circuit definition fixes a model, behavior, accumulation axis, state cut, intervention, and unchanged native consumer. It requires all four quadrants:

| Intervention | Every individual site | Whole path |
|---|---|---|
| Necessity: remove or replace state | Behavior survives | Behavior is removed |
| Sufficiency: install target state | Little target transfer | Target behavior is installed |

The universal quantifier matters: a weak average singleton effect does not suffice if one individual site is decisive. The signature is cut- and granularity-specific. It also does not, by itself, uniquely exclude redundancy, additive accumulation followed by a nonlinear consumer, or other competing explanations; dose, window, ordering, and control panels provide additional anatomy.

Saturn captures native execution, forks matched alternatives, changes typed state, and executes the original downstream model to tokens or pixels. Its exact restore/replay checks protect against confusing runtime error with a causal effect. The model's output supplies the behavioral evidence. See the [Saturn architecture and use protocol](../../../saturn/docs/SATURN-BIBLE.md), [evidence-plane guide](../../../saturn/docs/EVIDENCE-PLANE.md), and [capability map](../../../obsidian/blog/2026-08-14-what-saturn-can-actually-do.md).

## What the current evidence says

### FLUX: the cleanest time-circuit case

In FLUX.2 Klein 4B, the historical `joint.2 → joint.3 → joint.4 → single.0` text route carries twenty tested semantic contrasts: six strict nine-gate certificates, eleven additional carrier-level results, and three candidates. Single-step target transplantation leaves pixel MAD 48.4 to the target; all-step transplantation reduces it to 0.47. In the five-seed color necessity panel, removing one step leaves the target, while all-step interchange reverts to the source and all-step deletion produces the null image.

Later alternative-path controls show that the carrier is a redundant joint-region text-conditioning pathway. The historical route is a certified representative, not a unique or minimal route. Whole-path deletion is non-specific: a norm-matched sham also nulls the image, and deleting the input conditioning is equivalent to removing the prompt. Interchange and the singleton/joint gap carry the more specific information.

Klein 9B identity also shows the four-quadrant pattern on two seeds and two route windows, although the stricter nine-gate panel is 8/9. Lighting is mixed. SDXL is mixed in the opposite direction to the language models: target writing requires a temporal path, but removing an early step can be individually decisive.

Supporting writeups: [twenty-axis panel](../../bfl/demos/twenty-axis-semantic-route-circuit.md), [distributed K/V route](../../bfl/demos/distributed-kv-causal-route.md), [causal clock](../../bfl/demos/diffusion-time-causal-clock.md), and [SDXL decoder study](../../demos/sdxl-decoder.md). The newest [off-route](../../../saturn/experiments/2026-09-30-flux2-offroute-span-sweep/FINDINGS.md), [five-seed](../../../saturn/experiments/2026-09-30-e7-flux-color-multiseed/FINDINGS.md), [9B](../../../saturn/experiments/2026-10-01-e8-klein9b-nine-gate/FINDINGS.md), and [SDXL four-quadrant](../../../saturn/experiments/2026-10-01-e9-sdxl-four-quadrant/FINDINGS.md) records remain under Saturn.

### Language models: written during a formation window, committed late

Full sweeps changed the older IRD grid. No fully swept language-model cell currently passes all four quadrants. Selected transformer cells have low single-layer necessity, but a substantial single-layer write.

For identity, the recorded best isolated K/V writes are 0.808 at Qwen2.5-1.5B L23 and 0.809 at Gemma-2-2B L22, versus whole-trace writes approximately 1.0. Their best single-layer necessity fractions are only 0.079 and 0.078. These figures were checked directly in the corresponding report JSONs during this summary's preparation.

Window cuts further distinguish the cells: Qwen2.5-0.5B identity is a redundant pair; some other cells have a short band; the necessity-clean cases require a broader late band. The cleanest identity panels have best three-layer effects of only 0.18–0.23, with six to eight layers carrying much more. That is a real necessity/write asymmetry, but it fails the definition's single-site-sufficiency quadrant.

A residual write can install the information before the commit band. Native computation then forms stored state, and the answer reads it at the commit layer. In addition, operands are writable early at their own positions while the computed sum becomes writable late at the query position. Mamba's concentrated writer preserves state through unusually high retention over the suffix.

Consequently, the final boss survives as a model-local role or band. A universal boss layer or an all-family four-quadrant certificate is not established. The sampled Mamba certificates were retracted; Qwen3-30B's in-forward certificate does not survive the isolated cache-swap protocol. Training in the inspected Pythia identity case sharpens a late writer, reversing the earlier sampled interpretation that it progressively distributes the effect.

Sources: [residual-write findings](../../../saturn/experiments/2026-09-30-full-layer-sweeps/FINDINGS-E16-residual-writes.md), [isolated-write findings](../../../saturn/experiments/2026-09-30-full-layer-sweeps/FINDINGS-E17-isolated-kv-writes.md), [window necessity](../../../saturn/experiments/2026-09-30-full-layer-sweeps/FINDINGS-E19-window-necessity.md), [computed objects](../../../saturn/experiments/2026-09-30-full-layer-sweeps/FINDINGS-E11-computed-object.md), [Mamba sweeps](../../../saturn/experiments/2026-09-30-mamba-full-layer-sweeps/FINDINGS.md), and [writer clock](../../../saturn/experiments/2026-09-30-mamba-writer-clock/FINDINGS.md).

## Larger experiments incorporated in the story

| Experiment | Connection and boundary |
|---|---|
| [Scene-source compilation](../../demos/scene-generator.md) and its [full paper](../../demos/docs/scene-generator-paper.md) | Complete prompt-derived source installation reproduces 21/21 native images across seven specimens and five diffusion families. Exact native replay establishes execution equivalence; it does not establish independent semantic editing or prompt fidelity. |
| [Scene editing](../../demos/scene-editing.md) and [real hotpatch futures](../../bfl/demos/real-hotpatch-cinema.md) | Timing changes which properties a write can control. Register and program state can jointly reproduce an endpoint that neither alone reproduces. |
| [Character registers](../../demos/jen-character-register.md), [sprite registers](../../demos/jen-sprite-register.md), and [trait diagnostics](../../demos/anime-sprite-register.md) | Saved native reference operands can be replayed and reused. Fine identity, spatial ownership, and actor binding retain visible failures. |
| [Relations and transport](../../demos/flux-relations-and-transport.md) | Object movement depends on spatial support and early timing; donor-assisted contextual results must be separated from donor-free binding. |
| [Recipient-native counting patch](../../bfl/demos/recipient-native-capability-patch.md) | A small early patch improves exact count on held-out cases, but its collateral gate fails. |
| [Blind instrument trial](../pointwise-instruments-miss-distributed-circuits/evidence/instrument-trial/README.md) and [circuit-tracer comparison](../../../saturn/experiments/2026-09-30-circuit-tracer-head-to-head/FINDINGS.md) | Quantify particular readout and representation failures, rather than establish universal blindness of circuit methods. |

The manuscript is a consolidation of this circuit/formation thread, rather than a complete portfolio survey. [SourceWrite](../../demos/sourcewrite-consumer-feedback.md), [Qwen causal programs](../../demos/qwen-causal-programs.md), [Black Mamba memory and writer repair](../../demos/black-mamba-memory-and-writer-repair.md), and [reversible structural growth](../../demos/reversible-structural-growth.md) remain fuller standalone reports in the [Saturn highlights collection](../../demos/saturn-highlights.md).

## CoT: what was tested and what changed

The original IRD C7 scratchpad swaps changed answers across four model families, but the manipulated scratchpad already stated the answer. That establishes causal copying. A later [model-virtual-memory pilot](../../../saturn/experiments/2026-09-30-mvm-mamba-cot/FINDINGS.md) motivated a design in which the answer requires a further operation on an intermediate that is never restated.

[E10](../../../saturn/experiments/2026-10-01-e10-cot-intermediate-steps/FINDINGS.md) holds visible base text fixed, mean-ablates or counterfactually replaces a step's K/V rows, and observes the model's greedy final answer. It compares those state interventions with text mistake insertion and truncation, and restores original pages as a control.

| Recorded result | Qwen2.5-0.5B | Qwen2.5-1.5B |
|---|---:|---:|
| Non-copied single-intermediate items | 32 | 30 |
| Intermediate unmount changes answer | 32/32 | 30/30 |
| Intermediate swap produces the correct counterfactual answer | 15/32 | 30/30 |
| Two-step chain: early value unmount changes answer | 0/8 | 0/8 |
| Two-step chain: later value unmount changes answer | 8/8 | 8/8 |
| Two-step chain: later value swap produces counterfactual answer | 8/8 | 8/8 |
| Two-step chain: whole-scratchpad unmount changes answer | 8/8 | 8/8 |
| Maximum recorded remount sequence-logprob delta | 0.0 | 0.0 |

The single-intermediate result supports causal use of non-restated arithmetic state on admitted, scaffolded synthetic items. It does not establish an automated monitor of free-generated long reasoning or hidden motives.

**The chain is not a time circuit under the current definition at scratchpad-step grain.** Its later step is individually necessary and its counterfactual state is individually sufficient to direct the answer. Pooling the inert early step with the decisive later step gives 50% average single-step flips, but the definition concerns every singleton. Whole-path removal does not exceed the strongest singleton on the binary answer-change endpoint.

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

The [consolidated experiment directory](../../../saturn/experiments/2026-09-30-space-and-time-circuits/SUMMARY.md) links back to this summary. Verification here re-analyzed existing reports and code; no models were rerun, no historical results were rewritten, and the main manuscript was left untouched.
