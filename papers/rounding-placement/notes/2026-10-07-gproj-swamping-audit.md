# GProj and swamping: reference and implementation audit

A fresh paired Saturn replay confirms that centering and GProj address
different numerical channels. Integer phase alone leaves the ordinary-position
backward error essentially unchanged. Full results, controls, custody, and
historical continuation reanalysis are in
[the experiment findings](../../../../saturn/experiments/2026-10-07-attention-conservation-swamping/FINDINGS.md).

At Pythia-160m step143000, two fresh 256-token windows, median layer dQ error
against FP64 at the **same BF16 operands** falls from 3.05% to 0.125% with
correct actual-mass GProj. Against the **original FP32 operands**, centering
reduces median error from 17.08% to 1.28%, or 1.25% with GProj added. The
combined worst-layer original-input error remains 20.8%.

The draft should distinguish those references wherever it compares forward
centering with the published backward repair. Our original-input metric
includes lost forward operand information. It cannot rank methods on the
paper's fixed-BF16-input metric or establish superiority in long training.

The older gauge/phase helpers omit normalization by actual BF16 probability
mass. The training continuation's `QAttn.backward` also discards projected dS
on the ordinary non-native dK path (`exact_accum_worker.py:274`), and its dQ
projection uses unrounded P. Therefore the sentence that the row-sum step is
inert on training loss is a description of that historical implementation;
it is not a tested result for full published GProj. Keep the raw results and
historical sources unchanged, and attach this correction to their interpretation.

The three historical data orders still show a centering-only final held-out
loss benefit averaging 0.0499 nats/token after 1,000 steps. They do not test
the long-run regime in which Chen et al. report key-smoothing instability.
The defensible scope is complementary repairs plus bounded local training
benefit, with the broader instability-prevention claim still unestablished.
