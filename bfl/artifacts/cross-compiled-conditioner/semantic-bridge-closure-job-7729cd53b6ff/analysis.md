# Saturn semantic-bridge closure panel

This artifact is the closure panel for the provisional Smol/Mamba to Qwen semantic bridge. The FLUX.2 suffix, latent, scheduler, image-token IDs, and VAE remained fixed. Six baselines were captured first; the remaining rows are exact scalar suffix replays from durable family checkpoints.

## Specimen and execution contract

- semantic pair: `scene-snow-to-space`
- source: `a photorealistic red fox sitting in fresh snow at dawn, soft red light`
- target: `a photorealistic red fox sitting on a rocky lunar plain beneath a star-filled deep-space sky at dawn, soft red light`
- suffix fingerprint: `6204b2ba5ab485cb7f8269ce3febd3ba5815878b75316ba12f1c6b9b0e69c9ec`
- initial latent fingerprint: `14afb6217c7dbd7315930f48fea7c4024a82359602ed0ad7b74cf4cdf4b71f94`
- scheduler fingerprint: `ab51b5853ebd0b9408c2477fa4bb0730976bb04dff08e97d7ebfb4f7af86cb0e`
- image-ID fingerprint: `a2350f586c22955f8789ba7ace8f914c994c8297a007fe962a790a2aab9b9991`
- local evaluations: `30` = 6 baselines + 2 no-ops + 22 branches
- one-lease validation: `True`
- mrun policy: one guarded resident CUDA lease, no per-branch submission, no automatic retry

## Baseline images

| family | source | target |
|---|---|---|
| qwen | [source](baseline_qwen_a.png) | [target](baseline_qwen_b.png) |
| smol | [source](baseline_smol_a.png) | [target](baseline_smol_b.png) |
| mamba | [source](baseline_mamba_a.png) | [target](baseline_mamba_b.png) |

## Closure branches

The normalized rescue is measured against the family baseline and the Qwen source image. A value near one means the intervention removed most of the family mismatch for this specimen; it is not yet evidence of a trained universal bridge.

| family | branch | normalized rescue | Qwen-A MAD | Qwen-B MAD | subject MAD | background MAD | image |
|---|---|---:|---:|---:|---:|---:|---|
| smol | `checkpoint_noop` | — | 0.0000 | — | — | — | [image](checkpoint_noop_smol.png) |
| smol | `sham_same_value` | 0.000000 | 72.3326 | 65.7740 | 66.0032 | 76.2752 | [image](smol_sham_same_value.png) |
| smol | `full_joint4_text_all_steps` | 0.751136 | 18.0010 | 86.1183 | 16.5695 | 18.8927 | [image](smol_full_joint4_text_all_steps.png) |
| smol | `stable_channels_joint4_text_all_steps` | 0.035587 | 69.7585 | 52.3377 | 60.0288 | 75.8191 | [image](smol_stable_channels_joint4_text_all_steps.png) |
| smol | `lexical_slots_stable_channels_joint4_text_all_steps` | -0.002272 | 72.4970 | 65.2994 | 66.0162 | 76.5338 | [image](smol_lexical_slots_stable_channels_joint4_text_all_steps.png) |
| smol | `contrast_slots_stable_channels_joint4_text_all_steps` | 0.047056 | 68.9289 | 53.1651 | 59.8210 | 74.6022 | [image](smol_contrast_slots_stable_channels_joint4_text_all_steps.png) |
| smol | `low_energy_channels_joint4_text_all_steps` | -0.000456 | 72.3656 | 66.7690 | 67.1920 | 75.5883 | [image](smol_low_energy_channels_joint4_text_all_steps.png) |
| smol | `full_joint4_text_image_all_steps` | 1.000000 | 0.0000 | 94.8913 | 0.0000 | 0.0000 | [image](smol_full_joint4_text_image_all_steps.png) |
| smol | `full_single0_text_all_steps` | 0.438497 | 40.6150 | 87.0586 | 32.8128 | 45.4749 | [image](smol_full_single0_text_all_steps.png) |
| smol | `stable_channels_single0_text_all_steps` | 0.020556 | 70.8457 | 51.1506 | 60.3183 | 77.4033 | [image](smol_stable_channels_single0_text_all_steps.png) |
| smol | `full_single0_text_image_all_steps` | 1.000000 | 0.0000 | 94.8913 | 0.0000 | 0.0000 | [image](smol_full_single0_text_image_all_steps.png) |
| smol | `wrong_prompt_joint4_text_all_steps` | -0.265231 | 91.5175 | 14.0519 | 63.2043 | 109.1538 | [image](smol_wrong_prompt_joint4_text_all_steps.png) |
| mamba | `checkpoint_noop` | — | 0.0000 | — | — | — | [image](checkpoint_noop_mamba.png) |
| mamba | `sham_same_value` | 0.000000 | 78.1209 | 80.1833 | 77.0769 | 78.7712 | [image](mamba_sham_same_value.png) |
| mamba | `full_joint4_text_all_steps` | 0.816574 | 14.3294 | 88.1333 | 14.4204 | 14.2727 | [image](mamba_full_joint4_text_all_steps.png) |
| mamba | `stable_channels_joint4_text_all_steps` | 0.051204 | 74.1208 | 48.4889 | 61.7840 | 81.8053 | [image](mamba_stable_channels_joint4_text_all_steps.png) |
| mamba | `lexical_slots_stable_channels_joint4_text_all_steps` | 0.002529 | 77.9233 | 66.1775 | 70.1821 | 82.7453 | [image](mamba_lexical_slots_stable_channels_joint4_text_all_steps.png) |
| mamba | `contrast_slots_stable_channels_joint4_text_all_steps` | 0.054259 | 73.8821 | 49.1182 | 62.1197 | 81.2090 | [image](mamba_contrast_slots_stable_channels_joint4_text_all_steps.png) |
| mamba | `low_energy_channels_joint4_text_all_steps` | -0.057809 | 82.6370 | 67.2905 | 76.4643 | 86.4820 | [image](mamba_low_energy_channels_joint4_text_all_steps.png) |
| mamba | `full_joint4_text_image_all_steps` | 1.000000 | 0.0000 | 94.8913 | 0.0000 | 0.0000 | [image](mamba_full_joint4_text_image_all_steps.png) |
| mamba | `full_single0_text_all_steps` | 0.713756 | 22.3617 | 85.0738 | 25.0632 | 20.6788 | [image](mamba_full_single0_text_all_steps.png) |
| mamba | `stable_channels_single0_text_all_steps` | 0.071472 | 72.5374 | 49.9146 | 61.8405 | 79.2006 | [image](mamba_stable_channels_single0_text_all_steps.png) |
| mamba | `full_single0_text_image_all_steps` | 1.000000 | 0.0000 | 94.8913 | 0.0000 | 0.0000 | [image](mamba_full_single0_text_image_all_steps.png) |
| mamba | `wrong_prompt_joint4_text_all_steps` | -0.171929 | 91.5522 | 14.7263 | 63.2855 | 109.1595 | [image](mamba_wrong_prompt_joint4_text_all_steps.png) |

## Mapped support

The persisted boundary manifest is in `report.json`. It records the foreign and Qwen text states at `joint.3` and `joint.4` for every prompt side and scheduler step, together with lexical slots, stable channels, stepwise contrast slots, and low-energy channel controls.

| family | lexical slots | stable channels | contrast fingerprints |
|---|---:|---|---|
| smol | 32 | `92, 131, 214, 355, 364, 454, 472, 1444, 2301, 2433, 2651, 2769, 2772, 2808` | 4 steps |
| mamba | 32 | `92, 131, 214, 355, 364, 454, 472, 1444, 2301, 2433, 2651, 2769, 2772, 2808` | 4 steps |

## Interpretation boundary

One seed and one prompt pair. This closure panel determines the smallest all-step Qwen donor state that restores the frozen suffix; it does not establish a standalone learned Smol/Mamba bridge or a universal channel circuit.

The full all-step donor branches are the causal ceiling. The restricted branches test whether a smaller temporal semantic bridge—stable channels, lexical slots, contrast slots, or their controls—reproduces that ceiling without touching the denoiser, scheduler, image stream, or VAE.

