# Exact phase-resident serving: evidence bundle

This bundle contains three complementary proof panels for the same execution idea:

All three panels use `black-forest-labs/FLUX.2-klein-4B` at revision
`e7b7dc27f91deacad38e78976d1f2b499d76a294`, through the native Klein pipeline. The parity panel is
BF16, 512×512, and four steps; the deep-replay receipt uses an eight-step trajectory.

1. `phase-parity-receipt.json` compares a phase-resident schedule with per-call CPU offload on
   eight prompts/seeds and records pixel/PNG hashes plus measured speedups.
2. `cheap-deep-replay-receipt.json` checks cached entering-cut suffix replay across several cut
   positions, including edited suffixes. Prefix capture/validation is outside the quoted replay
   timing.
3. `edit-cache-receipt.json` checks reuse of one 256-token image reference across four real edits;
   the companion run receipt records cache hits and invalidations.

Run `python verify.py` from this directory. The checks are receipt-level and do not claim parity
for faster batch/compile/FP16 lanes that are outside the exact scalar contract.

The 10.66× parity speedup is denoise-loop time after phase preparation; the companion 6.25×
end-to-end figure includes the setup charged by the benchmark harness. Neither includes a separate
Tracer/MRI/circuit-capture pass. The 4,696× cache number is a reference-state lookup, not a full
image render.
