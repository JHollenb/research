---
title: Generative Model Run Survey
type: research-survey
status: active
updated: 2026-08-03
claim_status: synthesis-only
source_policy: latest-controlled-artifact-wins-with-history-retained
tags: [survey, generative-models, model-runs, language-models, diffusion, image-generation, moe, mamba, qwen, pythia, flux, provenance]
related:
  - "[[generative-model-analysis]]"
  - "[[../generative-model-wiki]]"
  - "[[../black-forest-labs-model-wiki]]"
  - "[[model-analysis-source-coverage]]"
  - "[[model-analysis-local-experiments-coverage]]"
---

# Generative Model Run Survey

This is the single run-oriented survey for the generative-model work in the current workspace. It
joins model-bearing runs, static model screens, diagnostic/instrument runs, controlled generative
organisms, and the runtime/custody evidence needed to interpret them. It is a synthesis layer, not
a replacement for raw reports. Every row below points to the source owner or frozen run ledger
that contains the complete attempt history, job IDs, artifact paths, and supersession decisions.

The short answer is that the models are not adequately described by a capability score or a named
module. Across the runs, the stable object is a trained substrate interacting with a context, a
state trajectory, an intervention or training history, a downstream consumer, and an execution
interface. We have strong local observations and several bounded causal specimens. We do not yet
have a complete natural-model causal twin, a universal circuit vocabulary, or a cross-modality law.

## Scope and audit rule

“All runs” here means all currently routed generative-model subjects and canonical run families in
the workspace as of 2026-08-03. It does not mean counting every copied checkpoint, vendored payload,
duplicate retry, cache file, or generated plot as a new experiment. A retry is a new execution
identity but remains attached to its predecessor; a cancelled, failed, or unsupported run remains
visible when it changes what the evidence licenses.

The survey includes:

- autoregressive language models, routed language models, state-space/Fourier outgroups, and
  controlled language-model organisms;
- continuous diffusion/rectified-flow image generators, discrete masked-token image generators,
  auxiliary decoders, and screened candidates;
- model acquisition, static anatomy, behavior, physiology, causal interventions, formation,
  adaptation, and runtime/custody runs when they bear on what a model is or how it works.

The source-coverage index reports 3,736 routed Markdown documents in the historical
`grok-mechanism-full-proof` corpus, 70 discovery experiment directories, 60 mrun recorder/decoder/
MRI/render/tape/mlops source files, and 770 model-analysis-tagged Obsidian notes in its latest
snapshot. Those are source-routing counts, not independent model results. The image atlas has 15
generator, family, or auxiliary entries. The BFL observatory currently has seven declared subjects,
472 behavior records, 14,172 physiology records, seven Bench subject cards, and a live C5 ledger.

## Evidence status

| Status | Meaning | What it permits |
|---|---|---|
| **model-bearing** | The declared model or checkpoint actually loaded and ran on a declared route. | Claims about the declared specimen, recipe, site, and run only. |
| **behavior** | Outputs were generated and scored or reviewed under a fixed prompt/seed/recipe panel. | Bounded behavior and failure trends; not a mechanism. |
| **readability / physiology** | Internal state was recovered or measured at a declared stream, site, time, and consumer. | Local information-recovery or use trends; not necessity or sufficiency. |
| **causal / bounded** | A controlled intervention changed a declared output or state against registered controls. | The scoped intervention effect and its collateral/repair profile. |
| **static / anatomy** | Revision, configuration, tensor inventory, or topology was validated without a forward. | Structural and custody facts only. |
| **diagnostic / instrument** | The route, hook, evaluator, or resource contract ran partially or failed before model science. | A statement about the instrument or execution envelope; not model absence. |
| **controlled organism** | The model was trained on a known toy or planted task with visible ground truth. | Instrument calibration and formation evidence; no automatic transfer to a natural model. |

Failed gates are retained as instrument or terminal-claim results. They do not erase directional
trends, near misses, heterogeneous families, or alternative explanations.

## Run inventory at a glance

| Run family | Subjects | Canonical run surface | Current reading |
|---|---|---|---|
| Dense Qwen scale and physiology | Qwen2.5 0.5B–14B; Qwen3 0.6B–32B; Qwen3.5 rows; Llama/Qwen comparison rows | [[../experiments/scale-panel|scale panel]], [[../experiments/scale-panel-reaudit|scale re-audit]], [[../experiments/recorder-explore|Recorder]], [[../experiments/generational-model-observatory-g0|G0]], [[../experiments/generational-model-observatory-g1|G1]] | Coding and small saturated probes do not show the original emergence story; family-clean Qwen3 multi-hop lift and rule induction do rise with scale. Decoder, curriculum, tokenizer, recipe, and interface effects still matter. |
| Qwen binding and adaptation | Qwen3 8B, 14B, 32B, 30B-A3B, 3.5-2B, plus Qwen3 1.7B gate | [[../experiments/qwen-newgen-conjunctive-binding-night|Qwen binding night]], [[../../experiments/2026-07-23-020411-qwen3-1.7b-native-circuit-behavior-gate/results|1.7B gate]] | Adapters acquire selective role/codebook behavior. The persistent exact-one/multiple-witness failure and policy differences prevent a native circuit claim. |
| Six-model MoE observatory | Mixtral, Qwen1.5-MoE, Qwen2-57B-A14B, OLMoE, Qwen3-30B-A3B, DeepSeek-V4-Flash | [[../experiments/generational-model-observatory-g2-moe|G2 MoE owner]], [[../../experiments/2026-07-18-195133-generational-model-observatory/study.moe.json|frozen study]] | Routing, load skew, locality, and bounded runtime are measured. Expert activity is not expert semantics. |
| Typed cartridge and transport ports | Qwen3-4B and SmolLM2-1.7B, with related model-local socket/renderer cells | [[../../experiments/2026-07-27-cross-family-cartridge-socket-smollm2/RESULTS.md|cross-family socket result]], [[../../experiments/2026-07-27-structured-router-cartridge/RESULTS.md|structured-router result]] | A byte-identical typed program can cross a family boundary after recipient-local calibration, while the generic relation frontend still fails its exact gate. This is interface portability, not a native circuit or general reasoning law. |
| Pythia/GPT-NeoX formation | Pythia-70M, 410M, 1.4B and checkpoint series; GPT-2/DistilGPT2 comparison cells | [[../experiments/pythia-70m-conjunctive-routing-mechanism-packet|Pythia mechanism packet]], [[../experiments/formation-cartography|formation cartography]] | Formation, relapse, source recovery, and local causal answer-state effects are visible on controlled tasks; no universal developmental law is established. |
| FNet/Mamba outgroup atlas | FNet Base; Mamba-1 130M/370M/2.8B; Mamba-2 370M; Codestral Mamba 7B; Falcon Mamba 7B; FLUX.1 comparison | [[../experiments/flux-fnet-mamba-mechanism-atlas|FNet/Mamba atlas]] | Mixer topology, state geometry, time constants, and runtime differ. Cross-family rank or speed is not intelligence or mechanism. |
| Generative image atlas | 15 generator, auxiliary, or screened entries | [[../../experiments/2026-07-24-generative-image-model-atlas/CURRENT_SYNTHESIS.md|current synthesis]], [[../../experiments/2026-07-24-generative-image-model-atlas/ARCHITECTURE_CONCEPT_MATRIX.md|comparison matrix]], [[../../experiments/2026-07-24-generative-image-model-atlas/MECHANISM_AUDIT.md|claim audit]] | Architecture and custody coverage is broad; behavior coverage is uneven; no image model has a validated causal semantic circuit. |
| BFL generational observatory | FLUX.1 Schnell, Klein base 4B, Klein distilled 4B, Klein 9B, Klein 9B-KV, Dev, Small Decoder | [[../../experiments/2026-08-01-233923-bfl-generational-model-observatory/RUNS.md|live run ledger]], [[../../experiments/2026-08-01-233923-bfl-generational-model-observatory/reports/SYNTHESIS_INTERIM.md|interim synthesis]] | Exact-latent behavior, trajectory, physiology, KV/interface, formation, and exploratory causal trends are collected. C5 identity and specificity adjudication remain open. |
| Controlled generative organisms | Modular addition, PAN/PAN-Hard, planted operators, Qwen toys, renderer families, diffusion toy organisms | [[../experiments/pan-hard|PAN-Hard]], [[../experiments/post-flux-toy-research|post-FLUX toys]], [[../../experiments/2026-08-02-002200-blind-tool-calibration-round5/REPORT.md|blind calibration report]] | They expose instrument pathologies and provide ground truth. They do not certify the corresponding mechanism in a natural model. |

## 1. Autoregressive dense language models

### Common execution model

The dense language-model runs execute a causal next-token transformer: tokenization and embeddings
enter repeated residual blocks; attention mixes context, MLPs write nonlinear features, and a
normalization/readout produces next-token logits. The work measures several different objects in
that process:

```text
static weights and topology  -> anatomy
prompt-conditioned activations -> physiology
output change under a lesion/patch -> causality
checkpoint/adaptation trajectory -> formation
```

The same layer or head can therefore be readable without being necessary, causally active without
being a complete circuit, or changed by a training intervention without being a native feature.

### Qwen family run cards

| Model | Run information | What we know | How the evidence is interpreted |
|---|---|---|---|
| **Qwen2.5-0.5B** | G0/G1 model-bearing Beast runs (`job-a7177bbcfd5d`, `job-9ebb0fa03e9b`); current scale-re-audit seeds include `job-7631d95a49a7`, `job-145180b6eb85`, and `job-a12982386920`. | Fixed-yardstick mean accuracy was `0.8250`; controlled-operation accuracy `0.9167`; G1 measured lower population concentration than Qwen3, and its MAP winder reached only `0.75` by the first criterion checkpoint. The corrected coding leg is already roughly `0.62–0.67`, and present-but-unused scope can be installed about `8.5×` cheaper than an absent control. | It is the baseline for the generation contrast and a useful distributed-physiology specimen. The original greedy zero and “no capability” readings were decoder artifacts, not model absence. |
| **Qwen2.5-1.5B** | Current scale re-audit succeeded on the all-capability job `job-fdf637f1a3e2`; the source records separate code fingerprints for later legs. | Coding `bracket_match_acc` reached `0.861`; Qwen2.5 multi-hop lift rises from `0.024` at 0.5B to `0.159` at 1.5B and then plateaus near `0.15` through 7B. | The fresh fingerprinted rows are usable; stale pre-fingerprint scale points cannot be silently combined into one curve. The family looks more like early saturation on these probes than a 7B coding cliff. |
| **Qwen2.5-3B** | Scale re-audit retries include `job-c5f8783d8e90` (host-pressure kill) and `job-7d0c32fcf477`; paired rows were still being reconciled in the owner report. | The killed run is an execution observation, not a model failure. | Host pressure, code identity, dtype, and seed must be separated before using this size in a scale claim. |
| **Qwen2.5-7B** | Exact BF16 headless physiology and specialization panels; the typed causal micro-edge run is the Qwen2.5-7B `mrun` specimen. | A bounded rank-one L20/H16/H20↔KV2 relay passed its local causal/tape/certificate checks under the declared SVA assay. | This is a same-pipeline local edge, not a complete circuit, global minimality result, or portable Qwen law. Headless physiology also omits logits/CE. |
| **Qwen2.5-14B** | Appears in the scale and specialized panels; some legacy scale rows are explicitly stale or unfingerprinted in the re-audit. | The source supports size coverage, not a clean homogeneous 14B capability curve. | Keep the model in the inventory, but do not promote the legacy point to current scale evidence without a current fingerprint and matched route. |
| **Qwen3-0.6B** | G0/G1 model-bearing Beast runs (`job-a6f1406fa789`, `job-52d9cf2bb4b1`). | Fixed-yardstick mean accuracy `0.9062`; controlled operation `1.0000`; G1 circuit/reserve activation ratio `22.29` versus `13.92` for Qwen2.5-0.5B; strongest sampled head dCE `1.059` versus `0.223`. The factorial toy failed its held-out behavior gate (`0.781` discovery / `0.438` validation). | Qwen3 changed the measured phenotype under the fixed instrument. Scale, tokenizer, training recipe, and architecture co-vary, so this is a bounded generational contrast, not a generational law. |
| **Qwen3-1.7B** | Native-circuit behavior-gate run is sealed at [[../../experiments/2026-07-23-020411-qwen3-1.7b-native-circuit-behavior-gate/results|the local result]]. | The reduced Phase-B factorial scored only `20/96` overall and `3/24` multiple-match rows. | This is a task/interface-specific no-go for selecting a native circuit. It is not evidence that Qwen3-1.7B lacks the capability in general. |
| **Qwen3-4B** | Present in the Qwen scale/generation inventory and family-clean multi-hop scale ladder; no promoted standalone native-mechanism card. | Qwen3 multi-hop lift over control is `0.249 ± 0.009`, the first point in the clean `4B → 14B → 32B` rise. Scope readout is already above the installation criterion (`0.906`, zero steps). | It is a comparison point in a real family-clean reasoning trend, not an independently closed causal specimen. The trend is metric- and family-specific. |
| **Qwen3-8B** | Corrected V/O adaptation job `job-5d92e2e383ce`; paired with the 14B arms in the binding night. | Base/trained final paired panel `0.1750 → 0.8906`; it learned role/codebook behavior but remained `0/12` on held-out multiple-match rejection. | The 8B substrate is sufficient for the adapted task. The one-seed 14B advantage is an adaptation-speed/robustness trend, not a parameter-only causal result. |
| **Qwen3-14B** | Corrected V/O, Q/K, and CVO arms: `job-5b83e09eb513`, `job-7446bb9187ef`, `job-7b88597eff77`. | V/O and Q/K reached `301/320` (`0.9406`); CVO `296/320`; role swap and codebook transformations mostly behaved selectively; all arms were `0/12` on multiple-match rejection. Order assays show policy differences, especially later-witness following. | The adapters acquired selective equivariance and an existential-conjunction-like behavior. Adapter success does not locate the frozen-base circuit or prove a multiplicative native algorithm. |
| **Qwen3-32B** | Included in the corrected Qwen binding scale/order panel and the clean family scale ladder; int8-paged multi-hop row ran on a 16GB card. | Multi-hop lift reaches `0.435 ± 0.021` versus `0.249 ± 0.009` at 4B and `0.348 ± 0.032` at 14B; systematic-learning/rule-induction also rises across the ladder. Fixed-panel order guard and multiple-witness behavior remain policy- and curriculum-sensitive. | This is the strongest current scale trend: scale and training improve a compositional measure after raw accuracy hid it. It still does not isolate raw parameter count or identify a shared route. |
| **Qwen3.5-2B** | Listed in the Qwen new-generation binding study as a comparison subject; no promoted native mechanism result. | The model is part of the comparison inventory, not a completed universal-circuit case. | Treat unclosed rows as proposed or bounded comparison context, not as missing evidence to be filled by intuition. |

The Qwen runs support a recurring pattern: capabilities can be represented, used in a controlled
adaptation, and still fail a stricter compositional or uniqueness test. Curriculum and answer-policy
semantics matter as much as parameter count. The broad Qwen state is distributed; high-leverage
populations exist, but named tails do not become a compression key or a complete knowledge store.

### Other dense and controlled language models

| Model | Run information and current result | How it works / boundary |
|---|---|---|
| **Pythia-70M** | Exact `EleutherAI/pythia-70m` `step143000` MechanismPacket; formation, two-pulse, seed, receiver-context, and final-block intervention legs are retained. A final-query residual marker predicts a registered onset, and a supervised final-state answer channel is causally effective on the declared task. | GPT-NeoX parallel attention/MLP residual blocks. The result is a local writer→transport→reader fragment on a controlled conjunctive task; the upstream route, whole-model closure, natural-pretraining interpretation, and portability remain open. |
| **Pythia-410M / 1.4B and checkpoint series** | Formation cartography, grokking/relapse, source-routing, projector, and checkpoint runs. | Checkpoints show competence, causal readability, and weight/activation organization on different clocks. Toy formation is informative but not a universal LLM development law. |
| **SmolLM2-360M** | Direct-attention parent, source-cut family search, downstream mediation, and held-out length panels in the model-disassembly/semantic-program line. | Set-valued source families and non-monotone search are real within the declared chart. A complete semantic program or single minimal source is not established. |
| **SmolLM2-1.7B** | The original scale ladder, model-disassembly/semantic-program comparisons, the cross-family task-agnostic cartridge socket (`job-42f90aa79ecb`), and the structured-router cartridge (`job-fa4a2a692235`). The socket passed inside-sum and outside-sum exchange `3/3` each, with random-core and scrambled-output ownership `0/3`; the structured router found candidates perfectly but failed its exact relation gate (`F1 .8912`, exact prompt `.7266`, exact slots `.7839`). | `HuggingFaceTB/SmolLM2-1.7B` is a 24-layer, width-2,048 `LlamaForCausalLM` with MHA/RoPE and tied embeddings. A frozen SmolLM-local socket can consume a Qwen-trained 40,270-parameter cartridge after layer 15 with zero swap optimization, rising to `.9896`/`.9883` from `.0273`/`.1641` baselines; this establishes a typed interface/transport result, not a native SmolLM circuit. The router failure localizes a remaining noun-to-query relation bottleneck. |
| **Llama 3.1-8B** | Scale-panel BF16 rows, exact BF16 headless CUDA physiology, and base/instruction specialization panels. `Llama-3.1-8B-Instruct` reached coding `0.588` and systematic reasoning `0.378`; the base comparison was an older FP32 coding `0.375` and reasoning `0.367` row. | Dense decoder-transformer behavior and specialization are measurable under the declared consumer. The headless route omits logits/CE and causal interventions, while the historical base/instruct dtype and code-path differences prevent a clean model-only comparison. |
| **Qwen2.5-7B comparison** | Exact BF16 headless CUDA physiology and base/instruction specialization panels alongside Llama 3.1-8B; its dedicated Qwen row above carries the typed causal micro-edge. | These runs compare live physiology under a fixed headless consumer; without logits/CE and causal interventions, observed specialization is not a mechanism. |
| **GPT-2 / DistilGPT2 / GPT-NeoX comparison cells** | Cross-model two-pulse, renderer/transport, and controlled mechanism calibration panels. | They test whether a role-aligned procedure can survive model-local coordinate refitting. A transferred procedure is not a universal circuit identity. |

## 2. Routed language models and MoE runs

### How routed runs work

An MoE model adds a router and a sparse expert bank to the residual computation. The route is
input- and position-dependent; the observed trace records which experts were selected, how skewed
the load was, how often nearby requests reused experts, and how much expert state had to move. A
route is a measured execution choice, not proof that an expert is a semantic module.

The frozen G2 panel used a live `moe-stream` route for Mixtral and the Qwen cases, a resident
`olmoe-cuda` route for OLMoE, and a static anatomy profile for DeepSeek. The six model jobs and
their immutable custody roots are listed in the [[../experiments/generational-model-observatory-g2-moe|G2 owner]].

| Model | Canonical job / route | What the run measured | Current model summary and boundary |
|---|---|---|---|
| **Mixtral-8x7B-v0.1** | `job-c64d19e50d34`, `moe-stream`; 480.89 s, 9,773 MB RSS, 918 MB VRAM. | Live routing, Gini `0.1920`, locality/skew nulls, expert payload cost. | Routing is comparatively diffuse in this trace. No expert-semantic or cross-model module claim. |
| **Qwen1.5-MoE-A2.7B** | `job-3368a64c2a16`, `moe-stream`; 56.21 s, 3,326 MB RSS, 894 MB VRAM. | Gini `0.4072`, route lift `0.1493`, locality and unselected slots. | Stronger route concentration than Mixtral on this bank; still a usage topology, not meaning. |
| **Qwen2-57B-A14B** | `job-9ccf61c29cc3`, `moe-stream`; 340.22 s, 7,368 MB RSS, 1,376 MB VRAM. | Gini `0.3158`, route lift `0.1313`, streamed expert execution. | Large sparse capacity can be measured under bounded memory. Parameter count and active-route cost do not identify capability mechanism. |
| **OLMoE-1B-7B-0924** | `job-496d2329b860`, `olmoe-cuda`; 84.90 s, 5,861 MB RSS, 7,776 MB VRAM. | Full profile, fixed-bank behavior `0.9125`, operation-bank `0.9167` versus scrambled `0.25`, MRI, residual factorial, and fast-runner quality/throughput. | MRI classified the live profile as distributed; the residual causal factorial stayed at chance and emitted no mechanism claim. The fast path reached `36.21` tok/s at B1 and `223.66×` aggregate throughput at B512, but throughput is a systems result. |
| **Qwen3-30B-A3B** | `job-88b15cc4d310`, `moe-stream`; 174.19 s, 6,117 MB RSS, 896 MB VRAM; also the Qwen binding bridge. | Gini `0.7123`, route lift `0.4487`, high locality and `0.4404` measured-window unselected slots; route membership churn with depth. | This trace has the strongest route concentration in G2. The adaptation bridge preserved codebook flips but remained `0/12` on multiple-match rejection; frozen routers are an intervention target, not a located semantic circuit. |
| **DeepSeek-V4-Flash** | `job-df75cf70bc50`, static anatomy; 79.50 s, 2,444 MB RSS, no VRAM. | Corrected logical/physical/quantization inventory and architecture screen. | Custom compressed attention, mixed FP4/FP8 experts, YaRN, and sliding-window semantics lack a parity-gated live engine in this panel. No behavior or physiology claim. |

The cleanest cross-MoE inference is conditional computation with family-specific routing geometry.
The false inference would be “high route Gini means a semantic expert.” The active computation is
consumer- and trace-specific; expert meaning requires held-out concept, causal, and replacement
tests that these runs did not close.

## 3. State-space and Fourier outgroups

| Model | Run | How it works and what was measured | Boundary |
|---|---|---|---|
| **FNet Base** | `job-0f9515ad8073` | Replaces learned attention mixing with a fixed two-dimensional Fourier transform; live Fourier/MLM profile and static decoder. | It is an architecture control, not a semantic transfer result. |
| **Mamba-1 130M** | `job-50e27efe53c5` | Input-selective recurrent state-space update plus local causal convolution; fused live/recorder path, time constant `0.09508`, live `170.86` tok/s. | State geometry and runtime are measured; no universal SSM circuit. |
| **Mamba-1 370M** | `job-ee6b5bb57239` | Same Mamba-1 family at matched smaller scale; time constant `0.08377`, live `89.37` tok/s, recorder surface. | Parameter and training differences remain; rank/time changes are descriptive. |
| **Mamba-1 2.8B** | `job-bbb1c1277727` | Fused live Mamba-1; time constant `0.11696`, `65.30` tok/s. | Scale transition is not an intelligence law. |
| **Mamba-2 370M** | `job-3af09c501db1` | Structured state-space duality with head/chunk structure; static anatomy, time constant `1.09447`. | The parameter-matched Mamba-1/Mamba-2 contrast is not training/data controlled. |
| **Mamba Codestral 7B** | `job-2aca4d3ac1fc` | Mamba-2 form at width 4096, 64 layers, state size 128, 128 heads, chunk 256; static anatomy. | No live route in this panel; architecture facts are not capability claims. |
| **Falcon Mamba 7B** | `job-de9ac676c864` | Fused Mamba runtime with actual `mamba_ssm`/`causal_conv1d` handles; time constant `0.14183`, `38.01` tok/s. | Fused speed is route-specific and not a semantic mechanism. |
| **FLUX.1 Schnell in this atlas** | `job-aa32bd3fb3f9` | Included under the same deterministic matrix-sampling contract as a cross-family reference; it is a rectified-flow image model, not an SSM. | Cross-family rank values do not measure image quality or capability. |

Across this panel, mixer topology changes the state geometry and the runtime contract. The runs do
not show that a common rank statistic or time constant is a model-wide measure of intelligence.

## 4. Continuous, rectified-flow, and image generators

### Common image-generation execution model

The continuous image generators generally encode text (and sometimes an image/reference), start
from a seeded latent, apply a scheduler-defined sequence of denoising or flow updates, and decode
through a VAE. The important axes are where text and image tokens meet, the latent codec, the
number and type of solver calls, CFG/reference-cache state, precision/offload policy, and the
downstream pixel consumer. The same word “concept” can therefore mean behavior, a readable hidden
direction, a causal edit, or a portable capability package; these are kept separate.

| Model | Canonical run information | What we know now | How / boundary |
|---|---|---|---|
| **FLUX.1 Schnell** | Original 14-prompt × 2-seed behavior panel; FNet/Mamba static comparison; BFL small physiology (8/8 families, 600 records) and Bench capture (800 records). | Coherent basics, style, spatial relations, and distinct people; mixed exact counts, repeated `THEE`, and anatomy/composition tails. | CLIP+T5 condition 19 joint plus 38 merged rectified-flow blocks with a 4-channel VAE. Legacy pooled reads mix text/image tokens; no semantic causal circuit. |
| **FLUX.2 Klein base 4B** | BFL behavior, C1 exact-latent endpoint (`192/192` rows), C2 full 48-family physiology (`3,600/3,600` activation rows), small physiology, and decoder/trajectory legs. | Relative to distilled 4B, every exact paired output/pixel hash changed; CLIP movement was heterogeneous, luminance rose, saturation/edge density fell on average. Late activation contracts strongly within the declared recipe. | Qwen3-conditioned five-joint/twenty-merged flow stack, 32-channel latent. Base versus distilled is a paired endpoint observation, not a distillation-mechanism proof. |
| **FLUX.2 Klein distilled 4B** | Original behavior panel; corrected explicit-stream readability; BFL C1/C2; H5–H9 route-dose/temporal/control work; H9R raw repair; current C5 family chunks. | Best observed quality/latency balance on the original panel; late target-image state conditionally separates color, typography, and style, not role assignment. H9 full-20 writes show a strong distributed route trend, while the reverse wrong-world control needs repair. | Four-step distilled Qwen3-conditioned flow. The strongest causal statement remains assay-relative and exploratory: raw repair and familywise specificity/adjudication are not yet complete, so no universal or endogenous circuit claim. |
| **FLUX.2 Klein 9B** | Behavior and small physiology (`job-2f47130aa7bc`, 600 records); 38-boundary trajectory/adapter certificates; C3 weight/interface factorial control cells. | Strong simple binding, style, hands, and people; no clear bounded advantage over 4B; strict counts remain seed-sensitive. | Wider Qwen3-conditioned eight-joint/twenty-four-merged flow stack. A prior style edit lost to the wrong-time control; it is not a causal concept result. |
| **FLUX.2 Klein 9B-KV** | Behavior, small physiology (`job-10cc734fae49`, 600 records), reference-KV pilot and full 4-cell C3 factorial; reference cache has 32 native layers and real cache extracts. | Reference delivery, call order, cache size, and paired interface effects are measurable. Native checkpoint/interface pairing shows a positive exploratory preservation interaction (`+0.17768426` across `96/96` families), but this is not semantic ownership. | Same declared 9B topology but distinct weights plus a reference-KV interface. “Same architecture” is not “same weights,” and cache delivery is not reference-style mechanism. |
| **FLUX.2 Dev** | Stock behavior attempt has `32/32` model-load failures; inherited decoupled route and current one-step transformer/VAE probe `job-ddc42204a166` completed under independent custody. | The transformer/VAE consumer is runnable with an inherited prompt tensor; current prompt frontend/processor packaging remains a barrier. No current-tokenizer or semantic mechanism claim. | Mistral3-conditioned eight-joint/48-merged stack. One-step decoupled evidence cannot certify stock multi-step parity or semantic selectivity. |
| **FLUX.2 Small Decoder** | Hardened paired decode probe `job-a3e0101fc56b` and BFL decoder leg. | One sealed latent decoded at cosine `0.9997839`, PSNR `44.6426 dB`, about `1.5166×` faster; not a standalone generator. | Narrow auxiliary VAE decoder. End-to-end package replacement, distributional quality, and equivalence remain untested. |
| **Z-Image** | Original shared 14-prompt × 2-seed behavior panel and legacy concept pilots. | Strongest manual counting and long multi-clause composition in that panel; slower 28-step recipe; no current certified concept ports. | Qwen3-conditioned 30-block undistilled single-stream flow model with refiners. Behavior is not a causal circuit. |
| **Qwen-Image-2512** | Original NF4 deployment behavior panel; no native physiology admission. | Strong discrete prompt semantics for counts, binding, text, and long relations, but every tested NF4 output showed severe mosaic/grain. | Qwen2.5-VL-conditioned 60-block image transformer, three-axis RoPE, 16-channel VAE. Precision/offload is a live confound; native/8-bit/NF4 canaries are required before interpretation. |
| **SDXL Base 1.0** | Original panel, current-wheel 16-gate/40-boundary trajectory certificate, adapter leg. | Fastest/lightest baseline; good simple objects/style; structured 512px failures in binding, counts, text, people, and long composition. | Dual-CLIP-conditioned multiscale latent U-Net with 4-channel VAE. Its different topology makes it a useful control, not a universal quality baseline. |
| **SANA 1.6B** | 28-image forced-512/20-step panel and 88-criterion review; diagnostic trajectory/no-op; guarded predecessor recovered read-only but successor remains unadmitted. | `11/88` review criteria passed, `77/88` failed, `0` uncertain. The run is off native resolution and the guarded retry failed before worker Python because 75/139 pinned wheels were absent. | Gemma2-conditioned 20-block linear-attention DiT with 32-channel deep-compression latent. The failure localizes the execution envelope, not native capability absence. |
| **HiDream-I1 Full** | Exact static package inventory; no full pipeline forward because the required fourth Llama-3.1-8B encoder is absent. | Anatomy and package custody only. | Three packaged encoders feed 16 double-stream and 32 sparse-MoE single-stream blocks. Routing, behavior, and expert specialization are unknown. |
| **Nucleus-Image** | Exact 51,656,728,957-byte static custody, 12 safetensors/1,554 tensors, guarded meta-only PLAN `job-fe1e4ac4693d` with 25/25 planning gates. | Planning feasibility and static router anatomy only; every load/dispatch/pipeline/forward counter was zero. No weights loaded, expert assignment, behavior, or concept evidence. | Qwen3-VL supplies fixed text K/V; image queries pass through three dense and 29 expert-choice sparse blocks with 64 routed plus one shared expert. LOAD remains NO-GO. |
| **Meissonic FP16** | Guarded static acquisition `job-2ec70844a962`, 16 files / 3,016,276,054 bytes; no forward. | Discrete sampler and architecture are known; no behavior or concept result. | CLIP-H-conditioned 14-joint/28-merged masked-token transformer over an 8,192-code VQ codec; mask/predict/fix/remask trajectory remains to be certified. |
| **HunyuanImage-3.0** | Zero-payload immutable screen only. | Config/header says 83.009B, 32-layer causal multimodal MoE, top-8 routing, 32-channel 3D VAE; no payload or runtime. | The selected payload would break the Beast disk reserve. This is a screened comparison target, not a run result. |
| **SD3.5 Large** | Immutable revision resolution only; access returned gated 403. | No payload, anatomy, behavior, or mechanism evidence. | MMDiT-family candidate; it remains an acquisition/access boundary. |

The architecture expansion demonstrates why “diffusion model” is too coarse: a U-Net attention
map, a joint/merged transformer stream, a reference-KV cache, an expert-choice router, and a
masked-code trajectory are different evidence surfaces. Architecture tells us where an instrument
can attach; it does not explain why a count, relation, hand, or text criterion succeeds or fails.

## 5. BFL generational observatory: current run ledger

The BFL observatory is the most complete current image run family and is still active. The full
history, including cancelled, lost, queued, superseded, and repaired identities, is in
[[../../experiments/2026-08-01-233923-bfl-generational-model-observatory/RUNS.md|RUNS.md]]. The
following is the current model-level digest; it intentionally does not rewrite the raw ledger.

| Subject | Completed run surface | Current trend | What remains open |
|---|---|---|---|
| **FLUX.1 Schnell** | Behavior/full panel, small physiology `job-74aa558a7000`, Bench capture. | Late activation L2 expands (`late/early ≈ 1.712`) in the small panel; this is a within-recipe trajectory shape. | Width, topology, scheduler, and conditioner confounds; no portable causal interpretation. |
| **Klein base 4B** | Behavior, exact-latent C1, full C2, static/decoder legs. | Exact latent inputs match across endpoints while every output/pixel pair differs; base C2 contracts strongly over normalized time. | Task-specific semantic evaluators and causal attribution of base/distilled differences. |
| **Klein distilled 4B** | Behavior, exact-latent C1, full C2, H9 route work, H9R repair. | Full-20 native writes flip donor conditions in both directions while several wrong-site/world controls do not; the route is distributed and dose/temporal effects are heterogeneous. | H9R bilateral familywise adjudication, endogenous necessity, minimality, and cross-model portability. |
| **Klein 9B** | Behavior, small physiology `job-2f47130aa7bc`, C3 ordinary-interface controls, Bench/static surfaces. | Activation L2 contracts (`late/early ≈ 0.869`) in the small panel; C3 ordinary/reference-interface main effect is near-flat under the declared consumer. | Separate checkpoint/interface co-adaptation from generic cache delivery and rerun semantic controls. |
| **Klein 9B-KV** | Behavior, small physiology `job-10cc734fae49`, C3 four-cell weights×interface factorial, reference cache, Bench capture. | Non-monotone trajectory with middle peak; native weights through native reference-KV interface show the strongest exploratory preservation interaction. | Semantic specificity, cache causal ownership, and visible-output alternatives. |
| **FLUX.2 Dev** | Stock pipeline retains 32 typed model-load failures; `job-ddc42204a166` completed one-step transformer/VAE/observational capture with inherited prompt tensor. | Runtime barrier localizes more to current prompt-frontend packaging than to the transformer/VAE consumer on this route. | Current prompt processing, multi-step parity, clean stock pipeline, and any causal/semantic claim. |
| **Small Decoder** | Paired latent decode and Bench/static status. | Decoder fidelity and speed trend only. | Full generator equivalence and end-to-end quality. |

### Current C5 and H9 state

- C5 successor chunks `job-d8b82062a1f9`, `job-938dec6e23c7`, `job-52aa50b299f9`, and
  `job-2ca0722aaa4d` cover `96/96` semantic families. The pooled full-20 margin effect is
  positive in `96/96` observed families, but all original chunks retain a model-identity technical
  gate miss because the inherited predicate compares against the Klein 4B revision rather than the
  9B revision. Route A was scheduler-lost after worker completion and readback; its history is not
  rewritten as scientific failure. A corrected compatibility overlay is running as
  `job-a135bf997904`.
- H9 `job-85c3633130e2` completed the full 12-arm/96-family panel. Full-20 writes flipped the donor
  condition in both directions; S4, wrong-token, wrong-world, and scrambled controls did not. This
  is a convergent bounded assay trend, not a universal architecture result.
- H9R `job-9bd1dd958932` has terminal raw repair evidence. The original reverse wrong-world arm had
  45/96 donor-colour collisions, so the repair is not silently substituted into history; bilateral
  familywise specificity and terminal adjudication are still pending.
- C4 single-stream surfaces show structured recipient-state stabilization/destabilization trends,
  while joint-stream scans show repeated block-2 destabilization and block-3 stabilization without
  an established semantic rescue. C5 dose curves are non-monotone and remain exploratory.

The right working inference is that a distributed, consumer-relative K/V route can influence the
declared FLUX.2 Klein 4B assay, with temporal accumulation and checkpoint/interface dependence. The
stronger claims—compact native quorum, endogenous necessity, semantic minimality, and transport to
another model—are not established.

## 6. Controlled generative organisms and instrument calibration

The toy runs are part of the generative-model survey because they reveal what a measurement tool can
and cannot establish.

| Organism / run family | What was supplied, learned, rendered, and measured | Current lesson |
|---|---|---|
| **Modular-addition / grokking Transformers** | The task and renderer provide known algebraic ground truth; training learns a solution; Fourier/weight measures and held-out behavior inspect formation. | Leverage can crystallize into weight-visible Fourier structure in a successful grokking regime, but failed-grok seeds and natural Qwen physiology show that this is not universal. |
| **PAN / PAN-Hard** | The controlled task, phase substrate, and renderer define known operators; the model learns parameters/routes; the evaluator measures behavior and intervention outcomes. | A fresh blind calibration cell recovered the conditional map point on `11/11` eligible trained organisms, but public seed metadata was reconstructible, the map interval missed its reliability floor, and the causal selector fired on paired nulls while producing no trained claims. Descriptive map evidence survives; strong blind calibration does not. |
| **Qwen toy generations / binding cubes** | Algebraic factors and response codebooks are supplied by the task; adapters or training acquire transformations; exact held-out behavior and interventions evaluate them. | They separate binding, decision, codebook, and uniqueness. A clean adapter behavior is not proof of the frozen base model's native route. |
| **Planted operators / diffusion toy organisms** | The planted operator is known, the model/renderer may learn or execute it, and the blind analyzer must recover it without an answer-key leak. | They are essential for calibrating selectors, decoders, nulls, and causal-set search. A pretty image or aggregate score is not evidence of a learned closed loop if later steps consumed oracle state. |

For every toy or visual run, the survey keeps five roles separate: what was supplied, what was
learned, what the renderer guaranteed, what the evaluator measured, and whether later steps consumed
model-predicted or oracle state.

## 7. How to read the cross-model evidence

Several findings recur across unrelated run families:

1. **Anatomy is not physiology.** Weight spectra, router tensors, static block types, and topology
   identify possible computation. They do not show which path a prompt or timestep uses.
2. **Physiology is not causality.** A readable activation or high recorder score can be a correlate,
   scaffold, sink, or consumer-specific signal. Causal claims need matched nulls, dose, collateral,
   held-out behavior, and custody.
3. **Routing is not semantics.** MoE route concentration and cache locality describe conditional
   execution. They do not identify expert concepts without semantic and causal controls.
4. **Formation changes the explanation.** Curriculum, adaptation, checkpoint, and initialization
   can move a capability wall, change policy, or migrate local carriers while preserving a broader
   function. Endpoint behavior alone cannot tell which happened.
5. **Consumers define equivalence.** A state can be equivalent for a scorer, a decoder, a next-token
   readout, a VAE, or a reference-KV consumer without being equivalent for another consumer.
6. **Execution is part of the result.** Dtype, quantization, offload, scheduler call count, CFG
   branch order, cache lifetime, host pressure, and dependency closure can change the measured
   computation. A failed route is not a model-negative result.
7. **Cross-model regularities are relational.** The promising invariant is a role or transport
   relation under a declared consumer, not a literal head/layer identity or one universal latent
   coordinate system.

## 8. What is established, and what is still missing

### Established or strongly supported locally

- The workspace has a functioning custody-aware run stack: mrun model execution, paged and streamed
  routes, artifact manifests, MinIO/MLflow/Trackio integration where available, and independent
  readback for major panels.
- Qwen generation contrasts, MoE routing geometry, Pythia checkpoint formation, and Mamba/FNet
  topology differences are measured under declared local contracts.
- Image-model architecture/custody coverage is broad, and the original shared image panel gives
  useful bounded behavior and failure trends across U-Net, flow-transformer, single-stream, linear-
  attention, MoE, and masked-token regimes.
- FLUX.2 Klein 4B has the strongest current natural-image internal trend: late target-image
  readability plus a distributed intervention route under a fixed assay, with counter-controls and
  failed gates retained.
- Controlled organisms expose the difference between a trend, a calibrated instrument, and a
  terminal mechanism claim.

### Not established

- A universal scale law, generation law, expert-semantic law, or cross-architecture circuit.
- A complete natural-model causal graph from source through transport to consumer.
- A compact image concept module or portable FLUX route.
- A native Qwen base-model conjunction/uniqueness circuit from the adapter studies.
- A general model-runtime speed claim inferred from one backend, dtype, or memory policy.
- A claim that failed SANA, Dev, Nucleus, Meissonic, Hunyuan, DeepSeek, or calibration routes prove
  model absence; those failures instead bound the instrument, custody, or terminal claim.

## Source-of-truth map

Use these in order when a summary and a raw record differ:

1. The latest frozen result artifact and independent verifier;
2. the current experiment owner and run ledger;
3. the dated synthesis page;
4. older blog or index prose.

Core sources:

- [[generative-model-analysis|Generative Model Analysis Index]] — broad program and model coverage.
- [[../generative-model-wiki|Generative Model Wiki]] — modality-first navigation and evidence ladder.
- [[../../experiments/2026-07-24-generative-image-model-atlas/CURRENT_SYNTHESIS.md|Generative Image Atlas current synthesis]].
- [[../../experiments/2026-07-24-generative-image-model-atlas/ARCHITECTURE_CONCEPT_MATRIX.md|Image architecture/concept matrix]].
- [[../../experiments/2026-07-24-generative-image-model-atlas/MECHANISM_AUDIT.md|Image mechanism/admission audit]].
- [[../../experiments/2026-08-01-233923-bfl-generational-model-observatory/RUNS.md|BFL run ledger]].
- [[../../experiments/2026-08-01-233923-bfl-generational-model-observatory/reports/BEHAVIOR_TRENDS.md|BFL behavior trends]].
- [[../../experiments/2026-08-01-233923-bfl-generational-model-observatory/reports/PHYSIOLOGY_TRENDS.md|BFL physiology trends]].
- [[../../experiments/2026-08-01-233923-bfl-generational-model-observatory/reports/NATURAL_CAUSAL_TRENDS.md|BFL natural causal trends]].
- [[../../experiments/2026-07-18-195133-generational-model-observatory/MOE-INSTRUMENT.md|MoE instrument contract]].
- [[../../experiments/2026-07-18-195133-generational-model-observatory/study.moe.json|Frozen six-model MoE study]].
- [[../experiments/generational-model-observatory-g0|G0 owner]], [[../experiments/generational-model-observatory-g1|G1 owner]], and [[../experiments/generational-model-observatory-g2-moe|G2 owner]].
- [[../experiments/scale-panel|Original dense-model scale panel]] and [[../experiments/scale-panel-reaudit|provenance-gated scale re-audit]].
- [[../../experiments/2026-07-27-cross-family-cartridge-socket-smollm2/RESULTS.md|SmolLM2 cross-family cartridge result]] and [[../../experiments/2026-07-27-structured-router-cartridge/RESULTS.md|structured-router result]].
- [[../experiments/flux-fnet-mamba-mechanism-atlas|FNet/Mamba atlas]].
- [[../experiments/pythia-70m-conjunctive-routing-mechanism-packet|Pythia mechanism packet]].
- [[../indexes/model-analysis-source-coverage|historical source coverage]] and [[../indexes/model-analysis-local-experiments-coverage|local experiment coverage]].

This page should be updated when a new canonical model-bearing run, static subject, or independent
adjudication changes a model's evidence state. Do not overwrite historical run outcomes; add a new
dated digest and preserve the predecessor identity.
