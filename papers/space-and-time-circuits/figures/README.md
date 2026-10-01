# Figures

All figures are built by `make_figures.py` from collected reports. It needs only numpy and matplotlib and runs no model code:

```
python research/papers/space-and-time-circuits/figures/make_figures.py
```

| figure | paper | what it shows | source receipts |
|---|---|---|---|
| `fig1-timeline.png` | §4 | How circuit formation and control were mapped, Aug 5 – Oct 1, 2026. Four lanes: diffusion, language models, instruments, retractions. | One dated record per event, listed in `EVENTS` in the script; the script fails if any source file is missing |
| `fig2-quadrants.png` | §§6.1, 6.4 | Best singleton necessity against best singleton write for ten selected original transformer cells, three Mamba identity cells and two Falcon attention cells. The shaded region marks the declared singleton bars of 0.25 necessity and 0.2 write; whole-path and validity checks are separate. Falcon has weaker write ports. Its SSM cuts are omitted because weak signed denominators destabilize necessity shares. | Transformers: `saturn/experiments/2026-09-30-full-layer-sweeps/results/{canary-70c9aa8890ca, qwen05-bfcd72596050, qwen15-11f9ce05b1fd, pythia4000-8ce7a03b7f57, pythia16000-177cfa16ed4a, gemma2-ed4ce1ac5974}` (`kv1_iso`, `kv_iso_suff_single`). Mamba: `saturn/experiments/2026-09-30-mamba-full-layer-sweeps/results/{sweep130-c909150c9b9f, sweep370-b04f471035d8, sweep28b-3114654c6ec1}` (`max_single_necessity.share`, `max_single_write.s_norm`). Falcon: [bundled E14 report](../evidence/hybrid-attn-ssm/report.json) (`necessity.attn`, `write.attn`) |
| `fig3-layer-profiles.png` | §6.1b | Per-layer isolated necessity, residual write (E16) and isolated K/V or state write (E17), by relative depth. Panels: SmolLM2, Qwen2.5-1.5B and Gemma-2 identity; Mamba-130M, 370M and 2.8B identity. Mamba necessity is Δlogprob divided by the whole-path Δlogprob. | Same reports as fig2 (`resid_suff_single`; `resid_write_per_layer`, `necessity_per_layer`, `necessity_all_delta`, `write_per_layer`) |
| `fig4-window-necessity.png` | §6.1b | E19: necessity of every contiguous window (width × start) for Qwen2.5-1.5B and Gemma-2-2B identity, and E19b: Gemma sliding vs global layer sets. Error bars are 95% bootstrap CIs. | `…/full-layer-sweeps/results/e19-qwen15-57ad67c21bd1`, `e19-gemma2-2f9593a800cd`, `e19b-gemma2-14e48b6093e8` |
| `fig5-cut-size.png` | §6.1b | Fraction of whole-path necessity carried by the best tested cut of size k, at each declared grain. The Pythia-70M induction control has a head carrying 0.58. In the necessity-clean language-model cells, the best single layer carries ≤ 0.18. The smallest tested qualifying windows span six or eight layers, except Gemma identity, which remains below 0.8 at eight; widths five and seven were not swept. | Pythia: `…/2026-09-30-e4-pythia-recovered-loss/results/e4-19e98d8ac631` and `e4-b69d8fc7654a` (band scope, mean ablation, `N_ko`). FLUX: `…/2026-09-30-e7-flux-color-multiseed/results/full-report.json` (`canary_e1b_route`, source interchange). Language models: the E19 reports |
| `fig6-skeleton-overlays.png` | §8 | Schematic of the static skeleton (route blocks × denoising steps) with dynamic circuits as overlays. It is a diagram; its numbers are quoted from §8 and their receipts are cited there. | §8 |

## Notes

- **FLUX in fig5.** The FLUX point uses the dp axis: (1 − dp_step) / (1 − dp_all), median over five seeds. The best single step, the last one in every seed, moves the image 0.37–0.46 of the way toward the source, yet the image stays nearest the *target* on every step and every seed. The all-step swap reaches the source (dp −0.85 to −0.94). With only four steps, a single step carries more of the dp distance than one layer of a 24–28-layer trace does.
- **Why not `job-ec1ab31d35f2`.** That space-circuit certificate (Qwen source routing) tests only the full parent edge set and has no single-site arm. The space control in fig5 is therefore the Pythia-70M head panel (E4), which measured single heads, pairs, the minimal triple and the five-head set.
