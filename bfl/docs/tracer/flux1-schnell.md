---
title: FLUX.1 Schnell tracer profile
type: checkpoint-profile
model_id: black-forest-labs/FLUX.1-schnell
revision: 741f7c3ce8b383c54771c7003378a50191e9efe9
claim_status: exploratory-anatomy-and-internal-physiology
---

# FLUX.1 Schnell

Schnell is the deepest transformer in the cohort: 19 joint blocks followed by 38 single-stream blocks, 24 heads, and 1,425 tracer components. Its forward-free anatomy assigns 48.26% of parameter mass to operation families, 27.50% to clock/modulation paths, and 6.03% to each of the four attention-facing families.

The bounded live probe reconstructed 1,368 heads across 57 layers. The strongest local-sensitivity sites were late single-stream heads, led by `S18H1`, `S17H4`, and `S13H8`; a tested early joint MLP lesion was larger than the tested early attention-head lesion. This nominates a search frontier for Schnell, not a prompt-to-image circuit or a semantic label for those heads.

`joint.i` and `single.i` are Schnell-local structural addresses. Schnell's 19-joint topology makes its address numbers non-interchangeable with Klein or Dev addresses.

Source: [original Schnell profile](../../../../obsidian/experiments/bfl-tracer-2026-08-06/flux1-schnell.md).
