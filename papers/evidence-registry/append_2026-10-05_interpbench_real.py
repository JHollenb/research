#!/usr/bin/env python3
"""Append the InterpBench real-generator rerun claim (array-rooted receipt → DependencyFingerprint path)."""
from pathlib import Path
import json, sys
from saturn_pub.evidence.claims import ClaimRow, ClaimsRegistry, DependencyFingerprint, _now_iso
HERE = Path(__file__).resolve().parent; REGISTRY = HERE / "claims.jsonl"
receipt = Path("/Users/jakeholl/domains/saturn/experiments/2026-10-05-interpbench-method-audit/results/real_full.json")
cid = "iai-real-generator-noemb-84models"
text = ("instrument-audit-interpbench section 5.1 (primary): no-embedding node-level mean AUROC over the 84 Tracr InterpBench models "
        "under the benchmark's real data generators: activation patching 0.990, EAP-IG 0.976, EAP 0.892, grad x act lab form 0.499 "
        "(no norm division 0.842), write-site lab form 0.462 (RMS raw 0.809), subspace 0.665 (matched-rank random 0.644), null 0.493; "
        "IOI models act_patch = EAP = EAP-IG = 0.500 (section 5.8).")
existing = {json.loads(l)["claim_id"] for l in open(REGISTRY) if l.strip()}
if cid in existing: print("exists"); sys.exit(0)
assert receipt.is_file()
fp = DependencyFingerprint(); fp.add_file(receipt, name="receipt")
stamp = _now_iso(None)
row = ClaimsRegistry(REGISTRY).append(ClaimRow(claim_id=cid, text=text, status="measured", receipt_path=str(receipt), fingerprint=fp, created_at=stamp, updated_at=stamp))
print(cid, row.sha256[:12])
