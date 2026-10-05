---
title: "48-hour related experiment coverage"
type: research-evidence-audit
status: completed-coverage-audit
date: 2026-10-01
updated: 2026-10-01T22:03:01-07:00
window_start: 2026-09-29T18:22:25-07:00
window_end: 2026-10-01T18:22:25-07:00
tags: [scaffolds, dynamic-circuits, experiment-coverage, evidence, native-consumer]
---

# 48-hour related experiment coverage

The [architecture outline](outline.md#appendix-e--related-experiment-coverage-for-the-last-48-hours) now accounts for the directly related and neighboring experiment families found in the requested 48-hour window. It includes formation/commit/mediation, source/read addressing, feedback, diffusion cut/operator controls, Mamba clocks and quotients, hybrid architectures, runtime memory, numerical formats, controlled FieldLM organisms, and instrument/goal-evaluation context. No model jobs were launched for this audit.

## Window, sources, and counting

The fixed window is **September 29, 2026 18:22:25 through October 1, 2026 18:22:25 PDT** (UTC September 30 01:22:25 through October 2 01:22:25). The endpoint was fixed when this audit began. Later evidence already entering the shared outline is preserved with its own date; it does not silently move the inventory window.

Read-only scheduler discovery returned 2,044 total saved jobs. The [saved window inventory](experiment-coverage-jobs-2026-10-01.json) selects **532 jobs** with at least one creation, start, or finish event inside the window, spanning **350 experiment labels**. Current states at that snapshot are 376 succeeded, 55 failed, 46 cancelled, 41 killed for VRAM, 12 killed for RAM, and two timed out. A job may have started before the window and finished inside it. These are execution dispositions, not scientific verdicts, independent samples, or experiment-family counts. The derived inventory contains only job identity, experiment label, state, and event times; commands, environment, credentials, and full scheduler payloads are omitted.

File discovery across twenty scientific roots returned **933 recently modified candidate records**: 859 in Saturn, 61 in research, twelve in the PhaseLock/FieldLM worktree, and one in spectral-phase-format-research. The filter included Markdown and report/result/receipt/analysis/manifest JSON records; custody copies, summaries, and multiple arms are not independent evidence. Repo history was used as a cross-check, including uncommitted local results. The date-near catalog below contains 53 Saturn package directories and 44 blog posts with September 29–October 1 origins. Some originated before the 48-hour window; they remain clearly marked background or updates. Findings and primary native reports were reviewed by family, rather than interpreting every file mtime as a new execution.

Execution receipts and report/source identity outrank folder names, Git commit dates, blog dates, and mtimes. The E7 FLUX five-seed color panel is `job-8d4a3845a671`, despite its stale scheduler label `flux2-residual-deletion-full-5seed`; it is counted once under that scheduler label and linked separately by its report identity. Sep 25-origin exact-join packages have genuine Sep 30 follow-up executions. The Sep 29 diffusion-memory document explicitly has no new GPU timing run. The Black Mamba quotient work is a local CPU replay of older toy checkpoints without Saturn/mrun custody. The connected SDXL lane had design/code, but no receipt at the cutoff. Connected Mamba held `job-f2943e224e03` finished at **18:24:13 PDT**, after the cutoff; subsequent connected Qwen correction/held files are also later extensions to check under their own run dates.

## What changed in the outline

The strongest additions are the 42-row Qwen E20 source→recipient-formed L22–27 store→native-consumer panel and its E17/E19 commit/window context; Qwen3 reverse-source held read/rescue; Pythia relay/writer recovered loss; E12/E13/E18 address/read-join contrasts; the computed-object addition panel; full Mamba sweeps and writer-clock interpretation; and Falcon's attention/SSM split. Main sections retain denominators, supplied addresses, task competence, signed ratios, and effective replication scope.

Diffusion coverage now links off-route spans, joint-region time accumulation, residual deletion, five-seed color, Klein9B, SDXL and perturbation-method comparisons. It preserves the progress-to-null correction and the difference between E1b joint-region block-output zeroing and E1c residual/input deletion, along with non-specific sham/deletion, failed specificity, mixed lighting, and SDXL early-step necessity bottleneck. A strict subtype miss does not erase a causal effect or establish mechanism absence.

Systems and adjacent sections now include Open Bench, SourceFrameStack, PhaseLock long-state/recall, integer-phase training, SPF native forward/backward and factored precision, FieldLM joint-Wiki/axis-web/relation reading, frozen WS1 substrate results and the weak development-only WS2 English boundary. Exact replay, supplied algebra, native numerical behavior, and learned semantic competence remain separate claims. Numerical speed/reference corrections and unexecuted/resource-failed attempts remain visible.

The previous [status audit](evidence-status-audit-2026-10-01.md) retains its original dated inspection and receives an additive update for C5 route-produced write/future access and the newer connected/checkpoint records. The initial “proposal only” route-attribution row is historical, not current status.

## Later E10 completed answer update

The [completed-answer and timing reproduction](../../../saturn/experiments/2026-10-01-e10-completed-answer-rerun/FINDINGS.md) adds two completed full mrun jobs after this inventory's fixed 18:22:25 PDT cutoff: Qwen0.5 `job-527c598e9bc0` and Qwen1.5 `job-d637c4110a59`. Each collects all 48 original rows, while retaining the historical 32/30 primary intervention denominators. These jobs are later corrective evidence, not additions to the frozen 532-job inventory or its disposition counts.

The [outline's E10 update](outline.md#111-operationstate-conjunctions-and-continuation) and [Obsidian experiment note](../../../obsidian/experiments/e10-completed-answer-rerun.md) document completed wrong removal answers on 26/32 and 3/30 rows, correct repairs on 6/32 and 25/30, two Qwen1.5 unresolved endpoints, and completed donor authorship on 19/32 and 30/30. All eight later products complete correctly despite the historical leading-number flag pattern. Generated-chain handoff and numerical-prefill limits remain explicit. Historical raw reports and the inventory window are preserved.

## Scheduler family map

These grouping labels are a coverage index over scheduler names. Primary reports resolve stale or reused names. Each family is mentioned in Appendix E; engineering success alone does not set its scientific claim level.

| Scheduler family | Jobs | Dispositions |
|---|---:|---|
| `ablation-method-sensitivity` | 7 | failed: 3, killed_ram: 1, succeeded: 3 |
| `circuit-tracer-comparison` | 13 | cancelled: 1, failed: 3, killed_vram: 1, succeeded: 8 |
| `connected-architecture` | 6 | failed: 1, succeeded: 5 |
| `e10-cot` | 6 | killed_ram: 1, killed_vram: 1, succeeded: 4 |
| `e12-bucket-exact-address` | 9 | failed: 2, succeeded: 7 |
| `e13-time-circuit-read-join` | 5 | succeeded: 5 |
| `e14-hybrid-attn-ssm` | 5 | cancelled: 1, killed_vram: 1, succeeded: 3 |
| `e18-bucket-join-time-reads` | 8 | killed_ram: 3, succeeded: 5 |
| `e8-klein9b-nine-gate` | 4 | cancelled: 1, succeeded: 3 |
| `e9-sdxl-four-quadrant` | 2 | succeeded: 2 |
| `fieldlm-axis-web-ws1` | 20 | cancelled: 3, failed: 1, succeeded: 15, timeout: 1 |
| `flux2-offroute-span` | 2 | succeeded: 2 |
| `flux2-residual-deletion` | 4 | succeeded: 4 |
| `flux2-time-accumulation` | 2 | succeeded: 2 |
| `full-layer-sweeps` | 35 | cancelled: 2, failed: 1, killed_ram: 1, succeeded: 31 |
| `grail-debugger-evaluation` | 20 | cancelled: 3, failed: 6, killed_ram: 1, killed_vram: 3, succeeded: 7 |
| `grail-internals-verifier` | 24 | cancelled: 2, failed: 4, killed_vram: 6, succeeded: 12 |
| `grail-recovered-loss` | 10 | failed: 1, killed_vram: 1, succeeded: 8 |
| `hidden-objective-excluded-context` | 28 | cancelled: 4, failed: 6, killed_vram: 2, succeeded: 16 |
| `ird-battery` | 1 | failed: 1 |
| `isolated-swap-reruns` | 9 | cancelled: 1, failed: 2, succeeded: 6 |
| `mamba-full-layer-sweeps` | 9 | killed_vram: 2, succeeded: 7 |
| `mamba-state-cut-certificate` | 8 | cancelled: 1, succeeded: 7 |
| `mamba-writer-clock` | 3 | succeeded: 3 |
| `mvm-cot` | 3 | succeeded: 3 |
| `older-origin-exact-join` | 5 | succeeded: 5 |
| `open-bench` | 10 | cancelled: 2, failed: 4, succeeded: 4 |
| `phase-integer-training` | 4 | failed: 1, succeeded: 3 |
| `phaselock-bithacks` | 45 | cancelled: 5, failed: 5, killed_ram: 2, killed_vram: 2, succeeded: 31 |
| `phaselock-context-and-free-wins` | 32 | failed: 1, killed_ram: 1, succeeded: 29, timeout: 1 |
| `phaselock-gauge-leak` | 50 | cancelled: 3, killed_ram: 1, killed_vram: 9, succeeded: 37 |
| `phaselock-review-fixes` | 9 | cancelled: 3, killed_vram: 1, succeeded: 5 |
| `pythia-recovered-loss` | 7 | failed: 1, killed_vram: 1, succeeded: 5 |
| `qwen-context-interface` | 6 | succeeded: 6 |
| `qwen-formation-and-vm` | 5 | succeeded: 5 |
| `qwen-head-edge` | 2 | failed: 1, succeeded: 1 |
| `qwen-route-future-attribution` | 2 | succeeded: 2 |
| `qwen-routing-mediation` | 1 | succeeded: 1 |
| `qwen3-reverse-source` | 3 | killed_vram: 2, succeeded: 1 |
| `room-studio-cancelled` | 1 | cancelled: 1 |
| `saturn-publication-fast-lane` | 15 | cancelled: 5, killed_vram: 2, succeeded: 8 |
| `scaffold-confirmation` | 15 | failed: 2, succeeded: 13 |
| `scaffold-dynamic-circuits` | 28 | failed: 6, killed_vram: 1, succeeded: 21 |
| `source-frame-stack` | 3 | cancelled: 1, succeeded: 2 |
| `spf-factored-precision` | 5 | failed: 1, succeeded: 4 |
| `spf-native-boundary` | 41 | cancelled: 7, failed: 2, killed_ram: 1, killed_vram: 6, succeeded: 25 |

## Date-near Saturn source catalog

Every directory below has a direct mention/link in Appendix E. This catalog records source availability, not fifty-three newly completed experiments. The outline and primary record supply each family's execution and claim boundary.

| Package | Entry record |
|---|---|
| `2026-09-29-causal-context-vm-integration` | [FINDINGS.md](../../../saturn/experiments/2026-09-29-causal-context-vm-integration/FINDINGS.md) |
| `2026-09-29-diffusion-memory-reuse-audit` | [FINDINGS.md](../../../saturn/experiments/2026-09-29-diffusion-memory-reuse-audit/FINDINGS.md) |
| `2026-09-29-phaselock-context-overflow` | [INTERPRETATION.md](../../../saturn/experiments/2026-09-29-phaselock-context-overflow/INTERPRETATION.md) |
| `2026-09-29-phaselock-free-wins` | [FINDINGS.md](../../../saturn/experiments/2026-09-29-phaselock-free-wins/FINDINGS.md) |
| `2026-09-29-phaselock-long-chat` | [REPORT.md](../../../saturn/experiments/2026-09-29-phaselock-long-chat/REPORT.md) |
| `2026-09-29-phaselock-long-session` | [REPORT.md](../../../saturn/experiments/2026-09-29-phaselock-long-session/REPORT.md) |
| `2026-09-30-ablation-method-sensitivity` | [FINDINGS.md](../../../saturn/experiments/2026-09-30-ablation-method-sensitivity/FINDINGS.md) |
| `2026-09-30-black-mamba-quotient-theorem` | [FINDINGS.md](../../../saturn/experiments/2026-09-30-black-mamba-quotient-theorem/FINDINGS.md) |
| `2026-09-30-blind-final-boss-certification` | [PLAN.md](../../../saturn/experiments/2026-09-30-blind-final-boss-certification/PLAN.md) |
| `2026-09-30-circuit-tracer-head-to-head` | [FINDINGS.md](../../../saturn/experiments/2026-09-30-circuit-tracer-head-to-head/FINDINGS.md) |
| `2026-09-30-e12-bucket-exact-address` | [FINDINGS.md](../../../saturn/experiments/2026-09-30-e12-bucket-exact-address/FINDINGS.md) |
| `2026-09-30-e13-time-circuit-read-join` | [FINDINGS.md](../../../saturn/experiments/2026-09-30-e13-time-circuit-read-join/FINDINGS.md) |
| `2026-09-30-e18-bucket-join-time-reads` | [FINDINGS.md](../../../saturn/experiments/2026-09-30-e18-bucket-join-time-reads/FINDINGS.md) |
| `2026-09-30-e4-pythia-recovered-loss` | [FINDINGS.md](../../../saturn/experiments/2026-09-30-e4-pythia-recovered-loss/FINDINGS.md) |
| `2026-09-30-e7-flux-color-multiseed` | [FINDINGS.md](../../../saturn/experiments/2026-09-30-e7-flux-color-multiseed/FINDINGS.md) |
| `2026-09-30-flux2-joint01-time-accumulation` | [FINDINGS.md](../../../saturn/experiments/2026-09-30-flux2-joint01-time-accumulation/FINDINGS.md) |
| `2026-09-30-flux2-offroute-span-sweep` | [FINDINGS.md](../../../saturn/experiments/2026-09-30-flux2-offroute-span-sweep/FINDINGS.md) |
| `2026-09-30-flux2-residual-deletion` | [FINDINGS.md](../../../saturn/experiments/2026-09-30-flux2-residual-deletion/FINDINGS.md) |
| `2026-09-30-full-layer-sweeps` | [PLAN.md](../../../saturn/experiments/2026-09-30-full-layer-sweeps/PLAN.md) |
| `2026-09-30-grail-b0-internals-verifier` | [FINDINGS.md](../../../saturn/experiments/2026-09-30-grail-b0-internals-verifier/FINDINGS.md) |
| `2026-09-30-grail-g1-hidden-objective-audit` | [FINDINGS.md](../../../saturn/experiments/2026-09-30-grail-g1-hidden-objective-audit/FINDINGS.md) |
| `2026-09-30-grail-g2-recovered-loss` | [FINDINGS.md](../../../saturn/experiments/2026-09-30-grail-g2-recovered-loss/FINDINGS.md) |
| `2026-09-30-grail-saturn-debugger-eval` | [FINDINGS.md](../../../saturn/experiments/2026-09-30-grail-saturn-debugger-eval/FINDINGS.md) |
| `2026-09-30-isolated-swap-reruns` | [FINDINGS.md](../../../saturn/experiments/2026-09-30-isolated-swap-reruns/FINDINGS.md) |
| `2026-09-30-mamba-full-layer-sweeps` | [FINDINGS.md](../../../saturn/experiments/2026-09-30-mamba-full-layer-sweeps/FINDINGS.md) |
| `2026-09-30-mamba-state-cut-certificate` | [FINDINGS.md](../../../saturn/experiments/2026-09-30-mamba-state-cut-certificate/FINDINGS.md) |
| `2026-09-30-mamba-writer-clock` | [FINDINGS.md](../../../saturn/experiments/2026-09-30-mamba-writer-clock/FINDINGS.md) |
| `2026-09-30-mvm-mamba-cot` | [FINDINGS.md](../../../saturn/experiments/2026-09-30-mvm-mamba-cot/FINDINGS.md) |
| `2026-09-30-phase-integer-training-poc` | [FINDINGS.md](../../../saturn/experiments/2026-09-30-phase-integer-training-poc/FINDINGS.md) |
| `2026-09-30-phaselock-bithacks` | [analysis-v1.md](../../../saturn/experiments/2026-09-30-phaselock-bithacks/analysis-v1.md) |
| `2026-09-30-phaselock-gauge-leak` | [FINDINGS-tier1.md](../../../saturn/experiments/2026-09-30-phaselock-gauge-leak/FINDINGS-tier1.md) |
| `2026-09-30-phaselock-review-fixes` | [2026-09-30-phaselock-review-fixes](../../../saturn/experiments/2026-09-30-phaselock-review-fixes/) |
| `2026-09-30-qwen3-reverse-source-mechanism` | [FINDINGS.md](../../../saturn/experiments/2026-09-30-qwen3-reverse-source-mechanism/FINDINGS.md) |
| `2026-09-30-saturn-pub-fast-lane` | [2026-09-30-saturn-pub-fast-lane](../../../saturn/experiments/2026-09-30-saturn-pub-fast-lane/) |
| `2026-09-30-source-frame-stack` | [FINDINGS.md](../../../saturn/experiments/2026-09-30-source-frame-stack/FINDINGS.md) |
| `2026-09-30-space-and-time-circuits` | [README.md](../../../saturn/experiments/2026-09-30-space-and-time-circuits/README.md) |
| `2026-09-30-spf-factored-precision` | [FINDINGS.md](../../../saturn/experiments/2026-09-30-spf-factored-precision/FINDINGS.md) |
| `2026-09-30-spf-native-boundary` | [2026-09-30-spf-native-boundary](../../../saturn/experiments/2026-09-30-spf-native-boundary/) |
| `2026-10-01-connected-architecture` | [README.md](../../../saturn/experiments/2026-10-01-connected-architecture/README.md) |
| `2026-10-01-e10-cot-intermediate-steps` | [FINDINGS.md](../../../saturn/experiments/2026-10-01-e10-cot-intermediate-steps/FINDINGS.md) |
| `2026-10-01-e14-hybrid-attn-ssm` | [FINDINGS.md](../../../saturn/experiments/2026-10-01-e14-hybrid-attn-ssm/FINDINGS.md) |
| `2026-10-01-e8-klein9b-nine-gate` | [FINDINGS.md](../../../saturn/experiments/2026-10-01-e8-klein9b-nine-gate/FINDINGS.md) |
| `2026-10-01-e9-sdxl-four-quadrant` | [FINDINGS.md](../../../saturn/experiments/2026-10-01-e9-sdxl-four-quadrant/FINDINGS.md) |
| `2026-10-01-open-bench` | [RESULTS.md](../../../saturn/experiments/2026-10-01-open-bench/RESULTS.md) |
| `2026-10-01-open-bench-families` | [README.md](../../../saturn/experiments/2026-10-01-open-bench-families/README.md) |
| `2026-10-01-qwen-formation-replay` | [FINDINGS.md](../../../saturn/experiments/2026-10-01-qwen-formation-replay/FINDINGS.md) |
| `2026-10-01-qwen-head-edge-topology` | [FINDINGS.md](../../../saturn/experiments/2026-10-01-qwen-head-edge-topology/FINDINGS.md) |
| `2026-10-01-qwen-route-write-future-attribution` | [FINDINGS.md](../../../saturn/experiments/2026-10-01-qwen-route-write-future-attribution/FINDINGS.md) |
| `2026-10-01-qwen-routing-mediation` | [FINDINGS.md](../../../saturn/experiments/2026-10-01-qwen-routing-mediation/FINDINGS.md) |
| `2026-10-01-qwen-scaffold-context-poc` | [FINDINGS.md](../../../saturn/experiments/2026-10-01-qwen-scaffold-context-poc/FINDINGS.md) |
| `2026-10-01-qwen-virtual-memory-audit` | [MAP.md](../../../saturn/experiments/2026-10-01-qwen-virtual-memory-audit/MAP.md) |
| `2026-10-01-scaffold-confirmation` | [FINDINGS.md](../../../saturn/experiments/2026-10-01-scaffold-confirmation/FINDINGS.md) |
| `2026-10-01-scaffold-dynamic-circuits` | [RESULTS.md](../../../saturn/experiments/2026-10-01-scaffold-dynamic-circuits/RESULTS.md) |

## Additional primary sources outside the date-named packages

- [Sep 25 exact-join admission/ambiguity handoff](../../../saturn/experiments/2026-09-25-ar-exact-join-admission/HANDOFF.md): new in-window dose/full-vocabulary/ordinal-address follow-ups in an older-origin package.
- [Joint Wiki/FieldLM candidate closure](../../../spf-wt-phaselock/domains/ml/spectral-native/docs/wiki-joint-field-20260929-findings.md): native component preservation, weak text reading, enumeration correction and competing interpretations.
- [Axis-web reasoning](../../../spf-wt-phaselock/domains/ml/spectral-native/docs/axis-web-reasoning-20260930-findings.md) and [relation-axis reader](../../../spf-wt-phaselock/domains/ml/spectral-native/docs/relation-axis-reader-20260930-findings.md): supplied algebra, synthetic identities and causal definition rebinding.
- [WS1 Wikipedia substrate](../../../spf-wt-phaselock/domains/ml/spectral-native/docs/wiki-substrate-20260930-findings.md): eight sealed predictions, graded alternatives versus early staged reading, weak supervision and supplied ID queries.
- [WS2/2Wiki coverage index](../../../spf-wt-phaselock/domains/ml/spectral-native/results/twowiki-text-20260930-index1.json), [development smoke](../../../spf-wt-phaselock/domains/ml/spectral-native/results/twowiki-text-20260930-smoke3.json), and [proposal](../../../spf-wt-phaselock/domains/ml/spectral-native/docs/twowiki-text-20260930-proposal.md): completed indexing/development runs, weak learned front-end, unopened target. The earlier blog's prospective wording does not erase these smoke results.
- [Rotation Swamping paper](../phaselock-kv-shifts/paper.md), [technical-blog variation](../phaselock-kv-shifts/blog.md), and [SPF two-domain machine note](../../../obsidian/spf/2026-09-30-spf-native-transformer-two-domain-machine.md): numerical formulation and partial measurements; overlapping primary experiments are counted once.
- [Scene-generator demo](../../demos/scene-generator.md), [scene-generator paper](../../demos/docs/scene-generator-paper.md), [character register](../../demos/jen-character-register.md), and [spatial relation/transport](../../demos/flux-relations-and-transport.md): earlier exact-source/native-output, register and supplied-rectangle evidence revisited by the recent survey, rather than fresh executions.
- [Main space/time paper](../space-and-time-circuits/paper.md), [time-emphasis variant](../space-and-time-circuits/time-emphasis-paper.md), [architectural paper](architectural-paper.md), [bridge paper](bridge-paper.md), and [earlier paper](paper.md): overlapping narrative variants; current corrections qualify historical drafts and critiques.
- [Integral Residual Dynamics](../integral-residual-dynamics/paper.md) and [Capabilities as Transactions](../capabilities-as-transactions/paper.md): related recent theory/transaction drafts with overlapping inherited evidence and later circuit-dossier corrections.

## Narrative source catalog

These posts are accounted for as experiment reports, recent syntheses, proposals, or background. A post's date does not prove when its underlying experiment ran. The frontier overview and its twelve essays organize open architecture questions; they are not twelve independent new assays. Older FieldLM stages and earlier scene/compiler results remain supporting history.

| Post | Document timing relative to fixed window |
|---|---|
| [The Field Reads Its Own Rules](../../../obsidian/blog/2026-09-29-010736-the-field-reads-its-own-rules.md) | Pre-window background |
| [2026-09-29 11:53:01 — Model Virtual Memory: From a Request to a Native Answer](../../../obsidian/blog/2026-09-29-115301-model-virtual-memory-from-a-request-to-a-native-answer.md) | Pre-window background |
| [A Small Model That Reads and Runs Its Rules](../../../obsidian/blog/2026-09-29-122123-a-small-model-that-reads-and-runs-its-rules.md) | Pre-window background |
| [2026-09-29 12:45:23 — My Top 20 Experiments and Tools](../../../obsidian/blog/2026-09-29-124523-top-20.md) | Pre-window background |
| [FieldLM: An Overview](../../../obsidian/blog/2026-09-29-125620-fieldlm-overview.md) | Pre-window origin; document updated in window |
| [2026-09-29 13:58:47 — Twenty experiments and tools with the most interesting futures](../../../obsidian/blog/2026-09-29-135847-top-20.md) | Pre-window background |
| [Growing FieldLM structure without gradient training](../../../obsidian/blog/2026-09-29-144831-growing-fieldlm-structure-without-gradient-training.md) | Pre-window background |
| [FieldLM learns to share arguments across clauses](../../../obsidian/blog/2026-09-29-152538-fieldlm-learns-to-share-arguments-across-clauses.md) | Pre-window background |
| [2026-09-29 19:13:30 PhaseLock at 100k tokens with a 32k cache](../../../obsidian/blog/2026-09-29-191330-phaselock-at-100k-tokens-with-a-32k-cache.md) | Written in window; execution date requires receipt |
| [2026-09-30 01:19:58 — Shared Memory and Batched Inference for Model Threads](../../../obsidian/blog/2026-09-30-011958-shared-memory-and-batched-inference-for-model-threads.md) | Written in window; execution date requires receipt |
| [Axes, a Web and a Reasoning Axis](../../../obsidian/blog/2026-09-30-013038-axes-web-and-a-reasoning-axis.md) | Written in window; execution date requires receipt |
| [2026-09-30-015100-compiling-model-work-for-10x-and-100x-speed](../../../obsidian/blog/2026-09-30-015100-compiling-model-work-for-10x-and-100x-speed.md) | Written in window; execution date requires receipt |
| [Where We Went Wrong: Stages, Starvation and Synthetic Worlds](../../../obsidian/blog/2026-09-30-015824-where-we-went-wrong-stages-starvation-and-synthetic-worlds.md) | Written in window; execution date requires receipt |
| [PhaseLock: What Immutable Keys Buy](../../../obsidian/blog/2026-09-30-032252-phaselock-what-immutable-keys-buy.md) | Written in window; execution date requires receipt |
| [From IDs to English: FieldLM Meets Real Questions](../../../obsidian/blog/2026-09-30-074500-from-ids-to-english.md) | Written in window; execution date requires receipt |
| [PhaseLock: Bit Hacks, Phase-Framed Pages and an SPF Arm](../../../obsidian/blog/2026-09-30-075337-phaselock-bit-hacks-phase-frames-spf.md) | Written in window; execution date requires receipt |
| [2026-09-30 10:31:48 — Following a Qwen Answer Back to Its Source](../../../obsidian/blog/2026-09-30-103148-following-a-qwen-answer-back-to-its-source.md) | Written in window; execution date requires receipt |
| [2026-09-30 10:52:06 — Source Frame Stacks Beside StateCuts](../../../obsidian/blog/2026-09-30-105206-source-frame-stacks-beside-statecuts.md) | Written in window; execution date requires receipt |
| [2026-09-30 11:54:43 — Phase Integers in Model Training](../../../obsidian/blog/2026-09-30-115443-phaselock-phase-integers-in-model-training.md) | Written in window; execution date requires receipt |
| [2026-09-30 13:05:02 — The Holy-Grail Checklist](../../../obsidian/blog/2026-09-30-130502-the-holy-grail-checklist.md) | Written in window; execution date requires receipt |
| [One Rounding per Boundary: SPF and Exact Accumulation in Training](../../../obsidian/blog/2026-09-30-131306-spf-exact-accumulation-one-rounding-per-boundary.md) | Written in window; execution date requires receipt |
| [Where SPF Actually Wins: Exact Law Plus Low-Precision Residual](../../../obsidian/blog/2026-09-30-133642-spf-exact-law-plus-residual.md) | Written in window; execution date requires receipt |
| [Black Mamba: The Quotient That Could Not Close](../../../obsidian/blog/2026-09-30-154435-black-mamba-the-quotient-that-could-not-close.md) | Written in window; execution date requires receipt |
| [Where the Error Lives: One Day Taking Training Numerics Apart with SPF](../../../obsidian/blog/2026-09-30-163532-spf-native-training-where-the-error-lives.md) | Written in window; execution date requires receipt |
| [2026-09-30 16:51:58 — The Scene Generator Survey: The Machine Is Prompt-Agnostic, the Program Is Not](../../../obsidian/blog/2026-09-30-165158-the-scene-generator-survey-the-machine-is-prompt-agnostic-the-program-is-not.md) | Written in window; execution date requires receipt |
| [2026-10-01 12:53:22 — Stable scaffolds and dynamic circuits across diffusion language and state space models](../../../obsidian/blog/2026-10-01-125322-stable-scaffolds-and-dynamic-circuits.md) | Written in window; execution date requires receipt |
| [2026-10-01 13:19:07 — What Saturn VM and model virtual memory have demonstrated](../../../obsidian/blog/2026-10-01-131907-saturn-vm-model-virtual-memory-evidence-checklist.md) | Written in window; execution date requires receipt |
| [2026-10-01-134012-frontier-interpretability-questions-and-our-evidence](../../../obsidian/blog/2026-10-01-134012-frontier-interpretability-questions-and-our-evidence.md) | Written in window; execution date requires receipt |
| [FQ03: Can Models Bind Meaning to Reusable Addresses?](../../../obsidian/blog/2026-10-01-134012-open-question-binding-and-semantic-addressing.md) | Written in window; execution date requires receipt |
| [A source forms the store that controls the answer](../../../obsidian/blog/2026-10-01-134012-open-question-causal-faithfulness.md) | Written in window; execution date requires receipt |
| [FQ02: What Are the Right Computational Units, and How Complete Is Feature Coverage?](../../../obsidian/blog/2026-10-01-134012-open-question-computational-units-and-feature-coverage.md) | Written in window; execution date requires receipt |
| [Exact ownership is not compression](../../../obsidian/blog/2026-10-01-134012-open-question-efficient-interpretable-models.md) | Document activity in window |
| [What the blind audits measured](../../../obsidian/blog/2026-10-01-134012-open-question-hidden-objectives-and-deception.md) | Written in window; execution date requires receipt |
| [FQ06: How Does Training Change Mechanisms, Not Just Scores?](../../../obsidian/blog/2026-10-01-134012-open-question-how-training-changes-mechanisms.md) | Written in window; execution date requires receipt |
| [What context constructs](../../../obsidian/blog/2026-10-01-134012-open-question-in-context-computation.md) | Written in window; execution date requires receipt |
| [2026-10-01 13:40:12 — Do models have a macroscopic organization that interpretability can reuse?](../../../obsidian/blog/2026-10-01-134012-open-question-macroscopic-model-organization.md) | Written in window; execution date requires receipt |
| [The supplied trace result](../../../obsidian/blog/2026-10-01-134012-open-question-reasoning-and-monitorability.md) | Document activity in window |
| [What crosses the boundary](../../../obsidian/blog/2026-10-01-134012-open-question-reusable-model-programs.md) | Document activity in window |
| [2026-10-01 13:40:12 — How are spatial relations and world-model representations organized inside generative models?](../../../obsidian/blog/2026-10-01-134012-open-question-spatial-and-world-model-representations.md) | Written in window; execution date requires receipt |
| [2026-10-01 13:40:12 — What would useful and scalable interpretability look like?](../../../obsidian/blog/2026-10-01-134012-open-question-useful-and-scalable-interpretability.md) | Written in window; execution date requires receipt |
| [2026-10-01 14:16:28 — The question decided which stored fact mattered](../../../obsidian/blog/2026-10-01-141628-the-question-decided-which-stored-fact-mattered.md) | Written in window; execution date requires receipt |
| [2026-10-01 14:48:43 — The Circuit Had to Be Formed Before It Could Be Read](../../../obsidian/blog/2026-10-01-144843-the-circuit-had-to-be-formed-before-it-could-be-read.md) | Written in window; execution date requires receipt |
| [2026-10-01 17:02:49 — The Written State Changed the Next Answer](../../../obsidian/blog/2026-10-01-170249-the-written-state-changed-the-next-answer.md) | Written in window; execution date requires receipt |
| [2026-10-01 17:54:16 — Routing Rewrote Memory and Changed the Next Read](../../../obsidian/blog/2026-10-01-175416-routing-rewrote-memory-and-changed-the-next-read.md) | Written in window; execution date requires receipt |

## Completeness and limits

All 53 date-near Saturn directories are named in the outline's coverage map; all 532 selected scheduler job IDs are retained once in the saved inventory. All scheduler-label groups have a named coverage family, including cancelled room-studio work, failed IRD, publication/loading checks, Grail/debugger benchmarks and hidden-objective context. Recent blog/paper variations and older-origin in-window follow-ups have explicit source links. The direct mechanism additions were checked against findings/native reports; primary custody and historic statuses are not rewritten by this audit.

This is completeness within the inspected workspace roots and scheduler snapshot, not a claim that every external or unsaved run was recoverable. The search did not infer new scientific evidence from absent files, passing execution, document updates, repeated receipt copies, or proposals. It added coverage and corrected stale current-status prose; it did not certify a universal architecture, automatic semantic addressing, autonomous loops, a physical spacetime metric, or production serving performance.
