"""E7: recovering the unpaired aligner on DCI/DOCCI for Qwen3-8B generative pooling via better INITIALIZATION
and few pairs, and (arm E) pairs-free SELECTION of the fixed-100-iterate / multi-seed Wasserstein-Procrustes run.

E6b proved (true-pair oracle) that a single rotation aligns Qwen3-gen to DINOv2 near-perfectly on all three
corpora; the off-SPC failure is the UNPAIRED SEARCH, not the geometry. E7 tests fixes for the search:

  A  pivot init (no image-text pairs): fit a rotation gen->Qwen3-Embedding on the SAME captions (text-text, within
     one modality), compose with the unpaired Qwen3-Embedding<->DINOv2 map their method already finds, use the
     composition as the gen map directly (A_compose) and as the init for their refinement (A_refine).
  B  transfer init: the SPC-fit rotation (raw and top-PC-removed) applied to DCI/DOCCI directly (B_transfer), and
     as the init for refinement on the target corpus (B_refine). Label: pairs were used, but on a DIFFERENT corpus.
  C  few true pairs (their Sec 4.4 protocol): k in {1,5,10,50,100} true pairs -> Procrustes-seeded init woven into
     every refinement step. Report the k at which gen recovers. candidate none (raw) and pc0 (axis removed).
  D  pairs-free search tweaks: remove the top-k PCs cumulatively (k=2..5), select by the pairs-free S1 score.
  E  pairs-free SELECTION of the existing fixed run: log per refinement iterate (and across seeds) both S1 and the
     true holdout FOSCTTM for the BASELINE aligner (no init change); score best-iterate-by-S1 vs last iterate and
     best-seed-by-S1 vs the mean/last over seeds. Their _fit returns the LAST of 100 iterates with no selection
     (verified at fdfad84, wasserstein_procrustes.py ll. 98-125); their paper reports average-over-seeds and calls
     unsupervised model selection an open problem (Sec 4/5). E asks whether a pairs-free score fixes that.

All arms reuse their library at fdfad84: WassersteinProcrustes, GeometricInitialization, retrieval_metrics, the
SPC-identical split (disjoint_split(n-holdout) halves; holdout = last `holdout` rows). The ONLY change per arm is
the initialization / the known pairs / the post-hoc selection. CPU on Beast via mrun, threads capped.

    uv run python -m e7_search_init.arms --arm <a|b|c|d|e> --corpus <...> [--smoke] --manifest-sha256 <sha>
    uv run python -m e7_search_init.arms --synthetic-smoke   # laptop, synthetic only (no real model/data)
"""

from __future__ import annotations

import argparse
from pathlib import Path

import torch

from common.rosetta import QWEN3_GEN_8B, VISION_B, fetch, receipt
from e5_scaffold_axis.gates import unit, unpaired_scores
from e5_scaffold_axis.run import Deflated, principal_axes
from e6_generality.sweep import smoke_gate
from unpaired_rosetta import WassersteinProcrustes
from unpaired_rosetta.assignment import batched_hungarian_matching
from unpaired_rosetta.embeddings import load_rows, num_rows
from unpaired_rosetta.evaluation import disjoint_split, retrieval_metrics, sample_pairs
from unpaired_rosetta.geometric_initialization import GeometricInitialization
from unpaired_rosetta.linalg import center_and_normalize, polar
from unpaired_rosetta.randomness import Randomness

OUT = Path(__file__).resolve().parents[1] / "results" / "e7_search_init"
SHORT = {QWEN3_GEN_8B: "qwen3-8b-gen", "qwen3-embedding-8b": "qwen3-emb", "mpnet": "mpnet"}
GEN = QWEN3_GEN_8B
EMB = "qwen3-embedding-8b"
SPC = "StanfordParagraphCaptioning"


# --------------------------------------------------------------------------------------------------------------
# Seeded / instrumented aligner. Subclasses their WassersteinProcrustes, preserving its exact preprocessing and
# refinement_step; the only changes are (1) start refinement from a provided weight instead of geometric init,
# (2) optionally log the pairs-free S1 and the true holdout FOSCTTM at every iterate.
# --------------------------------------------------------------------------------------------------------------
class SeededWassersteinProcrustes(WassersteinProcrustes):
    def __init__(self, *a, init_weight=None, refine=True, trace_val=None, trace_basis=None, trace_rows=2000, **k):
        super().__init__(*a, **k)
        self._init_weight = init_weight
        self._refine = refine
        self._trace_val = trace_val          # (vx_raw, vy_raw) holdout, to score FOSCTTM each iterate, or None
        self._trace_basis = trace_basis      # language projection basis used for the holdout keys, or None
        self._trace_rows = trace_rows
        self.trace = []                      # list of {iter, S1, foscttm}

    def _project(self, y):
        b = self._trace_basis
        return y if b is None else y - (y @ b) @ b.T

    def _iterate_scores(self, samples_x, samples_y, weight, it):
        # S1: mean cosine of Hungarian-matched pairs on a fixed subsample of the (centered-normalized) training rows.
        m = min(self._trace_rows, samples_x.shape[0], samples_y.shape[0])
        xh = unit(samples_x[:m] @ weight)
        yh = unit(samples_y[:m])
        rows, cols = batched_hungarian_matching(xh, yh, 10_000)
        s1 = float((xh[rows] * yh[cols]).sum(dim=1).mean())
        entry = {"iter": it, "S1_matched_cosine": s1}
        if self._trace_val is not None:
            vx, vy = self._trace_val
            model = _FrozenMap(self.mean_x, self.mean_y, weight, self._trace_basis)
            entry["foscttm"] = retrieval_metrics(model, vx, vy, Randomness(0))["foscttm"]
        self.trace.append(entry)

    def _fit(self, samples_x, samples_y, paired_x, paired_y, randomness):
        samples_x, samples_y = samples_x.float(), samples_y.float()
        self.mean_x = samples_x.mean(dim=0, keepdim=True)
        self.mean_y = samples_y.mean(dim=0, keepdim=True)
        samples_x = center_and_normalize(samples_x, self.mean_x)
        samples_y = center_and_normalize(samples_y, self.mean_y)
        if paired_x is not None and paired_x.shape[0] > 0:
            paired_x = center_and_normalize(paired_x.float(), self.mean_x)
            paired_y = center_and_normalize(paired_y.float(), self.mean_y)
        else:
            paired_x = paired_y = None

        if self._init_weight is None:
            init = GeometricInitialization(
                self.num_clusters, self.num_restarts, self.batch_size, self.num_workers
            )(samples_x, samples_y, paired_x, paired_y, randomness)
            weight = self.readout(samples_x, samples_y, init, paired_x, paired_y, randomness)
        else:
            weight = self._init_weight.float()
            assert weight.shape == (samples_x.shape[1], samples_y.shape[1]), \
                f"init weight {tuple(weight.shape)} != ({samples_x.shape[1]}, {samples_y.shape[1]})"

        if self._trace_val is not None:
            self._iterate_scores(samples_x, samples_y, weight, 0)
        if self._refine:
            for it in range(self.num_iterations):
                weight = self.refinement_step(samples_x, samples_y, weight, paired_x, paired_y, randomness)
                if self._trace_val is not None:
                    self._iterate_scores(samples_x, samples_y, weight, it + 1)
        self.weight = weight
        return self


class _FrozenMap:
    """A fitted-map view with their retrieval interface, for scoring a weight mid-refinement (trace)."""

    def __init__(self, mean_x, mean_y, weight, basis):
        self.mean_x, self.mean_y, self.weight, self.basis = mean_x, mean_y, weight, basis

    def _project(self, y):
        return y if self.basis is None else y - (y @ self.basis) @ self.basis.T

    def similarity(self, queries_x, keys_y):
        qx = center_and_normalize(queries_x.float(), self.mean_x) @ self.weight
        ky = center_and_normalize(self._project(keys_y.float()), self.mean_y)
        return qx @ ky.T


class Gated:
    """Deflated + known-pairs: project a fixed basis out of the language side, and forward true pairs to fit."""

    def __init__(self, aligner, basis=None):
        self.aligner, self.basis = aligner, basis
        self.mean_y = None

    def project(self, y):
        return y if self.basis is None else y - (y @ self.basis) @ self.basis.T

    def fit(self, sx, sy, randomness, paired_x=None, paired_y=None):
        py = self.project(paired_y.float()) if paired_y is not None else None
        self.aligner.fit(sx, self.project(sy.float()), paired_x, py, randomness)
        self.mean_y = self.aligner.mean_y
        return self

    def similarity(self, queries_x, keys_y):
        return self.aligner.similarity(queries_x, self.project(keys_y.float()))


def basis_for(candidate: str, sy: torch.Tensor) -> torch.Tensor | None:
    """pc{k} -> the single k-th PC [d,1]; dropk -> the top-k PCs [d,k]; none -> None."""
    if candidate == "none":
        return None
    if candidate.startswith("drop"):
        k = int(candidate.removeprefix("drop"))
        return principal_axes(sy, k)
    k = int(candidate.removeprefix("pc"))
    return principal_axes(sy, k + 1)[:, [k]]


def foscttm(model, vx, vy, seed=0) -> float:
    return retrieval_metrics(model, vx, vy, Randomness(seed))["foscttm"]


def default_kwargs(workers, smoke):
    kw = dict(num_workers=workers, num_threads=workers)
    if smoke:
        kw.update(num_clusters=10, num_restarts=3, batch_size=1500, num_iterations=5)
    return kw


def splits(corpus, language, seed, holdout, smoke):
    path_x, path_y = fetch(corpus, "vision", VISION_B), fetch(corpus, "language", language)
    n = num_rows(path_x)
    val_idx = torch.arange(n - holdout, n)
    ix, iy = disjoint_split(n - holdout, Randomness(seed), 3000 if smoke else None)
    sx, sy = load_rows(path_x, ix), load_rows(path_y, iy)
    vx, vy = load_rows(path_x, val_idx), load_rows(path_y, val_idx)
    return path_x, path_y, n, ix, iy, sx, sy, vx, vy


# --------------------------------------------------------------------------------------------------------------
# Synthetic smoke (laptop-safe: torch.randn only, never a real model or real embedding)
# --------------------------------------------------------------------------------------------------------------
def synthetic_smoke() -> dict:
    g = torch.Generator().manual_seed(0)
    x = torch.randn(3000, 32, generator=g)
    R = polar(torch.randn(32, 48, generator=g))                       # R R^T = I_32
    assert float((R @ R.T - torch.eye(32)).norm()) < 1e-5, "synthetic R not semi-orthogonal"
    mean_x = x.mean(0, keepdim=True)
    y = center_and_normalize(x, mean_x) @ R                           # exact rotation of centered-normalized X
    tx, vx = x[:2000], x[2000:]
    ty, vy = y[:2000], y[2000:]
    # (1) seed with the TRUE rotation, no refinement -> FOSCTTM ~ 0
    m_true = SeededWassersteinProcrustes(init_weight=R, refine=False, num_workers=1, num_threads=1).fit(
        tx, ty, None, None, Randomness(0))
    f_true = foscttm(m_true, vx, vy)
    assert f_true < 0.02, f"seeded-true-rotation not recovered (FOSCTTM {f_true})"
    # (2) seed with a perturbed rotation + refine -> should stay low (refinement does not break a good init)
    Rp = polar(R + 0.15 * torch.randn(32, 48, generator=g))
    m_ref = SeededWassersteinProcrustes(init_weight=Rp, refine=True, num_iterations=20, batch_size=2000,
                                        num_workers=1, num_threads=1).fit(tx, ty, None, None, Randomness(0))
    f_ref = foscttm(m_ref, vx, vy)
    assert f_ref < 0.10, f"seeded-perturbed+refine did not stay aligned (FOSCTTM {f_ref})"
    # (3) negative control: unrelated Y -> chance
    ybad = center_and_normalize(torch.randn(3000, 48, generator=g), None if False else torch.zeros(1, 48))
    m_bad = SeededWassersteinProcrustes(init_weight=R, refine=False, num_workers=1, num_threads=1).fit(
        tx, ybad[:2000], None, None, Randomness(0))
    f_bad = foscttm(m_bad, vx, ybad[2000:])
    assert f_bad > 0.35, f"negative control not near chance (FOSCTTM {f_bad})"
    # (4) trace path produces per-iterate S1 + FOSCTTM
    m_tr = SeededWassersteinProcrustes(init_weight=Rp, refine=True, num_iterations=5, batch_size=2000,
                                       num_workers=1, num_threads=1,
                                       trace_val=(vx, vy), trace_basis=None, trace_rows=1000).fit(
        tx, ty, None, None, Randomness(0))
    assert len(m_tr.trace) == 6 and all("foscttm" in e and "S1_matched_cosine" in e for e in m_tr.trace), "trace"
    # (5) text-text Procrustes recovers a known rotation (arm A building block)
    Rab = polar(torch.randn(48, 48, generator=g))
    a = center_and_normalize(torch.randn(2000, 48, generator=g), torch.zeros(1, 48))
    b = a @ Rab
    Rhat = polar(a.T @ b)
    assert float((Rhat - Rab).norm()) < 1e-3, "text-text Procrustes did not recover the rotation"
    return {"seeded_true_foscttm": f_true, "seeded_perturbed_refine_foscttm": f_ref,
            "negative_control_foscttm": f_bad, "textprocrustes_err": float((Rhat - Rab).norm()),
            "trace_len": len(m_tr.trace)}


# --------------------------------------------------------------------------------------------------------------
# Arms
# --------------------------------------------------------------------------------------------------------------
def arm_a(args, kwargs) -> tuple[str, dict, list]:
    """Pivot init via Qwen3-Embedding on the same captions (no image-text pairs). gen only."""
    rows = []
    corpus = args.corpus
    cand = args.candidate  # 'none' primary
    path_x = fetch(corpus, "vision", VISION_B)
    n = num_rows(path_x)
    val_idx = torch.arange(n - args.holdout, n)
    ix, iy = disjoint_split(n - args.holdout, Randomness(args.seed), 3000 if args.smoke else None)
    vx = load_rows(path_x, val_idx)
    gen_path, emb_path = fetch(corpus, "language", GEN), fetch(corpus, "language", EMB)
    sx_vis = load_rows(path_x, ix)
    sy_gen = load_rows(gen_path, iy)
    sy_emb = load_rows(emb_path, iy)
    vy_gen = load_rows(gen_path, val_idx)
    vy_emb = load_rows(emb_path, val_idx)
    if not args.smoke:
        print("smoke gate (gen):", smoke_gate(sx_vis, sy_gen, vx, vy_gen), flush=True)

    # 1) unpaired DINOv2<->Qwen3-Embedding map (their method; the pivot that works)
    emb_model = WassersteinProcrustes(**kwargs).fit(sx_vis, sy_emb, None, None, Randomness(args.seed))
    f_emb = foscttm(emb_model, vx, vy_emb, args.seed)  # control: should reproduce ~0.09 (E6)
    rows.append({"corpus": corpus, "arm": "A_emb_pivot_control", "candidate": "none", "foscttm_eval_only": f_emb})
    print(rows[-1], flush=True)

    # 2) text-text rotation emb->gen on the SAME captions (row i == row i; within one modality, no image pairs)
    pair_idx = torch.arange(0, n - args.holdout)
    emb_p = load_rows(emb_path, pair_idx)
    gen_p = load_rows(gen_path, pair_idx)
    mean_emb = emb_model.mean_y            # match the emb frame the emb_model outputs into
    mean_gen = sy_gen.float().mean(dim=0, keepdim=True)
    emb_c = center_and_normalize(emb_p.float(), mean_emb)
    gen_c = center_and_normalize(gen_p.float(), mean_gen)
    R = polar(emb_c.T @ gen_c)             # [d_emb, d_gen], emb -> gen
    r_err = float((R @ R.T - torch.eye(R.shape[0])).norm())
    # text-text self-check: how well does R align held-out emb to gen within the text modality?
    text_model = _FrozenMap(mean_emb, mean_gen, R, None)
    f_text = foscttm(text_model, vy_emb, vy_gen, args.seed)
    rows.append({"corpus": corpus, "arm": "A_text_text_emb_to_gen", "candidate": "none",
                 "foscttm_eval_only": f_text, "R_orth_err": r_err})
    print(rows[-1], flush=True)

    # 3) compose vision->emb (emb_model.weight) with emb->gen (R): init for the gen map
    W_init = emb_model.weight @ R          # [d_vis, d_gen]
    for refine, tag in ((False, "A_compose"), (True, "A_refine")):
        model = SeededWassersteinProcrustes(init_weight=W_init, refine=refine, **kwargs).fit(
            sx_vis, sy_gen, None, None, Randomness(args.seed))
        f = foscttm(model, vx, vy_gen, args.seed)
        rows.append({"corpus": corpus, "arm": tag, "candidate": cand, "foscttm_eval_only": f,
                     **unpaired_scores(Gated(model, None), sx_vis, sy_gen, args.seed)})
        print(rows[-1], flush=True)
    name = f"e7_armA-{corpus}-gen-{cand}" + (f"-seed{args.seed}" if args.seed else "")
    return name, {"n": n, "pivot_encoder": EMB}, rows


def arm_b(args, kwargs) -> tuple[str, dict, list]:
    """Transfer the SPC-fit rotation (raw + pc0-removed) to DCI/DOCCI: direct, and as a refinement init."""
    rows = []
    # fit the SPC gen maps once (none and pc0)
    spc_x, spc_y, _, six, siy, ssx, ssy, svx, svy = splits(SPC, GEN, args.seed, args.holdout, args.smoke)
    if not args.smoke:
        print("smoke gate (SPC gen):", smoke_gate(ssx, ssy, svx, svy), flush=True)
    W_spc, spc_models = {}, {}
    for cand in args.b_cands:
        basis = basis_for(cand, ssy)
        m = Gated(WassersteinProcrustes(**kwargs), basis).fit(ssx, ssy, Randomness(args.seed))
        spc_models[cand] = m
        W_spc[cand] = m.aligner.weight
        rows.append({"corpus": SPC, "arm": "B_spc_fit", "candidate": cand,
                     "foscttm_eval_only": foscttm(m, svx, svy, args.seed)})
        print(rows[-1], flush=True)

    for corpus in args.targets:
        tx, ty, tn, tix, tiy, tsx, tsy, tvx, tvy = splits(corpus, GEN, args.seed, args.holdout, args.smoke)
        # B_transfer: apply the SPC model directly (its own means + weight + its SPC-estimated basis)
        for cand in args.b_cands:
            f = foscttm(spc_models[cand], tvx, tvy, args.seed)
            rows.append({"corpus": corpus, "arm": "B_transfer", "candidate": cand, "foscttm_eval_only": f})
            print(rows[-1], flush=True)
        # B_refine: seed refinement on the TARGET from the SPC pc0 rotation, target pc0 projection
        basis_t = basis_for("pc0", tsy)
        model = Gated(SeededWassersteinProcrustes(init_weight=W_spc["pc0"], refine=True, **kwargs), basis_t).fit(
            tsx, tsy, Randomness(args.seed))
        rows.append({"corpus": corpus, "arm": "B_refine", "candidate": "pc0",
                     "foscttm_eval_only": foscttm(model, tvx, tvy, args.seed)})
        print(rows[-1], flush=True)
    name = f"e7_armB-SPCinit-gen" + (f"-seed{args.seed}" if args.seed else "")
    return name, {"targets": args.targets}, rows


def arm_c(args, kwargs) -> tuple[str, dict, list]:
    """Few true pairs (their Sec 4.4): k pairs -> Procrustes-seeded init woven into refinement."""
    rows = []
    corpus = args.corpus
    _, path_y, n, ix, iy, sx, sy, vx, vy = splits(corpus, GEN, args.seed, args.holdout, args.smoke)
    path_x = fetch(corpus, "vision", VISION_B)
    if not args.smoke:
        print("smoke gate (gen):", smoke_gate(sx, sy, vx, vy), flush=True)
    for cand in args.candidates:
        basis = basis_for(cand, sy)
        for k in args.ks:
            pidx = sample_pairs(n - args.holdout, k, Randomness(args.seed))
            px, py = load_rows(path_x, pidx), load_rows(path_y, pidx)
            model = Gated(WassersteinProcrustes(**kwargs), basis).fit(sx, sy, Randomness(args.seed), px, py)
            rows.append({"corpus": corpus, "arm": "C_fewpairs", "candidate": cand, "k_pairs": int(k),
                         "foscttm_eval_only": foscttm(model, vx, vy, args.seed)})
            print(rows[-1], flush=True)
    name = f"e7_armC-{corpus}-gen-{'-'.join(args.candidates)}-k{'-'.join(map(str, args.ks))}"
    name += f"-seed{args.seed}" if args.seed else ""
    return name, {"n": n, "ks": args.ks, "candidates": args.candidates}, rows


def arm_d(args, kwargs) -> tuple[str, dict, list]:
    """Pairs-free: remove the top-k PCs cumulatively (k=2..5), select by S1 (k=0/1 are none/pc0 from E6)."""
    rows = []
    corpus = args.corpus
    _, _, n, ix, iy, sx, sy, vx, vy = splits(corpus, GEN, args.seed, args.holdout, args.smoke)
    if not args.smoke:
        print("smoke gate (gen):", smoke_gate(sx, sy, vx, vy), flush=True)
    for k in args.ks:
        basis = principal_axes(sy, k)   # top-k PCs
        model = Gated(WassersteinProcrustes(**kwargs), basis).fit(sx, sy, Randomness(args.seed))
        rows.append({"corpus": corpus, "arm": "D_cumulative_dropk", "candidate": f"drop{k}", "k_removed": int(k),
                     **unpaired_scores(model, sx, sy, args.seed),
                     "foscttm_eval_only": foscttm(model, vx, vy, args.seed)})
        print(rows[-1], flush=True)
    name = f"e7_armD-{corpus}-gen-drop{'-'.join(map(str, args.ks))}" + (f"-seed{args.seed}" if args.seed else "")
    return name, {"n": n, "ks": args.ks}, rows


def arm_e(args, kwargs) -> tuple[str, dict, list]:
    """Pairs-free SELECTION of the fixed run: per-iterate S1 + true FOSCTTM for the BASELINE aligner (no init)."""
    rows = []
    corpus = args.corpus
    for language in args.encoders:
        _, _, n, ix, iy, sx, sy, vx, vy = splits(corpus, language, args.seed, args.holdout, args.smoke)
        cand = args.candidate
        basis = basis_for(cand, sy)
        proj = (lambda y, b=basis: y if b is None else y - (y @ b) @ b.T)
        aligner = SeededWassersteinProcrustes(
            init_weight=None, refine=True, trace_val=(vx, vy), trace_basis=basis,
            trace_rows=min(2000, n - args.holdout), **kwargs)
        aligner.fit(sx, proj(sy.float()), None, None, Randomness(args.seed))
        trace = aligner.trace
        last = trace[-1]
        best = min(trace, key=lambda e: e["foscttm"])
        best_s1 = max(trace, key=lambda e: e["S1_matched_cosine"])
        rows.append({
            "corpus": corpus, "language": SHORT.get(language, language), "candidate": cand, "seed": args.seed,
            "arm": "E_trace_baseline", "n_iters": len(trace) - 1,
            "foscttm_last": last["foscttm"], "foscttm_best": best["foscttm"], "best_iter": best["iter"],
            "foscttm_at_bestS1": best_s1["foscttm"], "bestS1_iter": best_s1["iter"],
            "S1_last": last["S1_matched_cosine"], "S1_best": best_s1["S1_matched_cosine"],
            "trace": trace,
        })
        print({k: v for k, v in rows[-1].items() if k != "trace"}, flush=True)
    name = f"e7_armE-{corpus}-{args.candidate}" + (f"-seed{args.seed}" if args.seed else "")
    return name, {"encoders": args.encoders, "candidate": args.candidate}, rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--arm", choices=["a", "b", "c", "d", "e"])
    parser.add_argument("--corpus", default="DenselyCaptionedImages")
    parser.add_argument("--targets", nargs="*", default=["DenselyCaptionedImages", "DOCCIDataset"])
    parser.add_argument("--encoders", nargs="*", default=[GEN, EMB, "mpnet"])
    parser.add_argument("--candidate", default="none")
    parser.add_argument("--candidates", nargs="*", default=["none"])
    parser.add_argument("--b-cands", nargs="*", default=["none", "pc0"])
    parser.add_argument("--ks", nargs="*", type=int, default=[1, 5, 10, 50, 100])
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--holdout", type=int, default=2000)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--synthetic-smoke", action="store_true")
    parser.add_argument("--manifest-sha256", default="")
    args = parser.parse_args()

    if args.synthetic_smoke:
        print("synthetic smoke:", synthetic_smoke(), flush=True)
        return

    kwargs = default_kwargs(args.workers, args.smoke)
    dispatch = {"a": arm_a, "b": arm_b, "c": arm_c, "d": arm_d, "e": arm_e}
    name, extra, rows = dispatch[args.arm](args, kwargs)
    if args.smoke:
        name += "-smoke"
    config = {**{k: v for k, v in vars(args).items() if k != "manifest_sha256"},
              "manifest_sha256": args.manifest_sha256, "vision": VISION_B, "aligner_kwargs": kwargs, **extra}
    print("receipt:", receipt(name, config, {"rows": rows}, OUT))


if __name__ == "__main__":
    main()
