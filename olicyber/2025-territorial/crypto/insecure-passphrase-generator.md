# Insecure Passphrase Generator

| | |
|---|---|
| **Section** | OliCyber 2025 Selezione Territoriale |
| **Category** | crypto |
| **Solves** | 235 |

## Overview

The provided script generates a passphrase by mapping each lowercase character of the flag to a word list:

```python
words = [
    "casa", "albero", "notte", "sole", "montagna", "fiume", "mare", "vento", "nuvola",
    "pioggia", "strada", "amico", "sorriso", "viaggio", "tempo", "cuore", "stella",
    "sogno", "giorno", "libro", "porta", "luce", "ombra", "silenzio", "fiore", "luna"
]
```

Each letter `a-z` is encoded as `words[ord(c) - ord('a')]`, while non-alphabetic characters are kept unchanged.

## Solve

The encoding is reversed by building a lookup table from word → character and decoding each token:

```python
words = [
    "casa", "albero", "notte", "sole", "montagna", "fiume", "mare", "vento", "nuvola",
    "pioggia", "strada", "amico", "sorriso", "viaggio", "tempo", "cuore", "stella",
    "sogno", "giorno", "libro", "porta", "luce", "ombra", "silenzio", "fiore", "luna"
]

decode_map = {w: chr(i + ord('a')) for i, w in enumerate(words)}

encoded = "fiume-amico-casa-mare-{-amico-tempo-viaggio-mare-_-sole-tempo-montagna-giorno-viaggio-libro-_-sorriso-montagna-casa-viaggio-_-giorno-montagna-notte-porta-sogno-montagna-_-mare-fiume-strada-giorno-amico-vento-vento-mare-}"

parts = encoded.split('-')

decoded = []
for p in parts:
    if p in decode_map:
        decoded.append(decode_map[p])
    else:
        decoded.append(p)

print("".join(decoded))
```

The decoded string reconstructs the original flag.