"""Independent expected observables using Python integers and library sorting.

Does not compile or run C, load models, read native stdout, or use oracle state.
The fixed data and small update recipe are the workload specification.
"""
from __future__ import annotations

import hashlib
import json
import struct

MASK = (1 << 64) - 1
OFFSET = 1469598103934665603
PRIME = 1099511628211
SORT_INPUT = (
    93, 7, 4294967295, 41, 0, 18, 73, 7,
    2048, 511, 31, 99, 2, 65535, 1009, 17,
    8, 1, 4096, 63, 127, 255, 1023, 3,
    8191, 5, 29, 11, 47, 23, 89, 13,
)
NAMES = ("amber", "birch", "cedar", "delta", "elm", "fir", "granite", "hazelnut")


def record_input() -> bytes:
    return "".join(
        f"{NAMES[(i * 3 + 1) % 8]},{(i * 7) % 23 + 1},{(i * 137) % 2000 + 50}\n"
        for i in range(80)
    ).encode("ascii")


def fold(values: list[int]) -> int:
    value = OFFSET
    for item in values:
        value = ((value ^ item) * PRIME) & MASK
    return value


def small_reference() -> dict:
    cells = dict(a=0x123456789ABCDEF0, b=0x0FEDCBA987654321,
                 c=0x3141592653589793, d=0x2718281828459045)
    # Interpret a mathematical update recipe, with explicit modulo 2**64.
    recipe = (
        ("a", "+", "b"), ("c", "^", "d"), ("b", "+", "c"), ("d", "^", "a"),
        ("a", "*", 3), ("b", "^", "d"), ("c", "+", "a"), ("d", "*", 5),
        ("a", "^", "c"), ("b", "-", "a"), ("c", "*", 7), ("d", "+", "b"),
        ("a", "+", "d"), ("b", "*", 11), ("c", "^", "b"), ("d", "-", "c"),
        ("a", "*", 13), ("b", "+", "d"), ("c", "+", "a"), ("d", "^", "b"),
        ("a", "-", "c"), ("b", "^", "a"), ("c", "+", "d"), ("d", "*", 17),
    )
    for target, operation, operand in recipe:
        rhs = cells[operand] if isinstance(operand, str) else operand
        lhs = cells[target]
        cells[target] = {"+": lambda: lhs + rhs, "-": lambda: lhs - rhs,
                         "^": lambda: lhs ^ rhs, "*": lambda: lhs * rhs}[operation]() & MASK
    result = cells["a"] ^ cells["b"] ^ cells["c"] ^ cells["d"]
    return dict(result_u64=result, final_cells=cells, updates=len(recipe))


def medium_reference() -> dict:
    ordered = sorted(SORT_INPUT)
    return dict(result_u64=fold(ordered), sorted_values=ordered, elements=len(ordered))


def large_reference() -> dict:
    data = record_input()
    quantities, revenues, counts = [0] * 8, [0] * 8, [0] * 8
    for line in data.splitlines():
        name, quantity_text, price_text = line.split(b",")
        quantity, price = int(quantity_text), int(price_text)
        # Since 33 == 1 (mod 8), the C name recurrence reduces to sum(name) % 8.
        bucket = sum(name) % 8
        quantities[bucket] += quantity
        revenues[bucket] += quantity * price
        counts[bucket] += 1
    flattened = [value for bucket in range(8)
                 for value in (quantities[bucket], revenues[bucket], counts[bucket])]
    return dict(result_u64=fold(flattened), records=sum(counts), input_bytes=len(data),
                input_sha256=hashlib.sha256(data).hexdigest(), quantities=quantities,
                revenues=revenues, counts=counts)


def expected() -> dict:
    results = {"tiny": dict(stdout_hex=b"Hello, world!\n".hex(), exit_code=0),
               "small": small_reference(), "medium": medium_reference(),
               "large": large_reference()}
    for key in ("small", "medium", "large"):
        results[key]["stdout_hex"] = struct.pack("<Q", results[key]["result_u64"]).hex()
        results[key]["exit_code"] = 0
    return results


if __name__ == "__main__":
    print(json.dumps(expected(), indent=2, sort_keys=True))
