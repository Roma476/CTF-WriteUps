# È tutto solo una convenzione

| | |
|---|---|
| **Section** | OliCyber 2023 Training Camp 3 |
| **Category** | web |
| **Solves** | 470 |

## Overview

The challenge gives the link to a site that only displays the message:

```
Fai una richiesta con metodo FLAG
```

## Solve

Sending a request with the custom `FLAG` method:

```bash
curl -X FLAG http://convenzione.challs.olicyber.it/
```

returns a hint instructing the user to inspect the response headers.

Using verbose mode:

```bash
curl -X FLAG -v http://convenzione.challs.olicyber.it/
```

reveals a custom HTTP header containing the flag.