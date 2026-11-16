# Excavation

| | |
|---|---|
| **Section** | wave 1 |
| **Category** | reverse engineering |
| **Solves** | 459 |

## Overview

Four save files from the fictional RPG "Sepulchure of the Undying" are provided. The challenge asks for a 16-character token rather than a normal flag.

## Solve

Each file begins with a 12-byte header: the 8-byte magic `9e e1 c7 21 02 00 02 00` followed by a 4-byte little-endian length. The payload is XORed with an 8-byte repeating key.

The plaintext is ASCII record data, so each key byte is recovered independently by scoring its decrypted column against a distribution of printable field-name and description bytes. The resulting key decrypts the save into item records, each with a length-prefixed name and description.

The first letters of the item names form an acrostic. The three reference saves spell `TORCH`, `SILVERMOON`, and `NIGHTENDSOON`, confirming the scheme; the team save has sixteen item names whose initials spell the token.

The submitted flag was `████████████████` and it was accepted.
