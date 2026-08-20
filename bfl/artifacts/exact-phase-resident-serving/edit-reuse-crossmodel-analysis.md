# Cross-model reference-edit reuse — analysis

Jobs: `job-981b01d2de66` (v1, null — latent ABI crash), `job-d6832f02cdf2` (v2, three clean cells + KV class-mismatch null), `job-86f2ae8e1d0a` (kv-v2, null — replay decode signature), `job-df22ad4e5c17` (kv-v3, KV cell complete). All 2026-08-19 on **beast**: AMD Ryzen 9 7950X (16C/32T), NVIDIA GeForce RTX 4080 (16,376 MiB VRAM, driver 580.159.03), 63,427 MiB RAM, torch 2.13.0+cu130, diffusers 0.39.0, Python 3.14. Panel: the original certified edit-reuse instrument verbatim — one own-model reference (pinned fox prompt), four real edits, seed 92001, 256×256, 4 steps, cut 2, per edit: native image-conditioned generate, cache-miss capture, cache-hit capture, checkpoint replay, pixel compare, then invalidation by `reference_id`.

## Result table

| cell (revision) | lane | native↔replay exact | mean cosine / mean ΔRGB | cache hits | hit speedup (median) | native / replay median |
| --- | --- | --- | --- | ---: | ---: | ---: |
| flux2-klein-4b `e7b7dc27` | resident | **4/4** | 1.0 / 0.0 | 4/4 | **4,711×** | 0.350 s / 0.175 s |
| flux2-klein-base-4b `a3b4f484` | resident | **4/4** | 1.0 / 0.0 | 4/4 | **5,039×** | 0.350 s / 0.175 s |
| flux2-klein-9b `92196c8e` | bf16 sequential | **4/4** | 1.0 / 0.0 | 4/4 | **57,324×** | 5.43 s / 2.71 s |
| flux2-klein-9b-kv `a6dfb36e` | bf16 sequential | **0/4** | 0.9974 / ~7.6 | 4/4 | **56,040×** | 5.11 s / 2.70 s |

All cells: `invalidations == 4`, `reference_token_count == 256`, hits returned the identical cached checkpoint. The klein-4b control replicates the original receipt (4,696× → 4,711× same-session).

## Interpretation

- **Convergent trend (klein family):** the typed reference-edit cache is exact and mechanically clean across three checkpoints spanning both memory lanes. The 4,696× number is now a replicated measurement, and under the sequential lane the same lookup ratio grows to ~5.7×10⁴ purely because the miss (reference-conditioned prefix capture, ~2.8 s streamed) is more expensive — the hit stays a ~50 µs keyed lookup. Honest framing unchanged: this is the reference-capture lookup, not a full render; the full-continuation medians are the native/replay columns (replay saves ~48% of a native edit on 9b by skipping the shared prefix and reference prep).
- **Recorded boundary (KV):** the 9b-kv cell fails exactness 0/4 with real deltas (mean ΔRGB 5.4–12.7, max up to 181/255, cosine ≥ 0.994) while its cache mechanics pass cleanly. The divergence is semantic, preregistered, and localized: the KV pipeline's native loop orders tokens `[reference, target]` at step 0 and runs reference tokens under extract-mode causal (self-only) attention with cached K/V on later steps; mrun's generic Flux2 capture ABI (`_flux2_denoise_steps`) concatenates `[target, reference]` through the standard forward. The KV pipeline therefore needs its own trajectory ABI (ref-first ordering, `kv_cache_mode="extract"` with `num_ref_tokens`, and the 2-arg id-scatter unpack) before its checkpoints can claim native equivalence. Two adjacent runtime gaps were recorded on the way: the KV snapshot's `model_index.json` declares the base Klein class (the certified class must be loaded explicitly, as image_atlas does), and the generic `_flux2_decode` calls the Klein 4-arg unpack signature — which also predicts the same decode failure on `Flux2Pipeline` (Dev), untested here.
- **Working inference:** the reference-edit cache mechanism is checkpoint- and lane-portable within the plain-Klein ABI and not pipeline-semantics-portable into the KV adaptation. "Shared execution surface, local execution semantics" — the cache contract is the surface; the KV's attention semantics are the locality.

## Instrument notes (v1 → kv-v3)

Three harness corrections, each preserved as null evidence: v1 derived latent channels as `in_channels//4` (32) instead of the ABI's 128 — every cell crashed at reference generation before any render; v2 loaded the KV snapshot via `DiffusionPipeline.from_pretrained`, which honors `model_index.json`'s base Klein class — the KV cell failed its own class assert; kv-v2 exposed the decode-signature gap (KV 2-arg id-scatter unpack vs the generic 4-arg call), worked around worker-side by dropping the unused `(h, w)` args and delegating to the pipeline's own operator (recorded as `replay_decode_shim` in the kv-v3 report; no math changed).

## Evidence

- `job-d6832f02cdf2/report.json` (klein-4b, base-4b, 9b cells + KV null)
- `job-df22ad4e5c17/report.json` (KV cell, complete)
- `job-981b01d2de66/`, `job-86f2ae8e1d0a/` (null-evidence receipts)
- Worker `saturn/workers/run_edit_reuse_crossmodel.py`; submitter `saturn/workers/submit_edit_reuse_crossmodel.py`
- Preregistration `saturn/experiments/2026-08-19-edit-reuse-crossmodel/README.md`
- Original certified receipt `research/bfl/artifacts/exact-phase-resident-serving/edit-cache-receipt.json`
