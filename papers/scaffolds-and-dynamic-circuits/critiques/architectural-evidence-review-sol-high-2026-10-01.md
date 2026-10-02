# Architectural evidence review — Sol/high technical reader

Date: 2026-10-01  
Scope: read-only review of the current [architectural paper](../architectural-paper.md), [bridge paper](../bridge-paper.md), [time-formed-circuit paper](../../space-and-time-circuits/time-emphasis-paper.md), and retained experiment artifacts. No model runs were performed.

## Verdict

The evidence base is sufficient for a strong **bounded architecture paper**, but the current draft does not yet contain the strongest completed test of its central scaffold claim. The preregistered Qwen predictive packet was completed after the draft's stated evidence cut. It turns the paper's most important proposed experiment—freezing the one-scene microscopic profile before new contexts—into existing evidence. The result is strong and usefully mixed: complete 24-coordinate profiles recur prospectively, especially for relation and identity, while the simplest shared-site and reader-group prediction fails for color and the weight-row perturbation does not establish the profile's learning origin.

After that packet is integrated, no new experiment is necessary for the paper's defensible central claim:

> In one frozen decoder transformer, a previously selected late state interface is reused across contents and operations; the current question changes the causal authority of identical stored state; an earlier supplied source can cause a recipient to form an independently effective late store; and discovery-frozen microscopic effect profiles predict substantial structure in new lexical/template/order contexts. Diffusion and state-space records supply convergent family-local implementations of source, live operation, writer, carried state, and consumer roles, without establishing one universal graph.

The paper should continue to call the cross-family object a hypothesis or candidate causal abstraction. Repeated semantic mediation through model-produced updates, the learning origin of the exact Qwen map, and a prospectively aligned cross-family graph remain open. Those are extensions, not missing prerequisites for the bounded result.

The draft is currently broader than it needs to be. Its Qwen evidence can carry the paper. Diffusion and Mamba should test the portability of the role vocabulary; compiler and VM results should appear as consequences of exposed interfaces. Treating all four as coequal contributions makes the manuscript read like a workspace inventory and weakens continuity with the first two papers.

## Priority 0: changes required before calling the draft current

### 1. Integrate the completed predictive Qwen confirmation

The draft repeatedly says prospective microscopic recurrence is future work: the last abstract sentence, §§1.2, 2, 6.3, 9, 14, the conclusion, and Appendix B. That is now stale. The source-sealed [preregistration](../../../../saturn/experiments/2026-10-01-scaffold-confirmation/qwen-predictive/PREREGISTRATION.md), [held analysis](../../../../saturn/experiments/2026-10-01-scaffold-confirmation/qwen-predictive/results/qwen-predictive-held-20ede7e6e0c0/analysis.json), [context-level analysis](../../../../saturn/experiments/2026-10-01-scaffold-confirmation/qwen-predictive/results/qwen-predictive-held-20ede7e6e0c0/context-analysis.json), and [post-run verification](../../../../saturn/experiments/2026-10-01-scaffold-confirmation/qwen-predictive/results/qwen-predictive-held-20ede7e6e0c0/postrun-verification.json) are completed artifacts.

The trained-weight panel crosses two unopened lexical sets, two templates, two sentence orders, two queried bindings, and identity/color/relation/size. Context is the replication unit: eight contexts at trained weights, not 128 independent rows or 4,736 independent arms. The frozen complete 24-coordinate discovery profiles have context-aggregated signed cosines of **0.8135 color, 0.9269 identity, and 0.9541 relation**. The matched generic coordinate permutation is only **0.0998, 0.1121, and −0.0850**, and cyclic wrong-operation profiles are **0.4854, 0.7321, and 0.3668**. Raw RMSE is more qualified: mapped beats operation-blind for identity (**0.1559 vs 0.1692**) and relation (**0.0293 vs 0.1496**), while operation-blind slightly beats mapped for color (**0.1372 vs 0.1418**). This is predictive recurrence with an operation-specific advantage strongest for relation, not a universal victory over every comparator.

The coarse predictions are even more informative. Identity's shared-site and reader ordering match all eight contexts; relation matches seven of eight; color matches only one of eight sites and zero of eight reader orderings. Native competence is also heterogeneous: 15/16 color rows, 6/16 identity rows, and 15/16 relation rows at trained weights. The unseen size operation has no competent registered readout and should remain `instrument-unavailable`, not a failed novel-operation prediction.

The deterministic 5% and 20% `v_proj.weight` row permutations do **not** show the predicted degradation on competence-matched contexts. Median mapped cosines remain approximately 0.88→0.90→0.91 for identity, 0.84→0.83→0.83 for color, and 0.955→0.952→0.946 for relation. This makes the perturbation non-diagnostic for learning origin. It should be reported prominently because it rules out using this particular control as evidence that the recurring profile depends on intact trained row organization.

The post-run verifier reports mechanics valid and explains why 4,736 logical lane identities collapse to 4,691 content-addressed lane identities: distinct logical native transactions can share an identical StateCut. The frozen verifier's literal denominator complaint remains visible. The manuscript should report that resolution instead of silently quoting either count as the sole denominator.

Recommended claim replacement:

> A discovery-frozen 24-coordinate late K/V effect profile prospectively recurs across eight new lexical/template/order contexts. Context-aggregated signed profile cosines are 0.813 for color, 0.927 for identity, and 0.954 for relation, well above a matched generic coordinate permutation. Operation-specific mapping improves most clearly for relation and identity; an operation-blind profile slightly improves color raw RMSE. Coarse shared-site and reader rankings replicate for identity and relation but fail for color. The result supports predictive recurrence of a distributed interface while rejecting a single invariant two-site ordering.

This result should follow the one-scene micro-map in §6.3 and become the paper's main transition from exploratory anatomy to prospective scaffold evidence. The current §9 “Predictive within-model scaffold” proposal should be rewritten as completed evidence plus the next unresolved cut, rather than left as an unperformed design.

### 2. Correct the bridge paper's use of historical feedback evidence

The bridge still says the earlier E6 packets establish a carried selector changing a live read and newly written K/V, describes two fresh competent 1.5B contexts plus an incompetent place counterexample, and uses the E6 wrong-site arm to argue about selector specificity. The [causal-mask audit](../../../../saturn/experiments/2026-10-01-scaffold-dynamic-circuits/ar-feedback/corrections/2026-10-01-causal-mask-audit.md) and corrected [routing findings](../../../../saturn/experiments/2026-10-01-qwen-routing-mediation/FINDINGS.md) supersede those interpretations. The old custom attention key lacked its matching causal-mask factory; self-replay could not reveal the shared defect. The 0.5B packet remains unqualified.

Suggested replacement for the E6 paragraph in bridge §3:

> Instrument review found that the earlier 0.5B and exact-policy 1.5B feedback packets registered a custom attention implementation without its matching causal-mask factory. Their multi-token read, appended-K/V, competence, continuation, and wrong-site results are therefore historical records rather than qualified native causal evidence. A corrected Qwen2.5-1.5B BF16 eager rerun registered both functions, matched uninstrumented eager controls, and produced competent green/yellow, spoon/fork, and Madrid/Berlin endpoints on the same three already-open contexts. Restoring the baseline L22 final-query routing row after the L4 selector change attenuated the answer-margin effect by 25.0%, 9.5%, and 40.0%; route-only effects were 50.0%, 14.3%, and 80.0% of the total selector contrasts, with negative factorial interactions. All baseline-route-restored branches retained the changed-selector four-token continuation, and the place arm is tie-sensitive. Newly appended L23 K/V changed, but it is a parallel endpoint of the perturbed query computation; downstream cache block/rescue remains untested. The result establishes a bounded causal route contribution, not a completed semantic feedback loop or fresh held-out generalization.

Bridge §7 should delete the inference from the old E6 layer-0 wrong-site arm. A narrow replacement is: “The corrected factorial shows that one late routing row carries only part of the selector effect; its place restoration arm is tie-sensitive, and other rows, values, layers, and state paths remain live alternatives.” The ledger entry should cite the corrected routing record and audit, and identify all three contexts as already open.

### 3. Reorder the architectural argument around the trilogy's logical progression

The three papers align cleanly if each answers one new question:

1. The time paper establishes **formation**: supplied source → ordered recipient-native formation → committed store → consumer, with FLUX as a strict path-distributed subtype.
2. The bridge establishes **reuse and dynamic participation**: the same stored intervention has different authority under different questions, with family-local source/program/register parallels.
3. The architecture paper should establish **predictive reusable organization**: discovery anatomy predicts held causal profiles, then compare how the role account lowers into other families and what executable consequences follow.

The architecture paper's Qwen spine should therefore be: same-patch/opposite-query effect → E20 formation/commitment → one-scene microscopic map → completed prospective profile panel → corrected route factorial → formation-successor boundaries. Diffusion, Mamba, development, compilation, and runtime then answer whether the same responsibilities recur or become executable elsewhere. The current structure makes the one-scene micro-map sound like the last word and spreads the strongest causal logic across §§5–12.

## Priority 1: strongest underused existing evidence

### Prospective Qwen query-route and color-value program

The [genome attention program](../../../../saturn/experiments/2026-09-09-genome-attention-program/FINDINGS.md) is directly relevant and currently omitted. On Qwen2.5-1.5B-Instruct, an independently selected L22/GQA-group-1 address was frozen before two held banks containing new names, wording, and order. Query-route and assignment-color-value changes move the expected signed margin on all 16 held rows; half query dose is correctly signed on all 16 and opposed dose on 15/16. The query and value changes interact nonadditively, and the combined arm preserves all 16 original first-token answers. The standalone attention program exactly reproduces the selected native attention module and is exercised through the unchanged suffix; the wider seven-panel study reports 704 exact CUDA attention writes and artifact-only CPU replay within 3.91e−5 maximum absolute error.

This gives the paper two things the three-context routing factorial alone cannot: prospective held contexts and an independently extracted query/value computation. It is a different checkpoint variant (`Qwen2.5-1.5B-Instruct` rather than the base specimen) and a single controlled color-retrieval operation. It therefore supports a convergent family-local route/value claim, not continuity of the exact base-model L4→L22→L23 path. One concise subsection is warranted; the 704-row mechanics denominator belongs in methods or the ledger, not the abstract.

### FLUX temporal edit and program × register closure

The architecture draft uses a two-parent conditioner/carrier factorial, but the [scene-editing record](../../../demos/scene-editing.md) is a clearer continuity anchor to both companion papers. In the blue-to-violet example, calls 2+3 visibly reach violet irises while retaining more recipient composition; calls 0+1 move more whole-image distance yet leave the eyes blue. This shows why family-local clock and consumer-aligned observable matter.

At the separate terminating boundary, target current program alone reaches eye-region projection **0.7124**, target incoming scheduler register alone **0.4035**, and their joint installation reproduces native joint RGB exactly. This is a target-corner 2×2 endpoint factorial, not independent mediation or proof of an eye-local wire. It is the most concrete visual statement of “current operation over carried history” and should accompany, rather than be replaced by, the broader two-parent result.

### Repeated FLUX consumption of model-produced image state

The [persistent-object program](../../../../saturn/experiments/2026-09-09-flux-persistent-object-program/FINDINGS.md) is the strongest existing cross-family example for externally clocked repeated feedback. Across three fresh scenes and two fresh seeds, both operation orders execute four edits, and every episode consumes its branch's own previous generated RGB through the native VAE/reference-image path. No oracle image, mask, or external renderer supplies later image state. Final source hashes agree across orders while every final RGB differs, demonstrating trajectory dependence. Discarding source history resets coarse attributes; resetting the image reference changes material and shape details. The bottle-spout failure and its adaptive full-source repair show that sparse semantic operands can omit contextual geometry.

Use this in §11.1 as bounded native recurrent state consumption under a host-supplied operation register. Preserve its limits: the host supplies A/B handles, grammar, requested operations, and register updates; visual review is unblinded; the September 9 record explicitly corrects an overstatement of novelty; and it does not establish autonomous goal/address selection or Qwen-style independently mediated new-cache feedback.

### Existing evidence that is already used enough or should stay peripheral

- The fresh-lease Qwen memory packet is accurately summarized in §12. It establishes exact executable closure across a new lease, not semantic discovery. More prominence would blur the mechanism/systems boundary.
- The prompt-to-new-program result passes 6/6 held arithmetic source programs through a safe host compiler/VM, but its semantic consumer is supplied host machinery. It is useful as an application example, not evidence for an internal neural scaffold.
- Shared-prefix fusion establishes page sharing and compact-kernel mechanics; compact-versus-exact attention-write error remains large (roughly 0.50–0.70 relative L2), so it should not support the semantic architecture claim.
- The corrected Qwen state-transition surrogate is a valuable negative result: exact target V remains sufficient, but the rank-four learned writer fails both held surfaces. It belongs in limitations if cheap Qwen compilation is discussed, not in the positive evidence chain.

## Concrete claim/evidence table

| Proposed paper claim | Best direct evidence | Evidence status | What is still missing |
|---|---|---|---|
| A source can initiate formation of a later independently effective store | [E20 mediation](../../../../saturn/experiments/2026-09-30-full-layer-sweeps/FINDINGS-E20-mediation.md): 42 rows; median block removal 0.924, independent rescue 0.871; wrong identity authors 37/42 | Strong bounded causal result; recipient-formed mediator after an oracle-supplied residual seed | Internal writer path and donor-free source/address synthesis |
| The same late store supports several operations and its authority depends on the question | [Qwen context panel](../../../../saturn/experiments/2026-10-01-qwen-scaffold-context-poc/FINDINGS.md): 64 rows, 32 unique opposite-query pairs, 128 payload-identity checks; medians 3.1305 and 0.5829 nats | Strong same-parent causal reuse | Query-to-address algorithm and broader task families |
| A microscopic scaffold profile predicts new contexts | Completed [predictive held panel](../../../../saturn/experiments/2026-10-01-scaffold-confirmation/qwen-predictive/results/qwen-predictive-held-20ede7e6e0c0/context-analysis.json) | Convergent prospective trend: high full-profile cosine; mixed operation-blind comparison; identity/relation coarse predictions replicate, color does not | Cross-checkpoint transfer and a useful novel-operation readout |
| State-dependent routing causally contributes to the answer | Corrected [three-context routing factorial](../../../../saturn/experiments/2026-10-01-qwen-routing-mediation/FINDINGS.md) plus prospective [genome attention program](../../../../saturn/experiments/2026-09-09-genome-attention-program/FINDINGS.md) | Direct bounded contribution; one open-context base-model panel plus held Instruct-model route/value panel | Full selector path and downstream mediation through the newly written cache |
| Recurring source/live-operation/writer/register responsibilities appear in diffusion | SDXL K/V under live Q; FLUX temporal edit; terminating program × register factorial; two-parent conditioner/carrier cut | Convergent family-local causal evidence with different cuts and observables | One complete independently mediated role graph is not required for the bounded comparative claim |
| Repeated native feedback consumes model-produced state | Native autoregressive token/cache loop; conversation branches; persistent-object RGB loop | Measured externally clocked feedback | Repeated role-specific semantic block/rescue of newly produced state; autonomous controller claims remain out of scope |
| Comparable roles occur in a state-space model | Mamba C/H cuts, ordered transition composition, bounded node-to-carrier compiler | Family-local trend with explicit competence failures | Prospectively aligned common graph; tensor equivalence is neither shown nor needed |
| The exact Qwen organization is learned | Pythia checkpoint trend and shuffle; Qwen predictive weight-dose control | Working developmental inference only; Qwen row-permutation dose is non-diagnostic | A behavior-matched, competence-preserving developmental/control test if the paper wants this as a terminal claim |
| Exposed interfaces support compilation | Complete prompt-source lowering; held in-family SDXL interaction programs; Mamba carrier map; exact extracted Qwen attention program | Several bounded constructive results under different input/consumer contracts | Generic semantic address/payload synthesis and cheap online state-conditioned compilation |
| Model state can be retained and resumed exactly | Durable Qwen VM and fresh-lease joint residual/K/V closure | Strong systems result | Production paging, throughput, and automatic semantic addressing are separate claims |
| One reusable role graph spans model families | Family-local responsibilities plus post-hoc matcher | Working hypothesis; matcher nearly ties depth null | Prospective cross-family alignment only if the manuscript seeks this stronger claim |

## Numerical and protocol fidelity audit

The main numbers presently in the architecture draft agree with their primary records:

- Qwen context: 64 correlated query rows, 128 manifest/digest checks for 32 unique opposite-query pairs, and query-selective medians 3.1305/0.5829 nats.
- E20: median removal 0.924 and recovery 0.871 are signed per-row ratios with distinct numerators; the draft correctly avoids treating them as complementary shares or probabilities.
- Microscopic map: L23/KV0/V and L22/KV1/V recur; across-binding cosines 0.947/0.927/0.961 and cross-operation cosines 0.749/0.336/0.778 are correct; group rescues are nonlinear and one logical binding per operation.
- Formation successor: 8/8 full L11 seeds and 8/8 late blocks are correct; the 37/51 and 18/49 depth-sweep denominators correctly exclude unavailable reads; alias and copying collateral remain visible.
- Corrected routing: the 25.0%/9.5%/40.0% restoration figures, 50.0%/14.3%/80.0% route-only figures, negative interactions, object target-logprob countertrend, and place tie are all accurately stated. BF16 routing should remain distinct from the FP32 context, E20, formation, and head packets.
- Pythia layers `[3,5]`, nonmonotonic trajectory, final fixed-site counterexample, and shuffle incompetence are accurately retained.
- SDXL image-axis projection is correctly defined as a coefficient along the native base-to-target RGB displacement. It should not be described as semantic correctness, cosine, or an eye-only score. The terminating program/register values use an eye-region recipient-to-joint endpoint axis and should remain explicitly distinct.

One wording issue becomes material once the predictive panel is added: “shared value routes have operation-specific weights” remains supported as a discovery description, but the held panel does not validate one invariant two-site/group ranking for color. The stronger, more accurate statement is that **the full distributed profile recurs prospectively while coarse site/group summaries can change by operation and context**.

## What the paper actually still needs

For the bounded paper, it needs synthesis and source updates rather than more gates or model runs:

1. Add a short primary findings document or transparent prose reduction for the predictive packet, because its current authority is spread across large JSON artifacts. Preserve the post-run logical/content-addressed denominator explanation and every countertrend.
2. Promote the completed prospective Qwen panel into the abstract, result table, §6, limitations, conclusion, and evidence ledger; change the evidence-cutoff metadata.
3. Repair the bridge's E6 paragraph and ledger so the trilogy does not contain mutually incompatible feedback claims.
4. Add one visual continuity example (the eye timing plus program/register factorial) and one cross-family repeated-state example (persistent-object RGB loop), each with its supplied-controller limits.
5. Demote VM implementation breadth and unsuccessful/host-consumer compiler branches to consequences, limitations, or appendix. They are useful, but they do not strengthen the central causal scaffold result in proportion to their length.

If the title and conclusion retain only “scaffold instances and a comparative circuit-class hypothesis,” these changes are enough. If the manuscript instead claims a learned universal scaffold, autonomous semantic recurrence, or a complete cross-family role graph, the existing record does not support that stronger claim. The right fix is to keep those as explicit future tests, not to assemble a larger conjunctive certification bundle.
