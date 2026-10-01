# Prior-art audit: diffusion time, text-stream registers, and cross-architecture scope

**Audit time:** 2026-10-01 09:41:51 PDT  
**Scope:** `paper.md` §§2, 5, 8, 10, 13, plus the E8 and E9 findings records.  
**Method:** Claims were checked against the primary papers and proceedings linked below. No model jobs were run and the paper was not edited.

## Bottom-line verdict

The paper has a real and potentially important contribution, but its current prior-art framing overclaims it. The claim in §13 that Prompt-to-Prompt, Stable Flow, KV-Edit, and Padding Tone “locate *where* an edit acts” while this paper “adds *when*” is false. Prompt-to-Prompt explicitly varies the number of denoising steps receiving an intervention. Since 2025–2026, PCI, Tinaz et al., TIDE, and DifFRACT have made diffusion-time dynamics a central object of study; PCI asks almost exactly “when does a concept lock in?” across five diffusion/flow models, and DifFRACT traces and causally intervenes on timestep-dependent feature circuits in four-step FLUX.1-schnell.

The novelty that survives is narrower and, in my view, stronger:

1. a **single-site versus whole-path, necessity versus sufficiency matrix** applied to a typed internal cut and judged by the native downstream consumer;
2. a clean FLUX.2 Klein 4B instance in which the text-stream intervention has a large single-step/all-step gap under exact replay, with source interchange separated from deletion-to-null;
3. the **formed-state versus residual-write distinction** in language models, including a late necessity band, a single residual authoring write, and a layerwise commit ledger;
4. a comparative taxonomy of **mixed quadrants**: clean four-quadrant behavior in FLUX, concentrated early necessity but distributed sufficiency in SDXL, and distributed necessity but concentrated writing in language models and Mamba.

No reviewed paper makes that exact package of claims across a DiT, autoregressive transformers, and a selective state-space model. But the manuscript itself also does not establish one symmetric “time circuit” across all three. By its own strict results, the clean four-quadrant certificate is established in diffusion; most language-model and Mamba cells have a distributed read/necessity side and a concentrated write side. The defensible cross-architecture result is therefore a shared **analysis framework and recurring asymmetric path anatomy**, not a shared certified circuit mechanism.

## Direct overlap, paper by paper

| Work | What it actually establishes | Overlap with this paper | What remains distinct here |
|---|---|---|---|
| [Prompt-to-Prompt](https://arxiv.org/abs/2208.01626) (Hertz et al., ICLR 2023) | Injects source cross-attention maps during selected denoising steps. Its timestamp parameter controls how long injection is applied; Figure 6 sweeps 0–100% of steps and reports the preservation/editability tradeoff. | Direct prior art for *when* an intervention lands and for trajectory-wide attention injection. | It does not test single-step versus whole-path necessity and sufficiency at one typed cut, or exact replay. |
| [Stable Flow](https://openaccess.thecvf.com/content/CVPR2025/html/Avrahami_Stable_Flow_Vital_Layers_for_Training-Free_Image_Editing_CVPR_2025_paper.html) (Avrahami et al., CVPR 2025) | Finds a fixed set of “vital” FLUX/SD3 layers through residual bypass and injects reference image embeddings into those layers during parallel generation. The layer study uses 64 prompts/seeds; the editing evaluation contains 3,200 samples and a user study. | Strong prior for distributed layer importance and for loading a dynamic source trajectory onto a fixed architectural subset. | Its scientific question is which depth sites support stable editing, not whether effect is path-constituted across denoising time. |
| [KV-Edit](https://openaccess.thecvf.com/content/ICCV2025/html/Zhu_KV-Edit_Training-Free_Image_Editing_for_Precise_Background_Preservation_ICCV_2025_paper.html) (Zhu et al., ICCV 2025) | Records background K/V at **each timestep and block layer along the probability-flow path**, then reuses the corresponding cache during denoising. The authors explicitly describe the K/V as a deterministic path and intentionally use all layers/timesteps. | Very close prior for a timestep-indexed K/V trajectory as an installable state object. It weakens broad “scenes compile” and “time-formed cache” novelty language. | KV-Edit is an editing system. It does not compare a single cached timestep with the whole trajectory or diagnose necessity/sufficiency quadrants. |
| [Padding Tone](https://aclanthology.org/2025.naacl-long.389/) (Toker et al., NAACL 2025) | Uses causal replacement before **every attention block at every diffusion step** and finds prompt-contextual padding tokens acting as registers in FLUX and SD3. It studies six models with 500 prompts × 10 seeds per configuration. | Direct prior for semantic information being written into the text stream during diffusion, for register language, and for cross-architecture dependence on multimodal self-attention versus cross-attention. Calling it merely a “where” paper is inaccurate. | It does not sweep individual timesteps or certify whole-path versus pointwise dependence. The new result is the temporal four-quadrant behavior of a joint-region text-stream cut, not discovery that FLUX text tokens can serve as registers. |
| [Relative Representations](https://openreview.net/forum?id=SrC-nwieGJ) (Moschella et al., ICLR 2023) | Represents a sample by similarities to fixed anchors, giving practical invariance to latent isometries/rescaling and enabling zero-shot stitching/comparison across CNNs, GCNs, and transformers and across modalities. | Prior for the general idea that representation identity can be relational and coordinate-independent across models. | The paper’s §5.3 result is different: nearly collinear causal-profile trajectories with low coordinate overlap inside a FLUX carrier. Moschella is suitable motivation, not an anticipation of the causal route result. |
| [Temporal Concept Dynamics / PCI](https://arxiv.org/abs/2512.08486) (Görgün et al., ICLR 2026) | Switches prompts at every timestep to measure concept insertion/deletion and asks when concepts lock into the trajectory. It covers 800 samples, 100 seeds per experiment, and SD2.1, SDXL, SD3.5, PixArt-alpha, and FLUX.1-dev. It reports a cross-model hierarchy and differences between U-Net/DiT and diffusion/rectified flow. | The closest prior to §10’s “when a write lands selects what changes.” It also refutes the suggestion that prior temporal work would necessarily have reported the manuscript’s exact cross-architecture finding: PCI did publish cross-architecture temporal findings, but at the prompt/output level. | PCI has no internal typed cut, no whole-path transplantation, and no four-quadrant circuit certificate. |
| [Emergence and Evolution of Interpretable Concepts](https://arxiv.org/abs/2504.15473) (Tinaz et al., NeurIPS 2025) | Trains SAEs at diffusion stages, tracks emergence/refinement of concepts, and causally shows early composition control, middle-stage style control, and late texture-only effects in Stable Diffusion 1.4. | Direct prior for temporal causal intervention and for stage-dependent semantic roles. It makes “standard instruments see only space” too categorical. | It does not look for a single-step/all-step gap and uses learned feature surrogates rather than the paper’s native whole-state cut. |
| [TIDE](https://ojs.aaai.org/index.php/AAAI/article/download/37006/40968) (Huang et al., AAAI 2026) | Builds temporal-aware SAEs for DiTs to capture changing activations across denoising steps and supports causal steering/editing. | Direct prior for an interpretability instrument designed around diffusion time. | It decomposes per-step activations; it does not provide this paper’s path necessity/sufficiency test. |
| [DifFRACT](https://arxiv.org/abs/2606.15796) (Mazur et al., 2026) | Trains timestep-conditioned transcoders for FLUX.1-schnell, builds attribution graphs at each of four denoising steps, and measures a text-to-image shift: text-stream attribution falls from 89.9% to 5.4% while image-stream attribution rises from 10.1% to 94.6%. Early versus late supernode suppression causally validates the temporal split. Its ordinary interventions scale features at every timestep. | This is the closest mechanistic prior. It already studies semantic propagation across diffusion steps, text/image stream migration, and time-window-specific causal interventions in four-step FLUX. Omitting it from the consolidated paper is a serious scholarship gap, especially because the earlier `certified-semantic-circuits` paper already called it the closest related program. | DifFRACT constructs a separate local graph at each step and does not ask whether no single step matters while the whole trajectory does. It also leaves reconstruction-error channels. The manuscript can claim its certificate exposes a failure mode of pointwise graphs, but only after a head-to-head test or as a precise methodological argument, not as “cannot see by construction.” |

## Is “where, not when” a fair summary?

No.

- It is plainly false for Prompt-to-Prompt: its edit function depends on timestep, it introduces a timestamp cutoff, and it sweeps the fraction of diffusion steps receiving source attention.
- It is false for Padding Tone as written: the intervention is installed before every attention block through all diffusion steps, and the paper explicitly asks when/how pads matter in the pipeline.
- It is especially untenable after PCI, Tinaz et al., TIDE, and DifFRACT, all published or public before this September 2026 draft.
- It is only approximately fair for Stable Flow’s main *localization* claim, which emphasizes depth, although its intervention still operates along the source and target trajectories.
- KV-Edit is best described as **whole-trajectory engineering without a temporal causal decomposition**, not a purely spatial locator.

A fair replacement would say: prior work has manipulated and measured diffusion time, including prompt-switch schedules, early/middle/late feature interventions, temporal SAEs, and timestep-conditioned attribution graphs. This paper adds a specific causal question they do not ask: whether a behavior is absent from every single timestep intervention yet present under intervention on the complete trajectory at a fixed typed cut.

## Claims that need narrowing

### “Standard instruments cannot see time circuits”

This should become a claim about the tested **pointwise use** of an instrument, not the instrument class. A temporal SAE or transcoder can represent step-varying features; DifFRACT already compares graphs and interventions across steps. These tools might still miss this paper’s carrier if the signal lies in reconstruction error or if each step is analyzed independently, but that is an empirical failure mode. The manuscript has a direct Gemma circuit-tracer result and a direct FLUX single-step patching result. It does not yet have a DifFRACT/TIDE-on-the-same-FLUX-cut result.

### “A new class of circuits”

As terminology, the space/time distinction is useful. As a priority claim, it needs a qualifier: **a four-quadrant causal class defined at an accumulation cut**. Distributed computation through time, timestep-specific concept formation, temporal feature trajectories, recurrent-state mechanisms, and all-step cache installation all have substantial prior art. The novelty is the certificate and the exact asymmetry it reveals, not the general fact that iterative models compute through time.

### “The same certificate shape across diffusion + AR + Mamba”

This is too strong if read as four-quadrant replication. The paper’s strict summary already says otherwise:

- FLUX.2 Klein 4B is the clean instance.
- Klein 9B identity reproduces the four quadrants on two seeds, but misses one of nine semantic-route gates; lighting is mixed.
- SDXL refutes the preregistered time-circuit prediction on necessity because steps 0–1 are individually necessary; only sufficiency is path-like.
- The language-model formed-state cut often has distributed necessity but residual writing is concentrated.
- The Mamba four-quadrant certificates were retracted after full sweeps found late writers.

The valuable cross-architecture claim is: “the same matrix exposes different path anatomies at comparable cuts, and a write-once/commit-late pattern recurs in transformers and Mamba.”

### “Static infrastructure / dynamic circuit”

The exact measurements in §8 can be novel, but the abstraction has close antecedents: Stable Flow uses a fixed vital-layer set with prompt-specific injected features; KV-Edit uses a fixed algorithm over timestep/layer-indexed dynamic K/V; Prompt-to-Prompt applies a fixed temporal operator to prompt-specific attention maps. Pitch §8 as a measured decomposition of this FLUX mechanism (including exact composition and two-parent rescue), not as the first static/dynamic decomposition of diffusion editing.

### “Scenes compile”

The 21/21 pixel-exact result across seven specimens and five families is potentially strong. The priority claim must distinguish it from trajectory caching/injection systems such as KV-Edit. “A prompt compiles to an installable source that reproduces native images exactly” is defensible if the compiled object and five-family result are public and independently runnable. As drafted, the relevant demos remain under TODO R6/private evidence, which prevents reviewers from assessing how much this exceeds cache replay.

## What the new E8 and E9 results do to the claim

E8 is useful replication, but should not be presented as a second strict nine-gate certificate. Identity shows the four quadrants on two seeds and two interchangeable windows, while the wrong-axis gate fails on one seed; lighting has an individually necessary first step on seed 7217 and weak all-step behavior on seed 4242. This supports a genuine identity result and a model/axis-dependent mixed-cell story.

E9 is scientifically valuable because it is a preregistered refutation. On one SDXL seed/contrast/cut, all-step writing is required, but steps 0–1 are individually necessary. That sharply distinguishes “distributed sufficiency” from a clean time circuit and strengthens the four-quadrant matrix as an analysis tool. It weakens any universal diffusion claim.

Together, E8/E9 make the paper more credible if they are used to emphasize **heterogeneous quadrant anatomy**, rather than treated as weaker replications of a universal class.

## Evidence standard relative to peers

The paper is unusually strong for a mechanistic-interpretability case study in several respects: exact no-op checks, native-consumer outcomes, interchange/deletion separation, full single-site sweeps after discovering earlier mistakes, preregistered refutations, and an unusually candid retraction ledger. The breadth across diffusion, transformer LMs, and Mamba exceeds most papers in this area.

Its weak point is that evidence volume is not the same as evidence concentration. Direct temporal-diffusion peers have much larger standardized evaluation sets:

- Padding Tone uses six model families and 5,000 images per model/representation configuration.
- Stable Flow uses a 3,200-sample editing set plus a user study.
- PCI uses five models, 800 concept/context samples, normally 100 seeds per experiment, and seed-budget analysis up to 1,000 seeds.
- DifFRACT evaluates 80 step-indexed graphs for its temporal analysis and releases the feature models/code.

By contrast, the manuscript’s cleanest causal result is concentrated in a small number of FLUX contrasts and seeds; much evidence is private; no other lab has replicated it; and several headline rows are assembled from different experiments with different gates. That is acceptable for discovery, but not for unrestricted claims such as “the class is the norm” or “today’s tools are built not to see it.”

My grade for this slice of the paper:

| Dimension | Grade | Reason |
|---|---:|---|
| Core causal idea | A− | The four-quadrant question and formed-state/residual-write split are sharp and useful. |
| Diffusion evidence quality | B+ | Exact causal replay and multiple operators are excellent; key sample counts and public reproducibility lag direct peers. |
| Cross-architecture breadth | A− for exploration / B− for terminal claim | The survey is unusually broad, but the architectures do not all certify the same circuit class. |
| Prior-art accuracy | C− | The “where, not when” sentence and omission of PCI, Tinaz, TIDE, and DifFRACT are material errors. |
| Publication readiness of this claim set | B− / major revision | The result should attract serious interest after narrowing, consolidating, and publicly packaging the core evidence. |

## Recommended related-work correction

The diffusion paragraph should distinguish four lines of prior work:

1. **trajectory-scheduled editing:** Prompt-to-Prompt and related attention injection;
2. **whole-trajectory state reuse:** KV-Edit;
3. **temporal concept dynamics:** Tinaz et al. and PCI;
4. **temporal internal decompositions:** TIDE and DifFRACT.

Then state the actual gap: none jointly performs single-step and whole-trajectory necessity and sufficiency at the same internal cut under exact replay and the unchanged native consumer.

## Frontier-lab attention, for this part of the paper

Yes, the strongest pieces are attention-worthy: the clean FLUX single/all-step crossover, the operator-sensitive null/source distinction, the commit ledger, and the direct circuit-tracer miss are exactly the kind of surprising causal results that Anthropic/OpenAI interpretability researchers would inspect. The broad “new class” framing is likely to trigger skepticism until the temporal-diffusion literature is handled correctly and the key receipts become public and independently runnable. The result is more likely to land if presented as a precise failure mode and a new certificate than as the first discovery that diffusion semantics evolve over time.

## Primary sources checked

- Hertz et al., [Prompt-to-Prompt Image Editing with Cross Attention Control](https://arxiv.org/abs/2208.01626)
- Avrahami et al., [Stable Flow: Vital Layers for Training-Free Image Editing](https://openaccess.thecvf.com/content/CVPR2025/html/Avrahami_Stable_Flow_Vital_Layers_for_Training-Free_Image_Editing_CVPR_2025_paper.html)
- Zhu et al., [KV-Edit: Training-Free Image Editing for Precise Background Preservation](https://openaccess.thecvf.com/content/ICCV2025/html/Zhu_KV-Edit_Training-Free_Image_Editing_for_Precise_Background_Preservation_ICCV_2025_paper.html)
- Toker et al., [Padding Tone: A Mechanistic Analysis of Padding Tokens in T2I Models](https://aclanthology.org/2025.naacl-long.389/)
- Moschella et al., [Relative Representations Enable Zero-Shot Latent Space Communication](https://openreview.net/forum?id=SrC-nwieGJ)
- Tinaz et al., [Emergence and Evolution of Interpretable Concepts in Diffusion Models](https://arxiv.org/abs/2504.15473)
- Huang et al., [TIDE: Temporal-Aware Sparse Autoencoders for Interpretable Diffusion Transformers](https://ojs.aaai.org/index.php/AAAI/article/download/37006/40968)
- Görgün et al., [Temporal Concept Dynamics in Diffusion Models via Prompt-Conditioned Interventions](https://arxiv.org/abs/2512.08486)
- Mazur et al., [DifFRACT: Diffusion Feature Reconstruction and Attribution for Circuit Tracing](https://arxiv.org/abs/2606.15796)

