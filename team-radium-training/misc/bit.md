# BIT

| | |
|---|---|
| **Section** | 4B INF CTFs |
| **Category** | misc |
| **Solves** | 3 |

## Overview

The challenge is a single string of digits with no prompt and no file:

0120212021201203120410120213014012012013031206120130101501203120130210214021010106120130212051501

Two counts give the first hint. The string contains exactly thirty `0`s and thirty `1`s, and deleting every digit from `2` to `6` leaves nothing but `0101…01`, sixty characters long. So the `0`s and `1`s are not data on their own — they are **markers**, and everything between two consecutive markers is a **length**.

Consecutive runs alternate bit value, starting with `0`: markers `0`, `1`, `0`, `1`, … The digits `2`–`6` sitting between two markers are the length of the run, and an empty gap (two markers back to back) is a run of length `1`.

The trap is the tail. After the very last `1` there is nothing left, and that empty remainder is still a valid final run. Dropping it produces 127 bits instead of 128, so the plaintext comes out truncated.

## Solve

Read the string as alternating runs, using the digits as counts:

gap   ''   2   2   2   2   2   ''  2   3   2   4   ''  ...
bit    0   1   0   1   0   1   0   1   0   1   0   1   ...
run   0   11  00  11  00  11   0  11  000 11 0000  1   ...

Sixty markers therefore produce sixty runs, which is exactly 128 bits — sixteen bytes of ASCII. This is enough to read the whole message out byte by byte.

```python
s = "0120212021201203120410120213014012012013031206120130101501203120130210214021010106120130212051501"

marks = [i for i, c in enumerate(s) if c in "01"]         

gaps = [s[marks[i] + 1:marks[i + 1]] for i in range(len(marks) - 1)]
gaps.append(s[marks[-1] + 1:])                           

bits = ""
for i, g in enumerate(gaps):
    bits += str(i % 2) * (1 if g == "" else int(g))        

assert len(bits) == 128
print(bytes(int(bits[i:i + 8], 2) for i in range(0, len(bits), 8)).decode())
```

The script prints the flag directly, confirming that the trailing implicit run was needed: without it the assertion fails at 127 bits.