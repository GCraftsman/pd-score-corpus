# data/

| File | Role |
| --- | --- |
| `composers.allowlist.json` | v1 composers (died 1908 or earlier) with aliases |
| `composers.denylist.json` | never keep (modern / soundtrack names) |
| `composers.graylist.json` | died after 1908; **not** in v1 |
| `manifest.csv` | filter output (PDMX paths + composer/title/piano flag). Generated. |
| `manifest.example.csv` | five **EXAMPLE** rows for tests/docs if the real CSV is absent |
| `stats.json` | counts from the last filter run. Generated. |

`.cache/PDMX.csv` and the Zenodo tarballs live outside this folder and
are gitignored. They are not the GitHub-repo payload.
