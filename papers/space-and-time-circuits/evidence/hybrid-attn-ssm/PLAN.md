# E14 — Hybrid attention + SSM, full per-layer sweep (paper §6.4 optional TODO)

Status: preregistered 2026-10-01 BEFORE first submit. Lead: paper "A New Class of
Circuits: Space and Time", §6.4 TODO [E14].

## Question
In a model whose every layer runs attention AND a Mamba2 SSM **in parallel**
(Falcon-H1-0.5B-Base), does the **attention key/value cut** behave like the fully
swept transformer cells — a path-distributed store needing a multi-layer late band,
with low single-layer necessity — while the **SSM state cut** behaves like Mamba —
one late "writer" layer that carries most of the store? Or do the two paths share a
single commit?

The certificate is a statement about a **cut**, not an architecture (§2.3 rule 1,
§6.4). Here one model exposes two cuts in the same layers, so we can read both.

## Specimen
- Model: `tiiuae/Falcon-H1-0.5B-Base` (local: `/mnt/big/llm-models/Falcon-H1-0.5B-Base`).
- 36 layers; every layer = parallel `self_attn` (GQA 8 heads / 2 KV, head_dim 64,
  key_multiplier, out-scaled) + `mamba` Mamba2 mixer (d_ssm 1536, d_state 128,
  n_heads 24, d_head 64, d_conv 4, n_groups 1), summed with per-path multipliers,
  then residual + MLP (`attn_layer_indices: null` ⇒ no attention-only or SSM-only
  layers; the hybrid is uniform). transformers 5.14.1 (job env), fp32, eager attn,
  tf32 off, seed 0.
- Cache (unified `DynamicCache(config)`): per layer `.keys/.values` (attention) and
  `.conv_states[0]/.recurrent_states[0]` (Mamba). Attention written by
  `past_key_values.update`; Mamba by `update_conv_state`/`update_recurrent_state`.

## Panel and admission (same as the transformer panel, §6.1)
- Behaviors: `identity` (14 animal subjects × 3 contexts, filler "creature") and
  `color` (10 colors × 3 contexts, filler "plain"), from the published
  `run_sae_comparison.build_items`. Reused verbatim: `answer_logprobs`,
  `bootstrap_median_ci`, `bootstrap_rate_ci`, `_fractions`, `_flips`, `_norm_gain`.
- Subject position found by the single-token diff of clean vs filler prompt (rows
  where tokenization is inconsistent are dropped).
- Admission: clean top-1 among candidates == answer AND (clean_lp − filler_lp) ≥ 1.0.

## Cuts and the isolated-swap protocol (§2.3 rule 2, rule 6)
Prefix = tokens through the subject (`[:subj+1]`); suffix = the rest (identical
across subjects). Capture clean (B rows) and filler (1 row) donor stores by
prefilling the prefix. Every arm RE-prefills the clean (necessity) or filler (write)
prefix into a fresh cache, patches the named cut, and **replays the suffix
token-by-token** (single-token decode path — the exact, deterministic path validated
in the Mamba sweep worker; it advances both the attention cache and the SSM state).
Score at the native consumer's last-position logits.

- **Attention K/V cut at layers S:** overwrite `keys/values[:,:,subj,:]` at each L∈S
  with the donor's (necessity: filler's; write: the row's clean subject's).
- **SSM state cut at layers S:** overwrite `conv_states[0]` and `recurrent_states[0]`
  at each L∈S with the donor's.

## Arms (four quadrants + windows), per behavior, aggregated over contexts
1. **Single-site necessity** (isolated, per layer L = 0..35): attention-only cut;
   SSM-only cut. Fraction = per-row Δlp divided by that subsystem's whole-path Δlp
   (attention-single ÷ attention-all; SSM-single ÷ SSM-all), median + 95% bootstrap
   CI; plus top-1 flip rate and raw median Δlp.
2. **Whole-path necessity:** attention-all, SSM-all, BOTH-all (attention+SSM at every
   layer). Raw median Δlp and flip rate (does the behavior die?). First/second half of
   each path as context.
3. **Single-site write sufficiency** (into the filler prompt, isolated, per L):
   attention-only; SSM-only. Normalized gain = gain ÷ (clean_lp − filler_lp).
4. **Whole-path write:** attention-all, SSM-all, BOTH-all.
5. **Window necessity (attention path, E19):** every contiguous window of width
   2/3/4/6 (and its complement), fraction ÷ attention-all, best window per width.
   (SSM windows added only if the smoke shows budget.)

## Exact no-op gates (hard; §2.2, §3)
- **Split no-op:** prefix→suffix replay with NO overwrite reproduces the clean
  full-forward last logits. Report `split_noop_max = max|·|`. Target ≤ 1e-3 (the
  Mamba state cut reports ≤ 2.5e-4 batch noise; transformer K/V ≤ 4e-5). If the SSM
  path's split no-op is larger than this under token-replay, the result is reported
  with that caveat.
- **Attention write no-op** and **SSM write no-op:** overwriting the filler's store
  with the filler's own store (source="filler") at layer 0 ⇒ gain ≈ 0.
- **Capability:** median admitted (clean_lp − filler_lp) and clean top-1 == answer.
- **Floor separation:** admission enforces the ≥ 1.0 drop.

## Predictions (stated in advance)
- **P1 (attention ≈ transformer band).** Best single attention-layer necessity share
  (÷ attention-all) is small (expect ≤ ~0.35, and ≤ ~0.08 if a clean cell exists);
  the attention path needs a multi-layer late band (best 3-adjacent window < ~0.8 for
  a necessity-clean behavior; ≥ 4–8 layers to reach 0.8), with the band late (≥ ~0.6
  of depth). I.e. attention looks path-distributed like §6.1/§6.1b.
- **P2 (SSM ≈ single writer).** One SSM layer at ~0.6–0.85 relative depth carries a
  large share (≥ ~0.4) of SSM-all necessity AND ≥ ~0.4 of SSM write sufficiency —
  concentrated, like all three Mamba models (§6.4).
- **P3 (shared vs separate commit).** Either the attention late band and the SSM
  writer sit at the SAME late depth (one commit, two cuts) or they are separated.
  Reported, not predicted.
- **Falsifiers / alternative outcomes (all acceptable, reported honestly):** both
  paths concentrate (hybrid is Mamba-like at both cuts); both distribute; one
  subsystem carries ≈ the entire store and the other ≈ 0 (parallel paths are not
  co-equal); no powered cell (admission too small). A failed gate ⇒ "not
  established", never "absent".

## Protocol
Smoke (3 subjects, 1 context, both behaviors; logs cache-attribute introspection and
per-phase timing) → inspect that the stores/gates are the expected data and size the
full run to ≤ ~10 min GPU → ONE full single-seed run. priority=100. VRAM reserve
right-sized to measured peak × 1.3 after smoke. No git commit; no paper.md edits.

## Method provenance (no external numeric canary — new model)
The attention K/V isolated cut is the operator validated in E17/E19 on transformers;
the SSM state cut (conv + recurrent swap, per layer, suffix token-replay) is the
operator validated in the Mamba E3b full-layer sweep and writer-clock workers. The
split no-op and write no-op gates are the internal exactness checks.

## Execution note (added after smoke, predictions unchanged)
Two smokes (n=3) validated the pipeline on `job-16b3e85a29fd` (token replay) and
`job-65df01884d67` (chunk replay):
- Cache layer = `LinearAttentionAndFullAttentionLayer`; shapes keys [B,2,13,64],
  conv [B,1792,4], rec [B,24,64,128]; Mamba runs the deterministic naive torch path
  (fast CUDA kernels absent).
- Exact gates PASS: split no-op 2.3e-5 (chunk) / 5.9e-5 (token); write no-ops ≤ 5e-6.
  Chunk and token give identical arm numbers to ~5 decimals, so the single multi-token
  suffix forward (chunk) is exact and ~3x faster. The full run uses `suffix_mode=chunk`
  and reports BOTH the chunk gate (the one the arms rely on) and the token reference.
- To fit the ~10-min budget on the naive Mamba path, the full run uses
  `max_contexts=2` (identity n≈28, color n≈20 — comparable to the published SmolLM2
  color n=27 cell) and runs the attention window sweep for `identity` only (the
  stronger behavior). All four-quadrant arms at both cuts run for BOTH behaviors.
Full run: `--windows --window-behaviors identity --suffix-mode chunk --max-contexts 2`,
VRAM 5000 / RAM 6000 MB (smoke peaks 3.3 GB / 3.7 GB x1.3), priority 100.
