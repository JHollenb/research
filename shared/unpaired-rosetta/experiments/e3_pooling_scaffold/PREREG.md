# E3 preregistration: pooling scaffold and commit layer (frozen before the first scored job)

Frozen 2026-10-09. The worker sha256 is recorded in each `submission.json`. Any later edit to `worker.py`
requires a new sha, and the smoke gate runs again inside the next job.

## Question

The paper's weakest cells are Qwen3 generative pooling on long captions (SPC, DCI, DOCCI), which the project
page reports as close to chance. Does a caption-independent scaffold inside the pooled state explain part of
that, and does the last layer carry readout directions that hurt alignment?

## Setting

- **Model:** `Qwen/Qwen3-1.7B`, bf16, on one CUDA GPU. The paper's Fig. 21 ladder uses the same model.
  Qwen3-8B is a TODO; see "Not covered".
- **Data:** their row order for `coco_train2014` (caption 0) and `StanfordParagraphCaptioning`. We take the
  first 2048 items, which is two of their 1024-item slices.
- **Image side:** their stored `dinov2_vit-b14@224_mean` rows. Row order was verified in `prepare.py`
  against their stored MPNet: SPC matched cos 1.000; COCO caption-0 retrieves its own row 95.7% of the time.
- **Metric:** their clipped CKA per 1024 slice, averaged over slices (their `token_pooling.py` protocol).

## Arms

| arm | definition |
|---|---|
| `think/gen_all/L{last}` | Replication of their generative pooling: thinking on, 128 greedy tokens, mean of the final-norm states that produce the tokens. |
| `think/gen_tokcentered` | Each state minus the corpus-mean state for the token it produces, then averaged. This is our displacement operation, with the token's own state as the template. |
| `think/gen_poscentered` | Control. Each state minus the corpus mean at its generated position. When every item hits the 128-token cap, this is a constant shift, and CKA is invariant to it. |
| `think/gen_post_think` | Only positions after `</think>`. Falls back to `gen_all` if `</think>` is not reached, and the coverage is reported. |
| `nothink/*` | The same arms with `enable_thinking=False`. The template already closes `</think>`, so `gen_post_think` equals `gen_all` here. |
| `mean/mean_all` | Their `MeanPooling`: mean over all chat-template tokens. |
| `mean/mean_caption` | Caption tokens only. |
| `mean/mean_no_first` | Drops the first real token, the attention-sink position. |
| depth sweep | Every arm at depth 0.5, 0.6, 0.7, 0.8, 0.9 and 1.0 of 28 layers. |
| `reference/mpnet_stored` | Their stored MPNet, as a sanity reference. |

## Predictions (Claim A = scaffold dilution, Claim B = commit layer)

Disclosure, two local wiring tests on CPU (Qwen3-0.6B, 24 items, 24 tokens):

1. The first test (COCO) showed the first 16 generated positions identical for every item. A1 was written after it.
2. Re-checking the math before freezing (`response.md` §3.3), we found that position-centering is a constant
   shift when lengths are capped. We added the token-centered arm and moved A2 onto it. A2 was changed before any
   CKA was seen.
3. The second test (SPC, after that change) printed clipped CKA values. With n = 24, far below their
   1024-item slices, they are uninformative. No prediction was changed after that test.

| id | prediction | falsified if |
|---|---|---|
| A1 | With thinking on, the first ≥ 12 generated positions are the same token for ≥ 90% of items on both corpora (scaffold token share). | share < 0.9 at position 12 on either corpus |
| A2 | `think/gen_tokcentered` > `think/gen_all` at the final layer, on both corpora, in both slices. | not higher in at least 3 of the 4 corpus × slice cells |
| A2c | Control, not a prediction. When ≥ 90% of items hit the token cap, `think/gen_poscentered` differs from `think/gen_all` only through clipped CKA's per-row clipping and normalization of a constant shift. Reported, not scored. | — |
| A3 | On SPC, the best scaffold-removed generative arm (`gen_tokcentered`, `gen_post_think`, or any `nothink` arm) beats `think/gen_all` by ≥ 0.02 clipped CKA (mean over slices). | gain < 0.02 |
| A4 | `mean/mean_caption` ≥ `mean/mean_all` at the final layer on both corpora. | lower on either corpus |
| B1 | For `mean/mean_caption` and `nothink/gen_all`, the best depth is < 1.0 on both corpora. | the best depth is 1.0 for either arm on either corpus |
| B2 | That best depth lies in 0.6–0.9, our measured commit band. | outside 0.6–0.9 |

## What we report regardless

Every arm, layer and slice. The scaffold token share by position. Coverage of `</think>`. Generation lengths.
Six decoded generations per corpus and mode. Wall time and peak VRAM. A negative result is reported as fully
as a positive one.

## Smoke gate (inside the job; any failure aborts before the scored run)

- Tokens and states are deterministic across two identical calls.
- Captured positions per item are between 1 and the token budget.
- All values are finite.
- `clipped_cka(x, x) == 1`.

## Not covered (TODO)

- Qwen3-8B, their 8B files: needs a paged or int8 path on a 16 GB card, or a larger GPU.
- DCI and DOCCI.
- WP FOSCTTM for the winning arm on the full corpus (E3b), so the gain is measured on their alignment metric
  and not only on their predictor.

## Amendment 1 (2026-10-09, before any scored report)

Three attempts (`job-6ade15147444`, `job-9bd9f5fbbd8b`, `job-799c12bf1b57`) were killed on VRAM. The last peak
was 12.3 GB, in SPC with thinking on at batch 64. None of them emitted a report, and no CKA was seen. Change:
SPC now runs at batch 16 (`--long-batch`); COCO stays at 64. The change affects memory only, apart from bf16
numerics of left-padded greedy decoding. Predictions are unchanged. New worker sha in `submission.json`.

## Scored run 1 (job-9426423166f5): verdicts as frozen

A1 TRUE, A2 FALSE (0/4), A3 FALSE (best scaffold-removed arm nothink/gen_tokcentered/L25 0.582 vs think/gen_all
0.591), A4 TRUE (margin 0.001–0.013), B1 FALSE, B2 FALSE. Best depth was 0.89 in 3 of 4 cells; for SPC mean_caption
it was 1.0, with 0.596 vs 0.594 at 0.89. The analyzer's first A3 pass picked `think/gen_post_think`, which equals
`gen_all` when `</think>` is never reached (0% coverage). That was a bug, fixed before the verdict was recorded.
The verdict is unchanged.

## Amendment 2 (2026-10-09, after scored run 1; POST-HOC, labelled as such)

Audit of the A2 arm. `gen_tokcentered` subtracts each token's corpus mean, and that mean *includes the item's own
states*. For a token seen once, the state is subtracted from itself and becomes zero. Rare tokens are the
caption's content words, which thinking mode restates. So the arm deletes content as well as scaffold, which
biases it against A2. That bias fits the measured pattern: the arm helps with thinking off (up to +0.05 at middle
layers) and hurts with thinking on.

Corrected arm `gen_tokcentered_loo20` (final two layers only):
- subtract the produced token's mean computed without the item's own states;
- subtract only for tokens seen ≥ 20 times in other items (frequent, template-like); leave other states unchanged;
- report the share of positions that were centered.

Prediction A2': `think/gen_tokcentered_loo20` > `think/gen_all` at the final layer in ≥ 3 of 4 corpus × slice
cells. Falsified otherwise. Every other frozen verdict above stands as recorded whatever A2' shows. Same data,
model and seeds; one job.

## Amendment 3 (2026-10-09, after both scored runs): bars decide predictions, not claims

The frozen bars above stay as recorded. What changes is how a claim is read from them. A2, A3 and B1 required a
fixed margin or "every cell", and one bar missed by a tie should not flip a whole claim. Each claim is now read
from paired per-slice effects (`analyze.py` writes them to `verdicts.json` → `effects`). A cell's sign counts only
when both 1,024-item slices agree. Decoding is greedy, so the slices measure sampling consistency, not seed noise.

| claim | frozen bars | effects (clipped CKA, final layer unless stated) | claim reading |
|---|---|---|---|
| A (token-level scaffold dilutes CKA with thinking on) | A2 ✗, A2′ ✗, A3 ✗ | centering with thinking on: −0.010 to −0.021, every cell negative | **refuted.** The effect has the opposite sign, so no margin choice matters. |
| A, thinking off | not frozen | token-centering +0.004 / +0.023, leave-own-out +0.008 / +0.027 (COCO / SPC), every cell positive | the mechanism works where the generated text is not a restatement. It still ends below thinking on (0.575 vs 0.591, SPC). |
| A4 (caption tokens ≥ all tokens) | A4 ✓ | COCO +0.002 (a tie in size), SPC +0.013 | **supported on SPC; a tie on COCO.** Recorded "true" before; that was too generous. |
| B (a late non-final layer beats the final layer) | B1 ✗, B2 ✗ (one cell) | depth 0.89 − 1.0: +0.007 to +0.015 in 5 of 6 non-thinking cells, including their own `mean_all` on both corpora; −0.002 for SPC `mean_caption`; thinking on −0.002 (COCO) and −0.027 (SPC) | **supported in direction, small**, for mean pooling and no-thinking generation. **Not** for their headline thinking-mode arm. The effect on FOSCTTM is untested. |

