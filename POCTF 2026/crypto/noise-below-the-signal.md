# Noise Below the Signal

| | |
|---|---|
| **Section** | wave 6 |
| **Category** | crypto |
| **Solves** | 195 |

## Overview

Nexus Communications shipped an LWE key exchange with two defects: the error bound is far too small (`B = 3`) and the secret is drawn from the same narrow distribution (`s ∈ {−3,…,3}ⁿ`). The handout gives the public matrix `A` (30 × 15), the vector `b = A·s + e mod q`, and the parameters `n = 15`, `q = 1601`, `m = 30`, `B = 3`.

With such a small noise term and a small secret, the problem is not a learning problem at all: it is a closest-vector problem whose target is much closer than the lattice spacing, so a single lattice reduction recovers `s` exactly.

## Solve

The relation `b = A·s + e (mod q)` means that `b` lies within `√(m)·B ≈ 16` of the lattice point `A·s + q·k` for a suitable integer vector `k`. The lattice

```text
L = { A·s + q·k : s ∈ Z^n, k ∈ Z^m } ⊂ Z^m
```

has determinant `q^(m−n) = 1601^15`, so its Gaussian-heuristic shortest vector has norm about `√(m / (2πe)) · q^((m−n)/m) ≈ 53`. A difference of norm 16 is already below that, which is why the parameters are broken.

To turn the CVP into SVP, embed the target with a Kannan embedding in dimension `m + n + 1 = 46`:

```text
[ q·I_m      0      0 ]   (m rows)
[ A           I_n    0 ]   (n rows, one per column of A)
[ b           0      1 ]   (target row)
```

A lattice vector built from this basis with last coordinate `t = ±1` is `(A·s + q·k + t·b, s, t)`, which for `t = 1` equals `(−e, s, 1)` because `b ≡ −A·s + e`. Its norm is at most `√(m·B² + n·B² + 1) ≈ 21`, far below the ≈ 120 LLL could otherwise be forced to accept: the planted short vector is orders of magnitude shorter than the rest of the reduced basis.

So the 46-row basis is LLL-reduced over the integers (integer rows, floating-point Gram–Schmidt maintained through a QR decomposition, size reduction plus the Lovász condition), and the reduced rows are scanned for one whose last coordinate is `±1`. That row carries the error vector in its first `m` positions and the (possibly sign-flipped) secret candidate in the next `n`.

Exactly one reduced row is that short, and it comes out with `t = 1`, so the secret is the negation of its middle block. Checking the candidate against all 30 samples gives centered residues in `[−3, 3]`, confirming the recovery. Submitting the resulting 15-integer array returns the flag.

The recovered flag is ████████████████.