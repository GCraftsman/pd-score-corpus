# sketch-06 — lyrical-strings orchestra

Committed artifacts for SKETCH-06 (lyrical / long-breath). Style pack `lyrical-strings`. `theme: develop`. Critic stop after v2.

## Sketch (context)

- Meld: Chopin Op.9 No.2 cantabile skyline + Handel Sarabande HWV 432 processional bed (PCs retargeted to labeled chords).
- Home key **Eb major**, 3/4, 60 BPM, 20 bars = 60s. PPQ 480.
- `theme_candidate_bars: 5–12` (nocturne spine — not sarabande blocks).
- Harmony: I I vi vi | I×4 | IV IV ii ii | V7×5 | I×3 (see cycles NOTES for full table).

## Orchestra MIDI (this folder)

| File | Role |
| --- | --- |
| `sketch.orchestra.v1.mid` | First-pass orch + theme develop |
| `sketch.orchestra.v2.mid` | Post-critic; **stop** |

Preview audio lives under `/workspace/cycles/sketch-06/` only — **not** committed.

## Critic (stop)

# ARRANGE-SKETCH-06 critic log

style_pack: lyrical-strings. preview: era-match intimate (slight widen at close). Analogs: bach-bwv1068-air / mozart-k421-iii roles only. Theme iron / develop on Vln I.

## v1
Maestro: 60s @ 60 BPM 3/4 Eb, theme statements [[5,12],[18,20]] contrast [13–17], Vln I owner, soft Vc octave A′ only (claimed), mid under A ≤2 (Vln II+Vla), Hn contrast-only, WW cadence/close, first-pass hygiene OK (CC64=0, Cb rest 1–4, no +12, locked GM). n_arr Fl1=9 Ob1=5 Cl1=3 Bn1=6 Hn1=5 VlnI=42 VlnII=20 Vla=20 Vc=53 Cb=16.
Critic: A′ Fl+Ob unison theme (close 8 desks; mel/mid 1.09→0.61) → rest Fl1+Ob1 on A′ (Ob bar-17 cadence stay; Cl+Bn stay). Cello mid doubles under A bars 5/7/9/11 → prose drop (bass bed stay; soft Vc A′ stay). Leave Vln I theme. Leave soft Vc A′. No heroic thicken. No analog pitches/BPM/hall.
Patches: /workspace/cycles/sketch-06/critic-v1/patches.json (p1-fl-ob-Ap-rest) + prose ask in critic-pass-01.md. dry-run touched=0 removed=12 added=0.

## v2 / pass 2
v1_followup: p1-fl-ob-Ap-rest APPLIED (Fl A′ 9→0; Ob A′ 3→0; Ob bar-17 cadence 2 KEPT; Cl+Bn+strings+soft Vc A′ KEPT; Vln I theme KEPT). Cello mid-double prose APPLIED (weak-beat mid hits bars 5/7/9/11: 4→0; Vc under A 20→16 bass bed; mid pads ≤ Vln II+Vla; soft Vc A′ KEPT).
Verdict: theme A audible/clearer (mel/mid 1.15); A′ clearer (Fl+Ob unisons gone; Vln I sole owner; 7 desks; Cl soft+Bn bass = slight widen OK). Intimacy OK. leftovers-only / STOP — 0 NEW asks.
Patches: /workspace/cycles/sketch-06/critic-v2/patches.json (empty). Loudnorm: critic-v2/. Review: critic-pass-02.md. dry-run touched=0 removed=0 added=0.
