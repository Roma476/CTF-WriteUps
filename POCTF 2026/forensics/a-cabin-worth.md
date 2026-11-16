# A Cabin Worth

| | |
|---|---|
| **Section** | wave 2 |
| **Category** | forensics |
| **Solves** | 434 |

## Overview

A Joplin 2.14.20 Linux profile was imaged while the application was running. The main database is one 4 KiB page; the 156,592-byte `database.sqlite-wal` holds 38 frames of 4 KiB pages. The visible `notes` table contains four live notes and the `deleted_items` table contains one row, but the deleted note is no longer in the current notes page. The WAL still holds the pre-delete page image.

## Solve

The WAL header at offset 0 is:

```text
magic 0x377f0682  version 3007000  page_size 4096
salt1 0xdb84c003  salt2 0x87bc0766
```

Each frame is a 24-byte header followed by 4096 bytes of page data. The frame header is six big-endian uint32 values: page number, database size after commit (zero for non-commit frames), salt-1, salt-2, checksum-1, checksum-2. All 38 frames pass the WAL checksum. Frame 38 is the final commit and sets the database size to 16 pages.

After applying the WAL, the current `notes` table is page 4 with four rows. The `deleted_items` table is page 12:

```text
rowid 1: item_type=1  item_id=4b7c9e1f3a5b7c9e1f3a5b7c9e1f3a5b
         deleted_time=1751326272000 (2025-06-30 23:31:12 UTC)  sync_target=0
```

`sqlite_sequence` confirms one deletion. The deleted item ID is absent from the current notes page, but the WAL contains the last pre-delete version of page 4: frame 25. Frame 35 is the post-delete page 4. Parsing frame 25 as a table-leaf page yields five notes; the fifth is:

```text
id: 4b7c9e1f3a5b7c9e1f3a5b7c9e1f3a5b
parent_id: a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6  (Dissertation)
title: Delacroix — 06/28 confirmation
body: ""
encryption_cipher_text: 1772 base64 characters
encryption_applied: 1
```

The `settings` table supplies the encryption parameters:

```text
note.encryption.algorithm      AES-256-GCM
note.encryption.kdf            PBKDF2-HMAC-SHA256
note.encryption.kdf_iterations 200000
note.encryption.blob_layout    salt(16) || nonce(12) || ciphertext || tag(16), base64
note.password_hint             my good widdle boy!
```

The hint points at Horatio, the dog named in the live `shopping` note. The password is `horatio`.

The note blob decodes to a 16-byte salt, a 12-byte nonce, 1285 bytes of ciphertext, and a 16-byte GCM tag. Deriving a 32-byte key with PBKDF2-HMAC-SHA256 over `horatio` and the salt, then decrypting with AES-256-GCM, reveals the deleted note body. The plaintext contains the working flag.

A minimal extractor/decryptor:

```python
import base64, hashlib, struct
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

PAGE = 4096
WAL = open("database.sqlite-wal", "rb").read()

def varint(b, o):
    v = 0
    for i in range(8):
        c = b[o + i]
        v = (v << 7) | (c & 0x7f)
        if not c & 0x80:
            return v, o + i + 1
    return (v << 8) | b[o + 8], o + 9

def nbytes(t):
    if t == 0: return 0
    if 1 <= t <= 4: return t
    if t == 5: return 6
    if t == 6: return 8
    if t == 7: return 8
    if t in (8, 9): return 0
    return (t - 12) // 2 if t % 2 == 0 else (t - 13) // 2

def record(p):
    hl, o = varint(p, 0)
    types = []
    while o < hl:
        t, o = varint(p, o)
        types.append(t)
    o = hl
    out = []
    for t in types:
        n = nbytes(t)
        raw = p[o:o + n]
        o += n
        if t == 0:
            v = None
        elif t in (8, 9):
            v = t - 8
        elif t == 7:
            v = struct.unpack(">d", raw)[0]
        elif t >= 12:
            v = raw.decode() if t % 2 else raw
        else:
            v = int.from_bytes(raw, "big", signed=True)
        out.append(v)
    return out

# frame 25 = page 4, last pre-delete notes page
off = 32 + (25 - 1) * (24 + PAGE)
page = WAL[off + 24:off + 24 + PAGE]
nc = struct.unpack_from(">H", page, 3)[0]

for i in range(nc):
    ptr = struct.unpack_from(">H", page, 8 + 2 * i)[0]
    plen, o = varint(page, ptr)
    rowid, o = varint(page, o)
    row = record(page[o:o + plen])
    if row[0] == "4b7c9e1f3a5b7c9e1f3a5b7c9e1f3a5b":
        blob = base64.b64decode(row[21])
        salt, nonce, tag = blob[:16], blob[16:28], blob[-16:]
        key = hashlib.pbkdf2_hmac("sha256", b"horatio", salt, 200000, 32)
        print(AESGCM(key).decrypt(nonce, blob[28:-16] + tag, None).decode())
```

The recovered flag is `POCTF{████…}`.