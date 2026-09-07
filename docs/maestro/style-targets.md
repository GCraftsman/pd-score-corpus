# Style targets (PD-legal technique packs)

**Job:** when a human asks for “big Hollywood,” “heroic brass,” “dark tense underscore,” translate that into **craft instructions** Maestro can execute — **without** naming living film composers, without loading their recordings, and without optimizing toward a copyrighted cue.

This is the safe substitute for “make it sound like [living composer / modern soundtrack].”

**Not legal advice.** Bound by [`../../LEGAL.md`](../../LEGAL.md) §11 (safe lane) and by [`analog-matching.md`](analog-matching.md) / [`analog-critic.md`](analog-critic.md). Rimsky-Korsakov *Principles of Orchestration* (PD) is OK as craft. Do not paste Adler/Piston/Kennan.

---

## Hard bans (fail closed)

If a job card, prompt, or NOTES.md contains any of the following, **refuse the style ask** and rewrite it into a pack below (or ask the coordinator for a PD pack name):

| Banned | Why |
| --- | --- |
| Named living film/TV/game composers (Williams, Zimmer, Giacchino, Horner, Elfman, Hisaishi, Newman, Desplat, …) | Access + similarity evidence; publicity risk |
| Named copyrighted film/TV/game cues or franchises as **audio/MIDI targets** | Composition + recording copyright |
| YouTube / Spotify / Apple Music / label rips as critic gold | Unauthorized reproduction of the master |
| Critic loops whose success metric is “closer to [copyrighted recording]” | Manufactures substantial-similarity + intent record |
| Quoting a third work’s **progression or motive** as gold | harmony-rules.md §4 |

**Allowed instead:**

- Pack names from this file (`heroic-brass`, `dark-pad`, …).
- PD composers on the allowlist (Wagner, Tchaikovsky, Dvořák, Bruckner, …) as **era language**, not as “copy that symphony movement.”
- CC/PD recordings in [`../../targets/`](../../targets/) as **texture analogs** only (tempo/meter/mood) — never same-work CYCLE gold for a copyrighted piece, never pitch copying.

If the user said a banned name, log:

```
style_request_rewritten: "Williams-like" → pack:heroic-brass
banned_name_dropped: true
```

Then proceed with the pack. Do **not** keep the banned name in track metadata, patch comments, or critic prose.

---

## How to apply a pack

1. Pick **one primary pack** (+ optional secondary accent).
2. Obey [`harmony-rules.md`](harmony-rules.md) (one home key, labeled chords). Packs change **texture/orchestration**, not the labeled progression.
3. Keep the user’s/sketch **skyline** ([`piano-solo-arrange.md`](piano-solo-arrange.md)).
4. Run [`first-pass.md`](first-pass.md).
5. Critic uses [`analog-critic.md`](analog-critic.md) if PD analogs were chosen — **role/density only**. Critic must **not** score against a banned recording.
6. NOTES.md: `style_pack: heroic-brass` (never `style_target: john_williams`).

---

## Pack: `heroic-brass`

**Feel:** open, affirmative, march-adjacent. Late-romantic PD language (Wagner / early Bruckner / ceremonial Tchaikovsky), not a trailer hybrid.

| Lever | Instruction |
| --- | --- |
| Melody | Vln I or trumpet on skyline; optional horn octave below at climax only |
| Harmony | Prefer I/i and V; secondary V once per 8 bars max; no random smash |
| Bass | Root + fifth; timp doubles downbeats at climax (era-allowed) |
| Mid | Horns pad triad; do not tutti every 8th |
| Rhythm | Clear downbeats; short fanfare answers **after** a phrase (not on top of the tune) |
| Density | Intro thin → climax winds/brass → thin again |
| Forbidden | Default +12 on everything; GM orchestra hit; quoting a famous fanfare motive |

**PD analog drawer (texture only):** `beethoven-op67-i` / `beethoven-op55-i` only if **not** the same work as the piano source; else proceed with zero analogs.

---

## Pack: `dark-pad`

**Feel:** low, sustained, little motion. Open-dark region of harmony-rules cadence map.

| Lever | Instruction |
| --- | --- |
| Melody | Sparse; skyline may be mid register (viola/clarinet), not always Vln I high |
| Harmony | i / i–VI; half cadence OK; no early authentic close |
| Bass | Pedal tonic or fifth; contrabass + bassoon |
| Mid | Slow horn or viola pads; tremolo strings optional (short spans) |
| Rhythm | Few onsets; no motor ostinato unless sketch labels it |
| Density | Stay ≤3 desks until lift region |
| Forbidden | Trailer brass hits; rising-string whoosh as a quoted gesture from a known cue |

**PD analog drawer:** `bach-bwv1068-air` (cantabile strings) as texture cousin only.

---

## Pack: `chase-ostinato`

**Feel:** forward motion, one repeating cell. Craft ostinato — not a transcription of a famous chase cue.

| Lever | Instruction |
| --- | --- |
| Melody | Skyline above; do not put the ostinato on Vln I |
| Harmony | Chord tones only in the ostinato; snap to labeled chords |
| Bass | Ostinato may be bass **or** mid — only **one** choir (SKILL ostinato rule) |
| Mid | Offbeats or 16ths on viola/violins II; leave holes |
| Rhythm | 1- or 2-bar loop; IOIs stable; no random fill every bar |
| Density | Ostinato + tune + bass; winds at climax only |
| Forbidden | Copying a known ostinato pitch sequence; stacking ostinato on every desk |

---

## Pack: `lyrical-strings`

**Feel:** cantabile, legato, intimate → wider. Dvořák / Tchaikovsky slow-movement language.

| Lever | Instruction |
| --- | --- |
| Melody | Vln I cantabile; optional cello countermelody in verse (chord tones) |
| Harmony | Smooth voice-leading; common-tone seams preferred |
| Bass | Soft; root on downbeats |
| Mid | Divisi-like: Vln II / Vla fill 3rd/5th |
| Rhythm | Long values; fewer 16ths |
| Density | Strings-first; winds double at cadences |
| Forbidden | Harp gliss as default “emotion”; brass chorale smashing the tune |

**PD analog drawer:** `bach-bwv1068-air`, `mozart-k421-iii` (chamber intimacy).

---

## Pack: `ceremonial-processional`

**Feel:** slow 4/4 or 2/2, dotted rhythms, public space. Handel / Elgar-adjacent is **gray** — use **allowlisted** ceremonial PD (Handel, Wagner marches language) only.

| Lever | Instruction |
| --- | --- |
| Melody | Mid-high; horns or trumpets may take skyline for 4–8 bars then return to strings |
| Harmony | Strong I–V–I; authentic close at punch |
| Bass | Heavy downbeats; timp with bass at cadences |
| Mid | Wind choir block chords on offbeats or sustained |
| Rhythm | Dotted / double-dotted optional in brass answers |
| Density | Build by adding choirs every 8 bars, not all at once |
| Forbidden | Quoting a national anthem or famous march theme |

---

## Pack: `scherzo-spark`

**Feel:** light, quick, playful. Mendelssohn / early Beethoven scherzo language.

| Lever | Instruction |
| --- | --- |
| Melody | High winds or Vln I staccato |
| Harmony | Clear cadences; avoid dense pads |
| Bass | Light; pizz-style short notes (short durations, not a string-library keyswitch) |
| Mid | Sparse; rests are part of the texture |
| Rhythm | Detached 8ths; first-pass.md duty cycle |
| Density | Low; climax is still not full tutti |
| Forbidden | Cartoon hits; mickey-mousing a copyrighted theme |

---

## Pack: `tragic-chorale`

**Feel:** block chords, slow, funeral-adjacent (Chopin prelude language, Bach chorale).

| Lever | Instruction |
| --- | --- |
| Melody | Top of SATB = skyline |
| Harmony | Chorale voicing; i and V; deceptive OK at end |
| Bass | Low, independent |
| Mid | Full SATB strings; no arpeggio spray |
| Rhythm | Near-simultaneous attacks |
| Density | 4 voices most of the time |
| Forbidden | Turning chorale into trailer percussion bed |

---

## Mapping fuzzy human phrases → packs

| Human said | Pack | Log |
| --- | --- | --- |
| “Williams / Star Wars / Superman fanfare” | `heroic-brass` | rewrite |
| “Zimmer / Inception / trailer BRAAAM” | `dark-pad` + optional `chase-ostinato` accent | rewrite; **no** brass-hit sample |
| “Hisashi / Ghibli / whimsical” | `lyrical-strings` or `scherzo-spark` | rewrite |
| “horror drone” | `dark-pad` | ok if no film title |
| “romance / love theme” | `lyrical-strings` | ok |
| “battle / epic fight” | `heroic-brass` + `chase-ostinato` | rewrite if named cue |
| “funeral / death” | `tragic-chorale` | ok |
| “royal / coronation” | `ceremonial-processional` | ok |

If two packs conflict (e.g. dark-pad + scherzo-spark), pick **one** primary; use the second only in the climax bucket.

---

## Critic / Maestro checklist (style jobs)

```
[ ] No banned composer/franchise/recording named in NOTES or patches
[ ] style_pack set to a pack id from this file
[ ] Harmony labels intact; pack did not invent a new progression
[ ] Skyline preserved (≥85% unless technique IS inversion)
[ ] Analogs (if any) are CC/PD from targets/ and not same-work
[ ] Critic asks are role/density only — not "match the Williams trumpet lick"
[ ] first-pass.md completed
```

Fail any box → fix before the next critic cycle.
