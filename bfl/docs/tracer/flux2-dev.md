---
title: FLUX.2 Dev tracer profile
type: checkpoint-profile
model_id: black-forest-labs/FLUX.2-dev
revision: 26afe3a78bb242c0a8bb181dcc8937bb16e5c66c
claim_status: exploratory-paged-forward-causal-evidence
---

# FLUX.2 Dev

Dev has 8 joint blocks, 48 single-stream blocks, 48 heads, and 2,744 tracer components. Its 32.223B-parameter transformer is about 64.45 GB in BF16, so the live assay used paged native forward execution on a 16 GB GPU rather than retaining a full autograd graph.

The forward-free role budget assigns 67.48% to operation/MLP, 7.50% each to the four attention-facing families, 2.24% to clock, and 0.30% to content. Three streamed passes measured 56 layers and 2,688 reconstructed heads; the matched `D0MLP` lesion changed the clean internal prediction by `0.171359` MSE. That is a real internal causal edge under the declared probe, not a complete Dev semantic circuit.

The execution boundary is part of the result: paged forward-only evidence establishes a useful Dev tracer path, while full backward MRI/Winder remains unearned in this memory configuration.

Source: [original Dev profile](../../../../obsidian/experiments/bfl-tracer-2026-08-06/flux2-dev.md).
