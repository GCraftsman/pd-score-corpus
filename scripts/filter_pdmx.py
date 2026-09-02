#!/usr/bin/env python3
"""Filter PDMX.csv down to a v1 death-date allowlist of 18th–19th century scores.

Reads the official PDMX.csv from Zenodo record 15571083 and writes
data/manifest.csv plus optional data/stats.json.

This script never downloads MuseScore.com. It only reads a local PDMX.csv
(and later, locally unpacked mid/mxl paths recorded in that CSV).
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Iterable

# PDMX.csv is ~225 MB / 254k rows; raise the field-size cap just in case.
csv.field_size_limit(min(sys.maxsize, 32 * 1024 * 1024))

EMPTY_VALUES = {"", "na", "n/a", "none", "null", "nan", "-"}

# Words stripped before composer matching (dates handled separately).
# Do not include single-letter tokens such as "a" — they are initials (W. A. Mozart).
NOISE_TOKENS = {
    "arr",
    "arrd",
    "arranged",
    "arrangement",
    "attrib",
    "attributed",
    "attr",
    "after",
    "by",
    "from",
    "harm",
    "harmonized",
    "trans",
    "transcribed",
    "transcription",
    "edition",
    "ed",
    "the",
    "and",
    "of",
    "an",
    "op",
    "opus",
    "no",
    "nr",
    "number",
    "anon",
    "anonymous",
    "unknown",
    "composer",
    "etc",
}

# JS Bach family members who are not the allowlisted person.
BACH_NOT_JS = re.compile(
    r"\b("
    r"c\s*p\s*e|cpe|carl\s+philipp|emanuel|"
    r"j\s*c\b|johann\s+christian|christian\s+bach|"
    r"w\s*f\b|wilhelm\s+friedemann|friedemann|"
    r"johann\s+christoph|johann\s+ludwig|"
    r"p\s*d\s*q|pdq"
    r")\b"
)

CLARA_SCHUMANN = re.compile(r"\bclara\b")
SIEGFRIED_WAGNER = re.compile(r"\bsiegfried\b")
RICHARD_STRAUSS = re.compile(r"\brichard\b")
ALESSANDRO_SCARLATTI = re.compile(r"\balessandro\b")

YEAR_RE = re.compile(r"\b(?:1[5-9]\d{2}|20\d{2})\b")
PAREN_RE = re.compile(r"\([^)]*\)")
PUNCT_RE = re.compile(r"[^\w\s]+", re.UNICODE)

# Title/tag/genre/song_name denylist. Conservative on "epic": only "epic hybrid".
CONTENT_DENY_PATTERNS = [
    r"\bsoundtrack\b",
    r"\bfilm\s*score\b",
    r"\bfilm\s*music\b",
    r"\bmovie\s*score\b",
    r"\bmovies?\b",
    r"\bfilms?\b",
    r"\btrailers?\b",
    r"\banime\b",
    r"\bdisney\b",
    r"\bvideo\s*games?\b",
    r"\bvideogames?\b",
    r"\bjohn\s+williams\b",
    r"\bzimmer\b",
    r"\bhisaishi\b",
    r"\bepic\s+hybrid\b",
    r"\barrangement\s+of\b",
    r"\barranged\s+from\b",
    r"\barr\.\s*of\b",
]
CONTENT_DENY_RE = re.compile("|".join(CONTENT_DENY_PATTERNS), re.IGNORECASE)

PIANO_RE = re.compile(
    r"\b(piano|pianoforte|fortepiano|kbd|keyboard)\b",
    re.IGNORECASE,
)

MANIFEST_FIELDS = [
    "pdmx_id",
    "musescore_id",
    "path",
    "mxl",
    "mid",
    "metadata",
    "composer",
    "composer_raw",
    "title",
    "song_name",
    "n_tracks",
    "is_piano_only",
    "license",
    "license_url",
    "tracks",
    "tags",
    "genres",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def parse_bool(value: object) -> bool:
    if value is True or value is False:
        return bool(value)
    if value is None:
        return False
    s = str(value).strip().lower()
    if s in {"true", "1", "yes", "t", "y"}:
        return True
    if s in {"false", "0", "no", "f", "n"} or s in EMPTY_VALUES:
        return False
    return False


def is_empty(value: object) -> bool:
    if value is None:
        return True
    return str(value).strip().lower() in EMPTY_VALUES


def strip_accents(text: str) -> str:
    decomposed = unicodedata.normalize("NFKD", text)
    return "".join(ch for ch in decomposed if not unicodedata.combining(ch))


def normalize_text(text: object) -> str:
    if text is None:
        return ""
    s = str(text).replace("\u00a0", " ")
    s = strip_accents(s).lower()
    s = s.replace("ß", "ss")
    s = PAREN_RE.sub(" ", s)
    s = YEAR_RE.sub(" ", s)
    s = s.replace("&", " and ")
    s = PUNCT_RE.sub(" ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def normalize_name(text: object) -> str:
    """Normalize a composer string and drop noise tokens / leftover years."""
    s = normalize_text(text)
    if not s:
        return ""
    tokens = [t for t in s.split() if t not in NOISE_TOKENS and not t.isdigit()]
    return " ".join(tokens)


def load_composer_list(path: Path, key: str = "composers") -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        return list(data.get(key, data.get("composers", [])))
    if isinstance(data, list):
        return data
    raise ValueError(f"Unexpected JSON shape in {path}")


def build_alias_index(entries: Iterable[dict]) -> tuple[dict[str, str], list[tuple[str, str]]]:
    """Return (exact alias -> canonical, aliases sorted longest-first)."""
    exact: dict[str, str] = {}
    pairs: list[tuple[str, str]] = []
    for entry in entries:
        canonical = entry["canonical"]
        aliases = list(entry.get("aliases") or [])
        aliases.append(canonical)
        seen: set[str] = set()
        for alias in aliases:
            n = normalize_name(alias)
            if not n or n in seen:
                continue
            seen.add(n)
            exact.setdefault(n, canonical)
            pairs.append((n, canonical))
    pairs.sort(key=lambda item: len(item[0]), reverse=True)
    return exact, pairs


def phrase_in(haystack: str, needle: str) -> bool:
    if not needle:
        return False
    if haystack == needle:
        return True
    return re.search(rf"(?:^|\s){re.escape(needle)}(?:\s|$)", haystack) is not None


def tokens_present(haystack_tokens: list[str], alias: str) -> bool:
    alias_tokens = alias.split()
    if len(alias_tokens) < 2:
        return False
    hay = set(haystack_tokens)
    return all(tok in hay for tok in alias_tokens)


def match_indexed_name(
    raw: object,
    exact: dict[str, str],
    pairs: list[tuple[str, str]],
) -> str | None:
    n = normalize_name(raw)
    if not n:
        return None
    if n in exact:
        return exact[n]
    tokens = n.split()
    for alias, canonical in pairs:
        if phrase_in(n, alias) or tokens_present(tokens, alias):
            return canonical
    return None


def is_js_bach_excluded(normalized: str) -> bool:
    return BACH_NOT_JS.search(normalized) is not None


def match_allowlist(
    raw: object,
    exact: dict[str, str],
    pairs: list[tuple[str, str]],
) -> str | None:
    n = normalize_name(raw)
    if not n:
        return None

    # Family / namesake guards before generic aliases fire.
    if "bach" in n.split() and is_js_bach_excluded(n) and "sebastian" not in n:
        return None
    if "schumann" in n.split() and CLARA_SCHUMANN.search(n):
        return None
    if "wagner" in n.split() and SIEGFRIED_WAGNER.search(n) and "richard" not in n:
        return None
    if "strauss" in n.split() and RICHARD_STRAUSS.search(n):
        return None
    if "scarlatti" in n.split() and ALESSANDRO_SCARLATTI.search(n) and "domenico" not in n:
        return None

    hit = match_indexed_name(raw, exact, pairs)
    if hit == "Johann Sebastian Bach" and is_js_bach_excluded(n) and "sebastian" not in n:
        return None
    if hit == "Johann Strauss II" and RICHARD_STRAUSS.search(n):
        return None
    if hit == "Domenico Scarlatti" and ALESSANDRO_SCARLATTI.search(n) and "domenico" not in n:
        return None
    if hit == "Robert Schumann" and CLARA_SCHUMANN.search(n):
        return None
    # Bare "bach" (and similar) after noise stripping.
    if hit is None and n == "bach":
        return "Johann Sebastian Bach"
    return hit


def match_denylist_composer(
    raw: object,
    exact: dict[str, str],
    pairs: list[tuple[str, str]],
) -> str | None:
    n = normalize_name(raw)
    if not n:
        return None
    tokens = n.split()
    # John Williams / Vaughan Williams only — not every hymn-tune Williams.
    if "williams" in tokens and ("john" in tokens or "vaughan" in tokens):
        if "vaughan" in tokens:
            return "Ralph Vaughan Williams"
        return "John Williams"
    if "strauss" in tokens and RICHARD_STRAUSS.search(n):
        return "Richard Strauss"
    return match_indexed_name(raw, exact, pairs)


def content_denied(row: dict) -> str | None:
    blob = " ".join(
        str(row.get(col) or "")
        for col in ("title", "tags", "genres", "song_name", "subtitle")
    )
    if is_empty(blob):
        return None
    m = CONTENT_DENY_RE.search(blob)
    if m:
        return m.group(0)
    return None


def parse_n_tracks(value: object) -> int | None:
    if is_empty(value):
        return None
    try:
        return int(float(str(value).strip()))
    except ValueError:
        return None


def looks_like_piano(text: object) -> bool:
    if is_empty(text):
        return False
    return PIANO_RE.search(str(text)) is not None


def classify_piano_only(row: dict, n_tracks: int | None) -> bool:
    """Piano-only: single track AND (tracks/instrumentation or tags look like piano).

    PDMX v9 `tracks` is numeric part IDs (e.g. "0", "0-0"), not instrument
    names. The tracks/instrumentation check is kept for forward compatibility.
    """
    if n_tracks != 1:
        return False
    if looks_like_piano(row.get("tracks")):
        return True
    if looks_like_piano(row.get("tags")):
        return True
    return False


def pdmx_ids(row: dict) -> tuple[str, str]:
    path = str(row.get("path") or "")
    meta = str(row.get("metadata") or "")
    encoding_id = Path(path).stem if path else ""
    musescore_id = Path(meta).stem if meta else ""
    return encoding_id, musescore_id


def column_true(row: dict, *names: str) -> bool | None:
    """Return True/False if any named column exists, else None."""
    found = False
    for name in names:
        if name in row:
            found = True
            if parse_bool(row.get(name)):
                return True
    if found:
        return False
    return None


def keep_row(
    row: dict,
    allow_exact: dict[str, str],
    allow_pairs: list[tuple[str, str]],
    deny_exact: dict[str, str],
    deny_pairs: list[tuple[str, str]],
    require_all_valid: bool,
) -> tuple[bool, str, dict]:
    """Return (keep, drop_reason, extra_fields)."""
    extra: dict = {}

    nlc = column_true(
        row,
        "subset:no_license_conflict",
        "no_license_conflict",
    )
    if nlc is None:
        # Fall back to the inverse of license_conflict if needed.
        if "license_conflict" in row and parse_bool(row.get("license_conflict")):
            return False, "license_conflict", extra
    elif nlc is False:
        return False, "license_conflict", extra

    if require_all_valid:
        av = column_true(row, "subset:all_valid", "all_valid")
        if av is False:
            return False, "not_all_valid", extra

    if parse_bool(row.get("is_original")):
        return False, "is_original", extra
    if parse_bool(row.get("is_draft")):
        return False, "is_draft", extra
    if parse_bool(row.get("has_paywall")):
        return False, "has_paywall", extra

    composer_raw = row.get("composer_name")
    if is_empty(composer_raw):
        return False, "empty_composer", extra

    denied = match_denylist_composer(composer_raw, deny_exact, deny_pairs)
    if denied:
        extra["denylist_composer"] = denied
        return False, "denylist_composer", extra

    denied_content = content_denied(row)
    if denied_content:
        extra["denylist_hit"] = denied_content
        return False, "denylist_content", extra

    canonical = match_allowlist(composer_raw, allow_exact, allow_pairs)
    if not canonical:
        extra["normalized_composer"] = normalize_name(composer_raw)
        return False, "not_allowlisted", extra

    n_tracks = parse_n_tracks(row.get("n_tracks"))
    extra["canonical"] = canonical
    extra["n_tracks"] = n_tracks
    extra["is_piano_only"] = classify_piano_only(row, n_tracks)
    return True, "", extra


def write_manifest_row(writer: csv.DictWriter, row: dict, extra: dict) -> None:
    encoding_id, musescore_id = pdmx_ids(row)
    n_tracks = extra.get("n_tracks")
    writer.writerow(
        {
            "pdmx_id": encoding_id,
            "musescore_id": musescore_id,
            "path": row.get("path") or "",
            "mxl": row.get("mxl") or "",
            "mid": row.get("mid") or "",
            "metadata": row.get("metadata") or "",
            "composer": extra.get("canonical") or "",
            "composer_raw": row.get("composer_name") or "",
            "title": row.get("title") or "",
            "song_name": row.get("song_name") or "",
            "n_tracks": "" if n_tracks is None else n_tracks,
            "is_piano_only": extra.get("is_piano_only"),
            "license": row.get("license") or "",
            "license_url": row.get("license_url") or "",
            "tracks": row.get("tracks") or "",
            "tags": row.get("tags") or "",
            "genres": row.get("genres") or "",
        }
    )


def run_filter(
    csv_path: Path,
    allowlist_path: Path,
    denylist_path: Path,
    manifest_path: Path,
    stats_path: Path | None = None,
    graylist_path: Path | None = None,
) -> dict:
    allow_entries = load_composer_list(allowlist_path)
    deny_entries = load_composer_list(denylist_path)
    allow_exact, allow_pairs = build_alias_index(allow_entries)
    deny_exact, deny_pairs = build_alias_index(deny_entries)

    gray_exact: dict[str, str] = {}
    gray_pairs: list[tuple[str, str]] = []
    if graylist_path and graylist_path.is_file():
        gray_exact, gray_pairs = build_alias_index(load_composer_list(graylist_path))

    drop_reasons: Counter[str] = Counter()
    composer_counts: Counter[str] = Counter()
    gray_seen: Counter[str] = Counter()
    total = 0
    kept = 0
    piano_only = 0
    multi_track = 0
    unknown_tracks = 0

    manifest_path.parent.mkdir(parents=True, exist_ok=True)

    with csv_path.open(newline="", encoding="utf-8") as inf, manifest_path.open(
        "w", newline="", encoding="utf-8"
    ) as outf:
        reader = csv.DictReader(inf)
        if not reader.fieldnames:
            raise SystemExit(f"No header row in {csv_path}")
        require_all_valid = (
            "subset:all_valid" in reader.fieldnames or "all_valid" in reader.fieldnames
        )
        writer = csv.DictWriter(outf, fieldnames=MANIFEST_FIELDS)
        writer.writeheader()
        for row in reader:
            total += 1
            keep, reason, extra = keep_row(
                row,
                allow_exact,
                allow_pairs,
                deny_exact,
                deny_pairs,
                require_all_valid,
            )
            if not keep:
                if reason == "not_allowlisted" and gray_exact:
                    g = match_indexed_name(row.get("composer_name"), gray_exact, gray_pairs)
                    if g:
                        gray_seen[g] += 1
                        drop_reasons["graylist_composer"] += 1
                    else:
                        drop_reasons[reason] += 1
                else:
                    drop_reasons[reason] += 1
                continue
            kept += 1
            composer_counts[extra["canonical"]] += 1
            n_tracks = extra.get("n_tracks")
            if extra.get("is_piano_only"):
                piano_only += 1
            elif n_tracks is None:
                unknown_tracks += 1
            elif n_tracks > 1:
                multi_track += 1
            else:
                # Single-track but not tagged piano: still kept.
                unknown_tracks += 1
            write_manifest_row(writer, row, extra)

    single_track_kept = kept - multi_track
    stats = {
        "source_csv": str(csv_path),
        "zenodo_record": "https://zenodo.org/records/15571083",
        "zenodo_doi": "10.5281/zenodo.15571083",
        "rows_read": total,
        "kept": kept,
        "piano_only": piano_only,
        "multi_track": multi_track,
        "single_track_not_tagged_piano": single_track_kept - piano_only,
        "drop_reasons": dict(drop_reasons),
        "top_composers": composer_counts.most_common(25),
        "composer_counts": dict(composer_counts),
        "graylist_seen_but_dropped": dict(gray_seen),
        "require_all_valid": require_all_valid,
    }
    if stats_path is not None:
        stats_path.parent.mkdir(parents=True, exist_ok=True)
        stats_path.write_text(json.dumps(stats, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return stats


def print_stats(stats: dict) -> None:
    print(f"rows read:          {stats['rows_read']}")
    print(f"kept:               {stats['kept']}")
    print(f"piano-only:         {stats['piano_only']}")
    print(f"multi-track:        {stats['multi_track']}")
    print(
        "single-track (not tagged piano): "
        f"{stats['single_track_not_tagged_piano']}"
    )
    print("drop reasons:")
    for reason, count in sorted(
        stats["drop_reasons"].items(), key=lambda kv: (-kv[1], kv[0])
    ):
        print(f"  {reason:24s} {count}")
    print("top composers:")
    for name, count in stats["top_composers"]:
        print(f"  {count:5d}  {name}")
    gray = stats.get("graylist_seen_but_dropped") or {}
    if gray:
        print("graylist composers seen (dropped, not in v1):")
        for name, count in sorted(gray.items(), key=lambda kv: (-kv[1], kv[0])):
            print(f"  {count:5d}  {name}")


def build_parser() -> argparse.ArgumentParser:
    root = repo_root()
    p = argparse.ArgumentParser(
        description="Filter PDMX.csv to the v1 death-date composer allowlist."
    )
    p.add_argument(
        "--csv",
        type=Path,
        default=root / ".cache" / "PDMX.csv",
        help="Path to PDMX.csv (default: .cache/PDMX.csv)",
    )
    p.add_argument(
        "--allowlist",
        type=Path,
        default=root / "data" / "composers.allowlist.json",
    )
    p.add_argument(
        "--denylist",
        type=Path,
        default=root / "data" / "composers.denylist.json",
    )
    p.add_argument(
        "--graylist",
        type=Path,
        default=root / "data" / "composers.graylist.json",
    )
    p.add_argument(
        "--manifest",
        type=Path,
        default=root / "data" / "manifest.csv",
    )
    p.add_argument(
        "--stats",
        type=Path,
        default=root / "data" / "stats.json",
    )
    p.add_argument(
        "--no-stats",
        action="store_true",
        help="Do not write data/stats.json",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if not args.csv.is_file():
        print(
            f"error: PDMX.csv not found at {args.csv}\n"
            "Download it first; see scripts/README.md for the exact Zenodo URL.",
            file=sys.stderr,
        )
        return 2
    stats_path = None if args.no_stats else args.stats
    gray = args.graylist if args.graylist.is_file() else None
    stats = run_filter(
        csv_path=args.csv,
        allowlist_path=args.allowlist,
        denylist_path=args.denylist,
        manifest_path=args.manifest,
        stats_path=stats_path,
        graylist_path=gray,
    )
    print_stats(stats)
    print(f"wrote {args.manifest}")
    if stats_path:
        print(f"wrote {stats_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
