"""Recipient-local edits of a qualified, sign-coded native value carrier.

This module knows no opcode, expected output, counterfactual activation or donor.
The caller supplies a previously measured role and its exact execution binding.
The native consumer remains responsible for the consequence of the requested edit.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

ROLE = "observed.aligned_window64"


def cut_state_identity(cut: Any) -> str:
    """Exact state identity while allowing a direct common-parent fork."""
    from saturn_pub.values import digest

    manifest = cut.manifest()
    manifest.pop("parent")
    return digest(manifest)


@dataclass(frozen=True)
class ValueBinding:
    role: str
    model_identity: str
    context: str
    graph_fingerprint: str
    parent_cut: str
    state_identity: str
    slot: str
    shape: tuple[int, ...]
    consumer: str

    def validate(self, session: Any) -> None:
        """A shared readable name alone never grants address equivalence."""
        if self.role != ROLE:
            raise ValueError("unsupported measured value role")
        current = session.capture(retain=False)
        if (session.adapter.model_identity != self.model_identity
                or session.adapter.context != self.context
                or session.adapter.graph_fingerprint != self.graph_fingerprint
                or current.fingerprint != self.parent_cut and current.parent != self.parent_cut
                or cut_state_identity(current) != self.state_identity):
            raise ValueError("symbol edit does not match its model/context/parent binding")
        if tuple(session.read(self.slot).shape) != self.shape:
            raise ValueError("symbol carrier geometry changed")
        specs = {spec.slot: spec for spec in session.adapter.node_specs}
        if self.consumer not in specs[self.slot].users:
            raise ValueError("symbol carrier no longer feeds the measured native consumer")


def reflect_coordinates(value: Any, masks: tuple[int, ...]):
    """XOR represented bits by reflecting only recipient-local coordinates.

    Masks are ordinary caller-requested edits, rather than answers. Sign coding
    and bit order are measured/supplied interpretation contracts. Magnitudes,
    dtype, device, layout and every unselected coordinate are preserved.
    """
    import torch

    if (not isinstance(value, torch.Tensor) or value.ndim != 3
            or tuple(value.shape[1:]) != (64, 1) or not value.is_floating_point()
            or not bool(torch.isfinite(value).all())):
        raise ValueError("expected a finite floating [batch,64,1] carrier")
    if len(masks) != value.shape[0] or any(
        isinstance(mask, bool) or not isinstance(mask, int) or not 0 <= mask < 1 << 64
        for mask in masks
    ):
        raise ValueError("one uint64 edit mask is required per recipient")
    selected = torch.tensor(
        [[bool(mask & (1 << bit)) for bit in range(64)] for mask in masks],
        dtype=torch.bool, device=value.device,
    ).unsqueeze(-1)
    result = value.clone(memory_format=torch.preserve_format)
    result[selected] = -value[selected]
    return result


@dataclass(frozen=True)
class ReflectValue:
    slot: str
    masks: tuple[int, ...]

    def __call__(self, reads):
        return {self.slot: reflect_coordinates(reads[self.slot], self.masks)}


def value_xor_act(slot: str, masks: tuple[int, ...], name: str):
    """Lower the request to a pure public Saturn Act over the live value."""
    import hashlib
    import json

    from saturn_pub.core import Act

    operation = ReflectValue(slot, masks)
    recipe = {"role": ROLE, "slot": slot, "masks": list(masks)}
    identity = hashlib.sha256(json.dumps(recipe, sort_keys=True).encode()).hexdigest()
    operation_id = "isa.symbol-value.recipient-reflection." + identity
    Act.register_operation(operation_id, "1", operation, pure=True)
    return Act.registered(
        name, (slot,), (slot,), operation_id=operation_id,
        operation_version="1", implementation=operation,
        parameters={**recipe, "payload_origin": "recipient-live-value-only",
                    "operation": "coordinate-sign-reflection"},
    )


def edit_symbol_value(session: Any, symbols: Any, binding: ValueBinding,
                      masks: tuple[int, ...], name: str):
    """Resolve the public symbol table, then request a separately typed write.

    The sidecar is read-only debug information. The Act, writable native port
    and exact binding checks supply mutation mechanics, rather than the alias.
    """
    binding.validate(session)
    resolved = symbols.resolve(session, binding.role, context=binding.context)
    if len(resolved.locations) != 1 or resolved.locations[0].slot != binding.slot:
        raise ValueError("public symbol table and functional carrier disagree")
    return session.apply(value_xor_act(binding.slot, masks, name))
