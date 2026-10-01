---
title: "A New Class of Circuits: Space and Time"
subtitle: "Localized circuits, time-accumulated circuits, and why standard instruments see only the first kind"
type: research-paper
status: draft-2
date: 2026-09-30
author: Jacob Hollenbeck
outline: outline.md
supersedes_for_external_release:
  - ../integral-residual-dynamics/paper.md
  - ../capabilities-as-transactions/paper.md
builds_on:
  - ../../bfl/docs/certified-semantic-circuits/paper.md
  - ../pointwise-instruments-miss-distributed-circuits/paper.md
tags: [interpretability, circuits, diffusion, language-models, state-space-models, causal-mediation, time-accumulation]
---

# A New Class of Circuits: Space and Time

Jacob Hollenbeck

*Draft 2, 2026-09-30.*

> **Draft notes.**
>
> **TODO markers.**
> - **TODO [E#]**: an experiment that is still running or has not been run (Appendix A).
> - **TODO [R#]**: a correction or collation that needs no compute (Appendix B).
> - **TODO [W]**: writing only.
>
> **Conventions.**
> - Numbers are measured unless marked otherwise, and receipt paths are inline.
> - "Public" means a receipt is bundled with a verifier under `research/`. "Private" means it exists only under `saturn/`.
> - At the author's direction, results from the 2026-09-30 blind-certification and grail tooling are excluded.
>
> The section-by-section evidence map is in [`outline.md`](outline.md).

---

## Abstract

**Space circuits.** Interpretability finds circuits one site at a time: a head, a feature or an edge whose removal hurts the behavior and whose insertion restores it. We call these *space circuits*. The standard instruments — activation patching, sparse-autoencoder ablation and attribution graphs — are built to find them.

**Time circuits.** We describe a second class that these instruments cannot see. A *time circuit* is a behavior constituted by a path along an accumulation axis:
- the denoising steps of a diffusion model;
- the layers of a token's key/value trace in a transformer;
- the recurrent state of a state-space model.

No single site on the path is necessary, but the path as a whole is. A four-quadrant certificate separates the two classes: single-site and whole-path ablation, single-site and whole-path writing. All four are judged by the model's unchanged output, behind an exact-replay gate.

**FLUX.2 Klein 4B is a clean time circuit.** A text-stream carrier across the denoising steps transports every semantic contrast we tested.
- Transplanting the target state at one step leaves the image far from the target (pixel MAD 48.4); at all steps it reproduces it (0.47).
- Removing any single step leaves the target (color contrast, 5/5 seeds). Removing all steps reverts the image to the source (interchange) or to the null image (deletion).

**Language-model stores are time circuits on necessity, but they are written once and committed late.** This holds in SmolLM2, Qwen2.5, Pythia, Gemma-2 and Mamba.
- **Necessity is path-constituted.** In the cleanest cells the best single layer carries ≤ 0.08 of the effect, while the second half of the trace carries 0.92–0.94.
- **The write is not distributed.** One residual write at the subject authors the answer from any layer up to a late commit band at about 0.7–0.9 of depth.
- **A commit ledger accounts for the store.** The residual write equals the sum of the downstream per-layer commits. It holds within 0.02–0.15 in Mamba, where the committing layer is the one that stops its own clock. In transformers it is redundant over 1–3 layers; in Gemma-2 only the sliding-window layers commit.
- **The store is read at the commit layer.** That read can be replaced by an exact-row join.
- **A computed answer is written in two places.** In addition problems, the operands are committed early at their own positions and the sum is formed late at the query position.

**Standard instruments see the controls, not the class.**
- *A space circuit, found:* on Pythia-70M induction, three heads are necessary and sufficient (recovered loss ≈ 1.0), and one head alone carries 0.58–0.72 of the necessity.
- *Anthropic's circuit tracer misses the store.* On the same Gemma-2-2B panel where a whole-state cut over the second half flips 83–84% of answers:
  - its attribution graph places the subject's largest layer at L0 and routes about 30% of influence through error nodes;
  - no feature-level intervention it supports — zero-ablation or a matched interchange; its own top features or all ~18,000 features at every position — converts the identity more than 0.08 of the way (median), and none flips more than 1 of 12 answers.
- *Elsewhere:* single-step patching reports the FLUX carrier as absent, and in a blind-graded trial four standard readouts gave the wrong verdict in 4 of 4 cases.

**Why it matters.** A time circuit has no single site to find, ablate or edit. The consequences are concrete:
- edits must be installed early;
- *when* a write lands selects *what* changes;
- a prompt compiles to an installable source that reproduces native images exactly.

---

## 1. Introduction

**Space circuits.** When interpretability researchers say a model "has a circuit" for a behavior, they usually mean a localized subgraph. Activation patching, path patching, automated circuit discovery, sparse-autoencoder feature ablation and attribution graphs all ask, in different ways, *which site matters*. They find what they are built to find: components whose removal hurts and whose insertion helps [Meng 2022; Wang 2022; Conmy 2023; Ameisen 2025]. We call these **space circuits**. They are real, and we certify some ourselves (§7).

This paper is about the circuits those tools cannot see.

**The anomaly.** It came from a production text-to-image model, FLUX.2 Klein 4B. We patched each site of a candidate route at a single denoising step and found nothing:
- transplanting the target's state at one step left the image at pixel distance 48.4 from the target;
- ablating one site at one step left the target intact (distance 7.9).

Under the field's standard instrument there was no necessary component and no sufficient one. Yet the same sites, patched across all four denoising steps, transferred the target almost completely (distance 0.47), and removing them across all steps reverted the image to the source. The internal separation between the two prompts grew at every step: 0.355, 0.919, 2.487, 9.723.

The route was carrying its signal *across time*. Each step's contribution was dispensable only because the other steps re-derived it [certified-semantic-circuits §5].

**Time circuits.** We call these **time circuits**. Our working name was the "final boss": the conjecture that a model funnels its output through a late, path-constituted store that smaller circuits write into [`obsidian/blog/2026-08-21-114500-the-final-boss-circuit.md`]. In language models, the whole-path half of the same certificate holds, with the accumulation axis being the depth of a token's key/value trace. Full sweeps, however, usually find a late writer layer inside that path. The cleanest time circuit we have is the diffusion one.

**Contributions.**
1. **Definition and certificate.** A definition and a certificate that separate space circuits from time circuits (§2).
2. **A time circuit in a production diffusion transformer.** It is located, controlled against alternative paths, and holds under both counterfactual and deletion interventions (§5).
3. **Path-constituted stores in language models, and a recurring late writer.** At the cut that carries state, a token's whole stored trace is necessary and sufficient. Full single-layer sweeps, now required, show that most cells also contain one late writer layer at ~0.7–0.9 of the depth, in transformers and Mamba alike. This retracts several sampled certificates (§6).
4. **Same-model contrasts.** Contrasts between space and time circuits in one model, including concentrated writers hidden inside otherwise distributed paths (§7).
5. **Static and dynamic decomposition.** A static-infrastructure / dynamic-circuit decomposition of the time circuit, with the editing and compilation results it explains (§§8, 10).
6. **Instrument failures.** Measured evidence that standard instruments miss this class, including a blind-graded trial and public-tool comparisons (§9).

**Boundaries.**
- We certify circuits per model. The diffusion and autoregressive instances share a *certificate shape*, not a physical circuit.
- The original language-model grid uses single-token readouts and at most four items per cell.
- FLUX whole-path deletion is non-specific and, at the input cut, equals removing the prompt (§5.5).
- We explain *what* moved, *where*, and to which consumer, but not why attention attended there (§12).

> **TODO [W]:** position this work against the limitations Anthropic states for Circuit Tracing:
> - attention patterns are frozen;
> - for cross-position flow, "we account for the information which flows from one token position to another, but not why".
>
> Also cover their QK-tracing follow-up [transformer-circuits.pub/2025/attention-qk]. Keep the claim modest.

## 2. Two classes of circuit

### 2.1 Definitions

**Setup.** Fix:
- a model;
- a behavior with a clean source condition and a target condition;
- an **accumulation axis** t;
- a **cut**: a typed interface at which state can be read and written, such as key/value rows, a block's output on the text stream, or a recurrent state.

The behavior is judged by the model's own unchanged **consumer**: its next-token distribution, or its scheduler and decoder rendering pixels.

- **Space circuit.** A set of sites S such that interventions on individual members of S have measurable necessity or sufficiency.
- **Time circuit.** A set of sites P along t that meets four conditions:
  - (i) no single site is necessary;
  - (ii) no single site is sufficient;
  - (iii) the whole path is necessary;
  - (iv) the whole path is sufficient.

**Formally.** Split the state at the cut into a prompt-invariant scaffold and a prompt-specific residual, x(t) = s(t) + r(t). A space circuit is visible in r(t*) at some site t*. A time circuit is visible only in a functional of the trajectory, R = 𝓘(r(t)) [integral-residual-dynamics §2].

**What is and isn't claimed.** The **wiring fact** — the consumer reads the final state, so whatever controls the output is present there — is close to a tautology and is *not* our claim. The claim is that the controlling object is path-constituted at the cut. The four-quadrant pattern below is the falsifiable signature of that.

### 2.2 The four-quadrant certificate

|  | single site | whole path |
|---|---|---|
| **necessity** (ablate) | behavior survives | behavior dies |
| **sufficiency** (write) | nothing happens | full authorship |

**Why this pattern discriminates.** A localized circuit passes at least one single-site quadrant. A diffuse but linear representation fails the whole-path quadrants too. Neither alternative produces this cross.

**Validity gates.** These are hard requirements, not successes:
- **exact no-op:** a zero-magnitude write reproduces the native output bit-for-bit;
- **exact uninstall;**
- **capability:** a clean capability margin;
- **floor separation:** separation from the generic-prompt floor.

### 2.3 Reading rules

1. **The cut matters.** A certificate is a statement about a cut, not about an architecture (§6.4).
2. **Use isolated swaps.** In a transformer, an *in-forward* key/value swap lets the subject token read its own replaced entries, which silently turns one layer into many. The *isolated* swap replaces cached entries after the subject has run normally, so only later reads change. On Qwen2.5-1.5B the two give 0.99 and 0.00 for the same layer [pointwise §4.3]. Isolated swaps are primary.
3. **Sweep every single site.** Two "representative" single layers are not enough. Full sweeps have exposed concentrated writers that sampled layers missed, in a transformer and in all three Mamba models (§§6.1, 6.4, 7.2).
4. **Name the intervention.** Counterfactual (interchange) replacement and deletion (zero, mean, resample) ask different questions. A carrier can be necessary under one and redundant under the other (§5.5).
5. **Read the gap, not the whole-path ablation.** Whole-path ablation of a token's state is close to deleting the token. The informative result is the single-site *failure* together with the size of the gap.
6. **Read the formed circuit; write through the residual.** A time circuit is *formed* over steps or layers. Necessity is read at the cut that carries the formed state: isolated K/V in transformers, the recurrent state in Mamba, the text stream in FLUX. Writes go through the **residual** at the source position, and the model forms the circuit itself.

   Installing formed K/V or state directly tests a different object. The in-forward K/V write is a hybrid: the subject token reads its own patched entry, so part of the write leaks into its residual and propagates to later layers.

   Precedent (Wall-A P4, SmolLM2, `job-0a07cb92d360`):

   | write | site | result |
   |---|---|---|
   | one residual write at L12 | residual | 1.006 |
   | one K/V write at L12 | formed K/V | 0.010 |
   | the full K/V trace | formed K/V | 1.093 |

   The FLUX route writes are text-stream (residual) writes. The language-model panel writes in §6.1 and the Mamba state writes in §6.4 are formed-circuit writes, and are being re-measured through the residual.

   > **TODO [E16] (running):** residual-write sweeps for every panel cell and for Mamba. These give the per-layer profile of where one residual write still authors the target (a formation window). The Qwen2.5-1.5B smoke shows one write authoring from any layer up to L23 and failing after L23–24, where the K/V late writer sits. Rewrite §§6.1 and 6.4 from the full result.

## 3. Method: exact replay judged by the native consumer

**Why exact replay.** Time circuits can be checked only by an instrument that can:
- capture a computation once;
- fork it many times, with one value replaced at every step or layer;
- replay the remainder exactly.

Approximate replay would bury a 1–2% single-site effect in numerical noise.

**Execution model.** Saturn represents model state as typed **Frames** and interventions as **Acts**. An Act declares its reads, writes and invalidations. A **StateCut** names an execution boundary from which matched futures can be forked.

**The exact no-op gate is measured, not assumed:**
- diffusion resume reproduces a mean RGB difference of 0.0;
- text resume reproduces identical tokens and logits;
- FLUX reproduces 8/8 images bitwise across two residency schedules [pointwise `appendix-execution-model.md`].

**Origins.** The runtime grew from an observation about Mamba. A resident Mamba-2.8B decoded at 34.2 tokens/s while a paged path managed 0.27. That gap separated four things: checkpoint bytes, executable pages, request state and output contracts [`obsidian/blog/2026-07-19-from-fast-mamba-to-a-100x-model-runtime.md`].

The first family-local transactional Act was built for Mamba-130M. Because Mamba mutates its cache in place, the Act refuses caller-owned caches and returns state only after a complete forward commits [`saturn/experiments/2026-08-13-mamba-phase8-atomic-act/README.md`].

**Thott.** An early instrument, Thott, read the transformer key/value cache as position clock × token address × contextual residual:
- de-rotating RoPE raised within-token phase coherence from 0.51 to 0.87;
- a codebook-only replacement was refuted: the clock × codebook key reconstruction reaches relative L2 error 0.189, but continuation agreement is only 0.047, and it diverges at step 2 (`job-080c3550be62`, E-X4);
- the residual, which grows with depth, was load-bearing. The decomposition native KV = clock/address base + contextual residual is implemented in `saturn/src/saturn/context_residual.py` [`obsidian/blog/2026-08-13-thott-from-cache-diff-to-circuit-thought.md`].

**FLUX has no mask over its conditioner.** All 512 conditioner rows are live keys at distinct RoPE positions, so the address there is position and occupancy (`job-79ff59eb54d2`, E-A).

That decomposition motivated using the key/value cut in language models.

**Model virtual memory.** The same transactional runtime exposes model state as mountable pages: transformer K/V pages (`CausalContextVM`) and Mamba per-layer (C_ℓ, H_ℓ) state pages (`MambaStateVM`). Operations are mount, fork, swap, diff, unmount, per-layer sweep and clock, and each is labeled as a formed-state read or a residual write (rule 6). The Mamba VM reproduces the paper's per-layer necessity sweep bit-for-bit, and the residual-write sweep to 3 decimals, from an independent implementation (`job-7075c40c839b`).

**Gates for FLUX.** Nine gates [certified-semantic-circuits §3]:
1. replication on two seeds;
2. sufficiency P ≥ 0.90;
3. necessity ≤ 0.15;
4. wrong-axis ≤ 0.35;
5. energy-matched sham ≤ 0.35;
6. dose response;
7. edge mediation ≥ 50%;
8. downstream continuation ≥ 0.75 with alignment ≥ 0.80;
9. replay integrity.

**Gates for language and state-space models.** The four-quadrant certificate with capability and floor gates: pc > 2 and floor gap ≤ 0.5 [`saturn/docs/IRD-CERTIFICATES.md`]. As of this draft, the single-site bars apply to *every* layer: necessity share < 25% and write |s| < 0.2.

**Canaries.** Every experiment reported here as new first reran a published number and proceeded only if it reproduced. Canaries in this draft reproduced byte-exactly (FLUX) or within 3e-4 (language models).

**Evidence ladder.** Results are labeled as one of:
- observation;
- trend;
- convergent trend;
- working inference;
- terminal claim.

A failed gate means "not established by this test", never "absent".

> **TODO [W]:** a one-paragraph comparison with TransformerLens, nnsight and pyvene, from the measurement paper's execution-model appendix.

## 4. How the time circuit was found

**Standard instruments missed it.** Our first single-step panel concluded "distributed relay with no necessary node". That reading is wrong in an instructive way: every node is necessary, but only across time [certified-semantic-circuits §5].

**It was found by swapping subsystems.** FLUX.2 has a clean interface between a text encoder and a frozen image program, so the encoder can be replaced entirely while the rest stays fixed.
- SmolLM2-1.7B and Mamba-1.4B, attached through trained adapters, drove the frozen denoiser to clean, coherent and semantically wrong images.
- Contrasting them with the native Qwen encoder located where the semantics diverged downstream. Route flow was 0.9312 native vs 0.5300 with SmolLM2.
- Full-state rescue reached 0.751 (SmolLM2) and 0.817 (Mamba). Compact selectors reached at most 0.051.
- At the route's entry, the foreign color separation was damped about 43× [`research/bfl/demos/cross-compiled-conditioner.md`; certified-semantic-circuits §7].

**It can also be found without labels.** We propagated random 5%-norm perturbations of an empty prompt to the return state:
- the method recovered three of four route sites and the `joint.4 → single.0` edge;
- clamp mediation removed 83–95% of the effect;
- downstream donation reconstructed 95–100%;
- off-route shams stayed at or below 0.095 [certified-semantic-circuits §8.3].

**A methods vignette.** A "0.2218 / 0.0013" pair circulated in our notes as the single-step / all-step contrast. No instrument produced it. The program's own audit caught it and replaced it with receipt-backed values [integral-residual-dynamics §1]. Plausible numbers that no instrument produced are the failure mode this paper is about.

> **TODO [R1]:** timeline figure (Aug 5 → Sep 30) from `obsidian/blog/2026-08-28-221644-the-week-in-review-from-the-final-boss-to-a-transaction-abi.md` and the source map in the outline.

## 5. A time circuit in a diffusion transformer

**Specimen.** FLUX.2 Klein 4B, revision `e7b7dc27f91deacad38e78976d1f2b499d76a294`, BF16, 256×256, four denoising steps, guidance 1.0. The denoiser has five *joint* blocks, in which text and image tokens form two interacting streams, followed by twenty *single* blocks, in which the streams are merged.

### 5.1 One carrier, every axis

We tested the route `joint.2 → joint.3 → joint.4 → single.0` against twenty semantic contrasts spanning twelve categories.
- **Six pass all nine gates strictly:** lighting .935, identity .920, weather .911, fur .894, orientation .873, relation .866.
- **Eleven** pass every gate except strict pixel reconstruction.
- **Three** remain candidates.

**Held-out tests.**
- **Unopened seeds:** the route gates replicated across the panel. The only route-gate failure missed by 0.002. The strict pixel tier was seed-sensitive.
- **New prompts written after the route was fixed:** four of six strict contrasts replicated strictly, and all six replicated the route, exactly at the preregistered bar.

**Clean-room audit.** An auditor reproduced every decision and caught 5/5 injected tampering attempts [`research/bfl/demos/twenty-axis-semantic-route-circuit.md`; `research/bfl/artifacts/twenty-axis-semantic-route-circuit/`; certified-semantic-circuits §4].

### 5.2 Built over time

| intervention at `joint.4` | single step | all four steps |
|---|---|---|
| transplant the target state (sufficiency) | MAD to target 48.4 (no transfer) | MAD to target 0.47 |
| ablate (necessity) | target intact (MAD 7.9) | reverts to source (−0.93) |

**Separation and mediation.**
- Return-state separation grows monotonically: identity 0.355 → 0.919 → 2.487 → 9.723; color 0.411 → 0.837 → 1.990 → 7.409.
- All-step edge-mediation rescues along the route are .946, .888 and .796 [certified-semantic-circuits §5, Fig. 2].

**Dose is not exchangeable across time.** On the conditioning axis:
- writes weighted ≈ [0.21, 0.22, 0.08, 0.04] across the four steps reproduce the target;
- a late double dose at equal nominal integral reaches only 0.055–0.288, against 0.522–0.810 for the all-step write;
- at identical net-zero dose, order alone moves the output in opposite directions.

These kernels measure reproduction of the target image, not when identity is decided (correction of 2026-09-22) [integral-residual-dynamics §8].

**A second distributed route.** A 20-site key/value route for color binding shows the same pattern [`research/bfl/demos/distributed-kv-causal-route.md`]:
- the all-step graft beats every single step;
- a compact two-site subset fails;
- native margins are +6.740 forward and +8.830 reverse;
- 45/96 reverse donor-color collisions leave bilateral specificity open.

**A causal clock.** The same relative dose has a final effect of 0.360 at resume step 1 and 0.078 at step 7 [`research/bfl/demos/diffusion-time-causal-clock.md`].

**Multi-seed (E7, MEASURED).** The color contrast's necessity holds across five seeds: the original 7217 plus 4242, 9001, 2024 and 1337 (`saturn/experiments/2026-09-30-e7-flux-color-multiseed/`, `job-8d4a3845a671`). The canary reproduces the recorded red↔blue image MAD (70.954 against 70.95) and an exact no-op.

On the route (joint.2 → joint.3 → joint.4 → single.0):
- every single-step removal leaves the blue target on all five seeds, under interchange, deletion and mean ablation;
- all-step interchange reverts to the red source (MAD to source 2–6, to target 70–76);
- all-step deletion falls to the null image on 5/5 seeds.

Deletion is non-specific, because a norm-matched sham also nulls, so interchange is the informative operator.

### 5.3 Coordinate-free

**Direction is shared, coordinates are not.**
- Across axes, per-module activation-difference trajectories are nearly collinear (minimum pairwise cosine 0.986).
- The physical coordinates that carry them barely overlap (mean Jaccard 0.063).

**Position-robust but site-dependent.**
- A one-token subject ("horse") shifts every downstream position, yet the route still transports identity at 0.988.
- Excluding the `joint.4` text site drops transfer to 0.59 and 0.49 [certified-semantic-circuits §6].

The durable object is a typed transition between processing stages, not a set of neuron or token indices.

### 5.4 Where the carrier is

**The objection.** In FLUX, text enters the image stream in the joint blocks and merges at `single.0`. Perhaps the route is just the architectural text-to-image bridge, which would carry every axis.

**The test.** An off-route sweep at the certified operating point: six strict axes, two seeds, nine gates.
- Jobs: `job-bef367be11de` (smoke), `job-4eebfe403976` (full).
- Record: `saturn/experiments/2026-09-30-flux2-offroute-span-sweep/FINDINGS.md`.
- The historical route reproduced the published ledger byte-exactly.

| arm (sites; stream) | axes certified (strict, 2 seeds) |
|---|---|
| route: joint.2, joint.3, joint.4, single.0 (text) | 6/6 |
| all-joint ceiling: joint.0–4, single.0 (text) | 6/6 (the route reaches 93.0–94.7% of its sufficiency) |
| joint.0–1 only (text) | 6/6 |
| joint.2–4 without single.0 (text) | 5/6 |
| route blocks, image stream | 1/6 (orientation only) |
| single.1–4 (text) | 0/6 |
| single.10–13 (text) | 0/6; necessity 0.24–0.68 |

**Reading.**
- **Transport is specific to the text stream through the joint region.** Image positions at the same blocks do not carry it, and neither do text positions in later single blocks.
- **The objection is partly upheld, and sharpened.** The carrier is the joint-region conditioning pathway, not "any path of comparable size".
- **Carriage within the joint region is redundant.** The historical route is one certified instance, not a unique or minimal route.

**Time accumulation is region-wide, not specific to the historical blocks.**
- Setup: we repeated the single-step versus all-step test for five site sets — joint.0 alone, joint.1 alone, both together, the whole joint region, and the route — on three setups (`job-64cc7efe2b22`, `job-67631847af7f`; record `saturn/experiments/2026-09-30-flux2-joint01-time-accumulation/FINDINGS.md`).
- Single-step writes failed in every case (max 0.28 and 0.56 against the 0.90 bar), and single-step ablations left the target intact.
- All-step writes passed (≥ 0.91), and all-step source ablation reverted (dp −0.91 to −0.98).

**Conclusion.** The FLUX time circuit is a time-accumulated text-stream carrier in the joint region. The historical route is its certified representative.

### 5.5 Necessity: interchange versus deletion

**The question.** The FLUX necessity results above replace the route's state with the *source* prompt's state at every step. That is a counterfactual (interchange) intervention. Following Miller et al. [2024], we asked whether the signature survives deletion.

**Full-route all-step result by method** (`job-76991cc209c4`; record `saturn/experiments/2026-09-30-ablation-method-sensitivity/FINDINGS.md`):

| method | dp (−1 = reverted to source) |
|---|---|
| source-state replacement | −0.934 |
| zero | +0.026 |
| prompt mean | −0.367 |
| resample | −0.03 (mean over draws) |

**The dp column misleads for deletion.** dp is a projection onto the source→target axis, so an image with neither content projects to about 0. The residual-cut experiment (E1c) reports the nearest image class and the distance to each reference (`job-a67fd0271b28`; record `saturn/experiments/2026-09-30-flux2-residual-deletion/FINDINGS.md`). Its canaries reproduce E1b and E2b within 5e-4, and its no-op is exact.

Across all 12 cells (four cuts × three setups), the cuts are:
- the residual text state entering joint.0;
- the residual at every joint block;
- the residual at the route blocks;
- the E1b block-output route.

| intervention | any single step | all steps |
|---|---|---|
| zero (deletion) | image stays nearest the **target** | image falls to the **null** (empty-prompt) image; MAD to target 60–81 vs a 37–52 source–target baseline |
| norm-matched random sham | — | null |
| source-state interchange | target (dp > −0.30 at every step) | **source** (dp −0.92 to −1.0) |

**The time-accumulation signature survives deletion.**
- Single-step deletion leaves the target intact, and all-step deletion removes it.
- The two operators differ only in the end state: interchange reverts to the source, while deletion falls to the content-free prior.
- We therefore **retract** the earlier reading (E2b, E1b) that "the target survives deletion". That reading came from dp ≈ 0, which marks the null image, not the target.

**Two caveats.**
- **Deletion is not specific.** The sham also gives the null image.
- **Input-cut deletion is trivial.** At the input cut, whole-path deletion is removal of the prompt by construction: zeroing the conditioning at joint.0 *is* the empty prompt (MAD to null 0.0). This is the diffusion form of reading rule 5. The informative evidence is the single-step failure and the size of the gap, under both operators.

No pooled or global conditioning path exists: the transformer receives only `encoder_hidden_states`. So no bypass is hiding content.

**Contrast with language models.** The language-model signature was robust to every method (§6.2). With the dp artifact removed, FLUX is too, when necessity is read as "removes the target".

> **TODO [W]:** report every FLUX necessity number as nearest class plus MAD to source, target and null, not dp alone. Re-read the certified-circuits paper's necessity column under this rule; its source-interchange values are unaffected.

### 5.6 The FLUX family

The semantic-object interface built on the route replicates across checkpoints at trend level, not as nine-gate certificates [`research/bfl/demos/semantic-circuit-object-part-III.md`].

| checkpoint | result |
|---|---|
| base-4B (undistilled, 50-step CFG) | white fox .888, sham ≤ .13 |
| Klein 9B (one seed) | subject write .743 vs sham .043; cross-scene value port .471 vs .076 |
| FLUX.1-schnell (T5 + CLIP) | object survives at noun-phrase-window grain: single row −.05 / .03, ±3 window .56 / .63 |

On FLUX.1-schnell, the route carries 0.6915 of image progress, 98% of the all-joint ceiling of 0.7069.

> **TODO [E8] (optional):** a nine-gate certificate on Klein 9B.

### 5.7 Other diffusion families

**SDXL (WAI / Illustrious v150), writer program.** It shows a causal diffusion-time clock:
- a rank-1 writer clock explains 0.662 of temporal energy and is sufficient (`job-3d43b5402436`);
- the time-formed schedule transfers to unseen seeds and objects at cosine 0.98–0.9997 (`job-b51e75ec32be`);
- reversing only the schedule melts geometry (`job-00c5ec5ca23f`).

**SDXL scene compiler.** It shows static keys and values with a dynamic query (§8).

**Chroma (DiT).** Its 28-step trajectory invalidates every step after step 0 (`job-3d34f8ee687c`).

All of these receipts are private and come from one checkpoint each.

> **TODO [R2]:** confirm these SDXL results are independent of the retracted rank-16 clock controller.
>
> **TODO [E9] (optional):** a four-quadrant certificate on one SDXL route.

## 6. Time circuits in language and state-space models

### 6.1 Transformer certificates, fully swept

**The original grid.** The original sink grid (Aug 21) certified subject-identity and color cells in SmolLM2-1.7B, Qwen2.5-0.5B, Qwen3-8B and Qwen3-30B-A3B. Each cell sampled two single layers (`saturn/docs/IRD-CERTIFICATES.md`).

**The motivating cell: SmolLM2-1.7B identity** (`job-6650205b45eb`). The clean answer is *fox*, at a +2.958-nat margin.
- **Necessity:**
  - replacing the subject's keys and values at L12 alone moves the answer log-probability by +0.031 nats (1.5% of the whole-path effect);
  - at L18 alone it moves by +0.403 nats (19.3%);
  - across the second half of the stack it moves by −2.088 and flips the answer to *wolf*.
- **Sufficiency:**
  - writing the target's full key/value trace authors the target (1.058–1.093);
  - a single layer carries 0.010–0.107.

The sufficiency run was killed by a memory leak after that leg finished, so its numbers come from the log receipt (`job-0a07cb92d360`).

**Full isolated sweeps change the grid.** Records: `saturn/experiments/2026-09-30-isolated-swap-reruns/FINDINGS.md` (E3) and `saturn/experiments/2026-09-30-full-layer-sweeps/PLAN.md` § Outcomes (E3b; results in `results/`).
- E3 jobs: `job-1be7f297d707`, `job-478bbaddb07b`, `job-096fb0a5197a`.
- E3b jobs: `job-1939cff2561e`, `job-7f98e89caaf1`, `job-a66f47c5f2a2`, `job-9c383862e6f9`.
- E3b canary: `job-76104f076045` reproduced SmolLM2 identity L19 0.3053 exactly.

Every necessity number is from the isolated swap with every single layer swept. The "single-layer write" column is the **in-forward K/V write** into a filler prompt, a formed-circuit write that partly leaks into the residual (rule 6). Qwen2.5-1.5B's L0 write of 0.985 is that leak. Residual-write profiles replace this column after E16. "Relative depth" is the writer layer's index divided by the layer count.

| cell | n | best single layer: necessity share (95% CI) | best single-layer write | second half (flip) | whole-path write | reading |
|---|---|---|---|---|---|---|
| Qwen2.5-1.5B identity | 42 | 0.079 at L23 | 0.985 at L0 (leak); **0.808 at L23** | 0.923 (0.905) | 1.00 | necessity-clean; K/V write concentrated at L23 |
| Gemma-2-2B identity | 42 | 0.078 at L22 | **0.809 at L22** (isolated; sliding-window layers L16/18/20 also 0.39–0.66) | 0.943 (0.83) | 1.00 | necessity-clean; write concentrated at L22 |
| Gemma-2-2B color | 25 | 0.151 at L20 | **0.648 at L20** (isolated) | 0.811 (0.84) | 1.00 | necessity-clean; write concentrated |
| SmolLM2-1.7B color | 27 | 0.098 at L18 | 0.542 | 0.939 (0.89) | 1.00 | necessity-clean; write concentrated |
| Qwen3-8B identity | 1 prompt | degenerate (scene prior) | 0.0018 | at the floor | 1.000 | write-clean; necessity degenerate |
| SmolLM2-1.7B identity | 34 | **0.305 at L19** (0.239–0.383) | **0.991 at L19** | 1.072 (0.97) | 1.00 | late writer, depth 0.79 |
| Qwen2.5-0.5B identity | 42 | **0.355 at L21** (0.285–0.408); L20 0.352 | **0.747 at L21** | 1.096 (0.93) | 1.00 | late writer pair, depth 0.83–0.88 |
| Pythia-410M identity, step 4000 | 36 | **0.318 at L16** (0.175–0.381) | 0.305 at L16 | 1.046 (0.86) | 1.00 | late writer, depth 0.67 |
| Pythia-410M identity, step 16000 | 39 | **0.507 at L17** (0.340–0.549) | **0.712 at L17** | 1.105 (0.90) | 1.00 | sharp late writer, depth 0.71 |
| Qwen2.5-0.5B color | 8 of 30 | 0.476 at L20 | 0.559 | 1.354 (1.0) | 1.00 | under-powered; inconclusive |
| Qwen3-30B-A3B identity | batched | flat ~1.18 at every layer; no ablation flips | 0.338 at L40 | no flip | 1.000 | no isolated certificate |

**Reading.**
- **The whole-path half holds in every powered cell.** The second half of the subject's key/value trace is necessary (flip 0.86–0.97), and the whole trace authors the target (1.00).
- **Single-layer behavior splits.**
  - Three cells are necessity-clean: Qwen2.5-1.5B, Gemma-2-2B and SmolLM2 color.
  - Four cells contain a late writer that carries 30–51% of necessity and up to 0.99 of the write: SmolLM2 identity, Qwen2.5-0.5B identity, and Pythia-410M at both steps.
- **SmolLM2 color is not clean on both halves.** Its necessity is clean, but its best single-layer write (0.542) exceeds the 0.2 bar.
- **No language-model cell yet passes all four quadrants under full sweeps.** The two necessity-clean identity cells were never write-swept.

**Qwen3-30B-A3B.** The public certificate [`evidence/ar-certificates/`] used the *in-forward* swap. Under the isolated swap, the in-forward reproduction is bit-exact (clean margin 7.2817), but no ablation, single or whole-path, flips the answer, and necessity is flat across all 48 layers. We read the in-forward 30B certificate as a confound of the in-forward swap: it lets the subject read its own replaced entries (§2.3). The bundle stays public as a record of the in-forward protocol, and this paper does not cite it as a time-circuit certificate.

**E15 result (MEASURED).** Neither remaining cell passes all four quadrants. Gemma-2-2B (`job-ed4ce1ac5974`, 78 s, gates ≤ 1e-4) has an isolated single-layer write of 0.81 at L22 (identity) and 0.65 at L20 (color). Qwen2.5-1.5B has 0.81 at L23 (E17). Both have necessity-clean, write-concentrated stores: written once, committed late (§6.1b).
>
> **TODO [W]:** relabel or annotate `evidence/ar-certificates/` so its 30B entry is marked in-forward-only.

### 6.1b Written once through the residual, committed late

Rule 6 says writes go through the residual. E16 does exactly that for every panel cell and for Mamba (`saturn/experiments/2026-09-30-full-layer-sweeps/FINDINGS-E16-residual-writes.md`; Mamba, Amendment R of the sweep record).
- **Transformers:** in the filler prompt, the residual entering block L at the subject position is replaced with the clean subject's.
- **Mamba:** the (target − base) block-output residual at layer ℓ is added at the carrier.

Each job ran in 24–42 s. The no-op checks are ≤ 4e-5 (transformers) and ≤ 2.5e-4 (Mamba, batch noise in the vocabulary head).

**Formation window.** One residual write authors the target from any layer up to the late writer, and fails right after it:

| cell | residual write still ≈ full at | after | formed-store writes at those layers |
|---|---|---|---|
| SmolLM2 identity | L19 | L20 0.78 → L23 0.07 | L19 0.99 |
| Qwen2.5-0.5B identity | L20 | L21 0.70, L22 0.04 | L20–21 0.67 / 0.75 |
| Qwen2.5-1.5B identity | L22 | L24 0.57 → L27 0.37 | L23 0.81, L27 0.37 |
| Pythia-410M s16000 identity | L17 | L18 0.48 → L22 0.01 | L17 0.71 |
| Gemma-2-2B identity | L16 | L17 0.90, L21 0.64, L23 0.36, L25 0.13 | L16 0.39, L18 0.53, L20 0.66, L22 0.81 (sliding-window); L17 −0.06, L21 −0.07 (global) |
| Mamba-130M identity | L19 output | L20 output 0.00 | L20 0.70 |
| Mamba-370M identity | L34 | L35 0.56, L39 0.16, L40 0.01 | L35 0.38, L39 0.39, L40 0.15 |
| Mamba-2.8B identity | L42 | L43 0.86, L44 0.22, L47 0.01 | L43 0.12, L44 0.60, L45 0.10, L47 0.11 |
| Mamba-2.8B counting | L38 | L39 0.81, L41 0.69, L44 0.01 | L39 0.13, L41 0.14, L44 0.67 |

**A commit ledger.** The residual write at ℓ equals the sum of the single-layer formed-store writes at the layers still downstream.
- **Mamba conserves to within 0.02–0.15.** Pearson r = 0.998–1.000 over the late half, and the per-layer state writes sum to 0.94–1.09.
- **Transformers match the shape but not the magnitude.** r = 0.95–1.00 over the late half, but the per-layer writes sum to 0.99–2.96.

**E17 isolated the transformer write and ruled out the leak as the cause of the overshoot.** In E17 the filler prefix runs through the subject, the subject's cached K/V at layer L is overwritten with the clean subject's, and only the suffix runs, so nothing leaks into the subject's own residual (`saturn/experiments/2026-09-30-full-layer-sweeps/FINDINGS-E17-isolated-kv-writes.md`; 5 jobs, 10 cells, no-op ≤ 4e-5).
- **The joint write is exact.** Isolated write at all layers = residual write at L0 = 1.000 in every cell. In a transformer the subject reaches later tokens only through its K/V.
- **The leak was real, but only in Qwen2.5-1.5B's early layers.** Its in-forward "L0 0.985" becomes 0.009 (identity) and 0.086 (color) under isolation, and its best single layer moves to L23 (0.81 / 0.75). In every other cell the isolated and in-forward per-layer values agree to 3 decimals.
- **The magnitude overshoot is not the leak.** The late-half ledger r is the same under isolation (0.95–1.00, within 0.005 of the in-forward arm), and Σ of isolated single-layer writes is still 0.99–2.96.
- **The overshoot is redundancy at the commit.** Adjacent late layers each nearly suffice alone, so their sum exceeds the joint write: Qwen2.5-0.5B identity L20 0.67 + L21 0.75; SmolLM2 identity L19 0.99 with L20–22 another 0.76.
- **Downstream of the commit layer the ledger is additive.** Max |R(ℓ) − Σ_{k≥ℓ} write(k)| is 0.001–0.15.

**Gemma-2-2B commits only on its sliding-window layers (MEASURED parity; meaning is inference).** Gemma-2 alternates sliding-window (even index) and global (odd index) attention. Every positive commit is on a sliding-window layer: L16, L18, L20 and L22, at 0.39–0.81 (identity) and 0.15–0.65 (color). The global layers between them write slightly *negative*: L17 −0.06 / −0.08 and L21 −0.07 / −0.03. On these 15-token prompts the 4096-token window covers the whole context, so the split is a difference in what the two layer types learned, not in what they can reach. It is the most redundant commit in the panel (Σ 2.96).

So Mamba commits through one clock-stopping layer and conserves exactly. Transformers commit redundantly over 1–3 adjacent late layers, and the sum saturates there.

**Relation to prior work on factual recall.** Three lines of work describe parts of this picture in transformers.

- **Causal tracing** [Meng 2022]. A noised run of a factual prompt is repaired by restoring the clean hidden state at one layer and position. The effect is strong at the last subject token in middle layers, and ROME then edits the mid-layer MLP there.
  - *Shared:* our residual write is the same class of intervention (we write into a filler prompt instead of a noised one), and the formation window is the causal-tracing curve.
  - *Different:* causal tracing measures single-site *sufficiency* and reads it as location. The other half of the certificate says otherwise. Isolated single-layer necessity shows that no single layer holds the store (≤ 0.08 in the cleanest cells), while a residual write succeeds from any layer up to the commit band. The tracing curve marks where a write *can* author the answer, not where the store *is*.
  - *Consequence:* this is a mechanism for the finding that causal-tracing localization does not predict which layer is best to edit [Hase 2023].
- **Dissecting recall** [Geva 2023]. Early MLPs enrich the last subject position, the relation propagates to the final token, and upper-layer attention heads extract the attribute from the enriched subject. They show this with attention-edge and sublayer knockouts.
  - *Shared:* our formation window corresponds to enrichment. Our late commit, with a read concentrated in one late head (E13), corresponds to extraction.
  - *Different:* we add
    - full single-layer sweeps under exact gates, which separate path-distributed necessity from the concentrated write;
    - the commit ledger;
    - the read replaced by an exact-row join (E12, E13, E18);
    - the commit confined to Gemma-2's sliding-window layers;
    - Mamba, where the committing layer is the one that stops its clock.
- **Deferred commitment** [Agarwal 2026], the closest prior result. Donor hidden states are patched every other layer in four 3–8B transformers. Entity information patched at the entity token transfers at 90–100% in early layers, while at the final token it becomes generation-controlling only late (88–97%).
  - *Shared:* this is our formation window and late commit, measured at the final token.
  - *Different:* their scope is sufficiency patching of hidden states, and they leave the routing from the entity position to the final token unlocalized. We add
    - necessity;
    - the isolated key/value cut;
    - every-layer sweeps;
    - the ledger, which localizes the commit to specific layers' keys and values (E16, E17);
    - the read site and its join (E13).

None of these works treats the diffusion case, where the time circuit is clean (§5), and none tests a feature-circuit instrument against such a store (§9, E6).

**Reading (inference).** In these language models the stored object is:
- *written once* through the residual;
- *formed* by the model;
- *committed* into the read store (K/V or recurrent state) over a short late band at ~0.7–0.9 of depth.

The answer then reads the committed store, and that read is distributed (§6.1 necessity). The "late writer" of the full sweeps is the largest commit. In Mamba, the committing layer is the one that stops its clock (§6.4).

This is the language-model form of the paper's time axis. The time is in the *formation and commit*, not in a necessity-distributed store.

> **TODO [W]:** reframe the abstract and §1 around "space circuits, time circuits (FLUX), and write-once/commit-late stores (LMs)".
>
> **TODO [W] (naming, low priority):** pick a name for the language-model structure (written once through the residual, formed by the model, committed late, read at the commit layer). Candidates:
> - "set-and-forget circuit" (the author's suggestion);
> - "write-once / commit-late store";
> - "commit circuit";
> - "deferred-commit circuit";
> - "latch circuit" (in Mamba the committing layer holds state by stopping its clock);
> - "time-formed store".

### 6.2 Robust to the ablation method

**Test.** We repeated the language-model test under zero, mean and resample ablation, as well as the original generic-filler replacement (`job-43479ccebd46`, `job-0e7f1e51394c`).

**Result.** In SmolLM2-1.7B and Qwen2.5-0.5B, every method:
- kept the L12 and L18 shares under 25% (SmolLM2 0.1–24.9%; Qwen 0.0–7.2%);
- removed *fox* from top-1 under whole-path ablation.

**The cut decides robustness.** Language-model whole-path ablation approximates deleting a token's stored state. FLUX block-output ablation is a mid-network patch inside a redundant region (§5.5). The robustness Miller et al. ask about depends on the cut.

E2b sampled L12 and L18 only. For Qwen2.5-0.5B, both sampled layers sit outside its L20–21 writer. The method-robustness of the late writers in §6.1 is untested.

### 6.3 Computed objects and free generation

**A computed object.** "The sum of three and five equals" yields " eight", which is not in the prompt.
- Ablating the operand carriers costs −5.41 nats, landing on the floor.
- The two *sampled* single layers carried ≤ 1.5%. The full sweep (E11, below) finds L17 at 0.35, so this figure is retracted.
- The "two and seven" trace authors " nine" at 0.979 (`job-3b014f386fb8`, private).

**E11, the full sweep (MEASURED; `job-e8180d6a5ab4`, SmolLM2-1.7B, 45 addition items).** The canary reproduces the −5.41 nats and the 0.979 authorship exactly. Gates are ≤ 5.2e-5. Record: `saturn/experiments/2026-09-30-full-layer-sweeps/FINDINGS-E11-computed-object.md`.
- **It is not a distributed certificate.** Isolated necessity concentrates at L17 (0.35 of the whole path, CI [0.31, 0.40]). The sampled "≤ 1.5%" missed it. It is a mixed cell with a late writer, like every other fully swept transformer cell.
- **It is written in two places at opposite depths.**
  - A residual write at the operand carriers installs the answer only early: full through L7, about 0.5 at L17, 0.04 by L23.
  - A residual write at the query token installs it only late: inert through L14, 0.86 at L18, 1.00 from L21.
  - The operand-to-sum step sits at L17–L18: necessity peaks at L17, and the carrier K/V commit and the query onset are both at L18.
- **The carrier ledger breaks before the commit.** At L9–L14 the carrier residual write is 0.58–0.65, while the downstream sum of isolated writes stays at 0.95–1.0. Inference: by then, the "and" and query positions have already read the filler operands.

So a computed object is not stored at a single carrier the way a recalled one is. Its operands are committed early, and the result is formed late at the position that will emit it.

**Free generation.** Single layers stay inert in every cell (≤ 0.04), while set cuts flip the continuation from the first token (`saturn/experiments/2026-08-21-multitoken-transport/`, private).

### 6.4 The certificate is about the cut, not the architecture

**Transformers.** Two transformers that certify at the key/value cut *lose their own certificates* at the hidden-state cut. When only the cut changes, single-site necessity moves from 1.0–1.5% to 172–236% of the whole-path effect (`job-13a15543fbb1`, `job-8e2d02c4a51e`, `job-0622676c3473`, `job-f11cab813f66`).

**Mamba's state cut.** Mamba carries its prompt as a per-layer pair: convolution state C_ℓ and recurrent state H_ℓ. Sealing and rehydrating that pair reproduces the native continuation 64/64 tokens with zero logit error [`saturn/experiments/2026-09-02-mamba-state-source-rosetta/FINDINGS.md`].

**E5 result (sampled layers).** At that cut, with single sites sampled at two layers, Mamba appeared to pass the certificate (record `saturn/experiments/2026-09-30-mamba-state-cut-certificate/FINDINGS.md`). The SmolLM2 parity canary was exact to four decimals, and the Mamba replay canary agreed within 6.1e-5.

**E3b result (full sweeps).** These overturn every sampled verdict (record `saturn/experiments/2026-09-30-mamba-full-layer-sweeps/FINDINGS.md`; jobs `job-7410ce4753a6`, `job-9ebdad137bb5`, `job-fb805c2515cc`).
- Per-layer variants were batched as rows of one forward pass and reproduced E5's independent values within 1e-4.
- Exact no-op and uninstall stayed at 0.

| model | behavior | whole-path necessity | sampled max single-site (E5) | full-sweep max single-site necessity / write (E3b) | whole-path write | verdict |
|---|---|--:|--:|---|--:|---|
| Mamba-2.8B (64 layers) | identity | −2.74 (fox→wolf) | 2.4% | **66.5% / 0.60 at L44** | 1.00 | not certified |
| Mamba-2.8B | counting | −1.15 (three→five) | 0.9% | **40.3% / 0.67 at L44** | 1.00 | not certified |
| Mamba-370M (48 layers) | identity | −1.79 | 1.0% | **66.6% / 0.39 at L39**; cluster L35 (write 0.38), L40 | 1.00 | not certified |
| Mamba-130M (24 layers) | identity | −3.62 | 9.1% | **81.3% / 0.70 at L20** | 1.00 | not certified |

**Same Mamba-2.8B, three cuts:**

| cut | result |
|---|---|
| state (C_ℓ, H_ℓ) | fails: one writer at L44 (full sweep) |
| conv1d carrier | fails: whole-trace write only 0.44 |
| hidden state | fails: L32 alone is 108.8% of the whole-path effect, reproducing the August measurement |

**Reading.**
- **Transformers.** The key/value cut certifies and the hidden cut does not. This stands on fully swept cells.
- **Mamba.** No cut yields the distributed four-quadrant certificate.
  - At the family-native state cut, the full trace still authors the answer (write 1.00), and second-half necessity is about equal to the whole.
  - But within that late block, a single layer at about 0.69–0.83 of the depth carries 40–81% of necessity and 0.39–0.70 of write sufficiency.
  - The concentration persists from 130M to 2.8B, so it is not a scale-floor effect within this range.
  - The two-layer samples (L12/L18, L24/L36, L32/L48) fell outside the writer in every case.
- **Scope.** Two-layer sampling produced the E5 "certificates". With full sweeps, Mamba looks like the transformer cells with late writers (§6.1): a necessary and sufficient whole path, plus one writer at 0.69–0.83 of the depth. Mamba differs in that *no* cell is necessity-clean, whereas three transformer cells are. Mamba's state is also path-formed by a separate test (below).
- **Retraction.** We retract the E5 claim that Mamba certifies at the state cut. "Mamba does not certify" is correct at every cut tested.

**The Mamba late writer is the layer that stops its clock.** We measured each layer's retention over the suffix, from subject to readout, on the same checkpoints (`saturn/experiments/2026-09-30-mamba-writer-clock/FINDINGS.md`; jobs `job-c115d4cdb811`, `job-92c7e677d9db`, `job-a90710f84b0d`; recompute canary ≤ 2.9e-5). Retention is exp(A·Σ_suffix Δ).
- The writer layer is a retention outlier in every cell. Its surviving-state fraction ranks 3/24, 2/48, 1/64 and 1/64 (z up to +4.3).
- Its selective timestep nearly freezes over the suffix: elapsed clock 0.03–0.07, against 1–8 for its neighbors and the final layers.
- Retention, not write magnitude, tracks the single-layer write (Spearman up to 0.85). Raw ‖ΔH_ℓ‖ anti-correlates.

So the writer *holds* the subject state until the readout. This is the Black Mamba "local clock hold" (m = 0 ⇒ identity transition) [`obsidian/blog/2026-09-18-214117-black-mamba-memories-with-their-own-time.md`] realized at one depth of a stock model. One prompt and one seed per cell. Black Mamba's own "local 24/24 vs global 0/24" is an arm comparison on a layerless organism, not a per-layer clock result.
>
> **TODO [E14] (optional):** a hybrid (attention + SSM) model, to test whether the attention layers carry a distributed store while the SSM layers concentrate.

**Path dependence in Mamba, by a separate test.** Ordered recurrent transitions compose spatial relations that endpoint states cannot:
- cached, staged and reversed-order transitions pass 3/3 on native-competent targets;
- adding the endpoint states passes 0/3 (`job-86dd44afaf69`; replicated in `job-ce9ce61407e0` and `job-76199bb99a65`).

This is evidence that state is path-formed. It is not a four-quadrant certificate.

### 6.5 Scale floor and developmental onset

**Pythia.**
- In Pythia-70M (six layers), capable checkpoints concentrate 79–81% of whole-path necessity in one layer: a space circuit.
- In Pythia-410M (24 layers), the earlier sampled reading was that a distributed signature arrives with capability and sharpens with training (`job-073398d3ef7b`). **The full sweep reverses this.** Between step 4000 and step 16000, a late writer *forms and sharpens*:
  - it moves from L16 to L17;
  - its necessity share rises from 0.318 to 0.507;
  - its single-layer write rises from 0.305 to 0.712.

  Training concentrates the effect into a late writer rather than spreading it.

**GPT-2 small.** 20 sparse-autoencoder features at one layer remove the whole effect [pointwise §4.4].

**Mamba.** Mamba is not a floor case. All three sizes, from 24 to 64 layers, concentrate in one late writer (§6.4).

**A recurring late writer.** Across families, the writer sits at a similar relative depth:

| model | writer layer | relative depth |
|---|---|---|
| SmolLM2-1.7B | L19 | 0.79 |
| Qwen2.5-0.5B | L20–21 | 0.83–0.88 |
| Pythia-410M | L17 | 0.71 |
| Mamba-130M | L20 | 0.83 |
| Mamba-370M | L39 | 0.81 |
| Mamba-2.8B | L44 | 0.69 |

No attention model up to 2.6B avoids the writer: Qwen2.5-1.5B and Gemma-2-2B are necessity-clean but write-concentrated (§6.1, E15). Whether larger models do is open (Qwen3-30B fails isolation, §6.1). This is an observation, not a scale law.

> **TODO [W]:** decide whether the late writer is the "final boss" in its original sense: a late store that smaller circuits write into. The 2026-08-21 posts argued for a role rather than a layer, and E13 tests whether the writer layer is where the answer *reads*.



### 6.6 Joint key/value transport across positions

**Qwen2.5-Coder-7B** (`job-a12ed4b56846`, n = 4). A natural PROGRAM prefix forms a task state that creates a persistent key/value corridor.

| arm | executes the program |
|---|---|
| write joint keys + values into a task-free recipient | 4/4 |
| write keys only | 0/4 |
| write values only | 0/4 |
| remove the corridor | 0/4 (execution abolished) |

The receipt itself records "terminal claim: false".

**Qwen2.5-Coder-1.5B.** Swapping layers 13–27 of the in-flight key/value state exchanges a passing future and a failing future exactly, over 122 tokens (`job-86b12ab70e83`, one task).

**Row permutation.** Tolerance to row permutation is expected, not a finding: attention is invariant to a joint permutation of source rows, softmax(Q(PK)ᵀ)PV = softmax(QKᵀ)V.

> **TODO [W]:** relate this to in-context task vectors [Hendel 2023] and function vectors [Todd 2024], and state what joint key/value carriage adds.

### 6.7 Chain-of-thought scratchpad state (limited)

Swapping the scratchpad token's keys and values flips the answer in four families:

| model | scratchpad swap | input-carrier swap |
|---|---|---|
| SmolLM | 8.02 | 1.82 |
| Qwen-0.5B | 9.23 | 0.88 |
| Qwen3-8B | 14.18 | 0.53 |
| Qwen3-30B | 11.59 | 1.64 |

(`saturn/experiments/2026-08-21-ird-fruit-battery/`, private.)

**Caveat.** The design uses one prompt pair per family, and the swapped token is the answer the scratchpad already states. This measures copying, not causal use of intermediate steps.

**Model virtual memory now supports this test.** The page swap / unmount / remount recipe runs on Qwen2.5-0.5B with exact page restore (`saturn/experiments/2026-09-30-mvm-mamba-cot/FINDINGS.md`, `job-8fa1e41f6adb`). On a tiny panel it discriminates the two cases:
- unmounting a *copied* value flips the answer (necessity 0.84);
- a *non-copied* intermediate arithmetic step is not used measurably (−0.015).

That is copying, not computation, for these items.

> **TODO [E10]:** an intermediate-step swap with ≥ 20 items, against truncation and mistake-insertion baselines [Lanham 2023]. Run it through model virtual memory (`saturn.model_os.CausalContextVM`) as page-level swap, unmount and remount of scratchpad pages, with exact no-op and uninstall gates. The Prefill(A‖B) ≠ Mount(…) check (§8) is the coherence control. This needs the MVM integration logged in `saturn/request.jsonl` (`mvm-model-os-vm-cli-cot-mamba`).

### 6.8 The read side: can an address replace the selection? (open)

**Why this section exists.** A time circuit says *what* the consumer reads and *where* that state was built. It does not say *why* the consumer's attention selects those rows. The program's working answer is the **source-boundary placement** thesis [`obsidian/blog/2026-09-25-153244-connecting-the-dots-from-saturn-to-the-field.md`, an inference note]:
- selection over a source table is an addressing operation: a spectral bucket narrows the candidates, and an exact identity key owns the choice;
- the model keeps its graded query and its graded payload.

**The thesis assembles three earlier pieces:**
- Thott's clock × address × residual decomposition of the key, with the address plane readable after RoPE de-rotation and the residual load-bearing (`job-080c3550be62`, §3);
- the Spectral Address ABI and Model-MMU contract (`saturn/docs/SPECTRAL-ADDRESS-ABI.md`);
- model virtual memory (§8, Prefill ≠ Mount).

**Measured test: an exact join inside a certified circuit.** On the Qwen source-routing circuit (§7.1, parent `job-ec1ab31d35f2`; this test `job-a05238ace419`; record `saturn/experiments/2026-09-25-ar-exact-join-admission/FINDINGS.md`):
- every query→source attention edge was cut;
- the top 32–64 heads were then allowed to read only the single row an exact key join selects, with the native values doing the rest.

**Results (forced choice over the alphabet):**
- Qwen2.5-0.5B recovers to 0.995–1.000 at lengths 12–256, matching the intact model.
- Qwen3-0.6B-Base recovers to 0.906–0.995, missing the preregistered bar.
- Shuffled and off-by-one rows give chance.
- The model's own contextual keys, used as join keys, fail in both models (P4). Row-unique-correct keys collapse with depth (Qwen2.5 at length 12: 192 of 192 at L0, 9 at L12, 7 at L24).

**What is not established** (the program's own same-day audit) [`HANDOFF.md`]:
- **Dose.** The selected heads natively put only 0.22–0.40 of their attention on the source row, so the one-hot read amplifies the answer row about 3×. "Exact beats soft" may be amplification.
- **Metric.** Scoring was forced choice, not full-vocabulary top-1.
- **Key finding.** Token keys were unique by construction, so the join was equivalent to the oracle and the key-finding step was never tested.

**The fully assembled stack.** A test that combined Thott custody, a spectral bucket, an exact typed key and a native Qwen consumer was mechanically valid, but behaviorally null:
- exact typed pages generated the held continuation 0/4;
- the record states "terminal claim: none" (`job-3e5b1ba855f9`; `saturn/experiments/2026-09-24-thott-spectral-causal-context/FINDINGS.md`).

**Oracle-row audit (E12).** The audit with matched dose and full-vocabulary scoring ran 192 rows per panel (`job-45eeccc382c6`, `job-5af831962de9`, `job-954d59cce4bb`).
- **Qwen2.5-0.5B, native dose.** An exact-row read at the native dose matches clean: top-1 0.83–1.0, lengths 12–256.
- **Repeated-cue panel (ambiguous keys).** A full-weight read of the exact latest row *beats the intact model*: Qwen3 top-1 0.25 → 0.44 and 0.13 → 0.39; Qwen2.5 smoke 0.31 → 0.75. The native-dose read gives about 0.
- The address there is rule-given.

**The read of a time-circuit store (E13).** We applied cut-and-join to the answer's read of the subject's key/value trace (`saturn/experiments/2026-09-30-e13-time-circuit-read-join/FINDINGS.md`; `job-4213d6716e81`, `job-d7df964836db`; follow-ups `job-f31d32367efc`, `job-3257c7538bff`).
- **The read is not itself a time circuit.**
  - Cutting the answer's attention to the subject is inert at every single layer (≤ 0.074 Qwen2.5-1.5B, ≤ 0.22 SmolLM2), yet the whole cut kills the answer.
  - Restoring the read at **one late layer** suffices: L23 in Qwen2.5-1.5B (1.22); L18–19 in SmolLM2 (0.82–1.11).
  - That is the same layer where the residual write's formation window closes (§6.1b).
- **The read can be replaced by a join.** A one-hot read of the exact subject row in the top-k reading heads reproduces the clean answer: Qwen top-8 full-vocab top-1 0.86; SmolLM2 color 1.00. Shuffled rows stay at chance.
- **Authorship.** Forcing a donor's subject row authors the donor's answer (Qwen +1.0 vs control 0; SmolLM2 at its concentration layer).
- **The bucket we built from the model's de-rotated L0 keys was degenerate** (cosine ≥ 0.9999 across positions), so the oracle row carried the join.

**Status.** The language-model picture is:
- written once through the residual;
- committed late (§6.1b);
- read at that late layer by a join on the exact row.

**A model-derived address (E12).** A model-derived address replaces the selection (`saturn/experiments/2026-09-30-e12-bucket-exact-address/FINDINGS.md`; `job-09432bae9699`, `job-b8db28ceb7d0`; additive `job-edbd0fad3c04`, `job-dd5884c9fa04`). The oracle canary reproduces the prior audit bit-for-bit.

How the address is computed:
- The de-rotated layer-0 key is standardized. This removes the shared, nearly collinear component that defeated E13's raw-cosine bucket.
- It is converted into phase words on a 16-bit integer ring.
- The bucket is the set of rows whose phase words match the cue's exactly. The parameters were chosen on the discovery split only.

Results:
- **Distinct tokens:** the bucket is a single row that contains the answer (1.00 at lengths 12–256, both checkpoints). The full-weight read equals the oracle. Keeping each head's native background and adding a modest read brings full-vocabulary top-1 to within 0.03 of the intact model.
- **Repeated cues:** the bucket narrows to the two cue occurrences, and an exact occurrence key owns identity. Full-vocabulary top-1:

  | model | bucket + exact key | random pick within bucket | heads' own soft read | intact model |
  |---|---|---|---|---|
  | Qwen2.5-0.5B | 0.69–0.78 | 0.31–0.36 | 0.12–0.25 | 0.06–0.16 |
  | Qwen3-0.6B | 0.31–0.47 | 0.11–0.20 | 0.03–0.06 | 0.08–0.22 |

- The model's contextual residual is not an exact key (0.20–0.26).

**Status.** For this certified circuit, attention's selection can be replaced by a join in two stages. A spectral bucket computed from the model's own keys narrows the candidates, and an exact key owns identity. On ambiguous keys, this beats the model's own read. This is a measured partial answer to *why attention reads where it does*.

**Scope:**
- synthetic induction;
- two ~0.5B checkpoints;
- one seed;
- the occurrence key is rule-given.

**E18: the bucket on time-circuit reads and natural text (MEASURED).** Record `saturn/experiments/2026-09-30-e18-bucket-join-time-reads/FINDINGS.md`; jobs `job-7000378e68c5` (Qwen2.5-1.5B), `job-65939d2b359a` (SmolLM2), `job-0b687da9088a` (Gemma-2-2B). The canary reproduces E13 bit-for-bit (second half 0.9227478; L23 0.0794).

*Standardization fixes E13's degenerate bucket on every cell.*
- The subject's standardized layer-0 phase word is unique: bucket size 1, the bucket equals the subject 1.00, held-out items included.
- A one-hot join on that bucket equals the oracle at the commit layer: Qwen2.5-1.5B L23 1.02 / top-1 0.88; over the commit band, SmolLM2 identity 0.96 and color 1.22.
- In every cell, the write's commit layer is the read's concentration layer.
- On Gemma, the forced join restores at the sliding-window commit layers (L22 1.30; L16 0.42; L18 0.39) and *hurts* at the global layers (L17 −0.17; L21 −0.42), matching the sliding-only commit (§6.1b).

*But this address presumes the selection.* The bucket is keyed to the subject's own key. The address the model could form from the query alone, by matching the predecessor's phase word, contains the subject row:
- 0.00 on identity, color and coreference;
- 1.00 only on natural *repetition* text, where a surface induction cue exists (natural-text panel: 9 repetition items, 7 coreference items).

So a time-circuit read is a join-replaceable one-hot read of the exact row. For an induction-like read the spectral bucket also explains *which* row; for a semantic read it does not, and the QK "why" stays open (§12).

> **TODO [E12]:** run the dose-matched, full-vocabulary exact-join audit (worker already built, never run) on Qwen2.5-0.5B and Qwen3-0.6B, with an ambiguous-key panel that forces instance or role keys to resolve. Expected cost is single-digit minutes per model (asserted from the E1 wall time).
> - **If it passes:** promote this subsection to a result: "the read is a join".
> - **If it fails:** retire the amplification reading and keep the QK "why" as an open problem in §12.
>
> **TODO [E13] (stretch):** apply the same cut-and-join to a *time-circuit* read, the SmolLM2 color cell or Qwen2.5-1.5B identity. This asks whether the consumer's selection of a path-constituted store is also join-replaceable.

## 7. Space circuits, and circuits that are both

### 7.1 Certified space circuits

**Pythia-70M induction writer.** At step 1000 the writer is the head pair {L3H1, L3H6}:
- clean accuracy is 89.4% on 320 held-out examples;
- cutting both heads' source edges gives 1.9% (chance 2.1%);
- head 1 alone leaves 75.0%, and head 6 alone 32.5%;
- a matched-cue cut keeps 92.8%;
- correct repair restores 93.8%, and wrong repair gives 2.8%;
- the pre-capability checkpoint (step 512) is inert.

A single-file CPU verifier reproduces it in under a minute [`research/bfl/docs/certified-semantic-circuits/verifier/verify_pythia_induction.py`].

**Qwen2.5-0.5B and Qwen3-0.6B source routing** (48-way relational induction, `job-ec1ab31d35f2`):
- 28/28 preregistered gates pass;
- source cut 0–1%;
- matched-cue cut > 91%;
- wrong donor ≤ 0.52%;
- exact repair.

It is the complete parent edge set (336 and 448 edges), with no compact envelope.

**Pythia date retrieval.** Date retrieval forms between steps 512 and 1000. Layer 3 carries 92% of the deletion effect at step 1000 and 76% by step 4000. At 410M the source moves to layer 11 [`obsidian/blog/2026-08-14-we-watched-a-capability-being-born.md`].

### 7.2 Same model, both kinds

**SmolLM2-1.7B: a concentrated writer inside a distributed path.**
- Subject identity is carried along the second half of the stack.
- But layer 19 alone carries 30.5% of necessity and 0.991 of write sufficiency, and every other layer stays below 5%.
- Color in the same model passes on necessity (§6.1).

So one model holds a distributed path and a space-like component on it.

**The same mix appears elsewhere.** Qwen2.5-0.5B identity (L20–21), Pythia-410M (L16→L17) and all three Mamba models (L20, L39, L44) show it: the whole path is necessary and sufficient, yet one late writer carries most of the effect (§§6.1, 6.4, 6.5). The two-layer samples fell outside the writer in every case. On the full-sweep evidence, a mixed path plus late writer is the common case in language models, and a clean time circuit is the exception.

**Qwen2.5-0.5B** has a certified space circuit (induction source routing) and a time-circuit identity cell.

> **TODO [R5]:** side-by-side four-quadrant figure from `job-ec1ab31d35f2` and the E3b sweep, plus a per-layer necessity/write profile for SmolLM2 identity and the three Mamba models.

**Pythia-70M: writer and relay.** The writer pair is a space circuit within its layer. The whole-model account also needs the upstream layer-2 relay that builds the induction keys.

**Writer and relay (E4, MEASURED; `job-19e98d8ac631`; record `saturn/experiments/2026-09-30-e4-pythia-recovered-loss/`).** Recovered-loss R was measured on the induction panel at step 1000, within layers 2–3, under mean and resample ablation. The canary reproduces §7.1 byte-exactly, and the no-op is exact.
- **The writer pair {L3H1, L3H6} is necessary but not sufficient.** Ablating it removes 0.74–0.81 of the recoverable loss, above all 20 size-matched random pairs. Keeping it alone recovers almost nothing (R 0.01–0.24; accuracy ≤ 9%).
- **The five-head set {L2H1, L2H7, L3H0, L3H1, L3H6} is necessary and sufficient.** R is 0.99–1.05 and N is 0.86–0.98, at the 95th–100th null percentile, and accuracy returns to about clean.
- **Necessity is concentrated in heads.**
  - The relay L2H1 alone carries 0.58–0.72.
  - The writer L3H6 carries 0.24–0.29.
  - L3H1 carries 0.06, and L2H7 and L3H0 carry about 0.

This is the space-circuit signature, against at most 0.15 per *layer* in the language-model stores (§6.1). Both ablation methods agree.

**E4b (MEASURED, `job-b69d8fc7654a`).** The minimal triple {L2H1, L3H1, L3H6} is necessary and sufficient on its own: R 0.92–1.05 and N 0.83–0.95, matching the five-head set within the CIs. L2H7 and L3H0 can be dropped. Sufficiency needs both writers and leans on L3H6: relay + L3H6 recovers 0.85–0.99; relay + L3H1 recovers only 0.44–0.78. So the space circuit is three heads: one relay and two writers.

## 8. Static infrastructure and dynamic circuits

A time circuit has two parts that behave differently across prompts.

| part | contents | across prompts and seeds |
|---|---|---|
| static | route order, writer roles, state boundaries, the native consumer, prompt-time keys and values | fixed |
| dynamic | which source rows, payload, signed coefficients, dose, spatial support, timing, the live query | changes per prompt |

**The skeleton holds while coordinates move** [`obsidian/blog/2026-08-26-151627-the-hypergraph-had-a-skeleton.md`; `obsidian/2026-08-29-003349-skeleton-ir-incremental-executor-proposal.md`]:
- the causal-profile cosine within an ontology is 0.9132, against 0.7344 across ontologies;
- the late `single.0:image` seam appears in 8/9 families;
- whole-state rescue at joint.2/3/4 gives 0.9440 mean RGB, against −0.1722 for a sham (`job-ce8c48e505c8`, `job-e70b2bff82cc`);
- route rankings are stable across seeds (Spearman 0.9516–0.9751) while payload cosine ranges from 0.32 to 0.86.

**Static keys and values, dynamic query.** In the SDXL scene compiler (`job-51aac02d9df3`) [`obsidian/blog/2026-09-01-231018-we-found-the-native-scene-compiler.md`]:
- the prompt's keys and values are byte-identical between denoising calls 0 and 14, while the live query drifts to cosine 0.84;
- installing the matched keys and values under the live query reproduces the native image exactly (α 1.0000, RGB MAE 0.0);
- keys alone reach 0.662, and values alone 0.718.

**Exact composition.** A four-factor cube (body × scene × gaze × color) reconstructs exactly under a Möbius decomposition (error 0.0) (`job-8d9a230b083d`, `job-f68e1365baae`, `job-755b73fca4f7`). Restoring the mediator:

| through | rescue |
|---|---|
| image stream | 83.07% |
| text stream | −1.84% |
| both streams | pixel-exact |

**Two parents.** The final image has two parents:

| restored | result |
|---|---|
| neither | 0.000 |
| register at step 2 only | 0.403 |
| program at step 3 only | 0.712 |
| both | 1.000, pixel-exact |

**The split is enforced in code.**
- An immutable `ExecutionSkeleton` carries no tensors and no execution authority (`saturn/src/saturn/execution_skeleton.py:790`).
- A `DynamicCircuitRecord` is evidence-only and pinned to a skeleton fingerprint (`dynamic_circuit.py:703`).

**Dynamic circuits that load onto the static route:**
- **Eye color.** The upstream program moves eye color about 0.887 targetward.
- **Eye geometry.** It reaches 0.931 and shares five to seven of eight consumer heads with color, while sharing only 10–15 of 64 source rows.
- **Object registers.** Fox and ball rows edit their own object at 13.7× and 9.6× selectivity. Value algebra turns a mug blue while the cat region barely moves (MAD 59.8 vs 1.9).
- **Character register.** A frozen register on the reference-slot bus reproduces native reference images byte-exactly, without training [`research/demos/jen-character-register.md`].
- **Spectral addresses.** They select an instance's contact side 6/6 using source states captured at `joint.3` across all four steps (`job-6386d22db7c1`). This is donor-assisted, not donor-free. Instance binding itself is not established (§11).

**Time-formed state cannot be assembled from parts formed independently.** Holding text and order fixed, key/value pages compiled together match the native next token on 6/6 panels, while pages compiled independently match 1/6 [`saturn/experiments/2026-09-25-book-index-two-source-coherence/FINDINGS.md`]. In general, Prefill(A‖B) ≠ Mount(Prefill(A), Prefill(B)). The stored state is a product of its causal path.

The address side of this split (why the consumer selects the rows it does) is treated in §6.8 and left open.

> **TODO [W]:** figure: the static skeleton with dynamic circuits as overlays.

## 9. Why standard instruments miss time circuits

**Blind-graded trial.** Six preregistered cases compared standard readouts with exact-replay verdicts, and a context-free grader judged each against the model's actual output [`research/papers/pointwise-instruments-miss-distributed-circuits/evidence/instrument-trial/`].
- In 4 of 4 main cases, the standard readout gave the wrong verdict and the exact-replay verdict matched.
- The reserve case also misreported. The honesty case was graded inconclusive and is reported verbatim.
- Case 1 is the FLUX single-step sweep. Its minimum donor progress, 0.2218, is above the 0.15 bar, so it reads "no necessary component" for the certified route.
- The standard-recipe arms are our own implementations.

**Sparse autoencoders.** Preregistered, on public tools: SAELens, `gpt2-small-res-jb`, and Gemma Scope `gemma-scope-2b-pt-res-canonical`.

| model and ablation | identity effect removed | color effect removed |
|---|---|---|
| Gemma-2-2B, top-20 features at the best single layer | 29% (20 random features: 0.5%) | — |
| Gemma-2-2B, subject-restricted ranking across all layers | 63% (random: 11%) | 90% (random: 35%) |

- In GPT-2 small, which is below the scale floor, one layer suffices.
- TransformerLens reproduces our implementation to within 1.5×10⁻⁴ nats [pointwise §4.4].

**Single-layer key/value patching** reports the store as absent. The best single layer gives .08 in Gemma-2-2B and Qwen2.5-1.5B, against .94 and .92 for the second half [pointwise §4.2].

**Causal tracing** [Meng 2022] makes the complementary error. It restores one site and reads success as location. A residual write succeeds anywhere in the formation window, so the trace points at a layer that is not, by itself, necessary (§6.1b).

**Attribution graphs** freeze attention and do not explain cross-position flow [Ameisen 2025]; QK tracing extends them to attention scores [Kamath 2025]. Time circuits at the key/value cut are cross-position, time-accumulated transport.

**A caution in the other direction.** A full single-layer sweep is itself a standard instrument, and here it was the one that caught the concentrated writers. Single-site tools are not wrong, only incomplete when sampled. The failure mode is reading "no single sampled site matters" as "no single site matters", or as "nothing matters".

**E6, circuit-tracer head-to-head (MEASURED).** We ran circuit-tracer [Hanna 2025], the open implementation of attribution graphs [Ameisen 2025], on Gemma-2-2B with the Gemma Scope transcoders [Lieberum 2024], on the same identity and color panel (`saturn/experiments/2026-09-30-circuit-tracer-head-to-head/FINDINGS.md`; `job-08262f0051a8` with attention frozen as default, `job-7bdea520e492` unfrozen; 20/20 items each).

*What the graph reports:*
- Replacement score 0.68–0.70: about 30% of influence goes through error nodes.
- The subject position carries 0.21–0.22 of feature influence, spread across layers (at most 0.18 for identity and 0.28 for color in any single layer).
- Its largest subject-position layer is L0 on 19/20 items. The commit band L16–L22, where the isolated K/V write lands (§6.1b), gets only 0.10–0.21.

*What its interventions do:*
- Zero-ablating the graph's own top-50 features costs −0.16 (identity) and −0.29 (color) in median Δlogprob, against about 0 for random features.
- No feature set flips the answer on any item, in either attention setting. That includes the graph's top-k at any position, the top-k at the subject, and all 509–827 subject-position features.
- With attention unfrozen, the ablations slightly *raise* the answer's logprob.

*What Saturn reports on the same panel:* cutting the subject's isolated K/V over the second half flips 0.83 (identity) and 0.84 (color) of items, while no single layer carries more than 0.15.

*Matched operator (MEASURED, `job-03225ce474d1`).* Here every active transcoder feature is set to its value on the filler prompt: Saturn's swap, in the instrument's own basis. The no-op gate is exact. The results:
- **Identity is invisible.** Swapping every feature at every position and layer (~18k) moves the answer at most 0.08 of the way to the filler, with at most 1/12 flips. The identity sits in the transcoders' error terms.
- **Color is partly visible, with the time-circuit shape:** single layers ≤ 0.12, second half 0.19–0.23, all layers 0.31–0.42. That is about a third of Saturn's 0.81 and 1.00.
- **The graph's own top features are not the store.** Swapping them moves the answer *away* from the filler (−0.02 to −0.19).

So, on its native operator and on the matched one alike, circuit-tracer does not find the store that a whole-state cut removes on 0.83–0.84 of items.

## 10. Consequences for editing and generation

Each of these follows from the carrier being built over time.

The same structure explains a known puzzle in language-model editing: the layer that causal tracing localizes is not the best layer to edit [Hase 2023]. In a write-once/commit-late store, any layer in the formation window can author the answer. What matters is installing the write before the commit band (§6.1b).

1. **Edits must be installed early.** A content-bound donor edit has 0.904–0.971 authority installed at the first cut, against 0.095–0.358 installed halfway through denoising (4/4). A hostile donor steers toward its own factor (0.926–0.953), shams stay near zero, and every branch rolls back exactly [`research/bfl/demos/real-hotpatch-cinema.md`].
2. **When a write lands selects what changes** (`job-eb10b3c02dc5`) [`research/demos/scene-editing.md`]:
   - installed late, a write turns the eyes violet and keeps the composition (P 0.069);
   - installed early, the same write moves the image while the eyes stay blue (0.577);
   - the program alone reaches 0.712, the register alone 0.404, and both together are exact.
3. **Moving an object is a space × time conjunction.**
   - Steps 0–1 perform the move. A late-only departure write gives 0.0006 [`saturn/experiments/2026-09-20-flux2-transport-temporal-carrier/FINDINGS.md`].
   - A reach decomposes into grip, route and departure patches whose union is clean 4/4. The action signal grows 8.0–21.9× from joint.0 to joint.4 [`saturn/experiments/2026-09-19-flux2-puppeteer-carrier-origin/FINDINGS.md`].
4. **Small early writes are amplified.**
   - Zeroing 18 scaffold rows (3.5%) at step 0 does about as much damage as swapping the whole prompt, and 80–89% of the damage enters at step 0 [`research/bfl/demos/empty-context-positional-scaffold.md`].
   - A 55,297-parameter patch at joint.2, step 0, repairs counting (three apples to five; held-out exact count 37% → 72%). Its collateral gate fails, with 48% of ordinary prompts disturbed: accumulation cuts both ways [`research/bfl/demos/recipient-native-capability-patch.md`].
5. **Scenes compile** (`job-5b20cdbb0f15`) [`research/demos/scene-generator.md`].
   - A prompt lowers to static keys and values installed across the run: 21/21 exact images across seven specimens and five diffusion families.
   - Complete installation gives MAE 0.0000, while partial installation fails.
6. **Writing through the carrier from another model.**
   - A foreign language model, bridged through per-symbol anchors, authors through the unchanged consumer at native parity (`job-0706b0497903`, public).
   - Held-out symbols are *read* (21/36 after correcting for template collapse) but not *authored* (sham level). An affine-ceiling argument explains why.

> **TODO [R6]:** commit and redact `research/demos/` before citing it.
>
> **TODO [W]:** one short paragraph on Room Studio as an applied pipeline: geometry decides, FLUX paints declared masks, and everything outside the masks is exact.

## 11. What failed, and what we retracted

**Retired or weakened claims.**
- A universal segment-level depth kernel is retired. What survives is "second-half-loaded, saturating".
- Kernel-weighted constructive editing is at sham level at 1.7B and family-dependent at 8B.

**Struck results.**
- A hallucination predictor was struck.
- An early-exit equivalence was a self-comparison.
- A damage ≈ necessity ordering was refuted in four families.

**Retracted.**
- A "crossed-pairing leak" was an oracle degeneracy.
- A fitted rank-16 "clock" controller: rank was confounded with dose and anchor count.
- A relation-synthesis claim (`scene.bind_relation` v3) was a donor-present paste. It was retracted the same day.

**Mixed or not established.**
- Per-carrier attribution is non-monotone in scale: it passes at ≤ 1.7B, fails at 8B and passes at 30B.
- Instance binding is not established. The old writer's target switch produced byte-identical writes 12/12, and changing instance IDs moved 0 pixels.
- A nonlinear interaction compiler lost to the additive baseline on held-out data (0.716 vs 0.735).
- The counting patch failed its collateral gate.
- August blind route discovery gave a trend without a certificate on Qwen2.5-0.5B. On FLUX it recovered three target edges, but only one survived a wrong-depth control.

**New in this draft.** Each comes from applying the certificate strictly:
- the SmolLM2 identity cell is not a clean time circuit (§7.2);
- every Mamba state-cut certificate (130M, 370M, 2.8B identity and counting) is retracted after full sweeps, each showing a single late writer (§6.4);
- Qwen2.5-0.5B identity and Pythia-410M identity show late writers under full sweeps, and the earlier "distributed signature sharpens with training" reading of Pythia is reversed (§§6.1, 6.5);
- the Qwen3-30B-A3B certificate does not survive the isolated swap (§6.1);
- a same-day misreading that FLUX necessity is interchange-only was itself corrected by E1c: the dp metric places the null image near 0, and deletion in fact removes the target (§5.5);
- the FLUX route is not unique (§5.4).

## 12. Limitations and open problems

- **Sample sizes.** The original language-model grid used at most four items per cell, readouts are single-token, and most diffusion results use two seeds.
- **Replication.** All work is from one lab, with no external replication. Several receipts are private; TODO [R6] and E3 reduce this.
- **Sampled cells.** Several cited cells still rest on two-layer samples: Qwen3-30B, the computed-object cell, and the E2b method panel. §§6.1 and 6.4 show that sampled verdicts can flip.
- **Minimality.** A certificate identifies a path-constituted mechanism at a cut, not a minimal or unique path. E1 shows the FLUX path is not unique.
- **Necessity.** FLUX whole-path deletion is non-specific (a random sham also nulls the image) and, at the input cut, equals removing the prompt. Interchange is the informative necessity operator (§5.5).
- **Region, not address.** We establish a causal *region*, not a depth- or position-specific *address*.
- **Why, not just what.** We explain what moved, where, and to which consumer, but not why attention attended there. The best candidate account is that selection is an address join (§6.8). It is measured only at forced-choice level, on one space circuit, and is confounded by dose. The model's own contextual keys fail as join keys.

> **TODO [E12]:** update this item after the dose-matched exact-join audit.

## 13. Related work

**Patching, tracing and editing.** Activation and path patching locate components by intervening at one site [Meng 2022; Wang 2022]. Best practice for the operator and the metric is set out in [Zhang & Nanda 2023; Heimersheim & Nanda 2024].
- Causal tracing [Meng 2022] and dissecting recall [Geva 2023] describe factual recall in transformers. §6.1b relates our formation window, commit and read to both, and to deferred commitment [Agarwal 2026].
- Causal-tracing localization does not predict where editing works [Hase 2023]. Our necessity sweeps supply one reason (§6.1b, §10).
- Self-repair [McGrath 2023; Rushing & Nanda 2024] is another way single-site ablation underestimates importance. It differs from a time circuit: in self-repair, downstream components compensate *in reaction to* an ablation, while in a time circuit the path itself is the store.
- Faithfulness scores depend on the ablation method [Miller 2024]. We therefore report interchange and deletion separately and gate both on exact replay.

**Circuit discovery.** Automated circuit discovery [Conmy 2023], sparse autoencoders and transcoders [Lieberum 2024], and attribution graphs [Ameisen 2025; Lindsey 2025] all rank sites or features. QK tracing extends attribution graphs to attention [Kamath 2025], and the circuit-tracer library releases them [Hanna 2025]. §9 runs circuit-tracer against a time-circuit store, under its native ablation and under a matched interchange.

**Distributed effects, 2026.** Two recent papers observe the distributed effect without naming a class of circuit.
- In-context task identity transfers 0% under single-position intervention at every layer of Llama-3.2-3B, but up to 96% under multi-position intervention [Cheng & Zhang 2026].
- Single-layer activation edits easily corrupt factual recall but rarely repair it [Bugaud 2026].

We add the certificate, the cut result, the full-sweep rule, the commit ledger, the diffusion carrier and the static/dynamic decomposition.

**Diffusion.** Related diffusion work includes:
- attention-based prompt editing [Hertz 2022];
- vital layers for editing in FLUX [Avrahami 2025];
- key/value-cache editing in diffusion transformers [Zhu 2025];
- padding tokens acting as registers in text-to-image models [Toker 2025].

These locate *where* an edit acts. §10 adds *when*.

**Task and function vectors.** In-context task vectors [Hendel 2023] and function vectors [Todd 2024] are compact carriers of a behavior read at one site. The time-circuit stores here are read at one site too (§6.8), but they are written along a path.

**Cross-model representation.** Relative representations [Moschella 2023] motivate our coordinate-free reading of the FLUX carrier (§5.3).

**Chain of thought.** Faithfulness has been measured by truncation and mistake insertion [Lanham 2023]. §6.7 adds page-level swaps of the scratchpad through model virtual memory.

## 14. Conclusion

There are two classes of circuit and one certificate to tell them apart.
- **Space circuits** are what the field's instruments find.
- **Time circuits** are built across steps or depth, and those instruments miss them by construction.

**What we certified.**
- A time-accumulated carrier in a production diffusion transformer.
- The same certificate shape in transformer language models at the key/value cut.

**What strict application changed.** Applying the certificate strictly sharpened every claim:
- the FLUX carrier is a redundant joint-region text stream, and its time-accumulation signature holds under both interchange and deletion;
- in language models, full sweeps found a late writer at ~0.7–0.9 of the depth in most cells, transformer and Mamba alike. The clean four-quadrant time circuit is established in diffusion. In language models it is so far only half-established, cell by cell.

So the space/time distinction is a property of a behavior at a cut, and the same model can hold both.

**The decomposition.** The static/dynamic decomposition turns the time circuit into an editing and compilation interface.

**What the instruments see.**
- On a space circuit (Pythia-70M induction), standard ablation finds three heads that are necessary and sufficient.
- On the time-circuit store in Gemma-2-2B, the attribution graph puts the subject's influence at L0 and in error nodes. No feature-level intervention it supports — ablation or matched interchange, at its top features or at every feature — converts the answer more than 0.08 of the way. A whole-state cut over the second half flips 83–84% of answers.

The class is real. It is the norm for stored objects in these models, and today's tools are built not to see it.

---

## References

- **[Agarwal 2026]** D. Agarwal. Relation Before Entity: Deferred Commitment in Language Model Factual Recall. ICML 2026 Mechanistic Interpretability Workshop. arXiv:2609.17537.
- **[Ameisen 2025]** E. Ameisen, J. Lindsey, et al. Circuit Tracing: Revealing Computational Graphs in Language Models. Transformer Circuits Thread, 2025. transformer-circuits.pub/2025/attribution-graphs/methods.html
- **[Avrahami 2025]** O. Avrahami, O. Patashnik, O. Fried, E. Nemchinov, K. Aberman, D. Lischinski, D. Cohen-Or. Stable Flow: Vital Layers for Training-Free Image Editing. CVPR 2025. arXiv:2411.14430.
- **[Bugaud 2026]** Z. Bugaud. Single-Layer Activation Edits Easily Corrupt Factual Recall but Rarely Repair It. Proceedings of the 6th Workshop on Trustworthy NLP (TrustNLP 2026), pp. 515–527.
- **[Cheng & Zhang 2026]** B. Cheng, J. Zhang. Single-Position Intervention Fails: Distributed Output Templates Drive In-Context Learning. arXiv:2605.04061, 2026.
- **[Conmy 2023]** A. Conmy, A. N. Mavor-Parker, A. Lynch, S. Heimersheim, A. Garriga-Alonso. Towards Automated Circuit Discovery for Mechanistic Interpretability. NeurIPS 2023. arXiv:2304.14997.
- **[Geva 2023]** M. Geva, J. Bastings, K. Filippova, A. Globerson. Dissecting Recall of Factual Associations in Auto-Regressive Language Models. EMNLP 2023. arXiv:2304.14767.
- **[Hanna 2025]** M. Hanna, M. Piotrowski, J. Lindsey, E. Ameisen. Circuit-Tracer: A New Library for Finding Feature Circuits. Proceedings of the 8th BlackboxNLP Workshop, 2025, pp. 239–249.
- **[Hase 2023]** P. Hase, M. Bansal, B. Kim, A. Ghandeharioun. Does Localization Inform Editing? Surprising Differences in Causality-Based Localization vs. Knowledge Editing in Language Models. NeurIPS 2023. arXiv:2301.04213.
- **[Heimersheim & Nanda 2024]** S. Heimersheim, N. Nanda. How to use and interpret activation patching. arXiv:2404.15255, 2024.
- **[Hendel 2023]** R. Hendel, M. Geva, A. Globerson. In-Context Learning Creates Task Vectors. Findings of EMNLP 2023. arXiv:2310.15916.
- **[Hertz 2022]** A. Hertz, R. Mokady, J. Tenenbaum, K. Aberman, Y. Pritch, D. Cohen-Or. Prompt-to-Prompt Image Editing with Cross Attention Control. arXiv:2208.01626, 2022.
- **[Kamath 2025]** H. Kamath, E. Ameisen, I. Kauvar, R. Luger, W. Gurnee, A. Pearce, S. Zimmerman, J. Batson, T. Conerly, C. Olah, J. Lindsey. Tracing Attention Computation Through Feature Interactions. Transformer Circuits Thread, 2025. transformer-circuits.pub/2025/attention-qk
- **[Lanham 2023]** T. Lanham et al. Measuring Faithfulness in Chain-of-Thought Reasoning. arXiv:2307.13702, 2023.
- **[Lieberum 2024]** T. Lieberum et al. Gemma Scope: Open Sparse Autoencoders Everywhere All At Once on Gemma 2. arXiv:2408.05147, 2024.
- **[Lindsey 2025]** J. Lindsey et al. On the Biology of a Large Language Model. Transformer Circuits Thread, 2025. transformer-circuits.pub/2025/attribution-graphs/biology.html
- **[McGrath 2023]** T. McGrath, M. Rahtz, J. Kramár, V. Mikulik, S. Legg. The Hydra Effect: Emergent Self-repair in Language Model Computations. arXiv:2307.15771, 2023.
- **[Meng 2022]** K. Meng, D. Bau, A. Andonian, Y. Belinkov. Locating and Editing Factual Associations in GPT. NeurIPS 2022. arXiv:2202.05262.
- **[Miller 2024]** J. Miller, B. Chughtai, W. Saunders. Transformer Circuit Faithfulness Metrics Are Not Robust. COLM 2024. arXiv:2407.08734.
- **[Moschella 2023]** L. Moschella, V. Maiorca, M. Fumero, A. Norelli, F. Locatello, E. Rodolà. Relative Representations Enable Zero-Shot Latent Space Communication. ICLR 2023. arXiv:2209.15430.
- **[Rushing & Nanda 2024]** C. Rushing, N. Nanda. Explorations of Self-Repair in Language Models. ICML 2024. arXiv:2402.15390.
- **[Todd 2024]** E. Todd, M. L. Li, A. S. Sharma, A. Mueller, B. C. Wallace, D. Bau. Function Vectors in Large Language Models. ICLR 2024. arXiv:2310.15213.
- **[Toker 2025]** M. Toker, I. Galil, H. Orgad, R. Gal, Y. Tewel, G. Chechik, Y. Belinkov. Padding Tone: A Mechanistic Analysis of Padding Tokens in T2I Models. NAACL 2025. arXiv:2501.06751.
- **[Wang 2022]** K. Wang, A. Variengien, A. Conmy, B. Shlegeris, J. Steinhardt. Interpretability in the Wild: a Circuit for Indirect Object Identification in GPT-2 small. ICLR 2023. arXiv:2211.00593.
- **[Zhang & Nanda 2023]** F. Zhang, N. Nanda. Towards Best Practices of Activation Patching in Language Models: Metrics and Methods. ICLR 2024. arXiv:2309.16042.
- **[Zhu 2025]** T. Zhu, S. Zhang, J. Shao, Y. Tang. KV-Edit: Training-Free Image Editing for Precise Background Preservation. ICCV 2025. arXiv:2502.17363.

**Models and tools.** Gemma 2 [arXiv:2408.00118]; Gemma Scope transcoders (`mwhanna/gemma-scope-transcoders`); Mamba [Gu & Dao, arXiv:2312.00752]; Pythia [Biderman et al., arXiv:2304.01373]; Qwen2.5 [arXiv:2412.15115]; SmolLM2 [arXiv:2502.02737]; FLUX.2 Klein (Black Forest Labs).

---

## Appendix A — Experiments

| ID | Experiment | Status | Record |
|---|---|---|---|
| E1 | FLUX off-route span sweep | **done** | `saturn/experiments/2026-09-30-flux2-offroute-span-sweep/` |
| E1b | Joint-region time accumulation and deletion | **done** | `saturn/experiments/2026-09-30-flux2-joint01-time-accumulation/` |
| E1c | Residual-state (true) deletion | **done**: deletion removes the target; dp artifact corrected | `saturn/experiments/2026-09-30-flux2-residual-deletion/` |
| E2b | Ablation-method sensitivity (LM + FLUX) | **done** | `saturn/experiments/2026-09-30-ablation-method-sensitivity/` |
| E3 | Isolated full sweeps + public AR bundle | **done** | `saturn/experiments/2026-09-30-isolated-swap-reruns/`; `evidence/ar-certificates/` |
| E3b-T | Full sweeps: Qwen2.5-0.5B, Qwen3-30B, Pythia-410M | **done**: late writers; 30B fails isolated | `saturn/experiments/2026-09-30-full-layer-sweeps/` |
| E17 | Isolated single-layer K/V write sweeps (additivity in transformers) | **done**: leak only in Qwen2.5-1.5B early layers; overshoot = redundant commit, additive after commit | `saturn/experiments/2026-09-30-full-layer-sweeps/FINDINGS-E17-isolated-kv-writes.md` |
| E15 | Full write sweeps: Qwen2.5-1.5B and Gemma-2-2B identity | **done**: write concentrated in both (Qwen L23 0.81; Gemma L22 0.81, color L20 0.65); no LM cell passes four quadrants | `saturn/experiments/2026-09-30-full-layer-sweeps/` |
| E16 | Residual-write sweeps, every panel cell + Mamba (rule 6) | **done** (incl. Gemma `job-ed4ce1ac5974`): formation window + Mamba commit ledger | same + `…-mamba-full-layer-sweeps/` |
| E3b-M | Full sweeps: Mamba-130M, 370M, 2.8B (identity + counting) | **done: none certified** (single late writer) | `saturn/experiments/2026-09-30-mamba-full-layer-sweeps/` |
| E5 | Mamba state-cut certificate | **done** (sampled; retracted by E3b-M) | `saturn/experiments/2026-09-30-mamba-state-cut-certificate/` |
| E6 | circuit-tracer head-to-head (Gemma-2-2B) | **done**: graph spreads subject influence (largest layer L0), ~30% error; no feature ablation flips the answer (0/20, attention frozen or not) vs K/V second-half cut flipping 0.83–0.84 | `saturn/experiments/2026-09-30-circuit-tracer-head-to-head/` |
| E4 | Pythia recovered-loss R (mean + resample) | **done**: writer necessary, not sufficient; five-head set necessary and sufficient (R ≈ 1.0); necessity concentrated in L2H1 and L3H6 | `saturn/experiments/2026-09-30-e4-pythia-recovered-loss/` |
| E7 | Multi-seed FLUX color necessity | **done**: 5/5 seeds; single step leaves the target, all-step interchange → source, deletion → null | `saturn/experiments/2026-09-30-e7-flux-color-multiseed/` |
| E8 | Klein 9B nine-gate certificate | optional | — |
| E9 | SDXL four-quadrant certificate | optional | — |
| E10 | CoT intermediate-step redesign | optional | — |
| E11 | Full sweep of the computed-object cell (§6.3) | **done**: mixed cell (necessity L17 0.35); operands written early at carriers (≤L7), sum written late at query (L18→L21) | `saturn/experiments/2026-09-30-full-layer-sweeps/FINDINGS-E11-computed-object.md` |
| E12 | Exact-join audit (dose, full vocab) + ambiguous keys + model-derived bucket address (§6.8) | **done: PASS**. Bucket from the model's own L0 phase words + exact key = oracle; within 0.03 of clean (additive); beats native on ambiguous keys | `saturn/experiments/2026-09-25-ar-exact-join-admission/`, `saturn/experiments/2026-09-30-e12-bucket-exact-address/` |
| E13 | Cut-and-join on a time-circuit read (§6.8) | **done**: read concentrated at the commit layer, join-replaceable; bucket degenerate | `saturn/experiments/2026-09-30-e13-time-circuit-read-join/` |
| E14 | Hybrid attention + SSM model full sweep (§6.4) | optional | — |
| E18 | Bucket + exact join on time-circuit reads (E13 cells at the commit layer) and on natural text (§6.8) | **done**: subject bucket fixes E13 (size 1; join = oracle at the commit layer; Gemma sliding layers yes, global layers no); a query-formed address finds the row only on repetition (1.00), not semantic reads (0.00) | `saturn/experiments/2026-09-30-e18-bucket-join-time-reads/` |

> **TODO [W]:** consolidate every harness into `saturn/experiments/2026-09-30-space-and-time-circuits/` (one tree, a top-level `run.py` and `canaries.json`) and cite it as the reproduction entry point.

## Appendix B — Corrections owed

| ID | Item |
|---|---|
| R1 | Timeline figure. |
| R2 | Confirm the SDXL clock results are independent of the retracted rank-16 controller. |
| R3 | Fix mis-citations inherited from the IRD and transaction drafts: the FLUX four-quadrant numbers are `job-7d53e47755f7` (case-1 ledger), not `job-6650205b45eb`; the 30B receipts are `job-7cc5b24954f0` and `job-ef8408d9c3d2`, not `job-38c1c37dd591` (a SmolLM2 smoke job); the scene-edit .9133 is in `research/bfl/demos/scene-circuit-certificate.md`, not `job-3cd13239dd91`. |
| R4 | Scale-floor wording after E3b. |
| R5 | Same-model figure and per-layer profiles. |
| R6 | Commit and redact `research/demos/`. |
| R7 | Locate or drop the measurement paper's unreceipted Pythia-70M single-layer claim. |
| R8 | The symbol-table read count is 21/36, not 35/54. |
| R9 | `ears_upright_folded` controls eyelid state. |
| R10 | ~~Interim Mamba sweep numbers~~: done, from `FINDINGS.md` and the report JSONs. |

## Appendix C — Source map

See [`outline.md`](outline.md), Appendix C, for the full source map: papers, BFL demos, research demos, dated obsidian posts, experiment records and code.
