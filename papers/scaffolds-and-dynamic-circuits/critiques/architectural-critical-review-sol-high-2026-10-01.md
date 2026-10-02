# Focused critical review — architectural paper as the third paper

**Reviewer:** independent GPT-5.6 Sol/high pass  
**Date:** 2026-10-01  
**Scope:** read-only review of [`architectural-paper.md`](../architectural-paper.md) against [`time-emphasis-paper.md`](../../space-and-time-circuits/time-emphasis-paper.md), [`bridge-paper.md`](../bridge-paper.md), the corrected [Qwen routing findings](../../../../saturn/experiments/2026-10-01-qwen-routing-mediation/FINDINGS.md), and the [predecessor causal-mask audit](../../../../saturn/experiments/2026-10-01-scaffold-dynamic-circuits/ar-feedback/corrections/2026-10-01-causal-mask-audit.md). No model runs or manuscript edits were made.

## Verdict

The draft contains enough strong evidence for a publishable third paper, but its distinct scientific object is not yet stated sharply enough. The first paper establishes formation → committed causal state → consumption. The bridge proposes reusable role organization with context-dependent participation. The third paper should explain and test the missing middle:

> **trained reusable substrate → prompt/history-built runtime scaffold instance → operation-specific causal support → native write/commitment → later consumption**

The current definition at `architectural-paper.md:48` jumps from a reusable functional scaffold directly to a “dynamic circuit instance” containing source, address, payload, timing, and participation. That collapses the history-built runtime object into the operation-specific support active on it. This matters scientifically: without the middle level, ordinary fixed architecture plus changing activations can be relabeled as a scaffold and a dynamic circuit.

The present evidence earns a strong bounded **reusable causal-interface** result in Qwen and complementary family-local source/state/write results. It does not yet earn a complete learned runtime-scaffold chain, a shared cross-family graph, or repeated role-specific semantic feedback. The draft generally admits these limits, but the abstract and conclusion should make the bounded Qwen claim the paper's center rather than presenting an inventory of every supporting system.

## What is already scientifically earned

### 1. A reused causal interface with operation-dependent authority

The strongest result is correctly identified at `architectural-paper.md:189-205`. The L22–27 interface was selected before the three transfer scenes; it carries several fact types; and the exact same parent and installed K/V bytes have different causal effects under opposite native questions. This is stronger than “different prompts produce different activations.” It establishes reusable stored-state authority plus query-conditioned consumption.

The microscopic follow-up at `architectural-paper.md:207-219` adds two recurring value coordinates and complementary six-query-head groups with operation-specific weighting. It is good mechanistic support, but it is one fox/cat scene and one order. It should remain an exploratory lowering of the coarse interface, not the proof of a general scaffold.

### 2. A source-to-formed-store chain

The 42-row E20 result at `architectural-paper.md:199-205` gives the paper its non-generic causal anatomy: a supplied earlier residual causes the recipient's native suffix to form a later store; isolated block removes the source effect; independent transplant rescues an unseeded recipient. This is the direct inheritance from the time paper. The draft correctly leaves the internal writer path unresolved.

The formation successors at `architectural-paper.md:221-234` are useful because the alias miss prevents an anchor-only story. Scene, retrieval, and literal copying broaden the organism; aliasing shows that later binding computation is missing. These are exploratory boundary cases, not additional independent confirmation.

### 3. A bounded causal route contribution under qualified native execution

The routing section at `architectural-paper.md:244-260` accurately tracks the corrected packet. One L22 final-query attention row changes answer margins using recipient-live values. Restoring baseline routing attenuates the selector effect by 25.0%, 9.5%, and 40.0%, while substantial selector effects remain. The place result is correctly marked tie-sensitive; newly appended L23 K/V and the current answer are correctly treated as parallel endpoints rather than a demonstrated mediation chain.

The predecessor defect is handled properly. The paper states that the old 0.5B and 1.5B E6/E8-style packets omitted the matching mask factory and are not qualified native causal eager evidence. It uses the corrected 1.5B rerun instead and does not requalify the 0.5B result (`architectural-paper.md:260,336-340`). This matches the corrected findings and audit. No material routing contradiction was found.

### 4. Bounded prospective programs

The SDXL held interaction programs at `architectural-paper.md:360-378` are genuine prospective evidence within a supplied factor family: held conjunction conditioners remain unopened until the program and controls are sealed. The unseen-family miss is especially valuable because it separates recurring depth/segment structure from payload extrapolation.

The Mamba affine carrier result at `architectural-paper.md:278-284` similarly supports bounded native-source-to-carrier synthesis, with object-specific maps, supplied native query nodes, small development support, and recipient-local offset failure all retained. These are supporting compiler results, not evidence for a universal scaffold.

## The missing conceptual middle

Add a four-level operational object near §1 and use it consistently:

1. **Trained substrate `S_theta`:** fixed weights, modules, and potential native interfaces. “Trained” states provenance; it does not prove that a particular role graph was learned as such.
2. **Runtime scaffold instance `Gamma_h`:** prompt- and history-built state under one causal parent—actual K/V, residual/latent/recurrent state, and available native read/write ports. It must have independently testable causal authority and persist long enough to support more than one possible operation or update.
3. **Dynamic support `D(Gamma_h, u_t)`:** the operation-specific subset, route, weighting, payload, and timing made causally relevant by the current query or operation `u_t`.
4. **Committed successor `Gamma_h'`:** state produced by a native writer and independently shown to affect a later consumer. This closes one update. Repeating the test can establish feedback.

This object is not earned merely because a network has activations. It becomes discriminating when the experiment can:

- vary prompt/history while holding the trained substrate fixed and causally change `Gamma_h`;
- hold `Gamma_h` fixed while changing the current operation and observe selective `D`, as the same-patch Qwen assay does;
- intervene on the native writer or newly committed state; and
- independently block/rescue that new state before a later consumer.

Current Qwen evidence strongly covers the first source/store formation and the second query-conditioned-consumption pieces, but in different joined panels. The corrected routing packet adds a live-read contribution, yet its new K/V has not been shown to mediate a later computation. The complete five-arrow chain is therefore an executable hypothesis assembled from measured segments, not yet one end-to-end causal result.

## Where the draft still risks relabeling generic architecture

### [Major] “Functional scaffold” remains too close to role-named architecture

At `architectural-paper.md:44-75`, source, address, carrier, writer, state, and consumer can be assigned to almost any autoregressive or diffusion computation. The manuscript says roles need intervention support, which helps, but recurrence at a broad late interface may still reflect a generic depth bottleneck or the built-in cache ABI. The cross-family table at `architectural-paper.md:286-302` is explicitly a candidate abstraction and the post-hoc matcher nearly ties a depth null; that table cannot establish the class.

The strongest defensible language is **reused causal interface** or **candidate runtime-scaffold organization**. Reserve **learned functional scaffold** for a discovery-frozen role profile that predicts held causal effects beyond matched depth/site/energy and operation-blind policies. The paper already proposes this at `architectural-paper.md:304-318`; it should also govern the main noun in the abstract and conclusion.

### [Major] “Native feedback is measured” is too broad for the scaffold-specific claim

At `architectural-paper.md:328-340`, autoregressive continuation consumes generated tokens and cache, and the conversation branches consume their own earlier output. That is valid native recurrence, but it is also generic model execution. The corrected routing experiment has not blocked/rescued the newly written K/V before a later consumer. The scratchpad handoff is admitted/teacher-forced and does not replace a free two-cycle assay.

Accordingly, `architectural-paper.md:26` and §11.1 should say that native recurrence/continuation is exercised under an external clock, while **role-specific semantic feedback remains unestablished**. The current phrase “externally clocked native feedback” can remain a systems property only if it is not presented as the architectural novelty.

### [Moderate] Compilation and executable memory are consequences, not the central scaffold evidence

Exact complete-source compilation runs the native conditioner and reproduces native success and native error. Durable VM reopen proves custody and executable state. These are valuable systems results, but neither distinguishes a learned scaffold from a well-engineered boundary. The manuscript recognizes this at `architectural-paper.md:134-147,360-367,390-414`; their prominence in the abstract and 10,941-word evidence tour still dilutes the scientific claim.

Keep the prospectively held compact interaction programs in the main evidence. Move complete-source replay, VM persistence, cost accounting, and tool inventories to an implications section or appendix.

## Strongest bounded main claim

I recommend a claim close to the following:

> In frozen Qwen2.5-1.5B, a recipient-formed late K/V interface is reused across several contents and operations. Byte-identical stored-state interventions acquire different native authority under different questions; two value routes show operation-specific weighting in one resolved scene; and a native-qualified intervention on one late attention row carries a bounded portion of a selector's answer effect while leaving other paths consequential. These results support a runtime-scaffold account of reusable state and operation-specific causal support, without yet establishing its learning origin, a complete update loop, or a universal cross-family graph.

Diffusion and Mamba should then be described as convergent family-local tests of individual roles and bounded program prediction. This is a strong paper because it joins formation, stable state, changing operation, and partial live routing at native interfaces. It does not need a universal architecture claim.

## Genuinely necessary next evidence

Only one new experiment is necessary for the stronger full-chain claim: a **prospective joined Qwen runtime-instance assay**.

1. Freeze the coarse store and microscopic reader/route policy before new scenes and operations.
2. Use two prompt histories to build different recipient-native runtime states at a common typed boundary.
3. Cross each fixed state with two native queries, preserving the same-parent/same-patch design.
4. Intervene on the predicted read route or value group, then capture the model-produced successor K/V.
5. Hold the emitted visible token fixed where needed, and independently block/rescue that successor K/V before a later native question or operation.
6. Compare with site/depth-matched, energy-matched, wrong-history, wrong-source, and operation-blind policies under the same intervention budget.

This single design distinguishes trained substrate, history-built runtime instance, operation-specific support, native write, and later consumption. A second cycle would establish repeated feedback, but one clean successor mediation is enough for the paper's immediate architectural advance. Mixed rows should remain signed evidence rather than becoming a conjunctive pass/fail gate.

If the paper retains **learned** as more than provenance, a separate same-family developmental study is necessary: freeze the role map and controls, follow it across competent checkpoints, and compare against matched architecture/depth policies. The current Pythia trend shows developmental causal sensitivity in another organism, while early/shuffled incompetence prevents it from proving the learning origin of the specific Qwen organization. The simpler option is to say “present in a trained checkpoint” and leave acquisition open.

Broad cross-family alignment, autonomous goal selection, a unique minimal graph, and more scene counts are not necessary for the bounded third-paper claim.

## Concrete narrative and supporting records

The absent anime eye example should be added as the paper's concrete explanation of the middle level, preferably immediately after the conceptual diagram:

- Early versus late installation of the **complete target-derived contextual text stream** yields different edits: early changes composition while retaining blue eyes; late reaches violet eyes with lower whole-image displacement and visible collateral.
- The separate program × incoming-register 2×2 gives eye-region projections 0.7124 and 0.4035 for the single factors and exact native joint RGB for both.

Together these make “current operation over carried history” visible. Preserve that the edit is target-assisted, full-stream, single-case, and collateral-bearing, and that the terminating-boundary factorial shows joint endpoint authority rather than independent mediation. The source is the [scene-editing record](../../../demos/scene-editing.md).

Two older records can support, but should not carry, the claim:

- The [FLUX persistent-object program](../../../../saturn/experiments/2026-09-09-flux-persistent-object-program/FINDINGS.md) joins four operations through each branch's prior RGB and shows trajectory dependence plus a contextual-geometry failure. Its handles, grammar, operation register, and source factors are host supplied, so it is evidence for an executable runtime instance and its insufficiency, not a learned model-selected loop.
- The [genome attention program](../../../../saturn/experiments/2026-09-09-genome-attention-program/FINDINGS.md) exactly extracts and replays conditional attention writes and finds order-sensitive value contribution in 0.5B and route/value interaction in 1.5B. It copies the complete attention module and relies on native hidden states, supplied architecture equations, and native prefixes/suffixes. It supports executable operation structure, not discovery of a compact semantic graph or the complete formation/write/consume chain.

## Alignment as the third paper

Use a distinct title and division of labor:

- **Paper 1:** identifies the time-formed causal object and its source → formed store → consumer anatomy.
- **Paper 2:** states the functional-scaffold hypothesis, claim ladder, alternatives, and cross-family research program.
- **Paper 3:** tests how a trained substrate is instantiated into runtime causal state and how a current operation selects support on it, centered on Qwen with diffusion as the visual explanatory case.

A title such as **“Runtime Scaffold Instances: From Formed State to Operation-Specific Causal Support”** would make the new contribution legible and avoid duplicating the bridge's “Scaffolds and Dynamic Circuits” identity.

The paper should lead with the four-level object, then present Qwen formation/store/query/read evidence, the corrected partial routing result, and the missing successor mediation. Follow with the anime program/register narrative and the strongest bounded prospective compiler results. Cross-family role tables, Pythia, persistent memory, VM closure, and the tool catalog can support the argument without sharing equal narrative weight.

## Final assessment

The draft has the evidence discipline, counterexamples, source custody, and mechanistic pieces needed for a strong paper. Its decisive revision is conceptual compression, not another broad evidence sweep. Define the runtime scaffold instance separately from both the trained substrate and the operation-specific dynamic support; center the bounded Qwen result; present diffusion as a concrete current-program × carried-history case; and state that successor-state mediation is the missing link. With that framing, the paper advances the sequence rather than restating the bridge or converting generic recurrent execution into a new class by terminology.

---

## Addendum — prospective Qwen held panel, 2026-10-01

This addendum updates the prospective-evidence assessment after direct inspection of the frozen [preregistration](../../../../saturn/experiments/2026-10-01-scaffold-confirmation/qwen-predictive/PREREGISTRATION.md) and held [`analysis.json`](../../../../saturn/experiments/2026-10-01-scaffold-confirmation/qwen-predictive/results/qwen-predictive-held-20ede7e6e0c0/analysis.json), [`context-analysis.json`](../../../../saturn/experiments/2026-10-01-scaffold-confirmation/qwen-predictive/results/qwen-predictive-held-20ede7e6e0c0/context-analysis.json), and [`postrun-verification.json`](../../../../saturn/experiments/2026-10-01-scaffold-confirmation/qwen-predictive/results/qwen-predictive-held-20ede7e6e0c0/postrun-verification.json). It supersedes the review's statement that the fine reader map is supported only by the original fox/cat scene.

### Material update

The full discovery-frozen 24-coordinate signed profiles prospectively recur across eight held context clusters. Context-aggregated no-fit signed cosines are **0.8135 for color, 0.9269 for identity, and 0.9541 for relation**, compared with **0.0998, 0.1121, and −0.0850** for the matched coordinate permutation and **0.4854, 0.7321, and 0.3668** for the cyclic wrong-operation profile. This is strong prospective evidence that the late interface contains reusable, operation-structured causal support rather than merely a post-hoc map of one scene.

The result is not uniformly operation-specific at every resolution:

- Relation is the cleanest profile result: the mapped profile wins raw RMSE on all 16 binding rows, and the predicted coarse site and reader order each transfer in 7/8 contexts.
- Identity has strong profile recurrence and its predicted coarse site/reader order transfers in 8/8 contexts, but native identity readout competence is only 6/16 rows.
- Color has strong shape recurrence against coordinate permutation, yet its raw RMSE (0.1418) is slightly worse than the operation-blind profile (0.1372). Its coarse site order transfers in only 1/8 contexts and reader order in 0/8. The color result therefore supports reuse of the full distributed profile, while disconfirming the proposed two-site/two-group summary as a portable color rule.
- Native competence is 15/16 for color, 6/16 for identity, and 15/16 for relation. The unseen size readout is unavailable, so it supplies no semantic generalization claim.

The 5% and 20% `v_proj.weight` row permutations do not produce the preregistered expected degradation on competence-matched contexts. They therefore do not establish dependence of this organization on the perturbed weight correspondence or its learning origin. This is an unresolved instrument/hypothesis result, not evidence that the causal profile was unlearned.

The post-run verifier records `instrument_status: executed` and `mechanics_status: valid`, with no final errors and 1,728 physical forwards. It explicitly reconciles shared content-addressed StateCuts/logical lane identities while retaining the frozen verifier's original lane-receipt denominator error. This is an appropriate correction trail rather than a reason to discard the held effects.

### Revised bounded main claim

The paper can now make a stronger within-model predictive claim:

> In frozen Qwen2.5-1.5B, discovery-derived signed causal profiles over a late 24-coordinate K/V interface prospectively predict held intervention-effect shape for identity, color, and relation across eight context clusters, substantially outperforming a matched coordinate permutation and a cyclic wrong-operation profile. Identity and relation also preserve the predicted coarse site/reader ordering, while color preserves the distributed profile but not that coarse ordering. Joined with recipient-formed-store mediation and same-state/different-query consumption, this establishes a bounded predictive runtime-scaffold profile in one checkpoint.

This upgrades “candidate runtime-scaffold organization” to **prospectively supported within-model scaffold profile**. It still does not establish a universal microscopic map, learning origin, cross-family alignment, or a full native update loop.

### Revised next-evidence priority

Repeating a frozen microscopic held-profile experiment is no longer the primary missing evidence. The decisive next cut remains the joined successor mediation described above: let a current operation read the history-built store, allow the model to write successor K/V, then independently block/rescue that successor before a later native consumer while controlling the visible token. That experiment would connect predictive operation-specific support to native commitment and later use.

The held profile already includes matched coordinate permutation, wrong-operation, operation-blind, and executed wrong-donor comparisons, so a generic-architecture explanation is materially narrowed. It is not eliminated: the operation-blind color competitor and failed color coarse ranks show that some recurrence belongs to a shared late-interface shape rather than the proposed operation-specific summary. Preserve that heterogeneity as part of the result.

Learning origin remains a separate question. The completed perturbation panel does not support the expected dose degradation, so the paper should continue to say “present in a trained checkpoint” unless a competent developmental or more diagnostic weight-organization assay establishes acquisition.
