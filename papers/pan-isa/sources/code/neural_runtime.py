"""Trainable neural transition head for the SPF x86 runtime.

The neural model is deliberately narrow: it learns the runtime transition
family from instruction bytes plus small architectural context features. The
typed transition adapter still emits exact proposals through the existing
SPF-validated commit contract, and the runtime fails closed if the neural head
does not select the proposal family that the adapter can prove.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
import hashlib
import json
import math
import random
from pathlib import Path
from typing import Any, Iterable, Optional, Sequence

from .compat import ensure_scripts_importable
from .decode import DecodedInstruction, decode_current
from .transitions import TransitionProposal

ensure_scripts_importable()

from pan_x86_isa.memory import SparseMemory  # noqa: E402
from pan_x86_isa.process import ProcessImage  # noqa: E402
from pan_x86_isa.runtime import (  # noqa: E402
    GPR64_BY_CODE,
    MASK64,
    StopReason,
    UnsupportedInstruction,
    _decode_modrm_address,
)


RAW_BYTE_COUNT = 15
MASK128 = (1 << 128) - 1
DEFAULT_EMBEDDING_DIM = 8
DEFAULT_HIDDEN_DIM = 96
RUNTIME_NEURAL_SCHEMA = "pan-isa-x86-runtime-neural-transition-v1"

RUNTIME_NEURAL_LABELS = (
    "NOP",
    "INT3",
    "SYSCALL",
    "PUSH_RBP",
    "POP_RBP",
    "LEAVE",
    "RET",
    "CALL_REL32",
    "JMP_REL32",
    "JMP_REL8",
    "MOV_IMM_REG",
    "MOV_RM_REG",
    "MOV_REG_RM",
    "LEA",
    "XOR_RM_REG",
    "ADD_IMM_RM",
    "SUB_IMM_RM",
    "MOV_IMM_RM",
    "MOVDQA_XMM_XMM",
    "MOVDQA_XMM_M128",
    "MOVDQA_M128_XMM",
    "MOVDQA_ALIGNMENT_FAULT",
    "MOVDQU_XMM_XMM",
    "MOVDQU_XMM_M128",
    "MOVDQU_M128_XMM",
    "PXOR_XMM_XMM",
    "PXOR_XMM_M128",
    "PADDQ_XMM_XMM",
    "PADDQ_XMM_M128",
    "FNOP",
    "FLD1",
    "FLDZ",
    "FSTP_ST",
)

NUMERIC_FEATURE_NAMES = (
    "prefix_66",
    "prefix_f2",
    "prefix_f3",
    "prefix_count",
    "rex_w",
    "rex_r",
    "rex_x",
    "rex_b",
    "width64",
    "cursor_after_opcode",
    "masked_instruction_len",
    "opcode_norm",
    "second_norm",
    "modrm_norm",
    "modrm_mod",
    "modrm_reg",
    "modrm_rm",
    *tuple(f"modrm_mod_is_{index}" for index in range(4)),
    *tuple(f"modrm_reg_is_{index}" for index in range(8)),
    *tuple(f"modrm_rm_is_{index}" for index in range(8)),
    "has_memory_operand",
    "memory_address_low4",
    "memory_address_aligned16",
    "x87_top",
    "x87_depth",
)


def _file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _state_low(value: int, mask: int) -> float:
    return float(int(value) & mask) / float(mask)


def _supported_instruction_length(runtime: object, instruction: DecodedInstruction) -> int:
    """Best-effort length for the runtime-supported instruction subset."""
    raw = instruction.raw
    cursor = int(instruction.cursor_after_opcode)
    opcode = int(instruction.opcode)
    rip = int(instruction.rip)
    memory = getattr(runtime, "memory")
    state = getattr(runtime, "state")
    try:
        if opcode in (0x90, 0xCC, 0x55, 0x5D, 0xC9, 0xC3):
            return cursor
        if opcode == 0x0F:
            second = raw[cursor]
            if second == 0x05:
                return cursor + 1
            if second in (0x6F, 0x7F, 0xEF, 0xD4):
                modrm = raw[cursor + 1]
                _mod, _reg, _rm_or_address, end = _decode_modrm_address(state, memory, rip + cursor + 2, modrm, instruction.rex)
                return max(cursor + 2, end - rip)
        if opcode in (0xD9, 0xDD):
            return cursor + 1
        if opcode in (0xE8, 0xE9):
            return cursor + 4
        if opcode == 0xEB:
            return cursor + 1
        if 0xB8 <= opcode <= 0xBF:
            return cursor + (8 if instruction.width == 64 and instruction.rex & 0x08 else 4)
        if opcode in (0x89, 0x8B, 0x8D, 0x31):
            modrm = raw[cursor]
            _mod, _reg, _rm_or_address, end = _decode_modrm_address(state, memory, rip + cursor + 1, modrm, instruction.rex)
            return max(cursor + 1, end - rip)
        if opcode == 0x83:
            modrm = raw[cursor]
            _mod, _reg, _rm_or_address, end = _decode_modrm_address(state, memory, rip + cursor + 1, modrm, instruction.rex)
            return max(cursor + 2, end - rip + 1)
        if opcode == 0xC7:
            modrm = raw[cursor]
            _mod, _reg, _rm_or_address, end = _decode_modrm_address(state, memory, rip + cursor + 1, modrm, instruction.rex)
            return max(cursor + 5, end - rip + 4)
    except Exception:
        return RAW_BYTE_COUNT
    return RAW_BYTE_COUNT


def _memory_operand_alignment(runtime: object, instruction: DecodedInstruction) -> tuple[float, float, float]:
    raw = instruction.raw
    cursor = int(instruction.cursor_after_opcode)
    opcode = int(instruction.opcode)
    rip = int(instruction.rip)
    memory = getattr(runtime, "memory")
    state = getattr(runtime, "state")
    try:
        if opcode == 0x0F and raw[cursor] in (0x6F, 0x7F, 0xEF, 0xD4):
            modrm = raw[cursor + 1]
            mod, _reg, rm_or_address, _end = _decode_modrm_address(state, memory, rip + cursor + 2, modrm, instruction.rex)
        elif opcode in (0x89, 0x8B, 0x8D, 0x31, 0x83, 0xC7):
            modrm = raw[cursor]
            mod, _reg, rm_or_address, _end = _decode_modrm_address(state, memory, rip + cursor + 1, modrm, instruction.rex)
        else:
            return 0.0, 0.0, 1.0
    except Exception:
        return 0.0, 0.0, 1.0
    if mod == 3:
        return 0.0, 0.0, 1.0
    low4 = int(rm_or_address) & 0xF
    return 1.0, float(low4) / 15.0, float(low4 == 0)


def encode_runtime_features(runtime: object, instruction: DecodedInstruction) -> tuple[list[int], list[float]]:
    """Return byte tokens and numeric context features for neural inference."""
    instruction_len = max(1, min(RAW_BYTE_COUNT, _supported_instruction_length(runtime, instruction)))
    masked_raw = instruction.raw[:instruction_len] + b"\x00" * max(0, RAW_BYTE_COUNT - instruction_len)
    raw = list(masked_raw[:RAW_BYTE_COUNT])
    raw.extend([0] * (RAW_BYTE_COUNT - len(raw)))
    cursor = int(instruction.cursor_after_opcode)
    second = raw[cursor] if cursor < len(raw) else 0
    modrm_index = cursor + 1 if instruction.opcode == 0x0F else cursor
    modrm = raw[modrm_index] if modrm_index < len(raw) else 0
    modrm_mod = (modrm >> 6) & 0x3
    modrm_reg = (modrm >> 3) & 0x7
    modrm_rm = modrm & 0x7
    state = getattr(runtime, "state")
    prefixes = set(int(item) for item in instruction.prefixes)
    has_memory_operand, memory_address_low4, memory_address_aligned16 = _memory_operand_alignment(runtime, instruction)
    numeric = [
        float(0x66 in prefixes),
        float(0xF2 in prefixes),
        float(0xF3 in prefixes),
        min(float(len(instruction.prefixes)) / 4.0, 1.0),
        float(bool(instruction.rex & 0x08)),
        float(bool(instruction.rex & 0x04)),
        float(bool(instruction.rex & 0x02)),
        float(bool(instruction.rex & 0x01)),
        float(instruction.width == 64),
        min(float(cursor) / RAW_BYTE_COUNT, 1.0),
        min(float(instruction_len) / RAW_BYTE_COUNT, 1.0),
        float(instruction.opcode) / 255.0,
        float(second) / 255.0,
        float(modrm) / 255.0,
        float(modrm_mod) / 3.0,
        float(modrm_reg) / 7.0,
        float(modrm_rm) / 7.0,
        *(float(modrm_mod == index) for index in range(4)),
        *(float(modrm_reg == index) for index in range(8)),
        *(float(modrm_rm == index) for index in range(8)),
        has_memory_operand,
        memory_address_low4,
        memory_address_aligned16,
        float(int(getattr(state, "x87_top", 0)) & 0x7) / 7.0,
        float(sum(1 for value in getattr(state, "x87", []) if value is not None)) / 8.0,
    ]
    return raw, numeric


def _matvec(weight: Sequence[Sequence[float]], bias: Sequence[float], vector: Sequence[float]) -> list[float]:
    out: list[float] = []
    for row, b in zip(weight, bias):
        total = float(b)
        for a, x in zip(row, vector):
            total += float(a) * float(x)
        out.append(total)
    return out


def _relu(values: Sequence[float]) -> list[float]:
    return [value if value > 0.0 else 0.0 for value in values]


def _softmax_confidence(logits: Sequence[float], index: int) -> float:
    top = max(float(x) for x in logits)
    exps = [math.exp(float(x) - top) for x in logits]
    total = sum(exps)
    return float(exps[index] / total) if total else 0.0


@dataclass
class RuntimeNeuralExport:
    labels: tuple[str, ...]
    byte_embedding: list[list[float]]
    layers: list[dict[str, Any]]
    numeric_feature_names: tuple[str, ...]
    raw_byte_count: int = RAW_BYTE_COUNT
    min_confidence: float = 0.50

    @classmethod
    def from_manifest(cls, manifest: dict[str, Any]) -> "RuntimeNeuralExport":
        weights = manifest.get("weights") or manifest.get("runtime_neural_export")
        if not isinstance(weights, dict):
            raise ValueError("learned neural runtime manifest does not contain exported weights")
        labels = tuple(str(item) for item in weights.get("labels") or manifest.get("labels") or ())
        if not labels:
            raise ValueError("learned neural runtime manifest has no labels")
        numeric_names = tuple(
            str(item)
            for item in weights.get("numeric_feature_names")
            or manifest.get("numeric_feature_names")
            or NUMERIC_FEATURE_NAMES
        )
        return cls(
            labels=labels,
            byte_embedding=[[float(x) for x in row] for row in weights["byte_embedding"]],
            layers=list(weights["layers"]),
            numeric_feature_names=numeric_names,
            raw_byte_count=int(weights.get("raw_byte_count", manifest.get("raw_byte_count", RAW_BYTE_COUNT))),
            min_confidence=float(manifest.get("min_confidence", weights.get("min_confidence", 0.50))),
        )

    def parameter_count(self) -> int:
        total = sum(len(row) for row in self.byte_embedding)
        for layer in self.layers:
            total += sum(len(row) for row in layer["weight"])
            total += len(layer["bias"])
        return int(total)

    def predict(self, raw_bytes: Sequence[int], numeric: Sequence[float]) -> tuple[str, float, list[float]]:
        if len(numeric) != len(self.numeric_feature_names):
            raise ValueError(
                f"numeric feature length {len(numeric)} does not match schema {len(self.numeric_feature_names)}"
            )
        vector: list[float] = []
        for item in list(raw_bytes[: self.raw_byte_count]) + [0] * max(0, self.raw_byte_count - len(raw_bytes)):
            vector.extend(self.byte_embedding[int(item) & 0xFF])
        vector.extend(float(x) for x in numeric)
        for index, layer in enumerate(self.layers):
            vector = _matvec(layer["weight"], layer["bias"], vector)
            if index != len(self.layers) - 1:
                vector = _relu(vector)
        winner = max(range(len(vector)), key=lambda i: vector[i])
        return self.labels[winner], _softmax_confidence(vector, winner), vector


@dataclass
class NeuralRuntimeTransitionModel:
    """Learned runtime adapter backed by exported neural weights."""

    manifest_data: dict[str, Any]
    export: RuntimeNeuralExport
    profile: str = "long64-ring3"
    promotion_ledger: Optional[dict[str, Any]] = None

    @classmethod
    def from_path(
        cls,
        path: Path,
        *,
        profile: str = "long64-ring3",
        promotion_ledger: Optional[dict[str, Any]] = None,
    ) -> "NeuralRuntimeTransitionModel":
        path = Path(path)
        if path.suffix == ".json":
            payload = json.loads(path.read_text(encoding="utf-8"))
        elif path.suffix == ".pt":
            try:
                import torch

                payload = torch.load(path, map_location="cpu")
            except Exception as exc:  # pragma: no cover - depends on local torch build
                raise ValueError(f"could not load neural runtime checkpoint {path}: {exc}") from exc
            if isinstance(payload, dict) and "manifest" in payload:
                manifest = dict(payload["manifest"])
                manifest["weights"] = payload.get("runtime_neural_export")
                payload = manifest
        else:
            raise ValueError(f"unsupported neural runtime artifact type: {path.suffix or '<none>'}")
        if not is_neural_runtime_manifest(payload):
            raise ValueError(f"{path} is not a runtime neural transition model")
        manifest = dict(payload)
        artifact_hash = _file_sha256(path)
        manifest.update(
            {
                "runtime_mode": "learned",
                "target_profile": manifest.get("target_profile") or profile,
                "trainable_weights_loaded": True,
                "runtime_execution_head_loaded": True,
                "artifact_path": str(path),
                "model_artifact_hash": artifact_hash,
                "commit_contract": "typed exact architectural state transition",
                "primary_semantics_path": "learned neural transition-family head plus SPF typed proposal adapter",
            }
        )
        promoted = manifest.get("promoted_forms")
        if promotion_ledger:
            from .model import _promoted_forms_from_ledger

            promoted = sorted(_promoted_forms_from_ledger(promotion_ledger, profile))
            manifest["promotion_ledger_loaded"] = True
            manifest["promotion_profile"] = profile
        manifest["promoted_forms"] = list(promoted or manifest.get("labels") or RUNTIME_NEURAL_LABELS)
        export = RuntimeNeuralExport.from_manifest(manifest)
        manifest["parameter_count"] = export.parameter_count()
        return cls(manifest_data=manifest, export=export, profile=profile, promotion_ledger=promotion_ledger)

    @property
    def manifest(self) -> dict[str, Any]:
        manifest = dict(self.manifest_data)
        manifest.pop("weights", None)
        return manifest

    def _unsupported(self, instruction: DecodedInstruction, name: str, detail: str, confidence: float) -> TransitionProposal:
        from .model import _runtime_effect_axes, _runtime_stage_for_name

        return TransitionProposal(
            kind="unsupported",
            rip=instruction.rip,
            instruction_hex=instruction.opcode_hex,
            instruction_name=name,
            stage=_runtime_stage_for_name(name),
            effect_axes=_runtime_effect_axes(name),
            profile=self.profile,
            iclass=name,
            iform=name,
            stop_reason=StopReason("unsupported_runtime_feature", detail=detail, address=instruction.rip),
            spf_manifest=self.manifest,
            model_artifact_hash=self.manifest_data.get("model_artifact_hash"),
            family_provenance="learned_neural_runtime_head",
            confidence=confidence,
        )

    def propose(self, runtime: object, instruction: DecodedInstruction) -> TransitionProposal:
        from .model import BootstrapSPFTransitionModel

        raw, numeric = encode_runtime_features(runtime, instruction)
        predicted, confidence, _logits = self.export.predict(raw, numeric)
        promoted = set(str(item) for item in self.manifest_data.get("promoted_forms") or [])
        if confidence < self.export.min_confidence:
            return self._unsupported(
                instruction,
                predicted,
                f"learned neural transition confidence below threshold: {confidence:.6f}",
                confidence,
            )
        if promoted and predicted not in promoted:
            return self._unsupported(
                instruction,
                predicted,
                f"learned neural runtime model has no promotion for predicted form {predicted}",
                confidence,
            )
        try:
            proposal = BootstrapSPFTransitionModel(profile=self.profile).propose(runtime, instruction)
        except UnsupportedInstruction:
            return self._unsupported(
                instruction,
                predicted,
                f"learned neural head selected {predicted}, but no typed adapter supports these bytes",
                confidence,
            )
        if proposal.instruction_name != predicted:
            return self._unsupported(
                instruction,
                predicted,
                f"learned neural head selected {predicted}, adapter proved {proposal.instruction_name}",
                confidence,
            )
        manifest = self.manifest
        manifest["learned_predicted_instruction"] = predicted
        return replace(
            proposal,
            spf_manifest=manifest,
            model_artifact_hash=self.manifest_data.get("model_artifact_hash"),
            family_provenance="learned_neural_runtime_head",
            confidence=confidence,
        )


def is_neural_runtime_manifest(payload: Any) -> bool:
    if not isinstance(payload, dict):
        return False
    schema = payload.get("schema_version")
    kind = payload.get("model_kind")
    return schema == RUNTIME_NEURAL_SCHEMA or kind == "learned_neural_transition_model" or "runtime_neural_export" in payload


def maybe_load_neural_transition_model(
    path: Path,
    *,
    profile: str = "long64-ring3",
    promotion_ledger: Optional[dict[str, Any]] = None,
) -> Optional[NeuralRuntimeTransitionModel]:
    path = Path(path)
    if path.suffix == ".json":
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return None
        if not is_neural_runtime_manifest(payload):
            return None
    elif path.suffix == ".pt":
        try:
            import torch

            payload = torch.load(path, map_location="cpu")
        except Exception:
            return None
        if isinstance(payload, dict) and "manifest" in payload:
            payload = payload["manifest"]
        if not is_neural_runtime_manifest(payload):
            return None
    else:
        return None
    return NeuralRuntimeTransitionModel.from_path(path, profile=profile, promotion_ledger=promotion_ledger)


def _fake_runtime(code: bytes, *, seed: int, unaligned: bool = False, x87_ready: bool = False) -> object:
    from .runtime import SPFPrimaryPanRuntime

    memory = SparseMemory()
    memory.map_region(0x400000, 0x1000, "rwx", "code")
    memory.load_bytes(0x400000, code + b"\xcc" + b"\x00" * 32)
    memory.protect_region(0x400000, 0x1000, "rx")
    memory.map_region(0x500000, 0x2000, "rw", "data")
    memory.map_region(0x700000, 0x2000, "rw", "stack")
    image = ProcessImage(
        memory=memory,
        entry=0x400000,
        initial_rsp=0x701000,
        brk=0x800000,
        program="runtime-neural-train",
        argv=["runtime-neural-train"],
        env={},
    )
    runtime = SPFPrimaryPanRuntime(image)
    state = runtime.state
    for index, name in enumerate(GPR64_BY_CODE):
        state.gpr[name] = (0x1000 + seed * 0x101 + index * 0x11111111) & MASK64
    state.gpr["RIP"] = 0x400000
    state.gpr["RBX"] = 0x500001 if unaligned else 0x500000
    state.gpr["RBP"] = 0x700800
    state.gpr["RSP"] = 0x700900
    state.rflags = 0x202 | ((seed & 1) << 0) | (((seed >> 1) & 1) << 6)
    memory.write(0x500000, bytes((seed + i) & 0xFF for i in range(256)), record=False)
    memory.write_int(state.gpr["RSP"], 0x400020 + seed, 8)
    memory.write_int(state.gpr["RBP"], 0x700A00 + seed, 8)
    state.xmm[0] = (0x00000000000000020000000000000001 + seed) & MASK128
    state.xmm[1] = (0x00000000000000040000000000000003 + seed * 3) & MASK128
    state.xmm[2] = (0xFFEEDDCCBBAA99887766554433221100 + seed) & MASK128
    if x87_ready:
        state.x87_top = 7
        state.x87[7] = 0x3FFF8000000000000000
        state.x87_tag = 0x3FFF
        state.x87_status = 7 << 11
    return runtime


def _imm32(seed: int) -> bytes:
    return int((seed * 0x10203 + 0x11223344) & 0xFFFFFFFF).to_bytes(4, "little")


def _rel32(seed: int) -> bytes:
    value = ((seed % 7) - 3) * 4
    return int(value & 0xFFFFFFFF).to_bytes(4, "little")


def _training_code_specs(samples_per_form: int) -> Iterable[tuple[bytes, dict[str, Any]]]:
    for seed in range(samples_per_form):
        low = seed & 7
        rex_b = 0x41 if seed & 8 else 0x40
        reg_modrm = 0xC0 | ((seed & 7) << 3) | ((seed + 1) & 7)
        mem_modrm = ((seed & 7) << 3) | 0x03
        yield b"\x90", {}
        yield b"\xcc", {}
        yield b"\x0f\x05", {}
        yield b"\x55", {}
        yield b"\x5d", {}
        yield b"\xc9", {}
        yield b"\xc3", {}
        yield b"\xe8" + _rel32(seed), {}
        yield b"\xe9" + _rel32(seed + 1), {}
        yield b"\xeb" + bytes([(seed % 9) - 4 & 0xFF]), {}
        yield bytes([0x48 | (rex_b & 1), 0xB8 + low]) + _imm32(seed) + _imm32(seed + 1), {}
        yield bytes([0xB8 + low]) + _imm32(seed), {}
        yield bytes([0x48, 0x89, reg_modrm]), {}
        yield bytes([0x48, 0x89, mem_modrm]), {}
        yield bytes([0x48, 0x8B, reg_modrm]), {}
        yield bytes([0x48, 0x8B, mem_modrm]), {}
        yield bytes([0x48, 0x8D, mem_modrm]), {}
        yield bytes([0x48, 0x8D, 0x35]) + _rel32(seed), {}
        yield bytes([0x31, reg_modrm]), {}
        yield bytes([0x31, mem_modrm]), {}
        yield bytes([0x48, 0x83, 0xC0 | ((seed + 1) & 7), seed & 0x7F]), {}
        yield bytes([0x48, 0x83, 0x00 | 0x03, seed & 0x7F]), {}
        yield bytes([0x48, 0x83, 0xE8 | ((seed + 1) & 7), seed & 0x7F]), {}
        yield bytes([0x48, 0x83, 0x28 | 0x03, seed & 0x7F]), {}
        yield bytes([0x48, 0xC7, 0xC0 | ((seed + 1) & 7)]) + _imm32(seed), {}
        yield bytes([0x48, 0xC7, 0x03]) + _imm32(seed), {}
        yield bytes([0x66, 0x0F, 0x6F, 0xC0 | ((seed & 7) << 3) | ((seed + 1) & 7)]), {}
        yield bytes([0x66, 0x0F, 0x6F, ((seed & 7) << 3) | 0x03]), {}
        yield bytes([0x66, 0x0F, 0x6F, ((seed & 7) << 3) | 0x03]), {"unaligned": True}
        yield bytes([0x66, 0x0F, 0x7F, 0xC0 | ((seed & 7) << 3) | ((seed + 1) & 7)]), {}
        yield bytes([0x66, 0x0F, 0x7F, ((seed & 7) << 3) | 0x03]), {}
        yield bytes([0xF3, 0x0F, 0x6F, 0xC0 | ((seed & 7) << 3) | ((seed + 1) & 7)]), {}
        yield bytes([0xF3, 0x0F, 0x6F, ((seed & 7) << 3) | 0x03]), {}
        yield bytes([0xF3, 0x0F, 0x7F, 0xC0 | ((seed & 7) << 3) | ((seed + 1) & 7)]), {}
        yield bytes([0xF3, 0x0F, 0x7F, ((seed & 7) << 3) | 0x03]), {}
        yield bytes([0x66, 0x0F, 0xEF, 0xC0 | ((seed & 7) << 3) | ((seed + 1) & 7)]), {}
        yield bytes([0x66, 0x0F, 0xEF, ((seed & 7) << 3) | 0x03]), {}
        yield bytes([0x66, 0x0F, 0xD4, 0xC0 | ((seed & 7) << 3) | ((seed + 1) & 7)]), {}
        yield bytes([0x66, 0x0F, 0xD4, ((seed & 7) << 3) | 0x03]), {}
        yield b"\xd9\xd0", {}
        yield b"\xd9\xe8", {}
        yield b"\xd9\xee", {}
        yield bytes([0xDD, 0xD8 + (seed & 7)]), {"x87_ready": True}


@dataclass
class RuntimeTrainingSample:
    raw: list[int]
    numeric: list[float]
    label: str


def build_training_samples(samples_per_form: int = 12) -> list[RuntimeTrainingSample]:
    from .model import BootstrapSPFTransitionModel

    model = BootstrapSPFTransitionModel()
    samples: list[RuntimeTrainingSample] = []
    for seed, (code, options) in enumerate(_training_code_specs(samples_per_form)):
        runtime = _fake_runtime(
            code,
            seed=seed,
            unaligned=bool(options.get("unaligned", False)),
            x87_ready=bool(options.get("x87_ready", False)),
        )
        instruction = decode_current(runtime)
        try:
            proposal = model.propose(runtime, instruction)
        except UnsupportedInstruction:
            continue
        if proposal.instruction_name not in RUNTIME_NEURAL_LABELS:
            continue
        raw, numeric = encode_runtime_features(runtime, instruction)
        samples.append(RuntimeTrainingSample(raw=raw, numeric=numeric, label=proposal.instruction_name))
    return samples


def _split_by_label(samples: Sequence[RuntimeTrainingSample], seed: int) -> tuple[list[int], list[int]]:
    rng = random.Random(seed)
    by_label: dict[str, list[int]] = {}
    for index, sample in enumerate(samples):
        by_label.setdefault(sample.label, []).append(index)
    train: list[int] = []
    val: list[int] = []
    for indices in by_label.values():
        rng.shuffle(indices)
        cut = max(1, int(len(indices) * 0.8))
        if len(indices) > 1:
            cut = min(cut, len(indices) - 1)
        train.extend(indices[:cut])
        val.extend(indices[cut:])
    rng.shuffle(train)
    rng.shuffle(val)
    return train, val


def _count_torch_params(model: Any) -> int:
    return int(sum(p.numel() for p in model.parameters()))


def _export_torch_model(model: Any, labels: Sequence[str], min_confidence: float) -> dict[str, Any]:
    state = model.state_dict()
    layers = []
    for name in ("fc1", "fc2", "out"):
        layers.append(
            {
                "weight": state[f"{name}.weight"].detach().cpu().tolist(),
                "bias": state[f"{name}.bias"].detach().cpu().tolist(),
            }
        )
    return {
        "labels": list(labels),
        "raw_byte_count": RAW_BYTE_COUNT,
        "numeric_feature_names": list(NUMERIC_FEATURE_NAMES),
        "byte_embedding": state["byte_embedding.weight"].detach().cpu().tolist(),
        "layers": layers,
        "min_confidence": float(min_confidence),
    }


def train_runtime_neural_model(
    model_out: Path,
    *,
    checkpoint_out: Optional[Path] = None,
    samples_per_form: int = 16,
    train_steps: int = 300,
    batch_size: int = 64,
    lr: float = 2e-3,
    seed: int = 1337,
    hidden_dim: int = DEFAULT_HIDDEN_DIM,
    embedding_dim: int = DEFAULT_EMBEDDING_DIM,
    min_confidence: float = 0.50,
    trace_manifest: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    try:
        import torch
        import torch.nn as nn
        import torch.nn.functional as F
    except Exception as exc:  # pragma: no cover - only exercised on no-torch hosts
        raise ValueError(f"training a runtime neural model requires torch: {exc}") from exc

    class TorchRuntimeNeuralHead(nn.Module):
        def __init__(self) -> None:
            super().__init__()
            self.byte_embedding = nn.Embedding(256, embedding_dim)
            input_dim = RAW_BYTE_COUNT * embedding_dim + len(NUMERIC_FEATURE_NAMES)
            self.fc1 = nn.Linear(input_dim, hidden_dim)
            self.fc2 = nn.Linear(hidden_dim, hidden_dim)
            self.out = nn.Linear(hidden_dim, len(RUNTIME_NEURAL_LABELS))

        def forward(self, raw: Any, numeric: Any) -> Any:
            x = self.byte_embedding(raw.long()).reshape(raw.shape[0], -1)
            x = torch.cat([x, numeric.float()], dim=-1)
            x = F.relu(self.fc1(x))
            x = F.relu(self.fc2(x))
            return self.out(x)

    samples = build_training_samples(samples_per_form=samples_per_form)
    if not samples:
        raise ValueError("runtime neural trainer produced no samples")
    label_to_index = {label: index for index, label in enumerate(RUNTIME_NEURAL_LABELS)}
    observed = sorted({sample.label for sample in samples})
    missing = sorted(set(RUNTIME_NEURAL_LABELS) - set(observed))
    if missing:
        raise ValueError(f"runtime neural trainer is missing labels: {missing}")

    train_idx, val_idx = _split_by_label(samples, seed)
    torch.manual_seed(seed)
    random.seed(seed)
    raw = torch.tensor([sample.raw for sample in samples], dtype=torch.long)
    numeric = torch.tensor([sample.numeric for sample in samples], dtype=torch.float32)
    target = torch.tensor([label_to_index[sample.label] for sample in samples], dtype=torch.long)
    model = TorchRuntimeNeuralHead()
    opt = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-4)
    generator = torch.Generator().manual_seed(seed)
    train_tensor = torch.tensor(train_idx, dtype=torch.long)
    history: list[dict[str, Any]] = []
    for step in range(max(1, train_steps)):
        take = train_tensor[torch.randint(len(train_tensor), (batch_size,), generator=generator)]
        logits = model(raw[take], numeric[take])
        loss = F.cross_entropy(logits, target[take])
        opt.zero_grad()
        loss.backward()
        opt.step()
        if step in {0, train_steps - 1} or (step + 1) % max(1, train_steps // 5) == 0:
            with torch.no_grad():
                train_pred = model(raw[train_idx], numeric[train_idx]).argmax(dim=1)
                val_pred = model(raw[val_idx], numeric[val_idx]).argmax(dim=1)
            history.append(
                {
                    "step": step + 1,
                    "loss": round(float(loss.item()), 6),
                    "train_exact": round(float((train_pred == target[train_idx]).float().mean().item()), 6),
                    "val_exact": round(float((val_pred == target[val_idx]).float().mean().item()), 6),
                }
            )

    export = _export_torch_model(model, RUNTIME_NEURAL_LABELS, min_confidence)
    runtime_export = RuntimeNeuralExport.from_manifest({"weights": export})
    train_exact = history[-1]["train_exact"]
    val_exact = history[-1]["val_exact"]
    parameter_count = _count_torch_params(model)
    model_out = Path(model_out)
    checkpoint_out = Path(checkpoint_out) if checkpoint_out is not None else model_out.with_suffix(".pt")
    manifest = {
        "ok": True,
        "schema_version": RUNTIME_NEURAL_SCHEMA,
        "model_id": model_out.stem,
        "model_kind": "learned_neural_transition_model",
        "runtime": "pan-isa-x86-runtime-spf",
        "runtime_mode": "learned",
        "target_profile": "long64-ring3",
        "trainable_weights_loaded": True,
        "runtime_execution_head_loaded": True,
        "primary_semantics_path": "learned neural transition-family head plus SPF typed proposal adapter",
        "commit_contract": "typed exact architectural state transition",
        "parameter_count": parameter_count,
        "labels": list(RUNTIME_NEURAL_LABELS),
        "promoted_forms": list(RUNTIME_NEURAL_LABELS),
        "raw_byte_count": RAW_BYTE_COUNT,
        "numeric_feature_names": list(NUMERIC_FEATURE_NAMES),
        "embedding_dim": embedding_dim,
        "hidden_dim": hidden_dim,
        "min_confidence": min_confidence,
        "weights": export,
        "training": {
            "samples": len(samples),
            "train_samples": len(train_idx),
            "validation_samples": len(val_idx),
            "samples_per_form": samples_per_form,
            "train_steps_requested": train_steps,
            "train_steps_completed": train_steps,
            "batch_size": batch_size,
            "lr": lr,
            "seed": seed,
            "history": history,
            "final_train_exact": train_exact,
            "final_validation_exact": val_exact,
            "observed_labels": observed,
            "trace_manifest": trace_manifest,
        },
    }
    _write_json(model_out, manifest)
    torch.save(
        {
            "schema_version": RUNTIME_NEURAL_SCHEMA,
            "manifest": {k: v for k, v in manifest.items() if k != "weights"},
            "runtime_neural_export": export,
            "state_dict": model.state_dict(),
        },
        checkpoint_out,
    )
    manifest["artifact_path"] = str(model_out)
    manifest["checkpoint_path"] = str(checkpoint_out)
    manifest["model_artifact_hash"] = _file_sha256(model_out)
    manifest["checkpoint_hash"] = _file_sha256(checkpoint_out)
    manifest["export_parameter_count"] = runtime_export.parameter_count()
    manifest["trained_weights_written"] = True
    return {k: v for k, v in manifest.items() if k != "weights"}
