# Downloading PDMX and running the v1 filter

Confirmed 2 September 2026 against the live Zenodo record
**https://zenodo.org/records/15571083** (v9, published 1 June 2025,
DOI **10.5281/zenodo.15571083**). HEAD of the CSV URL returned HTTP 200
with `Content-Length: 225399738`. The downloaded CSV MD5 matched the
record: `30392ccf38bb63ce70e7afae70f9c88c`.

Do **not** download the 9.6 GB `pdf.tar.gz` or the “Download All” 14.4 GB
bundle. The app wants symbolic files (MIDI + MusicXML).

## Exact file URLs (v9)

Prefer the `/api/records/.../files/.../content` links; they are the
bytes Zenodo actually serves. The `?download=1` HTML links resolve to
the same objects.

| File | Bytes | md5 | API URL |
| --- | ---: | --- | --- |
| `PDMX.csv` | 225,399,738 | `30392ccf38bb63ce70e7afae70f9c88c` | https://zenodo.org/api/records/15571083/files/PDMX.csv/content |
| `mid.tar.gz` | 214,395,208 | `d920a21b2fcd99a56d9c381b39debbb2` | https://zenodo.org/api/records/15571083/files/mid.tar.gz/content |
| `mxl.tar.gz` | 1,894,335,797 | `49ffd75ecf5489c0be6d41182eb11ff7` | https://zenodo.org/api/records/15571083/files/mxl.tar.gz/content |
| `metadata.tar.gz` | 159,444,765 | `5bc79445090dd2fe5e96cffa77a3461c` | https://zenodo.org/api/records/15571083/files/metadata.tar.gz/content |
| `data.tar.gz` (MusicRender JSON) | 2,237,580,506 | `f38dfa7b75f95e5a3d8d70459c1f9b72` | https://zenodo.org/api/records/15571083/files/data.tar.gz/content |
| `subset_paths.tar.gz` | 29,258,714 | `092eee416ece8060f77d08575b94a43d` | https://zenodo.org/api/records/15571083/files/subset_paths.tar.gz/content |
| `pdf.tar.gz` | 9,621,915,440 | `2e03ccd072755332bd63a75c57c89b3f` | **do not download for this app** |

HTML aliases (same files):

- https://zenodo.org/records/15571083/files/PDMX.csv?download=1
- https://zenodo.org/records/15571083/files/mid.tar.gz?download=1
- https://zenodo.org/records/15571083/files/mxl.tar.gz?download=1

Record JSON: https://zenodo.org/api/records/15571083

## Minimum download (filter only)

`PDMX.csv` (~215 MiB) is enough to *build the manifest*. MIDI/MXL
tarballs are needed later, when the app materializes files.

```bash
mkdir -p .cache
curl -L --fail -o .cache/PDMX.csv \
  https://zenodo.org/api/records/15571083/files/PDMX.csv/content
md5sum .cache/PDMX.csv
# expected: 30392ccf38bb63ce70e7afae70f9c88c
```

Or `scripts/download_pdmx.sh csv`.

## Run the filter

Python 3.10+ stdlib only (no pandas).

```bash
python3 scripts/filter_pdmx.py \
  --csv .cache/PDMX.csv \
  --allowlist data/composers.allowlist.json \
  --denylist data/composers.denylist.json \
  --graylist data/composers.graylist.json \
  --manifest data/manifest.csv \
  --stats data/stats.json
```

Prints total kept, piano-only, multi-track, drop reasons, and top
composers. Writes `data/manifest.csv` and `data/stats.json`.

Tests (no 225 MB CSV required):

```bash
python3 tests/test_filter_pdmx.py -v
```

## Unpack MIDI (and optionally MXL) next to the CSV

PDMX paths are relative to the dump root (`./mid/...`, `./mxl/...`).
Zenodo’s own notes:

```bash
PDMX_dir="/path/to/PDMX"
cd "${PDMX_dir}"
# after downloading the tar.gz files into this directory:
tar -xzf mid.tar.gz
# only if the app needs MusicXML:
# tar -xzf mxl.tar.gz
```

Then join `data/manifest.csv` columns `mid` / `mxl` onto that directory.
Do not commit the tarballs or the CSV into git (see `.gitignore`).

## What the filter actually checks

See the module docstring in `filter_pdmx.py` and the short list in the
top-level README. Composer matching: lowercase, strip accents and
punctuation, drop parenthetical years, then match aliases as phrases or
token bags. `C.P.E. Bach` is not `J.S. Bach`. `Richard Strauss` is not
`Johann Strauss II`.
