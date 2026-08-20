---
title: "Diffusion-Time Causal Clock, Character Pinning, and Image-Stream Roles"
type: experiment-report
status: native-consumer-temporal-editing-trend
rank_in_bfl_survey: 8
model: "FLUX.2 Klein 4B"
tags: [bfl, flux, diffusion-time, editing, identity, image-stream, causal-timing]
---

# Diffusion-Time Causal Clock, Character Pinning, and Image-Stream Roles

> [!summary]
> A temporal editing panel shows that the denoising step at which an intervention is installed determines whether it changes the final image. With fixed relative dose 0.15, a resume-at-k intervention has final relative effect 0.359 and amplification 2.399 at k=1 but only 0.078 and 0.523 at k=7, with a crossover near k=4. Whole-latent character pinning becomes reliable around k=4–6, and a regional intervention exposes an identity-versus-scene tradeoff. A native image-token address map further separates upstream carrier, bridge, semantic amplifier, and late terminal readout roles.

## Research question

Diffusion systems are often described as if an edit has a single strength independent of time. This experiment asks whether the denoising trajectory provides a causal clock: does the same relative state intervention have different downstream authority when installed at different resume steps? It then asks how that clock affects character identity, regional editing, and the roles of image-conditioned state sites.

The experiment has four parts: resume-at-k effect timing, a cheap-deep exactness control, character pinning, and regional sustained editing. A fifth analysis maps image-stream sites by replacing or intervening on them and measuring which endpoint properties move. The goal is not to propose a universal schedule, but to identify measurable temporal windows and distinguish identity transfer from scene preservation.

## Specimen and intervention

The specimen is FLUX.2 Klein 4B at 256×256 resolution. The base temporal panel uses an eight-step generation and a fixed relative input dose of 0.15. A resume-at-k branch starts from the saved state at step k, applies the same declared intervention, and runs the remaining native suffix. A control called cheap-deep computes the same state at each k with one forward pass instead of replaying the full prefix; its latent and image outputs are compared exactly against the reference implementation.

The character-pinning panel replaces the evolving latent with a reference character state at selected steps and measures identity similarity. The face identity remeasurement uses DINOv2 small CLS cosine over four scenes. Because this is a whole-image metric, it can reward composition and background similarity; the report keeps that confound explicit. The regional panel applies the reference state inside a spatial box while leaving the surrounding scene to the native trajectory.

## Resume-at-k results

The same relative dose has much greater final influence early in the trajectory. At k=1, final relative effect is 0.35981, pixel MAD is 12.9322, and amplification is 2.3986. At k=7, final relative effect is 0.0784, pixel MAD is 1.1853, and amplification is 0.5226. The effect curve crosses from amplification above one to attenuation below one near k=4.

The cheap-deep implementation is exact for every tested k. At k=7 it achieves a 7.993× speedup by using one forward pass rather than eight while preserving edit relative error 0.0. This matters scientifically because it makes dense timing sweeps affordable without changing the object being measured.

![Cheap-deep exactness and timing panel](../artifacts/diffusion-time-causal-clock/diffusion_cheap_deep_montage.jpg)

## Character identity and regional editing

Reference identity latent similarity rises from 0.295 at k=1 to 0.5423 at k=2, 0.9785 at k=4, 0.9982 at k=6, and 0.9992 at k=7. The same curve appears in two scenes, indicating a repeatable temporal transition for the declared character-pinning operation.

The four-scene face identity remeasurement gives DINOv2 CLS cosine k=1 −0.0209, k=2 0.1793, k=3 0.6966, k=4 0.9914, and k=6 0.9991. Across the four scenes, the persistence mean is 0.7913 versus −0.008 for baseline, and pairwise consistency is 0.722 versus 0.1351. These values establish a strong whole-image identity trend but not a face-crop identity guarantee.

Regional sustained replacement reveals a tradeoff rather than a free lunch. A box size 0.7 applied at steps 2–7 gives mean reference similarity 0.5249 and scene similarity 0.4107. A box size 0.5 applied at steps 2–4 gives reference 0.2011 and scene 0.7283. The smaller, shorter intervention preserves more scene while transferring less identity; the larger, sustained intervention transfers more reference content while disturbing more of the scene.

![Character pinning temporal curve](../artifacts/diffusion-time-causal-clock/character_pin_montage.jpg)

![Regional identity-scene tradeoff](../artifacts/diffusion-time-causal-clock/diffusion_regional_sustained_montage.jpg)

## Image-stream role map

The image-conditioned stream is not uniformly interchangeable. `joint.4:image` behaves as an upstream carrier with unit-dose progress approximately 0.445. `single.0:image` acts as a bridge and is the most reproducible scene carrier in the tested panel. `single.10:image` behaves as a semantic transport amplifier with progress approximately 0.589. `single.19:image` is a late terminal readout: absolute replacement reaches 1.000, but late interventions have less remaining denoising authority to reshape the full scene.

These labels are operational roles, not claims that a site owns one human semantic. They summarize the endpoint response under a defined replacement/intervention protocol. A carrier can be necessary for one consumer and merely correlated for another, so the role map should be read with its dose, time, and consumer conditions.

## Controls and limitations

Cheap-deep exactness controls implementation error in the temporal sweep. Repeated scenes control for a single composition. Baseline and pairwise comparisons expose the gap between identity transfer and generic image similarity. Regional boxes expose the identity-scene tradeoff. The image-stream role map uses address-specific interventions rather than activation inspection alone.

The panel is small and uses one model, one resolution, a limited number of steps, and a small seed set. Whole-latent replacement imports reference portrait composition, and whole-image DINOv2 can conflate identity with background. Zero effect late in the trajectory would not prove that a site is semantically irrelevant; it may simply be outside the remaining causal window. The claims therefore concern measured temporal authority under the declared native consumer.

## Claim status

**Observation:** identical intervention dose has a step-dependent effect, with a strong early-to-late attenuation; character pinning becomes reliable around k=4–6; regional editing trades identity for scene preservation.

**Convergent trend:** resume timing, exact cheap-deep replay, two-scene latent pinning, four-scene face remeasurement, and regional dose windows agree on a causal clock.

**Working inference:** diffusion-time state has a finite authority window, and image-conditioned sites occupy different positions in that temporal control hierarchy.

**Terminal status:** native-consumer temporal editing trend. This is not a universal timing law, a face-recognition benchmark, or proof that the role labels transfer unchanged to another model family.

## Local proof bundle

The bundle contains the temporal JSON records, image montages, and image-stream role map:

- [resume-at-k results](../artifacts/diffusion-time-causal-clock/diffusion_resume_klein4b.json)
- [character pin results](../artifacts/diffusion-time-causal-clock/character_pin_klein4b.json)
- [face identity remeasurement](../artifacts/diffusion-time-causal-clock/character_pin_faceid_klein4b.json)
- [image-token role map](../artifacts/diffusion-time-causal-clock/image-stream-control-buttons.md)
- [bundle verifier](../artifacts/diffusion-time-causal-clock/verify.py)

Run `python ../artifacts/diffusion-time-causal-clock/verify.py` from this directory to verify the reported timing, identity, regional, and role-map values.
