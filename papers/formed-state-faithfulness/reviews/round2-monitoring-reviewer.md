---
title: "Round-2 review: The Answer Follows the Cache (formerly Formed-State Faithfulness)"
reviewer: "CoT-monitoring / alignment (hostile-but-fair, external); same reviewer as round 1"
date: 2026-10-02
verdict: "Reject at main; weak-accept / borderline at a safety-interp workshop as a discussion note. Overall 4/10. Recommend folding into the companion paper rather than submitting separately."
scope: "Read-only on paper.md + README.md + round1 review/response. I did not re-run jobs or recompute from raw results; all figure/number claims = asserted by the paper, not re-verified."
---

# Round 2

## 1. Did the reframe fix round 1?

The concession is real and well executed. The silent-repair-rises-with-scale claim — the would-be-novel empirical result in round 1 — is retracted, correctly, via the operand-cut/resample controls (§7, Table 2). Integrity is now exemplary. But conceding the headline leaves the paper *thinner*, not stronger: what remains is (a) an **injected** token-vs-state dissociation that the paper itself calls "close to a sanity check" (L120), (b) a **retracted** claim re-badged as a known caveat, and (c) a **negative** probe. Honesty about a near-tautology and two negatives does not lift the contribution.

## 2. Is the remaining headline novel/useful, or trivially expected?

**Largely expected, and the paper says so.** Overwriting a step's full KV span across every layer and head with a donor value's rows, then getting the donor's answer (Table 1, 100%), is resample-ablation / activation patching at saturation. The forward pass reads the cache; of course it follows the edit (L120 concedes this). The "a step-reading monitor sees nothing" half is now correctly labeled "by construction" (L140, §6) — i.e. a tautology, not a finding: you *constructed* a token/state mismatch that no natural generation produces (L32, L130).

Against the named prior work the delta is modest:
- **Lanham'23 / Turpin'23** — their contribution is natural *unfaithfulness* (the model uses a cue it doesn't state). This paper's dissociation is injected; it shows a capability, not a behavior. The "text perturbations co-vary token and state" methodological point (§4.4) is fair and is the real novelty seam, but it is a methods improvement, not a monitoring result.
- **Pfau'24 (filler tokens)** — hidden computation that arises *under training*. Sharper than this paper on the axis that matters (natural vs injected). The "meaningful non-copied step" distinction is weaker than it sounds when the mismatch is hand-built.
- **Korbak'25** — "reading written steps is an upper bound on monitorability" is a corollary of their framing, not a new claim.
- **Activation patching / steering** (Vig'20, Meng ROME'22, Wang IOI'22, Geiger causal-abstraction; ActAdd/ITI) — the state-only swap and the donor-"authorship" result (§4.4, 0.59–1.00) *are* resample-ablation and representation steering. **None of this literature is cited** (§9, L194–202 cites self-repair and faithfulness only). Until it is, the "of course patching changes outputs" objection stands and novelty is overstated.

The genuinely non-trivial empirical nugget is the **text-only cell scale signal** (§4.1, L100): token pull 0.47/0.56 at 0.5B → 0.00 at 1.5B → 0.10 at 7B, i.e. the answer's read-point shifts from token to cache with scale. That is *not* a priori obvious and is the one result worth building a paper around — and it is one sentence on 2–3 points with no CIs.

## 3. Is it a real monitoring threat?

Not yet, and §4.3 defuses its own headline: the model re-verbalizes the injected value 0.66–1.00 of the time (L122–124), so a full-transcript monitor recovers most of it. The *measured* residual monitoring gap is the minority non-re-verbalized, decision-relevant fraction — which the paper never isolates as a number. The honest reading is: on synthetic arithmetic, with a hand-built edit, the net transcript-invisible effect is small. That is a reassuring result dressed as an alarming one.

## 4. Minimal experiments that would make it matter

1. **Natural occurrence (the whole ballgame).** Exhibit a token/state mismatch that arises in *free* generation (not injected) where the answer follows the cache against the written token. This converts a patching demo into a monitoring finding. Named as TODO D but absent; without it there is no demonstrated faithfulness failure.
2. **A residual that survives the transcript.** Find/construct a regime where the cache carries decision-relevant information the continuation does *not* re-verbalize, and quantify that fraction. This is the only number that makes the threat non-vacuous given §4.3.
3. **A detector that works.** Turn the probe negative into a positive: layer-swept, held-out FPR (named at L208/L260). "Cache channel dark to text but readable by a cheap probe" would be a genuinely useful monitoring contribution. As run (single layer, λ tuned in-sample, LOO, no FPR), the negative is uninformative — it cannot support "state-aware monitoring is hard."

## 5. Top-5 must-fix (with line refs)

1. **Title/abstract over-read an injected edit.** "The Answer Follows the Cache" (L2/L14) implies a discovered threat; the result is an injected capability the paper calls a near-sanity-check (L120). Retitle to name the injection (e.g. "A step's formed state *can be made to* override its token"), or deliver natural occurrence (exp 1).
2. **Lead with the measured residual, not the tautology.** §4.3 (L122–124) shows full-transcript monitoring recovers 0.66–1.00; state the net transcript-invisible, decision-relevant fraction as a single number and make *that* the monitoring claim. Right now the headline and its refutation sit in tension.
3. **Promote and power the text-only scale signal** (§4.1, L100) — the only non-expected empirical result. Add CIs/points or concede it is underpowered (2–3 points, 3B is base).
4. **Cite and position against activation-patching + steering** (§9, L194–202). The central method is resample-ablation + steering; omitting Vig/Meng/Wang/Geiger/ActAdd/ITI inflates novelty and leaves "of course patching changes outputs" unanswered.
5. **Make the probe negative mean something or demote it** (§5 L140; limitations L208/L260): layer sweep + held-out FPR, or state plainly it was not tested properly and drop the "state-aware monitor is the hard part" implication.

Secondary: the 3B-base-vs-Instruct confound (L56/L180/L257) and 2-points-per-axis undercut every scale statement, including the one good signal in (3); the pending 7B-Instruct (L56/L180) is load-bearing for scale and still absent.

## 6. Score, tier, and separate-vs-fold

**Overall 4/10.** Method and custody are strong; the exact-restore (Δ=0.0) instrument and the token×state 2×2 are citable. But the surviving empirical core is one expected (injected) dissociation, one retracted claim, and one uninformative negative — with the one non-trivial result (text-only scale signal) left underpowered and the threat largely closed by the paper's own re-verbalization number.

- **Main venue (ICLR/NeurIPS): reject.** No natural occurrence, no working detector, arithmetic-only, 2-point scale axes.
- **Safety/interp workshop (SoLaR/interp): weak-accept / borderline** as a discussion note — the exact-restore-gated dissociation method and the honest dispensability correction are worth a hallway argument.

**Separate vs fold — fold.** The companion `time-formed-circuits` paper already carries the repair phenomenon and swap-authorship numbers (paper's own §9 overlap statement, L202). After the concession, this note's standalone seam is a *methods* contribution — the exact-restore 2×2 and the operand-cut dispensability control — not an independent result. Recommendation: fold the 2×2 dissociation method + the dispensability/operand-cut control into the companion paper (or a short methods note), and hold a separate submission until **either** natural occurrence (exp 1) **or** a working state-aware detector (exp 3) lands. Those are what turn this from "patching a reasoning step does what patching does" into a monitoring result.

— *Measured vs asserted:* I verified paper/README text and internal consistency directly (measured); all run numbers and figures are asserted by the paper — I did not re-run jobs or re-open raw results.
