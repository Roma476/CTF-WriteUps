# The Apparatus, The Rapping

| | |
|---|---|
| **Section** | wave 3 |
| **Category** | steganography |
| **Solves** | 311 |

## Overview

The artifact is a 20.16-second, 22050 Hz, 16-bit mono WAV. The recording is mostly background noise interrupted by 65 bursts of a ~175 Hz tone. The bursts are the "rapping"; their durations and the gaps between them form Morse code.

## Solve

A 10 ms RMS envelope with a threshold of 1000 isolates the tone bursts from the background (background RMS is around 150). The burst durations fall into two clusters:

```text
short ~0.085 s  -> dot
long  ~0.240 s  -> dash
```

The gaps fall into two clusters:

```text
short ~0.080 s  -> intra-character gap
long  ~0.240 s  -> inter-character gap
```

There are no 7-unit word gaps. Grouping the 65 bursts at the long gaps and mapping the durations gives 16 Morse characters:

```text
.- ----. -.-. ..-. ..... ----- ...-- . -.-. -.-. --... . ...-- ----. ----- --...
```

Decoding the standard Morse table yields:

```text
████████████████
```

A minimal detector:

```python
import wave
import numpy as np

w = wave.open("seance-recording-1814.wav", "rb")
sr = w.getframerate()
x = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(float)

win, hop = int(sr * 0.01), int(sr * 0.005)
rms = np.array([
    np.sqrt(np.mean(x[i:i + win] ** 2))
    for i in range(0, len(x) - win, hop)
])
on = rms > 1000

runs = []
start = None
for i, v in enumerate(on):
    if v and start is None:
        start = i
    elif not v and start is not None:
        runs.append((start * hop / sr, i * hop / sr))
        start = None

chars = []
cur = []
for i, (a, b) in enumerate(runs):
    cur.append((a, b))
    if i == len(runs) - 1 or runs[i + 1][0] - b > 0.15:
        chars.append(cur)
        cur = []

morse = {
    ".-": "A", "-...": "B", "-.-.": "C", "-..": "D", ".": "E",
    "..-.": "F", "--.": "G", "....": "H", "..": "I", ".---": "J",
    "-.-": "K", ".-..": "L", "--": "M", "-.": "N", "---": "O",
    ".--.": "P", "--.-": "Q", ".-.": "R", "...": "S", "-": "T",
    "..-": "U", "...-": "V", ".--": "W", "-..-": "X", "-.--": "Y",
    "--..": "Z", "-----": "0", ".----": "1", "..---": "2",
    "...--": "3", "....-": "4", ".....": "5", "-....": "6",
    "--...": "7", "---..": "8", "----.": "9",
}

out = ""
for ch in chars:
    code = "".join("-" if b - a > 0.15 else "." for a, b in ch)
    out += morse[code]

print(out)
```

Output:

```text
████████████████
```

The recovered nonce is `████████████████`.