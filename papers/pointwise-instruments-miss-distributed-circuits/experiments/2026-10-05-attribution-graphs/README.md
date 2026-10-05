# Attribution graphs vs the native model (§4.9)

Evidence for §4.9. Model `google/gemma-2-2b` (FP32 native), Gemma Scope per-layer transcoders via
circuit-tracer (BF16 replacement model), RTX 4080.

| file | what |
|---|---|
| `panel.json`, `PREREGISTRATION.md` | frozen 56-prompt panel (sha256 `f787b9cf0c1d873a88fc3e5d657e1f06fb85936ec632227dd454f4e2dd98d0b6`) and plan, with the 2026-10-05 amendment |
| `flagship-summary.json` | corrected run: single-feature and top-20 group verdicts, three prediction modes, error-node shares; jobs `job-5cf546c13cad`, `job-a356191720e2`, `job-e3031f8a2944`, `job-d3c6b4221dc5` |
| `PREREGISTRATION-e2-dose.md`, `dose-random-control-results.json` | group size k ∈ {5,10,20,50,100} × factor ∈ {0,−0.5,−1,−2,−4}, matched-random control, pruned-graph and supernode arms; jobs `job-7c5949fd0d09`, `job-a3cacc860c09`, `job-693a029d160e`, `job-fc1b97f31e10`, `job-20c58a384add` |

The 50 sealed per-prompt bundles, which re-derive offline, and the code are public in the
saturn-pub repository under `experiments/circuit_tracer/`. A first run that mis-dosed the native
interventions (activation-indexing bug) was withdrawn; its correction note is in that README.

SHA-256:
    f787b9cf0c1d873a88fc3e5d657e1f06fb85936ec632227dd454f4e2dd98d0b6  panel.json
    ec53a7230d2246a8d9bd47472f780f43e719d1b09e9468b5be1e2d32ea09c1ee  PREREGISTRATION.md
    b658282905cbb44e5f42c60e970d7e353090d4fa5ce489a4585583e7ae4c6232  flagship-summary.json
    c68ebe0fd1539a9eb33066219c54f8341fdf5e797eb8d2d23e24dbcccf856dfe  PREREGISTRATION-e2-dose.md
    5efcbb5c841e7fc5fc05b5bfc5d2ffcd08142cff3ad62e66a923c918c12b21b5  dose-random-control-results.json
