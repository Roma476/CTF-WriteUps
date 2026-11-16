# No Structure Required

| | |
|---|---|
| **Section** | wave 3 |
| **Category** | web |
| **Solves** | 340 |

## Overview

SecureNotes v1.0 is a small document-store application backed by the “Whitmore Storage Engine.” Its login endpoint accepts JSON and passes the supplied values directly into the query object. This allows operator injection to bypass authentication, and the browse endpoint then exposes documents from collections that the signed-in user should not reach.

## Solve

The login form posts JSON to `login` with `username` and `password`. A source comment confirmed that the endpoint accepts `application/json` and that the two keys are passed through to the query as-is. Supplying query operators instead of strings bypassed the credential check:

```json
{"username": {"$ne": null}, "password": {"$ne": null}}
```

The response set a session cookie and reported a successful sign-in as an ordinary user:

```json
{"message": "Signed in as j.abernathy.", "next": ".../dashboard", "ok": true}
```

The dashboard linked to `browse?col=notes`, where the `col` parameter selects a collection and the raw documents are rendered. The page's own note stated that other collections may exist depending on role, but the browse handler applied no ownership or role restriction to the requested collection.

Enumerating collection names through `browse?col=<name>` exposed the backing data. The `users` collection revealed usernames, passwords, and roles, including an administrator account. The `secrets` collection returned a single document labelled as the team flag, with the marker in its `flag` field. Accessing that collection required no administrator session; the authentication bypass plus the unrestricted collection parameter was sufficient.

The submitted flag was POCTF{78.1814.████████████████.████████████████} and it was accepted.