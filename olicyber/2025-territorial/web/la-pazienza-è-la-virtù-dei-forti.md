# La pazienza è la virtù dei forti

| | |
|---|---|
| **Section** |OliCyber 2025 Selezione Territoriale |
| **Category** | web |
| **Solves** | 617 |

## Overview

The application suggests the flag will be available in the future (2031), implying a time-based restriction.

## Solve

Inspecting browser cookies reveals a value controlling the access time:

```
Get-Flag-Time
```

By modifying this cookie to:

```
Get-Flag-Time=1
```

and refreshing the page, the server-side check is bypassed and the flag is returned immediately.