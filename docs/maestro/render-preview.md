# Render preview (FluidSynth bounce)

**Job:** make a **fatter listen-now WAV** from an already-written SMF Type 1 arrangement. This is **production**, not composition. Do not change notes here to chase a commercial house sound.

**When:** after MIDI validates ([`midi-contract.md`](midi-contract.md)) and first-pass / critic cycle for this version is done — or when the coordinator asks for a preview bounce.

**Legal note (not advice):** Density craft + legal GM render improves clarity of *our* MIDI. Named-style imitation and copyrighted-cue transcription are refused ([`../../LEGAL.md`](../../LEGAL.md) §11, [`style-targets.md`](style-targets.md)). Preview audio is **not** a film-cleared stem, **not** training data, and **must not** be committed to the repo. Spitfire / BBCSO / Kontakt / other proprietary orchestral libraries stay **out** for repo artifacts and for any training set.

---

## Soundfonts (prefer in this order)

| Path | Notes |
| --- | --- |
| `/usr/share/sounds/sf3/MuseScore_General.sf3` | Prefer when present (MuseScore General) |
| `/usr/share/sounds/sf3/MuseScore_General_Full.sf3` | Heavier; OK if disk/time allow |
| `/usr/share/sounds/sf2/FluidR3_GM.sf2` | Fallback GM already referenced in SKILL.md |
| `/usr/share/sounds/sf2/default-GM.sf2` | Last resort |

Do **not** download random SFZ packs from the web for product previews without license review. Do **not** bounce through proprietary sample libraries for anything that lands in git or a training folder.

Pick the first path that exists; log `soundfont: <path>` in NOTES.

---

## Bounce recipe

```bash
# paths — set MIDI and OUT for this job
MIDI=arrangements/.../something.orchestra.vN.mid
OUT=/tmp/maestro-preview.wav
SF=/usr/share/sounds/sf3/MuseScore_General.sf3
# if MuseScore SF missing:
# SF=/usr/share/sounds/sf2/FluidR3_GM.sf2

fluidsynth -n -i -a file \
  -F "$OUT" \
  -r 48000 \
  -g 0.6 \
  "$SF" \
  "$MIDI"
```

| Flag | Intent |
| --- | --- |
| `-n -i` | no shell, no MIDI in |
| `-a file -F` | write WAV |
| `-r 48000` | consistent preview rate |
| `-g 0.6` | start gain; raise toward `0.8` only if peak is quiet (see gain pass) |

If `fluidsynth` or every SF is missing: log `preview: not run` and stop. Do not scrape a soundfont.

---

## MIDI balance before bounce (composition-adjacent, still legal)

Do these on the **MIDI** if the bounce is thin or uneven — still not a new style language:

1. **CC7** (volume) per desk: skyline ~100, pads ~70–85, bass ~90, brass hits ~95 only at climax bars.
2. **CC11** (expression): shape the phrase arc; return toward 80–100 after climaxes.
3. Velocities: follow [`first-pass.md`](first-pass.md) / orchestration dynamic map; avoid every note at 127.
4. Do not add hall CC “reverb depth” as a substitute for register contrast — that belongs in optional ffmpeg below.

---

## Optional mild reverb (ffmpeg)

Only if `ffmpeg` exists and the dry bounce is harsh. Keep it mild — this is headphone comfort, not a trailer mix.

```bash
DRY=/tmp/maestro-preview.wav
WET=/tmp/maestro-preview-wet.wav

ffmpeg -y -i "$DRY" -af "aecho=0.8:0.88:40:0.15,loudnorm=I=-16:TP=-1.5:LRA=11" "$WET"
```

| Control | Bound |
| --- | --- |
| Echo / reverb | short; do not wash the motor into the pad |
| True peak | ≤ −1.5 dBTP after loudnorm |
| Commit | **never** commit `DRY` or `WET` |

If loudnorm fails, fall back to a simple limiter:

```bash
ffmpeg -y -i "$DRY" -af "alimiter=limit=0.95" "$WET"
```

Log which chain ran (`render: dry` | `render: wet-loudnorm` | `render: wet-limiter`).

---

## Gain / clip check

```bash
ffmpeg -i /tmp/maestro-preview.wav -af "volumedetect" -f null - 2>&1 | grep -E 'max_volume|mean_volume'
```

| Result | Action |
| --- | --- |
| `max_volume` ≥ −0.5 dB | Re-bounce with lower `-g` (e.g. 0.45) or re-run limiter |
| `max_volume` < −12 dB | Re-bounce with higher `-g` (cap 0.85) or raise CC7 on skyline/bass only |
| Clipping / rectangular waveform | Fix MIDI velocities or gain; do not “fix” with more reverb |

---

## Deliverable

| Artifact | Commit? | Where |
| --- | --- | --- |
| SMF Type 1 | yes (when coordinator allows) | `arrangements/...` |
| Preview WAV | **no** | `/tmp/` or local scratch only |
| Proprietary library bounce | **no** | never for repo / training |

Hand the WAV path to the coordinator or human for listen-now. Product DAW path remains: open MIDI in Logic / GarageBand and assign Studio Strings / Horns / Woodwinds *after* export.

---

## Checklist

```
[ ] Legal SF chosen and logged
[ ] fluidsynth wrote WAV without error
[ ] Peak checked; not clipping
[ ] Optional reverb only if needed; mild
[ ] WAV not staged for git
[ ] NOTES has soundfont + render chain
[ ] No Spitfire/BBCSO/Kontakt path used
```
