# Round-2 response

**Decision accepted.** The paper is **parked as a record** (round-2 monitoring review 4/10, fold
recommended). Its content will likely fold into the companion paper (Paper 2). We did not attempt a
further defense; we applied only the evidence-accuracy fixes from `round2-evidence-audit.md` so the
parked record is correct. No scientific claim changed.

## Reviewer verdict

The round-2 monitoring reviewer recommends folding Paper 4 into the companion paper rather than
standing it alone at workshop scale. We agree: after Control A confirmed the central round-1 concern
(the removal effect is recompute-from-prompt, not a hidden channel), the standalone contribution is
one solid pre-registered dissociation (E2) plus one honest negative (the probe). That is better
placed as a section in Paper 2 than as a separate note. The record is kept here so the measurements,
controls, pre-registrations and retraction are preserved.

## Evidence fixes applied (from the round-2 audit)

- **MF1 (must-fix). 3B text-visible was never measured.** The only 3B run is the control worker
  `job-52b8771fc5ef`, whose report has no text-visible field; the dissociation panel never ran 3B.
  Table 1 3B text-visible cell is now `n/a`. "1.00 everywhere" (§4.2) softened to "1.00 on every row
  where it was measured (not measured at 3B)". Appendix C and README C6 softened identically. The 3B
  state-only point (1.00) is real and retained.
- **F2 (flag). 3B state-only provenance.** Added a note under Table 1: the 3B (base) state-only
  point comes from the control worker's `swap_changed` (job-52b8771fc5ef, worker rev 3b4db8d2,
  pre-resample), not the main 2×2 panel; equivalent by definition.
- **F3 (flag; source file). Stale cancelled job id.** `FINDINGS-addendum-2-draft.md:36` named the
  cancelled `job-366e400ba3aa`; corrected to the live `job-050706578e6c` (minimal edit). The paper
  already used the live id everywhere (0 hits on the cancelled id in `paper.md`).
- **F5 (minor). Fig F1 title.** Regenerated `figures/figF1_free_running.png` (was a copy of the EXP
  figure) with the pre-correction suptitle "removal is silently repaired & unspoken" removed; new
  title reads "ablation recomputes from the prompt; injected state is re-verbalized". The green bar
  is relabeled "answer still correct (recompute)". Bar values unchanged and match Appendix F.
- **F6 (minor). Mislabeled denominator.** The "Note on n" (§4.2) attributed the 1.5B-NF4 repair
  denominator (0.292, n=24) to "Section 7"; it is the Appendix G precision control
  (`job-4a5981fa28fc`). Relabeled.

**F4 (flag, no change).** Fig 2 (VM trace) and Appendix E (prior battery) are from experiments
outside this audit's source set; both are verified against their own sources and disclosed in
Appendix A/E as separate and not custody-audited. No defect; nothing changed.

## Status

README status set to "Parked 2026-10-02 after round 2 (4/10, fold recommended)" with a header note
pointing here. No commits made by the author agent; the coordinator owns commit and the fold into
Paper 2.
