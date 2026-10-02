# Round 1 review — prior-art positioning + clarity (frontier-lab reader lens)

Read title/abstract/intro/captions in full; skimmed body for jargon/structure/figures; opened all 6 PNGs. All IDs WebSearch-verified.

## 1. 3-minute reader
Repeatable thesis: *circuits built over execution order — source seeds state, model forms it, commits a store, consumer reads it — so the formed store localizes differently from source and read, and single-site/attribution tools land on one end and miss the store.* The **block-and-rescue dissociation** (block kills the effect; transplant into a fresh recipient restores it) is the sticky image. Good.

**Name risk: "time-formed" is confusing.** In transformer-land "time" = token position; here the axis is depth/denoising/recurrence, which the intro disambiguates three times. Prefer **"formed-store," "staged," or "construction" circuit** — foregrounds source→formation→commit→store→consumer, kills the token-time reading. If keeping it, disambiguate in sentence one.

## 2. Prior-art map (closest + delta; IDs verified)
- **Formation/commit/read** → Geva 2023, Agarwal 2609.17537 (deferred commitment). Delta: isolated store cut + transplant. Agarwal cite accurate, well positioned.
- **Isolated vs in-forward cut** → add a patching-methods cite (Zhang & Nanda 2309.16042, **missing**). 0.985→0.009 leak is strong.
- **E20 transplant** → Geiger 2023 (cited); transplant-into-fresh-recipient is the genuine novelty.
- **Read join / §7.2 control** → **Wang 2022 IOI (2211.00593, NOT cited)** — canonical distributed-but-locatable attention circuit; conspicuous absence.
- **Attribution-graph blind spot (§5)** → Ameisen 2025, Hanna 2025, Lieberum 2024 (cited). **Missing: Marks 2024 Sparse Feature Circuits; Dunefsky 2406.11944 (transcoder origin); Lindsey 2025 "Biology of an LLM"** (task-flagged). §5 tests transcoders without citing their origin or the SAE-circuit baseline.
- **FLUX path-distributed** → Mazur DifFRACT 2606.15796, Görgün 2512.08486 (cited). **Missing: Basu 2023 (2310.13730) + "Localizing Knowledge in Diffusion Transformers" (2505.18832)** — Basu's "diffusion knowledge is distributed, unlike LLMs" anticipates your LM-vs-diffusion split; demand-level.
- **Mamba write port (§7)** → **Sharma 2024 (2404.03646, NOT cited)** + "Mamba-2 State Sink" (2606.00930). **Biggest gap: an entire Mamba section cites zero prior Mamba interp.**

**Most damaging: Chughtai, Cooney & Nanda 2024 "Summing Up the Facts" (2402.07321, NOT cited).** Your load-bearing claim that `y=(x1+…+xn)/n` passes all four conditions IS their additive-motif / constructive-interference result; omitting it reads as unawareness to this audience. Defensive add: "Factual Retrieval… Redundant, Distributed, Non-Contiguous" (2606.21345). **Positive:** every 2026 ID you cite (Agarwal, Cheng&Zhang 2605.04061, Bugaud, Mazur, Görgün) verified real — no fabricated IDs.

## 3. Titles + abstract
(a) *"The Formed Store: Circuits Built Over Execution Order Hide From Single-Site and Attribution Tools."* (b) *"Block and Rescue: A Formation–Commit–Read Anatomy of Transformer and Diffusion Circuits."*

Abstract (lead with the number, not the taxonomy): "Activation patching and attribution graphs disagree about where a circuit lives. We show why: some circuits are built over execution order. A source seeds internal state, the model forms it over an interval, commits it to a store with independent causal authority, and a later consumer reads it — and these three localize to different places. Our central result is a block-and-rescue dissociation: in Qwen2.5-1.5B, Gemma-2-2B, and SmolLM2-1.7B, blocking the late recipient-formed key/value band removes 73–92% of a seed's effect, while transplanting that same band into a separate unseeded recipient restores 71–99% and authors the correct answer — the store carries specific content, not generic perturbation, and it reproduces on held-out identities. The tools built to find circuits miss this store: on Gemma-2-2B a published attribution-graph feature basis moves the answer ≤0.08 while a native cut flips 83%. A FLUX.2 diffusion transformer gives a strictly path-distributed instance no language-model cell matches — though a weighted additive mechanism also passes, so the signature names a support profile, not a mechanism. Construction history is part of causal anatomy."

## 4. Structure
~8,200 words + 6 figs + 4 tables ≈ 14–16pp double-column — at/over budget. **Skip-risk:** §8 (computed intermediate) and the Falcon-H1 "not established" row — demote §8 to a para + appendix, footnote the hybrid. **Promote §5** (tool miss, most frontier-relevant, buried past p.8). Move §2.3's four-condition algebra to §6 where it's used.

## 5. Jargon used before defined
- **"admitted rows"** — pervasive; admission criterion never stated. Define it.
- **"seed gain"** — abstract/Fig1/§3.3; formula only in Appendix B. One inline line at first use.
- **"authors"** (verb), **"filler state," "carrier," "commit band"** — undefined on first use. "space circuit" fine.

## 6. Figures (all opened)
Carry it: **Fig 1** (dissociation hero), **Fig 5** (feature-basis vs native cut — §5 punchline), **Fig 4** (FLUX quadrants w/ criterion lines). Fig 2's third panel reads as a separate chart — label as inset. Fig 6 defensive. **Fig 3 is never referenced in the body** — orphaned, small fonts; cite or cut. **Biggest gap: no schematic of source→formation→commit→store→consumer** — the core concept has no diagram (README wants one). Add as Fig 1a.

## 7. Five ranked changes
1. **Cite additive-motif + Mamba lineage** (Chughtai 2402.07321; Sharma 2404.03646) — credibility-level omissions for this audience.
2. **Rename / hard-disambiguate "time-formed"** in sentence one.
3. **Add the pipeline schematic; reference or cut Fig 3.**
4. **Lead abstract/intro with block-and-rescue + 83%-vs-0.08 tool miss**, not the taxonomy; promote §5.
5. **Define "admitted rows"/"seed gain" inline**; add Wang-IOI, Marks, Basu, Dunefsky, Lindsey-Biology cites.
