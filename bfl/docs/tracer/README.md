---
title: BFL Tracer Documentation
type: research-documentation-index
status: bounded-exploratory
updated: 2026-08-19
claim_status: observations-trends-and-working-inferences
---

# BFL Tracer Documentation

This is the checkpoint-scoped documentation for the Black Forest Labs tracer campaign. The
[multi-model tracer demo](../../demos/multi-model-structural-tracer.md) carries the short narrative
claim: the FLUX.2 line has a stable coarse role grammar, while concrete addresses, payloads, and
causal meanings remain topology-local. These cards retain the model-specific anatomy and live
assay boundaries behind that claim.

## Checkpoint atlas

| model/checkpoint | revision | topology or boundary | tracer scope | profile |
| --- | --- | --- | --- | --- |
| `black-forest-labs/FLUX.1-schnell` | `741f7c3ce8b383c54771c7003378a50191e9efe9` | 19 joint + 38 single; 24 heads | 1,425 components; internal physiology | [Schnell](flux1-schnell.md) |
| `black-forest-labs/FLUX.2-klein-base-4B` | `a3b4f4849157f664bdbc776fd7453c2783562f4d` | 5 joint + 20 single; 24 heads | 625 components; internal physiology | [Klein Base 4B](flux2-klein-base-4b.md) |
| `black-forest-labs/FLUX.2-klein-4B` | `e7b7dc27f91deacad38e78976d1f2b499d76a294` | 5 joint + 20 single; 24 heads | 625 components; internal physiology plus prompt/image route work | [Klein 4B](flux2-klein-4b.md) |
| `black-forest-labs/FLUX.2-klein-9B` | `92196c8e11f7b6cf2b7493e037d8c5345c559216` | 8 joint + 24 single; 32 heads | 1,056 components; internal physiology | [Klein 9B](flux2-klein-9b.md) |
| `black-forest-labs/FLUX.2-klein-9b-kv` | `a6dfb36eca3a3906eb2fd460795adfb844e5fcce` | 8 joint + 24 single; 32 heads | 1,056 components; KV-variant physiology | [Klein 9B-KV](flux2-klein-9b-kv.md) |
| `black-forest-labs/FLUX.2-dev` | `26afe3a78bb242c0a8bb181dcc8937bb16e5c66c` | 8 joint + 48 single; 48 heads | 2,744 components; paged forward-only physiology | [Dev](flux2-dev.md) |
| `black-forest-labs/FLUX.2-small-decoder` | `a3efc24f613ef42d9428af62fdbd6f5fd8856c4a` | convolutional VAE decoder | decoder-native anatomy and lesions | [Small Decoder](flux2-small-decoder.md) |

## What the tracer measures

The forward-free Base Decoder reads checkpoint tensor names and shapes and assigns practical roles
such as selector/address, payload, carrier, operation, clock, and content. It establishes an
enumerable search universe without running a prompt or image.

The live Deep Decoder and MRI panels attach those names to a real native forward. They reconstruct
Q/K attention before rotary position encoding, record gradient × activation under a declared
internal output-energy objective, and test selected zero-output lesions. These are internal
physiology instruments: they are useful for choosing the next route experiment, but their MSE and
sensitivity values are not image quality or semantic scores.

The Klein 4B card has the additional prompt-conditioned, same-seed image and scheduler-return
register work that supports a bounded lexical-to-spatial transport trend. The other cards do not
inherit that image-level claim. Dev uses paged forward-only execution because its 64.45 GB
transformer cannot retain the full autograd graph on the 16 GB device. The Small Decoder uses a
convolution-native probe because it is a renderer, not a DiT denoiser.

## Role grammar and address boundary

Across Klein 4B, Klein 9B, and Dev, operation/MLP mass is about 65.75%, 66.53%, and 67.48%; each of
the address, selector, payload, and carrier families is about 7.31%, 7.39%, and 7.50%. That stable
coarse grammar is a search prior, not aligned semantic content.

`joint.i` means the ordinal `i` of a joint/double-stream block in the local checkpoint topology;
`single.i` means a later merged single-stream block. The syntax is reusable, but the depth,
weights, payload basis, and causal effect are not globally aligned. Every intervention must
re-enumerate the recipient topology and close the loop through the native image consumer.

## Claim boundary

The campaign establishes multi-model instrument reuse and a convergent role grammar. It does not
establish a universal circuit, a portable semantic address, or a package that can be copied from
Klein 4B to 9B, 9B-KV, Dev, Schnell, or a newer variant by name alone. Rejected or subthreshold
instrument results remain useful search evidence; they are not silently promoted to image claims.

## Source evidence

- [Obsidian tracer atlas](../../../../obsidian/experiments/bfl-tracer-2026-08-06/README.md)
- [Seven-model narrative](../../../../obsidian/blog/2026-08-06-tracer-seven-bfl-models.md)
- [FLUX.1 cross-compiled instrumentation](../../../../obsidian/blog/2026-08-09-saturn-flux1-cross-compiled-conditioner.md)
- [BFL campaign report](../../../../mstack/experiments/bfl_campaign/bfl-campaign-2026-08.md)
- [BFL README: model and checkpoint portability](../../README.md#models-checkpoints-and-portability)

