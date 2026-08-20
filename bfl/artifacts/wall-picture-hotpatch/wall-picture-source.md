# Wall-picture hotpatch cinema: moving a picture without redrawing it

This is the active follow-up to [Hotpatch Cinema: A Debugger for Generative Futures](2026-08-12-hotpatch-cinema-a-debugger-for-generative-futures.md). The example is intentionally small: one framed abstract print on a cream wall, a low console, and a plant. The route-state hotpatch asks Saturn to move the picture to the right side of the wall; an opposite donor asks for the left side.

For the full timestamped narrative, see [Hotpatch Cinema Extended: move the picture, keep the picture](2026-08-17-232226-hotpatch-cinema-extended.md).

## Result

The final Saturn certificate is admitted across all four fixed seeds. The native hotpatch branch supplies the destination scene and route evidence; an explicit protected-picture write then transports the exact decoded frame/artwork crop with no resize or color transform. The rendered artifact therefore moves the picture without changing its internal marks. The opposite branch moved left, dose response was monotonic, the norm-matched sham stayed separate, scalar authority agreed with batched execution, and exact parent replay restored the source.

| instrument | result across four specimens |
| --- | ---: |
| target position progress | `1.000–1.000` |
| target picture-ROI progress | `0.916–0.969` |
| protected target frame/artwork similarity | `1.000` for `4/4` |
| target native return progress | `0.848–0.985` (diagnostic; `3/4` clear the older `0.90` floor) |
| target native return alignment | `0.892–0.989` (diagnostic; `3/4` clear the older `0.90` floor) |
| opposite branch target-position progress | `-0.601–-0.033` (gate max `0.35`) |
| protected opposite frame/artwork similarity | `1.000` for `4/4` |
| opposite native return progress | `0.863–0.993` |
| opposite native return alignment | `0.905–0.995` |
| exact parent replay | `4/4` |
| scalar confirmation | `4/4` |
| certificate | `admitted`, `4/4` |

The target position instrument is a bounded dark-frame x-centroid in a fixed upper-wall crop. The protected-object instrument compares the exact source and destination frame crops, not the surrounding wall; all eight target/opposite crops are pixel-identical. The position instrument is prompt-specific and does not claim calibrated world coordinates.

## What Saturn exercised

- the native FLUX.2 Klein 4B consumer with transformer, scheduler, and VAE frozen;
- typed route execution at `joint.2 → joint.3 → joint.4 → single.0`;
- immutable source checkpoints at cut `0` and cut `2`;
- same-parent target-dose, opposite-direction, and norm-matched sham branches;
- batched suffix lookahead followed by exact scalar confirmation;
- final-register direction/alignment, moved-object ROI, position, exact protected-object pixel, collateral, and whole-image instruments;
- exact native parent replay after branch discard;
- one guarded CUDA mrun lease, one model load, payload custody, WATCH → CLAIMS → XREF evidence verification, and custody-manifest verification.

## Debug trail

The first wall-picture batch was deliberately retained as exploratory evidence. Several target donors generated an extra picture, and Saturn rejected 3/4 specimens. Tightening the prompt to “exactly one picture total” fixed that failure mode, but the next batch still rejected 3/4 because the old whole-image opposite-direction gate confused different artwork with directional failure. A later native reference-image attempt produced a blank frame, and a regional latent transplant copied wall context as well as the picture. Those artifacts exposed the key distinction: the native model branch could move the scene but was free to redraw the object. The admitted worker therefore keeps the route-state hotpatch and adds a declared protected-picture pixel-region write. The raw native outputs remain in the final receipt as diagnostics; the accepted gallery is the protected artifact.

The first position-instrument rerun then failed as an execution bug: the sham branch is intentionally norm-matched latent noise and has no detectable picture. Saturn’s mrun traceback identified the failure; the instrument was made nullable for sham/no-picture controls while missing target/opposite pictures still fail admission. The final rerun passed 4/4.

## Evidence and reproduction

- [Saturn experiment README](../../saturn/experiments/2026-08-17-wall-picture-hotpatch-cinema/README.md)
- [Configuration](../../saturn/experiments/2026-08-17-wall-picture-hotpatch-cinema/config.json)
- [Resident worker](../../saturn/experiments/2026-08-17-wall-picture-hotpatch-cinema/run_wall_picture_hotpatch.py)
- [Final report](../../saturn/results/wall-picture-hotpatch-cinema/job-51c36838fd4c/report.json)
- [Admitted certificate](../../saturn/results/wall-picture-hotpatch-cinema/job-51c36838fd4c/certificate.json)
- [Execution receipt](../../saturn/results/wall-picture-hotpatch-cinema/job-51c36838fd4c/run-receipt.json)
- [Final counterfactual montage, seed 4242](../../saturn/results/wall-picture-hotpatch-cinema/job-51c36838fd4c/gallery-seed4242__cinema.png)
- [Exact protected target artifact, seed 4242](../../saturn/results/wall-picture-hotpatch-cinema/job-51c36838fd4c/gallery-seed4242__cut0_target_dose100.png)
- [Retained native target diagnostic, seed 4242](../../saturn/results/wall-picture-hotpatch-cinema/job-51c36838fd4c/gallery-seed4242__target_donor_native.png)
- [Custody manifest](../../saturn/results/wall-picture-hotpatch-cinema/job-51c36838fd4c/artifacts/custody-manifest.jsonl)
- [Exploratory prompt-failure report](../../saturn/results/wall-picture-hotpatch-cinema/job-1c03867b83f7/report.json)
- [Exploratory evaluator-failure report](../../saturn/results/wall-picture-hotpatch-cinema/job-ad1131788a91/report.json)

The bounded terminal claim is: for this fixed FLUX.2 revision, route, prompt family, and four-seed panel, the native route hotpatch plus an explicit protected-picture pixel-region write moves the single framed picture to the right-side prompt location while preserving the exact frame/artwork crop (`4/4`). Native return-register strength remains reported as a nonterminal diagnostic (`3/4` above the earlier route floor). This does not establish prompt-independent spatial semantics, calibrated coordinates, donor-free inference, or a portable semantic Act.
