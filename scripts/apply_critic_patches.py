#!/usr/bin/env python3
"""Apply critic JSON patches to an SMF Type 1 MIDI file.

Critic emits; this script applies. Maestro owns first-pass arrange and
anything the schema cannot express. Coordinator owns the job card.

Fail closed: unknown op, unknown desk name, desk missing from the MIDI,
missing required args, or start >= end in tick_range.

    python3 scripts/apply_critic_patches.py \
      --midi IN.mid --patches patches.json --out OUT.mid
    python3 scripts/apply_critic_patches.py \
      --midi IN.mid --patches patches.json --dry-run
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    import mido
except ImportError as exc:  # pragma: no cover
    raise SystemExit("error: mido is required (pip install mido)") from exc


OPS = (
    "set_duty",
    "transpose",
    "rest",
    "set_pitch",
    "set_velocity",
    "add_note",
    "shorten_to_beats",
)

PATCH_KEYS = {
    "id",
    "op",
    "desks",
    "tick_range",
    "bar_range",
    "duty",
    "semitones",
    "clip_lo",
    "clip_hi",
    "pitch",
    "velocity",
    "beats",
    "duration_ticks",
    "comment",
}

# Longest-first so "violin" wins over "vln" when splitting glued names.
_GLUED_PREFIXES = (
    "contrabassoon",
    "contrabass",
    "english horn",
    "bass trombone",
    "trombone",
    "trumpet",
    "clarinet",
    "bassoon",
    "piccolo",
    "timpani",
    "violin",
    "viola",
    "cello",
    "flute",
    "oboe",
    "horn",
    "harp",
    "continuo",
    "cymbal",
    "timp",
    "tpt",
    "vln",
    "vla",
    "bn",
    "hn",
    "fl",
    "ob",
    "cl",
    "vc",
    "cb",
    "tp",
)

_ABBREV = {
    "vln": "violin",
    "vla": "viola",
    "vc": "cello",
    "cb": "contrabass",
    "fl": "flute",
    "ob": "oboe",
    "cl": "clarinet",
    "bn": "bassoon",
    "hn": "horn",
    "tpt": "trumpet",
    "tp": "trumpet",
    "timp": "timpani",
}

_ROMAN = {"i": "1", "ii": "2", "iii": "3", "iv": "4"}

# token-key -> canonical track name (midi-contract.md)
_CANONICAL = {
    "piccolo": "Piccolo",
    "flute 1": "Flute 1",
    "flute 2": "Flute 2",
    "flute": "Flute 1",
    "oboe 1": "Oboe 1",
    "oboe 2": "Oboe 2",
    "oboe": "Oboe 1",
    "english horn": "English Horn",
    "clarinet 1": "Clarinet 1",
    "clarinet 2": "Clarinet 2",
    "clarinet": "Clarinet 1",
    "bassoon 1": "Bassoon 1",
    "bassoon 2": "Bassoon 2",
    "bassoon": "Bassoon 1",
    "contrabassoon": "Contrabassoon",
    "horn 1": "Horn 1",
    "horn 2": "Horn 2",
    "horn 3": "Horn 3",
    "horn 4": "Horn 4",
    "horn": "Horn 1",
    "trumpet 1": "Trumpet 1",
    "trumpet 2": "Trumpet 2",
    "trumpet": "Trumpet 1",
    "trombone 1": "Trombone 1",
    "trombone 2": "Trombone 2",
    "trombone": "Trombone 1",
    "bass trombone": "Bass Trombone",
    "tuba": "Tuba",
    "timpani": "Timpani",
    "cymbal": "Cymbal",
    "harp": "Harp",
    "continuo": "Continuo",
    "violin 1": "Violin I",
    "violin": "Violin I",
    "violin 2": "Violin II",
    "viola": "Viola",
    "cello": "Cello",
    "violoncello": "Cello",
    "contrabass": "Contrabass",
    "double bass": "Contrabass",
}


class PatchError(Exception):
    """Fail-closed validation or apply error."""


@dataclass
class Note:
    start: int
    end: int
    pitch: int
    velocity: int
    channel: int
    keep: bool = True


@dataclass
class Change:
    patch_id: str
    op: str
    desk: str
    detail: str


@dataclass
class Report:
    changes: list[Change] = field(default_factory=list)
    notes_touched: int = 0
    notes_removed: int = 0
    notes_added: int = 0

    def add(self, patch_id: str, op: str, desk: str, detail: str) -> None:
        self.changes.append(Change(patch_id, op, desk, detail))


def _prep_name(name: str) -> str:
    s = name.strip().lower().replace("&", " and ")
    s = s.replace("-", " ").replace("_", " ")
    s = re.sub(r"[./]", " ", s)
    s = re.sub(r"[^\w\s]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    if " " not in s:
        for prefix in _GLUED_PREFIXES:
            if s.startswith(prefix) and s != prefix:
                rest = s[len(prefix) :]
                if rest in _ROMAN or rest.isdigit():
                    s = prefix + " " + rest
                    break
    tokens: list[str] = []
    for tok in s.split():
        tok = _ABBREV.get(tok, tok)
        tok = _ROMAN.get(tok, tok)
        tokens.append(tok)
    return " ".join(tokens)


def canonical_desk(name: str) -> str | None:
    """Map a critic/track name to a midi-contract canonical desk, or None."""
    key = _prep_name(name)
    if not key:
        return None
    if key in _CANONICAL:
        return _CANONICAL[key]
    return None


def track_name_of(track: mido.MidiTrack) -> str:
    for msg in track:
        if msg.is_meta and msg.type == "track_name":
            return str(msg.name)
    return ""


def _int_pair(value: Any, label: str) -> tuple[int, int]:
    if not isinstance(value, list) or len(value) != 2:
        raise PatchError(f"{label} must be [start, end)")
    try:
        start = int(value[0])
        end = int(value[1])
    except (TypeError, ValueError) as exc:
        raise PatchError(f"{label} values must be integers") from exc
    if start < 0 or end < 0:
        raise PatchError(f"{label} values must be >= 0")
    if start >= end:
        raise PatchError(f"{label} must satisfy start < end (got {start}, {end})")
    return start, end


def _opt_int(patch: dict, key: str, lo: int | None = None, hi: int | None = None) -> int | None:
    if key not in patch or patch[key] is None:
        return None
    try:
        n = int(patch[key])
    except (TypeError, ValueError) as exc:
        raise PatchError(f"{key} must be an integer") from exc
    if lo is not None and n < lo:
        raise PatchError(f"{key} must be >= {lo}")
    if hi is not None and n > hi:
        raise PatchError(f"{key} must be <= {hi}")
    return n


def _req_number(patch: dict, key: str) -> float:
    if key not in patch or patch[key] is None:
        raise PatchError(f"op {patch.get('op')!r} requires {key}")
    try:
        n = float(patch[key])
    except (TypeError, ValueError) as exc:
        raise PatchError(f"{key} must be a number") from exc
    if n != n:  # NaN
        raise PatchError(f"{key} must be a number")
    return n


def validate_patch(patch: dict) -> None:
    if not isinstance(patch, dict):
        raise PatchError("each patch must be an object")
    extra = set(patch) - PATCH_KEYS
    if extra:
        raise PatchError(f"unknown patch field(s): {sorted(extra)}")
    pid = patch.get("id")
    if not isinstance(pid, str) or not pid.strip():
        raise PatchError("patch id must be a non-empty string")
    op = patch.get("op")
    if op not in OPS:
        raise PatchError(f"unknown op {op!r} (patch id={pid!r})")
    desks = patch.get("desks")
    if not isinstance(desks, list) or not desks or not all(isinstance(d, str) and d.strip() for d in desks):
        raise PatchError(f"patch {pid!r}: desks must be a non-empty array of strings")
    for desk in desks:
        if canonical_desk(desk) is None:
            raise PatchError(f"unknown desk name {desk!r} (patch id={pid!r})")
    _int_pair(patch.get("tick_range"), f"patch {pid!r} tick_range")
    if "bar_range" in patch and patch["bar_range"] is not None:
        _int_pair(patch["bar_range"], f"patch {pid!r} bar_range")
    if op == "set_duty":
        duty = _req_number(patch, "duty")
        if duty <= 0:
            raise PatchError(f"patch {pid!r}: duty must be > 0")
    elif op == "transpose":
        if "semitones" not in patch:
            raise PatchError(f"patch {pid!r}: transpose requires semitones")
        _opt_int(patch, "semitones")
        _opt_int(patch, "clip_lo", 0, 127)
        _opt_int(patch, "clip_hi", 0, 127)
        lo = patch.get("clip_lo")
        hi = patch.get("clip_hi")
        if lo is not None and hi is not None and int(lo) > int(hi):
            raise PatchError(f"patch {pid!r}: clip_lo > clip_hi")
    elif op == "set_pitch":
        _opt_int(patch, "pitch", 0, 127)
        if patch.get("pitch") is None:
            raise PatchError(f"patch {pid!r}: set_pitch requires pitch")
    elif op == "set_velocity":
        _opt_int(patch, "velocity", 0, 127)
        if patch.get("velocity") is None:
            raise PatchError(f"patch {pid!r}: set_velocity requires velocity")
    elif op == "add_note":
        _opt_int(patch, "pitch", 0, 127)
        if patch.get("pitch") is None:
            raise PatchError(f"patch {pid!r}: add_note requires pitch")
        if patch.get("velocity") is not None:
            _opt_int(patch, "velocity", 1, 127)
        has_dur = patch.get("duration_ticks") is not None
        has_beats = patch.get("beats") is not None
        if has_dur:
            n = _opt_int(patch, "duration_ticks", 1, None)
            if n is None:
                raise PatchError(f"patch {pid!r}: duration_ticks required")
        elif has_beats:
            beats = _req_number(patch, "beats")
            if beats <= 0:
                raise PatchError(f"patch {pid!r}: beats must be > 0")
        else:
            raise PatchError(f"patch {pid!r}: add_note requires duration_ticks or beats")
    elif op == "shorten_to_beats":
        beats = _req_number(patch, "beats")
        if beats <= 0:
            raise PatchError(f"patch {pid!r}: beats must be > 0")


def load_patches(path: Path) -> list[dict]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise PatchError(f"invalid JSON in {path}: {exc}") from exc
    if isinstance(data, list):
        raise PatchError("patches file must be an object with a 'patches' array, not a bare list")
    if not isinstance(data, dict) or "patches" not in data:
        raise PatchError("patches file must be an object with a 'patches' array")
    patches = data["patches"]
    if not isinstance(patches, list):
        raise PatchError("'patches' must be an array")
    seen: set[str] = set()
    for patch in patches:
        validate_patch(patch)
        pid = patch["id"]
        if pid in seen:
            raise PatchError(f"duplicate patch id {pid!r}")
        seen.add(pid)
    return patches


def extract_notes(track: mido.MidiTrack) -> tuple[list[Note], list[tuple[int, mido.Message]], int]:
    abs_t = 0
    other: list[tuple[int, mido.Message]] = []
    active: dict[tuple[int, int], list[tuple[int, int, int]]] = {}
    notes: list[Note] = []
    for msg in track:
        abs_t += int(msg.time)
        if msg.is_meta:
            if msg.type == "end_of_track":
                continue
            other.append((abs_t, msg.copy(time=0)))
            continue
        is_off = msg.type == "note_off" or (msg.type == "note_on" and msg.velocity == 0)
        is_on = msg.type == "note_on" and msg.velocity > 0
        if is_on:
            active.setdefault((msg.channel, msg.note), []).append(
                (abs_t, int(msg.velocity), int(msg.channel))
            )
        elif is_off:
            key = (int(msg.channel), int(msg.note))
            stack = active.get(key) or []
            if stack:
                start, vel, ch = stack.pop(0)
                notes.append(Note(start, abs_t, int(msg.note), vel, ch))
            # unmatched note-off dropped (nothing to keep)
        else:
            other.append((abs_t, msg.copy(time=0)))
    for (_ch, pitch), stack in active.items():
        for start, vel, ch in stack:
            end = max(abs_t, start + 1)
            notes.append(Note(start, end, int(pitch), vel, ch))
    return notes, other, abs_t


def rebuild_track(
    notes: list[Note],
    other: list[tuple[int, mido.Message]],
) -> mido.MidiTrack:
    events: list[tuple[int, int, mido.Message]] = []
    for tick, msg in other:
        events.append((tick, 1, msg))
    for note in notes:
        if not note.keep:
            continue
        end = max(note.end, note.start + 1)
        events.append(
            (
                note.start,
                2,
                mido.Message(
                    "note_on",
                    note=int(note.pitch),
                    velocity=int(note.velocity),
                    channel=int(note.channel),
                    time=0,
                ),
            )
        )
        events.append(
            (
                end,
                0,
                mido.Message(
                    "note_off",
                    note=int(note.pitch),
                    velocity=0,
                    channel=int(note.channel),
                    time=0,
                ),
            )
        )
    events.sort(key=lambda item: (item[0], item[1]))
    track = mido.MidiTrack()
    last = 0
    for tick, _prio, msg in events:
        delta = max(0, tick - last)
        track.append(msg.copy(time=delta))
        last = tick
    return track


def _in_range(onset: int, start: int, end: int) -> bool:
    return start <= onset < end


def _clip_end(note: Note, new_end: int, siblings: list[Note]) -> int:
    later = [
        n.start
        for n in siblings
        if n is not note
        and n.keep
        and n.pitch == note.pitch
        and n.channel == note.channel
        and n.start > note.start
    ]
    if later:
        new_end = min(new_end, min(later))
    return max(new_end, note.start + 1)


def _default_channel(notes: list[Note], other: list[tuple[int, mido.Message]]) -> int:
    for n in notes:
        if n.keep:
            return n.channel
    for _t, msg in other:
        if not msg.is_meta and hasattr(msg, "channel"):
            return int(msg.channel)
    return 0


def apply_one(
    patch: dict,
    desk: str,
    notes: list[Note],
    other: list[tuple[int, mido.Message]],
    ppq: int,
    report: Report,
) -> None:
    op = patch["op"]
    pid = patch["id"]
    start, end = _int_pair(patch["tick_range"], "tick_range")
    matched = [n for n in notes if n.keep and _in_range(n.start, start, end)]

    if op == "set_duty":
        duty = float(patch["duty"])
        dur = int(round(duty * ppq))
        if dur < 1:
            raise PatchError(f"patch {pid!r}: duty {duty} rounds to 0 ticks at PPQ {ppq}")
        for n in matched:
            new_end = _clip_end(n, n.start + dur, notes)
            report.add(pid, op, desk, f"pitch={n.pitch} {n.start}:{n.end} -> {n.start}:{new_end} (duty {duty})")
            n.end = new_end
            report.notes_touched += 1
        return

    if op == "shorten_to_beats":
        beats = float(patch["beats"])
        cap = int(round(beats * ppq))
        if cap < 1:
            raise PatchError(f"patch {pid!r}: beats {beats} rounds to 0 ticks at PPQ {ppq}")
        for n in matched:
            if (n.end - n.start) <= cap:
                continue
            new_end = _clip_end(n, n.start + cap, notes)
            report.add(pid, op, desk, f"pitch={n.pitch} {n.start}:{n.end} -> {n.start}:{new_end} (cap {beats} beats)")
            n.end = new_end
            report.notes_touched += 1
        return

    if op == "transpose":
        semi = int(patch["semitones"])
        lo = int(patch["clip_lo"]) if patch.get("clip_lo") is not None else 0
        hi = int(patch["clip_hi"]) if patch.get("clip_hi") is not None else 127
        for n in matched:
            raw = n.pitch + semi
            new_p = max(lo, min(hi, raw))
            report.add(pid, op, desk, f"{n.start}:{n.end} pitch {n.pitch} -> {new_p} (semitones {semi:+d})")
            n.pitch = new_p
            report.notes_touched += 1
        return

    if op == "set_pitch":
        pitch = int(patch["pitch"])
        for n in matched:
            report.add(pid, op, desk, f"{n.start}:{n.end} pitch {n.pitch} -> {pitch}")
            n.pitch = pitch
            report.notes_touched += 1
        return

    if op == "set_velocity":
        vel = int(patch["velocity"])
        for n in matched:
            report.add(pid, op, desk, f"{n.start}:{n.end} pitch={n.pitch} vel {n.velocity} -> {vel}")
            n.velocity = vel
            report.notes_touched += 1
        return

    if op == "rest":
        for n in matched:
            n.keep = False
            report.add(pid, op, desk, f"remove pitch={n.pitch} {n.start}:{n.end}")
            report.notes_removed += 1
        return

    if op == "add_note":
        pitch = int(patch["pitch"])
        vel = int(patch["velocity"]) if patch.get("velocity") is not None else 96
        if patch.get("duration_ticks") is not None:
            dur = int(patch["duration_ticks"])
        else:
            dur = int(round(float(patch["beats"]) * ppq))
        if dur < 1:
            raise PatchError(f"patch {pid!r}: add_note duration rounds to 0 ticks")
        onset = start
        new_end = onset + dur
        ch = _default_channel(notes, other)
        notes.append(Note(onset, new_end, pitch, vel, ch, keep=True))
        report.add(pid, op, desk, f"add pitch={pitch} vel={vel} {onset}:{new_end}")
        report.notes_added += 1
        return

    raise PatchError(f"unknown op {op!r}")  # unreachable after validate


def index_tracks(mf: mido.MidiFile) -> dict[str, list[int]]:
    """canonical desk -> track indices (conductor / unnamed skipped)."""
    by_canon: dict[str, list[int]] = {}
    for i, track in enumerate(mf.tracks):
        raw = track_name_of(track)
        if not raw:
            continue
        canon = canonical_desk(raw)
        if canon is None:
            continue
        by_canon.setdefault(canon, []).append(i)
    return by_canon


def apply_patches(
    midi_path: Path,
    patches: list[dict],
    out_path: Path | None,
    dry_run: bool = False,
) -> Report:
    mf = mido.MidiFile(str(midi_path))
    ppq = int(mf.ticks_per_beat)
    by_canon = index_tracks(mf)
    report = Report()

    parsed: dict[int, tuple[list[Note], list[tuple[int, mido.Message]]]] = {}

    for patch in patches:
        for desk_raw in patch["desks"]:
            canon = canonical_desk(desk_raw)
            if canon is None:
                raise PatchError(f"unknown desk name {desk_raw!r} (patch id={patch['id']!r})")
            idxs = by_canon.get(canon) or []
            if not idxs:
                raise PatchError(
                    f"desk {desk_raw!r} (canonical {canon!r}) not in MIDI track names "
                    f"(patch id={patch['id']!r})"
                )
            for idx in idxs:
                if idx not in parsed:
                    notes, other, _abs = extract_notes(mf.tracks[idx])
                    parsed[idx] = (notes, other)
                notes, other = parsed[idx]
                apply_one(patch, canon, notes, other, ppq, report)

    if dry_run:
        return report

    if out_path is None:
        raise PatchError("--out is required unless --dry-run")

    for idx, (notes, other) in parsed.items():
        mf.tracks[idx] = rebuild_track(notes, other)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    mf.save(str(out_path))
    return report


def format_report(report: Report, dry_run: bool) -> str:
    lines: list[str] = []
    current = None
    for ch in report.changes:
        key = (ch.patch_id, ch.op)
        if key != current:
            lines.append(f"PATCH {ch.patch_id}  {ch.op}")
            current = key
        lines.append(f"  {ch.desk}  {ch.detail}")
    if not report.changes:
        lines.append("no matching notes (patches applied, zero hits)")
    summary = (
        f"touched={report.notes_touched} removed={report.notes_removed} "
        f"added={report.notes_added}"
    )
    if dry_run:
        lines.append(f"dry-run; would change: {summary}")
    else:
        lines.append(f"applied: {summary}")
    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Apply critic JSON patches to an SMF Type 1 MIDI file."
    )
    p.add_argument("--midi", type=Path, required=True, help="Input .mid")
    p.add_argument("--patches", type=Path, required=True, help="patches.json")
    p.add_argument("--out", type=Path, help="Output .mid (required unless --dry-run)")
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would change; do not write --out",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if not args.midi.is_file():
        print(f"error: MIDI not found: {args.midi}", file=sys.stderr)
        return 2
    if not args.patches.is_file():
        print(f"error: patches not found: {args.patches}", file=sys.stderr)
        return 2
    if not args.dry_run and args.out is None:
        print("error: --out is required unless --dry-run", file=sys.stderr)
        return 2
    try:
        patches = load_patches(args.patches)
        report = apply_patches(args.midi, patches, args.out, dry_run=args.dry_run)
    except PatchError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    sys.stdout.write(format_report(report, dry_run=args.dry_run))
    if not args.dry_run and args.out is not None:
        print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
