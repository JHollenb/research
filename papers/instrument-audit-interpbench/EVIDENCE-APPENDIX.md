# Evidence claim registry (reproducibility addendum)

This paragraph belongs in the paper's `## Appendix: reproducibility`. It is kept in this
separate file rather than edited into `paper.md` because another agent may be editing
`paper.md` concurrently; fold it into the reproducibility appendix when that edit settles.

**Evidence claim registry.** The headline numbers are bound to their receipt bytes in a
saturn-pub evidence claim registry at `papers/evidence-registry/` (append-only,
hash-chained, standard-library only). The §5.1 / §5.3 node-level AUROC over 84 InterpBench
models (activation patching 0.941, EAP-IG 0.924, EAP 0.883, random null 0.498) and the §5.4
preregistered verdicts (P1 PASS, P2 FAIL, P3a/P3b FALSIFIED, P4 PASS) are all covered by the
single claim `iai-node-auroc-84models`, which fingerprints `results/full.json`. A reader
re-checks it offline, without loading a model, with `saturn-pub evidence claims verify
--check --registry papers/evidence-registry/claims.jsonl`, which re-hashes the receipt and
flips the claim to `stale` on any byte drift. (`full.json` has a JSON-array root, which
`ingest_receipt` rejects — it captures top-level `content_sha256`/`gates` from an object — so
this claim was registered through the same public `DependencyFingerprint`/`ClaimRow` API over
the identical file bytes; `verify` treats it like any other file-kind entry. The §5.2
edge-level table rests on `results/edge_full.json`, also array-rooted, and is not separately
registered here.)

The real-generator primary table (§5.1) and the IOI cells (§5.8) are bound to `results/real_full.json` by the claim `iai-real-generator-noemb-84models` (appended 2026-10-05; registry 19 claims, `verify --check` 19/19).
