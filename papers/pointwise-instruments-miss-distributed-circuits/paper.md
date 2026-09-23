---
title: "Single-Site Tests Miss Distributed Stores"
type: research-paper
status: published
date: 2026-08-21
updated: 2026-09-22
tags: [interpretability, activation-patching, sparse-autoencoders, causal-mediation, flux2, language-models, methods]
---

# Single-Site Tests Miss Distributed Stores

**Evidence from a diffusion transformer and five language models, a sparse-autoencoder comparison, and a blind-graded comparison of standard readouts against the model's own output**

Jacob Hollenbeck

*2026-08-21; revised 2026-09-22*

> Every number in this paper is measured and traceable to a file in this folder.

---

## Abstract

Activation patching usually asks one site at a time whether a component is necessary or sufficient for a behavior. We show measured cases where that question gets the wrong answer because the information the output depends on is spread across steps or layers: no single site is necessary and no single site's slice is sufficient, while the whole path is both. In FLUX.2 Klein 4B, ablating any one of four route components at any one denoising step leaves at least 22% of an identity transition intact, while ablating the same four components at every step leaves 0.13% and inserting them carries 91%, on held-out seeds. In language models, replacing a subject token's cached keys and values at a single layer, with the subject token's own computation left untouched, removes at most 16% of the effect in GPT-2 small and 8–18% in Qwen2.5-1.5B and Gemma-2-2B, while replacing them across the second half of the layers removes 81–104% and flips the top answer in 83–95% of items. We then ran a standard sparse-autoencoder workflow (SAELens with public GPT-2 and Gemma Scope SAEs) on the same prompts. In Gemma-2-2B, ablating the 20 most-attributed SAE features at the best single layer removes 29% of the subject's effect, 57 times more than 20 random features but far from the whole effect; in GPT-2 small, which is below the scale where we see distributed storage, the same procedure removes all of it. Ranking features across all layers and positions removes more than the whole effect in GPT-2 (3–9×), but almost entirely by deleting features on the other prompt tokens, and 200 random features alone remove 3.3 times the effect. In Gemma-2-2B the SAE workflow does find the store once the ablation spans every layer: restricted to the subject token but ranked across all 26 layers, 200 features remove 63% of the identity effect and 90% of the color effect (random: 11% and 35%). The failure is the single-layer question, not the features. TransformerLens reproduces our implementation on GPT-2 to within 1.5×10⁻⁴ nats. Finally, a preregistered, blind-graded comparison of four standard readouts against the model's own output gave the wrong verdict in 4 of 4 graded cases; those arms are our own implementations on cases chosen because we expected failures, so they show the failure modes exist, not how often they occur. All code, results and offline verifiers are included.

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
- **No constructive recipe.** Weighting a write by the measured per-layer or per-step profile did not beat writing at the best single site in SmolLM2-1.7B, and only partly recovered at Qwen3-8B.
- **Token time.** Unlike depth and diffusion steps, the token axis did not accumulate: ablating the scene suffix moves about 1% of the subject effect.
- **Breadth.** One lab; single-token answers; two templated behaviors; five language models from 124M to 2.6B in the preregistered panel, of which three were rerun with isolated swaps; the TransformerLens cross-check covers GPT-2 only; one diffusion model. Color admitted too few items in GPT-2 (4) and Qwen2.5-0.5B (8) to count. No external replication.

## 7. Related work

Activation patching and causal tracing [1, 2] and path patching [8] are the tools this paper examines, and Zhang and Nanda [3] and Heimersheim and Nanda [4] show that conclusions depend on metric and granularity. McGrath et al. [5] document the Hydra effect, where later layers compensate for an ablated attention layer, and Rushing and Nanda [6] study self-repair more broadly; our single-layer nulls are consistent with these compensation effects and extend them to per-layer key/value caches and diffusion steps. Sparse autoencoders [9] and the public SAEs we use [11, 12], with SAELens [10] and TransformerLens [14], are the standard feature-level toolkit; sparse feature circuits [15] rank features across layers with attribution, and our SAE-global arm is a simplified version of that procedure. Attribution patching [13] supplies the ranking score. Our companion paper [7] identifies and certifies the FLUX.2 route used in §4.1.

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

Every result file from the preregistered panel, first run and rerun, is in [`experiments/2026-09-22-sae-comparison/results/`](experiments/2026-09-22-sae-comparison/results/), with the environment, model commits and file hashes for each run.

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
