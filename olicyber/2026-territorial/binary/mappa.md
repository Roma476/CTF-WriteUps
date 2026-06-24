# mappa
| | |
|---|---|
| **Section** | OliCyber 2026 Selezione Territoriale |
| **Category** | binary |
| **Solves** | 54 |
## Overview
The binary asks the user to insert a flag and prints `Sbagliato!` or `Corretto!` depending on the result. Running it normally with a random guess just returns `Sbagliato!`, with no other visible behavior.

Running `strings` on the binary reveals three suspicious symbols:
```
edge_from
edge_label
edge_to
```
Checking the `.symtab` confirms these are global objects, each **36 bytes long**, all defined inside `mappa.c`. The binary's name ("mappa", Italian for "map") together with these three same-length arrays strongly suggests a graph: for each edge `i` there would be a source node (`edge_from[i]`), a destination node (`edge_to[i]`) and a label (`edge_label[i]`) — the classic adjacency-list-as-three-parallel-arrays representation.

`strings` also reveals this 36-character string, which is clearly `edge_label` since it contains flag-like characters (`{`, `}`, `_`) but scrambled:
```
c1}40yw{gu_ylt9r0ud_h7a1gf_bnhr702f_
```
`ltrace`/`strace` show no custom comparison function being called on the input — only `strcspn` to strip the trailing newline. This means the "real" logic must be static, built entirely from data already in the binary, rather than computed at runtime from the user input.

## Solve
To read the actual content of the three arrays, dump the `.rodata` section:
```bash
objdump -s -j .rodata mappa
```
Each array is 36 bytes, and since `edge_from`/`edge_to` are declared as plain byte arrays (not 4-byte ints — confirmed by their size of 36 in the symtab, matching 36 elements of 1 byte each), every byte is read as a single index value:
```
edge_from = 1f 06 23 10 16 11 0f 04 18 0c 12 0a 01 13 21 0d
            0b 17 08 09 19 22 02 1e 03 00 0e 20 07 14 15 1b
            1c 1d 05 1a

edge_label = c1}40yw{gu_ylt9r0ud_h7a1gf_bnhr702f_

edge_to   = 20 07 24 11 17 12 10 05 19 0d 13 0b 02 14 22 0e
            0c 18 09 0a 1a 23 03 1f 04 01 0f 21 08 15 16 1c
            1d 1e 06 1b
```
Indices go up to `0x24` = 36, so the graph has 37 nodes (0 to 36) for 36 edges — one edge short of a full cycle, consistent with a simple path rather than a cyclic or branching graph.

Comparing `edge_from[i]` and `edge_to[i]` element by element (e.g. `0x1f → 0x20`, `0x06 → 0x07`, `0x23 → 0x24`, ...) shows that it always holds:
```
edge_to[i] = edge_from[i] + 1
```
This means every edge simply connects node `k` to node `k+1`, for every `k` from 0 to 35. There are no branches and no actual choice of path: the "graph" collapses into a single straight line 0 → 1 → 2 → ... → 36. In other words, `edge_from`/`edge_to` don't encode any real graph logic — they only encode, for each character of `edge_label`, **which position in the final string it belongs to**. This is just a permutation table, used to scramble the flag inside the binary so it wouldn't appear in plain, readable form under a simple `strings`.

Since `edge_from[i]` is the position of node `k` (the start of edge `i`, before stepping to `k+1`), and the flag is built by walking the chain from node 0 onward, the character carried by the edge starting at position `k` must be the `k`-th character of the flag. So the correct position of `edge_label[i]` in the final string is exactly `edge_from[i]`.

Rebuilding the flag is then just a matter of reordering `edge_label[i]` into the array position given by `edge_from[i]`:
```python
edge_from = [0x1f,0x06,0x23,0x10,0x16,0x11,0x0f,0x04,0x18,0x0c,0x12,0x0a,0x01,0x13,0x21,0x0d,
             0x0b,0x17,0x08,0x09,0x19,0x22,0x02,0x1e,0x03,0x00,0x0e,0x20,0x07,0x14,0x15,0x1b,
             0x1c,0x1d,0x05,0x1a]
label = 'c1}40yw{gu_ylt9r0ud_h7a1gf_bnhr702f_'

n = len(label)
result = [''] * n
for i in range(n):
    result[edge_from[i]] = label[i]

print(''.join(result))
```