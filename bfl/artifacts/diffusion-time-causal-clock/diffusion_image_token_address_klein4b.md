---
schema: diffusion-image-token-address.v1
model: flux2-klein-4b
jobs:
  - job-d92d21f663d4
  - job-f026f4e39e27
status: exploratory-address-map
claim_status: spatial-addressability-and-redundancy-trend
---

# Diffusion image-token address map

## Result in one sentence

The image stream has a real native spatial address map, but color is not stored in one
image token: it is a distributed, time-integrated field with an uneven core and redundant
envelope. A 4x4 block leave-out experiment finds a strong spatial core in the upper-left
of this seed's latent grid, while single-token and block knock-ins fail to reproduce the
donor. The map is therefore useful for routing and graph construction, not yet a semantic
object map or evidence of a recovered training image.

## Instrument correction and native geometry

FLUX2 image token IDs are ordered as `(time, height, width, layer)`. The first version of
the probe read the last two fields as if they were `(height, width)`, which incorrectly
reported a `16x1` geometry in one assertion. The probe and the earlier spectral helper were
corrected to read `img_ids[..., 1:3]`. The successful reruns verify a 16x16 grid, row-major
flat indexing (`flat = row * 16 + col`), and native rows/columns from 0 through 15.

For visualization only, each token is assigned an approximate 16x16 pixel cell in the
256x256 decode. This is a coordinate correspondence, not a claim of exclusive pixel
ownership: attention, residual mixing, the packed latent transform, and the VAE spread
information across neighboring cells and channels.

The map montage is [`diffusion_image_token_address_map_klein4b.png`](diffusion_image_token_address_map_klein4b.png).
It shows the red and blue images with the native token grid, color/subject/scene activation
fields, block-only controls, representative-token controls, and the leave-one-block-out
return-alignment loss.

## Category fields are different spatial supports

At `joint.4` on the image stream, the probe measured the norm of the red-vs-blue, fox-vs-cat,
and snow/dawn-vs-desert/noon activation differences over four scheduler writes:

| category contrast | mean field norm | maximum | top-20 centroid `(row, col)` |
| --- | ---: | ---: | ---: |
| color | 61.98 | 122.11 | `(2.00, 2.65)` |
| subject | 79.37 | 131.70 | `(7.55, 7.30)` |
| scene | 131.45 | 198.12 | `(11.00, 6.85)` |

The top supports have little overlap. For the top 20 cells, color/subject Jaccard is
`0.026`, color/scene is `0.053`, and subject/scene is `0.053`; color and subject have zero
overlap in their top 10 cells. This is a useful trend toward separable category subspaces,
but it is not yet a stable semantic partition: it is one seed, one prompt family, one site,
and an activation field rather than a causal map.

The strongest color cells include `(row=3,col=4)`, `(2,4)`, `(1,2)`, `(3,1)`, and `(1,3)`.
The strongest subject cells concentrate around rows 8–12 and columns 4–14. The strongest
scene cells include a late lower field around row 14 as well as several mid-grid cells.
The category fields are therefore not simply “the image” or “the fox”; they are candidate
spatial supports for a future token-level hypergraph.

## Decoupling experiments

The block, representative-token, and line controls were performed at image `joint.4` with
donor norm equalized across their fixed supports. The permutation controls preserved the
donor field energy while rearranging its addresses. The full-donor and leave-one-block-out
controls use the raw donor field, so they provide the natural upper-bound and redundancy
comparison rather than another equalized-dose comparison.

### Single-token and block knock-ins

Replacing one representative token per 4x4 block never reproduced the full donor. Final
RGB mean absolute deviation (MAD) to blue stayed roughly `71.1–75.0`, and return-register
alignment was near zero or negative for many branches. Replacing an entire 4x4 block was
stronger but still incomplete: the best block was `block_3_1` at MAD `66.47`, while the
worst was `block_2_2` at `75.87`. The full image donor reached MAD `51.04` and return
alignment `0.876`.

This is the clearest decoupling result so far: a color-bearing direction exists in the image
stream, but it is not a single addressable slot. It needs a coalition of image tokens and
the repeated denoising writes that carry that coalition forward.

### Arrangement controls

The permutation controls preserved donor content while destroying or weakening its spatial
arrangement. Full donor transfer reached return alignment `0.876`; row shuffle reached
`0.502`, column shuffle `0.425`, and full grid shuffle `0.256`. RGB MAD was less orderly than
these latent measurements, which is itself informative: pixel distance can remain moderate
even when the returned latent points in the wrong direction.

The result supports native addressability. It does not support a simple pixel-copy story.
The model uses the spatial arrangement of the image-token field, but the field is interpreted
through learned mixing rather than copied cell by cell.

## Leave-one-block-out: what min/max flow was missing

The earlier diagnostic graph gave max flow `9.453015`, with the text stream contributing
`9.623356` of summed causal capacity and the image stream only `0.145942`. Because every
tested route was represented as a parallel source-to-sink path, the graph's leave-one-route
flow loss was mechanically equal to that route's own capacity. It could rank routes, but it
could not express redundancy among spatial tokens.

The native image-grid leave-out experiment adds that missing structure. With the full donor,
return alignment was `0.8757`. Omitting the upper-left 4x4 block (`block_0_0`) reduced it to
`0.7906`, a loss of `0.0850`, the largest loss in the 16-block sweep. Omitting `block_1_1`
reduced it to `0.8269`; omitting `block_3_3` reduced it only to `0.8650`, a loss of `0.0106`.

The color activation field predicts the causal leave-out loss with Pearson `r=0.782`. The
subject correlation is only `0.267`, and the scene correlation is negative in this run
(`-0.498`). That makes the color field a promising address-prioritization instrument: it
finds the blocks whose removal most disrupts the color direction, while the scene field is
not a proxy for the color circuit. A metric warning is important here: `block_0_0` had
RGB MAD `49.55`, numerically closer to blue than the full donor's `51.04`, even though its
return alignment was much worse (`.7906` versus `.8757`). Pixel MAD alone would rank this
causal degradation backwards.

This changes the flow interpretation. The model does not look like a set of independent
parallel routes; it looks like a spatial hypergraph with a high-value core and a redundant
envelope. The next graph should contain explicit text-site -> image-token edges, image-token
coalitions, checkpoint edges, and return-register consumers. Only then can min/max flow or
min-cut measure a meaningful spatial circuit rather than a bookkeeping capacity.

## What this does and does not establish

Established as an observation:

- image tokens have a recoverable native 16x16 coordinate system;
- color, subject, and scene contrasts produce different activation fields;
- spatial permutation changes the returned latent direction;
- color transfer is distributed across multiple image tokens and scheduler writes;
- some spatial blocks are more causally important than others in this seed.

Still open:

- whether these supports persist across seeds, prompts, sites, and model families;
- whether a stable field corresponds to a semantic object, a feature family, or merely a
  transport bottleneck;
- whether the field is low-rank/compressible in the SPF sense inside the native model;
- whether any internal direction reconstructs a training image or only a learned visual basis.

The strongest next experiment is a repeated-seed token-level hypergraph. Measure text-site to
image-token influence with matched knock-ins and leave-outs, then run coalition flow over the
stable edges. The result should be validated with return-register alignment, native RGB, and
checkpoint trajectories together; RGB MAD alone is too easy to fool.

## Reproducibility

- Probe: `mstack/experiments/diffusion_image_token_address_probe.py`
- Offline flow sensitivity: `mstack/experiments/diffusion_lexical_flow_sensitivity.py`
- Flow receipt: `mstack/results/diffusion_lexical_flow_sensitivity_klein4b.md`
- Raw v4 receipt: `mstack/results/diffusion_image_token_address_klein4b.json`
- CUDA jobs: `job-d92d21f663d4` and `job-f026f4e39e27`
