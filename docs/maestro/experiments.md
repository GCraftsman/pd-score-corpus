# Experiment cards (run in order)

Music Maestro: start at the first card whose id is **not** in
[`../../arrangements/NOTES.md`](../../arrangements/NOTES.md). One card
per run. Rules-only first. ML only if the weight license is
commercial-OK; otherwise log `SKIP-ML` and move on.

Shared success criteria (every card, unless a row overrides):

1. File is SMF Type 1, PPQ 480, path matches
   [`midi-contract.md`](midi-contract.md).
2. Listen-able in Logic Pro / GarageBand File→Open **or** FluidSynth
   (no crash, notes audible, no hanging notes).
3. No note outside the **practical** range table.
4. Source skyline pitch-class preserved in **Violin I** ≥ 85% of active
   1/32 buckets.
5. Duration = source ± 1 bar (or ± 1 bar of the 32-bar clip).
6. Track 0 metadata contains `arrangement: experimental, CC0`.
7. A NOTES.md block is appended.

Shared **forbidden**: Williams/Zimmer pastiche; YouTube; sample-lib
renders as training data; keyswitches; GM Orchestra Hit; Type 0;
`.logicx`; git commit.

---

## License blockers (read before any ML card)

| System | Code license | Weights / data | Maestro action |
| --- | --- | --- | --- |
| music21 | BSD-3 | n/a | **USE** |
| pretty_midi, mido | MIT | n/a | **USE** |
| Magenta / note-seq | Apache-2.0 | Magenta models: Apache, but **not** an orchestrator | tools OK; no Magenta checkpoint required |
| FIGARO (von Rütte et al.) | MIT code | trained on **Lakh MIDI** (pop, mixed ©) | **SKIP** pretrained |
| GETMusic (Microsoft Muzic) | MIT code | pop GM tracks (piano/gtr/bass/lead/strings/drums), not orchestra | **SKIP** (wrong task + likely Lakh-like data) |
| MuseCoco (Muzic) | MIT code | training data **not fully public**; text-to-MIDI, not piano→orchestra | **SKIP** |
| Anticipatory Music Transformer (Stanford CRFM) | Apache-2.0 code+weights | trained on Lakh; authors flag © of underlying MIDI | **SKIP** pretrained |
| MIDI-GPT (Metacreation Lab) | MIT code (2026 repo) | paper originally **Open RAIL-M / NC practice**; GigaMIDI/Lakh © | **SKIP** pretrained |
| NotaGen | MIT code+HF weights | pretrain 1.6M mixed pieces, then ~9k classical (mixed ©) | **SKIP** pretrained for product; optional research note only |
| SymphonyNet (Liu et al. ISMIR 2022) | MIT code | 46k symphony MIDI, mixed ©; **is** an orchestrator-ish model | **SKIP** pretrained; architecture is the interesting part |
| SymphonyGen (ISMIR 2026) | check repo if cloned | trained on SymphonyNet set + **cinematic** GRPO reference | **SKIP** (style + data). Do not use to “sound cinematic.” |
| METEOR (Le & Yang, IJCAI 2025) | confirm `dinhviettoanle/meteor` LICENSE before any clone | closest paper to re-orchestration | **SKIP** until license file is MIT/Apache **and** you accept mixed-© training data — default **SKIP** |
| Zhao et al. NeurIPS 2024 Structured Arrangement | research code | LMD + Slakh2100 | **SKIP** pretrained |
| Band-in-a-Box / PG Music | proprietary | n/a | **SKIP** |
| In-corpus prior (this repo’s 1,830 multi-track rows) | CC0/PDM encodings + our CC0 scripts | allowlisted composers only | **OK** (EXP-08) |

**Vaporware / do-not-wait:** anything without a tagged release, a LICENSE
file, and a reachable checkpoint. If a demo page exists but weights do
not, log `vaporware` and skip.

---

## EXP-01 — Chopin chorale → SATB strings (rules-only)

| Field | Value |
| --- | --- |
| **id** | `EXP-01` |
| **source query** | `is_piano_only=true` AND composer matches Chopin AND (`prelude` in title/tags) AND (`c minor` OR `op.28` / `Op.28` / `Op 28`) |
| **preferred row** | `QmdHbV5ya1MwSJnJNdSXw4UmKNU4JjtrBpSiFKMRS4F3rc` — Prélude in C Minor Op. 28 No. 20 (block-chord chorale) |
| **fallback** | `QmRdaucqDLh7YrGuyTqA43gnsXeKWpN6dhT177BweZo2qV` (Op. 28 No. 4) |
| **era** | early romantic, but **strings-only** (Chopin piano ≠ Tchaikovsky orchestra) |
| **ensemble token** | `strings` |
| **method** | rules-only (SKILL.md steps 3–11). No ML. |
| **expected tracks** | Conductor, Violin I, Violin II, Viola, Cello, Contrabass |
| **texture override** | force `chorale` |
| **clip** | full prelude if ≤ 32 bars; else first 32 |
| **success (extra)** | 4-voice SATB most of the time; Cb only where bass ≤ 48; no harp, no brass |
| **NOTES.md** | skyline-match %, n_voices histogram, range_drops, fluidsynth |

If the preferred MIDI is missing, take the next Chopin piano chorale-like
row (`n_sim` high, `rhythm_cv` low) and log the substitution.

---

## EXP-02 — Bach WTC prelude → baroque strings + continuo (rules-only)

| Field | Value |
| --- | --- |
| **id** | `EXP-02` |
| **source query** | `is_piano_only=true` AND composer Bach AND (`BWV 846` OR `Wohltemper` OR `Praeludium in C`) |
| **preferred row** | `QmbFt6yc1EUxZvqTVUg7xQY531BbkUcxn8uL3VYrB2uwjB` — WTC I Prelude in C BWV 846 |
| **do not use** | any row with `busoni` in title/tags |
| **era** | baroque |
| **ensemble token** | `baroque` |
| **method** | rules-only. Texture = `arpeggio`. **Do not** give every 16th to five string desks. |
| **expected tracks** | Conductor, Violin I, Violin II, Viola, Cello, Continuo (GM 6), Oboe 1 (outline), Bassoon 1 (with bass) |
| **algorithm extra** | per beat, strings play local min/max of the broken figure; continuo/harpsichord may take a reduction (one attack per beat); melody outline = implied top of each bar’s arpeggio → Vln I |
| **success (extra)** | you can still *hear* the prelude’s harmonic rhythm; no romantic pad; no harp; no horns |
| **NOTES.md** | note-density ratio `arr_notes / src_notes` (expect < 2.5, not 5×) |

---

## EXP-03 — Bach invention → polyphonic desks (rules-only)

| Field | Value |
| --- | --- |
| **id** | `EXP-03` |
| **source query** | `is_piano_only=true` AND composer Bach AND `invention` |
| **preferred row** | `QmcgPrR41ikm5Ci6ABVf4r58KCVov3VKepGZTgAnGRCoPD` — Invention No. 5 BWV 776 |
| **fallback** | `QmSkpv88AXBwfQVSki4Lja1uAi1SiabTExoBT7fJmkVgyd` (No. 15) |
| **era** | baroque |
| **ensemble token** | `baroque` |
| **method** | rules-only, texture = `polyphony`. Two streams: skyline vs remainder-with-independent-onsets. Vln I = stream A, Vln II or Vc = stream B (bass stream → Vc). Continuo doubles bass. **No chord filling.** |
| **expected tracks** | Conductor, Violin I, Violin II *or* Cello, Continuo, optional Bassoon with bass |
| **success (extra)** | both voices audible; no SATB homogenization; parallel-5ths *not* “fixed” |
| **NOTES.md** | n_streams, % buckets with >2 simultaneous assigned desks (should be low) |

---

## EXP-04 — Mozart London Sketchbook minuet → classical orchestra (rules-only)

| Field | Value |
| --- | --- |
| **id** | `EXP-04` |
| **source query** | `is_piano_only=true` AND composer Mozart AND (`minuet` OR `contredanse`) |
| **preferred row** | `QmbjiXNoTmLNHq6Xw8f6kWh2TBGGGcputXwLvsDE8oc8Fa` — Minuet in G K. 15c |
| **fallback** | `QmbL2idE5ykZoHvUMVzTdEWQvmyPqgHA5C4UWET1tkjqUk` (Contredanse in F K. 15h) |
| **era** | classical |
| **ensemble token** | `classical` |
| **method** | rules-only. Melody Vln I; bass Vc+Cb; offbeat inners → Vla + Horn 1–2 (held); winds double melody at cadences only. Trumpets/timp **off** unless mean velocity ≥ 100. |
| **expected tracks** | Conductor, Flute 1, Oboe 1, Clarinet 1, Bassoon 1, Horn 1, Horn 2, Violin I, Violin II, Viola, Cello, Contrabass |
| **success (extra)** | horns do not play 8th-note Alberti; winds have rest; melody on Vln I |
| **NOTES.md** | % beats horns are active (target 30–70% in a minuet, not 100%) |

---

## EXP-05 — Chopin waltz → strings + harp + horns (rules-only)

| Field | Value |
| --- | --- |
| **id** | `EXP-05` |
| **source query** | `is_piano_only=true` AND composer Chopin AND `waltz` |
| **preferred row** | `QmWqwAqr8yGcvHzHU6tyLhF2YL6551xx84brEx7uYoK4Z7` — Waltz in B minor (Op. 69) |
| **fallback** | `QmZpiR4dVBt5Wo6p6r3XWL8pSmzZ6bAUF9xfwDJfNHqBur` (Waltz in A minor B.150, simpler) |
| **era** | early romantic, **small** orchestra |
| **ensemble token** | `romantic` |
| **method** | rules-only, texture = `waltz`. Beat 1 → Cb+Vc; beats 2–3 → Vla + Horn chord tones; skyline → Vln I; LH figure may also go to Harp (rolled, not machine 8ths). No trombones, no tuba, no cymbal. |
| **expected tracks** | Conductor, Flute 1, Clarinet 1, Horn 1, Horn 2, Harp, Violin I, Violin II, Viola, Cello, Contrabass |
| **success (extra)** | audible 3/4 oom-pah-pah; melody not on harp; bass not on viola |
| **NOTES.md** | fraction of bars whose lowest-note onset is on beat 1 |

---

## EXP-06 — Beethoven slow movement → classical orchestra (rules-only)

| Field | Value |
| --- | --- |
| **id** | `EXP-06` |
| **source query** | `is_piano_only=true` AND composer Beethoven AND (`moonlight` OR `adagio` OR `sonata`) |
| **preferred row** | `QmeuK3Unr7ybzDCvVVbU4Eu878nUjDhRJpZMyzzMY5EQyr` — Moonlight Sonata 1st mvt (slow triplet texture) |
| **fallback** | `QmetPJWpxk5JX5tHPziMZZf4y1FzkEDYW3PDtnfv2BSN1z` (Sonatina in G Anh. 5 — if Moonlight is too long, clip Moonlight to 32 bars **first**) |
| **do not use** | rows titled as symphony piano *arrangements* (Symphony 7 / Symphony 9 piano reductions) — already orchestral music flattened; different task |
| **era** | classical / early romantic |
| **ensemble token** | `classical` |
| **method** | rules-only. Texture likely `arpeggio` + `homophony`. Triplets: **do not** assign every triplet to the whole orchestra. Outline → strings; broken figure → Vla or harp-off (no harp in classical token); melody (skyline, often middle-right hand) → Vln I *even if it is not always the global highest* — **override skyline** if a repeated-note bass is higher than the tune for a bucket (Moonlight: the G# octaves vs the tune). Implement: if a pitch is repeated ≥ 6 times in 2 bars and is not the local step-wise line, it is **not** melody. |
| **expected tracks** | Conductor, Flute 1, Oboe 1, Clarinet 1, Bassoon 1, Horn 1, Horn 2, Violin I, Violin II, Viola, Cello, Contrabass |
| **success (extra)** | the famous tune is on Vln I, not the ostinato; ostinato on Vla/Vc; duration of the clip ± 1 bar |
| **NOTES.md** | document the skyline override rule and % buckets overridden |

---

## EXP-07 — Cue sketch: melody + ostinato + pedal + hits (rules-only)

This is the film-app *function* test. Style is still 18th/19th-c.
**Hit-points are markers + timp/cymbal, not a new harmony.**

| Field | Value |
| --- | --- |
| **id** | `EXP-07` |
| **source query** | reuse EXP-04’s Mozart minuet if that MIDI parsed; else `QmbjiXNoTmLNHq6Xw8f6kWh2TBGGGcputXwLvsDE8oc8Fa` |
| **era** | classical |
| **ensemble token** | `cue-sketch` |
| **method** | rules-only on the same voice split as EXP-04, then: (1) **melody** track = Vln I; (2) **ostinato** = extract the most common 1-bar inner rhythm, loop it on Viola only; (3) **pedal** = local tonic as a whole-note on Contrabass+Bassoon, one change per 4 bars; (4) **hits** = markers `HIT 1` `HIT 2` `HIT 3` on the downbeats of bars 5, 9, and 13 (or last bar if shorter) + Timpani on the bass pitch class (clipped to 38–57) + Cymbal GM ch.10 note 49, velocity 100, duration 1 beat. **Do not** time-stretch to a video. Tempo map copied from source. |
| **expected tracks** | Conductor (with HIT markers), Violin I, Viola (ostinato), Cello, Contrabass, Bassoon 1, Horn 1, Timpani, Cymbal |
| **success (extra)** | markers exist at those bars; hits align to barlines within 1 tick; melody still ≥ 85% on Vln I; no trailer brass |
| **NOTES.md** | marker tick list, timp pitches used, statement “hit-points = tempo map, not orchestration” |

---

## EXP-08 — In-corpus instrument prior (no external weights)

| Field | Value |
| --- | --- |
| **id** | `EXP-08` |
| **source query** | same Chopin prelude as EXP-01 (compare against EXP-01) |
| **method** | **not** a public checkpoint. Build a tiny histogram from **this corpus**: take up to 40 multi-track (`is_piano_only=false`, `n_tracks>=4`) rows whose composer is Mozart or Beethoven or Haydn, load `midi/…`, map GM programs to our desk names, and for each sounding note record `(pitch_class, octave_bucket, gm_family)`. At inference, assign inner voices to the desk with the highest count for that `(pc, octave)` instead of the static SATB map. Melody and bass still from rules (skyline / lowest). |
| **license** | OK: allowlisted encodings only. No Lakh, no SymphonyNet dataset, no BBCSO audio. |
| **ensemble token** | `classical` |
| **expected tracks** | same as EXP-04 roster |
| **success (extra)** | MIDI validates; write a table `prior vs EXP-01 assignment disagreement %`; if prior is empty (no multi-track MIDI on disk), log `SKIP-no-multitrack-bytes` and stop — do **not** download random orchestral MIDI from the web |
| **NOTES.md** | n_prior_files, n_prior_notes, disagreement %, whether it sounded less/more idiomatic than EXP-01 (one sentence) |

If EXP-08’s prior is too thin (< 5 files), that is a result. Do not
“fix” it by pulling FIGARO/SymphonyNet weights.

---

## After the eight cards

Stop. Optionally propose (do not silently run) a follow-up:

- music21 `chordify()` vs greedy SATB on EXP-01
- clip-length ablation (8 vs 32 bars)
- **still SKIP** external NC/Lakh checkpoints

Never promote an ML experiment to “the app’s orchestrator” without a
license sentence in NOTES.md that a lawyer could read.
