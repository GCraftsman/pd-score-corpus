# Large-ensemble preview (density craft)

**When:** the coordinator job card sets `preview: large-ensemble`.  
**Default when unset:** era-match ensemble from [`orchestration-rules.md`](orchestration-rules.md) — do **not** auto-upgrade every job to this mode.

**What this is:** acoustic / engineering craft for a **denser listen-now GM orchestra**. Same harmony labels ([`harmony-rules.md`](harmony-rules.md)), same skyline rules ([`piano-solo-arrange.md`](piano-solo-arrange.md)), same variations ([`variation-techniques.md`](variation-techniques.md)). This file does **not** invent a new commercial harmonic language.

**What this is not:** a pastiche of any living film composer, franchise, or house trailer style. Do not name people or films. Do not copy a third work’s orchestration grid. Packs in [`style-targets.md`](style-targets.md) still apply for mood; this mode only thickens **texture** when the card asks.

**Legal note (not advice):** We thicken density and improve **render** ([`render-preview.md`](render-preview.md)) because those are generic production levers. We refuse named-style imitation and copyrighted-cue transcription because those create access + similarity evidence and living-composer branding confusion. See [`../../LEGAL.md`](../../LEGAL.md) §11 and [`style-targets.md`](style-targets.md) hard bans. Composition strategy stays on allowlisted PD-era craft.

---

## Preconditions

1. Job card has `preview: large-ensemble`.
2. First-pass hygiene still runs ([`first-pass.md`](first-pass.md)): detach 8ths, locked GM desks, no default +12, no GM 48/49 string ensemble as a fake “big” cheat.
3. Harmony bar labels exist; density changes must **not** rewrite chord labels.
4. If `style_pack` is set, obey that pack’s forbidden rows too.

Log: `preview: large-ensemble` in the NOTES.md block.

---

## Allowed levers (do these)

### 1. Register contrast

- Keep **one** low-weight layer (Cb + Vc roots) and **one** high motor or skyline. Do **not** put the same figure on every desk.
- Mid register (Vla / horns / clarinets) fills chord tones or slow pads — not a third copy of the motor.

### 2. Pad vs motor (one holds, one moves)

Rimsky-style color idea, paraphrased: at any 2-bar window, **one choir sustains** (pad) and **one choir moves** (motor / ostinato / detached 8ths). Swap roles at phrase seams, not every bar.

| Choir | Typical pad role | Typical motor role |
| --- | --- | --- |
| Strings | slow Vln II / Vla triad | Vln I skyline or detached mid 8ths |
| Winds | clarinet/bassoon hold | flute/oboe short answers after the phrase |
| Brass | soft horn pad | trumpet/horn **punctuation** only (see §4) |

Never: all three choirs motoring the same IOI grid.

### 3. Bass layering without mud

- Contrabass = root (or fifth on weak bars); Cello = octave above **or** slow countermelody on chord tones — pick one strategy per section.
- Do not stack Cb + Vc + Bsn + Tuba-like doubling on the same onset unless it is a labeled cadence downbeat.
- Leave 1–2 mid pitches empty under dense high activity.

### 4. Brass / percussion as punctuation

- Allowed at **labeled climaxes** and cadences only (harmony-rules cadence map / job-card markers).
- Hits: short brass chords or timp downbeats **aligned** to existing strong beats — not a constant wash, not a new ostinato on brass.
- Between climaxes: brass silent or soft horn pad ≤2 voices.

### 5. Long pads + short attacks

- Pads: duty ≥ 0.75 of written value (legato sustain).
- Motors / repeated 8ths: duty **0.20–0.25** beat per [`first-pass.md`](first-pass.md).
- Do not fuse pad and motor on the same desk in the same window.

### 6. Dynamic arc (MIDI, not hall-chase)

- Shape loudness with **velocity** and **CC11** (expression). Optional CC7 per desk for balance.
- Arc example for a 30–60s cue: thin/soft → build into climax → thin again. Numbers belong in NOTES (`vel_median_intro`, `vel_median_climax`).
- Do **not** fake “bigger” by chasing hall reverb inside the composition step — reverb is render-only ([`render-preview.md`](render-preview.md)).

### 7. Desk count (when card allows)

Era table still caps exotic instruments. Within classical/romantic GM desks already in first-pass:

- Prefer **more named desks with thinner parts** over fewer desks blasting tutti.
- Doubling: octave or unison only where [`orchestration-rules.md`](orchestration-rules.md) already allows; never +12 on skyline by default.

---

## Forbidden (fail closed)

| Forbidden | Why |
| --- | --- |
| Naming living composers, films, franchises, “trailer,” house-style brands | Living-composer / trademark / evidence risk |
| Copying a third work’s orchestration map (who doubles whom bar-by-bar) | Expression / substantial similarity |
| Pastiche checklists that reconstruct one commercial media house sound | Same |
| New harmonic language “because modern scores do X” | Harmony stays on our PD rules |
| GM Orchestra Hit, keyswitches, GM 48/49 as density cheat | Existing forbids |
| Spitfire / BBCSO / Kontakt renders as repo or training artifacts | EULA |
| Critic success metric “more like [name]” | LEGAL §11 |

If a human said a banned name, rewrite via [`style-targets.md`](style-targets.md) **and** keep this density mode only if the card still says `preview: large-ensemble`.

---

## Critic in this mode

- Still [`analog-critic.md`](analog-critic.md): **role / density / accompaniment ideas** vs a PD/CC analog from `targets/` (when present).
- Allowed asks: “pad too thin in mid,” “motor on too many desks,” “brass washing between climaxes,” “bass muddy under motor.”
- Forbidden asks: “more like [living composer],” “match the [film] brass stack,” pitch copying from any analog.
- Patches stay inside [`critic-patches.md`](critic-patches.md). Density fixes that need new desks or role swaps are Maestro rewrites, not silent pitch pastes.

---

## Checklist before bounce

```
[ ] Job card has preview: large-ensemble (else skip this file)
[ ] Harmony labels unchanged; skyline ≥85% unless technique is inversion
[ ] At most one motor choir per 2-bar window; one pad choir
[ ] Brass/perc only at labeled climaxes (or soft horn pad)
[ ] first-pass.md duty cycles applied
[ ] No banned names in NOTES / patches
[ ] Render via render-preview.md (optional but preferred) — wav not committed
```
