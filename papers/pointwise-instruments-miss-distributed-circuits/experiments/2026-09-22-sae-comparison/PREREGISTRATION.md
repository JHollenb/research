---
title: "Preregistration: SAE feature ablation vs. per-layer and whole-path interventions"
type: preregistration
status: frozen
frozen: 2026-09-22
tags: [preregistration, sparse-autoencoders, saelens, activation-patching]
---

# Preregistration: SAE feature ablation vs. per-layer and whole-path interventions

Frozen 2026-09-22 before any code for this experiment was written or run. Amendments are appended at the end with a date and reason; nothing above the amendments line changes after the first run.

## Question

When a standard sparse-autoencoder workflow (SAELens with public pretrained SAEs) is used to find the features that carry a prompt's subject into the model's answer, does it identify components whose ablation removes the behavior, and how does that compare with (a) replacing the subject token's key/value entries one layer at a time, (b) replacing them across layer ranges, and (c) replacing the subject token's residual stream at one layer?

## Models and SAEs

| model | weights | SAEs (SAELens release) | layers covered |
|---|---|---|---|
| Gemma-2-2B | `unsloth/gemma-2-2b` (ungated mirror of `google/gemma-2-2b`; record the commit and file SHA-256) | `gemma-scope-2b-pt-res-canonical`, width 16k, `layer_{L}/width_16k/canonical` | all 26 |
| GPT-2 small | `openai-community/gpt2` | `gpt2-small-res-jb` | all 12 (`blocks.{L}.hook_resid_pre`) |

The key/value and residual arms (below) also run, without SAEs, on SmolLM2-1.7B, Qwen2.5-0.5B, and Qwen2.5-1.5B, to replace the paper's original handful of prompts with a panel. Computation in fp32 throughout. Hook points for the SAE arms are the ones the SAEs were trained on.

## Prompts

Two behaviors, each with at least 24 items built from templates × subjects before any model is run:

- **identity:** "A photorealistic {subject} {pose} in {scene}. The animal in this picture is a" → answer is the subject's first token (e.g. " fox"). Subjects: at least 12 animals whose name is a single token in every tokenizer used; the candidate set for top-1 is the full subject list.
- **color:** "A {color} {object} on a {surface}. The color of the {object} is" → answer is the color's first token. Colors: at least 8 single-token colors; candidate set is the full color list.

The filler replaces the subject (or the color word) with a generic word ("creature" for identity, "plain" for color). Its key/value entries, residual states, and SAE latents are taken from the same prompt with the filler substituted, at the same token position (items where the substitution changes token count are excluded before running).

**Item admission (fixes the scene-prior confound).** An item is admitted only if, on the clean prompt, the answer is top-1 among candidates, and on the filler prompt the answer's log-probability is at least 1.0 nat lower than on the clean prompt. Admission is decided once, before any intervention arm is scored. The admitted count per model × behavior is reported; a cell with fewer than 12 admitted items is reported but not used for the decision rules.

## Arms

All arms intervene at the subject (or color-word) token position only, on the clean prompt, and score the change in log-probability of the answer (Δlp) plus whether the top-1 candidate changes.

- **KV-1:** replace that position's key and value entries with the filler's at a single layer L, for every L.
- **KV-range:** the same for the first half, the second half, and all layers.
- **Resid-1:** replace that position's residual stream with the filler's at a single layer L (input to block L), for every L.
- **SAE-k (single layer):** at layer L, encode the residual at the subject position, zero the top-k latents ranked by attribution (latent activation × gradient of the answer log-probability with respect to that latent), decode, and add back the SAE's reconstruction error so that only the chosen features change. k ∈ {1, 5, 20}. Every L.
- **SAE-swap (single layer):** replace the full SAE latent vector at the subject position with the filler's, keep the clean error term. Every L.
- **SAE-global:** rank all (layer, position, latent) triples over all layers and positions by the same attribution score, zero the top N simultaneously (errors kept), N ∈ {10, 50, 200}. This is the sparse-feature-circuit style of discovery.
- **Steering sufficiency:** on the filler prompt, add the decoder directions of the clean prompt's top-20 attributed latents at their clean activations at a single layer L; score the gain in the original answer's log-probability. Compare with writing the clean key/value entries into the filler prompt at a single layer and at all layers.

Every arm has a no-op control (hook installed, nothing changed; logits must match the unhooked run exactly in fp32) and, for the SAE arms, a random-feature control (k or N random active latents at the same layer or layers).

## Metrics and decision rules

The whole-path effect for an item is Δlp under KV-range(all). For each arm, report the median over admitted items of Δlp / whole-path Δlp ("fraction of path effect"), the top-1 flip rate, and 95% bootstrap intervals over items (10,000 resamples).

1. **Single-layer KV null (replication):** holds for a model × behavior if the best single layer's median fraction is below 0.25.
2. **SAE single-layer workflow finds a necessary component** if, at some layer, SAE-20 reaches a median fraction ≥ 0.5 or a flip rate ≥ 0.5.
3. **SAE global circuit is faithful** if SAE-global at N = 200 reaches a median fraction ≥ 0.5.
4. **Residual-stream bus:** Resid-1 at the best early layer reaching median fraction ≥ 0.5 is the predicted outcome (the paper already reports single-layer residual writes as sufficient); if it does not, that is reported as a contradiction of the paper.

## Predictions (stated so they can fail)

- Rule 1 holds for Gemma-2-2B, SmolLM2-1.7B, Qwen2.5-0.5B and Qwen2.5-1.5B. For GPT-2 small (124M, below the scale where the paper saw distributed storage) rule 1 may fail.
- Rule 4 holds: residual-stream interventions at an early layer act as a bus and remove most of the effect.
- Because SAE features live on the residual stream, SAE-swap at an early layer should inherit rule 4 and succeed; SAE-20 at a single layer is predicted to fall short of 0.5 because 20 features are a small part of a distributed code, but this is uncertain.
- No prediction is made for SAE-global.

Whatever the outcome, all rules are reported for every model × behavior, including those that contradict the predictions, and the paper's §5–6 will state the result as measured.

## Amendments

### 2026-09-22 — post-run code review (v2 rerun)

Two implementation defects were found in a code review AFTER the first (v1) run. The v1
outputs are kept for the record (`results/*.json`); a corrected rerun writes `*_v2.json`
outputs and `combined_summary_v2.json`. Reason: found in post-run code review, 2026-09-22.

1. **SAE-global ablation was non-propagating.** The v1 `sae_global_ablate` replaced the
   residual at *all* positions of each selected layer with `clean − (selected feature
   contributions)`, so each later layer's clamp overwrote the effect of upstream ablations
   and reset unselected positions to clean — the arm effectively measured only the last
   clamped layer. v2 replaces it with a propagating ablation: at each layer's SAE hook the
   *current* residual is encoded, and each selected `(position, latent)` is removed by
   subtracting `f_current[pos,lat]·W_dec[lat]` from that position only (error term and all
   other positions/latents untouched), so upstream ablations propagate. The random-feature
   control uses the same propagating scheme. v2 additionally reports, as a diagnostic, how
   the top-200 selected features distribute over positions (subject / answer-readout last
   position / other) and over layers.

2. **KV arms conflated two effects.** The v1 KV swap used a single full forward, so at
   layer L the subject token's own query (and every earlier query) also read the patched
   K/V, altering the subject's own residual stream from layer L onward (worst at L0). v2
   adds **isolated** KV variants: run the prefix through and including the subject token
   cleanly into a cache (subject stream intact at every layer), overwrite the subject
   position's K/V in that cache at layer L (or a layer range) with the filler's, then run
   only the suffix tokens and score the last position. The isolated no-op (same split, no
   overwrite) is compared to the unsplit clean logits; if not bit-exact in fp32 the max-abs
   difference is reported and the split no-op is used as the baseline for the isolated arms.
   v2 reports KV-1-isolated for every L, KV-range-isolated (first/second/all) and flip
   rates alongside the original arms (now labeled "in-forward"). Decision rule 1 is
   evaluated and reported on both variants; the **isolated** variant is primary.

No other part of the protocol (prompts, admission, SAE ids/hook points, other arms, metrics,
the four decision rules) changed.

### 2026-09-22 — scope reduction + TransformerLens replication (secondary)

Reason: user scope change during the v2 rerun; keep it efficient.

- **Scope reduced** for the v2 rerun to **gpt2, gemma2, qwen15** (the SmolLM2-1.7B and
  Qwen2.5-0.5B v1 results are kept as-is; their v2 jobs were cancelled).
- **TransformerLens replication (secondary, descriptive; no new decision rules).** Each model's
  v2 job additionally reruns arms through the standard community stack (TransformerLens
  `HookedTransformer` / SAELens `HookedSAETransformer`, fp32, no-processing weights so logits
  match Hugging Face). Loaded with `from_pretrained_no_processing` (gemma-2-2b via the ungated
  `unsloth/gemma-2-2b` weights with the identical config injected under the `google/gemma-2-2b`
  cache name, since TL resolves the config from the gated repo; TL version and processing flags
  recorded). Arms replicated: Resid-1 (`hook_resid_pre`/`post`), KV-1 in-forward
  (`hook_k`/`hook_v` at the subject position), KV-1 isolated (`TransformerLensKeyValueCache`,
  prefix then suffix), and SAE-k (attached SAE, ablating the same attributed latents as the HF
  arm). Reported descriptively: per-arm `max |Δlp_TL − Δlp_HF|` over items and whether the
  isolated-KV rule-1 and SAE-20 rule-2 verdicts agree between implementations. TL agreement is a
  descriptive check, not a decision rule. SAE-global is **not** replicated in TL (the propagating
  ablation needs all SAEs resident, which does not fit alongside the fp32 model on the 16 GB card);
  the HF propagating global with its random-feature control remains the reference.
- **Timing (secondary).** Wall-clock per intervention is recorded for full-recompute vs
  cached-prefix reuse, for both HF and TL (CUDA-synchronized, one warm-up), plus total job time.

### 2026-09-22 — SAE-global position-scope variants (secondary)

Reason: the gpt2 v2 SAE-global overshoots (N=200 removes ~9× the whole-path log-prob effect with
high flip rates), which indicates the top-N attributed features are dominated by non-subject
positions (context / answer-readout), making a "faithful" reading of rule 3 trivial rather than a
subject-store finding. To separate this, two extra SAE-global arms are added, each computed with
the same propagating ablation and each with its own position-matched random-feature control:
(a) **SAE-global-subject:** top-N by attribution restricted to the **subject** position across all
layers (the fair SAE analog of whole-path KV, which only touches the subject); (b)
**SAE-global-nonfinal:** top-N excluding the final (answer-readout) position. N ∈ {10, 50, 200}.
The position/layer distribution of the selected features is reported for all three scopes.
**Decision rule 3 is still evaluated on the original all-positions arm as preregistered;** the two
new arms are reported as secondary/descriptive only (no new decision rules). Applied to the v2
rerun of gpt2 and gemma2 (qwen15 has no public SAE).

### 2026-09-22 — TransformerLens cross-check limited to gpt2 (card constraint)

Reason: TransformerLens's `from_pretrained` transiently materializes a second fp32 copy of the
weights during its weight conversion, so gemma-2-2b (≈10.4 GB) and Qwen2.5-1.5B (≈6 GB) need two
copies at once, which does not fit alongside the run on the single 16 GB card (measured: gemma2 TL
peaked 15.2 GB, qwen15 TL 12.6 GB, both killed by the VRAM guard). The TL cross-check therefore
runs only on **gpt2** (HF vs TL agree to ≤1.5e-4 on every arm, matching rule-1-isolated and rule-2
verdicts, plus the timing comparison); gemma2 and qwen15 are rerun **without** the TL arm (HF
only), which still produces all primary/secondary arms (isolated KV, propagating SAE-global,
subject / non-final SAE-global). This is a hardware limitation of the cross-check, not of the
experiment; the gpt2 agreement already establishes the HF implementation matches the standard
TransformerLens/SAELens approach.
