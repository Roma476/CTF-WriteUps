# Commit to Memory

| | |
|---|---|
| **Section** | wave 2 |
| **Category** | steganography |
| **Solves** | 376 |

## Overview

A git bundle was exported from a researcher's side project. The clone is a linear 60-commit history with two files, `README.md` and `CHANGELOG.md`. `git grep`, `grep -r`, and `strings` over every blob return nothing. The flag is not in the working tree or in any blob. It is in the commit timestamps.

## Solve

`git log --reverse --format='%H %at %s' origin/main` shows that every commit has identical author and committer timestamps, increasing monotonically. The subjects and file diffs are cover. The intervals between consecutive author timestamps are printable ASCII:

```text
80 79 67 84 70 123 49 48 48 46 ...
 P  O  C  T  F  {  1  0  0  . ...
```

The first commit is the baseline; each later commit advances the clock by the ASCII value of the next flag character. There are 60 commits and 59 deltas, matching a 59-character flag.

Minimal extraction:

```python
import subprocess

ts = [int(x) for x in subprocess.check_output(
    ["git", "log", "--reverse", "--format=%at", "origin/main"],
    text=True,
).split()]

print("".join(chr(b - a) for a, b in zip(ts, ts[1:])))
```

Output:

```text
POCTF{100.1814.████████████████████████████████████████}
```

The repeated early-message block in the log is cover; it does not affect the timestamp channel. The recovered flag is `POCTF{████…}`.