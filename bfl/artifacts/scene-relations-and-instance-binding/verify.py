"""Verify summary-bundle hashes and recompute the finite equality/energy facts."""
from pathlib import Path
import hashlib
import json

ROOT=Path(__file__).resolve().parent


def main():
    manifest=json.loads((ROOT/'followup-manifest.json').read_text())
    for name,record in manifest['files'].items():
        raw=(ROOT/name).read_bytes()
        assert len(raw)==record['bytes'] and hashlib.sha256(raw).hexdigest()==record['sha256'],name
    first=json.loads((ROOT/'first-cut-report.json').read_text())
    second=json.loads((ROOT/'route-factorization-report.json').read_text())
    assert len(first['rows'])==33 and len(second['rows'])==30
    rows={r['row_id']:r for r in first['rows']}
    site_equal=0
    for seed in first['config']['seeds']:
        left,right=(rows[f'{seed}--compiled-{side}'] for side in ('left','right'))
        assert left['rgb_sha256']==right['rgb_sha256']
        assert rows[f'{seed}--neutral']['rgb_sha256']==rows[f'{seed}--zero-compiled']['rgb_sha256']
        for a,b in zip(left['act_receipts'],right['act_receipts'],strict=True):
            assert a['program_fingerprint']!=b['program_fingerprint']
            assert a['after']['sha256']==b['after']['sha256'];site_equal+=1
    source_equal=0
    for a,b in zip(first['decompositions'],second['decompositions'],strict=True):
        for key in ('native_neutral_sha256','native_left_sha256','native_right_sha256'):
            assert a[key]==b[key];source_equal+=1
    fractions=[d['target_predicate_energy']/d['target_energy'] for d in first['decompositions']]
    print(json.dumps({'files_verified':len(manifest['files']),'site_writes_equal':site_equal,
        'source_states_replayed':source_equal,'predicate_energy_fraction_range':[min(fractions),max(fractions)],
        'scope':'hash and arithmetic verification; visual contact judgments are not independently rescored'}))


if __name__=='__main__':main()
