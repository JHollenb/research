# Evidence and provenance

The paper synthesizes existing source and measured reports through October 30, 2026. Preparation used file inspection, JSON extraction, arithmetic checks and document validation only; it launched no scientific/model runs. This bundle supports reading and checking the reported summaries offline. It does not contain enough state to rerun training, native model forwards or the full receipt audits.

| Paper topic | Local evidence |
|---|---|
| Eleven-form starter and controller correction | [Starter report](starter-results.txt) |
| Six-model matched cohort, model state and training resources | [Selected raw report fields](six-model-summary.json); [figure data and timing provenance](../figures/README.md) |
| Operand invariance and older timing cohorts | [Runtime follow-up](runtime-followup.txt) |
| Selector/native-consumer boundary and unavailable hardware capture | [Inspection report](native-inspection.txt) |
| Early effects and unsuccessful C3b latent execution | [Early direct-effect report](early-direct-effect-results.txt) |
| R3 neural effects, exact counts and program outcomes | [Selected raw R3 fields](direct-effect-r3-summary.json) |
| Register/field pointers and coverage changes | [R4](r4-results.txt), [R5](r5-results.txt), [R6](r6-results.txt), [raw R7 report](r7-report.json) |
| SPF automata and FieldLM microcode | [Raw report](desf-report.json), [readable report](desf-account.txt) |
| Mamba scan/model parameter program | [Scan-lowering account](compiled-scan-account.txt) |
| Compact Boolean law, held exceptions, raw-bit route, eight-step loop | [Response atlas](mamba-response-atlas.txt), [route summary](mamba-route-summary.txt), [loop summary](mamba-loop-summary.txt) |
| Mamba source/encoding routes and conditional collateral repair | [Sequence account](state-transition-account.txt), [C/S restoration raw record](mamba-collateral-restoration.json) |
| Recipient-only MOV editor and independent saved-result audit | [Audit](nn-value-edit-audit.json) |
| Arithmetic editor transfer and its collateral exception | [Arithmetic account](arithmetic-edit-account.txt) |
| Assisted context cross and donor-free October 30 construction | [Crossed-context account](crossed-context-account.txt), [recipient-context account](recipient-context-account.txt), [raw report](recipient-context-report.json) |

`.txt` files preserve readable upstream reports as archival text. Their embedded original links describe the original workspace and are not this bundle's navigation; use the table above and the paper for local navigation. The reports distinguish source identities, direct observations and interpretation. Not every underlying tensor, test or receipt referenced inside them is copied.

`six-model-summary.json` and `direct-effect-r3-summary.json` are selected-field projections, not complete original JSON files. They retain values unchanged; omitted fields include large timing rows or probe/replay trajectories. Every projection names its original whole-file hash and transformation in [provenance.json](provenance.json). Full JSON snapshots and source snapshots have their own original and local hashes. The timing figure has a separate small provenance/data bundle.

Run the dependency-free local check from this directory:

```sh
rtk proxy python verify.py
```

It verifies local snapshot bytes against the manifest without opening the original workspace. A matching hash verifies identity of the copied evidence, not truth of a scientific claim or independent reproduction of a model result.

## Historical and working-tree identities

The inspected ISA repository's git HEAD is `0c529e1` from October 15, 2026. Much of the October 29–30 source and evidence is uncommitted. The manifest therefore binds individual bytes and modification times as well as the commit. Original paths are relative to the `domains` workspace, for provenance only. Modification times can reflect extraction, copying or later analysis rather than experiment execution dates. The latest included recipient/context findings have October 30 modification times; run identities and sealed reports determine the scientific specimens.

This account preserves distinct cohorts and authorities. The six-model study reuses the first four trained artifacts and newly times all six on matched ELF bytes. The earlier phase study, later neural direct effects, structural automata/microcode and frozen-symbol investigations are separate experiments. Symbol-study held/fresh examples do not automatically inherit original training-set quarantine. Derived counts and controls are not additional independent seeds.

## Delivery and audit limits

Some scientific runs completed before archive publication failed; their original output was recovered and verified without rerunning models. Some remote object-store publications remain queued while locally collected archives verify. These are delivery states, separate from model behavior. The snapshots retain the underlying accounts rather than rewriting historical scheduler failures into successes.

Automatic Saturn evidence sweeps cover declared streams and do not automatically validate semantic claims. Direct typed-receipt, saved-output, numerical and continuation audits supply additional scoped evidence. The paper reports their bounded conclusions; full trace stores, private runtime wheels, archives and checkpoints are excluded here. Terminal certification remains unassessed for the exploratory scientific claims.
