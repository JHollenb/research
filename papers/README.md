---
title: Research Papers
type: research-documentation
status: active
updated: 2026-10-05
---

# Research Papers

Six manuscripts are current. Everything else in this directory is an earlier draft, a parked note, or a companion that one of the six absorbed; those are listed at the end with what superseded them. Headline numbers across the six are bound to their result files in the [evidence registry](evidence-registry/README.md) (19 claims, re-checkable offline with `saturn-pub evidence claims verify --check`).

## Current manuscripts

| | Paper | One line | Strongest evidence |
|---|---|---|---|
| 1 | [Time-Formed Circuits: Formation, Commitment, and Causal Use](time-formed-circuits/README.md) | Some circuits are built over depth; the formed state commits to a late key/value band that can be moved between models. | Block removes 73–92%, independent-recipient transplant restores 71–99%, eight decoder families, four blind; matched transcoder interchange 0.31 vs native cut 0.94. |
| 2 | [Single-Site Tests Miss Distributed Stores](pointwise-instruments-miss-distributed-circuits/README.md) | Single-step or single-layer patching reports "nothing necessary" where the whole path is necessary and sufficient. | FLUX.2 22% / 0.13% / 91%; LM single layer ≤18% vs second half 81–104%; preregistered SAELens and Gemma Scope head-to-head; blind-graded instrument trial with verifiers. |
| 3 | [One Grokked Circuit Is Not a Certificate](instrument-audit-interpbench/README.md) | Calibrating an instrument on one known circuit under-determines the constraints it earns. | All 86 InterpBench circuits, real generators, hash-frozen scorer; baselines 0.990 / 0.976 / 0.892; two lab instruments at chance in their certified forms, rescued by one constraint change. |
| 4 | [Score Multi-Turn Interventions Against the Pass-Indexed Native](pass-indexed-baseline/README.md) | The baseline for a mid-context intervention is the model's own continuation, not the single-turn parent. | 2.5-nat drift, 11 of 12 conclusions flip on Qwen2.5-1.5B; replicates on instruct and 7B in plain text; chat template mis-sizes the effect by 2.7 nats on referential reads. |
| 5 | [Dynamic Circuits Loop Through a Stable Time Scaffold](time-circuit-scaffold/README.md) | The architecture hypothesis, stated with eight falsifiers and their status. | Query-gated authority 16/16, prospective reader profile 8/8, fine-tune asymmetry; two falsifiers fired and are reported as such. |
| 6 | [mdb and saturn-pub](mdb-saturn-pub/README.md) | Tools note for the two public packages that run a frozen model as a receipted, forkable, durable transaction across families. | Cross-family demonstrations (bit-identical CUDA-VMM aliasing, 21/21 RGB parity across five diffusion families, bit-exact Mamba fork); novelty claimed only for the combination. |

Suggested reading order: 1, 2, 3, then 4 as the methods companion, 5 for the theory, 6 for the tooling.

## Supporting documents

- [The Circuit That Survived Its Coordinates](../bfl/docs/certified-semantic-circuits/README.md): the certified distributed semantic route in FLUX.2 Klein 4B that paper 2 builds on.
- [Evidence registry](evidence-registry/README.md): the claim ledger and the script that built it.
- [Submission review, 2026-10-02](submission-review-2026-10-02.md) and its successor [2026-10-05](submission-review-2026-10-05.md): reviewer-style readiness assessments of the current manuscripts.

## Earlier drafts and parked notes

| Directory | Status |
|---|---|
| [space-and-time-circuits](space-and-time-circuits/README.md) | Outline and early draft; its spine became paper 1. |
| [scaffolds-and-dynamic-circuits](scaffolds-and-dynamic-circuits/README.md) | Three drafts of the architecture thesis; superseded by paper 5. |
| [integral-residual-dynamics](integral-residual-dynamics/README.md) | Theory companion to paper 2; its two usable results (isolated-swap, transport cut) were folded into paper 2 §4.7–4.8. |
| [capabilities-as-transactions](capabilities-as-transactions/README.md) | Cross-family dossier on a behavior as a joint key/value transaction; shelved, its measured cells live in paper 1 and paper 5. |
| [formed-state-faithfulness](formed-state-faithfulness/README.md) | Parked after review; chain-of-thought formed-state result, to fold into paper 5. |
| [phaselock-kv-shifts](phaselock-kv-shifts/README.md) | Rotation swamping in low-precision RoPE keys; numerics draft, standalone. |
| [rounding-placement](rounding-placement/README.md) | Where to round in low-precision attention; numerics draft, standalone. |
| [clocked-ledger-memory](clocked-ledger-memory/README.md) | Exact time-aware memory for a frozen language model; standalone draft. |
