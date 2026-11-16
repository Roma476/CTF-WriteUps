# Between the Lines

| | |
|---|---|
| **Section** | wave 7 |
| **Category** | web |
| **Solves** | 121 |

## Overview

A reverse proxy sits in front of an application server. The proxy enforces an access rule on `/internal/*`, but the two components parse HTTP/1.1 message framing differently. By exploiting that disagreement, a request can be smuggled past the proxy's path check and executed by the back end.

## Solve

The service at `between-the-lines.pointeroverflowctf.com:9008` identified itself as `aperture-telephone/0.1`, with the proxy identified as `aperture-telephone/0.1-proxy`. A normal request showed that the back end advertises `/echo` and that `/internal/*` is restricted; a direct request to `/internal/` was answered by the proxy with `403 Forbidden`.

To determine the direction of the desync, I sent a `POST /echo` carrying both `Content-Length` and `Transfer-Encoding: chunked`, with a `Content-Length` shorter than the chunked body. The back end answered with its body parser's view of the request: it had honoured the chunked encoding (reporting an empty body), while the front end had honoured `Content-Length`. The front end therefore uses `Content-Length` and the back end uses `Transfer-Encoding` — a CL.TE desync.

The exploit body was built so that the proxy would forward it in full as the request body, while the back end would see the end of the chunked body early and interpret the remaining bytes as a new request:

```http
0

GET /internal/flag HTTP/1.1
Host: between-the-lines.pointeroverflowctf.com
X-Team-Token: <team token from the challenge page>
Connection: close

```

The declared `Content-Length` covered the entire payload, so the proxy treated the embedded request as ordinary body bytes and never applied its `/internal/*` rule to it. The back end terminated the chunked body at the `0` chunk and then parsed the following bytes as a fresh request, which reached the restricted handler.

The proxy relayed the back end's pipelined responses on the same connection, exposing the restricted handler's reply alongside the `/echo` response. The reply contained the challenge marker. The submitted flag was POCTF{83.1814.████████████████.████████████████} and it was accepted.