"""E9: extend E8's CITE-seq analysis to the other single-cell pairs Schnaus et al.'s own loaders support -- PBMC
(scRNA pca50 vs scATAC topics50) and SNARE-seq (scRNA pca10 vs scATAC lsi19) -- to test whether the result (a rotation
exists; the failure is a search failure; the pairs-free self-score S1 selects good seeds; no nuisance axis) generalizes.

Reproduces each pair's setting exactly from their code @ fdfad84 (their loaders, their protocol, their aligner defaults
C=30 S=30 b=10000 R=100). The protocol is identical to CITE-seq for all three pairs: ``run_alignment`` draws a
``disjoint_split`` with ``Randomness(seed)`` (which ADVANCES that object), then passes the SAME advanced object into
``aligner.fit`` (the E8 reproduction bug; reproduced here), and ``evaluate`` scores with a fresh ``Randomness(seed)``
over all paired cells (holdout=0). SNARE-seq/CITE-seq are the ``other_domains.py`` driver; PBMC is ``domain_specific.py``
with the same run_alignment and additionally a label-transfer-accuracy (LTA) canary against their Table 9 (0.942).

Measurements per pair (none touch true pairs except the two oracles and the min-FOSCTTM references, all labelled):
  * oracle  -- true-pair orthogonal Procrustes (+ ridge-linear) FOSCTTM on a disjoint holdout: does a rotation exist?
  * search  -- per-seed FOSCTTM variance; S1 (mean matched pseudo-pair cosine) + S2 (CKA of pseudo-pairs) per iterate
               and per seed; does argmax-S1 select good seeds/iterates vs last-iterate and mean-over-seeds?
  * axis    -- top-PC cross-modal held-out R2 (each modality's top PCs predicted from the other) + depth-proxy corr.
               No removal arm unless an uncorrelated axis appears (pre-registered: removal only if R2 shows a nuisance
               axis). The "type test": a pair is nuisance-type if any top-PC has high variance share but low cross-modal
               R2, else variance-type.

Smoke (frozen; synthetic only; in-process before any real cell; aborts on failure): a known random rotation of a cloud
in the pair's X-dim is recovered by the oracle (FOSCTTM < 0.05) and scores S1 ~ 1; the logged aligner's final weight
equals the stock aligner's; the oracle/linear solves are finite. For a rectangular pair (SNARE) the smoke uses a random
semi-orthogonal map X->Y so dims differ as in the real data.

    uv run python -m e9_single_cell_more.run --pair PBMC --total-seeds 12 --seed-lo 0 --seed-hi 3
"""

from __future__ import annotations

import argparse
from pathlib import Path

import torch

from common.rosetta import receipt
from unpaired_rosetta.embeddings import embedding_path, load_rows, num_rows
from unpaired_rosetta.evaluation import disjoint_split, retrieval_metrics, label_transfer_accuracy
from unpaired_rosetta.geometry import cka
from unpaired_rosetta.linalg import center_and_normalize, polar
from unpaired_rosetta.randomness import Randomness, derive_seeds
from unpaired_rosetta.settings import storage_root
from unpaired_rosetta.assignment import batched_hungarian_matching
from unpaired_rosetta.wasserstein_procrustes import WassersteinProcrustes

from e9_single_cell_more.aligner_logged import LoggedWassersteinProcrustes

OUT = Path(__file__).resolve().parents[1] / "results" / "e9_single_cell_more"
RIDGE = 1e-3

# dataset -> (modality_x, model_x, modality_y, model_y, d_x, d_y, labels_file). From their modalities/single_cell.
PAIRS = {
    "PBMC": dict(dataset="PBMC", mod_x="rna", model_x="pca50", mod_y="atac", model_y="topics50",
                 d_x=50, d_y=50, labels="labels.pt", paper_foscttm=0.089, paper_sd=0.003, paper_cka=0.90,
                 paper_lta=0.942),
    "SNARE-seq": dict(dataset="SNARE-seq", mod_x="rna", model_x="pca10", mod_y="atac", model_y="lsi19",
                      d_x=10, d_y=19, labels="labels.pt", paper_foscttm=0.209, paper_sd=0.034, paper_cka=0.86,
                      paper_lta=None),
}


def paths(cfg):
    return (embedding_path(cfg["dataset"], cfg["mod_x"], cfg["model_x"]),
            embedding_path(cfg["dataset"], cfg["mod_y"], cfg["model_y"]))


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
    """Pairs-free self-scores on the (already centered+normalized) training sets. S1 = mean cosine of the Hungarian-
    matched pseudo-pairs of (X W) against Y over the full training set (one block). S2 = linear CKA of them. No pairs."""
    mapped = (train_x.double() @ weight.double())
    keys = train_y.double()
    block = max(mapped.shape[0], keys.shape[0])
    rows, cols = batched_hungarian_matching(mapped, keys, block)
    mx, ky = mapped[rows], keys[cols]
    s1 = float(torch.nn.functional.cosine_similarity(mx, ky, dim=-1).mean())
    s2 = float(cka(mx - mx.mean(0), ky - ky.mean(0)))
    return s1, s2


# --------------------------------------------------------------------------- their protocol


def load_pair(cfg, remove_topk: int):
    """Their load_rows for the pair (each cell unit-normed), optionally with the top-k variance axis of EACH modality
    projected out BEFORE their per-cell normalization (pairs-free: chosen by variance, not pairing)."""
    path_x, path_y = paths(cfg)
    raw_x, raw_y = torch.load(path_x).float(), torch.load(path_y).float()  # pre-normalization features
    depth = {"x": raw_x.sum(dim=1), "y": raw_y.sum(dim=1)}  # library-size proxy (sum of features per cell)
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
    basis = vt[:k].T.float()
    return c - (c @ basis) @ basis.T


def foscttm_of_map(mapping, x, y, seed):
    """Their evaluate() sequence: a fresh Randomness(seed) draws the (full) validation subset, then scores it. For
    weight=final this equals the paper's reported per-seed FOSCTTM; reused per iterate so the shuffle is identical."""
    rnd = Randomness(seed)
    idx = rnd.subset(x.shape[0], None)
    return retrieval_metrics(mapping, x[idx], y[idx], rnd)["foscttm"]


def eval_final_with_lta(mapping, x, y, labels, seed):
    """Reproduce their evaluate() exactly for the final map: fresh Randomness(seed) -> subset -> retrieval_metrics
    (consumes two permutations) -> label_transfer_accuracy on the same advanced randomness. Returns (foscttm, lta)."""
    rnd = Randomness(seed)
    idx = rnd.subset(x.shape[0], None)
    fos = retrieval_metrics(mapping, x[idx], y[idx], rnd)["foscttm"]
    lab = labels[idx]
    lta = label_transfer_accuracy(mapping, x[idx], y[idx], lab, lab, rnd)
    return fos, lta


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
    """True-pair ceiling: fit on a disjoint holdout split (50/50 of the paired cells), eval FOSCTTM on the held-out
    half. x[i],y[i] are the same cell. Randomness(0) fixes the split and the eval shuffle."""
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


def axis_table(x, y, depth, k):
    """For each modality: top-k PC variance shares, held-out R2 of each top PC predicted from the OTHER modality's raw
    features, |corr| of the top PC with the depth proxy, and the nuisance-axis / type-test verdict."""
    out = {}
    pairs = {"x": (x, y, depth["x"]), "y": (y, x, depth["y"])}
    for name, (feats, other, dep) in pairs.items():
        kk = min(k, feats.shape[1])
        scores, var_share = top_pcs(feats, kk)
        other_c = other.double() - other.double().mean(0, keepdim=True)
        r2 = [round(cv_r2(scores[:, j], other_c), 4) for j in range(kk)]
        vs = [round(float(v), 4) for v in var_share]
        out[name] = {
            "var_share_top": vs,
            "heldout_r2_from_other_top": r2,
            "abscorr_topPC_with_depth": round(abscorr(scores[:, 0], dep), 4),
            "min_r2_top": round(min(r2), 4),
        }
    return out


def type_verdict(axis, r2_threshold=0.30):
    """Nuisance-type if any top PC of either modality has cross-modal held-out R2 below the threshold (an axis the
    other side cannot predict); else variance-type. Returns (verdict, min_r2_overall)."""
    mins = [axis["x"]["min_r2_top"], axis["y"]["min_r2_top"]]
    worst = min(mins)
    return ("nuisance" if worst < r2_threshold else "variance"), round(worst, 4)


# --------------------------------------------------------------------------- smoke


def synthetic_smoke(d_x, d_y):
    g = torch.Generator().manual_seed(0)
    x = torch.randn(400, d_x, generator=g)
    r = polar(torch.randn(d_x, d_y, generator=g))  # semi-orthogonal [d_x,d_y] (handles d_x!=d_y)
    y = center_and_normalize(x, x.mean(0, keepdim=True)) @ r
    nx = torch.nn.functional.normalize(x, dim=-1)
    ny = torch.nn.functional.normalize(y, dim=-1)
    orc = oracle_foscttm(nx, ny, "orth")
    assert orc < 0.05, f"synthetic oracle did not recover rotation (FOSCTTM {orc})"
    cnx = center_and_normalize(x, x.mean(0, keepdim=True))
    cny = center_and_normalize(y, y.mean(0, keepdim=True))
    s1, _ = s1_s2(cnx, cny, r)
    assert s1 > 0.9, f"S1 of the true rotation too low ({s1})"
    a_stock = WassersteinProcrustes(num_clusters=8, num_restarts=3, num_iterations=5).fit(nx, ny, randomness=1)
    a_log = LoggedWassersteinProcrustes(num_clusters=8, num_restarts=3, num_iterations=5).fit(nx, ny, randomness=1)
    err = float((a_stock.weight - a_log.weight).abs().max())
    assert err < 1e-5, f"logged aligner diverged from stock ({err})"
    assert len(a_log.trajectory) == 6, f"trajectory length {len(a_log.trajectory)}"
    return {"synthetic_oracle_foscttm": round(orc, 5), "synthetic_true_rot_s1": round(s1, 5), "logged_vs_stock": err}


# --------------------------------------------------------------------------- main


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pair", required=True, choices=sorted(PAIRS))
    parser.add_argument("--seeds", type=int, default=12)
    parser.add_argument("--total-seeds", type=int, default=0)
    parser.add_argument("--seed-lo", type=int, default=0)
    parser.add_argument("--seed-hi", type=int, default=-1)
    parser.add_argument("--remove-topk", type=int, default=0)
    parser.add_argument("--iters", type=int, default=100)
    parser.add_argument("--restarts", type=int, default=30)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--manifest-sha256", default="")
    args = parser.parse_args()

    cfg = PAIRS[args.pair]
    smoke = synthetic_smoke(cfg["d_x"], cfg["d_y"])
    print("smoke:", smoke, flush=True)

    path_x, path_y = paths(cfg)
    x, y, depth = load_pair(cfg, args.remove_topk)
    assert x.shape == (num_rows(path_x), cfg["d_x"]), x.shape
    assert y.shape == (num_rows(path_y), cfg["d_y"]), y.shape
    labels = None
    if cfg["labels"]:
        labels = torch.load(storage_root() / "embeddings" / cfg["dataset"] / cfg["labels"])
        assert labels.shape[0] == x.shape[0], (labels.shape, x.shape)

    canary = {
        "cka_all": round(float(cka(x.double() - x.double().mean(0), y.double() - y.double().mean(0))), 4),
        "n_cells": int(x.shape[0]), "d_x": cfg["d_x"], "d_y": cfg["d_y"],
    }
    oracle = {"orth_holdout": round(oracle_foscttm(x, y, "orth"), 5),
              "lin_holdout": round(oracle_foscttm(x, y, "lin"), 5)}
    print("canary:", canary, "oracle:", oracle, flush=True)

    total = args.total_seeds or args.seeds
    hi = args.seed_hi if args.seed_hi >= 0 else total
    seeds = derive_seeds(42, total)[args.seed_lo:hi]
    print(f"pair={args.pair} seed universe total={total} slice[{args.seed_lo}:{hi}] -> {len(seeds)} seeds", flush=True)
    per_seed = []
    pooled_s1, pooled_fos = [], []
    for seed in seeds:
        rnd = Randomness(seed)
        idx_x, idx_y = disjoint_split(x.shape[0], rnd, None)  # 50/50 disjoint, their protocol (holdout=0)
        sx, sy = x[idx_x], y[idx_y]
        # Reproduce their run_alignment EXACTLY: the SAME randomness object (already advanced by the split) into fit.
        aligner = LoggedWassersteinProcrustes(
            num_clusters=30, num_restarts=args.restarts, batch_size=10_000,
            num_iterations=args.iters, num_workers=args.workers,
        ).fit(sx, sy, randomness=rnd)
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
        rec = {
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
        }
        if labels is not None:
            fos_f, lta_f = eval_final_with_lta(
                WeightMap(aligner.mean_x, aligner.mean_y, aligner.trajectory[-1]), x, y, labels, seed)
            rec["lta_last"] = round(lta_f, 5)
            rec["foscttm_last_with_lta_check"] = round(fos_f, 5)  # must equal foscttm_last (same shuffle sequence)
        per_seed.append(rec)
        pooled_s1 += s1_series
        pooled_fos += fos_series
        print(f"seed {seed}: foscttm_last={fos_series[-1]:.4f} s1_last={s1_series[-1]:.4f} "
              f"argmaxS1_iter_foscttm={fos_series[argmax_s1]:.4f} best_iter={fos_series[argmin_fos]:.4f}"
              + (f" lta={rec.get('lta_last')}" if labels is not None else ""), flush=True)

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
        "S1_selected_seed_foscttm": round(fos_last[sel_seed], 5),
        "S1_selected_seed": int(seeds[sel_seed]),
        "S1_selected_seed_and_iter_foscttm": round(per_seed[sel_seed]["foscttm_argmaxS1_iter"], 5),
        "best_seed_oracle_foscttm": round(fos_last[best_seed_oracle], 5),
        "mean_foscttm_argmaxS1_iter": round(float(torch.tensor(fos_argmaxS1_iter).mean()), 5),
        "spearman_S1last_vs_negfoscttm_across_seeds": round(spearman(s1_last, [-f for f in fos_last]), 4),
        "spearman_S1_vs_negfoscttm_pooled_iters": round(spearman(pooled_s1, [-f for f in pooled_fos]), 4),
    }
    print("selection:", selection, flush=True)

    axis = None
    tverdict = None
    if args.remove_topk == 0:
        axis = axis_table(x, y, depth, 5)
        tverdict = type_verdict(axis)
        print("axis:", axis, "type:", tverdict, flush=True)

    config = {**vars(args), "dataset": cfg["dataset"], "modality_x": cfg["mod_x"], "modality_y": cfg["mod_y"],
              "model_x": cfg["model_x"], "model_y": cfg["model_y"], "d_x": cfg["d_x"], "d_y": cfg["d_y"],
              "paper": {"foscttm": cfg["paper_foscttm"], "sd": cfg["paper_sd"], "cka": cfg["paper_cka"],
                        "lta": cfg["paper_lta"]},
              "seed_universe_total": total, "seed_slice": [args.seed_lo, hi], "seeds": [int(s) for s in seeds],
              "aligner": {"C": 30, "S": args.restarts, "b": 10000, "R": args.iters}, "smoke": smoke}
    results = {"canary": canary, "oracle": oracle, "selection": selection, "axis": axis,
               "type_verdict": tverdict, "per_seed": per_seed}
    name = f"e9_{cfg['dataset'].replace('-', '').lower()}_remove{args.remove_topk}_s{args.seed_lo}_{hi}"
    print("receipt:", receipt(name, config, results, OUT))


if __name__ == "__main__":
    main()
