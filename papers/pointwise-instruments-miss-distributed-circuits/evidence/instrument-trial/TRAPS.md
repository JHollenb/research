# Seven ways to be confidently wrong

Seven measurement failure modes, each hit in practice during this program, each producing
a clean-looking positive result, each now gated against. Condensed from §11 of the source
whitepaper ("The Circuit That Survived Its Coordinates"); the gate that kills each trap is
in bold.

**1. The latent-only false positive.** Internal text positions of a late merged block
showed 0.964 alignment cosine with intervention outcomes — while the rendered image never
changed, because the architecture discards those positions before output. Activation-
magnitude rankings reliably surface exactly these "disposal" sites. **Every internal claim
must be confirmed at an observable the model actually serves (the two-consumer rule).**

**2. Contrast collapse inflates alignment.** When an intervention collapses the two
contrast conditions toward each other, every subsequent patch scores a *higher* alignment
cosine while absolute effects are negligible — the screen names the collapsed arm the
stronger circuit. **Verify baseline contrast viability; report baseline-normalized
progress, never raw alignment.**

**3. The scaffold dominates similarity.** Shared structure across conditions (positional
scaffolds, templates, formatting) dominates global similarity between internal states: a
0.996-cosine reconstruction is compatible with zero semantic content (bundle case 4 — a
content-free template scores the same). **Test with semantic contrasts, or not at all.**

**4. A clean output is not a correct output.** Strong generative priors render plausible
outputs from degenerate internal states. **Output quality checks cannot substitute for
output content checks.**

**5. Terminal readout masquerades as origin.** Writing a complete target state at the last
pre-output boundary reproduces the target perfectly — and identifies nothing but the
readout. **Cross-check late-site interventions with delta-based screens before any "the
concept lives late" conclusion.**

**6. Relaxation artifacts read as structure.** Graph/flow analyses composed over
intervention evidence inherit their relaxations' artifacts: an *empty minimum cut* was a
property of the relaxation, not evidence the route has no bottleneck. **Derived graph
objects are search guides, never certificates.**

**7. A live site is not a circuit.** An early result named one block-call "the counting
circuit" from a behavioral association; under strict replication it survived 5 of 16
paired tests and was formally demoted. **Behavioral liveness is a candidate — promotion
needs the full battery, and every positive result owes its survival to a control designed
to kill it.**
