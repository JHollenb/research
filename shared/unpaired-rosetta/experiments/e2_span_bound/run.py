"""E2 - the span ceiling of pair-based maps, and pairs chosen to raise it (response.md, Claim C and Claim E).

Lemma C1 (exact): their ``linear`` baseline maps every query into span(Y_hat_p), so its score for a key depends on
the key only through its projection P_p y. Lemma C2 (Ky Fan + Cauchy-Schwarz): any map whose image lies in a
p-dim span has  E_i cos(map(x_i), y_i) <= sqrt(E_i ||P_p y_i||^2) <= sqrt(sum_{k<=p} lambda_k / sum_k lambda_k).

For p in a pair ladder this script measures, on the validation keys:
  energy_random   E||P_p y||^2 for their random pair draw (their sample_pairs)
  energy_kyfan    the Ky Fan ceiling for p dims (no p-dim span can do better)
  oracle_foscttm  FOSCTTM when each key's own projection is its query (natural best query in the span)
  linear/orthogonal/ours FOSCTTM and mean alpha with their random pairs
and the same with pairs chosen on the vision side only (k-means medoids of the unpaired images), which needs no
caption knowledge: choosing which images to caption is a free design decision in the few-pair setting.

Smoke:  python -m e2_span_bound.run --smoke
"""

from __future__ import annotations

import argparse
from pathlib import Path

import torch
from sklearn.cluster import KMeans

from common.rosetta import (
    VISION_B,
    ProjectionOracle,
    alpha,
    captured_energy,
    fetch,
    receipt,
    span_basis,
    top_eigen_energy,
    training_data,
    validation_data,
)
from unpaired_rosetta import WassersteinProcrustes
from unpaired_rosetta.baselines.linear import LinearMap
from unpaired_rosetta.baselines.orthogonal import OrthogonalMap
from unpaired_rosetta.embeddings import load_rows, num_rows
from unpaired_rosetta.evaluation import retrieval_metrics
from unpaired_rosetta.linalg import center_and_normalize
from unpaired_rosetta.randomness import Randomness

OUT = Path(__file__).resolve().parents[1] / "results" / "e2_span_bound"


def medoid_pairs(dataset: str, p: int, seed: int, pool_size: int = 20_000) -> torch.Tensor:
    """Indices of ``p`` images nearest to k-means centers of a random image pool (vision side only)."""
    path = fetch(dataset, "vision", VISION_B)
    pool = torch.randperm(num_rows(path), generator=torch.Generator().manual_seed(seed + 7919))[:pool_size]
    images = load_rows(path, pool)
    centers = KMeans(n_clusters=p, n_init=3, random_state=seed).fit(images.numpy()).cluster_centers_
    nearest = torch.cdist(torch.as_tensor(centers, dtype=images.dtype), images).argmin(dim=1)
    return pool[torch.unique(nearest)]


def evaluate_arms(sx, sy, px, py, val_x, val_y, seed, ours_kwargs, with_ours: bool) -> dict:
    out = {}
    arms = [("linear", LinearMap()), ("orthogonal", OrthogonalMap())]
    if with_ours:  # their aligner costs ~25 min per fit on full COCO; run it only where Claim C-iii needs it
        arms.append(("ours", WassersteinProcrustes(**ours_kwargs)))
    for name, aligner in arms:
        aligner.fit(sx, sy, px, py, Randomness(seed))
        keys = center_and_normalize(val_y.float(), aligner.mean_y)
        if hasattr(aligner, "transform"):
            query = aligner.transform(val_x)
        else:
            query = center_and_normalize(val_x.float(), aligner.mean_x) @ aligner.weight
        out[name] = {
            "foscttm": retrieval_metrics(aligner, val_x, val_y, Randomness(seed))["foscttm"],
            "alpha_mean": float(alpha(query, keys).mean()),
        }
    return out


def span_numbers(py, sy, val_y, p, seed) -> dict:
    mean_y = sy.mean(dim=0, keepdim=True)
    basis = span_basis(center_and_normalize(py.float(), mean_y))
    keys = center_and_normalize(val_y.float(), mean_y)
    oracle = ProjectionOracle(basis, mean_y)
    return {
        "span_rank": int(basis.shape[1]),
        "energy": float(captured_energy(keys, basis).mean()),
        "energy_kyfan": top_eigen_energy(keys, p),
        "oracle_foscttm": retrieval_metrics(oracle, val_y, val_y, Randomness(seed))["foscttm"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--language", default="mpnet")
    parser.add_argument("--train", default="coco_train2014")
    parser.add_argument("--validation", default="coco_val2014")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--pairs", type=int, nargs="*", default=[1, 2, 5, 10, 20, 50, 100, 200, 500, 1000])
    parser.add_argument("--selection", nargs="*", default=["random", "medoid"])
    parser.add_argument("--train-size", type=int, default=None)
    parser.add_argument("--validation-size", type=int, default=None)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--ours-pairs", type=int, nargs="*", default=[5, 20])
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    ours_kwargs = dict(num_workers=args.workers, num_threads=args.workers)
    if args.smoke:
        args.train_size, args.validation_size, args.pairs = 3000, 2000, [5, 20]
        ours_kwargs.update(num_clusters=10, num_restarts=3, batch_size=1500, num_iterations=5)

    val_x, val_y, _ = validation_data(args.validation, VISION_B, args.language, args.seed, args.validation_size)
    rows = []
    for selection in args.selection:
        for p in args.pairs:
            randomness = Randomness(args.seed)
            if selection == "random":
                sx, sy, px, py = training_data(args.train, VISION_B, args.language, randomness, args.train_size, p)
            else:
                indices = medoid_pairs(args.train, p, args.seed, pool_size=5000 if args.smoke else 20_000)
                sx, sy, px, py = training_data(
                    args.train, VISION_B, args.language, randomness, args.train_size, pair_indices=indices
                )
            row = {"selection": selection, "p": p, **span_numbers(py, sy, val_y, p, args.seed)}
            row.update(evaluate_arms(sx, sy, px, py, val_x, val_y, args.seed, ours_kwargs, p in args.ours_pairs))
            rows.append(row)
            print(row, flush=True)

    config = {**vars(args), "vision": VISION_B, "ours_kwargs": ours_kwargs}
    print("receipt:", receipt("e2_span_bound" + ("-smoke" if args.smoke else ""), config, {"rows": rows}, OUT))


if __name__ == "__main__":
    main()
