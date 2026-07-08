# how lucky you are

| | |
|---|---|
| **Section** | m0leCon 2021 Beginner CTF |
| **Category** | binary |
| **Solves** | 181 |

## Overview

After analyzing the binary with Ghidra, `generateRandomNumber()` calls `rand()` without a prior `srand()`, so the seed defaults to 1 and the output is always deterministic. The `main` compares the generated number against user input and opens `flag.txt` if they match.

## Solve

Set a breakpoint on `generateRandomNumber`, let it run to completion and read the return value from `$eax`:

```
$ gdb ./random
(gdb) break generateRandomNumber
(gdb) run
(gdb) finish
(gdb) print/d $eax
$1 = 1804289383
```

Since there's no `srand()`, the value is static across every execution — no need to rerun. Send it to the remote:

```
$ nc lucky.challs.olicyber.it 17000
Insert your key: 1804289383
```