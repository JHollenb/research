# Round-2 response — "Where You Round Beats How Many Bits" (Hollenbeck)

Two round-2 reviews (`round2-numerics-reviewer.md`, score 6.5/10; `round2-evidence-clarity.md`)
and the custody audit (`../../custody-audit-2026-10-02.md`, "B(x) training continuation",
verdict PASS). All edits are in `paper.md`, `README.md`, and `figures/` only; no file outside
this directory was touched. Numbers below were re-derived this round from
`results/{full6-s1234,core4-s2,core4-s3,full-mid-s0}.json`.

## The one FAIL (evidence-clarity D.1; custody nit #4)

**Fig 8 was the single-order (seed-1234) plot while the caption said "three orders averaged."**
Regenerated as a true 3-order figure. New `figures/make_fig8.py` (one matplotlib process) reads
all three orders and plots, for the four core arms: panel 1 held loss as the 3-order mean with a
min-max band; panel 2 the gap-to-FP32 as the 3-order mean with a min-max band (the primary
metric); panel 3 the one-step gradient error on the seed-1234 probe schedule (its step-0/999
endpoints replicate across orders, stated in the caption). Output is `figures/bx-training-3order.png`
(md5-distinct from the old single-order file). Paper now references it; the caption describes the
mean/band construction honestly. `bx-training-main.png` is retained only as a superseded artifact,
noted as such in the README.

## Numerics reviewer

1. **(§2, §3.2, §5.1, L38, L52) "Disclose the non-monotonic gap; reframe as transient recovery."**
   Added a dedicated paragraph at the loss result: the bf16−B(x) gap is largest early (3-order mean
   **+0.057 at step 300**; +0.073 in the seed-1234 order) and **narrows to +0.044 by step 1000** as
   plain BF16's descent efficiency climbs 0.41→0.84. Framed explicitly as *faster recovery from a
   bad-gradient checkpoint, not accumulating divergence*; the conservative late value is the
   headline. The peak is visible in Fig 8 (centre). Also added to the Limitations bullet. A
   placeholder (`<!-- TODO gap trajectory -->`) marks a dedicated per-step-spread plot as a round-2
   experiment.
2. **(§3 change, L40) "State the training-loss active ingredient = key-mean; GProj/integer-phase do
   not move the loss."** Done at the result: "**For the training loss specifically, the active
   ingredient is the key-mean removal (SageAttention's key smoothing)**: the mean-only arm (−0.027)
   ties or beats full B(x) (−0.021), and the softmax-gradient projection, unembedding-mean removal
   and integer phase do not move the loss measurably here." Abstract, §1 item 4, README headline 4,
   Limitations, and the §8.4 closing line all now attribute the loss benefit to key-mean removal,
   not to "the B(x) recipe." Added a calibration sentence in §2.2 naming which of the three steps is
   load-bearing on which result.
3. **(change #4) "Lift the custody hedge for the arithmetic; keep it for provenance."** The audit
   returned PASS on both arithmetic and job provenance, so the hedge is fully lifted: the §8.4 status
   line, Limitations, README ledger (all rows now "measured (custody PASS)") and provenance paragraph
   say the file→paper arithmetic and job provenance are verified. Scope limits (160M, 2.05M tokens,
   WikiText-2, reference harness) are kept verbatim.
4. **(change #1, essential ≤10-min experiment) "One current-model single fwd+bwd."** Agreed this is
   the single highest-value owed experiment and the binding main-track constraint. Added
   `<!-- TODO current-model fwd+bwd -->` placeholders in §7.3 (a column in the GFPA table) and the
   Limitations scale bullet, with the kill condition stated. It is already owed-experiment #1 in the
   README; left as owed rather than fabricated.
5. **(change #5) "Add the step64000 control at the same 3 data orders (n=1 now)."** Disclosed that
   the dose control is a single data order and added `<!-- TODO step64000 x3 -->`. The ledger row now
   carries "n=1."
6. **(L287) "6–15× the spread" is loose.** Replaced with the measured statement: mean gap 0.044
   against a **cross-order half-range of 0.006 (about 7×)**, consistent in sign across all three
   orders. Recomputed: per-order gaps −0.0387/−0.0416/−0.0509, mean −0.0438, half-range 0.0061 →
   7.2×.
7. **(L295) "within 0.001 nats"** → **0.0011** (ref 2.9562 / bf16 2.9563 / B(x) 2.9572 / mean 2.9561,
   range 0.0011). The "~20×" grad cut now specifies the metric: ~20× on median-per-parameter
   (21.5%→1.1%), ~10× on the norm-weighted metric.

**On scale/novelty (the remaining "borderline reject" driver):** acknowledged as the binding limit
and left honestly bounded. The paper does not claim a benefit above 160M; the current-model fwd+bwd
is flagged as the experiment that would flip the verdict. No new claim was added to paper over it.

## Evidence + clarity reviewer

- **B.6 / C.3 abstract attribution.** Abstract and §1 reworded: 204%→11.8% is now "removing the
  invariant (the per-head key mean, with its row sum restored)" i.e. the two-op B(x), not "subtracting
  the per-head key mean" alone. The 4-bit line is now "**an affine (bias/gain) correction**" (bias =
  Qwen2.5's 1.7%; gain = Qwen3's 0.6%), not "a per-channel gain correction."
- **D.4 FP8 min loss 3.27→3.26.** Fixed (min 3.2583 at t=200; 3.27 was t=100). Paper now says "min
  of 3.26 at step 200."
- **D.5 README throughput last digits.** mean-only 15.1k→**15.0k** (15048), fp32 17.0k→**16.9k**
  (16884). Fixed in README and the new paper ledger row.
- **D.6 "within 0.001 nats."** Fixed to 0.0011 (see numerics #7).
- **Note on the round-1 response's SageBwd parenthetical (2603.02170 exists).** Correct — that arXiv
  ID is real. It is harmless (the paper cites SageAttention3 as [14] and does not cite 2603.02170),
  and `round1-response.md` is left unedited as a historical record; flagging it here instead.
- Abstract re-trimmed to **198 words** after the attribution edits (verified `wc -w`).

## Custody-audit nits (B(x) training continuation section)

1. **Provenance pointer.** The seed-1234 order is now cited as `job-fec87d0ed93a` (full six-arm) in
   paper §8.4, the ledger, and README, replacing `job-05070b1d9ab9` (its bit-identical determinism
   replicate). README notes the two are determinism replicates of the same order.
2. **"twentyfold" at mid.** Metric specified: ~20× on median-per-parameter, ~10× norm-weighted.
3. **Throughput rounding.** Fixed (16.9k / 15.0k).
4. **Main figure single-order.** Resolved by the 3-order regeneration above.
5. **Context numbers out of scope.** The "203.8%→11.8%" / "410m 42.7%→3.0%" numbers are the parent
   §8.2 Table 6 figures (sourced to `ea-pythia160m.json`/`ea-pythia410m.json`), already independently
   verified in the evidence audit; left as-is.

## Net

The FAIL is fixed and every flagged number is corrected and re-derived from the raw JSON. The two
new honesty disclosures (transient gap; key-mean is the sole loss-mover) are in the body. The
remaining gap to main-track acceptance is scale, addressed only by the owed current-model
experiment, which is flagged, not claimed.
