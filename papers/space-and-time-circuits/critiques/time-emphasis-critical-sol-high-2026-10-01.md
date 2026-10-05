# Critical scientific review — time-formed circuits and functional scaffolds

**Reviewer:** independent GPT-5.6 Sol/high pass  
**Date:** 2026-10-01  
**Scope:** `time-emphasis-paper.md` and companion `bridge-paper.md`; manuscript and underlying findings/raw evidence were read only. No model runs or manuscript edits were made. The existing read-only verifiers were used where available.

## Overall assessment

The Qwen result is the strongest evidence in the pair: an early source intervention changes an endogenously formed late K/V state, blocking that late state removes most of the source effect, and an independently obtained late state rescues an unseeded recipient. The separate native read intervention closes a bounded source → formed store → consumer anatomy. FLUX supplies a well-bounded strict path-distributed subtype under a declared native endpoint and intervention matrix. The companion paper identifies a promising recurring role organization, but its strongest present conclusion is **reuse of a causal interface with context-dependent consumption**. A learned scaffold or feedback loop remains a working inference until recurrence is distinguished from architecture/depth and an actual carried-state update cycle is shown.

No material quantitative contradiction was found. The main corrections are conceptual claim boundaries rather than adverse empirical findings.

## Strengths to preserve

- The decoder evidence is unusually well separated into source, endogenous recipient formation, independent rescue, and consumer read. Exact replay closure is correctly kept distinct from independent rescue (`time-emphasis-paper.md:83-121`).
- The manuscripts consistently distinguish temporal formation from spatial locality. A locally writable late store can still have a temporally distributed construction history (`time-emphasis-paper.md:69-73,145-151`; `bridge-paper.md:38-45`).
- The FLUX strict subtype is appropriately threshold- and interface-bounded. The paper preserves partial singleton effects and explicitly avoids claiming nonlinearity (`time-emphasis-paper.md:171-198`).
- The eye example is reported with the necessary limitations: target-assisted full contextual text stream, visible collateral, distinct whole-image and eye-region observables, and no claim of an isolated iris module (`time-emphasis-paper.md:204-210`).
- Both papers correctly define runtime “commitment” without implying online weight learning or irreversible training-time change (`time-emphasis-paper.md:63,212`; `bridge-paper.md:28,138-141`).
- Counter-trends are retained: the early Qwen layer is not a standalone store, narrow isolated windows can be strong, Gemma’s observable is basis-dependent, and deletion results differ by FLUX deletion construction.

## Findings requiring revision

### [Major] Make the time-formed class test dissociative rather than existential

**Locations:** `time-emphasis-paper.md:53-65`, especially line 61; abstract line 20.

“Ordered construction or retention produces a state that controls a later consumer” still describes almost every deep or recurrent inference graph. Requiring a source, state, and consumer does not by itself prevent ordinary layerwise computation or architectural cache append from being relabeled as the proposed class.

Define the operational class by the intervention **dissociations** already present in E20:

1. an earlier source intervention changes a later state;
2. the later state is formed endogenously after the source intervention;
3. an isolated block at that later state removes the source effect;
4. an independently sourced state rescues an otherwise unseeded recipient; and
5. the later native consumer/read is independently perturbed when a full source → store → consumer claim is made.

State a negative comparator: generic ordered computation, cache append, or point-local pass-through without a separable later mediator and independent rescue does not establish this class. This makes E20 the positive exemplar instead of allowing the definition to earn itself by relabeling.

### [Major] Bound “formation trajectory” to what E20 actually localizes

**Locations:** `time-emphasis-paper.md:20,24-26,61-65,79-121`.

E20 identifies an early source, a later endogenous mediator band, and a consumer; it does not identify every intermediate carrier, writer, or edge between L12 and L22–27. “Formation trajectory” can therefore be read more strongly than the intervention supports. Add a direct scope sentence: **the experiment identifies a formation interval and causal endpoint, while the internal construction path through that interval remains unresolved.** The current acknowledgment that a complete head graph is unavailable is helpful but less precise than this boundary.

### [Major] Same stored patch with a changed query does not rule out a static fact table

**Locations:** `bridge-paper.md:24,36,96-102,148-160`.

The byte-identical late patch having different effects under different queries establishes query-conditioned **read/use** of stored state. It does not distinguish dynamic storage from a static K/V fact table: fixed values with query-dependent attention predict exactly this result. Replace “separate contextual consumption from a static fact table” with the narrower result: the stored state does not have equal, query-independent authority; the live query governs its native consumption. Preserve the experiment as strong evidence for dynamic semantic subcircuits on a reused interface, but list static storage plus dynamic read as a live explanation.

### [Major] Separate a reusable causal interface from a learned functional scaffold

**Locations:** `bridge-paper.md:22,49-71,88-102,134-160,199-205`.

The L22–27 K/V band is also an architecture-provided, broad late-cache interface. Reuse across fact roles may reflect a generic late-layer access/bottleneck property. The data establish a reused causal interface; “learned scaffold” needs a discriminator beyond successful role labels.

Add an operational scaffold criterion near the definition, not only as future work:

- freeze the candidate role/site/edge profile before held-out contexts and operations;
- show recurrence across at least two distinct semantic operations or payload families;
- require selective native-consumer effects under same-parent wrong-source, wrong-role, and changed-query controls; and
- compare against matched depth, width/energy, and architecture-preserving null profiles.

Until those controls are run, label the learned scaffold as a working inference. Do not turn these into retrospective hard gates or erase the current trend. The manuscript already proposes the right prospective depth/energy/null tests at `bridge-paper.md:160,199-205`.

### [Major] Reserve “loop” for demonstrated carried-state feedback

**Locations:** `bridge-paper.md:57-71,138-160`.

The paper uses recurrence both for repeated functional roles and for state feedback. These are distinct claims, especially beside Mamba’s architectural recurrence. Use “recurring role organization” for recurrence across tasks/operations. Claim a loop only when an intervened carried state changes a later read/write and the later write commits a newly testable state. The current Qwen evidence establishes source → formed store → query-conditioned consumer and prospective reuse, not yet a completed state-update cycle.

### [Moderate] Define semantic commitment by causal authority, not generic persistence

**Locations:** `time-emphasis-paper.md:53-65,127-155,212`; `bridge-paper.md:75-84,138-141`.

Every transformer layer installs cache state by architecture. The scientific result is that identity-dependent content becomes independently rescuable and consumer-relevant in L22–27. Define commitment as this measured acquisition of causal authority at a runtime interface. This prevents “commitment” from collapsing into cache write while preserving the explicit statement that weights do not change.

### [Moderate] Clarify the terminal-claim hierarchy

**Locations:** `time-emphasis-paper.md:47,218-226`.

The introduction calls Qwen the primary class anatomy, while the limitations section calls FLUX the only main terminal claim and describes decoder results as bounded mediation. A reader may infer that the Qwen evidence is scientifically secondary. Say directly: Qwen is the primary bounded causal-mechanism result; FLUX is the only threshold-certified instance of the stricter path-distributed subtype. The subtype’s terminal status should remain scoped to its declared endpoint, sites, seeds, and thresholds rather than becoming the sole authority for the broader class.

### [Moderate] Position the scaffold claim against causal abstraction and prompt-specific circuit work

**Locations:** `bridge-paper.md` (no related-work section); `time-emphasis-paper.md:240-246`.

The bridge needs explicit positioning against interventionally grounded causal abstraction and prior distinctions between stable mechanisms and prompt-specific graphs. In particular, cite Geiger et al., *Causal Abstraction* ([arXiv:2301.04709](https://arxiv.org/abs/2301.04709)), and the Circuit Tracing methodology’s context-independent/context-dependent interaction distinction ([Anthropic, 2025](https://www.transformer-circuits.pub/2025/attribution-graphs/methods.html)). The time paper should also make clear that temporal staging itself is not new: Geva, Meng, Agarwal, Cheng, Prompt-to-Prompt, PCI, and DifFRACT already motivate staged or time-sensitive computation. The plausible novelty is the cut-specific source → recipient-formed store → native consumer block/rescue anatomy, isolated store-window/read interventions, and the complete singleton-versus-whole FLUX matrix.

## Quantitative and evidence audit

- **E20 ratios:** correct. Each of the 42 rows uses that row’s actual positive seed gain as denominator before aggregation; the reported 1.577–5.555 range and 3.515 median are supported (`time-emphasis-paper.md:101-115`). Keep the warning that ratios above one are signed causal ratios, not mediation percentages. Put the denominator definition in or immediately under Table 1 as well as in Methods.
- **E20 effects and intervals:** block removal 0.924, independent rescue 0.871, early block 0.934, wrong-state control -0.067, item-bootstrap intervals, identity-cluster intervals, and wrong-identity count 37/42 all match the findings. The read-only E20 verifier passed 6/6 mechanics checks.
- **Formation/store/read panels:** the L0 leak, isolated late K/V write, Qwen/Gemma band sweeps, Qwen-1.5 single-layer read intervention, one-hot subject-row recovery, E18 bucket behavior, and 16/16 context formation/rescue results match the cited findings.
- **FLUX:** the read-only time-signature verifier passed all 15 site/seed cells. Change `0.56200` at `time-emphasis-paper.md:183` to `0.5620` or `0.56201`; the raw maximum is 0.562005440158259. Preserve the corrected deletion wording at line 190: historical carrier-swap deletion is null in 5/5, residual-route deletion in 4/5, and sham deletion in 5/5. Do not restore a generic 5/5 deletion statement.
- **Eye editing:** early/late whole-image scores, call-3 result, and program/register eye-region closure numbers match the artifacts. The interpretation remains target-assisted and collateral-bearing.
- **Bridge measurements:** the Qwen context results, SDXL Q/K/V and grammar results, FLUX program/register values, E1 exact-answer/whole-text values, E2 continuation recovery, Mamba layer effects, and Pythia rescue/control values match their underlying findings. At `bridge-paper.md:104`, label 0.793 explicitly as median recovery of **seeded answer gain**; another E2 summary uses a different normalization, so the denominator prevents a false inconsistency.

## Minor corrections

- `bridge-paper.md:9,18,184` links the companion as `../space-and-time-circuits/paper.md`. If this manuscript is intended to accompany the new focused paper, point those references to `time-emphasis-paper.md`.
- At `bridge-paper.md:158`, avoid defining the dynamic circuit as “small” only in a functional/narrative sense. Use “small” only for a measured supported subgraph relative to a declared comparison graph; otherwise say “selective functional overlay.”
- At `bridge-paper.md:114`, “cannot repair” should remain explicitly bounded to the tested lesion, checkpoint, prompt, call, and native suffix.

## Residual risks after revision

1. **Architecture confounding:** a late cache band may be the easiest generic intervention interface rather than a semantically specialized learned scaffold.
2. **Unresolved internal formation route:** E20 proves a mediated interval and endpoint but leaves intervening writers/edges unidentified.
3. **Static-store/dynamic-read equivalence:** current query-contrast evidence does not choose between a dynamically rewritten semantic record and static stored content with dynamic addressing.
4. **Cross-family lowering freedom:** source/carrier/writer/state/consumer labels can become unfalsifiable if family-specific lowerings are chosen after seeing effects. Prospective frozen lowerings and matched nulls are the needed next evidence.
5. **Single-example visual semantics:** the FLUX strict matrix is strong for the declared assay; the eye example is a useful anatomy case, not evidence for general semantic modularity.

With the major wording and operational-definition changes above, the first paper supports a bounded time-formed causal class centered on Qwen, with FLUX as a strict path-distributed subtype. The bridge supports recurring functional roles and context-dependent consumption as a convergent trend; the learned-scaffold and feedback-loop formulations should remain prospective working inferences.

---

## Final recheck addendum — 2026-10-01

This was a focused read-only recheck of the revised definitions and claim boundaries. It did not repeat the quantitative audit or introduce new experiments.

### Resolved

- **Operational class:** `time-emphasis-paper.md:61` now defines the decoder instance through a genuine source/store dissociation: earlier source change, recipient-formed later record, isolated block, and independent rescue into an unseeded recipient. It explicitly excludes generic execution order, cache append, and pointwise pass-through. This resolves the tautology concern.
- **Commitment:** `time-emphasis-paper.md:63` defines commitment as independently testable causal authority rather than cache persistence and again excludes online weight learning.
- **Formation scope:** `time-emphasis-paper.md:121` now says that E20 identifies a formation interval and causal endpoint while leaving the internal carrier/writer/edge path unresolved.
- **Claim hierarchy:** `time-emphasis-paper.md:224` clearly makes Qwen the primary bounded causal-mechanism result and FLUX the threshold-certified strict subtype; the FLUX certificate is not allowed to govern the decoder result.
- **Strict FLUX reporting:** the table now reports 0.5620 (`time-emphasis-paper.md:185`), preserves partial effects, and retains the correct 5/5 historical versus 4/5 residual-route deletion split. The text also says that the strict matrix identifies support topology and cannot distinguish additivity, redundancy, or re-derivation (`time-emphasis-paper.md:190-200`).
- **Reusable interface versus learned scaffold:** the bridge now supplies an explicit measured/trend/inference/open claim ladder (`bridge-paper.md:43`) and prospective scaffold criteria with frozen role profiles, semantic recurrence, same-parent controls, and matched architecture/depth/energy nulls (`bridge-paper.md:55`). It explicitly says the present record establishes reusable interfaces more directly than a learned scaffold.
- **Lookup alternative:** conventional query-dependent lookup is retained as a possible implementation at `bridge-paper.md:28,163-167`. The same-patch experiment is now correctly limited to query-conditioned causal consumption.
- **Recurrence versus feedback:** family-local recurring responsibilities and carried-state feedback are separated at `bridge-paper.md:57`; E6 is reported as bounded read/write evidence and explicitly not an autonomous semantic loop (`bridge-paper.md:110,153`).
- **Prior-art placement:** both papers now situate the role graph against causal abstraction and Circuit Tracing, and distinguish their empirical decomposition from prior staged-recall, temporal-intervention, and binding accounts.

### Diffusion/class consistency

The revised class language is consistent if the two claims are read at their stated levels. E20 supplies the full source → recipient-formed store → independent rescue identification. FLUX supplies a different family-local temporal case plus a stricter **support-topology** profile at the declared text-stream cut. The manuscript now explicitly says that temporal formation and distribution of causal support require separate evidence (`time-emphasis-paper.md:73`) and that the strict matrix alone establishes path-distributed support rather than its internal formation mechanism (`time-emphasis-paper.md:194-200`). Thus “strict subtype” does not imply that FLUX reproduced E20's K/V mediation assay.

One optional sentence would make this boundary maximally explicit: *FLUX's membership in the broader time-formed account is supported by the separate timing, continuation, and carried-register evidence; the four-quadrant matrix certifies only the strict support subtype.* The existing text already entails this, so I do not treat the omission as a material contradiction.

### Final disposition

**No material unresolved contradiction or newly introduced overclaim was found in the revised passages.** The remaining risks are correctly presented as open empirical questions: full internal formation paths, automatic semantic addressing, prospective scaffold generalization beyond matched nulls, and a complete feedback topology.
