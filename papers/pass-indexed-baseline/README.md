---
title: Score Multi-Turn Interventions Against the Pass-Indexed Native
type: research-documentation
status: draft
updated: 2026-10-05
---

# Score Multi-Turn Interventions Against the Pass-Indexed Native, Not a Fixed Parent

[The paper](paper.md) is a short methods note. When you intervene on a model inside a multi-turn
context — a steering vector added at turn three, a key/value patch read by a later question — the
honest baseline is the model's own continuation with the *same* earlier turns already executed
(the **pass-indexed** native), not the single-turn parent you started from. We measure how large
the error is when you use the fixed parent instead: on Qwen2.5-1.5B (base) the later-turn native
answer log-probability moves by a median ~2.5 nats, and scoring a late key/value install against
the fixed parent flips the sign and/or the 1-nat-threshold conclusion in 11 of 12 pass≥1 cells; a
format-matched baseline removes none of those flips, so the error is carried content, not
formatting. We replicate the sign/threshold flips on an instruction-tuned model and at 7B in plain text; under
the chat template the error vanishes on saturated reads and returns on referential reads (median
drift 2.23 nats, install effect mis-sized by 2.72 nats between baselines). The
recipe is what any careful evaluator would already do; the contribution is the measured size of
the error you make when you skip it.

- [`paper.md`](paper.md): the note (~4 pages) — the problem, setup, the drift, the format-vs-content
  decomposition, the install-conclusion flips with a format-matched control, the instruct + 7B
  replication, a six-line recipe, limitations, and related work.
- Measurements come from two preregistered experiments in the Saturn workspace (job IDs, canaries,
  and harness details are in the paper's reproducibility appendix):
  `saturn/experiments/2026-10-02-pass-indexed-baseline/` (the 1.5B-base measurement and the
  format-vs-content control) and `saturn/experiments/2026-10-05-pass-indexed-instruct-7b/` (the
  instruct and 7B replication).

Every number is measured and traceable to a frozen report in those experiment folders. All runs
are greedy, single-seed, FP32 (the 7B replication uses a layer-paged engine; its full run is
labelled where it uses BF16), on synthetic two-fact scenes.
