---
title: FLUX.2 Klein Base 4B tracer profile
type: checkpoint-profile
model_id: black-forest-labs/FLUX.2-klein-base-4B
revision: a3b4f4849157f664bdbc776fd7453c2783562f4d
claim_status: exploratory-anatomy-and-internal-physiology
---

# FLUX.2 Klein Base 4B

The full-capacity Base 4B checkpoint has 5 joint blocks, 20 single-stream blocks, 24 heads, and
625 tracer components. Its forward-free role budget is 65.75% operation/MLP, 7.31% each for
selector/address, payload, and carrier families, 4.40% clock, and 0.62% content.

The live internal probe reconstructed 25 layers and 600 heads. `D0H19`, `D0H7`, and `S18H16` led
gradient × activation, while the tested `D0MLP` lesion changed the clean internal prediction by
`0.153319` MSE versus `0.015214` for `D0H0`. These are candidate sites for prompt/image follow-up,
not semantic circuit labels.

This is the diagnostic comparison checkpoint for the recipient-native patch. It is not the runtime
donor for the distilled recipient package.

Source: [original Base 4B profile](../../../../obsidian/experiments/bfl-tracer-2026-08-06/flux2-klein-base-4b.md).

