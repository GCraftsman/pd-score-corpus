# Legal notes (not legal advice)

This file is a working memo for the film-scoring app that consumes this
corpus. **It is not legal advice.** It does not create an attorney–client
relationship. It does not claim that any file, encoding, stitched excerpt,
MIDI export, or rendered cue is “cleared for film,” “cleared for
commercial use,” or free of third-party rights. A qualified lawyer in the
relevant territories must review the stack before shipping or monetizing.

Date of this memo: 2 September 2026.

## 1. Layers: composition vs edition vs recording vs compilation

Copyright in music is stacked. Mixing up the layers is how “it’s on
MuseScore as public domain” turns into a bad cue sheet.

1. **Musical composition (the notes).** Melody, harmony, rhythm as
   authored. In the US, duration depends on publication date and, for
   newer/unpublished works, the author’s death date. See US Copyright
   Office Circular 15A, *Duration of Copyright*
   (https://www.copyright.gov/circs/circ15a.pdf). As of Public Domain Day
   2026, US works *published* in 1930 or earlier are in the public domain
   (https://web.law.duke.edu/cspd/publicdomainday/2026/). That is a
   publication-year rule, not a composer-death-year rule.
2. **Edition / engraving / arrangement.** A new, copyrightable editorial
   layer (fingerings, unique realizations, newly composed inner voices,
   a distinct piano reduction that adds material) can belong to the
   editor even when the underlying composition is public domain. A
   faithful copy of PD notes generally does not create a new composition
   copyright in the notes themselves (*Feist Publications, Inc. v. Rural
   Telephone Service Co.*, 499 U.S. 340 (1991): facts and public-domain
   material are not original; thin originality is required for a
   compilation copyright — https://www.law.cornell.edu/supremecourt/text/499/340).
3. **Sound recording (the master).** A recorded performance is a separate
   work. Public-domain *notes* do not make a Deutsche Grammophon (or
   MuseScore-synth, or sample-library) master free to ship.
4. **Compilation / database.** Selecting and arranging many scores can
   carry a thin compilation copyright if the selection is original.
   PDMX’s authors describe the dataset compilation as CC-BY; this repo
   CC0s *our* selection/manifest/scripts. That does not change the status
   of any underlying encoding.

The app should treat PDMX rows as **symbolic encodings of (claimed) PD
compositions**, not as licensed masters and not as a lawyer-vetted catalog.

## 2. Why a death-date allowlist, not PDMX license tags alone

PDMX includes only scores whose MuseScore uploaders declared **CC0** or
**Public Domain Mark** (paper: https://arxiv.org/abs/2409.10831;
HTML v2: https://arxiv.org/html/2409.10831v2). That is an *uploader
declaration*, not a chain-of-title search.

v1 of this corpus therefore **intersects** PDMX’s license filter with a
composer death-date allowlist: the composer died **1908 or earlier**.
Rationale:

- EU and many other territories use **life + 70 years**. Death in 1908
  ⇒ term ran through 1978 ⇒ public domain from 1 January 1979, for the
  composition, assuming no other rightsholder.
- The US publication-year clock (95 years from publication for
  pre-1978 published works) is *stricter* for anything first published
  after 1930. A 1908 death date makes it likely that the composer’s
  *lifetime publications* predate 1931, but it does not prove that a
  particular MuseScore file encodes a pre-1931 edition with no new
  copyrightable arrangement.
- License tags on a score-sharing site are noisy. PDMX itself documents
  a 12.29% public-vs-internal license conflict (see §4).
- Soundtrack, anime, and living-composer names still appear in a
  “public domain” scrape. The denylist exists because of that.

Graylist composers (Saint-Saëns 1921, Mahler 1911, Debussy 1918, Puccini
1924, Ravel 1937, Holst 1934, Elgar 1934, Rachmaninoff 1943) are **not**
in v1. Some of their *US-published-in-or-before-1930* works are now PD
in the US; later publications, unpublished works, and EU life+70 status
are not uniform. That is a lawyer/cataloguing job, not a CSV heuristic.

## 3. CC0 vs Public Domain Mark

- **CC0 1.0** (https://creativecommons.org/publicdomain/zero/1.0/legalcode)
  is a waiver (with a public-license fallback) by *someone who claims to
  own* copyright. An uploader can CC0 *their* encoding or original; they
  cannot waive a third party’s composition copyright.
- **Public Domain Mark 1.0**
  (https://creativecommons.org/publicdomain/mark/1.0/) is a *label* that
  the work is already in the public domain. It is not a license grant.
  It is only as good as the labeler’s research.

PDMX stores the declared license in `license` / `license_url`. Typical
values in the dump are `publicdomain` (PDM) and `cc0`. This corpus keeps
the original strings on each manifest row. It does not upgrade PDM to
CC0 or vice versa.

## 4. The 12.29% `license_conflict` problem

From the PDMX GitHub README and the Zenodo v9 record
(https://github.com/pnlong/PDMX, https://zenodo.org/records/15571083):

> Upon further use of the PDMX dataset, we discovered a discrepancy
> between the public-facing copyright metadata on the MuseScore website
> and the internal copyright data of the MuseScore files themselves,
> which affected 31,221 (12.29% of) songs. … We have noted files with
> conflicting internal licenses in the `license_conflict` column of
> PDMX. We recommend using the `no_license_conflict` subset of PDMX
> (which still includes 222,856 songs) moving forward.

The v1 filter **requires** `subset:no_license_conflict` (equivalently,
`no_license_conflict` true). Conflict rows are dropped, even when the
composer is allowlisted. That is a risk reduction, not a guarantee that
the remaining internal files match the public tag.

## 5. MuseScore Terms of Use vs Zenodo redistribution

PDMX encodings exist because the authors scraped MuseScore.com
(acknowledged in the paper and README; MetaScore/Dong is the requested
second citation). MuseScore’s Terms of Use
(https://musescore.com/legal/terms) restrict, among other things,
automated access/download of content and redistribution of content
downloaded or printed from the service. `robots.txt` disallows
`/score/*/download/*`.

**Uncertainty (flag, do not paper over):**

- This project does **not** scrape MuseScore and does **not** ship a
  live MuseScore client.
- It *does* contemplate redistributing a **curated subset of files that
  already appear in the Zenodo dump of PDMX** (DOI
  10.5281/zenodo.15571083), which PDMX authors published under a CC-BY
  compilation license with per-file CC0/PDM tags.
- Whether MuseScore ToS bind downstream users of a third-party research
  dump, whether CC0/PDM tags on user uploads survive ToS, and whether
  an app may fetch MXL/MID from Zenodo at build time, are questions a
  lawyer must answer. Possible outcomes range from “Zenodo+CC0/PDM is
  enough” to “only regenerate encodings from truly PD sources” to
  “need MuseScore’s permission.”

Until that review happens: prefer build-time or server-side fetch of
the Zenodo subset; do not scrape MuseScore.com; do not claim an
affiliation with MuseScore or PDMX.

## 6. Piano reductions of PD works

Piano-only encodings are **first-class** in this corpus. The app’s
piano-to-orchestra step is *the app’s* arrangement skill sitting on top
of PD notes; it is not a property of the MIDI file.

- A faithful piano *encoding* of a public-domain composition (the same
  pitches and durations) is, at the composition layer, still PD notes.
- A labeled **arrangement of** a work, a “piano transcription” that
  adds substantial new material, or an edition with a living arranger
  named in the title, may be a new copyrighted arrangement. The filter
  drops title/tag hits for `arrangement of` and `arranged from`, and
  drops `is_original == true` uploader originals. That is conservative
  and incomplete.
- Fingerings, editorial slurs, realized ornaments, and MuseScore-specific
  styling should be treated as *not needed* by the app (see README).
  Extract pitch, duration, and voice.

## 7. New MIDI / sample performance; no third-party master

Exporting SMF Type 1 from the app is a **new symbolic performance
stream** produced by the product, not a copy of someone else’s audio
master. Using it in Logic Pro / GarageBand via File → Open does not
import a commercial recording.

If the app (or the user) later renders audio:

- that render is a new sound recording (owned according to the app’s
  own terms / the user’s work-for-hire setup);
- it still must not copy a third-party master, YouTube rip, or
  MuseScore “custom audio” attachment (`has_custom_audio` in PDMX).

v1 does not ship audio.

## 8. Sample-library EULAs (if the app renders audio)

If a future version renders MIDI through Kontakt, Spitfire, BBCSO,
Audio Modeling, etc., the **sample library EULA** is an independent
permission layer. Many libraries:

- allow commercial soundtrack use of *rendered* audio;
- forbid redistributing the raw samples, and sometimes forbid using the
  library to build a competing sampler or a cloud instrument;
- require credit or a specific cue-sheet instrument name.

PD notes + SMF export do not override a sample-lib contract. Keep
rendering server-side or in the user’s DAW so the app is not
redistributing sample payloads.

## 9. Cue-sheet language (draft; lawyer must rewrite)

Do **not** register a PD composition as an original work. Do **not**
list MuseScore, PDMX, or this corpus as a publisher of the composition.

A conservative cue-sheet sketch for a stitched, newly performed cue:

- **Composition title:** historical title of the PD work(s) used, plus
  “excerpt” / movement if applicable. If several works are stitched,
  list each underlying PD work.
- **Composer:** historical composer (public domain). Publisher: none /
  public domain. Society affiliation: n/a for the PD composition.
- **Arrangement (if the app orchestrated a piano encoding or the user
  edited notes):** “Arrangement by [production company / composer of
  record], based on public-domain source material.” Register the
  *arrangement* only to the extent it contains new original material,
  and only after counsel agrees that the delta is registrable.
- **Sound recording:** “New recording by [production], [year]. Not a
  licensed master. Source encodings: PDMX-derived symbolic files; no
  third-party commercial recording used.”
- **Do not write:** “cleared for film,” “MuseScore licensed,” or
  “PDMX certified.”

Performing-rights societies still want accurate work titles for PD
material so they do not collect composition royalties that are not due.
Wrong metadata is how PD Beethoven becomes a claim against the cue.

## 10. What a lawyer must still confirm

Before any commercial film/TV/game/trailer use, counsel should at least:

1. Confirm territorial public-domain status of each *composition*
   (US publication-year vs EU/UK life+70 vs other). Circular 15A and
   Duke Public Domain Day 2026 are starting points, not a catalog.
2. Decide whether MuseScore ToS, CC0/PDM uploader tags, and the Zenodo
   CC-BY compilation license, taken together, allow redistributing or
   fetching the MXL/MID bytes this app needs (§5).
3. Review residual `license_conflict` risk even after dropping the
   12.29% subset, and whether internal MuseScore file tags should be
   re-checked.
4. Review whether specific encodings are copyrightable **editions or
   arrangements** rather than faithful copies (§6), including piano
   reductions.
5. Confirm that SMF Type 1 exports and any sample-lib renders do not
   implicate a third-party master or EULA restriction (§7–8).
6. Rewrite cue-sheet / publishing / PRO language (§9) for the
   production’s chain of title.
7. Advise on trademark in titles (“Star Wars” is the obvious case; the
   filter already drops soundtrack keywords, which is not a trademark
   legal analysis).
8. Advise on whether the app’s own stitched output should be released
   as CC0 (the product’s current intent) and how that interacts with
   the user’s commission agreement.
9. Confirm that *Feist* thin-compilation theory is being relied on only
   for this repo’s manifest (which we CC0), not as a blanket “datasets
   are free” argument.

### Primary URLs

| Topic | URL |
| --- | --- |
| US duration (Circ. 15A) | https://www.copyright.gov/circs/circ15a.pdf |
| Duke Public Domain Day 2026 | https://web.law.duke.edu/cspd/publicdomainday/2026/ |
| PDMX paper | https://arxiv.org/abs/2409.10831 |
| PDMX paper HTML v2 | https://arxiv.org/html/2409.10831v2 |
| PDMX Zenodo v9 | https://zenodo.org/records/15571083 |
| PDMX GitHub (license-conflict note) | https://github.com/pnlong/PDMX |
| CC0 1.0 legal code | https://creativecommons.org/publicdomain/zero/1.0/legalcode |
| Public Domain Mark 1.0 | https://creativecommons.org/publicdomain/mark/1.0/ |
| *Feist* (Cornell LII) | https://www.law.cornell.edu/supremecourt/text/499/340 |
| MuseScore Terms of Use | https://musescore.com/legal/terms |
