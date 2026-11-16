# Columns of Holes

| | |
|---|---|
| **Section** | wave 3 |
| **Category** | misc |
| **Solves** | 261 |

## Overview

The handout is a batch-operations memorandum from "Meridian Data Processing Services" with two enclosed 80-column job tickets, suffixes A and B. The memo states that a 16-character nonce is interleaved through each ticket's payload region at a stride given by the card's `PAT` marker, and that the fragments must be combined in the alphabetical order of the suffixes (A, then B). The printed human-readable row at the top of each card is described as damaged, so the information has to be recovered from the punched columns themselves.

## Solve

The two cards are embedded as 1600×640 images on page 2 of the PDF (xrefs 6 and 8). Thresholding the images and extracting connected components isolates the punched holes (roughly 27×12 px ellipses) from the printed glyphs (roughly 8×5 px). The holes fall on a regular lattice:

- 12 hole rows at y ≈ 111, 153.5, 196.5, 239, 281, 323.5, 366.5, 409, 451, 493.5, 536.5, 579 — these are the standard rows `12, 11, 0, 1, …, 9`;
- 80 hole columns starting at x ≈ 59.5 with a pitch of ≈ 19 px.

Reading the punch sets in Hollerith code (single punch `0`–`9` = digit; zone `12` + digit = `A`–`I`; zone `11` + digit = `J`–`R`; zone `0` + digit = `S`–`Z`; `8,3` = `=`, `0,1` = `/`) recovers both card decks:

```
CARD A: JOB=1814A   PID1819801/05/67OP?TQW59PAT=54  <36-char payload>
CARD B: JOB=1814B   PID2986325/07/67OP?KAR32PAT=23  <36-char payload>
```

The payload region begins at column 44; the `PAT` value is the two-digit `(offset, stride)` pair used to sample it. For card A the pair `(5, 4)` selects eight positions, and for card B `(2, 3)` selects eight positions; these are the choices that make every extracted character a hexadecimal digit. Each card therefore contributes an eight-character fragment.

Concatenating the fragments in suffix order — A first, then B — yields the 16-hex nonce.

The 16-hex nonce is `████████████████`.