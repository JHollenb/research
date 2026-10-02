#!/usr/bin/env python3
"""Reproducible generator for paper Figure 5 (fig5_variance_decomposition.png).

Three panels, one matplotlib process, no GPU:
  F2A  read-site variance split            (F2_F3_qwen_predictive_readmap.json)
  F2B  store necessity                     (F2_scaffold_poc_store_necessity.json)
  F2C  write-formation falsifier           (phase2_sitemap_analysis.json,
                                            confirm_fal3_analysis.json,
                                            Phase-2 argmax SD from FINDINGS-addendum recompute)

F2C plots, per cell, the frozen argmax locator (S1) and the commit locator (S2) for the
Phase-2 maps AND the preregistered fresh-color retest, with the four-layer threshold. The
retest's fresh-color cells clear every locator; the frozen argmax still trips on the Gemma
identity plateau (4.06, commit SD 0.00), as preregistered.

Run: python3 figures/make_fig5.py   (writes fig5_variance_decomposition.png beside this file)
"""
import os, json
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

SVD = os.path.expanduser("~/domains/saturn/experiments/2026-10-02-site-variance-decomposition/results")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fig5_variance_decomposition.png")

def L(name): return json.load(open(os.path.join(SVD, name)))

read = L("F2_F3_qwen_predictive_readmap.json")["variance_fraction"]
store = L("F2_scaffold_poc_store_necessity.json")
phase2 = L("phase2_sitemap_analysis.json")["models"]
confirm = L("confirm_fal3_analysis.json")["models"]

fig, axes = plt.subplots(1, 3, figsize=(17, 5.6))

# ---- F2A: read-site variance split ----
ax = axes[0]
keys = ['coord_main (SCAFFOLD localization)', 'coord*op (op-specific weighting)',
        'coord*binding (which-fact-queried weighting)', 'coord*lex (FACT weighting)',
        'coord*template (template weighting)', 'coord*order (order weighting)']
short = ['coord\n(scaffold)', 'coord x op', 'coord x\nbinding', 'coord x\nfact', 'coord x\ntemplate', 'coord x\norder']
vals = [read[k] for k in keys]
bars = ax.bar(short, vals, color=['#1e3a8a', '#2563eb', '#93c5fd', '#f59e0b', '#fbbf24', '#fde68a'])
ax.set_ylabel("fraction of profile variance")
ax.set_title("F2A  READ-site map (Qwen2.5-1.5B)\n24-coord x op x fact x template x order x binding")
for b, v in zip(bars, vals):
    ax.text(b.get_x() + b.get_width() / 2, v + .005, f"{v*100:.1f}%", ha='center', fontsize=8)
ax.set_ylim(0, .5); ax.tick_params(axis='x', labelsize=8)

# ---- F2B: store necessity ----
ax = axes[1]
sv = store['store_necessity_abs']['variance_fraction']
keys = ['op', 'scene_FACT', 'order_TEMPLATE', 'binding', 'op*scene', 'residual_higherorder']
short = ['op', 'fact\n(scene)', 'template\n(order)', 'binding', 'op x\nfact', 'resid']
vals = [sv[k] for k in keys]
bars = ax.bar(short, vals, color=['#1e3a8a', '#f59e0b', '#fbbf24', '#93c5fd', '#60a5fa', '#d1d5db'])
ax.set_ylabel("fraction of effect variance")
ax.set_title("F2B  STORE necessity at fixed band (Qwen2.5-1.5B)\neffect magnitude x op x fact x template x binding")
for b, v in zip(bars, vals):
    ax.text(b.get_x() + b.get_width() / 2, v + .008, f"{v*100:.1f}%", ha='center', fontsize=8)
ax.set_ylim(0, .95); ax.tick_params(axis='x', labelsize=8)

# ---- F2C: falsifier, frozen argmax (S1) vs commit (S2), Phase-2 AND confirm ----
ax = axes[2]
# Phase-2 per-cell S1 (frozen argmax SD) from FINDINGS-addendum recompute (audit-verified:
# Qwen color 5.45, Gemma identity 4.01 MATCH); S2 (commit SD) from phase2 JSON.
p2_s1 = {('qwen15', 'identity'): 3.81, ('qwen15', 'color'): 5.45, ('qwen15', 'shape'): 1.86,
         ('gemma2', 'identity'): 4.01, ('gemma2', 'color'): 3.05, ('gemma2', 'shape'): 2.45}
def p2_s2(m, op):
    return phase2[m]['band_location_primary_write_commit'][op]['write_commit_sd']

disp = {'qwen15': 'Qwen', 'gemma2': 'Gemma'}
cells = []  # (label, s1, s2)
for m, op in [('qwen15', 'identity'), ('qwen15', 'color'), ('qwen15', 'shape'),
              ('gemma2', 'identity'), ('gemma2', 'color'), ('gemma2', 'shape')]:
    cells.append((f"{disp[m]}\n{op}", p2_s1[(m, op)], p2_s2(m, op)))
clabel = {'colorC': 'color*', 'identity': 'id (canary)'}
for m, op in [('qwen15', 'colorC'), ('qwen15', 'identity'), ('gemma2', 'colorC'), ('gemma2', 'identity')]:
    d = confirm[m]['cells'][op]['write_signal_admitted']
    cells.append((f"{disp[m]}\n{clabel[op]}", d['S1_argmax_write_sd'], d['S2_write_commit_sd']))

x = np.arange(len(cells)); w = 0.4
s1 = [c[1] for c in cells]; s2 = [c[2] for c in cells]
ax.bar(x - w/2, s1, w, color='#f59e0b', hatch='//', edgecolor='white', label='S1 frozen argmax locator')
ax.bar(x + w/2, s2, w, color='#1e3a8a', label='S2 commit locator')
ax.axhline(4, ls='--', color='red', alpha=.7, lw=1.3)
ax.text(4.8, 4.12, "falsifier threshold (4 layers)", color='red', fontsize=7.5, ha='right', va='bottom')
ax.axvline(5.5, color='#9ca3af', ls=':', lw=1)
ax.text(2.5, 6.6, "Phase 2 (prior maps)", ha='center', fontsize=8, color='#374151')
ax.text(7.5, 6.6, "confirmatory (fresh colors)", ha='center', fontsize=8, color='#374151')
for i, v in enumerate(s1):
    ax.text(x[i] - w/2, v + .07, f"{v:.2f}", ha='center', fontsize=6.5, color='#92400e')
    if v >= 4:
        ax.text(x[i] - w/2, v + .5, "fired", ha='center', fontsize=6.5, color='red', fontweight='bold')
for i, v in enumerate(s2):
    ax.text(x[i] + w/2, v + .07, f"{v:.2f}", ha='center', fontsize=6.5, color='#1e3a8a')
ax.set_xticks(x); ax.set_xticklabels([c[0] for c in cells], fontsize=6.8)
ax.set_ylabel("SD of per-fact write layer (layers)")
ax.set_title("F2C  Write-formation falsifier: argmax (S1) vs commit (S2)\n"
             "frozen argmax fired 2/6 in Phase 2; confirm color cells clear all\n"
             "locators; argmax still trips on the identity plateau", fontsize=7.8)
ax.set_ylim(0, 7)
ax.legend(handles=[Patch(facecolor='#f59e0b', hatch='//', label='S1 frozen argmax locator'),
                   Patch(facecolor='#1e3a8a', label='S2 commit locator')],
          fontsize=7, loc='upper right', bbox_to_anchor=(1.0, 0.78))

plt.tight_layout()
plt.savefig(OUT, dpi=130)
print("wrote", OUT)
