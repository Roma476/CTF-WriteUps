# Binario Sus

| | |
|---|---|
| **Section** | Binary |
| **Category** | binary |
| **Solves** | 8 |

## Overview

The binary prints `Miao, non avrai la flag` as a decoy. The actual flag is hidden in `.rodata`, the `main` constructs it on the stack by reading individual bytes via a series of `lea` + `mov %al` instructions, but never prints it.

## Solve

Dump the `.rodata` section:

```bash
objdump -s -j .rodata miao
```

```
0x2000: 01000200 6c006100 67007b00 68006500
0x2010: 6f007d00 4d69616f 2c206e6f 6e206176
```

The `main` disassembly reads bytes in this order:

```asm
lea    0xe73(%rip),%rax   # 0x2004 → 'l'
lea    0xe6b(%rip),%rax   # 0x2006 → 'a'
lea    0xe63(%rip),%rax   # 0x2008 → 'g'
lea    0xe5b(%rip),%rax   # 0x200a → '{'
lea    0xe53(%rip),%rax   # 0x200c → 'h'
lea    0xe4b(%rip),%rax   # 0x200e → 'e'
lea    0xe37(%rip),%rax   # 0x2004 → 'l'
lea    0xe2d(%rip),%rax   # 0x2004 → 'l'
lea    0xe2f(%rip),%rax   # 0x2010 → 'o'
lea    0xe27(%rip),%rax   # 0x2012 → '}'
```

The final `lea` (offset `0x2014`) moves the pointer into `%rdi` and calls `printf` — pointing to `Miao, non avrai la flag`. The flag assembled on the stack is never printed, serving as a second layer of misdirection.

Reconstructing the bytes from `.rodata` in the order above yields the flag.