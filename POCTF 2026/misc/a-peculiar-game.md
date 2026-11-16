# A Peculiar Game

| | |
|---|---|
| **Section** | wave 4 |
| **Category** | misc |
| **Solves** | 215 |

## Overview

The challenge hands out a per-team PDF dressed as an 1887 chess column, *The Vienna Correspondence Monthly*. It reports a short correspondence game between "Signor Marchetti" and "Dr. Whitmore", annotated move by move, concluding 1/2-1/2. The prompt insists that something about the moves is very peculiar and that the game "isn't quite about chess". The objective is a 16-hex nonce.

## Solve

The game, transcribed from the PDF in PGN order, is:

```
1. b4   Nxb3    2. Nxd3  h4      3. Nxe3  Nxg3    4. Nxg3  Nxf3
5. Nxc3 Nxb3    6. c4    Nxa3    7. Nxg3  Nxg3    8. f4    f4
```

Two properties stand out immediately.

First, the game is not legal chess. Black cannot play `1...Nxb3` on the first move, both sides "capture" on `g3`, and both play `f4` in the last move. The notation is being used as a carrier, not as a game.

Second, and decisively, every single destination square lies on rank 3 or rank 4. The sixteen half-moves visit only the band of squares `a3`–`h4`, which contains exactly sixteen squares. Sixteen squares for a 16-hex nonce means each destination square is a hex digit.

The natural indexing of that 2×8 band is by file letter and then by rank, i.e. the alphabetical order of the square names:

```
a3=0  a4=1  b3=2  b4=3  c3=4  c4=5  d3=6  d4=7
e3=8  e4=9  f3=a  f4=b  g3=c  g4=d  h3=e  h4=f
```

so that a move like `b4` maps to `1*2 + (4-3) = 3`, while `f4` maps to `5*2 + (4-3) = b`.

Applying this table, in game order, to the sixteen destination squares

```
b4  b3  d3  h4  e3  g3  g3  f3  c3  b3  c4  a3  g3  g3  f4  f4
```

produces the sixteen nibbles of the nonce. Submitting the raw nonce to the challenge endpoint was accepted ("The game concludes."), which confirms the reading: the players were not playing chess at all, they were spelling out a hexadecimal string on the only sixteen squares the game ever touched.

The 16-hex nonce is `████████████████`.