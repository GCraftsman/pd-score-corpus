# Piano solo → invented orchestra (Maestro)

**North star:** the user plays a piano idea; the app emits a **full orchestra MIDI** you can hear now (GM) and open in GarageBand / Logic. **Keep the user’s tune.** Inner desks may embellish and play *with* it. Do **not** replace the tune with analog material. Do **not** match a famous recording of a different piece.

This is **not** CYCLE-* (reconstruct a symphony from its piano reduction toward that symphony’s gold).

Inputs: piano MIDI (user or `is_piano_only` corpus row) + 0–3 analog listen-notes from [`analog-matching.md`](analog-matching.md). Then SKILL.md steps 3–12 + this file. **v1 must still run [`first-pass.md`](first-pass.md)** (duty, tutti chop, no default +12, locked GM).

Output: SMF Type 1 per [`midi-contract.md`](midi-contract.md). Filename may use ensemble token `orchestra` (app path) rather than `strings`/`baroque`. Metadata: `arrangement: experimental, CC0` + analog slugs if any.

---

## 1. Preserve the tune

1. Skyline (SKILL.md §5A) **is** Violin I (optional flute 8va *only* if first-pass.md allows and the analog’s melody register is high — never a default +12).
2. Skyline pitch-class match in Vln I ≥ **85%** of active 1/32 buckets (same success bar as experiments.md).
3. Do not borrow analog pitches, motives, or bar-aligned rhythms onto Vln I.
4. If the analog suggests “melody in winds,” that means *color later in a climax*, not “delete the violin tune.”

---

## 2. Embellish, don’t overwrite

Inner voices and extra desks may:

- Pad (held chord tones, horns).
- Ostinato (one choir, SKILL.md §5D).
- Answer the tune (short wind echoes **after** a phrase, not on top of it).
- Walk the bass instead of pedal, if the analog’s *role* was walking — invent the walk from the **piano’s** bass pitch classes, not from analog notes.

They may **not**:

- Play a second tune that fights the skyline.
- Spray every piano 16th onto five desks (SKILL arpeggio rule).
- Copy analog inner figures.

Rimsky (PD, paraphrase): give the melody a color the accompaniment does not share.

---

## 3. Layer by section (shape, not gold bars)

Segment the **piano** clip into 4 buckets by time (not by analog bar numbers):

| Bucket | Rough span | Default layer |
| --- | --- | --- |
| intro | first ~15–20% | strings only, or Vln I + bass; winds tacet |
| verse / body | middle | add pad (horns/vla) and bass duty; keep density moderate |
| climax | loudest / densest piano window | winds double melody at cadences; brass/timp only if era table allows and piano velocity is high |
| thin | last phrase or after a cadence | drop winds; leave tune + bass |

Use analog listen-notes only as **when-to-add** hints (“winds enter after the texture has been going a while,” “thins after cadences”), mapped onto *these piano buckets*, never onto analog measure numbers.

Era still comes from the **piano composer** (or the user’s stated era), not from the analog’s composer. A Chopin waltz with a Mozart minuet analog still uses romantic-small orchestra, not a Mozart symphony roster.

---

## 4. When to add winds / brass / pads

| Piano texture (SKILL §4) | Start with | Add if analog role-notes say so |
| --- | --- | --- |
| `unaccompanied` / thin melody | Vln I + Vc | pad horns in verse only |
| `chorale` | SATB strings | horns pad; no arpeggio spray |
| `arpeggio` | outline on strings; harp only if romantic token | winds on outline at climax |
| `ostinato` | ostinato on **one** choir (vla or horns) | do not tutti the ostinato |
| `waltz` / dance | oom-pah strings + Vln I | winds on cadences |
| `polyphony` | one stream per desk, no chord fill | no analog “pad” that smears the invention |
| `homophony` / `storm` | strings + bass duty | winds/brass at climax only |

Leave piano texture on strings when the analog is chamber/strings and the piano is quiet. Full tutti is a climax color, not a default (first-pass.md tutti chop still applies).

---

## 5. v1, critic, product

1. Arrange from piano + analog *roles*.
2. Run [`first-pass.md`](first-pass.md).
3. Bounce GM (FluidSynth). This **is** the listen-now product preview.
4. Critic: [`analog-critic.md`](analog-critic.md) — 1–2 role/density asks. Same-work patch schema is optional; role-adds that need a new desk are **Maestro prose**.
5. Stop after the coordinator’s pass count. Do not chase analog hall or exact BPM.

Success: GarageBand/Logic File→Open; user’s tune obvious on Vln I; bass exists; it is not a stereo bounce and not a copy of the analog recording.
