# Exp2 first scene — viability gate FAILED (coordinator inspection)

Job `job-ed0aee67ac23` (prompts: neutral/left/right "… adjusts the focus of the left/right
camera", seeds 7001…7177) completed mechanically (smoke gate exact, 128 images, blinded key).

**Coordinator applied the pre-registered scene-viability gate to
`native-left-right-viability.png`:**

- native **LEFT** prompt → requested-side camera contact in **~0/16**
- native **RIGHT** prompt → requested-side camera contact in **~4/16**
- Gate requires ≥ 10/16 each side → **FAILS.**

Failure mode: subjects mostly hold a small handheld camera or touch their own face rather than
reaching to the two tripod cameras. The scene/action prompt is ambiguous.

**Consequence:** this 128-image run is **not scored**. It is retained as a failed-viability
record (report.json, judge/, judge-key.json, contact sheets kept immutable). The retry uses
stronger, side-explicit, tripod-contact prompts rendered native-left/right only, gate-first —
see `PREREG.md` (Exp 2 viability retry) and `results/exp2viab/`.
