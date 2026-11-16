# The Interior Route

| | |
|---|---|
| **Section** | wave 6 |
| **Category** | web |
| **Solves** | 148 |

## Overview

Bittner & Cross run a link preview tool: `POST /preview` with `{"url": "..."}` makes the server fetch that URL and return the body. The service claims it can only reach external hosts and cannot see any private network. That claim is the whole challenge — the preview endpoint is a server-side request forgery primitive, and the flag sits on the instance metadata service that the filter was supposed to cover.

## Solve

A baseline request for `https://example.com` returns a canned page (“Link preview unavailable for external URLs in demo mode”), which is just the demo behaviour. Asking for `http://127.0.0.1/` returns the same canned page: the loopback address is recognised and short-circuited. The filter is a list of forbidden hosts, not a check performed on the resolved address.

Link-local space is not on that list. Requesting `http://169.254.169.254/latest/meta-data/` reaches the metadata service instead of the demo stub, and the service answers `404 NOT FOUND` — a real HTTP response, proving the request left the preview worker and hit the metadata endpoint.

The IAM branch is present. `/latest/meta-data/iam/security-credentials/` returns a single role name, `poctf-service-role`, and fetching `/latest/meta-data/iam/security-credentials/poctf-service-role` returns the full credential document with `Code`, `LastUpdated`, `Type`, `AccessKeyId`, `SecretAccessKey`, `Token` and `Expiration`.

The `AccessKeyId` is not a key at all: it is the flag marker, planted where only the metadata service could hand it out. The surrounding credentials are obviously fake placeholders, so nothing further — no S3 call, no signing — is needed.

The flag is ████████████████.