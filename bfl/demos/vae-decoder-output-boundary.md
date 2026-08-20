---
title: "VAE and Decoder Output Boundary"
type: experiment-report
status: compatibility-and-output-connectivity-trend
rank_in_bfl_survey: 14
model: "FLUX.2 decoder/VAE boundary"
tags: [bfl, flux, vae, decoder, compatibility, residual-debugging, output-boundary]
---

# VAE and Decoder Output Boundary

> [!summary]
> A Small Decoder removes 43.678% of decoder parameters and runs about 1.517× faster while preserving high image similarity: pixel cosine 0.999784 and PSNR 44.64 dB. Exact parity fails for all 192/192 tested outputs. A third-party MageFlow VAE reaches latent cosine 0.945507 and full-swap image cosine 0.999729. Residual-merge replay is exact until a one-pixel shortcut shift creates terminal L2 207.13. A 283-arm blind probe reaches the output in every tested arm, establishing an output-connected envelope but not semantic necessity or identity.

## Research question

The decoder/VAE is the boundary between a model's latent state and pixels. This experiment asks which properties of that boundary are required for compatibility, which substitutions preserve useful output geometry, and which internal perturbations are visibly connected to the final image. The goal is to separate “close enough for an application” from “exactly the same decoder” and from “this component owns a semantic feature.”

The panel has four parts: a Small Decoder compatibility comparison, a third-party VAE swap, residual-merge debugging, and a blind component probe. Each uses a native image output as the consumer and reports its own boundary. No single high cosine is treated as proof of exact equivalence.

## Small Decoder compatibility

The Small Decoder removes 43.678% of decoder parameters and is approximately 1.517× faster in the measured configuration. It reaches pixel cosine 0.999784 and PSNR 44.64 dB against the native decoder. Despite these strong application-level similarities, exact parity fails in all 192/192 tested outputs. This is the essential boundary distinction: a decoder can be highly compatible while remaining numerically non-identical.

The compatibility metric is computed on decoded images under a fixed latent and preprocessing contract. Pixel cosine captures directional image agreement, while PSNR reports average reconstruction error. Exact parity is a separate byte/numeric comparison and is intentionally stricter. The result supports using the Small Decoder where a bounded perceptual or pixel tolerance is acceptable, but not where exact reproducibility is required.

## Third-party VAE swap

The MageFlow VAE reaches direct latent cosine 0.945507 in the tested latent-space comparison. When swapped into the full decoding path, the resulting image reaches cosine 0.999729 against the native output. The gap between latent and image similarity is informative: the surrounding decode pipeline can absorb some representation difference, and image-level compatibility should not be inferred from latent cosine alone.

The swap is a one-latent, small-panel result. It demonstrates a compatibility crossing, not a proof that the third-party VAE preserves all image semantics, preprocessing conventions, or downstream gradients. A broader seed and distribution panel is needed for a terminal interchangeability claim.

## Residual-merge debugger

The residual-merge debugger replays substitution through `norm1`, `conv1`, `norm2`, and `conv2` and matches the native replay exactly under the declared inputs. A one-pixel-shifted shortcut donor changes the terminal L2 by 207.13. This sharp contrast shows that the decoder's residual geometry and shortcut alignment are part of the output contract; a seemingly small spatial indexing error can create a large endpoint difference.

The debugging result is useful because it localizes a class of failures without relying on a final image score alone. Intermediate substitution I/O and receipt records show whether the error is introduced at a merge, normalization, convolution, or terminal decode stage.

## Blind output-connectivity probe

The blind probe tests 283 arms: seven residual blocks and a complete 8×8 field of source perturbations. All 283/283 nonzero source perturbations reach the output; there are no silent arms in the tested envelope. Alternate-seed deltas are approximately 6× at `up_blocks.1`, 14–15× at `up_blocks.2`, 13× at `up_blocks.3`, and then about 0.04× in the decoder tail, while still remaining nonzero.

These magnitudes describe local norm expansion and output connectivity. They do not establish semantic amplification, necessity, or ownership. A component can transmit a perturbation to pixels without being the component that represents the concept being changed.

![Native and alternate decoder outputs](../artifacts/vae-decoder-output-boundary/native.png)

![Alternate decoder output](../artifacts/vae-decoder-output-boundary/alternate.png)

## Controls and limitations

The exact-parity count controls overclaiming from cosine/PSNR. The third-party swap separates latent compatibility from image compatibility. Residual replay controls arithmetic and merge alignment. The blind probe controls the opposite failure mode: assuming a component is silent because a coarse perturbation did not visibly change the image.

The Small Decoder and MageFlow results are compatibility claims on bounded panels. The blind probe is an output-connected envelope, not a semantic circuit map. The residual norm expansions can be influenced by normalization scales and local geometry. No result here establishes arbitrary latent interchangeability, training-time gradient equivalence, or semantic necessity.

## Claim status

**Observation:** multiple decoder/VAE substitutions preserve high image similarity without exact parity, and every tested nonzero residual probe reaches the output.

**Convergent trend:** compatibility metrics, exact-parity failures, residual replay, and blind output connectivity jointly locate a meaningful but non-identical output boundary.

**Working inference:** the decoder can be treated as a compatibility surface with measurable tolerances, while residual alignment remains critical for exact replay.

**Terminal status:** bounded compatibility and output-connectivity trend. It is not a claim of semantic decoder ownership or exact interchangeability.

## Local proof bundle

The bundle contains the Small Decoder report, third-party swap, residual-merge records, blind probe, and visual endpoints:

- [decoder report](../artifacts/vae-decoder-output-boundary/report.json)
- [residual substitution I/O](../artifacts/vae-decoder-output-boundary/component-substitution-io.json)
- [blind probe](../artifacts/vae-decoder-output-boundary/flux-blind-probe.json)
- [decoder-boundary index](../artifacts/vae-decoder-output-boundary/decoder-boundary-index.md)
- [bundle verifier](../artifacts/vae-decoder-output-boundary/verify.py)

Run `python ../artifacts/vae-decoder-output-boundary/verify.py` from this directory to verify compatibility, exact-parity, residual-shift, and blind-probe values.
