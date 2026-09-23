#!/usr/bin/env python3
"""Stdlib-only integrity + verdict verifier for the four-quadrant test bundle.

Checks:
  1. SHA-256 of every bundled file against this file's embedded manifest (tamper-evidence).
  2. PNG magic bytes on every extracted render pane.
  3. Re-derives the campaign's headline verdicts from the shipped raw reports:
     - cross-model slot write at ceiling parity (job-69e2f6a6b492)
     - fp32 disambiguator pass + floor-bias confirmation (job-6299f2391d5c)
     - token-time point-read families present (job-8a96572572cd)
     - language-model necessity table and FLUX write-schedule values (jobs 6650205b45eb, 72f0e98679d5)

Exit codes: 0 = all checks pass, 2 = verdict re-derivation mismatch, 3 = integrity failure.
"""
import hashlib, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
MANIFEST = {
    "README.md": "d4c68ab57aa4994a3191fa737cdc330d7e1d7aade7fe0bc10b4d653105a20639",
    "anchored-parity-base-lion-s7217-job-0706b0497903.png": "9c8ac83ef014ba9b23c3ac9102e14c9a7b3fe6aed74c67624b96a1b23ba28e63",
    "anchored-parity-bridged-authorship-lion-s7217-job-0706b0497903.png": "5392ef1a79171cba3278b67466414267d67c345a9af6c29aa85eae6d3dca1f7e",
    "anchored-parity-bridged-authorship-wolf-s31337-job-0706b0497903.png": "df972726af3a97601914e9bc373b21c298b14af4d35b81af8ffede2925eab57d",
    "anchored-parity-native-authorship-lion-s7217-job-0706b0497903.png": "3eed5a73751df01c777affbc241f729e821d87e06d53982c786095ef768f8eb7",
    "anchored-parity-native-authorship-wolf-s31337-job-0706b0497903.png": "81c0175dda92179068a672c06242f930d236b5f2e0ef7fcf971cb12c770f1261",
    "anchored-parity-sham-lion-s7217-job-0706b0497903.png": "f9081baea02d26481b34ca035d289cf77446abf6dffca9534254089214aa5d8a",
    "anchored-parity-sham-wolf-s31337-job-0706b0497903.png": "b261c485c01302d6fb0ce88833733edf82ee576c7f53397184d31b22a6faa25e",
    "anchored-parity-target-wolf-s31337-job-0706b0497903.png": "f15e60049609a8857ee90baadc360c22072f4d776b13d78a54dbb6dd7440d49b",
    "kernel-allsteps-lion-s7217-job-6650205b45eb.png": "fe160e8522d2cdf951bc0d3f09480f12761f66cc6fd8ef9858d24760e685fda7",
    "kernel-late-double-dose-lion-s7217-job-6650205b45eb.png": "b5ee092a05d138ab5b369abb1ade0f4e0a88fb2cf39f0c44a7c62bbe17d39efc",
    "kernel-steponly-lion-s7217-job-6650205b45eb.png": "e2386736d6143a9aae745c9b100e4ac4173a6c7320c3d7a4f5f82269d96a094b",
    "kernel-target-lion-s7217-job-6650205b45eb.png": "22e3cd4b3270ce6ac08dfb8d3d3e76dbee0c5481ef55c74375803afc1550eda5",
    "report-final-tests-attempt1-job-88891036c1ee.json": "3bacfe79cdae4d12dd14e06e77291d3894c610627c7d3b016971e28599b38eb4",
    "report-final-tests-rerun-job-69e2f6a6b492.json": "44f89fc6ffc6f7a763793b8f8acf23894bb99481a40f2a0d80ea827f59c0f439",
    "report-fp32-recheck-job-6299f2391d5c.json": "c71544e404f935905c63fbb5ee56298d5276c2eb4cbab11d6f9ff56a7501f694",
    "report-lm-grid-job-72f0e98679d5.json": "5d22a9d21134a0a81b25fd4a2961e55bae7712c2b574148efbaab5a3d4d8b285",
    "report-lm-necessity-and-write-schedule-job-6650205b45eb.json": "3c1a4f6a6b40cca47a76d3bfb66824ff3ef76e601cab079b3b26d9209b32071d",
    "report-token-time-kernel-job-8a96572572cd.json": "2bd07b5e3bee7a48ceea5d638dbc89725e750faca16259fcfba0577db0484b82",
    "run-receipt-anchored-authorship-parity-job-0706b0497903.json": "7a40e3c478da16463372462b21801dc5b9588c101dda4d0e6a61c1dfed925a71",
    "run-receipt-final-tests-attempt1-prior-confound-job-88891036c1ee.json": "72ddcca0275b798604a9c52a70fcfa39cab66b7d663147794dd60f085c189c9c",
    "run-receipt-final-tests-rerun-floor-instrument-job-69e2f6a6b492.json": "ac78244dc68c214db345fdf521114c4f534def7f9f53af313ad753789d044720",
    "run-receipt-fp32-recheck-parity-0001-nats-job-6299f2391d5c.json": "21f9b5ad803b649c03070006a99ccbaff8fddd8f59a0be2de76d61a5fdad28b9",
    "run-receipt-grid-4of4-and-p1-path-dependence-job-72f0e98679d5.json": "ef0ccae0279e524ca1e47b074615bf0d06ded28e7b30b4893ec2f87becab9140",
    "run-receipt-k1-consumer-pass-job-e26a9f22e328.json": "34019e425dd219657c7e42e0feeecda7e0942ffe92efba4c521a8166de0ca09a",
    "run-receipt-p4-crossslot-attempt1-log-custody-job-0a07cb92d360.json": "9af6872e2809c45ebf710792dc9138a4ba79b616688a96ea746a0a3d306cdcca",
    "run-receipt-reading-35of54-job-2f81d080712e.json": "54deb90985ed754a2b0892ba0c3f26b678ac46f08a391d9ea68f11fc14c76025",
    "run-receipt-relations-latent-probe-job-6f4ee8adecd9.json": "1232ac6937471770fa915aa71655d95c9ad8e86ac38ba7ee1e34f6ddbf91f088",
    "run-receipt-sink-certificate-and-kernel-job-6650205b45eb.json": "5f900a93d1f088eb14883e788c52e968bd26b91cc8082a80fdd5b71e64620ae7",
    "run-receipt-symbol-class-battery-job-9c6453d29ac1.json": "0b6419ec30d6699650e48af38bb85652ac406d3253356ff02fa895e3539387ff",
    "run-receipt-token-time-kernel-job-8a96572572cd.json": "119184f423fc6e0148981f80f08cf7fd6a8f5149ab3bbb25f7bdeaa1163ab1ab",
    "run-receipt-v1-voided-refute-job-0b95e9b4326d.json": "4bcdd0218dfa0644820a86c9057c19f74641aeafbb4caec17e075951d4b04eb9",
    "run-receipt-zeroshot-authorship-negative-job-d8c971ba6e6f.json": "56fe258a273bfa4256c8eed2d5986fd762669563c3cc6b0252f581d777a609ad",
    "zeroshot-negative-bridged-authorship-wolf-s31337-job-d8c971ba6e6f.png": "59aa3b218293844d8064470a9d0f3b7204370df297090e442a1c949e2cc60fa2",
    "zeroshot-negative-native-control-wolf-s31337-job-d8c971ba6e6f.png": "81c0175dda92179068a672c06242f930d236b5f2e0ef7fcf971cb12c770f1261",
    "zeroshot-negative-sham-wolf-s31337-job-d8c971ba6e6f.png": "328baf671893b79bb2de5f6cfb5edb60cd37cd5b80b373bfd0d4300429a1acaf",
    "zeroshot-negative-target-wolf-s31337-job-d8c971ba6e6f.png": "f15e60049609a8857ee90baadc360c22072f4d776b13d78a54dbb6dd7440d49b",
}

def fail(code, msg):
    print("FAIL:", msg); sys.exit(code)

def main():
    # 1. integrity
    for fname, expected in sorted(MANIFEST.items()):
        p = os.path.join(HERE, fname)
        if not os.path.exists(p):
            fail(3, f"missing file: {fname}")
        got = hashlib.sha256(open(p, "rb").read()).hexdigest()
        if got != expected:
            fail(3, f"hash mismatch: {fname}")
    print(f"integrity: {len(MANIFEST)}/{len(MANIFEST)} files hash-verified")

    # 2. PNG magic
    pngs = [f for f in MANIFEST if f.endswith(".png")]
    for f in pngs:
        if open(os.path.join(HERE, f), "rb").read(8) != b"\x89PNG\r\n\x1a\n":
            fail(3, f"not a PNG: {f}")
    print(f"images: {len(pngs)}/{len(pngs)} valid PNG panes")

    # 3a. cross-model slot write at ceiling parity
    r = json.load(open(os.path.join(HERE, "report-final-tests-rerun-job-69e2f6a6b492.json")))
    cs = r["crossmodel_slot"]
    if abs(cs["gates"]["noop_max_abs"]) > 0.0:
        fail(2, "cross-model no-op gate not exact")
    for t in ("lion", "tiger", "wolf"):
        arms = cs["targets"][t]["arms"]
        d = abs(arms["bridged"]["s_norm"] - arms["true"]["s_norm"])
        if d > 0.005 or arms["bridged"]["s_norm"] < 0.5 or arms["sham"]["s_norm"] >= arms["bridged"]["s_norm"]:
            fail(2, f"ceiling-parity clause failed for {t} (delta {d:.4f})")
        print(f"cross-model slot {t}: bridged {arms['bridged']['s_norm']:.4f} vs true {arms['true']['s_norm']:.4f} (|d|={d:.4f}) sham {arms['sham']['s_norm']:.4f}")

    # 3b. fp32 disambiguator
    r = json.load(open(os.path.join(HERE, "report-fp32-recheck-job-6299f2391d5c.json")))
    v2 = r["v2_verdict"]
    if not v2["v2_pass"] or v2["lp_gap"] >= 0.5:
        fail(2, f"fp32 v2 bar failed (gap {v2['lp_gap']})")
    floors = {k: v["margin"] for k, v in r["floors"].items()}
    if not (floors["creature"] > floors["figure"] > floors["subject"]):
        fail(2, "floor-bias ordering not reproduced")
    print(f"fp32 recheck: v2 PASS at lp_gap {v2['lp_gap']}; floor spread creature {floors['creature']} / figure {floors['figure']} / subject {floors['subject']}")

    # 3c. token-time point-read
    r = json.load(open(os.path.join(HERE, "report-token-time-kernel-job-8a96572572cd.json")))
    fams = r["families"]
    for name, fam in sorted(fams.items()):
        if fam["pc_shift"] <= 2.0:
            fail(2, f"{name}: positive-control shift too small ({fam['pc_shift']})")
        print(f"token-time {name}: pc_shift {fam['pc_shift']}, L={fam['L']}/{fam['n_layers']} layers")

    # 3d. language-model necessity table (paper section 4.2) and write schedule (4.3)
    grid = json.load(open(os.path.join(HERE, "report-lm-grid-job-72f0e98679d5.json")))["grid"]
    cells = {("qwen2.5-0.5b", c): grid["qwen2.5-0.5b"]["cells"][c] for c in ("identity", "color")}
    cells[("smollm2-1.7b", "color")] = grid["smollm2-1.7b"]["cells"]["color"]
    k = json.load(open(os.path.join(HERE, "report-lm-necessity-and-write-schedule-job-6650205b45eb.json")))
    sink = k["ar_sink"]["arms"]
    print(f"smollm2-1.7b identity: L12 {sink['L12']['delta_lp_fox']:+.3f} L18 {sink['L18']['delta_lp_fox']:+.3f} second-half {sink['second_half']['delta_lp_fox']:+.3f} all {sink['all']['delta_lp_fox']:+.3f}")
    if not (sink["all"]["delta_lp_fox"] < -2.0 and max(abs(sink["L12"]["delta_lp_fox"]), abs(sink["L18"]["delta_lp_fox"])) < 0.25 * abs(sink["all"]["delta_lp_fox"])):
        fail(2, "smollm2 identity single-layer vs all-layer shape not reproduced")
    for (m, c), cell in sorted(cells.items()):
        nec = cell["necessity"]
        singles = [a for a in nec if a.startswith("L")]
        best = max(abs(nec[a]["delta_lp_base"]) for a in singles)
        sh = nec["second_half"]
        flip = sh["top1"] != cell["clean"]["top1"]
        print(f"{m} {c}: best single layer |dlp| {best:.3f}, second half {sh['delta_lp_base']:+.3f} -> {sh['top1']}, W2 single {cell['sufficiency'][[a for a in cell['sufficiency'] if a.startswith('W2_L')][0]]['s_norm']:+.4f}, W2 all {cell['sufficiency']['W2_all']['s_norm']:.3f}")
        if not (flip and best < 0.25 * abs(nec["all"]["delta_lp_base"])):
            fail(2, f"{m} {c}: four-quadrant necessity shape not reproduced")
    prog = {(b["target"], b["seed"], b["arm"]): b["progress"] for b in k["kernel"]["branches"]}
    lion = {a: prog[("lion", 7217, a)] for a in ("s0", "s01", "all", "s23_double")}
    print("write schedule lion 7217: " + ", ".join(f"{a} {v:.2f}" for a, v in lion.items()))
    if not (lion["all"] > lion["s01"] > lion["s0"] and lion["all"] > lion["s23_double"]):
        fail(2, "write-schedule ordering not reproduced")

    print("VERIFY OK")
    sys.exit(0)

if __name__ == "__main__":
    main()
