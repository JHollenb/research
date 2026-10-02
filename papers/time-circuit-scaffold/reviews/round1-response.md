# Round-1 response

Point-by-point reply to the three round-1 reviews. "Done" = fixed in this revision of
`paper.md`/`README.md`/`figures/`. "Running" = experiment in progress, marked by a
placeholder in the text. "Out of scope" = cannot be done from this directory.

All numeric changes were re-verified against the cited source FINDINGS/JSON this round.

## Highest-priority honesty items (coordinator + all three reviewers)

| # | Point | Action | Location |
|---|---|---|---|
| H1 | "Three falsifiers, none triggered" is false: the write-window falsifier fired. (Coordinator second correction: the frozen statistic is the SD of the per-item argmax write layer; it fired in 2 of 6 cells — Qwen color 5.45, Gemma identity 4.01 — and the earlier "4.17" is a post-hoc commit-locator SD, not the frozen statistic.) | Done. State that two held and the write-window falsifier fired as frozen in 2/6 cells; the frozen argmax locator tracks a noisy plateau; under a post-hoc commit locator the band is invariant in 5/6 cells; every per-fact SD is now labeled by locator; confirmatory run freezes all three locators. | Abstract; §1 overview; §3; §5 band + falsifier paras; §13; Fig 2 and Fig 5 captions; Appendix C |
| H2 | Read-site split (42.2/29.0/1.1) is retrospective, not the preregistered prospective result. | Done. Separated: the per-fact commit location is the preregistered prospective measurement; the split is a retrospective re-analysis of pre-freeze data on an op set incl. relation. Section renamed. | Abstract; §1; §5 opening + both split paras; §5 header |
| H3 | "42.2% = scaffold's share" is not defensible without a null. | Done. Lead with the interaction ratio (coord×op 29.0% : fact-like 2.7% ≈ 11×); report fact-like = coord×fact 1.1% + coord×binding 1.6%; do not read 42.2% as the learned share; untrained/shuffled null running. | Abstract; §5; Fig 5 caption; `<!-- TODO P2-A null -->` |
| H4 | §3 Pythia window numbers misassigned; "fails immediately after" false for Pythia. | Done. Corrected to 0.95@L17, 0.48@L18, 0.01 by L22 (gradual); kept Qwen0.5B/Mamba as the sharp-edge exemplars. | §3 para 2 |
| H5 | Sliding-window commit is parity-confounded (Gemma-2 strictly alternates). | **Landed** (§3, Figure B). The type-switch causal test ran: at 17-token prompts the sliding mask equals the full causal mask, so a type flip is an exact no-op (0.0 logit change; a real window-4 mask shifts logits 19.6), and the commit profile is byte-identical (positive L16/18/20/22, non-positive global L17/L21). Commit tracks depth/index, not attention type. Long-context untested (Gemma-3 unavailable). | §3 para 1; Figure B |
| H6 | State the function-vector / staged-inference mapping and claim the delta. | Done. Mapping to Geva/Lad (scaffold), Todd/Hendel (operation weighting), Feng & Steinhardt (row) in §1 with the delta (per-fact causal invariance + interaction split + cross-arch). FV-equivalence test running; XNOR hostile-inverse shows the installed object is a program, not a steering vector. | §1; §4; §10; `<!-- TODO P2-C function vectors -->` |

## Interpretability reviewer (5/10)

| Point | Action |
|---|---|
| §2 null model missing for the split | **Landed** (§5, Figure A). The null confirms the split is learned: coord→1.2–1.4%, op:fact 19.0→~1 in random/shuffled nets. The reviewer's A-P1 (coord-main trivial) failed; A-F3 fired. Bounded by null incompetence (top-1 0/96). |
| Fact factor low-powered (2 lex × 2 bindings) → 1.1% partly a design artifact | Done; stated in §5, and the per-fact band location is given as the direct fact-invariance test. |
| §3 sliding-window causal control | **Landed** (§3, Figure B). Type flip is an exact no-op (0.0) at our prompt lengths; commit profile byte-identical; tracks depth not attention type; long-context untested (Gemma-3 unavailable). |
| §4 lead result "expected" (attention weights a queried row more) | Acknowledged in §1 mapping; the novelty claimed is the byte-identical same-parent isolation and the variance split, not the phenomenon. |
| Soften "same organization appears" in SSM/diffusion to "consistent with" | Done; §7 retitled and reworded, Table 1 added, abstract and §13 softened. |
| Fig 5 caption: 2 panels described but PNG has 3; residual 10.4% unstated | Done; caption now describes F2A/F2B/F2C, the 10.4% residual, op×fact 2.0%, and notes F2C plots the commit-locator SDs while the frozen argmax falsifier (2/6 cells) is reported in §5. |
| F-label (F1/F2/F3) vs Fig-number mismatch | Done; captions now name the decisive-test panels (F1, F3, F2A–F2C). |
| Fig 1 caption/box overlap; Fig 3 "0.583" occlusion | Done; both figures regenerated. |
| Experiment C (FV equivalence) | **Landed** (§4, Figure C): additive op vector at L24 gives 0/14 flips, +2.19 nats, erases the identity route without building the relational one — NOT_FV. §10 XNOR adds that the installed object is not a steering vector. |

## Evidence audit

| Point | Action |
|---|---|
| "none triggered" overstated | Done (H1). |
| §3 Pythia window MISMATCH | Done (H4). |
| Split retrospective not prospective | Done (H2). |
| coord×binding 1.6% omitted (exceeds coord×fact) | Done; folded into the "fact-like 2.7%" term in abstract, §5, Fig 5, README. |
| Diffusion "57–97 MAE" unlocated | Resolved: it is in the cited survey blog (line 153: "diverged by 57–97 MAE"); kept, with the source noted in the README row and §10 record. |
| "32 same-parent query pairs" not verbatim | Done; restated as "16 same-parent contrasts per operation, 128 directional pairing checks." |
| Ref 2310.17191 (Feng & Steinhardt) absent from companion ref lists | Present in the sibling bridge draft; retained as verified prior art per coordinator. |
| 2026-dated arXiv IDs (2609.17537, 2606.15796) externally unverifiable | Flagged: these are inherited from the companion/space-time reference lists; they should be confirmed against the public record before camera-ready. |
| "well-powered cell" power threshold unstated | Done; §5 names the Qwen color cell (n=22, two sub-threshold facts) as the single underpowered one; identity (n=42) and Gemma color (n=25) are not. |
| Figures not re-rendered | fig1/fig3/fig7 regenerated this round; fig2/fig4/fig5/fig6 are the experiments' own plots and their caption numbers trace to the JSONs. |

## Prior-art / clarity

| Point | Action |
|---|---|
| Add Lad 2024, Chughtai 2024, Sharma 2024, Basu 2023, Nanda 2023, tuned lens (Belrose 2023), Gurnee 2024 | Done; all added with explicit deltas (Lad/Geva/Nanda/Belrose in §11 ¶1, Chughtai in §9, Sharma/Basu/Gurnee in §11 ¶4). |
| Cut §3 overlap with Paper 1 (identical window numbers, shared clock-dose jobs, Gemma sliding) | Done; §3 compressed ~40%, the sweeps now cited to the companion, only the per-fact SD kept as this paper's own. |
| Stale/asymmetric cross-refs; README line ~68 stale path | Done; companion link now `../time-formed-circuits/paper.md`; role-matcher evidence-map path repointed to the primary JSON (`ssm/results/e4-e1-e2-e3-alignment.json`). P1 linking back to P2 is out of scope (P1 not editable here). |
| §5 confound self-discounts the test | Done; the "all three ops are read-back" caveat is now below the results, labeled retrospective, and the relational addendum is described. |
| Thesis verbatim early + at close; gloss "space circuit"; disambiguate "scaffold" | Done; bold **Thesis** sentence at end of §1 ¶2 and restated at the close of §13; "space circuit" glossed on first use; "scaffold" disambiguated from prompt/CoT scaffolds. |
| Title | Done; changed to "The Commit Layer Does Not Move: A Fixed Time Scaffold Hosts Per-Input Circuits." |
| §8 (n=1/3) cut/fold | Done; compressed to a single bounded paragraph. |
| §9 tighten; §7 needs a figure | §9 kept (credibility) with the additive-null citation added; §7 now has Table 1 summarizing the three families in lieu of a figure. |
| "coordinate" undefined before §4 | Done; defined in §2 as (layer, key/value head, key-or-value), with "signed reader profile" glossed. |

## Added this round (coordinator directive)

- §10 "Constructive evidence: the fixed site is addressable" — the engineering converse:
  compiled programs/state installed at the fixed site run across new inputs through the native
  consumer, with matched negative controls failing (wrong-site write 1.011 vs −0.133; K/V 0.602
  vs −0.153, 14 held facts; wrong-source/sign diffusion 57–97 vs 0.0; hostile XNOR inverts
  148/150; absent/wrong page 0/4). Honest limits stated: mechanics-level not production;
  host-supplied addresses; donor-dependent scene payloads; shows the site is fixed and shared,
  not learned. Figures 8–9 added. All numbers verified at their cited paths; the stale E10
  15/32 and the withdrawn efficiency figures were not used.

## Running (placeholders in text)

Confirm-color (§5) has since landed in round 2 (see `round2-response.md`): the fresh-color retest
cleared FAL-3 under all three frozen locators in both families. No placeholders remain.

**Landed since round 1:**
- **P2-B sliding causality** (§3, Figure B): the Gemma-2 commit tracks depth, not attention type.
  At 17-token prompts the sliding-window mask equals the full causal mask, so a layer type flip is
  an exact no-op (0.0 logit change) while a real window-4 mask shifts logits 19.6; the per-layer
  commit profile is byte-identical under the swap (positive L16/18/20/22, non-positive global
  L17/L21). The alternation is confounded with layer parity, not caused by attention type;
  long-context untested (Gemma-3 unavailable). Source: `.../2026-10-02-p2-reviewer-experiments/
  results/B_analysis.json` (job-0b7652b2112d, Gemma-2-2B, 42 identity items, fp32 eager).
- **P2-A null** (§5, Figure A): the read-site split is learned — in random-init and weight-shuffled
  nets the coordinate main effect falls to 1.2–1.4% and the op:fact ratio from 19.0 to ~1 (v_proj
  permute keeps 11.9). The reviewer's "coord-main is trivial" hypothesis (A-P1) failed; A-F3 fired.
  A-P2/A-P3 passed; A-P4 passed in trained (0.997 vs 0.485) but failed for random_init (Δ+0.350),
  reported honestly, not as spurious. Bound stated: nulls incompetent (top-1 0/96) — shows learned,
  not scaffold-vs-any-competent-net. Disclosed: jackknife (not bootstrap) CI; frozen manifest
  re-sealed after results.
- **P2-C function vectors** (§4, Figure C): additive Todd-style op vector at L24 gives no top-1 flip
  (0/14), +2.19 nats relation, and erases the identity route without building the relational one —
  operation weighting is NOT_FV. Bounded negative (all-heads FV, fixed coefficient, extracted
  including held contexts, L24 top of grid).
- **Relational addendum** (§5, Table 1): capital-of on 40 fresh facts separates operation from fact
  prospectively (within-op per-item cosine 0.74–0.99; identity~capital 0.20–0.22; identity~color
  0.84–0.91). FAL-2b (cosine) not triggered; FAL-2a (sum-of-squares) fired for Gemma, reported as frozen.
