# Invisible Ink

| | |
|---|---|
| **Section** | wave 1 |
| **Category** | steganography |
| **Solves** | 583 |

## Overview

The challenge ships a single script, `invisible_text.py`, and a paragraph about how humans survive by communicating — crying, language, Morse, ASL. The last sentence is the one that matters: some messages are not broadcast for the world to see, and "I'm confident you'll **see** what I'm communicating if you **look** in the right place."

The script reassembles a list of base64 chunks, inflates them with zlib and prints the result, which its docstring calls a diary entry recovered in a custom "DR3 archive format". What actually comes out is a block of Unicode Braille, roughly 50 cells wide and 30-odd rows tall.

Braille is not a font, it is a raster: each glyph is a 2×4 dot matrix. So the block is a bitmap a little over a hundred pixels wide, and rendered it is a dithered image of the **default profile silhouette** — the anonymous head-and-shoulders avatar that social networks show when nobody has uploaded a picture.

That is the joke of the visible layer. The diary reader promises a diary and delivers the visual equivalent of "no image here": a placeholder for someone who has nothing to show. The output was never the message. The flag is in the file that produces it.

## Solve

`cat` shows a perfectly ordinary Python file. Look at what happens at the end of each line instead:

```bash
grep -nP '[ \t]+$' invisible_text.py | head
```

Almost every line carries whitespace between the end of its content and the newline, and the pattern alternates: a long run of spaces and tabs, then a line with a single tab, then a long run again. The long runs are carriers; the single tabs are camouflage, enough noise that the file looks consistently sloppy rather than deliberately written.

This is classic whitespace steganography. Space and tab are invisible in a terminal, survive copy-paste and most editor round-trips, and each one holds a bit: space is `0`, tab is `1`. One carrier run is one byte, padded on the left with spaces, which is why the runs are wider than the eight bits the character actually needs.

```python
from pathlib import Path

data = Path("invisible_text.py").read_bytes()
out = []

for line in data.splitlines():
    tail = line[len(line.rstrip(b" \t")):]
    if len(tail) < 10:
        continue
    bits = "".join("0" if c == 0x20 else "1" for c in tail)
    out.append(chr(int(bits, 2)))

print("".join(out))
```

The threshold only skips the lines that are too short to hold a padded byte; it is not part of the encoding. The output opens with `POCTF{`, which is the check that the bit order and the padding side are both right:

```
POCTF{████████████████}
```

The title is the whole hint, and it is unusually literal. The readable text of the program is the decoy; the program's *bytes* are the message. Two practical consequences: the file has to be read as bytes, because any decode/encode round-trip can normalise or drop the runs, and an editor configured to trim trailing whitespace on save destroys the payload without warning.