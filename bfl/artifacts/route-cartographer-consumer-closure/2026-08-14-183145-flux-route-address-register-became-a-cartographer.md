---
title: The FLUX Route Address Register Became a Cartographer
subtitle: Turning one joint Saturn capture into typed addresses, temporal graphs, and a plan for learned route discovery
author: codex
type: blog
subtype: saturn-flux-route-address-cartography
date: 2026-08-14
created: 2026-08-14T18:31:45-07:00
updated: 2026-08-14T20:33:37-07:00
timestamp: 2026-08-14T18:31:45-07:00
status: exploratory-report-and-fresh-route-confirmation
claim_status: fresh whole-edge consumer closure confirmed; selected local QKV proposals fail sufficiency/specificity; no terminal semantic-circuit claim
epistemic_status: Measured one-seed FLUX evidence, a complete multidomain Saturn panel, four fresh route-confirmation replicates, sealed foretelling, a persistent future forest, graph surrogates, weak labels, and explicit ABI limits are separated.
tags:
  - blog
  - saturn
  - flux
  - flux2
  - black-forest-labs
  - bfl
  - source-addressing
  - temporal-graphs
  - graph-algorithms
  - route-discovery
  - capability-discovery
  - model-os
  - ouroboros
  - qkv
  - consumer-closure
  - neural-programs
  - reversible-training
  - trend-first
related:
  - "[[./2026-08-14-203337-the-carrier-was-real-the-address-was-not-yet-a-program|The Carrier Was Real; the Address Was Not Yet a Program]]"
  - "[[../../saturn/docs/LEARNED-SOURCE-ADDRESSING|Learned Source Addressing]]"
  - "[[../../saturn/docs/MODEL-OS-API|Model OS API]]"
  - "[[../../saturn/docs/CAPABILITY-CARTOGRAPHER-ROADMAP-RESULTS|Capability Cartographer Results]]"
  - "[[../../saturn/docs/TEMPORAL-INSTRUMENTATION-MATRIX|Temporal Instrumentation Matrix]]"
  - "[[2026-08-14-155749-saturn-model-os-and-semantic-memory-bus-survey|Saturn's Model OS and Semantic Memory Bus]]"
source_artifacts:
  - saturn/results/joint-token-route-capture/job-3e0dfeb83996/report.json
  - saturn/results/joint-token-route-capture/job-3e0dfeb83996/qkv-source-rows.pt.gz
  - saturn/results/flux-route-address-register/job-3e0dfeb83996/build-receipt.json
  - saturn/results/flux-route-address-register/job-3e0dfeb83996/route-address-surface.json
  - saturn/results/flux-route-address-register/job-3e0dfeb83996/temporal-route-graph.json
  - saturn/results/flux-route-address-register/job-3e0dfeb83996/route-register.json
  - saturn/results/flux-route-address-register/job-3e0dfeb83996/capability-spec.json
  - saturn/results/flux-route-address-register/job-3e0dfeb83996/capability-ir.json
  - saturn/configs/flux-route-cartographer-capture.json
  - saturn/results/flux-route-cartographer-capture/job-c2afd4eb1044/report.json
  - saturn/results/flux-route-cartographer-capture/job-c2afd4eb1044/qkv-source-rows.pt.gz
  - saturn/results/flux-route-cartographer/selector-report.json
  - saturn/results/flux-route-cartographer/source-address-policy.json
  - saturn/results/flux-route-cartographer/selector-state.pt
  - saturn/experiments/2026-08-14-flux-route-cartographer/foretell_forest.py
  - saturn/results/flux-route-cartographer-v5/foretelling-forest-report.json
  - saturn/results/flux-route-cartographer-v5/foretelling/cross-context.json
  - saturn/results/flux-route-cartographer-v5/foretelling/role-local-predictions.json
  - saturn/results/flux-route-cartographer-v5/future-forest/manifest.json
  - saturn/configs/flux-multidomain-route-capture.json
  - mstack/experiments/diffusion_multidomain_route_capture_probe.py
  - saturn/workers/submit_saturn_joint_token_route_capture.py
  - saturn/results/flux-multidomain-route-capture/job-88e6850defb4/job-88e6850defb4/report.json
  - saturn/results/flux-multidomain-route-capture/job-88e6850defb4/job-88e6850defb4/qkv-source-rows.pt.gz
  - saturn/results/flux-multidomain-route-capture/job-88e6850defb4/job-88e6850defb4/run-receipt.json
  - saturn/results/flux-multidomain-cartographer-v3/multidomain-cartographer-report.json
  - saturn/results/flux-multidomain-cartographer-v3/route-signatures.json
  - saturn/results/flux-multidomain-cartographer-v3/foretelling/leave-one-domain-out.json
  - saturn/results/flux-multidomain-cartographer-v3/foretelling/sealed-predictions.json
  - saturn/results/flux-multidomain-cartographer-v3/future-forest/manifest.json
  - saturn/configs/flux-route-confirmation.json
  - mstack/experiments/diffusion_route_confirmation_probe.py
  - saturn/workers/run_saturn_route_confirmation.py
  - saturn/workers/submit_saturn_route_confirmation.py
  - saturn/results/flux-route-confirmation/job-bfe2e3d01563/report.json
  - saturn/results/flux-route-confirmation/job-bfe2e3d01563/run-receipt.json
  - saturn/results/flux-route-confirmation/job-bfe2e3d01563/confirmation-analysis.json
  - saturn/results/flux-route-confirmation/job-bfe2e3d01563/confirmation-analysis.md
---

# The FLUX Route Address Register Became a Cartographer

> [!summary] We took one corrected Saturn capture of FLUX.2 Klein 4B and lowered it into a typed route-address surface, a TemporalRouteRegister, two complementary graph projections, and a CapabilitySpec/CapabilityIR. The result is not yet a semantic circuit detector. It is more useful than that phrase suggests: it is the first durable control-plane map on which a learned route cartographer can be trained and tested.

## The short version

The question was whether a token can be understood as a route address rather than as an isolated symbol. The answer from this first panel is a qualified yes.

The address of a source is not just a token ID. It is closer to:

```text
model + context + semantic role + token span + position
  + transformer site + denoising step + Q/K/V stream
```

The same raw `red` token at the subject position and the lighting position is therefore allowed to be two different addresses. A retokenized word is represented as a span, not forced into a single token slot. The payload is kept separate from the address: Q/K can participate in routing, while V or a residual state can carry the recipient-local content. That separation is a design contract, not yet a proof that the model implements exactly that division.

The current artifact enumerates 324 candidate coordinates. It does not select one. It gives Saturn a stable surface over which selection, intervention, replay, and abstention can be defined.

## The specimen and the capture

The source was one corrected, one-parent Saturn run:

- FLUX.2 Klein 4B;
- one seed, 7217;
- one prompt family;
- 256×256 resolution and four denoising steps;
- 25 route sites, from `joint.0` through `single.19`;
- native base, subject-token, lighting-token, and retokenized-subject conditions;
- 50 site interventions and 31 QKV interventions.

The panel included same-token/different-role comparisons, different-token/same-role comparisons, retokenization, source deltas, wrong-source writes, position swaps, and exact zero-dose controls. The raw Q/K/V rows remain in a compressed sidecar; the derived register does not copy tensor payloads into its JSON metadata.

This distinction matters. The old failure mode was to make a pretty route diagram from a scalar activation difference. The new capture keeps the producer, address, carrier, consumer, intervention, and control visible as separate objects.

## We ran the cartographer

The proposal is no longer only a design sketch. We submitted a second one-lease Saturn capture, `job-c2afd4eb1044`, with an opt-in cartographer surface. It retained the full active text K matrix at `joint.2`, `joint.3`, and `joint.4`, plus role-scoped Q and V rows for all four conditions and four denoising steps. The original capture remains immutable; this is a new sidecar with schema `saturn-flux-route-cartographer-surface-v1`.

On that cached surface we trained a 204,322-parameter composite: the existing permutation-equivariant `SourceAddressPolicy` selected a token address, and a small 10-feature temporal head ranked nine site/QKV route candidates. The address labels were used only as discovery supervision; the route effect targets came from the native return-register/RGB closure measurements already recorded by the capture. The route head was evaluated on a held-out site (`joint.4`), while the address head was held out on the retokenized `scarlet` condition.

The result separates two claims cleanly:

| measurement | result | interpretation |
|---|---:|---|
| retokenized held-out address coverage | 1.00 | the selected address landed inside the two-token `scarlet` span in all 72 rows |
| candidate-order permutation invariance | 1.00 | the address policy did not depend on candidate ordering |
| random-key/native address agreement | 0.056 | the selection is not reproduced by random candidate geometry |
| held-out-site consumer-closure score | 0.977 | the weak route-effect predictor did not improve over its 0.990 baseline |
| exact rollback controls | 5/5 receipts verified | rejected selector futures restored the accepted state exactly |

The address result is strong for this bounded panel, but it is not semantic discovery: the target span came from the capture's controlled locus metadata. More importantly, the route head exposed a failure instead of hiding it. It ranked `joint.4/v` highest for the held-out retokenized case. The native consumer table says that the strongest observed route differs by role—approximately `joint.3/v` for the subject-color source and `joint.2/v` for the lighting-color source. Later updates that failed the frozen-consumer score were restored by Saturn, and an intentional negative rollback probe was also restored exactly.

That is already a useful cartographer: it can propose a typed source address and tell us when its route-effect forecast is not earned. The next selector must learn from richer payload/QKV geometry and use a context-held-out route-effect split; a high address score cannot be allowed to promote a bad consumer forecast.

## Foretelling made the cartographer respect the transfer boundary

The first portable foretelling pass pooled the subject and lighting roles. That was a useful negative result: its unopened-group harmful AUC was only 0.50 when subject-trained predictions were transferred to lighting, and 0.556 in the reverse direction. A single global route-effect law was too eager to treat two different local programs as one.

The repair is small but important. We fit two clock- and identity-blind portable forecasters over the temporal Q/K geometry—Q/K maximum similarity, temporal variability, attention entropy, query and key norms, and QKV-kind indicators—but keep the semantic transfer cells separate:

```text
subject_token  →  retokenized subject span
light_token    →  retokenized light role
```

Predictions were sealed before the retokenized consumer outcome was opened. The pooled comparator ranked `joint.2/v` for both roles. The role-local forecasters instead proposed:

| unopened role | sealed top route | forecast | native role maximum in the source panel |
|---|---|---:|---:|
| retokenized subject | `joint.3/v` | 0.116 | `joint.3/v` at 0.203 |
| retokenized light | `joint.2/v` | 0.140 | `joint.2/v` at 0.199 |

This agreement is a trend, not a held-out retokenized proof—the native closure labels come from the same small capture. It does show that the correct unit of transfer is not “all routes in the model.” It is the role-conditioned route program plus its tokenization change.

The [role-local foretelling and forest report](../../saturn/results/flux-route-cartographer-v5/foretelling-forest-report.json) now stores every proposal in a content-addressed [Future Forest](../../saturn/results/flux-route-cartographer-v5/future-forest/manifest.json): 18 route futures (nine Q/K/V candidates for each role), 20 observations, 19 decisions, and one combined promoted head. Closure verification passed after reopening the forest. The promoted future contains `subject_color/joint.3/v` and `light_color/joint.2/v`; all sibling proposals remain available for native replay.

Before promotion, the forest attached a native frozen-consumer audit to the combined head. The selected source-role routes scored 0.203 and 0.199, for a mean of 0.201 and a positive minimum. That gate passed, but it only validates the source-context analogue; the retokenized consumer outcome stayed sealed.

That makes the forest operational rather than decorative. Foretelling proposes a future from unopened evidence. The forest retains the alternatives and their provenance. A frozen-consumer replay can now promote, retain, or rewind the proposal without erasing why the alternatives were rejected. The route remains a scheduling hypothesis until that replay is run.

## The cartographer leaves the color toy

The next capture widened the panel deliberately. The question was no longer whether the machinery could distinguish two occurrences of `red`; it was whether the same route-address machinery could organize several kinds of controlled change while keeping tokenization, context, and consumer effects separate.

The complete [multidomain Beast capture](../../saturn/results/flux-multidomain-route-capture/job-88e6850defb4/job-88e6850defb4/report.json) used one resident FLUX.2 Klein 4B process, one seed, one prompt family, 250 in-process branches, and 140.5 seconds of wall time. It produced 175 consumer-closed site interventions, 54 native source-delta Q/K/V interventions, nine wrong-source controls, three position swaps, one exact zero-dose control, and a full Q/K/V cartographer surface at `joint.2`, `joint.3`, and `joint.4`.

| condition | controlled change | target span |
|---|---|---|
| `subject_color_blue` | subject `red` → `blue` | position 7, one token |
| `light_color_blue` | lighting `red` → `blue` | position 17, one token |
| `object_identity_cat` | `fox` → `cat` | position 8, one token |
| `action_running` | `sitting` → `running` | position 9, one token |
| `scene_grass` | `snow` → `grass` | position 12, one token |
| `time_night` | `dawn` → `night` | position 14, one token |
| `retokenized_subject` | subject `red` → `scarlet` | positions 7–8, two tokens; held out |

The first two rows are the critical same-token/different-context control. The middle four are different-token/same-role probes. The final row is the tokenization transfer test: `scarlet` expands the subject span and shifts every later text position by one. The [raw Q/K/V sidecar](../../saturn/results/flux-multidomain-route-capture/job-88e6850defb4/job-88e6850defb4/qkv-source-rows.pt.gz) keeps those spans explicit rather than pretending that a two-token word is one address.

### Native route signatures are not one universal route

For each native domain, the capture gives a 9-route source-delta closure vector over `joint.2/3/4 × Q/K/V`. The closure label is the same deliberately weak paired authority used above: `0.6 × return-register alignment + 0.4 × RGB alignment`. It is a route-effect label, not a semantic truth label.

The robust native panel rank selected `joint.2/v`: mean closure `0.233`, with the weakest domain still at `0.075`. `joint.3/v` was close behind at mean `0.206` and worst-domain `0.075`. The domain-specific maxima were different:

| domain proxy | strongest native route | closure |
|---|---|---:|
| subject color | `joint.2/v` | 0.084 |
| lighting color | `joint.2/v` | 0.218 |
| object identity | `joint.3/v` | 0.493 |
| action | `joint.2/v` | 0.250 |
| scene | `joint.4/v` | 0.214 |
| time | `joint.2/v` | 0.376 |

The exploratory route-signature clustering found three families: the two color contexts grouped together; object, action, and time grouped together; and scene was a singleton. That is useful as a proposal for the next probe battery, not as a claim that “object,” “action,” and “time” share a semantic program. The cluster is made from nine measured consumer effects in one prompt family. Still, it is exactly the kind of intermediate representation needed between raw tokens and a higher-level capability: a route signature says what a candidate address does before anyone names what it means.

The controls support the instrument. Zero dose produced zero return and RGB alignment. The native source-delta panel averaged `0.100` return alignment and `0.088` RGB alignment, while the wrong-source control averaged only `0.065` and `0.036`. Position swaps averaged `0.040` return alignment but `-0.098` RGB alignment. These are trends over small controls, not terminal specificity claims, but they are materially different from treating every residual movement as a route.

### The held-out retokenized path is visibly temporal

The held-out `scarlet` condition was replayed through every one of the 25 text-stream route sites after the foretelling boundary. This is separate from the sealed QKV proposal: the site replay measures a whole text-stream replacement at each edge, while the native QKV source-delta ABI expects equal-length source and target spans.

The consumer-closed site trace is strikingly structured. Mean closure across all 25 sites was `0.592`; `joint.0` was `0.999`, `joint.2` was `0.977`, and `joint.4` was `0.960`. The signal then decayed through the single stream: `single.12` was `0.451`, `single.18` was `0.104`, and `single.19` was exactly `0.000`. Of the 24 adjacent route transitions, 79.2% were decreases.

That is evidence for a temporal carrier corridor in this specimen. It is not evidence that every edge is a necessary circuit edge, and it is not the same as saying that the held-out `joint.4/v` QKV intervention has been consumer-closed. The retokenized QKV source-delta is explicitly recorded as one skipped branch because the native subject span has length one and `scarlet` has length two. The honest next instrument is a span-aware QKV intervention—pooling or aligning the two source subtokens—rather than silently dropping one token or broadcasting it and calling that a causal result.

### Foretelling sees the transfer boundary

The portable ridge forecaster was fit only on the 54 native QKV closure rows. Leave-one-domain-out errors ranged from `0.072` to `0.144` MAE across nine-route test cells; harmful AUC ranged from `0.375` to `1.000` where both positive and non-positive cells existed. The sample is too small for those figures to be a performance claim, but the variation is informative: a single feature ABI does not erase domain differences.

For the unopened retokenized QKV future, three forecasts disagreed:

| frozen predictor | sealed top route |
|---|---|
| subject-role local | `joint.4/v`, forecast `0.064` |
| color-pooled | `joint.4/v`, forecast `0.115` |
| all native domains | `joint.2/v`, forecast `0.173` |

This disagreement is not a bug to average away. `joint.2/v` is the robust native panel consensus; `joint.4/v` is the same-role tokenization-transfer proposal. The held-out site trace says both joint locations carry substantial whole-stream effect, but it cannot adjudicate their QKV-specific consumer closure. The [multidomain analysis report](../../saturn/results/flux-multidomain-cartographer-v3/multidomain-cartographer-report.json) keeps those authorities separate.

The [expanded Future Forest](../../saturn/results/flux-multidomain-cartographer-v3/future-forest/manifest.json) retains 54 native route observations, nine sealed held-out QKV futures, and the complete 25-edge held-out site audit. It closed with 66 nodes, 66 observations, 65 decisions, and 70 content objects; reopening verified the same closure. Its selected `joint.4/v` proposal was promoted only against a positive native subject-color source audit. The retokenized QKV outcome is still unopened, so this promotion means “schedule this future for the next replay,” not “the retokenized capability has been proven.”

### What changed in the capability picture

The result supports a more precise hierarchy:

```text
token span + context
  → role-conditioned address
  → temporal route signature
  → carrier/payload behavior
  → consumer-closed program
  → higher-level capability composed from several programs
```

The route signature is the useful middle layer. It is richer than a color label and smaller than a claim such as “understands lighting” or “knows how to write an application.” Object identity, action, scene, time, and color can all invoke the same low-level transport machinery while producing different route-effect vectors. Conversely, two prompts with the same word can select different role-conditioned addresses. A capability label should be assigned only after this intermediate signature survives new contexts, tokenizations, seeds, and consumer tests.

The next Saturn run is now clear: implement span-aware QKV source writes, replicate the six-domain panel across seeds and prompt families, and use the observed site trace as a frozen-consumer target for a small permutation-equivariant selector. Active graph selection, spectral route clustering, and temporal factorization can reduce the next search; they must schedule informative interventions, not substitute for consumer closure. The cartographer has left the color toy, but it has not yet earned semantic names for the terrain.

## What the Model OS lowering produced

The [route-address surface](../../saturn/results/flux-route-address-register/job-3e0dfeb83996/route-address-surface.json) contains the candidate coordinates. The [TemporalRouteRegister](../../saturn/results/flux-route-address-register/job-3e0dfeb83996/route-register.json) contains the typed history. The [temporal graph](../../saturn/results/flux-route-address-register/job-3e0dfeb83996/temporal-route-graph.json) contains the route projections. The [build receipt](../../saturn/results/flux-route-address-register/job-3e0dfeb83996/build-receipt.json) binds them to the immutable source artifacts.

The register contains:

- 685 states;
- 85 logical branches;
- 325 observations;
- explicit causal lineage separate from storage ancestry;
- content-addressed links to the report, run receipt, and QKV sidecar.

The structural graph has 56 nodes and 54 ordered edges. It represents two role-conditioned route chains, each with a source, 25 carrier sites, and two native consumers: the return register and the RGB readout.

The [CapabilitySpec](../../saturn/results/flux-route-address-register/job-3e0dfeb83996/capability-spec.json) names the current working hypothesis `flux.role-conditioned-route-transport`:

> A contextual source role selects a typed temporal route and carries a recipient-consumable QKV/residual program through the frozen FLUX denoising suffix.

This is deliberately a lower-level capability. It is not “understands color,” “draws a fox,” or “understands lighting.” Those are larger programs that may compose many route-transport primitives.

The [CapabilityIR](../../saturn/results/flux-route-address-register/job-3e0dfeb83996/capability-ir.json) is even more conservative. It defines the interface—source role, address result, payload intent, and consumer test—but contains no hidden tensor, payload binary, or cross-family tensor reuse.

## Why both flow and cut are useful

There are two graph questions, and collapsing them into one score loses the mechanism.

### Parallel route support

The parallel projection treats each site intervention as a separately measured route candidate and weights it by downstream alignment to the donor consumer. It is a route-redundancy measure. The normalized route entropy ranges from roughly 0.975 to 0.994, so this panel does not look like one uniquely isolated address. Early `joint.0` is strongest, but many sites retain substantial closure.

This is not literal simultaneous flow. The capacities are not probabilities, and summing them does not mean that all routes are active at once. It means that several individually tested addresses can produce similar consumer-facing effects.

### Serial temporal corridor

The serial projection treats the ordered sites as a surrogate carrier corridor. Its max-flow/min-cut therefore reports the weakest measured consumer-closure handoff among the active sites:

| role | consumer | bottleneck | corridor capacity |
|---|---|---|---:|
| subject color | return register | `single.18` | 0.114 |
| subject color | RGB | `single.18` | 0.374 |
| lighting color | return register | `single.18` | 0.299 |
| lighting color | RGB | `single.18` | 0.455 |

The zero at `single.19` is not treated as a failed route. That site has no downstream text consumer, so the graph explicitly excludes it from the active corridor and records the reason.

The correct interpretation is “`single.18` is the weakest measured late handoff in this panel,” not “`single.18` is a proven necessary circuit edge.” A necessity claim still requires ablation, replacement, dose-response, replication, and continuation.

## What the data says about tokens and routes

The address surface makes the main result visible: token identity is one feature among several, not the route itself. The same `red` ID appears under two role-conditioned addresses. The retokenized `scarlet` span expands the address space instead of being coerced into the `red` coordinate.

The QKV comparison points in the same direction. The same raw token across the subject and lighting roles has much lower average row similarity than the same-role red-to-blue changes. That is evidence for contextualized, role-conditioned state—not proof that the model has a clean semantic “redness” register.

The intervention controls are more informative than the raw similarity. A subject source delta at `joint.3` reaches RGB with alignment about 0.213. A wrong lighting source written into the subject path at `joint.3` reaches only about 0.068. A position swap at the same joint site reaches about 0.002. These are exactly the kinds of contrasts a route learner should consume.

## The limits of the current map

The map is bounded by what the capture retained. It enumerates the supplied 25 sites, three QKV sites, four steps, and four conditions. It still does not discover arbitrary temporal graphs from raw model execution. The new cartographer sidecar does, however, retain the full active text K matrix and role-scoped Q/V rows needed for a first address selector; that was the decisive missing instrument in the earlier artifact.

The selector therefore searches every captured text position at its declared route sites, but not every possible layer, stream, checkpoint, prompt, or temporal graph. Its address supervision is also controlled-locus supervision, not a proof that the network independently inferred the word's meaning.

The current capability inventory is 24/29 observables, or 82.8%, across seven edges. The two open edges are:

- dose-response for the full route-to-RGB handoff;
- simultaneous subject/light composition, overlap policy, continuation, and collateral behavior.

Those gaps are not administrative. They define the next experiment.

## Can graph mathematics improve this?

Yes, but different algorithms should answer different questions.

| Method | What it adds | First use |
|---|---|---|
| Dynamic tensor factorization | Finds route atoms across context × site × step × QKV × consumer | Separate shared transport from role-specific transport |
| Spectral clustering / diffusion maps | Finds soft route communities without forcing one hard label | Cluster addresses before semantic naming |
| Dynamic Bayesian networks or HMMs | Models route continuity and state transitions across steps | Distinguish a stable route from independent site effects |
| Intervention-aware Shapley/Owen values | Estimates marginal and interaction contributions | Measure overlap between subject and lighting Acts |
| Submodular or DPP probe selection | Chooses maximally informative next interventions | Avoid brute-forcing every address combination |
| Optimal transport | Aligns tokenized spans and route distributions | Compare `red`, `blue`, and retokenized `scarlet` |
| Persistent/zigzag homology | Tracks route topology across dose and checkpoint | Detect route birth, merger, and disappearance |
| Set/graph neural networks | Learns permutation-aware route ranking | Automatic address discovery after richer capture |

The first three additions should be tensor factorization, temporal state modeling, and active probe selection. Persistent homology is interesting, but it should come after the basic route identity and consumer labels are reliable. Fancy topology cannot repair a missing consumer boundary.

## Can a small model discover and label routes?

Yes. The model should not begin by predicting words such as “math” or “music.” That would encourage semantic overclaiming and make the label vulnerable to prompt leakage. It should learn three more basic outputs:

1. **Address distribution:** which typed candidate coordinate should be selected, or whether to abstain.
2. **Consumer forecast:** what return-register, RGB, continuation, and collateral effects the selected route is expected to produce.
3. **Route embedding:** a compact representation that can be clustered into route families.

The architecture can remain small:

```text
query state + role/context features
  → shared candidate scorer (SourceAddressPolicy)
  → temporal encoder over site/step/QKV candidates
  → address distribution + abstention
  → consumer-effect heads + route embedding
```

The first implementation can be a FLUX-local extension of the existing permutation-equivariant `SourceAddressPolicy`, with a small GRU or Set Transformer over the temporal candidate set. Q/K rows are candidate address features; V/residual rows remain a separate payload path. The selector must be permutation-equivariant over candidates and explicitly represent token spans, relative position, site, step, stream, and role.

The executed first implementation used the existing `SourceAddressPolicy` directly and paired it with a small MLP route head. It consumed full candidate K rows, role-specific Q rows, route site, step, Q/K geometry, and QKV kind. It selected the same role-conditioned address across denoising steps and generalized from one-token colors to the two-token `scarlet` span. The candidate-shuffle control was exactly invariant, which is an important sanity check for a set-valued address surface.

The first route-effect head was intentionally simple, and the result shows why the consumer head must remain authoritative. Its held-out score fell from 0.990 to 0.977 and its top route disagreed with the native closure ranking. Saturn's lexicographic policy promoted the first update because address accuracy improved, then rejected three later updates on the consumer endpoint; all rejected intervals restored the prior state exactly. For the next version, route-effect closure must be a non-negotiable promotion objective (or a Pareto constraint), not a secondary diagnostic after address accuracy.

The training target should be a vector, not a single semantic label:

```text
ranking loss
+ consumer-closure regression
+ temporal consistency
+ wrong-source / shuffled-source contrastive loss
+ tokenization and candidate-permutation invariance
+ sparsity or group regularization
+ calibrated abstention
```

Consumer closure supplies weak route labels. It does not supply semantic truth. A route label such as `subject-color/late-joint-v` should initially mean “this address family produces this measured consumer signature.” A higher-level label such as “lighting” should be assigned only after a heldout probe battery shows selective behavior across new prompts and controls.

Ouroboros already has the right conceptual separation: route discovery produces candidates, a behavioral fingerprint records use-case signatures, and a circuit assay requires sufficiency, necessity, specificity, continuation, and replication before certification. The learner should feed that pipeline; it should not bypass it.

## How Saturn should train it

This is a good Saturn experiment because the mutable object can be tiny and the consumer can stay frozen.

### Phase A: enrich the capture

At the same FLUX boundary, retain:

- the recipient query state;
- full candidate Q/K address keys for the declared token span or candidate set;
- V/residual payload rows separately;
- relative positions and span masks;
- route/site/step identity;
- consumer effects for top candidates and controls;
- prompt, seed, tokenization, and checkpoint split fingerprints.

The candidate surface must be broader than the teacher's chosen row. Otherwise the selector only learns to reproduce the supplied address.

### Phase B: train a small selector on cached evidence

Train only the selector and effect heads. Keep the FLUX model and native suffix frozen. Use Saturn's deterministic checkpoint controller so every short update interval captures parameters, optimizer, RNG, cursor, and module state. Bad selector updates must be restorable exactly.

Use discovery data for fitting, a feedback-monitor split for candidate promotion, and sealed prompt/seed splits for heldout and terminal evaluation. Do not call consumer labels label-free if those labels enter the optimizer.

### Phase C: future-peek through the native consumer

For each candidate selector update, replay a small batched panel through one resident FLUX process:

- native branch;
- learned top-1 and top-k routes;
- oracle route;
- wrong-source and wrong-address routes;
- norm-matched random route;
- shuffled candidate order;
- exact zero-dose and uninstall branches.

Measure local address accuracy, route selectivity, return-register closure, RGB closure, continuation, collateral, and repair. Promote only a candidate that improves the declared vector under the explicit policy; otherwise rewind exactly and retain the rejected future as evidence.

This should be one mrun lease with one resident model load and in-process logical branches. Saturn is most valuable here as a reversible feedback controller, not as a conventional epoch wrapper.

The first run followed that pattern for the capture: one resident FLUX process, 85 in-process branches, and no per-branch scheduler submissions. Selector fitting then stayed model-free on the immutable sidecar, but it still used Saturn's checkpoint controller. That division is useful: the expensive model lease supplied future consumer evidence once, while the cheap selector search could be rewound repeatedly without reloading FLUX. The failed route head is therefore preserved as negative evidence rather than silently tuned away.

## What would count as success?

The first success criterion is not a semantic label. It is a selector that, on heldout contexts, chooses a route whose frozen consumer signature beats random, shuffled, and wrong-source controls while preserving exact zero-dose and uninstall behavior.

The second is route-family stability: the learned embedding clusters the same role-conditioned program across prompts, seeds, and tokenizations better than raw token identity does.

Only then should we ask whether a cluster deserves a label such as “subject-color transport” or a higher-level capability name. A label is a hypothesis about use, backed by a probe battery—not a name pasted onto an activation cluster.

## The next experiment

The smallest informative next run is therefore not a giant graph sweep. It is:

1. one FLUX checkpoint and seed;
2. two roles, one tokenization contrast, and a small candidate span;
3. full query/key/payload capture at three QKV sites and four steps;
4. a small permutation-equivariant selector with a separate, consumer-constrained route head;
5. top-k, wrong-source, shuffle, random, zero-dose, and uninstall controls;
6. one frozen RGB/return-register suffix;
7. short reversible selector updates with exact Saturn rollback;
8. a context-held-out route-effect split, with payload/V geometry and temporal interactions added to the selector input.

The first pass has now completed items 1–7 and passed the address/rollback mechanics, while failing to earn route-effect prediction. The next pass must make the consumer endpoint decisive before promotion. If it works, the route register stops being only a map of a known terrain. It becomes a cartographer: a small learned system that proposes where to look, Saturn checks what the route does, and the frozen consumer decides whether the proposed program is real.

That is the path from token traces to discoverable neural programs without pretending that a graph cluster is already a capability.

## The fresh confirmation: the carrier is real, the local address is not yet portable

The full methods-and-findings write-up is now in [The Carrier Was Real; the Address Was Not Yet a Program](./2026-08-14-203337-the-carrier-was-real-the-address-was-not-yet-a-program.md).

We then ran the decisive follow-up: two fresh prompt families, two fresh seeds, and four proposed route addresses from the cartographer:

| proposed route | fresh QKV test | result |
|---|---|---|
| subject color | `joint.2/V` | donor-side ablation effect, but no sufficiency or specificity |
| object identity | `joint.3/V` | donor-side ablation effect, but no sufficiency or specificity |
| scene | `joint.4/V` | donor-side ablation effect, but no sufficiency or specificity |
| time | `joint.2/V` | donor-side ablation effect, but no sufficiency or specificity |

The result is a useful correction to the original picture. Whole text-state transfer closed at every freshly probed joint edge (`joint.0` through `joint.4`); the weakest mean return-register alignment was still 0.911. But replacing only the selected token's local `V` state did not reproduce the donor capability on the fresh contexts. Endpoint return alignment averaged 0.001 for subject color, 0.227 for object identity, 0.105 for scene, and 0.197 for time. None met the bounded 0.50 consumer sufficiency gate, and none beat the Q/K, wrong-source, and norm-matched sham controls by the required margin.

The donor-side ablations did move the native consumer: mean return-progress loss was 0.151, 0.424, 0.222, and 0.288 for those same four domains. That combination—necessity trend without transfer sufficiency—is exactly what a coalition or context-conditioned route should look like. The proposed address participates in the computation, but it is not the whole program. The missing carrier may include attention routing, a span, multiple Q/K/V projections, residual state, and the temporal handoff between sites.

So the graph picture survives, but its node type changes. A colored node such as `joint.2/V` is a candidate coordinate, not a capability. The transferable object is more likely a typed temporal subgraph:

```text
token span + role/context
  → Q/K routing coalition
  → V/residual payload
  → joint-site relay
  → native consumer
```

The [fresh raw report](../../saturn/results/flux-route-confirmation/job-bfe2e3d01563/report.json) and [artifact-only analysis](../../saturn/results/flux-route-confirmation/job-bfe2e3d01563/confirmation-analysis.md) keep the positive edge-closure evidence and the failed local-QKV gates side by side. The next experiment should therefore search and intervene on span-aware temporal coalitions, not promote a single QKV address merely because it ranked highly on one capture.
