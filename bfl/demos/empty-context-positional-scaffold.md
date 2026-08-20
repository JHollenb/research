---
title: "The Empty-Context Positional Scaffold and Tone Bank"
type: experiment-report
status: native-consumer-causal-trend
rank_in_bfl_survey: 10
model: "FLUX.2 Klein 4B with Qwen3 context"
tags: [bfl, flux, qwen3, context, positional-encoding, causal-intervention, tone-bank]
---

# The Empty-Context Positional Scaffold and Tone Bank

> [!summary]
> In FLUX.2 Klein 4B, an apparently empty maskless context is consumed as positional state rather than ignored padding. A 3.5%-occupancy intervention—zeroing 18 active-adjacent rows in a `[1,512,7680]` Qwen3 context—changes final RGB MAD by 41.9 and 53.2 across two seeds, comparable to or larger than whole-prompt swaps of 43.5 and 31.7. Matched-position controls show that 18 active tokens cost 42.7 and 55.5, while 205 active tokens cost only 16.4 and 22.1. The evidence supports a positional tone-bank/scaffold mechanism for this maskless consumer, not a claim that inactive rows are semantically empty in every architecture.

## Research question

Transformer inputs are often padded to a fixed length, and analysis commonly treats the padded rows as inert. This experiment asks whether that assumption holds for the native Qwen3 conditioning path used by FLUX.2 Klein 4B when no attention mask is supplied. The specific question is whether nominally empty rows still carry positional or contextual state that later image generation consumes.

Three explanations are compared. If padding is inert, zeroing inactive or active-adjacent rows should have little effect. If row identity matters, a small intervention at particular positions should be damaging even when token occupancy is low. If the effect is merely proportional to the number of active tokens, a larger active-token intervention should be more damaging than a smaller one at matched positions. The experiment includes substitution controls and per-step windows to distinguish these possibilities.

## Specimen and representation

The specimen is FLUX.2 Klein 4B at 256×256 resolution and four denoising steps. Its Qwen3 context has shape `[1,512,7680]` and is consumed without an attention mask. Approximately 28 rows are tokenizer-active and approximately 494 are nominally inactive. The intervention does not remove rows from the tensor; it zeros or substitutes selected row values and then sends the full fixed-length context through the unchanged native consumer.

The primary measure is final RGB mean absolute deviation (MAD) from the unmodified native output. Two independent seeds are used for the main zeroing panel. A matched-position control compares 18 active-token positions with 205 active-token positions at positions selected to control for row location. A substitution control replaces empty-prompt padding with other prompt padding rather than zeroing it. A per-step window records how much damage is attributable to state written at each denoising step.

## Results

Zeroing 18 active-adjacent rows, only 3.5% of nominal context occupancy, changes final RGB MAD by 41.9 and 53.2 across the two seeds. Whole-prompt swaps change MAD by 43.5 and 31.7. Thus a very small row intervention can rival or exceed a full prompt change under the native consumer.

The matched-position control rules out a simple “more active rows means more damage” explanation. Zeroing 18 active-token rows produces MAD 42.7 and 55.5, whereas zeroing 205 active-token rows at matched positions produces only 16.4 and 22.1. Position and local contextual state therefore matter more than raw row count in this panel.

Substitution is asymmetric. Replacing empty-prompt padding with other empty-prompt padding is nearly free, with MAD 12.5–20.2. Replacing it with unrelated prompt padding is worse than zeroing, with MAD 68.6 and 76.5. The row contents are not interchangeable merely because the tokenizer labels them as padding-like.

The per-step windows show approximately 80–89% of the damage in step 0. Later clean steps inherit the corrupted state rather than independently creating the effect. A Fourier write analysis is consistent with a low-rank positional tone bank: phase carries token-address information, while later blocks echo and consume that state.

[Context scaffold intervention evidence](../artifacts/empty-context-positional-scaffold/report.json)

## Mechanistic interpretation

The working model is that the fixed-length Qwen3 context contains a positional scaffold whose row values are available to downstream attention even when the rows are nominally inactive. The scaffold can be viewed as a tone bank: structured phase and low-rank components identify positions, and later computation transports or amplifies those distinctions. “Empty” therefore means semantically unfilled by a user token, not numerically absent from the computation.

This interpretation explains the three strongest observations together: small active-adjacent row edits are large, more active rows are not automatically more damaging, and unrelated padding substitution can be worse than zeroing. It is still an inference from intervention patterns. The experiment does not isolate a single Fourier basis vector or prove that a particular positional feature is the only causal carrier.

## Controls and limitations

The matched-position row-count control tests whether occupancy alone explains the result. Empty-to-empty substitution tests whether all padding states are equivalent. Whole-prompt swaps provide a scale reference. Per-step windows test when the perturbation enters the image trajectory. Using the native final consumer avoids mistaking a hidden-state difference for an image-level effect.

The panel uses one model family, one resolution, four steps, two seeds, and a maskless input contract. Zeroing corrupts the fixed context; it does not demonstrate that physically removing rows would have the same effect. The numbers should not be extrapolated to masked transformers, other Qwen3 variants, or architectures that normalize or truncate padding differently.

## Claim status

**Observation:** nominally empty Qwen3 context rows can causally affect native FLUX.2 images, with position-specific and content-specific sensitivity.

**Convergent trend:** occupancy-matched row interventions, substitution asymmetry, and early-step damage all support a consumed positional scaffold.

**Working inference:** the maskless context behaves as a positional tone bank whose phase and row address are part of the downstream input contract.

**Terminal status:** bounded native-consumer causal trend for Klein 4B. It is not a universal statement about padding, masks, or positional encoding in other model families.

## Local proof bundle

The bundle contains the raw context-pad report and receipts plus the explanatory evidence:

- [context-pad report](../artifacts/empty-context-positional-scaffold/report.json)
- [context-pad receipt](../artifacts/empty-context-positional-scaffold/run-receipt.json)
- [tone-bank analysis](../artifacts/empty-context-positional-scaffold/2026-08-13-the-write-was-a-tone-bank-and-the-scaffold-was-an-echo.md)
- [bundle verifier](../artifacts/empty-context-positional-scaffold/verify.py)

Run `python ../artifacts/empty-context-positional-scaffold/verify.py` from this directory to verify the row, substitution, and per-step evidence.
