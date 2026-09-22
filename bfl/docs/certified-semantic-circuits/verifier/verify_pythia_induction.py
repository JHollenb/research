#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Reproduce two causal circuit certificates in public Pythia-70M weights.

This file is intentionally standalone.  It imports only open-source packages from
requirements.txt and downloads only the public EleutherAI/pythia-70m weights.

The two positive certificates are:

1. source_edge: layer-3 heads 1 and 6 route the token after the earlier match to
   the final query position;
2. qk_address: cue-identity features in those heads' query/key channels select
   that source.

The optional step-512 run is a developmental negative control, not an absence
claim about every possible circuit at that checkpoint.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
from collections.abc import Iterable, Iterator
from contextlib import ExitStack
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Literal

import huggingface_hub
import numpy as np
import safetensors
import torch
import transformers
from huggingface_hub import hf_hub_download
from transformers import AutoModelForCausalLM

MODEL_ID = "EleutherAI/pythia-70m"
MODEL_SPECS = {
    "step512": {
        "commit": "8c6e2534e332a9122404629fdb4bac11bf68689c",
        "weights_sha256": "a46bd4c254e28664926b12762616596de5783608ca5403765586c126bdf5bcd4",
    },
    "step1000": {
        "commit": "0fa739a8417c3c7d2a98ed3b283cacec67fd61df",
        "weights_sha256": "09883f904c4a50de85c682cdfa0434aaf34e62392fe883e58410d12d39b1ee88",
    },
}
CONFIG_SHA256 = "002050231a9b1ec3ac77aa6b9b3bbdc4d923f4068a7dd33b8da72a9bd6ad9a43"

GENERATOR_SEED = 20260740
SPLIT_SEED = 20260741
RANDOM_CONTROL_SEED_BASE = 20260800
N_ITEMS = 640
PREFIX_LENGTH = 12
CLASSES = 48
BATCH_SIZE = 64
WRITER_LAYER = 3
CIRCUIT_HEADS = (1, 6)

# Filled from the canonical JSON serialization produced by build_workload().
EXPECTED_WORKLOAD_SHA256 = (
    "3cf98eced30ab10e7c9b6a8ffe0317e60fd72c89a27e95d51ee85fc775fb325d"
)

# Exact integer counts from the original fp32/CPU run.  These are a replication
# target, while the causal gates below are the architecture-independent verdict.
REFERENCE_COUNTS = {
    "source_edge": {
        "clean": 286,
        "noop": 286,
        "head_1_source_cut": 240,
        "head_6_source_cut": 104,
        "coalition_source_cut": 6,
        "matched_position_cut": 297,
        "correct_repair": 300,
        "wrong_repair": 9,
    },
    "qk_address": {
        "clean": 286,
        "q_semantic_delete": 35,
        "q_random_delete": 138,
        "q_correct_repair": 276,
        "q_wrong_repair": 24,
        "k_semantic_delete": 8,
        "k_random_delete": 8,
        "k_correct_repair": 241,
        "k_wrong_repair": 12,
        "k_match_control": 297,
    },
    "developmental_control": {
        "clean": 8,
        "coalition_source_cut": 8,
        "correct_repair": 9,
        "wrong_repair": 9,
    },
}


@dataclass(frozen=True)
class Item:
    tokens: tuple[int, ...]
    candidates: tuple[int, ...]
    label: int


@dataclass
class Batch:
    input_ids: torch.Tensor
    attention_mask: torch.Tensor
    last: torch.Tensor
    labels: torch.Tensor
    candidates: torch.Tensor
    item_indices: torch.Tensor


@dataclass
class Metrics:
    n: int
    correct: int
    accuracy: float
    mean_margin: float
    candidate_score_sha256: str
    target_source_attention_mass: float | None = None


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_sha256(value: Any) -> str:
    encoded = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def build_workload() -> tuple[list[Item], int, list[int], list[int], dict[str, Any]]:
    rng = np.random.default_rng(GENERATOR_SEED)
    alphabet = sorted(
        rng.choice(np.arange(1000, 20000), size=CLASSES, replace=False).tolist()
    )
    token_to_class = {token: index for index, token in enumerate(alphabet)}
    items: list[Item] = []
    for _ in range(N_ITEMS):
        prefix = rng.choice(alphabet, size=PREFIX_LENGTH, replace=False).tolist()
        cue_index = int(rng.integers(0, PREFIX_LENGTH - 1))
        tokens = prefix + prefix[: cue_index + 1]
        answer = prefix[cue_index + 1]
        items.append(
            Item(
                tokens=tuple(int(token) for token in tokens),
                candidates=tuple(alphabet),
                label=token_to_class[answer],
            )
        )

    order = torch.randperm(
        len(items), generator=torch.Generator().manual_seed(SPLIT_SEED)
    ).tolist()
    discovery = order[: N_ITEMS // 2]
    heldout = order[N_ITEMS // 2 :]
    manifest = {
        "schema": "open-pythia-circuit-workload.v1",
        "generator_seed": GENERATOR_SEED,
        "split_seed": SPLIT_SEED,
        "prefix_length": PREFIX_LENGTH,
        "alphabet": alphabet,
        "items": [
            {
                "tokens": list(item.tokens),
                "candidates": list(item.candidates),
                "label": item.label,
            }
            for item in items
        ],
        "discovery": discovery,
        "heldout": heldout,
    }
    return items, CLASSES, discovery, heldout, manifest


def positions(item: Item) -> tuple[int, int]:
    """Return (earlier cue position, answer/source position)."""

    match = len(item.tokens) - (PREFIX_LENGTH + 1)
    return match, match + 1


def iter_batches(
    items: list[Item],
    indices: Iterable[int],
    batch_size: int,
    device: torch.device,
) -> Iterator[Batch]:
    index_list = list(indices)
    for start in range(0, len(index_list), batch_size):
        selected = index_list[start : start + batch_size]
        chosen = [items[index] for index in selected]
        maximum = max(len(item.tokens) for item in chosen)
        ids = torch.zeros(len(chosen), maximum, dtype=torch.long)
        mask = torch.zeros_like(ids)
        labels = torch.tensor([item.label for item in chosen], dtype=torch.long)
        candidates = torch.tensor(
            [item.candidates for item in chosen], dtype=torch.long
        )
        for row, item in enumerate(chosen):
            length = len(item.tokens)
            ids[row, :length] = torch.tensor(item.tokens, dtype=torch.long)
            mask[row, :length] = 1
        yield Batch(
            input_ids=ids.to(device),
            attention_mask=mask.to(device),
            last=(mask.sum(1) - 1).to(device),
            labels=labels.to(device),
            candidates=candidates.to(device),
            item_indices=torch.tensor(selected, dtype=torch.long),
        )


def attention_module(model: Any) -> Any:
    return model.gpt_neox.layers[WRITER_LAYER].attention


def dense_module(model: Any) -> Any:
    return attention_module(model).dense


def qkv_module(model: Any) -> Any:
    return attention_module(model).query_key_value


def validate_architecture(model: Any) -> dict[str, Any]:
    observed = {
        "model_type": model.config.model_type,
        "layers": int(model.config.num_hidden_layers),
        "hidden_size": int(model.config.hidden_size),
        "heads": int(model.config.num_attention_heads),
        "vocab_size": int(model.config.vocab_size),
        "writer_layer": WRITER_LAYER,
        "head_width": int(model.config.hidden_size // model.config.num_attention_heads),
    }
    expected = {
        "model_type": "gpt_neox",
        "layers": 6,
        "hidden_size": 512,
        "heads": 8,
        "vocab_size": 50304,
        "writer_layer": 3,
        "head_width": 64,
    }
    if observed != expected:
        raise RuntimeError(
            f"architecture mismatch: expected {expected!r}, observed {observed!r}"
        )
    # Resolve the exact modules now, so a library layout change fails loudly.
    qkv = qkv_module(model)
    dense = dense_module(model)
    if tuple(qkv.weight.shape) != (1536, 512):
        raise RuntimeError(f"unexpected QKV weight shape: {tuple(qkv.weight.shape)}")
    if tuple(dense.weight.shape) != (512, 512):
        raise RuntimeError(
            f"unexpected dense weight shape: {tuple(dense.weight.shape)}"
        )
    return observed


def load_model(
    revision_name: str, device: torch.device, offline: bool
) -> tuple[Any, dict[str, Any]]:
    spec = MODEL_SPECS[revision_name]
    weights_path = hf_hub_download(
        MODEL_ID,
        "model.safetensors",
        revision=spec["commit"],
        local_files_only=offline,
    )
    config_path = hf_hub_download(
        MODEL_ID,
        "config.json",
        revision=spec["commit"],
        local_files_only=offline,
    )
    observed_weights_hash = sha256_file(weights_path)
    observed_config_hash = sha256_file(config_path)
    if observed_weights_hash != spec["weights_sha256"]:
        raise RuntimeError(
            f"weight hash mismatch for {revision_name}: {observed_weights_hash}"
        )
    if observed_config_hash != CONFIG_SHA256:
        raise RuntimeError(
            f"config hash mismatch for {revision_name}: {observed_config_hash}"
        )
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        revision=spec["commit"],
        local_files_only=offline,
        dtype=torch.float32,
        attn_implementation="eager",
        use_safetensors=True,
    ).to(device)
    model.eval()
    architecture = validate_architecture(model)
    return model, {
        "model_id": MODEL_ID,
        "revision_name": revision_name,
        "commit": spec["commit"],
        "weights_sha256": observed_weights_hash,
        "config_sha256": observed_config_hash,
        "architecture": architecture,
    }


def score_output(
    output: Any, batch: Batch
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    row = torch.arange(len(batch.input_ids), device=batch.input_ids.device)
    scores = output.logits[row, batch.last].gather(1, batch.candidates)
    chosen = scores.gather(1, batch.labels[:, None]).squeeze(1)
    alternatives = scores.clone()
    alternatives[row, batch.labels] = -torch.inf
    margin = chosen - alternatives.max(1).values
    correct = scores.argmax(1) == batch.labels
    return scores, correct, margin


def finalize_metrics(
    scores: list[torch.Tensor],
    correct: list[torch.Tensor],
    margins: list[torch.Tensor],
    attention_mass: float | None = None,
) -> Metrics:
    score_tensor = torch.cat(scores).contiguous()
    correct_tensor = torch.cat(correct)
    margin_tensor = torch.cat(margins)
    score_bytes = score_tensor.numpy().tobytes(order="C")
    return Metrics(
        n=int(correct_tensor.numel()),
        correct=int(correct_tensor.sum()),
        accuracy=float(correct_tensor.float().mean()),
        mean_margin=float(margin_tensor.float().mean()),
        candidate_score_sha256=hashlib.sha256(score_bytes).hexdigest(),
        target_source_attention_mass=attention_mass,
    )


def capture_dense_inputs(
    model: Any,
    items: list[Item],
    indices: list[int],
    batch_size: int,
    device: torch.device,
) -> tuple[torch.Tensor, torch.Tensor]:
    captured: list[torch.Tensor] = []
    labels: list[torch.Tensor] = []
    context: dict[str, torch.Tensor] = {}

    def pre_hook(_module: Any, inputs: tuple[Any, ...]) -> None:
        tensor = inputs[0]
        captured.append(tensor[context["row"], context["last"]].detach().float().cpu())

    handle = dense_module(model).register_forward_pre_hook(pre_hook)
    try:
        with torch.inference_mode():
            for batch in iter_batches(items, indices, batch_size, device):
                context["row"] = torch.arange(len(batch.input_ids), device=device)
                context["last"] = batch.last
                model(
                    input_ids=batch.input_ids,
                    attention_mask=batch.attention_mask,
                    use_cache=False,
                )
                labels.append(batch.labels.cpu())
    finally:
        handle.remove()
    return torch.cat(captured), torch.cat(labels)


def head_class_means(
    dense_inputs: torch.Tensor,
    labels: torch.Tensor,
    head: int,
    heads: int,
    classes: int,
) -> torch.Tensor:
    width = dense_inputs.shape[1] // heads
    values = dense_inputs[:, head * width : (head + 1) * width].float()
    means = torch.zeros(classes, width)
    for label in range(classes):
        selected = labels == label
        if selected.any():
            means[label] = values[selected].mean(0)
    return means


SourceBlock = Literal["source", "match"]
SourceRepair = Literal["correct", "wrong"]


def evaluate_source_edge(
    model: Any,
    items: list[Item],
    indices: list[int],
    batch_size: int,
    device: torch.device,
    heads_selected: tuple[int, ...] = (),
    block: SourceBlock | None = None,
    repair: SourceRepair | None = None,
    means_by_head: dict[int, torch.Tensor] | None = None,
    noop_clone: bool = False,
) -> Metrics:
    all_scores: list[torch.Tensor] = []
    all_correct: list[torch.Tensor] = []
    all_margins: list[torch.Tensor] = []
    total_heads = int(model.config.num_attention_heads)
    head_width = int(model.config.hidden_size // total_heads)

    for batch in iter_batches(items, indices, batch_size, device):
        with ExitStack() as stack:
            if block is not None:

                def attention_pre_hook(
                    _module: Any,
                    hook_args: tuple[Any, ...],
                    hook_kwargs: dict[str, Any],
                    _batch: Batch = batch,
                ) -> tuple[tuple[Any, ...], dict[str, Any]]:
                    attention_mask = hook_kwargs.get("attention_mask")
                    if attention_mask is None or attention_mask.ndim != 4:
                        raise RuntimeError(
                            "expected eager GPT-NeoX to supply a four-dimensional attention mask"
                        )
                    expanded = attention_mask.expand(
                        len(_batch.input_ids),
                        total_heads,
                        len(_batch.input_ids[0]),
                        len(_batch.input_ids[0]),
                    ).clone()
                    minimum = torch.finfo(expanded.dtype).min
                    for row, item_index in enumerate(_batch.item_indices.tolist()):
                        match, source = positions(items[item_index])
                        blocked_position = source if block == "source" else match
                        query = int(_batch.last[row])
                        for head in heads_selected:
                            expanded[row, head, query, blocked_position] = minimum
                    hook_kwargs["attention_mask"] = expanded
                    return hook_args, hook_kwargs

                handle = attention_module(model).register_forward_pre_hook(
                    attention_pre_hook, with_kwargs=True
                )
                stack.callback(handle.remove)

            if repair is not None or noop_clone:

                def dense_pre_hook(
                    _module: Any,
                    inputs: tuple[Any, ...],
                    _batch: Batch = batch,
                ) -> tuple[Any, ...]:
                    changed = inputs[0].clone()
                    if repair is None:
                        return (changed, *inputs[1:])
                    if means_by_head is None:
                        raise RuntimeError("repair requested without discovery means")
                    row = torch.arange(len(_batch.input_ids), device=device)
                    selected = changed[row, _batch.last].float()
                    targets = (
                        _batch.labels
                        if repair == "correct"
                        else (_batch.labels + 1) % CLASSES
                    )
                    for head in heads_selected:
                        section = slice(head * head_width, (head + 1) * head_width)
                        selected[:, section] = means_by_head[head][targets.cpu()].to(
                            selected
                        )
                    changed[row, _batch.last] = selected.to(changed)
                    return (changed, *inputs[1:])

                handle = dense_module(model).register_forward_pre_hook(dense_pre_hook)
                stack.callback(handle.remove)

            with torch.inference_mode():
                output = model(
                    input_ids=batch.input_ids,
                    attention_mask=batch.attention_mask,
                    use_cache=False,
                )
        scores, correct, margins = score_output(output, batch)
        all_scores.append(scores.detach().float().cpu())
        all_correct.append(correct.detach().cpu())
        all_margins.append(margins.detach().float().cpu())
    return finalize_metrics(all_scores, all_correct, all_margins)


def capture_qk_roles(
    model: Any,
    items: list[Item],
    indices: list[int],
    batch_size: int,
    device: torch.device,
) -> dict[str, torch.Tensor]:
    heads = int(model.config.num_attention_heads)
    width = int(model.config.hidden_size // heads)
    q_values: list[torch.Tensor] = []
    k_values: list[torch.Tensor] = []
    cue_labels: list[int] = []
    token_to_class = {token: index for index, token in enumerate(items[0].candidates)}
    context: dict[str, Any] = {}

    def hook(_module: Any, _inputs: tuple[Any, ...], output: torch.Tensor) -> None:
        shaped = (
            output.detach()
            .float()
            .view(output.shape[0], output.shape[1], heads, 3 * width)
        )
        q_rows: list[torch.Tensor] = []
        k_rows: list[torch.Tensor] = []
        for row, item_index in enumerate(context["indices"]):
            _match, source = positions(items[item_index])
            q_rows.append(shaped[row, int(context["last"][row]), :, :width])
            k_rows.append(shaped[row, source, :, width : 2 * width])
            cue_labels.append(token_to_class[items[item_index].tokens[-1]])
        q_values.append(torch.stack(q_rows).cpu())
        k_values.append(torch.stack(k_rows).cpu())

    handle = qkv_module(model).register_forward_hook(hook)
    try:
        with torch.inference_mode():
            for batch in iter_batches(items, indices, batch_size, device):
                context["indices"] = batch.item_indices.tolist()
                context["last"] = batch.last
                model(
                    input_ids=batch.input_ids,
                    attention_mask=batch.attention_mask,
                    use_cache=False,
                )
    finally:
        handle.remove()
    return {
        "q_query": torch.cat(q_values),
        "k_source": torch.cat(k_values),
        "cue_labels": torch.tensor(cue_labels, dtype=torch.long),
    }


def semantic_geometry(
    values: torch.Tensor, labels: torch.Tensor, classes: int
) -> dict[str, Any]:
    means = torch.zeros(classes, values.shape[-1])
    for label in range(classes):
        selected = labels == label
        if selected.any():
            means[label] = values[selected].mean(0)
    global_mean = values.mean(0)
    centered = means - global_mean
    _u, singular, vh = torch.linalg.svd(centered, full_matrices=False)
    tolerance = singular.max() * max(centered.shape) * torch.finfo(singular.dtype).eps
    rank = int((singular > tolerance).sum())
    return {
        "means": means,
        "global_mean": global_mean,
        "basis": vh[:rank].T.contiguous(),
        "rank": rank,
    }


def random_basis(width: int, rank: int, seed: int) -> torch.Tensor:
    generator = torch.Generator().manual_seed(seed)
    matrix = torch.randn(width, rank, generator=generator)
    return torch.linalg.qr(matrix, mode="reduced").Q


def nearest_mean_accuracy(
    values: torch.Tensor, labels: torch.Tensor, means: torch.Tensor
) -> float:
    centered_means = means - means.mean(0)
    centered_values = values - means.mean(0)
    scores = centered_values @ centered_means.T
    return float((scores.argmax(1) == labels).float().mean())


QKRole = Literal["q_query", "k_source", "k_match_control"]
QKMode = Literal["semantic_delete", "random_delete", "correct_repair", "wrong_repair"]


def evaluate_qk_address(
    model: Any,
    items: list[Item],
    indices: list[int],
    batch_size: int,
    device: torch.device,
    role: QKRole | None,
    mode: QKMode | None,
    geometries: dict[str, dict[int, dict[str, Any]]],
    random_geometries: dict[str, dict[int, torch.Tensor]],
) -> Metrics:
    total_heads = int(model.config.num_attention_heads)
    width = int(model.config.hidden_size // total_heads)
    token_to_class = {token: index for index, token in enumerate(items[0].candidates)}
    all_scores: list[torch.Tensor] = []
    all_correct: list[torch.Tensor] = []
    all_margins: list[torch.Tensor] = []
    source_mass = 0.0
    count = 0

    for batch in iter_batches(items, indices, batch_size, device):
        cue_labels = torch.tensor(
            [
                token_to_class[items[index].tokens[-1]]
                for index in batch.item_indices.tolist()
            ],
            dtype=torch.long,
        )
        handle = None
        if role is not None:

            def hook(
                _module: Any,
                _inputs: tuple[Any, ...],
                output: torch.Tensor,
                _batch: Batch = batch,
                _cues: torch.Tensor = cue_labels,
            ) -> torch.Tensor:
                changed = output.clone()
                shaped = changed.view(
                    len(_batch.input_ids), changed.shape[1], total_heads, 3 * width
                )
                for row, item_index in enumerate(_batch.item_indices.tolist()):
                    match, source = positions(items[item_index])
                    if role == "q_query":
                        position = int(_batch.last[row])
                        section = slice(0, width)
                        geometry_role = "q_query"
                    elif role == "k_source":
                        position = source
                        section = slice(width, 2 * width)
                        geometry_role = "k_source"
                    else:
                        position = match
                        section = slice(width, 2 * width)
                        geometry_role = "k_source"
                    for head in CIRCUIT_HEADS:
                        value = shaped[row, position, head, section].float()
                        geometry = geometries[geometry_role][head]
                        semantic_basis = geometry["basis"].to(value)
                        if mode == "random_delete":
                            active_basis = random_geometries[geometry_role][head].to(
                                value
                            )
                        else:
                            active_basis = semantic_basis
                        if mode in {"semantic_delete", "random_delete"}:
                            value = value - (value @ active_basis) @ active_basis.T
                        elif mode in {"correct_repair", "wrong_repair"}:
                            cue = int(_cues[row])
                            target = (
                                cue if mode == "correct_repair" else (cue + 1) % CLASSES
                            )
                            desired = geometry["means"][target].to(value)
                            value = (
                                value
                                + ((desired - value) @ semantic_basis)
                                @ semantic_basis.T
                            )
                        else:
                            raise ValueError(f"unsupported Q/K mode: {mode}")
                        shaped[row, position, head, section] = value.to(shaped)
                return changed

            handle = qkv_module(model).register_forward_hook(hook)
        try:
            with torch.inference_mode():
                output = model(
                    input_ids=batch.input_ids,
                    attention_mask=batch.attention_mask,
                    output_attentions=True,
                    use_cache=False,
                )
        finally:
            if handle is not None:
                handle.remove()

        scores, correct, margins = score_output(output, batch)
        attentions = output.attentions
        if attentions is None:
            raise RuntimeError("eager attention did not return attention weights")
        row_index = torch.arange(len(batch.input_ids), device=device)
        layer_attention = attentions[WRITER_LAYER][row_index, :, batch.last, :].float()
        for row, item_index in enumerate(batch.item_indices.tolist()):
            _match, source = positions(items[item_index])
            source_mass += float(
                layer_attention[row, list(CIRCUIT_HEADS), source].mean().cpu()
            )
        count += len(batch.input_ids)
        all_scores.append(scores.detach().float().cpu())
        all_correct.append(correct.detach().cpu())
        all_margins.append(margins.detach().float().cpu())

    return finalize_metrics(
        all_scores,
        all_correct,
        all_margins,
        attention_mass=source_mass / count,
    )


def metric_dict(metric: Metrics) -> dict[str, Any]:
    return asdict(metric)


def gate(name: str, passed: bool, detail: str) -> dict[str, Any]:
    return {"name": name, "passed": bool(passed), "detail": detail}


def run_source_edge_suite(
    model: Any,
    items: list[Item],
    discovery: list[int],
    heldout: list[int],
    batch_size: int,
    device: torch.device,
) -> dict[str, Any]:
    dense_inputs, labels = capture_dense_inputs(
        model, items, discovery, batch_size, device
    )
    means = {
        head: head_class_means(
            dense_inputs,
            labels,
            head,
            int(model.config.num_attention_heads),
            CLASSES,
        )
        for head in CIRCUIT_HEADS
    }
    conditions = {
        "clean": evaluate_source_edge(model, items, heldout, batch_size, device),
        "noop": evaluate_source_edge(
            model, items, heldout, batch_size, device, noop_clone=True
        ),
        "head_1_source_cut": evaluate_source_edge(
            model, items, heldout, batch_size, device, (1,), "source"
        ),
        "head_6_source_cut": evaluate_source_edge(
            model, items, heldout, batch_size, device, (6,), "source"
        ),
        "coalition_source_cut": evaluate_source_edge(
            model, items, heldout, batch_size, device, CIRCUIT_HEADS, "source"
        ),
        "matched_position_cut": evaluate_source_edge(
            model, items, heldout, batch_size, device, CIRCUIT_HEADS, "match"
        ),
        "correct_repair": evaluate_source_edge(
            model,
            items,
            heldout,
            batch_size,
            device,
            CIRCUIT_HEADS,
            "source",
            "correct",
            means,
        ),
        "wrong_repair": evaluate_source_edge(
            model,
            items,
            heldout,
            batch_size,
            device,
            CIRCUIT_HEADS,
            "source",
            "wrong",
            means,
        ),
    }
    n = conditions["clean"].n
    clean = conditions["clean"]
    noop = conditions["noop"]
    head_1 = conditions["head_1_source_cut"]
    head_6 = conditions["head_6_source_cut"]
    cut = conditions["coalition_source_cut"]
    matched = conditions["matched_position_cut"]
    repair = conditions["correct_repair"]
    wrong = conditions["wrong_repair"]
    gates = [
        gate("clean_capability", clean.accuracy >= 0.85, f"{clean.correct}/{n} >= 85%"),
        gate(
            "exact_noop",
            clean.candidate_score_sha256 == noop.candidate_score_sha256,
            "all heldout candidate logits are byte-identical",
        ),
        gate("coalition_necessity", cut.accuracy <= 0.05, f"{cut.correct}/{n} <= 5%"),
        gate(
            "position_specificity",
            matched.accuracy >= 0.85,
            f"matched earlier-cue cut remains {matched.correct}/{n} >= 85%",
        ),
        gate("correct_repair", repair.accuracy >= 0.85, f"{repair.correct}/{n} >= 85%"),
        gate("wrong_repair", wrong.accuracy <= 0.10, f"{wrong.correct}/{n} <= 10%"),
        gate(
            "repair_specificity",
            repair.accuracy - wrong.accuracy >= 0.75,
            f"correct-minus-wrong = {repair.accuracy - wrong.accuracy:.4f} >= 0.75",
        ),
        gate(
            "coalition_synergy",
            min(head_1.accuracy, head_6.accuracy) - cut.accuracy >= 0.25,
            "pair cut is at least 25 points worse than either individual cut",
        ),
    ]
    observed_counts = {name: value.correct for name, value in conditions.items()}
    return {
        "claim": (
            "On this heldout relational-induction workload, Pythia-70M step1000 "
            "causally uses the layer-3 H1+H6 final-query-to-earlier-source edges; "
            "the coalition is necessary, the neighboring position is not, and "
            "class-correct head-state repair is specifically sufficient."
        ),
        "conditions": {name: metric_dict(value) for name, value in conditions.items()},
        "gates": gates,
        "causal_certificate_passed": all(item["passed"] for item in gates),
        "observed_counts": observed_counts,
        "reference_counts": REFERENCE_COUNTS["source_edge"],
        "exact_reference_match": observed_counts == REFERENCE_COUNTS["source_edge"],
    }


def run_qk_address_suite(
    model: Any,
    items: list[Item],
    discovery: list[int],
    heldout: list[int],
    batch_size: int,
    device: torch.device,
) -> dict[str, Any]:
    discovery_capture = capture_qk_roles(model, items, discovery, batch_size, device)
    heldout_capture = capture_qk_roles(model, items, heldout, batch_size, device)
    geometries: dict[str, dict[int, dict[str, Any]]] = {
        "q_query": {},
        "k_source": {},
    }
    random_geometries: dict[str, dict[int, torch.Tensor]] = {
        "q_query": {},
        "k_source": {},
    }
    observational: list[dict[str, Any]] = []
    revision_ordinal = 1  # step512 is ordinal 0 in the frozen original panel.
    for role_index, role in enumerate(("q_query", "k_source")):
        for head in CIRCUIT_HEADS:
            geometry = semantic_geometry(
                discovery_capture[role][:, head],
                discovery_capture["cue_labels"],
                CLASSES,
            )
            geometries[role][head] = geometry
            random_geometries[role][head] = random_basis(
                int(model.config.hidden_size // model.config.num_attention_heads),
                int(geometry["rank"]),
                RANDOM_CONTROL_SEED_BASE
                + revision_ordinal * 100
                + head * 10
                + role_index,
            )
            observational.append(
                {
                    "role": role,
                    "head": head,
                    "cue_subspace_rank": int(geometry["rank"]),
                    "heldout_cue_decoding_accuracy": nearest_mean_accuracy(
                        heldout_capture[role][:, head],
                        heldout_capture["cue_labels"],
                        geometry["means"],
                    ),
                }
            )

    def evaluate(role: QKRole | None, mode: QKMode | None) -> Metrics:
        return evaluate_qk_address(
            model,
            items,
            heldout,
            batch_size,
            device,
            role,
            mode,
            geometries,
            random_geometries,
        )

    conditions = {
        "clean": evaluate(None, None),
        "q_semantic_delete": evaluate("q_query", "semantic_delete"),
        "q_random_delete": evaluate("q_query", "random_delete"),
        "q_correct_repair": evaluate("q_query", "correct_repair"),
        "q_wrong_repair": evaluate("q_query", "wrong_repair"),
        "k_semantic_delete": evaluate("k_source", "semantic_delete"),
        "k_random_delete": evaluate("k_source", "random_delete"),
        "k_correct_repair": evaluate("k_source", "correct_repair"),
        "k_wrong_repair": evaluate("k_source", "wrong_repair"),
        "k_match_control": evaluate("k_match_control", "semantic_delete"),
    }
    n = conditions["clean"].n
    clean = conditions["clean"]
    q_delete = conditions["q_semantic_delete"]
    q_correct = conditions["q_correct_repair"]
    q_wrong = conditions["q_wrong_repair"]
    k_delete = conditions["k_semantic_delete"]
    k_correct = conditions["k_correct_repair"]
    k_wrong = conditions["k_wrong_repair"]
    k_match = conditions["k_match_control"]
    gates = [
        gate("clean_capability", clean.accuracy >= 0.85, f"{clean.correct}/{n} >= 85%"),
        gate(
            "query_necessity",
            q_delete.accuracy <= 0.15,
            f"{q_delete.correct}/{n} <= 15%",
        ),
        gate(
            "query_correct_repair",
            q_correct.accuracy >= 0.80,
            f"{q_correct.correct}/{n} >= 80%",
        ),
        gate(
            "query_wrong_repair",
            q_wrong.accuracy <= 0.15,
            f"{q_wrong.correct}/{n} <= 15%",
        ),
        gate(
            "query_repair_specificity",
            q_correct.accuracy - q_wrong.accuracy >= 0.65,
            f"correct-minus-wrong = {q_correct.accuracy - q_wrong.accuracy:.4f} >= 0.65",
        ),
        gate(
            "source_key_necessity",
            k_delete.accuracy <= 0.05,
            f"{k_delete.correct}/{n} <= 5%",
        ),
        gate(
            "source_key_correct_repair",
            k_correct.accuracy >= 0.70,
            f"{k_correct.correct}/{n} >= 70%",
        ),
        gate(
            "source_key_wrong_repair",
            k_wrong.accuracy <= 0.10,
            f"{k_wrong.correct}/{n} <= 10%",
        ),
        gate(
            "key_position_specificity",
            k_match.accuracy >= 0.85,
            f"same key edit at earlier cue remains {k_match.correct}/{n} >= 85%",
        ),
        gate(
            "attention_selected",
            clean.target_source_attention_mass is not None
            and clean.target_source_attention_mass >= 0.85,
            f"clean source attention = {clean.target_source_attention_mass:.4f} >= 0.85",
        ),
        gate(
            "query_controls_attention",
            q_delete.target_source_attention_mass is not None
            and q_delete.target_source_attention_mass <= 0.15,
            f"after query deletion = {q_delete.target_source_attention_mass:.4f} <= 0.15",
        ),
        gate(
            "key_controls_attention",
            k_delete.target_source_attention_mass is not None
            and k_delete.target_source_attention_mass <= 0.01,
            f"after source-key deletion = {k_delete.target_source_attention_mass:.6f} <= 0.01",
        ),
    ]
    observed_counts = {name: value.correct for name, value in conditions.items()}
    return {
        "claim": (
            "On the same heldout workload, cue-identity geometry in the layer-3 "
            "H1+H6 query and earlier-source key channels causally selects the source: "
            "deletion removes source attention and behavior, correct repair restores "
            "them, wrong repair does not, and the same key edit at the neighboring "
            "earlier-cue position is harmless."
        ),
        "conditions": {name: metric_dict(value) for name, value in conditions.items()},
        "observational": observational,
        "gates": gates,
        "causal_certificate_passed": all(item["passed"] for item in gates),
        "observed_counts": observed_counts,
        "reference_counts": REFERENCE_COUNTS["qk_address"],
        "exact_reference_match": observed_counts == REFERENCE_COUNTS["qk_address"],
        "instrument_note": (
            "The semantic cue basis has high rank, so a matched-rank random deletion "
            "also removes much of each 64-dimensional head. Random deletion is retained "
            "as a diagnostic, not used as the semantic-specificity gate. Correct-versus-"
            "wrong repair and the matched-position intervention carry that claim."
        ),
    }


def run_developmental_control(
    model: Any,
    items: list[Item],
    discovery: list[int],
    heldout: list[int],
    batch_size: int,
    device: torch.device,
) -> dict[str, Any]:
    dense_inputs, labels = capture_dense_inputs(
        model, items, discovery, batch_size, device
    )
    means = {
        head: head_class_means(
            dense_inputs,
            labels,
            head,
            int(model.config.num_attention_heads),
            CLASSES,
        )
        for head in CIRCUIT_HEADS
    }
    conditions = {
        "clean": evaluate_source_edge(model, items, heldout, batch_size, device),
        "coalition_source_cut": evaluate_source_edge(
            model, items, heldout, batch_size, device, CIRCUIT_HEADS, "source"
        ),
        "correct_repair": evaluate_source_edge(
            model,
            items,
            heldout,
            batch_size,
            device,
            CIRCUIT_HEADS,
            "source",
            "correct",
            means,
        ),
        "wrong_repair": evaluate_source_edge(
            model,
            items,
            heldout,
            batch_size,
            device,
            CIRCUIT_HEADS,
            "source",
            "wrong",
            means,
        ),
    }
    clean = conditions["clean"]
    cut = conditions["coalition_source_cut"]
    correct = conditions["correct_repair"]
    wrong = conditions["wrong_repair"]
    gates = [
        gate("capability_off", clean.accuracy <= 0.10, f"clean = {clean.accuracy:.4f}"),
        gate(
            "cut_does_not_fake_effect",
            abs(clean.accuracy - cut.accuracy) <= 0.05,
            f"absolute clean-minus-cut = {abs(clean.accuracy - cut.accuracy):.4f}",
        ),
        gate(
            "repair_does_not_fake_specificity",
            abs(correct.accuracy - wrong.accuracy) <= 0.05,
            f"absolute correct-minus-wrong = {abs(correct.accuracy - wrong.accuracy):.4f}",
        ),
    ]
    observed_counts = {name: value.correct for name, value in conditions.items()}
    return {
        "claim_boundary": (
            "This is an affirmative negative control for the intervention machinery: "
            "at step512 the task is off and the same cut/repair panel does not create "
            "the positive signature. It does not prove that no other circuit exists."
        ),
        "conditions": {name: metric_dict(value) for name, value in conditions.items()},
        "gates": gates,
        "control_passed": all(item["passed"] for item in gates),
        "observed_counts": observed_counts,
        "reference_counts": REFERENCE_COUNTS["developmental_control"],
        "exact_reference_match": observed_counts
        == REFERENCE_COUNTS["developmental_control"],
    }


def print_suite(name: str, suite: dict[str, Any]) -> None:
    print(f"\n{name}")
    print("condition".ljust(28), "correct", "accuracy", "source-attn")
    for condition, metric in suite["conditions"].items():
        mass = metric.get("target_source_attention_mass")
        mass_text = "-" if mass is None else f"{mass:.6f}"
        print(
            condition.ljust(28),
            f"{metric['correct']:>3}/{metric['n']:<3}",
            f"{metric['accuracy']:.6f}",
            mass_text,
        )
    for item in suite["gates"]:
        print(
            f"  {'PASS' if item['passed'] else 'FAIL'} {item['name']}: {item['detail']}"
        )
    if "exact_reference_match" in suite:
        print(f"  exact reference counts: {suite['exact_reference_match']}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Certify public Pythia-70M induction circuits without Saturn."
    )
    parser.add_argument(
        "--suite",
        choices=("edge", "address", "all"),
        default="all",
        help="positive certificate(s) to execute on step1000",
    )
    parser.add_argument(
        "--developmental-control",
        action="store_true",
        help="also run the same source panel on the public step512 checkpoint",
    )
    parser.add_argument(
        "--device",
        choices=("auto", "cpu", "cuda", "mps"),
        default="cpu",
        help="CPU is the strict-reference authority; auto is useful for faster causal validation",
    )
    parser.add_argument("--batch-size", type=int, default=BATCH_SIZE)
    parser.add_argument("--threads", type=int, default=4)
    parser.add_argument(
        "--diagnostic-heldout",
        type=int,
        help="run only the first N heldout rows; mechanics only, never emits a certificate",
    )
    parser.add_argument(
        "--strict-reference",
        action="store_true",
        help="fail unless every integer count exactly matches the recorded CPU reference",
    )
    parser.add_argument(
        "--offline",
        action="store_true",
        help="use already cached Hugging Face files and make no network request",
    )
    parser.add_argument(
        "--output", type=Path, default=Path("pythia-circuit-certificate.json")
    )
    return parser.parse_args()


def resolve_device(name: str) -> torch.device:
    if name == "auto":
        if torch.cuda.is_available():
            return torch.device("cuda")
        if torch.backends.mps.is_available():
            return torch.device("mps")
        return torch.device("cpu")
    if name == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA requested but unavailable")
    if name == "mps" and not torch.backends.mps.is_available():
        raise RuntimeError("MPS requested but unavailable")
    return torch.device(name)


def main() -> None:
    args = parse_args()
    if args.batch_size <= 0:
        raise ValueError("--batch-size must be positive")
    if args.diagnostic_heldout is not None and args.diagnostic_heldout <= 0:
        raise ValueError("--diagnostic-heldout must be positive")
    torch.manual_seed(SPLIT_SEED)
    torch.set_num_threads(args.threads)
    torch.use_deterministic_algorithms(True)
    device = resolve_device(args.device)

    items, classes, discovery, heldout, workload_manifest = build_workload()
    workload_hash = canonical_sha256(workload_manifest)
    if workload_hash != EXPECTED_WORKLOAD_SHA256:
        raise RuntimeError(
            "workload hash mismatch; use the pinned NumPy/PyTorch versions from requirements.txt: "
            f"observed {workload_hash}"
        )
    diagnostic = args.diagnostic_heldout is not None
    if diagnostic:
        heldout = heldout[: args.diagnostic_heldout]
    print(f"workload sha256: {workload_hash}")
    print(f"device: {device}; discovery={len(discovery)}; heldout={len(heldout)}")

    model, step1000_provenance = load_model("step1000", device, args.offline)
    suites: dict[str, Any] = {}
    if args.suite in {"edge", "all"}:
        suites["source_edge"] = run_source_edge_suite(
            model, items, discovery, heldout, args.batch_size, device
        )
        print_suite("SOURCE EDGE", suites["source_edge"])
    if args.suite in {"address", "all"}:
        suites["qk_address"] = run_qk_address_suite(
            model, items, discovery, heldout, args.batch_size, device
        )
        print_suite("Q/K ADDRESS", suites["qk_address"])
    del model

    models = {"step1000": step1000_provenance}
    if args.developmental_control:
        control_model, step512_provenance = load_model("step512", device, args.offline)
        suites["developmental_control"] = run_developmental_control(
            control_model, items, discovery, heldout, args.batch_size, device
        )
        print_suite("STEP-512 DEVELOPMENTAL CONTROL", suites["developmental_control"])
        del control_model
        models["step512"] = step512_provenance

    positive_suites = [
        suite for name, suite in suites.items() if name in {"source_edge", "qk_address"}
    ]
    controls = [
        suite for name, suite in suites.items() if name == "developmental_control"
    ]
    causal_pass = all(suite["causal_certificate_passed"] for suite in positive_suites)
    controls_pass = all(suite["control_passed"] for suite in controls)
    exact_reference_match = all(
        suite["exact_reference_match"] for suite in suites.values()
    )
    certificate_passed = causal_pass and controls_pass and not diagnostic
    strict_passed = certificate_passed and (
        exact_reference_match if args.strict_reference else True
    )

    versions = {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "numpy": np.__version__,
        "torch": torch.__version__,
        "transformers": transformers.__version__,
        "huggingface_hub": huggingface_hub.__version__,
        "safetensors": safetensors.__version__,
    }

    body = {
        "schema": "open-pythia-circuit-certificate.v1",
        "status": "diagnostic"
        if diagnostic
        else ("certified" if strict_passed else "failed"),
        "claim_scope": (
            "Causal claims are bounded to the pinned Pythia-70M weights, the exact "
            "synthetic relational-induction distribution, restricted 48-token readout, "
            "layer-3 H1/H6 interventions, and the heldout panel. This is complete "
            "validation of that bounded claim, not proof of universality, uniqueness, "
            "or every computation performed by Pythia."
        ),
        "models": models,
        "workload": {
            "sha256": workload_hash,
            "classes": classes,
            "examples": N_ITEMS,
            "discovery": len(discovery),
            "heldout": len(heldout),
            "generator_seed": GENERATOR_SEED,
            "split_seed": SPLIT_SEED,
        },
        "execution": {
            "device": str(device),
            "batch_size": args.batch_size,
            "threads": args.threads,
            "diagnostic": diagnostic,
            "strict_reference_requested": args.strict_reference,
            "offline": args.offline,
            "script_sha256": sha256_file(Path(__file__).resolve()),
            "versions": versions,
        },
        "suites": suites,
        "causal_gates_passed": causal_pass,
        "controls_passed": controls_pass,
        "exact_reference_match": exact_reference_match,
        "certificate_passed": certificate_passed,
        "strict_verdict_passed": strict_passed,
    }
    report = {**body, "report_fingerprint": canonical_sha256(body)}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"\nreport: {args.output.resolve()}")
    print(f"report fingerprint: {report['report_fingerprint']}")
    if diagnostic:
        print("VERDICT: DIAGNOSTIC ONLY (heldout panel was truncated)")
        return
    if strict_passed:
        label = "STRICT REFERENCE PASS" if args.strict_reference else "CAUSAL PASS"
        print(f"VERDICT: {label}")
        return
    print("VERDICT: FAIL")
    raise SystemExit(1)


if __name__ == "__main__":
    main()
