# Figures

The figures this paper relies on are decoded from bundled receipts in the companion papers. Rather than duplicate the image bytes, this file maps each figure to its source and receipt. Every figure is re-derivable from a bundle in this repository.

| figure (in a companion paper) | what it shows for this paper | receipt |
|---|---|---|
| [`circuit-panel-proof-sheet.png`](../../../bfl/docs/certified-semantic-circuits/data/heldout-seeds/circuit-panel-proof-sheet.png) | the twenty-axis route dossier (§3): strict, carrier, and candidate rows across semantic axes on held-out seeds | [2], `data/heldout-seeds/circuit-panel-ledger.json` |
| [`fig1-single-step-patching.png`](../../pointwise-instruments-miss-distributed-circuits/figures/fig1-single-step-patching.png) | time accumulation (§4): single-site, single-step interventions read as "no effect" while the whole path removes or carries the behavior | bundled `job-6650205b45eb` in [1] |
| [`fig3-probe-vs-consumer.png`](../../pointwise-instruments-miss-distributed-circuits/figures/fig3-probe-vs-consumer.png) | consumer-bound authority (§4): a validated probe reads "no content" in a state the unchanged consumer renders as a wolf | [1], §5 |
| [`fig4-heldout-prompt-identity.png`](../../../bfl/docs/certified-semantic-circuits/figures/fig4-heldout-prompt-identity.png) | a held-out-prompt route edit with the wrong-axis control (§5): dose moves the subject toward the target while the wrong-axis donor changes a different attribute | [2], §4 |

If the blind auto-detection receipts and the K/V-chain receipt listed under "Evidence to bundle" in [`../README.md`](../README.md) are later redacted and bundled, their decoded panes belong here: the blind route-recovery map (target-edge recall vs address-specific recall) and the failing-gate table for the language-model trial, decoded by a stdlib script alongside the bundle's `verify.py`, following the convention in [1].

- [1] [Single-Site Tests Miss Distributed Stores](../../pointwise-instruments-miss-distributed-circuits/paper.md).
- [2] [The Circuit That Survived Its Coordinates](../../../bfl/docs/certified-semantic-circuits/paper.md).
