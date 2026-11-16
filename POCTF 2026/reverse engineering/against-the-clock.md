# Against the Clock

| | |
|---|---|
| **Section** | wave 8 |
| **Category** | reverse engineering |
| **Solves** | 61 |

## Overview

`clock` is a stripped non-PIE x86-64 ELF. It calls `time()` twice, performs a short busy loop, and then derives a decryption key from the timestamp. The ciphertext is a 59-byte blob at file offset `0x2020`, and the key stream is SHA-256 in counter mode:

```text
SHA256(seed_le64 || 0x542947a8_le64 || counter_le32)
```

The first eight bytes of each block are XORed with the ciphertext. The seed is the current Unix time, unless the busy loop takes at least two seconds, in which case the seed is XORed with `0x5a17eddecade5a17`.

## Solve

The constant `0x542947a8` is both a domain separator and the target epoch. In decimal it is `1411983272`, i.e. 2014-09-29 11:51:04 UTC. The intended way to run the binary is therefore:

```bash
faketime "@1411983272" ./clock
```

Alternatively, replay the decryption in Python:

```python
import hashlib, struct

epoch = 0x542947a8
ct = open("clock", "rb").read()[0x2020:0x2020 + 0x3b]

stream = b""
for counter in range(3):
    stream += hashlib.sha256(
        struct.pack("<Q", epoch) +
        struct.pack("<Q", 0x542947a8) +
        struct.pack("<I", counter)
    ).digest()

plaintext = bytes(a ^ b for a, b in zip(ct, stream))
print(plaintext)
```

The 59-byte plaintext is the flag. The accepted flag was `████████████████`.