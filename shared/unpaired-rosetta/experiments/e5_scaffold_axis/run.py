"""E5 - a non-visual scaffold axis in generative pooling, and an unpaired detector that removes it.

Context (post-hoc, 2026-10-09, after E3): their stored Qwen3-8B-gen embeddings of SPC put 13.8% of variance on one
principal axis that the image embedding barely predicts (held-out R^2 0.17, vs 0.88-0.89 for the top axis of
MPNet and Qwen3-Embedding). Projecting it out raises linear CKA with DINOv2 from 0.433 to 0.583, and the same
operation lowers CKA for MPNet (0.633 -> 0.466) and Qwen3-Embedding (0.657 -> 0.498). That is Lemma A1 behavior.

This experiment asks whether the CKA gain becomes an alignment gain under their aligner, and whether the axis
can be found WITHOUT pairs. Protocol: their WassersteinProcrustes with default hyperparameters; train on the two
disjoint halves of SPC minus a holdout; FOSCTTM on the last 2,000 SPC items (their `holdout` option; their paper
validates SPC-trained maps on COCO val instead, which would need the 14 GB COCO 8B-gen file).

Arms, per language model in {qwen3-8b-gen, qwen3-embedding-8b, mpnet}:
  raw         their pipeline unchanged
  drop1       project the top principal axis of the (unpaired) language training set out of every language row
  detector    unpaired: fit raw, take its Hungarian pseudo-pairs on the training sets, regress each of the top-10
              language PCs on the mapped vision rows (ridge, 2-fold on pseudo-pairs), drop every PC with R^2 < 0.3,
              refit. No true pair is used anywhere.

Predictions, frozen before any FOSCTTM from this script was seen:
  P5a  drop1 lowers FOSCTTM for qwen3-8b-gen and raises it for mpnet and qwen3-embedding-8b.
  P5b  the detector drops the top PC for qwen3-8b-gen and does not drop the top PC for the other two.
  P5c  the detector's FOSCTTM <= raw for all three models (it never hurts), and < raw for qwen3-8b-gen.

Scoring amendment (2026-10-09). Written after seeing raw and drop1 for qwen3-8b-gen (0.407 -> 0.036), and before
any detector, mpnet or qwen3-embedding-8b number. P5a and P5c compare single fits with strict inequalities, so a
noise-level change would decide them. A change now counts as a direction only when |delta FOSCTTM| exceeds twice
the seed SD of that model's raw arm (seeds 0, 1, 2: `--arms raw --seed 1|2`). A smaller change is reported as "no
detectable change", which for P5c is "does not hurt". The R^2 < 0.3 cut in the detector is a method setting, not a
verdict bar; the receipt keeps every PC's R^2, so any other cut can be re-scored.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import torch

from common.rosetta import QWEN3_GEN_8B, VISION_B, fetch, receipt
from unpaired_rosetta import WassersteinProcrustes
from unpaired_rosetta.assignment import batched_hungarian_matching
from unpaired_rosetta.embeddings import load_rows, num_rows
from unpaired_rosetta.evaluation import disjoint_split, retrieval_metrics
from unpaired_rosetta.linalg import center_and_normalize
from unpaired_rosetta.randomness import Randomness

OUT = Path(__file__).resolve().parents[1] / "results" / "e5_scaffold_axis"
CORPUS = "StanfordParagraphCaptioning"
LANGUAGES = (QWEN3_GEN_8B, "qwen3-embedding-8b", "mpnet")


class Deflated:
    """Wrap an aligner so the language side has fixed directions projected out (estimated on training rows)."""

    def __init__(self, aligner, basis: torch.Tensor | None) -> None:
        self.aligner, self.basis = aligner, basis
        self.mean_y = None

    def project(self, y: torch.Tensor) -> torch.Tensor:
        if self.basis is None:
            return y
        return y - (y @ self.basis) @ self.basis.T

    def fit(self, sx, sy, randomness):
        self.aligner.fit(sx, self.project(sy), None, None, randomness)
        self.mean_y = self.aligner.mean_y
        return self

    def similarity(self, queries_x, keys_y):
        return self.aligner.similarity(queries_x, self.project(keys_y))


def principal_axes(y: torch.Tensor, k: int) -> torch.Tensor:
    centered = (y - y.mean(0)).double()
    _, _, vt = torch.linalg.svd(centered, full_matrices=False)
    return vt[:k].T.float()  # [d, k]


def detector(aligner, sx, sy, k: int, threshold: float, seed: int) -> tuple[list[int], list[float]]:
    """Language PCs that the mapped vision side cannot predict, using pseudo-pairs only."""
    x_hat = center_and_normalize(sx.float(), aligner.mean_x) @ aligner.weight
    y_hat = center_and_normalize(sy.float(), aligner.mean_y)
    g = torch.Generator().manual_seed(seed)
    ox, oy = torch.randperm(len(x_hat), generator=g), torch.randperm(len(y_hat), generator=g)
    rows, cols = batched_hungarian_matching(x_hat[ox], y_hat[oy], 10_000)
    px, py = x_hat[ox[rows]].double(), sy[oy[cols]].double()
    axes = principal_axes(sy, k).double()
    scores = (py - sy.double().mean(0)) @ axes  # [m, k] PC scores of the pseudo-partners
    half = len(px) // 2
    r2 = []
    for j in range(k):
        y, total = scores[:, j], 0.0
        for a, b in ((slice(0, half), slice(half, None)), (slice(half, None), slice(0, half))):
            xa, xb, ya, yb = px[a], px[b], y[a], y[b]
            w = torch.linalg.solve(xa.T @ xa + 10.0 * torch.eye(xa.shape[1], dtype=xa.dtype), xa.T @ ya)
            total += float(1 - ((yb - xb @ w) ** 2).sum() / ((yb - yb.mean()) ** 2).sum())
        r2.append(total / 2)
    return [j for j in range(k) if r2[j] < threshold], r2


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--holdout", type=int, default=2000)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--k", type=int, default=10)
    parser.add_argument("--threshold", type=float, default=0.3)
    parser.add_argument("--languages", nargs="*", default=list(LANGUAGES))
    parser.add_argument("--arms", nargs="*", default=["raw", "drop1", "detector"])
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    kwargs = dict(num_workers=args.workers, num_threads=args.workers)
    if args.smoke:
        kwargs.update(num_clusters=10, num_restarts=3, batch_size=1500, num_iterations=5)

    path_x = fetch(CORPUS, "vision", VISION_B)
    n = num_rows(path_x)
    val_idx = torch.arange(n - args.holdout, n)
    rows = []
    for language in args.languages:
        path_y = fetch(CORPUS, "language", language)
        randomness = Randomness(args.seed)
        ix, iy = disjoint_split(n - args.holdout, randomness, 3000 if args.smoke else None)
        sx, sy = load_rows(path_x, ix), load_rows(path_y, iy)
        vx, vy = load_rows(path_x, val_idx), load_rows(path_y, val_idx)

        def run(name, basis, extra=None):
            model = Deflated(WassersteinProcrustes(**kwargs), basis).fit(sx, sy, Randomness(args.seed))
            score = retrieval_metrics(model, vx, vy, Randomness(args.seed))["foscttm"]
            row = {"language": language, "arm": name, "foscttm": score, **(extra or {})}
            rows.append(row)
            print(row, flush=True)
            return model

        raw = run("raw", None)
        if "drop1" in args.arms:
            run("drop1", principal_axes(sy, 1))
        if "detector" in args.arms:
            dropped, r2 = detector(raw.aligner, sx, sy, args.k, args.threshold, args.seed)
            basis = principal_axes(sy, args.k)[:, dropped] if dropped else None
            run("detector", basis, {"dropped_pcs": dropped, "pseudo_pair_r2": [round(v, 3) for v in r2]})

    config = {**vars(args), "vision": VISION_B, "corpus": CORPUS, "aligner_kwargs": kwargs}
    name = "e5_scaffold_axis" + ("" if args.arms == ["raw", "drop1", "detector"] else "-" + "-".join(args.arms))
    if args.languages != list(LANGUAGES):
        name += "-" + "-".join(language.split("_")[0] for language in args.languages)
    name += f"-seed{args.seed}" if args.seed else ""
    print("receipt:", receipt(name + ("-smoke" if args.smoke else ""), config, {"rows": rows}, OUT))


if __name__ == "__main__":
    main()
