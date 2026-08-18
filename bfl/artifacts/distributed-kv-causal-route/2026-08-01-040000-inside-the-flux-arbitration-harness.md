---
title: "Inside the FLUX Arbitration Harness"
subtitle: "A complete arc report: instrumenting the diffusion transformer's K/V memory, measuring a block-level restoration threshold, watching the quorum claim fail its own replication, and discovering that FLUX.1's text encoder cannot even compose the workload"
author: strider
type: experiment-report
subtype: generative-analysis
date: 2026-08-01
created: 2026-08-01T04:00:00-07:00
updated: 2026-08-02
status: arc-corrected-control-repair-pending
claim_status: restoration-threshold-portable-quorum-retracted-distributed-temporal-route-supported-five-controls-valid-reverse-wrong-world-invalid-bilateral-specificity-pending-universal-open-flux1-admission-failed
tags: [experiment-report, generative-analysis, model-analysis, flux, black-forest-labs, diffusion-transformers, mmdit, arbitration, coalition-competition, kv-graft, mediation, dose-response, gate-compression, held-out-replication, cross-architecture, klein-4b, flux1-schnell, single-stream, binding, text-encoder, clip, t5, qwen]
source_docs:
  - ../../experiments/2026-07-31-211500-flux-arbitration-harness/PLAN.md
  - ../../experiments/2026-07-31-211500-flux-arbitration-harness/DESIGN_REVIEW.md
  - ../../experiments/2026-07-31-211500-flux-arbitration-harness/outputs/g4-dose.v1.json
  - ../../experiments/2026-07-31-211500-flux-arbitration-harness/outputs/g4b-release-lattice.v1.json
  - ../../experiments/2026-07-31-211500-flux-arbitration-harness/outputs/klein-gate-fit.v1.json
  - ../../experiments/2026-07-31-211500-flux-arbitration-harness/outputs/h1-heldout-native-replication.v1.json
  - ../../experiments/2026-07-31-211500-flux-arbitration-harness/outputs/h2-semantic-quorum/h2-semantic-quorum.v1.json
  - ../../experiments/2026-07-31-211500-flux-arbitration-harness/outputs/h3-native-semantic-patch/h3-native-semantic-patch.v1.json
  - ../../experiments/2026-07-31-211500-flux-arbitration-harness/outputs/h4-native-carrier-confirmation/h4-native-carrier-confirmation.v1.json
  - ../../experiments/2026-08-01-flux1-schnell-arbitration/PLAN.md
  - ../../experiments/2026-08-01-conditioner-cartography/outputs/conditioner-cartography.v1.json
  - ../../experiments/2026-07-31-211500-flux-arbitration-harness/outputs/h7-heldout-quotient-dose/h7-heldout-quotient-dose.v1.json
  - ../../experiments/2026-07-31-211500-flux-arbitration-harness/outputs/h7-heldout-quotient-dose/H7_VISUAL_AUDIT.md
  - ../../experiments/2026-07-31-211500-flux-arbitration-harness/H8_TEMPORAL_ROUTE_LOCALIZATION_DESIGN.md
  - ../../experiments/2026-07-31-211500-flux-arbitration-harness/outputs/h8-temporal-route-localization/h8-temporal-route-localization.v1.json
  - ../../experiments/2026-07-31-211500-flux-arbitration-harness/outputs/h8-temporal-route-localization/H8_VISUAL_AUDIT.md
  - ../../experiments/2026-07-31-211500-flux-arbitration-harness/H9_SPECIFICITY_REPLICATION_DESIGN.md
  - ../../experiments/2026-07-31-211500-flux-arbitration-harness/outputs/h9-specificity-replication/h9-specificity-replication.v1.json
  - ../../experiments/2026-07-31-211500-flux-arbitration-harness/outputs/h9-specificity-replication/H9_VISUAL_AUDIT.md
  - ../../experiments/2026-08-02-bfl-three-claims/h9-causal-route/ADVERSARIAL_REVIEW.md
  - ../../experiments/2026-08-02-bfl-three-claims/h9-causal-route/OWNER_REPAIR_STATUS.md
  - ../../experiments/2026-07-31-211500-flux-arbitration-harness/H9_REVERSE_WRONG_WORLD_REPAIR_DESIGN.md
related:
  - "[[../indexes/generative-model-analysis|Generative Model Analysis Index]]"
  - "[[../generative-model-wiki|Generative Model Wiki]]"
  - "[[../model-analysis-wiki|Model Analysis Wiki]]"
  - "[[../black-forest-labs-model-wiki|Black Forest Labs Model Wiki]]"
  - "[[2026-08-01-013000-the-diffusion-transformer-had-the-same-quorum|The Diffusion Transformer Had the Same Quorum]]"
  - "[[2026-08-01-032700-the-restoration-was-real-the-quorum-was-not-proven|The Restoration Was Real; the Quorum Was Not Proven]]"
  - "[[2026-08-01-142952-the-payload-was-semantic-the-quorum-was-not-native|The Payload Was Semantic; the Quorum Was Not Native]]"
  - "[[2026-08-01-block-13-native-carrier-not-quorum|Block 13: Native Carrier, Not Quorum]]"
  - "[[2026-08-01-152951-the-answer-was-a-quotient-of-a-causal-state|The Answer Was a Quotient of a Causal State]]"
  - "[[2026-08-01-001500-opening-the-black-forest-what-six-parallel-tracks-taught-us-about-flux|Opening the Black Forest: What Six Parallel Tracks Taught Us About FLUX]]"
  - "[[2026-08-01-020000-the-plane-was-the-shadow-of-a-moving-frame|The Plane Was the Shadow of a Moving Frame]]"
  - "[[2026-07-31-212627-what-we-know-about-the-black-forest-models-a-data-driven-report|What We Know About the Black Forest Models]]"
  - "[[2026-07-31-205147-the-gate-survived-review-the-bias-did-not-and-flux-repeated-the-cliff|The Gate Survived Review; the Bias Did Not]]"
  - "[[2026-07-31-145130-the-conditioners-were-stock-checkpoints|The Conditioners Were Stock Checkpoints]]"
  - "[[2026-07-31-140500-the-gate-was-eleven-numbers-and-the-bias-knew-them|The Gate Was Eleven Numbers and the Bias Knew Them]]"
  - "[[2026-08-01-conditioner-cartography-reconstruction-bottleneck|The Binding Bottleneck Was Reconstruction, Not Encoding]]"
  - "[[2026-08-01-h7-heldout-quotient-replication|The Route Replicated; Native Specificity Did Not]]"
  - "[[2026-08-01-h8-temporal-route-localization|The Route Accumulates Across Time]]"
---

# Inside the FLUX Arbitration Harness

> **Adversarial correction, 2026-08-02.** The original H9 automatic verdict is superseded. Its
> reverse wrong-world arm reused a donor map certified only for forward clean-world payloads;
> 45/96 reverse donors collide with a destination color. Five controls, the distributed route,
> temporal accumulation, image custody, and full20 endpoint result survive. Bilateral six-control
> specificity awaits the frozen direction-safe H9R repair. The same implementation affected the
> earlier H5–H7 reverse wrong-world controls; they must not be cited as collision-safe evidence.

This is the complete arc report for the FLUX arbitration harness: one night's work from first
instrumentation to final verdict. The arc began at 21:15 on July 31 and closed around 04:00 on
August 1 — roughly seven hours of continuous measurement across two FLUX model families and nine
execution gates.

The high-level story is short. We built an instrument that grafts clean K/V memories into a
corrupted diffusion transformer and measures whether the image repairs. The instrument works. The
restoration pattern we found is real and portable to new prompts. But the interpretation we first
gave it — that the model organizes an endogenous "quorum" through specific blocks — was too strong.
A held-out replication test confirmed the portable part and corrected the overclaim. And when we
tried to extend the instrument to FLUX.1-schnell, we discovered that its older text encoder cannot
even compose the workload.

## What we were trying to learn

The question came from the Qwen language model work. In
[[2026-07-31-140500-the-gate-was-eleven-numbers-and-the-bias-knew-them|the Qwen arbitration
microscope]], we had found that when two facts compete for a single output token, the model resolves
the competition through a distributed coalition of K-heads. A 287-edge release hypergraph compressed
to an 11-parameter additive gate. The gate had necessary ports, supporting ports, and a sharp
threshold — a structure we called a "quorum."

The natural question: is that structure specific to autoregressive language models, or does it
appear in other transformer architectures? Black Forest Labs' FLUX family of diffusion transformers
offered a clean test. FLUX uses a Modified Multimodal Diffusion Transformer (MMDiT) with
double-stream blocks (joint text+image attention) feeding into single-stream blocks (image-only
attention with text K/V injected via cross-attention). The text conditioning enters through K/V
projections at specific sites — structurally analogous to the K-heads in Qwen.

We chose FLUX.2-klein-4B as the primary target (7.3 GB bf16, fits entirely on a 16 GB RTX 4080)
and FLUX.1-schnell as the bias-channel rung (12B transformer with `bias=True` on Q/K/V
projections, the pre-cliff architecture analogous to Qwen 0.5B).

## The workload: corrupted color binding

The arbitration workload is isomorphic to the Qwen binding task. Each trial has two worlds:

- **clean world**: `"a red cube on the left and a blue sphere on the right"` — two objects with
  distinct colors, deterministically placed
- **corrupt world**: the color token for object A is replaced with a distractor color at the
  SAME token position: `"a green cube on the left and a blue sphere on the right"`

The witness is a hue classifier over the left half of the generated image. In the clean world, the
left-half hue should match object A's color (red). In the corrupt world, it should flip to the
distractor (green). This produces a behavioral signal we can measure automatically.

The graft intervention: take clean-world K/V memories from the single-stream blocks and inject them
into the corrupt-world forward pass at the same token positions. If binding information travels
through these K/V channels, grafting the clean values should repair the corrupt image.

Sixteen prompt pairs were generated per gate, with enforced hue separation (minimum 60° between
colors), position constraints (object A always left), and single-token color verification.

## Timeline and gate progression

### ~21:15 Jul 31 — G0: instrumentation parity

The first gate establishes that the instrument doesn't break things. Eleven sub-gates, all
fail-closed:

1. **Untouched replay bit-exact** — same seed produces same latent hash
2. **Roundtrip write-landed** — K/V write actually modifies the target tensor
3. **Roundtrip bit-exact restore** — K/V write+restore produces identical latents to untouched
4. **Delivered edit applied** — overwritten K/V values are read back correctly
5. **Delivered edit changes latents** — the overwrite actually affects the output
6. Six more: static model layout, BTHF coordinate schema, hook cleanup, denoiser call count,
   bias-absence check, certified adapter profile

Result: **PASS 11/11.** The hooks are live, reversible, and causally effective.

### ~22:00 Jul 31 — G1: workload admission

Does the workload produce a clean enough signal? Each of 16 pairs generates a clean and corrupt
image. The clean image's left half should show the correct color; the corrupt image should flip.

- Clean correct rate: **16/16 (1.000)**
- Corrupt flipped rate: **15/16 (0.9375)**

Result: **PASS.** One corrupt pair's image was ambiguous (mixed hues), but the floor of 0.875 was
met. The workload produces reliable behavioral contrast.

### ~22:30 Jul 31 — G2/G2b: mediation bisection

Where does the binding information flow? FLUX.2-klein-4B has 5 double-stream blocks and 20
single-stream blocks.

**G2 (double-block probes)**: grafting all 5 double-stream K/V sites alone repairs **0/16** pairs.
The double-stream blocks do not carry the binding signal by themselves.

**G2b (full mediation scan)**: grafting single-stream K/V at all 20 blocks repairs **16/16** pairs.
Grafting all K/V (embed + double + single) also repairs 16/16. But every contiguous 5-block band
of single-stream blocks repairs **0/16**.

This establishes two facts: the binding lives in the single-stream blocks, and no small contiguous
subset is sufficient. The signal is distributed.

### ~23:00 Jul 31 — G4: dose-response

How many blocks do you need? Twenty-three arms systematically varied subset size and position:

| Subset size | Mean repair rate | Range | Arms |
|---|---|---|---|
| 5 | 0.000 | 0.000–0.000 | 4 |
| 6 | 0.000 | 0.000–0.000 | 3 |
| 8 | 0.042 | 0.000–0.125 | 3 |
| 10 | 0.050 | 0.000–0.188 | 5 |
| 12 | 0.000 | 0.000–0.000 | 3 |
| **14** | **0.604** | **0.000–0.938** | **3** |
| 16 | 0.896 | 0.813–1.000 | 3 |
| 18 | 0.917 | 0.875–0.938 | 3 |
| 20 | 1.000 | — | 1 |

A sharp threshold between size 12 (floor) and size 14 (mean 0.604). But the variance at size 14 is
enormous: 0.000 to 0.938. Whether a size-14 subset works depends on WHICH blocks are in it.

Position matters too: blocks 0–9 (early half) repair 3/16 (0.188), while blocks 10–19 (late half)
repair 0/16 (0.000) at the same subset size of 10.

### ~00:30 Aug 1 — G4b: release lattice

Which specific blocks matter? Thirty arms in three families:

**Necessity (drop-one, 20 arms)**: graft all 20 blocks minus one. Every block can be dropped
without losing full restoration — EXCEPT block 8:

| Block dropped | Repair rate | Delta from full |
|---|---|---|
| Block 8 | **0.188** | **−0.813** |
| Block 4 | 0.938 | −0.063 |
| Block 7 | 0.938 | −0.063 |
| Block 9 | 0.938 | −0.063 |
| Block 11 | 0.938 | −0.063 |
| All others | 1.000 | 0.000 |

Block 8 is the **kingmaker** — 8× more costly to remove than any other block. Losing it alone
drops restoration from 1.000 to 0.188.

**Sufficiency conditioning (6 arms)**: at size 14, does including the pair {8, 11} matter?

- Including {8, 11}: mean **0.583** (range 0.250–0.938)
- Excluding {8, 11}: mean **0.000** (0/16 on all three arms)

The pair is jointly necessary at threshold: without it, no size-14 coalition restores binding.
With it, most do.

**Pair probes (4 arms)**: the pair {8, 11} alone (size 2) repairs **0/16**. The pair plus 5 early
helpers repairs 3/16; the pair plus 5 late helpers repairs 0/16. The core is necessary but
radically insufficient.

### ~01:00 Aug 1 — Gate compression

All 53 arms (23 from G4 + 30 from G4b) were fit with a sigmoid-additive model:
`gate(subset) = σ(Σᵢ wᵢxᵢ + b)`, where xᵢ = 1 if block i is in the graft set.

| Model | LOO-CV R² | Parameters |
|---|---|---|
| Cardinality only (how many blocks) | 0.618 | 2 |
| Linear additive (which blocks, no squash) | 0.748 | 21 |
| **Sigmoid additive** | **0.970** | **21** |

The sigmoid captures the sharp 0-to-1 transition. Knowing WHICH blocks matter (R²=0.970) is 3×
better than knowing HOW MANY (R²=0.618).

Top weights from the sigmoid fit:

| Block | Weight | Share of total |
|---|---|---|
| **8** | **+4.676** | **29.6%** |
| 4 | +1.459 | 9.2% |
| 11 | +1.155 | 7.3% |
| 14 | +1.056 | 6.7% |
| 7 | +1.037 | 6.6% |
| 5 | **−0.580** | **3.7% (hurts)** |
| 16 | +0.000 | 0.0% (irrelevant) |

The bias term is **−11.01** — a subset must accumulate enough positive weight to push the logit sum
above zero. Block 8 alone contributes +4.676 of the needed ~11 logit units. Removing it drops most
coalitions below threshold. Block 5 is the only block with negative weight: including it in a graft
set slightly hurts restoration. Block 16 has weight zero.

No interaction term between blocks 8 and 11 improved the fit. The kingmaker pattern is a single
dominant weight in an additive sum, not a synergy.

### ~01:30 Aug 1 — discovery blog post

At this point, the results looked compelling enough for a strong claim:
[[2026-08-01-013000-the-diffusion-transformer-had-the-same-quorum|"The Diffusion Transformer Had
the Same Quorum."]] The word "quorum" was deliberately chosen to echo the Qwen result. The sigmoid
gate, the necessary core, the sharp threshold, the supporting coalition — all structurally analogous.

This was the high-water mark of the claim. What followed corrected it.

### ~02:00 Aug 1 — independent design review

An independent design review (by another session) identified the inferential gap in the discovery
results. The key insight: G4/G4b prove that clean K/V grafts CAN repair binding at a
subset-dependent threshold. They do not prove that the model USES those blocks for binding
natively. The intervention creates a counterfactual — "what if these blocks had clean memories?" —
but does not measure what the model does with those blocks in its natural forward pass.

Two specific gaps:

1. **Payload specificity**: we only tested correct-binding grafts. If ANY clean K/V repairs
   binding (even from a different pair), the restoration is partly a generic denoising effect, not
   a binding-specific intervention.
2. **Native site-specificity**: we never tested whether disrupting the model's own K/V at blocks
   {8, 11} hurts binding more than disrupting matched non-core blocks.

The review preregistered H1: 17 arms × 48 held-out instances (24 new pairs × 2 seeds), with frozen
interpretation thresholds.

### ~03:30 Aug 1 — H1: held-out replication

The most important run of the arc.

**What replicated:**

| Arm | Held-out rate | Discovery analog |
|---|---|---|
| full20_clean_graft | 46/48 (0.958) | 16/16 (1.000) |
| drop8 | 14/48 **(0.292)** | 3/16 (0.188) — **block 8 still kingmaker** |
| drop11 | 43/48 (0.896) | 15/16 (0.938) |
| all_but_8_11 | 5/48 (0.104) | 0/16 (0.000) |
| incl_core_14 | 39/48 **(0.813)** | ~9/16 (0.583) |
| excl_core_14 | 4/48 **(0.083)** | 0/16 (0.000) |

Block 8 dominance, core necessity, inclusion advantage — all replicate on new prompts and seeds.
The restoration threshold is portable.

**What failed:**

| Control arm | Rate | Threshold | Verdict |
|---|---|---|---|
| wrong_token_full20 | 12/48 **(0.250)** | ≤ 4/48 (0.083) | **FAIL** |
| wrong_world_full20 | 22/48 **(0.458)** | ≤ 4/48 (0.083) | **FAIL** |

**wrong_world_full20** is the critical failure. Grafting a DIFFERENT pair's clean K/V — completely
unrelated binding, different colors, different objects — repairs binding 46% of the time. This means
roughly half the "restoration" comes from overwriting corrupt K/V with ANY clean K/V, regardless of
content. The graft is partly a general denoising intervention.

**wrong_token_full20** also breached: grafting object B's color K/V partially repairs object A's
binding at 25%. The payload is less position-specific than the discovery implied.

**Native site-specificity: NULL.**

The most important test. If blocks {8, 11} are a native "quorum," disrupting their K/V should hurt
more than disrupting matched non-core blocks {6, 10}.

| Condition | Core {8,11} swap | Matched {6,10} swap | Delta |
|---|---|---|---|
| Clean, correct rate | 46/48 (0.958) | 47/48 (0.979) | −0.021 |
| Corrupt, distractor rate | 2/48 (0.042) | 1/48 (0.021) | +0.021 |
| Clean margin (bootstrap 95% CI) | — | — | [−4.26°, +3.72°] |
| Corrupt margin (bootstrap 95% CI) | — | — | [−4.22°, +2.85°] |

Both confidence intervals include zero. Blocks {8, 11} are NOT preferentially used for binding in
normal forward passes. The kingmaker status is a property of the intervention (those blocks are
effective graft targets), not a property of the native computation.

**Scientific verdict: HELDOUT_REPLICATION_NOT_MET.**

The word "quorum" was retracted for this model. The correct description became: **"portable
clean-payload restoration threshold with block-8-dominant additive gate structure; binding
specificity partial; native site-specificity unresolved."**

### ~03:30–04:00 Aug 1 — FLUX.1-schnell rung

With the cross-architecture claim already weakened by H1, we proceeded to the FLUX.1 rung to test
the bias-channel question independently. FLUX.1-schnell (12B transformer, 19 double + 38 single
blocks) has `bias=True` on all Q/K/V projections — the pre-cliff architecture.

**Memory engineering**: the 12B model with float8 layerwise casting fills ~12 GB. With activations
at 1024×1024, total exceeds 16 GB. Three approaches were tested:

- `pipeline.to(device)`: OOM (transformer + VAE simultaneously)
- `enable_model_cpu_offload`: OOM (whole transformer still on GPU at once)
- `enable_sequential_cpu_offload`: **works** (~676 MB peak VRAM, but ~2–3 min per image)

**G0 passed** (11/11) at both 512×512 and 1024×1024 — the instrumentation is correct.

**G1 failed** at every configuration:

| Resolution | Steps | Clean rate | Corrupt rate |
|---|---|---|---|
| 512×512 | 4 | 0.750 | 0.625 |
| 768×768 | 4 | 0.625 | 0.750 |
| 1024×1024 | 4 | 0.375 | 0.688 |
| 1024×1024 | 8 | 0.375 | 0.688 |

The floor is 0.9375 for both rates. FLUX.1-schnell cannot reliably compose two-object color binding
at ANY tested configuration. The CLIP+T5 text encoder lacks the compositional strength that
klein-4B's Qwen3-4B conditioner provides (which achieves clean=1.000, corrupt=0.9375 at 512×512
with 4 steps).

Visual inspection confirmed: at 512×512, images contain text artifacts and anatomical diagrams
instead of colored objects. At 1024×1024, the model sometimes produces one object coherently but
fails to bind two distinct colored objects. pair001 at 1024 generated a cave scene with human
silhouettes — a complete prompt failure.

The bias-channel question cannot be answered with this workload on FLUX.1-schnell. The failure is
at the text-encoder level, not the arbitration instrument level.

### ~14:00 Aug 1 — H2: semantic quorum (full-palette reanalysis)

The H1 wrong-world rate of 22/48 (0.458) was suspicious. Another session identified the root cause:
the binary hue witness used in H1 was a two-candidate scorer. If an output image had a third color
(neither target nor distractor), the binary scorer could round it to either — inflating wrong-world
hits. The fix: a **five-color joint witness** requiring both left AND right objects to match their
specific palette colors exactly.

H2 rescored the saved H1 images and ran 16 new arms × 48 instances (768 decoded images) with the
corrected witness.

| H1 arm | Old binary witness | Full-palette joint witness |
|---|---|---|
| full20_clean_graft | 46/48 | 41/48 |
| wrong_token_full20 | 12/48 | 7/48 |
| wrong_world_full20 | 22/48 | **1/48** |
| all_but_{8,11} | 5/48 | 5/48 |

The wrong-world failure was mostly a **scoring artifact**. Under the strict five-color witness,
wrong-world drops to 1/48 — well below the 4/48 ceiling. The restoration payload IS semantically
specific: unrelated donor K/V does NOT restore the correct binding.

Wrong-token remains at 7/48 (above 4/48 ceiling). The payload is not fully position-specific.

Native lesion (zeroing {8,11} vs {6,10}): clean 44/48 vs 42/48, corrupt 40/48 vs 39/48. Both
paired bootstrap intervals include zero. The 20-block all-site lesion dropped clean from 43→20 and
corrupt from 40→14. The route IS necessary in aggregate — but no small coalition is preferentially
so.

Verdict: **SEMANTIC_QUORUM_NOT_SUPPORTED.** The payload is semantic. The route is distributed. There
is no native quorum.

### ~15:00 Aug 1 — H3: native semantic patch (single-block scan)

H1 and H2 tested the G4b candidates ({8,11}) against matched controls. Maybe the wrong candidates
were selected. H3 scanned ALL 20 single-stream blocks individually — patch one clean block into the
corrupt run (forward direction) and one corrupt block into the clean run (reverse direction).

**Forward direction** (corrupt→clean single-block patches): every block holds the corrupt joint rate
at 0.750–0.833 against a 0.833 baseline. No single block flips binding when repaired alone.

**Reverse direction** (clean→corrupt single-block patches): every block holds the clean joint rate at
0.875–0.917 against a 0.896 baseline. No single block breaks binding when corrupted alone.

The most important result: **the native block ranking is completely different from the graft ranking.**

| Rank | Native candidate (H3 scan) | Graft kingmaker (G4b/gate fit) |
|---|---|---|
| 1 | block 14 (rank-score 4) | block 8 (29.6% weight) |
| 2 | block 13 (rank-score 4) | block 4 (9.2% weight) |
| 3 | block 11 (rank-score 6) | block 11 (7.3% weight) |
| 4 | block 7 (rank-score 8) | block 14 (6.7% weight) |
| ... | ... | ... |
| 12 | **block 8** (rank-score 16) | — |

Block 8 — the graft kingmaker, the sigmoid's dominant weight, the block whose removal crashed
restoration from 1.0→0.188 — ranks **12th** in native causal effect. The gate model describes
which blocks ACCEPT grafts best. It does not describe which blocks the model USES most.

Controls: scrambled/wrong-token/wrong-world at core = baseline. No semantic signal in
single-block corrupted patches.

Verdict: **NATIVE_CANDIDATE_SCAN_COMPLETE.** Top native candidates identified as blocks 13 and 14.
Passed to H4 for confirmatory testing.

### ~16:00 Aug 1 — H4: native carrier confirmation

Confirmatory run for H3's top candidates. Blocks {13,14} tested as a native carrier pair against
matched controls {6,10}. Scrambled, wrong-token, and wrong-world controls at the candidate pair.
Preregistered threshold: ≥10/48 disruption advantage over matched controls on the joint witness.

**Result: zero flips.** Not one arm — not candidate, not control, not scrambled — produced a
single joint-witness binding flip. Neither patching clean→corrupt nor corrupt→clean at blocks
{13,14} crosses the categorical threshold.

Margin effects are measurable (1–2.5° mean hue shift) and directionally consistent — blocks
{13,14} do move the output slightly more than matched controls. But "slightly more" is 2° on a
103° baseline margin. The binding computation does not concentrate enough at any pair of blocks
for a two-site patch to flip it.

Even the full pair {13,14} together only drops clean_joint from 0.875 to 0.771 — a degradation
but never a flip.

Verdict: **NATIVE_CARRIER_NOT_CONFIRMED** for the pair {13,14}. However, an independent
confirmatory run (documented in
[[2026-08-01-block-13-native-carrier-not-quorum|Block 13: Native Carrier, Not Quorum]])
established that **block 13 alone** IS a reproducible native semantic carrier: margin +1.95°
[+1.27, +2.69], clearing all preregistered contrasts vs matched and same-site controls. Block 14
did NOT confirm (CI crosses zero). But zero exact endpoint flips occurred (0/48 both directions) —
block 13 is a carrier without being a quorum.

This completes the three-way dissociation:
- **Block 8**: graft kingmaker (29.6% sigmoid weight), native rank 12
- **Block 13**: native carrier (margin +1.95°), but zero endpoint flips
- **No block or pair**: sufficient to flip binding categorically

The computation is genuinely distributed. The sharp threshold from G4/G4b is a property of the
graft intervention (you need enough clean blocks to overwhelm the corrupt residual), not a property
of native mechanism locality.

## H5 addendum: distributed continuous closure, not a compact endpoint circuit

The next assay widened the native exchange around block 13 on a fresh workload instead of
repeating the single-block scan. H5 ran 27 arms × 48 paired instances with S1, S2, S4, S8, full20,
matched native lesions, controls, and early/late block-13 windows. All technical gates passed and
all arm images passed visual audit.

The continuous native binding-margin effect increased across the sets, but the exact witness
separated the claims. S1/S2/S4 produced no reliable endpoint switches; S8 produced 1/48 forward
and 0/48 reverse switches; full20 produced 38/48 forward and 39/48 reverse. The per-instance
route analysis shows that the dominant continuous jump is S8→full20: +192.1990 forward and
+197.4907 reverse margin points. Thus H5 supports a distributed native carrier trajectory and
full-route behavioral quotient, not a compact native quorum.

Native lesions were selectively disruptive at the continuous margin relative to matched lesions,
and S4 beat wrong-token, wrong-world, and norm-matched scrambled controls. These results strengthen
the carrier claim without converting continuous necessity into discrete endpoint necessity. The
current follow-up is the graded H6 quotient-dose assay, which interpolates native/donor K/V state
at S4, S8, and full20 and tests K-only versus V-only endpoint effects.

## The dissociation: intervention susceptibility ≠ native mechanism

The most important finding of the full arc is not a specific block number. It is the **measured
dissociation** between two rankings that interpretability work often conflates:

1. **Intervention susceptibility**: which blocks are good targets for injecting new information?
   Answer: block 8 is dominant, with an additive gate (R²=0.970) and a sharp threshold at ~14
   blocks. This is real, portable, and predictive.

2. **Native importance**: which blocks does the model rely on for color binding in its natural
   forward pass? Answer: we could not identify any small coalition. Single-block and two-block
   patches — at every one of 20 blocks, and at the top-ranked pair — never flip binding. The
   computation is distributed below the resolution of pairwise intervention.

The gate-compression model (block 8 = 29.6%) is a useful tool for PREDICTING GRAFT OUTCOMES. It
is not a map of the model's native binding mechanism. The two are different objects, measured by
different experiments, with different rankings.

## Parallel context: the six-track BFL program

The arbitration harness was one of several parallel investigations into the FLUX model family,
documented in
[[2026-08-01-001500-opening-the-black-forest-what-six-parallel-tracks-taught-us-about-flux|Opening
the Black Forest]]. Key results from the other tracks that inform this arc:

| Track | Question | Verdict |
|---|---|---|
| T1 Lineage | Is FLUX.2 detectably related to the Schnell witness under the residual-facing instrument? | **NO DETECTABLE MATCH** — 1,425 cells at null; private ancestry open |
| T2 Counting | Is joint.4 a necessary counting bottleneck? | **NOT_VERIFIED** — seed-gated redundant routing |
| T3 Distillation | Does step-distillation erase representations? | **NO** — preserves from step 0 |
| T4 KV finetune | Where are 9B→9B-KV weight deltas largest? | **Q/K-HEAVY STATIC MAP** — cache causality open |
| T5 Retrodiction | Do weight statics predict mechanism location? | **CLEAN NULL** |
| T6 Typography | Are text rendering failures uniform? | **NO** — lexically gated |

The T2 result (counting circuits show redundant routing with 60% wrong-site rescue) parallels the
arbitration finding: interventions at a single "correct" site don't reliably control behavior
because the model routes around them. Redundant routing and distributed computation are the same
phenomenon seen from two instruments.

The T6 result (typography success is lexically gated — "open" renders at 1.0, "exit" at 0.0)
connects to the FLUX.1 conditioner failure: the text encoder determines what compositional
structure the denoiser receives. Conditioner capacity gates downstream mechanism.

## What the instrument measured (updated)

Across the full arc including H2–H8, the instrument produced **12,000+ generated images**, 53
discovery arms, 17 H1 replication arms, 16 H2 semantic arms, 50 H3 scan arms, 21 H4 confirmation
arms, 27 H5 closure arms, 41 H6 dose arms, 41 H7 held-out arms, and 35 H8 temporal arms — all
with per-block resolution, SHA256 custody chains, and frozen interpretation thresholds.

**What is real:**
- K/V instrumentation at single-stream blocks is causally live and reversible
- Clean K/V restoration has a portable threshold (replicates on held-out data)
- The restoration payload IS semantically specific (wrong-world = 1/48 under strict witness)
- Block 8 is the dominant graft target (29.6% of gate weight, graft-susceptibility kingmaker)
- The gate is additive and compresses to a sigmoid with R²=0.970
- The threshold requires ~14+ blocks with the right composition
- Block 13 is an independently confirmed native continuous carrier inside a distributed coalition;
  full20 exchange restores the exact witness on the H5 workload
- H8 supports distributed temporal accumulation: the full20 all-step route beats every single-step
  graft in both directions, and the route is not late-call-only

**What is not established:**
- That any small block coalition is endpoint-sufficient (H3 scan: no single block flips; H4: no
  pair flips; H5 compact sets do not reliably transfer the exact endpoint)
- That the graft ranking equals the native ranking (block 8 = graft rank 1, native rank 12)
- That the FLUX pattern replicates the Qwen pattern at the mechanism level
- That FLUX.1-schnell supports this workload at all
- That the full20 endpoint closure identifies a compact semantic quorum rather than cumulative
  distributed route exposure
- That native-vs-control specificity is workload-independent; H7 and H8 keep this boundary open

## What this means for the larger program

The arbitration microscope was originally built for Qwen. Porting it to FLUX.2-klein-4B was meant
to test universality. What we got instead was a deeper lesson: **the intervention tool and the
native mechanism are different objects.**

The graft instrument measures which blocks are effective targets for K/V injection. This is useful —
it predicts intervention outcomes with R²=0.970. But it does not map the model's native binding
computation. Four follow-up experiments (H2, H3, H4, H5) now define this dissociation:

- H2 corrected the witness and showed the payload IS semantic — wrong-world is genuinely low (1/48)
- H3 scanned all 20 blocks and showed the native ranking differs from the graft ranking
- H4 confirmed that even the top native candidates cannot flip binding as a pair
- H5 confirmed a distributed native continuous carrier and showed that exact endpoint recovery is
  concentrated in the full20 exchange rather than S4/S8 compact sets

The binding computation in FLUX.2-klein-4B is distributed below the resolution of pairwise K/V
intervention. No 2-block, and possibly no small-coalition, perturbation is sufficient to flip
color binding in native forward passes. The sharp threshold from G4/G4b describes how many clean
blocks you need to overwhelm the corrupt residual in a graft — a property of the intervention,
not a property of the model's native information routing.

### H6: the native quotient is graded, not compact

The H6 41-arm dose assay tested that remaining distinction directly. Joint K/V state was
interpolated at four strengths across S4, S8, and full20 on a fresh 48-instance workload, with
K-only/V-only decompositions and wrong-token, wrong-world, and norm-matched scrambled S4 controls.

The result supports an assay-relative graded native quotient. All alpha-1 joint continuous-margin
effects were positive, and the native S4 arm beat every control with positive paired confidence
intervals. But only three of six dose curves were monotone. The exact endpoint counts remained
small for S4/S8 and rose sharply for full20: forward clean-endpoint counts at alpha .25/.50/.75/1
were `0/0/1/1`, `0/1/2/3`, and `1/7/38/40`; reverse corrupt-endpoint counts were
`0/0/1/1`, `0/1/1/2`, and `0/6/35/41`.

The K/V split adds another constraint: K-only never produced an exact endpoint transfer, V-only
produced partial full-route transfers (`30/48` forward, `29/48` reverse), and the joint full20
route remained stronger (`40/48`, `41/48`). The evidence is coordinated native state, not a
single magic channel. The complete result and visual audit are in
[[2026-08-01-h6-native-quotient-dose]].

### H7: the route replicated, native specificity did not fully replicate

H7 repeated the 41-arm H6 quotient-dose protocol on a fresh 48-instance workload and fresh
latent seeds while holding the model, conditioner, route sets, scorer, and render budget fixed.
All technical custody gates passed. The distributed route replicated: full20 endpoint counts were
`0/4/36/41` forward and `1/10/35/41` reverse at alpha `.25/.50/.75/1.00`, while compact S4/S8
endpoint transfer remained weak. Three of six dose curves were monotone, including both full20
directions, and all alpha-1 joint continuous-margin effects were positive.

The qualification is the fresh specificity control. Native-vs-wrong-token was `+2.765`, 95% CI
`[+1.316, +4.828]`; native-vs-scrambled was `+3.783`, 95% CI `[+1.915, +6.142]`; native-vs-
wrong-world was `+2.558`, 95% CI `[-0.924, +5.980]`. The pre-set wrong-world confidence-bound
gate therefore failed. All control images were valid and remained at the corrupt endpoint, so
this is a workload-sensitive statistical limitation, not a render failure.

H7 strengthens the claim that FLUX.2-klein-4B has a held-out distributed denoiser route, while
narrowing the claim that the route is specifically native relative to every matched control.
The arc is resolved as a graded route, not as a compact quorum. H8 then localized the temporal
behavior on a repaired fresh workload: the full20 all-step graft exceeded every corresponding
single-step graft with positive lower confidence bounds in both directions, while the
late-minus-early contrast was negative. The prior H8 seed `20260809` was rejected by the
collision-safe donor preflight before any science arm; repaired seed `20260810` completed all
35 × 48 renders successfully.

See [[2026-08-01-h7-heldout-quotient-replication|The Route Replicated; Native Specificity Did
Not]] for the complete table and visual audit.

### H8: distributed temporal accumulation

H8 used FLUX.2-klein-4B revision `e7b7dc27f91deacad38e78976d1f2b499d76a294`, the admitted Qwen3
conditioner, four denoising steps, and 48 fresh instances. Its primary full20 all-step margin
effects were `+179.565 [157.329, 201.441]` forward and `+182.422 [160.293, 204.882]` reverse.
The all-step-minus-single-step differences were positive for every step, and all-step also
exceeded the sum of the single-step effects. The late-minus-early contrast was
`−24.621 [−35.398, −15.126]` forward and `−23.726 [−33.640, −15.179]` reverse.

The fresh H8 wrong-token, wrong-world, and scrambled controls also had positive continuous
margins (`+4.951`, `+5.300`, and `+5.939`, respectively), so this experiment resolves the
temporal route while preserving the native-specificity qualification. It does not prove a
universal semantic quorum. The full visual audit covered all 1,680 renders, three comparison
sheets, and 33 decisive full-resolution samples; the images were coherent and showed visible,
sometimes attribute-selective full20 movement rather than a renderer artifact.

See [[2026-08-01-h8-temporal-route-localization|The Route Accumulates Across Time]] for the full
table, endpoint witness, and artifact links.

### H9: five controls held; the reverse wrong-world arm needs repair

H9 powered the native-versus-control question with 96 instances and three matched S4 controls in
both directions. The stored arithmetic, image hashes, route accounting, full20 benchmark, and all
six nominal bootstrap contrasts reproduce. An adversarial source audit then found that the reverse
wrong-world arm was not the control the design specified: it reused the forward map, producing
45/96 donor-color collisions, including 20 direct matches to the reverse target.

Five contrasts remain admissible—forward wrong-token, wrong-world, and scrambled plus reverse
wrong-token and scrambled. Their conservative six-family lower bounds are all positive; the
smallest is `+2.345`. The nominal reverse wrong-world mean (`+6.171`) is retained only as a
contaminated trend. It cannot close the bilateral family.

The cumulative claim is therefore an assay-relative distributed K/V intervention route: it is
spatially broad, accumulates over denoising calls, and becomes endpoint-reliable at full20 coverage.
It is not yet a six-control specificity closure, an endogenous-necessity result, a compact quorum,
or a portable cross-model circuit. Separate directional maps are implemented, the CPU suite passes
`21/21`, and frozen H9R job `job-9bd1dd958932` is queued. Queued work is not evidence. See
[[2026-08-01-h9-native-specificity-replication|H9 After Adversarial Review: Five Controls Held, One Needs Repair]].

The FLUX.1 failure reinforces a different constraint: the conditioner determines what compositional
structure the denoiser can work with. CLIP+T5 cannot compose two-object color binding that
Qwen3-4B handles trivially. Any future mechanistic probe must gate on conditioner capacity first.

### Conditioner cartography: the bottleneck was reconstruction, not encoding

A follow-up experiment loaded all three text encoders (Qwen3-4B, T5-XXL, CLIP) on CPU and profiled
their per-layer representations across 16 binding prompts. The result overturns the obvious
hypothesis: CLIP actually has the *strongest* color separation in representation space (cos gap 0.222
vs Qwen3's 0.073). All three encoders separate color from object internally.

The real difference: all three absorb color-token norms into distributed context mid-network (ratio
crashes to 0.07–0.16), but only Qwen3 **reconstructs** — color/noncolor norm ratio recovers from
0.088 (layer 7) to 0.936 (final layer), with effective rank growing from 1.4 to 10.1. T5 stays at
~0.1 through its final layers; CLIP reaches 0.269. The denoiser gets high-rank, position-rich
binding structure from Qwen3 and low-rank smeared representations from CLIP/T5.

See [[2026-08-01-conditioner-cartography-reconstruction-bottleneck|The Binding Bottleneck Was
Reconstruction, Not Encoding]] for full diagnostics.

## The instrument

The harness is ~4,000 lines of Python across 12 source files and 6 test files, purpose-built for
this arc:

| Component | Lines | Function |
|---|---|---|
| `common.py` | ~680 | Two-stage pipeline, determinism pinning, layout gates, certified adapter |
| `workload.py` | ~200 | Seeded pair generator, hue separation, span location |
| `mediation_probe.py` | ~350 | 26-site uniform probe (embed + double + single), three tensor layouts |
| `kv_probe.py` | ~300 | K/V capture/graft with SHA256 custody and BTHF validation |
| `run_g0_parity.py` | ~360 | 11-gate instrumentation check |
| `run_g1_admission.py` | ~330 | Behavioral admission with hue witness |
| `run_g2b_mediation.py` | ~250 | Double/single bisection |
| `run_g4_dose.py` | ~300 | 23-arm dose-response |
| `run_g4b_release_lattice.py` | ~340 | 30-arm necessity/sufficiency/pair probes |
| `fit_klein_gate.py` | ~200 | Sigmoid-additive gate compression |
| `run_h1_heldout_native_replication.py` | ~1040 | 17-arm held-out + native swap |
| `run_h2_semantic_quorum.py` | ~800 | 16-arm semantic witness + role swap |
| `run_h3_native_semantic_patch.py` | ~900 | 50-arm all-block native scan |
| `run_h4_native_carrier_confirmation.py` | ~700 | 21-arm confirmatory pair test |

Every hook write is verified by SHA256 read-back. Every gate script records its numerics state,
model layout, and evidence chain. The harness was adapted for FLUX.1-schnell by changing text
encoding (CLIP+T5 dual), probe topology (19 double blocks), bias gate polarity, and memory strategy
(sequential CPU offload for the 12B transformer).

## Artifacts

- Experiment directory: `experiments/2026-07-31-211500-flux-arbitration-harness/`
- FLUX.1 adaptation: `experiments/2026-08-01-flux1-schnell-arbitration/`
- G4 dose response: `outputs/g4-dose.v1.json` (23 arms)
- G4b release lattice: `outputs/g4b-release-lattice.v1.json` (30 arms)
- Gate compression: `outputs/klein-gate-fit.v1.json` (R²=0.970)
- H1 held-out replication: `outputs/h1-heldout-native-replication.v1.json` (17 arms × 48 instances)
- H2 semantic quorum: `outputs/h2-semantic-quorum/h2-semantic-quorum.v1.json` (16 arms × 48 instances)
- H3 native scan: `outputs/h3-native-semantic-patch/h3-native-semantic-patch.v1.json` (50 arms)
- H4 carrier confirmation: `outputs/h4-native-carrier-confirmation/h4-native-carrier-confirmation.v1.json` (21 arms)
- H5 circuit closure: `outputs/h5-native-circuit-closure/h5-native-circuit-closure.v1.json` (27 arms)
- H5 visual audit and route analysis: `outputs/h5-native-circuit-closure/H5_VISUAL_AUDIT.md`,
  `outputs/h5-native-circuit-closure/H5_DISTRIBUTED_ROUTE_ANALYSIS.md`
- H6 quotient-dose design: `H6_NATIVE_QUOTIENT_DOSE_DESIGN.md`
- H6 quotient-dose result and visual audit: `outputs/h6-native-quotient-dose/h6-native-quotient-dose.v1.json`,
  `outputs/h6-native-quotient-dose/H6_VISUAL_AUDIT.md`
- H7 held-out quotient replication: `outputs/h7-heldout-quotient-dose/h7-heldout-quotient-dose.v1.json`,
  `outputs/h7-heldout-quotient-dose/H7_VISUAL_AUDIT.md`
- H8 temporal localization design: `H8_TEMPORAL_ROUTE_LOCALIZATION_DESIGN.md`
- H8 temporal localization result and visual audit:
  `outputs/h8-temporal-route-localization/h8-temporal-route-localization.v1.json`,
  `outputs/h8-temporal-route-localization/H8_VISUAL_AUDIT.md`
- H9 historical specificity run: H9_SPECIFICITY_REPLICATION_DESIGN.md, immutable report
  outputs/h9-specificity-replication/h9-specificity-replication.v1.json, visual audit
  outputs/h9-specificity-replication/H9_VISUAL_AUDIT.md; job-747ae0c09e49 succeeded; automatic
  bilateral verdict superseded by the reverse-control audit
- H9R direction-safe repair: H9_REVERSE_WRONG_WORLD_REPAIR_DESIGN.md; job-9bd1dd958932 queued
- Owner adjudication: ../2026-08-02-bfl-three-claims/FINAL_ADJUDICATION.md
- Visual audit directories: `outputs/h1-heldout-native/visual-audit/`, `outputs/h2-semantic-quorum/visual-audit/`, `outputs/h3-native-semantic-patch/visual-audit/`, `outputs/h4-native-carrier-confirmation/visual-audit/`
- Design review: `DESIGN_REVIEW.md` (frozen before H1 execution)
- H2 design: `H2_SEMANTIC_QUORUM_DESIGN.md`
- Conditioner cartography: `experiments/2026-08-01-conditioner-cartography/outputs/conditioner-cartography.v1.json` (3 encoders × all layers)

## Related posts

- [[2026-08-01-013000-the-diffusion-transformer-had-the-same-quorum|The Diffusion Transformer Had the Same Quorum]] — the discovery post (now carries an erratum)
- [[2026-08-01-032700-the-restoration-was-real-the-quorum-was-not-proven|The Restoration Was Real; the Quorum Was Not Proven]] — the held-out correction
- [[2026-08-01-142952-the-payload-was-semantic-the-quorum-was-not-native|The Payload Was Semantic; the Quorum Was Not Native]] — H2 full-palette reanalysis and native lesion
- [[2026-08-01-h5-distributed-native-circuit-closure|The Native Circuit Closed Only as a Distributed Trajectory]] — H5 continuous closure and exact-endpoint boundary
- [[2026-08-01-h6-native-quotient-dose|The Native Quotient Has a Dose Curve, Not a Compact Quorum]] — H6 graded route, K/V decomposition, and endpoint boundary
- [[2026-08-01-h7-heldout-quotient-replication|The Route Replicated; Native Specificity Did Not]] — H7 held-out route replication and specificity boundary
- [[2026-08-01-h8-temporal-route-localization|The Route Accumulates Across Time]] — H8 temporal route localization and distributed accumulation
- [[2026-08-01-h9-native-specificity-replication|H9 After Adversarial Review: Five Controls Held, One Needs Repair]] — corrected H9 status and frozen repair
- [[2026-08-01-001500-opening-the-black-forest-what-six-parallel-tracks-taught-us-about-flux|Opening the Black Forest: What Six Parallel Tracks Taught Us About FLUX]] — the six-track BFL program
- [[2026-08-01-020000-the-plane-was-the-shadow-of-a-moving-frame|The Plane Was the Shadow of a Moving Frame]] — why the response is ~8–16 dimensional, not a scalar plane
- [[2026-07-31-212627-what-we-know-about-the-black-forest-models-a-data-driven-report|What We Know About the Black Forest Models]] — FLUX model family data report
- [[2026-07-31-205147-the-gate-survived-review-the-bias-did-not-and-flux-repeated-the-cliff|The Gate Survived Review; the Bias Did Not]] — the QK-RMSNorm cliff finding
- [[2026-07-31-145130-the-conditioners-were-stock-checkpoints|The Conditioners Were Stock Checkpoints]] — BFL ships unmodified text encoders
- [[2026-07-31-140500-the-gate-was-eleven-numbers-and-the-bias-knew-them|The Gate Was Eleven Numbers and the Bias Knew Them]] — the Qwen arbitration microscope this ports from
- [[2026-08-01-conditioner-cartography-reconstruction-bottleneck|The Binding Bottleneck Was Reconstruction, Not Encoding]] — Qwen3 reconstructs binding at output; CLIP/T5 don't
