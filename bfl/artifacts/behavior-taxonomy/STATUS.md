# STATUS — T6 typography behavior substrate

## 2026-07-31 — panel frozen, tests green, discovery queued [MEASURED unless labelled]

Program stood up by cloning the counting program's behavior-admission shape (studied read-only:
`run_flux2_reference_behavior_atlas.py`, `compile_flux2_behavior_selection.py`,
`compile_flux2_reference_count_behavior_certificate.py`, `flux2-behavior-admission-atlas-v1.json`,
`flux2-reference-top-left-count-behavior-certificate-v1.json`,
`submit_flux2_reference_behavior_atlas.py`, status.md). Nothing outside this workspace was
edited.

### Frozen artifacts

- Panel: `scripts/flux2-typography-behavior-atlas-v1.json`, fingerprint
  `18fc7cba66bbf4fb66e6fad1b29079b8f81ca100c3146b321954183ee385e6f3`.
  8 families (presence/substitution/append/spell x plain/spec), 16 discovery seeds
  (76001..76141), 16 disjoint confirmation seeds (76303..76463), 2 discovery + 3 confirmation
  instantiations per transition; discovery = 256 pairs (512 images). `presence-plain` is the
  frozen easy plain-sign family. Case transitions excluded (scorer-invisible: normalization
  uppercases). Gates numeric in the panel: pair admission = exact normalized TrOCR match on
  upper AND transition-appropriate lower rule; confirmation admission per family = rate >= 0.5,
  Wilson lower 95 >= 0.35, rate per seed >= 0.25, rate per instantiation >= 0.25, total admitted
  >= 12 (counting-atlas thresholds); discovery selection = rate >= 0.25, upper exact >= 0.25,
  <= 1 lexicalization per transition. All-fail rule frozen: 0-admitted discovery is a valid
  measured result about 4-step distillation -> Wilson upper bounds + diagnostic graded signal,
  causal ladder redirects toward klein-9b (measured 0.25/0.307 vs Klein 4B 0.0/0.0 on the atlas
  common panel).
- PLAN.md sha256 at submit: `c7bbca052195ecd07b49b316c877ca364712931ca559080521d8c4834963b832`
  (recorded inside the job's source_sha256).
- Capture runtime borrowed byte-identical from the counting program
  (`ceebd900753b4f1f413b65a0926dfa57ffecc510320d8390094ff1c4f714a681`), submitter re-verifies
  copy == original fail-closed.

### Scorer

Reused, not reimplemented: `image_atlas.evaluate.OcrEvaluator` pinned TrOCR pathway
(`microsoft/trocr-small-printed` @ `04e994ab854b0089d4929f48c2b4dbe2ce78a340`, resolved through
the study registry), `normalize_ocr_text` + `edit_distance`. Runner asserts the pinned
processor/tokenizer classes at load.

### Tests / lint [MEASURED]

`python3 -m pytest tests/ -q` -> **13 passed** (freeze shape + row counts, transition structure
+ easy family, normalization stability, tamper rejection, Wilson bounds incl. the counting
certificate's 30/30 value 0.8864866068260312, presence/substitution/append admission rules,
summaries + confirmation gate, all-fail analysis, selection policy incl. NO_FAMILY_SELECTED and
tampered-report rejection). `uvx ruff@0.12.5 check` on all workspace sources -> clean
(E, F, we, UP, B, line 100). One real bug was caught by the tests before submission (atlas path
bootstrap used parents[2] instead of parents[1]) and fixed.

### Beast env prep [MEASURED]

sentencepiece 0.2.2 was absent from Beast's offline uv cache (OCR tokenizer dependency); seeded
it once online, then verified the full pinned dependency set resolves `--offline`
(torch 2.13.0+cu130, transformers 5.14.1, diffusers 0.39.0, sentencepiece 0.2.2 -> OFFLINE-OK).
Additive cache population only; no tenant state touched. TrOCR snapshot confirmed present at
`/mnt/big/llm-models/evaluators/trocr-small-printed`.

### Discovery job [MEASURED at 2026-07-31 ~15:5x PT]

- Submitted through mrun: **`job-13e485fa9139`**, experiment
  `flux2-typography-behavior-atlas-v1-discovery`, host pin beast, priority 40.
- Reservation (honest, precedent-cited): ram_mb 19500 (measured counting discovery RSS peak
  19026.8MB), vram_mb 9900 (measured klein VRAM 8546MB + resident TrOCR fp16, klein-4b ceiling
  family), cpu_threads 8, disk_gb 8, est_wall_s 5400, timeout_s 10800.
- Admission state at final check: **queued, unassigned**; scheduler detail: `unschedulable:
  beast: ram: need 21450MB (ceiling) > avail 21183MB` — correct: it waits.
- Queue at that moment: running on beast `job-9a1e94869dcd`
  (flux2-reference-joint4-image-call2-causal-paraphrase-v1, prio 82, ram 22000); queued #1
  `job-252152a9be31` (T2 causal replication, prio 82), **#2 this job**, #3 `job-38b8f48b15fc`
  (klein-base prepare, prio 0). This job sits behind both T2 causal jobs and displaced nothing.
- Receipt: `flux2-typography-behavior-atlas-discovery-job.json`.
- Expected report: `/mnt/big/sweep-logs/bfl-flux2-lineage-v1/typography-behavior-atlas-v1/discovery/job-13e485fa9139/report.json`.

## 2026-07-31 later — discovery attempt 1 FAILED at t+4s; runner fixed; retry running [MEASURED]

- `job-13e485fa9139` failed 4.1s after start (state verified live; failure record retained as
  `flux2-typography-behavior-atlas-discovery-job-failed-job-13e485fa9139.json`). Traceback:
  `AttributeError: 'NoneType' object has no attribute '__dict__'` inside
  `dataclasses._is_type` while exec'ing the capture runtime copy.
- Root cause (reproduced locally before fixing): `_pipeline_runtime()` loaded the
  dataclass-bearing capture module via `spec_from_file_location` + `exec_module` WITHOUT
  registering it in `sys.modules` first. Dataclass processing resolves string annotations
  (`from __future__ import annotations`) through `sys.modules[cls.__module__]`, which returns
  None for an unregistered module. The counting program never hit this because it imports the
  capture module through `importlib.import_module` (which registers).
- Fix: new `_load_module_from_path(name, path)` in the runner — registers the module in
  `sys.modules` under the stable name `run_flux2_semantic_port_summary_capture` BEFORE exec,
  pops it on failure, reuses a cached instance, and fails closed on name collisions. The same
  registered idiom was applied to the selection compiler and both test loaders (audited: the
  submitter's `importlib.import_module` was already safe; no other dynamic imports exist).
- Regression test added (`test_dynamic_module_loader_registers_in_sys_modules`): reproduces the
  exact failure shape on a synthetic dataclass module (unregistered exec raises
  AttributeError), then asserts the fixed helper loads, registers, caches, rejects collisions,
  and cleans up after a failed exec. Suite now **14 passed**; ruff clean.
- Frozen panel byte-untouched: `scripts/flux2-typography-behavior-atlas-v1.json` sha256 still
  `b3b0de72cd59d75b1a89e6666fde192b96a5cd50d65c8b3a6698a3fd3cab220e`, fingerprint
  `18fc7cba66bbf4fb66e6fad1b29079b8f81ca100c3146b321954183ee385e6f3`. Runner-code fix only
  (worker sha now `d81d1bc37423ada2caebd288c9bc766f44bed4880dff0730bf847237bc3fccbd`).
- Resubmitted with the SAME reservation (ram 19500 / vram 9900 / est_wall 5400 / timeout 10800,
  priority 40): **`job-42570022d2bb`**, experiment
  `flux2-typography-behavior-atlas-v1-discovery-retry1`, receipt
  `flux2-typography-behavior-atlas-discovery-job-retry1.json`. Admission verified live: beast
  was idle and the job went **running** on beast within seconds of submission (started_ts
  1785548657), and was verified still running at t+92.7s — past attempt 1's t+4.1s crash
  point, so the capture-runtime import now succeeds. Expected report:
  `/mnt/big/sweep-logs/bfl-flux2-lineage-v1/typography-behavior-atlas-v1/discovery/job-42570022d2bb/report.json`.

## 2026-07-31 later-2 — offload throughput kills retry1; two-phase resident rework [MEASURED]

- `job-42570022d2bb` was measured at ~56s/pair (coordinator measurement: 7 pairs in 475s incl.
  load; worker pinned single-core, GPU 12%, 8074MiB resident): 256 pairs -> ~4h vs the 10800s
  timeout. Root cause: study-row `load_strategy: model_cpu_offload` shuttles the 8GB Qwen3
  text encoder and 7.8GB denoiser CPU<->GPU on every pipeline call.
- Salvage BEFORE kill: 7 complete pairs (14 PNGs, presence-plain seeds 76001/76013/76021 x
  open/exit + 76031-iopen) copied to `results/salvage-job-42570022d2bb/`; sealed as parity
  oracle `scripts/typography-parity-manifest-job-42570022d2bb.json` (content sha
  `38174e0513b8e1fcab5c69c8fc5a4dea7e441aecb770437fba4a4dff05644430`), built by
  `scripts/build_typography_parity_manifest.py` (pixel hashes recomputed from lossless PNGs).
- Kill: scheduler had already marked the job `lost`; cancel POSTed; the still-alive worker
  process (our own tenant, PID-verified by cmdline) was SIGTERMed on beast; GPU verified free
  of our processes afterward. No other tenant touched.
- Two-phase resident execution implemented (runner-code only; panel byte-untouched):
  - Phase A: `remove_all_hooks()`, text encoder resident on GPU, SERIAL per-prompt encoding
    (batch of one, exactly the offload path's per-call math; padding fixed at max_length 512),
    prompt-string dedupe (24 unique prompts across the 256-pair discovery panel), embeds cached
    on CPU in produced bf16 (bit-exact round trip).
  - Phase B: text encoder off, denoiser+VAE resident, serial generation from cached embeds via
    the pipeline `prompt_embeds` path (encode_prompt rebuilds text_ids deterministically from
    embeds; `do_classifier_free_guidance` False at guidance 1.0; `_execution_device` resolves
    to cuda because vae is the first registered module). Seeds, scheduler, steps, guidance,
    resolution, OCR untouched. `__call__` encode defaults (max_seq 512, out layers 9/18/27)
    asserted against the live signature fail-closed.
  - New `--mode parity`: runs exactly the manifest's pair_ids through the two-phase path and
    requires pixel_sha256 EQUALITY per arm; report written first (evidence), then fail-closed.
    Reports now carry an `execution` block with per-phase wall/RSS/VRAM peaks and per-pair
    seconds for honest resizing.
- Tests: **17 passed** (adds unique-prompt dedupe incl. cross-family collapse, manifest
  build/verify/torn-pair exclusion, parity row subsetting + bogus-pair rejection, parity
  match/mismatch block, sealed salvage manifest binds to the frozen panel); ruff clean.
- Parity gate submission: first ask `job-7a7d53330525` (vram 14500) was measured unschedulable
  — the scheduler's 1.1x ceiling (15950MB) cannot fit the 16376MB card against any nonzero
  tenant baseline; that ask was over-fat for this card, not honest headroom. Cancelled it (own
  tenant) and resubmitted as **`job-a70371475e10`** with component-accounted vram 12500
  (expected phase-B peak ~10GB +25% headroom; reasoning sealed in the reservation source) and
  ram 19500 unchanged. Verified queued at prio 40 behind bob's prio-100 cert job and ahead of
  the prio-0 T3 cert jobs by normal priority ordering — nothing displaced. Discovery
  resubmission is GATED on parity all_match plus measured reservations.

## 2026-07-31 later-3 — hand-rolled two-phase abandoned for engine phase-cuda [MEASURED]

- Parity job `job-a70371475e10` (our hand-rolled two-phase) FAILED: device mismatch in
  `linear_1` — the manual phase swap left a module path (timestep/guidance embedder) on CPU.
  Not debugged further: a parallel track landed the same idea properly inside mrun.
- Switched to `mrun.diffusion.PhasePipeline` via the image_atlas opt-in
  `load_strategy: "phase-cuda"` (beast-side; engine parity evidence `job-eac6b216a07c`:
  parity_pass true bitwise vs model_cpu_offload, 0.61s/image at 512px/4 steps, denoise-phase
  VRAM peak 8583.3MB, encode-phase 8321.8MB, 10.66x per-image / 6.25x end-to-end).
- Runner rework (runner-code only; frozen panel byte-untouched, still
  `18fc7cba66bbf4fb66e6fad1b29079b8f81ca100c3146b321954183ee385e6f3`):
  - removed all runner-local residency machinery (remove_all_hooks/manual .to/embed cache) and
    the capture-runtime copy + its loader (obsolete with the engine path);
  - `_load_phase_pipeline`: mirrors the counting custody exactly (study row identity,
    revision, artifact bytes, dtype, OneModelLoadGate) and overrides load_strategy to
    phase-cuda IN MEMORY only — the study row on disk is immutable; requires the PhasePipeline
    wrapper back, records the override + engine evidence in runtime_binding;
  - `precompute(unique_prompts)` (24 unique prompts, serial batch-of-one) then duck-compatible
    per-pair calls that hit the embed memory cache; fail-closed custody:
    encode_calls == unique prompts and unplanned_swaps == 0;
  - parity mode (salvaged-oracle pixel_sha256 equality, fail-closed after sealing evidence)
    unchanged — the engine's own smoke does NOT substitute for this panel's oracle gate.
- Tests **17 passed**, ruff clean.
- Parity gate resubmitted: **`job-5a13d598c7fb`** (vram 11000 = engine-declared envelope over
  measured 8583.3 + TrOCR; ram 19500 precedent ceiling; PYTHONPATH now includes
  /home/beast/domains/mrun/src). Queued at prio 40 behind a running prio-100 tenant (verified
  live). Discovery resubmission remains GATED on this panel's parity all_match + measured
  peaks.

## 2026-07-31 later-4 — parity PASS bitwise; discovery running on measured envelope [MEASURED]

- Parity job **`job-5a13d598c7fb`** SUCCEEDED (total wall 29.7s). We verified the sealed report
  myself (`.../parity/job-5a13d598c7fb/report.json`, content seal
  `02669eac58fb350b41cf...`, canonical recomputation matches): **parity all_match TRUE — 7/7
  salvaged pairs, both arms, pixel_sha256 equal bitwise** against the model_cpu_offload
  oracle. Custody clean: strategy phase-cuda, unplanned_swaps 0, encode_calls == 3 unique
  prompts. Measured: phase A 5.5s/3 prompts; steady-state **1.19-1.21 s/pair including OCR**
  (first pair 7.8s warmup); VRAM alloc peak 8303MB / reserved 8484MB; RSS peak 16539MB.
  (Incidental behavior signal, parity-only rows: 4/7 presence-plain pairs ADMITTED by OCR —
  typography behavior is not all-fail at 4 steps on the easy family.)
- Discovery resubmitted on the measured envelope: **`job-d32bf4b13094`**, ram 18000 (measured
  16539 + margin; dropped from 19500 only to above-measured), vram 9900 (measured 8484 +
  klein-family ceiling), est_wall 1200, priority 40. Verified live: admitted immediately,
  RUNNING on beast, queue otherwise empty. Expected ~10-12 min.

## 2026-07-31 later-5 — discovery MEASURED, selection sealed, confirmation MEASURED, CERTIFICATE PASS

- Discovery **`job-d32bf4b13094`** succeeded; sealed report verified digit-for-digit
  (`e4fd99b7b655302f...`, canonical recomputation matches; config fingerprint bound). 125/256
  pairs admitted; all-fail NOT triggered — the 4-step all-fail contingency is moot. Execution:
  phase-cuda, 0 unplanned swaps, 24-prompt encode 3.0s, mean 1.200 s/pair, VRAM reserved
  8484MB, RSS 16750MB. Family results (n=32 each; rate / Wilson-lower / upper-exact):
  spell-plain .9375/.7985/.9375; spell-spec .9062/.7578/.9375; presence-plain .5/.3363
  (lexically gated: open .9375 vs exit .0625); presence-spec .5/.3363 (open 1.0, exit 0.0);
  substitution-spec .4688/.3087 (open-closed .8125, push-pull .125); substitution-plain
  .0938; append-spec .3438 (open-now .6875, exit-only 0.0); append-plain .1562.
- Selection sealed by the frozen policy (`flux2-typography-behavior-selection-v1.json`,
  `b0f205c0006a95ce...`): presence-plain, substitution-spec, append-spec, spell-plain ->
  192 confirmation pairs. Policy decided (margin tie-break gave presence-plain; spell-plain
  beat spell-spec on rate).
- Confirmation **`job-5bc3ca2850ed`** succeeded on the measured envelope (ram 18000 / vram
  9900; actual RSS 16726MB, VRAM 8484MB, 1.216 s/pair); sealed report verified
  (`cd9fbb5491e5e965...`, selection seal bound). 113/192 admitted. AUTHORITATIVE gates:
  **spell-plain PASS** (39/48 = .8125, Wilson-lower .6806, instantiations 1.0/.875/.5625,
  seed min .333); presence-plain FAIL only rate_per_instantiation (exit .1875 < .25; sale
  held-out hit 1.0); substitution-spec FAIL only rate_per_instantiation (push-pull .0625;
  stop-slow held-out .75); append-spec FAIL broadly (exit-only 0.0, Wilson-lower .1995).
- **Behavior certificate: PASS** — `flux2-typography-behavior-certificate-v1.json`, content
  seal `61f17553e4ab89f079233f6d9c15e3c2c62a5a11863c307abc3f8fd30b10e0d0` (file sha
  `6abfb0b5c65024...`), admitted family `spell-plain` only; non-admitted families sealed with
  their measured gating profiles. Compiler re-derives admission from records and verifies the
  full discovery->selection->confirmation seal chain; 18 CPU tests pass, ruff clean.
- Port-ranking leg DESIGN frozen: `PORT_RANKING_PLAN.md` sha256
  `fe5d806df178c30f89c10a1901818c156ba8def9874391936699935d669ca80a` — spell-plain substrate,
  counting-shape capture sites + max-T over seeds, and MANDATED three-resolution reporting
  (pooled / per-instantiation / per-seed-block) with per-cell Wilson admission and NO
  universality gates; hard open gate: capture-instrument parity under phase-cuda (or run
  captures under offload at measured cost) before any outcome-bearing capture.

### Gated (updated)

- Port-ranking IMPLEMENTATION (capture smoke, capture job, sealed ranking): gated on the
  frozen plan's capture-parity gate; not started.
- Causal panels and replication: gated on the sealed ranking; per-cell design per the frozen
  plan. No causal script exists in this workspace.
- (Earlier gates now CLOSED with sealed artifacts: selection <- discovery `e4fd99b7...`;
  confirmation <- selection `b0f205c0...`; certificate <- confirmation `cd9fbb54...`.)
