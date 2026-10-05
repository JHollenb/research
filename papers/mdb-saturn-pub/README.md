---
title: "mdb and saturn-pub: Durable, Receipted, Forkable Execution of Frozen Models"
type: research-documentation
status: draft
updated: 2026-10-05
---

# mdb and saturn-pub

[The paper](paper.md) is a tools / datasets-and-benchmarks note (the genre of nnsight
[2407.14561] and pyvene [2403.07809]) describing two independently installable Python packages
that make a frozen model run an inspectable, branchable, receipted and durable transaction over
one execution contract — and that span transformer, state-space (SSM) and diffusion families
under that same contract.

- `saturn-pub` (`saturn_pub`): in-process sessions, forks, declared interventions (`Act`s),
  hash-chained receipts, an offline evidence plane, and reversible (transactional) training.
- `mdb-runtime` (`mdb`): durable cross-process sessions, managed branch residency with eviction
  and hydration, portable export/import, and offline byte verification of an exported run with
  no model loaded.

The contract's four primitives are a sealed **StateCut**, an isolated **fork**, a declared
**Act**, and an immutable **Receipt**; over them sit a family adapter per architecture, a memory
plane, an evidence plane (`bisect`/`xref`/`claims`/`cite`), and a transactional training
controller with a persistent version-control forest (the **Future Forest**).

## What is in the paper

- Section 1 — the problem: interventions run in process, are unreceipted, and are usually
  language-model-only; and the question of who judges (the native consumer).
- Section 2 — design: the execution contract, four planes, adapters per family, durable
  export/import, the evidence plane, transactional training, and what is deliberately out of
  scope (no serving-throughput claim).
- Section 3 — what is measured: a seven-row cross-family demonstration table (shared K/V
  ancestry 40.91% + 8/8 tokens; durable residency/eviction/restart; CUDA-VMM aliasing
  bit-identical; routed working-set 1.859x at batch 4; 2,048-page archive read 4/4; scene
  compiler 21/21 RGB across 5 diffusion families; Mamba fork bit-exact + 2.2e-4 staged replay),
  the packaged qualification records, and the evidence plane / Future Forest numbers.
- Section 4 — first users: Time-Formed Circuits, Single-Site Tests Miss Distributed Stores,
  Pass-Indexed Baseline, the InterpBench instrument audit, and the circuit-tracer flagship
  (Gemma-2-2B single-feature graph-vs-native agreement 0.857 [0.835, 0.879]).
- Section 5 — comparison with prior art (nnsight / pyvene / TransformerLens / Patchscopes /
  vLLM-SGLang / Cartridges / Git-Theta) with the delta for each.
- Section 6 — limitations, in full: no external user yet; the efficiency wins are not
  equal-semantics; mount ≠ prefill (6/6 vs 1/6); the Future Forest flagship is a reindex;
  bounded adapter coverage; and the causal-mask defect a retired sibling harness carried past its
  own replay checks (on record in the time-circuit-scaffold paper).
- Section 7 — the three demonstrations the paper still needs before a main-track submission
  (outside user reproduces from an exported cut; an equal-semantics cost win; an end-to-end
  pipeline no other framework runs), marked not yet done.
- Section 8 — availability (install lines; Apache-2.0; mrun-pub for optional scheduler/diffusion
  extras).

## Labeling and provenance

Every number in the paper is marked **MEASURED** with the file that holds it, or **not
measured** where no file does; every interpretation is marked **ASSERTED**. The public toolkit
is version 0.4.0, Apache-2.0 (`saturn-pub/pyproject.toml`, `saturn-pub/LICENSE`). The runtime
demonstrations are summarized in the lab's blog evidence review
(`obsidian/blog/2026-10-01-131907-saturn-vm-model-virtual-memory-evidence-checklist.md`) and the
Saturn bible (`saturn/docs/SATURN-BIBLE.md`), with the per-experiment report paths cited in the
paper's §3 table. The packaged qualification records are in
`saturn-pub/packages/mdb/docs/QUALIFICATION.md`.

See [`figures/README.md`](figures/README.md) for the figure list (hand-drawn architecture
diagram to do; the comparison table and the demonstration table reproduced as figures).
