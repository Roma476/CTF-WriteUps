# Structural Failure

| | |
|---|---|
| **Section** | wave 7 |
| **Category** | forensics |
| **Solves** | 136 |

## Overview

The artifact is a 2,568-byte ZIP named `meridian-correspondence.zip`. The central directory and the End-of-Central-Directory record have been overwritten with garbage; the three local file headers and their DEFLATE streams are still present. The archive is therefore readable in principle, but not by tools that begin at the EOCD. `file` misidentifies it as an OpenPGP secret key, and Python's `zipfile` raises `BadZipFile: File is not a zip file`.

There is one additional wrinkle. The first byte of each local-header signature is damaged. The expected signature is `50 4b 03 04` (`PK\x03\x04`), but the archive contains:

```text
00000000: 94 4b 03 04 ...
000002a9: 53 4b 03 04 ...
00000451: 24 4b 03 04 ...
```

The `4b 03 04` tail survives in all three headers, so the headers can still be located by scanning for those three bytes and stepping back one byte. The rest of each local header — compression method, CRC, compressed size, uncompressed size, filename length, and filename — is intact. That is enough to decompress the entries without rebuilding the central directory.

## Solve

Start by confirming the damage:

```bash
file meridian-correspondence.zip
python3 -c 'import zipfile; zipfile.ZipFile("meridian-correspondence.zip")'
```

The first command prints `OpenPGP Secret Key Version 3`; the second prints `BadZipFile: File is not a zip file`. A search for `PK` or `PK\x03\x04` finds nothing. A search for the surviving `4b 03 04` finds exactly three occurrences, at offsets `1`, `682`, and `1106`; subtracting one gives the three local-header starts: `0`, `681`, and `1105`.

The local header format is:

```text
signature            4 bytes
version needed       2 bytes
flags                2 bytes
compression method   2 bytes
mod time             2 bytes
mod date             2 bytes
CRC-32               4 bytes
compressed size      4 bytes
uncompressed size    4 bytes
filename length      2 bytes
extra length         2 bytes
filename             variable
extra field          variable
compressed data      variable
```

Parsing the three headers gives:

| entry | header offset | data offset | compressed | uncompressed | CRC-32 |
|---|---|---:|---:|---:|---|
| `01_halberd_correspondence.txt` | `0` | `59` | 622 | 1128 | `f63692eb` |
| `02_steward_response.txt` | `681` | `734` | 371 | 663 | `2494a223` |
| `03_marchetti_annotations.md` | `1105` | `1162` | 1119 | 2121 | `64ef8dae` |

All three entries use method `8` (DEFLATE) with flags `0`, so the compressed sizes are in the local headers and there are no data descriptors. The last entry's data ends at offset `2281`; the remaining `287` bytes are the overwritten central directory and EOCD. There is no `PK\x01\x02` or `PK\x05\x06` in that tail, which is why standard tools refuse the file.

A minimal recovery script finds the headers, decompresses the raw DEFLATE streams, and checks every CRC:

```python
import struct, zlib

b = open("meridian-correspondence.zip", "rb").read()

starts = [i - 1 for i in range(len(b) - 2) if b[i:i+3] == b"\x4b\x03\x04"]

for start in starts:
    sig, ver, flags, method, mtime, mdate, crc, csize, usize, fnlen, extralen = \
        struct.unpack_from("<4sHHHHHIIIHH", b, start)
    name = b[start+30:start+30+fnlen].decode("utf-8")
    data_start = start + 30 + fnlen + extralen
    data = b[data_start:data_start+csize]
    out = zlib.decompress(data, -15)
    assert len(out) == usize, (name, len(out), usize)
    assert (zlib.crc32(out) & 0xffffffff) == crc, name
    open(name, "wb").write(out)
    print(f"{name}: {len(out)} bytes, CRC {crc:08x} OK")
```

The output is:

```text
01_halberd_correspondence.txt: 1128 bytes, CRC f63692eb OK
02_steward_response.txt: 663 bytes, CRC 2494a223 OK
03_marchetti_annotations.md: 2121 bytes, CRC 64ef8dae OK
```

The CRC check is the important part: the local headers contain the expected CRC-32 for each entry, and each decompressed stream matches. The recovery is not a guess.

The three recovered files tell the Meridian Circle story. `01_halberd_correspondence.txt` is Marion Halberd's request to the Circle's Steward: the Frame IV apparatus is still responding, she has documented seven completed sessions, and she wants the Circle's blessing to formalize the operation before "the subject for the coming session" is used. `02_steward_response.txt` is C. Whitmore's denial: the compact does not bend, the request is refused, and no archival copy of the response will be retained. `03_marchetti_annotations.md` is Elena's annotation set. Its first line contains the docket reference:

```text
# MARCHETTI 2026-14 docket ref: ████████████████
```

The annotations also record the provenance chain — Halberd to Steward on 06/09, Steward to Halberd on 06/11, Delacroix to Marchetti on 06/22, Marchetti to self on 06/28 — and Elena's instruction that the docket should reach her sister first, her advisor second, and not the Society, the university legal office, or Halberd.

The dead ends are useful. `file` guesses OpenPGP because the first byte of the first signature is `0x94` rather than `0x50`; the archive is still a ZIP. `zipfile` and other EOCD-based tools stop before reading the local headers, so they cannot list the archive even though the entries are intact. Rebuilding the central directory is unnecessary: the local headers contain the name, method, sizes, and CRC for every entry. The README's claim that the file was last seen as 240 KB is narrative; the actual artifact is 2,568 bytes, and the three local entries account for all of it except the 287-byte garbage tail. The raw DEFLATE streams must be decompressed with a negative window size (`zlib.decompress(data, -15)`); a normal `zlib.decompress(data)` expects a zlib header and fails because the streams are raw DEFLATE.

On the artifact page, submitting the raw token or `POCTF{████████████████}` returns:

```json
{"correct":true,"message":"Correct."}
```

The token is the 16-character docket reference from Elena's annotations, and the full marker is `POCTF{████…}`.

The docket reference in Elena's annotations is `████████████████`, and the flag is `POCTF{████…}`.