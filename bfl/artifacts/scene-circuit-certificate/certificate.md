# Saturn causal circuit certificate

- status: **certified**
- route: `joint.2 -> joint.3 -> joint.4 -> single.0`

The declared joint.2 -> joint.3 -> joint.4 -> single.0 route is a causally sufficient, necessary, specific, dose-responsive, and consumer-continuing scene circuit for native FLUX.2 Klein/Qwen under the recorded 256x256, four-step, guidance-1 experiment.

## Gates

| gate | result | observed | rule |
|---|---|---|---|
| reproducibility | PASS | `{"seed_count": 2, "seeds": ["4242", "9001"]}` | at least two independent seeds are required |
| sufficiency | PASS | `{"minimum_scene_progress": 0.9132605915813907}` | min scene progress >= 0.9 |
| necessity | PASS | `{"maximum_route_ablation_scene_progress": 0.022478059397213257}` | max route-ablation scene progress <= 0.15 |
| specificity_wrong_axis | PASS | `{"maximum_wrong_color_scene_progress": -0.4303132839954793, "minimum_wrong_color_margin": 1.3559930503211004}` | wrong-axis donor stays below the scene target and remains more color-like |
| specificity_sham | PASS | `{"maximum_sham_scene_progress": 0.10859346469260778}` | max norm-matched sham scene progress <= 0.35 |
| dose_response | PASS | `{"scene_progress_by_seed": {"4242": [1.284146122770835e-10, -0.01366973076151523, 0.059807889485324006, 0.4846719352443404, 0.9438734326776155], "9001": [1.343098965378431e-10, -0.058037997311915834, 0.020407592490434223, 0.37267900739623483, 0.9132605915813907]}, "scene_return_progress_by_seed": {"4242": [0.0, 0.08206312358379364, 0.3373183608055115, 0.879298985004425, 0.9836190342903137], "9001": [0.0, 0.15882575511932373, 0.4560082256793976, 0.7432774305343628, 0.9823917150497437]}}` | RGB dose is directionally monotone within display tolerance and the downstream return carrier is monotone within causal tolerance |
| mediation | PASS | `{"all_rescue_fractions": [0.9617085891578255, 0.9169450356587042, 0.7704782254031485, 0.9636500701550218, 0.9230346512086899, 0.8051734366468964], "minimum_rescue_fraction": 0.7704782254031485}` | every tested edge rescue fraction >= 0.5 |
| consumer_continuation | PASS | `{"minimum_scene_return_alignment": 0.9708396196365356, "minimum_scene_return_progress": 0.9823917150497437}` | the scene carrier survives into the final scheduler return register |
| exact_scalar_replay | PASS | `{"exact_scalar_branch_count_by_seed": {"4242": 18, "9001": 18}}` | all recorded intervention branches use scalar-authority checkpoint replay |

## Scope boundary

Certified is intentionally route-level and experiment-bounded. It does not establish a minimal token/channel subcircuit, universal prompt generalization, or that the four addresses are standalone semantic functions. Those are separate promotion targets.
