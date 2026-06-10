# Guess the Flag!

| | |
|---|---|
| **Section** | OliCyber 2024 Competizione Nazionale |
| **Category** | web |
| **Solves** | 352 |

## Overview

The page asks the user to guess the flag through an input field. The validation logic is triggered when clicking the **Guess** button.

Inspecting the source code reveals a heavily obfuscated JavaScript snippet in JSFuck.

## Solve

The JSFuck code can be deobfuscated using an online JSFuck decoder, revealing the validation function:

```javascript
() => {
    if (flag.value === "flag{...}") {
        win()
    } else {
        loose()
    }
}
```

The decoded string contains the correct flag value, which is required to pass the check.