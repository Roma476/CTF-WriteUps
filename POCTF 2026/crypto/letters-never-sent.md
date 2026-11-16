# Letters Never Sent

| | |
|---|---|
| **Section** | wave 1 |
| **Category** | crypto |
| **Solves** | 876 |

## Overview

The challenge gives us a letter and a message recovered with it:

```
GMAHI{2.1814.TQPCOJ5THOKCT6HM.FWDJZEANBQV7AO57ATESOZZIYD}
```

The letter is mostly atmosphere, but it contains exactly two useful facts. It is addressed to *Admiral Sir Francis Beaufort, Hydrographer to the Navy*, and the body praises "that reciprocal tableau which bears your name". That is the cipher, named after the same man: **Beaufort**. "Reciprocal" is the property that defines it — encryption and decryption are the same operation:

```
P = (K - C) mod 26
```

The other hint is the border of the letter. It is a frame of Victorian plant and object names — Rose, Violet, Snowdrop, Anchor, Tulip, Poppy, Carnation, Harp, Willow, Marigold, Dove, Oak, Narcissus, Fern, Lily — and a handful of them are marked with a small star. Reading those labels clockwise from the first one, the initials spell:

```
V A C A N T
```

Which is the key. Two things make the reading unambiguous: there are six starred labels and six letters, and the repeated `A` is matched by the two starred *Anchor* entries, one on the top edge and one on the bottom.

The ciphertext itself confirms that digits and separators are left in the clear: the `2.1814.` block survives untouched.

## Solve

The key is checked against the prefix. With `VACANT` and the Beaufort relation:

| Ciphertext | G | M | A | H | I |
|---|---|---|---|---|---|
| Key | V | A | C | A | N |
| Plaintext | P | O | C | T | F |

`K - C` gives `P O C T F` for the first five letters, which is the flag prefix and a confirmation that the key and the direction of the subtraction are both right. Using plain Vigenère (`C - K`) instead gives `LKNYZ`, so the letter is not just decoration: it picks the variant.

One alignment detail costs more time than the cipher itself. The key stream runs over the **whole** string, including the `GMAHI`/`POCTF` prefix, and only letters advance it — digits and punctuation are passed through without consuming a key character. After the five letters of `GMAHI` the key is already at its sixth letter, so the first character after the opening brace is aligned with `T`, not with `V`. Restarting the key at the brace produces garbage from the first byte.

```python
ct  = "GMAHI{2.1814.TQPCOJ5THOKCT6HM.FWDJZEANBQV7AO57ATESOZZIYD}"
key = "VACANT"

out, i = [], 0
for ch in ct:
    if ch.isalpha():
        k = ord(key[i % len(key)]) - ord("A")
        out.append(chr((k - (ord(ch) - ord("A"))) % 26 + ord("A")))
        i += 1
    else:
        out.append(ch)

print("".join(out))
```

Running the script prints the flag:

```
POCTF{2.1814.████████████████.██████████████████████████}
```

The first word of the body, `AFLAME`, is a useful sanity check: a wrong key or a one-off alignment would never produce an English word at that position.