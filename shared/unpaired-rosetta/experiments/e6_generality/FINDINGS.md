# FINDINGS — E6/E6b (X01) generality of the non-visual axis, and why the one-axis fix fails off SPC

Written 2026-10-23 00:30 PDT by the coordinator. The full write-up for the authors is `../../response.md` §3.6; this file is the experiment-level record. Pre-registrations: `PREREG.md` (E6, sha ac2259bd…, written 19:18 PDT before any DCI/DOCCI/COCO number) and `PREREG_E6b.md` (written 22:26 PDT before any oracle or restart number). All numbers MEASURED on Beast via mrun (CPU), receipts in `../results/e6_generality/`.

## Results

**E6, generality.**
- **The axis reproduces on long-caption corpora.** On DCI and DOCCI the Qwen3-8B generative-pooling top axis is dominant and non-visual: variance 19.4% / 22.2%, held-out image R² 0.052 / 0.052, against 0.77-0.87 for the control encoders.
- **It is absent on short captions.** On COCO-val the top axis is visual (R² 0.899), so this is a long-caption effect.
- **The pairs-free S1 detector still picks removing it**, though by thin margins (0.001-0.006).
- **Removing it rescues alignment on SPC only:**

  | corpus | FOSCTTM, axis kept → removed |
  |---|---|
  | SPC | 0.415 → 0.038 |
  | DCI | 0.479 → 0.391 |
  | DOCCI | 0.474 → 0.478 |

  Qwen3-Embedding reaches 0.093 / 0.096 on the same corpora.
- **Kill condition fired for the fix.**

**E6b, diagnosis.**
- **Oracle.** Given the true pairs, the best rotation aligns Qwen3-gen on all three corpora:

  | Qwen3-gen | SPC | DCI | DOCCI |
  |---|---|---|---|
  | axis kept | 0.009 | 0.014 | 0.010 |
  | axis removed | 0.007 | 0.010 | 0.007 |

  For comparison, Qwen3-Embedding reaches 0.001-0.003. An unconstrained linear map does no better (0.010-0.018).
- **Restarts.** Eight unpaired restarts chosen by S1 stay near chance (0.396 / 0.502; best of eight 0.280 / 0.341).
- **Other axes.** Gating off PC1-4 individually leaves gen near chance.
- **Transfer.** The SPC-fit map with the axis removed transfers to held-out COCO-val: 0.409 → 0.022 (job-41bbc0fa9a5a).
- **Verdict: search-limited.** The encoder's geometry is rotation-alignable; the unpaired search fails, and the axis is what misleads it.

## Deviations

- E6:
  - The full PC1-4 FOSCTTM ladder was descoped to none / PC0 at 3 seeds under contention; the ladder was completed in E6b.
  - There were three pre-data smoke-gate fixes in sweep.py.
  - COCO RAM reservations were raised after OOM diagnosis.
  - MPNet is itself poorly aligned on DCI (0.400), so it is not a clean control there.
- E6b:
  - The geometry-limited branch (cumulative drop-k) was not run because the frozen decision tree selected the search branch.
  - The oracle trains on all n − 2000 true pairs, which only strengthens the ceiling. A half-data oracle control was not run; that it is unnecessary is ASSERTED.
