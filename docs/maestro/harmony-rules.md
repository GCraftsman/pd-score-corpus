# Harmony rules (sketch + first pass)

**Job:** one **labeled chord progression** in one **home key**, then piano ideas / PD patches are voiced into those chords. For the future app (user piano → original-feeling GM orchestra).

Not CYCLE same-work gold. Do **not** match analog MIDI numbers. Do **not** scrape YouTube or copyrighted film scores. “Modern film-score sound” here means **progression + texture** on PD 18th–19th c. material, not Zimmer pastiche. Rimsky (PD) is OK as color craft; do not paste Adler/Piston/Kennan.

Sketch Artist **writes** the labeled progression. Maestro **obeys** it on first pass ([`piano-solo-arrange.md`](piano-solo-arrange.md), [`first-pass.md`](first-pass.md)). Variation recipes in [`variation-techniques.md`](variation-techniques.md) **never override** this file. If a roll would break a labeled chord, `SKIP` and log.

---

## 1. One home key

1. Pick a home key `K` (e.g. C minor) from the user’s piano idea: last clear cadence, or the mode of bar-1 pitch-class set, or the sketch card.
2. **Transpose every other source** (PDMX patch, analog is *not* a pitch source) into `K` **before** stitching. Store `transpose_semitones` on each source in NOTES.md.
3. Accidentals outside `K` are allowed only as: leading-tone to the next labeled chord, borrowed bVI/bVII in minor, or a **justified** chromatic mediant (see seams). Otherwise rewrite the inner voice to the labeled chord tones.
4. Do not modulate to a second tonic in a 30–60s v1 cue unless the sketch explicitly labels a new key with a pivot bar. Default: **one tonic**.

MIDI check: after transpose, ≥80% of non-skyline onset PCs in each labeled bar are in that bar’s chord-tone set (triad + optional 7th if labeled). Skyline may include passing/neighbor tones (see §5).

---

## 2. Allowed seam types

A **seam** is the join between two labeled chords (or two patches). Only these:

| Name | Roman (major home unless noted) | MIDI test |
| --- | --- | --- |
| Tonic pedal / I–V–I | I → V → I (minor: i → V → i) | bass PC is 1 then 5 then 1 of `K` |
| Authentic | V → I or V7 → I (minor: V → i) | dominant function then tonic; bass 5→1 |
| Half | I/ii/IV/vi → V (minor: i/iv/VI → V) | ends on V, not I |
| Deceptive | V → vi (minor: V → VI) | bass 5→6; not 5→1 |
| i–VI–III–VII | natural-minor / Aeolian loop | chord roots 1, b6, b3, b7 of `K`; next may be i or III |
| Circle of fifths | roots drop 7 semitones (or rise 5) each seam, 3+ steps | root motion ±5 or ±7 st each join |
| Common-tone | two triads share ≥1 PC; other voices move ≤2 st | shared PC held |
| Chromatic mediant | roots ±3 or ±4 st, **same quality** (M→M or m→m), ≥1 common tone **or** log a PD precedent (e.g. Schubert/Liszt mediant in allowlisted corpus) | if no common tone and no NOTES precedent, **illegal** |

Secondary V/x is allowed **once** per 8 bars, targeting the next labeled chord (V/V → V). No chains of applied chords in v1.

---

## 3. Cadence map for a 30–60s cue

Time is the **piano/sketch** timeline, not analog bars. Default 4/4; scale if 3/4.

| Region | ~span | Harmony job |
| --- | --- | --- |
| open dark | first 20–30% | tonic or i–VI; **no** authentic close; prefer i or i–v half-open |
| lift | middle | move (circle, mediant, or i–VI–III–VII); may hit V or III |
| punch close | last 15–25% | authentic V→I/i, or deceptive V→VI if the sketch wants open-ended |

Do **not** copy a famous cue’s changes (no “that Batman minor i–VI–III–VII as gold,” no transcribing a Williams cue). The **functions** (dark tonic, lift, close) are allowed; the **specific famous voicing** is not.

MIDI check: there is ≥1 half or authentic cadence in the last 25% of sounding duration, **or** a labeled deceptive close logged as intentional. Opening 20% does not contain V→I/i unless the sketch labeled a cold open on dominant.

---

## 4. Forbidden

- Random chromatic smash (two consecutive seams that are not in §2).
- Quoting a third work’s **progression** as gold (including analog recordings — analogs are texture only, [`analog-matching.md`](analog-matching.md)).
- Chasing analog MIDI numbers / bar-aligned pitch from a recording.
- Replacing the user’s or sketch **skyline** to “fix” harmony (voice-lead **inners and bass** into the labeled chord; passing tones on the tune are OK).
- Dual tonic, atonal stacks, or cluster-as-chord unless the sketch explicitly labeled a cluster bar (v1: don’t).
- CYCLE gold matching language on an ARRANGE / app-path job.

---

## 5. How to label a bar

Every sounding bar (or every 2 beats in 3/4 if the sketch is faster) gets:

```
bar: 7
roman: V7/i
abs: G7
root_pc: 7
quality: 7
key: C minor
```

- `roman` is relative to home `K`.
- `abs` is letter name after transpose (C, Cm, G7, Ab, …).
- Chord-tone PCs = triad of `abs` (+ 7th if `7`/`m7`/`dim7` in the label).
- Sketch writes this table. Maestro **does not invent** a competing progression.

Maestro first-pass check against the sketch table:

1. For each labeled span, collect inners + bass PCs (exclude skyline).
2. `in_chord = count(pc in chord-tone set) / count(all)`.
3. **Pass** if `in_chord ≥ 0.80` per span.
4. If fail: move **bass and inners** by ≤2 semitones toward nearest chord tone (greedy). **Do not** rewrite skyline pitch classes except octave (range clip).
5. Skyline may use passing/neighbor PCs on weak 16ths; on downbeats of a labeled bar, skyline PC should be chord-tone **or** log `skyline_appoggiatura` (max 1 per 2 bars).

Log `harmony_pass: true/false` and any `SKIP` variation rolls.
