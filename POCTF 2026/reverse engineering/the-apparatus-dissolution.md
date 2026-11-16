# The Apparatus, Dissolution

| | |
|---|---|
| **Section** | wave 7 |
| **Category** | reverse engineering |
| **Solves** | 122 |

## Overview

`apparatus_dissolution.c` embeds the dissolved output in `DATA[]` and exposes the forward cipher. Each of the four passes substitutes every byte through a 256-byte S-box (`TBL`), then rotates the buffer left by one byte.

## Solve

Invert the passes in reverse order. For each pass, rotate the buffer right by one byte, then apply the inverse S-box (`inv[TBL[i]] = i`). After four iterations `DATA[]` decrypts to the flag.

The submitted flag was POCTF{116.1814.████████████████.████████████████} and it was accepted.
