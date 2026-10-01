Four quadrant evidence and the scope of time circuits

Review addendum, 2026-10-01 11:09:45 PDT. This follows the author's questions about the four-quadrant criticism, contradictions after experimental updates, and the novelty of a time-circuit class. It preserves the manuscript and supplements the earlier review. The GPT-5.6 Sol high literature reviewers also rechecked the diffusion and language-model interpretations.

The diffusion experiments do achieve the stated operational pattern. The criticism concerns what that pattern uniquely identifies. It does not invalidate the intervention results, and a linear mechanism would not make temporal dependence uninteresting. The strongest supported claim is a full operational time-circuit signature at a declared cut in FLUX, accompanied by related but distinct profiles in decoder transformers and Mamba.

**What the FLUX experiments did**

The declared specimen is FLUX.2 Klein 4B, pinned revision e7b7dc27f91deacad38e78976d1f2b499d76a294, BF16, 256 by 256 pixels, four denoising steps, guidance 1.0. The historical route is joint.2 through joint.3 and joint.4 to single.0. Source and target prompt runs provide native states or prompt contrasts at corresponding interfaces and steps. Matched recipient runs install the target payload for sufficiency, or source state for counterfactual necessity, at one selected step or all four. The model, scheduler and decoder remain the consumer. Exact no-op controls check that the instrument reproduces the native output before an intervention is interpreted.

At the representative joint.4 cut, a single-step target transplant leaves pixel MAD to target at 48.4, while an all-step transplant reduces it to 0.47. A single-step necessity intervention leaves the target intact, with MAD 7.9, while all-step source replacement reverts it, with normalized progress about -0.93. These are the four operational outcomes reported in [the manuscript's diffusion panel](../paper.md:301).

The later joint-region experiment repeats single versus all-step interventions on five site sets and three setups. The maximum single-step write scores are 0.28 and 0.56, below the 0.90 full-transfer bar, versus at least 0.91 for all-step writing. Single-step necessity leaves the target and all-step source replacement reverts it. The E7 color experiment separately strengthens the necessity half across five seeds. Those five seeds should not be presented as five complete four-quadrant replications. See [the region experiment](../paper.md:372) and [the multiseed necessity experiment](../paper.md:327).

The evidence goes beyond a single positive intervention. It includes matched seeds and execution, no-op checks, off-route and stream comparisons, counterfactual necessity, deletion, sham controls, dose schedules and edge-mediation results. The off-route sweep establishes a redundant conditioning region rather than a unique minimal route. Deletion removes the target, but a norm-matched sham also nulls the image; interchange is therefore the more informative semantic necessity result. These qualifications describe what was learned, rather than erasing the effect.

**Why the pattern does not exclude a distributed linear representation**

Consider an unchanged linear readout y = (x1 + ... + x8)/8. A source has all eight components zero, and a target has all eight components one. Call the target behavior present when y exceeds 0.5.

| Intervention | Readout | Behavioral result |
|---|---:|---|
| Remove one target component | 0.875 | Target survives |
| Write one target component into source | 0.125 | Source remains |
| Remove every target component | 0 | Target disappears |
| Write every target component into source | 1 | Full target recovery |

This produces all four behavioral quadrants without any execution-time mechanism. On normalized effect measures, each single intervention is 0.125 and the joint effect is 1. Thus it can also meet small-single-effect bars such as necessity below 0.25 and write below 0.2. This is a logical counterexample to the claim of unique discrimination. It is not a fitted explanation of FLUX and is not evidence that FLUX actually uses this spatial mechanism.

The manuscript's sentence that a diffuse linear representation must fail whole-path necessity and sufficiency is therefore incorrect. A linear distributed representation can be jointly necessary and sufficient precisely because its individual contributions add. See [the discrimination claim](../paper.md:166).

The phrase "nothing happens" also needs care. The observed single-step write scores are sometimes appreciable, including 0.56. The appropriate claim is that no tested single step attains the specified full-transfer criterion. It is not that every singleton has zero causal effect. Literal zero scalar effects at all singleton interventions would be a different mathematical claim.

**What the timing experiments add**

Unequal effects of early and late dose, and opposite effects of the two net-zero schedules, establish that raw intervention dose is not exchangeable across denoising time. They reject an unweighted sum. They do not reject a time-varying linear response of the form delta-y = sum over t of Kt times ut.

For example, weights approximately [0.21, 0.22, 0.08, 0.04] predict a positive response to the schedule [+1, +1, -1, -1] and a negative response to its reverse. Both schedules have raw sum zero, but their weighted sums have opposite signs. Reversing a schedule changes which payload receives each time weight; it does not by itself demonstrate nonlinear interaction or state feedback.

This alternative is already supported within the research program. [Integral Residual Dynamics section 8](../../integral-residual-dynamics/paper.md:115) reports that the signed weighted-sum diffusion model won held-out selection: MSE 0.0177, versus 0.0202 for relaxation and 0.0218 for a saturating variant. The depth-axis fits are a separate result. The superseded paper is used here as the manuscript's cited source for the timing receipt, not as authority for its older sampled LM certificates.

The same section explicitly corrects the observable: the kernel measures reproduction of a target image, not the moment animal identity is decided. A low image-reproduction score can accompany a recognizable change of identity. Temporal weighting, layout, identity and exact image recovery should remain separate observations.

An additive temporal carrier can legitimately belong to an operational category called a time circuit. Nonlinearity is not a prerequisite for a useful circuit definition. What is unsupported is the further assertion that the four quadrants exclude distributed linear routes or establish a distinct nonlinear dynamical primitive.

If the stronger mechanism claim matters, one small follow-up is a held-out superposition test. Fit singleton responses on a development split and predict joint schedules. On a linear observable such as the final pre-VAE latent, measure delta-z(i+j) minus delta-z(i) minus delta-z(j). Reproducible held-out interaction would reject that fitted additive account. RGB and semantic judgments can corroborate the consumer effect. Such a test is optional for the bounded operational claim; it should not be imposed as a reason to discard the existing trend.

**What the language-model experiments establish**

The isolated K/V protocol runs the recipient prefix through the subject normally, overwrites selected cached subject entries afterward, then runs the suffix. This keeps the subject from reading its own transplanted entries and propagating a supposed single-layer intervention into later stores. Every-layer sweeps are crucial: two sampled layers missed the late writers.

In Qwen2.5-1.5B and Gemma-2-2B, singleton necessity is small, but an isolated singleton formed-store write reaches about 0.81. That exceeds the LM singleton-write bar of 0.2. Consequently the fully swept decoder-LM cells do not meet the paper's complete four-quadrant certificate. Residual writes are stronger still: a single early residual write can author the target, while the model subsequently commits its store late. Mamba sweeps likewise find concentrated late writers. These results establish a valuable formation/commit/read asymmetry, rather than one complete shared four-quadrant class across architectures. See [E15](../paper.md:525), [the isolated write protocol](../paper.md:559), and [the explicit singleton criteria](../paper.md:239).

**Exact contradictions and likely corrections**

Most items below are consistent with the author's explanation that new experiments were added without updating every summary. Their presence is an editorial problem, not evidence that the receipts are unreliable.

| Passage | Conflict and correction |
|---|---|
| [Section 6.1, line 521](../paper.md:521): the clean identity cells "were never write-swept" | [E15 at line 525](../paper.md:525) and E17 report completed writes near 0.81. Remove the stale sentence; retain the correctly stated absence of a full LM certificate. |
| [Section 6.4, line 709](../paper.md:709): transformer K/V "certifies" on fully swept cells | Conflicts with E15 and Figure 2's statement that no LM cell passes all four. Say K/V exposes distributed necessity plus a concentrated write. |
| [Section 7.2, line 957](../paper.md:957): Qwen2.5-0.5B has a "time-circuit identity cell" | [E19 at line 588](../paper.md:588) identifies the identity store as a redundant L20-L21 pair and calls it a space circuit with backup. Use that updated description. |
| [Section 12, line 1142](../paper.md:1142): computed object still rests on two sampled layers | [E11 at line 669](../paper.md:669) reports a full sweep over 45 addition items and retracts the earlier verdict. Remove the computed cell from this limitation. |
| [Section 6.1b, line 555](../paper.md:555): residual write "equals" downstream write sum; [line 568](../paper.md:568): Mamba "conserves exactly" | The neighboring text reports Mamba deviations of 0.02-0.15 and transformer sums of 0.99-2.96. State approximate conservation for Mamba and correlated, redundant commit profiles for transformers; reserve additivity for the bounded downstream segment. |
| [Abstract B, line 94](../paper.md:94): no supported intervention moves an answer beyond 0.08 | [Section 9, line 1073](../paper.md:1073) reports color effects of 0.31-0.42. Restrict the 0.08 claim to identity and explicitly report partial color visibility. |
| [Section 9, line 1053](../paper.md:1053): attribution graphs "do not explain cross-position flow" | [The introduction, line 128](../paper.md:128) correctly distinguishes accounting for flow from explaining why attention selected it. Use that distinction consistently. |
| [Conclusion, line 1186](../paper.md:1186): what was "certified" includes the same certificate shape in LMs | [Line 1192](../paper.md:1192) says the full signature is established in diffusion and only half-established in LMs. Label the LM finding as a partial signature or distinct profile, not a complete certificate. |

Two further issues concern interpretation rather than merely stale prose. First, the linear-exclusion claim at line 166 requires changing the argument. Second, [section 6.7](../paper.md:826) says early-step unmount is inert in 0/8 cases while consumed-step unmount flips 8/8; the next paragraph calls the chain distributed along the whole scratchpad. Those observations show an indispensable consumed step and dispensable earlier step. Whole-path necessity follows from removing the indispensable step and does not establish that no single scratchpad step is necessary. The supported CoT result remains strong: selected non-copied intermediate state is causally used, and a counterfactual page swap can author its downstream arithmetic consequence.

The manuscript also needs one consistent meaning of "single site matters." Its space-circuit definition uses any measurable singleton effect, while its time-circuit tests permit nonzero effects below thresholds. Those categories can overlap unless the definition specifies the observable, threshold, intervention and site grain. A measured operational classification is more defensible than a universal binary partition of all circuits.

**Prior work and the novelty claim**

The manuscript already gives substantive shared/different comparisons for Meng, Geva and Agarwal, especially [section 6.1b](../paper.md:609). The criticism should not be read as saying the author ignored prior work. Agarwal explicitly studies early availability and late commitment across four decoder models; the manuscript's additional isolated necessity, K/V cut and commit/read measurements are meaningful distinctions. [Relation Before Entity](https://arxiv.org/abs/2609.17537).

Cheng and Zhang already show single-position intervention failing while joint intervention succeeds, across multiple decoder families. That overlaps the broad distributed-intervention lesson, even though their position axis, task and intervention object differ. [Single-Position Intervention Fails](https://arxiv.org/abs/2605.04061).

Two close additions deserve direct comparison: DifFRACT uses timestep-conditioned transcoders and circuit interventions in FLUX.1[schnell], and Dura and colleagues study sequential CoT activation patching and joint head interventions. These overlap temporal diffusion analysis and reasoning-trajectory interventions respectively; they do not automatically preempt the paper's whole package. [DifFRACT](https://arxiv.org/abs/2606.15796), [Sequential Activation Patching](https://arxiv.org/abs/2608.22332).

The literature audit did not identify a predecessor with this exact collection of cut-specific four-quadrant tests, production diffusion results, full decoder/Mamba sweeps, write/commit/read contrasts and native tool comparison. That is a bounded audit conclusion, not proof of absolute priority. A paper can establish one relevant ingredient without publishing a synthesis across diffusion, decoder transformers and state-space models. Missing that synthesis does not remove the ingredient from prior art.

It is defensible to introduce "time circuits" as an operational category and report an instance in a transformer: FLUX is a diffusion transformer. It is not currently defensible to say full sweeps establish that category generally in decoder transformers, or to claim an exclusive new computational primitive distinguished from distributed linear mechanisms by these four outcomes alone.

Suggested central claim:

> We introduce time circuits as an operational category of causal routes whose control is distributed across an execution trajectory at a declared interface. In a production diffusion transformer, single-step interventions fail to reproduce or remove the target behavior, while matched whole-trajectory interventions succeed. Decoder transformers and Mamba exhibit related but distinct formation, commitment and read profiles, including distributed necessity and concentrated writers. These results show why sampled single-site measurements can miss causal support or misidentify the location of a stored object.

The original contribution can be strong without claiming that every constituent observation was previously unknown, that all architectures implement one mechanism, or that a four-cell diagnostic mathematically excludes every additive alternative.
