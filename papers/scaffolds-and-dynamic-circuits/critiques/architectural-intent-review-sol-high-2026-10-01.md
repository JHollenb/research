# Architectural intent review: from formed state to runtime scaffolds

**Reader:** GPT-5.6 Sol, high reasoning  
**Date:** 2026-10-01  
**Drafts read:** `architectural-paper.md`, `time-emphasis-paper.md`, and `bridge-paper.md`  
**Live draft hashes:** architectural `39f0c505...e339`; time-formed `56ccf5b4...fdcd6`; bridge `b41d01ff...a0d3c`  
**Scope:** high-level claim, narrative continuity across the three papers, title/thesis/opening, section order, and evidence centrality. This is a read-only review. I did not edit the manuscripts, re-audit the numerical sources, or run experiments.

## Overall assessment

There is a strong third paper inside the current draft, but the manuscript does not yet present it as the next conceptual step in the sequence. It currently reads as an expanded bridge paper, a new-results dossier, a compiler paper, and a Saturn systems paper combined. The evidence is unusually rich; the abundance hides the architectural realization.

The first paper now gives the reader a durable causal anatomy:

```text
source -> ordered native formation -> committed state -> consumer
```

The bridge gives the next realization:

```text
recurring functional roles + prompt/query/history-specific causal support
```

The third paper should answer a concrete new question: **what executable organization lets a prompt form state, live operations select and use it, and the resulting writes constrain subsequent computation?** Its answer should add one new architectural object:

```text
learned role substrate
        -> prompt- and history-built runtime scaffold instance
        -> current-operation dynamic circuit
        -> native write and causal commitment
        -> updated instance available to later consumers
```

That is the paper's distinctive claim. Frozen weights provide recurring causal affordances. A prompt and execution history instantiate contextual sources, stores, and available bindings within them. A current query or transition activates response-specific support over that state. Native computation writes the result into carried state, where it acquires persistent causal influence for later consumers. This is inference-time formation and commitment. Training learned the reusable substrate; it is not occurring during the runtime cycle.

The current draft contains every piece of this account, especially in §§1, 3, 6, 8, and 11, but it never names **the prompt-built runtime scaffold instance** as the new object. It instead defines a functional scaffold and a dynamic circuit instance, largely repeating the bridge's distinction. Naming the intermediate runtime object is the missing bridge.

## What is genuinely new in the third paper

The new claim is not simply that interfaces are reused or that causal support changes with the question. The bridge already establishes that measured result and frames the scaffold hypothesis. The third paper's contribution is an architectural account of **instantiation, execution, and commitment**:

1. **Instantiation:** a prompt and prior execution form a contextual runtime state inside a learned reusable role organization.
2. **Execution:** the current operation activates a particular causal coalition over that state; identical stored state can have different authority under different questions.
3. **Commitment or hardening:** native writers update carried state so that a transient operation has persistent influence on later computation.
4. **Re-entry:** later operations can consume the updated state, although repeated role-specific semantic mediation through a full loop remains open.

This account turns the first two papers into a model of runtime architecture. The model is two-level:

| Level | What is stable | What is instantiated or changed |
|---|---|---|
| Learned causal substrate | weights, physical modules, and recurring intervention-supported role affordances at one checkpoint | acquired during training; not rewritten by the prompt |
| Runtime scaffold instance | typed contextual sources, formed stores, current bindings, carried state, and available read/write interfaces | built and updated by prompt, query, native execution, and history |
| Dynamic circuit | the response-specific sources, reads, routes, payloads, signs, doses, and timing active for one operation | changes from one operation or state to the next |

The word **hardening** can now do useful work if it is defined once and kept bounded: a transient contextual computation becomes committed state with independently testable, persistent causal influence. It does not mean online weight learning, absolute irreversibility, or that every later intervention has lost authority.

This architectural model is supported in pieces, not as one fully mediated universal loop. Qwen supplies the strongest within-model slice. Diffusion gives the most legible source/live-operation/carried-register lowering. Mamba supplies a different state-transition ABI. The cross-family role graph remains a working abstraction. That evidence status is already present in the draft and should be part of the central thesis rather than scattered through limitations.

## Where the current draft overlaps the first two papers

The overlap is substantial enough that a reader may not know why this is a third paper.

- The title, **Scaffolds and Dynamic Circuits**, is nearly the bridge's title and promises the same paper.
- The abstract leads with the bridge result: fixed late Qwen K/V supports several operations and a byte-identical patch has question-dependent authority.
- §0 says the present paper asks “how such state becomes reusable,” which is exactly the bridge's question.
- §§1–3 repeat the scaffold/dynamic-support definitions, role graph, family-local lowering, reuse-versus-feedback distinction, and execution-axis caveats.
- §§5, 6.1–6.2, 7, 8, and 10 repeat the bridge's principal Qwen, diffusion, Mamba, cross-family, and strict-subtype material.
- §11 repeats the bridge's feedback, Pythia development, and compiler evidence at much greater length.

The inherited results belong here as premises, but they should be compressed into one “what the first two papers established” box or opening table. The third paper should spend its main narrative budget on the new runtime architecture and the newer evidence that resolves it more finely.

The strongest genuinely new or substantially extended evidence is:

- the Qwen microscopic reader map: recurring value coordinates with operation-specific weights and complementary query-head group rescues;
- the native-qualified Qwen routing factorial: one live read has a bounded causal contribution while recipient-live values and other paths remain consequential;
- the expanded formation successors across scene identity, return-value retrieval, literal copying, and aliasing, including the alias failure that locates the next missing binding writer;
- the more explicit compiler and state-retention consequences of treating formed state as an executable runtime object.

These should be identified as extensions of the first two papers, rather than placed beside inherited results with equal narrative status.

## The missing conceptual bridge

The paper currently moves from “functional scaffold” to “dynamic circuit instance.” That leaves an important question unanswered: what exactly has the prompt built before the current dynamic operation acts?

I recommend three explicit terms:

1. **Scaffold schema or learned role substrate:** the reusable causal organization supported by the trained model at a declared resolution.
2. **Runtime scaffold instance:** the context-specific configuration of formed sources, committed stores, carried state, and available bindings produced by the prompt and prior execution.
3. **Dynamic circuit instance:** the causal support active for the current query or transition over that runtime instance.

The native writer changes the runtime instance. A successful write **hardens** a transient computation when the resulting state acquires later causal authority. The next dynamic circuit can then act over the updated instance.

A minimal formalization would make the progression precise without pretending these are separately implemented modules:

\[
I_0 = B_\theta(x),\qquad
D_t = A_\theta(I_t, q_t),\qquad
I_{t+1}=H_\theta(I_t,D_t),\qquad
y_t=C_\theta(I_{t+1},q_t).
\]

Here \(\theta\) is fixed during the inference account; \(B\) forms the initial runtime instance from context, \(A\) identifies the operation-specific causal participation, \(H\) writes or commits new state, and \(C\) is the declared native consumer. The symbols name causal responsibilities, not model-native variables or independent modules.

This bridge also clarifies feedback. Reuse means different operations inhabit the same role organization. Feedback means state produced by one operation causally changes a later read/write. A complete semantic loop requires independent mediation through the newly written state; the current routing experiment changes the answer and appended K/V as parallel endpoints, so the later mediation step remains open.

## Training, inference, host control, and symbol tables

The draft contains the right qualifications, especially in §§1.3, 3, 4.3, and 12, but they arrive after an abstract that combines Pythia development, source compilation, native feedback, and Saturn persistence. The boundaries should be visible in the opening figure and thesis.

### Training and inference

Use a bright-line statement near the opening:

> Training changes the parameters that support recurring causal roles. The main architectural account holds those parameters fixed: prompts and execution history form runtime state, current operations select dynamic support, and native writers commit updated state. Developmental checkpoint evidence concerns how the substrate was acquired; it is not part of the inference-time hardening cycle.

This prevents “prompt-built scaffold” and “hardening” from sounding like prompt-time weight construction. Pythia can then remain useful developmental evidence without governing the architecture narrative.

### Native model and host runtime

The native model computes conditioner products, residuals, K/V, recurrent state, attention, denoiser output, logits, and images. The host supplies prompts, clocks, sampling policy, branch selection, intervention sites, persistence, and transaction semantics. Saturn exposes and manipulates the architecture; it does not prove that the model internally implements Saturn's VM concepts.

The current §4.3 table is excellent source material. Move a compressed version into the first two sections, because “program,” “compiler,” “writer,” “ABI,” “commit,” and “VM” otherwise accumulate a model-internal meaning the evidence does not establish.

### Observer coordinates and native symbols

The paper should say early and directly:

> Source rows, token spans, head groups, semantic factor labels, role names, and VM fields are experimenter coordinates grounded to varying degrees by native-consumer interventions. They are not evidence that the model owns a portable native symbol table.

This is especially important for the scene compiler and Mamba node-to-carrier work. A host can supply semantic row alignment, factor labels, or a source address and still demonstrate a real causal interface. The resulting claim is executable intervention at that interface, not automatic semantic naming or native address discovery.

## Recommended title, thesis, and opening

The current title is too close to the bridge and does not name the third paper's new object. My preferred title is:

> **From Formed State to Runtime Architecture**  
> *Prompt-Built Scaffold Instances, Dynamic Circuits, and Causal Commitment*

Two shorter alternatives are:

- **Prompt-Built Runtime Scaffolds in Generative Models**
- **Runtime Scaffolds: Dynamic Computation and Causal Commitment in Generative Models**

I would avoid making “predictive source compilation” the subtitle's main promise. It is a valuable consequence and partially separate contribution, while the paper's conceptual payoff is the runtime architecture.

### Proposed thesis paragraph

> The first paper showed that a circuit may have to be formed before it can be read. The second showed that recurring causal roles can support different response-specific circuits. This paper asks what runtime architecture those facts imply. We propose that frozen generative models provide a learned scaffold schema that prompts and execution history instantiate into causal state. A current query or transition activates a dynamic circuit over that instance; native writers commit the result into carried state that later consumers can use. This inference-time commitment is hardening of state, not a weight update. The role names and addresses in our assays are intervention-grounded observer coordinates, not evidence of a model-native symbol table.

### Proposed evidence paragraph

> Qwen supplies the most complete bounded slice. An upstream supplied residual causes recipient-native formation of a late store; the same late interface supports several operations and has question-dependent authority; two recurring value coordinates and complementary reader groups receive different weights by operation; and a native-qualified routing intervention shows that one live read contributes causally without exhausting the selector effect. Diffusion separates a prompt-derived source, live state-dependent binding, and a carried image register. Mamba supplies a distinct transition-state lowering. Together these results support prompt-built runtime scaffold instances with response-specific execution, while complete semantic addressing, repeated mediated feedback, and a universal cross-family graph remain open.

This opening makes the paper intelligible before any metric. The abstract can then keep only the two or three most diagnostic numbers: the Qwen block/rescue result, one same-patch query-selectivity result, and perhaps one microscopic-reader or routing result. The current abstract's routing percentages, multiple compiler classes, Pythia trend, Saturn persistence, and Mamba synthesis make it read as an evidence ledger.

## Recommended section order

### 1. From formed state to runtime architecture

Open with the three-paper progression, the schema/instance/dynamic-circuit distinction, one architecture figure, and the bounded claim ladder. Define hardening here. State that weights are frozen in the runtime account.

The figure should distinguish three boundaries visually:

```text
learned weights / role substrate
          |
prompt + prior history -> runtime scaffold instance I_t
                              |
current query/transition -> dynamic circuit D_t
                              |
native writer ----------> committed instance I_(t+1) -> consumer

host: supplies prompt, clock, intervention, sampling, persistence
observer: names roles and coordinates; native symbol table not established
```

### 2. What is measured, inferred, and supplied

Bring forward the best parts of current §§1.2–1.3, 3, and 4.3. Define causal runtime architecture versus physical module graph and external systems runtime. State the evidence ladder:

- measured within-model slice;
- convergent family-local lowerings;
- architectural inference about prompt-built instances;
- open native addressing, repeated feedback, learning origin, and universal graph.

Put detailed normalization, bootstrap, and selection-history contracts in an appendix.

### 3. Qwen: a bounded runtime scaffold instance

Make Qwen the paper's causal spine and organize the evidence by the architecture, not by experiment chronology:

1. **Formation and commitment:** inherit E20 briefly; source causes recipient-native late state with independent block/rescue.
2. **Dynamic use:** inherit the same-patch/opposite-question result briefly.
3. **Recurring readers, operation-specific participation:** lead with the two value coordinates and complementary reader groups. This is the clearest new refinement.
4. **Live routing and partial update:** present the corrected routing factorial as evidence for a causal current-operation contribution. State beside it that appended K/V is not yet a downstream mediator.
5. **Binding boundary:** use scene/retrieval/copy/alias successors to show where the architecture transfers and where source-anchor state is insufficient.

One composite diagram should mark which arrows each experiment supports. This would be more memorable than treating all packets as coequal subsections.

### 4. Family-local lowerings of the same runtime responsibilities

Use diffusion first because it makes the source/live-read/carried-register distinction visible. Restore the iconic eye rewind near the start of this section: the same target-derived complete contextual text stream installed early changes composition, while installation late changes iris color with more composition retained. This is a memorable picture of current operation over carried history. Label it before the image as target-assisted whole-stream transport with collateral, so it cannot be read as a permanent eye-color wire. Retain:

- fixed prompt-derived K/V with live latent-dependent Q;
- early versus late persistent influence as bounded hardening;
- program × carried-register factorial as joint authority, not mediation.

Then give Mamba one concise subsection on convolution/recurrent state and ordered transition composition. End with the existing cross-family role table, revised to include **runtime instance**, **dynamic operation**, and **commitment evidence** columns. State that comparable responsibilities are the inference; identical tensors and a unique graph are outside scope.

### 5. Executable consequences

Separate scientific architecture from engineering consequences:

1. A complete native prompt source can be sealed and replayed before the outcome.
2. Some development-fitted interaction programs predict held in-family payloads.
3. External systems can persist, branch, edit, and resume formed state through native consumers.

These results show that the interfaces are executable. They do not show that the model possesses the host compiler, VM, commit policy, semantic factor labels, or symbol table. Keep this section short enough that the paper remains about model architecture.

### 6. Boundaries and discriminating predictions

Combine current §§9, 10, and 14. Lead with the already known limits: fine Qwen map covers one scene/order; routing uses three opened contexts; newly appended state lacks downstream mediation; diffusion relation support can be broad and collateral; Mamba competence is sparse; cross-family matching is post-hoc and near a depth null.

Then give the minimum next cuts: prospective Qwen reader prediction, later binding writer, repeated semantic state mediation, crossed-state diffusion writer, and developmental origin. These are predictions of the architecture, not prerequisites for retaining current bounded results.

### 7. Relation to prior work and conclusion

Keep the current careful novelty boundaries. End on the architectural realization: learned substrate, prompt-built instance, dynamic operation, committed update, later consumer.

## Evidence centrality

| Evidence | Main text role | Recommended placement |
|---|---|---|
| Qwen E20 source → recipient-formed store → consumer | Foundation inherited from paper one; establishes formation and commitment | Main text, one concise subsection; full ratios and bootstrap detail in appendix/reference |
| Same-patch/opposite-query Qwen | Foundation inherited from bridge; establishes dynamic consumption | Main text, concise |
| Qwen microscopic reader map | Strongest new refinement: reused store coordinates with operation-specific weighting and group-level causal reads | Central main text, likely primary new figure |
| Native-qualified Qwen routing factorial | Strong new evidence for live operation/read contribution; other routes remain | Central main text with three-row table; instrument-audit detail in appendix |
| Scene/retrieval/copy/alias formation successors | Breadth and a useful binding failure | Main text as one compact boundary table; individual packets in appendix |
| Qwen window topology | Shows a role need not have one microscopic support topology | One paragraph or appendix; already developed in paper one |
| SDXL fixed source/live Q and program × register | Best cross-family illustration of runtime instance plus dynamic operation | Main text |
| FLUX early/late eye rewind | Iconic illustration that timing and carried history change what a complete contextual source can do; rules against a permanent eye wire interpretation | Main text figure, explicitly target-assisted and whole-stream |
| FLUX ontology/grammar and prospective site/time panels | Additional recurrence and support evidence | Condense to one paragraph; detailed profiles in appendix because bridge already carries the concept |
| Mamba C/H roles and transition composition | Distinct family-local state ABI and ordered execution | Compact main-text comparison |
| Mamba carrier compiler | Bounded compiler consequence with high-dimensional fit and limited generalization | Appendix or a compiler companion section, not architectural spine |
| Pythia checkpoint development | Evidence about acquisition during training | Appendix or discussion box; keep separate from inference architecture |
| Complete prompt-source compiler | Clear executability consequence; mostly native conditioner capture rather than learned replacement | Short main-text consequence; coverage tables in appendix |
| Compact SDXL interaction programs | Strong bounded prospective payload result, scientifically distinct | Short consequence section or separate compiler paper; detailed panels in appendix |
| SDXL live resolver and offline writer predictors | Future state-adaptive compilation boundary | Appendix/discussion unless the title promises compilation |
| Native conversation and scratchpad handoff | Ordinary/model-produced state affects later computation; role-specific loop still open | Appendix or feedback-boundary paragraph |
| Durable VM, fresh-lease memory, debugger, paging, scene VM | Systems evidence that state can be externalized and executed | Appendix or separate systems paper; one main-text implication paragraph |
| Tool catalogue, execution counts, VRAM/time, evidence ledger | Reproducibility and custody | Appendix only |
| Detailed formulas, bootstrap mechanics, selection histories | Necessary methods | Methods appendix; retain compact claim-relevant statements in main text |

## Specific narrative risks to fix

1. **“Architecture” currently names three things:** physical model architecture, causal role abstraction, and Saturn execution/runtime architecture. Define “causal runtime architecture” early and keep the other two explicitly qualified.
2. **“Scaffold instance” is currently underspecified.** The paper defines dynamic circuit instance but never names the contextual object the prompt built and later operations modify.
3. **“Compilation” currently ranges from running the native conditioner to predicting held payloads to serializing state.** These are different claims. Use `native source lowering`, `predictive payload compilation`, and `state persistence` as separate terms.
4. **“Feedback” can sound autonomous.** Keep “externally clocked native feedback” and distinguish it from model-selected goals, clocks, addresses, or commit policy.
5. **“Hardening” is absent from the current architectural vocabulary.** Add it as a plain-language alias for measured runtime commitment and keep the first paper's definition.
6. **The abstract overweights breadth.** It lists Qwen microscopic details, routing percentages, diffusion, Mamba, Pythia, compilers, and Saturn before the reader knows the architectural claim.
7. **The tool/VM material can reverse the evidence direction.** Saturn's names and transactions make state experimentally executable; they do not establish that the model internally organizes itself according to the host's schema.
8. **The cross-family role table can be mistaken for a discovered universal graph.** Add an evidence-status column or mark each cell as independently mediated, intervention-supported, observational, or host-supplied.

## Prioritized recommendations

1. **Retitle and rewrite the opening around the new object:** a prompt- and history-built runtime scaffold instance within a learned causal role substrate.
2. **Make instantiation → dynamic operation → hardening → later consumption the paper's section-level spine.** This is the architectural advance beyond the first two papers.
3. **State the training/inference and native/host boundaries in the first page.** Fixed weights support the runtime cycle; Pythia concerns acquisition; Saturn supplies control and persistence.
4. **State that role names and addresses are observer coordinates, not a native symbol table.** Repeat this beside compiler and VM claims.
5. **Use Qwen as one integrated causal slice.** Inherited formation and query-selectivity establish the base; the microscopic reader map and native routing factorial are the new central results; aliasing supplies the boundary.
6. **Use diffusion and Mamba as compact family-local lowerings.** Preserve their strongest causal contrasts and move the inventory of panels to appendices.
7. **Use the eye rewind as the visual intuition for current operation over carried history.** Qualify it as target-assisted whole-stream transport with collateral, rather than a permanent eye wire.
8. **Treat compilation and state virtualization as executable consequences.** Keep one clear section in the paper; move detailed compiler, memory, debugger, timing, and tool evidence out of the narrative spine.
9. **Move developmental Pythia and most methods/accounting detail to appendices.** They matter, but they currently blur training with inference and architecture with evidence custody.
10. **End with the bounded architectural claim:** models exhibit reusable causal roles, prompt-built contextual instances, response-specific dynamic computation, and runtime commitment; complete native addressing, repeated semantic feedback, learning origin, and a universal cross-family graph remain open.

The architectural draft does not need new experiments to become a compelling third paper. It needs a stronger object hierarchy and a more selective evidence hierarchy. Once the learned substrate, prompt-built runtime instance, dynamic operation, and committed update are made explicit, the existing evidence reads as a coherent architecture rather than a collection of successful interventions and systems demonstrations.

## Addendum: completed prospective Qwen microscopic confirmation

The evidence hierarchy above needs one material update. The “predictive within-model scaffold” experiment currently listed as future work in the architectural paper has already been completed under a frozen preregistration. The retained sources are `saturn/experiments/2026-10-01-scaffold-confirmation/qwen-predictive/PREREGISTRATION.md` and `results/qwen-predictive-held-20ede7e6e0c0/context-analysis.json`.

Across eight unopened context clusters, the frozen full 24-coordinate signed reader profiles recur prospectively with pooled signed cosine **0.8135 for color, 0.9269 for identity, and 0.9541 for relation**. The matched generic coordinate permutation gives **0.0998, 0.1121, and −0.0850**, respectively. This is existing third-paper evidence for predictive distributed organization at the declared late Qwen interface, not merely a proposed next test.

The result also sharpens the correct claim. The full distributed profile transfers much better than the coarse two-site summary: color satisfies the frozen coarse two-site ordering in only **1/8** contexts and the GQA group ordering in **0/8**, while identity satisfies its ordering in **8/8** and relation in **7/8**. The paper should therefore lead with prospective recurrence of the complete distributed profile and treat the two highlighted value sites and reader-group orderings as operation-dependent summaries, not as the scaffold itself or a universal micrograph.

The deterministic 5% and 20% value-projection row perturbations do not show the expected degradation of profile recurrence on competence-matched rows. This panel therefore does not establish the learning origin of the organization. Developmental origin remains open and should stay separate from the positive prospective inference-time result.

This update changes evidence centrality, not the proposed conceptual reframe. The prompt-built **runtime scaffold instance** remains the missing third-paper object. The completed panel strengthens the learned-substrate side by showing that a frozen distributed reader organization predicts new contexts. Full native successor mediation remains missing: the newer routing assay changes the current answer and newly appended state, but the appended state has not yet been independently blocked and rescued before a later native operation. The trilogy can therefore make a stronger existing claim about predictive distributed reuse while retaining commitment, later consumption, and complete semantic feedback as distinct evidence levels.
