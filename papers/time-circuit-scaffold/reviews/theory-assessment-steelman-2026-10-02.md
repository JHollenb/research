---
title: "Theory assessment (steelman, then attack): dynamic circuits on a stable time scaffold"
type: assessment
date: 2026-10-02
reviewer: "Opus 5.5 (claude-opus-5-5), second theory assessment at the author's request"
method: "Read-only. No models run. Read the original theory documents, the tool documents, the living theory, the two formal-math reviews and the first assessment, then spot-checked the primaries named below. Labels: MEASURED = read in a primary FINDINGS/README/report file named inline; INFERRED = my reasoning; PRIOR = my recollection of the literature, to be verified before citation."
sources:
  - research/papers/scaffolds-and-dynamic-circuits/architectural-paper.md
  - research/papers/scaffolds-and-dynamic-circuits/bridge-paper.md
  - research/papers/scaffolds-and-dynamic-circuits/outline.md
  - obsidian/blog/2026-10-01-125322-stable-scaffolds-and-dynamic-circuits.md
  - obsidian/blog/2026-10-01-193730-time-formed-scaffolds-in-qwen-flux-and-mamba.md
  - obsidian/blog/2026-10-01-131907-saturn-vm-model-virtual-memory-evidence-checklist.md
  - obsidian/blog/2026-10-01-134012-open-question-reusable-model-programs.md
  - obsidian/blog/2026-09-24-200745-a-model-virtual-memory-with-addresses-authority-and-local-time.md
  - obsidian/blog/2026-09-29-115301-model-virtual-memory-from-a-request-to-a-native-answer.md
  - obsidian/blog/2026-10-02-115541-the-time-scaffold-architecture-living-theory.md
  - saturn/docs/CAUSAL-CONTEXT-VM.md
  - saturn/docs/MODEL-OS-KERNEL.md
  - saturn/docs/VM-CACHE-PLANES.md
  - saturn/docs/SATURN-DEBUGGER.md
  - saturn/docs/SPECTRAL-ADDRESS-ABI.md
  - saturn/docs/SPECTRAL-SCENE-VM.md
  - saturn/docs/QWEN-VIRTUAL-CONTEXT.md
  - research/papers/time-circuit-scaffold/reviews/architecture-math-2026-10-02.md
  - research/papers/time-circuit-scaffold/reviews/dynamic-circuits-theory-2026-10-02.md
  - research/papers/time-circuit-scaffold/reviews/theory-assessment-opus-2026-10-02.md
  - saturn/experiments/2026-10-02-fixed-lowering-iia/FINDINGS.md
  - saturn/experiments/2026-10-02-attention-band-locator/FINDINGS.md
  - saturn/experiments/2026-10-02-blind-scaffold-prediction/FINDINGS.md
  - saturn/experiments/2026-10-02-e20-cross-family/FINDINGS.md
  - saturn/experiments/2026-10-02-qwen-variant-circuits/FINDINGS.md
  - saturn/experiments/2026-10-02-qwen-address-symbol-table/FINDINGS.md
  - saturn/experiments/2026-10-02-residual-program-v2/FINDINGS_qwen15it.md
  - saturn/experiments/2026-10-02-pass-indexed-baseline/FINDINGS.md
  - saturn/experiments/2026-10-02-routing-readout-correction/FINDINGS.md
  - saturn/experiments/2026-10-02-mamba-clock-retest/FINDINGS.md
  - saturn/experiments/2026-10-02-sdxl-relation-lockin/FINDINGS.md
  - saturn/experiments/2026-10-02-circuit-measurement-trial/FINDINGS.md
  - saturn/experiments/2026-10-02-commit-null/PREREG.md
  - saturn/experiments/2026-09-06-qwen-recursive-multipage-native-free-rosetta/FINDINGS.md
  - saturn/experiments/2026-09-24-spectral-virtual-context/FINDINGS.md
  - saturn/experiments/2026-08-13-semantic-program-payload/README.md
  - saturn/experiments/2026-09-30-isolated-swap-reruns/FINDINGS.md
tags: [assessment, theory, interpretability, time-scaffold, dynamic-circuits, steelman]
---

# Theory assessment: steelman, then attack

## 0. Bottom line

The theory has a real, defensible core, but the sentence currently used as its headline ("dynamic circuits loop through a stable time scaffold"; "a fixed machine runs a different program for each input") is not that core. That sentence is true of every deterministic stateful network by construction, and most of the formal apparatus built under it (conditional linearity, the single-read lemma, the K×V identity, complete-state closure, static-K/V-dynamic-Q in diffusion, the Mamba unrolled recurrence) is softmax and recurrence algebra that holds whether or not the theory is right. The core that is *not* true by construction is narrower and sharper: **trained networks factor into a small, fixed, findable store/read interface that later computation reads by address, and an input-dependent routing program that is itself computed from carried state; the interface is shared across inputs and operations, survives heavy continued training, and is sufficient as partial state.** That is a store/router factorization claim, and it is falsifiable. Today it is measured for one task family (in-context entity-attribute readout) in decoder transformers up to 7B, with good causal hygiene, and is untested on the operation classes that would make it an architecture theory rather than a better-instrumented Geva et al. extraction stage.

I also found that four of the eight "tool" tests the living theory lists as discriminating either test something other than what the commitment states or are guaranteed by construction (§5). Fixing those is cheap and matters, because the "run the model as software" claim currently borrows credibility from them.

Verdict: a theory-level headline is achievable, not yet earned. It should be the store/router factorization (§9), not the time-scaffold slogan, and it needs one decisive cross-operation test before it is headlined (§8.3). If that test fails, the first assessment's narrowing is correct; if it passes, the narrowing would undersell the work.

## 1. How to read this document

Every number below was read in the file named next to it. Where the living theory, a paper and a primary disagree, the primary wins. I did not rerun anything. The living theory's commitments are numbered C1–C8, and so are the paper's campaign results (C5 route attribution, C7 common graph, C8 native continuation). They are different objects; in this document C1–C8 always means the living-theory commitments, and I write "paper-C7" for the campaign.

## 2. Steelman (Q1)

### 2.1 The theory in its strongest form

I state it the way I think the author means it, using his own documents and tightening each clause to its most defensible precise version.

**T1. Interpreter and program.** For a trained model m, there is a fixed role lowering (L_m, π_m): a map from a small role set {source, address/reader, writer/commit, carried state, consumer} to execution-time sites (depth × position in an AR transformer; denoising call in diffusion; layer × step in an SSM). The lowering is fixed across inputs and operations, in the causal-abstraction sense: interchange interventions at L_m(r) commute with the high-level role machine at high IIA over a broad context × operation set (architecture-math §1.3). The per-input part is the **routing signature** Γ(c,t) — attention distributions, gate values, normalisation gains — plus realized payloads, doses and timing (dynamic-circuits-theory §0, §2.4).

**T2. Content moves linearly; computation is routing.** Given Γ, payloads propagate affinely to a model-internal pre-readout boundary; every non-additive effect (binding, relation, K×V conjunction) is mediated by a change of Γ, and Γ is a function of carried state (dynamic-circuits-theory §2.3, conditional linearity). Pointer-following therefore requires the query to have been written by an earlier read (single-read lemma, §3.2). Carried state is simultaneously the store and the input to the next routing decision: this is the "loop".

**T3. Time is the organizing axis.** Content is formed over ordered execution, committed into a store at a findable interface, and read later by a query that addresses it. Authority is time-indexed: what is committed early constrains what later sources can change (monotone loss of reachability, dynamic-circuits-theory §5.1, §5.5). The correct counterfactual baseline is therefore pass-indexed: the native at the current pass, not a fixed parent (living theory C6).

**T4. Run the model as software.** Because the interpreter is fixed and execution state is complete (architecture-math §2, complete-state theorem), a model execution is a process: states can be snapshotted (StateCut), forked, rewound, replayed, paged, and a program can be installed at the interface. The strong, non-trivial form of this claim is not "replay is exact" (that is determinism). It is: **partial state at the interface is sufficient for the consumer**, so the store can be paged, transplanted and compiled independently of the rest of the execution, and the per-input program can be installed or cached at fixed sites (architecture-math §2: "a narrow late K/V band is not sufficient by construction... ε-sufficiency of a narrow learned band is an empirical property of trained weights").

**T5. Learned and conserved.** The interface is a property of the trained weights (v_proj row permutation collapses the profile), and it is conserved under continued training while the code written into it drifts (living theory C7).

**T6. Family-general.** The same role machine lowers into transformers (K/V store, query read), diffusion (prompt K/V source, latent register, scheduler) and SSMs (conv/recurrent state, write vs retention), with different physical lowerings and no canonical graph.

### 2.2 What this would explain that standard framings do not

| Standard framing | What it gives | What the steelman adds, if true |
|---|---|---|
| Circuits (Elhage 2021; Wang 2022; Conmy 2023) [PRIOR] | Per-task subgraphs of heads/MLPs | One interface hosts many tasks with operation-specific weights over the same coordinates (Qwen L23/KV0/V and L22/KV1/V, cross-operation cosines 0.336–0.778; architectural-paper §6.3), and the location of that interface is predictable from one forward pass. A circuit catalogue would not predict that the next task reuses the same sites. |
| Features / SAEs / transcoders | A representational basis, mostly in the residual and MLP | The operative store for in-context readout lives in attention K/V at a position, which an MLP-feature graph misses: matched transcoder feature+error interchange moves identity 0.31 against 0.94 for a native K/V cut (first assessment P1, citing Paper 1 §5, Gemma, n=12). |
| Causal abstraction / DAS (Geiger 2021, 2023; Wu 2023) | The test (IIA) and learned alignments | A specific high-level model to align, with the claim that a single fixed alignment reaches the per-input ceiling. Causal abstraction says how to test a role graph; it does not supply one. |
| Key-value memories (Geva 2021) | FFN layers as key→value memories for parametric facts | A different memory: the attention K/V at the subject position in a late band, formed before the band and read by address. It says which KV memory the answer actually consumes in context. |
| Residual stream as channel (Elhage 2021) | Within-pass communication, Q/K/V-composition | The time axis across positions and passes: formation → commit → later read; history dependence of stored state (Mount ≠ Prefill); the pass-indexed native as the only valid baseline. |
| Causal tracing / ROME (Meng 2022) | A "late site" of attention at the last token, mid-layer MLPs at the subject | An independent unseeded-recipient rescue: the band formed by a seeded recipient, transplanted into a recipient that never saw the seed, authors the answer (rescue 0.871; wrong-identity band authors wrong identity 37/42; architectural-paper §6.2). Tracing shows restoration in the same run; this shows the formed band is a portable object. |

The software clause adds a further prediction that no rival framing makes: if partial state at the interface is sufficient, then interpretability findings convert directly into systems operations (page the store, cache the static source, recompute only routing), and those operations should work *only* at the located interface. That is the strongest version of "run the model as software", and it is testable (§8.4).

## 3. Is it correct? Commitment by commitment (Q2)

One fact frames the whole table. The living theory's changelog shows the commitments C1–C8 were added at 13:45 on 2026-10-02, after every result they cite had landed (IIA, locator, variants, pass-indexed baseline, residual v2; MEASURED, living-theory changelog). All eight "Holds" verdicts are therefore retrodictions. That does not make them wrong, but none of them is yet a prospective success of the commitment as written.

| # | Commitment | Verdict | Strongest support (MEASURED) | Strongest counter-evidence (MEASURED unless marked) |
|---|---|---|---|---|
| C1 | One fixed role mapping serves all inputs of an operation | **Partially supported** | Fixed/ceiling 0.87 [0.74, 1.00] Qwen2.5-1.5B and 1.00 Gemma-2-2B, wrong-role floor 0.00 (fixed-lowering-iia FINDINGS). Frozen 24-coordinate relation profile beats three competitors in 8/8 held contexts, RMSE .029 vs .149 (architectural-paper §6.7). | The "per-input ceiling" is the best of six overlapping candidate bands chosen by log P(counterfactual); on Gemma fixed = ceiling = ceiling(any) exactly, so the rival had no room to win (fixed-lowering-iia table). Absolute IIA 0.31–0.76 fails its own 0.75 bar; position admitted 0 rows; held `size` n=4. At microscopic resolution the fixed map fails for color (reader-order prediction 0/8, blind profile has lower raw error) and competent identity (0/4 wins) (architectural-paper §6.7). Fixed at band resolution, not at head resolution, for two of three operations. |
| C2 | The scaffold can be located from native reads alone | **Partially supported** | Blind locator: Phi-2 6/6, OLMo-2 5/6; on Phi-2 locator-band block 0.515 vs depth-band 0.065 (attention-band-locator FINDINGS). Depth-fraction rule failed blind on Pythia (block −0.28 at predicted band; blind-scaffold-prediction FINDINGS). | n = 2 blind models. Locator bands are wide relative to single-layer true bands: IoU locator-vs-true 0.125 (Phi-2, 8-layer band around L23) and 0.25 (OLMo-2). Rule C was chosen among three on Phase A. Gemma (known) is biased ~3 layers early, locator IoU 0.364 < depth 0.444. The statistic Σ_h α(final→subject)·‖v·W_O‖ is Geva's attribute-extraction locus made fit-free [PRIOR]. Qwen2.5-7B deferred. |
| C3 | Content is formed, committed into a store at a band, and read from there | **Supported for one task family; scope-limited** | E20 block/rescue in six decoder families plus 7B: Qwen 0.924/0.871 (n=42), held-out Qwen 0.728/0.713 (n=79), Gemma 0.768/0.985, SmolLM2 0.740/0.910 (e20-cross-family FINDINGS); OLMo-2 0.972/0.903, Phi-2 0.515/0.892 (locator FINDINGS). Band freeze leaves rescue 0.904/1.023; cutting answer→subject read 0.871→0.010 (architecture-math §3.2). | All AR cells use one templated in-context readout where the answer token is in the context (first assessment §0.2, run_sae_comparison.py:115). The prereg's own "band builds the store" prediction (P2a) failed; the theory was revised to "formed before, committed at" (architecture-math §3.2). Qwen2.5-7B block 0.595. "Distributed commit" fails on OLMo-2 (L13 carries 0.894 of 0.903). Paper-campaign Pythia acquisition: matched-depth L2 control stronger than the selected L3 lowering at every checkpoint (architectural-paper §11.2). The two tools cited for C3 do not test it (§5). |
| C4 | Participation is query-gated | **Supported, but predicted by any attention retrieval** | Byte-identical patch, only the question changes: 3.130 nats color 16/16, 0.583 position 16/16, 128 digest checks (architectural-paper §6.1). Symbol table T4: 2.66 vs 0.044 nats, 36/36 (qwen-address-symbol-table FINDINGS). | Not a counter-trend but a discrimination failure: a reader that attends to the queried attribute's span predicts exactly this. The rival the math names ("steering vector, ∂A/∂q = 0", architecture-math §5) is not a live rival for an attention model. |
| C5 | Address and payload are separate: K addresses, V carries value; the residual carries pointers | **Partially supported; half is architectural** | Instruct v2 (46 competent organisms): V-only 0.89 = K+V 0.89, K-only 0.0; alias residual seed recovers value 0.0 (residual-program-v2 FINDINGS_qwen15it). SDXL K×V interaction +0.3413 (architecture-math §4). | "V carries the payload" is the definition of softmax attention (o = Σ α_j v_j); the falsifier "V-only swaps fail to move content" cannot fire in a working attention read. "K addresses" has never been exercised in AR: T2a K-only swap is inert (0.087 nat, attention shift 0.019) because decided reads have address gain α(1−α) → 0, and the clean pre-RoPE joint swap was not run (symbol-table FINDINGS; P3 ratio 0.80 "confounded"). T3a "binding-changing K+V mis-binds" failed (14/14 transfer). The pointer/value split is the live, non-trivial half, and it has prior art (binding IDs, lookback) [PRIOR]. |
| C6 | State is history-formed; own outputs reshape later formation | **Supported but unfalsifiable as stated** | Joint vs independently formed pages 6/6 vs 1/6 (VM checklist, book-index experiment). Pass-indexed drift median +2.54 nats; answer-content increment +2.25 over a format-matched control; fixed parent flips 11/12 conclusions (pass-indexed-baseline FINDINGS). | The breaking outcomes ("Mount(A,B) = Prefill(A‖B)"; "earlier turns leave the baseline unchanged") are impossible in any causal transformer whose later tokens attend earlier ones, except in degenerate cases. The same FINDINGS shows later reads are dominated by the fact span, not the model's answers: donor-answer patch flips 0/4, fact-span patch 1.678 vs answer patch 0.285–0.429 nats. Independent-chunk KV mismatch is known in systems work (Prompt Cache, CacheBlend) [PRIOR]. |
| C7 | The scaffold survives training; the code changes | **Partially supported; falsifier half-fired and was reinterpreted** | Locator bimodal (L21–23, L27) in all six Qwen2.5-1.5B variants, 5/6 peak at L27; math CKA 0.72 in band vs 0.41 mid; base→coder 0.92 (qwen-variant-circuits FINDINGS). | The stated falsifier includes "destroys its shared coordinates". Math→base transplant is 0.05 and coder→base 0.34 (variants FINDINGS). One direction of the shared code is essentially destroyed; the commitment survived by being restated as "asymmetric code" after the data. One lineage, same initialization; late-layer CKA convergence may be generic output convergence (first assessment P5). E20 block/rescue at each variant's own band and the dynamic half are "frozen, not run". |
| C8 | The loaded object is a program, not a direction | **Unsupported by the evidence cited; weakly supported elsewhere** | Evidence that does bear on it: SDXL aligned rank-3 interaction program, held response cosine 0.9475, wrong-pair MAE 88.83, wrong-sign 58.07; mean-alone and centered-alone fail while their sum works (architectural-paper §11.4). Query selectivity (C4) is also an argument against "a direction". | The cited XOR/XNOR result does not test the model's scaffold: the XOR is applied by a host-side tensor-free IR, carriers are decoded by recipient-local ridge decoders mostly at the embedding or layer-0 boundary, and the result is written through the frozen head (semantic-program-payload README). The inverted XNOR "executing its own semantics" 74/75 is therefore guaranteed by the host computing XNOR. Wrong-source scene renders are guaranteed because diffusion source sufficiency is architectural (architecture-math §2). The SDXL compiler captures 5.86% (K) and 7.69% (V) of held interaction energy on an unseen factor family and does not beat the development mean (architectural-paper §11.4). |

**Net reading of correctness (INFERRED).** At band resolution, for in-context entity-attribute readout in decoder transformers from 1B to 7B, the formation → commit → addressed-read decomposition is well supported, with unusually careful causal design. "One fixed mapping" holds against a weak rival. Everything that would make the theory an *architecture* theory — the same interface across operation classes, a prediction of the dynamic part, cross-family content beyond the role vocabulary — is untested or null. Nothing measured contradicts the core; several theory-specific elaborations have been contradicted and retired (§4.2).

## 4. Is it useful? (Q3)

### 4.1 What it delivered that a rival framing would not have

1. **The independent-recipient rescue design.** Seeding a residual, letting the recipient form its own late K/V, then transplanting that formed band into an unseeded recipient (E20) is a direct product of thinking in formation/commit/consumer roles. Causal tracing and path patching restore within the same run; they do not ask whether the formed store is a portable object. This design is the program's strongest empirical contribution and it replicated in six families (MEASURED, e20-cross-family and locator FINDINGS).
2. **A cheap blind locator.** Thinking of the read as the interface led to a one-forward-pass statistic that beat a fitted depth rule on the one blind model where they disagree (Phi-2 block 0.515 vs 0.065). A circuits or SAE framing would not have produced a fit-free, transferable locator. The lineage to Geva's attention-knockout locus is real, but making it predictive is a step.
3. **Instrument-validity derivations.** The formalism has repeatedly caught experiments that could not discriminate: the A-only Mamba clock dose at k∈{0.5, 2} is inert by construction (carried term changes ≤7%), which led to the γ = 15–142 retest and the `RETENTION_NOT_COMMIT_LEVER` verdict (architecture-math §8; mamba-clock-retest FINDINGS); the sliding-window swap at length 17 is the identity map; the argmax-locator SD is ill-conditioned on a flat band; endpoint interactions cannot separate K×V from consumer curvature (dynamic-circuits-theory §7, item 7), which forced the raw-logit routing check. This is an underrated use: the theory is better at telling the author which experiments are uninformative than at predicting outcomes.
4. **The pass-indexed baseline.** The finding that a fixed parent flips 11/12 install conclusions in multi-turn contexts is a methods result with immediate practical value (pass-indexed-baseline FINDINGS). The general warning about patching baselines is prior art (Zhang & Nanda 2023) [PRIOR], but the StateCut framing produced the correct counterfactual mechanically.
5. **Fine-tune conservation with a directional asymmetry.** The question "does training move the machine or the code" comes from the theory. The answer — location conserved, readable code conserved base→derivative, written code drifted — is the most novel single observation in the program (first assessment agrees).

### 4.2 Theory-derived predictions and their fate

This is the most informative table in the document. It lists predictions that the theory, rather than generic attention mechanics, generated.

| Prediction | Source | Outcome (MEASURED) |
|---|---|---|
| Depth-fraction band rule predicts blind band | blind-scaffold-prediction PREREG | **Failed** on Pythia-1.4B |
| Attention locator predicts blind band | attention-band-locator PREREG | **Passed**, n=2 (Phi-2 6/6, OLMo-2 5/6) |
| The band builds the store (P2a) | formation-over-time prereg | **Failed**, F2 fired; restated as "commits" |
| Hop-depth law (ℓ* decreasing with hops) | dynamic-circuits-theory P8 | **Failed** on instruct n=46 (22/22/23) |
| Stale pointer lands on competitor (P2a) | dynamic-circuits-theory P2 | **Failed** (competitor 0.0, clean 0.89) |
| Mamba retention latch is the commit lever | 2026-09-30 writer-clock inference | **Failed** (`RETENTION_NOT_COMMIT_LEVER`, write 6/6) |
| Fine attributes lock later in SDXL (L1/L2) | sdxl-relation-lockin PREREG | **Failed** under the frozen readout |
| Binding-changing K+V mis-binds (T3a) | symbol-table PREREG | **Failed** (14/14 transfer) |
| K-only swap re-binds (T2a) | symbol-table PREREG | **Failed** (inert) |
| Keys cluster by role ≥8/12 | symbol-table PREREG | **Partial/failed** (7/12; cNMI 0.637 vs 0.632) |
| Connected graph forecast beats operation-blind | paper campaign C6 | **Failed** (MAE .015099 vs .014593; ties additive rival) |
| Fixed/ceiling ≥ 0.85 | fixed-lowering-iia PREREG | **Passed** (0.87, 1.00) against a narrow ceiling |
| Absolute fixed IIA ≥ 0.75 | fixed-lowering-iia PREREG | **Failed** (0.31–0.76) |
| Frozen relation profile beats competitors | confirmation campaign | **Passed** 8/8; color and identity did not |
| Query selectivity of identical bytes | symbol-table T4 | **Passed** (36/36) |
| V-only ≥ K+V | symbol-table T3b; v2 | **Passed** |
| Frozen routing kills raw-logit interaction | dynamic-circuits-theory P1 | **Passed**, true by construction (routing-readout-correction FINDINGS says so) |
| Matched K+V superadditive | architecture-math §4 | **Passed** qualitatively (+0.34, one factorial) |

**Pattern (INFERRED).** The passes are dominated by predictions that standard attention algebra also makes (selectivity, V as payload, frozen-routing linearity, K×V superadditivity) plus two genuinely theory-specific successes: the blind locator and the fixed lowering at its narrow ceiling. The predictions that are distinctive to the theory's *temporal* story (hop depth, stale pointer, fine-late lock-in, retention latch, band builds store) have failed at a high rate and been moved into "derived sub-claims that failed". Each retreat was empirically honest. Taken together they are the signature of a protective belt absorbing refutations while the hard core makes few risky predictions of its own (Lakatos's degenerating pattern). The author should treat this as the main risk to the theory, more than any single null.

## 5. Which tool successes discriminate the theory from "a deterministic network you can checkpoint"? (Q4)

The living theory says, correctly, that a tool counts as a test only where its success depends on the commitment. Applying that rule to the tools it lists:

| Tool / result | Listed under | What it actually is (MEASURED) | Discriminates? |
|---|---|---|---|
| Exact replay, fork, rewind (StateCut, CausalContextVM, MambaStateVM) | instruments | Complete-state theorem: equal complete state + equal future inputs ⇒ equal futures (architecture-math §2) | **No.** Guaranteed by determinism. Its value is instrument fidelity (it exposed the causal-mask defect that disqualified E6/E8). |
| Scene compiler 21/21 RGB parity; wrong-source renders the other scene | C8 | Prompt enters the denoiser only through text-encoder K/V and pooled conditioning, so the compiled source is complete by construction (architecture-math §2) | **No.** The math document itself labels it custody, not discovery. |
| **Page-out: layers 20–27 exported, native checkpoint reads 0/96, external 96/96, all four held cells exact** | C3 ("paging a committed store only works if there is a committed store to page") | The 96 "keys" are **decoder-layer parameter tensors**. A provider exported the *weights* of layers 20–27 into a content-addressed block; a fresh process loaded those weights from the block and generated multiply-by-4/7 continuations bit-exact (2026-09-06-qwen-recursive-multipage-native-free-rosetta FINDINGS). | **No, and misattributed.** This is weight paging. Bit-exactness follows from loading identical bytes. It involves no activation store, no commit band and no entity readout. It cannot support C3. |
| Virtual-context archive: 2,048 pages / 59,356 tokens; selected 4/4, wrong/absent 0/4, wrong page expresses its own value | C3 | Each page is the **all-layer** K/V of a self-contained fact text, mounted with RoPE relocation (2026-09-24-spectral-virtual-context FINDINGS) | **No for C3.** Reading a mounted all-layer page is in-context reading of a short document; a wrong page yielding its own value is what any attention model does with a wrong document. It does not depend on a late commit band. The same FINDINGS reports that merging all four independently compiled pages answered 1/4 vs 4/4 native, which is relevant to C6 and has systems prior art [PRIOR: Prompt Cache, CacheBlend]. |
| Frozen-site install: correct residual write 1.011 vs wrong site −0.133 vs shuffled −0.607 | C1 | Qwen2.5-0.5B E2 panel; source-residual site at **layer 2**; native clean top-1 only 6/14; the K/V-cut role was non-specific (shuffle retained the same 0.332) (VM checklist) | **Weakly.** An early-layer residual write at the subject position transferring identity is what causal tracing predicts for any model that keeps subject information position-local early. It shows site specificity, not a learned late scaffold. The cut-role failure is evidence against role specificity in that panel. |
| **XOR program 148/150; inverted XNOR executes XNOR 74/75; wrong address 31/75** | C8 | XOR is applied by a host-side tensor-free IR; recipient-local ridge decoders read Booleans from hidden states, mostly at the embedding/layer-0 boundary; the result is written through the frozen head; address routing is a learned policy (semantic-program-payload README) | **No.** The XNOR outcome is decided by the host program. What the result shows about the model is that early hidden states are linearly decodable and that the LM head can be driven to emit a chosen span — both known. It is a strong Saturn runtime result and says nothing about a scaffold. |
| Spectral address ABI (bit-exact gauge invariance; 0 tokenizer ties vs 821 float) | C5 | Integer-ring read kernel; the document itself says "native-consumer and renderer authority not established" (SPECTRAL-ADDRESS-ABI.md) | **No.** Serialization correctness; the living theory already says so. |
| Pass-indexed baseline / PassStateVM | C6 | Restore-and-continue native vs fixed parent; 11/12 flips | **No as evidence; yes as methodology.** History dependence follows from attention over new positions. |
| **E20 band-only transplant into an unseeded recipient** | C3 (as experiment) | Partial state (subject-position K/V at L22–27 only) carries 0.71–0.99 of the seed effect across six families | **Yes.** The math document states a narrow band is not sufficient by construction. This is the one VM-style operation whose success depends on the theory's store claim. |
| v_proj row permutation collapses the signed profile | C1/T5 | Full permutation: relation cosine .955→.049; competence also falls (relation 8/8→5/8) (architectural-paper §6.7) | **Partly.** It separates "trained weights" from "module geometry", but because competence collapses too it is learned-vs-broken, not learned-scaffold-vs-generic. |
| Fine-tune transplant asymmetry | C7 | base→coder 0.92 / coder→base 0.34; base→math 0.43 / math→base 0.05 | **Yes**, subject to the generic-convergence control. |
| Blind locator | C2 | §3 | **Yes**, at n=2. |
| Mamba write-vs-retention retest | (Mamba) | Release hurts 0/6; dt acts via write 6/6 | **Discriminates between two hypotheses inside the theory**, not between the theory and a generic view. |

**Answer to Q4 (INFERRED).** Of the tool successes, only the partial-state transplant (E20) discriminates the theory from "deterministic network you can checkpoint". Exact replay, compiled parity, page-out, the archive, the XNOR program, the spectral ABI and the pass-indexed baseline are each guaranteed by determinism, by architecture, or by a host-side computation. The software clause of the theory is therefore currently supported by one experiment, and the living theory's C3 and C8 tool entries should be corrected.

## 6. Is "unfalsifiable" fair, and does C1–C8 fix it? (Q5)

The charge is fair against the top-level sentence. "A fixed machine runs a per-input program that reads and writes carried state" is satisfied by every deterministic stateful computation, and the role machine a_t = A(s,u_t,z_t), z_{t+1} = T(z_t,w_t), y_t = C(z_{t+1},u_t) is the generic form of a state-space system. The cross-family statement is worse than unfalsified: since the math shows no canonical graph exists (architecture-math §1.3, §10), "the same roles lower differently in each family" cannot fail, which is why the common-graph null did not damage it. That is vacuity, not robustness.

The C1–C8 restatement fixes the *form* for C1, C2, C3 and C7: each names an outcome that could have happened. It does not fix the *epistemics*, for three reasons. First, the commitments were written after the results (§3). Second, three falsifiers cannot fire: C5's "V-only swaps fail to move content" (V is the payload by definition), C6's "Mount = Prefill" and "earlier turns leave the baseline unchanged" (impossible in a causal attention model), and C8's "inverted program still gives the intended answer" (the host computes the inverted program). Third, the thresholds are set against weak rivals: C1's 0.7 threshold is against a six-band ceiling that cannot beat the fixed band by much, and C4 is set against a steering-vector rival that no one proposes for attention.

Missing falsifiers that would make the theory risky:

1. **Cross-operation fixed lowering.** C1 says "all inputs of an operation". If every operation may have its own mapping, "one fixed machine" collapses into "each task has a circuit", the standard view. The architecture claim needs: one lowering per model, frozen before data, serves several operation classes (in-context attribute, parametric recall, two-hop composition, arithmetic or code retrieval). Breaks if a per-class re-located lowering beats it by a wide margin on two or more classes.
2. **A strong per-input rival.** Per-row best over every single layer, every contiguous band of width 2–8, per-KV-head subsets, and a per-prompt learned alignment (DAS) at matched site budget. Breaks if fixed/ceiling falls below 0.7 against that rival.
3. **A prospective prediction of the dynamic part.** The theory currently predicts only that routing varies. It should predict *which* rows and heads the answer query reads for held inputs (the address metric d_τ of dynamic-circuits-theory §4 is the obvious candidate), with a frozen rule. Breaks if the predicted routing does no better than attention-mass baselines.
4. **Partial-state sufficiency as a software prediction.** See §8.4.
5. **Acquisition order.** If interface and program are distinct objects, they should have distinct onsets during pretraining. Pre-register whether the interface location stabilizes before or after task competence on Pythia checkpoints. The current Pythia lane is a counter-trend (matched-depth L2 stronger at every checkpoint, architectural-paper §11.2).
6. **A matched generic-location null.** Run the locator and band test on content positions that the answer does not need (distractor entities). If the locator picks a band with the same block/rescue profile for irrelevant positions, "scaffold" reduces to "wherever attention reads".

## 7. Novelty (Q6)

| Prior line [PRIOR unless noted] | What it already established | Delta claimed here | My call |
|---|---|---|---|
| Geva et al. 2021, FFN key-value memories | MLP layers act as key→value stores for parametric knowledge | A different store: attention K/V at the subject position in a late band, for in-context content | New object, but compatible; the parametric case is untested here |
| Geva et al. 2023, dissecting recall | Subject enrichment; relation propagation; attribute extraction by upper-layer attention from the last token | Formed before the band; band computation unnecessary (0.904/1.023); read at the subject position only (0.871→0.010); independent-recipient rescue; fit-free locator | **Moderate.** A causal refinement of the extraction stage plus a predictive locator. Note that "band computation unnecessary" is partly expected: late-band K/V are projections of a residual that the band's own attention/MLP changes only slightly at the subject. |
| Meng et al. 2022, causal tracing / ROME | Localization by restoration; late attention site at the last token | Isolated cuts (0.985 in-forward vs 0.009 isolated); transplant into unseeded recipients | **Moderate**, methodological |
| Elhage et al. 2021, transformer circuits | Residual stream as channel; Q/K/V-composition; frozen-attention path expansion | Single-read lemma and pointer theorem; conditional linearity | **Small.** The pointer theorem restates Q/K-composition (induction heads are the K-composition case, Olsson 2022). Conditional linearity is the frozen-attention linearization used by path expansion and attribution graphs (Ameisen 2025). The K×V and α(1−α) identities are clean derivations of known softmax algebra. |
| Geiger et al. 2021, 2023; Wu et al. 2023 (DAS) | Causal abstraction; IIA; learned alignments | Uses the definition as is; fixed band reaches its narrow ceiling | **Small** until the ceiling is a real per-input rival |
| Todd 2024, function vectors; Hendel 2023, task vectors | Operations as compact, transportable vectors | Query-dependent, non-additive authority; per-item reader cosine 0.73–0.99 within vs 0.20 across operations | **Small**; FVs were never proposed as the store |
| Feng & Steinhardt 2023; Prakash et al. 2025 (lookback) | Binding IDs; address/pointer/payload separation in binding | Alias residual carries pointer, not value (0.0); V-only 0.89; K-only 0.0 | **Small**: a causal K/V/residual confirmation |
| Merullo et al. 2024, component reuse | Components reused across tasks | One L22–27 interface hosts identity 11/11, color 16/16, position 12/16 | **Small** |
| Lad et al. 2024, stages of inference | Relative-depth stages across families | Depth rule fails blind; model-read locator works | **Small–moderate** |
| Prakash et al. 2024; crosscoders (Lindsey 2024); base↔chat SAE transfer | Mechanisms preserved under fine-tuning; features transfer | Read location conserved under domain continued pretraining at weight cosine 0.2–0.4; **directional** readability asymmetry by causal transplant | **The most novel item** |
| Diffusion: Prompt-to-Prompt (Hertz 2022), eDiff-I (Balaji 2022), SDEdit, P2-weighting (Choi 2022), DAAM, Basu et al. on localizing knowledge in text-to-image models | Timestep-dependent roles; early steps fix layout; cross-attention control | Program × register closure; static K/V, dynamic Q; rectified-flow linear-Gaussian retention law | **Small.** Closure is the complete-state theorem; static K/V is architecture; the retention law is a neat derivation whose single-λ form the data already reject (dynamic-circuits-theory §5.3) |
| Mamba: Sharma et al. 2024 (locating/editing facts in Mamba); Zoology associative recall | Fact localization in SSMs | Write, not retention, is the commit lever (6/6) | **Small but clean** |
| Systems: vLLM PagedAttention, SGLang RadixAttention, Prompt Cache, CacheBlend, LMCache; H2O/Quest-style sparse working sets | Paged and shared KV; prefix trees; modular KV reuse and its cross-chunk error; attention sparsity for speed | Transactional StateCuts with lineage, receipts, commit/abort, durable export, exact native-consumer custody | **Engineering novelty in rigor and auditability**, not a scientific novelty; "Mount ≠ Prefill" is known in this literature |
| Interp tooling: TransformerLens, nnsight, pyvene | Hooks, interventions as programs, remote execution | Typed Acts, safe points, preview/commit, replay refusal without proof | **Tooling novelty** |

**Where the genuinely new part is (INFERRED).** Three things are new: (1) the claim, not yet fully tested, that a learned network exposes *one* fixed store/read interface that is shared across operations and conserved across training while its code drifts directionally; (2) the independent-recipient transplant as the test of partial-state sufficiency, which turns an interpretability finding into a systems operation; (3) an operational semantics for interventions (typed state, typed act, native consumer, pass-indexed native, lineage) that demonstrably changes conclusions (11/12 flips; the mask defect; in-forward 0.985 vs isolated 0.009). Item (1) is the theory; (2) and (3) are its method.

## 8. Attack (Q7)

### 8.1 The strongest case that it is trivial

Every structural statement in the formal documents follows from the architecture. Complete-state closure is determinism. Static K/V with dynamic Q in SDXL cross-attention is how cross-attention is wired. Payload linearity given frozen routing is true of any network whose only nonlinearities are softmax, gates and norms; the raw-logit successor itself says "conditional affinity is expected once that freeze is implemented correctly. It does not independently establish a learned scaffold" (routing-readout-correction FINDINGS). Query selectivity, V-as-payload and K×V superadditivity are softmax algebra. Mamba staged-vs-endpoint composition is h_2 = ρ_2ρ_1h_0 + ρ_2w_1 + w_2. Diffusion coarse-to-fine is posterior-mean denoising. History dependence of K/V is causal attention. On this reading, the theory is a well-organized notation for what the architectures already are, and the dynamic part ("routing varies per input") is the definition of a nonlinear network.

### 8.2 The strongest case that it is a relabeling

The one robust empirical core — a late band at the subject position that later attention reads — is Geva et al.'s attribute-extraction stage. "Source" is the subject token, "formation" is subject enrichment, "commit" is the subject-position K/V at upper layers, "reader" is the last token's attention, "consumer" is the unembedding. The locator is Geva's attention-knockout locus without fitting. The pointer/value result is lookback. The task is in-context copy readout, where the answer token is in the prompt, so the "store" may be nothing more than the place an induction-like copy head reads from. The "three families" breadth is vocabulary: the cross-family role matcher's best assignment beats the next by 0.0386 and is nearly tied with a depth null (architectural-paper §8), and the only prospectively aligned edge is "formed state → unchanged consumer", which for FLUX (target latent at a step) is close to a complete-state corollary.

### 8.3 The strongest case that it is wrong, and the experiment that would most damage it

The case that it is wrong rests on scope. Every positive AR result comes from attribute readout of an in-context entity in a fixed template family. Parametric recall is known [PRIOR: Meng 2022; Geva 2023] to route through mid-layer MLPs at the subject and through attention at the last token at different depths, and multi-hop recall resolves at depths that move with the hop [PRIOR: Biran et al. 2024]. If different operation classes use different interfaces, there is no "one fixed machine", only a library of task circuits, which is the standard view the theory set out to replace. The hop-depth failure does not settle this: it failed in a direction that is consistent with one band, but on a model and task where the band was already known.

**The single most damaging experiment: a cross-operation fixed-lowering test with a strong per-input rival.** In Qwen2.5-1.5B and Gemma-2-2B, freeze one lowering per model from the locator on the existing in-context task, before any new data. Then, with the identical nine-arm E20 panel and the IIA scorer, test it on three new operation classes with natively competent rows: parametric factual recall (CounterFact-style, answer not in context), two-hop composition (in-context "C refers to A" and a parametric two-hop), and one non-attribute operation (arithmetic result retrieval or code return value; the formation-replay Python retrieval is a starting organism). Score fixed against a widened per-input ceiling (all single layers, all contiguous bands of width 2–8, per-KV-head subsets) and against a per-class re-located band. The damaging outcome is: fixed/ceiling below 0.5 on two or more of the three new classes while per-class located sites succeed. That would show the "scaffold" is a per-task interface, reduce T1 to standard circuits plus Geva, and make the first assessment's narrowing mandatory. The theory-favorable outcome (fixed ≥ 0.8 of ceiling across classes) would be the first result that no rival framing predicts and would justify headlining the architecture. Cost is roughly the first assessment's to-dos 1 and 4 combined, a few hours of ≤2B runs.

### 8.4 A second test aimed at the software claim

If "run the model as software" is a theory claim rather than a tooling claim, it predicts partial-state sufficiency at the located interface and failure elsewhere. Test: compile only the located band's K/V for a fact span, mount it into a prompt that never contained the facts (no lower-layer K/V for those positions), and ask the operation. The theory's own routing story (pointers are formed by earlier reads into the answer and alias positions) predicts this should work for direct attribute reads and fail for pointer-following reads, unless the pointer is formed from other positions. Pre-register that split. A matched mount at a non-band window is the control. Success would make paging and caching consequences of the theory; failure would show the store is not self-sufficient and that the VM's value is fidelity, not theory.

## 9. Verdict (Q8)

**Is there a theory-level contribution worth headlining?** Conditionally yes. The headline should not be "dynamic circuits loop through a stable time scaffold" or "a fixed machine runs a per-input program"; those are architecture-true and will be read as vocabulary, as both earlier reviews found. The headline should be the store/router factorization: *trained networks expose a fixed, findable, partial-state-sufficient store/read interface shared across operations and conserved across training, and per-input computation is routing over that interface computed from carried state.* That statement can fail, and it is not implied by the architecture. It is not yet earned, because "shared across operations" and "partial-state sufficient beyond one task" are untested. If the cross-operation test of §8.3 passes, the architecture is the headline and the transformer-only narrowing would undersell it. If it fails, the first assessment's narrowing is correct.

I am not recommending narrowing on the basis of one test. Against all the evidence: the AR evidence is strong and replicated for one task family; the diffusion evidence is mostly architectural by the math document's own account (source sufficiency, static K/V, closure); the Mamba evidence is real but small (write lever 6/6; selected-state transfer +4.59/+7.65 nats with 90.3%/91.6% removed on restore; a 27-coordinate profile beating competitors on 8 capital and 4 delayed identity rows) and supports "the vocabulary lowers" rather than a shared mechanism; the cross-family graph is null; the tool results discriminate in one case. None of that justifies headlining three families. All of it is compatible with headlining the factorization in transformers and presenting diffusion and Mamba as lowerings that pass the same partial-state test.

### 9.1 Load-bearing pillars

1. **Formation, commit and addressed read are separable, and the formed store is a portable, partial-state-sufficient object.** E20 independent-recipient rescue in six families plus 7B; band freeze unnecessary; read at the subject position. Status: strong for one task family.
2. **The interface is fixed and findable.** One frozen lowering at the per-input ceiling; a fit-free locator from one forward pass. Status: adequate; needs the strong rival and n ≥ 8 blind models including ≥7B.
3. **The interface is shared across operations, and per-input computation is routing over it.** Query-gated participation (16/16, 16/16, 36/36), value-in-V and pointer-in-residual (replicated on instruct), routing-mediated interactions at the raw boundary, prospective relation profile 8/8. Status: shared across in-context attributes only; this is the pillar the cross-operation test decides.
4. **The interface survives training while its code drifts directionally.** Location conserved at weight cosine 0.2–0.4; base→derivative readable, derivative→base not. Status: one lineage; needs the generic-convergence control and a second lineage.
5. **Execution-state methodology changes conclusions.** Pass-indexed natives (11/12 flips), isolated vs in-forward cuts (0.985 vs 0.009), native-parity checks that caught the mask defect. Status: solid; present as method, not as evidence for the theory.

### 9.2 What must be added to make it hard to dismiss

1. The cross-operation fixed-lowering test with a strong per-input rival (§8.3). This is the only addition that turns the architecture into a headline.
2. A prospective prediction of the dynamic part: a frozen routing predictor (from d_τ or the locator's head weights) that names which rows and heads a held input's answer query reads, scored against attention-mass baselines.
3. The partial-state paging test (§8.4), to give the software claim a consequence that depends on the theory.
4. Blind locator at n ≥ 8 including Qwen2.5-7B (fix the meta-device hook bug) and at least one instruct model; report narrow-band IoU against single-layer true bands.
5. An independent-harness replication of one E20 cell (TransformerLens or nnsight), because one toolchain already had a silent mask defect.
6. For the fine-tune pillar: E20 at each variant's own band, CKA against an unrelated model, and one more lineage.
7. Rewrite C1–C8 so that every falsifier can fire, and re-run at least two of them prospectively before citing them as "Holds".

## 10. Where I disagree with the first assessment

1. **On what the theory is.** The first assessment treated the umbrella as unfalsifiable and moved it to the discussion. I agree the slogan is unfalsifiable, but there is a falsifiable architecture claim inside it — the store/router factorization with cross-operation sharing — that the first assessment did not separate out. Its recommended paper ("a fixed, findable read band") uses the right evidence but frames the result as a localization finding for one task, which is the narrowest reading. The right next step is to test the architecture claim across operation classes, not to shrink it in advance.
2. **On which tool results matter.** The first assessment discounted the VM and compiler work as "not a science headline". I agree, and I go further on two items it did not check: the C3 page-out tool is weight paging on a multiply task, and the C8 XNOR result is host-computed. Both should be removed from the theory's evidence. I disagree in the other direction on one item: the E20 band-only transplant is a VM-style partial-state operation whose success is not guaranteed, and it is the right bridge between the interpretability claim and the software claim.
3. **On the cross-family null.** The first assessment counted the null against breadth. I think it is more damaging than that: because the math says no canonical graph exists, the cross-family statement cannot fail, so it carries no content. The fix is to state a cross-family *test* (partial-state sufficiency at a located interface in each family), not to drop the families.
4. **On usefulness.** The first assessment did not credit the formalism's best use: catching uninformative experiments before or after they run (inert clock dose, identity-map sliding window, ill-conditioned argmax locator, endpoint-curvature confound). That is a real, repeatable benefit of having the math.
5. **On risk.** The first assessment listed the hop-depth and stale-pointer failures as credibility issues to retract. I read the full prediction table (§4.2) as a pattern: the theory's distinctive temporal predictions fail at a high rate and are retired as sub-claims while the core is restated. That pattern, not any single failure, is what a hostile reviewer will find, and the fix is a prospective, risky prediction from the core.
6. **Agreements.** I agree that the AR spine is one templated in-context task, that query selectivity and V-as-payload are expected, that the routing freeze is near-tautological, that fine-tune asymmetry is the most novel item, and that diffusion timing is the generic coarse-to-fine schedule.

## 11. Corrections the living theory needs now (MEASURED errors)

1. C3 "page-out" is weight paging of decoder layers 20–27 (96 parameter tensors) on a multiply-by-4/7 task, bit-exact because the bytes are identical (2026-09-06-qwen-recursive-multipage-native-free-rosetta FINDINGS). It is not evidence for a committed activation store. Remove it from C3.
2. C3 "virtual-context archive" uses all-layer K/V pages and does not touch the band; it is evidence for typed mounting, not for C3. Its all-pages arm (1/4 vs native 4/4) belongs under C6 with systems prior art cited.
3. C8 "XOR/XNOR" is a host-side program over embedding-level probes written through the frozen head (semantic-program-payload README). Replace it with the SDXL interaction-program result and its unseen-family miss.
4. C1's tool line (1.011 / −0.133 / −0.607) is the Qwen2.5-0.5B E2 layer-2 residual panel with native top-1 6/14 and a non-specific cut role; say so.
5. C5's and C6's falsifiers cannot fire as written; replace with the K-address test on undecided reads (pre-RoPE joint swap) and with a quantitative history-dependence prediction.
6. C7's falsifier partly fired (math→base 0.05); state that the "asymmetric code" reading was adopted after the data.
7. "It is learned: permuting value-projection rows collapses the reader profile" should add that competence collapses with it (relation 8/8→5/8), so this is learned-vs-broken.
8. Rename the living-theory commitments (for example K1–K8) to avoid collision with the paper's campaign labels C5/C7/C8.
