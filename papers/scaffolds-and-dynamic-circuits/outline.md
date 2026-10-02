---
title: "Scaffolds and Dynamic Circuits"
subtitle: "Reusable causal interfaces and context-dependent computation in Qwen, with comparisons to diffusion and state-space models"
type: research-paper
status: outline-draft
date: 2026-10-01
updated: 2026-10-01T17:12:25-07:00
author: Jacob Hollenbeck
companion_to:
  - ../space-and-time-circuits/paper.md
  - ./bridge-paper.md
builds_on:
  - ../../../saturn/docs/ROLE-PORTABILITY-ABI.md
  - ../../../saturn/docs/ROSETTA-CIRCUIT-EXPLORER-PROPOSAL.md
  - ../../../saturn/experiments/2026-08-29-rosetta-circuit-explorer/README.md
  - ../../../saturn/experiments/2026-09-02-scene-compiler-portability-audit/FINDINGS.md
  - ../../../saturn/experiments/2026-10-01-qwen-scaffold-context-poc/FINDINGS.md
  - ../../../saturn/experiments/2026-10-01-qwen-formation-replay/FINDINGS.md
  - ../../../saturn/experiments/2026-10-01-qwen-formation-replay/VM_CAPABILITIES.md
  - ../../../saturn/experiments/2026-10-01-qwen-head-edge-topology/FINDINGS.md
  - ../../../saturn/experiments/2026-10-01-scaffold-confirmation/FINDINGS.md
tags: [interpretability, causal-circuits, dynamic-circuits, diffusion, autoregressive-models, state-space-models, role-invariance]
---

# Scaffolds and Dynamic Circuits

> **How to use this outline.** This is the outline for a bounded architecture paper and a broader research program. Each section separates collected results, working inferences, and experiments needed only for stronger claims. The draft must not convert a proposed experiment into a result.
>
> - **TODO [E#]** is a prospective experiment. Appendix A fixes the experiment IDs and required evidence.
> - **TODO [R#]** is an evidence audit, collation, or correction using existing records only.
> - **TODO [W]** is writing or figure work.
>
> The first prospective wave is `E1` diffusion, `E2` autoregressive transformer, and `E3` state-space model under `saturn/experiments/2026-10-01-scaffold-dynamic-circuits/`. Its shared contract is [`PROTOCOL.md`](../../../saturn/experiments/2026-10-01-scaffold-dynamic-circuits/PROTOCOL.md).
>
> `../space-and-time-circuits/paper.md` is the current scientific record for the predecessor story. Its updated mixed findings supersede several terminal-sounding statements in the original `space-and-time-circuits/outline.md`. In particular, a strict four-quadrant circuit occurs in some diffusion cuts but is not the criterion for the architecture proposed here.
>
> The space–time circuit-class foundation is inherited from that paper. This outline asks what reusable organization can be built from those circuits; it does not make the class depend on proving a universal architecture, autonomous feedback, or a compiler.

---

## Abstract and current claim

**Bounded result.** In frozen Qwen2.5-1.5B, a late K/V interface fixed by prior work causally supports identity, color, and spatial-relation operations across four lexical scenes. Changing the native query changes the causal authority of byte-identical stored state. A subsequent microscopic packet finds two recurring value routes and both grouped-query reader groups, with stable binding-relative profiles and different operation weights. Earlier source-residual seeding induces recipient-native late state that can independently rescue the answer; this formation path also works for Python return-value retrieval, with copying and aliasing exposing collateral and binding limits.

These results support a reusable **functional interface with dynamic causal support**. The invariant is a measured state/reader/consumer organization; the dynamic part is which source is read and how strongly each route contributes under a particular operation. A subsequent discovery-frozen 24-coordinate profile predicts unopened spatial-relation effects better than three fixed alternatives in all eight context combinations. Color transfer is partial and its reader-order prediction misses; identity and size expose registered-readout limits. A conventional attention lookup can implement this organization. Establishing causal reuse does not require inventing a new neural module.

The broader **scaffold hypothesis** connects source, current operation/address, transition, writer, carried state, and native consumer. A new Qwen packet closes a directed two-update semantic path in development and one fresh competent city/country holdout: the first formed state changes the next native prediction; replacing only that prediction's newly formed state, with its visible token fixed, changes the later semantic answer. Two other held contexts remain semantically unavailable. Prospectively comparable FLUX/Mamba assays and a later Qwen appendix support a partial formed-state→native-consumer core, with explicit attribute and competence limits. They do not establish one complete cross-family graph. Pythia supplies a developmental trend; strong Qwen value-projection disorder changes the signed profile, while chronological acquisition of this organization remains open.

**Current status.** The bounded Qwen architecture result can be written from collected evidence now. Its coalition interface was fixed before transfer scenes; its detailed discovery head map and coding/copy/alias successors are exploratory, while the later profile and feedback packets have their own prospective seals and held splits. Historical terminal labels remain unchanged. The older E6 attention wrapper has a documented causal-mask defect; its routing/competence/continuation effects are qualified historical instrument observations, not native causal evidence. The current feedback packet uses a different native token runtime and names its authority explicitly. Complete mediation for every operation or family, a universal graph, unique minimal heads, autonomous loops, donor-free compilation, and production virtual memory are not prerequisites for this paper's bounded result.

**Headline evidence.** [Fixed-interface and same-patch/query contrasts](../../../saturn/experiments/2026-10-01-qwen-scaffold-context-poc/FINDINGS.md) · [microscopic reader graph](../../../saturn/experiments/2026-10-01-qwen-head-edge-topology/FINDINGS.md) · [formation and replay](../../../saturn/experiments/2026-10-01-qwen-formation-replay/FINDINGS.md) · [companion draft](bridge-paper.md) · [blog](../../../obsidian/blog/2026-10-01-141628-the-question-decided-which-stored-fact-mattered.md).

**New confirmation campaign.** [Integrated findings](../../../saturn/experiments/2026-10-01-scaffold-confirmation/FINDINGS.md) · [frozen-profile predictions and weight disorder](../../../saturn/experiments/2026-10-01-scaffold-confirmation/qwen-predictive/FINDINGS.md) · [successive written-state feedback](../../../saturn/experiments/2026-10-01-scaffold-confirmation/qwen-feedback/FINDINGS.md) · [prospective FLUX/Mamba core](../../../saturn/experiments/2026-10-01-scaffold-confirmation/cross-family/FINDINGS.md) · [later Qwen appendix](../../../saturn/experiments/2026-10-01-scaffold-confirmation/cross-family/qwen-appendix/FINDINGS.md).

**New blog.** [The written state changed the next answer](../../../obsidian/blog/2026-10-01-170249-the-written-state-changed-the-next-answer.md) explains the prediction, serial-state intervention, weight comparison, and shared-core implications with links back to this outline and the related architectural posts.

## 0. What is established and what remains

| Proposition | Current evidence and scope | Claim level |
|---|---|---|
| Space–time circuits provide the foundation | Predecessor paper's source/formation/store/consumer results and bounded path-distributed subtype | Inherited circuit-class foundation; universal architecture is a separate question |
| One fixed state interface supports several operations | Prior-fixed Qwen L22–27 across four lexical scenes; donor color 16/16, position 12/16, identity 11/11 available with five unavailable | Bounded causal result |
| Current operation changes which stored fact matters | Same parent and patch bytes, different native query; positive selective harm on 16/16 color and 16/16 position contrasts, medians 3.1305 and .5829 nats | Bounded causal result; directly answers context-dependent consumption |
| Shared reader routes carry different operation weights | Discovery L23/KV0/V and L22/KV1/V; both six-head GQA groups participate. Frozen relation profile beats three comparators in 8/8 new context combinations; color reader ranking misses | Bounded discovery plus prospective relation recurrence; no universal operation-specific map |
| Earlier source becomes independently causal carried state | Identity residual → recipient-formed late K/V → independent rescue/block; native formation also works for Python return-value retrieval | Bounded formation chain; supplied source/address, neither automatic addressing nor arithmetic computation |
| Successive written state affects later semantic answers | Native development color chain and one fresh city/country holdout; second-row block/swap/reinstall with first state and visible second token fixed | Bounded directed two-update path; 1/3 held contexts complete, host supplies queries; older E6 remains mask-qualified |
| Comparable responsibilities recur across substrates | Prospectively frozen FLUX/Mamba state/consumer profiles, n=2 each, plus later Qwen appendix n=1 competent of 3 | Prospective partial core; full shared role graph remains open |
| Final-checkpoint L22/L23 `v_proj` row correspondence supports this profile | Mild Qwen disruption mostly preserves it; full row permutation of those two value projections collapses signed shape, with competence losses | Bounded final-weight dependence; learning-time acquisition remains open; Pythia is a separate developmental trend |
| State can be persisted, edited, and consumed again | Native residual/Thott/paged-KV/debugger tests; fresh-lease clean and edited numerical replay | Executable-memory mechanics, separate from semantic architecture evidence |

**What can be written now.** A bounded architecture account of reusable state interfaces, context-dependent causal participation, shared readers with different weights, and recipient-native formation. No additional model run is necessary to report those collected results with their stated scope.

**The next discriminating tests have now run.** The frozen-profile test supports relation most clearly, color partially, and identity ambiguously under its registered consumer; size remains readout-unavailable. Strong value-projection disorder supplies a same-surface final-weight comparison, not a training timeline. The two-update packet closes one fresh competent semantic path. Cross-family alignment earns a partial state/consumer core, rather than the entire proposed role graph. See §6, §8, §9, and §11.1 for the positive results and counter-trends.

**Extensions with their own evidence obligations.** Broader semantic feedback needs additional competent contexts and longer update chains. A complete common diffusion/transformer/SSM graph needs prospective alignment of currently unmatched source/read/write/feedback roles. Learning-time acquisition needs a suitable same-assay checkpoint comparison. Automatic semantic addressing, a general learned semantic compiler, minimality, independent-lab replication, and production-memory claims each have separate obligations. Existing exact native-source compilation and bounded in-family payload prediction are completed results, rather than compiler absence. None should be bundled into a gate for the bounded result above.

**Run/data audit.** The [receipt-linked status audit](evidence-status-audit-2026-10-01.md) confirms that frozen-context prediction, bounded two-update mediation, final-weight disorder, and a prospective partial cross-family core have completed. The cross-family manifest explicitly reuses studied checkpoints and operation families while holding out exact prompts/seeds. A previously unused checkpoint **and** task family, with frozen formation-site/consumption-site/null-profile predictions, remains a stronger combined test. That narrower extension must not be described as if the completed prospective tests never ran.

## 1. The proposed object

### 1.1 Functional scaffold

**Claim.** A functional scaffold is a reusable, intervention-supported organization of causal roles. Learning origin, temporal feedback, and cross-family alignment are stronger properties to test separately.

Let a family-local execution expose candidate sites \(V_m\) and causal relations \(E_m\). A scaffold hypothesis is a role graph

\[
G^*=(R,E^*), \qquad
R=\{\text{source},\text{current operation/address},\text{reader/live read},\text{transition/carrier},\text{writer},\text{carried state},\text{native consumer}\},
\]

together with a family-local lowering \(L_m:R\rightarrow V_m\). This paper separates the current operation/address from the live reader explicitly; the earlier six-role ABI can combine those responsibilities. The role names earn content through signed interventions at the declared cut. Source and store lesions plus downstream rescue are required to call a node a mediator; a bounded replacement or write assay can establish only the narrower causal role it actually tests. A role label inferred from tensor shape, architecture documentation, or causal order alone is a hypothesis, not a finding.

The base object is reusable across examples and operations. Its measured core can be a source→formed-state→reader→consumer chain. A feedback extension proposes that carried state at step \(t-1\) helps determine the next live read, whose writer commits state for a later update:

```text
semantic source + current operation
                 |
                 v
carried state_(t-1) -> live address / transition read -> semantic writer
                                                            |
                                                            v
              unchanged native consumer <----------- carried state_t
                                                            |
                                                            +----> next live address / transition read
                                                                   (feedback extension)
```

The **static role scaffold** is the recurring organization of possible causal roles at a declared resolution. The **dynamic semantic support** is the input- and state-dependent selection and weighting of sources, reads, writers, doses, times, and sites on one execution. The physical module graph supplies the substrate; interventions identify the functional organization on it. The bounded Qwen record identifies a reusable causal interface and portions of that role graph. It does not yet identify every internal edge or a unique writer.

**Case recurrence** is reuse of causal responsibilities across examples or operations; prospective confirmation freezes the profile before testing unopened cases. **Temporal feedback** means updated state causally changes a later read and write. The first does not imply the second. **Learned functional organization beyond a generic architectural bottleneck** requires a claim-matched prospective discriminator (§9); it does not require every conceivable null to pass. Ordinary attention is a compatible implementation, and learning-time acquisition is distinct from inference-time formation of contextual state. The inherited space–time circuit class does not depend on these architectural extensions.

**Existing support.** The Saturn role-portability ABI already names six roles and forbids tensor equivalence. More directly, FLUX format×ontology and cross-prompt panels find a recurring interior text spine and late image handoff while lexical addresses and temporal weights change. Object×scene factorials in FLUX.2 and Krea separate prospective semantic main effects from target-assisted exact interaction rescue and expose a possible reusable scene-composition correction. Scene-compiler audits argue for a source → binding → writer → register → decoder role graph across several diffusion families. The 206-node / 305-edge object recurring across three seeds records the physical execution substrate, but it is passive and cannot identify a learned functional scaffold by itself.

**Collected role evidence.** Qwen identifies the source at layer resolution, recipient-native identity formation, the late carried K/V interface, query-dependent consumption, and two recurring microscopic value coordinates. GQA-group causal rescue resolves reader participation at group resolution. The fixed coalition transfers to lexical scenes; the later frozen relation profile predicts new context combinations, with heterogeneous color/identity transfer. Whole newly formed rows close the bounded two-update feedback edge at all-layer row resolution. The passive 206-node diffusion object still supplies only physical structure.

- **E1–E3 collected bounded modules; E4 partially extended prospectively:** the original matcher remains post-hoc. The new campaign independently freezes a smaller state/consumer profile for FLUX/Mamba, with a later prospective Qwen comparison. Unmatched roles keep the complete graph open.
- **R1 bounded audit completed:** the claim ledger above and §6 distinguish measured roles from the open unique writer, individual query-head necessity, complete microscopic formation edges, and inferred family-neutral roles. Extend this inventory when new evidence is added.

### 1.2 Dynamic semantic causal subcircuit

**Claim.** A dynamic subcircuit is the context- and operation-specific causal support loaded onto a scaffold during execution.

For input context \(c\), current operation \(o_t\), and carried state \(s_{t-1}\), define a dynamic record

\[
D_{m,c,o,t}=\big(A,P,\alpha,\tau,M\big),
\]

where \(A\) is the source/address selection, \(P\) the semantic payload, \(\alpha\) dose or gain, \(\tau\) timing/order, and \(M\subseteq V_m\) the causally supported family-local sites. The record is semantic only to the extent that same-parent interventions produce directed effects through the unchanged native consumer.

Dynamic does not mean that weights change online. It means that the causal support used for one computation varies with the live input and history while remaining organized by a reusable role graph. Physical site reuse, activation variation, low-rank geometry, or exact replay alone is insufficient.

**Existing support.** FLUX `DynamicCircuitRecord` artifacts keep prompt/seed-specific sources and payloads distinct from the skeleton. The full-scene compiler observes static prompt source with depth×time-varying internal hashes. The Qwen dynamic-circuit assay preserves signed local effects and reports terminal status as `not_assessed`. Its development shared schedule captures only about 5–10% of per-cell delta energy and its leave-one-cell-out schedule similarity is heterogeneous, which is evidence against equating one clock with the entire dynamic program.

**New bounded result.** The prior-fixed Qwen L22–27 interface transfers across four lexical scenes and multiple operations. Byte-identical stored interventions become selectively consequential under different native queries. The microscopic discovery finds binding-relative recurrence and graded operation-specific weights in shared value routes. The subsequent frozen profile predicts relation on unopened context combinations, while color's reader ranking fails. Together these identify dynamic causal participation on a reused interface; they do not establish invariant detailed weights for every semantic operation.

- **E1–E3 collection status:** immutable per-row source/site/state, control, continuation, and native-endpoint records are retained for the components each lane implemented. Complete mediation and several shared-profile fields remain explicitly unmeasured.
- **TODO [W]:** show dynamic overlays on one role graph without implying that the entire graph fires for every input.

### 1.3 Current operation and carried state

**Claim.** Native output depends on the interaction of the current operation with state carried from prior execution.

The minimal assay crosses operation and state from matched same-parent rows:

| | native carried state | counterfactual carried state |
|---|---|---|
| native current operation | native continuation | state-only counterfactual |
| counterfactual current operation | operation-only counterfactual | joint counterfactual |

The evidence is the full signed 2×2 response, including interactions and rows where one factor dominates. A conjunction is a possible result, not a gate. Source-to-store mediation then asks whether carried state lies on the causal path from source/current operation to the native endpoint.

**Existing support.** Qwen E20 reports a bounded source-to-late-store mediation result in one identity organism. Mamba transition records show that the same recurrent payload can reach different continuation basins when the convolution operand or runtime changes. Coding mediation shows a frozen suffix consumer changing behavior under an incoming-state transplant. These are useful precedents with different cuts and limitations.

**Collected Qwen operation×state result.** The Qwen1.5 same-patch/query panel holds the parent and donor K/V bytes fixed while changing the native question. The differential state effect is positive on 16/16 color and 16/16 position contrasts. This establishes context-dependent consumption in that specimen. A numerically identical effect, conjunction, or complete mediation for every operation is not required. The three architecture lanes have not run a prospectively aligned version of this assay.

- **E1 completed module:** the cut-two suffix-conditioner × formed-latent factorial is retained as a two-parent causal contrast, not unique endogenous source→store mediation.
- **E2 completed module:** retain the finite residual/K/V role map and the bounded identity source → endogenous L20 K/V → eight-token continuation chain. Report its 4/4 answer rescue, 2/4 continuation-match improvement, and weak color transfer separately; do not generalize the identity result to every operation.
- **E3 completed module:** convolution-only, recurrent-only, and joint-state profiles plus native continuation are retained. The downstream write assay does not identify an upstream mediator.
- **E6 historical modules and correction:** the original custom attention wrapper lacked its matching causal-mask registration. Its measured route/write effects and native-competence labels remain historical instrument observations. The corrected routing follow-up supplies native-qualified single-row effects on already-open contexts, with effective fresh n=0. The new feedback packet separately closes successive formed-row semantic authority in development and one fresh competent holdout (§11.1); it does not rehabilitate the old wrapper.

## 2. What would be new

**Claim.** The contribution is discovered role invariance plus semantic causal support, not the generic fixed-weights/dynamic-activation distinction.

The paper must keep these levels separate:

| Level | What it says | Why it is insufficient by itself |
|---|---|---|
| Architecture graph | Modules and state interfaces recur by construction | It can be written down without data or learning |
| Fixed weights, dynamic activations | Inputs produce different activations under one checkpoint | True of almost every neural network |
| Recurring physical sites | Similar layers/steps have high energy or intervention effects | May reflect depth, scale, or generic bottlenecks |
| Reusable causal interface | A prior-fixed interface has native causal authority on new contents or operations | Establishes bounded reuse; it need not identify every internal role |
| Mediated role graph | A source changes recipient-formed state whose block/rescue changes the native endpoint | Requires formation, block, and independent rescue at the claimed edges |
| Predictive functional scaffold | A frozen role profile predicts held effects beyond claim-matched generic-site explanations | Collected most clearly for relation; operation-specific transfer remains heterogeneous |
| Learned organization | The functional profile depends on trained weight correspondence and is acquired during learning | Final-weight disorder supports dependence; chronology needs a suitable checkpoint comparison |
| Dynamic semantic subcircuit | Input-specific support on the scaffold directs an unchanged native consumer | Requires semantic counterfactuals and per-row native endpoints |
| Cross-architecture role graph | Family-local lowerings instantiate an aligned role topology | Requires within-family evidence first and forbids tensor equivalence |

The contribution builds on the predecessor circuit class: the same formed interface can support different operations, and the current query changes its causal relevance. The stronger frozen-profile discriminator now supports relation beyond the three registered alternatives, with partial color and readout-limited identity/size results. Ordinary attention-based retrieval is compatible with the observed architecture. A complete algorithm, unique graph, and chronology of learning remain stronger claims.

- **E5 collected:** report the frozen profile, fixed controls, context-level errors, and competence-conditioned counter-trends in §9. Strong weight disorder is a post-held same-surface extension; training-time acquisition remains open.
- **TODO [W]:** lead with interface reuse and selective consumption, then the prospective relation forecast and directed feedback path. Keep discovery graphs, each held split, and post-held follow-ups distinct.

## 3. Regime, architecture, and the accumulation axis

**Claim.** Autoregressive execution is a regime; transformer and SSM are architectures.

- An **autoregressive regime** repeatedly consumes prior state plus a current token/operation and commits new state before the next native output. A transformer or an SSM can run in this regime; the executor supplies token selection and cache advancement.
- A **transformer architecture** typically carries explicit attention K/V plus residual state. It can also be evaluated teacher-forced or in a one-shot prefill without testing native autoregressive continuation.
- An **SSM architecture** carries recurrent and often convolutional state. It can serve the same autoregressive regime through a different family-local state ABI.
- A **diffusion regime** repeatedly applies a denoising operation to carried latent state. Its temporal axis is denoising time rather than generated-token time, even when the role graph aligns.

The paper may compare the role graph across regimes and architectures, but it must not treat “AR” as shorthand for “transformer,” infer a transformer result from a teacher-forced-only panel, or claim the same clock/state tensor across substrates.

- **E2 collected:** the endogenous-store extension includes an eight-token native autoregressive continuation under the frozen role addresses.
- **E3 collected:** both Mamba sizes include the eight-token continuation contract under the recorded runtime ABI; the later-query supplement is native-incompetent.
- **TODO [W]:** use “AR transformer lane” and “AR SSM lane” where both regime and architecture matter.

## 4. Operational discovery and held-out confirmation

**Claim.** A prospective scaffold prediction must separate discovery from evaluation. Exploratory graphs and prompt successors remain valuable with their actual selection history reported.

The stronger confirmation design distinguishes four partitions; the collected lanes implement different subsets:

1. **Mechanics cells:** small rows used only to qualify replay, cuts, endpoints, and resource fit.
2. **Discovery cells:** contexts and operations used to rank sites, infer roles, fit family-local resolvers, and choose a finite role graph.
3. **Context holdout:** unopened contexts for operations represented in discovery.
4. **Operation holdout:** unopened operations, with contexts disjoint from discovery; an optional double holdout contains both new context and new operation.

For a prospective test, the discovery artifact freezes the profile being tested, site bindings or resolver, allowed doses, preprocessing, metrics, and inclusion rules before holdout outcomes are opened. Clean native competence may define row eligibility if the rule is frozen and uses no intervention outcome. Ineligible rows remain visible in the denominator as native-incompetent, not scientific negatives. All four partitions are unnecessary for an exploratory packet or a bounded claim that tests fewer axes.

**Role profile.** A lane records the signed vector its instrument actually measures. The shared superset includes source lesion, store lesion, matched repair, wrong-source, wrong-operation, sham/random, dose, timing/order, continuation, collateral, and mediation effects; a first-wave lane may populate only a declared subset. Role alignment must compare common observed components and preserve missing fields and unmatched roles. It cannot treat raw tensor cosine or normalized depth as a substitute.

**Support criterion.** The exploratory paper reports the distribution of held-out role-profile agreement and native causal effects. It does not collapse them to an omnibus pass. A later terminal claim may preregister a smallest consumer-aligned bundle after calibration.

- **E1–E3 collected:** each lane records a bounded discovery/held split and freezes its selection before held causal outcomes. The implemented partitions and causal components differ by lane and do not amount to the full common superset.
- **Later Qwen modules:** L22–27 was inherited from E20 before the coalition transfer panel; fox/cat is a mechanics/discovery pilot and three lexical scenes are same-policy transfers. The microscopic graph and coding/copy/alias successors are exploratory. They must not be retroactively described as a frozen complete-graph holdout.
- **Confirmation campaign:** the 24-coordinate profile and three prediction controls freeze before two lexical sets × two templates × two orders. The feedback held manifest freezes fruit/shape, city/country, and tool/material before their outcomes. Full-dose disorder and query calibration use opened contexts and are explicitly post-held exploratory. The Qwen cross-family appendix has a later independent prospective boundary; it does not enlarge the original FLUX/Mamba contract retroactively.
- **TODO [R2]:** verify that no prior result used as a discovery prior leaks its target rows into the new holdout manifests.

## 5. Diffusion lane

**Working inference.** A diffusion model may reuse a source → current denoising operation/address → carrier/writer → latent register → RGB-consumer scaffold while prompt-, operation-, seed-, and step-specific causal support changes. The records below identify bounded portions of this organization.

### Current supporting records

- The FLUX format×ontology recurrence panel crosses three prompt forms with three scene organizations. Its shared five-cell lattice recurs while prompt-local lexical addresses and temporal weights move; within-ontology profile similarity is stronger than same-format/across-ontology similarity. This is direct causal motivation for a recurring bus with scene-conditioned execution.
- The cross-prompt structural-grammar panel finds a recurring interior joint-text spine and late image handoff across color, containment, action, reflection, atmosphere, and objectless-field contrasts, with operation-dependent stream handoffs and substantial reversed-time counter-trends.
- Object×scene source factorials in FLUX.2 and Krea prospectively compose a held object/scene combination from three development cells. The images separate coarse semantic main effects from pixel-sensitive interaction, and an unrelated interaction sometimes improves RGB distance without inserting its semantics. This motivates a reusable composition/control grammar while leaving grammar specificity unresolved.
- FLUX full-scene compilation gives exact native RGB for three prospectively sealed prompts at one seed; the source is static while sampled internal carrier hashes change across depth and time.
- The scene-compiler portability audit reports exact family-local prompt compilation across five diffusion families, alongside an unseen-family compressed-span miss: the reusable role story is stronger than the claim that one coordinate basis transfers.
- FLUX.2 seeds `60664`, `19173`, and `84291` compile to one passive 206-node / 305-edge execution skeleton (`2026-08-29-rosetta-circuit-explorer`). This confirms repeatable physical structure but does not identify the functional grammar.
- The current space/time paper reports strict path-distributed diffusion instances and mixed results elsewhere. Those certificates are evidence about a subtype at particular cuts, not proof of the scaffold architecture.

### Completed module and evidence still owed

**E1 completed bounded module: prospectively frozen diffusion address and two-parent dynamics assay.** The module pins FLUX.2 Klein 4B, BF16, a four-step 256×256 schedule, and the native scheduler/VAE. Two discovery rows—color and eye geometry—scan a prior-nominated five-boundary × four-step lattice under exact scalar replay. The worker freezes per-operation and global top-three address policies before it captures five held trajectories: two new color contexts, two new geometry contexts, and an unseen left/right relation, all under new prompt grammar and seeds.

Held rows install target-native deltas only at the frozen addresses. They retain a one-cell arm, the predicted and global supports, half and negative dose, wrong time, a norm-preserving roll, and an intervention-shaped exact base reinstall. This is target-assisted prediction of *where* a held semantic contrast has causal support; it is not autonomous payload prediction or whole-model discovery. A separate native cut after two denoising steps crosses suffix conditioner parent with formed latent parent. Its four cells measure two-parent dependence and interaction through final RGB/register output. They do not identify a unique endogenous source→store mediator.

**Implementation receipt and observations.** Smoke `job-2bd410aa468b` and full panel `job-8fea57981191` completed. The independent analyzer joins scheduler/request/source/model custody, reconstructs the freeze, checks all hook receipts and replay controls, preserves 438 physical denoiser forwards under the declared bound of 472, emits 107 derived evidence observations, and extracts unchanged PNGs. Frozen-support target-image progress is positive on all five held contrasts (`.626–.967`); all half-dose responses are positive and smaller (`.170–.325`), all negative-dose responses are negative, wrong-time effects are smaller (`.076–.198`), and norm-matched rolls are negative. Visual review adds an attribute-allocation qualification hidden by global RGB: eye color follows the suffix conditioner at the tested cut even though its global progress is `.145`, while the formed carrier retains red irises despite `.628` image-wide progress; relation and lamp geometry predominantly follow the formed carrier. The review is unblinded AI inspection and the relation edit has lighting/object collateral. `terminal_status` remains `not_assessed`.

An upstream text-address follow-up is collected separately. Its native-competent unseen relation row misses the predicted lexical-address effect (`-.045` RGB progress), so the current E1 record does not show that the downstream address recurrence is explained by one reusable lexical route. The later post-hoc address-scope diagnostic retains that miss, then finds target-like below placement when the whole active text block is transplanted (`.882` RGB progress). The nonlexical complement also moves toward the target (`.725`) but duplicates the glass; the row-permuted control is near base (`.054`). Single text ports at `t0` change composition with overlap (`.656–.713`), while `t1`–`t3` remain base-like. This localizes the failure to lexical scope versus broader text support at this cut, subject to collateral. It is not a frozen-policy held success, minimal relation circuit, or target-free compiler.

**What E1 can establish.** E1 supports a bounded within-checkpoint trend for prospective downstream causal-address recurrence, dose/sign sensitivity, and conditioner/formed-carrier attribute allocation. The upstream lexical miss keeps the live-address source explanation open. E1 cannot establish complete source/store mediation, a universal diffusion scaffold, minimality, a unique route, autonomous payload construction, or cross-family tensor portability.

## 6. Autoregressive transformer lane

**Bounded result and comparative hypothesis.** Qwen has a reused causal state interface, context-dependent readers, and recipient-native formation paths. Source/prefix, current query, transition/writer, formed store, and native LM-head continuation provide a transformer-specific role account; their alignment with other families remains a comparative hypothesis.

### Current supporting records

- `ArPrefixProgram` prospectively seals prompt K/V and reproduces eight-token native continuation exactly in Qwen2.5-0.5B and Pythia-70M; paired K/V row permutation preserves the tested function while breaking K/V pairing is causal.
- The Qwen native-skeleton/dynamic-circuit assay provides same-parent local and trajectory interventions on a bounded seeded successor-copy calibration. Its report is mechanically valid and explicitly leaves terminal status unassessed.
- The current space/time paper reports formed-store interventions, exhaustive late write/necessity profiles, and Qwen E20 source-to-store mediation. It also reports concentrated, redundant, and mixed writer profiles, so no symmetric all-transformer four-quadrant claim survives.
- Coding mediation provides a native test-harness endpoint in a small six-task organism, but model transplant, prompt route, formatting, and termination remain entangled.

### Completed module and evidence still owed

**E2: Finite AR-transformer role map plus endogenous-store extension.** The implemented Qwen2.5-0.5B module profiles every layer on discovery identity contexts with three typed assays: subject-position residual write, path-matched K/V write, and K/V cut. It freezes one selected and one wrong layer per role, then applies those addresses to a disjoint identity context and color prompts with exact restore, row shuffle, wrong site, and wrong source-layer controls. The sealed consumer is the full-vocabulary next-token head. Native-incompetent and denominator-inapplicable rows remain visible.

The continuation module reused the frozen early residual seed and L20 K/V address on four new identity and four new color rows. The early seed exactly reproduced all eight clean native identity tokens on 4/4 rows, including two native task mistakes. Blocking the formed L20 store reduced answer evidence on 4/4 identity rows; transplanting it into an unseeded path increased answer evidence on 4/4 and improved clean continuation match on 2/4. Median answer-gain recovery was `.793`. Color rescue was positive on 2/4, with median recovery `.083` and no continuation-match gain. This closes a bounded identity source → formed store → continuation chain with redundant routes; it is not operation-general.

An actual query×cache factorial sharpened that boundary. Coherent L20 caches carried fox, lion, and a wrong-donor dog into an animal query with `1.398–1.652` nat answer gains and a `1.844` nat source-specific margin, while the same band failed to convey red/green under a color query (`-.031` source-specific margin). The physical store is readable under one live operation and nearly unreadable under another.

**Implementation receipt.** Jobs `job-02e83e9ae183`, `job-24d2a7164160`, and `job-6a96dadc2701` are collected with exact matched no-ops and formed-store replay. The first map retains a non-specific K/V-cut counter-trend, and native color competence is heterogeneous. E2 cannot establish that every transformer uses the same physical store, that the identity chain generalizes to color, or that one late band carries every query-readable fact. `terminal_status` is `not_assessed`.

### Qwen2.5-1.5B architecture result

**Reused interface and context-dependent consumption.** The completed panel reuses the L22–27 interface fixed by prior E20 on a fox/cat pilot and three same-policy transfer scenes, yielding 64 correlated query rows. Late queried fact-span replacement authors color in 16/16 rows and position in 12/16, while identity authors the donor animal in 11/11 available reads with five unavailable. Position replacement jointly swaps layout and is already supported earlier in 9/16 rows. When parent and K/V patch are identical and only the native query changes, query-selective harm is positive in 16/16 color and 16/16 position contrasts, with medians 3.1305 and 0.5829 nats. The optional position→color diagnostic is native-competent in 15/16 rows and places the donor color top in 7/16. The 128 directional matching checks cover 32 unique query pairs; they establish exact patch pairing rather than independent replication. Custody is receipt-level with identical patch manifests/digests; the original retained tensors are unavailable for a fresh offline rehash. [Blog](../../../obsidian/blog/2026-10-01-141628-the-question-decided-which-stored-fact-mattered.md) · [findings](../../../saturn/experiments/2026-10-01-qwen-scaffold-context-poc/FINDINGS.md) · [analysis](../../../saturn/experiments/2026-10-01-qwen-scaffold-context-poc/analysis/analysis.json).

**Shared readers with operation-specific weights.** The 204-branch native Qwen1.5 graph packet resolves shared L23/KV0/V and L22/KV1/V influence across identity, color, and relation. Signed profile recurrence across two queried bindings is .947/.927/.961; operation overlaps are graded (.749 identity/color, .336 identity/relation, .778 color/relation). Both six-query-head GQA groups have causal repair effects. Qwen has twelve query heads sharing two K/V heads: KV0 feeds Q0–5 and KV1 feeds Q6–11. Individual query-head necessity, unique minimality, MLP writers, and microscopic source-token-to-reader edges remain open. The four-token native continuation reaches the executor's autoregressive token/cache loop. This extends the original coalition map in one scene/order; prospective microscopic replication and repeated semantic feedback remain separate questions. [Head/edge findings](../../../saturn/experiments/2026-10-01-qwen-head-edge-topology/FINDINGS.md) · [graph](../../../saturn/experiments/2026-10-01-qwen-head-edge-topology/graph.json).

**Prospective microscopic extension.** The confirmation campaign freezes that discovery's 24-coordinate signed profiles and operation-blind, wrong-operation, and within-band coordinate-permutation alternatives before opening two lexical sets × two templates × two orders. Relation beats all three fixed alternatives in raw error in 8/8 context combinations; competent context cosine is .954 versus .566 operation-blind and raw RMSE .029 versus .149. Color's competent cosine is .839 versus .828, while operation-blind raw error is slightly smaller (.109 versus .119). Color's coarse shared-site ranking matches only 1/8 combinations and reader ranking 0/8. Identity has six competent native binding rows out of sixteen; operation-blind is better on the four contexts with any competent identity row. Size is native-readout unavailable. The fixed generic coordinate permutation is poor across operations, but post-run LOCO generic A/B/reader ordering succeeds descriptively in 8/8: the prospective full profile is more discriminating than the coarse rank alone. These are bounded predictive recurrence and counter-trends, not an invariant map for every operation. [Predictive findings](../../../saturn/experiments/2026-10-01-scaffold-confirmation/qwen-predictive/FINDINGS.md).

**Recipient-native formation.** In the original panel, a supplied clean L12 identity residual produces recipient-native late state: independent anchor rescue yields the target in 16/16 generated reads and block-back yields the donor in 14/14 available reads. The later mechanically valid 247-arm, eight-case panel retains native source-token layer cuts and resumes residual writes through unchanged later layers. L11 is the post-layer cut entering L12. Full seeding gives the clean registered value first in 8/8 cases; norm-matched random writes give the donor first in 8/8. Scene identity and Python return values both close seed → recipient-formed L22–27 anchor → independent rescue → block in two prompt structures. The coding cases change consumer syntax as well as source order, so their difference cannot isolate an order effect. Copying has collateral/order effects; aliasing separates full-residual success from failed anchor-only rescue and exposes binding selection beyond the supplied source anchor. Source addresses and clean residual payloads are host-supplied. These experiments map source-to-state formation at layer resolution, while a complete microscopic writer path remains open. [Formation synthesis](../../../saturn/experiments/2026-10-01-qwen-formation-replay/FINDINGS.md).

**Prompt and instrument limits.** The source-line bundle is redundant in this source-step geometry because added pre-anchor rows were unchanged. A labelled-copy successor is natively competent in both orders, with one rescued continuation changing the second binding as collateral. A subtraction assay with independent 7/9 source and 6/8 output registries is mechanically valid but has unavailable native numeric readouts. Return-value retrieval therefore supplies the coding result; transformed arithmetic remains unestablished. These are exploratory successors rather than disjoint confirmatory holdouts. Formation during inference does not measure acquisition of the scaffold during training.

**Executable memory receipts, separate from the semantic result.** Real Qwen tests exercise residual eviction/hydration, LiveStateCut query/reopen, Thott shared/append/fork/restore, paged-K/V copy-on-write and native consumption, and debugger preview/abort/commit/restore/replay through an experiment-local residual delegate. A fresh lease reopens the physically bundled Thott parent/append and debugger residuals; clean and edited branches reproduce full logits/K/V/token hashes exactly. Historical debugger cuts omit staged K/V and parent-chain custody, so numerical closure comes from the joint bundle and chain equality is not claimed. The complete shipped durable-cut API, spectral semantic-address execution, MinIO serving, CUDA VMM integration, and continuous batching are unexercised here. These receipts make the intervention and replay machinery concrete; they do not independently establish a learned semantic scaffold. [VM audit](../../../saturn/experiments/2026-10-01-qwen-formation-replay/VM_CAPABILITIES.md) · [updated blog](../../../obsidian/blog/2026-10-01-141628-the-question-decided-which-stored-fact-mattered.md).

The new feedback packet additionally captures complete physical parents and staged K/V through LiveStateCut storage and restores cache/logits/token exactly in its resident runtime. This is same-process durable closure; it is distinct from the earlier fresh-lease joint-bundle result. Its fused TokenMachine path constructs native causal masks; a separate L22 decomposed observer reproduces that capture exactly. Monolithic `model.forward` parity on every cycle and production serving remain unclaimed.

## 7. Autoregressive SSM lane

**Working inference.** An SSM may instantiate comparable roles with token events, current input, ordered convolution/recurrent transitions, native state writes, carried state, and the unchanged LM-head continuation. E3 identifies bounded state-write profiles, rather than the full aligned graph.

### Current supporting records

- Mamba transition-source compilation reports depth-wide relation-delta alignment (`0.9792–0.9874`) across six held relation/entity cells, but strict native competence admitted only two held semantic cells.
- Recurrent-only and conv+recurrent programs behave differently on long continuation. A historical/current runtime discrepancy reversed which operand gave longer agreement, motivating the execution-ABI fingerprint and prohibiting unsealed state portability claims.
- Full Mamba sweeps in the current space/time paper found a locally decisive late writer/retention latch rather than a strict distributed four-quadrant circuit.
- The role-portability ABI already lowers common role names to Mamba-native `(conv, recurrent)` state and forbids tensor equivalence with transformer K/V.

### Completed module and evidence still owed

**E3 completed bounded module: prospective AR-SSM state-write scaffold assay.** The Mamba module captures complete convolution/recurrent state immediately after one changed carrier token. Discovery profiles every layer with generic `(C,H)` necessity, target `(C,H)` write, recurrent-only write, and convolution-only write. It freezes a three-layer band, then evaluates new identity/counting contexts and an unseen capital operation with target joint/recurrent/convolution state, wrong source, wrong layer, wrong sign, depth shuffle, uninstall, native log-probability effects, and eight-token continuation. The same finite assay is collected independently at 130M and 370M checkpoints.

This module identifies a downstream family-local state-write profile at a declared cut. It does not lesion an earlier source and restore a downstream state in the same parent, so it must not be reported as complete source→store mediation. Native-incompetent counting rows and a continuation/first-token admission disagreement remain part of the evidence.

**Implementation receipt and observations.** Corrected jobs `job-2bde6a0f47c7` (130M) and `job-ee475fa35dee` (370M) independently select late three-layer bands. Prompt-local convolution state carries most immediate lexical-source transfer; recurrent-only replacement is weak. Held identity and capital continuations change toward donor subjects/countries, early-layer and wrong-sign controls are weak, and coherent wrong donors produce coherent alternate subjects. Counting rows are native-incompetent and remain visible. The later-query supplement `job-44ac3efae7bf` is mechanically valid but lacks paired native semantic competence in both its primary and predeclared alternate organism, so it is `not_applicable`, not a negative architecture result. The supplement's diagnostic shift toward recurrent state is consistent with cut-dependent operand allocation but has no semantic authority. E3 can support a bounded role-recurrence and operand-specific state-write trend. It cannot establish optimized-kernel portability, universal SSM behavior, equivalence to transformer K/V, or a fully mediated endogenous path. `terminal_status` is `not_assessed`.

## 8. Cross-architecture extension

**Claim.** The same abstract role graph may recur across diffusion, AR transformers, and AR SSMs even though their tensors, sites, clocks, and state sizes differ.

Coarse source/transition, carried-state, and consumer responsibilities already have convergent support across the records. A prospectively aligned graph is a stronger extension. E4 is necessary for that cross-family claim, not for the bounded Qwen interface result.

The cross-family object is a graph of causal roles plus assay relations:

```text
semantic source
    -> current operation / live address
    -> family-local transition and writer
    -> carried state
    -> unchanged native consumer
```

For prospective confirmation, fit the alignment on discovery records and evaluate unopened, competent family-local assays. Compare common role-profile directions, mediation structure where measured, operation/state interactions, timing order, continuation behavior, and counter-trends. Exploratory alignment can use opened records if labelled as such. Do not compare raw logits, tensor cosine, hidden dimensions, normalized depth, or site names as if they were one representation.

**E4 partial prospective extension collected.** The new campaign freezes a smaller common profile before its FLUX/Mamba held outcomes: state-block remaining, coherent rescue, actual wrong-time/depth, and intact joint parent. Two held rows per family give mean profiles FLUX [.0845, .8073, .1589, 1] and Mamba [.0803, .9065, .0020, 1]. Causal-role RMSE .0928 is smaller than the frozen role-permutation .8526; the joint coordinate is normalized to one and is not independent evidence. A separately sealed later Qwen appendix has one paired-native-competent city/country row out of three: [.0076, .9585, .4939, 1]. Its competent pairwise alignment favors the causal map against both families. Its all-row diagnostic reverses that comparison when an incompetent tool target and a small base-to-target parent-contrast normalization denominator inflate the wrong-depth ratio. Both views remain visible. [FLUX/Mamba findings](../../../saturn/experiments/2026-10-01-scaffold-confirmation/cross-family/FINDINGS.md) · [Qwen appendix](../../../saturn/experiments/2026-10-01-scaffold-confirmation/cross-family/qwen-appendix/FINDINGS.md).

**Native endpoint qualifications.** Blinded FLUX review finds a mostly blue boot rescue with yellow panels, and an arched door produced by either current conditioning or formed state; global RGB understates the current-only local shape effect. Mamba's zebra rescue shifts the target score but first generates `small`, whereas Athens rescues exactly. Qwen's reverse-depth arm generates `1`, France rank 8,377, despite a sizable normalized candidate-margin shift. These are actual same-destination stress controls, not behavior-matched alternative architectures. The earned common edge is family-native formed state → unchanged native consumer. Current-operation/read, source mediation, minimal writer, and feedback are not completely matched.

**TODO [E4 full graph]:** extend the prospective alignment to the currently unmatched roles on competent family-local assays. Preserve family-specific edges and compare only commonly observed relations. The partial core does not identify the entire hypothesized topology.

**Historical diagnostic, not prospective confirmation.** A post-hoc signed-profile matcher used already opened held rows, and the SSM side pooled discovery and held cells while aliasing joint `(C,H)` controls to transformer roles. Its lowest-cost mapping—residual → convolution, K/V writer → joint state, K/V cut → recurrent state—was only `.0386` better than the next assignment and nearly tied a depth-based null. This historical ambiguity is retained. The new smaller prospective core does not retroactively qualify that matcher or close its full graph.

**Possible outcomes.** Full alignment, a smaller shared core plus family-specific roles, or no useful common graph are all reportable. A shared core would not imply a universal circuit or tensor ABI.

## 9. Minimum discriminating tests for stronger claims

**Claim.** The bounded causal interface result is already supported. A stronger predictive role-graph account should forecast unseen causal effects beyond generic late attention reuse. Predictive structure and learning origin are separate claims.

**E5 collected; frozen design retained below.** The confirmation campaign implements the microscopic prediction on unopened context combinations, with registered operation-blind, wrong-profile, and coordinate-permutation forecasts. Its full signed relation result is strongest; color/identity/size are heterogeneous as reported in §6. The original discovery protocol is:

1. Freeze the current microscopic sites, source/store/read assignments, and signed profiles before opening new contexts/orders for identity, color, and relation. Retain exact parent/patch identity when testing query-dependent relevance. For a semantically different operation, preregister a coarser shared-route prediction or freeze an explicit operation-to-profile resolver; the present record supplies no resolver for unseen operation weights.
2. Compare that prediction with a site/depth-matched profile and an operation-blind profile. Match intervention size and dose; activation energy or graph degree can refine the site match when they are the specific alternative explanation, rather than becoming additional mandatory tests.
3. Measure native semantic continuation, signed answer effects, collateral, and newly written state where a writer is claimed. Preserve incompetent and unavailable rows. Source-lesion, recipient-formed-store block, and independent rescue are needed where predicting a complete formation graph; color is a useful prospective complement to the already collected exploratory identity/coding chains. It is not required merely to test microscopic reader recurrence.

The question is whether frozen roles predict **which patch matters under which query and what downstream state forms**, better than the matched comparisons. This is a scientific discriminator, not an omnibus exploration gate. Profile agreement, magnitudes, counter-trends, and effective sample size remain visible.

**Additional claims and current tests.** Qwen's same-surface final-weight disorder now demonstrates dependence of the signed profile on the tested value-projection correspondence (§11.2). Pythia supports a separate developmental trend; neither establishes Qwen acquisition chronology. Successive semantic feedback is now boundedly established in development and one competent held context (§11.1). E4 earns the smaller prospective state/consumer core (§8); the complete graph remains open. Wrong-source, wrong-state, order/time, and random arms remain useful diagnostics, without requiring every control to win on every row. An incompetent randomized model cannot supply a behavior-matched semantic null.

## 10. The strict four-quadrant subtype is optional

**Claim.** A scaffolded dynamic circuit may be local, redundant, distributed, or mixed at a particular cut. The four-quadrant pattern is one optional subtype.

The strict pattern asks whether every tested singleton is below declared necessity and sufficiency criteria while the whole path meets both. It is valuable when applicable, but it is not required for:

- role recurrence;
- source-to-store mediation;
- operation/state interaction;
- a dynamic semantic subcircuit;
- cross-architecture role alignment.

A scaffold may contain a locally decisive writer or latch, as current transformer and Mamba records do. Conversely, a four-quadrant result can arise from a weighted additive path and does not by itself prove a learned scaffold.

**TODO [E10] (optional):** after E1–E3, run exhaustive singleton and joint interventions only in lanes whose first-wave profiles make this subtype scientifically informative. Keep it a separate result.

## 11. Extensions beyond the bounded result

### 11.1 Operation/state conjunctions and continuation

**Historical instrument qualification.** The E6/E8 custom attention wrapper registered a new implementation without its matching causal-mask factory in Transformers 5.14.1. Multi-token query chunks could therefore attend to future query tokens. The original routing, appended-state, native-competence, and continuation measurements below are historical observations under that instrument, not qualified native causal results. Exact wrapper self-replay cannot repair this shared defect. The [causal-mask audit](../../../saturn/experiments/2026-10-01-scaffold-dynamic-circuits/ar-feedback/corrections/2026-10-01-causal-mask-audit.md) preserves the reports; [corrected routing job a9855804978c](../../../saturn/experiments/2026-10-01-qwen-routing-mediation/FINDINGS.md) matches untouched eager controls on already-open contexts. It switches all three selectors, including Madrid/Berlin; the old London endpoint is not a native counterexample. Single-row route restoration attenuates margins by 25%, 9.5%, and 40%, while all selected continuations survive. It closes a bounded route contribution, not later-store mediation, and adds fresh n=0.

**Historical E6 route/write module under the qualified instrument.** Prospective job `job-dade0194f43a` freezes selector residual L12 → attention read L16 → newly committed query K/V L17 before opening three held outcomes. Its recorded discovery continuations are `a fox` and `the lion`; compiling the second selector into the fixed-first recipient yields `a lion`, so the historical first-token article gate is false even though the four-token fact changes. On held color, object, and place rows, recorded route recoveries are `1.880`, `1.027`, and `1.013`, and the L17 writer state is closer to the target in all three. Blocking fact 2 flips the read direction and lowers second-answer log probability in all three. These numbers are not reused as native causal measurements.

The held native first/second continuations are nevertheless identical (`red`, `plate`, and `Paris`), so the 0.5B panel cannot establish a paired semantic selector or held semantic feedback. L0 `wrong_site_second` exactly reproduces native-second endpoints and is therefore an upstream source baseline, not a hostile wrong-address null. Same-scope qualification job `job-3626c2a1b385` binds the prospective job/report/freeze/endpoint digests and closes hook delivery, capture counts, cache append, and exact endpoint replay. Because its held outcomes were already open, its effective scientific sample size is zero.

**Historical 1.5B replicate, also mask-qualified.** Exact-template job `job-01c81b3f5029` used predeclared green/yellow, spoon/fork, and Madrid/Berlin values with no selector search, lowering roles to L4→L22→L23. The old wrapper recorded two semantic switches, read recoveries .916/1.006, and London rather than Madrid on the first place endpoint. These are historical instrument observations; the recorded competence labels and London counterexample are not native task evidence. The corrected routing follow-up yields Madrid/Berlin and matches untouched eager execution. Neither historical self-replay nor the corrected already-open routing packet independently establishes later-store mediation; the new held packet below supplies that separate edge.

**Interpretation of the historical paragraphs.** Their recorded magnitudes and prior competence labels are preserved for provenance under the mask qualification above. Their original native-feedback interpretation is superseded; the current result comes from the independently sealed packet below.

**New directed two-update result, host-orchestrated.** A separate FP32 Qwen2.5-1.5B TokenMachine packet uses native causal masks and known queries appended one token at a time. Development produces `cat → blue → blue`. Coherent first-row fox state changes the next prediction and final answer to red. Processing that native red prediction forms a new recipient K/V row. With first state, prefix, query, visible red token, and recipient final hidden state fixed, swapping only the new second row to clean blue state yields blue; zero gives `is`; exact reinstall gives red. The frozen city/country holdout repeats the path: Berlin→Germany→Germany and Paris→France→France are both competent; a first-row donor yields native France; processing it forms S2; clean Germany S2 then flips the later answer France→Germany while visible France stays fixed; reinstall restores France. Direct parallel paths remain possible.

The causal intervention is the complete **all-28-layer newly staged K/V row bundle**. L27 names the resumable cut, not the sole layer written. One held context out of three earns the complete semantic path. Fruit's base and serial final readouts are incompetent; tool never forms its target state. All effects remain collected. The native semantic authority is fused TokenMachine execution with unchanged blocks/LM head; the separate decomposed L22 observer has exact same-parent logits/K/V/token parity at its capture. It does not prove every-cycle monolithic `model.forward` parity or unique L22 mediation. Host-supplied queries, donors, and branch selection make this a controlled semantic feedback assay, not an autonomous internal loop. Raw terminal status remains `held-confirmation-not-assessed`; no new calibrated terminal bundle is implied. [Feedback findings](../../../saturn/experiments/2026-10-01-scaffold-confirmation/qwen-feedback/FINDINGS.md).

### 11.2 Development and training

**E7 completed bounded module.** Pythia-70M final-checkpoint discovery selected K/V layers `[3,5]` from three new label-copy contexts before opening four held outcomes. The exact same full-prefix K/V profile, wrong-label donor, fixed `[0,4]` site control, and exact base reinstall ran through a single FP32 native LM-head consumer at steps 256, 512, 1000, 2000, 4000, and final. Native target top-1 competence rose from 0/4 at steps 256/512 to 3/4 at steps 1000/2000 and 4/4 at step4000/final. Mean held semantic denominator and selected raw effect were respectively `.046/.019` at step256, `.668/.200` at step512, `4.165/2.632` at step1000, `3.838/2.393` at step2000, `5.070/3.258` at step4000, and `5.333/3.310` at final. These signed trajectories are observations, not a monotonicity claim.

At final, the frozen coalition beat the coherent wrong-label donor on 4/4 held rows and the fixed random-site control on 3/4. The object-card row is the important counter-trend: `[0,4]` moved the target margin by `8.519`, versus `4.734` for frozen `[3,5]`. A final-parent in-memory weight shuffle preserved the module graph, parameter shapes, and each tensor's value multiset; it had 0/4 native top-1 competence and much smaller raw effects. That arm tests whether the final-frozen effect profile recurs after learned weight organization is destroyed; it does not rerun the discovery selector on shuffled discovery rows. Its incompetence is not a behavior-level semantic null.

Corrected panel `job-4e053261e196` used seven authenticated hydrations, one model object, 391 forwards, 28/28 exact intervention-shaped base reinstalls, the full-vocabulary native consumer, and report-bound evidence records. Named early checkpoints are QStore-bound to exact source bytes; QStore is not the causal runtime. The assay remains target-assisted and full-prefix, uses one 70M family and seven prompts, and did not preregister a separate expected native-output fingerprint after each hydration. It supports a developmental carrier-sensitivity trend; it does not establish a general developmental law, unique mediator, or universal scaffold.

**TODO [E7 extension, optional breadth]:** repeat the trajectory in a second checkpoint family and add source-lesion/store-rescue profiles if E6 identifies a qualified endogenous cut. For a learning-origin claim about the present Qwen role profile, a same-surface weight-organization discriminator is more direct than requiring a broad developmental law.

**Qwen same-surface final-weight organization comparison collected.** A preregistered mild arm permutes 13 or 51 output rows (5%/20%) in L22/L23 `v_proj`, including biases; signed profiles largely persist. The separately sealed post-held extension permutes all 256 rows in those two projections only, preserves shapes/norms, and restores weights bit-exactly. Across the same four opened context combinations, mapped cosine at doses 0/.05/.20/1.0 is identity .931/.924/.905/.569, color .838/.834/.794/.110, and relation .955/.952/.946/.049. The full disruption collapses signed alignment, including among remaining competent rows. Relation raw-error wins still occur in 3/4 all-row contexts and 2/4 competent/applicable contexts, so magnitude and signed organization are distinct observations. Native competence falls: identity 3/8→2/8, color 8/8→6/8, relation 8/8→5/8 binding rows. This establishes dependence of the measured profile on final-checkpoint value-projection correspondence, not a behavior-matched semantic null, smooth dose law, whole-model shuffle, or chronology of acquisition. Development query calibration finds identity answers in 8/8 formats/bindings and direct-adjective size answers in 2/2, while the registered size format stays unavailable; that motivates a new prospective instrument and does not reinterpret held size. [Predictive and disorder findings](../../../saturn/experiments/2026-10-01-scaffold-confirmation/qwen-predictive/FINDINGS.md).

### 11.3 Replication and breadth

**E8 partial bounded replication and local verifier.** The 370M Mamba panel repeats E3 at a second size. Historical E6 repeats a template/policy at Qwen1.5B, but its scientific interpretation remains mask-qualified. These are same-lab records, not independent-family or independent-laboratory confirmation. The historical [`campaign/RUN_INDEX.json`](../../../saturn/experiments/2026-10-01-scaffold-dynamic-circuits/campaign/RUN_INDEX.json) and [`campaign/verify.py`](../../../saturn/experiments/2026-10-01-scaffold-dynamic-circuits/campaign/verify.py) pin thirteen custody/mechanics packages; that receipt does not cure the shared attention-mask defect. Later Qwen coalition/head/formation and C1–C4 packets have their own custody and verification. Lexical/prompt transfers and the later prospective family comparisons add bounded breadth. Independent replication and a release-reviewed public bundle remain confidence and release work.

### 11.4 Predictive compiler

**E9 historical application precursor; predictive compiler is a separate claim.** E6 assembles each held recipient from prefix-donor activations and the family-local frozen address before that row's target query. Its old answer/competence results remain qualified by the mask defect, so they cannot certify a native semantic compiler. The corrected routing packet and new formed-row experiments supply bounded native state assembly and consumption with their own scopes. They do not learn an autonomous address/payload compiler or supply operation-blind/site-matched compiler baselines. Claiming the full E9 compiler requires compiling a held operation/context without its causal outcomes, executing it through the native consumer, and comparing with claim-matched baselines and an oracle ceiling. This application is unnecessary for the bounded architecture paper.

## 12. Instruments, analysis, and reporting

**Claim.** The evidence should remain trend-first and cut-specific.

Keep immutable lane-local raw records. The shared summary schema uses specimen/checkpoint/context, operation, source/address/route, carried-state parent, carrier trajectory, writer, consumer, intervention sign and dose, target/collateral/repair/continuation effects, instrument limitations, developmental stage, and terminal status where measured. Mark unknown fields explicitly; a common schema must not invent measurements. Summaries must preserve:

- signed effects and magnitudes;
- context and operation denominators;
- dose and checkpoint trajectories where present;
- rows that disagree with the aggregate;
- native-incompetent, inapplicable, and instrument-broken rows;
- discovery versus each holdout partition;
- evaluator disagreement and effective sample size.

Use separate `mechanics_status`, `instrument_status`, `trend_status`, and `terminal_status`. The first wave has `terminal_status: not_assessed` unless a later explicit, calibrated terminal bundle is declared before opening the relevant split.

### Minimum hard gates

Only evidence integrity and safe continuation may stop first-wave execution:

- exact model/checkpoint/tokenizer/runtime/config identity and artifact custody;
- held-out manifest quarantine and discovery-artifact freeze;
- same-parent lineage, non-aliasing branches, hook/intervention delivery counts, and declared replay tolerance;
- shape, dtype, device, finite-value, valid-cache/state, and native-consumer execution contracts;
- reversible restore/uninstall where claimed;
- memory, VRAM, timeout, and corruption guards.

Semantic thresholds, role-profile similarity, energy, cosine, mediation magnitude, RGB distance, task accuracy, and control wins are observations in exploration. A weak or mixed row does not abort remaining valid panels.

- **TODO [R3]:** define one schema crosswalk from E1–E3 outputs to the shared evidence record.
- **TODO [W]:** write results in the workspace vocabulary: observation, trend, convergent trend, working inference, terminal claim.

## 13. Applications and their additional evidence

**Implication.** A reusable causal interface makes state inspection, intervention, and replay practical. A validated predictive role map could additionally support a debugger or compiler that selects addresses by function and lowers them to family-native state.

Potential applications are:

- a causal debugger that follows source → store → consumer and shows input-specific support;
- a compiler that predicts a dynamic subcircuit for a new operation and abstains outside discovery support;
- family-local state virtualization with one control-plane vocabulary;
- training feedback that observes candidate futures at causal roles and rewinds rejected updates.

Existing scene compilers, role ABI, Frames/Acts/StateCuts, and the evidence plane provide mechanics. The new Qwen memory packet directly demonstrates bounded residual writes, Thott/paged-KV persistence, debugger transactions, and fresh-lease numerical replay. Automatic role selection and a donor-free compiler need separate prospective validation; production paging, serving performance, and transparent all-tensor memory need their own systems assays. Their absence does not weaken the measured causal architecture result.

## 14. Limitations and alternative explanations

- The evidence still comes from one lab and few model families. E3 spans two Mamba sizes and E7 spans six Pythia training checkpoints, while E1 and the main E2 role map remain narrow checkpoint/schedule specimens.
- A role profile can recur because depth, time, or bottleneck geometry recurs. The collected E5 comparison discriminates relation from three fixed alternatives, but color's coarse ranks and the descriptive LOCO generic ordering limit a uniformly operation-specific claim.
- Semantic tasks may share lexical templates or evaluator artifacts. Prospective claims must report their actual context/operation splits and template families. The current coding result is return-value retrieval; it does not establish a new algorithm or transformed arithmetic.
- Clean native-competence selection conditions the scientific population. Parent denominators and rejected rows remain visible.
- Source/store rescue may reflect a broad overwrite rather than the proposed mediator. Wrong-store, random, dose, collateral, and continuation controls constrain this interpretation without proving uniqueness.
- A family-local store may be redundant or self-repaired. Singleton and joint interventions answer different questions.
- Cross-family role alignment may be imposed by the analyst's vocabulary. The old post-hoc near-depth-null tie remains historical; the new prospective permutation comparison supports a smaller state/consumer core. Full source/read/write/feedback topology remains unmatched. Normalized joint=1 is not an independent observation, and severe wrong-coordinate controls are not behavior-matched architectures.
- Exact prompt/source reinstall proves compiler mechanics, not learned compact semantic decomposition.
- A strict four-quadrant result does not prove the scaffold; absence of the pattern does not refute it.
- Current Mamba evidence is runtime-sensitive and small; current AR dynamic-circuit evidence includes a synthetic successor-copy calibration; current diffusion evidence is strongest on a small number of seeds and schedules.
- Historical E6/E8 reads/writes, native competence, and continuations are qualified by a causal-mask defect. Corrected routing uses already-open contexts. The new host-orchestrated two-update packet has one clean held semantic chain out of three; fruit and tool limitations remain visible. It cannot supply independent-family feedback replication or an autonomous loop.
- The microscopic discovery map covers one scene/order. Its frozen profile has subsequent prospective context-combination evidence strongest for relation, partial for color, and readout-limited identity/size. Individual query heads are observed, while causal rescue is at six-head GQA-group resolution. Whole-row feedback interventions span all 28 layers and do not localize a minimal writer.
- Inference-time residual seeding supplies source payloads and token addresses. Recipient-native formation is measured; autonomous source/address discovery and training-time acquisition of the Qwen role graph are not. Strong final-weight disruption affects only two selected value projections and loses some competence, limiting learning-origin inference despite current-profile dependence.
- Numerical replay of the joint Thott/debugger bundle is exact in a fresh lease, while chain fingerprints differ. Memory mechanics and semantic architecture remain separate evidence classes.

## 15. Related work (plan)

**TODO [W]:** organize related work by the exact distinction it supplies:

- mechanistic circuits, activation/path patching, ACDC, attribution graphs, and causal scrubbing;
- temporal and sequential activation patching, deferred commitment, CoT interventions, and distributed stores;
- diffusion timing, timestep-conditioned graphs, vital-layer editing, and K/V editing;
- recurrent/SSM interpretability and state interventions;
- task/function vectors, state-space control, dynamic routing, conditional computation, and neural program interpreters;
- schema/role induction and graph matching;
- developmental interpretability and checkpoint trajectories.

Do not claim priority from absence of an identical phrase. State which prior pieces exist and which prospective causal combination this paper adds.

Primary anchors for the draft:

- [Geiger et al., *Causal Abstractions of Neural Networks*](https://arxiv.org/abs/2106.02997) formalize alignment between neural and causal-model variables and verify proposed high-level roles with interchange interventions. This supplies the causal-role abstraction basis; our proposed extension is a prospectively reusable recurrent role scaffold with state-dependent semantic support across substrates.
- [Todd et al., *Function Vectors in Large Language Models*](https://arxiv.org/abs/2310.15213) identify compact task representations carried by attention heads and test them with causal mediation. This motivates reusable semantic payloads; our planned discriminator asks whether payload support moves over a recurrent scaffold and changes with carried state and live operation.
- [Ameisen et al., *Circuit Tracing: Revealing Computational Graphs in Language Models*](https://www.transformer-circuits.pub/2025/attribution-graphs/methods.html) construct prompt-local replacement/attribution graphs and state the challenge of moving from local graphs to global circuits. Our proposed contribution is a held-out resolver for recurring causal roles, while preserving prompt-local support and unmatched roles.
- [Kamath et al., *Tracing Attention Computation Through Feature Interactions*](https://www.transformer-circuits.pub/2025/attention-qk/index.html) explain attention QK read patterns through feature interactions, extending attribution graphs that had frozen attention. This directly informs the proposed state→next-read test: carried state should causally alter the active read pattern and writer under a fixed external source.

The current contribution is bounded causal reuse: a prior-fixed state interface supports several operations, the query changes the authority of identical stored state, and shared reader routes have operation-specific weights. Recipient-native formation connects an earlier source to independently effective carried state. The new evidence adds prospective relation-profile prediction, a host-orchestrated two-update semantic path, dependence on final-weight correspondence, and a prospective partial state/consumer core across substrates. Complete graph alignment, learning-time acquisition, broader feedback, and automatic addressing remain stronger hypotheses. Priority requires a careful comparison with the cited work; it cannot be inferred from a new name or from the predecessor class alone.

## 16. Conclusion to write from current evidence

The Qwen evidence supports a reusable causal interface with dynamic semantic support. The same late state substrate serves several operations; the native question changes which fact matters; shared reader coordinates carry different operation weights; and earlier residuals can form independently causal late state. The scene, coding, copy, and alias contrasts reveal both reuse and structural limits. This is a concrete architecture result built on the predecessor space–time circuits.

The confirmation campaign now supplies prospective relation-profile recurrence beyond three fixed alternatives, while color's reader ordering misses and identity/size expose readout limits. A new native Qwen packet establishes a directed two-update semantic path in development and one fresh competent city/country holdout; host queries, all-layer donor state, and whole-row interventions define its scope. Full permutation of two value projections disrupts the signed profile, whereas mild permutation largely preserves it. This supports current weight-correspondence dependence rather than chronological acquisition.

Diffusion and Mamba prospectively align on a partial formed-state→native-consumer core, with a later one-row competent Qwen appendix. Visual attribute allocation, imperfect rescue continuations, unmatched roles, and the Qwen all-row normalization counter-trend prevent a complete shared-graph claim. Learning-time acquisition, fuller cross-family topology, broader feedback, automatic addressing, and a general learned semantic compiler remain separately testable extensions; exact source lowering and bounded payload prediction have already run. Local writers, redundant stores, distributed paths, and strict four-quadrant subtypes are compatible with the bounded account.

---

## Appendix A — Collected modules and prospective extensions

Q1–Q3, VM, and C1–C4 identify later packets without relabelling historical E1–E10 experiments. All historical terminal statuses are preserved, with the separate E6 mask qualification explicit. The final column states which claim needs the module; it is not a conjunctive completion checklist.

| ID | Experiment | Required output | Status | Claim served |
|---|---|---|---|---|
| Q1 | Prior-fixed Qwen1.5 interface across four lexical scenes; same-patch/query contrasts | Correlated native rows, identical patch receipts, identity formation/rescue/block, custody | **collected; positive multi-operation reuse and selective consumption; unavailable reads retained** | Bounded paper core |
| Q2 | Qwen microscopic head/edge packet | 204 typed branches; K/V effects, joint interactions, GQA-group rescue, native attention/context profiles | **collected; shared value coordinates and binding-relative profiles; one scene/order, exploratory** | Bounded paper core; prospective extension below |
| Q3 | Qwen residual formation across scene/coding/copy/alias structures and successors | Executable layer cuts, depth/dose curves, recipient-formed-state rescue/block, native continuations | **collected; identity/coding chains, copy collateral and alias limits; arithmetic readout unavailable** | Bounded paper core |
| VM | Qwen memory/residual/debugger and fresh-lease replay | Physical payload custody, native clean/edited logits/K/V/token replay, capability limits | **collected; exact joint-bundle numerical closure; chain equality unclaimed** | Separate systems result |
| C1 | Frozen microscopic profile prediction | Prior profiles, three fixed alternatives, unopened context/order rows, typed lane receipts, additive collision audit | **collected; relation raw wins 8/8 context combinations, color partial/ranks miss, identity/size readout limits** | Predictive bounded extension |
| C2 | Same-surface Qwen final-weight correspondence | 5%/20% sealed doses plus separately sealed post-held 100% rows of two value projections; competence/effect profiles, exact restoration | **collected; mild doses preserve, strong disruption collapses signed profile; acquisition chronology unestablished** | Current weight-organization dependence |
| C3 | Native successive formed-row feedback | Native S1/S2 predictions, all-28-layer row capture/block/swap/reinstall, fixed-S1 and visible-S2 serial intervention | **collected; development plus one competent held city/country case of three; causal mask/native authority explicit** | Bounded two-update semantic path |
| C4 | Prospective partial common state/consumer core | Frozen FLUX/Mamba four-profile contract, visual/native endpoints, later prospective Qwen admission, unmatched roles | **collected; n=2 FLUX, n=2 Mamba, later Qwen n=1 competent of 3; all-row disagreement retained** | Partial comparative architecture |
| E1 | Diffusion finite site×time discovery + context/operation holdout + target-assisted controls + suffix-conditioner×formed-latent factorial | Frozen top-three policies, native RGB/register rows, hook/replay receipts, contact sheets, custody | **collected and visually reviewed; recurrence/dose trend with attribute-allocation split; upstream lexical miss and post-hoc whole-text diagnosis retained; terminal not assessed** | Comparative evidence |
| E2 | Qwen0.5 full-layer residual-write/K/V-write/K/V-cut map; endogenous-store/continuation extension | Native next-token role rows, identity mediation, eight-token continuation, query×cache factorial | **collected; identity chain positive, color/query transfer weak or absent; terminal not assessed** | Comparative and formation evidence |
| E3 | AR SSM `(C,H)`/`C`/`H` state-write discovery + held transfer at two checkpoints | Signed operand controls, native logits/continuation, custody | **collected; late convolution-dominant transfer; later-query semantic assay not applicable; terminal not assessed** | Comparative evidence |
| E4 | Prospective cross-family role-graph alignment | Matched/unmatched roles, edge signs, profile errors, claim-matched null | **old post-hoc diagnostic retained; C4 earns smaller prospective state/consumer core, full graph open** | Stronger cross-family claim |
| E5 | Frozen microscopic/role profile on unopened contexts/orders | Native effects and prediction errors versus registered alternatives; no omnibus gate | **C1 collected with heterogeneous operation transfer; C2 adds final-weight dependence, chronology open** | Predictive scaffold and separate learning-origin question |
| E6 | Carried-state routing and successive semantic read/write updates | Route/read/write changes; mediated state update and later native semantic output | **historical E6/E8 mask-qualified; corrected routing on open contexts; C3 independently earns bounded serial feedback** | Stronger feedback claim |
| E7 | Checkpoint/developmental recurrence | Role/profile and native competence trajectories | **bounded Pythia-70M module collected; six real checkpoints plus final-weight shuffle; terminal not assessed** | Developmental trend; broader learning claim |
| E8 | Second-checkpoint/family replication and verifier | Raw-row bundle and family-local lowering record | **partial: second-size Mamba/Qwen plus historical thirteen-package verifier; independent-family/lab replication and public release pending** | Breadth, confidence, release |
| E9 | Outcome-free held dynamic-subcircuit compiler | Native endpoint versus operation-blind/site-matched baselines and oracle ceiling | **historical assembly precursor mask-qualified; native state assembly later measured, no learned compiler/baseline comparison** | Compiler application |
| E10 | Optional exhaustive strict four-quadrant assay | Singleton/joint necessity and sufficiency rows | **not run / optional** | Optional circuit subtype |

### First-wave execution constraints

- One mrun lease per finite lane; acquire the model once, cache immutable parents once, and batch same-shape causal arms where parity is qualified.
- Request CUDA for CUDA work and use intent-first planning unless measured history justifies an explicit reservation.
- Use strict preflight for long or shipped jobs, a queue note with physical-forward geometry and stop condition, and no automatic scientific retry that changes the specimen.
- If any lane is expected to exceed 15 minutes, obtain independent critical review of code and mrun configuration under the workspace `AGENTS.md` model preferences before the full run.
- Preserve failed, killed, cancelled, partial, and missing-output attempts as null mechanics evidence.

## Appendix B — Collation and writing tasks

| ID | Item |
|---|---|
| R1 | **Bounded audit complete in §0, §1.1, and §6:** source at layer resolution, recipient-native identity formation, late carried K/V, query-conditioned consumer, and two microscopic value routes are supported. Unique writer, individual necessary query heads, minimal route, and complete family-neutral graph remain open. Extend with new records. |
| R2 | Build the leakage ledger for all discovery priors and new holdout manifests. |
| R3 | Crosswalk E1–E3 lane outputs into the shared evidence-record schema. |
| R4 | **Current claim/evidence reconciliation complete:** Q1–Q3 and C1–C4 are integrated across abstract, definitions, results, limitations, and conclusion. Preserve the older seeded-copy calibration and E6 mask-qualified records separately; do not generalize their verdicts or rehabilitate them with new native packets. |
| R5 | Collate Mamba runtime discrepancy, native-competence denominator, conv/recurrent disagreement, and exact execution ABI. |
| R6 | Reconcile all claims with the current `space-and-time-circuits/paper.md`, not its original outline. |
| R7 | Prepare a public minimal raw-row bundle only after lane results are stable; preserve private receipts and corrections. |

## Appendix C — Source map

### Current paper and corrections

- `research/papers/space-and-time-circuits/paper.md` — current predecessor manuscript; use its updated mixed profiles.
- `research/papers/space-and-time-circuits/time-emphasis-paper.md` — formation-focused companion draft.
- `research/papers/scaffolds-and-dynamic-circuits/bridge-paper.md` — companion prose draft; the claim ledger in this outline reflects the later microscopic and formation packets.
- `research/papers/space-and-time-circuits/outline.md` — historical planning record containing claims superseded by the current paper.
- `research/papers/space-and-time-circuits/critiques/review-2026-10-01_094028_PDT.md` — claim-scope and instrument cautions.
- `research/papers/space-and-time-circuits/critiques/experiment-followup-2026-10-01_121715_PDT.md` — E20 mediation follow-up and remaining discriminants.

### Scaffold and dynamic-circuit machinery

- `saturn/docs/ROLE-PORTABILITY-ABI.md`
- `saturn/docs/ROSETTA-CIRCUIT-EXPLORER-PROPOSAL.md`
- `saturn/docs/DIFFUSION-CIRCUIT-EXPLORER-PORTABILITY.md`
- `saturn/docs/HYPERION.md`
- `saturn/src/saturn/execution_skeleton.py`
- `saturn/src/saturn/dynamic_circuit.py`
- `saturn/src/saturn/ar/role_portability.py`

### Diffusion records

- `saturn/experiments/2026-08-26-flux-cross-prompt-structural-grammar/FINDINGS.md`
- `saturn/experiments/2026-08-26-flux-rosetta-format-ontology-recurrence/FINDINGS.md`
- `saturn/experiments/2026-09-02-object-scene-source-factorial-rosetta/FINDINGS.md`
- `saturn/experiments/2026-09-02-scene-factor-edit-prep-rosetta/README.md`
- `saturn/experiments/2026-08-29-rosetta-circuit-explorer/README.md`
- `saturn/experiments/2026-09-02-flux-full-scene-compiler-rosetta/FINDINGS.md`
- `saturn/experiments/2026-09-02-scene-compiler-portability-audit/FINDINGS.md`
- `saturn/experiments/2026-09-02-prompt-agnostic-scene-compiler-rosetta/FINDINGS.md`
- `research/bfl/docs/certified-semantic-circuits/paper.md`

### First-wave implementation receipts

- `saturn/experiments/2026-10-01-scaffold-dynamic-circuits/PROTOCOL.md`
- `saturn/experiments/2026-10-01-scaffold-dynamic-circuits/diffusion/runs/panel-v1/summary.json`
- `saturn/experiments/2026-10-01-scaffold-dynamic-circuits/diffusion/runs/panel-v1/evidence-observations.jsonl`
- `saturn/experiments/2026-10-01-scaffold-dynamic-circuits/diffusion-text/FINDINGS.md`
- `saturn/experiments/2026-10-01-scaffold-dynamic-circuits/diffusion-text/runs/relation-posthoc-v1/summary.json`
- `saturn/experiments/2026-10-01-scaffold-dynamic-circuits/ar/FINDINGS.md`
- `saturn/experiments/2026-10-01-scaffold-dynamic-circuits/ar/CONTINUATION_FINDINGS.md`
- `saturn/experiments/2026-10-01-scaffold-dynamic-circuits/ar/QUERY_FACTORIAL_FINDINGS.md`
- `saturn/experiments/2026-10-01-scaffold-dynamic-circuits/ar-feedback/FINDINGS.md`
- `saturn/experiments/2026-10-01-scaffold-dynamic-circuits/ar-feedback/results/run-dade0194f43a/report.json`
- `saturn/experiments/2026-10-01-scaffold-dynamic-circuits/ar-feedback/results/run-3626c2a1b385/report.json`
- `saturn/experiments/2026-10-01-scaffold-dynamic-circuits/ar-feedback/results-qwen15/run-01c81b3f5029/report.json`
- `saturn/experiments/2026-10-01-scaffold-dynamic-circuits/ssm/FINDINGS.md`
- `saturn/experiments/2026-10-01-scaffold-dynamic-circuits/ssm/E4_ALIGNMENT.md`
- `saturn/experiments/2026-10-01-scaffold-dynamic-circuits/development/runs/panel-v7/summary.json`
- `saturn/experiments/2026-10-01-scaffold-dynamic-circuits/development/runs/panel-v7/evidence-observations.jsonl`
- `saturn/experiments/2026-10-01-scaffold-dynamic-circuits/development/runs/panel-v7/artifacts/developmental-trajectory.svg`
- `saturn/experiments/2026-10-01-scaffold-dynamic-circuits/campaign/RUN_INDEX.json`
- `saturn/experiments/2026-10-01-scaffold-dynamic-circuits/campaign/verification-receipt.json`
- `saturn/experiments/2026-10-01-scaffold-dynamic-circuits/RESULTS.md`
- `saturn/experiments/2026-10-01-scaffold-dynamic-circuits/EXECUTION.md`

### Autoregressive transformer records

- `saturn/experiments/2026-10-01-scaffold-confirmation/FINDINGS.md`
- [Confirmation run/data status and primary receipt map](evidence-status-audit-2026-10-01.md)
- `saturn/experiments/2026-10-01-scaffold-confirmation/qwen-predictive/FINDINGS.md`
- `saturn/experiments/2026-10-01-scaffold-confirmation/qwen-feedback/FINDINGS.md`
- `saturn/experiments/2026-10-01-scaffold-confirmation/cross-family/FINDINGS.md`
- `saturn/experiments/2026-10-01-scaffold-confirmation/cross-family/qwen-appendix/FINDINGS.md`
- `saturn/experiments/2026-10-01-scaffold-dynamic-circuits/ar-feedback/corrections/2026-10-01-causal-mask-audit.md`
- `saturn/experiments/2026-10-01-qwen-routing-mediation/FINDINGS.md`

- `saturn/experiments/2026-10-01-qwen-scaffold-context-poc/FINDINGS.md`
- `saturn/experiments/2026-10-01-qwen-head-edge-topology/FINDINGS.md`
- `saturn/experiments/2026-10-01-qwen-head-edge-topology/graph.json`
- `saturn/experiments/2026-10-01-qwen-formation-replay/FINDINGS.md`
- `saturn/experiments/2026-10-01-qwen-formation-replay/VM_CAPABILITIES.md`
- `saturn/experiments/2026-08-31-qwen-native-skeleton-dynamic-circuit-rosetta/README.md`
- `saturn/results/qwen-native-skeleton-dynamic-circuit-rosetta/job-a7396b9d3ba6/report.json`
- `saturn/experiments/2026-09-02-ar-prefix-compiler-rosetta/FINDINGS.md`
- `saturn/experiments/2026-09-04-coder-capability-circuit-mediation-v1/FINDINGS.md`
- `saturn/experiments/2026-09-30-full-layer-sweeps/FINDINGS-E20-mediation.md`

### State-space records

- `saturn/experiments/2026-09-03-mamba-scene-compiler-rosetta/FINDINGS.md`
- `saturn/experiments/2026-09-03-mamba-transition-source-compiler-rosetta/FINDINGS.md`
- `saturn/experiments/2026-09-30-mamba-full-layer-sweeps/`
- `saturn/experiments/2026-09-30-mvm-mamba-cot/FINDINGS.md`

### Execution and evidence contracts

- `saturn/docs/SATURN-BIBLE.md`
- `saturn/docs/EVIDENCE-PLANE.md`
- `mrun/docs/API.md`
- `mrun/docs/WORKPLAN.md`
- `obsidian/blog/2026-08-14-what-saturn-can-actually-do.md`

## Appendix D — Tool and authority map

This map states what each tool contributes and prevents a tool result from silently becoming the scientific claim. A listed tool may be prior infrastructure, a collected campaign instrument, or a proposed later instrument; the row says which.

| Tool or boundary | Purpose in this research program | Use in collected evidence | Authority limit |
|---|---|---|---|
| Saturn typed cuts, Frames/Acts/StateCuts, replay, and intervention hooks | Name family-local state boundaries, preserve parent identity, install typed interventions, and resume the unchanged program | Directly used by the E1 checkpoint/replay path and conceptually shared by the lane designs; E2/E3 use their own sealed family-local cuts | A valid cut proves mechanics and parentage, not semantic role recurrence |
| `mrun` planning and guarded CUDA leases | Plan acquisition/resources, reserve RAM/VRAM, pin genuinely host-local weights, enforce one finite outer lease, record telemetry and custody | Used for every real-model campaign panel | Admission and successful execution do not certify a causal or semantic claim |
| `mrun.diffusion.PhasePipeline` | Capture immutable native diffusion checkpoints, advance them exactly, and resume suffixes through scheduler and VAE | Used directly in E1 for step-specific scans and the cut-two factorial | Checkpoint closure proves replay fidelity; it does not prove that a selected address is unique or minimal |
| Recorder | Capture declared activations, states, addresses, and trajectories without changing the native consumer | Used in prior circuit work and represented by lane-local capture code; not a separate E1 selection authority | Recorded correlation or visibility is not causal support |
| Winder | Replay or transplant captured state under controlled common-parent continuations | Used in prior paper machinery and family-local equivalents; E1 uses PhasePipeline replay rather than claiming a new Winder result | Replay exposes an intervention effect only at the declared cut and consumer |
| Decoder | Read a represented variable or endpoint from recorded state | Used where prior records declare a decoder; E1 uses decoded native RGB instead of a learned semantic decoder | Decoder score diagnoses an instrument and cannot replace native-consumer causality |
| MRI, subspace/fingerprint tools, and generative typed-mechanism analysis | Localize candidate state, compare trajectories, propose low-dimensional payloads, and generate typed mechanism hypotheses | Supporting/prior instruments and candidates for E4–E9; not omnibus authorities in E1–E3 | Similarity, rank, energy, fingerprint agreement, or generated mechanism text is evidence about an instrument or hypothesis, never the terminal claim |
| Native VAE / LM head / autoregressive continuation | Consume intervened native state and expose image, full-vocabulary, token, or task behavior | E1 uses scheduler+VAE; E2/E3 use logits and eight-token continuation; E7 uses the full-vocabulary head; Q1–Q3 use native queries and four/eight-token continuations | Native output establishes what the model did; semantic competence and collateral require row-level interpretation. Executor token/cache recurrence alone does not establish a learned semantic feedback graph |
| `saturn-evidence` watch, claims, and xref plus source/payload custody | Preserve derived observations, watch instrument conditions, reconcile claims, resolve references, and bind immutable bytes | E1 and E7 analyzers emit report-SHA-bound observations; E2/E3 have evidence streams and receipts | Evidence-plane success means the records are present and internally linked, not that an exploratory effect passed |
| QStore checkpoint bytes | Address immutable model/checkpoint state for developmental comparisons | E7 binds steps 256/512/1000/2000/4000 through the existing QStore/source verifier, then uses the exact source weights in one FP32 HF causal runtime; not used by E1–E3 | A byte-addressed checkpoint supplies specimen identity, not developmental causality by itself; QStore is not E7's native consumer |
| Local analyzers, visual contact sheets, and permutation/random-label/site nulls | Reconstruct frozen policies, verify mechanics, preserve raw row metrics, expose images for human review, and compare against structure-destroying baselines | E1 analyzer/sheets and E7 custody/trend analyzer are complete; E4 is a post-hoc matcher; E7 includes wrong-label, fixed-site, and final-weight-shuffle controls | Analyzer summaries are additive. Raw reports and native outputs remain authoritative, and null choice must match the claim |
| Thott | Preserve transformer contextual state, token addresses, shared/append/fork ancestry, physical K/V pages, and representation residuals | Prior-paper reference; directly exercised in the separate Oct 1 Qwen formation and fresh-lease replay follow-up | Exact native restoration proves bounded executable closure. K/V representation residuals differ from the live hidden residual; storage ancestry and causal ancestry remain separate |
| `TokenMachine` / `LayerCut` | Retain and resume native token and post-layer execution, including residual and staged K/V needed by the suffix | Q3 formation cuts and the VM residual delegate use native layer execution | The source is supplied at a token address. Complete shipped durable-cut publishing/resume APIs are unexercised in these packets |
| `PayloadStore` / `LiveStateCutStore` | Persist physical payload bytes; query cold cut metadata and reopen verified state | VM residual eviction/hydration, cut query/reopen, and wrong-model refusal | Metadata alone does not supply executable closure; historical debugger cuts need the joint Thott/staged-KV bundle |
| `PagedKVCache` / `VMCache` | Share K/V pages with copy-on-write; bind typed address manifests to physical references | VM child write shares 27/28 pages and changes native logits; VMCache manifests are metadata | Paged native consumption is measured. Manifests do not imply physical CUDA VMM, semantic address resolution, or a transparent all-tensor pager |
| Saturn debugger controller/session | Break, watch, inspect, preview, abort, commit, restore, and replay state interventions | VM packet uses an experiment-local callback adapter backed by native LayerCuts; clean and zeroed residuals replay exactly | Generic shipped Qwen residual support is not claimed; numerical replay and chain-fingerprint equality are distinct |
| `CausalContextVM` / `CircuitRuntime` | Model a reusable transaction-state session that resumes through the native neural consumer | Prior-paper runtime reference only; current lanes use their sealed family-local runtimes | A reusable runtime contract establishes execution semantics, not learned role recurrence or cross-family identity |
| SAELens, Gemma Scope, and transcoders | Supply public sparse-feature and transcoder instruments for comparison with causal role discovery | Related prior-paper instruments; not used in the current campaign | Feature labels and reconstruction quality are instrument evidence. They do not replace same-parent interventions or native-consumer effects |
