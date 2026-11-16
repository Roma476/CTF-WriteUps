# What Goes Unwritten

| | |
|---|---|
| **Section** | wave 3 |
| **Category** | forensics |
| **Solves** | 313 |

## Overview

A public-library workstation was force-terminated during a Firefox session. The only artifact is a Windows minidump, `library-workstation-firefox.dmp`. The task is to recover the 16-character base32 session-restore token that Firefox held in memory but never wrote to disk.

The dump is a synthetic MDMP with four streams. The useful stream is `Memory64List` (type 9): 480 4K pages, all mapped at 4096-byte intervals. The token is not a contiguous 16-character string. It is split across two length-prefixed UTF-16LE records that meet at a page boundary. A direct `strings` search therefore finds plausible decoys but not the token.

## Solve

The stream directory is at RVA `0x20`. The fourth entry is the `Memory64List` stream at RVA `0x21c`, size `0x1e10`. Its first 16 bytes are:

- `uint64` range count = 480
- `uint64` data base RVA = `0x202c`

The descriptors follow at `0x22c`, 16 bytes each (`uint64 start`, `uint64 size`). The page data begins at file offset `0x202c` and is stored in descriptor order.

The records use the format:

```text
[uint32 total_len][uint32 magic][UTF-16LE string]
```

`total_len` includes the 8-byte header, so the string occupies `total_len - 8` bytes. Most records carry the decoy magic `de c0 ed 5d` and contain arbitrary Firefox-looking phrases; these dominate `strings -el`. Only two records use the real magic `ba b0 ad de`.

A minimal scanner over the `Memory64List` pages:

```python
import re, struct

b = open("library-workstation-firefox.dmp", "rb").read()
n, base = struct.unpack_from("<QQ", b, 0x21c)
magic = b"\xba\xb0\xad\xde"

for _ in range(n):
    start, size = struct.unpack_from("<QQ", b, 0x21c + 16 + _ * 16)
    page = b[base:base + size]
    base += size

    for m in re.finditer(re.escape(magic), page):
        length = struct.unpack_from("<I", page, m.start() - 4)[0]
        raw = page[m.start() + 4 : m.start() + length - 4]
        print(f"{start + m.start() - 4:#x} len={length:#x} "
              f"{raw.decode('utf-16le').rstrip(chr(0))!r}")
```

The scanner produces two hits:

```text
0x14100228fbe len=0x42 'sessionRestoreToken:YZRNXWAB'
0x14100229000 len=0x40 'ETEGUEP3|expires:1751659200'
```

The first record begins at `0x14100228fbe`, 66 bytes before the end of the page at `0x14100229000`. The second begins exactly at the next page. The virtual-address order is therefore unambiguous: the `sessionRestoreToken` value comes first, and the `expires` record follows it.

The first record supplies the eight characters after `sessionRestoreToken:`. The second supplies the eight characters before `|expires:`. Concatenating the two eight-character values in address order yields the 16-character token. Any search for a contiguous 16-character base32 string fails because the page boundary splits the value; `strings` also loses the record order and the length prefix.

The recovered token is `████████████████`.