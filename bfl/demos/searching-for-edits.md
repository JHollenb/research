---
title: "Searching for internal edits, keeping only the ones that improve the image"
type: experiment-report
status: "Promote-on-improvement editing with exact rollback, plus calibrated abstention; a methods result, no demonstrated route utility yet"
date: 2026-08-19
models:
  - name: "FLUX.2 Klein 4B (denoiser + Qwen3-4B text encoder)"
    id: "black-forest-labs/FLUX.2-klein-4B"
    revision: "e7b7dc27f91deacad38e78976d1f2b499d76a294"
merged_from:
  - route-cartographer-consumer-closure.md
  - native-state-route-selector-v6.md
tags: [flux2, diffusion, interpretability, model-editing, rollback, abstention, calibration]
---

# Searching for internal edits, keeping only the ones that improve the image

## What we found

We built two FLUX.2 Klein 4B experiments around one rule: propose an internal edit, and keep it only if the decoded image actually improves — otherwise roll it back exactly. A route map that predicts which internal pathway carries the next observation at **0.977 held-out accuracy** still has only **1 of 4** proposed edits promoted when each is judged on the final image, with **exact rollback 5/5** on the rejected ones. The same experiment shows why most proposals fail: single-token edits close the loop at just **0.001–0.227** return-state alignment, while a whole-text-state transfer reaches **≥ 0.911** — local addresses are good selectors, not standalone programs. A companion selector adds the complementary behavior: calibrated to a support radius with **zero false positives**, it abstains on a genuinely new image family and falls back to **byte-identical** native continuation (image difference 0.000). The result is methodological — a *promote-on-improvement + exact-rollback + abstain-when-unsure* loop that turns rejected edits and distribution shift into recorded evidence instead of silent failure.

![When the selector meets an unsupported family (six green circles, which this model already under-renders as five), it abstains, so its output is byte-identical to plain native continuation — image difference 0.000. Abstaining, not acting, is the correct move when no calibrated in-support advantage exists.](../artifacts/native-state-route-selector-v6/heldout__green_circles_six__seed-7001__selector_dispatch.png)

## Why it matters

Activation patching and most editing methods (ROME, Meng et al. 2022; Prompt-to-Prompt, Hertz et al. 2022) apply an internal change and read off its internal effect, keeping the edit. Here the adjudicator is the model's actual output: an edit is accepted only if the real denoiser, scheduler and decoder produce a better image, and every rejected edit is reverted exactly — the same exact-no-op guarantee used elsewhere as a correctness check, used here as a *rollback primitive*, in the spirit of Git-style model checkpointing. The selector adds a calibrated fail-closed gate: a support region, fixed in advance with zero false positives, decides when *not* to act. Both make negative results first-class, which is the point — an editor you can trust is one that mostly declines.

## Setup

| | |
|---|---|
| Model | FLUX.2 Klein 4B, revision `e7b7dc27…d76a294`; 256×256; 4 denoising steps |
| Blocks | five dual-stream (`joint.0`–`joint.4`) then twenty merged single-stream (`single.0`–`single.19`) blocks per step |
| Route | the internal pathway an edit is written to — its address, the hidden state carried there, and the timing — scored only by its effect on the two readouts |
| Readouts | the packed latent the scheduler consumes, and the decoded RGB image |
| Edited | address-driven state writes (cartographer); three fixed repair routes `joint3_gain2`, `joint4_gain2`, or none (selector) |
| Measured | *progress* `P = 1 − MAD(I, I_target)/MAD(I_source, I_target)`; *return-state alignment* (cosine of the latent displacement to the target's), with a 0.50 closure bar |

**The admission rule.** A proposed edit is *promoted* only if the decoded endpoint improves; otherwise the checkpoint is restored exactly (image unchanged, MAD 0.0). **Abstain** means native continuation: the selector leaves the trajectory untouched.

## Results

### Map the routes, predict the address, promote only on the image

*An address map is accurate and predictive, but closing the loop on the real image rejects most local edits — the pathway is a typed temporal coalition of address, state and timing, not a catalog of single-token programs.*

The cartographer captures 685 native states, 85 logical branches and 325 observations across 56 nodes and 54 edges, over both readouts and two role-conditioned chains (subject return vs. lighting return). Parallel routes show broad participation (entropy 0.975–0.994) while serial corridors are selective (subject-return corridor at `single.18` 0.114; RGB subject return 0.374; lighting 0.299 and 0.455). A held-out address selector predicts which pathway carries the next observation at 0.990 accuracy, 0.977 on later held-out evaluation — address information is not random.

Promotion is far stricter than prediction. Of four address-driven proposals, **one** is promoted (the endpoint improved) and **three** are rejected, with **exact rollback 5/5** restoring the prior image and route state. A fresh confirmation then demotes the strong "each address is its own program" reading: four single-token QKV edits reach endpoint return alignment only 0.001, 0.227, 0.105 and 0.197 — all below the 0.50 bar — while the complementary whole-text-state transfer closes every joint edge at weakest alignment 0.911. Local addresses are causally live but not sufficient on their own; address, carried state, timing and the downstream readout jointly determine the image. The map proposes; the image decides.

### A selector that abstains on a family it was not calibrated for

*Given an early native state, the selector picks a repair route or declines; calibrated for zero false positives, it correctly declines on an unsupported family and matches exact native continuation.*

The selector reads a 32-dimensional pooled summary of the early native `joint.1` text state and chooses `native`, `joint3_gain2`, `joint4_gain2`, or `abstain`. Development, calibration and held-out use disjoint families and disjoint seeds, and held-out outcomes are never visible at dispatch. Calibration selected support multiplier 3.0 / radius 8.115 as the largest region with zero false-positive repairs on its own panel.

On the green held-out panel (families the selector was never calibrated for), it abstained on both six-circle rows and chose native on the five-square and negative three-triangle rows — exactly matching constant native continuation. Its dispatch output is byte-identical to native (MAD 0.000; the zero-state and wrong-time control arms are also 0.000, inverted-state 1.298). The two independent evaluators agree on 105 of 106 rows. The honest reading: the selector changed the route *label* on some rows without improving the downstream count — both policies sit at positive mean count error 1.500 (0/4 exact; negatives exact), while the fixed `joint3` route reaches 0.500 and fixed `joint4` 2.500 and visibly merges components. No in-support regime with a calibrated route advantage ever arose, so abstention was correct rather than a miss. Treat the varied dispatch as a promising native-state signal, not yet useful orchestration.

![A fixed repair route (`joint3_gain2`) applied to the same held-out prompt. It is a non-native edit the selector could have dispatched; here it neither helps the count nor stays byte-identical, which is why an edit must be judged on the image before it is kept.](../artifacts/native-state-route-selector-v6/heldout__green_circles_six__seed-7001__fixed_joint3.png)

## Controls

- **Exact rewind + suffix replay** (exact): the rollback and the no-op are genuine, not approximate.
- **Held-out address prediction**: rules out that the selector memorized the captured sequence.
- **Promotion on the decoded image**: rules out internal-only overfitting — a predictable edit is not an accepted one.
- **Single-token QKV vs. whole-state transfer**: tests the local-program hypothesis directly.
- **Disjoint dev/calibration/held-out families and seeds; outcomes hidden at dispatch**: rules out leakage.
- **Two independent image evaluators, disagreements retained**: rules out choosing the favorable instrument.
- **Zero-state / inverted-state / wrong-time selector arms**: rule out a trivial dispatch artifact.

## Limits and open questions

| Limitation | Status |
|---|---|
| No demonstrated route utility | On this split the selector does not beat constant native or the fixed-route baselines; its varied dispatch did not improve the count outcome. |
| Correct-by-absence abstention | Calibration never entered an in-support regime with a real route advantage, so safe abstention is not yet a demonstrated discriminative win; the next experiment needs a calibration set with genuine in-support advantages and a held-out family where a selector can beat native without collateral. |
| Promotion yield | The cartographer promotes only 1 of 4 proposals; address predictability is necessary but not sufficient for an image-level improvement. |
| Instrument/readout dependence | Route entropy depends on the set of candidate pathways and the chosen endpoint; a low-entropy route in one readout can be distributed in another. |
| No universal topology or stable addresses | `joint.i`/`single.i` are the tested checkpoint's own ordinals; an address or its state must be re-enumerated and re-promoted for Klein 9B, Dev, or FLUX.1, never copied across revisions. |
| Evaluator resolution | The image atlas can merge components at low resolution (one calibration disagreement; the `joint4` control genuinely merges), so disagreements are retained, not resolved by downsampling. |
| Scope | One model, one split, one action set, two seeds per phase; no generalization claim. |

## Reproduce and inspect

- Route cartographer (capture, route signatures, native outcomes, held-out predictors): [`artifacts/route-cartographer-consumer-closure/`](../artifacts/route-cartographer-consumer-closure/) — run its `verify.py` to check capture size, entropy, selector accuracy, promotion/rollback, single-token failures, and whole-state closure.
- Native-state selector v6 (report, analysis, portable selector package, held-out images): [`artifacts/native-state-route-selector-v6/`](../artifacts/native-state-route-selector-v6/) — run its `verify.py` to check the 106-row panel, disjoint split, calibration radius, and held-out abstention.

Additional internal run logs are available on request.
