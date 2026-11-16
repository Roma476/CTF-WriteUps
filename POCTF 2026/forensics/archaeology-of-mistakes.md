# Archaeology of Mistakes

| | |
|---|---|
| **Section** | wave 5 |
| **Category** | forensics |
| **Solves** | 194 |

## Overview

The README gives a raw partition image (~40 MB) from Elena's laptop SSD and states that the filesystem metadata is inconclusive, but the blocks are not. Elena photographed something on 06/05, deleted the photo hours later, and then wrote a research attachment large enough to reuse part of the freed blocks, clobbering the middle of the JPEG.

The closing line — *the important thing about it is not what it shows* — is the design of the challenge. A JPEG starts with `FFD8` and the `APP1`/Exif segment; the picture itself is the entropy-coded scan data that comes after. An overwrite in the middle destroys the image and leaves the metadata untouched.

The image does not present itself as a filesystem:

```
$ file disk.raw
disk.raw: data

$ exiftool disk.raw
File Type        : URL
MIME Type        : application/x-mswinurl
```

ExifTool reads the leading bytes, decides the whole 42 MB file is a Windows `.url` shortcut, and reports nothing useful. `head` shows why: the blocks are a flat mixture of config files, log lines and XML from unrelated files.

## Solve

`binwalk -e disk.raw` reports no usable signatures and extracts nothing, so the file has to be carved:

```bash
photorec disk.raw
```

The carve produces `recup_dir.1` with hundreds of XML files and eight JPEGs. Each of them carries a complete EXIF block:

```bash
exiftool -DateTimeOriginal -UserComment *.jpg
```

| DateTimeOriginal | UserComment |
|---|---|
| 2026:06:02 10:12:03 | SPR reading room shelving, sealed folio area. token=VVXWD4RLUUNWMIAP |
| 2026:05:28 14:03:11 | Halberd lobby — waiting for curator, afternoon. token=ECQYLNUPY5XAI6PG |
| 2026:05:19 15:44:10 | Dissertation notebook, ch.3 marginalia. token=KXV77EBHNIX6CVOS |
| 2026:05:12 11:04:22 | Hollis Special Collections archive, west aisle. token=CXGQVX6ZAVZA3GTH |
| 2026:04:15 10:40:15 | Private library annex — east wing shelving. token=4IKEMTUJCDYLSZQ4 |
| 2026:04:28 09:16:57 | Latte at Redoubt Coffee, before advisor meeting. token=WOZ24DYJ7UUE5PVW |
| 2026:05:31 13:31:42 | SPR reading room monograph photocopy p.47. token=GDBAG3425RFRSNX3 |
| 2026:06:08 09:21:40 | Archive reviewer notes — Hollis manuscript annex. token=6T6OKAAEP27GX4VT |

Eight photos, eight tokens, and not one of them from 06/05. The missing file is the answer.

PhotoRec only emits files it can delimit, and the deleted photograph loses its scan data at the overwrite, so no ninth JPEG exists — but its EXIF header sits before the damage and is still in the image. A string search over the raw image shows **nine** tokens for eight files:

```bash
strings disk.raw | grep -i "token="
```

The extra one is the header that has no file:

```
Private library annex
 east wing shelving. token=████████████████ .Google Pixel 8 rear camera .
```

It is recognisable as a real EXIF record, not noise, because `grep -C 2` shows it surrounded by the same neighbours as the other comments — the `ASCII` type marker, the lens model, then the binary score data. This is the file that renders wrong: it cannot be rendered at all, which is precisely why its metadata is the only thing left to read.

Two traps are worth pointing out. Every photograph carries a token, so grepping for `token=` returns nine candidates of which eight are decoys. And one intact April photo carries the *same* `Private library annex — east wing shelving` text with a different token (`4IKEMT…`), so even the location string alone is ambiguous. The discriminator is the count: nine headers, eight files.

```
POCTF{████████████████}
```

For media that was deleted and then partially overwritten, the reliable part of a file is its edges — headers first. Carving gives a set of candidates, and the artifact worth chasing is often the one the carver refused to produce.