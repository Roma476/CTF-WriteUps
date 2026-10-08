# X0rland1a

| | |
|---|---|
| **Section** | HighSchools CTF Workshop - 2023 Bari |
| **Category** | crypto |
| **Solves** | 267 |

## Overview

The challenge welcomes us to "the magical world of XOR" and gives us a website (`http://xorlandia.challs.olicyber.it`). The page, called X0rland1a, has four fields:

- **Testo da xorare (Hex)**: the input text, in hexadecimal, already filled in with a long hex string (the encrypted flag)
- **Chiave (ASCII)**: the key, to be typed by us
- **Risultato (ASCII)**: the result of the XOR, as text
- **Risultato (Hex)**: the result of the XOR, in hexadecimal

With an empty key nothing happens, so we need to find the right key to decrypt the flag.

## Solve

The key is not given, but we know the format of the flags: they all start with `ITASEC{`. Since XOR is its own inverse (if `a ^ b = c`, then `c ^ b = a`), XORing the ciphertext with a known piece of plaintext reveals the part of the key used on that piece. This is a known-plaintext attack.

So I typed `ITASEC{` as the key. The result is mostly garbage, but its first characters are readable:

```
gabibbo...
```

Those characters are the first bytes of the key (the key repeats along the message, so it only shows up cleanly where our guess matches the real plaintext). Adding the `{` at the end of the guess gives the next character, and the whole key can be read as `gabibbo`.

Typing `gabibbo` as the key, the result field now shows the decrypted text, which is the flag.