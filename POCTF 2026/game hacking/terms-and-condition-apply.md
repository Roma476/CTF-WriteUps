# Terms and Conditions Apply

| | |
|---|---|
| **Section** | wave 7 |
| **Category** | game hacking |
| **Solves** | 92 |

## Overview

The game is a Godot 4.7.1 export. The embedded PCK lives in the `pck` section of the ELF and contains 200 files, including compiled `.gdc` scripts. The important scripts are `NetworkClient.gdc`, `boss.gdc`, `arena.gdc`, and `heal_zone.gdc`.

The server is authoritative for the boss state. A fresh session starts with:

```text
is_invulnerable = true
avoid_heal_zones = true
hp = 2147483000
```

The boss's starting HP is only 648 below `INT32_MAX`. Damage events are ignored while the boss is invulnerable, and the player's normal spell damage is only 25, so ordinary combat cannot reach zero. The arena's win condition is different: when the server state reports `hp < 0`, `arena.gdc` calls `NetworkClient.finish_and_get_flag()`.

Heal zones heal a boss standing inside them for 400 HP per second, applied in 0.1-second ticks, or about 40 HP per `heal_tick` event. Because the starting HP is just below the signed 32-bit limit, healing it past `2^31` wraps the value negative. The client also has the ability to send `flag_flip` events, so the boss's `avoid_heal_zones` flag can be turned off.

The client-side `watchdog.gdc` only compares the local boss properties against their initial values. Sending the flip as a signed server event, without changing the local property, avoids the watchdog entirely.

## Solve

The shortest route is to flip `avoid_heal_zones`, tell the server the boss is in a heal zone, and deliver enough heal ticks to cross the signed 32-bit boundary. The original `NetworkClient` autoload can generate the required HMAC-signed events:

```gdscript
NetworkClient.send_flip("avoid_heal_zones", false)
NetworkClient.send_zone(true)
for i in range(24):
    NetworkClient.send_heal(40)
```

The server accepted the flip and the zone entry; the boss HP then climbed by 40 per heal tick:

```text
2147483040
2147483080
...
2147483600
2147483640
-2147483616
```

At the final step the signed 32-bit value wrapped negative. The arena sees `hp < 0` and requests the finish marker. The finish endpoint returned the challenge flag, which was accepted by the submission page. The accepted flag was `████████████████`.