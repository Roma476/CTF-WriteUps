# Un giro sugli "alberi"

| | |
|---|---|
| **Section** | HighSchools CTF Workshop - 2023 Bari |
| **Category** | osint |
| **Solves** | 293 |

## Overview

The challenge gives us the Facebook profile of a "shady individual" (`https://www.facebook.com/profile.php?id=100091620543560`), who asked for help in a post. A Facebook account is required to view it.

The profile itself is almost empty: the only interesting content is a post containing a fake flag, which is a decoy. Nothing else on the profile is useful, so the next step is to pivot to other platforms. The profile's username, `GabiBOH0205`, can be reused as a handle on other social networks, so I enumerated accounts registered with the same name using `sherlock`.

## Solve

```
$ sherlock GabiBOH0205
[*] Checking username GabiBOH0205 on:

[+] F3.cool: https://f3.cool/GabiBOH0205/
[+] GitHub: https://www.github.com/GabiBOH0205
[+] Lichess: https://lichess.org/@/GabiBOH0205
[+] Pastebin: https://pastebin.com/u/GabiBOH0205
[+] TikTok: https://www.tiktok.com/@GabiBOH0205
[+] Trakt: https://www.trakt.tv/users/GabiBOH0205
[+] YouTube: https://www.youtube.com/@GabiBOH0205
```

Among the hits, the Pastebin profile stands out: it contains a single paste, with this content:

```
1. Belle le foreste: https://linktr.ee/gabibbari2023
```

The paste points to a Linktree page (`gabibbari2023`). Opening it, the flag is listed among the links on the page.