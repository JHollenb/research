# Round-1 response

Point-by-point reply to the three round-1 reviews. "Done" = fixed in this revision of
`paper.md`/`README.md`/`figures/`. "Running" = experiment in progress, marked by a
placeholder in the text. "Out of scope" = cannot be done from this directory.

All numeric changes were re-verified against the cited source FINDINGS/JSON this round.

## Highest-priority honesty items (coordinator + all three reviewers)

| # | Point | Action | Location |
|---|---|---|---|
| H1 | "Three falsifiers, none triggered" is false: FAL-3 (`sd_argmax_write > 4`) was crossed by Qwen color (SD 4.17). | Done. State plainly that two held and FAL-3 fired; label the robust-statistic (≤2.06) and two-fact-exclusion readings post hoc; treat the cell as a crossed falsifier pending a preregistered re-run. | Abstract; §1 overview; §5 falsifier para; §13; Fig 5 caption (F2C shows the crossing) |
| H2 | Read-site split (42.2/29.0/1.1) is retrospective, not the preregistered prospective result. | Done. Separated: the per-fact commit location is the preregistered prospective measurement; the split is a retrospective re-analysis of pre-freeze data on an op set incl. relation. Section renamed. | Abstract; §1; §5 opening + both split paras; §5 header |
| H3 | "42.2% = scaffold's share" is not defensible without a null. | Done. Lead with the interaction ratio (coord×op 29.0% : fact-like 2.7% ≈ 11×); report fact-like = coord×fact 1.1% + coord×binding 1.6%; do not read 42.2% as the learned share; untrained/shuffled null running. | Abstract; §5; Fig 5 caption; `<!-- TODO P2-A null -->` |
| H4 | §3 Pythia window numbers misassigned; "fails immediately after" false for Pythia. | Done. Corrected to 0.95@L17, 0.48@L18, 0.01 by L22 (gradual); kept Qwen0.5B/Mamba as the sharp-edge exemplars. | §3 para 2 |
| H5 | Sliding-window commit is parity-confounded (Gemma-2 strictly alternates). | Done. State the parity confound; softened "predicts"→"coincides with"; type-switch causal test running. | §3 para 1; `<!-- TODO P2-B sliding causality -->` |
| H6 | State the function-vector / staged-inference mapping and claim the delta. | Done. Mapping to Geva/Lad (scaffold), Todd/Hendel (operation weighting), Feng & Steinhardt (row) in §1 with the delta (per-fact causal invariance + interaction split + cross-arch). FV-equivalence test running; XNOR hostile-inverse shows the installed object is a program, not a steering vector. | §1; §4; §10; `<!-- TODO P2-C function vectors -->` |

## Interpretability reviewer (5/10)

| Point | Action |
|---|---|
| §2 null model missing for the split | Running (`<!-- TODO P2-A null -->`); until it lands we claim only the ratio, not the 42.2%. |
| Fact factor low-powered (2 lex × 2 bindings) → 1.1% partly a design artifact | Done; stated in §5, and the per-fact band location is given as the direct fact-invariance test. |
| §3 sliding-window causal control | Running (`<!-- TODO P2-B sliding causality -->`). |
| §4 lead result "expected" (attention weights a queried row more) | Acknowledged in §1 mapping; the novelty claimed is the byte-identical same-parent isolation and the variance split, not the phenomenon. |
| Soften "same organization appears" in SSM/diffusion to "consistent with" | Done; §7 retitled and reworded, Table 1 added, abstract and §13 softened. |
| Fig 5 caption: 2 panels described but PNG has 3; residual 10.4% unstated | Done; caption now describes F2A/F2B/F2C, the 10.4% residual, op×fact 2.0%, and the FAL-3 crossing. |
| F-label (F1/F2/F3) vs Fig-number mismatch | Done; captions now name the decisive-test panels (F1, F3, F2A–F2C). |
| Fig 1 caption/box overlap; Fig 3 "0.583" occlusion | Done; both figures regenerated. |
| Experiment C (FV equivalence) | Running (`<!-- TODO P2-C function vectors -->`); §10 adds the XNOR hostile-inverse evidence that the installed object is not a steering vector. |

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

`<!-- TODO confirm-color -->` (§5), `<!-- TODO P2-A null -->` (§5),
`<!-- TODO P2-B sliding causality -->` (§3), `<!-- TODO P2-C function vectors -->` (§4),
`<!-- TODO addendum: relational op -->` (§5).
