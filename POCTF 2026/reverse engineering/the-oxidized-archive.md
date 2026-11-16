# The Oxidized Archive

| | |
|---|---|
| **Section** | wave 6 |
| **Category** | reverse engineering |
| **Solves** | 161 |

## Overview

The handout is a stripped x86-64 Linux ELF (`oxidized_archive`) plus a README that promises "source and build instructions" but ships neither. The prompt says the utility reads no input, recovers an archive and prints it, yet prints nothing, because the archive and its key are baked into the binary and the author's crypto is not crypto.

Running it confirms the description: no output, exit status 1. Static analysis of the Rust binary is enough to recover both constants and to reimplement the toy cipher in a dozen lines of Python.

## Solve

Because the binary is stripped, function boundaries come from the `.eh_frame` FDE list rather than the symbol table. The user code sits at the very start of `.text`: a single FDE covers `0x15791`-`0x16261`, and that range is the program's `main`.

Reading it top to bottom:

1. `main` calls `std::env::args()` and branches on the argument count. With exactly one extra argument it computes `FNV-1a-64` of `argv[1]` (`offset basis 0xcbf29ce484222325`, `prime 0x100000001b3`) and compares the digest against a value materialised through a GOT slot. A mismatch prints `archive sealed. supplied token does not match.` and exits. The archive is never touched, which is why the program is silent when run normally.
2. Two constant blocks are then copied out of `.rodata` with `movups`: 128 bytes of "archive" at `0x5480` and a 24-byte, NUL-terminated key at `0x5500`.
3. The key is fed through the same FNV-1a-64 routine to produce a 64-bit seed.
4. That seed drives an LCG with PCG32 constants:

```text
state = seed
state = state * 0x5851f42d4c957f2d + 0x14057b7ef767814f   (mod 2^64)
keystream_byte = (state >> 33) & 0xff
```

   The compiler has vectorised the generator, then XORs 128 archive bytes against the 128 keystream bytes with SSE (`xorps` on 16-byte lanes) plus a scalar tail.
5. The result is scanned for the first `0x00` (the `str::from_utf8`/C-string length search at `0x16120`), and that slice is handed to `miniz_oxide`.

The last step is a decoy: decrypting the 128 bytes in Python with the reimplemented seed and LCG immediately yields printable ASCII beginning with `POCTF{`, so no decompression is required and the buffer already is the plaintext the utility was supposed to print.

The plaintext, and therefore the flag, is ████████████████.