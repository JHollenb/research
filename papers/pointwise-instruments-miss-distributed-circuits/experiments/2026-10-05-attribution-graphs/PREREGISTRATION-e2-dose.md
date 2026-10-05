# Preregistration — Track E2 "dose-groups" (circuit-tracer follow-up)

Frozen before the first full job. Track name: `e2-dose`. Model `google/gemma-2-2b`,
Gemma Scope per-layer transcoders (circuit-tracer set `"gemma"`), circuit-tracer git
`7f66876`, same 50-admitted preregistered panel as the flagship
(`panel.json` sha256 `f787b9cf0c1d873a88fc3e5d657e1f06fb85936ec632227dd454f4e2dd98d0b6`).
Decision rule frozen from `saturn_pub.interop.circuit_tracer.default_edge_rule`:
`drop >= 0.5` nats = `native_necessary`, `drop <= 0.1` = `native_effect_absent`, else
`inconclusive`; `drop = logprob(target|clean) - logprob(target|intervention)`.

## Shared graph build (done once per prompt; QA + QB read from it)

Rebuild each prompt's attribution graph with the flagship's parameters
(`attribute(..., max_feature_nodes=4096, offload="cpu", batch_size=64)`), rank the
`selected_features` by circuit-tracer's own `compute_node_influence` (the reimplemented
identical algorithm the flagship uses). Evaluate ALL cells for a prompt from this one graph
in one job (batched). Chunk prompts across jobs so each job <= ~15 min.

**Activation-indexing correction (frozen).** `graph.activation_values` is aligned with
`graph.active_features` (full, length `total_active_feats`); the adjacency/influence feature
block is ordered by `graph.selected_features`. The correct activation of adjacency feature `j`
is `activation_values[selected_features[j]]`, NOT `activation_values[j]`. The flagship runner
(`worker2.py`) used `activation_values[j]`, which is correct only if every active feature is
selected (`total_active_feats <= 4096`). We use the corrected index. We also record the
flagship's "buggy" value for every top-20 feature so the discrepancy is measured, not asserted.

**Determinism check (frozen).** For the 50 panel prompts, compare the rebuilt top-20 feature
set `{(layer,pos,feature)}` and influence rank to the committed flagship bundles. Report any
mismatch. Separately compare corrected vs flagship-recorded activation (expected to differ iff
`total_active_feats > 4096`).

## QUESTION A — dose / group size

Grid: group size `k in {5,10,20,50,100}` (and 200 where `n_selected>=200` and budget allows),
intervention factor `factor in {0, -0.5, -1, -2, -4}`. `factor` sets each feature's new
activation to `factor*activation` (feature_intervention `value`), and on the real model adds
`(factor-1)*activation*W_dec[feature]` at the feature's write layer/position — the flagship's
`-2x` steer is `factor=-2`, zero-ablate is `factor=0`. Groups are nested (top-k ⊂ top-100).

For every cell:
- **Native** (`native_group_intervention`, fp32 real weights): target-logprob drop + top-1 flip.
  Device: fp32 CUDA **resident** for speed (bit-identical to streamed per the flagship residency
  check); we cross-check the `k=20, factor∈{0,-2}` native drops against the flagship's committed
  numbers to confirm device/indexing effects are the only differences.
- **Graph prediction** (`feature_intervention`) under all three modes:
  `frozen_attention_iterative` (default), `unconstrained_iterative` (`freeze_attention=False`),
  `direct_effects` (`constrained_layers=range(n_layers)`). Graph predictions computed for the
  GRAPH top-k groups only (the random control is a native comparison, below).

Report, per family:
1. **Native flip-threshold curves**: per k, native top-1 flip rate vs `|factor|` (and the
   smallest `|factor|` that flips each prompt). Does a bigger group flip at a weaker dose?
2. **Graph-vs-native agreement** under the frozen rule (`classify_graph_vs_native`), per cell.
3. **Calibration per mode**: across cells, Spearman rank corr(graph_pred, native_drop) and
   mean `|graph_pred - native_drop|`.
"Does the graph predict the threshold" = whether the frozen-mode graph drop crosses 0.5 at the
same (k,factor) the native top-1 flips.

### CRITICAL CONTROL — matched-random groups (frozen)

For each graph top-k set `T={(l_i,p_i,f_i,a_i)}`, build a size-matched random set `R` drawn
from the prompt's ACTIVE transcoder features (`active_features`, with their true
`activation_values`), excluding every feature in `T`: for each member `i`, sample a feature at
the SAME `(layer l_i, position p_i)` whose `|activation|` is within `[0.5,2.0]×|a_i|` if any
exist, else the nearest-`|activation|` active feature at `(l_i,p_i)`; fall back to same layer →
same position → global if `(l_i,p_i)` has no other active feature. Use that feature's OWN
activation. Seed 0, deterministic. Record exact-`(l,p)`-match count. Native drop/flip measured
on `R` identically (no graph prediction — the random set is not a circuit).

**Preregistered margin.** "The graph found the causal set" holds for a (k,factor) cell/family
iff **mean native drop(graph) − mean native drop(random) ≥ 0.5 nats** AND **flip-rate(graph) −
flip-rate(random) ≥ 0.20 (absolute)**. If graph ≈ random within these margins, the observed
movement is generic damage, not circuit-specific.

- Falsifier for "graph found the causal set at the flagship cell (k=20, factor=-2)":
  (a) claim: graph top-20 is the causal set driving the 12/50 flips.
  (b) code computes: native flip rate and mean drop for graph-top-20 vs matched-random-20 at
      factor=-2.
  (c) under the claim graph ≫ random; under the alternative (generic damage from steering any 20
      active features) graph ≈ random. Outcomes differ → valid falsifier. If graph ≈ random we
      state the existing 12/50 result is ambiguous.

## QUESTION B — supernodes / pruned circuit

1. **Pruned node set (what a user sees).** `prune_graph(graph, node_threshold=0.8,
   edge_threshold=0.98)` (circuit-tracer's committed defaults, used by `create_graph_files` and
   the CLI/demo). Keep its feature nodes. Intervene on the WHOLE kept feature set at
   `factor∈{0,-2}`, native + graph (3 modes). Report kept-set size, native drop/flip,
   graph_vs_native.
2. **Automatic supernodes (frozen rule).** Partition the kept feature nodes by
   `(token position, layer-band)` with bands `[0,7),[7,13),[13,20),[20,26)` (quartiles of the
   26-layer depth). Each nonempty bucket is one supernode. Per supernode: native `factor∈{0,-2}`
   + graph prediction (frozen mode). Report per-supernode native vs graph effect; which
   supernodes are individually necessary natively (native drop ≥ 0.5 at factor 0, or top-1 flip
   at factor -2); and supernode-level graph-vs-native agreement.

- Falsifier for "supernodes are a fairer unit than top-k": supernode-level graph-vs-native
  agreement (over all supernode interventions, zero and -2x) exceeds the top-k group agreement
  (same factors) by ≥ 0.10. (a) claim: pruned/supernode interventions agree with native better
  than arbitrary top-k. (b) code computes both agreement rates. (c) under the claim supernode >
  top-k; under the alternative they are equal → valid.

## What results support which reading
- Flip needs a strong dose (|factor|≥2) regardless of k, and graph≈random at factor=-2 → the
  flagship's 12/50 is largely generic steering damage; the graph did not isolate a minimal
  causal set at the token granularity tested.
- Graph ≫ random at some (k,factor), and frozen-mode graph drop crosses 0.5 at the same cell the
  native flips → the graph predicts the causal set and the threshold.
- Pruned/supernode agreement > top-k agreement → graphs are better used as pruned circuits /
  supernodes than as raw top-k feature lists.

## Reporting
MEASURED vs INFERRED labelled. Bootstrap 95% CIs (percentile, 10k resamples, seed 0, resample
prompts) on per-family flip rates and agreement rates. Never round a miss into a pass. Job ids,
corrected-vs-flagship activation discrepancy, and every deviation recorded in FINDINGS-draft.md.
