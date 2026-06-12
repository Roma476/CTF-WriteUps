# Gabibbo Innovazione Tecnologica

| | |
|---|---|
| **Section** | OliCyber 2023 Selezione Territoriale |
| **Category** | misc |
| **Solves** | 331 |

## Overview

The challenge provides both the web application and its Git repository.

The site is a simple note-taking service where users can log in and view their notes. Looking at the source code, an `admin` user is automatically inserted into the database and one of its notes contains the flag:

```python
c.execute("INSERT INTO notes (user_id, note) VALUES (?, ?)", (1, os.environ.get("FLAG", "My example flag!")))
```

However, the password stored in the latest version of the application is hashed:

```python
hashed_pw = '$2b$12$AQ6terssqMr7pUBQleGDaut1hzaZ2xVotg3J/wkighj3..5DPH8Ji'
c.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('admin', hashed_pw))
```

Since the repository history is available, the Git commit history becomes the most interesting attack surface.

## Solve

Inspecting the commit history shows that password hashing was introduced after the admin account had already been added:

```bash
git log
```

Relevant commits:

```text
62e4954 hash passwords before inserting in the db
6d74ea9 add admin for testing login
```

By checking out the commit immediately before password hashing was implemented:

```bash
git checkout 6d74ea9024383fcbf6cb5894a8f2db63181e28c7
```

and reading `app.py`, the admin credentials can be recovered in plaintext:

```python
c.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('admin', 'tkdF^cZFFaAD3!dTEQ7n'))
```

Using these credentials:

```text
Username: admin
Password: tkdF^cZFFaAD3!dTEQ7n
```

it is possible to log into the challenge website and access the admin's notes, where the flag is stored.