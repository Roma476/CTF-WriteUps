# The Apparatus, Apport

| | |
|---|---|
| **Section** | wave 4 |
| **Category** | osint |
| **Solves** | 274 |

## Overview

A parcel with no return address arrives at the Liminal Society for Spectral Fellowship. It contains five recovered files: four cohere around a single person, and one item the archivists cannot account for. Nothing names the subject directly, so the figure has to be reconstructed by cross-reference. The deliverable is `SURNAME_YEAR`, where the year is a significant biographical event that also appears somewhere in the files (for example, `BLAVATSKY_1875`).

## Solve

The archive holds five files:

```
coordinates.gpx
correspondence.eml
recovered.jpg
transcript.pdf
unaccounted_transmission.txt
```

`coordinates.gpx` is the strongest skeleton. Its four waypoints already give the outline of a life:

| waypoint | time |
|---|---|
| Birthplace (Nashua) | 1857-06-27 |
| Boston, James's first sitting | 1885-05-01 |
| Cambridge (Hodgson) | 1889-11-01 |
| Death (Boston) | 1950-07-03 |

`correspondence.eml` is a reply from `archives@harvard.edu` to `researcher@lssf.org.uk`, subject `Re: William James — SPR correspondence file`. Its body states that James began the investigation in 1885 on his mother-in-law's suggestion; that the medium was a Boston housewife born in Nashua, New Hampshire, in 1857; and that Richard Hodgson of the Society for Psychical Research ran the American investigation until his death in 1905.

`transcript.pdf` is not plain text: its content stream is ASCII85 plus Flate, so `pdftotext` can silently miss it. Decoding the stream directly recovers the body:

```python
import re, zlib, base64

d = open('transcript.pdf', 'rb').read()
s = re.search(rb'stream\r?\n(.*?)endstream', d, re.S).group(1).strip().rstrip(b'~>')
print(zlib.decompress(base64.a85decode(s)).decode('latin1'))
```

The text is a note from a Harvard professor of philosophy to a Cambridge colleague about his continuing investigation — begun in 1885 — of a Boston medium whose principal control called itself "Dr. Phinuit". It quotes: "I do not doubt that Mrs. P. is in possession of a power as yet unexplained. I have investigated her for twenty years…"

`recovered.jpg` carries EXIF time `1887:11:15 21:30:00`, GPS data, and a description of a parlor scene: a woman in plain dress seated in an armchair, hands in her lap, eyes closed, while an academic gentleman takes notes at a small table. No name is engraved on the image; it is corroboration, not a label.

```
exiftool recovered.jpg
strings -a recovered.jpg | head
```

`unaccounted_transmission.txt` is the fifth item. It is a `SEANCE.EXE` fragment with no sender and a cryptic remark about the closed circle; it names no person, place or date. It is the file the archivists cannot account for, and it is a red herring.

Cross-referencing the four coherent files yields an American trance medium, a Boston housewife, born in Nashua, New Hampshire, on 27 June 1857, whose principal control was "Dr. Phinuit", investigated by William James from 1885 and by Richard Hodgson for the SPR. That is Leonora Piper (née Leonora Evelina Simonds). The surname is `PIPER`.

The year is the second decision. The files contain 1857, 1885, 1887, 1889, 1905 and 1950. The obvious pick — 1857, the birth year — is present and biographically correct, but it is not the event the challenge points at. The year 1885 appears in two of the four coherent files (the email and the transcript) and is labelled explicitly in the GPX as "Boston, James's first sitting". It is the incident that started the investigation and made the medium famous, matching the prompt's "a birth, a founding, a publication, a notable incident". The intended event is the first sitting of 1885.

The accepted answer is PIPER_1885.