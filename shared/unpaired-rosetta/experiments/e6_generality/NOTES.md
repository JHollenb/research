# E6 / E6b notes

## 2026-10-22 E6b (fix-diagnosis addendum) — IN PROGRESS

Addendum PREREG: `PREREG_E6b.md` (written before any new number). Owner rule: asymmetric skepticism on the E6
negative — before the response says "the one-axis fix is SPC-specific", find out WHY the fix fails off SPC.

### DECISIVE RESULT (measured): the geometry is rotation-alignable; the failure is the unpaired SEARCH

True-pair oracle ceilings. Receipt `../results/e6_generality/e6b_oracle-20261022T223221.json`
(job-1aca147d43d7). Smoke passed: synthetic rotation recovered FOSCTTM 0.0, polar semi-orthogonality err 2e-13.

Oracle = best map GIVEN the true pairs (train on arange(0, n-2000) paired; holdout = last 2000; their
retrieval_metrics). orth = orthogonal Procrustes (ceiling of their rotation family). lin = ridge linear map.

| corpus | gen none orth | gen pc0 orth | emb none orth | gen none lin | gen pc0 lin | emb none lin |
|---|---|---|---|---|---|---|
| SPC   | 0.0092 | 0.0071 | 0.0021 | 0.0190 | 0.0100 | 0.0026 |
| DCI   | 0.0144 | 0.0097 | 0.0028 | 0.0471 | 0.0181 | 0.0034 |
| DOCCI | 0.0104 | 0.0068 | 0.0010 | 0.0292 | 0.0102 | 0.0009 |

Compare the UNPAIRED aligner (E6, measured): gen none FOSCTTM SPC 0.415 / DCI 0.479 / DOCCI 0.474; gen pc0
SPC 0.038 / DCI 0.391 / DOCCI 0.478. So:

- A single rotation aligns Qwen3-gen to the image NEAR-PERFECTLY on all three corpora (oracle-orth 0.007–0.014),
  WITH OR WITHOUT the scaffold axis removed. The pc0-removed oracle (0.0097 DCI, 0.0068 DOCCI) is far below the
  branch threshold 0.15 on BOTH → **SEARCH-LIMITED branch** (per the frozen criterion).
- Canary C1 PASS: emb none oracle ≤ 0.05 everywhere (0.0021/0.0028/0.0010) and ≤ its unpaired (0.019/0.093/0.096).
- Canary C2: first clause PASS (SPC gen-pc0 oracle 0.0071 ≤ 0.10, reproduces the SPC rescue). Second clause
  FALSIFIED: gen-NONE oracle on SPC (0.0092) is NOT clearly worse than gen-pc0 (0.0071) — the scaffold axis does
  NOT block the true-pair rotation even on SPC. Refinement (label: measured): the scaffold axis harms the unpaired
  SEARCH (it corrupts the Hungarian pseudo-match that bootstraps the rotation), not the existence of a good rotation.
- oracle-lin ≈ oracle-orth everywhere (both ~0.01–0.05) → the obstacle is NOT the orthogonality constraint either;
  a rotation suffices. The shared linear structure is present; the unpaired search just does not find it off SPC.

**Interpretation (measured + inferred):** "the one-axis fix is SPC-specific" is true but the mechanism is sharper —
removing the scaffold axis is a *search aid*, not a geometry repair. The alignable rotation exists on DCI/DOCCI; the
unpaired WassersteinProcrustes (k-means geometric init + Hungarian/Sinkhorn refinement over two disjoint halves)
lands in a bad local optimum off SPC, and on SPC the axis removal happens to let the search escape it.

### Follow-ups in flight (poll + collect, then analyze)

Per the SEARCH-LIMITED branch (frozen criterion), part (2): does an unpaired procedure recover it?

- restarts gen-pc0 seeds 3–7, DCI + DOCCI, select by pairs-free S1 only (seeds 0–2 already measured in E6):
  job-8edb276681b7 (DCI 3,4,5), job-da8dfb505f89 (DCI 6,7), job-0af15fd3826f (DOCCI 3,4,5), job-01e790c31637 (DOCCI 6,7).
  PASS (search recoverable) if S1-selected restart FOSCTTM within 0.05 of oracle on both; else search not recoverable.
- genpcs (finishes the promised pc1–pc4 individual-PC ladder for gen): job-965818c000d2 (DCI pc1,pc2),
  job-7fb22ef1774e (DCI pc3,pc4), job-4f10dffd87be (DOCCI pc1,pc2), job-3b0f64c737c4 (DOCCI pc3,pc4).
- transfer2 (P6 SPC→COCO, chunked COCO reduce, raw vs drop1): job-41bbc0fa9a5a (running).

### How to continue if out of turns

1. `cd .../experiments; export MRUN_URL=http://127.0.0.1:19025` (sandbox disabled).
2. Poll: `~/domains/common/bin/common exec python -c "from mrun.client.api import Api; print(Api().json('GET','/api/jobs/<id>',timeout_s=60).get('state'))"`.
3. Collect: `~/domains/common/bin/common exec python e6_generality/submit.py --collect` (writes receipts into ../results/e6_generality/, updates jobs.json).
4. Analyze restarts: for each corpus, over seeds 0–7 (0–2 from E6 e6_sweep-*-none-pc0*, 3–7 from e6b_restarts-*),
   take argmax-S1 (S1_matched_cosine) and report its foscttm_eval_only; compare to oracle (0.0097 DCI, 0.0068 DOCCI).
5. Then edit response.md §3.6 + the frontmatter status line + the "still computing" parenthetical, and the README
   status row (see plan below). DO NOT touch the rest of response.md. Do not commit/push.

### Response edit plan (do after all jobs collected)

- §3.6: add the oracle paragraph (geometry is rotation-alignable; the fix is a search aid, not a geometry repair);
  keep the FOSCTTM table; fold in the pc1–pc4 ladder result and the SPC→COCO transfer; update the parenthetical.
- Frontmatter status line: note E6b measured (oracle rotation ceiling; the off-SPC failure is a search failure).
- README status row for the generality/response item.

---

(Older E6 run history is in the receipts/jobs.json; the frozen E6 PREREG is PREREG.md.)

---

## 2026-10-22 23:24 PDT — FINALIZE (E6b complete)

### Short version (plain language)

E6 found that removing one non-visual axis from Qwen3 generative-pooling text embeddings rescues Schnaus et al.'s unpaired alignment on SPC but not on DCI or DOCCI, and reported this as "the one-axis fix is SPC-specific". E6b asked WHY it fails off SPC: is the geometry un-alignable, or does the unpaired solver just fail to find the alignment? Answer (measured, decisive): the geometry is fine — given the TRUE pairs, a single rotation aligns Qwen3-gen to the image near-perfectly on all three corpora (holdout FOSCTTM 0.007–0.014, essentially the control-encoder ceiling 0.001–0.003). So the off-SPC failure is a failure of the UNPAIRED SEARCH, not of the geometry. Removing the axis is a search aid (it de-corrupts the solver's pseudo-pairing), not a geometry repair; it happens to be enough on SPC and not off it. Eight unpaired restarts selected by the pairs-free S1 do not recover it (near chance, 0.40/0.50; even the best restart, 0.28/0.34, is nowhere near the 0.007–0.010 oracle). No other single axis helps. The SPC-fit map with the axis removed transfers to held-out COCO-val (FOSCTTM 0.409 raw -> 0.022), consistent with the diagnosis (the removal rescues the fitting, done on SPC).

### Method

Oracle (decisive): train on the true pairs at arange(0, n-2000) (vision row i with language row i), holdout = last 2000, score with their retrieval_metrics (shuffle seed 0). Two maps fit on the training rows only: orthogonal Procrustes W=polar(Xc^T Yc) (the ceiling of their rotation-only family) and unconstrained ridge-linear W=(Xc^T Xc+1e-3 I)^-1 Xc^T Yc. pc0 removal mirrors E6's Deflated (project principal_axes(train_y,1) out of raw train_y and val_y before centering). Worker `e6b_oracle.py`, in-process synthetic smoke (recovers a known rotation FOSCTTM 0.0; polar semi-orthogonality err 2e-13). Restarts (part 2, search-limited branch): their WassersteinProcrustes defaults on gen-pc0 over seeds 0–7, select by pairs-free S1 only (`e6b_restarts.py`; seeds 0–2 reused from E6). Individual-PC ladder (fulfils the response's promised pc1–pc4 ladder): E6 `sweep.py` candidates pc1–pc4, gen, DCI+DOCCI, seed 0. P6 transfer: `e6b_transfer.py`, fit on SPC gen (two disjoint unpaired halves), eval on 5000 COCO-val rows loaded with a chunked reduce_texts (RAM-safe; chunk-vs-loadrows max dev 0.0). All CPU on Beast via mrun, 4 threads, right-sized RAM.

### Results

Oracle holdout FOSCTTM (true pairs); receipt `results/e6_generality/e6b_oracle-20261022T223221.json` (job-1aca147d43d7):

| cell | map | SPC | DCI | DOCCI |
|---|---|---|---|---|
| gen, no gate | orthogonal | 0.0092 | 0.0144 | 0.0104 |
| gen, pc0 removed | orthogonal | 0.0071 | 0.0097 | 0.0068 |
| gen, pc0 removed | linear (ridge) | 0.0100 | 0.0181 | 0.0102 |
| gen, no gate | linear (ridge) | 0.0190 | 0.0471 | 0.0292 |
| Qwen3-Embedding, no gate | orthogonal | 0.0021 | 0.0028 | 0.0010 |
| Qwen3-Embedding, no gate | linear (ridge) | 0.0026 | 0.0034 | 0.0009 |

Compare unpaired (E6, measured): gen none SPC 0.415 / DCI 0.479 / DOCCI 0.474; gen pc0 SPC 0.038 / DCI 0.391 / DOCCI 0.478; Qwen3-Embedding none 0.019 / 0.093 / 0.096.

Restarts, gen-pc0, holdout FOSCTTM by seed (S1 = pairs-free selector); receipts `e6b_restarts-{DCI,DOCCI}-*-seeds*.json` + E6 seeds 0–2:

- DCI (8 seeds): FOSCTTM 0.413/0.314/0.447/0.347/0.397/0.396/0.338/0.280 (seeds 0..7); argmax-S1 = seed 5 (S1 0.4948) -> 0.396; best-over-restarts 0.280. n=8.
- DOCCI (8 seeds): FOSCTTM 0.465/0.482/0.488/0.483/0.341/0.502/0.495/0.474; argmax-S1 = seed 5 (S1 0.4426) -> 0.502; best-over-restarts 0.341. n=8.

Individual-PC ladder, gen, holdout FOSCTTM (seed 0); receipts `e6_sweep-{DCI,DOCCI}-qwen3-8b-gen-{pc1-pc2,pc3-pc4}-*.json`:

- DCI: none 0.542, pc0 0.413, pc1 0.492, pc2 0.511, pc3 0.437, pc4 0.455.
- DOCCI: none 0.515, pc0 0.465, pc1 0.443, pc2 0.552, pc3 0.408, pc4 0.570.

P6 SPC->COCO transfer; receipt `e6b_transfer-SPC-to-coco_val2014-20261022T231943.json` (job-41bbc0fa9a5a): raw FOSCTTM 0.409, drop1 (SPC top PC removed) 0.022, on 5000 held-out COCO-val rows (chunked load, smoke dev 0.0).

### Verdict vs each PREREG_E6b prediction

- Canary C1 (oracle real, corpora alignable): PASS. Qwen3-Embedding oracle-orth 0.0021/0.0028/0.0010 <= 0.05 and <= its unpaired (0.019/0.093/0.096).
- Canary C2: first clause PASS (SPC gen-pc0 oracle 0.0071 <= 0.10, reproduces the SPC rescue). Second clause FALSIFIED (measured refinement): gen-none oracle on SPC (0.0092) is NOT clearly worse than gen-pc0 (0.0071) — the scaffold axis does not block the true-pair rotation even on SPC; its harm is to the unpaired search's pseudo-pairing, not to the geometry.
- Branch criterion: SEARCH-LIMITED fired (gen-pc0 oracle-orth 0.0097 DCI, 0.0068 DOCCI, both <= 0.15 and far below unpaired 0.391/0.478). Ran part (2) as registered.
- Part (2) recovery PASS criterion (S1-selected restart within 0.05 of oracle on both): FAIL = search NOT recoverable. S1-selected 0.396 (DCI) / 0.502 (DOCCI), best-over-restarts 0.280/0.341, vs oracle 0.0097/0.0068. The unpaired procedure does not recover it off SPC.
- Oracle-linear control: linear ~ orthogonal everywhere (0.010–0.018 vs 0.007–0.014), so the orthogonality constraint is not the obstacle; the shared linear structure is present and the unpaired search simply does not reach it.
- E6 kill condition (unchanged, already fired): the one-axis removal fix is SPC-specific. E6b explains the mechanism (search, not geometry); it does not revive the generality-of-the-fix claim.

### Controls / canaries

Synthetic rotation-recovery smoke in the oracle job (FOSCTTM 0.0, polar err 2e-13). Qwen3-Embedding oracle canary (C1). gen-none vs gen-pc0 oracle on SPC (C2). Chunked-reduce parity vs library load_rows (max dev 0.0). Negative control in the laptop unit test: an unrelated Y gives oracle FOSCTTM ~0.508 (chance). All MEASURED with receipt paths above.

### Deviations from PREREG_E6b

- Part (3) cumulative drop-k ladder (the GEOMETRY-limited branch) was NOT run, because the oracle fired the SEARCH-limited branch; per the frozen decision tree we ran part (2) instead. In its place we completed the individual-PC pc1–pc4 sweep that response.md §3.6 had promised ("the pc1–pc4 ladder"), using the frozen E6 sweep.py. Both the task and the response refer to this individual-PC ladder; the cumulative-k ladder was the conditional geometry-branch diagnostic and was not triggered.
- Oracle trains on all n-2000 paired rows (2x an unpaired half). This only makes the ceiling stronger; the control (Qwen3-Embedding) reaching 0.001–0.003 under the same protocol, and the data count being >> 768 dims either way, mean the near-zero oracle is driven by the true correspondence, not the row count (ASSERTED; a half-data oracle control was judged unnecessary and not run).
- transfer2 RAM reservation was clamped by mrun history to 11776 MB (declared 24000); the chunked load kept actual peak well under that and the job succeeded.

### Caveats

- S1 is a weak selector off SPC (on DOCCI it anti-selects: argmax-S1 picked the worst restart). The restart conclusion rests on the full spread and the best-over-restarts, both far from the oracle, not on the S1 pick alone.
- "Search-limited" is specific to their solver (k-means geometric init + Hungarian/Sinkhorn refinement, defaults). A different unpaired matcher might do better; we tested their procedure with 8 restarts, not all possible unpaired methods.
- Receipts live under `experiments/results/e6_generality/` (note: that is `experiments/results/`, not `unpaired-rosetta/results/`). jobs.json lists every job and state.

### Next step

Optional: a half-data oracle control to close the "true pairs vs more data" caveat airtight; and, if pursued, testing whether seeding their unpaired solver from a better initialization (e.g. a few known pairs, or the SPC-learned rotation) recovers DCI/DOCCI — that would turn "search-limited" into an actionable fix suggestion for the authors.

### Response edits applied (no commit/push)

response.md: frontmatter status line; §3.6 result paragraph replaced + oracle table + restart/ladder/transfer paragraphs + updated parenthetical; §3.6 "what this means" oracle sentence; §10 limits bullet (corrected the now-false "more wrong with it than this one axis" clause and the "still computing" parenthetical). README.md: the response.md status row. Nothing else in response.md touched. Backups of the pre-edit files are in the session scratchpad.
