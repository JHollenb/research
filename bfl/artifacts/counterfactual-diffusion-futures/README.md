# Counterfactual diffusion futures: evidence bundle

This bundle contains the replicated four-specimen panel for editing saved diffusion trajectories.
Each specimen has a source prompt, a matching donor prompt, a hostile donor, a norm-matched sham,
early and late checkpoint cuts, a dose curve, exact scalar confirmation, and rollback checks.

The report defines progress as normalized image distance toward the donor image, so the hostile
donor is a key control: a generic perturbation would not selectively move toward its own target.
The four PNGs are compact visual proof sheets for scene and subject transfer at two seeds each.

Run `python verify.py` from this directory. It verifies the reported specimen-level gates and
does not infer a universal timing law or portable edit package.
