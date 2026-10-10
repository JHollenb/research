"""E5c - a discovery-selected gate detector: choose which language axes to gate off without any true pair.

Origin: our spectral dimension ladder (spf-wt-phaselock/domains/ml/spectral-native/docs/v4-dimension-ladder-findings.md).
There, one learned gate per axis drove every nuisance-axis gate to exactly 0 (61/61 at N = 64). The gate was trained
on a supervised task loss, and small leftover gates were pruned by choosing the setting that scored best on
discovery data. Here no supervised loss exists. The only unpaired signal is the alignment itself, and gating inside
the fit is circular: E5's pseudo-pair detector kept the scaffold axis because the broken raw fit had already matched
the image's top axis onto it (pseudo-pair R^2 0.855 vs 0.16 on true pairs). So we port the ladder's second
mechanism, discovery selection. Each candidate gate setting gets its own fresh fit, and the setting is chosen by an
unpaired score of that fit on its own training rows.

One job = one (language, candidate) fit. Candidates: `none`, or `pc{k}` = gate off language PC k (k = 0..4,
estimated on the unpaired language training rows). Same protocol as run.py: their WassersteinProcrustes with
default settings, SPC minus the last 2,000 items for training, FOSCTTM on those 2,000. Scores, with no true pair:
  S1  mean cosine of Hungarian-matched pairs between the mapped vision and gated language training rows (their
      batched Hungarian, batch 10,000), i.e. how well one rotation makes the two clouds coincide as sets;
  S2  linear CKA over the first 4,096 matched pairs, i.e. relational agreement of the matching.
FOSCTTM uses true pairs and is evaluation only; it never enters the selection.

Predictions, frozen 2026-10-09 before any gates.py number was seen (the raw and pc0 FOSCTTM of all three models are
known from E5; S1 and S2 are not known for any candidate):
  G1  argmax-S1 selects pc0 for qwen3-8b-gen and none for qwen3-embedding-8b and mpnet.
  G2  the selected setting's FOSCTTM is within the seed-0 spread of the best candidate's FOSCTTM for each model
      (the selection does not leave a large gain on the table), read against the E5 seed spread once it lands.
  G3  the same holds for argmax-S2 (reported; a disagreement between S1 and S2 is a finding, not a failure).
Claim reading: G1 is the falsifier. If S1 prefers dropping a control's top PC, or keeps gen's, the unpaired gate
detector does not work in this form.

    uv run python -m e5_scaffold_axis.gates --language mpnet --candidate pc0
"""

from __future__ import annotations

import argparse
from pathlib import Path

import torch

from common.rosetta import QWEN3_GEN_8B, VISION_B, fetch, receipt
from e5_scaffold_axis.run import CORPUS, Deflated, principal_axes
from unpaired_rosetta import WassersteinProcrustes
from unpaired_rosetta import geometry as G
from unpaired_rosetta.assignment import batched_hungarian_matching
from unpaired_rosetta.embeddings import load_rows, num_rows
from unpaired_rosetta.evaluation import disjoint_split, retrieval_metrics
from unpaired_rosetta.linalg import center_and_normalize
from unpaired_rosetta.randomness import Randomness

OUT = Path(__file__).resolve().parents[1] / "results" / "e5_scaffold_axis"
SHORT = {QWEN3_GEN_8B: "qwen3-8b-gen"}


def unit(x: torch.Tensor) -> torch.Tensor:
    return x / x.norm(dim=1, keepdim=True).clamp_min(1e-12)


def unpaired_scores(model: Deflated, sx: torch.Tensor, sy: torch.Tensor, seed: int) -> dict:
    aligner = model.aligner
    x_hat = unit(center_and_normalize(sx.float(), aligner.mean_x) @ aligner.weight)
    y_hat = unit(center_and_normalize(model.project(sy.float()), aligner.mean_y))
    g = torch.Generator().manual_seed(seed)
    ox, oy = torch.randperm(len(x_hat), generator=g), torch.randperm(len(y_hat), generator=g)
    rows, cols = batched_hungarian_matching(x_hat[ox], y_hat[oy], 10_000)
    px, py = x_hat[ox[rows]], y_hat[oy[cols]]
    n = min(4096, len(px))
    return {
        "S1_matched_cosine": float((px * py).sum(dim=1).mean()),
        "S2_matched_linear_cka": float(G.cka((px[:n] - px[:n].mean(0)).double(), (py[:n] - py[:n].mean(0)).double())),
        "matched_pairs": int(len(px)),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--language", required=True)
    parser.add_argument("--candidate", required=True, help="none | pc{k}")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--holdout", type=int, default=2000)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    kwargs = dict(num_workers=args.workers, num_threads=args.workers)
    if args.smoke:
        kwargs.update(num_clusters=10, num_restarts=3, batch_size=1500, num_iterations=5)

    path_x, path_y = fetch(CORPUS, "vision", VISION_B), fetch(CORPUS, "language", args.language)
    n = num_rows(path_x)
    val_idx = torch.arange(n - args.holdout, n)
    ix, iy = disjoint_split(n - args.holdout, Randomness(args.seed), 3000 if args.smoke else None)
    sx, sy = load_rows(path_x, ix), load_rows(path_y, iy)
    vx, vy = load_rows(path_x, val_idx), load_rows(path_y, val_idx)

    basis = None
    if args.candidate != "none":
        k = int(args.candidate.removeprefix("pc"))
        basis = principal_axes(sy, k + 1)[:, [k]]
    model = Deflated(WassersteinProcrustes(**kwargs), basis).fit(sx, sy, Randomness(args.seed))
    row = {
        "language": args.language,
        "candidate": args.candidate,
        **unpaired_scores(model, sx, sy, args.seed),
        "foscttm_eval_only": retrieval_metrics(model, vx, vy, Randomness(args.seed))["foscttm"],
    }
    print(row, flush=True)
    name = f"e5_gates-{SHORT.get(args.language, args.language)}-{args.candidate}"
    name += (f"-seed{args.seed}" if args.seed else "") + ("-smoke" if args.smoke else "")
    config = {**vars(args), "vision": VISION_B, "corpus": CORPUS, "aligner_kwargs": kwargs}
    print("receipt:", receipt(name, config, {"row": row}, OUT))


if __name__ == "__main__":
    main()
