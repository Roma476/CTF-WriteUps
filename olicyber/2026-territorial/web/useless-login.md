# Useless login

| | |
|---|---|
| **Section** | OliCyber 2026 Selezione Territoriale |
| **Category** | web |
| **Solves** | 143 |

## Overview

The site provides a simple login/registration system, but after authentication there is no real functionality exposed to the user.

After logging in, the session cookie contains a Base64-encoded JSON object:

```
{"username":"foo","is_admin":0}
```

This shows that the application relies on client-side controlled session data.

## Solve

By decoding the cookie, modifying it to:

```
{"username":"foo","is_admin":1}
```

and re-encoding it in Base64, we can elevate privileges to admin.

Using the modified cookie in the session grants admin access, and visiting the authenticated area reveals the flag.