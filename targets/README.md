# Target sound (gold audio)

Gold **recordings** for a future comparator bot (name TBD). The bot
listens to a Music Maestro arrangement (MIDI rendered to audio) against
a file in this tree and returns **one or two concrete improvements**
for the next Maestro pass.

This is not a film-clearance catalog. Recordings here are only those we
can redistribute (CC0 / CC-BY / CC-BY-SA / PD sound recording). The
*composition* is public domain; a modern *performance* or *orchestration*
may still be copyrighted — we do not ship label/YouTube rips.

## Layout

```
targets/
  README.md                 ← you are here
  {work-slug}/
    source.json             ← pairing to corpus MIDI + license
    target.ogg              ← or .wav / .flac / .mp3
    LICENSE                 ← verbatim license of the recording
    notes.md                ← optional: what “match” means for this work
```

`work-slug` is lowercase ASCII, e.g. `chopin-op28-20`, `bach-bwv846`.

## `source.json`

```json
{
  "work_slug": "chopin-op28-20",
  "composer": "Frederic Chopin",
  "work_title": "Prelude in C minor, Op. 28 No. 20",
  "corpus_pdmx_ids": ["QmdHbV5ya1MwSJnJNdSXw4UmKNU4JjtrBpSiFKMRS4F3rc"],
  "corpus_midi": "midi/…/QmdHbV5ya1MwSJnJNdSXw4UmKNU4JjtrBpSiFKMRS4F3rc.mid",
  "maestro_experiment": "EXP-01",
  "target_file": "target.ogg",
  "target_kind": "orchestra | strings | chamber | piano | mixed",
  "target_is_arrangement": true,
  "arrangement_copyright": "unknown | pd | cc | all-rights-reserved",
  "recording": {
    "performer": "",
    "ensemble": "",
    "year": null,
    "url": "",
    "license": "CC0-1.0 | CC-BY-4.0 | CC-BY-SA-4.0 | PD-US-recording",
    "attribution": "",
    "format": "ogg",
    "sample_rate_hz": 44100
  },
  "compare": {
    "render_maestro_with": "fluidsynth-gm",
    "align": "start",
    "criteria": ["melody-register", "bass-weight", "texture-density", "articulation", "tempo-feel"]
  }
}
```

`target_kind` tells the comparator what a match even means:

| kind | Fair comparison |
| --- | --- |
| `orchestra` / `strings` | Maestro orchestral MIDI vs this recording (the intended loop) |
| `piano` | Only useful for “did we destroy the piece”; **not** a voicing target |
| `chamber` | Small-ensemble Maestro cards |

If `target_is_arrangement` is true, matching *orchestration choices*
(who plays the tune, how thick the midrange is) is in-scope.
Matching *that specific conductor’s rubato or hall reverb* is not
the first goal — see criteria below.

## Comparator contract (what the bot must return)

Input:

1. Path to Maestro MIDI (under `arrangements/`) or a rendered wav.
2. Path to `targets/{slug}/` (this folder).

If given MIDI, render with **FluidSynth + GM** at the target’s sample
rate (default 44.1 kHz, stereo). Do not render through Spitfire/BBCSO
for the scored loop unless the human later substitutes that render
locally — those EULAs do not belong in the repo.

Process (suggested, not sacred):

1. Loudness-normalize both sides (ITU-R BS.1770 / ffmpeg loudnorm) so
   the critic is not just saying “turn it up.”
2. Time-align (pad/trim to the shorter; or beat-track if tempos differ
   by > 3%). If alignment fails, say so and stop — do not invent a score.
3. Compare **a few** interpretable features, not a black-box embedding
   as the only output:
   - melody register (skyline median MIDI vs spectral centroid of the
     target’s mid/high band)
   - bass weight (energy below ~150 Hz)
   - texture density (onset rate / spectral flatness)
   - articulation (note length vs target RMS envelope)
   - tempo / rubato (global BPM, not microtiming in v1)
4. Optionally a small CLAP/open-l3 distance as a *tie-break*, never as
   the only sentence.

**Output — exactly one or two bullets**, each an instruction Music
Maestro can apply on the next pass, e.g.:

- `Raise Violin I an octave in bars 1–8; target melody sits ~C5 not G3.`
- `Thin inner strings: too many simultaneous mid-register notes vs target.`
- `Bass is light: double cello with contrabass on downbeats.`
- `Hits late: move timp to barline (marker HIT 1).`

Do **not** return a 20-line essay. Do **not** say “make it more cinematic.”
Do **not** ask Maestro to copy a copyrighted arrangement’s unique inner
voices if that would be reproducing a protected orchestration — stay at
the level of register, density, bass, articulation, tempo.

Write the two bullets into `arrangements/NOTES.md` under the experiment
id, tagged `comparator:`.

## Cycle

```
Music Maestro (EXP-n) → arrangements/*.mid
        ↓ render GM
Comparator vs targets/{slug}/target.*
        ↓ 1–2 bullets
Music Maestro revises (same pdmx_id, bump {ensemble} suffix or v2)
        ↓
stop after 3 comparator rounds unless a human says continue
```

## What this will not do

- Prove the recording is “the” correct orchestration.
- Authorize shipping the target audio inside the film-scoring app.
- Replace LEGAL.md.

## On disk (v1)

Provenance quotes: [SOURCES.md](SOURCES.md). Incoming raw downloads are gitignored.

| slug | kind | license | Fair piano→orchestra pair? |
| --- | --- | --- | --- |
| [beethoven-op67-i](beethoven-op67-i/) | orchestra | PD (Skidmore / Musopen) | **Yes** — same work as piano reduction `QmYE1Pgci…` |
| [beethoven-op55-i](beethoven-op55-i/) | orchestra | PD (Musopen Symphony 2012) | **Yes** — Eroica/I piano reduction |
| [mozart-k550-iii](mozart-k550-iii/) | orchestra | PD (Musopen Symphony 2012) | Yes for K.550 MIDI; texture-only for London minuets |
| [bach-bwv1068-air](bach-bwv1068-air/) | strings | PD-US federal (USAF) | Yes for strings chorale; Wilhelmj arrangement FLAG; US-only PD caveat |
| [mozart-k421-iii](mozart-k421-iii/) | chamber | PD (Musopen Quartet 2012) | Texture-only (no K.421 in corpus) |
| [chopin-op28-20](chopin-op28-20/) | piano | CC-BY-3.0 (Ivan Ilić) | **No** — last resort; no CC orchestra of Op.28/20 |
| [bach-bwv846](bach-bwv846/) | piano | CC0 (Ishizaka) | No |
| [beethoven-op27-2-i](beethoven-op27-2-i/) | piano | PD (Pitman / Musopen) | No; orchestral Moonlight transcriptions typically © |
| [chopin-b150](chopin-b150/) | piano | CC0 (Higuchi) | No |

Start the comparator loop on **beethoven-op67-i** and **beethoven-op55-i**.
