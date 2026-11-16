# Health Is a Social Construct

| | |
|---|---|
| **Section** | wave 4 |
| **Category** | game hacking |
| **Solves** | 206 |

## Overview

The download is a Godot 4.7.1 x86-64 export. The game logic is stored in the embedded PCK at file offset `0x4611138`, which contains 398 files. The relevant scripts are `scenes/auth_check.gdc`, `scenes/game/game_controller.gdc`, `scenes/game/room03.gdc`, `scenes/actors/player.gdc`, `scenes/actors/enemy_basic.gdc`, `FlagToken.gdc`, and `Ticker.gdc`.

The game authenticates with `game.token` and `team.key`, calls `GET /api/challenges/48/instance` to obtain a nonce, and then starts a 2.5-second HMAC ticker. The final room spawns a boss with `max_hp=3000` and `attack_damage=999`, while the player has `max_hp=100`, so ordinary play cannot win. When the boss dies, `room03` emits `room_cleared`; `game_controller._finalize_run()` calls `FlagService.request_marker()`, which POSTs to `/api/challenges/48/complete` with the auth headers and nonce. The returned `marker` is displayed by the flag overlay.

The important observation is that the completion endpoint receives no proof of a win. It only validates the team credentials and the instance nonce. The ticker is not required for completion, and the server has no knowledge of the boss HP, the room state, or whether the client was ever launched. The "social construct" is the client-side win check itself: skip it and ask the server for the marker.

## Solve

Extract the credentials from `credentials.zip` and request an instance nonce:

```http
GET /api/challenges/48/instance HTTP/1.1
Host: pointeroverflowctf.com
X-POCTF-GAME-TOKEN: ████████████████
X-POCTF-TEAM-KEY: ████████████████
```

The response contains the nonce used by the game:

```json
{"challenge_id":48,"download_count":0,"nonce":"████████████████","ok":true,"team_id":1814}
```

Then call the same completion endpoint that `FlagToken.gd` uses, without ever starting the game:

```http
POST /api/challenges/48/complete HTTP/1.1
Host: pointeroverflowctf.com
X-POCTF-GAME-TOKEN: ████████████████
X-POCTF-TEAM-KEY: ████████████████
X-POCTF-CHALLENGE-NONCE: ████████████████
Content-Type: application/json

{}
```

The server returned a marker:

```json
{"challenge_id":48,"marker":"████████████████","team_id":1814}
```

Submitting that marker to the challenge page returned `{"correct":true,"message":"Landed. Nicely done."}`.

The intended client-side route is also visible in the scripts. `room03.boss_max_hp` and `boss_attack_damage` are exported variables, and `enemy_basic.apply_damage()` trusts its argument. A debugger or a patched PCK can set the boss HP to 1, raise the player HP, or invoke `apply_damage(999999)` on the boss. That would make `room03` emit `room_cleared`, reach `_finalize_run()`, and mint the same marker through the normal overlay. But the endpoint is the weaker link: because `complete` does not verify that any of that happened, the game can be skipped entirely.

The accepted flag was ████████████████.