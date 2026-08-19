---
title: FLUX.2 Klein 9B tracer profile
type: checkpoint-profile
model_id: black-forest-labs/FLUX.2-klein-9B
revision: 92196c8e11f7b6cf2b7493e037d8c5345c559216
claim_status: exploratory-anatomy-and-internal-physiology
---

# FLUX.2 Klein 9B

Klein 9B has 8 joint blocks, 24 single-stream blocks, 32 heads, and 1,056 tracer components.
The forward-free role budget assigns 66.53% of mass to operation/MLP, 7.39% each to
selector/address, payload, and carrier, 3.34% to clock, and 0.56% to content.

The live probe reconstructed 32 layers and 1,024 heads. `D0H29`, `S5H26`, `D0H27`, and `D0H7`
led local sensitivity. The tested `D0MLP` lesion changed the clean internal prediction by
`0.149558` MSE versus `0.018289` for `D0H0`. Early joint and mid-depth single-stream sites both
remain candidates; the probe does not identify lexical or visual semantics.

The repeated first-joint MLP candidate supports a cross-model search order, not an address-level
transfer from Klein 4B.

Source: [original Klein 9B profile](../../../../obsidian/experiments/bfl-tracer-2026-08-06/flux2-klein-9b.md).

