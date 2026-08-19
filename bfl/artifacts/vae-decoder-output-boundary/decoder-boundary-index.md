---
title: "Black Forest Labs and SATURN: Holistic Timestamped Survey"
date: 2026-08-11
updated: 2026-08-11
status: audited-synthesis
claim_status: bounded-route-certificates-established; universal-semantic-circuit-open
scope: Black Forest Labs / FLUX work in saturn and obsidian
related:
  - "[[../../saturn/docs/SATURN-BIBLE|The Saturn Bible]]"
  - "[[../leaderboard-2026-08-13|SATURN Current Evidence Panel]]"
tags:
  - index
  - survey
  - black-forest-labs
  - bfl
  - flux
  - saturn
  - holistic
  - model-analysis
---

# Black Forest Labs and SATURN: Holistic Timestamped Survey

> Audit cutoff: 2026-08-11. Newer timestamped evidence takes precedence over
> older summaries, but older artifacts remain in the chronology as immutable
> historical evidence. For the newer August 13 panel, use
> [[../leaderboard-2026-08-13|the current evidence panel]].

## Executive assessment

The Black Forest Labs work moved from model observation to a reproducible,
typed, causally addressable execution map for FLUX.2 Klein 4B. The strongest
current result is not a single semantic neuron, token, or universal address.
It is a bounded route-level carrier: native Qwen conditioning is transported
through the route

    joint.2 → joint.3 → joint.4 → single.0 → scheduler return → VAE

and can be causally transferred under a fixed model, recipe, checkpoint,
contrast, seed panel, and gate policy.

The latest 20-contrast native panel contains:

- 6 strict route-and-RGB certificates;
- 11 carrier-certified contrasts whose causal route is established but whose
  strict terminal gates are incomplete;
- 3 candidates still open.

That is a substantial engineering and scientific win. It establishes a
reusable experimental boundary around FLUX semantics, replay, intervention,
and rendering. It does not establish minimality, universality, a semantic
token address, a background-only scene function, cross-model circuit
equivalence, or a universal foreign-conditioner compiler.

The broadest knowledge gained is that FLUX behaves like a typed software
pipeline with a distributed, time-expanded semantic carrier. Shape-compatible
conditioning is not semantic compatibility. Dense hidden-state similarity can
reproduce a prompt-invariant scaffold while missing the semantic transition.
The image program can remain healthy while its conditioner argument is wrong.

## 1. Scope, evidence policy, and precedence

### What counted as Black Forest Labs work

We treated an artifact as in scope when it explicitly named Black Forest Labs,
FLUX.1, FLUX.2, Klein, or Rosetta/SATURN work directly tied to a FLUX run.
AR-only architecture and Pythia proof work are included below as adjacent
methodology when they clarify the SATURN abstraction, but are not counted as
Black Forest Labs evidence.

The survey covers both tracked and present untracked worktree artifacts. It
also follows source lists in reports, so named helper files without a literal
Black Forest Labs string are included where they implement the reported
experiment. External paths such as experiments and mstack are cited as source
anchors when Obsidian points to them; they are not silently counted as part of
the saturn/obsidian file audit.

### Current evidence precedence

The precedence rule used throughout this document is:

1. raw receipts, reports, ledgers, and rendered artifacts from the newest
   completed run;
2. the newest detailed report that interprets those artifacts;
3. older summaries, indexes, and model wikis;
4. historical or deprecated branches, retained for failure analysis.

Accordingly, the 2026-08-11 20-axis ledger supersedes the 2026-08-10
12-axis campaign for the current aggregate count. The 12-axis campaign is
still important because it established the first clean route history. The
token-only scene route supersedes the deprecated raster-mask branch. The
corrected all-row carrier and scheduler-closed compiler supersede the
source-active-mask and residual-only compiler experiments. The fixed FLUX.1
checkpoint runtime supersedes the earlier parity gap.

There is one documentation hygiene issue: the YAML front matter in the
[living circuits wiki](../circuits-wiki.md) still contains an older
“none terminal yet” status line, while its later 2026-08-11 body reports the
20-axis panel. The raw
[consolidated 20-axis ledger](../../saturn/results/rosetta-20-circuit-search/consolidated/circuit-panel-ledger.md)
and the later body are treated as authoritative; the stale front matter is
preserved as a recorded inconsistency, not silently rewritten.

### Audit inventory

The pre-survey source inventory contained:

| area | audited inventory |
|---|---:|
| Obsidian Markdown matching the BFL/FLUX/Rosetta scope | 332 source files, 134,423 lines |
| dated Obsidian BFL/SATURN blog reports | 237 files, 99,215 lines |
| Saturn matching Python in src, workers, and tests | 345 files; 3,539 functions; 180 classes |
| Saturn matching source/config/documentation families | 66 source modules, 195 workers, 84 tests, 52 configs |
| Saturn result JSON matching the scope | 891 files; all parsed successfully |
| Saturn result Markdown and Python matching the scope | 127 Markdown, 2 Python |
| path-associated raster artifacts | 4,034 files inventoried |

The survey itself is a new synthesis artifact and is not included in those
pre-survey source counts. The source text files were reviewed through a
full-file pass, including the dated
blog corpus and the source/config/test families. The raster inventory was
enumerated and its linked reports, receipts, visual reviews, proof sheets,
and representative montages were checked. The reports and receipts are the
authoritative evidence layer for binary artifacts; a raster is not treated
as an independent claim merely because it looks convincing.

No new model run was launched for this survey. This is an audit and synthesis
of the existing artifacts.

## 2. Timestamped chronology

| date or phase | work and result |
|---|---|
| 2026-07-17–07-27 | The observatory, gate policy, model-as-software vocabulary, and early causal/evaluation discipline were established. Initial BFL work emphasized calibration, failure modes, and the distinction between a visible effect and a certified mechanism. |
| 2026-07-28–08-02 | The BFL model atlas and lineage sweep compared Schnell, Klein, Klein 9B, 9B-KV, Dev, and decoder variants. H1–H9-style behavior and artifact-custody records were collected; several early semantic and color/count gates failed or remained weak. |
| 2026-08-03–08-06 | SATURN acquired a more complete runtime shape: VAE/decoder checks, Dev lifecycle and memory work, TITAN/tracer instrumentation, bounded recorders, and explicit checkpoint/replay surfaces. Mechanical trace evidence was separated from semantic evidence. |
| 2026-08-07 | Rosetta became the central FLUX.2 experiment. Native Qwen and corrected Smol/Mamba adapters shared a target ABI and route topology, but semantic payload alignment remained poor. Exact replay and frozen-suffix comparisons localized the problem upstream of the image program. |
| 2026-08-08 | Dense hidden-state students matched teacher states better than free rollout behavior. The result established that interface and scheduler parity are necessary but not sufficient for semantic translation or closed-loop generation. |
| 2026-08-09 | Native action and scene interjections, dose sweeps, spatial/temporal mappers, collateral repair, family-delta analysis, carrier-range repair, and the first scheduler-closed compiler were developed. Action interpolation was identified as off-manifold; scene locality was shown to be globally coupled. |
| 2026-08-10 | The first major 12-axis route campaign, scene certificate, distributed-carrier analysis, semantic-function experiments, third-party VAE compatibility check, and scheduler-closed TECM v4 were consolidated. Four of 12 axes were strict and all 12 were carrier-certified in that historical campaign. |
| 2026-08-11 | The current 20-axis native-Qwen panel, image-control buttons, promptless substrate validation, synthetic signal controls, local Volterra response model, typed I/O synthesis, and abstract-coordinate interpretation were documented. The 20-axis panel is the current BFL/SATURN aggregate. |

The chronological narrative is anchored by the
[BFL overview](../bfl-overview.md), the
[BFL model wiki](../black-forest-labs-model-wiki.md), the
[lineage sweep](../experiments/bfl-flux2-lineage-sweep.md), the
[Rosetta/circuit chronology](../circuits-wiki.md), and the dated reports
linked throughout this survey.

## 3. Model cohort and baseline knowledge

The early BFL work matters because it defined the specimens, exposed weak
behavioral gates, and supplied the frozen model boundaries later used by
SATURN. These results are not interchangeable: Schnell, Klein base, distilled
Klein, 9B, 9B-KV, Dev, and decoder variants answer different questions.

| specimen | wins | limits and current interpretation |
|---|---|---|
| FLUX.1 Schnell | Approximately 11.891B DiT parameters; it became a second native SATURN substrate after the FLUX.1 phase/replay parity work. | Early color-binding admission failed at 512/768/1024; lineage alignment was near null. Its later clean-but-wrong foreign-conditioner behavior is a trend, not proof of the same circuit as FLUX.2. |
| FLUX.2 Klein base 4B | 818 tensors and about 7.982B packaged parameters; 50-step guidance-4 path, adapter checks, true-CFG checks, and 658/658 exact checkpoint validations. | Final forensics were not fully reconciled. The base path is a useful runtime/control specimen, not the current four-step circuit panel. |
| FLUX.2 Klein distilled 4B | The current native Qwen circuit specimen: four steps, guidance 1.0, 256×256, pinned revision, exact replay, route intervention, and the 20-axis panel. Earlier H5–H9 work established forward/reverse causal promise. | Count behavior degraded as object count rose; reverse wrong-world checks had 45/96 donor-color collisions. Those historical failures motivated stricter controls and are not erased by later route certificates. |
| FLUX.2 Klein 9B and 9B-KV | The 9B and 9B-KV packages share topology; 9B-KV changed 96.1081% of denoiser BF16 elements while retaining high CKA around .94. Cache overhead was about 512 MiB and 1.073×. | Large weight change does not imply a different software topology or a semantic conclusion. The 9B family is lineage/equivalence evidence, not the current 20-axis certificate specimen. |
| FLUX.2 Dev | About 56.319B packaged parameters; component-decoupled 11/11 lifecycle gates, full runtime/recorder work, and later MRI analysis passed their applicable checks. | Unchecked CLIP/count/OCR behavior and large memory demands leave the semantic mechanism open. Lifecycle success is not semantic success. |
| Small decoder | About 43.678% fewer decoder parameters, 1.517× faster, cosine .999784, and PSNR 44.6426 on the paired latent test. | It is highly compatible but not exactly equal. Compatibility, speed, and numerical closeness do not certify identical rendering semantics. |

The [BFL survey index](../indexes/black-forest-labs-survey.md) and the
[model wiki](../black-forest-labs-model-wiki.md) remain useful historical
atlases. Their older H5–H9 and cohort summaries must be read together with
the newer Rosetta ledgers rather than used as the current terminal status.

## 4. What SATURN made executable

SATURN’s principal win was turning a dense FLUX invocation into an
addressable, inspectable program. The recurring execution boundary is:

    conditioner → joint blocks → single blocks → packed return register
    → FlowMatch scheduler → VAE → RGB

The implementation work is spread across the boundary, checkpoint, trace,
replay, certificate, typed-transition, and Rosetta modules. The most important
software capabilities are:

- typed boundary snapshots with shape, dtype, stream, role, and route
  metadata;
- exact checkpoint fingerprints and same-process no-op replay;
- scalar and batched suffix execution under one resident model lease;
- explicit scheduler state, including the repaired FlowMatch sigma state;
- source/target/donor/sham/wrong-axis/ablation branch separation;
- artifact manifests, receipts, MinIO custody, and immutable historical
  reports;
- route-level causal certificates with fixed gates and explicit claim
  boundaries;
- debugger vocabulary for lexical, spatial, temporal, channel, consumer,
  and render coordinates;
- a generic FLUX.1/FLUX.2 phase surface without pretending that shared names
  imply shared weights or semantics.

The most important runtime correction was discovered during the carrier-range
work: serialized checkpoints retained timestep indices but not the installed
FlowMatch sigma state. A fresh process could therefore resume at the right
index with the wrong coefficient schedule. Current checkpoints persist and
verify input sigmas, installed sigmas, step count, and scheduler fingerprint.
Old cross-process comparisons remain historical diagnostics; current
same-process duplicate suffixes are exact.

This software discipline is itself a result. Once the source checkpoint,
latent, schedule, model objects, and branch plan are held fixed, image
differences can be attributed to a declared intervention rather than to
reloading, reseeding, scheduler drift, or an accidental ABI mismatch.

## 5. Anatomical and tracing results

The BFL tracer and model observatory supplied the first map of the execution
substrate:

- Schnell exposed approximately 1,425 traced components with 19 joint and
  38 single blocks.
- Klein 4B exposed approximately 625 components, with the route addresses
  used by the current Rosetta work.
- Klein 9B and 9B-KV exposed approximately 1,056 components and comparable
  topology despite weight differences.
- Dev exposed approximately 2,744 paged components.
- The current FLUX.2 route repeatedly localizes causal transfer through
  joint.2, joint.3, joint.4, and single.0, with later image and return
  boundaries acting as consumers or render carriers.

Tracer and MRI work also established limits that remain important:

- reconstructed attention was pre-RoPE rather than the exact post-RoPE
  operation;
- synthetic tracer objectives were mechanical probes, not semantic labels;
- Winder and hypergraph candidates were useful search instruments, not
  causal proof;
- a large activation or a high module cosine did not establish a circuit;
- support can move substantially while an abstract transition survives.

The strongest structural observation came from the 12-axis abstraction:
module trajectories were highly collinear, with pairwise cosine .985960, but
top-k physical support overlap was only Jaccard .063114. The simplest current
interpretation is a distributed program whose physical carrier changes with
the substrate, not a fixed universal coordinate set.

## 6. Current 20-axis causal panel

The authoritative current ledger is
[consolidated/circuit-panel-ledger.md](../../saturn/results/rosetta-20-circuit-search/consolidated/circuit-panel-ledger.md).
It used native Qwen conditioning for
black-forest-labs/FLUX.2-klein-4B, BF16, 256×256, four steps, guidance 1.0,
seeds 4242 and 9001, and the common route
joint.2 → joint.3 → joint.4 → single.0. Four sequential resident leases
covered the 20 axes in groups of 6/6/6/2, with 252 local replays per
six-axis group.

The ledger’s bounded score is reported below. It is a route-transfer score,
not a general image-quality score.

| contrast | current status | score | branch coverage |
|---|---|---:|---:|
| dawn → sunset lighting | strict | .935447 | 9/9 |
| black cat → red fox identity | strict | .920254 | 9/9 |
| clear → snowstorm weather | strict | .911350 | 9/9 |
| short → long fur | strict | .893927 | 9/9 |
| left → right orientation | strict | .872913 | 9/9 |
| beside → behind relation | strict | .865547 | 9/9 |
| solid → tuxedo markings | carrier-certified | .876655 | 7/9 |
| snow → beach scene | carrier-certified | .869275 | 7/9 |
| photo → oil style | carrier-certified | .869066 | 7/9 |
| metal → wood material | carrier-certified | .864014 | 7/9 |
| green → blue eyes | carrier-certified | .832171 | 7/9 |
| snow → forest scene | carrier-certified | .826474 | 7/9 |
| eyes open → narrowed/closed (ear prompt proxy) | carrier-certified* | .821684 | 7/9 |
| straight → coiled snake geometry | carrier-certified | .819208 | 7/9 |
| small → large size | carrier-certified | .805103 | 7/9 |
| snow → greenhouse scene | carrier-certified | .774059 | 7/9 |
| sitting → jumping action | carrier-certified | .714784 | 7/9 |
| sitting → lying pose | candidate/open | .752920 | 6/9 |
| one → two birds count | candidate/open | .734884 | 6/9 |
| on-chair → under-table relation/containment | candidate/open | .682085 | 6/9 |

`*` Correction: the historical `ears_upright_folded` row was prompted as an
ear-position contrast, but pane-level review shows the repeatable controlled
feature is eye openness/eyelid state; the ears remain pointed. The raw
route-level tier and score are unchanged, but this row is not evidence of an
ear semantic circuit. See the [additive correction](../../saturn/results/rosetta-20-circuit-search/corrections/ears-upright-folded-eye-control.md).

The six strict axes passed the full route-and-RGB certificate policy in the
current panel. The 11 carrier-certified axes passed the route-level causal
checks but remain short of the strict sufficiency/dose combination required
for the stronger label. The three candidate axes remain useful trends and
experiment proposals, not negative findings.

For the strict panel, route-transfer scores ranged from .8655 to .9354, the
minimum target-progress gate was about .901, the largest route ablation was
small, and rescue stayed positive. The current
scene confirmation independently reported minimum RGB progress .8017 on the
snow-to-beach mapper specimen, while the standalone scene certificate
reported minimum progress .9133, maximum route ablation .0225, weakest rescue
.7705, scheduler return minimum .9824, and alignment minimum .9708 across
its nine gates. These are different panels and are retained as such.

The route recurrence across the 20 contrasts is the important invariant. The
panel does not prove that joint.2 or joint.4 is a universal semantic address,
that the route is minimal, or that no other route can implement the same
transition.

### Historical 12-axis panel

The earlier 2026-08-10 major ledger tested 12 contrasts and classified all 12
as carrier-certified, with 4 strict. Its strict group was appearance/color,
geometry/topology, lighting/time, and material/style; the carrier group
included action, pose, relation, count, object/material, and scene variants.
It had route recurrence 1.0, 13 nested certificates, and zero recorded
mismatches. That campaign established the first broad route history. The
20-axis panel is the newer and larger current aggregate; the 12-axis result
must not be merged with it as though the two were one sample.

## 7. Promptless, image-stream, and synthetic signal controls

The current control work distinguishes structural substrate from semantic
meaning.

### Promptless substrate

The promptless probe used an empty-string learned Qwen conditioner, 25 typed
boundaries, norm-controlled random perturbations, four denoising steps, and
seeds 4242 and 9001. It found:

- exact no-op: maximum return RMS 0 and RGB MAD 0;
- route effects as high as return .6967 and RGB 35.89;
- sham controls bounded at return .0951/.0675 and RGB 1.8915/3.4143;
- strong edge mediation for joint.4 → single.0 and the downstream image
  chain;
- a weak, seed-asymmetric joint.2 → joint.3 edge that was not promoted.

This validates a promptless causal substrate and typed propagation. It does
not give anonymous perturbation directions semantic names. A promptless
route is a structural result until semantic donor/target contrasts and
intervention gates are attached.

### Image-stream control buttons

The image-stream screen tested native Qwen axes for appearance, scene, and
character. The measured role map is:

| site | bounded interpretation |
|---|---|
| joint.4:image | upstream image-carrier injection |
| single.0:image | cross-stream bridge |
| single.10:image | semantic-transport amplifier |
| single.19:image | late terminal image readout |

At unit dose, mean progress was approximately .445 at joint.4, .445 at
single.0, .589 at single.10, and 1.000 for an absolute single.19 replacement
in the tested panel. The last number is a terminal readout effect, not proof
that single.19 is the semantic origin. Donor-delta screens made single.19
source-preserving or negative, while single.10 and single.0 carried the
stronger transferable image signal.

Fractional doses of .25 and .5 were often negative. Exact no-op branches
were clean, and timestep placement mattered. The null proves an ABI
necessity; it does not prove a semantic label.

### Finite-horizon signal response

The synthetic signal panel applied impulse, step, ramp, sine, alternating,
and custom envelopes across four sites, 13 waveforms, three semantic axes,
and 159 branches. It showed a finite-horizon, nonlinear, polarity-sensitive
response:

- impulse responses were mostly negative early and positive late;
- late [0,0,1,1] signals retained measurable transfer;
- positive sine, negative sine, and alternating signals behaved differently;
- ramp-up could be positive while ramp-down was negative;
- all no-op branches remained exact.

The result supports a local time-dependent response model, not an LTI system,
universal formula, or donor-free semantic generator. A first-order linear
inverse controller had mean nonterminal progress only about .056. A compact
second-order Volterra model fit the measured responses with mean RMSE around
.031 and maximum around .061, then achieved mean nonterminal progress around
.395 on real FLUX.2 suffix validation. This is a useful local controller
instrument, not a transformer replacement or terminal semantic claim.

## 8. Scene, action, geometry, and collateral knowledge

The scene and action work corrected several attractive but too-broad
interpretations.

### Action is a discrete typed state

The action route is joint.4:text → single.0:image → single.10:image. For the
fox sitting-to-running contrast, full target-state injection reached about
.991 action progress with target-image MAD around .6 and exact no-op replay.
The earlier linear interpolation

    X(d) = S + d(T − S)

produced negative progress at .25 and .50 and a ghost-like malformed fox at
.50. The full target state at dose 1.0 was coherent.

The correct interpretation is not “smooth the dose curve.” The intermediate
state is off the typed representation manifold. Production action
interjection should use a discrete ActionState; fractional doses remain
diagnostic only.

### Scene is controlled but not separable

The deprecated raster-mask and feathered branches showed a tradeoff between
background progress and subject preservation. The current token-only
background route removed the pixel compositing intervention and still found
the same overlap:

- late return-register background transfer: background progress about .9276,
  subject preservation about .4508;
- upstream joint.4 image-token transfer: background progress about .6895,
  subject preservation about .5698;
- conservative safe masks preserve more fox but retain a visible old-scene
  bubble.

The spatial mapper found a carrier hole rather than a “bubble token.” The
temporal mapper found that joint.4’s field is large upstream and moves across
timesteps, while the packed return-register field grows about 17.8× from
step 0 to step 3. Broad step-3 and all-step return-register branches were
byte-identical. The final write therefore dominates the frozen VAE boundary,
but the carrier is spatially mixed.

The current status is controlled, not seamless. The tested exact channels did
not factor background from fox identity. A finer sub-token carrier, learned
local Jacobian, or explicit render-boundary compositor is still needed before
calling a large snow-to-space edit background-only.

### Geometry transfers the donor; it does not repair the donor

The snake geometry grid showed measurable transfer for closed coil to open C,
straight, S-curve, and rope-like donors. The strongest current lesson is that
the circuit transports donor geometry; it cannot repair a failed or
mis-specified donor. Sparse masks and spatial parity errors were corrected,
and the old circuit-range gallery was invalidated rather than reused.

### Bounded software labels

The collateral and family-delta work introduced useful but explicitly bounded
names:

| label | evidence | missing closure |
|---|---|---|
| LateTextSemanticAmplifier | joint.3:text → joint.4:text contrast gain of roughly 14–16× in both Smol and Mamba family differences, with shared top channels | all-step channel-family necessity and sufficiency |
| SceneLayoutCarrier | all-step single.0:image donor restored about 68–71% of foreign-to-Qwen pixel distance and converged across two foreign families | subject-preserving locality and prompt generality |
| ObjectIdentityConsumer | downstream retained text state selected a shared cat-like attractor while the scene scaffold transferred | exact downstream operation and minimal input slice |

These are interface hypotheses with typed arguments, execution intervals,
consumer effects, and missing tests. They are better than anonymous addresses,
but they are not anthropomorphic modules or universal semantic names.

## 9. Cross-family Rosetta and compiler results

The native Qwen and corrected Smol/Mamba work separated ABI compatibility from
semantic translation.

### Target-side carrier diagnosis

The native Qwen carrier is [1, 512, 7680]. All 512 target rows are live
contextual states, even though only 28 Qwen tokenizer rows are active and the
foreign source adapters had 16 active rows. The source attention mask applies
to source keys; it does not authorize zeroing target outputs.

The intervention result was decisive:

- source-active range only: negative or low rescue;
- Qwen tokenizer range only: low rescue;
- global/per-slot/per-channel norm transport: negative or misleading;
- half-native carrier: only about 23–31% pixel rescue;
- full native carrier: 100% exact Qwen image from both foreign checkpoints.

The frozen denoiser, scheduler, latent path, and VAE were therefore still a
working image program. The defect was the conditioner argument distributed
across the complete contextual carrier.

Global carrier cosine was demoted after a prompt-invariant scaffold was
isolated. A template could reach approximately .997 carrier cosine and still
render the same wolf for fox, blue fox, cat, and corgi. Semantic direction,
magnitude, route action, continuation, and rendered image are required
alongside global tensor similarity.

### Synchronized family delta

The synchronized Qwen/Smol/Mamba experiment held prompt bytes, latent, seed,
schedule, image IDs, suffix, and sites fixed. Over 36 matched coordinates:

- Smol-vs-Mamba token-map Pearson mean: .926690;
- channel-map Pearson mean: .979430;
- top-32 token-support Jaccard: .706502;
- top-128 channel-support Jaccard: .824257.

The late text difference gained about 15.7× for Qwen–Smol and 14.4× for
Qwen–Mamba from joint.3 to joint.4. A compact 32×128 late-text rectangle
contained about 97% of contrast energy but recovered only about 1–2% of image
distance when written once at the wrong time. The state representation was
compact; the executing function was time-indexed.

Complete all-step single.0:image donation restored about 68–71% of the
Qwen pixel distance and made the two foreign families converge to nearly the
same image, but the image was a coherent cat in the Qwen-like scene rather
than the Qwen fox. Scene/layout transport and object-identity execution are
therefore separable questions.

### Scheduler-closed TECM compiler

The corrected compiler retained all 512 target rows, centered prompt-specific
residuals against the native scaffold, and trained through the real frozen
transformer and FlowMatch scheduler. The v4 closed loss fell approximately
.475225 → .112744 in the latest summary; an earlier closure report records
.475225 → .118496 for its panel.

Across the scheduler-closed panel, red/blue fox and cat examples showed
roughly 42–54% MAD reduction, while the held-out corgi astronaut improved
only about 9% and became a dog without reliably carrying breed, suit, or
space. The exact percentage differs between the panel summaries because they
report different evaluation aggregations; the stable conclusion is the same:
seen-semantic repair capacity is real, prompt-disjoint universal translation
is not established.

The raw semantic-residual term changed little while route, denoiser action,
scheduler continuation, and images improved. The frozen consumer cares about
executable directions that global carrier metrics average away. This is the
strongest current Rosetta lesson: semantic compatibility is a behavioral
contract across a state transition, not memory-layout similarity.

### FLUX.1 cross-compilation and parity

FLUX.1 Schnell now has the same bounded SATURN capabilities as FLUX.2:
checkpoint capture, exact scalar replay, batched suffixes, phase stepping,
conditioner-stream preservation, debugger addresses, and exploratory causal
panels. The cross-family adapter compiled SmolLM2 into FLUX.1’s dual T5 plus
pooled CLIP contract. Native FLUX.1 rendered the intended red/blue and
held-out objects; the adapted branch rendered coherent but semantically
wrong images.

The fresh FLUX.1 causal panel reported a live route under one recipe:

    joint.2 → joint.3 → joint.4 → single.0

with rescue fractions .3700, .3275, and .2626 across the ordered edges. This
establishes feature parity and a convergent clean-but-wrong conditioning
trend. It does not establish that FLUX.1 and FLUX.2 share the same circuit:
FLUX.1 uses T5 plus pooled CLIP, has 19 joint and 38 single blocks, and has
a different substrate fingerprint from FLUX.2 Klein 4B.

## 10. VAE and decoder boundary findings

Decoder work separated compatibility from equivalence:

- the small decoder was faster and highly close on paired latent metrics but
  not exactly equal;
- the pinned third-party MageFlow VAE produced direct latent differences
  (MAE about .0455, RMSE about .0606, cosine about .9455) and a full FLUX2
  swap with image cosine about .999729, but this establishes compatibility for
  the specimen, not universal quality or identity;
- packed return-register, subpatch, and VAE channel scans found mixed
  influence rather than a clean background-only channel;
- the VAE’s overlapping receptive fields explain why a protected carrier hole
  can become a visible scene bubble.

The VAE is therefore a measurable consumer and boundary, not a convenient
place to assign semantic ownership after the fact.

## 11. Adjacent AR and portability work

The AR work is not a BFL result, but it clarified which parts of the SATURN
architecture are model-neutral:

- typed streams for data, control, state, resource, evidence, and route;
- a single-owner StateLedger;
- transaction-local hidden states, logits, positions, and KV;
- prefix_commit as the durable writer;
- component frames and tensor-free evidence;
- a runtime-neutral certificate vocabulary.

The Pythia-70M verifier demonstrated an independent public causal proof with
layer-3 heads 1/6 source routing, Q/K address behavior, 320 held-out cases,
exact no-op/cut/matched-position/repair controls, and a negative step-512
control. It is methodology correspondence, not FLUX evidence.

The AR transition student was approximately 12.40× smaller, had only 3/64
free-rollout agreement, and was about 7.46× faster in its proof setup. That
result supports the distinction between a compressed interface and a
successful teacher replacement.

The portability conclusion is therefore bounded: the typed runtime,
checkpoint, receipt, and certificate concepts transfer; physical support,
token coordinates, semantic basis, and consumer behavior must be measured
again for each model family.

## 12. Wins

The complete body of work produced these concrete wins:

1. A pinned FLUX.2 Klein 4B/Qwen execution surface with exact checkpoint,
   scheduler, VAE, and branch custody.
2. A current 20-axis native panel with 6 strict and 11 carrier-certified
   route results, plus 3 explicitly retained candidates.
3. A repeatable route recurrence through joint.2, joint.3, joint.4, and
   single.0 across many semantic contrast types.
4. Exact no-op controls and branch-level receipts that make intervention
   differences attributable.
5. A promptless substrate assay that recovered structural propagation without
   confusing it with semantic meaning.
6. Image-stream role separation: upstream carrier, bridge, amplifier, and
   terminal readout.
7. A correction from fractional action interpolation to a discrete valid
   target state.
8. A correction from raster-mask scene claims to native token-only,
   spatially and temporally measured carrier analysis.
9. A precise explanation of the scene bubble as carrier overlap and VAE
   consumption, rather than a mysterious semantic ghost.
10. Cross-family evidence that Smol and Mamba share a suffix-defined late
    amplifier and image-carrier topology even when their semantic payload is
    wrong.
11. The full-native-carrier closure that rendered the same Qwen result from
    both foreign checkpoints, localizing failure to conditioner translation.
12. A scheduler-closed compiler that repaired several seen semantics while
    exposing its held-out composition limit.
13. FLUX.1 feature parity with FLUX.2’s checkpoint/replay/debugger surface,
    plus a bounded FLUX.1 causal route.
14. Decoder/VAE compatibility measurements that prevent “close enough”
    numerical behavior from being misreported as exact equivalence.
15. A model-neutral typed runtime and evidence vocabulary that can be tested
    on AR and other substrates without importing FLUX semantic claims.
16. A substantial negative-knowledge record: failed gates, wrong-axis
    branches, sham controls, stale reports, scheduler bugs, invalid masks,
    and deprecated galleries were preserved rather than hidden.

## 13. Knowledge gained and corrections

The main lessons are:

- activation is not circuit;
- module cosine is not support identity;
- a token span is not a pixel region after joint attention;
- a high global carrier cosine can reproduce only a scaffold;
- all 512 contextual target rows can matter even when tokenizer-active rows
  are sparse;
- a compact tensor difference may require a site-and-timestep interval to
  become causally effective;
- full target states can be valid while linear mixtures are off-manifold;
- image-transfer progress and semantic correctness can diverge;
- a terminal readout can overwrite pixels without being semantic origin;
- a scene label is not a separability guarantee;
- a protected mask can preserve the subject by preserving mixed old carrier,
  not by isolating an independent subject variable;
- a clean image from a foreign conditioner can be a healthy suffix executing
  the wrong semantic argument;
- a scheduler-closed behavioral loss is more informative than a static
  hidden-state loss for this problem;
- exact replay, no-op controls, and receipts are scientific evidence, not
  merely infrastructure;
- a failed strict gate says “not established by this test,” not “absent”;
- cross-family agreement is useful evidence, but identical route names are
  not proof of identical circuits;
- visual review, scalar repair metrics, and tensor traces are independent
  instruments and must remain separate when they disagree.

These corrections changed the vocabulary from “the model has a scene
neuron” to bounded interfaces such as a time-expanded scene carrier, a late
text amplifier, and a downstream identity consumer. They also changed the
workflow from large, brittle benchmark gates to small resident panels,
checkpoint curves, causal flipbooks, and independent controls.

## 14. Current claim ledger

### Terminal or near-terminal bounded claims

- Under the pinned FLUX.2 Klein 4B/Qwen recipe and current gate policy, six
  contrasts have strict route-and-RGB certificates.
- Eleven additional contrasts have carrier-certified route evidence.
- The route is recurrent across the current 20-axis panel.
- Exact no-op and replay contracts are established for the current runtime
  and scheduler-state representation.
- FLUX.1 has SATURN feature parity and a live exploratory causal route under
  its own native ABI.
- Full native carrier donation closes the frozen-suffix image path for the
  tested foreign checkpoints.

### Working inferences

- The semantic carrier is distributed across typed boundaries and timesteps.
- joint.4 is a late text amplification boundary in the tested FLUX.2
  family-delta specimen.
- single.0:image is a broad scene/layout carrier whose consumer remains
  semantically active downstream.
- VAE overlap and a mixed packed return register constrain image locality.
- the Rosetta bottleneck is conditioner basis/behavioral alignment rather
  than a generally broken denoiser or VAE.

### Not established

- a minimal or universal circuit;
- a universal token, channel, block, or physical address for a concept;
- semantic names for promptless random directions;
- a background-only or pixel-perfect large scene function;
- identical FLUX.1 and FLUX.2 circuits;
- a prompt-disjoint universal Qwen-equivalent compiler;
- successful free-rollout student replacement;
- decoder/VAE exact equivalence from compatibility metrics;
- terminal claims beyond the tested models, seeds, contrasts, schedules, and
  intervention contracts.

## 15. Supersession and open work

| older or tempting interpretation | current reading |
|---|---|
| “The strongest result is the old H5–H9 or 12-axis summary.” | Those are historical campaigns; the 2026-08-11 20-axis ledger is current. |
| “A changed prompt token owns a pixel region.” | Joint attention broadcasts the change; spatial and temporal carrier maps are required. |
| “Half-dose action is a useful interpolation.” | It can be off-manifold; use full typed target state for production. |
| “The packed return register has a background-only channel.” | Tested channels are mixed with subject/scene effects; VAE overlap remains unresolved. |
| “A .997 carrier cosine means semantic translation.” | The metric can be dominated by a prompt-invariant scaffold. |
| “The foreign adapter failed because the image suffix is broken.” | Full native-carrier closure shows the suffix can render the native image; the conditioner argument is wrong. |
| “Shared joint/single names prove shared FLUX circuits.” | They are coordinate aliases across materially different substrates. |
| “A strict miss disproves the phenomenon.” | It means the current test did not establish the terminal claim; the trend remains evidence. |

The highest-value next experiments are:

- multiseed and prompt-held-out 20-axis replication;
- explicit minimality, wrong-route, and alternate-route tests;
- all-step channel-family necessity/sufficiency for the late amplifier;
- a learned local scene carrier or render-boundary compositor with collateral
  control;
- held-out semantic and compositional evaluation of the scheduler-closed
  compiler;
- a clean-room FLUX.1 versus FLUX.2 carrier-timing comparison;
- free-rollout closure tests for students rather than hidden-state matching;
- decoder Jacobian and sub-token measurements that keep the VAE boundary
  explicit.

## 16. Audit references

Primary current references:

- [current circuits wiki](../circuits-wiki.md)
- [20-axis consolidated ledger](../../saturn/results/rosetta-20-circuit-search/consolidated/circuit-panel-ledger.md)
- [major 12-axis historical ledger](../../saturn/results/rosetta-circuit-finder/major-ledger.md)
- [image-stream control report](../blog/2026-08-11-saturn-image-stream-control-buttons.md)
- [promptless circuit validation](../blog/2026-08-11-saturn-promptless-circuit-validation.md)
- [synthetic signal control](../blog/2026-08-11-saturn-synthetic-signal-control-of-image-circuit.md)
- [response models and component control](../blog/2026-08-11-saturn-model-lab-response-models-and-component-control.md)
- [circuit tools and typed I/O](../blog/2026-08-11-saturn-circuits-tools-and-io.md)
- [circuit collateral repair](../blog/2026-08-09-saturn-circuit-collateral-repair.md)
- [FLUX.1 cross-compiled conditioner](../blog/2026-08-09-saturn-flux1-cross-compiled-conditioner.md)
- [the circuit outlives SATURN](../blog/2026-08-11-the-circuit-outlives-saturn.md)
- [abstract circuit coordinates](../blog/2026-08-11-the-abstract-circuit-survived-its-coordinates.md)
- [scheduler-closed compiler report](../../saturn/results/rosetta-cross-family-manalysis/tecm-scheduler-closure/job-19ee4384139e/analysis.md)
- [scene certificate report](../../saturn/results/rosetta-scene-circuit-certificate/job-69fed6e9623a/certificate.md)
- [carrier-range repair report](../../saturn/results/rosetta-carrier-range-repair/job-6e355116bb07/analysis.md)

The older BFL model, lineage, tracer, runtime, and evaluation documents are
included in the 332-file audit inventory. The links above are the shortest
reproducible path through the final current evidence, while the chronology
and supersession table retain the older files’ findings, failures, and
corrections.
