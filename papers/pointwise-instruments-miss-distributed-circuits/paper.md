---
title: "Single-Site Tests Miss Distributed Stores"
type: research-paper
status: published
date: 2026-08-21
updated: 2026-09-22
tags: [interpretability, activation-patching, causal-mediation, flux2, language-models, methods]
---

# Single-Site Tests Miss Distributed Stores

**Evidence from a diffusion transformer and three language-model families, and a blind-graded comparison of standard readouts against the model's own output**

Jacob Hollenbeck

*2026-08-21; revised 2026-09-22*

---

## Abstract

Activation patching usually asks one site at a time whether a component is necessary or sufficient for a behavior. We show measured cases where that question gets the wrong answer because the information the output depends on is spread across steps or layers, so no single site is necessary and no single site's slice is sufficient, while the whole path is both. In FLUX.2 Klein 4B, ablating any one of four route components at any one denoising step leaves at least 22% of an identity transition intact, which reads as "no necessary component"; ablating the same four components at every step leaves 0.13%, and inserting them carries 91% of the transition, on held-out seeds. In SmolLM2-1.7B and Qwen2.5-0.5B, replacing a subject token's key/value entries at a single layer changes the target log-probability by at most 0.4 nats and never changes the answer, while replacing them across the second half of the stack moves it by 0.8–3.4 nats and flips the top answer in four of four cells. Writing the same displacement into a single layer's KV slice does almost nothing (normalized effect ≤ 0.11); writing it into all layers' KV restores the full effect. We package these results with a preregistered, blind-graded comparison of four standard readouts (single-step patching, a validated nearest-class-mean probe, a transferred difference-of-means direction, and a reconstruction cosine) against the unchanged downstream model on the same inputs; the standard readout gave the wrong verdict in 4 of 4 graded cases. The comparison uses our own implementations of these recipes on cases chosen because we expected them to fail, so it demonstrates that the failure modes exist, not how often they occur. Both evidence bundles ship with offline verifiers.

## 1. The problem

Causal-intervention methods in interpretability, from activation patching and path patching to causal tracing, typically localize a behavior by intervening on one site (a layer, head, position, or step) at a time and measuring the change in output [1–4]. A null at every site is often read as "this behavior has no localized mechanism here." That reading assumes the relevant information is concentrated enough that removing one piece hurts. If instead the output reads from a store that is written redundantly across many layers or steps, single-site ablation will be compensated by the rest of the store and single-site insertion will be too small to matter. Self-repair in language models, where downstream components compensate for an ablated one, is a known instance of this [5, 6], and best-practice guides for activation patching already warn that metrics and patching granularity change conclusions [3, 4].

This paper contributes measured examples of the pattern in two very different architectures, a simple test that distinguishes it from "no mechanism," and a blind-graded demonstration of how four common readouts produce confident wrong verdicts in the same regimes.

## 2. The four-quadrant test

For a behavior with a clean source and target condition, we run four interventions and judge each by the unchanged downstream model (the rest of the network, run to completion, reading out its own answer):

|  | one site | whole path |
|---|---|---|
| **necessity** (ablate in the target run) | behavior survives | behavior is removed |
| **sufficiency** (write into the source run) | little or no transfer | full transfer |

"Whole path" means the same component at every denoising step (diffusion) or the same token position's key/value entries across a contiguous range of layers (language models). A localized mechanism would pass at least one single-site quadrant. A behavior that the model does not actually depend on would fail the whole-path quadrants. The cross pattern above is what redundant, distributed storage predicts.

Two limits apply to how this test should be read. First, the pattern is relative to the cut being intervened on. Writing the full hidden-state displacement into the residual stream at a single layer is sufficient in every language-model cell below (normalized effect 0.85–1.02), because the residual stream carries everything downstream; the single-site nulls hold for per-layer KV slices, not for the residual stream. Second, whole-path ablation of a token's KV at every layer is close to deleting that token from the context, so the informative part of the result is the single-site failure and the size of the gap, not the whole-path success on its own.

## 3. Setup

**Diffusion.** FLUX.2 Klein 4B (revision `e7b7dc27f91deacad38e78976d1f2b499d76a294`), BF16, 256×256, 4 steps, guidance 1.0. The contrast is a fox → cat identity transition. The four components are the route sites `joint.2`, `joint.3`, `joint.4` and `single.0` found in our companion paper [7]. Effects are reported as the fraction of the source-to-target transition remaining (necessity) or carried (sufficiency), measured on the rendered image. Held-out seeds 31337 and 60660 were not used to choose the sites.

**Language models.** SmolLM2-1.7B, Qwen2.5-0.5B, Qwen3-8B. Prompts describe a scene and ask for the subject, its color, or its action (for example, a fox sitting in snow). Necessity replaces the subject position's keys and values with those computed for a generic filler word ("creature") at one layer, the first half, the second half, or all layers, and reports the change in log-probability of the original answer (Δlp) and the new top answer among a frozen candidate set. Sufficiency writes the source-to-target displacement into the hidden state at one layer (W1), one layer's KV (W2 single), or all layers' KV (W2 all), normalized so that 1.0 matches the native target. Every arm has an exact no-op gate (maximum absolute logit change 0.0).

**Execution.** All runs used exact-replay instrumentation: the unmodified parent computation is captured once, each intervention forks from it, and a no-op fork must reproduce the parent bit-for-bit before any intervention is scored.

## 4. Results

### 4.1 FLUX.2: no single step is necessary; the route across steps is

A sweep of every single component at every single step, in both directions, leaves at least 22.2% of the identity transition in place when ablated, and inserting any one of them at one step leaves the fox a fox (Figure 1). By the usual reading, no component is necessary. Ablating the same four components across all steps leaves 0.13% of the transition, and inserting them across all steps carries 91.1%, on both held-out seeds, with exact no-op gates.

![Figure 1. Single-component, single-step interventions at step 2 in FLUX.2 Klein 4B. Top-left: fox source and cat target. "sufficiency": inserting the cat-run state at one component into the fox run leaves a fox. "necessity": ablating one component in the cat run leaves a cat. "rescue": restoring one downstream edge after an upstream ablation also leaves a cat. Every single-site, single-step arm reads as "no effect." The same components across all steps remove (0.13% remaining) or carry (91.1%) the transition.](figures/fig1-single-step-patching.png)

### 4.2 Language models: single-layer KV swaps do almost nothing; the second half of the stack does everything

| model, behavior | clean answer | one layer (L12 / L18) Δlp | first half Δlp | second half Δlp → top answer | all layers Δlp → top answer |
|---|---|---:|---:|---:|---:|
| SmolLM2-1.7B, identity | fox | +0.03 / +0.40 | +0.36 | −2.09 → wolf | −2.09 → wolf |
| SmolLM2-1.7B, color | red | +0.02 / −0.04 | −0.13 | −1.20 → white | −1.08 → white |
| Qwen2.5-0.5B, identity | fox | +0.18 / +0.23 | −0.71 | −3.39 → wolf | −3.09 → wolf |
| Qwen2.5-0.5B, color | red | −0.02 / −0.06 | −0.10 | −0.98 → white | −0.83 → white |
| SmolLM2-1.7B, action | sitting | −0.00 / −0.08 | −0.10 | −0.71 → sitting | −0.95 → sitting |

In the four identity and color cells, no single-layer swap changes the answer and the largest single-layer effect is under a fifth of the path effect, while the second-half swap flips the top answer. The effect is concentrated in the second half: first-half swaps are small in three of four cells. The action cell shows the same shape but a smaller effect that does not flip the answer. Sufficiency mirrors necessity: writing the displacement into one layer's KV gives a normalized effect between −0.002 and 0.005 in the four Qwen2.5 and SmolLM2 color/identity/action cells from the grid run, while writing it into every layer's KV gives 1.01–1.31. A separate SmolLM2 identity run (lion, wolf, tiger targets) gives 0.01–0.11 for a single layer's KV and 1.06–1.09 for the full KV trace.

**Qwen3-8B.** We also ran identity and color cells on Qwen3-8B. We do not count them as evidence. In both, the answer is already predicted from the scene alone: with the subject replaced by a generic word, the model still answers "fox" at a 1.44-logit margin and "red" at a log-probability within 0.03 of the clean prompt. Whole-path ablation leaves the top answer unchanged in both. These cells passed a bar we amended after seeing this confound (ablation must land at the no-subject floor), and the identity cell needed an fp32 rerun to decide a 0.014-nat miss at BF16 resolution. The confound is informative in its own right: a necessity null can simply mean the context already determines the answer.

### 4.3 What the diffusion time axis does and does not show

Writing the target displacement at different subsets of the four FLUX steps and scoring pixel reproduction of the target render, early steps score far higher than late ones: step 0 alone 0.13, steps 0–1 0.37, all four 0.73, and steps 2–3 at double dose only 0.16 (lion, seed 7217; the other three seed/target cells are similar). That is a statement about reproducing the target image, not about identity. Figure 2 shows the difference: steps 0–1 still render a fox, while the late double-dose arm renders a recognizable lion in a different pose and coat, which pixel distance scores poorly. Early steps fix layout; late steps can still change what the animal is.

![Figure 2. Write schedule vs outcome for fox → lion in FLUX.2 Klein 4B (seed 7217). "Progress" is 1 − pixel MAD to the target render, normalized by source-to-target MAD. The late double-dose arm scores 0.16 but visibly renders a lion, so progress measures reproduction of the target image, not whether the identity changed.](figures/fig2-write-schedule.png)

## 5. Four readouts that give the wrong verdict

To make the practical consequence concrete, we preregistered six cases in which a common readout and the downstream model could disagree, ran both arms on matched inputs, and had a fresh grader with no project context compare anonymized readings against a frozen rubric. The success criterion, fixed in advance, was that the standard arm misreport in at least three of the four main cases.

| case | standard readout and its verdict | what the downstream model does | blind grade |
|---|---|---|---|
| 1. FLUX identity route | single-component, single-step patching sweep: "no necessary component" (≥ 22% of the transition survives every cell) | all-step ablation removes the transition (0.13% remains); all-step insertion carries it (91%) | misreport |
| 2. Foreign-conditioner subject rows (FLUX) | nearest-class-mean probe, 16/16 correct on held-out native states: "no decodable content" (top-1 tiger, margin 0.035 vs floor 0.352) | transplanting the two subject rows into a native fox run renders a wolf on both seeds (Figure 3) | misreport |
| 3. Cross-model direction transfer (Qwen) | transferred difference-of-means direction, bit-identical to the original pipeline: 95.4% negative cosines, "representations differ across families" | native cosines are 0% negative in every model; the split falls to 0.0 under mean-centering alone | misreport |
| 4. Reconstruction cosine (FLUX) | cosine 0.993–0.997 on held-out prompts: "state recovered" | a content-free mean template scores the same; rendered, the reconstruction differs from native by pixel MAD 70–97 and shows the wrong animal for all four prompts | misreport |
| 5. Mediation across steps (control case) | single-step mediation: "holds at the measured step" | holds in 17/18 step × axis cells | inconclusive |
| 6. Zeroed answer logits (reserve) | "a zeroed logit is a maximal knockout" | all 76 zero records are at the final layer, where RMSNorm of a zero vector followed by a bias-free unembedding gives zero arithmetically | misreport |

The criterion was met: 4 of 4 main cases graded as misreports, 5 counting the reserve. Case 5 was included because we expected the standard reading to be correct there; the grader instead declined to decide the generality question, and we report that disagreement as it stands.

![Figure 3. Case 2. Left to right: native fox run; a run with a foreign text encoder, whose subject rows a validated probe reads as containing no animal; the same two subject rows transplanted into the native fox run, which then renders a wolf; the native wolf prompt for reference.](figures/fig3-probe-vs-consumer.png)

**How to read this table.** The standard arms are our own implementations of each recipe, not TransformerLens, nnsight, SAELens, or another library; the diffusion cases could not use those libraries because none supports FLUX. We made each arm as strong as we could (case 2's probe was 16/16 on held-out native states; case 3's pipeline reproduced the original bit-for-bit), and a reviewer checked each arm before it ran. But the cases were chosen because we already suspected the readout would fail there, and the ground truth in each case comes from the downstream-model arm. The trial therefore shows that these failure modes occur in real models under faithful implementations. It does not estimate how often they occur, and it does not test sparse autoencoders or any other dictionary method. Case 2 in particular is partly a distribution-shift failure: a probe trained on native states is being applied to states produced by a different text encoder.

## 6. What broke, and what this does not show

- **Scale floor.** In 70M-parameter Pythia checkpoints that can do the task, about 80% of the effect is carried by a single layer. The distributed pattern appears at or above 410M in our tests, not below.
- **Cut dependence.** At the hidden-state cut, the single-site quadrants fail in SmolLM2 and Qwen2.5 as well as in Mamba-2.8B (single-site necessity rises to 172–236% of the path effect when only the cut changes). The pattern is a property of per-layer KV and per-step diffusion interventions, not of an architecture.
- **No constructive recipe.** Weighting a write by the measured per-layer or per-step profile did not produce a better edit than writing at the best single site in SmolLM2-1.7B (≈ sham vs 0.94–1.02), and only partly recovered at Qwen3-8B. Reading and writing are asymmetric.
- **Token time.** Unlike depth and diffusion steps, the token axis did not accumulate: ablating the scene suffix moves about 1% of the subject effect.
- **Tools not tested.** No sparse autoencoder, attribution-patching, or path-patching implementation was compared. The comparison in §5 covers single-step patching, probing, direction transfer, and reconstruction cosine only.
- **Breadth.** One lab, single-token readouts, a handful of prompts per cell, two to three seeds, models up to 8B plus one exploratory 30B mixture-of-experts identity cell. No external replication.

## 7. Related work

Activation patching and causal tracing [1, 2] and path patching [8] are the standard tools this paper examines. Zhang and Nanda [3] and Heimersheim and Nanda [4] show that patching conclusions depend on metric and granularity. McGrath et al. [5] document the Hydra effect, in which ablating one attention layer causes later layers to compensate, and Rushing and Nanda [6] study self-repair more broadly; our single-layer KV nulls are consistent with, and likely an instance of, these compensation effects. Sparse dictionary methods [9] decompose activations into features; we did not evaluate them. Our companion paper [7] identifies and certifies the FLUX.2 route used in §4.1.

## 8. Reproduce

Both bundles run offline with Python and no GPU.

```bash
# Four-quadrant certificate receipts and render panes
cd evidence/ird-certificate && python3 verify.py
# expect: 35/35 files hash-verified ... VERIFY OK

# Blind-graded instrument comparison
cd evidence/instrument-trial && pip install . && instrument-trial-verify
# expect: RESULT: all hashes and all mechanical verdicts verified
```

The receipts record the scheduler job ID, model path, and worker hash for every run. The grader's raw output is `evidence/instrument-trial/bundle/grading/grader-raw.json`.

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
