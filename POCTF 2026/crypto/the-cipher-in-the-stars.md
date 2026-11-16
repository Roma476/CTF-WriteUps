# The Cipher in the Stars

| | |
|---|---|
| **Section** | wave 8 |
| **Category** | crypto |
| **Solves** | 73 |

## Overview

The transcript contains 1,400 photon records, four announced state pairs, 128 parity-check rows, and a 128-bit syndrome. Each pair contains one rectilinear (`+`) state and one diagonal (`x`) state. The sender announces the pair; the receiver records a basis and an outcome.

A record is conclusive only when the receiver's outcome is orthogonal to the announced state in the receiver's basis. In that case the sender must have sent the other announced state, so its bit is the sifted bit. All other records are discarded.

## Solve

Apply the unambiguous-state-discrimination rule to the 1,400 records. There are 347 conclusive bits. The first 256 are the raw sifted key used by the reconciliation layer.

For each of the 128 published parity-check rows, compute the parity of the corresponding bits in the first 256 sifted bits. Compare these parities with the published syndrome; the difference is the syndrome of the transmission errors. Set up the 128 linear equations over GF(2) and solve for a low-weight error vector with a SAT solver. The sparse solution flips the following zero-indexed positions:

```text
1, 18, 54, 91, 95, 106, 137, 164, 173, 211
```

Flip those ten bits, then pack the corrected 256 bits most-significant-bit first into 32 bytes. The resulting hex string is the recovered shared key:

```text
████████████████
```

The accepted answer was the recovered key `████████████████`.