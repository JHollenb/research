"""Adapter for the Bob SPF/SPFTensor/SPFBlockMatrix implementation."""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np

from .compat import DEFAULT_BOB_SPF_SRC, install_python310_shims


class SPFBackendUnavailable(RuntimeError):
    """Raised when the Bob SPF implementation cannot be imported."""


@dataclass(frozen=True)
class SPFModules:
    source_root: Path
    AxisSpec: type
    SPFActionSpec: type
    SPFBlockMatrix: type
    SPFExecutionPolicy: type
    SPFGaugeSpec: type
    SPFMeasureSpec: type
    SPFProof: type
    SPFTransportKernel: type
    apply_transport: Any
    lower_transport: Any


@dataclass(frozen=True)
class SPFKernelBundle:
    source_root: str
    policy: Any
    identity: Any
    selector: Any
    transport: Any
    lowering: Any
    manifest: dict[str, Any]


def _bob_spf_src() -> Path:
    return Path(os.environ.get("PAN_BOB_SPF_SRC", str(DEFAULT_BOB_SPF_SRC))).expanduser()


@lru_cache(maxsize=1)
def import_spf_modules() -> SPFModules:
    src = _bob_spf_src()
    if not src.exists():
        raise SPFBackendUnavailable(f"Bob SPF source root does not exist: {src}")
    install_python310_shims()
    src_text = str(src)
    if src_text not in sys.path:
        sys.path.insert(0, src_text)
    try:
        from spf.tensor.kernel import AxisSpec, SPFBlockMatrix, SPFProof
        from spf.tensor.policy import SPFExecutionPolicy
        from spf.tensor.transport import (
            SPFActionSpec,
            SPFGaugeSpec,
            SPFMeasureSpec,
            SPFTransportKernel,
            apply_transport,
            lower_transport,
        )
    except Exception as exc:  # pragma: no cover - exercised when dependency is missing
        raise SPFBackendUnavailable(f"failed to import Bob SPF modules from {src}: {exc}") from exc
    return SPFModules(
        source_root=src,
        AxisSpec=AxisSpec,
        SPFActionSpec=SPFActionSpec,
        SPFBlockMatrix=SPFBlockMatrix,
        SPFExecutionPolicy=SPFExecutionPolicy,
        SPFGaugeSpec=SPFGaugeSpec,
        SPFMeasureSpec=SPFMeasureSpec,
        SPFProof=SPFProof,
        SPFTransportKernel=SPFTransportKernel,
        apply_transport=apply_transport,
        lower_transport=lower_transport,
    )


def build_runtime_kernels(state_size: int = 32) -> SPFKernelBundle:
    spf = import_spf_modules()
    policy = spf.SPFExecutionPolicy.strict()
    identity = spf.SPFBlockMatrix.identity(
        state_size,
        out_axis="pan_state_out",
        in_axis="pan_state_in",
    )
    policy.validate_kernel(identity, purpose="PAN state identity")

    selector = spf.SPFBlockMatrix.low_rank(
        np.ones((state_size, 1), dtype=np.complex128),
        np.ones((state_size, 1), dtype=np.complex128),
        proof=spf.SPFProof("pan_bootstrap_low_rank_selector", False, True, 0, 0),
    )
    policy.validate_kernel(selector, purpose="PAN bootstrap selector")

    measure = spf.SPFMeasureSpec("counting", ("pan_state_in",))
    gauge = spf.SPFGaugeSpec(("pan_state_in",), "none", measure)
    transport = spf.SPFTransportKernel(
        action=spf.SPFActionSpec("identity"),
        gauge=gauge,
        source_axes=(spf.AxisSpec("pan_state_in", state_size),),
        target_axes=(spf.AxisSpec("pan_state_out", state_size),),
        proof=spf.SPFProof("pan_state_transport", True, True, 0, 0),
        policy=policy,
    )
    audit = transport.audit(policy)
    audit.require_ok()
    lowering = spf.lower_transport(transport, policy=policy)
    manifest = {
        "schema_version": "pan-isa-x86-runtime-spf-manifest-v1",
        "dependency": "bob/repos/spf",
        "source_root": str(spf.source_root),
        "policy": policy.to_json_dict(),
        "state_size": int(state_size),
        "operators": {
            "identity": identity.cost(),
            "selector": selector.cost(),
            "transport": transport.cost(),
        },
        "transport_audit": audit.to_json_dict(),
        "transport_lowering": lowering.to_json_dict(),
        "uses_real_spfblockmatrix": identity.__class__.__name__ == "SPFBlockMatrix",
        "uses_real_spftransportkernel": transport.__class__.__name__ == "SPFTransportKernel",
    }
    return SPFKernelBundle(
        source_root=str(spf.source_root),
        policy=policy,
        identity=identity,
        selector=selector,
        transport=transport,
        lowering=lowering,
        manifest=manifest,
    )


def dependency_report() -> dict[str, Any]:
    try:
        bundle = build_runtime_kernels()
    except SPFBackendUnavailable as exc:
        return {"ok": False, "error": str(exc)}
    return {"ok": True, "manifest": bundle.manifest}
