---
title: "One Grokked Circuit Is Not a Certificate: Auditing Three Interpretability Instruments Against 84 Known Circuits"
type: research-paper
status: draft
date: 2026-10-05
updated: 2026-10-05
tags: [interpretability, mechanistic-interpretability, circuit-discovery, method-audit, benchmark, interpbench, activation-patching, attribution-patching, subspace]
---

# One Grokked Circuit Is Not a Certificate: Auditing Three Interpretability Instruments Against 84 Known Circuits

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
plus standard baselines, against the ground-truth circuits of **84 of the 86** InterpBench
models, reporting per-model node-level ROC-AUC against the published node set (and edge-level
AUROC for the two edge-attribution baselines). We preregistered four predictions and
hash-froze the scorer before the run. Measured means across 84 models: activation patching
0.941, EAP-IG 0.924, EAP 0.883 (the published ordering, P4 pass); gradient×activation 0.642
in its faithful centered-standard-deviation form and 0.783 in its magnitude form;
direct-logit write-site 0.484 (baseline-relative) and 0.693 (raw); subspace trace 0.772
(matched-rank random subspace 0.657, rank-1 0.761); random null 0.498. Two of the three
single-circuit verdicts transferred in direction — the gradient attribution is disqualified
for node localization (P1), and the write-site scan's scope boundary holds, so its mandated
baseline-relative form scores below chance for circuit-node recovery (P2 fail). The third did
not: the subspace trace's single-circuit failure was **falsified** here (P3a, P3b), yet its
own decisive control still denies it concept-specificity (the concept subspace beats a
matched-rank random subspace by only ~0.11–0.17 AUROC), so it is a degraded activation patch,
not a concept localizer. The conclusion is a caution about calibration: one known circuit
under-determines the deployment constraints an instrument earns. Caveat: for a reproducible
environment reason we sample inputs in-distribution to match the benchmark's sampler rather
than calling its compiled generator; the gold baseline reaching 0.94 bounds the damage, but
absolute AUROCs may shift.

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
benchmark of 84 independently published circuits, next to the standard baselines, and read off
a qualification table with the deployment constraint each method earns.

## 2. Benchmark and ground truth

InterpBench [2407.14494] distributes 86 semi-synthetic transformers (84 Tracr-compiled tasks
plus two IOI variants), each with its ground-truth edge set in `edges.pkl` and its weights in
`ll_model.pth`. Across all 86 configs the Tracr family shares a structure we rely on:
`normalization_type = None` (no LayerNorm), standard positional embeddings, sequential
attention→MLP, gelu, two layers, four heads, small `d_model`. We use the HuggingFace repo
`cybershiptrooper/InterpBench` at commit `a1242a84…`.

**Ground-truth node set.** Each `edges.pkl` is a list of `(writer, reader)` string edges in
the ACDC hook namespace, e.g. `blocks.1.attn.hook_result[2] → blocks.1.hook_q_input[2]`. We
promote edge endpoints to *node* granularity: attention-head nodes `('a', layer, head)` (from
`hook_result[h]` and the head readers `hook_{q,k,v}_input[h]`), MLP nodes `('m', layer)` (from
`hook_mlp_out`/`hook_mlp_in`), and the embedding nodes `('embed',)`, `('pos_embed',)`.
`hook_resid_post` (the model output) is not a scoreable component and is dropped. The candidate
node universe per model is every such node; a node is a ground-truth positive iff it is an
endpoint of some circuit edge after promotion. Node universes are small — median 12 nodes with
2 ground-truth positives (range 12–37 nodes), which makes a single model's AUROC coarse and is
why we aggregate across 84 models. For the two edge-attribution baselines we additionally score
the factorized writer→reader edge set directly (median 137-edge universe, 2 ground-truth edges).

**Scored set: 84 of 86.** We score the 84 Tracr-compiled models (81 categorical, i.e.
`d_vocab_out > 1`; 3 regression, `d_vocab_out == 1`). The two IOI models (`ioi`,
`ioi_next_token`) are excluded for two reasons (Section 7): their 42 MB weight files could not
be downloaded intact under a network throttle during the session, and — more fundamentally —
they are non-Tracr IOI models for which this note's synthetic-input assumptions (BOS index,
uniform value tokens) do not hold, so their results would be unfaithful even if loaded.

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

### 5.1 Headline: node-level AUROC across 84 models (MEASURED)

| method | kind | mean | median | min | max | frac beats null+0.1 |
|---|---|---:|---:|---:|---:|---:|
| **activation patching** | baseline — gold (exhaustive resample) | **0.941** | 1.000 | 0.667 | 1.000 | 1.000 |
| **EAP-IG** | baseline (EAP + integrated gradients) | **0.924** | 1.000 | 0.444 | 1.000 | 0.988 |
| **EAP** | baseline (edge attribution patching) | **0.883** | 0.900 | 0.500 | 1.000 | 0.940 |
| gradient×activation (magnitude) | instrument, magnitude variant | 0.783 | 0.900 | 0.185 | 1.000 | 0.810 |
| **subspace trace** | instrument (concept-subspace causal trace) | 0.772 | 0.770 | 0.400 | 1.000 | 0.821 |
| subspace, rank-1 control | instrument control | 0.761 | 0.845 | 0.250 | 1.000 | 0.714 |
| write-site (raw) | instrument, no-baseline variant | 0.693 | 0.791 | 0.033 | 1.000 | 0.631 |
| subspace, random control | instrument control (matched-rank random) | 0.657 | 0.661 | 0.000 | 1.000 | 0.571 |
| **gradient×activation (centered-std)** | instrument (faithful port) | 0.642 | 0.697 | 0.050 | 0.875 | 0.679 |
| **write-site (baseline-relative)** | instrument (mandated form) | 0.484 | 0.439 | 0.000 | 1.000 | 0.321 |
| random null | mean of 400 random vectors/model | 0.498 | 0.498 | 0.486 | 0.517 | 0.000 |

### 5.2 Edge-level AUROC (84 models, edge methods only, MEASURED)

| method | mean | median | min | max |
|---|---:|---:|---:|---:|
| EAP | 0.877 | 0.981 | 0.422 | 1.000 |
| EAP-IG | 0.895 | 0.993 | 0.478 | 1.000 |

EAP-IG ≥ EAP at the edge level as well as the node level.

### 5.3 Categorical vs regression split (means, MEASURED)

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

### 5.4 Preregistered verdicts (MEASURED)

| # | prediction | measured | verdict |
|---|---|---|---|
| **P1** | median gradxact < median act_patch − 0.10 | 1.000 − 0.697 = **0.303** | **PASS** — gradient×activation disqualified |
| **P2** | writesite ≥ null+0.1 on ≥60% of models | **32.1%** | **FAIL** — write-site not informative for circuit nodes |
| **P3a** | median subspace ≤ median null + 0.05 | 0.770 vs 0.498 (**+0.272**) | **FALSIFIED** |
| **P3b** | median \|subspace − subspace_rand\| ≤ 0.10 | **0.170** | **FALSIFIED** |
| **P4** | mean eap ∈ [0.65,0.95]; eap_ig ≥ eap−.05; act_patch ≥ eap−.05 | 0.883 / 0.924 / 0.941 | **PASS** |

### 5.5 Interpretation (ASSERTED where noted)

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
these shallow, LayerNorm-free compiled circuits the trace attains a respectable 0.772 AUROC and
beats the null on 82% of models — so the single-circuit *failure* (recovery no better than
random) does **not** replicate here (P3a, P3b both falsified). But the method's own decisive
control exposes what it is doing: a matched-rank random subspace reaches 0.657 and a rank-1
subspace 0.761, so the concept subspace's advantage over a random subspace of the same rank is
only ~0.11 (difference of means) to 0.17 (per-model median of the absolute difference) AUROC.
The signal is dominated by generic low-rank activation restoration — a degraded activation
patch — not by the concept being localized to the node. A high subspace-restore recovery is
therefore not evidence that the traced concept lives at that node, which is the same caution
[2311.17030] raise about subspace activation patching.

### 5.6 Per-prediction / per-method deployment constraints

| method | verdict for InterpBench node localization | deployment constraint earned (ASSERTED) |
|---|---|---|
| activation patching | **QUALIFIED — gold** (0.941) | the reference; use when the per-node forward budget is affordable |
| EAP-IG | **QUALIFIED** (0.924 node / 0.895 edge) | best gradient method; use the integrated-gradient path when patching is too expensive |
| EAP | **QUALIFIED** (0.883 node / 0.877 edge) | matches the published regime; fast first pass, dominated by IG and patching |
| gradient×activation (centered-std) | **DISQUALIFIED for node localization** (0.642; P1) | do not use the standard-deviation "content" pooling to find circuit nodes; the magnitude form (0.783) is a crude EAP and is far better |
| write-site (baseline-relative) | **DISQUALIFIED as a circuit-node detector** (0.484; P2 fail) | keep it for "which component writes this output feature"; it credits only direct-to-logit writers, so cross-depth circuit nodes are invisible and the mandated random-direction subtraction drives them negative |
| subspace trace | **QUALIFIED-WITH-CAVEAT as an importance proxy** (0.772) | usable as a cheap importance score on shallow circuits; do **not** read its recovery as concept localization — a matched-rank random subspace nearly matches it |

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

**Subspace trace — falsified.** The single-circuit verdict was that the trace fails to localize
— on a known numeric circuit and a grokked toy its recovery was no better than random or
rank-1. That failure did **not** reproduce here: across 84 circuits the trace is genuinely
informative (0.772, 82% beat-null). The single-circuit result over-generalized from a substrate
(Pythia-160M, deep, LayerNorm'd, a concept subspace that rotates across layers) where a fixed
input-defined subspace patched at deeper residual points is the wrong object, to a claim about
the instrument. On the shallow, LayerNorm-free compiled circuits here the same object is a usable
(if generic) importance score. The deeper *control-based* conclusion — concept ≈ random
subspace, so this is not a concept localizer — survives (the concept edge is only ~0.11–0.17
AUROC), but the headline failure verdict was substrate-specific.

**The honest conclusion (ASSERTED).** Two of three single-circuit verdicts transferred in
direction; one was falsified. A single known circuit is enough to *raise* a disqualification
hypothesis and to characterize a mechanism, but it under-determines the deployment constraints an
instrument earns — most sharply when the one circuit is structurally special (here: shallow and
LayerNorm-free vs deep and normalized). Calibration should be read as a lower bound on the
evidence an instrument needs, not an upper one: a verdict reached on one circuit should be stated
with its substrate, and a benchmark of many circuits can both confirm a transfer and overturn an
over-generalized failure.

## 7. Threats to validity

We state these in full because the first one is load-bearing.

1. **Data-generator deviation (primary caveat).** InterpBench's own `case.get_clean_data()`
   requires Tracr (jax/dm-haiku), which was uninstallable during the session under a severe
   external-bandwidth collapse (~3–15 KB/s). The scorer instead samples in-distribution random
   token sequences matching the benchmark's own random sampler — BOS at position 0 (index
   `d_vocab−2`), value tokens drawn uniformly from `0..d_vocab−3` at the remaining positions,
   full length `n_ctx` — and uses the ACDC-standard faithfulness-to-the-clean-run metric (KL for
   categorical, output L2 for regression), which needs no ground-truth labels and no high-level
   model. The method *ranking* is expected to be robust to this, but absolute AUROCs could shift
   with the original generator. The gold activation patch reaching 0.941 (and recovering the
   published circuits) bounds the damage: a badly mismatched input distribution would not let
   exhaustive patching recover the ground truth at 0.94.

2. **Reimplemented forward; no TransformerLens.** For the same bandwidth reason, the scorer
   reimplements the HookedTransformer forward in pure torch rather than installing TransformerLens
   1.19. These models have no LayerNorm (`normalization_type = None` on all 86), standard
   positional embeddings, sequential attention→MLP, and gelu, which makes a faithful forward
   small. It is validated **per model** by an exact direct-logit-attribution reconstruction of
   the model's own logits (sum of every node's direct write plus biases, projected through the
   unembedding): relative error ~1e-7 on every model (the absolute error reaches 1.5 only because
   some Tracr compiled logits reach ~4×10⁶). The baselines reproducing the published ordering is a
   second, independent check.

3. **Execution environment.** All model execution ran on a single workstation as a plain remote
   shell CPU process, outside the lab's job scheduler (whose worker contract is specific to a
   different stack and was not reachable without a tunnel); the run is a single sequential CPU
   process. No numbers were produced on a laptop.

4. **Single data draw, single seed.** `n_data = 256` clean + 256 corrupted per model, one seed.
   No extra seeds were run (the comparison is across 84 models, not across seeds).

5. **Coarse per-model AUROC.** The median node universe is 12 nodes with 2 ground-truth
   positives, so a single model's AUROC takes few discrete values; this is mitigated by
   aggregating over 84 models and is why we report medians and beat-null fractions alongside
   means.

6. **84 of 86.** The two IOI models are excluded — their weight files could not be downloaded
   intact under the throttle, and they are non-Tracr models for which the synthetic-input
   assumptions do not hold (they need an IOI-appropriate generator). Regression is a 3-model
   subsample; its means are reported but not interpreted.

7. **Node vs edge granularity for P4.** InterpBench's paper reports edge-AUROC; the primary
   comparison here is node-AUROC, with edge-AUROC reported as an augmentation (0.877 / 0.895) and
   consistent with the node-level ordering.

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
Forward validation: direct-logit-attribution reconstruction relative error ~1e-7 on every model.

Figures and their data file are listed in `figures/README.md`.

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
