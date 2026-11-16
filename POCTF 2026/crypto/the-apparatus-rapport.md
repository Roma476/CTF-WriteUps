# The Apparatus, Rapport

| | |
|---|---|
| **Section** | wave 2 |
| **Category** | crypto |
| **Solves** | 487 |

## Overview

The challenge provided two artefacts: a transcript from a mechanical tic-tac-toe apparatus, and a block of ciphertext. The transcript listed the apparatus's moves by board coordinate rather than by turn number, so the first problem was ordering them. The second problem was the alphabet: the ciphertext contained punctuation and braces, so it could not be a Vigenère over A–Z.

## Solve

The apparatus board is a 3×3 grid labelled A–I. Sorting the move table by its turn index yields the cell sequence:

    A  G  E  B  I

That sequence is the key. With A = 0 … Z = 25 it maps to the shifts 0, 6, 4, 1, 8.

A standard Vigenère table covers only 26 letters, but the ciphertext bytes span the full printable ASCII range (32–126, 95 symbols). The cipher is the same additive scheme over that alphabet:

    p_i = 32 + ((c_i - 32) - (k_i - 65)) mod 95

with `k_i` the key letter as its ASCII code, cycling every five characters. The reduction is modulo 95, not modulo 26.

The first five ciphertext characters are `PUGUN`. Applying the shifts:

    P - 0 = P
    U - 6 = O
    G - 4 = C
    U - 1 = T
    N - 8 = F

The plaintext therefore opens `POCTF{`, which is the expected prefix and confirms both the key and its phase: the key starts on the first ciphertext character, not after the prefix.

One dead end is worth recording. Since the key uses five distinct letters, sorting them alphabetically to `ABEGI` looks harmless, but the cipher is position-dependent. With `ABEGI` the second character decrypts as `U - 1 = T`, producing `POTTF{`, which is not a valid flag. The order taken from the transcript must be preserved.

A second ciphertext block, decrypted with the same key and phase, produced the flavortext:

> By salt and by ash, by the breath drawn but not returned, we open the way.

The full decryption is one line once the alphabet is fixed:

```python
p = "".join(chr(32 + ((ord(c) - 32) - (ord(k[i % 5]) - 65)) % 95)
            for i, c in enumerate(ct))
```

The flag is `POCTF{████…}`.