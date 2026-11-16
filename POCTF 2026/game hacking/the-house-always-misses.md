# The House Always Misses

| | |
|---|---|
| **Section** | wave 5 |
| **Category** | game hacking |
| **Solves** | 141 |

## Overview

The download is a Godot 4.7.1 x86-64 export. The embedded PCK starts at file offset `0x4643178` and contains 111 files. The relevant scripts are `scenes/game/gallery.gd`, `scenes/actors/target_base.gd`, the target subclasses (`flip_target.gd`, `popup_target.gd`, `duck.gd`, `civilian.gd`), `FlagToken.gd`, and `auth_check.gd`.

The gallery gives the player 60 seconds to reach a score of 1200. Flip targets are worth 25 points, popup targets 50, ducks 10, and civilians subtract 50. A shot is resolved entirely on the client in `gallery.gd:_click_at()`:

```gdscript
var query := PhysicsPointQueryParameters2D.new()
query.position = pos
query.collision_mask = 1
query.collide_with_areas = true
query.collide_with_bodies = false
var results := space.intersect_point(query, 8)
```

The first `TargetBase` in the results that has not already been hit receives `on_hit()`. The geometry of that query is what decides whether a shot lands.

On reaching the threshold, `gallery.gd:_win()` calls `FlagService.request_marker()`. `FlagToken.gd` then POSTs to `/api/challenges/49/complete` with the team headers and the nonce from `/api/challenges/49/instance`.

The challenge hint points at the hit test, but the completion endpoint is even more direct: it does not receive the score, a hit count, or any proof that the gallery was played. It only checks the credentials and the instance nonce.

## Solve

Request a nonce with the credentials from `credentials.zip`:

```http
GET /api/challenges/49/instance HTTP/1.1
Host: pointeroverflowctf.com
X-POCTF-GAME-TOKEN: ████████████████
X-POCTF-TEAM-KEY: ████████████████
```

The response contains the nonce:

```json
{"challenge_id":49,"download_count":0,"nonce":"████████████████","ok":true,"team_id":1814}
```

Then call the same completion endpoint used by `FlagToken.gd`:

```http
POST /api/challenges/49/complete HTTP/1.1
Host: pointeroverflowctf.com
X-POCTF-GAME-TOKEN: ████████████████
X-POCTF-TEAM-KEY: ████████████████
X-POCTF-CHALLENGE-NONCE: ████████████████
Content-Type: application/json

{}
```

The server returned the marker:

```json
{"challenge_id":49,"marker":"████████████████","team_id":1814}
```

Submitting the marker to the challenge page returned `{"correct":true,"message":"Landed. Nicely done."}`.

For the intended client-side route, replace the point query in `_click_at()` with a `PhysicsShapeQueryParameters2D` using a large `CircleShape2D`, so every target under the click is collected instead of only the exact pixel under the cursor. A debugger can also set `gallery._score` to `score_threshold`, or call `_win()` directly. The game's own hit geometry is the lie; changing that geometry changes what counts as a hit.

The accepted flag was ████████████████.