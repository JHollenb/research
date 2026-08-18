# FLUX.2 native interaction-residual panel

This is a derived summary of the immutable Saturn report in
`report.json`. The run used `black-forest-labs/FLUX.2-klein-4B`, revision
`e7b7dc27f91deacad38e78976d1f2b499d76a294`, native Qwen conditioning, 256×256,
four denoising steps, seeds `4242` and `9001`, and the route
`joint.2 → joint.3 → joint.4 → single.0`.

The panel had three deliberately diagnostic pairs and 17 scalar suffix
branches per pair/seed: 102 logical branch replays, one resident model load,
and no per-branch scheduler submissions. Worker time was 79.469 s; mrun
reported 91.72 s, 19,668 MB peak RSS, and 8,318 MB peak VRAM.

## Definition

For each native corner (`S`, `A`, `B`, `AB`) and route boundary/time:

```text
dA = A - S
dB = B - S
dAB = AB - S
IAB = dAB - dA - dB
```

The linear branch is `S + dA + dB`. The dose branches replay
`S + dA + dB + dose × IAB` through the unchanged suffix. Dose 1 and the
native `AB` donor are intentionally oracle/native-state controls: their exact
agreement does not constitute a learned compiler.

## Consumer response

Progress is RGB progress toward the native `AB` image, measured from the same
source image and source checkpoint.

| branch | mean | median | minimum | maximum |
|---|---:|---:|---:|---:|
| linear `S + dA + dB` | 0.3963 | 0.3591 | 0.1075 | 0.8269 |
| residual dose 0.25 | 0.5685 | 0.5633 | 0.3430 | 0.8851 |
| residual dose 0.50 | 0.6969 | 0.7102 | 0.4754 | 0.9071 |
| residual dose 0.75 | 0.8210 | 0.8255 | 0.7202 | 0.9348 |
| residual dose 1.00 | **0.9014** | 0.9071 | 0.8012 | 0.9747 |
| residual dose 1.25 | 0.8167 | 0.8312 | 0.6939 | 0.9098 |
| native `AB` donor | **0.9014** | 0.9071 | 0.8012 | 0.9747 |
| sign-flipped residual | 0.2655 | 0.2386 | −0.0008 | 0.6300 |
| residual shifted one step | 0.6573 | 0.6473 | 0.5592 | 0.7910 |
| residual shifted one route site | 0.4328 | 0.3869 | 0.1575 | 0.7904 |
| norm-matched random residual | −0.4010 | −0.3745 | −1.2802 | 0.1193 |
| interaction term alone | −0.0504 | −0.0465 | −0.2792 | 0.1138 |

The dose curve is the main new causal result. Adding the missing native
interaction term improves the frozen consumer across the panel, peaks near
the native dose, and degrades when overdriven. A wrong time or route boundary
retains some effect but loses substantial progress; a norm-matched random
residual does not explain the gain. The interaction term alone is not a
replacement for the first-order semantic changes.

The six cells, in pair/seed order, were:

| pair | seed | linear | dose .50 | dose 1.00 / native | wrong time | wrong site | sham |
|---|---:|---:|---:|---:|---:|---:|---:|
| identity + fur | 4242 | 0.5319 | 0.7396 | 0.9115 | 0.5592 | 0.3819 | −0.4755 |
| identity + fur | 9001 | 0.5128 | 0.6390 | 0.8012 | 0.6019 | 0.5461 | −0.2735 |
| lighting + weather | 4242 | 0.1931 | 0.6884 | 0.9267 | 0.6928 | 0.3918 | 0.0355 |
| lighting + weather | 9001 | 0.2055 | 0.4754 | 0.8916 | 0.6976 | 0.3289 | 0.1193 |
| orientation + relation | 4242 | 0.1075 | 0.7321 | 0.9027 | 0.6015 | 0.1575 | −1.2802 |
| orientation + relation | 9001 | 0.8269 | 0.9071 | 0.9747 | 0.7910 | 0.7904 | −0.5319 |

## Where the residual lives

The residual was nonzero at every captured route boundary and every step. The
following are means over all 24 boundary/time/pair/seed cells per boundary.

| boundary | mean `||IAB|| / ||dAB||` | mean `cos(dA+dB,dAB)` |
|---|---:|---:|
| joint.2 | 0.8200 | 0.7714 |
| joint.3 | 0.8752 | 0.7490 |
| joint.4 | 0.6022 | 0.8830 |
| single.0 | 0.6021 | 0.8834 |

The residual fraction by denoising step was 0.7599, 0.7576, 0.6967, and
0.6852. The exact algebraic reconstruction
`S + dA + dB + IAB = AB` had zero reported reconstruction error at the
captured states. Dose 1 and native `AB` produced image MAD 0.0 and identical
return-register metrics in every cell.

Applying the full residual at only one boundary gave mean `AB` progress of
0.3991 at joint.2, 0.3824 at joint.3, 0.4212 at joint.4, and 0.7920 at
single.0. This is evidence that the late return boundary has high consumer
leverage; it is not proof that single.0 is the unique producer of the
interaction term.

## Interpretation and boundary

This closes a causal separation, not a learned-composer claim:

1. The native `AB` state is substantially different from additive composition.
2. Supplying the missing native interaction term restores the native consumer
   response in a dose-dependent way.
3. Wrong timing, wrong boundary, sign reversal, and random-energy controls
   weaken or destroy the response.
4. Therefore the tested route can transport a valid joint state, while the
   construction of that state contains a non-additive interaction.

The experiment did not learn `IAB` from `dA` and `dB`, and it did not test
held-out semantic pairs or triples. The next experiment is a small
consumer-closed mixer trained on pair-disjoint combinations, with native
`AB` retained only as a teacher/reference and fresh held-out pairs kept out of
selection.
