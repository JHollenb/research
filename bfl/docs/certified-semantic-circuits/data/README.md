# Data for "The Circuit That Survived Its Coordinates"

Raw result files behind the paper's held-out and follow-up numbers. The 20-axis discovery panel, its clean-room recheck, and the promptless controls are in the companion bundle [`bfl/artifacts/twenty-axis-semantic-route-circuit/`](../../../artifacts/twenty-axis-semantic-route-circuit/).

| folder | paper section | contents |
|---|---|---|
| `heldout-seeds/` | §4 | the full 20-axis panel rerun on unopened seeds 31337/60660: per-axis tiers, gate values, proof sheet |
| `mediation-steps/job-*/` | §4 | edge mediation for the six strict axes at denoising steps 0, 1 and 3 (17 of 18 cells hold) |
| `response-panel/` | §8.1–8.2 | the signal/response panel analysis, the linear-inverse controller, and the fitted second-order controller with its fixed-dose baselines |

Naming in the raw files: `carrier-certified` in the files corresponds to *route-certified* in the paper (passes the causal-route gates but not both strict pixel gates). Scheduler job IDs are kept so each file can be matched to its run record.

Host-specific paths and hostnames were replaced with placeholders after the runs; scalar results are unchanged. Original file hashes are listed in `REDACTIONS.json`.
