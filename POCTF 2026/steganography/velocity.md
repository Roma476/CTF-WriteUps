# Velocity

| | |
|---|---|
| **Section** | wave 4 |
| **Category** | steganography |
| **Solves** | 257 |

## Overview

The artifact is a format-0 Standard MIDI file with one track, 480 ticks per quarter note, and 64 note-on events. The notes form a C-major étude sketch; the pitches are the cover. The payload is in the note-on velocities: every event uses either `0x60` (96) or `0x30` (48), so each note carries one bit.

## Solve

`file etude-in-c-1814.mid` reports `Standard MIDI data (format 0) using 1 track at 1/480`. The track contains meta events for tempo, time signature, key signature (C major), and track name, followed by 64 `90 <note> <velocity>` note-on events. The note-off events are `80 <note> <velocity>` and are irrelevant.

The velocities take only two values:

```text
0x60 = 96  -> 1
0x30 = 48  -> 0
```

Read the note-on events in file order and group the resulting 64 bits into 16 nibbles, most significant bit first. The first four notes have velocities `0x60, 0x60, 0x60, 0x30`, which gives `1110` = `e`:

```text
1110 1111 1010 1111 0110 0011 0010 0000
0110 0011 1000 0001 0011 1000 1111 1110
```

A minimal extraction:

```python
from pathlib import Path

b = Path("etude-in-c-1814.mid").read_bytes()
vel = [b[i + 2] for i in range(len(b) - 2) if b[i] == 0x90]
bits = "".join("1" if v == 0x60 else "0" for v in vel)
assert len(bits) == 64

nonce = "".join(f"{int(bits[i:i + 4], 2):x}" for i in range(0, 64, 4))
print(bits)
print(nonce)
```

Output:

```text
1110111110101111011000110010000001100011100000010011100011111110
████████████████
```

The byte scan is safe for this file because the track uses explicit note-on status bytes and no `0x90` appears as a data byte; a general parser should still track MIDI running status.

The recovered nonce is `████████████████`.