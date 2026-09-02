# Arrangement experiment log

Music Maestro appends one block per run. Do not delete prior blocks.
Do not git commit from this log (parent agent pushes).

Template:

```
## YYYY-MM-DDTHH:MMZ  EXP-0N  {pdmx_id}  {ensemble}
- source: composer / title / manifest row
- method: rules-only | music21 | in-corpus-prior | SKIP-ML
- midi: arrangements/{composer-slug}/{pdmx_id}.{ensemble}.mid
- duration_src_beats / duration_arr_beats
- range_violations: none | list
- melody_preservation: skyline pitch-class match % in Violin I
- preview: fluidsynth OK | fluidsynth FAIL | not run
- logic_notes: (leave blank if no human DAW pass)
- legal: source is_piano_only=true, allowlisted, no film-score scrape
- issues:
```

## 2026-09-02T07:45Z  EXP-01  QmdHbV5ya1MwSJnJNdSXw4UmKNU4JjtrBpSiFKMRS4F3rc  strings
- source: Frederic Chopin / Prélude in C Minor Opus 28 No. 20 / pdmx_id=QmdHbV5ya1MwSJnJNdSXw4UmKNU4JjtrBpSiFKMRS4F3rc (manifest is_piano_only=True, license=cc-zero, mid=./mid/3/24/….mid)
- method: rules-only
- midi: arrangements/frederic-chopin/QmdHbV5ya1MwSJnJNdSXw4UmKNU4JjtrBpSiFKMRS4F3rc.strings.mid
- duration_src_beats / duration_arr_beats: 51.998 / 51.998
- range_violations: none
- range_drops: Violin I 0, Violin II 0, Viola 0, Cello 0, Contrabass 0 (octave-shifted, not dropped: Cello 22, Contrabass 8)
- melody_preservation: skyline pitch-class match 100.00% in Violin I (61/61 active 1/32 buckets)
- n_voices histogram (onset buckets): {1: 8, 2: 4, 4: 49} — 4-voice SATB 80.3% of buckets
- preview: fluidsynth OK (MuseScore_General_Full.sf3; peak 0.29 FS, RMS 0.043 FS at gain 2.5; not silent)
- logic_notes:
- legal: source is_piano_only=true, allowlisted, no film-score scrape
- issues: Preferred MIDI used (not fallback). Full prelude kept (13.00 bars ≤ 32). Texture windows classified ostinato/homophony (LH octave repeats) but OVERRIDE chorale applied. Sequence name uses ASCII `--` / `...` because SMF meta is Latin-1 (spec em dash/ellipsis not encodable). CC64 present only ticks 22562–23041 (last cadence); melody re-articulated, no CC64 copied onto strings. Source pitch 24–75; cello bass octave-shifted into 36–76. Cb doubles cello 8vb only where source bass ≤ 48 and result ≥ 28 (doubling-table / SKILL E1 floor); C-extension not required after cello clip. No harp, no brass. Source PPQ already 480. No git commit; wav/mp3 written outside repo under /workspace/pd-demo/.
