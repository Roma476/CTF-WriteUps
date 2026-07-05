# trova_le_soluzioni3
| | |
|---|---|
| **Section** | HighSchools CTF Workshop - 2023 Perugia |
| **Category** | web |
| **Solves** | 216 |

## Overview
The site now uses a login form (`username`/`password`) backed by a SQL database to dynamically determine which files are visible to the logged-in user. Injecting a single quote `'` into the `username` field triggers a MySQL syntax error, disclosing the underlying query:
```
SELECT * FROM users WHERE password = '<hash>' AND name = '<username>'
```

## Solve
The query is vulnerable to classic SQL Injection. Submitting as `username`:
```
' OR 1=1 -- 
```
comments out the rest of the query (including the password check), causing the application to authenticate as `admin`. After login, an additional unreleased solution file is disclosed in the list:
```
/read.php?file=/soluzioni/20240509.txt
```
Requesting it returns the flag.