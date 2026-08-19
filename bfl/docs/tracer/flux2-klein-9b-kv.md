---
title: FLUX.2 Klein 9B-KV tracer profile
type: checkpoint-profile
model_id: black-forest-labs/FLUX.2-klein-9b-kv
revision: a6dfb36eca3a3906eb2fd460795adfb844e5fcce
claim_status: exploratory-variant-comparison
---

# FLUX.2 Klein 9B-KV

The 9B-KV variant shares the measured 8-joint/24-single, 32-head topology and 1,056-component
role grammar of ordinary Klein 9B. Its reported static budget is likewise 66.53% operation/MLP,
7.39% each for the attention-facing quartet, 3.34% clock, and 0.56% content.

The live probe reconstructed 32 layers and 1,024 heads, but its sensitivity ordering differed:
`D0H29` led and `S22H25` ranked second, near the end of the single stream, whereas ordinary 9B
ranked `S5H26` second. The tested `D0MLP` lesion was `0.155476` MSE versus `0.015150` for `D0H0`.

This is the useful counterexample to static-topology transfer: shared anatomy supports a common
search grammar, while variant-specific weights and KV behavior can move dynamic candidates.

Source: [original Klein 9B-KV profile](../../../../obsidian/experiments/bfl-tracer-2026-08-06/flux2-klein-9b-kv.md).

