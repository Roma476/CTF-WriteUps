# Frasi basate

| | |
|---|---|
| **Section** | OliCyber 2023 Selezione Territoriale |
| **Category** | binary |
| **Solves** | 665 |

## Overview

The challenge provides a Linux ELF executable and asks us to recover some "based phrases" hidden inside it.

Running the binary does not reveal anything useful, so a quick static inspection with `strings` is enough:

```bash
strings based
```

Among the extracted strings there is a suspiciously long Base64-encoded value:

```text
Qm9pYSBkZWgsIGxhIGZsYWcgaW4gYjY0LCBpbnRyb3ZhYmlsZSwgYXNzb2x1dGFtZW50ZSBmbGFne3N0cjFuZ2gzX2ludXQxbDFfZV9kMHYzX3RyMHY0cmwzXzNiM2RhNDYzY2NhZTNhOTVmODMxfQ==
```

## Solve

The long string found with `strings` is Base64 encoded.

A small Python script can be used to decode it:

```python
import base64

enc = "Qm9pYSBkZWgsIGxhIGZsYWcgaW4gYjY0LCBpbnRyb3ZhYmlsZSwgYXNzb2x1dGFtZW50ZSBmbGFne3N0cjFuZ2gzX2ludXQxbDFfZV9kMHYzX3RyMHY0cmwzXzNiM2RhNDYzY2NhZTNhOTVmODMxfQ=="

print(base64.b64decode(enc).decode())
```

Executing the script reveals a message containing the flag.