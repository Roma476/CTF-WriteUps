# Frequency and Consequence

| | |
|---|---|
| **Section** | wave 2 |
| **Category** | misc |
| **Solves** | 373 |

## Overview

The artifact is `signal.wav`: 9.0 seconds, 44.1 kHz, mono, 16-bit PCM. It carries sixteen constant tones buried in broadband noise, one per 500 ms slot. The sixteen tones are drawn from a 32-symbol alphabet spaced 50 Hz apart starting at 500 Hz (500, 550, …, 2050 Hz), which maps exactly onto the base32 alphabet `A–Z2–7`. The goal is the 16-character nonce.

## Solve

Reading the WAV and computing a sliding spectral peak shows the signal is organized in 500 ms blocks. Sixteen blocks span 8 s; the file is 9 s long, so the message starts at 0.5 s and ends at 8.5 s, with 0.5 s of noise before and after. Windows that start on multiples of 0.5 s produce a single clean peak (magnitude ≈ 2.4·10⁷), while windows offset by 0.25 s straddle two symbols and give mixed spectra (≈ 1.2·10⁷), which fixes the slot boundaries at `[0.5 + 0.5k, 1.0 + 0.5k)`.

For each slot, measure the energy at all 32 candidate frequencies with the Goertzel algorithm (a 0.5 s coherent integration, i.e. a 2 Hz-resolution DFT):

```python
for k in range(16):
    seg = x[int((0.5 + 0.5*k)*fs):int((1.0 + 0.5*k)*fs)]
    mags = [goertzel(seg, 500 + 50*i) for i in range(32)]
    sym  = ALPHABET[max(range(32), key=lambda i: mags[i])]
```

The winning tone in every slot beats the runner-up by a factor of at least ~21, so the decision is unambiguous. Indexing each detected tone through `ABCDEFGHIJKLMNOPQRSTUVWXYZ234567` yields the base32 nonce.

The 16-character nonce is `████████████████`.