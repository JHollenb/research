---
title: "Figures: mdb and saturn-pub"
type: research-documentation
status: draft
updated: 2026-10-05
---

# Figures

Three figures support the paper. None is rendered yet; this file is the spec.

## fig1 — architecture diagram (hand-drawn, to do)

Status: **to do** (hand-drawn).

The one execution contract, with the four primitives and four planes made visible. Draw the
transaction spine left to right — `capture -> fork -> inspect -> intervene -> native
continuation -> compare -> commit / restore` — with:

- the four primitives called out on the spine: **StateCut** (sealed, restorable, bound to model
  + execution + parent identity), **fork** (isolated branch), **Act** (declared, fail-closed
  intervention), **Receipt** (immutable JSON evidence per operation);
- one family-adapter lane per architecture under the spine (Qwen2/2.5 decoder; Mamba v1 SSM;
  FLUX / SDXL diffusion), each showing its native stages;
- the four planes as horizontal bands crossing the spine: execution/state, memory
  (pages / residency / eviction / hydration / durable backing), evidence
  (`bisect` / `xref` / `claims` / `cite`), training-control (transaction + Future Forest);
- the durable export/import boundary (`export` -> `mdb verify` with no model -> fresh-process
  `resume`) drawn as the cut leaving one process and re-entering another.

Keep it legible in light and dark; no lab-internal codenames except the public API names used in
the paper (StateCut, Act, Future Forest, mrun).

## fig2 — comparison table as a figure

Status: **to do** (render Section 5's table).

Render the Section 5 prior-art comparison (rows: intervene+continue; cross-process durable
session; byte-exact replay receipt; diffusion support; SSM support; training-interval
transactions; offline model-free verification; serving-grade throughput — marked **no** for us;
columns: nnsight/NDIF, pyvene, TransformerLens, Patchscopes, vLLM/SGLang, Cartridges, Git-Theta,
mdb+saturn-pub). The point the figure must carry (ASSERTED): the contribution is the *combination*
of cells, not any single cell; every primitive has a close antecedent.

## fig3 — the demonstration table

Status: **to do** (render Section 3.1's table).

Render the seven-row cross-family demonstration table (demonstration, model/family, n/scope,
headline number, file). Every number is MEASURED with its source file; the figure must keep the
file path visible so a reader can trace each number. Do not round away the honest controls
(absent/wrong-page 0/4; mount≠prefill 6/6 vs 1/6; 0 of 96 cross-lane logit digests match).
