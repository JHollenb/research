# Their work and ours: what is shared, what we can give, what we can take

Status labels: **measured** means we ran it and there is a receipt; **asserted** means it is reasoned from code
or prior results and has not been tested on their setting. Paths are relative to `~/domains`.

## 1. The two programs in one paragraph each

**Theirs** (see [README](README.md)). Two embedding spaces trained separately, such as DINOv2 images and MPNet
captions, share enough relational geometry that a single rotation W aligns them with no paired data. The
correspondence comes from matching cluster geometry (QAP on centered kernels), followed by alternating
Hungarian matching and Procrustes. Alignment quality is judged by retrieval (FOSCTTM) and predicted by CKA.

**Ours** (see `obsidian/blog/2026-10-09-171008-from-a-swapped-text-encoder-to-time-circuits-and-a-symbol-table.md`
and `obsidian/arcs/cross-conditioner-to-time-circuits.md`).
- **Swapping the text encoder.** We replaced the text encoder of a frozen FLUX.2 Klein 4B image model with
  foreign language models (SmolLM2-1.7B, Mamba-1.4B) through trained adapters. The images were clean but
  semantically wrong. Donating the full native conditioning tensor restored the byte-identical native image,
  which localized the whole fault to that tensor.
- **The symbol table.** Following the failure down to individual rows gave the cross-model symbol table:
  per-symbol correspondences between class displacements (a subject row minus its template scaffold), held in
  a shared low-rank subspace.
  - **Reading:** an unanchored bridge reads held-out symbols at 21/36 distinct rows (chance 2/36).
  - **Authoring:** an anchored bridge authors held-out symbols through the frozen image model at native
    parity (progress 0.523–0.810 vs native 0.520–0.817).
- **Consumer as judge.** Every claim is judged by the native consumer, meaning the unchanged downstream model
  producing an image or a next token, under exact replay.

## 2. What is shared

| | theirs | ours |
|---|---|---|
| Core question | can two separately trained spaces be put in correspondence? | can a foreign model's states drive a native consumer? |
| Unit of comparison | centered, unit-normalized embeddings | class displacements against a template scaffold (centering per context) |
| Map | one semi-orthogonal W | rank-40 shared subspace + 40×40 ridge; per-symbol anchors |
| Correspondence source | geometry (QAP on CKA kernels) | lexical anchors (same token in both vocabularies); geometry as of E0 below |
| Evaluation | retrieval (FOSCTTM); CKA predicts it | consumer authorship (render progress P vs native ceiling, shams, exact no-op) |
| Main caution | alignment is coarse | reading ≠ authoring; global cosine is dominated by scaffold |
| Text → image | Qwen3/MPNet → DINOv2 → RAE diffusion, no pairs | SmolLM2/Mamba → Qwen3 conditioner → FLUX.2, trained adapter |

Two specific overlaps:
- **The same conditioner.** Their Qwen3-8B language model is the stock text encoder of FLUX.2 Klein 9B. Our
  provenance work matched it by embedding bytes; see
  `obsidian/blog/2026-07-31-145130-the-conditioners-were-stock-checkpoints.md`.
- **Mirror-image designs.** Their text-to-image demo is a cross-conditioner experiment run without pairs. Ours
  is the same experiment run with a trained adapter, followed by a causal localization of the failure.

## 3. Their premise holds on our data (measured)

Run: `experiments/e0_symbol_qap/`. Input: our symbol-table receipt `job-0706b0497903`, 18 animals × 4 distinct
prefixes, SmolLM2 vs Klein-Qwen.
- **Shared geometry.** The off-diagonal entries of the two spaces' class-mean centered-cosine kernels correlate
  at **0.890**.
- **Zero-pair recovery.** QAP with zero pairs recovers the symbol correspondence **18/18**. This holds with
  2-opt local search and restarts (where the true permutation is the global optimum) and with **their MPOpt
  solver**. It also holds on each of the 4 prefixes alone.
- **Null.** With a Gaussian geometry in place of SmolLM2, the solver gets 0–2/18 correct.
- **Margin.** The margin is thin: the true objective is 23.59 and the best single swap is 23.54. Expect errors
  as the bank grows.
- **Fully unpaired rows.** With animal and prefix both unknown, 41.7% of rows are recovered (chance 5.6%).
  SmolLM2 rows cluster by prefix, not by animal (ARI 0.019; Klein-Qwen 0.331).
- **Solver note (ours, not theirs).** scipy's FAQ solver alone got stuck at 1/18, below the true objective.
  Their MPOpt does not have this problem.

This extends their claim to a new kind of pair: a language model against the conditioner of a diffusion model,
at the level of individual symbols. In our setup the correspondence is also checked causally, because the
anchored map it implies authors through the image model.

## 4. What we can do for them (detail and math in [response.md](response.md))

| claim | one line | basis | test |
|---|---|---|---|
| **A** scaffold dilution in generative pooling | The thinking-mode preamble is real (96–100% shared tokens), but token-level centering *lowers* CKA at Qwen3-1.7B with thinking on (−0.010 to −0.021, every cell): the preamble restates the caption. With thinking off, centering helps (+0.004 to +0.027). | **refuted** on effect sign (E3) | E3 |
| **A\*** non-visual scaffold axis *(post-hoc)* | In their stored Qwen3-8B-gen SPC embeddings, one axis holds 13.8% of variance with image R² 0.16. Removing it raises linear CKA 0.433 → 0.583 and lowers it for MPNet/Qwen3-Embedding. Clipped CKA hides the deficit. | measured offline (axis probe). Dropping the axis: SPC FOSCTTM 0.407 → **0.036** (single seed). Across 3 seeds the fix is 0.415 ± 0.055 → 0.038 ± 0.006, and the same drop wrecks MPNet and Qwen3-Embedding. The pseudo-pair detector failed (circular). A **gate detector** with no pairs (one fit per gate setting, chosen by matched cosine; ported from our spectral dimension ladder) picks the best setting for all three encoders in 9/9 model × seed cases | E5 |
| **B** commit-layer readout | A late non-final layer should align better than the last. | **supported, small**: depth 0.89 beats 1.0 by 0.007–0.015 in 5/6 no-thinking cells (incl. their `MeanPooling`); not for thinking-mode gen. Frozen B1/B2 failed on one 0.002 tie | E3 depth sweep |
| **C** span ceiling of pair baselines | Their `linear` baseline (and ASIF by construction) only sees keys through a p-dimensional projection. Mean fidelity is ≤ sqrt(captured energy) ≤ sqrt(top-p eigen-energy). This is why those baselines need 100–500 pairs. | proved (Lemmas C1–C2) | E2 |
| **D** read ≠ author | Near-zero FOSCTTM is compatible with low per-pair fidelity α. Measured on COCO: their unpaired map gives FOSCTTM 0.0073 with median α 0.527 (≈ 72% of mapped energy off the partner); 0% of pairs ≥ 0.895 (FLUX 8/8 zone), 43% ≤ 0.50. Oracles with 20k true pairs: orthogonal and least-squares maps retrieve identically (FOSCTTM 0.0027/0.0026) but differ by 0.21 in median α (0.57/0.78); their zero-pair map is 0.07 ± 0.03 below the best rotation (3 seeds). | proved (Prop. D1) + **supported** (E1) | E1, E4 |
| **E** anchor choice | If pairs are few, picking which images to caption (vision-side medoids) raises captured energy, and so the ceiling of C and D. Our symbol work: one anchor per concept lifts fidelity to 0.93–0.99. | Ky Fan (proved) + our Wall-A k=1 (measured) | E2 |
| **F** a consumer-grounded benchmark | Our FLUX and LM consumers have exact replay, a native-donation ceiling and shams. They could test any unpaired map with causal ground truth. | infrastructure exists (measured on our maps) | E4 |

## 5. What they can do for us

| idea | why it matters to us | status |
|---|---|---|
| **Geometry-derived anchors.** Use QAP/GW correspondence instead of string identity. | Wall A needed one paired example per symbol. E0 shows geometry alone gives the correspondence. This covers sources with no shared vocabulary: SceneGraph/CAD frontends (held-out progress −0.299), Mamba, image encoders. | measured on 18 symbols (E0); scaling untested |
| **MPOpt as the QAP solver** | Our ad-hoc FAQ got stuck; MPOpt and 2-opt both reach the optimum. | measured (E0) |
| **An orthogonal (Procrustes) constraint for adapters** | Our 15M-parameter SmolLM2→Qwen adapter overfit: train cosine 0.87, held-out about 0.20, direction cosine 0.02–0.06. A rotation has far fewer degrees of freedom. | asserted; offline test possible on the displacement dumps |
| **CKA as a pre-flight check** | Rank candidate foreign encoders and layers (SmolLM2 vs Mamba; which TECM slice) by CKA against the native conditioner before spending GPU time. | asserted; their R² = 0.73 is on their setting |
| **The k/p pair weighting** | A principled way to mix a few true anchors with many pseudo-pairs in our bridges. | asserted |
| **Their refinement loop** | Alternating Hungarian matching and Procrustes could raise our 41.7% fully unpaired row recovery. | untested |
| **Their RAE as a second consumer** | A DiT conditioned on one global embedding is a clean place to test whether conditioning is consumed with a front-loaded kernel, as we measured in FLUX (≈ [0.21, 0.22, 0.08, 0.04]). | asserted; needs their checkpoint |

## 6. Joint opportunities

1. **An unpaired symbol table at scale.** Run their aligner on a 200-symbol displacement bank (E4, step 2) and
   validate it causally through FLUX.
2. **"Shared geometry, model-specific fidelity."** Their result is that geometry is shared well enough to
   read. Ours is that authoring needs fidelity beyond what shared geometry gives (α ≥ about 0.9 on FLUX) unless
   anchored. Together they say exactly how the Platonic hypothesis holds: at the level of relations, not at
   the precision a consumer needs. E1 measures where their maps sit on that axis.
3. **Alignability vs consumability.** CKA predicts retrieval. Does it also predict consumer progress? E4 would
   give the first data on this.

## 7. Other work of ours we checked against their pipeline (2026-10-09)

Sources: PhaseLock / rotation swamping (`research/papers/phaselock-kv-shifts/`), the swamping paper
(`research/papers/rounding-placement/`), `mdb` (`saturn-pub/packages/mdb`, v0.1.0), and the spectral-address /
learned-chart work (`obsidian/spf/2026-09-24-spectral-token-context-factorization.md`, memories of 2026-09-24/25).

| work | does it help them? | why | status |
|---|---|---|---|
| **Swamping** ("remove the invariant in high precision before rounding") | **No, as a fix; yes, as a check.** | Their files do not have the failure. The one embedding with a huge common component (Qwen3-8B-gen, ‖mean of unit rows‖ 0.93, about 88% of the energy) is stored **fp32**. The bf16 files (MPNet, Qwen3-Embedding, DINOv2) have per-coordinate \|μ\|/σ of 6–13, far below the ~256 at which bf16 would lose the centered residual (our swamping regime was 835–2371). Centering is done in fp32. | **measured** (stored-file read, ≤ 4096 rows). This rules out a storage artifact behind the §3.4 axis. |
| **Swamping, as an analogy** | Conceptual only | Our swamping result says a large invariant spends the budget meant for content. Their aligner shows the representational version: it locks onto the dominant axis, and when that axis is non-visual the matching fails (E5). Centering removes the first-order invariant (the mean) but not this second-order one. | inferred; E5 is the measured instance |
| **PhaseLock** (rotation swamping in re-rotated bf16 KV caches) | No | Their rotations are recomputed in fp32 each iteration and never applied repeatedly to stored low-precision vectors. One bf16 rounding of a mapped vector (~2⁻⁹ relative) is negligible next to α ≈ 0.5–0.8. | asserted from their code |
| **mdb** (reversible model debugger, exact replay, receipts) | Not today | The alignment is static linear algebra on stored matrices, so there is nothing to step or fork. The one model execution, Qwen3 generative pooling, is where mdb would help: replay the 128-token generation, fork at the `<think>` preamble, find where the non-visual axis is written. But mdb qualifies Qwen2/2.5, not Qwen3. | needs a Qwen3 adapter |
| **Learned nuisance-axis gates** (spectral dimension ladder: learned gates zeroed 61/61 nuisance axes) | **Yes (measured, seed 0).** Ported as discovery selection, the detector picks the best setting in all three encoders | A gate per language PC, trained without pairs, is the natural generalization of "drop the top PC". The trap is what E5's detector hit: the training signal must not come from the fit being corrected. The working signal: refit per gate setting, then score each fit by its own unpaired matched cosine (rows are re-normalized after gating, so scores compare). | response §3.5 |
| **Charts / spectral addresses** ("charts carry information, not geometry") | No | Re-coordinatizing an embedding cannot add shared information. That fits E5, where the gain came from *removing* an axis. The product-code / exact-join argument does not explain the rotation ceiling: the 0.21 gap between best rotation and best linear map is the cost of orthogonality (per-direction scale), not of a factorization. | asserted |

Net: none of the four is a new fix for them. The swamping line gives one measured check, now in response §10: the
scaffold axis is representational, not a precision artifact. The ladder's gate idea, ported as discovery selection, became the working
unpaired detector (response §3.5).
