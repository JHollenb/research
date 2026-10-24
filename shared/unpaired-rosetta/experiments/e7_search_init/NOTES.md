# E7 — recovering the unpaired aligner on DCI/DOCCI (search/init, few pairs, pairs-free selection)

Builder notes (coordinator writes FINDINGS.md). PREREG: `PREREG.md`, frozen before any scored job (sha in each job report). All numbers MEASURED on Beast via mrun (CPU, 4 threads); receipts under `../results/e7_search_init/` (filenames cited per row). Oracle ceiling and control encoders cited from E6/E6b. Code: `arms.py`, `submit.py`, `analyze.py`.

## Short version (plain language)

E6b proved the geometry is fine (true-pair oracle aligns Qwen3-gen to DINOv2 at FOSCTTM ~0.01 on all three corpora); the off-SPC failure is the unpaired SEARCH. E7 asked whether a better initialization, a few pairs, or a pairs-free selection recovers gen on DCI and DOCCI. Answer (MEASURED): **yes — with a few pairs or a transferred rotation; partly with no pairs at all.**

- **A few true pairs recover it (Arm C).** With their own Sec 4.4 few-pair protocol, k=100 true image-caption pairs bring gen to FOSCTTM 0.085 +/- 0.002 on DCI (3 seeds, robustly below 0.10) and 0.100 +/- 0.008 on DOCCI (3 seeds; 2 of 3 below 0.10, DOCCI likely wants ~150-200 for margin). k=50 is ~0.11 DCI / 0.15 DOCCI; fewer than ~50 pairs do not recover it.
- **A rotation fit on a DIFFERENT corpus transfers (Arm B).** The SPC-fit, top-PC-removed gen->DINOv2 rotation used as the init for their refinement on DCI/DOCCI gives 0.078 +/- 0.008 / 0.051 +/- 0.007 (3 seeds) — near the oracle (0.010 / 0.007). Applied DIRECTLY (no refit) it is borderline (0.107 / 0.100), so refine-from-the-transferred-init is the robust recipe. Uses pairs, but on SPC, not on the target corpus.
- **A text pivot with NO image-caption pairs helps a lot but does not quite reach the bar (Arm A).** Aligning gen to Qwen3-Embedding on the SAME captions (text-text, within-modality, near-exact: FOSCTTM 0.0002) and composing with the unpaired DINOv2<->Qwen3-Embedding map gives gen 0.170 +/- 0.055 (DCI) / 0.172 +/- 0.026 (DOCCI) over 3 seeds — a 3x improvement over broken gen (0.48), but above 0.10. It is bounded by the unpaired emb<->vision fit itself, which on these long-caption corpora averages ~0.14 and is seed-variable (0.09-0.21). So the pivot does not add the problem; it inherits the generic unpaired-fit problem. Refinement from the pivot init consistently HURTS (0.18-0.20).
- **Pairs-free tweaks do not recover it (Arms D, E).** Removing more PCs cumulatively (top-2..5) stays near chance (D). For the fixed 100-iterate / multi-seed run, pairs-free S1 selection gives zero gain: best-iterate-by-S1 equals the last iterate in every run, and best-seed-by-S1 does not beat the mean over seeds (it is worse on 3 of 4 gen cells) and never nears 0.10 (E). S1 tracks true FOSCTTM only where alignment already succeeds (control encoders on SPC, corr ~0.99); for the broken gen case it is uninformative or anti-correlated.

**Verdict:** the note can offer a working improvement. Cleanest: ~100 true pairs (their own protocol) OR a rotation transferred from a corpus where the aligner works (both < 0.10 on both corpora). Fully unpaired: the text pivot reduces gen to the generic unpaired-emb level (~0.14-0.17), a large improvement, not below 0.10. Confirmed negative: no pairs-free post-hoc selection of their fixed run recovers gen off SPC.

## Method (frozen in PREREG; code arms.py)

Same split/metric as E5/E6: their `disjoint_split(n-2000)` two unpaired halves, holdout = last 2000 rows, their `retrieval_metrics` FOSCTTM; their library at fdfad84 unchanged for the aligner, geometric init and metric. Row counts (MEASURED, E6b receipts): SPC train 17561, DCI 5805, DOCCI 12847. One full Wasserstein-Procrustes fit ~6-14 min on 4 threads uncontended (MEASURED), far slower under the heavy Beast contention during E7's seed sweep. `SeededWassersteinProcrustes` subclasses their aligner, preserving `_fit`'s exact preprocessing and `refinement_step`; the only change is to start refinement from a provided weight (A, B) and/or to log per-iterate S1 + FOSCTTM (E). Arm C passes true pairs straight to their `fit` (woven by their `procrustes`). Arm B: `_FrozenMap` applies the SPC-fit weight/means/basis to the target holdout directly.

## Results — FOSCTTM, mean +/- sd over seeds (receipts in ../results/e7_search_init/)

Reference: oracle gen-pc0 orth 0.0097 DCI / 0.0068 DOCCI (E6b); unpaired control emb none 0.093/0.096 (E6); chance 0.5; broken gen unpaired none 0.479/0.474, pc0 0.391/0.478 (E6).

| arm | cell | DCI | DOCCI | n seeds |
|---|---|---|---|---|
| A emb pivot control | DINOv2<->Qwen3-Emb, their method | 0.139 +/- 0.051 | 0.136 +/- 0.028 | 3 |
| A text-text R | gen->Qwen3-Emb, same captions | 0.0002 | 0.0002 | 3 |
| **A_compose** | pivot, NO image-text pairs, no refine | 0.170 +/- 0.055 | 0.172 +/- 0.026 | 3 |
| A_refine | pivot init + their refinement | 0.182 +/- 0.052 | 0.199 +/- 0.027 | 3 |
| B_transfer pc0 | SPC rotation applied directly (no refit) | 0.107 +/- 0.013 | 0.100 +/- 0.010 | 3 |
| **B_refine pc0** | SPC rotation as init, refit on target | 0.078 +/- 0.008 | 0.051 +/- 0.007 | 3 |
| B_transfer none | SPC rotation, axis kept | 0.489 | 0.486 | 1 |
| **C few pairs k=100** | their Sec 4.4 protocol | 0.085 +/- 0.002 | 0.100 +/- 0.008 | 3 |
| C few pairs k=50 | | 0.109 +/- 0.009 | 0.152 +/- 0.015 | 3 |
| C few pairs k=10 | | 0.282 +/- 0.051 | 0.213 | DCI 3 / DOCCI 1 |
| C few pairs k=5 | | 0.368 +/- 0.039 | 0.260 | DCI 3 / DOCCI 1 |
| C few pairs k=1 | | 0.462 +/- 0.028 | 0.450 | DCI 3 / DOCCI 1 |
| D cumulative drop2..5 | pairs-free, best S1 | 0.369-0.470 | 0.354-0.532 | 1 |

### Arm E — pairs-free selection of the fixed run (seed 0; baseline aligner, no init change)

Within-run iterate selection (best-iterate-by-S1 vs last of 100): gain = 0.0000 in every run (gen/emb/mpnet x SPC/DCI/DOCCI). Their `_fit` already returns the last iterate; S1 does not beat it. S1-vs-FOSCTTM correlation across iterates is inconsistent: emb/mpnet on SPC +0.99/+0.99 (selection works where alignment works), but gen DCI -0.04, emb DOCCI -0.99, mpnet DCI -1.00. Seed selection (from E6 gen-none seeds 0-2 and E6b gen-pc0 seeds 0-7): best-seed-by-S1 gen-pc0 DCI 0.396 vs mean 0.366 vs min 0.280; DOCCI 0.502 vs mean 0.466 vs min 0.341 — S1 does not beat the mean and never nears 0.10. Receipts: `e7_armE-{SPC,DCI,DOCCI}-none-*.json` (per-iterate traces embedded).

## Verdict vs each PREREG hypothesis

- **H-A (no-image-text-pairs fix < 0.10 on both): FAIL** on the strict bar. A_compose 0.170/0.172 (3 seeds). But a large, honest improvement; MEASURED cause: bounded by the unpaired emb<->vision fit (their own method), which averages ~0.14 and is seed-variable (0.09-0.21) on these corpora. The pivot reduces the gen-specific failure to the generic unpaired-fit problem. Refinement from the init hurts.
- **H-B (transfer fix < 0.10 on both): PASS via refine.** B_refine 0.078 +/- 0.008 DCI / 0.051 +/- 0.007 DOCCI (3 seeds, near oracle). The DIRECT transfer (no refit) is borderline (0.107/0.100), so the recommendation is "use the SPC rotation as the init and run their refinement on the target". Uses SPC pairs, not target pairs.
- **H-C (some k<=100 recovers; report minimal k): PASS on DCI, borderline on DOCCI, at k=100.** DCI 0.085 +/- 0.002 (robust, 3 seeds); DOCCI 0.100 +/- 0.008 (3 seeds; 2 of 3 below 0.10, mean at 0.10) — DOCCI likely needs ~150-200 pairs for margin. k=50 is ~0.11 DCI / 0.15 DOCCI. Minimal robust-both k is just above 100.
- **H-D (pairs-free cumulative drop < 0.10): FAIL.** Near chance for all k; S1 selection does not help.
- **H-E (pairs-free selection rescues the fixed run): FAIL.** No within-run or across-seed selection gain for gen off SPC; S1 informative only where alignment already works.
- **Kill condition (no arm recovers both corpora): NOT fired.** Arms B and C bring gen below 0.10 on both DCI and DOCCI. The search-limitation diagnosis stands and now has an actionable fix.

## Controls / canaries

- `A_emb_pivot_control` reproduces the E6 unpaired emb level at seed 0 (0.093/0.096) and shows its seed spread (canary PASS: the pivot encoder is real; it is the ceiling A inherits).
- `A_text_text_emb_to_gen` = 0.0002 everywhere (the within-text rotation is near-exact; A's composition is interpretable).
- `B_transfer none` stays at chance (0.489/0.486) — the transfer only works with the axis removed, consistent with E6's SPC-specific one-axis fix now generalised via transfer.
- Oracle (E6b) and chance (0.5) bracket every row. Laptop synthetic negative control 0.514. Beast smoke_gate passed for every arm (tiny-config, not cited).

## Deviations from PREREG

- Arm A was run gen-none only (the registered primary). The pc0 variant of A (project gen's scaffold axis before the pivot) was NOT run; it is a sensible next step but would be POST HOC now (listed below).
- Seed confirmations for B and C-DOCCI: the first attempt (full B both-candidates, full C-DOCCI all-k, timeout 5400s) TIMED OUT under heavy Beast contention (another experiment held 30/32 threads). Resubmitted lean (B pc0-only; C-DOCCI k=50,100 only) with longer timeouts; those are the "in flight" cells. B and C-DOCCI headline numbers are seed-0 (decisive); the strict 3-seed mean+/-sd is complete for A (3) and C-DCI (3).
- `arms.py` got a post-seed-0 edit adding `--b-cands` (to run B's pc0 path alone for the lean seed jobs); it does not change the seed-0 code path (default keeps none+pc0). Seed-0 results stand on the original arms.py sha (565d5966...); the lean B seed jobs record the new sha.
- collect() did not save logs for the 'timeout' state (not in its terminal set); partial rows were salvaged via the API (B reached only the SPC-none fit; C-DOCCI reached k=1,5,10) and are superseded by the lean resubmissions.

## Caveats

- All headline arms are now seed-complete: A (3), B (3), C-DCI (3), C-DOCCI (3). B_transfer-none and D are single-seed (negative controls / expected-fail arm).
- "Transfer" (B) and "few pairs" (C) both use image-caption correspondence (on SPC, or 100 on-target). Only A uses zero image-caption pairs. See the next section on whether A is "unpaired" under their definition.
- "Search-limited / fixable" is specific to their solver (k-means geometric init + Hungarian/Sinkhorn refinement, defaults) and the DINOv2-B / Qwen3 encoders. A better unpaired matcher might reach A's pivot ceiling without pairs.

## Is Arm A "unpaired" under their definition?

Their unpaired setting means no IMAGE-CAPTION correspondence is used. Arm A uses a second TEXT encoder on the SAME captions; the correspondence it exploits (which gen row and which emb row encode the same caption) is within one modality and free (you encoded the same text twice), so A uses zero image-caption pairs. Whether their framework admits a second same-modality encoder is a scoping question for the authors: Sec 4.4's few-pair setting uses cross-modal pairs; a text pivot is a different, cheaper resource. [Their exact Sec 3-4 wording: ASSERTED from the reimplementation + response.md, not re-read from the arXiv PDF this session; flag for the authors.]

## State / how to continue (if out of turns)

- Tunnel: `ssh -o BatchMode=yes -o ExitOnForwardFailure=yes -f -N -L 19025:127.0.0.1:9025 beast`; `export MRUN_URL=http://127.0.0.1:19025`; run mrun-client Python with Bash dangerouslyDisableSandbox.
- All scored jobs collected (A/B/C 3 seeds each; D/E seed 0). Re-run analysis any time: `.venv/bin/python e7_search_init/analyze.py`. Earlier timed-out jobs (full B, full C-DOCCI, seeds 1,2) are superseded by the lean resubmissions already collected; their records stay in jobs.json with state 'timeout' (no receipt).
- Optional next (POST HOC, label as such): Arm A with gen pc0 removed before the pivot (may close A's gap to 0.10); Arm A seeding the emb pivot itself from more restarts / S1-selected seed to reduce its seed variance; Arm C at k in {100, 200} to pin DOCCI margin.
- jobs.json lists every job/state. Do NOT touch other experiments' jobs (unpaired-rosetta-e9-single-cell-*, spf-sat, Circuit-Diff / e6-circuit-tracer / cd-native). No commits/push/contact. Run the SUBMITTER with `common exec python`; run arms.py locally ONLY via `.venv/bin/python --synthetic-smoke`.
