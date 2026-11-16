# Panoptican

| | |
|---|---|
| **Section** | wave 3 |
| **Category** | reverse engineering |
| **Solves** | 333 |

## Overview

The stripped `panoptican` binary reads a PGM image, compares it against a pre-enrolled reference identity, and prints an authorization code when the image matches.

## Solve

The match path computes a sum of squared differences between the input and a 128-byte reference image, accepting a score at most `0x7d0` (2000). On success the code at `0x137c` XORs the reference image with a 128-byte key and prints the result as `AUTH: %s`.

Both arrays are in `.data`: the key at virtual address `0x4010` (file offset `0x3010`) and the reference at `0x4090` (file offset `0x3090`), 128 bytes each. XORing the two extracted arrays byte-by-byte yields the full flag. The embedded 16×8 bitmap is the enrolled reference; the authorization code is the flag.

The submitted flag was POCTF{120.1814.████████████████.████████████████} and it was accepted.
