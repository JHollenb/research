"""x86-de64-v1: direct-effect profile. Real x86-64 bytes, 8 GPRs, CF/ZF/SF/OF, RIP.

Nothing here is used by a model at serving time. This module generates instructions,
labels them with an independent emulator (Unicorn) and holds the encoding-side ground
truth (destination, source, width, immediate) used as decode supervision and for probes.
The PAN typed adapter is used only as a shadow checker (`pan_shadow`).
"""
from __future__ import annotations

import random
from dataclasses import dataclass

MASK64 = (1 << 64) - 1
GPRS = ("RAX", "RCX", "RDX", "RBX", "RSP", "RBP", "RSI", "RDI")
FLAG_BITS = {"CF": 0, "ZF": 6, "SF": 7, "OF": 11}
WINDOW = 15
CODE_BASE = 0x400000

# name: (width, kind, immediate bytes)
FORMS = {
    # x86-al8-v1 forms, operating on AL (low byte of RAX); upper 56 bits preserved
    "mov_al8": (8, "mov", 1), "add_al8": (8, "add", 1), "sub_al8": (8, "sub", 1), "xor_al8": (8, "xor", 1),
    "and_al8": (8, "and", 1), "or_al8": (8, "or", 1), "cmp_al8": (8, "cmp", 1), "test_al8": (8, "test", 1),
    "inc_al8": (8, "inc", 0), "dec_al8": (8, "dec", 0),
    # 32/64-bit register forms used by the rosetta panel and counter programs
    "mov_r32": (32, "mov", 4), "mov_r64": (64, "mov", 8), "mov_r64_c7": (64, "mov", 4),
    "add_r64_8": (64, "add", 1), "sub_r64_8": (64, "sub", 1), "add_r32_8": (32, "add", 1), "sub_r32_8": (32, "sub", 1),
    "add_r64_32": (64, "add", 4), "sub_r64_32": (64, "sub", 4), "xor_r32_r32": (32, "xor", 0),
    "nop": (64, "nop", 0), "syscall": (64, "syscall", 0),
}
AL8 = tuple(n for n in FORMS if n.endswith("al8"))
# Register/form pairs never generated for discovery or feedback (heldout-register panel).
HELDOUT_PAIRS = {("mov_r64", 5), ("add_r64_8", 3), ("sub_r64_8", 6), ("xor_r32_r32", 1), ("add_r32_8", 2)}
WIDTH_CLASS = {8: 0, 32: 1, 64: 2}


@dataclass
class Instruction:
    form: str
    code: bytes
    dest: int
    src: int
    width: int
    imm: int  # operand value at 64 bits after the form's sign/zero extension (0 when no immediate)


def encode(form, reg=0, imm=0, src=0):
    width, kind, nimm = FORMS[form]
    if form in AL8:
        reg = 0
        op = {"mov": 0xB0, "add": 0x04, "sub": 0x2C, "xor": 0x34, "and": 0x24, "or": 0x0C, "cmp": 0x3C, "test": 0xA8}
        if kind in op:
            code = bytes([op[kind], imm & 0xFF])
        else:
            code = bytes([0xFE, 0xC0 if kind == "inc" else 0xC8])
        value = imm & 0xFF
        operand = value
    elif form == "mov_r32":
        code = bytes([0xB8 + reg]) + (imm & 0xFFFFFFFF).to_bytes(4, "little")
        operand = imm & 0xFFFFFFFF
    elif form == "mov_r64":
        code = bytes([0x48, 0xB8 + reg]) + (imm & MASK64).to_bytes(8, "little")
        operand = imm & MASK64
    elif form == "mov_r64_c7":
        code = bytes([0x48, 0xC7, 0xC0 + reg]) + (imm & 0xFFFFFFFF).to_bytes(4, "little")
        operand = sext(imm & 0xFFFFFFFF, 32) & MASK64
    elif form in ("add_r64_8", "sub_r64_8", "add_r32_8", "sub_r32_8"):
        rex = b"\x48" if "r64" in form else b""
        code = rex + bytes([0x83, (0xC0 if form.startswith("add") else 0xE8) + reg, imm & 0xFF])
        operand = sext(imm & 0xFF, 8) & (MASK64 if "r64" in form else 0xFFFFFFFF)
    elif form in ("add_r64_32", "sub_r64_32"):
        code = bytes([0x48, 0x81, (0xC0 if form.startswith("add") else 0xE8) + reg]) + (imm & 0xFFFFFFFF).to_bytes(4, "little")
        operand = sext(imm & 0xFFFFFFFF, 32) & MASK64
    elif form == "xor_r32_r32":
        code = bytes([0x31, 0xC0 | (src << 3) | reg])
        operand = 0
    elif form == "nop":
        code, operand = b"\x90", 0
    elif form == "syscall":
        code, operand = b"\x0f\x05", 0
    else:
        raise ValueError(form)
    return Instruction(form, code, reg, src if form == "xor_r32_r32" else reg, width, operand)


def sext(value, bits):
    return value - (1 << bits) if value >> (bits - 1) & 1 else value


def special_value(rng):
    return rng.choice((0, 1, 2, 0x7F, 0x80, 0xFF, 0x100, 0x7FFFFFFF, 0x80000000, 0xFFFFFFFF, 0x100000000,
                       0x7FFFFFFFFFFFFFFF, 0x8000000000000000, MASK64, MASK64 - 1))


def random_state(rng):
    regs = [special_value(rng) if rng.random() < 0.25 else
            (rng.randrange(256) if rng.random() < 0.15 else rng.getrandbits(64)) for _ in GPRS]
    flags = {f: rng.randrange(2) for f in FLAG_BITS}
    return {"regs": regs, "flags": flags, "rip": CODE_BASE}


def random_imm(rng, nbytes, residue):
    """Immediate whose low byte satisfies the split residue rule ('train' → %4!=0, 'held' → %4==0)."""
    if nbytes == 0:
        return 0
    r = rng.random()
    if r < 0.3:
        value = rng.randrange(256)
    elif r < 0.45:
        value = special_value(rng) & ((1 << (8 * nbytes)) - 1)
    else:
        value = rng.getrandbits(8 * nbytes)
    low = value & 0xFF
    if residue == "train" and low % 4 == 0:
        value ^= rng.choice((1, 2, 3))
    if residue == "held":
        value &= ~3
    return value


def random_instruction(rng, *, residue="train", allow_heldout_pairs=False, forms=None):
    forms = forms or tuple(FORMS)
    while True:
        form = rng.choice(forms)
        reg = 0 if form in AL8 else rng.randrange(8)
        src = rng.randrange(8)
        if (form, reg) in HELDOUT_PAIRS and not allow_heldout_pairs:
            continue
        ins = encode(form, reg, random_imm(rng, FORMS[form][2], residue), src)
        return ins


def window(code, rng):
    tail = bytes(rng.randrange(256) for _ in range(WINDOW - len(code)))
    return code + tail


class Unicorn:
    """Independent emulator authority for one instruction on the 8-GPR + 4-flag state."""

    def __init__(self):
        import unicorn
        from unicorn import x86_const as x
        self.u, self.x = unicorn, x
        self.regs = [getattr(x, f"UC_X86_REG_{n}") for n in GPRS]

    def step(self, state, code):
        u, x = self.u, self.x
        uc = u.Uc(u.UC_ARCH_X86, u.UC_MODE_64)
        uc.mem_map(CODE_BASE, 0x2000)
        uc.mem_write(CODE_BASE, code + b"\x90" * 16)
        for reg, value in zip(self.regs, state["regs"], strict=True):
            uc.reg_write(reg, value)
        eflags = 2 | sum(v << FLAG_BITS[f] for f, v in state["flags"].items())
        uc.reg_write(x.UC_X86_REG_EFLAGS, eflags)
        uc.emu_start(CODE_BASE, CODE_BASE + 0x1000, count=1)
        eflags = uc.reg_read(x.UC_X86_REG_EFLAGS)
        return {"regs": [uc.reg_read(r) & MASK64 for r in self.regs],
                "flags": {f: (eflags >> b) & 1 for f, b in FLAG_BITS.items()},
                "rip": uc.reg_read(x.UC_X86_REG_RIP)}


def label(oracle, state, ins):
    """After-state from the emulator; SYSCALL is a terminal decode with unchanged state."""
    if ins.form == "syscall":
        return {"regs": list(state["regs"]), "flags": dict(state["flags"]), "rip": state["rip"] + 2}
    before = dict(state, rip=CODE_BASE)
    after = oracle.step(before, ins.code)
    after["rip"] = state["rip"] + (after["rip"] - CODE_BASE)
    return after


def example(rng, oracle, *, residue="train", allow_heldout_pairs=False, forms=None, state=None, ins=None):
    state = state or random_state(rng)
    ins = ins or random_instruction(rng, residue=residue, allow_heldout_pairs=allow_heldout_pairs, forms=forms)
    after = label(oracle, state, ins)
    return {"form": ins.form, "window": window(ins.code, rng).hex(), "length": len(ins.code), "dest": ins.dest,
            "src": ins.src, "width": ins.width, "imm": ins.imm, "syscall": int(ins.form == "syscall"),
            "before": state, "after": after}


def pan_shadow(state, code):
    """PAN typed adapter's proposal for the same instruction (shadow checker only)."""
    from pan_isa.runtime_adapter import runtime_fixture
    from pan_isa_x86_runtime_spf.decode import decode_current
    from pan_isa_x86_runtime_spf.model import BootstrapSPFTransitionModel
    runtime = runtime_fixture({"code": code.hex(), "seed": 0, "options": {}})
    runtime.state.gpr.update({n: v for n, v in zip(GPRS, state["regs"], strict=True)})
    runtime.state.gpr["RIP"] = CODE_BASE
    runtime.state.rflags = 2 | sum(v << FLAG_BITS[f] for f, v in state["flags"].items())
    ins = decode_current(runtime)
    proposal = BootstrapSPFTransitionModel().propose(runtime, ins)
    regs = list(state["regs"])
    for name, value in dict(proposal.register_writes).items():
        if name in GPRS:
            regs[GPRS.index(name)] = int(value) & MASK64
    rflags = int(proposal.rflags) if proposal.rflags is not None else runtime.state.rflags
    return {"regs": regs, "flags": {f: (rflags >> b) & 1 for f, b in FLAG_BITS.items()}, "name": proposal.instruction_name}


def counter_code(steps):
    """Same bytes as the shared counter ELF: XOR EDI,EDI; ADD RDI,1 × (steps−3); MOV EAX,60; SYSCALL."""
    return bytes.fromhex("31ff") + bytes.fromhex("4883c701") * (steps - 3) + bytes.fromhex("b83c0000000f05")


def make_rng(seed):
    return random.Random(seed)
