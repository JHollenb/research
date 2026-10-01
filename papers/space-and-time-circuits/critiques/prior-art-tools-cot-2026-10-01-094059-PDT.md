# Prior-art, tool-comparison, and chain-of-thought audit

**Timestamp:** 2026-10-01 09:40:59 PDT  
**Scope:** `paper.md` §§2, 6.7, 9, 13; local E6 and E10 findings and workers; primary literature on ACDC, activation patching, Anthropic circuit tracing and QK tracing, mechanistic CoT work, and frontier-lab CoT monitoring.  
**Review standard:** distinguish (a) a measured result, (b) what the instrument can express, (c) a cross-paper synthesis, and (d) an exclusive novelty claim.

## Bottom-line assessment

The paper contains a potentially original and attention-worthy **cross-architecture synthesis**: applying one whole-path/single-site certificate at typed state cuts across diffusion denoising, transformer depth/KV state, and recurrent state. I did not find a predecessor that publishes this full diffusion–transformer–state-space comparison under one exact-replay protocol.

That does **not** make the component claims unprecedented. The present draft materially understates prior work on multi-site patching, distributed circuit discovery, attention-mediated cross-position flow, and causal CoT analysis. Its strongest tool claim is also narrower than the prose says: E6 shows that one Gemma transcoder basis, with its reconstruction-error state held clean, fails to causally control a KV-carried identity store. It does not establish that circuit tracing is intrinsically single-site or that attribution graphs cannot represent cross-position flow. E10 cleanly establishes causal use of a non-restated arithmetic step in two small Qwen2.5 models, but its multi-step result does not meet the paper's own time-circuit definition because the consumed step alone is fully necessary.

The paper should keep the cross-architecture certificate as its primary novelty, present E6 as a bounded instrument/basis failure, and present E10 as an exact-cache causal assay rather than as the first proof that CoT steps are causally used or as a demonstrated general CoT-tracking system.

## Major finding 1: E10's chain result is not a time circuit under §2's definition

The definition requires **no single site to be necessary or sufficient**, while the whole path is both necessary and sufficient (`paper.md:148-166`). E10 instead reports:

- a non-copied single intermediate whose K/V rows are individually necessary in 100% of items and whose counterfactual state authors the corresponding answer in 47%/100% (`paper.md:818-825`; `FINDINGS.md:46-55`);
- in the two-step chain, the early step is inert, but the consumed second step alone flips 8/8 (`paper.md:826`; `FINDINGS.md:57-62`).

The second result is a localized carrier at the consumed step plus an earlier value that has been re-derived or overwritten. Whole-path ablation adds no demonstrated necessity beyond that individually necessary step. The sentence “a chain spreads necessity along the scratchpad path” (`paper.md:828`) is therefore not justified by the reported intervention table. It weakens the paper because it conflicts with its crisp certificate.

**Required correction:** state that E10 discovers a **single-site CoT carrier** at the consumed step and redundancy/rewriting of the earlier step. Remove the time-circuit classification unless a longer chain is shown in which every individual step is dispensable, the complete path is necessary and sufficient, and controls distinguish accumulation from simple downstream copying/re-derivation.

The current experiment remains useful. Exact remount, the Prefill-vs-Mount control, directed counterfactual authorship, and the inert-early/necessary-late contrast are unusually clean. They support “the model causally uses this written intermediate state” on the admitted synthetic panel. They do not support a general claim about tracking hidden reasoning or a universal temporal circuit.

## Major finding 2: §13 omits direct, stronger CoT predecessors

The related-work paragraph cites only Lanham and says the paper “adds page-level swaps” (`paper.md:1178`). That is inadequate as of this draft date.

### Direct causal predecessors

1. **Kudo et al., _LLMs Faithfully and Iteratively Compute Answers During CoT_** (Findings of EACL 2026; arXiv v4 March 2026) asks when subanswers are computed and how strongly CoT state causally affects the final answer. It uses counterfactual activation patching, patches coarse grids spanning an equation and four layers at once, evaluates 2,000 instances, and reports that later CoT steps causally control the answer with a recency structure across Qwen2.5 7B/14B/32B, Qwen2.5-Math, Yi, Llama 3, and Mistral-Nemo. See the [paper](https://arxiv.org/html/2412.01113), especially its causal setup and results at lines 215–230 in the HTML version.

   This work already answers the broad question “are non-copied arithmetic CoT intermediates causally used?” on a much larger and more diverse panel. E10's novelty is the **typed K/V page cut, unmount/remount exactness, and composable counterfactual cache graft**, not the conclusion that arithmetic CoT is causally used.

2. **Dura, Öztürk, and Tekir, _Mechanistic Interpretability of Chain-of-Thought Reasoning via Sequential Activation Patching_** (August 2026) explicitly argues that a single static token intervention is insufficient for effects distributed across a generated reasoning trajectory, then introduces sequential and sequential multi-head patching with random/cross-question controls. See the [paper](https://arxiv.org/abs/2608.22332). This is direct overlap with the draft's “pointwise tools miss path effects” motivation and must be discussed.

3. **Dutta et al., _How to Think Step-by-Step_** (TMLR 2024) identifies multiple parallel CoT pathways and functionally different heads across decision, copying, and induction stages in Llama-2 7B. See the [paper](https://arxiv.org/abs/2402.18312).

4. **Yeo, Satapathy, and Cambria, _Towards Faithful Natural Language Explanations_** (EMNLP 2025) uses activation patching as causal mediation to assess explanation faithfulness across 2B–27B models. See the [paper](https://arxiv.org/abs/2410.14155).

5. **Mehrafarin, Parekh, and Konstas, _When Chain-of-Thought Fails, the Solution Hides in the Hidden States_** (April 2026) patches individual CoT-token hidden states into direct-answer runs on GSM8K and measures answer recovery across models. See the [paper](https://arxiv.org/abs/2604.23351).

6. **Anthropic's _On the Biology of a Large Language Model_** already has a dedicated mechanistic CoT-faithfulness study on Claude 3.5 Haiku. It distinguishes faithful computation, confabulation, and backwards reasoning, then validates feature-cluster hypotheses by inhibition. See [Biology, CoT section](https://www.transformer-circuits.pub/2025/attribution-graphs/biology.html#chain-of-thought-faithfulness). The draft cites Biology elsewhere but omits this overlap from §13.

Lanham remains relevant as a behavioral baseline, but it is no longer the closest comparison. Add at least Kudo, Dura, Dutta, Yeo, and Biology; preferably include Mehrafarin as well.

### Suggested novelty language for E10

> Prior work has causally patched CoT hidden states, multi-token/layer grids, features, and sequential head sets. We add an exact-remount assay at the formed K/V-page cut: text remains unchanged while a step's cache rows are unmounted or replaced by a counterfactual item's rows, and the unchanged suffix consumer determines the answer. On two small Qwen2.5-Instruct models and admitted synthetic arithmetic items, this confirms causal use of a non-restated intermediate and localizes a later consumed step; it does not yet establish general CoT tracking or a scratchpad-axis time circuit.

## Major finding 3: E6 is an important bounded failure, not a fair whole-state head-to-head

E6 is competently executed and unusually transparent. It pins the model, transcoder revision, circuit-tracer commit, target logit, attention settings, panel, no-op, and all active feature interventions. The finding that all active-feature interchange barely moves identity while full isolated KV interchange does is real.

The interpretation needs three corrections.

### 3.1 “Matched operator” is not matched state

Saturn swaps the full isolated K/V state. Circuit-tracer swaps feature coefficients while keeping reconstruction-error terms at their **clean** values (`E6 FINDINGS.md:99-106`). Those error terms account for roughly 30% of end-to-end path influence, and the identity is inferred to reside there (`E6 FINDINGS.md:145-151`). Thus the two interventions differ in both cut and state coverage.

Calling the feature interchange “matched” overstates comparability. It is **operator-analogous within the learned feature basis**, not a matched whole-state intervention. The result establishes:

> The tested Gemma Scope transcoder basis plus circuit-tracer's supported feature intervention does not expose causal control of this identity store when reconstruction errors remain fixed.

It does not establish:

> Attribution-graph methods intrinsically cannot find distributed stores.

Anthropic explicitly defines error nodes as unexplained MLP-output residual, calls them “dark matter,” and warns that they can completely obscure mechanisms. It also says its circuit descriptions are partial. See [Circuit Tracing, error nodes and dark matter](https://www.transformer-circuits.pub/2025/attribution-graphs/methods.html#reconstruction-errors-and-dark-matter).

### 3.2 “All ~18,000 features” means all features active in either of two runs

The E6 worker builds interventions only for feature indices active in the clean or filler activation tensors at each selected cell. The draft's precise §9 wording says “every active transcoder feature” (`paper.md:1071`), but both abstracts shorten this to “all ~18,000 features” (`paper.md:70`, `paper.md:94`). Retain **active** in every occurrence. Otherwise readers may understand a sweep over the full 256k-feature dictionaries, including counterfactually inactive features, which was not done.

Circuit Tracing itself warns that inactive, counterfactually active features can be causally important and describes contrastive-pair analysis as a way to surface them. See [Circuit Tracing, inactive features](https://www.transformer-circuits.pub/2025/attribution-graphs/methods.html#the-role-of-inactive-features--inhibitory-circuits).

### 3.3 L0 attribution and KV commit location answer different questions

The graph's largest subject-position attribution at L0 identifies the ancestry/origin of answer-logit influence in a feature graph. Saturn's L16–L22 ledger identifies where an already propagating subject state is committed into isolated K/V. The discrepancy is interesting, but “the graph places the store at L0” confuses provenance with storage timing. The graph did not claim L0 was a memory-write location. Rephrase as:

> The graph attributes most subject-position feature influence to an early source and leaves substantial influence in error nodes; it does not expose the late K/V commit band under this feature basis.

### 3.4 Color and the earlier SAE result prevent a universal “tools cannot see it” claim

The circuit-tracer all-active-feature interchange moves color 0.31–0.42 of the way, and the separate public-SAE experiment removes 63% of identity effect and 90% of color effect when features are ranked across all layers (`paper.md:1039-1045`). These are not full recovery, but they are substantial detection. The announcement abstract's unqualified statement that “No intervention it supports moves the answer more than 0.08” (`paper.md:94`) is false for color; the 0.08 maximum applies to identity. Abstract A is more careful (`paper.md:68-70`).

Replace universal language with behavior-specific results and acknowledge that multi-layer SAE aggregation sees much of the effect even though it does not recover the full KV-store intervention.

## Major finding 4: attribution graphs do model cross-position flow; they originally omitted why attention routed it

The sentence “Attribution graphs freeze attention and do not explain cross-position flow” (`paper.md:1053`) is inaccurate. Anthropic's methods paper says the opposite: it accounts for information flowing between token positions through frozen attention (OV paths), but not **why** attention moved it (the QK circuit). See [Circuit Tracing methods](https://www.transformer-circuits.pub/2025/attribution-graphs/methods.html), especially the description of edges through frozen attention and the statement that the graph captures OV but ignores QK.

Kamath et al. then add head loadings and bilinear query/key feature attributions, explicitly integrating attention-mediated cross-position edges into attribution graphs. They apply this to induction, multiple choice, antonyms, and other mechanisms, and list entity binding and state tracking as target applications. See [Tracing Attention Computation Through Feature Interactions](https://www.transformer-circuits.pub/2025/attention-qk/index.html).

The paper correctly states this nuance at `paper.md:128-134`; §9 should use the same wording. QK tracing does not by itself test whole-path KV necessity or accumulation, so the paper retains a meaningful distinction. It should not claim the prior graph lacks cross-position flow.

## Major finding 5: standard circuit tools are not intrinsically single-site

The framing at `paper.md:46-53`, `paper.md:100-102`, `paper.md:1152`, and `paper.md:1182-1184` treats activation patching, ACDC, and attribution graphs as built only to find individually decisive sites. The primary sources do not support that categorical claim.

- **ACDC** iteratively corrupts/removes edges from a computational graph and returns a multi-edge subgraph. It recovered 68 of roughly 32,000 edges in Greater-Than and represents IOI with a 1,041-edge graph. It is sensitive to corruption distribution and thresholds, but is not intrinsically a single-site method. See [Conmy et al. 2023](https://arxiv.org/abs/2304.14997).
- **Activation-patching best practices** explicitly evaluate sliding windows of 3, 5, and 10 layers and compare joint window patches with sums of single-layer effects. See [Zhang & Nanda 2024](https://arxiv.org/html/2309.16042), especially §5 and Appendix G. The paper's window sweeps are a rigorous use of the same intervention family, not a capability unavailable to it.
- **Circuit Tracing** supports multiple-feature/supernode interventions and cumulative layer-range constrained patching. It is feature-basis-limited and reconstruction-limited, but not restricted to one feature or one layer. See [intervention methods](https://www.transformer-circuits.pub/2025/attribution-graphs/methods.html#validating-attribution-graph-hypotheses-with-interventions).

A defensible claim is:

> Common pointwise localization workflows, and one tested sparse replacement basis, can understate a path-distributed mechanism unless the analyst explicitly sweeps joint windows or whole paths.

The current “miss them by construction” conclusion is too strong. The paper's own full-layer/window sweeps use standard intervention concepts successfully.

## Major finding 6: the four-quadrant cross does not uniquely identify a new mechanistic class

The assertion that a “diffuse but linear representation fails the whole-path quadrants” (`paper.md:166`) needs proof or removal. A distributed additive representation followed by a threshold or saturating consumer can have negligible single-site effects, a large joint-ablation effect, and a large joint-write effect. Redundancy, synergy, thresholding, and measurement resolution can all produce the same qualitative cross without a distinct path-constituted object.

The certificate is valuable as an **operational phenotype at a declared cut**. It is not by itself a unique mechanistic discriminator. The paper needs either:

- a theorem with explicit assumptions under which the four quadrants exclude the competing classes; or
- language that calls it an operational signature and uses dose/window/ordering interventions to distinguish accumulation from additive distribution, redundancy, and consumer nonlinearity.

This matters for the prior-art position: distributed multi-component effects are old; the likely novelty is the particular typed-cut certificate, exact replay, window curves, and cross-architecture recurrence of the phenotype.

## Cross-architecture novelty: what appears present and absent in prior work

### Published overlapping pieces

- multi-edge and multi-component circuit discovery (ACDC and manual circuit work);
- sliding-window and multi-layer activation patching;
- cross-position information flow and QK/OV attention analysis;
- distributed effects over generated CoT positions and head sets;
- causal activation patching of intermediate arithmetic reasoning state across many transformer families;
- mechanistic CoT-faithfulness analysis at Anthropic;
- behavioral CoT faithfulness and monitorability evaluations at Anthropic and OpenAI.

### Apparently absent as one published result

- one named certificate applied at typed cuts to diffusion denoising steps, transformer K/V-by-depth state, and recurrent state;
- exact replay/uninstall as an explicit gate across those architectures;
- the same paper contrasting single-site, contiguous-window, and whole-path interventions with a late-commit ledger;
- a head-to-head showing a whole-state KV intervention vastly exceeds interventions available through a particular transcoder feature basis on the same Gemma panel.

The absence of the combined cross-architecture result supports a synthesis novelty claim. It does not erase the prior art in each component, and it does not show that prior authors would necessarily have published this synthesis if it were available to them. They asked different questions, used different cuts, and often did not have access to diffusion or recurrent state.

## Frontier-lab CoT-monitoring relevance

The topic is directly relevant to current lab priorities:

- OpenAI argues that CoT monitoring can detect reward hacking but is fragile under direct optimization ([Baker et al., 2025](https://openai.com/index/chain-of-thought-monitoring/)).
- OpenAI's later monitorability work defines intervention, process, and outcome-property evaluations across reasoning models ([Evaluating chain-of-thought monitorability](https://openai.com/index/evaluating-chain-of-thought-monitorability/)).
- Anthropic/OpenAI researchers find that reasoning models often fail to verbalize causal hint use, with reveal rates frequently below 20% ([Chen et al., 2025](https://arxiv.org/abs/2505.05410)).
- Anthropic's Biology paper already uses internal circuit tracing to audit faithful and unfaithful CoT examples.

E10 is relevant as a possible **internal causal complement** to behavioral monitoring: keep visible text fixed, alter only formed cache state, and observe whether the native continuation changes in the predicted direction. But the evidence currently covers teacher-forced synthetic arithmetic, two Qwen2.5-Instruct sizes, one greedy seed, and admitted successes. It does not yet track latent reasoning in frontier reasoning models, detect deception/reward hacking, recover hidden steps, or show an automated monitor.

Use “provides an exact causal primitive that could support CoT audits” rather than “enables chain-of-thought tracking.” A frontier-lab-strength follow-up would need free-generated long reasoning traces, several current reasoning-model families and scales, preregistered natural tasks, automated step segmentation, causal swaps tied to predicted downstream consequences, negative/irrelevant-step controls, robustness across sampling seeds, and comparison with visible-CoT monitors.

## Relative grades for the audited claims

| Claim area | Evidence quality | Novelty relative to peers | Current prose accuracy |
|---|---:|---:|---:|
| E6 instrument-specific Gemma result | **B+**: pinned, same panel, useful controls; one seed/dictionary and unmatched state coverage | **B** as a direct same-panel basis-failure case study | **C-** because abstracts and §9 generalize beyond the tested basis/operator |
| E10 causal use of a non-restated step | **A- internally**, **C externally**: exact gates and directed swaps; narrow admitted synthetic panel | **C** for the broad causal conclusion; **B** for exact KV-page intervention mechanics | **D+** for the time-circuit reading; it contradicts the definition |
| Claim that standard tools are single-site/by-construction blind | **D** | **D** | **D**; contradicted by ACDC, sliding-window patching, multi-feature tracing, and the paper's own SAE result |
| Cross-architecture certificate/synthesis | **B/B+**, conditional on the other experiment audits | **A-/B+**: no full predecessor found | **B-**; preserve the synthesis while narrowing exclusivity claims |
| CoT-tracking/frontier-lab implication | **C- at present** | potentially high if extended | **D if stated as enabled today; B if stated as a research direction** |

## Concrete revision checklist

1. Remove or revise the E10 “time circuit” reading; the consumed step is individually necessary.
2. Expand §13's CoT paragraph to cover Kudo 2026, Dura 2026, Dutta 2024, Yeo 2025, Anthropic Biology, and ideally Mehrafarin 2026.
3. Rename E6's “matched operator” to “feature-basis interchange analogue” and foreground that reconstruction errors remain clean.
4. Keep “active” before “~18,000 features” in both abstracts.
5. Fix Abstract B's ≤0.08 statement so it applies only to identity; color reaches 0.31–0.42 under all-layer feature interchange.
6. Replace “attribution graphs do not explain cross-position flow” with “they trace OV-mediated cross-position flow while freezing, and therefore originally did not explain the QK source of the attention pattern.”
7. Replace “standard tools miss them by construction” with a claim about common pointwise workflows and the tested sparse basis; acknowledge sliding-window/multi-site support.
8. Reconcile §9's public-SAE result (63% identity, 90% color removed) with the global claim that standard tools cannot see the class.
9. Present the four-quadrant certificate as an operational signature unless a uniqueness theorem is supplied.
10. Frame the paper's strongest novelty as the typed-cut, exact-replay, cross-architecture synthesis and its late-commit/window evidence.
11. Frame CoT relevance as an exact causal audit primitive, then propose the frontier-scale validation needed for “tracking.”

## Sources checked

- [Circuit Tracing: Revealing Computational Graphs in Language Models](https://www.transformer-circuits.pub/2025/attribution-graphs/methods.html)
- [On the Biology of a Large Language Model](https://www.transformer-circuits.pub/2025/attribution-graphs/biology.html)
- [Tracing Attention Computation Through Feature Interactions](https://www.transformer-circuits.pub/2025/attention-qk/index.html)
- [Towards Automated Circuit Discovery](https://arxiv.org/abs/2304.14997)
- [Towards Best Practices of Activation Patching](https://arxiv.org/html/2309.16042)
- [How to Use and Interpret Activation Patching](https://arxiv.org/abs/2404.15255)
- [Measuring Faithfulness in Chain-of-Thought Reasoning](https://arxiv.org/abs/2307.13702)
- [How to Think Step-by-Step](https://arxiv.org/abs/2402.18312)
- [Towards Faithful Natural Language Explanations](https://arxiv.org/abs/2410.14155)
- [LLMs Faithfully and Iteratively Compute Answers During CoT](https://arxiv.org/html/2412.01113)
- [When Chain-of-Thought Fails, the Solution Hides in the Hidden States](https://arxiv.org/abs/2604.23351)
- [Mechanistic Interpretability of CoT via Sequential Activation Patching](https://arxiv.org/abs/2608.22332)
- [Monitoring Reasoning Models for Misbehavior](https://openai.com/index/chain-of-thought-monitoring/)
- [Evaluating Chain-of-Thought Monitorability](https://openai.com/index/evaluating-chain-of-thought-monitorability/)
- [Reasoning Models Don't Always Say What They Think](https://arxiv.org/abs/2505.05410)

