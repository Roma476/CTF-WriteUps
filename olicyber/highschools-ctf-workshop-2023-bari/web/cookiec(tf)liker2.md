# CookieC(TF)liker2

| | |
|---|---|
| **Section** | HighSchools CTF Workshop - 2023 Bari |
| **Category** | web |
| **Solves** | 573 |

## Overview

This is the second part of the cookie clicker challenge, on the same website (`http://cookie.challs.olicyber.it`). The description adds a hint: the site seems to have "demands too hard to satisfy", suggesting that something happens once a certain condition is met while playing.

The site is the same clicker as before, which counts how many times the cookie on the page is clicked.

## Solve

Clicking the cookie 10 times and then refreshing the page makes a real cookie appear in the browser (an actual HTTP cookie of the site, not the in-game one). Inspecting the site's cookies, its value contains the flag.