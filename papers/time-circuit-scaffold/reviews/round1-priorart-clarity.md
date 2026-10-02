# Round 1 review — prior-art positioning, clarity, split with Paper 1

Reviewer lens: novelty/prior-art + busy-frontier-reader clarity + the Paper 1 split. Read-only; this is the one output.

## 1. The 3-minute read / thesis / names

What a reader remembers: *the commit layer doesn't move* (SD 0.00 across 42 Gemma facts), *identical bytes have query-dependent authority* (3.130 nats), the 42.2/29.0/1.1 variance split, and "attribution tools see the space circuit and miss the scaffold." That is a strong, memorable set — the abstract leads well.

The one-sentence thesis is sound but never lands **verbatim in one place**; it's distributed across abstract/intro, and the closing line drops the "space circuit per input" half. Put the full triple in one sentence, early (end of ¶1 §1) and again as the last line.

"Scaffold" is a good, sticky name — but it **collides**: Paper 1 §8 uses "teacher-forced scaffolds," and "scaffold/scaffolding" already means prompt/CoT structure in the field. "Space circuit" is the weak name: a frontier reader reads "space" as spatial/geometric, and its meaning is outsourced to the companion taxonomy. Gloss it in-line ("space circuit = locally-decisive, per-position operation") the first time, or rename.

## 2. Prior-art map (verified; deltas)

Closest-work gaps, all **uncited in §10** and all real:

- **Lad, Gurnee, Tegmark 2024, "Stages of Inference?"** (arXiv:2406.19384). *Four universal stages at fixed relative depths across 8 models* — this is the nearest competitor to your "fixed scaffold = fixed stages at a recurring fractional depth." Must cite and delta: they infer stages from layer delete/swap robustness and logit alignment; you give **per-fact causal input-invariance** of the commit (SD 0.00) and a variance decomposition. Without this cite the scaffold claim looks unaware of its predecessor.
- **Chughtai, Cooney, Nanda 2024, "Summing Up the Facts"** (arXiv:2402.07321). Factual recall is an **additive motif** of independent mechanisms. Your honest null (§9) literally "ties a plain additive baseline" — you must cite the paper that argued recall *is* additive, or §9 reads naive.
- **Sharma, Atkinson, Bau 2024, "Locating and Editing Factual Associations in Mamba"** (arXiv:2404.03646). Causal tracing + ROME in Mamba; mid-/late-layer causal components. Directly precedes your §3/§7 Mamba commit-depth claims. Uncited — the biggest gap for the Mamba section.
- **Basu et al. 2023, diffusion knowledge localization** (arXiv:2310.13730, ICLR'24). Causal mediation in diffusion; knowledge distributed across UNet + one causal text-encoder state. Precedes §7's "static bus." Cite.
- **Nanda et al. 2023, "Fact Finding"** (DeepMind, LessWrong/AF): three-stage recall (concat → lookup → multi-token embedding). Two-stage-recall predecessor; cite alongside Geva/Meng.
- **Belrose et al. 2023, Tuned Lens** (arXiv:2303.08112) + logit lens: iterative/by-layer inference. Light cite for "formation over ordered execution."
- **Gurnee et al. 2024, Universal Neurons** (arXiv:2401.12181, TMLR): universality across seeds — relevant to whether the scaffold is within-model vs universal (your §9 null).

Already-cited and fine: Meng, Geva, Hase, Todd, Hendel, Feng&Steinhardt, Conmy, Ameisen/Lindsey, Geiger, Hertz(P2P), McGrath, Gu&Dao, Biderman. Note: **2026 IDs (Agarwal 2609.17537, Kamath, Mazur 2606.15796, Görgün) I could not verify — mark unverified.**

## 3. Split with Paper 1 (overlaps → ownership)

Genuine duplication (reads as one paper twice):
- **Window-necessity numbers are identical** — "best single 0.08, three adj 0.23, band L22–27 0.96" appear in P1 Table 1 *and* P2 §3.
- **Mamba writer clock-dose + Fig: same job IDs** (job-baf14…, cbb0a…/cbb0a8…, e55f…) appear in **both** appendices; P1 §7.1/Fig 6 and P2 §3/§7 make the same "write is the lever, clock a correlate" claim.
- **Gemma sliding-window commit** (L16/18/20/22 positive, global negative) in P1 Table 4 and P2 §3.
- Formation window closing at commit; attribution-graph blindness; source→store mediation — P2 handles the last two correctly (explicit "cite to companion"), but **restates §3's sweeps as if new.**

Keep: **P1** owns formation window, distributed-band necessity, write port, clock-dose, attribution-graph head-to-head, block/rescue mediation, strict path-distributed diffusion signature. **P2** owns per-fact input-invariance, variance decomposition, same-parent query authority, reader re-weight-not-rebuild, frozen-profile prediction + weight-permutation, honest null. **Fix:** compress §3 ~40% to *cite P1* for the sweeps and keep only the per-fact SD result (genuinely yours).

Cross-ref defects: P2 links companion; **P1 never links back by path** (just "a companion line of work") — make symmetric. README evidence-map line 68 points at a **stale path** `scaffolds-and-dynamic-circuits/architectural-paper.md:433` — fix.

## 4. Titles + abstract

- Alt A: "The Commit Layer Doesn't Move: A Fixed Time Scaffold Hosts Per-Input Circuits"
- Alt B: "Where the Answer Commits Is Fixed; What Commits Is Chosen"

Abstract (≤200 w): *In a trained model the layer where a factual answer commits does not move with the input. Across 42 facts the commit lands at Gemma-2-2B layer 22 with standard deviation exactly zero (Qwen2.5-1.5B layer 23, SD 1.16). We call this fixed schedule — seed, formation, commit, store, consumer — the time scaffold, and show the per-input computation is a space circuit on it. Decomposing the variance of a fixed model's causal site maps, which coordinate is read carries 42.2% and the operation's weighting 29.0%, while the fact carries 1.1%; store necessity is 84.0% operation, 3.2% fact. Byte-identical stored state acquires query-dependent authority (median 3.130 nats). A reader profile frozen before evaluation predicts held contexts in all eight; permuting the trained value-projection rows collapses it, so the scaffold lives in the weights. The same organization appears in a state-space and a diffusion model. Standard attribution tools find the space circuit and miss the scaffold where the answer commits. We report one null plainly: the cross-family common graph ties an additive baseline.*

## 5. Structure

- **§8 (formed state feeds later) is the skip/cut candidate** — competent n=1/3; fold into limitations or cite to companion.
- **§3 is overlong** and overlaps P1 (above) — biggest cut.
- §9 null: keep (buys credibility), tighten to ~½.
- §5 confound ("all three ops are surface read-back" + the `<!-- TODO addendum -->`) currently **undercuts the decisive test** — a reader hits it and discounts 42.2/29.0/1.1. Land the relational addendum or move the caveat below the result, not mid-section. Length (~6,300 w / ~11 pp) is fine once §3 shrinks.

## 6. Jargon + figures

Jargon: define **"coordinate" = (layer, kv-head, key-or-value)** before first body use (§4 uses it pre-definition). "signed causal reader profile" is dense — gloss once. "space circuit," "grain," "same-parent," "query-selective harm" are OK once §2 is read.

Carry the paper: **Fig 1** (thesis anchor), **Fig 5** (decisive variance split), **Fig 2** (SD 0.00 input-invariance). Fig 3 is the memorable lead but **its data labels overlap the bars** ("0.583" occluded) — fix. **Fig 1 caption text overlaps the commit/store boxes.** Fig 5 F2A shows no residual bar while F2B shows "resid 10.4%" — named terms sum to ~75%; show or state the read-map residual. **§7 has no figure** for a strong cross-architecture generalization — add a small Mamba/diffusion panel or table.

## 7. Five ranked changes

1. **Add + delta the missing prior art** (Lad 2024 stages, Chughtai 2024 additive, Sharma 2024 Mamba, Basu 2023 diffusion, Nanda 2023, tuned lens). Highest-leverage: without them the novelty looks overclaimed.
2. **Cut §3 overlap with Paper 1** (identical necessity numbers, shared clock-dose job IDs, Gemma sliding-window); cite P1, keep only per-fact SD. Fix stale/asymmetric cross-refs.
3. **Resolve the §5 confound / land the addendum** so the decisive test isn't self-discounted.
4. **Fix the thesis + names**: one-sentence thesis verbatim early and at close; gloss or rename "space circuit"; disambiguate "scaffold" from teacher-forced scaffolds.
5. **Figure fixes**: Fig 3 label occlusion, Fig 1 caption overlap, Fig 5 residual; add a §7 figure.
