---
title: "The Empty Context Was Holding the Picture Up"
subtitle: "Two context measurements in one afternoon: an external KV cache is bit-exact but wire-bound (recompute beats a 1GbE store everywhere, and recompute is never the same context), and Klein's 494 'empty' conditioner rows turn out to be load-bearing scaffolding whose removal breaks the image harder than swapping the whole prompt."
date: 2026-08-13
updated: 2026-08-13
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
  - external-memory
  - flux2
  - conditioning
  - token-economy
related:
  - "[[./2026-08-13-the-rewind-left-the-tokens-in-the-cache|The Rewind Left the Tokens in the Cache]]"
  - "[[./2026-08-09-saturn-token-economy-and-context|SATURN Token Economy and Context]]"
  - "[[./2026-07-23-context-is-a-runtime-choice|Context Is a Runtime Choice]]"
  - "[[./2026-07-29-002529-one-million-records-four-retrieved-slots|One Million Records, Four Retrieved Slots]]"
source_docs:
  - ../../saturn/results/context-external-cache/job-0d5ab5c3d094/report.json
  - ../../saturn/results/context-external-cache/findings.md
  - ../../saturn/results/context-pad-occupancy/job-79ff59eb54d2/report.json
  - ../../saturn/configs/context-external-cache.json
  - ../../saturn/configs/context-pad-occupancy.json
---

# The Empty Context Was Holding the Picture Up

> [!warning] Corrections (same-day adversarial review, 16 confirmed findings)
> A 20-agent adversarial review corrected this post: (1) **"the external cache is the
> only exact path" was an overclaim** — a reviewer-run control showed a *path-faithful*
> recompute (prefill + forced replay of the recorded decode tail) is bit-exact on the
> same host; the cache's exactness value is cross-host / when the construction history
> is unavailable. The "continuation logits differ at every cell" diagnostic was an
> instrument bug (steps fed different pending tokens) and is **retracted**. (2) The
> evidence run's **publish column measured the content-addressed dedup path** (GET +
> verify), not upload; true uploads (from the killed runs) were 1.45–1.8x slower.
> (3) "Wire-bound" should read **store-path-bound** (64–80 MB/s incl. two hash passes,
> deserialize, copies); the crossover span is **150–747 MB/s** by the no-fixed-cost
> formula, and real thresholds are higher. (4) Pad "deletion" is really **corruption**
> — zeroed rows keep attracting uniform attention; true removal was not run. (5) The
> destroy/substitute ratio is **2.5–3.6x**, not 3–6x. (6) The donor was a minimal-edit
> same-length prompt, so "ANY prompt's pads" is unsupported. (7) Per-row-normalized,
> the occupancy dose-response **flattens after the first rung** (0.085 → 0.052 → 0.053)
> — the raw decline partly reflects ablating fewer rows. (8) Two "killed calibration
> jobs" (job-8330ab85d93a, job-e8a8e1d57dae) actually failed on worker code bugs, not
> VRAM. Numbers below are original; read them through these corrections.

> [!summary] The result in one sentence
> Context can live outside the model in an external cache and come back **bit-exactly** (KV content and continuation logits, gated through 32k tokens) while recomputing the same tokens **never** reproduces the same context — but on a 1GbE store the fetch is wire-bound at ~78 MB/s and loses to recompute at every scale (crossover ≈ 0.2–0.7 GB/s store bandwidth); meanwhile, the never-run native ablation of Klein's conditioner shows the 494 tokenizer-inactive rows are **load-bearing scaffolding**: zeroing them at 3.5% occupancy breaks the image harder than swapping the entire prompt, yet another prompt's pads substitute almost perfectly, and the dependence falls monotonically as occupancy rises.

> [!warning] Evidence boundary
> External-cache economics: two small models (qwen2.5-0.5b, qwen3-0.6b), one store (MinIO over ~1GbE LAN), one host; qwen3's ladder capped at 8,192 by a scheduler-clamped VRAM ceiling (two amendments recorded pre-evidence, timings replicated across three runs). Pad ablation: FLUX.2 Klein 4B, 256×256, 4 steps, three prompt rungs (18/67/205 active of 512), two seeds, RGB-only readout at cut-step 0. Cross-model claims are inventory of prior controlled results, not new runs.

Second measurement arc of the context-register program, driven by one user question:
*can context move out of the model into an external cache, with an adapter so models
use it?*

## Part 1 — The external context cache (E-X)

The adapter already exists: a Saturn durable token cut **is** an external context
cache (`publish_token_cut` / `restore_token_cut` against MinIO). What was never
measured is what it costs, and whether the cheap alternative — just re-run the prompt —
is actually equivalent. Both questions now have numbers
(`saturn/results/context-external-cache/job-0d5ab5c3d094/`):

| model | tokens | on wire | publish | restore | re-prefill | restore÷re-prefill |
|---|---|---|---|---|---|---|
| qwen2.5-0.5b | 512 | 6 MB | 0.63 s | 0.10 s | 0.04 s | 0.42× |
| qwen2.5-0.5b | 2,048 | 24 MB | 0.37 s | 0.31 s | 0.10 s | 0.33× |
| qwen2.5-0.5b | 8,192 | 96 MB | 1.45 s | 1.22 s | 0.38 s | 0.31× |
| qwen2.5-0.5b | 32,768 | 384 MB | 5.73 s | 4.90 s | 1.88 s | 0.38× |
| qwen3-0.6b | 512 | 56 MB | 0.82 s | 0.73 s | 0.09 s | 0.12× |
| qwen3-0.6b | 2,048 | 224 MB | 3.30 s | 2.82 s | 0.30 s | 0.11× |
| qwen3-0.6b | 8,192 | 896 MB | 13.2 s | 11.2 s | 1.22 s | 0.11× |

**Measured, gated:** the restore is bit-exact at every cell — per-layer KV content
`torch.equal`, and the forced continuation step after restore produces sha-identical
logits. Moving context out and back loses nothing, up to 384 MB of state.

**Measured, everywhere:** re-prefilling the identical committed tokens is **not the
same context**. KV divergence 0.19–11.25 max-abs bf16 per cell, and the continuation
logits after re-prefill differed from the source at *every* length (at 136 tokens in
the rewind panel they had happened to match; from 512 up they never do). Recompute is a
semantic substitute, not an identity — the external cache is the only exact path.

**Measured, the economics:** restore runs at 77–80 MB/s at every cell — the wire, not
the GPU. On this LAN, recompute beats the cache 2.4–9× everywhere. The crossover is a
**bandwidth threshold, not a context-length threshold**: the cache wins when the store
delivers more than `kv_bytes / reprefill_time` ≈ 204 MB/s (qwen2.5@32k) to 734 MB/s
(qwen3@8k). An NVMe-local tier (~2 GB/s) flips every cell; 1GbE never does. And
KV-heavy models are hurt twice: qwen3 carries 9.3× the bytes per token for only ~3× the
prefill cost, so external caching gets *relatively worse* as KV-per-token grows.

**The "models use it" (plural) half, answered from the corpus rather than new GPU:**
five controlled prior results say cross-model KV/hidden-state transport does not
separate from its nulls (embedding bridge ceiling cos 0.52; role-exchange within noise
of shuffled donors; cross-family READ install with `valid == scrubbed == no_state`; the
scratchpad-READ mint that went 0.17 → 0.05; adapter carrier cos 0.995 with semantic
fidelity 0.69–0.78 against a 0.99 bar). Even the *same* model can't rebuild its own KV
from its own tokens, per this panel. What crosses models in this corpus is
**records/text plus a per-model reader** — and three independent experiments (tiered
memory recall@K 1.000 / reader 0.63; scratchpad PoC; the mock harness at 0.99 with a
perfect reader) agree the reader, not the store, is the bottleneck. Full inventory and
recommendation: `saturn/results/context-external-cache/findings.md`.

## Part 2 — The empty context (E-A)

Yesterday's scouting established that the Flux.2 Klein denoiser receives **no attention
mask** over the `[1, 512, 7680]` conditioner: all 512 rows are live keys at distinct
RoPE positions, and the ~494 "padding" rows are prompt-conditioned encoder states, not
zeros. A donation panel had shown pad rows transport semantics into foreign carriers;
the clean **native** ablation had never been run. It ran today
(`saturn/results/context-pad-occupancy/job-79ff59eb54d2/`), against a no-op override
gate that held exact at 0.0:

RGB mean-abs delta vs baseline (two seeds), donor_full = swapping the whole prompt:

| occupancy | zero pads | noise pads | pad_swap | active_swap | donor_full |
|---|---|---|---|---|---|
| 18/512 (3.5%) | 41.9 / 53.2 | 39.6 / 54.4 | 16.0 / 21.4 | 39.7 / 30.0 | 43.5 / 31.7 |
| 67/512 (13.1%) | 23.3 / 30.4 | 28.1 / 32.5 | 8.6 / 12.1 | 58.2 / 59.7 | 58.4 / 59.1 |
| 205/512 (40.0%) | 16.4 / 22.1 | 14.1 / 18.6 | 4.6 / 6.2 | 42.1 / 61.8 | 42.6 / 62.6 |

Three findings, consistent across both seeds:

1. **The empty context is load-bearing.** At 3.5% occupancy, zeroing the 494 inactive
   rows moves the image as much as or *more than* replacing the entire prompt
   (53.2 vs 31.7 on seed 7217). The denoiser leans on rows the token accounting calls
   empty.
2. **But it is scaffolding, not meaning.** Substituting another prompt's pad rows costs
   3–6× less than destroying them (pad_swap 4.6–21.4), while swapping only the active
   rows reproduces the full-prompt swap almost exactly (active_swap ≈ donor_full at
   every rung). The prompt's semantics live in the active rows; the pads supply generic
   contextualized structure any prompt's pads can supply.
3. **Occupancy buys independence from the scaffold.** Pad-destruction damage falls
   monotonically, 42–53 → 23–30 → 16–22, as active tokens grow 18 → 67 → 205. A model
   given more real context relies less on the empty kind.

For the context register this settles the denominator question with a twist:
"occupancy" (active/512) is the right *semantic* axis, but the compute axis is pinned
at 512 attended rows — and the inactive region cannot be treated as dead weight,
because deleting it is a larger intervention than replacing the prompt.

## What this does not establish

- Cache economics on other stores (NVMe, 10GbE) are extrapolated from the measured
  wire-bound bandwidth, not measured; publish includes serialization, restore includes
  device transfer — components not separated.
- No live paging tier was built or measured; only whole-prefix handoff.
- Pad findings are RGB-only, one pipeline, one resolution/step count, cut-step-0
  overrides; per-step and return-register readouts not captured.
- The reader-bottleneck conclusion for plural-model sharing is an inventory synthesis
  of prior experiments, not a new head-to-head.

## The next experiment

A disk-local statecut store (one store-backend change) to measure the NVMe point on
the crossover curve; pad-row ablation with return-register readout and per-step dosing
to locate *when* the scaffold is consumed; then the register build, whose contract
table now includes: exactness lives in the cache, not in recompute, and capacity
accounting must count all 512 rows while payload accounting counts the active ones.

## Reproducibility and data

- External cache: `saturn/results/context-external-cache/job-0d5ab5c3d094/{report.json,run-receipt.json}`,
  findings + prior-art inventory `saturn/results/context-external-cache/findings.md`,
  frozen config `saturn/configs/context-external-cache.json` (2 amendments pre-evidence),
  code `saturn/src/saturn/context_external_cache.py` + CPU tests.
- Pad ablation: `saturn/results/context-pad-occupancy/job-79ff59eb54d2/{report.json,run-receipt.json}`,
  frozen config `saturn/configs/context-pad-occupancy.json`,
  worker `saturn/workers/run_saturn_context_pad_occupancy.py`.
- Killed calibration jobs (timings replicated, no gates read): job-81c46f79934b,
  job-a9af6e455942, job-8330ab85d93a, job-e8a8e1d57dae.
- Baseline constants: `saturn/results/context-cost-baseline/` (E-D0); rewind contract:
  `saturn/results/context-rewind-accounting/three-rewind-behaviors.md` (E-C).
