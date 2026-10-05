---
title: "Submission review: the six primary papers (2026-10-05)"
type: review
date: 2026-10-05
scope: >
  research/papers/{time-formed-circuits, pointwise-instruments-miss-distributed-circuits,
  pass-indexed-baseline, instrument-audit-interpbench, time-circuit-scaffold, mdb-saturn-pub},
  read against papers/evidence-registry/claims.jsonl (19 claims) and each paper's README/CHANGELOG.
method: >
  Single reviewer pass, read-only. Each paper.md and README.md read in full; claims.jsonl read in
  full; cross-paper number collisions and vocabulary grepped directly from the paper bodies.
  No experiments run, no papers edited. Judgments are labelled ASSERTED; every quoted number names
  the file it came from. Successor to submission-review-2026-10-02.md.
---

# Submission review (2026-10-05)

This is the successor to `submission-review-2026-10-02.md`. That review covered two draft manuscripts
(`space-and-time-circuits/paper.md` and `scaffolds-and-dynamic-circuits/`) and found "real, checkable
results under too much wording," flagging length, hedging, internal jargon, three-papers-per-draft
scope, and a handful of stale/overclaimed lines. Since then the two drafts have been split and rebuilt
into the six papers reviewed here, a `papers/evidence-registry/` claim ledger (19 claims) now binds
many headline numbers to receipt bytes, and four of the six papers have been reworked or created on
2026-10-05.

Verdict in one line (ASSERTED): the science is in much better shape than on 10-02 — the jargon,
hedging, and scope bloat are largely gone, and the registry is a real improvement — but the six papers
are at very different readiness levels, two have **zero** of their own headline numbers in the
registry (`time-circuit-scaffold`, `mdb-saturn-pub`), and there is one concrete cross-paper number
mismatch (the circuit-tracer panel, pointwise §4.9 vs mdb §4) that must be reconciled before either
is submitted.

| Paper | Registry claims | Readiness (ASSERTED) |
|---|---:|---|
| time-formed-circuits | 7 | ready after listed fixes |
| pointwise-instruments-miss-distributed-circuits | 1 | ready after listed fixes |
| pass-indexed-baseline | 9 | ready after listed fixes (closest to ready) |
| instrument-audit-interpbench | 2 | ready after listed fixes |
| time-circuit-scaffold | 0 | not ready (substantial fixes) |
| mdb-saturn-pub | 0 | not ready (per the paper's own §7) |

---

## 1. time-formed-circuits

### (a) Central claim and strongest evidence
A circuit can be *formed* over an ordered execution axis (depth/denoising/recurrence) before it is
read, so the seed, the formed store, and the readout localize to different places; the flagship is a
block-and-rescue dissociation at a late key/value band. Headline numbers, all from
`time-formed-circuits/paper.md`: blocking the recipient-formed late band removes **0.73 to 0.92** of
an early seed's effect and transplanting it restores **0.71 to 0.99** across Qwen2.5-1.5B, Gemma-2-2B,
SmolLM2-1.7B and held-out identities (abstract, §3.4, Table 2); the original Qwen panel is block
**0.924 [0.765, 1.030]** / rescue **0.871 [0.850, 0.894]** over 42 rows, seed gains 1.577–5.555 nats
(§3.3); it reproduces at 7B (rescue **0.770**, block **0.595**, wrong **−0.026**, n=40, commit ~L21,
§3.4); transplant sufficiency reproduces in four blind families (rescue **0.64 to 1.62**), and the
block half recovers once the band is found causally (GPT-2 XL **0.160 → 0.888** at L31–42, Phi-2
**0.033 → 0.485** at L21–28, Table 2, Fig 7). An MLP-transcoder feature-and-error interchange moves the
identity answer at most **0.31** vs **0.94** for a native K/V cut; color recovers to **0.99** (§5,
Fig 4). FLUX.2 gives a strict four-condition signature (**0.5620 / 0.20743 / 0.91309 / 0.01101**, §6.1,
Table 3). The in-forward-vs-isolated gap at Qwen L0 is **0.985 vs 0.009** (§2.2). The frozen L22–27 band
is operation-general: recall block/rescue 0.902/0.862, two-hop 0.911/0.933, arithmetic joint-operand
rescue 0.925 (§8.1).

### (b) What changed since 2026-10-02
Per the CHANGELOG (§CHANGELOG, "Submission-readiness pass 2026-10-05") and the README "Round-5" entry:
§7.1 Mamba now leads with the matched clock-dose test (retention +0.0322 / write −0.0664 / joint
−0.0343 nats) as the causal evidence (resolving the 10-02 fix #3 two-source disagreement); §5 leads
with the matched feature-and-error interchange and states both E6 denominators explicitly (0.31/0.99 on
n=12/8; native 0.83/0.84 on the 42/25 sweep — the 10-02 fix #6); §8.1 (operation-general band) added;
Table 2 gained four blind-band rows (OLMo-2-1B, Pythia-1.4B, Phi-2, GPT-2 XL) and then two causal-band
rows for the deep models; prior art gained arXiv:2606.21345 and Syed 2023; "scaffold"/"custody"
reworded out of the body; a §2.1 Terminology paragraph grounds seed/formed store/readout; "19/32" is
now used throughout for the 0.5B computed-swap (the 10-02 fix #2 "15/32"). The README notes the
custody audit of the P1 experiments PASSED (byte-identical predictions across versions). No measured
number was altered.

### (c) Remaining weaknesses an outside reviewer would raise
- **One lab, one harness, small n per cell, mostly single seed** (§10 concedes this). LM cells are ≤42
  rows; pretraining-seed robustness is unmeasurable on public checkpoints.
- **Scale ceiling is sharp.** Positive mediation stops at 7B; the only >7B test (Qwen3-30B) did not
  survive the isolated cut (§10). Gemma-2-9B unavailable.
- **The causal-band rows are selected on the rows they are scored on** (§3.4). The split-half stability
  check (197/200, 200/200) mitigates but does not fully remove the selection-on-test concern for a
  skeptical reviewer.
- **The FLUX signature "buys less than its name suggests"** — the paper says so (§6.3): a weighted
  additive mechanism also passes it, no LM cell passes, and it is threshold-dependent (0.913 vs a 0.90
  line while a singleton already reaches 0.562).
- **§5 identity panel is 12 items** and the native cut vs feature operator are not magnitude-matched
  (§5 cautions); the 0.31-vs-0.94 gap conflates basis coverage with how much state each operator
  touches.
- **No sub-layer-grain sweep** (heads, K vs V, positions) of a distributed cell (§10, "Owed").

### (d) Readiness verdict: **ready after listed fixes**
- [ ] Bind the FLUX four-condition bounds (§6.1, `0.5620/0.20743/0.91309/0.01101`) and the 7B
      block-and-rescue (§3.4, `0.770/0.595`) to receipts — both are headline numbers with no registry
      claim (see (e)).
- [ ] Bind or explicitly cross-reference the §3.3 original-panel receipt (`0.924/0.871`, source file
      `FINDINGS-E20-mediation.md`), which differs from the registered cross-family receipt.
- [ ] Add at least one external-model / external-harness replication to answer "one lab" (§10 open).
- [ ] Consider a sub-layer sweep of one distributed cell (owed item) to pre-empt the "a finer
      instrument could find a compact site" objection.

### (e) Registry binding (`papers/evidence-registry/claims.jsonl`)
Bound (7): `tfc-e20-xfam-table2` (Table 2 cross-family cells), `tfc-e20-nonqwen-table2` (four blind-band
rows), `tfc-p1b-clustered-ci-table2` (identity-clustered CIs), `tfc-p1c-e6-interchange-fig4` (§5
feature+error interchange 0.31/0.99), `tfc-e6-native-kv-cut` (§5 native cut 0.94),
`tfc-breakit-operation-general` (§8.1), `tfc-e20-causal-band-table2` (causal-band rows / Fig 7).
**Not bound:** FLUX §6 (0.5620/0.20743/0.91309/0.01101), 7B §3.4 (0.770/0.595), the §2.2/§3.2
in-forward-vs-isolated gap (0.985/0.009), §3.1 formation windows, §3.2 Table 1 window-necessity, §3.5
P1-A formation-vs-propagation (0.871/0.985 legs), §4 read cut-and-join, §7/§7.1 Mamba writer and
clock-dose/retest, §8 computed-state E10 (19/32, 30/30), and the §3.3 original-panel point estimates as
cited to `FINDINGS-E20-mediation.md`.

---

## 2. pointwise-instruments-miss-distributed-circuits

### (a) Central claim and strongest evidence
Single-site activation patching reports "no necessary component" where a redundant distributed store
means no single site is necessary/sufficient but the whole path is both. Headline numbers from
`pointwise-instruments-miss-distributed-circuits/paper.md`: in FLUX.2 Klein 4B, single-component /
single-step ablation leaves **≥22%** (22.2%) of an identity transition, while all-four / all-step
leaves **0.13%** and insertion carries **91%** (abstract, §4.1); isolated single-layer K/V removal is
at most **16%** (GPT-2) and **8–18%** (Qwen/Gemma) while second-half removal is **81–104%** with flip
**83–95%** (§4.3); SAE top-20 at the best single layer removes **29%** of the Gemma identity effect
(57× random) but the answer flips in only 5% of items (§4.4); the in-forward-vs-isolated gap at Qwen
L0 is **0.99 vs 0.00** (§4.7); the transport-cut control gives single-site necessity **1.0–1.5%** at
the K/V cut but **172–236%** at the residual cut (§4.8); the attribution-graph panel finds **13 of
1,000** single features necessary, top-20 joint ablation flips **15 of 50** (all 8 two-hop; random 5),
−2× steer flips **45 of 50** (§4.9); the blind-graded readout comparison is **4 of 4** misreports (§5).
TransformerLens reproduces GPT-2 to **1.5×10⁻⁴** nats (§4.5).

### (b) What changed since 2026-10-02
This paper was not in the 10-02 review (that review covered space-and-time and scaffolds). Per its
CHANGELOG (two 2026-10-05 entries) and README: §4.9 (attribution graphs on Gemma-2-2B with circuit-tracer)
was added; §4.7 (the isolated-swap gotcha as one number) and §4.8 (the transport-cut result folded from
the IRD companion) were added; Related work (§7) was rewritten to state the delta and added refs
[16]–[22]. No earlier measured number was altered. Status in the front matter is `published` /
updated 2026-10-05 — the most mature of the six.

### (c) Remaining weaknesses an outside reviewer would raise
- **The blind-graded §5 trial shows failure modes exist, not how often** — cases were chosen because
  failure was expected and the arms are the author's own implementations (§5, abstract both say so). A
  reviewer will note the 4/4 headline cannot be read as a rate.
- **Breadth** (§6): one lab, single-token answers, two templated behaviours, five LMs (124M–2.6B) of
  which three rerun with isolated swaps, TransformerLens cross-check on GPT-2 only, one diffusion
  model, no external replication; color admitted too few items in GPT-2 (4) and Qwen-0.5B (8).
- **§4.9 rests on one model and one transcoder family**, and its first run was mis-dosed and rerun — a
  reviewer will want the corrected bundles to be the ones cited.
- **Circuit-tracer numbers disagree with the mdb paper's flagship** on what looks like the same panel
  (see cross-paper §iii) — this must be reconciled.
- **Only one registry claim** covers the §4.3/§4.4 panel; the distinctive FLUX, attribution-graph,
  transport-cut and blind-trial numbers are unbound (see (e)).

### (d) Readiness verdict: **ready after listed fixes**
- [ ] Reconcile the §4.9 circuit-tracer numbers with mdb-saturn-pub §4 (13/1,000 vs 0 necessary; 15/50
      vs 0 joint-flip; 45/50 vs 12/50 −2× steer) — state which run each reports and why they differ, or
      align them (cross-paper §iii).
- [ ] Bind the FLUX §4.1 (22%/0.13%/91%), §4.9 attribution-graph, and §5 blind-trial numbers to
      receipts, or state plainly that only §4.3/§4.4 are registry-covered.
- [ ] Verify the arXiv:2606.21345 title (the CHANGELOG already flags it as a "descriptive placeholder
      pending verification").

### (e) Registry binding
Bound (1): `pim-prereg-panel-sae-v2` (§4.3 preregistered panel + §4.4 SAE arms, rerun
`combined_summary_v2.json`). **Not bound:** §4.1 FLUX (22%/0.13%/91%), §4.5 TransformerLens
(1.5×10⁻⁴), §4.7 isolated-swap gotcha (0.99/0.00), §4.8 transport cut (1.0–1.5% / 172–236%, which lives
in the IRD companion), §4.9 attribution graphs (13/1,000, 15/50, 45/50, 64%), and §5 blind-trial (4/4).

---

## 3. pass-indexed-baseline

### (a) Central claim and strongest evidence
When you intervene inside a multi-turn context, the baseline must be the model's own continuation with
the same earlier turns run (the pass-indexed native), not the single-turn parent; the paper measures
the error. Headline numbers from `pass-indexed-baseline/paper.md`: on Qwen2.5-1.5B (base) the later-turn
native answer logprob moves a median **2.54 nats**, all positive (per-pass **+3.125 / +2.202 / +2.063**,
§3), and the native argmax differs in **11 of 12** pass≥1 cells; scoring a late K/V install against the
fixed parent flips sign and/or the 1-nat conclusion in **11 of 12** cells, and a format-matched baseline
removes **none** of them (§5). The format/content decomposition is format **+1.312**, question **−0.051**,
answer-content **+2.247** nats (§4). Replication: 1.5B-Instruct raw **2.76** nats / **9 of 12** flips,
chat **0.002** nats / **0/12**; 7B-Instruct raw **1.99** nats / **4/12** (bdiff 1.04), chat **0.000** /
**0/12**; 0.5B-Instruct chat **0.005** / 0/12; 1.5B-Instruct referential chat **2.23** nats / 0/12
(bdiff **2.72**); distractor **0.077** / 0/12 (§6). Spearman(|drift|, −fixed-parent logprob) = **0.91**
over 60 chat cells (§6).

### (b) What changed since 2026-10-02
New standalone methods note (date/updated 2026-10-05; the base measurement was preregistered
2026-10-02, the instruct/7B and the three chat-unsaturated cells added 2026-10-05). It is the realization
of the 10-02 feedback thread "Pass-indexed baseline + residual focus." The README/§6 describe the
two-regime (raw vs chat) replication as the main 2026-10-05 addition, with the chat-regime claim stated
as a mis-sized effect rather than a flipped conclusion (the referential arm's sign/flip prediction
failed, 0/12, disclosed in §6).

### (c) Remaining weaknesses an outside reviewer would raise
- **One model family (Qwen2.5), synthetic two-fact scenes, greedy, single seed, ≤7B, no cross-family
  check** (§8). Narrow prompt/scene diversity.
- **The 7B run uses a layer-paged BF16 engine**, a different numeric regime than the FP32 primary;
  reported as a direction/size replication, not a bit match (§8).
- **Low novelty by the paper's own admission** — "the recipe is what any careful evaluator would
  already do" (abstract, §1, §7); the contribution is the measured magnitude. A reviewer may find this
  a short workshop note rather than a main-track result.
- **Steering-vector addition is "argued by analogy," not run** (§8); only a K/V install is measured.
- **"Beast" and "mrun" appear in the §7 body recipe** (line 287) — lab infrastructure names in the
  method text (vocabulary §iv).

### (d) Readiness verdict: **ready after listed fixes** (closest of the six to ready)
- [ ] Remove the lab infrastructure names "Beast" / "mrun" from the §7 recipe body (line 287); keep
      them in the reproducibility appendix if needed.
- [ ] Bind the §4 format/content decomposition (+1.312 / −0.051 / +2.247) and the §7 mdb BenchSession
      BF16 reproduction (+3.33 / +2.08 / +2.22, `job-30443c340ead`) to receipts, or note they are
      unbound (see (e)).
- [ ] Optional: a single cross-family check (e.g. Llama or Gemma) would materially widen §8.

### (e) Registry binding
Bound (9): `pib-r0-drift-r2-flips-base` (§3 R0 drift + §5 R2 11/12 flips), `pib-instruct15b-raw`
(9/12), `pib-instruct15b-chat` (0/12), `pib-instruct7b-raw-bf16` (4/12), `pib-instruct7b-chat-bf16`
(0/12), `pib-chat-unsat-referential` (2.226 / 2.718 nats), `pib-chat-unsat-05b` (0.005), 
`pib-chat-unsat-distractor` (0.077 / 0.39), `pib-chat-unsat-p3-spearman` (Spearman 0.912). This paper is
the best-covered relative to its headline count. **Not bound:** the §4 format/content decomposition
numbers (the `pib-r0` claim text covers R0 drift and R2 flips, not the format-matched increments) and
the §7 mdb BenchSession reproduction (`job-30443c340ead`).

---

## 4. instrument-audit-interpbench

### (a) Central claim and strongest evidence
A single-circuit calibration under-determines what an instrument earns; scored against 86 InterpBench
models, the single-circuit verdicts transfer *in direction* but each instrument's one carried
deployment constraint fails. Headline numbers from `instrument-audit-interpbench/paper.md`
(primary = no-embedding, real generator, 84 Tracr, §5.1): activation patching **0.990**, EAP-IG
**0.976**, EAP **0.892**; lab grad×act **0.499** and write-site **0.462** sit at the **0.493** null,
rescued by dropping one constraint each (grad×act no-norm **0.842**; write-site no-baseline
**0.708–0.809**); subspace trace **0.665** vs matched-rank random **0.644**. All-nodes secondary (§5.2):
act_patch **0.941/0.942**, EAP-IG **0.924/0.925**, EAP **0.883/0.852**. Edge-level (§5.3): EAP
0.868/0.877, EAP-IG 0.894/0.895. Ranking is robust to the generator (Spearman **0.98**, max mean shift
**0.083**). Verdicts: **P1 PASS, P2 FAIL, P3a/P3b FALSIFIED, P4 PASS, P5/P6/P7 PASS** (§5.5). IOI
(§5.8): gold act_patch and both EAP = **0.500** under the benchmark's non-contrastive corruption.
Forward validated against TransformerLens (Tracr relmax **3.7e-5**, IOI LayerNorm **2.1e-6**).

### (b) What changed since 2026-10-02
New paper (date/updated 2026-10-05; not in the 10-02 review). Per the Changelog: v1 (synthetic
in-distribution sampler, all-nodes, 84 Tracr) → v2 (2026-10-05) re-ran the full audit with InterpBench's
own data generators on all 86 models, added the two IOI models, made the no-embedding universe primary,
added five score variants localizing each instrument's failure to its carried constraint, and
**corrected the first pass's one over-general claim** ("P3 falsified" was an all-nodes embedding
artifact; on the no-embedding universe the subspace failure replicates, concept edge +0.021). The
two load-bearing first-pass caveats (data generator, reimplemented forward) are closed.

### (c) Remaining weaknesses an outside reviewer would raise
- **"In-house instruments" with no external meaning.** Two of the three audited methods (grad×act lab
  form, write-site scan) are this lab's own; a reviewer outside the lab cannot independently judge
  whether the "mandated form" is a fair target, so the audit partly grades the lab's own earlier
  choices. The transfer-of-direction framing mitigates this but should be foregrounded.
- **Single seed, single data draw** (n_data=256/128), coarse per-model AUROC (median 12-node universe,
  2 positives) — aggregated over 84 models but each model's AUROC takes few values (§7).
- **Execution ran on a single CPU workstation outside the scheduler** (§7.3); reproducible but not the
  lab's qualified path.
- **Regression is a 3-model subsample** and is reported but not interpreted (§5.4, §7.6).
- **Edge-level AUROC and the P5/P6/P7 verdicts are not individually bound** (see (e)).

### (d) Readiness verdict: **ready after listed fixes** (strongest evidentiary standing of the six)
- [ ] Add a dedicated registry claim (or extend `iai-real-generator-noemb-84models`) for the edge-level
      AUROC (EAP 0.868/0.877, EAP-IG 0.894/0.895) and the P5/P6/P7 verdicts; currently the receipt files
      exist but no claim text names them.
- [ ] Foreground, early, that two of the three audited instruments are the lab's own and what that does
      and does not let the audit conclude.

### (e) Registry binding
Bound (2): `iai-node-auroc-84models` (receipt `full.json`: synthetic all-nodes 0.941/0.924/0.883 + P1–P4
verdicts) and `iai-real-generator-noemb-84models` (receipt `real_full.json`: no-embedding real
0.990/0.976/0.892, the lab-form chance values 0.499/0.462, the repair variants, and the IOI 0.500).
Both headline metrics (the demoted all-nodes and the primary no-embedding) are therefore bound.
**Not bound:** the edge-level AUROC table (§5.3) and the explicit P5/P6/P7 pass verdicts (the receipts
`edge_full.json` / `real_edge_full.json` / `rerun_analysis.json` are cited in §Appendix but carry no
claim id).

---

## 5. time-circuit-scaffold

### (a) Central claim and strongest evidence
Dynamic per-input circuits loop through a stable "time scaffold" — a store/router factorization with a
fixed, findable store read by address and an input-dependent routing program. Headline numbers from
`time-circuit-scaffold/paper.md`: a byte-identical stored state has query-dependent authority — median
**3.130** nats harm for color (16/16), **0.583** for position (16/16), **3.021** for a lookup (16/16),
128 directional checks (§1.1); a frozen 24-coordinate reader profile beats three competitors in all 8
held contexts (mapped cosine **0.954** vs **0.566**, RMSE 0.029 vs 0.149) and permuting the two value
projections collapses it (relation **0.955 → 0.049**, color 0.838 → 0.110, identity 0.931 → 0.569,
§1.2); fine-tuning conserves the read location but the band code transfers base→coder **0.92** /
base→math 0.43 but coder→base **0.34** / math→base **0.05** (§1.3); the blind locator hits 6/6 on Phi-2,
5/6 on OLMo-2, within-2 fraction 0.5 across seven models, and the deep-model misses relocate causally
(GPT-2 XL **0.888** vs 0.160, Phi-2 **0.485** vs 0.033, §1.4); one frozen band ties a per-input oracle
across operations (**0.85/0.95/1.00**, §1.5); the cross-family common graph is a null (MAE **0.015099**
vs 0.014593; role-matcher 6.9125 vs 6.9511, §1.6). Of eight commitments C1–C8, six hold, one fired
(C2), two narrowed (C3/C5 edges) (§2).

### (b) What changed since 2026-10-02
Major rebuild. At 10-02 this thesis lived in `scaffolds-and-dynamic-circuits/` (which the 10-02 review
called "≈90% redundant" with a bridge spine). Per the Changelog, on 2026-10-05 it was rewritten
findings-first as the new `time-circuit-scaffold/`: abstract leads with six measured findings and ends
with the C1–C8 falsifier scoreboard; §3 adds dispatch-gate / orthogonal-correction / cache-decomposition
results as single-cell "static-infrastructure-vs-dynamic-routing"; the 2026-10-05 causal-band result was
incorporated (and cited to the companion rather than duplicated); untraceable carrier-cosine figures
(0.995/0.78) were omitted in favour of the traceable 0.6602 record; the cross-family common graph is
now stated as a null, not a headline (the 10-02 review's recommendation). The `../scaffolds-and-dynamic-circuits/`
drafts are marked superseded.

### (c) Remaining weaknesses an outside reviewer would raise
- **The headline sentence is admitted to be unfalsifiable** ("a framing that no deterministic stateful
  network can violate," abstract/§2); the falsifiable core is the store/router factorization, and of
  its eight commitments **three fired this round** (C2 blind findability; C3/C5 edges: band-only K/V
  retrieves at 0.000; borrowed routing smuggles content through MLP gates). A reviewer will read this
  as a thesis substantially narrowed by its own tests.
- **The distinctive C4 result (query-gated authority) is "held but not distinctive" — "any attention
  model predicts this"** (§2 C4 row). The reader-profile and fine-tune results are single-model,
  single-seed, eight correlated contexts.
- **The cross-family common graph is a measured null** (§1.6) and there is no positive result above 7B
  (§5) — so the "architecture theory" is explicitly untested on the operations that would make it one
  (§2.1 close).
- **The v_proj-permutation result is not a behaviour-matched null** (the permuted network is less
  competent, §1.2 ASSERTED), and the null-network control has a disclosed failed prediction (the frozen
  reader beats operation-blind in the random net too, §1.6).
- **Zero of its own headline numbers are in the registry** (see (e)) — the only registry-covered rows
  it uses (the causal band) belong to the companion.
- **Role vocabulary "source / address/reader / writer / carried state / consumer"** is defined but reads
  as private jargon (§1.2 note in vocabulary §iv).

### (d) Readiness verdict: **not ready** (substantial fixes)
- [ ] Bind the paper's own headline numbers to receipts: §1.1 query-selective (3.130/0.583/3.021), §1.2
      reader profile (0.954/0.566) and v_proj permutation (0.955→0.049), §1.3 fine-tune transfer
      asymmetry (0.92/0.34/0.05), §1.5 break-it (0.852/0.950/1.000), §1.6 null (0.015099). Currently
      **none** are in `claims.jsonl`. This is the single biggest readiness gap of any of the six.
- [ ] Decide whether the paper is an "architecture theory" or a "better-instrumented extraction
      account" — §2.1 concedes it is untested as the former. Retitle/reframe accordingly, or run the
      cross-operation test that would discriminate.
- [ ] Add a behaviour-matched competent-non-scaffold control for §1.2 (the disclosed gap).
- [ ] Reduce the C1–C8 falsifier-scoreboard framing so a reviewer is not asked to accept an
      unfalsifiable headline alongside a three-firing core.

### (e) Registry binding
Bound: **0 of its own headline numbers.** The causal-band rows it uses in §1.4 are bound under the
companion's `tfc-e20-causal-band-table2`, which the paper correctly cites rather than duplicates. Every
other headline (query-selective authority, reader profile, v_proj permutation, fine-tune asymmetry,
blind locator, break-it, cross-family null, function-vector failure, the §3 single-cell results) is
**not bound.**

---

## 6. mdb-saturn-pub

### (a) Central claim and strongest evidence
Two public packages (`saturn-pub`, `mdb`) make a frozen model run as one inspectable, branchable,
receipted, durable transaction across transformer, SSM and diffusion families; the honest novelty is
the *combination*, not any primitive. Headline numbers from `mdb-saturn-pub/paper.md` (§3): shared K/V
ancestry **40.91%** byte reduction with **8/8** tokens matching the HF comparator; CUDA-VMM aliasing
bit-identical (32→24 MiB); routed working-set decode **1.859×** (63.99→119.04 tok/s) at batch 4; a
2,048-page archive answers **4/4** (absent/wrong 0/4); scene compiler **21/21** RGB across 5 diffusion
families; Mamba fork bit-exact with **2.2×10⁻⁴** staged replay. Evidence plane (§3.3): **97.7%** of
hash-pinned paths dead but **73.4%** byte-recoverable; xref indexed 218,164 citations; bisect answered
12 questions in 53 probes vs 1,010. Release validation (§3.2): v0.4.0 **480 passed, 1 skipped**. The
circuit-tracer flagship (§4): Gemma-2-2B single-feature graph-vs-native agreement **0.857 [0.835,
0.879]**, 0 individually native-necessary.

### (b) What changed since 2026-10-02
New paper (date 2026-10-05; not in the 10-02 review). Per its Changelog, the 2026-10-05 verification
pass measured the v0.4.0 test count (480 passed, 1 skipped) in place of the unmeasured release figure,
cited the causal-mask defect to its record (time-circuit-scaffold Limitations; the 2026-10-01 routing
re-run) rather than calling it unrecorded, and spot-checked every §3/§4 headline against its source
file. The README frames it as a tools / datasets-and-benchmarks note in the genre of nnsight/pyvene.

### (c) Remaining weaknesses an outside reviewer would raise
- **The paper itself says it is not ready for a main track (§7):** three demonstrations are "not yet
  done" — an outside user reproducing from an exported cut, an equal-semantics cost win, and an
  end-to-end pipeline no other framework runs.
- **No external user; all five "first users" are the author's own work** (§6). "Adoption is a claim we
  cannot make."
- **Efficiency wins are not equal-semantics** (§6): the 1.859× routed decode changes the eligible
  history; the CUDA-VMM construction is bit-identical but not integrated.
- **The Future Forest flagship is a reindex** (§3.3, §6): `model_loads: 0`, `checkpoint_reads: 0`,
  `optimizer_steps: 0` — it proves storage/runtime mechanics, not a live training forest.
- **The circuit-tracer flagship numbers disagree with pointwise §4.9** on an apparently-identical panel
  (cross-paper §iii).
- **Zero registry claims of its own** (see (e)); §4 leans on the other papers' bound numbers but quotes
  the *demoted* instrument-audit metric (see §iii).
- **Whimsical internal codenames ("Future Forest", "Ouroboros") in the body** (vocabulary §iv).

### (d) Readiness verdict: **not ready** (by the paper's own §7)
- [ ] Complete at least the first of the three §7 demonstrations (an outside user reproduces from an
      exported cut) before any main-track claim; the paper is otherwise fine as an arXiv/tools note
      that states its gaps honestly.
- [ ] Reconcile the §4 circuit-tracer flagship numbers with pointwise §4.9 (cross-paper §iii).
- [ ] Update §4's instrument-audit restatement to quote the paper's *primary* no-embedding real-generator
      metric (0.990/0.976/0.892), not only the demoted all-nodes synthetic (0.941/0.924/0.883) — or say
      explicitly which metric it is quoting (§iii).
- [ ] Consider adding registry claims for the §3 demonstration numbers so the tools note is as
      receipt-bound as the papers that depend on it.

### (e) Registry binding
Bound: **0.** None of the §3 demonstration numbers (40.91%, 1.859×, 21/21, 2.2e-4, 97.7%, 480 passed) or
the §4 circuit-tracer flagship (0.857) are in `claims.jsonl`. §4 restates numbers that are bound in
their own papers (time-formed, pointwise, pass-indexed, instrument-audit), but those bindings live in
those papers, not here.

---

## Cross-paper section

### (i) Ranked by strength of evidence and likely impact (ASSERTED)

1. **time-formed-circuits** — the highest-impact claim (construction history is causal anatomy; the
   tools built to find circuits cannot reach the formed store) backed by the deepest evidence: a
   block-and-rescue dissociation across eight decoder cells, held-out identities, 7B, a clean diffusion
   instance, and seven registry claims.
2. **instrument-audit-interpbench** — the most bulletproof: 84 known circuits, preregistered, a
   real-generator rerun that leaves the ranking unchanged, an independent TransformerLens forward check,
   and both metrics bound; impact is a sharp, defensible calibration caution rather than a new mechanism.
3. **pointwise-instruments-miss-distributed-circuits** — the most mature and broadest (five LMs + FLUX +
   a public-tool SAE workflow + a blind-graded trial), but only one registry claim and an unresolved
   internal number clash hold it below the top two.
4. **pass-indexed-baseline** — airtight and fully receipt-bound (9/9 of its cells), the closest to
   ready, but narrow (one family, synthetic) and explicitly low-novelty ("what any careful evaluator
   would already do").
5. **time-circuit-scaffold** — a genuinely interesting factorization, but an admittedly unfalsifiable
   headline, three falsifier firings this round, a cross-family null core, single-seed results, and zero
   of its own numbers in the registry put its evidentiary standing well below the four above.
6. **mdb-saturn-pub** — a careful, honest tools note whose impact is gated entirely on adoption it does
   not yet have; by its own §7 it needs three unrun demonstrations and has no registry coverage.

### (ii) Overlaps and duplication, with a recommendation per overlap

- **Causal-band rows (GPT-2 XL 0.888/0.160 at L31–42; Phi-2 0.485/0.033 at L21–28)** appear in both
  `time-formed-circuits` Table 2 / Fig 7 and `time-circuit-scaffold` §1.4. **Already handled correctly:**
  time-circuit-scaffold §1.4 says "these rows are folded into the companion paper's Table 2 and Figure 7;
  we cite them there rather than duplicate the table," and the registry binds them once
  (`tfc-e20-causal-band-table2`). **Recommend: keep as cite (no change).**
- **break-it operation-general band (0.852/0.950/1.000; joint-operand rescue 0.925)** appears in
  `time-formed-circuits` §8.1 and `time-circuit-scaffold` §1.5 (both from `2026-10-02-break-it-r2`).
  **Recommend: cite, not duplicate** — let time-formed §8.1 own it (it is registry-bound there as
  `tfc-breakit-operation-general`) and have time-circuit-scaffold §1.5 cite the companion, as it already
  does for the causal band.
- **Block/rescue dissociation (0.924/0.871; 0.73–0.92 / 0.71–0.99; 7B 0.770/0.595)** appears in
  `time-formed-circuits` §3 and is restated in `time-circuit-scaffold` §2 (C3 row) and `mdb-saturn-pub`
  §4. **Recommend: cite** — time-formed owns it; the companion's C3 row and the tools note's §4 should
  read as one-line citations (they largely do).
- **The FLUX route** appears in `pointwise` §4.1 (four route components `joint.2/3/4`, `single.0`;
  22%/0.13%/91%) and `time-formed` §6 (text-stream transplant; P-bounds 0.5620/0.20743/0.91309/0.01101).
  These are the **same model/route family measured at different cuts and metrics**, so they are not
  redundant, but a reviewer reading both will want the relationship stated. **Recommend: cross-cite** —
  each should note the other measures the same FLUX route at a different cut.
- **Chat-regime / pass-indexed cells** (2.54 / 2.76 / 1.99 nats; 11/12, 9/12, 4/12, 0/12) appear in
  `pass-indexed-baseline` and are restated in `mdb-saturn-pub` §4. **Recommend: cite** (pass-indexed
  owns them; mdb §4 is a correct one-line restatement).
- **Circuit-tracer Gemma-2-2B panel** appears in `pointwise` §4.9 and `mdb-saturn-pub` §4 as apparently
  the same preregistered 56-prompt / 50-admitted panel, both pointing at
  `saturn-pub .../experiments/circuit_tracer/`, but with **different numbers** (see §iii).
  **Recommend: reconcile first, then one owns and the other cites** — do not ship both as-is.

### (iii) Consistency checks (exact strings, with files)

**One concrete mismatch to fix — the circuit-tracer panel.** `pointwise` §4.9 and `mdb-saturn-pub` §4
describe what reads as the same preregistered 56-prompt / 50-admitted Gemma-2-2B circuit-tracer panel
(7 task families, top-20, thresholds 0.5/0.1 nats), and both cite the same bundle directory
(`experiments/circuit_tracer/`). The reported counts disagree:

- Single-feature necessity:
  - `pointwise-instruments-miss-distributed-circuits/paper.md:142`: "Of 1,000 single-feature ablations,
    **13 (1.3%) were individually necessary**"
  - `mdb-saturn-pub/paper.md:356`: "Single features: **0** individually native-necessary ...
    graph-vs-native agreement **0.857 [0.835, 0.879]**"
- −2× steering of the top-20:
  - `pointwise .../paper.md:142`: "steering the top 20 to −2× their activation **flips 45 of 50**
    (random 20)"
  - `mdb-saturn-pub/paper.md:358`: "steering the top-20 set to −2x activation **flips the native top-1
    on 12 of 50**"
- Top-20 joint / zero-ablation:
  - `pointwise .../paper.md:142`: "Ablating the same 20 features jointly **flips the answer on 15 of 50
    prompts**"
  - `mdb-saturn-pub/paper.md:359`: "**joint zero-ablation never flips the top-1** (0.34 [0.22, 0.48])
    yet the graph predicts a large drop on 13"

These may be two genuinely different runs (pointwise's circuit-tracer intervention at the transcoder
write site vs mdb's `saturn_pub.trial` native-arbitration seam), but because both are framed as the
same panel and cite the same bundle, a reviewer reading both will treat 45/50-vs-12/50 and
15/50-flips-vs-0-flips as a contradiction. **The coordinator must state which run each paper reports
and why the numbers differ, or align them.**

**One framing/staleness mismatch (not a numeric contradiction).** `mdb-saturn-pub/paper.md:337–340`
restates instrument-audit as node AUROC "activation patching **0.941**, EAP-IG **0.924**, EAP
**0.883**" — the *demoted all-nodes synthetic* metric — while the instrument-audit paper's own abstract
and §5.1 now lead with the no-embedding real-generator metric "activation patching **0.990**, EAP-IG
**0.976**, EAP **0.892**" (`instrument-audit-interpbench/paper.md:51`, `:321–322`). Both numbers are
real and both appear in the instrument-audit paper, so this is not a false number, but mdb quotes the
paper's secondary metric as though it were the headline.

**Coincidental string collisions I checked and cleared (NOT inconsistencies):** the string `0.924`
is both the time-formed block fraction and the instrument-audit EAP-IG AUROC; `0.941` is both the
OLMo-2-1B rescue (time-formed Table 2) and the instrument-audit act_patch AUROC; `0.770` is both the
time-formed 7B rescue and the instrument-audit subspace median (all-nodes); `0.852` is both the
break-it arithmetic ratio (time-formed §8.1 / time-circuit-scaffold §1.5) and the instrument-audit EAP
real all-nodes mean. Same digits, different quantities — no action needed.

All other restated numbers I checked are consistent across papers (2.54 / 2.76 / 1.99 nats and 11/12 in
pass-indexed vs mdb §4; 73–92% / 71–99% / 0.31 / 0.94 in time-formed vs mdb §4; 22% / 0.13% / 91% and
1.5×10⁻⁴ in pointwise vs mdb §4; 0.941/0.924/0.883 in instrument-audit §5.2 vs mdb §4).

### (iv) Vocabulary — remaining lab-internal terms in the paper bodies (file:line)

Genuinely worth fixing (lab infrastructure / whimsical codenames in a science body):
- `pass-indexed-baseline/paper.md:287` — "run on **Beast** through **mrun** in BF16 (**mdb**'s Qwen lane
  refuses FP32)". Host name + scheduler name + tool name in the §7 recipe body. (Also the only `mrun`
  hit in any of the four science papers.)
- `mdb-saturn-pub/paper.md:199, :285, :409, :443` — "**Future Forest** (the lab's name for the
  persistent version-control store)". Whimsical internal codename; acknowledged as a lab name but kept
  in the body.
- `mdb-saturn-pub/paper.md:215` — "the lab's compilation/route facade (named **Ouroboros** internally)".
  Named once, explicitly internal.
- `mdb-saturn-pub/paper.md:222` — "the lab's **Saturn** research workspace".

Defined-but-private-jargon-adjacent (reviewer may still flag; these are deliberately defined in-paper):
- `time-circuit-scaffold/paper.md:23` — role vocabulary "**source**, address/reader, writer, carried
  state, **consumer**" (the task's "source/store/consumer as private jargon"); defined once but used as
  the paper's spine. "scaffold" is this paper's own title term and is in scope here.
- `mdb-saturn-pub` — "**StateCut**" (`:107, :177, :472`), "**Act**" (`:116` and throughout), "sealed"
  (`:25, :33, :67, :107, ...`), "**custody**" (`:74, :145, :152`), "**mrun-pub**" (`:505`). These are
  the public-API names the tools paper is about, so they are largely inherent, but a reviewer will still
  flag them as unglossed jargon on first read.

Acceptable (tool name in a reproducibility/appendix context, not the science body):
- `time-formed-circuits/paper.md:387–388` — "**saturn-pub** evidence claim registry" (Appendix C).
- `pointwise .../paper.md:146, :203` — "**saturn-pub** repository" / "**saturn-pub** evidence claim
  registry"; "**sealed** per-prompt bundles" (`:146`, standard usage).
- `pass-indexed-baseline/paper.md:341` — "weight **custody** sha256 asserted" (reproducibility appendix).

Standard-usage hits (not jargon, listed because the term is on the watch-list):
- `time-formed-circuits/paper.md:190` — "Two **denominators** are in play" (ordinary statistics: two
  different normalizers; not private jargon).

Not found anywhere in the six bodies: "TokenMachine", "final boss", "StateCut"/"Act" in the four science
papers (only in `mdb-saturn-pub`), "scaffold" as a stray term in `time-formed-circuits` (it survives
only in the `../time-circuit-scaffold/` companion link and in Appendix A experiment paths such as
`scale-9b-scaffold`, `blind-scaffold-prediction`).

### (v) Older / secondary drafts in papers/ (one-line status each, from their READMEs)

- **capabilities-as-transactions/** (status: draft, 2026-09-30) — "The Final Boss Is a Role, Not a
  Layer"; the final-boss/transaction dossier. **Superseded / consolidated** into
  `space-and-time-circuits/` (which lists it as one of four consolidated sources); depends on pointwise,
  IRD and the bfl route for its receipts. Still carries the flagged term "final boss" (defined in-paper)
  and "denominator".
- **integral-residual-dynamics/** (status: draft, 2026-09-30) — the theory-and-certificate companion to
  pointwise (which its README names as "the primary IRD measurement paper"). **Standalone theory
  companion**, not superseded; its transport-cut and isolated-swap results are folded into pointwise
  §4.7–4.8.
- **space-and-time-circuits/** (status: draft-3, 2026-10-01) — the consolidation draft the 10-02 review
  targeted; it is the spine `time-formed-circuits` was built on. **Superseded** by `time-formed-circuits`
  (Paper 1) and `time-circuit-scaffold` (Paper 2).
- **scaffolds-and-dynamic-circuits/** (status: revised-architectural-drafts, 2026-10-01) — explicitly
  "Superseded by ../time-circuit-scaffold/"; kept for its method and figures. **Superseded.**
- **phaselock-kv-shifts/** (updated 2026-09-30) — "Rotation Swamping"; "Neither version is submitted or
  published." **Standalone draft whose content is merged into `rounding-placement/`** (the numerics
  paper); several of its evidence files are cited by `rounding-placement`.
- **rounding-placement/** (draft 2026-10-02, round-3 reviews addressed) — "Where You Round Beats How
  Many Bits"; merges the PhaseLock/rotation-swamping line with the training-numerics (B(x)/exact-
  accumulation) line into one claim. **Standalone draft, active** (the realization of the 10-02 review's
  "possible third paper"). Not one of the six primary papers.
- **clocked-ledger-memory/** (README) — "A Clocked Ledger: exact, time-aware memory for a frozen LM."
  **Standalone draft**; E5 (512k–10M) is the only run still pending.
- **formed-state-faithfulness/** (status: Parked 2026-10-02 after round 2, 4/10, fold recommended) —
  "The Answer Follows the Cache." **Parked / to be folded** into Paper 2 (`time-circuit-scaffold`); kept
  as an accurate record with only evidence-accuracy fixes applied.
- **mrun-model-execution/** (status: source-verified-draft, 2026-09-29) — an implementation review of
  the mrun model-execution stack. **Standalone systems draft** (currently untracked in git). Linked from
  the repo and papers READMEs; not one of the six primary papers.

---

*Prepared read-only; no paper was edited and no experiment was run. Every quoted number names its source
file; all ranked-list and readiness judgments are ASSERTED.*

## Addendum (2026-10-05, after the review)

Resolved by the coordinator the same day; the body above is left as written.

- **Cross-paper mismatch (iii).** mdb-saturn-pub §4 had copied the withdrawn first-run circuit-tracer numbers from `saturn-pub/docs/circuit-tracer.md`; it now reports the corrected rerun that pointwise §4.9 carries (13/1000 necessary, agreement 0.846 [0.824, 0.868], −2× steer 45/50, zero-ablation 15/50) and names the first run as a verification episode. The saturn-pub docs text still describes the first run and is out of scope here.
- **Stale restatement.** mdb-saturn-pub §4 now quotes instrument-audit's primary no-embedding real-generator numbers (0.990 / 0.976 / 0.892).
- **Vocabulary (iv).** pass-indexed §7 no longer names the host or the scheduler; mdb-saturn-pub no longer names the lab workspace by codename. Tool-level names in the tools paper (StateCut, Act, Future Forest, mrun-pub) are public API names and stay.
- **Registry.** 19 → 41 claims (verify 41/41, chain_ok). time-circuit-scaffold now has six of its own (`tcs-*`), mdb-saturn-pub eight (`mdb-*`), and the specific unbound numbers listed above for time-formed (FLUX bounds, 7B, original panel), pointwise (FLUX, LM grid, instrument trial, §4.9), pass-indexed (format-vs-content control) and instrument-audit (edge level) are bound.
- **Citation.** arXiv:2606.21345 was verified against the arXiv listing earlier in the day; the pointwise changelog now says so.
- **Still open, as the review states:** outside replication for every paper; the three tools-paper demonstrations; a behaviour-matched competent control for scaffold §1.2; a sub-layer sweep.
