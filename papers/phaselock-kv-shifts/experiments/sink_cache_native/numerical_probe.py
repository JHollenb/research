"""Isolate retained-key error over one full native SinkCache shift trajectory."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import tempfile
from pathlib import Path

import torch


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def rotate_half(value: torch.Tensor) -> torch.Tensor:
    half = value.shape[-1] // 2
    return torch.cat((-value[..., half:], value[..., :half]), dim=-1)


def run() -> None:
    workspace = Path(__file__).resolve().parents[5]
    source = workspace / "sink_cache" / "custom_generate" / "generate.py"
    baseline_bytes = subprocess.check_output(
        ["git", "-C", str(source.parents[1]), "show", "HEAD:custom_generate/generate.py"]
    )
    torch.manual_seed(7)
    window, sinks, head_dim, vectors = 1024, 4, 128, 64
    capacity = window + sinks
    frequencies = 1_000_000.0 ** (-torch.arange(0, head_dim, 2, dtype=torch.float32) / head_dim)
    angles = torch.arange(capacity, dtype=torch.float32)[:, None] * frequencies[None]
    cos = torch.cat((angles.cos(), angles.cos()), dim=-1).to(torch.bfloat16)
    sin = torch.cat((angles.sin(), angles.sin()), dim=-1).to(torch.bfloat16)
    raw = torch.randn(vectors, head_dim, dtype=torch.float32).to(torch.bfloat16)

    with tempfile.TemporaryDirectory(prefix="sink-cache-probe-") as temporary:
        old_source = Path(temporary) / "old.py"
        old_source.write_bytes(baseline_bytes)
        modules = {
            "upstream_bf16": load_module(old_source, "upstream_sink"),
            "patched_fp32_unit": load_module(source, "patched_sink"),
        }
        coefficients = {}
        for name, module in modules.items():
            cache = module.SinkCache(window_length=capacity, num_sink_tokens=sinks)
            coefficients[name] = cache._get_rerotation_cos_sin(
                torch.empty(1, 1, 1, head_dim, dtype=torch.bfloat16), cos, sin
            )
        # This ablation changes arithmetic precision without normalizing the
        # source table's derived coefficient, so it separates the two edits.
        coefficients["fp32_only"] = tuple(part.float() for part in coefficients["upstream_bf16"])

        outcomes = {}
        for source_position in (128, 512, capacity - 2):
            initial = (
                raw * cos[source_position] + rotate_half(raw) * sin[source_position]
            ).to(torch.bfloat16)
            target = (
                raw * cos[sinks] + rotate_half(raw) * sin[sinks]
            ).to(torch.bfloat16).float()
            rows = {}
            for name, (coefficient_cos, coefficient_sin) in coefficients.items():
                current = initial.clone()
                for position in range(source_position - 1, sinks - 1, -1):
                    index = position - sinks
                    c = coefficient_cos[0, index]
                    s = coefficient_sin[0, index]
                    if name == "upstream_bf16":
                        current = current * c + rotate_half(current) * s
                    else:
                        current32 = current.float()
                        current = (current32 * c + rotate_half(current32) * s).to(torch.bfloat16)
                current = current.float()
                rows[name] = {
                    "mean_relative_l2_error_to_direct": float(
                        ((current - target).norm(dim=-1) / target.norm(dim=-1)).mean()
                    ),
                    "mean_norm_ratio_to_direct": float(
                        (current.norm(dim=-1) / target.norm(dim=-1)).mean()
                    ),
                    "mean_cosine_to_direct": float(
                        torch.nn.functional.cosine_similarity(current, target, dim=-1).mean()
                    ),
                }
            outcomes[str(source_position)] = rows
    print(json.dumps({"capacity": capacity, "sinks": sinks, "vectors": vectors,
                      "transformers": __import__("transformers").__version__,
                      "outcomes": outcomes}, indent=2))


if __name__ == "__main__":
    run()
