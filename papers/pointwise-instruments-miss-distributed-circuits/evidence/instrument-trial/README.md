# The Instrument Trial

**When the reading contradicts the consumer: an executable benchmark for verdict-grade
interpretability.**

This repository ships the receipts for a preregistered head-to-head between the field's
standard measurement instruments — single-step activation patching, linear/dictionary
probes, cosine-similarity readouts — and consumer-gated causal certification, on matched
models, prompts, seeds, and internal state. The arbiter in every case is the **unchanged
native consumer**: the rest of the model, run to completion, deciding what the internal
state actually does.

The claim under test is narrow and falsifiable: *verdict-grade readings taken without
consumer closure can invert, in specific measured regimes.* This bundle lets you check
that claim on your laptop, with no GPU, from hash-verified receipts.

## Quickstart

```bash
pip install .
instrument-trial-verify
```

`instrument-trial-verify` checks every bundled receipt against its SHA-256 manifest, then
re-derives every case verdict from the raw receipt scalars using the frozen mechanical
decision rules (no interpretation layer), and compares them to the published verdicts.
Exit 0 = everything reproduces. The verifier is stdlib-only Python.

## The cases

| Case | Standard-instrument verdict | Consumer-level ground truth | Blind grade (standard arm) |
|------|-----------------------------|------------------------------|----------------------------|
| 1. Identity circuit (FLUX.2, diffusion) | Single-site/single-step patching sweep (4 sites × 4 steps, both directions): **"no necessary component"** — every single-cell ablation leaves the identity transition ≥ 0.22 of baseline | Ablating the same 4 components **across all steps** stops the transition (residual 0.0013 of baseline) and inserting them carries it (0.91), on held-out seeds, exact-replay gated | **MISREPORT** |
| 2. Wolf register (FLUX.2, conditioner state) | Held-out nearest-class-mean probe, validated **16/16** on native carriers (8/8 animals): **"no decodable content"** on the foreign register (top1 *tiger*, margin 0.035 vs floor 0.352); the archived own-template dictionary rule reads "decodable: deer" | Transplanting the 2 subject rows into the native run renders a **wolf** on both seeds (sham flat, exact gates) — the consumer decodes what a validated-flawless probe cannot see | **MISREPORT** |
| 3. Direction transfer (Qwen LMs) | Fitted difference-of-means direction transferred cross-model, bit-parity with the archived pipeline (delta 0.0): negative-cosine fraction **0.954** → **"representations differ across families"** | Raw native cosines 0% negative in every model; the split collapses to **0.0** under mean-centering alone (also diagonal/ZCA). Low-split control model reads 0.0 → the arm itself is validated | **MISREPORT** (control: MATCH) |
| 4. 0.996 cosine (FLUX.2, reconstruction) | Cosine ≥ 0.99 on held-out prompts: **"state recovered"** | A **content-free mean template** scores the same 0.993–0.997; rendered through the consumer, the reconstruction differs from native by pixel MAD 70–97 (exact duplicate: 0.0) and shows the wrong animal for all four prompts | **MISREPORT** |
| 5. Mediation across steps (honesty case) | Single-step mediation read: "holds at the measured step" | Swept across steps: holds in 17/18 axis×step cells — the standard reading was right in scope; included because an honest roster contains cases where the standard instrument reads correctly | INCONCLUSIVE (declines the generality question) |
| 6. Zero-write records (reserve) | "A zeroed answer logit is a maximal knockout effect" | 76/76 exactly-zero records sit at the final layer, where a bias-free unembedding after RMSNorm(0)=0 produces zero by arithmetic | **MISREPORT** |

**Blind-graded result: k = 4 of 4 non-reserve, non-honesty cases are standard-arm misreports
with consumer-gated matches (5 counting the reserve), against a preregistered success
criterion of k ≥ 3.** The grader was a context-free agent given only the rubric and
anonymized instrument readings (deterministic arm-order, no arm identities); its raw output
with per-grade deciding facts ships in `bundle/grading/grader-raw.json`. In every misreport
case the standard arm was bit-faithful (case 3: parity delta 0.0 with the original pipeline),
validated-flawless (case 2: 16/16 native validation), or threshold-matched to the certified
arm (case 1) — the misreports are properties of the method, not of a weak implementation.

## What this is not

- Not a claim that the standard tools are broken in general. The trial's claim is about
  **verdict-grade** readings taken without consumer closure, in these measured regimes.
- Not a strawman: each community arm implements the strongest faithful version of the
  standard recipe (preregistered per case, adversarially reviewed before running), and
  case 5 is included precisely because the standard reading survives it.
- Not free of disclosed imperfections: the grading record carries two disclosures verbatim
  (one grader/expectation disagreement on the honesty case; one X/Y-assignment transposition
  relative to the preregistered ordering rule, with blinding unaffected) — see the source
  tree's FINDINGS.md. Disagreements are reported, never reconciled.

## Vocabulary

See [GLOSSARY.md](GLOSSARY.md) for the two-way mapping between this project's terms
(Act, StateCut, route, carrier, native consumer) and the field's (intervention,
checkpoint, circuit, prompt context, behavioral readout).

## Seven ways to be confidently wrong

The measurement traps that motivated the whole program, each hit in practice and now
gated against: [TRAPS.md](TRAPS.md).

## Provenance

Receipts were produced by the SATURN transactional runtime (typed interventions,
bit-exact replay, fail-closed replay contracts, hash-chained evidence ledgers) on
FLUX.2-klein-4B (public weights) and Qwen-family models (public weights). Each receipt
carries its scheduler job ID; `bundle/manifest.json` pins content hashes. The
preregistration (case roster, decision rules, gates G1–G5, blind-grading protocol) was
frozen before the new arms ran.
