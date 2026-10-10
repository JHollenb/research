"""E5 probe (post-hoc, offline): is the top axis of each stored SPC language embedding visual or scaffold?

For each language model on SPC (first N rows, their stored files) against their stored DINOv2-B rows:
clipped and linear CKA, top language PC variance share, held-out R^2 of the top-5 language PCs from the image
embedding (ridge, 2-fold), |corr| of top language PC with top image PC and with paragraph length, linear CKA
after projecting out the top-k language PCs, and mutual 10-NN. Lemma A1 predicts: projecting out a scaffold
axis RAISES linear CKA; projecting out a shared axis lowers it.

    uv run python -m e5_scaffold_axis.axis_probe
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import torch

from common.rosetta import QWEN3_GEN_8B, VISION_B, fetch, receipt
from unpaired_rosetta import geometry as G
from unpaired_rosetta.embeddings import load_rows

OUT = Path(__file__).resolve().parents[1] / "results" / "e5_scaffold_axis"
CORPUS = "StanfordParagraphCaptioning"
CAPTIONS = Path(__file__).resolve().parents[1] / "e3_pooling_scaffold" / "payload" / f"{CORPUS}.json"


def centered(x):
    return (x - x.mean(0)).double()


def drop(x, k):
    x = centered(x)
    if k == 0:
        return x
    u, s, vt = torch.linalg.svd(x, full_matrices=False)
    return x - (u[:, :k] * s[:k]) @ vt[:k]


def pcs(x, k):
    u, s, _ = torch.linalg.svd(centered(x), full_matrices=False)
    return u[:, :k] * s[:k]


def corr(a, b):
    a, b = a - a.mean(), b - b.mean()
    return float((a @ b) / (a.norm() * b.norm()))


def cv_r2(y, x, lam=10.0):
    half, total = len(y) // 2, 0.0
    for a, b in ((slice(0, half), slice(half, None)), (slice(half, None), slice(0, half))):
        w = torch.linalg.solve(x[a].T @ x[a] + lam * torch.eye(x.shape[1], dtype=x.dtype), x[a].T @ y[a])
        total += float(1 - ((y[b] - x[b] @ w) ** 2).sum() / ((y[b] - y[b].mean()) ** 2).sum())
    return total / 2


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rows", type=int, default=4096)
    args = parser.parse_args()
    idx = torch.arange(args.rows)
    v = load_rows(fetch(CORPUS, "vision", VISION_B), idx)
    vc = centered(v)
    pv1 = pcs(v, 1)[:, 0]
    length = None
    if CAPTIONS.exists():
        captions = json.loads(CAPTIONS.read_text())
        if len(captions) >= args.rows:
            length = torch.tensor([len(c.split()) for c in captions[: args.rows]], dtype=torch.float64)
    rows = []
    for model in (QWEN3_GEN_8B, "qwen3-embedding-8b", "mpnet"):
        l = load_rows(fetch(CORPUS, "language", model), idx)
        lc = centered(l)
        spectrum = torch.linalg.svdvals(lc) ** 2
        p = pcs(l, 5)
        row = {
            "model": model,
            "clipped_cka": G.clipped_cka(v, l),
            "linear_cka": G.cka(vc, lc),
            "top_pc_variance_share": float(spectrum[0] / spectrum.sum()),
            "heldout_r2_top5_pcs_from_vision": [cv_r2(p[:, k], vc) for k in range(5)],
            "abs_corr_top_pc_with_top_vision_pc": abs(corr(p[:, 0], pv1)),
            "corr_top_pc_with_length": corr(p[:, 0], length) if length is not None else None,
            "linear_cka_after_drop_k": {k: G.cka(vc, drop(l, k)) for k in (0, 1, 2, 3, 5)},
            "mutual_knn10_first1024": float(G.mutual_knn(v[:1024], l[:1024], 10)),
        }
        rows.append(row)
        print(json.dumps(row), flush=True)
    print("receipt:", receipt("e5_axis_probe", vars(args), {"rows": rows}, OUT))


if __name__ == "__main__":
    main()
