# A Map of Small Things

| | |
|---|---|
| **Section** | wave 4 |
| **Category** | crypto |
| **Solves** | 320 |

## Overview

The service uses a custom elliptic-curve Diffie-Hellman variant called MapCrypt. The curve is `y² = x³ + x (mod p)` with `p = 17759930830448937043`, and the base point is `G = (2, 2130375071143573863)`. The task is to recover the private key `k` from the public key `Q = kG`. The parameters are weak: the curve has `j = 1728`, `p ≡ 3 (mod 4)`, and the group order is smooth.

## Solve

Because `p ≡ 3 (mod 4)` and the curve is `y² = x³ + ax` with `a = 1`, `b = 0`, the group order is

```text
#E(Fp) = p + 1 = 17759930830448937044
       = 2² · 38603 · 121123 · 949584469
```

The base point has full order `p + 1`. For our instance the public key is

```text
Q = (12583775432034319774, 16756047493174394364)
```

Use Pohlig-Hellman. For each prime power `q^e`, compute

```text
P  = (N / q^e) · G
Q' = (N / q^e) · Q
```

and solve `Q' = xP` in the subgroup of order `q^e`. The three odd factors are small enough for baby-step giant-step; the largest subgroup has order `949584469`, so the BSGS table has about `sqrt(949584469) ≈ 30815` entries. The residues are:

```text
k mod 4         = 3
k mod 38603     = 13177
k mod 121123    = 33957
k mod 949584469 = 831978970
```

CRT gives

```text
k = 10255475597827708535
```

and the local check `k · G == Q` succeeds. The challenge accepts the raw decimal integer, so submitting `10255475597827708535` returns the canonical flag:

```text
████████████████
```

The private key is k = 10255475597827708535.