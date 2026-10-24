"""E6 axis probe: the E5 scaffold-axis probe, parameterised by corpus.

Same measurements as e5_scaffold_axis/axis_probe.py (clipped and linear CKA, top language PC variance share,
held-out R^2 of the top-5 language PCs from the image embedding, |corr| of the top language PC with the top image
PC and with caption length when a caption payload exists, linear CKA after projecting out the top-k language PCs,
mutual 10-NN), run on a `--corpus` other than SPC. Their stored embeddings, their load path. Lemma A1 predicts
projecting out a scaffold axis RAISES linear CKA and projecting out a shared axis LOWERS it.

    uv run python -m e6_generality.axis_probe --corpus DenselyCaptionedImages
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import torch

from common.rosetta import QWEN3_GEN_8B, VISION_B, fetch, receipt
from e5_scaffold_axis.axis_probe import centered, corr, cv_r2, drop, pcs
from unpaired_rosetta import geometry as G
from unpaired_rosetta.embeddings import load_rows, num_rows

OUT = Path(__file__).resolve().parents[1] / "results" / "e6_generality"
CAPTION_DIR = Path(__file__).resolve().parents[1] / "e3_pooling_scaffold" / "payload"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", required=True)
    parser.add_argument("--rows", type=int, default=4096)
    parser.add_argument("--manifest-sha256", default="")
    args = parser.parse_args()

    path_v = fetch(args.corpus, "vision", VISION_B)
    rows_avail = num_rows(path_v)
    n = min(args.rows, rows_avail)
    idx = torch.arange(n)
    v = load_rows(path_v, idx)
    vc = centered(v)
    pv1 = pcs(v, 1)[:, 0]

    length = None
    caption_file = CAPTION_DIR / f"{args.corpus}.json"
    if caption_file.exists():
        captions = json.loads(caption_file.read_text())
        if len(captions) >= n:
            length = torch.tensor([len(c.split()) for c in captions[:n]], dtype=torch.float64)

    rows = []
    for model in (QWEN3_GEN_8B, "qwen3-embedding-8b", "mpnet"):
        l = load_rows(fetch(args.corpus, "language", model), idx)
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

    config = {**vars(args), "vision": VISION_B, "rows_used": n, "rows_available": rows_avail}
    print("receipt:", receipt(f"e6_axis_probe-{args.corpus}", config, {"rows": rows}, OUT))


if __name__ == "__main__":
    main()
