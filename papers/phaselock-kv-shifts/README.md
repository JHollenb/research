# PhaseLock: stable position shifts for sliding KV caches

[Paper draft](paper.md) · Jacob Hollenbeck · 2026-09-24

This draft reports the completed Qwen streaming and kernel experiments. Section 5 includes a checked Saturn/mrun ring-buffer prototype, a held-out 20,000-token quality run with a stronger FP32-arithmetic/BF16-storage rerotation control, a two-script synthetic conversation recall assay, and a reserved production-engine result. The paper is not yet submitted or published.

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
