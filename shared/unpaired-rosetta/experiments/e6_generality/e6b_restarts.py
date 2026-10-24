"""E6b part (2): multi-restart unpaired search on gen-pc0 (search-limited branch).

One job = one (corpus) running their WassersteinProcrustes (defaults, as E6) on gen with the top PC removed, at each
seed in `--seeds` (each seed is an independent restart of the whole init+refinement pipeline). Reports, per seed, the
pairs-free S1/S2 and the true-pair holdout FOSCTTM. Selection among restarts is by S1 ONLY (pairs-free); FOSCTTM is
evaluation only. Same split as E6. Seeds 0,1,2 are already measured (p3fast); default --seeds runs the new restarts
3-7, and selection is assembled over all available seeds in analysis. Frozen in PREREG_E6b.md section (2).

    uv run python -m e6_generality.e6b_restarts --corpus DOCCIDataset --seeds 3 4 5
"""

from __future__ import annotations

import argparse
from pathlib import Path

import torch

from common.rosetta import QWEN3_GEN_8B, VISION_B, fetch, receipt
from e5_scaffold_axis.gates import unpaired_scores
from e5_scaffold_axis.run import Deflated, principal_axes
from e6_generality.sweep import smoke_gate
from unpaired_rosetta import WassersteinProcrustes
from unpaired_rosetta.embeddings import load_rows, num_rows
from unpaired_rosetta.evaluation import disjoint_split, retrieval_metrics
from unpaired_rosetta.randomness import Randomness

OUT = Path(__file__).resolve().parents[1] / "results" / "e6_generality"
SHORT = {QWEN3_GEN_8B: "qwen3-8b-gen"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", required=True)
    parser.add_argument("--language", default=QWEN3_GEN_8B)
    parser.add_argument("--seeds", nargs="*", type=int, default=[3, 4, 5, 6, 7])
    parser.add_argument("--candidate", default="pc0")
    parser.add_argument("--holdout", type=int, default=2000)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--manifest-sha256", default="")
    args = parser.parse_args()
    kwargs = dict(num_workers=args.workers, num_threads=args.workers)

    path_x, path_y = fetch(args.corpus, "vision", VISION_B), fetch(args.corpus, "language", args.language)
    n = num_rows(path_x)
    val_idx = torch.arange(n - args.holdout, n)

    rows = []
    for seed in args.seeds:
        ix, iy = disjoint_split(n - args.holdout, Randomness(seed), None)
        sx, sy = load_rows(path_x, ix), load_rows(path_y, iy)
        vx, vy = load_rows(path_x, val_idx), load_rows(path_y, val_idx)
        if seed == args.seeds[0]:
            print("smoke gate:", smoke_gate(sx, sy, vx, vy), flush=True)
        k = int(args.candidate.removeprefix("pc"))
        basis = principal_axes(sy, k + 1)[:, [k]] if args.candidate != "none" else None
        model = Deflated(WassersteinProcrustes(**kwargs), basis).fit(sx, sy, Randomness(seed))
        row = {"corpus": args.corpus, "language": args.language, "candidate": args.candidate, "seed": seed,
               **unpaired_scores(model, sx, sy, seed),
               "foscttm_eval_only": retrieval_metrics(model, vx, vy, Randomness(seed))["foscttm"]}
        rows.append(row)
        print(row, flush=True)

    name = f"e6b_restarts-{args.corpus}-{SHORT.get(args.language, args.language)}-{args.candidate}-seeds"
    name += "-".join(map(str, args.seeds))
    config = {**vars(args), "vision": VISION_B, "aligner_kwargs": kwargs, "rows_available": n}
    print("receipt:", receipt(name, config, {"rows": rows}, OUT))


if __name__ == "__main__":
    main()
