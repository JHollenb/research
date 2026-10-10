# Pre-registration — BFL demo controls (FLUX.2 Klein 4B)

Written and committed before the scored mrun jobs. Two control experiments that
harden two existing public demo pages. All compute on a single RTX 4080 (16 GB) through mrun.

- Model: `black-forest-labs/FLUX.2-klein-4B`, pinned revision
  `e7b7dc27f91deacad38e78976d1f2b499d76a294`, materialized at
  a local flat snapshot of the pinned revision.
- Precision BF16, guidance 1.0, 4 denoising steps, batch 1, text-only (no reference image).
- Adapter: `saturn_pub.adapters.flux2.Flux2KleinAdapter`, block granularity, resident.
  Transformer has 5 joint blocks (`joint.0..4`) and 20 single blocks (`single.0..19`);
  text slot width = 24 heads × 128 = 3072; conditioning seq-len = 512 (Qwen3 chat-template,
  `padding="max_length"`, so every prompt yields identical length — route subtraction and
  prompt swaps are shape-safe).
- Scoring and judging code is frozen in `run.py` at the committed SHA before the scored jobs.

## Shared frozen smoke gate (runs first, in-process; abort on failure)

Each scored job first runs these mechanics checks on a single specimen/seed and aborts
(non-zero exit → failed job) if any fail. Only on pass does it continue to the full panel
in the same process:

1. **Unpatched stepped-vs-native parity.** The adapter trajectory driven block-by-block
   (project → 5 joint → 20 single → flow commit per step) must produce per-step latent
   digests bit-identical to the ordinary diffusers full-forward trajectory
   (`_flux2_native_step` + scheduler) on the same inputs.
2. **StateCut resume parity.** Capture a `StateCut` at a step boundary, restore it into a
   fresh session, finish the trajectory, and require the resumed final-latent digest to
   equal the straight-through (native) final-latent digest.
3. **Zero-dose identity.** A route branch with dose 0 (Exp 1) / an M-arm that writes the
   captured native value back unchanged (Exp 2 liveness) must reproduce the unpatched
   final image bytes exactly.
4. **Expected fields present.** The report dict carries the declared schema keys.

## Experiment 1 — Is a route edit more than a prompt swap?

Reproduces and extends `research/bfl/demos/counterfactual-diffusion-futures.md`.

- Resolution 256×256. Four specimens: scene transfer seeds 9001, 1337; subject transfer
  seeds 4242, 9001.
- Prompts (verbatim from the demo):
  - source: `a photorealistic red fox sitting in fresh snow at dawn, soft red light`
  - scene donor: `a photorealistic red fox standing in a sunlit desert at noon, warm red light`
  - subject donor: `a photorealistic red cat sitting in fresh snow at dawn, soft red light`
  - hostile donor: `a photorealistic blue fox sitting in fresh snow at dawn, soft blue light`
- Route sites (text stream): `after:joint.2`, `after:joint.3`, `after:joint.4`,
  and the text rows of `after:single.0`. At every denoising step `t ≥ cut`, the text slot
  at each site is replaced by `h_src(site,t) + dose·(h_donor(site,t) − h_src(site,t))`,
  where `h_src`/`h_donor` are captured from the unpatched pure source / pure donor
  trajectories (same initial latent + img_ids; donor differs only in conditioning). This is
  the original formula `R_branch = R_source + dose·(R_donor − R_source)`. Cuts: 0 and 2.
- Arms per specimen and cut:
  - (a) **ROUTE** dose 1 (reproduces the original arm).
  - (b) **PROMPT-SWAP**: run the source trajectory to the cut, then continue with the
    donor's conditioning (encoder output) for all remaining steps, no route patch.
    At cut 0 this is the full donor generation.
  - (c) at cut 0 only, additionally **hostile ROUTE** dose 1 and **hostile PROMPT-SWAP**.
- Scores (RGB, 0–255 scale, per final decoded image):
  - progress `P = 1 − MAD(I, I_donor) / (MAD(I_src, I_donor) + ε)`, ε = 1e-6.
    `I_src` = pure source image, `I_donor` = the axis donor image. (Hostile "own progress"
    uses `I_donor_hostile`; hostile "target progress" uses the axis `I_donor`.)
  - arm difference `d = MAD(I_route, I_swap) / MAD(I_src, I_donor)`.
- **Reproduction check:** report `P_route(cut0)` next to the demo's original progress
  (scene-9001 0.916, scene-1337 0.907, subject-4242 0.971, subject-9001 0.904; late/cut2
  0.165/0.095/0.099/0.358). Agreement within ≈0.10 is a successful reproduction.
- **Decision rule (per cut, pre-registered):**
  - "route ≈ prompt swap" if `|P_route − P_swap| ≤ 0.05` AND `d ≤ 0.10` for all four specimens;
  - "route differs" if `d > 0.25` in ≥ 3/4 specimens;
  - otherwise "partial".
  Both cuts are reported.

## Experiment 2 — Camera-contact replication (text-only, more seeds, blinded)

Text-only generalization of `research/bfl/demos/scene-relations-and-instance-binding.md`
(no saved "Jen" reference image, so it is reproducible from the public repo).

- Resolution 512×512, 16 fresh seeds (not 26091741/26091841/26091842):
  `7001, 7013, 7027, 7039, 7043, 7057, 7069, 7079, 7103, 7109, 7121, 7127, 7129, 7151, 7159, 7177`.
- Prompts (left/right token-length matched; differ only in the word left/right):
  - neutral: `a person sits at a wooden table between two cameras on tripods`
  - left:  `a person sits at a wooden table between two cameras on tripods and adjusts the focus of the left camera`
  - right: `a person sits at a wooden table between two cameras on tripods and adjusts the focus of the right camera`
- Definitions (at `joint.3` text, each of the 4 steps): native joint.3 text states `H_L`,
  `H_R` from the left/right prompts; `M = (H_L + H_R)/2`, `D = (H_R − H_L)/2`.
  `P` is the diagonal projector onto the predicate rows = the token positions of the
  predicate phrase "adjusts the focus", resolved from the tokenizer offset mapping (the
  same rows in both prompts; asserted identical). `D_pred = P D`, `D_rest = (I − P) D`.
- Arms (each a full 4-step trajectory; interventions use the **neutral** conditioning and
  overwrite the full `joint.3` text slot every step): `neutral`; `native left`;
  `native right`; `M`; `M+D_rest`; `M−D_rest`; `M+D_pred`; `M−D_pred`. 16 seeds × 8 arms
  = 128 images.
- **Sign convention (verified against the FINDINGS, deviates from the task brief's
  parenthetical):** the demo and FINDINGS define `D = (H_R − H_L)/2`, so `M + D = H_R`
  (the right-target prompt). Therefore:
  - `M+D_rest` and `M+D_pred` request the **right** camera;
  - `M−D_rest` and `M−D_pred` request the **left** camera;
  - `native left` requests left, `native right` requests right.
  (The task brief wrote "M+D_rest (expect left)"; that contradicts `D=(H_R−H_L)/2` and is
  recorded as a corrected deviation.)
- **Metrics (judged later, blinded, by the coordinator — not by this agent):**
  - primary = fraction of `M±D_rest` images whose hand contacts the **requested** camera,
    with a Wilson 95% CI (n = 32: 16 seeds × 2 signs);
  - secondary = the same fraction for `native left`/`native right` and for `M±D_pred`;
  - `M`-alone left-bias rate (fraction of 16 M images contacting the left camera).
- **Blinding:** every image is written to `results/exp2/judge/<random-id>.png`; a key file
  `results/exp2/judge-key.json` (kept separate from the sheets) maps id → {arm, seed,
  requested_side}. Contact sheets show the shuffled ids only. This agent does **not** judge.
- **Scene-viability gate (pre-registered handling):** the brief asks to stop if native
  left/right do not produce requested-side contact in ≥ 10/16 each. Because the blinding
  rule forbids this agent from judging contact, this agent does **not** self-judge or
  self-abort on contact. The mechanics smoke gate still governs abort. A separate,
  labelled (non-blinded) native-left/right sheet is produced so the coordinator can apply
  the viability gate before trusting the full panel. Up to two pre-registered prompt
  variants were allowed in the smoke stage; this run uses the single primary set above and
  defers any prompt change to the coordinator.

## Experiment 2 — viability gate outcome and prompt retry (added before the retry job)

**First scene viability gate FAILED by coordinator inspection** of
`results/exp2/native-left-right-viability.png` (job `job-ed0aee67ac23`, prompts "… adjusts the
focus of the left/right camera", seeds 7001…7177): native LEFT ≈ 0/16, native RIGHT ≈ 4/16
requested-side contact (subjects mostly hold a handheld camera or touch their face). Gate
requires ≥ 10/16 each → fails, so that 128-image run is **not scored** and is kept as an
immutable failed-viability record (see `results/exp2/VIABILITY-FAILED.md`). The 8-arm run is
**not** launched for the retry until the coordinator passes the new scene.

**Gate-first retry (`--experiment exp2viab`, pre-registered here before the retry job):** one
mrun job that renders **native left/right only** for **two prompt variants** across **16 fresh
seeds** `8101, 8111, 8117, 8123, 8147, 8161, 8167, 8171, 8179, 8191, 8209, 8219, 8221, 8231,
8233, 8237` (disjoint from 7001… and the historical 26091741 set), 512², then **stops**. Same
mechanics smoke gate first (abort on failure). The two tripod cameras are described as large and
on tripods, clearly separate from the person, who reaches out and makes explicit contact with
the camera on a stated **side of the image**; left/right prompts are token-length matched and
differ only at the side token; the predicate span (the action phrase) is kept as the predicate
rows for the eventual M/D arms. Exact strings:

- **Variant A** (predicate span "adjusting its focus ring"; verified predicate rows
  `[38,39,40,41]`=`[' adjusting',' its',' focus',' ring']`, left/right differ only at token 32):
  - left:  `a photo of a person seated at a wooden table between two large cameras on tripods, reaching out with one hand and touching the camera on the left side of the image, adjusting its focus ring`
  - right: `… touching the camera on the right side of the image, adjusting its focus ring`
- **Variant B** (predicate span "firmly gripping the lens"; verified predicate rows
  `[28,29,30,31]`=`[' firmly',' gripping',' the',' lens']`, left/right differ only at token 37):
  - left:  `a photo of a person seated at a wooden table between two large cameras on separate tripods, reaching out with one hand and firmly gripping the lens of the camera on the left side of the image`
  - right: `… firmly gripping the lens of the camera on the right side of the image`

Deliverable: one non-blinded viability sheet per variant (labelled seed + side),
`results/exp2viab/viability-variant-A.png` and `…-B.png`, plus per-image PNGs. The worker does
not judge; the coordinator applies the ≥ 10/16-each gate and decides whether (and with which
variant) to authorize the full 8-arm run.

**Gate decision (coordinator, non-blinded read of the viability sheets):** **Variant B PASSES**
(left ≈ 14/16, right ≈ 15/16 requested-side contact; clean single-person layouts). Variant A not
used (crowded, multiple people, ambiguous hands). Authorized the full 8-arm blinded run on
Variant B + the same 16 fresh seeds `8101…8237`.

**Full 8-arm blinded run on Variant B (`--experiment exp2b`):** prompts =
- left: `…reaching out with one hand and firmly gripping the lens of the camera on the left side of the image`
- right: `… on the right side of the image`
- neutral (Variant B without the action/side clause, same structure):
  `a photo of a person seated at a wooden table between two large cameras on separate tripods`

Arms: `neutral`, `native left`, `native right`, `M`, `M+D_rest (→right)`, `M−D_rest (→left)`,
`M+D_pred (→right)`, `M−D_pred (→left)`. Predicate rows `[28,29,30,31]`=`[' firmly',' gripping',
' the',' lens']`; interventions overwrite the full `joint.3` text each of the 4 steps on the
neutral-conditioned trajectory. 512², 16 seeds `8101…8237`. Same mechanics smoke gate; same
blinding (random ids, separate `judge-key.json`, shuffled sheets labelled by id only). Metrics
and sign convention unchanged from the Experiment 2 section above. Worker does not judge.

## Recording

Per experiment: backend, device, dtype, model/revision, adapter identity, torch/diffusers
versions, mrun job id, wall time, peak VRAM/RSS, smoke results, full tables, report.json,
contact sheet PNG(s) (≤ ~1.5 MB each), and for Exp 2 the judge dir + key path. Git SHAs of
the staged `src/saturn_pub` and `run.py` are embedded in each report.
