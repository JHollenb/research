---
title: "A New Class of Circuits: Space and Time"
subtitle: "Localized circuits, time-accumulated circuits, and why standard instruments see only the first kind"
type: research-paper
status: outline-draft
date: 2026-09-30
author: Jacob Hollenbeck
supersedes_for_external_release:
  - ../integral-residual-dynamics/paper.md
  - ../capabilities-as-transactions/paper.md
builds_on:
  - ../../bfl/docs/certified-semantic-circuits/paper.md
  - ../pointwise-instruments-miss-distributed-circuits/paper.md
tags: [interpretability, circuits, diffusion, language-models, causal-mediation, time-accumulation]
---

# A New Class of Circuits: Space and Time

> **How to use this outline.** Every section lists its claim, the evidence that already exists (with receipt paths), and what is still owed. Three markers:
> - **TODO [E#]** is an experiment to run. The full list with cost estimates is in Appendix A.
> - **TODO [R#]** is a result to collate, verify, or correct from existing receipts, with no new compute. The list is in Appendix B.
> - **TODO [W]** is writing only.
>
> "Public" means the receipt is bundled with a verifier under `research/`. "Private" means it exists only under `saturn/results` or `saturn/experiments`.
>
> Excluded by the author's direction: results produced on 2026-09-30 by `saturn/experiments/2026-09-30-blind-final-boss-certification/`, the 2026-09-30 grail/G2 runs (`saturn/experiments/2026-09-30-grail-*`), and the 2026-09-30 holy-grail audit. Where those runs touched a claim, the claim is marked TODO for re-measurement.
>
> This paper consolidates four documents into one story:
> 1. the certified FLUX.2 route paper (`research/bfl/docs/certified-semantic-circuits/paper.md`);
> 2. the measurement paper (`research/papers/pointwise-instruments-miss-distributed-circuits/paper.md`);
> 3. the IRD theory draft (`research/papers/integral-residual-dynamics/paper.md`);
> 4. the final-boss / transaction draft (`research/papers/capabilities-as-transactions/paper.md`).
>
> Assessment and census notes: `research/papers/capabilities-as-transactions/assessment-notes.md`.

---

## Abstract (draft)

> **TODO [W]:** finalize the numbers after Appendix A.

Interpretability's circuits are **space circuits**: small sets of components (heads, features, edges) that a single-site intervention can find, because removing one hurts and inserting one helps. We report a second class, **time circuits**. A time circuit is built up across the model's accumulation axis: denoising steps in a diffusion transformer, or layers along a token's key/value trace in a language model. Every member of a time circuit is individually unnecessary and individually insufficient, while the whole path is both necessary and sufficient.

A four-quadrant certificate separates the two classes. Single-site ablation and writing both fail, while whole-path ablation removes the behavior and whole-path writing installs it, all judged by the model's own unchanged output machinery. Exact replay is a hard gate. Neither a localized circuit nor a diffuse linear representation produces this pattern.

**In FLUX.2 Klein 4B.** One route, `joint.2 → joint.3 → joint.4 → single.0`, carries all twenty semantic contrasts we tested:
- six pass all nine preregistered gates, eleven more pass every gate except strict pixel reconstruction, and three remain candidates;
- the route gates replicated on unopened seeds and on new prompts;
- single-step patching reports the route as absent;
- the route is coordinate-free, can be rediscovered without prompts, and is separable from its text encoder.

**In language models.** The same four-quadrant signature appears in SmolLM2-1.7B, Qwen2.5-0.5B, Qwen3-8B and Qwen3-30B-A3B. It is absent at a 6-layer, 70M-parameter model, appears by about 400M, and arrives with capability during training. The certificate is a property of a *transport cut*: two transformers lose their own certificates when only the cut moves from key/value to hidden state.

**Static and dynamic parts.** A time circuit decomposes into static infrastructure (route order, writer roles, the native consumer, prompt-time keys and values) and per-prompt dynamic circuits (payload, address, dose, timing). This decomposition explains a family of image-editing results:
- edits must be installed early;
- *when* a write lands selects *which* semantic changes;
- moving an object is a space × time conjunction;
- a prompt compiles to an installable source that reproduces native images exactly.

**Instruments.** Standard instruments see only space circuits. In a blind-graded trial, four standard readouts gave the wrong verdict in 4 of 4 cases. A preregistered sparse-autoencoder workflow on public SAEs finds the store only when its ablation spans layers.

## 1. Introduction

**Claim.** There are two classes of circuit. The field's instruments are built for the first. The second class is common in models above roughly 1B parameters and in every iterative generator we checked, and it is the class that commits the output.

**Paragraph plan:**
1. **The standard picture.** A circuit is a localized subgraph. Single-site patching, path patching, ACDC, SAEs and attribution graphs all ask "which site matters?" (Meng 2022; Wang 2022; Conmy 2023; Ameisen 2025).
2. **The anomaly.** In FLUX.2, single-step patching at every site of a route returns "no necessary component", and the same sites patched across all steps remove and install the behavior.
   - Single-step transplant leaves pixel distance 48.4 to target; all-step leaves 0.47.
   - Single ablation leaves the target intact (7.9); all-step full-route ablation reaches −0.93.
   - Source: `certified-semantic-circuits/paper.md` §5.
3. **The name.** We call these *time circuits*. Our working name was the "final boss": the conjecture that every model funnels its output through a late, path-constituted store that smaller circuits write into. Origin post: `obsidian/blog/2026-08-21-114500-the-final-boss-circuit.md`.
4. **What is new:**
   - the certificate;
   - the cross-modal evidence;
   - the cut result;
   - the static/dynamic decomposition;
   - the demonstration that standard tools miss the class.
5. **Contributions (numbered list):**
   - (C1) the definition and four-quadrant certificate;
   - (C2) the FLUX.2 route;
   - (C3) language-model certificates and the scale floor;
   - (C4) the cut result;
   - (C5) static infrastructure vs dynamic circuits;
   - (C6) instrument failure, measured;
   - (C7) applications as consequences.
6. **Boundaries up front:** the circuits are certified per model; the autoregressive and diffusion instances share a *certificate shape*, not a physical circuit; n ≤ 4 per language-model cell.

**TODO [W]:** cite the Anthropic Circuit Tracing limitations (frozen attention; cross-position flow "but not why") and their QK follow-up (transformer-circuits.pub/2025/attention-qk). Position time circuits as a class that frozen-attention, single-pass replacement models are not designed to expose. Do not claim to solve "why attention attended".

## 2. Definitions

### 2.1 Space circuit
A set of components S such that single-site interventions on members of S have measurable necessity or sufficiency, judged by the native output.

Canonical examples:
- induction heads;
- the IOI circuit;
- our certified Pythia-70M induction writer (§7.1).

### 2.2 Time circuit
A set of sites P along an accumulation axis t, where t is denoising steps or layers of a token's K/V trace, such that:
- (i) single-site necessity fails;
- (ii) single-site sufficiency fails;
- (iii) whole-path necessity passes;
- (iv) whole-path sufficiency passes.

All four are judged by the unchanged native consumer.

Formal object, from the IRD draft §2:
- split the state into scaffold and residual, x(t) = s(t) + r(t);
- the consumer reads a functional of the residual trajectory, R = 𝓘(r(t)), rather than r(t\*) at any single site.

**TODO [W]:** port IRD §2–3 in compressed form. Keep the "wiring fact is not the claim" paragraph.

### 2.3 The four-quadrant certificate

|  | single site | whole path |
|---|---|---|
| necessity (ablate) | behavior survives | behavior dies |
| sufficiency (write) | nothing happens | full authorship |

**Validity gates:**
- exact no-op: a zero-magnitude write reproduces the output bit-for-bit;
- exact uninstall;
- clean capability with generic-floor separation (IRD C2–C3).

**Reading rules** (IRD §3):
1. The cut matters.
2. Isolated, not in-forward, key/value swaps. On Qwen2.5-1.5B the in-forward swap gives 0.99 and the isolated swap 0.00 (`pointwise…/paper.md` §4.3).
3. Whole-path ablation is close to deleting the token, so the informative part is the single-site failure.

### 2.4 Static infrastructure and dynamic circuits
- **Static:** route order, writer roles, state boundaries, the native consumer, and prompt-time K/V.
- **Dynamic:** source rows and coordinates, payload, signed coefficients, dose, spatial support, timing, and the live query.

Origin: `obsidian/blog/2026-08-26-151627-the-hypergraph-had-a-skeleton.md:64-74` (G_physical vs G_execution vs G_output).

Reified in code:
- `saturn/src/saturn/execution_skeleton.py:790` (`ExecutionSkeleton`: descriptive, no execution authority);
- `saturn/src/saturn/dynamic_circuit.py:703` (`DynamicCircuitRecord`: evidence-only, pinned to a skeleton fingerprint).

Proposal: `obsidian/2026-08-29-003349-skeleton-ir-incremental-executor-proposal.md`.

### 2.5 Relation between the two classes
A time circuit is the *sink* that space circuits write into (`obsidian/blog/2026-08-21-114500-the-final-boss-circuit.md`, "sink corollary"). Below the scale floor the sink collapses into a space circuit (§6.4).

## 3. Method: exact replay with the native consumer as judge

**Claim.** Time circuits are only checkable with an instrument that can do three things:
- capture a computation once;
- fork it many times with one value replaced at every step;
- replay the rest exactly.

**Content, with sources:**
- **Saturn execution model.** Frame, Act, StateCut, fork/replay, and the exact no-op gate. See `research/papers/pointwise-instruments-miss-distributed-circuits/appendix-execution-model.md`, which measures the no-op: diffusion resume mean RGB difference 0.0, FLUX 8/8 bitwise across residency schedules. Background:
  - `saturn/docs/SATURN-BIBLE.md`, `SATURN-DEBUGGER.md`, `ROLE-PORTABILITY-ABI.md`, `DIFFUSION-TRANSACTION-ABI.md`;
  - origin story: `obsidian/blog/2026-09-04-151836-from-final-boss-to-saturn-vm.md` and `2026-08-31-110633-from-the-final-boss-to-a-debuggable-circuit-runtime.md`.
- **The nine-gate certificate** (FLUX). Gates: replication, sufficiency P ≥ 0.90, necessity ≤ 0.15, wrong-axis ≤ 0.35, energy sham ≤ 0.35, dose, edge mediation ≥ 50%, continuation ≥ 0.75 / alignment ≥ 0.80, and replay integrity. Source: `certified-semantic-circuits/paper.md:81`.
- **The four-quadrant certificate** (language models), defined in IRD C1–C8: `saturn/docs/IRD-CERTIFICATES.md`.
- **Precursor instrument: Thott,** which reads the K/V cache as clock × address × residual:
  - de-rotating RoPE raises within-token phase coherence from 0.51 to 0.87;
  - a codebook-only replacement is refuted (0.03–0.08);
  - the depth-growing residual of about 19–22% is load-bearing.
  - Sources: `obsidian/blog/2026-08-13-thott-from-cache-diff-to-circuit-thought.md`, `2026-08-13-the-cache-was-a-file-format.md`; job `job-080c3550be62` (private).
  - Role: motivates the language-model cut. A precursor, not evidence.
- **Evidence ladder:** observation → trend → convergent trend → working inference → terminal claim. A failed gate means "not established", never "absent".
- **Cost:** capture once, fork many. One model load runs 40 logical branches in 8 physical calls (hotpatch-cinema). Cheap-deep resume is 7.993× at k = 7 with exact parity (`research/bfl/demos/diffusion-time-causal-clock.md`).

**TODO [W]:** a one-paragraph comparison with TransformerLens, nnsight and pyvene, adapted from `appendix-execution-model.md`.

## 4. How the time circuit was found

**Claim.** It was invisible to the standard instruments. Contrasting two conditioners driving the same frozen image program exposed it.

**Narrative, in date order.** Source for this section: `obsidian/blog/2026-08-28-221644-the-week-in-review-from-the-final-boss-to-a-transaction-abi.md`, plus the primary posts listed in Appendix C.

1. **The conditioner swap (Aug 5–11).**
   - SmolLM2-1.7B and Mamba-1.4B, through a trained adapter, drive the frozen FLUX.2 body to clean but wrong images.
   - Contrasting them with native Qwen located where semantics diverge downstream:
     - route flow is 0.9312 native vs 0.5300 SmolLM2;
     - full-state rescue is 0.751 / 0.817, while compact selectors reach ≤ 0.051;
     - the foreign color separation at the route's entry is damped about 43×.
   - Sources: `research/bfl/demos/cross-compiled-conditioner.md`, `cross-family-conditioner-repair.md`; `certified-semantic-circuits/paper.md` §7.
2. **Promptless rediscovery.** Random 5%-norm perturbations of an empty prompt recover 3 of 4 route sites and the `joint.4 → single.0` edge.
   - Clamp mediation removes 83–95%; downstream donation reconstructs 95–100%.
   - Off-route sham ≤ 0.0951 vs route effects up to 0.697.
   - Source: `certified-semantic-circuits/paper.md` §8.3 (public).
3. **The misreading we made first.** The first single-step panel was summarized as "distributed relay with no necessary node" (`certified-semantic-circuits/paper.md` §5). That is the instrument failure this paper is about.
4. **The folklore number.** A "0.2218 / 0.0013" pair circulated but was not in the record. It was caught by the program's own audit and replaced with receipt-backed values (IRD §1). Keep this as a methods vignette.
5. **The instrument trial (Aug 20),** blind-graded. Covered in §9.
6. **The language-model sink (Aug 21),** covered in §6.

**TODO [R1]:** a figure (timeline strip) showing the Aug 5 → Sep 22 sequence. Build it from the week-in-review post and Appendix C.

## 5. Time circuits in diffusion

### 5.1 One route carries every axis (FLUX.2 Klein 4B)

**Evidence (public):**
- **Panel.** Twenty contrasts across twelve categories: 6 strict 9/9, 11 carrier 7/9, 3 candidates.
  - Top strict rows: lighting .935, identity .920, weather .911, fur .894, orientation .873, relation .866.
  - Sources: `research/bfl/demos/twenty-axis-semantic-route-circuit.md`; `research/bfl/artifacts/twenty-axis-semantic-route-circuit/`.
- **Held-out seeds.** Route gates replicated across the panel; the only route failure missed by 0.002 (0.1522 vs 0.15). The strict tier was seed-sensitive (5/14/1).
- **Held-out prompts.** 4/6 strict and 6/6 route, exactly at the preregistered bar. Source: `certified-semantic-circuits/experiments/2026-09-22-prompt-heldout/`.
- **Clean-room audit.** 0 decision mismatches; 5/5 tamper injections caught.

**Correction to carry:** `ears_upright_folded` controls eyelid state, not ears (`certified-semantic-circuits/corrections/ears-upright-folded-eye-control.md`).

### 5.2 Built over time: single-step patching cannot see it

**Evidence:**
- Return-state separation grows 0.355 → 0.919 → 2.487 → 9.723 (identity) and 0.411 → 0.837 → 1.990 → 7.409 (color). Figure: `certified-semantic-circuits/figures/fig2-separation-curves.png`.
- All-step edge-mediation rescues: .946, .888, .796.
- Distributed K/V color-binding route (20 sites):
  - native margins +6.740 forward / +8.830 reverse;
  - recoveries 83/96 and 88/96;
  - the compact {8,11} subset fails, and all-step beats every single step;
  - caveat: 45/96 reverse donor-color collisions;
  - source: `research/bfl/demos/distributed-kv-causal-route.md` (public).
- Causal clock: same dose, k = 1 effect 0.360 / amplification 2.399 vs k = 7 0.078 / 0.523, crossover near k = 4. Source: `research/bfl/demos/diffusion-time-causal-clock.md` (public).
- Consumption kernel (corrected 2026-09-22): front-loaded weights ≈ [0.21, 0.22, 0.08, 0.04].
  - It measures pixel reproduction, not when identity is decided.
  - Late double dose at equal nominal integral: 0.055–0.288, vs all-step 0.522–0.810.
  - Source: IRD §8; `pointwise…/paper.md` §4.6.

**TODO [E7]:** multi-seed necessity for the color contrast, currently single-seed (`certified-semantic-circuits/paper.md:246`).

### 5.3 Coordinate-free
- Per-module trajectories: minimum pairwise cosine 0.986. Physical support: mean Jaccard 0.063.
- Token-position shift (horse / fox / rabbit): 0.9879 / 0.9876 / 0.9873.
- Excluding the `joint.4` text site drops transfer to 0.59 / 0.49.
- Source: `certified-semantic-circuits/paper.md` §6.

### 5.4 Is it just the text-to-image bridge? (alternative-path controls)

**Reviewer objection.** In FLUX, text crosses into the image stream in the joint blocks and merges at `single.0`, so any such bridge would carry every axis.

**Existing answers:**
- **Gates.** The wrong-axis (≤ 0.35) and energy-matched sham (≤ 0.35) gates pass on every certified row.
- **Promptless controls.** Off-route sham ≤ 0.0951; the last merged block's text positions show exactly 0.0.
- **Leave-one-out.** Removing the `joint.4` text site drops transfer to 0.59 / 0.49.
- **Local vs whole-state.** Single-token QKV routes score 0.001–0.227, while whole text-state transfer closes every joint edge (weakest 0.911). Source: `research/bfl/demos/route-cartographer-consumer-closure.md:41-43`.
- **All-joint ceiling, FLUX.1-schnell only.** The route carries 0.6915 = 98% of the all-joint 0.7069 ceiling, all 57 text sites reach 0.7292, and single blocks alone are near-inert. Source: `research/bfl/demos/semantic-circuit-object-part-III.md:100`.
- **Operating-point dependence.** At base-4B with 50-step CFG, early joint bands approach the full effect (redundancy). Source: `semantic-circuit-object-part-III.md:76`.

**TODO [E1]:** an off-route span sweep at the *certified* Klein-4B / 4-step / 256² operating point. Arms:
- `joint.0–1` only;
- `joint.2–4` without `single.0`;
- image stream only;
- all-joint ceiling;
- `single.1–19` spans.

Same axes, seeds and gates. This closes the objection where the claim is made.

### 5.5 The family: FLUX checkpoints and conditioners (Part III)
- **FLUX.2 base-4B** (undistilled, 50-step CFG): white fox .888, green ball .784 / .836, sham ≤ .13 (`job-17788d5a1b0d`).
- **Klein 9B:** subject write .743 vs sham .043, port .471 vs .076, one seed (`job-638d05dcbff2`, `job-3e1bc534e0eb`).
- **FLUX.1-schnell** (T5 + CLIP): same object at noun-phrase-window grain. A single row is sham-level (−.05 / .03), while the ±3 window reaches .56 / .63.

Sources: `research/bfl/demos/semantic-circuit-object-part-III.md` (public); cohort revisions in `research/bfl/README.md`.

**Status.** Register-level replication is at trend level. These are *not* nine-gate certificates on those checkpoints.

**TODO [E8] (optional):** a nine-gate certificate on Klein 9B, two seeds, at least one axis.

### 5.6 Beyond FLUX: other diffusion families
- **SDXL UNet** (WAI / Illustrious v150):
  - a rank-1 writer clock explains 0.662 of temporal energy and is causally sufficient (α 0.635 vs 0.671 independent) (`job-3d43b5402436`);
  - the time-formed schedule transfers to unseen seeds and objects at cosine 0.98–0.9997 (`job-b51e75ec32be`);
  - main stream writes early, skip writes late; object identity is a middle × late conjunction (`job-310d96377d34`, `job-19ae75968d58`);
  - reversing only the schedule melts geometry (`job-00c5ec5ca23f`).
  - All private; folder pattern `saturn/experiments/2026-08-3*-sdxl-*rosetta/`.
- **SDXL scene compiler.** Static K/V + dynamic Q → dynamic P:
  - K/V are byte-identical across calls 0 ↔ 14, while Q cosine drifts 0.9999 → 0.8399;
  - matched K + V under live Q gives α 1.0000, RGB MAE 0.0;
  - source: `job-51aac02d9df3`; `obsidian/blog/2026-09-01-231018-we-found-the-native-scene-compiler.md`.
- **Chroma DiT, 28 steps.** Step-0 state is reusable; steps 1–27 are invalidated by the trajectory (`job-3d34f8ee687c`).

**TODO [R2]:** confirm that the SDXL "writer clock" results are *not* covered by the retracted rank-16 clock controller (`job-dfcb4146232b`, `job-8a18f3102d6f`; `obsidian/blog/2026-08-31-143646-rank-16-was-a-basin-not-a-clock.md`). Record the verdict in this section.

**TODO [E9] (optional):** a four-quadrant certificate on one SDXL route, to lift §5.6 from trend to certificate.

## 6. Time circuits in language models

### 6.1 The sink certificate

**SmolLM2-1.7B identity** (`job-6650205b45eb`, public in `pointwise…/evidence/four-quadrant-tests/`):

| ablation arm | Δlp(fox) | set top-1 |
|---|---:|---|
| L12 | +0.031 | fox |
| L18 | +0.403 | fox |
| first half | +0.357 | fox |
| second half | −2.088 | wolf |
| all layers | −2.093 | wolf |

Single layers carry 1.5% and 19.3% of the whole-path effect.

**Sufficiency (P4, cross-slot).**

| write | score |
|---|---|
| Hidden-slot write | 0.90–1.02 |
| Full K/V trace | 1.058–1.093 |
| Single K/V slice | 0.010–0.107 |
| Shams | ≤ 0.047 |

Job `job-0a07cb92d360` was killed by a VRAM leak, so the numbers come from the log receipt. Disclose this.

**Grid** (`job-72f0e98679d5`): Qwen2.5-0.5B identity and color, SmolLM2 color and verb.

**Qwen3-8B:** fp32 dual-backend recheck gap 0.267, parity 0.0001 nat (`job-6299f2391d5c`, public). Instrument story: the floor confound and the bf16 last-unit artifact.

**Qwen3-30B-A3B identity:**
- pc 22.6, single ≤ 2.9%, W2_all 1.0376, gap 0.062 nat to floor;
- caveat: the generic floor still answers "fox";
- arithmetic is issued-qualified;
- jobs `job-7cc5b24954f0`, `job-ef8408d9c3d2` (private).

Certificate registry: `saturn/docs/IRD-CERTIFICATES.md:126-141`.

**Corrections and owed work:**
- **TODO [R3]:** fix the receipt mis-citations inherited from the IRD draft:
  - the diffusion row cites `job-6650205b45eb`, but the numbers are in `pointwise…/evidence/instrument-trial/bundle/case-1/circuit-panel-ledger.json` (`job-7d53e47755f7`);
  - the 30B row cites `job-38c1c37dd591` (a SmolLM smoke job).
- **TODO [E3]:** isolated-swap reruns for SmolLM2-1.7B identity (flagged "not rerun", `pointwise…/paper.md:90`) and Qwen3-8B.
- **TODO [E3]:** public redacted bundles with `verify.py` for the 8B and 30B certificates.

### 6.2 Computed objects and free generation
- **Computed object.** "The sum of three and five equals" → " eight".
  - Carrier ablation −5.41 nats onto the floor; single layers ≤ 1.5%.
  - The "two and seven" trace authors " nine" at 0.979.
  - Job `job-3b014f386fb8` (private).
- **Free generation.** Single layers are inert in every cell (≤ 0.04), while set cuts flip the continuation from step 0. Sources: `saturn/experiments/2026-08-21-multitoken-transport/`, `saturn/results/ird-multitoken/` (private).

### 6.3 The certificate is about a cut, not an architecture
- Mamba-2.8B does not certify at the hidden-state cut: single layers are 110% / 65% of all-layer.
- SmolLM2 and Qwen2.5 *lose their own certificates* at the same cut: single-site necessity goes from 1.0–1.5% to 172–236%.
- Jobs `job-13a15543fbb1`, `job-8e2d02c4a51e`, `job-0622676c3473`, `job-f11cab813f66` (private). Narrative in IRD §7.

**TODO [E5]:** the SSM recurrent-state cut was built and queued (`job-beb10c04a81d`, `job-a97cb1825d39`, Addendum AC in `saturn/experiments/2026-08-21-wall-a-addressing/README.md`). Find the result; if it is missing, rerun. Either outcome is reportable: a pass extends the class to SSMs, and a fail scopes it to attention transports.

### 6.4 Scale floor and developmental onset
- **Pythia-70M** (6 layers): capable checkpoints carry 79–81% of whole-path necessity in one layer. It is a space circuit, not a time circuit.
- **Pythia-410M** (24 layers): the certificate appears with capability and sharpens afterward (W2_single 0.257 → −0.025).
- **GPT-2 124M:** concentrated; 20 SAE features at one layer remove the whole effect (`pointwise…/paper.md` §4.4, public).
- Jobs: `job-073398d3ef7b` (private); `saturn/experiments/2026-08-21-ird-verification-battery/README.md:320-338`.

**TODO [R4]:** fix the wording. "Arrives with capability" is too broad: 410M single-site constructive is 0.2573 at step 4000, above the 0.2 bar, and passes both strict bars only at step 16000.

### 6.5 Joint key/value transport across positions
- **Coder-7B natural task-state chain:**
  - joint K/V install 4/4; K-only 0/4; V-only 0/4; wrong-layer 0/4;
  - lesion 0/4; neighbor repair 4/4;
  - n = 4; the receipt states "terminal claim: false";
  - job `job-a12ed4b56846` (private); `saturn/experiments/2026-08-25-natural-task-state-kv-causal-chain/RESULTS.md`.
- **Coder-1.5B reciprocal in-flight swap.** Layers 13–27 give the exact 122-token passing future in the failing process, and vice versa. K-only and V-only fail. n = 1 task (`job-86b12ab70e83`).
- **Framing.** The row-permutation tolerance is the expected attention identity softmax(Q(PK)ᵀ)PV = softmax(QKᵀ)V. Report it as an instrument check, not a finding.
- **Prior art to cite:** in-context task vectors (Hendel 2023) and function vectors (Todd 2024). State what joint-K/V carriage adds.

### 6.6 Chain-of-thought scratchpad state (limited)
Scratchpad-token K/V swaps flip the answer in four families:
- SmolLM 8.02 vs carriers 1.82;
- Qwen-0.5B 9.23 vs 0.88;
- Qwen3-8B 14.18 vs 0.53;
- Qwen3-30B 11.59 vs 1.64.

Source: `saturn/experiments/2026-08-21-ird-fruit-battery/README.md` (private).

**Limit:** one prompt pair per family, and the swapped token is the stated answer, so this measures copying.

**TODO [E10] (optional):** an intermediate-step swap, at least 20 items, against truncation and mistake-insertion baselines (Lanham 2023). Alternatively, drop this subsection.

## 7. Space circuits, for contrast

### 7.1 Certified space circuits (public)
- **Pythia-70M step 1000 induction writer** {L3H1, L3H6}:
  - clean 89.4%, source cut 1.9% (chance 2.1%);
  - head 1 alone 75.0%, head 6 alone 32.5%;
  - matched-cue cut 92.8%; correct repair 93.8%; wrong repair 2.8%;
  - the step-512 null is inert.
  - Verifier: `research/bfl/docs/certified-semantic-circuits/verifier/verify_pythia_induction.py` (57 s on CPU).
- **Qwen2.5-0.5B / Qwen3-0.6B-Base source routing:**
  - 28/28 gates;
  - source cut 0–1%; matched-cue > 91%; wrong-donor ≤ 0.52%; exact repair;
  - job `job-ec1ab31d35f2`; `obsidian/blog/2026-08-11-the-autoregressive-source-circuit-closed.md`;
  - caveat: it is the complete parent (336 / 448 edges), with no compact envelope.
- **Pythia date-retrieval birth.** Source, write, carrier and consumer arrive between steps 512 and 1000; L3 deletion share is 92% at step 1000, falling to 76% at step 4000; at 410M the source moves to L11. Sources: `saturn/experiments/2026-08-14-natural-date-formation-microscope`; `obsidian/blog/2026-08-14-we-watched-a-capability-being-born.md`.

### 7.2 Same model, both classes (key figure)
- **Qwen2.5-0.5B** has a certified space circuit (induction source routing, `job-ec1ab31d35f2`) and a certified time circuit (identity sink, `job-72f0e98679d5`).
  - **TODO [R5]:** build the side-by-side four-quadrant table from these two receipts. No new compute if both receipts carry single-site and whole-path numbers; otherwise this becomes E6.
- **Pythia-70M.** The writer pair is a space circuit, but the whole-model account needs the upstream layer-2 relay.
  - **TODO [E4]:** re-measure recovered-loss R for {L3H1, L3H6} and for the 5-head set {L2H1, L2H7, L3H0, L3H1, L3H6}, under mean *and* resample ablation, with size-matched random sets. The 2026-09-30 numbers are excluded.
- **Same model, different cut.** Covered in §6.3.

**TODO [W]:** Figure: four-quadrant bars for one space circuit and one time circuit in the same model.

## 8. Static infrastructure and dynamic circuits

**Claim.** The time circuit is the static chassis. Each edit, register, attribute or scene is a dynamic circuit loaded onto it.

**Evidence:**
- **Skeleton holds, coordinates move** (Aug 26).
  - Same-ontology causal-profile cosine 0.9132 vs cross-ontology 0.7344; rank-one shared energy 0.7990.
  - The late `single.0:image` seam appears in 8/9 families.
  - Whole-state rescue at joint.2/3/4 gives 0.9440 mean RGB vs sham −0.1722 (`job-ce8c48e505c8`, `job-e70b2bff82cc`).
  - Held-seed: whole-register write at the t2 commitment phase gives 0.918 RGB (`job-bd7cc3ef0f2d`).
  - Sources: `obsidian/blog/2026-08-26-142017-the-route-holds-the-coordinates-move.md`, `2026-08-26-184423-the-skeleton-survived-its-coordinates-did-not.md`.
- **Seed stability.** Route Spearman 0.9516–0.9751 across seeds, while payload cosine is 0.32–0.86 (skeleton-IR proposal `:91`).
- **Four-factor cube** (Aug 28).
  - Möbius reconstruction error 0.0.
  - Mediator image-only restore 83.07%; text-only −1.84%; both streams pixel-exact.
  - Higher-order body term: L2 1.232, cosine 0.206.
  - Jobs `job-8d9a230b083d`, `job-f68e1365baae`, `job-755b73fca4f7`.
  - Sources: `obsidian/blog/2026-08-28-105410-the-model-was-a-runtime-not-a-dictionary.md`, `2026-08-28-141114-the-control-map-and-the-circuits-we-have.md`.
- **Two-parent closure.** Neither 0.000; register-t2 0.403; program-t3 0.712; both 1.000, pixel-exact.
- **Static K/V, dynamic Q** (SDXL, §5.6). This is the mechanistic form of the split.
- **Substrate separation.** Full native conditioning gives a 100% byte-identical recovery; the best partial reaches 7.6%, and half reaches 23–31% (`certified-semantic-circuits/paper.md` §7).

**Dynamic circuits that load onto the route, one line each:**

| Dynamic circuit | Result | Source |
|---|---|---|
| Eye color | Upstream program about 0.887 targetward | `obsidian/blog/2026-08-28-141114-…:294` |
| Eye geometry | 0.931; shares 5–7/8 consumer heads with color, but K/V source rows overlap only 10–15/64 | same |
| Eye color × geometry | Nonadditive residual needed for exact closure | `…105410…:234-238` |
| Object registers (fox / ball / mug) | Selectivity 13.7× / 9.6×; wrong-address inert; value algebra gives a blue mug (MAD 59.8 vs cat 1.9) | `research/bfl/demos/semantic-circuit-object-part-I.md`, `-II.md` |
| Character register (Jen) | Reference-slot bus [1024, 2048); byte-exact native equivalence 2/2; delete → restore exact; 0 training | `research/demos/jen-character-register.md` (untracked) |
| Sprite register (negative) | Reference-slot swap does not move screen position | `research/demos/jen-sprite-register.md` |

**Spectral address as the binding layer:**
- FLUX.2 contact side is selected 6/6 by native mean plus target contrast, with source states at `joint.3` across all four steps (`job-6386d22db7c1`).
- The old writer's target switch is byte-identical 12/12 (`job-47589b8693dc`).
- Sources: `saturn/experiments/2026-09-18-flux2-spectral-instance-binding/README.md`; ABI `saturn/docs/SPECTRAL-ADDRESS-ABI.md`.
- Do not cite the unrelated SPF numeric-format work.

**TODO [W]:** a figure of the static skeleton with dynamic circuits as overlays, for eyes, register, scene and move.

**TODO [E2]:** the completeness falsifier, incremental vs full replay (`saturn/src/saturn/circuit_incremental.py`), is specified but unbuilt. Optional: run it on the 206-cell / 305-edge FLUX time × depth skeleton (`saturn/docs/GENERALIZED-CIRCUIT-ATLAS-ROUTER.md`) to give one completeness number for the static skeleton.

## 9. Why standard instruments miss time circuits

**Claim.** The class is invisible by construction to single-site and single-layer instruments. We measured that directly.

**Instrument Trial (Aug 20), blind-graded:**
- In 4 of 4 main cases the standard readout misreported, while the exact-replay verdict matched.
- The reserve case also misreported; the honesty case was inconclusive and is reported verbatim.
- Case 1 is the FLUX single-step sweep: min donor progress 0.2218 > 0.15, read as "no necessary component", vs the certified route.
- Case 2: a probe perfect at 16/16 is still blind to what the consumer decodes.
- Case 3: a raw 0.9537 collapses to 0.0 under centering.
- Public bundle: `research/papers/pointwise-instruments-miss-distributed-circuits/evidence/instrument-trial/`; also `~/domains/instrument-trial` (`instrument-trial-verify`).
- Caveat: the "community" arms are the author's implementations of standard recipes.

**SAE, preregistered, public tools** (SAELens; `gpt2-small-res-jb`; Gemma Scope `gemma-scope-2b-pt-res-canonical`):
- Gemma-2-2B: top-20 features at the best layer remove 29% vs 0.5% for random features.
- Subject-restricted ranking across all layers removes 63% (identity) / 90% (color), vs random 11% / 35%.
- GPT-2: concentrated, so one layer suffices (a space circuit).
- Source: `pointwise…/paper.md` §4.4; `experiments/2026-09-22-sae-comparison/` (public).

**TransformerLens parity:** 4.6×10⁻⁵ to 1.5×10⁻⁴ nats over 504 cells. Gemma FP32 does not fit in 16 GB.

**Single-layer K/V panel:**

| model | best single layer | second half |
|---|---|---|
| Gemma-2-2B | .08 | .94 |
| Qwen2.5-1.5B | .08 | .92 |

The in-forward artifact on Qwen2.5-1.5B is 0.99 vs 0.00 isolated (`pointwise…/paper.md` §4.2–4.3, public).

**Attribution patching** is used as the SAE ranking score.

**Anthropic Circuit Tracing.** Its stated limitations are frozen attention and unexplained cross-position flow. Time circuits on the K/V cut are exactly cross-position, time-accumulated transport.

- **TODO [W]:** say what the QK-tracing follow-up does and does not address.
- **TODO [E6] (optional):** a live baseline with ACDC on GPT-2 or Gemma-2-2B, and/or an attribution-graph tool, on the same contrasts. Prediction: such tools localize the space circuit in GPT-2 and diffuse or miss the time circuit in Gemma-2-2B. Cost: minutes for ACDC on GPT-2, hours for attribution graphs.
- **TODO [E2b]:** a zero / mean / resample ablation sensitivity check on the SmolLM2 or Gemma sink and on FLUX all-step ablation, answering Miller et al. 2024. Under 5 minutes per model.

## 10. Consequences: what time circuits explain about editing and generation

Each result is framed as a consequence of the route being built over time.

1. **Edits must be installed early.**
   - Hotpatch 4/4: early cut 0.904–0.971, late cut 0.095–0.358.
   - A hostile donor steers to its own target (0.926–0.953); sham ≈ 0; exact rollback.
   - Source: `research/bfl/demos/real-hotpatch-cinema.md`, `counterfactual-diffusion-futures.md` (public, with verifiers).
2. **When you write selects what changes.**
   - Violet eyes: a late write gives violet eyes with composition kept (P 0.069); an early write moves the image while the eyes stay blue (0.577).
   - Program-only 0.712, register-only 0.404, both exact.
   - Jobs `job-eb10b3c02dc5`, `job-a5985d4ac3a9`.
   - Source: `research/demos/scene-editing.md` (untracked).
3. **Moving an object is a space × time conjunction.**
   - Steps 0–1 do the move; late-only departure is 0.0006; departure 0.998 / arrival 0.74.
   - Source: `saturn/experiments/2026-09-20-flux2-transport-temporal-carrier/FINDINGS.md` (private).
   - Puppeteer: ΔRMS grows 8.0–21.9× from joint.0 to joint.4; grip ∪ route ∪ departure is clean 4/4 (`saturn/experiments/2026-09-19-flux2-puppeteer-carrier-origin/FINDINGS.md`, private).
4. **Small early writes are amplified.**
   - Empty-context scaffold: 80–89% of the damage enters at step 0 (`research/bfl/demos/empty-context-positional-scaffold.md`).
   - Apples counting patch: 55,297 params at joint.2 / step 0 turn 3 apples into 5, and held-out exact-count rises 37% → 72%. Its collateral gate *fails* (48% of ordinary prompts disturbed), so accumulation cuts both ways (`research/bfl/demos/recipient-native-capability-patch.md`).
   - Temporal carrier compiler: authority by step is 0.035 / 0.228 / 0.508 / 0.722 (`temporal-carrier-compiler.md`).
5. **Scenes compile.**
   - The prompt lowers to static K/V installed across the run: 21/21 exact across 7 specimens / 5 families; complete install MAE 0.0000, partial fails (`job-5b20cdbb0f15`).
   - SDXL decoder: "the route carries a trajectory, not a point" (`job-5ff713bb2342`).
   - Sources: `research/demos/scene-generator.md`, `sdxl-decoder.md` (untracked).
   - Survey: `obsidian/blog/2026-09-30-165158-the-scene-generator-survey-the-machine-is-prompt-agnostic-the-program-is-not.md`.
6. **Writing through the route from another model.**
   - Cross-model symbol table: anchored authorship at native parity (`job-0706b0497903`, public).
   - Held-out read 21/36 after template collapse (was "35/54").
   - Zero-shot authorship is at sham level, with an affine-ceiling argument (`saturn/experiments/2026-08-21-wall-a-addressing/`).
   - Value algebra ports to 9B: .471 vs .076.
7. **Product: Room Studio.** Geometry decides, FLUX paints declared masks, and everything outside is exact (`room-studio/evidence/layered-render-20260928.md`; branch `feat/layered-harmonize`, unmerged). Give it a short paragraph only.

**TODO [R6]:** commit `research/demos/` before citing it (currently untracked), with redaction per the `REDACTIONS.json` convention.

## 11. What failed, and what we retracted

Keep this section. It is the credibility of the paper.

- A universal segment-level depth kernel is retired. What survives is "second-half-loaded, saturating" (IRD §8).
- Kernel-weighted constructive editing is at sham level at 1.7B and family-dependent at 8B (C8).
- The V4 hallucination predictor was struck. F-F (early exit) was a self-comparison. F-D was refuted in 4 families.
- C5 attribution is non-monotone: pass ≤ 1.7B, fail at 8B, pass at 30B.
- The crossed-pairing "leak" was oracle degeneracy and is retracted (`obsidian/blog/2026-08-26-105431-the-leak-was-in-the-oracle-not-the-address.md`).
- The rank-16 clock controller is retracted.
- `scene.bind_relation` v3 was a donor-present paste and is retracted (`obsidian/blog/2026-09-12-222447-the-picture-called-our-bluff.md`).
- "Topology 5.6×" was weakened.
- Instance binding is not established: the old writer's target switch is byte-identical 12/12, and an instance-ID change moves 0 pixels.
- The capability patch failed its collateral gate.
- The nonlinear interaction compiler loses to the additive baseline on held-out (0.716 vs 0.735).
- Blind route discovery (Aug): Qwen2.5-0.5B produced a trend without a certificate (`saturn/experiments/2026-08-23-mimas-blind-final-boss/`). On FLUX (Aug, `job-dbf7448dc00e`), all 3 target edges were recovered but only 1/3 survived the wrong-depth control. Report this as an address-specificity limit.

## 12. Limitations
- **Denominators:** n ≤ 4 per language-model cell; most diffusion results are 2 seeds.
- **Readouts:** single-token readouts in language models.
- **Breadth:** one lab, no external replication.
- **Private receipts:** 8B, 30B and SDXL receipts are private. TODO [E3] and TODO [R6] reduce this.
- **What the certificate does not show:** it identifies causal topology at a cut, not minimality or every computation on the path.
- **Address specificity:** the route is a causal region; depth-specific addressing is not established (§11).
- **Attention:** time circuits explain what moved and where, not why attention attended.

## 13. Related work

**TODO [W]:** expand.
- **Patching methods:** activation and path patching (Meng 2022; Wang 2022; Zhang & Nanda 2023; Heimersheim & Nanda 2024).
- **Window patching and its caveats:** ROME's 10-layer windows; Hase 2023 ("Does localization inform editing?").
- **Self-repair:** McGrath 2023 (Hydra); Rushing & Nanda 2024.
- **Faithfulness:** Miller 2024 (metrics not robust); IOI's about 87%.
- **Decomposition tools:** SAEs and transcoders; Circuit Tracing / Biology (Ameisen 2025; Lindsey 2025) and the QK follow-up; ACDC.
- **2026 work on the same phenomenon:**
  - *Single-Position Intervention Fails* (arXiv 2605.04061);
  - *Single-Layer Activation Edits Easily Corrupt Factual Recall but Rarely Repair It* (TrustNLP 2026).
  - Engage both directly: they observe distributed effects; we add the certificate, the cut result, the diffusion route and the static/dynamic decomposition.
- **Diffusion:** Prompt-to-Prompt; Stable Flow (2411.14430, vital layers in FLUX); KV-Edit (2502.17363); diffusion timing literature.
- **Task and function vectors:** Hendel 2023; Todd 2024.
- **Cross-model work:** relative representations (Moschella 2023); universal SAEs / SPARC; the linear representation transferability hypothesis.
- **Padding tokens as registers:** Padding Tone (2501.06751), which confirms our predicate-row finding.

## 14. Conclusion (draft)

Two classes of circuit, one certificate to tell them apart:
- space circuits are what the field's instruments find;
- time circuits are what the output reads, and they are invisible to those instruments by construction;
- the evidence is a certified route in a production DiT plus the same certificate shape in four language models above 0.5B;
- a static/dynamic decomposition turns the class into an editing and compilation interface.

---

## Appendix A — Experiments still to run (TODO [E#])

Costs come from recorded wall-times: FLUX panels run in minutes per group with one model load; language-model panels take 52–284 s per model on an RTX 4080. Run under mrun on Beast, one seed first per the prototype policy, then a second seed for paper evidence.

| ID | Experiment | Closes | Est. cost | Priority |
|---|---|---|---|---|
| E1 | Off-route span sweep at the certified Klein-4B / 4-step point (`joint.0–1`, `joint.2–4` without `single.0`, image-only, all-joint ceiling, `single.*` spans); same axes, seeds and gates | §5.4 "just the bridge" objection | single-digit minutes | **High** |
| E2b | Zero / mean / resample ablation sensitivity on the LM sink and FLUX all-step ablation | Miller 2024 critique | < 5 min per model | **High** |
| E3 | Isolated-swap reruns: SmolLM2-1.7B identity, Qwen3-8B; redacted public bundles with `verify.py` for 8B and 30B | public AR evidence | < 2 min per model, plus packaging; 30B larger | **High** |
| E4 | Recovered-loss R for the Pythia-70M writer and 5-head set under mean and resample ablation, with size-matched random sets (replaces excluded 2026-09-30 runs) | §7.2 space-circuit completeness | minutes | Medium |
| E5 | SSM recurrent-state cut: find results of `job-beb10c04a81d` / `job-a97cb1825d39`, rerun if absent | §6.3 scope | minutes to an hour | Medium |
| E6 | Live ACDC (GPT-2, Gemma-2-2B) and/or attribution-graph baseline on the same contrasts | §9 head-to-head | minutes (ACDC GPT-2) to hours | Optional |
| E7 | Multi-seed necessity for the FLUX color contrast | §5.2 | minutes | Medium |
| E8 | Nine-gate certificate on Klein 9B, 2 seeds, ≥ 1 axis | §5.5 breadth | under an hour | Optional |
| E9 | Four-quadrant certificate on one SDXL route | §5.6 breadth | under an hour | Optional |
| E10 | C7 redesign: intermediate-step swap, ≥ 20 items, vs truncation and mistake-insertion | §6.6 | under an hour | Optional |
| E2 | Completeness falsifier (incremental vs full replay) on the 206-cell skeleton | §8 completeness | build plus minutes | Optional |

## Appendix B — Collation and corrections, no compute (TODO [R#])

| ID | Item |
|---|---|
| R1 | Timeline figure, Aug 5 → Sep 22, from the week-in-review post and Appendix C. |
| R2 | Confirm the SDXL writer-clock results are independent of the retracted rank-16 clock controller. |
| R3 | Fix the mis-cites: diffusion four-quadrant numbers → `job-7d53e47755f7` / case-1 ledger; 30B → `job-7cc5b24954f0` / `job-ef8408d9c3d2`; scene-edit .9133 → `research/bfl/demos/scene-circuit-certificate.md` + `bfl/artifacts/scene-circuit-certificate/` (not `job-3cd13239dd91`). |
| R4 | Reword "certificate arrives with capability" for 410M (strict at step 16000). |
| R5 | Same-model space + time table for Qwen2.5-0.5B from `job-ec1ab31d35f2` and `job-72f0e98679d5`. |
| R6 | Commit and redact `research/demos/` before citing (scene-editing, scene-generator, jen, sdxl-decoder). |
| R7 | Pointwise paper's Pythia-70M single-layer claim (`paper.md:149`) has no receipt in its folder. Locate it or drop it. |
| R8 | Symbol-table read count: use 21/36 (post template-collapse), not 35/54. |
| R9 | Carry the eyelid correction for `ears_upright_folded`. |

## Appendix C — Source map (where each part of the story lives)

**Papers and whitepapers:**
- `research/bfl/docs/certified-semantic-circuits/paper.md` (published FLUX route; verifier)
- `research/papers/pointwise-instruments-miss-distributed-circuits/` (published measurement paper; SAE, TransformerLens, instrument trial, four-quadrant evidence)
- `research/papers/integral-residual-dynamics/paper.md` (theory draft; C1–C8; cut; scale floor; kernel)
- `research/papers/capabilities-as-transactions/paper.md` (transaction draft; K/V chain; leaks)
- `obsidian/whitepapers/certified-semantic-circuits-flux2.md`

**BFL demos** (public, with verifiers under `research/bfl/artifacts/`):
- twenty-axis-semantic-route-circuit
- cross-compiled-conditioner
- cross-family-conditioner-repair
- route-cartographer-consumer-closure
- semantic-circuit-object-part-I / II / III
- distributed-kv-causal-route
- diffusion-time-causal-clock
- real-hotpatch-cinema
- counterfactual-diffusion-futures
- wall-picture-hotpatch
- recipient-native-capability-patch
- typed-snake-topology-interaction
- temporal-carrier-compiler
- nonlinear-interaction-compiler
- empty-context-positional-scaffold
- scene-circuit-certificate
- scene-relations-and-instance-binding
- textless-klein-renderer
- multi-model-structural-tracer
- model-family-forensics

**Research demos** (untracked): `research/demos/` scene-generator, scene-editing, jen-character-register, jen-sprite-register, anime-sprite-register, sdxl-decoder, static-decoder.

**Timeline and synthesis posts** (`obsidian/blog/`):

| Date | Post |
|---|---|
| 2026-08-11 | `the-autoregressive-source-circuit-closed` |
| 2026-08-13 | Thott posts |
| 2026-08-14 | `we-watched-a-capability-being-born` |
| 2026-08-20 | `214500-the-instruments-took-the-stand` |
| 2026-08-21 | `114500-the-final-boss-circuit`; `133000-the-integral-had-weights`; `165323-the-sink-was-later-than-we-thought`; `171243-mimas-put-the-transformer-on-trial` |
| 2026-08-23 | `032321-the-sink-was-a-pipeline`; `132131-the-final-boss-became-a-transaction`; `151546-mimas-found-the-late-route-not-the-final-boss` |
| 2026-08-25 | `171913-the-final-boss-was-not-disproved-it-became-a-transaction`; `221529-the-final-boss-was-a-role-not-a-layer` |
| 2026-08-26 | `001538-program-review-three-walls…`; `084513-from-circuits-to-transactions`; `105431-the-leak-was-in-the-oracle…`; `142017-the-route-holds-the-coordinates-move`; `151627-the-hypergraph-had-a-skeleton`; `184423-the-skeleton-survived…` |
| 2026-08-28 | `105410-the-model-was-a-runtime-not-a-dictionary`; `141114-the-control-map-and-the-circuits-we-have`; `221644-the-week-in-review…` (**timeline**) |
| 2026-08-30 | `172904-the-scene-transaction-machine-runs-on-a-stable-chassis` |
| 2026-08-31 | `110633-from-the-final-boss-to-a-debuggable-circuit-runtime` |
| 2026-09-01 | `231018-we-found-the-native-scene-compiler` |
| 2026-09-03 | `111020-recorder-basins-and-final-boss-skeleton-survey` |
| 2026-09-04 | `151836-from-final-boss-to-saturn-vm`; `212009-two-rows-five-depths-one-operation` |
| 2026-09-08 | `211251-from-the-final-boss-to-executable-models` |
| 2026-09-12 | `222447-the-picture-called-our-bluff` |
| 2026-09-30 | `165158-the-scene-generator-survey…` |

Ledger: `obsidian/2026-08-21-113000-wall-a-ird-campaign-ledger.md`.

**Experiment records:**
- `saturn/experiments/2026-08-21-wall-a-addressing/README.md` (addenda K–AC)
- `2026-08-21-ird-verification-battery/`, `2026-08-21-ird-fruit-battery/`
- `2026-08-21-multitoken-transport/`
- `2026-08-20-instrument-trial/`
- `2026-08-23-mimas-blind-final-boss/`
- `2026-08-25-natural-task-state-kv-causal-chain/`
- `2026-08-19-object-multimodel/`
- `2026-09-18-flux2-spectral-instance-binding/`
- `2026-09-19-flux2-puppeteer-carrier-origin/`
- `2026-09-20-flux2-transport-temporal-carrier/`
- SDXL rosetta series `2026-08-30…2026-09-01`
- Registry: `saturn/docs/IRD-CERTIFICATES.md`

**Code:**
- `saturn/src/saturn/circuit_certificate.py`, `circuit_incremental.py`, `execution_skeleton.py`, `dynamic_circuit.py`, `static_projection_cache.py`, `circuit_thought_trace.py`, `spectral_address.py`
- `saturn/src/saturn/mimas/`
