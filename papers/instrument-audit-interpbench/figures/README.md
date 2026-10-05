---
title: Figures — Instrument audit vs InterpBench
type: research-documentation
status: draft
updated: 2026-10-05
---

# Figures

Both figures are generated from the frozen per-model result file
`saturn/experiments/2026-10-05-interpbench-method-audit/results/full.json` — a list of 84
per-model records, each with a `node_auroc` dict keyed by method name
(`act_patch`, `eap`, `eap_ig`, `gradxact`, `gradxact_mag`, `writesite`, `writesite_raw`,
`subspace`, `subspace_rand`, `subspace_rank1`, `random`), plus `case`, `categorical`,
`n_nodes`, and `n_gt_pos`. No new computation is needed; both figures read AUROC values
directly from that file.

## Figure 1 — Per-method node-AUROC distribution across 84 models

A strip/jitter plot (one column per method, one dot per model, 84 dots per column), methods
ordered by mean AUROC descending, with the mean marked and the random-null band
(≈0.486–0.517) drawn as a shaded reference. Shows the full per-model spread behind the
headline means: the baselines (activation patching, EAP-IG, EAP) sit high and tight; the
gradient×activation centered-std form and the baseline-relative write-site form overlap or
fall below the null band; the subspace trace and its matched-rank random control sit close
together, visually making the "degraded activation patch, not a concept localizer" point.

- Data: `results/full.json`, field `node_auroc[<method>]` over all 84 records.
- Methods to plot: all 11 keys above (baselines bolded; the two instrument controls —
  `subspace_rand`, `subspace_rank1` — shown adjacent to `subspace`).

## Figure 2 — Per-model scatter: activation patching vs gradient×activation (centered-std)

A scatter of the 84 models, x = `node_auroc['act_patch']`, y = `node_auroc['gradxact']`, with
the identity line `y = x` drawn. Points mostly fall far below the diagonal (gold near 1.0,
gradient×activation well under it), making the 30-point gap (P1) a per-model picture rather
than a single mean. Mark categorical vs regression points differently (field `categorical`),
and optionally overlay `node_auroc['gradxact_mag']` in a second series to show the magnitude
form closing most of the gap.

- Data: `results/full.json`, fields `node_auroc['act_patch']`, `node_auroc['gradxact']`
  (and optionally `node_auroc['gradxact_mag']`), split by `categorical`.
