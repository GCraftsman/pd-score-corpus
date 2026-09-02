# Critic rubric — analog refs (not same-work gold)

Compare the Maestro **GM bounce** to the **analog recording(s)** for **role, density, and accompaniment ideas** only.

This is **not** CYCLE gold. Forbidden: “match the gold MIDI numbers,” note-for-note or bar-aligned pitch matching, copying analog motives onto the piano tune, chasing analog tempo or hall.

---

## Allowed (1–2 asks per pass)

Write instructions Maestro can apply to the **piano-derived** MIDI:

- “Horns could pad in the quiet 8 (verse bucket).”
- “Thin the mid: too many simultaneous inner-string notes vs analog’s spare accompaniment.”
- “Bass could walk instead of pedal in the body (use piano bass PCs, not analog notes).”
- “Winds enter too early; keep intro strings-only.”
- “Ostinato is on too many desks; leave it on viola only.”
- “Climax has no color change; double Vln I with flute at cadences only.”

Each ask names a **section bucket** (intro / verse / climax / thin) or a **desk family**, not analog bar numbers and not analog pitches.

---

## Forbidden

- Transcribe analog melody/bass/inner pitches.
- “Bar 12 analog does X, do X at tick N.”
- Time-stretch or retune Maestro to analog BPM/hall.
- Replace Violin I (the user’s tune) with analog material.
- Williams/Zimmer/cinematic language.
- Re-litigating first-pass.md (fused 8ths, locked GM, default +12). If v1 skipped hygiene, say `first-pass miss` and stop.

---

## Patch schema vs prose

[`critic-patches.md`](critic-patches.md) + `scripts/apply_critic_patches.py` are **note-level ops on existing desks** (same-work CYCLE tool): transpose a range, drop a desk in a tick window, velocity/CC, etc. They **do not invent new desks or GM programs**.

| Critic thought | Vehicle |
| --- | --- |
| Thin/drop/quiet an existing desk in a window | JSON patch (`mute` / velocity / drop-range) if the op exists |
| Walk bass / change figuration / add horn pad that is **not** already a track | **Maestro prose** in NOTES.md (`critic_prose:`). Do **not** fake a patch. Do **not** extend the applier in this playbook. |
| “Add trumpet desk” | Prose. Applier fail-closed on unknown desks. |

If a pass is all role-adds, emit **zero** JSON patches and two prose lines. That is a valid critic turn.

Cap: **1–2** asks total (patches + prose combined).

---

## Listen recipe

1. Loudness-normalize both (same as `targets/README.md`). Do not score “too quiet.”
2. Do **not** require beat-alignment to the analog. If tempos differ, still judge *roles* and *density shape*.
3. If no analog was chosen, critic only against SKILL.md / first-pass.md / piano-solo-arrange.md — no invented gold.

Log analog slugs + the 1–2 asks in NOTES.md. Then yield.
