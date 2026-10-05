# Native surface delta findings

This generated note decodes retained native affine surface blobs. It is a model-free geometry report and does not certify role emergence.

* Report SHA-256: `b8d1c7986437af4d3bde8ada6b008ac3238b46b6632f192794adf7be89d44a9c`
* Request SHA-256: `2bec66baf8b191693ba35a35c1677110209661919899f3bd25a68924a6991e86`
* Future Forest archive SHA-256: `69caaddf119f959f5c77266051772e514fe8afd4ce9920f85016832752528f78`
* Decoded candidate surfaces: `24`

## Dose table

| family | arm | interval | promoted | ΔW L2 / parent L2 | ΔW RMS | object hash |
|---|---|---:|---:|---:|---:|---|
| mamba | matched_depth | 0 | yes | 0.000966318 | 0.000499821 | verified |
| mamba | matched_depth | 1 | yes | 0.000458138 | 0.000236968 | verified |
| mamba | matched_depth | 2 | yes | 0.000222406 | 0.000115038 | verified |
| mamba | matched_depth | 3 | yes | 0.000108981 | 5.63694e-05 | verified |
| mamba | operation_label_swap | 0 | yes | 0.000794592 | 0.000499801 | verified |
| mamba | operation_label_swap | 1 | yes | 0.000380156 | 0.000239119 | verified |
| mamba | operation_label_swap | 2 | yes | 0.000188526 | 0.000118583 | verified |
| mamba | operation_label_swap | 3 | yes | 9.39691e-05 | 5.91068e-05 | verified |
| mamba | writer | 0 | yes | 0.000794569 | 0.000499787 | verified |
| mamba | writer | 1 | yes | 0.000375924 | 0.000236457 | verified |
| mamba | writer | 2 | yes | 0.000186073 | 0.00011704 | verified |
| mamba | writer | 3 | yes | 9.27611e-05 | 5.83469e-05 | verified |
| qwen | matched_depth | 0 | yes | 0.0158933 | 0.000499955 | verified |
| qwen | matched_depth | 1 | yes | 0.00740794 | 0.000233074 | verified |
| qwen | matched_depth | 2 | yes | 0.00359622 | 0.000113166 | verified |
| qwen | matched_depth | 3 | yes | 0.0017662 | 5.55844e-05 | verified |
| qwen | operation_label_swap | 0 | retained/rejected | 0.0149942 | 0.000499974 | verified |
| qwen | operation_label_swap | 1 | retained/rejected | 0.00749711 | 0.000249987 | verified |
| qwen | operation_label_swap | 2 | retained/rejected | 0.00374855 | 0.000124993 | verified |
| qwen | operation_label_swap | 3 | retained/rejected | 0.00187428 | 6.24967e-05 | verified |
| qwen | writer | 0 | yes | 0.014993 | 0.000499933 | verified |
| qwen | writer | 1 | yes | 0.00717421 | 0.000239247 | verified |
| qwen | writer | 2 | yes | 0.00350107 | 0.00011677 | verified |
| qwen | writer | 3 | yes | 0.00172208 | 5.74405e-05 | verified |

## Writer versus wrong-label geometry

The table reports exact cosines and component doses decoded from the retained parent/candidate blobs. A shared update direction remains a geometric observation, not evidence that the wrong-label arm learned the same semantic role.

| family | interval | wrong-label / writer ΔW L2 | whole ΔW cosine | components (dose ratio; cosine) |
|---|---:|---|---|---:|---|
| mamba | 0 | 1.00003 | 0.435782 | dt_proj.bias×0.9999/0.3207, dt_proj.weight×1/0.284, x_proj×1/0.5278 |
| mamba | 1 | 1.01126 | 0.459134 | dt_proj.bias×1.003/0.3424, dt_proj.weight×1.021/0.2934, x_proj×1.006/0.5539 |
| mamba | 2 | 1.01319 | 0.456206 | dt_proj.bias×1.006/0.3432, dt_proj.weight×1.021/0.284, x_proj×1.009/0.5546 |
| mamba | 3 | 1.01302 | 0.451446 | dt_proj.bias×1.007/0.3401, dt_proj.weight×1.019/0.2745, x_proj×1.009/0.5532 |
| qwen | 0 | 1.00008 | 0.0980262 | v_proj.bias×1/0.1953, v_proj.weight×1/0.09796 |
| qwen | 1 | 1.04489 | 0.097411 | v_proj.bias×1.045/0.1818, v_proj.weight×1.045/0.09736 |
| qwen | 2 | 1.07043 | 0.0947022 | v_proj.bias×1.069/0.1719, v_proj.weight×1.07/0.09465 |
| qwen | 3 | 1.08803 | 0.0921132 | v_proj.bias×1.085/0.1612, v_proj.weight×1.088/0.09207 |

## Final fresh formed-state transfer

These rows were opened only after the reversible intervals. They use the baseline suffix consumer for baseline, transfer, and blocker contrasts; the accepted native surface is reported separately by the worker.

| family | arm | row | original C0 consumer | transfer Δ margin | blocker removed | source/state receipts |
|---|---|---|---:|---:|---:|---:|
| mamba | matched_depth | transfer-named-nation-canada-brazil-forward | yes | 0.00683212 | 0.0041008 | 4 |
| mamba | matched_depth | transfer-named-nation-canada-brazil-reverse | yes | 0.0467434 | 0.0221786 | 4 |
| mamba | operation_label_swap | transfer-named-nation-canada-brazil-forward | yes | 0.447735 | 0.451126 | 4 |
| mamba | operation_label_swap | transfer-named-nation-canada-brazil-reverse | yes | 0.327154 | 0.325325 | 4 |
| mamba | writer | transfer-named-nation-canada-brazil-forward | yes | 0.457836 | 0.46077 | 4 |
| mamba | writer | transfer-named-nation-canada-brazil-reverse | yes | 0.353975 | 0.351925 | 4 |
| qwen | matched_depth | transfer-named-nation-canada-brazil-forward | yes | -0.00394917 | -0.00364208 | 4 |
| qwen | matched_depth | transfer-named-nation-canada-brazil-reverse | yes | 0.00192666 | 0.000793457 | 4 |
| qwen | operation_label_swap | transfer-named-nation-canada-brazil-forward | yes | 0 | 0 | 4 |
| qwen | operation_label_swap | transfer-named-nation-canada-brazil-reverse | yes | 0 | 0 | 4 |
| qwen | writer | transfer-named-nation-canada-brazil-forward | yes | 0.445127 | 0.441001 | 4 |
| qwen | writer | transfer-named-nation-canada-brazil-reverse | yes | 0.433943 | 0.433676 | 4 |

## Mamba x_proj row partition

For the native Mamba surface, `x_proj` has shape `[80, 1536]` and `dt_proj.weight` has input width 48. The exact bookkeeping partition is dt rows `0:48`, B rows `48:64`, and C rows `64:80` (`d_state=16`). The table reports saved candidate delta norms and relative norms; the slices share one native surface and are not separate causal interventions.

| arm | interval | dt ΔL2 | B ΔL2 | C ΔL2 | dt ΔL2/parent | B ΔL2/parent | C ΔL2/parent |
|---|---:|---:|---:|---:|---:|---:|---:|
| matched_depth | 0 | 0.135759 | 0.0783736 | 0.0783763 | 0.00510578 | 0.00551035 | 0.0061572 |
| matched_depth | 1 | 0.0647275 | 0.0371083 | 0.0373942 | 0.00243428 | 0.00260906 | 0.00293771 |
| matched_depth | 2 | 0.0313628 | 0.017705 | 0.0179301 | 0.00117947 | 0.00124482 | 0.00140857 |
| matched_depth | 3 | 0.0153301 | 0.00851591 | 0.00866067 | 0.000576515 | 0.000598741 | 0.000680369 |
| operation_label_swap | 0 | 0.135754 | 0.078381 | 0.0783793 | 0.00512638 | 0.00502775 | 0.0064437 |
| operation_label_swap | 1 | 0.0648802 | 0.0386161 | 0.0381394 | 0.00244981 | 0.00247683 | 0.00313521 |
| operation_label_swap | 2 | 0.0320947 | 0.0192111 | 0.0190121 | 0.00121179 | 0.00123213 | 0.00156278 |
| operation_label_swap | 3 | 0.0159691 | 0.00956809 | 0.00949685 | 0.000602922 | 0.000613648 | 0.000780609 |
| writer | 0 | 0.13575 | 0.0783796 | 0.0783788 | 0.00512625 | 0.00502766 | 0.00644365 |
| writer | 1 | 0.0641542 | 0.038272 | 0.0385874 | 0.00242247 | 0.00245469 | 0.00317186 |
| writer | 2 | 0.0316143 | 0.0189926 | 0.0192354 | 0.00119372 | 0.00121807 | 0.001581 |
| writer | 3 | 0.0157238 | 0.00944777 | 0.00959623 | 0.000593697 | 0.000605902 | 0.000788697 |

## Qualifications

* Object SHA-256 checks verify custody bytes before decoding; no foundation weights are loaded.
* The pairwise dose table compares saved parameter displacements, not downstream competence or role specificity.
* Mamba x_proj and dt_proj jointly alter clock, B/C selection, retention, and current read; component norms do not isolate a single causal term.
* For Mamba x_proj [80, 1536] and dt_proj.weight input width 48, the native bookkeeping partition is dt rows 0:48, B rows 48:64, and C rows 64:80 (d_state=16); these row norms are descriptive, not independent interventions.
* A high writer/wrong-label dose similarity or delta cosine is consistent with a shared generic gradient direction, but cannot by itself explain the downstream score.
* Qwen and Mamba surface norms are family-local and must not be normalized into a common magnitude ladder.
