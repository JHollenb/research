#!/usr/bin/env bash
# Run one experiment module on Beast and print its receipt into the job log.
#
#   bash seeds/beast_job.sh <module> [args...]
#
# Uses the venv provisioned once at /mnt/usb-storage/unpaired-rosetta/venv-sys: Beast's existing mrun env
# (torch, numpy, scipy, scikit-learn, huggingface_hub, linked by a .pth file) plus only their library (pinned
# commit fdfad84, copied in) and pylibmgm 1.1.2. Their embeddings are pre-copied to $UNPAIRED_ROSETTA_ROOT, so
# nothing is downloaded per job. Never write to / on Beast.
set -euo pipefail
cd "$(dirname "$0")/.."

BASE=/mnt/usb-storage/unpaired-rosetta
PY=$BASE/venv-sys/bin/python
export HF_HOME=$BASE/hf HF_HUB_OFFLINE=1
export UNPAIRED_ROSETTA_ROOT=$BASE/storage
export OMP_NUM_THREADS=${OMP_NUM_THREADS:-4} MKL_NUM_THREADS=${MKL_NUM_THREADS:-4}
"$PY" -c "import torch, unpaired_rosetta, pylibmgm; print('env ok torch', torch.__version__)"

module=$1
shift
log=$(mktemp -p "$BASE")
"$PY" -m "$module" "$@" 2>&1 | tee "$log"
path=$(sed -n 's/^receipt: //p' "$log" | tail -1)
rm -f "$log"
[ -n "$path" ] && [ -f "$path" ] || { echo "no receipt" >&2; exit 2; }
echo "UNPAIRED_ROSETTA_RECEIPT_NAME=$(basename "$path")"
echo "UNPAIRED_ROSETTA_RECEIPT_GZIP_B64=$(gzip -c "$path" | base64 -w0)"
