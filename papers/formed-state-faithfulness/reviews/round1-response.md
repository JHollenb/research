---
title: "Round-1 response — Two Channels of a Reasoning Step (formerly Formed-State Faithfulness)"
author: Jacob Hollenbeck
date: 2026-10-02
scope: response to round1-monitoring-reviewer.md, round1-evidence-audit.md, round1-priorart-clarity.md
---

# Round-1 response

Thank you to all three reviewers. The two substantive reviews converged on the same two asks — (1) the
silent-repair result is under-controlled against recompute-from-prompt, and (2) the paper led with the
artificial capacity result and buried the natural one — and we have rebuilt the framing around both.
Four controls are running (A repair-from-prompt, B probe monitor, C bfloat16-7B + 3B, D natural
problems); where a fix needs data we have placed an explicit in-text placeholder and softened the
claim to what is measured. Legend: DONE / DONE-partial / RUNNING / DECLINED(reason).

## A. Monitoring reviewer (overall 4/10) — the central objection

**A1. Repair-from-prompt confound (your §2, decisive).** AGREED; this is the most important change.
DONE (framing) + RUNNING (control). Section 5 now states plainly that ablating only the step's span
leaves the operands in the prompt and cache, so a recovered answer may be benign recompute-from-prompt
(monitor reads the same operands) rather than hidden re-derivation, and that the two readings have
opposite monitoring implications. We cite your own "tell" (state-only flips 100% with no room to
regenerate; ablate-then-generate recovers more with scale because the model is given room to recompute)
in §5.1. Every flagged sentence — old L170, L174, L211, L260, L268, L310 — is softened from "silently
re-derive / under-counts a step's role / grows with capability" to "removing the step's cached state is
increasingly compensated at larger scale," and "both models used it" is removed. §5.6 now says the
present, defensible claim is ablation-metric robustness (single-site removal under-measures a step's
effect, more so with scale), and that the monitorability reading waits on Control A. The decisive
experiment you specify (ablate step + cut operand access; converse arm; sanity arm) is `TODO A` in §5.1
and is running; we commit to revising the framing to whichever way it falls.

**A2. Capacity is near-tautological; "capacity" oversells (your §3).** AGREED. DONE. "Near-total
capacity" is retired as a headline. §4.2 is retitled "The hidden-state channel is load-bearing (a
maximal edit)" and now says explicitly that the forward pass runs on the cache, so the state-only flip
is close to a sanity check and we read it as confirming the answer region *uses* the step's stored
state, not as a capacity number in any information sense. The word "capacity" no longer appears as a
claim.

**A3. The re-verbalization recovery is the policy-relevant result and is buried (your §3, §5).**
AGREED. DONE. It is promoted: §4.3 is now a full subsection with the per-arm recovery fractions
(0.66-1.00), Figure 3 carries it as a third series, and both the abstract and the contributions state
that a full-transcript monitor recovers most. §7.1 separates the step-reading monitor (zero recall, now
stated as *by construction*, not a finding) from the full-transcript monitor.

**A4. Evidence is thin for a main-venue monitorability claim.** AGREED; we have re-scoped to
workshop-ready with main-venue pending controls (frontmatter `venue_target`). RUNNING: bfloat16-7B via
paged execution and Qwen2.5-3B (`TODO C`, your change 3); natural reasoning (`TODO D`, your change 4);
repair-from-prompt (`TODO A`). DONE: free-running is now explicitly exploratory and both arms discounted
by their own canary (we had only discounted 7B before — the evidence auditor and you are right that 1.5B
at 8/9 = 0.889 is also below the frozen 0.90). Two-points-per-axis is stated in the Fig 2 caption and
§9.

**A5. Mean-ablation OOD (your §4 secondary).** DONE (disclosed) + future work. §9 now notes mean-ablation
may push the cache off-distribution, so "repaired vs not" partly conflates "step unneeded" with "mean
landed near a valid state," and that a zero/resample-ablation comparison would harden §5.

**A6. Over/underclaims by line (your §5).** DONE. Title changed (see C1). "near-total capacity" demoted
(A2). The repair sentences softened (A1). §3's "×4 families up to 30B" is now explicitly flagged as a
*separate prior battery* on a different task/models and moved to a one-paragraph §3 + Appendix E, so it
cannot be read as reach for the core claims; it is also removed from the limitations sentence.

**A7. Figures (your §6).** DONE. Fig 1 is built (static two-lane schematic with the three
interventions), not a placeholder. Fig 3 gains the re-verbalization/recovery series. Fig 4 is demoted to
Appendix F. Scope caveat reduced to two substantive statements (§4.4, §9).

**A8. Your three experiments.** All adopted as the running controls A (repair-from-prompt), B (probe-based
state monitor, now `TODO B` in §7.3), C (natural reasoning + bfloat16-7B). We agree these are what would
move the score and we are running them.

## B. Evidence audit (custody clean; 10 fixes) — all applied

1. README abstract dropped the discounted 11% free number. DONE.
2. Table 1 vs Table 2 n (1.5B NF4 21/23/24) explained in a table note under Table 1. DONE.
3. Table F1 (free) 7B header n=9 vs 8 scored footnoted. DONE.
4. §3 provenance stated inline (prior battery, different task/models) + Appendix E. DONE.
5. Text-only cell now reported (§4.1): 0.47/0.56 at 0.5B, 0.00 at 1.5B, 0.10 at 7B — and it is a nice
   scale signal (token pull falls, state dominates with scale). DONE.
6. Fig 2 caption "overlap" softened to "sit on or near," noting the 1.5B float32 diamond at 0.83. DONE.
7. Appendix C E3 row tagged discounted. DONE.
8. VRAM figures labeled asserted at first mention (§2.2), not only the appendix. DONE.
9. README status made consistent (audit complete). DONE.
10. Superseded primary `fig1_repair_vs_scale.png` confirmed unreferenced in paper.md. DONE.

Thank you for the independent recompute; the common-subset and re-verbalization rows matching our raw-row
recomputation is the check we most wanted.

## C. Prior-art / clarity reviewer

**C1. Title + re-lead.** DONE. Title is now your option B, "Two Channels of a Reasoning Step: The Token a
Monitor Reads and the Cache It Does Not," chosen because it stays accurate whichever way Control A falls
(it names the dissociation, which does not depend on the repair mechanism), where option A's "under-measures
its role" would be false if A shows benign recompute-from-prompt. Abstract and intro now lead with the
natural silent-repair scale result (common-subset 0.095→0.762), then the dissociation, then the
full-transcript recovery, close to your suggested abstract.

**C2. Self-repair literature uncited (your #1 objection).** AGREED; this was the conspicuous gap. DONE.
§5.6 and §8 now position silent repair as a reasoning-step-grain, scale-and-quantization-quantified
instance of the self-repair / Hydra family: McGrath et al. 2023 (2307.15771), Rushing & Nanda 2024
(2402.15390), with Bugaud 2026 (TrustNLP 2026, as in Paper 1) as the contrasting "corrupt-easily-repair-
rarely" datapoint. The honest delta (grain, scale/quant quantification, monitorability framing) is stated.

**C3. Implicit/latent reasoning uncited.** DONE. §8 adds Yu 2024 (2411.15862), Yang et al. 2024
(2402.16837), Biran et al. 2024 (2406.12775, back-patching 32-66%). Radhakrishnan et al. 2023 (2307.11768)
added to the §7.3 recommendation. All IDs web-verified; none invented.

**C4. Paper-1 overlap.** DONE. §8 now cites Paper 1 for the *existence* of the repair phenomenon and the
E10 numbers, and gives a sharp new-contribution list (scale curve + 0.5B anchor + 7B; fp32/NF4 controls;
token-vs-state 2×2; re-verbalization/full-transcript analysis; monitorability framing). We agree Paper 1's
§8 should be trimmed to a pointer; that is a note for the Paper-1 authors and we have not edited Paper 1.

**C5. Structure/length.** DONE. §3 compressed to one paragraph + Appendix E; §6 compressed and its table +
figure moved to Appendix F; §4.4-4.6 merged into one subsection; the step-vs-full-transcript scope stated
twice (§4.3, §7.1) rather than four times. Body is ~40 KB (~10 pp).

**C6. Jargon/definitions.** DONE. "Formed state" is defined in the first sentence of §2 as the K/V cache
written at the step positions. "monitor-blind" renamed to "written-step-blind" in abstract, Table 1, Fig
3, and §7 (zero occurrences of the old term remain). "remount" was already absent from the body.

**C7. Figures.** DONE, as in A7 (Fig 1 built, Fig 3 recovery series, Fig 4 to appendix).

## D. What still depends on the running controls

The paper is honest that the headline monitorability reading of Section 5 is pending Control A, and that a
bfloat16 large point (C) and natural problems (D) are needed for a main-venue claim. We will fold their
results, and any further corrections, into round 2 with a changelog. We did not change any measured number;
the custody audit confirms the point estimates, and this revision is entirely framing, scope, prior art,
figures, and structure.

---

# Round-2 update (controls landed) — central flaw conceded

The decisive control the monitoring reviewer asked for (A: ablate the step **and** cut operand
access) has run, and **the reviewer was right.** We concede the central flaw explicitly and have
rebuilt the paper around it.

- **E1 "silent repair" is recompute-from-prompt, not a hidden channel.** With operands
  attention-masked, post-ablation repair collapses wherever the cut is non-destructive: 0.188→0.000
  (0.5B, sanity 1.000) and 0.531→0.031 (3B, sanity 1.000). The non-destructive resample control
  confirms it: the model never reproduces the original answer once the operands are changed
  (tracks-original = 0.000 at 0.5B and 1.5B); it tracks the new visible operands. At 1.5B the mask
  was destructive (sanity 0.571), so the resample control carries the verdict there (a partial pass:
  R4 = 0.450 misses the R1−0.15 bound, but still recompute-from-prompt). We have **retracted** the
  "silently re-derive / grows with capability" reading; the rate is not even monotone
  (0.188/0.762/0.531) and the 3B point is a base model. E1 is now presented as a *dispensability*
  caveat for removal-based attribution (Section 7), exactly as the reviewer characterized it.
- **We re-led with the dissociation, not the artificial capacity edit**, per the clarity reviewer —
  but demoted even further: the title is now "The Answer Follows the Cache," and the state-only swap
  is stated plainly as an *injected* dissociation (it shows the hidden channel *can* override the
  token), with the full-transcript re-verbalization recovery kept.
- **The probe (control B) is a negative, reported as one.** The reviewer's suggestion to test a
  state-aware monitor was the right instinct, but our single-layer linear probe did **not** clear its
  pre-registered swap-decode bar (0.19/0.19/0.00 < 0.70). The looser 0.84-0.97 flag is exploratory
  only (no false-positive rate; ridge penalty tuned on the evaluated items). We do **not** headline
  "monitor the cache"; a layer-swept, held-out probe is future work.
- **Remaining asks honored as scope:** natural-task reasoning (the reviewer's domain-breadth point)
  is named as the main open gap (TODO D); a clean 7B-Instruct bf16 point is pending (job-050706578e6c).

Net: the paper is now a workshop-scale note with one solid pre-registered result (the injected
token-vs-state dissociation) and two honest negatives (E1 = dispensability; the probe missed its
bar). We thank the monitoring reviewer; the operand-cut control changed our conclusion.
