# The View from Above

| | |
|---|---|
| **Section** | wave 7 |
| **Category** | osint |
| **Solves** | 113 |

## Overview

The image is an aerial crop of a long hull lying on sand: no superstructure, no port, no skyline, nothing that geolocates on its own. The description is the only lead, and it is written as a joke about status — *ex-ship. Non-vessel. Un-boat.* A stranded, abandoned hull is, in maritime law, no longer a vessel, which is exactly what the picture shows: the remains of a ship rather than a ship. *Retirement was much less kind to the old lady* adds the second fact: she was already old when she came ashore.

The task is to identify the wreck from its history and answer a single question: at what time did she run aground.

## Solve

The hull is the only distinctive shape in the frame, so the search starts there: a reverse image search on the crop, cropped again to the wreck itself, returns a name — **Aline Ramos**.

That is a lead, not an answer. Confirming it means checking that the record describes the geometry in the image. The Aline Ramos lies at the tip of Ilha do Caju, near the entrance to the barra do Carrapato, south of Tutóia in Maranhão, Brazil: a single straight hull on a sandbank at the mouth of a tidal inlet, no infrastructure around it. That matches the crop line for line.

The history also matches the hints. The ship was launched in August 1963 as the **Barão do Amazonas** and later renamed Aline Ramos — two identities, one of them retired. On 16 November 1981 she was carrying salt when she grounded; a bureaucratic fight over insurance followed, and the hull was towed closer to the beach. It stayed there: looted, corroded, and now used as an artificial breakwater that is fully exposed at low tide. An eighteen-year-old cargo ship that ends up as scenery is the "retirement" the description is mocking.

The date comes from the same record, and so does the time, given as *por volta das 19h40* — around 19:40 local time on 16 November 1981. Note the source's own inconsistency: the standfirst of the article says "late 1980s", while the body gives the exact date. The dated body wins; a rounded decade in a subtitle is not evidence.

The last step is a format trap, not an arithmetic one. Maranhão runs on UTC−3, and 19:40 is the local reading on a 24-hour clock. The checker wants the same reading on a 12-hour clock:

```
19:40  →  7:40 PM
```

Submitting `19:40` is rejected. Submitting `7:40` — the identical clock time, written the American way — returns the flag. No timezone conversion is involved, and anyone who starts converting between zones will move away from the answer rather than toward it.

The answer is **7:40 PM**.