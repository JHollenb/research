# Figures — Single-Site Tests Miss Distributed Stores

Each figure lists the receipt bundle it is decoded from. Paths are relative to this paper's folder.

| File | Figure | Data / receipts |
|---|---|---|
| `fig1-single-step-patching.png` | Fig 1. Single-component, single-step interventions at step 2 in FLUX.2 Klein 4B (sufficiency / necessity / rescue panes); the same four components across all steps remove (0.13% remaining) or carry (91.1%) the transition. | `evidence/four-quadrant-tests/` (render panes + four-quadrant receipts; `python3 verify.py` re-derives the headline values). |
| `fig2-write-schedule.png` | Fig 2. Write schedule vs outcome for fox → lion (seed 7217); "progress" is 1 − pixel MAD to the target render, showing it measures target-image reproduction, not identity. | `evidence/four-quadrant-tests/` (write-schedule receipts, §4.6). |
| `fig3-probe-vs-consumer.png` | Fig 3. Case 2: native fox run; foreign-text-encoder run (probe reads "no animal"); the two subject rows transplanted into the native fox run (renders a wolf); native wolf reference. | `evidence/instrument-trial/` (blind-graded comparison; `instrument-trial-verify` re-checks every receipt hash). |

No new figures are required by the 2026-10-05 pass; the §4.7–§4.8 additions are text (numbers 0.99 vs 0.00 and 1.0–1.5% → 172–236%) and need no figure.
