"""The paper's WassersteinProcrustes, instrumented to record the weight at every iterate.

The arithmetic and the randomness consumption are identical to the stock aligner (verbatim copy of ``_fit`` from
``unpaired_rosetta.wasserstein_procrustes`` at commit fdfad84), so the final weight -- and hence the reported
FOSCTTM -- is bit-for-bit the same. The only addition is ``self.trajectory``: the weight after the read-out
(iterate 0) and after each of the R refinement steps (iterates 1..R). Nothing uses the true pairs.
"""

from __future__ import annotations

import torch

from unpaired_rosetta.determinism import torch_threads
from unpaired_rosetta.geometric_initialization import GeometricInitialization
from unpaired_rosetta.linalg import center_and_normalize
from unpaired_rosetta.randomness import Randomness
from unpaired_rosetta.wasserstein_procrustes import WassersteinProcrustes


class LoggedWassersteinProcrustes(WassersteinProcrustes):
    """Same aligner, plus ``trajectory``: the list of weights [R+1] and the centered-normalized training sets."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.trajectory: list[torch.Tensor] = []
        self.train_x = None  # centered + normalized training X, as the refinement sees it
        self.train_y = None

    @torch.inference_mode()
    def fit(self, samples_x, samples_y, paired_x=None, paired_y=None, randomness=0):
        if not isinstance(randomness, Randomness):
            randomness = Randomness(randomness)
        with torch_threads():
            return self._fit(samples_x, samples_y, paired_x, paired_y, randomness)

    def _fit(self, samples_x, samples_y, paired_x, paired_y, randomness):
        samples_x, samples_y = samples_x.float(), samples_y.float()
        self.mean_x = samples_x.mean(dim=0, keepdim=True)
        self.mean_y = samples_y.mean(dim=0, keepdim=True)
        samples_x = center_and_normalize(samples_x, self.mean_x)
        samples_y = center_and_normalize(samples_y, self.mean_y)
        self.train_x, self.train_y = samples_x, samples_y
        if paired_x is not None and paired_x.shape[0] > 0:
            paired_x = center_and_normalize(paired_x.float(), self.mean_x)
            paired_y = center_and_normalize(paired_y.float(), self.mean_y)
        else:
            paired_x = paired_y = None

        initialization = GeometricInitialization(
            self.num_clusters, self.num_restarts, self.batch_size, self.num_workers
        )
        correspondence = initialization(samples_x, samples_y, paired_x, paired_y, randomness)
        weight = self.readout(samples_x, samples_y, correspondence, paired_x, paired_y, randomness)
        self.trajectory = [weight.clone()]
        for _ in range(self.num_iterations):
            weight = self.refinement_step(samples_x, samples_y, weight, paired_x, paired_y, randomness)
            self.trajectory.append(weight.clone())
        self.weight = weight
        return self
