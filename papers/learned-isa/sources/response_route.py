"""Finite raw-window routing observations for a frozen response program.

The route learner sees only 120 raw input bits and measured output-register
changes. It retains all matching copy/invert/constant candidates and abstains
when a route bit is not uniquely resolved on the discovery panel.
"""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from typing import Any

SCHEMA = "isa-response-route-program-v1"
REGISTER_COUNT = 8
REGISTER_WIDTH = 64
RAW_WINDOW_BYTES = 15
ROUTE_INDEX_WIDTH = 3


class ResponseRouteError(ValueError):
    """A response-route input or finite table has an invalid shape."""


def raw_bits(raw_window_hex: str) -> list[int]:
    """Expand a 15-byte input window to 120 least-significant-bit-first bits."""

    try:
        raw = bytes.fromhex(raw_window_hex)
    except (TypeError, ValueError) as exc:
        raise ResponseRouteError("raw window must be hexadecimal") from exc
    if len(raw) != RAW_WINDOW_BYTES:
        raise ResponseRouteError("raw window must contain exactly fifteen bytes")
    return [(byte >> bit) & 1 for byte in raw for bit in range(8)]


def _words(values: Sequence[int], field: str) -> list[int]:
    result = [int(value) for value in values]
    if len(result) != REGISTER_COUNT or any(value < 0 or value >= 1 << REGISTER_WIDTH for value in result):
        raise ResponseRouteError(f"{field} must contain eight unsigned 64-bit words")
    return result


def infer_consumer(observation: Mapping[str, Any]) -> dict[str, Any]:
    """Infer a row's candidate destination from changed words; retain head evidence."""

    before = _words(observation["register_words_before"], "register_words_before")
    after = _words(observation["register_words_after"], "register_words_after")
    changed_counts = [(left ^ right).bit_count() for left, right in zip(before, after, strict=True)]
    maximum = max(changed_counts)
    winners = [index for index, count in enumerate(changed_counts) if count == maximum]
    selected = winners[0] if maximum > 0 and len(winners) == 1 else None

    logits = observation.get("dest_logits")
    head_index = None
    if isinstance(logits, Sequence) and not isinstance(logits, (str, bytes)) and len(logits) == REGISTER_COUNT:
        numeric_logits = [float(value) for value in logits]
        if all(math.isfinite(value) for value in numeric_logits):
            head_index = max(range(REGISTER_COUNT), key=numeric_logits.__getitem__)
    return {
        "selected_register": selected,
        "selection_status": "unique-changed-output-winner" if selected is not None else "ambiguous-or-unchanged",
        "changed_bit_counts_by_register": changed_counts,
        "changed_winner_slots": winners if maximum else [],
        "destination_head_argmax": head_index,
        "destination_head_agrees": selected == head_index if selected is not None and head_index is not None else None,
        "input_words": before,
        "native_words": after,
        "nonconsumer_words_exact": ({index: before[index] == after[index]
                                      for index in range(REGISTER_COUNT) if index != selected}
                                     if selected is not None else {}),
    }


def infer_route_bit_rules(observations: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    """Fit the three route-index bits against every raw input bit.

    Matching bit positions, polarity, evidence count, and alternatives remain
    explicit. A rule is selected only if exactly one candidate matches all
    complete discovery rows.
    """

    if not observations:
        raise ResponseRouteError("at least one discovery observation is required")
    windows = [raw_bits(str(row["raw_window_hex"])) for row in observations]
    selected = [row.get("consumer", {}).get("selected_register") for row in observations]
    complete = all(isinstance(value, int) and 0 <= value < REGISTER_COUNT for value in selected)
    rules = []
    for output_bit in range(ROUTE_INDEX_WIDTH):
        target = [((int(value) >> output_bit) & 1) if isinstance(value, int) else None
                  for value in selected]
        candidates = []
        if complete:
            for input_position in range(RAW_WINDOW_BYTES * 8):
                feature = [window[input_position] for window in windows]
                if feature == target:
                    candidates.append({"kind": "copy", "input_bit_position": input_position,
                                       "byte_index": input_position // 8,
                                       "bit_index_lsb_first": input_position % 8})
                if [1 - value for value in feature] == target:
                    candidates.append({"kind": "invert", "input_bit_position": input_position,
                                       "byte_index": input_position // 8,
                                       "bit_index_lsb_first": input_position % 8})
            if target and all(value == target[0] for value in target):
                candidates.append({"kind": "constant", "value": target[0]})
        rules.append({
            "output_bit_lsb_first": output_bit,
            "evidence_count": sum(value is not None for value in target),
            "observed_output_bits": target,
            "candidate_rules": candidates,
            "selected_rule": candidates[0] if len(candidates) == 1 else None,
            "status": ("uniquely-identified-on-discovery" if len(candidates) == 1
                       else "ambiguous" if candidates else "unresolved"),
            "feature_search_domain": "all 120 raw window bits",
        })
    return rules


def infer_nonconsumer_copy(observations: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """Record whether all seven unselected words copied on every discovery row."""

    checked = 0
    mismatches = []
    for row in observations:
        consumer = row.get("consumer", {})
        selected = consumer.get("selected_register")
        if not isinstance(selected, int) or not 0 <= selected < REGISTER_COUNT:
            continue
        before = _words(row["register_words_before"], "register_words_before")
        after = _words(row["register_words_after"], "register_words_after")
        for register in range(REGISTER_COUNT):
            if register == selected:
                continue
            checked += 1
            if before[register] != after[register]:
                mismatches.append({"query_id": row.get("query_id"), "register": register,
                                   "before": before[register], "after": after[register]})
    established = len(observations) > 0 and checked == len(observations) * (REGISTER_COUNT - 1) and not mismatches
    return {
        "status": "observed-copy-on-all-discovery-rows" if established else "not-established",
        "checked_unselected_words": checked,
        "expected_unselected_words": len(observations) * (REGISTER_COUNT - 1),
        "mismatch_count": len(mismatches),
        "mismatches": mismatches,
        "application": "copy the seven unselected input words" if established else None,
    }


def build_route_program(discovery: Sequence[Mapping[str, Any]], frozen_response_program: Mapping[str, Any],
                        *, response_program_sha256: str) -> dict[str, Any]:
    """Combine the observed route table with the exact, separately frozen q-law."""

    if frozen_response_program.get("schema") != "isa-generated-response-program-v1":
        raise ResponseRouteError("frozen response program has an unexpected schema")
    if frozen_response_program.get("semantic_name") is not None:
        raise ResponseRouteError("frozen response program must retain its unassigned semantic name")
    if frozen_response_program.get("complete") is not True:
        raise ResponseRouteError("frozen response program is incomplete on its observed tables")
    observed_windows = list(dict.fromkeys(str(row["raw_window_hex"]).lower() for row in discovery))
    if len(observed_windows) != len(discovery):
        raise ResponseRouteError("discovery rows must contain distinct raw windows")
    # Validate the scope bytes now so the serving path can compare canonical hex.
    for window in observed_windows:
        raw_bits(window)
    consumers = [infer_consumer(row) for row in discovery]
    enriched = [{**row, "consumer": consumer} for row, consumer in zip(discovery, consumers, strict=True)]
    return {
        "schema": SCHEMA,
        "discovery_rows": len(discovery),
        "observed_raw_window_hexes": observed_windows,
        "raw_window_width_bits": RAW_WINDOW_BYTES * 8,
        "route_index_width_bits": ROUTE_INDEX_WIDTH,
        "route_bit_rules": infer_route_bit_rules(enriched),
        "native_consumer_observations": [
            {"query_id": row.get("query_id"), **consumer} for row, consumer in zip(discovery, consumers, strict=True)
        ],
        "nonconsumer_copy_rule": infer_nonconsumer_copy(enriched),
        "target_word_program": dict(frozen_response_program),
        "target_word_program_sha256": response_program_sha256,
        "route_scope": "only the exact discovery raw windows; route candidates were searched over all 120 raw input bits",
        "semantic_name": None,
    }


def _apply_rule(rule: Mapping[str, Any], bits: Sequence[int]) -> int | None:
    selected = rule.get("selected_rule")
    if not isinstance(selected, Mapping):
        return None
    kind = selected.get("kind")
    if kind == "constant":
        return int(selected["value"])
    position = selected.get("input_bit_position")
    if not isinstance(position, int) or not 0 <= position < len(bits):
        return None
    value = int(bits[position])
    return value if kind == "copy" else 1 - value if kind == "invert" else None


def serve_response(route_program: Mapping[str, Any], raw_window_hex: str,
                   register_words_before: Sequence[int]) -> dict[str, Any]:
    """Serve from raw window, the before-register bank, and the frozen q-law only."""

    bits = raw_bits(raw_window_hex)
    bank = _words(register_words_before, "register_words_before")
    if route_program.get("schema") != SCHEMA:
        raise ResponseRouteError("response route program schema mismatch")
    observed_windows = route_program.get("observed_raw_window_hexes")
    canonical_window = bytes.fromhex(raw_window_hex).hex()
    if (not isinstance(observed_windows, list)
            or canonical_window not in {str(window).lower() for window in observed_windows}):
        return {
            "status": "outside-observed-raw-window-scope",
            "route_index": None,
            "route_bits_lsb_first": [None] * ROUTE_INDEX_WIDTH,
            "target_word_prediction": None,
            "register_words_prediction": [None] * REGISTER_COUNT,
            "nonconsumer_words_prediction_available": False,
        }
    route_bits = [_apply_rule(rule, bits) for rule in route_program.get("route_bit_rules", [])]
    route = None
    status = "route-unavailable"
    if len(route_bits) == ROUTE_INDEX_WIDTH and all(value in (0, 1) for value in route_bits):
        route = sum(int(value) << index for index, value in enumerate(route_bits))
        status = "routed"
    if route is None:
        return {"status": status, "route_index": None, "route_bits_lsb_first": route_bits,
                "target_word_prediction": None, "register_words_prediction": [None] * REGISTER_COUNT}

    from isa_lab.response_quotient import serve_word

    program = route_program["target_word_program"]
    target_result = serve_word(program, bank[route])
    prediction: list[int | None] = [None] * REGISTER_COUNT
    nonconsumer = route_program.get("nonconsumer_copy_rule", {})
    if nonconsumer.get("status") == "observed-copy-on-all-discovery-rows":
        prediction = list(bank)
    if target_result.get("status") == "predicted":
        prediction[route] = int(target_result["word"])
    return {
        "status": "predicted" if target_result.get("status") == "predicted" else target_result.get("status"),
        "route_index": route,
        "route_bits_lsb_first": route_bits,
        "selected_input_word": bank[route],
        "target_word_prediction": target_result,
        "register_words_prediction": prediction,
        "nonconsumer_words_prediction_available": nonconsumer.get("status") == "observed-copy-on-all-discovery-rows",
    }


__all__ = [
    "RAW_WINDOW_BYTES", "REGISTER_COUNT", "REGISTER_WIDTH", "ROUTE_INDEX_WIDTH", "SCHEMA",
    "ResponseRouteError", "build_route_program", "infer_consumer", "infer_nonconsumer_copy",
    "infer_route_bit_rules", "raw_bits", "serve_response",
]
