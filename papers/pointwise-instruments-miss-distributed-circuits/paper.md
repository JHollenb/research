---
title: "Single-Site Tests Miss Distributed Stores"
type: research-paper
status: published
date: 2026-08-21
updated: 2026-10-05
tags: [interpretability, activation-patching, sparse-autoencoders, attribution-graphs, transcoders, causal-mediation, flux2, language-models, methods]
---

# Single-Site Tests Miss Distributed Stores

**Evidence from a diffusion transformer and five language models, a sparse-autoencoder comparison, and a blind-graded comparison of standard readouts against the model's own output**

Jacob Hollenbeck

*2026-08-21; revised 2026-09-22 and 2026-10-05*

> Every number in this paper is measured and traceable to a file in this folder.

---

## Abstract

Activation patching usually asks one site at a time whether a component is necessary or sufficient for a behavior. We show measured cases where that question gets the wrong answer because the information the output depends on is spread across steps or layers: no single site is necessary and no single site's slice is sufficient, while the whole path is both. In FLUX.2 Klein 4B, ablating any one of four route components at any one denoising step leaves at least 22% of an identity transition intact, while ablating the same four components at every step leaves 0.13% and inserting them carries 91%, on held-out seeds. In language models, replacing a subject token's cached keys and values at a single layer, with the subject token's own computation left untouched, removes at most 16% of the effect in GPT-2 small and 8–18% in Qwen2.5-1.5B and Gemma-2-2B, while replacing them across the second half of the layers removes 81–104% and flips the top answer in 83–95% of items. We then ran a standard sparse-autoencoder workflow (SAELens with public GPT-2 and Gemma Scope SAEs) on the same prompts. In Gemma-2-2B, ablating the 20 most-attributed SAE features at the best single layer removes 29% of the subject's effect, 57 times more than 20 random features but far from the whole effect; in GPT-2 small, which is below the scale where we see distributed storage, the same procedure removes all of it. Ranking features across all layers and positions removes more than the whole effect in GPT-2 (3–9×), but almost entirely by deleting features on the other prompt tokens, and 200 random features alone remove 3.3 times the effect. In Gemma-2-2B the SAE workflow does find the store once the ablation spans every layer: restricted to the subject token but ranked across all 26 layers, 200 features remove 63% of the identity effect and 90% of the color effect (random: 11% and 35%). The failure is the single-layer question, not the features. TransformerLens reproduces our implementation on GPT-2 to within 1.5×10⁻⁴ nats. The same pattern appears in the features an attribution graph selects: in Gemma-2-2B with public transcoders, 13 of 1,000 single graph features are individually necessary, while ablating a graph's top 20 jointly flips the answer on 15 of 50 preregistered prompts, including all 8 two-hop prompts (20 matched-random features: 5); where the tool's own intervention predictions miss, they mostly under-predict the real model. Finally, a preregistered, blind-graded comparison of four standard readouts against the model's own output gave the wrong verdict in 4 of 4 graded cases; those arms are our own implementations on cases chosen because we expected failures, so they show the failure modes exist, not how often they occur. All code, results and offline verifiers are included.

## 1. The problem

Causal-intervention methods in interpretability, from activation patching and path patching to causal tracing, typically localize a behavior by intervening on one site (a layer, head, position or step) at a time and measuring the change in output [1–4, 8]. A null at every site is often read as "this behavior has no localized mechanism here." That reading assumes the relevant information is concentrated enough that removing one piece hurts. If instead the output reads from a store that is written redundantly across many layers or steps, single-site ablation is compensated by the rest of the store and single-site insertion is too small to matter. Self-repair in language models, where later components compensate for an ablated one, is a known instance [5, 6], and best-practice guides already warn that patching granularity changes conclusions [3, 4]. Sparse-autoencoder workflows [9–13] inherit the same question: a feature ablated at one layer can be rewritten or bypassed elsewhere.

This paper contributes (i) measured examples of the pattern in a diffusion transformer and several language models, (ii) a test that separates it from "no mechanism," (iii) a preregistered comparison with a standard SAE workflow on the same prompts, and (iv) a blind-graded demonstration of four readouts that give confident wrong verdicts in the same regimes.

## 2. The four-quadrant test

For a behavior with a clean source and target condition, we run four interventions and judge each by the unchanged rest of the model, run to completion and reading out its own answer:

|  | one site | whole path |
|---|---|---|
| **necessity** (ablate in the target run) | behavior survives | behavior is removed |
| **sufficiency** (write into the source run) | little or no transfer | full transfer |

"Whole path" means the same component at every denoising step (diffusion) or the same token position's cached keys and values across a contiguous range of layers (language models). A localized mechanism passes at least one single-site quadrant; a behavior the model does not depend on fails the whole-path quadrants. The cross pattern is what redundant, distributed storage predicts.

Three points govern how the test should be read.

1. **The cut matters.** Replacing the subject token's residual stream at a single early layer removes the whole effect in every language model we tested (median 1.00 of the path effect at layer 0), because the residual stream carries everything downstream of it. The single-site nulls hold for per-layer key/value slices and per-step diffusion components, not for the residual stream.
2. **How the key/value swap is done matters.** If the swap is applied inside one forward pass, the subject token's own attention at that layer also reads the replaced entries, which changes the subject's residual stream from that layer onward, so a "single-layer" swap silently becomes a multi-layer one. We call this the *in-forward* swap. The *isolated* swap runs the prompt through the subject token normally, replaces the cached entries at the chosen layers, and then runs only the later tokens, so only later tokens' reads change. §4.3 shows the difference can be total. The isolated swap is the primary measurement in this paper.
3. **Whole-path ablation is close to deleting the token.** Replacing a token's keys and values at every layer is nearly the same as removing it from the context, so the informative result is the single-site failure and the size of the gap, not the whole-path success by itself.

## 3. Setup

**Diffusion.** FLUX.2 Klein 4B (revision `e7b7dc27f91deacad38e78976d1f2b499d76a294`), BF16, 256×256, 4 steps, guidance 1.0. The contrast is a fox → cat identity transition. The four components are the route sites `joint.2`, `joint.3`, `joint.4` and `single.0` identified in the companion paper [7]. Effects are the fraction of the source-to-target transition remaining (necessity) or carried (sufficiency), measured on the rendered image; held-out seeds 31337 and 60660 were not used to choose the sites.

**Language models, first measurements.** SmolLM2-1.7B, Qwen2.5-0.5B and Qwen3-8B, with one to three prompts per cell, in-forward swaps, BF16 or FP32 (§4.2).

**Language models, preregistered panel.** GPT-2 small, Gemma-2-2B, SmolLM2-1.7B, Qwen2.5-0.5B and Qwen2.5-1.5B, FP32, with the design frozen before any code was written ([preregistration](experiments/2026-09-22-sae-comparison/PREREGISTRATION.md)). Two behaviors with templated prompts: *identity* ("A photorealistic {animal} {pose} in {scene}. The animal in this picture is a" → the animal; 14 animals × 3 pose/scene contexts = 42 items, scored among the 14 animals) and *color* ("A {color} {object} on a {surface}. The color of the {object} is" → the color; 10 colors × 3 object/surface contexts = 30 items, scored among the 10 colors). The filler replaces the subject or color word with "creature" or "plain" at the same token position. An item is admitted only if the clean answer is top-1 among candidates and the filler prompt lowers its log-probability by at least 1 nat, which removes items where the scene already implies the answer; cells with fewer than 12 admitted items are reported but not used for decisions. Each item's whole-path effect is the change in answer log-probability (Δlp) when the subject's keys and values are replaced at every layer; every arm is reported as a fraction of that effect (median over items, 95% bootstrap interval), together with the rate at which the top answer changes. Every arm has a no-op control that installs the hook and changes nothing; all were exactly 0.0 in FP32 (isolated-split no-ops ≤ 1.4×10⁻⁴ nats, used as the baseline for isolated arms).

**SAE arms.** GPT-2 small uses `gpt2-small-res-jb` [11] (all 12 layers, `hook_resid_pre`); Gemma-2-2B uses Gemma Scope `gemma-scope-2b-pt-res-canonical`, width 16k [12] (all 26 layers, `hook_resid_post`), loaded through SAELens [10]. Features are ranked by attribution (activation × gradient of the answer log-probability [13]). *SAE-k* zeroes the top-k features at the subject position of one layer, keeping the SAE's reconstruction error so only the chosen features change. *SAE-global* zeroes the top-N features ranked over all layers and positions, propagating through the network; *SAE-global-subject* restricts the ranking to the subject position. Each has a random-feature control of the same size.

**Execution.** The diffusion experiments and the first language-model measurements used an exact-replay runtime: the unmodified computation is captured once, each intervention forks from that captured state, and a no-op fork must reproduce the parent exactly before any intervention is scored ([Appendix](appendix-execution-model.md)). The preregistered panel uses a standalone script on Hugging Face Transformers, SAELens and TransformerLens so it can be rerun without that runtime ([`run_sae_comparison.py`](experiments/2026-09-22-sae-comparison/run_sae_comparison.py)).

## 4. Results

### 4.1 FLUX.2: no single step is necessary; the route across steps is

A sweep of every single component at every single step, in both directions, leaves at least 22.2% of the identity transition in place when ablated, and inserting any one of them at one step leaves the fox a fox (Figure 1). By the usual reading, no component is necessary. Ablating the same four components across all steps leaves 0.13% of the transition, and inserting them across all steps carries 91.1%, on both held-out seeds, with exact no-op gates.

![Figure 1. Single-component, single-step interventions at step 2 in FLUX.2 Klein 4B. Top-left: fox source and cat target. "sufficiency": inserting the cat-run state at one component into the fox run leaves a fox. "necessity": ablating one component in the cat run leaves a cat. "rescue": restoring one downstream edge after an upstream ablation also leaves a cat. Every single-site, single-step arm reads as "no effect." The same components across all steps remove (0.13% remaining) or carry (91.1%) the transition.](figures/fig1-single-step-patching.png)

### 4.2 Language models, first measurements (in-forward swaps)

| model, behavior | clean answer | one layer (L12 / L18) Δlp | first half Δlp | second half Δlp → top answer | all layers Δlp → top answer |
|---|---|---:|---:|---:|---:|
| SmolLM2-1.7B, identity | fox | +0.03 / +0.40 | +0.36 | −2.09 → wolf | −2.09 → wolf |
| SmolLM2-1.7B, color | red | +0.02 / −0.04 | −0.13 | −1.20 → white | −1.08 → white |
| Qwen2.5-0.5B, identity | fox | +0.18 / +0.23 | −0.71 | −3.39 → wolf | −3.09 → wolf |
| Qwen2.5-0.5B, color | red | −0.02 / −0.06 | −0.10 | −0.98 → white | −0.83 → white |
| SmolLM2-1.7B, action | sitting | −0.00 / −0.08 | −0.10 | −0.71 → sitting | −0.95 → sitting |

These swaps were made with hooks on the key and value projections inside a single forward pass, so they are in-forward swaps in the sense of §2. In-forward swaps overstate a single layer's reach, which makes the small single-layer effects here conservative. Sufficiency mirrors necessity: writing the source-to-target displacement into one layer's keys and values gives a normalized effect between −0.002 and 0.005, and into every layer's gives 1.01–1.31; a separate SmolLM2 identity run gives 0.01–0.11 and 1.06–1.09. Qwen3-8B identity and color cells were also run but are not counted: with the subject replaced by a generic word the model still predicts the answer (fox at a 1.44-logit margin; red within 0.03 nats), so no ablation could flip it. The preregistered panel's admission rule exists to exclude exactly this case.

### 4.3 Language models, preregistered panel

| model | behavior (admitted items) | best single layer, isolated | first half, isolated | second half, isolated (flip rate) | best single layer, in-forward |
|---|---|---:|---:|---:|---:|
| GPT-2 small (124M) | identity (39) | 0.16 [0.11, 0.23] at L10 | −0.01 | 0.99 [0.97, 1.00] (92%) | 0.18 at L10 |
| Qwen2.5-1.5B | identity (42) | 0.08 [0.06, 0.12] at L23 | −0.08 | 0.92 [0.89, 0.97] (90%) | **0.99 at L0** |
| Qwen2.5-1.5B | color (22) | 0.18 [0.06, 0.23] at L23 | 0.29 | 1.04 [0.92, 1.24] (95%) | **0.97 at L0** |
| Gemma-2-2B | identity (42) | 0.08 [0.07, 0.08] at L22 | −0.04 | 0.94 [0.91, 0.98] (83%) | 0.08 at L22 |
| Gemma-2-2B | color (25) | 0.15 [0.13, 0.17] at L20 | 0.10 | 0.81 [0.70, 0.91] (84%) | 0.15 at L20 |
| SmolLM2-1.7B | identity (34) | not rerun | — | — | 0.39 at L19 |
| SmolLM2-1.7B | color (27) | not rerun | — | — | 0.09 at L18 |
| Qwen2.5-0.5B | identity (42) | not rerun | — | — | 0.35 at L20 |

Values are fractions of the whole-path effect (median, 95% bootstrap interval). With isolated swaps, the preregistered rule "the best single layer removes less than a quarter of the effect" holds in all five cells measured, while the second half of the layers removes 81–104% and flips the answer in 83–95% of items. In GPT-2 and Gemma-2-2B the in-forward and isolated swaps nearly agree (0.18 vs 0.16; 0.08 vs 0.08; 0.15 vs 0.15); Qwen2.5-1.5B is where they diverge.

The in-forward column shows why the distinction in §2 matters. In the first run, Qwen2.5-1.5B appeared to store the subject entirely at layer 0: swapping layer 0's keys and values in-forward removed 99% of the identity effect and 97% of the color effect. With the subject token's own computation left untouched, layer 0 removes 0.00 (identity) and 0.03 (color). The in-forward swap at layer 0 had changed the subject token's own hidden state through self-attention, which then propagated through every later layer. A single-site test with this implementation detail would have reported a sharply localized, early mechanism that does not exist. The SmolLM2-1.7B and Qwen2.5-0.5B identity cells, which exceeded the 0.25 threshold in-forward (0.39 and 0.35), were not rerun with isolated swaps, so we do not count them either way.

### 4.4 Sparse-autoencoder features

| model, behavior | SAE-20 at best single layer (flip) | 20 random features, same layer | SAE-global-subject N = 10 / 50 / 200 | random, subject position | SAE-global N = 10 / 50 / 200 | random, all positions |
|---|---|---|---|---|---|---|
| GPT-2, identity | 1.25 [0.87, 1.38] at L6 (77%) | 0.28 | 0.73 / 0.46 / 0.45 | 0.06 / 0.30 / 0.84 | 3.08 / 8.02 / 9.36 | 0.09 / 0.66 / 3.31 |
| Gemma-2-2B, identity | 0.29 [0.22, 0.33] at L17 (5%) | 0.005 | 0.21 / 0.39 / 0.63 | 0.00 / 0.01 / 0.11 | 2.15 / 4.45 / 6.51 | 0.00 / 0.00 / 0.01 |
| Gemma-2-2B, color | 0.52 [0.40, 0.65] at L17 (44%) | 0.51 | 0.34 / 0.80 / 0.90 | 0.00 / 0.08 / 0.35 | 1.81 / 3.13 / 4.43 | 0.00 / 0.01 / 0.04 |

Values are fractions of the whole-path key/value effect; values above 1 mean the ablation removed more answer log-probability than deleting the subject did.

**Single-layer SAE ablation.** In Gemma-2-2B the attribution step finds the right features: the top 20 at layer 17 remove 29% of the identity effect, against 0.5% for 20 random features at the same layer. But 29% is not the effect; the rest is carried elsewhere and the answer changes in only 5% of items. This is the SAE version of the single-layer null. For color the top-20 ablation reaches 0.52, nominally passing the preregistered "necessary component" threshold of 0.5, but 20 random features at the same layer reach 0.51, so the layer is sensitive to any perturbation and the pass is not evidence of a located mechanism. GPT-2 small behaves differently: 20 features at layer 6 remove the whole effect (1.25, flip 77%), specifically (random: 0.28). That matches the scale floor in §6: in small models the store is concentrated.

**Global SAE ablation.** Ranking features over every layer and position and ablating the top N removes 3–9 times the whole-path effect in GPT-2 and flips every answer, so by the preregistered rule it is "faithful." It is not locating the subject: of the 8,400 features selected across items at N = 200, 8,383 sit on neither the subject token nor the final position but on the rest of the prompt, and 200 random features remove 3.3 times the effect on their own. Restricted to the subject position, the global ranking removes 0.45–0.73 of the effect in GPT-2 against 0.06–0.84 for random subject-position features; the N = 200 random control exceeds the attributed set.

Gemma-2-2B differs in two ways. First, the global ranking is specific: random features at any N remove at most 4% of the effect, while the attributed ones remove 1.8–6.5 times it. It still does not isolate the subject — of the N = 200 selections, 14% (identity) and 9% (color) sit on the subject token, 30% and 28% on the final position and the rest on other tokens — and dropping the final position leaves most of the overshoot (identity 3.45 at N = 200), so the readout position alone does not explain it. Second, the subject-restricted ranking works: it removes 0.63 of the identity effect at N = 200 (flip 52%, random 0.11) and 0.80–0.90 of the color effect at N = 50–200 (flip 76–92%, random 0.08–0.35). That arm ablates the subject token's features at every layer at once, so it is a whole-path intervention expressed in SAE features. It agrees with the key/value result: the same features that remove 29% at one layer remove most of the effect when the ablation spans the layers. What misleads is the single-layer question, not the SAE.

**Steering.** Adding the clean prompt's top-20 attributed feature directions to the filler prompt at a single layer recovers a median 0.91 of the answer log-probability in GPT-2 (layer 10) and 0.20–0.29 in Gemma-2-2B (layers 0–1, first run); writing the clean keys and values into the filler prompt at every layer recovers 1.00 in both.

### 4.5 TransformerLens and cost

Running the same arms through TransformerLens (`HookedTransformer` / `HookedSAETransformer`, version 3.9.0, weights loaded without processing so logits match Hugging Face) reproduces our implementation on GPT-2 to within 4.6×10⁻⁵–5.5×10⁻⁵ nats for the residual and key/value arms and 1.5×10⁻⁴ for SAE-20 over the 504 identity item × layer cells (6.8×10⁻⁵ and 1.3×10⁻⁴ over the 360 color cells), and gives the same verdicts on both applicable decision rules. TransformerLens was not run on Gemma-2-2B or Qwen2.5-1.5B. For Gemma-2-2B we tried: the TransformerLens copy of the model in FP32 exceeded the memory of the 16 GB GPU (peak 15.1 GB before the process was stopped, even with our copy removed from the GPU first), so the Gemma numbers rest on our implementation alone.

On these short prompts (under 20 tokens), reusing a cached prefix instead of recomputing the whole prompt gave no speed-up: 0.31 ms vs 0.32 ms per intervention per item with Hugging Face, and 0.60 ms vs 1.24 ms with TransformerLens, whose key/value cache path was slower. The whole GPT-2 job, including every arm, both libraries and all bootstrap intervals, took 284 s on one RTX 4080; the Qwen2.5-1.5B job took 52 s. Prefix reuse pays off for long shared prefixes and diffusion trajectories (Appendix §2 and §4), not for prompts this short.

### 4.6 What the diffusion time axis does and does not show

Writing the target displacement at different subsets of the four FLUX steps and scoring pixel reproduction of the target render, early steps score far higher than late ones: step 0 alone 0.13, steps 0–1 0.37, all four 0.73, and steps 2–3 at double dose only 0.16 (lion, seed 7217; the other three seed/target cells are similar). That is a statement about reproducing the target image, not about identity. Figure 2 shows the difference: steps 0–1 still render a fox, while the late double-dose arm renders a recognizable lion in a different pose and coat, which pixel distance scores poorly. Early steps fix layout; late steps can still change what the animal is.

![Figure 2. Write schedule vs outcome for fox → lion in FLUX.2 Klein 4B (seed 7217). "Progress" is 1 − pixel MAD to the target render, normalized by source-to-target MAD. The late double-dose arm scores 0.16 but visibly renders a lion, so progress measures reproduction of the target image, not whether the identity changed.](figures/fig2-write-schedule.png)

### 4.7 The isolated swap, in one number

The single most important implementation detail is which swap you run. An *in-forward* key/value swap lets the subject token's own attention read the replaced entries, so a "single-layer" edit silently becomes multi-layer; the *isolated* swap (§2) replaces the cached entries after the subject has finished computing and then runs only later tokens. The two can disagree completely: in Qwen2.5-1.5B identity, swapping layer 0's keys and values in-forward removes **0.99** of the effect, while the same swap done in isolation removes **0.00** (§4.3). A single-site test with the in-forward implementation would report a sharply localized early mechanism that does not exist. The first run of our own preregistered panel used in-forward swaps; the error was found in code review and rerun under a dated amendment, and both runs are kept.

### 4.8 The certificate is about a cut, not an architecture

Whether the distributed signature appears depends on the *transport cut*, not on the model family. The theory companion runs a control that moves only the cut: single-site necessity at the key/value cut is **1.0–1.5%** of the path effect (the distributed signature), and moving the cut to the residual (hidden) stream sends the *same two transformers' single-site necessity to **172–236%***, because the residual stream carries everything downstream of the cut, so one early residual cut is near-maximally necessary (§2, point 1). A state-space (Mamba-family) model likewise fails to certify at a residual-stream cut. Reading a residual-cut null as "this architecture lacks the mechanism" is therefore a cut artifact; the distributed store is addressed by the key/value cache, and the certificate is a statement about a cut, not an architecture. These two sharpenings are developed in the theory companion [16].

### 4.9 Attribution graphs: the single-versus-group question at the feature level

Attribution graphs built on transcoders [23, 24] are now a standard way to read a feature circuit off one prompt, and the tooling also predicts what an intervention on that circuit will do. The prediction is computed in a *replacement model* (transcoder reconstructions, attention patterns frozen at their clean values by default, transcoder error held fixed), not in the model itself. We asked the four-quadrant question of the graph's own features, judged by the real model.

**Setup.** Gemma-2-2B with the Gemma Scope per-layer transcoders; circuit-tracer [25] builds the graph (BF16) and ranks feature nodes by influence on the answer. A panel of 56 prompts in 7 task families (capitals, two-hop factual recall, antonyms, translation, acronyms, arithmetic sequences, category/rhyme) was preregistered and hash-committed before the first job; a prompt was admitted only if the native FP32 greedy answer equalled the target (50 admitted; 6 dropped and recorded, not replaced). Each of the top 20 features, and the 20 jointly, was re-run as an intervention on the native weights at the transcoder's write site, scored by the change in the answer's log-probability under the rule fixed in advance (≥ 0.5 nats necessary, ≤ 0.1 nats absent). A matched-random control drew 20 other active features from the same prompt with the same layer, position and activation band.

**One feature versus the group.** Of 1,000 single-feature ablations, 13 (1.3%) were individually necessary, all on two-hop and translation prompts; in 84.6% [82.4, 86.8] the graph agreed, almost always that the effect is small. Ablating the same 20 features jointly flips the answer on 15 of 50 prompts, including all 8 two-hop prompts (drops of 2.4–12.2 nats), against 5 of 50 for the matched-random set (mean drop 1.93 vs 0.09 nats). Widening the group to the top 100 features raises zero-ablation flips to 64% (random 8%), and steering the top 20 to −2× their activation flips 45 of 50 (random 20). This is the single-site pattern of §4.3–4.4 again, now in the features an attribution graph selects: the ranking finds the causal set, but almost no member of it is necessary alone.

**Which way the graph errs.** Where the graph's group predictions miss, they mostly *under*-predict the real model. The single zero-ablation inversion is a property of the default frozen-attention mode (the unconstrained mode predicts 0.17 nats against 1.53). On every two-hop prompt the native drop exceeds the graph's (e.g. 12.20 vs 5.21 nats), and across prompts the native drop exceeds the frozen-attention prediction by more than 0.4 nats on 11 of 50 for zero-ablation. Among circuit-tracer's three intervention modes, unconstrained propagation is the most accurate (mean absolute error 1.27 nats for zero-ablation, never over-predicting by more than 0.4) and the fully linearized direct-effects mode, in which graph edges are computed, the least (1.82). Transcoder error nodes carry 11–19% of node influence that no feature exposes.

**What this adds.** Graph-guided group interventions on real weights are strong and specific, so the graph's ranking is useful; single-feature verdicts and frozen-attention necessity predictions understate how much the model depends on the selected features, most on compositional prompts. A first run of this comparison read the tool's activation array in the wrong order and mis-dosed every native intervention; with the wrong doses the model looked robust and the graph looked over-confident. That was found by an independent reimplementation, fixed, and the whole panel rerun under the unchanged preregistration; two reimplementations agree on the corrected numbers. Summaries, both preregistrations and job ids are in [`experiments/2026-10-05-attribution-graphs/`](experiments/2026-10-05-attribution-graphs/README.md); the 50 sealed per-prompt bundles, which re-derive offline, and the correction note are public in the saturn-pub repository (`experiments/circuit_tracer/`).

## 5. Four readouts that give the wrong verdict

To make the practical consequence concrete, we preregistered six cases in which a common readout and the downstream model could disagree, ran both arms on matched inputs, and had a fresh grader with no project context compare anonymized readings against a frozen rubric. The success criterion, fixed in advance, was that the standard arm misreport in at least three of the four main cases.

| case | standard readout and its verdict | what the downstream model does | blind grade |
|---|---|---|---|
| 1. FLUX identity route | single-component, single-step patching sweep: "no necessary component" (≥ 22% of the transition survives every cell) | all-step ablation removes the transition (0.13% remains); all-step insertion carries it (91%) | misreport |
| 2. Foreign-encoder subject rows (FLUX) | nearest-class-mean probe, 16/16 correct on held-out native states: "no decodable content" (top-1 tiger, margin 0.035 vs floor 0.352) | transplanting the two subject rows into a native fox run renders a wolf on both seeds (Figure 3) | misreport |
| 3. Cross-model direction transfer (Qwen) | transferred difference-of-means direction, bit-identical to the original pipeline: 95.4% negative cosines, "representations differ across families" | native cosines are 0% negative in every model; the split falls to 0.0 under mean-centering alone | misreport |
| 4. Reconstruction cosine (FLUX) | cosine 0.993–0.997 on held-out prompts: "state recovered" | a content-free mean template scores the same; rendered, the reconstruction differs from native by pixel MAD 70–97 and shows the wrong animal for all four prompts | misreport |
| 5. Mediation across steps (control case) | single-step mediation: "holds at the measured step" | holds in 17/18 step × axis cells | inconclusive |
| 6. Zeroed answer logits (reserve) | "a zeroed logit is a maximal knockout" | all 76 zero records are at the final layer, where RMSNorm of a zero vector followed by a bias-free unembedding gives zero arithmetically | misreport |

The criterion was met: 4 of 4 main cases graded as misreports, 5 counting the reserve. Case 5 was included because we expected the standard reading to be correct there; the grader declined to decide the generality question, and we report that disagreement as it stands.

![Figure 3. Case 2. Left to right: native fox run; a run with a foreign text encoder, whose subject rows a validated probe reads as containing no animal; the same two subject rows transplanted into the native fox run, which then renders a wolf; the native wolf prompt for reference.](figures/fig3-probe-vs-consumer.png)

**How to read this table.** The standard arms are our own implementations of each recipe. TransformerLens does not load FLUX; nnsight and pyvene can hook a diffusion denoiser as a generic PyTorch module but were not used. We made each arm as strong as we could (case 2's probe was 16/16 on held-out native states; case 3's pipeline reproduced the original bit-for-bit), and a reviewer checked each arm before it ran. But the cases were chosen because we already suspected the readout would fail there, and the ground truth in each case comes from the downstream-model arm. The trial therefore shows that these failure modes occur in real models under faithful implementations; it does not estimate how often they occur. Case 2 is partly a distribution-shift failure: a probe trained on native states is applied to states produced by a different text encoder. The SAE comparison in §4.4, which uses public tools on public models, is the more direct test of a standard workflow.

## 6. What broke, and what this does not show

- **Scale floor.** In 70M-parameter Pythia checkpoints that can do the task, about 80% of the effect is carried by a single layer, and in GPT-2 small (124M) 20 SAE features at one layer remove the whole effect. The distributed pattern appears at or above roughly 400M parameters in our tests.
- **Cut dependence.** Residual-stream swaps at an early layer remove the whole effect in every model (§2). The pattern is a property of per-layer key/value and per-step diffusion interventions.
- **Implementation dependence.** In-forward and isolated key/value swaps can disagree completely (Qwen2.5-1.5B layer 0: 0.99 vs 0.00). The first run of our own preregistered experiment used in-forward swaps and a global SAE ablation that did not propagate between layers; both were found in code review after the first run, fixed, and rerun under a dated amendment. The first-run files are kept.
- **Our own attribution-graph run.** The first run of §4.9 read circuit-tracer's activation array in selection order rather than active-feature order and mis-dosed every native intervention on 44 of 50 prompts; it made the model look robust and the graph look over-confident. It was caught by an independent reimplementation, fixed with regression tests, and rerun in full under the unchanged preregistration. §4.9 rests on one model and one transcoder family.
- **No constructive recipe.** Weighting a write by the measured per-layer or per-step profile did not beat writing at the best single site in SmolLM2-1.7B, and only partly recovered at Qwen3-8B.
- **Token time.** Unlike depth and diffusion steps, the token axis did not accumulate: ablating the scene suffix moves about 1% of the subject effect.
- **Breadth.** One lab; single-token answers; two templated behaviors; five language models from 124M to 2.6B in the preregistered panel, of which three were rerun with isolated swaps; the TransformerLens cross-check covers GPT-2 only; one diffusion model. Color admitted too few items in GPT-2 (4) and Qwen2.5-0.5B (8) to count. No external replication.

## 7. Related work

Activation patching and causal tracing [1, 2] and path patching [8] are the tools this paper examines, and Zhang and Nanda [3] and Heimersheim and Nanda [4] show that conclusions depend on metric and granularity. McGrath et al. [5] document the Hydra effect, where later layers compensate for an ablated attention layer, and Rushing and Nanda [6] study self-repair more broadly; our single-layer nulls are consistent with these compensation effects and extend them to per-layer key/value caches and diffusion steps. Sparse autoencoders [9] and the public SAEs we use [11, 12], with SAELens [10] and TransformerLens [14], are the standard feature-level toolkit; sparse feature circuits [15] rank features across layers with attribution, and our SAE-global arm is a simplified version of that procedure. Attribution patching [13] supplies the ranking score. Transcoders [23] and the attribution graphs built on them [24], available through the circuit-tracer library [25], predict intervention effects in a replacement model; §4.9 checks those predictions against the native model. Our companion paper [7] identifies and certifies the FLUX.2 route used in §4.1, and the theory companion [16] gives the four-quadrant certificate and the transport-cut result folded into §4.8.

The delta from prior distributed-mechanism work is the isolated-versus-in-forward cut (§4.7), the full key/value and per-step sweeps that overturn sampled single-site certificates, and a standard SAE workflow run on public tools and models. Related findings report the same distribution without the single-vs-whole-path test: deferred relation-before-entity commitment across four decoder models [17], 0% single-position against up to 96% multi-position in-context transfer in LLaMA/Qwen/Gemma [18], and redundant, distributed, non-contiguous factual retrieval [19]; task and function vectors read a compact carrier at one site [20, 21]. On the diffusion side, DifFRACT trains timestep-conditioned transcoders on a FLUX diffusion transformer and intervenes across every denoising step [22], which is the feature-level analogue of our all-step quadrant.

## 8. Reproduce

```bash
# Four-quadrant receipts, render panes, and the first language-model table (offline, standard library)
cd evidence/four-quadrant-tests && python3 verify.py
# expect: 37/37 files hash-verified ... VERIFY OK

# Blind-graded readout comparison (offline, standard library)
cd evidence/instrument-trial && pip install . && instrument-trial-verify
# expect: RESULT: all hashes and all mechanical verdicts verified

# Preregistered panel and SAE comparison (GPU; about 1–8 minutes per model on an RTX 4080)
cd experiments/2026-09-22-sae-comparison && pip install -r requirements.txt
python run_sae_comparison.py --model gpt2 --device cuda --out-dir results --out-tag _v2 --tl
```

The attribution-graph comparison (§4.9) is summarized, with job ids and hashes, in [`experiments/2026-10-05-attribution-graphs/`](experiments/2026-10-05-attribution-graphs/README.md).

Every result file from the preregistered panel, first run and rerun, is in [`experiments/2026-09-22-sae-comparison/results/`](experiments/2026-09-22-sae-comparison/results/), with the environment, model commits and file hashes for each run.

The paper's central tables are also bound to their receipt bytes in a saturn-pub evidence claim registry at `../evidence-registry/` (append-only, hash-chained, standard-library only): `pim-prereg-panel-sae-v2` covers the §4.3 preregistered panel and the §4.4 SAE arms (the rerun `combined_summary_v2.json` in the results directory above). Re-check offline, without loading a model, with `saturn-pub evidence claims verify --check --registry papers/evidence-registry/claims.jsonl`, which re-hashes the receipt and flips the claim to `stale` on any drift.

## References

[1] K. Meng, D. Bau, A. Andonian, Y. Belinkov. Locating and Editing Factual Associations in GPT. arXiv:2202.05262, 2022.
[2] A. Geiger, H. Lu, T. Icard, C. Potts. Causal Abstractions of Neural Networks. NeurIPS 2021, arXiv:2106.02997.
[3] F. Zhang, N. Nanda. Towards Best Practices of Activation Patching in Language Models: Metrics and Methods. arXiv:2309.16042, 2023.
[4] S. Heimersheim, N. Nanda. How to use and interpret activation patching. arXiv:2404.15255, 2024.
[5] T. McGrath, M. Rahtz, J. Kramár, V. Mikulik, S. Legg. The Hydra Effect: Emergent Self-repair in Language Model Computations. arXiv:2307.15771, 2023.
[6] C. Rushing, N. Nanda. Explorations of Self-Repair in Language Models. arXiv:2402.15390, 2024.
[7] J. Hollenbeck. The Circuit That Survived Its Coordinates: Causal Evidence for Distributed Semantic Routes in a Production Diffusion Transformer. [bfl/docs/certified-semantic-circuits/paper.md](../../bfl/docs/certified-semantic-circuits/paper.md), 2026.
[8] K. Wang, A. Variengien, A. Conmy, B. Shlegeris, J. Steinhardt. Interpretability in the Wild: a Circuit for Indirect Object Identification in GPT-2 small. arXiv:2211.00593, 2022.
[9] H. Cunningham, A. Ewart, L. Riggs, R. Huben, L. Sharkey. Sparse Autoencoders Find Highly Interpretable Features in Language Models. arXiv:2309.08600, 2023.
[10] J. Bloom, C. Tigges, D. Chanin, and contributors. SAELens. https://github.com/jbloomAus/SAELens, 2024.
[11] J. Bloom. Open Source Sparse Autoencoders for all Residual Stream Layers of GPT2-Small (`gpt2-small-res-jb`). 2024.
[12] T. Lieberum, S. Rajamanoharan, A. Conmy, L. Smith, N. Sonnerat, V. Varma, J. Kramár, A. Dragan, R. Shah, N. Nanda. Gemma Scope: Open Sparse Autoencoders Everywhere All At Once on Gemma 2. arXiv:2408.05147, 2024.
[13] A. Syed, C. Rager, A. Conmy. Attribution Patching Outperforms Automated Circuit Discovery. arXiv:2310.10348, 2023.
[14] N. Nanda, J. Bloom, and contributors. TransformerLens. https://github.com/TransformerLensOrg/TransformerLens, 2022.
[15] S. Marks, C. Rager, E. J. Michaud, Y. Belinkov, D. Bau, A. Mueller. Sparse Feature Circuits: Discovering and Editing Interpretable Causal Graphs in Language Models. arXiv:2403.19647, 2024.
[16] J. Hollenbeck. Integral Residual Dynamics: Models Consume Trajectory Functionals, Not Sites. [../integral-residual-dynamics/paper.md](../integral-residual-dynamics/paper.md), 2026.
[17] D. Agarwal. Relation Before Entity: Deferred Commitment in Language Model Factual Recall. ICML 2026 Mechanistic Interpretability Workshop. arXiv:2609.17537.
[18] B. Cheng, J. Zhang. Single-Position Intervention Fails: Distributed Output Templates Drive In-Context Learning. arXiv:2605.04061, 2026.
[19] Hochman, H., Shapira, N., Goldberg, Y. Factual Retrieval in LLMs Is a Redundant, Distributed and Non-Contiguous Process. arXiv:2606.21345, 2026.
[20] R. Hendel, M. Geva, A. Globerson. In-Context Learning Creates Task Vectors. Findings of EMNLP 2023. arXiv:2310.15916.
[21] E. Todd, M. L. Li, A. S. Sharma, A. Mueller, B. C. Wallace, D. Bau. Function Vectors in Large Language Models. ICLR 2024. arXiv:2310.15213.
[22] A. Mazur, N. Konovalova, A. Alanov. DifFRACT: Diffusion Feature Reconstruction and Attribution for Circuit Tracing. arXiv:2606.15796, 2026.
[23] J. Dunefsky, P. Chlenski, N. Nanda. Transcoders Find Interpretable LLM Feature Circuits. NeurIPS 2024, arXiv:2406.11944.
[24] E. Ameisen, J. Lindsey, A. Pearce, W. Gurnee, N. L. Turner, B. Chen, C. Citro, et al. Circuit Tracing: Revealing Computational Graphs in Language Models. Transformer Circuits Thread, 2025.
[25] M. Hanna, M. Piotrowski, J. Lindsey, E. Ameisen. circuit-tracer: A New Library for Finding Feature Circuits. BlackboxNLP 2025.

## CHANGELOG

Attribution-graph extension (2026-10-05). No earlier measured number was altered.

- **§4.9 added — attribution graphs.** Preregistered 56-prompt panel on Gemma-2-2B with Gemma Scope transcoders and circuit-tracer: 13/1,000 single graph features necessary; top-20 joint ablation flips 15/50 (all 8 two-hop; matched-random 5/50); −2× steer 45/50 (random 20/50); top-100 ablation 64% (random 8%); the tool's intervention predictions mostly under-predict the native effect; unconstrained mode most accurate. Abstract, §6 (our own mis-dosed first run, caught and rerun) and §7 (refs [23]–[25]) updated.

Submission-readiness pass (2026-10-05). No measured number was altered.

- **§4.7 added — the isolated swap, in one number.** Crystallizes the in-forward-versus-isolated gotcha (Qwen2.5-1.5B layer 0: 0.99 vs 0.00) as its own short section, folded from the theory companion; §4.3 keeps the detailed treatment.
- **§4.8 added — the certificate is about a cut, not an architecture.** Folds in the transport-cut result from the theory companion: single-site necessity 1.0–1.5% at the key/value cut jumps to 172–236% at the residual-stream cut in the same transformers, so a residual-cut null is a cut artifact, not an architecture property.
- **Related work (§7)** now states the delta against prior distributed-mechanism work and adds references [16]–[22]: the IRD theory companion, Agarwal 2026 (deferred commitment), Cheng & Zhang 2026 (single vs multi-position), arXiv:2606.21345 (non-contiguous factual retrieval), Hendel 2023 and Todd 2024 (task/function vectors), and DifFRACT (timestep-conditioned transcoders on FLUX). The arXiv:2606.21345 title is a descriptive placeholder pending verification.
- The blind-trial framing (cases chosen because failure was expected; the four-readout result shows the failure modes exist, not how often) was already in the abstract and §5 and is unchanged.
