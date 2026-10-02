# Rebuild notes — Paper 2 (time-circuit-scaffold), 2026-10-02

What changed in the rebuild from commit fb2c343, and why. The coordinator's architecture
brief, math doc, and mid-task directives override the earlier structure where they conflict.

## 1. Thesis and framing

- **Old spine:** "The commit layer does not move: an input-invariant time scaffold hosts
  per-input circuits in small transformers." The paper was organized around one preregistered
  commit-invariance test plus a variance split, with appendix one-liners.
- **New spine:** "Dynamic circuits loop through a stable time scaffold." The scaffold is a
  reusable organization of causal ROLES (source, reader/transition, writer, carried state,
  consumer), identified by intervening on recurring roles — NOT a commit-layer index. Built
  over ordered execution (denoising steps / depth+positions / recurrent transitions). The body
  is one section per property, seven properties, each replicated across diffusion, AR
  transformer, and SSM, from the ~50 original passing experiments and the model virtual machine.
- Title drops "in Small Transformers"; subtitle names the breadth (transformers 70M–7B, SSM,
  hybrid, five diffusion families).
- Formal definition section (§2) now follows the math doc §1.3: scaffold = a fixed lowering +
  alignment with high interchange-intervention accuracy; dynamic circuit = active edge set +
  realized values. "Static" = fixed alignment, not fixed layer index. Coordinates are not unique.
- Functional form a_t/w_t/z_{t+1}/y_t and the Mamba channel recurrence added to §2.

## 2. Promotions (aligned, into the spine)

- **E20 cross-family + 7B** promoted into Property 3 (source→store over ordered execution):
  Gemma 0.768/0.985, SmolLM2 0.740/0.910, held-out Qwen 0.728/0.713, and Qwen2.5-7B
  rescue 0.770 / block 0.595 / wrong −0.026 (block lower at 7B because the commit leaks past a
  6-layer mediator; rescue unaffected). Source: `2026-10-02-e20-cross-family`,
  `2026-10-02-scale-9b-scaffold` (final E20 now in `results/e20_analysis_with_7b.json`).
- **Relational per-item reader cosine** used in Property 2 as the robust statistic (within-op
  0.73–0.99 vs across-op 0.204/0.218).
- **Scene generator** is now a centerpiece (Property 7 + §1 teaser figure + Property 2
  K-address/V-payload + Property 3 install timing), with the equation mapping
  s_{k+1}=Φ(s_k,S), I=R(s_T) onto the roles. Figures copied into `figures/`:
  fig_scene_compiler_flux2, fig_k_address_v_payload, fig_eye_color_timing,
  fig_eye_geometry_timing, fig_chair_transport.
- **Model virtual machine** framed as "the architecture made executable" (Property 7): swap
  success = interchange-intervention accuracy; ancestry 6/6 vs 1/6 is a time-formation result.

## 3. New aligned results integrated (from the math doc)

- **Formation over time (§3.2 of math doc)** → Property 3. Prereg-frozen (Qwen
  job-eaf503028c04, Gemma job-9acb76a12273). Best single band layer 0.732/0.804 (store
  distributed); freezing the band's attn+MLP leaves rescue intact 0.904/1.023 (content present
  at band entry; band projections commit it); cutting consumer→subject collapses rescue
  0.871→0.010 and 0.985→0.015; pre-band L13–21 freeze cuts Qwen to 0.675. Phrased as: the late
  band is the commit/read-out zone, formed over the preceding depth. This REPLACES the
  `<!-- TODO formation-over-time -->` placeholder.
- **Attention identities (§4 of math doc)** → Property 2. K is address, V is payload; interaction
  = α_s(1−α_s)(E−1)/D·Δv, predicting the SDXL factorial (0.72139/0.66201/0.71808/1.0, Δ 0.3413).
  Joint-row-permutation invariance treated as an OPEN check (0.859 measured vs exact predicted;
  run fp64 before citing). Not overclaimed.
- **Mamba clock retest (§8 of math doc)** → Property 3 / §10. Prereg-frozen, γ = 15–142 dose
  (`2026-10-02-mamba-clock-retest`): verdict RETENTION_NOT_COMMIT_LEVER (release hurts 0/6,
  dt via retention 0/6 / via write 6/6, writer-specific 1/6). The commit lowers to the writer W;
  retention is a correlate (survival 0.66–0.90). The earlier k∈{0.5,2} dose was inert by
  construction and is cited as evidence neither way. REPLACES `<!-- TODO mamba-clock-retest -->`.

## 4. Demotions (misaligned proxies → §13 "Additional checks and their limits" + Appendix D)

Per the math doc §9, these test a proxy (a single commit-layer index, a lexical-set fact-variance
ratio, an incompetent null, an inference-mask swap, an inert dose) rather than the role graph, and
several do not discriminate the thesis from its alternative. They are reported with their limits,
NOT as spine:

- site-variance decomposition and its FAL-1/FAL-3 locators;
- the confirm-color retest;
- the commit-location SD (incl. 7B SD 2.30): argmax of a flat ~6-layer plateau has SD≈1.7 by
  construction, and a scaffold-free account predicts a large spread too; trained 1.16/1.60 vs
  incompetent null 8.56/7.28 and 10.03/10.22 shows learned-not-generic, bounded by incompetence;
- random/shuffled nulls (behaviorally dead, top-1 0/96);
- the sliding-window type swap (exact no-op at seq 17: swaps only the inference mask);
- the function vector (unit-coefficient, all-head weak negative);
- the pre-band subject freeze (could not see band-internal/cross-position formation);
- the A-only clock dose (inert by construction; superseded by the aligned retest).
- A discriminating-alternatives table was added to §13 (math doc §9.2).

## 5. Validity corrections applied (from the two validity audits)

- (a) Dropped the "op beats fact 11×/19×" variance-ratio headline. Lead with the per-item reader
  cosine. Clean 20-country ratio reported plainly: 2.65 (Qwen), 0.72 (Gemma, FAL-2a fired). The
  circular "denoised" cosine is not used as a rebuttal.
- (b) FAL-3 frozen argmax disclosed as a locator artifact (locates the plateau, not the commit);
  the silent FAL-1 locator swap (argmax-necessity → late-half argmin) disclosed; confirm retest
  re-froze all three prospectively; Qwen fell short at 27 colors (frozen ≥40) — disclosed.
- (c) Sliding-window type swap: removed "tracks depth not type"; states it swaps only the
  inference mask (weights trained as sliding/global) and the question is untested at short context.
- (d) Commit-location fixedness presented as consistent with Geva/Meng/Lad, NOT the discriminating
  test (now a weak symptom / Appendix D); null numbers reported with the incompetence bound.
- (e) Formation "built over time": removed the "construction unsupported" reading; the correct
  band-internal test has now run (§3 above) and refines the band to the commit zone.
- (f) Mamba clock: do NOT say "clock not causal"/"stops its clock refuted" from the old dose; the
  aligned retest (§3 above) resolves it as RETENTION_NOT_COMMIT_LEVER (write is the lever).
- (g) Null nets incompetent (0/96) → show learned, not scaffold-vs-any-competent-net; A-P4 random-init
  +0.350 kept disclosed as a failed prediction.
- (h) Function vectors reported as a weak negative (unit coefficient, all heads).
- (i) 7B numbers used as corrected (commit L21 rel 0.778, all 40 in L19–27, single-argmax SD 2.30
  the wrong yardstick for a redundant band; E20 rescue 0.770 / block 0.595 / wrong −0.026).
- (j) Retractions kept disclosed (E5 Mamba cert; 30B MoE negative; "deletion leaves target"
  corrected; oracle efficiency headline; SmolLM2 label). Paper 4's CoT E2 state swap is one
  paragraph in Property 4, scoped as injected; the E1 hidden-channel reading is noted as demoted.
- Formation 16/16 / 14/14 re-attributed to `qwen-scaffold-context-poc/FINDINGS.md:62` (L12 seed);
  `qwen-formation-replay` supplies the Python/copy generality.

## 6. Figures

- Reused valid: fig1 (schematic), fig2 (→ Appendix D1), fig3 (same-patch), fig4 (reader cosine),
  fig6 (confirmation), fig7 (null), fig9 (controls), figA/figB/figC (→ Appendix D reviewer controls).
- Added (copied from primary artifacts): fig_scene_compiler_flux2, fig_k_address_v_payload,
  fig_eye_color_timing, fig_eye_geometry_timing, fig_chair_transport.
- Removed from body: fig5_variance_decomposition — its variance-ratio panel is invalid under
  correction (a) and should be regenerated (per-item cosine + clean 2.65/0.72 ratio) if used at all.
  fig8 superseded as teaser by fig_scene_compiler_flux2.

## 7. Rules honored

- Every number traces to a FINDINGS / results JSON / report (MEASURED); no blind-final-boss or grail
  tool outputs cited. Body free of lab jargon (Saturn/mrun/job IDs/E#); those confined to Appendix A.
- Obsidian style: no mid-sentence line breaks; one claim per paragraph. Length ~13.8k words + appendix.
- No commit (the coordinator commits). No other papers or experiment dirs edited.

## 8. Still open / flagged for the coordinator

- fig5 regeneration (or permanent removal) is a figure task not done here.
- The competent non-scaffold network control (for the learned claim) and a same-assay authentic
  checkpoint trajectory (to date acquisition) remain open; noted in §12.
- Joint-row-permutation exact-invariance is an open fp64 check (§4); 0.859 cited only as near-invariant.
- Several freezes are evidenced by file mtime only (no hash); disclosed in §C and the custody audit.
