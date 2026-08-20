---
title: "The Conditioners Were Stock Checkpoints"
subtitle: "Everything we currently know about the Black Forest Labs models we hold, how each fact was derived, and the first weight-level provenance result in the image atlas"
author: strider
type: blog
date: 2026-07-31
created: 2026-07-31T14:51:30-07:00
status: measured-with-explicit-boundaries
claim_status: conditioner-provenance-measured-denoiser-provenance-out-of-scope-causal-circuit-cell-local-replication-queued
tags: [blog, gen-models, flux, flux2, black-forest-labs, provenance, fingerprints, eigenbasis, lineage, anatomy, physiology, behavior, causal-circuits, mrun, manalysis]
source_docs:
  - ../../experiments/2026-07-24-generative-image-model-atlas/BFL_FLUX2_REPORT.md
  - ../../experiments/2026-07-24-generative-image-model-atlas/outputs/fetched-bfl-flux2-lineage/comparison/activation-alignment.json
  - ../../experiments/2026-07-24-generative-image-model-atlas/outputs/conditioner-provenance-20260731/
  - ../../experiments/2026-07-29-202802-flux2-fp32-control-feasibility/status.md
  - ../../experiments/2026-07-26-distillation-fingerprints/RESULTS.md
related:
  - "[[2026-07-28-143331-inside-the-black-forest-flux-models|Inside the Black Forest]]"
  - "[[2026-07-28-123731-what-generative-image-models-know-and-where-they-fail|What Generative Image Models Know]]"
  - "[[2026-07-28-173304-four-doors-beyond-the-image-model-atlas|Four Doors Beyond the Image Model Atlas]]"
  - "[[2026-07-30-115051-flux-ownership-localized-to-the-joint-merged-transition|FLUX Ownership Localized to the Joint–Merged Transition]]"
  - "[[../experiments/bfl-flux2-lineage-sweep|BFL FLUX.2 Lineage Sweep]]"
---

# The Conditioners Were Stock Checkpoints

## The result at a glance

Black Forest Labs ships its FLUX.2 text encoders verbatim. As of today we can name the exact
public parent checkpoint of every conditioner in our pinned cohort, at the weight-byte level:

| FLUX component | Parent checkpoint (measured today) | Evidence class |
|---|---|---|
| FLUX.2 Dev `text_encoder` | `mistralai/Mistral-Small-3.2-24B-Instruct-2506` | embedding byte-identity (sampled) + eigenbasis ≈ 1.0 |
| FLUX.2 Klein 9B `text_encoder` | `Qwen/Qwen3-8B` | embedding byte-identity (sampled) + eigenbasis 0.9999992 |
| FLUX.2 Klein 4B `text_encoder` | `Qwen/Qwen3-4B` | embedding byte-identity (sampled) + eigenbasis 0.9999999 |

Three days ago, [[2026-07-28-143331-inside-the-black-forest-flux-models|Inside the Black
Forest]] could say only what the configs declare: "a Qwen3 conditioner", "a Mistral3-derived
conditioner". That was asserted anatomy read off `config.json`. Today's result is measured
provenance: the embedding weight bytes of each BFL conditioner match one specific public
checkpoint and mismatch its siblings.

The denoisers are the opposite story, and the boundary is structural: they have no vocabulary
embedding and no public parent, so the provenance instrument cannot reach them — not "we have
not tried yet" but out of scope by construction. The conditioners were stock; the denoisers are
the black forest.

This post consolidates everything we currently know about the six BFL subjects, with the
derivation and the instrument behind every class of fact.

## 1. Who "the models" are, and the custody they sit on

Everything below concerns the six pinned local subjects — FLUX.1 Schnell, FLUX.2 Klein 4B,
Klein 9B, Klein 9B-KV, FLUX.2 Dev, and the FLUX.2 Small Decoder — at these exact revisions
(measured from the registry readback of 2026-07-29; artifact identities in
`BFL_FLUX2_REPORT.md`):

| Subject | HF revision | Registry name |
|---|---|---|
| FLUX.1 Schnell | `741f7c3c…` | `base-flux1-schnell/v2` |
| Klein 4B | `e7b7dc27…` | `base-flux2-klein-4b/v1` |
| Klein 9B | `92196c8e…` | `base-flux2-klein-9b/v1` |
| Klein 9B-KV | `a6dfb36e…` | `base-flux2-klein-9b-kv/v1` |
| Dev | `26afe3a7…` | `base-flux2-dev/v1` |
| Small Decoder | `a3efc24f…` | `base-flux2-small-decoder/v1` |

This is not a claim about every BFL release: Kontext, Krea, Pro, and the FLUX.1 dev/fill/canny
family are not in the cohort. Model bytes live on Beast under `/mnt/big/llm-models`; the sweep
mirror is `s3://experiments/model-analysis/bfl-flux2-lineage-v1/results/` (2,883 objects,
17.442 GB, zero missing on full listing).

## 2. Anatomy — measured from safetensors headers and configs

Derived by the static tier of `image_atlas` (safetensors-header accounting plus config
inventories; no forward pass required):

| Subject | Packaged params | Denoiser | Conditioner | VAE | Block program (joint+merged @ width) |
|---|---:|---:|---:|---:|---|
| Schnell | 16.860B | 11.891B | CLIP 0.123B + T5 4.762B | 0.084B (16-ch) | 19+38 @ 3072, iface 4096 |
| Klein 4B | 7.982B | 3.876B | Qwen3 4.022B | 0.084B (32-ch) | 5+20 @ 3072, iface 7680 |
| Klein 9B | 17.353B | 9.079B | Qwen3 8.191B | 0.084B (32-ch) | 8+24 @ 4096, iface 12288 |
| Klein 9B-KV | 17.353B | same shapes | same | same | identical inventory to 9B |
| Dev | 56.319B | 32.223B | Mistral3 24.011B | 0.084B (32-ch) | 8+48 @ 6144, iface 15360 |
| Small Decoder | 0.062B | — | — | decoder-narrowed VAE | enc 128/256/512/512, dec 96/192/384/384 |

Facts that matter downstream:

- Component sums reconcile exactly to packaged totals for every generator. Dev's byte/param
  ratio is 2.00298 (implies a small non-BF16 remainder; unremarked in the original report).
- Klein 9B and 9B-KV share a complete tensor-metadata inventory SHA-256 (`bf581e02…`): 883
  tensors, identical shapes — but their denoiser weight shards differ and none of 28 matched
  outputs is pixel-identical (mean pair MAE 25.60). Same skeleton, different anatomy.
- A `guidance` conditioning role exists in Dev's config and is absent in Schnell and Klein 4B.
  The statement "Dev is guidance-distilled" remains **asserted** (read off the local
  architecture card); the config role presence/absence is the only measured proxy.
- No Mamba, state-space, scene-register, or sparse-MoE substrate exists in any held checkpoint
  — the hypothesis of "The Model After FLUX" is refuted for this cohort (measured against all
  configs and weights).

## 3. Conditioner provenance — the new result, and exactly how it was derived

### Instrument

The embedding-provenance fingerprint (`mrun fingerprint`, branch
`feat/embed-provenance-fingerprint` in `~/domains/mrun-fp`; measured validation in
`experiments/2026-07-26-distillation-fingerprints/RESULTS.md`) reads **one tensor per model**
— the input token embedding — by HTTP range-read, centers it, and caches the top-k eigenbasis
of its Gram. Lineage between two models is the mean cos² of the principal angles between their
top-k eigenbases. Three design rules, all learned the hard way on the LLM side:

1. **Lineup, never threshold.** Alignment numbers are not comparable across lineups (an
   unrelated pair has measured 0.64; a parent and its own heavily-tuned descendant 0.19). The
   API refuses single-candidate calls.
2. **Substrate, never teacher.** The instrument names the checkpoint a model was *initialized
   from*, and is blind to distillation teachers by construction.
3. **Subspace, not spectrum.** Scalar spectral summaries (n50/n90, stable rank) are weak,
   scale-dependent provenance evidence; only the eigenbasis lineup carried its ground-truth
   validation (4/5 R1-Distill cases: true base 0.96–0.9998 vs wrong siblings 0.19–0.67; known
   limit: base-vs-instruct ties).

Today's run added a cheaper leg in front: a **byte screen** — SHA-256 over three sampled
256-row chunks of the embedding at spread offsets. If a candidate matches all three chunks and
the shape, the parent is identified at byte level and the eigenbasis becomes confirmation.

Artifacts for this run (script, log, per-model eigenbasis caches, alignment table):
`experiments/2026-07-24-generative-image-model-atlas/outputs/conditioner-provenance-20260731/`.
Two instrument adaptations were required and are recorded there: a subfolder-aware
`HubSource` (BFL ships conditioners as diffusers components under `text_encoder/`), and
`trim=False` panel-wide because BFL's `text_encoder/` folders carry no `tokenizer.json`
(both sides therefore compare all `V_cfg` rows — a recorded deviation from the tok-trim
discipline of the 07-26 panel).

### Data

FLUX.2 Dev text encoder (`Mistral3ForConditionalGeneration`, d=5120, V=131072) against four
same-shape Mistral candidates:

| Candidate | byte screen | eigenbasis k=64 | k=256 |
|---|---|---:|---:|
| Mistral-Small-3.2-24B-Instruct-2506 | **match (3/3 chunks)** | **0.9999997** | 0.9999996 |
| Mistral-Small-3.1-24B-Instruct-2503 | differ | 0.9999166 | 0.9998616 |
| Mistral-Small-3.1-24B-Base-2503 | differ | 0.9998745 | 0.9997634 |
| Mistral-Nemo-Base-2407 (control) | differ | 0.0125440 | 0.0502981 |

The random-subspace null at k=64/d=5120 is 0.0125. The Nemo control lands on the null to the
third decimal — the cleanest control separation this instrument has produced. Note what the
two evidence classes each do: the whole Mistral-Small-3.x family ties at ≥0.9998 (the formal
lineup verdict is AMBIGUOUS at margin 0.0001 — the documented base-vs-instruct limit), so the
**eigenbasis names the family and kills the control; only the bytes name the checkpoint.**

FLUX.2 Klein 9B text encoder (`Qwen3ForCausalLM`, d=4096, V=151936, untied):

| Candidate | byte screen | k=64 | k=256 |
|---|---|---:|---:|
| Qwen3-8B | **match (3/3 chunks)** | **0.9999992** | 0.9999998 |
| Qwen3-8B-Base | differ | 0.9991320 | 0.9974890 |
| DeepSeek-R1-0528-Qwen3-8B (distill control) | differ | 0.9987105 | 0.9934895 |

FLUX.2 Klein 4B text encoder (`Qwen3ForCausalLM`, d=2560, V=151936, tied):

| Candidate | byte screen | k=64 | k=256 |
|---|---|---:|---:|
| Qwen3-4B | **match (3/3 chunks)** | **0.9999999** | 0.9999999 |
| Qwen3-4B-Base | differ | 0.8924175 | 0.9444592 |
| Qwen3-4B-Instruct-2507 | differ | 0.8700694 | 0.9216855 |
| Qwen3-4B-Thinking-2507 | differ | 0.8548623 | 0.9085084 |

The 4B panel separates cleanly even in subspace (margin ≈ 0.11): the 2507 releases were heavy
continued-pretrain events that moved the embedding, exactly the regime the instrument was
built to detect. BFL picked the *original* Qwen3-4B hybrid release, not Base and not a 2507.

### Claim boundary

- "Byte-identical" means three sampled 256-row chunks per pair, not a full-tensor hash.
  Overwhelming for identification; not a formal bit-equality certificate.
- Only the input embedding was compared. The conditioner *body* almost certainly matches too,
  but that is currently inference, not measurement — the row-delta leg over full shards would
  close it if it ever matters.
- The Klein lineups required bypassing the instrument's matched-object guard, which refuses on
  *recorded* `len(tokenizer)` (BFL ships no tokenizer.json in the subfolder → subject records
  V_cfg; candidates record 151669) even though both sides computed over identical rows. The
  bypass recomputes principal angles directly from the cached eigenbases
  (`align_from_cache.py`); an upstream fix (compare effective rows when trim=cfg) is owed.
- **Teacher attribution stays out of scope.** Nothing here says what taught the denoisers.

## 4. Denoiser lineage — what we have instead, and why provenance stops here

The denoisers have no vocabulary embedding and no public parent checkpoint, so eigenbasis
provenance is structurally out of reach. Three weaker, non-equivalent evidence classes exist:

**Matched-stimulus activation geometry** (`manalysis.globality`, linear + RBF CKA with
row-shuffled nulls; 80 stimuli × 9 depth/time coordinates; Dev excluded as static-only):

| Pair | linear CKA | RBF CKA |
|---|---:|---:|
| Schnell ↔ Klein 4B | 0.502 | 0.553 |
| Schnell ↔ Klein 9B | 0.544 | 0.600 |
| Schnell ↔ Klein 9B-KV | 0.529 | 0.583 |
| Klein 4B ↔ Klein 9B | 0.879 | 0.901 |
| Klein 4B ↔ Klein 9B-KV | 0.842 | 0.862 |
| Klein 9B ↔ Klein 9B-KV | **0.939** | **0.945** |

Shuffled nulls sit near 0.03–0.09, so all of these are far above chance. The generational
break (FLUX.1 vs FLUX.2 ≈ 0.5; within-FLUX.2 ≈ 0.85–0.94) is real geometry — but CKA is
explicitly *not* neuron correspondence, algorithm identity, or lineage proof.

**Sampled weight spectra** (`image_atlas/tensors.py`: effective rank, stable rank, top-singular
energy over 32 sampled matrices per model). Most concentrated role everywhere: adaptive
modulation (stable rank ≈ 4.7). For the only same-shape denoiser pair, 9B vs 9B-KV, the
sampled median deltas are ~0 effective rank / −0.10 stable rank — shape-identical,
weight-different, cause unknown. The direct standard→KV weight-delta analysis remains the
oldest owed item on the lineage list.

**Delta accounting** across the family (block program, widths, latent channels, conditioner
swaps) — descriptive lineage evidence only. The Four Doors piece already stated the honest
version: comparing the published Klein artifacts is *"useful lineage evidence, not a
distillation experiment."* Nothing measured since changes that sentence.

One genuinely open instrument idea: Schnell and Klein 4B share denoiser width 3072, so a
weight-matrix principal-angle comparison is *possible* — but it would be a new, unvalidated
instrument. The LLM fingerprint earned its verdicts against known ground truth
(R1-Distill); no such ground-truth panel exists for DiT blocks, so any number it produced
today would be uninterpretable. That validation panel is the prerequisite, not the sweep.

## 5. Physiology — what runs, exactly, on our hardware

All measured under mrun guarded admission with trajectory certificates (the certificates prove
the instrumented pipeline reproduces the stock pipeline bit-for-bit before any claim opens):

- **Klein 9B-KV reference cache**: call 1 processes 2,048 reference+target tokens and extracts
  a 32-layer K/V cache (max observed 512 MiB); calls 2–4 process 1,024 target tokens against
  the cache. One matched probe: 1.073× wall-time vs standard. Zeroing the cached reference
  changes 785,642 output uint8 values (mean |Δ| 37.56) vs 455,010 (mean 1.14) for standard —
  a strong route to pixels, deliberately not read as "style lives in the cache".
- **Dev runs decoupled on a 66 GB host**: 112.8 GB of BF16 weights; conditioner (24.0B) and
  denoiser (32.2B) never co-resident; 75 persisted `[1,512,15360]` prompt embeddings; 12.7 GB
  swap at forward completion proves paging carried it. Full analysis job: 571 s, 17.4 GB peak
  RSS, 11.6 GB peak VRAM, 14/14 gates.
- **Small Decoder**: 43.678% fewer decoder-path parameters, 1.517× faster single-pair decode,
  cosine 0.999784 / PSNR 44.64 dB vs the full VAE — one latent, five serial decodes;
  explicitly not a distributional quality claim.

## 6. Behavior — narrow, matched, honest

Common panel (14 prompts × 2 seeds, 512 px, 4 steps; CLIP + objective component counts + TrOCR):

| Model | mean CLIP | count exact | OCR exact/char |
|---|---:|---:|---:|
| Schnell | 0.351 | 0.500 | 0 / 0.083 |
| Klein 4B | 0.351 | 0.833 | 0 / 0 |
| Klein 9B | 0.354 | 0.500 | 0.250 / 0.307 |
| Klein 9B-KV | 0.353 | 0.667 | 0 / 0.209 |
| Dev (diagnostic tier) | 0.360 | 0.833 | 0.250 / 0.472 |

The sharpest behavioral fact in the family is the Klein 4B counting cliff (matched 96-record
panel): count 2 → 1.000, 3 → 0.875, 4 → 0.875, 5 → 0.4375, 6 → 0.1875, 7 → 0.0625. Exact
counting collapses between five and seven objects. These are narrow diagnostics, not a
quality ranking.

## 7. From readable state to a causal circuit — where the last three days went

The 07-28 atlas ended at "readable everywhere, causal nowhere": corrected readouts localized
red/blue, typography, and style at `single.19.target_image` call 0 (max-T p = 0.0078) and
count information at `joint.4.target_image` calls 0–1, while every style intervention was
null. Since then, on FLUX.2 Klein 4B (all sealed reports in
`experiments/2026-07-29-202802-flux2-fp32-control-feasibility/results/`):

1. **Physical layer closed.** The 14-row FP32 "impossible panel" (controls unrealizable in
   BF16) passed on retry (`job-60235f8e9b63`) after an earlier attempt died on admission.
2. **Semantic-port ranking** (288 generations, max-T over 999 within-seed permutations): the
   top discovery coordinates are one contiguous seam — `joint.4 → single.0 → single.1`,
   target-image, owned cell, call 0, all p = 0.001
   ([[2026-07-30-115051-flux-ownership-localized-to-the-joint-merged-transition|writeup]]).
3. **Behavior substrate admitted**: the top-left exact-count transition passed 30/30 paired
   trials across discovery/confirmation/corner/replication; Wilson 95% lower bound 0.8865.
4. **First necessary-and-sufficient development cut**: the complete `joint.4` trajectory —
   text-only, image-only, and dual-stream addition AND deletion all 1.0, with a thresholded
   dose response (0 at ≤0.5 dose, 1.0 at 0.75).
5. **Replication PASS** (`job-b8b1853d86d6`): 4/4 pairs, 24/24 predeclared arms, mean and
   minimum normalized effect 1.0, one model load.
6. **Time/stream localization**: image route localizes to call 2 alone (necessary and
   sufficient on the development pair; wrong-time −0.15/0.50, equal-energy random 0.0); the
   text route is causal but *fails specificity* — a norm-matched random text edit also
   deletes the behavior.
7. **Strict canary PASS** (`job-91e0a99cca2d`): addition 4/4, deletion 3/4, dose monotone
   4/4, equal-energy/wrong-call/wrong-stream/wrong-sign all 0.0 — but wrong-cell 0.284 and
   wrong-site 0.377 are nonzero, and only the two top-left pairs pass every strict gate.

The correct current claim is therefore a **`joint.4:target_image:owned_cell:call_2` top-left
local circuit candidate** — not a location-invariant counting circuit. The 16-pair strict
replication (`job-f6ad5c934059`) and the alternate-lexicalization panel (`job-9a0b2352112f`)
are compiled, sealed, and queued; at the last live admission check (2026-07-31 ~14:25 PDT)
both are unschedulable behind three legitimate resident jobs on Beast (17.8 GB free vs a
24.2 GB honest ceiling). No reservation was understated to jump the queue.

## 8. What we still do not know

- **Denoiser provenance and training history.** No teacher, data mixture, curriculum, or
  optimizer fact is recoverable from the artifacts we hold. "Guidance-distilled" for Dev
  remains an assertion from its architecture card.
- **No location-invariant semantic circuit.** The admitted candidate is cell-local; strict
  replication has not run.
- **Dev contributes zero rows to activation geometry** (static-only tier), and its rich
  diagnostic suite (recorder, readouts, winder) still sits behind an unguarded ancestry.
- ~~The passing Dev diffusion-MRI card~~ — resolved 2026-07-31: the card (finalizer
  `job-5ade25b50ea9`, status observed-bounded, planned-closure gaps `{}`) verifies
  **byte-identical across three independent stores** — local
  `outputs/live-bfl-flux2/diffusion-mri/flux2-dev/card.json`, the MinIO mirror, and Beast
  disk — with all six fingerprint hashes matching the report and the finalizer job confirmed
  `succeeded` on the live scheduler. Only the stale `/tmp` snapshot says PASS:false; do not
  quote it. One residual: the MinIO-archived `BFL_FLUX2_REPORT.md` snapshot (2026-07-27)
  predates the current local report — the archive holds an older edition. And the match is
  card-content verification; the composite-fingerprint *derivation* was not re-derived.
- **Small Decoder distributional quality**, human-preference and safety panels: absent.

## 9. Instrument index — how each fact class was derived

| Fact class | Instrument | Where it lives / how it works |
|---|---|---|
| Anatomy (params, tensors, shapes) | safetensors-header + config readers | `image_atlas/{static_analysis,tensors}.py`; header accounting, no forward pass |
| Weight spectra (sampled) | matrix diagnostics | `image_atlas/tensors.py` — effective/stable rank, top-singular energy over 32 sampled matrices |
| **Conditioner provenance** | embedding-eigenbasis fingerprint + byte screen | `~/domains/mrun-fp` (`mrun fingerprint`); method + validation: `experiments/2026-07-26-distillation-fingerprints/RESULTS.md`; this run: `outputs/conditioner-provenance-20260731/` |
| Activation geometry | linear/RBF CKA + shuffled nulls | `manalysis/src/manalysis/globality.py` |
| Exact runtime custody | trajectory/adapter certification | `manalysis/src/manalysis/diffusion/{profiles,trajectory}.py` — fail-closed family adapters, pixel-parity gates |
| Interventions | scope-safe capture/ablate/patch | `manalysis/src/manalysis/diffusion/interventions.py` + FP32 precision islands |
| Causal plans | world-transition compiler | `manalysis` world-transition-compilation.v1 — enumerated licensed worlds, frozen subsets, Holm/max-T correction |
| Behavior | objective scorers | HSV component counting, CLIP, TrOCR; certificates with Wilson bounds |
| Orchestration/custody | mrun guarded admission | measured reservations, sealed payloads, SHA-bound resume; scheduler at zima:9025 |

The instrument stack is the actual story of the week: the same six checkpoints that produced
an observational atlas on Monday produced byte-level provenance and a replicated, controlled,
cell-local causal candidate by Thursday — because every new claim class arrived with its own
refusal conditions. The conditioners were stock checkpoints. The denoisers are still the black
forest, and the only honest way in remains the one the queue is currently holding: sixteen
sealed pairs, seven strict controls, and no shortcut past admission.
