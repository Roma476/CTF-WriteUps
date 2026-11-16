# A Quiet Home

| | |
|---|---|
| **Section** | wave 4 |
| **Category** | forensics |
| **Solves** | 281 |

## Overview

The artifact set is a Home Assistant backup (`home-assistant_v2.db`, `configuration.yaml`), a Mosquitto broker log, and a 1,857-byte packet capture. The narrative places Elena's device tracker at Hollis, unlocks the front door at 14:47 with keypad slot 04, shows motion in the study until 15:34, and locks the door from inside at 15:36. The token is the 16-character base32 serial of a device that should not be in the apartment.

The capture and broker log run three hours ahead of the narrative clock — 17:47 rather than 14:47 — but the relative order is exact. The problem reduces to correlating three sources: the MQTT capture, which contains the device traffic; the broker log, which shows which clients were connected; and the Home Assistant database, which shows which devices the system knew about. A device that appears in the capture and the broker log but has no normal place in the device registry is the one the intruder carried.

## Solve

The capture is a classic Ethernet/IPv4/TCP pcap (`linktype 1`) containing MQTT PUBLISH packets. There is no TCP handshake, so a stream reassembler may not reconstruct the session; parsing the TCP payloads directly is deterministic. `strings` is enough for a first pass:

```bash
strings -n 3 mqtt-capture.pcap | grep -iE 'rf_key|serial|Aeotec|MiniMote|front_door|keypad'
```

For exact source addresses and timestamps, walk the pcap records and print each TCP payload:

```python
import struct
import datetime

b = open("mqtt-capture.pcap", "rb").read()
o = 24

while o + 16 <= len(b):
    ts, us, n, _ = struct.unpack_from("<IIII", b, o)
    o += 16
    p = b[o:o+n]
    o += n

    if len(p) < 14 or struct.unpack_from("!H", p, 12)[0] != 0x0800:
        continue

    ip = p[14:]
    ihl = (ip[0] & 0x0f) * 4
    if ip[9] != 6:
        continue

    tcp = ip[ihl:]
    thl = (tcp[12] >> 4) * 4
    data = tcp[thl:]

    if data:
        t = datetime.datetime.fromtimestamp(ts + us / 1e6, datetime.timezone.utc)
        print(t.isoformat(), data)
```

The relevant packets, decoded from their MQTT framing:

| time (UTC) | source | topic | payload |
|---|---|---|---|
| `17:47:00` | `192.168.1.11:44100` | `zwave/lock.front_door/state` | `{"state": "unlocked", "code_slot": 4, "changed_by": "keypad_04"}` |
| `17:47:30` | `192.168.1.47:55555` | `zwave/rf_key_c4pf5/attributes` | `{"node_id": 47, "product_id": "0x0037", "product_type": "0x0217", "product_serial": "████████████████", "manufacturer": "Aeotec", "model": "MiniMote Key Fob (ZW088)"}` |
| `18:36:00` | `192.168.1.11:44100` | `zwave/lock.front_door/state` | `{"state": "locked", "code_slot": 4, "changed_by": "keypad_04"}` |

Each MQTT packet starts with `0x30` (PUBLISH), followed by a variable-length remaining-length field, a two-byte topic length, the topic, and the JSON payload. The key fob message arrives exactly 30 seconds after the unlock, from a host that does not appear in the normal MQTT client set, and before the door is locked again. The living-room and study motion packets are normal Zigbee traffic; the key fob is the only new device in the window.

The Home Assistant database is SQLite. Open it read-only and query the `devices` table:

```python
import sqlite3

con = sqlite3.connect("file:home-assistant_v2.db?mode=ro", uri=True)

for row in con.execute(
    "select name, manufacturer, model, identifiers from devices order by name"
):
    print(row)
```

The suspicious row is:

```text
('RF Key Fob (unknown pairing)', 'Aeotec', 'MiniMote Key Fob (ZW088)',
 '[["zwave", "████████████████"]]')
```

The database contains 15 devices and 14 entities. The key fob is the only device named `unknown pairing`, and it is the only device with no corresponding entity row. The other 14 devices are named, paired devices with entities: the Schlage front-door lock, the Aeotec motion sensors, the Hue lamps, the Ecobee thermostat, the Roomba, and Elena's iPhone. Z-Wave JS created a device-registry row when the fob came into radio range, but never created an entity for it. That is the registry signature of an unpaired device that was observed and then disappeared.

The broker log confirms the client lifetime:

```bash
grep -nE 'zwave_c4pf5|192\.168\.1\.47' mosquitto.log
```

```text
124:1719942450: New client connected from 192.168.1.47 as zwave_c4pf5 (p2, c1, k60).
125:1719942451: Received PUBLISH from zwave_c4pf5 (d0, q0, r0, m0, 'zwave/rf_key_c4pf5/attributes', ... (256 bytes))
134:1719945420: Client zwave_c4pf5 disconnected.
```

The epoch values convert to `17:47:30`, `17:47:31`, and `18:37:00` UTC. The fob client exists only for the 49.5-minute intrusion window: it connects 30 seconds after the door unlocks and disconnects after the door locks at `18:36:00`. The source `192.168.1.47` is not one of the normal clients:

| client | source | role |
|---|---|---|
| `homeassistant` | `192.168.1.10` | Home Assistant |
| `zigbee2mqtt` | `192.168.1.11` | Zigbee gateway |
| `zwavejs2mqtt` | `192.168.1.12` | Z-Wave gateway |
| `front_door_lock` | `192.168.1.15` | front-door lock |
| `roomba_j7` | `192.168.1.20` | robot vacuum |
| `zwave_c4pf5` | `192.168.1.47` | only during the intrusion |

The `.47` host appears only for the fob's lifetime. Its last octet matches the fob's `node_id: 47`, and the client ID `zwave_c4pf5` is a transient broker identity, not the serial. The log gives the client and topic; the pcap supplies the serial; the database confirms the same serial in the device registry. The three sources agree.

The fob is an Aeotec MiniMote Key Fob (ZW088), a portable Z-Wave remote. It was not the access method: the door was opened with keypad slot 04, assigned to M. Halberd, not with the fob. The fob is the object the intruder carried. Its radio was detected by Elena's Z-Wave network when it came into range, it published its product attributes 30 seconds after the door opened, and it left the broker when the intruder locked the door and departed. The device that "shouldn't be there" is the fob, not the lock, the motion sensors, or Elena's phone.

Several details are deliberate dead ends. The database contains many 16-character base32 strings — `XKHPH6UB6KQYW2PM` is the front-door lock, `C4OUN5RVMLW522LU` is Elena's iPhone, and so on — but those belong to named, paired devices. The key fob is the only unknown pairing and the only device without an entity. The `states` and `entities` tables are noisy and do not contain the fob; querying them alone misses the device-registry row. The broker log's `(256 bytes)` is a framing count, not the serial; the pcap's TCP payload is the authoritative JSON. The pcap has no TCP handshake, so a normal MQTT dissector may not reassemble the stream; direct payload parsing is sufficient. The artifact clocks are also shifted: the pcap and log say `2024-07-02`, while the narrative says Thursday `06/25/2026`, and the times differ by three hours. The relative sequence — unlock, fob, motion, lock — is what matters.

The fob's serial is 16 base32 characters and is accepted raw or wrapped by the artifact page. The device is the Aeotec MiniMote Key Fob (ZW088), and the token is its `product_serial`. The serial of the unknown key fob is `████████████████`, and the flag is `POCTF{████…}`.