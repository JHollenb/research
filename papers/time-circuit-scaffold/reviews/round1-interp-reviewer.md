# Round 1 — Interpretability reviewer (hostile but fair)

Paper: *The Time Circuit Is the Scaffold* (Hollenbeck, 2026-10-02). Read in full with
companion Paper 1 and all 7 figures opened; one record set (`site-variance-decomposition`
FINDINGS/PREREG) spot-checked.

## Summary verdict
A clean, candid paper with one genuinely useful reframing and one over-sold headline
number. The within-model results (same-patch/different-query, per-fact commit invariance,
frozen-reader transfer, Gemma sliding-window commit) are real and mostly well-controlled.
The central variance-decomposition statistic is not, as presented, evidence of a *learned*
scaffold, and the "decisive preregistered test" conflates a prospective run with a
retrospective re-analysis. The honest-null section (§9) and the instrument-defect
disclosure (line 165) are exemplary.

## 1. Thesis clarity / novelty
The thesis is clear and operationalized (fixed schedule = coord/band location; per-input =
op weighting + row selection). Falsifiable in principle. **But it is mostly a unification
of known results, and the paper undersells how close.** "Scaffold" ≈ Geva 2023
enrich→propagate→extract + Meng 2022 mid-layer band + Agarwal 2026 deferred commitment.
"Operation re-weights a recurring reader" ≈ Todd 2023 function vectors (reusable operation
carrier read at a late site). "Fact selects the row" ≈ Feng & Steinhardt binding IDs /
basic query-driven attention. The same-patch/different-query result (Fig 3), the cleanest
in the paper, is essentially "attention weights a stored row more when the query points at
it" — expected. **Genuinely new:** (a) quantifying the split as a *variance decomposition*;
(b) per-fresh-fact commit-layer SD (0.00 Gemma / 1.16 Qwen) as a crisp invariance metric;
(c) the Gemma sliding-window-only commit; (d) cross-architecture breadth. (a) is the
headline and is the weakest (see §2). The paper should state the Geva+Todd+Feng mapping
explicitly in §1 and claim the delta, not the frame.

## 2. Variance-decomposition methodology — the core problem
- **Unit/design:** cell = (24 coord × 3 op × 2 lex × 2 template × 2 order × 2 binding) =
  1,152, response = signed reader-profile value. Crossed and balanced. Good.
- **"coord main effect = scaffold" is not a fair interpretation (lines 19, 91, 171,
  abstract).** The coordinate main effect — different coordinates have different average
  causal magnitude — is trivially large in *any* structured function, including an
  untrained net. 42.2% measures that triviality, not a learned schedule. The *defensible*
  claim is the interaction ratio coord×op : coord×fact = 29.0 : 1.1 (≈26×). Drop 42.2% as
  "the scaffold's share," or justify it against a null.
- **No null model.** The §6 v_proj permutation tests *profile transfer*, not the *split*.
  Propose: rerun the identical decomposition on (i) randomly-initialized Qwen2.5-1.5B, (ii)
  weight-shuffled, (iii) (ideal) scrambled-data-trained. Prediction under the thesis: coord
  main effect stays ~large everywhere (confirming it's trivial), but coord×op carries
  structured, held-out-predictive variance *only* in the trained model. Without this the
  42.2% number should be cut.
- **Effective n / power.** Facts enter as only 2 bindings + 2 lexical sets (1 df each) —
  very low power to *find* a fact effect, so "fact = 1.1%" is partly a design artifact, not
  only a finding. Contexts are correlated replications (stated honestly at 111, 163).
- **Provenance conflation (lines 91 vs 101 — important).** FINDINGS confirms the headline
  42.2/29.0/1.1 split is a **Phase-1 re-analysis of pre-existing `qwen-predictive` data**
  (ops incl. relation), while the **preregistered prospective Phase-2 run used ops
  {identity, color, shape} — all read-back** — which line 101 admits cannot separate op
  from fact on the read side. So the abstract's signature number is retrospective and from
  a different op set than the preregistered run; the prospective/frozen contribution is the
  per-fact band location, not the read-split. The paper markets both as "the decisive
  preregistered test." Separate them explicitly.
- **Falsifier power.** Thresholds are loose (band move >4 layers in a 28-layer model when
  SD≈1; "per-fact reader varies as much as per-op" when the prospective ops are read-back
  so per-op variation is itself suppressed). Low power to trigger = weak prereg. And one
  falsifier *did* fire: Qwen-color SD 4.17 > 4.0 (Fig 5 F2C), explained post hoc as "2
  weak-signal facts." Admissible only if those facts failed the *preregistered* admission
  margin; if admitted, the falsifier triggered and must be reported as such.

## 3. Sliding-window commit (line 55)
Interesting but **not shown to be architecture-causal.** In Gemma-2 sliding/global layers
strictly alternate, so "commits only on sliding layers" is perfectly confounded with
depth/layer parity. Single seed, n 8–42. Settling controls: (a) a model with a *different*
local:global ratio (Gemma-3 is 5:1) — if commit still avoids global layers under 5:1, the
parity confound breaks; (b) the clean causal test: force a global layer's attention to
local windowing (or vice-versa) and see whether commit authority moves with the *type*, not
the index. As written this is correlational-with-parity.

## 4. Over/under-claims (line numbers)
- 19/171/abstract: 42.2% "scaffold" — overclaim (see §2).
- 55: "architecture's layer typing predicts where the commit lands" — parity-confounded.
- 91 vs 101: provenance conflation of prereg vs re-analysis.
- 119/173/123: "The same organization appears in a state-space and a diffusion model" —
  underpowered. Mamba is 12 rows, single seed; the diffusion "21/21 byte-exact" is a
  transplant round-trip identity (close to Hertz 2022 prompt-to-prompt), not evidence of a
  shared *schedule*. Soften to "consistent with."
- 31/155: "tools blind to the scaffold / native cut flips 83%" is the companion's single
  transcoder set on one model; keep the companion's own hedge.
- **Underclaims / credit:** §9 honest null (ties additive baseline to the digit, wins 1/3)
  and §11 instrument-defect disclosure are model scientific hygiene. Keep prominent.
- Honest-null adequacy: good, but extend it — null-test the *within-model split* (§2),
  not only the cross-family graph.

## 5. Clarity / figures
- Internal label mismatch: figures are titled F1/F2/F3 (decisive-test IDs) but cited as
  Fig 2/5/4 — reconcile.
- **Fig 5 caption (line 93) describes two panels; the PNG has three** (F2C write-SD is
  undocumented in the caption). And F2B shows a **10.4% residual** bar absent from text
  (line 95). Fix both.
- Fig 1: the "ordered execution → depth/denoising/recurrent" line overlaps the boxes/arrows.
- Fig 3: "0.583 nats" label collides with the error-bar cap (minor).
- Otherwise figures are legible and honestly annotated (Fig 6 correlated-context note is good).

## 6. Score & disposition
- **Score: 5/10.** Solid, honest, incrementally novel; headline stat over-interpreted.
- ICLR/NeurIPS main: **reject** as-is (central number needs a null; sliding-window needs a
  causal control; prereg/re-analysis conflation). Borderline-accept if §2 null + §3 control
  land.
- Interp workshop (BlackboxNLP / MI): **accept** — the reframing, honest nulls, and
  cross-arch breadth are workshop-valuable.
- Would my team read/cite? **Yes, read; cite the per-fact commit-invariance metric and the
  honest-null methodology.** Not the 42.2% figure.

## 7. Six ranked changes
1. Replace "coord main effect = scaffold (42.2%)" with the coord×op:coord×fact ratio +
   an untrained/shuffled-net null for the split (§2).
2. Add the sliding-window *causal* control (different local:global ratio, or swap attention
   type within the band) (§3).
3. Disentangle prereg prospective (band location) from retrospective re-analysis (read
   split) in §5; re-caption "decisive preregistered test" accordingly.
4. Report the Qwen-color SD-4.17 falsifier firing explicitly; state whether the excluded
   facts failed the preregistered margin.
5. Power up the fact factor (>2 bindings, >2 lexical sets) or state the 1.1% is power-
   limited, not a null fact effect.
6. Fix Fig 5 caption/panel/residual mismatches and the F-label↔Fig-number inconsistency;
   add the Geva/Todd/Feng mapping to §1.

## Three experiments that would most change my mind (~10 min, ≤9B; paged 7B+ available)
A. **Untrained-net null for the split.** Same 1,152-cell decomposition on randomly-init
   and weight-shuffled Qwen2.5-1.5B. If coord main effect stays ~40% and coord×op does
   *not* predict held contexts there, the trained-vs-random contrast *makes* the scaffold
   claim. This is the single most decisive missing control.
B. **Sliding-window causality.** Within Gemma's band, force one global layer to local
   windowing (and one local to global) and re-measure commit authority. If authority tracks
   attention *type* not index, the architecture claim is earned; if it tracks index, it's
   parity.
C. **Function-vector equivalence test.** Extract a Todd-style op vector for identity vs
   relation and test whether adding it reproduces the "operation re-weights the reader"
   effect (cosine shift L23.KV0 vs L22.KV1). If the FV already explains the op split, the
   "space circuit" is function vectors under a new name — and the paper should say so; if it
   doesn't, that's a concrete novelty claim. A 7B paged replication of the per-fact commit
   SD would separately address the single-seed/small-model scope.
