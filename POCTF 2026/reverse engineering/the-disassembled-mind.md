# The Disassembled Mind

| | |
|---|---|
| **Section** | wave 2 |
| **Category** | reverse engineering |
| **Solves** | 405 |

## Overview

The specimen is a Python 3.13 `.pyc`. The `check()` function contains five inline 59-byte constants; two are decoys and three XOR together into the flag.

## Solve

After the 16-byte header, `marshal` loads the module code object. The nested `check()` code object has five 59-byte `bytes` constants in `co_consts`. Testing all ten 3-element combinations and XORing each byte-wise, combination `(0, 2, 3)` yields a printable 59-byte string beginning with `POCTF{`; the other combinations do not. Constants 1 and 4 are the decoys.

The submitted flag was POCTF{117.1814.████████████████.████████████████} and it was accepted.
