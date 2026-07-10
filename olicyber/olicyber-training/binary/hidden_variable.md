# Hidden Variable

| | |
|---|---|
| **Section** | Software Security |
| **Category** | binary |
| **Solves** | 1127 |

## Overview

The binary exposes a global variable named `fl4g` inside the ELF `.data` section.

Using symbol inspection, the variable is located without needing runtime interaction:

```bash
readelf -s hidden_variable | grep fl4g
```

The symbol points to a memory region where the flag is stored in a non-standard layout.

## Solve

The flag is reconstructed directly from the ELF using pwntools:

```python
from pwn import *

elf = ELF("./hidden_variable")

data = elf.read(elf.symbols["fl4g"], 200)
flag = data[::4].decode()
print(flag)
```