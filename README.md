# pd-score-corpus

Curated **public-domain symbolic music** (MIDI + MusicXML) drawn from
[PDMX](https://arxiv.org/abs/2409.10831) for Michael Lacasse’s
film-scoring app.

The app **stitches exact parts** from 18th–19th century works, treats
**piano-only scores as first-class** (the app arranges piano into
multi-instrument textures), and **exports SMF Type 1** for Logic Pro /
GarageBand.

## v1 numbers (PDMX Zenodo v9)

| | count |
| --- | ---: |
| PDMX rows scanned | 254,077 |
| **kept** | **3,730** |
| piano-only (`n_tracks==1` + piano tag) | 186 |
| multi-track | 1,830 |
| single-track, not tagged piano | 1,714 |
| license-conflict drops | 31,221 |
| graylist drops (Debussy, Ravel, …) | 323 |

Top composers in the keep set: Bach 1,190; Mozart 380; Beethoven 279; Handel 227; Purcell 179; Chopin 157. All 40 allowlisted composers appear at least once.

Piano-only is sparse because PDMX v9 `tracks` is numeric part IDs, not instrument names — classification is tag-driven. Many of the 1,714 untagged single-track files are likely keyboard encodings; treat `is_piano_only` as a lower bound.

This repository is the *selector* plus the **v1 MIDI bytes**:
allow/deny/gray composer lists, a filter over `PDMX.csv`, a manifest,
and `midi/` (3,730 Standard MIDI files, ~92 MB, same ids as the
manifest `mid` column). It is not a 14 GB PDMX mirror, and it is
**not a clearance catalog**. MusicXML is not checked in; unpack
`mxl.tar.gz` from Zenodo if you need it (see scripts/README.md).

**Do not claim these files are cleared for film.** Read [LEGAL.md](LEGAL.md).

## What the app should do with a row

1. **Resolve bytes from the PDMX dump** using the paths on the manifest
   (`mxl`, `mid`, optionally MusicRender `path`). Fetch at **build time**
   or **server-side**. Do not scrape MuseScore.com. Do not ship the
   whole dump inside a client binary if you can avoid it — size, update
   cadence, and the MuseScore-ToS-vs-Zenodo uncertainty in LEGAL.md §5
   all argue for a server or build step.
2. **Load MusicXML (preferred) or MIDI.** MusicXML keeps voices, bar
   lines, tempo text, and section marks that SMF Type 0 would flatten.
   MIDI is the fallback when `mxl` is `N/A` (PDMX notes 42 corrupted
   sources; v1 also requires `subset:all_valid`).
3. **Extract pitch, duration, and voice.** Ignore fingerings, editorial
   marks, MuseScore styling, realized ornaments you did not ask for, and
   lyrics unless a future vocal feature needs them.
4. **Stitch excerpts.** Concatenate or overlay selected measures/parts
   from one or more allowlisted works. The composition layer remains
   public-domain *notes* of the named composer(s); the stitch is the
   product’s editorial act.
5. **Export SMF Type 1** (multiple tracks, not Type 0). Write:
   - track names (instrument / extracted part),
   - tempo map,
   - markers (rehearsal letters, user edit points).
6. **User opens the file in Logic Pro or GarageBand** via File → Open
   (or drag onto the arrange window). This is a new MIDI file, not a
   licensed audio master.
7. **Piano → orchestra is an app skill**, not a property of the source
   file. Rows with `is_piano_only=true` are eligible for that pipeline
   *and* for literal piano use. Multi-track allowlisted rows are kept
   too — use them when the user wants the original parts.

If the product’s own stitched MIDI/MusicXML is original enough to
copyright, the current intent is to **CC0 the app’s stitched output**
so downstream film use does not grow a second composition claim on PD
material. That is a product policy; counsel still has to bless it
(LEGAL.md §10).

## v1 filter (short)

`scripts/filter_pdmx.py` keeps a PDMX row only if **all** of these hold:

1. `subset:no_license_conflict` is true (drops the documented 12.29%
   public-vs-internal license mismatch).
2. `subset:all_valid` is true when the column exists (MXL, PDF, and MID
   all present; 42 PDMX files fail this).
3. `composer_name` is non-empty and matches
   [`data/composers.allowlist.json`](data/composers.allowlist.json)
   (death year ≤ 1908, with aliases).
4. `is_original` is false (uploader originals out; we want encodings of
   historical works).
5. not `is_draft`, not `has_paywall`.
6. title / tags / genres / song_name do not hit the soundtrack / film /
   anime / “arrangement of” denylist; composer is not on
   [`data/composers.denylist.json`](data/composers.denylist.json).
7. Piano-only is *classified*, not used as a drop rule:
   `n_tracks == 1` and (`tracks` looks like piano/pianoforte/kbd **or**
   `tags` contain piano). PDMX v9 `tracks` is numeric part IDs, so in
   practice this is tag-driven.

Graylist composers (Debussy, Ravel, …) live in
[`data/composers.graylist.json`](data/composers.graylist.json) and are
**not** in v1.

How to download `PDMX.csv` / `mid.tar.gz` and run the filter:
**[scripts/README.md](scripts/README.md)**. Exact Zenodo URLs were
fetched from https://zenodo.org/records/15571083 (v9, 1 June 2025).

## Cite

Please cite **both** papers, as the PDMX authors request. See
[CITATION.cff](CITATION.cff).

```bibtex
@inproceedings{long2024pdmx,
  author={Long, Phillip and Novack, Zachary and Berg-Kirkpatrick, Taylor and McAuley, Julian},
  booktitle={ICASSP 2025 - 2025 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)},
  title={{PDMX}: A Large-Scale Public Domain MusicXML Dataset for Symbolic Music Processing},
  year={2025},
  pages={1-5},
  doi={10.1109/ICASSP49660.2025.10890217}
}

@article{xu2024generating,
  title={Generating Symbolic Music from Natural Language Prompts using an LLM-Enhanced Dataset},
  author={Xu, Weihan and McAuley, Julian and Berg-Kirkpatrick, Taylor and Dubnov, Shlomo and Dong, Hao-Wen},
  journal={arXiv preprint arXiv:2410.02084},
  year={2024}
}
```

Dataset: Zenodo v9, DOI [10.5281/zenodo.15571083](https://doi.org/10.5281/zenodo.15571083).
Code: [pnlong/PDMX](https://github.com/pnlong/PDMX) (MIT).
Demo: https://pnlong.github.io/PDMX.demo/

## License

- **This repo’s** lists, scripts, docs, and derived `data/manifest.csv`:
  [CC0 1.0](LICENSE).
- **Individual encodings:** CC0 or Public Domain Mark as tagged by the
  MuseScore uploader and copied into PDMX (see each manifest row).
- **PDMX compilation:** CC-BY 4.0 per the Zenodo record; cite Long et al.

[NOTICE](NOTICE) · [LEGAL.md](LEGAL.md)
