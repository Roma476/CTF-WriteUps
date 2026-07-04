# find-me
| | |
|---|---|
| **Section** | HighSchools CTF Workshop - 2023 Verona |
| **Category** | web |
| **Solves** | 223 |

## Overview
The homepage links to a menu page:
```
http://find-me.challs.olicyber.it/menu?file=menu.txt
```
The `file` GET parameter is passed unsanitized to the server-side file read function, resulting in a classic Local File Inclusion / Path Traversal vulnerability.

## Solve
By traversing outside the intended directory:
```
http://find-me.challs.olicyber.it/menu?file=../../flag.txt
```
the server reads and returns the content of `flag.txt` instead of the menu file, leaking the flag. No filtering on `../` sequences or path normalization is performed on the `file` parameter, allowing arbitrary file reads elsewhere on the filesystem as well (subject to the web server's permissions).