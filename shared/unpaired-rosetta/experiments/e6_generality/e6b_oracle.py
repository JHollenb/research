"""E6b decisive oracle: the true-pair ceiling for a single rotation (and for an unconstrained linear map).

For each (corpus, language, candidate) the oracle trains on the TRUE pairs at indices arange(0, n-holdout) -- vision
row i paired with language row i -- and evaluates holdout FOSCTTM on the last `holdout` rows with their
`retrieval_metrics` (shuffle seed 0). Two maps, both fit on the training rows only:

  orth   W = polar(Xc^T Yc)                      orthogonal-Procrustes optimum, the ceiling of their rotation family
  lin    W = (Xc^T Xc + lam I)^-1 (Xc^T Yc)      best linear map X->Y under least squares (ridge, lam=1e-3)

`pc0` removal mirrors E6's Deflated: basis = principal_axes(train_y, 1), projected out of raw train_y and val_y
before centering. The oracle is an upper bound (it sees the true correspondence and all n-holdout rows). Frozen in
PREREG_E6b.md. One job runs every cell and writes one combined receipt.

Smoke (frozen; in-process before any real cell; aborts on failure): synthetic rotation recovery (FOSCTTM < 0.02),
semi-orthogonal polar (||W^T W - I|| < 1e-3), finite ridge solve; then per real cell, finite unit-norm rows and
equal vision/language counts.

    uv run python -m e6_generality.e6b_oracle --manifest-sha256 <sha>
"""

from __future__ import annotations

import argparse
from pathlib import Path

import torch

from common.rosetta import QWEN3_GEN_8B, VISION_B, fetch, receipt
from e5_scaffold_axis.run import principal_axes
from unpaired_rosetta.embeddings import load_rows, num_rows
from unpaired_rosetta.evaluation import retrieval_metrics
from unpaired_rosetta.linalg import center_and_normalize, polar
from unpaired_rosetta.randomness import Randomness

OUT = Path(__file__).resolve().parents[1] / "results" / "e6_generality"
SHORT = {QWEN3_GEN_8B: "qwen3-8b-gen"}
CORPORA = ["StanfordParagraphCaptioning", "DenselyCaptionedImages", "DOCCIDataset"]
RIDGE = 1e-3


def project_out(y: torch.Tensor, basis: torch.Tensor | None) -> torch.Tensor:
    if basis is None:
        return y
    return y - (y @ basis) @ basis.T


class OracleMap:
    """A fitted map with their aligner's retrieval interface, but the WEIGHT comes from the true pairs.

    All arithmetic in float64 (a ceiling / near-tie quantity); retrieval_metrics casts scores to double anyway.
    """

    def __init__(self, mean_x, mean_y, weight, basis) -> None:
        self.mean_x, self.mean_y, self.weight, self.basis = mean_x, mean_y, weight, basis

    def transform(self, queries_x: torch.Tensor) -> torch.Tensor:
        return center_and_normalize(queries_x.double(), self.mean_x) @ self.weight

    def similarity(self, queries_x: torch.Tensor, keys_y: torch.Tensor) -> torch.Tensor:
        keys = center_and_normalize(project_out(keys_y.double(), self.basis), self.mean_y)
        return self.transform(queries_x) @ keys.T


def fit_oracle(train_x, train_y, basis, kind: str, lam: float = RIDGE) -> tuple[OracleMap, dict]:
    py = project_out(train_y.double(), basis)
    mean_x = train_x.double().mean(dim=0, keepdim=True)
    mean_y = py.mean(dim=0, keepdim=True)
    xc = center_and_normalize(train_x.double(), mean_x)
    yc = center_and_normalize(py, mean_y)
    cross = xc.T @ yc
    diag = dict(cross_fro=float(cross.norm()))
    if kind == "orth":
        weight = polar(cross)
        diag["weight_orth_err"] = float((weight @ weight.T - torch.eye(weight.shape[0], dtype=weight.dtype)).norm())
    elif kind == "lin":
        gram = xc.T @ xc
        diag["gram_trace"] = float(gram.trace())
        weight = torch.linalg.solve(gram + lam * torch.eye(gram.shape[0], dtype=gram.dtype), cross)
        diag["weight_fro"] = float(weight.norm())
    else:
        raise ValueError(kind)
    assert torch.isfinite(weight).all(), f"non-finite oracle weight ({kind})"
    return OracleMap(mean_x, mean_y, weight.double(), basis), diag


def synthetic_smoke() -> dict:
    g = torch.Generator().manual_seed(0)
    x = torch.randn(4000, 768, generator=g, dtype=torch.float64)
    r = polar(torch.randn(768, 4096, generator=g, dtype=torch.float64))  # semi-orthogonal rows: r r^T = I_768
    assert float((r @ r.T - torch.eye(768, dtype=torch.float64)).norm()) < 1e-6, "synthetic R not semi-orthogonal"
    y = center_and_normalize(x, x.mean(0, keepdim=True)) @ r  # exact rotation of centered-normalized X
    tx, vx = x[:3000], x[3000:]
    ty, vy = y[:3000], y[3000:]
    model, diag = fit_oracle(tx, ty, None, "orth")
    assert diag["weight_orth_err"] < 1e-3, f"polar not semi-orthogonal (err {diag['weight_orth_err']})"
    foscttm = retrieval_metrics(model, vx, vy, Randomness(0))["foscttm"]
    assert foscttm < 0.02, f"synthetic rotation not recovered (FOSCTTM {foscttm})"
    _, lindiag = fit_oracle(tx, ty, None, "lin")
    assert lindiag["weight_fro"] > 0 and lindiag["gram_trace"] > 0, "ridge solve degenerate"
    return {"synthetic_orth_foscttm": foscttm, "polar_orth_err": diag["weight_orth_err"]}


def real_checks(train_x, train_y, val_x, val_y) -> None:
    for name, t in (("train_x", train_x), ("train_y", train_y), ("val_x", val_x), ("val_y", val_y)):
        assert torch.isfinite(t).all(), f"{name} non-finite"
        dev = float((t.norm(dim=1) - 1).abs().max())
        assert dev < 2e-2, f"{name} not unit-norm (max dev {dev})"
    assert train_x.shape[0] == train_y.shape[0], "train vision/language count mismatch"
    assert val_x.shape[0] == val_y.shape[0], "holdout vision/language count mismatch"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--holdout", type=int, default=2000)
    parser.add_argument("--manifest-sha256", default="")
    args = parser.parse_args()

    smoke = synthetic_smoke()
    print("smoke:", smoke, flush=True)

    rows = []
    cells = [(QWEN3_GEN_8B, "none"), (QWEN3_GEN_8B, "pc0"), ("qwen3-embedding-8b", "none")]
    for corpus in CORPORA:
        path_x = fetch(corpus, "vision", VISION_B)
        n = num_rows(path_x)
        train_idx = torch.arange(0, n - args.holdout)
        val_idx = torch.arange(n - args.holdout, n)
        vis_train = load_rows(path_x, train_idx)
        vis_val = load_rows(path_x, val_idx)
        for language, candidate in cells:
            path_y = fetch(corpus, "language", language)
            lang_train = load_rows(path_y, train_idx)
            lang_val = load_rows(path_y, val_idx)
            real_checks(vis_train, lang_train, vis_val, lang_val)
            basis = principal_axes(lang_train, 1).double() if candidate == "pc0" else None
            for kind in ("orth", "lin"):
                model, diag = fit_oracle(vis_train, lang_train, basis, kind)
                foscttm = retrieval_metrics(model, vis_val, lang_val, Randomness(0))["foscttm"]
                row = {"corpus": corpus, "language": language, "candidate": candidate, "map": kind,
                       "foscttm_oracle": foscttm, "n_train": int(len(train_idx)), "n_holdout": int(len(val_idx)),
                       **diag}
                rows.append(row)
                print({k: (round(v, 5) if isinstance(v, float) else v) for k, v in row.items()}, flush=True)

    config = {**vars(args), "vision": VISION_B, "ridge_lambda": RIDGE, "corpora": CORPORA,
              "cells": [[SHORT.get(l, l), c] for l, c in cells], "smoke": smoke}
    print("receipt:", receipt("e6b_oracle", config, {"rows": rows}, OUT))


if __name__ == "__main__":
    main()
