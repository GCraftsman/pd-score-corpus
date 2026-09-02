# SMF Type 1 output contract

Music Maestro **must** emit files that Logic Pro / GarageBand can File→Open
without a stereo bounce and without a `.logicx` project. Spec below is
normative. If a library cannot do one of these, switch libraries (prefer
`mido` for meta events, `pretty_midi` for notes).

Apple’s own description of what an SMF carries (events, track names,
markers, tempo, copyright) is here:
https://support.apple.com/guide/logicpro/standard-midi-files-lgcpdf6a3851/mac

Logic **Format 1** = multiple tracks, independent data. Logic **Format 0**
= one track. We never write Format 0. Logic will auto-create a software
instrument per MIDI track and may label the *track header* from the GM
program name; region names come from the MIDI track/sequence name. Write
**both** a GM program change *and* a human track name.

## File

| Field | Value |
| --- | --- |
| Format | SMF Type 1 (format=1) |
| PPQ (ticks per quarter) | **480** |
| Encoding | Standard MIDI File, not RMID, not XMF |
| Extension | `.mid` |
| Path | `arrangements/{composer-slug}/{pdmx_id}.{ensemble}.mid` |

`composer-slug`: canonical allowlist name, NFKD, ASCII fold, lowercase,
spaces/`/`/`'` → `-`, collapse repeats. Examples:

- `Johann Sebastian Bach` → `johann-sebastian-bach`
- `Wolfgang Amadeus Mozart` → `wolfgang-amadeus-mozart`
- `Pyotr Ilyich Tchaikovsky` → `pyotr-ilyich-tchaikovsky`
- `Frederic Chopin` → `frederic-chopin`

`ensemble` is one of:

| Token | Meaning |
| --- | --- |
| `strings` | Vln I, Vln II, Vla, Vc, Cb |
| `baroque` | strings + continuo cello/bass + 2 oboes + bassoon (no romantic brass) |
| `classical` | 2.2.2.2 / 2.2.0.0 / timp / strings |
| `romantic` | 2.2.2.2 / 4.2.3.1 / timp / harp / strings |
| `cue-sketch` | melody + ostinato + pedal + hit tracks (film-cue *function*, 19th-c. language) |

Example:
`arrangements/frederic-chopin/QmdHbV5ya1MwSJnJNdSXw4UmKNU4JjtrBpSiFKMRS4F3rc.strings.mid`

Create the composer directory if missing. Do not overwrite a previous
experiment’s file; if the same `(pdmx_id, ensemble)` is re-run, append
`.r2`, `.r3` before `.mid` and log the reason.

## Track 0 — conductor

No notes. Channel unused. Contains, in this order near tick 0:

1. **Sequence name** meta (`FF 03`): `{composer} — {title} [{pdmx_id[:12]}…]`
2. **Copyright / text** meta (`FF 02` *and* a `FF 01` text event):

   ```
   source: {composer}, {title} (pdmx_id={pdmx_id})
   arrangement: experimental, CC0
   not cleared for film; see LEGAL.md
   ```

3. **Initial tempo** (`FF 51`): copy from source. If source has no tempo,
   write 120 BPM (`500000` µs/quarter). Copy the **entire tempo map**
   (every `set_tempo`) at the same ticks as the source.
4. **Time signature** (`FF 58`): copy from source. Default 4/4,
   metronome=24, thirty-seconds=8. Copy every subsequent time-sig change.
5. **Key signature** (`FF 59`) if known from music21 or MIDI key-sig
   events; otherwise omit (do not guess from the title alone).
6. **Markers** (`FF 06`):
   - `START` at tick 0
   - `END` at the last source note-off tick
   - Rehearsal letters every 8 bars if the piece is ≥16 bars (`A`, `B`, …)
   - Any hit-points for cue experiments: `HIT {n}` at the specified bar
     (this is a **tempo-map / marker** problem, not an extra orchestral
     choir — see experiments EXP-07)

Do **not** put notes on track 0. Do **not** use MIDI channel 10 for any
pitched orchestral track (GM percussion).

## Instrument tracks

One SMF track per instrument. Track order is **score order**, omitting
unused instruments (empty tracks make Logic spawn empty software
instruments — skip them).

### Score order (full romantic roster)

| # | Track name (exact) | GM program **0-index** | GM 1-index name | MIDI ch |
| --- | --- | ---: | --- | ---: |
| 1 | Piccolo | 72 | 73 Piccolo | 1 |
| 2 | Flute 1 | 73 | 74 Flute | 2 |
| 3 | Flute 2 | 73 | 74 Flute | 3 |
| 4 | Oboe 1 | 68 | 69 Oboe | 4 |
| 5 | Oboe 2 | 68 | 69 Oboe | 5 |
| 6 | Clarinet 1 | 71 | 72 Clarinet | 6 |
| 7 | Clarinet 2 | 71 | 72 Clarinet | 7 |
| 8 | Bassoon 1 | 70 | 71 Bassoon | 8 |
| 9 | Bassoon 2 | 70 | 71 Bassoon | 9 |
| 10 | Horn 1 | 60 | 61 French Horn | 11 |
| 11 | Horn 2 | 60 | 61 French Horn | 12 |
| 12 | Horn 3 | 60 | 61 French Horn | 13 |
| 13 | Horn 4 | 60 | 61 French Horn | 14 |
| 14 | Trumpet 1 | 56 | 57 Trumpet | 15 |
| 15 | Trumpet 2 | 56 | 57 Trumpet | 16 |
| 16 | Trombone 1 | 57 | 58 Trombone | 1 (reuse; unique *track*) |
| 17 | Trombone 2 | 57 | 58 Trombone | 2 |
| 18 | Bass Trombone | 57 | 58 Trombone | 3 |
| 19 | Tuba | 58 | 59 Tuba | 4 |
| 20 | Timpani | 47 | 48 Timpani | 5 |
| 21 | Cymbal | *channel 10, note 49* (crash cymbal 1) | GM drum | 10 |
| 22 | Harp | 46 | 47 Orchestral Harp | 6 |
| 23 | Violin I | 40 | 41 Violin | 7 |
| 24 | Violin II | 40 | 41 Violin | 8 |
| 25 | Viola | 41 | 42 Viola | 9 |
| 26 | Cello | 42 | 43 Cello | 11 |
| 27 | Contrabass | 43 | 44 Contrabass | 12 |

Notes:

- **GM is preview only.** Final sound is Logic **Studio Strings / Studio
  Horns / Studio Woodwinds** (or GarageBand orchestral patches) assigned
  by the user after File→Open. Do not embed keyswitch notes for
  Spitfire/BBCSO/Kontakt. Those note numbers are library-specific and
  will sound as pitches on GM and on Studio Strings.
- Channel reuse across tracks is OK in Type 1 (Logic uses *tracks*, not
  channels, as the identity). Still avoid channel 10 except the optional
  Cymbal hit track.
- Timpani GM program 47 is a *pitched* GM instrument, not the drum map.
  Write **concert-pitch** timpani notes in MIDI 38–55 (see ranges).
- Cymbal is the **only** GM channel-10 use, and only for notated hits
  (EXP-07). No drum kit grooves.

### Per-instrument track contents (tick 0, then notes)

1. Track name meta `FF 03` = exact name from the table (`Violin I`, not
   `ViolinI` or `vl1`).
2. Program change on that track’s channel = GM 0-index from the table.
3. CC **7** (channel volume) = 100.
4. CC **10** (pan) = choir defaults:

   | Choir | Pan |
   | --- | ---: |
   | Violin I | 80 (slight stage-left / audience-right is fine; use 80) |
   | Violin II | 48 |
   | Viola | 40 |
   | Cello | 56 |
   | Contrabass | 64 |
   | Woodwinds | 64 ± 8 by desk |
   | Horns | 32 |
   | Trumpets | 96 |
   | Low brass | 64 |
   | Harp | 24 |
   | Timpani | 64 |

   These are preview hints. Logic’s Studio Strings has its own stage.
5. CC **11** (expression) initial = mapped from source dynamic
   ([orchestration-rules.md](orchestration-rules.md) § Dynamics).
6. CC **1** (modulation) initial = 0 for GM preview. For Logic Studio
  Strings the user may remap CC1 to dynamics; still write a *simple*
   CC11 phrase shape so GM preview is not organ-like.
7. CC **64** (sustain) = **0 always** on strings, winds, brass. Piano
   pedal in the *source* is a sustain hint: either lengthen notes to the
   pedal-up tick (re-articulation off) or ignore it. Never copy CC64 onto
   orchestral tracks (breaks legato scripts in real libraries).
8. Then note-on / note-off pairs. **Concert pitch.** No transposing
   instrument offsets in the MIDI file (see § Concert pitch).
9. Note-off every note. No hanging notes. Prefer explicit note-off, not
   note-on velocity 0, but both are valid.

## Concert pitch vs transposed parts

| Layer | Pitch |
| --- | --- |
| MIDI in this repo | **Concert pitch** (what you hear) |
| Logic Studio Strings preview | Concert pitch |
| Future MusicXML / printed parts | Transpose: clarinet in Bb written M2 higher; horn in F written P5 higher; double bass written 8va higher; piccolo written 8va lower |

Do **not** write transposed MIDI “so the part looks right.” Logic will
play it a second / a fifth off. Transposition reminders live in
[`orchestration-rules.md`](orchestration-rules.md) for a later notation
pass only.

## Tempo, duration, and alignment

- Copy source tempo map 1:1. Do not “musicalize” tempo (no extra rubato
  curve) in v1 experiments unless the source already has it.
- Arrangement duration must match source duration **± 1 bar**.
- Do not pad with extra pickup bars. Do not trim the last chord early.
- Quantize nothing that the source did not already quantize. If the
  source is messy, leave it messy and log it.

## What not to put in the file

- Keyswitch notes (C0, A0, etc. below the instrument range).
- Program changes mid-track to fake articulations.
- Embedded audio, SMPTE, or `.logicx` hunks.
- Lyric events unless the source is a chorale *and* the experiment card
  asks for them (v1 cards do not).
- A “conductor click” note track.
- GM “Orchestra Hit” (program 55). Forbidden. Hits = timp + optional
  cymbal, or a marked tutti accent.

## Validation checklist (run before logging)

Compute these in code; write the numbers into
[`../../arrangements/NOTES.md`](../../arrangements/NOTES.md).

1. `mido.MidiFile(path).type == 1` and `ticks_per_beat == 480`.
2. Track 0 has no `note_on` with velocity > 0.
3. Every note-bearing track has a `track_name` and a `program_change`.
4. No pitched note on channel 10.
5. Every note pitch ∈ instrument range table (practical range). Count of
   clipped notes logged; **fail** the card if any note had to be dropped
   rather than octave-shifted into range.
6. Skyline of the source (highest sounding pitch per onset bucket of
   1/32 note) pitch-class sequence vs Violin I: ≥ 85% pitch-class match
   on buckets where the source skyline is active. (Octave doubling of
   the melody on Flute is extra, not a replacement.)
7. Last event tick of arrangement ∈ [source_last − 1 bar, source_last + 1 bar].
8. File opens in FluidSynth without error:
   `fluidsynth -n -i -a file -F /tmp/preview.wav soundfont.sf2 the.mid`
   (if FluidSynth or a soundfont is absent, log `preview: not run` and
   still emit the MIDI).
9. Metadata text contains `arrangement: experimental, CC0`.

## CC event density

Write CC11 as a **step envelope**, not a sample-accurate curve:

- At each new musical dynamic, one CC11 event.
- Optional: at the start of a sustained note longer than a half note,
  CC11 = attack value; 50% through the note, +8; 90% through, back to
  attack. This stops GM strings sounding like an organ.
- Do not write CC events every tick (Logic files become uneditable).

## Reference GM program table (0-index)

Full GM1 map: MIDI Association GM Level 1. We only use the orchestral
slice above. Piano GM 0 may appear on a *source* file; it must not
appear on the arrangement except if an experiment explicitly keeps a
keyboard continuo (baroque: use GM **6 Harpsichord**, track name
`Continuo`).
