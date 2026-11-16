# The Geometry of Secrets

| | |
|---|---|
| **Section** | wave 7 |
| **Category** | steganography |
| **Solves** | 109 |

## Overview

The artifact is a 35-line Wavefront OBJ. It declares 24 vertices and 3 faces, with the header `# Marchetti Modeling Suite — export`, `# Geometry, decorative. Provenance uncertain.`, and `# Model: piece-1814`. A comment `# reference geometry follows` separates the first 16 vertices from the last 8. The last 8 are a cube at `±2.0`, and the three faces reference only those vertices (`17`–`24`):

```
f 17 18 19 20
f 21 22 23 24
f 17 18 22 21
```

The first 16 vertices are referenced by no face. In a normal mesh every vertex is used; here the first 16 are orphaned. That is the first clue: the geometry is a carrier, and the unused vertices are the payload.

The second clue is the coordinates of those 16 vertices. Every one has a uniform magnitude: either all three coordinates are `±0.5`, or all three are `±1.0`. So each vertex is a cube corner (three sign bits) plus a scale bit (inner shell `0.5` vs outer shell `1.0`). Three bits plus one bit is a nibble, and 16 vertices give exactly 16 hex digits — the length of the team nonce. The reference cube at `±2.0` is a third, larger shell: it makes the file look like a decorative model, but it is not part of the message.

## Solve

The file inventory confirms the split:

```bash
grep -c '^v ' piece-1814.obj   # 24
grep -c '^f ' piece-1814.obj   # 3
grep -n '^#' piece-1814.obj    # comments, including "reference geometry follows"
```

The first 16 vertices are:

```
v -0.5000 -0.5000 -0.5000
v -1.0000 -1.0000  1.0000
v  1.0000 -1.0000 -1.0000
v  0.5000 -0.5000 -0.5000
v -1.0000  1.0000 -1.0000
v  0.5000 -0.5000 -0.5000
v  1.0000 -1.0000 -1.0000
v  1.0000 -1.0000 -1.0000
v  0.5000  0.5000  0.5000
v -1.0000  1.0000  1.0000
v  0.5000 -0.5000 -0.5000
v -1.0000  1.0000  1.0000
v -1.0000  1.0000 -1.0000
v -0.5000 -0.5000 -0.5000
v -1.0000 -1.0000  1.0000
v  0.5000  0.5000  0.5000
```

The decode is one nibble per vertex, with the bits in the order the coordinates appear: sign of `x`, sign of `y`, sign of `z`, then the scale bit. Positive is `1`, negative is `0`; `1.0` is `1`, `0.5` is `0`. The nibble is:

```
nibble = (x > 0) << 3 | (y > 0) << 2 | (z > 0) << 1 | (abs(x) == 1.0)
```

| # | vertex | signs (x,y,z) | scale | nibble |
|---|---|---|---|---|
| 1 | -0.5 -0.5 -0.5 | 000 | 0.5 | 0 |
| 2 | -1.0 -1.0 1.0 | 001 | 1.0 | 3 |
| 3 | 1.0 -1.0 -1.0 | 100 | 1.0 | 9 |
| 4 | 0.5 -0.5 -0.5 | 100 | 0.5 | 8 |
| 5 | -1.0 1.0 -1.0 | 010 | 1.0 | 5 |
| 6 | 0.5 -0.5 -0.5 | 100 | 0.5 | 8 |
| 7 | 1.0 -1.0 -1.0 | 100 | 1.0 | 9 |
| 8 | 1.0 -1.0 -1.0 | 100 | 1.0 | 9 |
| 9 | 0.5 0.5 0.5 | 111 | 0.5 | e |
| 10 | -1.0 1.0 1.0 | 011 | 1.0 | 7 |
| 11 | 0.5 -0.5 -0.5 | 100 | 0.5 | 8 |
| 12 | -1.0 1.0 1.0 | 011 | 1.0 | 7 |
| 13 | -1.0 1.0 -1.0 | 010 | 1.0 | 5 |
| 14 | -0.5 -0.5 -0.5 | 000 | 0.5 | 0 |
| 15 | -1.0 -1.0 1.0 | 001 | 1.0 | 3 |
| 16 | 0.5 0.5 0.5 | 111 | 0.5 | e |

Reading the nibbles in vertex order gives:

```
0 3 9 8 5 8 9 9 e 7 8 7 5 0 3 e
```

which is the nonce:

```
████████████████
```

The whole extraction is small:

```python
verts = []
for line in open("piece-1814.obj"):
    if line.startswith("v "):
        verts.append(tuple(map(float, line.split()[1:4])))

nonce = ""
for x, y, z in verts[:16]:
    nibble = ((x > 0) << 3) | ((y > 0) << 2) | ((z > 0) << 1) | int(abs(x) == 1.0)
    nonce += format(nibble, "x")

print(nonce)
```

Output:

```
████████████████
```

Submission is the standard JSON form:

```bash
curl -sS -X POST 'https://pointeroverflowctf.com/challenges/the-geometry-of-secrets/submit' \
  -H 'Content-Type: application/json' \
  -b 'session=<cookie>' \
  --data '{"flag":"████████████████"}'
```

and the response is:

```json
{"correct":true,"message":"Correct."}
```

The reference cube is the main dead end. Its eight vertices and three faces invite two wrong readings. First, treating the first 16 vertices as a raw bitstream — 48 sign bits followed by 16 scale bits — gives `064524ee340f6b5a` (or `6b5a064524ee340f` with the streams reversed). It is 16 hex characters, so it looks plausible, but it is rejected. Second, using the reference cube's vertex order as a codebook for the eight corners gives `c5febeff03e3bc50` (corner index plus scale as the low bit) or `6af7d7ff0979d6a0` (scale as the high bit); both are rejected. The reference cube is exactly what its comment says: reference geometry, not a key. The message is in the orphan vertices, and the encoding is per-vertex, not per-axis-stream.

The other decoys are the comments and the mesh. `strings` on the OBJ returns only the Marchetti header and the `reference geometry follows` line; there is no text fragment. The three faces form only part of a cube and encode nothing. The `±2.0` cube is visually a third shell, but the payload is the two inner shells at `±0.5` and `±1.0`; including the reference vertices in the decode shifts the string and fails.

The construction is consistent: three sign bits choose one of the eight corners of a cube, the scale bit chooses the shell, and the resulting four-bit value is a hex digit. Sixteen vertices fill sixteen hex digits, matching the sixteen-character nonce. The phrase "precision in every dimension" is the hint for the fourth bit: the magnitude is the extra dimension that turns a 3D corner into a nibble.

The geometry decodes to `████████████████`, and the marker is `POCTF{████…}`.