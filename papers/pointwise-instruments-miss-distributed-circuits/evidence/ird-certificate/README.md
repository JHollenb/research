# IRD Golden-Demo Artifact Bundle

Receipts and render panes extracted from the 2026-08-21 Wall A / IRD campaign in `~/domains/saturn/results/`. Source of truth remains the saturn tree; this bundle is a hash-pinned snapshot for the golden demo. Run `python3 verify.py` (stdlib only) to re-check integrity and re-derive the headline verdicts.

## Render panes (decoded from the reports' b64 payloads)

| file | job | what it shows |
|---|---|---|
| `anchored-parity-*-lion-s7217-job-0706b0497903.png` | job-0706b0497903 | anchored cross-model authorship: base scene, native-authored lion, SmolLM-feature-bridged lion, sham — bridged ≈ native at \|Δprogress\| ≤ 0.01 |
| `anchored-parity-*-wolf-s31337-job-0706b0497903.png` | job-0706b0497903 | same four arms, wolf, held-out seed |
| `zeroshot-negative-*-wolf-s31337-job-d8c971ba6e6f.png` | job-d8c971ba6e6f | zero-shot extrapolated authorship: bridged direction indistinguishable from sham (honest negative) |
| `kernel-{target,allsteps,steponly,late-double-dose}-lion-s7217-job-6650205b45eb.png` | job-6650205b45eb | front-loaded consumption kernel: step-0 write nearly reaches the all-step arm; late double-dose at equal nominal integral does not |

## Receipts (`run-receipt-*`)

| tag | job | leg |
|---|---|---|
| `v1-voided-refute` | job-0b95e9b4326d | full-space eval 0/54; frozen refute voided by span-confinement audit |
| `reading-35of54` | job-2f81d080712e | rank-40 displacement-subspace reading: 35/54 held-out vs chance 3/54 |
| `zeroshot-authorship-negative` | job-d8c971ba6e6f | consumer-leg negative: extrapolation reads but cannot render |
| `anchored-authorship-parity` | job-0706b0497903 | anchored symbols author at native parity |
| `k1-consumer-pass` | job-e26a9f22e328 | k = 1 native forward pass per symbol; all frozen bars pass |
| `symbol-class-battery` | job-9c6453d29ac1 | verbs read + author (swimming FULL PASS); relations item-independent; colors metric-floored |
| `relations-latent-probe` | job-6f4ee8adecd9 | content mirror fails to swap above/below; early pinning confirmed |
| `p4-crossslot-attempt1-log-custody` | job-0a07cb92d360 | P4 MATCH from log receipt after disclosed VRAM kill |
| `sink-certificate-and-kernel` | job-6650205b45eb | AR sink certificate issued + consumption kernel measured |
| `grid-4of4-and-p1-path-dependence` | job-72f0e98679d5 | grid 4/4 (color × Qwen2.5); zero-net-integral path dependence |
| `final-tests-attempt1-prior-confound` | job-88891036c1ee | scene-prior confound surfaced at Qwen3-8B |
| `final-tests-rerun-floor-instrument` | job-69e2f6a6b492 | amended prior-floor bar; cross-model ceiling parity; full report shipped |
| `token-time-kernel` | job-8a96572572cd | token-time point-read; full report shipped |
| `fp32-recheck-parity-0001-nats` | job-6299f2391d5c | fp32 disambiguator passes v2 bar; floor bias measured; full report shipped |

## Full reports shipped

Four small reports are included whole (`report-*.json`) so the verifier can re-derive verdicts without the saturn tree; the large symbol-table/IRB-kernel reports stay in `~/domains/saturn/results/` (their render panes and run-receipts are here).
