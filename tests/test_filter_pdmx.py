#!/usr/bin/env python3
"""Unit tests for scripts/filter_pdmx.py (stdlib unittest, no pytest required)."""

from __future__ import annotations

import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import filter_pdmx as f  # noqa: E402

FIXTURE = ROOT / "tests" / "fixtures" / "pdmx_fixture.csv"
ALLOW = ROOT / "data" / "composers.allowlist.json"
DENY = ROOT / "data" / "composers.denylist.json"
GRAY = ROOT / "data" / "composers.graylist.json"


class NormalizeTests(unittest.TestCase):
    def test_accents_and_punctuation(self):
        self.assertEqual(f.normalize_name("Antonín Dvořák"), "antonin dvorak")
        self.assertEqual(f.normalize_name("J.S. Bach"), "j s bach")
        self.assertEqual(f.normalize_name("W.A. Mozart (1756-1791)"), "w a mozart")
        self.assertEqual(f.normalize_name("Johann Sebastian Bach (1685--1750)"), "johann sebastian bach")

    def test_empty(self):
        self.assertTrue(f.is_empty("NA"))
        self.assertTrue(f.is_empty(""))
        self.assertTrue(f.is_empty(None))
        self.assertFalse(f.is_empty("Bach"))


class AllowlistTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        entries = f.load_composer_list(ALLOW)
        cls.exact, cls.pairs = f.build_alias_index(entries)

    def hit(self, name: str) -> str | None:
        return f.match_allowlist(name, self.exact, self.pairs)

    def test_common_variants(self):
        self.assertEqual(self.hit("J. S. Bach"), "Johann Sebastian Bach")
        self.assertEqual(self.hit("JS Bach"), "Johann Sebastian Bach")
        self.assertEqual(self.hit("Bach"), "Johann Sebastian Bach")
        self.assertEqual(self.hit("Bach Johann Sebastian"), "Johann Sebastian Bach")
        self.assertEqual(self.hit("Ludvig van Beethoven"), "Ludwig van Beethoven")
        self.assertEqual(self.hit("Frédéric Chopin"), "Frederic Chopin")
        self.assertEqual(self.hit("W.A.Mozart"), "Wolfgang Amadeus Mozart")
        self.assertEqual(self.hit("P. I. Tchaikovsky"), "Pyotr Ilyich Tchaikovsky")
        self.assertEqual(self.hit("Antonín Dvořák"), "Antonin Dvorak")
        self.assertEqual(self.hit("Johann Strauss II"), "Johann Strauss II")
        self.assertEqual(self.hit("Händel"), "George Frideric Handel")
        self.assertEqual(self.hit("Rimsky-Korsakov"), "Nikolai Rimsky-Korsakov")

    def test_exclusions(self):
        self.assertIsNone(self.hit("C.P.E. Bach"))
        self.assertIsNone(self.hit("Carl Philipp Emanuel Bach"))
        self.assertIsNone(self.hit("Clara Schumann"))
        self.assertIsNone(self.hit("Richard Strauss"))
        self.assertIsNone(self.hit("Alessandro Scarlatti"))
        self.assertIsNone(self.hit("Claude Debussy"))
        self.assertIsNone(self.hit("Jacob Handl"))
        self.assertIsNone(self.hit("Jacobus Gallus"))
        self.assertIsNone(self.hit(""))
        self.assertIsNone(self.hit("NA"))


class DenylistTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        entries = f.load_composer_list(DENY)
        cls.exact, cls.pairs = f.build_alias_index(entries)

    def hit(self, name: str) -> str | None:
        return f.match_denylist_composer(name, self.exact, self.pairs)

    def test_named_composers(self):
        self.assertEqual(self.hit("Igor Stravinsky"), "Igor Stravinsky")
        self.assertEqual(self.hit("John Williams"), "John Williams")
        self.assertEqual(self.hit("Ralph Vaughan Williams"), "Ralph Vaughan Williams")
        self.assertEqual(self.hit("Richard Strauss"), "Richard Strauss")
        self.assertEqual(self.hit("Joe Hisaishi"), "Joe Hisaishi")
        self.assertIsNone(self.hit("Johann Strauss II"))
        self.assertIsNone(self.hit("William James Kirkpatrick"))


class PianoAndContentTests(unittest.TestCase):
    def test_piano_from_tags(self):
        row = {"n_tracks": "1", "tracks": "0", "tags": "piano-baroque"}
        self.assertTrue(f.classify_piano_only(row, 1))

    def test_not_piano_numeric_tracks(self):
        row = {"n_tracks": "1", "tracks": "0", "tags": "NA"}
        self.assertFalse(f.classify_piano_only(row, 1))

    def test_multi_track_not_piano_only(self):
        row = {"n_tracks": "4", "tracks": "0-1-2-3", "tags": "piano"}
        self.assertFalse(f.classify_piano_only(row, 4))

    def test_content_denylist(self):
        self.assertIsNotNone(f.content_denied({"title": "Star Wars movie soundtrack", "tags": "", "genres": "", "song_name": ""}))
        self.assertIsNotNone(f.content_denied({"title": "Arrangement of Handel Messiah", "tags": "NA", "genres": "NA", "song_name": "NA"}))
        self.assertIsNone(f.content_denied({"title": "Epic Overture", "tags": "", "genres": "", "song_name": ""}))
        self.assertIsNotNone(f.content_denied({"title": "Trailer cue", "tags": "epic hybrid", "genres": "", "song_name": ""}))


class FixtureFilterTests(unittest.TestCase):
    def test_fixture_keeps_expected_rows(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            manifest = tmp_path / "manifest.csv"
            stats_path = tmp_path / "stats.json"
            stats = f.run_filter(
                csv_path=FIXTURE,
                allowlist_path=ALLOW,
                denylist_path=DENY,
                manifest_path=manifest,
                stats_path=stats_path,
                graylist_path=GRAY,
            )
            self.assertEqual(stats["kept"], 5)
            self.assertEqual(stats["piano_only"], 2)  # Bach piano tags + Mozart piano tags
            ids = []
            with manifest.open(newline="", encoding="utf-8") as fh:
                for row in csv.DictReader(fh):
                    ids.append(row["pdmx_id"])
            self.assertEqual(
                ids,
                [
                    "QmKeepBachPiano",
                    "QmKeepBeethovenOrch",
                    "QmKeepDvorak",
                    "QmKeepStraussII",
                    "QmKeepMozartDates",
                ],
            )
            loaded = json.loads(stats_path.read_text(encoding="utf-8"))
            self.assertIn("Claude Debussy", loaded["graylist_seen_but_dropped"])
            self.assertGreater(loaded["drop_reasons"].get("license_conflict", 0), 0)
            self.assertGreater(loaded["drop_reasons"].get("empty_composer", 0), 0)
            self.assertGreater(loaded["drop_reasons"].get("is_original", 0), 0)
            self.assertGreater(loaded["drop_reasons"].get("denylist_composer", 0), 0)
            self.assertGreater(loaded["drop_reasons"].get("denylist_content", 0), 0)


if __name__ == "__main__":
    unittest.main()
