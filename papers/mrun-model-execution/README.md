---
title: mrun model execution paper
date: 2026-09-29
type: research-documentation
status: source-verified-draft
tags: [mrun, inference, scheduling, systems]
---

# mrun model execution

[Read the paper](paper.md): an implementation review of model acquisition, planning, fleet admission, guarded execution, paged and native runtimes, batching, state transactions, compiled reuse, serving, and evidence retention.

The review preserves its source snapshot, regression outcomes, controlled diagnostics, and five historical performance artifacts. It documents three limits found during verification and distinguishes fresh mechanics checks from earlier hardware measurements. No new pretrained-model benchmark was run.

[Evidence and reproduction](evidence/README.md). Verify the portable bundle with:

```bash
python3 evidence/verify.py
```

The paper describes a dirty working-tree snapshot dated September 29, 2026, rather than a released package identified by its version alone.
