# ARMT / RMT baseline for the clocked ledger — BABILong qa2@128k

Status: completed 2026-10-02. All runs on Beast via mrun (RTX 4080, fp32). `paper.md` not modified.
Code: `spf-wt-phaselock/domains/ml/memory-adapter-babilong/{armt_worker.py, armt_backends.py, diag_format.py, armt_vendor/}`,
commits `4d7ca149`, `02241e55` on `feat/phaselock` (not pushed).

## Question

Does the bound clocked ledger (qa2@128k 0.91–0.97) beat the actual BABILong state of the art, the
Recurrent Memory Transformer (RMT) and Associative RMT (ARMT), on the same documents?

## Distribution check

The ledger's E8b qa2@128k cell is standard BABILong qa2@128k: `ledger_worker7.py` calls
`load_babilong("qa2", "128k", limit=100)` on the unmodified `RMT-team/babilong` `data/qa2/128k.json`
(exactly 100 rows). "Held-out rooms" constrains the ledger writer's training vocabulary, not the
evaluation documents. ARMT and RMT therefore face no distribution shift; the "standard" and "E8b"
columns are the same 100 documents.

## Results (qa2@128k, n = 100, exact match, 95% bootstrap CI)

| method | published | reproduced here | regime |
|---|---:|---:|---|
| ARMT (145M) | **0.998** | 0.92 [0.86, 0.97] (`job-af86f09258e0`) | fine-tuned end-to-end on BABILong qa2 |
| **Clocked ledger, bound (E8b)** | — | **0.97 / 0.91 / 0.97** (seeds 17/29/43; mean 0.95) | frozen Qwen-1.5B + front end trained without test entities/rooms |
| RMT (137M) | 0.563 | 0.45 [0.35, 0.55] (`job-d6ea4882fcf3`) | fine-tuned end-to-end on BABILong qa2 |
| plain ledger (h2m1) | — | 0.57–0.61 | frozen Qwen-1.5B + ledger |
| long context / dense RAG | — | 0.24 / 0.11–0.14 | frozen Qwen-1.5B |

Published values: arXiv 2407.04841v1, Table 1 (ARMT 64k 1.000, 128k 0.998, 1M 0.994; RMT 64k 0.727,
128k 0.563, 1M 0.255). 1M was not reproduced.

## Verdict

- The ledger **loses to published ARMT** (0.95 vs 0.998).
- The ledger **ties the reproducible public ARMT checkpoint** (0.92; confidence intervals overlap).
- The ledger **beats RMT decisively** (0.563 published, 0.45 reproduced).
- Regime difference: ARMT and RMT are trained end-to-end on qa2 (in distribution); the ledger is a
  frozen 1.5B reader whose writer never saw the test entities or rooms.

## Reproduction detail

| backend / tokenization | qa2 64k | qa2 128k | qa1 128k |
|---|---:|---:|---:|
| ARMT per-sentence (faithful) | 0.90 [0.84, 0.96] | **0.92 [0.86, 0.97]** | 0.69 [0.60, 0.78] |
| ARMT whole-string | 0.77 [0.68, 0.85] | 0.78 [0.70, 0.86] | 0.53 [0.43, 0.63] |
| RMT whole-string (best) | 0.67 [0.58, 0.76] | **0.45 [0.35, 0.55]** | 0.43 [0.34, 0.53] |
| RMT per-sentence | 0.63 [0.53, 0.72] | 0.36 [0.27, 0.45] | 0.44 [0.35, 0.54] |

Ledger detail (`evidence/ledger-e8b-full.json`, seeds 17/29/43): qa2@128k 0.97/0.91/0.97, CIs
[0.93, 1.0] / [0.85, 0.96] / [0.93, 1.0]; plain 0.58/0.61/0.61. qa2@64k 0.97/0.91/0.97. qa1@128k
0.98/0.96/0.98.

### ARMT reproduction gap (0.92 vs published 0.998)

Ruled out (measured):
- transformers version: transformers 4.44.2 + torch 2.3.1 and transformers 5.13.1 + torch 2.13
  give bit-identical outputs (`job-a33144ba1028`, `job-5d34a871034d`);
- weight loading: the 204 duplicate ARMT keys are `torch.equal`; `missing_keys = 0`.

Localized: tokenization granularity. Training tokenizes each sentence separately; whole-string
tokenization is out of distribution. Format sweep (`job-bd0f1d554811`, n = 40): no GEN token 0.425,
whole-string + GEN 0.725, per-sentence + GEN 0.875. Per-sentence tokenization lifts ARMT 0.78 → 0.92.
The residual gap is most likely approximate sentence-boundary recovery (the public JSON is
pre-joined; boundaries were recovered by splitting on ". ") or a difference between the public
checkpoint and the paper's best run. RMT prefers whole-string tokenization.

## Provenance

- Checkpoints (≈0.82 GB total; Beast `/mnt/big` HF cache and `/mnt/usb-storage/armt-work/ckpts`):
  - `irodkin/armt_babilong_qa2` rev `1b2bbe4b746c82c29ea2cd463b4d9f5bc16e5ec0`, 530,956,177 B;
    num_mem_tokens 10, d_mem 64, n_heads 1, use_denom True, gating False.
  - `booydar/rmt-gpt2-babilong-qa2` rev `cbcc781d220bf97966b5d56acea729f4fd4f70d7`, 326,148,069 B;
    num_mem_tokens 16.
- Backbone: stock `gpt2` config and tokenizer (`from_config`); checkpoints supply all weights.
  Device CUDA, fp32, segment length 512, peak VRAM ~0.9–1.0 GB.
- Pinned environment: torch 2.3.1+cu121, transformers 4.44.2, tokenizers 0.19.1, numpy 1.26.4,
  CPython 3.11 at Beast `/mnt/usb-storage/armt-work/venv`.
- Vendored modeling: `RodkinIvan/associative-recurrent-memory-transformer` branch ACT, commit 786728c.
- Evaluation: `tokenize(context) + tokenize(question) + [GEN]`, greedy generation, official
  `compare_answers` (label-constrained over six rooms).
- Jobs: smoke `job-9c2b35f7adee`; whole-string `job-23c356882538` (ARMT), `job-d6ea4882fcf3` (RMT);
  pinned-environment confirmation `job-a33144ba1028`, `job-5d34a871034d`; format sweep
  `job-bd0f1d554811`; per-sentence `job-af86f09258e0` (ARMT), `job-4f97fcaf5c59` (RMT).

## Not verified

- The Hugging Face leaderboard qa2 cells (dynamic page).
- 1M-token reproduction (published values cited).
- Exact original sentence boundaries.
