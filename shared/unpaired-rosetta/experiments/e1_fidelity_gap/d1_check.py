"""E1b - Proposition D1 check: predict FOSCTTM from the fidelity alpha and the residual's effective dimension.

For a map q_i = alpha_i y_i + beta_i u_i (u_i unit, orthogonal to y_i), Prop. D1 predicts
    P(j outranks i) ~= Phi_bar( (alpha_i / beta_i) * sqrt((d_eff - 1)(1 - c_ij) / (1 + c_ij)) ),
with c_ij = <y_i, y_j> and d_eff the participation ratio of the residual directions u. We fit the two
closed-form oracle maps (orthogonal and least squares on N true pairs, cheap) and their method with p pairs
(optional, slow), then compare predicted with measured FOSCTTM on the same validation queries.

    uv run python -m e1_fidelity_gap.d1_check [--with-ours]
"""

from __future__ import annotations

import argparse
from pathlib import Path

import torch

from common.rosetta import VISION_B, receipt, training_data, validation_data
from e1_fidelity_gap.run import mapped
from unpaired_rosetta import WassersteinProcrustes
from unpaired_rosetta.baselines.linear import LinearMap
from unpaired_rosetta.baselines.orthogonal import OrthogonalMap
from unpaired_rosetta.evaluation import retrieval_metrics
from unpaired_rosetta.linalg import center_and_normalize
from unpaired_rosetta.randomness import Randomness

OUT = Path(__file__).resolve().parents[1] / "results" / "e1_fidelity_gap"


def predicted_foscttm(q: torch.Tensor, y: torch.Tensor, queries: int, seed: int) -> dict:
    q = torch.nn.functional.normalize(q.double(), dim=-1)
    y = torch.nn.functional.normalize(y.double(), dim=-1)
    a = (q * y).sum(-1).clamp(-0.999999, 0.999999)
    b = (1 - a**2).sqrt()
    u = (q - a[:, None] * y) / b[:, None]
    cov = (u.T @ u) / u.shape[0]
    d_eff = float(torch.trace(cov) ** 2 / torch.trace(cov @ cov))
    idx = torch.randperm(q.shape[0], generator=torch.Generator().manual_seed(seed))[:queries]
    c = (y[idx] @ y.T).clamp(-0.999999, 0.999999)
    z = (a[idx] / b[idx])[:, None] * ((d_eff - 1) * (1 - c) / (1 + c)).sqrt()
    p = 0.5 * torch.erfc(z / 2**0.5)
    p[torch.arange(len(idx)), idx] = float("nan")
    # measured on the same queries, by direct ranking
    s = q[idx] @ y.T
    true = s[torch.arange(len(idx)), idx]
    beats = (s > true[:, None]).double()
    beats[torch.arange(len(idx)), idx] = float("nan")
    return {"d_eff": d_eff, "alpha_median": float(a.median()), "pred_foscttm": float(torch.nanmean(p)),
            "measured_foscttm_same_queries": float(torch.nanmean(beats)),
            "empirical_var_u_dot_y": float(torch.var((u[idx] @ y.T)[~beats.isnan()])),
            "model_var_u_dot_y": float(torch.nanmean((1 - c**2) / (d_eff - 1)))}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--language", default="mpnet")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--pairs", type=int, nargs="*", default=[20, 200, 2000, 20000])
    parser.add_argument("--queries", type=int, default=2000)
    parser.add_argument("--with-ours", action="store_true")
    args = parser.parse_args()
    val_x, val_y, _ = validation_data("coco_val2014", VISION_B, args.language, args.seed)
    rows = []
    for p in args.pairs:
        randomness = Randomness(args.seed)
        sx, sy, px, py = training_data("coco_train2014", VISION_B, args.language, randomness, None, p)
        arms = [("orth", OrthogonalMap()), ("lin", LinearMap())]
        if args.with_ours:
            arms.append(("ours", WassersteinProcrustes(num_workers=4, num_threads=4)))
        for name, aligner in arms:
            aligner.fit(sx, sy, px, py, Randomness(args.seed))
            keys = center_and_normalize(val_y.float(), aligner.mean_y)
            row = {"arm": name, "p": p, **predicted_foscttm(mapped(aligner, val_x), keys, args.queries, args.seed),
                   "foscttm_full": retrieval_metrics(aligner, val_x, val_y, Randomness(args.seed))["foscttm"]}
            rows.append(row)
            print(row, flush=True)
    print("receipt:", receipt("e1_d1_check" + (f"-seed{args.seed}" if args.seed else ""), vars(args), {"rows": rows}, OUT))


if __name__ == "__main__":
    main()
