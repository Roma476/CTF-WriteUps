# MIC

| | |
|---|---|
| **Section** | OliCyber 2024 Competizione Nazionale |
| **Category** | binary |
| **Solves** | 90 |

## Overview

```
$ checksec --file=MIC
Arch:      amd64-64-little
RELRO:     Full RELRO
Canary:    Canary found
NX:        NX enabled
PIE:       PIE enabled
SHSTK:     Enabled
```

The binary asks for an unlock key of exactly 36 bytes (checked with `strlen`), then calls `check_key`. If the check passes, `main` decrypts a hidden message by XORing a global buffer (`flag`) with the key, and prints it with `puts`.

After analyzing the binary with Ghidra, the interesting functions are:

- `format_key`: copies the 36 bytes of the input into a global 6x6 matrix called `grille`.
- `check_key`: implements a Cardan grille. It repeats 4 times (one for each 90° rotation of the matrix), and at each round it reads 9 characters from the grid at the positions given by the pairs (row, column) stored in the global array `secret`. The 4 x 9 = 36 characters collected this way are compared with the constant array `encrypted_key` using `strncmp`.

## Solve

The first idea was to patch `check_key` to always return 1, so that any 36-byte string would be accepted. This does not work: the XOR uses the correct key, so with a fake one the output is just unreadable bytes, and `puts` stops at the first null byte.

The key has to be the real one, and it can be recovered offline. `encrypted_key` is not the input, but what the grille extracts from the input after the 4 rotations. Since the extraction positions (`secret`) and the rotations are known, the process can be inverted: every byte of `encrypted_key` is put back in the cell of the 6x6 grid it was read from, and reading the grid row by row gives the 36 bytes of the original key. XORing this key with the `flag` buffer decrypts the message.

The script reads `encrypted_key`, `secret` and `flag` directly from the ELF with pwntools:

```python
from pwn import *

elf = ELF('./MIC')
encrypted_key = elf.read(elf.symbols['encrypted_key'], 36)
secret = elf.read(elf.symbols['secret'], 18) 
flag_raw = elf.read(elf.symbols['flag'], 36)

grid_indices = [[r * 6 + c for c in range(6)] for r in range(6)]

def rotate_grid(g):
    return [[g[5 - c][r] for c in range(6)] for r in range(6)]

input_grid = [[None for _ in range(6)] for _ in range(6)]
curr_grid = grid_indices
idx = 0

for rot in range(4):
    for i in range(9):
        r = secret[i * 2]
        c = secret[i * 2 + 1]
        orig_cell_flat = curr_grid[r][c]
        orig_r = orig_cell_flat // 6
        orig_c = orig_cell_flat % 6
        input_grid[orig_r][orig_c] = encrypted_key[idx]
        idx += 1
    curr_grid = rotate_grid(curr_grid)

correct_key = bytearray(36)
for r in range(6):
    for c in range(6):
        correct_key[r * 6 + c] = input_grid[r][c]

decrypted_flag = bytes([f ^ k for f, k in zip(flag_raw, correct_key)])
print(decrypted_flag.decode('latin1'))
```

Running the script prints the flag.