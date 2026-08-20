# Held-out Saturn function-recovery matrix

This is the held-out native FLUX.2/Klein run for seed `7218` and the prompt
`a photorealistic blue fox sitting in fresh snow at dawn, soft blue light`.
The denoiser is the real frozen FLUX.2 model. Smol and Mamba are conditioner
arms; the experiment does not train or replace the denoiser.

## Execution contract

- mrun job: `job-36639a716923`
- device: CUDA on `beast`
- one outer mrun submission and one model load
- 12 Saturn checkpoints: three families × four denoising cuts
- 80 intervention branches plus 12 exact no-op suffix replays
- 92 local evaluations total
- peak VRAM: 8,266.8 MB
- peak process RSS: 22,990.2 MB
- all checkpoint replays matched the corresponding full run at zero RGB MAD

## Baseline

The foreign-to-native image distances were:

| family | RGB MAD to native Qwen |
|---|---:|
| Smol | 82.3186 |
| Mamba | 83.1801 |

The native Qwen baseline is the semantic reference. The foreign baselines are
valid renderer outputs but do not match the Qwen image.

## Complete-return interventions

At the late step (`step 3`), replacing the complete return of any of the four
typed boundaries (`joint.2`, `joint.3`, `joint.4`, or `single.0`) with the
same-step native Qwen return produced the same downstream image within this
run. The image distance became:

| foreign family | foreign baseline | Qwen-donor image | improvement | fraction rescued |
|---|---:|---:|---:|---:|
| Smol | 82.3186 | 23.4780 | 58.8406 | 71.5% |
| Mamba | 83.1801 | 23.9645 | 59.2156 | 71.2% |

The effect was time-dependent: at step 2 the Qwen-donor distances were 38.16
(Smol) and 35.38 (Mamba), while step 0 remained much farther away at 53.44
and 45.33. The late typed state therefore carries a stronger recoverable
semantic contrast than the early state in this four-step schedule.

Nulling the complete late return was strongly causal as well: the RGB MAD from
the foreign baseline was 46.18 for Smol and 69.00 for Mamba at `joint.4`, and
the scheduler register changed. This is necessity evidence for the boundary,
not proof that the boundary alone is a source-level function.

## Interpretation

The identical late donor images across the four whole-return sites are a
useful carrier-equivalence observation. It says that, under this checkpoint
and suffix, several typed boundaries expose interchangeable native semantic
state to the downstream program. It does **not** mean their internal
operations are identical or that any one physical address is the origin of
meaning.

The report contains 16 dynamic function candidates (four boundaries × four
steps), repeated Frame/Act-style typed signatures, and 28 repeated traced
internal operation paths for each family. The conservative label is therefore
`candidate_semantic_function`, not recovered source code.

## Artifact

- [machine-readable report](function-recovery-heldout-report.json)
- [run receipt](function-recovery-heldout-receipt.json)
- [native Qwen baseline](heldout-native-qwen.png)
- [Smol baseline](heldout-smol.png)
- [late Smol joint.4 Qwen donor](heldout-smol-qwen-donor.png)
