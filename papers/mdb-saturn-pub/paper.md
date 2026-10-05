---
title: "mdb and saturn-pub: Durable, Receipted, Forkable Execution of Frozen Transformer, State-Space and Diffusion Models"
author: Jacob Hollenbeck
type: research-paper
status: draft
date: 2026-10-05
evidence_cutoff: 2026-10-05
tags: [tools, interpretability, systems, transformers, state-space-models, diffusion, causal-intervention, reproducibility, receipts, model-virtual-memory]
---

# mdb and saturn-pub: Durable, Receipted, Forkable Execution of Frozen Transformer, State-Space and Diffusion Models

Jacob Hollenbeck

> Labeling convention. Every quantitative claim is marked **MEASURED** with the file that
> holds it, or **not measured** when no file does. Every interpretation is marked
> **ASSERTED**. Paths are given relative to the research workspace root (`saturn-pub/`,
> `saturn/`, `research/`). The public toolkit is `saturn-pub` (version 0.4.0, Apache-2.0);
> MEASURED in `saturn-pub/pyproject.toml`.

## Abstract

Causal-intervention tools for interpretability run interventions *in process*: a patch is
applied, a forward pass is read, and the result lives only in that interpreter's memory, is
not sealed to the inputs and weights that produced it, and usually targets language models
alone. We describe two independently installable Python packages that make a model run an
inspectable, branchable, receipted and durable transaction over one execution contract, and
that span transformer, state-space (SSM) and diffusion families under the same contract.
`saturn-pub` (`saturn_pub`) supplies in-process sessions, forks, declared interventions,
hash-chained receipts, an offline evidence plane and reversible training. `mdb-runtime`
(`mdb`, the model-virtual-memory debugger) supplies durable cross-process sessions, managed
branch residency with eviction and hydration, portable export/import, and offline byte
verification of an exported run with no model loaded. The contract's primitives are a sealed
state cut, an isolated fork, a declared intervention (an `Act`), and an immutable receipt;
over them sit a family adapter per architecture, a memory plane, an evidence plane
(`bisect`/`xref`/`claims`/`cite`), and a transactional training controller with a persistent
version-control forest. We report MEASURED demonstrations across families: shared causal
key/value ancestry with a 40.91% key/value-byte reduction and 8/8 token agreement; durable
residency, eviction, rollback and fresh-process restart; a CUDA virtual-memory aliasing
construction that is bit-identical to flat tensors; a routed working-set decode of 1.859× at
batch four; a 2,048-page frozen-model archive read 4/4; a scene compiler reproducing 21
native RGB endpoints across five diffusion families; and a Mamba virtual memory with
bit-exact fork and 2.2x10^-4 staged replay. Five first users already rely on the contract,
including a preregistered circuit-tracer edge arbitration on Gemma-2-2B (single-feature
graph-vs-native agreement 0.846 [0.824, 0.868]). We claim no novelty over any single
primitive: each has a close antecedent in prior work, which we cite with its delta. The
honest novelty is the *combination* — transformer + SSM + diffusion, durable cross-process
forkable sessions, byte-exact replay with hash-chained receipts, native-consumer judging, and
transactional training control in one contract. We state in full what is not yet
demonstrated, including that there is no external user yet, that the efficiency wins are not
equal-semantics serving claims, and that a sibling attention-intervention harness once emitted
confident but invalid results from a causal-mask defect that its own replay checks did not catch. Three
demonstrations needed before a main-track submission are named and marked not yet done.

## 1. The problem

A causal-intervention experiment in interpretability is, operationally, a small program:
capture some internal state, change one part of it, run the rest of the model, and compare.
The standard tools make this program easy to write but leave three properties out of the
contract.

*Interventions run in process and are not durable.* A patched run exists in one interpreter.
Another process, a reviewer, or the same researcher a month later cannot reopen the exact
branched state and continue it; they re-run from a script and hope the environment matches.
nnsight/NDIF (2407.14561) and pyvene (2403.07809) build an intervention graph and execute it,
locally or on a remote server, but the unit of persistence is the program and its outputs,
not a sealed, resumable branch of model state.

*Results are unreceipted.* The number in a notebook is not bound to the bytes of the weights,
inputs, execution settings and intermediate state that produced it. When a reference path
rots or a kernel changes, nothing detects that the claim no longer rests on what it cited. A
replay audit of one lab's historical receipts found **97.7%** of hash-pinned
reference *paths* dead on the local filesystem (MEASURED,
`saturn-pub/packages/mdb/src/mdb/artifact_custody.py` module docstring; the same figure for
`(path, sha256)` pairs appears in `saturn/docs/SATURN-BIBLE.md`).

*The subject is almost always a language model.* Activation patching, attribution graphs,
SAE/transcoder readouts and steering all assume a transformer decoder. A state-space model's
recurrent/convolution state and a diffusion transformer's scheduler/latent timetable have the
same need — stop, branch, change one carrier, continue natively, compare — but no single
framework exposes them under one contract.

A fourth, quieter problem is *who judges*. A probe, a cosine readout, or an SAE ablation is an
instrument; its verdict is a candidate. The authority that should decide whether an
intervention mattered is the rest of the real model run to completion — the native consumer.
Patchscopes (2401.06102) and SelfIE (2403.10949) already make the model's own readout the
judge of a patched state; that idea is prior, and we adopt it rather than claim it.

This paper describes a contract that adds durability, receipts, cross-family coverage and
native-consumer judging to the in-process intervention, and reports what has and has not been
measured over it.

## 2. Design

### 2.1 The execution contract

The toolkit gives native execution one explicit transaction boundary (ASSERTED framing;
`saturn-pub/docs/architecture.md`):

```
capture -> fork -> inspect -> intervene -> native continuation -> compare -> commit / restore
```

Four primitives carry it (names are the public API's own; `saturn-pub/docs/architecture.md`,
"Primary concepts"):

- **StateCut** — a sealed, restorable state closure bound to model identity, execution
  contract and parent identity. It captures execution tensors and weight *identity*, not
  model weights; the same weights and contract are reconstructed separately before a restore
  (`saturn-pub/docs/usage.md`).
- **Fork** — an isolated branch from a captured parent, with its own mutable execution state
  and receipts; the parent and sibling branches are unaffected.
- **Act** — a declared intervention: its reads, writes, invalidations, parameters and
  numerical intent are stated up front, and the adapter validates slot geometry, dtype,
  device and family invariants. Non-finite, wrong-shape, unavailable-boundary and undeclared
  edits are refused fail-closed (`saturn-pub/packages/mdb/docs/EXPERIMENTS.md`).
- **Receipt** — immutable JSON evidence about one operation and its execution point. Every
  session operation records one (`saturn-pub/docs/usage.md`).

"Exactness" here means a named state boundary and numerical program reproduce bit-for-bit
within one numerical lane — not agreement across all kernels or devices
(`saturn-pub/README.md`). The native numerical contract binds framework and Python versions,
kernel, strides, device, batch and numerical settings; changing them requires a new adapter
identity (`saturn-pub/docs/architecture.md`). In-process `Act`s can execute Python and
adapters are trusted code: the declared-visibility closure is a scientific contract, not an OS
security sandbox (ASSERTED; `saturn-pub/docs/usage.md`).

### 2.2 Four planes

We organize the contract as four planes (ASSERTED organization; only the evidence plane is a
literal public-API name):

1. **Execution/state plane** — sessions, cuts, forks, `Act`s, receipts, native continuation
   (`saturn_pub.core`; `saturn-pub/src/saturn_pub/cli.py` exposes an in-process debugger whose
   every operation delegates to the public `Session` API).
2. **Memory plane** — logical tensor pages, physical sharing, private ownership, residency,
   capacity, eviction and hydration, with durable backing. MDB's memory inspection reports
   `branches`, `row_bytes`, `visible_bytes`, `total_kv_bytes`, `unique_allocations`,
   `backing_pages`, `vm_events`, `evictions`, `hydrations` for Qwen, and recurrent/image
   analogues for Mamba and diffusion (`saturn-pub/packages/mdb/docs/USAGE.md`,
   "Memory and addresses"). Pages are logical tensor storage; this is explicitly *not*
   integrated hardware CUDA virtual memory in the general runtime (see §6).
3. **Evidence plane** — a stdlib-only subpackage (`saturn_pub.evidence`) that imports neither
   torch nor the rest of the toolkit, with four verbs sharing one canonical-JSON + sha256
   custody idiom (`saturn-pub/src/saturn_pub/evidence/__init__.py`): `bisect` (first-divergence
   search backward over an ordered cut lattice via a caller probe, probes-used reported
   against a linear scan), `xref` (SQLite index over the addresses receipts cite), `claims`
   (hash-chains a claim to its evidence receipts and auto-stales it on byte drift, with a
   read-only `--check` for CI), and `cite` (binds model and input to an address at write
   time). The same four verbs serve token cuts, layer cuts, denoising steps and training
   intervals (`saturn-pub/docs/usage.md`). MDB ships the same tools as CLIs (`mdb bisect`,
   `xref`, `claims`, `watch`, `custody`, `cite`, `evidence`;
   `saturn-pub/packages/mdb/docs/USAGE.md`).
4. **Training-control plane** — a transactional checkpoint controller and a persistent
   version-control forest (§2.5).

### 2.3 Adapters per family

A family adapter declares the state addresses and native continuation boundaries for one
architecture and executes one native transition; the `Session` lifecycle is identical above
it. The qualified families are Qwen2/Qwen2.5 decoders, Mamba v1 (SSM), and the FLUX and SDXL
diffusion pipelines (`saturn-pub/packages/mdb/docs/USAGE.md`). Autoregressive stages are
`embedding -> layer 0..N -> normalization/readout -> sampling -> commit`; diffusion stages are
`conditioning -> internal blocks -> denoising -> scheduler -> VAE -> commit`, and a diffusion
cut retains the actual scheduler state, timetable and RNG — reusing only a seed is
insufficient (`saturn-pub/packages/mdb/docs/EXPERIMENTS.md`, "Resume a diffusion block"). The
fine-grained attention-edge and pre-`o_proj` interventions used by the induction certificate
support the llama-style decoders whose per-head output projection is a contiguous
`self_attn.o_proj` slice (`llama`, `mistral`, `mixtral`, `gemma`, `qwen2`, `qwen3`); other
registered families (`gpt2`, `gpt_neox`, `phi`) have a different attention layout and are
**refused fail-closed rather than silently mismeasured** (MEASURED surface;
`saturn-pub/src/saturn_pub/certificate/panel.py` docstring). A JSON-only custom adapter needs
no model framework at all (`saturn-pub/docs/usage.md`).

### 2.4 Durable export and import

A `StateCut` can be saved to a content-addressed local store that survives process exit, and a
`ReplayBundle` packages a measured program, named branch heads, the available local ancestry
and provenance (`saturn-pub/docs/usage.md`). MDB extends this to durable *cross-process*
sessions: `export` writes retained cuts and their payload closure; `resume` in a fresh process
validates model and execution identity before continuing; and `mdb verify --root ...` audits
the exported closure's bytes **without loading model weights** — a manifest-bound aggregate of
verified descriptors, payload digests, byte counts and integrity checks
(`saturn-pub/packages/mdb/docs/USAGE.md`, "Offline tools"). Byte verification is separate from
numerical compatibility: a verified export still needs the exact model and environment to
continue.

### 2.5 Transactional training and the version-control forest

`TrainingTransaction` (saturn-pub) and `DeterministicCheckpointController` (the lab's controller
name) make a bounded training interval transactional. The registered closure includes
parameters, buffers, optimizer state and topology, gradients, non-persistent buffers, module
modes, `requires_grad`, process and named RNG, and the experiment-owned cursor; candidate
evaluation must not mutate the accepted state, and rejection restores and verifies the exact
accepted fingerprint (`saturn/docs/SATURN-BIBLE.md`, "Transactional training control";
`saturn-pub/docs/training.md`). A rejected candidate means "do not continue from this state
under this policy," not "the mechanism is absent"; the trend, lineage and scores are retained.

The **Future Forest** (the lab's name for the persistent version-control store) holds immutable
content objects, parent-plus-diff nodes, observations, decisions and an accepted-head pointer,
and supports `create_root`, `fork`, `observe`, `decide`, `cherry_pick`, `three_way_merge`,
promote, prune and rewind (verbs MEASURED in `saturn/src/saturn/future_forest.py`). Promotion
is a compare-and-swap head update; rejected futures stay queryable. This gives training
ancestry git-like mechanics without claiming arbitrary semantic merges are safe (ASSERTED;
`saturn/docs/SATURN-BIBLE.md`, "Persistent Future Forest").

### 2.6 Deliberately out of scope

The contract makes **no serving-throughput claim** (ASSERTED). The general runtime is single
writer, serialized execution, local durable backing, with no production continuous batching,
no automatic per-prompt semantic discovery and no integrated CUDA virtual memory in the managed
paging path (`saturn-pub/packages/mdb/docs/USAGE.md`, "Current operating boundary"). The
private branch-search controller, automatic branch scheduling and pruning policies are outside
the public release (`saturn-pub/docs/usage.md`); the lab's compilation/route facade (named
Ouroboros internally) is likewise not part of the public toolkit. The efficiency numbers in §3
come from separate experiments with separate causes and cannot be summed into one serving
claim (ASSERTED; blog evidence review,
`obsidian/blog/2026-10-01-131907-saturn-vm-model-virtual-memory-evidence-checklist.md`).

## 3. What is measured

Each row is MEASURED at the cited file. Several demonstrations live in the lab's research
workspace (`saturn/`), summarized in the blog evidence review cited above; the public toolkit
packages (`saturn-pub/`) carry the contract and the qualification records.

### 3.1 Runtime demonstrations across families

| # | Demonstration | Model / family | n or scope | Headline number | File |
|---|---|---|---|---|---|
| 1 | Shared causal K/V ancestry, private futures | Qwen2.5 (24 decoder layers), virtual lane | 63-row common ancestor + two 14-row private tails; 8 generated steps | Raw committed K/V 1,118,208 vs 1,892,352 bytes = **40.91%** reduction; **8/8** tokens match the HF comparator (max logit diff 0.34375) | `saturn/experiments/2026-09-25-causal-context-vm-end-to-end/FINDINGS.md`; report `saturn/results/causal-context-vm-end-to-end/job-59bd7d03489a/report.json` |
| 2 | Durable residency, eviction, rollback, restart | Qwen2.5 | two resident sessions; artifact audit 12 txns / 48 plane manifests / 12 checkpoints | two sessions within **1,314,816 bytes** K/V capacity, **2** LRU evictions; reload kept the cut fingerprint; restore reproduced the first-token logit digest; **deleted the source store and reopened in a fresh process with identical next logits** | `saturn/experiments/2026-09-29-causal-context-vm-integration/FINDINGS.md`; report `saturn/results/causal-context-vm-integration/job-97e3192c594e/report.json` |
| 3 | CUDA virtual-memory aliasing of a shared prefix | Qwen K/V, RTX 4080 | two branches, shared physical prefix handles, forced FlashAttention | both branches' attention outputs **bit-identical** to flat tensors (zero max error); physical K/V **32 MiB -> 24 MiB** | `saturn/experiments/2026-09-25-virtual-context-three-closures/FINDINGS.md`; report `saturn/results/virtual-context-three-closures-cuda-vmm/job-9e7f79751e31/report.json` |
| 4 | Routed working-set decode throughput | Qwen2.5, MPS | 17 fresh-process cells; batch-4 case mounts 128 of 32,768 rows | every compact output bit-for-bit matches the suffix view; all cells beat dense median; **16/17** keep dense top-1; batch 4: cache **1.5 GiB -> 6 MiB**, **63.99 -> 119.04 tok/s = 1.859x**, 5/5 repeats win | `saturn/experiments/2026-09-26-primary-routed-working-set/FINDINGS.md`; report `saturn/results/primary-routed-working-set/local-f1a0365c04ef/report.json` |
| 5 | Small active read over a large backing archive | frozen Qwen | 2,048 self-contained fact pages; K/V in CPU | archive represents **59,356 tokens** (exceeds the 32,768-position window); selected pages answer **4/4** held questions; absent and matched-wrong pages **0/4** | `saturn/experiments/2026-09-24-spectral-virtual-context/FINDINGS.md`; report `saturn/results/spectral-virtual-context/local-guard-20260924-scale-v2/report.json` |
| 6 | Scene compiler, cross-family RGB parity | 5 diffusion families, 7 specimens | sealed source installed into a common recipient, native generator run | **21/21** recorded native RGB endpoints reproduced (a parity result: exact replay reproduces native mistakes too) | `research/demos/docs/scene-generator-paper.md`; data `research/demos/artifacts/scene-generator/artifacts/reports/cross-model-replication.json` |
| 7 | SSM virtual memory: fork and staged replay | Mamba-130M | no-op/uninstall/fork/replay battery | no-op and uninstall error **0**; fork **bit-exact**; staged native replay max error **~2.2x10^-4** with matching argmax; 24-layer necessity profile reproduced bit-for-bit; clock reconstruction within ~2.8x10^-5 | `saturn/experiments/2026-09-30-mvm-mamba-cot/FINDINGS.md`; report `saturn/experiments/2026-09-30-mvm-mamba-cot/results/mamba-7075c40c839b/report.json` |

The four efficiency results (rows 1, 3, 4, 5) have **different causes** — sharing removes
duplicate ancestry, hardware VMM changes the backing allocation, working-set selection reduces
the rows eligible for attention, paging changes residency — and are not additive into one
serving claim (ASSERTED; blog evidence review).

### 3.2 Qualification records (the packaged runtime)

MDB's installed-wheel mechanics and bounded model-backed proofs are recorded in
`saturn-pub/packages/mdb/docs/QUALIFICATION.md` (all MEASURED there):

- Fresh installed runtime wheel: **188 passed, 5 skipped**; clean pinned-dependency run
  **193 passed, 5 skipped**; byte-audit follow-up **199 passed, 5 skipped**; the dependency-free
  wheel's root/session imports and offline CLI work without torch or the scheduler.
- Qwen retained-cut audit: **1,158** committed cuts agree with expected token and logit bytes;
  portable follow-up — seven continuations exact and three stock-native comparisons exact after
  deleting the original source store.
- Mamba corrected memory/recovery: three private siblings, **147 evictions, 245 hydrations**,
  exact private suffixes and a 32-token fresh continuation after source removal.
- FLUX full assay: Klein 4B distilled, BF16/CUDA, 3 prompts x 2 seeds, 512x512, 4 denoise
  steps; six native comparisons exact; **48 evictions, 27 hydrations**; source-deleted fresh
  continuation.
- SDXL full assay: Illustrious XL, FP16/CUDA; six native comparisons exact; **59 evictions, 44
  hydrations**.
- Cross-lane honesty: native vs virtual Qwen has 8, 16 and 32 equal token positions across
  three prompts and **0 of 96** logit digests match across lanes — cuts cannot be exchanged
  across lanes without conversion.
- Paper adapters: E20 reproduces **42** native observable rows and three baseline replays; E6
  interchange has **1,400** exact native comparisons and **40** exact saved-input replays
  (these do not extend the interactive family catalog).

Release validation of the `saturn-pub` package itself is version-specific (MEASURED,
`saturn-pub/docs/validation.md`): v0.1.0 — 35 tests passed on Python 3.10 and 3.12, six example
scripts; v0.2.0 — 79 tests passed, 11 offline example scripts; a FLUX.2 extension — 38 tests; a
writer/notebook extension — 45 tests. On the v0.4.0 checkout the full suite runs **480 passed, 1 skipped** (MEASURED, `pytest -q` in `saturn-pub/`, 2026-10-05, Python 3.12 venv, 33 s); the CI-green claim on Python 3.10 is from the public repository's release notes and is not re-measured here.

### 3.3 The evidence plane and the version-control forest

The evidence plane was run over a lab's full historical record (MEASURED,
`saturn/docs/SATURN-BIBLE.md`): `xref` indexed **218,164** address citations with model
attribution; a bisect-economics case answered **12** real questions in **53** probes versus
**1,010** linear reads; a shakedown over **555** results entries, **134,782** stream records and
**527** receipts confirmed **32/32** findings on independent re-derivation, with **0**
non-finite values in 134,782 records and **0** conflicts across 112/112 cross-arc cells. Of the
hash-pinned reference paths, **97.7%** were dead on the local filesystem while **73.4%** (1,442
of 1,965 refs) remained byte-exact recoverable from the object store — the pointer rotted, not
the bytes.

The **Future Forest flagship must be reported as a reindex, not a live training forest**
(MEASURED, `saturn/results/persistent-future-forest/address-surface-v1/report.json`): its
`claim_status` is `artifact-only-runtime-mechanics-proof-not-model-replication`, with
`model_loads: 0`, `checkpoint_reads: 0`, `optimizer_steps: 0` and `scheduler_submissions: 0`.
It verifies storage and runtime semantics — three fresh artifact-only reopen closures (step256:
249 decisions, 256 observations, 10 content objects, 5,229,251 bytes; step512: 186 / 190 / 7 /
3,268,443; step1000: 125 / 128 / 6 / 2,614,295), all dependency closures verified, with **17**
compiled `Act` leaves independently executable — but it reindexes already-measured evidence and
does not constitute a new model run or a statistical replication. A separate address proof
reports **540 branches, 560 nodes/decisions, 574 observations, 17 executable leaves, 23 objects
/ 11.1 MB** (MEASURED, `saturn/docs/SATURN-BIBLE.md`).

## 4. First users

Five bodies of work already depend on the contract. Each is cited as a demonstration of the
toolkit, with its own headline numbers (all MEASURED in the cited paper's folder).

**Time-Formed Circuits** (`research/papers/time-formed-circuits/paper.md`). Uses capture, fork,
a late key/value band cut, and a band transplant into an unseeded recipient, judged by the
native consumer, across decoder families and a FLUX.2 diffusion transformer. Blocking the
late recipient-formed K/V band removes **73–92%** of an early seed's effect in Qwen2.5-1.5B,
Gemma-2-2B and SmolLM2-1.7B; transplanting the same band restores **71–99%** and authors the
correct answer (wrong-content control authors the wrong answer); the transplant reproduces in
four blind families (OLMo-2-1B, Pythia-1.4B, Phi-2, GPT-2 XL; rescue 0.64–1.62 of the seed
gain). A matched transcoder-feature interchange moves the identity answer at most **0.31** of
the way versus **0.94** for a native K/V cut.

**Single-Site Tests Miss Distributed Stores**
(`research/papers/pointwise-instruments-miss-distributed-circuits/paper.md`). In FLUX.2 Klein
4B, ablating any one of four route components at any one denoising step leaves at least **22%**
of an identity transition intact, while ablating all four at every step leaves **0.13%** and
inserting them carries **91%**. In language models, single-layer K/V replacement removes at most
**16%** (GPT-2 small) and 8–18% (Qwen2.5-1.5B, Gemma-2-2B), while replacement across the second
half of layers removes **81–104%** and flips the top answer on 83–95% of items. TransformerLens
reproduces the implementation on GPT-2 to **1.5x10^-4 nats**; a blind-graded comparison of four
standard readouts against the model's own output gave the wrong verdict in **4 of 4** graded
cases (on cases chosen because failures were expected).

**Score Multi-Turn Interventions Against the Pass-Indexed Native**
(`research/papers/pass-indexed-baseline/paper.md`). Uses native continuation from the same
earlier turns as the correct baseline for a mid-context intervention. On Qwen2.5-1.5B (base),
the later-turn native answer log-probability moves a median of **2.54 nats** versus the
single-turn parent; scoring a late K/V install against the single-turn parent rather than the
pass-indexed native flips the sign and/or the 1-nat conclusion in **11 of 12** cells. The effect
reproduces on instruct weights (2.76 nats, 9/12) and at 7B (1.99 nats, 4/12) in the plain-text
regime and **attenuates to zero** in the chat-template regime (0.002 nats, 0/12), for a reason
the base experiment's own control predicts.

**One Grokked Circuit Is Not a Certificate**
(`research/papers/instrument-audit-interpbench/paper.md`). Scores three in-house instruments
plus standard baselines against the ground-truth circuits of all **86** InterpBench models (84 Tracr-compiled aggregated, two IOI reported separately), with the benchmark's own data generators, seven preregistered predictions and a hash-frozen scorer. Measured no-embedding node-level mean AUROC over the 84 Tracr models: activation patching **0.990**, EAP-IG **0.976**, EAP **0.892** (the published ordering); gradient x activation 0.499 in its calibrated form and 0.842 without the norm division; direct-logit write-site 0.462 baseline-relative and 0.809 as a raw RMS; subspace trace 0.665 against a matched-rank random subspace 0.644; random null 0.493. The method ranking is unchanged between the synthetic and real generators (Spearman 0.98). The headline numbers
are bound to receipt bytes in a `saturn-pub` evidence claim registry
(`research/papers/evidence-registry/`) re-checkable offline with
`saturn-pub evidence claims verify --check`.

**circuit-tracer native-edge arbitration (flagship)**
(corrected run: `research/papers/pointwise-instruments-miss-distributed-circuits/experiments/2026-10-05-attribution-graphs/flagship-summary.json`; the sealed per-prompt bundles are in `saturn-pub/experiments/circuit_tracer/`, whose `docs/circuit-tracer.md` text still describes the withdrawn first run). Takes an attribution graph's edges and lets the unchanged native Gemma-2-2B consumer arbitrate each, through the `saturn_pub.trial` seam. Over a **preregistered** panel (sha256 frozen before the run) of 56 candidate prompts across 7 task families, admission = native fp32 greedy top-1 equals target, `top_k = 20`, thresholds 0.5/0.1 nats: **50 of 56 admitted**, 1000 single-feature edges + 100 group interventions. The native adapter validated first: stepped-vs-native max-abs logit delta **4.5x10^-5**, 16/16 greedy exact, mid-layer cut fresh-process replay exact, streamed == resident bitwise (max logit delta **0.0**), peak VRAM **2.4 GB streamed vs 10.6 GB resident**. Single features: **13 of 1000** individually native-necessary, graph-vs-native agreement **0.846 [0.824, 0.868]**, invert **0.001 [0.000, 0.003]**. Group interventions (50 prompts): steering the top-20 set to −2x activation flips the native top-1 on **45 of 50** (graph agrees large on 47; agreement 0.96 [0.90, 1.00]); joint zero-ablation flips **15 of 50** (agreement 0.56 [0.42, 0.70]). Transcoder error nodes carried **11.4–18.5%** (median 14.0%) of node influence the feature circuit never exposes. A first run of this comparison read the tool's activation array in the wrong order and mis-dosed every native intervention (0 single features necessary, 12 of 50 steer flips, no zero-ablation flips); an independent reimplementation caught it, and the whole panel was rerun under the unchanged preregistration. That episode is itself a measured instance of the verification contract (§6).

ASSERTED: these five share the contract's primitives — capture, fork, declared `Act`,
native-consumer judgment, and hash-pinned offline re-derivation — and none is an external user
(§6).

The corrected flagship numbers above are bound to `flagship-summary.json` in the evidence registry as `mdb-circuit-tracer-flagship-corrected`; the seven Section 3.1 demonstration rows are bound to their report files as `mdb-demo-shared-kv-ancestry`, `mdb-demo-durable-residency`, `mdb-demo-cuda-vmm-aliasing`, `mdb-demo-routed-working-set`, `mdb-demo-archive-read`, `mdb-demo-scene-compiler-rgb` and `mdb-demo-mamba-fork-replay`.

## 5. Comparison with prior art

We claim no primitive as novel; each has a close antecedent, cited with its delta. The table is
an ASSERTED reading of each tool's documented scope, not a benchmark.

| Capability | nnsight / NDIF (2407.14561) | pyvene (2403.07809) | TransformerLens | Patchscopes (2401.06102) | vLLM / SGLang (2309.06180) | Cartridges (2506.06266) | Git-Theta (2306.04529) | **mdb + saturn-pub** |
|---|---|---|---|---|---|---|---|---|
| Intervene + continue natively | yes | yes | yes | yes (own readout) | n/a | n/a | no | yes |
| Cross-process durable forkable session | no | no | no | no | no | partial (reusable state) | n/a (params) | **yes** |
| Byte-exact replay with hash-chained receipt | no | no | no | no | no | no | no (versions params) | **yes** |
| Diffusion support | no | no | no | no | no | no | n/a | **yes** |
| SSM support | partial (model-agnostic hooks) | partial | no | no | no | no | n/a | **yes** |
| Training-interval transactions | no | no | no | no | no | no | partial (version only) | **yes** |
| Offline model-free verification | no | no | no | no | no | no | partial | **yes** |
| Serving-grade throughput | partial (remote exec) | no | no | no | **yes** | partial | no | **no** |

Deltas (ASSERTED, scoped to the cited IDs):

- **nnsight/NDIF (2407.14561)** — gives `intervene`/`continue`, deferred remote execution and
  intervention graphs. Delta: we add a *sealed, resumable* cross-process branch of model state
  and byte-exact receipts; we do not offer their hosted remote-execution service.
- **pyvene (2403.07809)** — a configurable intervention library over many models. Delta: durable
  forks, receipts, diffusion/SSM adapters and transactional training; no claim of broader
  intervention-type coverage than pyvene at a point in time.
- **Patchscopes (2401.06102) / SelfIE (2403.10949)** — the model's own readout as judge of a
  patched state. This is **prior**; our native-consumer judgment is the same idea, packaged with
  forks and receipts. No novelty claimed on native-consumer readout itself.
- **TransformerLens** — the de facto transformer-only hook/patch library; our GPT-2 path
  reproduces it to 1.5x10^-4 nats (§4). Delta: cross-family and durable; no novelty on hooks.
- **vLLM (2309.06180) / SGLang RadixAttention / vAttention (2405.04437)** — production KV serving
  and CUDA-VMM KV management. Delta: we demonstrate a *research* CUDA-VMM aliasing construction
  (§3, row 3) and shared-prefix attention, but make **no serving-throughput claim** and do not
  provide continuous batching.
- **Prompt Cache (2311.04934) / CacheBlend (2405.16444)** — modular KV reuse and the
  concatenation≠prefill problem. Delta: our shared-ancestry and two-source results *measure* that
  mount≠prefill (§6) rather than approximate around it; we do not claim their serving speedups.
- **Cartridges (2506.06266)** — a trained, reusable KV state. Delta: our reusable state is an
  exact captured cut with receipts and a native continuation contract, not a trained artifact;
  Cartridges' training-time compression is prior and distinct.
- **"Models take notes at prefill" (2606.17107)** — KV editing at prefill. Delta: our KV edits
  are declared `Act`s with fail-closed validation and replayable receipts; the editing idea is
  prior.
- **Git-Theta (2306.04529)** — git for model parameters. Delta: the Future Forest versions
  *execution state and decisions* (cuts, observations, promotions), not parameter blobs;
  parameter versioning is Git-Theta's and is prior.
- **Task/function vectors (2310.15916 / 2310.15213)**, **Prompt-to-Prompt (2208.01626)**,
  **DifFRACT (2606.15796)** — specific intervention/edit mechanisms our adapters can host as
  `Act`s; each is prior art for its own mechanism and we claim none of them.

**Honest novelty claim (ASSERTED).** No prior framework spans transformer + SSM + diffusion with
durable cross-process forkable sessions, byte-exact replay with hash-chained receipts,
native-consumer judging, and transactional training control in **one contract**. Every primitive
has a close antecedent above; the combination is the contribution.

## 6. Limitations

Stated in full.

- **No external user yet (ASSERTED).** The five first users in §4 are all the author's own work.
  No independent party has reproduced a result from an exported cut. Adoption is a claim we
  cannot make.
- **The efficiency wins are not equal-semantics (ASSERTED).** The 1.859x routed working-set
  decode (§3, row 4) deliberately changes the rows eligible for attention, so full dense logits
  differ; it is a fixed-prefix experiment, not a production multi-token serving benchmark
  (`saturn/experiments/2026-09-26-primary-routed-working-set/FINDINGS.md`). The CUDA-VMM
  construction (row 3) is bit-identical but "integration into the growing Qwen session manager
  remains open." MDB's diffusion timing (FLUX bench 2.43–5.61 s/image; worker scope 684.49 s;
  `saturn-pub/packages/mdb/docs/QUALIFICATION.md`) is explicitly *not* a speedup or
  bare-pipeline ratio.
- **Mount ≠ prefill (MEASURED).** In the two-source coherence test, pages formed *jointly*
  matched the native first-token top-1 on **6/6** panels; pages formed *independently* and then
  concatenated matched on **1/6** — mounting independently formed K/V is not equivalent to
  prefilling them in context (`saturn/experiments/2026-09-25-book-index-two-source-coherence/FINDINGS.md`;
  report `saturn/results/book-index-two-source-coherence/job-e4471d27ec3c/report.json`). This is
  the concatenation≠prefill problem of Prompt Cache / CacheBlend, measured rather than
  engineered around.
- **The Future Forest flagship is a reindex (MEASURED).** As reported in §3.3, the
  address-surface run loaded no model and read no checkpoint; it proves storage/runtime
  semantics, not a live training forest
  (`saturn/results/persistent-future-forest/address-surface-v1/report.json`).
- **Adapter family coverage is bounded (MEASURED/ASSERTED).** Qualified families are Qwen2/2.5,
  Mamba v1, FLUX and SDXL; Mamba2 and hybrid architectures are unsupported, and native and
  virtual Qwen lanes have separate numerical contracts whose cuts cannot be exchanged without
  conversion (`saturn-pub/packages/mdb/docs/USAGE.md`). Qualification is checkpoint-, backend-
  and numerical-contract-specific and does not generalize to every pipeline or cross-device
  restore (`saturn-pub/packages/mdb/docs/QUALIFICATION.md`).
- **A sibling harness once emitted confident invalid results, and verification caught it.** The
  fine-grained attention-intervention path refuses, fail-closed, the decoder families whose
  attention layout it does not match, "rather than silently mismeasured"
  (`saturn-pub/src/saturn_pub/certificate/panel.py`), and the circuit-tracer integration verifies
  its residual-write address numerically (reported max-abs fp32 difference) rather than assuming
  it (`saturn-pub/docs/circuit-tracer.md`, "The address alignment is measured, not assumed"). The defect itself is on record (MEASURED, `research/papers/time-circuit-scaffold/paper.md`, Limitations, and `saturn/experiments/2026-10-01-qwen-routing-mediation/FINDINGS.md`): an earlier feedback-and-selector instrument installed a custom attention function without its matching causal mask, so a multi-token query chunk could attend to future tokens, and the result passed the instrument's own replay checks. The instrument was retired, the affected routing measurement was re-run on untouched eager execution with zero future attention in every preceding query row, and the guardrails above are the general form of the fix. ASSERTED: a measured alignment check and a fail-closed family gate are what
  separate a usable harness from one that is confidently wrong.
- **In-process `Act`s are not a security sandbox (ASSERTED).** The declared-visibility closure is
  a scientific contract; adapters and callable `Act`s execute trusted Python
  (`saturn-pub/docs/usage.md`).
- **No deployed service (MEASURED).** The in-process debugger protocol is exercised, but deployed
  fleet live-attach and a production broker remain unqualified
  (`saturn-pub/packages/mdb/docs/QUALIFICATION.md`).

## 7. What the paper still needs before a main-track submission

Three demonstrations are named and **not yet done** (ASSERTED):

1. **An outside user reproduces a result from an exported cut.** An independent party installs
   `mdb`, takes an exported `StateCut` + `ReplayBundle`, runs `mdb verify` and a fresh-process
   `resume`, and recovers the sealed continuation — closing the "no external user" gap of §6.
   *Not yet done.*
2. **An equal-semantics cost win.** A measured latency or memory win under *identical* output
   semantics (bit-for-bit logits or RGB), as opposed to the working-set result that changes the
   eligible history. This is the honest serving-adjacent claim the contract does not yet make.
   *Not yet done.*
3. **An end-to-end pipeline no other framework runs.** One experiment that chains the contract
   across families — e.g. a diffusion scene compiled from a sealed source, an SSM state forked
   and replayed, and a transformer K/V band transplanted — all under one receipted, durable
   session, demonstrating a workflow nnsight/pyvene/TransformerLens cannot express. *Not yet
   done.*

## 8. Availability

The public toolkit is `saturn-pub` (import `saturn_pub`), version **0.4.0**, licensed
**Apache-2.0** (MEASURED, `saturn-pub/pyproject.toml`; `saturn-pub/LICENSE`). The repository is
public at github.com/JHollenb/saturn-pub (cite the repository; test count MEASURED in §3.2).

```bash
# saturn-pub (in-process sessions, forks, acts, receipts, evidence, training)
pip install -e '.[ar,diffusion,train,dev]'          # from the saturn-pub checkout
# add .[interop] for SAELens / TransformerLens, .[notebooks] for Jupyter

# mdb-runtime (durable cross-process sessions, memory residency, offline verify)
pip install ./packages/mdb                            # dependency-free core + offline tools
pip install './packages/mdb[autoregressive]'          # caller-owned language models
```

The two packages are independently installable, import neither each other nor private lab code,
and keep separate test suites; CI runs them separately on Python 3.10 and 3.12
(`saturn-pub/docs/monorepo.md`). The dependency-free cores (metadata inspection, byte
verification, the evidence tools) require no model frameworks. MDB's optional scheduler and
diffusion extras pin a public HTTPS Git revision of **mrun-pub** (the lab's auditable model
execution package; github.com/JHollenb/mrun-pub); no private access, workspace or credentials
are required (`saturn-pub/packages/mdb/docs/INSTALL.md`). Model weights and local result
archives are not bundled.

## Changelog

- **2026-10-05 (consistency pass).** The circuit-tracer flagship paragraph now reports the corrected rerun (13/1000 necessary, agreement 0.846, −2x steer 45/50, zero-ablation 15/50) in place of the withdrawn first-run numbers it had copied from `saturn-pub/docs/circuit-tracer.md`, and names the first run as a verification episode; the InterpBench summary in Section 4 now quotes that paper's real-generator primary numbers.
- **2026-10-05 (verification pass).** Test count measured on the v0.4.0 checkout (480 passed, 1 skipped) in place of the unmeasured release figure; the causal-mask defect in Section 6 cited to its record (time-circuit-scaffold Limitations; the 2026-10-01 routing re-run) instead of being called unrecorded; every Section 3 and Section 4 headline spot-checked against its source file.
- **2026-10-05.** First draft.

## References

- nnsight / NDIF — 2407.14561.
- pyvene — 2403.07809.
- Patchscopes — 2401.06102.
- SelfIE — 2403.10949.
- TransformerLens — (software; no arXiv ID cited here).
- MemGPT — 2310.08560.
- vLLM — 2309.06180; SGLang RadixAttention — (software); vAttention — 2405.04437.
- Prompt Cache — 2311.04934; CacheBlend — 2405.16444.
- Cartridges — 2506.06266.
- Models take notes at prefill (KV editing) — 2606.17107.
- Git-Theta — 2306.04529.
- Task vectors — 2310.15916; Function vectors — 2310.15213.
- Prompt-to-Prompt — 2208.01626.
- DifFRACT — 2606.15796.
- First users: `research/papers/time-formed-circuits/paper.md`;
  `research/papers/pointwise-instruments-miss-distributed-circuits/paper.md`;
  `research/papers/pass-indexed-baseline/paper.md`;
  `research/papers/instrument-audit-interpbench/paper.md`;
  circuit-tracer flagship `saturn-pub/docs/circuit-tracer.md`.
