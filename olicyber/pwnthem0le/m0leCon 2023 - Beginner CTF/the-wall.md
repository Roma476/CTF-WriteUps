# The Wall
| | |
|---|---|
| **Section** | m0leCon 2023 Beginner CTF |
| **Category** | binary |
| **Solves** | 120 |

## Overview
After analyzing the binary with Ghidra, the flag is read into `notaflagbuffer` at offset `0x14` for `100` bytes, right up to the end of a `0x78`-byte buffer that was previously zeroed with `memset`. Since `0x14 + 100 == 0x78`, the flag data fills the buffer exactly to its end, leaving no room for a null terminator after it.

The "Write note" option reads user input into the start of the same buffer with `read(0, notaflagbuffer, 0x1000)`. There's a check that calls `empty_stdin()` if exactly `0x14` (20) bytes are sent without a trailing newline, but this check doesn't stop the write and doesn't add a terminator either — it only drains any queued extra input.

The "Read note" option prints the buffer with `printf("%s", notaflagbuffer)`, which reads until it hits a null byte. If we fill the first 20 bytes without ever writing a `\0`, `printf` won't stop there: it keeps reading straight through into the adjacent memory where the flag was stored, leaking it entirely.

## Solve
Write exactly 20 bytes with no newline to the note, then read it back — `printf` overruns into the flag region right after our input:

```python
from pwn import *

chall = remote('thewall.challs.olicyber.it', 21007)

chall.sendlineafter(b'Choose an option: ', b'1')
chall.sendafter(b'Share some thoughts: ', b'A' * 20)  

chall.sendlineafter(b'Choose an option: ', b'2')

print(chall.recvall(timeout=2).decode(errors='replace'))
```