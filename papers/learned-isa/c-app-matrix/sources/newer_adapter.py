"""Raw serving adapter for frozen R3 direct-effect executors.

This module provides no ELF loader, instruction parser, ALU, memory-load path,
syscall policy or reference-state repair. The caller supplies its current
15-byte fetch window and model-predicted architectural state. The caller may
commit these predictions through its declared memory/Linux ABI.

Importing this module does not import Torch or instantiate a model.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


GPRS = ("RAX", "RCX", "RDX", "RBX", "RSP", "RBP", "RSI", "RDI")
FLAGS = ("CF", "ZF", "SF", "OF")
MASK64 = (1 << 64) - 1
SOURCE_SHA256 = {
    "direct_effect/model.py": "0cecd8699f4a603d38fc1583a0141eeddb99db3da1272fe143f38bb7159aa09c",
    "isa_lab/ssm.py": "319f942903166039e3f6d25a82b38f87412054ea18bf31e19c77554af6998573",
}
CHECKPOINT_SHA256 = {
    "nn": "30caebe4b2fb96b037829dc212a8620673b75b10ff74d3e421ec79c7d582e235",
    "mamba": "9399e921776d7a5437c5bbd51bfc1928f09d2ddea444fe2aa1c9cf282baf7f1e",
    "hydra": "0dc718f43f1336305419df39d22c62c4cba4e971b0aaf7199f2ffd95409a951c",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class FrozenDirectEffect:
    """Load one exact R3 specimen; ``step`` receives no reference after-state.

    ``artifact_dir`` contains ``model.pt`` and ``result.json`` with ``config``.
    Expected architecture: width48, layers3, state4, store=True, aligned=True.
    The frozen source modules must be imported from the supplied source root.
    This class validates their bytes but does not manipulate ``sys.path``.
    """

    def __init__(self, arch: str, artifact_dir: str | Path, *, device: str = "cpu"):
        if arch not in CHECKPOINT_SHA256:
            raise ValueError(f"unknown R3 architecture: {arch}")
        import torch
        from direct_effect import model as model_module
        from isa_lab import ssm as ssm_module

        artifact_dir = Path(artifact_dir)
        checkpoint = artifact_dir / "model.pt"
        actual_sha = sha256(checkpoint)
        if actual_sha != CHECKPOINT_SHA256[arch]:
            raise ValueError(f"checkpoint identity mismatch for {arch}: {actual_sha}")
        for module, name in ((model_module, "direct_effect/model.py"), (ssm_module, "isa_lab/ssm.py")):
            if sha256(Path(module.__file__)) != SOURCE_SHA256[name]:
                raise ValueError(f"frozen source identity mismatch: {name}")
        config = json.loads((artifact_dir / "result.json").read_text())["config"]
        options = {k: config[k] for k in ("aligned", "relptr", "regptr", "fieldptr", "maskkey", "aux_detach") if k in config}
        if options.get("aligned") is not True:
            raise ValueError("this adapter's frozen R3 cohort requires aligned=True")
        self.model = model_module.Executor(arch, width=48, layers=3, state=4, store=True, **options).to(device)
        self.model.load_state_dict(torch.load(checkpoint, map_location=device, weights_only=True), strict=True)
        self.model.eval()
        self.torch, self.device = torch, device
        self.metadata = {
            "architecture": arch,
            "track": "direct-effect-x86-de64-v2-r3",
            "checkpoint_sha256": actual_sha,
            "artifact_bytes": checkpoint.stat().st_size,
            "parameter_count": sum(p.numel() for p in self.model.parameters()),
            "tensor_state_bytes": sum(t.numel() * t.element_size() for t in self.model.state_dict().values()),
            "source_sha256": dict(SOURCE_SHA256),
            "config": config,
            "device": device,
            "register_order": list(GPRS),
            "flag_order": list(FLAGS),
        }

    def step(self, window: bytes, before: dict) -> dict:
        """Return raw predicted effects without any ABI or reference correction.

        ``before`` has ``regs`` (8 unsigned words), ``flags`` (named bits),
        and ``rip``. ``window`` is the caller's actual fetch, at most 15 bytes;
        a short final window is zero padded as in direct_effect.v2.step.
        RIP advances only by predicted length. No hidden state persists.
        """
        torch = self.torch
        if not isinstance(window, bytes) or len(window) > 15:
            raise ValueError("window must be at most 15 bytes")
        registers = before["regs"]
        if len(registers) != 8 or any(not isinstance(v, int) or not 0 <= v <= MASK64 for v in registers):
            raise ValueError("expected 8 unsigned 64-bit register values")
        flags = [before["flags"][name] for name in FLAGS]
        if any(v not in (0, 1) for v in flags):
            raise ValueError("flags must be bits")
        window = window.ljust(15, b"\0")
        win = torch.tensor([[(v >> i) & 1 for v in window for i in range(8)]], dtype=torch.float32, device=self.device)
        regs = torch.tensor([[[(v >> i) & 1 for i in range(64)] for v in registers]], dtype=torch.float32, device=self.device)
        flag_tensor = torch.tensor([flags], dtype=torch.float32, device=self.device)
        with torch.inference_mode():
            output = self.model(win, regs, flag_tensor)
        if any(not bool(torch.isfinite(value).all()) for value in output.values()):
            raise FloatingPointError("nonfinite model output")

        def word(bits) -> int:
            return sum(int(value) << i for i, value in enumerate(bits))

        predicted_regs = (output["regs"][0] > 0).long().tolist()
        predicted_flags = (output["flags"][0] > 0).long().tolist()
        length = int(output["length"][0].argmax()) + 1
        return {
            "regs": [word(bits) for bits in predicted_regs],
            "flags": dict(zip(FLAGS, predicted_flags)),
            "length": length,
            "rip": int(before["rip"]) + length,
            "store": bool(output["store"][0] > 0),
            "store_addr": word((output["store_addr"][0] > 0).long().tolist()),
            "store_value": word((output["store_value"][0] > 0).long().tolist()),
            "syscall": bool(output["syscall"][0] > 0),
        }
