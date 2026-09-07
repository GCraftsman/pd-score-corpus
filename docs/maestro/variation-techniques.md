# Variation techniques (random first-pass catalog)

Named recipes Sketch Artist may **bake into a sketch** and Maestro may **randomly apply** on first pass. Bind: **never override** [`harmony-rules.md`](harmony-rules.md). If a roll would break the labeled progression or (unless the technique *is* inversion) skyline recognizability, **do not apply** — log `SKIP <name> <reason>`.

Pick **0–2** techniques per 30–60s cue (uniform among those that pass the preflight). Log `rolled:` and `applied:` separately.

**Default Sketch roll pool (prefer):** `melody_inversion`, `left-to-right mirror`, `high/low part inversion`, `meld`, `rhythm-from-A + notes-from-B` — single-source / non-gap transforms. **Do not roll** `patchwork` or `gap-fill` on new sketches unless the job card sets `patchwork: true` (gap-fill only makes sense with patchwork gaps).

Window sizes are in **bars of the home meter** unless noted. MIDI is PPQ 480, concert pitch.

Skyline recognizability (non-inversion techniques): after the recipe, SKILL.md skyline pitch-class match vs the **pre-technique** skyline ≥ **70%** of active 1/32 buckets in that window, **or** skip.

---

## patchwork

> **RETIRED for default Sketch jobs.** Do **not** roll on new sketches unless the job card explicitly sets `patchwork: true`. Section kept for history / old NOTES. Prefer single-source transforms below.

**What:** 2-bar quotes from source A, 1-bar gaps (silence or hold) before the next quote.

**Steps:**

1. Segment the sketch/piano into 2-bar cells aligned to labeled chords (do not start a quote mid-bar unless the seam is a labeled chord change).
2. Place quote, quote, **gap** (1 bar), quote… Gap: all desks rest, **or** bass holds the labeled chord root (choose one per cue; default hold-root).
3. Quotes keep original IOIs and PCs (after home-key transpose).

**Must not break:** labeled chord of each quoted cell; skyline inside a quote (it *is* the quote). Gap bar must still be labeled (usually continue previous chord or the next chord as a pedal).

**SKIP if:** a 2-bar window contains two conflicting labeled chords that the quote would smash.

---

## meld

**What:** spine (skyline + labeled bass) from A, motor (ostinato/inner rhythm) from B.

**Steps:**

1. A = user’s/sketch tune (skyline + bass PC per bar). B = another transposed PD patch or a generated ostinato on chord tones.
2. Motor: take B’s IOIs in a 1-bar loop; retarget each attack to the **nearest chord tone** of the labeled chord (not B’s original PCs if they clash).
3. Assign motor to **one** choir (viola or horns), not the whole orchestra (SKILL.md ostinato rule).

**Must not break:** A’s skyline PCs; labeled chords (motor PCs ⊆ chord tones + passing on offbeats only).

**SKIP if:** B’s meter ≠ home meter and you cannot resample IOIs to the bar without changing attack count by >25%.

---

## gap-fill

> **RETIRED for default Sketch jobs.** Do **not** roll unless the job card sets `patchwork: true` (and gaps exist). Section kept for history. Prefer non-gap recipes.

**What:** Maestro writes the silent bars up to the next labeled chord.

**Steps:**

1. Find spans with no piano/sketch notes but a labeled chord on the **next** attack (or a 1-bar gap from patchwork).
2. Fill with **chord tones only**: bass root or fifth; optional inner pad; optional Vln I neighbor that resolves to the next skyline PC.
3. Density: thinner than adjacent quoted bars (≤2 desks).

**Must not break:** next labeled chord; do not start a new tune in the gap.

**SKIP if:** gap > 2 bars (leave rest; don’t noodle).

---

## melody inversion

**What:** invert skyline about an **axis pitch**.

**Steps:**

1. Axis `A` = median skyline pitch of the window, or a labeled chord tone nearest that median (prefer scale degree 1 or 5 of `K`).
2. Each skyline pitch `p` → `2A - p`. Clip into Violin I practical range by octave **after** inversion if needed (first-pass: no default +12 as a style add; range clip is OK).
3. Inners/bass stay on labeled chord tones (re-voice if the inverted tune now collides unison with an inner — move the **inner**).

**Must not break:** labeled chords (bass/inners). Skyline recognizability **does not** apply (this technique IS inversion). Downbeat skyline still chord-tone or `skyline_appoggiatura` per harmony-rules §5.

**SKIP if:** after inversion, >30% of downbeat skyline PCs are outside the labeled chord **and** cannot be called neighbor/appoggiatura.

---

## left-to-right mirror

**What:** reverse a window in time.

**Steps:**

1. Window = 1 or 2 complete bars (labeled-chord aligned).
2. Reverse attack order: `t' = t_end - (t - t_start) - duration` (keep durations). PCs unchanged.
3. If the reversed bass PC on the **downbeat** is not a chord tone of that bar’s label, swap the last and first bass notes **or SKIP**.

**Must not break:** the **bar’s** labeled chord (all downbeats after reverse). Skyline match vs original will fail — require instead: set of skyline PCs in the window is **unchanged** (same multiset).

**SKIP if:** window crosses a labeled seam (two chords) unless both bars share the same label.

---

## high/low part inversion

**What:** RH/LH or melody/bass **register swap**.

**Steps:**

1. Skyline notes move **down** by `d` semitones, bass notes **up** by `d`, where `d` = (median_skyline − median_bass) clipped so both land in practical ranges (Vln I 55–100, Cello/bass 28–76). Typical `d` ≈ 12–24.
2. If a swapped bass note is now above the swapped tune, reduce `d` until tune > bass on downbeats.
3. Re-check chord tones: after swap, bass PC on downbeats ⊆ labeled chord. If not, pick the nearest chord-tone **pitch class** in the new register (keep PC class, change octave).

**Must not break:** labeled progression (PCs); the tune must still be the higher line on downbeats.

**SKIP if:** no `d` in 8–24 keeps both in range and bass PC legal.

---

## rhythm-from-A + notes-from-B

**What:** IOIs from A, pitch classes from B (then snap to labeled chords).

**Steps:**

1. A, B = two windows of equal **attack count**, or truncate the longer.
2. Output attacks use A’s IOIs (start times relative to window). PCs cycle through B’s PC sequence (after transpose to `K`).
3. Snap each PC to nearest **chord tone** of the bar it lands in (≤ 2 st). If snap > 2 st, drop that attack.
4. Apply to **motor/inners** by default. Apply to skyline only if Sketch Artist marked the window `skyline_swap: true`; then recognizability vs original skyline is waived for that window only.

**Must not break:** labeled chords after snap; default skyline if `skyline_swap` is false.

**SKIP if:** attack counts differ by >1 and cannot truncate; or >40% attacks drop at snap.

---

## Preflight (every roll)

```
if technique in (patchwork, gap-fill) and job.patchwork != true: SKIP  # retired default
if would_change_labeled_chord_tones_of_downbeats: SKIP
if technique != melody_inversion and skyline_pc_match < 0.70: SKIP
if technique == left_to_right_mirror and window_crosses_seam: SKIP
log SKIP or APPLIED with window bars
```

Maestro still runs [`first-pass.md`](first-pass.md) after recipes. Techniques do not unlock GM 48/49, default +12, or analog pitch copying.
