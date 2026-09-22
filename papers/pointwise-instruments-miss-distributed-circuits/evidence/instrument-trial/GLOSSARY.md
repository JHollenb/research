# Glossary

This page maps the corpus's vocabulary to the interpretability field's standard terms, in both directions. The house terms are mostly *stricter versions* of the standard ones — the extra strictness is the point, and each entry says what the stricter version adds.

## House term → field term

| House term | Nearest field term | What the house version adds |
|---|---|---|
| **Act** | intervention / activation patch | Preview→commit semantics: an Act is proposed, previewed against typed state, and only then committed. A raw patch has no such two-phase contract. |
| **StateCut** | checkpoint | Custody: a StateCut is a typed, content-addressed cut of run state (packed latent, IDs, schedule cursor, conditioner embeds) with a SHA-256-validated manifest and bit-exact resume. A checkpoint is usually just weights or a pickle. |
| **Frame** | forward-pass scope / hook context | Typed boundaries: reads and writes go through declared addresses with dtype/shape checks, not arbitrary Python hooks. |
| **route** | circuit | A consumer-closure requirement: a route is only *certified* when the unchanged native consumer's output — not an internal metric — validates necessity/sufficiency, under exact-replay gates and sham controls. |
| **carrier** | run / prompt context | The specific execution whose state hosts an intervention. "Native carrier" = the unmodified run; interventions are described as row/register transplants *between* carriers, which keeps donor and host bookkeeping explicit. |
| **register** | token-position-localized feature bundle | Addressed by conditioner row (token position), not by fitted direction — identified by causal transplant, not by probe readout. |
| **typed payload** | steering vector / patch value | Declared dtype, shape, and address; rejected on mismatch rather than silently broadcast. |
| **conditioner row** | text-encoder token embedding (cross-attention conditioning) | Row-level addressability as a first-class debugger primitive. |
| **native consumer** | downstream behavioral readout | The *unchanged* rest of the model (and decoder), run to completion. The corpus's central rule: an internal activation change is not a result; only the native consumer decides. |
| **exact gate (0.0)** | reproducibility check | Bit-exact replay of the unmodified path, enforced fail-closed before any intervention result is read. |
| **sham control** | random / mismatched-intervention control | Mandatory in the demo template's controls table; a result without its sham is not reportable. |
| **replay contract** | — (no standard equivalent) | A verifier that refuses to replay when model identity, source revision, backend, or schema cannot be proven; drift fails closed instead of silently proceeding. |
| **claims registry** | — (no standard equivalent) | An executable registry (`saturn-claims`) where each claim carries a replay recipe and a dependency fingerprint over exact file bytes; when a dependency drifts, the claim auto-downgrades to stale. |
| **evidence plane** | — (no standard equivalent) | The stdlib-only verbs (`saturn-claims`, `saturn-xref`, `saturn-bisect`, `saturn-watch`, `saturn-custody`, `saturn-evidence`) that make readings citable, queryable, and auditable after the fact. |
| **first-divergence / bisect** | — (closest: regression bisection) | Binary search over steps/checkpoints/streams for the first probe divergence, with hash-chained probe ledgers (measured 53 probes where linear replay needed 1,010). |

## Field term → house term

| Field term | House reading |
|---|---|
| activation patching | An Act without preview/commit, custody, or consumer closure. The Instrument Trial's community arm implements it per published best practice (Zhang & Nanda) as the baseline. |
| circuit | A route candidate. It becomes a certified route only after the 9-gate battery with the native consumer as arbiter. |
| linear probe / dictionary readout | A reading, not a verdict. Measured cases in this corpus show probe verdicts inverting against consumer ground truth (cosine floor 0.186 while the consumer decodes *wolf*; 0.996 cosine reconstruction rendering the wrong animal). |
| steering vector | A typed payload candidate, subject to dtype/shape/address checks and dose controls. |
| checkpoint | A StateCut if and only if it retains the tensors needed for bit-exact resume plus a validated manifest; otherwise it is just a file. |
| ablation | A zero-write Act. Caution from E10: final-layer zero-writes can produce mechanical zeros (RMSNorm(0)=0, no lm_head bias) that read as circuit phenomena but are arithmetic artifacts. |

## Why the strictness exists (one paragraph)

Seven measurement traps documented in the flagship whitepaper — including a 0.996-cosine internal-state reconstruction that renders the wrong animal, and whole-image scalars that understated real effects three separate times — are the empirical record behind every "adds" column above. The stricter contract is not hygiene for its own sake; each clause exists because the unrestricted version produced a wrong verdict in a measured case.
