# References (Music Maestro)

Fetched 2 September 2026. Each entry has a **status tag**:
`PD` public domain, `CC` Creative Commons, `MIT`/`BSD`/`Apache` permissive
code, `NC` non-commercial or RAIL restriction, `©-data` code may be
permissive but **training data is mixed-copyright**, `proprietary`,
`vaporware`.

Do not paste proprietary textbook examples into the repo.

---

## 1. Classical orchestration (craft)

| Work | URL | Tag | Notes |
| --- | --- | --- | --- |
| Rimsky-Korsakov, *Principles of Orchestration* (Steinberg ed.; Agate tr. 1922) | https://imslp.org/wiki/Principles_of_Orchestration_(Rimsky-Korsakov,_Nikolay) | **PD** | Primary craft source. IMSLP tags the 1913 RU and 1922 EN prints PD. |
| Same, Project Gutenberg #33900 (HTML text + examples) | https://gutenberg.org/files/33900/33900-h/33900-h.htm | **PD** (Gutenberg terms) | Convenient text search. US PD as 1922 publication. |
| Gutenberg EPUB/images | https://www.gutenberg.org/cache/epub/33900/pg33900-images.html | **PD** | |
| Wikimedia scan of 1913 Russian edition | https://commons.wikimedia.org/wiki/File:Rimsky_Korsakov_Fundamentals_of_orchestration_1913.djvu | **PD** | US PD: published before 1931. |
| Samuel Adler, *The Study of Orchestration*, 4th ed., Norton 2016 | publisher listing https://books.google.com/books/about/The_Study_of_Orchestration.html?id=kEgNjwEACAAJ | **proprietary** | Cite *concepts* (ranges, doubling) only. Do not copy prose or examples. |
| Walter Piston, *Orchestration*, Norton 1955 | catalog / ISBN 0393097404 | **proprietary** | Same rule. |
| Alfred Blatter, *Instrumentation and Orchestration* | Schirmer / Cengage | **proprietary** | Same rule. |
| Kent Kennan & Donald Grantham, *The Technique of Orchestration*, 7th ed., Routledge 2024 | https://www.amazon.com/Technique-Orchestration-Kent-Kennan-ebook/dp/B0CWFH5PPR | **proprietary** | Same rule. |
| Compact range + transposition sheet (Brooks / octatone) | https://octatone.com/wp-content/uploads/2015/01/Instrument-Ranges-2014.pdf | treat as **©** convenience chart | Cross-check only; our MIDI numbers are in orchestration-rules.md. |
| MIDI note range table | https://soundprogramming.net/file-formats/midi-note-ranges-of-orchestral-instruments/ | convenience table | Slightly optimistic; we use stricter *practical* bounds. |
| Clefs / transposing instruments (Clements) | https://www.clementstheory.com/study/range-transposition-and-clefs/ | educational © | Horn in F = P5; clarinet Bb = M2; bass/piccolo 8ve. |
| US Copyright Office: instrumentation as derivative authorship | https://www.copyright.gov/comp3/chap800/ch800-performing-arts.pdf | US gov | “Simply assigning entire lines to new instruments” may *not* be enough original authorship — relevant to LEGAL.md arrangements. |

---

## 2. Practical MIDI / DAW

| Work | URL | Tag |
| --- | --- | --- |
| Apple, Standard MIDI files in Logic Pro | https://support.apple.com/guide/logicpro/standard-midi-files-lgcpdf6a3851/mac | Apple docs |
| GM Level 1 spec (program map, CC 1/7/10/11/64) | https://ccrma.stanford.edu/~esteban/teaching/McGill_MUMT306/RP-003_General_MIDI_System_Level_1_Specification_96-1-4_0.1.pdf | MMA spec |
| CMU mirror of GM patch names (may 404; use MMA/GM1) | https://www.cs.cmu.edu/~music/cmsip/readings/GMSpecs_Patches.htm | spec republication |
| CC1 vs CC11 vs velocity (orchestral libraries) | https://modwheel.net/guides/understanding-midi-ccs | commercial blog, **not** a sample-lib EULA |
| Hao Ling Sheng, MIDI orchestration humanizing | https://www.haolingsheng.com/music-production/midi-orchestration-realism.html | blog |
| Sean Kim, mockup template (CC1/CC11/CC64) | https://blog.imseankim.com/realistic-orchestral-mockups-template-building-tutorial/ | blog |
| VI-Control thread: Logic names tracks from GM program | https://vi-control.net/community/threads/logic-x-midi-import-without-instruments-audio-plugins.159538/ | community |

Implication we encoded: write **both** a human `track_name` and a GM
`program_change`; no Spitfire keyswitches; CC64 off on orchestral
channels; GM is preview; Logic Studio Strings is the intended later
sound.

---

## 3. Rule-based / DSP-ish symbolic methods

| Work | URL | Tag | Use |
| --- | --- | --- | --- |
| Uitdenbogerd & Zobel, “Melodic matching techniques for large music databases,” ACM MM 1999 (*all-mono* skyline) | https://people.eng.unimelb.edu.au/jzobel/fulltext/acm-mm99.pdf · https://doi.org/10.1145/319463.319470 | ACM © paper, **algorithm is simple and reimplementable** | SKILL.md step 5A |
| Skyline demo (MiDiLiB) | https://purl.pt/282/1/v3d2/projects/midilib/midilib/english/skydemo.html | educational | |
| music21 LH/RH `PartStaff` | https://stackoverflow.com/questions/56572720/how-to-retrieve-the-left-and-right-hand-of-a-piano-piece-using-music21 | CC BY-SA 4.0 Q&A; music21 itself **BSD-3** | prefer MusicXML staves when present |
| musicpy split_melody (highest-pitch heuristic family) | https://musicpy.readthedocs.io/en/latest/The%20algorithm%20to%20split%20the%20main%20melody%20and%20chords%20from%20a%20piece%20of%20music/ | check package license before importing the lib; **reimplement**, don’t vendor if unclear | |
| PM2S / neural hand split | mentioned in various transcription stacks | **©-data** / research | v1 uses heuristics, not PM2S weights |

---

## 4. Libraries (commercial-OK as code)

| Library | URL | Tag |
| --- | --- | --- |
| music21 v2+ | https://github.com/cuthbertLab/music21 · https://pypi.org/project/music21/ | **BSD-3-Clause** |
| pretty_midi | https://github.com/craffel/pretty-midi · LICENSE MIT | **MIT** |
| Magenta | https://github.com/magenta/magenta/blob/main/LICENSE | **Apache-2.0** |
| Magenta note-seq | https://github.com/magenta/note-seq | **Apache-2.0** (repo archived) |
| mido | https://github.com/mido/mido | **MIT** (standard) |
| FluidSynth | https://www.fluidsynth.org/ | **LGPL** — preview binary, not shipped inside a proprietary static link without legal review |

---

## 5. ML / symbolic papers and tools (2020–2026)

| System | Paper / code | Tag | Maestro |
| --- | --- | --- | --- |
| **FIGARO** (von Rütte et al., fine-grained control) | https://github.com/dvruette/figaro (MIT) · paper via OpenReview | MIT code, **©-data** (Lakh) | SKIP pretrained |
| **GETMusic** (Lv et al., any-track diffusion) | https://arxiv.org/abs/2305.10841 · https://github.com/microsoft/muzic (MIT) · https://github.com/microsoft/muzic/tree/main/getmusic | MIT code; pop GM track set, not orchestra | SKIP (task + data) |
| **MuseCoco** (Lu et al., text→symbolic) | https://arxiv.org/abs/2306.00110 · https://microsoft.github.io/muzic/musecoco/ · muzic MIT | MIT code; training data not fully public; wrong task | SKIP |
| **Anticipatory Music Transformer** (Thickstun et al., Stanford CRFM 2023) | https://crfm.stanford.edu/2023/06/16/anticipatory-music-transformer.html | Apache-2.0 code+weights; Lakh **©-data**; authors say Apache may not reflect legal status of the model | SKIP pretrained |
| **MIDI-GPT** (Pasquier et al., AAAI 2025) | https://arxiv.org/abs/2501.17011 · https://github.com/Metacreation-Lab/MIDI-GPT (MIT 2026) · https://doi.org/10.1609/aaai.v39i2.32138 | Code MIT; paper describes **Open RAIL-M / NC practice** and GigaMIDI/Lakh | SKIP pretrained |
| **NotaGen** (Wang et al., 2025) | https://arxiv.org/abs/2502.18008 · https://github.com/ElectricAlexis/NotaGen (MIT) · https://huggingface.co/ElectricAlexis/NotaGen (license: mit) | MIT code+weights; 1.6M mixed pretrain | SKIP pretrained for product |
| **SymphonyNet** (Liu et al., ISMIR 2022) | https://arxiv.org/abs/2205.05448 · https://archives.ismir.net/ismir2022/paper/000066.pdf · https://github.com/symphonynet/SymphonyNet (MIT) · https://symphonynet.github.io | MIT code; 46k symphony MIDI **©-data**; joint orchestration-by-masking is relevant *as an idea* | SKIP pretrained |
| **SymphonyGen** (ISMIR 2026, hierarchical cinematic orchestration) | https://huggingface.co/SymphonyGen/SymphonyGen · claimed code github.com/symphonygen/symphonygen | cinematic GRPO reward; SymphonyNet dataset | **SKIP** style + data. If the demo 404s, treat as **vaporware** until cloned with LICENSE |
| **METEOR** (Le & Yang, IJCAI 2025) — melody-aware re-orchestration | https://arxiv.org/abs/2409.11753 · https://github.com/dinhviettoanle/meteor · https://huggingface.co/dinhviettoanle/meteor | **closest scientific task**; confirm LICENSE before clone; default SKIP | SKIP until permissive + counsel |
| **Structured Multi-Track Accompaniment Arrangement** (Zhao et al., NeurIPS 2024) piano→multi-track | https://proceedings.neurips.cc/paper_files/paper/2024/file/b95cb2d3f647dae571203bab285077e7-Paper-Conference.pdf · https://github.com/zhaojw1998/Structured-Arrangement-Code | LMD + Slakh **©-data** | SKIP pretrained |
| Unifying Symbolic Music Arrangement (NeurIPS 2025) | https://proceedings.neurips.cc/paper_files/paper/2025/file/15a5d4408b2bb41b9f923d724bb943f3-Paper-Conference.pdf | research | read, don’t ingest weights blindly |
| Magenta RealTime (audio, not symbolic orchestra) | https://magenta.withgoogle.com/magenta-realtime | Apache-ish + extra terms; **audio**, wrong modality | SKIP |
| Band-in-a-Box class systems | PG Music commercial | **proprietary** | SKIP |
| PDMX (this corpus’s parent) | https://arxiv.org/abs/2409.10831 · Zenodo https://zenodo.org/records/15571083 | compilation **CC-BY**; per-file CC0/PDM | source of bytes, not an orchestrator |

Microsoft Muzic umbrella license (GETMusic, MuseCoco code):

```
https://github.com/microsoft/muzic/blob/main/LICENSE  → MIT, (c) Microsoft
```

MIT **code** is not a license to the **training corpus** and not a
license to ship generated music that copies © MIDI the model memorized.

---

## 6. Legal (already in-repo)

| Doc | URL / path | Tag |
| --- | --- | --- |
| This repo LEGAL.md | [`../../LEGAL.md`](../../LEGAL.md) | memo, not advice |
| CC0 1.0 | https://creativecommons.org/publicdomain/zero/1.0/legalcode | CC0 |
| Public Domain Mark 1.0 | https://creativecommons.org/publicdomain/mark/1.0/ | label |
| Duke Public Domain Day 2026 | https://web.law.duke.edu/cspd/publicdomainday/2026/ | US 1930 publications |
| Circular 15A | https://www.copyright.gov/circs/circ15a.pdf | US gov |
| MuseScore ToS | https://musescore.com/legal/terms | proprietary ToS |

Sample-library EULAs (Spitfire, BBCSO, etc.) are **proprietary** and
typically: commercial *cues* OK, **training on renders** forbidden.
Maestro never records those renders into a training set.

---

## 7. How to cite in NOTES.md

One line per experiment is enough, e.g.:

```
refs: Rimsky Gutenberg 33900 (PD); Uitdenbogerd skyline ACM MM 1999;
GM1 spec; Logic SMF help; music21 BSD-3; pretty_midi MIT.
```
