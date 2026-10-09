---
title: "Learning where to read before writing"
type: experiment-report
date: 2026-08-19
models:
  - id: EleutherAI/pythia-70m
    role: synthetic key/value task (step 512 / 1000 / 4000 checkpoints)
  - id: Qwen/Qwen2.5-0.5B
    role: natural-language retrieval (layer 12, width 896)
  - id: Qwen/Qwen3-0.6B
    role: natural-language retrieval (layer 14, width 1024)
status: "bounded cross-model development result"
merged_from:
  - source-address-control-plane.md
tags: [language-models, routing, read-before-write, cross-model, interpretability]
---

# Learning where to read before writing

A language-model companion to the FLUX work: it isolates one piece of the intervention recipe we use
on the image models — *which live hidden state should an edit read?* — and measures it on its own.

## What we found

Most intervention experiments bundle three jobs together: find the hidden state that holds the
relevant information, turn it into a write the frozen model can accept, and check that the unchanged
model uses the write. When the output is wrong, a single score can't say which step failed. We split
the first job out as a learned **address policy** that picks one recipient-local row (or abstains),
then run a separate **write** through the frozen model. On a synthetic Pythia key/value task, learned
addressing plus the write reaches **59/128** correct outputs, against 3/128 for the frozen model
alone, 12/128 for a fixed address, and 78/128 for an oracle address. A later self-debugging pass,
which recompiles the write and then the address policy, reaches **92/128** learned (oracle 105/128)
on a fresh alphabet, with exact zero-write and frozen behavior. The same read-before-write role shows
up in natural-language Qwen models, in each family's own coordinates — but a package compiled for one
family cannot be reused directly in another.

## Why it matters

Activation patching usually fixes *where* it reads by hand and asks only what to write. By making the
read location an explicit, learned, abstaining component, we can localize failures: the address can
be right while the payload is wrong, or vice versa. This is the same discipline the FLUX image work
uses to keep route, payload, model and continuation failures distinct — tested here where ground
truth is cheap.

## How it works

The program has five stages: native context → candidate address keys and masks → a policy that
selects one row or abstains → fetch the live state at that row → a recipient-local write into the
frozen model. The address key is not the payload: in the key/value task the policy can route by a
*predecessor* key while the write consumes the *value* at the selected row. The policy is trained on
cached states while the base model stays frozen, and at serving time it sees no oracle positions, no
answers, no prompt lookup and no donor model. A package is bound to one model, tokenizer, layer and
width; a wrong-family package is refused rather than silently misread.

## Pythia results

| branch | correct | rate |
|---|---:|---:|
| frozen model alone | 3/128 | 2.34% |
| fixed source address | 12/128 | 9.38% |
| learned address + write | 59/128 | 46.09% |
| oracle address + write | 78/128 | 60.94% |

The policy itself resolves 96/128 addresses. The important failure is the **fresh-alphabet** control:
address accuracy holds at 68/128 (53.13%), but the old payload reaches only 12/128 even with oracle
addresses — so "the route was wrong" is not the only way a transfer can fail. Recompiling the policy
into later checkpoints recovers much of the behavior: step 1000 goes 67/128 → 103/128 and step 4000
goes 46/128 → 100/128 (frozen → recompiled).

## Self-debugging pass

The self-debugging run uses paired frozen, learned and oracle readings to decide which part gets the
next bounded update. It first sends effort to the payload, because the old oracle payload had
regressed; after that improves, it sends the next update to the address, now the larger gap. On a
sealed fresh-process 128-row trial:

| branch | correct |
|---|---:|
| frozen | 5/128 |
| fixed address | 13/128 |
| learned address + recompiled payload | 92/128 |
| oracle address + recompiled payload | 105/128 |
| wrong source | 1/128 |
| random address | 11/128 |
| source zeroed | 5/128 (scores frozen-exact) |

Address resolution reaches 113/128. The earlier fresh-alphabet oracle ceiling was 12/128; payload
feedback raises it to 105/128, and recompiling the address then delivers 92/128 with no oracle at
runtime. The trial used no optimizer, donor model, donor trace, gold-label read, or oracle
source-position read.

## Natural-language and cross-family results

Wrapping six key/value facts in natural-language templates, the native middle-layer geometry already
retrieves the right value row almost perfectly; the learned policy adds a conservative, abstaining
selection surface.

| family | native fresh retrieval | learned selective precision | learned coverage |
|---|---:|---:|---:|
| Qwen2.5-0.5B, layer 12, width 896 | 128/128 | 76.9% | 50.8% |
| Qwen3-0.6B, layer 14, width 1024 | 128/128 | 82.1% | 52.3% |

The same abstract key-to-value role compiles separately into each family. Applying a Qwen2 package to
Qwen3 (or the reverse) fails closed, because the model, tokenizer, layer and width differ.
Cross-family generalization here means recompiling the role, not reusing tensors.

## Limits and open questions

- A development result on one synthetic task, checkpoint set, sequence length, fresh alphabet and
  compiler seed; not an autonomous multi-token continuation or a self-improving model.
- An address identifies a state a separate writer may use; it does not carry the meaning itself, and
  the payload can fail on a fresh vocabulary even when the address is right.
- Native geometry can be explicit in one family while the compiled package is unusable in another.
- Open: multi-token spans, contradictions, unanswerable inputs, more seeds and families, and long
  autonomous continuation.

## Reproduce and inspect

- [Bundle README](../artifacts/source-address-roadmap/README.md)
- [Roadmap matrix](../artifacts/source-address-roadmap/source-address-roadmap-matrix.json) and
  [summary](../artifacts/source-address-roadmap/source-address-roadmap-summary.md)
- [Self-debugging summary](../artifacts/source-address-roadmap/self-debugging-summary.md) and
  [verification](../artifacts/source-address-roadmap/self-debugging-verification.json)
- [Bundle verifier](../artifacts/source-address-roadmap/verify.py)
