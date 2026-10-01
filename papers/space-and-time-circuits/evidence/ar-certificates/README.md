# AR time-circuit certificates — public evidence bundle

Redacted receipts for the autoregressive (language-model) four-quadrant
certificates that paper §6.1 previously had only as private `saturn/results`
jobs. Produced for paper TODO **[E3]** (`paper.md:328`). Redaction follows the
convention in
`../../../pointwise-instruments-miss-distributed-circuits/evidence/four-quadrant-tests/REDACTIONS.json`
(host filesystem paths → `<host-path>`, machine nickname `beast` → `gpu-host`;
**all scalars unchanged**). Before/after SHA-256 and per-pattern replacement
counts are in `REDACTIONS.json`. The redactor is proved convention-correct by
reproducing the already-public `report-fp32-recheck-job-6299f2391d5c.json`
byte-for-byte (sha256 `c71544e404f935905c63fbb5ee56298d5276c2eb4cbab11d6f9ff56a7501f694`).

## Verify

```
python verify.py
```

Stdlib only. It re-checks every receipt's SHA-256 against `REDACTIONS.json` and
re-derives the headline four-quadrant values directly from the reports:
single-site necessity inert (|Δ_single/Δ_all| < 0.25), single-site write inert
(|W2_single| ≤ 0.1), whole-path write authors (W2_all s_norm ≥ 0.9), whole-path
necessity at the v2 multi-filler-floor bar (mean floor recomputed here), and the
Qwen3-8B dual-backend parity. Expected: `VERDICT: ALL PASS`.

## Contents

### `qwen3-8b/` — identity certificate, fp32, dual backend, multi-filler floor
The 8B cell could not be scored by the single-filler panel (the "creature" filler
still predicts "fox"); it is certified under a multi-filler floor
(mean of creature/figure/subject) in fp32, run on two independent backends that
agree to ≤ 0.0001 nat:

- `report-paged-fp32-job-ead9d040871b.json` / `run-receipt-*` — fused-paged
  fp32-CUDA (`PagedSafetensors`+`PagedLinear`, per-layer shard release; 8B fp32
  on a 16 GB card, peak VRAM ~5.3 GB). **Private** until this bundle.
- `report-cpu-fp32-job-6299f2391d5c.json` / `run-receipt-*` — CPU-fp32 twin
  (peak RSS ~47 GB). Already public in the pointwise paper's
  `evidence/four-quadrant-tests/`; copied here so the dual-backend parity
  headline (lp-gap 0.267 / 0.267, v2 PASS both) is self-contained.

Headline (both backends): single-site necessity frac L18 ≈ −0.10, L27 ≈ +0.24
(< 0.25); whole-path lp-gap to mean floor 0.267 ≤ 0.5 and margin clause pass
(v2 PASS); write single W2 = −0.004 (inert), W2_all s_norm = 1.020 (authors).

### `qwen3-30b-a3b/` — identity certificate, fp32 primary + bf16 companion
Both **private** until this bundle. The fp32 run carries the multi-filler floor
(`extra_floors`: figure, subject) and is the certifying run; the bf16 run is a
cross-backend companion (same quadrant shape, single-filler floor only).

- `report-fp32-job-ef8408d9c3d2.json` / `run-receipt-*` — `paged-layer-fp32-cuda`.
  Single-site necessity frac L24 ≈ −0.025, L36 ≈ −0.029 (< 0.25); whole-path
  lp-gap to the 3-filler mean floor 0.055 ≤ 0.5, margin clause pass (v2 PASS);
  write single W2 = −0.004 (inert), W2_all s_norm = **1.0376** (authors); pc_shift
  22.6.
- `report-bf16-job-7cc5b24954f0.json` / `run-receipt-*` — `paged-layer-bf16-cuda`
  companion: single inert, W2_all 1.0366 (authors), necessity-all within 0.19 of
  the single filler floor. Its fp32-specific *margin* bar is reported, not gated
  (a lone bf16 filler floor is fox-biased — the exact artifact the fp32
  multi-filler run removes; wall-a Addenda S/W).

## Not included, and why

`job-38c1c37dd591` is **not** a 30B receipt — it is a **SmolLM2-1.7B smoke job**
(`battery_name: "moe-smoke"`, one cell `smollm2-1.7b-pagedlayer.identity`,
`n_layers: 24`). The IRD draft mis-cited it as the 30B source; this is paper
correction **R3** (`paper.md:326, 593`). The 30B identity certificate is
`job-ef8408d9c3d2` (primary) + `job-7cc5b24954f0` (companion), as above.

## Provenance

Source jobs (private `saturn/results`): `ird-q3-paged-recheck/job-ead9d040871b`,
`ird-q3-fp32-recheck/job-6299f2391d5c`, `ird-battery/job-ef8408d9c3d2`,
`ird-battery/job-7cc5b24954f0`. Design: `saturn/experiments/2026-08-21-wall-a-addressing`
Addenda U/W/X (8B) and Y (30B). Built by
`saturn/experiments/2026-09-30-isolated-swap-reruns/build_bundle.py`.
