# The Wrong Channel

| | |
|---|---|
| **Section** | wave 6 |
| **Category** | steganography |
| **Solves** | 161 |

## Overview

The artifact is a 128×96, 8-bit RGBA PNG. The red, green, and blue channels have high-entropy low-order bits, so a standard RGB LSB scan produces noisy candidates and false positives. The real payload is not in those bits and not in an ancillary PNG chunk: the file contains only `IHDR`, one `IDAT`, and `IEND`. The payload is in the alpha channel.

## Solve

A chunk walk shows no `tEXt`, `zTXt`, or `iTXt` metadata, and the decompressed image data is exactly the expected size: `128 * 96 * 4 + 96` filter bytes. The RGB LSBs are the decoy.

The alpha channel is constant at 255 except for eight pixels at the start of the image:

```text
(0,0) a=239   (0,1) a=222   (0,2) a=125   (0,3) a=118
(0,4) a=4     (0,5) a=204   (0,6) a=77    (0,7) a=112
```

Read in raster order, those alpha values are the bytes:

```text
ef de 7d 76 04 cc 4d 70
```

This is the 8-byte nonce, or 16 hex characters:

```text
████████████████
```

The values are the alpha bytes themselves, not their least significant bits, which is why an RGB-only LSB scan misses them.

A minimal check:

```python
from PIL import Image

im = Image.open("channel-1814.png").convert("RGBA")
w, h = im.size
px = im.load()
raw = bytes(
    px[x, y][3]
    for y in range(h)
    for x in range(w)
    if px[x, y][3] != 255
)
print(raw.hex())
```

Output:

```text
████████████████
```