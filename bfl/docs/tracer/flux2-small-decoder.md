---
title: FLUX.2 Small Decoder tracer profile
type: checkpoint-profile
model_id: black-forest-labs/FLUX.2-small-decoder
revision: a3efc24f613ef42d9428af62fdbd6f5fd8856c4a
claim_status: exploratory-decoder-physiology
---

# FLUX.2 Small Decoder

Small Decoder is a 62.373M-parameter convolutional VAE decoder, not a DiT denoiser. It therefore does not receive invented `joint.*` or attention-head semantics. Its decoder-native anatomy uses convolution, residual, upsampling, and output sites.

The real latent-to-pixel probe measured `conv_in`, `up_blocks.2.resnets.0.conv_shortcut`, and `conv_out`. `conv_in` had the largest local sensitivity (`9.4486e-5`) and largest tested lesion effect (`0.009834` MSE); the late shortcut's lesion was `0.005189` MSE. These are internal pixel-decoding effects, not prompt semantics or image-quality scores.

The decoder is retained as a boundary case in the seven-artifact campaign: the common instrument contract survives, but the transformer-specific role grammar correctly does not.

Source: [original Small Decoder profile](../../../../obsidian/experiments/bfl-tracer-2026-08-06/flux2-small-decoder.md).
