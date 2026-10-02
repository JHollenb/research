---
title: "Round-1 review: Formed-State Faithfulness"
reviewer: "CoT-monitoring / alignment (hostile-but-fair, external)"
date: 2026-10-02
verdict: "Reject at ICLR/NeurIPS main; borderline-accept at a safety/interp workshop. Overall 4/10."
scope: "Read-only review of paper.md, README.md, figures/ (fig2/3/4 opened; fig1 is a TODO placeholder). I did not re-run jobs or recompute numbers from raw results; cited figures = asserted by the paper, verified visually only."
---

# Review

## 1. Thesis, relevance, novelty
**Thesis (one sentence):** A reasoning step's causal role splits into a token-visible channel (the written value a CoT monitor reads) and a hidden key/value-cache channel (which it cannot); the hidden channel has near-total capacity under a direct edit, and "silent repair" of a removed step rises with scale, so reading the written CoT is an upper bound on monitorability, not a measure of it.

**Would my team care?** Yes to the framing. Intervening on the KV cache directly — gated by a bit-exact restore control — is a genuine methodological step past text-only faithfulness (Lanham'23, Turpin'23), which co-vary token and state. The exact-restore no-op (Δ=0.0) is the paper's best idea and I'd cite it as an instrument.

**New vs prior work.** The state-vs-text *dissociation under exact-restore gating* is new relative to Lanham/Turpin (text-only) and sharper than Pfau'24 (filler tokens carry computation — adjacent, but on meaningless tokens; here a meaningful non-copied step). The "silent repair rises with scale" empirical claim is the novel part. But see §2: its headline interpretation is under-controlled, and the capacity result (§3) is close to expected.

## 2. Is "silent repair rises with scale" a faithfulness finding? (the central problem)
No — not as controlled. The experiment ablates **only the step's KV span** and leaves the **operand tokens in the cache** ("6", "7", "minus 5"). A larger model answering correctly is most parsimoniously **recompute-from-prompt**: it re-derives 6×7−5=37 from inputs that are still present and still visible to a monitor. The paper's own §5.1 concedes the alternative ("reconstructs the removed step, **or routes around it**") then scores all of it as "repair / under-counting."

This matters because the two readings have **opposite** monitoring implications:
- *Hidden re-derivation* (paper's framing): the step's role travels through state a monitor can't audit → monitorability degrades with scale.
- *Recompute-from-prompt* (the untested confound): the step was **dispensable given the visible inputs**; the monitor reads the same operands the model used → **no monitorability loss at all**, just single-site-ablation brittleness (exactly Miller'24, which the paper cites).

A sharp tell that the confound is live: the **state-only edit flips 100%** (teacher-forced, no regeneration — the corrupted cached state flows through) while **ablate+128-token generation repairs more with scale** (the model is *allowed to recompute*). The difference between the two panels *is* "was the model given room to recompute from the still-cached operands." That is the recompute story, visible inside the paper's own design.

**The decisive missing control:** ablate the step **and** cut the model's access to the operand/question tokens (attention mask or ablate their cache). If repair collapses → recompute-from-prompt (benign for monitoring). If it persists → genuine hidden re-derivation (the claimed threat). Until this runs, every "silently re-derive / under-counts a step's role / grows with capability" sentence (L170, L174, L211, L260, L268, L310) is an overclaim; "both models used it" (L211) is asserted, not shown. Honestly reframed, §5 is a contribution to **ablation-metric robustness** (step redundancy given visible inputs rises with scale), not to CoT monitorability.

## 3. Is the state-only swap a real monitoring threat? Is the capacity framing adequate?
The paper is admirably honest that it's artificial (§4.4, §9) — a *capacity* result, not natural hiding. But the result is near-tautological: the forward pass runs on the KV cache, so overwriting the step's cache with another value's cache and getting that value's answer is close to a sanity check; the surprise would be the opposite. "Capacity" here is "a hand-built max-strength edit saturates," not capacity in any rate/information sense — the word oversells. And the paper's own §4.3 **defangs the headline**: in natural continuation the model re-verbalizes the injected value 0.66–1.00 of the time, so a **full-transcript monitor recovers most of it** and the net hidden-over-visible information is small. That reassuring result is the most policy-relevant finding in the paper and it's buried as a "scope correction." Relevance to real threats is limited to a conditional upper bound ("*if* training/architecture came to use the channel"), which is legitimate but weak.

## 4. Is the evidence enough?
For an exploratory/workshop note with this honesty, nearly. For a main-venue monitorability claim, no:
- **Synthetic 2-op arithmetic** is the *worst case* for the repair claim — operands sit in the prompt, so recompute-from-prompt is trivial. Natural reasoning is untested for the core results.
- **Scale = 2 points per axis** (0.5B→1.5B bf16; 1.5B→7B NF4). A slope from two points. 3B missing.
- **7B is NF4-only**, and NF4 itself halves repair (the paper's own confound, §5.5), so the single biggest point sits on a deflated axis. The task notes a **paged 7B is available** — a bf16 7B point is the obvious fix and the paper doesn't attempt offload.
- **Free-running** (closest to deployment) is **discounted by its own no-op canary** (8/9, 5/9 < 0.90). So the entire *confirmatory* story is teacher-forced hand-constructed edits; the one natural-generation panel certifies nothing. Good integrity, but it means the deployment-relevant claim rests on exploratory data.
- One seed is fine given greedy decoding; item bootstrap is appropriate.

Secondary: **mean-ablation** may push activations OOD; "repaired vs not" partly conflates "step unneeded" with "mean landed near a valid state." A zero/resample-ablation comparison would harden §5. The early-vs-late canary helps locality but not OOD-ness.

## 5. Over/underclaims (line numbers)
- **Over.** Title (L2/L13) "the Cache It Cannot" — the full-transcript monitor mostly can (§4.3). L19/L37 "near-total capacity" leads with the near-tautological artificial edit. L170/174/211/260/268/310 "silently re-derive / under-counts a step's role / grows with capability" — unestablished vs recompute-from-prompt. L107 breadth ("×4 families up to 30B") is borrowed from a *different* prior experiment (2026-08-21-ird-fruit-battery) and concerns the copied-token channel, not the core results — risks implying the capacity/repair claims have that reach.
- **Under / exemplary honesty.** L19 scope line; §4.4; §6.1/6.3 free-running discount; §5.5 NF4 confound reported straight; L63/L370 VRAM figures labeled *asserted*; L375 manifest-amended-after-freeze disclosed (minor integrity ding: the "pre-registration" is not bit-immutable, though pre-reg remains the authority). The re-verbalization recovery (§4.3) is **underclaimed** — it's the constructive monitoring result and should be promoted, not hidden.

## 6. Figures & clarity
- **Fig 2** (repair vs scale): clear, two axes separated, 7B marked NF4, CIs, helpful callouts. Best figure. Only hides that each line is 2 points.
- **Fig 3** (token vs state): six bar-pairs all pinned at ~1.0 — visually content-free, reinforces the tautology worry. Replace with a table, or add the re-verbalization rate (0.66–1.00) as a third series — *that* has structure and carries the real message.
- **Fig 4** (free-running): clear, but visualizes the *discounted* panel; keep it flagged exploratory, out of main tables.
- **Fig 1** is a TODO placeholder (L97–99). A "submission manuscript" with a missing headline figure is not submission-ready — build or cut.
- Writing is strong but over-hedged: the scope caveat is restated ~5× (§4.3, §4.4, §7.1, §9, §10), diluting signal. Tighten.

## 7. Score and venue
**Overall 4/10.** Method and honesty are strong; the central causal claim is under-controlled and the domain too narrow to support a monitorability conclusion.
- **ICLR/NeurIPS main: reject** (needs the prompt-ablation control + natural reasoning + a non-NF4 large point).
- **Safety/interp workshop (SoLaR, interp): borderline-accept / weak-accept** — the exact-restore instrument, the state-vs-text framing, and the exemplary custody make it worth discussing; add the prompt control.
- **Would my team read/cite?** Read: yes. Cite the **exact-restore-gated state-vs-text dissociation method**: likely. Cite "silent repair rises with scale" as evidence of monitorability degradation: **not without the prompt-ablation control.**

## 8. Six ranked changes + three experiments
**Changes (ranked):**
1. Add the **repair-from-prompt control** (§2); until then soften §5/§7 to "answer recoverable after step removal, mechanism unresolved."
2. **Re-frame:** promote the full-transcript re-verbalization recovery (§4.3) to a headline; demote "near-total capacity" (it's a near-tautological max-strength edit).
3. Add a **bf16 7B point** (paged/offload — available) and **Qwen2.5-3B** if cacheable, so scale is >2 points and the top point is off the NF4-deflated axis.
4. Move the repair measurement to a **natural-reasoning dataset** (GSM8K-style), where operands aren't trivially in the prompt.
5. **Build or cut Fig 1; rework Fig 3** (add re-verbalization series / make a table); keep free-running out of main tables until a panel passes its own canary.
6. Cleanly separate **step-reading monitor** (zero recall is *by construction*, not a finding) from **full-transcript monitor** (recovers most); de-duplicate the scope caveats.

**Experiments (≤10 min, ≤7B, Qwen available) that would most change my mind:**
- **A — Repair-from-prompt (decisive).** Same admitted items: ablate the step's KV *and* mask attention to (or ablate) the operand/question tokens; measure residual repair at 0.5B/1.5B/7B. Collapse → benign recompute; persistence → genuine hidden re-derivation. Reuses the exact-restore gate.
- **B — Probe-based state monitor.** Fit a cheap linear probe on the cached state at the step position to decode the stored value; show it flags the state-only mismatch the text monitor misses. Operationalizes §7.3 and tests whether the "hidden" channel is actually dark to a *state-aware* monitor (if a linear probe reads it, it isn't).
- **C — Natural-reasoning repair with a bf16 7B point.** Re-run the ablation-repair curve on word problems with a bit-exact teacher-forced setup and a paged bf16 7B, with control A applied. Survives → I'm largely convinced; vanishes → the headline is a synthetic-arithmetic + NF4 artifact.
