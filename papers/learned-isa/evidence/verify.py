"""Verify the small local reading bundle without model or workspace dependencies."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    manifest = json.loads((root / "evidence/provenance.json").read_text())
    failures = []
    for row in manifest["files"]:
        path = (root / row["snapshot_path"]).resolve()
        if not path.is_relative_to(root):
            failures.append(f"unsafe path: {row['snapshot_path']}")
            continue
        if not path.is_file():
            failures.append(f"missing: {row['snapshot_path']}")
            continue
        data = path.read_bytes()
        if hashlib.sha256(data).hexdigest() != row["snapshot_sha256"]:
            failures.append(f"hash mismatch: {row['snapshot_path']}")
        if len(data) != row["snapshot_bytes"]:
            failures.append(f"size mismatch: {row['snapshot_path']}")
    if failures:
        raise SystemExit("\n".join(failures))
    print(f"Verified {len(manifest['files'])} local evidence/source snapshots.")


if __name__ == "__main__":
    main()
