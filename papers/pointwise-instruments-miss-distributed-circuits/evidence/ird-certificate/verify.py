#!/usr/bin/env python3
"""Stdlib-only integrity + verdict verifier for the IRD golden-demo artifact bundle.

Checks:
  1. SHA-256 of every bundled file against this file's embedded manifest (tamper-evidence).
  2. PNG magic bytes on every extracted render pane.
  3. Re-derives the campaign's headline verdicts from the shipped raw reports:
     - cross-model slot write at ceiling parity (job-69e2f6a6b492)
     - fp32 disambiguator pass + floor-bias confirmation (job-6299f2391d5c)
     - token-time point-read families present (job-8a96572572cd)

Exit codes: 0 = all checks pass, 2 = verdict re-derivation mismatch, 3 = integrity failure.
"""
import hashlib, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
MANIFEST = {
    "README.md": "0c611ee76ddafea3fc6d0ccc221f0f2b825d5d8e8bf43fc5f745296eb2d1aa8f",
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
    "report-final-tests-attempt1-job-88891036c1ee.json": "a9e3a02d41069a72620b9468662d5e8ae947c61cc3abdca097986f3e41855cd0",
    "report-final-tests-rerun-job-69e2f6a6b492.json": "490c0a528f68851a2d9c30b16b9fcb56c9f12016bad6ab2fa109562a5ead138d",
    "report-fp32-recheck-job-6299f2391d5c.json": "c1bc205dab1a2f2dcae0a478d9b4d2f031e21f44f054d43aa24dc43dc5ae572e",
    "report-token-time-kernel-job-8a96572572cd.json": "41569096119c6d9a1ee0021d0ea0a0d6d06ab1e64b0fd9ae41c727baf687b65c",
    "run-receipt-anchored-authorship-parity-job-0706b0497903.json": "cb44c9060136ddd618a38bc37c00f221a71e1ffb0cad8f8259999cc7f8e086cb",
    "run-receipt-final-tests-attempt1-prior-confound-job-88891036c1ee.json": "e19014b6395ddcfbec4a55fb1f688db93b3e1386ac148ecc78a046ec13d4bfb9",
    "run-receipt-final-tests-rerun-floor-instrument-job-69e2f6a6b492.json": "e36b558685a35f9c6dac33382f379ae48a478714973819dc3077b7aed20b9970",
    "run-receipt-fp32-recheck-parity-0001-nats-job-6299f2391d5c.json": "8412be27352a66de913aeb4531ab767475846f855cea095767cfdd07e55bfbb1",
    "run-receipt-grid-4of4-and-p1-path-dependence-job-72f0e98679d5.json": "38e6a43e2aaa20b8fe571a7984d6a5928a8ed2326ae66c99616f58d1a36d7eb2",
    "run-receipt-k1-consumer-pass-job-e26a9f22e328.json": "bfb8c66445d3807701b6f1104354dcc735a572c8719d6ed8ec2e783096879802",
    "run-receipt-p4-crossslot-attempt1-log-custody-job-0a07cb92d360.json": "9a272ff8a602630be3f0e1d082bd7caf1c48dfadc6741502982d094cf5991706",
    "run-receipt-reading-35of54-job-2f81d080712e.json": "4ab35e92f765c6c988455e54fe5f9ce848c355aa9155986061b4e260f606a637",
    "run-receipt-relations-latent-probe-job-6f4ee8adecd9.json": "73271494f6c406a28f981553a65200f0181848d231726671232145a1b8fc28bf",
    "run-receipt-sink-certificate-and-kernel-job-6650205b45eb.json": "76ae8336a7503bf77ff468e4ad2176d782268cefa2fa1586ab2cdc9af1c60f19",
    "run-receipt-symbol-class-battery-job-9c6453d29ac1.json": "faae05a6c0d4505bad7e2e949358903cfb638a13177a29ace4441eaef0972eba",
    "run-receipt-token-time-kernel-job-8a96572572cd.json": "ac5677e2bfa8bc51d1ed710456dedcf863bc9ed021ec0640db4ced203335a579",
    "run-receipt-v1-voided-refute-job-0b95e9b4326d.json": "a36be916a1add7b7dd803f003c0f970b6affbcdc7ba3c563c9b34d2315f35844",
    "run-receipt-zeroshot-authorship-negative-job-d8c971ba6e6f.json": "a88ad58364540522a0f4ed89885c544394118070b372cffe601480ead11337a8",
    "zeroshot-negative-bridged-authorship-wolf-s31337-job-d8c971ba6e6f.png": "59aa3b218293844d8064470a9d0f3b7204370df297090e442a1c949e2cc60fa2",
    "zeroshot-negative-native-control-wolf-s31337-job-d8c971ba6e6f.png": "81c0175dda92179068a672c06242f930d236b5f2e0ef7fcf971cb12c770f1261",
    "zeroshot-negative-sham-wolf-s31337-job-d8c971ba6e6f.png": "328baf671893b79bb2de5f6cfb5edb60cd37cd5b80b373bfd0d4300429a1acaf",
    "zeroshot-negative-target-wolf-s31337-job-d8c971ba6e6f.png": "f15e60049609a8857ee90baadc360c22072f4d776b13d78a54dbb6dd7440d49b"
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

    print("VERIFY OK")
    sys.exit(0)

if __name__ == "__main__":
    main()
