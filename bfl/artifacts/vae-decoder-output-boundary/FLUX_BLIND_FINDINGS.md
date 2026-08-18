---
title: "Blind circuit probe on a real FLUX artifact"
type: experiment-record
status: measured
date: 2026-08-05
claim_status: exploratory
tags: [experiment, flux, manalysis, mstack, mrun, blind-debugging, causal-debugging, propagation, generative-models]
related:
  - "[[../2026-08-05-debugger-excellence-toy-causal-graphs/BLIND_CIRCUIT_FINDINGS|Toy blind circuit findings]]"
  - "[[../2026-08-05-001500-flux-evidence-graph-donor-map/README|FLUX same-device donor map]]"
  - "[[../../manalysis/src/manalysis/generative/dataflow.py|TensorFlowGraph]]"
  - "[[../../manalysis/src/manalysis/generative/runtime_trace.py|Runtime trace]]"
---

# Blind circuit probe on a real FLUX artifact

## Result

The moonshot-derived blind structural pass ran on the immutable same-device FLUX2 donor-map
artifact produced by mrun. It detected an **opaque intervention-to-output propagation envelope**,
not a unique semantic circuit.

| measurement | result |
|---|---:|
| intervention arms | 283 |
| nonzero source perturbations | 283 |
| output-changing arms | 283 (1.000) |
| opaque source groups | 7 |
| opaque observed stages | 24 |
| candidate output producers | unit.23 |
| repeated output corridor | unit.07, unit.09, unit.10, unit.12, unit.14, unit.15, unit.16, unit.18, unit.19, unit.20, unit.21, unit.22, unit.23 |
| unique semantic circuit | **not detected** |

The identifiers in the result are intentionally opaque (`source.NN` and `unit.NN`). The detector
remapped source and stage coordinates before computing support, backward reachability, or graph
convergence. It did not read arm labels, donor metadata, model-role labels, post-hoc scores, or an
oracle.

## What the artifact says

- **Observation:** every one of the 283 nonzero source perturbations moved the terminal decoded
  summary.
- **Trend:** the interventions share a repeated late-stage corridor: `unit.07, unit.09, unit.10, unit.12, unit.14, unit.15, unit.16, unit.18, unit.19, unit.20, unit.21, unit.22, unit.23`.
- **Working inference:** the instrumented VAE suffix carries a broad perturbation envelope into the
  output. This is consistent with the earlier same-device dose and consumer-trajectory trends.
- **Terminal claim:** this artifact does not identify a semantic feature circuit, a necessary
  upstream subset, or a sufficient subset.

The summary-only closure pass and the graph-backed backward pass converge on the same output
corridor: **True**. That agreement is useful instrument evidence,
but it is not independent causal proof because both views consume the same per-arm summaries.

## Why this is weaker than the toy result

The toy stepping stone had isolated intervention arms, negative controls, and recorder closures
that left some branches silent. Here, every nonzero intervention is already on a route that reaches
the terminal, and the report gives only aggregate stage deltas. A downstream carrier or readout can
therefore look like a common circuit member even when the artifact cannot establish its necessity.

This is exactly the distinction the blind pass is meant to expose: on a real model it finds a
repeatable structural lead, then stops at the evidence boundary instead of converting propagation
into circuit identity.

## Validation and provenance

The specimen is the FLUX2 Klein 4B CUDA/BF16 run `job-a2aacc5c10d7`, completed with strict mrun
preflight. The donor-map receipt reports success, about 553 seconds elapsed, and 8.5 GB peak VRAM.
The blind pass itself is local read-only analysis of those immutable results; no duplicate GPU suite
was submitted.

Inputs:

- [`same-device-donor-map.json`](../2026-08-05-001500-flux-evidence-graph-donor-map/results/same-device-donor-map.json)
- [`same-device-donor-map-receipt-job-a2aacc5c10d7.json`](../2026-08-05-001500-flux-evidence-graph-donor-map/results/same-device-donor-map-receipt-job-a2aacc5c10d7.json)
- [`rank1-vae-trace.json`](../2026-08-04-214836-flux-nccl-substitution/results/raw/component-substitution/rank1-vae-trace.json)

Reproduce:

```bash
cd /Users/jakeholl/domains/manalysis
/Users/jakeholl/domains/manalysis/.venv/bin/python \
  ../experiments/2026-08-05-flux-blind-circuit-probe/flux_blind_circuit_probe.py
```

The JSON result is [`results/flux-blind-probe.json`](results/flux-blind-probe.json). The executable
checks are in [`test_flux_blind_circuit_probe.py`](test_flux_blind_circuit_probe.py).

## Next decisive assay

Keep coordinates opaque, but add matched interventions that create a silent baseline, a localized
lesion, and a dose-matched route swap. Capture raw branch-level tensors at the latent boundary and
at the candidate corridor. Then compare necessity, collateral change, and repair/continuation
effects across seeds. Until that exists, the correct result is an output-connected envelope, not a
discovered FLUX circuit.
