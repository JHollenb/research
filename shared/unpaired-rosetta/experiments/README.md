# Experiments for the response

Each experiment tests one claim in `../response.md`. Every scored number is computed with their library at the
pinned commit `fdfad84` (installed by `uv sync`), so a difference from their numbers can only come from the arm
we change. Results land in `results/<experiment>/` as JSON receipts. Each receipt holds the config, the numbers,
their commit, our commit and the software versions. Receipts with `-smoke` in the name check wiring only and
are never cited as results.

| id | claim | where it runs | status (2026-10-09) |
|---|---|---|---|
| E0 `e0_symbol_qap` | Their premise holds on our data: zero-pair QAP recovers the cross-model symbol table | laptop CPU, seconds; needs our private dump | **MEASURED** 18/18 (2,000 restarts + MPOpt) |
| E1 `e1_fidelity_gap` | D: FOSCTTM ≠ consumer-grade fidelity α; headroom decomposition (+ `d1_check.py`) | laptop CPU, ~25 min per unpaired fit | **MEASURED** (`e1_fidelity_gap-20261009T200203.json`): ours-p0/p10/p100 median α 0.527/0.473/0.507; orth-oracle 0.572, lin-oracle 0.781 at equal FOSCTTM; E1b `d1_check.py` not run |
| E2 `e2_span_bound` | C + E: span ceiling of pair baselines; vision-side medoid pairs raise it | laptop CPU; `ours` only at p ∈ {5, 20} | queued after E1; E2b `draws.py` (seeds 1–5, baselines only) queued after E2 |
| E3 `e3_pooling_scaffold` | A + B: generative-pooling scaffold; commit-layer depth | mrun (CUDA), ~12 min | **MEASURED** (`job-9426423166f5`, `job-5fd45e7c7f0d`): A refuted on effect sign; B supported in direction, small (PREREG Amendment 3) |
| E5 `e5_scaffold_axis` | A\* (post-hoc): a non-visual axis in Qwen3-gen embeddings; an unpaired detector removes it | laptop CPU (`axis_probe.py` seconds; `run.py` ~1 h) | probe **MEASURED**; gen fix 0.415 ± 0.055 → 0.038 ± 0.006 (3 seeds); controls wrecked by the same drop; pseudo-pair detector failed; **gate detector `gates.py` selects correctly in 9/9 encoder × seed cases** |
| E4 `e4_consumer_closure` | D on a real generator with causal ground truth (FLUX.2 Klein 4B) | mrun (CUDA) | design only |

## Seeds on the fleet

`seeds/submit.py` reruns E1 and E5 at seeds 0–4, the E2b draw spread, and the D1 check at seeds 0–4 on Beast, 26
jobs (`--plan full`, then `--collect`). Beast uses a venv provisioned once at `/mnt/usb-storage/unpaired-rosetta/venv-sys`:
its existing torch 2.13 env plus their library (fdfad84) and pylibmgm, with embeddings pre-copied. Parity check:
the Beast smoke matches the laptop smoke to 1e-6 FOSCTTM on all three arms, despite torch 2.13 vs 2.14 and
Python 3.14 vs 3.12 (`results/e5_scaffold_axis/*smoke*`). At full scale the hosts differ: Qwen3-gen at seed 0
gives raw 0.407 on the laptop vs 0.419 on Beast, and drop-top-PC 0.036 vs 0.033 (`e5_gates-qwen3-8b-gen-{none,pc0}`).
Read this as fit noise, comparable to seed noise. Compare arms within one host.

## Setup

```bash
cd research/shared/unpaired-rosetta/experiments
UV_PYTHON_PREFERENCE=only-managed uv sync --python 3.12     # their library + pylibmgm (MPOpt)
```

Embeddings are downloaded on first use from their Hugging Face dataset
(`schnaus/unpaired-rosetta-embeddings`) into `.storage/`. That directory is gitignored. The COCO DINOv2-B and
MPNet files total 1.4 GB.

## Run

```bash
uv run python -m e0_symbol_qap.run            # --dump <report.json>; default = our Saturn receipt
uv run python -m e1_fidelity_gap.run          # --smoke for a wiring check
uv run python -m e2_span_bound.run
uv run python -m e3_pooling_scaffold.prepare  # builds payload/ (captions + their stored rows), 13 MB
~/domains/common/bin/common exec python e3_pooling_scaffold/submit.py            # mrun
~/domains/common/bin/common exec python e3_pooling_scaffold/submit.py --collect job-XXXX
```

`e3_pooling_scaffold/worker.py` also runs without mrun: `python worker.py --data payload --device cuda`, in any
env with torch and transformers.

## Figures

`~/domains/common/bin/common exec python experiments/figures/make_figures.py` (from the project folder; needs
matplotlib) rebuilds `../figures/*.png` from the receipts alone.

## TODO

- **mrun-pub:** E3 and E4 submit through the private fleet client (`mrun.client.submit.launch`). Port both
  submitters to the public `mrun-pub` package so readers outside our fleet can rerun them.
- **Public FLUX path for E4:** the consumer test reuses the private Saturn symbol-table worker. Move it to
  `saturn-pub` (and `mdb` for retained branches) once the FLUX adapter is public.
- **Public E0 input:** the symbol-table dump is a private Saturn receipt. Publish the fp16 displacement
  matrices (108 rows × 2 spaces, about 2 MB) next to these scripts.
- **Qwen3-8B for E3:** the 8B files need a paged or int8 path on the 16 GB card.

## Provenance

- **Their code:** `github.com/dominik-schnaus/unpaired-rosetta`, MIT. Commit `fdfad84` was read on
  2026-10-09.
- **Vendored file:** `e3_pooling_scaffold/their_geometry.py` is their `geometry.py`, verbatim plus a header
  line. It is vendored because the GPU worker does not install their package.
