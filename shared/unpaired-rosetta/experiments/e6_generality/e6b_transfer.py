"""E6b P6: SPC->COCO transfer, finished with a chunked COCO reduce (keeps RAM ~20 GB).

Same protocol as e6_generality/transfer.py (fit WassersteinProcrustes with their defaults on two disjoint unpaired
halves of SPC gen minus the last `holdout`; evaluate FOSCTTM on a random `eval_rows` subset of COCO-val gen the map
never saw; arms `raw` and `drop1` = the SPC-training top PC projected out of every language row). The only change:
the COCO gen file is 13.9 GB float32 [40504, 21, 4096]; load the eval rows with a chunked reduce_texts so peak RAM
stays bounded. The SPC fit is unchanged from E6. Frozen in PREREG_E6b.md section (4).

    uv run python -m e6_generality.e6b_transfer --eval-corpus coco_val2014
"""

from __future__ import annotations

import argparse
from pathlib import Path

import torch

from common.rosetta import QWEN3_GEN_8B, VISION_B, fetch, receipt
from e5_scaffold_axis.run import Deflated, principal_axes
from unpaired_rosetta import WassersteinProcrustes
from unpaired_rosetta.embeddings import embedding_path, load_rows, num_rows, reduce_texts
from unpaired_rosetta.evaluation import disjoint_split, retrieval_metrics
from unpaired_rosetta.randomness import Randomness

OUT = Path(__file__).resolve().parents[1] / "results" / "e6_generality"
FIT_CORPUS = "StanfordParagraphCaptioning"


def load_rows_chunked(path: Path, indices: torch.Tensor, chunk: int = 2000) -> torch.Tensor:
    """load_rows, but gather + reduce in row-blocks so a 13.9 GB file never materialises in full."""
    embeddings = torch.load(path, mmap=True)
    out = []
    for start in range(0, len(indices), chunk):
        idx = indices[start:start + chunk]
        order = torch.argsort(idx)
        block = embeddings[idx[order]][torch.argsort(order)]
        out.append(reduce_texts(block).float().clone())
        del block
    return torch.cat(out, dim=0)


def smoke(eval_corpus: str) -> dict:
    """Chunked reduce of the first 64 COCO rows must equal the library load_rows of those rows within 1e-4."""
    path_y = fetch(eval_corpus, "language", QWEN3_GEN_8B)
    idx = torch.arange(64)
    a = load_rows_chunked(path_y, idx, chunk=16)
    b = load_rows(path_y, idx)
    dev = float((a - b).abs().max())
    assert dev < 1e-4, f"chunked reduce disagrees with load_rows (max dev {dev})"
    assert torch.isfinite(a).all() and (a.norm(dim=1) - 1).abs().max() < 2e-2, "chunked rows not unit/finite"
    return {"chunk_vs_loadrows_max_dev": dev}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--eval-corpus", default="coco_val2014")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--holdout", type=int, default=2000)
    parser.add_argument("--eval-rows", type=int, default=5000)
    parser.add_argument("--chunk", type=int, default=2000)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--manifest-sha256", default="")
    args = parser.parse_args()
    kwargs = dict(num_workers=args.workers, num_threads=args.workers)

    sm = smoke(args.eval_corpus)
    print("smoke:", sm, flush=True)

    fit_x = fetch(FIT_CORPUS, "vision", VISION_B)
    fit_y = fetch(FIT_CORPUS, "language", QWEN3_GEN_8B)
    n_fit = num_rows(fit_x)
    ix, iy = disjoint_split(n_fit - args.holdout, Randomness(args.seed))
    sx, sy = load_rows(fit_x, ix), load_rows(fit_y, iy)

    eval_x = fetch(args.eval_corpus, "vision", VISION_B)
    eval_y = embedding_path(args.eval_corpus, "language", QWEN3_GEN_8B)
    n_eval = num_rows(eval_x)
    rnd = Randomness(args.seed)
    eval_idx = rnd.subset(n_eval, min(args.eval_rows, n_eval))
    vx = load_rows(eval_x, eval_idx)
    vy = load_rows_chunked(eval_y, eval_idx, chunk=args.chunk)
    assert vx.shape[0] == vy.shape[0], "eval vision/language count mismatch"

    rows = []
    for arm, basis in (("raw", None), ("drop1", principal_axes(sy, 1))):
        model = Deflated(WassersteinProcrustes(**kwargs), basis).fit(sx, sy, Randomness(args.seed))
        foscttm = retrieval_metrics(model, vx, vy, Randomness(args.seed))["foscttm"]
        row = {"fit_corpus": FIT_CORPUS, "eval_corpus": args.eval_corpus, "arm": arm,
               "foscttm_eval_only": foscttm, "eval_rows": int(len(eval_idx))}
        rows.append(row)
        print(row, flush=True)

    name = f"e6b_transfer-SPC-to-{args.eval_corpus}" + (f"-seed{args.seed}" if args.seed else "")
    config = {**vars(args), "fit_corpus": FIT_CORPUS, "vision": VISION_B, "aligner_kwargs": kwargs,
              "n_fit": n_fit, "n_eval": n_eval, "smoke": sm}
    print("receipt:", receipt(name, config, {"rows": rows}, OUT))


if __name__ == "__main__":
    main()
