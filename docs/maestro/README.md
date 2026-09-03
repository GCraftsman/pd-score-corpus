# Music Maestro instruction set

**Audience:** Music Maestro, a teammate coding/music agent. No human in the loop.
**Date:** 2 September 2026.
**Repo:** [pd-score-corpus](https://github.com/GCraftsman/pd-score-corpus) (public). Owner: GCraftsman / Michael Lacasse.

This directory is the playbook for turning **piano / keyboard symbolic music** into **multi-instrument and full orchestral SMF Type 1** files for Logic Pro / GarageBand.

Read this file, then follow [`SKILL.md`](SKILL.md) for every experiment. Run [`first-pass.md`](first-pass.md) on v1 before critic; critic emits JSON patches ([`critic-patches.md`](critic-patches.md)). Two jobs: (1) CYCLE same-work gold vs a recording of **that** piece; (2) **app path** — piano idea → invented orchestra using analog *texture* refs ([`analog-matching.md`](analog-matching.md)). Do not improvise a film-score style and do not train on copyrighted audio.

## Hard constraints (non-negotiable)

1. **Legal.** Read [`../../LEGAL.md`](../../LEGAL.md). Arrangements of public-domain *notes* can themselves be copyrighted. Product intent is to **CC0 the app’s stitched/arranged MIDI**. That is a product policy, not a film-clearance. **Do not claim any output is cleared for film.**
2. **No Williams / Zimmer / living-composer imitation.** Style target is the **source composer’s era** (Bach → baroque strings+continuo; Mozart/Beethoven → classical orchestra; Tchaikovsky → romantic orchestra). Era tables: [`orchestration-rules.md`](orchestration-rules.md).
3. **Do not train on, scrape, or transcribe** YouTube, commercial recordings, or copyrighted film scores.
4. **Sample-library EULAs.** Spitfire, BBCSO, Kontakt, etc. forbid training on their *renders*. Preview with **FluidSynth + a GM soundfont**, or open the MIDI in Logic and assign **Studio Strings / Studio Horns / Studio Woodwinds** *after* export. Never bake audio into the repo. Never commit `.logicx` or bounced stems.
5. **Do not fight the MIDI extract.** Files may already live under [`../../midi/`](../../midi/) matching the manifest `mid` path with `mid/` → `midi/`. Do **not** delete [`.cache/`](../../.cache/). Do **not** `git commit` (parent will push).
6. **Output is SMF Type 1**, named tracks, tempo map, markers. Not Type 0. Not a stereo bounce. Not `.logicx`.

## Who does what

| Role | Does |
| --- | --- |
| Music Maestro (you) | First-pass arrange ([`first-pass.md`](first-pass.md)); anything the patch schema cannot express; MIDI + NOTES.md |
| Critic | Emits JSON patches only ([`critic-patches.md`](critic-patches.md)). Does not edit MIDI bytes. |
| Applier | `scripts/apply_critic_patches.py` applies critic JSON to an SMF |
| Coordinator / parent | Job card (clip, gold recording, cycle id). Reviews, pushes git, opens files in Logic |
| App (future) | Stitches excerpts and exports user-facing SMF |

**Ownership:** Critic emits, applier code applies, Maestro owns first-pass arrange + anything the schema cannot express, coordinator owns the job card (clip / gold / id).

## How to pick a source row

File: [`../../data/manifest.csv`](../../data/manifest.csv) (3,730 works). Columns include `pdmx_id`, `composer`, `title`, `song_name`, `n_tracks`, `is_piano_only`, `mid`, `mxl`, `tags`, `license`.

**Default query (piano → orchestra pipeline):**

```text
is_piano_only == true
AND composer in data/composers.allowlist.json
```

v1 has **186** piano-only rows (lower bound: PDMX v9 `tracks` is numeric part IDs, so tagging is incomplete). Prefer these for orchestration experiments.

**Resolve bytes:**

- MIDI on disk: `midi/{shard}/{sub}/{pdmx_id}.mid`  
  Manifest `mid` looks like `./mid/1/30/{pdmx_id}.mid` — replace the `mid` directory name with `midi`.
- MusicXML is preferred when you need voices / barlines; it may not be extracted in this checkout. MIDI is the always-on fallback.
- If a file is missing, skip the row and log it. Do not scrape MuseScore.com.

**Skip a row if any of these hold:**

- Title/tags contain `busoni`, `arrangement of`, `transcription of` a *named living or graylisted arranger* (Busoni died 1924 — graylist-era editorial layer).
- Composer is graylisted or denylisted ([`data/composers.graylist.json`](../../data/composers.graylist.json), [`data/composers.denylist.json`](../../data/composers.denylist.json)).
- You would need YouTube / a copyrighted recording to “hear how it should go.”

**Untagged single-track rows** (`is_piano_only=false`, `n_tracks==1`, 1,714 of them) are *candidates* for keyboard encodings. Use them only after piano-only cards pass, and treat them as keyboard until proven otherwise.

## Output contract (short)

Full spec: [`midi-contract.md`](midi-contract.md).

- SMF **Type 1**, PPQ **480**.
- Track 0 = conductor (tempo, time signature, key signature, markers, metadata text).
- One instrument per subsequent track, GM program for *preview only*.
- Filename: `arrangements/{composer-slug}/{pdmx_id}.{ensemble}.mid`
- Metadata text event: source work + `arrangement: experimental, CC0`.

## File index

| File | Purpose |
| --- | --- |
| [SKILL.md](SKILL.md) | Reusable recipe. Follow every experiment. |
| [first-pass.md](first-pass.md) | v1 hygiene before critic (detach 8ths, GM map, no default +12) |
| [critic-patches.md](critic-patches.md) | Critic JSON ops; apply-then-verify |
| [orchestration-rules.md](orchestration-rules.md) | Ranges, role map, doubling, density, CC, era tables |
| [midi-contract.md](midi-contract.md) | Exact SMF Type 1 layout |
| [analog-matching.md](analog-matching.md) | Pick 1–3 PD/CC analog recordings (tempo/meter/texture, not same work) |
| [piano-solo-arrange.md](piano-solo-arrange.md) | App path: keep user’s tune, embellish, section layers |
| [analog-critic.md](analog-critic.md) | Critic: role/density/accompaniment ideas only; no pitch copying |
| [harmony-rules.md](harmony-rules.md) | One home key, allowed seams, cadence map, bar labels |
| [variation-techniques.md](variation-techniques.md) | Random first-pass recipes; SKIP if they break harmony |
| [experiments.md](experiments.md) | Numbered experiment cards, in order |
| [references.md](references.md) | Citations with URLs and license tags |
| [../../arrangements/NOTES.md](../../arrangements/NOTES.md) | Append-only run log |
| [../../LEGAL.md](../../LEGAL.md) | Composition vs edition vs recording vs EULA |

## Suggested stack (all commercial-OK as *libraries*)

| Library | License | Use |
| --- | --- | --- |
| [music21](https://github.com/cuthbertLab/music21) | BSD-3-Clause | parse, key, meter, voice, MusicXML |
| [pretty_midi](https://github.com/craffel/pretty-midi) | MIT | MIDI I/O, instruments, CC |
| [mido](https://github.com/mido/mido) | MIT | low-level SMF Type 1, meta events |
| FluidSynth + a GM soundfont | varies (soundfont-specific) | headphone preview, **not** the product sound |

Do **not** pull pretrained weights until you have read the license table in [`experiments.md`](experiments.md) and [`references.md`](references.md). Most public “piano-to-band” checkpoints were trained on Lakh MIDI / pop / cinematic corpora and are **SKIP** for this product.

## Success, in one sentence

A human can File→Open the MIDI in Logic Pro, rename tracks onto Studio Strings (or GarageBand orchestral patches), hear the **source melody on Violin I**, hear bass in celli/basses, and not hear notes outside the instrument ranges in [`orchestration-rules.md`](orchestration-rules.md).
