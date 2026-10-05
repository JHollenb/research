#!/usr/bin/env python3
"""Append the remaining headline bindings flagged by submission-review-2026-10-05: time-formed FLUX/7B/original panel,
pointwise FLUX/LM/instrument trial, pass-indexed format-vs-content control, instrument-audit edge level, and the seven
mdb-saturn-pub section-3 demonstration rows. Run with /Users/jakeholl/domains/saturn-pub/.venv/bin/python; append-only."""
from pathlib import Path
import json, sys, glob
from saturn_pub.evidence.claims import ClaimRow, ClaimsRegistry, DependencyFingerprint, ingest_receipt, _now_iso
HERE = Path(__file__).resolve().parent; REGISTRY = HERE / "claims.jsonl"
E = Path("/Users/jakeholl/domains/saturn/experiments"); S = Path("/Users/jakeholl/domains/saturn/results")
P = Path("/Users/jakeholl/domains/research/papers/pointwise-instruments-miss-distributed-circuits/evidence")
verdict = sorted(glob.glob(str(P/"instrument-trial/verdicts/*.json")))
CLAIMS = [
 ("tfc-flux-four-condition-table3", E/"2026-09-30-flux2-joint01-time-accumulation/results/full-report.json",
  "time-formed-circuits section 6.1 / Table 3 / Fig 5: FLUX.2 four-condition bounds 0.5620 (max single-call write) / 0.91309 (min all-call write) / 0.20743 (min single-call source replacement) / 0.01101 (max all-call)."),
 ("tfc-e20-7b", E/"2026-10-02-scale-9b-scaffold/results/e20_analysis_with_7b.json",
  "time-formed-circuits section 3.4: Qwen2.5-7B paged FP32, 40 facts: rescue 0.770, block 0.595, wrong-identity -0.026; commit median L21, all facts L19-27."),
 ("tfc-e20-original-panel", E/"2026-09-30-full-layer-sweeps/FINDINGS-E20-mediation.md",
  "time-formed-circuits section 3.3: Qwen2.5-1.5B original panel block 0.924, rescue 0.871, wrong-identity authors own answer 37/42, earlier band 0.066."),
 ("pim-flux-four-condition", P/"four-quadrant-tests/report-final-tests-rerun-job-69e2f6a6b492.json",
  "pointwise section 4.1: FLUX.2 Klein 4B route components, any single step leaves >=22% of the transition, all steps leave 0.13%, insertion carries 91% (verify.py re-derives from this bundle)."),
 ("pim-lm-grid", P/"four-quadrant-tests/report-lm-grid-job-72f0e98679d5.json",
  "pointwise section 4.3: single-layer key/value replacement removes at most 16% (GPT-2 small) and 8-18% (Qwen2.5-1.5B, Gemma-2-2B); second-half replacement removes 81-104% and flips the top answer on 83-95% of items."),
 ("pim-instrument-trial", Path(verdict[0]) if verdict else P/"instrument-trial/REDACTIONS.json",
  "pointwise section 5: blind-graded comparison of four standard readouts against the native output, standard arm misreports in 4 of 4 graded cases (instrument-trial-verify re-derives every verdict)."),
 ("pib-format-content-control", E/"2026-10-02-pass-indexed-baseline/results/pass-indexed-5dbbbeee0dea/control-analysis.json",
  "pass-indexed-baseline section 4: format priming +1.312 nats, question-content increment -0.051, answer-content increment +2.247 (length-matched control, Qwen2.5-1.5B base)."),
 ("iai-edge-real-84models", E/"2026-10-05-interpbench-method-audit/results/real_edge_full.json",
  "instrument-audit-interpbench section 5.3: edge-level AUROC over the 84 Tracr models under the real generator, EAP 0.868, EAP-IG 0.894."),
 ("mdb-demo-shared-kv-ancestry", S/"causal-context-vm-end-to-end/job-59bd7d03489a/report.json",
  "mdb-saturn-pub section 3.1 row 1: shared causal K/V ancestry, raw committed K/V 1,118,208 vs 1,892,352 bytes (40.91% reduction), 8/8 tokens match the comparator."),
 ("mdb-demo-durable-residency", S/"causal-context-vm-integration/job-97e3192c594e/report.json",
  "mdb-saturn-pub section 3.1 row 2: two resident sessions within 1,314,816 bytes, 2 LRU evictions, restore reproduces the first-token logit digest, fresh-process reopen after source deletion."),
 ("mdb-demo-cuda-vmm-aliasing", S/"virtual-context-three-closures-cuda-vmm/job-9e7f79751e31/report.json",
  "mdb-saturn-pub section 3.1 row 3: CUDA virtual-memory aliasing of a shared prefix, attention outputs bit-identical to flat tensors, physical K/V 32 MiB -> 24 MiB."),
 ("mdb-demo-routed-working-set", S/"primary-routed-working-set/local-f1a0365c04ef/report.json",
  "mdb-saturn-pub section 3.1 row 4: routed working-set decode, batch 4 cache 1.5 GiB -> 6 MiB, 63.99 -> 119.04 tok/s (1.859x), 16/17 cells keep dense top-1."),
 ("mdb-demo-archive-read", S/"spectral-virtual-context/local-guard-20260924-scale-v2/report.json",
  "mdb-saturn-pub section 3.1 row 5: 2,048-page archive representing 59,356 tokens, selected pages answer 4/4 held questions, absent and matched-wrong pages 0/4."),
 ("mdb-demo-scene-compiler-rgb", Path("/Users/jakeholl/domains/research/demos/artifacts/scene-generator/artifacts/reports/cross-model-replication.json"),
  "mdb-saturn-pub section 3.1 row 6: scene compiler reproduces 21/21 recorded native RGB endpoints across five diffusion families (receipt lives under research/demos, not yet committed to the research repository)."),
 ("mdb-demo-mamba-fork-replay", E/"2026-09-30-mvm-mamba-cot/results/mamba-7075c40c839b/report.json",
  "mdb-saturn-pub section 3.1 row 7: Mamba-130M virtual memory, no-op and uninstall error 0, fork bit-exact, staged native replay max error ~2.2e-4 with matching argmax."),
]
existing = {json.loads(l)["claim_id"] for l in open(REGISTRY) if l.strip()}
reg = ClaimsRegistry(REGISTRY); stamp = _now_iso(None)
for cid, receipt, text in CLAIMS:
    if cid in existing: print("skip", cid); continue
    if not receipt.is_file(): print("MISSING", cid, receipt, file=sys.stderr); sys.exit(2)
    try:
        row = ingest_receipt(reg, receipt, cid, text, "measured", now=stamp)
    except Exception as e:
        fp = DependencyFingerprint(); fp.add_file(receipt, name="receipt")
        row = reg.append(ClaimRow(claim_id=cid, text=text, status="measured", receipt_path=str(receipt), fingerprint=fp, created_at=stamp, updated_at=stamp))
        print("  (fingerprint path:", type(e).__name__+")")
    print(cid, row.sha256[:12])
