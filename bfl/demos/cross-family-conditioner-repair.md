---
title: "Cross-Family Conditioner Substitution and Scheduler-Closed Repair in FLUX.2"
type: experiment-report
status: partial-learned-repair-with-heldout-boundary
rank_in_bfl_survey: 5
model: "FLUX.2 Klein 4B"
tags: [bfl, flux, conditioner, cross-family, adapter, scheduler-closure, semantic-translation]
---

# Cross-Family Conditioner Substitution and Scheduler-Closed Repair in FLUX.2

> [!summary]
> A frozen FLUX.2 Klein 4B image suffix accepts conditioning from a foreign language model after an explicit adapter maps the foreign sequence into the native `[512, 7680]` contract. Supplying the complete native conditioning tensor restores the native image exactly, proving that the suffix is healthy and the interchange problem is upstream. A learned 14.97M-parameter adapter reaches high tensor cosine but only partial semantic image fidelity. A larger 21.07M-parameter time-expanded mapper trained through the real denoiser, scheduler, and VAE strongly improves seen prompts; the fully held-out corgi prompt improves only modestly. A separate held-out intervention shows that complete late native-state replacement rescues 71.5% of the foreign-to-native image distance for SmolLM2 and 71.2% for Mamba. The result establishes ABI compatibility and partial repair, not universal semantic interchange.

## Research question

Can the language-conditioning component of a FLUX.2 image generator be replaced by a different language model while keeping the image denoiser, scheduler, latent process, and VAE frozen?

This is an interface-versus-semantics experiment. It separates four questions that are often
collapsed into one scalar:

1. Can a foreign sequence be shaped to the native tensor contract?
2. Does the unchanged image suffix accept a complete native conditioning tensor supplied to the
   foreign branch?
3. Does a learned adapter preserve semantic directions, not only tensor geometry?
4. Can training through the actual image consumer repair the semantic loss, including on prompts
   withheld from fitting?

## Interface contract

The native branch is:

```text
prompt → native language conditioner → C_native ∈ R^(512×7680)
        → frozen FLUX.2 transformer → scheduler → VAE → RGB image
```

The foreign branch replaces only the conditioner:

```text
prompt → SmolLM2-1.7B or Mamba-1.4B → S ∈ R^(512×2048)
        → learned adapter Aφ(S) = C_foreign ∈ R^(512×7680)
        → same frozen transformer → same scheduler → same VAE → RGB image
```

The target sequence length is 512 and the target width is 7,680. The denoiser is never trained or replaced. All image comparisons use the same seed, resolution, step count, and native downstream components.

## Three experimental layers

### Layer 1: Mechanical closure

The strongest mechanical control writes the complete native conditioner into the foreign branch,
then runs the unchanged suffix. It restores the native image exactly. This localizes the failure:
the denoiser, scheduler, VAE, latent initialization, and decoder path can consume the native
carrier; the foreign branch fails because its learned conditioning is not in the native semantic
coordinate system.

Compact carrier masks are weaker controls. A selected-site mask reaches approximately 0.935
similarity, while top-token and top-channel masks reach approximately 0.094 and −0.050 on the
same diagnostic. The useful semantic payload is distributed across the sequence and channels,
not stored in one obvious lexical slot.

### Layer 2: Learned carrier adapter

The first learned adapter has 14,966,272 parameters and is trained for 700 steps with masked token MSE plus a masked cosine term. It maps the foreign `[512, 2048]` sequence to the native `[512,7680]` sequence. On a same-prompt held-out parity panel, the corrected Smol adapter reaches:

- mean RGB cosine 0.8258;
- mean RGB absolute difference 83.32;
- train token cosine about 0.872;
- corrected red-versus-blue image MAD 11.423, versus 70.954 for native conditioning on the same
  diagnostic.

This is the central “clean but wrong” result. High carrier cosine is not semantic equivalence. A
foreign tensor can look geometrically aligned while driving different denoiser actions and images.

### Layer 3: Time-expanded consumer-closed repair

The time-expanded conditioner mapper (TECM) is trained against the actual downstream computation, not only the static carrier. The reported v4 contract uses:

| Property | Value |
|---|---:|
| Mapper parameters | 21,074,176 |
| Carrier warm-start steps | 900 |
| Scheduler-closure steps | 120 |
| Frozen image suffix | transformer, scheduler, VAE |
| Native duplicate control | exact |
| Real scheduler parity | max absolute error 0 |

The objective combines native-carrier residual error, minimal-pair direction alignment, per-token
scale, residual cosine, denoiser action, and scheduler continuation. Rendered arms all resume the same cut-0 state and use exact scalar suffixes.

## Scheduler-closed results

The latest four-prompt rendered panel compares the pre-closure TECM v3 with scheduler-closed TECM v4. RGB-MAD is lower when the repaired image is closer to the native-Qwen reference.

| Prompt   | Split               | Pre-closure MAD | Closed MAD | Improvement |
| -------- | ------------------- | --------------: | ---------: | ----------: |
| Blue fox | downstream seen     |         64.2505 |    29.5398 |     34.7108 |
| Cat      | downstream seen     |         74.4253 |    37.6073 |     36.8180 |
| Fox      | downstream seen     |         70.4207 |    40.9002 |     29.5205 |
| Corgi    | downstream held out |         96.2340 |    87.6347 |      8.5993 |

Mean improvement is 33.6831 RGB-MAD points on downstream-seen prompts and 8.5993 points on the held-out corgi prompt. The held-out result moves the output toward a dog category but does not reliably recover the corgi, astronaut, or space-scene composition. It is therefore evidence of partial transfer, not prompt-disjoint semantic equivalence.

![Native blue-fox reference](../artifacts/cross-family-conditioner-repair/native-blue-fox.png)

![Pre-repair blue-fox output](../artifacts/cross-family-conditioner-repair/pre-repair-blue-fox.png)

![Scheduler-closed blue-fox output](../artifacts/cross-family-conditioner-repair/repaired-blue-fox.png)

![Native held-out corgi reference](../artifacts/cross-family-conditioner-repair/native-corgi-heldout.png)

![Pre-repair held-out corgi output](../artifacts/cross-family-conditioner-repair/pre-repair-corgi-heldout.png)

![Scheduler-closed held-out corgi output](../artifacts/cross-family-conditioner-repair/repaired-corgi-heldout.png)

## Held-out function-recovery matrix

The learned adapter has a second failure mode: it may carry a useful payload but address the
recipient's semantic route incorrectly. A separate held-out panel diagnoses this by replacing the
complete typed return at one boundary with the native-Qwen return at the same denoising step.

The panel uses a blue-fox prompt at seed 7218, four typed boundaries (`joint.2`, `joint.3`,
`joint.4`, `single.0`), four denoising cuts, and two foreign families. It contains 12 checkpoint
captures, 80 intervention branches, 12 exact no-op suffix replays, and 92 local evaluations.
Every checkpoint replay matches its full native run at zero RGB MAD.

Foreign-to-native baseline distances are:

| Foreign family | Baseline RGB-MAD to native Qwen |
|---|---:|
| SmolLM2-1.7B | 82.3186 |
| Mamba-1.4B | 83.1801 |

Replacing the complete late return at any of the four tested boundaries produces:

| Foreign family | Qwen-donor RGB-MAD | Distance rescued |
|---|---:|---:|
| SmolLM2-1.7B | 23.4780 | 71.5% |
| Mamba-1.4B | 23.9645 | 71.2% |

Nulling the same late return is strongly causal: RGB-MAD changes by 46.18 for Smol and 69.00 for Mamba at the `joint.4` boundary, while the scheduler return register also changes. The late native state is therefore a high-value recoverable carrier in this held-out cell. However, a complete native return is an oracle payload intervention; it does not show that the learned adapter can select or construct that payload without native assistance.

## Interpretation

The experiment separates the cross-family problem into a useful decomposition:

```text
interface shape → payload geometry → semantic route address → denoiser action
                → scheduler continuation → final RGB consumer
```

The interface shape is solved for the tested families. Complete native payloads are consumed
correctly. The learned adapter reaches high static carrier cosine but loses semantic directions.
Training through the real consumer improves seen prompts and exposes a held-out boundary, while oracle late-state replacement shows that much of the foreign-to-native gap is recoverable if the right recipient state is supplied.

The main bottleneck is therefore not only tensor transport. It is recipient-local semantic address
translation: finding the state, route, dose, and temporal location that the frozen suffix knows how
to consume.

## Working inference and claim boundary

**Observation:** the same frozen FLUX.2 image suffix accepts native and foreign conditioner paths;
complete native carrier donation restores the native image exactly.

**Trend:** a learned foreign-to-native adapter can be geometrically aligned and still semantically
wrong; consumer-closed training improves seen prompts but only modestly improves a fully held-out prompt.

**Convergent trend:** native late-state replacement rescues 71.5% and 71.2% of foreign-to-native
image distance for two foreign families in a held-out cell, with exact replay and causal nulls.

**Terminal status:** partial learned repair and bounded function-recovery evidence. Universal
prompt-disjoint conditioner interchange, donor-free semantic address translation, and native
equivalence are not established.

## Local proof bundle

The complete compact evidence is in [the local artifact bundle](../artifacts/cross-family-conditioner-repair/):

- [native conditioner receipt](../artifacts/cross-family-conditioner-repair/native-conditioner-receipt.json)
- [corrected Smol receipt](../artifacts/cross-family-conditioner-repair/smol-conditioner-receipt.json)
- [scheduler-closed v4 report](../artifacts/cross-family-conditioner-repair/tecm-v4-report.json)
- [held-out function-recovery report](../artifacts/cross-family-conditioner-repair/function-recovery-heldout-report.json)
- [held-out analysis](../artifacts/cross-family-conditioner-repair/function-recovery-heldout-analysis.md)
- [receipt verifier](../artifacts/cross-family-conditioner-repair/verify.py)

Run `python ../artifacts/cross-family-conditioner-repair/verify.py` from this directory to check the adapter contract, exact scheduler controls, mapper size, and held-out evaluation counts.
