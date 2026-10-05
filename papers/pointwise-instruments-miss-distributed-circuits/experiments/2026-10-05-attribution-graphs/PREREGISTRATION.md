# Preregistration — circuit-tracer native edge test on Gemma-2-2B

This file is committed **before** the measurement run. It freezes the prompt panel, the
admission rule, the decision rule, the selection and intervention parameters, the graph
prediction modes, and the agreement categories. Nothing below is changed after results are
seen; the only post-run edits to this directory are the scrubbed result files
(`summary.json`, `bundles/`, `README.md`), never this plan.

## Frozen panel

- File: [`panel.json`](panel.json)
- `sha256(panel.json)` = **`f787b9cf0c1d873a88fc3e5d657e1f06fb85936ec632227dd454f4e2dd98d0b6`**
- 56 candidate prompts across 7 task families (8 each), modeled on the example types in
  Anthropic's attribution-graphs work:
  `multi_hop_factual`, `capitals`, `antonyms`, `translation`, `acronym_abbreviation`,
  `arithmetic_sequence`, `category_rhyme`.

Recompute the hash to confirm the panel was not altered:

```bash
python3 -c "import hashlib; print(hashlib.sha256(open('experiments/circuit_tracer/panel.json','rb').read()).hexdigest())"
# -> f787b9cf0c1d873a88fc3e5d657e1f06fb85936ec632227dd454f4e2dd98d0b6
```

## Admission rule (frozen)

A candidate is **admitted** iff the native `google/gemma-2-2b` greedy top-1 next token (the
fp32 reference forward) equals the first token of its `answer` string. The replacement
model's clean (no-op) top-1 is used **only** as a pre-filter to avoid building an attribution
graph for a candidate that will not be admitted; the admission of record is the fp32 native
top-1. Candidates that fail admission are **recorded** (with the top-1 they actually produced)
and **dropped** — they are never replaced, re-phrased, or supplemented after the fact. The
candidate panel is over-provisioned (56) precisely so that admission failures do not create
pressure to swap prompts in.

## Decision rule (frozen; the existing `default_edge_rule`)

```
metric = consumer_logprob_drop = logprob(target|clean) - logprob(target|intervention)   [nats]
native_necessary     iff drop >= 0.50
native_effect_absent iff drop <= 0.10
inconclusive         otherwise
```

These thresholds are the shipped `saturn_pub.interop.circuit_tracer.default_edge_rule`
values and are **not** tuned after seeing results.

## Selection, interventions, and prediction modes (frozen)

- `top_k = 20` feature nodes per prompt, ranked by circuit-tracer's own
  `compute_node_influence`.
- Single-feature intervention: zero-ablate each selected feature; native necessity graded by
  the rule above; `graph_vs_native` compared to the graph's predicted drop in the
  **frozen-attention iterative** mode (the circuit-tracer default).
- Group interventions (both, per prompt): **joint zero-ablation** (`multiplier = 0`) and
  **−2× steering** (`multiplier = -2`) of the whole top-k set.
- Graph-predicted group drops are computed under **all three** `feature_intervention` modes:
  1. `frozen_attention_iterative` — `freeze_attention=True, constrained_layers=None` (the
     circuit-tracer default; the mode its own intervention demos use).
  2. `unconstrained_iterative` — `freeze_attention=False, constrained_layers=None` (attention
     and LayerNorm recompute).
  3. `direct_effects` — `constrained_layers=range(0, n_layers)` (freeze attention + LayerNorm
     denominators + all MLPs; the fully linearized regime the attribution **graph edges**
     themselves are computed in).

## Agreement categories (frozen; from `classify_graph_vs_native`)

`agree_small` (graph & native both ≤ 0.10), `agree_large` (both ≥ 0.50), `invert` (graph
≥ 0.50 but native ≤ 0.10), `mixed` (anything else with a prediction), `no_graph_prediction`.

## Reported statistics (frozen)

- Agreement rate (`agree_small` + `agree_large`) over admitted single-feature edges, with a
  percentile bootstrap **95% CI** (10 000 resamples, seed 0, resampling edges), reported
  overall and per task family.
- Inversion rate and `mixed` rate with the same bootstrap.
- Group-intervention agreement per intervention type, with bootstrap over prompts.
- Transcoder error-node influence-share distribution (min / median / max over admitted
  prompts).

## Adapter validation (frozen protocol, same run)

Before any edge test, the native Gemma-2 `DecoderAdapter` is validated on the real fp32
weights: stepped (layer-by-layer) logits vs a native full forward (max-abs Δ), 16-token
greedy decode equals `model.generate` greedy, and a mid-layer cut replays exactly in a fresh
process. Separately, `residency="streamed"` vs `"resident"` is checked on the real weights
(16-token greedy bit-exact, max logit Δ, mid-layer fresh-process replay, peak VRAM).

## Amendment 2026-10-05 (implementation fix; plan unchanged)

The first run's native interventions read circuit-tracer's `activation_values` by selected-node
position, but that array is aligned with `active_features`; on 44 of 50 admitted prompts every
native ablation and −2× steer (and the −2× graph prediction) used another feature's activation.
The selector was fixed (`activation_values[selected_features[i]]`, misaligned graphs refused,
regression tests added) and the whole panel rerun once under this unchanged plan: same frozen
panel and sha256, admission rule, `top_k`, thresholds, prediction modes, and statistics. The
first run's results are withdrawn; its job ids are listed in the README for the record. No
prompt, threshold, or rule was changed after seeing the corrected results.
