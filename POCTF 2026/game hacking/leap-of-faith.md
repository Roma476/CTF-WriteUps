# Leap of Faith

| | |
|---|---|
| **Section** | wave 2 |
| **Category** | game hacking |
| **Solves** | 352 |

## Overview

The download is a Godot 4.7.1 x86-64 export. The embedded PCK starts at file offset `0x4611138` and contains 79 files. The relevant scripts are `player.gd`, `goal.gd`, `GameController.gd`, `SceneManager.gd`, `end_screen.gd`, `auth_check.gd`, and `FlagToken.gd`.

`player.gd` is a `CharacterBody3D` with exported `move_speed=6.0`, `jump_velocity=17.5`, and `gravity=18.0`. The final platform is intentionally out of reach for that jump. `goal.gd` is an `Area3D` that emits `goal_reached` when the player body enters it. `GameController.gd` connects that signal to `Scenes.goto_end()`, which loads `end_screen.tscn`. The end screen immediately calls `FlagService.request_marker()`, and `FlagToken.gd` POSTs to `/api/challenges/47/complete` with the team headers and the nonce from `/api/challenges/47/instance`.

The challenge page notes that the uploaded binary is actually the test build and trivializes the intended jump. That is useful, but the completion endpoint is the weaker link: it receives no proof that the player ever reached the goal, cleared the level, or even launched the game. It only validates the credentials and the instance nonce.

## Solve

Request a nonce with the credentials from `credentials.zip`:

```http
GET /api/challenges/47/instance HTTP/1.1
Host: pointeroverflowctf.com
X-POCTF-GAME-TOKEN: ████████████████
X-POCTF-TEAM-KEY: ████████████████
```

The response contains the nonce:

```json
{"challenge_id":47,"download_count":0,"nonce":"████████████████","ok":true,"team_id":1814}
```

Then call the same completion endpoint used by `FlagToken.gd`:

```http
POST /api/challenges/47/complete HTTP/1.1
Host: pointeroverflowctf.com
X-POCTF-GAME-TOKEN: ████████████████
X-POCTF-TEAM-KEY: ████████████████
X-POCTF-CHALLENGE-NONCE: ████████████████
Content-Type: application/json

{}
```

The server returned the marker:

```json
{"challenge_id":47,"marker":"████████████████","team_id":1814}
```

Submitting the marker to the challenge page returned `{"correct":true,"message":"Landed. Nicely done."}`.

The intended game-side route is also clear from the scripts. `jump_velocity` is an exported property, so a debugger or a patched PCK can raise it enough to clear the final gap. Alternatively, setting the player's `global_position` to the goal's position makes the goal area fire `goal_reached`, which leads to the end screen and the same marker request. Either change is local to the client; the server does not verify the jump.

The accepted flag was ████████████████.