# The Notary's Seal

| | |
|---|---|
| **Section** | wave 7 |
| **Category** | crypto |
| **Solves** | 150 |

## Overview

The notary seals a document by computing `c = m^e mod n` with `e = 3`. The modulus is 2048 bits, but the seal is only 1387 bits, so `m^3 < n`. The modular reduction never happens: the seal is an exact integer cube. The document is recovered with an integer cube root, no factoring required.

## Solve

The page gives a 2048-bit modulus `n`, the exponent `e = 3`, and the seal

```text
c = 0x7e74fc33f9eec5d02a253749eeb1dbea50aa45a16c453324712b2419634a8dca31deeea213747c5c99d055a9e68e191a2e11450c7080fe4532f7a7f690dc0dd388dfd87ca6c817662158d4bffdf519e213cca8491e4fdfd7183225cd26dd3d6d2d8dacce7008b5c9a25dbdb1f1309cb85cf7be387cfd7c2a191fb3ea1951b95ace6b704718fd4fee753830d0fd76c03bada5f91d03334a1c42db26026d6d519614ce98f176c2fffcbd43a33df65
```

Because `c < n` and `c` is a perfect cube, compute its integer cube root by binary search:

```python
def icbrt(x):
    lo, hi = 0, 1 << ((x.bit_length() + 2) // 3)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if mid**3 <= x:
            lo = mid
        else:
            hi = mid - 1
    return lo

m = icbrt(c)
assert m**3 == c
print(m.to_bytes((m.bit_length() + 7) // 8, 'big').decode())
```

The root is 463 bits, or 58 bytes. It decodes to the flag:

```text
████████████████
```

The sealed document is the flag ████████████████.