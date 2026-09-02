# Critic patches

Tiny JSON ops. Critic **emits**; `scripts/apply_critic_patches.py`
**applies**; Maestro owns first-pass arrange
([`first-pass.md`](first-pass.md)) and anything this schema cannot
express; coordinator owns the job card (clip / gold / id).

Schema file: [`../../schemas/critic-patch.schema.json`](../../schemas/critic-patch.schema.json).

---

## Cadence

1. Maestro ships v1 after [`first-pass.md`](first-pass.md).
2. Critic emits **1–2 NEW patches per cycle** (more only if they are
   independent: different desks or non-overlapping `tick_range`).
3. Apply:

   ```bash
   python3 scripts/apply_critic_patches.py \
     --midi IN.mid --patches patches.json --out OUT.mid
   ```

4. Next critic pass lists previous patch `id`s as **APPLIED** (or
   names the miss). Do not re-emit an applied id.
5. Dry-run (no write):

   ```bash
   python3 scripts/apply_critic_patches.py \
     --midi IN.mid --patches patches.json --dry-run
   ```

Fail closed: unknown `op`, unknown desk name, desk not in the SMF
track names, missing required args, duplicate `id`, `tick_range`
start ≥ end. The applier does not invent desks or GM programs.

---

## Patch object

Every patch:

| Field | Required | Meaning |
| --- | --- | --- |
| `id` | yes | Stable string. Next pass confirms it. |
| `op` | yes | One of the ops below. |
| `desks` | yes | Track names. Case-insensitive. `Violin I` / `Vln I` / `VlnI` match. |
| `tick_range` | yes | `[start, end)` absolute ticks. A note matches if **onset** ∈ range. |
| `bar_range` | no | `[start, end)` 1-indexed bars. Documentary; applier uses `tick_range`. |
| numeric args | per op | See table. |

Envelope:

```json
{
  "cycle_id": "CYCLE-B5I-01",
  "source_midi": "arrangements/…/….orchestra.v1.mid",
  "patches": [ { "id": "…", "op": "…", "desks": ["…"], "tick_range": [0, 480] } ]
}
```

Bare arrays are invalid. Unknown fields on a patch are invalid.

---

## Ops

| op | Args | Effect |
| --- | --- | --- |
| `set_duty` | `duty` > 0 (beats) | Set sounding duration to `round(duty * PPQ)` ticks. |
| `shorten_to_beats` | `beats` > 0 | Cap duration at `round(beats * PPQ)`; leave shorter notes. |
| `transpose` | `semitones`; optional `clip_lo` / `clip_hi` (0–127, default 0/127) | `pitch = clamp(pitch + semitones, clip_lo, clip_hi)`. |
| `rest` | — | Drop notes whose onset is in range. |
| `set_pitch` | `pitch` 0–127 | Retune matching notes. |
| `set_velocity` | `velocity` 0–127 | Set note-on velocity. |
| `add_note` | `pitch`; `duration_ticks` ≥ 1 **or** `beats` > 0; optional `velocity` (default 96) | Insert at `tick_range[0]` on each named desk. Does not create tracks. |

`set_duty` is the fused-8th fix (0.498 → 0.225). `shorten_to_beats` is
the “don’t lengthen, only cap” variant (Eroica 2-beat holds → ~1 beat).

---

## Desk matching

Match `track_name` meta, case-insensitive, after collapsing
punctuation/spaces and expanding `Vln`/`Vla`/`Vc`/`Cb`/`Fl`/`Ob`/`Cl`/
`Bn`/`Hn`/`Tpt`/`Timp`. Canonical names are the midi-contract table
(`Violin I`, `Flute 1`, `Timpani`, …).

Unknown token (e.g. `Banjo`, `strings`) → error. Known desk with no
track in this file → error. Conductor / unnamed tracks are never
targets.

---

## What the schema cannot express

Maestro rewrite, not a patch:

- New desks / GM program changes / Type 0→1 rebuilds.
- “Rest winds except tuttis” when tutti is a heuristic, not a tick
  range (encode the range or rewrite).
- Voice-leading (drop Vln II a 3rd to an octave below Vln I with a
  G3 floor) if it needs per-note pairing against another desk —
  `transpose` + `clip_lo` can do a uniform 8vb; mixed pairing cannot.
- Job-card clip / tempo map / gold alignment.

---

## Apply-then-verify

Critic cycle *n+1* NOTES block starts with `vN_followup:` and one
`APPLIED` / miss per previous id. Numbers (duty, MIDI pitch, counts),
not vibes. Same pattern as `CYCLE-B5I-01` and `CYCLE-B55I-01`.
