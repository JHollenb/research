"""Bit-sliced direct-effect executors: the model emits the whole next architectural state.

Supplied representation (reported, not semantics): instruction-window bytes and register
values are given as bits; the register file is laid out as 64 bit-position tokens, each
holding bit i of all eight GPRs. Everything else is learned: instruction length, operand
decoding (destination/source/width/immediate, as soft reads), arithmetic and carries, flags,
width-dependent write merging (8-bit preserve / 32-bit zero-extend / 64-bit) and copying of
untouched registers. There is no supplied ALU, parser, write mux or candidate vocabulary.

Architectures differ only in the mixer along the bit axis (LSB → MSB):
  nn     MLP-Mixer (token MLP + full cross-position MLP); no recurrence
  mamba  stacked Mamba-style selective scans (causal, LSB → MSB)
  hydra  stacked Hydra-style bidirectional scans
"""
from __future__ import annotations

import torch
from torch import nn
from torch.nn import functional as F

from isa_lab.ssm import HydraMixer, MambaMixer

BITS, NREG, WINDOW_BITS, NFLAG = 64, 8, 15 * 8, 4


class TokenMix(nn.Module):
    def __init__(self, width):
        super().__init__()
        self.norm1, self.norm2 = nn.LayerNorm(width), nn.LayerNorm(width)
        self.cross = nn.Sequential(nn.Linear(BITS, 2 * BITS), nn.GELU(), nn.Linear(2 * BITS, BITS))
        self.token = nn.Sequential(nn.Linear(width, 2 * width), nn.GELU(), nn.Linear(2 * width, width))

    def forward(self, x):
        x = x + self.cross(self.norm1(x).transpose(1, 2)).transpose(1, 2)
        return x + self.token(self.norm2(x))


def field_code(window_bits, start):
    """window_bits [B,120] (LSB first per byte), start [B,K,118] weights over field start bit j -> [B,K,3]: bits j..j+2."""
    return torch.einsum("bkj,bji->bki", start, window_bits.unfold(1, 3, 1))


def start_cover(start):
    """start [B,2,118] weights over field starts -> [B,120] mass with which each window bit lies in either field."""
    s = torch.nn.functional.pad(start, (0, 2))  # [B,2,120], s[j] = weight of a field starting at bit j
    cover = (s + torch.nn.functional.pad(s, (1, 0))[..., :-1] + torch.nn.functional.pad(s, (2, 0))[..., :-2]).clamp(max=1)
    return 1 - (1 - cover[:, 0]) * (1 - cover[:, 1])


class Executor(nn.Module):
    def __init__(self, arch, width=48, layers=3, state=4, store=False, aligned=False, relptr=False, regptr=False,
                 fieldptr=False, maskkey=False, aux_detach=None):
        super().__init__()
        # Evaluation-time hard snapping of soft choices (no parameters): any of "regsel" (dest/src register reads),
        # "regptr", "imm" (immediate read heads), "aligned", "relptr", "flagq". Empty = the trained soft model.
        self.snap = set()
        self.fieldptr = fieldptr = fieldptr or maskkey
        self.maskkey = maskkey
        self.aux_detach = maskkey if aux_detach is None else aux_detach
        regptr = regptr or fieldptr  # fieldptr keeps regptr's shared code map and write mux
        self.regptr = regptr
        if fieldptr:
            # round-5 arm (supplied structure: a register code is 3 contiguous instruction bits; learned: where each
            # field starts, per form, chosen from z). One pointer per field (destination, source) over start bits.
            self.field_ptr = nn.Linear(256, 2 * (WINDOW_BITS - 2))
            if maskkey:
                # combined arm: pass 1 (unmasked z) picks the field starts, the window bits under them are masked to
                # zero, and pass 2 (z of the masked window) re-picks the starts and feeds everything downstream.
                self.decoder_m = nn.Sequential(nn.Linear(WINDOW_BITS, 256), nn.GELU(), nn.Linear(256, 256), nn.GELU())
                self.field_ptr_m = nn.Linear(256, 2 * (WINDOW_BITS - 2))
            self.reg_map = nn.Linear(3, NREG)
            self.write_en = nn.Linear(256, 1)
            self.new_val = nn.Linear(width, 1)
        elif regptr:
            # round-4 arm (supplied structure, learned decode): six pointers over the instruction bits (+0/+1 slots)
            # read a 3-bit destination code and a 3-bit source code; one shared map turns a code into a register
            # choice; a single write-enable + per-token new value is written to the chosen register (one write mux).
            self.reg_ptr = nn.Linear(256, 6 * (WINDOW_BITS + 2))
            self.reg_map = nn.Linear(3, NREG)
            self.write_en = nn.Linear(256, 1)
            self.new_val = nn.Linear(width, 1)
        self.relptr = relptr
        if relptr:  # round-3 arm: pointer read whose logits depend only on (j - i) via a z-chosen relative profile
            self.rel_head = nn.Linear(256, WINDOW_BITS + BITS - 1)
            self.register_buffer("rel_index", (torch.arange(WINDOW_BITS)[None, :] - torch.arange(BITS)[:, None]) + BITS - 1,
                                 persistent=False)
        self.arch = arch
        self.width = width
        self.store = store
        self.aligned = aligned
        if aligned:  # v3 layout: token i also sees bit i of the little-endian integer starting at each byte offset 0..7
            self.offset_head = nn.Linear(256, 8)
        if store:  # v2: memory store effects (enable, 64-bit address, 64-bit value), all model-emitted
            self.store_flag = nn.Linear(256, 1)
            self.store_out = nn.Linear(width, 2)
        self.decoder = nn.Sequential(nn.Linear(WINDOW_BITS, 256), nn.GELU(), nn.Linear(256, 256), nn.GELU())
        z = 256
        self.dest, self.src = nn.Linear(z, NREG), nn.Linear(z, NREG)
        self.width_head, self.length = nn.Linear(z, 3), nn.Linear(z, 15)
        self.syscall = nn.Linear(z, 1)
        self.pos = nn.Parameter(torch.randn(BITS, 16) * 0.1)
        self.ins_pos = nn.Parameter(torch.randn(WINDOW_BITS + 2, 16) * 0.1)  # +zero/+one constant slots
        self.query = nn.Linear(16 + z, 16 * 2)  # two immediate-read heads
        self.inp = nn.Linear(NREG + 2 + 2 + 16 + z + (9 if aligned else 0) + (1 if relptr else 0), width)
        if arch == "nn":
            self.mixers = nn.ModuleList(TokenMix(width) for _ in range(layers))
        elif arch == "mamba":
            self.mixers = nn.ModuleList(MambaMixer(width=width, state=state) for _ in range(layers))
        elif arch == "hydra":
            self.mixers = nn.ModuleList(HydraMixer(width=width, state=state, heads=4) for _ in range(layers))
        else:
            raise ValueError(arch)
        self.post = nn.ModuleList(nn.Sequential(nn.LayerNorm(width), nn.Linear(width, 2 * width), nn.GELU(),
                                                nn.Linear(2 * width, width)) for _ in range(layers))
        self.reg_out = nn.Linear(width, NREG)
        self.imm_out = nn.Linear(width, 1)
        self.flag_query = nn.Linear(z, 16 * 4)
        self.flags = nn.Sequential(nn.Linear(z + NFLAG + 4 * width + width, 128), nn.GELU(), nn.Linear(128, NFLAG))

    def _choose(self, logits, kind):
        if kind in self.snap:
            return torch.nn.functional.one_hot(logits.argmax(-1), logits.shape[-1]).to(logits.dtype)
        return logits.softmax(-1)

    def forward(self, window_bits, reg_bits, flags, capture=None):
        """window_bits [B,120], reg_bits [B,8,64] (LSB first), flags [B,4] → dict of logits."""
        b = window_bits.shape[0]
        z = self.decoder(window_bits * 2 - 1)
        z0 = z
        if self.maskkey:
            start1 = self._choose(self.field_ptr(z).view(b, 2, -1), "regptr")  # [B,2,118]
            keep = 1 - start_cover(start1)  # [B,120]: window bits not under either field
            if capture is not None:
                capture["field_start1"] = start1.argmax(-1).detach()
                capture["key_keep"] = keep.detach()
            z = self.decoder_m((window_bits * 2 - 1) * keep)
        # auxiliary destination/source heads (trained, never consumed). With the masked key they read the detached
        # unmasked z0: on masked z their loss would reward keeping the register bits visible, i.e. not masking the field.
        dest, src = (self.dest(z0.detach()), self.src(z0.detach())) if self.aux_detach else (self.dest(z), self.src(z))
        pd, ps = self._choose(dest, "regsel"), self._choose(src, "regsel")
        if self.fieldptr:
            head = self.field_ptr_m if self.maskkey else self.field_ptr
            start = self._choose(head(z).view(b, 2, -1), "regptr")  # [B,2,118]
            code = field_code(window_bits, start).flatten(1)  # [B,6] = destination bits, source bits
            pd = self._choose(self.reg_map(code[:, :3] * 2 - 1), "regptr")
            ps = self._choose(self.reg_map(code[:, 3:] * 2 - 1), "regptr")
            if capture is not None:
                capture["reg_code"] = code.detach()
                capture["field_start"] = start.argmax(-1).detach()
            starts_p = torch.stack((start1, start)) if self.maskkey else start.unsqueeze(0)  # [passes,B,2,118]
        elif self.regptr:
            slots = torch.cat((window_bits, window_bits.new_zeros(b, 1), window_bits.new_ones(b, 1)), -1)  # [B,122]
            code = torch.einsum("bkj,bj->bk", self._choose(self.reg_ptr(z).view(b, 6, -1), "regptr"), slots)  # [B,6] code bits
            pd = self._choose(self.reg_map(code[:, :3] * 2 - 1), "regptr")
            ps = self._choose(self.reg_map(code[:, 3:] * 2 - 1), "regptr")
            if capture is not None:
                capture["reg_code"] = code.detach()
        a = torch.einsum("br,bri->bi", pd, reg_bits)
        s = torch.einsum("br,bri->bi", ps, reg_bits)
        # immediate reads: each bit position attends over instruction bits + constant 0/1 slots
        q = self.query(torch.cat((self.pos.expand(b, -1, -1), z.unsqueeze(1).expand(-1, BITS, -1)), -1))
        q = q.view(b, BITS, 2, 16)
        keys = self.ins_pos  # [122,16]
        values = torch.cat((window_bits, window_bits.new_zeros(b, 1), window_bits.new_ones(b, 1)), -1)  # [B,122]
        att = torch.einsum("bihd,jd->bihj", q, keys) * 4.0
        imm = torch.einsum("bihj,bj->bih", self._choose(att, "imm"), values)  # [B,64,2]
        parts = [reg_bits.transpose(1, 2), a.unsqueeze(-1), s.unsqueeze(-1), imm,
                 self.pos.expand(b, -1, -1), z.unsqueeze(1).expand(-1, BITS, -1)]
        if self.aligned:
            # slots[b, i, o] = window bit 8*o + i (layout only; which offset holds the immediate is learned)
            slots = window_bits.unfold(1, BITS, 8)  # [B, 8, 64]
            slots = slots.transpose(1, 2)
            pick = torch.einsum("bo,bio->bi", self._choose(self.offset_head(z), "aligned"), slots)
            parts += [slots * 2 - 1, pick.unsqueeze(-1) * 2 - 1]
            if capture is not None:
                capture["aligned_pick"] = pick.detach()
        if self.relptr:
            rel = self.rel_head(z)[:, self.rel_index]  # [B, 64, 120]: logit for window bit j at output bit i = r(z)[j - i]
            read = torch.einsum("bij,bj->bi", self._choose(rel, "relptr"), window_bits)
            parts.append(read.unsqueeze(-1) * 2 - 1)
            if capture is not None:
                capture["rel_read"] = read.detach()
                capture["rel_argmax"] = rel.argmax(-1).detach()
        tokens = torch.cat(parts, -1)
        h = self.inp(tokens)
        if capture is not None:
            capture["input"] = h.detach()
        for i, (mixer, post) in enumerate(zip(self.mixers, self.post, strict=True)):
            h = mixer(h)
            h = h + post(h)
            if capture is not None:
                capture[f"layer{i}"] = h.detach()
        if self.regptr:
            w = (torch.sigmoid(self.write_en(z)) * pd).unsqueeze(1)  # [B,1,8]: how much each register is overwritten
            reg_logits = (1 - w) * (reg_bits.transpose(1, 2) * 8 - 4) + w * self.new_val(h)
        else:
            reg_logits = reg_bits.transpose(1, 2) * 8 - 4 + self.reg_out(h)  # residual copy prior
        fq = self.flag_query(z).view(b, 4, 16)
        point = self._choose(torch.einsum("bkd,id->bki", fq, self.pos), "flagq")
        read = torch.einsum("bki,biw->bkw", point, h).flatten(1)
        flag_logits = self.flags(torch.cat((z, flags, read, h.mean(1)), -1)) + (flags * 8 - 4)
        if capture is not None:
            capture["z"] = z.detach()
            capture["imm_read"] = imm.detach()
        out = {"regs": reg_logits.transpose(1, 2), "flags": flag_logits, "dest": dest, "src": src,
               "width": self.width_head(z), "length": self.length(z), "syscall": self.syscall(z).squeeze(-1),
               "imm": self.imm_out(h).squeeze(-1)}
        if self.regptr:
            out["reg_pick"] = pd
        if self.fieldptr:
            out["field_start_p"] = starts_p
        if self.store:
            so = self.store_out(h)
            out.update({"store": self.store_flag(z).squeeze(-1), "store_addr": so[..., 0], "store_value": so[..., 1]})
        return out


def to_bits(value, n=BITS):
    return [(value >> i) & 1 for i in range(n)]


def from_bits(bits):
    return sum(int(b) << i for i, b in enumerate(bits))


FLAG_ORDER = ("CF", "ZF", "SF", "OF")


def batch_tensors(examples, device="cpu"):
    win = torch.tensor([[(byte >> j) & 1 for byte in bytes.fromhex(e["window"]) for j in range(8)] for e in examples],
                       dtype=torch.float32, device=device)
    regs = torch.tensor([[to_bits(v) for v in e["before"]["regs"]] for e in examples], dtype=torch.float32, device=device)
    flags = torch.tensor([[e["before"]["flags"][f] for f in FLAG_ORDER] for e in examples], dtype=torch.float32, device=device)
    return win, regs, flags


def targets(examples, device="cpu"):
    from .profile import WIDTH_CLASS
    t = lambda x, **k: torch.tensor(x, device=device, **k)
    return {"regs": t([[to_bits(v) for v in e["after"]["regs"]] for e in examples], dtype=torch.float32),
            "flags": t([[e["after"]["flags"][f] for f in FLAG_ORDER] for e in examples], dtype=torch.float32),
            "dest": t([e["dest"] for e in examples]), "src": t([e["src"] for e in examples]),
            "width": t([WIDTH_CLASS[e["width"]] for e in examples]), "length": t([e["length"] - 1 for e in examples]),
            "syscall": t([e["syscall"] for e in examples], dtype=torch.float32),
            "imm": t([to_bits(e["imm"]) for e in examples], dtype=torch.float32)}


def loss(out, tgt, before_regs):
    changed = (tgt["regs"] != before_regs).float()
    reg_w = 1 + 20 * changed
    terms = {
        "regs": F.binary_cross_entropy_with_logits(out["regs"], tgt["regs"], weight=reg_w),
        "flags": F.binary_cross_entropy_with_logits(out["flags"], tgt["flags"]),
        "dest": F.cross_entropy(out["dest"], tgt["dest"]), "src": F.cross_entropy(out["src"], tgt["src"]),
        "width": F.cross_entropy(out["width"], tgt["width"]), "length": F.cross_entropy(out["length"], tgt["length"]),
        "syscall": F.binary_cross_entropy_with_logits(out["syscall"], tgt["syscall"]),
        "imm": F.binary_cross_entropy_with_logits(out["imm"], tgt["imm"]),
    }
    return sum(terms.values()), terms


def decode_outputs(out):
    """Hard (thresholded/argmax) emitted effects; this is exactly what is fed to the next step."""
    return {"regs": (out["regs"] > 0).long(), "flags": (out["flags"] > 0).long(), "dest": out["dest"].argmax(-1),
            "src": out["src"].argmax(-1), "width": out["width"].argmax(-1), "length": out["length"].argmax(-1) + 1,
            "syscall": (out["syscall"] > 0).long(), "imm": (out["imm"] > 0).long()}


class SignSTE(torch.autograd.Function):
    @staticmethod
    def forward(ctx, x):
        ctx.save_for_backward(x)
        return torch.where(x >= 0, torch.ones_like(x), -torch.ones_like(x))

    @staticmethod
    def backward(ctx, g):
        # tanh-shaped straight-through gradient: bounded, so kept codes (|x| >= 2) do not
        # multiply gradients across instructions.
        (x,) = ctx.saved_tensors
        return g * (1 - torch.tanh(x).square())


class LatentExecutor(nn.Module):
    """C3b: no external register file. The model carries a learned discrete latent state.

    H has one 16-channel binary (±1, straight-through) code per bit position. Registers are
    read into H once, at program start, by a learned encoder. After that every instruction
    maps (H_t, instruction window) → H_{t+1}; architectural registers and flags are only
    decoded from H by readout heads for shadow checking. Nothing outside the model stores
    register values between instructions.
    """

    def __init__(self, arch, width=48, layers=3, state=4, code=16):
        super().__init__()
        self.code = code
        self.core = Executor(arch, width=width, layers=layers, state=state)
        self.encode_regs = nn.Linear(NREG + NFLAG, code)
        self.to_code = nn.Linear(width, code)
        self.code_in = nn.Linear(code, NREG + 2)  # replaces register-bit inputs of the core
        self.reg_head = nn.Linear(code, NREG)
        self.flag_head = nn.Sequential(nn.Linear(code * 2, 64), nn.GELU(), nn.Linear(64, NFLAG))

    def encode(self, reg_bits, flags):
        x = torch.cat((reg_bits.transpose(1, 2), flags.unsqueeze(1).expand(-1, BITS, -1)), -1) * 2 - 1
        return SignSTE.apply(self.encode_regs(x))

    def readout(self, h):
        return {"regs": self.reg_head(h).transpose(1, 2), "flags": self.flag_head(torch.cat((h.mean(1), h[:, 0]), -1))}

    def forward(self, window_bits, h, capture=None):
        c = self.core
        b = window_bits.shape[0]
        z = c.decoder(window_bits * 2 - 1)
        q = c.query(torch.cat((c.pos.expand(b, -1, -1), z.unsqueeze(1).expand(-1, BITS, -1)), -1)).view(b, BITS, 2, 16)
        values = torch.cat((window_bits, torch.zeros(b, 1, device=h.device), torch.ones(b, 1, device=h.device)), -1)
        imm = torch.einsum("bihj,bj->bih", torch.einsum("bihd,jd->bihj", q, c.ins_pos * 1.0).mul(4.0).softmax(-1), values)
        tokens = torch.cat((self.code_in(h), imm, c.pos.expand(b, -1, -1), z.unsqueeze(1).expand(-1, BITS, -1)), -1)
        x = c.inp(tokens)
        for i, (mixer, post) in enumerate(zip(c.mixers, c.post, strict=True)):
            x = mixer(x)
            x = x + post(x)
            if capture is not None:
                capture[f"layer{i}"] = x.detach()
        h_next = SignSTE.apply(self.to_code(x) + h * 2.0)  # residual keeps untouched codes stable
        if capture is not None:
            capture["code"] = h_next.detach()
        out = self.readout(h_next)
        out.update({"length": c.length(z), "syscall": c.syscall(z).squeeze(-1), "dest": c.dest(z),
                    "width": c.width_head(z), "imm": c.imm_out(x).squeeze(-1)})
        return out, h_next
