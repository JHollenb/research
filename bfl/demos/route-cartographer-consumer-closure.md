---
title: "Route Cartographer with Consumer-Closed Promotion"
type: experiment-report
status: consumer-closed-route-trend
rank_in_bfl_survey: 13
model: "FLUX.2 Klein 4B"
model_id: "black-forest-labs/FLUX.2-klein-4B"
revision: "e7b7dc27f91deacad38e78976d1f2b499d76a294"
checkpoint_role: "distilled native generator"
tags: [bfl, flux, route-cartography, address, consumer-closure, rollback, future-prediction]
---

# Route Cartographer with Consumer-Closed Promotion

> [!summary] A route cartographer captures 685 native states, 85 logical branches, and 325 observations across 56 nodes and 54 edges, spanning two consumers and two role-conditioned chains. Parallel routes have entropy 0.975–0.994, while serial corridors are far more selective. A held-out address selector reaches 0.990→0.977 accuracy. Address-driven updates are promoted only when the native endpoint improves: one update is promoted, three are rejected, and exact rollback succeeds 5/5. A fresh confirmation rejects the stronger interpretation that each local address is a standalone program; whole text-state transfers close every joint edge with weakest return alignment 0.911, while single-token QKV routes reach only 0.001–0.227.

## Research question

The experiment asks whether an internal route can be mapped as a stable address-driven program whose local carriers are sufficient to predict and control native endpoint behavior. A cartographer must do more than collect correlations: it must record route state, test held-out addresses, predict future observations, and close the loop by admitting or rejecting updates according to the native consumer.

The competing interpretations are a local program, a distributed carrier route, or a typed temporal coalition. The local-program hypothesis predicts that a single token or address-specific QKV state should transfer a meaningful endpoint effect. The carrier-route hypothesis predicts that addresses are useful selectors but that complete typed text-state transfers or multi-site coalitions are needed for consumer closure.

## Capture and representation

The capture contains 685 native states, 85 logical branches, and 325 observations across 56 nodes and 54 edges. It records the source state, 25 carrier candidates, and two native consumers: packed return and RGB endpoint. Two role-conditioned chains separate subject return from lighting return. A route signature is a structured record of address, state carrier, consumer, timing, dose, and endpoint response.

This cartography is native to `black-forest-labs/FLUX.2-klein-4B@e7b7dc27f91deacad38e78976d1f2b499d76a294`. The address register is deliberately useful beyond one report, but its entries are local ordinal coordinates: `joint.i` and `single.i` refer to the tested checkpoint's own topology. The same typed route schema can be re-enumerated for Klein 9B, 9B-KV, Dev, or FLUX.1; an address, carrier value, or semantic interpretation must not be copied across those models without a fresh native-consumer promotion test.

Parallel route entropy lies between 0.975 and 0.994, indicating broad participation across candidate carriers. Serial corridor entropy is lower: the subject-return corridor at `single.18` is 0.114, RGB subject return is 0.374, and lighting is 0.299 for subject return and 0.455 for RGB. These values describe route concentration under the cartographer's instrumentation; they do not directly translate into semantic ownership.

## Prediction and promotion

The held-out address selector predicts route addresses at 0.990 accuracy in the first measurement and 0.977 in the later held-out evaluation. This is a useful selector result: address information is not random, and the cartographer can forecast which carrier will be involved in the next observation.

Promotion is stricter than selection. One address-driven update is promoted because the native endpoint improves. Three later updates are rejected because the native endpoint does not improve. Exact rollback succeeds 5/5, restoring the prior endpoint and route state. The result demonstrates a closed consumer gate: internal predictability is necessary for promotion but not sufficient.

[Cartographer route signatures](../artifacts/route-cartographer-consumer-closure/route-signatures.json)

## Fresh confirmation and the local-program demotion

The fresh confirmation tests four single-token QKV routes. Their endpoint return alignments are 0.001, 0.227, 0.105, and 0.197, all below the 0.50 closure gate. These routes show that local addresses can be causally live without being complete programs.

The complementary whole text-state transfer closes every joint edge, with the weakest endpoint return alignment 0.911. The gap between single-token QKV and whole text-state transfer is the central result: the address register is a real selector and carrier map, but local address identity alone is not enough to reproduce the full consumer-level operation.

The simplest working explanation is a typed temporal coalition. Address, carrier content, route timing, and downstream consumer jointly determine the endpoint. The cartographer can discover and predict that structure, but it should not collapse the structure into a single-token program without a stronger closure result.

## Controls and limitations

Held-out address prediction controls memorization of the captured sequence. Native endpoint promotion controls internal-only overfitting. Rejected updates and exact rollback make negative evidence operational rather than anecdotal. Single-token QKV routes test the local-program hypothesis directly, while whole text-state transfer tests whether a fuller typed state closes the consumer.

The route map is instrument- and consumer-specific. Entropy depends on the candidate carrier set, the route representation, and the chosen endpoint. A route with low entropy in one consumer can be distributed in another. The result does not establish that every semantic behavior has the same 56-node topology or that every address is stable across model revisions.

## Claim status

**Observation:** route addresses and carriers are predictable, but consumer-level promotion rejects most local updates unless the native endpoint improves.

**Convergent trend:** capture statistics, selector accuracy, promotion/rejection, exact rollback, single-token failures, and whole-state closure converge on a distributed route interpretation.

**Working inference:** the route address register is a cartographic selector for a typed temporal coalition, not a catalog of independent local programs.

**Terminal status:** consumer-closed route-mapping trend. It is not a universal route topology, a proof of local semantic ownership, or a guarantee that address selection alone is sufficient for native execution.

The methodological result is the admission rule: route prediction is only a proposal. A candidate enters the promoted state only when the native image consumer improves; otherwise the update is rejected and the prior state is restored exactly. This keeps internal route utility separate from actual image capability and makes negative futures part of the evidence rather than discarded noise.

## Local proof bundle

The bundle contains capture receipts, route signatures, native outcomes, held-out predictors, and the cartographer narrative:

- [route signatures](../artifacts/route-cartographer-consumer-closure/route-signatures.json)
- [native route outcomes](../artifacts/route-cartographer-consumer-closure/native-route-outcomes.json)
- [multidomain report](../artifacts/route-cartographer-consumer-closure/multidomain-cartographer-report.json)
- [bundle verifier](../artifacts/route-cartographer-consumer-closure/verify.py)

Run `python ../artifacts/route-cartographer-consumer-closure/verify.py` from this directory to verify capture size, route entropy, selector accuracy, promotion/rollback, local-route failures, and whole-state closure.
