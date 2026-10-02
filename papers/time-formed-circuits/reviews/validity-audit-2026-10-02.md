# Measurement-validity audit — Paper 1 (time-formed-circuits)

Date: 2026-10-02. READ-ONLY (code, not FINDINGS). No model runs, no paper edits.
Scope: `saturn/experiments/2026-10-02-p1-reviewer-experiments/` (A/B/C) + E20
block/rescue, Mamba clock-dose, FLUX four-quadrant, isolated-vs-in-forward.
Thesis under test (author): circuits are *time-formed* — built over ordered
execution; "store is not in early layers" is EXPECTED and non-discriminating.

Custody (numbers trace to final runs) is already PASS per `custody-audit-2026-10-02.md`;
this audit is about **what the interventions can and cannot discriminate**.

---

## A — Formation vs propagation (`worker_pA_formation.py`, job-802a/d37e)

(a) **Claim:** the late band is *constructed*, not the seed linearly propagated into late K/V.
(b) **Computed:** transplant seeded band vs (i) seed-layer K/V, (ii) matched-width early band,
(iii) LOO-by-identity ridge image of the seed, (iv) a **freeze** arm. The freeze
(`_add_freeze_hooks`) captures the pre-layer hidden state at the *subject position* and writes it
back post-layer — i.e. it zeroes the attn+MLP residual delta **only at the subject position, only
for pre-band layers** (Qwen L13–21; Gemma L8–15). The **band layers run normally** and **all other
positions run normally**. In Gemma `freeze_layers == early_layers == [8..15]`; the band [16..23] is
untouched.
(c) **Discriminating:** legs (i)+(ii)+(iii) genuinely refute *linear* propagation — late 0.87/0.98
vs early −0.03/−0.03, seed-layer −0.01/+0.08, linear-image 0.02/0.10, held-out R² −0.13/−0.06. That
is VALID as an answer to the reviewer's attack. **Expected-under-both:** "late ≫ early" alone does
not separate time-formed from a late space-circuit; it is a localization, not a construction, result.
The **freeze leg is uninformative for "built over time"**: by construction it cannot see formation
that happens *inside the band* or *across other positions* — exactly the routes the thesis predicts.
A near-null freeze is therefore TRIVIALLY-EXPECTED under the thesis.
(d) **Verdict:** legs i–iii **VALID** (refute linear propagation); freeze leg **UNINFORMATIVE /
TRIVIALLY-EXPECTED**.
(e) **Round-2 narrowing — licensed?** Yes, as worded. The paper (§3.5, §11) says "77% survives" (Qwen
0.675/0.871=0.775), "intervening-layer construction unsupported in both" (Qwen 0.197<0.20 near-miss;
Gemma freeze no-op), and explicitly declines to claim construction, concluding only "assembled into
the late band, not read off the source." That scoping is correct and matches what the instrument can
see. Two flags: (1) the Qwen "0.197 is real (CIs separated)" rests on **item-bootstrap** CIs that
Part B itself calls anti-conservative — not re-done under identity clustering. (2) Any phrasing like
"formed mostly from the seed" would be in tension with the linear-image refutation; the paper's
actual wording avoids it — keep it that way.
(f) **Correct cheap test (~10 min, 4080):** reuse this worker, vary `mediator_layers`/add a band-
internal freeze: (A) **progressive capture** — transplant {22},{22,23},…,{22..27}; rescue crossing
threshold only after several band layers accumulate is positive evidence of over-band formation.
(B) **band-internal subject-position freeze** — freeze subject residual at L22..27 (not L13–21) and
re-capture; collapse here (where pre-band freeze was null) localizes construction to the band.
(C) **position-resolved** — ablate band-layer attention from the subject row to earlier positions;
loss of the transplantable store = formation-by-reading-over-positions.

## B — Identity-clustered bootstrap (`analyze_B_clustered.py`)

(a) Do block/rescue survive honest (identity-clustered) CIs? (b) Resamples `subject`, pools rows,
10k reps; sanity-gate reproduces item medians to <1e-6 (verified in JSON). (c) Correctly fixes the
pseudo-replication the reviewer flagged; medians unchanged, CIs widen, lower bounds >0 in all 4 cells.
(d) **VALID** (clean, pure reanalysis). (e) Licensed. One honesty note already in-paper: under
clustering the wrong-identity *signed* CI includes 0 in 3/4 cells, so the content control is the
candidate top-1, not the signed fraction — the paper states this.

## C — Error-node interchange (`worker_pC_e6_error.py`, job-5b8f)

(a) Does a *matched* feature+error swap reach the identity store? (b) Reimplements circuit-tracer's
unfrozen perform-loop adding `dE=E_filler−E_clean` at the decoder site; `features_only` reproduces
the library (0.044 vs 0.049; color 0.313 vs 0.344), so error arms are in-regime. (c) Identity
features+error 0.31 vs native K/V 0.94; color 0.99. The identity miss is **partly expected by
construction** (transcoders replace MLP; attention is not in the basis), as the paper concedes — and
the paper *also* concedes the operators are **not magnitude-matched** (native perturbs the whole
attention path, feature op only MLP+error), so 0.31-vs-0.94 conflates basis-coverage with
perturbation size. The informative, non-trivial content is the **behavior split**: color IS recovered
(0.99) once error is included, so the basis is not uniformly blind — that makes the identity miss
meaningful. (d) **VALID but partly-expected-by-construction**; the color/identity split carries the
weight. P-C2 (error_only>features_only) was FALSE (error_only negative) — reported honestly. n=12
identity → wide interval on 0.31 (paper says so).

## E20 — block/rescue + cross-family (`worker_e20_mediation.py`, `worker_e20_xfam.py`)

(a) A late-band K/V store has independent causal authority. (b) Isolated prefix→suffix split; block =
overwrite seeded band with unseeded recipient's; rescue = transplant seeded band into a fresh unseeded
recipient; wrong-identity control; private cloned caches; replay Δ≤8.6e-5. (c) **Discriminating** —
the independent rescue (0.71–0.99) + wrong-identity authoring the competitor (top-1 0.75–1.00) +
near-zero earlier-band establishes a *committed, content-specific, transplantable* store. This is the
paper's real contribution and is NOT "store is late" restated. (d) **VALID** (strongest result). Caveat
(in-paper): recipient-native formation, not donor-free; not a unique route.

## Isolated vs in-forward cut (§2.2; `run_sae_comparison.py`)

(a) In-forward cuts leak into formation. (b) L0 in-forward authors 0.985 vs isolated 0.009. (d)
**VALID and foundational** — the clean 0.985/0.009 gap is what licenses every isolated-cut store claim
and is itself a good hygiene demonstration.

## Mamba writer clock-dose (`clock_dose_worker.py`, job-baf1/cbb0/e55f)

(a) The writer's causal property is its *write*, not its near-stopped *clock*. (b) At one layer, dose
A (retention), B (write), or dt (joint) by ×0.5/×2, 3 prompts/task; metric = Δmargin vs clean.
(c)(d) **WEAK.** Problems visible in `summary.json`: (1) The **dt (joint) arm is the largest lever**
(130M-identity dt 1.868 > B 1.369), yet "write is the larger lever in all six cells" compares only
A-vs-B and sets dt aside — but **dt IS the clock/timestep** that "stopped," so the thing that moved
the answer most is the clock, dismissed only because it co-moves write. (2) At a near-frozen writer
dt≈0.03, a ×2 retention(A) dose leaves ρ=exp(A·dt)≈1, so the A-only arm is **near-inert by
construction**, not by discovery — "retention isn't the lever" is partly guaranteed. (3) Specificity:
the large levers (B, dt) are **NOT writer-specific** (B writer/neighbor ratio ≈1.05–1.18), while the
only writer-specific lever (A) is tiny — so *nothing here cleanly localizes a causal writer*; the
paper flags clock non-specificity (2.8B neighbor 0.36>writer 0.04) but not that the write is equally
non-specific. (e) "Clock lever not causal" is **not well licensed as stated**; licensed claim is
narrower: "a pure-retention(decay) perturbation is weak and writer-specific, while write/timestep
perturbations are strong but not writer-localized." (f) Cheap test: force the writer's elapsed clock
up to the neighbor's 1–8 range (large dt multiply, not ×2) **while holding W=dt·B·u fixed** (rescale B
by 1/dt_factor) to isolate retention at a *running* clock. Also: custody flags paper L226 "three of
six" should be **two of six** (writer_A_releaseclock_k2>0 only 130M-id +0.207, 370M-id +0.140).

## FLUX four-quadrant / strict signature (§6, §2.3)

(a) A strictly path-distributed support profile. (b) 15 cells, P-progress bounds 0.562/0.207/0.913/
0.011 vs 0.90/0.15 lines. (c)(d) **VALID-but-weak as a support-profile observation; UNINFORMATIVE as
a mechanism claim** — the paper itself says so (§2.3: a weighted-additive `y=Σxᵢ/n` passes all four;
"buys less than its name suggests"), and demotes it from central. Flag: the sufficiency pass is
**threshold-fragile** — all-call 0.913 clears the 0.90 line by 0.013 while a single call already
reaches 0.562; a slightly different criterion flips the verdict. The paper discloses this. Licensed
because not over-read.

---

### Bottom line
- **VALID / central:** E20 block-rescue (+cross-family), isolated-vs-in-forward hygiene, B clustering.
- **VALID but scoped:** A legs i–iii (refute *linear* propagation only); C (expected-by-construction;
  color/identity split is the signal).
- **UNINFORMATIVE for the thesis:** A's freeze leg (cannot see band-internal / cross-position
  formation) — the author's self-flag that the formation analysis is non-discriminating is CORRECT,
  and the paper's narrowed §3.5/§11 wording is licensed precisely because it claims only
  "assembled into the late band, not read off the source."
- **WEAK:** Mamba clock-dose (dt is the largest lever yet set aside; A-arm inert at a frozen clock;
  large levers non-specific) and the FLUX strict signature (threshold-fragile, mechanism-silent).
- No fabrication or wrong-run contamination found (consistent with custody PASS). The only numeric
  fix is paper L226 "three"→"two" of six (already in custody required-fixes).
