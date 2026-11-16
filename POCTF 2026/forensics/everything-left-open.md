# Everything Left Open

| | |
|---|---|
| **Section** | wave 1 |
| **Category** | forensics |
| **Solves** | 801 |

## Overview

The README frames the artifact: docket `MARCHETTI / 2026-14`, a Firefox profile pulled from Elena's office workstation at Hollis University, found unlocked with an SPR provenance page in the last active tab, session interrupted mid-review. Analyst K. Vance, retained by R. Marchetti. The goal is "find what she was about to submit".

The archive contains a standard Firefox profile:

```
k-vance-profile/
├── places.sqlite
├── logins.json
├── formhistory.sqlite
├── prefs.js
└── sessionstore-backups/
    └── recovery.jsonlz4
```

"About to submit" rules out the obvious files. `places.sqlite` holds history and bookmarks, `logins.json` holds saved credentials, and `formhistory.sqlite` only receives values from forms that were actually submitted, for autocomplete. A form left half-filled is in none of them.

`prefs.js` explains why the data is on disk anyway:

```js
user_pref("browser.startup.page", 3);
user_pref("browser.sessionstore.resume_from_crash", true);
```

Restore-on-startup plus crash recovery means Firefox periodically serialises the current state of every tab — URL, scroll position and the live contents of form fields — into `sessionstore-backups/recovery.jsonlz4`, whether or not anything was ever submitted.

## Solve

The recovery file is not a normal LZ4 stream. Firefox uses `mozLz4`: an 8-byte magic `mozLz40\0`, a 4-byte little-endian length of the decompressed payload, and then the LZ4 block. That 12-byte header is why `cat` and `lz4 -d` both fail on it.

```python
import json, lz4.block

raw = open("k-vance-profile/sessionstore-backups/recovery.jsonlz4", "rb").read()
assert raw[:8] == b"mozLz40\0"
sess = json.loads(lz4.block.decompress(raw[12:]))

for w in sess["windows"]:
    for t in w["tabs"]:
        for e in t["entries"]:
            if e.get("formdata"):
                print(e["url"])
                for k, v in e["formdata"].items():
                    print(f"  {k:<14} = {v}")
```

`dejsonlz4` does the same unwrapping if it is installed. The single tab with unsent data is the SPR catalogue entry:

```
https://catalog.spr.org.uk/apparatus/provenance/lssf
```

with four fields:

| Field | Value |
|---|---|
| `id` | `hollis-office-desktop-elena` |
| `analyst-name` | `K. Vance` |
| `artifact-flag` | `POCTF{...}` |
| `case-notes` | Subject: E. Marchetti disappearance. Chain of custody initiated 2026-06-29. See docket MARCHETTI/2026-14. |

`artifact-flag` is the flag:

```
POCTF{██████████████████████████████████████████████████}
```

As a sanity check, `cat` on the raw `.jsonlz4` already shows readable JSON fragments — LZ4 stores unmatched bytes as literals, so short strings survive verbatim inside the compressed block even before decompression.

The brief's "pay attention to the details" is not idle. `logins.json` contains two entries whose `encryptedUsername` and `encryptedPassword` are not encrypted at all, only base64:

```
hollis.edu   → e.marchetti@hollis.edu
pastebin.com → anon-analyst / hunter2
```

None of this is needed for the flag, but it is sitting in the same profile, and an "anon-analyst" account is exactly the kind of thing a later stage picks up.