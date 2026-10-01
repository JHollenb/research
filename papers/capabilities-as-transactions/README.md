---
title: "Capabilities as Support-Aware Transactions: The Final Boss Is a Role, Not a Layer"
type: research-documentation
status: draft
updated: 2026-09-30
---

# Capabilities as Support-Aware Transactions

[The paper](paper.md) reports what happened when we hunted for "the final boss" — a single late circuit that commits a model's output — and found a transaction instead. A behavior, where it is a path-constituted object at all, is carried as an addressed, time-accumulated *joint* key/value (or residual) state and committed by an **unchanged native consumer** (the model's own next-token head, or its own scheduler and decoder). The "final boss" survives only as the **terminal consumer role** at the end of that chain, not as an anatomical location. The paper gives the cross-family dossier with denominators, the ways the transaction differs from a static circuit, the leverage, the honest leaks, and a blind auto-detection trial that produced a trend without a certificate.

"Final boss" is the author's working term; the paper defines it formally as the terminal consumer role and uses that definition thereafter.

## Files

- [`paper.md`](paper.md): the paper.
- [`figures/`](figures/README.md): the figures the paper relies on live in the companion papers, decoded from their bundled receipts; `figures/README.md` maps each to its receipt.

## Companion papers

This paper depends on, and cross-references, three companions in this repository:

- [Single-Site Tests Miss Distributed Stores](../pointwise-instruments-miss-distributed-circuits/paper.md) — the single-site-vs-whole-path instrument and its offline verifiers.
- [The Circuit That Survived Its Coordinates](../../bfl/docs/certified-semantic-circuits/paper.md) — the certified twenty-axis diffusion route, the time-accumulation result, and the portable CPU verifier for the induction circuit.
- [Integral Residual Dynamics](../integral-residual-dynamics/paper.md) — the trajectory-functional object and the four-quadrant certificate suite C1–C8.

## Evidence

Numbers that are bundled in a companion paper are cited by path and are authoritative there. Numbers that live only in the private experiment store are cited by job ID and marked as such; this paper does not copy private files into the public repository.

**Re-derivable from a companion bundle (authoritative):**

- Twenty-axis route panel (6 strict / 11 carrier / 3 candidate, two seeds): the `data/` and `experiments/` trees of the diffusion paper [above].
- Sink grid, cross-model slot write, kernel: `evidence/four-quadrant-tests/` in the distributed-store paper (`job-6650205b45eb`, `job-72f0e98679d5`, `job-6299f2391d5c`, `job-69e2f6a6b492`).
- Cross-model symbol table anchored authorship at native parity: `evidence/four-quadrant-tests/run-receipt-*-job-0706b0497903.json` and the anchored-parity panes in the distributed-store paper.
- Certified induction writer + portable CPU verifier: `verifier/verify_pythia_induction.py` in the diffusion paper.

**Evidence to bundle (candidate receipts; currently in the private experiment store, cited by job ID):**

| claim (paper section) | job ID(s) |
|---|---|
| autoregressive K/V causal chain: joint 4/4, K-only 0/4, V-only 0/4; joint-row-shift result 4/4 / full 2/4; P1-row-permuted-resid 4/4; terminal claim false (§3, §4, §6) | `job-a12ed4b56846` (`analysis/RESULTS.md`, `report.json`, `records.csv`) |
| G2 whole-model induction account: writer scope-2 R .871; 5-head scope-1 R .926 (§3) | `job-12c7fc70c022`, `job-b936245a2c2d`, `job-fbb7ea570ad5` |
| scene-edit certificate (§3) | `job-3cd13239dd91` (summary bundled in the distributed-store paper) |
| cross-checkpoint / cross-family portability (§3) | `job-17788d5a1b0d`, `job-638d05dcbff2`, `job-a676189574d1`, `job-f0edaded5d06` |
| hotpatch image edits (§5) | hotpatch-cinema run (no job ID declared in the source demo) |
| wall-picture edit (§5) | wall-picture hotpatch run (no job ID declared in the source demo) |
| value algebra + 9B port (§5) | object-multimodel battery (`job-e1ba0cbed889` and cohort) |
| donor-free writer / two-call composition (§5) | `job-3003b3a3be8b`, `job-c10dc83b3e25` |
| recipient-native counting patch, refuted for deployment (§6) | recipient-capability-patch run |
| coordinate/position map refuted (§4, §6) | `job-3980f89faa61` |
| instance binding not established (§6) | `job-47589b8693dc`, `job-6386d22db7c1` |
| retracted "clock" controller (§6) | `job-dfcb4146232b`, `job-8a18f3102d6f`, `job-25ee91384d15` |
| blind route rediscovery, best result (§7): target-edge recall 1.0 | `job-97708a5d46b8` |
| blind route rediscovery, adversarial (§7): recall 1.0, address-specific 0.333 | `job-dbf7448dc00e` |
| blind language-model final-boss, trend without certificate (§7): 0 certificate observations; wrong-depth 0.631; singleton necessity share 0.443 | `sequence-ab7695e26a8c` |

The blind auto-detection receipts (`job-97708a5d46b8`, `job-dbf7448dc00e`, `sequence-ab7695e26a8c`) and the K/V-chain receipt (`job-a12ed4b56846`) are result JSONs that the companion papers' convention allows bundling **after redaction** — the blind receipts embed absolute local filesystem paths in their `report` fields, which must be replaced with placeholders and their before/after SHA-256 hashes recorded in a `REDACTIONS.json`, per the convention in [the distributed-store paper's evidence bundles](../pointwise-instruments-miss-distributed-circuits/evidence/four-quadrant-tests/REDACTIONS.json). Because that redaction pass has not been run, they are cited by job ID here rather than copied. When bundled, each bundle ships a stdlib `verify.py` that re-checks file hashes and re-derives the headline verdicts (the four-quadrant gate fractions, the target-edge-recall values, and the failing-gate observed-vs-bar rows).

## Open placeholder

§7 ends with a placeholder subsection, **"Blind certification on FLUX.2 Klein 4B (in progress, 2026-09-30)"**, to be completed by the lead session running that experiment. It is marked as a placeholder in the paper.
