# section31

| | |
|---|---|
| **Section** | OliCyber 2024 Selezione Territoriale |
| **Category** | pwn |
| **Solves** | 328 |

## Overview

Running `readelf -a` on the binary reveals the flag hidden character by character in the section headers, named `flag_0_f`, `flag_1_l`, `flag_2_a`, etc. Just read the third field of each `flag_*` section name in order.

## Solve

The flag can be read manually from the section names or extracted directly with:

```bash
readelf -W -S section31 | grep "flag_" | awk '{print $2}' | cut -d'_' -f3 | tr -d '\n' && echo
```