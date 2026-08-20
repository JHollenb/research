---
title: "Closed-Loop Students and Reference Mappers"
type: experiment-report
status: bounded-native-parity-trend
rank_in_bfl_survey: 9
model: "FLUX.2 Klein 4B"
tags: [bfl, flux, closed-loop, student, mapper, reference-register, rollout]
---

# Closed-Loop Students and Reference Mappers

> [!summary]
> A compact student with a dense transition, patchwise reference register, uncertainty-gated correction bank, and native-action predictor reproduces native FLUX.2 behavior in teacher-forced and free rollout modes. The mapper has 3,768,459 parameters and scheduler parity cosine 0.9999981638. A full trajectory over 6,400 images reaches free image cosine 0.878103 mean and 0.743759 minimum, improving across later cuts. In a bounded performance lane, the reference-register student runs about 22.2–32.7× faster than native generation and reaches 0.960046 mean / 0.796 minimum free-rollout image cosine. Worst cases remain poor, so this is a strong closed-loop trend rather than a native replacement claim.

## Research question

Can a small learned transition model consume its own predicted state and continue a diffusion-like image trajectory without being rescued by teacher-forced reference states? This experiment evaluates that question at three levels: one-step mapper accuracy, free rollout over a long trajectory, and a bounded performance lane with prompt-disjoint evaluation.

The key distinction is between a teacher-forced emulator and a closed-loop student. Teacher forcing supplies the correct previous state at every step and can conceal compounding error. Free rollout feeds the student's own prediction back into the next transition. A useful student must remain on the native consumer's image manifold under this feedback loop, not merely match isolated transitions.

## Model and data contract

The specimen is FLUX.2 Klein 4B at 256×256 resolution, BF16 CUDA, revision `e7b7dc27f91deacad38e78976d1f2b499d76a294`. The mapper contains 3,768,459 trainable parameters. Its inputs are the current state, step metadata, reference patches, and uncertainty features. Its outputs are a dense state transition, a patchwise reference-register update, an uncertainty-gated banked correction, and a predictor for the native action consumed by the next step.

The complete mapper collection uses 1,200 teacher-forced and 1,800 free-rollout optimization steps over 4,800 transition samples. Scheduler parity is measured by cosine similarity between the student-side and native scheduler updates. The score is 0.9999981638, which controls one important numerical contract before image-level rollout is judged.

The longer trajectory contains 800 steps over 6,400 images. The bounded performance lane uses 24 prompts: 12 training prompts and 12 prompt-disjoint evaluation prompts. Its throughput comparison measures the same output contract for the native generator and the reference-register student. A separate audit distinguishes dense and uncertainty-gated mapper modes because the headline values are not interchangeable.

## One-step and trajectory results

The uncertainty-mode mapper free rollout has mean image cosine 0.750672 and minimum 0.066238 in its raw rollout panel. The dense audit reports mean 0.757, with all/dense/uncertainty means of 0.734, 0.757, and 0.751. A one-step closed latent cosine is 0.953. These values show that state-level agreement and image-level agreement are related but not identical; the lowest examples are materially worse than the mean.

The full 800-step trajectory is stronger: free image cosine is 0.878103 mean and 0.743759 minimum. By trajectory cut, the mean rises from 0.849561 to 0.866503, 0.883158, and 0.913191. The corresponding minimum rises from 0.743759 to 0.763277, 0.785953, and 0.831640. The upward curve is evidence that the student does not simply drift monotonically away from the native trajectory over the measured horizon.

[Full trajectory evidence](../artifacts/closed-loop-students-mappers/full-trajectory.json)

## Bounded performance lane

On the 24-prompt lane, the HybridReferenceRegisterStudent reaches approximately 80–89 images per second while native generation reaches 2.7–3.9 images per second, corresponding to 22.2–32.7× throughput improvement in the measured configurations. Free reference/edit rollout image cosine is 0.960046 mean with minimum 0.796. Teacher-forced image cosine is approximately 0.987.

The throughput rows must be interpreted carefully. Some wider-batch measurements reuse one captured input across the batch, so they establish a bounded repeated-input performance result rather than independent-prompt throughput at every row. The prompt-disjoint split is the more informative generalization check, while the full trajectory is the more informative closed-loop stability check.

## Why the result matters

A closed-loop student creates a possible separation between expensive native state generation and cheap repeated continuation. It can support rapid reference edits, interactive exploration, and large candidate sweeps if the student can preserve the consumer-relevant image contract. The experiment also provides a concrete way to measure where a student fails: scheduler parity, one-step latent closure, image-level rollout, trajectory cut, and worst-case examples are separate diagnostics.

The reference register is important because a simple low-dimensional recurrent state is not assumed to retain every spatial detail needed for image continuation. Patchwise reference access and uncertainty-gated correction give the student a way to recover local information without handing it the full native computation. That architectural choice is an experimental hypothesis, not a claim that the learned components are the only viable design.

## Controls and limitations

Teacher-forced versus free rollout controls compounding error. Scheduler cosine controls numerical update parity. Prompt-disjoint evaluation controls memorization of the training prompt set. Dense versus uncertainty-gated audit modes control for a hidden mode mismatch in the reported mean. The minimum scores keep the report from hiding failure behind an average.

The worst examples are poor enough that the student is not a drop-in native replacement. Latent/VAE closure is incomplete, and the performance lane's reused-input rows do not establish fully independent prompt throughput. The student is trained against a bounded specimen and native action contract; portability to other model families, resolutions, or conditioning regimes remains untested.

## Claim status

**Observation:** a 3.77M-parameter reference-register student can remain usable under free rollout and can run substantially faster than native generation in a bounded lane.

**Convergent trend:** scheduler parity, one-step closure, long free rollout, improving trajectory cuts, prompt-disjoint evaluation, and throughput measurements all support consumer-relevant compression.

**Working inference:** patchwise reference state plus uncertainty-gated correction is sufficient to preserve much of the native image trajectory for the tested task, while avoiding the full native compute cost.

**Terminal status:** bounded closed-loop and performance trend. It is not a universal native replacement, not a proof of independent-prompt throughput at every batch size, and not a guarantee on the worst-case tail.

## Local proof bundle

The bundle contains mapper and full-trajectory JSON records, receipts, trajectory visuals, and the performance reference:

- [mapper report](../artifacts/closed-loop-students-mappers/mapper-complete-v3.json)
- [full trajectory report](../artifacts/closed-loop-students-mappers/full-trajectory.json)
- [performance reference](../artifacts/closed-loop-students-mappers/black-forest-labs-performance-reference-2026-08-11.md)
- [bundle verifier](../artifacts/closed-loop-students-mappers/verify.py)

Run `python ../artifacts/closed-loop-students-mappers/verify.py` from this directory to verify the parameter count, scheduler parity, free-rollout means/minima, trajectory cuts, and bounded speedup.
