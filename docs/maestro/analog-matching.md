# Analog matching (before first pass)

**Job:** pick **1–3** PD/CC orchestra or strings *recordings* that feel like the piano idea in **tempo, meter, and mood/texture**. They are **not** the same work and **not** a transcription of the piano piece.

This is for the **future app** (user plays piano → listen-now GM orchestra). It is **not** CYCLE-* same-work gold (piano reduction vs that symphony’s recording). Do **not** write “match the gold MIDI numbers.” Do **not** use YouTube or label rips. Pool: [`../../targets/`](../../targets/) plus allowlisted corpus metadata to *reject same-work* pairs. Rimsky-Korsakov (PD) is OK as craft; do not paste copyrighted orchestration textbooks.

Maestro + Critic run this **before** [`first-pass.md`](first-pass.md). Write the chosen analogs into the NOTES.md block (`analogs:` list). If nothing in `targets/` fits, **say so and proceed with zero analogs** — do not scrape.

---

## 1. Fingerprint the piano source

From the piano MIDI (SKILL.md steps 3–4), log:

| Field | How |
| --- | --- |
| `bpm` | median tempo from conductor / set_tempo |
| `meter` | time signature (e.g. 3/4, 4/4, 6/8) |
| `texture` | piece-level label from SKILL.md step 4: `chorale` / `arpeggio` / `ostinato` / `waltz` / `polyphony` / `homophony` / `unaccompanied` |
| `era` | composer death-year table in [`orchestration-rules.md`](orchestration-rules.md) (baroque / classical / romantic) |
| `mood` | one word from texture + dynamics: `cantabile` if median velocity < 70 and `n_sim` low; `dance` if waltz/minuet meter; `storm` if `n_sim` high and velocity high; else `neutral` |
| `work_id` | composer + catalog (BWV, Op., K.) if known — **ban list for analog titles** |

Clip length is the coordinator’s job card. Analog duration may be longer; you will only *listen* to a similar span, not time-stretch the analog onto the piano.

---

## 2. Candidate pool

**In:** `targets/*/source.json` where `target_kind` is `orchestra`, `strings`, or `chamber`. Skip `target_kind: piano` (wrong medium). Skip any analog whose `corpus_pdmx_ids` or `work_title` is the **same work** as the piano source (same Op./K./BWV movement). A Beethoven 5/I orchestra file is **illegal** as analog for a Beethoven 5 piano reduction — that is CYCLE gold, not analog.

**Out:** YouTube, IMSLP performer-©, Stokowski-class copyrighted transcriptions, NC licenses, anything not in this repo’s `targets/`.

Current v1 pool (examples of *kind*, not a prescribed map):

| slug | kind | useful analog for |
| --- | --- | --- |
| `beethoven-op67-i` | orchestra, 4/4 allegro, dense | storm / homophony / high-energy 4/4 **other than Op.67** |
| `beethoven-op55-i` | orchestra, 3/4–ish Eroica pulse, long span | classical allegro **other than Op.55** |
| `mozart-k550-iii` | orchestra minuet 3/4 | dance / waltz / minuet **other than K.550** |
| `mozart-k421-iii` | chamber minuet 3/4 | smaller dance texture **other than K.421** |
| `bach-bwv1068-air` | strings cantabile | slow chorale / air **other than BWV 1068** (Wilhelmj FLAG still applies as *texture*, not as notes) |

Piano gold (`chopin-op28-20`, `bach-bwv846`, …) is **not** an analog for orchestra.

---

## 3. Match recipe (score, pick top 1–3)

Score each remaining candidate. Keep those with **score ≥ 3**, cap at 3. Tie-break: prefer `orchestra` over `strings` over `chamber`; prefer shorter files.

| Test | Points | Fail |
| --- | ---: | --- |
| Meter: exact same | +2 | — |
| Meter: compatible (2/4↔4/4, 3/4↔3/8, 6/8↔3/4) | +1 | 5/4 vs 4/4 = 0 and do not pick unless pool empty |
| BPM: analog global BPM within **±12** of source, or **±15%**, whichever is looser | +2 | if analog is >2× or <0.5×, drop |
| Texture: same SKILL label | +2 | — |
| Texture: cousin (`waltz`↔minuet-feel, `chorale`↔`cantabile` air, `homophony`↔`ostinato` with pad) | +1 | `polyphony` vs `chorale` = 0 |
| Era: same table | +1 | skip a romantic analog for a Bach invention unless nothing else exists |
| Mood word overlap | +1 | — |
| Same work / same catalog | **disqualify** | — |

Do **not** maximize “sounds like the famous recording of this piece.” Maximize “a listener would file these in the same *texture drawer*.”

Log: `analog_slug`, score breakdown, why same-work was rejected if it was a near miss.

---

## 4. What to extract from an analog (listen notes)

Listen to ~the clip length (or 60–90 s). Write **prose roles**, not MIDI.

**Extract:**

- Who has **melody** vs **pad** vs **bass** vs **ostinato** (desk families, not pitches).
- **Density by section** (intro thin / middle tutti / end thin) in bars of the *analog*, as a *shape*, not a map onto the piano’s bar numbers.
- **Register**: melody high vs mid; bass weight light vs heavy.
- **When winds enter**; when texture **thins**.
- Articulation family: detached 8ths vs sostenuto pad (words only).

**Never extract:**

- Pitches, scale degrees, or chord labels from the analog.
- Motives, licks, or distinctive inner-voice figures.
- Bar-aligned rhythms (“bar 17 analog does this, copy it”).
- Hall, mic, vibrato, or exact BPM microtiming.

The analog is a **role cartoon**, not a score to transcribe. Rimsky’s craft reminder (PD): a tune wants a *clear* color; accompaniment wants a *different* color — do not put the same figure on every desk.

---

## 5. Hand-off

NOTES.md must contain:

```
analogs:
  - slug: mozart-k550-iii
    score: 6
    take: 3/4 dance; melody in high strings; winds pad; bass light; thins after cadence
```

Then Maestro arranges from the **piano** using [`piano-solo-arrange.md`](piano-solo-arrange.md). Critic uses [`analog-critic.md`](analog-critic.md), not CYCLE gold numbers.
