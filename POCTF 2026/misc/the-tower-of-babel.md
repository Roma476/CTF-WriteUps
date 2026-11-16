# The Tower of Babel

| | |
|---|---|
| **Section** | wave 6 |
| **Category** | misc |
| **Solves** | 159 |

## Overview

`babel.txt` is a reference sheet plus a 399-character message drawn only from the seven letters `A E I O U X Y`. The sheet describes five operations — four base-N encodings keyed to the integer they represent, and one columnar transposition of width 7 — applied in an unspecified order. Only the character set at each stage tells you which operation produced it, so the peel is driven by inspection rather than by guessing the order.

The encodings are: base 3 (`0`,`1`,`2`), Bitcoin base 58 (58 alphanumerics without `0`, `I`, `O`, `l`), RFC 1924 base 85 (the variant whose alphabet contains `{`, `}`, `` ` ``, `<`, `>`), and base 7 over `A E I O U Y X` in that digit order. All four are big-integer conversions: the whole string is a numeral, so decoding means evaluating it as one integer and re-emitting the digits in the target base.

## Solve

The outermost layer announces itself immediately: only seven distinct characters, exactly the base-7 alphabet. Evaluating the message as a base-7 numeral and writing the integer as bytes yields 140 printable ASCII characters.

Those 140 characters use digits, letters, `|`, `` ` ``, `$`, `~`, `;`, `<`, `>` — a mix that fits RFC 1924 base 85 but not Ascii85 (which stops at `u`). Decoding is again a single big-integer conversion, not the 5-char-to-4-byte block form: the result is 112 characters that look like Bitcoin base 58, except for three `0` characters.

The `0` is the tell. Base 58 deliberately has no `0`, and the transposition is documented to pad the last row with `'0'` before reading columns. So the next layer is the transposition. Writing the 112 characters into a 16 × 7 grid column by column and reading the rows back gives the original string followed by `000`.

Stripping that padding leaves a 109-character base-58 numeral. Decoding it as a big integer yields 80 digits drawn from `0`, `1`, `2` — the ternary layer.

Base 3 with 80 digits is about 126 bits, which decodes to 16 bytes of ASCII, and those 16 hexadecimal characters are the nonce the reference sheet asked for.

The recovered nonce is ████████████████.