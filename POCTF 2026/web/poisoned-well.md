# Poisoned Well

| | |
|---|---|
| **Section** | wave 2 |
| **Category** | web |
| **Solves** | 579 |

## Overview

The Daily Whatever is served behind a response cache that is keyed only on the request path and the session cookie. The page's canonical link, RSS alternate link, and Open Graph URL are generated from the `X-Forwarded-Host` header, which the cache does not take into account. A single request carrying a forged host therefore stores a poisoned homepage under the normal cache key, and subsequent visitors receive the attacker-controlled URL.

## Solve

Signing in at `/login` with the team session token returns a signed session cookie that encodes the team identifier and the team nonce. The homepage then renders its metadata from the request host:

```html
<link rel="canonical" href="https://poisoned-well.pointeroverflowctf.com/">
<link rel="alternate" href="https://poisoned-well.pointeroverflowctf.com/rss.xml" type="application/rss+xml">
<meta property="og:url" content="https://poisoned-well.pointeroverflowctf.com/">
```

The page itself advertises the weakness: the cache is keyed strictly on request path plus session cookie, and all other request-modifying headers are treated as informational. Supplying a different host through `X-Forwarded-Host` is reflected into those three URLs while the response is still stored under the ordinary path and cookie key:

```bash
curl -b cookies.txt -D - \
  -H 'X-Forwarded-Host: news.example' \
  https://poisoned-well.pointeroverflowctf.com/
```

That response comes back with `X-Cache: MISS` and with the canonical, alternate, and `og:url` values pointing at `https://news.example/`. A second request without the header then hits the poisoned entry:

```bash
curl -b cookies.txt -D - https://poisoned-well.pointeroverflowctf.com/
```

This time the cache answers with `X-Cache: HIT`, and the HTML still contains the attacker-supplied host in its metadata, even though the request carried the legitimate host. The `Vary: Cookie` header explains why the entry is scoped to the team's session, so the same poisoned page is served to every later request made with that cookie, including the attacker's own.

The verification endpoint reads the canonical host out of the cached response and confirms the poisoning:

```bash
curl -b cookies.txt https://poisoned-well.pointeroverflowctf.com/verify
```

It reports `"cached_host": "news.example/"` together with `"ok": true` and the team's marker. If a clean response is accidentally cached first, `/reset` clears the entry so the poisoning can be repeated. The submitted flag was POCTF{82.1814.████████████████.████████████████} and it was accepted.