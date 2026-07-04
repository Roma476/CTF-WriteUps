# trova_le_soluzioni
| | |
|---|---|
| **Section** | HighSchools CTF Workshop - 2023 Perugia |
| **Category** | web |
| **Solves** | 437 |

## Overview
The page lists exam solutions, each linked to a resource of the form:
```
http://trova-le-soluzioni.challs.olicyber.it/soluzioni-2023-2024/soluzioni/20231006.txt
```
Only the 6 October 2023 solution is enabled; the others (4 Dec 2023, 10 Mar 2024, 9 May 2024) are shown as disabled `<span>` elements in the HTML, without an actual link, but the naming convention (`YYYYMMDD.txt`) is disclosed directly in the page source via the visible dates.

## Solve
Guessing the filename for the not-yet-published exam by following the same date pattern:
```
http://trova-le-soluzioni.challs.olicyber.it/soluzioni-2023-2024/soluzioni/20231204.txt
```
The file is directly accessible despite not being linked on the page (no server-side access control, only client-side hiding), and returns the flag.