---
title: "Assessment notes: the final-boss circuit, IRD, and related work"
type: review-notes
date: 2026-09-30
status: working notes; under revision (a deeper dig into the final-boss circuit is in progress)
scope: shared by capabilities-as-transactions/ and integral-residual-dynamics/; see each paper's review-notes.md for paper-specific items
---

# Assessment notes: the final-boss circuit, IRD, and related work

These notes record one session's external-impact assessment so it can be referred back to. Each section is labeled. A "first pass" section reflects a reading that the author has since said underweights the final-boss circuit. A deeper dig is under way, and its result will be added as a new section rather than by editing these.

## 1. First-pass assessment (paper text only)

**Verdict.** Neither the IRD draft nor the capabilities-as-transactions draft, as written, is likely to draw frontier-lab attention.

**Reasons:**
- **Overlap with known work.** The "single site null, whole path works" phenomenon overlaps known and recent work: ROME window patching, Hydra and self-repair, *Does Localization Inform Editing?*, arXiv 2605.04061, and TrustNLP 2026.
- **Thin evidence.** Cells have n ≤ 4, readouts are single-token, and many receipts are private job IDs.
- **Nonstandard vocabulary** ("transaction", "terminal consumer role", "custody").
- **An unfilled §7 placeholder** in the capabilities draft.

**Distinctive items identified:**
- The cut result: the certificate exists at the K/V cut and vanishes at the residual cut in the same model.
- In-forward vs isolated K/V swap (0.99 vs 0.00).
- The method discipline: exact no-op gate, consumer-judged verdicts, retractions kept on the record.

## 2. Lineage dig (same day; author-flagged tool results excluded)

**Lowered:**
- **C7 chain-of-thought externalization.** There is one prompt pair per family, and the swapped token is the answer the scratchpad already states. The result shows copying of a stated answer, not causal use of intermediate steps.
- **Joint K/V row-permutation invariance is an attention identity**, softmax(Q(PK)ᵀ)PV = softmax(QKᵀ)V, and should not be presented as a finding or as a leak.
- **The 7B task-state K/V chain needs citations.** It needs to cite in-context task vectors (Hendel et al., 2023) and function vectors (Todd et al., 2024).
- **The donor-free writer's 5/6 needs its baseline.** It should be reported alongside the 2026-08-26 mean-tape baseline (6/6); the surviving claim is that factorization buys address specificity, not computation.
- **Stale number.** The symbol table's "35/54 read" was restated as 21/36 after template collapse, but the capabilities draft §5 still cites 35/54.

**Raised:**
- **Program-level evidence discipline:** falsifiers fired and stayed recorded, the 8B floor confound and bf16 artifact were caught and fixed with a preregistered fp32 dual-backend rerun, the "0.2218 / 0.0013" folklore was caught, and the Instrument Trial was blind-graded.
- **The infrastructure:** Saturn's exact capture, fork and replay, plus consumer-closed certification. The 2026-08-26 three-walls review rated this the highest-ceiling contribution.

**Excluded.** Findings from the 2026-09-30 blind-certification run (`saturn/experiments/2026-09-30-blind-final-boss-certification/`) are withdrawn: the author flagged that run's tooling as unreliable.

## 3. Symbol-table and image-editing dig (subagent, Opus 4.8, read-only)

**Ranked strongest results:**
1. **The FLUX.2 certified distributed route** (`research/bfl/docs/certified-semantic-circuits/paper.md`). It has 9 frozen gates, held-out seeds and a held-out-prompt confirmation, exact no-op, a foreign-encoder swap, promptless rediscovery, and a public Pythia-70M CPU verifier. MEASURED.
2. **Single-Site Tests Miss Distributed Stores** (`research/papers/pointwise-instruments-miss-distributed-circuits/`). MEASURED and publicly reproducible. It includes the preregistered SAE comparison on SAELens and Gemma Scope, and TransformerLens parity at 1.5×10⁻⁴ nats.
3. **The scene-generator exact K/V compile** (`research/demos/scene-generator.md`). 21/21 exact across 5 families, 0.0000 MAE, with a row-permutation control. MEASURED.
4. **The cross-model symbol table** (MEASURED, receipts bundled):
   - read ≠ author: held-out symbols read, but zero-shot authorship is at sham level;
   - one anchor authors at native parity;
   - an affine-ceiling negative result.
5. **The IRD sink grid**, 8/8. MEASURED, with receipts mostly private.
6. **Object value algebra and the donor-free writer.** The value algebra (blue mug, 9B port 0.471 vs sham 0.076) and the donor-free rank-64 writer (5/6) are MEASURED with private receipts. Both are small-n, and the writer's labels are provisional.
7. **The wall-picture hotpatch** (4-seed protected-object certificate) and the Darkroom composition. MEASURED, with a verifier.

**Prior art:**
- **Cross-model.** Relative representations and model stitching (Moschella et al., 2023), universal and concept-aligned SAEs (SPARC, USAEs), and the Linear Representation Transferability Hypothesis already cover cross-model feature maps. New here: authorship judged through an unchanged generative consumer, the read ≠ author split with an affine ceiling, and the diffusion-conditioner domain.
- **Editing.** Prompt-to-Prompt, Stable Flow, KV-Edit, FLUX Kontext and RF-Solver/FireFlow, evaluated on PIE-Bench, are ahead as editors. The contribution here is mechanism and measurement: timing-dependent edit kind, and exact compilation.

**Lab-attention judgment (asserted):**
- **The methods pair (items 1–2) plausibly yes.** Its audiences are the Anthropic and GDM interpretability teams and Black Forest Labs.
- **What would raise the odds most:** a completeness or recovered-behavior score for the certified route, and a head-to-head against ACDC, attribution patching and SAE circuits.

**Hazards flagged:**
- `research/demos/` is untracked.
- Room Studio is deployed from an unmerged branch.
- The capabilities draft cites about 50 private-only numbers.
- Several numbers were corrected upstream and are now handled.

## 4. Revised verdict at end of session (before the author's correction)

| Item | Lab attention? |
|---|---|
| IRD draft | No as standalone; fold its cut and isolated-swap results into the measurement paper. |
| Capabilities draft | No as standalone; reuse the transaction grammar as discussion. |
| FLUX certified circuits + measurement paper | Plausibly yes, once exposed. |
| Program (Saturn and the certification standard) | Highest ceiling; gated on packaging. |

**Highest-value next experiments:**
1. A completeness score for the certified route, with method baselines.
2. Address specificity on a public model.
3. C7 redesigned to swap an intermediate step at n ≥ 20, against truncation and mistake-insertion baselines.

## 5. Author's correction (2026-09-30): what the first pass missed

As stated by the author; these are to be verified in the deeper dig.

- **The "final boss" is a circuit, not only a framing.** It is the same circuit as the FLUX.2 whitepaper's certified route.
- **It ties directly to** the `research/bfl/demos/` series: the twenty-axis route, the hotpatch, apples (the recipient capability patch), fox (the semantic circuit object), and the symbol table.
- **It was found in essentially every diffusion and autoregressive model above about 1B that was checked.**
- **It laid the groundwork for the scene generator** and for the finding that the residual builds the circuit out over *time*.
- **The IRD paper is the account of why standard tools failed to find this circuit**, when Saturn found it once the cross-conditioner work succeeded (`research/bfl/demos/cross-compiled-conditioner.md`, `cross-family-conditioner-repair.md`).

## 6. A second session's line of thought (pasted by the author; not re-verified here)

A separate session reviewed the final-boss docs and drew these conclusions.

**Thesis restated** as a transaction:
1. Context forms the task.
2. An addressed residual or K/V carrier holds it across positions.
3. A local write and a protocol action happen at the recipient.
4. The unchanged native consumer produces the behavior.
5. The result is committed or rewound.

**Bars.**
- 0.90 is the FLUX strict sufficiency gate, and 0.30 is slightly stricter than the FLUX 0.35 sham and wrong-axis ceiling. Both are in-family bars.
- The induction certificates demanded R ≈ 1.0: Pythia (300 − 6)/(286 − 6) = 1.05, and Qwen source cut 0.010 with repair 0.995.

**Loss-based R is the wrong yardstick for the final boss:**
- **Static vs temporal.** Single-step patching barely transfers while all-step patching does, so a static component-set R would score a real temporal circuit near zero.
- **Loss vs consumer output.** Verdicts are exact typed consumer outputs (k/4, pixel equality), not cross-entropy.
- **Mean ablation vs installation.** The evidence is installing formed K/V into a neutral recipient, which mean ablation cannot express.

**A success-form R-analogue already in the receipts:**

| Transaction | R-analogue | n |
|---|---|---|
| Qwen2.5-Coder-7B joint-K/V installation | (4 − 0)/(4 − 0) = 1.0 | 4 operands |
| FLUX mediator restore | 0.83 image stream only; 1.00 both streams | 1 seed |

**Leaks.** In the K/V chain, joint-row-shift is 4/4 install (2/4 full continuation) and the row-permuted residual is 4/4. The receipt marks "bounded chain candidate: False, terminal claim: false"; n = 4 throughout.

**Measured differences from classic circuits:**
- **Joint K/V carriage:** K-only and V-only 0/4, joint 4/4.
- **Protocol vs formation:** protocol alone 0/4.
- **Non-monotone dose:** 0.25 → 4/4, 0.5 → 0/4.
- **Consumer-bound authority:** register plus program 1.000; either alone 0.403 or 0.712.
- **Time accumulation:** separation grows from 0.355 to 9.723 across denoising steps.

**Hypothesis it raised (unverified there).** Attribution graphs freeze attention patterns and do not explain cross-position information movement. That is the gap K/V-carried transactions target. The capabilities draft §8 already cites Anthropic's circuit-tracing methods paper for the stated limitation ("we account for the information which flows from one token position to another, but not why").

## 7. Deeper dig into the circuit itself (same day, in progress)

Read: `obsidian/blog/2026-08-21-114500-the-final-boss-circuit.md`, `research/bfl/README.md`, `research/bfl/demos/{cross-compiled-conditioner, semantic-circuit-object-part-III, twenty-axis-semantic-route-circuit, diffusion-time-causal-clock, distributed-kv-causal-route}.md`, and `research/bfl/docs/certified-semantic-circuits/paper.md` (abstract, §5, §6, §8.3, §13).

**What the circuit is (measured, per the cited receipts):**
- **Origin.** "Final boss" names the conjecture that every model has a late, path-constituted residual circuit that commits the output, a *sink* that smaller circuits write into. Its anchor is the FLUX.2 identity relay (`job-7d53e47755f7`).
- **First LM certificate (2026-08-21).** In SmolLM2-1.7B, `job-6650205b45eb`:
  - single layers carry 1.5% and 19.3% of the effect, while the second half of the stack flips fox→wolf;
  - P4 (`job-0a07cb92d360`) shows the hidden-slot write and the full-K/V-trace write carry the same object (1.006–1.093), while a single K/V slice carries ≈ 0.01–0.11.
- **One route carries every axis.** In FLUX.2 Klein 4B the route `joint.2 → joint.3 → joint.4 → single.0` carries all 20 tested contrasts across 12 categories (6 strict 9/9, 11 carrier 7/9, 3 candidate). The causal route gates replicated on unopened seeds and on new prompts.
- **Time-accumulated.** Single-step transplant leaves pixel distance 48.4 to target, while all-step leaves 0.47. Return-state separation grows 0.355 → 0.919 → 2.487 → 9.723 over four steps.
- **Coordinate-free.** Per-module trajectories are nearly collinear across axes (min cosine 0.986), while physical support barely overlaps (mean Jaccard 0.063). The route survives a token-position shift (horse/fox/rabbit 0.988).
- **Separable from the substrate.** A foreign conditioner gives clean but wrong images. Through the route, the foreign color separation at the route's entry is damped about 43×, and return-state separation recovers to about 71% of native by the last step. Native donation restores the byte-identical image.
- **Discovered through the conditioner swap.** The Rosetta comparison of Qwen, SmolLM2 and Mamba conditioners exposed where semantics diverge downstream:
  - route flow was 0.9312 native vs 0.5300 SmolLM2;
  - full-state rescue was 0.751 / 0.817, while compact selectors reached ≤ 0.051.
- **Found without prompts.** A promptless perturbation pass recovered 3 of 4 route sites and the `joint.4 → single.0` edge, with off-route shams ≤ 0.095.
- **Replicated across FLUX checkpoints** (Part III), as object registers on the same grammar: base-4B undistilled at 50-step CFG, klein-9B (subject write 0.743 vs sham 0.043), and FLUX.1-schnell at T5 noun-phrase-window grain.
- **Every later tool writes through this route:** object registers, value algebra, the cross-model symbol table, hotpatch timing, the scene compiler, and the scene-generator work.

**Revised reading.** The first pass judged the two drafts by their own text. The circuit behind them is stronger than either draft shows. It is a single, general, time-accumulated, coordinate-free semantic transport route in a production DiT, with promptless rediscovery and a substrate-swap control. The drafts abstract it into "transaction" and "trajectory functional" vocabulary and lead with thinner autoregressive material.

**Main reviewer objection to preempt.** Is the route simply FLUX's architectural text→image conditioning pathway? In FLUX, text enters the image stream through the joint blocks and is merged at `single.0`. A pathway every semantic must cross would naturally carry every axis and be found promptlessly. The whitepaper does not directly address this.

The non-architectural content is:
- the route starts at `joint.2`, not `joint.0`;
- single-step invisibility;
- coordinate freedom;
- substrate separation.

To settle it, run matched alternative-path controls: `joint.0–1`, the image stream only, and other single-block spans.

## 8. A third session's outside view (pasted by the author; partly re-verified)

**Mapping to the stated limitations** of Anthropic's *Circuit Tracing* (2025-03-27):

| Their stated gap | How this work relates |
|---|---|
| Attention patterns are frozen and unexplained | K/V carriage runs the real attention transaction: it shows *what* moved, not why QK chose it |
| Cross-position flow: they account for "the information which flows from one token position to another, but not why" | The joint K/V carrier result |
| Error nodes | Native replay has no replacement model, so there are no error nodes by construction |
| Replacement faithfulness | Interventions are on the real model |
| Inhibitory and inactive features | Measurable with fork/replay counterfactuals, but not yet demonstrated |

**Verified this session:**
- The frozen-attention limitation is stated on the methods page.
- Anthropic has since published *Tracing Attention Computation Through Feature Interactions* (transformer-circuits.pub/2025/attention-qk), which targets the QK "why" directly. Any claim that this work fills the gap must cite it and say what it adds.

**Auditing game** (Marks et al., arXiv 2503.10965). Verified in outline: the API-only team failed, and teams with data and weight access succeeded, with SAEs used to surface the relevant training documents. A reported 2026 follow-up finding negligible circuit-tracing benefit was not verified.

**Correction to that session.** It identified "the IRD paper" with *Single-Site Tests Miss Distributed Stores*. They are separate papers: the latter is the measurement paper, and IRD is the theory companion built on its receipts.

**Bars it cites.** R ≥ 0.90 is stricter than IOI's about 87% and above Anthropic's replacement score of about 0.61. It proposes adding resample ablation, with size-matched random controls, to answer Miller et al. (2024). Its G1/G2 framing comes from the 2026-09-30 holy-grail audit, which the author flagged as same-day tooling; treat those items as unconfirmed.

## 9. Model census for the circuit (subagent, Opus 4.8; excludes the author-flagged 2026-09-30 run)

**Full certificates above 1B: 4 models** (MEASURED):
- **FLUX.2 Klein 4B.** Nine-gate route certificate, public and clean-room audited.
- **SmolLM2-1.7B.** Four-quadrant sink certificate (`job-6650205b45eb`, grid `job-72f0e98679d5`).
- **Qwen3-8B.** Four-quadrant sink certificate after the fp32 recheck (`job-6299f2391d5c`, public).
- **Qwen3-30B-A3B.** Identity four-quadrant certificate (`job-7cc5b24954f0`, `job-ef8408d9c3d2`, private only). The generic floor still answers "fox", and the arithmetic cell is issued-qualified.

**Distributed pattern, no four-quadrant certificate: 2** (public, 2026-09-22 SAE panel). Gemma-2-2B: best single layer .08, second half .94. Qwen2.5-1.5B: best single layer .08, second half .92.

**Below 1B:**
- Qwen2.5-0.5B certifies.
- Pythia-410M certifies at capability onset.
- Pythia-70M is concentrated (79–81% of necessity in one layer).
- GPT-2 124M is concentrated: 20 SAE features at one layer remove the effect.

**Above 1B, trend, partial, failed or not established: about 13:**
- FLUX checkpoints: base-4B, Klein 9B (one seed), and FLUX.1-schnell (route .6915 = 98% of the all-joint ceiling, not a same-circuit certificate).
- Code models: Qwen2.5-Coder-7B (transaction, terminal claim false) and Coder-1.5B.
- Qwen3-1.7B.
- OLMoE-1B-7B (kernel only).
- Pythia-1.4B (kernel only).
- Mamba-2.8B, tested at the wrong cut; the recurrent-state cut was never run.
- SDXL ×3, Krea 2 and Chroma1-HD, tested by whole-conditioner swap only, with no specificity.

**Same object or analogy?** The author's own documents call the autoregressive sink a role-level analogy with a shared proof grammar, not the same physical circuit:
- certified-semantic-circuits `paper.md:295`: "the proof grammar — though not the FLUX route itself — survived transplantation";
- `obsidian/blog/2026-09-03-111020-…:284`: "The same physical final-boss circuit exists in diffusion and AR | No".

The defensible cross-model claim is "the same certificate shape appears in 1 diffusion and 3 AR models above 1B (plus 2 at pattern level)". It is not "the same circuit in every model above 1B".

**Mis-citations verified in this session** (fix before any external reader):
1. **IRD §5 grid, diffusion-identity row.** It cites "bundled `job-6650205b45eb`", but that report contains no 0.0013 / 0.222 / 0.911 values. The FLUX four-quadrant numbers are in `pointwise…/evidence/instrument-trial/bundle/case-1/circuit-panel-ledger.json` (0.001333, 0.911229), and the panel job is `job-7d53e47755f7`.
2. **IRD §5, 30B extension.** It lists `job-38c1c37dd591`, which is a SmolLM paged-fp32 smoke job (`saturn/experiments/2026-08-21-wall-a-addressing/README.md:1629`). The 30B receipts are `job-7cc5b24954f0` and `job-ef8408d9c3d2`.
3. **Capabilities §3, scene-edit row.** It pins sufficiency .9133 to `job-3cd13239dd91`, a mediation-steps report (`case-5`) that does not contain .9133. Its .0225 does appear there. Find the true source for .9133 / .7705.

**Also from the census:**
- The P4 sufficiency write (`job-0a07cb92d360`) was killed by a VRAM leak, and its no-op gate was never recovered. The IRD paper discloses this; keep the disclosure.
- The pointwise paper's Pythia-70M single-layer claim (`paper.md:149`) has no receipt in its folder.

## 10. Revised verdict after the deeper dig

**The circuit is more important than either draft shows.** It is one route carrying all 20 tested semantic axes in a production DiT, with these properties:
- invisible to single-step patching, because it is time-accumulated;
- coordinate-free;
- rediscoverable without prompts;
- separable from its substrate.

The same four-quadrant signature recurs in three autoregressive models above 1B (1.7B, 8B, 30B MoE), with a measured scale floor and an onset at capability. This is a real cross-modal methods result: standard instruments systematically miss a class of accumulated circuits, and a certificate finds them. It answers the frozen-attention and cross-position limitations Anthropic itself states, and the model is BFL's own.

**The drafts are the bottleneck:**
- **The story is split across four documents:** the whitepaper, the single-site measurement paper, IRD, and capabilities.
- **IRD omits its own discovery story:** the cross-conditioner contrast and the 20-axis route.
- **Capabilities buries the circuit** under the transaction vocabulary.
- **Three citations are wrong**, and "every model above 1B" overstates the record.

| Item | Lab attention? |
|---|---|
| IRD draft as written | No |
| Capabilities draft as written | No |
| One consolidated paper (route + time accumulation + instrument trial + AR certificate grid with public receipts + alternative-path controls + resample-ablation check) | Plausibly yes: BFL, and the Anthropic and GDM interpretability teams. A methods paper, not a safety headline. |

**What would push it over:**
1. Alternative-path controls that answer "it is just the text→image bridge".
2. Public receipts for the AR certificates (30B is private only).
3. A head-to-head on Gemma-2-2B (public SAEs exist) showing attribution graphs or ACDC miss what the certificate finds.
4. A one-number completeness score for the FLUX route.

## Sources (web, this session)

- [Single-Position Intervention Fails (arXiv 2605.04061)](https://arxiv.org/html/2605.04061)
- [Single-Layer Activation Edits Easily Corrupt Factual Recall but Rarely Repair It](https://aclanthology.org/2026.trustnlp-main.38/)
- [Models Take Notes at Prefill: KV Cache Can Be Editable and Composable](https://arxiv.org/html/2606.17107v1)
- [Relative representations (Moschella et al.)](https://arxiv.org/html/2209.15430v2)
- [SPARC: Concept-Aligned Sparse Autoencoders](https://arxiv.org/html/2507.06265v1)
- [Linear Representation Transferability Hypothesis](https://arxiv.org/pdf/2506.00653)
- [Stable Flow (2411.14430)](https://www.alphaxiv.org/abs/2411.14430)
- [KV-Edit (2502.17363)](https://arxiv.org/html/2502.17363v2)
- [The Hydra Effect (2307.15771)](https://arxiv.org/abs/2307.15771)
- [Does Localization Inform Editing? (2301.04213)](https://arxiv.org/pdf/2301.04213)
- [Circuit Faithfulness Metrics Are Not Robust (2407.08734)](https://arxiv.org/pdf/2407.08734)
- [Circuit Tracing: Revealing Computational Graphs in Language Models](https://transformer-circuits.pub/2025/attribution-graphs/methods.html)
- [Tracing Attention Computation Through Feature Interactions](https://transformer-circuits.pub/2025/attention-qk/index.html)
- [Auditing language models for hidden objectives (2503.10965)](https://arxiv.org/html/2503.10965v2)
