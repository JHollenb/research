"""E2b - draw-to-draw spread for the E2 ladder, so random vs medoid selection is read against noise (Claim E).

E2 (`run.py`) fits one draw per p (seed 0). This reruns the closed-form arms (linear, orthogonal) and the span
numbers for seeds 1..N, for both selections, at p <= 100. Their aligner is not rerun (about 25 min per fit).
Scoring: medoid beats random at a given p when its mean over seeds 0..N is better by more than twice the
standard error of the difference. Otherwise that p is "no detectable difference".

    uv run python -m e2_span_bound.draws            # --seeds 1 2 3 4 5 --pairs 1 2 5 10 20 50 100
"""

from __future__ import annotations

import argparse

from common.rosetta import VISION_B, receipt, training_data, validation_data
from e2_span_bound.run import OUT, evaluate_arms, medoid_pairs, span_numbers
from unpaired_rosetta.randomness import Randomness


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--language", default="mpnet")
    parser.add_argument("--train", default="coco_train2014")
    parser.add_argument("--validation", default="coco_val2014")
    parser.add_argument("--seeds", type=int, nargs="*", default=[1, 2, 3, 4, 5])
    parser.add_argument("--pairs", type=int, nargs="*", default=[1, 2, 5, 10, 20, 50, 100])
    parser.add_argument("--selection", nargs="*", default=["random", "medoid"])
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    train_size, validation_size, pool = (3000, 2000, 5000) if args.smoke else (None, None, 20_000)
    if args.smoke:
        args.seeds, args.pairs = args.seeds[:1], [5]

    # One fixed validation set (seed 0, as in run.py) so draws differ only in training split and pairs.
    val_x, val_y, _ = validation_data(args.validation, VISION_B, args.language, 0, validation_size)
    rows = []
    for seed in args.seeds:
        for selection in args.selection:
            for p in args.pairs:
                randomness = Randomness(seed)
                if selection == "random":
                    sx, sy, px, py = training_data(args.train, VISION_B, args.language, randomness, train_size, p)
                else:
                    indices = medoid_pairs(args.train, p, seed, pool_size=pool)
                    sx, sy, px, py = training_data(
                        args.train, VISION_B, args.language, randomness, train_size, pair_indices=indices
                    )
                row = {"seed": seed, "selection": selection, "p": p, **span_numbers(py, sy, val_y, p, seed)}
                row.update(evaluate_arms(sx, sy, px, py, val_x, val_y, seed, {}, with_ours=False))
                rows.append(row)
                print(row, flush=True)
    print("receipt:", receipt("e2_draws" + ("-smoke" if args.smoke else ""), vars(args), {"rows": rows}, OUT))


if __name__ == "__main__":
    main()
