---
name: theme-development
description: Use when a job card says theme: develop, or when Sketch Artist / Maestro must spot a theme-worthy skyline, develop it into a catchy overarching melody, and place returns without loop-spam — bound by harmony-rules and lawsuit-safe packs.
---

# Theme development (film-score app loop)

**Job:** from a Sketch Artist / Maestro **sketch MIDI**, recognize what is theme-worthy, develop it into a catchy overarching melody (“the theme”), and place/emphasize it so a listener can hum it — without making it a 2-note tag or hammering it on repeat.

**When:** job card sets `theme: develop`. If unset, do **not** force a theme cycle; keep the sketch skyline as-is under [`piano-solo-arrange.md`](piano-solo-arrange.md).

**Who:**

| Role | Does |
| --- | --- |
| Sketch Artist | May tag `theme_candidate:` in NOTES (bars + pitch summary). Optional. |
| Maestro | Spots (or accepts the tag), develops, places statements on first pass when `theme: develop`. |
| Critic | Checks “theme audible?” and “overused?” — role/density only; may ask to thin competing mid. |

**Bound by:** [`harmony-rules.md`](harmony-rules.md) (labeled chords stay), [`variation-techniques.md`](variation-techniques.md) (when rolling recipes), [`style-targets.md`](style-targets.md) (texture packs only), [`first-pass.md`](first-pass.md), [`../../LEGAL.md`](../../LEGAL.md) §11.

**Legal note (not advice):** Develop *this* sketch’s material. Do not write a franchise theme, name living composers/films, scrape YouTube, or quote a third famous tune. PD craft (Rimsky paraphrase for color) is OK. Style packs change texture, not the theme’s pitch identity.

---

## 1. Theme spotting (MIDI-testable)

Work from the sketch’s **skyline** (highest active pitch-class stream per SKILL.md / piano-solo-arrange), not from the motor.

### 1.1 Candidate windows

Scan overlapping windows of **4–8 bars** (prefer 4 or 8 in the home meter). For each window, extract the skyline note sequence (onset, MIDI pitch, duration in ticks).

**Reject as theme if any hold:**

| Test | Fail when |
| --- | --- |
| Too short | &lt; **8** distinct note onsets **or** &lt; **4** bars of sounding skyline |
| Tag / fanfare fragment | ≤ **4** onsets total (2-note tags always fail) |
| Motor / ostinato | Same pitch-class set + IOI pattern repeats every 1 bar for ≥ 3 bars on that desk — that is accompaniment, not theme |
| Unpitched wash | ≥ 80% of onsets are the same pitch class |
| Competing bass | Candidate is mostly the bass desk doubled up an octave |

### 1.2 Score candidates (pick the best)

Log scores; pick the highest that passes minimums.

| Feature | How to score (0–1) | Prefer |
| --- | --- | --- |
| Length | `min(1, n_onsets / 12)` after clamp to 8–16 onsets ideal | ~8–16 notes |
| Contour mix | fraction of intervals that are steps (1–2 semitones) in **[0.35, 0.75]** → 1; outside → lower | step + leap mix |
| Leap identity | at least **one** leap ≥ 3 semitones and ≤ 12; none → 0.4 | memorable peak |
| Rhythmic identity | unique IOI pattern vs a flat stream of equal 8ths (edit distance) | not all equal |
| Register | median pitch in practical Vln I / flute range (G3–E6 concert) | singable |
| Sketch tag bonus | +0.15 if Sketch Artist `theme_candidate` overlaps ≥ 50% of bars | honor the tag |

**Minimum to accept:** length ≥ 0.5, contour ≥ 0.4, not motor. Else log `theme: none_found` and keep sketch skyline without a formal statement cycle.

Log:

```
theme_candidate_bars: [start, end]
theme_n_onsets: N
theme_score: ...
theme_source: sketch_tag | spotted
```

---

## 2. Development (not pastiche)

Operate **only** on the chosen theme’s pitch/rhythm cells. Snap every developed pitch to the **labeled chord tones** of the bar (passing tones on weak parts of the beat only, per harmony-rules).

### Allowed transforms

| Name | What | Bound |
| --- | --- | --- |
| sequence | Restate cell starting on a new scale degree / chord | New pitches ⊆ labeled chord tones (+ diatonic steps between) |
| inversion | Mirror intervals around the first note’s axis | Skyline recognizability rule from variation-techniques **waived** only for windows marked `technique: inversion` |
| fragmentation | Use first 3–5 onsets as a call; answer with harmony fill | Do not fragment below 3 onsets as a “statement” |
| extension | Add 1–2 bars of chord-tone continuation after the cell | Same home key; no new modulation |
| register transfer | Same PCs/IOIs, octave shift to another allowed desk | Desk must be in era GM map; theme ownership rules in §4 |

Pick **1–2** transforms per 30–60s cue for *returns* (not for the first full statement). Log `theme_dev: sequence+fragmentation` etc.

### Forbidden in development

- Inventing a **competing** chord progression
- Quoting or aiming at a **third famous tune** (any franchise / anthem / pop hook)
- Borrowing a living-composer motive “for catchiness”
- Turning the motor into the theme by loudness alone

---

## 3. Placement / emphasis (anti–loop-spam)

For a **30–60s** cue (typical app path):

| Slot | What | Bars (guide) |
| --- | --- | --- |
| A — first statement | Full theme (4–8 bars), clear | After a short intro **or** starting by bar 3–5 — not required on bar 1 |
| B — contrast | No full theme; motor/pad/fragment only | ≥ **4** bars or ≥ 25% of cue |
| A′ — return | Full or lightly developed | After contrast |
| A″ — climax (optional) | Full theme, louder / thicker | Only if cue ≥ ~45s **and** statement budget allows |

### Statement budget

| Cue length | Max **full** statements | Min silence/contrast between full statements |
| --- | --- | --- |
| ≤ 35s | **2** | ≥ 4 bars or ≥ 8s |
| 36–60s | **3** | ≥ 4 bars or ≥ 8s |
| &gt; 60s | **4** | ≥ 6 bars |

**Full statement** = ≥ 75% of the theme’s onsets in order (PC match), same rhythmic identity ± ornament.

Fragments (≤ 5 onsets) may appear once in the contrast region; they **do not** count toward the max, but if fragment count &gt; 3, Critic should flag overuse.

Log:

```
theme_statements: [[bars], [bars], ...]
theme_contrast_bars: [...]
```

### Emphasis (without screaming)

- First and climax statements: skyline velocity / CC11 above accompanying desks (~+15–25 velocity or CC11 15–20 higher).
- Contrast region: theme desk rests or holds long notes **not** outlining the full contour.
- Do not restate the full theme on consecutive phrases with no contrast.

---

## 4. Orchestration hand-off

| Rule | Detail |
| --- | --- |
| Owner | **Violin I** owns the theme by default. If `style_pack` allows (e.g. `heroic-brass` climax only), trumpet/horn may take **one** statement — then return to Vln I. |
| Motors off theme desk | Ostinato / detached mid 8ths stay on Vla, Vln II, or horns — **never** on the theme-owner desk during a full statement. |
| Doubling | Optional soft octave below (Vc or Hn) on climax statement only; no default +12. |
| Competing mid | During full statements, mid pads ≤ 2 voices; leave spectral room under the skyline. |
| Critic | May request `thin_mid` / density cuts so the theme reads — not pitch rewriting of the theme. |

---

## 5. Lawsuit-safe checklist

```
[ ] No living-composer / film / franchise names in NOTES or patches
[ ] No “write a [franchise] theme” job accepted — rewrite to style pack + this file
[ ] No YouTube / copyrighted cue as theme model
[ ] No third-work tune quote
[ ] style_pack (if any) used for texture only — theme pitches come from the sketch
[ ] Harmony labels unchanged by development
```

Fail → rewrite before critic cycle.

---

## NOTES.md fields (append)

```
theme: develop
theme_source: sketch_tag | spotted | none_found
theme_candidate_bars: [start, end]
theme_statements: [...]
theme_dev: ...
theme_owner_desk: Violin I
```

---

## Critic rubric (theme mode)

**Pass if:**

1. A listener (or onset skyline check) can find ≥ 1 full statement with PC-order match ≥ 75% to the logged candidate.
2. Statement count ≤ budget for cue length.
3. ≥ one contrast region without a full statement.
4. Theme-owner desk is not also running the motor during statements.

**Fail / ask (1–2 items):** “theme buried under mid,” “only a 2-note tag,” “statements back-to-back,” “motor on Vln I during A.”

Do **not** ask to match an external famous theme.
