---
title: "Two Channels of a Reasoning Step: The Token a Monitor Reads and the Cache It Does Not"
author: Jacob Hollenbeck
type: research-paper
status: submission-manuscript (round-1 revision)
date: 2026-10-02
venue_target: interpretability / AI-safety venue (workshop-ready; main-venue pending running controls)
evidence_cutoff: 2026-10-02
companion: ../time-formed-circuits/
working_name: "Formed-State Faithfulness"
tags: [chain-of-thought, faithfulness, monitorability, self-repair, causal-mediation, key-value-state, interpretability]
---

# Two Channels of a Reasoning Step: The Token a Monitor Reads and the Cache It Does Not

**Jacob Hollenbeck**

## Abstract

Chain-of-thought monitoring assumes that reading what a model writes reveals what it used. We test this on a single arithmetic step whose value the prompt never restates (Qwen2.5, 0.5B-7B), editing the key/value cache the step forms, under an exact-restore control that reproduces the base answer bit-for-bit. Our cleanest result is natural and scale-dependent: after a step's cached state is removed, the model still answers correctly far more often at larger scale, the removal unannounced in the text. On common items the still-correct rate rises from 0.095 (0.5B) to 0.762 (1.5B), so removal-based attribution under-measures the effect of removing a step. Whether this is internal re-derivation or recomputation from operands still in the prompt is a control we are running. A precision control rules out a floating-point artifact; 4-bit quantization roughly halves the rate. Separately, a maximal edit shows the hidden-state channel is load-bearing: overwriting only the cached state, written value held correct, flips the answer on 95-100% of items. A step-reading monitor is blind to this, but the model usually re-verbalizes the injected value (0.66-1.00), so a full-transcript monitor recovers most. Reading written reasoning steps bounds monitorability rather than measuring it. Scope: synthetic arithmetic, greedy, one seed.

---

## 1. Introduction

A chain-of-thought monitor reads the reasoning a model writes and acts on it: it flags steps that look like reward hacking, deception, or disallowed planning. This only works if the written reasoning is a faithful trace of the computation that produced the answer. Recent position work makes the stakes explicit: chain-of-thought monitorability is a real but fragile property that current training happens to give us and could remove (Korbak et al. 2025), and reasoning models already reach answers for reasons they do not state (Chen et al. 2025; Turpin et al. 2023).

Most faithfulness measurements intervene on the chain's *text*. They truncate it, insert a mistake, paraphrase it, or replace it with filler, then watch whether the answer moves (Lanham et al. 2023; Turpin et al. 2023). These are the right first questions and they are black-box, which is their strength. But a text intervention always changes two things at once: the token a monitor would read, and the internal state that token's position forms in the key/value cache. If the answer moves, a text method cannot say which of the two channels carried the effect.

This paper separates the two channels and measures each on the same reasoning step. We study a single step whose written value is *non-copied*: the final answer needs one further operation on it, and the prompt never restates the value, so a correct answer cannot be produced by copying the written number alone. On such a step we ask two questions. Does the answer depend on the *written token* (what a monitor reads)? And does it depend on the *formed cache state* at that token's position (what a monitor does not read)? We make the second answerable with an exact-restore control: before trusting any cache edit, we require that ablating and then restoring the exact original rows reproduces the base answer's token-sequence log-probability bit-for-bit, so any change under a real edit is caused by the edit, not by leaky replay. This passes on every item of every run.

We lead with the result that is natural, not constructed. When we remove a step's cached state and let the model finish, larger models recover the correct answer far more often, and the regenerated text does not announce the removal. So a removal-based attribution scheme under-measures the effect of deleting a step, increasingly with scale. This is our cleanest number (common-subset still-correct rate 0.095 at 0.5B to 0.762 at 1.5B), and we are careful about its interpretation: the operands remain visible in the prompt, so the model may be recomputing from them rather than re-deriving the step through hidden state, and those two readings have opposite monitoring implications. A control that cuts operand access is running; until it lands we report the measured compensation, not a mechanism.

Our contributions are the following.

1. A natural, scale-dependent result: removing a step's cached state is compensated far more often at larger scale (still-correct rate rising with size at matched precision), with a precision control that rules out a floating-point artifact and a measured 4-bit confound (Section 5).

2. A clean dissociation of the two channels on the same items, using edits a text-only method cannot perform. A maximal state-only edit shows the hidden-state channel is load-bearing (95-100% of items); a monitor reading only the written step is blind to it, but the model usually re-verbalizes the injected value, so a full-transcript monitor recovers most (Section 4).

3. The monitorability reading, stated with its scope: a step-reading monitor has zero recall against the state-only edit by construction, a full-transcript monitor recovers most of it, and removal-based attribution under-measures a step's effect increasingly with scale, with the mechanism (hidden re-derivation versus recompute-from-prompt) pending a running control (Section 7). We recommend state-aware probes and repair-aware ablation metrics.

The headline for practice is narrow: reading written reasoning steps is an upper bound on what a monitor can know, not a measure of it. How loose that bound is depends on the model, the edit, and whether the monitor reads the full transcript, and we quantify it for one task family.

---

## 2. Setup

*Formed state*, in this paper, means the key/value cache written at a step's token positions during the forward pass: the internal state a token forms, as opposed to the token text itself.

### 2.1 Task

We study teacher-forced two-operation arithmetic chains. The written intermediate step is non-copied: the model states one value, and the final answer requires one more operation on that value, while the answer cue never restates it. For example, the chain states "6 times 7 = 42" and the cue then asks for that result minus five; the answer 37 cannot be produced by copying "42" alone. Removing the copy route lets a cache edit on the step be read as an edit to computed, not transcribed, information.

Each item is admitted to an arm only if the model's greedy completed answer under the chosen cue is correct and the model is on-policy for the step (it would itself compute the step's value). Answer cues are selected per item from candidates that do not restate the step, taking the first the model answers correctly. Admission is per arm, so the admitted count n differs across models; we report n with every rate.

A numeric answer is credited only when the generated text closes it syntactically (end-of-sequence, a line break, an explicit "the answer is N", or terminal punctuation); an unfinished right-hand side such as "= 42 - 5" is not an answer. This conservative reading matters: an earlier version of this line of work used a short fixed-length parser that scored unfinished expressions as answers, inflating apparent removal failures. The present readout runs generation to 128 tokens and reads the closed answer.

### 2.2 Models and precision

We use Qwen2.5-Instruct at 0.5B, 1.5B, and 7B parameters, greedy decoding, one seed, with stock attention and native causal masks. We could not run a clean single-precision curve across all three sizes, and are explicit about how we compensate.

The 3B checkpoint was not cached and new downloads were disallowed under a storage constraint, so the size curve is 0.5B / 1.5B / 7B. The 7B model in bfloat16 did not fit on our 16 GB accelerator: an attempt was recorded but never completed as a job, while 4-bit (NF4) quantization fit with an observed peak of 5.9 GB. The 7B model therefore runs in NF4. The specific capacity figures sometimes cited for this (bfloat16 weights near 15.2 GB, a rejected reservation, an admittable ceiling) are *asserted* from model size and configuration, not read from a saved artifact, and are collected in Appendix D; only the 5.9 GB peak and the absent completed-job record are measured. A paged/offload bfloat16 7B point is available and is one of the controls we are running (Section 5.6).

To keep the scale claim from being a precision artifact we add two measured controls: 0.5B and 1.5B in both float32 and bfloat16 (the float32-versus-bfloat16 axis), and 1.5B additionally in NF4 (the bfloat16-versus-4-bit axis). The NF4 1.5B point brackets the 7B-NF4 point so 7B is read against a quantization-matched 1.5B, not against the bfloat16 curve. As Section 5 reports, this control earned its place: 4-bit quantization itself changes the rate.

### 2.3 The two channels

A reasoning step can influence the answer through two channels. The *token-visible channel* is the written step value as text, which a chain-of-thought monitor reads; a text intervention acts on it, but because re-running re-forms the cache from the edited text, it moves the hidden channel too. The *hidden-state channel* is the key/value cache the step's positions form, which a reader of the written chain cannot access; we act on it directly by editing the cached rows while leaving the written tokens unchanged.

### 2.4 The exact-restore intervention and three canaries

All cache interventions operate on the step's token span across every layer and head. *Ablate* replaces the step's rows with the per-position mean (removing the step's specific state). *Swap* overwrites the step's rows with another item's rows for the same span (installing a different value's state). *Restore* ablates then writes back the exact original rows.

The exact-restore control is the instrument's foundation: for every admitted item, restore reproduces the base answer's token-sequence log-probability to within 1e-3, and does so exactly (observed maximum absolute difference 0.0) on every item of every run, including 4-bit. Because restoration is bit-exact, a change under ablate or swap is attributable to the edit, not to replay error.

Two further canaries guard against an inert or an indiscriminate instrument. The *copied point-read canary* uses a passcode-readout family where the written value genuinely is a copy of a prompt token; there, ablating the value flips the answer on 100% of items (n=8 per run; see the 7B footnote in Appendix B), showing the instrument fires when a value is read from its token. The *early-versus-late canary* uses two-step chains: ablating the already-consumed early step changes nothing (0.00, n=8) while ablating the decisive late step changes everything (1.00, n=8), showing the edit is localized.

One scope limit: the teacher-forced edit changes the step's *stored* state, which later answer generation reads; it does not rewrite already-formed downstream positions, and the model does not regenerate the earlier text after the edit. Section 6 relaxes this by letting the model write and continue its own chain.

![A reasoning step lives in two lanes: the token a monitor reads and the cache it does not](figures/fig1_two_lane_schematic.png)

*Figure 1. A non-copied reasoning step occupies two lanes. The written token "= 42" (yellow) is what a text monitor reads; the key/value state it forms (red) is what a monitor cannot read directly, and the answer reads from that state. The three interventions: a text edit changes the token and re-forms its state (what text methods do); a state-only swap keeps the correct token but overwrites its cached state; a state ablation removes the step's cached state and lets the model continue.*

The same instrument renders one real item concretely (Figure 2), which previews the two edits before the aggregate panels. On the item "6 times 7, minus 5" with scratchpad "6 times 7 = 42" (Qwen2.5-1.5B, bfloat16; the product 42 is never restated and the answer 37 is not the product), per-layer necessity (zeroing the step's page one layer at a time) peaks at the writer layer 20 (0.274) with a narrow commit band at layers 20-22, and at the decisive answer digit the answer depends on both the visible scratch token (3.38 nats) and the hidden formed state (3.76 nats). A state-only donor swap flips the answer while the visible text still reads "= 42" (the Section 4 dissociation, on one item); zeroing the page drives the answer wrong (−3.04 nats), so this particular item is *not* silently repaired. We flag that honestly: silent repair is item-dependent, and this harder multiply step shows none, unlike the 0.76 aggregate repair rate at 1.5B (Section 5). The exact-restore no-op canary is 0.0.

![What a text monitor reads versus what the cache holds, for one item](figures/fig2_vm_trace.png)

*Figure 2. What a text monitor reads versus what the cache holds, for one real item (Qwen2.5-1.5B bfloat16; the computed non-restated step 6×7−5, scratchpad "= 42", answer 37). Top: a layer × generated-token heatmap of attention onto the formed intermediate page, with the per-layer necessity side panel peaking at the writer layer 20 (0.274) and the necessity/commit band 20-22 marked. Bottom: per generated token, the answer's dependence on the visible scratch token (blue, what a text monitor reads) and on the hidden formed state (red, what it does not); at the decisive answer digit both are load-bearing (visible 3.38, hidden 3.76 nats). A state-only donor swap flips the answer with the visible text fixed at "= 42"; zeroing the page breaks the answer (−3.04 nats), so this item is not silently repaired — item-dependent, unlike the 0.76 aggregate at 1.5B (Section 5). No-op canary 0.0. Trace and job in Appendix A.*

### 2.5 Monitor definition

A *step-reading monitor* reads the written reasoning steps, parses the stated step, and predicts the answer from it; this is the object text-based faithfulness work operates on, and it is blind to the hidden-state channel by construction. A *full-transcript monitor* reads the entire generated output, including the answer continuation. We distinguish the two throughout, because they differ sharply on the state-only edit (Section 4.3, Section 7.1).

---

## 3. The token-visible channel (prior supporting battery)

We first confirm, from a separate prior battery, that the token-visible channel behaves as text methods assume. This battery is not part of the pre-registered panel of Sections 4-6: it is an earlier, independently recorded set of runs on a different task (code-trace) and different models (SmolLM2-1.7B, Qwen2.5-0.5B, Qwen3-8B, Qwen3-30B-A3B), measured with receipts and an exact-restore no-op. When a chain writes the answer value itself, swapping the key/value state at that written token flips the answer and shifts its log-probability by 8-14 nats across four families, while swapping the input operand tokens shifts it by under 2 nats and does not flip it; the answer is read from the externalized token, not re-integrated from the inputs, and a worked chain turns an otherwise-incapable model capable. The per-family numbers and provenance are in Appendix A and Appendix E. The point for this paper is only calibration: on the token-visible channel, a text monitor reads the thing that matters. The rest of the paper concerns the case this picture misses, where the written step is not the answer and the answer depends on state the text does not carry.

---

## 4. The hidden-state channel: token-versus-state dissociation

### 4.1 The dissociation design

We hold the task to the non-copied step and run a two-by-two on the same admitted items, crossing the written step token (correct original versus a wrong value) with the stored step state (correct original versus the wrong value's state): base (both correct); both-wrong (written value edited and re-formed, state wrong); state-only (written value correct, state wrong); and text-only (written value wrong, state restored to correct). The cell that isolates the hidden channel is state-only: the written chain reads the correct value, but the cached state is the wrong value's.

A scale signal already appears in the fourth, text-only, cell. When we corrupt the written value but restore the state to correct, the answer still changes on 0.47 (0.5B bfloat16) and 0.56 (0.5B float32) of items, but on 0.00 at 1.5B (all precisions) and 0.10 at 7B. At 0.5B the written token still pulls the answer even with the state corrected; by 1.5B the corrected state dominates the wrong token. The two channels are not only separable, their relative strength shifts toward the hidden channel with scale.

### 4.2 The hidden-state channel is load-bearing (a maximal edit)

Overwriting only the stored state, with the written value left correct, changes the completed answer on 100% of admitted items at 0.5B and 1.5B (bfloat16, float32, and NF4) and on 95% at 7B (Table 1). A concrete instance at 0.5B: the chain reads "6 times 7 = 42" (correct) while the state of "43" is installed, and the model answers 38 = 43 − 5. The written step is correct and the answer is wrong; a monitor reading only that step sees nothing amiss.

**Table 1. State-only edit changes the answer while the written step stays correct (written-step-blind rate), and the text-visible edit for comparison. Rate [95% bootstrap CI]; n is admitted single items with a valid 2×2 cell (smaller than the repair n in Table 2 for 1.5B NF4; see note).**

| Model | Precision | n | Written-step-blind change (state only) | Text-visible change |
|---|---|---:|---|---|
| 0.5B | bfloat16 | 32 | 1.00 [1.00, 1.00] | 1.00 |
| 0.5B | float32 | 32 | 1.00 [1.00, 1.00] | 1.00 |
| 1.5B | bfloat16 | 21 | 1.00 [1.00, 1.00] | 1.00 |
| 1.5B | float32 | 29 | 1.00 [1.00, 1.00] | 1.00 |
| 1.5B | NF4 | 21 | 1.00 [1.00, 1.00] | 1.00 |
| 7B | NF4 | 22 | 0.955 [0.864, 1.000] | 1.00 |

*Note on n.* For 1.5B NF4 the dissociation denominator (items with a valid 2×2 cell) is 21, the text-visible denominator is 23, and the repair denominator in Table 2 is 24; the counts differ because the cells have different validity requirements, not because of an inconsistency.

This is a near-maximal edit, and we read it conservatively. The forward pass runs on the cache, so overwriting the step's cache with another value's state and getting that value's answer is close to a sanity check; the surprising outcome would be the opposite. We therefore treat it as confirming that the answer region *uses* the step's stored state, and as an existence proof that the hidden channel is load-bearing, rather than as a capacity number in any information-theoretic sense. The pre-registered prediction (state-only change at least 0.30, text-visible at least as large) held, and the falsifier (interval includes zero) did not fire.

### 4.3 The written step is blind, but the answer continuation usually is not

The written-step-blind label is scoped to a monitor that reads only the written step. The model's own answer continuation frequently exposes the injected value: with the state of 43 installed, the model continues "43 − 5 = 38", so 43 appears in the generated text. Among items where the state-only edit changed the answer, the continuation re-states the injected value on 21/32 at 0.5B (0.66), 20/21 at 1.5B bfloat16 (0.95), 29/29 at 1.5B float32 (1.00), 21/21 at 1.5B NF4 (1.00), and 14/21 at 7B (0.67). A monitor that reads the full generated transcript would catch most of this edit.

So the dissociation reads as follows: the step's hidden state can override its written value; monitoring the written step alone is insufficient; but the model usually re-states the hidden value later, so a full-transcript monitor largely recovers it. What the written step fails to carry, the answer often carries. The unrecoverable part is confined to items where the continuation does not re-verbalize the value (about a third at 0.5B and 7B, near zero at 1.5B). This recovery is the most policy-relevant finding in the section, and it is why we frame the hidden channel as a reason to read the whole transcript, not as a claim that the model is unobservable.

![A step's role splits into token-visible and written-step-blind channels; the blind channel is mostly recovered from the full transcript](figures/fig3_token_vs_state.png)

*Figure 3. For each arm, the text-visible edit (red) and the state-only edit (blue) each change the answer on nearly all items; the two channels are separately sufficient. The third series (green) is the fraction of state-only answer changes a full-transcript monitor would recover because the model re-verbalizes the injected value (0.66-1.00). The gap below green is the residual a full-transcript monitor would miss.*

### 4.4 Scope, sufficiency, and why text methods cannot isolate this

The state-only edit is artificial: no natural generation process writes a correct value into the text while forming a wrong value's state, and we do not claim models do this on their own. The edit's role is to drive the hidden channel directly so we can measure that it is load-bearing; the naturally occurring gap is Section 5.

A directed variant confirms sufficiency and content-specificity. Installing a *different* item's step state (a donor swap) makes the model emit the donor's arithmetic answer on 0.59 of items at 0.5B (bfloat16, [0.41, 0.75], n=32), 0.81 at 1.5B bfloat16 ([0.62, 0.95], n=21), 1.00 at 1.5B float32 ([1.00, 1.00], n=29), and 0.82 at 7B NF4 ([0.64, 0.96], n=22). No text intervention can perform this, because the written chain still shows the original step; the donor's influence travels entirely through the installed state. More generally, text perturbation co-varies token and state (editing the text re-forms the cache), so it cannot attribute an effect to either channel; the state-only and donor edits move the state with the token held fixed, which is the manipulation text methods cannot express. This is the methodological gap relative to Lanham et al. (2023) and Turpin et al. (2023), whose interventions are our text-visible baselines.

---

## 5. Removing a step is compensated more at larger scale

### 5.1 The measurement, and what it does and does not show

We ablate the step's stored state, let the model complete its answer, and ask whether the answer is still correct. A correct answer after removal we call *silent repair*: the model recovers the answer and the completed text does not announce that anything was removed. A wrong answer is a clean removal failure.

This quantity bears on removal-based attribution, which treats a removal failure as evidence the step mattered. If the model recovers the answer, a removal test scores the step as dispensable; the more it recovers, the more such tests under-measure the effect of deleting the step. That much is what we measure.

What we do *not* yet establish is the mechanism, and the distinction is central. The operands remain in the prompt and in the cache after we ablate only the step's span. So a recovered answer could be *hidden re-derivation* (the step's role travels through state a monitor cannot audit, the monitoring-relevant threat) or *recompute-from-prompt* (the model recomputes 6×7−5 from inputs that are still present and still visible to a monitor, which is benign for monitoring and is simply single-site-ablation brittleness in the sense of Miller et al. 2024). A tell that the second reading is live is internal to our own design: the state-only edit flips the answer 100% with no room to regenerate, while ablate-then-generate recovers more with scale precisely because the model is given room to recompute from the still-cached operands. We therefore report the measured compensation and soften any claim of hidden re-derivation. The decisive control is running.

<!-- TODO A repair-from-prompt -->
*(Running) Control A, repair-from-prompt.* Same admitted items: ablate the step's state **and** cut the model's access to the operand/question tokens (attention mask or cache ablation), with a converse arm (operands cut, step intact) and a sanity arm. If recovery collapses when operands are cut, the compensation is benign recompute-from-prompt; if it persists, it is genuine hidden re-derivation. This result will determine whether Section 5 is a monitorability finding or an ablation-robustness finding, and we will revise the framing to match.

### 5.2 Compensation rises with scale at fixed precision

Silent repair rises sharply with model size (Table 2, Figure 4). On the bfloat16 axis it goes from 0.19 at 0.5B to 0.76 at 1.5B (+0.57, non-overlapping intervals). On the 4-bit axis it goes from 0.29 at 1.5B to 0.73 at 7B (+0.44, non-overlapping). The pre-registered prediction (rises with scale, 0.5B-to-largest increase at least 0.25) held on both axes; the falsifier did not fire.

**Table 2. Silent-repair rate after ablating the step's stored state. Rate [95% bootstrap CI], n admitted single items.**

| Model | Precision | n | Silent-repair rate | Removal-wrong rate |
|---|---|---:|---|---|
| 0.5B | bfloat16 | 32 | 0.188 [0.062, 0.344] | 0.812 |
| 0.5B | float32 | 32 | 0.188 [0.062, 0.344] | 0.812 |
| 1.5B | bfloat16 | 21 | 0.762 [0.571, 0.952] | 0.238 |
| 1.5B | float32 | 29 | 0.828 [0.690, 0.966] | 0.103 |
| 1.5B | NF4 | 24 | 0.292 [0.125, 0.458] | 0.625 |
| 7B | NF4 | 22 | 0.727 [0.545, 0.909] | 0.273 |

### 5.3 The comparison is not paired, but the effect survives on common items

Admission accepts a different subset at each size; the admitted sets are nested within the 0.5B pool of 32 (32/32/21/29/24/22), so the headline rates are over overlapping, unequal sets. Restricted to items admitted at both compared sizes, the effect strengthens: on the 21 items admitted at both 0.5B and 1.5B (bfloat16), repair is 2/21 (0.095) versus 16/21 (0.762); on the 17 admitted at both 1.5B and 7B (NF4), 6/17 (0.353) versus 14/17 (0.824); on the 11 admitted at all six arms, 0.091 (0.5B), 0.818 (1.5B bfloat16), 0.273 (1.5B NF4), 0.818 (7B NF4). The rise with scale and the 4-bit deflation are not artifacts of which items each arm admitted.

### 5.4 The effect is not a floating-point artifact

The float32-versus-bfloat16 control is a null, as predicted: identical at 0.5B (0.188 versus 0.188), and 0.762 versus 0.828 at 1.5B (difference 0.066, overlapping intervals). The effect is not bfloat16 rounding. This de-confounds an earlier two-point observation from our own prior work in which the smaller model was float32 and the larger bfloat16 (Section 8).

### 5.5 A confound we did not predict: 4-bit quantization halves repair

At 1.5B, NF4 gives 0.292 against 0.762 in bfloat16 (difference 0.47): 4-bit quantization roughly halves the silent-repair rate at fixed size. This refutes the part of our pre-registration predicting the 4-bit gap would be within 0.20, and we report it straight. The consequence is a reporting discipline: the 7B point (4-bit only) is compared to the 4-bit 1.5B point, where the scale effect still holds (0.29 to 0.73). The pre-registered cross-check passes: the 4-bit gap (0.47) is smaller than the bfloat16 size gap (0.57). For anyone monitoring quantized deployments, a 4-bit model repairs removed steps about half as often as its bfloat16 counterpart, so removal-based attribution will look more faithful on it for reasons unrelated to the reasoning being more externalized.

![Silent repair rises with scale](figures/fig4_repair_vs_scale.png)

*Figure 4. Silent-repair rate after ablating a step's stored state, versus model size (log scale), two precision axes drawn separately. Solid bfloat16 line connects 0.5B (0.19) and 1.5B (0.76); there is no bfloat16 7B point. Dashed 4-bit line connects 1.5B (0.29) and 7B (0.73), 7B labeled NF4-only. Float32 diamonds (0.5B, 1.5B) sit on or near the bfloat16 points (the 1.5B float32 diamond is slightly above, at 0.83); the 4-bit 1.5B point sits well below, the quantization confound made visible. Each line is two points. Error bars are 95% bootstrap CIs.*

### 5.6 What this does to removal-based metrics, and what is still needed

What we can say now is scoped to ablation-metric robustness: single-site removal increasingly under-measures a step's effect as scale grows, at fixed precision, so the same removal that scores a step as load-bearing at 0.5B scores it as dispensable at 1.5B. This is a concrete, directional, scale-dependent instance of the general warning that circuit and faithfulness scores depend on ablation methodology (Miller et al. 2024), and it is a step-grain, task-answer instance of the self-repair family in which an ablation is compensated downstream (McGrath et al. 2023; Rushing & Nanda 2024). Whether it is also a *monitorability* finding depends on Control A: if the compensation is hidden re-derivation, reading the chain misses a step's role; if it is recompute-from-prompt, the monitor reads the same operands the model used and nothing is hidden. Two further controls are running and will sharpen the claim.

<!-- TODO C bf16-7B/3B -->
*(Running) Control C, off the deflated axis.* A paged/offload bfloat16 7B point and, if cacheable, a Qwen2.5-3B point, so the curve has more than two points per axis and the top point is not on the 4-bit-deflated axis.

<!-- TODO D natural problems -->
*(Running) Control D, natural reasoning.* The ablation-repair curve on natural word problems rather than synthetic arithmetic, where operands are not trivially present as clean tokens, with Control A applied. Synthetic arithmetic is the worst case for the repair claim because the operands sit in the prompt; the natural-task result is what would make the monitorability reading robust.

---

## 6. Free-running chain-of-thought (exploratory)

The teacher-forced panel prefills the whole chain, so the model never regenerates the step after an edit. To probe the deployment-closer setting we let the model write its own chain on natural word problems, admit items where the base answer is correct and a self-generated intermediate is locatable, then ablate or swap that intermediate's cached state and continue natively. This panel is exploratory: the sample is small (nine admitted of twenty at 1.5B), and it is not bit-exact. By our pre-registered no-op threshold of 0.90, both arms are discounted (a no-edit re-rollout matches the base 8/9 = 0.889 at 1.5B and 5/9 = 0.556 at 7B), so no confirmatory claim rests on it; the core results are the exact-gated teacher-forced panels.

Two directional observations, stated as suggestive. First, self-generated state is causally read: swapping a self-written intermediate to a wrong value changes the answer on 100% of items at both sizes, refuting the falsifier that self-generated state is not read downstream even under the weak instrument. Second, at 1.5B, ablating a self-written step leaves the answer correct 7/9 of the time while the regenerated text restates an edited value only 1/9 of the time; this looks like the Section 5 compensation reproduced when the model authors its own chain, subject to the same repair-from-prompt caveat and to the discount. A coherent *injected* value (the swap), by contrast, is re-verbalized on 100% of items, so that manipulation is monitor-visible in free generation. The full free-running table and figure are in Appendix F.

---

## 7. What a monitor can and cannot see

### 7.1 A step-reading monitor has zero recall by construction; a full-transcript monitor recovers most

Under the state-only edit the written step is the correct original, so a step-reading monitor predicts the base (correct) answer by construction and its recall on the state-induced answer changes is zero (the written-step-blind rate is 1.00 at 0.5B/1.5B, 0.955 at 7B). We state plainly that this zero is *by construction*, not a discovered property: a monitor that reads only the step cannot see an edit we placed entirely outside the step text.

The policy-relevant number is the full-transcript one. Because the model re-verbalizes the injected value on 0.66-1.00 of changed items (Section 4.3), a monitor reading the whole transcript recovers most of this edit; the residual it misses is the minority of non-re-verbalized items. The defensible statement is therefore: *reading the written reasoning steps is insufficient, because a step's hidden state can override its written value; reading the full transcript restores most of the visibility for this edit* (an artificial edit, per Section 4.4).

### 7.2 Removal-based monitoring and attribution degrade with scale (mechanism pending)

Separately, a scheme that removes a step and checks whether the answer breaks will increasingly miss steps that larger models compensate for (Section 5). Whether this is a monitorability loss (hidden re-derivation) or benign (recompute from visible operands) is exactly what Control A resolves; until then the safe statement is that single-site removal under-measures a step's effect at scale. Reading written reasoning steps is, in this precise and bounded sense, an upper bound on monitorability rather than a measure of it.

### 7.3 Recommendations for practice

First, pair text monitors with state-aware probes where the cost is justified. The hidden channel is directly measurable, and a cheap probe on the cached state at a step's position could flag a token-state mismatch a text monitor misses. Whether such a mismatch ever arises naturally is open; a probe deployed alongside a text monitor would answer it, and if a linear probe can read the stored value then the channel is not actually dark to a state-aware monitor. We are building this probe.

<!-- TODO B probe monitor -->
*(Running) Control B, probe-based state monitor.* Fit a cheap probe on the cached state at the step position to decode the stored value, and test whether it flags the state-only mismatch a step-reading monitor misses, and whether it reads the "hidden" channel at all.

Second, make ablation-based faithfulness and attribution metrics repair-aware: a removal the model compensates for should be scored as a repair event and reported separately, because its rate changes with scale and quantization, rather than folded into "the step did not matter." Where decomposition into separately checked sub-questions is feasible, it also narrows the gap between what the chain states and what the answer uses (Radhakrishnan et al. 2023).

### 7.4 Relation to the obfuscation risk

Our results are mechanistic and upstream of the training-dynamics risk that optimizing against a monitor teaches models to hide intent in the chain while still misbehaving (Baker et al. 2025); we do not study training pressure. What we add is a lower-level fact about where a step's influence can live, and a measurement of how much of it a full-transcript monitor currently recovers.

---

## 8. Related work

**Self-repair / the Hydra effect.** The closest prior work is the self-repair literature: ablating a component causes others to compensate, so the ablation under-states the component's role (McGrath et al. 2023, the Hydra effect, at 7B on logit direct effect; Rushing & Nanda 2024, across families, imperfect and noisy). Our silent repair is the same family at a different grain: measured at the semantic reasoning-step level on the task answer (recovery of a non-copied value), not at the head/layer level on logit direct effect, and quantified across scale and quantization. As a contrasting datapoint, single-layer edits corrupt factual recall easily but repair it rarely (Bugaud 2026), whereas we find step-level recovery that is substantial and rises with scale. What is new here is the scale-and-quantization quantification and the monitorability framing (pending Control A); the existence of compensation under ablation is not new, and we position silent repair explicitly as its reasoning-step, scale-dependent instance.

**Latent / implicit multi-step computation.** The hidden-channel result is adjacent to work on internal intermediate computation. Yu (2024) probes hidden states on implicit multi-step arithmetic and argues models do not robustly compute intermediate steps internally when only prompted; our load-bearing state-only edit is a causal rather than probing counterpart on a meaningful non-copied step. Yang et al. (2024) find latent multi-hop reasoning used in a majority of prompts for some relation types, with a scaling trend on the first hop; Biran et al. (2024) show back-patching hidden representations from later to earlier layers corrects 32-66% of failed multi-hop answers, a repair-adjacent mechanism. These concern factual multi-hop rather than arithmetic step removal, but they bound how much intermediate computation is internal versus textual.

**Text-perturbation faithfulness.** Lanham et al. (2023) intervene on the text (early answering, adding mistakes, paraphrasing, filler) and watch the answer; Turpin et al. (2023) show chains can misrepresent the true cause of a prediction. These are our text-visible baselines; the methodological difference is that text perturbations co-vary token and state and so cannot isolate the cache channel (Section 4.4).

**Hidden computation in filler tokens.** Pfau et al. (2024) show transformers can use meaningless filler tokens' hidden states to carry computation absent from the token identities; we isolate the state at a *meaningful* non-copied step under exact-restore gating and tie it to a scale-dependent repair rate.

**Monitorability, and faithfulness-metric robustness.** Korbak et al. (2025) and Baker et al. (2025) frame monitorability as valuable, fragile, and degradable by training or architecture. Chen et al. (2025) show reasoning models often do not verbalize cues they rely on. Paul et al. (2024) study and improve faithfulness through causal mediation of steps; Bentham et al. (2024) show a common faithfulness metric correlates with accuracy after normalization; Miller et al. (2024) show circuit faithfulness scores are highly sensitive to ablation methodology. Our Section 5 gives that sensitivity a direction and a candidate cause.

**Our own prior work (overlap statement).** A companion paper on time-formed circuits (its Section 8) already reports the *existence* of this repair phenomenon and the swap-authorship numbers for the two-operation chain (E10: removal wrong 3/30, repairs 25/30 at 1.5B bfloat16; donor authorship 19/32 and 30/30), with the smaller and larger models in different precisions and with the chain shown not to meet that paper's strict distributed-time-circuit certificate. We cite that paper for the prior E10 result and do not re-claim it. What is new here and not in the companion: the scale *curve* with a 0.5B anchor and a 7B point, the float32-versus-bfloat16 and bfloat16-versus-4-bit precision controls, the token-versus-state 2×2 dissociation, the re-verbalization / full-transcript analysis, and the monitorability framing. A separate small study of freely generated lexical bindings (not arithmetic) found that moving only a self-generated value's cached state, visible reply fixed, changes a later answer (3/3 eligible, 2/3 blocking), corroborating the hidden-state channel for non-arithmetic self-generated content at small n.

---

## 9. Limitations

The task is synthetic two-operation arithmetic, chosen so a non-copied step and a clean cue can be constructed and checked; the capacity, repair, and free-running measurements are arithmetic only, and synthetic arithmetic is the worst case for the repair claim because the operands sit in the prompt (Control D addresses this). The central mechanism of Section 5 is unresolved pending Control A: we report compensation under removal, not hidden re-derivation. The models are Qwen2.5 Instruct at 0.5B/1.5B/7B; the 3B point is missing, each precision axis is two points, and decoding is greedy with one seed (within-arm variability is item-level bootstrap, not seed-level). The 7B model runs only in 4-bit, on an axis the paper itself shows deflates repair; a bfloat16 7B point is Control C. Mean-ablation may push the cache off-distribution, so "repaired versus not" partly conflates "step unneeded" with "the mean landed near a valid state"; a zero/resample-ablation comparison would harden Section 5. The state-only and donor edits are artificial and measure that the hidden channel is load-bearing, not natural behavior (Section 4.4); the zero-recall figure is for a step-reading monitor and is true by construction, with a full-transcript monitor recovering most. The free-running panel is small and discounted by its own canary (Section 6, Appendix F). The two-step chains do not meet a strict distributed-time-circuit certificate, and we do not claim they do.

---

## 10. Conclusion

A reasoning step influences a model's answer through two channels: the token it writes, which a monitor reads, and the cache it forms, which a monitor does not read directly. Separating them under an exact-restore control, we find that a maximal state-only edit confirms the hidden channel is load-bearing (95-100%), that a step-reading monitor is blind to it while a full-transcript monitor recovers most because the model re-verbalizes the injected value, and that removing a step's cached state is compensated far more often at larger scale (still-correct rate 0.095 to 0.762 on common items, 0.5B to 1.5B), not a floating-point artifact and surviving on common items, with 4-bit quantization halving it. The scale result is our cleanest, and we are careful with it: whether the compensation is hidden re-derivation or recomputation from operands still visible in the prompt is a control we are running, and the monitorability reading waits on it. What we can already conclude is that single-site removal under-measures a step's effect increasingly with scale, and that reading written reasoning steps bounds monitorability rather than measuring it. We recommend pairing text monitors with state-aware probes and making ablation-based metrics repair-aware.

---

## Appendix A. Experiment table

All runs: Qwen2.5-Instruct, greedy, one seed, stock attention with native causal masks, on a single RTX 4080. CIs are 95% item-level bootstrap (10,000 resamples). Pre-registration and falsifiers were frozen before any job. The primary record directory is `saturn/experiments/2026-10-02-cot-formed-state-faithfulness/`.

**Full teacher-forced runs (Sections 4, 5).**

| Model | Precision | Panel | n single | Job ID |
|---|---|---|---:|---|
| 0.5B | bfloat16 | teacher | 32 | job-8acc379d0951 |
| 0.5B | float32 | teacher | 32 | job-bd0bf96a7a27 |
| 1.5B | bfloat16 | teacher | 21 | job-d0ad89ab793c |
| 1.5B | float32 | teacher | 29 | job-4861f1f15284 |
| 1.5B | NF4 | teacher | 24 | job-4a5981fa28fc |
| 7B | NF4 | teacher | 22 | job-bc10cd445816 |

**Full free-running runs (Section 6, Appendix F).**

| Model | Precision | Panel | n admitted | Job ID | Status |
|---|---|---|---:|---|---|
| 1.5B | bfloat16 | free | 9 | job-602f0c494da4 | discounted (no-op 8/9 = 0.889 < 0.90) |
| 7B | NF4 | free | 9 | job-f904b4749690 | discounted (no-op 5/9) |

**Single-item VM trace (Figure 2).** Qwen2.5-1.5B-Instruct, bfloat16, eager, exact cache-edit, item 6×7−5 (scratchpad "= 42", answer 37), `job-e034c77db8d6`; per-layer necessity peak at layer 20 (0.274), commit band 20-22, state-only donor swap flips the answer with the visible text fixed, zeroing the page breaks the answer (−3.04 nats, no silent repair on this item), no-op canary 0.0. Source: `saturn/experiments/2026-10-02-vm-trace-visualizer/` (FINDINGS-draft.md, renders/qwen-trace.png, traces/qwen-trace.json).

**Supporting prior experiments (verified against the above before citing).**

| Role | Task / finding | Models | Source path |
|---|---|---|---|
| Token-visible channel (Section 3, Appendix E) | Chain externalization; written-token swap dominates input swap; plain-incapable to chain-capable | SmolLM2-1.7B, Qwen2.5-0.5B, Qwen3-8B, Qwen3-30B-A3B | `saturn/experiments/2026-08-21-ird-fruit-battery/README.md` |
| Computed-state causal use (confounded precedent, de-confounded here) | Swap authorship 19/32, 30/30; removal-wrong 26/32, 3/30 | Qwen2.5-0.5B (fp32), 1.5B (bf16) | `research/papers/time-formed-circuits/paper.md` (E10); `saturn/experiments/2026-10-01-e10-completed-answer-rerun/FINDINGS.md` |
| Hidden state in self-generated content (non-arithmetic) | Move self-generated value's state, visible reply fixed, later answer changes 3/3 eligible, block 2/3 | Qwen2.5-1.5B (fp32) | `saturn/experiments/2026-10-01-qwen-alias-binding-feedback/FINDINGS.md` |
| Copied-value necessity (context) | Unmounting a copied value flips the answer (0.84); non-copied earlier reading superseded as a restatement artifact | Qwen2.5-0.5B | `saturn/experiments/2026-09-30-mvm-mamba-cot/FINDINGS.md` |

## Appendix B. Methods details

**Interventions.** Cache edits act on the step's token span across all layers and heads. Ablate replaces rows with the per-position mean; swap overwrites with another cache's same span; restore writes back the exact original rows. The text-visible edit replaces the written step value with a same-token-length wrong value and re-prefills. A swap changes the step's stored state that answer generation reads, not already-formed downstream positions (Section 2.4).

**Admission.** Admitted iff the greedy completed answer is correct and, where required, the model is on-policy for the step. Cue selection uses a short rollout to pick the first non-restating cue the model answers correctly; all arms use a 128-token continuation. Base native correctness is 1.00 for every arm except 7B NF4 (0.955, i.e. 1 of 22 admitted singles had a wrong full-128-token base despite passing cue selection).

**Readout.** A numeric answer is credited only when syntactically closed; an unfinished compound right-hand side is not an answer. This replaces an earlier 14-token leading-number parser.

**Canaries (all runs).** Exact-restore no-op: maximum absolute answer-sequence log-probability difference 0.0 (threshold 1e-3), every admitted item including 4-bit. Copied point-read: unmount changes the answer at rate 1.00 (n=8 copied items per run; at 7B, 7 copied items were admitted and the flip rate is computed over the 6 with a scored unmount, so the 7B copied canary is 6/6, not 8/8). Early-versus-late: early 0.00, late 1.00 (n=8).

**Statistics.** Rates are over admitted items (each item one bootstrap cluster); intervals from 10,000 resamples; rates with fewer than 8 items reported as fractions.

## Appendix C. Pre-registration predictions and outcomes

| Prediction (frozen before runs) | Outcome |
|---|---|
| Repair rises with scale on bfloat16; 0.5B-to-largest increase at least 0.25 | Held: 0.19 to 0.76 (bfloat16), 0.29 to 0.73 (4-bit axis); falsifier did not fire. Mechanism (hidden re-derivation vs recompute-from-prompt) is unresolved pending Control A |
| Precision is not the driver: within 0.20 at matched size for float32 and 4-bit | Partly held: float32-vs-bfloat16 null (0.066 at 1.5B); 4-bit-vs-bfloat16 refuted (0.47), reported as a confound |
| State-only change at least 0.30 at 1.5B and 7B; text-visible at least as large | Held: 1.00 at 1.5B, 0.955 at 7B; text-visible 1.00. Scope: the continuation re-verbalizes the injected value on 0.66-1.00 of changed items, so the blind label is for a step-reading monitor, not a full-transcript one |
| Free-running: state edit changes answer at least 0.30; text reveals fewer than answer changes; swap repair higher at 7B | Exploratory: swap changes answer 1.00 (falsifier refuted); ablate text-reveals (0.11) below answer-change at 1.5B; both arms discounted by the frozen no-op canary (8/9 and 5/9, both below 0.90) |
| Exact-restore no-op reproduces base answer within 1e-3 | Held exactly (0.0) on every admitted item and run |

## Appendix D. Deviations log

- 3B uncached, downloads disallowed; size curve is 0.5B / 1.5B / 7B.
- 7B bfloat16 did not fit on the 16 GB accelerator (attempt recorded, no completed job); 7B runs in NF4 (observed peak 5.9 GB). The GB figures (15.2 / 15.9 / 14.6) are *asserted* from model size and configuration, not from a saved rejection artifact. A paged/offload bfloat16 7B point is Control C (Section 5.6).
- NF4 lowers repair at fixed size (0.292 vs 0.762 at 1.5B); the 7B point is read against 1.5B NF4.
- Scale comparison is unpaired/nested (32/32/21/29/24/22); common-subset robustness in Section 5.3.
- Written-step-blind scope: continuation re-verbalizes the injected value on 21/32, 20/21, 29/29, 21/21, 14/21 of changed items; a full-transcript monitor recovers most (Sections 4.3, 7.1).
- An offline quantization dependency was loaded through an additive path shim inert on the bfloat16/float32 paths; non-quantized results were collected under a prior worker revision, only the 4-bit runs under the later one.
- The frozen manifest was amended after its timestamp with an additive bug-fix entry and a worker-hash bump; the frozen predictions, falsifiers, and the 3B / 7B-NF4 deviations are as registered in the pre-registration, which predates the first full run and is the authority. The manifest is therefore not bit-immutable.
- The free-running panel is not bit-exact; by the frozen no-op threshold of 0.90 both arms are discounted (1.5B 8/9 = 0.889, 7B 5/9 = 0.556). It is exploratory; all confirmatory results rest on the bit-exact restore gate.
- A custody audit completed after the first draft and recomputed the point estimates exactly from the final post-bug-fix full runs; its corrections are incorporated. Round-1 reviewer corrections (re-lead, repair-from-prompt framing, prior-art additions, figure and scope fixes) are incorporated in this revision; Controls A-D are running.

## Appendix E. Token-visible channel: per-family numbers (Section 3)

Prior battery, separate task (code-trace) and models, measured in float32 with the exact-restore no-op passing and no falsifier firing. Written-token state swap versus input-only swap, as the answer's log-probability shift in nats: SmolLM2-1.7B 8.02 vs 0.94; Qwen2.5-0.5B 9.23 vs 0.88; Qwen3-8B 14.18 vs 0.53; Qwen3-30B-A3B 11.59 vs 1.64 (plain incapable at margin −1.09, chain-capable at +5.82). At 1.7B the plain prompt is answered incorrectly (margin −0.54) and a worked chain makes it correct (+2.40). Source: `saturn/experiments/2026-08-21-ird-fruit-battery/README.md` (Addenda F1-R, F2-R, F3-R). These are a supporting prior battery, not part of the pre-registered panel of Sections 4-6.

## Appendix F. Free-running chain-of-thought (discounted panel)

Both arms are below the pre-registered no-op threshold of 0.90 and are reported for completeness only.

**Table F1. Free-running chain-of-thought. Rate [95% bootstrap CI where n permits]; n admitted and located.**

| Model | n | Ablate: answer changed | Ablate: silent repair | Ablate: text reveals edit | Swap: answer changed | Swap: text reveals edit | Free no-op canary |
|---|---:|---|---|---|---|---|---|
| 1.5B bfloat16 | 9 | 0.222 [0.00, 0.556] | 0.778 | 0.111 [0.00, 0.333] | 1.000 | 1.000 | 0.889 (8/9), discounted |
| 7B NF4 | 9* | 0.500 [0.125, 0.875] | 0.444 | 0.222 [0.00, 0.556] | 1.000 | 1.000 | 0.556 (5/9), discounted |

*The 7B `ablate answer-changed` rate (0.500) is computed over 8 scored items (one of the 9 admitted lacked a scored ablate continuation); the header n = 9 is the admitted-and-located count. The rate is unaffected.

![Free-running chain-of-thought](figures/figF1_free_running.png)

*Figure F1. Free-running chain-of-thought (exploratory; both arms below the pre-registered no-op threshold of 0.90). Left: ablating a self-generated step changes the answer rarely (blue), is silently repaired (green), and the regenerated text seldom reveals the edit (red). Right: swapping to a coherent wrong value always changes the answer and is always re-verbalized.*

## References

- Baker, B., Huizinga, J., Gao, L., Dou, Z., Guan, M. Y., Madry, A., Zaremba, W., Pachocki, J., Farhi, D. (2025). Monitoring Reasoning Models for Misbehavior and the Risks of Promoting Obfuscation. arXiv:2503.11926.
- Bentham, O., Stringham, N., Marasović, A. (2024). Chain-of-Thought Unfaithfulness as Disguised Accuracy. arXiv:2402.14897.
- Biran, E., Gottesman, D., Yang, S., Geva, M., Globerson, A. (2024). Hopping Too Late: Exploring the Limitations of Large Language Models on Multi-Hop Queries. EMNLP 2024. arXiv:2406.12775.
- Bugaud, Z. (2026). Single-Layer Activation Edits Easily Corrupt Factual Recall but Rarely Repair It. Proceedings of the 6th Workshop on Trustworthy NLP (TrustNLP 2026), pp. 515-527.
- Chen, Y., Benton, J., Radhakrishnan, A., Uesato, J., Denison, C., Schulman, J., Somani, A., Hase, P., Wagner, M., Roger, F., Mikulik, V., Bowman, S. R., Leike, J., Kaplan, J., Perez, E. (2025). Reasoning Models Don't Always Say What They Think. arXiv:2505.05410.
- Korbak, T., Balesni, M., Barnes, E., Bengio, Y., Benton, J., Bloom, J., Chen, X., Cooney, A., et al. (2025). Chain of Thought Monitorability: A New and Fragile Opportunity for AI Safety. arXiv:2507.11473.
- Lanham, T., et al. (2023). Measuring Faithfulness in Chain-of-Thought Reasoning. arXiv:2307.13702.
- McGrath, T., Rahtz, M., Kramár, J., Mikulik, V., Legg, S. (2023). The Hydra Effect: Emergent Self-repair in Language Model Computations. arXiv:2307.15771.
- Miller, J., Chughtai, B., Saunders, W. (2024). Transformer Circuit Faithfulness Metrics are not Robust. arXiv:2407.08734.
- Paul, D., West, R., Bosselut, A., Faltings, B. (2024). Making Reasoning Matter: Measuring and Improving Faithfulness of Chain-of-Thought Reasoning. arXiv:2402.13950.
- Pfau, J., Merrill, W., Bowman, S. R. (2024). Let's Think Dot by Dot: Hidden Computation in Transformer Language Models. arXiv:2404.15758.
- Radhakrishnan, A., Nguyen, K., Chen, A., Chen, C., Denison, C., et al. (2023). Question Decomposition Improves the Faithfulness of Model-Generated Reasoning. arXiv:2307.11768.
- Rushing, C., Nanda, N. (2024). Explorations of Self-Repair in Language Models. ICML 2024. arXiv:2402.15390.
- Turpin, M., Michael, J., Perez, E., Bowman, S. R. (2023). Language Models Don't Always Say What They Think: Unfaithful Explanations in Chain-of-Thought Prompting. NeurIPS 2023. arXiv:2305.04388.
- Yang, S., Gribovskaya, E., Kassner, N., Geva, M., Riedel, S. (2024). Do Large Language Models Latently Perform Multi-Hop Reasoning? ACL 2024. arXiv:2402.16837.
- Yu, Y. (2024). LLMs Do Not Think Step-by-step In Implicit Reasoning. arXiv:2411.15862.
