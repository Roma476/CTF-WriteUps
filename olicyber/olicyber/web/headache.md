# Headache

| | |
|---|---|
| **Section** | Web Security |
| **Category** | web |
| **Solves** | 3362 |

## Overview

The HTTP response includes a custom header containing the flag.

## Solve

There are multiple ways to retrieve it (browser, curl, Python requests, etc.), but the fastest is simply opening DevTools and inspecting the response headers of the main request.

Alternatively:

```
curl -v http://headache.challs.olicyber.it/
```

The response includes a `Flag` header containing the solution:

```
Flag: <redacted>
```