"""E0 - their premise on our data: is the cross-model symbol table recoverable with zero pairs? (shared.md, §3)

Input: the fp16 pooled subject-row displacements of 18 animals x 6 templates in two spaces, SmolLM2-1.7B (source)
and the FLUX.2 Klein 4B Qwen3 conditioner (native), from our symbol-table job ``job-0706b0497903``
(saturn/results/symbol-table-bridge/job-0706b0497903/report.json; private, path is an argument).

Arms (all zero pairs unless stated):
  qap-class      class means (mean over the distinct prefixes), centered-cosine kernels, Koopmans-Beckmann QAP
                 solved with 2-opt local search from random starts (best of R restarts)
  qap-prefix     the same on each prefix alone (four independent 18-node problems)
  mpopt-class    the same problem with their solver (MPOpt via pylibmgm) on their CKA costs
  null           a Gaussian source geometry in place of SmolLM2 (what the solver finds in noise)
  seeded-k       k known correspondences fixed, accuracy on the other 18-k (scipy FAQ, partial_match)
  rows-unpaired  rows of both spaces with animal AND prefix unknown: agglomerative clusters per space, then QAP
                 on cluster means; accuracy = animal recovered per source row

Template collapse: causal conditioners give bit-identical subject-row displacements for templates sharing the
prefix before the subject token, so templates are deduplicated by exact equality first (4 distinct of 6).
"""

from __future__ import annotations

import argparse
import base64
import json
import warnings
from pathlib import Path

import numpy as np
from scipy.optimize import quadratic_assignment

from common.rosetta import receipt

ANIMALS = ("bear", "cat", "cow", "deer", "dog", "duck", "eagle", "fox", "frog", "goat",
           "horse", "lion", "owl", "pig", "rabbit", "sheep", "tiger", "wolf")
OUT = Path(__file__).resolve().parents[1] / "results" / "e0_symbol_qap"
DEFAULT_DUMP = Path.home() / "domains/saturn/results/symbol-table-bridge/job-0706b0497903/report.json"


def load(dump: Path):
    d = json.loads(dump.read_text())["displacements"]
    keys = [tuple(k) for k in d["keys"]]

    def matrix(name: str, dim: str) -> np.ndarray:
        raw = np.frombuffer(base64.b64decode(d[name]), dtype=np.float16)
        return raw.reshape(len(keys), d[dim]).astype(np.float64)

    return keys, matrix("x_resid_fp16_b64", "x_dim"), matrix("y_resid_fp16_b64", "y_dim")


def distinct_templates(keys, *spaces) -> list[str]:
    templates = sorted({k[1] for k in keys})
    block = lambda m, t: np.stack([m[keys.index((a, t))] for a in ANIMALS])  # noqa: E731
    keep: list[str] = []
    for t in templates:
        if not any(all(np.array_equal(block(m, t), block(m, u)) for m in spaces) for u in keep):
            keep.append(t)
    return keep


def centered_cosine(m: np.ndarray) -> np.ndarray:
    m = m - m.mean(0, keepdims=True)
    m = m / np.linalg.norm(m, axis=1, keepdims=True)
    return m @ m.T


def objective(kx: np.ndarray, ky: np.ndarray, perm: np.ndarray) -> float:
    return float(np.sum(kx * ky[np.ix_(perm, perm)]))


def two_opt(kx, ky, perm):
    perm, best, n, improved = perm.copy(), objective(kx, ky, perm), len(perm), True
    while improved:
        improved = False
        for i in range(n):
            for j in range(i + 1, n):
                perm[i], perm[j] = perm[j], perm[i]
                value = objective(kx, ky, perm)
                if value > best + 1e-12:
                    best, improved = value, True
                else:
                    perm[i], perm[j] = perm[j], perm[i]
    return perm, best


def solve(kx, ky, restarts: int, seed: int):
    rng = np.random.default_rng(seed)
    results = [two_opt(kx, ky, rng.permutation(len(kx))) for _ in range(restarts)]
    results.sort(key=lambda r: -r[1])
    identity = tuple(range(len(kx)))
    return results[0][0], results[0][1], sum(tuple(p) == identity for p, _ in results), results


def mpopt(kx, ky, seed: int):
    """Their solver on their costs (geometric_initialization.cka_matching_costs without pairs)."""
    import torch
    from unpaired_rosetta.qap import MPOptQAPSolver

    def centered(gram):  # H K H, as their centered_kernel does for a linear kernel
        return gram - gram.mean(dim=0, keepdim=True) - gram.mean(dim=1, keepdim=True) + gram.mean()

    a, b = torch.as_tensor(kx), torch.as_tensor(ky)
    # Minimize Tr(-K_A P K_B P^T), i.e. maximize the CKA numerator, exactly as their cka_matching_costs without pairs.
    return MPOptQAPSolver().solve(-centered(a), centered(b), None, seed).numpy()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dump", type=Path, default=DEFAULT_DUMP)
    parser.add_argument("--restarts", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    if args.smoke:
        args.restarts = 50
    warnings.filterwarnings("ignore", category=FutureWarning)
    keys, X, Y = load(args.dump)
    templates = distinct_templates(keys, X, Y)
    n, results = len(ANIMALS), {"templates_distinct": templates}

    def class_means(m):
        return np.stack([np.mean([m[keys.index((a, t))] for t in templates], 0) for a in ANIMALS])

    kx, ky = centered_cosine(class_means(X)), centered_cosine(class_means(Y))
    tri = np.triu_indices(n, 1)
    results["kernel_offdiag_corr"] = float(np.corrcoef(kx[tri], ky[tri])[0, 1])

    perm, best, hits, all_runs = solve(kx, ky, args.restarts, args.seed)
    identity = np.arange(n)
    swaps = []
    for i in range(n):
        for j in range(i + 1, n):
            q = identity.copy()
            q[i], q[j] = q[j], q[i]
            swaps.append(objective(kx, ky, q))
    distinct_optima = sorted({round(v, 6) for _, v in all_runs}, reverse=True)[:5]
    results["qap_class"] = {
        "correct": int((perm == identity).sum()), "of": n, "objective_found": best,
        "objective_true": objective(kx, ky, identity), "restarts": args.restarts, "restarts_hitting_truth": hits,
        "best_single_swap": max(swaps), "top_local_optima": distinct_optima,
        "errors": [(ANIMALS[i], ANIMALS[perm[i]]) for i in range(n) if perm[i] != i],
    }
    try:
        mp = mpopt(kx, ky, args.seed)
        results["mpopt_class"] = {"correct": int((mp == identity).sum()), "of": n}
    except Exception as error:  # pylibmgm missing or failing is recorded, not hidden
        results["mpopt_class"] = {"error": repr(error)}

    results["qap_prefix"] = {}
    for t in templates:
        px = centered_cosine(np.stack([X[keys.index((a, t))] for a in ANIMALS]))
        py = centered_cosine(np.stack([Y[keys.index((a, t))] for a in ANIMALS]))
        p, _, h, _ = solve(px, py, max(args.restarts // 4, 20), args.seed)
        results["qap_prefix"][t] = {"correct": int((p == identity).sum()), "of": n, "restarts_hitting_truth": h}

    rng = np.random.default_rng(args.seed + 5)
    nulls = []
    for _ in range(10):
        g = centered_cosine(rng.standard_normal(class_means(X).shape))
        p, _, _, _ = solve(g, ky, max(args.restarts // 10, 20), int(rng.integers(1 << 30)))
        nulls.append(int((p == identity).sum()))
    results["null_gaussian_correct"] = nulls

    results["seeded"] = {}
    for k in (1, 2, 3, 5):
        accs = []
        for trial in range(20):
            anchors = rng.choice(n, k, replace=False)
            best_perm, best_val = None, -np.inf
            for start in range(30):
                res = quadratic_assignment(kx, ky, method="faq", options={
                    "maximize": True, "partial_match": np.stack([anchors, anchors], 1),
                    "P0": "randomized", "rng": int(rng.integers(1 << 31))})
                if res.fun > best_val:
                    best_val, best_perm = res.fun, res.col_ind
            rest = [i for i in range(n) if i not in anchors]
            accs.append(float(np.mean([best_perm[i] == i for i in rest])))
        results["seeded"][str(k)] = {"mean_acc_other": float(np.mean(accs)), "chance": 1 / (n - k)}

    from sklearn.cluster import AgglomerativeClustering
    from sklearn.metrics import adjusted_rand_score

    def rows(m):
        return np.stack([m[keys.index((a, t))] for a in ANIMALS for t in templates])

    def unit(m):
        m = m - m.mean(0)
        return m / np.linalg.norm(m, axis=1, keepdims=True)

    rx, ry = rows(X), rows(Y)
    labels = np.repeat(np.arange(n), len(templates))
    cluster = lambda r: AgglomerativeClustering(n_clusters=n, metric="cosine", linkage="average").fit_predict(unit(r))  # noqa: E731
    cx, cy = cluster(rx), cluster(ry)
    mx = np.stack([rx[cx == c].mean(0) for c in range(n)])
    my = np.stack([ry[cy == c].mean(0) for c in range(n)])
    pc, _, _, _ = solve(centered_cosine(mx), centered_cosine(my), max(args.restarts // 2, 20), args.seed + 7)
    majority = np.array([np.bincount(labels[cy == c], minlength=n).argmax() for c in range(n)])
    results["rows_unpaired"] = {
        "animal_recovered_share": float(np.mean(majority[pc[cx]] == labels)), "chance": 1 / n,
        "cluster_ari_source": float(adjusted_rand_score(labels, cx)),
        "cluster_ari_native": float(adjusted_rand_score(labels, cy)),
    }
    print(json.dumps(results, indent=2))
    config = {**vars(args), "dump": str(args.dump)}
    print("receipt:", receipt("e0_symbol_qap" + ("-smoke" if args.smoke else ""), config, results, OUT))


if __name__ == "__main__":
    main()
