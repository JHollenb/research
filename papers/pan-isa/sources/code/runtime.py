"""Standalone PAN x86 runtime whose instruction path goes through SPF proposals."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

from .compat import ensure_scripts_importable
from .action_ledger import isa_transition_ledger_row
from .fabric_executor import FabricValueStore
from .model import BootstrapSPFTransitionModel
from .pan_fabric_integrated import (
    PAN_FABRIC_MODES,
    backend_for_fabric_mode,
    trace_record_from_route,
    training_record_from_trace,
)
from .pl_router import RuntimeRouter
from .transitions import TransitionProposal, validate_transition_proposal

ensure_scripts_importable()

from pan_x86_isa.memory import MemoryFault  # noqa: E402
from pan_x86_isa.process import load_elf64  # noqa: E402
from pan_x86_isa.runtime import MASK64, PanRuntime, StopReason, runtime_scope as base_runtime_scope  # noqa: E402


def runtime_scope() -> Dict[str, object]:
    scope = dict(base_runtime_scope())
    unsupported = [
        item
        for item in scope.get("unsupported_cases", [])
        if item not in {"Full SIMD/x87/vector state.", "all remaining unimplemented Linux x86-64 syscalls"}
    ]
    unsupported.append("SIMD/x87 outside the runtime Stage 4 subset")
    unsupported.append("all remaining unimplemented Linux x86-64 syscalls")
    scope.update(
        {
            "runtime": "pan-isa-x86-runtime-spf",
            "instruction_semantics": "SPF primary typed transition proposals",
            "requires_qemu_for_execution": False,
            "uses_bob_spf": True,
            "first_milestone": "static long64-ring3 ELF",
            "simd_x87_scope": [
                "SSE/SSE2 XMM register and m128 memory heads for MOVDQA, MOVDQU, PXOR, and PADDQ",
                "aligned MOVDQA m128 #GP(0) fail-closed behavior",
                "x87 stack-register heads for FNOP, FLD1, FLDZ, and FSTP ST(i)",
            ],
            "ps_pl_routing": {
                "authority": "PS validates and commits every transition",
                "backends": ["auto", "ps", "pl-sim", "pl-xrt"],
                "fabric_daemon": "optional resident PS service for typed SPF graph packets over Unix sockets",
                "v1_pl_subset": [
                    "MOVDQU_XMM_M128",
                    "MOVDQU_M128_XMM",
                    "PXOR_XMM_XMM",
                    "PXOR_XMM_M128",
                    "PADDQ_XMM_XMM",
                    "PADDQ_XMM_M128",
                ],
                "x87": "PS-only in v1",
            },
            "dynamic_linking": False,
            "threading": False,
            "signals": False,
            "unsupported_cases": unsupported,
        }
    )
    return scope


class SPFPrimaryPanRuntime(PanRuntime):
    """PAN runtime with a model proposal/commit instruction execution path."""

    def __init__(
        self,
        image: object,
        model: Optional[Any] = None,
        *,
        profile: str = "long64-ring3",
        trace_proposals: bool = False,
        backend: str = "auto",
        pl_xclbin: Optional[str] = None,
        pl_kernel_name: str = "pan_simd_v1",
        pl_min_instructions: int = 8,
        pl_min_groups: int = 2,
        fabric_mode: str = "backend",
        fabric_daemon_socket: Optional[str] = None,
        trace_action_ledger: bool = False,
    ):
        super().__init__(image)
        if fabric_mode not in PAN_FABRIC_MODES:
            raise ValueError(f"unsupported PAN fabric mode {fabric_mode!r}; expected one of {PAN_FABRIC_MODES}")
        self.model = model or BootstrapSPFTransitionModel()
        self.profile = profile
        self.last_model_proposal: Optional[TransitionProposal] = None
        self.model_transition_count = 0
        self.proposal_trace: List[Dict[str, Any]] = []
        self.trace_proposals = trace_proposals
        self.trace_action_ledger = trace_action_ledger
        self.action_ledger_rows: List[Dict[str, Any]] = []
        self.fabric_mode = fabric_mode
        self.fabric_daemon_socket = fabric_daemon_socket
        resolved_backend = backend_for_fabric_mode(fabric_mode, requested_backend=backend, pl_xclbin=pl_xclbin)
        self.backend_mode = resolved_backend
        self.router = RuntimeRouter(
            backend=resolved_backend,
            pl_xclbin=pl_xclbin,
            pl_kernel_name=pl_kernel_name,
            min_instructions=pl_min_instructions,
            min_repeated_groups=pl_min_groups,
        )
        self.route_trace: List[Dict[str, Any]] = []
        self.fabric_trace: List[Dict[str, Any]] = []
        self.fabric_training_records: List[Dict[str, Any]] = []
        self.fabric_value_store = FabricValueStore(session_id=f"runtime-fabric-{id(self):x}")

    @classmethod
    def from_elf(
        cls,
        path: Path,
        argv: Optional[List[str]] = None,
        env: Optional[Dict[str, str]] = None,
        *,
        uid: Optional[int] = None,
        euid: Optional[int] = None,
        gid: Optional[int] = None,
        egid: Optional[int] = None,
        model: Optional[Any] = None,
        profile: str = "long64-ring3",
        trace_proposals: bool = False,
        backend: str = "auto",
        pl_xclbin: Optional[str] = None,
        pl_kernel_name: str = "pan_simd_v1",
        pl_min_instructions: int = 8,
        pl_min_groups: int = 2,
        fabric_mode: str = "backend",
        fabric_daemon_socket: Optional[str] = None,
        trace_action_ledger: bool = False,
    ) -> "SPFPrimaryPanRuntime":
        return cls(
            load_elf64(Path(path), argv=argv, env=env, uid=uid, euid=euid, gid=gid, egid=egid),
            model=model,
            profile=profile,
            trace_proposals=trace_proposals,
            backend=backend,
            pl_xclbin=pl_xclbin,
            pl_kernel_name=pl_kernel_name,
            pl_min_instructions=pl_min_instructions,
            pl_min_groups=pl_min_groups,
            fabric_mode=fabric_mode,
            fabric_daemon_socket=fabric_daemon_socket,
            trace_action_ledger=trace_action_ledger,
        )

    def _step_instruction(self) -> StopReason:
        routed = self.router.route(self)
        proposal = routed.proposal
        action_constraints = self._transition_action_constraints()
        action_state = self._transition_action_state(proposal)
        self.last_model_proposal = proposal
        self.model_transition_count += routed.instruction_count
        self.route_trace.append(routed.decision.to_json())
        if self.trace_proposals:
            self.proposal_trace.append(proposal.to_json())
        reason = self._commit_transition(proposal, constraints=action_constraints)
        committed = reason.kind == "running" and proposal.kind in {"normal", "syscall", "breakpoint"}
        if self.trace_action_ledger:
            self.action_ledger_rows.append(
                isa_transition_ledger_row(
                    action_state,
                    {
                        "kind": "execute_instruction",
                        "instruction": proposal.instruction_name,
                        "rip": hex(int(proposal.rip)),
                    },
                    action_constraints,
                    proposal,
                    measurement={
                        "environment": {
                            "runtime": "pan-isa-x86-runtime-spf",
                            "backend_mode": self.backend_mode,
                            "fabric_mode": self.fabric_mode,
                        },
                        "metrics": {
                            "runtime_stop_reason": reason.to_json(),
                            "routed_instruction_count": routed.instruction_count,
                            "committed": committed,
                        },
                    },
                    lineage={"source": "SPFPrimaryPanRuntime._step_instruction"},
                )
            )
        fabric_trace = trace_record_from_route(
            routed,
            reason,
            fabric_mode=self.fabric_mode,
            committed=committed,
            fabric_daemon_socket=self.fabric_daemon_socket,
        )
        self._attach_fabric_values(fabric_trace)
        self.fabric_trace.append(fabric_trace)
        self.fabric_training_records.append(training_record_from_trace(fabric_trace, routed, reason))
        return reason

    def _transition_action_constraints(self) -> Dict[str, Any]:
        manifest = getattr(self.model, "manifest", {})
        confidence_threshold = 1.0
        if manifest.get("runtime_mode") == "learned":
            confidence_threshold = float(manifest.get("runtime_confidence_threshold", manifest.get("min_confidence", 1.0)))
        return {
            "expected_profile": self.profile,
            "exact_confidence": confidence_threshold,
            "require_learned": bool(manifest.get("runtime_mode") == "learned"),
            "backend_mode": self.backend_mode,
            "fabric_mode": self.fabric_mode,
        }

    def _transition_action_state(self, proposal: TransitionProposal) -> Dict[str, Any]:
        return {
            "rip": hex(int(proposal.rip)),
            "profile": self.profile,
            "backend_mode": self.backend_mode,
            "fabric_mode": self.fabric_mode,
            "steps_before": int(self.steps),
            "route_index": len(self.route_trace),
        }

    def _attach_fabric_values(self, trace: Dict[str, Any]) -> None:
        graph = dict(trace.get("graph") or {})
        buffers = dict(graph.get("buffers") or {})
        graph_id = str(trace.get("graph_id") or "graph_unknown")
        input_ids = {}
        for name in sorted(trace.get("input_value_ids") or {}):
            spec = dict(buffers.get(name) or {})
            value = self.fabric_value_store.create_metadata(
                name,
                elements=int(spec.get("elements") or max(1, int(trace.get("instruction_count") or 1))),
                residency="ps",
                materialized=True,
                producer=graph_id,
                metadata={
                    "graph_id": graph_id,
                    "direction": "input",
                    "region_kind": trace.get("region_kind"),
                },
            )
            input_ids[name] = value.value_id
        output_ids = {}
        for name in sorted(trace.get("output_value_ids") or {}):
            spec = dict(buffers.get(name) or {})
            residency = str((trace.get("residency_after") or {}).get(name) or "unknown")
            materialization_reason = trace.get("materialization_reason")
            value = self.fabric_value_store.create_metadata(
                name,
                elements=int(spec.get("elements") or max(1, int(trace.get("instruction_count") or 1))),
                residency=residency,
                materialized=residency == "ps" or materialization_reason is not None,
                producer=graph_id,
                validation=dict(trace.get("validation") or {}),
                materialization_reason=None if materialization_reason is None else str(materialization_reason),
                metadata={
                    "graph_id": graph_id,
                    "direction": "output",
                    "region_kind": trace.get("region_kind"),
                    "placement_action": trace.get("placement_action"),
                },
            )
            output_ids[name] = value.value_id
            trace.setdefault("residency_after", {})[name] = value.residency
        trace["input_value_ids"] = input_ids
        trace["output_value_ids"] = output_ids

    def _commit_transition(self, proposal: TransitionProposal, *, constraints: Optional[Dict[str, Any]] = None) -> StopReason:
        constraints = dict(constraints or self._transition_action_constraints())
        validation_error = validate_transition_proposal(
            proposal,
            expected_profile=str(constraints.get("expected_profile", self.profile)),
            exact_confidence=float(constraints.get("exact_confidence", 1.0)),
            require_learned=bool(constraints.get("require_learned", False)),
        )
        if validation_error is not None:
            return validation_error
        if proposal.stop_reason is not None and proposal.kind in {"unsupported", "fault", "exception"}:
            return proposal.stop_reason
        assert proposal.next_rip is not None
        for write in proposal.memory_writes:
            self.memory.write(write.address, write.data)
        for name, value in proposal.register_writes.items():
            self.state.gpr[name] = int(value) & MASK64
        for name, value in proposal.xmm_writes.items():
            index = int(name[3:])
            self.state.xmm[index] = int(value) & ((1 << 128) - 1)
        if proposal.rflags is not None:
            self.state.rflags = int(proposal.rflags) & MASK64
        if proposal.mxcsr is not None:
            self.state.mxcsr = int(proposal.mxcsr) & 0xFFFFFFFF
        if proposal.x87_state is not None:
            stack = proposal.x87_state["st"]
            self.state.x87 = [None if value is None else int(value) & ((1 << 80) - 1) for value in stack]
            self.state.x87_top = int(proposal.x87_state["top"]) & 0x7
            self.state.x87_tag = int(proposal.x87_state["tag"]) & 0xFFFF
            self.state.x87_status = int(proposal.x87_state["status"]) & 0xFFFF
            self.state.x87_control = int(proposal.x87_state["control"]) & 0xFFFF
        self.state.gpr["RIP"] = int(proposal.next_rip) & MASK64
        if proposal.kind == "syscall":
            return self._syscall()
        if proposal.stop_reason is not None:
            return proposal.stop_reason
        return StopReason("running")

    def summary(self) -> Dict[str, Any]:
        payload = super().summary()
        payload["runtime_scope"] = runtime_scope()
        payload["model_manifest"] = self.model.manifest
        payload["runtime_profile"] = self.profile
        payload["model_transition_count"] = self.model_transition_count
        payload["last_model_proposal"] = None if self.last_model_proposal is None else self.last_model_proposal.to_json()
        payload["proposal_trace_count"] = len(self.proposal_trace)
        payload["action_ledger_row_count"] = len(self.action_ledger_rows)
        payload["fabric_mode"] = self.fabric_mode
        payload["fabric_daemon_socket"] = self.fabric_daemon_socket
        payload["fabric_trace_count"] = len(self.fabric_trace)
        payload["fabric_training_record_count"] = len(self.fabric_training_records)
        payload["fabric_value_store"] = self.fabric_value_store.to_json()
        payload["backend_mode"] = self.backend_mode
        payload["backend_stats"] = self.router.stats
        payload["route_trace_count"] = len(self.route_trace)
        return payload
