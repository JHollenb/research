---
title: "SourceAddress: Learning Where to Read Before Writing"
type: experiment-report
status: bounded-cross-model-development-trend
model: "Pythia-70M, Qwen2.5-0.5B, and Qwen3-0.6B"
tags: [source-address, sourcewrite, routing, recipient-local, self-debugging, cross-model]
---

# SourceAddress: Learning Where to Read Before Writing

> [!summary]
> We separate the question “which live state should an intervention read?” from “what payload should it write?” A learned SourceAddress policy selects a recipient-local source row or abstains, then a separate SourceWrite payload runs through the frozen native consumer. On the Pythia step-512 panel, learned addressing plus SourceWrite reaches `59/128` outputs versus `3/128` native, `12/128` fixed-address, and `78/128` oracle. The latest self-debugging follow-up relowers the payload and then the address policy, reaching `92/128` learned and `105/128` oracle on a fresh alphabet with exact source-zero/native behavior. Natural-language Qwen panels show the same address role in family-local coordinates, but direct package reuse is rejected. This is bounded control-plane evidence, not a universal semantic-address or capability-transfer claim.

## What we are testing

Many intervention experiments bundle three separate problems together:

1. find the live source state that contains the relevant information;
2. convert that source state into a recipient-compatible write;
3. verify that the unchanged native consumer uses the write.

If the final output is wrong, a single score cannot tell us whether the address, payload, writer, or consumer failed. This experiment makes the source address an explicit, typed program component and measures each plane separately.

The main Pythia organism is a synthetic relational task with moving key/value sources. The Qwen extension tests whether the same abstract key-to-value role appears in natural-language wrappers and can be recompiled into different model families. These are control-plane and compiler tests, not FLUX image claims; the BFL work uses the vocabulary to keep route, payload, consumer, and continuation failures distinct.

## How SourceAddress works

The program has five stages:

```text
native context
  → candidate address keys and masks
  → SourceAddressPolicy: select a row or abstain
  → fetch the live payload state at that row
  → recipient-local SourceWrite → frozen native consumer
```

An address key is not the payload itself. In the key/value organism, the selector may route by a predecessor key state while the write consumes the value state at the selected row. The policy is trained on cached boundary states, while the base recipient remains frozen. Serving excludes oracle positions, answers, prompt lookup, donor states, donor logits, and donor models.

The policy package is bound to the model, tokenizer, layer, width, and runtime contract. It can abstain when confidence is insufficient. A wrong-family package is rejected rather than silently interpreted in a different coordinate system.

## Pythia results

The step-512 Pythia panel compares the unchanged native consumer, a fixed source position, a learned SourceAddress policy, and an oracle source position:

| branch | correct outputs | rate |
| --- | ---: | ---: |
| native frozen consumer | `3/128` | `2.34%` |
| fixed source address | `12/128` | `9.38%` |
| learned address + SourceWrite | `59/128` | `46.09%` |
| oracle address + SourceWrite | `78/128` | `60.94%` |

The selector itself resolves `96/128` addresses. This is a native-consumer result, not only an address-classification score: the selected live state must pass through the separately compiled write and change the frozen recipient's output.

The fresh-alphabet control is the important failure localization. Address accuracy remains `68/128 = 53.13%`, but the old payload reaches only `12/128` even with oracle addresses. The address policy survived better than the payload/consumer interface, showing that “the route was wrong” is not the only explanation for a failed transfer.

The checkpoint-lowering follow-up shows recipient-local recompilation can restore part of the addressed behavior:

| recipient checkpoint | frozen policy | recipient-lowered policy |
| --- | ---: | ---: |
| step `1000` | `67/128` | `103/128` |
| step `4000` | `46/128` | `100/128` |

## Self-debugging SourceWrite follow-up

The latest self-debugging run uses paired native, learned, and oracle observations to choose which plane receives the next bounded update. The first diagnosis sends compute to payload/consumer relowering because the old oracle payload has regressed. After the payload improves, the next diagnosis sends compute to address relowering because routing is now the larger gap.

On the sealed fresh-process 128-row trial:

| branch | correct outputs |
| --- | ---: |
| native | `5/128` |
| fixed address | `13/128` |
| learned address + relowered payload | `92/128` |
| oracle address + relowered payload | `105/128` |
| wrong source | `1/128` |
| random address | `11/128` |
| source zero | `5/128`, candidate scores native-exact |

Address resolution reaches `113/128`. The earlier fresh-alphabet oracle ceiling was `12/128`, so recipient-local payload feedback raises the oracle ceiling to `105/128`; address relowering then delivers `92/128` without an oracle at runtime. The fresh trial contains no optimizer, donor model, donor trace, gold-label read, or oracle source-position read.

This is a development result on one synthetic organism, checkpoint, sequence length, fresh alphabet, and compiler seed. It does not establish autonomous multi-token continuation or a general self-improving model.

## Natural-language and family-local results

The semantic-source extension wraps six key/value facts in natural-language templates, then tests unseen and fresh wrappers. The native middle-layer geometry already retrieves the correct value row nearly perfectly; the learned policy adds a conservative selection and abstention surface.

| family | native fresh retrieval | learned selective precision | learned coverage |
| --- | ---: | ---: | ---: |
| Qwen2.5-0.5B, layer `12`, width `896` | `128/128` | `76.9%` | `50.8%` |
| Qwen3-0.6B, layer `14`, width `1024` | `128/128` | `82.1%` | `52.3%` |

The same semantic role is compiled separately into each family. Direct Qwen2-to-Qwen3 and Qwen3-to-Qwen2 package application fails closed because the model/tokenizer/layer/width ABI differs. Cross-family generalization here means semantic recompilation, not tensor portability.

## What the evidence establishes

The convergent trend is that source addressing is a distinct and often learnable control plane. It can select a moving recipient-local source, abstain conservatively, survive some checkpoint changes, and improve a frozen native consumer when paired with a compatible payload. The latest self-debugging run also shows that future feedback can identify whether payload compatibility or address delivery is currently the larger bottleneck.

The evidence does not establish a universal semantic coordinate system. An address does not carry the meaning by itself; it identifies a state that a separate writer may use. The payload can fail on a fresh vocabulary even when the address is right. Native geometry can be explicit in one family while the package remains unusable in another. Multi-token spans, contradictions, unanswerable inputs, additional seeds, more families, and long autonomous continuation remain open.

The correct status is a **bounded cross-model development trend**. The source address is a useful program boundary for debugging and recipient-local compilation, not a claim that a portable semantic block has been discovered.

## Local proof bundle

- [Bundle README](../artifacts/source-address-roadmap/README.md)
- [Latest roadmap matrix](../artifacts/source-address-roadmap/source-address-roadmap-matrix.json)
- [Roadmap summary](../artifacts/source-address-roadmap/source-address-roadmap-summary.md)
- [Self-debugging summary](../artifacts/source-address-roadmap/self-debugging-summary.md)
- [Self-debugging verification](../artifacts/source-address-roadmap/self-debugging-verification.json)
- [Bundle verifier](../artifacts/source-address-roadmap/verify.py)

The bundle keeps the latest matrix and verification receipts together so the headline numbers can be checked without relying on a narrative summary alone.
