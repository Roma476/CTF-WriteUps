# Client-Side Truth

| | |
|---|---|
| **Section** | wave 8 |
| **Category** | game hacking |
| **Solves** | 53 |

## Overview

The game is a Godot client. Its scripts are packed into a PCK embedded in the ELF; the `pck` section starts at file offset `0x4611138`. The PCK header gives the file-table offset, the table lists 128 files, and each entry provides the data offset, size, and MD5. Extracting and decompiling the `.gdc` scripts reveals the network protocol in `NetworkClient.gdc`:

```text
POST /challenges/client-side-truth/game/start
POST /challenges/client-side-truth/game/pos   {"ts":..., "x":..., "y":..., "z":...}
POST /challenges/client-side-truth/game/fire  {"ts":...}
GET  /challenges/client-side-truth/game/state
GET  /challenges/client-side-truth/game/win_marker
```

The client authenticates with `Authorization: Bearer <game.token>` and `X-Team-ID: <team_id>`. The boss starts with 500 HP and each shot does 50 damage. Damage is only valid from inside the `count_room` area, but the position is supplied by the client and is not validated server-side.

## Solve

Start a game session, then set the position inside the count room. The working position is `[-20, 21.8, 18.1]`. Fire ten times; each call subtracts 50 HP, reducing the boss to zero. Query the state to see `"won": true`, then fetch the win marker:

```python
import json, time, urllib.request

BASE = "https://pointeroverflowctf.com"
TOKEN = "<game.token>"
TEAM = "<team_id>"
H = {
    "Authorization": "Bearer " + TOKEN,
    "X-Team-ID": TEAM,
    "Content-Type": "application/json",
}

def req(method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(BASE + path, data=data, headers=H, method=method)
    with urllib.request.urlopen(r, timeout=15) as resp:
        return resp.read().decode()

req("POST", "/challenges/client-side-truth/game/start", {})
req("POST", "/challenges/client-side-truth/game/pos",
    {"ts": int(time.time() * 1000), "x": -20, "y": 21.8, "z": 18.1})
for _ in range(10):
    req("POST", "/challenges/client-side-truth/game/fire",
        {"ts": int(time.time() * 1000)})
print(req("GET", "/challenges/client-side-truth/game/win_marker"))
```

The win marker contains the flag. The accepted flag was `████████████████`.