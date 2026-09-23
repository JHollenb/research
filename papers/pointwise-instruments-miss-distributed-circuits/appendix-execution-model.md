---
title: "Appendix: the capture-and-replay execution model"
type: methods-appendix
status: published
date: 2026-09-22
---

# Appendix: how the causal experiments are executed

Every causal result in the main text and its companion paper, except the standalone sparse-autoencoder comparison, comes from one execution
discipline: **capture the unmodified computation once, then fork many
interventions from that captured state, each checked against an exact no-op
before it is scored.** This appendix describes that discipline in plain language,
labels each claim *measured* or *asserted*, and states honestly what the harness
does not do that established interpretability libraries do.

## 1. Capturing a run and replaying it exactly

A generation is treated as a state machine, not one opaque `generate()` call. At a
chosen boundary the harness writes a **captured state**: a content-addressed,
tensor-typed snapshot that holds only the state a resume genuinely needs, plus a
fingerprint (a SHA-256 over each tensor's shape, dtype, and raw bytes). Model
weights and anything recomputable (position IDs, attention masks, RoPE inputs)
are excluded and named by identity instead.

| Setting | What the captured state holds | Boundary |
|---|---|---|
| Diffusion (FLUX.2/FLUX.1) | packed latent state, latent IDs, full timestep schedule, conditioning (text/pooled/reference embeddings), reference-attention KV, guidance, step index; for FLUX.2 also the exact installed sigma schedule + a scheduler-config fingerprint | after any denoising step |
| Language models (dense Qwen2/Qwen3) | token IDs, attention mask, cursor, sampler identity, per-layer key/value cache (one pair per layer), frame lineage; mid-token variant also holds the residual at a layer + staged KV deltas | after any committed token, or after any decoder layer |

RNG is handled by identity: the diffusion path passes the caller's generator
straight through to initial-latent sampling, and the language-model path is
deterministic greedy decoding, so what is bound is the sampler identity, not a
random state. *(asserted, from runtime contracts)*

**Enforcement.** Exactness is not assumed, it is *checked* on every resume. On a
diffusion resume the reinstalled timestep and sigma tensors must equal the stored
ones bit-for-bit (`torch.equal`) or the replay is refused; a config-fingerprint
mismatch fails closed. The scheduler cursor is explicitly reset to the cut index
so late-step coefficients are correct. Across the board, the **exact no-op check**
is the gate: resuming a captured state with *no* intervention must reproduce the
parent exactly — zero pixel difference (mean absolute RGB 0.0) and boundary
activations at cosine 1.0 for images; identical token IDs and `torch.equal`
logits for text; a recorded maximum absolute logit change of 0.0 in the
certificate. Only after a
no-op fork reproduces the parent is any intervention scored. *(measured — see
below)*

**What breaks exactness.** Three things, all documented and guarded:

- **Batch geometry.** A different batched matmul shape is a different numerical
  contract even when the rows are independent; the harness therefore encodes
  prompts one at a time (batched encoding pads the sequence and changes the
  embeddings) and only claims bit-exactness for scalar (row-at-a-time) suffixes.
  A fused batch is labelled `batch-dependent`, never silently called exact.
  *(measured: a four-row batched diffusion call produced small deterministic RGB
  differences even with identical initial latents.)*
- **Precision (bf16).** Any cast breaks bitwise parity, so cached embeddings keep
  their exact dtype (a bf16 embed stays bf16 with no fp32 round trip), and a
  changed dtype cannot inherit an earlier exactness claim. In this paper the
  Qwen3-8B identity cell needed an fp32 rerun to resolve a 0.014-nat difference at
  bf16 resolution (§4.2). *(measured/asserted)*
- **Kernels.** The language worker verifies the *realized* attention kernel is the
  deterministic one (SDPA), not merely that it was requested. A non-deterministic
  scan path is reported as a numerical observation, not hidden behind a boolean.
  *(asserted; one kernel-difference measurement of ≤4.35×10⁻⁴ is recorded
  elsewhere.)*

**Measured evidence.** A diffusion smoke on FLUX.2 Klein-4B recorded 8/8 images
bitwise identical (pixel *and* PNG SHA-256 equal) between two residency schedules
on the same card. The language proof ran an independent Hugging Face forward and
`generate`, ran the same prompt through the harness, and required identical token
IDs and `torch.equal` logits at every generated token; an independent verifier
(not the worker) then re-checked continuation from durable cuts after tokens 1/8/
32, layer replays, and forks — all gates `true`.

## 2. Fork, rewind, and transactional interventions

Because the parent is captured once and is immutable, an intervention is a
**fork**: a child that shares the parent state and runs only the part of the
computation downstream of the cut. Forking is metadata-only; a fork refuses to
start while a step is pending; a **rewind** reverts a child to the parent's exact
state; and running a captured state forward with a null edit is the no-op check
of §1.

An intervention is **declared, not improvised**. It names its `reads` (the
addresses/state it consumes) and its `writes` (the addresses it may change), plus
its dose limit, the downstream output it is scored on, and its replay contract. Writing outside
the declared set fails closed (the runtime diffs actual updates against declared
writes and rejects the excess). Committing versus discarding is explicit: a
**commit** advances the current state to the child; a **discard/abort** leaves the
parent current and marks the child restored; the language-model KV path goes further,
with staged per-layer deltas that only a single commit operation may promote and
an abandon path that proves the parent bytes were left unchanged.

**What this buys, in compute.** Re-running a whole forward pass per intervention
pays for the shared prefix once per intervention; forking pays for it once,
total, and each fork runs only its suffix.

| Arm (FLUX.2 Klein-4B, 512×512, 4 steps, 4 branches, cut after step 2) | Median wall | Denoiser work | Exact? |
|---|---:|---:|---|
| Four complete re-generations | 2.192 s | 16 steps | reference |
| Capture once + exact scalar suffixes | **1.450 s** | 2 shared + 8 suffix | **byte-exact control** |
| Capture once + fused suffix | 1.580 s | 2 shared + 2 batched suffix | batch-dependent |

*(measured.)* The saving grows with branch count and cut depth: denoiser work
fell from 16 steps to 10, and the shared prefix cost zero denoiser calls on
replay. In the language-model path, an eight-token suffix reused a mean **90.12%** of
the prompt's per-layer work *(measured)*. How large the win is depends entirely
on how much shared work each fork reuses: from ~1.5× on this small four-branch
diffusion panel, up to **242×** on a Qwen3-30B eight-branch panel that reuses a
long captured prefix and its expert pages, and ~**4,700×** when a repeated edit
replays a whole captured trajectory instead of recomputing it *(both measured, in
the upper "everything reusable" regime; the receipts explicitly disclaim any
general-throughput reading)*. Two honest caveats: at this small
image size the *physical-call* reduction (4→1) came with a *0.915×* native-forward
wall ratio — forking cuts calls, not necessarily wall time, at small sizes
*(measured)*; and an interactive cross-process replay path that traverses the model twice
measured *0.518×* (0.360× when every state is also written to durable storage), so the win is real only when the
prefix is genuinely reused *(measured)*.

## 3. Relation to existing instruments

The standard libraries do most of what a single forward pass needs, and we do not
claim to replace them.

| Capability | TransformerLens | nnsight | pyvene | This harness |
|---|---|---|---|---|
| Read activations in one pass | `run_with_cache` / `ActivationCache` | trace + `.save()` | collect hooks | yes |
| Write/patch a site in one pass | `run_with_hooks` | set module I/O | interchange intervention | yes |
| KV cache for generation | `HookedTransformerKeyValueCache` | `.generate()` traces | via HF | per-layer KV capture |
| Declared read-set/write-set intervention | manual | manual | **yes** (component/unit/pos) | yes |
| Trainable interventions / gradients | limited | **yes** | **yes** (DAS) | no (the exact path is forward-only) |
| Large model zoo, little porting | **yes** | **yes** (+ remote/NDIF) | **yes** | no (a few pinned models) |
| Diffusion-step / sigma-schedule state as resumable state | no (language models only) | generic module hooks on the denoiser; sampler state not first-class | generic module hooks; sampler state not first-class | **yes** |
| Exact no-op guarantee, measured + gated | do-it-yourself | do-it-yourself | do-it-yourself | **yes** |
| Durable, content-addressed cross-process checkpoint | in-memory only | in-memory only | in-memory only | **yes** |
| Transactional staged KV writes (single commit) | no | no | no | **yes** |
| Capture-once, fork-many suffix reuse | batch patches in one pass; KV-cache reuse by hand | batch patches in one graph | batched interventions | **yes**, with exact no-op per fork |

Read fairly: TransformerLens ports many families behind a clean hook namespace
with cheap read-all-activations and path-patching utilities; nnsight offers a
general deferred-execution graph, gradient interventions, and remote execution of
very large models; pyvene offers serializable intervention schemes and trainable
(DAS) interventions. All three are open and need no scheduler. What the harness
adds is narrow but
load-bearing for this paper: **diffusion-step state** as first-class capturable/
resumable state (TransformerLens does not load FLUX; nnsight and pyvene can hook the denoiser as a generic PyTorch module, but none treats the sampler's timestep and noise-schedule state as capturable, resumable state, which the step-wise FLUX experiments in §4 and [7] require), a **measured and enforced exact-replay
guarantee**, **durable cross-process checkpoints**, **transactional KV writes**,
and **prefix reuse** so a whole-path intervention is not paid for once per site.
Its cost is generality: the exact paths cover a handful of pinned models, require
a job scheduler and content-addressed storage, and do no training in the exact
path.

## 4. Measured efficiency numbers

| Number | Context | Measured / asserted |
|---|---|---|
| **10.66× per image** | diffusion residency schedule vs weight-shuttling offload, Klein-4B, RTX 4080; 8/8 bit-identical | measured (receipt) |
| 6.25×–6.31× end-to-end | same job, whole panel including one encode + one swap | measured (receipt/doc) |
| **1.450 s vs 2.192 s** replay | 4 branches, cut after step 2; 2 shared + 8 suffix steps; control byte-exact | measured (doc + experiment receipt) |
| 90.12% per-layer work reused | 8-token language suffix over an immutable prefix | measured (receipt) |
| 0.518× / 0.360× / 1.004× / 1.054× | language-model suffix replay: interactive two-pass, cold / with durable storage / single-call resident / suffix without copying the branch | measured (receipt) |
| 2.21× | language-model fast path vs the exact reference path; Qwen2.5-0.5B; ≈ parity with native HF (147 vs 146 tok/s) | measured (doc medians) |
| 22.99× (64× lower local-page work) | cached coarse state + 4-page edit wave on a *synthetic* test model, not FLUX | measured, but synthetic |
| **242.1× hot replay on Qwen3-30B** | eight-branch one-token panel: replay a captured 283-token parent (45.8 ms) vs the 11.082 s full-prompt batch control; 8/8 token parity, zero expert bytes moved | measured (receipt) |
| **4,696× edit-cache replay** | FLUX.2 Klein-4B repeated edit: replay a captured trajectory (37 µs median) vs recompute (0.174 s); 4/4 edits exact | measured (receipt) |
| **1.665× / 3.507× on Qwen3-30B, realistic workloads** | four common-prefix branch panels (code completion, document QA, planning, explanation), 320 generated tokens: hot replay 66.530 s vs warm native batching 110.777 s and warm scalar 233.301 s (sums of per-workload values) | measured (receipt) |

The results files behind the numbers in this section and in §2 are in unpublished internal reports\*, except the phase-resident diffusion serving result, which is published with its receipts in [`bfl/demos/exact-phase-resident-serving.md`](../../bfl/demos/exact-phase-resident-serving.md).

\* Unpublished internal documents. Ask the publisher for more information.

The 242.1× figure is the upper regime: a one-token panel where a fork reuses the captured prefix, the expert pages it touched, and the output head; the run's own record states that it is not a claim that arbitrary generation is 242× faster. On realistic multi-token workloads the same mechanism measured 1.665× over warm native batching and 3.507× over scalar execution, which is the number to use for practical estimates.

## 5. Making these paper experiments cheap

Most experiments here reduce to **capture-once, fork-many**:

- **The four-quadrant tests (§2–§4).** The single-site vs whole-path grid is many
  interventions over *one* parent per cell. The paper's own run receipts show the
  intended shape: one model load, all output renders in-process, zero extra
  scheduler submissions, each arm gated by a maximum absolute logit change of 0.0.
The diffusion
  all-step vs single-step sweep is the branch-replay table of §2 applied per
  component and step; the language layer/first-half/second-half/all-layers sweep
  forks the same captured prefill and rewrites different KV subsets.
- **The instrument comparison (§5).** The single-step patching arm (case 1) is
  the same capture-once/fork-many sweep; the probe, direction-transfer, and
  reconstruction arms (cases 2–4) read from *cached* captured states rather than
  re-generating, so the "standard readout" and the "downstream model" arms share
  one forward and differ only in what they read or write. The sparse-autoencoder comparison (§4.4) does not use this harness at all: it is a standalone script built on Hugging Face Transformers, SAELens and TransformerLens, so that anyone can rerun it.
- **The FLUX held-out panel.** Held-out seeds re-run the *frozen* configuration
  (byte-identical except the seed), and each six-axis group loads the model once
  and executes its 252 branches from shared per-group captures — dose curves,
  wrong-axis and energy shams, per-site and full-route ablations, and mediation
  edges are all forks of the same parents, not independent generations.

The general rule: anything that varies only *what is read or written* downstream
of a fixed point should fork a captured state, and anything that must be exact
should carry the no-op check as an acceptance gate.
