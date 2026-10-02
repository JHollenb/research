---
title: "Round-1 review: prior-art positioning + clarity"
paper: formed-state-faithfulness/paper.md
reviewer_lens: novelty/prior-art + busy-frontier-lab-reader clarity + companion overlap
date: 2026-10-02
status: READ-ONLY review (this file is the only output)
---

# Round-1 review — novelty/prior-art + clarity

All arXiv IDs below verified via WebSearch 2026-10-02. Numeric claims are the other reviewers' remit; I spot-checked only internal consistency.

## 1. Three-minute takeaway (title/abstract/intro/captions)

What a busy reader retains: (a) a hidden KV-cache channel can set the answer even when the written step is correct (95-100%); (b) bigger models silently re-derive removed steps, so ablation under-counts. **Two headlines compete, and the paper leads with the weaker one.** The capacity result (a) is strong but *artificial* and gets walked back within two sentences by the full-transcript-recovery caveat (0.66-1.00), diluting the opening punch. The silent-repair result (b) is *natural*, the paper's own "monitor-relevant" phenomenon (§7.2), and has the cleanest number in the paper (common-subset 0.095→0.762). It should lead.

**Title accuracy after the reframe.** "...the Cache It Cannot [read]" is literally true (a monitor reads tokens, not cache) but rhetorically oversells: §4.3/§7.1 show a full-transcript monitor recovers *most* state-only edits because the model re-verbalizes the hidden value. A reader remembers "there's a channel monitors can't see," which the paper's own honest finding contradicts. Title is defensible for a *step-reading* monitor + the capacity claim, but it foregrounds the artificial result over the natural one.

**Two alternative titles:**
- A (leads with natural result): *"Silent Repair Rises with Scale: Removing a Reasoning Step Under-Measures Its Role in Larger Models."*
- B (keeps dissociation, softened): *"Two Channels of a Reasoning Step: The Token a Monitor Reads and the Cache It Does Not."*

**≤200-word abstract (leads with cleanest result):**
> Chain-of-thought monitoring assumes that reading what a model writes reveals what it used. We test this on a single arithmetic reasoning step whose value the prompt never restates (Qwen2.5, 0.5B-7B), under an exact-restore control that reproduces the base answer bit-for-bit. Our cleanest, naturally occurring result: after a step's cached state is removed, larger models silently re-derive it and still answer correctly far more often, rising with scale at matched precision. On items admitted at both sizes, silent repair goes from 0.095 (0.5B) to 0.762 (1.5B), and the regenerated text never announces the removal. Removal-based attribution therefore under-counts a step's role, increasingly with capability — a scale-dependent, step-level form of self-repair. A precision control rules out a floating-point artifact; 4-bit quantization roughly halves repair, a confound we report. Separately, an artificial edit shows the hidden cache channel has near-total capacity: overwriting only the cached state, written value held correct, flips the answer on 95-100% of items. A step-reading monitor is blind to this, though the model usually re-verbalizes the injected value, so a full-transcript monitor recovers most. Reading written reasoning steps bounds monitorability rather than measuring it. Scope: synthetic arithmetic, greedy, one seed.

## 2. Prior-art map (exact deltas; IDs verified)

**CRITICAL GAP — self-repair literature is uncited.** The paper cites *none* of McGrath 2023 (Hydra Effect, 2307.15771) or Rushing & Nanda 2024 (Explorations of Self-Repair, ICML 2024, 2402.15390), even though **companion Paper 1 cites both** in exactly the relevant sentence ("Self-repair can make a single-site ablation underestimate importance"). A frontier-lab reader's first objection will be: *is "silent repair" just self-repair at the step level?* Partly yes — it is the same family (ablate → downstream compensates → ablation under-counts). The honest, defensible delta:
- **Grain:** self-repair is measured at the *component* (head/layer) grain on logit *direct effect*; silent repair is at the *semantic reasoning-step* grain on *task answer* (re-derivation of a non-copied value). New.
- **Scale + quantization quantification** of the under-counting. New and the paper's strongest contribution.
- **Monitorability framing** (removal-based attribution under-counts, increasingly with capability). New.
Position silent repair explicitly as a *task-level, scale-dependent instance of the Hydra/self-repair family* in §5.6 and §8. Also add Bugaud 2026 ("single-layer edits easily corrupt but rarely repair," cited in Paper 1) as a contrasting datapoint.

**Implicit-reasoning / latent-multi-hop literature is uncited and directly adjacent** (the hidden-channel-capacity claim is "arithmetic intermediates computed internally"):
- *LLMs Do Not Think Step-by-step In Implicit Reasoning* (2411.15862) — probes hidden states on multi-step arithmetic; closest work to the capacity claim's domain. Must cite.
- Yang et al. 2024, *Do LLMs Latently Perform Multi-Hop Reasoning?* (ACL 2024, 2402.16837) — latent intermediate computation; scaling trend first-hop only.
- Biran et al. 2024, *Hopping Too Late* (EMNLP 2024, 2406.12775) — back-patching restores 32-66% of failed multi-hop answers; a repair-adjacent mechanism worth one sentence.

**Already cited, correctly (verified):** Lanham 2023 (2307.13702, incl. early-answering/adding-mistakes as techniques — no separate cite needed); Turpin 2023 (2305.04388); Chen 2025 (2505.05410); Korbak 2025 (2507.11473); Baker 2025 (2503.11926); Pfau 2024 (2404.15758); Paul 2024 (2402.13950); Bentham 2024 (2402.14897); Miller 2024 (2407.08734, the ablation-robustness point — good, but it is *not* a substitute for the self-repair mechanism papers).

**Optional add:** Radhakrishnan 2023, *Question Decomposition Improves Faithfulness* (2307.11768) — relevant to §7.3 recommendations; low priority.

Do not invent IDs; all above are WebSearch-confirmed.

## 3. Overlap / split with companion papers

- **Paper 1 (time-formed-circuits) §8 already reports the repair phenomenon** ("removal... wrong 3 of 30 at 1.5B... repairs correctly 25 of 30") and the swap-authorship numbers (E10). This is a *double-publication risk*. Paper 3 handles it reasonably (§8 "Our own prior work" + Appendix frame it as a confounded precedent de-confounded here) — keep that, but make the new-contribution list sharper: the scale *curve* (0.5B anchor + 7B), the fp32/NF4 controls, the token-vs-state 2×2, the free-running test, and the monitorability framing are new; the *existence* of repair is not. Recommend Paper 1's §8 be trimmed to a pointer so both papers don't claim repair (note for Paper-1 authors).
- **Paper 2 (time-circuit-scaffold):** essentially no overlap (scaffold fixity vs faithfulness). No cite needed; one optional sentence of context at most. The alias-binding corroboration (C20) is shared with Paper 2 §8 but used for different claims — fine.
- **Keep the companion cross-ref** (frontmatter + §8). It is the right split.

## 4. Structure / length / skip-risk

~8,970 words → ~13-15pp with tables/figures; **over the 9-11pp target.** Cuts:
- **§3 (token-visible channel) is the biggest skip-risk.** It uses a *different task* (code-trace) and *different models* (SmolLM2-1.7B, Qwen3-8B, 30B-MoE) that appear nowhere else. A busy reader wonders if this is the paper's point, then those models vanish. Compress to ~one paragraph (calibration: "the token channel behaves as text methods assume") + appendix. High leverage for length and focus.
- **§6 (free-running) is discounted by its own canary** (8/9, 5/9 < 0.90). Giving it a full section + full Figure 4 over-weights discounted evidence for a skeptical reader. Compress to ~half, demote Fig 4 to appendix.
- **Merge §4.4/4.5/4.6** (capacity-not-hiding / why-text-can't) — repetitive.
- The step-monitor-vs-full-transcript scope is re-litigated ~4× (abstract, intro-contrib-5, §4.3, §7.1). Necessary for honesty but tighten to 2 statements.
- **Promote** §5.3 common-subset (0.095→0.762) toward the front — it is the most defensible number and belongs in abstract + near Table 2.

## 5. Jargon / definitions

- **"formed state"** (title term) is never explicitly equated to "KV cache state built during the forward pass" for a standalone reader; §2.3 defines "hidden-state channel = the cache the step forms" but never glosses the title phrase. Add one sentence in the abstract/intro.
- **"monitor-blind"** — used in the abstract and as a Table 1 column header *before* §4.3 scopes it. Given the reframe, the bare label over-claims. Rename to **"step-monitor-blind"** or **"written-step-blind"** in abstract, Table 1, and Fig 3 legend. This is the single accuracy fix most aligned with the custody reframe.
- **"silent repair"** — defined §5.1; used earlier (abstract/contrib-4) with inline gloss. OK.
- **"token-visible," "non-copied," "on-policy," "admitted," "exact-restore"** — all defined on/near first use. Good.
- **"remount"** — NOT used in the paper (text uses "restore" consistently; "remount" survives only as a JSON key in the README evidence map). No action in paper; optional README tidy.

## 6. Figures

- **Fig 1 (schematic) is still a placeholder.** This is the one figure that makes the two-channel thesis legible in 10 seconds, and both companion papers ship a Fig 1 schematic. **Produce a static two-lane (written-token vs formed-cache) schematic now — do not wait for the VM-trace visualizer.** Highest-leverage clarity fix for the 3-minute reader.
- **Fig 2 (repair vs scale) is the paper's best figure** — carries the natural headline, two precision axes clear, annotations good. Keep, feature it.
- **Fig 3 (token vs state) under-informs:** every bar ≈1.0, so it looks flat and hides the interesting part (that blue = monitor-blind, and that most is re-verbalized). Add a third series — re-verbalization/recovery rate or the unrecoverable residual — so the figure carries the §4.3 nuance instead of only the caption.
- **Fig 4 (free-running):** exploratory/discounted; demote to appendix (caption already flags discount).

## 7. Five ranked changes

1. **Cite and distinguish the self-repair/Hydra literature** (McGrath 2023 2307.15771; Rushing & Nanda 2024 2402.15390; Bugaud 2026) in §5.6 and §8; frame silent repair as a *scale-dependent, reasoning-step-grain instance* of self-repair. #1 reviewer objection; companion Paper 1 already cites these, so the omission is conspicuous.
2. **Re-lead abstract (and framing) with the natural silent-repair result** (common-subset 0.095→0.762); demote the artificial capacity result to second, since it is immediately walked back. Consider Title A.
3. **Produce the Fig 1 two-lane schematic now**; ship no placeholder. Biggest clarity gain for a busy reader.
4. **Rename "monitor-blind" → "written-step-blind"** in abstract/Table 1/Fig 3, and **add a recovery/residual series to Fig 3** so figure and label match the custody reframe.
5. **Add implicit-arithmetic prior art** (2411.15862; Yang 2024; Biran 2024), **sharpen the Paper-1 overlap statement**, and **compress §3 + §6** to reach ~10pp and cut skip-risk.
