"""Shared helpers: their evaluation protocol, their embeddings, and the quantities our claims are about.

Everything that decides a number in their paper (splits, preprocessing, the aligner, FOSCTTM) is imported from
their library at the pinned commit, so a difference between our numbers and theirs can only come from the arm we
change. The functions defined here are the new measurements: per-pair fidelity ``alpha``, captured energy of a pair
span, and the projection-oracle FOSCTTM of a span.
"""

from __future__ import annotations

import json
import os
import platform
import subprocess
import time
from pathlib import Path

EXPERIMENTS = Path(__file__).resolve().parents[1]
os.environ.setdefault("UNPAIRED_ROSETTA_ROOT", str(EXPERIMENTS / ".storage"))

import torch  # noqa: E402
from torch import Tensor  # noqa: E402

from unpaired_rosetta.embeddings import embedding_path, load_rows, num_rows  # noqa: E402
from unpaired_rosetta.evaluation import disjoint_split, retrieval_metrics, sample_pairs  # noqa: E402
from unpaired_rosetta.linalg import center_and_normalize  # noqa: E402
from unpaired_rosetta.randomness import Randomness  # noqa: E402

HF_REPOSITORY = "schnaus/unpaired-rosetta-embeddings"
THEIR_COMMIT = "fdfad84ea488f29702a61a455be71622c4ff5d49"
VISION_B = "dinov2_vit-b14@224_mean"
QWEN3_GEN_8B = "qwen3-8b-gen_69445574b3021b8a2733e87d8603d769"


def storage_root() -> Path:
    return Path(os.environ["UNPAIRED_ROSETTA_ROOT"])


def fetch(dataset: str, modality: str, model: str) -> Path:
    """Download one stored embedding file from their Hugging Face dataset (skipped if present)."""
    path = embedding_path(dataset, modality, model)
    if not path.exists():
        from huggingface_hub import hf_hub_download

        relative = path.relative_to(storage_root()).as_posix()
        hf_hub_download(HF_REPOSITORY, relative, repo_type="dataset", local_dir=storage_root())
    return path


def training_data(
    dataset: str,
    model_x: str,
    model_y: str,
    randomness: Randomness,
    train_size: int | None = None,
    num_pairs: int = 0,
    pair_indices: Tensor | None = None,
) -> tuple[Tensor, Tensor, Tensor | None, Tensor | None]:
    """Their ``load_training_data`` (experiments/alignment.py) for the vision/language setting.

    ``pair_indices`` replaces their random ``sample_pairs`` draw when an arm chooses the pairs itself (E2).
    """
    path_x, path_y = fetch(dataset, "vision", model_x), fetch(dataset, "language", model_y)
    indices_x, indices_y = disjoint_split(num_rows(path_x), randomness, train_size)
    samples_x, samples_y = load_rows(path_x, indices_x), load_rows(path_y, indices_y)
    if pair_indices is None and num_pairs == 0:
        return samples_x, samples_y, None, None
    if pair_indices is None:
        pair_indices = sample_pairs(num_rows(path_x), num_pairs, randomness)
    return samples_x, samples_y, load_rows(path_x, pair_indices), load_rows(path_y, pair_indices)


def validation_data(
    dataset: str,
    model_x: str,
    model_y: str,
    seed: int,
    size: int | None = None,
) -> tuple[Tensor, Tensor, Randomness]:
    """Their ``load_validation_data``: row-aligned validation pairs, drawn with a fresh ``Randomness(seed)``."""
    randomness = Randomness(seed)
    path_x, path_y = fetch(dataset, "vision", model_x), fetch(dataset, "language", model_y)
    indices = randomness.subset(num_rows(path_x), size)
    return load_rows(path_x, indices), load_rows(path_y, indices), randomness


def foscttm(aligner, val_x: Tensor, val_y: Tensor, randomness: Randomness) -> float:
    return retrieval_metrics(aligner, val_x, val_y, randomness)["foscttm"]


# ---------------------------------------------------------------------------------------------------------------
# New measurements
# ---------------------------------------------------------------------------------------------------------------


@torch.inference_mode()
def alpha(mapped_x: Tensor, keys_y: Tensor) -> Tensor:
    """Per-pair fidelity ``alpha_i = cos(map(x_i), y_i)`` for row-aligned mapped queries and preprocessed keys.

    FOSCTTM only asks whether ``y_i`` outranks the other keys; a consumer that is *driven* by ``map(x_i)``
    (a generator conditioned on it) sees ``alpha_i`` of the true signal and ``sqrt(1 - alpha_i^2)`` of something
    else. This is the quantity the read/author distinction is about (response.md, Claim D).
    """
    mapped = torch.nn.functional.normalize(mapped_x.double(), dim=-1)
    keys = torch.nn.functional.normalize(keys_y.double(), dim=-1)
    return (mapped * keys).sum(-1)


def quantiles(values: Tensor, qs=(0.05, 0.25, 0.5, 0.75, 0.95)) -> dict[str, float]:
    values = values.double()
    out = {f"q{int(q * 100):02d}": float(torch.quantile(values, q)) for q in qs}
    out["mean"] = float(values.mean())
    return out


def span_basis(rows: Tensor) -> Tensor:
    """Orthonormal basis ``[d, r]`` of the row span of ``rows`` (``r <= p``)."""
    q, r = torch.linalg.qr(rows.double().T)
    keep = r.diagonal().abs() > 1e-10 * r.diagonal().abs().max().clamp(min=1e-300)
    return q[:, keep]


def captured_energy(keys: Tensor, basis: Tensor) -> Tensor:
    """``||P y_i||^2`` per unit key: the share of each key that a span-confined map can reproduce at all."""
    keys = torch.nn.functional.normalize(keys.double(), dim=-1)
    return ((keys @ basis) ** 2).sum(-1)


def top_eigen_energy(keys: Tensor, p: int) -> float:
    """Ky Fan ceiling: the most energy any ``p``-dim subspace can capture, ``sum_{k<=p} lambda_k / sum lambda``."""
    keys = torch.nn.functional.normalize(keys.double(), dim=-1)
    eigenvalues = torch.linalg.svdvals(keys) ** 2
    return float(eigenvalues[:p].sum() / eigenvalues.sum())


class ProjectionOracle:
    """Scores ``<P y_i, y_j>``: each true key, projected onto a span, is used as its own query.

    Call it as ``retrieval_metrics(oracle, val_y, val_y, randomness)``: the "queries" are the true partners. This is
    the natural best query inside the span, not a proven optimum (response.md, Claim C), so it is reported next to
    the measured baselines and never in place of them.
    """

    def __init__(self, basis: Tensor, mean_y: Tensor) -> None:
        self.basis, self.mean_y = basis, mean_y

    def similarity(self, queries_y: Tensor, keys_y: Tensor) -> Tensor:
        queries = center_and_normalize(queries_y.float(), self.mean_y).double()
        projected = (queries @ self.basis) @ self.basis.T
        return projected @ center_and_normalize(keys_y.float(), self.mean_y).double().T


def receipt(name: str, config: dict, results: dict, out_dir: Path) -> Path:
    """Write ``results/<name>/<timestamp>.json`` with the config, the numbers and the software versions."""
    import numpy
    import scipy
    import sklearn

    try:
        ours = subprocess.run(
            ["git", "-C", str(EXPERIMENTS), "rev-parse", "HEAD"], capture_output=True, text=True, check=False
        ).stdout.strip()
    except OSError:
        ours = ""
    record = {
        "experiment": name,
        "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "config": config,
        "results": results,
        "software": {
            "their_commit": THEIR_COMMIT,
            "our_commit": ours,
            "python": platform.python_version(),
            "torch": torch.__version__,
            "numpy": numpy.__version__,
            "scipy": scipy.__version__,
            "sklearn": sklearn.__version__,
            "host": platform.node(),
        },
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{name}-{time.strftime('%Y%m%dT%H%M%S')}.json"
    path.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    return path
