#!/usr/bin/env python3
"""Append the 2026-10-05 (late) claims: causal-band relocation and chat-unsaturated cells.
Run with /Users/jakeholl/domains/saturn-pub/.venv/bin/python. Append-only; refuses if a claim_id exists."""
from pathlib import Path
import json, sys
from saturn_pub.evidence.claims import ClaimsRegistry, ingest_receipt, _now_iso
HERE = Path(__file__).resolve().parent; REGISTRY = HERE / "claims.jsonl"
E = Path("/Users/jakeholl/domains/saturn/experiments")
CLAIMS = [
    ("tfc-e20-causal-band-table2", E/"2026-10-05-e20-causal-band-phi2-gpt2xl/results/analysis.json",
     "time-formed-circuits Table 2 causal-band rows and Fig 7: GPT-2 XL L31-42 block 0.888 [0.829, 1.022] rescue 1.203 (locator band 0.160); Phi-2 L21-28 block 0.485 [0.402, 0.517] rescue 0.862 (locator band 0.033); controls OLMo-2 IoU 1.00, Pythia-1.4B IoU 0.71."),
    ("pib-chat-unsat-referential", E/"2026-10-05-pass-indexed-chat-unsaturated/results/arm_b_ref-6fe222d7fd5f/report.json",
     "pass-indexed-baseline section 6: Qwen2.5-1.5B-Instruct chat template, referential reads; median |drift| passes>=1 2.226 nats, median |baseline difference| passes>=2 2.718 nats, 0/12 sign-or-1-nat flips."),
    ("pib-chat-unsat-05b", E/"2026-10-05-pass-indexed-chat-unsaturated/results/arm_a_q05i-7d1a89ea97a7/report.json",
     "pass-indexed-baseline section 6: Qwen2.5-0.5B-Instruct chat template, scene-pinned reads; median |drift| 0.005 nats, 0/12 flips (saturated)."),
    ("pib-chat-unsat-distractor", E/"2026-10-05-pass-indexed-chat-unsaturated/results/arm_c_distr-7cec3eb6012f/report.json",
     "pass-indexed-baseline section 6: Qwen2.5-1.5B-Instruct chat template, distractor 'second animal' read; median |drift| 0.077 nats, |baseline difference| 0.39, 0/12 flips."),
    ("pib-chat-unsat-p3-spearman", E/"2026-10-05-pass-indexed-chat-unsaturated/results/p3-scatter.json",
     "pass-indexed-baseline section 6: Spearman(|drift|, -fixed-parent logprob) = 0.912 over 60 per-pass chat cells (Pearson 0.790)."),
]
existing = {json.loads(l)["claim_id"] for l in open(REGISTRY) if l.strip()}
reg = ClaimsRegistry(REGISTRY); stamp = _now_iso(None)
for cid, receipt, text in CLAIMS:
    if cid in existing: print("skip existing", cid); continue
    if not receipt.is_file(): print("MISSING", cid, receipt, file=sys.stderr); sys.exit(2)
    row = ingest_receipt(reg, receipt, cid, text, "measured", now=stamp); print(cid, row.sha256[:12])
