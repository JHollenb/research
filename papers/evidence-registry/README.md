# Submission evidence claim registry

This directory is a [saturn-pub](../../../saturn-pub) **evidence claim registry**: one
append-only, hash-chained JSONL ledger (`claims.jsonl`) that binds every headline
number in the four submitted papers to the exact receipt file on disk that carries
it. Each claim fingerprints the receipt's bytes; `verify` re-hashes them and flips any
claim whose receipt has drifted to `stale`, so a stale number can never keep
presenting itself as current evidence.

- `claims.jsonl` — the ledger (13 claims). Append-only and hash-chained.
- `claims.jsonl.head` — sidecar head pointer guarding against silent tail truncation.
- `build_registry.py` — the reproducible build (re-creates `claims.jsonl` from the receipts).

Everything in `saturn_pub.evidence` is standard-library only and loads no model, so
`verify` runs offline on a laptop in well under a second.

## Run verify (what a reader runs)

From the `saturn-pub` repository (it owns the `saturn-pub` CLI):

```bash
cd /Users/jakeholl/domains/saturn-pub
./.venv/bin/saturn-pub evidence claims verify --check \
  --registry /Users/jakeholl/domains/research/papers/evidence-registry/claims.jsonl
# clean: checked=13 still_valid=13 newly_stale=0 restored=0 unresolvable=0 chain_ok=True  (exit 0)
```

`--check` is read-only (it never writes to the ledger): **exit 0** = all claims valid,
**3** = drift / newly-stale detected, **2** = hash chain broken. Drop `--check` to let
`verify` append a `stale` row for each drifted claim (exit 0 chain ok, 1 chain broken).

List the current claims, or the full history of one:

```bash
./.venv/bin/saturn-pub evidence claims list    --registry .../claims.jsonl
./.venv/bin/saturn-pub evidence claims history pib-r0-drift-r2-flips-base --registry .../claims.jsonl
```

To rebuild from scratch (receipts unchanged): delete `claims.jsonl` and `claims.jsonl.head`,
then `/Users/jakeholl/domains/saturn-pub/.venv/bin/python build_registry.py`.

## Claim IDs by paper and table

### time-formed-circuits
| claim id | covers | receipt |
|---|---|---|
| `tfc-e20-xfam-table2` | Table 2 cross-family cells (Qwen2.5-1.5B pub + held-out, Gemma-2-2B, SmolLM2-1.7B) | `2026-10-02-e20-cross-family/results/analysis.json` |
| `tfc-e20-nonqwen-table2` | Table 2 blind-band rows (OLMo-2-1B, Pythia-1.4B, Phi-2, GPT-2 XL) | `2026-10-05-e20-nonqwen-families/results/analysis.json` |
| `tfc-p1b-clustered-ci-table2` | Table 2 identity-clustered 95% bootstrap CIs | `2026-10-02-p1-reviewer-experiments/results/B_clustered_stats.json` |
| `tfc-p1c-e6-interchange-fig4` | §5 / Fig 4 feature+error interchange (identity 0.31, color 0.99) | `2026-10-02-p1-reviewer-experiments/results/C_analysis.json` |
| `tfc-e6-native-kv-cut` | §5 native key/value cut 0.94 | `2026-09-30-full-layer-sweeps/results/gemma2-ed4ce1ac5974/report.json` |
| `tfc-breakit-operation-general` | §8.1 operation-general frozen L22-27 band | `2026-10-02-break-it-r2/results/breakit-r2-qwen15base-6c46852af315/report.json` |

### pass-indexed-baseline
| claim id | covers | receipt |
|---|---|---|
| `pib-r0-drift-r2-flips-base` | §3 R0 drift (+3.125/+2.202/+2.063 nats) and §5 R2 11/12 flips | `2026-10-02-pass-indexed-baseline/results/pass-indexed-35d4adaeed36/analysis.json` |
| `pib-instruct15b-raw` | §6 table, Qwen2.5-1.5B-Instruct raw (9/12 flips) | `2026-10-05-pass-indexed-instruct-7b/results/q15i_raw_full-23194c4f1d09/analysis.json` |
| `pib-instruct15b-chat` | §6 table, Qwen2.5-1.5B-Instruct chat (0/12 flips) | `2026-10-05-pass-indexed-instruct-7b/results/q15i_chat_full-2e4198b3de14/analysis.json` |
| `pib-instruct7b-raw-bf16` | §6 table, Qwen2.5-7B-Instruct raw (4/12 flips) | `2026-10-05-pass-indexed-instruct-7b/results/q7i_raw_full_bf16-8243f04af7c7/analysis.json` |
| `pib-instruct7b-chat-bf16` | §6 table, Qwen2.5-7B-Instruct chat (0/12 flips) | `2026-10-05-pass-indexed-instruct-7b/results/q7i_chat_full_bf16-1d9876bd8f78/analysis.json` |

### instrument-audit-interpbench
| claim id | covers | receipt |
|---|---|---|
| `iai-node-auroc-84models` | §5.1 / §5.3 / §5.4 node-level AUROC (84 models) and preregistered verdicts | `2026-10-05-interpbench-method-audit/results/full.json` |

### pointwise-instruments-miss-distributed-circuits
| claim id | covers | receipt |
|---|---|---|
| `pim-prereg-panel-sae-v2` | §4.3 preregistered panel + §4.4 SAE arms (rerun v2) | `research/papers/pointwise-instruments-miss-distributed-circuits/experiments/2026-09-22-sae-comparison/results/combined_summary_v2.json` |

## Notes on two receipts

- **InterpBench `full.json` has a JSON-array root.** `ingest_receipt` requires an
  object root (it captures top-level `content_sha256`/`config_sha256`/`gates`), so it
  rejects an array-rooted file. `iai-node-auroc-84models` is therefore registered
  through the same public `DependencyFingerprint` / `ClaimRow` / `ClaimsRegistry.append`
  API, fingerprinting the identical file bytes. `verify` treats it exactly like every
  other `file`-kind entry — a byte change to `full.json` makes the claim `stale`.
- **The pointwise receipt was not in the custody handoff list.** The pointwise paper's
  headline numbers come from its own `experiments/2026-09-22-sae-comparison/` (cited in
  that paper's §8), not from the `saturn/experiments/…` receipts that cover the other
  three papers. `pim-prereg-panel-sae-v2` points at `combined_summary_v2.json` so the
  pointwise table is covered by a claim id; this is the one receipt here outside the
  handoff list.


## Appended 2026-10-05 (late)

`append_2026-10-05_late.py` adds five claims (registry now 18, verify 18/18): `tfc-e20-causal-band-table2` (time-formed-circuits causal-band rows / Fig 7), and `pib-chat-unsat-referential`, `pib-chat-unsat-05b`, `pib-chat-unsat-distractor`, `pib-chat-unsat-p3-spearman` (pass-indexed-baseline §6 chat cells).

`append_2026-10-05_interpbench_real.py` adds `iai-real-generator-noemb-84models` (instrument-audit §5.1 real-generator primary table; array-rooted receipt, fingerprint path). Registry now 19.
