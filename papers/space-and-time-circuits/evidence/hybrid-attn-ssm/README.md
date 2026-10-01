# Falcon hybrid attention and SSM evidence

This bundle pins the recovered E14 result used in [paper §6.4](../../paper.md). It copies the successful job's report, collection receipt, scheduler execution record and log without changing their bytes. The log is named `job-log.txt` here. The submitted worker, design and helper are included with their original source hashes.

`job-5efb5697631c` completed on 2026-10-01 at 01:40:58 PDT. Falcon-H1-0.5B-Base has 36 parallel attention/Mamba2 layers. The run uses CUDA FP32, TF32 disabled, eager attention, seed 0, two contexts and chunk suffix replay. Every singleton is swept at both formed-state cuts for identity and color; identity attention additionally has all 133 width-2/3/4/6 windows and complements.

The result supports attention-dominated post-subject dependence with partial SSM writing. Whole-attention replacement changes 17/22 identity candidates, SSM replacement changes 2/22, and both change 21/22. Attention and SSM whole-cut identity writes are 0.987 and 0.345. Attention's best singleton identity write is 0.224; the best six-layer necessity window carries 0.715 of its whole-cut effect. No new strict four-quadrant certificate is established. Color has only 9/20 admitted items, all in the first context. Candidate flips are not full-vocabulary greedy accuracy.

Run the record audit from any directory:

```sh
python3 /path/to/research/papers/space-and-time-circuits/evidence/hybrid-attn-ssm/verify_record.py
```

The verifier uses only Python's standard library and executes no model. It checks the pinned report SHA-256 (`914ee169683a7f751e2b3e1517c6b280ef2d7e3380083d3b13bd692e335a6121`), equality with the compressed report embedded in the log, the receipt's log hash, submitted source hashes, completion metadata and layer/window coverage. The included `verification-2026-10-01.json` is the saved derived audit. These are record-consistency checks, not an independent scientific replication.

The report saves aggregate medians and bootstrap intervals without raw item rows. It cannot support an independent re-bootstrap. Replay is numerically close rather than bit-identical, within the declared 1e-3 contract. Small SSM removal effects do not establish that SSM computation was dispensable during prefix formation. Falcon residual-formation, read-layer and retention-clock sweeps remain open.

The canonical [Saturn findings](../../../../../saturn/experiments/2026-10-01-e14-hybrid-attn-ssm/FINDINGS.md) retain the smokes and failed first full attempt as separate execution history. This bundle contains the completed scientific record only; recovery submitted no new model job.
