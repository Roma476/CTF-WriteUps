# Byte-flag

| | |
|---|---|
| **Section** | Miscellaneous |
| **Category** | misc |
| **Solves** | 2600 |

## Overview

The challenge provides a single PNG image attachment:

```
flag.png
```

## Solve

Inspecting the file contents directly reveals that additional data has been appended after the end of the PNG image.

A simple:

```bash
cat flag.png
```

shows the PNG data followed by the flag appended at the end of the file.