# The Hidden Path

| | |
|---|---|
| **Section** | wave 5 |
| **Category** | steganography |
| **Solves** | 160 |

## Overview

The artifact is a one-page type specimen, `specimen.pdf`, with sixteen glyph outlines. Each glyph is a house-like shape: a rectangle with a roof. The right vertical wall ends either above or below the roof apex. Those two states are the only difference between the glyphs, and they encode one bit each. Sixteen bits make a four-digit hexadecimal nonce.

## Solve

Extract the glyph paths from the PDF content stream. Each path has the form

```text
n x0 y0 m x1 y1 l x2 y2 l x3 y3 l x4 y4 l h
```

The second `l` point is the top of the right wall, and the third `l` point is the roof apex. In PDF coordinates the y-axis points up, so a right-wall top above the apex is a 0 and one below it is a 1. Read the glyphs in row-major order.

```python
import re, zlib, base64

raw = open('specimen.pdf', 'rb').read()
stream = re.search(rb'stream\r?\n(.*?)endstream', raw, re.S).group(1).strip()
if stream.endswith(b'~>'):
    stream = stream[:-2]
content = zlib.decompress(base64.a85decode(stream)).decode('latin1')

paths = re.findall(
    r'n ([\d.]+) ([\d.]+) m ([\d.]+) ([\d.]+) l '
    r'([\d.]+) ([\d.]+) l ([\d.]+) ([\d.]+) l '
    r'([\d.]+) ([\d.]+) l h',
    content,
)

bits = ''.join('0' if float(p[5]) > float(p[7]) else '1' for p in paths)
print(bits, f'{int(bits, 2):04X}')
```

The sixteen comparisons produce the bit string

```text
████████████████
```

The page accepts the raw nonce, so no `POCTF{...}` wrapper is needed:

```text
████████████████
```

The specimen encodes the raw nonce ████████████████.