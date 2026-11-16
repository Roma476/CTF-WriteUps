# Forty Measures Deep

| | |
|---|---|
| **Section** | wave 5 |
| **Category** | crypto |
| **Solves** | 168 |

## Overview

The artifact is a one-track MIDI file, `score.mid`, with one note per character. The notes are not random music: their MIDI numbers are ASCII codes shifted by a fixed amount. The challenge gives `POCTF` as known plaintext, which is enough to recover the substitution.

## Solve

The track contains 58 note-on events, each 480 ticks long. Reading the note numbers in order gives:

```text
80 79 67 84 70 64 60 57 63 54 61 54 57 63 ...
```

As ASCII, the first six are `POCTF@`. Subtracting 5 from every note gives the ciphertext:

```text
KJ>OA;74:1814:THCUU@FOPK2R4NEO:2GDJS3B3TS=6SDS=G772EGO2EDV
```

The known plaintext `POCTF{` matches `KJ>OA;` under a simple substitution:

- letters, `>`, `@`, and `=` shift by +5 (`K`→`P`, `J`→`O`, `>`→`C`, ...),
- digits are unchanged,
- `:` becomes `.`, `;` becomes `{`, and `V` becomes `}`.

Applying that substitution to the whole ciphertext:

```python
cipher = "KJ>OA;74:1814:THCUU@FOPK2R4NEO:2GDJS3B3TS=6SDS=G772EGO2EDV"
out = []
for ch in cipher:
    if ch.isdigit():
        out.append(ch)
    elif ch == ':':
        out.append('.')
    elif ch == ';':
        out.append('{')
    elif ch == 'V':
        out.append('}')
    else:
        out.append(chr(ord(ch) + 5))
print(''.join(out))
```

The output has the canonical shape `POCTF{74.1814.<nonce>.<sig>}`:

```text
████████████████
```

The score decodes to the flag ████████████████.