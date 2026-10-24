# E7 — recovering the unpaired aligner on DCI/DOCCI (search/init, few pairs, pairs-free selection)

Builder notes (coordinator writes FINDINGS.md). PREREG: `PREREG.md` (sha in each job report), frozen before any scored job. All numbers MEASURED on Beast via mrun (CPU, 4 threads), receipts under `../results/e7_search_init/`. Oracle ceiling and control encoders cited from E6/E6b. This file: short version, then method, results table, verdict vs PREREG, controls, deviations, caveats, how-to-continue.

## Short version (plain language)

E6b proved the geometry is fine (true-pair oracle aligns gen to DINOv2 at FOSCTTM ~0.01 on all three corpora); the off-SPC failure is the unpaired SEARCH. E7 tests fixes. [FILL after collection: which arm(s) bring gen on DCI and DOCCI below 0.10, and whether any needs no image-caption pairs.]

## Method (frozen in PREREG; code `arms.py`)

Same split/metric as E5/E6: their `disjoint_split(n-2000)` two unpaired halves, holdout = last 2000 rows, their `retrieval_metrics` FOSCTTM, seed 0, their library at fdfad84 unchanged for the aligner/init/metric. Row counts (MEASURED from E6b receipts): SPC train 17561, DCI 5805, DOCCI 12847; holdout 2000 each. One full Wasserstein-Procrustes fit ~6-14 min on 4 threads under contention (MEASURED from E6 job durations).

- **A (pivot, no image-text pairs):** R = orthogonal Procrustes gen->Qwen3-Embedding on the same captions (text-text, row i==row i, within-modality); W_emb = their unpaired DINOv2<->Qwen3-Embedding map; init = W_emb @ R (DINOv2->gen). `A_compose` = init used directly (no refinement), `A_refine` = their refinement from init. Controls in-job: `A_emb_pivot_control`, `A_text_text_emb_to_gen`.
- **B (transfer):** SPC-fit gen rotation (none, pc0), applied to DCI/DOCCI directly (`B_transfer`) and as a refinement init on the target (`B_refine`, pc0). Pairs used, but on a different corpus.
- **C (few true pairs, their Sec 4.4):** k in {1,5,10,50,100} true pairs woven by their `procrustes` into init + every refinement step. candidate none primary, pc0 secondary.
- **D (pairs-free):** cumulative top-k PC removal, k in {2,3,4,5}, select by pairs-free S1 (k=0,1 = none/pc0 from E6).
- **E (pairs-free selection of the fixed run):** baseline aligner (no init change), per-iterate S1 + true holdout FOSCTTM logged over the 100 refinement iterates, gen/emb/mpnet on SPC/DCI/DOCCI (seed 0); multi-seed for the seed-selection question. Their `_fit` returns the LAST iterate with no selection (verified fdfad84 ll. 98-125); paper reports mean-over-seeds and calls unsupervised selection open (Sec 4/5).

## Is Arm A "unpaired" under their definition?

Their unpaired setting means no IMAGE-CAPTION (cross-modal) correspondence is used. Arm A uses a second TEXT encoder on the SAME captions; the correspondence it exploits (which gen row and which emb row are the same caption) is within one modality and is free — you encoded the same caption text twice. So A uses zero image-caption pairs. Whether their framework "allows" a second same-modality encoder is a scoping question for the authors: their Sec 4.4 few-pair setting uses cross-modal pairs; a text pivot is a different, cheaper resource (no human labelling, no image-text matching). I label this arm "no image-text pairs" and flag the second-encoder assumption explicitly. [Their exact Sec 3-4 wording: ASSERTED from the reimplementation + response.md; not re-read from the arXiv PDF in this session.]

## Smoke (passed; not cited for results)

- Laptop synthetic (`--synthetic-smoke`, synthetic tensors only): seeded-true-rotation FOSCTTM 0.0; seeded-perturbed+refine 0.0; negative control 0.514 (chance); text-text Procrustes err 7.3e-6; trace emits per-iterate S1+FOSCTTM. MEASURED 2026-10-23.
- Beast smoke (tiny config, 5 arms on DCI, job ids below): all succeeded, smoke_gate passed, finite in-range FOSCTTM for every arm path. Tiny-config numbers (NOT cited) already hinted: A_text_text R=0.0002 (pivot building block near-exact); C k=100 0.058 / k=50 0.077 on DCI; E gen corr(S1,-FOSCTTM)=0.605. Smoke receipts: `e7_arm{A..E}-*-smoke-*.json`.

## Results

[FILL after collect: table arm x corpus (x encoder for E) -> FOSCTTM, with receipts + job ids. Oracle ref: gen-pc0 orth 0.0097 DCI / 0.0068 DOCCI; chance 0.5; control emb unpaired 0.093/0.096 (E6).]

## Verdict vs PREREG

[FILL: H-A/H-B/H-C/H-D/H-E PASS/FAIL; kill condition; minimal recovery k for C.]

## State / how to continue (if out of turns)

- Tunnel: `ssh -o BatchMode=yes -o ExitOnForwardFailure=yes -f -N -L 19025:127.0.0.1:9025 beast`; `export MRUN_URL=http://127.0.0.1:19025`; run mrun-client Python with Bash option dangerouslyDisableSandbox.
- Scored jobs submitted 2026-10-23 ~22:20 PDT (plans A,C,B,E,D; 10 jobs) — see `../results/e7_search_init/jobs.json` for ids/args.
- Collect: `~/domains/common/bin/common exec python e7_search_init/submit.py --collect` (writes receipts into ../results/e7_search_init/, updates jobs.json). Note: run the SUBMITTER with `common exec python` (mrun client env); run the ARMS module only on Beast via mrun, or locally only with `.venv/bin/python` and ONLY `--synthetic-smoke`.
- Analyze: `.venv/bin/python e7_search_init/analyze.py` (reads receipts; prints the A/B/C/D table and the E trace-selection table).
- Not yet submitted (do if an arm is borderline / budget): `--plan Cpc0` (few pairs + axis removal), `--plan Emulti` (gen baseline seeds 1,2 for seed-selection). For any arm that MEETS the bar on both corpora, add seeds 1,2 (3 total) before the note cites it (rule 8).
- Do NOT touch Circuit-Diff jobs (experiment e6-circuit-tracer / cd-native) or the spf-sat job. No commits/push/contact.
