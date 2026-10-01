# E20 follow-up and remaining work

Written 2026-10-01. This updates the proposed experiment and pending-definition
items in `status-sync-and-remaining-work-2026-10-01_115212_PDT.md`. That earlier
review remains a historical record; its E14/E20 status is superseded here.

## The optional experiment was run

E20 lives in the original
`saturn/experiments/2026-09-30-full-layer-sweeps/` directory and is registered
in the consolidated space-and-time suite. Smoke `job-ae430ab2aebd` and full
`job-e1f652e80f43` succeeded through mrun on Beast. The full run used the same
42-row Qwen2.5-1.5B identity panel, CUDA FP32/eager, with a single resident lease
and no automatic retry.

One clean donor residual entering L12 seeded a filler recipient. The recipient
then formed its own downstream state. We captured the resulting L22–27 subject
K/V, blocked it with unseeded recipient K/V, and transplanted it into an
otherwise unseeded recipient. Subject computation finished before cache edits;
only the unchanged suffix read the overwritten entries.

- The L12 seed raised target logprob by a median 3.515 nats.
- The late-band block removed **92.4%** of that effect, median itemwise ratio
  with 95% bootstrap interval **76.5%–103.0%**.
- Transplanting the seed-formed band into the unseeded recipient recovered
  **87.1%**, interval **85.0%–89.4%**; the target became full-vocabulary top-1 on
  **37/42** rows, compared with **38/42** for the complete seed.
- The matched-width earlier L16–21 block retained **93.4%** of the seed effect.
- A wrong-identity band authored the wrong donor's token on **37/42** rows and
  the intended target on **0/42**.
- All 42 seed denominators were positive and well separated from zero. Every
  late-band block lowered target logprob. Context medians converge, while the
  complete signed row distribution remains saved.

Exact block/restore is a replay control. The claim-bearing rescue is the
transplant into an **unseeded** recipient. Source identities, log/report
round-trip, complete rows/arms, finite values, arithmetic and replay diagnostics
passed the independent artifact verifier. The evidence pipeline ingested the
mechanics receipt and verified its custody. Its surface is explicitly
`target-receipts-only`; no activation-stream coverage or semantic decoding is
implied.

## What this changes

This is the combined source → endogenous formed store → native consumer test
that was missing from the earlier critique. It strengthens the AR temporal
formation account substantially. Your argument that a locally sufficient
residual intervention can seed a computation across later layers is correct;
the new experiment also measures which downstream store carries most of its
effect.

The paper now defines **time-formed circuits** as the broad family and the
**strict path-distributed four-quadrant circuit** as a subtype. It names
**diffusion accumulation**, **autoregressive formation/commit**, and **SSM
retention/latch** variations, retaining FLUX and Mamba as tested specimens.
Locality and temporal formation can coexist. The four quadrants do not exclude
weighted linear accumulation.

E20 does not change the existing isolated L23 write of approximately 0.81. The
Qwen cell therefore still lacks the strict subtype's low-singleton-write
quadrant. It does not identify a unique route, show that natural donor
computation has the same complete mediation, decode intermediate semantics,
prove nonlinearity or establish free-running chain-of-thought tracking.

## What remains

No additional experiment is required merely to report this bounded result.
The publication work is to finalize the abstract, finish citation/backlink and
release collation, package the strongest runnable evidence, and keep the
specimen-level claims consistent across the paper and figures.

Further scientific extensions remain separate: held-out/natural-task and
cross-model replication of E20; finer-grain source/store/consumer mapping;
query-derived semantic addressing; and tracking state in free-running CoT
rather than only the controlled E10 arithmetic panel. Falcon's E14 is now
completed as a formed-state hybrid sweep, while its source-formation, read-layer
and retention-clock assays remain unmeasured. These are scope boundaries and
research opportunities, not reasons to erase the convergent evidence already
reported.

Full method, heterogeneity, metrics and receipt links:
[`FINDINGS-E20-mediation.md`](../../../../saturn/experiments/2026-09-30-full-layer-sweeps/FINDINGS-E20-mediation.md).
