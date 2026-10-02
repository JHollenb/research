# Round 3 — Interpretability reviewer (hostile but fair)

Paper: *The Commit Layer Does Not Move* (Hollenbeck, 2026-10-02, round-2 revision).
Read in full; round2-*.md + round2-response.md read first; Fig 5 pixel-inspected; figure
mtimes and every housekeeping fix verified at the file level.

## Did the round-2 must-fixes land? (all verified, not taken on trust)

1. **Confirm-color, both halves** — landed. Abstract L19, §3 L63, §5 L99, §13 L204, AppxC L261,
   AppxA L225. Qwen S1 2.84/S2 1.44/S3 1.76 (48 items); Gemma S1 3.44/S2 0.90/S3 0.97 (106).
   No cell fires on any locator. Phase-2 Qwen-color firing does not reproduce. The invariance
   no longer rests on the post-hoc locator. This clears the round-2 #1 blocker.
2. **Fig 5 F2C regenerated** — confirmed (mtime 05:24 > response 05:20). Pixel-inspected:
   now plots frozen argmax S1 + commit S2 per cell, threshold at 4, "fired" flags on the
   three real firings (Qwen color 5.45, Gemma id 4.01, Gemma-id confirm-canary 4.06). The old
   "FAL-3 threshold"→4.17-commit mislabel and "2 weak-signal facts" annotation are gone. The
   figure now matches the corrected §5 text and no longer undersells the fired falsifier.
3. **Agarwal / Merullo / Stoehr** — Agarwal own delta sentence §11 L184 + explicit
   same-layer-vs-relation-before-entity reconciliation §5 L114; Merullo §4 L77 + §11 L186
   (delta: signed per-coordinate split vs qualitative reuse); Stoehr §6 L118 with delta.
   (Stoehr is in §6 only, not §11 as round-2 interp asked — but it is cited with a delta, which
   satisfies prior-art #c. Not a must-fix.)
4. **§10 trimmed** — fork/replay + archive-page moved to Appendix D; body kept to scene-compiler
   21/21 + wrong-source/sign + XOR/XNOR inversion. Landed.
5. **Cuts** — Figs A/B → Appendix D; §3 companion summary cut; §13 ~40% shorter, ends on the
   interpretation consequence; abstract ends on attribution, not a caveat (242 words, ≤250).
6. **Sliding-window de-causalized** — §3 L59 reads depth-not-attention-type; the type-flip is an
   exact no-op at 17 tokens, window-4 live at 19.6. Honestly downgraded.
7. **Null = learned-but-incompetent** — abstract L19 carries the top-1 0/96 bound and
   "learned, not scaffold-versus-any-competent-net." No longer buried mid-§5.

Housekeeping all verified: line-103 TODO gone; zero "in progress/pending" stale phrases; "20
countries … 40 facts" (§5 L103); same-parent count reconciled in AppxA.

## Remaining must-fix

1. **Title "The Commit Layer Does Not Move" is unscoped and sits in tension with the paper's
   own text** (L1/L11 vs §3 L67). §3 L67 says across operations the commit "barely moves … shifts
   by … 2 in Gemma-2-2B"; the title says it does *not* move. The per-fact, within-operation,
   within-model claim is earned (SD 0.00/1.16; retest holds under three frozen locators). The
   *unscoped* absolute is not: scope is 2 models ≤2B, ~4 ops, 17-token prompts, single seed, and
   the cross-family generalization is itself a null (§9). **Fix:** scope the subtitle — e.g.
   append the tested scope, or make the subtitle carry "per fresh fact, within model" — so the
   absolute headline is grounded. This is the single remaining exposure a hostile reader hits
   first. (Round-2 #1 is now *evidentially* answered by confirm-color; the *title* itself was
   never softened.)

## Minor (polish, not blocking)

- **Fig 5 F2A still labels the 42.2% bar "coord (scaffold)"** while §5 L91 / caption L93 are
  careful that 42.2% is not the scaffold's share without the null. The null now backs "learned,"
  so the label is defensible, but it runs one step ahead of the text's hedge. Consider
  "coord (main effect)".
- Two Gemma-identity argmax numbers coexist (Phase-2 4.01, confirm-canary 4.06); abstract cites
  4.06. Both correct, both in Fig 5 — a reader may briefly conflate them. One clause would help.
- Abstract remains dense/caveat-laden at the close (prior-art already noted); cosmetic.

## New contradictions from the edits

None material. Numbers trace consistently across abstract ↔ §3 ↔ §5 ↔ §13 ↔ Fig 5; the
confirm-retest values match in abstract/§5/AppxC/figure; the falsifier tally (2 of 6 fired,
retest clears color, argmax trips Gemma-id plateau) is internally coherent everywhere.

## Score & tier

**Score: 7/10** (up from round-2's 6 — confirm-color both halves + Fig 5 fix were the two
named conditions, and both landed and verify). The honesty discipline is genuinely strong.
- Main conference (ICLR/NeurIPS): **borderline/weak accept** — ready once the title is scoped;
  all substantive round-2 blockers cleared.
- MI workshop (BlackboxNLP): **clear accept.**
- Would my team cite it? Yes — the per-fact commit-invariance metric, the learned-split null,
  the honest-null methodology, and the function-vector delta.

## Submit-readiness verdict

**Submit-ready for workshop now.** For a main-conference submission, one blocking edit remains:
scope the title/subtitle (minutes of work, no new experiment). The still-open items the paper
already names honestly — a behaviorally competent null, long-context attention-type causality,
the checkpoint-trajectory dating — are legitimately future work, not submission blockers.
