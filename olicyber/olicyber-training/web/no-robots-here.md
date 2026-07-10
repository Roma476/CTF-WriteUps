# No Robots Here

| | |
|---|---|
| **Section** | Web Security |
| **Category** | web |
| **Solves** | 3249 |

## Overview

The application exposes a `robots.txt` file.

## Solve

Visiting:

```
/robots.txt
```

reveals a hidden path:

```
User-agent: *
Disallow: /I77p0mhKjr.html
```

Accessing the disallowed endpoint directly:

```
/I77p0mhKjr.html
```

returns the page containing the flag.