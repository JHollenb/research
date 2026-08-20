# Native-state FLUX route selector v6 analysis

This is an artifact-only analysis of the balanced, leave-family-out selector v6 report. The selector was compiled from earlier native `joint.1` state; development image labels were frozen before held-out dispatch.

## Saturn execution

- Rows: `106` across `22` immutable parent cuts.
- Selector raw feature matched the held-out native capture: `{'rows': 6, 'matches': 6, 'rate': 1.0}`.
- Native rewind exact: `True`; step suffix replay exact: `True`.
- Future Forest closure: `True`; reopened closure: `True`.
- Atlas/independent agreement: `{'agreement_rate': 0.9905660377358491, 'agreements': 105, 'rows': 106}`.
- Held-out outcomes visible at dispatch: `False`.
- Selector held-out outcome vector matched constant native continuation: `True`.
- Development/held-out seed sets disjoint: `True`; development seeds: `2`; held-out seeds: `2`.
- Development/held-out family sets disjoint: `True`; development families: `["negative_red_apples", "negative_red_squares", "positive_red_apples", "positive_red_squares"]`; held-out families: `["negative_green_triangles", "positive_green_circles", "positive_green_squares"]`.
- Selector abstentions: `2` with fixed margin `0.1`.
- Support policy: `standardized-nearest-development-native-state`, radius `8.115`, multiplier `3.000`; held-out dispatch rows with support telemetry: `6`, out of support: `2`.
- Selector schema identity: observed `saturn-native-state-route-selector-v6`, expected `saturn-native-state-route-selector-v6`, matches `True`; selector version `v6-calibrated-support-aware-three-route`.

## Development compilation

- Development examples: `8`; feature dimension: `32`; ridge lambda: `1.0`.
- Class balancing: `inverse-label-frequency`.
- Development fit accuracy: `1.000`; majority constant baseline: `native` at `0.750`; gain: `0.250`.
- Label distribution: `{"abstain": 0, "joint3_gain2": 1, "joint4_gain2": 1, "native": 6}`.

### Leave-one-family-out diagnostics

| Held-out family | Rows | Fit rows | Accuracy | Predictions | Labels |
|---|---:|---:|---:|---|---|
| `negative_red_apples` | 2 | 6 | 0.000 | `["joint3_gain2", "joint3_gain2"]` | `["native", "native"]` |
| `negative_red_squares` | 2 | 6 | 1.000 | `["native", "native"]` | `["native", "native"]` |
| `positive_red_apples` | 2 | 6 | 0.000 | `["native", "native"]` | `["joint3_gain2", "joint4_gain2"]` |
| `positive_red_squares` | 2 | 6 | 0.500 | `["native", "joint4_gain2"]` | `["native", "native"]` |

| Development action | Positive mean error | Positive exact | Negative mean error | Negative exact |
|---|---:|---:|---:|---:|
| `abstain` | 1.000 | 0.500 | 0.000 | 1.000 |
| `joint3_gain2` | 0.000 | 1.000 | 0.000 | 1.000 |
| `joint4_gain2` | 0.500 | 0.750 | 0.000 | 1.000 |
| `native` | 1.000 | 0.500 | 0.000 | 1.000 |

The image outcome is used only to compile the frozen development labels. The held-out worker receives the earlier native feature and sealed selector package, not the development utility.

## Held-out result — independent RGB evaluator

| Branch | Positive mean error | Positive exact | Negative mean error | Negative exact | Mean image MAD |
|---|---:|---:|---:|---:|---:|
| `fixed_joint3` | 0.500 | 0.500 | 0.000 | 1.000 | 9.402 |
| `joint4_control` | 2.500 | 0.500 | 0.000 | 1.000 | 8.361 |
| `native` | 1.500 | 0.000 | 0.000 | 1.000 | 0.000 |
| `selector_dispatch` | 1.500 | 0.000 | 0.000 | 1.000 | 0.000 |
| `selector_inverted` | 1.500 | 0.000 | 0.000 | 1.000 | 1.298 |
| `selector_wrong_time` | 1.500 | 0.000 | 0.000 | 1.000 | 0.000 |
| `selector_zero_state` | 1.500 | 0.000 | 0.000 | 1.000 | 0.000 |

## Held-out result — image-atlas evaluator

The atlas is an independent instrument, not a replacement for the RGB connected-component evaluator. Its disagreements remain visible below.

| Branch | Positive mean error | Positive exact | Negative mean error | Negative exact | Mean image MAD |
|---|---:|---:|---:|---:|---:|
| `fixed_joint3` | 0.500 | 0.500 | 0.000 | 1.000 | 9.402 |
| `joint4_control` | 2.500 | 0.500 | 0.000 | 1.000 | 8.361 |
| `native` | 1.500 | 0.000 | 0.000 | 1.000 | 0.000 |
| `selector_dispatch` | 1.500 | 0.000 | 0.000 | 1.000 | 0.000 |
| `selector_inverted` | 1.500 | 0.000 | 0.000 | 1.000 | 1.298 |
| `selector_wrong_time` | 1.500 | 0.000 | 0.000 | 1.000 | 0.000 |
| `selector_zero_state` | 1.500 | 0.000 | 0.000 | 1.000 | 0.000 |

### Selector decisions

| Held-out task | Seed | Selected action | RGB observed | Atlas observed | Expected |
|---|---:|---|---:|---:|---:|
| `green_circles_six` | 7001 | `abstain` | 5 | 5 | 6 |
| `green_circles_six` | 7002 | `abstain` | 5 | 5 | 6 |
| `green_squares_five` | 7001 | `native` | 3 | 3 | 5 |
| `green_squares_five` | 7002 | `native` | 3 | 3 | 5 |
| `green_triangles_three_negative` | 7001 | `native` | 3 | 3 | 3 |
| `green_triangles_three_negative` | 7002 | `native` | 3 | 3 | 3 |

### Evaluator disagreements

| Phase | Task | Seed | Branch | RGB count | Atlas count |
|---|---|---:|---|---:|---:|
| `calibration` | `red_circles_five_calibration` | 8002 | `joint4_gain2` | 4 | 2 |

### Atlas resolution sensitivity

The frozen image atlas nominally downsamples to `160×160`; this artifact-only audit repeats its hue-mask component count at larger resolutions. A count that recovers at full resolution is an evaluator-resolution issue, while a count that remains merged is a genuine rendered-geometry collateral effect.

| Seed | Branch | 160 | 256 | 384 | 512 |
|---:|---|---:|---:|---:|---:|
| 7001 | `native` | 5 | 5 | 5 | 5 |
| 7001 | `selector_dispatch` | 5 | 5 | 5 | 5 |
| 7001 | `fixed_joint3` | 5 | 5 | 5 | 5 |
| 7001 | `joint4_control` | 1 | 1 | 2 | 2 |
| 7002 | `native` | 5 | 5 | 5 | 5 |
| 7002 | `selector_dispatch` | 5 | 5 | 5 | 5 |
| 7002 | `fixed_joint3` | 5 | 5 | 5 | 5 |
| 7002 | `joint4_control` | 1 | 1 | 4 | 5 |

Held-out selector action distribution: `{"abstain": 2, "native": 4}`.

## Interpretation

The selector dispatched multiple actions on held-out parents: `{"abstain": 2, "native": 4}`. The full development fit is `1.000` versus `0.750` for its majority constant baseline, and the leave-one-family-out rows show whether that fit survives family separation.
The varied held-out dispatch is a trend toward state-dependent control, but its complete image-outcome vector matches constant native continuation: `True`. The selector therefore changes the route label without improving the downstream count result on this panel; the fixed joint routes outperform both policies on positive held-out error. Treat the route diversity as a promising native-state signal, not yet as useful orchestration.
The native feature, package round-trip, and Future Forest mechanics are instrument checks; they do not by themselves prove that the feature carries a semantic capability key.

## Calibration phase

The calibration phase contained `32` rows across `8` parent cuts and was completed before the Future Forest rewind that opened the green held-out phase.
The predeclared objective was `max-route-coverage-subject-to-calibration-collateral-cap` with maximum calibration false-positive rate `0.25`. The chosen support multiplier was `3.0` and radius `8.11496114730835`; held-out outcomes were not available to this decision.

| Multiplier | Radius | Route coverage | False-positive rate | Mean selected utility | Mean native utility | Safe | Actions |
|---:|---:|---:|---:|---:|---:|---|---|
| 0.5 | 1.352 | 0.000 | 0.000 | 0.750 | 0.750 | True | `{"abstain": 8}` |
| 0.75 | 2.029 | 0.000 | 0.000 | 0.750 | 0.750 | True | `{"abstain": 8}` |
| 1.0 | 2.705 | 0.000 | 0.000 | 0.750 | 0.750 | True | `{"abstain": 8}` |
| 1.25 | 3.381 | 0.000 | 0.000 | 0.750 | 0.750 | True | `{"abstain": 8}` |
| 1.5 | 4.057 | 0.000 | 0.000 | 0.750 | 0.750 | True | `{"abstain": 8}` |
| 2.0 | 5.410 | 0.000 | 0.000 | 0.750 | 0.750 | True | `{"abstain": 8}` |
| 3.0 | 8.115 | 0.500 | 0.000 | 0.750 | 0.750 | True | `{"abstain": 4, "native": 4}` |

The v6 serving policy was therefore frozen from calibration-only evidence as `{"abstain": 4, "native": 4}` on calibration parents. The new green held-out phase was then dispatched through that frozen package; its result is reported separately above and was not fed back into the policy.

The calibration result is an exploratory controller trend. It measures whether a separate utility-bearing split can open useful in-support coverage under a collateral cap; it does not establish that the state representation is semantic or that the policy transfers beyond these families and seeds.
