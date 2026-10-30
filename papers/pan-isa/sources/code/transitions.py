"""Typed transition proposals for the SPF runtime executor."""
from __future__ import annotations

from dataclasses import dataclass, field
import math
from typing import Any, Optional

from .compat import ensure_scripts_importable

ensure_scripts_importable()

from pan_x86_isa.runtime import GPR64_BY_CODE, MASK64, StopReason  # noqa: E402


MASK80 = (1 << 80) - 1
MASK128 = (1 << 128) - 1


SUPPORTED_KINDS = {
    "normal",
    "syscall",
    "breakpoint",
    "fault",
    "exception",
    "unsupported",
}
SUPPORTED_MEMORY_WRITE_SIZES = {1, 2, 4, 8, 16, 32, 64}
SUPPORTED_STAGES = {
    "stage0_register_scalar",
    "stage1_address_memory",
    "stage2_control_flow",
    "stage3_complex_scalar",
    "stage4_simd_x87",
}
USER64_CANONICAL_BITS = 48


def _validation_stop(detail: str, *, address: Optional[int] = None) -> StopReason:
    return StopReason("unsupported_runtime_feature", detail=detail, address=address)


def _is_u64(value: Any) -> bool:
    return isinstance(value, int) and 0 <= int(value) <= MASK64


def _parse_u64_address(value: Any) -> Optional[int]:
    if _is_u64(value):
        return int(value)
    if isinstance(value, str):
        try:
            parsed = int(value, 16) if value.lower().startswith("0x") else int(value, 10)
        except ValueError:
            return None
        if 0 <= parsed <= MASK64:
            return parsed
    return None


def _is_canonical_user64(value: int) -> bool:
    """Return whether an address is canonical under 48-bit user64 addressing."""
    sign = 1 << (USER64_CANONICAL_BITS - 1)
    low_mask = (1 << USER64_CANONICAL_BITS) - 1
    low = int(value) & low_mask
    canonical = low | (~low_mask & MASK64) if low & sign else low
    return (int(value) & MASK64) == canonical


@dataclass(frozen=True)
class MemoryWrite:
    address: int
    data: bytes
    access: str = "write"

    def to_json(self) -> dict[str, Any]:
        return {
            "address": hex(int(self.address)),
            "size": len(self.data),
            "data_hex": self.data.hex(),
            "access": self.access,
        }


@dataclass(frozen=True)
class TransitionProposal:
    kind: str
    rip: int
    instruction_hex: str
    instruction_name: str
    stage: Optional[str] = None
    effect_axes: dict[str, Any] = field(default_factory=dict)
    profile: Optional[str] = None
    iclass: Optional[str] = None
    iform: Optional[str] = None
    operands: tuple[dict[str, Any], ...] = ()
    widths: dict[str, int] = field(default_factory=dict)
    next_rip: Optional[int] = None
    register_writes: dict[str, int] = field(default_factory=dict)
    register_write_masks: dict[str, int] = field(default_factory=dict)
    xmm_writes: dict[str, int] = field(default_factory=dict)
    xmm_write_masks: dict[str, int] = field(default_factory=dict)
    memory_writes: tuple[MemoryWrite, ...] = ()
    memory_reads: tuple[dict[str, Any], ...] = ()
    rflags: Optional[int] = None
    flag_write_mask: Optional[int] = None
    flag_defined_mask: Optional[int] = None
    mxcsr: Optional[int] = None
    x87_state: Optional[dict[str, Any]] = None
    exception: Optional[dict[str, Any]] = None
    stop_reason: Optional[StopReason] = None
    spf_manifest: dict[str, Any] = field(default_factory=dict)
    model_artifact_hash: Optional[str] = None
    source_hashes: dict[str, str] = field(default_factory=dict)
    family_provenance: Optional[str] = None
    confidence: float = 1.0

    def to_json(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "rip": hex(int(self.rip)),
            "instruction_hex": self.instruction_hex,
            "instruction_name": self.instruction_name,
            "stage": self.stage,
            "effect_axes": dict(self.effect_axes),
            "profile": self.profile,
            "iclass": self.iclass,
            "iform": self.iform,
            "operands": list(self.operands),
            "widths": dict(self.widths),
            "next_rip": None if self.next_rip is None else hex(int(self.next_rip)),
            "register_writes": {name: hex(value) for name, value in sorted(self.register_writes.items())},
            "register_write_masks": {name: hex(value) for name, value in sorted(self.register_write_masks.items())},
            "xmm_writes": {name: f"0x{int(value) & MASK128:032x}" for name, value in sorted(self.xmm_writes.items())},
            "xmm_write_masks": {name: f"0x{int(value) & MASK128:032x}" for name, value in sorted(self.xmm_write_masks.items())},
            "memory_reads": list(self.memory_reads),
            "memory_writes": [write.to_json() for write in self.memory_writes],
            "rflags": None if self.rflags is None else hex(int(self.rflags)),
            "flag_write_mask": None if self.flag_write_mask is None else hex(int(self.flag_write_mask)),
            "flag_defined_mask": None if self.flag_defined_mask is None else hex(int(self.flag_defined_mask)),
            "mxcsr": None if self.mxcsr is None else hex(int(self.mxcsr) & 0xFFFFFFFF),
            "x87_state": self.x87_state,
            "exception": self.exception,
            "stop_reason": None if self.stop_reason is None else self.stop_reason.to_json(),
            "confidence": float(self.confidence),
            "model_artifact_hash": self.model_artifact_hash,
            "source_hashes": dict(self.source_hashes),
            "family_provenance": self.family_provenance,
            "spf": self.spf_manifest,
        }


def validate_transition_proposal(
    proposal: TransitionProposal,
    *,
    expected_profile: str = "long64-ring3",
    exact_confidence: float = 1.0,
    require_learned: bool = False,
) -> Optional[StopReason]:
    """Validate a typed proposal before architectural commit.

    The runtime is deliberately fail-closed: malformed learned outputs return a
    StopReason and commit nothing. Bootstrap proposals pass through the same
    checks so learned and deterministic modes share one commit contract.
    """
    if proposal.kind not in SUPPORTED_KINDS:
        return _validation_stop(f"unsupported transition kind: {proposal.kind!r}", address=proposal.rip)
    if not _is_u64(proposal.rip) or not _is_canonical_user64(proposal.rip):
        return _validation_stop("SPF transition has non-canonical rip", address=proposal.rip)
    if proposal.profile is not None and proposal.profile != expected_profile:
        return _validation_stop(
            f"SPF transition profile {proposal.profile!r} does not match runtime profile {expected_profile!r}",
            address=proposal.rip,
        )
    manifest_profile = proposal.spf_manifest.get("target_profile") or proposal.spf_manifest.get("profile")
    if manifest_profile is not None and manifest_profile != expected_profile:
        return _validation_stop(
            f"SPF manifest profile {manifest_profile!r} does not match runtime profile {expected_profile!r}",
            address=proposal.rip,
        )
    if require_learned and not proposal.spf_manifest.get("trainable_weights_loaded"):
        return _validation_stop("learned runtime mode received a non-learned transition proposal", address=proposal.rip)
    if require_learned and proposal.kind == "normal" and (not proposal.stage or not proposal.effect_axes):
        return _validation_stop("learned runtime transition omitted stage/effect_axes contract", address=proposal.rip)
    if proposal.stage is not None and proposal.stage not in SUPPORTED_STAGES:
        return _validation_stop(f"SPF transition stage {proposal.stage!r} is not supported", address=proposal.rip)
    if proposal.effect_axes and not isinstance(proposal.effect_axes, dict):
        return _validation_stop("SPF transition effect_axes must be a JSON object", address=proposal.rip)
    if proposal.stage is not None and proposal.effect_axes.get("stage") not in (None, proposal.stage):
        return _validation_stop("SPF transition effect_axes stage does not match proposal stage", address=proposal.rip)
    if not isinstance(proposal.confidence, (float, int)) or not math.isfinite(float(proposal.confidence)):
        return _validation_stop("SPF model confidence is not finite", address=proposal.rip)
    if float(proposal.confidence) < exact_confidence:
        return _validation_stop(
            f"SPF model confidence below exact threshold: {proposal.confidence}",
            address=proposal.rip,
        )

    may_stop_without_rip = proposal.stop_reason is not None and proposal.kind in {"unsupported", "fault", "exception"}
    if proposal.next_rip is None and not may_stop_without_rip:
        return _validation_stop("SPF transition omitted next_rip", address=proposal.rip)
    if proposal.next_rip is not None and (not _is_u64(proposal.next_rip) or not _is_canonical_user64(proposal.next_rip)):
        return _validation_stop("SPF transition has non-canonical next_rip", address=proposal.rip)

    allowed_gprs = set(GPR64_BY_CODE)
    for name, value in proposal.register_writes.items():
        if name == "RIP":
            return _validation_stop("SPF transition must use next_rip instead of a RIP register write", address=proposal.rip)
        if name not in allowed_gprs:
            return _validation_stop(f"SPF transition writes unsupported register {name!r}", address=proposal.rip)
        if not _is_u64(value):
            return _validation_stop(f"SPF transition register write {name!r} is not a u64 value", address=proposal.rip)
    for name, mask in proposal.register_write_masks.items():
        if name not in allowed_gprs:
            return _validation_stop(f"SPF transition masks unsupported register {name!r}", address=proposal.rip)
        if not _is_u64(mask):
            return _validation_stop(f"SPF transition register mask {name!r} is not a u64 mask", address=proposal.rip)
    allowed_xmm = {f"XMM{i}" for i in range(16)}
    for name, value in proposal.xmm_writes.items():
        if name not in allowed_xmm:
            return _validation_stop(f"SPF transition writes unsupported XMM register {name!r}", address=proposal.rip)
        if not isinstance(value, int) or not 0 <= int(value) <= MASK128:
            return _validation_stop(f"SPF transition XMM write {name!r} is not a u128 value", address=proposal.rip)
    for name, mask in proposal.xmm_write_masks.items():
        if name not in allowed_xmm:
            return _validation_stop(f"SPF transition masks unsupported XMM register {name!r}", address=proposal.rip)
        if not isinstance(mask, int) or not 0 <= int(mask) <= MASK128:
            return _validation_stop(f"SPF transition XMM mask {name!r} is not a u128 mask", address=proposal.rip)
    if proposal.rflags is not None and not _is_u64(proposal.rflags):
        return _validation_stop("SPF transition rflags is not a u64 value", address=proposal.rip)
    if proposal.flag_write_mask is not None and not _is_u64(proposal.flag_write_mask):
        return _validation_stop("SPF transition flag_write_mask is not a u64 mask", address=proposal.rip)
    if proposal.flag_defined_mask is not None and not _is_u64(proposal.flag_defined_mask):
        return _validation_stop("SPF transition flag_defined_mask is not a u64 mask", address=proposal.rip)
    if proposal.mxcsr is not None and (not isinstance(proposal.mxcsr, int) or not 0 <= int(proposal.mxcsr) <= 0xFFFFFFFF):
        return _validation_stop("SPF transition mxcsr is not a u32 value", address=proposal.rip)
    if proposal.x87_state is not None:
        if not isinstance(proposal.x87_state, dict):
            return _validation_stop("SPF transition x87_state is not a JSON object", address=proposal.rip)
        stack = proposal.x87_state.get("st")
        if not isinstance(stack, list) or len(stack) != 8:
            return _validation_stop("SPF transition x87_state.st must contain 8 physical registers", address=proposal.rip)
        for value in stack:
            if value is not None and (not isinstance(value, int) or not 0 <= int(value) <= MASK80):
                return _validation_stop("SPF transition x87 register is not null or u80", address=proposal.rip)
        for field_name, mask in (("top", 0x7), ("tag", 0xFFFF), ("status", 0xFFFF), ("control", 0xFFFF)):
            value = proposal.x87_state.get(field_name)
            if not isinstance(value, int) or not 0 <= int(value) <= mask:
                return _validation_stop(f"SPF transition x87_state.{field_name} is out of range", address=proposal.rip)

    for read in proposal.memory_reads:
        if not isinstance(read, dict):
            return _validation_stop("SPF transition memory read event is not a JSON object", address=proposal.rip)
        if read.get("access", "read") != "read":
            return _validation_stop(f"SPF transition memory read access {read.get('access')!r} is not read", address=proposal.rip)
        size = read.get("size")
        if not isinstance(size, int) or size not in SUPPORTED_MEMORY_WRITE_SIZES:
            return _validation_stop("SPF transition memory read has unsupported size", address=proposal.rip)
        address = _parse_u64_address(read.get("address"))
        if address is None or not _is_canonical_user64(address):
            return _validation_stop("SPF transition memory read has non-canonical address", address=proposal.rip)
        end = address + size - 1
        if end > MASK64 or not _is_canonical_user64(end):
            return _validation_stop("SPF transition memory read crosses a non-canonical boundary", address=proposal.rip)

    for write in proposal.memory_writes:
        if write.access != "write":
            return _validation_stop(f"SPF transition memory access {write.access!r} is not commit-write", address=write.address)
        if not isinstance(write.data, (bytes, bytearray)):
            return _validation_stop("SPF transition memory write data is not bytes", address=write.address)
        if len(write.data) not in SUPPORTED_MEMORY_WRITE_SIZES:
            return _validation_stop(f"SPF transition memory write has unsupported size {len(write.data)}", address=write.address)
        if not _is_u64(write.address) or not _is_canonical_user64(write.address):
            return _validation_stop("SPF transition memory write has non-canonical address", address=write.address)
        end = int(write.address) + len(write.data) - 1
        if end > MASK64 or not _is_canonical_user64(end):
            return _validation_stop("SPF transition memory write crosses a non-canonical boundary", address=write.address)
    return None
