#!/usr/bin/env python3
"""Tests for scripts/apply_critic_patches.py (stdlib unittest, no pytest)."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import mido

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import apply_critic_patches as ap  # noqa: E402

FIXTURE_MIDI = ROOT / "tests" / "fixtures" / "critic_patch_input.mid"
FIXTURE_PATCHES = ROOT / "tests" / "fixtures" / "critic_patch.json"
SCRIPT = ROOT / "scripts" / "apply_critic_patches.py"


def notes_of(path: Path, desk: str = "Violin I") -> list[tuple[int, int, int, int]]:
    """Return (start, end, pitch, velocity) for a named desk, onset-sorted."""
    mf = mido.MidiFile(str(path))
    out: list[tuple[int, int, int, int]] = []
    for track in mf.tracks:
        if ap.canonical_desk(ap.track_name_of(track)) != ap.canonical_desk(desk):
            continue
        notes, _other, _t = ap.extract_notes(track)
        for n in notes:
            if n.keep:
                out.append((n.start, n.end, n.pitch, n.velocity))
    out.sort()
    return out


class CanonicalDeskTests(unittest.TestCase):
    def test_aliases(self):
        self.assertEqual(ap.canonical_desk("Violin I"), "Violin I")
        self.assertEqual(ap.canonical_desk("vln i"), "Violin I")
        self.assertEqual(ap.canonical_desk("VlnI"), "Violin I")
        self.assertEqual(ap.canonical_desk("Violin 1"), "Violin I")
        self.assertEqual(ap.canonical_desk("Vln II"), "Violin II")
        self.assertEqual(ap.canonical_desk("Vla"), "Viola")
        self.assertEqual(ap.canonical_desk("Vc"), "Cello")
        self.assertEqual(ap.canonical_desk("Cb"), "Contrabass")
        self.assertEqual(ap.canonical_desk("Timp"), "Timpani")
        self.assertEqual(ap.canonical_desk("Fl 1"), "Flute 1")
        self.assertEqual(ap.canonical_desk("Bn2"), "Bassoon 2")

    def test_unknown_name(self):
        self.assertIsNone(ap.canonical_desk("Banjo"))
        self.assertIsNone(ap.canonical_desk("strings"))
        self.assertIsNone(ap.canonical_desk("GM pad"))


class FixtureCliTests(unittest.TestCase):
    def test_cli_changes_duty_and_pitch(self):
        self.assertTrue(FIXTURE_MIDI.is_file(), "missing critic_patch_input.mid")
        self.assertTrue(FIXTURE_PATCHES.is_file(), "missing critic_patch.json")
        before = notes_of(FIXTURE_MIDI)
        self.assertEqual(len(before), 4)
        # three fused 8ths at duty 0.498 (239 ticks) then one long
        self.assertEqual([n[1] - n[0] for n in before[:3]], [239, 239, 239])
        self.assertEqual(before[3][2], 75)  # Eb5

        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "out.mid"
            proc = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--midi",
                    str(FIXTURE_MIDI),
                    "--patches",
                    str(FIXTURE_PATCHES),
                    "--out",
                    str(out),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertTrue(out.is_file())
            after = notes_of(out)

        self.assertEqual(len(after), 4)
        duty_ticks = [n[1] - n[0] for n in after[:3]]
        self.assertEqual(duty_ticks, [108, 108, 108])  # 0.225 * 480
        for n in after[:3]:
            self.assertAlmostEqual((n[1] - n[0]) / 480, 0.225, places=3)
        self.assertEqual(after[3][2], 63)  # transpose -12, Eb5 -> Eb4
        self.assertEqual(after[3][0], 960)
        self.assertEqual([n[2] for n in after[:3]], [67, 67, 67])

    def test_dry_run_does_not_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "should-not-exist.mid"
            proc = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--midi",
                    str(FIXTURE_MIDI),
                    "--patches",
                    str(FIXTURE_PATCHES),
                    "--out",
                    str(out),
                    "--dry-run",
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertFalse(out.exists())
            self.assertIn("dry-run", proc.stdout)
            self.assertIn("detach-8ths", proc.stdout)
            self.assertIn("transpose-long", proc.stdout)


class FailClosedTests(unittest.TestCase):
    def _run(self, patches: dict, midi: Path | None = None) -> subprocess.CompletedProcess:
        midi = midi or FIXTURE_MIDI
        with tempfile.TemporaryDirectory() as tmp:
            pdir = Path(tmp)
            patch_path = pdir / "p.json"
            patch_path.write_text(json.dumps(patches), encoding="utf-8")
            out = pdir / "out.mid"
            return subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--midi",
                    str(midi),
                    "--patches",
                    str(patch_path),
                    "--out",
                    str(out),
                ],
                check=False,
                capture_output=True,
                text=True,
            )

    def test_unknown_op(self):
        proc = self._run(
            {
                "patches": [
                    {
                        "id": "bad-op",
                        "op": "braam",
                        "desks": ["Violin I"],
                        "tick_range": [0, 480],
                    }
                ]
            }
        )
        self.assertEqual(proc.returncode, 2)
        self.assertIn("unknown op", proc.stderr)

    def test_unknown_desk_name(self):
        proc = self._run(
            {
                "patches": [
                    {
                        "id": "bad-desk",
                        "op": "rest",
                        "desks": ["Banjo"],
                        "tick_range": [0, 480],
                    }
                ]
            }
        )
        self.assertEqual(proc.returncode, 2)
        self.assertIn("unknown desk name", proc.stderr)

    def test_known_desk_missing_from_midi(self):
        proc = self._run(
            {
                "patches": [
                    {
                        "id": "no-timp",
                        "op": "rest",
                        "desks": ["Timpani"],
                        "tick_range": [0, 480],
                    }
                ]
            }
        )
        self.assertEqual(proc.returncode, 2)
        self.assertIn("not in MIDI", proc.stderr)

    def test_bare_array_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            pdir = Path(tmp)
            patch_path = pdir / "p.json"
            patch_path.write_text("[]", encoding="utf-8")
            proc = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--midi",
                    str(FIXTURE_MIDI),
                    "--patches",
                    str(patch_path),
                    "--dry-run",
                ],
                check=False,
                capture_output=True,
                text=True,
            )
        self.assertEqual(proc.returncode, 2)
        self.assertIn("patches", proc.stderr)


class RestAndAddTests(unittest.TestCase):
    def test_rest_then_add_note(self):
        patches = [
            {
                "id": "rest-first",
                "op": "rest",
                "desks": ["Vln I"],
                "tick_range": [0, 240],
            },
            {
                "id": "add-g3",
                "op": "add_note",
                "desks": ["Violin I"],
                "tick_range": [0, 108],
                "pitch": 55,
                "velocity": 80,
                "beats": 0.225,
            },
        ]
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "out.mid"
            report = ap.apply_patches(FIXTURE_MIDI, patches, out, dry_run=False)
            self.assertEqual(report.notes_removed, 1)
            self.assertEqual(report.notes_added, 1)
            after = notes_of(out)
        self.assertEqual(after[0], (0, 108, 55, 80))
        self.assertEqual(len(after), 4)  # dropped one, added one, three remaining


if __name__ == "__main__":
    unittest.main()
