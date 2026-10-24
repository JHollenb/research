"""E8: the CITE-seq "partially aligned" tier (scRNA vs ADT) -- does a rotation exist, is the failure a search
failure, and is there a dominant nuisance axis?

Reproduces their CITE-seq setting exactly (their loaders, their disjoint-train / all-paired-eval protocol, their
aligner defaults C=30 S=30 b=10000 R=100), then adds three measurements, none of which touches true pairs except the
two oracles (labelled) and the min-FOSCTTM references (labelled):

  * oracle  -- true-pair orthogonal Procrustes (and ridge-linear) FOSCTTM on a disjoint holdout: does a rotation exist?
  * search  -- per-seed FOSCTTM variance; S1 (mean matched pseudo-pair cosine) and S2 (CKA of pseudo-pairs) logged
               per iterate and per seed; does argmax-S1 select good iterates / seeds vs last-iterate and mean-over-seeds?
  * axis    -- top-PC cross-modal held-out R2 (each modality's top PCs predicted from the other), correlation of the
               top PC with a sequencing-depth proxy, and the effect of removing the top axis (pairs-free, by variance).

Smoke (frozen; synthetic only; runs in-process before any real cell; aborts on failure): a known random rotation of
a 25-dim cloud is recovered by the oracle (FOSCTTM < 0.02) and scores S1 ~ 1; the logged aligner's final weight equals
the stock aligner's; ridge solve finite.

    uv run python -m e8_single_cell.run --seeds 20 [--remove-topk 0] [--manifest-sha256 <sha>]
"""

from __future__ import annotations

import argparse
from pathlib import Path

import torch

from common.rosetta import receipt
from unpaired_rosetta.embeddings import embedding_path, load_rows, num_rows
from unpaired_rosetta.evaluation import disjoint_split, retrieval_metrics
from unpaired_rosetta.geometry import cka
from unpaired_rosetta.linalg import center_and_normalize, polar
from unpaired_rosetta.randomness import Randomness, derive_seeds
from unpaired_rosetta.assignment import batched_hungarian_matching
from unpaired_rosetta.wasserstein_procrustes import WassersteinProcrustes

from e8_single_cell.aligner_logged import LoggedWassersteinProcrustes

OUT = Path(__file__).resolve().parents[1] / "results" / "e8_single_cell"
DATASET = "CITE-seq"
MOD_X, MOD_Y, MODEL = "rna", "adt", "raw25"
RIDGE = 1e-3


# --------------------------------------------------------------------------- maps & self-scores


class WeightMap:
    """A fitted linear map with the aligner's retrieval interface, for an arbitrary weight (double precision)."""

    def __init__(self, mean_x, mean_y, weight) -> None:
        self.mean_x, self.mean_y, self.weight = mean_x, mean_y, weight.double()

    def transform(self, queries_x):
        return center_and_normalize(queries_x.double(), self.mean_x) @ self.weight

    def similarity(self, queries_x, keys_y):
        return self.transform(queries_x) @ center_and_normalize(keys_y.double(), self.mean_y).T


def s1_s2(train_x, train_y, weight):
    """Pairs-free self-scores of a weight on the (already centered+normalized) training sets.

    S1 = mean cosine of the Hungarian-matched pseudo-pairs of (X W) against Y over the full training set (one block,
    no shuffle, deterministic). S2 = linear CKA of the matched pseudo-pairs. No true pairs are used.
    """
    mapped = (train_x.double() @ weight.double())
    keys = train_y.double()
    block = max(mapped.shape[0], keys.shape[0])
    rows, cols = batched_hungarian_matching(mapped, keys, block)
    mx, ky = mapped[rows], keys[cols]
    s1 = float(torch.nn.functional.cosine_similarity(mx, ky, dim=-1).mean())
    s2 = float(cka(mx - mx.mean(0), ky - ky.mean(0)))
    return s1, s2


# --------------------------------------------------------------------------- their protocol


def load_pair(remove_topk: int):
    """Their load_rows for CITE-seq rna/adt (each cell unit-normed), optionally with the top-k variance axis of EACH
    modality projected out BEFORE their per-cell normalization (pairs-free: chosen by variance, not by any pairing).

    Returns the processed [1000, 25] tensors for rna and adt, plus a raw-depth proxy per cell.
    """
    path_x, path_y = embedding_path(DATASET, MOD_X, MODEL), embedding_path(DATASET, MOD_Y, MODEL)
    raw_x, raw_y = torch.load(path_x).float(), torch.load(path_y).float()  # [1000,25] pre-normalization
    depth = {"rna": raw_x.sum(dim=1), "adt": raw_y.sum(dim=1)}  # library-size proxy (sum of features per cell)
    if remove_topk > 0:
        raw_x = _project_out_top(raw_x, remove_topk)
        raw_y = _project_out_top(raw_y, remove_topk)
        x = torch.nn.functional.normalize(raw_x, dim=-1)
        y = torch.nn.functional.normalize(raw_y, dim=-1)
    else:
        x, y = load_rows(path_x), load_rows(path_y)  # exact paper preprocessing
    return x, y, depth


def _project_out_top(feats, k):
    c = feats - feats.mean(0, keepdim=True)
    _, _, vt = torch.linalg.svd(c.double(), full_matrices=False)
    basis = vt[:k].T.float()  # [d,k]
    return c - (c @ basis) @ basis.T


def foscttm_of_map(mapping, x, y, seed):
    """Their evaluate() sequence: a fresh Randomness(seed) draws the (full) validation subset, then scores it. For
    weight=final this equals the paper's reported per-seed FOSCTTM; reused per iterate so the shuffle is identical."""
    rnd = Randomness(seed)
    idx = rnd.subset(x.shape[0], None)
    return retrieval_metrics(mapping, x[idx], y[idx], rnd)["foscttm"]


def spearman(a, b):
    a = torch.as_tensor(a, dtype=torch.float64)
    b = torch.as_tensor(b, dtype=torch.float64)
    ra = a.argsort().argsort().double()
    rb = b.argsort().argsort().double()
    ra, rb = ra - ra.mean(), rb - rb.mean()
    d = ra.norm() * rb.norm()
    return float((ra @ rb) / d) if float(d) > 0 else 0.0


# --------------------------------------------------------------------------- oracle (true pairs, labelled)


def oracle_foscttm(x, y, kind):
    """True-pair ceiling: fit on a disjoint holdout split (500/500 of the 1000 paired cells), eval FOSCTTM on the
    held-out half. x[i],y[i] are the same cell. Randomness(0) fixes the split and the eval shuffle."""
    n = x.shape[0]
    perm = Randomness(0).permutation(n)
    tr, va = perm[: n // 2], perm[n // 2 :]
    mean_x = x[tr].double().mean(0, keepdim=True)
    mean_y = y[tr].double().mean(0, keepdim=True)
    xc = center_and_normalize(x[tr].double(), mean_x)
    yc = center_and_normalize(y[tr].double(), mean_y)
    cross = xc.T @ yc
    if kind == "orth":
        weight = polar(cross)
    else:
        gram = xc.T @ xc
        weight = torch.linalg.solve(gram + RIDGE * torch.eye(gram.shape[0], dtype=gram.dtype), cross)
    assert torch.isfinite(weight).all()
    mapping = WeightMap(mean_x, mean_y, weight)
    return retrieval_metrics(mapping, x[va], y[va], Randomness(0))["foscttm"]


# --------------------------------------------------------------------------- axis probe


def cv_r2(target, predictors, lam=1e-2):
    n = target.shape[0]
    half = n // 2
    total = 0.0
    for a, b in ((slice(0, half), slice(half, None)), (slice(half, None), slice(0, half))):
        xa, ya = predictors[a], target[a]
        w = torch.linalg.solve(xa.T @ xa + lam * torch.eye(xa.shape[1], dtype=xa.dtype), xa.T @ ya)
        pred = predictors[b] @ w
        yb = target[b]
        total += float(1 - ((yb - pred) ** 2).sum() / ((yb - yb.mean()) ** 2).sum())
    return total / 2


def top_pcs(feats, k):
    c = feats.double() - feats.double().mean(0, keepdim=True)
    u, s, _ = torch.linalg.svd(c, full_matrices=False)
    scores = u[:, :k] * s[:k]
    var_share = (s**2 / (s**2).sum())[:k]
    return scores, var_share


def abscorr(a, b):
    a = a.double() - a.double().mean()
    b = b.double() - b.double().mean()
    d = a.norm() * b.norm()
    return float((a @ b).abs() / d) if float(d) > 0 else 0.0


def axis_table(x, y, depth):
    """For each modality: top-5 PC variance shares, held-out R2 of each top PC predicted from the OTHER modality's
    raw features, and |corr| of the top PC with the depth proxy."""
    out = {}
    pairs = {"rna": (x, y, depth["rna"]), "adt": (y, x, depth["adt"])}
    for name, (feats, other, dep) in pairs.items():
        scores, var_share = top_pcs(feats, 5)
        other_c = other.double() - other.double().mean(0, keepdim=True)
        out[name] = {
            "var_share_top5": [round(float(v), 4) for v in var_share],
            "heldout_r2_from_other_top5": [round(cv_r2(scores[:, k], other_c), 4) for k in range(5)],
            "abscorr_topPC_with_depth": round(abscorr(scores[:, 0], dep), 4),
        }
    return out


# --------------------------------------------------------------------------- smoke


def synthetic_smoke():
    g = torch.Generator().manual_seed(0)
    d = 25
    x = torch.randn(400, d, generator=g)
    r = polar(torch.randn(d, d, generator=g))  # orthogonal
    y = center_and_normalize(x, x.mean(0, keepdim=True)) @ r
    # oracle recovers the rotation
    orc = oracle_foscttm(torch.nn.functional.normalize(x, dim=-1), torch.nn.functional.normalize(y, dim=-1), "orth")
    assert orc < 0.05, f"synthetic oracle did not recover rotation (FOSCTTM {orc})"
    # S1 of the true rotation on centered-normalized data is near 1
    cnx = center_and_normalize(x, x.mean(0, keepdim=True))
    cny = center_and_normalize(y, y.mean(0, keepdim=True))
    s1, _ = s1_s2(cnx, cny, r)
    assert s1 > 0.9, f"S1 of the true rotation too low ({s1})"
    # logged aligner final weight == stock aligner final weight (identical randomness)
    xs = torch.nn.functional.normalize(x, dim=-1)
    ys = torch.nn.functional.normalize(y, dim=-1)
    a_stock = WassersteinProcrustes(num_clusters=8, num_restarts=3, num_iterations=5).fit(xs, ys, randomness=1)
    a_log = LoggedWassersteinProcrustes(num_clusters=8, num_restarts=3, num_iterations=5).fit(xs, ys, randomness=1)
    err = float((a_stock.weight - a_log.weight).abs().max())
    assert err < 1e-5, f"logged aligner diverged from stock ({err})"
    assert len(a_log.trajectory) == 6, f"trajectory length {len(a_log.trajectory)}"
    return {"synthetic_oracle_foscttm": round(orc, 5), "synthetic_true_rot_s1": round(s1, 5), "logged_vs_stock": err}


# --------------------------------------------------------------------------- main


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=int, default=20)
    parser.add_argument("--remove-topk", type=int, default=0)
    parser.add_argument("--iters", type=int, default=100)
    parser.add_argument("--restarts", type=int, default=30)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--manifest-sha256", default="")
    args = parser.parse_args()

    smoke = synthetic_smoke()
    print("smoke:", smoke, flush=True)

    x, y, depth = load_pair(args.remove_topk)
    assert x.shape == (num_rows(embedding_path(DATASET, MOD_X, MODEL)), 25), x.shape

    # canary geometry on all paired cells
    canary = {
        "cka_all1000": round(float(cka(x.double() - x.double().mean(0), y.double() - y.double().mean(0))), 4),
        "n_cells": int(x.shape[0]),
    }
    oracle = {"orth_holdout": round(oracle_foscttm(x, y, "orth"), 5),
              "lin_holdout": round(oracle_foscttm(x, y, "lin"), 5)}
    print("canary:", canary, "oracle:", oracle, flush=True)

    seeds = derive_seeds(42, args.seeds)
    per_seed = []
    pooled_s1, pooled_fos = [], []
    for seed in seeds:
        rnd = Randomness(seed)
        idx_x, idx_y = disjoint_split(x.shape[0], rnd, None)  # 500/500 disjoint, their protocol (holdout=0)
        sx, sy = x[idx_x], y[idx_y]
        aligner = LoggedWassersteinProcrustes(
            num_clusters=30, num_restarts=args.restarts, batch_size=10_000,
            num_iterations=args.iters, num_workers=args.workers,
        ).fit(sx, sy, randomness=seed)
        tx, ty = aligner.train_x, aligner.train_y
        iters = []
        for t, w in enumerate(aligner.trajectory):
            s1, s2 = s1_s2(tx, ty, w)
            fos = foscttm_of_map(WeightMap(aligner.mean_x, aligner.mean_y, w), x, y, seed)
            iters.append({"iter": t, "s1": round(s1, 5), "s2": round(s2, 5), "foscttm": round(fos, 5)})
        s1_series = [r["s1"] for r in iters]
        fos_series = [r["foscttm"] for r in iters]
        argmax_s1 = int(torch.tensor(s1_series).argmax())
        argmin_fos = int(torch.tensor(fos_series).argmin())
        per_seed.append({
            "seed": int(seed),
            "foscttm_last": fos_series[-1],
            "s1_last": s1_series[-1],
            "s2_last": iters[-1]["s2"],
            "foscttm_argmaxS1_iter": fos_series[argmax_s1],
            "argmaxS1_iter": argmax_s1,
            "foscttm_best_iter_oracle": fos_series[argmin_fos],  # labelled: uses truth, reference only
            "best_iter_oracle": argmin_fos,
            "spearman_s1_vs_negfoscttm_iters": round(spearman(s1_series, [-f for f in fos_series]), 4),
            "iters": iters,
        })
        pooled_s1 += s1_series
        pooled_fos += fos_series
        print(f"seed {seed}: foscttm_last={fos_series[-1]:.4f} s1_last={s1_series[-1]:.4f} "
              f"argmaxS1_iter_foscttm={fos_series[argmax_s1]:.4f} best_iter={fos_series[argmin_fos]:.4f}", flush=True)

    # across-seed selection (pairs-free uses s1_last; oracle/min references labelled)
    fos_last = [r["foscttm_last"] for r in per_seed]
    s1_last = [r["s1_last"] for r in per_seed]
    fos_argmaxS1_iter = [r["foscttm_argmaxS1_iter"] for r in per_seed]
    sel_seed = int(torch.tensor(s1_last).argmax())
    best_seed_oracle = int(torch.tensor(fos_last).argmin())
    fos_t = torch.tensor(fos_last)
    selection = {
        "mean_foscttm_last": round(float(fos_t.mean()), 5),
        "std_foscttm_last": round(float(fos_t.std()), 5),
        "min_foscttm_last": round(float(fos_t.min()), 5),
        "max_foscttm_last": round(float(fos_t.max()), 5),
        # pairs-free selection over seeds, using S1 of the last iterate
        "S1_selected_seed_foscttm": round(fos_last[sel_seed], 5),
        "S1_selected_seed": int(seeds[sel_seed]),
        # pairs-free selection over seeds AND iterates (argmax S1 iterate of the argmax-S1 seed)
        "S1_selected_seed_and_iter_foscttm": round(per_seed[sel_seed]["foscttm_argmaxS1_iter"], 5),
        # references that use truth (labelled)
        "best_seed_oracle_foscttm": round(fos_last[best_seed_oracle], 5),
        "mean_foscttm_argmaxS1_iter": round(float(torch.tensor(fos_argmaxS1_iter).mean()), 5),
        # correlations
        "spearman_S1last_vs_negfoscttm_across_seeds": round(spearman(s1_last, [-f for f in fos_last]), 4),
        "spearman_S1_vs_negfoscttm_pooled_iters": round(spearman(pooled_s1, [-f for f in pooled_fos]), 4),
    }
    print("selection:", selection, flush=True)

    axis = axis_table(x, y, depth) if args.remove_topk == 0 else None
    if axis:
        print("axis:", axis, flush=True)

    config = {**vars(args), "dataset": DATASET, "modality_x": MOD_X, "modality_y": MOD_Y, "model": MODEL,
              "seeds": [int(s) for s in seeds], "aligner": {"C": 30, "S": args.restarts, "b": 10000, "R": args.iters},
              "smoke": smoke}
    results = {"canary": canary, "oracle": oracle, "selection": selection, "axis": axis, "per_seed": per_seed}
    name = f"e8_citeseq_remove{args.remove_topk}"
    print("receipt:", receipt(name, config, results, OUT))


if __name__ == "__main__":
    main()
