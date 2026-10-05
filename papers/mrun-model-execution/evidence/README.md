---
title: mrun model execution verification evidence
date: 2026-09-29
type: evidence-guide
status: complete-with-recorded-failures
tags: [mrun, verification, provenance, systems]
---

# Evidence and reproduction

This bundle distinguishes fresh local software verification from historical model/hardware measurements. It contains no model weights. Neither the portable verifier nor snapshot capture performs a production scheduler write.

## Fresh observations

[review-snapshot.json](review-snapshot.json) records the source HEAD/branch, pre-existing dirty-file inventory, hashes of 286 mrun Python source files and selected documents, package versions, test summaries, synthetic-host planning, explicit-dimension estimator diagnostics, a weight-free MoE capability diagnostic, and filtered read-only fleet health/version/inventory observations. The custom source-records digest is a review identity; it is not the compiler's runtime-distribution digest or a historical wheel identity.

[test-source-records.json](test-source-records.json) binds the tested source files. [test-commands.json](test-commands.json) retains the suite arguments, working directory, launcher and environment. All pretrained-model tests were disabled. Tests using small constructed models or temporary safetensors stores are mechanics checks, not pretrained-model qualification. Fleet integration starts its own localhost scheduler and agent with synthetic credentials and temporary data/work roots.

| Lane | Passed | Failed | Skipped | Original log | JUnit |
|---|---:|---:|---:|---|---|
| Initial review | 466 | 2 | 1 | [log](review-tests.log) | [XML](review-tests.xml) |
| Runtime and temporary fleet | 247 | 1 | 10 | [log](runtime-tests.log) | [XML](runtime-tests.xml) |
| Additional compiler/runtime | 130 | 0 | 0 | [log](compiler-tests.log) | [XML](compiler-tests.xml) |
| Isolated co-admission repeat | 1 | 0 | 0 | [log](coadmission-isolated.log) | [XML](coadmission-isolated.xml) |

The initial failures are `test_recorder_task_holds_all_layer_attention` and `test_count_logits_adds_a_vocab_scaled_term`. The estimator did not discover a Qwen2.5 configuration and used its fallback dimensions. A separate diagnostic supplied the dimensions assumed by these tests; it restored both formula assertions without loading weights or changing the implementation. That result qualifies the arithmetic under explicit inputs, not the missing configuration or observed peak memory.

The runtime failure is `test_small_jobs_coadmit_past_legacy_slot_cap`. The combined-suite log shows RAM headroom below the needed commitment during submission; all three jobs eventually succeeded, but simultaneous running was not observed. The unchanged case passed alone. Both outcomes are preserved, and the suite robustness issue remains open.

The capability diagnostic constructs no real engine. It calls `MoEStreamEngine.capabilities()` on a minimal object and confirms that the reported `mlp_acts=True` conflicts with the explicitly unsupported `forward_acts` method. It identifies a reporting defect without making a model-output claim.

## Historical artifacts

These files were copied byte-for-byte from `mrun/docs/evidence`. Their recorded qualification outcomes are historical. This review did not rerun their model or accelerator acquisition and does not assert that their promoted distributions match the current dirty checkout.

| Artifact | Original SHA-256 | Main use |
|---|---|---|
| [CPU branch pack](prior/sciencegraph-qwen25-0.5b-v3-cpu-30x-v2.json) | `06fc912c63ffe3dedb143023643347bd730c29ac52eebcfd3edea323e5d1b96d` | Prefix/suffix sharing, 30 trials |
| [Automatic campaign](prior/automatic-campaign-qwen25-0.5b-v3-cpu-30x-v1.json) | `a1a93e3fd76825756a7d2c4d91799554c0bbc0b457aeb94e2829e5e64cc068f0` | Duplicate prompt/readout sharing, 30 trials |
| [CUDA Graph acquisition](prior/cuda-graph-primary-4dc54fcd1048.json) | `402e1c9d91929399e4480028a265ae30db6e8e49b665f8b010f50b34e1f8871b` | Matched capture control, setup, residency, raw campaign samples |
| [Profile fusion](prior/profile-fusion-qwen25-0.5b-cuda-v1.json) | `461bc417f20cc26614d90bf8e67a52ae72da0c1cbf78543bef1fd4274a0b2a62` | Nine unqualified cells; counter-trend retained |
| [Resident selected-score service](prior/resident-batch-service-qwen25-0.5b-cuda-v1.json) | `df251ac23172a3d4ed16653f41bc33450c8937f7e12a422ec8f07a847391afb4` | Cohort/queue telemetry, cancellation and refill |

The CPU central speedups are ratios of marginal medians. The CUDA central contrasts are medians of paired duration ratios. The verifier recomputes the relevant medians, paired ratios, wins and graph setup break-even from preserved samples. It does not rerun the statistical interval procedures or independently certify the original measurement instrument.

## Verify the portable bundle

From the paper directory:

```bash
python3 evidence/verify.py
```

This checks [checksums.json](checksums.json), recorded test counts, and selected historical result arithmetic. The manifest is a local integrity record, not a signature or proof of authorship. Source and tested-file comparisons can be added when the reviewed workspace is available:

```bash
python3 evidence/verify.py --workspace /Users/jakeholl/domains
```

Source drift makes that optional comparison fail; it does not invalidate the preserved historical record. The bundle contains source hashes and links, not a complete archived source checkout or an installable runtime wheel.

## Repeat the review

The shared environment must already contain the checked-out mrun and its test dependencies. From the paper directory, choose a new output path:

```bash
python3 evidence/reproduce.py \
  --workspace /Users/jakeholl/domains \
  --output-dir /tmp/mrun-review-repeat
```

The helper refuses an existing output directory, runs the four recorded lanes in order, and saves separate logs/XML and return codes. It continues after a test failure so observations remain complete. The fleet lane can be sensitive to local memory pressure, pending fixture work, and availability of localhost port 9925. No original evidence is overwritten.

To capture a new source/environment observation afterward, use the workspace's shared launcher and a fresh destination:

```bash
rtk proxy /Users/jakeholl/domains/common/bin/common exec python \
  /Users/jakeholl/domains/research/papers/mrun-model-execution/evidence/capture_review.py \
  --workspace /Users/jakeholl/domains \
  --output /tmp/mrun-review-repeat/review-snapshot.json
```

Add `--live` only when read-only production scheduler health/version/host queries are wanted. The script refuses to replace an existing snapshot. Fresh repetitions are additional observations and do not retroactively turn the original failures into passes.
