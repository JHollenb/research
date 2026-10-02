# Round-3 response — "Where You Round Beats How Many Bits" (Hollenbeck)

Two round-3 reviews: `round3-numerics-reviewer.md` (7/10, clear workshop accept, borderline main)
and `round3-evidence-audit.md` (**PASS**, one FIX + rounding NITs). All fixes are in `paper.md`,
`README.md`, `reviews/` only; no file outside this directory touched. The §8.3 speed number and the
two rounding NITs were re-derived from raw JSON this session.

## Numerics reviewer — top-5 must-fix (all applied)

1. **Abstract now states the current-model negative.** The measured block ends: "But on the one
   current model tested (Qwen3-1.7B) the precondition is present yet the BF16 gradient error is mild
   (1.9%), failing a preregistered prediction; the training benefit is bounded to that
   large-additive-key-mean regime, one 160M model, not at scale." A frontier reviewer now gets the
   "does this happen in my models" answer from the abstract. (Re-trimmed to 200 words.)
2. **Title + banner narrowed.** Title → "Where You Round Beats How Many Bits: Rotation Swamping and
   Boundary Placement in Low-Precision Attention" (README matched). Banner now says swamping links
   three failures and the FP32 cliff is a companion integer-range fix, and that the three recipe
   steps are named where each applies — no more "one mechanism behind four / one recipe fixes all
   four."
3. **Loss attribution fixed (also evidence item 5).** §8.4 headline now: "removing the per-head key
   mean lowers the final held-out loss by 0.050 nats; the full two-op B(x) lowers it 0.044, its
   softmax row-sum restoration being inert on the loss." The inert op is no longer credited; the
   mean-only arm is listed as "the largest benefit." Abstract and §1 match.
4. **"No longer diagnostic-only" tied to §7.4 in the same breath** at both occurrences (§1 and §8.4
   close): "…and only in the large-additive-key-mean regime; the one current QK-norm model tested
   (Qwen3-1.7B, §7.4) shows no such blowup."
5. **Thin-n floors flagged adjacent to the headlines.** Log-polar leg is now marked "a single thin
   probe (n = 2×48 tokens), not a headline" in §2.3, §8.2 and README headline 5. At the 7× spread
   (§8.4) we add that these are three deterministic data-order replicates (dropout off, seeds
   bit-identical), a data-order spread, not a stochastic-training noise floor.

## Evidence audit

1. **(FIX) §8.3 speed citation.** Corrected to the real source: `spf-native-boundary/results/
   speed-v1.json` part_a[2] (`job-141c554fb988`), bf16_tc 92.62 vs lns8_exact_int 0.9715 TFLOP/s =
   **~95×** (was "~93×" citing a nonexistent two-domain-note table). Re-derived from raw this session
   (2·8192·4096·4096 / time). Paper §8.3, the Appendix A ledger, and README (ledger + the two
   round-0/round-1 "corrected" bullets) all updated; the round-1 "95× → 93×" change is flagged as
   having itself been wrong.
2. **(NIT) Rounding.** Qwen2.5-1.5B plain-BF16 dQ **27.9% → 27.8%** (raw 27.847) in Table 5, the
   Appendix ledger, and README; Qwen2.5-0.5B offset-8M **20.3% → 20.2%** (raw 20.246) in Table 5.
3. **(NIT) §5.1 bias numbers cited.** The 316 / 1.08 / 74% / step-45 calibration figures now carry
   "[from the companion inference paper `../phaselock-kv-shifts/paper.md` §5.1]".
4. **(NIT) §6 ring CIs sourced.** Added: point perplexities are in `free-wins-quality.json`; the
   block-bootstrap 95% intervals are from the companion paper's analysis (§6).

## Tier / scope

Per both reviewers, the paper is **workshop-ready as a bounded claim**; main-track is gated only on
the owed **≥4B forward+backward** (needs >16 GB VRAM — Qwen3-4B was killed at ~15.4 GB on the 16 GB
4080). README now states this explicitly as the one tier-moving experiment. Not fabricated, flagged.

All round-3 numbers re-derived from raw JSON; nothing fabricated.
