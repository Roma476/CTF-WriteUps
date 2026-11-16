# The Consulting Room

| | |
|---|---|
| **Section** | wave 3 |
| **Category** | crypto |
| **Solves** | 296 |

## Overview

The challenge exposes an encrypted medical record and a compliance endpoint that only reports whether a candidate record has valid PKCS#7 padding. That is a padding oracle. The record is AES-CBC, so the oracle is enough to recover the plaintext block by block without the key.

## Solve

The page provides a per-team Bearer token, a hex-encoded record, and the endpoint:

```text
POST https://pointeroverflowctf.com/challenges/consulting-room/oracle
Authorization: Bearer ████████████████
Content-Type: application/json

{"record": "<hex>"}
```

A valid padding returns `{"padding":"valid"}`; an invalid one returns HTTP 400 with `{"padding":"invalid"}`. The record is five AES blocks: one IV and four ciphertext blocks.

For a ciphertext block `C_i`, the plaintext is `P_i = D(C_i) XOR C_{i-1}`. The oracle tests the padding of `D(C_i) XOR X`, where `X` is the block we control. Decrypt the last byte first. For padding value `p`, set the already-known suffix to `I_j XOR p`, where `I = D(C_i)`, and try all 256 values for the current byte. When the oracle accepts, the candidate is `I_pos XOR p`. For `p = 1`, a false positive is possible when the real plaintext already ends in more than one padding byte, so flip an earlier byte and require the oracle to reject the modified record.

```python
import json, urllib.request

URL = "https://pointeroverflowctf.com/challenges/consulting-room/oracle"
TOKEN = "..."  # per-team Bearer token from the page

def oracle(prev, block):
    req = urllib.request.Request(
        URL,
        data=json.dumps({"record": (prev + block).hex()}).encode(),
    )
    req.add_header("Authorization", "Bearer " + TOKEN)
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read())["padding"] == "valid"
    except urllib.error.HTTPError as e:
        return json.loads(e.read())["padding"] == "invalid"

def decrypt_block(prev, block):
    inter = [0] * 16
    for pad in range(1, 17):
        pos = 16 - pad
        for guess in range(256):
            probe = bytearray(prev)
            for j in range(pos + 1, 16):
                probe[j] = inter[j] ^ pad
            probe[pos] = guess ^ pad
            if oracle(bytes(probe), block):
                if pad == 1:
                    check = bytearray(probe)
                    check[pos - 1] ^= 0xff
                    if not oracle(bytes(check), block):
                        continue
                inter[pos] = guess
                break
    return bytes(inter[i] ^ prev[i] for i in range(16))
```

Run it for blocks 1 through 4, concatenate, and strip the PKCS#7 padding. The recovered plaintext is 64 bytes: the 58-byte flag followed by six `0x06` padding bytes.

```text
████████████████
```

The recovered record is the flag ████████████████.