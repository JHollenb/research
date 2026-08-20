# Saturn TECM v4 scheduler-closed repair

The all-512-row TECM compiler is trained through the frozen FLUX.2 semantic route, denoiser action, and real scheduler transition. All rendered arms resume one cut-0 checkpoint as exact scalar suffixes.

## Execution contract

- checkpoint: `traj-41ae05f05547bad43078e6a046982286`
- native same-process duplicate exact: `True`
- real scheduler parity max-abs: `0`
- carrier warm-start steps: `900`
- scheduler-closure steps: `240`
- local exact suffixes: `23`
- mrun submissions/model loads: `1 / 1`

## Closed objective

Loss fell from `0.419610` to `0.080188`. The table measures the same held target steps before and after scheduler closure.

| component | before | after | reduction |
|---|---:|---:|---:|
| `joint.4.image` | 0.005352 | 0.004438 | 0.000914 |
| `joint.4.text` | 0.540859 | 0.479982 | 0.060877 |
| `noise_action` | 0.038231 | 0.026938 | 0.011293 |
| `scheduler_continuation` | 0.028758 | 0.020353 | 0.008405 |
| `semantic_residual` | 1.164362 | 1.139586 | 0.024776 |
| `single.0.image` | 0.013976 | 0.010803 | 0.003173 |
| `single.0.text` | 0.540767 | 0.480723 | 0.060044 |

## Rendered acceptance

| prompt | split | TECM v3 MAD | scheduler-closed MAD | improvement | semantic residual cosine before → after | images |
|---|---|---:|---:|---:|---:|---|
| blue_fox | downstream_held_out | 64.2505 | 64.5730 | -0.3225 | -0.0193 → 0.0213 | [native](native_qwen_blue_fox.png) / [v3](tecm_v3_blue_fox.png) / [closed](scheduler_closed_blue_fox.png) |
| cat | downstream_held_out | 74.4253 | 73.5311 | 0.8942 | 0.0462 → 0.0311 | [native](native_qwen_cat.png) / [v3](tecm_v3_cat.png) / [closed](scheduler_closed_cat.png) |
| corgi | downstream_held_out | 96.2340 | 87.6044 | 8.6296 | -0.0637 → -0.0060 | [native](native_qwen_corgi.png) / [v3](tecm_v3_corgi.png) / [closed](scheduler_closed_corgi.png) |
| fox | downstream_held_out | 70.4207 | 71.0605 | -0.6398 | 0.0140 → 0.0860 | [native](native_qwen_fox.png) / [v3](tecm_v3_fox.png) / [closed](scheduler_closed_fox.png) |

## Same-prompt conditioner seed panel

Prompt: `a corgi astronaut floating in a space station, editorial illustration`

| seed | native Qwen | TECM v3 | scheduler-closed TECM v4 | v3 MAD | closed MAD |
|---:|---|---|---|---:|---:|
| 7217 | [image](native_qwen_corgi.png) | [image](tecm_v3_corgi.png) | [image](scheduler_closed_corgi.png) | 96.2340 | 87.6044 |
| 7218 | [image](seed_panel_native_qwen_7218.png) | [image](seed_panel_tecm_v3_7218.png) | [image](seed_panel_scheduler_closed_7218.png) | 93.0024 | 82.3561 |
| 7219 | [image](seed_panel_native_qwen_7219.png) | [image](seed_panel_tecm_v3_7219.png) | [image](seed_panel_scheduler_closed_7219.png) | 94.3210 | 84.1535 |

## Interpretation

- Mean RGB-MAD improvement on downstream-seen prompts: `0.0000`.
- Mean RGB-MAD improvement on the downstream-held-out prompt: `2.1404`.
- Route/action/register improvements establish that the compiler is moving the right executable boundary only when the rendered image also improves.
- A seen-prompt repair is a capacity result. The held-out arm is the generalization check; neither is a universal equivalence certificate.

## Claim boundary

All four eval prompts (fox, blue_fox, cat, corgi) are held out from both carrier warm-start and downstream closure fitting; closure trains only on the train-panel prompts. Held-out recovery here is a prompt-disjoint generalization trend, not a cross-family equivalence certificate.
