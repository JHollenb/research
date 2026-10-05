# Figures — Time-Formed Circuits

Each figure below lists the data file it is (or should be) generated from. Paths are relative to `~/domains/`. The three figures the submission review calls out as the ones the paper most needs are marked **[review]**; they map to Fig 2, Fig 4, and Fig 5.

## Main body

| File | Figure | Data file(s) |
|---|---|---|
| `fig1-schematic.png` | Fig 1. The operational object (seed → formation → commit → store → readout, with block and transplant). | Hand-drawn schematic; no data file. |
| `fig2-dissociation.png` | **[review]** Fig 2. Cross-family dissociation bars: per-row **seed = 1**, **block** removed, **rescue** recovered, **wrong-identity (wrong-band)** retained, with identity-clustered 95% intervals. | `saturn/experiments/2026-10-02-p1-reviewer-experiments/results/B_clustered_stats.json` (intervals); point estimates from `saturn/experiments/2026-10-02-e20-cross-family/results/analysis.json`. |
| `fig3-formation.png` | Fig 3. Where the transplantable store lives (Qwen2.5-1.5B and Gemma-2-2B): late band vs seed-layer, earlier band, and a linear prediction of the band from the seed. | `saturn/experiments/2026-10-02-p1-reviewer-experiments/results/A_analysis.json`. |
| `fig4-error-interchange.png` | **[review]** Fig 4. E6 side-by-side: feature-only, matched feature-and-error, and error-only operators **against the native key/value cut** (whole-path solid, second-half dashed), identity vs color. | `saturn/experiments/2026-10-02-p1-reviewer-experiments/results/C_analysis.json`; native-cut reference from `saturn/experiments/2026-09-30-circuit-tracer-head-to-head/` (`job-ed4ce1ac5974`). |
| `fig5-flux-quadrants.png` | **[review]** Fig 5. FLUX four-quadrant 2×2 (single-call vs all-call, necessity vs sufficiency) with the four measured bounds, plus the five-seed color necessity strip. | 2×2 bounds from `saturn/experiments/2026-09-30-flux2-joint01-time-accumulation/FINDINGS.md` (0.5620 / 0.20743 / 0.91309 / 0.01101); 5-seed strip from `saturn/experiments/2026-09-30-e7-flux-color-multiseed/`. |

## Appendix D (supplementary)

| File | Figure | Data file(s) |
|---|---|---|
| `figS1-window-necessity.png` | Fig S1. Window necessity across the formation band (seven decoder cells). | `saturn/experiments/2026-09-30-full-layer-sweeps/FINDINGS-E19-window-necessity.md`. |
| `figS2-mamba-clock-retest.png` | Fig S2. Aligned retention retest at the Mamba writer (release vs write lever). | `saturn/experiments/2026-10-02-mamba-clock-retest/results/`. |

`figS2-mamba-clock-dose.png` is the superseded clock-dose figure and is not referenced by the paper.
