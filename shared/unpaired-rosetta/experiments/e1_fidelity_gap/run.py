"""E1 - fidelity gap: does a good FOSCTTM imply a map good enough to *drive* a consumer? (response.md, Claim D)

For each aligner we report FOSCTTM (their metric, their code) next to the distribution of the per-pair fidelity
``alpha_i = cos(map(x_i), y_i)`` on the same validation pairs. Arms:

  ours-p0       their WassersteinProcrustes, no pairs (the paper's headline setting)
  ours-p{k}     the same with k known pairs (their few-pair protocol)
  orth-oracle   orthogonal Procrustes on N true training pairs: the best any single rotation can do here
  lin-oracle    least squares on N true training pairs: drops the orthogonality constraint

The oracles give the headroom decomposition  alpha(ours-p0) <= alpha(orth-oracle) <= alpha(lin-oracle) <= 1:
the first gap is what unpaired estimation costs, the second what the orthogonal constraint costs, the last what any
linear map costs. Smoke:  python -m e1_fidelity_gap.run --smoke
"""

from __future__ import annotations

import argparse
from pathlib import Path

import torch

from common.rosetta import VISION_B, alpha, quantiles, receipt, training_data, validation_data
from unpaired_rosetta import WassersteinProcrustes
from unpaired_rosetta.baselines.linear import LinearMap
from unpaired_rosetta.baselines.orthogonal import OrthogonalMap
from unpaired_rosetta.evaluation import retrieval_metrics
from unpaired_rosetta.linalg import center_and_normalize
from unpaired_rosetta.randomness import Randomness

OUT = Path(__file__).resolve().parents[1] / "results" / "e1_fidelity_gap"
# Reference zones measured on the FLUX.2 Klein 4B conditioner (Wall A, research/bfl): >= 0.895 rendered 8/8,
# <= 0.50 failed. They are consumer-specific and are reported only as a reference scale, not as a claim about RAE.
FLUX_RENDERS, FLUX_FAILS = 0.895, 0.50


def mapped(aligner, queries: torch.Tensor) -> torch.Tensor:
    if hasattr(aligner, "transform"):
        return aligner.transform(queries)
    return center_and_normalize(queries.float(), aligner.mean_x) @ aligner.weight


def score(name: str, aligner, val_x, val_y, seed: int) -> dict:
    metrics = retrieval_metrics(aligner, val_x, val_y, Randomness(seed))
    keys = center_and_normalize(val_y.float(), aligner.mean_y)
    a = alpha(mapped(aligner, val_x), keys)
    # Mean similarity of a mapped query to the *other* keys, on a 2,000-query sample: the distractor level that
    # FOSCTTM compares alpha against.
    sample = torch.randperm(val_x.shape[0], generator=torch.Generator().manual_seed(seed))[:2000]
    sims = torch.nn.functional.normalize(mapped(aligner, val_x[sample]).double(), dim=-1) @ keys.double().T
    off = sims.clone()
    off[torch.arange(len(sample)), sample] = float("nan")
    return {
        "arm": name,
        "foscttm": metrics["foscttm"],
        "alpha": quantiles(a),
        "distractor_mean": float(torch.nanmean(off)),
        "distractor_q99": float(torch.nanquantile(off.flatten()[~off.flatten().isnan()][:2_000_000], 0.99)),
        "share_alpha_ge_flux_renders": float((a >= FLUX_RENDERS).double().mean()),
        "share_alpha_le_flux_fails": float((a <= FLUX_FAILS).double().mean()),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--language", default="mpnet")
    parser.add_argument("--train", default="coco_train2014")
    parser.add_argument("--validation", default="coco_val2014")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--pairs", type=int, nargs="*", default=[10, 100])
    parser.add_argument("--oracle-pairs", type=int, default=20_000)
    parser.add_argument("--train-size", type=int, default=None)
    parser.add_argument("--validation-size", type=int, default=None)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--smoke", action="store_true", help="tiny sizes, checks wiring only (not a result)")
    args = parser.parse_args()
    if args.smoke:
        args.train_size, args.validation_size, args.oracle_pairs, args.pairs = 3000, 2000, 2000, [10]
    ours_kwargs = dict(num_workers=args.workers, num_threads=args.workers)
    if args.smoke:
        ours_kwargs.update(num_clusters=10, num_restarts=3, batch_size=1500, num_iterations=5)

    val_x, val_y, _ = validation_data(args.validation, VISION_B, args.language, args.seed, args.validation_size)
    rows = []
    for p in [0, *args.pairs]:
        randomness = Randomness(args.seed)
        sx, sy, px, py = training_data(args.train, VISION_B, args.language, randomness, args.train_size, p)
        aligner = WassersteinProcrustes(**ours_kwargs).fit(sx, sy, px, py, randomness)
        rows.append(score(f"ours-p{p}", aligner, val_x, val_y, args.seed))
        print(rows[-1], flush=True)

    randomness = Randomness(args.seed)
    sx, sy, px, py = training_data(args.train, VISION_B, args.language, randomness, args.train_size, args.oracle_pairs)
    for name, cls in (("orth-oracle", OrthogonalMap), ("lin-oracle", LinearMap)):
        rows.append(score(name, cls().fit(sx, sy, px, py), val_x, val_y, args.seed))
        print(rows[-1], flush=True)

    config = {**vars(args), "vision": VISION_B, "ours_kwargs": ours_kwargs}
    name = "e1_fidelity_gap" + (f"-seed{args.seed}" if args.seed else "") + ("-smoke" if args.smoke else "")
    print("receipt:", receipt(name, config, {"arms": rows}, OUT))


if __name__ == "__main__":
    main()
