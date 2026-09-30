# Rotation Swamping: Why BF16 Cannot Move RoPE Keys, and Why QK-Norm Makes It Worse

*Formerly "PhaseLock: Stable Position Shifts for Sliding KV Caches".*

[Paper draft](paper.md) · Jacob Hollenbeck · updated 2026-09-30

This draft reports the completed Qwen streaming and kernel experiments. It distinguishes the larger fixed-window pass-key stress result from the smaller live conversation assay. Section 5 includes a checked Saturn/mrun ring-buffer prototype, a held-out 20,000-token quality run with a stronger FP32-arithmetic/BF16-storage rerotation control, and the two-script synthetic conversation recall assay. Section 6 summarizes a source-level audit of inference repositories, including the separate vLLM cache-identity report, and a paired native Hugging Face SinkCache model comparison. That public cache comparison did not reproduce the paper's catastrophic BF16 perplexity loss under bounded local positions. It did find a separate absolute-position integration defect: at a 1,024-token recent window, correcting retained-key phases improved post-fill perplexity from 14.933 to 10.018 on a 20,000-token train stream and from 15.982 to 10.441 on an independent 10,000-token test stream. No native production-engine run is pending. The paper is not yet submitted or published.

The underlying run identifiers and exact configurations are in the paper's reproducibility section. Raw artifacts remain in the workspace experiment archive pending preparation of a PhaseLock-only public supplement.

The [PhaseLock-only streaming summary](evidence/streaming-summary.json) gives unrounded table values and source-file hashes. Figure 1 has a [binned data extract](evidence/nll-bins.json) and a [rendering script](figures/plot_excess_nll.py). The extract records the SHA-256 of its full source result.

The [integrated prototype summary](evidence/integrated-prototype-summary.json) binds its raw output and checked Saturn receipt by SHA-256. The source experiment is in `saturn/experiments/2026-09-24-phaselock-integrated-ring/` in this workspace.

The [six-window shift profile](evidence/shift-scaling.json) records operation-scope scaling and its checked source receipt.

The [held-out integrated analysis](evidence/heldout-integrated-analysis.json)
contains paired block measurements and both raw-result hashes. [Figure 2](figures/heldout-integrated-nll.png)
shows the effect of BF16 versus FP32 rerotation arithmetic beside the two
immutable rings; its [script](figures/plot_heldout_integrated.py) is included.

The [conversation recall extract](evidence/conversation-recall.json) records
both matched scripts' per-case answers, target scores, source ages, and raw
result hashes. The source assay and full raw results remain in the local Saturn
experiment archive pending preparation of a public supplement.

The [pass-key stress extract](evidence/passkey-shift-stress.json) records the
fixed-window answer counts and source hashes separately from the live assays.

Section 6 (added 2026-09-30) reports the follow-up in `saturn/experiments/2026-09-29-phaselock-free-wins/`. It covers a single-buffer, CUDA-graphed ring that ties pristine rotate-at-read once attention accumulates in FP32, and rotation swamping ([probe](experiments/rotation_swamping/probe.py), [evidence](evidence/rotation-swamping.json)). It shows an FP32 absolute-position threshold at exactly 2^24 that integer phase removes, and bias-subtracted pre-RoPE quantization. It adds fused and GQA split-K kernels and true-position page retrieval. The [quality](evidence/free-wins-quality.json), [offset](evidence/free-wins-offset.json), [recall](evidence/free-wins-recall.json) and [speed](evidence/free-wins-speed.json) extracts are produced by [`build_free_wins_evidence.py`](build_free_wins_evidence.py); [`figures/plot_free_wins.py`](figures/plot_free_wins.py) renders Figures 3–5.

Sections 6.8–6.10 (added 2026-09-30) report the follow-up in `saturn/experiments/2026-09-30-phaselock-bithacks/`:
- **§6.8:** exact in-kernel integer trigonometry as fast as a stored phase table, and page-framed 4-bit keys that decode 8.6% faster than the fused BF16 kernel at 32k.
- **§6.9:** a Qwen3-0.6B/1.7B replication. Rerotation fails harder, even in FP32. The 2^24 threshold replicates. A QK-norm gain outlier explains Qwen3's plain-Q4 failure.
- **§6.10:** a measured law for the ring's speed advantage over rotate-at-read.

§6.4 adds 100,000-token streams with zero key rewrites and bit-exact restart, from `saturn/experiments/2026-09-29-phaselock-long-session/`.

The [speed](evidence/bithacks-speed.json), [quality](evidence/bithacks-quality.json) and [Qwen3](evidence/bithacks-qwen3.json) extracts are produced by [`build_bithacks_evidence.py`](build_bithacks_evidence.py).
