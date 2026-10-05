#!/usr/bin/env python3
"""Build the submission evidence claim registry from the papers' receipt files.

This script ingests one saturn-pub evidence claim per headline receipt for the
four papers under submission, into the append-only hash-chained ledger
``claims.jsonl`` in this directory. Each claim fingerprints the exact bytes of
the receipt file that carries the number; ``saturn-pub evidence claims verify``
re-hashes those bytes and flips a claim to ``stale`` if its receipt drifts.

Run from the saturn-pub repository's environment, e.g.:

    /Users/jakeholl/domains/saturn-pub/.venv/bin/python build_registry.py

It refuses to run if ``claims.jsonl`` already exists (delete it to rebuild),
because the ledger is append-only and re-running would duplicate rows.

Receipt identification (measured from src/saturn_pub/evidence/claims.py):
``ingest_receipt`` requires the receipt JSON root to be an object and captures
``content_sha256`` / ``config_sha256`` / ``gates`` when present, then
fingerprints the receipt file (raw bytes). One receipt here, InterpBench
``full.json``, has a JSON *array* root, which ``ingest_receipt`` rejects; it is
registered through the same public ``DependencyFingerprint`` / ``ClaimRow`` /
``ClaimsRegistry.append`` API, fingerprinting the identical file bytes, so
``verify`` treats it exactly like every other file-kind entry.
"""

from __future__ import annotations

import sys
from pathlib import Path

from saturn_pub.evidence.claims import (
    ClaimRow,
    ClaimsRegistry,
    DependencyFingerprint,
    ingest_receipt,
)
from saturn_pub.evidence.claims import _now_iso  # timestamp helper used by ingest_receipt

HERE = Path(__file__).resolve().parent
REGISTRY = HERE / "claims.jsonl"
E = Path("/Users/jakeholl/domains/saturn/experiments")
RESEARCH = Path("/Users/jakeholl/domains/research/papers")

# (claim_id, paper, receipt_path, text, object_rooted)
CLAIMS = [
    # ---- time-formed-circuits ----
    (
        "tfc-e20-xfam-table2",
        "time-formed-circuits",
        E / "2026-10-02-e20-cross-family/results/analysis.json",
        "time-formed-circuits Table 2 (E20 block-and-rescue) cross-family cells: "
        "Qwen2.5-1.5B published + held-out, Gemma-2-2B, SmolLM2-1.7B; median signed "
        "fraction of per-row seed gain for block-removed and rescue-recovered.",
        True,
    ),
    (
        "tfc-e20-nonqwen-table2",
        "time-formed-circuits",
        E / "2026-10-05-e20-nonqwen-families/results/analysis.json",
        "time-formed-circuits Table 2 blind-band rows: OLMo-2-1B block 1.087/rescue "
        "0.941, Pythia-1.4B 1.294/1.624, Phi-2 0.033/0.642, GPT-2 XL 0.160/0.658.",
        True,
    ),
    (
        "tfc-p1b-clustered-ci-table2",
        "time-formed-circuits",
        E / "2026-10-02-p1-reviewer-experiments/results/B_clustered_stats.json",
        "time-formed-circuits Table 2 identity-clustered 95% bootstrap CIs (resample "
        "identities, 10000 reps) for the block/rescue dissociation; 4 cells, lower "
        "bounds > 0.",
        True,
    ),
    (
        "tfc-p1c-e6-interchange-fig4",
        "time-formed-circuits",
        E / "2026-10-02-p1-reviewer-experiments/results/C_analysis.json",
        "time-formed-circuits section 5 / Fig 4: matched feature+error interchange "
        "toward filler, identity 0.314 (error-only -0.149), color 0.990.",
        True,
    ),
    (
        "tfc-e6-native-kv-cut",
        "time-formed-circuits",
        E / "2026-09-30-full-layer-sweeps/results/gemma2-ed4ce1ac5974/report.json",
        "time-formed-circuits section 5: Gemma-2-2B native key/value cut, identity "
        "second-half removed fraction median 0.943 (the 0.94 native cut that the "
        "0.31 feature interchange cannot reach).",
        True,
    ),
    (
        "tfc-breakit-operation-general",
        "time-formed-circuits",
        E / "2026-10-02-break-it-r2/results/breakit-r2-qwen15base-6c46852af315/report.json",
        "time-formed-circuits section 8.1: frozen Qwen2.5-1.5B L22-27 band is "
        "operation-general over recall/two-hop/arith; best-site-contains-L22 rate "
        "1.0; recall block/rescue 0.902/0.862, two-hop 0.911/0.933, arith "
        "joint-operand rescue 0.925.",
        True,
    ),
    # ---- pass-indexed-baseline ----
    (
        "pib-r0-drift-r2-flips-base",
        "pass-indexed-baseline",
        E / "2026-10-02-pass-indexed-baseline/results/pass-indexed-35d4adaeed36/analysis.json",
        "pass-indexed-baseline section 3 (R0) and 5 (R2), Qwen2.5-1.5B base FP32: "
        "per-pass median drift +3.125/+2.202/+2.063 nats (all positive); R2 11/12 "
        "install-conclusion flips; fact-span K/V bit-identical across passes "
        "(c2_factspan_kv_maxabs 0.0).",
        True,
    ),
    (
        "pib-instruct15b-raw",
        "pass-indexed-baseline",
        E / "2026-10-05-pass-indexed-instruct-7b/results/q15i_raw_full-23194c4f1d09/analysis.json",
        "pass-indexed-baseline section 6: Qwen2.5-1.5B-Instruct raw-text regime, "
        "FP32 eager; later-pass baseline moves by nats and R2 install-conclusion "
        "flips = 9/12.",
        True,
    ),
    (
        "pib-instruct15b-chat",
        "pass-indexed-baseline",
        E / "2026-10-05-pass-indexed-instruct-7b/results/q15i_chat_full-2e4198b3de14/analysis.json",
        "pass-indexed-baseline section 6: Qwen2.5-1.5B-Instruct chat-template regime, "
        "FP32 eager; drift attenuates to ~0 and R2 flips = 0/12 (saturated-read "
        "boundary case).",
        True,
    ),
    (
        "pib-instruct7b-raw-bf16",
        "pass-indexed-baseline",
        E / "2026-10-05-pass-indexed-instruct-7b/results/q7i_raw_full_bf16-8243f04af7c7/analysis.json",
        "pass-indexed-baseline section 6: Qwen2.5-7B-Instruct raw-text regime, "
        "paged-layer BF16; R2 install-conclusion flips = 4/12.",
        True,
    ),
    (
        "pib-instruct7b-chat-bf16",
        "pass-indexed-baseline",
        E / "2026-10-05-pass-indexed-instruct-7b/results/q7i_chat_full_bf16-1d9876bd8f78/analysis.json",
        "pass-indexed-baseline section 6: Qwen2.5-7B-Instruct chat-template regime, "
        "paged-layer BF16; drift ~0 and R2 flips = 0/12.",
        True,
    ),
    # ---- instrument-audit-interpbench ----
    (
        "iai-node-auroc-84models",
        "instrument-audit-interpbench",
        E / "2026-10-05-interpbench-method-audit/results/full.json",
        "instrument-audit-interpbench sections 5.1/5.3/5.4: node-level AUROC over 84 "
        "InterpBench models; act_patch mean 0.941, EAP-IG 0.924, EAP 0.883, random "
        "null 0.498; preregistered verdicts P1 PASS, P2 FAIL, P3a/P3b FALSIFIED, P4 "
        "PASS. full.json is JSON-array-rooted, so it is registered via the "
        "DependencyFingerprint/ClaimRow public API (ingest_receipt requires an "
        "object root).",
        False,  # array root -> lower-level API
    ),
    # ---- pointwise-instruments-miss-distributed-circuits ----
    (
        "pim-prereg-panel-sae-v2",
        "pointwise-instruments-miss-distributed-circuits",
        RESEARCH
        / "pointwise-instruments-miss-distributed-circuits/experiments/2026-09-22-sae-comparison/results/combined_summary_v2.json",
        "pointwise-instruments section 4.3 (preregistered panel) and 4.4 (SAE), "
        "rerun v2: isolated best-single-layer vs second-half fractions and flip "
        "rates across GPT-2/Gemma-2-2B/Qwen2.5-1.5B, plus SAE single-layer/global/"
        "subject arms. Receipt from the paper's own experiments/2026-09-22-"
        "sae-comparison (not in the handoff receipt list; added so the pointwise "
        "table is covered by a claim ID).",
        True,
    ),
]


def main() -> int:
    if REGISTRY.exists():
        print(f"refusing to build: {REGISTRY} already exists (delete it to rebuild)", file=sys.stderr)
        return 1
    registry = ClaimsRegistry(REGISTRY)
    stamp = _now_iso(None)
    for claim_id, paper, receipt, text, object_rooted in CLAIMS:
        if not receipt.is_file():
            print(f"MISSING receipt for {claim_id}: {receipt}", file=sys.stderr)
            return 2
        if object_rooted:
            row = ingest_receipt(registry, receipt, claim_id, text, "measured", now=stamp)
        else:
            fp = DependencyFingerprint()
            fp.add_file(receipt, name="receipt")
            row = registry.append(
                ClaimRow(
                    claim_id=claim_id,
                    text=text,
                    status="measured",
                    receipt_path=str(receipt),
                    fingerprint=fp,
                    created_at=stamp,
                    updated_at=stamp,
                )
            )
        print(f"{paper:52s} {claim_id:30s} {row.sha256[:12]}")
    print(f"\nwrote {len(CLAIMS)} claims to {REGISTRY}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
