#!/usr/bin/env python3
"""Verifier for the AR-certificate evidence bundle (stdlib only).

Run from anywhere:  python verify.py [bundle_dir]   (default: this file's dir)

1. Re-checks every receipt's SHA-256 against REDACTIONS.json (sha256_after).
2. Re-derives the headline four-quadrant certificate values directly from the
   (redacted) report.json files — scalars are never redacted — and checks them
   against the pre-stated certificate bars:
     * single-site necessity is inert       (|Δ_single / Δ_all| < 0.25)
     * single-site write is inert           (|W2_single s_norm| <= 0.1)
     * whole-path write authors             (W2_all s_norm >= 0.9)
     * whole-path necessity meets the v2 multi-filler-floor bar
       (|lp(all) - mean_floor_lp| <= 0.5 AND margin(all) <= mean_floor_margin + 0.5),
       with mean_floor recomputed here from the per-filler floors.
3. For Qwen3-8B, checks the two backends (paged-CUDA-fp32, CPU-fp32) agree to
   <= 0.02 nats on the graded quantities (the paper's dual-backend parity).

Exit code 0 iff every hash matches and every headline bar passes.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def check_hashes(bundle: Path):
    red = json.loads((bundle / "REDACTIONS.json").read_text())
    ok = True
    print("== hash re-check (sha256_after) ==")
    for entry in red["files"]:
        f = bundle / entry["file"]
        got = sha256(f)
        want = entry["sha256_after"]
        good = (got == want)
        ok = ok and good
        print(f"  [{'OK' if good else 'MISMATCH'}] {entry['file']}  {got[:16]}")
    return ok


def _frac(a, b):
    return (a / b) if b else float("nan")


def verify_q3_8b(bundle: Path):
    """q3 recheck schema: cell.necessity[*].delta_lp_base/lp_base/margin, floors, v2_verdict."""
    print("\n== Qwen3-8B identity (dual-backend fp32, multi-filler floor) ==")
    backends = {
        "paged-CUDA-fp32": bundle / "qwen3-8b/report-paged-fp32-job-ead9d040871b.json",
        "CPU-fp32": bundle / "qwen3-8b/report-cpu-fp32-job-6299f2391d5c.json",
    }
    allok = True
    graded = {}
    for name, path in backends.items():
        rep = json.loads(path.read_text())
        cell = rep["cell"]
        nec = cell["necessity"]
        suf = cell["sufficiency"]
        d_all = nec["all"]["delta_lp_base"]
        single_fracs = {k: _frac(nec[k]["delta_lp_base"], d_all) for k in ("L18", "L27")}
        floors = rep["floors"]
        mean_floor_lp = sum(f["lp_base"] for f in floors.values()) / len(floors)
        mean_floor_margin = sum(f["margin"] for f in floors.values()) / len(floors)
        all_lp = nec["all"]["lp_base"]
        all_margin = nec["all"]["margin"]
        lp_gap = abs(all_lp - mean_floor_lp)
        w2_single = suf["W2_L18"]["s_norm"]
        w2_all = suf["W2_all"]["s_norm"]
        single_inert = all(abs(v) < 0.25 for v in single_fracs.values())
        write_single_inert = abs(w2_single) <= 0.1
        write_all_authors = w2_all >= 0.9
        v2 = (lp_gap <= 0.5) and (all_margin <= mean_floor_margin + 0.5)
        ok = single_inert and write_single_inert and write_all_authors and v2
        allok = allok and ok
        # cross-check our recomputed gap vs the receipt's stored verdict
        stored = rep.get("v2_verdict", {})
        gap_matches = abs(lp_gap - stored.get("lp_gap", lp_gap)) <= 0.01
        graded[name] = {"all_lp": all_lp, "mean_floor_lp": round(mean_floor_lp, 4),
                        "lp_gap": round(lp_gap, 4), "w2_all": w2_all, "w2_single": w2_single}
        print(f"  [{name}]")
        print(f"    single-site necessity frac  L18={single_fracs['L18']:.4f} "
              f"L27={single_fracs['L27']:.4f}  -> inert<0.25: {single_inert}")
        print(f"    whole-path necessity        lp(all)={all_lp:.4f} mean_floor={mean_floor_lp:.4f} "
              f"gap={lp_gap:.4f} (<=0.5), margin={all_margin:.4f}<= {mean_floor_margin+0.5:.4f}: {v2}")
        print(f"    write  single W2={w2_single:+.4f} (inert<=0.1:{write_single_inert})  "
              f"all W2={w2_all:.4f} (authors>=0.9:{write_all_authors})")
        print(f"    recomputed gap matches stored v2_verdict.lp_gap: {gap_matches}")
        allok = allok and gap_matches
        print(f"    CERT {'PASS' if ok else 'FAIL'}")
    # dual-backend parity
    a, b = graded["paged-CUDA-fp32"], graded["CPU-fp32"]
    parity = max(abs(a[k] - b[k]) for k in ("all_lp", "mean_floor_lp", "lp_gap", "w2_all", "w2_single"))
    print(f"  dual-backend parity (max |Δ| over graded quantities) = {parity:.4f} (<=0.02): {parity <= 0.02}")
    allok = allok and (parity <= 0.02)
    return allok


def verify_q3_30b(bundle: Path):
    """battery schema: cells['qwen3-30b-a3b.identity'].necessity[*].delta_lp/lp_base_answer/margin,
    generic_floor, extra_floors, sufficiency."""
    print("\n== Qwen3-30B-A3B identity (fp32 primary + bf16 companion) ==")
    # fp32 (multi-filler floor) is the certifying run: full v2 bar.
    # bf16 (single-filler floor) is a cross-backend consistency companion: the
    # quadrant shape must hold and necessity-all must still fall to within 0.5 of
    # floor, but the fp32-specific margin bar is reported, not gated (a single
    # bf16 filler floor is fox-biased -- the exact artifact the fp32 multi-filler
    # run was introduced to remove; see wall-a Addendum S/W).
    reps = {
        "fp32 (primary, certifying)": (bundle / "qwen3-30b-a3b/report-fp32-job-ef8408d9c3d2.json", True),
        "bf16 (companion)": (bundle / "qwen3-30b-a3b/report-bf16-job-7cc5b24954f0.json", False),
    }
    allok = True
    for name, (path, gate_margin) in reps.items():
        rep = json.loads(path.read_text())
        cell = rep["cells"]["qwen3-30b-a3b.identity"]
        nec = cell["necessity"]
        suf = cell["sufficiency"]
        d_all = nec["all"]["delta_lp"]
        single_fracs = {k: _frac(nec[k]["delta_lp"], d_all) for k in ("L24", "L36")}
        # multi-filler floor: generic_floor plus any extra_floors
        floor_lps = [cell["generic_floor"]["lp_base_answer"]]
        floor_margins = [cell["generic_floor"]["margin"]]
        for _k, v in (cell.get("extra_floors") or {}).items():
            floor_lps.append(v["floor"]["lp_base_answer"])
            floor_margins.append(v["floor"]["margin"])
        mean_floor_lp = sum(floor_lps) / len(floor_lps)
        mean_floor_margin = sum(floor_margins) / len(floor_margins)
        all_lp = nec["all"]["lp_base_answer"]
        all_margin = nec["all"]["margin"]
        lp_gap = abs(all_lp - mean_floor_lp)
        w2_single = suf["W2_L24"]["s_norm"]
        w2_all = suf["W2_all"]["s_norm"]
        single_inert = all(abs(v) < 0.25 for v in single_fracs.values())
        write_single_inert = abs(w2_single) <= 0.1
        write_all_authors = w2_all >= 0.9
        margin_ok = all_margin <= mean_floor_margin + 0.5
        nec_near_floor = lp_gap <= 0.5
        v2 = nec_near_floor and margin_ok
        ok = single_inert and write_single_inert and write_all_authors and nec_near_floor and (margin_ok or not gate_margin)
        allok = allok and ok
        print(f"  [{name}]  n_floors={len(floor_lps)}")
        print(f"    single-site necessity frac  L24={single_fracs['L24']:.4f} "
              f"L36={single_fracs['L36']:.4f}  -> inert<0.25: {single_inert}")
        print(f"    whole-path necessity        lp(all)={all_lp:.4f} mean_floor={mean_floor_lp:.4f} "
              f"gap={lp_gap:.4f} (<=0.5:{nec_near_floor}), margin={all_margin:.4f}<= {mean_floor_margin+0.5:.4f}: "
              f"{margin_ok}{'' if gate_margin else ' (reported, not gated for companion)'}")
        print(f"    write  single W2={w2_single:+.4f} (inert<=0.1:{write_single_inert})  "
              f"all W2={w2_all:.4f} (authors>=0.9:{write_all_authors})")
        print(f"    {'CERT' if gate_margin else 'COMPANION'} {'PASS' if ok else 'FAIL'}")
    return allok


def main() -> int:
    bundle = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent
    hashes_ok = check_hashes(bundle)
    q8_ok = verify_q3_8b(bundle)
    q30_ok = verify_q3_30b(bundle)
    ok = hashes_ok and q8_ok and q30_ok
    print(f"\n== VERDICT: {'ALL PASS' if ok else 'FAILURES PRESENT'} "
          f"(hashes={hashes_ok} q3_8b={q8_ok} q3_30b={q30_ok}) ==")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
