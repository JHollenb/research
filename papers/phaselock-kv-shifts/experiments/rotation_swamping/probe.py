"""Rotation swamping under repeated one-position rerotation with rounded storage.

Qwen2.5 RoPE frequencies (theta=1e6, head_dim=128). Random keys are rotated to
position p0, then rerotated by -1 position n times with an FP32 twiddle (or a
BF16-rounded twiddle) and rounded to the storage dtype after every step. Reports
mean relative key error and norm ratio versus direct RoPE, and, per channel pair,
the fraction of the intended rotation actually achieved. Prediction: a pair whose
per-step change omega*|k| is below half a storage ulp (omega < 2^-9 for BF16,
2^-11 for FP16) is rounded back to its old value, so its rotation is lost.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import torch

D = 128
INV = 1.0 / (1e6 ** (np.arange(0, D, 2) / D))


def rot(x, ang):
    c, s = torch.cos(ang), torch.sin(ang)
    x1, x2 = x[..., :64], x[..., 64:]
    return torch.cat([x1 * c - x2 * s, x2 * c + x1 * s], -1)


def run(store, twiddle, n_max=1024, p0=2000, n_keys=4096, seed=0):
    torch.manual_seed(seed)
    k = torch.randn(n_keys, D, dtype=torch.float64)
    c = torch.cos(torch.tensor(-INV)).float()
    s = torch.sin(torch.tensor(-INV)).float()
    if twiddle == "bf16":
        c, s = c.bfloat16().float(), s.bfloat16().float()
    x = rot(k, torch.tensor(p0 * INV)).to(store).float()
    start = x.clone()
    rows = []
    for n in range(1, n_max + 1):
        x = torch.cat([x[:, :64] * c - x[:, 64:] * s, x[:, 64:] * c + x[:, :64] * s], -1).to(store).float()
        if n in (1, 4, 16, 64, 256, 1024):
            ex = rot(k, torch.tensor((p0 - n) * INV))
            rows.append({"n": n,
                         "mean_rel_error": float(((x.double() - ex).norm(dim=-1) / ex.norm(dim=-1)).mean()),
                         "mean_norm_ratio": float((x.double().norm(dim=-1) / ex.norm(dim=-1)).mean())})
        if n == 256:
            z0 = torch.complex(start[:, :64].double(), start[:, 64:].double())
            z = torch.complex(x[:, :64].double(), x[:, 64:].double())
            achieved = torch.angle(z * z0.conj()).mean(0).numpy()
            expected = (-n * INV + np.pi) % (2 * np.pi) - np.pi
            frac = (achieved / expected).tolist()
    return rows, frac


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    out = {"schema": "phaselock-rotation-swamping-v1", "omega": INV.tolist(), "arms": {}}
    for name, store, tw in [("fp32_twiddle_bf16_store", torch.bfloat16, "fp32"),
                            ("bf16_twiddle_bf16_store", torch.bfloat16, "bf16"),
                            ("fp32_twiddle_fp16_store", torch.float16, "fp32"),
                            ("fp32_twiddle_fp32_store", torch.float32, "fp32")]:
        rows, frac = run(store, tw)
        out["arms"][name] = {"trajectory": rows, "achieved_rotation_fraction_at_256": frac}
    for name, ulp in (("bf16", 2 ** -8), ("fp16", 2 ** -10)):
        out[f"pairs_below_half_ulp_{name}"] = int((INV < ulp / 2).sum())
    out["random_walk_prediction_bf16_n1024"] = float(np.sqrt(1024) * 2 ** -9 / np.sqrt(3))
    args.out.write_text(json.dumps(out, indent=1))
    for k, v in out["arms"].items():
        f = np.array(v["achieved_rotation_fraction_at_256"])
        print(k, [round(r["mean_rel_error"], 4) for r in v["trajectory"]],
              "swamped-pair mean frac %.3f" % f[INV < 2 ** -9].mean())


if __name__ == "__main__":
    main()
