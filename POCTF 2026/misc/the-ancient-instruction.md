# The Ancient Instruction

| | |
|---|---|
| **Section** | wave 8 |
| **Category** | misc |
| **Solves** | 66 |

## Overview

The artifact is a Brainfuck program written with the eight trigrams `☰☱☲☳☴☵☶☷`. Brainfuck has exactly eight commands, so the puzzle is to recover the permutation that maps the trigrams to `><+-.,[]`. The program's first output is a short header naming the command alphabet, followed by the flag.

## Solve

Index the trigrams in the order `☰☱☲☳☴☵☶☷`, convert the artifact to an instruction stream, and try the 8! possible command permutations. The correct mapping is:

```text
☰ ☱ ☲ ☳ ☴ ☵ ☶ ☷
] < > - , . + [
```

A small interpreter is enough:

```python
symbols = "☰☱☲☳☴☵☶☷"
index = {c: i for i, c in enumerate(symbols)}
command = "]<>-,.+["

code = [command[index[c]] for c in open("program.txt", encoding="utf-8").read()
        if c in index]
```

Run the resulting Brainfuck program. It prints the command alphabet `+-><.,[]` as a self-check and then the flag. The accepted flag was `████████████████`.