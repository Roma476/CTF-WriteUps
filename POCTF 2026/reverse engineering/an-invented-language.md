# An Invented Language

| | |
|---|---|
| **Section** | wave 4 |
| **Category** | reverse engineering |
| **Solves** | 256 |

## Overview

The archive contains `prog.bin` for an undocumented stack-based VM and `vm.c`, its reference interpreter.

## Solve

`vm.c` defines the complete instruction set: `0x01` push imm32, `0x02` pop, `0x03` dup, `0x04` swap, `0x05` add, `0x06` sub, `0x07` xor, `0x08` and, `0x09` rotate byte, `0x0a` load, `0x0b` store, `0x0c` print, `0x0d` halt.

The reference VM produces no output. A Python interpreter for the same ISA shows that the program pushes immediate pairs, XORs them, and stores 59 bytes into `m[0..58]`; it never reaches a print instruction. Dumping the final memory reveals the flag.

The submitted flag was POCTF{123.1814.████████████████.████████████████} and it was accepted.
