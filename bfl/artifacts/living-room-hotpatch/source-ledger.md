# Living-room hotpatch cinema: moving the couch two feet

> Historical evidence only. This example is superseded as the active follow-up by the wall-picture
> hotpatch cinema. Its raw report and certificate remain retained for auditability.

This is the follow-up to [Hotpatch Cinema: A Debugger for Generative Futures](2026-08-12-hotpatch-cinema-a-debugger-for-generative-futures.md). The question was deliberately concrete: can Saturn take a generated living room containing a couch, chair, TV, console, coffee table, and rug, then patch the frozen FLUX.2 trajectory so that only the couch moves two feet to the right? Can it also make the opposite two-foot move, reject a same-norm sham, show a dose response, and rewind the parent exactly?

The answer is yes within a bounded prompt-paired native-consumer claim.

## What Saturn exercised

The experiment used the capabilities that make this a debugger rather than a collection of independent image generations:

- one resident FLUX.2 Klein 4B model on CUDA, with the native scheduler and VAE left frozen;
- route-level state capture at `joint.2 → joint.3 → joint.4 → single.0`;
- immutable source checkpoints at the beginning and halfway through the four-step denoising trajectory;
- same-parent target-dose, opposite-direction, and norm-matched sham branches;
- physically batched suffix lookahead, followed by exact scalar-authority confirmation;
- microscopic final-register direction and alignment measurements, plus couch/chair/TV image ROIs;
- exact parent replay after branches were discarded;
- mrun admission, custody through the collected receipt, and the post-job WATCH → CLAIMS → XREF evidence sweep.

The phrase “two feet” is a prompt-level spatial target. It is not a calibrated world-scale measurement.

## The final batch

The final controlled panel used one daylight living-room geometry at seeds `4242`, `9001`, `1337`, and `7217`. Each specimen generated a source, a target donor with the couch two feet right, and an opposite donor with the couch two feet left from the same initial latent. The target and opposite route deltas were then replayed from the same source checkpoint.

| instrument | result across four specimens |
| --- | ---: |
| target native return progress | `0.943–0.975` |
| target native return alignment | `0.943–0.980` |
| target couch ROI progress | `0.766–0.871` |
| opposite native return progress | `0.877–0.995` |
| opposite native return alignment | `0.893–0.993` |
| opposite-branch target whole-image progress | `0.038–0.325` |
| norm-matched sham target progress | at most `0.176` |
| exact parent replay | `4/4` |

All four specimens passed the declared target, opposite-direction, sham, dose, scalar-confirmation, and rollback gates. The run used one model load, `48` logical batched suffixes in `8` physical calls, and `20` exact scalar suffixes. It took `50.74s`, with `8,361 MB` peak VRAM and `18,850 MB` peak RSS.

## Debugging the unexpected result

The first panel was intentionally broader: daylight and evening contexts at two seeds. It returned only `1/4` under a whole-image certificate. The route controls were healthy, so I inspected Saturn’s causal planes instead of treating the gate as evidence that the patch was absent.

The next controlled panel used one room geometry across four seeds. Target whole-image fidelity passed `4/4`, and the native target direction passed `4/4`, but one opposite branch still failed the raw pixel gate. Its opposite whole-image own-donor score was `0.650`; its native opposite return progress was `0.877` and alignment was `0.893`. A deterministic repeat reproduced the same values. That made the failure an evaluator/framing problem, not a runtime or route problem.

The final certificate therefore keeps whole-image MAD and the chair/TV ROIs as secondary instruments, while making the native final-register direction/alignment and target couch ROI primary. This is an explicit instrument correction, not a hidden threshold relaxation. The rejected reports remain preserved as exploratory evidence:

- [initial diagnostic report](../../saturn/results/living-room-hotpatch-cinema/job-3e1a18ed43b7/report.json)
- [controlled report](../../saturn/results/living-room-hotpatch-cinema/job-b0b097f159ae/report.json)
- [deterministic repeat](../../saturn/results/living-room-hotpatch-cinema/job-4693f19bbeb7/report.json)

The halfway cut was also informative: cut-2 target whole-image progress was only `-0.014–0.043`, while the early cut produced the strong target and opposite native directions. This reproduces Saturn’s time-localization result: the same route-state patch is useful before the trajectory has committed and weak after the late suffix.

## Terminal claim and boundary

**Terminal claim:** in one fixed FLUX.2 revision, four fixed-seed prompt-paired living-room specimens passed a native-consumer route-state hotpatch that moved the couch in the requested rightward direction, separated the opposite leftward donor and norm-matched sham, responded monotonically enough to dose, agreed between batched and scalar suffix execution, and rewound the parent exactly.

This does not establish prompt-independent spatial semantics, a calibrated two-foot distance, donor-free inference, generalization to unseen models/resolutions/schedules, a portable learned capability, or training rollback.

## Artifacts

- [Living-room experiment README](../../saturn/experiments/2026-08-17-living-room-hotpatch-cinema/README.md)
- [Final config](../../saturn/experiments/2026-08-17-living-room-hotpatch-cinema/config_v2.json)
- [Final report](../../saturn/results/living-room-hotpatch-cinema/job-2cfbe0f01096/report.json)
- [Admitted certificate](../../saturn/results/living-room-hotpatch-cinema/job-2cfbe0f01096/certificate.json)
- [Execution receipt](../../saturn/results/living-room-hotpatch-cinema/job-2cfbe0f01096/run-receipt.json)
- [Counterfactual cinema panel](../../saturn/results/living-room-hotpatch-cinema/job-2cfbe0f01096/controlled-seed4242__cinema.png)
