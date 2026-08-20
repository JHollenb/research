# Learned source addressing

Saturn now treats a neural read address as an explicit program component.
`SourceAddressPolicy` scores recipient-native address keys, selects a live row
or abstains, and passes that row identity to a separately compiled SourceWrite
payload. Address keys and payload states are distinct: a key/value circuit may
route by a predecessor key while consuming the value state at the selected row.

## Stack

```text
context tokens
  -> frozen recipient boundary states
  -> candidate address keys + mask + stable positions
  -> SourceAddressPolicy (position-equivariant selection/confidence/abstain)
  -> live payload fetch at selected row
  -> SourceWrite v2 (source-necessary recipient-local delta)
  -> frozen native consumer and continuation
```

The policy artifact is bound to model, tokenizer, layer, and width. Packages
are content-addressed, tamper-checked, and reject wrong-family application.
Serving inputs explicitly exclude oracle positions, answers, prompt lookup,
donor states/logits, and donor models.

## What the development matrix demonstrates

- A moving-source toy proves the selector learns content rather than a fixed
  position (>95% heldout, fixed-index <20%).
- Pythia step512 learns 96/128 held-out addresses. Through the frozen consumer,
  learned addressing reaches 59/128 versus 3/128 native, 12/128 fixed-index,
  and 78/128 oracle.
- On a fresh token alphabet, selector accuracy remains 68/128 but the old
  SourceWrite payload reaches only 12/128 even with oracle addresses. Saturn
  therefore localizes the miss to payload/consumer compatibility.
- A frozen step512 policy transfers partially to step1000 (67/128) and step4000
  (46/128). Recipient-local feedback relowers it to 103/128 and 100/128.
- In natural-language key/value contexts, middle-layer native geometry retrieves
  the right source at 127/128 or 128/128 on heldout Qwen2.5/Qwen3 prompts and
  128/128 on both fresh-template trials.
- Learned sealed policies provide conservative abstention: fresh-template
  selective precision is 76.9% at 50.8% coverage on Qwen2.5 and 82.1% at 52.3%
  coverage on Qwen3.
- The same semantic source role compiles into Qwen2.5 layer 12/width 896 and
  Qwen3 layer 14/width 1024. Direct cross-family tensor-package reuse fails
  closed; family-local semantic lowering succeeds.
- A self-debugging follow-up used paired oracle/learned counterfactual gaps to
  schedule payload relowering before address relowering. On a sealed fresh
  alphabet, recipient-local payload feedback raised the oracle ceiling from
  12/128 to 105/128; address relowering then delivered 92/128 without a runtime
  oracle, versus 5/128 native and 13/128 fixed-address execution.
- A typed semantic memory bus selected live Frame and persisted Thott payloads
  on 512/512 controlled heldout rows. Shuffled keys destroyed address and
  consumption; shuffled payloads preserved address but destroyed consumption.
- A two-Act dispatcher selected, abstained, fell back to native state, and
  rejected overlapping writes exactly on 160 sealed controlled rows.
- Address watchpoints emitted typed checkpoint-confidence events and compiled
  one-parent replay plans without launching independent condition runs.

## Use cases

- internal evidence retrieval before a factual repair;
- selective memory or context-register reads with calibrated abstention;
- tool-result routing without hard-coded token positions;
- source-aware hotpatches that can distinguish a wrong route from a bad payload;
- checkpoint migration where Saturn relowers only the broken component;
- model debugging that separates address, payload, write, consumer, and
  continuation failures.

The self-debugger ranks which component gets the *next bounded compute
allocation*. This is not an acceptance threshold. It compares the oracle
payload's regression against the learned route's gap to the current oracle,
mutates only the larger-opportunity plane, replays the paired panel, and then
reassesses. Every diagnosis is retained in a fingerprint-chained ledger.

## Claim boundary and next work

This is a bounded development result, not a terminal universal claim. The next
confirmation suite must recompile recipient-local payloads on fresh alphabets
and later checkpoints; add contradictions, unanswerable cases, dense
distractors, multi-token spans, and autonomous continuations; add non-Qwen
transformer and state-space families; and replicate the sealed matrix across
seeds with composition conflicts and continuation-triggered rollback.

The compact verified result is
`results/source-address-roadmap-matrix/matrix.json`; its sibling `summary.md`
contains the headline numbers. Reproduction harnesses live under
`experiments/2026-08-13-learned-source-address/` and
`experiments/2026-08-13-semantic-source-generalization/`.
