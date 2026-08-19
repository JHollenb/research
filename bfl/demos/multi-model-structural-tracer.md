---
title: "Multi-Model Structural Tracer: One Role Grammar, Topology-Local Circuits"
type: experiment-report
status: convergent-structural-trend
rank_in_bfl_survey: 3
model_scope: "Seven pinned BFL checkpoints/components"
tags: [bfl, flux, tracer, model-family, portability, role-grammar, circuit-discovery]
---

# Multi-Model Structural Tracer: One Role Grammar, Topology-Local Circuits

> [!summary]
> The tracer campaign examined seven pinned BFL artifacts rather than treating one FLUX.2
> checkpoint as the whole family. Across six DiT-bearing models, every transformer tensor mapped
> into a common structural vocabulary and the FLUX.2 4B/9B/Dev panels repeated a coarse role grammar:
> a large operation core, address/selector/payload/carrier interfaces, an early joint-stream region,
> and a later merged-stream region. The result gives the next experiment a useful search order. It
> does not establish a universal circuit, aligned bases, or portable semantic addresses.

## Checkpoint cohort

The campaign used these pinned model artifacts, with the Small Decoder retained as a decoder
boundary rather than forced into the DiT grammar:

| model/checkpoint | revision | native shape | evidence scope |
| --- | --- | --- | --- |
| `black-forest-labs/FLUX.1-schnell` | `741f7c3ce8b383c54771c7003378a50191e9efe9` | 19 joint + 38 single | static tracer; later native capture/resume follow-up |
| `black-forest-labs/FLUX.2-klein-base-4B` | `a3b4f4849157f664bdbc776fd7453c2783562f4d` | 5 joint + 20 single | static tracer; matched base/distilled diagnosis |
| `black-forest-labs/FLUX.2-klein-4B` | `e7b7dc27f91deacad38e78976d1f2b499d76a294` | 5 joint + 20 single | primary demos, tracer, route panels |
| `black-forest-labs/FLUX.2-klein-9B` | `92196c8e11f7b6cf2b7493e037d8c5345c559216` | 8 joint + 24 single | static tracer; bounded stock trajectory/readouts |
| `black-forest-labs/FLUX.2-klein-9b-kv` | `a6dfb36eca3a3906eb2fd460795adfb844e5fcce` | 8 joint + 24 single | tracer; native reference-K/V trajectory |
| `black-forest-labs/FLUX.2-dev` | `26afe3a78bb242c0a8bb181dcc8937bb16e5c66c` | 8 joint + 48 merged/single | tracer; component-decoupled runtime/instrumentation |
| `black-forest-labs/FLUX.2-small-decoder` | `a3efc24f613ef42d9428af62fdbd6f5fd8856c4a` | decoder-only boundary | decoder anatomy and paired diagnostics |

## What recurs across the FLUX.2 line

The static adapter mapped every tensor in the six DiT-bearing subjects (`mapped_frac = 1.0`) into
the same coarse vocabulary: content, state, address, selector, payload, carrier, clock, operation,
and readout. In the FLUX.2 family, the role budgets were:

| role budget | Klein 4B | Klein 9B | Dev |
| --- | ---: | ---: | ---: |
| operation / MLP | 65.75% | 66.53% | 67.48% |
| address, selector, payload, carrier — each | 7.31% | 7.39% | 7.50% |
| clock / time conditioning | 4.40% | 3.34% | 2.24% |
| content | 0.62% | 0.56% | 0.30% |

This is useful breadth evidence: it suggests searching address/selection, payload/carrier, and
early nonlinear operations before treating every tensor as equally likely. The first joint-block
MLP (`D0MLP`) is an especially useful homology candidate because a bounded internal lesion changed
the flow output in Klein 4B, Klein 9B, and Dev. The probe was not a common semantic image panel, so
it establishes a search anchor, not a shared concept circuit.

## The `joint.*` mapping is an address ABI

`joint.i` names the ordinal `i` of a joint/double-stream block in the checkpoint's own denoiser;
`single.i` names a later merged/single-stream block. Thus
`joint.2 → joint.3 → joint.4 → single.0` can be carried by the same typed route schema across
instrument implementations, but it is not a globally aligned layer path. Schnell has 19 joint
blocks, Klein 4B has 5, and Klein 9B/9B-KV and Dev have 8. The same ordinal has a different relative
depth and may carry a different basis, token role, or consumer effect.

The portable part is the instrumentation contract: enumerate the local topology, capture typed
state, replay the native suffix, and require the native consumer to close the route. The
checkpoint-local part is the payload, readout, semantic label, intervention dose, and causal
interpretation. A route map can therefore be reused as a search coordinate system without
pretending that a Klein 4B circuit can be copied into 9B, Dev, or FLUX.1 by name.

## Claim boundary

**Observation:** the seven-subject panel repeats a coarse structural vocabulary and the FLUX.2
4B/9B/Dev family repeats an operation-heavy role grammar.

**Convergent trend:** static anatomy, normalized graph structure, first-joint lesion assays, and
the FLUX.1 capture/resume follow-up support systematic instrument reuse across declared specimens.

**Working inference:** the grammar is a useful prior for choosing the next search surface, while
specific circuits remain topology-, checkpoint-, prompt-, and consumer-local.

**Terminal status:** convergent structural breadth trend. This is not a universal semantic circuit,
not aligned representation evidence, and not a license to transfer an address or payload without
fresh recipient-local validation.

## Evidence

- [Tracer campaign synthesis](../../obsidian/blog/2026-08-06-tracer-seven-bfl-models.md)
- [FLUX.1 cross-compiled capture/resume follow-up](../../obsidian/blog/2026-08-09-saturn-flux1-cross-compiled-conditioner.md)
- [BFL model/checkpoint README](../README.md#models-checkpoints-and-portability)
- [Model ledger](../../obsidian/experiments/bfl-tracer-2026-08-06/README.md)
