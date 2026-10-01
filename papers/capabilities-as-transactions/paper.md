---
title: "Capabilities as Support-Aware Transactions: The Final Boss Is a Role, Not a Layer"
type: research-paper
status: draft
date: 2026-08-28
updated: 2026-09-30
tags: [interpretability, circuits, causal-mediation, kv-cache, diffusion, language-models, transactions, blind-discovery]
---

# Capabilities as Support-Aware Transactions: The Final Boss Is a Role, Not a Layer

**A cross-family account of behaviors carried as addressed, time-accumulated key/value transactions and committed by an unchanged native consumer — with the controls that partly fail, the claims that were retracted, and a blind auto-detection trial that produced a trend without a certificate**

Jacob Hollenbeck

*2026-08-28; revised 2026-09-30*

> Every number in this paper is measured. Bundled receipts are cited by path; receipts that live only in the private experiment store are cited by job ID and marked as such. Job IDs are retained in this public release by the author's choice.

---

## Abstract

We set out to find "the final boss": the single late circuit that commits a model's output. We did not find one, and the way it failed is the result. Across a production diffusion transformer and several autoregressive language models, the object that commits a behavior is not a layer, a vector, or a fixed integral. It is a **transaction**: context establishes a route and a recipient-local address; native computation forms or commits an executable state; that state is carried across depth or denoising time in the residual and key/value cache; a recipient transition and an output protocol expose it; and an **unchanged native consumer** — the model's own next-token head, or its own scheduler and decoder — turns it into behavior and a continuation. The "final boss" survives only as the **terminal consumer role** at the end of that chain, not as an anatomical location. We define the transaction and its four-quadrant certificate, and report evidence across behavior families with denominators: a twenty-axis diffusion route panel (6 of 20 strict, 11 of 20 carrier-certified, 3 of 20 candidate, two seeds); a two-seed scene-edit certificate; a cross-family portability trend across three checkpoints of one diffusion family and a cross-family conditioner; an autoregressive key/value causal chain in a 7B code model in which cross-position joint key/value installs the behavior (4 of 4) while key-only and value-only writes do not (0 of 4 each); the distributed-store sink grid from a companion paper; and a certified induction circuit in a public 70M model whose whole-model loss account we complete this week. We state plainly how this differs from classic static circuits — time accumulation, cross-position joint key/value, a separation between formation and protocol, non-monotone dose basins, and authority bound to the consumer — and we are explicit about the leaks: key/value chain controls that only partly pass (joint-row-shift installs the behavior 4 of 4 but reproduces the full continuation only 2 of 4; a row-permuted residual passes 4 of 4); a terminal claim that is *false* and a bounded-chain candidate that is *False* in the cleanest autoregressive case; every cell has n = 4; a fitted "clock" controller that was retracted under audit; and instance binding that is not established. A blind route-discovery instrument, given the carrier interface and consumer but not the route coordinates, rediscovered the diffusion route's target edges (3 of 3) but recovered only 1 of 3 under a wrong-depth control, and on a language model returned a trend without a certificate (0 certificate observations; the winning window fails single-site-necessity-share at 0.44 against a 0.25 bar and wrong-depth address-specificity at 0.63 against a 0.5 bar). We close on what the transaction view does and does not answer: it explains what moved where and to which consumer; it does not explain why attention attended there.

## 1. From a layer to a role

Interpretability's working image of a capability is often a small set of components — heads, features, a subgraph — that computes a function, localized enough that ablating it hurts and inserting it helps. We hunted for that object in its strongest form: a single late circuit that commits the output, a "final boss." The hunt failed in the productive sense. There is no universal late layer whose blind ablation removes a capability, and no portable vector that installs it. What recurs across models and modalities is a *grammar of roles*, and the last role in that grammar — the one at which formed state becomes behavior — is what the name "final boss" now denotes.

We state the working hypothesis directly. A model behavior is produced by a context-conditioned, recipient-local **state transaction**:

```
context and prompt history
  → route and recipient-local address
  → native nonlinear formation or commitment
  → ordered residual and/or key/value carriage
  → recipient-local write and output protocol
  → unchanged native consumer
  → behavior and autonomous continuation
```

The transaction is a tuple — source event, recipient-local address, payload, carrier trajectory, formation law, recipient transition, native consumer, continuation horizon — and its governing rule is a discipline about authority: **no field acquires semantic or execution authority because it has a high activation, decodes cleanly, reconstructs well, or resembles a donor geometrically. The consumer must execute it.** The **terminal consumer role** (informally, the "final boss") is the first downstream transition whose *native* computation makes an installed state behaviorally authoritative under a particular consumer and future horizon. It can be a late output action, a distributed image writer, a persistent key/value corridor plus a decoder, or a transaction spanning early formation and late consumption. It is not required to be one layer.

This paper is a companion to two measurement papers in this repository. The distributed-store methods paper [1] contains the single-site-vs-whole-path instrument and its offline verifiers; the certified diffusion-circuit paper [2] certifies the twenty-axis route and its traps; and a theory companion [3] defines the trajectory-functional object and its eight certificates. Here we make the *transaction* — its stages, its consumer-bound authority, and the controls it passes and fails — the scientific center, and we add the cross-family dossier, the leverage, the honest leaks, and a blind auto-detection trial.

## 2. Method: freeze the suffix, name the consumer, judge by the output

All causal evidence uses one scheme, shared with [1, 2]: capture the unmodified computation once, fork a branch from that captured state with one internal value replaced, hold everything downstream bit-identical, and run the native suffix to an output the model actually serves. Two properties are load-bearing.

**The exact no-op gate.** Resuming a capture with a zero-magnitude write must reproduce the native output bit-for-bit (maximum absolute logit difference 0.0, or mean absolute pixel difference 0.0). Every "install," "rescue," or "revert" result is interpreted against that gate; a result is trusted only because the untouched replay is exact.

**The consumer decides.** Every branch is scored on an observable the model serves — the next-token distribution over a frozen candidate set for language models, or the unchanged scheduler-and-decoder to pixels for diffusion. Internal similarity (carrier cosine, reconstruction, route overlap) is a diagnosis, never a verdict; §5 and [2] document cases where it points the wrong way.

The **four-quadrant certificate** ([3], §3) is the promotion rule: a behavior is a path-constituted transaction at a tested cut only when single-site ablation and single-site writing both fail while whole-path ablation removes the behavior and whole-path writing installs it, all judged by the unchanged consumer, with no-op and uninstall as hard validity gates and a capability-and-generic-floor gate as an eligibility condition. Evidence is labeled on a fixed ladder — observation, trend, convergent trend, working inference, terminal claim — and a failed gate means "not established by this test," not "absent."

## 3. The transaction across behavior families

The table below is a dossier of the behavior families we studied, with verdicts on the ladder above and their denominators. It is a table of *named cells*, not interchangeable replications.

| family / behavior | model(s) | verdict | denominator | headline | receipt |
|---|---|---|---|---|---|
| diffusion route, six axes (lighting, identity, weather, fur, orientation, relation) | FLUX.2 Klein 4B | **certified** (9/9 gates) | 2 seeds | min target progress ≥ .866; max ablation ≤ .072 | [2]; bundled `circuit-panel-ledger.json` |
| diffusion route, eleven axes (marking, scene×3, style, material, eyes, geometry, size, action) | FLUX.2 Klein 4B | **carrier** (7/9 gates) | 2 seeds | route established, strict pixel tier open | [2] |
| diffusion route, three axes (pose, count, relation-2) | FLUX.2 Klein 4B | **candidate** (6/9) | 2 seeds | trend only; edge rescue below .50 | [2] |
| scene edit (four-factor compound) | FLUX.2 Klein 4B | **certified-route** | 2 seeds | sufficiency .9133; ablation .0225; wrong-color −.4303; sham ≤ .1086; mediation .7705 | private `job-3cd13239dd91` (bundled summary in [1]) |
| cross-checkpoint portability | FLUX.2 base-4B, 9B | **trend** | 2 seeds/ckpt | subject write on 9B .743 vs sham .043 (> 15×) | private `job-17788d5a1b0d`, `job-638d05dcbff2` |
| cross-family conditioner (FLUX.1) | FLUX.1-schnell | **trend** | 2 seeds | route carries .6915 image progress, 98% of the all-joint ceiling | private `job-a676189574d1` |
| autoregressive key/value causal chain | Qwen2.5-Coder-7B | **trend** (terminal claim false) | n = 4 | joint K/V installs 4/4; K-only 0/4; V-only 0/4 | private `job-a12ed4b56846` |
| distributed-store sink grid | 1 diffusion + 3 AR families ≤ 8B (+30B MoE) | **certified** (four-quadrant) | 8 cells, n ≤ 4 | 8/8 four-quadrant closures | [1, 3]; bundled `job-6650205b45eb`, `job-72f0e98679d5`, `job-6299f2391d5c` |
| certified induction circuit | Pythia-70M (step 1000) | **certified (writer); whole-model account partial** | 1 seed | writer scope-2 R .871; 5-head whole-model scope-1 R .926 | private `job-12c7fc70c022`, `job-b936245a2c2d`; verifier in [2] |
| recipient-native capability patch (counting) | FLUX.2 Klein 4B | **refuted for deployment** | 8 paired cells | installs 3→5, but collateral gate fails | private `job` (recipient-patch, see §6) |
| coordinate / position map | FLUX.1, FLUX.2 | **refuted** | 2 seeds | `translate_blocks(+4)` leaves object in place | private `job-3980f89faa61` |
| instance binding | FLUX.2 Klein 4B | **not established** | 3 seeds | old operator target has no numerical path (12/12 identical writes) | private `job-47589b8693dc` |
| fitted residual-schedule "clock" | Qwen (AR) | **retracted** | — | rank confounded with dose/anchor count | private `job-dfcb4146232b`, correction on file |

Three of these deserve the detail that makes the transaction concrete.

**The autoregressive key/value chain (private `job-a12ed4b56846`).** In a 7B code model performing a natural task, we captured the native execution, then tried to install the same behavior into a neutral prompt by writing the formed subject state. The dossier line above is the whole point of the transaction view: the behavior installs when the *joint* key/value trace is written (`P0-Mplus`, 4 of 4, with autonomous continuation 4 of 4) and does **not** install when only the keys (`P0-Mplus-K-only`) or only the values (`P0-Mplus-V-only`) are written (0 of 4 each). Removing the natural key/value support at the carrier layer abolishes the behavior (`natural-lesion` 0 of 4) and a neighboring-layer repair restores it (`natural-neighbor-L1-state`, `natural-neighbor-L4-state`, 4 of 4), while a wrong-layer write (`natural-wrong-layer-L0-state`) does not (0 of 4). The installed carrier matches the natural lesion at cosine 0.9999756, over a prefix-only support of 4,644 layer/component/position rows. The `protocol-only` arm (writing the output format without the task state) is 0 of 4: the format is not the task. This is a transaction, not a site.

**The certified induction circuit and its whole-model account (this week, 2026-09-30).** In a public 70M model at the checkpoint on which it was certified (step 1000), the certified two-head writer {layer-3 head 1, layer-3 head 6} recovers 87.1% of the induction loss *within its layer* (scope-2 R 0.871, recovered KL 0.925), but keeping only those two heads and mean-ablating every other head recovers almost nothing of the whole-model induction loss (scope-1 R 0.042, against a random-pair mean of 0.035). The certificate is the *writer* end of the transaction; the whole-model account needs the upstream previous-token relay that builds the induction keys. A held-out completion identifies it: adding two layer-2 heads lifts scope-1 induction R from 0.045 to 0.897, and a third layer-3 head to 0.933; the minimal whole-model set is five heads {layer-2 heads 1 and 7, layer-3 heads 0, 1, 6} at test scope-1 R 0.926 (random same-shape controls mean 0.17, max 0.50) (private `job-12c7fc70c022`, `job-b936245a2c2d`; the single-file CPU verifier for the certified writer ships with [2]). The result is exactly the transaction grammar: an *address* stage (layer-2 key-builders) feeding a *writer* (the certified layer-3 heads) feeding the consumer (the unembedding). The score stays a strong partial: one seed, one family, one checkpoint; on the fully-trained checkpoint the same five heads give scope-1 R 0.55 and are no longer specific.

**The scene-edit certificate (private `job-3cd13239dd91`; summary bundled in [1]).** A four-factor compound scene edit certifies as a route on two seeds with minimum scene sufficiency 0.9133, route-ablation progress 0.0225, wrong-color progress −0.4303, maximum sham 0.1086, minimum mediation 0.7705, consumer return progress 0.9824 and alignment 0.9708, exact scalar replay. What it does *not* establish — scene-only disentanglement, minimal addresses, preservation of every non-scene factor — is recorded as the boundary.

## 4. How this differs from a classic static circuit

Five properties separate a support-aware transaction from a fixed subgraph, and each is measured.

1. **Time accumulation.** The effect is built across the accumulation axis. In the diffusion route, single-step interventions fail necessity and sufficiency at every site while all-step interventions pass both ([2], §5); in language models the store is the second half of the layer stack, with no single late layer necessary ([1], §4; [3], §5). A static-circuit reading of a single step or layer reports "absent."
2. **Cross-position joint key/value.** The carrier is a joint object. In the 7B chain (§3), key-only and value-only writes are 0 of 4 while the joint write is 4 of 4; in a separate autoregressive prefix-compiler experiment on two public models (a 0.5B model and a public 70M model), a *joint* key/value row permutation or reversal preserves the eight-token continuation while moving keys alone or values alone diverges at the first token (receipts in private experiment store). The correct mathematical object is a set of paired records modulo joint permutation, not an absolute token-row address.
3. **Formation separates from protocol.** The output format is not the task. In one compiler study, a protocol-only action on task-bearing sealed contexts passed 4 of 4, while the same protocol on taskless neutral inputs passed 0 of 8 exact-task consumers (private experiment; the route-discovery instrument's follow-up queries). A successful output prefix is not proof that the task program formed there.
4. **Non-monotone dose basins.** Dose is not a linear strength knob. A recipient capability patch reaches the target count at dose 2 but not at doses 0.25–1 or 4 (counts 3/3/3/5/3 across doses 0.25/0.5/1/2/4; §6); a state-equivalence dose scan brackets a finite launch basin between dose 1.0 and 1.25; a diffusion spatial-address edit is cleanest at the centered address (mean absolute error to target 25.4 at shift 0, rising to 35–42 on either side); and late extra dose cannot buy back a missing early step ([3], §8). "More is better" is false.
5. **Authority is bound to the consumer.** Carrier cosine, reconstruction, route similarity, and plausible images repeatedly disagreed with what the unchanged consumer did ([2], §7, §11; [1], §5). A capability package is real only when its native consumer, continuation, custody, and rollback contract all agree; a state that decodes cleanly but is ignored by the recipient is not executable at that port.

## 5. Leverage

The transaction view is operational: naming the address, the carrier, and the consumer lets one edit, transplant, and compose behaviors, with the consumer as referee.

- **Real image edits (hotpatch).** A four-specimen replication installs a scene or subject edit early in denoising and reaches 0.904–0.971 progress toward the intended factor, while a hostile donor moves toward its own incompatible factor (0.926–0.953) and the same edit installed halfway through denoising falls to 0.095–0.358; the run is one model load, forty logical branches in eight physical calls, all no-ops exact (private, hotpatch-cinema). A prompt-paired wall-picture edit moves a framed picture to the requested side (target position progress 1.000, picture-region progress 0.916–0.969) while preserving the exact decoded frame crop in 4 of 4 specimens (private, wall-picture hotpatch).
- **The wrong-address control.** Specificity is a control, not a hope: a wrong-color donor scores −0.4303 against a sham ceiling of 0.1086 on the scene edit (§3); a wrong-address object write leaves the fox at sham-level 1.3–6.3 mean absolute error while the addressed ball whitens; the address selects the target and the payload selects the transform ([2] and private object battery).
- **Value algebra.** Displacements compose. A difference of value-cache rows (a blue-ball value minus a red-fox value) added to a mug row renders a blue mug — moving the mug region by 59.8–65.0 mean absolute error while the cat region moves 1.9–3.6 — and ports to the 9B checkpoint at 0.471 against a sham of 0.076 (receipts in private experiment store; 9B port `job-638d05dcbff2`).
- **The cross-model symbol table.** A foreign model's features, anchored per-symbol through a low-rank shared displacement subspace, author content through the unchanged native consumer at parity with native authorship (|Δ progress| ≤ 0.01 per cell against shams separated by 0.62–1.29; bundled `job-0706b0497903` in [1]); held-out symbols the bridge never saw *read* at 35 of 54, twelve times chance, but zero-shot *authorship* of unanchored symbols fails at the consumer (0.13–0.24 ≈ sham) — the measured boundary. A donor-free compact writer then installs a task in a neutral prompt at 5 of 6 sealed consumers with a rank-64 package that is 2.3% of the carrier bytes (private `job-3003b3a3be8b`), and a two-call composition passes 8 of 8 (private `job-c10dc83b3e25`).

## 6. Honest leaks and limits

The transaction view earns its keep only with the controls that broke.

- **Key/value chain controls that only partly pass (private `job-a12ed4b56846`).** In the 7B chain, a *joint-row-shift* of the carrier still installs the behavior (`P0-Mplus-joint-row-shift`, result 4 of 4) but reproduces the full native continuation only 2 of 4, and a *row-permuted residual* passes fully (`P1-row-permuted-resid`, 4 of 4). These say the carried object is partly position-invariant — a set of paired records modulo joint permutation, §4 — which is a real result and also a leak: an intervention that scrambles row order should, on a strict address account, fail, and it does not. We keep both the pass and the partial.
- **The terminal claim is false, on purpose.** The same chain records `Bounded chain candidate: False` and `Terminal claim: false`; only the core causal chain under trend-first adjudication is `True`. The first discovery run of this chain had a live-cache indexing no-op, so its earlier nulls are instrument-invalid rather than a scientific null. We report the trend and withhold the terminal claim.
- **Every cell is n = 4.** The chain's arms are all x/4; the sink grid cells are n ≤ 4 ([3]); the diffusion panel is two seeds ([2]). This is replication, not a distribution, and no headline rests on a single cell.
- **A retracted fitted controller.** An earlier result fit a low-rank "clock" that appeared to author a diffusion program at rank 16 and fail below it. Under audit it was withdrawn: the target delta had been supplied before the candidate was built, rank was confounded with dose and anchor count (eight target rows at rank 8 but sixteen at rank 16), and the null was geometrically weak (private `job-dfcb4146232b`, `job-8a18f3102d6f`; corrections on file). The related "rank-16 was a clock" reading is retained only as an instrument-correction record. A separate source-dependency adapter was likewise corrected from a unique-source claim to a redundant nonlinear adapter at bounded scope.
- **Instance binding is not established.** For a scene relation, changing only the old writer's declared target produced byte-identical writes at 12 of 12 seed×step boundaries and identical images at 3 of 3 seeds: target selection has no numerical path when parent, predicate, rows, and dose are fixed (private `job-47589b8693dc`). A donor-assisted directional write does switch contact between two cameras in 6 of 6 cases (private `job-6386d22db7c1`), and a spectral address algebra can *read* the right instance, but there is no established standalone `bind(subject, predicate, object)` and no donor-free instance binder. A property can be bound to a role; binding it to a specific one of two identical instances is open.
- **A capability that was refuted for deployment.** A recipient-native counting patch (three apples → five) installs through the consumer with a rank-8 package of 55,297 parameters (104 kilobytes) and improves exact-count from 37% to 72% on an expanded held-out panel, but its collateral gate fails: a binary detector fires on 58 of 120 ordinary prompts (about 48%) with a 95th-percentile pixel deviation of 41.5 against a 6.0 threshold. Style correlates with the score at 0.928 while object-multiplicity correlates at 0.029. It is not a counting module and is not approved for deployment; we report it as a refuted product and a working instrument.

## 7. A blind auto-detection trial

If the transaction's route is real, an instrument blind to its coordinates should rediscover it. We ran a route-discovery instrument that was given the carrier interface, the candidate generator, the consumer, the semantic axis, and the selection policy, but for which the expected route extent and the route coordinates were **withheld from the discovery workers and supplied to certification only by a sealed selection**. This is coordinate-blind, not semantically blind, and we say so.

**The best result (diffusion; private `job-97708a5d46b8`).** Blind discovery on the diffusion identity axis promoted a contiguous route through `joint.0`–`single.0` and recovered all three historical target edges (`target_edge_recall` 1.0: `joint.2→joint.3`, `joint.3→joint.4`, `joint.4→single.0`), with the historical sink `single.0` recovered and the ordered contiguous subroute matched. A semantic method and a coordinate-blind structural method independently named the same transport skeleton.

**The adversarial failure (diffusion; private `job-dbf7448dc00e`, v3 reanalysis).** A second discovery run recovered the same three target edges (`target_edge_recall` 1.0) but only **1 of 3 survived an address-specificity control** (`address_specific_target_edge_recall` 0.333: only `joint.2→joint.3`), and the historical sink was recovered without being address-specific. Recall without the depth control is 3 of 3; with the wrong-depth control it is 1 of 3. Recovering the edges is not the same as certifying that the effect is depth-addressed.

**Trend without a certificate (language model; private `sequence-ab7695e26a8c`, one Qwen2.5-0.5B checkpoint, identity axis).** The route-blind scan found the necessity-and-sufficiency neighborhood but issued **0 bounded certificate observations** — status `TREND-WITHOUT-CERTIFICATE`. The development-selected winning window (depths 20–21) passes its whole-path necessity (−2.02 nats), positive control (11.79), and exact no-op (0.0), but fails the four-way and control gates that the transaction certificate requires:

| gate | bar | observed | verdict |
|---|---|---|---|
| single-site necessity fails (share) | < 0.25 | 0.443 | fail |
| single-site sufficiency fails (max normalized shift) | < 0.20 | 0.630 | fail |
| wrong-depth address specificity (effect ratio) | ≤ 0.50 | 0.631 | fail |
| final-dose rival | ≤ 0.50 | 0.645 | fail |
| wrong-source | ≤ 0.20 | 0.329 | fail |

A single depth explains 44% of the path-scale necessity and 63% of the path-scale sufficiency, and the same doses under an injective non-identity depth remap retain 63% of the effect. The honest reading is that blind coordinate discovery recovers the *trend* — the route neighborhood is real and re-findable — but a blind pass does not, on this checkpoint and axis, produce the strict four-quadrant, wrong-depth-specific certificate that a supplied-coordinate pass produces. "Failed gate" means "not established by this test," not "absent."

**Blind certification on FLUX.2 Klein 4B (in progress, 2026-09-30).** A blind certification pass on the diffusion model is running as this draft is written; its result will be filled in here. *(Placeholder — to be completed by the lead session.)*

## 8. Relation to open problems

The transaction view is a claim about *what moved where, and to which consumer*. It is deliberately silent on a set of questions that the mechanistic-interpretability literature has named as open, and it inherits their difficulty.

Anthropic's circuit-tracing methods work [4] lists limitations that bound our account too. It does not explain *attention patterns*: our certificate shows that a joint key/value carrier at a set of positions is necessary and sufficient through the consumer, but not why the query-key computation attended to those positions in the first place. The same work names **cross-position information flow** as unexplained — "we account for the information which flows from one token position to another, but not why" — which is exactly the boundary of §4's cross-position joint key/value result: we can show the joint object is the carrier (key-only and value-only 0 of 4, joint 4 of 4) without explaining why the attention that builds it routes as it does. Their **error nodes** and **replacement-model faithfulness** caveats have our analogue: our exact-replay gate guarantees the *untouched* suffix is bit-identical, but a whole-path write can be non-minimal, and a route certificate identifies causal topology without identifying every computation on the path ([2], §9; [3], §10).

Faithfulness is quantitative and fragile. Miller, Chughtai and Saxe [5] show that circuit-faithfulness metrics are highly sensitive to ablation methodology, and the indirect-object-identification circuit — a canonical static circuit — is about 87% faithful on its own metric [6], not 100%. Our numbers carry the same caution: the induction writer recovers 87.1% of within-layer loss and only 4.2% of whole-model loss until the upstream relay is added (§3), and the blind language-model pass fails its specificity gates (§7). Sharkey et al. [7] catalogue the field's open problems — superposition, the reliability of feature dictionaries, the absence of agreed evaluation standards — and our contribution is narrow against that list: a promotion rule (the four-quadrant certificate judged by the unchanged consumer) and a discipline (spend as much audit effort on every pass as on every refutation), not a solution to superposition or a universal decomposition.

Plainly: the transaction view explains that a behavior is carried as an addressed, time-accumulated joint key/value (or residual) state and committed by a named native consumer, and it gives controls that distinguish that from a localized circuit and from a diffuse representation. It does not explain why attention attended where it did, it does not certify minimality, and its blind rediscovery recovers the route as a trend but not always as a strict certificate.

## 9. Related work

The instruments this paper reinterprets — activation patching, path patching, causal tracing [8, 9, 10] — and the granularity caveats that make single-site nulls ambiguous [10, 11] are treated at length in [1]. Self-repair [12, 13] is the compensation mechanism that lets a distributed carrier survive single-site ablation. Attribution-graph circuit tracing [4, 14] is the closest program in spirit: it traces causal structure through native computation and names its own limits (attention, cross-position flow, error nodes, faithfulness), which we adopt as the boundary of the transaction view in §8. Faithfulness-metric sensitivity [5] and the IOI circuit's measured faithfulness [6] set the quantitative caution; the open-problems survey [7] sets the scope. The certified diffusion route, its coordinate-freedom, and its traps are in [2]; the distributed-store instrument and its blind-graded readout comparison are in [1]; the trajectory-functional theory and certificate suite are in [3]. The novel element here is the *transaction*: a behavior as a support-aware chain from formation through an addressed joint key/value carrier to a recipient-local write and an unchanged native consumer, with authority bound to that consumer, denominators on every family, and the retractions kept in view.

## 10. Conclusion

We did not find the final boss as a layer. We found that a capability, where it is a path-constituted object at all, is a transaction: context forms a state, an address and a joint key/value carrier move it across depth or denoising time, a recipient write and a protocol expose it, and an unchanged native consumer commits it into behavior and a continuation. The "final boss" is the terminal consumer role at the end of that chain. The evidence is a cross-family dossier with denominators, the differences from a static circuit are measured (time accumulation, cross-position joint key/value, formation-versus-protocol, non-monotone basins, consumer-bound authority), the leverage is real (edits, value algebra, a cross-model symbol table), and the leaks are on the record (partly-passing row controls, a false terminal claim, n = 4, a retracted controller, unestablished instance binding, a refuted product). A blind instrument rediscovers the route as a trend but not always as a strict certificate. What the transaction view answers is what moved where and to which consumer; what it does not answer — why attention attended there — is the next problem, and it is not ours to claim closed.

## References

[1] J. Hollenbeck. Single-Site Tests Miss Distributed Stores. [../pointwise-instruments-miss-distributed-circuits/paper.md](../pointwise-instruments-miss-distributed-circuits/paper.md), 2026.
[2] J. Hollenbeck. The Circuit That Survived Its Coordinates: Causal Evidence for Distributed Semantic Routes in a Production Diffusion Transformer. [../../bfl/docs/certified-semantic-circuits/paper.md](../../bfl/docs/certified-semantic-circuits/paper.md), 2026.
[3] J. Hollenbeck. Integral Residual Dynamics: Models Consume Trajectory Functionals, Not Sites. [../integral-residual-dynamics/paper.md](../integral-residual-dynamics/paper.md), 2026.
[4] E. Ameisen, J. Lindsey, A. Pearce, W. Gurnee, N. L. Turner, B. Chen, et al. Circuit Tracing: Revealing Computational Graphs in Language Models. Transformer Circuits, https://transformer-circuits.pub/2025/attribution-graphs/methods.html, 2025-03-27.
[5] J. Miller, B. Chughtai, W. Saxe. Transformer Circuit Faithfulness Metrics Are Not Robust. arXiv:2407.08734, 2024.
[6] K. Wang, A. Variengien, A. Conmy, B. Shlegeris, J. Steinhardt. Interpretability in the Wild: a Circuit for Indirect Object Identification in GPT-2 small. arXiv:2211.00593, 2022.
[7] L. Sharkey, B. Chughtai, J. Batson, J. Lindsey, J. Wu, L. Bushnaq, et al. Open Problems in Mechanistic Interpretability. arXiv:2501.16496, 2025.
[8] K. Meng, D. Bau, A. Andonian, Y. Belinkov. Locating and Editing Factual Associations in GPT. arXiv:2202.05262, 2022.
[9] A. Geiger, H. Lu, T. Icard, C. Potts. Causal Abstractions of Neural Networks. NeurIPS 2021, arXiv:2106.02997.
[10] F. Zhang, N. Nanda. Towards Best Practices of Activation Patching in Language Models: Metrics and Methods. arXiv:2309.16042, 2023.
[11] S. Heimersheim, N. Nanda. How to use and interpret activation patching. arXiv:2404.15255, 2024.
[12] T. McGrath, M. Rahtz, J. Kramár, V. Mikulik, S. Legg. The Hydra Effect: Emergent Self-repair in Language Model Computations. arXiv:2307.15771, 2023.
[13] C. Rushing, N. Nanda. Explorations of Self-Repair in Language Models. arXiv:2402.15390, 2024.
[14] J. Lindsey, W. Gurnee, E. Ameisen, B. Chen, A. Pearce, N. L. Turner, et al. On the Biology of a Large Language Model. Transformer Circuits, 2025.
