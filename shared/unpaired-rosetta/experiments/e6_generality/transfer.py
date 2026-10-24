"""E6 transfer protocol: fit the unpaired map on SPC Qwen3-8B-gen, evaluate FOSCTTM on another corpus.

Schnaus et al.'s headline validation fits maps on one corpus and evaluates them on held-out COCO-val. This script
reproduces that for the gen encoder: the WassersteinProcrustes map (their defaults) is fit on SPC (train on SPC
minus the last `holdout` rows), and FOSCTTM is measured on a random subset of `--eval-corpus` rows the map never
saw. Two arms: `raw` (their pipeline) and `drop1` (the top PC of the SPC training language rows projected out of
every language row, train and eval) -- i.e. does the SPC-learned fix transfer to the eval corpus. The map, its
means and the dropped axis all come from SPC only; no eval-corpus statistic is used.

    uv run python -m e6_generality.transfer --eval-corpus coco_val2014
"""

from __future__ import annotations

import argparse
from pathlib import Path

import torch

from common.rosetta import QWEN3_GEN_8B, VISION_B, fetch, receipt
from e5_scaffold_axis.run import Deflated, principal_axes
from unpaired_rosetta import WassersteinProcrustes
from unpaired_rosetta.embeddings import load_rows, num_rows
from unpaired_rosetta.evaluation import disjoint_split, retrieval_metrics
from unpaired_rosetta.randomness import Randomness

OUT = Path(__file__).resolve().parents[1] / "results" / "e6_generality"
FIT_CORPUS = "StanfordParagraphCaptioning"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--eval-corpus", required=True)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--holdout", type=int, default=2000)
    parser.add_argument("--eval-rows", type=int, default=5000)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--manifest-sha256", default="")
    args = parser.parse_args()
    kwargs = dict(num_workers=args.workers, num_threads=args.workers)

    fit_x = fetch(FIT_CORPUS, "vision", VISION_B)
    fit_y = fetch(FIT_CORPUS, "language", QWEN3_GEN_8B)
    n_fit = num_rows(fit_x)
    ix, iy = disjoint_split(n_fit - args.holdout, Randomness(args.seed))
    sx, sy = load_rows(fit_x, ix), load_rows(fit_y, iy)

    eval_x = fetch(args.eval_corpus, "vision", VISION_B)
    eval_y = fetch(args.eval_corpus, "language", QWEN3_GEN_8B)
    n_eval = num_rows(eval_x)
    assert num_rows(eval_y) == n_eval, "eval vision/language row-count mismatch"
    rnd = Randomness(args.seed)
    eval_idx = rnd.subset(n_eval, min(args.eval_rows, n_eval))
    vx, vy = load_rows(eval_x, eval_idx), load_rows(eval_y, eval_idx)

    rows = []
    for arm, basis in (("raw", None), ("drop1", principal_axes(sy, 1))):
        model = Deflated(WassersteinProcrustes(**kwargs), basis).fit(sx, sy, Randomness(args.seed))
        foscttm = retrieval_metrics(model, vx, vy, Randomness(args.seed))["foscttm"]
        row = {"fit_corpus": FIT_CORPUS, "eval_corpus": args.eval_corpus, "arm": arm,
               "foscttm_eval_only": foscttm, "eval_rows": int(len(eval_idx))}
        rows.append(row)
        print(row, flush=True)

    name = f"e6_transfer-SPC-to-{args.eval_corpus}" + (f"-seed{args.seed}" if args.seed else "")
    config = {**vars(args), "fit_corpus": FIT_CORPUS, "vision": VISION_B, "aligner_kwargs": kwargs,
              "n_fit": n_fit, "n_eval": n_eval}
    print("receipt:", receipt(name, config, {"rows": rows}, OUT))


if __name__ == "__main__":
    main()
