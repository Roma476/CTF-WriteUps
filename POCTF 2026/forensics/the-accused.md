# The Accused

| | |
|---|---|
| **Section** | wave 8 |
| **Category** | forensics |
| **Solves** | 67 |

## Overview

The challenge provides Marion Halberd's outbox, a tarball containing six apparatus session logs and a passwd fragment, and a telnet capture of an attempted log wipe. The live session filenames carried subject tags, but log rotation stripped those tags before the archives were written. The surviving logs therefore identify only an operator code and a subject code. The challenge page explicitly warns that this is the team's one and only accusation: a correct token paired with the wrong accused permanently closes the case, awards zero points, forfeits Good Gumshoe, and allows no retries. The README adds that the case-solved achievement depends on the accusation, not on earning the flag on a later retry. The task is to identify Elena Marchetti's session and the operator who ran it.

## Solve

The tarball contains six logs. Only `session_QBRM7DGJ3WVZ3ZEX.log.1` has `frame=IV`, `subject-selection-protocol=BYPASSED`, `safety-interlocks=OVERRIDE (operator)`, and `subject=SBJ_14`; it runs from 22:14 to 23:03 on 2026-06-28. The other five are Frame I/STANDARD sessions. The 06/25 log is explicitly identified in the outbox as the Weiss subject, SBJ_17, so it is a deliberate red herring.

The outbox email from Halberd at 23:07 on 06/28 says the "Marchetti issue" was logged "under the Frame IV catalog with the standard designation." Since QBRM is the only Frame IV log, `SBJ_14` is Elena Marchetti.

The passwd fragment maps the QBRM operator code to a name: `APP_OPR_7` is `Marion Halberd`. The telnet capture corroborates this: the login is `halberd`, and the session tries `rm session_*_marchetti.log*` and `rm *marchetti*`. Both fail because rotation stripped the subject tag, and the attacker's own comment reads `# rotator stripped the tag. nothing to grep.` The capture's `ls` also lists QBRM in the live directory, making it the only session ID common to the capture and the surviving tarball; the page states the required token is the `session_id` inside the tarball.

Marion Halberd is therefore both the operator of Elena's session and the person who attempted to destroy its log. The accepted answer was the session token `████████████████` with the accusation `marion_halberd` (Prof. Marion Halberd).