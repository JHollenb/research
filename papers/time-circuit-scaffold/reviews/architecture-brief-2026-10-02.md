---
title: "Architecture brief for the Paper 2 rebuild"
type: coordinator-brief
date: 2026-10-02
sources: research/papers/scaffolds-and-dynamic-circuits/{outline,architectural-paper,bridge-paper}.md; obsidian/blog/2026-10-01-125322-stable-scaffolds-and-dynamic-circuits.md; obsidian/blog/2026-10-01-193730-time-formed-scaffolds-in-qwen-flux-and-mamba.md; obsidian/blog/2026-10-01-131907-saturn-vm-model-virtual-memory-evidence-checklist.md; saturn/docs/CAUSAL-CONTEXT-VM.md; reviews/evidence-inventory-2026-10-02.md
---

# Architecture brief: what Paper 2 claims

## The proposed architecture, in the author's terms

**Dynamic circuits loop through a stable time scaffold.** On each step, an operation does four things:
1. reads the present carried state;
2. acts through recurring writer and consumer roles;
3. changes the carried state;
4. thereby influences the next operation.

The machinery recurs. The operations, sources, addresses, payloads and state vary with each execution.

- **Time-formed state:** ordered execution forms state that later computation uses. The time axis depends on the regime:
  - diffusion: denoising steps;
  - autoregressive transformer: depth through the layers plus token positions (formation through depth, commit into late K/V, a later read);
  - state-space model: recurrent transitions.
- **The scaffold is "static"** in one sense only: the same causal responsibilities recur across executions at a declared resolution. Activations, addresses and effective pathways still change. The scaffold is identified by intervening on recurring roles and finding that they stay causally useful as prompts, payloads and operations change. It is **not** "one commit layer at a fixed index." Location-fixedness of a late band is at most one weak symptom.
- **Roles:** source; current operation/address; live reader or transition; writer; carried state; native consumer. A family-local lowering maps roles to sites, and the map can be partial and many-to-many. A role earns content only from native intervention consequences.
- **Functional form:**
  - a_t = A_m(s, u_t, z_t)
  - w_t = W_m(s, u_t, z_t, a_t)
  - z_{t+1} = T_m(z_t, w_t)
  - y_t = C_m(z_{t+1}, u_t)
  - Here z is carried state, u the current operation, s the contextual source. In Mamba one channel is h_t = ρ_t ⊙ h_{t−1} + w_t, read through s_t = ⟨c_t, h_t⟩ + D u_t.
- **The space circuit / dynamic circuit** is the source coalition, address, payload, dose, timing and participation that implement one computation on the scaffold. Example: eye color and eye geometry reuse 5–7 of the top 8 consumer heads, but their source programs share only 10–15 of 64 rows.
- **The Saturn VM / MVM is this architecture made executable.**
  - **State and planes:** a StateCut is carried state at a declared boundary. The four cache planes (Source / Address / Operator / Renderer) are the roles.
  - **Operations:** mount, fork and swap load a per-input program onto a fixed native consumer that always runs.
  - **Mamba backend:** the VM exports and resumes Mamba state the same way.
  - **Why it is evidence:** the VM works because the scaffold is fixed and state is formed in time. Correct installs reproduce native behavior, while wrong-site, wrong-source and wrong-sign installs fail. "Ancestry changes meaning" (Prefill(A‖B) ≠ Mount(A,B), 6/6 vs 1/6) is a direct time-formation result.

## Paper spine: properties and their family coverage

| Property | Original passing evidence (from the outline, architectural paper, 10-01 posts and VM checklist) |
|---|---|
| **1. Reusable interfaces host different computations** (the scaffold recurs) | **FLUX:** format×ontology recurrence, same-organization profiles 0.913 vs different 0.734; the late image seam among the strongest in 8/9 families. **Eyes:** color/geometry share consumer heads but use different source rows. **Qwen:** one fixed L22–27 interface serves color 16/16, position 12/16, identity 11/11. **Mamba:** one shared history serves identity and capital. **SDXL:** depth/segment profile recurs on an unseen factor family. |
| **2. Context and operation select the participation** (space circuit) | **Same patch, different query:** 16/16 + 16/16 (3.130 / 0.583 nats). **Mamba:** identity vs capital on byte-identical history. **Readers:** operation-specific reader weights; per-item reader cosine within an operation 0.73–0.99 vs across operations 0.20 (relational addendum; valid per audit). **Eyes:** source coalition rows differ per attribute. **Conjunctions:** need an interaction field with consumer-visible authority. |
| **3. State is formed over ordered execution and carried forward** (time) | **E20 source→recipient-formed store:** block 0.924, rescue 0.871, wrong-identity 37/42. It replicates on Gemma, SmolLM2, held-out Qwen, and **Qwen2.5-7B** (rescue 0.770, wrong −0.026). **Recipient formation:** rescue 16/16, block 14/14; Python return value and copying. **Full-sweep asymmetry:** necessity spreads across a band while the write port is concentrated. **FLUX:** path-distributed four-quadrant certificate. **Temporal closure:** program 0.712, register 0.403, both together exact. **Chair transport.** **Mamba transition composition:** 3/3 vs endpoint-sum 0, staged execution exact. **Mamba L0→L18–20:** donkey/Vienna (+4.59/+7.65 nats; restoring the selected state removes 90–92% of the effect). **Ancestry:** 6/6 vs 1/6. |
| **4. Newly written state changes later reads** (the loop) | **Two-update** France→Germany with the visible token fixed. **Route→write→future:** key-only transfer exact; L23–27 closure on 3 fresh held contexts. **History×row** 4-cell decomposition: history +1.28–1.58, row opposing, on 4 held contexts. **Mamba:** S2 closure exact; fresh CPU dog/cat (+2.74). **SDXL:** writer→successor→later writer; a stale writer matches its immediate output but diverges later. |
| **5. The scaffold predicts held behavior** | **Frozen 24-coordinate relation profile:** 8/8. **Mamba 27-coordinate profile:** capital 8/8, identity 4/4. **Cross-family:** a partial state/consumer core, with its nulls. |
| **6. It lives in trained weights** | **v_proj** row permutation collapses the profile. **C8** controlled native learning. **Pythia** developmental trajectory. **C6** acquisition. |
| **7. The VM is the architecture made executable** | **Scene compiler:** 21/21 across 7 specimens (3 SDXL-family) / 5 diffusion families, with wrong-source/sign controls (FLUX.2 wrong-source 54.5–94.3, wrong-sign 60.0–89.3 MAE). **Compiled XOR program:** 148/150 vs native 0/150; an inverted XNOR binary executes XNOR on 74/75 and matches XOR on only 1/75 and 0/75 (a custody control: XOR is computed by the installed program, not in-model). **Frozen-site install:** 1.011 vs wrong site −0.133. **Page-out:** 0/96 checkpoint reads. **Archive:** 4/4 vs 0/4. **Exact fork/replay/export:** Qwen and Mamba. **Shared ancestry with private futures.** |

## What tonight's (2026-10-02) checks are, relative to this architecture

- **Aligned, promote into property 3:**
  - E20 cross-family and Qwen 7B;
  - identity-clustered CIs.
- **Aligned, use in property 2:** the relational addendum's per-item reader cosine.
- **Misaligned, appendix "additional checks" with caveats, or drop:** these test a proxy (a single commit-layer index, or a lexical-set "fact" variance ratio), an incompetent null, an inference-mask swap, or an inert dose. None of them tests the role graph:
  - the site-variance decomposition and its FAL-1/FAL-3 locators;
  - the confirm-color retest;
  - the commit-location SD at 7B;
  - the random/shuffled nulls;
  - the sliding-window type swap;
  - the function vector;
  - the pre-band subject freeze;
  - the Mamba A-only clock-dose.
- **Mamba commit = write, not retention (resolved by the aligned retest):** the clock-outlier correlation stands as a measured correlate (writer survival 0.63–0.90 vs the network median), but the preregistered clock retest (γ=15–142, forcing the writer's survival to the median) shows the commit lowers to the writer W, not to retention — releasing retention hurts in 0/6 cells, dt acts via the write in 6/6 and via retention in 0/6, and the prereg's own discriminator that retention beats a matched write went 4/6 only as a near-tie (≤0.07 nats). Verdict: RETENTION_NOT_COMMIT_LEVER; the write is the lever.

## Honest limits to keep

- The complete common graph across families is a null. The connected forecast ties an additive rival.
- Competence limits; addresses supplied by the host; single seed; the historical causal-mask defect; scene compiler results are parity results (reproducing native mistakes too).
- Learned-vs-architectural is separate from fixed-and-shared.
- Retractions:
  - E5 Mamba certificate;
  - Qwen3-30B in-forward confound;
  - "deletion leaves the target";
  - the oracle-assisted 10^8 headline.

## Scene generator: the working proof (author directive, 2026-10-02)

The scene generator is the architecture written as a program. The prompt is compiled once into a static source S: paired K/V at every cross-attention site plus pooled conditioning. The fixed interpreter Φ consumes S against the live carried image state s_k, so that s_{k+1} = Φ(s_k, S), and the renderer is the consumer, I = R(s_T). Mapped onto the architecture's roles:
- source = S
- live reader = the queries derived from the evolving residual
- writer = Φ updating the latent
- carried state = s_k (latent plus scheduler history)
- consumer = R (VAE / RGB)

Feature it as a centerpiece with image examples, not as an appendix line. Source: research/demos/docs/scene-generator-paper.md, research/demos/scene-generator.md, research/demos/scene-editing.md, research/demos/flux-relations-and-transport.md.

**Exact-execution results**
- **Exact closure:** the SDXL compiled source reproduces the native image byte-for-byte on 3 previously unused prompts. It reproduces 21/21 native RGB endpoints across 7 specimens and 5 families (three SDXL-family specimens, FLUX.1, FLUX.2, Chroma, and Krea2), with 0 model loads.
- **Controls at the same site:**
  - a wrong source renders the *other prompt's* scene;
  - a wrong sign renders blank grey;
  - FLUX.2 MAE (flux2-klein.json, 3 prompts): wrong-source 54.5–94.3, wrong-sign 60.0–89.3, permuted rows 4.6–22.8, complete 0.0;
  - SDXL: wrong-sign 94.29.
- **Address vs payload (SDXL Q×K×V factorial):**
  - K selects where and V supplies what: k-only permutation α 0.436, v-only permutation 0.627, wrong-K 0.358, wrong-V 0.413, joint-row permutation 0.859, compiled 1.000;
  - the K×V interaction is Δα 0.3413.
- **Static bus, dynamic query:** K/V are byte-identical across scheduler calls, while edited-vs-base query cosine falls from 0.9999 (call 0) to 0.8399 (call 14): the address diverges with the carried state. This is the scaffold/dynamic split in one measurement.

**Time on the scaffold (scene editing)**
- **Install timing decides the edit:**
  - early install changes composition and framing;
  - late install changes iris color while keeping composition;
  - eye geometry responds to early install;
  - 12 native references are reproduced across 56 images.
- **Same consumer, different source:** eye color and geometry reuse 5–7 of the top 8 consumer heads, but their source rows share only 10–15 of 64.
- **Temporal closure:** current program alone 0.712, carried register alone 0.403, both together exact. Program and history must agree.
- **Conjunctions:** they need an interaction field whose sign, dose and address change the output, and the dose response repeats across seeds.
- **Chair transport:** a spatial conjunction across the early steps moves the chair; writing at the destination alone duplicates it, and writing at the source alone reinforces it.

**Engineering consequence:** caching prompt-static projections cuts the median forward time from 33.895 s to 28.407 s with RGB exact.

**Figures to use (copy into figures/)**
- research/demos/artifacts/scene-generator/artifacts/images/cross-model/flux2-scene-compiler-proof-sheet.png (compiled = native; wrong-source / wrong-sign / row-permutation)
- research/demos/artifacts/scene-generator/artifacts/images/binding/analysis/k-address-v-payload-proof-sheet.png (K address, V payload)
- obsidian/images/2026-10-01-stable-scaffold-eye-color.png and 2026-10-01-stable-scaffold-eye-geometry.png (install timing on the time axis)
- obsidian/images/2026-09-19-chair-transport-spatiotemporal-conjunction.png
- Optional: other cross-model proof sheets (sdxl, chroma, krea2, flux1, illustrious-xl) as a montage

**Limits to keep:**
- The 21/21 result is replay parity, not semantic task success: the native references sometimes miss the requested subjects.
- Results are donor/prompt-derived; there is no donor-free payload compiler, no instance binding, and no shared tensor binary across families.
- Each family has its own lowering of the roles.
