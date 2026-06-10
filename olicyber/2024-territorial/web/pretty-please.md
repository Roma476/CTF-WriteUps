# Pretty please

| | |
|---|---|
| **Section** | OliCyber 2024 Selezione Territoriale |
| **Category** | web |
| **Solves** | 889 |

## Overview

The page submits a POST parameter named `how` with one of the values exposed in a dropdown menu. A `Show source` link is also available.

## Solve

The source code reveals an additional valid value not present in the UI:

```
pretty please
```

Submitting it manually:

```bash
curl -X POST -d "how=pretty please" http://prettyplease.challs.olicyber.it/
```

returns the flag.