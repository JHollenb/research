Completed experiment status and remaining work

The manuscript, its README and its figure source notes have been updated to reconcile completed experiments with older summaries. This is a status and wording correction, not a rerun of the scientific experiments. Historical receipts and retractions are preserved. The earlier timestamped critiques describe the manuscript before these edits.

**Corrections completed**

- E15/E17 write sweeps are now reported as completed, including the approximately 0.81 isolated writes in the two necessity-clean identity cells.
- The K/V versus hidden-state comparison now establishes cut sensitivity rather than claiming two currently certified LM cells.
- Qwen2.5-0.5B identity is described using E19's redundant L20–21 pair, alongside its time-formed execution profile.
- Qwen3-30B and the computed-object cell are no longer described as still awaiting full sweeps. The historical public Qwen3 bundle remains distinguished from the later isolated sweep.
- Klein 9B's two-seed identity result appears in the family summary; its 8/9 route gates and mixed lighting outcome remain visible.
- The SDXL heading now says four-quadrant test rather than successful certificate; its early necessity bottleneck is retained.
- The early exact-join limitations and degenerate raw bucket are labeled as earlier stages. E12/E18's subsequent successes are reported without claiming query-derived semantic selection was solved.
- The E10 update distinguishes the necessary consumed intermediate from the dispensable earlier, re-derived intermediate.
- Circuit-tracer identity and color outcomes are separated, and feature interchange is described as an analogue that leaves reconstruction error terms clean.
- The commit ledger is approximate, and the Gemma color downstream deviation of 0.208 is included.
- Window-width claims now refer to tested widths rather than exact minimum lengths. Gemma identity's 0.76 at eight layers is retained rather than treated as crossing 0.8.
- One residual intervention seeding formation is explicitly distinguished from a claim that native formation makes exactly one write.
- The conclusion reports the exact three strict quadrants satisfied by necessity-clean transformer cells rather than saying the class is vaguely half-established.

**What the existing AR evidence supports**

The author's source-write argument is correct: a one-time residual intervention can seed an ordered computation that runs through later layers. Its sufficiency does not locate the whole circuit at the injection boundary. Local source controllability and distributed downstream formation are different properties.

The paired existing profiles are stronger evidence than propagation alone. [E16](../../../../saturn/experiments/2026-09-30-full-layer-sweeps/FINDINGS-E16-residual-writes.md) measures a formation window: one upstream residual intervention can author the answer, with authority falling across or after the late commit. [E17](../../../../saturn/experiments/2026-09-30-full-layer-sweeps/FINDINGS-E17-isolated-kv-writes.md) shows that isolated K/V writes at many of those early boundaries have little authority, while late formed-store ports become strong. [E19](../../../../saturn/experiments/2026-09-30-full-layer-sweeps/FINDINGS-E19-window-necessity.md) shows that native necessity in the clean transformer cells is distributed across a wider late band even though its intervention write ports are concentrated or redundant. These results support a bounded time-formed commit circuit or store in autoregressive transformers.

The dispute is therefore not whether the experiments happened or whether a sufficient residual seed can participate in a temporal circuit. It is whether the manuscript's strict four-quadrant definition is the entire class or one subtype. Under the current definition, a singleton formed-store write near 0.81 exceeds the 0.2 bar. Propagation of a different intervention at the residual cut does not change that measurement. It does support a broader formation-based family.

**Remaining writing and release work**

1. Resolve the taxonomy consistently. A defensible proposal is a broad time-formed family, with the strict path-distributed four-quadrant profile as a subtype. AR commit circuits can be time-formed and locally writable; Mamba can be time-formed and have concentrated clock-held retention. Locality and temporal formation can coexist. The current section 2 definition has not been silently changed by this status pass.
2. Correct the section 2 argument that distributed linear representations cannot pass the whole-path quadrants. The eight-component counterexample in the [clarification](clarification-2026-10-01_110945_PDT.md) shows that assertion is false. Neither a temporal label nor a useful new category requires nonlinearity. The timing results reject an unweighted time-exchangeable sum, while the existing diffusion fit favors a signed weighted sum.
3. Update the two candidate abstracts and the opening class claims after the taxonomy is settled. Keep one abstract. Replace absolute claims that all instruments are unable to detect the class with the observed limits of particular sampled tests and feature bases. The later body and conclusion already report those limits more precisely.
4. Complete the closest-prior-work comparisons, including temporal diffusion circuit tracing and sequential CoT patching. The current Meng, Geva and Agarwal shared/different comparisons are substantive and should be preserved. A new synthesis across architectures can remain original when some of its ingredients have predecessors.
5. Complete the manuscript's declared citation and release collation: private receipt packaging/redaction, inherited citation corrections, the remaining source-count and label corrections, and the optional applied-pipeline paragraph. Appendix B remains the checklist; this pass did not modify historical source papers or claim that private artifacts have been published.

**Remaining scientific questions**

Query-derived semantic addressing remains unresolved despite successful subject-referenced joins. Late-writer method robustness still has only the older sampled operator panel. Exhaustive below-layer-grain localization, broader capability/task coverage and independent replication remain open. E14 is optional and unrun. These are scope limits and research opportunities, not a blanket requirement to add another large benchmark before publishing the bounded findings.

**The smallest stronger AR mechanism test**

For the broad time-formed AR claim, the existing evidence is already convincing. To establish more directly that the causal effect of a residual seed is mediated by the identified late store, combine the existing interventions on one clean cell:

| Arm | Purpose | Predicted result if the late store mediates the seed |
|---|---|---|
| Recipient baseline | Establish the source outcome | Source answer |
| One precommit donor residual write | Seed the target through the native suffix | Target answer |
| The same write, with its late formed-store band replaced by recipient state | Block the proposed mediator while retaining the seed | Loss of target authorship |
| Restore the coherent band captured from the seeded run | Rescue the proposed mediator | Recovery of target authorship |

Use matched parents, coherent counterfactual replacement, native continuation and measured no-op controls. Keep unrelated donor or band controls appropriate to the proposed route. The strongest result is the signed block-and-rescue effect on the unchanged consumer, not simply a scalar pass flag.

This test is proposed, not executed. A targeted search of the cited sweep and adjacent experiment records did not identify this exact combined mediation panel. If an existing receipt already contains it, the next step is collation rather than another experiment. A successful result would strengthen the formation-to-store causal account; it would not make a strong singleton formed-store write satisfy the existing strict singleton-write criterion.

Validation: the stale-status phrases were checked after editing, updated numerical summaries were compared with the cited E16/E17/E19 tables, two GPT-5.6 Sol high reviewers checked the revised LM and tooling interpretations, and git diff --check passed. No model jobs were launched.
