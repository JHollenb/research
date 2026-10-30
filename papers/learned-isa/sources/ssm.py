"""Small CPU reference SSM mixers; no CUDA kernels or pretrained checkpoints.

Mamba-style: selective diagonal recurrence, causal convolution, gated readout.
Hydra-style: shared noncausal convolution, separate directional B/C/delta,
one-position shifted forward/reverse SSD scans and content-dependent diagonal.
See docs/ssm-and-native-contract.md for upstream equations and boundaries.
"""
from __future__ import annotations

import math

import torch
from torch import nn
from torch.nn import functional as F


def selective_scan(x, dt, a, b, c):
    """Associative prefix scan of h[t]=exp(dt*A)h[t-1]+dt*B*x.

    Shapes: x,dt [batch,length,channels], A [channels,state], B,C
    [batch,length,state]. The doubling schedule avoids divisions by tiny
    cumulative products and is differentiable through every selective writer.
    """
    decay = torch.exp(dt.unsqueeze(-1) * a)
    state = dt.unsqueeze(-1) * x.unsqueeze(-1) * b.unsqueeze(-2)
    stride = 1
    while stride < x.shape[1]:
        old_decay, old_state = decay, state
        state = torch.cat((old_state[:, :stride], old_state[:, stride:] +
                           old_decay[:, stride:] * old_state[:, :-stride]), dim=1)
        decay = torch.cat((old_decay[:, :stride], old_decay[:, stride:] * old_decay[:, :-stride]), dim=1)
        stride *= 2
    return (state * c.unsqueeze(-2)).sum(-1)


def rms(x):
    return x * torch.rsqrt(x.square().mean(-1, keepdim=True) + 1e-5)


class MambaMixer(nn.Module):
    def __init__(self, width=16, state=4, expansion=2, kernel=3):
        super().__init__()
        inner = width * expansion
        self.inner, self.state, self.kernel = inner, state, kernel
        self.in_proj = nn.Linear(width, 2 * inner)
        self.conv = nn.Conv1d(inner, inner, kernel, groups=inner, padding=kernel - 1)
        self.select = nn.Linear(inner, 1 + 2 * state, bias=False)
        self.dt_proj = nn.Linear(1, inner)
        self.a_log = nn.Parameter(torch.log(torch.arange(1, state + 1).float()).repeat(inner, 1))
        self.d = nn.Parameter(torch.ones(inner))
        self.out_proj = nn.Linear(inner, width)
        with torch.no_grad():
            dt = torch.exp(torch.empty(inner).uniform_(math.log(.001), math.log(.1)))
            self.dt_proj.bias.copy_(dt + torch.log(-torch.expm1(-dt)))

    def forward(self, tokens):
        u, gate = self.in_proj(rms(tokens)).chunk(2, -1)
        u = F.silu(self.conv(u.transpose(1, 2))[..., :tokens.shape[1]].transpose(1, 2))
        delta, b, c = self.select(u).split((1, self.state, self.state), -1)
        dt = F.softplus(self.dt_proj(delta))
        y = selective_scan(u, dt, -self.a_log.exp(), b, c)
        return tokens + self.out_proj((y + self.d * u) * F.silu(gate))


class HydraMixer(nn.Module):
    def __init__(self, width=16, state=4, expansion=2, kernel=3, heads=4):
        super().__init__()
        inner = width * expansion
        self.inner, self.state, self.heads = inner, state, heads
        self.in_proj = nn.Linear(width, 2 * inner + 4 * state + 2 * heads)
        channels = inner + 4 * state
        self.conv = nn.Conv1d(channels, channels, kernel, groups=channels, padding=kernel // 2)
        self.a_log = nn.Parameter(torch.zeros(heads))
        self.dt_bias = nn.Parameter(torch.full((heads,), -3.0))
        self.diagonal = nn.Linear(inner, heads)
        self.out_proj = nn.Linear(inner, width)
        nn.init.ones_(self.diagonal.bias)

    def forward(self, tokens):
        gate, xbc, dt = self.in_proj(rms(tokens)).split(
            (self.inner, self.inner + 4 * self.state, 2 * self.heads), -1)
        xbc = F.silu(self.conv(xbc.transpose(1, 2)).transpose(1, 2))
        x, bf, cf, br, cr = xbc.split((self.inner, self.state, self.state, self.state, self.state), -1)
        df, dr = dt.chunk(2, -1)
        expand = self.inner // self.heads
        dt = F.softplus(torch.cat((df, dr.flip(1))) + self.dt_bias).repeat_interleave(expand, -1)
        a = -self.a_log.exp().repeat_interleave(expand).unsqueeze(-1)
        y = selective_scan(torch.cat((x, x.flip(1))), dt, a,
                           torch.cat((bf, br.flip(1))), torch.cat((cf, cr.flip(1))))
        # Strictly off-diagonal directional outputs, as in the Hydra mixer.
        shifted = F.pad(y[:, :-1], (0, 0, 1, 0))
        forward, reverse = shifted.chunk(2, 0)
        diagonal = self.diagonal(x).repeat_interleave(expand, -1) * x
        y = forward + reverse.flip(1) + diagonal
        return tokens + self.out_proj(rms(y) * F.silu(gate))


class SSMStageHead(nn.Module):
    def __init__(self, count, outputs, has_flags, mixer):
        super().__init__()
        self.has_flags = has_flags
        self.embedding = nn.Embedding(count, 16)
        self.bos = nn.Parameter(torch.randn(16) * .02)
        self.context = nn.Linear(4, 16)
        self.mixer = mixer()
        self.readout = nn.Sequential(nn.Linear(48, 64), nn.GELU())
        self.outputs = nn.ModuleList(nn.Linear(64, n) for n in outputs)

    def selector_logits(self, ops, flags=None):
        if flags is None or not self.has_flags:
            flags = torch.zeros((len(ops), 4), device=ops.device)
        tokens = torch.stack((self.bos.expand(len(ops), -1), self.embedding(ops), self.context(flags)), 1)
        mixed = self.mixer(tokens)
        value = self.readout(mixed.flatten(1))
        return tuple(layer(value) for layer in self.outputs)

    def forward(self, ops, flags=None):
        return self.selector_logits(ops, flags)[0]


class SSMRuntimeHead(nn.Module):
    def __init__(self, numeric_features, mixer):
        super().__init__()
        self.embedding = nn.Embedding(256, 16)
        self.mixer = mixer()
        self.readout = nn.Sequential(nn.Linear(48 + numeric_features, 64), nn.GELU(), nn.Linear(64, 33))

    def forward(self, raw, numeric):
        mixed = self.mixer(self.embedding(raw))
        pooled = torch.cat((mixed[:, 0], mixed.mean(1), mixed[:, -1], numeric), -1)
        return self.readout(pooled)
