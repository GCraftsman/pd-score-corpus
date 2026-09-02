#!/usr/bin/env bash
# Download selected PDMX v9 files from Zenodo record 15571083.
# Usage: scripts/download_pdmx.sh [csv|mid|mxl|metadata]
# Default: csv
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DEST="${PDMX_CACHE:-$ROOT/.cache}"
mkdir -p "$DEST"

API="https://zenodo.org/api/records/15571083/files"
TARGET="${1:-csv}"

fetch() {
  local name="$1" md5="$2"
  local url="${API}/${name}/content"
  echo "GET $url -> $DEST/$name"
  curl -L --fail -o "$DEST/$name" "$url"
  local got
  got="$(md5sum "$DEST/$name" | awk '{print $1}')"
  if [[ "$got" != "$md5" ]]; then
    echo "md5 mismatch for $name: got $got expected $md5" >&2
    exit 1
  fi
  echo "ok $name md5 $got"
}

case "$TARGET" in
  csv) fetch PDMX.csv 30392ccf38bb63ce70e7afae70f9c88c ;;
  mid) fetch mid.tar.gz d920a21b2fcd99a56d9c381b39debbb2 ;;
  mxl)
    echo "warning: mxl.tar.gz is ~1.9 GB" >&2
    fetch mxl.tar.gz 49ffd75ecf5489c0be6d41182eb11ff7
    ;;
  metadata) fetch metadata.tar.gz 5bc79445090dd2fe5e96cffa77a3461c ;;
  pdf)
    echo "refusing to download pdf.tar.gz (~9.6 GB). Not needed for this app." >&2
    exit 2
    ;;
  *)
    echo "usage: $0 [csv|mid|mxl|metadata]" >&2
    exit 2
    ;;
esac
