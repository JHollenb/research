"""E6b part (3): drop-k FOSCTTM ladder under their aligner (geometry-limited branch).

One job = one (corpus, language). Fits their WassersteinProcrustes (defaults, as E6) with the top k language PCs
projected out (basis = principal_axes(sy, k), first k columns, estimated on the unpaired training half -- E6's gate),
for each k in `--ks`. k=0 is `none`, k=1 is `pc0`. Reports pairs-free S1/S2 and true-pair holdout FOSCTTM per k.
Same split as E6 (train on the two disjoint halves of corpus minus the last `holdout`; FOSCTTM on those `holdout`).
Seed 0. Frozen in PREREG_E6b.md section (3). k=0,1 at seed 0 are already measured (p3fast); default --ks runs the new
rungs 2,3,4 and the ladder is assembled with those anchors.

    uv run python -m e6_generality.e6b_ladder --corpus DOCCIDataset --ks 2 3 4
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


def basis_for_k(sy: torch.Tensor, k: int) -> torch.Tensor | None:
    return None if k == 0 else principal_axes(sy, k)  # first k PCs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", required=True)
    parser.add_argument("--language", default=QWEN3_GEN_8B)
    parser.add_argument("--ks", nargs="*", type=int, default=[2, 3, 4])
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--holdout", type=int, default=2000)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--manifest-sha256", default="")
    args = parser.parse_args()
    kwargs = dict(num_workers=args.workers, num_threads=args.workers)

    path_x, path_y = fetch(args.corpus, "vision", VISION_B), fetch(args.corpus, "language", args.language)
    n = num_rows(path_x)
    val_idx = torch.arange(n - args.holdout, n)
    ix, iy = disjoint_split(n - args.holdout, Randomness(args.seed), None)
    sx, sy = load_rows(path_x, ix), load_rows(path_y, iy)
    vx, vy = load_rows(path_x, val_idx), load_rows(path_y, val_idx)

    smoke = smoke_gate(sx, sy, vx, vy)
    print("smoke gate:", smoke, flush=True)

    rows = []
    for k in args.ks:
        basis = basis_for_k(sy, k)
        model = Deflated(WassersteinProcrustes(**kwargs), basis).fit(sx, sy, Randomness(args.seed))
        row = {"corpus": args.corpus, "language": args.language, "drop_k": k,
               **unpaired_scores(model, sx, sy, args.seed),
               "foscttm_eval_only": retrieval_metrics(model, vx, vy, Randomness(args.seed))["foscttm"]}
        rows.append(row)
        print(row, flush=True)

    name = f"e6b_ladder-{args.corpus}-{SHORT.get(args.language, args.language)}-k" + "-".join(map(str, args.ks))
    name += f"-seed{args.seed}" if args.seed else ""
    config = {**vars(args), "vision": VISION_B, "aligner_kwargs": kwargs, "rows_available": n, "smoke_gate": smoke}
    print("receipt:", receipt(name, config, {"rows": rows}, OUT))


if __name__ == "__main__":
    main()
