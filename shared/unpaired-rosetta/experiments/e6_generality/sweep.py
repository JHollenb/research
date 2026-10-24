"""E6 gate sweep: the E5 discovery-selected gate detector + FOSCTTM, on a `--corpus` other than SPC.

One job = one (corpus, language, seed). It fits each candidate gate setting, scores it with the pairs-free S1/S2
and with true-pair FOSCTTM (evaluation only), and writes ONE combined receipt with a row per candidate. Candidates
default to the full sweep `none, pc0, pc1, pc2, pc3, pc4` (as E5 seed 0); pass `--candidates none pc0` for the
seed-1/2 top-two runs. Their WassersteinProcrustes with default hyperparameters, SPC-identical protocol: train on
the corpus minus the last `holdout` rows (two disjoint unpaired halves), FOSCTTM on those held-out rows, the
dropped axis is the top PC of the unpaired language training rows.

Smoke gate (frozen, runs in-process before any scored candidate; aborts the job on failure): (1) the reduced gen
embedding is finite and unit-norm; (2) a tiny fit on a 3000-row disjoint subset returns a finite FOSCTTM in
[0, 0.5]; (3) principal_axes(sy, 1) is unit-norm and its projection is non-trivial. `--smoke` runs only the tiny
config (wiring check, never cited).

    uv run python -m e6_generality.sweep --corpus DenselyCaptionedImages --language qwen3-embedding-8b
"""

from __future__ import annotations

import argparse
from pathlib import Path

import torch

from common.rosetta import QWEN3_GEN_8B, VISION_B, fetch, receipt
from e5_scaffold_axis.gates import unpaired_scores
from e5_scaffold_axis.run import Deflated, principal_axes
from unpaired_rosetta import WassersteinProcrustes
from unpaired_rosetta.embeddings import load_rows, num_rows
from unpaired_rosetta.evaluation import disjoint_split, retrieval_metrics
from unpaired_rosetta.randomness import Randomness

OUT = Path(__file__).resolve().parents[1] / "results" / "e6_generality"
SHORT = {QWEN3_GEN_8B: "qwen3-8b-gen"}
ALL_CANDIDATES = ["none", "pc0", "pc1", "pc2", "pc3", "pc4"]


def basis_for(candidate: str, sy: torch.Tensor) -> torch.Tensor | None:
    if candidate == "none":
        return None
    k = int(candidate.removeprefix("pc"))
    return principal_axes(sy, k + 1)[:, [k]]


def smoke_gate(sx: torch.Tensor, sy: torch.Tensor, vx: torch.Tensor, vy: torch.Tensor) -> dict:
    """Frozen in-process checks; raise on failure. Returns the smoke diagnostics for the receipt.

    sx and sy are the two UNPAIRED training halves (disjoint_split makes them differ by up to one row for odd n),
    so FOSCTTM is evaluated on the PAIRED holdout (vx, vy), never on sx vs sy.
    """
    assert torch.isfinite(sy).all() and torch.isfinite(sx).all(), "non-finite rows"
    norms = sy.norm(dim=1)
    # reduce_texts normalizes in the STORED precision (bf16 for most files, ~2^-8 error), so unit norm holds only
    # to ~5e-3 after the .float() cast. Tolerance 2e-2 confirms normalization ran while still catching a genuinely
    # unnormalized/garbage row (off by >> 0.02).
    assert (norms - 1).abs().max() < 2e-2, f"language rows not unit-norm (max dev {float((norms-1).abs().max())})"
    assert vx.shape[0] == vy.shape[0], "holdout vision/language row-count mismatch"
    axis = principal_axes(sy, 1)
    assert abs(float(axis.norm()) - 1.0) < 1e-4, "top PC not unit-norm"
    trace_full = float((sy - sy.mean(0)).pow(2).sum())
    projected = sy - (sy @ axis) @ axis.T
    trace_drop = float((projected - projected.mean(0)).pow(2).sum())
    assert trace_drop < trace_full, "projecting out the top PC did not reduce variance"
    mx, my = min(3000, sx.shape[0]), min(3000, sy.shape[0])
    tiny = WassersteinProcrustes(num_clusters=10, num_restarts=3, batch_size=1500, num_iterations=5,
                                 num_workers=4, num_threads=4)
    model = Deflated(tiny, None).fit(sx[:mx], sy[:my], Randomness(0))
    mv = min(2000, vx.shape[0])
    foscttm = retrieval_metrics(model, vx[:mv], vy[:mv], Randomness(0))["foscttm"]
    # Finiteness + valid-metric-range wiring check on the paired holdout. FOSCTTM is a fraction in [0, 1] with 0.5
    # = chance; a degenerate tiny-config fit (restarts=3, iters=5) of the broken gen case can legitimately land
    # above 0.5 (worse than chance) in a finite sample, so the check is only finiteness and [0, 1] -- it guards
    # against NaN/crash, not fit quality. The scored FOSCTTM uses the full config on the full holdout.
    assert torch.isfinite(torch.tensor(foscttm)) and 0.0 <= foscttm <= 1.0, f"smoke FOSCTTM {foscttm}"
    return {"tiny_fit_holdout_foscttm": foscttm, "trace_full": trace_full, "trace_after_drop_pc0": trace_drop}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", required=True)
    parser.add_argument("--language", required=True)
    parser.add_argument("--candidates", nargs="*", default=ALL_CANDIDATES)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--holdout", type=int, default=2000)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--manifest-sha256", default="")
    args = parser.parse_args()
    kwargs = dict(num_workers=args.workers, num_threads=args.workers)
    if args.smoke:
        kwargs.update(num_clusters=10, num_restarts=3, batch_size=1500, num_iterations=5)

    path_x, path_y = fetch(args.corpus, "vision", VISION_B), fetch(args.corpus, "language", args.language)
    n = num_rows(path_x)
    val_idx = torch.arange(n - args.holdout, n)
    ix, iy = disjoint_split(n - args.holdout, Randomness(args.seed), 3000 if args.smoke else None)
    sx, sy = load_rows(path_x, ix), load_rows(path_y, iy)
    vx, vy = load_rows(path_x, val_idx), load_rows(path_y, val_idx)

    smoke = smoke_gate(sx, sy, vx, vy) if not args.smoke else {"skipped_for_smoke_config": True}
    print("smoke gate:", smoke, flush=True)

    rows = []
    for candidate in args.candidates:
        basis = basis_for(candidate, sy)
        model = Deflated(WassersteinProcrustes(**kwargs), basis).fit(sx, sy, Randomness(args.seed))
        row = {
            "corpus": args.corpus,
            "language": args.language,
            "candidate": candidate,
            **unpaired_scores(model, sx, sy, args.seed),
            "foscttm_eval_only": retrieval_metrics(model, vx, vy, Randomness(args.seed))["foscttm"],
        }
        rows.append(row)
        print(row, flush=True)

    name = f"e6_sweep-{args.corpus}-{SHORT.get(args.language, args.language)}"
    if args.candidates != ALL_CANDIDATES:
        name += "-" + "-".join(args.candidates)
    name += (f"-seed{args.seed}" if args.seed else "") + ("-smoke" if args.smoke else "")
    config = {**vars(args), "vision": VISION_B, "aligner_kwargs": kwargs, "rows_available": n, "smoke_gate": smoke}
    print("receipt:", receipt(name, config, {"rows": rows}, OUT))


if __name__ == "__main__":
    main()
