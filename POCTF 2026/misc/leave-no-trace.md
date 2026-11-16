# Leave No Trace

| | |
|---|---|
| **Section** | wave 7 |
| **Category** | misc |
| **Solves** | 104 |

## Overview

The target is a small static personal homepage for "M. Lange", last updated in 2019. The rendered page is a reading list and a contact note; the hint says that the page is not the site. The flag nonce is sixteen characters, split into four four-character fragments, each hidden on a different HTTP surface and labeled with its position. The solution is therefore not on the page at all: it is in the HTML source, the response headers, `robots.txt`, and the metadata of the favicon.

The site is served under `/challenges/leave-no-trace/site/` and the platform session cookie is required. The fragments are found with `curl -i` and a small amount of binary inspection, not with directory brute force.

## Solve

The first surface is the HTML body. Viewing the source shows a comment above `<body>`:

```html
<!-- site: personal-static; fragment 1/4: ec15 -->
```

That is fragment `1/4: ec15`.

The second surface is the HTTP response headers. A `GET` or `HEAD` on the site root returns, among the usual security headers:

```
x-powered-by: handwritten HTML
x-site-fragment: 2/4:b7b6
```

The custom `x-site-fragment` header carries `2/4: b7b6`. It is invisible in the rendered page and in the body source; only the response headers expose it.

The third surface is `robots.txt`:

```
# Personal site — please respect crawl-delay.
User-agent: *
Crawl-delay: 5
Disallow: /drafts/
Disallow: /notes/private/
Disallow: /.rev-0de5/     # build tag; ignore
Disallow: /_backup/

Sitemap: /sitemap.xml
```

The line `Disallow: /.rev-0de5/` disguises the fragment as a revision/build tag. `0de5` is the four-character token, and the `# build tag; ignore` comment is the misdirection: the thing the author says to ignore is exactly what was left behind. It fills the remaining `3/4` slot.

The fourth surface is the favicon. The page links it as `favicon.png`; fetching the PNG and running `strings` over it shows two `tEXt` chunks:

```
tEXtDescription
personal-site favicon; ignore
tEXtFragment
4/4:a5c9
```

The `tEXtFragment` chunk is `4/4: a5c9`. The `tEXtDescription` says "ignore" as well; the fragment is in the neighboring chunk, not in the description. `exiftool favicon.png` shows the same PNG text chunks in a more structured form.

The four pieces, in order, are:

```
1/4  ec15
2/4  b7b6
3/4  0de5
4/4  a5c9
```

Concatenated, the nonce is:

```
████████████████
```

The submission endpoint is `POST /challenges/leave-no-trace/submit` with a JSON body:

```http
POST /challenges/leave-no-trace/submit
Content-Type: application/json

{"answer":"████████████████"}
```

The response is:

```json
{"correct":true,"message":"Correct. Marker recorded."}
```

The endpoint accepts separators or none and is case-insensitive; it also accepts the full `POCTF{...}` marker. Submitting the bare nonce is enough.

The commands used, with the session cookie elided:

```bash
BASE='https://pointeroverflowctf.com/challenges/leave-no-trace/site'
curl -i "$BASE/" -b 'session=<cookie>'
curl -i "$BASE/robots.txt" -b 'session=<cookie>'
curl -s "$BASE/favicon.png" -b 'session=<cookie>' | strings -n 4
```

The instructive dead ends are the remaining "surfaces" that look promising but are empty. `sitemap.xml`, referenced by `robots.txt`, returns 404: the sitemap is one of the traces that was removed, not the fragment. The disallowed directories (`/drafts/`, `/notes/private/`, `/_backup/`, and `/.rev-0de5/`) all return 404; `/.rev-0de5/` is not a directory to list, it is a build tag carrying the fragment. `OPTIONS /` returns `Allow: GET, HEAD, OPTIONS` with no fragment, `TRACE` returns 405, and `/.well-known/security.txt` and `humans.txt` return 404. Brute-forcing filenames is unnecessary; the four surfaces are already visible from a normal request.

The pattern is the point of the challenge: a static site is more than its rendered body. The response headers, the crawler policy, and the binary assets are separate HTTP surfaces, and each one can retain something the author forgot. The two "ignore" comments — in `robots.txt` and in the favicon description — are the same misdirection, and the fragments sit next to them.

The nonce is `████████████████`, and the marker is `POCTF{████…}`.