# Exact phase-resident serving: evidence bundle

This bundle contains three complementary proof panels for the same execution idea:

1. `phase-parity-receipt.json` compares a phase-resident schedule with per-call CPU offload on
   eight prompts/seeds and records pixel/PNG hashes plus measured speedups.
2. `cheap-deep-replay-receipt.json` checks recompute-to-cut plus suffix replay across several cut
   positions, including edited suffixes.
3. `edit-cache-receipt.json` checks reuse of one 256-token image reference across four real edits;
   the companion run receipt records cache hits and invalidations.

Run `python verify.py` from this directory. The checks are receipt-level and do not claim parity
for faster batch/compile/FP16 lanes that are outside the exact scalar contract.
