# Four-Quadrant Test Receipts

Run records, full reports and render panes behind §4 of [Single-Site Tests Miss Distributed Stores](../../paper.md). Run `python3 verify.py` (standard-library Python, no GPU) to check every file hash and re-derive the paper's headline values from the reports.

## Full reports

| file | paper section | contents |
|---|---|---|
| `report-lm-necessity-and-write-schedule-job-6650205b45eb.json` | §4.2, §4.3 | SmolLM2-1.7B identity necessity arms (single layer, halves, all layers); FLUX.2 write-schedule arms and their render panes |
| `report-lm-grid-job-72f0e98679d5.json` | §4.2 | SmolLM2-1.7B color and Qwen2.5-0.5B identity/color necessity and sufficiency arms |
| `report-final-tests-rerun-job-69e2f6a6b492.json` | §4.2 | SmolLM2-1.7B action cell; Qwen3-8B identity/color cells and their no-subject floors; a cross-model write check |
| `report-final-tests-attempt1-job-88891036c1ee.json` | §4.2 | first Qwen3-8B attempt, where the no-subject confound was found |
| `report-fp32-recheck-job-6299f2391d5c.json` | §4.2 | fp32 rerun of the Qwen3-8B identity cell with three filler words |
| `report-token-time-kernel-job-8a96572572cd.json` | §6 | token-axis ablations (scene-suffix effect ≈ 1% of the subject effect) |

## Render panes

| files | what they show |
|---|---|
| `kernel-{target,allsteps,steponly,late-double-dose}-lion-s7217-*.png` | fox → lion writes at all steps (progress 0.73), step 0 only (0.13, still a fox), and steps 2–3 at double dose (0.16, a lion in a different pose). Progress is pixel reproduction of the target render, not identity (paper §4.3). |
| `anchored-parity-*`, `zeroshot-negative-*` | a related cross-model write experiment not used in the paper's claims: a direction computed from one model's text features renders the target animal when anchored to a matched example, and fails when extrapolated to unseen animals |

## Run records

The `run-receipt-*.json` files are the scheduler's records for each job (command, worker hash, model path, environment, exit state). Their names follow the internal experiment log and are kept so each file can be matched to its job ID.

Host-specific paths and hostnames were replaced with placeholders after the runs; scalar results are unchanged. Original file hashes are listed in `REDACTIONS.json`.
