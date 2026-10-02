---
title: "Scaffolds and Dynamic Circuits"
subtitle: "Causal evidence for state-dependent semantic computation"
type: research-paper
status: empirical-draft
date: 2026-10-01
updated: 2026-10-01T17:36:48-07:00
author: Jacob Hollenbeck
companion_to:
  - ../space-and-time-circuits/paper.md
evidence_root: ../../../saturn/experiments/2026-10-01-scaffold-dynamic-circuits/
confirmation_root: ../../../saturn/experiments/2026-10-01-scaffold-confirmation/
tags: [interpretability, causal-circuits, dynamic-circuits, diffusion, autoregressive-models, state-space-models]
---

# Scaffolds and Dynamic Circuits

## Causal evidence for state-dependent semantic computation

Jacob Hollenbeck

*Empirical draft, October 1, 2026.*

The companion [outline](outline.md) records the larger experimental program. This manuscript integrates the original thirteen-package campaign, the prior-fixed Qwen context study, and the later [confirmation campaign](../../../saturn/experiments/2026-10-01-scaffold-confirmation/FINDINGS.md) into one empirical architecture account. Package verification establishes execution and evidence integrity; it does not certify a shared architecture or constitute a public release. The older 0.5B/1.5B selector packets used a defective custom causal-mask registration, so §10 preserves their observations as historical instrument records and derives the current feedback claim only from the separately qualified native packet. The [receipt-linked status audit](evidence-status-audit-2026-10-01.md) maps the combined evidence.

## Abstract

We investigate whether neural models reuse a stable organization of causal roles while particular inputs and carried states instantiate different semantic computations. We call the proposed class **scaffolded dynamic circuits**: source information and a current operation interact with carried state to determine a read, produce a write, and update state available to later computation. A recurrent member additionally returns model-formed state to a later native computation. The scaffold is a proposed learned organization of roles, rather than the engineered module graph or a constant activation tensor. We test components of this account in diffusion, autoregressive transformers, and autoregressive state-space models using controlled state interventions and unchanged native consumers.

Qwen experiments show query-conditioned causal consumption of the same recorded state patch and an upstream seed → recipient-formed store → continuation chain. A discovery-frozen 24-coordinate profile predicts unopened spatial-relation effects better than three fixed alternatives in all eight context combinations (competent cosine .954 versus .566 operation-blind; raw RMSE .029 versus .149). Color transfers partially, identity is readout-limited, and size is unavailable under the frozen held format. A native-qualified packet independently manipulates successive model-formed K/V rows and closes a directed two-update semantic path in development and one city/country case out of three held contexts. Fully permuting all 256 output rows and biases of only L22/L23 `v_proj` after the holdout collapses relation profile cosine from .955 to .049 and reduces native competence, establishing final-checkpoint correspondence dependence without dating acquisition. In FLUX.2 Klein 4B, selected site/time policies transfer across five new contrasts, while an upstream lexical-row relation policy misses and a post-hoc broader-context intervention recovers the relation with collateral. Mamba experiments expose late state interfaces at two sizes. A prospective FLUX/Mamba formed-state/consumer profile has RMSE .0928 versus .8526 for a frozen role permutation; a separately prospective Qwen appendix agrees on its one competent row but reverses in the all-row normalized diagnostic.

These findings support reusable causal interfaces and state-dependent semantic computation in bounded cases. A unique learned role graph shared across families, autonomous semantic operation selection, and general automatic address/payload compilation remain open. The paper integrates predictive recurrence, serial semantic mediation, and final-weight dependence while retaining the heterogeneous results that limit their generality. Ordinary attention and routing can implement the measured organization; a complete learned role graph requires further causal prediction and localization.

## 1. Introduction

An interpretability account can locate a component that influences an answer without explaining how the model selects that computation or how the resulting state becomes available to a later operation. A color may be supplied through one state boundary, an object's placement through another, and a question may change which of those stored variables affects the output. The computational object may therefore include both a recurring interface and a context-dependent program running through it.

The motivating observation arose during work on a diffusion scene generator. Object identity, eye appearance, geometry, placement, and relations could be manipulated through a recurring execution structure, while the effective semantic support varied with the scene and stage of generation. The resulting interpretation was a stable architecture with dynamic circuits that branch through it and return information to accumulated state. The predecessor [Space and Time Circuits](../space-and-time-circuits/paper.md) establishes the importance of separating source formation, storage, and consumption. The present paper asks whether that separation describes a reusable organization of computation.

This question needs stronger evidence than the observation that weights stay fixed while activations change. Input-dependent attention and recurrent state are already properties of the model architectures. The proposed scientific object is a **learned causal role organization** that predicts interventions across contexts: where a source can seed computation, what a later operation reads, where its result is written, and how the resulting state affects subsequent computation. Different physical layers and state types may implement corresponding roles.

The completed experiments identify recurring interfaces and show that their effects depend on operation, state scope, and cut. Prospective prediction is strongest for spatial relation, while counter-trends delimit operation transfer. The serial packet demonstrates independent later authority of a model-formed semantic row. A developmental panel links increasing competence to stronger causal effects in Pythia; same-surface Qwen disorder separately establishes final-weight correspondence dependence. The partial cross-family formed-state/consumer core is prospectively supported, with source, live-read, minimal-writer, and feedback roles still unmatched across families.

| Contribution | Evidence reported here | Scope |
|---|---|---|
| Reusable causal interfaces | Frozen diffusion addresses, transformer writer/store assays, and a prospective 24-coordinate Qwen profile | Relation profile recurs in 8/8 context combinations; color/identity/size delimit transfer |
| State-dependent semantic computation | Query-conditioned consumption, formed-store rescue, and independently manipulated successive formed rows | Bounded two-update path in development and one of three held contexts; host supplies prompts and donors |
| Learned task organization | Six authenticated Pythia checkpoints plus full L22/L23 Qwen value-row disorder | Developmental trend in one Pythia task and final-weight correspondence dependence in Qwen; Qwen chronology remains open |
| Cross-family architectural hypothesis | Frozen FLUX/Mamba formed-state/consumer profile and separately admitted Qwen appendix | Partial common edge; shared source/read/write/feedback graph remains unestablished |

The distinction between a transformer and a state-space model is architectural. **Autoregressive** describes an execution regime; both architectures can execute autoregressively. We retain that distinction throughout.

## 2. The scaffold and dynamic circuit hypothesis

### 2.1 A causal role scaffold

Let a model execute with external source information `u`, current operation `q`, and carried state `z_t`. A candidate role-level description is:

\[
a_t = R(u,q,z_t), \qquad
w_t = W(u,q,z_t,a_t), \qquad
z_{t+1} = U(z_t,w_t), \qquad
y_t = C(q,z_{t+1}).
\]

Here `a_t` denotes the active read or family-local transition, `w_t` a write, `U` state update, and `C` the unchanged native consumer. The next operation may read the updated state. This is a proposed causal abstraction, rather than a newly fitted mathematical model of the measured networks. A model can implement these roles through distributed, redundant, or locally concentrated mechanisms.

The **functional scaffold** is the recurring organization of these roles and their causal relations. “Static” means reusable across specified contexts, not immutable during learning or identical at every layer. A **dynamic semantic circuit** is the execution-specific support, payload, timing, and route whose intervention changes a declared semantic variable through the native consumer. A physical interface may recur while its current payload and semantic effect change.

A recurrent member additionally requires updated state to affect a later read or transition. The historical selector panel proposed a carried-state → read → write/output episode, but its custom attention instrument omitted the required causal-mask registration. A separately corrected routing packet establishes a bounded native read contribution on already-open contexts. The native serial packet goes further: it changes a first formed row, observes the next native semantic prediction, and then changes only that prediction's newly formed row while holding the visible token and recipient computation fixed. This closes a bounded two-update causal path. Because the host supplies prompts, questions, branch choices, and coherent donors, it does not establish autonomous operation selection or an indefinitely self-sustaining loop.

### 2.2 Physical lowering and role identity

For a candidate role graph `G`, a family-local mapping places roles at tensor boundaries, token positions, time steps, or recurrent operands. The mapping may depend on model, context, operation, and current state. It need not be one-to-one: multiple sites can implement a writer, and a single site can support several operations.

Role identity must be earned through intervention relations. A late layer, a high-energy activation, or a tensor named “state” can nominate a candidate. None establishes that the site has the proposed role. A useful role profile records source perturbation, store perturbation, correct and wrong rescue, timing, dose, collateral, and native continuation. Two roles should align because these causal profiles and their dependencies align, rather than because the analyst gives them the same name.

### 2.3 Competing explanations

Broad replacement of a downstream state can move output toward a donor without identifying a semantic circuit. A fixed late interface can also reflect architectural depth or a generic bottleneck. A routing change can be an ordinary consequence of replacing source information. Cross-family alignment can arise from coarse role labels and incomplete profiles.

The experiments therefore ask more specific questions: do addresses chosen before held outcomes retain directed effects; does the same store behave differently under different native operations; does carried state alter a subsequent read when facts and the live query are fixed; and does task-relevant causal organization change across learning? Each question weakens some alternatives while leaving others open.

## 3. Relation to space and time circuits

The predecessor distinguishes local causal support from controlling state formed through ordered execution. Its strict path-distributed subtype requires a declared joint path to be necessary and sufficient while no singleton meets those criteria at the same cut and resolution. That certificate concerns the distribution of causal support.

The scaffold hypothesis concerns the organization through which different semantic computations form, store, and consume state. It can contain a locally decisive writer, a redundant store, a distributed path, or a mixture. A strict four-quadrant pattern is therefore an optional subtype, not a requirement for this paper's proposed class. No new exhaustive four-quadrant certificate is claimed here.

The scene generator is practical motivation for this distinction. Earlier compilation work used manipulable model-state boundaries to reproduce native scenes and compose edits. Those results show that state interfaces can support executable applications. They do not by themselves prove that the learned network has a unique reusable role graph, and they are not counted as new experiments in this campaign.

## 4. Experimental protocol

### 4.1 Models and native consumers

The combined evidence uses `black-forest-labs/FLUX.2-klein-4B` at BF16 with four denoising steps and 256×256 outputs; `Qwen/Qwen2.5-0.5B` and `Qwen/Qwen2.5-1.5B` at BF16 in the original campaign; `state-spaces/mamba-130m-hf` and `state-spaces/mamba-370m-hf` at FP32; and `EleutherAI/pythia-70m` at FP32 across six training checkpoints. The prior-fixed context study and the predictive and feedback confirmation packets use Qwen2.5-1.5B FP32 under their separately sealed runtimes. The cross-family confirmation uses native CUDA BF16 FLUX, CUDA FP32 Mamba-130M, and the separately admitted FP32 Qwen packet. These numerical paths are not treated as interchangeable replications.

Diffusion branches continue through the native scheduler and VAE to RGB. Language-model branches use the unchanged full-vocabulary head, with four-token or eight-token greedy continuations where specified. Internal attention, state distance, and profile agreement are supporting measurements. Native output determines what the model did; correctness, semantic specificity, and collateral still require separate interpretation.

### 4.2 Discovery and evaluation

The primary diffusion, transformer, and SSM panels use finite discovery profiles to freeze family-local addresses before opening held outcomes. Candidate interfaces are partly nominated by earlier work; this is disclosed prior information, rather than an unconstrained whole-model discovery claim. Held rows test new contexts or operations within the stated organism. The Qwen prediction packet freezes 24 coordinates—layers 22–27, two K/V head groups, and K versus V—plus operation-blind, wrong-operation, and within-band permutation alternatives before opening two lexical sets × two templates × two orders. The cross-family packet separately freezes a four-coordinate formed-state/consumer profile before two FLUX and two Mamba rows; its later Qwen appendix has its own prospective admission boundary.

Intervention **addresses** and **payloads** have different provenance. Frozen addresses can be predicted prospectively even when native donor trajectories supply held payloads. Most campaign interventions use such donor state. The selector panel assembles its held prefix state before evaluating the held query outcome, but still receives donor activations and supplied semantic positions. It is not a learned semantic compiler.

Post-hoc relation diagnosis, the original role matcher, and opened-outcome mechanics reproduction are identified separately. The old matcher is distinct from the later prospectively frozen partial cross-family profile. The corrected Qwen routing packet uses already-open contexts and adds no fresh holdout denominator; it does not rehabilitate the historical selector measurements. The separate prior-fixed Qwen study contains a pilot and same-policy lexical transfers; its correlated arms do not become independent replications.

### 4.3 Common parents and controls

Branches share an immutable native parent, while mutable branch state is isolated. No-op, reinstall, intervention delivery, input/model identity, state shape, and lineage validate the instrument. Family-specific controls include wrong donor, wrong site or time, sign reversal, dose, paired or unpaired state permutations, read blocking, and fixed-site comparisons. The available control set varies across modules; the common protocol is not a claim that every proposed arm was executed everywhere.

Semantic competence is assessed from the native endpoint at the declared horizon. We retain incompetent parents and inapplicable denominators in the full record. They restrict what an assay can establish; they do not establish that a mechanism is absent. Optional arms and misses remain visible rather than being combined into an omnibus scientific gate.

### 4.4 Measurements and sampling

Diffusion target progress is `1 − D(I, I_T) / (D(I_B, I_T) + 10⁻⁸)`, where `D` is mean absolute RGB difference. Zero corresponds approximately to the base endpoint and one to the target. Negative values move farther from the target. Progress is a global image-distance measurement, not semantic accuracy or a percentage of causal control.

Language-model scores use declared answer log probabilities or target-versus-alternative margins, in nats. For Qwen writes, normalized answer effect is `(log p_obs − log p_filler) / (log p_clean − log p_filler)` for the declared answer; the cut numerator is `log p_clean − log p_obs`. Nonpositive or undefined semantic denominators remain inapplicable. Eight-token continuation match is the fraction of positions equal to the clean continuation, with recovery `(match_obs − match_filler) / (1 − match_filler)`. Mamba's signed target-minus-base answer margin change is normalized by the full target-state effect. Pythia's raw target-margin change is normalized only where its native target-parent minus base-parent margin is positive.

Rescue ratios can exceed one or become unstable when the denominator is small. Feedback read balance is attention mass on fact 2 minus mass on fact 1; route recovery is `(balance_compiled − balance_first) / (balance_second − balance_first)`. Writer measurements compare the newly appended query K/V to both native states. Developmental profile agreement is cosine similarity between the concatenated four-context × six-layer raw-effect vector and the final checkpoint's vector. These different normalizations are not pooled into one causal score.

We report per-context outcomes and descriptive trajectories. The small, deliberately constructed organisms and correlated intervention arms do not justify population-level confidence intervals or significance tests based on arm count. A large number of causal branches improves measurement resolution without increasing the number of independent contexts.

## 5. Diffusion experiments

### 5.1 Frozen site and time addresses

Two discovery contrasts, cup color and cat eye geometry, scan a prior-nominated five-coordinate × four-time lattice: joint blocks 1–4 on the text stream and single block 0 on the image stream, each at steps 0–3. Descending signed RGB progress, with lexical tie-breaking, freezes three top-three policies before held trajectory capture: color from the cup row, geometry from the eye row, and global from the mean across both. Color support is `single.0:image@t3`, `single.0:image@t2`, and `joint.1:text@t2`; geometry and global support use the same two image cells and `joint.4:text@t0`. Held color/geometry rows use their operation policy; the unseen relation uses global. Five held contrasts have new contexts and seeds. Native target trajectories supply the state deltas. The panel also crosses suffix conditioner and formed latent at a cut after two steps [D1].

| Held contrast | Selected support | Wrong time | Rolled delta | Conditioner only | Carrier only |
|---|---:|---:|---:|---:|---:|
| Vase color | .741 | .198 | −.109 | .261 | .439 |
| Eye color | .741 | .076 | −.453 | .145 | .628 |
| Fox eye geometry | .626 | .088 | −.402 | .234 | .534 |
| Lamp geometry | .855 | .194 | −1.274 | −.037 | .757 |
| Left/right relation | .967 | .194 | −.178 | −.001 | .974 |

*Table 1. Whole-image target progress. These are descriptive values for five held contrasts, not independent estimates of semantic recovery.*

Half-dose progress ranges from .170 to .325, and every negative-dose response is negative. Both complete native parents and their final registers are recovered exactly through the intervention-shaped replay path. The selected support transfers across these contrasts with sign and dose structure, although two selected cells replace late full image-stream state. Generic downstream overwriting remains a material alternative.

The conditioner/carrier factorial gives a more precise attribute observation than the global score. In unblinded AI inspection, the conditioner-only eye-color arm has blue irises despite .145 image progress, while the carrier-only arm retains red irises despite .628 progress. The spatial relation and lamp outline instead follow the formed carrier at this cut. Thus higher global target similarity can misidentify which branch controls a particular attribute. Relation targets also differ in lighting and sphere appearance, so this is not isolated relation editing.

Pixel difference-in-differences residuals range from .058 to .506 of the native target-delta L2 norm. They describe image-level interaction, not a requirement for the architecture or proof of semantic conjunction. Independent blinded attribute and collateral scoring remains pending.

### 5.2 Upstream text support

A second prospective panel permits only joint-text interventions and replaces the changed lexical-token rows, leaving all other rows exact. It reuses the disclosed discovery contrasts but evaluates four fresh held contrasts. No image-stream state is installed [D2].

| Held contrast | Selected lexical rows | Wrong time | Rolled rows | Conditioner only | Carrier only |
|---|---:|---:|---:|---:|---:|
| Bowl color | .343 | .330 | .009 | .366 | .342 |
| Bird color | .410 | .391 | −.039 | .234 | .574 |
| Clock geometry | .584 | .033 | −.033 | −.013 | .710 |
| Above/below relation | −.045 | .025 | .037 | −.001 | .963 |

*Table 2. Upstream lexical-row target progress. Color has weak timing specificity; the new relation is a prospective miss.*

Visual review finds purple bird and dark blue/purple bowl surfaces, with bird orientation and geometry collateral. The clock becomes rounded or octagonal rather than a clean circle. The cone remains above the cube under the selected lexical rows, although native endpoints express the intended relations and the carrier-only branch renders below. This failure is informative about the chosen address basis. It cannot be explained by native relation incompetence in this row.

### 5.3 Diagnosing relational scope

One post-hoc diagnostic retains that failed row and the original frozen ports, changing payload scope. The lexical arm reproduces −.045 progress. Whole active text yields .882 and visually places the cone below the floating cube. The nonlexical complement yields .725 and also changes the relation, but creates a duplicate glass block. Row-permuted whole text yields .054 and retains the base relation [D3].

Sixteen single-port whole-text probes show strong step-zero composition changes (.656–.713), with overlap collateral; later ports retain the base relation. The working inference is that relation-relevant information extends beyond the changed word's row and is sensitive to early contextual state. Broader text replacement can also overwrite several scene variables at once. The panel therefore does not identify a minimal relation representation, establish multiport necessity, or turn the original prospective miss into a held success.

## 6. Autoregressive transformer experiments

### 6.1 Recurring write interfaces

The Qwen2.5-0.5B discovery panel profiles residual writes, K/V writes, and K/V cuts across layers. Two identity discovery contexts freeze residual L2, K/V writer L20, and K/V cut L21 before a disjoint identity context and color evaluations [T1]. It retains 2,016 discovery and 748 held arm rows. Those rows are correlated intervention measurements.

Residual and write effects recur at the frozen addresses. The cut assay is less specific: its shuffle control is degenerate and a wrong-source arm is stronger than the selected intervention. Native color competence is heterogeneous, including one context with zero clean first-token accuracy. Consequently the panel supports recurring writer interfaces more strongly than a unique source-specific cut.

### 6.2 Source to formed store to continuation

A continuation extension reuses the frozen addresses on four new identity and four new color examples. An early L2 seed lets the recipient execute its unchanged suffix and form endogenous L20 K/V. The seed reproduces all eight clean native identity tokens on 4/4 rows, including two native task mistakes. Reproducing a native trajectory establishes control of that trajectory, rather than correctness on all four tasks [T2].

Blocking the formed store reduces answer evidence on all four identity rows. Installing the recipient-formed store into an unseeded path increases answer evidence on 4/4, with median recovery of .793 of the seeded answer gain. Clean continuation match improves on 2/4. Color rescue is positive on 2/4, median recovery .083, with no continuation-match gain.

This is a bounded source → formed store → native continuation chain with redundant routes and operation-dependent mediation. The source seed is supplied; endogenous downstream formation does not make the entire procedure donor-free. Partial continuation improvement also limits any claim that the store alone specifies the complete future program.

### 6.3 Query-dependent readability

An actual animal/color query × source-cache factorial uses coherent prompts carrying both facts. Paired native source prompts answer both queries correctly. A frozen L20 cache installed into a neutral parent transfers fox, lion, and a coherent wrong-donor dog under the animal query, with answer gains of 1.398–1.652 nats. The same cache band fails to transfer red and green under the color query. The source-specific margin is 1.844 nats for animal and −.031 for color [T3].

The result distinguishes operation-dependent store readability from native prompt incompetence. It also shows why a useful recurring physical interface should not be labeled a universal semantic store.

### 6.4 The same stored patch under different questions

A separate contemporaneous Qwen2.5-1.5B FP32 study provides a complementary contrast [Q1]. Prior E20 evidence fixes late K/V L22–27 and comparison L16–21 before a fox/cat pilot and three same-policy lexical transfer packets. Across 32 opposite-query parent pairs, all 128 directional patch manifests and recorded tensor digests match. The question changes while the recorded parent and patch stay fixed.

Query-selective harm is positive in 16/16 directional color contrasts, median 3.130 nats, and 16/16 position contrasts, median .583. Queried late fact-span replacement makes donor color the full-vocabulary top choice in 16/16 and donor position in 12/16. Identity transfer appears in 11/11 available four-token reads; five reads are unavailable and remain part of the sixteen-row population. Position also transfers at the earlier band in 9/16, limiting unique late localization.

An oracle-assisted L12 seed yields target identity in 16/16 generated reads; the recipient forms downstream state, and transplanting its formed late anchor rescues identity in 16/16. The optional composed position→color assay is diagnostic, with native competence 15/16 and donor color top choice 7/16.

This study supports query-conditioned causal consumption and a reusable late interface. Its custody is receipt-level: recorded manifests and digests are checked, but activation tensors are unavailable for a fresh offline rehash. Participating heads, query-to-address computation, feedback topology, and automatic address discovery remain unmapped. The packets add breadth within Qwen and are outside the thirteen-package campaign ledger.

### 6.5 Prospective microscopic recurrence and weight correspondence

The confirmation packet freezes a signed 24-coordinate Qwen profile over L22–27 × two grouped-query K/V head groups × K/V, together with an operation-blind mean, a cyclic wrong-operation profile, and a within-band coordinate permutation. Its unopened breadth is two lexical sets × two templates × two orders, with two binding rows per combination. The eight context combinations are the effective comparison units; 128 logical panels, 4,736 receipted lanes, and 1,728 physical forwards measure those units rather than creating additional independent contexts [C1].

| Operation | Applicable contexts | Mapped cosine | Operation-blind cosine | Mapped raw RMSE | Blind raw RMSE | Mapped raw wins |
|---|---:|---:|---:|---:|---:|---:|
| Relation | 8 | .954 | .566 | .029 | .149 | 8/8 |
| Color | 8 | .839 | .828 | .119 | .109 | 5/8 |
| Identity | 4 | .892 | .901 | .204 | .140 | 0/4 |

*Table 3. Competence-applicable profile summaries. Relation transfers cleanly; color retains broad signed similarity but loses the raw-error and reader-order comparisons; identity is limited to four applicable contexts.*

Relation beats every frozen competitor in raw RMSE in all eight context combinations and matches the predicted reader order in all eight applicable comparisons. Color's predicted reader order misses in 8/8 combinations even though its full profile remains similar. Identity produces a registered answer in only 6/16 native binding rows, and its favorable all-row similarity does not survive the competent-only comparison. Size produces no registered native answer under the frozen held format. A later opened-development format obtains identity in 8/8 observations and direct-adjective size in 2/2, diagnosing readout sensitivity without replacing the held consumer or creating new held successes.

Mild permutations of 5% and 20% of L22/L23 `v_proj` output rows mostly preserve the profile. A separately sealed post-held exploratory arm then permutes all 256 output rows and corresponding biases of those two value projections, while preserving tensor geometry and norms and restoring the original weights exactly. Across the same four opened contexts, all-row signed cosine against the frozen mapped forecast changes from .931 to .569 for identity, .838 to .110 for color, and .955 to .049 for relation. These are medians across context means, not direct trained-versus-disrupted profile cosines. Native competence also falls. Relation retains a lower raw error than the blind profile in 3/4 all-row contexts and 2/4 competent/applicable contexts, showing that signed organization and scalar error answer different questions. This establishes dependence of the measured profile on final-checkpoint L22/L23 value-row correspondence. It does not establish chronological acquisition, and the opened-context follow-up is not a second predictive holdout.

![Prospective relation-profile prediction and final-weight correspondence](figures/confirmation-results.svg)

*Figure 1. Panel A shows competent context-median raw RMSE for the frozen mapped and operation-blind profiles; the context combinations cross lexical set, template, and order and are not independent lexical worlds. Panel B shows all-row mapped signed cosine across four already-opened contexts under increasing L22/L23 value-row permutation. The full-dose extension is post-held exploratory and measures final-weight correspondence while competence falls; it is not a training chronology or a whole-model weight test.*

## 7. Autoregressive state-space experiments

Mamba-130M and Mamba-370M separately profile native per-layer convolution state `C` and recurrent state `H`, independently selecting late three-layer bands. The corrected 130M panel freezes [14,19,20]; the 370M panel freezes [32,35,39]. Disjoint identity, counting, and capital contexts are retained [S1, S2].

In this immediate lexical-source assay, convolution state supplies most of the transfer. Recurrent-only replacement is weak. Held identity and capital continuations change to the donor subject or country; coherent wrong donors produce coherent alternate subjects. Early-layer and wrong-sign controls have weak effects. These are state- and cut-specific observations rather than a general claim that Mamba's recurrent operand is unimportant.

Native counting competence is absent in the tested prompts. Some capital continuations begin with an article or preposition, making a strict first-token answer rule inapplicable even when the eight-token continuation contains the semantic answer. We report that distinction rather than treating the scoring rule as a scientific null.

A later-query supplement reuses a previously sealed band but finds no paired native semantic competence in either its primary organism or predeclared alternate. Its semantic factorial is therefore inapplicable [S3]. Diagnostic effects shift toward recurrent state at this later cut. That shift suggests that operand allocation depends on where the computation is observed, but cannot establish semantic query-conditioned consumption.

The maximum native replay logit difference is .0003052 under the declared .001 tolerance. Same-shape batching is qualified for this runtime. Two model sizes support a bounded within-family recurrence of late interfaces; they do not constitute independent-family or independent-laboratory replication.

## 8. Cross-family role alignment

The family-local experiments offer plausible correspondences, but their causal resolution differs. Diffusion includes current conditioning and a formed denoising latent, transformer packets manipulate complete formed K/V rows, and Mamba exposes convolution and recurrent state. The original exploratory matcher used already-open outcomes and nearly tied a depth null [A1]; it remains a post-hoc diagnostic rather than the authority for the common architecture claim.

The confirmation campaign therefore freezes a smaller common object before held execution: formed-state block remaining, coherent formed-state rescue, an actual wrong coordinate, and the intact joint parent. The state-block arm is distinct from rescue, and the wrong coordinate is scored against the same target destination. Two natively applicable FLUX rows and two natively competent Mamba rows yield [C3]:

| Family | State block remaining | Coherent rescue | Wrong coordinate | Intact parent |
|---|---:|---:|---:|---:|
| FLUX | .0845 | .8073 | .1589 | 1.0000 |
| Mamba | .0803 | .9065 | .0020 | 1.0000 |
| Qwen appendix, competent row | .0076 | .9585 | .4939 | 1.0000 |

Across the four FLUX/Mamba coordinates, the causal-role profile RMSE is .0928, compared with .8526 for the frozen role permutation. This earns a prospective partial correspondence: **family-native formed carried state → unchanged family-native consumer**. It does not align a complete source/current-operation/live-read/minimal-writer/feedback graph.

Native endpoints narrow the numerical result. FLUX's boot rescue is mostly blue but retains yellow panels, and either current conditioning or formed state can produce the arched door; whole-image distance understates the current-only local shape effect. Mamba's Athens rescue reaches the target continuation, while the zebra rescue strongly raises the target logit but begins with `small` rather than `zebra`. The supplied donors, differing family clocks, two rows per family, and severe wrong-coordinate controls prevent a universality or minimality claim.

A separately prospective Qwen appendix admits the feedback packet without revising the original FLUX/Mamba contract. Its single competent city/country row aligns better with the causal map than the permuted map against both families and generates `France` under coherent rescue; reversed depth generates `1`, with France ranked 8,377. The all-three-row profile reverses the RMSE comparison because an incompetent tool/material target and a small parent-contrast denominator inflate the wrong-depth ratio to 27.231. That mechanically valid disagreement remains in the record. The competent Qwen row extends the partial common edge; it does not turn four profile coordinates into four independent samples or establish a complete three-family graph.

## 9. Falsifiers and alternative explanations

Several observed controls constrain interpretation. Wrong-time and rolled deltas weaken downstream diffusion transfer, while the lexical color rows show little wrong-time separation. Whole-context relation replacement recovers a relation that lexical replacement misses, but also exposes collateral. Wrong-source K/V cuts can outperform the chosen source, revealing nonspecificity. Earlier transformer and raw embedding interventions demonstrate alternate routes. Mamba's convolution/recurrent balance changes with the cut.

The developmental panel supplies a final-weight shuffle and fixed-site controls (§11). The Qwen profile adds operation-blind, wrong-operation, coordinate-permutation, and graded L22/L23 value-row disorder controls (§6.5). Full Qwen disorder collapses signed relation shape while retaining favorable raw error in some contexts and reducing competence; it is a final-weight correspondence test, not a behavior-matched null or a learning chronology. The Pythia fixed-site control outperforms selected sites on one final row. Neither observation can be suppressed to create a cleaner narrative.

Broader discriminators remain necessary: matched energy controls, site-degree and depth nulls, operation-blind policies, coherent off-task donors, reduced role graphs, and equivalent-budget prospective prediction. A destructive random perturbation is not an adequate comparison for a coherent semantic transplant. Controls must test the specific alternative being considered.

No failed control is used to erase the rest of the evidence. Conversely, mechanically valid execution and a favorable output cannot resolve every alternative. The paper keeps observation, trend, working inference, and terminal claim separate.

## 10. Carried state changes the next computation

**Historical instrument qualification.** Sections 10.1–10.3 retain the original selector packet's design and observations. The subsequent [causal-mask audit](../../../saturn/experiments/2026-10-01-scaffold-dynamic-circuits/ar-feedback/corrections/2026-10-01-causal-mask-audit.md) shows that both model sizes registered custom attention without its mask factory. Their multi-token read, cache, competence, and continuation values are historical instrument observations, not qualified native eager evidence. The corrected routing packet and the new two-update packet have their own native authority; §10.4 reports the latter.

### 10.1 Fixed facts and a fixed live query

The selector-state assay holds two semantic facts and the live query fixed. Donor prefixes differ in their carried selector, indicating first or second. A selector-position residual from a prefix-only donor is installed into the fixed-first recipient, then the native query executes. Selection searches twenty selector/read pairs: selector sites [0,2,4,8,12] × read layers [12,16,20,22]. It maximizes the product of native second-minus-first and compiled second-on-first attention-balance shifts on one discovery organism, breaking ties by lower selector site then lower read layer. No answer logits enter the selection. The next layer is designated for query K/V capture. This nominated writer location is a protocol choice, not an independently discovered semantic commit site [F1–F3].

The selector intervention changes the measured attention read, newly appended query K/V, and native continuation; read-blocking arms separately test contributions to answer evidence. These observations do not establish a serial causal edge from the appended K/V to the output. Hook counts, delivered hashes, untouched rows, read captures, and append geometry establish intervention mechanics. A later independent consumer of the new K/V has not been tested.

### 10.2 Small-model read and appended state

Qwen2.5-0.5B selects selector L12 and read L16 from one discovery organism, with L17 designated as the post-read K/V capture layer. Discovery continuations are “a fox,” “the lion,” and “a lion” after the state installation. Articles make the strict first-token rule fail; the four-token semantic observation is retained separately.

Across three fresh color, object, and place contexts, the intervention shifts fact-2-minus-fact-1 attention balance by +.00765, +.04363, and +.15925. Newly written L17 state moves closer to native-second in all three. Yet native first/second continuations are respectively red/red, plate/plate, and Paris/Paris, and the compiled outputs are unchanged. There is no held native selector contrast to recover.

Fact-2 read blocking reverses attention balance and lowers the second-answer log probability in all three rows, without changing greedy continuation. A raw L0 intervention exactly reproduces native-second; it is effectively source/embedding replacement and is treated as a source baseline. These findings support route/write recurrence and causal read consequences, not held semantic feedback or unique L12 ownership. Exact mechanics reproduction adds no fresh contexts.

### 10.3 Larger-model semantic selection

A single Qwen2.5-1.5B capacity repetition uses the predeclared same template and selection policy, with three fresh held contexts and no prompt retry or additional selector-policy search. Discovery's native selectors both produce lion, so discovery semantic competence remains limited. The prescribed attention search selects selector L4 and read L22 before held outcomes; L23 is designated as the post-read K/V capture layer.

| Held context | Native first | Native second | Installed second state | Read-balance shift | Route recovery |
|---|---|---|---|---:|---:|
| Color | green | yellow | yellow | +.09746 | .916 |
| Object | spoon | fork | fork | +.12878 | 1.006 |
| Place | London, with Madrid supplied | Berlin | Berlin | +.00282 | 4.611 |

*Table 4. Historical selector observations under the mask-defective instrument. Semantic selection appeared to succeed on two contexts among three predeclared held contexts; those recorded competence labels and values are not qualified native causal measurements.*

In this historical packet, the joint color/object observation suggested that carried state changes a later read, new state, and answer while external facts and the live query stay fixed. All three recorded L23 states move toward the recorded second-selector state. The causal-mask defect prevents using these observations as native task evidence; the recorded London endpoint is not a native place counterexample.

Blocking the fact-2 read makes attention balance negative and lowers second-answer log probability by .209, .088, and .335 nats. It changes the place answer from Berlin to the supplied Madrid, while color and object remain yellow and fork. Off-target blocking has mixed score effects. Thus the selected read contributes to answer evidence, but clean full mediation or unique circuit ownership is not established. The successful L0 source baseline further limits unique localization.

Under its historical instrument, the result suggested one state-sensitive read/write episode. The corrected routing follow-up on these already-open contexts supplies native causal evidence that one L22 routing row carries part of the selector effect, but it adds no fresh holdout denominator and does not rehabilitate the old numbers. The independent packet below supplies the qualified later-state mediation result.

### 10.4 Completed two-update confirmation

The [feedback packet](../../../saturn/experiments/2026-10-01-scaffold-confirmation/qwen-feedback/FINDINGS.md) uses fused TokenMachine native-layer execution with causal masks. A same-parent decomposed L22 observer matches the fused path exactly on token, logits, and committed K/V at its capture; semantic outputs come from the separate fused `machine.step`. This establishes parity at the declared observation boundary, not monolithic `model.forward` equivalence on every cycle. Development generates cat→blue→blue; a coherent first formed-row replacement drives red→red. Holding the first state, prefix, later query, visible red token, and recipient final hidden state fixed, replacing only the newly formed second row with blue state makes the final answer blue; zero gives `is`, and exact reinstall restores red. Each intervention replaces the complete newly appended K/V row across all 28 layers at an L27 final-layer cut. “L27 cut” therefore names the resume boundary, not a claim that L27 alone writes or carries the mechanism.

Frozen held job `job-1a141a746afa` closes the same path for Berlin/Germany versus Paris/France. A coherent Paris first-row state changes the native second prediction to France while the visible first token remains Berlin; processing native France forms the recipient second row. With that first state, prefix, later query, visible France token, and final hidden state fixed, replacing only the new France row with the Germany row changes the later answer France→Germany; zero gives `is`, and exact France reinstall restores France. Fruit's base/serial semantic endpoint is incompetent and tool's target formation fails, so the complete paired claim is one of three held contexts. The prompts, known query suffixes, donors, branch selection, and interventions are host supplied. The result establishes a directed two-update semantic path with possible parallel paths; it does not establish autonomous operation selection, a unique/minimal L22/L23/L27 writer, or a donor-free loop. The raw terminal status remains unassessed. [Primary report](../../../saturn/experiments/2026-10-01-scaffold-confirmation/qwen-feedback/results/held-combined-1a141a746afa/report.json).

## 11. Development across training checkpoints

Pythia-70M offers a controlled developmental organism [P1]. All six final-checkpoint layers are evaluated on three label-copy discovery prompts. Mean normalized target recovery across applicable discovery rows ranks layers, with lower-layer tie-breaking and support size two, yielding full-prefix in-forward K/V layers [3,5]. That policy is frozen before four fresh held contexts are evaluated at steps 256, 512, 1000, 2000, 4000, and final step 143000. One FP32 GPT-NeoX runtime is used throughout. A seventh hydration restores final weights before per-tensor shuffling.

| Checkpoint | Native target top choice | Mean signed target-margin change, nats | Profile cosine to final |
|---|---:|---:|---:|
| 256 | 0/4 | .019 | .055 |
| 512 | 0/4 | .200 | .128 |
| 1000 | 3/4 | 2.632 | .620 |
| 2000 | 3/4 | 2.393 | .721 |
| 4000 | 4/4 | 3.258 | .769 |
| Final, 143000 | 4/4 | 3.310 | 1.000 |
| Shuffled final | 0/4 | .041 | .049 |

*Table 5. Four held contexts at each checkpoint. The cosine of the final profile to itself is 1 by definition. The trajectory is heterogeneous, including a decrease in mean effect between steps 1000 and 2000.*

![Developmental trajectories of native competence, raw intervention effects, and layer-profile agreement](../../../saturn/experiments/2026-10-01-scaffold-dynamic-circuits/development/runs/panel-v7/artifacts/developmental-trajectory.svg)

*Figure 2. The verified developmental panel separates real training checkpoints from the shuffled-final diagnostic. The figure's custody record binds the analyzed summary and plotting source.*

At final, selected sites outperform wrong-label donors on 4/4 rows and fixed sites [0,4] on 3/4. The object row is a counter-trend: fixed sites shift the margin by 8.519 nats, versus 4.734 for selected sites. Mean normalized recovery is .874, with a relation ratio above one; this is not a causal share.

Native competence, raw effects, and profile agreement strengthen together across the broader trajectory. This supports a learned component beyond the fixed module layout in the tested organism. Early and shuffled native incompetence prevents their small effects from serving as behavior-level exclusion tests. The shuffled panel evaluates the final-frozen profile; it does not rerun discovery selection on shuffled discovery prompts.

The K/V intervention includes the current query inside the forward pass. It therefore measures learned task support, not isolated persistent-store mediation. Checkpoint files, tokenizer/configuration, and runtime versions are authenticated, but an independently expected native-output fingerprint after each hydration was not preregistered. A single model trajectory cannot establish universal developmental formation of the proposed scaffold. It also cannot date the Qwen organization measured in §6.5: Pythia's checkpoint curve and Qwen's final-weight correspondence intervention address different specimens and different questions.

## 12. Compilation and the scene generator

The architectural hypothesis would be useful if a role scaffold allowed a compiler to choose semantic support for a new context before seeing the desired target trajectory. The present experiments distinguish progress toward that goal from the goal itself.

Frozen address policies predict where donor state can be installed. In the selector assay, each held state assembly is sealed before evaluating its query and continuation. That supplies an outcome-free assembly precursor. The payload still comes from a native donor prefix, and semantic token positions are supplied. There is no learned mapping from a desired semantic change to a new payload, no compiler comparison against operation-blind or site-matched baselines, and no autonomous circuit induction.

Separate scene-generator records supply constructive results beyond the historical selector assembly precursor. The [packaged complete-source report](../../demos/artifacts/scene-generator/artifacts/reports/cross-model-replication.json) retains 21/21 exact native RGB endpoints across seven specimens and five family labels; requested prompts pass through native conditioning and projection before target rendering, without a target image or independent target trajectory as input. This is source-before-outcome execution, not a learned replacement semantic parser. [Held SDXL interaction programs](../../../saturn/experiments/2026-09-02-sdxl-centered-edge-basis-resolver-rosetta/FINDINGS-address-native-rgb.md) additionally predict bounded in-family conjunction payloads from development charts and supplied semantic row alignment. An unseen factor family leaves most of its interaction energy outside the fitted span. These records are developed in the [architectural synthesis](architectural-paper.md) and are not pooled into this campaign's sample count.

This campaign adds evidence that a single changed word need not contain the full relation payload and that carrier and live conditioning allocate different attributes at a given cut. A practical compiler should therefore keep source address, contextual payload, time, writer, and native consumer distinct.

If the broader architecture is established, it could support more reusable scene controls and semantic state programs. The current paper does not demonstrate a new general scene generator, cross-family tensor portability, inference speedup from circuit extraction, or replacement of dense native execution.

## 13. Execution and reproducibility

All real-model campaign and confirmation panels run through mrun on Beast's RTX 4080. The original thirteen authoritative successful jobs produce the historical thirteen-package ledger; the confirmation packets retain their own sealed jobs and are not folded into that count. Coding and auditing proceed in parallel; full accelerator panels are scheduled sequentially. Each finite panel has one outer lease and one resident model, with immutable parents reused across in-process causal branches [X1, C1–C4].

FLUX remains scalar BF16 to preserve the exact RGB/register authority of its assay. It reuses captured denoising checkpoints and duplicate payload branches rather than repeating common prefixes. Mamba batches same-shape arms under its qualified numerical contract. Qwen uses path-matched execution after full-sequence/split execution exposed BF16 differences. Pythia uses one model object with seven strict hydrations and 391 physical forwards.

Successful canonical scheduler times range from 11.39 to 135.04 seconds. They include scheduler execution overhead but exclude earlier failures and qualification attempts outside the authoritative ledger. These timings document execution economy. There is no matched baseline establishing a speedup or the fastest possible configuration. The separate FP32 Qwen study is excluded from this range and count.

A CUDA planner defect in one Qwen factorial reserved zero VRAM despite a CUDA requirement. The immutable job is retained, and subsequent launchers separate device, precision, and attention fields and use measured envelopes. Pythia qualification also exposed an attention-registry closure leak; the authoritative version unregisters closures in `finally`. Incorrect earlier null-parent lineages and killed runs remain unchanged. Corrections repair future execution and bound the accepted result; they do not rewrite historical failures.

The original campaign verifier checks source/report hashes, scheduler completion, declared mechanics, freeze lineage, corrections, and local custody. Its campaign-level root verification reports thirteen verified packages, zero errors, and zero pending entries [V1]. The confirmation lanes separately bind their frozen contracts, model bytes, source, reports, typed interventions, and reinstalls; the predictive verifier's 45 native-lane key collisions were audited as identical empty-patch physical parents with distinct execution outputs, not missing lanes. Raw terminal statuses remain unassessed. The prior-fixed Qwen study instead offers target-receipt custody, as described in §6.4.

Appendices provide the completed job ledger, evidence map, and tool-purpose map. Sharing or publication would require a deliberate public bundle and an independently runnable environment; neither is claimed by local verification.

## 14. Limitations and decisive next experiments

The Qwen packet establishes later semantic authority of independently manipulated model-formed state in a directed two-update path. Its complete held result is one of three contexts, with supplied queries and complete all-layer row donors. The result does not identify a unique/minimal writer, and it is mixed endogenous/host-supplied execution rather than an autonomous loop. The earlier selector packet remains disqualified as native causal evidence by its mask defect. Specifically route-produced L23 state in the corrected routing packet has not been independently mediated; that follow-up uses already-open contexts and therefore neither adds a fresh denominator nor rehabilitates the historical packet.

Diffusion uses one model, a four-step low-resolution schedule, few contexts and seeds, native target payloads, and limited visual review. Global RGB progress conflates semantic and collateral changes; the prospective cross-family review is blind at arm judgment but still only two rows. The relation scope diagnosis is post-hoc and broad. Transformer write bands are not unique; Mamba's original later-query semantic assay is unavailable; and the earned cross-family object contains only the formed-state/consumer edge. Pythia supplies one developmental trajectory and an in-forward rather than isolated-store intervention. The Qwen profile has eight correlated context combinations in one checkpoint, incomplete identity competence, no held size readout, and no acquisition timeline.

The historical proposals below now have the following statuses:

1. **Prospective role prediction: completed for a microscopic context holdout and partial cross-family core.** Relation beats three fixed competitors in 8/8 contexts; color is mixed and identity/size readout-limited. Prediction of a full formation/read/write graph in an unused checkpoint and task family remains open.
2. **Source/read/writer/store mediation: partially completed.** Source-to-formed-store block/rescue and serial second-row mediation are measured. The alias later-reference attention-output versus MLP-output writer cut and route-produced L23 future mediation remain distinct open experiments.
3. **Repeated recurrence: bounded semantic test completed.** Development plus one fresh held city/country context closes two updates. Broader/longer feedback and autonomous operation selection remain extensions.
4. **Learned scaffold discrimination: final-weight dependence measured, acquisition open.** Full L22/L23 value-projection disorder changes signed profiles. Pythia supplies a separate checkpoint trend; a Qwen same-assay learning timeline is still needed for chronology.
5. **Semantics and replication: blinded FLUX review and partial prospective comparisons completed.** Their attribute/continuation disagreements remain visible. Unused families/checkpoints and independent environments would extend confidence.
6. **Predictive compilation: bounded source and held-payload programs completed.** Exact full native prompt/IR source lowering and in-family held interactions are established separately. General automatic semantic address/payload synthesis remains open; the exact same-prompt crossed-state diffusion writer design has not been located.

These are discriminating experiments rather than a checklist whose failure would declare the mechanism absent. Each would certify only its declared scope. A unique shared architecture would require convergence among prospective role prediction, mediated recurrence, development, and replication.

## 15. Related work

**Causal abstraction.** Geiger et al. formalize alignment between neural variables and a higher-level causal model, tested using interchange interventions [Geiger 2021](https://arxiv.org/abs/2106.02997). This provides a natural basis for the role graph proposed here. The unresolved extension is a reusable recurrent mapping that predicts state-dependent semantic support across contexts and substrates.

**Reusable task representations.** In-context task vectors and causally identified function vectors provide precedents for internal representations that affect later task behavior [Hendel 2023](https://aclanthology.org/2023.findings-emnlp.624/), [Todd 2024](https://arxiv.org/abs/2310.15213). Our donor-state interventions overlap with this broader idea. The prior-fixed query contrasts show that the live operation changes the authority of byte-identical stored state, while the native serial packet shows later authority of a newly formed semantic row. Successful activation injection alone would establish neither relation.

**Circuit reuse and adaptation.** Merullo et al. show substantial component reuse between indirect-object identification and colored-object tasks, including intervention-predicted downstream effects [Merullo 2024](https://arxiv.org/abs/2310.08744). Nainani et al. show that a circuit can retain components and mechanisms while adding input edges across prompt variants [Nainani 2024](https://arxiv.org/abs/2411.16105). Reusable components and dynamic support are therefore established research directions. Our proposed role-level distinction must add prospective causal predictions, rather than claim novelty from reuse or changing activations alone.

**Circuit graphs and attention formation.** Transcoder analysis explicitly factors input-dependent and input-invariant circuit terms [Dunefsky 2024](https://papers.nips.cc/paper_files/paper/2024/hash/2b8f4db0464cc5b6e9d5e6bea4b9f308-Abstract-Conference.html). Circuit Tracing constructs replacement-model attribution graphs and discusses movement from prompt-local graphs toward global circuits [Ameisen 2025](https://www.transformer-circuits.pub/2025/attribution-graphs/methods.html). QK tracing explains attention scores through feature interactions [Kamath 2025](https://www.transformer-circuits.pub/2025/attention-qk/index.html). Our attention assay measures the causal change in a native read after a state intervention but does not identify feature interactions, participating heads, or the query-to-address algorithm. It addresses a coarser state boundary and does not claim the first static/dynamic circuit decomposition.

**Development.** Pythia makes training trajectories available for analysis across checkpoints [Biderman 2023](https://arxiv.org/abs/2304.01373). Tigges et al. track circuits across training and scale, finding recurring high-level algorithms despite changes in their physical implementation [Tigges 2024](https://papers.nips.cc/paper_files/paper/2024/hash/47c7edadfee365b394b2a3bd416048da-Abstract-Conference.html). Our small Pythia panel contributes a particular final-frozen intervention trajectory and shuffled-parent diagnostic. It is not the first developmental circuit study.

**Recurrent state and cross-architecture comparison.** Mamba supplies selective state-space computation [Gu and Dao 2023](https://arxiv.org/abs/2312.00752). Wang et al. compare Transformer/Mamba features and induction mechanisms [Wang 2024](https://arxiv.org/abs/2410.06672). Our family-local operands and proposed role abstraction sit within that existing cross-architecture research. The original post-hoc matcher does not establish universality; the later prospective packet earns only the smaller formed-state/consumer correspondence stated in §8.

**Diffusion control and circuit tracing.** Prompt-to-Prompt establishes attention-control editing [Hertz 2022](https://arxiv.org/abs/2208.01626). DifFRACT uses timestep-conditioned transcoders and feature attribution/interventions for diffusion circuit tracing [Mazur 2026](https://arxiv.org/abs/2606.15796). These precedents preclude a claim that this campaign first discovers temporal diffusion circuits or internal editing controls. The diffusion contribution here is prospective native-state address reuse, separation of conditioning from formed carrier at a cut, and a retained lexical-scope miss with a post-hoc contextual diagnosis.

**Temporal causal control.** The companion space-and-time paper separates formation, commitment, retention, and consumption and reports strict distributed-path instances at specific diffusion cuts [Hollenbeck 2026](../space-and-time-circuits/paper.md). This manuscript combines that distinction with operation-dependent consumption, frozen microscopic relation prediction, successive formed-state semantic effects, and developmental organization. The contribution is the combined causal record and its architectural formulation; broader operation transfer, a complete common role graph, and Qwen acquisition chronology remain extensions.

## 16. Conclusion

The completed experiments show reusable state interfaces with operation-dependent authority and recipient-native state formation. The strongest prospective result is a frozen relation profile that beats three alternatives in all eight unopened context combinations. The strongest recurrent result is a serial two-update path in development and one fresh competent held case: a native semantic prediction forms a new row whose isolated replacement changes the later answer. Full L22/L23 value-row disorder shows that the signed Qwen profile depends on final-checkpoint correspondence. Prospectively matched FLUX and Mamba interventions, plus a separately admitted competent Qwen row, earn a partial formed-state → native-consumer core while preserving visual, continuation, competence, and normalization disagreements.

These results support bounded scaffolded dynamic circuits, including a recurrent semantic member: reusable causal interfaces carry execution-specific semantic support, and newly formed state can govern a later native computation. A complete shared source/read/writer/feedback topology, Qwen learning chronology, broader feedback replication, autonomous operation selection, automatic addressing, and donor-free compilation remain open. These extensions do not serve as prerequisites for the inherited circuit-class foundation or the measured architectural instances. The [status audit](evidence-status-audit-2026-10-01.md) links the completed reports and the narrower experiments required for those stronger claims. Raw terminal statuses remain unassessed; the class-level interpretation is a working inference built from bounded causal results rather than a universal architecture certificate.

## Appendix A Experiment status

| ID | Question | Completed evidence | Evidence still needed |
|---|---|---|---|
| E1 | Do diffusion addresses and state roles recur? | Downstream held address/dose panel, conditioner×carrier factorial, upstream lexical panel, post-hoc relation diagnosis | Blinded semantic scoring, narrower contextual payloads, fuller source/store mediation |
| E2 | Do transformer formation, storage, and consumption separate? | Frozen role map, identity formed-store rescue, query×cache factorial, prospective relation profile, serial formed-row mediation | Broader operation transfer, unique writer localization, and longer continuation mediation |
| E3 | Do SSM state roles recur? | Two-size state-replacement/continuation panels; later-query diagnostic | Native-competent query organism and mediated read/write recurrence |
| E4 | Is the causal role graph shared across families? | Post-hoc matcher retained; prospective FLUX/Mamba formed-state/consumer profile plus later Qwen appendix | Full prospective source/read/writer/feedback graph on competent held rows |
| E5 | Does the hypothesis outperform architectural alternatives? | Timing/sign/donor/site controls; three frozen Qwen profile alternatives; graded and full L22/L23 value-row disorder | Broader behavior-matched architecture, energy, and site-degree comparisons; learning chronology |
| E6 | Can carried state change subsequent computation? | Historical selector packet retained under mask-defect qualification; native development plus one-of-three held serial two-update path | Broader competent domains, route-specific writer mediation, dose/order, and autonomous cycles |
| E7 | Does task-relevant organization develop? | Six Pythia checkpoints and final-parent shuffle | Multiple trajectories and discovery at each developmental stage |
| E8 | Does the result replicate? | Second-size Mamba and Qwen panels; thirteen-package local verifier; prospective partial FLUX/Mamba core and later Qwen comparison | Independent family, environment/laboratory, broader competent rows, and public release |
| E9 | Can dynamic support be compiled before outcomes? | Outcome-free held state assembly using donor activations | Learned compiler, held payload prediction, matched baselines and composition |
| E10 | Is a strict distributed-path subtype present? | No new exhaustive assay in this campaign | Optional singleton/joint necessity and sufficiency at one declared cut |

## Appendix B Sampling and execution

### Logical units and repeated measurements

| Module | Logical units | Dependence and competence limits |
|---|---|---|
| Diffusion downstream | Two discovery contrasts; five held prompt/seed contrasts | Arms and factorial cells share each parent |
| Diffusion lexical | Two disclosed discovery contrasts; four fresh held contrasts | Reuses discovery organisms; one relation miss |
| Relation diagnosis | One already opened relation | Zero fresh prospective or replication units |
| Qwen role map | 28 discovery prompts; 44 held prompts | Subject/template nesting; 2,764 arm rows are not independent samples |
| Qwen continuation | Eight fresh prompts, four identity and four color | Eighty arm rows and eight derived mediation summaries |
| Qwen query×cache | Two queries × four caches in one template family | Eight factorial cells, not eight independent specimens |
| Each Mamba size | Two discovery cells; three held cells | Shared templates; counting incompetent, capital continuation informative |
| Mamba later query | Four factorial cells | Zero paired-native-competent semantic units |
| Historical Qwen-0.5B feedback | One discovery organism; three held contexts | Recorded read/write effects and competence labels are mask-defective instrument observations |
| Feedback qualification | Previously opened endpoints | Adds zero scientific contexts |
| Historical Qwen-1.5B feedback | One discovery organism; three fresh held contexts | Recorded two competent contexts and place counterexample retained as mask-defective observations, not native task evidence |
| Pythia development | Three discovery prompts; four held prompts | Same four prompts repeated across six checkpoints and shuffled final |
| Separate Qwen context study | Four lexical scenes, one pilot and three transfers | 64 query rows and 1,024 branches are correlated; outside campaign ledger |
| Qwen frozen-profile confirmation | Eight context combinations: two lexical sets × two templates × two orders; two binding rows each | 128 panels and 4,736 lanes are repeated causal measurements; identity has four applicable contexts and size none under the frozen readout |
| Qwen serial feedback confirmation | One development organism; three held semantic domains | Complete semantic path in 1/3 held contexts; prompts, queries, donors, and branch choices are host supplied |
| Prospective FLUX/Mamba common profile | Two held rows per family | Four coordinates are a profile dimension, not four samples; local visual and continuation outcomes qualify scalar scores |
| Later Qwen comparative appendix | Three held rows; one paired-native-competent row | Competent pairwise comparison n=1; all-row normalization reverses profile agreement |

The Qwen role map's held native top-choice competence is 6/14 for identity and 4/10, 0/10, and 8/10 across the three color templates. These native outcomes remain separate from writer-effect measurements. The campaign has no pooled independent sample count.

### Successful job ledger

| Panel | Authoritative mrun job | Canonical scheduler seconds |
|---|---|---:|
| Diffusion addresses and parents | `job-8fea57981191` | 135.04 |
| Diffusion lexical text | `job-def6cf9f980e` | 116.65 |
| Diffusion relation scope | `job-c00fc5cdc60a` | 43.10 |
| Qwen role map | `job-02e83e9ae183` | 15.51 |
| Qwen formed-store continuation | `job-24d2a7164160` | 11.42 |
| Qwen query×cache factorial | `job-6a96dadc2701` | 11.39 |
| Qwen-0.5B selector feedback | `job-dade0194f43a` | 11.40 |
| Feedback mechanics qualification | `job-3626c2a1b385` | 12.46 |
| Qwen-1.5B selector feedback | `job-01c81b3f5029` | 14.47 |
| Mamba-130M | `job-2bde6a0f47c7` | 20.60 |
| Mamba-370M | `job-ee475fa35dee` | 35.94 |
| Mamba later query | `job-44ac3efae7bf` | 18.53 |
| Pythia development | `job-4e053261e196` | 15.50 |

The ledger counts jobs and packages, not thirteen independent scientific replications. One row is mechanics reproduction. The successful canonical times sum to 462.01 seconds, or 7.70 minutes, excluding failed and superseded attempts. Local verification checks 308 mechanics/custody conditions across 556 evidence rows; these rows are derived measurements rather than independent specimens. Resource peaks and future measured envelopes are documented in [execution notes](../../../saturn/experiments/2026-10-01-scaffold-dynamic-circuits/EXECUTION.md).

The confirmation work has a separate lane-local ledger rather than being retroactively counted as additional historical campaign packages. Its authoritative entries are the frozen-profile held job `job-20ede7e6e0c0`, the full-disorder follow-up `job-c6a7ade0e793`, the development query calibration `job-0c3f8540b101`, the combined serial-feedback holdout `job-1a141a746afa`, and the sealed FLUX/Mamba and admitted Qwen comparative packets linked below. Raw reports preserve their original terminal labels; no aggregate certification status is assigned here.

## Appendix C Evidence and references

### Campaign records

- **D1:** [Diffusion verified summary](../../../saturn/experiments/2026-10-01-scaffold-dynamic-circuits/diffusion/runs/panel-v1/summary.json), [AI visual observations](../../../saturn/experiments/2026-10-01-scaffold-dynamic-circuits/diffusion/runs/panel-v1/artifacts/semantic-review-ai.json), and [contact sheet](../../../saturn/experiments/2026-10-01-scaffold-dynamic-circuits/diffusion/runs/panel-v1/artifacts/contact-sheet-held-overview.png).
- **D2:** [Upstream findings](../../../saturn/experiments/2026-10-01-scaffold-dynamic-circuits/diffusion-text/FINDINGS.md), [verified summary](../../../saturn/experiments/2026-10-01-scaffold-dynamic-circuits/diffusion-text/runs/panel-v3/summary.json), and [AI visual observations](../../../saturn/experiments/2026-10-01-scaffold-dynamic-circuits/diffusion-text/runs/panel-v3/artifacts/semantic-review-ai.json).
- **D3:** [Relation scope findings](../../../saturn/experiments/2026-10-01-scaffold-dynamic-circuits/diffusion-text/RELATION_FINDINGS.md), [summary](../../../saturn/experiments/2026-10-01-scaffold-dynamic-circuits/diffusion-text/runs/relation-posthoc-v1/summary.json), and [scope images](../../../saturn/experiments/2026-10-01-scaffold-dynamic-circuits/diffusion-text/runs/relation-posthoc-v1/artifacts/contact-sheet-relation-scopes.png).
- **T1:** [Qwen role findings](../../../saturn/experiments/2026-10-01-scaffold-dynamic-circuits/ar/FINDINGS.md).
- **T2:** [Formed-store and continuation findings](../../../saturn/experiments/2026-10-01-scaffold-dynamic-circuits/ar/CONTINUATION_FINDINGS.md).
- **T3:** [Actual query factorial](../../../saturn/experiments/2026-10-01-scaffold-dynamic-circuits/ar/QUERY_FACTORIAL_FINDINGS.md).
- **F1:** [Selector feedback findings](../../../saturn/experiments/2026-10-01-scaffold-dynamic-circuits/ar-feedback/FINDINGS.md) and [0.5B raw report](../../../saturn/experiments/2026-10-01-scaffold-dynamic-circuits/ar-feedback/results/run-dade0194f43a/report.json).
- **F2:** [Instrumented qualification report](../../../saturn/experiments/2026-10-01-scaffold-dynamic-circuits/ar-feedback/results/run-3626c2a1b385/report.json).
- **F3:** [1.5B raw feedback report](../../../saturn/experiments/2026-10-01-scaffold-dynamic-circuits/ar-feedback/results-qwen15/run-01c81b3f5029/report.json).
- **S1–S3:** [Mamba findings and job sources](../../../saturn/experiments/2026-10-01-scaffold-dynamic-circuits/ssm/FINDINGS.md).
- **A1:** [Post-hoc alignment](../../../saturn/experiments/2026-10-01-scaffold-dynamic-circuits/ssm/E4_ALIGNMENT.md) and [additive interpretation](../../../saturn/experiments/2026-10-01-scaffold-dynamic-circuits/ssm/E4_FOLLOWUP.md).
- **P1:** [Development protocol](../../../saturn/experiments/2026-10-01-scaffold-dynamic-circuits/development/README.md), [verified summary](../../../saturn/experiments/2026-10-01-scaffold-dynamic-circuits/development/runs/panel-v7/summary.json), and [figure custody](../../../saturn/experiments/2026-10-01-scaffold-dynamic-circuits/development/runs/panel-v7/artifacts/developmental-trajectory-custody.json).
- **X1:** [Execution notes](../../../saturn/experiments/2026-10-01-scaffold-dynamic-circuits/EXECUTION.md), [shared protocol](../../../saturn/experiments/2026-10-01-scaffold-dynamic-circuits/PROTOCOL.md), and [results synthesis](../../../saturn/experiments/2026-10-01-scaffold-dynamic-circuits/RESULTS.md).
- **V1:** [Campaign index](../../../saturn/experiments/2026-10-01-scaffold-dynamic-circuits/campaign/RUN_INDEX.json), [verifier](../../../saturn/experiments/2026-10-01-scaffold-dynamic-circuits/campaign/verify.py), and [separate campaign-level root receipt](../../../saturn/experiments/2026-10-01-scaffold-dynamic-circuits/campaign/root-verification-receipt.json).

### Separate contemporaneous evidence

- **Q1:** [Qwen context proof-of-concept findings](../../../saturn/experiments/2026-10-01-qwen-scaffold-context-poc/FINDINGS.md) and [raw aggregate](../../../saturn/experiments/2026-10-01-qwen-scaffold-context-poc/analysis/analysis.json). Separate FP32 runtime and job ledger; receipt-level activation custody.

### Confirmation records

- **C0:** [Integrated confirmation findings](../../../saturn/experiments/2026-10-01-scaffold-confirmation/FINDINGS.md) and [receipt-linked status audit](evidence-status-audit-2026-10-01.md).
- **C1:** [Frozen Qwen profile and weight-correspondence findings](../../../saturn/experiments/2026-10-01-scaffold-confirmation/qwen-predictive/FINDINGS.md).
- **C2:** [Native successive formed-row feedback findings](../../../saturn/experiments/2026-10-01-scaffold-confirmation/qwen-feedback/FINDINGS.md) and [held report](../../../saturn/experiments/2026-10-01-scaffold-confirmation/qwen-feedback/results/held-combined-1a141a746afa/report.json).
- **C3:** [Prospective FLUX/Mamba common-profile findings](../../../saturn/experiments/2026-10-01-scaffold-confirmation/cross-family/FINDINGS.md).
- **C4:** [Later prospective Qwen appendix](../../../saturn/experiments/2026-10-01-scaffold-confirmation/cross-family/qwen-appendix/FINDINGS.md).
- **C5:** [Corrected native routing mediation](../../../saturn/experiments/2026-10-01-qwen-routing-mediation/FINDINGS.md). Already-open contexts; no new held denominator and no rehabilitation of F1–F3.

### Primary literature

- **Geiger 2021:** Atticus Geiger, Hanson Lu, Thomas Icard, and Christopher Potts. [Causal Abstractions of Neural Networks](https://arxiv.org/abs/2106.02997).
- **Todd 2024:** Eric Todd, Millicent L. Li, Arnab Sen Sharma, Aaron Mueller, Byron C. Wallace, and David Bau. [Function Vectors in Large Language Models](https://arxiv.org/abs/2310.15213). ICLR 2024; preprint 2023.
- **Hendel 2023:** Roee Hendel, Mor Geva, and Amir Globerson. [In-Context Learning Creates Task Vectors](https://aclanthology.org/2023.findings-emnlp.624/). Findings of EMNLP.
- **Merullo 2024:** Jack Merullo, Carsten Eickhoff, and Ellie Pavlick. [Circuit Component Reuse Across Tasks in Transformer Language Models](https://arxiv.org/abs/2310.08744). ICLR 2024; preprint 2023.
- **Nainani 2024:** Jatin Nainani et al. [Adaptive Circuit Behavior and Generalization in Mechanistic Interpretability](https://arxiv.org/abs/2411.16105). Preprint.
- **Dunefsky 2024:** Jacob Dunefsky, Philippe Chlenski, and Neel Nanda. [Transcoders Find Interpretable LLM Feature Circuits](https://papers.nips.cc/paper_files/paper/2024/hash/2b8f4db0464cc5b6e9d5e6bea4b9f308-Abstract-Conference.html). NeurIPS.
- **Ameisen 2025:** Emmanuel Ameisen et al. [Circuit Tracing: Revealing Computational Graphs in Language Models](https://www.transformer-circuits.pub/2025/attribution-graphs/methods.html).
- **Kamath 2025:** Harish Kamath et al. [Tracing Attention Computation Through Feature Interactions](https://www.transformer-circuits.pub/2025/attention-qk/index.html).
- **Biderman 2023:** Stella Biderman et al. [Pythia: A Suite for Analyzing Large Language Models Across Training and Scaling](https://arxiv.org/abs/2304.01373).
- **Tigges 2024:** Curt Tigges, Michael Hanna, Qinan Yu, and Stella Biderman. [LLM Circuit Analyses Are Consistent Across Training and Scale](https://papers.nips.cc/paper_files/paper/2024/hash/47c7edadfee365b394b2a3bd416048da-Abstract-Conference.html). NeurIPS.
- **Gu and Dao 2023:** Albert Gu and Tri Dao. [Mamba: Linear-Time Sequence Modeling with Selective State Spaces](https://arxiv.org/abs/2312.00752).
- **Wang 2024:** Junxuan Wang et al. [Towards Universality: Studying Mechanistic Similarity Across Language Model Architectures](https://arxiv.org/abs/2410.06672). Preprint.
- **Hertz 2022:** Amir Hertz et al. [Prompt-to-Prompt Image Editing with Cross Attention Control](https://arxiv.org/abs/2208.01626). Preprint 2022; ICLR 2023.
- **Mazur 2026:** Artyom Mazur, Nina Konovalova, and Aibek Alanov. [DifFRACT: Diffusion Feature Reconstruction and Attribution for Circuit Tracing](https://arxiv.org/abs/2606.15796). Preprint.
- **Hollenbeck 2026:** Jacob Hollenbeck. [Space and Time Circuits: Causal Control Across Model Trajectories](../space-and-time-circuits/paper.md). Workspace manuscript, October 1, 2026.

## Appendix D Tools and their purposes

| Tool or boundary | Purpose | Use and authority in this manuscript |
|---|---|---|
| Saturn typed cuts, Frames, Acts, StateCuts, and intervention hooks | Name state boundaries, install interventions, preserve lineage, and resume native execution | Direct diffusion replay and sealed family-local equivalents; mechanics do not identify semantic roles by themselves |
| mrun | Acquire/place models, guard CUDA resources, schedule finite leases, collect telemetry and custody | Every real-model campaign panel; execution success does not certify the hypothesis |
| `mrun.diffusion.PhasePipeline` | Capture and resume immutable denoising checkpoints through scheduler and VAE | Diffusion panels; native replay preserves the declared numerical consumer |
| Recorder | Capture activations, state, addresses, and trajectories | Prior-tool vocabulary and lane-local capture equivalents; observations nominate causal tests |
| Winder | Replay or transplant state under controlled continuation | Prior-tool vocabulary and family-local equivalents; effects are scoped to their cut |
| Decoder | Read represented variables or decoded output from state | Native VAE/RGB is primary here; learned probe or decoder scores would not replace consumer evidence |
| MRI and subspace/fingerprint instruments | Localize candidate support and compare trajectories or representations | Supporting/prior instruments; not separate causal authorities in this campaign |
| Generative typed-mechanism analysis | Propose mechanisms and typed causal hypotheses | Prior/supporting machinery; generated explanations require interventions |
| Native scheduler, VAE, LM head, and greedy continuation | Consume the intervened state and expose images, logits, and generated tokens | Direct outcome authority, with competence and collateral interpreted separately |
| `saturn-evidence` watch, claims, and xref | Emit linked observations, detect instrument anomalies, and bind claims to evidence | Offline evidence processing; zero fires or valid linkage is not a semantic pass |
| Source and payload custody | Preserve hashes, source identity, tensor payload linkage, and correction history | Local campaign evidence; separate Qwen study has the weaker receipt-level scope described in §6.4 |
| QStore checkpoint records | Authenticate immutable model checkpoint bytes | Pythia source identity; the HF FP32 runtime is the causal consumer |
| Local analyzers and campaign verifier | Reconstruct policies, validate mechanics/custody, preserve per-row metrics | Thirteen-package local verification; no aggregate scientific or publication verdict |
| Contact sheets and visual review | Inspect target attributes, composition, and collateral in native images | Original diffusion panels use unblinded AI observations; the separate cross-family packet records fixed-seed arm-anonymous judgments before unblinding |
| Role matcher and frozen profile/null controls | Compare family-local causal profiles and alternatives | Original matcher is post-hoc and nearly tied its null; later FLUX/Mamba profile is prospective but earns only the formed-state/consumer edge |
| `TokenMachine`, fused layer execution, and decomposed observer | Advance one native token step, capture complete formed rows, and observe the declared L22 read boundary | Native semantic authority is fused TokenMachine execution; exact decomposed parity holds at capture and is not a claim of monolithic parity on every cycle |
| Thott | Read K/V in terms of positional clock, address, and contextual state | Predecessor reference; not a distinct campaign instrument |
| `CausalContextVM` and `CircuitRuntime` | Execute reusable native state transactions and continuation | Prior runtime motivation; no new VM performance claim in this campaign |
| SAELens, Gemma Scope, and transcoders | Supply sparse-feature and replacement-model comparison instruments | Prior/related instruments; not used in the thirteen campaign panels |
