# The Apparatus, Levitation

| | |
|---|---|
| **Section** | wave 5 |
| **Category** | web |
| **Solves** | 168 |

## Overview

The LSSF parlour portal exchanges a team session token for a signed JWT that carries a role claim. Only the `SPIRIT` role may read the recovered marker from the transcript endpoint. The application verifies tokens with an RSA public key but also accepts HMAC-signed tokens, using that same public key material as the HMAC secret — an algorithm-confusion flaw that allows a forged `SPIRIT` token.

## Solve

The challenge page issued a short-lived team token. Posting it to the portal's session endpoint opened a `MEDIUM` session:

```http
POST /session HTTP/1.1
Host: levitation.pointeroverflowctf.com
Content-Type: application/json

{"token": "<team session token>"}
```

The response set a `levitation_session` cookie containing an RS256 JWT with header `{"alg":"RS256","typ":"JWT","kid":"spirit-key-1"}` and a payload carrying `team_id`, a per-team nonce, and `"role":"medium"`.

The portal advertised its verification material at `/.well-known/jwks.json`, and also exposed the same key as a raw PEM at `/spirit-key.pem`. That file contained a normal RSA public key. However, the verifier accepted an HS256 token whose HMAC secret was the exact contents of that public PEM file, including the trailing newline. With the header still naming `kid: spirit-key-1`, the algorithm confusion was accepted and the role claim was trusted.

I minted a replacement token with the same `team_id` and the same nonce claim as the issued session, but with `"role":"spirit"`, and signed it as HS256 using the raw PEM bytes as the key:

```python
header  = {"alg": "HS256", "typ": "JWT", "kid": "spirit-key-1"}
payload = {"team_id": 1814, "nonce": "<issued nonce>", "role": "spirit", ...}
signing_input = b64url(json(header)) + "." + b64url(json(payload))
token = signing_input + "." + b64url(hmac_sha256(pem_bytes, signing_input))
```

Requesting `/api/transcript` with this forged cookie returned the `SPIRIT` transcript instead of the medium-only attendance text. The transcript ended with the recovered marker, which was submitted successfully.

The submitted flag was POCTF{80.1814.████████████████.████████████████} and it was accepted.