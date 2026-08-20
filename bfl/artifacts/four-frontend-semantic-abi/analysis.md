# Saturn synchronized cross-family four-axis map

This is the first single-specimen family-delta map that measures Qwen, Smol, and Mamba on the same FLUX.2 suffix, semantic pair, latent, image IDs, scheduler, and checkpoint contract.

## Specimen

- semantic pair: `heldout-two-blue-foxes-snow-to-space`
- source: `a minimal flat illustration showing exactly two separate blue foxes arranged in a horizontal row on pure white, no other objects`
- target: `a minimal flat illustration showing exactly two separate blue foxes arranged in a horizontal row on a star-filled lunar plain, no other objects`
- suffix fingerprint: `6204b2ba5ab485cb7f8269ce3febd3ba5815878b75316ba12f1c6b9b0e69c9ec`
- initial latent fingerprint: `71906fca2e96c7e7045999235b9d01406f0a9662e8e3127917a8a0706a9835c4`
- image-ID fingerprint: `a2350f586c22955f8789ba7ace8f914c994c8297a007fe962a790a2aab9b9991`
- scheduler fingerprint: `ab51b5853ebd0b9408c2477fa4bb0730976bb04dff08e97d7ebfb4f7af86cb0e`
- observational coordinates: `72`
- causal continuation: exact scalar checkpoint suffixes

The mapped quantities are `R_F(p) = H_Q(p) - H_F(p)` and `C_F = [H_Q(b)-H_Q(a)] - [H_F(b)-H_F(a)]`. The worker independently checks `C_F = R_F(b)-R_F(a)` at every coordinate.

## Baseline images

| family | source image | target image | source MAD vs Qwen | target MAD vs Qwen |
|---|---|---|---:|---:|
| qwen | [source](baseline_qwen_a.png) | [target](baseline_qwen_b.png) | 0.0000 | 0.0000 |
| smol | [source](baseline_smol_a.png) | [target](baseline_smol_b.png) | 100.0287 | 108.1917 |
| mamba | [source](baseline_mamba_a.png) | [target](baseline_mamba_b.png) | 38.3885 | 113.2790 |

## Lexical-to-target-slot map

Source positions remain tokenizer-family local. Smol and Mamba positions are mapped into the adapter's 512 learned target slots by the actual fitted cross-attention weights; they are never relabeled as Qwen token IDs.

| family | source span A | source span B | mapping | top target slots |
|---|---|---|---|---|
| qwen | `20:22` | `20:25` | `native_one_to_one_position` | `279, 206, 261, 491, 480, 451, 293, 172` |
| smol | `16:18` | `16:22` | `trained_adapter_cross_attention` | `355, 362, 70, 354, 361, 198, 335, 353` |
| mamba | `17:19` | `17:23` | `trained_adapter_cross_attention` | `414, 482, 462, 202, 130, 173, 351, 463` |

## Strongest synchronized internal deltas

Rows are ranked by contrast-of-contrasts RMS. A high direct residual can be a generic family codec offset; a high contrast identifies the part of that offset that changes when the requested scene changes.

| family | rank | site | stream | step | timestep | contrast RMS | semantic cosine |
|---|---:|---|---|---:|---:|---:|---:|
| smol | 1 | `single.0` | `text` | 3 | 0.703125 | 280.706848 | -0.008506 |
| smol | 2 | `joint.4` | `text` | 3 | 0.703125 | 279.024719 | -0.007344 |
| smol | 3 | `single.0` | `text` | 2 | 0.875000 | 269.414490 | -0.029890 |
| smol | 4 | `joint.4` | `text` | 2 | 0.875000 | 268.323303 | -0.028712 |
| smol | 5 | `single.0` | `text` | 1 | 0.957031 | 217.892975 | -0.039213 |
| smol | 6 | `joint.4` | `text` | 1 | 0.957031 | 217.426285 | -0.037802 |
| smol | 7 | `single.0` | `text` | 0 | 1.000000 | 149.525925 | 0.000528 |
| smol | 8 | `joint.4` | `text` | 0 | 1.000000 | 148.635468 | 0.002479 |
| smol | 9 | `joint.3` | `text` | 1 | 0.957031 | 17.888491 | -0.018486 |
| smol | 10 | `joint.3` | `text` | 0 | 1.000000 | 15.907450 | -0.006933 |
| smol | 11 | `joint.3` | `text` | 2 | 0.875000 | 15.046165 | -0.013668 |
| smol | 12 | `joint.2` | `text` | 1 | 0.957031 | 11.359931 | -0.040159 |
| mamba | 1 | `single.0` | `text` | 3 | 0.703125 | 277.582672 | -0.050747 |
| mamba | 2 | `joint.4` | `text` | 3 | 0.703125 | 275.962128 | -0.050153 |
| mamba | 3 | `single.0` | `text` | 2 | 0.875000 | 268.304718 | -0.058148 |
| mamba | 4 | `joint.4` | `text` | 2 | 0.875000 | 267.263092 | -0.057856 |
| mamba | 5 | `single.0` | `text` | 1 | 0.957031 | 214.435425 | 0.065716 |
| mamba | 6 | `joint.4` | `text` | 1 | 0.957031 | 214.049026 | 0.064708 |
| mamba | 7 | `single.0` | `text` | 0 | 1.000000 | 137.932465 | 0.001605 |
| mamba | 8 | `joint.4` | `text` | 0 | 1.000000 | 137.260178 | 0.001711 |
| mamba | 9 | `joint.3` | `text` | 1 | 0.957031 | 16.825060 | 0.007903 |
| mamba | 10 | `joint.3` | `text` | 0 | 1.000000 | 15.178294 | -0.000711 |
| mamba | 11 | `joint.3` | `text` | 2 | 0.875000 | 13.725033 | 0.005026 |
| mamba | 12 | `joint.2` | `text` | 1 | 0.957031 | 10.686750 | 0.008730 |

## Exact checkpoint interventions

Every row below is a separate scalar Saturn suffix resume. No batch-dependent screening output is used as causal evidence.

| family | branch | coordinate | rescue | subject MAD vs Qwen | background MAD vs Qwen | image |
|---|---|---|---:|---:|---:|---|
| smol | `sham_same_value` | `qwen-vs-smol:single.0:text:step3` | 0.000000 | 122.0893 | 87.0337 | [image](smol_sham_same_value.png) |
| smol | `positive_full_site_donor` | `qwen-vs-smol:single.0:text:step3` | 0.122182 | 113.9225 | 72.4234 | [image](smol_positive_full_site_donor.png) |
| smol | `semantic_top_tokens` | `qwen-vs-smol:single.0:text:step3` | 0.093841 | 116.2734 | 75.5434 | [image](smol_semantic_top_tokens.png) |
| smol | `semantic_top_channels` | `qwen-vs-smol:single.0:text:step3` | -0.050185 | 125.4041 | 93.0582 | [image](smol_semantic_top_channels.png) |
| smol | `semantic_token_channel_intersection` | `qwen-vs-smol:single.0:text:step3` | -0.042971 | 124.6179 | 92.3746 | [image](smol_semantic_token_channel_intersection.png) |
| smol | `spatial_token_channel_intersection` | `qwen-vs-smol:single.0:image:step2` | -0.009176 | 123.3019 | 87.7780 | [image](smol_spatial_token_channel_intersection.png) |
| smol | `selected_site_all_steps` | `qwen-vs-smol:single.0:image:step2` | 0.934990 | 9.4953 | 4.7402 | [image](smol_selected_site_all_steps.png) |
| smol | `packed_return_intersection` | `qwen-vs-smol:scheduler.return:image:step3` | 0.193679 | 81.3188 | 80.2644 | [image](smol_packed_return_intersection.png) |
| mamba | `sham_same_value` | `qwen-vs-mamba:single.0:text:step3` | 0.000000 | 72.8106 | 18.1119 | [image](mamba_sham_same_value.png) |
| mamba | `positive_full_site_donor` | `qwen-vs-mamba:single.0:text:step3` | 0.009751 | 72.2304 | 17.8588 | [image](mamba_positive_full_site_donor.png) |
| mamba | `semantic_top_tokens` | `qwen-vs-mamba:single.0:text:step3` | 0.006858 | 72.4123 | 17.9282 | [image](mamba_semantic_top_tokens.png) |
| mamba | `semantic_top_channels` | `qwen-vs-mamba:single.0:text:step3` | -0.009411 | 73.6543 | 18.1890 | [image](mamba_semantic_top_channels.png) |
| mamba | `semantic_token_channel_intersection` | `qwen-vs-mamba:single.0:text:step3` | -0.008094 | 73.4779 | 18.2126 | [image](mamba_semantic_token_channel_intersection.png) |
| mamba | `spatial_token_channel_intersection` | `qwen-vs-mamba:single.0:image:step3` | -0.001301 | 72.9676 | 18.0988 | [image](mamba_spatial_token_channel_intersection.png) |
| mamba | `selected_site_all_steps` | `qwen-vs-mamba:single.0:image:step3` | 0.821394 | 10.1604 | 4.9102 | [image](mamba_selected_site_all_steps.png) |
| mamba | `packed_return_intersection` | `qwen-vs-mamba:scheduler.return:image:step3` | 0.297029 | 48.4800 | 14.3248 | [image](mamba_packed_return_intersection.png) |

## Controls and interpretation boundary

- validation passed: `True`
- residual identity passed: `True`
- exact coordinate coverage: `True`
- exact checkpoint no-ops: `True`
- batch-dependent evidence used: `False`

Fresh one-seed held-out count/color/scene pair. Qwen, Smol, and Mamba are independently lowered into one frozen Klein suffix; this is an exploratory three-family ABI component for joining with the structured frontend probe, not a four-frontend closure.

Raw selected direct/contrast tensors and the two family checkpoints are content-addressed in MinIO; their manifest and tensor URIs are in `report.json` under `persisted_boundaries` and `checkpoint_handles`.
