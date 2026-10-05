#!/usr/bin/env python3
"""Append claims for time-circuit-scaffold (6) and mdb-saturn-pub (1). Receipts are the primary
record each number is quoted from: a JSON report where one carries the number, else the FINDINGS
file. Run with /Users/jakeholl/domains/saturn-pub/.venv/bin/python; append-only."""
from pathlib import Path
import json, sys
from saturn_pub.evidence.claims import ClaimRow, ClaimsRegistry, DependencyFingerprint, ingest_receipt, _now_iso
HERE = Path(__file__).resolve().parent; REGISTRY = HERE / "claims.jsonl"
E = Path("/Users/jakeholl/domains/saturn/experiments"); R = Path("/Users/jakeholl/domains/research/papers")
CLAIMS = [
 ("tcs-query-gated-authority", E/"2026-10-02-qwen-address-symbol-table/FINDINGS.md", False,
  "time-circuit-scaffold section 1.1: byte-identical K/V patch, query changed only; median added harm 3.130 nats color (16/16), 0.583 position (16/16), 3.021 lookup (16/16)."),
 ("tcs-reader-profile-held", E/"2026-10-01-scaffold-confirmation/qwen-predictive/results/qwen-predictive-held-20ede7e6e0c0/context-analysis.json", True,
  "time-circuit-scaffold section 1.2: frozen 24-coordinate relation reader profile on 8 held contexts, mapped signed cosine 0.954 vs operation-blind 0.566, raw RMSE 0.029 vs 0.149."),
 ("tcs-finetune-asymmetry", E/"2026-10-02-qwen-variant-circuits/analysis/transplant_summary.json", True,
  "time-circuit-scaffold section 1.3: band K/V transplant rescue base->coder 0.921, base->math 0.432, coder->base 0.342, math->base 0.054."),
 ("tcs-breakit-cross-operation", E/"2026-10-02-break-it-r2/FINDINGS.md", False,
  "time-circuit-scaffold section 1.5: frozen band L22-27 fixed-over-ceiling 0.852 arithmetic, 0.950 recall, 1.000 two-hop; joint subject+operand rescue 0.925."),
 ("tcs-null-nets-function-vector", E/"2026-10-02-p2-reviewer-experiments/FINDINGS-AC-coordinator.md", False,
  "time-circuit-scaffold section 1.6: coordinate main effect 0.012/0.014 in untrained/shuffled nets vs 0.381 trained, native top-1 0/96; function-vector injection 0/14 flips, +2.19 nats."),
 ("tcs-routing-transfer-gates", E/"2026-10-02-routing-transfer/results/routing-transfer-7ef4d3f7a69f/report.json", True,
  "time-circuit-scaffold section 2.1: donor frozen routing makes the recipient emit the donor answer (recipient-correct 0.00-0.03, donor-answer 0.97-1.00); MLP gate activations alone reproduce it."),
 ("mdb-circuit-tracer-flagship-corrected", R/"pointwise-instruments-miss-distributed-circuits/experiments/2026-10-05-attribution-graphs/flagship-summary.json", True,
  "mdb-saturn-pub section 4 and pointwise section 4.9: corrected circuit-tracer flagship on Gemma-2-2B, 50/56 admitted; 13/1000 single features necessary, agreement 0.846 [0.824, 0.868]; -2x steer flips 45/50, zero-ablation 15/50; error-node share 11.4-18.5%."),
]
existing = {json.loads(l)["claim_id"] for l in open(REGISTRY) if l.strip()}
reg = ClaimsRegistry(REGISTRY); stamp = _now_iso(None)
for cid, receipt, obj, text in CLAIMS:
    if cid in existing: print("skip", cid); continue
    if not receipt.is_file(): print("MISSING", cid, receipt, file=sys.stderr); sys.exit(2)
    if obj:
        try:
            row = ingest_receipt(reg, receipt, cid, text, "measured", now=stamp); print(cid, row.sha256[:12]); continue
        except Exception as e:
            print("ingest_receipt failed for", cid, "->", type(e).__name__, "; using fingerprint path")
    fp = DependencyFingerprint(); fp.add_file(receipt, name="receipt")
    row = reg.append(ClaimRow(claim_id=cid, text=text, status="measured", receipt_path=str(receipt), fingerprint=fp, created_at=stamp, updated_at=stamp))
    print(cid, row.sha256[:12])
