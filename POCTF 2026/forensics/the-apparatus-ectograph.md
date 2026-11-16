# The Apparatus, Ectograph

| | |
|---|---|
| **Section** | wave 6 |
| **Category** | forensics |
| **Solves** | 183 |

## Overview

The recovered Threshold data directory contains `threshold.db`, `config.json`, an `attachments/` folder, and two loose text files. The SQLite schema is small: `users`, `devices`, `sessions`, `threads`, `thread_participants`, `messages`, `message_edits`, `reactions`, and `attachments`. There are 58 messages across ten threads, 21 device rows, and 40 sessions; `message_edits` and `reactions` are empty. The important table is `messages`, because every row keeps both `sender_id` — the account — and `sender_device_id`, the client that actually sent it. The prompt describes exactly a mismatch between those two columns: the messages look like Elena's account, but not like one of Elena's devices.

One clock issue has to be settled before any query. The prompt uses `2026-06-28 22:47`, but the database's `sent_at` values are 2024 epochs. The range is `1719080400`–`1719962400`, or `2024-06-22 18:20:00`–`2024-07-02 23:20:00` UTC. A literal `WHERE sent_at >= 1782686820` returns zero rows. The useful boundary is not the narrative timestamp; it is the last message from Elena's original device, after which the account's next messages come from a different client.

## Solve

Start with the device table for `u_elena` / `@e.marchetti`:

```bash
sqlite3 threshold.db <<'SQL'
.headers on
.mode column
SELECT id, device_name, device_fingerprint,
       datetime(registered_at, 'unixepoch') AS registered,
       datetime(last_seen_at, 'unixepoch')  AS last_seen,
       is_active
FROM devices
WHERE user_id = 'u_elena'
ORDER BY registered_at;
SQL
```

The result is four rows:

| device id | device name | registered (UTC) | last seen (UTC) | active |
|---|---|---|---|---|
| `6XQDEDUHPWFMNMVE` | Elena's MacBook Pro | 2024-02-03 22:40:00 | 2024-07-02 17:20:00 | 1 |
| `GZSNOSIHIU62F773` | Elena's iPhone 15 Pro | 2024-02-03 22:50:00 | 2024-07-02 17:50:00 | 1 |
| `████████████████` | Elena's MacBook | 2024-07-02 18:21:00 | 2024-07-03 02:00:00 | 1 |
| `DWA2CYMFMTOEFMWK` | Elena's iPad | 2024-07-03 09:46:40 | 2024-06-27 18:20:00 | 0 |

Three rows have activity before the incident: the MacBook Pro, the iPhone, and the iPad, whose `last_seen_at` is `2024-06-27 18:20:00`. The iPad's `registered_at` is later than its `last_seen_at`, which is impossible for a genuinely new device; it is inactive and, as shown below, has no sessions and no messages. That anomaly is the decoy. The fourth row, `████████████████`, has no pre-incident activity: it is created at `2024-07-02 18:21:00`, after Elena's last genuine message, and it is the only device that sends messages after that point.

Group Elena's messages by sending device:

```sql
SELECT sender_device_id, COUNT(*) AS n,
       datetime(MIN(sent_at), 'unixepoch') AS first,
       datetime(MAX(sent_at), 'unixepoch') AS last
FROM messages
WHERE sender_id = 'u_elena'
GROUP BY sender_device_id;
```

The output is only two devices:

```text
6XQDEDUHPWFMNMVE  20  2024-06-22 19:20:00  2024-07-02 18:00:01
████████████████   3  2024-07-02 19:20:00  2024-07-02 23:20:00
```

The MacBook Pro sent 20 messages and stopped at `2024-07-02 18:00:01`. That last message is `m_f4vcbsc2yesi`, the attachment message for `20260628_ectograph_transcript.txt`. The next three messages from Elena's account are all from `████████████████`:

| sent (UTC) | thread | body | read at |
|---|---|---|---|
| 2024-07-02 19:20:00 | `th_delacroix` | "You're right. Deleting. Please stop contacting me. I'm dropping the research. Delete everything I sent you." | `NULL` |
| 2024-07-02 20:20:00 | `th_rennick` | "Aldous, I've thought about it. I'm withdrawing from the program effective immediately. I'll be unreachable for a few weeks. Please don't try to contact me." | `NULL` |
| 2024-07-02 23:20:00 | `th_renata` | "Ren I'm going up to Marion's for the weekend. Research overnight, phone off. Don't worry." | `NULL` |

These are the three messages the prompt describes. They are coordinated across three different threads, all within four hours, and all from the same non-original device. The content is also consistent with an attempt to close the investigation: the Delacroix message destroys the transcript thread, the Rennick message explains an abrupt withdrawal, and the Renata message gives a false location and a reason to be unreachable. The `read_at` values are `NULL`; the genuine messages have read receipts, so the absence is another small inconsistency.

The device row and its sessions explain why `████████████████` is the pen:

```sql
SELECT id, device_name, device_fingerprint,
       datetime(registered_at, 'unixepoch') AS registered,
       datetime(last_seen_at, 'unixepoch')  AS last_seen,
       is_active
FROM devices WHERE id = '████████████████';

SELECT datetime(started_at, 'unixepoch') AS started, ip_address
FROM sessions WHERE device_id = '████████████████'
ORDER BY started_at;
```

The device is named "Elena's MacBook", fingerprint `MacBookAir-M2 macOS 14.5`, registered at `2024-07-02 18:21:00` and last seen at `2024-07-03 02:00:00`. Its registration is about 21 minutes after the last message from `6XQDEDUHPWFMNMVE`, and about 59 minutes before the first forged message. That is the enrollment window. Its sessions are:

```text
2024-07-02 18:21:00   203.0.113.113
2024-07-05 18:21:00   203.0.113.66
```

The network evidence is unusually clean: 38 of the 40 sessions in the database use `192.0.2.x`, while the two sessions for `████████████████` use `203.0.113.x`. The two documentation ranges — TEST-NET-1 and TEST-NET-3 — were deliberately kept apart. The device was enrolled, immediately opened a session from the second range, sent the three messages, and was seen again three days later from the same range. The second session is after the database's last message, so the device remained active after the forgery.

The iPad is the main dead end. `DWA2CYMFMTOEFMWK` has `last_seen_at = 2024-06-27 18:20:00` but `registered_at = 2024-07-03 09:46:40`, is marked `is_active = 0`, and has no sessions or messages:

```sql
SELECT COUNT(*) FROM messages WHERE sender_device_id = 'DWA2CYMFMTOEFMWK'; -- 0
SELECT COUNT(*) FROM sessions WHERE device_id = 'DWA2CYMFMTOEFMWK';        -- 0
```

If the only criterion is "a device that shouldn't exist", the iPad looks like the answer because its timestamps are impossible. It is not: it authored none of the three messages. The decisive column is `messages.sender_device_id`, not `devices.registered_at`. The iPad is a decoy, and submitting its ID returns `Incorrect`.

The attachments and loose text files are also decoys. Only one attachment is actually referenced by a message: `att_ecto_cpvzcjyj` on `m_f4vcbsc2yesi`, the ectograph transcript. The other four — `20260615_rennick_deadline.png`, `20260620_redoubt_receipt.jpg`, `20260625_spr_confirmation.pdf`, and `20260626_yee_subtweet.png` — have `message_id = NULL`. They are orphaned flavor files, not part of the message graph. Their `content_hash` values are 16 characters and look base32-like, but they are content hashes, not device IDs; the same is true of the 16-character session IDs. `unaccounted_transmission.txt` is an out-of-band ASCII fragment and contains no device identifier.

The transcript is the narrative hint, not the payload:

```text
The hand is not the medium's.
The signal comes from behind the wall.
The pen has never left the drawer.
The words were spoken in another room.
```

That is the same observation the database makes: the hand typing is not Elena's, the pen is not one of her devices, and the words came from another room. The `README.txt` states it more directly: "Not everything you'll read here was said by whom it looks like."

The timestamp cutoff is another dead end. Querying the literal 2026 epoch returns nothing, and querying the 2024-06-28 22:47 epoch returns many genuine messages from `6XQDEDUHPWFMNMVE`; it does not isolate the three forged ones. The reliable pivot is the device switch: after the last `6XQDEDUHPWFMNMVE` message, the account has exactly three messages, and all three carry the same new `sender_device_id`.

The rogue device is `████████████████`. It is 16 characters and valid base32. On the artifact page, submitting the raw token or `POCTF{████████████████}` returns:

```json
{"correct":true,"message":"Correct."}
```

The full marker is `POCTF{████…}`.

The pen that was not the medium's is `████████████████`, and the flag is `POCTF{████…}`.