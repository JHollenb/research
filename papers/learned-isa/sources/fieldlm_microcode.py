"""Lane B: learned microcode records in a FieldLM `FieldFabric`, executed through lane A's SPF datapath.

Induction (no gradient optimizer, no oracle ALU, no decode labels):
  1. Group training transitions by their instruction bytes, with a trailing immediate of s ∈ {8, 4, 1, 0} bytes
     (tried largest first; the immediate must be used by the effect, otherwise s is rejected).
  2. Fit one effect per group from transitions only: destination register, source (immediate with zero or sign
     extension / register / constant 1), operation width and merge class, write or not, the per-bit ALU table (reused
     from the table library or induced, `spf_datapath.induce`) and the four flag taps; or SYSCALL; or a store whose
     address and value are registers.
  3. Learn the operand-field mask and the code → register map: a 3-bit field inside an opcode byte becomes a field
     role when (a) one global code → register map explains it across groups and (b) masking it merges at least two
     groups with identical abstract effects (MDL: fewest records, every record consistent).
  4. Store one record per (shape, masked opcode bytes) in a FieldFabric view; serving reads it with a FabricProgram.
Supplied (reported): the role vocabulary of steps 1–2 (3-bit fields at bit 0 or 3 of an opcode byte; trailing
immediates of 0/1/4/8 bytes; width/merge classes 8 preserve, 32 zero-extend, 64 replace; store to [register];
SYSCALL), lane A's automaton shape and flag-tap vocabulary, the lookup tie-break (most specific key), the bit/byte
layout, fetch at the emitted RIP and the OS boundary. Learned: everything else listed above.
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict

import numpy as np
import torch

from isa_lab.dependencies import field_modules

from . import spf_datapath as D

MASK = {8: 0xFF, 32: 0xFFFFFFFF, 64: (1 << 64) - 1}
IMM_SIZES = (8, 4, 1, 0)
FIELD_SHIFTS = (0, 3)


def u64(x):
    return np.asarray(x).view(np.uint64) if np.asarray(x).dtype == np.int64 else np.asarray(x, dtype=np.uint64)


def imm_value(window, length, s, ext):
    """Little-endian immediate of s bytes ending at `length`, zero- or sign-extended to 64 bits. window (N, 15)."""
    if s == 0:
        return np.zeros(len(window), dtype=np.uint64)
    v = np.zeros(len(window), dtype=np.uint64)
    for k in range(s):
        v |= window[np.arange(len(window)), length - s + k].astype(np.uint64) << np.uint64(8 * k)
    if ext == "sign" and s < 8:
        top = (v >> np.uint64(8 * s - 1)) & np.uint64(1)
        v = np.where(top == 1, v | (np.uint64(MASK[64]) ^ np.uint64((1 << (8 * s)) - 1)), v)
    return v


class Library:
    """Shared per-bit ALU tables (lane A), keyed by canonical form; executors cached."""

    def __init__(self):
        self.tables, self.execs, self.induced = [], [], []

    def add(self, tab, info):
        for i, t in enumerate(self.tables):
            if t.key() == tab.key():
                return i
        self.tables.append(tab)
        self.execs.append(D.SPFExecutor(tab))
        self.induced.append(info)
        return len(self.tables) - 1

    def run(self, i, a, b, cf, w):
        A, B = D.bits(a, w), D.bits(b, w)
        out, before, final = self.execs[i].run(A, B, cf)
        return D.from_bits(out), D.tap_signals(A, B, out, before, final, w)


def _taps(sig, fl, fl_after):
    taps = {}
    for k, f in enumerate(D.FLAGS):
        t = D.induce_tap(sig, fl[:, k].astype(np.int64), fl_after[:, k].astype(np.int64))
        if t is None:
            return None
        taps[f] = D.tap_json(t)
    return taps


def _fit_alu(lib, g, d_rows, srcs, w, write, induce, induce_rows):
    """Try one (width, write) hypothesis with a per-row destination over the source candidates.

    induce=False: reuse a library table only. induce=True: induce a new table (kept only if the whole hypothesis fits).
    """
    m = np.uint64(MASK[w])
    ar = np.arange(len(d_rows))
    a = g["before"][ar, d_rows] & m
    target = g["after"][ar, d_rows] & m
    fl, fla = g["flags"], g["after_flags"]
    cf = fl[:, 0].astype(np.int64)
    for src_name, b_full in srcs:
        b = b_full & m
        if not induce:
            for ti in range(len(lib.tables)):
                res, sig = lib.run(ti, a, b, cf, w)
                if write and not np.array_equal(res, target):
                    continue
                taps = _taps(sig, fl, fla)
                if taps is not None:
                    return {"src": src_name, "table": ti, "taps": taps}
            continue
        if not write:
            continue  # result bits unobserved: only a library table may be reused (the flags decide)
        tab, info = D.induce(a, b, target, w, cf, max_rows=induce_rows)
        if tab is None:
            continue
        ex = D.SPFExecutor(tab)
        A, B = D.bits(a, w), D.bits(b, w)
        out, bef, fin = ex.run(A, B, cf)
        if not np.array_equal(D.from_bits(out), target):
            continue  # induced on the first rows, wrong on the rest
        taps = _taps(D.tap_signals(A, B, out, bef, fin, w), fl, fla)
        if taps is not None:
            ti = lib.add(tab, {**info, "from_rows": int(min(len(a), induce_rows))})
            return {"src": src_name, "table": ti, "taps": taps}
    return None


def fit_alu_rows(lib, g, d_rows, srcs_for, induce_rows):
    """Width, write, table and taps for a fixed per-row destination; srcs_for(d_rows) gives the source candidates."""
    before, after = g["before"], g["after"]
    ar = np.arange(len(d_rows))
    diff = before != after
    dchanged = diff[ar, d_rows]
    diff[ar, d_rows] = False
    if diff.any():
        return None  # some other register changed
    srcs = srcs_for(d_rows)
    for induce in (False, True):  # MDL: reuse a library table anywhere before inducing a new one
        for write in (True, False):
            if not write and dchanged.any():
                break
            for w in (64, 32, 8):
                if write:
                    old, new = before[ar, d_rows], after[ar, d_rows]
                    if w == 8 and not ((old >> np.uint64(8)) == (new >> np.uint64(8))).all():
                        continue
                    if w == 32 and not ((new >> np.uint64(32)) == 0).all():
                        continue
                r = _fit_alu(lib, g, d_rows, srcs, w, write, induce, induce_rows)
                if r is not None:
                    return {"width": w, "write": write, **r}
    return None


def fit_group(lib, g, induce_rows=256):
    """One effect explaining every transition of a group (fixed bytes, fixed immediate size)."""
    s, length = g["s"], g["length"]
    before, after, fl, fla = g["before"], g["after"], g["flags"], g["after_flags"]
    n = len(before)
    if g["syscall"].all():
        if (before == after).all() and (fl == fla).all():
            return {"kind": "syscall"}
        return None
    if g["syscall"].any():
        return None
    if g["store"].all():
        if s or not ((before == after).all() and (fl == fla).all()):
            return None
        addr = [r for r in range(8) if (before[:, r] == g["store_addr"]).all()]
        val = [r for r in range(8) if (before[:, r] == g["store_value"]).all()]
        if addr and val:
            return {"kind": "store", "addr": {"reg": addr[0]}, "value": {"reg": val[0]}}
        return None
    if g["store"].any():
        return None
    changed = [r for r in range(8) if (before[:, r] != after[:, r]).any()]
    if len(changed) > 1:
        return None
    for d in (changed if changed else list(range(8))):
        d_rows = np.full(n, d)
        if s:
            srcs_for = lambda dr: [({"imm": s, "ext": e}, imm_value(g["window"], np.full(n, length), s, e))  # noqa: E731
                                   for e in ("zero", "sign")]
        else:  # the destination itself first (r, r forms), then every register, then the constant 1
            srcs_for = lambda dr, d=d: [({"reg": r}, before[:, r]) for r in [d] + [x for x in range(8) if x != d]] + \
                [({"const": 1}, np.ones(n, dtype=np.uint64))]  # noqa: E731
        r = fit_alu_rows(lib, g, d_rows, srcs_for, induce_rows)
        if r is not None:
            return {"kind": "alu", "dest": {"reg": d}, **r}
    if (before == after).all() and (fl == fla).all():
        return {"kind": "none"}
    return None


def group_rows(data, idx, s):
    keys = defaultdict(list)
    win, length = data["window"], data["length"]
    for i in idx:
        l = int(length[i])
        if s >= l:
            continue
        keys[(l, s, win[i, :l - s].tobytes())].append(i)
    return keys


def take(data, rows):
    rows = np.asarray(rows)
    return {"before": u64(data["regs"][rows]), "after": u64(data["after"][rows]), "flags": data["flags"][rows],
            "after_flags": data["after_flags"][rows], "window": data["window"][rows], "syscall": data["syscall"][rows],
            "store": data["store"][rows], "store_addr": u64(data["store_addr"][rows]), "store_value": u64(data["store_value"][rows])}


def reg_roles(effect):
    """Roles of an effect that name a register."""
    if effect["kind"] == "alu":
        return ["dest"] + (["src"] if "reg" in effect["src"] else [])
    if effect["kind"] == "store":
        return ["addr", "value"]
    return []


def fields_of(opcode):
    return [(j, k) for j in range(len(opcode)) for k in FIELD_SHIFTS]


def code_at(opcode, f):
    return (opcode[f[0]] >> f[1]) & 7


def masked(opcode, fields):
    b = bytearray(opcode)
    for j, k in fields:
        b[j] &= ~(7 << k) & 0xFF
    return bytes(b)


def skeleton(effect, assignment):
    """The merge signature of an effect: its kind and operand roles, with masked roles replaced by their field.

    The extension and the flag taps are left out: they are refitted on the pooled rows of a merged record.
    """
    e = {"kind": effect["kind"]}
    for role in reg_roles(effect):
        e[role] = {"field": list(assignment[role])} if role in assignment else {"reg": effect[role]["reg"]}
    if effect["kind"] == "alu":
        src = effect["src"]
        if "imm" in src:
            e["src"] = {"imm": src["imm"]}
        elif "const" in src:
            e["src"] = {"const": src["const"]}
        # The operation stays in the signature: without it, an opcode-extension field (ModRM.reg of 81 /0 vs 81 /5)
        # looks like a register field, since masking it merges ADD and SUB records that differ only in their table.
        e.update(table=effect["table"], width=effect["width"], write=effect["write"])
    return e


def learn_code_map(groups, fixed_map=None):
    """Global code → register map by voting over fields that merge ≥ 2 groups consistently (step 3a)."""
    if fixed_map is not None:
        return dict(fixed_map), {"supplied": True}
    votes = defaultdict(Counter)
    fams = defaultdict(list)
    for (length, s, opcode), effect in groups.items():
        for role in reg_roles(effect):
            for f in fields_of(opcode):
                key = (length, s, role, f, masked(opcode, [f]), json.dumps(skeleton(effect, {role: f}), sort_keys=True))
                fams[key].append((code_at(opcode, f), effect[role]["reg"]))
    for pairs in fams.values():
        codes = {c for c, _ in pairs}
        consistent = all(len({r for c2, r in pairs if c2 == c}) == 1 for c in codes)
        if len(codes) >= 2 and consistent:
            for c, r in set(pairs):
                votes[c][r] += 1
    cmap = {c: v.most_common(1)[0][0] for c, v in votes.items()}
    return cmap, {"votes": {str(c): dict(v) for c, v in votes.items()}}


def learn_families(groups, cmap, use_fields=True):
    """Step 3b: per group, the field assignment whose (masked key, skeleton) is shared by the most groups."""
    options = {}
    count = Counter()
    for gk, effect in groups.items():
        length, s, opcode = gk
        roles = reg_roles(effect)
        combos = [{}]
        for role in roles:
            reg = effect[role]["reg"]
            opts = [None] + ([f for f in fields_of(opcode) if cmap.get(code_at(opcode, f)) == reg] if use_fields else [])
            combos = [{**c, role: f} if f is not None else dict(c) for c in combos for f in opts]
        sigs = []
        for c in combos:
            if len(set(c.values())) < len(c):
                continue  # two roles cannot share one field
            fields = sorted(set(c.values()))
            sig = (length, s, json.dumps({r: list(f) for r, f in sorted(c.items())}), masked(opcode, fields).hex(),
                   json.dumps(skeleton(effect, c), sort_keys=True))
            sigs.append((c, sig))
        options[gk] = sigs
        for _, sig in sigs:
            count[sig] += 1

    def rank(item):
        c, sig = item
        n = count[sig]
        return (-(n if (n >= 2 or not c) else 0), -len(c), sig)  # a mask must merge ≥ 2 groups to be taken

    families = defaultdict(list)
    for gk, sigs in options.items():
        families[min(sigs, key=rank)[1]].append(gk)
    return families


def _resolve_rows(windows, length, s, role_json, cmap):
    if "reg" in role_json:
        return np.full(len(windows), role_json["reg"])
    j, k = role_json["field"]
    codes = (windows[:, j].astype(np.int64) >> k) & 7
    return np.array([cmap[int(c)] for c in codes])


def refit_family(lib, data, rows, sig, cmap, induce_rows):
    """Width, write, extension, table and taps on the pooled rows of a merged record; None if no single effect fits."""
    length, s, _, _, sk_json = sig
    sk = json.loads(sk_json)
    if sk["kind"] != "alu":
        return sk
    g = take(data, rows)
    n = len(rows)
    d_rows = _resolve_rows(g["window"], length, s, sk["dest"], cmap)
    src = sk["src"]
    if "imm" in src:
        srcs_for = lambda dr: [({"imm": s, "ext": e}, imm_value(g["window"], np.full(n, length), s, e)) for e in ("zero", "sign")]  # noqa: E731
    elif "const" in src:
        srcs_for = lambda dr: [({"const": src["const"]}, np.full(n, src["const"], dtype=np.uint64))]  # noqa: E731
    else:
        sr = _resolve_rows(g["window"], length, s, src, cmap)
        srcs_for = lambda dr: [(src, g["before"][np.arange(n), sr])]  # noqa: E731
    r = fit_alu_rows(lib, g, d_rows, srcs_for, induce_rows)
    if r is None:
        return None
    return {**sk, **r, "src": r["src"]}


def share_taps(records, lib, data, cmap):
    """Step 5 (MDL): per flag, every alu record takes the consistent candidate tap with the largest total support.

    Candidates are every record's own tap and, per table, the tap induced on the union of that table's records; support
    is the number of training rows of all records (any table) a candidate explains. One rule for the whole machine
    beats a per-record constant that only holds because a record never saw the case (e.g. ZF = 0 on an XOR record
    whose 53 rows never produced zero).
    """
    keys = [k for k, rec in records.items() if rec["effect"]["kind"] == "alu"]
    info = {}
    for key in keys:
        rec = records[key]
        e, (length, s) = rec["effect"], rec["shape"]
        g = take(data, rec["rows"])
        n = len(rec["rows"])
        d_rows = _resolve_rows(g["window"], length, s, e["dest"], cmap)
        m = np.uint64(MASK[e["width"]])
        a = g["before"][np.arange(n), d_rows] & m
        src = e["src"]
        if "imm" in src:
            b = imm_value(g["window"], np.full(n, length), s, src["ext"])
        elif "const" in src:
            b = np.full(n, src["const"], dtype=np.uint64)
        else:
            b = g["before"][np.arange(n), _resolve_rows(g["window"], length, s, src, cmap)]
        _, sig = lib.run(e["table"], a, b & m, g["flags"][:, 0].astype(np.int64), e["width"])
        info[key] = (sig, g["flags"].astype(np.int64), g["after_flags"].astype(np.int64), n)
    by_table = defaultdict(list)
    for key in keys:
        by_table[records[key]["effect"]["table"]].append(key)
    changed = 0
    for k, f in enumerate(D.FLAGS):
        cands = {json.dumps(records[key]["effect"]["taps"][f]) for key in keys}
        for tkeys in by_table.values():
            cat = {nm: np.concatenate([info[key][0][nm] for key in tkeys]) for nm in info[tkeys[0]][0]}
            union = D.induce_tap(cat, np.concatenate([info[key][1][:, k] for key in tkeys]),
                                 np.concatenate([info[key][2][:, k] for key in tkeys]))
            if union is not None:
                cands.add(json.dumps(D.tap_json(union)))
        ok = {c: {key for key in keys if np.array_equal(
            D._apply_tap(D.tap_from_json(json.loads(c)), info[key][0], info[key][1][:, k]), info[key][2][:, k])} for c in cands}
        support = {c: sum(info[key][3] for key in ok[c]) for c in cands}
        for key in keys:
            best = max((c for c in cands if key in ok[c]), key=lambda c: (support[c], c))
            if json.loads(best) != records[key]["effect"]["taps"][f]:
                records[key]["effect"]["taps"][f] = json.loads(best)
                changed += 1
    return {"taps_changed": changed}


def operands(e, length, windows, regs):
    """Destination and source values for rows sharing one resolved alu effect."""
    w, d = e["width"], e["dest"]["reg"]
    m = np.uint64(MASK[w])
    n = len(windows)
    src = e["src"]
    if "imm" in src:
        b = imm_value(windows, np.full(n, length), src["imm"], src["ext"])
    elif "reg" in src:
        b = regs[:, src["reg"]]
    else:
        b = np.full(n, src["const"], dtype=np.uint64)
    return regs[:, d] & m, b & m


def apply_effect(lib, e, length, windows, regs, flags):
    """Next registers, flags, syscall, store (enable, address, value) for rows sharing one resolved effect."""
    n = len(windows)
    regs2, flags2 = regs.copy(), flags.astype(np.int64).copy()
    sc, st = np.zeros(n, dtype=np.int64), np.zeros(n, dtype=np.int64)
    addr, val = np.zeros(n, dtype=np.uint64), np.zeros(n, dtype=np.uint64)
    if e["kind"] == "syscall":
        sc[:] = 1
    elif e["kind"] == "store":
        st[:] = 1
        addr, val = regs[:, e["addr"]["reg"]].copy(), regs[:, e["value"]["reg"]].copy()
    elif e["kind"] == "alu":
        w, d = e["width"], e["dest"]["reg"]
        a, b = operands(e, length, windows, regs)
        res, sig = lib.run(e["table"], a, b, flags[:, 0].astype(np.int64), w)
        taps = {f: D.tap_from_json(t) for f, t in e["taps"].items()}
        flags2 = D.flag_values(taps, sig, flags.astype(np.int64))
        if e["write"]:
            regs2[:, d] = (regs[:, d] & ~np.uint64(0xFF)) | res if w == 8 else res
    return regs2, flags2, sc, st, addr, val


def resolve_effect(effect, opcode, cmap):
    """Concrete register numbers for an abstract effect (None if a code has no learned register)."""
    e = json.loads(json.dumps(effect))
    for role in ("dest", "src", "addr", "value"):
        if role in e and isinstance(e[role], dict) and "field" in e[role]:
            code = code_at(opcode, tuple(e[role]["field"]))
            if code not in cmap:
                return None
            e[role] = {"reg": cmap[code]}
    return e


def explains(lib, effect, length, g, cmap, opcode):
    e = resolve_effect(effect, opcode, cmap)
    if e is None:
        return False
    regs2, flags2, sc, st, addr, val = apply_effect(lib, e, length, g["window"], g["before"], g["flags"])
    return bool((regs2 == g["after"]).all() and (flags2 == g["after_flags"]).all() and (sc == g["syscall"]).all()
                and (st == g["store"]).all() and (~g["store"].astype(bool) | ((addr == g["store_addr"]) & (val == g["store_value"]))).all())


class Microcode:
    """Fitted records + table library + code map; serving through a FieldFabric FabricProgram read."""

    def __init__(self, records, lib, cmap, stats):
        self.lib, self.cmap, self.stats = lib, cmap, stats
        api, chart = field_modules()
        self.api = api
        self.fabric = api.FieldFabric()
        view = chart.RoleChartField.from_state({"charts": [], "classes": {}, "merge_log": [], "role_class_merges": [],
                                                "records": [], "active_axes": None})
        self.fabric.register_view("microcode", view)
        self.fabric.manage_view("microcode")
        rows, self.shapes, self.support = [], {}, {}
        for index, ((length, s, mask_json, key_hex), rec) in enumerate(sorted(records.items())):
            shape = json.dumps([length, s, json.loads(mask_json)])
            self.shapes.setdefault(shape, (length, s, [tuple(f) for f in json.loads(mask_json).values()]))
            rows.append(chart.Record("isa", "x86-de64-v2", 0, (shape, key_hex, json.dumps(rec["effect"], sort_keys=True)),
                                     f"induced-{index}", index))
            self.support[(shape, key_hex)] = len(rec["rows"])
        self.fabric.mutate_records("microcode", add=rows)
        self.fabric._refresh_view_indices()
        self.program = api.FabricProgram("read-microcode", (api.ReadStep("microcode", 0, {0: "$shape", 1: "$key"}, {2: "effect"}),),
                                         ("effect",))
        self.n_records = len(rows)
        self.memo = {}
        self.reads = 0

    def lookup(self, window):
        """All (shape, record) hits for one window; most specific (most unmasked opcode bits), then most support."""
        hits = []
        for shape, (length, s, fields) in self.shapes.items():
            opcode = bytes(window[:length - s])
            key = masked(opcode, fields).hex()
            mk = (shape, key)
            if mk not in self.memo:
                reader = self.fabric.__class__.__new__(self.fabric.__class__)
                reader.__dict__.update(self.fabric.__dict__)
                reader.frames, reader.abstractions = {}, {}
                r = reader.run(self.program, {"shape": shape, "key": key}, "isa", "x86-de64-v2")
                self.reads += 1
                self.memo[mk] = json.loads(r["value"]) if r["status"] == "resolved" else None
            if self.memo[mk] is not None:
                hits.append((8 * (length - s) - 3 * len(fields), self.support.get(mk, 0), length, s, fields, opcode, self.memo[mk]))
        if not hits:
            return None, 0
        hits.sort(key=lambda h: (-h[0], -h[1]))
        return hits[0], len(hits)

    def predict(self, windows, regs, flags):
        """Batched: windows (N, 15) uint8, regs (N, 8) uint64, flags (N, 4) → dict of outputs + abstain mask."""
        N = len(windows)
        out = {"regs": regs.copy(), "flags": flags.astype(np.int64).copy(), "length": np.zeros(N, dtype=np.int64),
               "syscall": np.zeros(N, dtype=np.int64), "store": np.zeros(N, dtype=np.int64),
               "store_addr": np.zeros(N, dtype=np.uint64), "store_value": np.zeros(N, dtype=np.uint64),
               "abstain": np.zeros(N, dtype=bool), "ambiguous": np.zeros(N, dtype=bool)}
        plans = defaultdict(list)
        for i in range(N):
            hit, nh = self.lookup(windows[i])
            if hit is None:
                out["abstain"][i] = True
                continue
            out["ambiguous"][i] = nh > 1
            _, _, length, s, _, opcode, effect = hit
            e = resolve_effect(effect, opcode, self.cmap)
            if e is None:
                out["abstain"][i] = True
                continue
            out["length"][i] = length
            plans[json.dumps([length, s, e], sort_keys=True)].append(i)
        for plan, rows in plans.items():
            length, s, e = json.loads(plan)
            rows = np.array(rows)
            r2, f2, sc, st, addr, val = apply_effect(self.lib, e, length, windows[rows], regs[rows], flags[rows])
            out["regs"][rows], out["flags"][rows], out["syscall"][rows], out["store"][rows] = r2, f2, sc, st
            out["store_addr"][rows], out["store_value"][rows] = addr, val
        return out

    def describe(self):
        recs = []
        for r in self.fabric.view("microcode").records:
            recs.append({"shape": json.loads(r.roles[0]), "key": r.roles[1], "effect": json.loads(r.roles[2]),
                         "support_rows": self.support.get((r.roles[0], r.roles[1]), 0)})
        return {"records": recs, "code_map": {str(k): v for k, v in sorted(self.cmap.items())},
                "tables": [t.describe() for t in self.lib.tables], "table_induction": self.lib.induced,
                "stats": {**self.stats, "group_rows": {f"{l}|{s}|{o.hex()}": n for (l, s, o), n in self.stats["group_rows"].items()}}}


def fit(data, arm="learned", induce_rows=256, max_group_rows=512, emit=print):
    """arm: learned (fields + code map learned) | supplied_map (code map = identity, fields learned) | unmasked."""
    lib = Library()
    n = len(data["length"])
    unassigned = np.arange(n)
    groups, group_idx = {}, {}
    passes = []
    for s in IMM_SIZES:
        while True:  # repeat while a pass assigns anything: a table induced late can explain a group tried earlier
            keys = group_rows(data, unassigned, s)
            taken = []
            for gk, rows in sorted(keys.items(), key=lambda kv: (-len(kv[1]), kv[0])):
                g = {**take(data, rows[:max_group_rows]), "s": s, "length": gk[0]}
                effect = fit_group(lib, g, induce_rows)
                if effect is None or (s and not (effect.get("kind") == "alu" and "imm" in effect.get("src", {}))):
                    continue
                if len(rows) > max_group_rows:  # the effect must hold on every row of the group, not only the fitting rows
                    if fit_group(lib, {**take(data, rows), "s": s, "length": gk[0]}, induce_rows) != effect:
                        continue
                groups[gk], group_idx[gk] = effect, rows
                taken += rows
            unassigned = np.setdiff1d(unassigned, np.array(taken, dtype=np.int64))
            passes.append({"imm_bytes": s, "rows_assigned": len(taken)})
            if not taken:
                break
    cmap, cinfo = learn_code_map(groups, fixed_map={c: c for c in range(8)} if arm == "supplied_map" else None)
    families = learn_families(groups, cmap, use_fields=arm != "unmasked")
    records, split, merged, collided = {}, 0, 0, 0
    # Two families can share one masked key but differ in their operation (e.g. XOR r, r with r = r is also SUB r, r).
    # The key can then hold only one of them: the family with more rows keeps it, the others stay unmerged.
    owner = {}
    for sig, gks in families.items():
        rk = sig[:4]
        size = sum(len(group_idx[gk]) for gk in gks)
        if rk not in owner or size > owner[rk][0]:
            owner[rk] = (size, sig)
    for sig, gks in families.items():
        length, s, mask_json, key_hex, _ = sig
        rows = [i for gk in gks for i in group_idx[gk]]
        if len(gks) > 1 and owner[sig[:4]][1] != sig:
            collided += 1
            effect = None
        else:
            effect = refit_family(lib, data, rows, sig, cmap, induce_rows) if len(gks) > 1 else None
        if effect is not None:
            records[(length, s, mask_json, key_hex)] = {"effect": effect, "rows": rows, "shape": (length, s), "groups": len(gks)}
            merged += 1
            continue
        if len(gks) > 1 and owner[sig[:4]][1] == sig:
            split += 1
        for gk in gks:  # unmerged: one record per group with its own concrete effect
            records[(gk[0], gk[1], "{}", gk[2].hex())] = {"effect": groups[gk], "rows": group_idx[gk], "shape": (gk[0], gk[1]),
                                                           "groups": 1}
    absorbed = 0
    merged_keys = [k for k, r in records.items() if r["groups"] > 1]
    for key in [k for k, r in records.items() if r["groups"] == 1]:
        length, s, _, key_hex = key
        opcode = bytes.fromhex(key_hex)
        g = take(data, records[key]["rows"])
        for mk in merged_keys:
            ml, ms_, mmask, mkey = mk
            fields = [tuple(f) for f in json.loads(mmask).values()]
            if (ml, ms_) != (length, s) or masked(opcode, fields).hex() != mkey:
                continue
            if explains(lib, records[mk]["effect"], length, g, cmap, opcode):
                records[mk]["rows"] = records[mk]["rows"] + records[key]["rows"]
                del records[key]
                absorbed += 1
                break
    shared = share_taps(records, lib, data, cmap)
    stats = {"arm": arm, "train_rows": int(n), "groups": len(groups), "unfit_rows": int(len(unassigned)),
             "merged_records": merged, "families_split_on_refit": split, "families_lost_key_collision": collided, "absorbed_groups": absorbed, "passes": passes, "code_map_info": cinfo, "shared_taps": shared,
             "group_rows": {gk: len(r) for gk, r in group_idx.items()}}
    emit("ISA_DESF_FIT:" + json.dumps({"arm": arm, "rows": int(n), "groups": len(groups), "records": len(records), "merged": merged,
                                        "split": split, "collided": collided, "absorbed": absorbed, "tables": len(lib.tables), "unfit_rows": int(len(unassigned)),
                                        "code_map": {str(k): v for k, v in sorted(cmap.items())}}))
    return Microcode(records, lib, cmap, stats)


class TorchAdapter:
    """Presents a fitted Microcode as the Executor interface used by v2.exactness / run_program / carry_run_panel."""

    def __init__(self, mc):
        self.mc = mc
        self.abstained = 0
        self.ambiguous = 0
        self.mixers = []

    def eval(self):
        return self

    def train(self):
        return self

    def __call__(self, win, regs, flags, capture=None):
        w = win.cpu().numpy().astype(np.uint8).reshape(len(win), 15, 8)
        windows = (w.astype(np.uint16) << np.arange(8, dtype=np.uint16)).sum(-1).astype(np.uint8)
        rb = regs.cpu().numpy().astype(np.uint64)  # (N, 8, 64)
        rv = (rb << np.arange(64, dtype=np.uint64)).sum(-1, dtype=np.uint64)
        fl = flags.cpu().numpy().astype(np.int64)
        o = self.mc.predict(windows, rv, fl)
        self.abstained += int(o["abstain"].sum())
        self.ambiguous += int(o["ambiguous"].sum())
        sign = lambda x: torch.from_numpy(np.where(x, 1.0, -1.0).astype(np.float32))  # noqa: E731
        regs_bits = (o["regs"][:, :, None] >> np.arange(64, dtype=np.uint64)) & np.uint64(1)
        ab = o["abstain"]
        reg_logits = sign(regs_bits.astype(bool))
        if ab.any():
            reg_logits[torch.from_numpy(ab)] = -reg_logits[torch.from_numpy(ab)]  # an abstention never counts as exact
        length = np.zeros((len(windows), 15), dtype=np.float32) - 1
        length[np.arange(len(windows)), np.clip(o["length"] - 1, 0, 14)] = 1
        bits64 = lambda x: sign(((x[:, None] >> np.arange(64, dtype=np.uint64)) & np.uint64(1)).astype(bool))  # noqa: E731
        return {"regs": reg_logits, "flags": sign(o["flags"].astype(bool)), "length": torch.from_numpy(length),
                "syscall": sign(o["syscall"].astype(bool)), "store": sign(o["store"].astype(bool)),
                "store_addr": bits64(o["store_addr"]), "store_value": bits64(o["store_value"]),
                "dest": torch.zeros(len(windows), 8), "src": torch.zeros(len(windows), 8),
                "width": torch.zeros(len(windows), 3), "imm": torch.zeros(len(windows), 64)}
