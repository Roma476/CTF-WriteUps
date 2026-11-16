# The Apparatus, Invocation

| | |
|---|---|
| **Section** | wave 1 |
| **Category** | misc |
| **Solves** | 633 |

## Overview

The challenge is a 7×7 grid of candles: forty-nine cells, each either lit or dark. A press toggles the pressed candle and its four orthogonal neighbours; the goal is to darken every candle. The notes make the algebra explicit: any sequence of presses is allowed, the order does not matter, only the set does, and a reset restores the team's own initial pattern. Pressing the same cell twice cancels, so each cell is pressed at most once. This is a Lights Out variant, and it is solved as a linear system over GF(2), not by search.

The page also exposes a `complete` endpoint that accepts the set of presses and returns the flag. The solver below reads the board from the screenshot, solves the system, and posts the resulting clicks to that endpoint.

## Solve

Read the board row-major, with `1` for a lit candle and `0` for a dark one. The captured board is:

```
1 1 1 0 0 1 1
1 0 1 1 1 1 1
1 1 0 1 0 0 0
1 0 0 1 0 1 1
0 1 1 0 0 1 1
1 1 0 0 1 0 1
1 0 0 1 1 0 1
```

Flattened, that is the 49-bit vector `b`. Let `x` be a 49-bit vector where `x[i] = 1` means cell `i` is pressed. Let `A` be the 49×49 matrix with `A[i][j] = 1` when pressing `j` toggles cell `i`, i.e. when `j == i` or `j` is an orthogonal neighbour of `i`. Every press is an XOR of a cross into the board, so the final state is `b XOR (A x)`. The goal is the all-zero state:

```
A x = b   over GF(2)
```

Two presses on the same cell cancel, which is exactly `1 + 1 = 0` in GF(2); that is why only the set matters and why brute force over `2^49` is unnecessary. Gaussian elimination over GF(2) — ordinary elimination with XOR instead of subtraction — solves the 49×49 system in 49³ operations and is exact. The 7×7 Lights Out matrix has full rank 49 over GF(2), so the solution is unique for every board.

The solver builds `A` from the toggle rule, augments it with `b`, reduces with Gauss-Jordan, and reads `x` back. The code is the payload that was run in the browser console on the challenge page:

```javascript
(async function () {
  const N = 7;
  const size = N * N;
  const initialBits = [
    1,1,1,0,0,1,1,
    1,0,1,1,1,1,1,
    1,1,0,1,0,0,0,
    1,0,0,1,0,1,1,
    0,1,1,0,0,1,1,
    1,1,0,0,1,0,1,
    1,0,0,1,1,0,1,
  ];

  // A[i][j] = 1 iff pressing j toggles cell i: self plus orthogonal neighbours.
  const A = Array.from({ length: size }, () => new Array(size).fill(0));
  for (let r = 0; r < N; r++) {
    for (let c = 0; c < N; c++) {
      const i = r * N + c;
      A[i][i] = 1;
      for (const [dr, dc] of [[-1,0],[1,0],[0,-1],[0,1]]) {
        const nr = r + dr, nc = c + dc;
        if (nr >= 0 && nr < N && nc >= 0 && nc < N) {
          A[i][nr * N + nc] = 1;
        }
      }
    }
  }

  // Gauss-Jordan on [A | b] over GF(2).
  const M = A.map((row, i) => [...row, initialBits[i]]);
  let rank = 0;
  for (let col = 0; col < size; col++) {
    let pivot = -1;
    for (let r = rank; r < size; r++) {
      if (M[r][col] === 1) { pivot = r; break; }
    }
    if (pivot === -1) continue;
    [M[rank], M[pivot]] = [M[pivot], M[rank]];
    for (let r = 0; r < size; r++) {
      if (r !== rank && M[r][col] === 1) {
        for (let c = col; c <= size; c++) M[r][c] ^= M[rank][c];
      }
    }
    rank++;
  }

  // Back-substitute; free variables (if any) stay 0.
  const x = new Array(size).fill(0);
  for (let r = rank - 1; r >= 0; r--) {
    let first = -1;
    for (let c = 0; c < size; c++) {
      if (M[r][c] === 1) { first = c; break; }
    }
    if (first === -1) continue;
    let val = M[r][size];
    for (let c = first + 1; c < size; c++) {
      if (M[r][c] === 1) val ^= x[c];
    }
    x[first] = val;
  }

  const clicks = [];
  for (let i = 0; i < size; i++) {
    if (x[i] === 1) clicks.push({ r: Math.floor(i / N), c: i % N });
  }

  console.log('clicks', clicks);
  const res = await fetch(window.location.pathname + 'complete', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ clicks }),
  });
  const data = await res.json();
  console.log(data);
  if (data.flag) alert('FLAG: ' + data.flag);
})();
```

For the captured board the elimination returns 15 presses:

```
(0,0) (0,3) (0,4) (1,6) (2,2) (3,0) (3,2) (3,6)
(5,0) (5,1) (5,5) (6,0) (6,1) (6,2) (6,5)
```

Applying those crosses to `b` zeroes every cell. The script then posts `{"clicks":[{"r":0,"c":0}, ...]}` to `window.location.pathname + 'complete'` and the server returns `{flag}`. The page path ends with `/`, so the relative endpoint resolves to the challenge's `complete` route; running the script from another origin loses the team session and the request fails.

The instructive dead ends are mostly modelling mistakes. Brute force is out: `2^49` is not searchable, and the linear structure makes it unnecessary. Including diagonals, or omitting the pressed cell, changes `A` and produces a set that leaves the board wrong. Inverting the bit convention (`0` for lit instead of `1`) solves for the complement and turns every candle on rather than off. Reading the image column-major instead of row-major transposes `b` relative to `A` and yields a plausible-looking but invalid click set. Sending a flat array or 1-indexed coordinates does not match the `{clicks:[{r,c}]}` schema. Pressing order is irrelevant, but duplicates cancel, so the set must contain each cell once.

The apparatus printed its name:

```
POCTF{████…}
```