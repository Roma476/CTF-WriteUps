# Conditional Existence

| | |
|---|---|
| **Section** | wave 5 |
| **Category** | misc |
| **Solves** | 163 |

## Overview

The per-team archive contains a small C program and its source. Without the required environment variable the program prints only `.`. The source checks `POCTF_INCANTATION`: it must be exactly 12 uppercase hexadecimal characters. That value is used as a repeating XOR key over an embedded ciphertext, and the program verifies the SHA-256 of the decrypted plaintext against an embedded digest. The source also contains a four-part riddle whose answers produce the incantation.

## Solve

The four riddle answers are:

- the year Helena P. Blavatsky died in London: `1891`;
- the surname of the London paranormal investigator who ran the National Laboratory of Psychical Research and investigated Borley Rectory: `price`;
- the Indian suburb where the Theosophical Society moved its international headquarters in 1882: `adyar`;
- the one-word name of the Enochian scryer who recorded the angelic communications with John Dee: `kelley`.

The phrase is therefore `1891 price adyar kelley`. Concatenating the answers with single spaces, hashing the UTF-8 bytes with SHA-256, and taking the first 12 uppercase hexadecimal characters gives the required incantation.

```python
import hashlib

phrase = "1891 price adyar kelley"
incantation = hashlib.sha256(phrase.encode()).hexdigest()[:12].upper()
print(incantation)
```

Running the supplied program with that value in `POCTF_INCANTATION` decrypts the ciphertext, satisfies the embedded hash check, and prints the flag.

The flag is ████████████████.