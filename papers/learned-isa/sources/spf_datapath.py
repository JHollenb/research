"""Lane A (D1): a per-bit ALU automaton induced from whole-register transitions, executed by SPF `monomial_scan`.

An ALU entry is a Mealy automaton over the bits of one operation:
  symbol_i = (a_i, b_i)                      operand bits at position i (4 symbols)
  state    in {0..n-1}                       carried between bit positions (n learned, smallest first)
  next     = T[symbol_i, state]              a transformation-monoid map (generate / kill / propagate for a carry)
  bit_i    = E[symbol_i, state_before_i]     the result bit, stored as a {0, π} phase in the map's diag plane
  start    = S[CF_in]                        start state, chosen by the incoming carry flag (ADC/SBB need it)
  direction LSB→MSB or MSB→LSB               learned
Execution: `MonomialTransitionTable(bijective=False)` scanned with `order="right"` gives, at every bit, the state reached
from each start state, by index gathers and SPF32 word multiplies only (no coherent addition, unit-circle words).
The result bit at i is the emission phase of the map taken at i, read at the state before i.

Learned from transitions (operand values in, result value and flags out): n, T, E, S, direction and the flag taps.
Never used as supervision: intermediate carries, any oracle ALU. Supplied in this lane and reported: operand fetch
(destination value, extended operand, operation width), write-back, the {0, π} bit readout, and the flag-tap
vocabulary (which datapath signals a flag may be a function of).
"""
from __future__ import annotations

import itertools
import json
from dataclasses import dataclass

import numpy as np

from isa_lab.dependencies import spf_modules

HALF_TURN = 32768
FLAGS = ("CF", "ZF", "SF", "OF")


def _spf():
    core, _, _ = spf_modules()
    import spf.tensor.monomial_scan as ms  # mounted by spf_modules()
    return core, ms


def bits(x, width):
    """(N,) uint64 → (N, width) uint8, LSB first."""
    x = np.asarray(x, dtype=np.uint64)
    return ((x[:, None] >> np.arange(width, dtype=np.uint64)[None, :]) & np.uint64(1)).astype(np.uint8)


def from_bits(b):
    b = np.asarray(b, dtype=np.uint64)
    return (b << np.arange(b.shape[-1], dtype=np.uint64)).sum(-1, dtype=np.uint64)


@dataclass(frozen=True)
class Table:
    """A canonical induced automaton (state gauge fixed: states numbered in order of first use from start(CF=0))."""

    n: int
    trans: tuple  # trans[s][q] -> q'   (s = 2*a_i + b_i)
    emit: tuple  # emit[s][q] -> bit
    start: tuple  # start[cf_in] -> q
    reverse: bool

    def key(self):
        return json.dumps([self.n, self.trans, self.emit, self.start, self.reverse])

    def describe(self):
        return {"states": self.n, "transitions": [list(r) for r in self.trans], "emissions": [list(r) for r in self.emit],
                "start_by_cf": list(self.start), "direction": "MSB->LSB" if self.reverse else "LSB->MSB"}


class SPFExecutor:
    """Run a Table on SPF planes. Returns result bits, the state before each bit and the final state."""

    def __init__(self, table: Table):
        self.table = table
        core, ms = _spf()
        self.core = core
        n = table.n
        perms = np.array(table.trans, dtype=np.int64).reshape(4, n)
        theta = (np.array(table.emit, dtype=np.int64).reshape(4, n) * HALF_TURN).astype(np.uint16)
        diags = core.pack_words(np.zeros((4, n), dtype=np.int16), theta)
        self.rom = ms.MonomialTransitionTable(perms, diags, unit_circle=True, bijective=False)
        self.counters = {"scans": 0, "word_multiplications": 0, "coherent_additions": 0}

    def run(self, a_bits, b_bits, cf_in):
        """a_bits, b_bits (N, w) uint8; cf_in (N,) → (result bits (N, w), state before bit (N, w), final state (N,))."""
        t = self.table
        sym = (2 * a_bits.astype(np.int64) + b_bits.astype(np.int64))
        order = sym[:, ::-1] if t.reverse else sym
        res = self.rom.scan(order, order="right", method="sequential")
        self.counters["scans"] += 1
        self.counters["word_multiplications"] += res.counters.word_multiplications
        self.counters["coherent_additions"] += res.counters.coherent_additions
        start = np.array(t.start, dtype=np.int64)[np.asarray(cf_in, dtype=np.int64)]  # (N,)
        perm = res.prefix.perm  # (N, w, n): state after step i from each start state
        after = np.take_along_axis(perm, start[:, None, None].repeat(perm.shape[1], 1), axis=-1)[..., 0]  # (N, w)
        before = np.concatenate([start[:, None], after[:, :-1]], axis=1)
        word = self.rom.diags[order, before]  # emission phase of the map taken at each bit
        out = (self.core.unpack_theta(word).astype(np.int64) // HALF_TURN).astype(np.uint8)
        if t.reverse:
            out, before = out[:, ::-1], before[:, ::-1]
        return out, before, after[:, -1]


# ---------------------------------------------------------------- induction


def _canonical(n, trans, emit, start, reverse):
    """Fix the state-relabeling gauge: number states by first appearance (start(0), start(1), then BFS over symbols).

    A one-state table has no carried state, so its scan direction is unobservable; it is recorded as LSB→MSB.
    """
    if n == 1:
        reverse = False
    order = []
    for q in list(start) + [trans[s][q] for q in range(n) for s in range(4)]:
        if q not in order:
            order.append(q)
    for q in range(n):
        if q not in order:
            order.append(q)
    relabel = {old: new for new, old in enumerate(order)}
    tr = [[0] * n for _ in range(4)]
    em = [[0] * n for _ in range(4)]
    for s in range(4):
        for q in range(n):
            tr[s][relabel[q]] = relabel[trans[s][q]]
            em[s][relabel[q]] = emit[s][q]
    return Table(n, tuple(tuple(r) for r in tr), tuple(tuple(r) for r in em), tuple(relabel[q] for q in start), reverse)


def induce(a, b, result, width, cf_in, max_states=2, max_rows=512):
    """Smallest automaton consistent with every transition, by exhaustive search over transition and start maps.

    Emission entries are read off the data (an entry never observed stays 0 and is reported as unidentified).
    Returns (Table | None, info) where info lists every consistent behaviourally-distinct candidate count.
    """
    a = np.asarray(a, dtype=np.uint64)[:max_rows]
    b = np.asarray(b, dtype=np.uint64)[:max_rows]
    r = np.asarray(result, dtype=np.uint64)[:max_rows]
    cf = np.asarray(cf_in, dtype=np.int64)[:max_rows]
    A, B, R = bits(a, width), bits(b, width), bits(r, width)
    sym_lsb = 2 * A.astype(np.int64) + B.astype(np.int64)
    info = {"rows": int(len(a)), "searched": {}}
    for n in range(1, max_states + 1):
        found = []
        trans_space = list(itertools.product(range(n), repeat=4 * n))
        start_space = list(itertools.product(range(n), repeat=2))
        T = np.array(trans_space, dtype=np.int64).reshape(-1, 4, n)  # (C, 4, n)
        for reverse in (False, True):
            sym = sym_lsb[:, ::-1] if reverse else sym_lsb
            bitsR = R[:, ::-1] if reverse else R
            C = T.shape[0]
            cidx = np.arange(C)[:, None]
            for st in start_space:
                q = np.broadcast_to(np.array(st, dtype=np.int64)[cf], (C, len(a))).copy()  # (C, N)
                pres = np.zeros(C * 4 * n * 2, dtype=np.int64)  # per candidate: (symbol, state, observed bit) seen?
                for i in range(width):
                    s = np.broadcast_to(sym[:, i], q.shape)
                    code = ((cidx * 4 + s) * n + q) * 2 + bitsR[:, i].astype(np.int64)[None, :]
                    pres += np.bincount(code.ravel(), minlength=pres.size)
                    q = T[cidx, s, q]
                pres = pres.reshape(C, 4, n, 2) > 0
                ok = ~(pres[..., 0] & pres[..., 1]).any((1, 2))  # one result bit per (symbol, state): a Mealy machine
                for c in np.flatnonzero(ok):
                    em = pres[c, :, :, 1].astype(int)
                    unk = int((~pres[c, :, :, 0] & ~pres[c, :, :, 1]).sum())
                    found.append((_canonical(n, T[c].tolist(), em.tolist(), st, reverse), unk))
        info["searched"][n] = int(T.shape[0]) * len(start_space) * 2
        if found:
            uniq = {}
            for tab, unk in found:
                uniq.setdefault(tab.key(), (tab, unk))
            # Behaviourally distinct on this data's symbols? Report all; choose fewest unidentified entries, then key order.
            ranked = sorted(uniq.values(), key=lambda x: (x[1], x[0].key()))
            info.update(states=n, consistent=len(uniq), unidentified_entries=ranked[0][1])
            return ranked[0][0], info
    info.update(states=None, consistent=0)
    return None, info


# ---------------------------------------------------------------- flag taps


def tap_signals(a_bits, b_bits, out, before, final, width):
    """The supplied vocabulary of datapath signals a flag may depend on."""
    top = width - 1
    return {"r_top": out[:, top].astype(np.int64), "a_top": a_bits[:, top].astype(np.int64), "b_top": b_bits[:, top].astype(np.int64),
            "q_top": before[:, top].astype(np.int64), "q_final": final.astype(np.int64),
            "or_result": out.max(1).astype(np.int64), "xor_result": (out.sum(1) & 1).astype(np.int64)}


TAP_ORDER = (  # simplest first (MDL): constants and copies, one-signal functions, then two- and three-signal tables
    ("preserve",), ("const", 0), ("const", 1),
    ("fn", ("or_result",)), ("fn", ("r_top",)), ("fn", ("q_final",)), ("fn", ("xor_result",)),
    ("fn", ("q_top", "q_final")), ("fn", ("a_top", "b_top", "r_top")),
)


def _apply_tap(tap, sig, old):
    if tap[0] == "preserve":
        return old
    if tap[0] == "const":
        return np.full_like(old, tap[1])
    names, table = tap[1], tap[2]
    idx = np.zeros_like(old)
    for nm in names:
        idx = idx * 4 + sig[nm]  # states ≤ 3 → base 4 keeps every combination distinct
    return np.array(table, dtype=np.int64)[idx]


def induce_tap(sig, old, target):
    """First tap in TAP_ORDER consistent with every row; function tables are read off the data."""
    for spec in TAP_ORDER:
        if spec[0] != "fn":
            pred = _apply_tap(spec, sig, old)
            if np.array_equal(pred, target):
                return spec
            continue
        names = spec[1]
        idx = np.zeros_like(old)
        for nm in names:
            idx = idx * 4 + sig[nm]
        size = 4 ** len(names)
        table = np.full(size, -1, dtype=np.int64)
        good = True
        for v in np.unique(idx):
            vals = np.unique(target[idx == v])
            if len(vals) > 1:
                good = False
                break
            table[v] = vals[0]
        if good:
            return ("fn", names, tuple(int(x) if x >= 0 else 0 for x in table))
    return None


def flag_values(taps, sig, old_flags):
    """taps: dict flag -> tap; old_flags (N, 4) → (N, 4)."""
    return np.stack([_apply_tap(taps[f], sig, old_flags[:, k].astype(np.int64)) for k, f in enumerate(FLAGS)], 1)


def tap_json(tap):
    return list(tap) if tap[0] != "fn" else ["fn", list(tap[1]), list(tap[2])]


def tap_from_json(t):
    return tuple(t) if t[0] != "fn" else ("fn", tuple(t[1]), tuple(t[2]))
