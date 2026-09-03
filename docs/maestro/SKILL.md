---
name: piano-to-orchestra
description: Transform allowlisted piano/keyboard MIDI from pd-score-corpus into SMF Type 1 multi-instrument orchestral arrangements for Logic Pro. Use when Music Maestro runs an experiment, maps piano texture to strings/winds/brass, or writes arrangements/*.mid.
---

# Piano → orchestra (Music Maestro)

Follow this recipe for **every** experiment. Cards in
[`experiments.md`](experiments.md) only change *source query*, *ensemble*,
and *method*. Rules live in [`orchestration-rules.md`](orchestration-rules.md).
Bytes layout lives in [`midi-contract.md`](midi-contract.md).
First-pass hygiene (before critic): [`first-pass.md`](first-pass.md).
Critic JSON patches: [`critic-patches.md`](critic-patches.md).
App path (piano solo → invented orchestra, analog refs):
[`analog-matching.md`](analog-matching.md),
[`piano-solo-arrange.md`](piano-solo-arrange.md),
[`analog-critic.md`](analog-critic.md).
Not CYCLE same-work gold — do not match analog MIDI numbers.
Harmony + variations: [`harmony-rules.md`](harmony-rules.md), [`variation-techniques.md`](variation-techniques.md).


## 0. Preconditions

- Working copy: the `pd-score-corpus` repo root (clone of https://github.com/GCraftsman/pd-score-corpus).
- Do **not** `git commit`. Do **not** delete `.cache/`. Do **not** rewrite `LEGAL.md`.
- Do **not** scrape MuseScore, YouTube, or film scores.
- Do **not** render through Spitfire/BBCSO for training or for repo artifacts.
- Python 3.11+ with `music21`, `pretty_midi`, `mido`, `numpy`. Install if missing:
  `pip install music21 pretty_midi mido numpy` (BSD-3 / MIT / MIT).
- Read [`README.md`](README.md) once per session.

## 1. Pick the experiment card

Open [`experiments.md`](experiments.md). Run the **lowest-numbered card
that has not been logged** in [`../../arrangements/NOTES.md`](../../arrangements/NOTES.md).
Do not start EXP-08 (or any ML card) before EXP-01…EXP-07 exist as MIDI
files. Skip any card whose license flag is `SKIP-ML`.

## 2. Select a source row

From `data/manifest.csv`:

1. Filter `is_piano_only` truthy (`True` / `true` / `1`).
2. Apply the card’s composer / title / tag query (case-insensitive
   substring on `composer`, `title`, `song_name`, `tags`).
3. Drop rows whose title/tags contain `busoni`, `liszt transcription` of
   a graylisted source, `arrangement of`, or a soundtrack keyword.
4. Prefer `license` in `{cc-zero, cc0, publicdomain, pdm}`.
5. Prefer shorter files for first pass: if you can parse duration, pick
   a row whose MIDI is **16–64 bars** or **< 3 minutes**. If duration is
   unknown, pick the first remaining match and clip the arrangement to
   the first **32 bars** for the experiment (log the clip). Clipping is
   allowed for experiments; the app later stitches full works.
6. Resolve path: manifest `mid` `./mid/{a}/{b}/{id}.mid` → on-disk
   `midi/{a}/{b}/{id}.mid`. If missing, try the next row.

Record `pdmx_id`, composer, title, path.

## 3. Load and inspect

```python
import pretty_midi, mido
from pathlib import Path
pm = pretty_midi.PrettyMIDI(str(src_path))
mf = mido.MidiFile(str(src_path))
```

Log:

- `type`, `ticks_per_beat`, track count, instruments, tempo changes
- pitch min/max, duration seconds, estimate bars from time signature
- whether CC64 (sustain) is present
- whether the file is Type 0 (one track, typical for piano)

If MusicXML exists for the same id, parse with `music21.converter.parse`
and prefer its `PartStaff` split (RH/LH) over a pitch-threshold split.

## 4. Classify texture (one label per 2-bar window)

For each 2-bar window compute:

| Feature | How |
| --- | --- |
| `n_sim` | mean number of simultaneous pitches |
| `span` | p95(highest) − p5(lowest), in semitones |
| `rhythm_cv` | coefficient of variation of IOIs of onsets |
| `lh_repeat` | if a pitch class in MIDI ≤ 48 repeats ≥ 4 times in the window |
| `skyline_unique` | unique skyline pitches / total onsets |

Assign **one** label (first match wins):

1. `unaccompanied` if `n_sim < 1.4`
2. `chorale` if `n_sim ≥ 3.5` and `rhythm_cv < 0.35` (block chords)
3. `ostinato` if `lh_repeat` and not chorale
4. `arpeggio` if `n_sim ≥ 2` and mean note duration ≤ a dotted eighth
   and span ≥ 12
5. `waltz` if meter is 3/4 or 3/8 and bass onsets cluster on beat 1
6. `polyphony` if ≥ 2 independent rhythmic streams (see step 5)
7. else `homophony`

The **piece-level** label is the mode of window labels. Use it to pick
density and doubling from the rules file.

## 5. Split voices (rules-only algorithm)

Work in **absolute ticks**. Bucket onsets to the nearest 1/32 note
(15 ticks at PPQ 480? No: 480/8 = 60 ticks per 32nd). Use 60-tick
buckets.

**A. Skyline (melody).** Uitdenbogerd & Zobel *all-mono*: in each
bucket that contains an onset, take the **highest** pitch that starts
in that bucket. If it would overlap the next skyline onset, truncate
it. This is Violin I (and optional Flute 8va). Cite:
https://people.eng.unimelb.edu.au/jzobel/fulltext/acm-mm99.pdf

**B. Bass.** In each bucket, take the **lowest** pitch with MIDI
number ≤ 52 (E3) if any; else the lowest pitch in the bucket if it is
≤ 60. This is Cello, with Contrabass doubling **down an octave** when
the concert pitch is ≥ 36 (C2) after the 8vb (i.e. don’t send the bass
below E1=28 unless the source bass is already there).

**C. Hands.** If music21 gives two `PartStaff`s, treat staff 0 as RH
and staff 1 as LH. Else split at **MIDI 60 (C4)** *except* when a
note is within 7 semitones of the previous note assigned to a hand
(voice-leading override). This is a heuristic, not a neural hand
separator. Log crossings.

**D. Inner voices.** Remaining notes after removing (skyline ∪ bass)
are inners.

- If `chorale`: sort remaining pitches high→low into Violin II, Viola,
  (overflow → Horn 1 as a held chord tone). Target SATB: 4 voices.
- If `arpeggio`: do **not** spray every 16th onto strings. Keep the
  arpeggio on **Harp** (romantic) or **Viola+Cello broken** (classical);
  strings get the *outline* (local min/max of the figure each beat).
- If `ostinato`: assign the repeating figure to **one** choir (usually
  Viola or Horns), not the whole orchestra.
- If `polyphony` (invention/fugue): each rhythmic stream is one
  instrument (Vln I, Vln II, Vla, Vc). No chord filling.
- If `waltz`: beat 1 → Cb+Vc (bass), beats 2 and 3 → Vla (+ Horn
  chord tones), skyline → Vln I.

**E. Chord-tone assignment (chorale and homophony).** For each
bucket, the sounding pitch classes are a chord. Assign:

| Voice | Preference |
| --- | --- |
| Violin I | skyline (already taken) |
| Violin II | next-highest chord tone, prefer stepwise from previous Vln II |
| Viola | next, prefer filling the 5th or 3rd |
| Cello | bass (already taken) |
| Horns | double the triad, omit the doubled 5th if muddy |

Voice leading: prefer the assignment that **minimizes total
semitone motion** of Vln II and Vla from the previous bucket
(greedy). Parallel fifths/octaves: **style option**, not a law.
For Bach-era cards, log parallels but do not “correct” Bach.
For Mozart/Beethoven cards, avoid *new* parallel 5ths you introduced
that were not in the piano source (don’t add them; don’t rewrite the
source to remove them).

**F. Pedal.** If source CC64 ≥ 64 between t0 and t1, notes that
ended while the pedal was down may be **extended** to the pedal-up
tick *on harp and on string pads only*. Melody (skyline) is
**re-articulated** (do not smear the tune). Never copy CC64 to
orchestral channels.

## 6. Choose the ensemble from the composer’s era

Look up the composer in the era table in
[`orchestration-rules.md`](orchestration-rules.md). The experiment
card may override (e.g. strings-only). Then apply the **role map**
and **doubling table**. Clip every note into the instrument’s
**practical** MIDI range by octave shift toward the center of the
range. If after ±1 octave the note is still out of range, **drop it**
and increment `range_drops` (fail the card if `range_drops > 0` on
melody or bass).

## 7. Dynamics → velocity and CC11

Source note velocity `v` (0–127):

- Output velocity = `clamp(int(0.4 * v + 50), 48, 110)` for sustains
  (strings/winds). For timpani hits and cymbal, use `clamp(v, 64, 120)`.
- CC11 initial = `clamp(int(0.6 * median_velocity + 20), 40, 110)`.
- Map text dynamics if music21 has them: pp=40, p=55, mp=70, mf=85,
  f=100, ff=115 (CC11). Velocity stays mid; CC11 carries the dynamic
  (GM preview + Logic-friendly).

## 8. Write the SMF

Implement [`midi-contract.md`](midi-contract.md) literally:

- Type 1, PPQ 480. Re-time events if the source PPQ ≠ 480
  (`tick_out = round(tick_in * 480 / src_ppq)`).
- Track 0 conductor + metadata text including
  `arrangement: experimental, CC0`.
- Exact track names. GM programs for preview. Concert pitch.
- Filename pattern. Create directories as needed.

## 8b. First-pass hygiene, then critic

Run [`first-pass.md`](first-pass.md) on v1 **before** handing it to
critic (detach fused 8ths, chop tutti attacks, locked GM map, no
default +12 melody doubling). Critic emits 1–2 JSON patches per
cycle ([`critic-patches.md`](critic-patches.md)). Apply with:

```bash
python3 scripts/apply_critic_patches.py \
  --midi IN.mid --patches patches.json --out OUT.mid
```

The next critic pass must confirm previous patch ids **APPLIED**.
Anything the schema cannot express is a Maestro rewrite, not a patch.

## 9. Validate

Run the checklist in `midi-contract.md` § Validation. If a check
fails, fix the MIDI; do not log a green result.

## 10. Preview (optional but preferred)

If `fluidsynth` and a GM soundfont exist:

```bash
fluidsynth -n -i -a file -F /tmp/maestro-preview.wav /usr/share/sounds/sf2/FluidR3_GM.sf2 path.mid
```

Do not commit the wav. Do not use a commercial orchestral library.

## 11. Log

Append one block to [`../../arrangements/NOTES.md`](../../arrangements/NOTES.md)
using the template in that file. Include numbers, not vibes.

## 12. Stop

Do not start the next card in the same turn if the current MIDI is
not on disk and logged. One card, one MIDI, one log block, then yield.

## Forbidden shortcuts

- “I’ll just put String Ensemble GM 48 on one track.” That is Type-1
  illegal for this project: we need *named desks*.
- “I’ll keyswitch for legato.” No keyswitches.
- “I’ll make it sound cinematic.” No. Era language only.
- “I’ll download a SymphonyNet / FIGARO / MIDI-GPT checkpoint.” Read
  the license table first; almost all pretrained weights are SKIP.
- “I’ll train on BBCSO bounces of these MIDIs.” Forbidden by EULA.
