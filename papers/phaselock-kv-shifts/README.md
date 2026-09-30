# Rotation Swamping: Why BF16 Cannot Move RoPE Keys, and Why QK-Norm Makes It Worse

*Formerly "PhaseLock: Stable Position Shifts for Sliding KV Caches".*

[Technical write-up](paper.md) · Jacob Hollenbeck · updated 2026-09-30

A sliding KV cache that re-rotates its stored keys one position at a time and writes them back in BF16 loses the rotation of every RoPE pair with frequency below 2⁻⁹: 35 of Qwen's 64. With FP32 rotation arithmetic this still costs 1.4% perplexity on Qwen2.5-1.5B and 27% and 49% on Qwen3-0.6B and 1.7B, and keeping only those 35 pairs exact removes 97–103% of the loss. Qwen3 suffers more because its QK-norm gain concentrates key energy in the same slow pairs. Shifting in blocks of 16 or more positions, or never rewriting a key, removes the cost. The write-up also covers an FP32 position cliff at exactly 2²⁴ that integer phase (PhaseLock) removes, per-channel correction that makes 4-bit pre-RoPE keys usable, fused Triton kernels, true-position retrieval of evicted pages, and an audit of public cache implementations, including a position-contract defect in the Hugging Face `SinkCache` Hub cache.

The write-up is not submitted or published. The full research-paper version, with the superseded first-draft experiments (live-stream and integrated-prototype consumers, pass-key stress test, scripted conversation assay), is in git history at commit `c4d1e09`; its evidence extracts remain in [`evidence/`](evidence/).

## Contents

- [`paper.md`](paper.md): the technical write-up.
- [`evidence/`](evidence/): result extracts, each binding its raw results and executed sources by SHA-256. [`review-fixes.json`](evidence/review-fixes.json) holds the block-shift and exact-pair statistics.
- [`figures/`](figures/): figures and the scripts that regenerate them.
- [`experiments/`](experiments/): the swamping probe and the native `SinkCache` comparison harness.
- [`build_free_wins_evidence.py`](build_free_wins_evidence.py) and [`build_bithacks_evidence.py`](build_bithacks_evidence.py): regenerate the §3–§10 extracts from raw results.

The model runs themselves live in `saturn/experiments/2026-09-29-phaselock-free-wins/`, `2026-09-29-phaselock-long-session/`, `2026-09-30-phaselock-bithacks/` and `2026-09-30-phaselock-review-fixes/` in this workspace; the write-up's reproducibility table maps each result to its jobs.
