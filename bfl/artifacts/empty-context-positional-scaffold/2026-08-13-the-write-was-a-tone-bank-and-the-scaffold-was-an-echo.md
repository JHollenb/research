---
title: "The Write Was a Tone Bank and the Scaffold Was an Echo"
subtitle: "Three panels in one evening: the KV divergence has structure but not saturation (tail-local above a kernel-regime boundary, bounded propagation); the pad scaffold is consumed at denoise step 0 and turns out to be a semantic echo, not inert substrate; and the KV write itself is a low-rank positional tone bank whose phase carries the token address — values are magnitude-at-an-address, keys need the position clock."
date: 2026-08-13
type: blog
status: measured-research-report
claim_status: measured-with-preregistered-gates
subtype: context-register-program-measurements
author: claude
tags:
  - blog
  - saturn
  - context
  - kv-cache
  - spf
  - phase-address
  - flux2
  - conditioning
related:
  - "[[./2026-08-13-the-empty-context-was-holding-the-picture-up|The Empty Context Was Holding the Picture Up]]"
  - "[[./2026-08-13-the-rewind-left-the-tokens-in-the-cache|The Rewind Left the Tokens in the Cache]]"
  - "[[./2026-07-23-context-is-a-runtime-choice|Context Is a Runtime Choice]]"
source_docs:
  - ../../saturn/results/context-divergence-structure/job-b278a46637b2/report.json
  - ../../saturn/results/context-pad-windows/job-eb85a55a5aa5/report.json
  - ../../saturn/results/context-write-spectra/job-6eba52af38ab/report.json
  - ../../saturn/configs/context-divergence-structure.json
  - ../../saturn/configs/context-pad-windows.json
  - ../../saturn/configs/context-write-spectra.json
  - ../../saturn/results/context-external-cache/findings.md
---

# The Write Was a Tone Bank and the Scaffold Was an Echo

> [!summary] The result in one sentence
> The recompute-vs-cache divergence is **not** fullness-saturation — above a kernel-regime boundary at ~512 tokens it is confined *exactly* to the recomputed tail (early positions bit-equal at every N ≥ 2048) with bounded, non-compounding propagation (one token flip in 896 continuation tokens); the diffusion pad scaffold is **consumed at denoise step 0** and is a *semantic echo* (empty-prompt pads substitute nearly free, an unrelated prompt's pads do more damage than zeroing, and the occupancy effect survives a matched-position control); and the KV write itself is a **low-rank positional tone bank** (Fourier concentration ~50× its Gaussian null) whose **phase carries the token address** (within-token coherence 0.51–0.54 vs 0.30 matched nulls) — a magnitude-at-token-address re-representation works partially for values (agreement 0.375, 2.2× better than a shuffled-address null) and fails for keys, which entangle the address with the position clock.

> [!warning] Evidence boundary
> AR panels: qwen2.5-0.5b and qwen3-0.6b, bf16/sdpa on one RTX 4080, deterministic natural-sentence corpus; qwen3 ladders capped (4096 divergence, 2048 spectra) by a scheduler-clamped VRAM ceiling — amendments recorded pre-evidence. Pad panel: FLUX.2 Klein 4B, 256×256, 4 steps, two prompt rungs, two seeds; zeroing corrupts rather than removes rows (maskless attention). Phase-address and codebook results are one corpus, one context length (2,048), greedy readout. The "RoPE signature" reading of the key tone bank is a working inference, not established.

Follow-up to the same-day external-cache and empty-context posts, driven by three user
directions: characterize the 2nd/3rd-order effects of relocating the cache (the
saturation hypothesis), dig into *how* the pad substrate is molded, and ask what the
KV write *is* — spectrally, and as a data structure.

## Panel 1 — the divergence has structure, but it is not saturation (E-X2)

Setup: the same N tokens computed two ways — one-shot prefill vs prefill(N−64) + 64
forced decode steps — with a bitwise determinism control (same prefill twice) at every
cell. `saturn/results/context-divergence-structure/job-b278a46637b2/`.

- **Determinism control passed at every (model, length)** — two identical prefills are
  bit-equal, so the divergence is the execution split, not run variance. (This is the
  control whose absence the adversarial review flagged in the first cache panel.)
- **At N ≥ 2048 the divergence is confined exactly to the recomputed tail**: 16/16 top
  divergent positions in the 64-token tail, and the first 512 positions differ by
  exactly `0.000` — at N = 2048, 4096, 8192, and 32768, both models. The
  fullness-saturation prediction (early positions contaminated as the window fills) is
  **refuted** in this regime.
- **A regime boundary exists at N = 512**: there the *entire* cache diverges (100% of
  positions, position 0 included, top positions scattered mid-sequence) — an
  execution-regime change between 448- and 512-token prefills, not gradual saturation.
- **Propagation is bounded, not compounding**: 128-token greedy continuations agree
  100% in six of seven cells; logits drift stays flat (first quarter ≈ last quarter,
  ~0.2–0.6). The one behavioral event: qwen3@512 flipped one token at step 11 (drift
  spike 14.5, then decay). Divergence magnitudes are quantization-scale, not
  noise-scale (qwen3 max-abs 11.2), and correlate only weakly with key norms
  (Spearman −0.23…0.10) — the massive-activation proxy found no sink structure.

Practical read for a relocated cache: above the small-N regime boundary, recomputed
context differs from cached context only in the recomputed span, and the difference
does not snowball. The danger zone is small contexts near kernel-regime boundaries,
and near-tie tokens are always the fuse.

## Panel 2 — the scaffold is consumed at step 0, and it is an echo (E-A2)

Setup: per-step pad-row ablation windows via chained `advance_checkpoint` segments
(the no-op chain gates **exact at 0.0** against plain resume — the instrument is
clean), per-step packed-return-register readout, plus the three controls the
adversarial review demanded. `saturn/results/context-pad-windows/job-eb85a55a5aa5/`.

RGB MAD vs baseline, short rung (18/512 active), seeds 4242/7217:

| window (zero pads) | step 0 | step 1 | step 2 | step 3 | steps 0–1 | steps 2–3 | all |
|---|---|---|---|---|---|---|---|
| seed 4242 | **31.8** | 13.3 | 10.7 | 7.8 | 41.0 | 14.6 | 41.9 |
| seed 7217 | **47.2** | 11.2 | 11.2 | 8.3 | 52.4 | 14.5 | 53.2 |

- **Step 0 carries ~80–89% of the full-trajectory damage**; single-step damage falls
  monotonically with step; steps 2–3 add almost nothing once 0–1 are hit. The register
  curves show the mechanism: the step-0 displacement **compounds through the
  trajectory** (0.03 → 0.69 by step 3) even when every later step sees clean pads.
  This is prefix inertia as mechanism — the image really is set super early, in the
  *denoise* trajectory, and the scaffold is a step-0 ingredient.
- **The molding is semantic.** Pads from an *empty* prompt substitute nearly free
  (12.5–20.2 MAD) — most of the scaffold function needs no prompt at all. But pads
  from an *unrelated* prompt do **more damage than zeroing** (68.6/76.5 vs 41.9/53.2)
  — pad rows carry a diffuse echo of their prompt that injects competing content when
  it conflicts. "Generic scaffold" was half right: the pads are a neutral substrate
  *plus* a semantic echo, and the earlier minimal-edit donor masked the echo because
  its echo nearly matched.
- **The occupancy effect survives the matched-position control**: zeroing the *same*
  307 rows (positions 205–511) costs 42.7/55.5 at 18-token occupancy but only
  16.4/22.1 at 205-token occupancy — same rows, same positions, **2.6× less damage**
  with more real context. The review's row-count confound is answered: the reliance
  shift is real.

## Panel 3 — what the write is (E-X3)

Setup: per-layer K/V position-by-channel matrices from a 2,048-token natural-text
prefill; spectral statistics with matched nulls; channel-paired phasor phases (the
route-op convention — the rFFT-over-features mag/phase split is a documented
rank-capped confound and was not used); and a behavioral codebook test with an
exact-tensor identity gate (passed: agreement 1.0, drift 0.0).
`saturn/results/context-write-spectra/job-6eba52af38ab/`.

- **The key stream is a tone bank.** Fourier concentration along the position axis:
  0.385 (qwen2.5) / 0.260 (qwen3) vs **0.007** for the same-shape Gaussian null — a
  ~50× lift — on a scaffold with stable-rank ~2% of null. The cache's keys are a
  periodic positional carrier (working inference: RoPE's rotation written into
  storage) over a very low-rank structure. The write is not noise-like; it has an
  algorithmic shape.
- **The recompute delta, by contrast, is spectrally white** (0.124 vs nulls
  0.129/0.122) but direction-concentrated (stable-rank well below null) — the
  divergence is rounding noise confined to a few directions, not a signal.
- **Phase carries the token address.** Within-token-id phase coherence 0.51/0.54 vs
  0.303 for *both* the shuffled-id and size-matched-random nulls, across every layer.
  Same token → same phase pattern. The SPF program's phase=address hypothesis holds in
  real Qwen KV caches, measured against its own null conventions.
- **Magnitude-at-a-token-address: values yes (partially), keys no.** Rebuilding the
  cache as `magnitude[position] × direction[token_id]`:
  - Values: continuation agreement 0.375 (qwen2.5) with first divergence at step 24;
    the true codebook reconstructs **2.2× better** than a shuffled-address null (0.42
    vs 0.95 relative error) — the token-identity addressing is real structure.
  - Keys: agreement 0.0, instant divergence — keys entangle the token address with
    the position clock, so a position-blind address destroys them. Coherent with
    Panel A: the tone bank *is* the position clock.
  - The refined data structure this points to: **K ≈ direction[token] rotated by a
    separable position-phase clock; V ≈ magnitude at a token address** — precisely
    the separable-phase-clock shape from the spectral-tokenizer lineage. That
    factorization is the next panel, not this one.

> [!note] On "our spectral tokenizer"
> The workspace holds four spectral-token lineages (sin-token-encoding's sinusoidal
> token IDs, SpectralMapper's learned amplitude/phase bands, the embedding rFFT split
> with its documented rank confound, and the token phase-clock store). This panel
> transfers the concepts common to all — phase as address, magnitude as content,
> separable clocks — and its results land on the same side as the measured SPF claims
> (cl-0292: magnitude strip nearly free for addressing). Which lineage "the spectral
> tokenizer" names is worth one clarifying sentence from the author.

## What this does not establish

- The RoPE reading of the tone bank (no direct comparison against a RoPE-free control
  or per-frequency match to the rotary schedule).
- Any cross-corpus or cross-length generality for the phase-address coherence numbers.
- That a position-aware K factorization works — proposed, not run.
- Why the N=512 regime boundary sits where it sits (kernel dispatch internals,
  worker-attested territory).
- Pad-echo semantics beyond one unrelated prompt; per-block reads of the echo.

## Reproducibility and data

- E-X2: `saturn/results/context-divergence-structure/job-b278a46637b2/` (+ killed
  calibration job-3c248864b6d6 with 6/7 replicating cells), config
  `saturn/configs/context-divergence-structure.json`, code
  `saturn/src/saturn/context_divergence.py` + CPU tests.
- E-A2: `saturn/results/context-pad-windows/job-eb85a55a5aa5/`, config
  `saturn/configs/context-pad-windows.json`, worker
  `saturn/workers/run_saturn_context_pad_windows.py`.
- E-X3: `saturn/results/context-write-spectra/job-6eba52af38ab/`, config
  `saturn/configs/context-write-spectra.json`, code
  `saturn/src/saturn/context_write_spectra.py` + CPU tests.
- Same-day corrections to the earlier cache/pad posts (16 confirmed review findings):
  correction block in `2026-08-13-the-empty-context-was-holding-the-picture-up.md` and
  `saturn/results/context-external-cache/findings.md`.
