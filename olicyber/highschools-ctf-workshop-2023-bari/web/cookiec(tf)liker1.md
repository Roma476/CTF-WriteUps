# CookieC(TF)liker1

| | |
|---|---|
| **Section** | HighSchools CTF Workshop - 2023 Bari |
| **Category** | web |
| **Solves** | 656 |

## Overview

The challenge gives us a website (`http://cookie.challs.olicyber.it`) described as an idle game that "hides something". The site is a simple clicker: it counts how many times the cookie on the page is clicked, and nothing else is visible from the UI.

Since everything runs client-side, the next step is to look at the page source and at the JavaScript it loads.

## Solve

Opening the page source with `Ctrl+U` shows the script loaded by the page, `main.js`. At the very beginning of the file there are two suspicious constants, `sus` and `sus2`, whose values look like base64 strings:

```js
let counter = 0;
let checker = true;
const elemCounter = document.querySelector("#counter");
const sus = "SVRBU0VDe0IxNWN1MTc1XzRyM18zdjFMIX0="
const sus2 = "aHR0cHM6Ly93d3cueW91dHViZS5jb20vd2F0Y2g/dj1kUXc0dzlXZ1hjUQo="
const rainyContainer = document.getElementById("rainy-container");
const body = document.body;
```

Decoding both strings from base64, `sus` gives the flag, while `sus2` turns out to be a rickroll.