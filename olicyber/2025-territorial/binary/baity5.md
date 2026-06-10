# Baity5

| | |
|---|---|
| **Section** | OliCyber 2025 Selezione Territoriale |
| **Category** | binary |
| **Solves** | 211 |

## Overview

The provided ELF does not produce any visible output when executed.

Inspecting the binary with `strings` reveals a long encoded payload:

```
Ao(mgHYtQJARB^:F^J`7F`(_sD)5Nj?X[eY1gaj2@:rqYDIYA2ARo.^DI5_=BlnVX?Y)&JAnEtX215
```

## Solve

The extracted string is Base85-encoded data.

```python
import base64

enc = b"Ao(mgHYtQJARB^:F^J`7F`(_sD)5Nj?X[eY1gaj2@:rqYDIYA2ARo.^DI5_=BlnVX?Y)&JAnEtX215"
print(base64.a85decode(enc).decode())
```

The decoded output corresponds to the flag.