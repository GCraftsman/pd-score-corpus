# First-pass hygiene (before critic)

Music Maestro **must** apply this list to v1 **before** handing the MIDI
to critic. Critic cycles are for local register/density/articulation
fixes, not for undoing fused 8ths or a locked GM map.

Evidence below is only from two critic loops. Do not generalize from
other pieces.

| Cycle | Job | Gold | Clip | Critic cycles |
| --- | --- | --- | --- | ---: |
| `CYCLE-B5I-01` | Beethoven 5/I piano → orchestra | Skidmore College Orchestra PD (Musopen) | ~2 min | 5 |
| `CYCLE-B55I-01` | Eroica/I piano → orchestra | Musopen / Czech NSO PD | ~1 min | 10 |

Coordinator owns the job card (clip, gold, cycle id). Hard-clip sounding
duration from that card. Do not write notes past the clip.

Full ranges/doubling: [`orchestration-rules.md`](orchestration-rules.md).
Bytes: [`midi-contract.md`](midi-contract.md). Critic JSON:
[`critic-patches.md`](critic-patches.md).

---

## Locked GM map (0-index)

Preview only. Named desks. **No** GM 48/49 string ensemble, **no** harp
(program 46) on these classical-orchestra jobs.

| Desk | GM 0-index |
| --- | ---: |
| Flute 1/2 | 73 |
| Oboe 1/2 | 68 |
| Clarinet 1/2 | 71 |
| Bassoon 1/2 | 70 |
| Horn 1–n | 60 |
| Trumpet 1/2 | 56 |
| Timpani | 47 |
| Violin I/II | 40 |
| Viola | 41 |
| Cello | 42 |
| Contrabass | 43 |

Keep 40/41 for violin/viola desks. Do not replace desks with 48.

---

## MUST on v1

### 1. Detach repeated 8ths (the #1 bug)

Fused 8ths at **0.498 beat** (239 ticks at PPQ 480) were the first
critic finding on both loops.

- Repeated 8ths (motti, fate figures, inner 8th streams): sounding
  duty **0.20–0.25 beat** (96–120 ticks). Rest is silence.
- Leave true longs (half notes, fermatas, cello-theme pedals) alone.
- `CYCLE-B5I-01` v1: fate-motif 8th duty 0.498 so three 8ths fused;
  Skidmore onset 2.16/s vs Maestro 1.00/s. v2 set bars 1–5 to 0.225.
  Later 8ths at tick≥5040 were still 0.477–0.498 until v3.
- `CYCLE-B55I-01` v1: viola cello-theme 8ths and late Vln II / Vla /
  Vc / Cb 8ths at 0.498. Same fix: 0.225.

Test: for 8ths that should detach, `duration_ticks / PPQ ∈ [0.20, 0.25]`.
Count of 8ths with duty ≥ 0.40 on those desks in those windows = 0.

### 2. Chop tutti attack chords

Full-beat **0.998** (479 ticks) fused the Eroica opening.

- Tutti attack chords: sounding duty **0.35–0.45 beat**.
- `CYCLE-B55I-01` bars 1–2: 0.998 beat on all 19 desks + timp. Gold
  first-4s RMS bursts 0.31/0.39s vs Maestro 0.50/0.50s; duty>25%peak
  17.7% vs 30.5%; first-4s onset 2.00 vs 0.75 /s. v2 → 0.40 beat
  (192 ticks).

Do **not** apply this cap to sustained theme notes.

### 3. No default melody doubling at +12

Do not auto-copy the skyline to flute/oboe/bn2 at +12 (or unison) for
the whole clip.

- `CYCLE-B5I-01` v1: all 229 Oboe 1 notes matched Vln I (229/381 of
  Vln I); Flute 1 +12 on 213/229 (desk median MIDI 87 / D#6). Maestro
  centroid 1580 Hz vs Skidmore 1217 Hz. v2 rested WW after the motto
  except tuttis (Ob1/Fl1 229 → 49).
- `CYCLE-B55I-01` v1: Bn2 106/108 at +12 of cello; Fl1 45/48 +12 of
  Vln I. Critic later dropped Bn2 to unison.

Winds color tuttis and cadences. They do not busy-up the tune.

### 4. Contrabass = cello 8vb, except floor and quiet themes

- Cb sounds **one octave below cello** when the result is in range
  (practical 28–55; do not send below the desk floor).
- If cello is **already at floor**, do not drop Cb another octave.
- **Rest Cb on quiet themes** (cello theme, first-theme stretch after
  a fermata). Do not bury the tune.
- `CYCLE-B5I-01`: v1 Cb 8vb-doubled cello 29/32 of the opening 32
  beats — do **not** add more bass (Maestro <150 Hz 4.86% already >
  Skidmore 4.30%). v4 rested Cb on bars 7–16 (ticks 5040–16320).
- `CYCLE-B55I-01`: Cb REST bars 3–9 (cello theme). Opening tuttis may
  take Cb; the quiet theme does not.

### 5. All string desks on tuttis / motti

Every string desk that exists in the file plays tutti hits and motto
attacks. Viola silent is a defect.

- `CYCLE-B5I-01` v1: viola silent bars 1–5 (first Vla note at 17.26s).
  Critic: add Vla on motto hits at G3. v2 added 6 notes.

### 6. Timpani on tutti tonic/dominant hits — do not auto-8vb

- Hits on tutti tonic/dominant. No rolls. GM 47, pitched, not ch.10.
- Do **not** auto-drop timp an octave to “add bass.”
- `CYCLE-B5I-01` v1: first hit was beat 6 D3 (3.92s); missing the
  first motto long (beat 2 / 0.80s). v2 put G2/C3 on both motto longs.
- `CYCLE-B55I-01` v6: retune opening timp Eb3→Eb2. First-4s 20–150 Hz
  went to **26.7% vs gold 11%** and stayed there through v10. That
  overshoot is the lesson: do not auto-8vb timp (or everything else).

### 7. Hard clip from the job card

Sounding MIDI ends at the card’s clip (barline after the last wanted
phrase). `CYCLE-B5I-01` ~2 min; `CYCLE-B55I-01` ~1 min. FluidSynth
release tail may run a few seconds past; the MIDI last note-off must
not.

---

## Do **not** encode as defaults

These showed up as critic asks and then as overshoots. They are
**local**, not v1 rules:

| Don’t | Why (measured) |
| --- | --- |
| Always add bass | B5I v1 already above Skidmore <150 Hz (4.86 vs 4.30). Later theme-window 24.88% vs 0.71% until Cb rested. |
| Always drop another octave | Eroica critic stacked Cb then Vc/Bn 8vb; opening timp Eb2 overshot first-4s bass 26.7% vs 11%. Floors exist so you stop. |
| Always more timp | Eroica v7–v8 piled late Eb2 hits; bars 25–36 bass closed on gold (17→20.6 vs 21.6%) — then **stop**. Opening Eb2 still overshot; more timp does not fix that. |

Silence is legal. A quiet theme on Vc + Bn + Vla 8ths is a valid bar.

---

## Hand-off

1. Write v1 SMF (Type 1, PPQ 480, named desks, this GM map).
2. Run this checklist in code; fix the MIDI; do not log green otherwise.
3. Give v1 to critic. Critic emits 1–2 **new** JSON patches per cycle
   ([`critic-patches.md`](critic-patches.md)).
4. Apply with `scripts/apply_critic_patches.py`. Next critic pass
   confirms previous ids **APPLIED**.
5. Anything the schema cannot express → Maestro rewrite, not a patch.
