# Redactions (certified-semantic-circuits)

Host-specific paths and hostnames were replaced with placeholders after the runs; scalar results are unchanged; original file hashes are listed in REDACTIONS.json.

This scan covered `corrections/` and `verifier/` only (not `paper.md` or `README.md`, which were left untouched). No host-specific paths, machine nicknames, private IPs, or remote-storage/SSH URLs were found in those files, so 0 file(s) needed editing. `verifier/verify_pythia_induction.py` was intentionally left unmodified even though it was in scope, because its SHA-256 is quoted in the paper; a manual check of that file also found no host-specific strings in it. See REDACTIONS.json for the (empty) per-pattern replacement log.
