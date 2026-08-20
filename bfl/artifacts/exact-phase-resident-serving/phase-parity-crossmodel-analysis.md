# Cross-model exact phase-resident serving parity — analysis

Jobs: `job-4bc506e9fe64` (resident lane; 2026-08-19) and `job-6a7f7b0603dd` (seq-v2 corrected specimen; 2026-08-19), plus the fast-substrate follow-ups `job-271e7732c430` (fast-v1; fp8-seq cells clean, resident cell null) and `job-4da6fc7c4238` (fast-v2, complete) with mechanics probe `job-8f3276b63a61`. Panel: certified 4 prompts × 2 seeds (101, 202), 512×512, 4 steps, fresh CPU generator per image per arm, identical VAE memory controls and numerical contract per cell; only the residency/encoding schedule differed between arms.

## Hardware

All jobs ran on **beast**: AMD Ryzen 9 7950X (16 cores / 32 threads), NVIDIA GeForce RTX 4080 (**16,376 MiB VRAM**, driver 580.159.03), **63,427 MiB RAM** (~64 GiB physical), torch 2.13.0+cu130, diffusers 0.39.0, Python 3.14, weights pinned under `/mnt/big/llm-models`. Every absolute wall-time number in this document is bound to that host.

## Result table (certified lanes)

| cell (revision) | pipeline / lane | parity (pixel+PNG) | per-image | end-to-end | cand. VRAM peak | child RSS |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| flux2-klein-4b `e7b7dc27` | Flux2KleinPipeline, resident bf16 | **8/8 exact** | 12.73× | 7.02× | 8592 MB | 18.9 GB |
| flux2-klein-base-4b `a3b4f484` | Flux2KleinPipeline, resident bf16 | **8/8 exact** | 12.38× | 7.19× | 8592 MB | 19.0 GB |
| flux2-klein-9b `92196c8e` | Flux2KleinPipeline, sequential bf16 | **8/8 exact** | 1.18× | 1.06× | 676 MB | 35.0 GB |
| flux1-schnell `741f7c3c` | FluxPipeline, sequential + fp8-e4m3 layerwise | **8/8 exact** | 1.43× | 1.36× | 652 MB | 33.9 GB |

All cells: `encode_calls=4`, `unplanned_swaps=0` — exactly one encode per prompt, no accidental weight swaps. Job walls: 478 s (resident pair) and 279 s (sequential pair).

## Fast substrates for models that do not fit the card (2026-08-19 follow-up)

mrun's paged/fused substrates (`dense_qstore_cuda`, the `qwen3-moe-cuda` routed pager, `resident_advanced`) page quantized **LLM** weight rows/expert blocks and do not cover diffusion transformers, so the fast lanes here use the workspace's proven FLUX memory contracts plus one new hybrid built on them:

| cell | substrate (both arms) | parity | per-image | end-to-end | cand mean | VRAM peak |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| flux2-klein-9b-fp8seq | fp8-e4m3 storage + bf16 compute, sequential offload | **8/8 exact** | 1.18× | 1.06× | 6.08 s | 676 MB |
| flux2-klein-9b-kv-fp8seq | fp8-e4m3 + bf16, sequential offload | **8/8 exact** | 2.49× | 2.24× | 6.13 s | 675 MB |
| flux2-klein-9b-fp8resident | **hybrid**: fp8 denoiser resident on-card + accelerate-hook Qwen3-8B encoder streaming | **0/8 — separate numerical contract** (median ΔRGB 4.6, range 2.2–14.0) | 6.40× | 4.36× | **1.51 s** | 9,961 MB |

- **fp8-seq lanes** keep the certified schnell contract and remain bitwise within-substrate. Session variance is visible and recorded: the same 9b-fp8seq cell measured 1.54×/1.39× in `job-271e7732c430` and 1.18×/1.06× in `job-4da6fc7c4238`; parity was stable across both sessions, speedups were not. The KV pipeline benefits most (2.49×) because its per-image native path is ~15.3 s under the same memory contract.
- **The hybrid resident lane is the fast result: 1.51 s/image at 512² for a denoiser that is 18.6 GB in bf16 on a 16 GB card** — 3.9× faster than the bf16-sequential lane's 5.96 s and 6.4× vs its own streamed-fp8 reference session. It is also honestly *not* a bitwise lane: resident vs streamed materialization of the same fp8 weights diverges at bf16 accumulation level (working inference: kernel/workspace selection under different memory pressure), median ΔRGB 4.6 over the 8-image panel. It is a throughput contract with a declared numerical boundary, like batch>1 — usable where the fp8 storage contract is already accepted, and ~4× cheaper in time.
- VRAM story: the hybrid holds 9,961 MB peak (fp8 denoiser + bf16-skip modules + activations + streamed encoder window) inside the 16,376 MiB card; the Qwen3-8B conditioner (~16.4 GB bf16) never loads wholesale — it streams per-submodule only during the encode phase.
- **Mechanics note (probe `job-8f3276b63a61`):** the first hybrid attempt produced meta latents because `DiffusionPipeline._execution_device` resolves through the *first un-hooked* component and fell back to `self.device` — the encoder's meta tensors (probe printed `EXECUTION_DEVICE meta` while every transformer parameter was correctly fp8/bf16-resident on cuda). The fix is metadata-only: instance-set `_exclude_from_cpu_offload = {"transformer", "vae"}` so the walk reads the encoder hooks' cuda. This resolution gap is a diffusers property of mixed-hook pipelines, recorded here for the next hybrid.

## Interpretation (vocabulary per workspace policy)

- **Observation:** every one of the 64 candidate images is bitwise identical (pixel sha256 and PNG sha256) to its offload-reference twin, across three checkpoints, two pipeline classes (`Flux2KleinPipeline`, `FluxPipeline`), both conditioner ABIs (Qwen3 single-stream; T5 sequence + pooled CLIP), and both memory lanes (resident phase split; external sequential offload where the phase contract reduces to typed boundaries + exact-dtype embed caching + encoder detach).
- **Convergent trend:** with the certified 2026-07-31 Klein-4B receipt, bitwise phase-serving parity now has five independent cells across the supported FLUX surface on this host. The encode→denoise component boundary held without modification in every lane it was declared for.
- **Working inference:** the portable object is the explicit execution contract (typed phase boundaries, exact-dtype conditioner custody, scheduler/RNG identity), not any learned or model-specific state — consistent with the demo's original claim. Sequential-lane speedups (1.06–1.43×) are confined to encoder-stream removal, as preregistered; they are telemetry, not the claim.
- **Terminal status (engineering):** exact scalar phase-serving parity is established for the four pinned specimens above at 512²/4-step/declared guidance on the Beast RTX 4080 (two more bitwise cells added by the fp8-seq fast lanes: 9b and 9b-kv under fp8-e4m3 storage + bf16 compute). Not established by this run: 1024², batch>1, compile modes, FLUX.2-dev, klein-9b-kv reference conditioning, other hosts. The fp8-resident hybrid is a separate throughput contract (non-bitwise by measurement), not a parity lane.

## Instrument note (v1 → seq-v2)

The first job's sequential cells rendered all images 8/8 bitwise-exact and then crashed in post-render cleanup: the harness called `PhasePipeline.close()`, whose `module.to("cpu")` is illegal under external sequential offload (accelerate meta tensors). Parity was recovered from the surviving job-workspace PNGs (hash re-check on the collected copies), and `job-6a7f7b0603dd` re-ran both cells with `close()` skipped in non-resident lanes, reproducing 8/8 exactly with clean receipts. The v1 null cells are preserved as null evidence of the harness bug, not of any contract failure.

## Evidence

- `job-4bc506e9fe64/report.json`, `run-receipt.json` (resident cells + errors)
- `job-6a7f7b0603dd/report.json`, `run-receipt.json` (sequential cells, clean)
- `job-271e7732c430/report.json` (fast-v1: fp8-seq cells, resident null)
- `job-4da6fc7c4238/report.json` (fast-v2: all three fast cells complete)
- probe `job-8f3276b63a61` logs (`EXECUTION_DEVICE meta` diagnosis)
- Worker `saturn/workers/run_phase_parity_crossmodel.py`; submitter `saturn/workers/submit_phase_parity_crossmodel.py`; probe `saturn/workers/probe_fp8resident.py`
- Preregistration `saturn/experiments/2026-08-19-phase-parity-crossmodel/README.md`
- Prior certified receipt `mrun/docs/evidence/diffusers-phase-cuda-klein4b-smoke.json`
