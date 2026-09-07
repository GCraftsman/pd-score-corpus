---
name: desk-roles
description: Use when a Maestro job card rotates choir roles across form regions (theme_owner_plan, ensemble: piano-strings-horns-ww, perc: final_pass_only) — lawsuit-safe craft vocabulary and region handoffs, no living film composers.
---

# Desk roles (choir rotation across form)

**Job:** assign **who does what** per form region so the tune, bed, color, and pulse stay clear. Lawsuit-safe acoustic craft only — no living film composers, no franchise names, no “sound like X.”

**When:** job card sets any of:

- `theme_owner_plan: …` (region principal handoff)
- `ensemble: piano-strings-horns-ww(+perc last)`
- `perc: final_pass_only`
- or an explicit per-region role table

If unset, fall back to era maps in [`orchestration-rules.md`](orchestration-rules.md) and theme ownership in [`theme-development.md`](theme-development.md) (default Vln I).

**Legal note (not advice):** Role rotation is orchestration craft (Rimsky-style color paraphrase OK). It is **not** a pastiche of a commercial media house. See [`../../LEGAL.md`](../../LEGAL.md) §11 and [`style-targets.md`](style-targets.md).

---

## Vocabulary (USE these words only)

In NOTES.md, patches, and critic prose, use **only** this vocabulary for desk jobs:

| Allowed term | Meaning |
| --- | --- |
| **principal** / **cantabile** / **thematic statement** | Who owns the tune in this region |
| **harmonic bed** / **sustained sonorities** / **pads** | Long chord tones; little motion |
| **obbligato** / **countermelody** / **color** | Secondary moving line (not the principal) |
| **motor** / **pulse** / **ostinato** / **rhythmic scaffolding** | Repeated attack pattern on **chord tones** |

### Never write (banned in NOTES / patches)

`melody` · `harmony` · `support` · `rhythm-drive` · living-composer / film / franchise labels as role names

If a human or old note used a banned word, **rewrite** to the table above before logging.

---

## Default roster

### When job says `ensemble: piano-strings-horns-ww(+perc last)`

| Always on | Locked until final ironing |
| --- | --- |
| **Piano** (Acoustic Grand, GM 0) — stays in the score | **Percussion** (timp / triangle / cymbals / soft roll) |
| Strings (Vln I/II, Vla, Vc, Cb) | |
| Horns | |
| Woodwinds (Fl, Ob, Cl, Bn as era allows) | |

Piano track stays **live** for the whole cue (it may rest in a region, but the track remains). Do not delete the piano desk because another choir took principal.

### When job says `perc: final_pass_only`

- **First orchestra pass:** no timp, no triangle, no cymbals, no drum-kit GM, no perc desks with notes.
- **Last ironing pass only** (after critic density/theme checks): light **PD-era** percussion — downbeat punctuation and/or a soft roll at a labeled climax. Not a kit groove. Not constant wash.

Log: `perc: locked` on early passes; `perc: final_pass_added` on the last.

---

## Theme handoff (`theme_owner_plan`)

When the job card sets `theme_owner_plan` (or equivalent region list), **principal** rotates as follows unless the card overrides with an explicit table:

| Region | Form role (guide) | Principal owner |
| --- | --- | --- |
| **A** (open) | First thematic statement / open | **French horns** (soft cantabile or clear statement — not a brass smash) |
| **B** (middle) | Contrast / develop | **Woodwinds** — prefer **clarinet or oboe solo**, not tutti WW |
| **C** (close) | Return / close | **Piano** (Acoustic Grand) owns principal |

Other choirs each region are reassigned among **harmonic bed**, **obbligato/color**, and **motor/pulse** — one choir per job when possible (do not put motor on the principal desk during a full thematic statement).

### Example per-region table (log this shape in NOTES)

```
theme_owner_plan:
  A (bars 1–6):
    principal: Horns
    harmonic_bed: Strings (Vln II / Vla / Vc pads)
    obbligato: Clarinet (sparse)
    motor: none | Vla pulse on chord tones
  B (bars 7–14):
    principal: Clarinet (or Oboe) solo
    harmonic_bed: Horns pads
    obbligato: Vln I color (not competing statement)
    motor: none | low strings pulse
  C (bars 15–20):
    principal: Piano
    harmonic_bed: Strings
    obbligato: Horns soft
    motor: none
    perc: (final pass only) timp downbeat at last climax
```

Bar ranges come from the job card / sketch form. If the cue is shorter, shrink regions but keep A→B→C ownership order.

### Interaction with theme-development.md

- Spotting / statement budget / anti–loop-spam still apply ([`theme-development.md`](theme-development.md)).
- “Owner” there defaults to Vln I; **`theme_owner_plan` overrides** region by region.
- Full thematic statements still need contrast between returns; handoff ≠ permission to spam the tune on every desk.

---

## Assignment rules (every region)

1. **One principal** choir/desk for the region.
2. **Motors off the principal desk** during a full thematic statement.
3. Harmonic bed uses chord tones of the labeled harmony ([`harmony-rules.md`](harmony-rules.md)).
4. Obbligato is thinner and usually lower velocity / CC11 than principal.
5. Do not assign the same figure to every desk (register contrast — see [`large-ensemble-preview.md`](large-ensemble-preview.md) when `preview: large-ensemble`).
6. Era ranges and GM map: [`orchestration-rules.md`](orchestration-rules.md), [`first-pass.md`](first-pass.md).

---

## Critic checks

- Can you name the **principal** desk per region from the bounce?
- Is banned vocabulary absent from NOTES/patches?
- Was perc silent until final pass when `perc: final_pass_only`?
- Did piano remain in the score when the ensemble flag required it?

Forbidden critic ask: “more like [living composer] brass handoff.”

---

## NOTES fields

```
ensemble: piano-strings-horns-ww(+perc last)
perc: final_pass_only | final_pass_added
theme_owner_plan: true
desk_roles:
  A: { principal, harmonic_bed, obbligato, motor }
  B: { ... }
  C: { ... }
```
