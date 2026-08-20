---
title: "Cross-Compiled Conditioners: The Body Crossed First, Then the Payload"
subtitle: "What the FLUX.2 and FLUX.1 experiments actually show about driving a frozen image program with a foreign language model"
type: research-demo
status: convergent-portability-trend
claim_status: bounded-interface-interchange-semantic-equivalence-open
rank_in_bfl_survey: 3
model_scope: "FLUX.2 Klein distilled 4B primary; FLUX.1 Schnell family extension"
model_ids:
  - black-forest-labs/FLUX.1-schnell
  - black-forest-labs/FLUX.2-klein-4B
revisions:
  flux1_schnell: 741f7c3ce8b383c54771c7003378a50191e9efe9
  flux2_klein_4b: e7b7dc27f91deacad38e78976d1f2b499d76a294
checkpoint_role: "FLUX.2 recipient substrate; FLUX.1 cross-family extension"
source_conditioners:
  - native Qwen
  - SmolLM2-1.7B
  - Mamba-1.4B
consumer: "native denoiser, scheduler, VAE, and RGB image output"
backend: "CUDA on Beast; FP8 storage with sequential CPU offload"
runtime: "Saturn PhasePipeline under mrun; CUDA on Beast"
tags:
  - bfl
  - flux
  - cross-model
  - cross-family
  - conditioner
  - rosetta
  - saturn
---

# Cross-compiled conditioners

> [!summary]
> The foreign conditioner crossed the type boundary before it crossed the
> meaning boundary. In both FLUX.2 and FLUX.1, a learned adapter made a
> different language model legal to the native image stack. The frozen
> denoiser stayed coherent, the scene scaffold often survived, and Saturn
> could replay and intervene on the resulting state. But exact object,
> character, and color semantics remained tied to the recipient's native
> conditioner basis. The result is a working Rosetta instrument—not yet a
> universal semantic translator.

The old version of this demo was a ledger of scores. The scores are useful,
but they hide the sequence of discoveries:

1. FLUX.2 first showed that a foreign language model could drive a real,
   frozen image body.
2. Saturn then showed that the body, route, scheduler, and VAE were still
   addressable, while the foreign semantic payload was weak, distributed, and
   time-dependent.
3. A scheduler-closed compiler repaired several seen prompts, but the
   held-out corgi exposed the remaining generalization gap.
4. FLUX.1 repeated the experiment through a different conditioner ABI:
   T5 plus pooled CLIP instead of Qwen. The images were again coherent but
   semantically wrong.
5. The FLUX.1 Saturn port reached feature parity with the FLUX.2 instrument.
   That is a portability result about execution and measurement, not proof of
   one shared FLUX circuit.

The compact version is:

> **The body crossed. The carrier crossed. The instrument crossed. The
> recipient's meaning did not come along for free.**

## What was actually being compiled?

The experiment changes one boundary while freezing the image program behind it:

~~~mermaid
flowchart LR
    Q["Native Qwen / T5+CLIP"] --> ABI["Recipient conditioner ABI"]
    S["SmolLM2"] --> A["Cross-family adapter"]
    M["Mamba"] --> A
    A --> ABI
    ABI --> B["Frozen native FLUX body"]
    B --> D["Scheduler + VAE"]
    D --> RGB["RGB image"]
~~~

For FLUX.2, the native target carrier is a '[512, 7680]' Qwen-side field.
SmolLM2 and Mamba are separately mapped into that field. For FLUX.1, SmolLM2
must produce both the T5 sequence '[512, 4096]' and pooled CLIP vector
'[768]'. The denoiser, scheduler, VAE, latent initialization, resolution, and
recipient checkpoint remain native and frozen.

That makes the comparison unusually clean. A failed image can be attributed
first to the conditioner translation rather than to a simultaneously changed
denoiser or renderer. Saturn adds the second layer of control: checkpoint
capture, exact suffix replay, batched branches, route addresses, and
artifact custody.

There are three different claims here, and they should not be merged:

| Layer | Question | Status |
|---|---|---|
| ABI / execution | Can the recipient consume a foreign conditioner field? | **Yes, bounded** |
| Image program | Does the native suffix still produce valid, structured images? | **Yes, repeatedly** |
| Semantics | Does the foreign field preserve the prompt's object, color, and identity? | **Partial and open** |

## Act I — FLUX.2: a healthy body reading the wrong vocabulary

### The first crossing

The initial FLUX.2 experiment was deliberately asymmetric: SmolLM2 supplied
the language-side states, a trainable adapter produced the Qwen-shaped
conditioning field, and the real FLUX.2 Klein 4B denoiser, scheduler, and VAE
did all image generation.

The first result was already informative. The adapted images were clean and
stable rather than noise, but held-out prompts collapsed toward generic
tabletop or cup-like scenes. The adapter had crossed the family, not the
meaning. This was an interface-interchange result, not semantic equivalence.

The first run used a deliberately small 300-step, unmasked fitting recipe.
The corrected comparison restored the intended 700-step masked loss with CPU
FP32 source features. That correction matters: the historical underfit result
is preserved as evidence, but it is not allowed to stand in for the corrected
adapter.

### The Rosetta map

Saturn made the next question executable: if Qwen, SmolLM2, and Mamba all reach
the same target ABI, where does their semantic difference appear downstream?
The answer was not “one bad token row.” The full '[512, 7680]' carrier is
contextual and distributed. The relevant candidate route was:

~~~text
conditioner
  → joint.2
  → joint.3
  → joint.4
  → single.0
  → scheduler return register
  → VAE RGB
~~~

The corrected FLUX.2 Smol and Mamba branches could be replayed through the same
frozen suffix. Full-state interventions recovered substantial native image
distance—normalized rescue '0.751' for Smol and '0.817' for Mamba—while
compact selectors barely moved the consumer ('0.036' and '0.051' for the
strongest compact controls). Lexical-row and stable-channel stories were too
small or too brittle to explain the image response.

The route-level numbers tell the same story. Native Qwen route flow was
'0.9312'; corrected Smol was '0.5300'. The foreign carrier was live and
addressable, but its semantic transport was attenuated and delayed. Exact
checkpoint replay still worked in both arms, so the mismatch was not a
scheduler or custody failure.

### The repair that nearly looked like a solution

The scheduler-closed TECM compiler trained through the real frozen transformer
and FlowMatch continuation rather than stopping at an embedding loss. It
improved the three downstream-seen prompts by a mean RGB-MAD of '50.1856'.
That is real repair capacity.

The held-out corgi improved by only '7.2718', and the rendered result became a
different dog in a different scene rather than the requested astronaut corgi.
This is the important turn in the story: a compiler can learn to repair a
recipient's executable trajectory for seen semantics without having learned a
prompt-disjoint semantic translation.

| FLUX.2 scheduler-closed arm | Result | What it says |
|---|---:|---|
| Seen-prompt mean RGB-MAD improvement | '50.1856' | downstream repair capacity is real |
| Held-out corgi RGB-MAD improvement | '7.2718' | generalization remains weak |
| Native route flow | '0.9312' | native semantic action is strong in this route |
| Corrected Smol route flow | '0.5300' | foreign transport is live but depleted |
| Full-state Smol rescue | '0.751' | recipient state contains recoverable payload |
| Full-state Mamba rescue | '0.817' | the effect is not unique to one source family |

### The pictures say more than the parity cosine

The seen red fox is the best-case repair: the scheduler-closed foreign branch
gets close to the native snow-and-dawn render. The held-out corgi is the
generalization check: the foreign branch is a coherent image, but it is not
the requested character or setting.

| Seen prompt: the repair works locally | Held-out prompt: the meaning does not travel reliably |
|---|---|
| ![Native FLUX.2 red fox](../../../saturn/results/rosetta-cross-family-manalysis/tecm-scheduler-closure/job-ffb476166198/native_qwen_fox.png) | ![Native FLUX.2 astronaut corgi](../../../saturn/results/rosetta-cross-family-manalysis/tecm-scheduler-closure/job-ffb476166198/native_qwen_corgi.png) |
| **Native Qwen** | **Native Qwen** |
| ![Scheduler-closed FLUX.2 red fox](../../../saturn/results/rosetta-cross-family-manalysis/tecm-scheduler-closure/job-ffb476166198/scheduler_closed_fox.png) | ![Scheduler-closed FLUX.2 held-out dog](../../../saturn/results/rosetta-cross-family-manalysis/tecm-scheduler-closure/job-ffb476166198/scheduler_closed_corgi.png) |
| **Scheduler-closed foreign-conditioned branch** | **Scheduler-closed foreign-conditioned branch** |

_Figure 1. The left pair is a seen-prompt repair; the right pair is the
held-out test. These are the scheduler-closed TECM v4 artifacts, not a claim
that a single adapter loss solved semantic translation._

The same distinction explains why the corrected Smol branch can have
same-prompt image cosine '0.8258' while its red/blue separation is only
'11.423', versus '70.954' for native Qwen. Image cosine measures a broad
visual relationship. It is not an object or word-level semantic score.

## Act II — FLUX.1: a different ABI, the same clean-but-wrong shape

FLUX.1 Schnell is not the same suffix with a different label. Its native
conditioner is a dual stream: T5 token states '[512, 4096]' plus pooled CLIP
'[768]'. Its transformer has 19 joint and 38 single blocks, compared with
FLUX.2 Klein's 5 joint and 20 single blocks. The substrate fingerprints and
parameter counts differ as well.

That makes FLUX.1 a useful family extension, not evidence that the two models
share weights or semantic addresses.

### The cross-family adapter

The FLUX.1 adapter translated SmolLM2 '[512, 2048]' states into both native
conditioner streams. It had '14,378,496' trainable parameters. The source
encoder, native teacher conditioner, transformer, scheduler, and VAE stayed
frozen. Eight prompts were used for fitting and four were held out; the
adapter ran for 700 steps with seed '7217'. Native and adapted branches used
the same latent, four denoising steps, '256×256', and guidance '0.0'.

The training fit was good on seen prompts and much weaker on held-out prompts:

| FLUX.1 observation | Value |
|---|---:|
| Training token cosine | '0.9501' |
| Held-out token cosine | '0.5076' |
| Held-out pooled cosine | '0.4460' |
| Native/adapted held-out image cosine | '0.7392' |
| Native red↔blue image MAD | '111.7350' |
| Adapted red↔blue image MAD | '86.2943' |
| Adapted/native red↔blue separation | '0.7723' |

The image cosine is deliberately not treated as a semantic gate. The visual
result is the clearer read: the adapted branch remains active and structured,
but it does not keep the recipient's lexical identity.

![FLUX.1 native versus adapted red/blue contrast](../../../saturn/results/flux1-cross-compiled/job-a2cd2f54c6f4/images/semantic-contrast/contact-sheet.png)

_Figure 2. Native FLUX.1 outputs are on the left; SmolLM2-adapted outputs are
on the right. The native branch preserves the fox contrast. The adapted
branch retains broad visual regularities but collapses the requested subject
into graphic-like forms._

The held-out panel removes the possibility that this is only a red/blue
quirk. Across a lighthouse, astronaut corgi, oranges, and snowy cabin, the
adapted images remain coherent while the requested object or scene identity
drifts.

![FLUX.1 held-out native versus adapted comparison](../../../saturn/results/flux1-cross-compiled/job-a2cd2f54c6f4/images/held-out/contact-sheet.png)

_Figure 3. The broad scene/style scaffold is more stable than object identity.
“Same scene” here means a retained low-frequency visual scaffold, not
pixel-level equality or prompt-faithful semantics._

This is the FLUX.1 version of the FLUX.2 result:

1. the foreign conditioner reaches the recipient ABI;
2. the frozen image suffix remains capable of producing clean images;
3. scene, lighting, palette, and composition can partially survive;
4. character, object, and precise lexical meaning drift.

The result is convergent across architectures, but the architectures are not
interchangeable. FLUX.1 uses T5 plus pooled CLIP; FLUX.2 uses a Qwen-derived
carrier. Their shared Saturn aliases are a coordinate vocabulary, not a proof
of one common circuit.

## The instrument crossed too

The FLUX.1 result has a second layer that the original adapter-only report
could not provide. Saturn now supports FLUX.1 checkpoint capture, exact scalar
resume, phase stepping, batched suffixes, both conditioner streams, debugger
addresses, and exploratory causal panels through the shared PhasePipeline
surface.

The fresh FLUX.1 panel recovered a live route under one prompt, seed,
checkpoint, and intervention recipe:

~~~text
joint.2 → joint.3 → joint.4 → single.0
~~~

The exact scalar controls separated red from blue as expected:

| Intervention | Result | MAD vs red | MAD vs blue |
|---|---|---:|---:|
| Sufficiency: 'joint.4@2' | stayed red | '1.7893' | '65.5385' |
| Necessity: 'joint.4@2' | became blue | '65.7333' | '2.6845' |
| Coalition: 'joint.2+joint.3+joint.4@2' | stayed red | '1.9591' | '65.5420' |
| Rescue: 'joint.2→joint.3@2' | became blue | '65.2726' | '1.8203' |

Ordered mediation fractions were positive but modest:

~~~text
joint.2 → joint.3: 0.3700
joint.3 → joint.4: 0.3275
joint.4 → single.0: 0.2626
~~~

![FLUX.1 causal checkpoint montage](../../../saturn/results/rosetta-cross-family-manalysis/flux1-native-fixed/images/causal-checkpoint-panel/montage.png)

_Figure 4. The FLUX.1 causal panel keeps the snow scene and latent recipe
fixed while interventions move the red/blue state. It shows a live,
addressable route under this recipe; it does not certify a universal circuit._

The route is therefore a useful convergent trend, not an architectural
identity claim:

| Property | FLUX.1 Schnell | FLUX.2 Klein distilled 4B |
|---|---:|---:|
| Native conditioner | T5 + pooled CLIP | Qwen prompt carrier |
| Context width | '4096' + '768' pooled | '7680' |
| Joint blocks | '19' | '5' |
| Single blocks | '38' | '20' |
| Transformer parameters | '11,891M' | '3,876M' |
| Saturn route aliases | 'joint.2 → joint.3 → joint.4 → single.0' | same aliases |
| Meaning of shared aliases | local address vocabulary | local address vocabulary |

The fact that both models answer interventions at 'joint.4' does not mean the
same depth, weights, carrier timing, or semantic function lives there. FLUX.1
is feature-parity evidence and a second clean-but-wrong conditioning trend,
not a same-circuit certificate.

## What crossed, and what did not

| Layer of the program | What the evidence supports |
|---|---|
| **Custody and mechanics** | One guarded mrun lease, pinned checkpoints, exact replay, and immutable result artifacts. |
| **Conditioner ABI** | SmolLM2 and Mamba can be lowered into FLUX.2's Qwen-shaped field; SmolLM2 can be lowered into FLUX.1's T5+CLIP contract. |
| **Frozen consumer** | Native denoiser, scheduler, VAE, and RGB readout remain usable with the foreign field. |
| **Route instrumentation** | FLUX.2 route interventions and the FLUX.1 parity panel expose live recipient-local causal behavior. |
| **Scene scaffold** | A convergent trend: broad layout, palette, lighting, and texture can survive the translation. |
| **Semantic payload** | Partial: seen repair and local rescue exist, but held-out object/identity transfer is weak. |
| **Address portability** | Not automatic. Later register work finds row-sharp behavior in FLUX.2 but NP-window behavior in FLUX.1's bidirectional T5 conditioner. |
| **Universal semantic compiler** | Not established. |

The latest BFL portability synthesis sharpens the wording: payload operation
can travel across recipients, but the address granularity and route remain
architecture-dependent. For this image experiment, that means “the adapter
produced legal state” and “the recipient interpreted that state as the
intended prompt” must remain separate records.

## Current claim boundary

### Observation

With the native image suffix frozen, foreign conditioners produce valid,
structured images through both FLUX.2 and FLUX.1 recipient contracts. Saturn
can capture, replay, and intervene on the resulting state.

### Convergent trend

Across FLUX.2 Qwen/Smol/Mamba and FLUX.1 native/Smol comparisons, scene and
style scaffolds survive more readily than object, character, color, and
lexical identity. Full contextual state and route/time-aware interventions
matter more than a small lexical-row or norm-matching patch.

### Working inference

The bottleneck is not a broken VAE or an unusable denoiser. It is translation
into the recipient's learned semantic coordinate system: the carrier must
preserve the right directions, magnitudes, continuation, and address grain at
the times the frozen consumer reads them.

### Bounded terminal claims

- An explicit SmolLM2 adapter can make frozen native FLUX.2 consume a foreign
  conditioning family under the pinned Klein 4B recipe.
- An explicit SmolLM2 adapter can make frozen native FLUX.1 consume a foreign
  dual-stream conditioner under the pinned Schnell recipe.
- FLUX.1 now has bounded Saturn feature parity and a live exploratory causal
  route under the tested recipe.

### Not established

- semantic equivalence between native and foreign conditioners;
- one universal FLUX.1/FLUX.2 circuit behind the shared route aliases;
- held-out prompt-faithful object or identity transfer;
- cross-family portability of the learned adapter to larger, non-distilled,
  or otherwise different FLUX checkpoints;
- a compact, prompt-independent semantic address map.

The BFL survey therefore treats cross-family compilation as a high-value
portability study with open joints—not as a finished model interchange result.

## Evidence trail and artifacts

### Narrative posts and surveys

- [The Adapter Crossed the Family, Not the Meaning](../../../obsidian/blog/2026-08-06-the-adapter-crossed-the-family-not-the-meaning.md)
- [SATURN Became a Rosetta Map for FLUX.2](../../../obsidian/blog/2026-08-07-saturn-flux2-rosetta-map.md)
- [The Scene Stayed; the Character Moved — FLUX.1](../../../obsidian/blog/2026-08-09-saturn-flux1-cross-compiled-conditioner.md)
- [Black Forest Labs and SATURN: Holistic Timestamped Survey](../../../obsidian/indexes/black-forest-labs-saturn-holistic-survey-2026-08-11.md)
- [BFL Survey Review and Experiment Verification](../../../obsidian/2026-08-17-154515-bfl-survey-review-and-experiment-verification.md)
- [The Phase Boundary Held: Exact Serving Parity Across Four FLUX Checkpoints](../../../obsidian/blog/2026-08-19-133000-phase-parity-crossmodel.md)
- [The Registers Travel: Object Semantics Across FLUX Models](../../../obsidian/blog/2026-08-19-133500-the-registers-travel-object-semantics-across-flux-models.md)
- [The Payload Crossed the Wall](../../../obsidian/blog/2026-08-19-173454-the-payload-crossed-the-wall.md)
- [Two Boundaries Crossed](../../../obsidian/blog/2026-08-19-164000-two-boundaries-crossed.md)

### FLUX.2 reports and receipts

- [Rosetta consolidated readout](../../../saturn/results/rosetta-cross-family-manalysis/ROSETTA-CONSOLIDATED.md)
- [Semantic-bridge closure analysis](../../../saturn/results/rosetta-semantic-bridge-closure/job-21e43d04de4d/analysis.md)
- [Scheduler-closed TECM v4 analysis](../../../saturn/results/rosetta-cross-family-manalysis/tecm-scheduler-closure/job-ffb476166198/analysis.md)
- [Corrected FLUX.2 Smol report](../../../saturn/results/rosetta-cross-family-manalysis/corrected-flux2-smol-retry/flux2-smol.json)
- [FLUX.2 native report](../../../saturn/results/rosetta-cross-family-manalysis/flux2-native.json)

### FLUX.1 reports and receipts

- [FLUX.1 versus FLUX.2 conditioner comparison](../../../saturn/results/flux1-cross-compiled/job-a2cd2f54c6f4/flux1-vs-flux2-comparison.md)
- [FLUX.1 result JSON](../../../saturn/results/flux1-cross-compiled/job-a2cd2f54c6f4/result.json)
- [FLUX.1 run receipt](../../../saturn/results/flux1-cross-compiled/job-a2cd2f54c6f4/run-receipt.json)
- [FLUX.1 artifact manifest and SHA-256 hashes](../../../saturn/results/flux1-cross-compiled/job-a2cd2f54c6f4/artifact-manifest.json)
- [FLUX.1 adapted/native red-blue contact sheet](../../../saturn/results/flux1-cross-compiled/job-a2cd2f54c6f4/images/semantic-contrast/contact-sheet.png)
- [FLUX.1 held-out contact sheet](../../../saturn/results/flux1-cross-compiled/job-a2cd2f54c6f4/images/held-out/contact-sheet.png)
- [FLUX.1 causal montage](../../../saturn/results/rosetta-cross-family-manalysis/flux1-native-fixed/images/causal-checkpoint-panel/montage.png)

### Runtime implementation

- [FLUX.1 dual-stream conditioner](../../../saturn/src/saturn/flux1_conditioner.py)
- [FLUX.1 checkpoint/runtime adapter](../../../saturn/src/saturn/flux1_checkpoint.py)
- [Shared diffusion PhasePipeline](../../../mrun/src/mrun/diffusion/phase.py)

The raw PNGs, JSON reports, run receipts, and manifests are the primary
artifacts. This page is the narrative comparison layer: it explains why a
clean adapted image is evidence of a functioning consumer, why a held-out
semantic miss remains a real miss, and why FLUX.1/FLUX.2 agreement is a
convergent trend rather than a claim that their internal circuits are the
same.
