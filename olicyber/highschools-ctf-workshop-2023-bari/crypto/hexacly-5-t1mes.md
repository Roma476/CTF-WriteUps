# HEXacly 5 t1mes

| | |
|---|---|
| **Section** | HighSchools CTF Workshop - 2023 Bari |
| **Category** | crypto |
| **Solves** | 400 |

## Overview

The challenge describes encoding as a system of signals or symbols conventionally designated to represent information, and recommends using [CyberChef](https://gchq.github.io/CyberChef/). It gives us an encoded flag:

```text
VmtkMFUyTnJNVlpPVlZaV1YwZG9VRlpyVlhka01WSnpWV3hLYkdGNlVqVlZNVkpQVkRGS1JrMVVUbFZYU0VKRFZGWmFkMk5XWkhSa1JUVnNZa1ZXTlZZeWVGTldhelZXVGxab1dGZElRazlhVjNoM1l6RlNkR05GTlU1aVNFSjRWakZTUTFSdFZuSldXR3hZWWtaS1lWUlVRWGhPYkZwWllrVTFWMUl4U25rPQ==
```

The ciphertext is clearly base64, given the character set and the `==` padding at the end. The title, "HEXacly 5 t1mes", is a hint on how it was built: base64 applied 5 times, followed by something related to hex.

## Solve

Following the hint, I decoded the string from base64 5 times in a row:

```
$ echo "<ciphertext>" | base64 -d | base64 -d | base64 -d | base64 -d | base64 -d
```

The result is not readable text yet, but a string made only of hexadecimal digits. This is the "HEX" part of the title, so one last step is needed: decoding the hex string into bytes with `xxd`.

```
$ echo "<hex string>" | xxd -r -p
```

This gives the flag.

Alternatively, the whole process can be done in a single step with CyberChef: pasting the ciphertext in the input and using the "Magic" operation, which detects the chain of encodings automatically and returns the flag directly.