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

