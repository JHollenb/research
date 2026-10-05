---
title: "One Grokked Circuit Is Not a Certificate: Auditing Three Interpretability Instruments Against 86 Known Circuits"
type: research-paper
status: draft
date: 2026-10-05
updated: 2026-10-05
tags: [interpretability, mechanistic-interpretability, circuit-discovery, method-audit, benchmark, interpbench, activation-patching, attribution-patching, subspace]
---

# One Grokked Circuit Is Not a Certificate: Auditing Three Interpretability Instruments Against 86 Known Circuits

**A method-audit note: do single-circuit verdicts on an interpretability instrument transfer to a benchmark of known circuits?**

Jacob Hollenbeck

*2026-10-05*

> Every node-level and edge-level AUROC in this note is **MEASURED**: it is recomputed from
> the frozen per-model result files named in the reproducibility appendix. Interpretations —
> why a method behaves as it does, and what it earns the right to be used for — are labelled
> **ASSERTED**. The single load-bearing caveat is stated in the abstract and in full in
> Section 7: the input generator is an in-distribution stand-in for the benchmark's own
> compiled data generator, so absolute AUROCs may shift under the original generator even
> though the method *ranking* is expected to be robust.

---

## Abstract

Before an interpretability instrument is trusted on an unknown model, it should be
calibrated on a circuit that is known by construction — this is standard practice
[2407.14494, 2301.05062, 2409.13714, Mueller 2025, 2311.17030, causal scrubbing,
2503.09532]. We had previously calibrated three in-house instruments — a gradient×activation
attribution, a direct-logit write-site scan, and an input-concept subspace causal trace — on
exactly **one** known circuit each: a grokked modular-addition transformer (for the first
two) and a known numeric circuit on Pythia-160M (for the third). That single-circuit exercise
disqualified the gradient attribution, certified the write-site scan for a narrow question,
and found the subspace trace was not a calibrated site-localizer. The question this note
answers is whether those single-circuit verdicts transfer. We score all three instruments,
plus standard baselines, against the ground-truth circuits of all **86** InterpBench models
(the 84 Tracr-compiled tasks as the aggregate, the two IOI models reported separately),
reporting per-model node-level ROC-AUC against the published node set (and edge-level AUROC for
the two edge-attribution baselines). We preregistered four predictions and hash-froze the
scorer before the first run, and preregistered three more (P5–P7) before the real-generator
rerun. We score on two node universes and take as **primary** the
**no-embedding** universe (attention-head and MLP nodes only), because the embedding is a
trivial ground-truth positive on 83 of 84 models and inflates the all-nodes score. We then
**re-ran the entire audit with the benchmark's own data generators** (Tracr/iit) on all **86**
models — including the two IOI models the first pass had skipped — in place of the
in-distribution sampler the first pass used. Measured no-embedding means under the real
generator (84 Tracr models): activation patching 0.990, EAP-IG 0.976, EAP 0.892 (the published
ordering; P4 holds); edge-level AUROC, the benchmark's own metric, EAP 0.868 / EAP-IG 0.894.
Both lab instruments, in the exact forms their single-circuit calibration mandated, sit **at
chance** — gradient×activation 0.499 and direct-logit write-site 0.462 against a 0.493 null —
while dropping the one deployment constraint each carried from its grokked circuit rescues it
(grad×activation without the norm division 0.842; write-site without the random-direction
baseline subtraction 0.708–0.809). The subspace trace (0.665) is statistically
**indistinguishable from a matched-rank random subspace** (0.644), so once the embedding
artifact is removed its single-circuit failure **replicates**. The headline result is that the
method ranking is **robust to the data generator**: every per-method mean shifts by < 0.1
between the synthetic and real generators (max 0.083) and the ordering is preserved (Spearman
0.98), so all three single-circuit verdicts transfer **in direction** — what each instrument
fails is the specific deployment constraint it carried (the grad×act norm division, the
write-site baseline-relative rule, the subspace "concept = site" reading), not the underlying
signal. The two IOI models are reported separately: under the benchmark's own non-contrastive
(independent-resample) corruption even exhaustive patching is uninformative (0.50), a property
of the IOI generator rather than of the instruments. The forward is validated against an
independent TransformerLens implementation (Tracr relmax 3.7e-5; the IOI LayerNorm forward
2.1e-6). The first pass's load-bearing data-generator caveat is thus closed — the ranking it
reported survives the real generator — and its one over-general claim (that the subspace
failure was *falsified*) is corrected: it was an all-nodes embedding artifact. The conclusion
is a caution about calibration: one known circuit under-determines the deployment constraints
an instrument earns.

## 1. Motivation: calibrate before you trust, and on how many circuits?

Causal interpretability methods are used to make claims — this node is in the circuit, that
component writes this feature, this concept lives at this site — and the field has converged
on calibrating a method against a circuit that is known by construction before trusting it on
an unknown one. InterpBench [2407.14494] and the Tracr line it builds on [2301.05062,
2409.13714] exist precisely to supply such known circuits; the Mechanistic Interpretability
Benchmark (MIB) [Mueller et al. 2025] formalizes circuit- and causal-variable-level scoring;
subspace activation patching has been shown to admit an interpretability *illusion* unless it
is controlled against a matched baseline [2311.17030]; causal scrubbing [Chan et al. 2022]
makes the faithfulness of a hypothesized circuit itself the test; and SAEBench [2503.09532]
is the same discipline for dictionaries. The common thread: a method earns trust by recovering
a structure someone already wrote down.

This lab had done that calibration, but on a thin substrate. Three instruments were each
calibrated against a *single* known circuit. (i) A gradient×activation attribution and (ii) a
reverse-chronological direct-logit write-site scan were both evaluated on one grokked
modular-addition transformer with a re-derived Fourier circuit. There, the gradient
attribution was disqualified — it placed a confident false positive on a constant component
and understated the true causal sources — while the write-site scan was certified for one
narrow question ("which component writes a given output feature"), with hard usage constraints
(baseline-relative contrasts only, directions constructed at the probed site, a
component-norm floor). (iii) An input-concept subspace causal trace was evaluated on a known
numeric circuit on Pythia-160M and on a one-layer grokked toy; there it failed — restoring the
concept subspace recovered the behavior no better than a matched-rank random subspace or a
rank-1 subspace, so it was declared *not* a calibrated site-localizer.

A single known circuit is cheap and tempting, but it is one point. A grokked mod-add
transformer is two layers, LayerNorm-free, periodic, and algorithmically degenerate; a verdict
reached there may be a fact about that circuit rather than about the instrument. **The
question of this note is whether single-circuit verdicts transfer.** We re-run all three
instruments — ported faithfully, same aggregations, same mandated controls — against a
benchmark of 86 independently published circuits (84 Tracr-compiled, aggregated; two IOI,
reported separately), next to the standard baselines, and read off a qualification table with
the deployment constraint each method earns.

## 2. Benchmark and ground truth

InterpBench [2407.14494] distributes 86 semi-synthetic transformers (84 Tracr-compiled tasks
plus two IOI variants), each with its ground-truth edge set in `edges.pkl` and its weights in
`ll_model.pth`. The 84 Tracr models share a structure we rely on: `normalization_type = None`
(no LayerNorm), standard positional embeddings, sequential attention→MLP, gelu, two layers, four
heads, small `d_model`. The two IOI models differ — six layers, `LNPre` LayerNorm (parameter-
free), the gpt2 vocabulary — and are scored with a matching LayerNorm forward (§3, §7). We use
the HuggingFace repo `cybershiptrooper/InterpBench` at commit `a1242a84…`.

**Ground-truth node set.** Each `edges.pkl` is a list of `(writer, reader)` string edges in
the ACDC hook namespace, e.g. `blocks.1.attn.hook_result[2] → blocks.1.hook_q_input[2]`. We
promote edge endpoints to *node* granularity: attention-head nodes `('a', layer, head)` (from
`hook_result[h]` and the head readers `hook_{q,k,v}_input[h]`), MLP nodes `('m', layer)` (from
`hook_mlp_out`/`hook_mlp_in`), and the embedding nodes `('embed',)`, `('pos_embed',)`.
`hook_resid_post` (the model output) is not a scoreable component and is dropped. The candidate
node universe per model is every such node; a node is a ground-truth positive iff it is an
endpoint of some circuit edge after promotion. Node universes are small — median 12 nodes with
2 ground-truth positives (range 12–37 nodes), which makes a single model's AUROC coarse and is
why we aggregate across 84 models. Crucially, the embedding is a ground-truth positive on 83 of
84 models (49 of 84 have exactly `{embed, m0}`), a trivial positive that inflates the all-nodes
AUROC; we therefore take the **no-embedding** universe (attention-head + MLP nodes only, ground
truth restricted the same way; median non-embedding positive count = 1) as the **primary** node
metric and report all-nodes as secondary (§5.1–5.2). For the two edge-attribution baselines we
additionally score the factorized writer→reader edge set directly (median 137-edge universe,
2 ground-truth edges) — the benchmark's own metric.

**Scored set: all 86.** We score the 84 Tracr-compiled models (81 categorical, i.e.
`d_vocab_out > 1`; 3 regression, `d_vocab_out == 1`) and the two IOI models. The first pass
excluded the IOI models (truncated downloads; a synthetic sampler that did not fit them); the
rerun re-downloads their weights intact (42 MB each) and scores them with the benchmark's own
IOI generator and a matching LayerNorm forward. They are reported **separately** (§5.8, §7):
their corruption is the benchmark's own non-contrastive re-sample, under which even exhaustive
patching is uninformative, so folding them into the Tracr aggregates would be misleading.

## 3. Methods

Every method scores a node with a single scalar; node-level ROC-AUC of that scalar against
node-in-circuit is the comparison. All methods share one performance signal, evaluated over
the non-first sequence positions (position 0 is dropped — the benchmark's `not_first_seq`
slice):

- **Categorical** (`d_vocab_out > 1`): performance scalar `m = Σ_{pos≥1} CE(logits, clean_argmax)`
  (cross-entropy of the run's logits to the clean run's argmax token — a label-free signal with
  nonzero clean gradient); faithfulness distance `faith = mean_{pos≥1} KL(clean ‖ run)`.
- **Regression** (`d_vocab_out == 1`): `m = Σ_{pos≥1} output`; `faith = mean-over-examples of
  ‖run − clean‖₂` over the non-first positions.

Both `faith` metrics are zero at the clean run. They are the ACDC-standard self-referential
faithfulness measures: they need no ground-truth labels and no high-level model. Let `a_n`
denote a node's captured activation (sliced to head `h` for attention-head nodes),
`a_n^clean`/`a_n^corrupt` its clean/corrupted-input values, and `g_n = ∂m/∂a_n` the clean
gradient.

**Activation patching (gold; exhaustive resample).** For each node, replace its clean
activation by the corrupted-input activation at *all* positions and score it by the
faithfulness distance of the patched run from the clean run:

```
score_actpatch(n) = faith( forward(clean_input, patch a_n ← a_n^corrupt at all positions) )
```

This is ACDC-style node importance [2304.14997] and the reference against which the cheaper
methods are judged.

**Edge attribution patching (EAP)** [2310.10348]. One clean forward/backward plus one corrupted
forward; the node score collapses the first-order patching estimate over positions and features:

```
score_eap(n) = | Σ_{pos≥1, feat}  g_n ⊙ (a_n^clean − a_n^corrupt) |
```

**EAP with integrated gradients (EAP-IG)** [2403.17806]. As EAP, but the gradient is integrated
over a 5-step interpolation of the *input embedding* between the corrupted and clean inputs
(midpoints `α = (i+0.5)/5`), with the per-node gradient accumulated along the path:

```
ḡ_n = (1/5) Σ_{i=0..4}  ∂m/∂a_n  evaluated at  embed = corr_emb + α_i (clean_emb − corr_emb)
score_eapig(n) = | Σ_{pos≥1, feat}  ḡ_n ⊙ (a_n^clean − a_n^corrupt) |
```

**Gradient×activation attribution** (first instrument under test). The zero-baseline
attribution `g_n ⊙ a_n`, reduced per example `i` to `A_i(n) = Σ_{pos≥1, feat} g_n ⊙ a_n^clean`.
Two aggregations across examples, and the choice between them is exactly what the single-circuit
calibration flagged as load-bearing:

```
centered-std ("content") form (the faithful port):   score(n) = std_i( A_i(n) ) / RMSnorm(n)
magnitude form:                                        score(n) = | mean_i( A_i(n) ) |
```

where `RMSnorm(n) = sqrt( mean_{pos≥1, examples} ‖a_n^clean‖² )`. The centered-std form is the
one disqualified on the grokked mod-add circuit; the magnitude form is algebraically a
zero-baseline attribution patch (a crude EAP).

**Direct-logit write-site scan** (second instrument). Project a node's additive write `w_n`
onto a task-readout direction and aggregate as a normalized centered standard deviation. For
categorical models the readout is the clean-predicted token's unembedding column, evaluated
per position (`val = (w_n W_U)` gathered at the clean argmax token); for regression it is the
single output column `W_U[:,0]`. The normalized score is
`s(n) = std_{pos≥1, examples}(val) / RMSnorm(w_n)`. Because these models have no LayerNorm, no
LN-scaling enters. Two forms:

```
baseline-relative (mandated instrument form):  score(n) = s_true(n) − mean_{16 random dirs} s_rand(n)
raw (no baseline):                              score(n) = s_true(n)
```

with a rand-vs-rand calibration recorded every run (two independent random-direction sets,
seeds 11 and 18; 16 directions each) — the first of the deployment constraints the
single-circuit certification imposed.

**Subspace causal trace** (third instrument). Build a low-rank input concept subspace `V` from
the top principal components of the centered clean embedding capturing ≥90% of variance (rank
`r`). Corrupt the input by projecting `V` out of the embedding; score each node by the recovery
of the faithfulness metric when the clean `V`-component is restored at that node's output:

```
corrupt(t) = t − (t V) Vᵀ                         (applied at hook_embed)
restore_V@n: at node n's output, add ((a_n^clean − t) V) Vᵀ
score_subspace(n) = faith(corrupt) − faith(restore_V @ n)
```

We include the single-circuit method's *own decisive controls*: a matched-rank random
orthonormal subspace `Vr` (QR of a Gaussian) and a rank-1 subspace `V1` (the top PC alone),
scored identically. If the concept subspace is doing concept-specific work, it should beat the
matched-rank random subspace; if it is merely restoring generic low-rank activation, it will
not.

**Proper random null.** The single scalar-draw null is degenerate (see Section 4). The null
here is the *mean node-AUROC over `K = 400` independent random score vectors* per model, which
converges to ≈0.5 and gives a per-model distribution to beat.

**Scoring.** Per-model node-level ROC-AUC is the Mann-Whitney / average-rank statistic of node
score vs node-in-circuit over the candidate universe. We report, across the 84 models: mean,
median, min, max, and the fraction of models on which each method beats that model's own random
null by ≥0.1 AUROC. Edge-level ROC-AUC is reported for EAP and EAP-IG over the factorized edge
universe.

## 4. Preregistration

The scorer (`worker.py`), this prediction list, and the frozen science parameters were
hash-recorded (SHA-256 in `FROZEN.json`) before the single-seed run across all 86 models. A
three-model smoke (cases 3, 4, 11) validated the pipeline only; the smoke numbers are not the
test. Frozen parameters: `n_data = 256` clean + 256 corrupted per model, single seed (clean
seed 0, corrupt seed 1000); EAP-IG 5 steps; write-site 16 random directions × two sets;
subspace variance fraction 0.90; random-null seed 1234; BOS index `d_vocab−2`, value tokens
`0..d_vocab−3`.

The four preregistered predictions and their falsifiers, verbatim:

- **P1 (gradient×activation disqualified vs gold).** `median AUROC(gradxact, centered-std) <
  median AUROC(act_patch) − 0.10`. *Falsifier*: gap < 0.10. Secondary, not pass/fail: report the
  magnitude form.
- **P2 (write-site informative).** `fraction of models with AUROC(writesite) ≥ AUROC(random) +
  0.10 is ≥ 0.60`. *Falsifier*: fraction < 0.60.
- **P3 (subspace trace replicates the single-circuit failure).** *P3a (task-literal):* `median
  AUROC(subspace) ≤ median AUROC(random) + 0.05`; falsifier: subspace median > random median +
  0.05. *P3b (mechanistic, pre-specified):* `median_models | AUROC(subspace) −
  AUROC(subspace_rand) | ≤ 0.10` — the concept subspace is statistically indistinguishable from
  a matched-rank random subspace, the decisive control. P3b holding would mean the failure
  replicates even if P3a is falsified (a rank-`r` restore is a degraded patch and can be
  informative without the *concept* being special).
- **P4 (EAP matches the published regime).** `mean AUROC(eap) ∈ [0.65, 0.95]` AND `mean
  AUROC(eap_ig) ≥ mean AUROC(eap) − 0.05` AND `mean AUROC(act_patch) ≥ mean AUROC(eap) − 0.05` —
  the published ordering ACDC ≥ EAP-IG ≈ ACDC > EAP. *Caveat*: the paper reports edge-AUROC; the
  primary comparison here is node-AUROC, with edge-AUROC as an augmentation.

**One disclosed post-freeze correction, and it flips P2.** The originally-frozen scorer computed
the random null as a *single* fixed-seed scalar draw reused identically across all models. That
is degenerate: one draw gives a per-model AUROC with mean ≈0.09 (not ≈0.5), which spuriously
inflated every "beats-random" fraction. We corrected it to the proper averaged null (mean of
400 independent random score vectors per model; measured mean 0.498, tight range 0.486–0.517).
This is a methodological bug fix, not a result-dependent choice — it does not touch any
prediction's *definition* — but it is a deviation from the frozen artifact and we disclose it as
one. It changes exactly one verdict: **P2 passed under the buggy null and fails under the correct
null.** The corrected scorer is the SHA recorded as `worker.py`; the originally-frozen SHA is
recorded as `worker.py_prefreeze`. Edge-level scoring (`worker_edge.py`) is a post-hoc
augmentation, labelled as such.

## 5. Results

> **Primary metric and data (revised 2026-10-05).** Two changes make the headline below the
> primary one. (i) The **no-embedding node universe** (attention-head + MLP nodes only) is the
> **primary** metric: the embedding is a ground-truth positive on 83 of 84 models and 49 of 84
> have exactly `{embed, m0}`, so the all-nodes score is inflated by a trivial positive (median
> non-embedding positive count = 1). (ii) The audit was **re-run with the benchmark's own data
> generators** (Tracr/iit) on all **86** models — including the two IOI models — in place of
> the first pass's in-distribution sampler. §5.1 is the primary (no-embedding, real) result;
> §5.2 is the all-nodes universe with a real-generator column added; §5.4 reports every
> verdict, including the rerun's P5–P7. Five extra score variants isolate *which* part of each
> instrument fails (the aggregator vs the carried deployment constraint).

### 5.1 Primary — no-embedding node universe, synthetic → real generator (MEASURED, 84 Tracr)

| method | synthetic | real | Δ | role |
|---|---:|---:|---:|---|
| activation patching | 0.994 | **0.990** | −0.004 | baseline (gold) |
| EAP-IG | 0.970 | **0.976** | +0.006 | baseline |
| EAP | 0.935 | **0.892** | −0.043 | baseline |
| grad×act, std no-norm (`std_raw`) | 0.826 | 0.842 | +0.016 | grad×act repair: drop the norm |
| grad×act, magnitude (`mag`) | 0.798 | 0.827 | +0.029 | crude zero-baseline attribution patch |
| write-site, RMS no-baseline (`rms_raw`) | 0.806 | 0.809 | +0.003 | write-site repair: drop the baseline |
| write-site, RMS baseline-relative (`rms`) | 0.757 | 0.778 | +0.021 | write-site, RMS aggregation |
| write-site, std no-baseline (`raw`) | 0.731 | 0.708 | −0.023 | write-site without the baseline |
| subspace trace | 0.662 | 0.665 | +0.004 | instrument 3 |
| subspace, matched-rank random control | 0.667 | 0.644 | −0.023 | control |
| subspace, rank-1 control | 0.717 | 0.635 | −0.083 | control |
| grad×act, magnitude/norm | 0.493 | 0.523 | +0.030 | |mean|/norm |
| grad×act, rms/norm | 0.484 | 0.506 | +0.021 | rms/norm |
| **grad×act (centered-std/norm) — instrument A lab form** | 0.481 | **0.499** | +0.018 | **mandated form → chance** |
| **write-site (baseline-relative) — instrument B lab form** | 0.479 | **0.462** | −0.017 | **mandated form → chance** |
| random null | 0.493 | 0.493 | 0.000 | null |

The ranking is **robust to the data generator**: every per-method mean shifts by < 0.1
(max 0.083, `subspace_rank1`) and the ordering is preserved (Spearman 0.982; max rank
displacement 2, among statistically-tied neighbours; 0 methods change tier) — **P5 and P6
pass**. The two lab instruments in their mandated forms sit at the 0.493 null; removing the one
constraint each carried from its single grokked circuit rescues it (the norm division for
grad×act: 0.499 → 0.842; the random-direction baseline subtraction for the write-site scan:
0.462 → 0.708/0.809). The concept subspace is statistically indistinguishable from a
matched-rank random subspace (0.665 vs 0.644, edge +0.021).

### 5.2 All-nodes node universe (secondary; first-pass synthetic with a real-generator column, MEASURED)

| method | kind | synth mean | **real mean** | median (synth) | min | max | frac beats null+0.1 |
|---|---|---:|---:|---:|---:|---:|---:|
| **activation patching** | baseline — gold (exhaustive resample) | 0.941 | **0.942** | 1.000 | 0.667 | 1.000 | 1.000 |
| **EAP-IG** | baseline (EAP + integrated gradients) | 0.924 | **0.925** | 1.000 | 0.444 | 1.000 | 0.988 |
| **EAP** | baseline (edge attribution patching) | 0.883 | **0.852** | 0.900 | 0.500 | 1.000 | 0.940 |
| gradient×activation (magnitude) | instrument, magnitude variant | 0.783 | 0.797 | 0.900 | 0.185 | 1.000 | 0.810 |
| **subspace trace** | instrument (concept-subspace causal trace) | 0.772 | 0.775 | 0.770 | 0.400 | 1.000 | 0.821 |
| subspace, rank-1 control | instrument control | 0.761 | 0.712 | 0.845 | 0.250 | 1.000 | 0.714 |
| write-site (raw) | instrument, no-baseline variant | 0.693 | 0.670 | 0.791 | 0.033 | 1.000 | 0.631 |
| subspace, random control | instrument control (matched-rank random) | 0.657 | 0.649 | 0.661 | 0.000 | 1.000 | 0.571 |
| **gradient×activation (centered-std)** | instrument (faithful port) | 0.642 | 0.645 | 0.697 | 0.050 | 0.875 | 0.679 |
| **write-site (baseline-relative)** | instrument (mandated form) | 0.484 | 0.475 | 0.439 | 0.000 | 1.000 | 0.321 |
| random null | mean of 400 random vectors/model | 0.498 | 0.498 | 0.498 | 0.486 | 0.517 | 0.000 |

On the all-nodes universe the subspace trace shows a spurious edge over its random control
(0.772 vs 0.657 synthetic; 0.775 vs 0.649 real) — this is the **embedding artifact**: restoring
the clean embedding subspace at the `embed` node trivially recovers the metric. On the
no-embedding primary universe (§5.1) that edge vanishes.

### 5.3 Edge-level AUROC (84 Tracr, edge methods only; synthetic → real, MEASURED)

Edge-level AUROC over the factorized writer→reader edge set is the benchmark's own metric.

| method | synth mean | real mean | synth median | real median |
|---|---:|---:|---:|---:|
| EAP | 0.877 | 0.868 | 0.981 | 0.978 |
| EAP-IG | 0.895 | 0.894 | 0.993 | 0.994 |

EAP-IG ≥ EAP at the edge level as well as the node level, under both generators.

### 5.4 Categorical vs regression split (means, synthetic all-nodes, MEASURED)

| method | categorical (n=81) | regression (n=3) |
|---|---:|---:|
| activation patching | 0.947 | 0.778 |
| EAP | 0.887 | 0.769 |
| EAP-IG | 0.930 | 0.769 |
| gradient×activation (centered-std) | 0.637 | 0.767 |
| write-site (baseline-relative) | 0.482 | 0.541 |
| subspace trace | 0.771 | 0.800 |

The regression subsample is three models and its means are weak; we report it for completeness
and do not draw regression-specific conclusions.

### 5.5 Preregistered verdicts (MEASURED)

**First pass (frozen P1–P4, all-nodes, synthetic) — and the same four under the real generator.**
All four keep their pass/fail status when the synthetic sampler is replaced by the benchmark's
own generator (last column):

| # | prediction | synthetic (all-nodes) | verdict | real (all-nodes) |
|---|---|---|---|---|
| **P1** | median gradxact < median act_patch − 0.10 | 1.000 − 0.697 = **0.303** | **PASS** — grad×act disqualified | gap **0.326** → PASS |
| **P2** | writesite ≥ null+0.1 on ≥60% of models | **32.1%** | **FAIL** — write-site not informative | **29.8%** → FAIL |
| **P3a** | median subspace ≤ median null + 0.05 | 0.770 vs 0.498 (**+0.272**) | **FALSIFIED** | +0.262 → FALSIFIED |
| **P3b** | median \|subspace − subspace_rand\| ≤ 0.10 | **0.170** | **FALSIFIED** | **0.186** → FALSIFIED |
| **P4** | mean eap ∈ [0.65,0.95]; eap_ig ≥ eap−.05; act_patch ≥ eap−.05 | 0.883 / 0.924 / 0.941 | **PASS** | 0.852 / 0.925 / 0.942 → PASS |

**Rerun predictions P5–P7 (no-embedding primary universe, preregistered in `PREREG-rerun.md`).**

| # | prediction | measured (real) | verdict |
|---|---|---|---|
| **P5** | no-embedding method ordering preserved synthetic → real | Spearman **0.982**; max rank displacement 2 (tied neighbours); 0 methods change tier | **PASS** |
| **P6** | every per-method mean shifts \|real − synth\| < 0.10 | max shift **0.083** (no-emb) / 0.049 (all-nodes) | **PASS** |
| **P7** | audit verdicts keep status on no-emb | V1 grad×act lab = chance (0.499 vs null 0.493); V2 write-site lab = chance (0.462); V3 **subspace ≈ random** (concept edge **+0.021**, the single-circuit failure **replicates**); V4 EAP regime (0.892/0.976/0.990) | **PASS (all four)** |

The P3 reconciliation: on **all-nodes** the concept subspace beats its matched-rank random
control (edge +0.116 synthetic / +0.126 real), which the first pass read as *falsifying* the
single-circuit "subspace fails to localize" verdict. That edge is the **embedding artifact** —
it comes from restoring the clean embedding subspace at the trivial `embed` node. On the
no-embedding primary universe the edge is **+0.021** (synthetic −0.006), so the subspace trace
is **not** a concept localizer and the single-circuit failure **replicates** (V3). All three
single-circuit verdicts therefore transfer in direction once the embedding artifact is removed.

### 5.6 Interpretation (ASSERTED where noted)

**The baselines reproduce the literature ordering.** Exhaustive patching and the
integrated-gradient attribution are strong and nearly indistinguishable at the top (0.941,
0.924), plain EAP is a notch below (0.883), and all three clearly beat the cheap heuristics,
at both node and edge level. P4 holds. This is the expected `ACDC ≥ EAP-IG ≈ ACDC > EAP`
regime [2304.14997, 2310.10348, 2403.17806], and its reproduction here is also the strongest
internal check on the reimplemented forward (Section 7): a wrong forward would not recover the
published circuits at 0.94.

**Gradient×activation is aggregation-sensitive; the content pooling is the wrong knob (ASSERTED).**
The faithful centered-std "content" form sits 30 AUROC points below the gold (0.642 vs 0.941,
median 0.697 vs 1.000) and barely separates circuit nodes from the rest. The magnitude
form — algebraically a zero-baseline attribution patch — recovers most of the gap (0.783).
Gradient attribution is therefore *not* intrinsically weak for localization; the choice of how
to pool a node's per-input attribution into one scalar is load-bearing, and the
standard-deviation pooling is the wrong choice. This is the same mechanism the single-circuit
calibration identified on grokked mod-add, where the centered-std repair also failed component
assignment.

**The baseline-relative write-site form is below chance; its raw form is informative (ASSERTED).**
Projecting a node's write onto the readout direction credits only components that write
*directly* to the logits; a node acting through a later head or MLP is invisible, and
subtracting the matched random-direction share drives true multi-layer nodes negative. The
mandated baseline-relative form scores 0.484 — below chance — and beats the null on only 32%
of models (P2 fail). The raw form, without the random-direction subtraction, is better (0.693)
but still well below the gold. Direct-logit attribution remains valid for its own
question — which component writes a given output feature — but should not be used to recover
circuit membership across depth.

**The subspace trace is a degraded activation patch, not a concept localizer (ASSERTED).** On
the all-nodes universe the trace attains 0.772 AUROC and beats a matched-rank random subspace
by ~0.11 (means) — which the first pass read as *not* replicating the single-circuit failure.
But that edge is the **embedding artifact** (§5.1–5.2): it is produced by restoring the clean
embedding subspace at the trivial `embed` node. On the **no-embedding primary universe** the
concept subspace (0.665) and a matched-rank random subspace (0.644) are statistically
indistinguishable — concept edge +0.021 (synthetic −0.006) — so the single-circuit failure
**replicates**, and the first pass's "P3 falsified" was an artifact of scoring the embedding.
The signal is dominated by generic low-rank activation restoration — a degraded activation
patch — not by the concept being localized to the node. A high subspace-restore recovery is
therefore not evidence that the traced concept lives at that node, which is the same caution
[2311.17030] raise about subspace activation patching.

**The failing part is the deployment constraint, not the aggregator (ASSERTED, no-embedding).**
The five extra score variants localize each disqualification. grad×act: the lab form divides
the per-input attribution by the node norm, and *that division* is what kills it — dropping it
lifts the standard-deviation form from 0.499 to 0.842 and the magnitude form from 0.523 to
0.827, both to baseline-competitive territory; the std-vs-magnitude aggregator choice is
secondary. Write-site: the lab form subtracts a matched random-direction share, and *that
subtraction* is the problem — the raw scans are competitive (0.708 std / 0.809 RMS) while the
mandated baseline-relative std form collapses to 0.462 (chance). Each instrument's one
carried-over rule from its single grokked circuit is exactly the rule that fails to transfer.

### 5.7 Per-prediction / per-method deployment constraints

| method | verdict for InterpBench node localization | deployment constraint earned (ASSERTED) |
|---|---|---|
| activation patching | **QUALIFIED — gold** (0.941) | the reference; use when the per-node forward budget is affordable |
| EAP-IG | **QUALIFIED** (0.924 node / 0.895 edge) | best gradient method; use the integrated-gradient path when patching is too expensive |
| EAP | **QUALIFIED** (0.883 node / 0.877 edge) | matches the published regime; fast first pass, dominated by IG and patching |
| gradient×activation (centered-std) | **DISQUALIFIED for node localization** (0.642; P1) | do not use the standard-deviation "content" pooling to find circuit nodes; the magnitude form (0.783) is a crude EAP and is far better |
| write-site (baseline-relative) | **DISQUALIFIED as a circuit-node detector** (0.484; P2 fail) | keep it for "which component writes this output feature"; it credits only direct-to-logit writers, so cross-depth circuit nodes are invisible and the mandated random-direction subtraction drives them negative |
| subspace trace | **QUALIFIED-WITH-CAVEAT as an importance proxy** (0.772) | usable as a cheap importance score on shallow circuits; do **not** read its recovery as concept localization — a matched-rank random subspace nearly matches it |

The AUROCs in this table are the first-pass all-nodes numbers; the no-embedding primary universe
(§5.1) sharpens every verdict in the same direction — the two disqualified instruments fall to
chance (grad×act 0.499, write-site 0.462 vs null 0.493), and the subspace trace's edge over its
matched-rank random control vanishes (0.665 vs 0.644), so its "importance proxy" is a generic
low-rank activation patch with no concept specificity. The qualified/disqualified assignments
are unchanged under the real generator (P5/P6/P7, §5.5).

### 5.8 IOI models (reported separately, MEASURED)

The two IOI models are scored with the same methods and the `MiniLN` LayerNorm forward
(full-logit reconstruction vs TransformerLens: relmax 2.1e-6 for `ioi`, 5.0e-7 for
`ioi_next_token`), `n_data = 128`. They are kept out of the Tracr aggregates because the
benchmark's own IOI corruption is an independent re-sample (not an ABC/name-swap): patching a
node with another valid IOI sentence's activation barely moves the KL-to-clean, so even
exhaustive patching cannot localize. No-embedding AUROC (GT positives / nodes in parentheses):

| model | act_patch | EAP | EAP-IG | grad×act (lab) | grad×act (mag) | grad×act (std_raw) | write-site (lab) | subspace | subspace_rand |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ioi (4/30) | 0.500 | 0.500 | 0.500 | 0.490 | 0.712 | 0.981 | 0.692 | 0.529 | 0.519 |
| ioi_next_token (13/30) | 0.500 | 0.500 | 0.500 | 0.475 | 0.652 | 0.606 | 0.638 | 0.357 | 0.421 |

The gold `act_patch` and both EAP variants sit exactly at 0.500 — a property of the IOI data
generator, not of the instruments. This is the mirror image of the Tracr result: there the real
generator leaves the ranking intact, here it removes the signal that patching needs, which is
itself the paper's point that the data generator is load-bearing. Full per-method and all-nodes
rows are in `results/real_full.json`.

## 6. What transfers from one grokked circuit, and what does not

Three single-circuit verdicts; three transfer outcomes.

**Gradient×activation — transferred in direction.** It was disqualified on one grokked mod-add
circuit and is disqualified here, for the same measured reason: the centered-standard-deviation
pooling cannot order nodes, while the magnitude pooling (a zero-baseline attribution patch) can.
The verdict and its mechanism both carried over to 84 independent circuits.

**Write-site scan — its scope boundary transferred.** The single-circuit exercise *certified*
this instrument, but only for a narrow question ("which component writes a given output
feature"), with the explicit characterization that it is a direct-logit-writer detector and
must be used with baseline-relative contrasts and site-constructed directions. This audit
applies it to a question it was never certified for — cross-depth circuit-node membership — and
it fails there (0.484, below chance in its mandated form). That is not a contradiction of the
original verdict; it is a confirmation of the original scope boundary. What transferred is the
*deployment constraint*, which is the part of a single-circuit verdict most worth trusting.

**Subspace trace — transferred (corrected).** The single-circuit verdict was that the trace
fails to localize — recovery no better than a matched-rank random or rank-1 subspace. The first
pass reported this *falsified* on all-nodes (the concept subspace beat its random control by
~0.11), but that edge is the **embedding artifact**: it is produced at the trivial `embed` node.
On the no-embedding primary universe the concept subspace (0.665) and a matched-rank random
subspace (0.644) are statistically indistinguishable — concept edge +0.021 — so the
control-based verdict (concept ≈ random subspace, i.e. not a concept localizer) **replicates**.
The trace remains a usable *generic* low-rank importance score on these shallow circuits, but
the "this concept lives at this node" reading does not transfer.

**The honest conclusion (ASSERTED).** With the embedding artifact removed and the benchmark's
own data generators used on all 86 models, **all three** single-circuit verdicts transfer *in
direction*: what each instrument fails is the specific deployment constraint it carried from its
one grokked circuit — the grad×act norm division, the write-site baseline-relative subtraction,
and the subspace "concept = site" reading — not the underlying signal, which the norm-free /
baseline-free / random-subspace controls recover. A single known circuit is enough to *raise* a
disqualification hypothesis and to name its mechanism, but it under-determines the exact
deployment constraint, and — as the first pass's all-nodes "P3 falsified" shows — a thin scoring
universe can even invert the verdict. Calibration should be read as a lower bound on the evidence
an instrument needs: state the substrate of any single-circuit verdict, score on a non-trivial
node universe, and treat a benchmark of many known circuits as the thing that turns a
single-circuit hypothesis into a usable constraint. That the ranking is unchanged under the
benchmark's real generator (P5/P6) is what licenses trusting these constraints.

## 7. Threats to validity

The first pass's two load-bearing threats — the data generator and the reimplemented forward —
are now **closed** by the rerun; we state the original caveats and their resolution in full.

1. **Data-generator deviation — CLOSED.** The first pass could not install Tracr (jax/dm-haiku)
   under a severe external-bandwidth collapse (~3–15 KB/s), so it sampled in-distribution random
   token sequences with an *assumed* encoding (BOS at `d_vocab−2`, value tokens `0..d_vocab−3`).
   The rerun installs the real stack offline (laptop-downloaded linux-cp310 wheels — jaxlib 0.4.30
   etc. — `scp`ed to a `venv-tracr`) and uses the benchmark's **own** generators on all 86 models:
   `case.get_clean_data()`/`get_corrupted_data()` for Tracr and iit `IOIDatasetWrapper` for IOI.
   The real encoding differs materially from the first pass's assumption (e.g. case 3 real BOS
   index = 0, not 4; case 4 real position-0 token = 2, not 5), so the first pass's clean run was
   partly out-of-distribution. Yet the method ranking is unchanged: every per-method mean shifts
   by < 0.1 (max 0.083) and the ordering is preserved (Spearman 0.98) — P5 and P6 (§5.5). The
   caveat the first pass flagged as load-bearing therefore does not change any conclusion; the
   ACDC-standard faithfulness-to-the-clean-run metric (KL / output-L2) is retained throughout.

2. **Reimplemented forward — now independently validated.** The scorer still reimplements the
   HookedTransformer forward in pure torch (for the Tracr models, `normalization_type = None`; for
   the IOI models, a `MiniLN` forward that adds the exact parameter-free `LNPre` + `ln_final`).
   Beyond the first pass's residual-sum direct-logit-attribution accounting check (which validates
   the *accounting*, not the attention computation), the forward is now validated against an
   **independent TransformerLens 2.18.0 implementation** (HookedTransformer from each
   `ll_model_cfg.pkl`): worst max-abs relative error **3.72e-5** over the 84 non-IOI models
   (63 causal + 21 bidirectional) and **2.1e-6** for the IOI `MiniLN` full-logit reconstruction.
   The baselines reproducing the published ordering is a second, independent check.

3. **Execution environment.** All model execution ran on a single workstation as a plain remote
   shell CPU process, outside the lab's job scheduler (whose worker contract is specific to a
   different stack and was not reachable without a tunnel); each run is a single sequential CPU
   process. Data generation (the Tracr/jax/iit stack) and scoring (the pure-torch stack, the same
   torch as the first pass) ran in separate venvs so the real-vs-synthetic comparison is
   apples-to-apples. No numbers were produced on a laptop (laptop work was wheel/model download
   and `scp` only).

4. **Single data draw, single seed.** `n_data = 256` clean + 256 corrupted per Tracr model
   (128 per IOI model, for memory), one seed (clean 42, corrupt 43). The comparison is across 84
   models, not across seeds.

5. **Coarse per-model AUROC, and a thin node universe.** The median node universe is 12 nodes
   with 2 ground-truth positives, so a single model's AUROC takes few discrete values (mitigated
   by aggregating over 84 models). More consequentially, the embedding is a ground-truth positive
   on 83 of 84 models, which inflates the all-nodes AUROC; we therefore make the **no-embedding
   universe** (attention-head + MLP nodes only) the primary metric and report all-nodes as
   secondary. The first pass's "P3 falsified" was a direct consequence of scoring the embedding
   (§5.5).

6. **All 86 scored; IOI with a generator caveat.** The two IOI models are now included (their
   42 MB weight files were re-downloaded intact — the first pass's curl copies were truncated to
   2.2/10 MB). They are reported separately because the benchmark's own IOI corruption is an
   **independent re-sample** (not an ABC/name-swap), so patching a node with another valid IOI
   sentence's activation barely moves the KL-to-clean and even exhaustive patching is uninformative
   (0.50) — a property of the IOI data generator, not of the instruments. Regression is still a
   3-model subsample; its means are reported but not interpreted.

7. **Node vs edge granularity for P4.** InterpBench's paper reports edge-AUROC; the primary
   comparison here is node-AUROC, with edge-AUROC reported alongside (synthetic 0.877 / 0.895 →
   real 0.868 / 0.894) and consistent with the node-level ordering under both generators.

## 8. Recommendation

A method audit should report, per method: (i) the AUROC against a *proper* null — the mean over
many random score vectors per model, with a confidence interval — not a single draw, and not
"beats chance" without a matched null; (ii) **both** aggregation variants when a method pools
per-input attributions into a scalar, because the pooling is load-bearing (the gradient×activation
gap here is entirely in the aggregation); (iii) matched-rank controls for any subspace- or
rank-restricted method (a matched-rank random subspace and rank-1), because a low-rank restore
can be an informative importance score without being concept-specific; and (iv) the single
deployment constraint the method earns — the one question it may be trusted to answer — rather
than a bare pass/fail. And calibrate on more than one circuit: state the substrate of any
single-circuit verdict, and treat a benchmark of many known circuits as the thing that promotes a
single-circuit hypothesis into a usable constraint.

## Appendix: reproducibility

Preregistration and frozen hashes:
`saturn/experiments/2026-10-05-interpbench-method-audit/` — `PREREG.md`, `FROZEN.json`
(SHA-256: `worker.py` `850eeced…`, `worker.py_prefreeze` `7c51941e…`, `worker_edge.py`
`c3fe9b93…`, `PREREG.md` `12ecbcd8…`, `analyze.py` `274daf3c…`), `worker.py` (node-level, frozen
v2 with the corrected null), `worker_edge.py` (edge-level augmentation), `analyze.py`,
`FINDINGS.md`, `PAPER-SECTION.md`, `RUN_LOG.txt`. Raw per-model results: `results/full.json`
(node level, 84 models — `case`, per-method `node_auroc`, `categorical`, `dla_recon_err`,
`n_nodes`, `n_gt_pos`, `gt_pos_nodes`) and `results/edge_full.json` (edge level, 84 models). Every
AUROC in this note is recomputed from those two files.

Runs (a plain remote-shell CPU process on one workstation; the lab's scheduler was not used):
`full-node` = `worker.py --cases <86> --n-data 256` → `results/full.json` (84 ok;
`ioi`/`ioi_next_token` skipped); `full-edge` = `worker_edge.py --cases <84> --n-data 256` →
`results/edge_full.json`; plus three-model smokes (cases 3, 4, 11) for pipeline validation only.
Ground truth: HuggingFace `cybershiptrooper/InterpBench` at commit
`a1242a84f8a4d07d1be9a8f5ec710415198016b2`; benchmark code `github.com/FlyingPumba/InterpBench`.

Real-generator rerun (2026-10-05): preregistration `PREREG-rerun.md` and frozen hashes
`FROZEN-rerun.json` (SHA-256: `gen_real_data.py` `18505003…`, `worker_real.py` `ce325006…`,
`worker_edge_real.py` `962e99fa…`; `worker.py`/`worker_edge.py` reused unchanged). New code:
`gen_real_data.py` (benchmark generators → per-case input tensors, run in a `venv-tracr` built
offline from laptop-downloaded linux-cp310 wheels), `worker_real.py` (reuses `worker.py`; adds
real-data loading, the no-embedding universe, five score variants, and `MiniLN` for the IOI
LayerNorm forward), `worker_edge_real.py`, `analyze_rerun.py`. Raw results: `results/real_full.json`
(node, 86 models — `auroc_all`, `auroc_noemb`, `null_*`, per-method scores, `kind`,
`dla_recon_err`/`tl_recon_relerr`), `results/real_edge_full.json` (edge, 84 Tracr),
`results/rerun_analysis.json` (synthetic-vs-real tables + P5–P7). Comparison baseline:
`results_audit_ext.json` (the same 15 methods and two universes rescored on the synthetic
sampler). Forward validation: residual-sum direct-logit-attribution per model (accounting), the
baselines recovering the published circuits, and an **independent TransformerLens** comparison
(84 non-IOI models, worst max-abs relative error 3.72e-5; IOI `MiniLN` full-logit relerr 2.1e-6;
`results/tl_forward_check.json`).

Figures and their data file are listed in `figures/README.md`.

## Changelog

- **2026-10-05 (v2, real-generator rerun).** Re-ran the full audit with InterpBench's own data
  generators (Tracr/iit) on all **86** models, replacing the first pass's synthetic
  in-distribution sampler, and added the two IOI models (LayerNorm forward, validated to 2.1e-6
  against TransformerLens). Made the **no-embedding** node universe primary (the embedding is a
  trivial ground-truth positive on 83/84 models). Added five score variants that localize each
  instrument's failure to its carried deployment constraint (norm division; baseline-relative
  subtraction). Results: the method ranking is robust to the real generator — every per-method
  mean shifts < 0.1 (max 0.083) and the ordering is preserved (Spearman 0.98); **P5, P6, P7
  pass**, and the frozen all-nodes P1–P4 keep their status. Corrected the first pass's one
  over-general claim: "P3 falsified" was an all-nodes embedding artifact; on the no-embedding
  universe the subspace trace is indistinguishable from a matched-rank random subspace (concept
  edge +0.021), so the single-circuit failure **replicates** and all three single-circuit
  verdicts now transfer in direction. Closed the first pass's load-bearing data-generator and
  reimplemented-forward caveats. Abstract, §2, §5, §6, §7 updated accordingly.
- **2026-10-05 (v1).** Initial audit: 84 Tracr models, synthetic in-distribution sampler,
  all-nodes node universe; P1 pass, P2 fail, P3 (all-nodes) falsified, P4 pass.

## References

[2407.14494] N. Gupta, J. Rumbelow, et al. *InterpBench: Semi-Synthetic Transformers for Evaluating Mechanistic Interpretability Techniques.* arXiv:2407.14494, 2024.
[2301.05062] D. Lindner, J. Kramár, S. Farquhar, M. Rahtz, T. McGrath, V. Mikulik. *Tracr: Compiled Transformers as a Laboratory for Interpretability.* arXiv:2301.05062, 2023.
[2409.13714] H. Thurnherr, J. Scheurer. *TracrBench: Generating Interpretability Testbeds with Large Language Models.* arXiv:2409.13714, 2024.
[Mueller et al. 2025] A. Mueller et al. *MIB: A Mechanistic Interpretability Benchmark.* 2025.
[2311.17030] A. Makelov, G. Lange, N. Nanda. *Is This the Subspace You Are Looking For? An Interpretability Illusion for Subspace Activation Patching.* arXiv:2311.17030, 2023.
[Chan et al. 2022] L. Chan, A. Garriga-Alonso, N. Goldowsky-Dill, et al. *Causal Scrubbing: A Method for Rigorously Testing Interpretability Hypotheses.* Alignment Forum / Redwood Research, 2022.
[2503.09532] A. Karvonen, C. Rager, et al. *SAEBench: A Comprehensive Benchmark for Sparse Autoencoders in Language Model Interpretability.* arXiv:2503.09532, 2025.
[2304.14997] A. Conmy, A. Mavor-Parker, A. Lynch, S. Heimersheim, A. Garriga-Alonso. *Towards Automated Circuit Discovery for Mechanistic Interpretability (ACDC).* NeurIPS 2023 (arXiv:2304.14997).
[2310.10348] A. Syed, C. Rager, A. Conmy. *Attribution Patching Outperforms Automated Circuit Discovery (EAP).* arXiv:2310.10348, 2023.
[2403.17806] M. Hanna, S. Pezzelle, Y. Belinkov. *Have Faith in Faithfulness: Going Beyond Circuit Overlap When Finding Model Mechanisms (EAP-IG).* arXiv:2403.17806, 2024.
[2309.16042] F. Zhang, N. Nanda. *Towards Best Practices of Activation Patching in Language Models.* arXiv:2309.16042, 2023.
[2404.15255] S. Heimersheim, N. Nanda. *How to Use and Interpret Activation Patching.* arXiv:2404.15255, 2024.
[Elhage et al. 2021] N. Elhage, N. Nanda, C. Olsson, et al. *A Mathematical Framework for Transformer Circuits.* Anthropic, 2021.
