# PREREG — E7: recovering the unpaired aligner on DCI/DOCCI (search/initialization, few pairs, pairs-free selection)

Written 2026-10-23 before any E7 Beast job touched real-model data. This pre-registration is frozen on submission of the first scored job; any scorer/threshold change after seeing a scored number is labelled POST HOC.

## Question

E6b proved (true-pair orthogonal-Procrustes oracle) that the geometry is rotation-alignable on all three long-caption corpora (holdout FOSCTTM 0.009 SPC / 0.014 DCI / 0.010 DOCCI, 0.007/0.010/0.007 with the top gen PC removed), yet Schnaus et al.'s unpaired aligner on Qwen3-8B generative-pooling ("gen") stays near chance off SPC (DCI 0.479 / DOCCI 0.474; pc0-removed 0.391 / 0.478; 8 restarts best 0.280 / 0.341). The failure is the unpaired SEARCH/initialization, not the geometry. **Can a change to the initialization, a few true pairs, or a pairs-free selection recover gen on DCI and DOCCI, so the note can offer a working improvement rather than only a diagnosis?**

## Primary metric and protocol

Holdout FOSCTTM on the SAME split as E5/E6: their `disjoint_split(n - holdout, Randomness(seed))` two unpaired halves; holdout = the last `holdout = 2000` rows; score with their `retrieval_metrics` (shuffle seed = run seed). Their library at commit fdfad84 used unchanged for the aligner, geometric initialization, splits and metric. Vision = DINOv2 ViT-B/14 mean. Language = gen unless stated. Seed 0 by default. All compute on Beast via mrun, CPU, threads capped (<= 4 OMP/MKL/torch). Chance = 0.5. Oracle ceiling and control encoders (Qwen3-Embedding, MPNet) already MEASURED in E6/E6b and cited; Arm A re-measures the Qwen3-Embedding pivot as its own control.

## Arms (frozen). Code: `e7_search_init/arms.py` (sha in the job report). The only change per arm is the init / known pairs / post-hoc selection; the refinement path is their `refinement_step`.

- **A — pivot init, no image-text pairs.** Fit a rotation `R` from gen to Qwen3-Embedding on the SAME captions (text-text, row i == row i; within one modality, uses no image-caption pair). Fit the unpaired DINOv2<->Qwen3-Embedding map `W_emb` with their method (the pivot they already find well). Compose `W_init = W_emb @ R` (DINOv2 -> gen). Report `A_compose` (use `W_init` directly, no refinement) and `A_refine` (their refinement from `W_init`). Controls in the same job: `A_emb_pivot_control` (W_emb's own FOSCTTM, should reproduce ~0.09) and `A_text_text_emb_to_gen` (R's within-text FOSCTTM, should be very low). gen, candidate none, DCI and DOCCI.
- **B — transfer init.** The SPC-fit gen rotation (candidate none and pc0), fit once, applied to DCI/DOCCI directly (`B_transfer`, no refit — the e6b transfer measurement extended to these corpora) and as the init for refinement on the target with the target's pc0 projection (`B_refine`). Label: pairs were used, but on a DIFFERENT corpus (SPC). DCI and DOCCI.
- **C — few true pairs (their Sec 4.4 protocol).** k in {1, 5, 10, 50, 100} true pairs drawn with their `sample_pairs` from the training pool, woven by their `procrustes` into the initialization and every refinement step. candidate none (raw) primary; pc0 (axis removed) secondary. gen, DCI and DOCCI. Report the smallest k that recovers.
- **D — pairs-free search tweaks.** Remove the top-k gen PCs cumulatively, k in {2,3,4,5} (k=0,1 = none/pc0 already in E6), selected by the pairs-free S1 matched-cosine score already in our code. gen, DCI and DOCCI. (E6b showed 8 restarts and individual PCs do not help; this is the cumulative-k branch E6b did not run.)
- **E — pairs-free SELECTION of the fixed run (coordinator addendum, folded in before any job).** Their `_fit` returns the LAST of `num_iterations=100` refinement iterates with no selection (verified at fdfad84, `wasserstein_procrustes.py` ll. 98-125); their paper reports the mean over seeds and calls unsupervised model selection an open problem (Sec 4/5). For the BASELINE aligner (no init change) on gen, Qwen3-Embedding and MPNet, and corpora SPC, DCI, DOCCI (COCO best-effort), log at every iterate both the pairs-free S1 matched-cosine (on a fixed training subsample) and the true holdout FOSCTTM. Score (i) best-iterate-by-S1 vs the last iterate, and, using multiple seeds (gen baseline seeds 0-2 plus the E6b 8-seed gen-pc0 restarts), (ii) best-seed-by-S1 vs the mean/last over seeds. Report how often S1 selection beats last/mean on true FOSCTTM, by how much, and the S1-vs-FOSCTTM correlation.

## Hypotheses / PASS-FAIL thresholds (frozen). Success = gen FOSCTTM < 0.10 on BOTH DCI and DOCCI (the control encoders' level).

- **H-A:** `A_compose` OR `A_refine` gen < 0.10 on both DCI and DOCCI -> a WORKING no-image-text-pairs fix. (ASSERTED prior: likely, since W_emb works ~0.09 and R is near-exact text-text.)
- **H-B:** `B_transfer` or `B_refine` gen < 0.10 on both -> a working fix using only a different corpus's pairs. (Prior: e6b showed SPC->COCO transfer 0.022; plausible.)
- **H-C:** some k <= 100 gives gen < 0.10 on both; report the minimal such k. (Prior: their Sec 4.4 recovered with ~100 pairs on COCO.)
- **H-D:** best-S1-selected cumulative-drop < 0.10 on both. (Prior from E6b: FAIL expected; reported with the full spread, asymmetric-skepticism bar.)
- **H-E:** best-iterate-by-S1 and/or best-seed-by-S1 is within 0.05 of the best achievable and beats the last/mean iterate by a material margin on gen DCI/DOCCI; else pairs-free selection does not rescue the fixed run.

**Kill condition (from the E6b dossier, specialised):** the off-SPC failure is a search failure. If NO arm (A, B, C with k<=100, D, E) brings gen below 0.10 on both DCI and DOCCI, E7 cannot offer a working unpaired or few-pair recovery and the note stays a diagnosis (the search-limitation claim is unrevised). A single arm meeting the bar on both corpora overturns "no working fix".

## Named nulls / controls / canaries

- Qwen3-Embedding and MPNet stay well aligned on DCI/DOCCI (E6: emb 0.093/0.096). Arm A re-measures the emb pivot (canary: `A_emb_pivot_control` <= ~0.12).
- `A_text_text_emb_to_gen` must be low (the text-text rotation is real), else A's composition is uninterpretable.
- Oracle ceiling (E6b): gen-pc0 orth 0.0097 DCI / 0.0068 DOCCI; any arm is judged against this and chance 0.5.
- Negative control (synthetic, in the laptop smoke): a seeded map against an unrelated Y gives FOSCTTM ~0.5 (MEASURED 0.514).
- Seed canary: an arm claimed as a fix is re-run at seeds 1,2 (3 total) before the note cites it.

## Smoke checks (frozen; run before any scored number)

1. **Laptop synthetic smoke** (`--synthetic-smoke`, synthetic tensors only, no real model/data): (a) `SeededWassersteinProcrustes` seeded with the true rotation and no refinement recovers it (FOSCTTM < 0.02); (b) seeded with a perturbed rotation + refinement stays aligned (< 0.10); (c) a seeded map against an unrelated Y is near chance (> 0.35); (d) the trace path emits per-iterate S1 and FOSCTTM; (e) text-text Procrustes recovers a known rotation (< 1e-3). MEASURED 2026-10-23: 0.0 / 0.0 / 0.514 / trace_len 6 / err 7.3e-6 — all pass.
2. **Beast smoke job** (`--smoke`, tiny aligner config): each arm runs end to end on DCI, with the frozen `e6_generality.sweep.smoke_gate` data checks (finite unit-norm rows; a tiny fit returns finite FOSCTTM in [0,1]); abort on failure. Never cited for a result.

## Fast-run / scoring discipline

Scored jobs are sized to a few full fits each (one full Wasserstein-Procrustes fit MEASURED at ~6-14 min on 4 threads under contention); timeouts generous (up to 90 min) because Beast is shared. Single seed per arm; extra seeds (max 3) only for an arm that meets the bar on a paper-relevant claim. Any threshold/scorer change after a scored number is POST HOC. Every shipped file's sha256 and the manifest are recorded in each job report.

## Pre-registration looks (local runs that touched real models or real data: NONE)

- `--synthetic-smoke` ran on the laptop on synthetic `torch.randn` tensors only; no real model loaded, no real embedding read. No real-model or real-data run happened locally. All real-data execution is on Beast via mrun.
