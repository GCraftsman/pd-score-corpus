# Orchestration rules (testable)

Pitch convention: **C4 = MIDI 60**, concert pitch, 12-TET. Scientific
pitch names use that same middle C (not the C3=60 Yamaha convention).

These rules are for **Music Maestro code**, not for a human composition
seminar. Every range is a closed MIDI interval. Clip or octave-shift
into the **practical** column; the **extreme** column is for logging
only (“I wanted C7 on violin, practical max is E7, OK”).

Craft sources (see [`references.md`](references.md)): Rimsky-Korsakov
*Principles of Orchestration* is **public domain** (IMSLP + Gutenberg).
Adler, Piston, Blatter, Kennan are **proprietary textbooks** — use them
only as named *concepts* (do not paste their examples or prose).

---

## 1. Instrument ranges (concert pitch)

`lo`/`hi` = practical MIDI notes inclusive. `xlo`/`xhi` = extreme /
solo. `open` = open strings or natural harmonics to prefer. Transpose
column is for **MusicXML / printed parts only** — MIDI stays concert.

### Strings

| Inst | Scientific practical | MIDI lo–hi | Extreme MIDI | Open strings (MIDI) | Transpose for parts |
| --- | --- | --- | --- | --- | --- |
| Violin | G3–E7 | **55–100** | 55–103 (G7) | G3=55, D4=62, A4=69, E5=76 | none |
| Viola | C3–E6 | **48–88** | 48–93 (A6) | C3=48, G3=55, D4=62, A4=69 | none (alto clef) |
| Cello | C2–E5 | **36–76** | 36–84 (C6) | C2=36, G2=43, D3=50, A3=57 | none |
| Contrabass | E1–G3 | **28–55** | 24–60 (C1 ext. → C4) | E1=28, A1=33, D2=38, G2=43 | written **8va higher** |

Bass sounds **one octave below** the written part. MIDI = sounding.
C-extension (C1=24) is allowed only if the source bass is already ≤ E1
and the era is romantic; otherwise clip to 28.

### Woodwinds

| Inst | Scientific practical | MIDI lo–hi | Extreme MIDI | Transpose for parts |
| --- | --- | --- | --- | --- |
| Piccolo | D5–C8 sounding | **74–108** | 74–108 | written 8va *lower* |
| Flute | C4–D7 | **60–98** | 59–98 (B3 rare) | none |
| Oboe | Bb3–G6 | **58–91** | 58–93 | none |
| English horn | E3–C6 | **52–84** | 52–86 | written P5 higher |
| Clarinet in Bb | D3–Bb6 concert | **50–94** | 50–96 (C7) | written **M2 higher** |
| Clarinet in A | C#3–A6 concert | **49–93** | 49–95 | written m3 higher |
| Bass clarinet | Bb1–G5 concert | **34–79** | 34–82 | written M9 higher |
| Bassoon | Bb1–Eb5 | **34–75** | 34–79 | none |
| Contrabassoon | Bb0–Bb3 | **22–46** | 22–53 | written 8va higher |

v1 experiments use **Bb clarinet** (concert MIDI) and do not switch to
A clarinet. If a passage is written in a sharp key and you later emit
MusicXML, you may choose A clarinet then — not in MIDI.

### Brass

| Inst | Scientific practical | MIDI lo–hi | Extreme MIDI | Transpose for parts |
| --- | --- | --- | --- | --- |
| Horn in F | F2–F5 | **41–77** | 34–84 | written **P5 higher** |
| Trumpet in Bb | E3–C6 concert | **52–84** | 52–86 | written **M2 higher** |
| Trombone (tenor) | E2–F5 | **40–77** | 40–82 | none (bass/tenor clef) |
| Bass trombone | Bb1–Bb4 | **34–70** | 34–74 | none |
| Tuba | D1–F4 | **26–65** | 26–67 | none |

### Percussion, harp, continuo

| Inst | Scientific practical | MIDI lo–hi | Notes |
| --- | --- | --- | --- |
| Timpani (set) | D2–A3 typical | **38–57** | 2–4 drums; no chromatic runs; write **tonic/dominant** of the local key plus one neighbor |
| Crash cymbal | GM ch.10 note **49** | 49 | hits only, duration ≤ 1 beat of MIDI; let GM ring |
| Harp | Cb1–G#7 | **23–104** | no more than 4-note chords; avoid 7-note piano clusters; no pedal-diagram in MIDI |
| Harpsichord continuo | F1–F6 | **29–89** | GM 6; baroque cards only; keep it quieter (CC7=70) |

### Compact MIDI cheat-sheet (practical)

```
Violin        55–100     Viola         48–88
Cello         36–76      Contrabass    28–55
Flute         60–98      Oboe          58–91
Clarinet Bb   50–94      Bassoon       34–75
Horn F        41–77      Trumpet Bb    52–84
Trombone      40–77      Tuba          26–65
Harp          23–104     Timpani       38–57
Piccolo       74–108
```

Source: practical composites of Rimsky (PD), the octatone/Brooks range
sheet, and the MIDI table at
https://soundprogramming.net/file-formats/midi-note-ranges-of-orchestral-instruments/
(that page is a convenience table, slightly optimistic on cello high
end and trumpet — we use the stricter practical column above).

---

## 2. Default piano → orchestra role map

Apply after voice split ([SKILL.md](SKILL.md) step 5). Pitches are
concert MIDI.

| Piano material | Default destination | Fallback if out of range |
| --- | --- | --- |
| RH top (skyline) | **Violin I** | Flute if all skyline ≥ 72 (C5) *and* era ≥ classical; else 8vb onto Vln I |
| RH inner | **Violin II**, then Viola | Clarinet 1 if Vln II already has a moving line |
| LH chords / offbeat accompaniment | **Viola** + **Horn 1–2** (held, not machine-gun 8ths) | Bassoon if horns rest |
| LH lowest (bass) | **Cello** at pitch; **Contrabass** 8vb | If bass > 55, leave Cb out; if bass < 28, clip to 28 |
| Fast broken LH (arpeggio) | **Harp** (romantic) or Vc/Vla outline (classical/baroque) | see density table |
| Pedal wash | string *pad* on Vla+Vc, CC11 low, no CC64 | never winds |
| Accents / sfz | Timpani on bass pitch class if in 38–57, else tutti velocity bump | optional cymbal on `HIT` markers only |

SATB mapping of a 4-note piano chorale (high→low):

| SATB | Instrument |
| --- | --- |
| S | Violin I |
| A | Violin II |
| T | Viola |
| B | Cello (+ Cb 8vb if B ≤ 48) |

Do not assign SATB to a brass choir by default. Brass *double* strings
in f/ff tuttis of classical/romantic cards, they do not replace them.

---

## 3. Choirs

### Strings (`strings` ensemble)

Always present except `unaccompanied` windows (then Vln I solo).

- Divisi: not in v1. One MIDI line per desk. Double-stops allowed on
  Vla/Vc only when the source chord is a 5th or 6th *and* both notes
  lie on playable strings (span ≤ 7 semitones for vla, ≤ 12 for vc).
- Tremolo / pizz: not in v1 (would need keyswitches or GM programs 44/45
  on a *separate* track). Use arco sustain.

### Woodwinds

- Baroque: 2 oboes + 1 bassoon. Flute only if the skyline sits ≥ 72.
- Classical: 2.2.2.2 (Fl, Ob, Cl, Bn) in pairs. Winds double the tune
  at cadences and play held inner tones; they do not busy-up 16ths.
- Romantic: same 2.2.2.2 plus optional piccolo if skyline ≥ 84; harp
  joins. Do not add saxophone (not in this era table).

### Brass

- Baroque: **off** (except festive Handel-style timp+tpt if the card
  says so — default off).
- Classical: 2 horns; 2 trumpets + timpani only in f tuttis or when
  the source has fanfare-like repeated notes ≥ MIDI 60.
- Romantic: 4 horns, 2 trumpets, 3 trombones, tuba. Still: brass do
  not play every chord. Horns bind harmony; trumpets/trombones enter
  at climaxes (top 20% of window-mean velocity, or explicit f/ff).

### Percussion

- Timpani: tonic/dominant of the estimated key, hits on downbeats of
  tuttis and on `HIT` markers. No timpani rolls in v1 (GM cannot).
- Cymbal: **hits only**, and only when the experiment card adds `HIT`
  markers. Never a groove.

---

## 4. Doubling table

Octave doubling is how a piano texture becomes an orchestra. Use the
table; then read “when NOT to double.”

| Line | Default doubling | MIDI relation |
| --- | --- | --- |
| Melody (skyline) | Vln I + Flute 8va | flute = melody + 12 if melody+12 ∈ [72, 98], else flute tacet |
| Melody (soft, p) | Vln I only, or Vln I + Vln II all'unisono | unison = same MIDI, Vln II velocity −8 |
| Melody (f, classical cadence) | Vln I + Ob 1 (unison or 8va) | oboe must sit in 58–91 |
| Bass | Vc + Cb 8vb | cb = bass − 12 if result ≥ 28 |
| Bass (baroque continuo) | Vc + harpsichord LH; Cb optional | harpsichord doubles bass at pitch, sparse |
| Inner 3rd | Vla + Cl 1 | clarinet tacet if inner < 50 |
| Inner 5th | Horn 1 (held) | horns do not take 16th-note inners |
| Tutti ff chord | strings + winds + horns + (romantic) trombones | each choir gets ≤ 4 notes of the chord |

### When NOT to double

| Don’t | Why | Test |
| --- | --- | --- |
| Clarinets in unison below MIDI 52 with bassoons and celli | muddy (Rimsky: low clarinets in 8ves with bassoons thicken without speaking) | if cl_pitch < 52 and bn or vc already has that pc, drop clarinet |
| Flute + Oboe unison below MIDI 72 | oboe eats the flute | flute tacet or 8va |
| Three octaves of the same pc below MIDI 48 (e.g. Bn + Vc + Cb + Tuba) | undefined rumble | max **two** sounding octaves below 48 |
| Horns doubling a fast bass line | unplayable / comic | horns only on notes ≥ quarter-note |
| Piccolo on chromatic inner voices | shrill, not 18th/19th-c. | piccolo = melody 8va only |
| Harp doubling staccato 16ths with pizz (we don’t pizz in v1) | useless | harp = arpeggio or rolled chord, ≤ 8 notes/s |
| Melody doubled by trombone in its mid register at p | too heavy | trombone tacet under p |

Rimsky (Gutenberg, Ch. I–II) is the PD authority for “who can double
whom.” When in doubt: **strings carry the texture; winds color; brass
punctuate.**

---

## 5. Density by texture

Cap **simultaneous sounding MIDI notes** (not counting 8va doubles of
the same pc as extra density — they count as 1 for this cap, but they
still exist as notes).

| Texture | Max desks with notes in a beat | What they play | Winds | Brass | Perc |
| --- | --- | --- | --- | --- | --- |
| `unaccompanied` | 1–2 | Vln I melody; optional Vc pedal | optional Fl 8va | off | off |
| `chorale` | 5 strings + 2 horns | SATB + Cb 8vb | double SAT at cadences | horns bind | timp on phrase ends |
| `arpeggio` | 3–4 | outline on Vln I / Vc; figure on harp or vla | held chord tones | off unless f | off |
| `ostinato` | 3 | ostinato on *one* choir; melody on Vln I; bass | color | off | off |
| `waltz` | 4–6 | bass beat 1; chords 2–3; melody | melody 8va in repeats | horns on 2–3 | optional timp on 1 |
| `polyphony` | = n_voices | one stream per desk | one stream per WW if 3–4 voices | off | off |
| `homophony` | 5–8 | melody + block or broken acc. | double melody at f | horns | timp if f |

**Tessitura control.** After assignment, compute mean MIDI per desk.
If Vln I mean < 67 (G4) for ≥ 8 bars, consider 8va up *if* still ≤ 100.
If Vc mean > 60 for ≥ 8 bars and Cb is tacet, that is OK (tenor cello).
If *all* winds sit in 48–60 together, drop two of them.

**Silence is legal.** A bar with only Vln I + Vc is a valid orchestral
bar. Filling every hole is how MIDI orchestration starts to sound like
a synth pad.

---

## 6. Dynamics → CC11 / velocity

| Source | Velocity (note-on) | CC11 | CC1 (GM preview) |
| --- | --- | --- | --- |
| pp | 52 | 40 | 0 |
| p | 64 | 55 | 0 |
| mp | 76 | 70 | 0 |
| mf | 88 | 85 | 0 |
| f | 100 | 100 | 0 |
| ff | 110 | 115 | 0 |
| source velocity `v` (no text) | `clamp(0.4*v+50, 48, 110)` | `clamp(0.6*median_v+20, 40, 110)` | 0 |

Phrase shape on any note **≥ half note**:

1. CC11 at onset = table value
2. CC11 at 50% duration = min(table+8, 127)
3. CC11 at 90% duration = max(table−12, 1)  (taper)

CC7 (volume) stays 100. Do not automate CC7 (Logic users expect faders
to stay put).

CC64 = 0 on all orchestral tracks. Piano pedal → note lengthening on
harp/pads only ([SKILL.md](SKILL.md) step 5F).

**GM vs Logic.** CC1 is unused in our GM preview so a GM violin does
not grow an unintended vibrato. In Logic Studio Strings the user may
bind CC1 to dynamics; that is *their* mapping. We still give them CC11
as a phrase envelope.

---

## 7. Transposition reminders (notation only)

MIDI = concert. If a later pass writes MusicXML parts:

| Instrument | MIDI (concert) | Written |
| --- | --- | --- |
| Clarinet in Bb | N | N+2 |
| Horn in F | N | N+7 |
| Trumpet in Bb | N | N+2 |
| English horn | N | N+7 |
| Double bass | N | N+12 |
| Piccolo | N | N−12 |
| Contrabassoon | N | N+12 |
| Bass clarinet (treble) | N | N+14 |

Test: a concert C4=60 on horn becomes written G4=67. If you ever see
written-pitch MIDI in an arrangement file, the card **fails**.

---

## 8. Era tables (style target = source era)

**Not** “cinematic.” **Not** Williams/Zimmer. Match the composer.

### Baroque — death ≤ 1760 plus Rameau/Telemann

Composers: Bach, Handel, Scarlatti, Rameau, Vivaldi, Telemann,
Pachelbel, Corelli, Purcell.

| Slot | Use |
| --- | --- |
| Ensemble token | `baroque` |
| Core | Vln I, Vln II, Vla, Vc, Continuo (harpsichord GM 6) |
| Winds | 2 oboes, 1 bassoon (double strings or play a reduction) |
| Brass/perc | off by default |
| Texture | preserve counterpoint; no romantic pads; no harp |
| Density | low; `polyphony` and `chorale` dominate |

Bach chorale-style piano: SATB strings, bassoon with bass, oboes with
S/A. Do **not** use Busoni piano transcriptions (arranger d. 1924).

### Classical — Haydn, Mozart, Clementi, Boccherini, Gluck, early Beethoven

| Slot | Use |
| --- | --- |
| Ensemble token | `classical` |
| Core | 2.2.2.2 / 2 horns / strings |
| Trumpets+timp | tuttis and fanfares only |
| Trombones/tuba/harp | off |
| Texture | clear melody + accompaniment; winds in pairs |
| Density | medium; lots of rest in brass |

### Early / mid romantic — Schubert, late Beethoven, Mendelssohn, Schumann, Chopin, Berlioz, Rossini, Donizetti, Bellini, Gounod, Bizet

| Slot | Use |
| --- | --- |
| Ensemble token | `romantic` (or `strings` if the card says so) |
| Core | 2.2.2.2 / 4 horns / 2 tpt / 3 tbn / tuba / timp / strings |
| Harp | **on** for Chopin/Schubert arpeggios and nocturne LH |
| Texture | more doubling, still leave air; horns as glue |
| Chopin special | he wrote for piano, not orchestra: use a *small* romantic
  orchestra or strings+harp+winds. Do not pretend it is Tchaikovsky. |

### Late romantic — Brahms, Tchaikovsky, Dvořák, Wagner, Verdi, Grieg, Rimsky-Korsakov, Mussorgsky, Borodin, Bruckner, Franck, Johann Strauss II, Liszt (orchestral thinking)

| Slot | Use |
| --- | --- |
| Ensemble token | `romantic` |
| Core | as early romantic, winds may double melody more often |
| Harp | on |
| Brass | more present, still not a film-brass ostinato |
| Texture | richer doubling; still clip to ranges; no 20th-c. cluster |

Liszt piano works: treat as late-romantic piano, not as a tone poem
unless the source is already an orchestral reduction.

---

## 9. Voice leading (style option)

- **Do not rewrite the source** to satisfy schoolbook species
  counterpoint.
- **Do** avoid *introducing* parallel perfect 5ths/octaves between
  Vln I and bass that were **not** in the piano reduction, for
  Mozart/Haydn/Beethoven cards.
- For Bach, parallels that exist in the source stay.
- Prefer common tones in horns (same MIDI across adjacent buckets).
- Max melodic leap on winds: 16 semitones except octave doubling of
  the tune. Bigger leaps → rest that desk for the beat.

---

## 10. Film-cue functions (without film-score harmony)

A piano *sketch* for a cue is still 18th/19th-c. notes. Typical
functions, mapped to our choirs:

| Sketch layer | Choir |
| --- | --- |
| Melody | Vln I (+ Fl 8va) |
| Ostinato | Vla or Horns, *one* figure |
| Pedal | Cb + Bn, long notes |
| Hits | Timpani ± cymbal, on **markers**, not a new harmonic language |

Hit-points are a **tempo-map / marker** problem: they must land on a
barline or a notated beat of the source. Do not stretch the
arrangement to a video file. Do not add “braams,” clusters, or
trailer percussion.

---

## 11. Unit tests Maestro should write (even if tiny)

Put assertions in the experiment script, not a new package:

```python
RANGES = {
  "Violin I": (55, 100), "Violin II": (55, 100), "Viola": (48, 88),
  "Cello": (36, 76), "Contrabass": (28, 55), "Flute 1": (60, 98),
  "Oboe 1": (58, 91), "Clarinet 1": (50, 94), "Bassoon 1": (34, 75),
  "Horn 1": (41, 77), "Trumpet 1": (52, 84), "Trombone 1": (40, 77),
  "Tuba": (26, 65), "Harp": (23, 104), "Timpani": (38, 57),
  "Piccolo": (74, 108),
}
```

For every note `n` on track `name`: `lo <= n.pitch <= hi`.
