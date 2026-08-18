# FLUX.2 Dev VAE FP32 decoder-boundary probe

Identical raw 32-channel VAE latents were decoded by the native Klein VAE and the downloaded Dev VAE in float32. This is a direct decoder observation, not an end-to-end generation or quality certificate.

- Latents: `3`
- Output mean MAE: `0.00056828953`
- Output mean RMSE: `0.000800737685`
- Output max absolute delta: `0.0309097469`
- Output mean cosine: `0.999991007`
- Mean changed clipped fraction: `0.0724919637`

| Seed index | MAE | RMSE | Max abs | Cosine | Changed clipped fraction |
|---:|---:|---:|---:|---:|---:|
| 0 | 0.000556411397 | 0.000784848301 | 0.0175884329 | 0.999991025 | 0.0711606344 |
| 1 | 0.000585075746 | 0.000824307182 | 0.0309097469 | 0.999991024 | 0.0746218363 |
| 2 | 0.000563381447 | 0.000793057572 | 0.0237691402 | 0.999990972 | 0.0716934204 |

## Decoder-stage trajectory

- `decoder.conv_out` — mean MAE `0.00056828953`, mean cosine `0.999991007`
- `decoder.mid_block` — mean MAE `0.00212121496`, mean cosine `0.999992989`
- `decoder.up_blocks.0` — mean MAE `0.00625360294`, mean cosine `0.999993950`
- `decoder.up_blocks.1` — mean MAE `0.0362545579`, mean cosine `0.999984625`
- `decoder.up_blocks.2` — mean MAE `0.0626660008`, mean cosine `0.999983760`
- `decoder.up_blocks.3` — mean MAE `0.0434122786`, mean cosine `0.999998623`
- `post_quant_conv` — mean MAE `0.000947646175`, mean cosine `0.999998339`

## Interpretation

The FP32 probe tests whether the static Dev-VAE numerical difference survives the decoder boundary under identical inputs. It does not identify the cause of the difference and does not establish perceptual quality, semantic behavior, or end-to-end pipeline equivalence.
