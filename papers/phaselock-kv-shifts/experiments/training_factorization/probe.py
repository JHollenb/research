"""Small CPU algebra probe, not a model-training or throughput experiment.

Run through common/bin/common exec python. Checks relative-phase attention,
projection-bias expansion, tile frames, their parameter gradients, softmax
pairwise factorization, and exact integer conservation before float casting.
The integer phase code below is an explicit mathematical reference, not an SPF
runtime implementation or a production kernel.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import torch


torch.set_num_threads(1)
torch.set_default_dtype(torch.float64)
torch.manual_seed(34272)


def rotations(angles: torch.Tensor) -> torch.Tensor:
    c, s = angles.cos(), angles.sin()
    return torch.stack((c, -s, s, c), -1).reshape(*angles.shape, 2, 2)


def rotate(x: torch.Tensor, angles: torch.Tensor) -> torch.Tensor:
    return torch.einsum("...mab,...mb->...ma", rotations(angles), x)


def phase_words(positions: list[int], frequencies: list[int], bits: int = 32):
    mask = (1 << bits) - 1
    return [[(p * f) & mask for f in frequencies] for p in positions]


def relative_angles(positions: list[int], frequencies: list[int], bits: int = 32):
    # Python integer products prevent overflow in this mathematical reference.
    modulus = 1 << bits
    return torch.tensor([
        [[((pj - pi) * f) % modulus * (2 * math.pi / modulus)
          for f in frequencies] for pj in positions] for pi in positions
    ])


def max_difference(a: torch.Tensor, b: torch.Tensor) -> float:
    return (a - b).abs().max().item()


def main() -> None:
    n, width, pairs, value_width = 6, 5, 3, 4
    x = torch.randn(n, width)
    params = [torch.randn(2 * pairs, width, requires_grad=True),
              torch.randn(2 * pairs, width, requires_grad=True),
              torch.randn(value_width, width, requires_grad=True),
              torch.randn(2 * pairs, requires_grad=True),
              torch.randn(2 * pairs, requires_grad=True),
              torch.randn(value_width, requires_grad=True)]
    wq, wk, wv, bq, bk, bv = params
    q = (x @ wq.T + bq).reshape(n, pairs, 2)
    k = (x @ wk.T + bk).reshape(n, pairs, 2)
    v = x @ wv.T + bv
    omega = torch.tensor([0.7, 0.003, 0.0000019], requires_grad=True)
    pos = torch.tensor([0, 1, 3, 7, 10, 15])
    angles = pos[:, None] * omega[None, :]
    delta = (pos[None, :] - pos[:, None])[:, :, None] * omega
    scale = 1 / math.sqrt(2 * pairs)
    dense = torch.einsum("ima,jma->ij", rotate(q, angles), rotate(k, angles)) * scale
    relative = (q[:, None] * rotate(k[None, :], delta)).sum((-1, -2)) * scale

    c = q[:, None, :, 0] * k[None, :, :, 0] + q[:, None, :, 1] * k[None, :, :, 1]
    d = q[:, None, :, 1] * k[None, :, :, 0] - q[:, None, :, 0] * k[None, :, :, 1]
    expanded_pairs = (c * delta.cos() + d * delta.sin()).sum(-1) * scale

    q0, k0 = (x @ wq.T).reshape(n, pairs, 2), (x @ wk.T).reshape(n, pairs, 2)
    bqp, bkp = bq.reshape(pairs, 2), bk.reshape(pairs, 2)
    expanded_bias = sum([
        (q0[:, None] * rotate(k0[None, :], delta)).sum((-1, -2)),
        (q0[:, None] * rotate(bkp, delta)).sum((-1, -2)),
        (bqp * rotate(k0[None, :], delta)).sum((-1, -2)),
        (bqp * rotate(bkp, delta)).sum((-1, -2)),
    ]) * scale

    # Drop q_i^T b_K, a common logit offset for each query, BEFORE rounding.
    # cos(delta)-1 is evaluated without subtracting two nearly equal floats.
    bias_generator = torch.tensor([[0., -1.], [1., 0.]])
    rotated_bias_residual = (-2 * (delta / 2).sin().square())[..., None] * bkp
    rotated_bias_residual = rotated_bias_residual + delta.sin()[..., None] * torch.einsum("ab,mb->ma", bias_generator, bkp)
    bias_cancelled_scores = (q[:, None] * (rotate(k0[None, :], delta)
                                         + rotated_bias_residual)).sum((-1, -2)) * scale

    page_origins = torch.tensor([0, 0, 0, 7, 7, 7])
    local_angles = (pos - page_origins)[:, None] * omega
    tile_delta = (page_origins[None, :] - page_origins[:, None])[:, :, None] * omega
    qpage, kpage = rotate(q, local_angles), rotate(k, local_angles)
    page = (qpage[:, None] * rotate(kpage[None, :], tile_delta)).sum((-1, -2)) * scale

    mask = torch.ones(n, n, dtype=torch.bool).triu(1)
    upstream = torch.randn(n, value_width)

    def consume(scores):
        p = scores.masked_fill(mask, -torch.inf).softmax(-1)
        return ((p @ v) * upstream).sum()

    targets = params + [omega]
    dense_grads = torch.autograd.grad(consume(dense), targets, retain_graph=True)
    relative_grads = torch.autograd.grad(consume(relative), targets, retain_graph=True)
    page_grads = torch.autograd.grad(consume(page), targets, retain_graph=True)
    bias_cancelled_grads = torch.autograd.grad(consume(bias_cancelled_scores), targets, retain_graph=True)
    named = ["WQ", "WK", "WV", "bQ", "bK", "bV", "omega"]

    p = relative.masked_fill(mask, -torch.inf).softmax(-1)
    a = upstream @ v.T
    g = p * (a - (p * a).sum(-1, keepdim=True))
    manual_dq = (g[:, :, None, None] * rotate(k[None, :], delta)).sum(1) * scale
    manual_dk = (g[:, :, None, None] * rotate(q[:, None], -delta)).sum(0) * scale
    direct_dq, direct_dk = torch.autograd.grad(consume(relative), (q, k), retain_graph=True)

    rotated_k = rotate(k, angles).flatten(1)
    direct_rotary_query_grad = scale * g @ rotated_k
    pairwise = torch.zeros_like(direct_rotary_query_grad)
    for i in range(n):
        for j in range(i + 1):
            for ell in range(j + 1, i + 1):
                pairwise[i] += (scale * p[i, j] * p[i, ell]
                                * (a[i, j] - a[i, ell])
                                * (rotated_k[j] - rotated_k[ell]))

    generator = torch.tensor([[0., -1.], [1., 0.]])
    rotated_relative_k = rotate(k[None, :], delta)
    tangent = torch.einsum("ab,ijmb->ijma", generator, rotated_relative_k)
    manual_frequency_grad = (scale * g[:, :, None]
                             * (pos[None, :] - pos[:, None])[:, :, None]
                             * (q[:, None] * tangent).sum(-1)).sum((0, 1))

    frequencies = [round((1 << 32) * w / (2 * math.pi)) for w in omega.detach().tolist()]
    relative0 = relative_angles(pos.tolist(), frequencies)
    integer_scores0 = (q[:, None] * rotate(k[None, :], relative0)).sum((-1, -2)) * scale
    integer_grads0 = torch.autograd.grad(consume(integer_scores0), params, retain_graph=True)
    offset_rows = []
    for offset in [1 << 24, 1 << 32, 5_000_000_000, 1 << 60]:
        shifted = [int(p) + offset for p in pos.tolist()]
        words = phase_words(shifted, frequencies)
        difference_words = [[[(words[j][m] - words[i][m]) % (1 << 32)
                              for m in range(pairs)] for j in range(n)] for i in range(n)]
        shifted_angles = relative_angles(shifted, frequencies)
        shifted_scores = (q[:, None] * rotate(k[None, :], shifted_angles)).sum((-1, -2)) * scale
        shifted_grads = torch.autograd.grad(consume(shifted_scores), params, retain_graph=True)
        offset_rows.append({"offset": offset,
                            "max_relative_angle_difference": max_difference(relative0, shifted_angles),
                            "max_score_difference": max_difference(integer_scores0, shifted_scores),
                            "max_parameter_gradient_difference": max(max_difference(a, b) for a, b in zip(integer_grads0, shifted_grads)),
                            "word_difference_identity": difference_words == phase_words_differences(pos.tolist(), frequencies)})

    no_rope_scores = torch.einsum("ima,jma->ij", q, k) * scale
    no_rope_key_bias_grad, = torch.autograd.grad(consume(no_rope_scores), (bk,), retain_graph=True)

    logaq = torch.randn(n, pairs, requires_grad=True)
    logak = torch.randn(n, pairs, requires_grad=True)
    phiq = torch.randn(n, pairs, requires_grad=True)
    phik = torch.randn(n, pairs, requires_grad=True)
    phase_delta = phik[None, :] - phiq[:, None] + delta.detach()
    amplitude_product = (logaq[:, None] + logak[None, :]).exp()
    polar_scores = scale * (amplitude_product * phase_delta.cos()).sum(-1)
    polar_p = polar_scores.masked_fill(mask, -torch.inf).softmax(-1)
    polar_g = polar_p * (a - (polar_p * a).sum(-1, keepdim=True))
    polar_autograd = torch.autograd.grad(consume(polar_scores), (logaq, logak, phiq, phik), retain_graph=True)
    amplitude_terms = scale * polar_g[:, :, None] * amplitude_product * phase_delta.cos()
    phase_terms = scale * polar_g[:, :, None] * amplitude_product * phase_delta.sin()
    polar_manual = (amplitude_terms.sum(1), amplitude_terms.sum(0), phase_terms.sum(1), -phase_terms.sum(0))

    eta = 3 / 1024
    exact_g = torch.tensor([1 + eta, -1., -eta, 0.])
    cast_g = exact_g.to(torch.bfloat16).double()
    probabilities = torch.full((4,), 0.25).to(torch.bfloat16).double()
    rho, mass = cast_g.sum(), probabilities.sum()
    projected = cast_g - rho / mass * probabilities
    leak_rows = []
    for common_key in [0, 256, 65536, 1_048_576]:
        witness_k = torch.tensor([[common_key, j] for j in range(4)], dtype=torch.float64)
        leak_rows.append({"common_key": common_key,
                          "exact_first_coordinate": (exact_g @ witness_k / 8)[0].item(),
                          "bf16_operand_first_coordinate": (cast_g @ witness_k / 8)[0].item(),
                          "projected_first_coordinate": (projected @ witness_k / 8)[0].item()})

    # Rational surrogate softmax Jacobian: integer mass and centered numerator.
    numerators = [1, 1, 1, 1]
    value_scale = 256
    integer_values = [1027, -1024, -3, 0]
    total_mass = sum(numerators)
    center_numerator = sum(n * a for n, a in zip(numerators, integer_values))
    conserved = [n * (total_mass * a - center_numerator)
                 for n, a in zip(numerators, integer_values)]
    reconstructed = torch.tensor(conserved) / (value_scale * total_mass**2)

    out = {
        "scope": "CPU float64 mathematical mechanics; no pretrained model, optimizer trajectory, or GPU timing",
        "seed": 34272,
        "torch_version": torch.__version__,
        "score_max_abs_differences": {"relative": max_difference(dense, relative),
                                      "pair_expansion": max_difference(dense, expanded_pairs),
                                      "bias_expansion": max_difference(dense, expanded_bias),
                                      "page_frames": max_difference(dense, page)},
        "parameter_gradient_max_abs_differences": {
            name: {"relative": max_difference(dg, rg), "page_frames": max_difference(dg, pg),
                   "analytical_bias_cancellation": max_difference(dg, bg)}
            for name, dg, rg, pg, bg in zip(named, dense_grads, relative_grads, page_grads, bias_cancelled_grads)},
        "analytical_bias_cancellation": {
            "probability_max_abs_difference": max_difference(dense.masked_fill(mask, -torch.inf).softmax(-1),
                                                            bias_cancelled_scores.masked_fill(mask, -torch.inf).softmax(-1)),
            "logit_row_shift_identity_max_abs_difference": max_difference(dense - (q * bkp).sum((-1, -2))[:, None] * scale,
                                                                         bias_cancelled_scores),
            "note": "Linear pre-RoPE key bias only. This changes floating-point execution while preserving real-arithmetic probabilities and parameter gradients. Not a general replacement for GProj."},
        "manual_backward_max_abs_differences": {"dq": max_difference(direct_dq, manual_dq),
                                               "dk": max_difference(direct_dk, manual_dk),
                                               "omega": max_difference(relative_grads[-1], manual_frequency_grad)},
        "pairwise_gradient_max_abs_difference": max_difference(pairwise, direct_rotary_query_grad),
        "integer_relative_phase_offsets": offset_rows,
        "key_bias_gradient_norm": {"with_rope": dense_grads[4].norm().item(),
                                   "without_rope": no_rope_key_bias_grad.norm().item(),
                                   "note": "A pre-RoPE key bias is not a common post-RoPE key translation. Its gradient need not vanish."},
        "learned_polar_coordinate_adjoint": {
            "max_abs_difference": max(max_difference(a, b) for a, b in zip(polar_autograd, polar_manual)),
            "common_content_phase_gradient_sum_max_abs": (polar_autograd[2].sum(0) + polar_autograd[3].sum(0)).abs().max().item(),
            "note": "Smooth explanatory coordinates with independent log amplitudes and angles; no integer quantization, polar storage, or model training claim."},
        "bf16_row_mass": rho.item(),
        "common_key_leak": leak_rows,
        "integer_centered_numerator": {"sum": sum(conserved),
                                       "score_gradient_max_abs_difference": max_difference(exact_g, reconstructed),
                                       "note": "Conservation before conversion is exact. Rounding each reconstructed operand to BF16 breaks it again. This is a quantized surrogate, not the derivative of literal integer rounding."},
        "frequency_error_angle_bounds": {str(r): math.pi * r / (1 << 32)
                                         for r in [32768, 131072, 1 << 24, 5_000_000_000]},
    }
    destination = Path(__file__).with_name("mechanics.json")
    destination.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))


def phase_words_differences(positions: list[int], frequencies: list[int]):
    modulus = 1 << 32
    return [[[(pj - pi) * f % modulus for f in frequencies]
             for pj in positions] for pi in positions]


if __name__ == "__main__":
    main()
