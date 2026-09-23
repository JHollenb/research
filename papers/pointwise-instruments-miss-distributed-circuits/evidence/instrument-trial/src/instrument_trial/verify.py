#!/usr/bin/env python3
"""Verify the Instrument Trial bundle on any machine. Stdlib only, no GPU.

Checks, in order:
  1. Every bundled receipt matches its SHA-256 in bundle/manifest.json.
  2. Every case verdict re-derives from the receipts by the frozen mechanical
     decision rules (the same rules frozen in the preregistration).

Exit codes: 0 = all verified; 3 = a hash or verdict mismatch; 2 = structural
error (missing files, malformed JSON).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

NECESSITY_THRESHOLD = 0.15
COSINE_RECOVERED_THRESHOLD = 0.99


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def derive_case_1(bundle: Path) -> dict[str, str]:
    sweep = _load(bundle / "case-1" / "native-object-mediation.json")
    necessity = [b for b in sweep["panel"]["branches"]
                 if b["kind"] == "necessity"]
    passing = [b for b in necessity
               if b["donor_progress"] <= NECESSITY_THRESHOLD]
    standard = ("necessary component exists" if passing
                 else "no necessary component")
    ledger = _load(bundle / "case-1" / "circuit-panel-ledger.json")
    row = next(r for r in ledger["rows"] if r["axis_id"] == "identity_cat_fox")
    output_check = (
        "the 4-site route is jointly necessary as a time-accumulated object"
        if (row["level"] == "certified"
            and row["aggregate"]["max_route_ablation_progress"]
            <= NECESSITY_THRESHOLD)
        else "route not certified")
    return {"standard": standard, "output_check": output_check}


def derive_case_2_probe(bundle: Path) -> dict[str, str]:
    rep = _load(bundle / "case-2" / "probe-job-f58bcd26f295-report.json")
    gates = rep["gates"]
    if not (gates["parity_ok"] and gates["g1_ok"]):
        return {"standard_strengthened": "arm broken (gates failed)"}
    primary = str(rep["model"]["mapper_seeds"][0])
    return {"standard_strengthened": rep["foreign_scores"][primary]["verdict"]}


def derive_case_3(bundle: Path) -> dict[str, Any]:
    out: dict[str, Any] = {"standard": {}, "output_check": {}}
    for path in sorted((bundle / "case-3").glob("whitening-job-*-report.json")):
        rep = _load(path)
        for mr in rep["model_reports"]:
            model = mr["model"]
            fractions = mr["transform_negative_fraction_overall"]
            raw = fractions["raw"]
            if not mr["parity_within_tolerance"]:
                out["standard"][model] = "arm broken (parity gate failed)"
                continue
            out["standard"][model] = (
                "representations differ across families" if raw > 0.30
                else "no representational difference detected")
            transformed = min(fractions["centered"], fractions["zca"])
            if raw > 0.30 and transformed <= 0.5 * raw:
                out["output_check"][model] = (
                    "the split is an artifact of fitted-direction transfer "
                    "(collapses under centering/whitening); native geometry "
                    "not divergent")
            elif raw <= 0.30:
                out["output_check"][model] = ("no representational difference "
                                        "(consistent with raw)")
            else:
                out["output_check"][model] = ("split persists under whitening; "
                                        "representational difference not "
                                        "ruled out")
    return out


def derive_case_2(bundle: Path) -> dict[str, str]:
    rep = _load(bundle / "case-2" / "xcond-job-e1ba0cbed889-report.json")
    resid = rep["readout"]["carrier_resid"]
    floor = rep["readout"]["resid_floor_deer_vs_tiger"]
    above = {a: c for a, c in resid.items() if c > floor}
    standard = ("no decodable content" if not above
                 else "decodable: " + max(above, key=above.get))
    e3 = [b for b in rep["branches"]
          if b["label"] == "E3:transplant_foreign_subject_into_native"]
    sham = [b for b in rep["branches"]
            if b["label"] == "E2a:sham_noise_subject_rows"]
    moved = all(b["roi"]["fox"]["progress"] > 0.3 for b in e3)
    sham_flat = all(abs(b["roi"]["fox"]["progress"]) < 0.1 for b in sham)
    gates_exact = all(v == 0.0 for v in rep["gates"].values())
    output_check = ("subject rows carry content (transplant moves the subject region "
              "on both seeds, sham flat, exact gates)"
              if moved and sham_flat and gates_exact else "not established")
    return {"standard": standard, "output_check": output_check}


def derive_case_4(bundle: Path) -> dict[str, str]:
    rep = _load(bundle / "case-4" / "tecm-v2-job-3a259f6d1b9e-report.json")
    smol = rep["comparisons"]["flux2-smol"]
    tecm_cos = [smol[p]["tecm_carrier_cosine"] for p in smol]
    standard = ("state recovered"
                 if all(c >= COSINE_RECOVERED_THRESHOLD for c in tecm_cos)
                 else "state not recovered")
    duplicate_mad = rep["checkpoint_control"][
        "same_process_native_duplicate"]["rgb_mad"]
    render_mad = [smol[p]["tecm_vs_native"]["rgb_mad"] for p in smol]
    template_cos = [smol[p]["template_carrier_cosine"] for p in smol]
    behaviorally_wrong = (min(render_mad) > 50.0 and duplicate_mad == 0.0
                          and all(c >= COSINE_RECOVERED_THRESHOLD
                                  for c in template_cos))
    output_check = ("state not recovered (rendered output contradicts the cosine; "
              "content-free template matches it)"
              if behaviorally_wrong else "not established")
    return {"standard": standard, "output_check": output_check}


def derive_case_5(bundle: Path) -> dict[str, str]:
    cells = []
    for path in sorted((bundle / "case-5").glob("mediation-job-*-report.json")):
        rep = _load(path)
        for axis, entry in rep["axes"].items():
            for gate in entry["certificate"]["gates"]:
                if gate["id"] == "mediation":
                    cells.append(bool(gate["passed"]))
    n_pass = sum(cells)
    output_check = (f"not a step artifact: {n_pass}/{len(cells)} axis x step cells "
              "hold; failure localized"
              if n_pass >= len(cells) - 1 and len(cells) >= 12
              else "step-generality not established")
    return {"standard": "mediation holds at the measured step; "
                         "no claim about other steps",
            "output_check": output_check}


def main() -> int:
    parser = argparse.ArgumentParser()
    default_root = Path(__file__).resolve().parents[2]
    parser.add_argument("--bundle", type=Path,
                        default=default_root / "bundle")
    parser.add_argument("--expected", type=Path,
                        default=default_root / "verdicts" / "expected.json")
    args = parser.parse_args()

    try:
        manifest = _load(args.bundle / "manifest.json")
    except (OSError, json.JSONDecodeError) as err:
        print(f"structural error: cannot read manifest: {err}")
        return 2

    mismatches = []
    for rel, expected_sha in sorted(manifest.items()):
        path = args.bundle / rel
        if not path.is_file():
            print(f"structural error: missing bundled file {rel}")
            return 2
        actual = _sha(path)
        status = "ok" if actual == expected_sha else "HASH MISMATCH"
        if actual != expected_sha:
            mismatches.append(rel)
        print(f"  {status:14s} {rel}")

    try:
        expected = _load(args.expected)
        derived = {
            "case-1": derive_case_1(args.bundle),
            "case-2": derive_case_2(args.bundle),
            "case-2-probe": derive_case_2_probe(args.bundle),
            "case-3": derive_case_3(args.bundle),
            "case-4": derive_case_4(args.bundle),
            "case-5": derive_case_5(args.bundle),
        }
    except (OSError, KeyError, json.JSONDecodeError, StopIteration) as err:
        print(f"structural error during verdict derivation: {err}")
        return 2

    verdict_mismatch = False
    for case, arms in sorted(derived.items()):
        for arm, verdict in sorted(arms.items()):
            want = expected.get(case, {}).get(arm)
            ok = verdict == want
            verdict_mismatch |= not ok
            print(f"  {'ok' if ok else 'VERDICT MISMATCH':18s} {case}/{arm}: "
                  f"{verdict}")

    if mismatches or verdict_mismatch:
        print("RESULT: FAILED verification")
        return 3
    print("RESULT: all hashes and all mechanical verdicts verified")
    return 0


if __name__ == "__main__":
    sys.exit(main())
