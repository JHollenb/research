#!/usr/bin/env python3
"""Recompute the paper's FLUX time signature from bundled saved distances."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PINS = {
    "joint-region-report.json": "799f173989898f8d9d5465a717038ec0cc094cf970388dcf9c109f7190f2f4d2",
    "color-necessity-report.json": "2ad48f08f0aebc4422c159a3a887eb7a64ebf6b5a5cd31c14ff0da1c4e124e0a",
}
REVISION = "e7b7dc27f91deacad38e78976d1f2b499d76a294"
STEPS = tuple(f"s{i}" for i in range(4))


def load(name: str) -> dict:
    data = (HERE / name).read_bytes()
    if hashlib.sha256(data).hexdigest() != PINS[name]:
        raise ValueError(f"report identity mismatch: {name}")
    r = json.loads(data)
    if (r["model"], r["revision"], r["steps"]) != ("flux2-klein-4b", REVISION, 4):
        raise ValueError(f"specimen mismatch: {name}")
    return r


def verify() -> dict:
    r = load("joint-region-report.json")
    expected_setups = {"catfox_s4242", "catfox_s9001", "foxcat_s7217"}
    expected_sites = {"j0", "j1", "j0_j1", "joint_region", "route"}
    if set(r["results"]) != expected_setups:
        raise ValueError("setup coverage mismatch")
    cells = []
    for setup, so in r["results"].items():
        if so["no_op"]["mad_vs_source"] != 0:
            raise ValueError(f"nonzero image no-op: {setup}")
        if set(so["site_sets"]) != expected_sites:
            raise ValueError(f"site-set coverage mismatch: {setup}")
        baseline = so["baseline_axis_mad"]
        if baseline <= 0:
            raise ValueError(f"invalid contrast denominator: {setup}")
        for site, sr in so["site_sets"].items():
            values = {}
            for op, arm in (("write", sr["sufficiency"]),
                            ("replace", sr["necessity"]["source"])):
                if set(arm) != {*STEPS, "all"}:
                    raise ValueError(f"step coverage mismatch: {setup}/{site}/{op}")
                values[op] = {}
                for scope, row in arm.items():
                    p = 1 - row["mad_vs_target"] / baseline
                    if abs(p - row["scene_progress"]) > 1e-5:
                        raise ValueError(f"progress mismatch: {setup}/{site}/{op}/{scope}")
                    values[op][scope] = p
            w, n = values["write"], values["replace"]
            criteria = {
                "every_single_write_below_0.90": max(w[s] for s in STEPS) < .90,
                "every_single_replacement_above_0.15": min(n[s] for s in STEPS) > .15,
                "whole_write_at_least_0.90": w["all"] >= .90,
                "whole_replacement_at_most_0.15": n["all"] <= .15,
            }
            cells.append({"setup": setup, "site_set": site, "criteria": criteria,
                          "singleton_write_max": max(w[s] for s in STEPS),
                          "singleton_replacement_min": min(n[s] for s in STEPS),
                          "whole_write": w["all"], "whole_replacement": n["all"]})

    r = load("color-necessity-report.json")
    if {so["seed"] for so in r["results"].values()} != {7217, 4242, 9001, 2024, 1337}:
        raise ValueError("color seed coverage mismatch")
    color = {}
    for arm in ("canary_e1b_route", "resid_route"):
        counts = dict(single_interchange_target=0, single_deletion_target=0,
                      whole_interchange_source=0, whole_deletion_null=0,
                      whole_sham_null=0, zero_noop=0)
        for so in r["results"].values():
            a = so["arms"][arm]
            for scopes in a.values():
                for row in scopes.values():
                    nearest = min(("source", "target", "null"),
                                  key=lambda c: row[f"mad_vs_{c}"])
                    if nearest != row["nearest"]:
                        raise ValueError(f"nearest-reference mismatch: {so['seed']}/{arm}")
            counts["single_interchange_target"] += all(a["source"][s]["nearest"] == "target" for s in STEPS)
            counts["single_deletion_target"] += all(a["zero"][s]["nearest"] == "target" for s in STEPS)
            counts["whole_interchange_source"] += a["source"]["all"]["nearest"] == "source"
            counts["whole_deletion_null"] += a["zero"]["all"]["nearest"] == "null"
            counts["whole_sham_null"] += a["sham"]["all"]["nearest"] == "null"
            counts["zero_noop"] += a["noop"]["all"]["mad_vs_target"] == 0
        color[arm] = counts

    certificate_count = sum(all(c["criteria"].values()) for c in cells)
    return {"mechanics_status": "record-consistent", "scope": "saved distances; no model execution",
            "input_sha256": PINS, "four_quadrant_cells": cells,
            "four_quadrant_certificates": certificate_count,
            "color_necessity_seeds": 5, "color_necessity": color}


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
