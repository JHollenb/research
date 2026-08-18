# FLUX.2 Dev full-analysis failure diagnosis

Date: 2026-07-27  
Scope: read-only diagnosis of `job-18929d947c5b`; no Atlas, mrun, manalysis, or Obsidian edits and no fleet action.

## Verdict

The run is **NO-GO for every promoted result** for two independent reasons:

1. its remove+restore sentinel failed pixel identity; and
2. it was submitted through ordinary `POST /api/jobs`, not guarded admission, so the public receipt says `job is not guarded` and `executed_payload` is null.

The locally fetched trajectory, behavior, recorder, and readout files are failed-run diagnostics only. There is no `analysis.json`. They cannot be admitted retroactively.

## Intervention failure

Terminal evidence reports that all winder gates passed except `restoration_pixels_exact`. Both sessions applied once, but the restored image still changed 765,280 of 786,432 RGB channel values, with maximum delta 255 and mean delta 23.563. That is a large surviving intervention, not a near-threshold pixel-rounding miss.

The exact manalysis wheel bound by the trajectory certificate is SHA-256 `e1625dcf533431809c4037f3b0cd0a1ca8fb4e67b5081a8cc6322d2e23449d73`; it matches the current vendored wheel. Its output sessions register PyTorch forward hooks with `prepend=True`. Consequently, hooks execute in reverse entry order:

- entering `patch` then `ablate` executes `ablate` then `patch` and restores the clean tensor;
- entering `ablate` then `patch` executes `patch` then `ablate`, leaving the lesion last.

During this audit the worker changed at 15:23 PDT to `with patch, ablate:` and acquired a LIFO explanation. The test changed shortly afterward to assert that spelling with `inspect.getsource`. These post-failure edits, plus the large observed image delta, make the shipped opposite context order the high-confidence likely cause. The old archive cannot be byte-inspected locally, and its unguarded custody prevents using the current tree as proof of what ran.

There is a second unresolved risk: the patch source comes from a separate clean pipeline call. The clean-capture image was pixel-exact, but no gate compared the selected activation bytes across clean calls. A source-text assertion neither proves runtime hook composition nor excludes cross-call activation drift under disk dispatch.

## Custody failure

`scripts/submit_flux2_dev_full_analysis.py` still imports `submit` from `mrun.client.submit` and calls `submit(**spec)`. That client always sends `POST /api/jobs`, followed by a mutable payload `PUT`. The server computes `custody_required = guarded and payload_kind == "shipped"`; only `POST /api/jobs/guarded` creates guarded custody and server-adds the `payload_custody_v2` need.

Therefore, putting `payload_custody_v2: true` in the ordinary client's `needs` object is only a client field/capability selector. It does not upgrade admission. `job is not guarded` and `executed_payload: null` are the expected result of this path.

Any new queued resume created by this wrapper has the same defect. In particular, `b7019352686a` is unguarded if it came from the current wrapper; it cannot become evidence even if it succeeds. This report makes no cancellation recommendation and performed no fleet mutation.

## Current repair audit

Observed current-tree changes:

- `scripts/analyze_flux2_dev_decoupled.py`: restoration context is now `with patch, ablate`, which is the correct order for `prepend=True` sessions.
- `scripts/submit_flux2_dev_full_analysis.py`: a resume lowers declared VRAM from 12,900 MiB to 12,000 MiB, but submission remains legacy and unguarded.
- `tests/test_flux2_dev_full_analysis.py`: adds a resumed-VRAM assertion and a source-string assertion for context order.

Snapshot hashes:

- worker: `dffdb25dd031f2498c5041f5a2c3fbc48b2b9005f014f987ffcb49cd24a4e81b`
- submitter: `761fa075e8614ff1bea7786d60482c40e7bcbc91001765ec9680e1d812b74340`
- focused test: `de530f9c1acd82063ee9620336aea7e98ce8bd2b621419b908b046ba571c7ca6`
- wheel: `e1625dcf533431809c4037f3b0cd0a1ca8fb4e67b5081a8cc6322d2e23449d73`

The semantic order fix is plausible, but the repair is not release-ready: its test is structural rather than behavioral, its cross-call source identity remains untested, and custody is still definitively wrong.

Two later hash snapshots were identical, and the final check found no Atlas script/test write in the preceding three minutes. The three repaired files therefore appeared locally stable at handoff, although their writer/provenance remains unknown.

## Post-diagnosis external resume result

After this diagnosis was written, externally submitted resume
`job-b7019352686a` reached terminal `failed` in 543.4 seconds. It is useful only
as a repair diagnostic:

- the winder pilot passed every sentinel, including pixel-exact restoration
  (`changed_values = 0`, `max_abs_delta = 0`, `mean_abs_delta = 0.0`);
- the learned, equal-energy random, and wrong-time arms each applied exactly
  once and produced non-zero rendered changes;
- the overall analysis still failed because the reused common and native
  behavior evaluations lacked the required `printed_line_ocr` scores; and
- the public receipt returned HTTP 409 `job is not guarded`, while both the job
  and result report `executed_payload: null`.

This strongly confirms that the corrected LIFO context order repairs the
original restoration defect. It does not cure custody, does not admit the
reused behavior/readout artifacts, and does not support a semantic or causal
concept claim. A fresh guarded winder certificate remains the minimum valid
next fleet run.

## Minimal changes required in Atlas

1. Replace the direct legacy `submit` call with the existing guarded controller primitives: deterministic pack, payload contract, pre-POST request/submission anchors, fenced claim, `POST /api/jobs/guarded`, exact seal, public terminal receipt, and declared/sealed/executed payload equality. Require a fresh preflight for the exact changed payload.
2. Replace the `inspect.getsource` test with a real composed-session test. On a toy adapter, assert that `with patch, ablate` returns the exact clean tensor, the opposite order fails, both sessions apply once, scopes are exact, and all hooks are removed.
3. In the GPU sentinel, capture the clean selected tensor before the lesion and the restored tensor after the patch in the same forward. Bind both to the same full `InvocationKey` and require `torch.equal`, dtype/device/shape identity, and matching fingerprints. Use a callable patch source from that same invocation rather than relying only on a previous pipeline call.
4. Retain a separate active-ablation arm and require it to change the selected tensor and rendered output, preventing a vacuous rescue pass.
5. Persist a failed `winder-pilot.json` before raising, explicitly marked `PASS: false` and non-promotable, so exact tensor/pixel/evidence diagnostics survive failure.
6. Move the algebraic rescue sentinel ahead of the 28-step behavior panel and 128-stimulus recorder. The readout-selected semantic intervention can remain later; the instrumentation gate should fail fast.

## Cheaper gated recertification

Run a new, guarded `winder-certify` stage before another full analysis:

1. exact current payload preflight and guarded custody smoke;
2. exact model/plan/wheel load, one prompt, one seed, four steps;
3. two clean calls with selected-activation fingerprints to establish repeatability;
4. one active ablation proving the channel is non-vacuous;
5. one same-forward capture -> ablate -> patch -> post-capture rescue, requiring tensor and pixel exactness;
6. exact hook cleanup plus a successful public guarded terminal receipt.

Do not run the common behavior panel, native 28-step panel, 128-stimulus recorder, readout fitting, or evaluators in this certificate. Only after that certificate passes should the full analysis rerun from a fresh guarded payload, with the rescue sentinel first. Failed-job files may guide debugging but must not be reused as admitted evidence.

## Local verification

`diagnose.py` uses real PyTorch `prepend=True` hooks to reproduce both context orders and inspects the current worker, submitter, server, wheel binding, and selected readout cell. Local checks:

- Atlas focused test: 5 passed;
- sibling diagnostic tests: 2 passed;
- sibling Ruff check: clean;
- no network or job actions performed.

Failed artifact hashes inspected:

- trajectory certificate: `3f76670988a398c7acfdbbabf0e3c286747a08f77a57d4eb55e38cfead232e62`
- recorder capture: `25ca5b0994a1f20f70c57db471f6b1740756229c8b84d2d9814ec1962fc69e6b`
- recorder readouts: `4281b48714bae817cf421135eeebbb209138b3647f53fe188da6981993c2b3f9`
