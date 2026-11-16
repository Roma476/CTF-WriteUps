# The Logic Inside

| | |
|---|---|
| **Section** | wave 4 |
| **Category** | web |
| **Solves** | 262 |

## Overview

A URL preview service fetches user-supplied URLs server-side and reports only the outcome and the upstream HTTP status code. A hostname filter blocks loopback and private addresses, but the filter can be bypassed with an alternative representation of `127.0.0.1`. That turns the preview service into a status-code oracle against a second application bound to `127.0.0.1:9001`, whose `/flag` endpoint checks a nonce prefix.

## Solve

The preview endpoint accepted a JSON body of the form `{"url": "..."}` and returned a small JSON object such as:

```json
{"note": "preview generated", "ok": true, "upstream_status": 200}
```

Requests to literal loopback and private hosts were rejected before any fetch:

```json
{"error": "host blocked by policy", "hostname_seen": "127.0.0.1", "ok": false}
```

The filter operated on the hostname string, not on the resolved address. The single-label host `0` passed the filter and resolved to `127.0.0.1`; the decimal and octal forms of the address worked as well. The preview service could therefore be pointed at the internal application:

```text
http://0:9001/flag?guess=<prefix>
```

The internal application returns `200` when the supplied hexadecimal string is a prefix of the 16-character nonce, and `404` otherwise (`400` for an empty guess). Because the preview service reports the upstream status code, it acts as a prefix oracle.

I recovered the nonce one character at a time. For each position, the current known prefix was extended with each candidate from `0123456789abcdef`; the candidate whose status was `200` was kept, and the search moved to the next position:

```python
prefix = ""
for _ in range(16):
    for ch in "0123456789abcdef":
        if upstream_status(f"http://0:9001/flag?guess={prefix}{ch}") == 200:
            prefix += ch
            break
```

Sixteen positions yielded the complete 16-character nonce, and a final query with the full value returned `200`. The submitted nonce was ████████████████ and it was accepted.