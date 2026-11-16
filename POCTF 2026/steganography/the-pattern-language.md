# The Pattern Language

| | |
|---|---|
| **Section** | wave 8 |
| **Category** | steganography |
| **Solves** | 50 |

## Overview

`pattern.png` is a 440-by-440 tartan swatch with a 20-pixel border and a 16-by-16 grid of 25-pixel threads. Each cell is a one-pixel checkerboard made from two shades. The shades are multiples of `0x11`, so they are nibbles `0x0` through `0xf` rendered as grayscale.

The plain weave is the clue: at every intersection the visible pixel is exactly one of the two thread colors. The color common to a column is the warp thread; the color common to a row is the weft thread. Reading the columns and rows gives the two 16-nibble setts:

```text
warp: 7899d6bac0a05dfc
weft: ebf0bfd3fca1fb61
```

## Solve

The nonce is not the concatenation of the setts. The image is a two-share visual-cryptography construction: the warp and weft are independent shares, and the secret is their XOR. Interpret each sett as an 8-byte value and XOR them:

```python
warp = int("7899d6bac0a05dfc", 16)
weft = int("ebf0bfd3fca1fb61", 16)
print(f"{warp ^ weft:016x}")
```

The result is a 16-hex-character raw nonce. Submitting that value on the challenge page was accepted. The accepted raw nonce was `████████████████`.